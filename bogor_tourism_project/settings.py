import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# ============================================================
# SUB-PATH CONFIGURATION (untuk deploy di subdirectory)
# ============================================================
# Jika aplikasi diakses via sub-path seperti /python, set di .env
# Contoh: SUB_PATH=/python atau kosongkan untuk root domain
SUB_PATH = config('SUB_PATH', default='').rstrip('/')  # hapus trailing slash

if SUB_PATH:
    FORCE_SCRIPT_NAME = SUB_PATH
    USE_X_FORWARDED_HOST = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',  # Untuk fitur geospasial
    
    # Third party apps
    'django_extensions',
    
    # Local apps
    'tourism_app',
    'maps_app',
    'analytics_app',

    # format rupiah
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files serving
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bogor_tourism_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'bogor_tourism_project.wsgi.application'
ASGI_APPLICATION = 'bogor_tourism_project.asgi.application'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',  # PostGIS untuk geospatial
        # 'OPTIONS': {
        #     'driver': 'psycopg',  # Untuk memastikan django pakai psycopg versi terbaru
        # },
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# ============================================================
# STATIC FILES CONFIGURATION
# ============================================================
# Static URL akan otomatis berprefix SUB_PATH jika diset
STATIC_URL = f'{SUB_PATH}/static/' if SUB_PATH else '/static/'
# Path absolut folder static di server
STATIC_ROOT = config('STATIC_ROOT', default=str(BASE_DIR / 'staticfiles'))
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# ============================================================
# MEDIA FILES CONFIGURATION
# ============================================================
# Media URL akan otomatis berprefix SUB_PATH jika diset
MEDIA_URL = f'{SUB_PATH}/media/' if SUB_PATH else '/media/'

# Path absolut folder media di server
MEDIA_ROOT = config('MEDIA_ROOT', default=str(BASE_DIR / 'media'))

# Internationalization
LANGUAGE_CODE = 'id'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB


# ============================================================
# SECURITY SETTINGS (Production)
# ============================================================
# if not DEBUG:
#     SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SECURE_BROWSER_XSS_FILTER = True
#     SECURE_CONTENT_TYPE_NOSNIFF = True
#     X_FRAME_OPTIONS = 'DENY'
