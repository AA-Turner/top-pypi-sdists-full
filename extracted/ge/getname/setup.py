#!/usr/bin/env python
#  -*- coding: utf-8 -*-


from setuptools import setup

import getname


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    with open('README.md') as f:
        long_description = f.read()


setup(
    name='getname',
    version=getname.__version__,
    description='Get popular cat/dog/superhero/supervillain names',
    long_description=long_description,
    url='http://github.com/lord63/getname',
    author='lord63',
    author_email='lord63.j@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='name cat dog superhero supervillain',
    packages=['getname'],
    install_requires=[
        'click>=4.0',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'getname=getname.cli:cli']
    }
)
