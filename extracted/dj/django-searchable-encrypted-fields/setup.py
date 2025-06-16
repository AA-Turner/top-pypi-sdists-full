#!/usr/bin/env python

from setuptools import setup

setup(
    name="django-searchable-encrypted-fields",
    version="0.2.1",
    license="MIT",
    description="Django model fields encrypted using Pycryptodome AES-256 GCM.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Guy Willett",
    author_email="<guy@chamsoft.co>",
    maintainer="Guy Willett",
    maintainer_email="<guy@chamsoft.co>",
    url="https://gitlab.com/guywillett/django-searchable-encrypted-fields",
    packages=["encrypted_fields"],
    install_requires=["Django>=3.2", "pycryptodome>=3.7.0"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
    ],
)
