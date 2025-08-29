# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2024 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************

import setuptools


def find_packages():
    packages = setuptools.find_packages()
    packages = [package for package in packages if package.startswith("comet_ml")]
    return packages


setuptools.setup(
    name="comet_ml",
    packages=find_packages(),
    package_data={"comet_ml": ["schemas/*.json"]},
    url="https://www.comet.com",
    author="Comet ML Inc.",
    author_email="mail@comet.com",
    description="Supercharging Machine Learning",
    long_description=open("README.rst", encoding="utf-8").read(),
    long_description_content_type="text/x-rst",
    install_requires=[
        "dulwich>=0.20.6, !=0.20.33 ; python_version>='3.0'",  # https://github.com/jelmer/dulwich/issues/950
        "everett[ini]>=1.0.1,<3.2.0",
        "importlib-metadata; python_version < '3.8'",
        "jsonschema>=2.6.0,!=3.1.0",
        "psutil>=5.6.3",
        "python-box<7.0.0",
        "requests-toolbelt>=0.8.0",
        "requests>=2.18.4",
        "rich>=13.3.2 ; python_version>='3.7.0'",
        "semantic-version>=2.8.0",
        "sentry-sdk>=1.1.0",
        "setuptools ; python_version>='3.12'",
        "simplejson",
        "urllib3>=1.21.1",
        "wrapt>=1.11.2",
        "wurlitzer>=1.0.2",
    ],
    extras_require={"cpu_logging": []},
    entry_points={
        "console_scripts": [
            "comet = comet_ml.scripts.comet:main",
        ],
        "spacy_loggers": [
            "comet_ml.spacy.logger.v1 = comet_ml.integration.spacy:comet_logger_v1"
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    license="MIT",
    version="3.52.0",
)
