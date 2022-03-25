# PIR 센서에서 동작이 감지된 경우
# KAKAO 톡 메시지 전송

import requests
import json
from gpiozero import MotionSensor, LED
from signal import pause

key_path = '/home/pi/workspace/iot_server/access_token.txt' # 절대 경로(매일 바뀌므로 로그인 한 번씩 해줘야함)

def send_talk(text, mobile_web_url, web_url=None):
    if not web_url:
        web_url = mobile_web_url
    
    with open(key_path, "r") as f:
        token = f.read()
    
    talk_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    header = {"Authorization": f"Bearer {token}"}

    # 문자열 하나,링크 하나로 구성되 카톡 메시지를 사전으로 구성
    text_template = {
        'object_type': 'text', # 템플릿 유형
        'text': text,
        'link': {
            'web_url': web_url,
            'mobile_web_url': mobile_web_url
        }
    }

    payload = {'template_object': json.dumps(text_template)} # 메시지(json 문자열로 표현)
    res = requests.post(talk_url, data=payload, headers=header) # post로 전송
    return res.json()

pir = MotionSensor(18)
led = LED(20)

def motion_detect():
    led.on()
    res = send_talk('침입 발생', 'http://172.30.1.22:8000/mjpeg?mode=stream')
    print('침입 발생')
    if res.get('result_code') != 0:
        print('전송 실패: ', res['msg'], res['code'])
    
pir.when_motion = motion_detect
pir.when_no_motion = led.off

pause()

