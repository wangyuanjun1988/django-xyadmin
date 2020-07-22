from apps.rbac.models import Menu


def init_permission(request, user_obj):
    """
    初始化用户权限, 写入session
    :param request:
    :param user_obj:
    :return:
    """

    #模块ID列表
    phead_menu_item_list = user_obj.roles.filter(permissions__status=1).values('permissions__menu__parent_id').distinct()
    if user_obj.is_superuser == 1:
        phead_menu_item_list = Menu.objects.filter(parent_id=1).values('id')

    #菜单ID和模块ID列表
    head_menu_childitem_list = user_obj.roles.filter(permissions__status=1).values('permissions__menu__id',
                                                     'permissions__menu__title',
                                                     'permissions__menu__parent_id',
                                                     'permissions__menu__data_icon',
                                                     'permissions__menu__i_class_name',
                                                     'permissions__menu__menu_code').distinct()

    parent_id_list=[]
    if user_obj.is_superuser == 1: #超级管理员
        for item in phead_menu_item_list:
            parent_id_list.append(item['id'])
    else :
        for item in phead_menu_item_list:
            parent_id_list.append(item['permissions__menu__parent_id'])


    #用户的权限模块名称
    head_menu_item_list = Menu.objects.filter(id__in=parent_id_list, id__gt=1).values('id', 'title', 'data_icon', 'i_class_name', 'menu_code')

    head_menu_url_list = []
    for item in head_menu_item_list:
        if item['title']:
            childtemp_list = []
            for child in head_menu_childitem_list:
                if child['permissions__menu__parent_id'] == item['id']:
                    childtemp = {"id": child['permissions__menu__id'],
                                 "title": child["permissions__menu__title"],
                                 "data_icon": child["permissions__menu__data_icon"],
                                 "i_class_name": child["permissions__menu__i_class_name"],
                                 "menu_code": child["permissions__menu__menu_code"]}
                    childtemp_list.append(childtemp)

            temp = {"id": item['id'],
                    "title": item["title"],
                    "data_icon": item["data_icon"],
                    "i_class_name": item["i_class_name"],
                    "menu_code": item["menu_code"],
                    "child":childtemp_list}
        head_menu_url_list.append(temp)

    permission_item_list = user_obj.roles.filter(permissions__status=1).values('permissions__url',
                                                 'permissions__title',
                                                 'permissions__menu_id',
                                                 'permissions__data_icon',
                                                 'permissions__i_class_name',
                                                 'permissions__is_menu',
                                                 'permissions__menu_code').distinct()

    permission_url_list = []
    # 用户权限url列表，--> 用于中间件验证用户权限
    permission_menu_list = []
    # 用户权限url所属菜单列表 [{"title":xxx, "url":xxx, "menu_id": xxx},{},]

    for item in permission_item_list:
        permission_url_list.append(item['permissions__url'])
        if item['permissions__menu_id']:
            temp = {"title": item['permissions__title'],
                    "url": item["permissions__url"],
                    "menu_id": item["permissions__menu_id"],
                    "data_icon": item["permissions__data_icon"],
                    "i_class_name": item["permissions__i_class_name"],
                    "is_menu": item["permissions__is_menu"],
                    "menu_code": item["permissions__menu_code"]}
            permission_menu_list.append(temp)

    menu_list = list(Menu.objects.values('id', 'title', 'parent_id'))
    # 注：session在存储时，会先对数据进行序列化，因此对于Queryset对象写入session，加list()转为可序列化对象

    from django.conf import settings  # 通过这种方式导入配置，具有可迁移性

    # 保存用户权限url列表
    request.session[settings.SESSION_PERMISSION_URL_KEY] = permission_url_list
    request.session[settings.SESSION_HEAD_MENU_KEY] = head_menu_url_list

    # 保存 权限菜单 和所有 菜单；用户登录后作菜单展示用
    request.session[settings.SESSION_MENU_KEY] = {
        settings.ALL_MENU_KEY: menu_list,
        settings.PERMISSION_MENU_KEY: permission_menu_list,
    }