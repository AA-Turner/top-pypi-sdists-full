"""
Tests for cancel-statement-on-stop on the Athena V4 executor.

``AthenaV4Executor.wait`` already stopped the query on an interrupt; the change routes that call
through ``run_bounded``, so it is time-bounded and a failure to stop is logged at ``warning``
instead of ``debug``. The stop request and the re-raise are unchanged.

The boto3 client is a Mock; no AWS call is made.
"""

import contextlib
import io
import logging
import unittest
from unittest import mock

from sagemaker_studio.utils.athena_v4 import AthenaV4Executor

QID = "99999999-8888-7777-6666-555555555555"
CANCEL_LOGGER = "sagemaker_studio.utils._statement_cancel"


class AthenaInterruptStopsTheQueryTest(unittest.TestCase):
    def setUp(self):
        self.client = mock.Mock()
        self.executor = AthenaV4Executor(self.client, "wg")

    def test_interrupt_stops_the_query_and_re_raises(self):
        self.client.get_query_execution.side_effect = KeyboardInterrupt

        notice = io.StringIO()
        with contextlib.redirect_stderr(notice):
            with self.assertRaises(KeyboardInterrupt):
                self.executor.wait(QID)

        self.client.stop_query_execution.assert_called_once_with(QueryExecutionId=QID)
        # The cell shows why it stopped, above the traceback.
        self.assertIn("cancel request accepted by Athena", notice.getvalue())

    def test_a_failing_stop_is_logged_at_warning_and_still_re_raises(self):
        self.client.get_query_execution.side_effect = KeyboardInterrupt
        self.client.stop_query_execution.side_effect = RuntimeError("athena said no")

        with self.assertLogs(CANCEL_LOGGER, level=logging.WARNING) as logs:
            with self.assertRaises(KeyboardInterrupt):
                self.executor.wait(QID)

        self.client.stop_query_execution.assert_called_once_with(QueryExecutionId=QID)
        self.assertIn(f"Athena query {QID} cancel: cancellation request failed", logs.output[0])
