# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.0.4'


setup(
    name='excel-base',
    version=version,
    keywords='Excel Base',
    description='Excel Base',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    url='https://github.com/Brightcells/excel-base',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['excel_base'],
    py_modules=[],
    install_requires=['xlwt', 'screen', 'TimeConvert>=1.5.3'],

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
