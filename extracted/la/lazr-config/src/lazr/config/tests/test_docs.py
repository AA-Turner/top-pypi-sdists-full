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

__all__ = []

import doctest
import importlib.util
from pathlib import Path

DOCTEST_FLAGS = (
    doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF
)


def load_tests(loader, tests, pattern):
    """Load the doc tests (docs/*, if any exist)."""
    doctest_files = []
    spec = importlib.util.find_spec("lazr.config")
    if spec and spec.submodule_search_locations:
        docs_path = Path(list(spec.submodule_search_locations)[0]) / "docs"
        if docs_path.is_dir():
            for path in docs_path.iterdir():
                if path.name.endswith(".rst"):
                    doctest_files.append(str(path.resolve()))
    tests.addTest(
        doctest.DocFileSuite(
            *doctest_files,
            module_relative=False,
            optionflags=DOCTEST_FLAGS,
            encoding="UTF-8",
        )
    )
    return tests
