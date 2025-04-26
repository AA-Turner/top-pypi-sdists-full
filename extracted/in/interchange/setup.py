#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from os import path

from setuptools import setup, find_packages


README_FILE = path.join(path.dirname(__file__), "README.md")


def get_readme():
    with open(README_FILE) as f:
        return f.read()


setup(
    name="interchange",
    version="2021.0.4",
    description="Data types and interchange formats",
    author="Nigel Small",
    author_email="technige@py2neo.org",
    url="https://github.com/py2neo-org/interchange",
    project_urls={
        "Bug Tracker": "https://github.com/py2neo-org/interchange/issues",
        "Documentation": "https://docs.py2neo.org/interchange/",
        "Source Code": "https://github.com/py2neo-org/interchange",
    },
    license="Apache License, Version 2.0",
    keywords=[],
    platforms=[],
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries"],
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("docs", "test", "test.*")),
    py_modules=[],
    install_requires=[
        "pytz",
        "six",
    ],
)
