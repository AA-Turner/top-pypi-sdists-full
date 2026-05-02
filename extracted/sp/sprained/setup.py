#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 K. Richard Pixley.
# See LICENSE for details.
#
# Time-stamp: <02-Mar-2010 07:18:25 PST by rich@noir.com>

import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='sprained',
    version='0.008',
    author='K. Richard Pixley',
    author_email='rich@noir.com',
    description='An integration of the spread toolkit, (http://spread.org), with twisted.',
    license='MIT',
    keywords='twisted spread',
    url='http://packages.python.org/sprained',
    long_description=read('README'),
    # setup_requires=[
    # 	'nose>=0.11.1',
    # ],
    install_requires=[
    	'nose>=0.11.1',
        'Twisted>=9.0.0',
        'SpreadModule>=1.5',
        'metaserializer>=0.006',
    ],
    packages=find_packages(),
    include_package_data=True,
    test_suite='nose.collector',
    py_modules=['sprained'],
    requires=[
        'collections',
        'metaserializer',
        'os',
        'spread',
        'twisted.internet',
        'zope.interface',
    ],
    provides=[
        'sprained',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Twisted',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
    ],
)
