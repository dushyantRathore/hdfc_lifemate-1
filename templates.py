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


def ask_for_location(sender_id):
    quick_reply_template = json.dumps({
                              "recipient":{
                                "id":sender_id
                              },
                              "message":{
                                "text":"Please share your location:",
                                "quick_replies":[
                                  {
                                    "content_type":"location",
                                  }
                                ]
                              }
                            })
    post_request(quick_reply_template)


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


# ----------------------- View Insurance Life -> Benefits ------------------ #


def view_insurance_life_benefits(sender_id):
    benefits_list = json.dumps({
        "recipient": {
            "id": sender_id
        }, "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "list",
                    "elements": [
                        {
                            "title": "Click2Protect Plan",
                            "image_url": "http://www.mydailylifetips.com/wp-content/uploads/2014/08/hdfc-click-2-protect-plus-online-term-plan-review.png",
                            "subtitle": "Benefits offered",
                        },
                        {
                            "title": "Coverage",
                            "subtitle": "Comprehensive coverage at affordable cost"
                                        "\nProvide financial protection for you and your family"
                        },
                        {
                            "title": "Customize your plan ",
                            "subtitle": "Choice of cover options"
                                        "\nLife Option"
                                        "\nExtra Life Option"
                                        "\n Income Option"
                        },
                        {
                            "title": "Loads of other Benefits",
                            "subtitle": "Death Benefit"
                                        "\nMaturity Benefit and Life Stage Protection",
                        }
                    ]
                }
            }
        }
    })

    post_request(benefits_list)


# ------------------------ View Insurance Life - Things to keep in mind ----------- #

def important(sender_id):
    important_list = json.dumps({
        "recipient": {
            "id": sender_id
        }, "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "list",
                    "elements": [
                        {
                            "title": "Click2Protect Plan",
                            "image_url": "http://blogs.studyinsweden.se/wp-content/uploads/2015/09/Screen-shot-2012-09-05-at-2.23.34-PM.png",
                            "subtitle": "Things to keep in mind",
                        },
                        {
                            "title": "Premiums",
                            "subtitle": "Minimum Annualized Premium: 3000"
                                        "\n-> Plan has a grace period of 30 days for yearly, half yearly and quarterly frequencies from the premium due date."
                                        "\n-> In case you do not pay premiums before the end of grace period, the policy will lapse. "
                                        "\n-> All risk covers will cease and nobenefits will be payable in case of lapsed policies."
                        },
                        {
                            "title": "Who will get the benefit?",
                            "subtitle": "The benefit on death will be paid to your nominee. As per Section 39 of the Insurance Act, 1938, "
                                        "\nyou can nominate aperson to receive the benefit under this policy."
                        },
                        {
                            "title": "What is not covered?",
                            "subtitle": "-> In case of death due to suicide, within 12 months from the date of inception of the policy, "
                                        "\nthe nominee of thepolicy holder shall be entitled to 80% of the premiums paid."
                                        "\n-> In case of death due to suicide within 12 months from the date of revival of the policy, "
                                        "\nthe nominee of the policyholdershall be entitled to 80% of the premiums paid post revival. ",
                        }
                    ]
                }
            }
        }
    })

    post_request(important_list)


# ------------------------ Best for me - Age option ----------- #


def create_apply_age_list(sender_id): # Apply -> Age List
    age_list = json.dumps({
        "recipient":{
    "id": sender_id
  },
  "message":{
    "text":"What is your Age ? ",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"less than 35",
        "payload":"age_<35"
      },
      {
        "content_type":"text",
        "title":"35-45",
        "payload":"age_35-35"
      },
        {
            "content_type": "text",
            "title": "greater than 45",
            "payload": "age_>45"
        }
    ]
  }

})

    post_request(age_list)


# ------------------- Best for me - Gender Option ------------- #

def create_apply_gender_list(sender_id): # Apply -> Gender List
    gender_list = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": "What is your gender ? ",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Male",
                    "payload": "gender_male"
                },
                {
                    "content_type": "text",
                    "title": "Female",
                    "payload": "gender_female"
                }
            ]
        }
    })

    post_request(gender_list)

def send_qr_code_template(sender_id, image_url):
    temp = json.dumps(
        {
  "recipient":{
    "id":sender_id
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":[
          {
            "title":"Breaking News: Record Thunderstorms",
            "subtitle":"The local area is due for record thunderstorms over the weekend.",
            "image_url":image_url,
            "buttons":[
              {
                "type":"element_share"
              }              
            ]
          }
        ]
      }
      }}}
      )
    post_request(temp)



# --------------------- Best for me - Marital Status --------------- #


def create_apply_marital_status_list(sender_id): # Apply -> Gender List
    status_list = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": "What is your marital status ? ",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Married",
                    "payload": "married"
                },
                {
                    "content_type": "text",
                    "title": "Unmarried",
                    "payload": "unmarried"
                },
                {
                    "content_type": "text",
                    "title": "Divorced",
                    "payload": "divorced"
                }
            ]
        }
    })

    post_request(status_list)


# --------------- Best for me - Occupation ----------- #
def create_occupation_list(sender_id):
    occupation_list = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": "What is your occupation ? ",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Self Employed",
                    "payload": "self employed"
                },
                {
                    "content_type": "text",
                    "title": "Government Job",
                    "payload": "government job"
                },
                {
                    "content_type": "text",
                    "title": "Private Job",
                    "payload": "private job"
                }
            ]
        }
    })

    post_request(occupation_list)


# ----------------------- Best for Me - Income List ----------- #


def create_income_list(sender_id):
    income_list = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": "What is your annual income ? ",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Below 5 Lakhs",
                    "payload": "below"
                },
                {
                    "content_type": "text",
                    "title": "5 to 10 Lakhs",
                    "payload": "between"
                },
                {
                    "content_type": "text",
                    "title": "Above 10 Lakhs",
                    "payload": "above"
                }
            ]
        }
    })

    post_request(income_list)

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
                "type":"postback",
                "title":"Tele/Video Chat",
                "payload":"chat"
              },
              {
                "type":"postback",
                "title":"Nearest HDFC Centre",
                "payload":"hdfc_location"
              },
              {
                "type":"postback",
                "title":"Quick complaint",
                "payload":"complaint_description"
              }
            ]
          }
        ]
      }
    }
  }
})

    post_request(alternate_support_list)

# ------------------------ Chat options list ----------------- #


def create_chat_list(sender_id):
    chat_list = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Choose your option",
                    "buttons": [
                        {
                            "type": "phone_number",
                            "title": "IVR Helpline",
                            "payload": "+15105551234"
                        },
                        {
                            "type": "web_url",
                            "url": "https://www.skype.com/en/",
                            "title": "Video Call",
                            "webview_height_ratio": "compact"
                        }
                    ]
                }
            }
        }
    })

    post_request(chat_list)


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

def create_yes_no_button(sender_id, question, context):
    button_message = json.dumps({
        "recipient":{
                        "id": sender_id
                    },
        "message":{
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": question,
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

