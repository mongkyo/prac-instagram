import json

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import LoginForm, SignupForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    context={}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            next_path = request.GET.get('next')
            if next_path:
                return redirect(next_path)
            return redirect('posts:post-list')
    else:
        form = LoginForm()
    context['form'] = form
    return render(request, 'members/login.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('posts:post-list')


def signup_view(request):
    context = {}
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('posts:post-list')
    else:
        form = SignupForm()

    context['form'] = form
    return render(request, 'members/signup.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # is_valid()를 통과하고 인스턴스 수정이 완료되면
            # messages모듈을 사용해서 템플릿에 수정완료 메시지 표시
            messages.success(request, '프로필 수정이 완료되었습니다.')
    form = UserProfileForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'members/profile.html', context)


def facebook_login(request):
    api_get_access_token = 'https://graph.facebook.com/v3.2/oauth/access_token'
    code = request.GET.get('code')
    params = {
        'client_id': 249955975697367,
        'redirect_uri': 'http://localhost:8000/members/facebook-login/',
        'client_secret': 'd2a0a4a8d439da52d2b88b65a43f6198',
        'code': code,
    }
    response = requests.get(api_get_access_token, params)
    # 인수로 전달한 문자열이 'JSON'형식일 것으로 생각
    # json.loads는 전달한 문자열이 JSON형식 일 경우, 해당 문자열을 parsing해서 파이썬 object를 리턴함
    # response_object = json.loads(response.text)

    data = response.json()
    access_token = data['access_token']

    # access_token을 사용해서 사용자 정보를 가져오기
    pass
