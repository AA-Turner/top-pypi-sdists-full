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

from setuptools import find_packages, setup

from common_setup import DEFAULT_CLASSIFIERS, DESCRIPTION_TEMPLATE, common_setup_kwargs, version

if "b" in version:
    msg = (
        "Major releases must not have a 'b' for beta in the version. "
        "Go back and make a release branch with tag, then update the version number."
    )
    raise RuntimeError(msg)

python_versions = ">= 3.7"

description = DESCRIPTION_TEMPLATE.format(
    package_name="datarobot",
    pypi_url_target="https://pypi.python.org/pypi/datarobot/",
    extra_desc="",
    python_versions=python_versions,
    pip_package_name="datarobot",
    docs_link="https://datarobot-public-api-client.readthedocs-hosted.com/en/latest-release/",
)

# `*_vendor*` is deliberately NOT excluded: pipelines went GA, so the stable
# wheel has to carry the vendored covalent / covalent-cloud runtime it needs.
# `make vendor` backfills __init__.py into the vendored namespace dirs so
# find_packages picks all of them up. `*_experimental*` stays excluded -- the
# rest of that tree is still pre-GA.
packages = find_packages(exclude=["tests*", "*_experimental*"])

common_setup_kwargs.update(
    name="datarobot",
    version=version,
    packages=packages,
    long_description=description,
    classifiers=DEFAULT_CLASSIFIERS,
)

# Honor MANIFEST.in so the vendored covalent / covalent-cloud trees (including
# the *.dist-info metadata that importlib.metadata.version("covalent") reads at
# runtime) ship inside the wheel. Passed directly to setup() because the typed
# value union on common_setup_kwargs doesn't allow bool. Mirrors setup_weekly.py.
setup(**common_setup_kwargs, include_package_data=True)
