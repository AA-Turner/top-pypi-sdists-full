"""ChartsMixin (Client's methods) and ChartsResource (`client.charts`): save how one chart draws and how a
page lays out its sections (twin: app/runs/telemetry/charts). Layouts are behind the team flag `chart_layouts`."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from probe.foundation.compat.compat import StrEnum

from ... import errors
from ..ids import _is_uuid
from ..resource import Resource

CHART_SETTINGS_PATH = "/v1/chart-settings"
#: The reserved key of a page's settings row: it holds key_metrics, section_order, hidden_sections.
#: The team feature that turns every `chart` write on (`GET /v1/teams/features`).
CHART_LAYOUTS_FEATURE = "chart_layouts"
LAYOUTS_OFF_MESSAGE = "chart layouts are off for this team"
PAGE_ROW_KEY = "__probe_key_metrics_v1__"
MAX_KEY_METRICS = 12


class ChartXAxis(StrEnum):
    STEP = "step"
    WALL_CLOCK = "wall_clock"
    RELATIVE = "relative"


class ChartSmoothing(StrEnum):
    NONE = "none"
    EMA = "ema"
    SMA = "sma"
    GAUSSIAN = "gaussian"
    TWEMA = "twema"


#: Smoothings that take a window of points; the rest take a factor in [0, 1).
_WINDOWED = {ChartSmoothing.SMA, ChartSmoothing.GAUSSIAN}
#: The anchor field a scope kind is saved under.
_ANCHOR_FIELD = {"run": "run_id", "experiment": "experiment_id", "project": "project_id"}


def parse_smoothing(spec: str) -> dict[str, Any]:
    """``"ema:0.6"`` / ``"sma:10"`` / ``"none"`` as the settings fields it sets."""
    name, _, amount = str(spec).partition(":")
    try:
        method = ChartSmoothing(name.strip().lower())
    except ValueError:
        raise errors.ValidationError(
            f"smoothing {name!r} is not one of {', '.join(m.value for m in ChartSmoothing)}"
        ) from None
    fields: dict[str, Any] = {"smoothing": method.value}
    if method is ChartSmoothing.NONE:
        return fields
    try:
        if method in _WINDOWED:
            fields["smoothing_window"] = int(amount) if amount else 10
        else:
            fields["smoothing_factor"] = float(amount) if amount else 0.6
    except ValueError:
        raise errors.ValidationError(f"smoothing amount {amount!r} is not a number") from None
    return fields


def parse_x_axis(axis: str, *, kind: str) -> str | dict[str, Any]:
    """A built-in axis by name, else the metric ``[kind:]key`` as an exact metric selector."""
    try:
        return ChartXAxis(axis).value
    except ValueError:
        pass
    metric_kind, sep, metric_key = axis.partition(":")
    if not sep:
        metric_kind, metric_key = kind, axis
    if not metric_key:
        raise errors.ValidationError("name an x axis: step, wall_clock, relative or a metric key")
    return {"kind": metric_kind, "key": metric_key, "dimensions": {}}


class ChartsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- chart settings and layouts (`PUT /v1/chart-settings`) ----------------------------
    # `scope` is a run id, or a project or experiment (slug, uuid or `id:<uuid>`). Each save reads the
    # row first and merges, so setting one field never drops the others.

    def set_chart(
        self,
        scope: str,
        key: str,
        *,
        kind: str = "model",
        x_axis: str | None = None,
        smoothing: str | None = None,
        is_log_y: bool | None = None,
    ) -> dict:
        """Save how metric ``key`` draws in ``scope``: ``x_axis`` (``step``, ``wall_clock``,
        ``relative`` or a metric ``[kind:]key``), ``smoothing`` (``ema:0.6``, ``sma:10``, ``none``) and
        ``is_log_y``. Fields left None stay as they are. Returns the saved row."""
        self._require_chart_layouts()
        patch: dict[str, Any] = {}
        if x_axis is not None:
            patch["x_axis"] = parse_x_axis(x_axis, kind=kind)
        if smoothing is not None:
            patch.update(parse_smoothing(smoothing))
        if is_log_y is not None:
            patch["y_scale"] = "log" if is_log_y else "linear"
        if not patch:
            raise errors.ValidationError("nothing to set: give --x-axis, --smoothing or --log-y")
        return self._save_chart_settings(scope, key, patch, should_drop_amounts=bool(smoothing))

    def set_chart_layout(
        self,
        scope: str,
        *,
        key_metrics: Sequence[str] | None = None,
        order: Sequence[str] | None = None,
        hide: Sequence[str] | None = None,
        kind: str = "model",
    ) -> dict:
        """Save the page's key metrics (``[kind:]key`` each, at most 12), section ``order`` and
        ``hide`` (sections to hide). Fields left None stay. Needs the team flag ``chart_layouts``:
        without it the server answers 403 ``chart_layouts_off``."""
        self._require_chart_layouts()
        patch: dict[str, Any] = {}
        if key_metrics is not None:
            if len(key_metrics) > MAX_KEY_METRICS:
                raise errors.ValidationError(f"a page has at most {MAX_KEY_METRICS} key metrics")
            patch["key_metrics"] = [_to_metric_pair(item, kind) for item in key_metrics]
        if order is not None:
            patch["section_order"] = list(dict.fromkeys(order))
        if hide is not None:
            patch["hidden_sections"] = list(dict.fromkeys(hide))
        if not patch:
            raise errors.ValidationError("nothing to set: give --key-metrics, --order or --hide")
        return self._save_chart_settings(scope, PAGE_ROW_KEY, patch)

    def _require_chart_layouts(self) -> None:
        """Refuse before any read or write unless the team has the flag: agent chart writes are
        off for every team by default (the dashboard's own saves use the route directly)."""
        if not self.supports_team_feature(CHART_LAYOUTS_FEATURE):
            raise errors.ScopeError(LAYOUTS_OFF_MESSAGE)

    def _resolve_chart_anchor(self, scope: str) -> dict[str, str]:
        ref = str(scope).strip()
        bare = ref.removeprefix("id:")
        found = self.get_scope(bare) if (ref.startswith("id:") or _is_uuid(bare)) else self.get_scope_by_slug(ref)
        field = _ANCHOR_FIELD.get(str(found.get("kind")))
        if field is None:
            raise errors.NotFoundError(f"{ref!r} is not a run, experiment or project")
        return {field: str(found["id"])}

    def _save_chart_settings(
        self, scope: str, key: str, patch: dict[str, Any], *, should_drop_amounts: bool = False
    ) -> dict:
        anchor = self._resolve_chart_anchor(scope)
        target = {**anchor, "metric_key": key}
        rows = self.transport.get(CHART_SETTINGS_PATH, params=target).get("rows") or []
        own = next((row for row in rows if _is_own_row(row, anchor, key)), None)
        settings = {k: v for k, v in ((own or {}).get("settings") or {}).items() if k != "_provenance"}
        if should_drop_amounts:
            # A new method brings its own amount; the old method's would be a silent stray.
            for stale in ("smoothing_factor", "smoothing_window"):
                settings.pop(stale, None)
        settings.update(patch)
        body: dict[str, Any] = {**target, "settings": settings}
        if own and own.get("updated_at"):
            body["expected_updated_at"] = own["updated_at"]
        return self.transport.put(CHART_SETTINGS_PATH, body)


def _is_own_row(row: dict, anchor: dict[str, str], key: str) -> bool:
    """The chain read answers parent tiers too; only the row on this exact anchor and key is ours."""
    return row.get("metric_key") == key and all(str(row.get(field)) == value for field, value in anchor.items())


def _to_metric_pair(item: str, default_kind: str) -> dict[str, str]:
    kind, sep, key = str(item).partition(":")
    if not sep:
        kind, key = default_kind, str(item)
    if not key:
        raise errors.ValidationError(f"{item!r} is not a metric: use key or kind:key")
    return {"kind": kind, "key": key}


class ChartsResource(Resource):
    """`client.charts`: save chart settings and page layouts."""

    __slots__ = ()

    def set(self, scope: str, key: str, **options: Any) -> dict:
        """`Client.set_chart`."""
        return self._client.set_chart(scope, key, **options)

    def set_layout(self, scope: str, **options: Any) -> dict:
        """`Client.set_chart_layout`."""
        return self._client.set_chart_layout(scope, **options)
