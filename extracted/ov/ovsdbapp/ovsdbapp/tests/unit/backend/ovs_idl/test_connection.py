# Copyright 2015, Red Hat, Inc.
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

import queue
from unittest import mock

from ovs import poller

from ovsdbapp.backend.ovs_idl import connection
from ovsdbapp.backend.ovs_idl import idlutils
from ovsdbapp import exceptions
from ovsdbapp.tests import base


@mock.patch.object(connection.threading, 'Thread')
class TestOVSNativeConnection(base.TestCase):

    @mock.patch.object(connection, 'TransactionQueue')
    def setUp(self, mock_trans_queue):
        super().setUp()
        self.idl = mock.Mock()
        self.mock_trans_queue = mock_trans_queue
        self.conn = connection.Connection(self.idl, timeout=1)
        self.mock_trans_queue.assert_called_once_with(1)

    @mock.patch.object(poller, 'Poller')
    @mock.patch.object(idlutils, 'wait_for_change')
    def test_start(self, mock_wait_for_change, mock_poller, mock_thread):
        self.idl.has_ever_connected.return_value = False
        self.conn.start()
        self.idl.has_ever_connected.assert_called_once()
        mock_wait_for_change.assert_any_call(self.conn.idl, self.conn.timeout)
        mock_poller.assert_called_once_with()
        mock_thread.assert_called_once_with(target=self.conn.run)
        self.assertIs(True, mock_thread.return_value.daemon)
        mock_thread.return_value.start.assert_called_once_with()

    def test_queue_txn(self, mock_thread):
        self.conn.start()
        self.conn.queue_txn('blah')
        self.conn.txns.put.assert_called_once_with('blah',
                                                   timeout=self.conn.timeout)

    def test_queue_txn_timeout(self, mock_thread):
        self.conn.queue_txn('blah', timeout=5)
        self.conn.txns.put.assert_called_once_with('blah', timeout=5)

    def test_queue_txn_full(self, mock_thread):
        self.conn.txns.put.side_effect = queue.Full
        txn = mock.Mock(commands=[])

        ex = self.assertRaises(exceptions.TimeoutException,
                               self.conn.queue_txn, txn)

        self.assertIn('cause: TXN queue is full', str(ex))
        self.assertNotIn('last connection error', str(ex))

    def test_queue_txn_full_reports_last_error(self, mock_thread):
        self.conn.txns.put.side_effect = queue.Full
        self.conn.last_error = ValueError(
            'filedescriptor out of range in select()')
        txn = mock.Mock(commands=[])

        ex = self.assertRaises(exceptions.TimeoutException,
                               self.conn.queue_txn, txn)

        self.assertIn("cause: TXN queue is full, last connection error: "
                      "ValueError('filedescriptor out of range in "
                      "select()')", str(ex))

    def _run(self, *idl_run_effects):
        """Run one loop of run() per effect, raising it unless it is None."""
        self.conn.poller = mock.Mock()
        self.conn.is_running = True
        self.conn.txns.get_nowait.return_value = None
        effects = list(idl_run_effects)

        def idl_run():
            effect = effects.pop(0)
            if not effects:
                # Leave the loop after the last iteration.
                self.conn.is_running = False
            if effect is not None:
                raise effect

        self.idl.run.side_effect = idl_run
        self.conn.run()

    def test_run_stores_last_error(self, mock_thread):
        error = RuntimeError('unhandled')

        self._run(error)

        self.assertIs(error, self.conn.last_error)
        # The queued transaction stays queued for the next loop.
        self.conn.txns.get_nowait.assert_not_called()

    def test_run_clears_last_error(self, mock_thread):
        self._run(RuntimeError('unhandled'), None)

        self.assertIsNone(self.conn.last_error)
        self.conn.txns.get_nowait.assert_called_once_with()


class TestTransactionQueue(base.TestCase):

    def test_init(self):
        # a test to cover py34 failure during initialization (LP Bug #1580270)
        # make sure no ValueError: can't have unbuffered text I/O is raised
        connection.TransactionQueue()
