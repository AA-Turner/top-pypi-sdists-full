from typing import Any

import pytest

from mistralai.workflows import get_workflow_definition, workflow
from mistralai.workflows.core.tracing._temporal_tracing_interceptor import (
    _deterministic_workflow_traceparent,
    get_temporal_tracing_interceptors,
)
from mistralai.workflows.models import SearchAttributes

from .utils import create_test_worker


@workflow.define(name="test-missing-trace-header-workflow")
class MissingTraceHeaderWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "ok"


def _trace_id_from_traceparent(traceparent: str) -> str:
    return traceparent.split("-")[1]


@pytest.mark.asyncio
async def test_missing_workflow_trace_header_uses_deterministic_trace_id(
    temporal_env: Any,
    mock_upsert_search_attributes: Any,
) -> None:
    async with create_test_worker(
        temporal_env,
        workflows=[MissingTraceHeaderWorkflow],
        activities=[],
        interceptors=get_temporal_tracing_interceptors(),
    ):
        workflow_def = get_workflow_definition(MissingTraceHeaderWorkflow)
        assert workflow_def is not None

        handle = await temporal_env.client.start_workflow(
            workflow_def.name,
            id="test-missing-trace-header",
            task_queue="test-task-queue",
        )
        await handle.result()
        description = await handle.describe()

    expected_trace_id = _trace_id_from_traceparent(
        _deterministic_workflow_traceparent(description.namespace, description.id, description.run_id)
    )
    upserted_attrs = mock_upsert_search_attributes.call_args.args[0]
    attrs = {pair.key.name: pair.value for pair in upserted_attrs}

    assert attrs[SearchAttributes.otel_trace_id] == expected_trace_id
    assert attrs[SearchAttributes.otel_trace_id] != "00000000000000000000000000000000"
