import unittest
from unittest.mock import MagicMock

from abstra_internals.controllers.execution.execution_conn import (
    StdioBuffer,
    get_broadcast_publisher,
    set_broadcast_publisher,
)


class TestStdioBufferDualPublish(unittest.TestCase):
    """Tests that StdioBuffer publishes to both conn and broadcast publisher."""

    def tearDown(self):
        set_broadcast_publisher(None)

    def test_flush_publishes_to_broadcast_publisher(self):
        """When a broadcast publisher is set, _flush should also call publisher.publish()."""
        mock_conn = MagicMock()
        mock_publisher = MagicMock()
        set_broadcast_publisher(mock_publisher)

        buf = StdioBuffer(mock_conn, flush_interval=10.0)  # long interval, manual flush
        buf.add({"type": "stdout", "log": "hello"})
        buf._flush()
        buf.close()

        # conn.send should have the stdio_batch
        mock_conn.send.assert_called_once()
        call_args = mock_conn.send.call_args[0][0]
        self.assertEqual(call_args["type"], "stdio_batch")

        # publisher.publish should also have the stdio_batch
        mock_publisher.publish.assert_called_once()
        pub_args = mock_publisher.publish.call_args[0][0]
        self.assertEqual(pub_args["type"], "stdio_batch")

    def test_flush_works_without_broadcast_publisher(self):
        """When no broadcast publisher is set, _flush should only send to conn."""
        mock_conn = MagicMock()
        set_broadcast_publisher(None)

        buf = StdioBuffer(mock_conn, flush_interval=10.0)
        buf.add({"type": "stdout", "log": "hello"})
        buf._flush()
        buf.close()

        mock_conn.send.assert_called_once()

    def test_broadcast_publisher_failure_does_not_affect_conn(self):
        """If broadcast publisher.publish() fails, conn.send() should still work."""
        mock_conn = MagicMock()
        mock_publisher = MagicMock()
        mock_publisher.publish.side_effect = Exception("rabbitmq down")
        set_broadcast_publisher(mock_publisher)

        buf = StdioBuffer(mock_conn, flush_interval=10.0)
        buf.add({"type": "stdout", "log": "hello"})
        buf._flush()
        buf.close()

        # conn.send should still have been called
        mock_conn.send.assert_called_once()

    def test_conn_failure_does_not_affect_broadcast_publisher(self):
        """If conn.send() fails, broadcast publisher.publish() should still work."""
        mock_conn = MagicMock()
        mock_conn.send.side_effect = Exception("connection lost")
        mock_publisher = MagicMock()
        set_broadcast_publisher(mock_publisher)

        buf = StdioBuffer(mock_conn, flush_interval=10.0)
        buf.add({"type": "stdout", "log": "hello"})
        buf._flush()
        buf.close()

        # publisher.publish should still have been called
        mock_publisher.publish.assert_called_once()


class TestBroadcastPublisherGlobal(unittest.TestCase):
    """Tests for the global broadcast publisher get/set."""

    def tearDown(self):
        set_broadcast_publisher(None)

    def test_get_returns_none_by_default(self):
        """get_broadcast_publisher should return None when nothing is set."""
        set_broadcast_publisher(None)
        self.assertIsNone(get_broadcast_publisher())

    def test_set_and_get(self):
        """set_broadcast_publisher / get_broadcast_publisher round-trip."""
        mock_pub = MagicMock()
        set_broadcast_publisher(mock_pub)
        self.assertIs(get_broadcast_publisher(), mock_pub)

    def test_set_none_clears(self):
        """Setting None should clear the publisher."""
        mock_pub = MagicMock()
        set_broadcast_publisher(mock_pub)
        set_broadcast_publisher(None)
        self.assertIsNone(get_broadcast_publisher())
