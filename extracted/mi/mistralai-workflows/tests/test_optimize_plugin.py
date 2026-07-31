"""Tests for evaluation.optimize (GEPA-style) using in-process Temporal."""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from mistralai.observability.api_models import (
    EvaluationRunGenerationResponse,
    EvaluationRunOutputRecordResponse,
    EvaluationRunRecordResponse,
    EvaluationRunScoreResponse,
    ListEvaluationRunRecordsResponse,
    PaginatedResult,
)
from temporalio.client import WorkflowFailureError

from mistralai.workflows import get_workflow_definition, workflow
from mistralai.workflows.plugins.evaluation import GEPA, MutatorProposal, MutatorRequest, Tunable, evaluation
from mistralai.workflows.plugins.evaluation._activities import optimize_fetch_records, optimize_mutate
from mistralai.workflows.plugins.evaluation.types import Evaluator, Score, TaskContext, TunableSystem

from .test_evaluation_plugin import (
    _EVAL_ACTIVITIES,
    _create_test_worker_with_mock_obs,
    _make_mock_obs_client,
)


@evaluation.task
async def opt_task(ctx: TaskContext) -> str:
    # The output (hence the score) is driven purely by the tunable `x`.
    return str(ctx.system.params["x"])


@evaluation.scorer
async def opt_scorer(input_record: dict[str, Any], output: str) -> Score:
    return Score(value=float(output) / 10.0)


@evaluation.mutator
async def bump_to_nine(request: MutatorRequest) -> MutatorProposal:
    # Custom mutator as an activity: ignores the LLM entirely, proposes x=9 directly.
    # `request` is typed — attribute access, not dict lookups.
    return MutatorProposal(changed={"x": 9}, reasoning=f"bump x to 9 (saw {len(request.failures)} failures)")


@workflow.define(name="bump-mutator-subworkflow")
class BumpMutatorSubworkflow:
    @workflow.entrypoint
    async def run(self, params: MutatorRequest) -> MutatorProposal:
        # Custom mutator as a subworkflow: receives the typed request as `params`,
        # returns the same MutatorProposal contract. Proposes x=8.
        return MutatorProposal(changed={"x": 8}, reasoning="subworkflow bump to 8")


def _mock_obs_client_with_record(output: str, value: float) -> Any:
    mock_client = _make_mock_obs_client()
    record = EvaluationRunRecordResponse(
        id="r1",
        input={"a": 1},
        output_record=EvaluationRunOutputRecordResponse(
            generations=[
                EvaluationRunGenerationResponse(
                    output=output,
                    status="success",
                    scores={"accuracy": [EvaluationRunScoreResponse(value=value, status="success", rationale="ok")]},
                )
            ],
        ),
    )
    mock_client.evaluation.beta.list_records = AsyncMock(
        return_value=ListEvaluationRunRecordsResponse(records=PaginatedResult(results=[record], count=1, next=None))
    )
    return mock_client


@workflow.define(name="test-optimize-workflow")
class OptimizeWorkflow:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.optimize(
            # "model" is a fixed (non-Tunable) slot: it must survive into the result params.
            system=TunableSystem(name="candidate", params={"x": Tunable(1, bounds=(0, 10)), "model": "fixed-model"}),
            dataset=params["dataset"],
            task=opt_task,
            evaluators=[Evaluator(name="accuracy", scorer=opt_scorer)],
            # 4 records → D_pareto=2, D_feedback=2; 2 mutation attempts, no holdout (scored on D_pareto).
            algo=GEPA(iterations=2, pareto_size=2, minibatch_size=1, holdout=0),
        )
        win = result.winner or result.best_attempt
        best = max(result.trajectory, key=lambda c: c.score)  # trajectory is generation-order, so pick the top scorer
        seed = next(c for c in result.trajectory if c.from_ is None)
        return {
            "baseline_x": result.baseline.system["x"],
            "optimized_x": win.system["x"] if win else None,
            "baseline_model": result.baseline.system.get("model"),
            "optimized_model": win.system.get("model") if win else None,
            "optimized_score": win.score if win else None,
            "verdict": result.verdict,
            "gain": win.gain if win else None,
            "n_candidates": len(result.trajectory),
            "top_score": best.score,
            "top_reasoning": best.reasoning,
            "seed_reasoning": seed.reasoning,
        }


@workflow.define(name="test-optimize-custom-mutator-workflow")
class OptimizeCustomMutatorWorkflow:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.optimize(
            # Two tunables, but bump_to_nine only returns {"x": 9} — the untouched "y" must keep
            # its seed value (7), not be dropped from the candidate.
            system=TunableSystem(
                name="candidate", params={"x": Tunable(1, bounds=(0, 10)), "y": Tunable(7, bounds=(0, 10))}
            ),
            dataset=params["dataset"],
            task=opt_task,
            evaluators=[Evaluator(name="accuracy", scorer=opt_scorer)],
            algo=GEPA(iterations=2, pareto_size=2, minibatch_size=1, holdout=0, mutator=bump_to_nine),  # type: ignore[arg-type]
        )
        win = result.winner or result.best_attempt
        best = max(result.trajectory, key=lambda c: c.score)
        return {
            "baseline_x": result.baseline.system["x"],
            "optimized_x": win.system["x"] if win else None,
            "optimized_y": win.system.get("y") if win else None,
            "verdict": result.verdict,
            "top_reasoning": best.reasoning,
        }


@workflow.define(name="test-optimize-subworkflow-mutator-workflow")
class OptimizeSubworkflowMutatorWorkflow:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.optimize(
            system=TunableSystem(name="candidate", params={"x": Tunable(1, bounds=(0, 10))}),
            dataset=params["dataset"],
            task=opt_task,
            evaluators=[Evaluator(name="accuracy", scorer=opt_scorer)],
            algo=GEPA(iterations=2, pareto_size=2, minibatch_size=1, holdout=0, mutator=BumpMutatorSubworkflow),  # type: ignore[arg-type]
        )
        win = result.winner or result.best_attempt
        best = max(result.trajectory, key=lambda c: c.score)
        return {
            "baseline_x": result.baseline.system["x"],
            "optimized_x": win.system["x"] if win else None,
            "verdict": result.verdict,
            "top_reasoning": best.reasoning,
        }


class TestEvaluationOptimize:
    @pytest.mark.asyncio
    async def test_optimize_climbs_and_returns_winner(self, temporal_env: Any) -> None:
        mock_client = _make_mock_obs_client()
        # The reflective mutation activity asks the LLM for improved values; stub it to
        # jump the tunable to 9 (score 0.9) so the search visibly climbs off the seed.
        response = MagicMock()
        response.choices = [MagicMock()]
        response.choices[0].message.content = json.dumps({"reasoning": "raise x hard", "x": 9})
        mock_client.chat.complete_async = AsyncMock(return_value=response)
        # The fetch activity reads per-record scores/rationales for Pareto + reflection.
        record = EvaluationRunRecordResponse(
            id="r1",
            input={"a": 1},
            output_record=EvaluationRunOutputRecordResponse(
                generations=[
                    EvaluationRunGenerationResponse(
                        output="9",
                        status="success",
                        scores={"accuracy": [EvaluationRunScoreResponse(value=1.0, status="success", rationale="ok")]},
                    )
                ],
            ),
        )
        mock_client.evaluation.beta.list_records = AsyncMock(
            return_value=ListEvaluationRunRecordsResponse(records=PaginatedResult(results=[record], count=1, next=None))
        )

        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[OptimizeWorkflow],
            activities=[opt_task, opt_scorer, optimize_mutate, optimize_fetch_records, *_EVAL_ACTIVITIES],
            mock_client=mock_client,
        ):
            workflow_def = get_workflow_definition(OptimizeWorkflow)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}]}},
                id="test-optimize-basic",
                task_queue="test-task-queue",
            )
            result = await handle.result()

        out = result["result"]
        assert out["baseline_x"] == 1  # the initial seed
        assert out["optimized_x"] == 9  # climbed from seed x=1
        # Fixed (non-Tunable) slots are merged back into the result params, not dropped.
        assert out["baseline_model"] == "fixed-model"
        assert out["optimized_model"] == "fixed-model"
        assert out["optimized_score"] == pytest.approx(0.9)  # validated on the holdout
        assert out["verdict"] == "success"  # winner beats the baseline
        assert out["gain"] == pytest.approx(0.8)  # 0.9 - 0.1
        assert out["n_candidates"] == 3  # seed + 2 mutations
        assert out["top_score"] == pytest.approx(0.9)  # best candidate in the trajectory
        assert "raise x hard" in (out["top_reasoning"] or "")  # mutation reasoning captured on candidates
        assert out["seed_reasoning"] is None  # the seed has no mutation reasoning

    @pytest.mark.asyncio
    async def test_optimize_with_custom_mutator_activity(self, temporal_env: Any) -> None:
        # No chat mock: a custom @evaluation.mutator replaces the default reflective activity,
        # so the LLM is never called. optimize_mutate is not even registered — proving the
        # custom activity path is taken.
        mock_client = _mock_obs_client_with_record(output="9", value=1.0)

        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[OptimizeCustomMutatorWorkflow],
            activities=[opt_task, opt_scorer, bump_to_nine, optimize_fetch_records, *_EVAL_ACTIVITIES],
            mock_client=mock_client,
        ):
            workflow_def = get_workflow_definition(OptimizeCustomMutatorWorkflow)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}]}},
                id="test-optimize-custom-mutator",
                task_queue="test-task-queue",
            )
            result = await handle.result()

        out = result["result"]
        assert out["baseline_x"] == 1
        assert out["optimized_x"] == 9  # climbed via the custom mutator
        assert out["optimized_y"] == 7  # untouched slot kept its seed value (not dropped)
        assert out["verdict"] == "success"
        assert "bump x to 9" in (out["top_reasoning"] or "")  # custom mutator's reasoning captured

    @pytest.mark.asyncio
    async def test_optimize_with_custom_mutator_subworkflow(self, temporal_env: Any) -> None:
        mock_client = _mock_obs_client_with_record(output="8", value=1.0)

        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[OptimizeSubworkflowMutatorWorkflow, BumpMutatorSubworkflow],
            activities=[opt_task, opt_scorer, optimize_fetch_records, *_EVAL_ACTIVITIES],
            mock_client=mock_client,
        ):
            workflow_def = get_workflow_definition(OptimizeSubworkflowMutatorWorkflow)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}]}},
                id="test-optimize-custom-mutator-subworkflow",
                task_queue="test-task-queue",
            )
            result = await handle.result()

        out = result["result"]
        assert out["baseline_x"] == 1
        assert out["optimized_x"] == 8  # climbed via the subworkflow mutator
        assert out["verdict"] == "success"
        assert "subworkflow bump to 8" in (out["top_reasoning"] or "")

    @pytest.mark.asyncio
    async def test_optimize_persists_optimization_create_first(self, temporal_env: Any) -> None:
        # The workflow-side create-first wiring: an upfront create_optimization, each candidate run
        # linked via _orchestrator.run, and a completed finalize — end-to-end through the worker.
        mock_client = _make_mock_obs_client()
        response = MagicMock()
        response.choices = [MagicMock()]
        response.choices[0].message.content = json.dumps({"reasoning": "raise x", "x": 9})
        mock_client.chat.complete_async = AsyncMock(return_value=response)
        record = EvaluationRunRecordResponse(
            id="r1",
            input={"a": 1},
            output_record=EvaluationRunOutputRecordResponse(
                generations=[
                    EvaluationRunGenerationResponse(
                        output="9",
                        status="success",
                        scores={"accuracy": [EvaluationRunScoreResponse(value=1.0, status="success", rationale="ok")]},
                    )
                ],
            ),
        )
        mock_client.evaluation.beta.list_records = AsyncMock(
            return_value=ListEvaluationRunRecordsResponse(records=PaginatedResult(results=[record], count=1, next=None))
        )

        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[OptimizeWorkflow],
            activities=[opt_task, opt_scorer, optimize_mutate, optimize_fetch_records, *_EVAL_ACTIVITIES],
            mock_client=mock_client,
        ):
            workflow_def = get_workflow_definition(OptimizeWorkflow)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}]}},
                id="test-optimize-persist",
                task_queue="test-task-queue",
            )
            result = await handle.result()

        # 1. The optimization row is created up front with source="workflow".
        create = mock_client.evaluation._endpoints.create_optimization
        create.assert_awaited_once()
        create_req = create.call_args.args[0]
        assert create_req.source == "workflow"
        assert create_req.algorithm == "GEPA"

        # 2. Every candidate run is linked to the optimization at creation.
        run_calls = mock_client.evaluation.beta.create_run.call_args_list
        assert run_calls, "expected candidate runs"
        for call in run_calls:
            assert call.kwargs["optimization_id"] == "test-optimization-id"
            assert set(call.kwargs["optimization_metadata"]) >= {"gen", "subset"}

        # 3. The optimization is finalized completed, with an outcome.
        patch = mock_client.evaluation._endpoints.patch_optimization
        patch.assert_awaited_once()
        assert patch.call_args.args[0] == "test-optimization-id"
        patch_req = patch.call_args.args[1]
        assert patch_req.status == "completed"
        assert patch_req.outcome is not None
        # (optimization_url on the result is covered by the SDK test; OptimizeWorkflow here returns a
        # custom dict, not result.model_dump(), so there's nothing to assert on that front.)
        assert result["result"]["verdict"] == "success"

    @pytest.mark.asyncio
    async def test_optimize_marks_optimization_failed_on_search_error(self, temporal_env: Any) -> None:
        # If the search raises (here: the reflective mutation LLM call keeps failing), the workflow
        # must finalize the optimization as `failed` before propagating.
        mock_client = _make_mock_obs_client()
        mock_client.chat.complete_async = AsyncMock(side_effect=RuntimeError("llm unavailable"))
        record = EvaluationRunRecordResponse(
            id="r1",
            input={"a": 1},
            output_record=EvaluationRunOutputRecordResponse(
                generations=[
                    EvaluationRunGenerationResponse(
                        output="1",
                        status="success",
                        scores={"accuracy": [EvaluationRunScoreResponse(value=0.1, status="success", rationale="ok")]},
                    )
                ],
            ),
        )
        mock_client.evaluation.beta.list_records = AsyncMock(
            return_value=ListEvaluationRunRecordsResponse(records=PaginatedResult(results=[record], count=1, next=None))
        )

        async with _create_test_worker_with_mock_obs(
            temporal_env,
            workflows=[OptimizeWorkflow],
            activities=[opt_task, opt_scorer, optimize_mutate, optimize_fetch_records, *_EVAL_ACTIVITIES],
            mock_client=mock_client,
        ):
            workflow_def = get_workflow_definition(OptimizeWorkflow)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"params": {"dataset": [{"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}]}},
                id="test-optimize-failed",
                task_queue="test-task-queue",
            )
            with pytest.raises(WorkflowFailureError):
                await handle.result()

        patch = mock_client.evaluation._endpoints.patch_optimization
        statuses = [call.args[1].status for call in patch.call_args_list]
        assert "failed" in statuses


@pytest.mark.asyncio
async def test_optimize_rejects_local_mode() -> None:
    # Workflow optimize reads each candidate's records back from AI Studio; a local run doesn't
    # persist them, so local=True is rejected up front rather than returning empty scores.
    with pytest.raises(ValueError, match="local"):
        await evaluation.optimize(
            system=TunableSystem(name="candidate", params={"x": Tunable(1, bounds=(0, 10))}),
            dataset=[{"a": 1}],
            task=opt_task,
            evaluators=[Evaluator(name="accuracy", scorer=opt_scorer)],
            algo=GEPA(iterations=1, pareto_size=1, minibatch_size=1, holdout=0),
            local=True,
        )
