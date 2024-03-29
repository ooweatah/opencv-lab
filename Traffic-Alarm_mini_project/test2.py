import json
import requests

url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

# 사용자 토큰
headers = {
    "Authorization": "Bearer " + "kYZP2Fro1J9b8IVn9oqYV8tbH73_wRM24eccyVbDCj10mAAAAYfIjkKB"
}


data = {
    "template_object" : json.dumps({ "object_type" : "text",
                                     "text" : "야간모드가 활성화 되었습니다.",
                                     "link" : {
                                                 "web_url" : "www.naver.com"
                                              }
    })
}

response = requests.post(url, headers=headers, data=data)
#print(response.status_code)
if response.json().get('result_code') == 0:
    print('메시지를 성공적으로 보냈습니다.')
else:
    print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))