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
    upload_run_scores,
)
from mistralai.workflows.plugins.evaluation._record_workflow import EvalRecordWorkflow
from mistralai.workflows.plugins.evaluation.types import Evaluator, RunEvaluator, RunEvaluatorContext, Score

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
    run_response.run_evaluators = []
    beta.create_run = AsyncMock(return_value=run_response)

    beta.upload_input_records = AsyncMock()
    beta.upload_output_records = AsyncMock()
    beta.upload_run_scores = AsyncMock()

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


@evaluation.scorer
async def failing_scorer(input_record: dict, output: str) -> Score:
    if output == "fail_scorer":
        raise ValueError("Scorer intentional failure")
    return Score(value=1.0, rationale="ok")


@workflow.define(name="test-task-workflow")
class TaskWorkflow:
    """A workflow used as a task (instead of @evaluation.task)."""

    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        text = params.get("text", "no text")
        return {"result": f"workflow-{text}"}


@evaluation.run_scorer
async def mean_accuracy_run_scorer(context: RunEvaluatorContext) -> Score:
    values = []
    for record in context.records:
        for gen in record.output.generations:
            for score_list in gen.scores.values():
                for s in score_list:
                    if s.status == "success" and s.value is not None:
                        values.append(s.value)
    mean = sum(values) / len(values) if values else 0.0
    return Score(value=mean, rationale=f"Mean across {len(values)} scores")


@evaluation.run_scorer
async def failing_run_scorer(context: RunEvaluatorContext) -> Score:
    raise ValueError("Run scorer intentional failure")


# -- Wrapper workflows that call evaluation.run() --


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


@workflow.define(name="test-eval-workflow-with-run-evaluators")
class EvalWorkflowWithRunEvaluators:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=echo_task,
            evaluators=[Evaluator(name="accuracy", scorer=always_one_scorer)],
            run_evaluators=[RunEvaluator(name="mean_accuracy", scorer=mean_accuracy_run_scorer)],
        )
        return {
            "run_id": result.run_id,
            "run_url": result.run_url,
            "statistics": {k: v.model_dump() for k, v in result.statistics.items()},
            "run_scores": {k: v.model_dump() for k, v in result.run_scores.items()},
        }


@workflow.define(name="test-eval-workflow-task-as-workflow")
class EvalWorkflowTaskAsWorkflow:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=TaskWorkflow,
            evaluators=[Evaluator(name="accuracy", scorer=always_one_scorer)],
        )
        return {"run_id": result.run_id, "run_url": result.run_url}


@workflow.define(name="test-eval-workflow-scorer-failure")
class EvalWorkflowScorerFailure:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=echo_task,
            evaluators=[Evaluator(name="flaky", scorer=failing_scorer)],
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


@workflow.define(name="test-eval-workflow-local")
class EvalWorkflowLocal:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=echo_task,
            evaluators=[Evaluator(name="accuracy", scorer=always_one_scorer)],
            run_evaluators=[RunEvaluator(name="mean_accuracy", scorer=mean_accuracy_run_scorer)],
            local=True,
        )
        return {
            "run_id": result.run_id,
            "run_url": result.run_url,
            "statistics": {k: v.model_dump() for k, v in result.statistics.items()},
            "run_scores": {k: v.model_dump() for k, v in result.run_scores.items()},
        }


@workflow.define(name="test-eval-workflow-run-evaluator-failure")
class EvalWorkflowRunEvaluatorFailure:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=echo_task,
            evaluators=[Evaluator(name="accuracy", scorer=always_one_scorer)],
            run_evaluators=[
                RunEvaluator(name="failing", scorer=failing_run_scorer),
                RunEvaluator(name="mean_accuracy", scorer=mean_accuracy_run_scorer),
            ],
        )
        return {
            "run_id": result.run_id,
            "run_scores": {k: v.model_dump() for k, v in result.run_scores.items()},
        }


# -- Tests --


_EVAL_ACTIVITIES = [setup_evaluation_run, upload_input_records, upload_output_records, upload_run_scores]


def _make_mock_obs_client_with_run_evaluators(
    run_evaluator_names: list[str] | None = None,
) -> MagicMock:
    """Build a mock obs client that also supports run evaluators."""
    client = _make_mock_obs_client()
    names = run_evaluator_names or ["mean_accuracy"]
    run_evaluator_objs = []
    for i, name in enumerate(names):
        obj = MagicMock()
        obj.name = name
        obj.id = f"run-evaluator-id-{i + 1}"
        run_evaluator_objs.append(obj)
    run_response = client.evaluation.beta.create_run.return_value
    run_response.run_evaluators = run_evaluator_objs
    return client


def _create_test_worker_with_mock_obs(temporal_env, workflows, activities, mock_client=None):
    """Create a test worker that injects a mock obs client factory via DI override."""
    from mistralai.workflows.core.dependencies.dependency_injector import DependencyInjector

    if mock_client is None:
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
                workflows=[*workflows, ParallelExecutionWorkflow, EvalRecordWorkflow],
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

    @pytest.mark.asyncio
    async def test_evaluation_with_run_evaluators(self, temporal_env: Any) -> None:
        mock_client = _make_mock_obs_client_with_run_evaluators()
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowWithRunEvaluators],
            activities=[echo_task, always_one_scorer, mean_accuracy_run_scorer, *_EVAL_ACTIVITIES],
            mock_client=mock_client,
        ):
            workflow_def = get_workflow_definition(EvalWorkflowWithRunEvaluators)
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
                id="test-eval-run-evaluators",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["run_id"] == "test-run-id"
            assert result["result"]["run_url"] is not None
            # Statistics computed from canonical objects
            assert "accuracy" in result["result"]["statistics"]
            # Run scores are full _Score dicts with value, status, rationale
            run_score = result["result"]["run_scores"]["mean_accuracy"]
            assert run_score["value"] == 1.0
            assert run_score["status"] == "success"
            assert "Mean across" in run_score["rationale"]

    @pytest.mark.asyncio
    async def test_evaluation_task_as_workflow(self, temporal_env: Any) -> None:
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowTaskAsWorkflow, TaskWorkflow],
            activities=[always_one_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflowTaskAsWorkflow)
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
                id="test-eval-task-as-workflow",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["run_id"] == "test-run-id"
            assert result["result"]["run_url"] is not None

    @pytest.mark.asyncio
    async def test_evaluation_with_scorer_failure(self, temporal_env: Any) -> None:
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowScorerFailure],
            activities=[echo_task, failing_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflowScorerFailure)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {
                    "params": {
                        "dataset": [
                            {"text": "ok"},
                            {"text": "fail_scorer"},
                        ],
                    },
                },
                id="test-eval-scorer-failure",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            # The evaluation completes despite a scorer failing
            assert result["result"]["run_id"] == "test-run-id"

    @pytest.mark.asyncio
    async def test_evaluation_local_mode(self, temporal_env: Any) -> None:
        """local=True keeps Temporal topology but skips Observability API calls."""
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowLocal],
            activities=[echo_task, always_one_scorer, mean_accuracy_run_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflowLocal)
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
                id="test-eval-local",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["run_id"] == "local"
            assert result["result"]["run_url"] is None
            # Statistics and run evaluators still computed
            assert "accuracy" in result["result"]["statistics"]
            run_score = result["result"]["run_scores"]["mean_accuracy"]
            assert run_score["value"] == 1.0
            assert run_score["status"] == "success"

    @pytest.mark.asyncio
    async def test_evaluation_run_evaluator_failure(self, temporal_env: Any) -> None:
        """A failing run evaluator is encoded as error, following ones still execute."""
        mock_client = _make_mock_obs_client_with_run_evaluators(
            run_evaluator_names=["failing", "mean_accuracy"],
        )
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowRunEvaluatorFailure],
            activities=[
                echo_task,
                always_one_scorer,
                failing_run_scorer,
                mean_accuracy_run_scorer,
                *_EVAL_ACTIVITIES,
            ],
            mock_client=mock_client,
        ):
            workflow_def = get_workflow_definition(EvalWorkflowRunEvaluatorFailure)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {
                    "params": {
                        "dataset": [
                            {"text": "hello"},
                        ],
                    },
                },
                id="test-eval-run-evaluator-failure",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["run_id"] == "test-run-id"
            # First run evaluator failed but encoded as error score
            failing_score = result["result"]["run_scores"]["failing"]
            assert failing_score["status"] == "error"
            assert failing_score["value"] is None
            assert failing_score["error"] is not None
            # Second run evaluator still executed successfully
            mean_score = result["result"]["run_scores"]["mean_accuracy"]
            assert mean_score["status"] == "success"
            assert mean_score["value"] == 1.0
