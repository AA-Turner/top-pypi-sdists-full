#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


setup(
    name="pytest-eventlet",
    description="Applies eventlet monkey-patch as a pytest plugin.",
    version="1.0.0",
    author="Nameko Authors",
    url="https://github.com/nameko/pytest-eventlet",
    packages=find_packages(exclude=["test", "tests", "tests.*"]),
    install_requires=["eventlet"],
    extras_require={"dev": ["coverage", "pytest"]},
    dependency_links=[],
    entry_points={"pytest11": ["pytest_eventlet=pytest_eventlet.plugin"]},
    zip_safe=True,
    license="Apache License, Version 2.0",
)
