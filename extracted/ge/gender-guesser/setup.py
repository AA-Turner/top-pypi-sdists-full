#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.test import test as TestCommand
from io import open
import sys


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

setup(
    name='gender-guesser',
    version='0.4.0',
    author='Israel Saeta Pérez',
    author_email='israel@lead-ratings.com',
    packages=['gender_guesser'],
    package_dir={'gender_guesser': 'gender_guesser'},
    package_data={'gender_guesser': ['data/*.txt']},
    test_suite='test',
    tests_require=['tox'],
    cmdclass={'test': Tox},
    url='https://github.com/lead-ratings/gender-guesser',
    license='GPLv3',
    description='Get the gender from first name.',
    long_description=open('README.rst', encoding='utf-8').read(),
)
