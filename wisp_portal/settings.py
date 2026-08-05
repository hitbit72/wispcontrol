"""
Configuración de Django para el proyecto Portal WISP.

Fase actual: NÚCLEO
- Modelo de datos base (usuarios, clientes, contratos, sectores, dispositivos, interfaces, enlaces)
- Autenticación con roles (administrador / técnico)
- Sin monitorización, sin API MikroTik, sin dashboard todavía (fases siguientes)
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Seguridad -----------------------------------------------------------
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'clave-insegura-solo-para-desarrollo-cambiar-en-produccion'
)
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# --- Apps ------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps propias del núcleo
    'accounts',
    'clientes',
    'red',
    'mikrotik',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wisp_portal.urls'

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

WSGI_APPLICATION = 'wisp_portal.wsgi.application'
ASGI_APPLICATION = 'wisp_portal.asgi.application'

# --- Base de datos: PostgreSQL --------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'wisp_portal'),
        'USER': os.environ.get('DB_USER', 'wisp_admin'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# --- Usuario personalizado (con roles) ------------------------------------
AUTH_USER_MODEL = 'accounts.Usuario'

# --- Cifrado de campos sensibles (ej. clave API de routers MikroTik) ------
# Generar con: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
FIELD_ENCRYPTION_KEY = os.environ.get('FIELD_ENCRYPTION_KEY')

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'login'

# --- Internacionalización --------------------------------------------------
LANGUAGE_CODE = 'es'
TIME_ZONE = os.environ.get('DJANGO_TIME_ZONE', 'Europe/Madrid')
USE_I18N = True
USE_TZ = True

# --- Archivos estáticos ------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- Datos del mikrotik -----------------------------------------------------------
#
# Estos datos son configurados directamente en el router y se usan para crear los secrets PPPoE y las colas simples.
#
# ACTIVE_LIST = Nombre de la lista de firewall donde se agregan los clientes activos.
# PPP_DISABLED = Nombre del profile PPPoE que se asigna a los clientes deshabilitados.
# parent, busrt-limit, busrt-threshold, burst-time, bucket-size, queue, total-queue, place-before: son parámetros de la cola simple preconfigurados en el mikrotik que se aplican a todos los clientes.

MK_OPTIONS = {
    'ACTIVE_LIST': 'ACTIVE_USER',
    'PPP_DISABLED': 'DISABLE_USER',
    'SIMPLE_QUEUE': {
        'name': '',
        'target': '',
        'parent': 'LAN_TOTAL',
        'max_limit': '5M/10M',
        'limit-at': '2M/5M',
        'priority': '6/6',
        'burst-limit': '0/0',
        'burst-threshold': '0/0',
        'burst-time': '0s/0s',
        'bucket-size': '0.1/0.1',
        'queue': 'cake-fibra/cake-fibra',
        'total-queue': 'default',
        'place-before': 'Ciber1',
        'comment': ''
    },
    'SECRET': {
        'name': '',
        'password': '',
        'profile': 'default',
        'service': 'pppoe',
        'comment': ''
    },
	'FW_LIST': {
		'address': '',
		'list': 'ACTIVE_USER',
		'comment': '',
		'disabled':'no'
	}
}