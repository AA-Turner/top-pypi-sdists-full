#!/usr/bin/env python
from setuptools import setup

setup(
    name='pymorphy3-dicts-ru',
    version='2.4.417150.4580142',
    author='Danylo Halaiko',
    author_email='d9nich@pm.me',
    url='https://github.com/no-plagiarism/pymorphy3-dicts',

    description='Russian dictionaries for pymorphy2',
    long_description=open('README.rst').read(),

    license='MIT license',
    packages=['pymorphy3_dicts_ru'],
    package_data={'pymorphy3_dicts_ru': ['data/*']},
    zip_safe=False,
    entry_points={'pymorphy3_dicts': "ru = pymorphy3_dicts_ru"},

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],
)
