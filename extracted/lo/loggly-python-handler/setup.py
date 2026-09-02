#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="loggly-python-handler",
    version='1.0.1',
    description="Python logging handler that sends messages to Loggly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="loggly logging handler https",
    author="Loggly",
    author_email="support@loggly.com",
    url="https://github.com/loggly/loggly-python-handler/",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests-futures >= 1.0.0",
    ],
    include_package_data=True,
    platform='any',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers'
    ]
)
