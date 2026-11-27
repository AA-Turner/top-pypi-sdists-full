import asyncio
import logging
from collections.abc import Iterator

import pytest
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core.tracing._otel_config import _WorkflowRunFilter
from mistralai.workflows.testing import create_test_worker

from .fixtures import PureWorkflow


class _CapturingHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__(level=logging.DEBUG)
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)


@pytest.fixture
def captured_records() -> Iterator[list[logging.LogRecord]]:
    handler = _CapturingHandler()
    handler.addFilter(_WorkflowRunFilter())
    root = logging.getLogger()
    root.addHandler(handler)
    try:
        yield handler.records
    finally:
        root.removeHandler(handler)


async def _wait_for_workflow_task_failure_log(records: list[logging.LogRecord]) -> logging.LogRecord:
    while True:
        for record in records:
            if record.getMessage().startswith("Failed activation on workflow"):
                return record
        await asyncio.sleep(0.05)


class TestWorkflowTaskFailureLog:
    @pytest.mark.asyncio
    async def test_failure_log_carries_workflow_ids(
        self, temporal_env: WorkflowEnvironment, captured_records: list[logging.LogRecord]
    ) -> None:
        async with create_test_worker(temporal_env, workflows=[PureWorkflow]):
            handle = await temporal_env.client.start_workflow(
                "pure_workflow",
                {"unexpected_field": 1},
                id="workflow-task-failure-log",
                task_queue="test-task-queue",
            )
            record = await asyncio.wait_for(_wait_for_workflow_task_failure_log(captured_records), timeout=30)
            await handle.terminate()

        assert getattr(record, "workflowExecutionID", None) == "workflow-task-failure-log"
        assert getattr(record, "workflowRunID", None) == handle.result_run_id
        assert getattr(record, "workflowName", None) == "pure_workflow"
        assert record.exc_info is not None
