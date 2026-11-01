"""RunViewsMixin, Client's methods: expression views and spans over a run's series (twin:
app/metric_views)."""

from __future__ import annotations
from typing import Any
from .....models import (
    MetricViewCreate,
    MetricViewPatch,
    MetricViewPreviewRequest)


def _view_spec(spec: Any) -> dict:
    """Normalize an expression-view spec through ``probe.expr``.

    An ``Expr``, a bare node dict, and a full ``{"expression": ...}`` mapping are
    all accepted and all validated. Imported lazily: ``expr`` pulls the generated
    models, and a client that never touches views should not pay for them.
    """
    from ....reads import expr as expr_module

    return expr_module.spec(spec)


class RunViewsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- expression views (read-time computed panels, research-os 0088) ------
    def create_view(self, run_id: str, name: str, spec: Any) -> dict:
        """Save an expression view on a run — a formula over series the run has
        already logged, evaluated at READ time (no points are stored).

        ``spec`` is a :class:`probe.expr.Expr`, a node dict, or a full
        ``{"expression": ...}`` mapping; all three normalize through
        :func:`probe.expr.spec`, which validates before anything reaches the
        wire. Names are unique per run among live views.

        Works on a COMPLETED run: a view reads the catalog, it does not append to
        the run's history. Nothing about finishing a run closes this door."""
        body = MetricViewCreate(name=name, spec=_view_spec(spec))
        return self.transport.post(
            f"/v1/runs/{run_id}/views", body.model_dump(mode="json", exclude_none=True)
        )

    def list_views(self, run_id: str) -> list[dict]:
        """Every live view on a run, with its spec and provenance."""
        return self.transport.get(f"/v1/runs/{run_id}/views")

    def update_view(
        self,
        view_id: str,
        *,
        name: str | None = None,
        spec: Any = None,
        expected_updated_at: str | None = None,
    ) -> dict:
        """Rename a view and/or replace its expression. Omitted fields are left
        alone — this is a PATCH, not a whole-row write.

        ``spec`` REPLACES the stored expression whole. ``expected_updated_at``
        is the view's ``updated_at`` as you read it: the server then refuses
        (409, carrying the current name, spec and ``updated_at``) instead of
        overwriting an edit made since. Omitted, the write is unconditional."""
        body: dict = {}
        if name is not None:
            body["name"] = name
        if spec is not None:
            body["spec"] = _view_spec(spec)
        if not body:
            raise ValueError("update_view needs a name or a spec to change")
        # AFTER the emptiness check: a precondition alone changes nothing.
        if expected_updated_at is not None:
            body["expected_updated_at"] = expected_updated_at
        return self.transport.patch(
            f"/v1/views/{view_id}",
            MetricViewPatch(**body).model_dump(mode="json", exclude_none=True),
        )

    def delete_view(self, view_id: str) -> None:
        """Soft-delete a view. The series it read are untouched."""
        self.transport.delete(f"/v1/views/{view_id}")

    def view_data(
        self,
        run_id: str,
        view_id: str,
        *,
        step_from: int | None = None,
        step_to: int | None = None,
        max_points: int | None = None,
    ) -> dict:
        """Evaluate a saved view and return its curve.

        Read the envelope, not just ``points``: ``missing_inputs`` names series
        the expression referenced that the run has none of, ``dropped_nonfinite``
        counts steps whose result was NaN/inf (a divide-by-zero), and
        ``truncated`` says the input scan hit its bound before the range ended.
        An empty ``points`` with a populated ``missing_inputs`` is a typo in the
        spec, not a run with no data."""
        params = {
            param: value
            for param, value in {
                "step_from": step_from,
                "step_to": step_to,
                "max_points": max_points,
            }.items()
            if value is not None
        }
        return self.transport.get(f"/v1/runs/{run_id}/views/{view_id}/data", params=params or None)

    def preview_view(
        self,
        run_id: str,
        spec: Any,
        *,
        step_from: int | None = None,
        step_to: int | None = None,
        max_points: int | None = None,
    ) -> dict:
        """Evaluate a spec WITHOUT saving it — same envelope as :meth:`view_data`.

        The check to run before :meth:`create_view`: a spec that names a series
        the run never logged comes back with ``missing_inputs`` here, instead of
        being saved as a panel that renders empty for everyone."""
        body = MetricViewPreviewRequest(
            spec=_view_spec(spec),
            step_from=step_from,
            step_to=step_to,
            **({"max_points": max_points} if max_points is not None else {}),
        )
        return self.transport.post(
            f"/v1/runs/{run_id}/views/preview",
            body.model_dump(mode="json", exclude_none=True),
        )

    def run_spans(
        self,
        run_id: str,
        *,
        span_type: str | None = None,
        parent_span_id: str | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        """Read a run's trajectory spans back (the write path is ``Run.span``)."""
        params = {
            k: v
            for k, v in {
                "span_type": span_type,
                "parent_span_id": parent_span_id,
                "step_from": step_from,
                "step_to": step_to,
                "limit": limit,
            }.items()
            if v is not None
        }
        return self.transport.get(f"/v1/runs/{run_id}/spans", params=params or None)

    def get_span(self, span_id: str) -> dict:
        return self.transport.get(f"/v1/spans/{span_id}")
