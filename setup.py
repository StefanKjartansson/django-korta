#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup, find_packages, Command
except ImportError:
    from distutils.core import setup, find_packages, Command

class RunTests(Command):
    description = "Run the django test suite from the test_project dir."

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        this_dir = os.getcwd()
        testproj_dir = os.path.join(this_dir, "test_project")
        os.chdir(testproj_dir)
        sys.path.append(testproj_dir)
        from django.core.management import execute_manager
        os.environ["DJANGO_SETTINGS_MODULE"] = os.environ.get(
                "DJANGO_SETTINGS_MODULE", "test_settings")
        settings_file = os.environ["DJANGO_SETTINGS_MODULE"]
        settings_mod = __import__(settings_file, {}, {}, [''])
        execute_manager(settings_mod, argv=[
            __file__, "test"])
        os.chdir(this_dir)

setup(
    name = "djkorta",
    version = "0.1",
    packages = find_packages(exclude=['test_project']),
    install_requires = [
        'Django==1.3.1',
        'coverage==3.5.1',
        'django-nose==0.1.3',
        'nose==1.1.2',
        'wsgiref==0.1.2',
        'django-uni-form==0.9.0',
    ],
    package_data = {
        'djkorta': ['fixtures/*.json', 'templates/*.*',],
    },
    cmdclass = {"test": RunTests},
    author="stefan",
    author_email="stefan@Stefan-Kjartanssons-MacBook-Pro.local",
    description="",
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
