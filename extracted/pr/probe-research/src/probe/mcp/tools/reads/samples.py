"""samples: the RL sample store's reads in one tool (the five questions, the task view, the samples running now,
one watched sample's turns), each the route's answer. Read-only: agents cancel and retry with the CLI."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from mcp.server.fastmcp.exceptions import ToolError

from ....foundation.compat.compat import StrEnum


class SampleView(StrEnum):
    """What to read. `live`: the samples running now, slow, hung or abandoned, and what is failing (`run`, `state`,
    `hung_after`). `turns`: a watched sample's turns (`run`, `sample` = a live row's `attempt_id`, `after`).
    `list`: a run's samples (`step`, `result`, `reward`, `split`, `where`, `include`, `grep`). `show` / `logs`: one
    sample whole / its full log (`sample` = a sample id). `stats`: grouped measures (`run`, `by`, `measure`,
    `pass_rule`, `where`). `capture`: did every sample arrive, and what each producer cannot capture (`run`). `tasks`: the run's tasks; `task`,
    `task_samples`, `curve`: one `task`. `compare`: one `task` `at` steps or checkpoints. `weights`: weight versions.
    `best_checkpoint`: by `metric`, `mode`. `points`: per-sample metrics: the run's keys (`run`), one key's series
    (`run`, `metric` = the key, `split`, `by` step|update|run), or one sample's (`sample`, optional `metric`).
    `points_capture`: per step, declared vs received and the loss checks (`run`)."""

    LIVE = "live"
    TURNS = "turns"
    LIST = "list"
    SHOW = "show"
    LOGS = "logs"
    STATS = "stats"
    CAPTURE = "capture"
    TASKS = "tasks"
    TASK = "task"
    TASK_SAMPLES = "task_samples"
    CURVE = "curve"
    COMPARE = "compare"
    WEIGHTS = "weights"
    BEST_CHECKPOINT = "best_checkpoint"
    POINTS = "points"
    POINTS_CAPTURE = "points_capture"


@dataclass(frozen=True)
class SampleQuery:
    """The tool's arguments; each view reads the ones it names."""

    run: str = ""
    sample: str = ""
    task: str = ""
    step: int | None = None
    result: str = ""
    reward: float | None = None
    split: str = ""
    where: list[str] = field(default_factory=list)
    include: list[str] = field(default_factory=list)
    grep: str = ""
    by: list[str] = field(default_factory=list)
    measure: list[str] = field(default_factory=list)
    pass_rule: str = ""
    at: list[str] = field(default_factory=list)
    metric: str = ""
    mode: str = ""
    state: list[str] = field(default_factory=list)
    hung_after: str = ""
    after: int | None = None
    cursor: str | None = None
    limit: int | None = None


def _list_samples(client: Any, query: SampleQuery) -> dict:
    return client.list_samples(query.run, step=query.step, result=query.result or None, reward=query.reward,
                               split=query.split or None, where=query.where or None, include=query.include,
                               grep=query.grep or None, cursor=query.cursor, limit=query.limit)  # fmt: skip


def _get_stats(client: Any, query: SampleQuery) -> dict:
    return client.get_sample_stats(query.run, by=query.by or ["step"], measure=query.measure or ["mean_reward", "count"],
                                   where=query.where or None, pass_rule=query.pass_rule or None,
                                   include=query.include, split=query.split or None)  # fmt: skip


def _read_points(client: Any, query: SampleQuery) -> dict:
    """One sample's points, a key's series, or the run's keys, by which arguments are given."""
    if query.sample:
        return client.get_sample_points(query.sample, key=query.metric or None)
    if not query.run:
        raise ToolError("samples view=points needs `run` (its keys, or a `metric`'s series) or `sample`")
    if query.metric:
        return client.get_sample_point_series(query.run, query.metric, split=query.split or None,
                                              by=query.by[0] if query.by else None)  # fmt: skip
    return client.list_sample_point_keys(query.run)


#: Each view: the arguments it needs, and its read.
READS: dict[SampleView, tuple[tuple[str, ...], Callable[[Any, SampleQuery], dict]]] = {
    SampleView.LIVE: (("run",), lambda c, q: c.list_live_samples(
        q.run, states=q.state, hung_after=q.hung_after or None, limit=q.limit)),
    SampleView.TURNS: (("run", "sample"), lambda c, q: c.list_live_turns(q.run, q.sample, after=q.after,
                                                                         limit=q.limit)),
    SampleView.LIST: (("run",), _list_samples),
    SampleView.SHOW: (("sample",), lambda c, q: c.get_sample(q.sample)),
    SampleView.LOGS: (("sample",), lambda c, q: c.get_sample_log(q.sample)),
    SampleView.STATS: (("run",), _get_stats),
    SampleView.CAPTURE: (("run",), lambda c, q: c.get_sample_capture(q.run)),
    SampleView.TASKS: (("run",), lambda c, q: c.list_sample_tasks(
        q.run, split=q.split or None, where=q.where or None, cursor=q.cursor, limit=q.limit)),
    SampleView.TASK: (("run", "task"), lambda c, q: c.get_sample_task(q.run, q.task)),
    SampleView.TASK_SAMPLES: (("run", "task"), lambda c, q: c.list_task_samples(q.run, q.task, cursor=q.cursor)),
    SampleView.CURVE: (("run", "task"), lambda c, q: c.get_task_curve(
        q.run, q.task, measure=q.measure or ["mean_reward", "min", "max", "count"])),
    SampleView.COMPARE: (("task", "at"), lambda c, q: c.compare_samples(q.task, q.at, split=q.split or None)),
    SampleView.WEIGHTS: (("run",), lambda c, q: c.list_weight_versions(q.run)),
    SampleView.BEST_CHECKPOINT: (("run", "metric"), lambda c, q: c.get_best_checkpoint(
        q.run, q.metric, mode=q.mode or "max")),
    SampleView.POINTS: ((), _read_points),
    SampleView.POINTS_CAPTURE: (("run",), lambda c, q: c.get_sample_points_capture(q.run)),
}


class SamplesToolMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    def read_samples(self, view: SampleView, query: SampleQuery) -> dict:
        """One view's answer, as its route gives it (rl-next W34, D49, D61). A view missing an argument it needs
        is refused, naming it."""
        needed, read = READS[SampleView(view)]
        missing = [name for name in needed if not getattr(query, name)]
        if missing:
            raise ToolError(f"samples view={SampleView(view).value} needs "
                            f"{' and '.join(f'`{name}`' for name in missing)}")  # fmt: skip
        answer = dict(read(self.source.client, query) or {})
        return self._envelope(answer, next_cursor=answer.pop("next_cursor", None))
