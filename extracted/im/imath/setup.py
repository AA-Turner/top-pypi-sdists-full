# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imath",
    version="0.0.2",
    author="innovata sambong",
    author_email="iinnovata@gmail.com",
    description='innovata-debug',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/innovata/imath",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"":"pkg"},
    packages=setuptools.find_packages(where="pkg"),
    python_requires=">=3.8",
)
