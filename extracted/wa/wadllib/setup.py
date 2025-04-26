#!/usr/bin/env python

# Copyright 2008-2009 Canonical Ltd.  All rights reserved.
#
# This file is part of wadllib
#
# wadllib is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, version 3 of the License.
#
# wadllib is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with wadllib. If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages


# generic helpers primarily for the long_description
def generate(*docname_or_string):
    marker = '.. pypi description ends here'
    res = []
    for value in docname_or_string:
        if value.endswith('.rst'):
            with open(value) as f:
                value = f.read()
            idx = value.find(marker)
            if idx >= 0:
                value = value[:idx]
        res.append(value)
        if not value.endswith('\n'):
            res.append('')
    return '\n'.join(res)
# end generic helpers


install_requires = [
    'importlib-resources; python_version < "3.9"',
    'lazr.uri',
    ]

setup(
    name='wadllib',
    version='2.0.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        '': ['*.xml', '*.json', '*.rst'],
        },
    include_package_data=True,
    zip_safe=False,
    maintainer='LAZR Developers',
    maintainer_email='lazr-developers@lists.launchpad.net',
    description=open('README.rst').readline().strip(),
    long_description=generate(
        'src/wadllib/docs/main.rst',
        'NEWS.rst',
    ),
    long_description_content_type='text/x-rst',
    license='LGPL v3',
    python_requires=">=3.8",
    install_requires=install_requires,
    url='https://launchpad.net/wadllib',
    project_urls={
        "Source": "https://code.launchpad.net/wadllib",
        "Issue Tracker": "https://bugs.launchpad.net/wadllib",
        "Documentation": "https://wadllib.readthedocs.io/en/latest/",
    },
    download_url='https://launchpad.net/wadllib/+download',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",  # noqa: E501
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        ],
    extras_require={
        "docs": ['Sphinx'],
        "test": [
            'multipart',
        ]
    },
    test_suite='wadllib.tests',
    )
