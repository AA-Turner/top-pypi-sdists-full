"""PointWriter: one producer's per-sample metrics and update records, checked and journaled as ops on their own route
(`POST /v1/runs/{id}/samples/points`), never merged with `/samples/batch` ops. Behind `run.samples.log_metrics`,
`log_metrics_many` and `log_update`; the caller (`RunSamples`) catches and counts every failure."""

from __future__ import annotations

import threading
from collections.abc import Iterable, Mapping
from typing import TYPE_CHECKING, Any

from .....foundation.safe_warn import safe_warn as _diagnostics
from ....routes import WriteOp, path_for
from .rows import ROW_FIELDS, build_point_row, build_update_row

if TYPE_CHECKING:
    from ..samples import RunSamples

#: Items and bytes per journaled op, the samples ops' caps (the drain merges points ops up to the same).
OP_MAX_ITEMS = 1_000
OP_MAX_BYTES = 4 * 1024 * 1024
#: The arguments a `log_metrics_many` row may carry beside its bookkeeping.
_ROW_ARGUMENTS = frozenset({"sample_key", "key", "metrics", "step", "update", "split", "weights", "agg"})


class PointWriter:
    """The points side of one `RunSamples` view (its producer)."""

    def __init__(self, samples: RunSamples) -> None:
        self._samples = samples
        #: Flattened nested keys this view has made: `run.log`'s budget on keys minted from nested dicts.
        self._known: set[str] = set()
        self._warned_left: set[str] = set()
        self._lock = threading.Lock()

    def log_metrics(self, sample_key: str, metrics: Mapping[str, Any], *, step: int, update: int | None,
                    split: str | None, weights: Any, agg: Any, fields: Mapping[str, Any]) -> int:  # fmt: skip
        row = self._build(sample_key, metrics, step=step, update=update, split=split, weights=weights, agg=agg,
                          fields=fields)  # fmt: skip
        self._send([row], [])
        return 1

    def log_metrics_many(self, rows: Iterable[Mapping[str, Any]]) -> int:
        """Each row checked alone (a bad one is counted on `failures` and the rest go); one op for all of them."""
        built = []
        for given in rows:
            try:
                built.append(self._build_from(given))
            except Exception as exc:  # noqa: BLE001 -- one bad row never costs the rest
                self._samples._record_failure("log_metrics_many", exc)
        self._send(built, [])
        return len(built)

    def log_update(self, step: int, update: int | None, *, level: str, fields: Mapping[str, Any]) -> None:
        with self._lock:
            row, left = build_update_row(step, update, level, fields, self._known)
        self._warn_left("log_update", left)
        self._send([], [row])

    def _build_from(self, given: Mapping[str, Any]) -> dict:
        row = dict(given)
        sample_key = row.pop("sample_key", None) or row.pop("key", None)
        if sample_key is None or "metrics" not in row or "step" not in row:
            raise ValueError("a log_metrics_many row needs sample_key, metrics and step")
        stray = sorted(set(row) - _ROW_ARGUMENTS - ROW_FIELDS)
        if stray:
            raise TypeError(f"a log_metrics_many row does not take {', '.join(stray)}")
        fields = {name: row.pop(name) for name in list(row) if name in ROW_FIELDS}
        return self._build(sample_key, row["metrics"], step=row["step"], update=row.get("update"),
                           split=row.get("split"), weights=row.get("weights"), agg=row.get("agg"), fields=fields)  # fmt: skip

    def _build(self, sample_key: str, metrics: Mapping[str, Any], **arguments: Any) -> dict:
        with self._lock:
            row, left = build_point_row(sample_key, metrics, known=self._known, **arguments)
        self._warn_left("log_metrics", left)
        return row

    def _warn_left(self, call: str, left: list[str]) -> None:
        """Say once per name what a call left out (not a finite number: sent as unknown, never as 0)."""
        new = [name for name in left if name not in self._warned_left]
        if new:
            self._warned_left.update(new)
            _diagnostics.warn(f"probe: run.samples.{call} left out {', '.join(sorted(new)[:5])} (not a finite "
                              "number); warned once per key")  # fmt: skip

    def _send(self, points: list[dict], updates: list[dict]) -> None:
        """Journal the rows as ops of at most `OP_MAX_ITEMS` items and `OP_MAX_BYTES`."""
        from ..wire import measure_bytes

        body: dict[str, list] = {}
        count = size = 0
        for name, item in [*(("points", p) for p in points), *(("updates", u) for u in updates)]:
            weight = measure_bytes(item)
            if count and (count + 1 > OP_MAX_ITEMS or size + weight > OP_MAX_BYTES):
                self._write_op(body)
                body, count, size = {}, 0, 0
            body.setdefault(name, []).append(item)
            count += 1
            size += weight
        if body:
            self._write_op(body)

    def _write_op(self, lists: dict[str, list]) -> None:
        run = self._samples._run
        body = run._stamp_writer({"producer": self._samples.producer, **lists})
        body["write_epoch"] = run.write_epoch or 1  # required, never a fence (as `/samples/batch`)
        run._progress.bump()
        run._client.write("POST", path_for(WriteOp.SAMPLE_POINTS, run.id), body, strict=False)
