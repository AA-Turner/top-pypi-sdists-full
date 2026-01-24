#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst", encoding="utf8") as readme_file:
    readme = readme_file.read()

install_requirements = open("requirements.txt").readlines()

setup(
    author="Thoughtful",
    author_email="support@thoughtfulautomation.com",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="Thoughtful OCR Package",
    long_description=readme,
    include_package_data=True,
    install_requires=install_requirements,
    keywords="thoughtful-ocr, t-ocr, t_ocr",
    name="t_ocr",
    packages=find_packages(include=["t_ocr", "t_ocr.*"]),
    test_suite="tests",
    url="https://www.thoughtful.ai/",
    version="1.5.6",
    zip_safe=False,
)
