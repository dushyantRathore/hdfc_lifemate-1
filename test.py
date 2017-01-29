import json
import requests
def send_feedback_to_web(username="satwik", text="I love the ux"):
    URL = 'http://hdfc-support.mybluemix.net/submitFeedback'
    data = {}
    data['user'] = username
    data['feedback'] = text
    json_data = json.dumps(data)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    req_post = requests.post(URL, data=json_data, headers=headers)
    return req_post.content

def getTranslation(job_id):
    apikey="625b9864-f2be-42e9-89ce-4aab222a3860"
    url = "https://api.havenondemand.com/1/job/result/"

    url = url+job_id+"?apikey="+apikey

    r=requests.post(url)

    d = r.json()

    # Response Text
    caller_resp = d['actions'][0]['result']['document'][0]['content']

    return caller_resp

def post_to_dashboard(jobID):
    print(jobID)
    time.sleep(15)
    translation = getTranslation(jobID)
    if translation:
        return send_feedback_to_web(text=str(translation))
    else:
        return "couldn't decode"

def update_dashboard(jobID)
	res = requests.get('https://sheltered-falls-53215.herokuapp.com//update-dashboard/'+jobID)
	return res.content