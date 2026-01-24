"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

import codecs
import os.path
import pathlib

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="MultiPyVu",
    version=get_version("src/MultiPyVu/__version.py"),
    description="Control MultiVu using Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={"MultiPyVu": [
            "images/*.jpg",
            "images/*.png",
            "font/*.ttf",
            "scripts/*",
            "MultiVuDataFile/*.py",
            "logging_config.yaml"
            ]
        },
    python_requires=">=3.7",
    install_requires=[
        "pandas",
        "pywin32>=300; platform_system=='Windows'",
        "pillow",
        "pyyaml"
    ],
)
