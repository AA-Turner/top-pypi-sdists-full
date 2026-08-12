"""Tests for the evaluation plugin using in-process Temporal."""

from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from mistralai.workflows import get_workflow_definition, workflow
from mistralai.workflows.core.execution.concurrency import ParallelExecutionWorkflow
from mistralai.workflows.plugins.evaluation import evaluation
from mistralai.workflows.plugins.evaluation._activities import (
    _get_obs_client_factory,
    create_optimization,
    create_optimization_trial,
    patch_optimization,
    patch_optimization_trial,
    patch_optimization_trial_run,
    setup_evaluation_run,
    upload_input_records,
    upload_output_records,
    upload_run_scores,
)
from mistralai.workflows.plugins.evaluation._record_workflow import EvalRecordWorkflow
from mistralai.workflows.plugins.evaluation.types import (
    Evaluator,
    Goal,
    RunEvaluator,
    RunEvaluatorContext,
    Score,
    ScorerContext,
    System,
    TaskContext,
)

from .utils import create_test_worker


def _make_mock_obs_client() -> MagicMock:
    """Build a mock observability client that satisfies all activity calls."""
    client = MagicMock()
    beta = AsyncMock()
    client.evaluation.beta = beta
    client.evaluation._resolve_project_slug = AsyncMock(return_value="test-project")
    client.evaluation._resolve_evaluation_slug = AsyncMock(return_value=("test-eval", "test-project"))
    client.evaluation._build_run_url = MagicMock(return_value="https://console.mistral.ai/eval/run/test-run-id")
    client.evaluation._build_optimization_url = MagicMock(
        return_value="https://console.mistral.ai/eval/optimization/test-optimization-id"
    )

    # create/patch optimization endpoints (create-first optimize flow)
    optimization_response = MagicMock()
    optimization_response.id = "test-optimization-id"
    optimization_response.organization_id = "test-org"
    optimization_response.workspace_id = "test-workspace"
    client.evaluation._endpoints.create_optimization = AsyncMock(return_value=optimization_response)
    client.evaluation._endpoints.patch_optimization = AsyncMock(return_value=optimization_response)

    # create/patch trial + trial-run endpoints (trial-based persistence, OBS-2053)
    trial_response = MagicMock()
    trial_response.id = "test-trial-id"
    client.evaluation._endpoints.create_optimization_trial = AsyncMock(return_value=trial_response)
    client.evaluation._endpoints.patch_optimization_trial = AsyncMock(return_value=trial_response)
    client.evaluation._endpoints.patch_optimization_trial_run = AsyncMock(return_value=None)

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


@evaluation.task(execution_timeout=timedelta(seconds=2))
async def hanging_task(input_record: dict) -> str:
    if input_record.get("hang"):
        await asyncio.sleep(3600)
    return input_record.get("text", "ok")


@evaluation.task
async def system_task(input_record: dict, system: dict) -> str:
    """Task that uses the system params."""
    prefix = system.get("params", {}).get("prefix", "")
    return f"{prefix}: {input_record.get('text', 'no text')}"


@evaluation.task
async def optional_system_task(input_record: dict, system: dict | None) -> str:
    """Task that accepts system but handles None gracefully."""
    if system:
        prefix = system.get("params", {}).get("prefix", "")
        return f"{prefix}: {input_record.get('text', 'no text')}"
    return input_record.get("text", "no text")


@evaluation.scorer
async def has_prefix_scorer(input_record: dict, output: str) -> Score:
    """Checks if the output starts with a prefix (any non-empty prefix before ':')."""
    if ":" in output and output.split(":")[0].strip():
        return Score(value=1.0, rationale="Has prefix")
    return Score(value=0.0, rationale="No prefix")


@workflow.define(name="test-task-workflow")
class TaskWorkflow:
    """A workflow used as a task (instead of @evaluation.task)."""

    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        record = params["input_record"]
        text = record.get("text", "no text")
        return {"result": f"workflow-{text}"}


@evaluation.task
async def context_task(context: TaskContext) -> str:
    """Task that uses TaskContext."""
    prefix = ""
    if context.system:
        prefix = context.system.params.get("prefix", "")
    verbose = (context.metadata or {}).get("verbose", False)
    text = context.input_record.get("text", "no text")
    if verbose:
        return f"{prefix}: {text} [verbose]"
    return f"{prefix}: {text}"


@evaluation.scorer
async def context_scorer(context: ScorerContext) -> Score:
    """Scorer that uses ScorerContext to access system and metadata."""
    has_system = context.system is not None
    has_metadata = bool(context.metadata)
    return Score(
        value=1.0 if has_system and has_metadata else 0.0,
        rationale=f"system={has_system}, metadata={has_metadata}",
    )


@evaluation.scorer
async def metadata_type_scorer(context: ScorerContext) -> Score:
    """Scorer that verifies metadata is always a dict, never None."""
    is_dict = isinstance(context.metadata, dict)
    return Score(value=1.0 if is_dict else 0.0, rationale=f"type={type(context.metadata).__name__}")


@workflow.define(name="test-task-workflow-with-system")
class TaskWorkflowWithSystem:
    """A workflow-as-task that uses the system param."""

    @workflow.entrypoint
    async def run(self, params: dict) -> str:
        record = params["input_record"]
        system = params.get("system") or {}
        text = record.get("text", "no text")
        prefix = system.get("params", {}).get("prefix", "")
        return f"{prefix}: {text}"


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


@evaluation.run_scorer
async def metadata_echo_run_scorer(context: RunEvaluatorContext) -> Score:
    """Returns 1.0 if the expected metadata key is present, 0.0 otherwise."""
    has_key = "experiment" in context.metadata
    return Score(value=1.0 if has_key else 0.0, rationale=f"metadata={context.metadata}")


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


@workflow.define(name="test-eval-workflow-hanging-task")
class EvalWorkflowHangingTask:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=hanging_task,
            evaluators=[Evaluator(name="accuracy", scorer=always_one_scorer)],
            local=True,
        )
        return {
            "run_id": result.run_id,
            "statistics": {k: v.model_dump() for k, v in result.statistics.items()},
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


_EVAL_ACTIVITIES = [
    setup_evaluation_run,
    upload_input_records,
    upload_output_records,
    upload_run_scores,
    create_optimization,
    create_optimization_trial,
    patch_optimization,
    patch_optimization_trial,
    patch_optimization_trial_run,
]


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

    @pytest.mark.asyncio
    async def test_evaluation_hanging_task_times_out(self, temporal_env: Any) -> None:
        """A task that hangs is killed by the child workflow execution_timeout."""
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowHangingTask],
            activities=[hanging_task, always_one_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflowHangingTask)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {
                    "params": {
                        "dataset": [
                            {"text": "fast", "hang": False},
                            {"text": "slow", "hang": True},
                            {"text": "also fast", "hang": False},
                        ],
                    },
                },
                id="test-eval-hanging-task",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            # The evaluation completes despite a hanging task
            assert result["result"]["run_id"] == "local"
            # The non-hanging records should have scores
            assert "accuracy" in result["result"]["statistics"]


# -- Concurrency tracking helpers --

_task_concurrency_counter: int = 0
_task_max_concurrency_seen: int = 0
_task_concurrency_lock = asyncio.Lock()


@evaluation.task(max_concurrency=2)
async def tracked_task(input_record: dict) -> str:
    global _task_concurrency_counter, _task_max_concurrency_seen
    async with _task_concurrency_lock:
        _task_concurrency_counter += 1
        if _task_concurrency_counter > _task_max_concurrency_seen:
            _task_max_concurrency_seen = _task_concurrency_counter

    await asyncio.sleep(0.05)

    async with _task_concurrency_lock:
        _task_concurrency_counter -= 1

    return input_record.get("text", "ok")


@workflow.define(name="test-eval-concurrency")
class EvalConcurrencyWorkflow:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=tracked_task,
            evaluators=[Evaluator(name="accuracy", scorer=always_one_scorer)],
            local=True,
        )
        return {"run_id": result.run_id}


class TestEvaluationConcurrency:
    @pytest.mark.asyncio
    async def test_task_max_concurrency_respected(self, temporal_env: Any) -> None:
        global _task_concurrency_counter, _task_max_concurrency_seen
        _task_concurrency_counter = 0
        _task_max_concurrency_seen = 0

        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalConcurrencyWorkflow],
            activities=[tracked_task, always_one_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalConcurrencyWorkflow)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {
                    "params": {
                        "dataset": [{"text": f"item-{i}"} for i in range(6)],
                    },
                },
                id="test-eval-concurrency",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["run_id"] == "local"
            assert _task_max_concurrency_seen <= 2, (
                f"Expected max 2 concurrent tasks, but saw {_task_max_concurrency_seen}"
            )


# -- Goal support workflows --


@workflow.define(name="test-eval-workflow-with-goals")
class EvalWorkflowWithGoals:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=echo_task,
            evaluators=[
                Evaluator(name="accuracy", scorer=always_one_scorer, goal=Goal.gte(0.8)),
                Evaluator(name="quality", scorer=always_one_scorer, aggregate_goal=Goal.between(0.5, 1.0)),
            ],
        )
        return {"run_id": result.run_id, "run_url": result.run_url}


@workflow.define(name="test-eval-workflow-with-run-evaluator-goals")
class EvalWorkflowWithRunEvaluatorGoals:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=echo_task,
            evaluators=[Evaluator(name="accuracy", scorer=always_one_scorer)],
            run_evaluators=[
                RunEvaluator(name="mean_accuracy", scorer=mean_accuracy_run_scorer, goal=Goal.gte(0.9)),
            ],
        )
        return {
            "run_id": result.run_id,
            "run_url": result.run_url,
            "run_scores": {k: v.model_dump() for k, v in result.run_scores.items()},
        }


class TestEvaluationGoals:
    @pytest.mark.asyncio
    async def test_evaluator_goals_passed_to_backend(self, temporal_env: Any) -> None:
        """Goals on Evaluator are forwarded to the backend create_run call."""
        mock_client = _make_mock_obs_client()
        # Add a second evaluator to the mock response
        eval_obj_2 = MagicMock()
        eval_obj_2.name = "quality"
        eval_obj_2.id = "evaluator-id-2"
        run_response = mock_client.evaluation.beta.create_run.return_value
        run_response.evaluators = [run_response.evaluators[0], eval_obj_2]

        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowWithGoals],
            activities=[echo_task, always_one_scorer, *_EVAL_ACTIVITIES],
            mock_client=mock_client,
        ):
            workflow_def = get_workflow_definition(EvalWorkflowWithGoals)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"text": "hello"}]}},
                id="test-eval-goals",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"]["run_id"] == "test-run-id"

        # Verify goals were passed to create_run
        create_run_call = mock_client.evaluation.beta.create_run.call_args
        evaluators_arg = create_run_call.kwargs.get("evaluators") or create_run_call[1].get("evaluators")
        assert len(evaluators_arg) == 2

        accuracy_eval = evaluators_arg[0]
        assert accuracy_eval.goal is not None
        assert accuracy_eval.goal.operator == "gte"
        assert accuracy_eval.goal.value == 0.8
        assert accuracy_eval.aggregate_goal is None

        quality_eval = evaluators_arg[1]
        assert quality_eval.goal is None
        assert quality_eval.aggregate_goal is not None
        assert quality_eval.aggregate_goal.operator == "between"
        assert quality_eval.aggregate_goal.min == 0.5
        assert quality_eval.aggregate_goal.max == 1.0

    @pytest.mark.asyncio
    async def test_run_evaluator_goals_passed_to_backend(self, temporal_env: Any) -> None:
        """Goals on RunEvaluator are forwarded to the backend create_run call."""
        mock_client = _make_mock_obs_client_with_run_evaluators()

        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowWithRunEvaluatorGoals],
            activities=[echo_task, always_one_scorer, mean_accuracy_run_scorer, *_EVAL_ACTIVITIES],
            mock_client=mock_client,
        ):
            workflow_def = get_workflow_definition(EvalWorkflowWithRunEvaluatorGoals)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"text": "hello"}]}},
                id="test-eval-run-evaluator-goals",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"]["run_id"] == "test-run-id"

        # Verify run evaluator goals were passed to create_run
        create_run_call = mock_client.evaluation.beta.create_run.call_args
        run_evaluators_arg = create_run_call.kwargs.get("run_evaluators") or create_run_call[1].get("run_evaluators")
        assert len(run_evaluators_arg) == 1

        run_eval = run_evaluators_arg[0]
        assert run_eval.goal is not None
        assert run_eval.goal.operator == "gte"
        assert run_eval.goal.value == 0.9

    @pytest.mark.asyncio
    async def test_evaluator_without_goals_sends_none(self, temporal_env: Any) -> None:
        """Evaluators without goals still work — goal fields are None."""
        mock_client = _make_mock_obs_client()

        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflow],
            activities=[echo_task, always_one_scorer, *_EVAL_ACTIVITIES],
            mock_client=mock_client,
        ):
            workflow_def = get_workflow_definition(EvalWorkflow)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"text": "hello"}]}},
                id="test-eval-no-goals",
                task_queue="test-task-queue",
            )
            await handle.result()

        create_run_call = mock_client.evaluation.beta.create_run.call_args
        evaluators_arg = create_run_call.kwargs.get("evaluators") or create_run_call[1].get("evaluators")
        assert len(evaluators_arg) == 1
        assert evaluators_arg[0].goal is None
        assert evaluators_arg[0].aggregate_goal is None


# -- Metadata forwarding workflows --


@workflow.define(name="test-eval-workflow-metadata-forwarding")
class EvalWorkflowMetadataForwarding:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=echo_task,
            evaluators=[Evaluator(name="accuracy", scorer=always_one_scorer)],
            run_evaluators=[RunEvaluator(name="meta_check", scorer=metadata_echo_run_scorer)],
            metadata={"experiment": "v1", "team": "obs"},
            local=True,
        )
        return {
            "run_id": result.run_id,
            "run_scores": {k: v.model_dump() for k, v in result.run_scores.items()},
        }


# -- System passthrough workflows --


@workflow.define(name="test-eval-workflow-with-system")
class EvalWorkflowWithSystem:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=system_task,
            evaluators=[Evaluator(name="has_prefix", scorer=has_prefix_scorer)],
            system=System(name="test-system", params={"prefix": "Summary"}),
            local=True,
        )
        return {
            "run_id": result.run_id,
            "statistics": {k: v.model_dump() for k, v in result.statistics.items()},
        }


@workflow.define(name="test-eval-workflow-with-system-no-system-arg")
class EvalWorkflowWithSystemNoSystemArg:
    """System is provided but task doesn't accept it — should still work."""

    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=echo_task,
            evaluators=[Evaluator(name="accuracy", scorer=always_one_scorer)],
            system=System(name="test-system", params={"prefix": "Summary"}),
            local=True,
        )
        return {
            "run_id": result.run_id,
            "statistics": {k: v.model_dump() for k, v in result.statistics.items()},
        }


@workflow.define(name="test-eval-workflow-system-task-no-system-provided")
class EvalWorkflowSystemTaskNoSystemProvided:
    """Task accepts (input_record, system) but evaluation.run() omits system."""

    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=optional_system_task,
            evaluators=[Evaluator(name="accuracy", scorer=always_one_scorer)],
            local=True,
        )
        return {
            "run_id": result.run_id,
            "statistics": {k: v.model_dump() for k, v in result.statistics.items()},
        }


@workflow.define(name="test-eval-workflow-system-via-workflow-task")
class EvalWorkflowSystemViaWorkflowTask:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=TaskWorkflowWithSystem,
            evaluators=[Evaluator(name="has_prefix", scorer=has_prefix_scorer)],
            system=System(name="test-system", params={"prefix": "Summary"}),
            local=True,
        )
        return {
            "run_id": result.run_id,
            "statistics": {k: v.model_dump() for k, v in result.statistics.items()},
        }


class TestEvaluationMetadataForwarding:
    @pytest.mark.asyncio
    async def test_metadata_forwarded_to_run_evaluator(self, temporal_env: Any) -> None:
        """metadata from evaluation.run() is forwarded to RunEvaluatorContext."""
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowMetadataForwarding],
            activities=[echo_task, always_one_scorer, metadata_echo_run_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflowMetadataForwarding)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"text": "hello"}]}},
                id="test-eval-metadata-forwarding",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["run_id"] == "local"
            run_scores = result["result"]["run_scores"]
            assert "meta_check" in run_scores
            assert run_scores["meta_check"]["value"] == 1.0


class TestEvaluationSystemPassthrough:
    @pytest.mark.asyncio
    async def test_system_passed_to_task(self, temporal_env: Any) -> None:
        """When task accepts (input_record, system), system is forwarded."""
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowWithSystem],
            activities=[system_task, has_prefix_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflowWithSystem)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"text": "hello"}, {"text": "world"}]}},
                id="test-eval-system-passthrough",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["run_id"] == "local"
            # The system_task prepends "Summary: " so has_prefix_scorer should score 1.0
            stats = result["result"]["statistics"]
            assert "has_prefix" in stats
            assert stats["has_prefix"]["avg"] == 1.0

    @pytest.mark.asyncio
    async def test_system_ignored_when_task_does_not_accept_it(self, temporal_env: Any) -> None:
        """When task only accepts (input_record), system is ignored gracefully."""
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowWithSystemNoSystemArg],
            activities=[echo_task, always_one_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflowWithSystemNoSystemArg)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"text": "hello"}]}},
                id="test-eval-system-ignored",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["run_id"] == "local"
            assert "accuracy" in result["result"]["statistics"]

    @pytest.mark.asyncio
    async def test_system_task_works_without_system_provided(self, temporal_env: Any) -> None:
        """When task accepts (input_record, system) but no system is provided, system=None is forwarded."""
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowSystemTaskNoSystemProvided],
            activities=[optional_system_task, always_one_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflowSystemTaskNoSystemProvided)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"text": "hello"}]}},
                id="test-eval-system-task-no-system",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["run_id"] == "local"
            assert "accuracy" in result["result"]["statistics"]

    @pytest.mark.asyncio
    async def test_system_passed_to_workflow_as_task(self, temporal_env: Any) -> None:
        """When task is a workflow class, system is forwarded via params["system"]."""
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowSystemViaWorkflowTask, TaskWorkflowWithSystem],
            activities=[has_prefix_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflowSystemViaWorkflowTask)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"text": "hello"}, {"text": "world"}]}},
                id="test-eval-system-workflow-task",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["run_id"] == "local"
            stats = result["result"]["statistics"]
            assert "has_prefix" in stats
            assert stats["has_prefix"]["avg"] == 1.0


# -- Context objects workflows --


@workflow.define(name="test-eval-workflow-context-task")
class EvalWorkflowContextTask:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=context_task,
            evaluators=[Evaluator(name="accuracy", scorer=always_one_scorer)],
            system=System(name="test-system", params={"prefix": "Summary"}),
            metadata={"verbose": True},
            local=True,
        )
        return {
            "run_id": result.run_id,
            "statistics": {k: v.model_dump() for k, v in result.statistics.items()},
        }


@workflow.define(name="test-eval-workflow-context-scorer")
class EvalWorkflowContextScorer:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=echo_task,
            evaluators=[Evaluator(name="context_check", scorer=context_scorer)],
            system=System(name="test-system", params={"key": "value"}),
            metadata={"experiment": "v1"},
            local=True,
        )
        return {
            "run_id": result.run_id,
            "statistics": {k: v.model_dump() for k, v in result.statistics.items()},
        }


@workflow.define(name="test-eval-workflow-context-scorer-no-system")
class EvalWorkflowContextScorerNoSystem:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=echo_task,
            evaluators=[Evaluator(name="context_check", scorer=context_scorer)],
            local=True,
        )
        return {
            "run_id": result.run_id,
            "statistics": {k: v.model_dump() for k, v in result.statistics.items()},
        }


class TestEvaluationContextObjects:
    @pytest.mark.asyncio
    async def test_task_context_receives_system_and_metadata(self, temporal_env: Any) -> None:
        """TaskContext-style task receives system and metadata."""
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowContextTask],
            activities=[context_task, always_one_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflowContextTask)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"text": "hello"}]}},
                id="test-eval-context-task",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["run_id"] == "local"
            assert "accuracy" in result["result"]["statistics"]

    @pytest.mark.asyncio
    async def test_scorer_context_receives_system_and_metadata(self, temporal_env: Any) -> None:
        """ScorerContext-style scorer receives system and metadata."""
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowContextScorer],
            activities=[echo_task, context_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflowContextScorer)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"text": "hello"}]}},
                id="test-eval-context-scorer",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["run_id"] == "local"
            stats = result["result"]["statistics"]
            assert "context_check" in stats
            # context_scorer returns 1.0 when both system and metadata are present
            assert stats["context_check"]["avg"] == 1.0

    @pytest.mark.asyncio
    async def test_scorer_context_without_system(self, temporal_env: Any) -> None:
        """ScorerContext-style scorer works when system/metadata are not provided."""
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowContextScorerNoSystem],
            activities=[echo_task, context_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflowContextScorerNoSystem)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"text": "hello"}]}},
                id="test-eval-context-scorer-no-system",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["run_id"] == "local"
            stats = result["result"]["statistics"]
            assert "context_check" in stats
            # context_scorer returns 0.0 when system or metadata missing
            assert stats["context_check"]["avg"] == 0.0


class TestUsesContextStyleWithDepends:
    """_uses_context_style must ignore Depends() params when counting positional args."""

    def test_task_context_with_depends_is_detected(self) -> None:
        from mistralai.workflows.core.dependencies.dependency_injector import Depends
        from mistralai.workflows.plugins.evaluation._orchestrator import _uses_context_style

        def _fake_dep() -> str:
            return "injected"

        async def my_task(ctx: TaskContext, dep: str = Depends(_fake_dep)) -> str:
            return ctx.input_record["text"]

        assert _uses_context_style(my_task, TaskContext) is True

    def test_scorer_context_with_depends_is_detected(self) -> None:
        from mistralai.workflows.core.dependencies.dependency_injector import Depends
        from mistralai.workflows.plugins.evaluation._orchestrator import _uses_context_style

        def _fake_dep() -> str:
            return "injected"

        async def my_scorer(ctx: ScorerContext, dep: str = Depends(_fake_dep)) -> Score:
            return Score(value=1.0)

        assert _uses_context_style(my_scorer, ScorerContext) is True


# -- score() building block tests --


@workflow.define(name="test-eval-score-context-scorer")
class EvalWorkflowScoreContextScorer:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        from mistralai.workflows.plugins.evaluation._orchestrator import score

        dataset = params["dataset"]
        outputs = [r.get("text", "no text") for r in dataset]
        scores = await score(
            dataset=dataset,
            outputs=outputs,
            evaluators=[Evaluator(name="meta_type", scorer=metadata_type_scorer)],
        )
        return {"scores": scores}


class TestScoreBuildingBlock:
    @pytest.mark.asyncio
    async def test_score_supports_scorer_context(self, temporal_env: Any) -> None:
        """score() detects ScorerContext-style scorers and passes a ScorerContext."""
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowScoreContextScorer],
            activities=[metadata_type_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflowScoreContextScorer)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"text": "hello"}]}},
                id="test-eval-score-context-scorer",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            scores = result["result"]["scores"]
            assert len(scores) == 1
            assert scores[0]["meta_type"]["value"] == 1.0


# -- metadata is always a dict tests --


@workflow.define(name="test-eval-workflow-metadata-always-dict")
class EvalWorkflowMetadataAlwaysDict:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=params["dataset"],
            task=echo_task,
            evaluators=[Evaluator(name="meta_type", scorer=metadata_type_scorer)],
            local=True,
            # no metadata= passed
        )
        return {
            "run_id": result.run_id,
            "statistics": {k: v.model_dump() for k, v in result.statistics.items()},
        }


class TestMetadataAlwaysDict:
    @pytest.mark.asyncio
    async def test_scorer_context_metadata_is_dict_when_not_provided(self, temporal_env: Any) -> None:
        """ScorerContext.metadata is {} (not None) when evaluation.run() omits metadata."""
        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[EvalWorkflowMetadataAlwaysDict],
            activities=[echo_task, metadata_type_scorer, *_EVAL_ACTIVITIES],
        ):
            workflow_def = get_workflow_definition(EvalWorkflowMetadataAlwaysDict)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"text": "hello"}]}},
                id="test-eval-metadata-always-dict",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            stats = result["result"]["statistics"]
            assert "meta_type" in stats
            # metadata_type_scorer returns 1.0 when metadata is a dict
            assert stats["meta_type"]["avg"] == 1.0
