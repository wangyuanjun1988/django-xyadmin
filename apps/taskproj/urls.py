from django.urls import path, re_path
from . import views

urlpatterns = [
    path('/index', views.index),
    path('/tasks', views.TaskView.as_view({'get':'list'}))
]