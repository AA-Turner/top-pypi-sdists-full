"""

spotlib :  Copyright 2018-2020, Blake Huber

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

see: https://www.gnu.org/licenses/#GPL

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
contained in the program LICENSE file.

"""

import os
import sys
import platform
import subprocess
from shutil import which
from setuptools import setup, find_packages
import getpass
from codecs import open
import spotlib


requires = [
    'boto3>=1.12.1',
    'libtools>=0.3.3',
    'pytz>=2018.3'
]


_project = 'spotlib'
_root = os.path.abspath(os.path.dirname(__file__))


def _root_user():
    """
    Checks localhost root or sudo access.  Returns bool
    """
    if os.geteuid() == 0:
        return True
    elif subprocess.getoutput('echo $EUID') == '0':
        return True
    return False


def _user():
    """Returns username of caller"""
    return getpass.getuser()


def _set_pythonpath():
    """
    Temporarily reset PYTHONPATH to prevent home dir = python module home
    """
    os.environ['PYTHONPATH'] = '/'


def module_dir():
    """Filsystem location of Python3 modules"""
    bin_path = which('python3.6') or which('python3.7')
    bin = bin_path.split('/')[-1]
    if 'local' in bin:
        return '/usr/local/lib/' + bin + '/site-packages'
    return '/usr/lib/' + bin + '/site-packages'


def os_parityPath(path):
    """
    Converts unix paths to correct windows equivalents.
    Unix native paths remain unchanged (no effect)
    """
    path = os.path.normpath(os.path.expanduser(path))
    if path.startswith('\\'):
        return 'C:' + path
    return path


def preclean(dst):
    if os.path.exists(dst):
        os.remove(dst)
    return True


def read(fname):
    basedir = os.path.dirname(sys.argv[0])
    return open(os.path.join(basedir, fname)).read()


setup(
    name=_project,
    version=spotlib.__version__,
    description='Library for retrieving Amazon EC2 Spot Price Data',
    long_description=read('DESCRIPTION.rst'),
    url='https://github.com/fstab50/spotlib',
    author=spotlib.__author__,
    author_email=spotlib.__email__,
    license='GPL-3.0',
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
    ],
    keywords='Amazon AWS EC2 spot prices lambda reports cost management',
    packages=find_packages(exclude=['assets', 'docs', 'reports', 'scripts', 'tests']),
    install_requires=requires,
    python_requires='>=3.6, <4',
    entry_points={
        'console_scripts': [
            'spotcli=spotlib.cli:init'
        ]
    },
    zip_safe=False
)
