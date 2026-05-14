import json
from datetime import datetime, timezone
from unittest import TestCase
from unittest.mock import patch

from abstra_internals.logger import AbstraLogger


class LifecycleTest(TestCase):
    """Pins the on-the-wire JSON contract that Fluent Bit's Merge_Log
    (and downstream Kibana queries on `log_processed.fields.*`) depend on.
    """

    def _capture(self, message, attrs=None):
        with patch("abstra_internals.logger.os.write") as mock_write:
            AbstraLogger.lifecycle(message, attrs)
        self.assertEqual(mock_write.call_count, 1)
        fd, payload = mock_write.call_args[0]
        self.assertEqual(fd, 1)
        line = payload.decode("utf-8")
        self.assertTrue(line.endswith("\n"))
        return json.loads(line.rstrip("\n"))

    def test_emits_tracing_subscriber_shape(self):
        before = datetime.now(timezone.utc)
        parsed = self._capture(
            "[RUN abc] Job trigger received",
            {"executionId": "abc", "projectId": "p1", "stage": "trigger.received"},
        )
        self.assertEqual(parsed["level"], "INFO")
        self.assertEqual(parsed["target"], "abstra_internal")
        self.assertEqual(
            parsed["fields"],
            {
                "message": "[RUN abc] Job trigger received",
                "executionId": "abc",
                "projectId": "p1",
                "stage": "trigger.received",
            },
        )
        # ISO8601, parseable, and not in the past
        ts = datetime.fromisoformat(parsed["timestamp"].replace("Z", "+00:00"))
        self.assertGreaterEqual(ts, before)

    def test_omits_none_attribute_values(self):
        parsed = self._capture(
            "msg",
            {"executionId": "abc", "empty": None, "alsoEmpty": None},
        )
        self.assertEqual(parsed["fields"], {"message": "msg", "executionId": "abc"})

    def test_emits_message_only_payload_when_attrs_missing(self):
        parsed = self._capture("plain message")
        self.assertEqual(parsed["fields"], {"message": "plain message"})

    def test_non_json_serializable_attr_falls_back_to_str(self):
        class Opaque:
            def __str__(self):
                return "opaque-repr"

        parsed = self._capture("msg", {"obj": Opaque()})
        self.assertEqual(parsed["fields"]["obj"], "opaque-repr")

    def test_writes_directly_to_fd1_bypassing_sys_stdout(self):
        # Even if sys.stdout.write is monkey-patched (as StdioPatcher does in
        # the executor subprocess), lifecycle still emits via os.write(1, …).
        import sys

        original_write = sys.stdout.write
        captured_via_stdout = []

        def fake_write(s):
            captured_via_stdout.append(s)
            return len(s)

        sys.stdout.write = fake_write
        try:
            with patch("abstra_internals.logger.os.write") as mock_write:
                AbstraLogger.lifecycle("msg", {"executionId": "abc"})
            mock_write.assert_called_once()
            # sys.stdout.write must NOT have been used — that's the whole point.
            self.assertEqual(captured_via_stdout, [])
        finally:
            sys.stdout.write = original_write
