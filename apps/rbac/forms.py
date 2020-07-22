# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from django.forms import ModelForm, fields, widgets,ValidationError
from .models import UserInfo, Role, Permission, Menu


class UserInfoForm(ModelForm):
    username = fields.CharField(min_length=5, max_length=32, required=True, error_messages={
        'required': "用户名不能为空!",
        'min_length':"至少5位字符",
        'max_length': "至多32位字符"
    })
    nickname = fields.CharField(min_length=3, max_length=32, required=True, error_messages={
        'required': "昵称不能为空!",
        'min_length':"至少3位字符",
        'max_length': "至多32位字符"
    })
    password = fields.CharField(min_length=6, max_length=32, required=True, error_messages={
        'required': "密码不能为空!",
        'min_length': "至少3位字符",
        'max_length': "至多32位字符"
    })
    email = fields.EmailField(required=False)
    class Meta:
        model = UserInfo
        fields = ['username','nickname','password','email','gender','status','roles']


class UserInfo_New_Form(UserInfoForm):

    def clean_username(self):
        un = self.cleaned_data['username']
        user = UserInfo.objects.filter(username=un)
        if user:
            raise ValidationError('用户名已存在!')
        return self.cleaned_data['username']


class RoleForm(ModelForm):
    title = fields.CharField(min_length=3, max_length=32, required=True, error_messages={
        'required': "角色名称不能为空!",
        'min_length': "至少3位字符",
        'max_length': "至多32位字符"
    })

    class Meta:
        model = Role
        fields = ['title','permissions']
