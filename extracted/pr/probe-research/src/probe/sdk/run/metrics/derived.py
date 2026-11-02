"""DerivedMetricsMixin, Run's methods: derived series and expression views on the run, and the
server-side reads of its metrics."""

from __future__ import annotations
from typing import Any
from ....models import (
    DerivedProvenance,
    MetricBatch,
    MetricPointIn)
from probe.sdk.routes import WriteOp, path_for


def _metric_batch_body(
    points: list[MetricPointIn], *, provenance: DerivedProvenance | None = None
) -> dict:
    """Serialize a metric batch. Origin is BATCH-level by design (0087): a derived
    computation writes one logical stream, so a mixed-origin batch is
    unrepresentable rather than merely discouraged.

    A logged batch stays byte-identical to what it has always been — `origin` and
    `provenance` are None-excluded, so nothing new rides on the hot path."""
    batch = MetricBatch(
        points=points,
        origin="derived" if provenance is not None else None,
        provenance=provenance,
    )
    body = batch.model_dump(mode="json", exclude_none=True)
    if provenance is not None:
        # `inputs` are SeriesSelectors, whose READ-side fields (smoothing_factor,
        # smoothing_window, x_axis...) carry defaults. Dumped normally they land
        # in stored provenance as smoothing settings on a lineage record that has
        # nothing to do with smoothing — noise a human then has to discount.
        # exclude_defaults keeps only what the caller actually declared.
        body["provenance"] = provenance.model_dump(
            mode="json", exclude_none=True, exclude_defaults=True
        )
    return body


def _derived_provenance(
    *,
    producer: str,
    note: str | None,
    inputs: list[Any] | None,
    code_ref: str | None,
    kind: str,
) -> DerivedProvenance:
    """Build the provenance record for a derived write.

    `inputs` is self-declared lineage: which stored series the computation read.
    Bare strings are the common case and resolve to `{key, kind}` against the
    batch's own kind, so a caller writing `inputs=["eval/mean_reward"]` gets a
    real selector rather than a rejected body.
    """
    selectors = None
    if inputs:
        selectors = [
            {"key": item, "kind": kind} if isinstance(item, str) else item for item in inputs
        ]
    return DerivedProvenance(producer=producer, note=note, inputs=selectors, code_ref=code_ref)


class DerivedMetricsMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    # -- derived metrics (computed after the fact, research-os 0087) --------
    def log_derived(
        self,
        metrics: dict[str, float],
        *,
        step: int,
        producer: str,
        note: str | None = None,
        inputs: list[Any] | None = None,
        code_ref: str | None = None,
        kind: str = "model",
        wall_clock: str | None = None,
        dimensions: dict[str, Any] | None = None,
        agg: str | None = None,
        strict: bool | None = None,
    ):
        """Write metrics that were COMPUTED after the fact, not measured live.

        The door for an agent backfilling a metric nobody logged at training
        time — AUROC from stored predictions, a cumulative integral of reward, a
        rescored eval. It works on a **completed** run: the series catalog is a
        row store, so a finished run is not a sealed archive.

        ``producer`` is required and is the point — a derived series carries
        ``origin="derived"`` plus provenance saying what produced it, so nobody
        ever has to wonder whether a curve came from the training loop or from a
        notebook two weeks later. The server stamps ``computed_at`` and
        ``created_by`` on top; a client cannot forge either.

        ``step`` is required, unlike :meth:`log`. Auto-increment is a footgun
        here: a backfill lands on steps that already exist, and a counter
        starting at 0 on a fresh handle would silently write the wrong axis.

        ``inputs`` is best-effort lineage — which stored series the computation
        read. Pass metric keys as strings (resolved against ``kind``) or full
        selector dicts. Use :meth:`log_derived_series` to push a whole curve in
        one request rather than one call per step.

        A derived key that collides with an existing LOGGED series is refused
        for that series alone: the ingest door skips it, reports it loudly, and
        writes the rest of the batch. Origin is fixed at a series' first write.

        ``metrics`` must be flat: unlike :meth:`log`, nested dicts are NOT
        flattened here (every value must be a number).
        """
        numeric = {k: float(v) for k, v in metrics.items()}
        if not numeric:
            return None
        points = [
            MetricPointIn(
                key=key,
                kind=kind,
                value=value,
                step_index=int(step),
                wall_clock=wall_clock,
                dimensions=dimensions,
                agg=agg,
            )
            for key, value in numeric.items()
        ]
        body = _metric_batch_body(
            points,
            provenance=_derived_provenance(
                producer=producer, note=note, inputs=inputs, code_ref=code_ref, kind=kind
            ),
        )
        return self._client.write(
            "POST", path_for(WriteOp.METRICS, self.id), self._stamp_writer(body), strict=strict
        )

    def log_derived_series(
        self,
        key: str,
        points: Any,
        *,
        producer: str,
        note: str | None = None,
        inputs: list[Any] | None = None,
        code_ref: str | None = None,
        kind: str = "model",
        dimensions: dict[str, Any] | None = None,
        agg: str | None = None,
        strict: bool | None = None,
    ):
        """Push a whole derived CURVE in one request — the usual backfill shape.

        ``points`` is either a ``{step: value}`` mapping or an iterable of
        ``(step, value)`` pairs. One batch, one request: a 3000-step backfill
        through :meth:`log_derived` would be 3000 round trips, which is the
        difference between tooling and a demo.

        Provenance arguments mean exactly what they do on :meth:`log_derived`.
        """
        pairs = points.items() if hasattr(points, "items") else points
        rows = [
            MetricPointIn(
                key=key,
                kind=kind,
                value=float(value),
                step_index=int(step),
                dimensions=dimensions,
                agg=agg,
            )
            for step, value in pairs
        ]
        if not rows:
            return None
        body = _metric_batch_body(
            rows,
            provenance=_derived_provenance(
                producer=producer, note=note, inputs=inputs, code_ref=code_ref, kind=kind
            ),
        )
        return self._client.write(
            "POST", path_for(WriteOp.METRICS, self.id), self._stamp_writer(body), strict=strict
        )

    # -- expression views (read-time computed panels, research-os 0088) -----
    def views(self) -> list[dict]:
        """Every live expression view on this run."""
        return self._client.list_views(self.id)

    def create_view(self, name: str, spec: Any) -> dict:
        """Save an expression view — a formula over series this run already has,
        evaluated at read time. ``spec`` is a :class:`probe.expr.Expr`, a node
        dict, or a full ``{"expression": ...}`` mapping. See
        :meth:`Client.create_view`."""
        return self._client.create_view(self.id, name, spec)

    def view_data(self, view_id: str, **kw: Any) -> dict:
        """Evaluate a saved view; see :meth:`Client.view_data` for the envelope
        (``missing_inputs`` / ``dropped_nonfinite`` / ``truncated``)."""
        return self._client.view_data(self.id, view_id, **kw)

    def preview_view(self, spec: Any, **kw: Any) -> dict:
        """Evaluate a spec without saving it — the check to run before
        :meth:`create_view`."""
        return self._client.preview_view(self.id, spec, **kw)

    # -- metrics / coordinates (read) ---------------------------------------
    def grouped_metrics(self, key: str, **kw: Any) -> dict:
        """Server-side reduce/group over this run's points; see
        :meth:`Client.get_metrics_grouped` for the parameters and paging."""
        return self._client.get_metrics_grouped(self.id, key, **kw)

    def wide_metrics(self, **kw: Any) -> dict:
        """Step x metric table for this run; see :meth:`Client.get_metrics_wide`."""
        return self._client.get_metrics_wide(self.id, **kw)

    def export_points(self, **kw: Any):
        """Lossless raw-point generator for this run; see
        :meth:`Client.export_metric_points`."""
        return self._client.export_metric_points(self.id, **kw)

    def coordinates(self) -> list[dict]:
        """This run's coordinate catalog (0060); see
        :meth:`Client.list_run_coordinates`."""
        return self._client.list_run_coordinates(self.id)
