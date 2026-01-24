#!/usr/bin/env python

"""
/*******************************************************************************
 * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
 * All rights reserved.
 * 
 * Contributors:
 *     Cambridge Semantics Incorporated
 *******************************************************************************
 """

from setuptools import setup, find_packages

#with open('readme.md') as readme_file:
 #   readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ['urllib3>=1.25.11', 'requests>=2.23.0', 'rdflib>=5.0.0']

setup_requirements = []

test_requirements = []

setup(
    author="Tommy Fang, William Ades, Curtis Galione, Andrew Parisi, Alex Ledger",
    author_email='info@cambridgesemantics.com',
    python_requires='>=3.5',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    description="PyAnzo is a library for interacting with Anzo",

    entry_points={
        'console_scripts': [],
    },
    install_requires=requirements,
#    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",

    keywords='pyanzo',
    name='pyanzo',
    packages=find_packages(include=['pyanzo', 'pyanzo.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='',
    version='3.3.12',
    zip_safe=False,
)
