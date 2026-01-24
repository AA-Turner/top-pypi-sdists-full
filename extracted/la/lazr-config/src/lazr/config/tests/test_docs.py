# Copyright 2009-2021 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.config.
#
# lazr.config is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.config is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.config.  If not, see <http://www.gnu.org/licenses/>.

"""Test harness for doctests."""

__all__ = []

import atexit
import doctest
import os

from pkg_resources import (
    cleanup_resources,
    resource_exists,
    resource_filename,
    resource_listdir,
)

DOCTEST_FLAGS = (
    doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF
)


def load_tests(loader, tests, pattern):
    """Load the doc tests (docs/*, if any exist)."""
    doctest_files = []
    if resource_exists("lazr.config", "docs"):
        for name in resource_listdir("lazr.config", "docs"):
            if name.endswith(".rst"):
                doctest_files.append(
                    os.path.abspath(
                        resource_filename("lazr.config", "docs/%s" % name)
                    )
                )
    atexit.register(cleanup_resources)
    tests.addTest(
        doctest.DocFileSuite(
            *doctest_files,
            module_relative=False,
            optionflags=DOCTEST_FLAGS,
            encoding="UTF-8",
        )
    )
    return tests
