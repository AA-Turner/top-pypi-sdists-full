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

"""Module contents."""


import unittest

from mailmanclient import Client


class TestTemplates(unittest.TestCase):
    """Tests for various types of templates.
    """

    def setUp(self):
        self.client = Client(
            'http://localhost:9001/3.1/',  'restadmin', 'restpass')
        self.domain = self.client.create_domain('example.net')
        self.mlist = self.domain.create_list('test1')

    def tearDown(self):
        for temp in self.mlist.templates:
            temp.delete()
        for temp in self.domain.templates:
            temp.delete()
        self.domain.delete()
        for temp in self.client.templates:
            temp.delete()

    def test_set_template(self):
        # At first, there are no templates at site, domain or list context
        self.assertEqual(len(self.client.templates), 0)
        self.assertEqual(len(self.domain.templates), 0)
        self.assertEqual(len(self.mlist.templates), 0)

        # Now, let's try to set a different template at each context level.
        self.client.set_template('list:user:notice:welcome',
                                 'http://example.com/welcome.txt')
        self.domain.set_template('list:user:notice:welcome',
                                 'http://example.com/welcome2.txt')
        self.mlist.set_template('list:user:notice:welcome',
                                'http://example.com/welcome3.txt')

        # Now, let's try to fetch the templates again.
        site_templates = self.client.templates
        self.assertEqual(len(site_templates), 1)
        self.assertEqual(site_templates[0].uri,
                         'http://example.com/welcome.txt')

        domain_templates = self.domain.templates
        self.assertEqual(len(domain_templates), 1)
        self.assertEqual(domain_templates[0].uri,
                         'http://example.com/welcome2.txt')

        mlist_templates = self.mlist.templates
        self.assertEqual(len(mlist_templates), 1)
        self.assertEqual(mlist_templates[0].uri,
                         'http://example.com/welcome3.txt')

    def test_site_templates_with_password(self):
        # It is possible to set templates with passwords.
        self.assertEqual(len(self.client.templates), 0)
        self.client.set_template('list:user:notice:goodbye',
                                 'http://example.com/goodbye.txt',
                                 username='testuser',
                                 password='testpass')
        site_templates = self.client.templates
        self.assertEqual(len(site_templates), 1)
        temp = site_templates[0]
        self.assertEqual(temp.uri, 'http://example.com/goodbye.txt')
        self.assertEqual(temp.username, 'testuser')
        self.assertEqual(temp.password, 'testpass')

    def test_domain_templates_with_password(self):
        self.assertEqual(len(self.domain.templates), 0)
        self.domain.set_template('list:user:notice:goodbye',
                                 'http://example.com/goodbye.txt',
                                 username='testuser',
                                 password='testpass')
        domain_templates = self.domain.templates
        self.assertEqual(len(domain_templates), 1)
        temp = domain_templates[0]
        self.assertEqual(temp.uri, 'http://example.com/goodbye.txt')
        self.assertEqual(temp.username, 'testuser')
        self.assertEqual(temp.password, 'testpass')

    def test_list_templates_with_password(self):
        self.assertEqual(len(self.mlist.templates), 0)
        self.mlist.set_template('list:user:notice:goodbye',
                                'http://example.com/goodbye.txt',
                                username='testuser',
                                password='testpass')
        mlist_templates = self.mlist.templates
        self.assertEqual(len(mlist_templates), 1)
        temp = mlist_templates[0]
        self.assertEqual(temp.uri, 'http://example.com/goodbye.txt')
        self.assertEqual(temp.username, 'testuser')
        self.assertEqual(temp.password, 'testpass')
