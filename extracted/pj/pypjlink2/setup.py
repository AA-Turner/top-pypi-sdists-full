#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

from pypjlink import version

with open('README.md', 'r') as fh:
    long_description = fh.read()

print(long_description)
setup(
    name='pypjlink2',
    version=version,
    author=('Peter Ward <peteraward@gmail.com>, '
            'Gaetano Guerriero <gaetano.guerriero@spacespa.it>, '
            'Benoit Louy <pypjlink@mm.st>'),
    author_email='pypjlink@mm.st',
    url='https://github.com/benoitlouy/pypjlink',
    description='PJLink is a standard for controlling data projectors.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Topic :: Multimedia :: Video :: Display',
        'Topic :: Utilities',
    ],

    install_requires=['appdirs'],
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'pjlink = pypjlink.cli:main',
        ],
    },
    test_suite='tests',
)
