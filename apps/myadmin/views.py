from django.shortcuts import render, redirect, HttpResponse
from apps.rbac.models import UserInfo, Menu
from apps.rbac.service.init_permission import init_permission
from django.conf import settings
import json
import django.utils.timezone as timezone
import logging

logger = logging.getLogger('log')


def index(request):
    if(request.session.get('userid')!=None):
        return render(request, 'xyadmin/index.html')
    return redirect('/xyadmin/login')


def main(request):
    return render(request, 'xyadmin/page/main.html')


def login(request):
    if request.method == 'GET':
        return render(request,'xyadmin/page/login/login.html')
    else :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = UserInfo.objects.filter(username=username, password=password).first()
        if not user_obj:
            #return render(request, "wyjadmin/page/login/login.html", {'error': '用户名或密码错误！'})
            response_data = {}
            response_data['status'] = 'false'
            response_data['info'] = '用户名或密码错误!'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            init_permission(request, user_obj)  # 调用init_permission，初始化权限
            user_obj.lastlogintime = timezone.now()
            user_obj.save()
            #return redirect('index')
            response_data = {}
            response_data['status'] = 'true'
            response_data['url'] = 'index'
            request.session["username"] = username
            request.session["userid"] = user_obj.id
            return HttpResponse(json.dumps(response_data), content_type="application/json")


def logout(request):
    del request.session["username"]
    del request.session["userid"]
    del request.session[settings.SESSION_PERMISSION_URL_KEY]
    del request.session[settings.SESSION_HEAD_MENU_KEY]
    del request.session[settings.SESSION_MENU_KEY]
    return redirect('login')

