#!/usr/bin/env python
import os
import sys

from setuptools import setup, find_packages

version = '0.3'

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'v%s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

with open('README.rst') as readme_file:
    readme = readme_file.read()

if sys.argv[-1] == 'readme':
    print(readme)
    sys.exit()

requirements = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil", "requests"]

test_requirements = ["mock", "urllib3_mock"]

setup(
    name='phaxio',
    version=version,
    packages=find_packages(),
    test_suite='tests',
    install_requires=requirements,
    tests_require=test_requirements,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
    ],

    # metadata for upload to PyPI
    author='Aryeh Polsky',
    author_email='anpolsky@gmail.com',
    description='Python client for Phaxio v2 API',
    long_description=readme,
    license='MIT License',
    keywords='python phaxio fax api',
    url='https://github.com/anpolsky/phaxio-python',
)
