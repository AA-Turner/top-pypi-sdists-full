from typing import Any
from unittest.mock import patch

import pytest
from pydantic import BaseModel

from mistralai.workflows import activity, get_sticky_worker_session, run_sticky_worker_session, workflow
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException

from .utils import create_test_worker


class WorkflowParams(BaseModel):
    n_activities: int


class WorkflowResult(BaseModel):
    worker_ids: list[str]
    unique_workers: int


@activity(sticky_to_worker=True)
async def sticky_activity(worker_id: str) -> str:
    return worker_id


@workflow.define(name="test-sticky-session-implicit")
class ImplicitStickySessionWorkflow:
    """Workflow that uses implicit sticky session (auto-created)."""

    @workflow.entrypoint
    async def run(self, params: WorkflowParams) -> WorkflowResult:
        worker_ids = []

        async with run_sticky_worker_session():
            for _ in range(params.n_activities):
                worker_id = await sticky_activity("test-worker-1")
                worker_ids.append(worker_id)

        return WorkflowResult(
            worker_ids=worker_ids,
            unique_workers=len(set(worker_ids)),
        )


@workflow.define(name="test-sticky-session-explicit")
class ExplicitStickySessionWorkflow:
    """Workflow that uses explicit sticky session (captured and reused)."""

    @workflow.entrypoint
    async def run(self, params: WorkflowParams) -> WorkflowResult:
        worker_ids = []

        session = await get_sticky_worker_session()

        # First batch with session
        async with run_sticky_worker_session(session):
            for _ in range(params.n_activities):
                worker_id = await sticky_activity("test-worker-1")
                worker_ids.append(worker_id)

        # Second batch with same session
        async with run_sticky_worker_session(session):
            for _ in range(params.n_activities):
                worker_id = await sticky_activity("test-worker-1")
                worker_ids.append(worker_id)

        return WorkflowResult(
            worker_ids=worker_ids,
            unique_workers=len(set(worker_ids)),
        )


class TestStickyWorkerSession:
    @pytest.mark.asyncio
    async def test_implicit_sticky_session_routes_to_same_worker(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ImplicitStickySessionWorkflow],
            activities=[sticky_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "test-sticky-session-implicit",
                WorkflowParams(n_activities=5),
                id="test-implicit-sticky-session",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert result["unique_workers"] == 1, "All sticky activities should run on the same worker"
            assert len(result["worker_ids"]) == 5

    @pytest.mark.asyncio
    async def test_explicit_sticky_session_reuses_worker_across_scopes(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ExplicitStickySessionWorkflow],
            activities=[sticky_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "test-sticky-session-explicit",
                WorkflowParams(n_activities=3),
                id="test-explicit-sticky-session",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            # Should execute 6 activities total (3 in each scope) all on same worker
            assert result["unique_workers"] == 1, "Same worker should be used across both scopes"
            assert len(result["worker_ids"]) == 6

    @pytest.mark.asyncio
    async def test_sticky_activity_without_session_raises_error(self, temporal_env: Any) -> None:
        with patch("mistralai.workflows.core.activity.temporalio.workflow.in_workflow", return_value=True):
            with pytest.raises(WorkflowsException) as exc_info:
                await sticky_activity("test-worker-1")

            assert exc_info.value.code == ErrorCode.STICKY_WORKER_SESSION_MISSING
            assert "sticky to worker but no task queue is set" in str(exc_info.value)
            assert "run_sticky_worker_session" in str(exc_info.value)
