"""The three sibling files an app version uploads beside ``app.yaml``.

Normative reference: ``_contracts/appversion/00-SYNTHESIS.md`` §2 §4.

These are *not* manifest models. They mirror what the fe-market **Add version** form accepts,
character for character, because the app author uploads these exact bytes:

======================================  ===================================  ==================
file                                    form field                           shape
======================================  ===================================  ==================
``metrics.json``                        "Analytics Metrics (JSON File)"      **bare array**
``widgets.json``                        "Dashboard Widgets (JSON File)"      **bare array**
``post_processing_config.json``         "Post Processing Config (JSON File)" object, per model
======================================  ===================================  ==================

Two consequences shape every decision in this module.

**Nothing downstream validates these against reality.** ``be-application`` checks only that a
widget's ``dataKey`` resolves *within the uploaded config itself*; whether the engine emits that
key is checked in no repo. Declared-but-unpublished renders an empty chart, published-but-undeclared
is stored in ClickHouse and never read. Both are silent. That is what
:mod:`matrice_analytics.engine.testing.generate` checks 6 and 7 exist to catch, and this module is
the parsing layer beneath them.

**The models are deliberately permissive.** A field being *wrong* is a finding for the check to
report against the manifest, with a readable message and an index; it is not a parse failure here.
Only genuinely structural damage — the file is not an array, an entry is not an object, ``key`` is
missing — is a parse problem. Extra keys are kept and warned about rather than dropped, because
``be-application`` stores the array verbatim: a stray ``_comment`` really does reach production.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

__all__ = [
    "CHART_TYPES_RENDERED",
    "DATA_SOURCES",
    "METRICS_FILENAME",
    "POST_PROCESSING_FILENAME",
    "RESERVED_WIDGET_TOKENS",
    "WIDGETS_FILENAME",
    "ConfigProblem",
    "MetricEntry",
    "PostProcessingConfig",
    "WidgetBinding",
    "WidgetEntry",
]

#: The three filenames, as the guidelines name them.
METRICS_FILENAME = "metrics.json"
WIDGETS_FILENAME = "widgets.json"
POST_PROCESSING_FILENAME = "post_processing_config.json"

#: ``widgetDataSource.ts:2-7``. Anything else makes ``parseDataSources`` return ``None``, which
#: drops the widget before it renders — the PY-1c defect.
DATA_SOURCES: frozenset[str] = frozenset({"metric", "tracking_class"})

#: The live dashboard collapses everything except ``bar`` to a line (PY-1d,
#: ``ZoneWidgetChart.tsx:50-54``). Declaring ``gauge`` is not an error, it is just not honoured,
#: so this drives a warning rather than a failure.
CHART_TYPES_RENDERED: frozenset[str] = frozenset({"bar", "line"})

#: ``splitBatchBucketsFromConfig`` skips this literal token when building the dashboard's query
#: (``volumeAnalyticsHelpers.ts:167``), so a widget bound to it fetches nothing. It remains
#: perfectly valid as a ``metrics.json`` entry — the metrics union requests that separately.
RESERVED_WIDGET_TOKENS: frozenset[str] = frozenset({"total_count"})


@dataclass(frozen=True)
class ConfigProblem:
    """One thing wrong with one of the three files.

    Problems are *returned*, never raised: a malformed sibling file must not stop the rest of the
    suite from running, in the same way :func:`~matrice_analytics.engine.testing.generate._resolve_app`
    turns a load failure into data.
    """

    where: str
    message: str
    severity: Literal["error", "warning"] = "error"

    def __str__(self) -> str:
        return f"{self.where}: {self.message}"


@dataclass(frozen=True)
class WidgetBinding:
    """One resolved ``dataKey`` token paired with the source that says where to look it up.

    ``metric`` reads ``business_metrics[key]`` — our ``results-agg.metrics[].key``.
    ``tracking_class`` reads ``analytics[key]`` / ``analytics_totals[key]`` — our
    ``current_counts[].category``, i.e. an **entity name**, not a metric key. Two keyspaces, no
    cross-namespace fallback (``volumeAnalyticsHelpers.ts:385-424``).
    """

    token: str
    data_source: str


class _ConfigModel(BaseModel):
    """Base for the uploaded files.

    ``extra="allow"`` on purpose — see the module docstring. The manifest's ``ManifestModel`` uses
    ``extra="forbid"`` because a typo there is an app that cannot work; here a typo is an app that
    ships junk to Mongo, which is worth a warning and not a refusal to parse.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True, str_strip_whitespace=True)

    def extra_keys(self) -> tuple[str, ...]:
        return tuple(sorted(self.model_extra or {}))


class MetricEntry(_ConfigModel):
    """One element of ``metrics.json``.

    ``key`` is the join to ``app.yaml`` ``metrics[].key`` and to ``widgets.json`` ``dataKey``, by
    exact string match. ``aggType`` is camelCase on the wire and ``agg_type`` in the manifest; the
    alias carries that difference so a check can compare the two directly.
    """

    key: str
    name: str | None = None
    unit: str | None = None
    agg_type: str | None = Field(default=None, alias="aggType")
    category: str | None = None

    @field_validator("key")
    @classmethod
    def _key_must_be_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("key must be a non-empty string")
        return value


class WidgetEntry(_ConfigModel):
    """One element of ``widgets.json``."""

    key: str
    title: str | None = None
    chart_type: str | None = Field(default=None, alias="chartType")
    category: str | None = None
    data_key: str = Field(default="", alias="dataKey")
    data_source: str = Field(default="", alias="dataSource")

    @field_validator("key")
    @classmethod
    def _key_must_be_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("key must be a non-empty string")
        return value

    def tokens(self) -> tuple[str, ...]:
        """The ``dataKey`` CSV, split and trimmed. Blank falls back to the widget's own ``key``."""
        raw = self.data_key.strip() or self.key
        return tuple(part.strip() for part in raw.split(",") if part.strip())

    def resolve_bindings(self) -> tuple[tuple[WidgetBinding, ...], str | None]:
        """Pair each token with its source, or explain why the widget is invalid.

        Mirrors ``widgetKeySources`` / ``parseDataSources``. A single ``dataSource`` applies to
        every token; a CSV must be positionally 1:1 with ``dataKey``. **A length mismatch or an
        unknown source silently drops the whole widget on the live dashboard**, so this returns a
        reason rather than a partial binding.
        """
        tokens = self.tokens()
        if not tokens:
            return (), "dataKey is empty and the widget key is not usable as a fallback"

        sources = [part.strip() for part in self.data_source.split(",") if part.strip()]
        if not sources:
            return (), (
                "dataSource is missing; the dashboard treats an absent dataSource as an invalid "
                "widget and does not render it (PY-1c)"
            )

        unknown = sorted({source for source in sources if source not in DATA_SOURCES})
        if unknown:
            allowed = ", ".join(sorted(DATA_SOURCES))
            return (), f"dataSource {', '.join(repr(item) for item in unknown)} is not one of: {allowed}"

        if len(sources) == 1:
            return tuple(WidgetBinding(token, sources[0]) for token in tokens), None

        if len(sources) != len(tokens):
            return (), (
                f"dataKey has {len(tokens)} token(s) but dataSource has {len(sources)}; a CSV "
                f"dataSource must be positionally 1:1 with dataKey, and a mismatch invalidates the "
                f"whole widget"
            )

        return tuple(WidgetBinding(token, source) for token, source in zip(tokens, sources)), None


class PostProcessingConfig(_ConfigModel):
    """``post_processing_config.json`` — the only one of the three that reaches the engine.

    be-inference copies this object verbatim into ``nodeConfig`` under **both** ``use_case_config``
    and ``post_processing_config`` and it becomes the analytics job's parameters unchanged, so the
    platform imposes no schema beyond it being an object. Only ``usecase`` is load-bearing here: it
    is the join to ``app.yaml`` ``app.id``.
    """

    usecase: str | None = None
    category: str | None = None
    app_manifest: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)
