#!/usr/bin/env python
# -*- coding: utf-8 -*-
from io import open as io_open
import os
from setuptools import setup, find_packages

src_dir = os.path.abspath(os.path.dirname(__file__))
README_rst = ''
fndoc = os.path.join(src_dir, 'README.rst')
with io_open(fndoc, mode='r', encoding='utf-8') as fd:
    README_rst = fd.read()
setup(
    name='tdqm',
    version='0.0.1',
    description='Alias for typos of tqdm',
    long_description=README_rst,
    long_description_content_type='text/x-rst',
    license='MPLv2.0',
    url='https://github.com/tqdm/tqdm',
    maintainer='tqdm developers',
    maintainer_email='python.tqdm@gmail.com',
    platforms=['any'],
    install_requires=['tqdm'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='progressbar progressmeter progress bar meter'
             ' rate eta console terminal time',
)
