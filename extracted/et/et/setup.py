# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

package_name = "et"

setup(
    author = "See https://github.com/reece/et",
    author_email = "reecehart@gmail.com",
    description = open("doc/short-description.txt").read().replace("\n", " "),
    long_description = open("README.md").read(),
    name = package_name,
    url = "https://github.com/reece/et",
    use_scm_version = True,
    zip_safe = True,

    packages = find_packages(),

    install_requires = [
    ],

    setup_requires = [
        "pytest-runner",
        # 1.11 is latest that works here; https://github.com/pypa/setuptools_scm/issues/134
        "setuptools_scm==1.11",
        "wheel",
    ],

    tests_require = [
        "pytest",
        "pytest-cov",
        "tox",
    ],
)
