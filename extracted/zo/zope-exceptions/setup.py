##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
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
# This package is developed by the Zope Toolkit project, documented here:
# https://zopetoolkit.readthedocs.io/
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.exceptions package
"""
import os

from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='zope.exceptions',
    version='6.0',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.dev',
    description='Zope Exceptions',
    long_description=(read('README.rst') + '\n\n' +
                      read('CHANGES.rst')),
    keywords='zope exceptions',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope :: 3',
    ],
    url='https://github.com/zopefoundation/zope.exceptions',
    project_urls={
        'Issue Tracker': ('https://github.com/zopefoundation/'
                          'zope.exceptions/issues'),
        'Sources': 'https://github.com/zopefoundation/zope.exceptions',
    },
    license='ZPL-2.1',
    python_requires='>=3.9',
    install_requires=[
        'setuptools',
        'zope.interface',
    ],
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'docs': ['Sphinx', 'repoze.sphinx.autointerface'],
        'test': ['zope.testrunner >= 6.4'],
    },
)
