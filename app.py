import os
import json
import pickle
import sys
import md5
import magic
import time
import random
import requests

from flask import Flask, request, send_file, send_from_directory

import constants

import templates as tp

import qr_utils
import templates
import faq
import location

app = Flask(__name__)

INSURANCE_IMAGES_DIRECTORY = "images"
QR_CODE_DIRECTORY = os.path.join('images', 'qr')
WEB_URL = 'http://hdfc-support.mybluemix.net/submitFeedback'
USER_MAP = {
    "satwik": "1150846678361142",
    "dushyant": "1311151252277587"
}
INVERSE_USER_MAP = {v: k for k, v in USER_MAP.iteritems()}

password = ["abc", "xyz", "uvw"]


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


@app.route('/update-dashboard/<jobID>', methods=['GET'])
def post_to_dashboard(jobID):
    print(jobID)
    time.sleep(15)
    translation = getTranslation(jobID)
    if translation:
        return send_feedback_to_web(text=str(translation))
    else:
        return "couldn't decode"


@app.route('/send_message', methods=['POST'])
def send_message_via_api():
    data = request.form
    username = data.get("username")
    text = data.get("alert")
    try:
        send_message(USER_MAP[username], text)
        return "Success"
    except Exception, err:
        return "Failed! Error: "+ str(err)


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    print(json.dumps(data, indent=2))  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                # Someone sent us a message
                if messaging_event.get("message"):

                    if messaging_event.get("message").get("text"):
                        sender_id = messaging_event["sender"]["id"]
                        message_text =  messaging_event.get("message").get("text")

                        flag_received = get_flag() # Get the Flag
                        if not flag_received:
                            flag_received = {}

                        if message_text:
                            message_text = message_text.lower()

                        # Code for main section (handles login and rest)
                        if flag_received.get('section') == 'main' and message_text:

                            if message_text == "login":
                                send_message(sender_id, "Enter your Login ID")
                            elif len(message_text) == 6:
                                send_message(sender_id, "Enter your password")
                            elif message_text in password:
                                send_message(sender_id, "You have successfully logged in")
                                send_message(sender_id, "Use the persistent menu to explore the features of the bot")
                            elif message_text == "sign up":
                                send_message(sender_id, "Please share your AADHAAR Card QR")

                            elif message_text == "hi" or message_text == "hello" or message_text == "hey" or message_text == "start" or message_text == "begin" or message_text == "yo" :

                                token = os.environ["PAGE_ACCESS_TOKEN"]
                                user_details_url = "https://graph.facebook.com/v2.6/%s" % sender_id
                                user_details_params = {'fields': 'first_name,last_name,profile_pic',
                                                       'access_token': token}

                                user_details = requests.get(user_details_url, user_details_params).json()
                                send_message(sender_id, "Hello " + user_details['first_name'] + " " + user_details['last_name'] + ":). Welcome to HDFC Lifemate!")
                            elif flag_received.get('sub-section')=="remind":
                                send_message(sender_id, "Allright! I'll remind you :)")

                        # Code to handle insurance product queries of the users
                        elif flag_received.get('section') == 'insurance_help' and message_text:
                                insurance_name = flag_received.get('sub-section')
                                log_to_messenger(sender_id, insurance_name, "Query for")
                                if "featu" in message_text :
                                    feature_path =  os.path.join(insurance_name, 'features.png')
                                    create_image_message(sender_id, feature_path, True)
                                elif "eligibi" in message_text:
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

                        elif flag_received.get('section') == 'support':
                            if message_text == "yes":
                                send_message(sender_id, "I'm glad :)")
                                update_flag(
                                    {
                                        "section": "support",
                                        "sub-section":"satisfied"
                                    })
                            elif message_text == "no":
                                tp.create_alternate_support_list(sender_id)
                                update_flag(
                                    {
                                        "section": "support",
                                        "sub-section": "alternate-support"
                                    })
                            elif flag_received.get('sub-section') == "auto-answer":
                                ans = faq.closest_matching_answer(message_text)
                                send_message(sender_id, ans)
                                tp.quickreplies_satisfied(sender_id)
                            elif flag_received.get('sub-section') == "complaint-provided":
                                ref_no = "1254984"
                                data = json.dumps({
                                    "description" :message_text,
                                    "complaint_number": ref_no
                                    })
                                if sender_id=="407924042881094":
                                    pass
                                else:
                                    send_feedback_to_web("dushyant", message_text)
                                qr_image_path = qr_utils.create_qr(data, 'images/qr/xyz.png')
                                create_image_message(sender_id, qr_image_path, True)
                                tp.send_qr_code_template(sender_id, 'https://sheltered-falls-53215.herokuapp.com/images/qr/xyz.png')

                        elif flag_received.get('section') == 'bestforme' and message_text:
                            if message_text == "less than 35" or message_text == "35-45" or message_text == "greater than 45":
                                tp.create_apply_gender_list(sender_id)
                            elif message_text == "male" or message_text == "female":
                                tp.create_apply_marital_status_list(sender_id)
                            elif message_text == "married" or message_text == "unmarried" or message_text == "divorced":
                                tp.create_occupation_list(sender_id)
                            elif message_text == "self employed" or message_text == "government job" or message_text == "private job" :
                                tp.create_income_list(sender_id)
                            if message_text == "below 5 Lakhs" or message_text == "5 to 10 lakhs" or message_text == "greater than 10 lakhs":
                                send_message(sender_id, "HDFC Life recommends the following top 3 plans : "
                                                        "\n1. Click2Protect Plus Plan"
                                                        "\nApply - https://onlineinsurance.hdfclife.com/buy-online-term-insurance-plans/click-2-protect-plus/Life?source=W-TEBT_PP_CPP_BodyBO1_2015&agentcode=00399206"
                                                        "\n2. HDFC Life ProGrowth Plus"
                                                        "\nApply - https://onlineinsurance.hdfclife.com/buy-online-investment-plans/progrowth-plus-ulip-plan?source=W_TEBT_PP_UPS_BodyBO_UPS&agentcode=00399206"
                                                        "\n3.HDFC Super Income Plan"
                                                        "\nApply - https://onlineinsurance.hdfclife.com/buy-online-savings-plans/super-income-plan?source=W_TEBT_PP_MBU_BodyBO1_2015&agentcode=00399206")

                        else:
                            print message_text
                            send_message(sender_id, "Heyy!!")

                    if messaging_event.get("message").get("attachments"):
                        sender_id = messaging_event["sender"]["id"]
                        if messaging_event["message"]["attachments"][0]["type"] == "image":
                            log_to_messenger(sender_id, "Image received from user.")
                            image_url = messaging_event["message"]["attachments"][0]["payload"]["url"]
                            log(image_url)
                            update_image_url(image_url)
                            filename = save_image_from_url(is_qr=True)
                            log_to_messenger(sender_id, filename, "Image path:")
                            user_data = qr_utils.decode_aadhar_from_qr(filename, True)
                            string_to_send = "Test string"
                            if user_data:
                                user_data = json.loads(user_data)
                                string_to_send = '\n'.join([str(k)+ "\t:" + str(v) for k,v in user_data.iteritems()])
                            send_message(sender_id, string_to_send)
                            tp.create_yes_no_button(sender_id, "Confirm Details?", "aadhar")
                        if messaging_event["message"]["attachments"][0]["type"] == "location":
                            flag_received = get_flag()
                            if flag_received == {'section':'support','sub-section':'location-asked'}:
                                log_to_messenger(sender_id, "Location received from user.")
                                lat = float(messaging_event["message"]["attachments"][0]["payload"]["coordinates"]["lat"])
                                lng = float(messaging_event["message"]["attachments"][0]["payload"]["coordinates"]["long"])
                                d = {"lat": lat, "lng": lng}
                                log_to_messenger(sender_id, str(d), "coordinates")
                                update_location(d)
                                hdfc_life_ceneter_results = location.find_contacts(get_location(), "insurance")
                                data = json.loads(hdfc_life_ceneter_results)
                                for i in range(0, len(data)):
                                    j = data[i]
                                    subtitle =  "Distance : " + j["distance"] + "\t Time : \t" + j["time"] + " /n" + j["address"]
                                    tp.create_generic_template(sender_id, j["name"], subtitle, j["image_url"], j["phone"], j["url"] )

                # user clicked/tapped "postback" button in earlier message
                if messaging_event.get("postback"):
                    payload_received = messaging_event["postback"].get("payload")
                    sender_id = messaging_event["sender"]["id"]
                    log_to_messenger(sender_id, payload_received, "payload")

                    if payload_received == "getstarted":  # Get Started
                        reset_flag()
                        tp.quickreplies_getstarted(sender_id)
                        flag_to_update = {
                            'section':'main',
                            'sub-section': ''
                        }
                        update_flag(flag_to_update)

                    elif payload_received == "view_insurance":  # View Insurance Offered
                        sender_id = messaging_event["sender"]["id"]
                        print(sender_id)
                        tp.create_view_insurance_list(sender_id)

                    elif payload_received.startswith('view_insurance_'):  # View Insurance Offered - Other Features
                        insurance_name = payload_received.split('_')[-1]

                        # Description
                        send_message(sender_id, "Description"
                                                "\n1. A simple way to get comprehensive protection at an affordable price"
                                                "\n2. Protect yourself and your loved ones"
                                                "\n3. Provides a benefit amount in the unfortunate event of Death"
                                                "\n4. Ease out the financial worries of your family")

                        # List Template - Benefits
                        tp.view_insurance_life_benefits(sender_id)

                        # List Templates - Things to Keep in Mind
                        tp.important(sender_id)

                        # Graph
                        create_image_message(sender_id, "Graph.jpg", True)

                        send_message(sender_id, "Anything else I can help you with?",flag={"section" : "insurance_help", "sub-section" : insurance_name})

                    elif payload_received == "apply":  # Best for me / Apply Option
                        send_message(sender_id, "Please select the appropriate options", flag={"section" : "bestforme", "sub-section" : ""})
                        tp.create_apply_age_list(sender_id)

                    elif payload_received == "claim":  # Claim Option
                        tp.create_claim_type_list(sender_id)

                    elif payload_received == "aadhar_yes":  # View Insurance Offered
                        send_message(sender_id, "Thankyou! Your details have been recorded :)")
                        send_message(sender_id, "Now you can login with your Aadhar Number!")

                    elif payload_received == "aadhar_no":  # View Insurance Offered
                        send_message(sender_id, "Please scan the QR code again")

                    elif payload_received == "natural_death":  # Claim -> Natural Death
                        send_message(sender_id, "Your request has been registered, please keep the following documents ready : "
                                                "\n1. Death Certificate"
                                                "\n2. Original Policy Documents"
                                                "\n3. Medical Records"
                                                "\n4. Claim Form - http://www.hdfclife.com/iwov-resources/pdf/customerservice/HDSL%20Statement%20of%20Death%20Claim.pdf")
                        send_message(sender_id, "Thank You, our executive shall get in touch with you within the next 48 hours.")

                    elif payload_received == "critical_illness":  # Claim -> Critical Illness
                        send_message(sender_id, "Your request has been registered, please keep the following documents ready : "
                                                "\n1. Medical Records"
                                                "\n2. Original Policy Documents"
                                                "\n3. Claim Form - https://www.hdfclife.com/iwov-resources/pdf/customerservice/health/criticare/CriticalIllness.pdf")
                        send_message(sender_id, "Thank You, our executive shall get in touch with you within the next 48 hours.")

                    elif payload_received == "account":  # My Account
                        tp.create_account_list(sender_id)

                    elif payload_received == "view_account_policies":  # My Account -> View Policies
                        tp.create_account_policies_list(sender_id)

                    elif payload_received == "pay_remind":  # My Account -> View Policies -> Pay Option
                        tp.create_pay_remind_list(sender_id)

                    elif payload_received == "remind":  # My Account -> View Policies -> Remind Option
                        update_flag({
                            "section":"main",
                            "sub-section":"remind"
                            })
                        send_message(sender_id, "When do you want me to remind me?")
                        time.sleep(6)
                        send_message(sender_id, "Allright I'll remind you :)")

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
                        send_message(sender_id, "Please tell me how can I assist you?")
                        update_flag({
                            "section":"support",
                            "sub-section":"auto-answer"
                            })
                    elif payload_received == "chat":
                        tp.create_chat_list(sender_id)
                    elif payload_received == "hdfc_location":  # Support
                        tp.ask_for_location(sender_id)
                        update_flag({
                            "section":"support",
                            "sub-section":"location-asked"
                            })
                    elif payload_received == "complaint_description":
                        send_message(sender_id, "We're sorry for you :(, can you please describe your issue ")
                        update_flag({
                            "section":"support",
                            "sub-section":"complaint-provided"
                            })




    return "ok", 200


def update_flag(val):
    fname = "flag.p"
    fileObj = open(fname,'wb')
    print("updating flag to ->",val)
    pickle.dump(val,fileObj)
    fileObj.close()


def get_flag():
    try:
        fname = "flag.p"
        fileObj = open(fname, 'r')
        return pickle.load(fileObj)
    except:
        return None

def update_location(loc):
    fname = "location.p"
    fileObj = open(fname,'wb')
    pickle.dump(loc,fileObj)
    fileObj.close()

def get_location():
    try:
        fname = "location.p"
        fileObj = open(fname, 'r')
        return pickle.load(fileObj)
    except:
        return None

def reset_flag():
    fname = "flag.p"
    fileObj = open(fname,'wb')
    pickle.dump({},fileObj)
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

    # recipient_id = "1311151252277587"
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
    #send_message(sender_id, str(data))
    pass

def log_to_messenger(sender_id, data, context=""):
    #send_message(sender_id, context + ": " + str(data))
    pass


def log(message):  # simple wrapper for logging to stdout on heroku
    print(json.dumps(str(message), indent=4))
    sys.stdout.flush()


def save_image_from_url(image_url='', image_name='', is_qr=False):
    if not image_url:
        image_url = get_image_url()
    session = requests.session()
    response = session.get(image_url)
    filename = image_name
    if not image_name:
        filename = 'image_%s.jpeg' % md5.new(image_url).hexdigest()
    if is_qr:
        filename = os.path.join(QR_CODE_DIRECTORY, filename)
    with open(filename, 'wb') as handle:
        for block in response.iter_content(1048576):
            if not block:
                break
            handle.write(block)
        handle.close()
    mimetype = magic.from_file(filename, mime=True)
    if not mimetype.startswith('image/'):
        raise Exception('Not an image: ' + mimetype)
    return filename

def send_feedback_to_web(username="satwik", text="I love the ux"):
    URL = 'http://hdfc-support.mybluemix.net/submitFeedback'
    data = {}
    data['user'] = username
    data['feedback'] = text
    json_data = json.dumps(data)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    req_post = requests.post(URL, data=json_data, headers=headers)
    return req_post.content
    


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

def getTranslation(job_id):
    apikey="625b9864-f2be-42e9-89ce-4aab222a3860"
    url = "https://api.havenondemand.com/1/job/result/"

    url = url+job_id+"?apikey="+apikey

    r=requests.post(url)

    d = r.json()

    # Response Text
    caller_resp = d['actions'][0]['result']['document'][0]['content']

    return caller_resp


# ------------------- Run App ---------------------- #

if __name__ == '__main__':
    app.run(debug=True)