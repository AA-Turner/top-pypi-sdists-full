#!/usr/bin/env python3

import setuptools
import sys
from src.ibapi import get_version_string

if sys.version_info < (3,1):
    sys.exit("Only Python 3.1 and greater is supported")


setuptools.setup(
    name='ibapi',
    version=get_version_string(),

    description='Official Interactive Brokers API',

    # Allow UTF-8 characters in README with encoding argument.
    long_description=open('README.rst', encoding="utf-8").read(),
    long_description_content_type='text/x-rst',
    keywords=['ib', 'interactive brokers', 'ibpy', 'tws'],

    author='IBG LLC',
    author_email='dnastase@interactivebrokers.com',
    url='https://interactivebrokers.github.io/tws-api',
    license='IB API Non-Commercial License or the IB API Commercial License',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},

    # pip 9.0+ will inspect this field when installing to help users install a
    # compatible version of the library for their Python version.
    python_requires='>=3.1',

    # There are some peculiarities on how to include package data for source
    # distributions using setuptools. You also need to add entries for package
    # data to MANIFEST.in.
    # See https://stackoverflow.com/questions/7522250/
    include_package_data=True,

    # This is a trick to avoid duplicating dependencies between both setup.py and
    # requirements.txt.
    # requirements.txt must be included in MANIFEST.in for this to work.
    # It does not work for all types of dependencies (e.g. VCS dependencies).
    # For VCS dependencies, use pip >= 19 and the PEP 508 syntax.
    #   Example: 'requests @ git+https://github.com/requests/requests.git@branch_or_tag'
    #   See: https://github.com/pypa/pip/issues/6162
    install_requires=open('requirements.txt').readlines(),
    zip_safe=False,

    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

)
