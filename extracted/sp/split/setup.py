#!/usr/bin/env python

from distutils.core import setup

LONG_DESCRIPTION = open("README").read()
LICENSE = open("LICENSE").read()

setup(name='split',
   version='0.4',
   description='Functions to split or partition sequences.',
   long_description=LONG_DESCRIPTION,
   author='Sergey Astanin',
   author_email='s.astanin@gmail.com',
   url='https://bitbucket.org/astanin/python-split',
   license=LICENSE,
   classifiers= [ "Development Status :: 4 - Beta",
                  "Intended Audience :: Developers",
                  "License :: OSI Approved :: MIT License",
                  "Operating System :: OS Independent",
                  "Programming Language :: Python :: 2",
                  "Programming Language :: Python :: 3",
                  "Topic :: Software Development :: Libraries" ],
   py_modules = ['split'])
