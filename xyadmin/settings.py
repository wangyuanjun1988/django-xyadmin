"""
Django settings for xyadmin project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%d)@a-y_8d63qfe6*uf%ov4&1@pwr@)y+dofy=as=#_^_lfk1='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'django_celery_beat',
    'rest_framework',
    'apps.rbac',
    'apps.myadmin',
    'apps.taskproj'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.rbac.middleware.rbac.RbacMiddleware',
]
X_FRAME_OPTIONS = 'SAMEORIGIN'
ROOT_URLCONF = 'xyadmin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'xyadmin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xyadmin',
        'HOST': '127.0.0.1',
        'USER': 'wang',
        'PASSWORD': '123456',
        'OPTIONS': {'charset':'utf8mb4'},
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    #     # Put strings here, like "/home/html/static" or "C:/www/django/static".
    #     # Always use forward slashes, even on Windows.
    #     # Don't forget to use absolute paths, not relative paths.
)

LOGIN_REDIRECT_URL = '/index/'

# 定义session 键：
# 保存用户权限url列表
# 保存 权限菜单 和所有 菜单
SESSION_PERMISSION_URL_KEY = 'xy_permission_url'

SESSION_HEAD_MENU_KEY = 'xy_head_menu'
SESSION_MENU_KEY = 'xy_menu_key'
ALL_MENU_KEY = 'xy_all_menu_key'
PERMISSION_MENU_KEY = 'xy_permission_menu'

LOGIN_URL = '/xyadmin/login'
REGEX_URL = r'^{url}'  # url作严格匹配
REGEX_PHONE = r'^1[3-9]\d{9}$'

# 配置url权限白名单
SAFE_URL = [
    '/xyadmin/login',
    '/xyadmin/logout',
    '/xyadmin/rbac/menuchild',
    '/xyadmin/task/*',
]

# CELERY
CELERY_BROKER_URL = 'redis://:football@192.168.85.131:13379/11' # Broker配置，使用Redis作为消息中间件
# CELERY_RESULT_BACKEND = 'redis://:football@192.168.85.131:13379/11' # BACKEND配置，这里使用redis
CELERY_RESULT_BACKEND = 'django-db' # 使用django orm 作为结果存储
CELERY_RESULT_SERIALIZER = 'json' # 结果序列化方案