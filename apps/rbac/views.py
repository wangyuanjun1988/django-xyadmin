from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import UserInfo, Role
from .forms import UserInfo_New_Form,UserInfoForm, RoleForm
from django.conf import settings
import json
from apps.rbac.service import menuserver


#菜单
def menuchild(request):
    pmenu = request.session[settings.SESSION_HEAD_MENU_KEY]
    menu = request.session[settings.SESSION_MENU_KEY][settings.PERMISSION_MENU_KEY]
    data = {}
    for pm in pmenu:
        pm_data = []
        for pmchild in pm['child']:
            m_data = []
            for m in menu:
                if m['menu_id'] == pmchild['id'] and  m['is_menu'] == 1:
                    m_data.append({'title': m['title'],
                                   'icon': m['data_icon'],
                                   'href': m['url'],
                                   'spread': False})
            pm_data.append({'title': pmchild['title'],
                                     'icon': pmchild['data_icon'],
                                     'href': '',
                                     'spread': False,
                                     'children': m_data})

        data[pm['menu_code']] = pm_data


    return HttpResponse(json.dumps(data))


#后台入口
def index(request): # 提供后台管理的入口
    return render(request, 'rbac/pbookplay.html')


#用户列表页
def users(request):
    """查询所有用户信息"""
    return render(request, 'rbac/users/userlist.html')


#用户数据接口
def users_data(request):
    key = request.GET.get('key')
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if key:
        user_list = UserInfo.objects.values('id', 'username', 'nickname', 'email', 'gender', 'status', 'add_time', 'lastlogintime',
                                            'roles__title').filter(is_superuser=0, username__contains=key).order_by('-id')
    else:
        user_list = UserInfo.objects.values('id', 'username', 'nickname', 'email', 'gender', 'status', 'add_time','lastlogintime',
                                            'roles__title').filter(is_superuser=0).order_by( '-id')
    paginator = Paginator(user_list,limit)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    response_data = {}
    response_data['code'] = '0'
    response_data['msg'] = ''
    response_data['count'] = paginator.count
    response_data['data'] = list(contacts)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#添加用户
def users_add(request):
    if request.method == "GET":
        # 传入ModelForm对象
        model_form = UserInfo_New_Form()
        role_list = Role.objects.all().values_list('id','title')
        return render(request, 'rbac/users/useradd.html', {'model_form': model_form, 'role_list': role_list})
    else:
        model_form = UserInfo_New_Form(request.POST)
        response_data = {}
        if model_form.is_valid():
            model_form.save()
            response_data['code'] = '1'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
            #return redirect(reverse(users))
        else:
            response_data['code'] = '0'
            response_data['error'] = model_form.errors
            return HttpResponse(json.dumps(response_data), content_type="application/json")
            #return render(request, 'rbac/useradd.html',{'model_form': model_form, 'title': '新增用户'})


#编辑用户
def users_edit(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        user_obj = UserInfo.objects.filter(id=id).first()
        model_form = UserInfoForm(instance=user_obj)
        role_list = Role.objects.all().values_list('id', 'title')
        return render(request, 'rbac/users/useredit.html', {'model_form': model_form, 'role_list': role_list, 'user_id':id})
    else:
        id = request.POST.get('id')
        user_obj = UserInfo.objects.filter(id=id).first()
        model_form = UserInfoForm(request.POST, instance=user_obj)
        #model_form.clean_username(id)
        response_data = {}
        if model_form.is_valid():
            model_form.save()
            response_data['code'] = '1'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data['code'] = '0'
            response_data['error'] = model_form.errors
            return HttpResponse(json.dumps(response_data), content_type="application/json")


#删除用户
def users_delete(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids')
        user_obj = UserInfo.objects.filter(id__in=ids, is_superuser=0)
        user_obj.delete()
        response_data = {}
        response_data['code'] = '1'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
        # return redirect(reverse(users))


#角色列表页
def roles(request):
    """查询所有用户信息"""
    return render(request, 'rbac/roles/rolelist.html')


#角色数据接口
def roles_data(request):
    key = request.GET.get('key')
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if key:
        role_list = Role.objects.values('id', 'title').filter(title__contains=key).order_by('-id')
    else:
        role_list = Role.objects.values('id', 'title').order_by('-id')
    paginator = Paginator(role_list, limit)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    response_data = {}
    response_data['code'] = '0'
    response_data['msg'] = ''
    response_data['count'] = paginator.count
    response_data['data'] = list(contacts)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#添加角色
def roles_add(request):
    if request.method == "GET":
        # 传入ModelForm对象
        model_form = RoleForm()
        menu_tree_list = menuserver.role_menu_permission()
        return render(request, 'rbac/roles/roleadd.html', {'model_form': model_form, 'menu_tree_list': menu_tree_list})
    else:
        model_form = RoleForm(request.POST)
        response_data = {}
        if model_form.is_valid():
            model_form.save()
            response_data['code'] = '1'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data['code'] = '0'
            response_data['error'] = model_form.errors
            return HttpResponse(json.dumps(response_data), content_type="application/json")


#编辑角色
def roles_edit(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        role_obj = Role.objects.filter(id=id).first()
        model_form = RoleForm(instance=role_obj)
        menu_tree_list = menuserver.role_menu_permission(role_id=id)
        return render(request, 'rbac/roles/roleedit.html', {'model_form': model_form, 'menu_tree_list': menu_tree_list, 'role_id':id})
    else:
        id = request.POST.get('id')
        role_obj = Role.objects.filter(id=id).first()
        model_form = RoleForm(request.POST, instance=role_obj)
        response_data = {}
        if model_form.is_valid():
            model_form.save()
            response_data['code'] = '1'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data['code'] = '0'
            response_data['error'] = model_form.errors
            return HttpResponse(json.dumps(response_data), content_type="application/json")


#删除角色
def roles_delete(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids')
        role_obj = Role.objects.filter(id__in=ids)
        role_obj.delete()
        response_data = {}
        response_data['code'] = '1'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
        # return redirect(reverse(users))

# 修改密码
def user_editpassword(request):
    if request.method == 'GET':
        return render(request, 'rbac/editpassword/user_editpassword.html')
    else:
        response_data = {}
        id = request.session["userid"]
        pwd = request.POST.get('pwd')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')
        user = UserInfo.objects.get(id=id)
        if user.password == pwd and pwd1== pwd2:
            user.password = pwd1
            user.save()
            response_data['code'] = '1'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data['code'] = '0'
            response_data['error'] = '两次密码不一致'
            return HttpResponse(json.dumps(response_data), content_type="application/json")







def menus(request):
    pass


def menus_data(request):
    pass


def menus_add(request):
    pass


def menus_edit(request):
    pass


def menus_delete(request):
    pass

