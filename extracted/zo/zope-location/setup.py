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
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.location package
"""
import os

from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


setup(
    name='zope.location',
    version='6.0',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.dev',
    description='Zope Location',
    long_description=(
        read('README.rst') + '\n\n' + read('CHANGES.rst')),
    license='ZPL-2.1',
    keywords=('zope location structural'),
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
            'Framework :: Zope :: 5',
    ],
    url='http://github.com/zopefoundation/zope.location/',
    python_requires='>=3.9',
    install_requires=[
        'setuptools',
        'zope.interface>=4.0.2',
        'zope.schema>=4.2.2',
        'zope.proxy>=4.0.1',
    ],
    extras_require={
        'zcml': ['zope.configuration'],
        'component': ['zope.component >= 4.0.1'],
        'copy': ['zope.copy >= 4.0'],
        'test-minimal': ['zope.testrunner >= 6.4'],
        'test-component': [
            'zope.testrunner >= 6.4',
            'zope.component >= 4.0.1',
            'zope.configuration',
        ],
        'test': [
            'zope.testrunner >= 6.4',
            'zope.configuration',
            'zope.component >= 4.0.1',
            'zope.copy >= 4.0',
        ],
        'docs': [
            'repoze.sphinx.autointerface',
            'Sphinx',
            'zope.component >= 4.0.1',
            'zope.configuration',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
