import cv2
import numpy as np
import RPi.GPIO as rg
import time
import json
import requests

url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

# 사용자 토큰
headers = {
    "Authorization": "Bearer " + "kYZP2Fro1J9b8IVn9oqYV8tbH73_wRM24eccyVbDCj10mAAAAYfIjkKB"
}
data1 = {
    "template_object" : json.dumps({ "object_type" : "text",
                                     "text" : "야간모드가 활성화 되었습니다.",
                                     "link" : {
                                                 "web_url" : "www.naver.com"
                                              }
    })
}
data2 = {
    "template_object" : json.dumps({ "object_type" : "text",
                                     "text" : "야간모드가 종료 되었습니다.",
                                     "link" : {
                                                 "web_url" : "www.naver.com"
                                              }
    })
}
data3 = {
    "template_object" : json.dumps({ "object_type" : "text",
                                     "text" : "프로그램이 종료되었습니다.",
                                     "link" : {
                                                 "web_url" : "www.naver.com"
                                              }
    })
}

rg.setmode(rg.BCM)
led_red = 17
led_yellow = 27
led_green = 22

rg.setup(led_red,rg.OUT)
rg.setup(led_yellow,rg.OUT)
rg.setup(led_green,rg.OUT)

def on_LED(led_pin):
    rg.output(led_pin,rg.HIGH)

def off_LED(led_pin):
    rg.output(led_pin,rg.LOW)

cap = cv2.VideoCapture(0)

while True:
    
    ret, frame = cap.read()

   
    if not ret:
        break

    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    
    lower_red1 = np.array([0, 80, 100])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([170, 80,  100])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    
    red_mask = mask1 + mask2 

    
    lower_yellow = np.array([15, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([80, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

   
    red_circles = cv2.HoughCircles(red_mask, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    yellow_circles = cv2.HoughCircles(yellow_mask, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    green_circles = cv2.HoughCircles(green_mask, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

   
    if red_circles is not None:
        print("Red light.")
        on_LED(led_red)
        off_LED(led_yellow)
        off_LED(led_green)
        red_circles = np.round(red_circles[0, :]).astype("int")
        for (x, y, r) in red_circles:
            cv2.circle(frame, (x, y), r, (0, 0, 255), 4)

    elif yellow_circles is not None:
        print("Yellow light.")
        on_LED(led_yellow)
        off_LED(led_red)
        off_LED(led_green)
        yellow_circles = np.round(yellow_circles[0, :]).astype("int")
        for(x, y, r) in yellow_circles:
            cv2.circle(frame, (x, y), r, (0, 0, 255), 4)

    elif yellow_circles is not None and green_circles is not None:
        print("Yellow and Green light.")
        on_LED(led_green)
        on_LED(led_yellow)
        off_LED(led_red)
        yellow_circles = np.round(yellow_circles[0, :]).astype("int")
        green_circles = np.round(green_circles[0, :]).astype("int")
        for (x, y, r) in yellow_circles:
            cv2.circle(frame, (x, y), r, (0, 255, 255), 4)
        for (x, y, r) in green_circles:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)

    
    elif green_circles is not None:
        print("Green light.")
        yellow_circles = np.round(green_circles[0, :]).astype("int")
        on_LED(led_green)
        off_LED(led_red)
        off_LED(led_yellow)
        for(x, y, r) in yellow_circles:
            cv2.circle(frame, (x, y), r, (0, 0, 255), 4)
    elif red_circles is not None and green_circles is not None:
        print("Red and Green light.")
        on_LED(led_green)
        on_LED(led_yellow)
        off_LED(led_red)
        red_circles = np.round(red_circles[0, :]).astype("int")
        green_circles = np.round(green_circles[0, :]).astype("int")
        for (x, y, r) in yellow_circles:
            cv2.circle(frame, (x, y), r, (0, 255, 255), 4)
        for (x, y, r) in green_circles:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)

    elif cv2.waitKey(1) & 0xFF == ord('y'):
        response = requests.post(url, headers=headers, data=data1)
        if response.json().get('result_code') == 0:
            print('메시지를 성공적으로 보냈습니다.')
        else:
            print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))
        while True:
            on_LED(led_yellow)
            time.sleep(1)
            off_LED(led_yellow)
            time.sleep(1)
            if cv2.waitKey(1) & 0xFF == ord('x'):
                response = requests.post(url, headers=headers, data=data2)
                if response.json().get('result_code') == 0:
                    print('메시지를 성공적으로 보냈습니다.')
                else:
                    print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))
                off_LED(led_yellow)
                
                break;


    else :
        
        off_LED(led_green)
        off_LED(led_red)
        off_LED(led_yellow)

    cv2.imshow("frame", frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        response = requests.post(url, headers=headers, data=data3)
        if response.json().get('result_code') == 0:
            print('메시지를 성공적으로 보냈습니다.')
        else:
            print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))
        break


cap.release()
cv2.destroyAllWindows()
rg.cleanup()




