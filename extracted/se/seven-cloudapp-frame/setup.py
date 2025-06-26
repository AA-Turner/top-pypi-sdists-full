# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2020-08-21 14:59:50
@LastEditTime: 2022-09-30 10:45:22
@LastEditors: HuangJianYi
@Description: 
"""
from __future__ import print_function
from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="seven_cloudapp_frame",
    version="1.2.40",
    author="seven",
    author_email="tech@gao7.com",
    description="seven cloudapp frame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="http://gitlab.tdtech.gao7.com/TaoBaoCloud/seven_cloudapp_frame.git",
    packages=find_packages(),
    install_requires=[
        "seven-framework>=1.2.3",
        "seven-top >=1.0.28",
        "asq==1.3",
        "emoji==1.6.1",
        "xmltodict==0.12.0",
        "requests==2.32.3",
        "requests-pkcs12==1.25",
        "mmh3==3.0.0",
        "bce-python-sdk==0.8.61"
    ],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='~=3.4',
)