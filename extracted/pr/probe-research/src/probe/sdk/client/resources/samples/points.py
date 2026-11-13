"""SamplePointsMixin, Client's methods: the per-sample metrics' reads (the keys, a key's series, one sample's points,
training capture), each a dict as the route answers it (twin: app/runs/samples/points)."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote


def _quote(value: Any) -> str:
    return quote(str(value), safe="")


def _drop_none(**values: Any) -> dict[str, Any]:
    return {name: value for name, value in values.items() if value is not None}


class SamplePointsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def list_sample_point_keys(self, run_id: str) -> dict:
        """`GET /v1/runs/{id}/samples/points/keys`: every key the run logged per sample, by split (`PointKeyList`)."""
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/samples/points/keys")

    def get_sample_point_series(
        self,
        run_id: str,
        key: str,
        *,
        split: str | None = None,
        by: str | None = None,
        agg: str | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
    ) -> dict:
        """`GET /v1/runs/{id}/samples/points?key=`: one key's series by step, update or the whole run, with its sums
        and weights (`PointSeries`)."""
        query = _drop_none(key=key, split=split, by=by, agg=agg, step_from=step_from, step_to=step_to)
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/samples/points", params=query)

    def get_sample_points(self, sample_id: str, *, key: str | None = None) -> dict:
        """`GET /v1/samples/{id}/points`: one sample's points and loss bookkeeping, or why it has none
        (`SamplePoints`)."""
        return self.transport.get(f"/v1/samples/{_quote(sample_id)}/points", params=_drop_none(key=key))

    def get_sample_points_capture(self, run_id: str, *, step_from: int | None = None,
                                  step_to: int | None = None) -> dict:  # fmt: skip
        """`GET /v1/runs/{id}/samples/points/capture`: per step, declared vs received and both checks
        (`PointsCapture`)."""
        query = _drop_none(step_from=step_from, step_to=step_to)
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/samples/points/capture", params=query)
