#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = '0.0.74'

setuptools.setup(
    name="pywilight",
    version=version,
    author="Leonardo Figueiro",
    author_email="leoagfig@gmail.com",
    description="Python API for WiLight in Home Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/leofig-rj/pywilight',
    install_requires = ['requests', 'ifaddr'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
