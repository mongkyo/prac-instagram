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
    user = authenticate(request, facebook_request_token=request.GET.get('code'))
    if user:
        login(request, user)
        return redirect('posts:post-list')
    messages.error(request, '페이스북 로그인에 실패하였습니다')
    return redirect('members:login')
