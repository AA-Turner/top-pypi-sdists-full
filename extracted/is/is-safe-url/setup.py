#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()


setup(
    name="is_safe_url",
    version="1.0",
    description="Django's is_safe_url() bundled as a standalone package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Markus Holtermann, Django Software Foundation and individual contributors",
    author_email="info@markusholtermann.eu",
    url="https://gitlab.com/MarkusH/is_safe_url",
    py_modules=["is_safe_url"],
    include_package_data=True,
    license="BSD",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
