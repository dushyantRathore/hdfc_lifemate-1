import json
import os
import requests
import sys


# ------------------------ Get Started Member List---------------------- #


def quickreplies_getstarted(sender_id):
    getstarted = json.dumps({
        "recipient":{
                        "id": sender_id
                    },
                    "message":{
        "text": "Choose your Option ",
        "quick_replies": [
            {
                "content_type": "text",
                "title": "Login",
                "payload": "member_yes"
            },
            {
                "content_type": "text",
                "title": "Sign Up",
                "payload": "member_no"
            }
        ]
       }
    })

    post_request(getstarted)

def quickreplies_satisfied(sender_id):
    getstarted = json.dumps({
        "recipient":{
                        "id": sender_id
                    },
                    "message":{
        "text": "Are you satisfied?",
        "quick_replies": [
            {
                "content_type": "text",
                "title": "Yes",
                "payload": "yes"
            },
            {
                "content_type": "text",
                "title": "No",
                "payload": "no"
            }
        ]
       }
    })

    post_request(getstarted)

# ------------------------ Insurance Plans List ------------------------- #


def create_view_insurance_list(sender_id):
    insurance_list_template = json.dumps({
        "recipient": {"id": sender_id
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


# ------------------------ Best for me - Age option ----------- #


def create_apply_age_list(sender_id):
    age_list = json.dumps({
        "recipient":{
    "id":"sender_id"
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"button",
        "text":"What is your age ? ",
        "buttons":[
          {
            "type":"postback",
            "title":"< 35 years.",
            "payload":"age_<35"
          },
          {
            "type":"postback",
            "title":"35-45 years",
            "payload":"age_35-45"
          },
            {
                "type": "postback",
                "title": ">45 years",
                "payload": "age_>45"
            }
        ]
      }
    }
  }
    })

    post_request(age_list)


# ------------------------ Claim Options List ---------------- #

def create_claim_type_list(sender_id):
    claim_list = json.dumps({
    "recipient":{
                    "id": sender_id
                },
    "message":{
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "Please choose your option",
                "buttons": [
                    {
                        "type": "postback",
                        "title" : "Natural Death",
                        "payload" : "natural_death"
                    },
                    {
                        "type": "postback",
                        "title": "Critical Illness",
                        "payload": "critical_illness"
                    }
                ]
            }
        }
    }
    })

    post_request(claim_list)


# ---------------------- My Account List --------------------- #


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


# ------------------------ Pay/Remind List ---------------- #

def create_pay_remind_list(sender_id):
    pay_remind_list = json.dumps({
    "recipient":{
                    "id": sender_id
                },
    "message":{
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "Please choose your option",
                "buttons": [
                    {
                        "type": "web_url",
                        "url": "http://www.hdfclife.com/customer-service/pay-premium",
                        "title": "Pay"
                    },
                    {
                        "type": "postback",
                        "title": "Set Reminder",
                        "payload": "remind"
                    }
                ]
            }
        }
    }
    })

    post_request(pay_remind_list)


# ----------------- Alternate Support List ---------------------- #
def create_alternate_support_list(sender_id):
    alternate_support_list = json.dumps({
        "recipient": {
            "id": sender_id
        }, "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":[
           {
            "title":"What do you want to do ? ",
            "subtitle":"Select your option",
            "buttons":[
              {
                "type":"phone_number",
                "title":"Call Helpline",
                "payload":"+15105551234"
              },{
                "type":"postback",
                "title":"Nearest HDFC Centre",
                "payload":"hdfc_location"
              }
            ]
          }
        ]
      }
    }
  }
})

    post_request(alternate_support_list)

def signup_from_web_button(sender_id):
    signup_button = json.dumps({
    "recipient":{
                    "id": sender_id
                },
    "message":{
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "Thanks! Your details have been recorded.",
                "buttons": [
                    {
                        "type": "web_url",
                        "url": "http://www.hdfclife.com/customer-service/pay-premium",
                        "title": "Finish"
                    }
                ]
            }
        }
    }
    })

    post_request(signup_button)


# ---------------------- Generic Template ----------------------------------- #

def create_generic_template(sender_id, name, subtitle, image_url, phone, navigation_url):
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


# ------------------------- Yes/No Button ------------------------ #

def create_yes_no_button(sender_id):
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
                                "payload":"_yes"
                              },
                              {
                                "type":"postback",
                                "title":"No",
                                "payload":"_no"
                              }
                        ]
                    }
                }
            }
        })
    post_request(button_message)


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


def log(message):  # simple wrapper for logging to stdout on heroku
    print (str(message))
    sys.stdout.flush()

