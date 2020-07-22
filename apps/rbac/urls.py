from django.urls import path,re_path
from . import views

urlpatterns = [
    path('/menuchild', views.menuchild),

    path('/user_editpassword', views.user_editpassword),
    path('/users_data', views.users_data),
    path('/users_add', views.users_add),
    path('/users_edit', views.users_edit),
    path('/users_delete', views.users_delete),
    path('/users', views.users),

    path('/roles_data', views.roles_data),
    path('/roles_add', views.roles_add),
    path('/roles_edit', views.roles_edit),
    path('/roles_delete', views.roles_delete),
    path('/roles', views.roles),

    path('/menus_data', views.menus_data),
    path('/menus_add', views.menus_add),
    path('/menus_edit', views.menus_edit),
    path('/menus_delete', views.menus_delete),
    path('/menus', views.roles),

    path('/', views.index),
]