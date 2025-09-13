##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""zope.ptresource setup
"""
import os

from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


long_description = (read('README.rst') + '\n\n' + read('CHANGES.rst'))

TESTS_REQUIRE = [
    'zope.testing',
    'zope.testrunner >= 6.4',
]

setup(
    name='zope.ptresource',
    version='6.0',
    url='https://github.com/zopefoundation/zope.ptresource/',
    project_urls={
        'Issue Tracker': ('https://github.com/zopefoundation/'
                          'zope.ptresource/issues'),
        'Sources': 'https://github.com/zopefoundation/zope.ptresource',
    },
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.dev',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope :: 3',
    ],
    description='Page template resource plugin for zope.browserresource',
    long_description=long_description,
    license='ZPL-2.1',
    python_requires='>=3.9',
    install_requires=[
        'setuptools',
        'zope.browserresource',
        'zope.interface',
        'zope.pagetemplate',
        'zope.publisher',
        'zope.security',
    ],
    extras_require={
        'test': TESTS_REQUIRE
    },
    include_package_data=True,
    zip_safe=False,
)
