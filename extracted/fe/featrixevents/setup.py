#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""Setup script for featrixevents package."""

from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent


def get_version():
    init_file = this_directory / "__init__.py"
    if init_file.exists():
        for line in init_file.read_text().splitlines():
            if line.startswith("__version__"):
                return line.split('"')[1]
    return "0.1.0"


setup(
    name="featrixevents",
    version=get_version(),
    author="Featrix",
    author_email="support@featrix.com",
    description="Post events to the Featrix platform.",
    long_description="Post events to the Featrix platform. See https://docs.featrix.com",
    long_description_content_type="text/plain",
    url="https://github.com/Featrix/sphere",
    packages=["featrixevents"],
    package_dir={"featrixevents": "."},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.20.0",
    ],
    zip_safe=False,
)
