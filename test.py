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
print(send_feedback_to_web())