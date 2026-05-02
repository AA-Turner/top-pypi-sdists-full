"""Module for package and distribution."""
from setuptools import setup

exec(open("src/ga4gh/vrsatile/pydantic/version.py").read())
setup(version=__version__)  # noqa: F821
