#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright 2015-2016 Richard Huang <rickypc@users.noreply.github.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
IMAP Library - a IMAP email testing library.
"""

# To use a consistent encoding
import codecs
from os.path import abspath, dirname, join
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

LIBRARY_NAME = 'ImapLibrary'
CWD = abspath(dirname(__file__))
VERSION_PATH = join(CWD, 'src', LIBRARY_NAME, 'version.py')
exec(compile(open(VERSION_PATH).read(), VERSION_PATH, 'exec'))

with codecs.open(join(CWD, 'README.rst'), encoding='utf-8') as reader:
    LONG_DESCRIPTION = reader.read()

setup(
    name='robotframework-%s' % LIBRARY_NAME.lower(),
    version=VERSION,  # pylint: disable=undefined-variable  # noqa
    description='A IMAP email testing library for Robot Framework',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/rickypc/robotframework-%s' % LIBRARY_NAME.lower(),
    author='Richard Huang',
    author_email='rickypc@users.noreply.github.com',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Robot Framework',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Testing',
    ],
    keywords='robot framework testing automation imap email mail softwaretesting',
    platforms='any',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['future', 'robotframework >= 2.6.0']
)
