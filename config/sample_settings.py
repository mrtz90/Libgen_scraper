# At first create local_settings.py and put this information on it.

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<enter you secret key here>'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': '<database_name>',
       'USER': '<database_username>',
       'PASSWORD': '<password>',
       'HOST': '<database_hostname_or_ip>',
       'PORT': '<database_port>',
   }
}
