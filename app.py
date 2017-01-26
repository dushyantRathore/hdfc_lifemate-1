import os
import json
import pickle
import sys
import md5
import magic

import requests

from flask import Flask, request, send_file, send_from_directory

import constants

import templates as tp

import qr_utils
import templates

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
    print(json.dumps(data, indent=2))  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                sender_id = messaging_event["sender"]["id"]
                recipient_id = messaging_event["recipient"]["id"]

                # Someone sent us a message
                if messaging_event.get("message"):
                    
                    message_text = messaging_event["message"].get("text")
                    flag_received = get_flag()
                    if not flag_received:
                        flag_received = {}

                    if message_text:
                        message_text = message_text.lower()

                    if message_text == "login":
                        send_message(sender_id, "Enter your Login ID : ")
                        flag = {
                            'section' : 'main',
                            'sub-section' : 'username'
                        }
                        update_flag(flag)

                    if flag_received.get('sub-section') == "username":
                        send_message(sender_id, "Enter your Password : ")
                        flag = {
                            'section' : 'main',
                            'sub-section' : 'password'
                        }
                        update_flag(flag)

                    if flag_received.get('sub-section') == "password":
                        send_message(sender_id, "You have successfully Logged In", flag = {'section' : 'main', 'sub-section' : ''})


                    # Code to handle insurance product queries of the users
                    if flag_received.get('section') == 'insurance_help' and message_text:
                            insurance_name = flag_received.get('sub-section')
                            log_to_messenger(sender_id, insurance_name, "Query for")
                            if "eligibi" in message_text:
                                elgibility_path = os.path.join(insurance_name, 'eligibility.png')
                                create_image_message(sender_id, elgibility_path, True)
                            elif "premium" in message_text:
                                premium_path = os.path.join(insurance_name, 'premium.png')
                                create_image_message(sender_id, premium_path, True)
                            elif "option" in message_text:
                                options_path = os.path.join(insurance_name, 'options.png')
                                create_image_message(sender_id, options_path, True)
                            else:
                                send_message(sender_id, "For more details, please refer : \n" + constants.brochure_links.get(insurance_name))
                    else:
                        print message_text
                        send_message(sender_id, "Heyy!!")

                # delivery confirmation
                if messaging_event.get("delivery"):
                    pass

                # optin confirmation
                if messaging_event.get("optin"):
                    pass

                # optin confirmation
                if messaging_event.get("attachments"):
                    log_to_messenger(sender_id, "attachment received!")
                    if messaging_event["message"]["attachments"][0]["type"] == "image":
                        log("Image received from user.")
                        image_url = messaging_event["message"]["attachments"][0]["payload"]["url"]
                        log(image_url)
                        update_image_url(image_url)
                        filename = save_image_from_url()
                        user_data = qr_utils.decode_aadhar_from_qr(filename, True)
                        send_message(sender_id, user_data)




                # user clicked/tapped "postback" button in earlier message
                if messaging_event.get("postback"):
                    payload_received = messaging_event["postback"].get("payload")
                    log_to_messenger(sender_id, payload_received, "payload")

                    if payload_received == "getstarted":  # Get Started
                        tp.quickreplies_getstarted(sender_id)
                        flag = {
                            'section':'main',
                            'sub-section': ''
                        }
                        update_flag(flag)

                    elif payload_received == "member_yes":  # A Registered Member
                        send_message(sender_id, "Kindly enter your userID : ")

                    elif payload_received == "member_no":  # Not a Registered Member
                        send_message(sender_id, "Please send your AADHAAR card Image/Scan")

                    elif payload_received == "view_insurance":  # View Insurance Offered
                        sender_id = messaging_event["sender"]["id"]
                        print(sender_id)
                        tp.create_view_insurance_list(sender_id)

                    elif payload_received.startswith('view_insurance_'):  # View Insurance Offered - Other Features
                        insurance_name = payload_received.split('_')[-1]
                        features_path = os.path.join(insurance_name, 'features.png')
                        create_image_message(sender_id, features_path, True)
                        send_message(sender_id, "Anything else I can help you with?",flag={"section" : "insurance_help", "sub-section" : insurance_name})
                        log_to_messenger(sender_id, features_path, "image_path")

                    elif payload_received == "apply":  # Best for me / Apply Option
                        send_message(sender_id, "Woohoo")

                    elif payload_received == "claim":  # Claim Option
                        tp.create_claim_type_list(sender_id)

                    elif payload_received == "natural_death":  # Claim -> Natural Death
                        send_message(sender_id, "Please upload the following documents (PDF/Scan) : "
                                                "\n1. Death Certificate"
                                                "\n2. Original Policy Documents"
                                                "\n3. Medical Records")

                    elif payload_received == "critical_illness":  # Claim -> Critical Illness
                        send_message(sender_id, "Please upload the following documents (PDF/Scan) : "
                                                "\n1. Medical Records"
                                                "\n2. Original Policy Documents")

                    elif payload_received == "account":  # My Account
                        tp.create_account_list(sender_id)

                    elif payload_received == "view_account_policies":  # My Account -> View Policies
                        tp.create_account_policies_list(sender_id)

                    elif payload_received == "pay_remind":  # My Account -> View Policies -> Pay Option
                        tp.create_pay_remind_list(sender_id)

                    elif payload_received == "remind":  # My Account -> View Policies -> Remind Option
                        send_message(sender_id, "Your Reminder has been set")

                    elif payload_received == "view_account_funds":  # My Account -> View Funds
                        send_message(sender_id, "Your account funds are as follows : ")
                        image_url1 = "funds/User1.jpeg"
                        create_image_message(sender_id, image_url1, True)
                        image_url2 = "funds/User1.png"
                        create_image_message(sender_id, image_url2, True)

                    elif payload_received == "view_account_history":  # My Account -> View History
                        send_message(sender_id, "Your account history is as follows : ")
                        image_url = "history/User1.png"
                        create_image_message(sender_id, image_url, True)

                    elif payload_received == "support":  # Support
                        send_message(sender_id, "Woohoo")


    return "ok", 200


def update_flag(val):
    fname = "flag.p"
    fileObj = open(fname,'wb')
    pickle.dump(val,fileObj)
    fileObj.close()


def get_flag():
    try:
        fname = "flag.p"
        fileObj = open(fname, 'r')
        return pickle.load(fileObj)
    except:
        return None


def reset_flag():
    fname = "flag.p"
    fileObj = open(fname,'wb')
    pickle.dump(None,fileObj)
    fileObj.close()


def update_image_url(image_url):
    fname = "image_url.p"
    fileObj = open(fname,'wb')
    pickle.dump(image_url,fileObj)
    fileObj.close()


def get_image_url():
    try:
        fname = "image_url.p"
        fileObj = open(fname, 'r')
        return pickle.load(fileObj)
    except:
        return None


def send_message(recipient_id, message_text, flag={}):

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
    print(json.dumps(str(message), indent=4))
    sys.stdout.flush()


def save_image_from_url(image_url='', image_name=''):
    if not image_url:
        image_url = get_image_url()
    session = requests.session()
    response = session.get(image_url)
    filename = image_name
    if not image_name:
        filename = 'image_%s.jpeg' % md5.new(image_url).hexdigest()
    with open(filename, 'wb') as handle:
        for block in response.iter_content(1048576):
            if not block:
                break
            handle.write(block)
        handle.close()
    mimetype = magic.from_file(filename, mime=True)
    if not mimetype.startswith('image/'):
        raise Exception('Not an image: ' + mimetype)
    if os.stat(filename).st_size > 3072 * 1024:  # 3MB? unsure
        raise Exception('Bigger than 3MB')
    else:
        # filename = sys.argv[1]
        log("Shouldn't be here.")
    result = ic.find_type(filename)
    return filename


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
    tp.post_request(image_message)


# ------------------- Run App ---------------------- #

if __name__ == '__main__':
    app.run(debug=True)