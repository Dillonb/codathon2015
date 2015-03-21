"""
Django settings for codathon2015 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import ldap
from django_auth_ldap.config import LDAPSearch

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ijmf2__2n62cl^7k_3$+q7)f^$w2s%!w(=0kg!!di0gu76r)gp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'classapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
)

STATIC_URL = "/static/"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,"static"),
    '/var/www/html/static'
)


AUTH_USER_MODEL = "classapp.UVMUser"

AUTH_LDAP_SERVER_URI = "ldap://ldap.uvm.edu"
#AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=People,dc=uvm,dc=edu",
    #ldap.SCOPE_SUBTREE, "(uid=%user)s")
AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=People,dc=uvm,dc=edu"
AUTH_LDAP_START_TLS = True

AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "uvm_email": "mail",
    "full_name": "gecos",
    "department": "ou",
    "netid": "uid"
}

AUTH_LDAP_DENY_GROUP = "eduPersonAffiliation=Faculty"

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_auth_ldap.backend.LDAPBackend',
)

import logging
logger = logging.getLogger("django_auth_ldap")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

ROOT_URLCONF = 'codathon2015.urls'

WSGI_APPLICATION = 'codathon2015.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
