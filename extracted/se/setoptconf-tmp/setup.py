import os.path
import re

from setuptools import setup, find_packages


def get_description():
    readme = os.path.join(os.path.dirname(__file__), "README.rst")
    return open(readme, "r").read()


setup(
    name="setoptconf-tmp",
    version='0.3.1',
    author="Jason Simeone",
    author_email="jay@classless.net",
    maintainer="Carl Crowder",
    maintainer_email="git@carlcrowder.com",
    license="MIT",
    keywords=["settings", "options", "configuration", "config", "arguments"],
    description="A module for retrieving program settings from various"
    " sources in a consistant method.",
    long_description=get_description(),
    url="https://github.com/carlio/setoptconf-tmp",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(exclude=["test.*", "test"]),
    extras_require={"YAML": ["pyyaml"]},
)
