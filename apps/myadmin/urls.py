# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from django.urls import path, include
from apps.myadmin import views as my_views

urlpatterns = [
    path('index', my_views.index,name='index'),
    path('main', my_views.main,name='main'),
    path('login', my_views.login,name='login'),
    path('logout', my_views.logout,name='logout'),
    path('rbac', include('apps.rbac.urls')),
]