"""Executor teardown must close agent tools leaked by user code.

Warm executors are reused across executions. If user code (or run_agent)
leaves a BrowserTools open, the playwright driver keeps an asyncio loop
marked as running on the executor thread and stacks Chromium/driver
processes on every reuse, eventually killing the executor mid-delivery
("Execution did not complete on a previous delivery")."""

import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.agents import lifecycle
from abstra_internals.controllers.execution.executor_process import handle_execute


class LeakedTool:
    def __init__(self):
        self.closed = False
        lifecycle.register_tool(self)

    def close(self):
        self.closed = True
        lifecycle.unregister_tool(self)


def _make_request():
    request = MagicMock()
    request.execution_id = "550e8400-e29b-41d4-a716-446655440000"
    request.worker_id = "worker-1"
    request.rabbitmq_params = None
    request.connection = MagicMock()
    request.stage.type_name = "job"
    request.user_jwt = None
    return request


class TestExecutorLeakedToolsCleanup(unittest.TestCase):
    def setUp(self):
        lifecycle.close_leaked_tools()
        self.state = MagicMock()
        self.state.is_warmed_up.return_value = True
        self.response_queue = MagicMock()

    def tearDown(self):
        lifecycle.close_leaked_tools()

    def _run(self, run_side_effect):
        with (
            patch(
                "abstra_internals.controllers.execution.executor_process.ExecutionController"
            ) as controller_cls,
            patch(
                "abstra_internals.controllers.execution.executor_process.make_client_from_context"
            ),
            patch(
                "abstra_internals.controllers.execution.executor_process.StdioPatcher"
            ),
            patch("abstra_internals.controllers.execution.executor_process.Settings"),
        ):
            controller_cls.return_value.run.side_effect = run_side_effect
            handle_execute(
                state=self.state,
                request=_make_request(),
                response_queue=self.response_queue,
                root_path="/tmp/project",
                server_port=3000,
            )

    def test_leaked_tool_is_closed_after_successful_execution(self):
        leaked = {}

        def run(**_kwargs):
            leaked["tool"] = LeakedTool()

        self._run(run)

        self.assertTrue(leaked["tool"].closed)
        self.assertEqual(lifecycle.open_tools_count(), 0)

    def test_execution_ended_is_sent_before_leaked_tools_are_closed(self):
        # A wedged Chromium can block BrowserTools.close() indefinitely
        # (playwright's close has no client-side timeout). The delivery
        # lifecycle — log flush and execution:ended — must not sit behind it.
        events = []

        class OrderedTool(LeakedTool):
            def close(self):
                events.append("tool_closed")
                super().close()

        request = _make_request()

        def record_send(payload):
            if "execution:ended" in payload:
                events.append("ended_sent")

        request.connection.send.side_effect = record_send

        with (
            patch(
                "abstra_internals.controllers.execution.executor_process.ExecutionController"
            ) as controller_cls,
            patch(
                "abstra_internals.controllers.execution.executor_process.make_client_from_context"
            ),
            patch(
                "abstra_internals.controllers.execution.executor_process.StdioPatcher"
            ),
            patch("abstra_internals.controllers.execution.executor_process.Settings"),
            patch(
                "abstra_internals.controllers.execution.executor_process.WORKER_LOG_TO_QUEUE",
                True,
            ),
            patch(
                "abstra_internals.controllers.execution.executor_process.web_editor_uses_db",
                return_value=False,
            ),
        ):
            controller_cls.return_value.run.side_effect = lambda **_: OrderedTool()
            handle_execute(
                state=self.state,
                request=request,
                response_queue=self.response_queue,
                root_path="/tmp/project",
                server_port=3000,
            )

        self.assertEqual(events, ["ended_sent", "tool_closed"])

    def test_leaked_tool_is_closed_when_user_code_raises(self):
        leaked = {}

        def run(**_kwargs):
            leaked["tool"] = LeakedTool()
            raise RuntimeError("user code exploded")

        self._run(run)

        self.assertTrue(leaked["tool"].closed)
        self.assertEqual(lifecycle.open_tools_count(), 0)
