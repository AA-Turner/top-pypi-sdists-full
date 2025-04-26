import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="python_version",
    version="0.0.2",
    author="Aaron Halfaker",
    author_email="aaron.halfaker@gmail.com",
    description="Provides a simple utility for checking the python version.",
    url="https://gitlab.com/halfak/python_version",
    license="MIT License",  # noqa
    packages=find_packages(),
    include_package_data=True,
    long_description=read("README.md"),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python",
    ],
)
