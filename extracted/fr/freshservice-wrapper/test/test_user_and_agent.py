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

from freshservice.api import API, AgentAPI, UserAPI
from freshservice.errors import AgentSearchFailed, UserSearchFailed


TEST_DOMAIN = 'flamunda'
AGENT_ID = 7000006217
USER_ID = 7000479601


class TestAgent(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = API(os.environ['FRESHSERVICE_API_KEY'], TEST_DOMAIN)
        cls.agent_api = AgentAPI(cls.api)

    def test_agent_search(self):
        agent = self.agent_api.search('lennart.weiss@egym.de')
        self.assertEqual(agent.id, AGENT_ID)

    def test_agent_search_error(self):
        with self.assertRaises(AgentSearchFailed):
            self.agent_api.search('hello.world@egym.de')


class TestUser(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = API(os.environ['FRESHSERVICE_API_KEY'], TEST_DOMAIN)
        cls.user_api = UserAPI(cls.api)

    def test_user_search(self):
        user = self.user_api.search('hello.world@egym.de')
        self.assertEqual(user.id, USER_ID)

    def test_user_search_error(self):
        with self.assertRaises(UserSearchFailed):
            self.user_api.search('nonexisting.user@egym.de')
