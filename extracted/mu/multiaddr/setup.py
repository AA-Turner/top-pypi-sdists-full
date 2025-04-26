#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()


with open('HISTORY.rst') as history_file:
    history = history_file.read()


version = '0.0.9'

setup(
    name='multiaddr',
    version=version,
    description="Python implementation of jbenet's multiaddr",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/x-rst",
    author="Steven Buss",
    author_email='steven.buss@gmail.com',
    url='https://github.com/multiformats/py-multiaddr',
    download_url=(
        'https://github.com/multiformats/py-multiaddr/tarball/%s' % version),
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_dir={'multiaddr': 'multiaddr'},
    include_package_data=True,
    license='MIT License',
    zip_safe=False,
    keywords='multiaddr',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
        'varint',
        'six',
        'base58',
        'netaddr',
    ],
    test_suite='tests',
    tests_require=[
        'pytest',
    ],
)
