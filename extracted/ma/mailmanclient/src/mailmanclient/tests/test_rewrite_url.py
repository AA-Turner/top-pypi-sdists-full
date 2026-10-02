# Copyright (C) 2019-2023 by the Free Software Foundation, Inc.
#
# This file is part of mailman.client.
#
# mailman.client is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, version 3 of the License.
#
# mailman.client is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with mailman.client.  If not, see <http://www.gnu.org/licenses/>.

"""Test for the rewriting of self_link URLs."""

import unittest

from mailmanclient import Client


class TestRewriteUrl(unittest.TestCase):
    """Test that self_link paths are safely rewritten"""

    def setUp(self):
        self._client = Client(
            'http://127.0.0.1:9001/3.1', 'restadmin', 'restpass')
        self.domain = self._client.create_domain('example.org')

    def tearDown(self):
        self.domain.delete()

    def test_domain_self_link_is_localhost(self):
        domain = self._client.get_domain('example.org')
        assert domain.self_link.startswith('http://localhost:9001/')

    def test_connection_rewrite_url(self):
        link = self._client._connection.rewrite_url(self.domain.self_link)
        assert link.startswith('http://127.0.0.1:9001/')

    def test_connection_rewrites_url(self):
        response, _c = self._client._connection.call(self.domain.self_link)
        assert response.url.startswith('http://127.0.0.1:9001/')
