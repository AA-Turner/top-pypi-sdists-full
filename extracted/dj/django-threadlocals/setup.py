#!/usr/bin/env python
# User: Troy Evans
# Date: 1/24/13
# Time: 8:54 PM
#
# Copyright 2015, Nutrislice Inc.  All rights reserved.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-threadlocals",
    packages=setuptools.find_packages(),
    version="0.10",
    author="Ben Roberts",
    author_email="ben@nutrislice.com",
    description="Contains utils for storing and retreiving values from threadlocals, and middleware for placing the current Django request in threadlocal storage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/nebstrebor/django-threadlocals',
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
    ],
)