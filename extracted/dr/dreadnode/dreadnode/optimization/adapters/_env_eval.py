"""Shared helpers for adapters that evaluate a candidate against a live
:class:`~dreadnode.core.environment.TaskEnvironment`.

Extracted from :class:`~dreadnode.optimization.adapters.env.CapabilityEnvAdapter`
so multiple adapters (CapabilityEnvAdapter today, SessionRuntimeAdapter next)
can share the per-row provisioning + scoring path. Behavior is unchanged
relative to the original ``CapabilityEnvAdapter._score_row`` /
``_build_trajectory_record`` / ``_score_from_metrics`` / ``_numeric_metrics``.

All functions are pure module-level helpers — no adapter state. Adapters
pass the row + agent + scorers + defaults; the helper provisions the
environment, runs the agent, scores, and returns a record dict in the
shape the existing ``make_reflective_dataset`` consumes.
"""

import statistics
import typing as t

from dreadnode.core.scorer import Metric, Scorer

if t.TYPE_CHECKING:
    from dreadnode.core.environment import TaskEnvironment


def numeric_metrics(metrics: dict[str, "Metric"]) -> dict[str, float]:
    """Project a metric map to ``{name: float_value}`` for numeric metrics."""
    return {
        name: float(metric.value) for name, metric in metrics.items() if metric.value is not None
    }


def score_from_metrics(
    metrics: dict[str, "Metric"],
    *,
    error: BaseException | None,
    score_name: str | None = None,
) -> float:
    """Reduce a metric map to a single trial score.

    - Errors short-circuit to 0.0.
    - With ``score_name`` set, the named metric's value is the score.
    - Otherwise, single-metric maps return that one value; multi-metric maps
      prefer ``"score"`` and fall back to the mean.
    """
    if error is not None or not metrics:
        return 0.0

    if score_name is not None:
        metric = metrics.get(score_name)
        return float(metric.value) if metric is not None and metric.value is not None else 0.0

    values = [float(metric.value) for metric in metrics.values() if metric.value is not None]
    if len(values) == 1:
        return values[0]
    if "score" in metrics and metrics["score"].value is not None:
        return float(metrics["score"].value)
    return statistics.mean(values) if values else 0.0


def build_trajectory_record(
    *,
    row: dict[str, t.Any],
    prompt: str,
    output: t.Any,
    metrics: dict[str, "Metric"],
    error: BaseException | None,
    task_ref: str,
) -> dict[str, t.Any]:
    """Build the per-row trajectory record consumed by ``make_reflective_dataset``.

    The shape is intentionally the same dict the original
    ``CapabilityEnvAdapter._build_trajectory_record`` produced so existing
    reflective-dataset projection in ``StackAwareCapabilityAdapter`` keeps
    working unchanged.
    """
    from dreadnode.agents.trajectory import Trajectory, trajectory_to_turns

    turns: list[dict[str, t.Any]] | None = None
    output_summary: str | None = None
    if isinstance(output, Trajectory):
        turns = trajectory_to_turns(output)
        output_summary = output.get_summary()
    elif output is not None:
        output_summary = str(output)

    return {
        "input": prompt,
        "row": row,
        "task_ref": task_ref,
        "output": output_summary,
        "metrics": numeric_metrics(metrics),
        "passed": error is None and any(bool(m.value) for m in metrics.values()),
        "error": repr(error) if error is not None else None,
        "turns": turns,
    }


async def score_row_with_task_env(
    *,
    row: dict[str, t.Any],
    agent: t.Any,
    dn: t.Any,
    fitted_scorers: list[t.Any],
    default_task_ref: str,
    timeout_sec: int | None,
    score_name: str | None,
    capture_traces: bool,
) -> dict[str, t.Any]:
    """Provision a TaskEnvironment for one row, run the agent, score the output.

    Per-row ``inputs`` template into the task's rendered instruction;
    ``task_ref`` on the row overrides ``default_task_ref``. The dataset's
    ``goal`` field is intentionally not consulted — for capability_env
    optimization the task's rendered instruction is authoritative. A task
    without a usable instruction raises rather than silently running the
    agent on an empty prompt.

    Returns ``{"output", "score", "objective_scores", "trajectory"}`` —
    same shape ``CapabilityEnvAdapter._score_row`` historically produced.
    """
    task_ref = str(row.get("task_ref") or default_task_ref)
    inputs = row.get("inputs") if isinstance(row.get("inputs"), dict) else None

    env: TaskEnvironment = dn.task_env(
        task_ref,
        inputs=inputs,
        timeout_sec=timeout_sec,
    )
    async with env:
        prompt = env.render_instruction() or env.instruction
        if not prompt:
            raise ValueError(
                f"Task {task_ref!r} has no instruction — capability_env "
                "optimization requires the task to drive the agent's prompt."
            )
        error: BaseException | None = None
        output: t.Any = None
        metrics: dict[str, Metric] = {}
        try:
            output = await agent.run(prompt)
            metric_map = await Scorer.evaluate(
                output,
                fitted_scorers,
                assert_scores=False,
            )
            metrics = {name: values[0] for name, values in metric_map.items() if values}
        except Exception as exc:
            error = exc

    trajectory = (
        build_trajectory_record(
            row=row,
            prompt=prompt,
            output=output,
            metrics=metrics,
            error=error,
            task_ref=task_ref,
        )
        if capture_traces
        else None
    )
    return {
        "output": output,
        "score": score_from_metrics(metrics, error=error, score_name=score_name),
        "objective_scores": numeric_metrics(metrics),
        "trajectory": trajectory,
    }
