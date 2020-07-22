from apps.rbac.models import Menu,Permission,Role


#角色权限
def role_menu_permission(role_id=0):
    #菜单
    menu_item_list = Menu.objects.values('id','title','parent_id')
    permission_item_list = Permission.objects.values('id','title','menu_id','is_menu')
    role_permission_list = []
    if role_id != 0:
        role_permission_ids_list = Role.objects.get(id=role_id).permissions.all().values('id')
        for item in role_permission_ids_list:
            role_permission_list.append(item['id'])

    #菜单树
    menu_tree_list = [{"title":"后台首页","checked":1,"disabled":"false","value":5,"data":[]},{"title":"后台主页","checked":1,"disabled":"false","value":6,"data":[]}]
    for item_first in menu_item_list:
        if item_first['parent_id'] == 1 and item_first['id'] != 1:
            data_first = menu_item_list.filter(parent_id=item_first['id'])
            temp_data_first = []
            if data_first:
                for item_second in data_first:
                    data_second = permission_item_list.filter(menu_id=item_second['id'])
                    temp_data_second = []
                    if data_second:
                        for item_third in data_second:
                            temp_third = {"value": item_third['id'],
                                           "title": item_third["title"],
                                           "checked": 0,
                                           "data": []}
                            if temp_third["value"] in role_permission_list:
                                temp_third["checked"] = 1
                            temp_data_second.append(temp_third)
                    #二级
                    temp_second = {"value": item_second['id'],
                                   "title": item_second["title"],
                                   "checked": 0,
                                   "data": temp_data_second}

                    temp_data_first.append(temp_second)

                # 一级
                temp_first = {"value": item_first['id'],
                              "title": item_first["title"],
                              "checked": 0,
                              "data": temp_data_first}

            menu_tree_list.append(temp_first)

    return menu_tree_list