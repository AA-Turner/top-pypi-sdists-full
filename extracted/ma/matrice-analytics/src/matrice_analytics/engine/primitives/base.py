"""The ``Primitive`` protocol and the four types every primitive speaks in.

Normative source: ``_contracts/09-tobe-engine-architecture.md`` §3 (the interface) and §6
(the two custom-code interfaces).  ``_contracts/10-app-authoring-guide.md`` is the same
API written for app authors, and
``ml-applications/guidelines/examples/04-queue-service-time/logic.py`` is a real custom primitive
that must keep working against this module unchanged.

Three design constraints, each with a defect behind it:

**A protocol, not a base class.**  ``BaseProcessor`` today carries ~20 payload-shaping
helpers plus a duplicate deprecated set of all of them (``core/base.py:617-781``).
Inheritance is how that happened: the base class became the place to put anything shared,
and then anything at all.  A protocol gives primitives *nothing to inherit* -- shared
behaviour lives in the runtime, which calls them (``09`` §3).

**Primitives are pure over ``(detections, state, config)``.**  They return
primitive-shaped data.  Nothing here knows the wire format: only
:mod:`matrice_analytics.engine.contract.emit` builds a payload, which is what makes three
divergent builders impossible (**PY-3**, objective **O1**).  Nothing here knows an app's
name either (``09`` §1).

**The clock is injectable and frame-driven** (**PY-13**).  ``should_aggregate(frame_ts)``
is designed for frame timestamps but ``engine_session.py:595`` passes ``time.time()``, so
replay, backfill and simulation aggregate on wall-clock and produce wrong windows.
:attr:`FrameContext.frame_ts` is the real frame time, and :class:`FrameClock` is the
default clock: it only advances when a frame says so.

The whole coupling surface between a primitive and a manifest is
:attr:`PrimitiveOutput.values` -- ``source: ratio_compliance.compliance_pct`` resolves to
``outputs["ratio_compliance"].values["compliance_pct"]`` via :func:`resolve_value`, and an
unresolvable source is an error, *not* a metric that reads zero forever (``09`` §3).
"""

from __future__ import annotations

import inspect
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, ClassVar, NamedTuple, Protocol, runtime_checkable

from pydantic import BaseModel, model_validator

from matrice_analytics.engine.contract.schemas import (
    GLOBAL_ZONE,
    Detection,
    StreamInfo,
    WireSegmentationMask,
    ZoneConfig,
)
from matrice_analytics.engine.state import StateStore

__all__ = [
    "Clock",
    "CustomPrimitive",
    "FrameClock",
    "FrameContext",
    "Keypoint",
    "MaskRef",
    "PipelineDetection",
    "Primitive",
    "PrimitiveEvent",
    "PrimitiveOutput",
    "PrimitiveRegistrationError",
    "PrimitiveRegistry",
    "PrimitiveValueError",
    "REGISTRY",
    "Scalar",
    "SourceResolutionError",
    "TrackState",
    "WallClock",
    "WindowOutput",
    "conformance_problems",
    "register",
    "resolve_value",
]

#: What a ``values`` entry may hold.  ``metrics[].data`` is a float and ``count`` is an int
#: on the wire, and a numeric *string* is rejected outright (contract Section 1 rule 6), so
#: the set is closed here too rather than at emit time.
Scalar = float | int | str


class PrimitiveValueError(ValueError):
    """A :attr:`PrimitiveOutput.values` entry is not a publishable scalar.

    Caught at construction rather than at emit: by the time the contract rejects a
    ``None`` the frame that produced it is gone, and the failure reads as "the payload is
    malformed" rather than "this primitive returned nothing for this key".
    """


class SourceResolutionError(KeyError):
    """A ``metrics[].source`` does not resolve against the pipeline's outputs.

    ``09`` §3: *an unresolvable source is a manifest load error -- not a metric that reads
    zero forever*.  The current engine's silent-zero behaviour is indistinguishable from a
    genuinely quiet camera, which is why this raises.
    """


class PrimitiveRegistrationError(ValueError):
    """A class cannot be registered as a primitive implementation."""


# ---------------------------------------------------------------------------
# The clock (PY-13)
# ---------------------------------------------------------------------------


@runtime_checkable
class Clock(Protocol):
    """The engine's only source of "now".

    Injectable so that replay, backfill and generated tests are driven by frame time
    rather than by the host's wall clock (**PY-13**).  Windowing
    (``engine/runtime/window.py``) consumes this; primitives should read
    :attr:`FrameContext.frame_ts` and never call a clock at all.
    """

    def now(self) -> float:
        """Current time in epoch seconds."""
        ...


@dataclass(slots=True)
class FrameClock:
    """The default clock: it advances only when a frame says so (**PY-13**).

    Feeding it the real frame timestamp makes a replayed hour of footage produce exactly
    the windows the live run produced.  ``time.time()`` cannot do that, which is the whole
    defect.

    Example:
        >>> clock = FrameClock()
        >>> clock.advance(1_700_000_000.0)
        >>> clock.now() == 1_700_000_000.0
        True
    """

    _now: float = 0.0

    def now(self) -> float:
        """The timestamp of the most recent frame."""
        return self._now

    def advance(self, frame_ts: float) -> None:
        """Move the clock to ``frame_ts``.

        Args:
            frame_ts: The real frame timestamp, epoch seconds.

        Raises:
            ValueError: ``frame_ts`` goes backwards.  Out-of-order frames would reopen a
                closed window and double-publish it; the caller must decide to drop or to
                reset, and cannot decide it by accident.
        """
        if frame_ts < self._now:
            raise ValueError(
                f"frame_ts {frame_ts} is before the clock's current time {self._now}. "
                "Frames must arrive in order; an out-of-order frame would reopen an "
                "already-published aggregation window (PY-13). Drop the frame, or reset "
                "the clock explicitly."
            )
        self._now = frame_ts

    def reset(self, frame_ts: float = 0.0) -> None:
        """Force the clock to ``frame_ts``, e.g. when a stream restarts."""
        self._now = frame_ts


@dataclass(frozen=True, slots=True)
class WallClock:
    """``time.time()``, for the few places that genuinely mean wall-clock.

    Never the default.  Passing this where a :class:`FrameClock` belongs is exactly
    **PY-13** (``engine_session.py:595``), so it is a named type you have to opt into
    rather than a bare call buried in a session.
    """

    def now(self) -> float:
        """Current wall-clock time in epoch seconds."""
        return time.time()


# ---------------------------------------------------------------------------
# What a primitive sees
# ---------------------------------------------------------------------------


class Keypoint(NamedTuple):
    """One pose joint, ``(x, y, confidence)``, **normalized 0-1** like a bounding box.

    A tuple rather than a model because that is the wire shape
    (``_contracts/04-asis-live-frame-contract.md:678-706``: a fixed-length list of
    ``[x, y, confidence]``) and because a skeleton is 17 of these per person per frame --
    validating a Pydantic model 425 times a second at 25 fps buys nothing that the intake
    parse has not already checked.

    **Both coordinate conventions in one field is defect PY-7**, so there is only one here.
    The legacy tree's keypoints are absolute pixels -- ``hands_above_head_margin_px`` is
    compared directly against a joint ``y`` (``fence_climbing_detection_pose.py:139``) and
    ``head_h = shoulder_y - y1`` mixes a joint ``y`` with a bbox edge
    (``face_covering_detection_pose.py:175``) -- while every box in this engine is
    normalized 0-1 and a box outside that range is rejected outright (**BE-10**/**BE-12**).
    Mixing the two in one :class:`FrameContext` is how a silent 1920x error happens, so
    ``runtime/session.py`` normalizes at intake and everything downstream reads 0-1.

    :attr:`confidence` is the per-joint visibility score.  **A payload with no confidence
    channel yields 0.0, never 1.0.**  Legacy forges ``1.0`` (``fall_detection.py:86``,
    ``:103``, ``:112``, and the same lines in both siblings), which makes every
    ``min_keypoint_confidence`` gate pass unconditionally whatever the manifest says -- a
    config field that cannot fail is worse than no field.
    """

    x: float
    y: float
    confidence: float


@dataclass(frozen=True, slots=True)
class MaskRef:
    """A segmentation mask as the engine carries it -- **a reference, not pixels**.

    Engine-internal like :attr:`PipelineDetection.entity`, with one exception:
    :meth:`PipelineDetection.to_wire` re-emits :attr:`rle` (when present) as the wire's
    declared, RLE-only ``Detection.segmentation`` field -- never :attr:`polygon` or a
    rasterized :attr:`area_px`, since this engine does not encode pixels for the wire (no
    numpy/cv2, **PY-20**) and a decoded shape has nothing ready-to-emit.

    Three carriers, because the producers ship three and each is cheaper than the last to
    turn into an area (``landslide_detection.py:283-313`` cascades over exactly these):

    :attr:`area_px`
        A foreground pixel count already computed upstream
        (``merged_det["segmentation_area"] = mask_info["area_pixels"]``,
        ``landslide_detection.py:836``).  Free -- no decode at all.
    :attr:`rle`
        The base64 ``simple_rle`` the live producer sends
        (``_contracts/04-asis-live-frame-contract.md:657-671``).  Decoded by
        :func:`~matrice_analytics.engine.primitives.segmentation_area.decode_simple_rle_area`
        with ``base64`` and ``int.from_bytes`` -- **no numpy, no cv2** (**PY-20**).
    :attr:`polygon`
        A contour.  ``cv2.contourArea`` returns the unsigned shoelace area of a simple
        polygon, so the pure-Python shoelace in
        :func:`~matrice_analytics.engine.primitives.segmentation_area.polygon_area` is
        behaviour-preserving rather than an approximation.

    :attr:`size` is the mask's **own** array shape, ``(height, width)``, in model input
    space.  It is the denominator, which is why ``segmentation_area`` needs no frame
    resolution: a mask covers the whole frame in model space, so ``area_px / (h * w)`` is
    resolution-free.  That is the choice legacy Tier 1 made
    (``landslide_detection.py:285-291``) and the reason this primitive never calls
    :meth:`FrameContext.require_resolution`.
    """

    area_px: int | None = None
    """Foreground pixel count in :attr:`size` space, when the producer already counted it."""

    size: tuple[int, int] | None = None
    """``(height, width)`` of the mask's own array -- the area denominator."""

    rle: str | None = None
    """Base64 run lengths; see :attr:`encoding`."""

    encoding: str = "simple_rle"
    """How :attr:`rle` is encoded.  Only ``simple_rle`` is decodable here, and anything else
    is **refused** rather than decoded anyway: COCO's compressed RLE uses the same
    ``counts`` key with an LEB128-style byte stream, so treating it as uint32 run lengths
    would publish a plausible, wrong area with no error."""

    polygon: tuple[tuple[float, float], ...] | None = None
    """Contour vertices in :attr:`size` space, or normalized 0-1 when :attr:`size` is None."""


class PipelineDetection(Detection):
    """A wire :class:`~matrice_analytics.engine.contract.schemas.Detection` plus the
    fields the pipeline adds before a primitive sees it.

    ``09`` §3 says ``FrameContext.detections`` are "already entity-remapped and
    zone-assigned", but the wire ``Detection`` carries neither an ``entity`` nor a
    ``zone``: ``category`` is the *model's* class label, which is precisely what entity
    remapping exists to stop primitives from depending on.  Rather than redeclare the
    detection (the contract owns it -- **O1**), this subclasses it, so
    :class:`~matrice_analytics.engine.contract.schemas.BoundingBox`, the 0-1 range check
    (**BE-10**, **BE-12**) and the confidence check keep applying unchanged.

    :meth:`to_wire` converts back.  Use it -- the extra two fields must not reach the
    payload, and ``extra="forbid"`` on the wire model means a stray one is a hard failure
    at emit rather than a silent extra key.
    """

    entity: str = ""
    """The analytics entity from ``model.entity_mapping``, e.g. ``"person"``.

    Defaults to :attr:`~matrice_analytics.engine.contract.schemas.Detection.category` when
    the pipeline has no mapping for the label, so a primitive can always read it.
    """

    zone: str = GLOBAL_ZONE
    """The assigned zone name, ``"global"`` for single-bucket apps.

    Never ``"__global__"`` -- the sentinel splits an app's ClickHouse history into two
    unrelated series (**PY-6**).  Detections matching no zone land in whatever bucket
    ``zones.on_no_match`` declares, and are *counted*, never silently dropped (**PY-10**).
    """

    mask: MaskRef | None = None
    """This detection's segmentation mask, or ``None`` when it carries none.

    Read by ``segmentation_area`` and by nothing else.  ``None`` is the honest value for a
    detector-only stream and is what makes ``measured_count < instance_count`` -- the
    visible signal for a mask-pipeline outage that legacy has no way to report, because it
    substitutes the bounding box for the mask with no flag and no log
    (``landslide_detection.py:307-313``).
    """

    keypoints: tuple[Keypoint, ...] = ()
    """This detection's pose joints, **normalized 0-1**, empty when there are none.

    Read by ``keypoint_pose``.  For ``skeleton_type: coco17`` this is 17 entries, in the
    Ultralytics/OpenPose order the legacy extractors assume
    (``fall_detection.py:28-29``, ``fence_climbing_detection_pose.py:25-32``); the tuple is
    complete and positional, never sparse.  See :class:`Keypoint` for why the units are
    normalized and why a missing confidence channel is ``0.0``.
    """

    @model_validator(mode="after")
    def _entity_defaults_to_category(self) -> "PipelineDetection":
        """Fill ``entity`` from ``category`` rather than leaving it empty.

        An empty ``entity`` compares unequal to every entity name, so a custom primitive's
        ``if det.entity != "person"`` would skip every detection and report zero -- the
        silent-zero failure mode this engine is built to remove.
        """
        if not self.entity:
            # validate_assignment is on; write through __dict__ rather than re-entering
            # validation from inside the validator (same trick as IncidentMessage).
            self.__dict__["entity"] = self.category
        if not self.zone:
            self.__dict__["zone"] = GLOBAL_ZONE
        return self

    @classmethod
    def from_detection(
        cls,
        detection: Detection,
        *,
        entity: str = "",
        zone: str = GLOBAL_ZONE,
        mask: MaskRef | None = None,
        keypoints: Sequence[Keypoint] = (),
    ) -> "PipelineDetection":
        """Attach pipeline fields to a wire detection.

        ``mask`` and ``keypoints`` are keyword-only and default to "absent" because the wire
        :class:`~matrice_analytics.engine.contract.schemas.Detection` cannot carry them --
        they come from the raw producer dict, which ``runtime/session.py`` parses.
        """
        return cls(
            category=detection.category,
            confidence=detection.confidence,
            bounding_box=detection.bounding_box,
            track_id=detection.track_id,
            entity=entity or detection.category,
            zone=zone,
            mask=mask,
            keypoints=tuple(keypoints),
        )

    def to_wire(self) -> Detection:
        """Drop the pipeline-internal fields, yielding the contract's detection.

        ``entity`` and ``zone`` are engine concepts: the payload's per-zone structure
        already carries the zone (**FROZEN-2**) and its ``category`` is the model label the
        overlay draws.  Emitting either would be a new, undeclared wire field.
        :attr:`keypoints` is dropped for the same reason.

        :attr:`mask` is the one field that conditionally survives: its ``rle`` (when the
        producer sent a ready-to-emit ``simple_rle`` string) becomes ``Detection.segmentation``
        below, byte for byte -- a genuinely declared wire field (:class:`WireSegmentationMask`
        on :class:`Detection`), not a leak, since ``extra="forbid"`` would reject anything not
        named on that model.  A mask that only carries a polygon or a precomputed
        :attr:`~.MaskRef.area_px` has nothing ready-to-emit -- this method never rasterizes or
        encodes pixels (no numpy/cv2, **PY-20**) -- so ``segmentation`` stays ``None`` for it,
        same as for a detector-only stream.  This method still names every wire field
        explicitly rather than copying whatever :class:`PipelineDetection` happens to hold, so
        an engine-internal field cannot leak into a payload by being added upstream.
        """
        segmentation = None
        if self.mask is not None and self.mask.rle is not None and self.mask.size is not None:
            segmentation = WireSegmentationMask(encoding=self.mask.encoding, counts=self.mask.rle, size=self.mask.size)
        return Detection(
            category=self.category,
            confidence=self.confidence,
            bounding_box=self.bounding_box,
            track_id=self.track_id,
            segmentation=segmentation,
        )


@dataclass(frozen=True, slots=True)
class FrameContext:
    """Everything a primitive is given for one frame, in one zone.

    A plain frozen dataclass rather than a Pydantic model **on purpose**: this is
    constructed once per frame *per zone* -- at 25 fps with four zones that is 100
    validations a second per camera -- and its contents have already been validated
    upstream (``StreamInfo`` for ``fps``, :class:`PipelineDetection` for the detections).
    The models in ``engine/contract`` and ``engine/manifest`` sit on cold paths and stay
    Pydantic; the hot path does not.

    Frozen, with ``detections`` copied to a tuple and ``previous`` wrapped read-only, so a
    primitive cannot mutate the set the next primitive in the pipeline is about to see.
    """

    detections: Sequence[PipelineDetection]
    """This zone's detections, already entity-remapped, tracked and zone-assigned."""

    zone: str
    """``"global"`` or a zone name.  Never ``"__global__"`` (**PY-6**)."""

    frame_ts: float
    """The **real frame timestamp**, epoch seconds -- never ``time.time()`` (**PY-13**).

    Derived from the media anchor (``stream_time`` / rtp), so a replayed stream produces
    the same windows, the same dwell times and the same incident durations as the live run
    did.  Every duration a primitive computes must come from this field.
    """

    fps: float
    """Source frames per second, from ``StreamInfo.original_fps``.  ``0.0`` means unknown.

    **No primitive divides by this, and none should.**  Every duration in the engine comes
    from :attr:`frame_ts` deltas (**PY-13**) -- see ``dwell`` ("no ``fps`` arithmetic") and
    ``velocity_state`` ("Every duration comes from ``FrameContext.frame_ts``"), both of
    which were written that way precisely so a declared rate that disagrees with the
    delivered one cannot skew a measurement.

    It is carried for the S3 ``input_streams`` echo and for a custom stage that wants the
    declared rate as *metadata*.  A stage that reads it must handle ``0.0``: the producer
    genuinely may not know the rate, and refusing the stream over a number nothing computes
    with is how INF-2606 killed every camera on a node whose upstream capture clock was
    mis-stamped.
    """

    previous: Mapping[str, "PrimitiveOutput"] = field(default_factory=dict)
    """Outputs of the earlier stages of this pipeline, keyed by stage name.

    Keyed by *stage* name, not primitive name: a manifest may run the same primitive twice
    with different ``name:`` values, and ``metrics[].source`` resolves against the stage
    name (``manifest.models.PrimitiveConfig.stage_name``).
    """

    stream: StreamInfo | None = None
    """The camera and frame context for this stream -- **the standard channel**.

    ``StreamInfo`` (``contract/schemas.py``, surface S4) already carries every piece of
    per-camera context a primitive can legitimately need: identity (``camera_id``,
    ``camera_name``, ``camera_group``), the app (``app_id``, ``application_name``, ...),
    ``location``, ``original_fps``, ``resolution``, and the media anchors ``rtp_number`` /
    ``stream_time`` / ``frame_id``.  Putting a reference to it here means there is exactly
    one place to look, and one place for the runtime to fill in.

    **Why this field exists.** Stage B built four workstreams in parallel and two of them
    independently needed the frame resolution -- geometry to convert normalized 0-1 boxes
    to pixels, ``velocity_state`` to evaluate a px/s threshold -- and, with no channel for
    it, invented two different ones: an injected ``SceneGeometry`` in one, a private state
    key with a silent 1920x1080 fallback in the other.  Two mechanisms for one need, one of
    them guessing.  A third would have appeared with the next primitive.

    Optional only so that a test can construct a context for a primitive that does not need
    it.  **The runtime always sets it.**  A primitive that needs a field should reach for
    :meth:`require_resolution` (or read ``ctx.stream`` directly) rather than defaulting,
    because a wrong resolution is silently wrong output -- the numbers look plausible and
    are off by the ratio of the two frame sizes.
    """

    def __post_init__(self) -> None:
        """Freeze the containers and reject the two values that break arithmetic."""
        object.__setattr__(self, "detections", tuple(self.detections))
        if not isinstance(self.previous, MappingProxyType):
            object.__setattr__(self, "previous", MappingProxyType(dict(self.previous)))
        if not self.zone:
            object.__setattr__(self, "zone", GLOBAL_ZONE)
        if self.fps < 0:
            raise ValueError(
                f"FrameContext.fps must not be negative, got {self.fps}. Zero is allowed and "
                "means the producer does not know the rate; a negative one is a parse error."
            )
        if self.frame_ts != self.frame_ts:  # NaN
            raise ValueError(
                "FrameContext.frame_ts is NaN. It must be the real frame timestamp in "
                "epoch seconds (PY-13); a missing media anchor is a loud error, not a NaN."
            )

    # -- standardised accessors over ``stream`` -----------------------------------
    # Thin readers, not a second source of truth. They exist so a primitive never has to
    # write `ctx.stream.resolution if ctx.stream else <guess>` -- the guess is the bug.

    @property
    def resolution(self) -> tuple[int, int] | None:
        """``(width, height)`` in pixels, or ``None`` when unknown.

        ``None`` and ``(0, 0)`` both mean "not configured" and both come back as ``None``,
        so callers have one thing to check. Use :meth:`require_resolution` when the
        primitive cannot work without it.
        """
        if self.stream is None:
            return None
        width, height = self.stream.resolution
        return (width, height) if width > 0 and height > 0 else None

    def require_resolution(self, what: str) -> tuple[int, int]:
        """``resolution``, or a loud error naming who needed it and why.

        Bounding boxes are normalized 0-1; anything expressed in pixels -- zone polygons,
        a px/s speed threshold, an inset distance -- needs this to be meaningful. Guessing
        a default produces output that is plausible and wrong by the ratio of the guessed
        frame size to the real one, which is far worse than not starting.
        """
        resolution = self.resolution
        if resolution is None:
            raise PrimitiveValueError(
                f"{what} needs the frame resolution, and this stream has none. "
                "Bounding boxes are normalized 0-1, so a pixel-space value cannot be "
                "evaluated without it. Set StreamInfo.resolution from the camera's source "
                "dimensions at session setup -- do not default it, because a wrong "
                "resolution is silently wrong output rather than a failure."
            )
        return resolution

    @property
    def camera_id(self) -> str:
        """The camera this frame came from, or ``""`` when no stream is attached."""
        return self.stream.camera_id if self.stream else ""

    @property
    def frame_id(self) -> str:
        """The frame's media anchor, or ``""``. Useful when raising an event."""
        return self.stream.frame_id if self.stream else ""

    @property
    def zone_config(self) -> "ZoneConfig | None":
        """The camera's zone geometry, normalized 0-1, or ``None`` when unconfigured."""
        return self.stream.zone_config if self.stream else None

    def of_entity(self, *entities: str) -> tuple[PipelineDetection, ...]:
        """This frame's detections restricted to ``entities``.

        The one convenience on this type.  It is here rather than on a base class because
        every primitive needs it and none of them may inherit anything (``09`` §3) -- and
        it is a filter over data the caller already has, not a shared behaviour that could
        grow into another ``BaseProcessor``.
        """
        wanted = frozenset(entities)
        return tuple(det for det in self.detections if det.entity in wanted)


# ---------------------------------------------------------------------------
# What a primitive returns
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TrackState:
    """One tracked object as a primitive sees it.

    Carried on :attr:`PrimitiveOutput.tracks` so that a later stage (``dwell``,
    ``velocity_state``, a custom primitive) can read it without re-implementing tracking --
    the thing every use case does today, and the reason 17 of them hand-rolled a dwell
    clock.
    """

    track_id: int
    entity: str
    zone: str = GLOBAL_ZONE
    first_seen: float = 0.0
    """Frame timestamp of the first sighting (**PY-13**: frame time, not wall-clock)."""
    last_seen: float = 0.0
    """Frame timestamp of the most recent sighting."""
    state: str = ""
    """A primitive-defined label, e.g. ``"stationary"``.  Free string; not a wire enum."""
    attributes: Mapping[str, Scalar] = field(default_factory=dict)
    """Extra per-track scalars, e.g. ``{"speed_px_s": 12.4}``."""

    def __post_init__(self) -> None:
        object.__setattr__(self, "attributes", MappingProxyType(dict(self.attributes)))

    @property
    def duration_seconds(self) -> float:
        """How long this track has been observed, in frame time."""
        return max(0.0, self.last_seen - self.first_seen)


@dataclass(frozen=True, slots=True)
class PrimitiveEvent:
    """An **incident candidate** -- something happened, at a frame time.

    Deliberately not an incident: severity here is a free string and the runtime maps it
    through :func:`matrice_analytics.engine.contract.schemas.parse_severity` on the way to
    the wire.  A primitive that imported the wire ``Severity`` enum would know the wire
    format, and then so would the next one (**O1**).

    Incident *lifecycle* -- confirmation frames, find-or-create on ``incident_id``,
    up-only escalation, closing -- belongs to the runtime, not here.  A primitive says
    "this is happening now"; nothing more.
    """

    kind: str
    """The incident type key, matching ``incidents.types[].key`` in the manifest."""
    ts: float
    """Frame timestamp of the event (**PY-13**)."""
    severity: str = ""
    """``info|low|medium|high|critical``, or ``""`` to let the manifest decide.

    Also accepts the internal ``"significant"``, which the runtime maps to ``high``
    (**FROZEN-7**) -- it must never reach the wire.
    """
    zone: str = GLOBAL_ZONE
    track_id: int | None = None
    values: Mapping[str, Scalar] = field(default_factory=dict)
    """Context for ``human_text``'s ``{key}`` interpolation."""

    def __post_init__(self) -> None:
        if not self.kind.strip():
            raise ValueError(
                "PrimitiveEvent.kind must be non-empty; it is joined to incidents.types[].key by exact string match"
            )
        object.__setattr__(self, "values", _freeze_values(self.values, "PrimitiveEvent"))


def _freeze_values(values: Mapping[str, Any], where: str) -> Mapping[str, Scalar]:
    """Validate and freeze a ``values`` mapping.

    Rejects the three things that turn into a bad row rather than an error downstream:
    a non-string key, ``None`` (the classic "the metric reads zero forever"), and a
    non-scalar.  ``bool`` is coerced to ``int`` because the contract rejects a bool where a
    number is declared (Section 1 rule 6) while primitives such as ``state_machine``
    legitimately publish an ``active`` flag.
    """
    cleaned: dict[str, Scalar] = {}
    for key, value in values.items():
        if not isinstance(key, str) or not key.strip():
            raise PrimitiveValueError(
                f"{where}.values has a non-string or empty key ({key!r}); keys are what "
                "metrics[].source resolves against"
            )
        if value is None:
            raise PrimitiveValueError(
                f"{where}.values[{key!r}] is None. Publish the number you mean -- 0.0 for "
                "'nothing happened' -- or omit the key so the unresolved source is an "
                "error (09 §3) rather than a metric that reads zero forever."
            )
        if isinstance(value, bool):
            cleaned[key] = int(value)
        elif isinstance(value, (int, float, str)):
            cleaned[key] = value
        else:
            raise PrimitiveValueError(
                f"{where}.values[{key!r}] is a {type(value).__name__}; a values entry must "
                "be a float, int or str because it becomes metrics[].data or an "
                "interpolated human_text field. Put structured state in "
                "PrimitiveOutput.tracks or the StateStore instead."
            )
    return MappingProxyType(cleaned)


@dataclass(frozen=True, slots=True)
class PrimitiveOutput:
    """What one pipeline stage produces for one frame, in one zone (``09`` §3)."""

    values: Mapping[str, Scalar] = field(default_factory=dict)
    """The mapping ``metrics[].source`` resolves against -- the whole coupling surface
    between a primitive and a manifest (``09`` §3).

    ``source: ratio_compliance.compliance_pct`` reads
    ``outputs["ratio_compliance"].values["compliance_pct"]``.  Keys are declared in the
    stage's config model (``PrimitiveConfig.output_names``) so the manifest loader can
    reject an unresolvable source *before* the app runs; ``custom`` is the one stage whose
    keys are only known to the author's Python (``CustomConfig.OPEN_OUTPUTS``).
    """

    tracks: Mapping[int, TrackState] = field(default_factory=dict)
    """Per-track state, keyed by tracker id, for downstream stages to read."""

    events: Sequence[PrimitiveEvent] = ()
    """Incident candidates raised by this frame.  Usually empty."""

    wire_detections: Sequence[PipelineDetection] | None = None
    """Override for this zone's wire-facing detections list, or ``None`` for "no override".

    ``session.py``'s frame result (S3) normally publishes the zone's admitted detections
    as-is, each carrying the model's raw ``category``. A stage that needs the wire to show a
    filtered or relabeled view -- e.g. ``line_crossing``'s ``expose_corridor_state``, which
    shows only tracks currently between its two lines, categorized ``in``/``out`` instead of
    the model's class -- sets this instead of touching ``ctx.detections`` (frozen) or the
    contract's ``Detection.category`` default (which stays the model label everywhere else,
    deliberately -- it is what the overlay draws). ``None`` is the default for every other
    stage, and means "publish the zone's normal detections, unchanged". If more than one
    stage in a zone sets this on the same frame, the runtime uses the last one in pipeline
    order and logs a warning -- an app should have at most one opinion about what the wire's
    detections list looks like.
    """

    def __post_init__(self) -> None:
        object.__setattr__(self, "values", _freeze_values(self.values, "PrimitiveOutput"))
        object.__setattr__(self, "tracks", MappingProxyType(dict(self.tracks)))
        object.__setattr__(self, "events", tuple(self.events))
        if self.wire_detections is not None:
            object.__setattr__(self, "wire_detections", tuple(self.wire_detections))


@dataclass(frozen=True, slots=True)
class WindowOutput:
    """What one stage contributes to the 60-second aggregation (``09`` §3).

    Separate from :class:`PrimitiveOutput` because it means something different: these
    values are already collapsed over the window and are published once, whereas a
    ``PrimitiveOutput.values`` entry is a per-frame sample that ``metrics[].agg_type`` still
    has to collapse.  Conflating the two is how a percentage gets published as a
    60-second *sum* (**PY-1**).

    There are no ``tracks`` here: a track is a per-frame fact, and the window is over.
    """

    values: Mapping[str, Scalar] = field(default_factory=dict)
    events: Sequence[PrimitiveEvent] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "values", _freeze_values(self.values, "WindowOutput"))
        object.__setattr__(self, "events", tuple(self.events))


def resolve_value(outputs: Mapping[str, PrimitiveOutput], source: str) -> Scalar:
    """Resolve a ``metrics[].source`` against a frame's stage outputs.

    ``<stage>.<value>``, where ``<value>`` may itself contain dots
    (``detect.person.count`` is stage ``detect``, value ``person.count``).

    Args:
        outputs: Stage name -> that stage's output, i.e. what
            :attr:`FrameContext.previous` holds.
        source: The manifest source string.

    Returns:
        The scalar the manifest asked for.

    Raises:
        SourceResolutionError: The stage or the value is missing.  ``09`` §3: *an
            unresolvable source is a manifest load error -- not a metric that reads zero
            forever*.  The message names what *is* available, because the usual cause is a
            one-character typo in ``app.yaml``.
    """
    stage, _, value_name = source.partition(".")
    if not stage or not value_name:
        raise SourceResolutionError(f"source {source!r} is not '<stage>.<value>', e.g. 'unique_count.new'")
    if stage not in outputs:
        raise SourceResolutionError(
            f"source {source!r} names stage {stage!r}, which is not in the pipeline. "
            f"Stages present: {', '.join(sorted(outputs)) or '(none)'}."
        )
    values = outputs[stage].values
    if value_name not in values:
        raise SourceResolutionError(
            f"source {source!r}: stage {stage!r} published no value named {value_name!r}. "
            f"It published: {', '.join(sorted(values)) or '(nothing)'}."
        )
    return values[value_name]


# ---------------------------------------------------------------------------
# The interface
# ---------------------------------------------------------------------------


@runtime_checkable
class Primitive(Protocol):
    """The one interface (``09`` §3).  A protocol, so there is nothing to inherit.

    An implementation is any class with these members -- no registration in a base class,
    no ``super().__init__()``, no ``BaseProcessor``.  That is the point: the ~20 payload
    helpers and their duplicate deprecated twins accumulated on
    ``core/base.py:617-781`` *because* there was somewhere shared to put them.

    Implementations are pure over ``(detections, state, config)``: given the same frames
    and the same starting state they produce the same outputs, which is what makes the
    generated determinism test (**O5**) meaningful.

    Note:
        ``isinstance(obj, Primitive)`` checks only that the members exist -- that is all a
        ``runtime_checkable`` protocol can do.  Use :func:`conformance_problems` when you
        want the *reasons* something does not conform.
    """

    name: ClassVar[str]
    """The manifest primitive key, e.g. ``"zone_occupancy"``.  Must be in
    :data:`matrice_analytics.engine.manifest.models.PRIMITIVES`."""

    Config: ClassVar[type[BaseModel]]
    """The Pydantic config model for this primitive, i.e. its entry in
    ``manifest.models``.  Validation happens at manifest load, so a typo in ``app.yaml``
    fails at startup instead of three hours later as a ``KeyError``."""

    def __init__(self, config: BaseModel, state: StateStore) -> None:
        """Construct with a validated config and an already-scoped state store.

        The store is scoped to ``<camera_id>/<app_id>/<zone>/<primitive>`` by the runtime,
        so an implementation writes bare names (``state.set("seen", ...)``) and cannot
        collide with another camera, app, zone or stage.

        **All** mutable state goes through ``state``.  A plain ``self._counts`` dict is a
        review defect: it is invisible to a future Redis backing (``09`` §4, **D6**).
        """
        ...

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Handle one frame, in one zone.  No I/O, no threads, no models (``09`` §6)."""
        ...

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Collapse this stage's per-frame outputs into the 60-second aggregation.

        Given the outputs this same instance returned from :meth:`process` during the
        window, in frame order.
        """
        ...

    def reset(self) -> None:
        """Clear window-scoped state at the aggregation boundary.

        **Not** a full reset.  ``09`` §4 rule 2: window sums clear here; cumulative totals
        clear only when the process does (**FROZEN-4**).  Implementations express this by
        calling :meth:`~matrice_analytics.engine.state.store.StateStore.end_window`, or by
        clearing named keys -- what they must not do is clear a total, because the
        backend's rollup formula assumes those only reset on restart.
        """
        ...


@runtime_checkable
class CustomPrimitive(Protocol):
    """A full pipeline stage written by an app author (``09`` §6).

    Narrower than :class:`Primitive` on purpose: no ``name`` (the manifest stage supplies
    it) and no ``window`` (the runtime aggregates the ``values`` a custom stage publishes,
    using each metric's ``agg_type``).  ``reset`` is optional; the runtime calls it if it
    is there.

    The loader enforces exactly ``Config`` + ``process``
    (``manifest/loader.py:_resolve_custom_impl``), so this protocol and that check must
    stay in step.

    Custom code must not touch the wire format, re-implement a primitive, do network I/O,
    load a model, or spawn a thread -- each is a current pathology with a name in
    ``12-defect-register.md`` (**PY-15** for the last one).
    """

    Config: ClassVar[type[BaseModel]]

    def __init__(self, config: BaseModel, state: StateStore) -> None: ...

    def process(self, ctx: FrameContext) -> PrimitiveOutput: ...


_PRIMITIVE_MEMBERS: tuple[str, ...] = ("name", "Config", "process", "window", "reset")


def conformance_problems(impl: type[Any], *, custom: bool = False) -> list[str]:
    """Explain why ``impl`` is not a conforming primitive, or return ``[]``.

    ``isinstance(x, Primitive)`` answers yes/no; this answers "which member is missing and
    what should its signature be", which is what an app author or a reviewer actually
    needs.  Used by :meth:`PrimitiveRegistry.register` so a bad implementation fails at
    import time rather than on the first frame.

    Args:
        impl: The candidate class.
        custom: Check against :class:`CustomPrimitive` (``Config`` + ``process``) rather
            than the full :class:`Primitive`.

    Returns:
        A list of human-readable problems, empty when ``impl`` conforms.
    """
    problems: list[str] = []
    if not isinstance(impl, type):
        return [f"{impl!r} is a {type(impl).__name__}, not a class"]

    required = ("Config", "process") if custom else _PRIMITIVE_MEMBERS
    for member in required:
        if getattr(impl, member, None) is None:
            problems.append(
                f"{impl.__name__} has no {member!r}. "
                + {
                    "name": "Set `name: ClassVar[str]` to the manifest primitive key.",
                    "Config": "Set `Config = <a pydantic BaseModel>` so app.yaml is "
                    "validated at load time, not as a KeyError mid-stream.",
                    "process": "Implement `process(self, ctx: FrameContext) -> PrimitiveOutput`.",
                    "window": "Implement `window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput`.",
                    "reset": "Implement `reset(self) -> None`; it clears WINDOW state only (09 §4 rule 2).",
                }[member]
            )

    config_model = getattr(impl, "Config", None)
    if config_model is not None and not (isinstance(config_model, type) and issubclass(config_model, BaseModel)):
        problems.append(f"{impl.__name__}.Config must be a pydantic BaseModel subclass, got {config_model!r}")

    if not custom:
        stated = getattr(impl, "name", None)
        if stated is not None and (not isinstance(stated, str) or not stated.strip()):
            problems.append(f"{impl.__name__}.name must be a non-empty string, got {stated!r}")

    for member in ("process", "window", "reset"):
        candidate = getattr(impl, member, None)
        if candidate is not None and not callable(candidate):
            problems.append(f"{impl.__name__}.{member} is not callable")

    init = getattr(impl, "__init__", None)
    if callable(init) and init is not object.__init__:
        try:
            parameters = list(inspect.signature(init).parameters)
        except (TypeError, ValueError):  # pragma: no cover - C-level __init__
            parameters = []
        if parameters[1:3] not in ([], ["config", "state"]):
            problems.append(
                f"{impl.__name__}.__init__ takes {parameters[1:]!r}; the runtime calls "
                "`Impl(config, state)`, so the first two parameters must be named "
                "`config` and `state` (09 §3)."
            )
    return problems


# ---------------------------------------------------------------------------
# The registry
# ---------------------------------------------------------------------------


class PrimitiveRegistry:
    """Manifest primitive name -> implementation class.

    This is how the runtime turns a validated manifest into a pipeline without knowing a
    single app's name (``09`` §1): it reads ``pipeline[].kind``, looks the class up here,
    and constructs it with the stage's already-validated config and a scoped state store.

    The key set is closed -- it is
    :data:`matrice_analytics.engine.manifest.models.PRIMITIVES`, the same 17 names the
    manifest schema accepts.  Registering anything else raises, because a primitive no
    manifest can name is dead code and a manifest naming a primitive that is not here must
    fail loudly at load, not silently emit nothing.

    Example:
        >>> registry = PrimitiveRegistry()
        >>> @registry.register
        ... class Detect:
        ...     name = "detect"
        ...     Config = DetectConfig
        ...     def __init__(self, config, state): ...
        ...     def process(self, ctx): return PrimitiveOutput()
        ...     def window(self, frames): return WindowOutput()
        ...     def reset(self): ...
        >>> registry.get("detect") is Detect
        True
    """

    __slots__ = ("_impls",)

    def __init__(self) -> None:
        self._impls: dict[str, type[Primitive]] = {}

    # -- registration -------------------------------------------------------

    def register(self, impl: type[Any] | None = None, *, name: str | None = None) -> Any:
        """Register an implementation.  Usable bare or with an explicit name.

        ``@registry.register`` takes the key from ``cls.name``;
        ``@registry.register(name="detect")`` states it, and then ``cls.name`` must agree
        (two spellings of one key is how the legacy catalogue ended up with two
        registration lists that disagree -- ``09`` §9).

        Args:
            impl: The class, when used as a bare decorator.
            name: The manifest primitive key, when stated explicitly.

        Returns:
            The class (bare form) or a decorator (keyword form).

        Raises:
            PrimitiveRegistrationError: The name is unknown to the manifest schema,
                already taken, disagrees with ``cls.name``, or the class does not conform.
        """

        def decorate(cls: type[Any]) -> type[Any]:
            key = name or getattr(cls, "name", None)
            if not isinstance(key, str) or not key.strip():
                raise PrimitiveRegistrationError(
                    f"{getattr(cls, '__name__', cls)!r} has no primitive name. Set "
                    "`name: ClassVar[str] = '<manifest key>'`, or use "
                    "@register(name='<manifest key>')."
                )
            stated = getattr(cls, "name", None)
            if stated is not None and stated != key:
                raise PrimitiveRegistrationError(
                    f"{cls.__name__} is registered as {key!r} but declares name={stated!r}. "
                    "One primitive, one key: two spellings mean the manifest and the "
                    "registry disagree about which class runs."
                )
            _check_known_primitive(key, cls)
            if key in self._impls and self._impls[key] is not cls:
                raise PrimitiveRegistrationError(
                    f"primitive {key!r} is already registered to "
                    f"{self._impls[key].__name__}; it is implemented ONCE (objective O2)."
                )
            problems = conformance_problems(cls)
            if problems:
                raise PrimitiveRegistrationError(
                    f"{cls.__name__} does not implement the Primitive protocol:\n  - " + "\n  - ".join(problems)
                )
            self._impls[key] = cls
            return cls

        if impl is not None:
            return decorate(impl)
        return decorate

    # -- lookup -------------------------------------------------------------

    def get(self, name: str) -> type[Primitive]:
        """The class registered for ``name``.

        Raises:
            KeyError: Nothing is registered for it.  The message distinguishes "not
                implemented yet" (``08`` §2 marks four primitives 🔜) from "not a
                primitive at all", because the fix differs.
        """
        try:
            return self._impls[name]
        except KeyError:
            known = ", ".join(sorted(self._impls)) or "(none)"
            raise KeyError(
                f"no implementation registered for primitive {name!r}. The manifest "
                f"schema accepts it but the runtime cannot run it yet (08 §2 marks the "
                f"unimplemented ones). Registered: {known}."
            ) from None

    def create(self, name: str, config: BaseModel, state: StateStore) -> Primitive:
        """Instantiate the primitive registered for ``name``.

        Args:
            name: The manifest primitive key.
            config: The stage's validated config, an instance of the class's ``Config``.
            state: A store already scoped to
                ``<camera_id>/<app_id>/<zone>/<primitive>`` (``09`` §4).

        Returns:
            The constructed primitive.

        Raises:
            KeyError: Nothing is registered for ``name``.
            TypeError: ``config`` is not an instance of the class's ``Config`` model.
        """
        impl = self.get(name)
        if not isinstance(config, impl.Config):
            raise TypeError(
                f"primitive {name!r} expects a {impl.Config.__name__} config, got "
                f"{type(config).__name__}. The manifest loader produces the right model; "
                "a mismatch here means the stage was built from the wrong pipeline entry."
            )
        return impl(config, state)

    def names(self) -> tuple[str, ...]:
        """Registered primitive names, sorted -- deterministic for tests and logs."""
        return tuple(sorted(self._impls))

    def missing(self) -> tuple[str, ...]:
        """Manifest primitives with no implementation yet, sorted.

        The runtime's startup check: a manifest naming one of these must fail loudly
        (``09`` §5), and this is the list it fails against.
        """
        return tuple(sorted(set(_manifest_primitive_names()) - set(self._impls)))

    def __contains__(self, name: object) -> bool:
        return name in self._impls

    def __len__(self) -> int:
        return len(self._impls)

    def __repr__(self) -> str:
        return f"PrimitiveRegistry({', '.join(self.names()) or 'empty'})"


def _manifest_primitive_names() -> frozenset[str]:
    """The closed set of manifest primitive keys, or empty if the schema is unavailable.

    Imported lazily and defensively for the same reason
    ``manifest.models._cross_check_contract_vocabulary`` does it: the two packages are
    built independently and neither may hard-fail on the other's absence at import time.
    """
    try:
        from matrice_analytics.engine.manifest.models import PRIMITIVES  # noqa: PLC0415
    except Exception:  # pragma: no cover - sibling package unavailable
        return frozenset()
    return frozenset(PRIMITIVES)


def _check_known_primitive(key: str, cls: type[Any]) -> None:
    """Reject a registration under a name no manifest can declare."""
    known = _manifest_primitive_names()
    if known and key not in known:
        raise PrimitiveRegistrationError(
            f"{cls.__name__} registers primitive {key!r}, which is not in the manifest "
            f"vocabulary. No app.yaml can name it, so it would never run. Legal keys: "
            f"{', '.join(sorted(known))}. If this really is a new primitive, add its "
            f"config model to engine/manifest/models.py first (08 §2)."
        )


REGISTRY = PrimitiveRegistry()
"""The process-wide registry the runtime builds pipelines from.

Tests that need isolation construct their own :class:`PrimitiveRegistry` instead of
mutating this one -- there is deliberately no ``unregister``.
"""


def register(impl: type[Any] | None = None, *, name: str | None = None) -> Any:
    """Register on the default :data:`REGISTRY` (see :meth:`PrimitiveRegistry.register`).

    Example:
        >>> @register
        ... class ZoneOccupancy:
        ...     name = "zone_occupancy"
        ...     Config = ZoneOccupancyConfig
        ...     ...
    """
    return REGISTRY.register(impl, name=name)
