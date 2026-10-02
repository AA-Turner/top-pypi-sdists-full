# Copyright (C) 2017-2023 by the Free Software Foundation, Inc.
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

"""Tests for Mailing List."""

import time

from urllib.error import HTTPError
from unittest import TestCase
from mailmanclient import Client
from mailmanclient.restobjects.member import Member


class TestMailingListMembershipTests(TestCase):

    def setUp(self):
        self._client = Client(
            'http://localhost:9001/3.1', 'restadmin', 'restpass')
        try:
            self.domain = self._client.create_domain('example.com')
        except HTTPError:
            self.domain = self._client.get_domain('example.com')
        self.mlist = self.domain.create_list('foo')

    def tearDown(self):
        self.domain.delete()

    def test_list_is_owner(self):
        # Tests MailingList.is_owner
        # First, we add an owner to the mailing list and then make sure that
        # we see it in the owners roster.
        anne_addr = 'ann@example.com'
        self.mlist.add_owner(anne_addr)
        # Check that the address
        owners_list = [owner.email for owner in self.mlist.owners]
        self.assertIn(anne_addr, owners_list)
        # Now, we make sure that we get the same result in our API.
        self.assertTrue(self.mlist.is_owner(anne_addr))
        # Make sure we get False for someone who is not a list owner.
        self.assertFalse(self.mlist.is_owner('random@example.com'))
        # Make sure that a subscriber doesn't return True for is_owner check.
        # We are doing this test because of the way is_owner test works. A
        # wrong value for `role` could result in a list member being tested
        # as owner.
        self.mlist.subscribe('bart@example.com')
        self.assertFalse(self.mlist.is_owner('bart@example.com'))
        # Now, try the same thing for Moderators.
        self.mlist.add_moderator('mod@example.com')
        self.assertFalse(self.mlist.is_owner('mod@example.com'))

    def test_list_is_moderator(self):
        # Tests MailingList.is_moderator
        # First, we add a moderator to the list.
        mod_addr = 'mod@example.com'
        self.mlist.add_moderator(mod_addr)
        mods_emails = [mod.email for mod in self.mlist.moderators]
        self.assertIn(mod_addr, mods_emails)
        self.assertFalse(self.mlist.is_owner(mod_addr))
        # Owners shouldn't return true for this API.
        owner_addr = 'owner@example.com'
        self.mlist.add_owner(owner_addr)
        self.assertFalse(self.mlist.is_moderator(owner_addr))
        # Subscribers shouldn't return true for this API.
        subscriber_addr = 'subscriber@example.com'
        self.mlist.subscribe(subscriber_addr)
        self.assertFalse(self.mlist.is_moderator(subscriber_addr))

    def test_list_is_member(self):
        # Tests MailingList.is_member
        subscriber_addr = 'subscriber@example.com'
        self.mlist.subscribe(subscriber_addr, pre_verified=True,
                             pre_confirmed=True, pre_approved=True)
        all_subscribers = [member.email for member in self.mlist.members]
        self.assertIn(subscriber_addr, all_subscribers)
        # Now make sure we get the same result through this API.
        self.assertTrue(self.mlist.is_member(subscriber_addr))
        # Make sure owners don't pass this check.
        owner_addr = 'owner@example.com'
        self.mlist.add_owner(owner_addr)
        self.assertFalse(self.mlist.is_member(owner_addr))
        # Make sure moderators don't pass this check.
        mod_addr = 'mod@example.com'
        self.mlist.add_moderator(mod_addr)
        self.assertFalse(self.mlist.is_member(mod_addr))

    def test_list_is_owner_or_mod(self):
        # Tests MailingList.is_owner_or_mod
        # Tests MailingList.is_moderator
        # First, we add a moderator to the list.
        mod_addr = 'mod@example.com'
        self.mlist.add_moderator(mod_addr)
        mods_emails = [mod.email for mod in self.mlist.moderators]
        self.assertIn(mod_addr, mods_emails)
        self.assertTrue(self.mlist.is_owner_or_mod(mod_addr))
        # Owners shouldn't return true for this API.
        owner_addr = 'owner@example.com'
        self.mlist.add_owner(owner_addr)
        owners_list = [owner.email for owner in self.mlist.owners]
        self.assertIn(owner_addr, owners_list)
        self.assertTrue(self.mlist.is_owner_or_mod(owner_addr))
        # Subscribers shouldn't return true for this API.
        subscriber_addr = 'subscriber@example.com'
        self.mlist.subscribe(subscriber_addr)
        self.assertFalse(self.mlist.is_owner_or_mod(subscriber_addr))

    def test_list_unsubscribe(self):
        # Tests MailingList.unsubscribe
        subscriber_addr = 'subscriber@example.com'
        self.mlist.subscribe(subscriber_addr, pre_verified=True,
                             pre_confirmed=True, pre_approved=True)
        self.assertTrue(self.mlist.is_member(subscriber_addr))
        self.mlist.unsubscribe(subscriber_addr, pre_confirmed=True,
                               pre_approved=True)
        self.assertFalse(self.mlist.is_member(subscriber_addr))


class TestHeldMessage(TestCase):

    def setUp(self):
        self._client = Client(
            'http://localhost:9001/3.1', 'restadmin', 'restpass')

        try:
            self.domain = self._client.create_domain('example.com')
        except HTTPError:
            self.domain = self._client.get_domain('example.com')

        self.mlist = self.domain.create_list('foo')
        # Test that a held message can be moderated.
        msg = """\
From: nonmember@example.com
To: foo@example.com
Subject: Hello World
Message-ID: <msgid>

Hello!
"""
        self._inject_message(msg, self.mlist)
        # Wait for the message to appear in the held queue for 10 seconds max.
        self._wait_for_message_in_held_queue(self.mlist, 30)

    def tearDown(self):
        self.domain.delete()

    def _inject_message(self, msg, mlist):
        inq = self._client.queues['in']
        inq.inject('foo.example.com', msg)

    def _wait_for_message_in_held_queue(self, mlist, timeout):
        """Wait for held message in mlist for timeout seconds."""
        start_time = time.time()
        while True:
            # if (start_time + timeout > time.time()):
            #     print('timeout trying to wait for message')
            #     break
            all_held = mlist.held
            if len(all_held) > 0:
                print('Total time to wait for message:')
                print(time.time() - start_time)
                break
            time.sleep(0.1)

    def test_held_message_moderation(self):
        # Test that message was held and not timed out.
        self.assertEqual(len(self.mlist.held), 1)
        held = self.mlist.held[0]
        held_message = self.mlist.get_held_message(held.request_id)

        # Now, let's try to reject this message with a reason.
        response = self.mlist.reject_message(held_message.request_id,
                                             reason='You shall not pass.')
        self.assertEqual(response.status_code, 204)
        # Make sure that the message was rejected.
        self.assertEqual(len(self.mlist.held), 0)

    def test_held_message_moderation_message_object(self):
        # The only difference between this and the above test is that we use
        # the `held_message.reject` API, which for some reason as different
        # code to make the same API call.
        self.assertEqual(len(self.mlist.held), 1)
        held = self.mlist.held[0]
        held_message = self.mlist.get_held_message(held.request_id)

        # Now, let's try to reject this message with a reason.
        response = held_message.reject(reason='You shall not pass.')
        self.assertEqual(response.status_code, 204)
        # Make sure that the message was rejected.
        self.assertEqual(len(self.mlist.held), 0)


class TestMailingList(TestCase):

    def setUp(self):
        self._client = Client(
            'http://localhost:9001/3.1', 'restadmin', 'restpass')
        try:
            self.domain = self._client.create_domain('example.com')
        except HTTPError:
            self.domain = self._client.get_domain('example.com')
        self.mlist = self.domain.create_list('foo')

    def tearDown(self):
        self.domain.delete()

    def test_subscribe_without_display_name(self):
        self.mlist.subscribe('aperson@example.com',
                             pre_verified=True,
                             pre_confirmed=True,
                             pre_approved=True)
        users = self.mlist.members[0]
        self.assertEqual(users.display_name, '')

    def test_subscribe_with_display_name(self):
        self.mlist.subscribe('bperson@example.com',
                             display_name='B Person',
                             pre_verified=True,
                             pre_confirmed=True,
                             pre_approved=True)
        users = self.mlist.members[0]
        self.assertEqual(users.display_name, 'B Person')

    def test_invite(self):
        data = self.mlist.subscribe('cperson@example.com',
                                    invitation=True)
        # cperson is not a member yet.
        self.assertRaisesRegex(ValueError,
                               'not a member',
                               self.mlist.get_member,
                               'cperson@example.com')
        # But we got a token for the invitation.
        self.assertEqual(data['token_owner'], 'subscriber')

    def test_get_individual_pending_request(self):
        data = self.mlist.subscribe('aperson@example.com', pre_confirmed=False)
        self.assertEqual(data['token_owner'], 'subscriber')
        # Now get the individual request object.
        json = self.mlist.get_request(data['token'])
        self.assertEqual(json['token_owner'], data['token_owner'])
        self.assertEqual(json['token'], data['token'])

    def test_get_unsubscription_requests(self):
        member = self.mlist.subscribe(
            'aperson@example.com',
            pre_confirmed=True, pre_verified=True, pre_approved=True)
        self.assertTrue(isinstance(member, Member))
        self.assertEqual(len(self.mlist.members), 1)
        settings = self.mlist.settings
        settings['unsubscription_policy'] = 'moderate'
        settings.save()
        # try to unsubscribe a user.
        self.mlist.unsubscribe('aperson@example.com', pre_approved=False)
        self.assertEqual(len(self.mlist.members), 1)
        self.assertEqual(len(self.mlist.unsubscription_requests), 1)
        unsub_req = self.mlist.unsubscription_requests[0]
        self.assertEqual(unsub_req['token_owner'], 'moderator')
        self.assertEqual(unsub_req['email'], 'aperson@example.com')
