"""Adversarial / negative tests for the dataclass Serializable.

The golden and differential tests only exercise well-formed input. These assert the
constructor / ``model_validate`` REJECTS malformed input the way pydantic did (so the
repositories' ``try/except`` skip-and-log path still fires and no illegal wire is
emitted), and ACCEPTS the wider set of ISO datetime formats pydantic accepted.

These lock in the fixes from the cross-AI review (None into a required field, str
fed to a list, invalid Literal / discriminator, strict datetime format).
"""

import unittest

from abstra_internals.entities.execution import Execution
from abstra_internals.entities.execution_context import (
    FormContext,
    HookContext,
    Request,
    Response,
)
from abstra_internals.repositories.models import PreExecution
from abstra_internals.repositories.tasks import TaskDTO

_HOOK_WIRE = {
    "type": "hook",
    "request": {"method": "GET", "queryParams": {}, "headers": {}, "body": ""},
    "response": {"headers": {}, "status": 200, "body": ""},
    "sentTasks": [],
    "legacyThreadData": {},
    "mockExecution": {"testPendingTasks": [], "testRequest": None},
}


def _exec_wire(**over):
    w = {
        "id": "e1",
        "stageId": "s1",
        "status": "running",
        "pid": 1,
        "workerId": "w1",
        "createdAt": "2024-01-02T03:04:05.000000Z",
        "updatedAt": None,
        "context": _HOOK_WIRE,
    }
    w.update(over)
    return w


class RejectsMalformedInput(unittest.TestCase):
    def test_none_for_required_union_raises(self):
        with self.assertRaises((ValueError, TypeError)):
            PreExecution.model_validate(
                {"stageId": "s", "context": None, "executionId": "e"}
            )

    def test_unreconstructable_context_raises(self):
        with self.assertRaises((ValueError, TypeError)):
            PreExecution.model_validate(
                {"stageId": "s", "context": 5, "executionId": "e"}
            )

    def test_str_for_list_field_raises(self):
        bad = dict(_HOOK_WIRE, sentTasks="ab")  # would silently become ["a","b"]
        with self.assertRaises((ValueError, TypeError)):
            HookContext.model_validate(bad)

    def test_invalid_literal_raises(self):
        # type "hook" is not valid for FormContext (Literal["form"])
        with self.assertRaises((ValueError, TypeError)):
            FormContext.model_validate(dict(_HOOK_WIRE, type="hook"))

    def test_invalid_status_literal_raises(self):
        with self.assertRaises((ValueError, TypeError)):
            Execution.model_validate(_exec_wire(status="bogus"))

    def test_missing_required_field_raises(self):
        with self.assertRaises((ValueError, TypeError)):
            Response.model_validate({"status": 200})  # missing headers, body


class AcceptsValidInput(unittest.TestCase):
    def test_none_for_optional_ok(self):
        # updated_at is Optional -> None allowed; locked/completed Optional too.
        e = Execution.model_validate(_exec_wire(updatedAt=None))
        self.assertIsNone(e.updated_at)
        t = TaskDTO.model_validate(
            {
                "id": "t",
                "type": "x",
                "payload": {},
                "status": "pending",
                "targetStageId": "s",
                "created": {"at": "now", "byExecutionId": None, "byStageId": None},
                "locked": None,
                "completed": None,
            }
        )
        self.assertIsNone(t.locked)

    def test_tolerant_datetime_formats_accepted(self):
        # pydantic accepted these; strict from_utc_iso_string would not.
        for dt in [
            "2024-01-02T03:04:05+00:00",  # no microseconds, +00:00
            "2024-01-02T03:04:05Z",  # no microseconds, Z
            "2024-01-02T03:04:05.123456+00:00",  # micros, +00:00
            "2024-01-02T03:04:05.000000Z",  # the canonical written form
        ]:
            with self.subTest(dt=dt):
                e = Execution.model_validate(_exec_wire(createdAt=dt))
                # re-serializes to the canonical .%fZ form
                self.assertTrue(e.dump()["createdAt"].endswith("Z"))

    def test_structured_body_still_encoded(self):
        r = Request.model_validate({"method": "POST", "body": {"a": 1}})
        self.assertEqual(r.body, '{"a": 1}')


if __name__ == "__main__":
    unittest.main()
