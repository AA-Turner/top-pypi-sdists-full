#!/usr/bin/env python

import os
import sys

VERSION = "v1.1"

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

license = """
MIT License
Copyright (c) 2022 Shawn Saenger
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyws66i",
    version=VERSION,
    description="Python API for talking to Soundavo's WS66i 6-zone amplifier using the telnet protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ssaenger/pyws66i",
    download_url="https://github.com/ssaenger/pyws66i/archive/{}.tar.gz".format(VERSION),
    author="Shawn Saenger",
    author_email="shawnsaenger@gmail.com",
    license="MIT",
    packages=["pyws66i"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Programming Language :: Python :: 3.8',
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
    zip_safe=True,
)
