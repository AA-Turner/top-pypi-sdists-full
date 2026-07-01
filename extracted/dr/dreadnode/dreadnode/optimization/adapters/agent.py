from __future__ import annotations

import statistics
import typing as t

from pydantic import BaseModel, ConfigDict, Field

from dreadnode.agents.trajectory import Trajectory, trajectory_to_turns
from dreadnode.evaluations.evaluation import Evaluation
from dreadnode.optimization.backends.base import OptimizationEvaluationBatch
from dreadnode.optimization.result import OptimizationEvaluation

if t.TYPE_CHECKING:
    from dreadnode.agents.agent import Agent
else:
    Agent = t.Any


class DreadnodeAgentAdapter(BaseModel):
    """Adapter that evaluates agent instruction candidates with Evaluation."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    agent: Agent
    dataset: list[dict[str, t.Any]] = Field(default_factory=list)
    scorers: t.Any = Field(default_factory=list)
    score_name: str | None = None
    goal_field: str = "goal"
    dataset_input_mapping: list[str] | dict[str, str] | None = None
    name: str | None = None

    def seed_candidate(self) -> dict[str, str]:
        """Return the current instruction candidate for this agent."""
        return {"instructions": self.agent.instructions or ""}

    def apply_candidate(self, candidate: dict[str, str]) -> Agent:
        """Clone the agent and apply an instruction-only candidate."""
        instructions = candidate.get("instructions")
        if instructions is None:
            raise ValueError("Agent optimization candidates must include 'instructions'.")
        return self.agent.with_(instructions=instructions)

    async def evaluate(
        self,
        batch: list[dict[str, t.Any]],
        candidate: dict[str, str],
        *,
        capture_traces: bool = False,
    ) -> OptimizationEvaluationBatch:
        """Evaluate one batch of examples and return per-example scores."""
        agent = self.apply_candidate(candidate)
        evaluation = Evaluation(
            name=self.name or f"{agent.name or 'agent'} optimization",
            task=agent.task(name=agent.name),
            dataset=batch,
            dataset_input_mapping=self._resolve_dataset_input_mapping(batch),
            scorers=self.scorers,
        )
        result = await evaluation.run()
        return OptimizationEvaluationBatch(
            outputs=[sample.output for sample in result.samples],
            scores=[self._sample_score(sample) for sample in result.samples],
            trajectories=(
                [self._serialize_sample(sample) for sample in result.samples]
                if capture_traces
                else None
            ),
            objective_scores=[self._metric_scores(sample) for sample in result.samples] or None,
        )

    async def evaluate_candidate(
        self,
        candidate: dict[str, str],
        example: dict[str, t.Any] | None = None,
    ) -> OptimizationEvaluation:
        """Evaluate one candidate in a GEPA-compatible `(score, side_info)` shape."""
        batch = [example] if example is not None else self.dataset
        if not batch:
            raise ValueError("Agent optimization requires at least one dataset example.")
        evaluation_batch = await self.evaluate(
            batch,
            candidate,
            capture_traces=True,
        )
        score = statistics.mean(evaluation_batch.scores) if evaluation_batch.scores else 0.0
        side_info: dict[str, t.Any] = {
            "scores": evaluation_batch.scores,
            "batch_size": len(batch),
        }
        if evaluation_batch.trajectories is not None:
            side_info["trajectories"] = evaluation_batch.trajectories
        return OptimizationEvaluation(score=score, side_info=side_info)

    def make_reflective_dataset(
        self,
        candidate: dict[str, str],
        eval_batch: OptimizationEvaluationBatch,
        components_to_update: list[str],
    ) -> dict[str, list[dict[str, t.Any]]]:
        """Build component-scoped reflective data for GEPA."""
        components = components_to_update or ["instructions"]
        trajectories = eval_batch.trajectories or []
        dataset: dict[str, list[dict[str, t.Any]]] = {}

        for component in components:
            component_rows: list[dict[str, t.Any]] = []
            for score, trajectory in zip(eval_batch.scores, trajectories, strict=False):
                component_rows.append(
                    {
                        "Candidate": candidate.get(component, ""),
                        "Inputs": trajectory.get("input"),
                        "Generated Outputs": trajectory.get("output"),
                        "Feedback": self._format_feedback(score=score, trajectory=trajectory),
                    }
                )
            dataset[component] = component_rows

        return dataset

    def _resolve_dataset_input_mapping(
        self,
        batch: list[dict[str, t.Any]],
    ) -> list[str] | dict[str, str]:
        if self.dataset_input_mapping is not None:
            return self.dataset_input_mapping
        if not batch:
            return {self.goal_field: "goal"}
        first_row = batch[0]
        if self.goal_field in first_row:
            return {self.goal_field: "goal"}
        if len(first_row) == 1:
            first_key = next(iter(first_row))
            return {first_key: "goal"}
        raise ValueError(
            "Agent optimization examples must provide a goal field or an explicit dataset_input_mapping."
        )

    def _sample_score(self, sample: t.Any) -> float:
        if self.score_name is not None:
            metric = sample.metrics.get(self.score_name)
            if metric is not None and metric.value is not None:
                return float(metric.value)
            return 0.0

        metric_values = [
            metric.value for metric in sample.metrics.values() if metric.value is not None
        ]
        if len(metric_values) == 1:
            return float(metric_values[0])
        if "score" in sample.metrics and sample.metrics["score"].value is not None:
            return float(sample.metrics["score"].value)
        return 1.0 if sample.passed else 0.0

    def _serialize_sample(self, sample: t.Any) -> dict[str, t.Any]:
        output = sample.output
        turns: list[dict[str, t.Any]] | None = None
        output_summary: str | None = None
        if isinstance(output, Trajectory):
            turns = trajectory_to_turns(output)
            output_summary = output.get_summary()

        return {
            "input": sample.input,
            "output": output_summary,
            "metrics": self._metric_scores(sample),
            "passed": sample.passed,
            "error": str(sample.error) if sample.error else None,
            "turns": turns,
        }

    def _metric_scores(self, sample: t.Any) -> dict[str, float]:
        return {
            name: float(metric.value)
            for name, metric in sample.metrics.items()
            if metric.value is not None
        }

    def _format_feedback(self, *, score: float, trajectory: dict[str, t.Any]) -> str:
        parts = [f"Score: {score:.4f}"]
        error = trajectory.get("error")
        if error:
            parts.append(f"Error: {error}")
        metrics = trajectory.get("metrics")
        if metrics:
            parts.append(f"Metrics: {metrics}")
        return " | ".join(parts)
