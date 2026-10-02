#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import (
    absolute_import,
    division,
    generators,
    nested_scopes,
    print_function,
    unicode_literals,
    with_statement,
)

import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines() if x.strip()]

setup(
    name="django-middleware-global-request",
    version="0.3.6",
    description="Django middleware that keep request instance for every thread.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="rRR0VrFP",
    maintainer="rRR0VrFP",
    license="MIT",
    license_files=("LICENSE",),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["django extensions", "django middleware global request"],
    packages=find_packages(
        ".",
        exclude=[
            "django_middleware_global_request_example",
            "django_middleware_global_request_example.migrations",
            "django_middleware_global_request_example.management",
            "django_middleware_global_request_example.management.commands",
            "django_middleware_global_request_demo",
        ],
    ),
    requires=requires,
    install_requires=requires,
    zip_safe=False,
    include_package_data=True,
)
