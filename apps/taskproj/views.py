from django.shortcuts import render
from django.http import JsonResponse
from apps.taskproj import tasks
from django_celery_beat.models import PeriodicTask #倒入插件model
from rest_framework import serializers
from rest_framework import pagination
from rest_framework.viewsets import ModelViewSet
# Create your views here.


def index(request, *args, **kwargs):
    res = tasks.add.delay(1, 3)
    # 任务逻辑
    return JsonResponse({'status': 'successful', 'task_id': res.task_id})


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = '__all__'


class Mypagination(pagination.PageNumberPagination):
    """自定义分页"""
    page_size = 2
    page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 4


class TaskView(ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = Userserializer
    permission_classes = []
    pagination_class = Mypagination