#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
from itertools import chain
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from distutils.command.build import build

from setuptools import Command
from setuptools import find_packages
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install_lib import install_lib
from setuptools.command.easy_install import easy_install


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


class BuildWithPTH(build):
    def run(self):
        build.run(self)
        path = join(dirname(__file__), 'src', 'pytest-cover.pth')
        dest = join(self.build_lib, basename(path))
        self.copy_file(path, dest)


class EasyInstallWithPTH(easy_install):
    def run(self):
        easy_install.run(self)
        path = join(dirname(__file__), 'src', 'pytest-cover.pth')
        dest = join(self.install_dir, basename(path))
        self.copy_file(path, dest)


class InstallLibWithPTH(install_lib):
    def run(self):
        install_lib.run(self)
        path = join(dirname(__file__), 'src', 'pytest-cover.pth')
        dest = join(self.install_dir, basename(path))
        self.copy_file(path, dest)
        self.outputs = [dest]

    def get_outputs(self):
        return chain(install_lib.get_outputs(self), self.outputs)


class DevelopWithPTH(develop):
    def run(self):
        develop.run(self)
        path = join(dirname(__file__), 'src', 'pytest-cover.pth')
        dest = join(self.install_dir, basename(path))
        self.copy_file(path, dest)


class GeneratePTH(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        with open(join(dirname(__file__), 'src', 'pytest-cover.pth'), 'w') as fh:
            with open(join(dirname(__file__), 'src', 'pytest-cover.embed')) as sh:
                fh.write(
                    'import os, sys;'
                    'exec(%r)' % sh.read().replace('    ', ' ')
                )

setup(
    name='pytest-cover',
    version='3.0.0',
    license='MIT',
    description='Pytest plugin for measuring coverage. Forked from `pytest-cov`.',
    long_description='%s\n%s' % (read('README.rst'), re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
    author='Marc Schlaich',
    author_email='marc.schlaich@gmail.com',
    maintainer='Ionel Cristian Mărieș',
    maintainer_email='contact@ionelmc.ro',
    url='https://github.com/ionelmc/pytest-cover',
    packages=[],
    py_modules=['bogus'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
        'Topic :: Software Development :: Testing'
    ],
    keywords=[
        'cover', 'coverage', 'pytest', 'py.test', 'distributed', 'parallel',
    ],
    install_requires=[
        'pytest-cov>=2.0',
    ],
)
