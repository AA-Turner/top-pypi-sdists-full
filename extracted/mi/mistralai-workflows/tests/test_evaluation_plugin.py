"""Tests for the evaluation plugin using in-process Temporal."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from mistralai.workflows import get_workflow_definition, workflow
from mistralai.workflows.core.execution.concurrency import ParallelExecutionWorkflow
from mistralai.workflows.plugins.evaluation import evaluation
from mistralai.workflows.plugins.evaluation._activities import (
    _get_obs_client_factory,
    setup_evaluation_run,
    upload_input_records,
    upload_output_records,
)
from mistralai.workflows.plugins.evaluation.types import Evaluator, Score

from .utils import create_test_worker


def _make_mock_obs_client() -> MagicMock:
    """Build a mock observability client that satisfies all activity calls."""
    client = MagicMock()
    beta = AsyncMock()
    client.evaluation.beta = beta
    client.evaluation._resolve_project_slug = AsyncMock(return_value="test-project")
    client.evaluation._resolve_evaluation_slug = AsyncMock(return_value=("test-eval", "test-project"))
    client.evaluation._build_run_url = MagicMock(return_value="https://console.mistral.ai/eval/run/test-run-id")

    # get_or_create returns an object with .slug
    eval_response = MagicMock()
    eval_response.slug = "test-eval"
    beta.get_or_create = AsyncMock(return_value=eval_response)

    # create_run returns an object with .id and .evaluators
    evaluator_obj = MagicMock()
    evaluator_obj.name = "accuracy"
    evaluator_obj.id = "evaluator-id-1"
    run_response = MagicMock()
    run_response.id = "test-run-id"
    run_response.evaluators = [evaluator_obj]
    beta.create_run = AsyncMock(return_value=run_response)

    beta.upload_input_records = AsyncMock()
    beta.upload_output_records = AsyncMock()

    return client


# -- Task and scorer definitions for tests --


@evaluation.task
async def echo_task(input_record: dict) -> str:
    return input_record.get("text", "no text")


@evaluation.task
async def failing_task(input_record: dict) -> str:
    if input_record.get("should_fail"):
        raise ValueError("Intentional failure")
    return input_record.get("text", "ok")


@evaluation.scorer
async def always_one_scorer(input_record: dict, output: str) -> Score:
    return Score(value=1.0, rationale="always 1")


# -- Wrapper workflow that calls evaluation.run() --


@workflow.define(name="test-eval-workflow")
class EvalWorkflow:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=echo_task,
            evaluators=[Evaluator(name="accuracy", scorer=always_one_scorer)],
        )
        return {"run_id": result.run_id, "run_url": result.run_url}


@workflow.define(name="test-eval-workflow-with-failures")
class EvalWorkflowWithFailures:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=failing_task,
            evaluators=[Evaluator(name="accuracy", scorer=always_one_scorer)],
        )
        return {"run_id": result.run_id, "run_url": result.run_url}


# -- Tests --


_EVAL_ACTIVITIES = [setup_evaluation_run, upload_input_records, upload_output_records]


def _create_test_worker_with_mock_obs(temporal_env, workflows, activities):
    """Create a test worker that injects a mock obs client factory via DI override."""
    from mistralai.workflows.core.dependencies.dependency_injector import DependencyInjector

    mock_client = _make_mock_obs_client()
    injector = DependencyInjector.get_singleton_instance()

    # Save original DI state
    original_ctx = injector._dependencies_ctx.copy()

    # Override the factory DI to return a callable that always gives our mock
    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def mock_factory_ctx():
        yield lambda **kwargs: mock_client

    injector._dependencies_ctx[_get_obs_client_factory] = mock_factory_ctx

    class _OverrideContext:
        async def __aenter__(self):
            worker_ctx = create_test_worker(
                temporal_env,
                workflows=[*workflows, ParallelExecutionWorkflow],
                activities=activities,
            )
            self._worker_ctx = worker_ctx
            self._worker = await worker_ctx.__aenter__()
            return self._worker

        async def __aexit__(self, *args):
            await self._worker_ctx.__aexit__(*args)
            # Restore original DI state
            injector._dependencies_ctx = original_ctx

    return _OverrideContext()


class TestEvaluationPlugin:
    @pytest.mark.asyncio
    async def test_basic_evaluation_run(self, temporal_env: Any) -> None:
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflow],
            activities=[echo_task, always_one_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflow)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {
                    "params": {
                        "dataset": [
                            {"text": "hello"},
                            {"text": "world"},
                        ],
                    },
                },
                id="test-eval-basic",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["run_id"] == "test-run-id"
            assert result["result"]["run_url"] is not None

    @pytest.mark.asyncio
    async def test_evaluation_with_task_failure(self, temporal_env: Any) -> None:
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowWithFailures],
            activities=[failing_task, always_one_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflowWithFailures)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {
                    "params": {
                        "dataset": [
                            {"text": "good", "should_fail": False},
                            {"text": "bad", "should_fail": True},
                            {"text": "also good", "should_fail": False},
                        ],
                    },
                },
                id="test-eval-failure",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            # The evaluation should complete despite one task failing
            assert result["result"]["run_id"] == "test-run-id"
