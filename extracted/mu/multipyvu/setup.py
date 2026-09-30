"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

# name, version, description, license, dependencies, and readme are
# configured in pyproject.toml. Only the settings without a pyproject.toml
# equivalent (package discovery/layout and non-Python package data) live here.
setup(
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
)
