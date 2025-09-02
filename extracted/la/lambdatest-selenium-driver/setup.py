from setuptools import setup, find_packages
from os import path

cwd = path.abspath(path.dirname(__file__))
with open(path.join(cwd, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="lambdatest-selenium-driver",
    version="1.0.5",
    author="LambdaTest <keys@lambdatest.com>",
    description="Python Selenium SDK for testing with Smart UI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LambdaTest/lambdatest-python-sdk",
    keywords="lambdatest python selenium sdk",
    packages=find_packages(),
    license="MIT",
    install_requires=[
        "selenium>=3",
        "lambdatest-sdk-utils"
    ],
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
    ],
)
