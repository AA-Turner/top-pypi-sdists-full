"""The 60-second aggregation window: what closes it, and what it publishes.

Normative sources: ``_contracts/07-tobe-canonical-contract.md`` §2 (surface **S1**),
``_contracts/09-tobe-engine-architecture.md`` §4 (the two clears) and
``clauding/STAGE_BC_PLAN.md`` §3 (C3), §6b (couplings 3 and 4).

Five decisions carry a defect each:

**``current_counts`` on S1 is an arrival delta, not a level (BE-16).**  ``raw_analytics`` is a
*delta plus level* schema -- ``count`` is "how many arrived since the previous reading",
``totalCount`` is "how many were there at the reading" -- and the five-minute rollup is
``argMin(totalCount, t) + sum(count) - argMin(count, t)``.  Publishing the frame level in
``count`` makes that formula add up occupancy readings instead of arrivals, which multiplies
the published footfall by roughly the number of windows in the bucket.  S3 is the opposite
case and keeps the level, because a frame has no interval to take a delta over and
be-analytics reads its ``current_counts`` as "how many objects right now".  Both surfaces are
built from the same four quantities by :class:`ZoneCounters`; see its docstring.

**The boundary is on the injectable clock, never ``time.time()`` (PY-13).**
``engine_session.py:595`` passes ``time.time()`` into a function designed for frame
timestamps, so a replayed or backfilled stream aggregates on wall-clock and produces windows
that never existed.  :class:`~matrice_analytics.engine.primitives.base.FrameClock` advances
only when a frame says so, and :meth:`AggregationWindow.is_due` reads exactly that.  This
module never imports :mod:`time`.

**``WindowOutput`` values are published as-is (§6b coupling 4).**  ``detect.window()``
already collapsed the window to its *peak* and ``unique_count.window()`` to a window *sum*.
Re-applying ``metrics[].agg_type`` on top would sum 1,500 per-frame peaks and publish 4,500
people -- that is **PY-1**, live in production today.  ``agg_type`` still travels on the wire,
because it is how the *backend* collapses this window into its five-minute rollup; it is not
a second instruction to this module.  The only place ``agg_type`` is applied here is a
``custom`` stage, which has no ``window()`` and therefore publishes per-frame samples.

**``end_window()`` is the boundary, ``clear()`` never is (09 §4 rule 2).**
:meth:`AggregationWindow.rollover` calls
:meth:`~matrice_analytics.engine.state.store.StateStore.end_window` on the session's root
scope, which drops every :attr:`~matrice_analytics.engine.state.store.Lifetime.WINDOW` key in
every primitive's subtree and leaves the ``PERSISTENT`` ones -- the tracker blobs, the
smoothing histories, the cumulative totals -- untouched.  Clearing a total here would make
the backend read every window boundary as a process restart (**FROZEN-4**).

**A ``derived[]`` metric obeys the same rule, from the same flag.**  A derived value whose
operands are all window outputs is computed *from already-aggregated numbers*, so it is
itself already aggregated and is published verbatim -- ``agg_type`` travels on the wire for
the backend's rollup and is not applied here.  One whose operands are per-frame samples is
evaluated per frame and *is* collapsed with ``agg_type``, exactly like a ``custom`` stage's
values.  The manifest decides which
(:func:`~matrice_analytics.engine.manifest.models.resolve_derived`); this module only obeys.
A zero denominator anywhere in the expression makes the reading **undefined**, which
contributes no sample and therefore publishes ``0.0`` -- never ``NaN``, which would cost the
whole window (finding **F1**).

**``emit_empty_windows`` defaults true and is honoured.**  With ``false``, an app that saw
nothing publishes nothing, which is today's behaviour
(``legacy_analytics_bridge.py:3007``) and the reason incident-only apps are absent from
every volume dashboard and generate a recurring "where is this app?" report.  The flag makes
that a choice rather than an accident.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final

from matrice_analytics.engine.contract.emit import build_aggregation
from matrice_analytics.engine.contract.schemas import (
    GLOBAL_ZONE,
    UNASSIGNED_ZONE,
    AggregationResult,
    AggType,
    MetricEntry,
    StreamInfo,
    TrackingCount,
    TrackingStats,
    parse_agg_type,
    to_rfc3339z,
)
from matrice_analytics.engine.manifest.expr import DerivedExpression, EvaluationError
from matrice_analytics.engine.manifest.models import (
    AppManifest,
    DerivedMetricSpec,
    DerivedScopeLiteral,
    MetricSpec,
    resolve_derived,
    resolve_source,
)
from matrice_analytics.engine.primitives.base import (
    Clock,
    PipelineDetection,
    PrimitiveOutput,
    Scalar,
    WindowOutput,
)
from matrice_analytics.engine.state import Lifetime, StateStore

__all__ = [
    "AggregationWindow",
    "DerivedOperand",
    "DerivedPlan",
    "MetricPlan",
    "ZoneCounters",
    "collapse",
    "derived_plan",
    "human_text_for",
    "metric_plan",
    "stage_key_map",
]

logger = logging.getLogger(__name__)

#: Retained per-frame outputs per (zone, stage) are capped at
#: ``window_seconds * fps * _RETENTION_SLACK`` frames.  ``dwell``, ``velocity_state``,
#: ``state_machine`` and ``incident_quantise`` all read ``frames`` in their ``window()``, so
#: the outputs have to be kept -- but a stream whose declared fps is wrong (or whose clock
#: stopped advancing) would otherwise grow the list without bound for the life of the process.
#: Four times the expected frame count is far outside normal jitter and inside a bounded heap.
_RETENTION_SLACK: Final[int] = 4

#: State keys.  ``carry`` and ``totals_at_start`` are PERSISTENT: they describe the *previous*
#: window and must survive the boundary that clears everything else (**PY-4**, **FROZEN-4**).
_CARRY_KEY: Final[str] = "window_carry_counts"
_TOTALS_AT_START_KEY: Final[str] = "window_start_totals"


# ---------------------------------------------------------------------------
# Per-zone count bookkeeping (the four count lists, FROZEN-5)
# ---------------------------------------------------------------------------


class ZoneCounters:
    """The four count lists for one zone, maintained frame by frame.

    All four are always emitted (**FROZEN-5**) even though ``current_new_counts`` and
    ``total_counts`` are ignored on the backend's main ingestion path: the instant-metric
    formula path and ``dataField`` resolution read them, and on the frame surface their
    absence is **PY-2** -- ``hasTrackingStats`` fails on all seven probe paths and every
    instant metric evaluates against zero.

    **The same four names mean different things on the two surfaces, because the two
    surfaces are read by different consumers (BE-16).**  There are therefore two builders:
    :meth:`window_count_lists` for S1 and :meth:`count_lists` for S3.  Both read the same
    four quantities; they differ only in which quantity ``current_counts`` carries.

    :meth:`window_count_lists` -- **S1**, ``results-agg``, once per window:

    ==========================  =======================================================
    List                        What this class puts in it
    ==========================  =======================================================
    ``current_counts``          per-entity uniques **first seen during this window** --
                                an arrival *delta*, because it lands in
                                ``raw_analytics.count`` and the backend's rollup sums it
    ``current_new_counts``      the same arrivals.  On a window surface "new in this
                                window" and "the window's arrival delta" are one number
    ``total_counts``            per-entity uniques since process start (FROZEN-4)
    ``total_current_counts``    previous window's last-frame count + this window's new
                                arrivals (**PY-4**: *not* a copy of ``current_counts``)
    ==========================  =======================================================

    :meth:`count_lists` -- **S3**, the per-frame return value:

    ==========================  =======================================================
    ``current_counts``          the **last observed frame's** per-entity count -- a level
    ``current_new_counts``      per-entity uniques first seen during this window
    ``total_counts``            per-entity uniques since process start (FROZEN-4)
    ``total_current_counts``    the same occupancy carry as S1
    ==========================  =======================================================

    **Why ``current_counts`` differs (BE-16).**  ``raw_analytics`` is a *delta plus level*
    schema: each row says how many arrived since the previous reading (``count``) and how
    many were there at the reading (``totalCount``), and the five-minute rollup is
    ``argMin(totalCount, t) + sum(count) - argMin(count, t)``
    (``10_aggregated_analytics_totals_schema.sql:7``).  Put a level in ``count`` and that
    sum adds up occupancy readings: on the six-window sequence in
    ``tests/unit/engine/test_runtime_window.py::TestTheBackendRollupFormula`` it publishes
    **28 people through a shop that ten walked through**.  The legacy engine already got
    this right on its default path -- ``legacy_analytics_bridge:2811`` sets
    ``current_counts = window_new_sum``.  S3 has no interval to take a delta over, and
    be-analytics' instant-metric extractor reads its ``current_counts`` as
    ``total_count``/``category_total_count``, i.e. "how many objects right now"
    (``tracker_clickhouse_service.go:1097-1120``) -- so there the level is correct and must
    stay.

    ``current_counts``, ``current_new_counts`` and ``total_counts`` all come from a
    ``unique_count`` stage's ``per_category.<entity>`` values -- the only stage that knows
    what "distinct" means.  An app without one publishes zero arrivals rather than guessing:
    a per-frame count summed over a window is not a unique count, and publishing it as one
    is the error this whole engine exists to stop.  :meth:`AggregationWindow.build` says so
    out loud, once, because on S1 that also means the app has no volume series.
    """

    __slots__ = (
        "_carry",
        "_current",
        "_entities",
        "_live_active",
        "_new",
        "_start_totals",
        "_totals",
        "_zone",
    )

    def __init__(self, zone: str, entities: Sequence[str]) -> None:
        self._zone = zone
        self._entities: tuple[str, ...] = tuple(entities)
        self._current: dict[str, int] = {}
        self._totals: dict[str, int] = {}
        self._new: dict[str, int] = {}
        self._carry: dict[str, int] = {}
        self._start_totals: dict[str, int] = {}
        self._live_active: bool = False

    # -- lifecycle ----------------------------------------------------------

    def load(self, state: StateStore) -> None:
        """Read the two cross-window values from the store."""
        self._carry = {str(k): int(v) for k, v in (state.get(_CARRY_KEY, {}) or {}).items()}
        self._start_totals = {str(k): int(v) for k, v in (state.get(_TOTALS_AT_START_KEY, {}) or {}).items()}

    def observe(
        self,
        detections: Sequence[PipelineDetection],
        outputs: Mapping[str, PrimitiveOutput],
    ) -> None:
        """Fold one frame in.

        Args:
            detections: This zone's detections for the frame, after entity remapping.
            outputs: This zone's stage outputs for the frame, keyed by stage name.  Scanned
                for ``per_category.<entity>`` values rather than for a stage literally named
                ``unique_count``, because a manifest may run it under its own ``name:``.
        """
        live: dict[str, int] = {}
        for output in outputs.values():
            for key, value in output.values.items():
                if not key.startswith("live_category."):
                    continue
                entity = key[len("live_category.") :]
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    live[entity] = int(value)

        self._live_active = bool(live)
        if live:
            # A stage published an explicit live snapshot (e.g. line_crossing's
            # `expose_corridor_state`, where "current" means "between the two lines right
            # now", a category no raw detection's entity ever carries) -- use it in place of
            # the default per-entity headcount, which cannot express that.
            self._current = live
        else:
            current: dict[str, int] = dict.fromkeys(self._entities, 0)
            for detection in detections:
                current[detection.entity] = current.get(detection.entity, 0) + 1
            self._current = current

        for output in outputs.values():
            for key, value in output.values.items():
                if not key.startswith("per_category."):
                    continue
                entity = key[len("per_category.") :]
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    self._totals[entity] = int(value)
        self._new = {
            entity: max(0, total - int(self._start_totals.get(entity, 0))) for entity, total in self._totals.items()
        }

    def rollover(self, state: StateStore) -> None:
        """Carry this window's tail into the next one (**PY-4**) and rebase ``new``.

        Both writes are :attr:`~matrice_analytics.engine.state.store.Lifetime.PERSISTENT`:
        they are facts about the window that just closed, and ``end_window()`` is about to
        delete everything that is a measurement *of* it.
        """
        state.set(_CARRY_KEY, dict(self._current), lifetime=Lifetime.PERSISTENT)
        state.set(_TOTALS_AT_START_KEY, dict(self._totals), lifetime=Lifetime.PERSISTENT)
        self._carry = dict(self._current)
        self._start_totals = dict(self._totals)
        self._new = {}

    # -- reads --------------------------------------------------------------

    @property
    def zone(self) -> str:
        return self._zone

    @property
    def current(self) -> Mapping[str, int]:
        """The last observed frame's per-entity counts."""
        return dict(self._current)

    @property
    def saw_anything(self) -> bool:
        """Whether any detection was counted in this window (drives ``emit_empty_windows``)."""
        return any(self._current.values()) or any(self._new.values())

    @property
    def new(self) -> Mapping[str, int]:
        """Per-entity uniques first seen during this window -- the arrival delta."""
        return dict(self._new)

    def _occupancy_carry(self) -> dict[str, int]:
        """``total_current_counts``: previous window's last-frame count + this window's new.

        **PY-4.**  Not a copy of anything: it is the reading the backend's rollup takes
        ``argMin(totalCount, t)`` of, and it has to include the first reading's arrivals
        because the formula subtracts them back out again
        (``10_aggregated_analytics_totals_schema.sql:146``).
        """
        return {
            entity: int(self._carry.get(entity, 0)) + int(self._new.get(entity, 0))
            for entity in set(self._carry) | set(self._new)
        }

    def count_lists(self) -> dict[str, list[TrackingCount]]:
        """The four count lists for the **frame** surface (S3), ready for
        :class:`~matrice_analytics.engine.contract.schemas.FrameTrackingStats`.

        ``current_counts`` is the frame's *level* here, deliberately: be-analytics'
        instant-metric ``dataField`` resolution reads it as ``total_count`` /
        ``category_total_count``, i.e. "how many objects right now"
        (``tracker_clickhouse_service.go:1097-1120``).  A frame is an instant, so there is
        no interval for an arrival delta to be a delta *over*.  The window surface is the
        one that needs the delta -- :meth:`window_count_lists`.

        ``total_current_counts`` is the occupancy-carry formula (``_occupancy_carry``) UNLESS
        a stage published an explicit live snapshot (``live_category.*``) this frame, in which
        case it is the same reading as ``current_counts``, verbatim. The carry formula answers
        "what should the backend's rollup treat as the running level", which presupposes
        ``current_counts`` means "arrivals" -- not true here, where it means "how many are in
        this live category right now" and there is nothing to carry across a window boundary.
        """
        total_current = self._current if self._live_active else self._occupancy_carry()
        return {
            "current_counts": _counts(self._current),
            "current_new_counts": _counts(self._new),
            "total_counts": _counts(self._totals),
            "total_current_counts": _counts(total_current),
        }

    def window_count_lists(self) -> dict[str, list[TrackingCount]]:
        """The four count lists for the **window** surface (S1), ready for
        :class:`~matrice_analytics.engine.contract.schemas.TrackingStats`.

        ``current_counts`` is this window's **arrival delta** (**BE-16**).  It lands in
        ``raw_analytics.count``, which the backend sums; a level there makes the
        five-minute rollup add up occupancy readings and publish several times the true
        footfall.  See the class docstring for the arithmetic.

        ``current_counts`` and ``total_current_counts`` are built over **one shared key
        set**, because the ingest mapper iterates ``current_counts`` and looks each
        category up in ``total_current_counts`` (``tracker_clickhouse_service.go:659-679``):
        a category missing from the first list drops its occupancy carry on the floor.  An
        entity that is zero in *both* is left out entirely -- there is nothing to say about
        it, and a twenty-class model would otherwise write twenty empty rows a minute.
        """
        arrivals = dict(self._new)
        carry = self._occupancy_carry()
        entities = sorted(
            entity for entity in set(arrivals) | set(carry) if int(arrivals.get(entity, 0)) or int(carry.get(entity, 0))
        )
        counts = [TrackingCount(category=entity, count=int(arrivals.get(entity, 0))) for entity in entities]
        return {
            "current_counts": counts,
            # On a window surface these are the same quantity under two names: "arrivals
            # during the reporting interval". Legacy only differed because it happened to
            # put a per-frame `latest_new` here (bridge:2812), which no consumer reads.
            "current_new_counts": list(counts),
            "total_counts": _counts(self._totals),
            "total_current_counts": [
                TrackingCount(category=entity, count=int(carry.get(entity, 0))) for entity in entities
            ],
        }


def _counts(values: Mapping[str, int]) -> list[TrackingCount]:
    """A count list, zero entries dropped, ordered by entity name for determinism."""
    return [TrackingCount(category=entity, count=int(count)) for entity, count in sorted(values.items()) if int(count)]


def human_text_for(counts: Mapping[str, int]) -> str:
    """A display string for a zone, e.g. ``"3 person, 1 vehicle"``.

    Display only: nothing parses this, and be-analytics reads the count lists rather than the
    text.  Deliberately not pluralised -- "3 persons" and "3 people" are both wrong for some
    entity name, and an entity name is whatever the app author mapped, so the count and the
    name are given unchanged.
    """
    parts = [f"{count} {entity}" for entity, count in sorted(counts.items()) if count]
    return ", ".join(parts) if parts else "no detections"


# ---------------------------------------------------------------------------
# Metric collapse
# ---------------------------------------------------------------------------


def collapse_zones(samples: Sequence[float], how: str) -> float:
    """Collapse one metric's per-zone readings into a single number, by ``across_zones``.

    Deliberately **not** :func:`collapse`, which collapses a metric over *time* and is selected
    by ``agg_type``. The two axes are independent and a manifest routinely wants different
    answers on each -- ``max_time_in_zone_seconds`` is ``agg_type: last`` (the window's own last
    reading, because ``dwell`` already aggregated it) and ``across_zones: max`` (the worst
    zone). Sharing one function would have forced them together.

    Lives here rather than in ``session.py`` because both surfaces now need it -- the flat
    per-frame ``result['metrics']`` map and ``zone: collapsed`` on ``results-agg`` -- and a key
    that meant one thing per frame and another per window would be worse than either.

    *samples* is never empty: the caller drops a metric no zone resolved rather than collapsing
    nothing into a ``0`` (``09`` §3).
    """
    if how == "max":
        return max(samples)
    if how == "mean":
        return sum(samples) / len(samples)
    return sum(samples)


def collapse(samples: Sequence[float], agg_type: AggType | str) -> float:
    """Collapse per-frame samples with ``agg_type``.

    Used for ``custom`` stages **only** -- see the module docstring.  A registered
    primitive's ``window()`` has already aggregated, and applying this on top of it is
    **PY-1**.

    Args:
        samples: The per-frame values, in frame order.
        agg_type: The metric's declared aggregation.  ``MetricSpec.agg_type`` is a *string*
            literal while ``MetricEntry.agg_type`` is the :class:`AggType` enum, so both are
            accepted and coerced through :func:`parse_agg_type` -- an ``is`` comparison against
            the enum silently matched nothing when handed the manifest's string, and the
            fall-through published a ``last`` for every metric.

    Returns:
        The collapsed value; ``0.0`` for no samples, which reads as "a quiet camera" rather
        than dropping the metric and leaving a gap in the series.

    Raises:
        ValueError: ``agg_type`` is not one of the five legal values.  Never a fallback: an
            ``agg_type`` that quietly degrades to ``sum`` is exactly **PY-1**.
    """
    if not samples:
        return 0.0
    resolved = parse_agg_type(agg_type)
    if resolved is AggType.sum:
        return float(sum(samples))
    if resolved is AggType.mean:
        return float(sum(samples)) / float(len(samples))
    if resolved is AggType.min:
        return float(min(samples))
    if resolved is AggType.max:
        return float(max(samples))
    return float(samples[-1])  # AggType.last


@dataclass(frozen=True, slots=True)
class MetricPlan:
    """One declared metric, joined to the stage and value name that produce it.

    Resolved once at setup rather than per window (or, in the session, per frame): the join is
    pure manifest arithmetic and doing it on the hot path is the kind of cost that only shows
    up at 25 fps across six buckets.
    """

    spec: MetricSpec
    stage: str
    """The **stage name** the value comes from -- see :func:`stage_key_map`."""
    value: str
    """The value key inside that stage's ``values``, e.g. ``"person.count"``."""


def metric_plan(manifest: AppManifest) -> tuple[MetricPlan, ...]:
    """Resolve every ``metrics[].source`` against the pipeline, once.

    Raises:
        ValueError: A source does not resolve.  It cannot happen for a manifest that came
            through the loader -- :meth:`AppManifest._check_metric_sources` already ran -- but
            a manifest built in Python can skip that, and an unresolvable source must be an
            error rather than a metric that reads zero forever (``09`` §3).
    """
    keys = stage_key_map(manifest)
    plan: list[MetricPlan] = []
    for metric in manifest.metrics:
        resolved = resolve_source(manifest, metric.source, where=f"metrics ({metric.key})")
        plan.append(
            MetricPlan(
                spec=metric,
                stage=keys.get(resolved.stage, resolved.stage),
                value=resolved.value,
            )
        )
    return tuple(plan)


@dataclass(frozen=True, slots=True)
class DerivedOperand:
    """One ``<stage>.<value>`` operand of a derived expression, joined to the pipeline."""

    source: str
    """The name as written in ``expr`` -- the key :meth:`DerivedExpression.evaluate` looks up."""
    stage: str
    """The real **stage name** the value comes from -- see :func:`stage_key_map`."""
    value: str
    """The value key inside that stage's ``values``."""
    from_global: bool = False
    """Read this operand from the ``global`` bucket, not from the zone being evaluated.

    Set by a ``global.``-prefixed operand.  It is what lets one expression divide a zone's
    reading by a **frame-wide** one; without it every operand resolves in the same bucket, so
    a zone's share of itself is 100% and no per-zone metric can express a share of the frame.
    """


@dataclass(frozen=True, slots=True)
class DerivedPlan:
    """One ``derived[]`` entry, parsed and joined to the pipeline, ready to evaluate.

    Built once at session setup: the parse and the stage join are pure manifest arithmetic,
    and a 25fps stream across six buckets is the wrong place to be re-parsing a string.
    """

    spec: DerivedMetricSpec
    expression: DerivedExpression
    scope: DerivedScopeLiteral
    """``"window"`` -- evaluate once at the boundary, publish verbatim; ``"frame"`` -- evaluate
    per retained frame and collapse the samples with ``agg_type``.  Decided by the manifest
    (:func:`~matrice_analytics.engine.manifest.models.resolve_derived`), never here."""
    operands: tuple[DerivedOperand, ...]

    @property
    def window_aggregated(self) -> bool:
        """``True`` when this value must be published **as-is** (**PY-1**, §6b coupling 4)."""
        return self.scope == "window"


def derived_plan(manifest: AppManifest) -> tuple[DerivedPlan, ...]:
    """Resolve every ``derived[].expr`` against the pipeline, once.

    Uses the loader's own function
    (:func:`~matrice_analytics.engine.manifest.models.resolve_derived`), so the scope the
    runtime evaluates in is by construction the scope the manifest validated -- and an operand
    that does not resolve raises here exactly as it would at load, rather than becoming a
    metric that reads zero forever (``09`` §3).

    Raises:
        ValueError: An operand does not resolve, or the declared scope is impossible.  It
            cannot happen for a manifest that came through the loader
            (:meth:`AppManifest._check_derived` already ran) but a manifest built in Python
            can skip that.
    """
    keys = stage_key_map(manifest)
    plan: list[DerivedPlan] = []
    for spec in manifest.derived:
        resolved = resolve_derived(manifest, spec, where=f"derived ({spec.key})")
        plan.append(
            DerivedPlan(
                spec=spec,
                expression=resolved.expression,
                scope=resolved.scope,
                operands=tuple(
                    DerivedOperand(
                        source=operand.source,
                        stage=keys.get(operand.stage, operand.stage),
                        value=operand.value,
                        from_global=operand.from_global,
                    )
                    for operand in resolved.operands
                ),
            )
        )
    return tuple(plan)


def stage_key_map(manifest: AppManifest) -> dict[str, str]:
    """Map every name a ``metrics[].source`` may use onto the real stage name.

    ``resolve_source`` accepts a stage's ``name:`` *or* its primitive name while that is
    unambiguous, so ``source: custom.served`` resolves against a stage named ``queue``.  The
    pipeline outputs are keyed by stage name only, so the two have to be joined here -- with
    the same rule ``manifest.resolve_source`` uses, or a metric would validate at load and
    fail to resolve at runtime.
    """
    mapping = {stage.stage_name: stage.stage_name for stage in manifest.pipeline}
    by_primitive: dict[str, list[str]] = {}
    for stage in manifest.pipeline:
        by_primitive.setdefault(stage.PRIMITIVE, []).append(stage.stage_name)
    for primitive, names in by_primitive.items():
        if len(names) == 1:
            mapping.setdefault(primitive, names[0])
    return mapping


def _number(value: Scalar | None) -> float | None:
    """A ``values`` entry as a float, or ``None`` when it is not a number.

    ``values`` admits ``str`` (``velocity_state`` publishes a state *label*), and a metric
    pointed at one is a manifest error the loader cannot catch -- the type is only known at
    runtime.  Returning ``None`` lets the caller say which metric and which source.
    """
    if isinstance(value, bool):
        return float(int(value))
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _is_deliberately_silent(window_output: WindowOutput | None) -> bool:
    """Whether a stage ran in this bucket and chose to publish **nothing**.

    The three states a caller has to tell apart, and only the middle one is a problem:

    * ``None`` -- the stage did not run in this bucket at all.  Either the manifest and the
      runtime disagree, or a ``zones: all_in_one`` stage exists only in ``global``.
    * a :class:`WindowOutput` **with** values, none of them the one asked for -- the stage's
      output names have drifted from its config model.  This is drift, and it is silent data
      loss, so it warrants the warning.
    * a :class:`WindowOutput` with **no** values -- the stage ran and has nothing to say here.
      ``dwell`` with ``state: in_zone`` does exactly this in the ``unassigned`` bucket, where
      a session can never open, rather than publishing a resolved ``0`` that would reach the
      wire as a permanent zero series next to the real per-zone row.

    A ``custom`` stage also returns an empty :class:`WindowOutput`, but it does so to route
    itself down the ``agg_type``-over-frames path -- so its callers find per-frame samples and
    never reach this check.  Only a stage with neither a window value nor a frame sample does.
    """
    return window_output is not None and not window_output.values


# ---------------------------------------------------------------------------
# The window
# ---------------------------------------------------------------------------


class AggregationWindow:
    """One camera's open aggregation window.

    Owned by :class:`~matrice_analytics.engine.runtime.session.Session`, which feeds it every
    frame and asks it, on the frame clock, whether the window is due.  The window does not
    call the primitives -- the session owns those -- so :meth:`build` is handed the
    :class:`WindowOutput` map it needs.  That split keeps this class testable with plain
    dicts and keeps "who owns the primitives" answered once.

    Example:
        >>> window = AggregationWindow(manifest, stream, clock, state,      # doctest: +SKIP
        ...                            emission_zones=("global",))
        >>> window.observe(1_700_000_000.0, {"global": outputs}, {"global": detections})
        >>> window.is_due()
        False
    """

    __slots__ = (
        "_arrivals_measurable",
        "_clock",
        "_counter_root",
        "_counters",
        "_derived_plan",
        "_emission_zones",
        "_entities",
        "_frames",
        "_last_ts",
        "_manifest",
        "_max_frames",
        "_metric_plan",
        "_no_arrivals_warned",
        "_retention_warned",
        "_start_ts",
        "_state",
        "_stream",
        "_window_seconds",
        "reset_timestamp",
    )

    def __init__(
        self,
        manifest: AppManifest,
        stream: StreamInfo,
        clock: Clock,
        state: StateStore,
        *,
        emission_zones: Sequence[str],
        reset_timestamp: str = "",
    ) -> None:
        """Open a window for one camera.

        Args:
            manifest: The validated app manifest.  ``emission.window_seconds`` sets the
                cadence and ``emission.emit_empty_windows`` decides whether a silent window
                publishes.
            stream: The typed :class:`~matrice_analytics.engine.contract.schemas.StreamInfo`;
                supplies every S1 envelope identity field and ``original_fps``.
            clock: The session's clock.  A
                :class:`~matrice_analytics.engine.primitives.base.FrameClock` in production
                and in replay (**PY-13**); ``WallClock`` only where wall-clock is genuinely
                meant.
            state: The session's **root** scope.  ``end_window()`` is called on it, so it
                must be the scope that contains every primitive's subtree.
            emission_zones: The zones that appear in ``tracking_stats`` -- the drawn zones
                for a zoned app, else ``("global",)``.  Never both: a payload carrying zone
                series *and* a ``global`` series double-counts in any dashboard that sums
                zones.
            reset_timestamp: RFC3339 instant at which this camera's cumulative counters last
                reset, i.e. process start (**FROZEN-4**).  Writable afterwards: the session
                anchors it to the *first frame* rather than to its own construction, because a
                session built minutes before the stream starts would otherwise claim a reset
                that no counter was affected by.
        """
        self._manifest = manifest
        self._stream = stream
        self._clock = clock
        self._state = state
        self._emission_zones: tuple[str, ...] = tuple(emission_zones)
        self.reset_timestamp = reset_timestamp
        self._window_seconds = float(manifest.emission.window_seconds)
        self._entities: tuple[str, ...] = tuple(sorted(manifest.model.entities))
        self._metric_plan = metric_plan(manifest)
        self._derived_plan = derived_plan(manifest)
        # Counters live beside the primitives but under a scope no stage can occupy:
        # <camera>/<app>/_counters/<zone>, where a stage scope is <camera>/<app>/<zone>/<stage>.
        self._counter_root = state.scoped(stream.camera_id).scoped(manifest.app.id).scoped("_counters")

        self._start_ts: float | None = None
        self._last_ts: float = 0.0
        self._frames: dict[str, dict[str, list[PrimitiveOutput]]] = {}
        self._counters: dict[str, ZoneCounters] = {}
        self._retention_warned = False
        # S1's `current_counts` is an arrival delta (BE-16), and only `unique_count` can
        # decide what an arrival is. Resolved once here rather than probed per window.
        self._arrivals_measurable = any(stage.PRIMITIVE == "unique_count" for stage in manifest.pipeline)
        self._no_arrivals_warned = False

        # 0.0 is a normal value, not a defaulting bug: the producer may not know the rate
        # (INF-2606), and nothing here needs the true one -- this only sizes a safety cap on
        # retained per-frame outputs, so an assumed 30 that is 3x off still leaves a cap 3x
        # the real frame count, which is what `_RETENTION_SLACK` is already for.
        fps = float(stream.original_fps or 0.0)
        expected = self._window_seconds * (fps if fps > 0 else 30.0)
        self._max_frames = max(64, int(expected) * _RETENTION_SLACK)

    # -- observation --------------------------------------------------------

    def observe(
        self,
        frame_ts: float,
        zone_outputs: Mapping[str, Mapping[str, PrimitiveOutput]],
        zone_detections: Mapping[str, Sequence[PipelineDetection]],
        *,
        stream: StreamInfo | None = None,
    ) -> None:
        """Fold one frame's per-zone results into the open window.

        The first frame **opens** the window, and its timestamp -- not the process start --
        is the window's origin.  A camera that starts publishing at 00:00:37 gets its first
        boundary at 00:01:37, not a 23-second stub, and a replay of the same footage gets the
        same boundaries (**PY-13**).

        Args:
            frame_ts: This frame's time, epoch seconds.
            zone_outputs: Each bucket's per-stage output for this frame.
            zone_detections: Each bucket's detections for this frame.
            stream: This frame's stream context.  When given, the window **re-anchors** its
                S1 envelope to it, so the published ``rtp_number`` names a frame this window
                actually contains rather than the one the session was constructed from.  The
                identity fields are the same object either way -- only the media anchors move
                -- and :meth:`build` already publishes ``input_timestamp`` from the last
                observed frame, so this makes the two agree.  ``None`` leaves the anchor
                alone, which is what a caller that has no per-frame stream wants.
        """
        if stream is not None:
            self._stream = stream
        if self._start_ts is None:
            self._start_ts = frame_ts
            logger.debug(
                "aggregation window opened at frame_ts=%s (%.0fs cadence)",
                frame_ts,
                self._window_seconds,
            )
        self._last_ts = frame_ts

        for zone, outputs in zone_outputs.items():
            retained = self._frames.setdefault(zone, {})
            for stage, output in outputs.items():
                samples = retained.setdefault(stage, [])
                if len(samples) < self._max_frames:
                    samples.append(output)
                elif not self._retention_warned:
                    self._retention_warned = True
                    logger.warning(
                        "aggregation window retained %d frames for %s/%s, which is %dx the "
                        "expected count for a %.0fs window at %s fps (0 = rate unknown, cap "
                        "sized at an assumed 30) -- no further frames "
                        "will be retained. Window values sourced from the state store stay "
                        "correct; values a primitive derives from its per-frame outputs "
                        "(dwell, velocity_state, state_machine) will under-report. The usual "
                        "cause is a frame clock that is not advancing.",
                        len(samples),
                        zone,
                        stage,
                        _RETENTION_SLACK,
                        self._window_seconds,
                        self._stream.original_fps,
                    )
            self.counters_for(zone).observe(zone_detections.get(zone, ()), outputs)

    def counters_for(self, zone: str) -> ZoneCounters:
        """This zone's :class:`ZoneCounters`, created and loaded on first use.

        Public because the **frame** surface needs the same four count lists as the window
        surface (**PY-2**), from the same numbers.  The session reads them from here rather
        than maintaining a second set, which is how the frame path and the window path came to
        disagree in the first place.
        """
        counters = self._counters.get(zone)
        if counters is None:
            counters = ZoneCounters(zone, self._entities)
            counters.load(self._counter_root.scoped(zone))
            self._counters[zone] = counters
        return counters

    # -- boundary -----------------------------------------------------------

    @property
    def is_open(self) -> bool:
        """Whether at least one frame has been observed since the last boundary."""
        return self._start_ts is not None

    @property
    def start_ts(self) -> float | None:
        """Frame timestamp of the first frame in this window, or ``None``."""
        return self._start_ts

    @property
    def last_ts(self) -> float:
        """Frame timestamp of the most recent frame."""
        return self._last_ts

    def is_due(self, now: float | None = None) -> bool:
        """Whether ``window_seconds`` have elapsed **on the frame clock** (**PY-13**).

        Args:
            now: Override the clock, for tests.  Production passes nothing: the session
                advances the :class:`FrameClock` from ``frame_ts`` and this reads it, which
                is what makes a replayed hour produce the live run's windows.
        """
        if self._start_ts is None:
            return False
        current = self._clock.now() if now is None else now
        return (current - self._start_ts) >= self._window_seconds

    def frames_for(self, zone: str, stage: str) -> tuple[PrimitiveOutput, ...]:
        """The per-frame outputs retained for one stage in one zone, in frame order.

        This is what the session passes to ``primitive.window(frames)``.
        """
        return tuple(self._frames.get(zone, {}).get(stage, ()))

    # -- publication --------------------------------------------------------

    def build(self, zone_window_outputs: Mapping[str, Mapping[str, WindowOutput]]) -> AggregationResult | None:
        """Build the ``results-agg`` message for the closing window.

        Args:
            zone_window_outputs: ``zone -> stage -> WindowOutput``, from the session calling
                each primitive's ``window()``.  Values are used **as-is** (§6b coupling 4).

        Returns:
            The validated :class:`AggregationResult`, or ``None`` when the window is empty
            and ``emission.emit_empty_windows`` is false.

        Raises:
            ValueError: The window is not open -- there is nothing to publish, and silently
                returning ``None`` would hide a caller bug behind the same value that means
                "deliberately empty".
            ConformanceViolation: The assembled payload fails one of the six checks.
        """
        if self._start_ts is None:
            raise ValueError(
                "AggregationWindow.build() called with no frames observed. Check is_due() "
                "(or is_open) first: 'no window' and 'an empty window' are different states, "
                "and only the second one is a publishing decision."
            )

        saw_anything = any(counters.saw_anything for counters in self._counters.values())
        if not saw_anything and not self._manifest.emission.emit_empty_windows:
            logger.info(
                "window %s..%s saw no tracking and emission.emit_empty_windows is false -- "
                "publishing nothing. The app is invisible on volume dashboards for this "
                "window; that is the declared choice, not a fault.",
                self._start_ts,
                self._last_ts,
            )
            return None

        self._warn_if_no_arrivals_are_measurable()
        tracking_stats = {
            zone: TrackingStats(
                input_timestamp=to_rfc3339z(self._last_ts),
                reset_timestamp=self.reset_timestamp,
                # The WINDOW builder, not the frame one: `current_counts` on S1 is the
                # window's arrival delta (BE-16). See ZoneCounters.
                **self.counters_for(zone).window_count_lists(),
            )
            for zone in self._emission_zones
        }
        metrics = self._build_metrics(zone_window_outputs)

        return build_aggregation(
            self._stream,
            input_timestamp=self._last_ts,
            tracking_stats=tracking_stats,
            metrics=metrics,
        )

    def _warn_if_no_arrivals_are_measurable(self) -> None:
        """Say, once, that this app cannot produce a volume series (**BE-16**).

        S1's ``current_counts`` is an arrival delta, and an arrival is a *first sighting of
        a distinct object* -- which only a ``unique_count`` stage can decide.  An app
        without one publishes zeros there, so ``raw_analytics.count`` is zero, so the app is
        flat on every volume dashboard.  That is the honest answer: the alternative is to
        put the per-frame level in ``count``, which is the defect this method exists to
        announce rather than repeat.  The occupancy carry still travels in
        ``total_current_counts`` (one window stale, since it is the previous window's
        last-frame level plus zero arrivals), and an app that wants a live count should
        publish it as a ``metrics[]`` entry -- ``current_occupancy`` with
        ``agg_type: last``, exactly as contract §2.4 shows.
        """
        if self._arrivals_measurable or self._no_arrivals_warned:
            return
        if not any(counters.saw_anything for counters in self._counters.values()):
            return
        self._no_arrivals_warned = True
        logger.warning(
            "app %r saw detections but declares no 'unique_count' stage, so it cannot "
            "measure arrivals: results-agg current_counts -- and therefore "
            "raw_analytics.count, the series behind every volume dashboard -- will publish "
            "0 for every window. Add a 'track' + 'unique_count' pair to the pipeline, or "
            "accept that this app is deliberately not a counting app and read its "
            "occupancy from metrics[] instead (BE-16).",
            self._manifest.app.id,
        )

    def _build_metrics(self, zone_window_outputs: Mapping[str, Mapping[str, WindowOutput]]) -> list[MetricEntry]:
        """One :class:`MetricEntry` per declared metric per zone it applies to.

        ``metrics[]`` first, then ``derived[]``.  The two are indistinguishable on the wire --
        both are ``results-agg.metrics[]`` rows -- and the order is only so a payload reads the
        way the manifest does.
        """
        entries: list[MetricEntry] = []
        for planned in self._metric_plan:
            metric = planned.spec
            if metric.zone == "collapsed":
                value = self._collapsed_value(
                    metric,
                    # `planned` bound as a default: the lambda is called synchronously
                    # inside `_collapsed_value` and never stored, so the late binding B023
                    # warns about cannot bite today -- pinning it says so out loud and
                    # survives someone making that call lazy.
                    lambda zone, planned=planned: self._metric_value(planned, zone, zone_window_outputs),
                )
                if value is not None:
                    entries.append(
                        MetricEntry(
                            key=metric.key,
                            data=value,
                            agg_type=metric.agg_type,
                            category=metric.category,
                            zone=GLOBAL_ZONE,
                        )
                    )
                continue
            zones = self._emission_zones if metric.zone == "per_zone" else (GLOBAL_ZONE,)
            for zone in zones:
                value = self._metric_value(planned, zone, zone_window_outputs)
                if value is None:
                    continue
                entries.append(
                    MetricEntry(
                        key=metric.key,
                        data=value,
                        agg_type=metric.agg_type,
                        category=metric.category,
                        zone=zone,
                    )
                )
        for derived in self._derived_plan:
            spec = derived.spec
            if spec.zone == "collapsed":
                value = self._collapsed_value(
                    spec,
                    lambda zone, derived=derived: self._derived_value(derived, zone, zone_window_outputs),
                )
                if value is not None:
                    entries.append(
                        MetricEntry(
                            key=spec.key,
                            data=value,
                            agg_type=spec.agg_type,
                            category=spec.category,
                            zone=GLOBAL_ZONE,
                        )
                    )
                continue
            zones = self._emission_zones if spec.zone == "per_zone" else (GLOBAL_ZONE,)
            for zone in zones:
                value = self._derived_value(derived, zone, zone_window_outputs)
                if value is None:
                    continue
                entries.append(
                    MetricEntry(
                        key=spec.key,
                        data=value,
                        # Verbatim from the manifest, whatever the scope: at window scope this is
                        # the backend's rollup instruction and nothing here applied it; at frame
                        # scope it is also what collapsed the samples below. Either way the wire
                        # says how the *next* layer should collapse these readings.
                        agg_type=spec.agg_type,
                        category=spec.category,
                        zone=zone,
                    )
                )
        return entries

    def _collapsed_value(self, spec: Any, read: Any) -> float | None:
        """One number for a ``zone: collapsed`` metric: its zones, reduced by ``across_zones``.

        The same reduction ``Session._frame_metric_values`` already applies to the flat
        per-frame map, applied here so ``results-agg`` can carry it too. That symmetry is the
        point: a key declared ``collapsed`` means the same quantity on both surfaces, where a
        ``per_zone`` key means one number per frame and N rows per window.

        ``unassigned`` is excluded, exactly as it is per frame. It is a real diagnostic series
        in its own right -- a suddenly non-zero ``unassigned`` is how an operator finds out a
        polygon is drawn wrong -- but folding it into "the value for this camera" would mix a
        measurement with its own error term. It still ships as its own labelled row for any
        metric declared ``per_zone``.

        ``None`` when no zone had a reading, so the row is omitted rather than published as a
        zero nobody can account for.
        """
        samples = []
        for zone in self._emission_zones:
            if zone == UNASSIGNED_ZONE:
                continue
            value = read(zone)
            if value is not None:
                samples.append(value)
        if not samples:
            return None
        return collapse_zones(samples, spec.across_zones)

    def _metric_value(
        self,
        planned: MetricPlan,
        zone: str,
        zone_window_outputs: Mapping[str, Mapping[str, WindowOutput]],
    ) -> float | None:
        """Resolve one metric for one zone, or ``None`` to skip it with a warning.

        Resolution order, and why:

        1. the stage's :class:`WindowOutput` -- **already aggregated**, published verbatim
           (§6b coupling 4);
        2. the retained per-frame samples collapsed with ``agg_type`` -- the ``custom`` case,
           which has no ``window()``;
        3. skip, loudly.  A gap in the series is visible; a fabricated ``0.0`` is not, and it
           is indistinguishable from a genuinely quiet camera (``09`` §3).
        """
        metric = planned.spec
        stage = planned.stage
        name = planned.value

        window_output = zone_window_outputs.get(zone, {}).get(stage)
        if window_output is not None and name in window_output.values:
            value = _number(window_output.values[name])
            if value is not None:
                return value
            logger.warning(
                "metric %r points at %s, which published the non-numeric value %r; "
                "metrics[].data is a float (contract §1 rule 6). Skipping.",
                metric.key,
                metric.source,
                window_output.values[name],
            )
            return None

        samples: list[float] = []
        for frame in self.frames_for(zone, stage):
            number = _number(frame.values.get(name))
            if number is not None:
                samples.append(number)
        if samples:
            return collapse(samples, metric.agg_type)

        if _is_deliberately_silent(window_output):
            # The stage RAN here and published nothing at all -- not "this one name is
            # missing", which is drift, but "I have no readings in this bucket". `dwell` with
            # `state: in_zone` does this in the `unassigned` bucket, where no session can ever
            # open. Skipping is the same outcome as below; the difference is that this is
            # expected every window for the life of the process, so warning about it would be
            # a per-window, per-camera, per-metric line saying only that the engine is working.
            logger.debug(
                "metric %r (source %r) has no reading in zone %r: stage %r publishes nothing "
                "there by design. No row is emitted for this zone.",
                metric.key,
                metric.source,
                zone,
                stage,
            )
            return None

        logger.warning(
            "metric %r (source %r) resolved to nothing in zone %r: stage %r published "
            "neither a window value nor a per-frame value named %r. The manifest validated "
            "this source, so either the stage did not run in this zone or its output names "
            "have drifted from its config model.",
            metric.key,
            metric.source,
            zone,
            stage,
            name,
        )
        return None

    # -- derived metrics ----------------------------------------------------

    def _derived_value(
        self,
        planned: DerivedPlan,
        zone: str,
        zone_window_outputs: Mapping[str, Mapping[str, WindowOutput]],
    ) -> float | None:
        """Evaluate one ``derived[]`` expression for one zone, or ``None`` to skip it.

        Three outcomes, and the difference between the second and the third is the whole point:

        * a **number** -- the expression evaluated;
        * ``0.0`` -- the expression is *undefined* (a zero denominator).  "No denominator"
          means "no reading", and 0.0 is what every legacy producer of a rate publishes for it
          (``legacy_analytics_bridge.py``:2444, :2461, :2562, :2618).  It is also the only
          answer that cannot reach the wire as ``NaN`` and cost the whole window (**F1**);
        * ``None`` -- something is **wrong**: an operand the manifest resolved is missing at
          runtime, or the arithmetic overflowed.  The metric is skipped and logged, because a
          gap in a series is diagnosable and a fabricated number is not (``09`` §3).
        """
        if planned.scope == "window":
            values = self._window_operand_values(planned, zone, zone_window_outputs)
            if values is None:
                return None
            try:
                result = planned.expression.evaluate(values)
            except EvaluationError as error:
                logger.warning(
                    "derived metric %r (%s) could not be evaluated in zone %r: %s Skipping.",
                    planned.spec.key,
                    planned.expression.text,
                    zone,
                    error,
                )
                return None
            # Undefined over the whole window is a quiet camera, not a fault.
            return 0.0 if result is None else result

        samples: list[float] = []
        for frame_values in self._frame_operand_values(planned, zone):
            try:
                result = planned.expression.evaluate(frame_values)
            except EvaluationError as error:
                logger.warning(
                    "derived metric %r (%s) could not be evaluated on a frame in zone %r: %s "
                    "Dropping that frame's sample.",
                    planned.spec.key,
                    planned.expression.text,
                    zone,
                    error,
                )
                continue
            if result is not None:
                # An undefined frame contributes no sample -- so `mean` is the mean over the
                # frames that HAD a denominator, which is exactly what legacy
                # loitering_percentage published (bridge:1680-1686).
                samples.append(result)
        return collapse(samples, planned.spec.agg_type)

    def _window_operand_values(
        self,
        planned: DerivedPlan,
        zone: str,
        zone_window_outputs: Mapping[str, Mapping[str, WindowOutput]],
    ) -> dict[str, float] | None:
        """Every operand's window value, or ``None`` when one is missing or non-numeric.

        The bucket is chosen **per operand**, not per metric: a ``global.``-prefixed operand
        reads the whole-frame bucket while its neighbours read *zone*, which is what lets one
        expression state "this zone's share of the frame".
        """
        values: dict[str, float] = {}
        for operand in planned.operands:
            source_zone = GLOBAL_ZONE if operand.from_global else zone
            output = zone_window_outputs.get(source_zone, {}).get(operand.stage)
            raw = output.values.get(operand.value) if output is not None else None
            number = _number(raw)
            if number is None:
                if _is_deliberately_silent(output):
                    # The operand's stage publishes nothing in this bucket by design, so the
                    # whole derived metric has no reading here. Same skip, without the warning
                    # -- see _is_deliberately_silent.
                    logger.debug(
                        "derived metric %r has no reading in zone %r: operand %r comes from "
                        "stage %r in bucket %r, which publishes nothing there by design.",
                        planned.spec.key,
                        zone,
                        operand.source,
                        operand.stage,
                        source_zone,
                    )
                    return None
                logger.warning(
                    "derived metric %r reads operand %r, and stage %r published %r for it at "
                    "window scope in zone %r. The manifest resolved this operand, so either the "
                    "stage did not run in this zone or its output names have drifted from its "
                    "config model. Skipping the metric.",
                    planned.spec.key,
                    operand.source,
                    operand.stage,
                    raw,
                    zone,
                )
                return None
            values[operand.source] = number
        return values

    def _frame_operand_values(self, planned: DerivedPlan, zone: str) -> list[dict[str, float]]:
        """One operand map per retained frame, skipping frames that are missing a value.

        The retained lists are **index-aligned**: :meth:`observe` appends one
        :class:`PrimitiveOutput` per stage per frame, so index *i* is frame *i* for every
        stage.  If they are *not* the same length -- a stage that did not run on some frames --
        the shortest wins and the mismatch is logged, because silently zipping frame 10 of one
        stage against frame 7 of another produces a plausible number from two different
        moments.

        Retention is keyed by ``(bucket, stage)`` rather than by stage alone, because a
        ``global.``-prefixed operand can name the **same stage** as an unprefixed one -- as
        ``detect.person.count / global.detect.person.count`` does -- and those are two
        different series. Keying by stage would have made the second silently overwrite the
        first, so the expression would have divided a number by itself and published 100%.
        Both buckets are observed on the same frames, so the index alignment above still
        holds across them.
        """
        retained = {
            (GLOBAL_ZONE if operand.from_global else zone, operand.stage): self.frames_for(
                GLOBAL_ZONE if operand.from_global else zone, operand.stage
            )
            for operand in planned.operands
        }
        lengths = {key: len(frames) for key, frames in retained.items()}
        usable = min(lengths.values(), default=0)
        if usable and len(set(lengths.values())) > 1:
            logger.warning(
                "derived metric %r evaluates per frame in zone %r, but its stages retained "
                "different frame counts (%s). Using the first %d frame(s) of each: pairing "
                "different frames' values would publish a plausible number from two moments.",
                planned.spec.key,
                zone,
                lengths,
                usable,
            )

        frames: list[dict[str, float]] = []
        for index in range(usable):
            values: dict[str, float] = {}
            for operand in planned.operands:
                bucket = GLOBAL_ZONE if operand.from_global else zone
                number = _number(retained[(bucket, operand.stage)][index].values.get(operand.value))
                if number is None:
                    values = {}
                    break
                values[operand.source] = number
            if values:
                frames.append(values)
        return frames

    # -- rollover -----------------------------------------------------------

    def rollover(self) -> None:
        """Close the window: carry the tail forward, then clear WINDOW state.

        Order matters.  :meth:`ZoneCounters.rollover` writes the carry values the next
        window's ``total_current_counts`` needs (**PY-4**) *before*
        :meth:`~matrice_analytics.engine.state.store.StateStore.end_window` runs, and it
        writes them ``PERSISTENT`` so the clear cannot take them with it.

        ``end_window()`` on the session's root scope is the one call that clears every
        primitive's window-scoped keys -- peaks, per-window sums, "new this window" -- and
        cannot touch a cumulative total, because the lifetime was declared at write time
        (``09`` §4 rule 2).  ``clear()`` here would be the bug that whole design prevents.
        """
        for zone, counters in self._counters.items():
            counters.rollover(self._counter_root.scoped(zone))
        self._state.end_window()
        self._frames = {}
        self._start_ts = None
        self._retention_warned = False

    def __repr__(self) -> str:
        return (
            f"AggregationWindow(open={self.is_open}, start_ts={self._start_ts}, "
            f"last_ts={self._last_ts}, zones={list(self._emission_zones)!r}, "
            f"window_seconds={self._window_seconds})"
        )
