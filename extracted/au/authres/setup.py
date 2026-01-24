# -*- coding: ISO-8859-1
#  Copyright © 2011 Scott Kitterman <scott@kitterman.com>

#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at

#    https://www.apache.org/licenses/LICENSE-2.0

#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from setuptools import setup

setup(name='authres',
    version='1.2.0',
    description='authres - Authentication Results Header Module',
    author='Julian Mehnle, Scott Kitterman',
    author_email='julian@mehnle.net',
    url='https://launchpad.net/authentication-results-python',
    license='Apache 2.0',
    packages = ['authres',],
    include_package_data=True,
    package_data = {'authres': ['tests']},
    keywords = ['dkim', 'spf', 'dmarc', 'email', 'authentication', 'rfc5451', 'rfc7001', 'rfc7601', 'rfc8601'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Email :: Mail Transport Agents',
        'Topic :: Communications :: Email :: Filters',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe = False,
)
