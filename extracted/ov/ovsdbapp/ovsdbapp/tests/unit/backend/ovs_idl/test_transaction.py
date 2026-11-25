# Copyright (c) 2026 Red Hat LLC
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import time
from unittest import mock

import testscenarios

from ovsdbapp.backend.ovs_idl import connection
from ovsdbapp.backend.ovs_idl import transaction
from ovsdbapp import exceptions
from ovsdbapp.tests import base


load_tests = testscenarios.load_tests_apply_scenarios


class TestTransaction(base.TestCase):
    scenarios = [
        ('check_error', {'check_error': True}),
        ('ignore_error', {'check_error': False}),
    ]

    @mock.patch.object(transaction.Transaction, 'pre_commit')
    def test_pre_commit_exception_aborts(self, pre_commit):
        # Use a real python-ovs transaction to check that abort clears idl.txn.
        api = mock.Mock(idl=mock.Mock(txn=None, change_seqno=0))
        txn = transaction.Transaction(api, mock.Mock(timeout=1),
                                      check_error=self.check_error)
        command = txn.add(mock.Mock())
        error = RuntimeError('pre_commit failed')
        pre_commit.side_effect = error

        raised = self.assertRaises(RuntimeError, txn.do_commit)

        self.assertIs(error, raised)
        self.assertIsNone(api.idl.txn)
        command.run_idl.assert_not_called()


class TestTransactionTimeout(base.TestCase):

    def setUp(self):
        super().setUp()
        self.conn = mock.Mock(timeout=180)
        self.txn = transaction.Transaction(mock.Mock(), self.conn,
                                           timeout=60)
        self.txn.results = mock.Mock()

    @mock.patch.object(transaction.time, 'monotonic')
    def test_commit_shares_timeout(self, monotonic):
        # 20 seconds are spent waiting for room in the queue.
        monotonic.side_effect = [100, 120]
        self.txn.results.get.return_value = []

        self.txn.commit()

        self.conn.queue_txn.assert_called_once_with(self.txn, timeout=60)
        self.txn.results.get.assert_called_once_with(timeout=40)
        self.assertEqual(160, self.txn.deadline)

    @mock.patch.object(transaction.time, 'monotonic')
    def test_commit_queue_wait_exhausts_timeout(self, monotonic):
        monotonic.side_effect = [100, 170]
        self.txn.results.get.return_value = []

        self.txn.commit()

        self.txn.results.get.assert_called_once_with(timeout=0)

    def test_commit_timeout_reports_last_error(self):
        conn = connection.Connection(mock.Mock(), timeout=180)
        self.addCleanup(conn.txns.close)
        conn.last_error = ValueError('filedescriptor out of range in select()')
        txn = transaction.Transaction(mock.Mock(), conn, timeout=0.01)

        ex = self.assertRaises(exceptions.TimeoutException, txn.commit)

        self.assertIn("cause: Result queue is empty, last connection error: "
                      "ValueError('filedescriptor out of range in "
                      "select()')", str(ex))

    @mock.patch.object(transaction.idl, 'Transaction')
    def test_do_commit_expired(self, idl_txn):
        self.txn.add(mock.Mock())
        self.txn.deadline = time.monotonic() - 1

        ex = self.assertRaises(exceptions.TimeoutException,
                               self.txn.do_commit)

        self.assertIn('cause: Transaction expired in the queue', str(ex))
        idl_txn.assert_not_called()

    @mock.patch.object(transaction.idl, 'Transaction')
    def test_do_commit_not_expired(self, idl_txn):
        command = self.txn.add(mock.Mock())
        self.txn.deadline = time.monotonic() + 60
        idl_txn.return_value.commit_block.return_value = (
            idl_txn.return_value.SUCCESS)

        self.assertEqual([command.result], self.txn.do_commit())

        command.run_idl.assert_called_once_with(idl_txn.return_value)
