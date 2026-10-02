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

"""Test for the general Client specific behavior.."""

import unittest

from mailmanclient import Client
from urllib.error import HTTPError


class TestUrlencodedPaths(unittest.TestCase):
    """Test that paths are always safe"""

    def setUp(self):
        self._client = Client(
            'http://localhost:9001/3.1', 'restadmin', 'restpass')
        self.domain = self._client.create_domain('example.org')

    def tearDown(self):
        self.domain.delete()
        for user in self._client.users:
            user.delete()

    def test_bans_paths_are_urlencoded_when_needed(self):
        # Test that we can ban regular expressions.
        self._client.bans.add('^something?example@something.com')
        bans = self._client.bans
        self.assertEqual(len(bans), 1)
        # This should actually call the URL and should return True.
        self.assertIn('^something?example@something.com', self._client.bans)

    def test_member_paths_are_urlencoded(self):
        mlist = self.domain.create_list('other')
        mlist.subscribe('apers?on@example.com',
                        pre_verified=True,
                        pre_confirmed=True,
                        pre_approved=True)
        # Make sure that member exists.
        self.assertEqual(len(mlist.members), 1)
        # Let's see if we can get the member resource. This will
        try:
            member = mlist.get_member('apers?on@example.com')
            self.assertIsNotNone(member)
        except HTTPError:
            self.fail('Unexpected HTTPError.')

    def test_non_member_paths_are_urlencoded(self):
        mlist = self.domain.create_list('some')
        mlist.add_role(address='somperson?123@example.com', role='moderator')
        # Now, this shouldn't raise 404 error.
        try:
            mlist.remove_role(
                address='somperson?123@example.com', role='moderator')
        except HTTPError:
            self.fail('Unexpected HTTPError.')


class TestHooks(unittest.TestCase):

    def test_initialize_with_hooks(self):
        # Test that we can initialize mailmanclient with hooks.
        calls = []

        def store_calls(params):
            calls.append(params)
            return params
        client = Client(
            'http://localhost:9001/3.1', 'restadmin', 'restpass',
            request_hooks=[store_calls])
        # Make *any* API call.
        client.domains
        # Now make sure the call was stored.
        self.assertEqual(len(calls), 1)
        params = calls[0]
        self.assertEqual(
            params.get('url'), 'http://localhost:9001/3.1/domains')

    def test_add_hooks(self):
        calls = []

        def store_calls(params):
            calls.append(params)
            return params
        client = Client(
            'http://localhost:9001/3.1', 'restadmin', 'restpass')
        # Make *any* API call.
        client.domains
        # Now make sure the call was not stored.
        self.assertEqual(len(calls), 0)
        client.add_hooks([store_calls])
        # Now make another API call.
        client.lists
        params = calls[0]
        self.assertEqual(params.get('url'), 'http://localhost:9001/3.1/lists')


class TestFindUsers(unittest.TestCase):

    def setUp(self):
        self._client = Client(
            'http://localhost:9001/3.1', 'restadmin', 'restpass')
        self._client.create_user('anne@example.com', 'xxx', 'Anne Person')
        self._client.create_user('bart@example.com', 'xxx', 'Bee Person')

    def tearDown(self):
        for user in self._client.users:
            user.delete()

    def test_find_users(self):
        # Make sure the users are created.
        self.assertEqual(len(self._client.users), 2)
        # Now search for the user.
        users = self._client.find_users('bee')
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].display_name, 'Bee Person')
        # search for the email.
        users = self._client.find_users('ne@ex')
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].display_name, 'Anne Person')

    def test_find_user_page(self):
        self.assertEqual(len(self._client.users), 2)
        # Now search for the user.
        users = self._client.find_users_page('person', count=1, page=1)
        # We should've got only single user with count=1.
        self.assertEqual(len(users), 1)
        # Total results should be 2.
        self.assertEqual(users.total_size, 2)
        self.assertEqual(users[0].display_name, 'Anne Person')
