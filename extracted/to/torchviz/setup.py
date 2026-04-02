#!/usr/bin/env python
import os
import shutil
import sys
from setuptools import setup, find_packages

VERSION = '0.0.3'

# Read in README.md for our long_description
cwd = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cwd, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup_info = dict(
    # Metadata
    name='torchviz',
    version=VERSION,
    author='Sergey Zagoruyko',
    author_email='sergey.zagoruyko@enpc.fr',
    url='https://github.com/pytorch/pytorchviz',
    description='A small package to create visualizations of PyTorch execution graphs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='BSD',

    # Package info
    packages=find_packages(exclude=('test',)),

    zip_safe=True,

    install_requires=[
        'torch',
        'graphviz'
    ]
)

setup(**setup_info)
