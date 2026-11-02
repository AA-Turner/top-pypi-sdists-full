from setuptools import setup
from os import path
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    readme_description = f.read()
setup(
name = "safeIO",
packages = ["safeIO"],
version = "1.2",
license = "MIT",
description = "Safely make I/O operations to files in Python even from multiple threads... and more!",
author = "Anime no Sekai",
author_email = "niichannomail@gmail.com",
url = "https://github.com/Animenosekai/safeIO",
download_url = "https://github.com/Animenosekai/safeIO/archive/v1.2.tar.gz",
keywords = ['file', 'io', 'thread-safe', 'thread', 'management', 'file-management', 'animenosekai', 'threading'],
install_requires = None,
classifiers = ['Development Status :: 4 - Beta', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.3', 'Programming Language :: Python :: 3.4', 'Programming Language :: Python :: 3.5', 'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: 3.9'],
long_description = readme_description,
long_description_content_type = "text/markdown",
include_package_data=True,
)
