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

                if messaging_event.get("message"):  # someone sent us a message

                    # the facebook ID of the person sending you the message
                    # the recipient's ID, which should be your page's facebook
                    # ID
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = messaging_event["message"][
                        "text"]  # the message's text

                    send_message(sender_id, "Hii bitches!")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                # user clicked/tapped "postback" button in earlier message
                if messaging_event.get("postback"):
                    payload_received = messaging_event[
                        "postback"].get("payload")
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
            "elements": [
                {
                    "title": "Classic T-Shirt Collection",
                    "image_url": "https://peterssendreceiveapp.ngrok.io/img/collection.png",
                    "subtitle": "See all our colors",
                    "default_action": {
                        "type": "web_url",
                        "url": "https://peterssendreceiveapp.ngrok.io/shop_collection",
                        "messenger_extensions": True,
                        "webview_height_ratio": "tall",
                        "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                    },
                    "buttons": [
                        {
                            "title": "View",
                            "type": "web_url",
                            "url": "https://peterssendreceiveapp.ngrok.io/collection",
                            "messenger_extensions": True,
                            "webview_height_ratio": "tall",
                            "fallback_url": "https://peterssendreceiveapp.ngrok.io/"                        
                        }
                    ]
                },
                {
                    "title": "Classic White T-Shirt",
                    "image_url": "https://peterssendreceiveapp.ngrok.io/img/white-t-shirt.png",
                    "subtitle": "100% Cotton, 200% Comfortable",
                    "default_action": {
                        "type": "web_url",
                        "url": "https://peterssendreceiveapp.ngrok.io/view?item=100",
                        "messenger_extensions": True,
                        "webview_height_ratio": "tall",
                        "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                    },
                    "buttons": [
                        {
                            "title": "Shop Now",
                            "type": "web_url",
                            "url": "https://peterssendreceiveapp.ngrok.io/shop?item=100",
                            "messenger_extensions": True,
                            "webview_height_ratio": "tall",
                            "fallback_url": "https://peterssendreceiveapp.ngrok.io/"                        
                        }
                    ]                
                },
                {
                    "title": "Classic Blue T-Shirt",
                    "image_url": "https://peterssendreceiveapp.ngrok.io/img/blue-t-shirt.png",
                    "subtitle": "100% Cotton, 200% Comfortable",
                    "default_action": {
                        "type": "web_url",
                        "url": "https://peterssendreceiveapp.ngrok.io/view?item=101",
                        "messenger_extensions": True,
                        "webview_height_ratio": "tall",
                        "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                    },
                    "buttons": [
                        {
                            "title": "Shop Now",
                            "type": "web_url",
                            "url": "https://peterssendreceiveapp.ngrok.io/shop?item=101",
                            "messenger_extensions": True,
                            "webview_height_ratio": "tall",
                            "fallback_url": "https://peterssendreceiveapp.ngrok.io/"                        
                        }
                    ]                
                },
                {
                    "title": "Classic Black T-Shirt",
                    "image_url": "https://peterssendreceiveapp.ngrok.io/img/black-t-shirt.png",
                    "subtitle": "100% Cotton, 200% Comfortable",
                    "default_action": {
                        "type": "web_url",
                        "url": "https://peterssendreceiveapp.ngrok.io/view?item=102",
                        "messenger_extensions": True,
                        "webview_height_ratio": "tall",
                        "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                    },
                    "buttons": [
                        {
                            "title": "Shop Now",
                            "type": "web_url",
                            "url": "https://peterssendreceiveapp.ngrok.io/shop?item=102",
                            "messenger_extensions": True,
                            "webview_height_ratio": "tall",
                            "fallback_url": "https://peterssendreceiveapp.ngrok.io/"                        
                        }
                    ]                
                }
            ],
             "buttons": [
                {
                    "title": "View More",
                    "type": "postback",
                    "payload": "payload"                        
                }
            ]  
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
