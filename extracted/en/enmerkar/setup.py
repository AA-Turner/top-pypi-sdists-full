#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


setup(
    name='enmerkar',
    description='Utilities for using Babel in Django',
    long_description=read('README.rst') + u'\n\n' + read('CHANGELOG.rst'),
    version='0.7.1',
    license='BSD',
    author='Christopher Grebs',
    author_email='cg@webshox.org',
    maintainer='Zego',
    maintainer_email='opensource@zego.com',
    url='https://github.com/Zegocover/enmerkar',
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'django>=2.2',
        'babel>=1.3',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    entry_points={
        'babel.extractors': [
            'django = enmerkar.extract:extract_django',
        ]
    }
)
