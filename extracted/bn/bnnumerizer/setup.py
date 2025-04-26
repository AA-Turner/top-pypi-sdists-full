
#-*- coding: utf-8 -*-
"""
@author:mnansary
"""
#------------------------------------------------------------
from __future__ import print_function
#------------------------------------------------------------
from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='bnnumerizer',
  version='0.0.2',
  description='Bangla Number text to String Converter',
  long_description=open('README.md',encoding='utf-8').read() + '\n\n' + open('CHANGELOG.txt',encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/banglakit/number-to-bengali-word',  
  author='Aniruddha Adhikary,Mahir Labib Chowdhury',
  author_email='',
  license='MIT', 
  classifiers=classifiers,
  keywords=['bangla','number','word numerizer'], 
  packages=find_packages(),
  install_requires=[''] 
)