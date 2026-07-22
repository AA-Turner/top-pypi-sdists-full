"""Golden wire-format guard for the Serializable hierarchy.

The exact JSON produced by ``dump()``/``dump_json()`` is a wire contract: it is
written to the DB and to the queue and read back by cloud-api and by other
running deployments. This test freezes that output (fixture generated from the
original pydantic implementation) so the migration to plain dataclasses is
proven **byte-identical** — both the field VALUES (``dump()`` dict equality) and
the field ORDER (``dump_json()`` exact string).

If this test fails after a change, the wire format drifted — do not update the
fixture to make it pass unless the format change is intentional and coordinated
across every consumer.
"""

import datetime
import json
import os
import unittest

from abstra_internals.entities.execution import Execution
from abstra_internals.entities.execution_context import (
    CodeSnippetContext,
    CodeSnippetExecutionMock,
    FormContext,
    FormExecutionMock,
    HookContext,
    HookExecutionMock,
    JobContext,
    JobExecutionMock,
    PageContext,
    PageExecutionMock,
    Request,
    Response,
    ScriptContext,
    ScriptExecutionMock,
)
from abstra_internals.repositories.models import (
    PingMessage,
    PreExecution,
    RunSnippetMessage,
    RunSnippetSandboxedMessage,
    StopAllExecutionsMessage,
    StopExecutionMessage,
)
from abstra_internals.repositories.tasks import (
    ExecutionTasksResponse,
    TaskDTO,
    TaskEventDetails,
)

_FIXTURE = os.path.join(
    os.path.dirname(__file__), "_golden", "serializable_golden.json"
)

DT1 = datetime.datetime(2024, 1, 2, 3, 4, 5, tzinfo=datetime.timezone.utc)
DT2 = datetime.datetime(2024, 6, 7, 8, 9, 10, tzinfo=datetime.timezone.utc)


def _task_event(at="2024-01-02T03:04:05+00:00"):
    return TaskEventDetails(at=at, by_execution_id="exec-1", by_stage_id="stage-1")


def _task_dto(tid="task-1"):
    return TaskDTO(
        id=tid,
        type="my_task",
        payload={"k": "v", "n": 1},
        status="pending",
        target_stage_id="stage-x",
        created=_task_event(),
        locked=None,
        completed=None,
    )


def build_instances():
    """The canonical set of representative instances — MUST match the generator
    used to produce the fixture. Keyed by the fixture's names."""
    req = Request(
        method="POST",
        query_params={"c": "3"},
        headers={"auth": "secret"},
        body='{"a": 1}',
    )
    resp = Response(headers={"X": "y"}, status=200, body="ok")
    return {
        "Request": req,
        # dict body is intentionally passed to exercise the before-validator that
        # JSON-encodes structured input into the str field.
        "Request_structured_body": Request(method="POST", body={"a": 1}),  # type: ignore[arg-type]
        "Response": resp,
        "HookExecutionMock": HookExecutionMock(test_request=req),
        "FormExecutionMock": FormExecutionMock(test_answers=["a", None]),
        "ScriptExecutionMock": ScriptExecutionMock(test_trigger_task=_task_dto()),
        "JobExecutionMock": JobExecutionMock(test_pending_tasks=[_task_dto()]),
        "PageExecutionMock": PageExecutionMock(),
        "CodeSnippetExecutionMock": CodeSnippetExecutionMock(),
        "HookContext": HookContext(request=req, response=resp),
        "FormContext": FormContext(request=req),
        "ScriptContext": ScriptContext(task_id="task-123"),
        "JobContext": JobContext(),
        "PageContext": PageContext(request=req, response=resp, page_path="/p"),
        "CodeSnippetContext": CodeSnippetContext(),
        "TaskEventDetails": _task_event(),
        "TaskDTO": _task_dto(),
        "ExecutionTasksResponse": ExecutionTasksResponse(
            trigger_task=_task_dto("t-trigger"), sent_tasks=[_task_dto("t-sent")]
        ),
        "PreExecution": PreExecution(
            stage_id="s1",
            context=HookContext(request=req, response=resp),
            execution_id="e1",
            user_jwt="jwt",
            send_queue="sq",
            recv_queue="rq",
            queue_expire_ms=1000,
        ),
        "StopExecutionMessage": StopExecutionMessage.create(execution_id="e1"),
        "StopAllExecutionsMessage": StopAllExecutionsMessage(),
        "RunSnippetMessage": RunSnippetMessage.create(code="print(1)"),
        "RunSnippetSandboxedMessage": RunSnippetSandboxedMessage.create(
            code="print(1)", queue_expire_ms=5000, timeout_ms=1000
        ),
        "PingMessage": PingMessage(),
        "Execution": Execution(
            id="exec-1",
            stage_id="stage-1",
            status="running",
            pid=1234,
            worker_id="w1",
            created_at=DT1,
            updated_at=DT2,
            context=HookContext(request=req, response=resp),
        ),
        "Execution_no_updated": Execution(
            id="exec-2",
            stage_id="stage-2",
            status="finished",
            pid=1,
            worker_id="w2",
            created_at=DT1,
            updated_at=None,
            context=ScriptContext(task_id="t9"),
        ),
    }


class SerializableGoldenTest(unittest.TestCase):
    def setUp(self):
        with open(_FIXTURE, encoding="utf-8") as f:
            self.golden = json.load(f)
        self.instances = build_instances()

    def test_fixture_and_instances_cover_the_same_classes(self):
        self.assertEqual(set(self.golden), set(self.instances))

    def test_dump_matches_golden_values(self):
        for name, obj in self.instances.items():
            with self.subTest(name=name):
                self.assertEqual(obj.dump(), self.golden[name]["dump"])

    def test_dump_json_matches_golden_bytes(self):
        for name, obj in self.instances.items():
            with self.subTest(name=name):
                self.assertEqual(obj.dump_json(), self.golden[name]["dump_json"])


if __name__ == "__main__":
    unittest.main()
