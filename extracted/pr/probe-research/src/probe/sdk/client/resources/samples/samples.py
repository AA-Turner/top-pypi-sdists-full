"""SampleReadsMixin, Client's methods: the RL sample store's reads (list, show, compare, stats, capture,
weights, tasks, logs, tokens, best checkpoint), each a dict as the route answers it, and SamplesResource
(client.samples), the same reads as the contract's models (twin: app/runs/samples)."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from ...resource import Resource

if TYPE_CHECKING:
    from .....generated.samples import (
        BestCheckpoint,
        Capture,
        SampleCompare,
        SampleList,
        SampleLog,
        SampleOut,
        SampleStats,
        SampleTokens,
        TaskCurve,
        TaskDetail,
        TaskList,
        WeightList,
    )


def _build_query(**values: Any) -> dict[str, Any]:
    """Query parameters with None dropped and lists joined by commas (`by=step,result`); a tuple is
    a repeated parameter (`at=...&at=...`)."""
    query: dict[str, Any] = {}
    for name, value in values.items():
        if value is None or value == [] or value == ():
            continue
        if isinstance(value, bool):
            query[name] = "true" if value else "false"
        elif isinstance(value, tuple):
            query[name] = [str(item) for item in value]
        elif isinstance(value, list):
            query[name] = ",".join(str(item) for item in value)
        else:
            query[name] = value
    return query


def _build_where(where: Mapping[str, Any] | Iterable[str] | None) -> list[str] | None:
    """`--where scenario.set=P2` filters as the routes take them: `key:value` items."""
    if where is None:
        return None
    if isinstance(where, Mapping):
        return [f"{key}:{value}" for key, value in where.items()]
    return [item.replace("=", ":", 1) if ":" not in item else item for item in where]


def _get_contract():
    """The sample contract's models, imported on first typed read (about 80 ms)."""
    from .....generated import samples

    return samples


def _quote(value: str) -> str:
    return quote(str(value), safe="")


class SampleReadsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def list_samples(
        self,
        run_id: str,
        *,
        step: int | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
        split: str | None = None,
        result: str | None = None,
        outcome: str | None = None,
        reward: float | None = None,
        task_id: str | None = None,
        where: Mapping[str, Any] | Iterable[str] | None = None,
        include: Iterable[str] | None = None,
        stale_after: str | None = None,
        grep: str | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> dict:
        """`GET /v1/runs/{id}/samples`: a page of sample rows (`SampleList`), the response cut to
        4 KiB. ``include``: `dropped`, and `rewound` for the abandoned branch; ``stale_after``: the
        in-flight rows silent this long (`10m`); ``grep``: text in the response, turns or log tail."""
        wanted = list(include or ())
        query = _build_query(
            step=step,
            step_from=step_from,
            step_to=step_to,
            split=split,
            result=result,
            outcome=outcome,
            reward=reward,
            task=task_id,
            where=_build_where(where),
            include=[item for item in wanted if item != "rewound"],
            include_rewound=True if "rewound" in wanted else None,
            stale_after=stale_after,
            grep=grep,
            cursor=cursor,
            limit=limit,
        )
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/samples", params=query)

    def get_sample(self, sample_id: str) -> dict:
        """`GET /v1/samples/{id}`: one merged sample, its text whole (`SampleOut`)."""
        return self.transport.get(f"/v1/samples/{_quote(sample_id)}")

    def get_sample_log(self, sample_id: str) -> dict:
        """`GET /v1/samples/{id}/logs`: one sample's full log (`SampleLog`)."""
        return self.transport.get(f"/v1/samples/{_quote(sample_id)}/logs")

    def get_sample_tokens(self, sample_id: str, *, start: int | None = None, end: int | None = None) -> dict:
        """`GET /v1/samples/{id}/tokens`: a slice of its per-token arrays (`SampleTokens`)."""
        query = _build_query(start=start, end=end)
        return self.transport.get(f"/v1/samples/{_quote(sample_id)}/tokens", params=query)

    def compare_samples(
        self,
        task_id: str,
        at: Iterable[str],
        *,
        match: Iterable[str] | None = None,
        split: str | None = None,
    ) -> dict:
        """`GET /v1/samples/compare`: one task instance at each ``at`` (`RUN@step:0`,
        `RUN@version:41`, `RUN@checkpoint:best(eval/val)`), as `SampleCompare`."""
        query = _build_query(task=task_id, at=tuple(at), match=tuple(match or ()), split=split)
        return self.transport.get("/v1/samples/compare", params=query)

    def get_sample_stats(
        self,
        run_ids: str | Iterable[str],
        *,
        by: Iterable[str] = ("step",),
        measure: Iterable[str] = ("mean_reward", "count"),
        where: Mapping[str, Any] | Iterable[str] | None = None,
        pass_rule: str | None = None,
        include: Iterable[str] | None = None,
        split: str | None = None,
    ) -> dict:
        """`GET /v1/runs/{id}/samples/stats`: grouped measures (`SampleStats`). Several runs read
        side by side (`runs=a,b`)."""
        runs = [run_ids] if isinstance(run_ids, str) else list(run_ids)
        query = _build_query(
            by=list(by),
            measure=list(measure),
            where=_build_where(where),
            **{"pass": pass_rule},
            include=list(include or ()),
            split=split,
            runs=runs if len(runs) > 1 else None,
        )
        return self.transport.get(f"/v1/runs/{_quote(runs[0])}/samples/stats", params=query)

    def get_sample_capture(self, run_id: str) -> dict:
        """`GET /v1/runs/{id}/samples/capture`: is the capture complete? Yes or no, with the first
        reasons (`Capture`)."""
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/samples/capture")

    def list_weight_versions(self, run_id: str) -> dict:
        """`GET /v1/runs/{id}/samples/weights`: every weight push and its checkpoint (`WeightList`)."""
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/samples/weights")

    def list_sample_tasks(
        self,
        run_id: str,
        *,
        sort: str | None = None,
        split: str | None = None,
        where: Mapping[str, Any] | Iterable[str] | None = None,
        runs: Iterable[str] | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> dict:
        """`GET /v1/runs/{id}/tasks`: the run's task instances with their totals (`TaskList`); `split` train (the
        default), eval or sft."""
        query = _build_query(
            sort=sort, split=split, where=_build_where(where), runs=list(runs or ()), cursor=cursor, limit=limit
        )
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/tasks", params=query)

    def get_sample_task(self, run_id: str, task_id: str) -> dict:
        """`GET /v1/runs/{id}/tasks/{task_id}`: what the task is, with its totals (`TaskDetail`)."""
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/tasks/{_quote(task_id)}")

    def list_task_samples(self, run_id: str, task_id: str, *, cursor: str | None = None) -> dict:
        """`GET /v1/runs/{id}/tasks/{task_id}/samples`: every sample of one task (`SampleList`)."""
        query = _build_query(cursor=cursor)
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/tasks/{_quote(task_id)}/samples", params=query)

    def get_task_curve(
        self,
        run_id: str,
        task_id: str,
        *,
        measure: Iterable[str] = ("mean_reward", "min", "max", "count"),
        runs: Iterable[str] | None = None,
    ) -> dict:
        """`GET /v1/runs/{id}/tasks/{task_id}/curve`: one point per step, per run (`TaskCurve`)."""
        query = _build_query(measure=list(measure), runs=list(runs or ()))
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/tasks/{_quote(task_id)}/curve", params=query)

    def get_best_checkpoint(self, run_id: str, metric: str, *, mode: str = "max", is_from_evals: bool = False) -> dict:
        """`GET /v1/runs/{id}/checkpoints/best`: the checkpoint whose step's value of ``metric`` is
        best, with its lineage (`BestCheckpoint`). Never a guess: a named metric. ``is_from_evals``:
        read it from the eval runs that used each checkpoint, not from this run's own points."""
        query = _build_query(metric=metric, mode=mode, from_evals=is_from_evals or None)
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/checkpoints/best", params=query)


class SamplesResource(Resource):
    """`client.samples`: the sample reads as the contract's models (`probe.generated.samples`)."""

    __slots__ = ()

    def list(self, run_id: str, **filters: Any) -> "SampleList":
        """A page of a run's samples (`Client.list_samples`)."""
        return self._to_model(_get_contract().SampleList, self._client.list_samples(run_id, **filters))

    def get(self, sample_id: str) -> "SampleOut":
        return self._to_model(_get_contract().SampleOut, self._client.get_sample(sample_id))

    def get_log(self, sample_id: str) -> "SampleLog":
        return self._to_model(_get_contract().SampleLog, self._client.get_sample_log(sample_id))

    def get_tokens(self, sample_id: str, *, start: int | None = None, end: int | None = None) -> "SampleTokens":
        return self._to_model(_get_contract().SampleTokens, self._client.get_sample_tokens(sample_id, start=start, end=end))

    def compare(self, task_id: str, at: Iterable[str], **options: Any) -> "SampleCompare":
        return self._to_model(_get_contract().SampleCompare, self._client.compare_samples(task_id, at, **options))

    def get_stats(self, run_ids: str | Iterable[str], **options: Any) -> "SampleStats":
        return self._to_model(_get_contract().SampleStats, self._client.get_sample_stats(run_ids, **options))

    def get_capture(self, run_id: str) -> "Capture":
        return self._to_model(_get_contract().Capture, self._client.get_sample_capture(run_id))

    def list_weights(self, run_id: str) -> "WeightList":
        return self._to_model(_get_contract().WeightList, self._client.list_weight_versions(run_id))

    def list_tasks(self, run_id: str, **options: Any) -> "TaskList":
        return self._to_model(_get_contract().TaskList, self._client.list_sample_tasks(run_id, **options))

    def get_task(self, run_id: str, task_id: str) -> "TaskDetail":
        return self._to_model(_get_contract().TaskDetail, self._client.get_sample_task(run_id, task_id))

    def list_task_samples(self, run_id: str, task_id: str, *, cursor: str | None = None) -> "SampleList":
        return self._to_model(_get_contract().SampleList, self._client.list_task_samples(run_id, task_id, cursor=cursor))

    def get_task_curve(self, run_id: str, task_id: str, **options: Any) -> "TaskCurve":
        return self._to_model(_get_contract().TaskCurve, self._client.get_task_curve(run_id, task_id, **options))

    def get_best_checkpoint(self, run_id: str, metric: str, **options: Any) -> "BestCheckpoint":
        return self._to_model(_get_contract().BestCheckpoint, self._client.get_best_checkpoint(run_id, metric, **options))
