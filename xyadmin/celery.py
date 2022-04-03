# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xyadmin.settings') #设置django环境

app = Celery('taskproj')

app.config_from_object('django.conf:settings', namespace='CELERY') #使用CELERY_ 作为前缀，在settings中写配置

