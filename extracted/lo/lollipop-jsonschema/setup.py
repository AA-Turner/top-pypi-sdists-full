#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='lollipop-jsonschema',
    version='0.9.0',
    description=('Library to convert Lollipop schema to JSON schema'),
    long_description=read('README.rst'),
    author='Maxim Kulkin',
    author_email='maxim.kulkin@gmail.com',
    url='https://github.com/maximkulkin/lollipop-jsonschema',
    packages=['lollipop_jsonschema'],
    include_package_data=True,
    install_requires=['lollipop>=1.1.5'],
    license='MIT',
    zip_safe=False,
    keywords=('lollipop', 'json', 'schema'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
