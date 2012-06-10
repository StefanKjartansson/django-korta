from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}

INSTALLED_APPS += ('djkorta',)
#INSTALLED_APPS += ('uni_form',)

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
