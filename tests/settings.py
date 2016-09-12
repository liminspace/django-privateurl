import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'test'

DEBUG = True

SITE_ID = 1

INSTALLED_APPS = (
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'privateurl',
    'tests',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tests.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3'),
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'dju',
        # 'USER': 'root',
        # 'PASSWORD': '',
    }
}

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

EMAIL_SUBJECT_PREFIX = '[Django test] '
EMAIL_RETURN_PATH = 'return.path@example.com'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': (os.path.join(BASE_DIR, 'templates'),),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.template.context_processors.csrf',
            ),
        },
    },
]

PRIVATEURL_URL_NAMESPACE = 'purl'
