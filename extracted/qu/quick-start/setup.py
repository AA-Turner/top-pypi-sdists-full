import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

NAME = "quick-start"
DESCRIPTION = "My short description for my project."
URL = "http://github.com/andreztz/quick-start"
EMAIL = "andreztz@gmail.com"
AUTHOR = "André Pereira dos Santos"
KEYWORDS = "quick start project"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = "0.0.dev10"


def readme():
    with open(os.path.join(here, "README.md")) as f:
        return f.read()


def required():
    with open(os.path.join(here, "requirements.txt")) as f:
        return f.read().splitlines()


package = {
    "name": NAME,
    "version": VERSION,
    "description": DESCRIPTION,
    "long_description": readme(),
    "long_description_content_type": "text/markdown",
    "keywords": KEYWORDS,
    "author": AUTHOR,
    "author_email": EMAIL,
    "url": URL,
    "license": "MIT",
    "packages": find_packages(),
    "install_requires": required(),
    "entry_points": {"console_scripts": ["pyinit=quickstart.__main__:main"]},
    "python_requires": REQUIRES_PYTHON,
    "scripts": [os.path.join(here, "quickstart/quickstart_installer")],
    "classifiers": [
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    "data_files": [("", ["data/sample.zip"])],
}


setup(**package)
