from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'test.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

INSTALLED_APPS += ('djkorta',)
INSTALLED_APPS += ('uni_form',)

INSTALLED_APPS += ('django_nose',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['djkorta',
    '--failed',
    '--stop',
    '--with-coverage',
    '--cover-erase',
    '--cover-package=djkorta',
    '--cover-tests',
]

from local_settings import *
