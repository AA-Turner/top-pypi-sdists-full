"""``segmentation_area`` -- how much of the frame a set of masks covers.

Normative sources: ``_contracts/08-tobe-primitive-catalogue.md`` §2 (the vocabulary entry) and
``_migration/wave-d1/group4-missing/PRIMITIVE_SPECS.md`` §1, which was written against the
legacy code rather than against the plan.  It replaces ``_calculate_mask_area_percentage``,
byte-identical in ``landslide_detection.py:251-315`` and ``flood_detection.py:253-317``.

**The mask carries its own denominator, so this primitive needs nothing from the frame.**
The wire mask is base64 ``simple_rle`` plus ``size = [height, width]`` in model input space
(``_contracts/04-asis-live-frame-contract.md:657-671``), so the covered fraction is *a sum of
alternate run lengths divided by ``h * w``*: ``base64.b64decode`` and ``int.from_bytes`` over
4-byte chunks, ``O(runs)``, **no numpy, no cv2** (**PY-20**) and no
:meth:`~.base.FrameContext.require_resolution`.  That is also the choice legacy Tier 1 made
(``landslide_detection.py:285-291``): dividing by the mask's own array area rather than by the
frame's makes the result independent of the camera's resolution, which matters because a mask
covers the whole frame in model space and YOLO emits masks at the model's internal resolution
unless ``retina_masks`` is set.

Four corrections to the legacy cascade, each of which changed a number:

**The reducer is a config field.**  ``landslide_detection`` **sums** over detections
(``:362``, ``:1329``) and ``flood_detection`` takes the **max**
(``flood_detection.py:1059-1063``).  That is the only behavioural difference between the two
apps and the current config model cannot express it at all, so one of them had to be wrong.
The default is ``max``: a sum double-counts overlapping masks, which is how
``total_landslide_area_pct`` legitimately reaches 120 %.

**Units are a fraction in 0-1, never percent.**  Legacy publishes 0-100
(``landslide_detection.py:277-278``) while every other area quantity in this engine is a
fraction -- ``incident_quantise.threshold_area`` is validated ``le=1.0`` and
``_check_threshold_area`` raises on a pixel² value.  Publishing percent here would put the
engine's two area scales at odds and make ``source: segmentation_area.area_ratio`` unusable as
a quantiser input.  A dashboard that wants percent sets ``unit: percent`` on the metric; the
conversion belongs at emit, once.

**A missing mask is a choice, not a silent substitution.**  Legacy Tier 3
(``landslide_detection.py:307-313``) returns *bounding-box coverage as if it were mask
coverage*, with no flag and no log, so a mask-pipeline outage is invisible on a segmentation
app.  Here it is :attr:`SegmentationArea.on_missing_mask`, it defaults to ``error``, and
``measured_count`` publishes how many detections actually carried a mask so that the
substitution is visible even when it is chosen.

**Nothing here is temporal.**  Legacy hard-codes a per-episode rolling max
(``landslide_detection.py:424``) and a 60-second incident cooldown (``:427``); neither is a
config field and neither belongs to this primitive.  Hysteresis is ``state_machine``, cooldown
is the incident lifecycle, and severity is ``incident_quantise`` or a manifest
``severity_from``.  There is no clock call in this module and no per-track state.
"""

from __future__ import annotations

import base64
import binascii
import logging
from collections.abc import Sequence
from typing import ClassVar, Final, NamedTuple

from matrice_analytics.engine.manifest.models import SegmentationAreaConfig
from matrice_analytics.engine.primitives.base import (
    FrameContext,
    MaskRef,
    PipelineDetection,
    PrimitiveOutput,
    PrimitiveValueError,
    Scalar,
    WindowOutput,
    register,
)
from matrice_analytics.engine.state import Lifetime, StateStore

__all__ = [
    "SIMPLE_RLE",
    "MaskMeasurement",
    "SegmentationArea",
    "decode_simple_rle_area",
    "measure_mask",
    "polygon_area",
]

logger = logging.getLogger(__name__)

SIMPLE_RLE: Final[str] = "simple_rle"
"""The one mask encoding this module can decode (contract ``04`` §5.1).

Anything else is refused rather than decoded anyway.  COCO's *compressed* RLE uses the same
``counts`` key with an LEB128-style byte stream, so reading it as little-endian uint32 run
lengths would publish a plausible and wrong area -- the failure class this engine exists to
remove.
"""

_UINT32: Final[int] = 4
"""Bytes per run length in ``simple_rle``."""

#: WINDOW keys.  Two names for the two readings of one level (**PY-1**): the window's last
#: frame and its high-water mark.  A ``WindowOutput`` is published verbatim, so ``agg_type``
#: cannot turn one name into both.
_LAST_RATIO = "last_area_ratio"
_PEAK_RATIO = "peak_area_ratio"
_PEAK_INSTANCE_RATIO = "peak_max_area_ratio"
_LAST_INSTANCES = "last_instance_count"
_LAST_MEASURED = "last_measured_count"
_WINDOW_FRAMES = "frames_in_window"

#: Defaults for the three fields ``PRIMITIVE_SPECS.md`` §1.2 adds to ``SegmentationAreaConfig``
#: but which are not on the model yet.  Read with ``getattr`` **once, in the constructor**, so
#: this primitive picks the fields up the moment they land and behaves per the spec until then.
#: This is deliberately not the legacy pattern it looks like: ``proximity_detection.py:2154``
#: reads ``self._proximity_iou_duplicate_threshold`` per call with a default it never assigns,
#: which turned a documented knob into a hidden constant.  These three are named, defaulted
#: here, and reported as a schema correction -- delete them when the model carries them.
_DEFAULT_REDUCE: Final[str] = "max"
_DEFAULT_CLAMP: Final[bool] = True
_DEFAULT_ON_MISSING_MASK: Final[str] = "error"


class MaskMeasurement(NamedTuple):
    """One detection's mask, measured.

    A named triple rather than three parallel lists, because the three travel together and
    :attr:`measured` is what separates "0 % coverage" from "no mask at all" -- exactly the
    distinction legacy loses when Tier 3 substitutes the bounding box.
    """

    ratio: float
    """Covered fraction of the mask's own space, ``0-1``."""

    area_px: int
    """Foreground pixels in that space, or ``0`` when the ratio did not come from a pixel
    count (a normalized polygon, or a bounding-box proxy)."""

    measured: bool
    """Whether a real mask produced this.  ``False`` for a bounding-box proxy and for the
    ``zero`` policy, which is what ``measured_count`` reports."""


def decode_simple_rle_area(counts: str) -> int:
    """Foreground pixel count from a base64 ``simple_rle`` run-length string.

    The decoded bytes are little-endian ``uint32`` run lengths that alternate
    background/foreground **starting with background**, laid out row-major over the mask's
    ``size`` (contract ``04`` §5.1).  The foreground area is therefore the sum of the runs at
    **odd** indices -- no allocation of the mask itself, no numpy, ``O(runs)``.

    Args:
        counts: The base64 ``counts`` string as the producer sends it.

    Returns:
        Total foreground pixels.  ``0`` for an empty string, which is a legitimate
        "nothing segmented" rather than an error.

    Raises:
        ValueError: The string is not base64, or its decoded length is not a multiple of 4.
            Both mean the payload is not what it claims to be, and a truncated final run
            would silently under-report the area.

    Example:
        >>> import base64, struct
        >>> counts = base64.b64encode(struct.pack("<4I", 2, 3, 4, 7)).decode()
        >>> decode_simple_rle_area(counts)  # 3 + 7 foreground pixels
        10
    """
    if not counts:
        return 0
    try:
        raw = base64.b64decode(counts, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError(
            f"segmentation mask counts is not valid base64 ({exc}). The wire contract "
            "(04 §5.1) says counts is base64 of little-endian uint32 run lengths; a "
            "non-base64 value means the producer sent a different encoding under the "
            "simple_rle name."
        ) from exc
    if len(raw) % _UINT32:
        raise ValueError(
            f"segmentation mask decodes to {len(raw)} bytes, which is not a multiple of "
            f"{_UINT32}. simple_rle is a sequence of little-endian uint32 run lengths, so a "
            "partial trailing run means the payload is truncated -- decoding it anyway would "
            "under-report the area with no error."
        )
    # Odd indices are the foreground runs: the sequence starts on background.
    return sum(
        int.from_bytes(raw[offset : offset + _UINT32], "little")
        for offset in range(_UINT32, len(raw), 2 * _UINT32)
    )


def polygon_area(points: Sequence[Sequence[float]]) -> float:
    """Unsigned area of a simple polygon, by the shoelace formula.

    ``cv2.contourArea`` returns exactly this for a simple (non-self-intersecting) contour, so
    replacing the legacy call (``landslide_detection.py:302``) with 4 lines of stdlib is
    behaviour-preserving rather than an approximation -- and it removes a cv2 import from a
    module the engine is forbidden to have one in (**PY-20**).

    Args:
        points: ``[(x, y), ...]`` vertices, in either winding order, in any one unit.

    Returns:
        The area in that unit squared; ``0.0`` for fewer than three vertices, which is a
        degenerate contour and not an error.
    """
    if len(points) < 3:
        return 0.0
    total = 0.0
    previous = points[-1]
    for point in points:
        total += previous[0] * point[1] - point[0] * previous[1]
        previous = point
    return abs(total) * 0.5


def measure_mask(mask: MaskRef | None) -> MaskMeasurement | None:
    """Measure one mask, or return ``None`` when it carries nothing usable.

    The three-tier cascade of ``landslide_detection.py:283-313``, minus its silent tiers:
    a pre-computed :attr:`~.base.MaskRef.area_px`, then :attr:`~.base.MaskRef.rle`, then
    :attr:`~.base.MaskRef.polygon`.  The denominator is always the mask's own
    :attr:`~.base.MaskRef.size`, which is the correction to legacy's Tier 2 -- that tier
    divides a polygon area by the *frame* area while Tier 1 divides by the mask's, so the two
    tiers of one function publish two different quantities under one name.

    A polygon with no ``size`` is treated as already normalized 0-1, because that is the only
    other coordinate space this engine has.

    Returns:
        The measurement, or ``None`` when there is no mask, no usable size, or no carrier.
        ``None`` is what :attr:`SegmentationArea.on_missing_mask` then decides about -- it is
        never quietly turned into ``0.0``.

    Raises:
        ValueError: The mask claims an encoding this module cannot decode, or its ``rle`` is
            malformed.  Loud, because a mis-decoded mask is a plausible wrong number.
    """
    if mask is None:
        return None
    denominator = 0.0
    if mask.size is not None:
        height, width = mask.size
        denominator = float(height) * float(width)

    if mask.area_px is not None and denominator > 0.0:
        return MaskMeasurement(min(1.0, mask.area_px / denominator), int(mask.area_px), True)

    if mask.rle:
        if mask.encoding != SIMPLE_RLE:
            raise ValueError(
                f"segmentation mask encoding {mask.encoding!r} is not {SIMPLE_RLE!r}, and "
                "this primitive decodes no other. COCO compressed RLE ships under the same "
                "'counts' key with a byte-packed stream, so decoding it as uint32 run "
                "lengths would publish a wrong area silently. Have the producer send "
                "simple_rle, or an area_pixels count."
            )
        area_px = decode_simple_rle_area(mask.rle)
        if denominator <= 0.0:
            raise ValueError(
                "segmentation mask carries run lengths but no size, so there is no "
                "denominator for the coverage fraction. size is [height, width] in model "
                "input space (contract 04 §5.1) and the mask cannot be normalized without "
                "it -- the frame resolution is deliberately not a substitute, because a mask "
                "is emitted in the model's space and not the camera's."
            )
        return MaskMeasurement(min(1.0, area_px / denominator), area_px, True)

    if mask.polygon:
        area = polygon_area(mask.polygon)
        # No size => the polygon is already in normalized 0-1 space, where the frame's area
        # is 1.0 and the shoelace area *is* the fraction.
        scale = denominator if denominator > 0.0 else 1.0
        return MaskMeasurement(min(1.0, area / scale), int(area) if denominator > 0.0 else 0, True)

    return None


@register(name="segmentation_area")
class SegmentationArea:
    """Mask coverage for one zone, one frame -- as a fraction, never a percent.

    Outputs (:attr:`~.base.PrimitiveOutput.values`), each resolvable as ``<stage>.<name>``:

    ``area_ratio``
        The reduced coverage, ``0-1``.  ``max`` of the instances by default, ``sum`` when
        ``reduce: sum`` reproduces ``landslide_detection``'s total.  Clamped to ``1.0``
        unless ``clamp: false``.
    ``max_area_ratio``
        The largest single instance, whatever ``reduce`` is.  Legacy publishes both
        (``max_landslide_area_pct`` ``:1337``, ``total_landslide_area_pct`` ``:1338``) and an
        operator reads them differently: one answers "how big is the biggest slide", the
        other "how much ground is moving".
    ``instance_count``
        Detections of ``classes`` in this zone this frame.
    ``measured_count``
        How many of them carried a real mask.  **``measured_count < instance_count`` is the
        mask-outage signal**, and it exists because legacy's silent bounding-box proxy has
        none: a dead mask stage there publishes plausible coverage forever.
    ``area_px``
        The reduced foreground pixel count in the masks' own space -- a **diagnostic**, not a
        metric.  It is resolution-dependent by construction and only comparable when every
        mask in the frame shares one ``size``; ``area_ratio`` is the number a manifest should
        threshold on.  It is published because the config model declares it today (see the
        schema corrections in this module's port report).

    At window scope (:meth:`window`) ``area_ratio`` is the **last** frame's coverage and
    ``area_ratio_peak`` is the window's high-water mark, because a ``WindowOutput`` is
    published verbatim and one name cannot answer both (**PY-1**).

    Not here, on purpose: severity (that is ``incident_quantise`` or a manifest
    ``severity_from``), smoothing (``state_machine``), cooldown (the incident lifecycle), and
    ``flood_detection``'s *filter* semantics -- a primitive cannot remove a detection from the
    frame the next stage sees, and one that could would be action at a distance.  See the port
    report for that fidelity limit.
    """

    name: ClassVar[str] = "segmentation_area"
    Config: ClassVar[type[SegmentationAreaConfig]] = SegmentationAreaConfig

    __slots__ = ("_clamp", "_classes", "_config", "_on_missing_mask", "_reduce", "_state")

    def __init__(self, config: SegmentationAreaConfig, state: StateStore) -> None:
        """Bind a validated config to a state store already scoped to this stage.

        Args:
            config: The validated ``segmentation_area:`` block.
            state: Scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` by the runtime.  The
                window peak lives here rather than in an instance attribute (``09`` §4 rule 1,
                **D6**), which is also why ``__slots__`` leaves no room for one.

        Raises:
            ValueError: ``normalize: none`` -- see the message.  Refused at construction, so
                it is a startup failure (``09`` §5) rather than a metric nobody can use.
        """
        if config.normalize != "frame":
            raise ValueError(
                f"segmentation_area does not support normalize={config.normalize!r}. "
                "'none' would publish a raw pixel² count as the coverage metric, which is "
                "resolution-dependent, not comparable across cameras, and the exact value "
                "incident_quantise._check_threshold_area exists to reject. Coverage is "
                "always a fraction of the mask's own space; the raw pixel count is published "
                "alongside it as the diagnostic 'area_px'. Drop the field from the manifest."
            )
        self._config = config
        self._state = state
        self._classes: tuple[str, ...] = tuple(config.classes)
        # Read once, here: see _DEFAULT_* above for why these are getattr and what has to
        # happen to make them plain attribute reads.
        self._reduce: str = str(getattr(config, "reduce", _DEFAULT_REDUCE))
        self._clamp: bool = bool(getattr(config, "clamp", _DEFAULT_CLAMP))
        self._on_missing_mask: str = str(
            getattr(config, "on_missing_mask", _DEFAULT_ON_MISSING_MASK)
        )

    # -- per frame ----------------------------------------------------------

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Measure this zone's masks for one frame.

        Args:
            ctx: The frame.  Only ``detections`` are read -- there is no clock call and no
                :meth:`~.base.FrameContext.require_resolution`, because the masks carry their
                own denominator.

        Returns:
            The five values above.  Never any events: coverage becomes an incident through a
            manifest threshold, which is the runtime's decision (**O1**).

        Raises:
            PrimitiveValueError: A detection of ``classes`` carries no usable mask and
                ``on_missing_mask`` is ``error`` (the default), or a mask is malformed.  A
                mask-free frame on a segmentation app is a broken deployment, and a
                bounding-box proxy for it is plausible and wrong.
        """
        detections = ctx.of_entity(*self._classes)
        measurements = [self._measure(det, ctx) for det in detections]

        ratios = [m.ratio for m in measurements]
        measured = [m for m in measurements if m.measured]
        max_ratio = max(ratios) if ratios else 0.0
        area_ratio = self._reduced(ratios, clamp=self._clamp)
        # clamp=False: ``clamp`` bounds a *fraction* at 1.0, and applying it to a pixel count
        # would publish 1 px for every mask -- a unit confusion of exactly the kind this
        # primitive exists to remove.
        area_px = self._reduced([float(m.area_px) for m in measured], clamp=False)

        self._accumulate(area_ratio, max_ratio, len(detections), len(measured))

        return PrimitiveOutput(
            values={
                "area_ratio": area_ratio,
                "max_area_ratio": max_ratio,
                "instance_count": len(detections),
                "measured_count": len(measured),
                "area_px": int(area_px),
            }
        )

    def _measure(self, det: PipelineDetection, ctx: FrameContext) -> MaskMeasurement:
        """One detection's coverage, applying ``on_missing_mask`` when there is no mask.

        Raises:
            PrimitiveValueError: The mask is unusable and the policy is ``error``, or the mask
                is present and malformed.  :func:`measure_mask` raises a plain ``ValueError``
                for the malformed case; it is re-raised as a
                :class:`~.base.PrimitiveValueError` with the stage and zone attached, because
                "which stage on which camera" is the first thing anybody asks.
        """
        try:
            measurement = measure_mask(det.mask)
        except ValueError as exc:
            raise PrimitiveValueError(
                f"segmentation_area stage {self._config.stage_name!r} cannot measure a "
                f"{det.entity!r} mask in zone {ctx.zone!r} at frame_ts {ctx.frame_ts}: {exc}"
            ) from exc
        if measurement is not None:
            return measurement

        if self._on_missing_mask == "bbox_proxy":
            # Legacy Tier 3, named. Boxes are normalized 0-1, so the box area IS a fraction of
            # the frame -- no resolution needed. measured=False is what makes the substitution
            # visible in measured_count, which legacy has no equivalent of.
            box = det.bounding_box
            width = max(0.0, box.xmax - box.xmin)
            height = max(0.0, box.ymax - box.ymin)
            return MaskMeasurement(min(1.0, width * height), 0, False)
        if self._on_missing_mask == "zero":
            return MaskMeasurement(0.0, 0, False)
        raise PrimitiveValueError(
            f"segmentation_area stage {self._config.stage_name!r} got a {det.entity!r} "
            f"detection with no usable segmentation mask in zone {ctx.zone!r} at frame_ts "
            f"{ctx.frame_ts}. A mask-free frame on a segmentation app means the mask half of "
            "the pipeline is not running, and substituting the bounding box for it -- what "
            "the legacy processor does silently (landslide_detection.py:307-313) -- reports "
            "box coverage as mask coverage forever. Fix the producer, or state the fallback "
            "with on_missing_mask: bbox_proxy (counted in measured_count) or "
            "on_missing_mask: zero."
        )

    def _reduced(self, values: Sequence[float], *, clamp: bool) -> float:
        """Collapse this frame's per-instance values with ``reduce``.

        ``max`` by default: ``sum`` double-counts every pixel two masks share, which is how
        ``total_landslide_area_pct`` exceeds 100 in production.  Legacy clamps each
        *detection* to 100 % and never clamps the sum (``landslide_detection.py:293``), so
        ``clamp`` here clamps the quantity that is actually published -- and only when the
        quantity is a fraction.
        """
        if not values:
            return 0.0
        total = sum(values) if self._reduce == "sum" else max(values)
        return min(1.0, total) if clamp and total > 1.0 else total

    # -- the window ---------------------------------------------------------

    def _accumulate(
        self, area_ratio: float, max_ratio: float, instances: int, measured: int
    ) -> None:
        """Fold this frame into the window, in the state store.

        :attr:`~matrice_analytics.engine.state.Lifetime.WINDOW` throughout: every one of
        these is a measurement *of* the window, and carrying a peak across a boundary reports
        yesterday's landslide as today's (``09`` §4 rule 2).
        """
        self._state.set(_LAST_RATIO, area_ratio, lifetime=Lifetime.WINDOW)
        self._state.set(
            _PEAK_RATIO,
            max(float(self._state.get(_PEAK_RATIO) or 0.0), area_ratio),
            lifetime=Lifetime.WINDOW,
        )
        self._state.set(
            _PEAK_INSTANCE_RATIO,
            max(float(self._state.get(_PEAK_INSTANCE_RATIO) or 0.0), max_ratio),
            lifetime=Lifetime.WINDOW,
        )
        self._state.set(_LAST_INSTANCES, instances, lifetime=Lifetime.WINDOW)
        self._state.set(_LAST_MEASURED, measured, lifetime=Lifetime.WINDOW)
        self._state.incr(_WINDOW_FRAMES, 1, lifetime=Lifetime.WINDOW)

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Collapse the window.  ``area_ratio`` is a level, so it gets **two** names (**PY-1**).

        ``area_ratio`` here is the coverage on the window's **last** frame and
        ``area_ratio_peak`` is the window's **maximum**.  A ``WindowOutput`` is published
        verbatim -- the runtime does not re-apply ``metrics[].agg_type`` to a registered
        primitive -- so a single name would answer one of those questions and answer the other
        one wrongly, in silence.  ``max_area_ratio`` at window scope is the largest single
        instance seen **anywhere in the window**, which is the only reading of a per-frame
        maximum that an operator asks for.

        Args:
            frames: This stage's per-frame outputs for the window, in frame order.  Unused:
                the accumulators in the state store hold the same data already folded, and
                they survive a window whose retained frames were capped
                (``runtime/window.py`` truncates at ``max_frames``, which would silently
                lower a peak computed from this list).

        Returns:
            The five window keys, or an empty output for a window with no frames -- an empty
            aggregation is not a coverage of zero.
        """
        del frames
        if not float(self._state.get(_WINDOW_FRAMES) or 0.0):
            return WindowOutput()
        values: dict[str, Scalar] = {
            "area_ratio": float(self._state.get(_LAST_RATIO) or 0.0),
            "area_ratio_peak": float(self._state.get(_PEAK_RATIO) or 0.0),
            "max_area_ratio": float(self._state.get(_PEAK_INSTANCE_RATIO) or 0.0),
            "instance_count": int(self._state.get(_LAST_INSTANCES) or 0),
            "measured_count": int(self._state.get(_LAST_MEASURED) or 0),
        }
        return WindowOutput(values=values)

    def reset(self) -> None:
        """Clear the window accumulators at the aggregation boundary.

        :meth:`~matrice_analytics.engine.state.store.StateStore.end_window`, not ``clear()``:
        this stage keeps no cumulative total today, and reaching for the full reset is the
        habit that erases one somewhere else (``09`` §4 rule 2, **FROZEN-4**).
        """
        self._state.end_window()
