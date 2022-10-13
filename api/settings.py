"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from datetime import timedelta
import os
import dj_database_url

try:
    from api.secrets import (PROD_SECRET_KEY,
                             # AWS_ACCESS_KEY_ID,
                             # AWS_SECRET_ACCESS_KEY,
                             SENDER_EMAIL_ADDRESS,
                             EMAIL_HOST_USER,
                             EMAIL_HOST_PASSWORD,
                             TMP_ALLOWED_ORIGIN_1)
except ImportError:
    try:
        PROD_SECRET_KEY = os.environ['SECRET_KEY']
        # AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
        # AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
        # SENDER_EMAIL_ADDRESS = os.environ['SENDER_EMAIL_ADDRESS']
        EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
        EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
        TMP_ALLOWED_ORIGIN_1 = os.environ['TMP_ALLOWED_ORIGIN_1']
    except KeyError:
        raise IOError('Missing configuration.')


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


######################################
###                                ###
###   MANUAL SETTINGS START HERE   ###
###                                ###

DEBUG = False
JWT_AUTH = True

###                                ###
###    MANUAL SETTINGS END HERE    ###
###                                ###
######################################


# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = '_k)j9k^4k2$_mjlspiccb$%zd4_q$(&4*)o#b28j2!e^m&ne35' if DEBUG else PROD_SECRET_KEY

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', 'anki-webapp-backend.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'django_filters',
    'whitenoise.runserver_nostatic',
    'anki',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    # in case I run a couple of other React apps:
    'http://localhost:3001',
    'http://localhost:3002',
    'http://localhost:3003',
    TMP_ALLOWED_ORIGIN_1
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r'^https://anki-webapp.*\.vercel\.app$',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'api.wsgi.application'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# AWS SES (temporarily unavailable) TODO: new AWS account, new SES
# EMAIL_BACKEND = 'django_ses.SESBackend'
# Tmp solution:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
# EMAIL_HOST_USER is retrieved from env | secrets.py
# EMAIL_HOST_PASSWORD is retrieved from env | secrets.py


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'anki_db',
        'USER': 'krastsislau',
        'PASSWORD': '$def#pass',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
