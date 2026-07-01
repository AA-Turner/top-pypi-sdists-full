"""Agent.Judge — specialized agent for evaluating trajectories against a rubric.

Thin wrapper over ``dreadnode.scorers.judge.llm_judge`` that adapts the scorer
to consume a full :class:`Trajectory` (multi-turn message log) rather than a
single output string. Used by the hosted training ``llm_judge`` verification
method and by anyone grading rollouts in a notebook.

Exposed as ``Agent.Judge(...)`` (class attribute) and as ``AgentJudge`` directly
from ``dreadnode.agents``.
"""

import typing as t
from dataclasses import dataclass, field
from pathlib import Path

from dreadnode.core.metric import Metric

if t.TYPE_CHECKING:
    from dreadnode.agents.trajectory import Trajectory
    from dreadnode.core.scorer import Scorer


@dataclass(slots=True)
class JudgeResult:
    """Structured result of an :class:`AgentJudge` evaluation.

    Attributes:
        passed: Whether the trajectory cleared the judge's passing threshold.
        score: Scalar in ``[0, 1]`` — the rubric-driven judge score.
        reason: Free-text rationale returned by the judge LLM.
        metrics: Raw metric list from the underlying scorer (score metric
            first, followed by the boolean pass metric).
    """

    passed: bool
    score: float
    reason: str
    metrics: list[Metric] = field(default_factory=list)


class AgentJudge:
    """Specialized agent that evaluates a :class:`Trajectory` against a rubric.

    Example::

        from dreadnode.agents import Agent

        judge = Agent.Judge(
            model="openai/gpt-4o",
            rubric="rce",
            passing_threshold=0.7,
        )
        result = await judge.evaluate(rollout.trajectory)
        if result.passed:
            print("win!", result.score, result.reason)

    Reuses the production :func:`dreadnode.scorers.judge.llm_judge` scorer
    (rubric YAML loading, XML response parsing, fallback regex, etc.) — this
    class only adapts the transcript shape and surfaces a :class:`JudgeResult`.
    """

    def __init__(
        self,
        *,
        model: str,
        rubric: str | Path,
        passing_threshold: float = 0.5,
        system_prompt: str | None = None,
        model_params: dict[str, t.Any] | None = None,
    ) -> None:
        if not 0.0 <= passing_threshold <= 1.0:
            raise ValueError(
                f"passing_threshold must be between 0.0 and 1.0 (got {passing_threshold!r})"
            )

        # Lazy import keeps agents/__init__ import graph cheap — scorers.judge
        # pulls in yaml + the rubrics dir.
        from dreadnode.scorers.judge import llm_judge

        self._model = model
        self._rubric = rubric
        self._passing_threshold = passing_threshold
        self._system_prompt = system_prompt
        self._model_params = model_params
        self._scorer: Scorer[t.Any] = llm_judge(
            model=model,
            rubric=rubric,
            passing=lambda score: score >= passing_threshold,
            system_prompt=system_prompt,
            model_params=model_params,
        )

    @property
    def model(self) -> str:
        return self._model

    @property
    def rubric(self) -> str | Path:
        return self._rubric

    @property
    def passing_threshold(self) -> float:
        return self._passing_threshold

    async def evaluate(
        self,
        trajectory: "Trajectory",
        *,
        context: dict[str, t.Any] | None = None,
    ) -> JudgeResult:
        """Score ``trajectory`` against the configured rubric.

        Flattens ``trajectory.messages`` to a transcript formatted as
        ``[role] content`` lines, optionally prepended with a
        ``# Task context`` block built from ``context`` (task instruction,
        env service URLs, flag hints, etc.).

        Args:
            trajectory: The agent run to evaluate. Uses ``trajectory.messages``
                which already chains per-step messages in chat order.
            context: Optional per-call context merged into the judge's input.
                Good use: pass the rendered task instruction and any known
                ground-truth hints so the judge can evaluate faithfulness.

        Returns:
            A :class:`JudgeResult` with ``passed`` / ``score`` / ``reason``.

        Raises:
            ValueError: if the scorer returned fewer than two metrics (the
                scorer contract is score metric + pass metric).
        """

        transcript = self._trajectory_to_transcript(trajectory, context=context)
        metrics = await self._scorer.normalize_and_score(transcript)
        if not metrics:
            raise ValueError(
                "AgentJudge scorer returned no metrics — check the judge model's output format."
            )

        score_metric = metrics[0]
        score = float(score_metric.value)
        reason = str(score_metric.attributes.get("reason", ""))

        # Second metric is the boolean pass flag (see scorers/judge.py). If
        # absent, fall back to threshold comparison so callers still get a
        # sensible ``passed`` value.
        if len(metrics) >= 2:
            passed = bool(metrics[1].value)
        else:
            passed = score >= self._passing_threshold

        return JudgeResult(
            passed=passed,
            score=score,
            reason=reason,
            metrics=list(metrics),
        )

    @staticmethod
    def _trajectory_to_transcript(
        trajectory: "Trajectory",
        *,
        context: dict[str, t.Any] | None = None,
    ) -> str:
        """Render a transcript the judge LLM can consume.

        Format:
            # Task context
            - key: value
            - ...

            # Conversation transcript
            [system] ...
            [user] ...
            [assistant] ...
            ...

        Context is optional. The conversation section always appears, even
        for empty trajectories (judge then scores on instruction only).
        """

        lines: list[str] = []
        if context:
            lines.append("# Task context")
            for key, value in context.items():
                lines.append(f"- {key}: {value}")
            lines.append("")
        lines.append("# Conversation transcript")
        for msg in trajectory.messages:
            role = getattr(msg, "role", "unknown")
            content = getattr(msg, "content", "") or ""
            lines.append(f"[{role}] {content}")
        return "\n".join(lines)


__all__ = ["AgentJudge", "JudgeResult"]
