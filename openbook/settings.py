"""
Django settings for openbook project.

Generated by 'django-admin startproject' using Django 1.11.16.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import logging.config
import os
import sys

import sentry_sdk
from django.utils.translation import gettext_lazy  as _
from dotenv import load_dotenv, find_dotenv
from sentry_sdk.integrations.django import DjangoIntegration
from django_replicated.settings import *

# Logging config
from sentry_sdk.integrations.rq import RqIntegration

from openbook_common.utils.environment import EnvironmentChecker

LOGGING_CONFIG = None
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        }
    },
    'loggers': {
        # root logger
        '': {
            'level': 'INFO',
            'handlers': ['console'],
        },
    },
})

logger = logging.getLogger(__name__)

# Load dotenv
load_dotenv(verbose=True, dotenv_path=find_dotenv())

# The current execution environment
ENVIRONMENT = os.environ.get('ENVIRONMENT')

if not ENVIRONMENT:
    if 'test' in sys.argv:
        logger.info('No ENVIRONMENT variable found but test detected. Setting ENVIRONMENT=TEST_VALUE')
        ENVIRONMENT = EnvironmentChecker.TEST_VALUE
    else:
        raise NameError('ENVIRONMENT environment variable is required')

environment_checker = EnvironmentChecker(environment_value=ENVIRONMENT)

# Django SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY')

if not SECRET_KEY:
    raise NameError('SECRET_KEY environment variable is required')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = environment_checker.is_debug()
IS_PRODUCTION = environment_checker.is_production()
IS_BUILD = environment_checker.is_build()
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
if IS_PRODUCTION:
    if not ALLOWED_HOSTS:
        raise NameError('ALLOWED_HOSTS environment variable is required when running on a production environment')
    ALLOWED_HOSTS = [allowed_host.strip() for allowed_host in ALLOWED_HOSTS.split(',')]
else:
    if ALLOWED_HOSTS:
        logger.info('ALLOWED_HOSTS environment variable ignored.')
    ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # Has to be before contrib admin
    # See https://django-modeltranslation.readthedocs.io/en/latest/installation.html#required-settings
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_nose',
    'ordered_model',
    'storages',
    'video_encoding',
    'imagekit',
    'django_media_fixtures',
    'cacheops',
    'django_rq',
    'scheduler',
    'django_extensions',
    'openbook_common',
    'openbook_auth',
    'openbook_posts',
    'openbook_circles',
    'openbook_connections',
    'openbook_importer',
    'openbook_lists',
    'openbook_follows',
    'openbook_communities',
    'openbook_invitations',
    'openbook_tags',
    'openbook_categories',
    'openbook_notifications',
    'openbook_devices',
    'openbook_moderation',
    'openbook_translation',
]

MODELTRANSLATION_FALLBACK_LANGUAGES = ('en',)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'openbook_common.middleware.TimezoneMiddleware'
]

ROOT_URLCONF = 'openbook.urls'

AUTH_USER_MODEL = 'openbook_auth.User'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
REDIS_DEFAULT_DB = int(os.environ.get('REDIS_DEFAULT_DB', '0'))

redis_protocol = 'rediss://' if IS_PRODUCTION else 'redis://'

redis_password = '' if not REDIS_PASSWORD else ':%s' % REDIS_PASSWORD

REDIS_LOCATION = '%(protocol)s%(password)s@%(host)s:%(port)d' % {'protocol': redis_protocol,
                                                                 'password': redis_password,
                                                                 'host': REDIS_HOST,
                                                                 'port': REDIS_PORT}

RQ_SHOW_ADMIN_LINK = True

RQ_QUEUES_REDIS_DB = int(os.environ.get('RQ_QUEUES_REDIS_DB', '2'))

CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": '%(redis_location)s/%(db)d' % {'redis_location': REDIS_LOCATION, 'db': REDIS_DEFAULT_DB},
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "ob-api-"
    },
    'rq-queues': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": '%(redis_location)s/%(db)d' % {'redis_location': REDIS_LOCATION, 'db': RQ_QUEUES_REDIS_DB},
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "ob-api-rq-"
    }
}

CACHEOPS_REDIS_DB = int(os.environ.get('CACHEOPS_REDIS_DB', '1'))

CACHEOPS_REDIS = '%(redis_location)s/%(db)d' % {'redis_location': REDIS_LOCATION, 'db': CACHEOPS_REDIS_DB}

CACHEOPS_DEFAULTS = {
    'timeout': 60 * 60
}

CACHEOPS = {
    # Don't cache anything automatically
    '*.*': {},
}

RQ_QUEUES = {
    'default': {
        'USE_REDIS_CACHE': 'rq-queues',
    },
}

if IS_BUILD:
    NOSE_ARGS = [
        '--cover-erase',
        '--cover-package=.',
        '--with-spec', '--spec-color',
        '--with-coverage', '--cover-xml',
        '--verbosity=1', '--nologcapture']
else:
    NOSE_ARGS = [
        '--cover-erase',
        '--cover-package=.',
        '--with-spec', '--spec-color',
        '--with-coverage', '--cover-html',
        '--cover-html-dir=reports/cover', '--verbosity=1', '--nologcapture', '--nocapture']

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

WSGI_APPLICATION = 'openbook.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if IS_BUILD or TESTING:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'open-book-api'
        }
    }
else:
    RDS_DB_NAME = os.environ.get('RDS_DB_NAME')
    RDS_USERNAME = os.environ.get('RDS_USERNAME')
    RDS_PASSWORD = os.environ.get('RDS_PASSWORD')
    RDS_PORT = os.environ.get('RDS_PORT')
    RDS_HOSTNAME = os.environ.get('RDS_HOSTNAME')

    RDS_HOSTNAME_WRITER = os.environ.get('RDS_HOSTNAME_WRITER', RDS_HOSTNAME)
    RDS_HOSTNAME_READER = os.environ.get('RDS_HOSTNAME_READER', RDS_HOSTNAME_WRITER)

    db_options = {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        'charset': 'utf8mb4'
    }

    writer_db_config = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': RDS_DB_NAME,
        'USER': RDS_USERNAME,
        'PASSWORD': RDS_PASSWORD,
        'HOST': RDS_HOSTNAME_WRITER,
        'PORT': RDS_PORT,
        'OPTIONS': db_options,
    }

    DATABASES = {
        'default': writer_db_config,
        'Reader': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': RDS_DB_NAME,
            'USER': RDS_USERNAME,
            'PASSWORD': RDS_PASSWORD,
            'HOST': RDS_HOSTNAME_READER,
            'PORT': RDS_PORT,
            'OPTIONS': db_options,
        }
    }

    DATABASE_ROUTERS = ['django_replicated.router.ReplicationRouter']

    REPLICATED_DATABASE_SLAVES = ['Reader', ]

    MIDDLEWARE.append('django_replicated.middleware.ReplicationMiddleware', )

    REPLICATED_VIEWS_OVERRIDES = {
        '/admin/*': 'master',
    }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# REST Framework config

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

# AWS Translate
AWS_TRANSLATE_REGION = os.environ.get('AWS_TRANSLATE_REGION', '')
AWS_TRANSLATE_MAX_LENGTH = os.environ.get('AWS_TRANSLATE_MAX_LENGTH', 10000)
if TESTING:
    OS_TRANSLATION_STRATEGY_NAME = 'testing'
else:
    OS_TRANSLATION_STRATEGY_NAME = 'default'

OS_TRANSLATION_CONFIG = {
    'default': {
        'STRATEGY': 'openbook_translation.strategies.amazon.AmazonTranslate',
        'TEXT_MAX_LENGTH': AWS_TRANSLATE_MAX_LENGTH,
        'DEFAULT_TRANSLATION_LANGUAGE_CODE': 'en'
    },
    'testing': {
        'STRATEGY': 'openbook_translation.strategies.tests.MockAmazonTranslate',
        'TEXT_MAX_LENGTH': 40,
        'DEFAULT_TRANSLATION_LANGUAGE_CODE': 'en'
    }
}

UNICODE_JSON = True

# The sentry DSN for error reporting
SENTRY_DSN = os.environ.get('SENTRY_DSN')
if IS_PRODUCTION:
    if not SENTRY_DSN:
        raise NameError('SENTRY_DSN environment variable is required when running on a production environment')
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), RqIntegration()]
    )
else:
    if SENTRY_DSN:
        logger.info('SENTRY_DSN environment variable ignored.')

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/


TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = [
    ('es', _('Spanish')),
    ('en', _('English')),
    ('de', _('German')),
    ('sv', _('Swedish')),
    ('fr', _('French')),
    ('it', _('Italian')),
    ('tr', _('Turkish')),
    ('pt-br', _('Portuguese, Brazilian')),
]

LANGUAGE_CODE = 'en'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'

MEDIA_ROOT = os.environ.get('MEDIA_ROOT', './media')

MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'openbook/static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Video encoding

VIDEO_ENCODING_FORMATS = {
    'FFmpeg': [
        {
            'name': 'mp4_sd',
            'extension': 'mp4',
            'params': [
                '-codec:v', 'libx264', '-crf', '20', '-preset', 'medium',
                '-b:v', '1000k', '-maxrate', '1000k', '-bufsize', '2000k',
                '-vf', 'scale=-2:480',  # http://superuser.com/a/776254
                '-codec:a', 'aac', '-b:a', '128k', '-strict', '-2',
            ],
        },
        {
            'name': 'webm_sd',
            'extension': 'webm',
            'params': [
                '-b:v', '1000k', '-maxrate', '1000k', '-bufsize', '2000k',
                '-codec:v', 'libvpx', '-r', '30',
                '-vf', 'scale=-1:480', '-qmin', '10', '-qmax', '42',
                '-codec:a', 'libvorbis', '-b:a', '128k', '-f', 'webm',
            ],
        },
    ]
}

PROXY_URL = os.environ.get('PROXY_URL')

# Openbook config

USERNAME_MAX_LENGTH = 30
USER_MAX_FOLLOWS = int(os.environ.get('USER_MAX_FOLLOWS', '1500'))
USER_MAX_CONNECTIONS = int(os.environ.get('USER_MAX_CONNECTIONS', '1500'))
USER_MAX_COMMUNITIES = 200
POST_MAX_LENGTH = int(os.environ.get('POST_MAX_LENGTH', '5000'))
POST_COMMENT_MAX_LENGTH = int(os.environ.get('POST_MAX_LENGTH', '1500'))
POST_IMAGE_MAX_SIZE = int(os.environ.get('POST_IMAGE_MAX_SIZE', '10485760'))
POST_LINK_MAX_DOMAIN_LENGTH = int(os.environ.get('POST_LINK_MAX_DOMAIN_LENGTH', '126'))
POST_MEDIA_MAX_ITEMS = int(os.environ.get('POST_MEDIA_MAX_ITEMS', '1'))
PASSWORD_MIN_LENGTH = 10
PASSWORD_MAX_LENGTH = 100
CIRCLE_MAX_LENGTH = 100
COLOR_ATTR_MAX_LENGTH = 7
LIST_MAX_LENGTH = 100
PROFILE_NAME_MAX_LENGTH = 192
PROFILE_LOCATION_MAX_LENGTH = 64
PROFILE_BIO_MAX_LENGTH = int(os.environ.get('PROFILE_BIO_MAX_LENGTH', '1000'))
PROFILE_AVATAR_MAX_SIZE = int(os.environ.get('PROFILE_AVATAR_MAX_SIZE', '10485760'))
PROFILE_COVER_MAX_SIZE = int(os.environ.get('PROFILE_COVER_MAX_SIZE', '10485760'))
WORLD_CIRCLE_ID = 1
PASSWORD_RESET_TIMEOUT_DAYS = 1
COMMUNITY_NAME_MAX_LENGTH = 32
COMMUNITY_TITLE_MAX_LENGTH = 32
COMMUNITY_DESCRIPTION_MAX_LENGTH = 500
COMMUNITY_USER_ADJECTIVE_MAX_LENGTH = 16
COMMUNITY_USERS_ADJECTIVE_MAX_LENGTH = 16
COMMUNITY_RULES_MAX_LENGTH = int(os.environ.get('COMMUNITY_RULES_MAX_LENGTH', '5000'))
COMMUNITY_CATEGORIES_MAX_AMOUNT = 3
COMMUNITY_CATEGORIES_MIN_AMOUNT = 1
COMMUNITY_AVATAR_MAX_SIZE = int(os.environ.get('COMMUNITY_AVATAR_MAX_SIZE', '10485760'))
COMMUNITY_COVER_MAX_SIZE = int(os.environ.get('COMMUNITY_COVER_MAX_SIZE', '10485760'))
TAG_NAME_MAX_LENGTH = 32
CATEGORY_NAME_MAX_LENGTH = 32
CATEGORY_TITLE_MAX_LENGTH = 64
CATEGORY_DESCRIPTION_MAX_LENGTH = 64
DEVICE_NAME_MAX_LENGTH = 32
DEVICE_UUID_MAX_LENGTH = 64
SEARCH_QUERIES_MAX_LENGTH = 120
FEATURE_VIDEO_POSTS_ENABLED = os.environ.get('FEATURE_VIDEO_POSTS_ENABLED', 'True') == 'True'
FEATURE_IMPORTER_ENABLED = os.environ.get('FEATURE_IMPORTER_ENABLED', 'True') == 'True'
MODERATION_REPORT_DESCRIPTION_MAX_LENGTH = 1000
MODERATED_OBJECT_DESCRIPTION_MAX_LENGTH = 1000
GLOBAL_HIDE_CONTENT_AFTER_REPORTS_AMOUNT = int(os.environ.get('GLOBAL_HIDE_CONTENT_AFTER_REPORTS_AMOUNT', '20'))
MODERATORS_COMMUNITY_NAME = os.environ.get('MODERATORS_COMMUNITY_NAME', 'mods')
PROXY_WHITELIST_DOMAIN_MAX_LENGTH = 150
SUPPORTED_MEDIA_MIMETYPES = [
    'video/mp4',
    'video/3gpp',
    'image/gif',
    'image/jpeg',
    'image/png'
]

# Email Config

EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'
AWS_SES_REGION = os.environ.get('AWS_SES_REGION')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
SERVICE_EMAIL_ADDRESS = os.environ.get('SERVICE_EMAIL_ADDRESS')
EMAIL_HOST = os.environ.get('EMAIL_HOST')

# AWS Storage config

AWS_PUBLIC_MEDIA_LOCATION = os.environ.get('AWS_PUBLIC_MEDIA_LOCATION')
AWS_STATIC_LOCATION = 'static'
AWS_PRIVATE_MEDIA_LOCATION = os.environ.get('AWS_PRIVATE_MEDIA_LOCATION')
AWS_DEFAULT_ACL = None

if IS_PRODUCTION:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
    AWS_S3_ENCRYPTION = True
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_HOST = os.environ.get('AWS_S3_HOST', 's3.amazonaws.com')
    AWS_S3_CUSTOM_DOMAIN = '%s.%s' % (AWS_STORAGE_BUCKET_NAME, AWS_S3_HOST)

    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_PUBLIC_MEDIA_LOCATION)

    STATICFILES_STORAGE = 'openbook.storage_backends.S3StaticStorage'

    DEFAULT_FILE_STORAGE = 'openbook.storage_backends.S3PublicMediaStorage'

    PRIVATE_FILE_STORAGE = 'openbook.storage_backends.S3PrivateMediaStorage'

# ONE SIGNAL
ONE_SIGNAL_APP_ID = os.environ.get('ONE_SIGNAL_APP_ID')
ONE_SIGNAL_API_KEY = os.environ.get('ONE_SIGNAL_API_KEY')
