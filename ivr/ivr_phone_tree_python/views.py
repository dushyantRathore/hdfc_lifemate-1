from flask import render_template, redirect, url_for, request, session, flash
from ivr_phone_tree_python import app
import twilio.twiml
from ivr_phone_tree_python.view_helpers import twiml
import requests
import json


@app.route('/')
@app.route('/ivr')
def home():
    return render_template('index.html')


@app.route('/ivr/welcome', methods=['POST'])
def welcome():

    # Experiment

    callerNum = request.form['From']
    print(callerNum)

    # Experiment close

    response = twilio.twiml.Response()
    with response.gather(numDigits=1, action=url_for('menu'), method="POST") as g:
        g.say("Welcome to HDFC Life mate. Your twenty-four-seven Helpline. "+
              "To check status of your complaint, press 1. . "+
              "To send us a voice feedback or complaint, press 2. . "
              "To talk to our executive, press 3. . "+
              "To know more about our plans. press 4.  . "+
              "To get a download link for our app, press 5. . "+
              "   ",
              voice='alice', language="en-US", loop=3)
    return twiml(response)


@app.route('/ivr/menu', methods=['POST'])
def menu():
    selected_option = request.form['Digits']
    option_actions = {'1': _check_complaint_status,
                      '2': _record_message,
                      '3': _talk_to_executive,
                      '4': _sms_plans,
                      '5': _download_app}

    if option_actions.has_key(selected_option):
        response = twilio.twiml.Response()
        option_actions[selected_option](response)
        return twiml(response)

    return _redirect_welcome()


@app.route('/ivr/complaint', methods=['POST'])
def complaint():
    
    response = twilio.twiml.Response()
    _lookup_complaint(response, request.form['Digits'])
    return twiml(response)

    return _redirect_welcome()

@app.route('/ivr/sms_to', methods=['POST'])
def sms_to():
  selected_option = request.form['Digits']
  option_texts = {'1': "Click2Protect - http://bit.ly/2jOrBnz",
                  '2': "Click2Invest - http://bit.ly/TrjSgf",
                  '3': "Easy Health Plan - http://bit.ly/2j1YpvW"}

  if option_texts.has_key(selected_option):
        response = twilio.twiml.Response()
        _send_sms(response, option_texts[selected_option])
        return twiml(response)

  return _redirect_welcome()


@app.route('/ivr/send_message', methods=['POST'])
def send_message():
    recording_url = request.values.get("RecordingUrl", None)
    callerNum = request.form['From']

    print(recording_url)

    job_id = post_to_haven(recording_url)

    print("Caller Number : "+callerNum)
    print("Job ID : "+job_id)

    response = twilio.twiml.Response()
    response.say("Thank you. Your response has been duly noted. "+
                  "You will now be redirected to the main menu", voice="alice", language="en-US")

    #text_to_send = getData(job_id)

    #ans = update_dashboard(job_id)

    #ans = sendToBluemix(text_to_send, callerNum)

    response.redirect(url_for('welcome'))
    return twiml(response)




# private methods

def _check_complaint_status(response):
    with response.gather(numDigits=6, action=url_for('complaint'), method="POST") as g:
        g.say("Please enter your 6 digit complaint number.  .  ."
              ,voice="alice", language="en-US", loop=2)

    return response


def _talk_to_executive(response):
    response.dial("+918447370864")
    response.say("We hope you are satisfied with your care.  "+
                  "You will now be redirected to the main menu"
                  ,voice="alice", language="en-US")
    response.redirect(url_for('welcome'))
    return response


def _download_app(response):
    response.sms("Androd App Link", to="+919990402599", sender="+19898164061")
    response.say("You have been sent an SMS with the link to download the app. "+
                  "You will now be redirected to the main menu", voice="alice", language="en-US")
    response.redirect(url_for('welcome'))
    return response

def _sms_plans(response):
    with response.gather(numDigits=1, action=url_for('sms_to'), method="POST") as g:
      g.say("HDFC Life offers you four plans - "+
                  "Press One to know about Click Two Protect Plus plan.   "+
                  "Press Two to know about Click Two Invest plan.   "+
                  "Press Three to know about Easy Health Plan.   "+
                  "Press Star to return to the main menu.   "
                  ,voice="alice", language="en-US", loop=3)

    return response

def _send_sms(response, sms_text):
    response.sms(sms_text, to="+919990402599", sender="+19898164061")
    response.say("You have been sent an SMS with the link to download the plan brochure. "+
                  "You will now be redirected to the main menu", voice="alice", language="en-US")
    response.redirect(url_for('welcome'))
    return response

def _lookup_complaint(response, number):
    response.say("Your complaint number - " + number+
                  "is still under process. Please be patient while our team "+
                  "addresses your issue.   "+
                  "You will now be redirected to the main menu"
                  ,voice="alice", language="en-US")
    response.redirect(url_for('welcome'))
    return response


def _redirect_welcome():
    response = twilio.twiml.Response()
    response.say("Returning to the main menu", voice="alice", language="en-US")
    response.redirect(url_for('welcome'))
    return twiml(response)


def _record_message(response):
    response.say("Record your message after the beep. Press any key to end your recording.", voice="alice", language="en-US")
    response.record(playBeep=True, action=url_for('send_message'))
    return response


def post_to_haven(audio_url):
    url = "https://api.havenondemand.com/1/api/async/recognizespeech/v1?url="
    #video_url = "https://www.havenondemand.com/sample-content/videos/hpnext.mp4"
    url=url+audio_url+"&language=en-GB"
    apikey = "625b9864-f2be-42e9-89ce-4aab222a3860"
    data={}
    data["apikey"]=apikey
    r=requests.post(url,data=data)
    return r.json()['jobID']

def getData(job_id):
    url = "https://api.havenondemand.com/1/job/result/"
    apikey = "625b9864-f2be-42e9-89ce-4aab222a3860"
    #job_id = "w-eu_0b1f7864-d390-4601-b4a5-8b69092299bc"
    url = url+job_id+"?apikey="+apikey

    r=requests.post(url)

    d = r.json()

    # Response Text
    caller_resp = d['actions'][0]['result']['document'][0]['content']
    return caller_resp


def sendToBluemix(text, number):

  URL = 'http://hdfc-support.mybluemix.net/submitFeedback'

  data = {}
  data['user'] = number
  data['feedback'] = text
  json_data = json.dumps(data)
  headers = {"Content-Type": "application/json", "Accept": "application/json"}
  req_post = requests.post(URL, data=json_data, headers=headers)

  return 0

def update_dashboard(jobID):
  res = requests.get('https://sheltered-falls-53215.herokuapp.com//update-dashboard/'+jobID)
  return res.content