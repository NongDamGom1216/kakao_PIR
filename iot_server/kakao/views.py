from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from kakao.forms import KaKaoTalkForm
import json
import requests
from django.contrib import messages

client_id = "YOUR REST API KEY"

# 토큰이 만료되면 http://172.30.1.22:8000/kakao/login/ 에서 로그인해줘야함

class KakaoLoginView(TemplateView):
    template_name = "kakao_login.html"

    # context 사전 구성
    # **kwargs : 가변 키워드 인수(사전) -> (k=v, k=v, k=v) 식으로 호출
    # 튜플이나 리스트일 때는 가변 인수 * 한 개만 쓴다 -> *args
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        # 전달 받은 모든 키워드 인수를 사전 형태인 그대로 전달한다
        context["client_id"] = client_id # context 변수에 rest key 대입
        return context

class KakaoAuthView(TemplateView):
    template_name = "kakao_token.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = self.request.GET['code']
        token = self.getAccessToken(code)
        context["client_id"] = client_id
        context["token"] = token
        self.save_access_token(token["access_token"]) # 받은 토큰을 파일에 저장

        return context
    
    # 세션 코드값 code 를 이용해서 ACCESS TOKEN과 REFRESH TOKEN을 발급 받음
    def getAccessToken(self, code):
        url = "https://kauth.kakao.com/oauth/token"
        payload = "grant_type=authorization_code"
        payload += "&client_id=" + client_id
        # 응답받을 redirect_url
        payload += "&redirect_url=http://172.30.1.22:8000/kakao/oauth&code=" + code
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        response = requests.post(url, data=payload, headers=headers)
        return response.json()

    def save_access_token(self, access_token):
        with open("access_token.txt", "w") as f: #상대 경로에 저장
            f.write(access_token)

class kakaoTalkView(FormView):
    form_class = KaKaoTalkForm
    template_name = "kakao_form.html"
    success_url = "/kakao/talk"

    def form_valid(self, form):
        res, text = form.send_talk()

        if res.json().get('result_code') == 0:
            messages.add_message(self.request, messages.SUCCESS, "메시지 전송 성공 : " + text)
        else:
            messages.add_message(self.request, messages.ERROR, "메시지 전송 실패 : " + str(res.json()))
        return super().form_valid(form)