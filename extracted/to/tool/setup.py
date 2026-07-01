#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from _version import version


setup(
    name = 'tool',
    version = version,
    packages = find_packages(),
    package_data = {
        'tool': ['ext/*/*/*.html'],
    },

    install_requires = [
        'argh >= 0.2.0',         # console interface
        'pydispatcher >= 2.0.1', # signals
        'pyyaml >= 3.08',        # configuration
    ],
    test_suite = 'nose.collector',
    tests_require = ['coverage >= 3.3', 'nose >= 0.11'],

    # metadata for upload to PyPI
    author = 'Andrey Mikhaylenko',
    author_email = 'andy@neithere.net',
    description = 'A compact modular conf/web/console framework.',
    long_description='A compact modular conf/web/console framework.',
    license = 'GPL3',
    keywords = 'wsgi web framework',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
