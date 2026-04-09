import json
import time
import unittest
from unittest.mock import MagicMock, patch

import flask_sock

from abstra_internals.utils.websockets import bind_ws_with_connection


def _make_mock_conn(messages, execution_id=None):
    """Create a mock connection that returns messages sequentially, then signals closed."""
    remaining = list(messages)

    mock_conn = MagicMock()
    mock_conn.execution_id = execution_id

    def poll_side_effect(timeout=0.0):
        if not remaining:
            return False
        return True

    def recv_side_effect(*args, **kwargs):
        if not remaining:
            raise EOFError("No more messages")
        return remaining.pop(0)

    mock_conn.poll.side_effect = poll_side_effect
    mock_conn.recv.side_effect = recv_side_effect
    # After messages are consumed, closed returns True
    type(mock_conn).closed = property(lambda self: len(remaining) == 0)

    return mock_conn


def _make_mock_ws():
    """Create a mock WS that blocks on receive() long enough for client_loop to process,
    then raises ConnectionClosed."""
    mock_ws = MagicMock()

    def receive_side_effect(timeout=None):
        # Block long enough for client_loop to process messages
        time.sleep(5.0)
        raise flask_sock.ConnectionClosed()

    mock_ws.receive.side_effect = receive_side_effect
    return mock_ws


class TestWebSocketBroadcastInterception(unittest.TestCase):
    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_form_protocol_messages_sent_to_ws(self, MockBroadcast):
        form_msg = '{"type": "form:update", "payload": {}}'
        mock_conn = _make_mock_conn([form_msg])
        mock_ws = _make_mock_ws()

        bind_ws_with_connection(mock_ws, mock_conn, block=False)
        time.sleep(0.5)

        # Form protocol message (string) should go to ws.send()
        mock_ws.send.assert_called_once_with(form_msg)
        # Should NOT be sent to BroadcastController
        MockBroadcast.broadcast.assert_not_called()

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_stdio_message_forwarded_to_broadcast(self, MockBroadcast):
        stdio_msg = {
            "type": "stdio",
            "payload": {
                "type": "stdout",
                "log": "hello",
                "execution_id": "e1",
                "stage_id": "s1",
            },
        }
        mock_conn = _make_mock_conn([stdio_msg])
        mock_ws = _make_mock_ws()

        bind_ws_with_connection(mock_ws, mock_conn, block=False)
        time.sleep(0.5)

        # stdio dict should go to BroadcastController, not ws.send()
        MockBroadcast.broadcast.assert_called_once()
        broadcast_msg = json.loads(MockBroadcast.broadcast.call_args[1]["msg"])
        self.assertEqual(broadcast_msg["type"], "stdio")

        # ws.send should NOT have been called with this message
        for call_args in mock_ws.send.call_args_list:
            msg = call_args[0][0]
            if isinstance(msg, str):
                try:
                    parsed = json.loads(msg)
                    self.assertNotEqual(parsed.get("type"), "stdio")
                except json.JSONDecodeError:
                    pass

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_task_message_skipped_in_client_loop(self, MockBroadcast):
        """Task dict messages are skipped by client_loop (fanout consumer handles them)."""
        task_msg = {"type": "task", "payload": {"id": "t1", "status": "pending"}}
        mock_conn = _make_mock_conn([task_msg])
        mock_ws = _make_mock_ws()

        bind_ws_with_connection(mock_ws, mock_conn, block=False)
        time.sleep(0.5)

        MockBroadcast.broadcast.assert_not_called()
        mock_ws.send.assert_not_called()

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_mixed_messages_correctly_routed(self, MockBroadcast):
        form_msg = '{"type": "form:update", "payload": {}}'
        stdio_msg = {"type": "stdio", "payload": {"type": "stdout", "log": "hello"}}
        task_msg = {"type": "task", "payload": {"id": "t1", "status": "pending"}}
        form_msg2 = '{"type": "form:response", "payload": {"key": "val"}}'

        mock_conn = _make_mock_conn([form_msg, stdio_msg, task_msg, form_msg2])
        mock_ws = _make_mock_ws()

        bind_ws_with_connection(mock_ws, mock_conn, block=False)
        time.sleep(1.0)

        # BroadcastController should have been called once (stdio only; task uses fanout)
        self.assertEqual(MockBroadcast.broadcast.call_count, 1)

        # ws.send should have been called twice (form messages)
        ws_send_calls = [c[0][0] for c in mock_ws.send.call_args_list]
        self.assertIn(form_msg, ws_send_calls)
        self.assertIn(form_msg2, ws_send_calls)
        self.assertEqual(len(ws_send_calls), 2)

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_stdio_batch_unpacked_and_forwarded_to_broadcast(self, MockBroadcast):
        batch_msg = {
            "type": "stdio_batch",
            "payload": [
                {
                    "type": "stdout",
                    "log": "line1",
                    "execution_id": "e1",
                    "stage_id": "s1",
                },
                {
                    "type": "stderr",
                    "log": "line2",
                    "execution_id": "e1",
                    "stage_id": "s1",
                },
            ],
        }
        mock_conn = _make_mock_conn([batch_msg])
        mock_ws = _make_mock_ws()

        bind_ws_with_connection(mock_ws, mock_conn, block=False)
        time.sleep(0.5)

        # Batch of 2 items should produce 2 individual broadcast calls
        self.assertEqual(MockBroadcast.broadcast.call_count, 2)
        for call in MockBroadcast.broadcast.call_args_list:
            msg = json.loads(call[1]["msg"])
            self.assertEqual(msg["type"], "stdio")
            self.assertIn("payload", msg)

        # Should NOT be sent to ws.send
        mock_ws.send.assert_not_called()

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_broadcast_error_does_not_break_form_messages(self, MockBroadcast):
        MockBroadcast.broadcast.side_effect = Exception("WebSocket broadcast failed")

        stdio_msg = {"type": "stdio", "payload": {"type": "stdout", "log": "hello"}}
        form_msg = '{"type": "form:update", "payload": {}}'
        mock_conn = _make_mock_conn([stdio_msg, form_msg])
        mock_ws = _make_mock_ws()

        bind_ws_with_connection(mock_ws, mock_conn, block=False)
        time.sleep(0.5)

        # Even if broadcast fails, form messages should still be sent to ws
        mock_ws.send.assert_called_once_with(form_msg)

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_execution_ended_triggers_cleanup_and_forwarded_to_ws(self, MockBroadcast):
        ended_msg = json.dumps({"type": "execution:ended", "execution_id": "e1"})
        mock_conn = _make_mock_conn([ended_msg])
        mock_ws = _make_mock_ws()

        bind_ws_with_connection(mock_ws, mock_conn, block=False)
        time.sleep(0.5)

        # execution:ended SHOULD be sent to the browser WebSocket so frontend knows execution ended
        mock_ws.send.assert_called_once_with(ended_msg)
        # Should NOT go to BroadcastController
        MockBroadcast.broadcast.assert_not_called()

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_execution_ended_after_logs_still_broadcasts_logs(self, MockBroadcast):
        stdio_msg = {"type": "stdio", "payload": {"type": "stdout", "log": "hello"}}
        ended_msg = json.dumps({"type": "execution:ended", "execution_id": "e1"})
        mock_conn = _make_mock_conn([stdio_msg, ended_msg])
        mock_ws = _make_mock_ws()

        bind_ws_with_connection(mock_ws, mock_conn, block=False)
        time.sleep(0.5)

        # stdio message should have been broadcast
        MockBroadcast.broadcast.assert_called_once()
        # execution:ended SHOULD be sent to ws so frontend knows execution ended
        mock_ws.send.assert_called_once_with(ended_msg)

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_cleanup_broadcasts_execution_update_when_conn_has_execution_id(
        self, MockBroadcast
    ):
        """When do_cleanup runs and conn has execution_id, it broadcasts execution:update."""
        form_msg = '{"type": "form:update", "payload": {}}'
        ended_msg = json.dumps({"type": "execution:ended", "execution_id": "e1"})
        mock_conn = _make_mock_conn([form_msg, ended_msg], execution_id="e1")
        mock_ws = _make_mock_ws()

        bind_ws_with_connection(mock_ws, mock_conn, block=False)
        time.sleep(0.5)

        # Form msg and execution:ended both go to ws.send
        ws_send_calls = mock_ws.send.call_args_list
        self.assertEqual(len(ws_send_calls), 2)
        self.assertEqual(ws_send_calls[0][0][0], form_msg)
        self.assertEqual(ws_send_calls[1][0][0], ended_msg)

        # execution:ended triggers do_cleanup which broadcasts execution:update
        broadcast_calls = MockBroadcast.broadcast.call_args_list
        self.assertEqual(len(broadcast_calls), 1)
        broadcast_msg = json.loads(broadcast_calls[0][1]["msg"])
        self.assertEqual(broadcast_msg["type"], "execution:update")
        self.assertEqual(broadcast_msg["payload"]["execution_id"], "e1")

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_no_execution_update_when_conn_has_no_execution_id(self, MockBroadcast):
        """When conn has no execution_id, do_cleanup does NOT broadcast execution:update."""
        ended_msg = json.dumps({"type": "execution:ended", "execution_id": "e1"})
        mock_conn = _make_mock_conn([ended_msg], execution_id=None)
        mock_ws = _make_mock_ws()

        bind_ws_with_connection(mock_ws, mock_conn, block=False)
        time.sleep(0.5)

        # execution:ended SHOULD be sent to ws so frontend knows execution ended
        mock_ws.send.assert_called_once_with(ended_msg)
        # But no broadcast since conn has no execution_id
        MockBroadcast.broadcast.assert_not_called()

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_logs_broadcast_then_execution_update_on_ended(self, MockBroadcast):
        """stdio messages are broadcast, then execution:ended triggers execution:update."""
        stdio_msg = {"type": "stdio", "payload": {"type": "stdout", "log": "hello"}}
        ended_msg = json.dumps({"type": "execution:ended", "execution_id": "e1"})
        mock_conn = _make_mock_conn([stdio_msg, ended_msg], execution_id="e1")
        mock_ws = _make_mock_ws()

        bind_ws_with_connection(mock_ws, mock_conn, block=False)
        time.sleep(0.5)

        # 2 broadcasts: stdio + execution:update from do_cleanup
        self.assertEqual(MockBroadcast.broadcast.call_count, 2)

        msg1 = json.loads(MockBroadcast.broadcast.call_args_list[0][1]["msg"])
        self.assertEqual(msg1["type"], "stdio")

        msg2 = json.loads(MockBroadcast.broadcast.call_args_list[1][1]["msg"])
        self.assertEqual(msg2["type"], "execution:update")
        self.assertEqual(msg2["payload"]["execution_id"], "e1")

        # execution:ended SHOULD go to ws so frontend knows execution ended
        mock_ws.send.assert_called_once_with(ended_msg)


class TestWebSocketBroadcastGating(unittest.TestCase):
    """Tests that BroadcastController.broadcast() is NOT called in client_loop
    when WORKER_LOG_TO_QUEUE=true (fanout consumer handles it instead)."""

    @patch("abstra_internals.utils.websockets.WORKER_LOG_TO_QUEUE", True)
    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_stdio_not_broadcast_when_flag_on(self, MockBroadcast):
        """With WORKER_LOG_TO_QUEUE=true, stdio messages should NOT be broadcast from client_loop."""
        stdio_msg = {"type": "stdio", "payload": {"type": "stdout", "log": "hello"}}
        mock_conn = _make_mock_conn([stdio_msg])
        mock_ws = _make_mock_ws()

        bind_ws_with_connection(mock_ws, mock_conn, block=False)
        time.sleep(0.5)

        # BroadcastController.broadcast should NOT be called from client_loop
        # (the fanout consumer handles it)
        MockBroadcast.broadcast.assert_not_called()

        # stdio should still NOT be sent to ws (intercepted and skipped)
        mock_ws.send.assert_not_called()

    @patch("abstra_internals.utils.websockets.WORKER_LOG_TO_QUEUE", True)
    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_stdio_batch_not_broadcast_when_flag_on(self, MockBroadcast):
        """With WORKER_LOG_TO_QUEUE=true, stdio_batch should NOT be broadcast from client_loop."""
        batch_msg = {
            "type": "stdio_batch",
            "payload": [
                {"type": "stdout", "log": "line1"},
                {"type": "stderr", "log": "line2"},
            ],
        }
        mock_conn = _make_mock_conn([batch_msg])
        mock_ws = _make_mock_ws()

        bind_ws_with_connection(mock_ws, mock_conn, block=False)
        time.sleep(0.5)

        MockBroadcast.broadcast.assert_not_called()
        mock_ws.send.assert_not_called()

    @patch("abstra_internals.utils.websockets.WORKER_LOG_TO_QUEUE", True)
    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_task_not_broadcast_from_client_loop(self, MockBroadcast):
        """With WORKER_LOG_TO_QUEUE=true, task messages should NOT be broadcast from client_loop
        (fanout consumer handles it instead)."""
        task_msg = {"type": "task", "payload": {"id": "t1", "status": "pending"}}
        mock_conn = _make_mock_conn([task_msg])
        mock_ws = _make_mock_ws()

        bind_ws_with_connection(mock_ws, mock_conn, block=False)
        time.sleep(0.5)

        MockBroadcast.broadcast.assert_not_called()
        mock_ws.send.assert_not_called()


if __name__ == "__main__":
    unittest.main()
