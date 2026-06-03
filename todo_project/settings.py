import os
import ssl
import certifi
from pathlib import Path


# ================= BASE DIRECTORY =================
BASE_DIR = Path(__file__).resolve().parent.parent


# ================= SECURITY =================
# Read sensitive settings from environment variables for deployment
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-replace-me')

# Set DEBUG via environment variable (default True for local development)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS can be a comma-separated list in env, otherwise empty list
ALLOWED_HOSTS =['*']


# ================= INSTALLED APPS =================
INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CUSTOM APP
    'rest_framework',
    'tasks',
]


# ================= MIDDLEWARE =================
MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ================= URL CONFIG =================
ROOT_URLCONF = 'todo_project.urls'


# ================= TEMPLATES =================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [BASE_DIR / 'templates'],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]


# ================= WSGI =================
WSGI_APPLICATION = 'todo_project.wsgi.application'


# ================= DATABASE =================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ================= PASSWORD VALIDATION =================
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


# ================= LANGUAGE =================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ================= STATIC FILES =================
STATIC_URL = '/static/'
# if you need a global static folder in the future:
# STATICFILES_DIRS = [BASE_DIR / "static"]

# for production collectstatic
STATIC_ROOT = BASE_DIR / "staticfiles"


# ================= LOGIN SETTINGS =================
LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'home'

LOGOUT_REDIRECT_URL = 'login'


# ================= EMAIL CONFIGURATION =================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_USE_SSL = False

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')

# Gmail App Password (set in environment; do not commit plaintext passwords)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# ================= SSL CERTIFICATE FIX =================

ssl._create_default_https_context = ssl.create_default_context(
    cafile=certifi.where()
)


# ================= DEFAULT PRIMARY KEY =================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'