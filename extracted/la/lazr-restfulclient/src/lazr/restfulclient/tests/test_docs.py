# Copyright 2012 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.json
#
# lazr.json is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.json is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.json.  If not, see <http://www.gnu.org/licenses/>.
"""Test harness for doctests."""

__all__ = [
    "load_tests",
]

import doctest
import importlib.util
import os
from pathlib import Path

import wsgi_intercept
from wsgi_intercept.httplib2_intercept import install, uninstall

# We avoid importing anything from lazr.restful into the module level,
# so that standalone_tests() can run without any support from
# lazr.restful.

DOCTEST_FLAGS = (
    doctest.ELLIPSIS
    | doctest.NORMALIZE_WHITESPACE
    | doctest.REPORT_NDIFF
    | doctest.IGNORE_EXCEPTION_DETAIL
)


def setUp(test):
    from lazr.restful.example.base.tests.test_integration import WSGILayer

    install()
    wsgi_intercept.add_wsgi_intercept(
        "cookbooks.dev", 80, WSGILayer.make_application
    )


def tearDown(test):
    from lazr.restful.example.base.interfaces import IFileManager
    from zope.component import getUtility

    uninstall()
    file_manager = getUtility(IFileManager)
    file_manager.files = {}
    file_manager.counter = 0


def find_doctests(suffix, ignore_suffix=None):
    """Find doctests matching a certain suffix."""
    doctest_files = []
    spec = importlib.util.find_spec("lazr.restfulclient")
    if spec and spec.submodule_search_locations:
        docs_path = Path(list(spec.submodule_search_locations)[0]) / "docs"
        if docs_path.is_dir():
            for path in sorted(docs_path.iterdir()):
                if ignore_suffix is not None and path.name.endswith(
                    ignore_suffix
                ):
                    continue
                if path.name.endswith(suffix):
                    doctest_files.append(os.path.abspath(str(path)))
    return doctest_files


def load_tests(loader, tests, pattern):
    """Load all the doctests."""
    from lazr.restful.example.base.tests.test_integration import WSGILayer

    restful_suite = doctest.DocFileSuite(
        *find_doctests(".rst", ignore_suffix=".standalone.rst"),
        module_relative=False,
        optionflags=DOCTEST_FLAGS,
        setUp=setUp,
        tearDown=tearDown,
    )
    restful_suite.layer = WSGILayer
    tests.addTest(restful_suite)
    tests.addTest(
        doctest.DocFileSuite(
            *find_doctests(".standalone.rst"),
            module_relative=False,
            optionflags=DOCTEST_FLAGS,
        )
    )
    return tests
