#!/usr/bin/env python
import os
import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    long_description = readme.read()
with open(os.path.join(os.path.dirname(__file__), 'pyhdfs.py')) as py:
    version = re.search(r"__version__ = '(.+?)'", py.read()).group(1)

setup(
    name="PythonWebHDFS",
    version=version,
    description="Customized Python Web HDFS client",
    long_description=long_description,
    author="SparkSnail",
    author_email="noreplay@gmail.com",
    license="MIT License",
    py_modules=['pyhdfs'],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Filesystems",
    ],
    install_requires=[
        'requests',
        'simplejson',
    ],
    cmdclass={'test': PyTest},
    package_data={
        '': ['*.rst'],
    },
)
