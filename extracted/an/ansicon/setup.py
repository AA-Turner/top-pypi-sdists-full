#!/usr/bin/env python
# Copyright 2017 Avram Lubkin, All Rights Reserved

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
A Python wrapper for loading Jason Hood's ANSICON

ANSICON can be found at https://github.com/adoxa/ansicon
"""

import io

from setuptools import setup


def readme(filename, encoding='utf8'):
    """
    Read the contents of a file
    """

    with io.open(filename, encoding=encoding) as source:
        return source.read()


setup(
    name='ansicon',
    version='1.89.0',
    description="Python wrapper for loading Jason Hood's ANSICON",
    long_description=readme('README.rst'),
    author='Avram Lubkin',
    author_email='avylove@rockhopper.net',
    maintainer='Avram Lubkin',
    maintainer_email='avylove@rockhopper.net',
    url='https://github.com/Rockhopper-Technologies/ansicon',
    license='MPLv2.0',
    zip_safe=False,
    install_requires=[],
    tests_require=[],
    packages=['ansicon'],
    package_data={'ansicon': ['*.dll']},
    test_suite='tests',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords='ansicon terminal console',
)
