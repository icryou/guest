# coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

# Create your views here.


def index(request):
    return render(request, "index.html")


# 登录
def login_action(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
        # if username == 'admin' and password == 'admin123':
            response = HttpResponseRedirect('/event_manage/')
            request.session['user'] = username
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


# 发布会管理
@login_required()
def event_manage(request):
    username = request.session.get('user', '')
    event_list = Event.objects.all()
    paginator = Paginator(event_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'event_manage.html', {"user": username, "events": contacts})


# 发布会名称搜索
@login_required()
def sreach_name(request):
    username = request.session.get('user', '')
    sreach_name = request.GET.get('name', "")
    event_list = Event.objects.filter(name__contains=sreach_name)
    paginator = Paginator(event_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "event_manage.html", {"user": username, "events": contacts})


# 嘉宾管理
@login_required()
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


# 嘉宾手机号搜索
@login_required()
def sreach_phone(request):
    username = request.session.get('user', '')
    sreach_phone = request.GET.get('phone', "")
    sreach_name_bytes = sreach_phone.encode(encoding="utf-8")
    guest_list = Guest.objects.filter(phone__contains=sreach_name_bytes)
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


# 签到页面
@login_required()
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index.html', {'event': event})

# 签到动作
@login_required()
def sign_index_action(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone', '')
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone error.'})
    result = Guest.objects.get(phone=phone)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': "user has sign in."})
    else:
        Guest.objects.filter(phone=phone).update(sign='1')
        return render(request, 'sign_index.html', {'event': event, 'hint': 'sign in success!', 'guest': result})


# 退出登录
@login_required()
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/')
    return response