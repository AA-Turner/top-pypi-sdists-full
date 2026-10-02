# Copyright 2023 Agnostiq Inc.

import site
import sys

from setuptools import find_packages, setup

site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

with open("VERSION") as f:
    version = f.read().strip()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup_info = {
    "name": "covalent_cloud",
    "packages": find_packages(exclude=["tests"]),
    "version": version,
    "maintainer": "Agnostiq",
    "url": "https://github.com/datarobot/covalent-cloud-sdk",
    "download_url": f"https://github.com/datarobot/covalent-cloud-sdk/archive/v{version}.tar.gz",
    "license": "Apache License 2.0",
    "author": "Agnostiq",
    "author_email": "support@agnostiq.ai",
    "description": "Covalent Cloud SDK",
    "long_description": open("README.md").read(),
    "long_description_content_type": "text/markdown",
    "include_package_data": True,
    "install_requires": required,
    "python_requires": ">=3.10",
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Adaptive Technologies",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development",
        "Topic :: System :: Distributed Computing",
    ],
}

if __name__ == "__main__":
    setup(**setup_info)
