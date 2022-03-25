from django.urls import path
from kakao.views import *

urlpatterns = [
    path('login', KakaoLoginView.as_view(), name="login"),
    path('oauth', KakaoAuthView.as_view(), name="oauth"),
    path('talk', kakaoTalkView.as_view(), name="talk"),
]