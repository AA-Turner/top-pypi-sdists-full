#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright 2020, Nigel Small
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


from os.path import dirname, join as path_join
from setuptools import setup, find_packages


from english import (
    __author__,
    __email__,
    __license__,
    __package__,
    __version__,
)


source_url = "https://github.com/technige/english"


with open(path_join(dirname(__file__), "README.rst")) as f:
    README = f.read()


packages = find_packages(exclude=("docs", "test"))
package_metadata = {
    "name": __package__,
    "version": __version__,
    "description": "English language utility library for Python",
    "long_description": README,
    "author": __author__,
    "author_email": __email__,
    "url": source_url,
    "project_urls": {
        "Bug Tracker": "{}/issues".format(source_url),
        "Source Code": source_url,
    },
    "entry_points": {
        "console_scripts": [
        ],
    },
    "packages": packages,
    "py_modules": [
    ],
    "install_requires": [
        "six",
    ],
    "extras_require": {
    },
    "license": __license__,
    "classifiers": [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
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
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Linguistic",
    ],
}

setup(**package_metadata)
