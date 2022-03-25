from django import forms
import json
import requests

class KaKaoTalkForm(forms.Form):
    text = forms.CharField(label='전송할 Talk', max_length=300)
    web_url = forms.CharField(label='Web URL', max_length=300, initial='http://172.30.1.22:8000/mjpeg')
    mobile_web_url = forms.CharField(label='Mobile Url', max_length=300, initial='http://172.30.1.22:8000/mjpeg')

    def send_talk(self): # 실제 톡을 보내는 메소드
        talk_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        with open("access_token.txt", "r") as f: # access_token을 읽어서 저장
            token = f.read()
        header = {"Authorization": f"Bearer {token}"} # 위에서 얻은 값을 header에 저장

        # 문자열 하나,링크 하나로 구성되 카톡 메시지를 사전으로 구성
        text_template = {
            'object_type': 'text', # 템플릿 유형
            'text': self.cleaned_data['text'],
            'link': {
                'web_url': self.cleaned_data['web_url'],
                'mobile_web_url': self.cleaned_data['mobile_web_url']
            }
        }

        print(text_template)
        payload = {'template_object': json.dumps(text_template)} # 메시지(json 문자열로 표현)
        res = requests.post(talk_url, data=payload, headers=header) # post로 전송
        return res, self.cleaned_data['text']