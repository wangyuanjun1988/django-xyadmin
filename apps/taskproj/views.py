from django.shortcuts import render
from django.http import JsonResponse
from apps.taskproj import tasks

# Create your views here.


def index(request, *args, **kwargs):
    res = tasks.add.delay(1, 3)
    # 任务逻辑
    return JsonResponse({'status': 'successful', 'task_id': res.task_id})
