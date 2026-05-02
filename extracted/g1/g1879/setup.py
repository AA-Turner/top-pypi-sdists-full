#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

# with open("README.md", "r", encoding='utf-8') as fh:
#     long_description = fh.read()

setup(
    name="g1879",
    version="0.5.2",
    author="g1879",
    author_email="g1879@qq.com",
    description="A personal toolkit.",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    license="MIT",
    keywords="g1879",
    url="https://gitee.com/g1879/g1879",
    include_package_data=True,
    packages=find_packages(),
    # install_requires=[
    #     "selenium",
    #     "lxml",
    #     "tldextract",
    #     "requests"
    # ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.8'
)
