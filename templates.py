import json


# -------------------- View Insurance Plans Template ---------------------- #

def create_insurance_list_template(sender_id):
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

# ---------------------- Generic Template ----------------------------------- #

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