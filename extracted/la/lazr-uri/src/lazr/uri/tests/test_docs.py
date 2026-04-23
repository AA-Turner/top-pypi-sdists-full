# Copyright 2009 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.uri
#
# lazr.uri is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.uri is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.uri.  If not, see <http://www.gnu.org/licenses/>.

"""Test harness for doctests."""


__all__ = [
    "load_tests",
]

import doctest
import importlib.util
from pathlib import Path

DOCTEST_FLAGS = (
    doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF
)


def find_doctests(suffix):
    """Find doctests matching a certain suffix."""
    doctest_files = []
    spec = importlib.util.find_spec("lazr.uri")
    if not spec or not spec.submodule_search_locations:
        return doctest_files
    docs_path = Path(list(spec.submodule_search_locations)[0]) / "docs"
    for path in docs_path.iterdir():
        if path.name.endswith(suffix):
            doctest_files.append(str(path.resolve()))
    return doctest_files


def load_tests(loader, tests, pattern):
    """Load all the doctests."""
    tests.addTest(
        doctest.DocFileSuite(
            *find_doctests(".rst"),
            module_relative=False,
            optionflags=DOCTEST_FLAGS,
        )
    )
    return tests
