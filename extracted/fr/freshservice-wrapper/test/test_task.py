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

from freshservice.api import API, TaskAPI, TicketAPI
from freshservice.errors import ResponseError
from freshservice.models import Task


TEST_DOMAIN = 'flamunda'
AGENT_ID = 7000027089


class TestTask(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = API(os.environ['FRESHSERVICE_API_KEY'], TEST_DOMAIN)
        cls.ticket_api = TicketAPI(cls.api)
        cls.task_api = TaskAPI(cls.api)

        # create reference ticket
        cls.ticket_id = cls.ticket_api.create_ticket(
            'Test', 'requester@egym.de').display_id
        # create reference task
        cls.task = cls.task_api.create_task(
            'Test', 'description', cls.ticket_id, owner_id=AGENT_ID)

    def test_delete(self):
        task_id = self.task_api.create_task(
            'Test', 'description', self.ticket_id).id
        self.task_api.delete_task(self.ticket_id, task_id)
        with self.assertRaises(ResponseError):
            self.task_api.get_task(self.ticket_id, task_id)

    def test_update_and_get(self):
        self.assertEqual(self.task.description, 'description')
        self.assertEqual(self.task.owner_id, AGENT_ID)
        self.assertEqual(self.task.title, 'Test')
        self.assertEqual(self.task.status, 'open')

        self.task_api.update_task(
            self.ticket_id, self.task.id, status=Task.COMPLETED)

        self.task = self.task_api.get_task(
            self.ticket_id, self.task.id)
        self.assertEqual(self.task.status, 'completed')

    def test_magic_methods(self):
        print(self.task)
        print(repr(self.task))

    def test_get_all_tasks(self):
        tasks = self.task_api.get_all_tasks(self.ticket_id)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Test")

    def test_error(self):
        with self.assertRaises(ResponseError):
            task_api = TaskAPI(self.api, module="none")
            task_api.create_task(" ", " ", 0)
