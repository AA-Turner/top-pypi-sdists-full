#!/usr/bin/env python

# Copyright 2009-2018 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.restfulclient
#
# lazr.restfulclient is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.restfulclient is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.restfulclient.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import find_packages, setup


# generic helpers primarily for the long_description
def generate(*docname_or_string):
    marker = ".. pypi description ends here"
    res = []
    for value in docname_or_string:
        if value.endswith(".rst"):
            with open(value) as f:
                value = f.read()
            idx = value.find(marker)
            if idx >= 0:
                value = value[:idx]
        res.append(value)
        if not value.endswith("\n"):
            res.append("")
    return "\n".join(res)


# end generic helpers


tests_require = [
    "fixtures>=1.3.0",
    "lazr.authentication",
    "lazr.restful>=0.11.0",
    'mock; python_version < "3"',
    "oauth",
    "testtools",
    "wsgi_intercept",
    "zope.testrunner",
]

setup(
    name="lazr.restfulclient",
    version="0.14.6",
    namespace_packages=["lazr"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    maintainer="LAZR Developers",
    maintainer_email="lazr-developers@lists.launchpad.net",
    description=open("README.rst").readline().strip(),
    long_description=generate(
        "src/lazr/restfulclient/docs/index.rst", "NEWS.rst"
    ),
    license="LGPL v3",
    install_requires=[
        "distro",
        'httplib2; python_version < "3"',
        'httplib2>=0.7.7; python_version >= "3"',
        'importlib-metadata; python_version < "3.8"',
        "oauthlib",
        "setuptools",
        "six",
        "wadllib>=1.1.4",
    ],
    url="https://launchpad.net/lazr.restfulclient",
    project_urls={
        "Source": "https://code.launchpad.net/lazr.restfulclient",
        "Issue Tracker": "https://bugs.launchpad.net/lazr.restfulclient",
        "Documentation": "https://lazrrestfulclient.readthedocs.io/en/latest/",
    },
    download_url="https://launchpad.net/lazr.restfulclient/+download",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",  # noqa: E501
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    tests_require=tests_require,
    extras_require=dict(
        docs=["Sphinx"],
        test=tests_require,
    ),
    test_suite="lazr.restfulclient.tests",
)
