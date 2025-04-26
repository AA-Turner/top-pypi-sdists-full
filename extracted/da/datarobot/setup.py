#
# Copyright 2021 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from setuptools import find_packages, setup

from common_setup import common_setup_kwargs, DEFAULT_CLASSIFIERS, DESCRIPTION_TEMPLATE, version

python_versions = ">= 3.7"

description = DESCRIPTION_TEMPLATE.format(
    package_name="datarobot",
    pypi_url_target="https://pypi.python.org/pypi/datarobot/",
    extra_desc="",
    python_versions=python_versions,
    pip_package_name="datarobot",
    docs_link="https://datarobot-public-api-client.readthedocs-hosted.com",
)

packages = find_packages(exclude=["tests"])

common_setup_kwargs.update(
    name="datarobot",
    version=version,
    packages=packages,
    long_description=description,
    classifiers=DEFAULT_CLASSIFIERS,
)

setup(**common_setup_kwargs)
