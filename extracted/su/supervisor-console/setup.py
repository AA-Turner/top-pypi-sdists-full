#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import os

from setuptools import setup, find_packages

_Version='0.5.2'

setup(
    name = 'supervisor-console',
    version = _Version,
    py_modules = ['supervisor_console'],
    author = 'Carsten Igel',
    author_email = 'cig@bite-that-bit.de',
    description = '',
    long_description = '',
    license = 'BSD-3-Clause',
    keywords = '',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    url = 'https://github.com/carstencodes/supervisor-console',
    install_requires=[
        "supervisor >= 4.0"
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: Log Analysis',
        'Topic :: System',
        'Topic :: System :: Boot',
        'Topic :: System :: Boot :: Init',
        'Topic :: System :: Logging',
        'Typing :: Typed'
    ],
    entry_points = {
        'console_scripts': [
            'supervisor-console = supervisor_console.__main__:main',
        ]
    }
)
