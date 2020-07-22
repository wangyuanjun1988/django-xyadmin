from django.db import models
import django.utils.timezone as timezone


# Create your models here.
class Menu(models.Model):
    """
    菜单
    """
    title = models.CharField(max_length=32, unique=True)
    menu_code = models.CharField(max_length=100, default='')
    i_class_name = models.CharField(max_length=100, default='')
    data_icon = models.CharField(max_length=100, default='')
    parent = models.ForeignKey("Menu", on_delete=models.CASCADE, null=True, blank=True)
    # 定义菜单间的自引用关系
    # 权限url 在 菜单下；菜单可以有父级菜单；还要支持用户创建菜单，因此需要定义parent字段（parent_id）
    # blank=True 意味着在后台管理中填写可以为空，根菜单没有父级菜单

    def __str__(self):
        # 显示层级菜单
        title_list = [self.title]
        p = self.parent
        while p:
            title_list.insert(0, p.title)
            p = p.parent
        return '-'.join(title_list)


class Permission(models.Model):
    """
    权限
    """
    title = models.CharField(max_length=32, default='')
    url = models.CharField(max_length=128, default='')
    is_menu = models.IntegerField(default=1)
    menu_code = models.CharField(max_length=100, default='')
    i_class_name = models.CharField(max_length=100, default='')
    data_icon = models.CharField(max_length=100, default='')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField(default=1, verbose_name='状态', help_text='状态')

    def __str__(self):
        # 显示带菜单前缀的权限
        return '{menu}---{permission}'.format(menu=self.menu, permission=self.title)


class Role(models.Model):
    """
    角色：绑定权限
    """
    title = models.CharField(max_length=32, unique=True)

    permissions = models.ManyToManyField(Permission)
    # 定义角色和权限的多对多关系

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    用户：划分角色
    """
    username = models.CharField(max_length=32, default='', verbose_name='用户名', help_text='用户名')
    password = models.CharField(max_length=64, default='123456', verbose_name='密码', help_text='密码')
    nickname = models.CharField(max_length=32, default='', verbose_name='昵称', help_text='昵称')
    email = models.EmailField(default='', verbose_name='邮箱', help_text='邮箱')
    gender = models.CharField(max_length=6, choices=(("male",u"男"), ("female", u"女"), ("baomi", u"保密")),default='male')
    status = models.IntegerField(default=1, verbose_name='状态', help_text='状态')
    is_superuser = models.IntegerField(default=0, verbose_name='是否是超级管理员', help_text='是否是超级管理员')
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")
    lastlogintime = models.DateTimeField(default=timezone.now, verbose_name="最后登录时间")
    roles = models.ManyToManyField(Role, related_name='userrole')
    # 定义用户和角色的多对多关系

    def __str__(self):
        return self.nickname
