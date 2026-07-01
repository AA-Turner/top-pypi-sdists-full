# -*- coding: utf-8 -*-

# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='ummalqura',
      version='2.0.1',
      description='Python Hijri Ummalqura',
      long_description=long_description,
      url='https://github.com/borni-dhifi/ummalqura',
      author='Borni DHIFI',
      author_email='dhifi.borni@gmail.com',
      keywords=['ummalqura'],
      license='Waqef',
      packages=['ummalqura'],
      zip_safe=False)
