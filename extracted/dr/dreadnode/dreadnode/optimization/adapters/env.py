"""Capability adapter that scores candidates against a live ``TaskEnvironment``.

The shipped ``StackAwareCapabilityAdapter`` materializes a candidate capability
and evaluates it via ``Evaluation`` against a static dataset. ``CapabilityEnvAdapter``
swaps the evaluation loop: each dataset row provisions a fresh hosted task
environment, runs the rebuilt agent against the env's rendered instruction,
and calls the user's scorers while the env is still alive so scorers can
reach the sandbox via the ``current_task_environment`` contextvar.

All other adapter surfaces (seed candidate, materialize, propose-new-texts,
reflective-dataset construction) are inherited unchanged from
``StackAwareCapabilityAdapter``.
"""

import asyncio
import statistics
import typing as t

from pydantic import Field, PrivateAttr

from dreadnode.core.scorer import Scorer
from dreadnode.optimization.adapters._env_eval import score_row_with_task_env
from dreadnode.optimization.adapters.stack import StackAwareCapabilityAdapter
from dreadnode.optimization.backends.base import OptimizationEvaluationBatch
from dreadnode.optimization.result import OptimizationEvaluation


class CapabilityEnvAdapter(StackAwareCapabilityAdapter):
    """Capability adapter that scores candidates against a provisioned task environment.

    Each dataset row is evaluated by provisioning a ``TaskEnvironment`` via
    :func:`dreadnode.task_env`, rendering the task instruction, running the
    rebuilt agent, and invoking the configured scorers against the agent's
    output. Scorers can read ``dreadnode.core.current_task_environment`` to
    reach the live sandbox (e.g. to shell-probe for a flag) while it is still
    provisioned.

    Dataset row conventions:
        - ``task_ref`` (optional): overrides the adapter's default task ref
          on a per-row basis. Drives which task each trial provisions.
        - ``inputs`` (optional): per-row template bindings substituted into
          the task's instruction. The primary mechanism for per-row variation.
        - Scoring fields (``expected_output``, ``needle``, ``reward``, etc.)
          for reward-recipe-based scoring.

    The dataset's ``goal`` field is explicitly NOT consulted: the task's
    rendered instruction is the agent's user message, and the capability's
    mutable surfaces are the optimization target. "Injecting a different
    prompt per row" isn't a capability_env concept — it's a capability_agent
    concept, and that adapter should be used instead.

    Attributes:
        task_ref: Default task reference passed to :func:`dreadnode.task_env`
            when a row does not override it.
        timeout_sec: Optional per-env provisioning timeout.
    """

    task_ref: str
    timeout_sec: int | None = None
    parallel_rows: int = Field(default=1, ge=1)
    """Maximum dataset rows to evaluate concurrently within one candidate's
    ``evaluate()`` call. ``1`` preserves serial behaviour. Higher values
    provision that many ``TaskEnvironment`` sandboxes in parallel, so watch
    platform concurrency limits."""

    _dreadnode_factory: t.Callable[[], t.Any] | None = PrivateAttr(default=None)

    async def evaluate(
        self,
        batch: list[dict[str, t.Any]],
        candidate: dict[str, str],
        *,
        capture_traces: bool = False,
    ) -> OptimizationEvaluationBatch:
        """Evaluate a candidate by running the rebuilt agent against per-row task envs."""
        dn = self._resolve_dreadnode()
        fitted_scorers = Scorer.fit_many(self.scorers)
        materialized = await asyncio.to_thread(self.materialize_candidate, candidate)

        try:
            agent = self._build_agent(materialized)

            if self.parallel_rows > 1 and len(batch) > 1:
                semaphore = asyncio.Semaphore(self.parallel_rows)

                async def _guarded(row: dict[str, t.Any]) -> dict[str, t.Any]:
                    async with semaphore:
                        return await self._score_row(
                            row=row,
                            agent=agent,
                            dn=dn,
                            fitted_scorers=fitted_scorers,
                            capture_traces=capture_traces,
                        )

                per_row = await asyncio.gather(*(_guarded(row) for row in batch))
            else:
                per_row = [
                    await self._score_row(
                        row=row,
                        agent=agent,
                        dn=dn,
                        fitted_scorers=fitted_scorers,
                        capture_traces=capture_traces,
                    )
                    for row in batch
                ]
        finally:
            materialized.cleanup()

        outputs = [entry["output"] for entry in per_row]
        scores = [entry["score"] for entry in per_row]
        objective_scores = [entry["objective_scores"] for entry in per_row]
        trajectories = [entry["trajectory"] for entry in per_row if entry["trajectory"] is not None]

        return OptimizationEvaluationBatch(
            outputs=outputs,
            scores=scores,
            trajectories=trajectories if capture_traces and trajectories else None,
            objective_scores=objective_scores or None,
        )

    async def _score_row(
        self,
        *,
        row: dict[str, t.Any],
        agent: t.Any,
        dn: t.Any,
        fitted_scorers: list[t.Any],
        capture_traces: bool,
    ) -> dict[str, t.Any]:
        """Provision the env for one row, run the agent, collect scores.

        Delegates to :func:`score_row_with_task_env` so other adapters
        (e.g. SessionRuntimeAdapter) can reuse the same logic.
        """
        return await score_row_with_task_env(
            row=row,
            agent=agent,
            dn=dn,
            fitted_scorers=fitted_scorers,
            default_task_ref=self.task_ref,
            timeout_sec=self.timeout_sec,
            score_name=self.score_name,
            capture_traces=capture_traces,
        )

    async def evaluate_candidate(
        self,
        candidate: dict[str, str],
        example: dict[str, t.Any] | None = None,
    ) -> OptimizationEvaluation:
        """Evaluate one candidate in GEPA-compatible ``(score, side_info)`` form."""
        batch = [example] if example is not None else self.dataset
        if not batch:
            raise ValueError("Env optimization requires at least one dataset example.")
        evaluation_batch = await self.evaluate(batch, candidate, capture_traces=True)
        score = statistics.mean(evaluation_batch.scores) if evaluation_batch.scores else 0.0
        side_info: dict[str, t.Any] = {
            "scores": evaluation_batch.scores,
            "batch_size": len(batch),
        }
        if evaluation_batch.trajectories is not None:
            side_info["trajectories"] = evaluation_batch.trajectories
        return OptimizationEvaluation(score=score, side_info=side_info)

    def _resolve_dreadnode(self) -> t.Any:
        """Resolve the ``Dreadnode`` instance used to provision task environments."""
        if self._dreadnode_factory is not None:
            return self._dreadnode_factory()
        from dreadnode import _get_default_instance

        return _get_default_instance()
