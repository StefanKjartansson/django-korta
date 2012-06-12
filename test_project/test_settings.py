from settings import *

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))


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
