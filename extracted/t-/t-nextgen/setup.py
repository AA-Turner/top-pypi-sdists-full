#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

install_requirements = open("requirements.txt").readlines()

setup(
    author="Thoughtful",
    author_email="support@thoughtful.ai",
    python_requires=">=3.9",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    description="A Python library providing seamless methods to interact "
    "with NextGen application, enabling automation and integration for enhanced workflow efficiency",
    long_description=readme,
    keywords="t_nextgen",
    name="t_nextgen",
    packages=find_packages(include=["t_nextgen", "t_nextgen.*"]),
    test_suite="tests",
    url="https://www.thoughtful.ai/",
    version="0.4.15",
    zip_safe=False,
    install_requires=install_requirements,
)
