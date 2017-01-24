import os
import json
import pickle
import sys

import requests

from flask import Flask, request, send_file, send_from_directory

app = Flask(__name__)

INSURANCE_IMAGES_DIRECTORY = "images"


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

@app.route('/images/<path:filename>', methods=['GET'])
def return_image(filename):
    print(filename)
    return send_from_directory(INSURANCE_IMAGES_DIRECTORY, filename, mimetype='image/png')


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
                    log_to_messenger(sender_id, payload_received, "payload")
                    if payload_received == "view_insurance":
                        sender_id = messaging_event["sender"]["id"]
                        print(sender_id)
                        create_view_insurance_list(sender_id)
                    elif payload_received == "apply":
                        send_message(sender_id, "Woohoo")
                    elif payload_received == "claim":
                        send_message(sender_id, "Woohoo")
                    elif payload_received == "account":
                        create_account_list(sender_id)
                    elif payload_received == "view_account_policies":
                        create_account_policies_list(sender_id)
                    elif payload_received == "view_account_funds":
                        send_message(sender_id, "Woohoo")
                    elif payload_received == "view_account_history":
                        send_message(sender_id, "Woohoo")
                    elif payload_received == "help":
                        send_message(sender_id, "Woohoo")
                    elif payload_received.startswith('view_insurance_'):
                        insurance_name = payload_received.split('_')[-1]
                        features_path = os.path.join(insurance_name, 'features.png')
                        create_image_message(sender_id, features_path, True)
                        log_to_messenger(sender_id, features_path, "image_path")

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


def log_to_messenger(sender_id, data):
    send_message(sender_id, str(data))


def log_to_messenger(sender_id, data, context=""):
    send_message(sender_id, context + ": " + str(data))


def log(message):  # simple wrapper for logging to stdout on heroku
    print (str(message))
    sys.stdout.flush()


# ------------------------ Insurance Plans List ------------------------- #


def create_view_insurance_list(sender_id):
    insurance_list_template = json.dumps({
    "recipient":{"id":sender_id
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
                }
            ],
        }
    }
}
    
})

    post_request(insurance_list_template)

# ---------------------- My account List --------------------- #


def create_account_list(sender_id):
    account_list_template = json.dumps({
        "recipient": {
            "id": sender_id
        }, "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "list",
                    "top_element_style": "compact",
                    "elements": [
                        {
                            "title": "Account Details",
                            "subtitle": "Get your Account Details",
                        },
                        {
                            "title": "My Policies",
                            "subtitle": "Check the policies associated with your account",
                            "buttons": [
                                {
                                    "title": "View",
                                    "type": "postback",
                                    "payload": "view_account_policies"
                                }
                            ]
                        },
                        {
                            "title": "My Funds",
                            "subtitle": "Check the funds associated with your account",
                            "buttons": [
                                {
                                    "title": "View",
                                    "type": "postback",
                                    "payload": "view_account_funds"
                                }
                            ]
                        },
                        {
                            "title": "Premium History",
                            "subtitle": "Check your Premium History",
                            "buttons": [
                                {
                                    "title": "View",
                                    "type": "postback",
                                    "payload": "view_account_history"
                                }
                            ]
                        }
                    ]
                }
            }
        }

    })

    post_request(account_list_template)


# ----------------------- Account Policies List -------------------------- #
def create_account_policies_list(sender_id):
    policies_list_template = json.dumps({
        "recipient": {"id": sender_id
                      }, "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "list",
                    "top_element_style": "compact",
                    "elements": [
                        {
                            "title": "Account Policies",
                            "subtitle": "Details of the policies associated with your account",
                        },
                        {
                            "title": "Click2Protect",
                            "subtitle": "Premium - 40,000"
                                        "\nDue Date - 29/01/2017 ",
                            "buttons": [
                                {
                                    "title": "Pay/Remind",
                                    "type": "postback",
                                    "payload": "pay_remind"
                                }
                            ]
                        },
                        {
                            "title": "Click2Invest",
                            "subtitle": "Premium - 20,000"
                                        "\nDue Date - 05/03/2017 ",
                            "buttons": [
                                {
                                    "title": "Pay/Remind",
                                    "type": "postback",
                                    "payload": "pay_remind"
                                }
                            ]
                        },
                        {
                            "title": "Cancer Care",
                            "subtitle": "Premium - 80,000"
                                        "\nDue Date - 06/05/2017 ",
                            "buttons": [
                                {
                                    "title": "Pay/Remind",
                                    "type": "postback",
                                    "payload": "pay_remind"
                                }
                            ]
                        }
                    ]
                }
            }
        }

    })

    post_request(policies_list_template)

# ------------------------ Post Request -------------------- #


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

# -------------------- Image Creation ----------------------- #


def create_image_message(sender_id, image_url, from_system=False):

    if from_system:
        image_url = "https://sheltered-falls-53215.herokuapp.com/images/" + image_url

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
    post_request(image_message)

# ------------------- Run App ---------------------- #

if __name__ == '__main__':
    app.run(debug=True)