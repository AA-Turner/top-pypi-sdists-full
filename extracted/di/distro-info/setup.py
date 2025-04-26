#!/usr/bin/python3

import os
import re

from setuptools import setup


PACKAGES = []
PY_MODULES = ["distro_info"]
SCRIPTS = ["debian-distro-info", "ubuntu-distro-info"]


def get_debian_version():
    """look what Debian version we have"""
    version = None
    changelog = "../debian/changelog"
    if os.path.exists(changelog):
        head = open(changelog, "rb").readline().decode("utf-8")
        match = re.compile(r".*\((.*)\).*").match(head)
        if match:
            version = match.group(1)
    return version


if __name__ == "__main__":
    setup(
        name="distro-info",
        version=get_debian_version(),
        py_modules=PY_MODULES,
        packages=PACKAGES,
        test_suite="distro_info_test",
        url='https://salsa.debian.org/debian/distro-info',
        author='Benjamin Drung',
        author_email='bdrung@debian.org',
    )
