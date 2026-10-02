# coding:utf-8
import sys

from setuptools import setup, find_packages
from volcengine import VERSION

install_requires = [
    "requests>=2.25.1",
    "retry>=0.9.2",
    "pytz>=2020.5",
    "pycryptodome>=3.9.9",
    "protobuf>=3.18.3",
    "google>=3.0.0",
    "six>=1.0",
]

setup(
    name="volcengine-compat",
    version=VERSION,
    keywords=("pip", "volcengine", "volc-sdk-python"),
    description="Be Compatible with the Volcengine SDK for Python, The version of package dependencies has been modified. like pycryptodome, pytz.",
    license="MIT License",

    url="https://github.com/yaoice/volc-sdk-python",
    author="Ice Yao",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=install_requires
)
