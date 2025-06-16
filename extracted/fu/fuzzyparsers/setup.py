#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#  Copyright (C) Joel B. Mohler <joel@kiwistrawberry.us>
#
#  Distributed under the terms of The MIT License
###########################################################

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='fuzzyparsers',
    version='0.9.5.1',  # also update in fuzzyparsers/__init__.py
    description='A collection of free-form input parsers (with special focus on dates)',
    license='MIT',
    author='Joel B. Mohler',
    author_email='joel@kiwistrawberry.us',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/jbmohler/fuzzyparsers',
    packages=['fuzzyparsers'],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"])
