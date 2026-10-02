# Copyright (C) 2010-2023 by the Free Software Foundation, Inc.
#
# This file is part of mailman.client.
#
# mailman.client is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# mailman.client is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with mailman.client.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import find_packages, setup

from setup_helpers import get_version, require_python

require_python(0x30600f0)
__version__ = get_version('src/mailmanclient/constants.py')


def readme():
    with open('README.rst') as fd:
        return fd.read()


setup(
    name='mailmanclient',
    version=__version__,
    packages=find_packages('src'),
    description='mailmanclient -- Python bindings for Mailman REST API',
    long_description=readme(),
    long_description_content_type='text/x-rst',
    package_dir={'': 'src'},
    include_package_data=True,
    maintainer='Barry Warsaw',
    maintainer_email='barry@list.org',
    license='LGPLv3',
    url='http://www.list.org/',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)', # noqa
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP ',
    ],
    install_requires=[
        'requests',
        'typing_extensions;python_version<"3.8"',
        ],
    extras_require={
        'testing': [
            'pytest',
            'pytest-services',
            'mailman>=3.3.1',
            'falcon>1.4.1',
            'httpx',
            ],
        'docs': [
            'sphinx',
            'sphinx-rtd-theme',
            'sphinx-issues',
            'pydoctor',
        ],
        'lint': [
            'flake8>3.0',
            'flake8-bugbear',
           ]
        },
    )
