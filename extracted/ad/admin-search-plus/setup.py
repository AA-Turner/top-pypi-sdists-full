#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup

readme = open("README.md").read()

setup(
    name="admin-search-plus",
    version="0.3.1",
    author="David Graves",
    description="Mixin for Django's admin objects to enhance searching by limiting searchable fields",
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email="dgraves@gravitate-us.com",
    url="https://github.com/Lenders-Cooperative/django-admin-search-plus",
    download_url="https://github.com/Lenders-Cooperative/django-admin-search-plus/archive/v_03.tar.gz",
    packages=["admin_search_plus"],
    include_package_data=True,
    install_requires=[
        "Django>=2.2.9",
    ],
    keywords="django admin search",
    license="bsd-3-clause",
    platforms=["any"],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ]
)