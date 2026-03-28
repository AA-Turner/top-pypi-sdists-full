import json
import time
import unittest
from unittest.mock import MagicMock

from abstra_internals.entities.execution_context import Response


class TestDrainUntilResponse(unittest.TestCase):
    """Tests for the drain_until_response helper that skips stdio messages."""

    def _mock_connection(self, recv_sequence, poll_returns_true=True):
        conn = MagicMock()
        conn.recv = MagicMock(side_effect=recv_sequence)
        conn.poll = MagicMock(return_value=poll_returns_true)
        return conn

    def test_returns_dict_response_immediately(self):
        from abstra_internals.controllers.execution.drain import drain_until_response

        conn = self._mock_connection([{"headers": {}, "status": 200, "body": "ok"}])
        result = drain_until_response(conn)
        self.assertEqual(result, {"headers": {}, "status": 200, "body": "ok"})

    def test_returns_response_object_immediately(self):
        from abstra_internals.controllers.execution.drain import drain_until_response

        resp = Response(headers={}, status=200, body="ok")
        conn = self._mock_connection([resp])
        result = drain_until_response(conn)
        assert result is not None
        self.assertIsInstance(result, Response)
        self.assertEqual(result.body, "ok")

    def test_skips_single_stdio_batch(self):
        from abstra_internals.controllers.execution.drain import drain_until_response

        conn = self._mock_connection(
            [
                {"type": "stdio_batch", "payload": [{"type": "stdout", "log": "hi"}]},
                {"headers": {}, "status": 200, "body": "<h1>Page</h1>"},
            ]
        )
        result = drain_until_response(conn)
        assert result is not None
        self.assertEqual(result["body"], "<h1>Page</h1>")

    def test_skips_multiple_stdio_messages(self):
        from abstra_internals.controllers.execution.drain import drain_until_response

        conn = self._mock_connection(
            [
                {"type": "stdio_batch", "payload": []},
                {"type": "stdio", "payload": {"type": "stderr", "log": "warn"}},
                {"type": "stdio_batch", "payload": []},
                {"headers": {}, "status": 200, "body": "done"},
            ]
        )
        result = drain_until_response(conn)
        assert result is not None
        self.assertEqual(result["body"], "done")

    def test_parses_json_string_response(self):
        from abstra_internals.controllers.execution.drain import drain_until_response

        conn = self._mock_connection(
            [
                '{"headers": {}, "status": 200, "body": "from string"}',
            ]
        )
        result = drain_until_response(conn)
        assert result is not None
        self.assertIsInstance(result, dict)
        self.assertEqual(result["body"], "from string")

    def test_skips_stdio_batch_as_json_string(self):
        from abstra_internals.controllers.execution.drain import drain_until_response

        conn = self._mock_connection(
            [
                json.dumps({"type": "stdio_batch", "payload": []}),
                {"headers": {}, "status": 200, "body": "ok"},
            ]
        )
        result = drain_until_response(conn)
        assert result is not None
        self.assertEqual(result["body"], "ok")

    def test_returns_none_on_none_recv(self):
        from abstra_internals.controllers.execution.drain import drain_until_response

        conn = self._mock_connection([None])
        result = drain_until_response(conn)
        self.assertIsNone(result)

    def test_returns_unparseable_string_as_is(self):
        from abstra_internals.controllers.execution.drain import drain_until_response

        conn = self._mock_connection(["not valid json at all"])
        result = drain_until_response(conn)
        self.assertEqual(result, "not valid json at all")

    def test_returns_execution_ended_dict(self):
        from abstra_internals.controllers.execution.drain import drain_until_response

        conn = self._mock_connection(
            [
                {"type": "execution:ended", "data": {"exitStatus": "EXCEPTION"}},
            ]
        )
        result = drain_until_response(conn)
        assert result is not None
        self.assertEqual(result["type"], "execution:ended")

    def test_returns_stream_start_dict(self):
        from abstra_internals.controllers.execution.drain import drain_until_response

        conn = self._mock_connection(
            [
                {"__page_stream__": "start", "status": 200, "headers": {}},
            ]
        )
        result = drain_until_response(conn)
        assert result is not None
        self.assertEqual(result["__page_stream__"], "start")

    def test_timeout_returns_none(self):
        """When poll() times out (no messages), returns None."""
        from abstra_internals.controllers.execution.drain import drain_until_response

        conn = self._mock_connection([], poll_returns_true=False)
        start = time.monotonic()
        result = drain_until_response(conn, timeout=0.1)
        elapsed = time.monotonic() - start
        self.assertIsNone(result)
        self.assertLess(elapsed, 1.0)

    def test_timeout_while_draining_stdio(self):
        """If only stdio messages keep coming and we exceed timeout, returns None."""
        from abstra_internals.controllers.execution.drain import drain_until_response

        call_count = 0

        def fake_recv():
            nonlocal call_count
            call_count += 1
            return {"type": "stdio_batch", "payload": []}

        def fake_poll(timeout=0.0):
            return True

        conn = MagicMock()
        conn.recv = fake_recv
        conn.poll = fake_poll

        start = time.monotonic()
        result = drain_until_response(conn, timeout=0.3)
        elapsed = time.monotonic() - start

        self.assertIsNone(result)
        self.assertGreater(elapsed, 0.2)
        self.assertLess(elapsed, 1.0)
        self.assertGreater(call_count, 1)

    def test_many_stdio_messages_before_response_works(self):
        """More than 100 stdio messages should still work (no counter limit)."""
        from abstra_internals.controllers.execution.drain import drain_until_response

        messages = [{"type": "stdio_batch", "payload": []} for _ in range(200)]
        messages.append({"headers": {}, "status": 200, "body": "finally"})

        conn = self._mock_connection(messages)
        result = drain_until_response(conn, timeout=5.0)
        assert result is not None
        self.assertEqual(result["body"], "finally")


class TestNormalizeResponse(unittest.TestCase):
    """Tests for normalize_response helper."""

    def test_response_object_returned_as_is(self):
        from abstra_internals.controllers.execution.drain import normalize_response

        resp = Response(headers={"X": "1"}, status=201, body="created")
        result = normalize_response(resp)
        self.assertIs(result, resp)

    def test_dict_converted_to_response(self):
        from abstra_internals.controllers.execution.drain import normalize_response

        result = normalize_response(
            {
                "headers": {"Content-Type": "text/html"},
                "status": 200,
                "body": "<h1>OK</h1>",
            }
        )
        assert result is not None
        self.assertEqual(result.status, 200)
        self.assertEqual(result.body, "<h1>OK</h1>")
        self.assertEqual(result.headers, {"Content-Type": "text/html"})

    def test_dict_uses_defaults_for_missing_keys(self):
        from abstra_internals.controllers.execution.drain import normalize_response

        result = normalize_response({"custom": "value"})
        assert result is not None
        self.assertEqual(result.status, 200)
        self.assertEqual(result.body, "")
        self.assertEqual(result.headers, {})

    def test_string_returns_generic_500(self):
        from abstra_internals.controllers.execution.drain import normalize_response

        result = normalize_response("Traceback (most recent call last): ...")
        assert result is not None
        self.assertEqual(result.status, 500)
        self.assertEqual(result.body, "Internal Server Error")
        self.assertNotIn("Traceback", result.body)

    def test_none_returns_none(self):
        from abstra_internals.controllers.execution.drain import normalize_response

        self.assertIsNone(normalize_response(None))

    def test_unexpected_type_returns_none(self):
        from abstra_internals.controllers.execution.drain import normalize_response

        self.assertIsNone(normalize_response(42))
        self.assertIsNone(normalize_response([1, 2, 3]))
        self.assertIsNone(normalize_response(True))


class TestNormalizeResponseInternalMessages(unittest.TestCase):
    """Tests that normalize_response treats internal protocol messages
    (execution:ended, execution:started) as errors, not valid responses."""

    def test_execution_ended_exception_returns_500(self):
        from abstra_internals.controllers.execution.drain import normalize_response

        result = normalize_response(
            {"type": "execution:ended", "data": {"exitStatus": "EXCEPTION"}}
        )
        assert result is not None
        self.assertEqual(result.status, 500)
        self.assertEqual(result.body, "Internal Server Error")

    def test_execution_ended_finished_returns_500(self):
        from abstra_internals.controllers.execution.drain import normalize_response

        result = normalize_response(
            {"type": "execution:ended", "data": {"exitStatus": "FINISHED"}}
        )
        assert result is not None
        self.assertEqual(result.status, 500)
        self.assertEqual(result.body, "Internal Server Error")

    def test_execution_started_returns_500(self):
        from abstra_internals.controllers.execution.drain import normalize_response

        result = normalize_response({"type": "execution:started", "executionId": "abc"})
        assert result is not None
        self.assertEqual(result.status, 500)
        self.assertEqual(result.body, "Internal Server Error")


if __name__ == "__main__":
    unittest.main()
