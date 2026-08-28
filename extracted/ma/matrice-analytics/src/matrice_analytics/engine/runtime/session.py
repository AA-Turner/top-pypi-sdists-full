"""Per-camera execution: one manifest, one stream, one pipeline per zone.

Normative sources: ``_contracts/09-tobe-engine-architecture.md`` §§1-4,
``clauding/STAGE_BC_PLAN.md`` §3 (C2), §4 (loader integration) and §6b (the five couplings).

The structural change from the old engine, in one line::

    detections -> entity remap -> ZONE PARTITION (once) -> pipeline per zone

``analytics/engine.py:362-381`` instantiates **zones x categories** processor objects and
each of them re-derives zone membership from the raw detections.  Here membership is decided
**once per frame**, by :func:`~matrice_analytics.engine.primitives.geometry.assign_detections_to_zones`,
and each pipeline is handed a detection set that is already its own.  Same numbers, one
partition, and the partition's *losses* are counted rather than dropped (**PY-10**).

What runs, per frame:

======  ==========================================================================
Bucket  Contents
======  ==========================================================================
        ``global``: every mapped detection.  Always present.  Metrics declared
        ``zone: global`` read it, incidents are evaluated against it, and it is the
        only bucket for an app with no ``zones:`` block.
        one per drawn zone, when the manifest opts into zones.  Metrics declared
        ``zone: per_zone`` read these.
        ``unassigned``: detections inside no drawn zone, when
        ``zones.on_no_match: unassigned`` (**PY-10** -- *count what lands there*).
======  ==========================================================================

The per-zone buckets are the ones that reach the wire (``tracking_stats`` and
``agg_summary`` are keyed by them, **FROZEN-2**/**PY-5**).  ``global`` is deliberately *not*
emitted alongside them: a payload carrying both a per-zone series and a whole-frame series
double-counts in any dashboard that sums zones.

**The one opt-out, and what it is for.**  Partitioning first is right for every registered
primitive and wrong for exactly one thing: a custom stage cannot observe a *transition*
between zones -- queue→counter, entry→exit, owner-leaves-object -- because the ``Queue``
bucket's detections all read ``Queue``, the ``Counter`` bucket has its own isolated state
scope, and the ``global`` bucket sees the whole frame with no zone on anything.  A ``custom``
stage may therefore declare ``zones: all_in_one``, and it is then built **only in the
``global`` bucket** (one instance, one state scope) and handed every detection the partition
kept with ``det.zone`` still carrying the zone *this module's own partition* assigned -- so
the app reads the transition off the detections instead of redoing point-in-polygon by hand.
No second geometry pass: the alignment comes out of the same partition
(:meth:`Session._partition`, :meth:`Session._all_zones_view`).  Registered primitives cannot
opt in, and the schema will not let them try -- see ``CustomConfig.all_in_one``.

The five §6b couplings, and where each is honoured:

1. **Resolution.**  Every :class:`FrameContext` is built with ``stream=<StreamInfo>``, so
   ``ctx.resolution`` / ``ctx.require_resolution(...)`` work everywhere.  One channel; the
   private ones are gone.  :meth:`Session.process_frame` is the only place a context is
   constructed, which is what keeps it one channel.
2. **``on_overlap`` is on ``ZonesSpec``**, not on ``ZoneOccupancyConfig`` -- so
   ``manifest.zones.on_overlap`` is passed both to the session's own partition and into the
   ``ZoneOccupancy`` constructor (:func:`_construct`).  Miss it and overlap silently reverts
   to ``first_match``.
3. **``PrimitiveEvent.kind`` is the stage name**, not an incident key.  The incident type is
   resolved from ``incidents.types[].severity_from`` naming a stage (:class:`_IncidentRule`),
   never by matching ``kind`` against ``incidents.types[].key``.
4. **``WindowOutput`` is already aggregated** -- see
   :mod:`matrice_analytics.engine.runtime.window`, which publishes it verbatim.
5. **Track ids travel on ``PrimitiveOutput.tracks`` *and* on the detections the later stages
   see.**  A tracker stage publishes its ``tracks`` map -- that is still the channel
   ``unique_count`` prefers, and it still carries entity, timing and per-track attributes
   that a detection cannot.  This module additionally **stamps
   ``PipelineDetection.track_id``** from that map, joining on
   ``TrackState.attributes["det_index"]``, before it builds the ``FrameContext`` for the
   stages that come after the tracker (:func:`_stamp_track_ids`).

   The original rule was "never back-fill", and it starved three primitives:
   ``line_crossing``, ``dwell`` and ``velocity_state`` all read ``det.track_id``, found
   ``None``, and published zeros -- silently, because "a tracker associated nothing" and "the
   ids never arrived" were one code path.  A field named ``track_id`` on a *pipeline*
   detection that the pipeline refuses to fill in is a trap, so the pipeline fills it in:
   ``PipelineDetection`` exists precisely to carry the fields the pipeline adds (its
   ``entity`` and ``zone`` are filled in the same way, by this same module).

   Three properties keep the original concern -- two stages with two ideas of identity --
   from coming back:

   * the stamp is a **copy**, not a mutation.  ``FrameContext`` still hands each stage a set
     no earlier stage has written to, and the ``global`` bucket's ids cannot leak into a zone
     bucket that shares detection objects with it;
   * only a stage the *manifest* declares as ``track`` may stamp (:attr:`Session._track_stages`),
     so a ``dwell`` or ``velocity_state`` ``tracks`` map -- neither of which carries a
     ``det_index`` -- cannot overwrite an id;
   * what the caller gave us is left alone: ``zone_detections`` and the wire ``detections[]``
     carry the ids the *input* had, so the payload surface is unchanged.

Nothing here imports ``post_processing`` or ``analytics`` (**PY-20**): a runtime import used
to execute ~180 legacy modules and pull in torch and cv2.
"""

from __future__ import annotations

import inspect
import logging
import uuid
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Final

from pydantic import BaseModel, ValidationError

from matrice_analytics.engine.contract.emit import (
    Publisher,
    build_frame_result,
    build_incident,
    publish_aggregation,
    publish_incident,
    to_payload,
)
from matrice_analytics.engine.contract.schemas import (
    GLOBAL_ZONE,
    SEVERITY_RANK,
    UNASSIGNED_ZONE,
    AggregationResult,
    BoundingBox,
    Detection,
    FrameResult,
    FrameSummaryEntry,
    FrameTrackingStats,
    Incident,
    IncidentMessage,
    Severity,
    StreamInfo,
    parse_severity,
    parse_stream_time,
    to_rfc3339z,
)
from matrice_analytics.engine.manifest.expr import EvaluationError
from matrice_analytics.engine.manifest.models import (
    AcrossZonesLiteral,
    AppManifest,
    CustomConfig,
    DetectConfig,
    IncidentLifecycle,
    IncidentType,
    MetricThreshold,
    PrimitiveConfig,
    TrackConfig,
    ZoneOccupancyConfig,
)
from matrice_analytics.engine.primitives import REGISTRY
from matrice_analytics.engine.primitives.base import (
    Clock,
    FrameClock,
    FrameContext,
    Keypoint,
    MaskRef,
    PipelineDetection,
    Primitive,
    PrimitiveEvent,
    PrimitiveOutput,
    PrimitiveRegistry,
    WindowOutput,
    conformance_problems,
)
from matrice_analytics.engine.primitives.geometry import (
    SceneGeometry,
    ZoneAssignment,
    assign_detections_to_zones,
)
from matrice_analytics.engine.runtime.stream_info import resolve_stream_info
from matrice_analytics.engine.runtime.window import (
    AggregationWindow,
    _number,
    collapse_zones,
    derived_plan,
    human_text_for,
    metric_plan,
    stage_key_map,
)
from matrice_analytics.engine.state import InMemoryStateStore, Lifetime, StateStore

if TYPE_CHECKING:  # pragma: no cover - typing only
    from matrice_analytics.engine.manifest.loader import CustomImpl, LoadedApp

__all__ = [
    "DEFAULT_THRESHOLD_SEVERITY",
    "FrameOutcome",
    "Session",
    "SessionError",
]

logger = logging.getLogger(__name__)


DEFAULT_THRESHOLD_SEVERITY: Final[str] = "medium"
"""Severity for a ``severity_from: {metric: {">": n}}`` rule with no graded ``levels``.

A bare threshold says *this is a violation*; it does not say how bad.  The middle rung is the
honest reading, and a manifest that means something else says so with ``levels:``.  Defaulting
to ``critical`` would page someone at 3am for a config that never asked to.
"""

#: How many frames of "still happening" are remembered before confirmation.  Bounded so a
#: week-long incident cannot grow an unbounded counter in the state store.
_MAX_STREAK: Final[int] = 10_000

#: Keys a raw detection mapping may use for each field.  Deliberately generous on *input* and
#: exact on output: the detections dict is not ours (surface S3, doc ``04``) and every producer
#: in the tree spells at least one of these differently.
_CATEGORY_KEYS: Final[tuple[str, ...]] = ("category", "class", "class_name", "label", "name")
_CONFIDENCE_KEYS: Final[tuple[str, ...]] = ("confidence", "score", "conf")
_BOX_KEYS: Final[tuple[str, ...]] = ("bounding_box", "bbox", "box", "xyxy")
_TRACK_KEYS: Final[tuple[str, ...]] = ("track_id", "trackId", "tracker_id")
_INDEX_KEYS: Final[tuple[str, ...]] = ("class_id", "class_index", "index")
#: Where a segmentation mask hides.  ``segmentation`` is the live wire spelling
#: (``04`` §5.1) and the rest are what the legacy ingest whitelist already carries
#: (``landslide_detection.py:889-901``): ``masks``/``mask``, plus the flat ``mask_rle`` +
#: ``shape`` + ``segmentation_area`` triple the dual-port backend record is flattened into
#: (``:834-836``).
_MASK_KEYS: Final[tuple[str, ...]] = ("segmentation", "mask", "masks", "segmentation_mask")
_MASK_RLE_KEYS: Final[tuple[str, ...]] = ("counts", "rle", "mask_rle")
_MASK_SIZE_KEYS: Final[tuple[str, ...]] = ("size", "shape", "mask_shape")
_MASK_AREA_KEYS: Final[tuple[str, ...]] = ("area_px", "area_pixels", "segmentation_area")
_MASK_POLYGON_KEYS: Final[tuple[str, ...]] = ("polygon", "contour", "segmentation")
#: A polygon vertex is ``[x, y]`` (or ``[x, y, z]``, the third number ignored) -- never more.
#: A row this long is not a vertex; it is one row of a dense pixel-mask array sent undecoded
#: (see ``_to_polygon``, which raises on it rather than silently reading its first two pixels
#: as a coordinate).
_MAX_POLYGON_VERTEX_LEN: Final[int] = 3
#: A real contour has, at most, a few thousand points. A polygon this long -- either spelling
#: -- is almost certainly a dense pixel-mask array (``height * width`` numbers) rather than a
#: contour (see ``_to_polygon``).
_MAX_POLYGON_POINTS: Final[int] = 10_000
#: One spelling only -- ``keypoints`` is the wire name (``04`` §5.1) and the single key all
#: three legacy pose extractors read (``fall_detection.py:64`` and both siblings).
_KEYPOINT_KEY: Final[str] = "keypoints"
#: Where the model input dimensions come from when the keypoints are in pixel space.  ``[w, h]``
#: for ``keypoint_space``/``image_size``; ``shape`` is ``[h, w]`` like a numpy shape.
_KEYPOINT_SPACE_KEYS: Final[tuple[str, ...]] = ("keypoint_space", "image_size", "input_shape")
_BOX_CORNER_ALIASES: Final[tuple[tuple[str, ...], ...]] = (
    ("xmin", "x1", "left", "x"),
    ("ymin", "y1", "top", "y"),
    ("xmax", "x2", "right"),
    ("ymax", "y2", "bottom"),
)


class SessionError(ValueError):
    """The session cannot run this manifest against this stream.

    Always raised at **setup**, never per frame (``09`` §5).  Every condition it covers --
    an unimplemented primitive, a missing geometry requirement, a zone name that collides
    with the ``global`` bucket -- would otherwise produce a stream of plausible zeros, and a
    plausible zero is indistinguishable from a quiet camera.
    """


# ---------------------------------------------------------------------------
# What one frame produced
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FrameOutcome:
    """Everything one frame produced, for the caller and for tests."""

    frame_ts: float
    """The frame's own timestamp, epoch seconds (**PY-13**)."""

    zone_outputs: Mapping[str, Mapping[str, PrimitiveOutput]]
    """``bucket -> stage name -> output``.  Includes the ``global`` bucket."""

    zone_detections: Mapping[str, tuple[PipelineDetection, ...]]
    """``bucket -> the detections that pipeline saw``, after remap and partition."""

    metric_values: Mapping[str, float]
    """This frame's reading of each declared metric -- a flat ``{key: value}`` map, so a
    ``zone: per_zone`` metric has no zone to be reported under and is instead the **sum
    across every zone the app emits** (:attr:`Session.emission_zones`); a ``zone: global``
    metric reads the ``global`` bucket, as it always has.

    What a metric-threshold ``incidents.types[].severity_from`` is evaluated against
    (**always** the ``global`` bucket -- see :meth:`Session._active_for`, unaffected by the
    summing above). An event-driven incident's (``incident_quantise``) ``human_text``
    placeholders are resolved separately, from the zone the incident actually fired in
    (:meth:`Session._advance`) -- summing here would be the wrong answer for a per-zone
    alert about ONE zone. A metric whose source did not resolve in any zone this frame is
    absent rather than zero (``09`` §3).
    """

    incidents: tuple[IncidentMessage, ...] = ()
    """``incident_res`` messages raised by this frame -- on a **transition** only."""

    aggregation: AggregationResult | None = None
    """The ``results-agg`` message, on the frame that closed a window; else ``None``."""

    frame_result: FrameResult | None = None
    """The per-frame return value (surface S3), when ``emission.frame_summary`` is true."""

    unassigned: int = 0
    """Detections that fell inside no drawn zone (**PY-10**: countable, never silent)."""

    unmapped: int = 0
    """Detections whose model label is in no ``model.entity_mapping`` alias set.

    The single most common cause of an empty dashboard (``FIELD_REFERENCE`` §14), and today it
    produces no signal at all.  A non-zero value here on every frame means the mapping's
    right-hand side does not match the model's labels.
    """

    def payload(self) -> dict[str, Any]:
        """The S3 return dict, or ``{}`` when frame summaries are switched off.

        py_analytics does **not** publish this: it returns it, and an inference worker outside
        this workspace XADDs it to ``<cameraId>_<appDeploymentId>_output_topic``.  We own
        ``agg_summary`` and the detections inside it and nothing else in that envelope
        (backlog **Q5**).
        """
        return {} if self.frame_result is None else to_payload(self.frame_result)


# ---------------------------------------------------------------------------
# Entity remap
# ---------------------------------------------------------------------------


class _EntityMapper:
    """``model.entity_mapping`` inverted: model label -> analytics entity.

    The mapping's right-hand side must match the detector's labels character for character
    (``08`` §3), and nothing can validate that from the manifest -- so this counts the misses
    instead of discarding them silently.
    """

    __slots__ = ("_by_index", "_by_label", "_by_label_ci", "_label_by_index")

    def __init__(self, manifest: AppManifest) -> None:
        self._by_label: dict[str, str] = {}
        self._by_label_ci: dict[str, str] = {}
        for entity, labels in manifest.model.entity_mapping.items():
            for label in labels:
                self._by_label[label] = entity
                self._by_label_ci.setdefault(label.strip().lower(), entity)
        self._by_index: dict[int, str] = {}
        self._label_by_index: dict[int, str] = {}
        unmapped: list[str] = []
        for index, label in (manifest.model.index_to_category or {}).items():
            self._label_by_index[int(index)] = label
            entity = self._by_label.get(label) or self._by_label_ci.get(label.strip().lower())
            if entity is not None:
                self._by_index[int(index)] = entity
            else:
                unmapped.append(f"{index}={label!r}")
        if unmapped:
            # INFO, not WARNING: declaring a class the app does not map is legitimate and
            # common -- filtering by entity_mapping is the point, and a sparse COCO head's
            # slot 0 is genuinely unused. So this states a fact rather than raising an alarm,
            # at construction, once per session.
            #
            # It is worth stating because the inverse case is indistinguishable from here and
            # cost days: a weapon deployment shipped `{"0": "knife", "1": "gun "}` against a
            # six-class manifest, and the trailing space meant `gun` mapped to nothing while
            # looking correct. The whitespace itself is now handled where the label is read;
            # this line is what makes the remaining "declared but counted by nothing" set
            # visible without having to infer it from an absence of incidents.
            logger.info(
                "entity_mapping: %d index_to_category entr%s map to no entity in this "
                "manifest and %s ignored: %s. The manifest maps %s. Expected when an app "
                "deliberately declares classes it does not count; check for a typo or stray "
                "whitespace if one of these was meant to be mapped.",
                len(unmapped),
                "y" if len(unmapped) == 1 else "ies",
                "is" if len(unmapped) == 1 else "are",
                ", ".join(sorted(unmapped)),
                sorted(self._by_label),
            )

    def entity_for(self, label: str, index: int | None) -> str | None:
        """The entity for a model label, or ``None`` when the app never mapped it.

        Exact match wins.  A case-insensitive match is accepted as a *second* pass because
        ``"Person"`` vs ``"person"`` is the single most common spelling miss and silently
        counting zero is a worse answer than counting the detection; ``index_to_category`` is
        the last resort, for deployments that send a class index and no label.
        """
        if label:
            entity = self._by_label.get(label)
            if entity is not None:
                return entity
            entity = self._by_label_ci.get(label.strip().lower())
            if entity is not None:
                return entity
        if index is not None:
            return self._by_index.get(int(index))
        return None

    def label_for_index(self, index: int | None) -> str:
        """The model label ``index_to_category`` gives a class index, or ``""``."""
        return "" if index is None else self._label_by_index.get(int(index), "")

    def is_bare_index(self, label: str) -> bool:
        """Whether ``label`` is a class index wearing a label's clothing, e.g. ``"1"``.

        A detector with no label map sends its index where the label goes.  ``"1"`` is a
        *truthy* string, so it survives every ``or`` chain that means to fall back and reaches
        the overlay as the drawn label -- which is how one payload came to report
        ``category="1"`` in ``current_counts`` and ``"person"`` in ``total_counts``.

        A numeric string the app actually *mapped* is not bare: a model may legitimately call
        its classes ``"0"`` and ``"1"``, and second-guessing that would rename its classes.
        """
        return _ascii_digits(label) and label.strip() not in self._by_label

    def display_label(self, label: str, index: int | None) -> str:
        """The label to draw for a detection, preferring a real name over a bare index.

        ``index_to_category`` wins over a bare index and *only* over a bare index -- a genuine
        model label is never overridden.  Returns ``""`` only when there was nothing to work
        with, which leaves the caller's own fallback (the entity name) to apply.
        """
        if label and not self.is_bare_index(label):
            return label
        return self.label_for_index(index) or label

    @property
    def labels(self) -> tuple[str, ...]:
        """Every model label this app mapped, sorted -- for the "nothing matched" warning."""
        return tuple(sorted(self._by_label))


# ---------------------------------------------------------------------------
# Incident rules (§6b coupling 3)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class _IncidentRule:
    """One ``incidents.types[]`` entry, resolved against the pipeline at setup.

    **``PrimitiveEvent.kind`` is a stage name, not an incident key** (§6b coupling 3).
    ``IncidentQuantiseConfig`` has no incident key at all; the manifest joins the other way,
    with ``severity_from: <stage>``.  Matching ``kind`` against
    ``incidents.types[].key`` would therefore match nothing, forever, with no error -- so the
    join is resolved once, here, and recorded as :attr:`stage`.
    """

    spec: IncidentType
    stage: str = ""
    """The stage whose events raise this incident, for ``severity_from: <stage>``."""

    thresholds: Mapping[str, MetricThreshold] = field(default_factory=dict)
    """``{metric_key: threshold}`` for ``severity_from: {metric: {op: value}}``."""

    @property
    def key(self) -> str:
        return self.spec.key

    @property
    def is_event_driven(self) -> bool:
        return bool(self.stage)


# ---------------------------------------------------------------------------
# The session
# ---------------------------------------------------------------------------


class Session:
    """One camera running one app.

    Built once per ``(camera, app deployment)`` and fed frames in order.  Everything that can
    fail because of a bad manifest/installation combination fails in the constructor:
    unimplemented primitives, missing zone or line geometry, a zone name that collides with
    the ``global`` bucket, an incident rule that could never fire.

    Example:
        >>> from matrice_analytics.engine.manifest.loader import load_app_bundle
        >>> app = load_app_bundle("apps/people_counting")           # doctest: +SKIP
        >>> session = Session.from_loaded_app(app, stream_info)     # doctest: +SKIP
        >>> outcome = session.process_frame(detections, frame_ts=1_700_000_000.0)
        >>> outcome.aggregation is None      # no window boundary yet    # doctest: +SKIP
        True
    """

    __slots__ = (
        "_all_in_one_stages",
        "_clock",
        "_custom",
        "_derived_plan",
        "_emission_zones",
        "_entities",
        "_geometry",
        "_incident_state",
        "_intake_floor",
        "_keypoint_space_warned",
        "_manifest",
        "_mapper",
        "_metric_plan",
        "_pipelines",
        "_polygons",
        "_publisher",
        "_reference_point",
        "_registry",
        "_reset_timestamp",
        "_rules",
        "_stage_keys",
        "_stage_order",
        "_state",
        "_stream",
        "_track_stages",
        "_unmapped_warned",
        "_window",
        "_window_state",
        "_zone_polygons",
        "_zoned",
    )

    # -- construction -------------------------------------------------------

    def __init__(
        self,
        manifest: AppManifest,
        stream: StreamInfo,
        *,
        state: StateStore | None = None,
        clock: Clock | None = None,
        registry: PrimitiveRegistry | None = None,
        custom: Mapping[str, "CustomImpl"] | None = None,
        publisher: Publisher | None = None,
        started_at: float | None = None,
    ) -> None:
        """Build the pipelines for every zone this app runs in.

        Args:
            manifest: The validated manifest, from
                :func:`~matrice_analytics.engine.manifest.loader.load_app`.
            stream: The typed input (surface S4).  Use
                :func:`~matrice_analytics.engine.runtime.stream_info.parse_stream_info` to get
                one from the worker's untyped dict, so the fallbacks it took are logged.
            state: The root state scope.  Defaults to a fresh
                :class:`~matrice_analytics.engine.state.memory.InMemoryStateStore`; pass one in
                to share a backing between sessions or to assert on keys in a test.
            clock: The session's clock.  Defaults to a
                :class:`~matrice_analytics.engine.primitives.base.FrameClock`, which advances
                only when a frame says so -- never ``time.time()`` (**PY-13**).
            registry: Primitive registry.  Defaults to the process-wide
                :data:`~matrice_analytics.engine.primitives.base.REGISTRY`.
            custom: ``stage name -> CustomImpl`` from
                :func:`~matrice_analytics.engine.manifest.loader.load_app_bundle`.  Required
                when the pipeline declares a ``custom`` stage: the manifest can name one, but
                only the loader can import it.
            publisher: Where ``results-agg`` and ``incident_res`` go.  ``None`` means the
                session builds and validates payloads and hands them back on
                :class:`FrameOutcome` without publishing -- which is exactly what a test wants.
            started_at: Process/session start, epoch seconds, used as every zone's
                ``reset_timestamp`` (**FROZEN-4**: totals mean "since this instant").  Defaults
                to the first frame's timestamp.

        Raises:
            SessionError: The manifest cannot be run against this stream.
        """
        self._manifest = manifest
        self._stream = stream
        self._state: StateStore = state if state is not None else InMemoryStateStore()
        self._clock: Clock = clock if clock is not None else FrameClock()
        self._custom: Mapping[str, "CustomImpl"] = dict(custom or {})
        self._publisher = publisher
        self._registry: PrimitiveRegistry = registry if registry is not None else REGISTRY
        self._mapper = _EntityMapper(manifest)
        # A session-level scope for bookkeeping that belongs to no single stage -- the zone
        # partition counters behind `_report_partition`. Scoped under a reserved name so it
        # cannot collide with a stage: `__session__` is not a legal stage_name.
        self._window_state: StateStore = (
            self._state.scoped(stream.camera_id).scoped(manifest.app.id).scoped(GLOBAL_ZONE).scoped("__session__")
        )
        self._stage_keys = stage_key_map(manifest)
        self._metric_plan = metric_plan(manifest)
        self._derived_plan = derived_plan(manifest)
        self._entities: tuple[str, ...] = tuple(sorted(manifest.model.entities))
        self._stage_order: tuple[str, ...] = tuple(stage.stage_name for stage in manifest.pipeline)
        # §6b coupling 5: the stages allowed to stamp det.track_id. Taken from the manifest,
        # not from "which stage published tracks", because dwell, velocity_state and
        # state_machine publish tracks too and none of them carries the det_index the join
        # needs -- letting them stamp would hand a later stage an id derived from an earlier
        # stage's opinion rather than from the tracker.
        self._track_stages: frozenset[str] = frozenset(
            stage.stage_name for stage in manifest.pipeline if isinstance(stage, TrackConfig)
        )
        # `custom` stages that declared `zones: all_in_one`. They are built in the `global`
        # bucket only and handed the whole frame with each detection's own zone still on it --
        # see _all_zones_view. Only `custom` can be in here (CustomConfig owns the field).
        self._all_in_one_stages: frozenset[str] = frozenset(
            stage.stage_name for stage in manifest.pipeline if stage.all_in_one
        )
        self._unmapped_warned = False
        self._keypoint_space_warned = False
        self._reset_timestamp = to_rfc3339z(started_at) if started_at is not None else ""
        self._intake_floor = self._resolve_intake_floor()

        self._check_runnable()
        self._geometry = SceneGeometry.from_stream_info(stream)
        self._check_geometry()

        self._zoned, self._zone_polygons = self._resolve_zones()
        self._reference_point = self._resolve_reference_point()
        self._emission_zones = self._resolve_emission_zones()

        self._pipelines = {bucket: self._build_pipeline(bucket) for bucket in self.buckets}
        self._rules = self._resolve_incident_rules()
        self._incident_state = self._state.scoped("incidents")
        self._window = AggregationWindow(
            manifest,
            stream,
            self._clock,
            self._state,
            emission_zones=self._emission_zones,
            reset_timestamp=self._reset_timestamp,
        )

        logger.info(
            "session ready: app=%s v%s camera=%s stages=%s buckets=%s emitting=%s",
            manifest.app.id,
            manifest.app.version,
            stream.camera_id,
            list(self._stage_order),
            list(self.buckets),
            list(self._emission_zones),
        )

    @classmethod
    def from_loaded_app(
        cls,
        app: "LoadedApp",
        stream_info: Mapping[str, Any] | StreamInfo | None,
        **kwargs: Any,
    ) -> "Session":
        """Build a session from a loaded app bundle and the worker's raw ``stream_info``.

        The whole chain from ``STAGE_BC_PLAN`` §4 in one call::

            load_app_bundle(ref) -> Session.from_loaded_app(app, stream_info)
                                 -> session.process_frame(detections, frame_ts=...)

        Args:
            app: What :func:`~...loader.load_app_bundle` returned -- its ``manifest`` and its
                already-imported ``custom`` implementations.
            stream_info: The untyped worker dict (parsed and logged by
                :func:`~...runtime.stream_info.resolve_stream_info`) or an already-typed
                :class:`StreamInfo`.
            **kwargs: Passed through to :class:`Session`.

        Returns:
            The ready session.

        Raises:
            StreamInfoError: A required ``stream_info`` field is missing.
            SessionError: The manifest cannot be run against this stream.
        """
        stream = stream_info if isinstance(stream_info, StreamInfo) else resolve_stream_info(stream_info).stream
        kwargs.setdefault("custom", getattr(app, "custom", None))
        return cls(app.manifest, stream, **kwargs)

    # -- setup checks -------------------------------------------------------

    def _resolve_intake_floor(self) -> float:
        """The intake confidence floor.

        ``model.confidence_threshold``, lowered to the smallest ``detect.min_confidence`` any
        stage declared -- because that field documents itself as an *override* of the model
        threshold, and a stage cannot see the model block (``09`` §1).  Filtering at the model
        floor first would make a lower override unreachable, so the intake admits the union and
        each ``detect`` stage still applies its own.

        ``min_confidence_per_class`` is an override of the *override* and counts the same way:
        a per-class floor below the stage's own ``min_confidence`` is unreachable if intake
        already discarded the detections, and "the floor I set is ignored" is the defect this
        method exists to prevent.  A per-class floor **above** it -- the PPE case, ``no_hardhat``
        at 0.91 against a stage floor of 0.5 -- costs nothing here: ``min`` ignores it, and the
        primitive applies it where it belongs.
        """
        floor = float(self._manifest.model.confidence_threshold)
        for stage in self._manifest.pipeline:
            if not isinstance(stage, DetectConfig):
                continue
            if stage.min_confidence is not None:
                floor = min(floor, float(stage.min_confidence))
            for per_class in stage.min_confidence_per_class.values():
                floor = min(floor, float(per_class))
        return floor

    def _check_runnable(self) -> None:
        """Refuse a manifest naming something this build cannot run (``09`` §5)."""
        unimplemented = self._manifest.unimplemented_primitives()
        if unimplemented:
            raise SessionError(
                f"app {self._manifest.app.id!r} declares primitive(s) "
                f"{', '.join(unimplemented)} that this engine has not implemented. The "
                "manifest schema deliberately validates apps ahead of the runtime (08 §2), so "
                "this is a startup refusal rather than a load error -- running on would "
                "publish a pipeline with a silently missing stage."
            )
        missing: list[str] = []
        for stage in self._manifest.pipeline:
            if isinstance(stage, CustomConfig):
                if stage.stage_name not in self._custom:
                    raise SessionError(
                        f"stage {stage.stage_name!r} is a custom primitive ({stage.impl!r}) but "
                        "no implementation was supplied. Build the session with "
                        "Session.from_loaded_app(load_app_bundle(ref), ...) -- only the loader "
                        "imports and validates the app's Python."
                    )
                problems = conformance_problems(self._custom[stage.stage_name].obj, custom=True)
                if problems:
                    raise SessionError(
                        f"custom stage {stage.stage_name!r} does not implement the "
                        "CustomPrimitive protocol:\n  - " + "\n  - ".join(problems)
                    )
                continue
            if stage.PRIMITIVE not in self._registry:
                missing.append(stage.PRIMITIVE)
        if missing:
            raise SessionError(
                f"no implementation is registered for {', '.join(sorted(set(missing)))}. "
                f"Registered: {', '.join(self._registry.names()) or '(none)'}. A manifest naming an "
                "unregistered primitive must fail at session start, not emit nothing (09 §5)."
            )

    def _check_geometry(self) -> None:
        """Check the camera against the geometry the manifest says it needs.

        The requirements are the manifest's own words
        (:meth:`AppManifest.geometry_requirements`), and they divide in two:

        ``exact`` -- **always fatal.**  ``line_crossing.method: abline`` infers direction from
        the order two parallel lines are crossed in; with one line there is no order and with
        three there is no pairing, so the counter reports zero forever without complaining.

        ``minimum`` -- fatal only when ``zones.required`` is true.  That field exists precisely
        to say whether a camera with no geometry is a startup error, and ``zone_occupancy``
        declares its own documented fallback ("with no zone geometry every detection lands in
        the 'unassigned' bucket").  Refusing to start regardless would override the one field
        an author has to express the choice -- so it is a warning naming the consequence.
        """
        required_zones = self._manifest.zones is not None and self._manifest.zones.required
        problems: list[str] = []
        for requirement in self._manifest.geometry_requirements():
            have = len(self._geometry.zone_names()) if requirement.kind == "zones" else len(self._geometry.line_names())
            if requirement.exact is not None and have != requirement.exact:
                problems.append(f"{requirement.describe()} This camera has {have}.")
            elif requirement.minimum is not None and have < requirement.minimum:
                if requirement.kind == "lines" or required_zones:
                    problems.append(f"{requirement.describe()} This camera has {have}.")
                else:
                    logger.warning(
                        "camera %s has no zone geometry: %s Set zones.required: true to make "
                        "this a startup error instead.",
                        self._stream.camera_id,
                        requirement.describe(),
                    )
        if problems:
            raise SessionError(
                f"camera {self._stream.camera_id!r} does not have the geometry app "
                f"{self._manifest.app.id!r} requires:\n  - " + "\n  - ".join(problems)
            )

    def _resolve_zones(self) -> tuple[bool, tuple[str, ...]]:
        """Decide whether this app runs per zone, and over which zone identities.

        Zoning is **opt-in from the manifest**: a camera may have polygons drawn for a
        different app, and partitioning an app that never mentioned zones would split its
        series without anyone asking.  A ``zones:`` block or a ``zone_occupancy`` stage is the
        opt-in.

        The partition covers exactly the zones the app asked for.  A ``zone_occupancy`` stage
        naming three of a camera's five polygons gets three buckets, not five: the other two
        would otherwise reach the wire as zone series this app never declared, and a stray
        ``zoneId`` in ClickHouse is indistinguishable from a real one.

        Raises:
            SessionError: A named zone is not drawn on this camera, or a drawn zone collides
                with an engine bucket name.  The first is
                :meth:`SceneGeometry.select_zones`' own error, re-raised as a session failure
                because it is a manifest/installation mismatch found at startup.
        """
        wants_zones = self._manifest.zones is not None or any(
            isinstance(stage, ZoneOccupancyConfig) for stage in self._manifest.pipeline
        )
        try:
            self._polygons = self._geometry.select_zones(self._wanted_zones())
        except ValueError as exc:  # GeometryError subclasses ValueError
            raise SessionError(str(exc)) from exc
        identities = tuple(zone.identity for zone in self._polygons)
        if not wants_zones or not identities:
            self._polygons = ()
            return (False, ())

        collisions = [name for name in identities if name in {GLOBAL_ZONE, UNASSIGNED_ZONE}]
        if collisions:
            raise SessionError(
                f"camera {self._stream.camera_id!r} has zone(s) named {collisions}, which "
                f"collide with the engine's own bucket names {[GLOBAL_ZONE, UNASSIGNED_ZONE]}. "
                "Both names reach ClickHouse as zoneId, so the drawn zone's counts would merge "
                "with the whole-frame or no-match bucket. Rename the zone in the streaming UI."
            )
        return (True, identities)

    def _wanted_zones(self) -> str | list[str]:
        """``"all"``, or the union of the zone names the ``zone_occupancy`` stages listed."""
        named: list[str] = []
        for stage in self._manifest.pipeline:
            if not isinstance(stage, ZoneOccupancyConfig):
                continue
            if stage.zones == "all":
                return "all"
            for name in stage.zones:
                if name not in named:
                    named.append(name)
        return named or "all"

    def _resolve_reference_point(self) -> str:
        """Which point of a box decides zone membership, for the session's own partition.

        Taken from the ``zone_occupancy`` stage when there is one, so the partition and that
        stage cannot disagree about where a person is standing; ``foot_center`` otherwise --
        the new default, and a deliberate change from the legacy ``use_foot_center=False``
        (``analytics/geometry.py:184``), which puts a tall person in the zone behind the one
        they are standing in.
        """
        for stage in self._manifest.pipeline:
            if isinstance(stage, ZoneOccupancyConfig):
                return stage.reference_point
        return "foot_center"

    def _resolve_emission_zones(self) -> tuple[str, ...]:
        """The zones that reach the wire (**FROZEN-2**, **PY-5**)."""
        if not self._zoned:
            return (GLOBAL_ZONE,)
        zones = list(self._zone_polygons)
        if self._no_match_policy == "unassigned":
            # PY-10: the bucket is emitted, not hidden. A series called 'unassigned' that is
            # suddenly non-zero is how an operator finds out a polygon was redrawn badly.
            zones.append(UNASSIGNED_ZONE)
        return tuple(zones)

    @property
    def _no_match_policy(self) -> str:
        spec = self._manifest.zones
        if spec is not None:
            return spec.on_no_match
        for stage in self._manifest.pipeline:
            if isinstance(stage, ZoneOccupancyConfig):
                return stage.on_no_match
        return "unassigned"

    @property
    def _on_overlap(self) -> str:
        """``zones.on_overlap`` -- **on ``ZonesSpec``**, not on the stage (§6b coupling 2)."""
        return self._manifest.zones.on_overlap if self._manifest.zones is not None else "first_match"

    def _build_pipeline(self, bucket: str) -> dict[str, Primitive]:
        """Instantiate one pipeline for one bucket, in manifest order.

        Each stage gets a store scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` (``09`` §4),
        so two zones cannot share a tracker, a dwell clock or a seen-id set, and two cameras
        cannot share anything at all.

        The one exception is a ``custom`` stage that declared ``zones: all_in_one``: it is
        built **only in the ``global`` bucket**, so there is exactly one instance and exactly
        one store, ``<camera_id>/<app_id>/global/<stage>``.  That is the whole point of the
        flag -- a queue→counter handoff clock written under ``Queue`` was invisible to the
        instance running under ``Counter``, and ``StateStore.scoped()`` only goes deeper, so
        there was no way up.  One bucket, one scope, no way to write a handoff into a store
        the other half of the handoff cannot read.
        """
        pipeline: dict[str, Primitive] = {}
        for stage in self._manifest.pipeline:
            if stage.all_in_one and bucket != GLOBAL_ZONE:
                continue
            scope = self._scope_for(bucket, stage.stage_name)
            if isinstance(stage, CustomConfig):
                impl = self._custom[stage.stage_name]
                pipeline[stage.stage_name] = _CustomStage(stage.stage_name, impl.obj, impl.config, scope)
                continue
            pipeline[stage.stage_name] = _construct(
                self._registry.get(stage.PRIMITIVE),
                stage,
                scope,
                geometry=self._geometry,
                on_overlap=self._on_overlap,
                zoned=self._zoned,
                bucket=bucket,
            )
        return pipeline

    def _scope_for(self, bucket: str, stage_name: str) -> StateStore:
        store = self._state
        for component in (self._stream.camera_id, self._manifest.app.id, bucket, stage_name):
            store = store.scoped(component)
        return store

    def _resolve_incident_rules(self) -> tuple[_IncidentRule, ...]:
        """Resolve every ``incidents.types[]`` entry against the pipeline (§6b coupling 3).

        Raises:
            SessionError: ``severity_from`` names a fixed severity level.  The manifest allows
                it and documents it as "always this severity while the incident is open", but
                nothing states what *opens* it -- so this runtime cannot raise it, and an
                incident type that can never fire is exactly the silent nothing this engine
                exists to remove.  Point ``severity_from`` at an ``incident_quantise`` stage or
                at a metric threshold.
        """
        spec = self._manifest.incidents
        if spec is None:
            return ()
        rules: list[_IncidentRule] = []
        for incident in spec.types:
            source = incident.severity_from
            if isinstance(source, Mapping):
                rules.append(_IncidentRule(spec=incident, thresholds=dict(source)))
                continue
            if source in {member.value for member in Severity}:
                raise SessionError(
                    f"incidents.types[{incident.key!r}].severity_from is the fixed level "
                    f"{source!r}. A fixed level says how severe the incident is but not what "
                    "raises it, so this runtime has no trigger to bind it to and the type "
                    "would never fire. Use severity_from: <an incident_quantise stage>, or a "
                    "metric threshold such as {my_metric: {'>': 0}}."
                )
            stage_name = self._stage_keys.get(source)
            if stage_name is None:
                raise SessionError(
                    f"incidents.types[{incident.key!r}].severity_from names {source!r}, which "
                    f"is not a stage in this pipeline ({', '.join(self._stage_order)})."
                )
            rules.append(_IncidentRule(spec=incident, stage=stage_name))
        return tuple(rules)

    # -- introspection ------------------------------------------------------

    @property
    def manifest(self) -> AppManifest:
        return self._manifest

    @property
    def stream(self) -> StreamInfo:
        """The typed per-camera input.  Passed into every :class:`FrameContext`."""
        return self._stream

    @property
    def geometry(self) -> SceneGeometry:
        """The camera's geometry, resolved to pixels **once**, here (**PY-7**)."""
        return self._geometry

    @property
    def buckets(self) -> tuple[str, ...]:
        """Every bucket a pipeline runs in: ``global`` first, then the zones."""
        if not self._zoned:
            return (GLOBAL_ZONE,)
        return (GLOBAL_ZONE, *self._emission_zones)

    @property
    def emission_zones(self) -> tuple[str, ...]:
        """The zones that appear in ``tracking_stats`` / ``agg_summary`` (**PY-5**)."""
        return self._emission_zones

    @property
    def stage_names(self) -> tuple[str, ...]:
        """Stage names in pipeline order -- the keys of ``ctx.previous``."""
        return self._stage_order

    @property
    def window(self) -> AggregationWindow:
        """The open aggregation window."""
        return self._window

    def __repr__(self) -> str:
        return (
            f"Session(app={self._manifest.app.id!r}, camera={self._stream.camera_id!r}, "
            f"buckets={list(self.buckets)!r}, stages={list(self._stage_order)!r})"
        )

    # -- the frame ----------------------------------------------------------

    def process_frame(
        self,
        detections: Sequence[Any],
        *,
        frame_ts: float | None = None,
        frame_id: str | None = None,
        stream_time: str | None = None,
        rtp_number: str | None = None,
    ) -> FrameOutcome:
        """Run one frame through every bucket's pipeline.

        Args:
            detections: This frame's detections.  Accepts
                :class:`~matrice_analytics.engine.primitives.base.PipelineDetection`,
                :class:`~matrice_analytics.engine.contract.schemas.Detection`, or the plain
                dicts the pipeline actually sends (see :func:`_to_detection` for the spellings
                accepted).  Bounding boxes are **normalized 0-1** (contract §4).
            frame_ts: The frame's real timestamp, epoch seconds.  Omit it only when
                ``stream_time`` (here or on the stream) carries the media anchor -- there is
                no fallback to ``time.time()``, because that fallback is **PY-13**.
            frame_id: This frame's media key, if it changes per frame.
            stream_time: This frame's media anchor in the §3.3 format.
            rtp_number: This frame's RTP timestamp, the anchor the media server resolves the
                alert image from.  Per frame like the two above, **not** per session: left at
                the session's first value every incident on the camera resolves to the same
                thumbnail and the same looked-up wall-clock time.

        Returns:
            The :class:`FrameOutcome`.

        Raises:
            SessionError: A detection cannot be read, or no frame timestamp is available.
            ValueError: ``frame_ts`` goes backwards -- :class:`FrameClock` refuses to reopen a
                window it already published.  Drop the frame, or reset the clock explicitly.
        """
        resolved_ts = self._frame_timestamp(frame_ts, stream_time)
        if isinstance(self._clock, FrameClock):
            self._clock.advance(resolved_ts)
        if not self._reset_timestamp:
            # FROZEN-4: totals mean "since this instant". The first frame is the honest
            # anchor -- a session constructed minutes before the stream started would
            # otherwise claim a reset that no counter was affected by.
            self._reset_timestamp = to_rfc3339z(resolved_ts)
            self._window.reset_timestamp = self._reset_timestamp

        stream = self._frame_stream(frame_id, stream_time, rtp_number)
        mapped, unmapped = self._intake(detections)
        buckets, unassigned, zone_of = self._partition(mapped)

        zone_outputs: dict[str, dict[str, PrimitiveOutput]] = {}
        events: list[PrimitiveEvent] = []
        for bucket, bucket_detections in buckets.items():
            outputs: dict[str, PrimitiveOutput] = {}
            pipeline = self._pipelines[bucket]
            # §6b coupling 5: rebound after a tracker stage, so the stages below it read ids
            # from det.track_id. Never the same objects as `buckets[bucket]`: the global
            # bucket and a zone bucket share detection objects (the partition copies only
            # what it stamps a zone onto), so an in-place write here would leak the global
            # tracker's ids into every zone pipeline that runs after it.
            staged: Sequence[PipelineDetection] = bucket_detections
            for stage_name in self._stage_order:
                primitive = pipeline.get(stage_name)
                if primitive is None:
                    # A `zones: all_in_one` stage, in a bucket that is not `global`. It was
                    # never built here (_build_pipeline), because it runs once for the whole
                    # frame rather than once per zone. Skipping it is what makes that true.
                    continue
                ctx = FrameContext(
                    detections=(
                        self._all_zones_view(staged, zone_of) if stage_name in self._all_in_one_stages else staged
                    ),
                    zone=bucket,
                    frame_ts=resolved_ts,
                    fps=stream.original_fps,
                    previous=outputs,
                    # §6b coupling 1: the standard channel. ctx.resolution,
                    # ctx.require_resolution, ctx.camera_id, ctx.frame_id and
                    # ctx.zone_config all read this, and there is no second one.
                    stream=stream,
                )
                output = primitive.process(ctx)
                outputs[stage_name] = output
                events.extend(output.events)
                if stage_name in self._track_stages and output.tracks:
                    staged = _stamp_track_ids(staged, output.tracks, bucket, stage_name)
            zone_outputs[bucket] = outputs

        # FrameOutcome.metric_values sums a `zone: per_zone` metric across every emitted zone
        # (see _frame_metric_values) rather than reading the global bucket's permanently-zero
        # reading of it; incident evaluation separately gets the full per-zone map so a
        # per-zone incident's human_text resolves from the one zone it actually fired in.
        metric_values = self._frame_metric_values(zone_outputs)
        incidents = self._evaluate_incidents(resolved_ts, stream, events, zone_outputs)

        # `stream=` so the window's S1 envelope carries this frame's media anchors. Without it
        # the aggregation publishes the anchor of the frame the session was built from, which
        # for a long-lived camera is hours stale.
        self._window.observe(resolved_ts, zone_outputs, buckets, stream=stream)
        frame_result = self._frame_result(buckets, zone_outputs) if self._manifest.emission.frame_summary else None
        aggregation = self._close_window() if self._window.is_due() else None

        return FrameOutcome(
            frame_ts=resolved_ts,
            zone_outputs={zone: dict(outputs) for zone, outputs in zone_outputs.items()},
            zone_detections=buckets,
            metric_values=metric_values,
            incidents=incidents,
            aggregation=aggregation,
            frame_result=frame_result,
            unassigned=unassigned,
            unmapped=unmapped,
        )

    def _frame_timestamp(self, frame_ts: float | None, stream_time: str | None) -> float:
        """The frame's own time, from the caller or from the media anchor (**PY-13**).

        Never ``time.time()``.  ``engine_session.py:595`` passes wall-clock into a
        frame-timestamped function, so replay, backfill and simulation aggregate on the host's
        clock and produce windows the live run never had.
        """
        if frame_ts is not None:
            value = float(frame_ts)
            if value != value:  # NaN
                raise SessionError("frame_ts is NaN; it must be the real frame time in epoch seconds")
            return value
        anchor = stream_time or self._stream.stream_time
        if anchor:
            try:
                return parse_stream_time(anchor).timestamp()
            except ValueError as exc:
                raise SessionError(
                    f"cannot derive a frame timestamp: stream_time {anchor!r} does not parse "
                    f"({exc}). Pass frame_ts= explicitly."
                ) from exc
        raise SessionError(
            "no frame timestamp: pass frame_ts=, or a stream_time media anchor in the "
            "'YYYY-MM-DD-HH:mm:ss.ffffff UTC' format (contract §3.3). There is deliberately no "
            "fallback to time.time(): that fallback is PY-13 and it makes every replayed or "
            "backfilled window wrong."
        )

    def _frame_stream(self, frame_id: str | None, stream_time: str | None, rtp_number: str | None) -> StreamInfo:
        """The stream context for this frame, with the media anchors refreshed.

        **All three** anchors, not two.  ``rtp_number`` sits in the same ``Media anchoring``
        block of :class:`StreamInfo` as the other two and is just as per-frame: it is the
        frame's raw 90 kHz RTP timestamp, and the backend resolves both the alert thumbnail
        (``frame_helper.go``, ``BuildImageData``) and the looked-up wall-clock time from it.
        Refreshing only ``frame_id``/``stream_time`` -- as this did -- pinned every incident
        and every aggregation on a camera to the anchor of the first frame its session ever
        saw, so every alert showed the same image.

        Copied rather than mutated: :class:`FrameContext` is frozen and hands the same object
        to every stage, so a stage that kept a reference must not see it change underneath.
        """
        updates: dict[str, Any] = {}
        if frame_id is not None and frame_id != self._stream.frame_id:
            updates["frame_id"] = frame_id
        if stream_time is not None and stream_time != self._stream.stream_time:
            updates["stream_time"] = stream_time
        if rtp_number is not None and rtp_number != self._stream.rtp_number:
            updates["rtp_number"] = rtp_number
        return self._stream.model_copy(update=updates) if updates else self._stream

    # -- intake and partition -----------------------------------------------

    def _intake(self, raw: Sequence[Any]) -> tuple[tuple[PipelineDetection, ...], int]:
        """Entity-remap and threshold this frame's detections.

        The floor is :meth:`_resolve_intake_floor`.  An unmapped label is **counted**, never
        silently dropped: it is the most common cause of an empty dashboard and today it
        produces no signal at all.

        **This method rebuilds :class:`PipelineDetection` field by field, so every field the
        pipeline's detection carries has to be listed here.**  A field that is not is dropped
        in silence, and the primitive that reads it publishes zeros with no error -- which is
        exactly the failure class this engine exists to remove.  ``mask`` and ``keypoints``
        are parsed by :func:`_to_mask` and :func:`_to_keypoints` and passed through below;
        the two other copy sites (:func:`_stamp_track_ids` and the zone stamp in
        ``primitives/geometry.py``) use ``model_copy``, which carries every field by
        construction and needs no maintenance.
        """
        kept: list[PipelineDetection] = []
        unmapped = 0
        for item in raw:
            detection = _to_detection(item)
            index = _class_index(item)
            if isinstance(detection, PipelineDetection) and detection.entity in self._entities:
                # The caller already remapped -- respect it rather than re-deriving the entity
                # from the model label, which a caller is entitled to have changed.
                entity = detection.entity
            else:
                entity = self._mapper.entity_for(detection.category, index) or ""
            if not entity:
                unmapped += 1
                continue
            if float(detection.confidence) < self._intake_floor:
                continue
            if isinstance(detection, PipelineDetection) and detection.entity == entity and detection.category:
                # The caller's remap is respected, but a bare class index is not a label
                # anyone can read, so it is still resolved.  ``model_copy`` carries every
                # field by construction, which is why this path does not fall through to the
                # field-by-field rebuild below even now that the rebuild carries ``zone``:
                # the next field added to ``PipelineDetection`` is free here and is one more
                # line to forget there.
                label = self._mapper.display_label(detection.category, index)
                kept.append(
                    detection if label == detection.category else detection.model_copy(update={"category": label})
                )
                continue
            mask, keypoints = self._detection_extras(item, detection)
            kept.append(
                PipelineDetection(
                    # A deployment that sends only a class index has no usable label on the
                    # detection, and ``category`` is the label the overlay draws -- so it is
                    # resolved through ``index_to_category``, falling back to the entity name
                    # rather than reaching the wire empty (contract §1 rule 7).  "Only an
                    # index" covers a category that is *absent* and one that is *numeric*;
                    # see :meth:`_EntityMapper.display_label` for why the second needs saying.
                    category=self._mapper.display_label(detection.category, index) or entity,
                    confidence=detection.confidence,
                    bounding_box=detection.bounding_box,
                    track_id=detection.track_id,
                    entity=entity,
                    # Engine-internal, and dropped again by to_wire(). Listed here because
                    # this branch reconstructs the detection: see the method docstring.
                    mask=mask,
                    keypoints=keypoints,
                    # `zone` was the field this rebuild forgot. A caller that hands in an
                    # already-zoned PipelineDetection whose entity does not match the resolved
                    # one misses the fast path above and lands here, and dropping the field
                    # reset that detection to the global bucket -- so it was counted, in the
                    # wrong series, with no error anywhere. Latent only because intake normally
                    # runs before zone partition and a raw producer dict has no `zone` key.
                    # The wire `Detection` has no such field, hence the isinstance test rather
                    # than a getattr default.
                    zone=detection.zone if isinstance(detection, PipelineDetection) else GLOBAL_ZONE,
                )
            )
        if unmapped:
            self._state.incr("unmapped_detections", unmapped, lifetime=Lifetime.PERSISTENT)
            if not self._unmapped_warned:
                self._unmapped_warned = True
                logger.warning(
                    "app %s: %d detection(s) on this frame carry a label that is in no "
                    "model.entity_mapping alias set, so they are counted by nothing. An "
                    "unmapped label is the most common cause of an empty dashboard: the "
                    "right-hand side of entity_mapping must match the model's labels "
                    "character for character. Mapped labels: %s.",
                    self._manifest.app.id,
                    unmapped,
                    ", ".join(self._mapper.labels) or "(none)",
                )
        return (tuple(kept), unmapped)

    def _detection_extras(self, item: Any, detection: Detection) -> tuple[MaskRef | None, tuple[Keypoint, ...]]:
        """This detection's mask and keypoints -- the two engine-internal input fields.

        Both are optional and both are dropped by :meth:`PipelineDetection.to_wire`, so adding
        them is additive on the wire.  A caller that hands in a
        :class:`~matrice_analytics.engine.primitives.base.PipelineDetection` has already
        parsed them and keeps its own; a raw producer dict is parsed here.

        Keypoints are normalized against the model input dimensions, which come from the
        detection's own ``keypoint_space``/``image_size``/``input_shape`` when it states one and
        from ``StreamInfo.resolution`` otherwise.  The stream's resolution is the *camera's*
        frame size, which equals the model input space only when inference runs at source
        resolution -- so it is used and **logged once**, rather than guessed silently, and a
        producer that sends normalized keypoints (the documented wire shape, contract ``04``
        §5.1) never reaches that path at all.
        """
        if isinstance(detection, PipelineDetection):
            return (detection.mask, detection.keypoints)
        if not isinstance(item, Mapping):
            return (None, ())
        mask = _to_mask(item)
        # The provider is passed, not called: a stream whose producer sends normalized
        # keypoints -- or none at all -- must not emit the assumption warning below.
        keypoints = _to_keypoints(item, self._keypoint_space)
        return (mask, keypoints)

    def _keypoint_space(self) -> tuple[int, int] | None:
        """``(width, height)`` to normalize pixel-space keypoints by, or ``None``.

        Warn-once, because it is an *assumption*: the keypoints' space is the model's input
        space and this is the camera's.  It is not the ``velocity_state`` 1920x1080 guess that
        was deleted -- the value is declared by the deployment rather than invented -- but a
        letterboxed 640x640 model on a 1920x1080 camera would still be scaled wrongly, and the
        fix is for the producer to send normalized keypoints or to state ``keypoint_space``.
        """
        resolution = self._stream.resolution
        width, height = (int(resolution[0]), int(resolution[1])) if resolution else (0, 0)
        if width <= 0 or height <= 0:
            return None
        if not self._keypoint_space_warned:
            self._keypoint_space_warned = True
            logger.warning(
                "app %s camera %s: keypoints arrived in pixel space and are being normalized "
                "by the stream resolution %dx%d. That is the camera's frame size, not "
                "necessarily the model's input size, so a model that infers at a different "
                "resolution will be scaled by the ratio of the two. Have the producer send "
                "keypoints normalized 0-1 (contract 04 §5.1, the same space as the bounding "
                "box), or a keypoint_space: [width, height] on the detection.",
                self._manifest.app.id,
                self._stream.camera_id,
                width,
                height,
            )
        return (width, height)

    def _partition(
        self, detections: Sequence[PipelineDetection]
    ) -> tuple[dict[str, tuple[PipelineDetection, ...]], int, tuple[str | None, ...]]:
        """Assign every detection to its bucket -- **once**, before any pipeline runs.

        Returns:
            ``({bucket: detections}, no_match_count, zone_of)``.  The ``global`` bucket holds
            the whole frame; a zoned app additionally gets one bucket per drawn zone and, under
            ``on_no_match: unassigned``, an ``unassigned`` bucket.  ``no_match_count`` is
            populated under **every** policy, including ``drop`` (**PY-10**).

            ``zone_of`` is the same information one entry per **input** detection, positionally
            aligned with *detections*: the bucket that detection landed in, or ``None`` when it
            matched nothing and ``on_no_match: drop`` threw it away.  It is empty for an
            unzoned app, which has nothing to say.  :meth:`_all_zones_view` is its only reader,
            and it exists so a ``zones: all_in_one`` stage can be handed the whole frame with
            each detection's real zone on it **without a second point-in-polygon pass** --
            "membership is decided once per frame" is the claim this module opens with.

        Note:
            ``stamp_zone=False``, and this method does the copying instead.  The stamp is a
            ``model_copy``, so a stamped detection is a new object and the mapping back to its
            input position is lost -- exactly what ``zone_of`` needs.  Asking geometry for the
            *unstamped* partition keeps object identity, which is what makes the alignment
            below exact rather than a guess based on comparing boxes.  Same number of copies as
            before: one per detection per bucket it landed in.
        """
        buckets: dict[str, tuple[PipelineDetection, ...]] = {GLOBAL_ZONE: tuple(detections)}
        if not self._zoned:
            return (buckets, 0, ())

        assignment: ZoneAssignment = assign_detections_to_zones(
            detections,
            # The polygons selected once at setup -- the same set the buckets were built from,
            # so the partition and the emission zones cannot disagree.
            self._polygons,
            self._geometry.resolution,
            reference_point=self._reference_point,  # type: ignore[arg-type]
            on_no_match=self._no_match_policy,  # type: ignore[arg-type]
            on_overlap=self._on_overlap,  # type: ignore[arg-type]
            # See the Note above: identity in, alignment out. The stamping the pipeline needs
            # -- a primitive reads ctx.zone, and a custom one may read det.zone -- happens
            # three lines below, over the same objects.
            stamp_zone=False,
        )
        position = {id(detection): index for index, detection in enumerate(detections)}
        zone_of: list[str | None] = [None] * len(detections)

        def stamp(found: Sequence[PipelineDetection], identity: str) -> tuple[PipelineDetection, ...]:
            for detection in found:
                index = position.get(id(detection))
                if index is not None and zone_of[index] is None:
                    # setdefault semantics: under on_overlap 'all_match' one detection is in
                    # several buckets, and the whole-frame view has room for it once. First
                    # match in drawing order, which is what 'first_match' would have chosen.
                    zone_of[index] = identity
            return tuple(detection.model_copy(update={"zone": identity}) for detection in found)

        for identity in self._zone_polygons:
            buckets[identity] = stamp(assignment.by_zone.get(identity, ()), identity)
        unassigned = stamp(assignment.unassigned, UNASSIGNED_ZONE)
        if UNASSIGNED_ZONE in self._emission_zones:
            buckets[UNASSIGNED_ZONE] = unassigned

        self._note_partition(assignment, len(detections))
        return (buckets, assignment.no_match_count, tuple(zone_of))

    def _note_partition(self, assignment: ZoneAssignment, total: int) -> None:
        """Accumulate where this frame's detections landed, for one line at the window boundary.

        The question an operator actually has when a zoned app publishes zeros is "are the
        detections landing outside the polygon?", and until now the only way to answer it was to
        infer it from the *absence* of numbers. Under ``on_no_match: drop`` even the
        ``unassigned`` series is gone, so there is nothing at all to infer from.

        Counted per frame, reported per window (``09`` §3: a number an operator can see beats a
        zero they cannot account for). WINDOW lifetime, so the boundary clears it.
        """
        if not self._zoned:
            return
        self._window_state.incr(_PARTITION_SEEN, float(total), lifetime=Lifetime.WINDOW)
        self._window_state.incr(_PARTITION_NO_MATCH, float(assignment.no_match_count), lifetime=Lifetime.WINDOW)
        self._window_state.incr(_PARTITION_ASSIGNED, float(assignment.assigned_count), lifetime=Lifetime.WINDOW)
        for identity, found in assignment.by_zone.items():
            self._window_state.incr(f"{_PARTITION_ZONE_PREFIX}{identity}", float(len(found)), lifetime=Lifetime.WINDOW)

    def _report_partition(self) -> None:
        """One line per window naming where the detections went, and a warning when most are lost.

        Escalates on the decelerating schedule ``dwell._note_global_bucket_skip`` already uses:
        a camera whose polygons genuinely cover a corner of the scene is not a defect, and must
        not fill the log for the life of the deployment -- but a camera losing most of its
        detections needs saying out loud, repeatedly, until somebody redraws the zone.
        """
        if not self._zoned:
            return
        seen = int(self._window_state.get(_PARTITION_SEEN, 0.0) or 0.0)
        if not seen:
            return
        no_match = int(self._window_state.get(_PARTITION_NO_MATCH, 0.0) or 0.0)
        assigned = int(self._window_state.get(_PARTITION_ASSIGNED, 0.0) or 0.0)
        per_zone = ", ".join(
            f"{identity}={int(self._window_state.get(f'{_PARTITION_ZONE_PREFIX}{identity}', 0.0) or 0.0)}"
            for identity in self._zone_polygons
        )
        logger.info(
            "app %s camera %s: %d detection(s) this window, %d in zones (%s), %d matched no "
            "polygon (%.0f%%, on_no_match: %s)",
            self._manifest.app.id,
            self._stream.camera_id,
            seen,
            assigned,
            per_zone or "none drawn",
            no_match,
            100.0 * no_match / seen,
            self._no_match_policy,
        )

        if no_match * 2 <= seen:
            self._window_state.set(_PARTITION_LOSS_STREAK, 0.0, lifetime=Lifetime.PERSISTENT)
            return
        streak = self._window_state.incr(_PARTITION_LOSS_STREAK, 1.0, lifetime=Lifetime.PERSISTENT)
        if streak in (1.0, 10.0) or streak % 100 == 0:
            logger.warning(
                "app %s camera %s: %.0f%% of detections have landed outside every drawn polygon "
                "for %d consecutive window(s). The geometry is probably not describing this "
                "camera's current view -- check that the polygons were drawn against this "
                "stream (resolved resolution %s) and not a different camera or a since-moved "
                "one. Every zone-scoped metric reads only the %d detection(s) that did match.",
                self._manifest.app.id,
                self._stream.camera_id,
                100.0 * no_match / seen,
                int(streak),
                self._geometry.resolution,
                assigned,
            )

    @staticmethod
    def _all_zones_view(
        detections: Sequence[PipelineDetection], zone_of: Sequence[str | None]
    ) -> tuple[PipelineDetection, ...]:
        """The whole frame for a ``zones: all_in_one`` stage, each detection carrying its zone.

        *detections* is the ``global`` bucket as the stage would otherwise have seen it --
        already entity-remapped and, if a ``track`` stage ran above, already carrying
        ``det.track_id``, because :func:`_stamp_track_ids` returns the same detections in the
        same order.  That positional identity is the join: ``zone_of[i]`` is where the
        partition put detection ``i``, so the view carries **both** the tracker's ids and the
        session's own zone assignment.  A cross-zone stage needs both -- a handoff is one
        *track* moving between two *zones* -- and neither bucket could offer both before.

        A detection the partition dropped (``on_no_match: drop``) is dropped here too: the app
        declared those detections out of scope, and resurrecting them in one stage's view would
        make that stage disagree with every count on the same frame.

        Returns:
            The stamped view, or *detections* unchanged when there is nothing to stamp -- an
            unzoned app, where the flag is a no-op because the whole frame is the only bucket.
        """
        if not zone_of:
            return tuple(detections)
        return tuple(
            detection if detection.zone == zone else detection.model_copy(update={"zone": zone})
            for detection, zone in zip(detections, zone_of, strict=True)
            if zone is not None
        )

    # -- metrics, incidents, frame result -----------------------------------

    def _metric_values(self, zone_outputs: Mapping[str, Mapping[str, PrimitiveOutput]], zone: str) -> dict[str, float]:
        """This frame's reading of every declared metric, for incidents raised in ``zone``.

        A ``metrics[].zone: per_zone`` entry reads *this* ``zone``'s own stage outputs; a
        ``zone: global`` entry always reads the ``global`` bucket's, regardless of which zone
        is asking -- the same split :func:`~.window._build_metrics` already applies when it
        resolves the same declaration for the published aggregation. Getting this wrong is
        why an ``incident_quantise``-driven incident's ``human_text`` used to always read a
        per-zone placeholder (e.g. ``{active_people_at_risk}``) as ``0``: ``dwell.state:
        in_zone`` publishes nothing in the ``global`` bucket by design (see
        ``dwell.py::_state_verdict``), so a metric sourced from it is genuinely present there
        -- just permanently zero -- which is indistinguishable from the real answer being
        zero until the value is read from the zone the incident actually fired in.

        A metric whose source did not resolve is **absent**, not zero: ``09`` §3 -- a metric
        that reads zero forever is indistinguishable from a quiet camera, and it is what an
        unresolvable source produces today.
        """
        values: dict[str, float] = {}
        for planned in self._metric_plan:
            source_zone = zone if planned.spec.zone in _ZONED_METRIC_SCOPES else GLOBAL_ZONE
            outputs = zone_outputs.get(source_zone)
            if outputs is None:
                continue
            output = outputs.get(planned.stage)
            if output is None:
                continue
            raw = output.values.get(planned.value)
            if isinstance(raw, bool):
                values[planned.spec.key] = float(int(raw))
            elif isinstance(raw, (int, float)):
                values[planned.spec.key] = float(raw)
        return values

    def _derived_frame_values(
        self, zone_outputs: Mapping[str, Mapping[str, PrimitiveOutput]], zone: str
    ) -> dict[str, float]:
        """This frame's live reading of every ``derived[]`` entry, for ``zone``.

        ``Session._metric_plan`` only ever resolved ``manifest.metrics`` -- ``derived[]`` was
        evaluated exclusively at the aggregation boundary (:meth:`AggregationWindow.build`),
        so a metric declared under ``derived:`` was absent from ``FrameOutcome.metric_values``
        and from an incident's ``human_text`` on **every** frame, regardless of its declared
        ``scope``. This closes that gap by evaluating the same expression
        (:class:`~matrice_analytics.engine.manifest.expr.DerivedExpression`, the identical
        safe-arithmetic evaluator ``window.py`` uses -- nothing here re-parses ``expr``)
        against each operand's live per-frame reading.

        Because a source primitive with its own running accumulators (``zone_occupancy``,
        ``unique_count``) now publishes "the peak/mean/total so far" per frame rather than
        omitting the key until the window closes, a ``scope: window`` derived entry reads as
        "the expression evaluated against the running values so far" here -- a live,
        monotonically-settling approximation of the number :meth:`AggregationWindow.build`
        publishes at the boundary, which remains the source of truth and is untouched by this
        method. A ``scope: frame`` entry reads exactly what it would if this frame were the
        only one retained -- the same per-frame evaluation :meth:`AggregationWindow` already
        does before collapsing many of them with ``agg_type``.

        An operand that does not resolve leaves the metric **absent**, not zero, matching
        :meth:`_metric_values`'s own contract (``09`` §3).
        """
        values: dict[str, float] = {}
        for planned in self._derived_plan:
            source_zone = zone if planned.spec.zone in _ZONED_METRIC_SCOPES else GLOBAL_ZONE
            operands: dict[str, float] = {}
            resolved = True
            for operand in planned.operands:
                operand_zone = GLOBAL_ZONE if operand.from_global else source_zone
                outputs = zone_outputs.get(operand_zone)
                output = outputs.get(operand.stage) if outputs is not None else None
                raw = output.values.get(operand.value) if output is not None else None
                number = _number(raw)
                if number is None:
                    resolved = False
                    break
                operands[operand.source] = number
            if not resolved:
                continue
            try:
                result = planned.expression.evaluate(operands)
            except EvaluationError:
                # Same treatment as a metric skip: a gap in the series is diagnosable, and
                # this frame's already-logged-elsewhere primitive outputs are the diagnostic.
                continue
            # Undefined this frame (a zero denominator) is a quiet reading, not a fault --
            # same rule _derived_value applies at the boundary.
            values[planned.spec.key] = 0.0 if result is None else result
        return values

    def _resolved_values(
        self, zone_outputs: Mapping[str, Mapping[str, PrimitiveOutput]], zone: str
    ) -> dict[str, float]:
        """Every declared ``metrics[]`` and ``derived[]`` reading for ``zone``, this frame.

        ``metrics[]`` first, then ``derived[]`` -- the same order
        :meth:`AggregationWindow._build_metrics` uses for the published aggregation, so a
        payload reads the way the manifest does either way. The two key-spaces do not
        collide in practice: ``AppManifest`` validation rejects a ``derived[].key`` that
        repeats a ``metrics[].key``.
        """
        values = self._metric_values(zone_outputs, zone)
        values.update(self._derived_frame_values(zone_outputs, zone))
        return values

    def _frame_metric_values(self, zone_outputs: Mapping[str, Mapping[str, PrimitiveOutput]]) -> dict[str, float]:
        """:attr:`FrameOutcome.metric_values` -- one flat reading per declared metric.

        ``result["metrics"]`` (``runtime/backends.py::_outcome_as_result``) publishes this
        dict verbatim to callers outside this workspace, so it has no zone dimension to give
        a ``zone: per_zone`` metric on a multi-zone camera -- unlike an incident's
        ``human_text``, which is scoped to the one zone that raised it (see
        :meth:`_advance`), there is no single zone this flat map could pick without being
        arbitrarily wrong about the others. Collapsing across the zones answers a different,
        but always-defined, question -- "how much, anywhere on this camera" -- and beats the
        alternative this replaced: reading the ``global`` bucket's permanently resolved ``0``
        for a ``state: in_zone``-gated metric, which reports "nobody, ever" for an app that may
        be actively raising incidents in three zones at once.

        **How** they collapse is each metric's own ``across_zones`` (default ``sum``), not one
        rule for all of them: a count sums, a ``max_*`` takes the maximum and an average or a
        percentage takes the mean.  Summing is right for the first and nonsense for the other
        two -- two zones each averaging 1.8 seconds are not 3.6 seconds of anything.

        The ``unassigned`` bucket is **excluded**.  It is an emission zone, so ``results-agg``
        publishes its own labelled row for it and the **PY-10** diagnostic is untouched -- but
        it is by definition *not* a zone, and folding it in here would answer a third question
        again: ``unique_zone_entrants`` would count people who never entered a zone, and no
        caller reading a key with "zone" in its name wants that.  ``dwell`` already excludes it
        by construction (``dwell.py``, ``_measures_nothing``); ``unique_count`` does not, which
        is why this has to be stated rather than assumed.

        A ``zone: global`` metric is unaffected -- it already has exactly one zone.

        ``derived[]`` entries (resolved by :meth:`_derived_frame_values`, via
        :meth:`_resolved_values`) collapse under the exact same rule, keyed by their own
        ``zone``/``across_zones`` -- a ``derived: {zone: per_zone}`` entry (e.g. a per-zone
        percentage) is exactly as ambiguous on this flat map as a ``metrics[]`` one, and
        answering "how much, anywhere on this camera" is the same right answer for both.
        """
        per_zone: dict[str, AcrossZonesLiteral] = {
            planned.spec.key: planned.spec.across_zones
            for planned in self._metric_plan
            if planned.spec.zone in _ZONED_METRIC_SCOPES
        }
        per_zone.update(
            {
                planned.spec.key: planned.spec.across_zones
                for planned in self._derived_plan
                if planned.spec.zone in _ZONED_METRIC_SCOPES
            }
        )
        if not per_zone:
            # The overwhelmingly common case (an unzoned app declares none): one lookup,
            # identical to the pre-collapsing behaviour.
            return self._resolved_values(zone_outputs, GLOBAL_ZONE)

        # The global-scoped entries first -- _resolved_values(zone_outputs, GLOBAL_ZONE) resolves
        # only those against the global bucket (a per_zone key it would also compute here is
        # itself a global-bucket reading, not the collapse, so it is excluded rather than kept
        # and then overwritten below).
        values: dict[str, float] = {
            key: value for key, value in self._resolved_values(zone_outputs, GLOBAL_ZONE).items() if key not in per_zone
        }
        readings: dict[str, list[float]] = {key: [] for key in per_zone}
        for zone in self._emission_zones:
            if zone == UNASSIGNED_ZONE:
                continue
            for key, value in self._resolved_values(zone_outputs, zone).items():
                if key in readings:
                    readings[key].append(value)
        for key, samples in readings.items():
            # No zone resolved it -> absent, not 0 (``09`` §3), exactly as before.
            if samples:
                values[key] = _collapse_zones(samples, per_zone[key])
        return values

    def _evaluate_incidents(
        self,
        frame_ts: float,
        stream: StreamInfo,
        events: Sequence[PrimitiveEvent],
        zone_outputs: Mapping[str, Mapping[str, PrimitiveOutput]],
    ) -> tuple[IncidentMessage, ...]:
        """Run the incident lifecycle and emit on **transitions** only (contract §3.4).

        The backend does find-or-create with **up-only escalation**: re-sending the same
        severity is a no-op, a de-escalation is not representable, and only a non-empty
        ``end_time`` closes an incident.  Emitting per frame would therefore be 1,500 writes a
        minute that mean nothing.

        Takes the frame's full ``zone_outputs`` rather than one precomputed ``metric_values``
        dict: a threshold rule is evaluated in the ``global`` bucket only (see
        :meth:`_active_for`), but an event-driven rule (``incident_quantise``) fires **per
        zone**, and its ``human_text`` may interpolate a ``zone: per_zone`` metric -- which
        only has a real reading in the zone the incident fired in, not in ``global``.
        :meth:`_advance` resolves the right one per ``(rule, zone)`` pair.
        """
        if not self._rules or self._manifest.incidents is None:
            return ()
        lifecycle = self._manifest.incidents.lifecycle
        if lifecycle.emit_on == "never":
            return ()

        messages: list[IncidentMessage] = []
        for rule in self._rules:
            active = self._active_for(rule, events, zone_outputs)
            for incident in self._close_orphans(rule, active, frame_ts):
                messages.append(build_incident(stream, incidents=[incident], category=rule.spec.category))
            for zone, severity in active.items():
                incident = self._advance(rule, zone, severity, frame_ts, lifecycle, zone_outputs)
                if incident is not None:
                    messages.append(build_incident(stream, incidents=[incident], category=rule.spec.category))
        published = tuple(messages)
        if self._publisher is not None:
            for message in published:
                publish_incident(self._publisher, message)
        return published

    def _active_for(
        self,
        rule: _IncidentRule,
        events: Sequence[PrimitiveEvent],
        zone_outputs: Mapping[str, Mapping[str, PrimitiveOutput]],
    ) -> dict[str, str]:
        """``{zone: severity}`` for this rule this frame -- ``""`` severity means inactive.

        Every bucket the rule *could* fire in is present in the result, so an absent event is
        a decay tick rather than a frozen counter.
        """
        if rule.is_event_driven:
            # §6b coupling 3: match on the STAGE NAME the event carries, never on the
            # incident key. IncidentQuantiseConfig has no incident key to match against.
            #
            # Only the emission zones are tracked. A zoned app runs the same quantiser in the
            # 'global' bucket *and* in each zone, so tracking both would open two incidents for
            # one fire -- and the wire has no zone field to tell them apart (Incident carries
            # none), so an operator would see the same alert twice.
            active: dict[str, str] = {zone: "" for zone in self._emission_zones}
            for event in events:
                if event.kind != rule.stage or event.zone not in active:
                    continue
                zone = event.zone
                current = active.get(zone) or ""
                candidate = event.severity or DEFAULT_THRESHOLD_SEVERITY
                if not current or _rank(candidate) > _rank(current):
                    active[zone] = candidate
            return active

        # A metric-threshold rule is evaluated in the zones its own metrics are defined in.
        #
        # This used to be GLOBAL_ZONE unconditionally, on the reasoning that `Incident` carries
        # no zone field so a per-zone threshold has nothing to disambiguate it. That constraint
        # is real but self-imposed: the event-driven branch above *already* opens one incident
        # per emission zone on the same wire, and four shipped apps depend on it. `_incident_id`
        # hashes the zone (uuid5 over camera/app/type/zone/start_time), so the backend's
        # find-or-create keeps concurrent zone incidents distinct with no schema change.
        #
        # What it cost: a threshold over a `zone: per_zone` metric read the GLOBAL bucket, where
        # a `state: in_zone` dwell measures nothing -- so the rule could never fire on a zoned
        # camera, and a missing alert is indistinguishable from a quiet site.
        #
        # Opt-in by data: a rule whose threshold metrics are all `zone: global` still resolves
        # to exactly one lifecycle keyed `global`, byte for byte as before.
        #
        # `_resolved_values`, not `_metric_values`: `derived[]` is now evaluated per frame
        # (`_derived_frame_values`), so a derived key is a legal threshold source.
        active = {}
        for zone in self._threshold_zones(rule):
            metric_values = self._resolved_values(zone_outputs, zone)
            severity = ""
            for metric_key, threshold in rule.thresholds.items():
                value = metric_values.get(metric_key)
                if value is None or not _threshold_matches(threshold, value):
                    continue
                candidate = _graded_severity(threshold, value)
                if not severity or _rank(candidate) > _rank(severity):
                    severity = candidate
            active[zone] = severity
        return active

    def _threshold_zones(self, rule: _IncidentRule) -> tuple[str, ...]:
        """The buckets a metric-threshold rule is evaluated in.

        The emission zones when any of the rule's own threshold metrics is zone-scoped -- that
        metric's real reading only exists in a zone, so evaluating it in ``global`` asks a
        question the bucket cannot answer. ``(global,)`` otherwise, which is every app that has
        not opted in.
        """
        if not self._zoned:
            return (GLOBAL_ZONE,)
        zoned_keys = {planned.spec.key for planned in self._metric_plan if planned.spec.zone in _ZONED_METRIC_SCOPES}
        zoned_keys |= {planned.spec.key for planned in self._derived_plan if planned.spec.zone in _ZONED_METRIC_SCOPES}
        if any(key in zoned_keys for key in rule.thresholds):
            return self._emission_zones
        return (GLOBAL_ZONE,)

    def _close_orphans(self, rule: _IncidentRule, active: Mapping[str, str], frame_ts: float) -> list[Incident]:
        """Close any incident left open in a zone this rule no longer evaluates.

        Lifecycle records are keyed ``f"{rule.key}|{zone}"`` and are ``Lifetime.PERSISTENT`` --
        they survive a restart, deliberately, so an incident that was open when a container
        bounced is not re-raised as new. That makes a *change* in the zone set dangerous: a rule
        that moves from ``global``-only to per-zone (because a manifest retargeted a metric, or
        because a camera had its first polygon drawn) leaves a ``rule|global`` record with
        ``open: True`` that no later frame will ever visit again. Nothing decrements it, nothing
        closes it, and the operator sees an alert that never goes away and cannot be cleared.

        So: remember which zones this rule evaluated last, and when the set changes, close every
        record the new set abandoned -- with a real ``end_time``, which is the only thing the
        backend treats as a close.
        """
        remembered = self._incident_state.get(f"{rule.key}|__zones__")
        previous = tuple(str(zone) for zone in remembered) if isinstance(remembered, (list, tuple)) else ()
        current = tuple(active)
        if previous == current:
            return []
        self._incident_state.set(f"{rule.key}|__zones__", list(current), lifetime=Lifetime.PERSISTENT)

        closed: list[Incident] = []
        for zone in previous:
            if zone in active:
                continue
            key = f"{rule.key}|{zone}"
            record = self._incident_state.get(key)
            if not isinstance(record, dict) or not record.get("open"):
                continue
            logger.info(
                "app %s camera %s: incident %r was open in zone %r, which this rule no longer "
                "evaluates (zones changed from %s to %s); closing it rather than leaving an "
                "alert nobody can clear",
                self._manifest.app.id,
                self._stream.camera_id,
                rule.key,
                zone,
                list(previous),
                list(current),
            )
            closed.append(self._incident(rule, record, end_time=to_rfc3339z(frame_ts)))
            record["open"] = False
            self._incident_state.set(key, record, lifetime=Lifetime.PERSISTENT)
        return closed

    def _advance(
        self,
        rule: _IncidentRule,
        zone: str,
        severity: str,
        frame_ts: float,
        lifecycle: IncidentLifecycle,
        zone_outputs: Mapping[str, Mapping[str, PrimitiveOutput]],
    ) -> Incident | None:
        """Advance one ``(type, zone)`` lifecycle by one frame; return what to emit.

        Confirmation uses **soft decay**, matching the ``state_machine`` primitive and
        ``base_processor.py:258-292``: an inactive frame decrements the streak by one rather
        than resetting it, so a detector that drops one frame in five still confirms.  A hard
        reset makes ``confirm_frames`` unreachable on any real camera, which is how a
        confirmation threshold ends up quietly lowered to 1.
        """
        # Resolved for *this* zone, not the frame's global-only reading: a per_zone metric
        # (e.g. dwell.active_count under state: in_zone) is only ever real here, in the zone
        # the incident fired in -- the global bucket publishes it as a permanent, resolved 0.
        # `_resolved_values` (not bare `_metric_values`) so a `human_text` placeholder can also
        # name a `derived[]` key -- e.g. `{peak_occupancy}` used to be permanently unresolved
        # here regardless of zone, since `zone_occupancy.peak_occupancy` was a `.window()`-only
        # reading; it is now live per frame (see `zone_occupancy.process`), and any genuine
        # `derived:` placeholder resolves the same way for the first time.
        metric_values = self._resolved_values(zone_outputs, zone)
        state = self._incident_state
        key = f"{rule.key}|{zone}"
        record: dict[str, Any] = dict(state.get(key, {}) or {})
        streak = int(record.get("streak", 0))
        empty = int(record.get("empty", 0))
        is_open = bool(record.get("open", False))
        emitted: Incident | None = None

        if severity:
            streak = min(_MAX_STREAK, streak + 1)
            empty = 0
            if not is_open and streak >= lifecycle.confirm_frames:
                record["start_time"] = to_rfc3339z(frame_ts)
                record["id"] = self._incident_id(rule, zone, str(record["start_time"]))
                record["severity"] = severity
                record["human_text"] = _interpolate(rule.spec.human_text, metric_values)
                is_open = True
                emitted = self._incident(rule, record, end_time="")
            elif is_open and _rank(severity) > _rank(str(record.get("severity", ""))):
                # Up-only escalation (contract §3.4): the backend ignores a downward change,
                # so a de-escalation is not emitted -- it is not representable.
                record["severity"] = severity
                record["human_text"] = _interpolate(rule.spec.human_text, metric_values)
                emitted = self._incident(rule, record, end_time="")
        else:
            streak = max(0, streak - 1)
            if is_open:
                empty += 1
                if empty >= lifecycle.close_after_empty_frames:
                    # The snapshot from the open/escalate frame, NOT this frame's readings. A
                    # close fires only after `close_after_empty_frames` frames with nothing in
                    # them, so re-interpolating here describes the empty frame that closed the
                    # incident rather than the incident itself: every placeholder resolves to
                    # the primitive's empty-frame value and a fire alert closes reading
                    # "severity rank 0, 0 of frame" beside a severity_level of "low". The text
                    # and the payload have to agree.
                    emitted = self._incident(rule, record, end_time=to_rfc3339z(frame_ts))
                    is_open = False
                    streak = 0
                    empty = 0

        record.update({"streak": streak, "empty": empty, "open": is_open})
        # PERSISTENT: an open incident outlives the aggregation window it started in. Writing
        # this WINDOW-scoped would close and reopen every incident once a minute, and the
        # backend's find-or-create would then show one alert per minute (09 §4 rule 2).
        state.set(key, record, lifetime=Lifetime.PERSISTENT)
        return emitted

    def _incident_id(self, rule: _IncidentRule, zone: str, start_time: str) -> str:
        """A stable id for one occurrence of one incident type in one zone.

        The backend does **find-or-create on ``incident_id``** (contract §3.2), so the id has to
        be identical every time this occurrence is mentioned and different for the next one.
        A UUID5 over ``camera/app/type/zone/start_time`` gives both, and gives them
        *deterministically*: the same frames produce the same id in every process, which is what
        makes a payload diffable against a golden file and a replay comparable to the live run.

        The contract's wording says UUID4.  A v4 would satisfy find-or-create equally while
        making every generated determinism assertion (objective **O5**) impossible, and a random
        id is exactly the class of thing **PY-9** is about -- so this is v5 over a stable string.
        It is still a UUID string on the wire; reverting is one line.
        """
        return str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"matrice-incident/{self._stream.camera_id}/{self._manifest.app.id}/{rule.key}/{zone}/{start_time}",
            )
        )

    def _incident(
        self,
        rule: _IncidentRule,
        record: Mapping[str, Any],
        *,
        end_time: str,
    ) -> Incident:
        """Build one ``incidents[]`` entry from a lifecycle record.

        ``human_text`` comes off the record rather than being interpolated here: it is written
        on the frame that opened or escalated the incident, which is the only frame whose
        readings describe it (see :meth:`_advance`).  The fallback re-interpolates against an
        empty mapping, leaving every placeholder literal -- that is reachable only for a record
        written by a build predating the snapshot, since incident state is
        :attr:`Lifetime.PERSISTENT` and survives a restart.  A visible ``{placeholder}`` is the
        right failure there: it says "this text was not resolved", where a silently
        re-interpolated zero would read as a measurement.
        """
        return Incident(
            incident_id=str(record["id"]),
            incident_type=rule.key,
            # parse_severity maps the internal 'significant' onto 'high' (FROZEN-7); it must
            # never reach the wire, and a primitive is free to say it.
            severity_level=parse_severity(record.get("severity") or DEFAULT_THRESHOLD_SEVERITY),
            human_text=str(record.get("human_text") or _interpolate(rule.spec.human_text, {})),
            start_time=str(record["start_time"]),
            end_time=end_time,
        )

    def _wire_detections_for(
        self,
        zone: str,
        zone_outputs: Mapping[str, Mapping[str, PrimitiveOutput]],
    ) -> Sequence[PipelineDetection] | None:
        """A stage's override for this zone's wire detections, or ``None`` for none.

        Scans in pipeline order (dict iteration order, which ``zone_outputs`` preserves from
        insertion); the last stage that sets :attr:`PrimitiveOutput.wire_detections` wins, with
        a warning if more than one did -- an app declaring two such stages has not decided
        what "the detections" means and silently picking the first would hide that.
        """
        override: Sequence[PipelineDetection] | None = None
        setters: list[str] = []
        for stage, output in zone_outputs.get(zone, {}).items():
            if output.wire_detections is not None:
                override = output.wire_detections
                setters.append(stage)
        if len(setters) > 1:
            logger.warning(
                "zone %r: %d stages set wire_detections this frame (%s) -- using the last "
                "one (%s). An app should have exactly one stage overriding the wire's "
                "detections list.",
                zone,
                len(setters),
                ", ".join(setters),
                setters[-1],
            )
        return override

    def _frame_result(
        self,
        buckets: Mapping[str, Sequence[PipelineDetection]],
        zone_outputs: Mapping[str, Mapping[str, PrimitiveOutput]],
    ) -> FrameResult:
        """Build the per-frame return value (surface S3).

        Two corrections over today's frame path:

        * ``agg_summary`` is keyed by **zone**, consistently (**PY-5**).  Today the key is
          ``"<int>"``, ``"None"``, ``"current_frame"`` or a zone name depending on which file
          built it, and three consumers break on multi-zone payloads.  This is a **visible
          behaviour change for three consumers** and ships announced, not slipped in.
        * every zone's ``tracking_stats`` carries **all four count lists** (**PY-2**).  Today
          it carries only ``human_text`` and ``detections``
          (``analytics/schemas.py:280-289``), so be-analytics' ``hasTrackingStats`` fails on
          all seven probe paths and *every instant metric evaluates against zero*.
        """
        summary: dict[str, FrameSummaryEntry] = {}
        for zone in self._emission_zones:
            # The same counters the window surface publishes, already folded by
            # AggregationWindow.observe() on this frame -- one set of numbers, two surfaces.
            counters = self._window.counters_for(zone)
            wire_detections = self._wire_detections_for(zone, zone_outputs)
            source = wire_detections if wire_detections is not None else buckets.get(zone, ())
            summary[zone] = FrameSummaryEntry(
                tracking_stats=FrameTrackingStats(
                    input_timestamp=to_rfc3339z(self._window.last_ts),
                    reset_timestamp=self._reset_timestamp,
                    detections=[det.to_wire() for det in source],
                    human_text=human_text_for(counters.current),
                    **counters.count_lists(),
                ),
                business_analytics={stage: dict(output.values) for stage, output in zone_outputs.get(zone, {}).items()},
            )
        return build_frame_result(agg_summary=summary, original_fps=self._stream.original_fps)

    # -- the window boundary ------------------------------------------------

    def _close_window(self) -> AggregationResult | None:
        """Aggregate, publish, then clear WINDOW state -- in that order.

        ``primitive.window(frames)`` is called before anything is reset, because several
        primitives read their per-frame outputs there (``dwell``, ``velocity_state``,
        ``state_machine``, ``incident_quantise``) and the rest read WINDOW-lifetime state that
        the boundary is about to delete.
        """
        window_outputs: dict[str, dict[str, WindowOutput]] = {}
        for bucket, pipeline in self._pipelines.items():
            collected: dict[str, WindowOutput] = {}
            for stage_name, primitive in pipeline.items():
                collected[stage_name] = primitive.window(self._window.frames_for(bucket, stage_name))
            window_outputs[bucket] = collected

        result = self._window.build(window_outputs)
        if result is not None and self._publisher is not None:
            publish_aggregation(self._publisher, result)

        # Before the WINDOW state is cleared below -- these counters live in it.
        self._report_partition()

        for pipeline in self._pipelines.values():
            for primitive in pipeline.values():
                primitive.reset()
        self._window.rollover()
        return result

    def flush(self) -> AggregationResult | None:
        """Close a partial window at the end of a stream.

        Returns:
            The ``results-agg`` message for the frames observed since the last boundary, or
            ``None`` when no frame has arrived since (or when the window is empty and
            ``emit_empty_windows`` is false).
        """
        if not self._window.is_open:
            return None
        return self._close_window()


# ---------------------------------------------------------------------------
# Construction, intake and threshold helpers
# ---------------------------------------------------------------------------


#: Where this window's detections landed, for the one line `_report_partition` emits.
#:
#: WINDOW lifetime, so the boundary clears them -- except the loss streak, which is the thing
#: that has to survive a boundary to know it is a streak.
_PARTITION_SEEN: Final[str] = "partition_seen"
_PARTITION_NO_MATCH: Final[str] = "partition_no_match"
_PARTITION_ASSIGNED: Final[str] = "partition_assigned"
_PARTITION_ZONE_PREFIX: Final[str] = "partition_zone."
_PARTITION_LOSS_STREAK: Final[str] = "partition_loss_streak"

#: Metric scopes whose reading comes from a *zone* bucket rather than the whole-frame one.
#:
#: ``per_zone`` and ``collapsed`` differ only in what reaches ``results-agg`` -- N labelled rows
#: versus one reduced row (``window._build_metrics``). Per frame there is one number either way,
#: and it is the same number, so both resolve out of the zone and reduce by ``across_zones``.
_ZONED_METRIC_SCOPES: Final[frozenset[str]] = frozenset({"per_zone", "collapsed"})


def _collapse_zones(samples: Sequence[float], how: AcrossZonesLiteral) -> float:
    """The across-zones reduction, which now lives in ``window`` because both surfaces use it.

    Kept as a name here so the call sites in this module read unchanged. The implementation
    moved when ``zone: collapsed`` made ``results-agg`` need the same reduction the flat
    per-frame map applies -- a key that collapsed one way per frame and another per window
    would be worse than either.
    """
    return collapse_zones(samples, how)


def _construct(
    impl: type[Primitive],
    config: PrimitiveConfig,
    state: StateStore,
    *,
    geometry: SceneGeometry,
    on_overlap: str,
    zoned: bool = False,
    bucket: str = GLOBAL_ZONE,
) -> Primitive:
    """Instantiate a primitive, supplying the keyword arguments it declares.

    Three primitives need something the four-argument protocol does not carry, and each takes
    it as a keyword-only argument with a default:

    ``geometry=``
        the camera's :class:`SceneGeometry`, resolved to pixels **once** at session setup
        (**PY-7**).  Building it per frame per zone would be 100 constructions a second and
        would move every setup error into the hot path.

    ``on_overlap=``
        **§6b coupling 2.**  ``on_overlap`` lives on ``ZonesSpec`` -- the top-level ``zones:``
        block -- not on ``ZoneOccupancyConfig``, because it is a property of the camera's
        geometry rather than of one stage.  A runtime that forgets to pass it gets
        ``first_match`` silently, which is the undefined insertion-order behaviour **PY-10** is
        about.

    ``zoned=``
        whether this app runs **per zone**.  ``dwell.state: in_zone`` is the only consumer:
        a zoned app always runs the ``global`` bucket too, and that bucket has to be skipped
        there rather than treated as a misconfiguration -- but a *single-bucket* app with
        ``state: in_zone`` really is one, and the two look identical from inside a
        ``FrameContext`` (``ctx.zone == "global"`` in both).  Only the session knows.

    ``bucket=``
        which bucket this instance was built for.  ``dwell`` is again the only consumer, and
        again it is something the stage cannot recover for itself: ``window()`` takes no
        ``FrameContext``, so at window scope -- where the published metric rows are built --
        it has no other way to know it is the ``unassigned`` instance, the one bucket where
        ``state: in_zone`` can never open a session and must publish nothing rather than a
        resolved ``0``.

    The signature is *inspected* rather than the classes being named here, so a new geometry
    primitive is wired by declaring the keyword and nothing else.  A registry-wide
    ``create(name, config, state)`` cannot do this, which is why this function exists.
    """
    if not isinstance(config, impl.Config):
        raise SessionError(
            f"primitive {impl.__name__} expects a {impl.Config.__name__}, got "
            f"{type(config).__name__}; the stage was built from the wrong pipeline entry."
        )
    try:
        parameters = inspect.signature(impl.__init__).parameters
    except (TypeError, ValueError):  # pragma: no cover - C-level __init__
        parameters = {}  # type: ignore[assignment]
    extra: dict[str, Any] = {}
    if "geometry" in parameters:
        extra["geometry"] = geometry
    if "on_overlap" in parameters:
        extra["on_overlap"] = on_overlap
    if "zoned" in parameters:
        extra["zoned"] = zoned
    if "bucket" in parameters:
        extra["bucket"] = bucket
    return impl(config, state, **extra)  # type: ignore[call-arg]


class _CustomStage:
    """Adapter making a :class:`CustomPrimitive` look like a full :class:`Primitive`.

    ``09`` §6: a custom stage declares ``Config`` and ``process`` and nothing else.  It has no
    ``window()`` on purpose -- *the runtime* aggregates the ``values`` it publishes, using each
    metric's ``agg_type`` over the per-frame samples
    (:func:`~matrice_analytics.engine.runtime.window.collapse`).  Returning an empty
    :class:`WindowOutput` here is what routes it down that path, and it is the one case where
    ``agg_type`` is applied by this engine at all (§6b coupling 4).

    ``reset`` is optional and is forwarded when present.
    """

    __slots__ = ("_impl", "_name", "_state")

    def __init__(self, name: str, impl: type[Any], config: BaseModel, state: StateStore) -> None:
        self._name = name
        self._state = state
        self._impl = impl(config, state)

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        output = self._impl.process(ctx)
        if not isinstance(output, PrimitiveOutput):
            raise SessionError(
                f"custom stage {self._name!r} returned {type(output).__name__} from process(); "
                "it must return a PrimitiveOutput (09 §6)."
            )
        return output

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        del frames
        return WindowOutput()

    def reset(self) -> None:
        reset = getattr(self._impl, "reset", None)
        if callable(reset):
            reset()
        else:
            self._state.end_window()

    def __repr__(self) -> str:
        return f"_CustomStage({self._name!r}, {type(self._impl).__name__})"


#: The :class:`TrackState` attribute that joins a track back to the detection it came from.
#: ``track.py`` publishes it on every emitted track and documents it as *the* way "a later
#: stage can reach the detection's box"; this is the other half of that sentence.
_DET_INDEX: Final[str] = "det_index"


def _stamp_track_ids(
    detections: Sequence[PipelineDetection],
    tracks: Mapping[int, Any],
    bucket: str,
    stage_name: str,
) -> tuple[PipelineDetection, ...]:
    """Fill in ``track_id`` on the detections the stages below a tracker will see.

    The join is ``TrackState.attributes["det_index"]`` -> position in the detection sequence,
    which is the join ``track.py`` designed and documented and which nothing was using.
    Filling the field is not "mutating a primitive's input": ``PipelineDetection`` is the
    *pipeline's* detection and ``track_id`` is a field it declares, exactly like the ``entity``
    and ``zone`` this module already fills in.  What would be mutation is writing to the
    objects an earlier stage was handed, which is why every stamped detection is a copy and
    the caller rebinds rather than assigning into a tuple.

    Args:
        detections: This bucket's detections as the tracker stage saw them -- ``det_index``
            indexes *this* sequence.
        tracks: The tracker stage's :attr:`PrimitiveOutput.tracks`.
        bucket: The zone bucket, for the log line.
        stage_name: The tracker stage, for the log line.

    Returns:
        The same detections, with ``track_id`` set wherever the tracker claimed one.  A
        detection the tracker did not associate keeps ``track_id=None`` and is therefore still
        counted as ``untracked`` by ``line_crossing`` -- an unassociated detection is
        genuinely uncountable and must not be given a borrowed id.
    """
    by_index: dict[int, int] = {}
    for track_id in sorted(tracks):  # sorted: first-wins is deterministic (O5)
        index = tracks[track_id].attributes.get(_DET_INDEX)
        if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < len(detections):
            continue
        by_index.setdefault(index, int(track_id))
    if not by_index:
        # A tracker that emitted tracks none of which points at a detection cannot be joined,
        # and the stages below are about to raise. Say which stage broke the join first.
        logger.warning(
            "stage %r in bucket %r published %d track(s) but none carries a usable %r "
            "attribute, so no detection could be given a track id. line_crossing, dwell and "
            "velocity_state read det.track_id and will refuse to run rather than count zero. "
            "A registered `track` stage always publishes %r; a replacement must too.",
            stage_name,
            bucket,
            len(tracks),
            _DET_INDEX,
            _DET_INDEX,
        )
        return tuple(detections)
    return tuple(
        detection
        if index not in by_index or detection.track_id == by_index[index]
        else detection.model_copy(update={"track_id": by_index[index]})
        for index, detection in enumerate(detections)
    )


def _to_detection(item: Any) -> Detection:
    """Read one raw detection into the contract's type.

    The detections list is **not ours** (doc ``04``): it arrives from the inference pipeline in
    whichever shape the producing worker uses.  Input is therefore generous about spellings
    and strict about values -- a box outside 0-1 raises, because a pixel-space box is silently
    mis-rendered by fe-streaming (**BE-10**) and wraps to garbage in MPR1 storage (**BE-12**).

    The returned ``category`` may be ``""``: a deployment that sends only a class index has no
    label, and resolving one needs ``model.index_to_category``, which is the caller's business
    (:meth:`Session._intake`).  Deciding *whether the app wants this detection* is not this
    function's job either -- it parses, and nothing more.
    """
    if isinstance(item, Detection):  # includes PipelineDetection
        return item
    if not isinstance(item, Mapping):
        raise SessionError(f"detection must be a mapping or a Detection, got {type(item).__name__} ({item!r:.60})")
    label = ""
    for key in _CATEGORY_KEYS:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            label = value.strip()
            break
    confidence = 0.0
    for key in _CONFIDENCE_KEYS:
        value = item.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            confidence = float(value)
            break
    track_id = None
    for key in _TRACK_KEYS:
        value = item.get(key)
        if isinstance(value, int) and not isinstance(value, bool):
            track_id = int(value)
            break
    try:
        box = _to_box(item)
        if box is None:
            raise SessionError(
                f"detection {item!r:.120} carries no bounding box; tried "
                f"{list(_BOX_KEYS)} and the flat corner keys. Boxes are normalized 0-1 "
                "(contract §4)."
            )
        return Detection(
            category=label,
            confidence=min(1.0, max(0.0, confidence)),
            bounding_box=box,
            # §6b coupling 5: a caller-supplied track id is carried, and is what the stages
            # see when the pipeline has no `track` stage of its own. When it does, that stage
            # is the pipeline's one identity authority and its ids are stamped over this one
            # (_stamp_track_ids) -- otherwise unique_count would dedupe on the tracker's ids
            # while line_crossing counted on the caller's, which is the two-stages-two-
            # identities problem the original "never back-fill" rule was guarding against.
            # The stamp is applied to copies, so this value is what `zone_detections` and the
            # wire payload keep.
            track_id=track_id,
        )
    except ValidationError as exc:
        raise SessionError(
            f"detection {item!r:.120} is not usable: {exc}. The most likely cause is a "
            "pixel-space bounding box: boxes are normalized 0-1, always (contract §4). "
            "Divide by the frame width and height before handing them to the engine."
        ) from exc


def _to_box(item: Mapping[str, Any]) -> BoundingBox | None:
    """Read a bounding box from any of the shapes the pipeline sends."""
    for key in _BOX_KEYS:
        raw = item.get(key)
        if isinstance(raw, BoundingBox):
            return raw
        if isinstance(raw, Mapping):
            corners = _corners(raw)
            if corners is not None:
                return BoundingBox(xmin=corners[0], ymin=corners[1], xmax=corners[2], ymax=corners[3])
        if isinstance(raw, Sequence) and not isinstance(raw, (str, bytes)) and len(raw) == 4:
            values = [float(v) for v in raw]
            return BoundingBox(xmin=values[0], ymin=values[1], xmax=values[2], ymax=values[3])
    corners = _corners(item)
    if corners is not None:
        return BoundingBox(xmin=corners[0], ymin=corners[1], xmax=corners[2], ymax=corners[3])
    return None


def _corners(node: Mapping[str, Any]) -> tuple[float, float, float, float] | None:
    """``(xmin, ymin, xmax, ymax)`` from a mapping using any accepted corner names."""
    found: list[float] = []
    for aliases in _BOX_CORNER_ALIASES:
        for alias in aliases:
            value = node.get(alias)
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                found.append(float(value))
                break
        else:
            return None
    return (found[0], found[1], found[2], found[3])


def _to_mask(item: Mapping[str, Any]) -> MaskRef | None:
    """Read a segmentation mask from a raw detection, or ``None`` when it carries none.

    Three shapes, all of which ship today:

    * the live wire record, ``segmentation: {counts, encoding, size}`` (contract ``04`` §5.1);
    * the flattened backend record, ``mask_rle`` + ``shape`` + ``segmentation_area`` sitting
      directly on the detection (``landslide_detection.py:834-836``, whitelisted through
      ``:889-901``);
    * a polygon, ``segmentation: [[x, y], ...]`` -- legacy Tier 2
      (``landslide_detection.py:296-305``), where a flat ``[x1, y1, x2, y2, ...]`` list
      *silently* falls through to the bounding-box proxy.  It does not fall through here.

    ``None`` means "no mask on this detection", which is a legitimate detector-only stream and
    is what ``segmentation_area.on_missing_mask`` decides about.

    Raises:
        SessionError: A mask is present and unreadable -- a record with no usable carrier, a
            non-numeric polygon, an odd-length flat polygon, or a malformed ``size``.  A
            half-read mask would publish coverage that is plausible and wrong, and legacy's
            silent fall-through to the box is the defect this replaces.
    """
    for key in _MASK_KEYS:
        raw = item.get(key)
        if raw is None:
            continue
        if isinstance(raw, MaskRef):
            return raw
        if isinstance(raw, Mapping):
            record = _mask_from_record(raw, key)
            if record is None:
                raise SessionError(
                    f"detection field {key!r} is a mask record but carries nothing measurable: "
                    f"expected one of {list(_MASK_RLE_KEYS)} (base64 run lengths), "
                    f"{list(_MASK_AREA_KEYS)} (a pixel count) or {list(_MASK_POLYGON_KEYS)} "
                    f"(a contour). Got keys {sorted(raw)}."
                )
            return record
        if isinstance(raw, Sequence) and not isinstance(raw, (str, bytes)):
            polygon = _to_polygon(raw, key)
            if polygon is not None:
                return MaskRef(polygon=polygon, size=_mask_size(item, key))
    return _mask_from_record(item, "detection")


def _mask_from_record(node: Mapping[str, Any], where: str) -> MaskRef | None:
    """Build a :class:`MaskRef` from a mapping, or ``None`` when it holds no carrier."""
    area: int | None = None
    for key in _MASK_AREA_KEYS:
        value = node.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            area = int(value)
            break
    rle: str | None = None
    for key in _MASK_RLE_KEYS:
        value = node.get(key)
        if isinstance(value, str) and value.strip():
            rle = value.strip()
            break
    polygon: tuple[tuple[float, float], ...] | None = None
    for key in _MASK_POLYGON_KEYS:
        value = node.get(key)
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            polygon = _to_polygon(value, f"{where}.{key}")
            if polygon is not None:
                break
    if area is None and rle is None and polygon is None:
        return None
    encoding = node.get("encoding")
    return MaskRef(
        area_px=area,
        size=_mask_size(node, where),
        rle=rle,
        encoding=str(encoding) if isinstance(encoding, str) and encoding.strip() else "simple_rle",
        polygon=polygon,
    )


def _mask_size(node: Mapping[str, Any], where: str) -> tuple[int, int] | None:
    """The mask's own ``(height, width)``, the denominator of its coverage fraction.

    ``[height, width]`` in every spelling: that is the wire's ``size`` (contract ``04`` §5.1)
    and legacy's ``shape``, which is a numpy shape (``landslide_detection.py:286-289``).
    Getting the order wrong is invisible for a square mask and off by the aspect ratio for
    every other one, which is why there is exactly one reader.

    Raises:
        SessionError: A size key is present but is not two positive numbers.
    """
    for key in _MASK_SIZE_KEYS:
        value = node.get(key)
        if value is None:
            continue
        if (
            isinstance(value, Sequence)
            and not isinstance(value, (str, bytes))
            and len(value) == 2
            and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in value)
            and float(value[0]) > 0
            and float(value[1]) > 0
        ):
            return (int(value[0]), int(value[1]))
        raise SessionError(
            f"{where}.{key} is {value!r}; a mask size is [height, width] in model input "
            "space, two positive numbers (contract 04 §5.1). It is the denominator of the "
            "coverage fraction, so a bad one makes the area meaningless rather than absent."
        )
    return None


def _to_polygon(raw: Sequence[Any], where: str) -> tuple[tuple[float, float], ...] | None:
    """Read a contour as ``((x, y), ...)``, accepting the pair and flat spellings.

    ``None`` when the sequence is empty or is not a polygon at all (a mask record's other
    fields land here too).  Legacy accepts only ``[[x, y], ...]`` -- ``np.array(seg).ndim == 2``
    at ``landslide_detection.py:301`` -- and a flat ``[x1, y1, x2, y2, ...]`` list falls
    through to the bounding-box proxy with no log.  Both are read here.

    **Neither spelling of "many numbers" is trusted blindly.**  A dense pixel-mask array --
    one row of ``height`` lists each ``width`` numbers long, or the same thing flattened to
    ``height * width`` numbers -- satisfies this function's own shape checks: a row reads as a
    "vertex" of however many numbers it has, and a flat list reads as pairs regardless of how
    many there are.  Read that way, a real mask silently becomes a degenerate few-point
    "polygon" (each row's first one or two pixels as one point) with a plausible-looking,
    wrong, near-zero area -- exactly the "half-read mask published as a real number" failure
    :func:`_to_mask` exists to refuse.  :data:`_MAX_POLYGON_VERTEX_LEN` and
    :data:`_MAX_POLYGON_POINTS` catch this the only way possible without decoding pixels: a
    real contour vertex is ``[x, y]`` (never dozens/hundreds of numbers, which a mask row is),
    and a real contour has at most a few thousand points (never ``height * width`` of them).
    This primitive still never decodes a dense pixel array itself (no numpy/cv2, **PY-20**,
    see ``segmentation_area.py``'s module docstring) -- it fails loudly instead, so the
    producer sends ``simple_rle`` (contract ``04`` §5.1) rather than decoded pixels.

    Raises:
        SessionError: The sequence looks like a polygon and is malformed: a non-numeric
            vertex, an odd-length flat list, or -- either spelling -- so many numbers it is
            almost certainly a dense pixel-mask array rather than a contour.
    """
    if not raw:
        return None
    first = raw[0]
    if isinstance(first, Sequence) and not isinstance(first, (str, bytes)):
        points: list[tuple[float, float]] = []
        for vertex in raw:
            if (
                not isinstance(vertex, Sequence)
                or isinstance(vertex, (str, bytes))
                or len(vertex) < 2
                or not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in vertex[:2])
            ):
                raise SessionError(
                    f"{where} looks like a polygon but has the vertex {vertex!r}; every vertex "
                    "must be a numeric [x, y] pair."
                )
            if len(vertex) > _MAX_POLYGON_VERTEX_LEN:
                raise SessionError(
                    f"{where} has a {len(vertex)}-number 'vertex' (first few: "
                    f"{list(vertex[:5])!r}...); a polygon point is [x, y] (or [x, y, z]), never "
                    "more. This many numbers in one row means the payload is a dense "
                    "pixel-mask array -- one row per mask row, one number per pixel -- not a "
                    "contour. This primitive never decodes a dense pixel array (no numpy/cv2, "
                    "PY-20): encode it as simple_rle (contract 04 §5.1) instead of sending "
                    "decoded pixels."
                )
            points.append((float(vertex[0]), float(vertex[1])))
        if len(points) > _MAX_POLYGON_POINTS:
            raise SessionError(
                f"{where} has {len(points)} vertices, far more than any real contour has. "
                "This is almost certainly a dense pixel-mask array shaped as one row per mask "
                "row, not a polygon: encode it as simple_rle (contract 04 §5.1) instead of "
                "sending decoded pixels."
            )
        return tuple(points)
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in raw):
        return None
    if len(raw) % 2:
        raise SessionError(
            f"{where} is a flat polygon of {len(raw)} numbers, which is not an even count of "
            "[x, y] pairs. Legacy drops this shape silently and falls back to bounding-box "
            "area (landslide_detection.py:296-313), reporting box coverage as mask coverage."
        )
    if len(raw) // 2 > _MAX_POLYGON_POINTS:
        raise SessionError(
            f"{where} is a flat list of {len(raw)} numbers ({len(raw) // 2} points), far more "
            "than any real contour has. This is almost certainly a flattened dense pixel-mask "
            "array (length height*width), not a polygon: encode it as simple_rle (contract 04 "
            "§5.1) instead of sending decoded pixels."
        )
    values = [float(v) for v in raw]
    return tuple((values[i], values[i + 1]) for i in range(0, len(values), 2))


def _to_keypoints(item: Mapping[str, Any], space: Callable[[], tuple[int, int] | None]) -> tuple[Keypoint, ...]:
    """Read a detection's pose joints, **normalized 0-1**, or ``()`` when it has none.

    ``keypoints`` is the only key, and that is deliberate: it is the wire name (contract ``04``
    §5.1) and the single key all three legacy extractors read (``fall_detection.py:64`` and
    both siblings).

    Two shapes are accepted -- the documented wire one (a list of ``[x, y, confidence]``) and a
    flat list -- and **everything else raises**.  The legacy parser's four silent
    ``except ...: return None`` handlers (``fall_detection.py:89-116``) are how a malformed
    payload becomes "no falls detected", which is the failure this function refuses to
    reproduce.

    Two corrections to legacy, both from ``PRIMITIVE_SPECS.md`` §2.4:

    **A missing confidence channel is 0.0, never 1.0.**  Legacy substitutes ``1.0``
    (``fall_detection.py:86``, ``:103``, ``:112``), so every ``min_keypoint_confidence`` gate
    passes unconditionally whatever the manifest says -- the joint might not have been detected
    at all.  ``0.0`` means "we do not know it is visible", which is the truth.

    **Coordinates are normalized here, so the pipeline has one unit.**  Legacy keypoints are
    absolute pixels while every box in this engine is 0-1, and mixing the two in one context is
    **PY-7** -- the class of bug that produces a silent 1920x error.  A payload already inside
    0-1 is taken as normalized; otherwise the dimensions come from the detection's own
    ``keypoint_space``/``image_size``/``input_shape``, then from ``space()`` (the stream
    resolution, warned about once).

    Raises:
        SessionError: The value is not a list, holds a non-numeric joint, is a flat list whose
            length is neither a multiple of 3 nor of 2, or is in pixel space on a stream with
            no dimensions to normalize by.
    """
    raw = item.get(_KEYPOINT_KEY)
    if raw is None:
        return ()
    if isinstance(raw, (Mapping, str, bytes)) or not isinstance(raw, Sequence):
        raise SessionError(
            f"detection {_KEYPOINT_KEY!r} is a {type(raw).__name__}; it must be a list of "
            "[x, y, confidence] joints, complete and fixed-length for the skeleton (contract "
            "04 §5.1). The legacy dict form ({'xy': ..., 'conf': ...}) is deliberately not "
            "accepted: it is one of the shapes whose confidence channel is optional, and a "
            "keypoint with a forged confidence defeats min_keypoint_confidence entirely."
        )
    if not raw:
        return ()

    triples = _keypoint_triples(raw)
    if not triples:
        return ()
    largest = max(max(abs(x), abs(y)) for x, y, _ in triples)
    if largest <= 1.0 + 1e-6:
        return tuple(Keypoint(x, y, c) for x, y, c in triples)

    dimensions = _keypoint_space(item) or space()
    if dimensions is None:
        raise SessionError(
            f"detection keypoints are in pixel space (largest coordinate {largest:g}) and this "
            "stream declares no resolution, so they cannot be normalized. Bounding boxes are "
            "normalized 0-1 always (contract §4) and keypoints must share that space -- mixed "
            "units in one frame is defect PY-7. Either have the producer send normalized "
            "keypoints, set keypoint_space: [width, height] on the detection, or set "
            "StreamInfo.resolution from the camera's source dimensions."
        )
    width, height = dimensions
    return tuple(Keypoint(x / width, y / height, c) for x, y, c in triples)


def _keypoint_triples(raw: Sequence[Any]) -> tuple[tuple[float, float, float], ...]:
    """``(x, y, confidence)`` per joint, in the payload's own coordinate space."""
    first = raw[0]
    if isinstance(first, Sequence) and not isinstance(first, (str, bytes)):
        joints: list[tuple[float, float, float]] = []
        for joint in raw:
            if (
                not isinstance(joint, Sequence)
                or isinstance(joint, (str, bytes))
                or len(joint) < 2
                or not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in joint[:3])
            ):
                raise SessionError(f"detection keypoint {joint!r} is not a numeric [x, y] or [x, y, confidence] joint.")
            # No confidence channel -> 0.0. Never 1.0; see this module's _to_keypoints.
            confidence = float(joint[2]) if len(joint) > 2 else 0.0
            joints.append((float(joint[0]), float(joint[1]), confidence))
        return tuple(joints)

    if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in raw):
        raise SessionError(
            f"detection keypoints hold a non-numeric entry: {list(raw)[:6]!r}...; a flat "
            "keypoint list is [x0, y0, c0, x1, y1, c1, ...] or [x0, y0, x1, y1, ...]."
        )
    values = [float(v) for v in raw]
    if len(values) % 3 == 0:
        # The wire shape, flattened: 51 numbers for coco17.
        return tuple((values[i], values[i + 1], values[i + 2]) for i in range(0, len(values), 3))
    if len(values) % 2 == 0:
        # xy only (legacy's length-34 shape): confidence is unknown, so it is 0.0.
        return tuple((values[i], values[i + 1], 0.0) for i in range(0, len(values), 2))
    raise SessionError(
        f"detection keypoints is a flat list of {len(values)} numbers, which is neither a "
        "multiple of 3 ([x, y, confidence] per joint) nor of 2 ([x, y] per joint). The wire "
        "shape is a complete fixed-length list for the skeleton -- 51 numbers for coco17 -- "
        "and a length that fits neither means joints are missing, which would shift every "
        "index and read the wrong joint."
    )


def _keypoint_space(item: Mapping[str, Any]) -> tuple[int, int] | None:
    """The model input ``(width, height)`` this detection's keypoints are measured in.

    ``keypoint_space``/``image_size`` are ``[width, height]``; ``input_shape`` is a numpy-style
    ``[height, width]``, matching the mask's ``shape``.  Stated per detection because only the
    producer knows its model's input size -- the stream's resolution is the camera's.
    """
    for key in _KEYPOINT_SPACE_KEYS:
        value = item.get(key)
        if (
            isinstance(value, Sequence)
            and not isinstance(value, (str, bytes))
            and len(value) == 2
            and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in value)
            and float(value[0]) > 0
            and float(value[1]) > 0
        ):
            first, second = int(value[0]), int(value[1])
            return (second, first) if key == "input_shape" else (first, second)
    return None


def _ascii_digits(value: Any) -> bool:
    """Whether ``value`` is a string of plain ASCII digits, e.g. ``"1"``.

    ``str.isdigit()`` alone is also true for superscripts and Arabic-Indic digits, which
    ``int()`` then rejects or reads as a number no detector meant; requiring ASCII keeps this
    to the one shape that actually arrives -- a class index that was formatted as text.
    """
    if not isinstance(value, str):
        return False
    text = value.strip()
    return bool(text) and text.isascii() and text.isdigit()


def _coerce_index(value: Any) -> int | None:
    """One raw value read as a class index, or ``None`` when it is not one.

    Accepts an ``int`` and an ASCII-digit string, because model nodes disagree on the *type* as
    well as the key: ``rfdetr_decode._emit`` sends the index as the string ``"1"`` so that the
    legacy ``apply_category_mapping`` can map it, and a node with no label map configured has
    nothing else to send.
    """
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return int(value)
    return int(value.strip()) if _ascii_digits(value) else None


def _class_index(item: Any) -> int | None:
    """A detection's class index, for ``model.index_to_category`` deployments.

    An explicit index key wins.  A numeric *category* is the fallback, because a detector with
    no label map sends its class index where the label goes -- ``{"category": "1"}`` -- and
    reading that only as a label means ``index_to_category`` is never consulted, no entity
    matches, and every detection is counted as unmapped and dropped.  The result is an empty
    dashboard behind an inference log full of detections, which is the exact failure class this
    engine exists to remove.

    A category that is a *real* label still wins over the index, because
    :meth:`_EntityMapper.entity_for` tries the label first: a model is entitled to name its
    classes ``"0"`` and ``"1"`` and map them in ``entity_mapping``.
    """
    if isinstance(item, Detection):  # includes PipelineDetection
        # A caller-built detection carries no index *key* -- the typed model has no field for
        # one -- so its category is the only place an index can be, and for a node with no
        # label map configured that category is exactly what the index arrived as.
        return _coerce_index(item.category)
    if not isinstance(item, Mapping):
        return None
    for key in (*_INDEX_KEYS, *_CATEGORY_KEYS):
        index = _coerce_index(item.get(key))
        if index is not None:
            return index
    return None


def _rank(severity: str) -> int:
    """Ascending severity order, tolerant of the internal spellings (**FROZEN-7**)."""
    if not severity:
        return -1
    try:
        return SEVERITY_RANK[parse_severity(severity)]
    except ValueError:
        return -1


def _threshold_matches(threshold: MetricThreshold, value: float) -> bool:
    """Whether ``value`` satisfies any operator on this ``severity_from`` threshold.

    A graded ``levels`` list with no comparison operator fires at its lowest rung, which is
    what "graded" means: below the first rung nothing is wrong.
    """
    operators = threshold.operators
    if operators:
        for operator, bound in operators.items():
            if _compare(operator, value, bound):
                return True
        return False
    if threshold.levels:
        return value >= threshold.levels[0].value
    return False


def _compare(operator: str, value: float, bound: float) -> bool:
    if operator == ">":
        return value > bound
    if operator == ">=":
        return value >= bound
    if operator == "<":
        return value < bound
    if operator == "<=":
        return value <= bound
    if operator == "==":
        return value == bound
    return value != bound  # "!="


def _graded_severity(threshold: MetricThreshold, value: float) -> str:
    """The highest ``levels`` rung ``value`` reaches, else :data:`DEFAULT_THRESHOLD_SEVERITY`.

    ``levels`` are validated ascending by ``value`` at manifest load, so walking them in order
    and keeping the last match is well defined -- which is the point of that validation.
    """
    severity = ""
    for level in threshold.levels:
        if value >= level.value:
            severity = level.level
    return severity or DEFAULT_THRESHOLD_SEVERITY


def _interpolate(template: str, values: Mapping[str, float]) -> str:
    """Fill ``{metric_key}`` placeholders in ``human_text``.

    An operator reads this on a phone at 3am (``08`` §4), so a missing value leaves the
    placeholder visible rather than raising: losing the whole alert because one metric did not
    resolve this frame is strictly worse than an alert with one gap in it.  The manifest
    already rejects a placeholder that is not a declared metric.
    """
    return template.format_map(_Placeholders(values))


class _Placeholders(dict):  # type: ignore[type-arg]
    """``format_map`` view that renders numbers tidily and keeps unknowns literal."""

    def __init__(self, values: Mapping[str, float]) -> None:
        super().__init__(values)

    def __missing__(self, key: str) -> str:
        return "{" + key + "}"

    def __getitem__(self, key: str) -> Any:
        value = super().get(key)
        if value is None:
            return self.__missing__(key)
        number = float(value)
        return str(int(number)) if number.is_integer() else f"{number:.2f}"
