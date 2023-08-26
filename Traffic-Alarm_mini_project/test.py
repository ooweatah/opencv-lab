import json
import requests

url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

headers = {
    "Content-Type:": "application/x-www.form-urlencoded",
    "Authorization": "Bearer " + \
    "kYZP2Fro1J9b8IVn9oqYV8tbH73_wRM24eccyVbDCj10mAAAAYfIjkKB"
}

data = {
    "template_object" :json.dumps({
    "object_type" : "text",
    "text" : "야간 모드가 활성화 되었습니다."
    })
}

response = requests.post(url, headers=headers, data=data)
print(response.status_code)
if response.json().get('result_code') ==0:
    print('Message send successed')

else:
    print('Message send failed. : ' +str(response.json()))