import time
import unittest
from unittest.mock import MagicMock

from abstra_internals.controllers.execution.execution_conn import (
    StdioBuffer,
    get_execution_conn,
    get_stdio_buffer,
    set_execution_conn,
)


class TestExecutionConn(unittest.TestCase):
    def tearDown(self):
        set_execution_conn(None)

    def test_default_conn_is_none(self):
        self.assertIsNone(get_execution_conn())

    def test_set_and_get_conn(self):
        mock_conn = MagicMock()
        set_execution_conn(mock_conn)
        self.assertIs(get_execution_conn(), mock_conn)

    def test_clear_conn(self):
        mock_conn = MagicMock()
        set_execution_conn(mock_conn)
        set_execution_conn(None)
        self.assertIsNone(get_execution_conn())

    def test_set_conn_creates_buffer(self):
        mock_conn = MagicMock()
        set_execution_conn(mock_conn)
        self.assertIsNotNone(get_stdio_buffer())

    def test_clear_conn_closes_buffer(self):
        mock_conn = MagicMock()
        set_execution_conn(mock_conn)
        set_execution_conn(None)
        self.assertIsNone(get_stdio_buffer())

    def test_default_buffer_is_none(self):
        self.assertIsNone(get_stdio_buffer())

    def test_replace_conn_creates_new_buffer(self):
        mock_conn1 = MagicMock()
        mock_conn2 = MagicMock()
        set_execution_conn(mock_conn1)
        buf1 = get_stdio_buffer()
        set_execution_conn(mock_conn2)
        buf2 = get_stdio_buffer()
        self.assertIsNot(buf1, buf2)


class TestStdioBuffer(unittest.TestCase):
    def test_add_appends_to_buffer(self):
        mock_conn = MagicMock()
        buffer = StdioBuffer(mock_conn, flush_interval=10.0)
        buffer.add({"type": "stdout", "log": "hello"})
        self.assertEqual(len(buffer._buffer), 1)
        buffer.close()

    def test_flush_sends_batch(self):
        mock_conn = MagicMock()
        buffer = StdioBuffer(mock_conn, flush_interval=10.0)
        buffer.add({"type": "stdout", "log": "line1"})
        buffer.add({"type": "stderr", "log": "line2"})
        buffer._flush()

        mock_conn.send.assert_called_once()
        msg = mock_conn.send.call_args[0][0]
        self.assertEqual(msg["type"], "stdio_batch")
        self.assertEqual(len(msg["payload"]), 2)
        self.assertEqual(msg["payload"][0]["log"], "line1")
        self.assertEqual(msg["payload"][1]["log"], "line2")
        buffer.close()

    def test_flush_empty_buffer_does_nothing(self):
        mock_conn = MagicMock()
        buffer = StdioBuffer(mock_conn, flush_interval=10.0)
        buffer._flush()
        mock_conn.send.assert_not_called()
        buffer.close()

    def test_close_does_final_flush(self):
        mock_conn = MagicMock()
        buffer = StdioBuffer(mock_conn, flush_interval=10.0)
        buffer.add({"type": "stdout", "log": "final"})
        buffer.close()

        mock_conn.send.assert_called_once()
        msg = mock_conn.send.call_args[0][0]
        self.assertEqual(msg["type"], "stdio_batch")
        self.assertEqual(msg["payload"][0]["log"], "final")

    def test_auto_flush_on_interval(self):
        mock_conn = MagicMock()
        buffer = StdioBuffer(mock_conn, flush_interval=0.05)
        buffer.add({"type": "stdout", "log": "hello"})
        time.sleep(0.2)
        mock_conn.send.assert_called()
        buffer.close()

    def test_conn_error_does_not_raise(self):
        mock_conn = MagicMock()
        mock_conn.send.side_effect = Exception("RabbitMQ down")
        buffer = StdioBuffer(mock_conn, flush_interval=10.0)
        buffer.add({"type": "stdout", "log": "hello"})
        # Should not raise
        buffer._flush()
        buffer.close()

    def test_flush_clears_buffer(self):
        mock_conn = MagicMock()
        buffer = StdioBuffer(mock_conn, flush_interval=10.0)
        buffer.add({"type": "stdout", "log": "hello"})
        buffer._flush()
        self.assertEqual(len(buffer._buffer), 0)
        buffer.close()


if __name__ == "__main__":
    unittest.main()
