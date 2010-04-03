# Django settings for django_foafssl project.


import os.path
import sys
import foafssl
import posixpath

FOAFSSL_ROOT = os.path.abspath(os.path.dirname(foafssl.__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SERVE_MEDIA = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS


# Fix up foafssl imports here. We would normally place foafssl in 
# a directory accessible via the Django app, but this is an
# example and we ship it a couple of directories up.
#sys.path.insert(0, os.path.join(PROJECT_ROOT, '../../django_foafssl/'))

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = ''
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = ''
MEDIA_URL = '/site_media/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'static')
#STATIC_ROOT = os.path.join(PROJECT_ROOT, 'media')
STATIC_URL = '/site_media/static/'
STATICFILES_DIRS = (
    ('gencert', os.path.join(PROJECT_ROOT, 'media')),
    ('foafssl', os.path.join(FOAFSSL_ROOT, 'media')),
)


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media/'
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'esz%-6@ht$qka5t554t)3(fm)-2l36f65c+ez7qj^ok375duec'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'gencert.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
#    os.path.join(PROJECT_ROOT, '../../django_foafssl/templates'),
    os.path.join(FOAFSSL_ROOT, "templates"),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
#    "misc.context_processors.contact_email",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'foafssl',
    'uni_form'
)

# settings for jabberd
JABBER_DOMAIN = 'xmpp.rhizomatik.net'
#JABBER_DOMAIN = 'calamar.net'
JABBER_CACERT_PATH = os.path.join(PROJECT_ROOT, 'jabberd_data/xmpp_foaf_cacert.pem')
JABBER_CAKEY_PATH = os.path.join(PROJECT_ROOT, 'jabberd_data/xmpp_foaf_cakey.key')
CERT_SERIAL_PATH = os.path.join(PROJECT_ROOT, 'jabberd_data/xmpp_foaf_cert_serial.txt')
