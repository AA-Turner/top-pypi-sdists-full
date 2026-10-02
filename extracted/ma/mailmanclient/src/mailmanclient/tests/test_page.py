# Copyright (C) 2016-2023 by the Free Software Foundation, Inc.
#
# This file is part of mailmanclient.
#
# mailmanclient is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, version 3 of the License.
#
# mailmanclient is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with mailmanclient.  If not, see <http://www.gnu.org/licenses/>.

"""Test Page corner cases."""
import unittest

from unittest.mock import Mock
from urllib.parse import urlsplit, parse_qs

from mailmanclient.constants import DEFAULT_PAGE_ITEM_COUNT
from mailmanclient.restbase.page import Page

__metaclass__ = type
__all__ = [
    'TestPage',
    ]


class TestPage(unittest.TestCase):

    def test_url_simple(self):
        connection = Mock()
        connection.call.return_value = (None, {'start': 0, 'total_size': 0})
        page = Page(connection, '/some-path', None)
        built_qs = parse_qs(urlsplit(page._build_url()).query)
        self.assertEqual(built_qs, dict(
            count=[str(DEFAULT_PAGE_ITEM_COUNT)],
            page=["1"]))

    def test_url_with_qs(self):
        connection = Mock()
        connection.call.return_value = (None, {'start': 0, 'total_size': 0})
        page = Page(connection, '/some-path?with=a&query=string', None)
        built_qs = parse_qs(urlsplit(page._build_url()).query)
        self.assertEqual(built_qs, {
            "with": ["a"],
            "query": ["string"],
            "count": [str(DEFAULT_PAGE_ITEM_COUNT)],
            "page": ["1"],
            })
