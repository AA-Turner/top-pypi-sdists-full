# Copyright 2018 eGym GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from unittest import TestCase

from freshservice.api import API, TicketAPI
from freshservice.errors import BadInput
from freshservice.models import Ticket


TEST_DOMAIN = 'flamunda'


class TestTicket(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = API(os.environ['FRESHSERVICE_API_KEY'], TEST_DOMAIN)
        cls.ticket_api = TicketAPI(cls.api)

        # create reference ticket
        ticket_data = {
            'description': 'Test',
            'status': Ticket.CLOSED,
            'priority': Ticket.LOW,
            'source': Ticket.PORTAL,
            'cc_email': 'test@egym.de',
            'reply_cc': 'test@egym.de'
        }
        cls.ticket = cls.ticket_api.create_ticket(
            'Test', 'requester@egym.de', **ticket_data)

    def test_add_note(self):
        self.ticket_api.add_note(
            self.ticket.display_id, description="Test", public=True)
        self.ticket_api.add_note(
            self.ticket.display_id, description="Test2")

    def test_delete(self):
        self.assertFalse(self.ticket.deleted)
        self.ticket_api.delete_ticket(self.ticket.display_id)
        self.ticket = self.ticket_api.get_ticket(self.ticket.display_id)
        self.assertTrue(self.ticket.deleted)

    def test_magic_methods(self):
        print(repr(self.ticket))
        print(str(self.ticket))

    def test_properties(self):
        ticket = eval(repr(self.ticket))
        assert hasattr(ticket, 'coordinate')
        assert hasattr(ticket, 'location')
        assert hasattr(ticket, 'type')
        ticket.priority = 'urgent'
        ticket.status = 'open'
        ticket.source = 'chat'
        self.assertEqual(ticket.priority, 'urgent')
        self.assertEqual(ticket.status, 'open')
        self.assertEqual(ticket.source, 'chat')
        with self.assertRaises(BadInput):
            ticket.priority = 'bla'
        with self.assertRaises(BadInput):
            ticket.status = 'blop'
        with self.assertRaises(BadInput):
            ticket.source = 'blurb'

    def test_update_and_get(self):
        self.assertIsInstance(self.ticket, Ticket)
        self.assertEqual(self.ticket.subject, 'Test')
        self.assertEqual(self.ticket.description, 'Test')
        self.assertEqual(self.ticket.status, 'closed')
        self.assertEqual(self.ticket.priority, 'low')
        self.assertEqual(self.ticket.source, 'portal')

        self.ticket_api.update_ticket(
            self.ticket.display_id,
            subject='Test update',
            due_by='2100-01-01')

        self.ticket = self.ticket_api.get_ticket(self.ticket.display_id)
        self.assertIsInstance(self.ticket, Ticket)
        self.assertEqual(self.ticket.subject, 'Test update')
        self.assertEqual(self.ticket.due_by, '2100-01-01T00:00:00+01:00')
