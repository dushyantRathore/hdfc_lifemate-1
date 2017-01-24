import os
import json
import pickle
import sys

import requests
from flask import Flask, request

app = Flask(__name__)

INSURANCE_IMAGES_DIRECTORY = "images/"


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                sender_id = messaging_event["sender"]["id"]
                recipient_id = messaging_event["recipient"]["id"]

                # someone sent us a message
                if messaging_event.get("message"):
                    if messaging_event.get("message").get("text"):
                        message_text = messaging_event["message"]["text"]
                        print message_text
                        send_message(sender_id, "Heyy!!")

                # delivery confirmation
                if messaging_event.get("delivery"):
                    pass

                # optin confirmation
                if messaging_event.get("optin"):
                    pass

                # user clicked/tapped "postback" button in earlier message
                if messaging_event.get("postback"):
                    payload_received = messaging_event["postback"].get("payload")
                    if payload_received == "view_insurance":
                        sender_id = messaging_event["sender"]["id"]
                        print(sender_id)
                        create_view_insurance_list(sender_id)
                    elif payload_received == "apply":
                        create_yes_no_button_message(sender_id, "hell_yeah", "YES or NO")
                    elif payload_received == "history":
                        create_image_message(sender_id, 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Thats_all_folks.svg/2000px-Thats_all_folks.svg.png')
                    elif payload_received.startswith('view_insurance_'):
                        insurance_name = payload_received.split('_')[-1]
                        features_path = os.path.join(INSURANCE_IMAGES_DIRECTORY, insurance_name, "features.png")
                        create_image_message(sender_id, features_path)
                        send_message(sender_id, "Any further queries?", flag={"view":insurance_name})

    return "ok", 200

def update_flag(val):
    fname = "flag.p"
    fileObj = open(fname,'wb')
    pickle.dump(loc,fileObj)
    fileObj.close()

def get_location():
    try:
        fname = "flag.p"
        fileObj = open(fname, 'r')
        return pickle.load(fileObj)
    except:
        return None


def send_message(recipient_id, message_text, flag=''):

    log("sending message to {recipient}: {text}".format(
        recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

    if flag:
        update_flag(flag)


def log(message):  # simple wrapper for logging to stdout on heroku
    print (str(message))
    sys.stdout.flush()


def create_generic_template(sender_id, name, subtitle, image_url, phone, navigation_url):
    log("inside create generic template method")
    response_msg = json.dumps(
        {"recipient": {"id": sender_id},
         "message": {
             "attachment": {
                 "type": "template",
                 "payload": {
                     "template_type": "generic",
                     "elements": [
                         {
                             "title": name,
                             "subtitle": subtitle,
                             "image_url": image_url,
                             "buttons": [
                                 {
                                     "type": "postback",
                                     "payload": "Call",
                                     "title": "Call"
                                 },
                                 {
                                     "type": "web_url",
                                     "title": "Navigate",
                                     "url": navigation_url
                                 }
                             ]
                         }
                     ]
                 }
             }
         }
         })
    post_request(response_msg)


def create_yes_no_button_message(sender_id, context, question_text):
    button_message = json.dumps({
    "recipient":{
                    "id": sender_id
                },
    "message":{
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "HDFC Life currently offers following products, please select one of them",
                "buttons": [
                          {
                            "type":"postback",
                            "title":"Yes",
                            "payload":context+"_yes"
                          },
                          {
                            "type":"postback",
                            "title":"No",
                            "payload":context+"_no"
                          }
                    ]
                }
            }
        }
    })

    post_request(button_message)


def create_view_insurance_list(sender_id):
    print(sender_id)
    insurance_list_template = json.dumps({
  "recipient":{
    "id":sender_id
  }, "message": {
    "attachment": {
        "type": "template",
        "payload": {
            "template_type": "list",
            "top_element_style": "compact",
            "elements": [
                {
                    "title": "HDFC Life Insurance Plans",
                    "subtitle": "Please choose a plan of your interest",
                },
                {
                    "title": "Click2Protect",
                    "subtitle": "HDFC Life Insurance Plan",
                    "buttons": [
                        {
                            "title": "View",
                            "type": "postback",
                            "payload": "view_insurance_life"
                        }
                    ]                
                },
                {
                    "title": "Click2Invest",
                    "subtitle": "HDFC Life Investment Plan",
                    "buttons": [
                        {
                            "title": "View",
                            "type": "postback",
                            "payload": "view_insurance_invest"
                        }
                    ]
                },
                {
                    "title": "Easy Health",
                    "subtitle": "HDFC Health Insurance Plan",
                    "buttons": [
                        {
                            "title": "View",
                            "type": "postback",
                            "payload": "view_insurance_health"
                        }
                    ]
                },
                {
                    "title": "Cancer Care",
                    "subtitle": "HDFC Cancer Care Plan",
                    "buttons": [
                        {
                            "title": "View",
                            "type": "postback",
                            "payload": "view_insurance_cancer"
                        }
                    ]
                }
            ],
        }
    }
}
    
})

    post_request(insurance_list_template)


def post_request(body):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers,
                      data=body)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def create_image_message(sender_id, image_url):

    image_message = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image_url
                }
            }
        }
})

if __name__ == '__main__':
    app.run(debug=True)
