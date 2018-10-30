import imghdr
import io
import json
from pprint import pprint

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import LoginForm, SignupForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout, get_user_model

User = get_user_model()


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
    api_base = 'https://graph.facebook.com/v3.2'
    api_get_access_token = f'{api_base}/oauth/access_token'
    api_me = f'{api_base}/me'
    code = request.GET.get('code')
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': 'http://localhost:8000/members/facebook-login/',
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'code': code,
    }
    response = requests.get(api_get_access_token, params)
    # 인수로 전달한 문자열이 'JSON'형식일 것으로 생각
    # json.loads는 전달한 문자열이 JSON형식 일 경우, 해당 문자열을 parsing해서 파이썬 object를 리턴함
    # response_object = json.loads(response.text)

    data = response.json()
    access_token = data['access_token']

    # access_token을 사용해서 사용자 정보를 가져오기
    params = {
        'access_token': access_token,
        'fields': ','.join([
            'id',
            'first_name',
            'last_name',
            'picture.type(large)',
        ]),
    }
    response = requests.get(api_me, params)
    data = response.json()

    facebook_id = data['id']
    first_name = data['first_name']
    last_name = data['last_name']
    url_img_profile = data['picture']['data']['url']
    # HTTP GET요청의 응답을 받아옴
    img_response = requests.get(url_img_profile)
    img_data = img_response.content
    # 응답의 binary data를 사용해서 In-memory binary stream(file)객체를 생성
    ext = imghdr.what('', h=img_data)

    f = SimpleUploadedFile(f'{facebook_id}.{ext}', img_response.content)
    try:
        user = User.objects.get(username=facebook_id)
        user.last_name = last_name
        user.first_name = first_name
        # user.img_profile = f
        user.save()

    except User.DoesNotExist:
        user = User.objects.create_user(
            username=facebook_id,
            first_name=first_name,
            last_name=last_name,
            img_profile=f,
        )

    login(request, user)
    return redirect('posts:post-list')
