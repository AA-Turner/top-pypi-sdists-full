#!/usr/bin/env python
# Installs interruptingcow.

import os, sys
from distutils.core import setup

def long_description():
    """Get the long description from the README"""
    return open(os.path.join(sys.path[0], 'README.rst')).read()

setup(
    author='Erik van Zijst',
    author_email='erik.van.zijst@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Debuggers',
        'Topic :: System :: Benchmark',
        'Topic :: System :: Monitoring',
        'Topic :: Utilities',
    ],
    description='A watchdog that interrupts long running code.',
    keywords='debug watchdog timer interrupt',
    license='MIT',
    long_description=long_description(),
    name='interruptingcow',
    packages=['interruptingcow'],
    url='https://bitbucket.org/evzijst/interruptingcow',
    version='0.8',
)
