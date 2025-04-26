# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

if sys.version_info[0] < 3:
    with open('README.md', 'r') as fh:
        long_description = fh.read()
else:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()

setup(
    name='apimatic-requests-client-adapter',
    version='0.1.7',
    description='An adapter for requests client library consumed by the SDKs generated with APIMatic',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='APIMatic',
    author_email='support@apimatic.io',
    license='MIT',
    url='https://github.com/apimatic/requests-client-adapter',
    packages=find_packages(),
    install_requires=[
        'apimatic-core-interfaces~=0.1.0',
        'requests~=2.31',
        'cachecontrol~=0.12.6'
    ],
    tests_require=[
        'pytest~=7.2.2',
        'pytest-cov~=4.0.0'
    ]
)
