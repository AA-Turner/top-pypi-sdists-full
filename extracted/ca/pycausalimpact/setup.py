# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# We used setup.py from the requests library as reference:
# https://github.com/requests/requests/blob/master/setup.py


from __future__ import absolute_import

import os
import re
import sys

from codecs import open

from setuptools import setup
from setuptools.command.test import test as TestCommand


here = os.path.abspath(os.path.dirname(__file__))

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

py_version = sys.version_info
if py_version.major == 2 and py_version.minor == 7:
    install_requires = [
        'numpy==1.16.6',
        'scipy==1.2.2',
        'pandas==0.24.2',
        'statsmodels==0.9.0',
        'matplotlib==2.2.4',
        'jinja2>=2.10'
    ]

    tests_require = [
        'pytest==4.6.5',
        'pytest-cov',
        'mock==3.0.5',
        'tox'
    ]

else:
    install_requires = [
        'numpy',
        'scipy',
        'statsmodels>=0.11.0',
        'matplotlib>=2.2.3',
        'jinja2>=2.10'
    ]

    tests_require = [
        'pytest',
        'pytest-cov',
        'mock',
        'tox'
    ]

setup_requires = [
    'flake8',
    'isort',
    'pytest-runner'
]

extras_require = {
    'docs': [
        'ipython',
        'jupyter'
    ],
    'testing': tests_require
}

packages = ['causalimpact']

_version = {}
_version_path = os.path.join(here, 'causalimpact', '__version__.py')
with open(_version_path, 'r', 'utf-8') as f:
    exec(f.read(), _version)

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()


class PyTest(TestCommand):

    user_options = [
        ('coverage=', None, 'Runs coverage report.'),
        ('html=', None, 'Saves result to html report.'),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []
        self.coverage = False
        self.html = False

    def finalize_options(self):
        TestCommand.finalize_options(self)

        if self.coverage:
            self.pytest_args.extend(['--cov-config', '.coveragerc'])
            self.pytest_args.extend([
                '--cov', 'causalimpact', '--cov-report', 'term-missing'])

        if self.html:
            self.pytest_args.extend(['--cov-report', 'html'])

        self.pytest_args.extend(['-p', 'no:warnings'])

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='pycausalimpact',
    version=_version['__version__'],
    author='Willian Fuks',
    author_email='willian.fuks@gmail.com',
    url='https://github.com/dafiti/causalimpact',
    description= "Python version of Google's Causal Impact model",
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=packages,
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    extras_require=extras_require,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering',
    ],
    cmdclass={'test': PyTest},
    test_suite='tests'
)
