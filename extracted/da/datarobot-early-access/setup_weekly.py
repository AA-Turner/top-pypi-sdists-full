#
# Copyright 2021-2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from datetime import datetime

from setuptools import find_packages, setup

from common_setup import DESCRIPTION_TEMPLATE, common_setup_kwargs, version

# We presently version the `datarobot` package with a version number that
# may contain either a 'b' or 'rc' in it. For the purposes of the
# `datarobot-early-access` package, we don't necessarily care that these
# exist, only that the package represents the codebase at a specific date.
# So remove the 'b' and 'rc'
version = version.replace("rc", "b")
version = version.split("b")[0]
version += datetime.today().strftime(".%Y.%m.%d")
# Add a build number based on the current time to ensure uniqueness for multiple releases in a day
version += datetime.today().strftime(".%H%M%S")

python_versions = ">= 3.7"

# for weekly releases, we do not support python 2 any longer; default classifiers otherwise
# this replaces common_setup.DEFAULT_CLASSIFIERS
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]

description = DESCRIPTION_TEMPLATE.format(
    package_name="datarobot_early_access",
    pypi_url_target="https://pypi.python.org/pypi/datarobot-early-access/",
    extra_desc=(
        'This package is the "early access" version of the client. **Do NOT use this package'
        " in production--you will expose yourself to risk of breaking changes and bugs.** For"
        " the most stable version, see the quarterly release on PyPI at"
        " https://pypi.org/project/datarobot/."
    ),
    python_versions=python_versions,
    pip_package_name="datarobot_early_access",
    docs_link="https://datarobot-public-api-client.readthedocs-hosted.com/en/early-access/",
)

packages = find_packages(exclude=["tests*"])

common_setup_kwargs.update(
    name="datarobot_early_access",
    version=version,
    project_urls={
        "Documentation": "https://datarobot-public-api-client.readthedocs-hosted.com/en/early-access/",
        "Changelog": "https://datarobot-public-api-client.readthedocs-hosted.com/en/early-access/CHANGES.html",
    },
    packages=packages,
    long_description=description,
    classifiers=classifiers,
)

setup(**common_setup_kwargs)
