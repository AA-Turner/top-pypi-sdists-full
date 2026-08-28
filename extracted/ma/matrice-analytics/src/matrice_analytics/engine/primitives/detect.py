"""``detect`` -- thresholded class presence and counts, with confidence smoothing.

Normative sources: ``_contracts/08-tobe-primitive-catalogue.md`` §1 (the primitive),
``_contracts/09-tobe-engine-architecture.md`` §3 (the interface) and §4 (state).

``detect`` is the universal first stage: given this frame's detections for one zone, it
publishes how many of each configured entity are present, how many in total, and the best
confidence seen.  Every other primitive in the catalogue is downstream of this one, which
is why it is also the one place the five-field smoothing block is implemented.

**What this stage counts is a level, and a level never reaches ``raw_analytics.count``
(BE-16).**  ``<entity>.count`` is "how many of these are in view", which is the right number
for a ``metrics[]`` entry (``current_occupancy``, ``agg_type: last``) and for the *frame*
surface's ``current_counts``, where be-analytics reads it as the instant-metric
``total_count``.  It is the wrong number for ``results-agg``'s ``current_counts``, which is
an arrival *delta* the backend sums over a five-minute bucket -- summing levels there
publishes several times the true footfall.  Arrivals need identity, so they come from
``unique_count``; this stage deliberately contributes nothing to them.

Four constraints are load-bearing and each has a defect behind it:

**No wall clock** (**PY-13**).  Every timestamp is :attr:`FrameContext.frame_ts`; this
module never imports :mod:`time`.  ``detect`` is frame-indexed rather than time-indexed --
the smoothing window is *N frames*, not *N seconds* -- so a replayed stream smooths
identically to the live run.

**No private state** (``09`` §4 rule 1, **D6**).  The smoothing windows live in the
:class:`~matrice_analytics.engine.state.store.StateStore` under one key holding plain
JSON-shaped data, not in a ``self._windows`` dict.  A ``self.`` dict is invisible to a
future Redis backing and to every test that wants to assert on reset semantics.

**No salted hashing** (**PY-9**).  The legacy smoother identifies an object with
``abs(hash(hash_string))`` (``post_processing/utils/smoothing_utils.py:176``), so the
identity of every smoothed object changes on each process start.  Here the identity is the
track id when there is one and an explicit quantised-box *string* otherwise -- a dict key,
never a salted hash.

Smoothing lifetime is deliberately :attr:`~matrice_analytics.engine.state.store.Lifetime.PERSISTENT`
(``09`` §4 rule 2): a confidence window is a fact about an object that is still in frame,
not a measurement of the 60-second window.  Clearing it on the aggregation boundary would
make every object re-ramp its window at :00 and drop counts once a minute.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, ClassVar

from matrice_analytics.engine.manifest.models import DetectConfig, SmoothingConfig
from matrice_analytics.engine.primitives.base import (
    FrameContext,
    PipelineDetection,
    PrimitiveOutput,
    Scalar,
    WindowOutput,
    register,
)
from matrice_analytics.engine.state import Lifetime, StateStore

__all__ = ["Detect"]


#: State key holding ``{object_key: record}`` for the smoother.  One key, one plain dict,
#: so a durable backing can serialise it without knowing anything about this primitive.
_SMOOTHING_KEY = "smoothing"

#: State key holding the frame counter the smoother ages records against.  Frames, not
#: seconds: :class:`SmoothingConfig` is specified in frames (**PY-13** -- a frame-indexed
#: window replays identically; a wall-clock one does not).
_FRAME_KEY = "frame_index"

#: WINDOW-lifetime peaks, so :meth:`Detect.window` still reports the right numbers when the
#: runtime does not retain every per-frame :class:`PrimitiveOutput`.
_PEAK_TOTAL_KEY = "window_peak_total"
_PEAK_PER_ENTITY_KEY = "window_peak_per_entity"
_PEAK_CONFIDENCE_KEY = "window_max_confidence"

#: WINDOW-lifetime *last* counts -- the value on the most recent frame of the current window.
#: The store rather than ``frames[-1]``: the runtime caps how many per-frame outputs it retains
#: (``runtime/window.py`` stops appending at ``_max_frames``), so on a long window ``frames[-1]``
#: is an *early* frame, not the last one. A peak survives that truncation; a "last" does not.
_LAST_TOTAL_KEY = "window_last_total"
_LAST_PER_ENTITY_KEY = "window_last_per_entity"

#: Grid resolution used to derive a stable identity for an *untracked* detection.
#: Normalized 0-1 space, so 32 cells is ~3% of the frame per cell.  Coarse on purpose: a
#: finer grid gives a moving object a new identity every frame, which empties its window.
_BOX_QUANT = 32


def _quantise(value: float) -> int:
    """Snap a normalized 0-1 coordinate onto the identity grid.

    Deterministic across processes (**PY-9**): plain arithmetic, no ``hash()``.
    """
    return int(round(max(0.0, min(1.0, value)) * _BOX_QUANT))


def _object_key(detection: PipelineDetection) -> str:
    """A stable smoothing identity for one detection.

    A tracker id is the only *correct* identity, so it wins whenever the pipeline has run
    ``track`` first.  Without one, the identity is the entity plus the detection's box
    snapped to a coarse grid -- good enough for a stationary or slow object, and honestly
    weak for a fast one.  That weakness is inherited from the legacy smoother and is the
    reason a manifest that cares about smoothing should place ``track`` before ``detect``.

    Args:
        detection: The detection to identify.

    Returns:
        A key that is identical in every process for identical input (**PY-9**).
    """
    if detection.track_id is not None:
        return f"t:{detection.entity}:{detection.track_id}"
    box = detection.bounding_box
    return (
        f"b:{detection.entity}:{_quantise(box.xmin)}:{_quantise(box.ymin)}:{_quantise(box.xmax)}:{_quantise(box.ymax)}"
    )


class _Smoother:
    """The five-field smoothing block, over a :class:`StateStore`.

    105 of 123 existing configs carry :class:`SmoothingConfig` *identically*
    (``08`` §1), so the defaults matter far more than the flexibility.  Both algorithms
    reduce to "smooth this object's confidence series, then admit it against the
    threshold"; they differ only in the smoother:

    ``window``
        The unweighted mean of the last ``window_size`` confidences -- a direct port of
        ``smoothing_utils._apply_window_smoothing``.

    ``ema``
        An exponential moving average with ``alpha = 2 / (window_size + 1)``, the standard
        span-to-alpha conversion, so ``window_size`` means the same "roughly this many
        frames of memory" in both algorithms.

    Two knobs shape the admit decision rather than the smoother:

    ``confidence_range_factor``
        Hysteresis.  An object must reach ``min_confidence`` to be admitted, but only has
        to hold ``min_confidence * (1 - confidence_range_factor)`` to *stay* admitted.
        This is the legacy "observability" borderline band expressed as a Schmitt trigger,
        and it is what stops a count flickering between 2 and 3 all minute.

    ``cooldown_frames``
        How many frames an unseen object keeps its window before the record is dropped.
        A record in cooldown contributes **no count** -- it only survives a brief detector
        dropout so the object does not have to re-ramp its window from empty.  The legacy
        config declares this field and never reads it
        (``smoothing_utils.py:97,110``: ``object_cooldowns`` is created, cleared and
        counted, never written); this is the behaviour it was declared for.
    """

    __slots__ = ("_config", "_state", "_thresholds")

    def __init__(self, config: SmoothingConfig, thresholds: Mapping[str, float], state: StateStore) -> None:
        """Bind the smoother to a config and the primitive's already-scoped store.

        Args:
            config: The manifest's smoothing block.
            thresholds: Admit threshold **per entity**. Legacy PPE floors ``NO-Hardhat``
                at 0.91 because the class is noisy while everything else sits at 0.50
                (``ppe_compliance.py:220-244``); one scalar cannot express that, and
                smoothing is on by default, so this is the path a PPE app actually takes.
            state: The primitive's state scope.  All smoothing state lives here
                (``09`` §4 rule 1) -- never on ``self``.
        """
        self._config = config
        self._thresholds = thresholds
        self._state = state

    @property
    def _alpha(self) -> float:
        """EMA smoothing factor from the window span."""
        return 2.0 / (float(self._config.window_size) + 1.0)

    def _smooth(self, record: dict[str, Any], confidence: float) -> float:
        """Fold ``confidence`` into ``record`` and return the smoothed value."""
        if self._config.algorithm == "ema":
            previous = record.get("ema")
            value = confidence if previous is None else self._alpha * confidence + (1.0 - self._alpha) * float(previous)
            record["ema"] = value
            return value
        history: list[float] = list(record.get("history", []))
        history.append(confidence)
        if len(history) > self._config.window_size:
            history = history[-self._config.window_size :]
        record["history"] = history
        return sum(history) / float(len(history))

    def admit(self, detections: Sequence[PipelineDetection]) -> tuple[PipelineDetection, ...]:
        """Return the detections that survive smoothing, in input order.

        Args:
            detections: This frame's candidate detections, already restricted to the
                configured entities.

        Returns:
            The admitted subset.  Never a synthesised detection: a smoother that invents
            boxes inflates counts and puts a phantom on the overlay.
        """
        frame_index = int(self._state.get(_FRAME_KEY, 0)) + 1
        self._state.set(_FRAME_KEY, frame_index, lifetime=Lifetime.PERSISTENT)

        records: dict[str, dict[str, Any]] = dict(self._state.get(_SMOOTHING_KEY, {}) or {})
        factor = 1.0 - self._config.confidence_range_factor

        admitted: list[PipelineDetection] = []
        seen: set[str] = set()
        for detection in detections:
            key = _object_key(detection)
            seen.add(key)
            record = records.setdefault(key, {"admitted": False})
            smoothed = self._smooth(record, float(detection.confidence))
            admit = self._thresholds.get(detection.entity, 0.0)
            # Hysteresis is per entity too: a class floored at 0.91 must hold 0.91*(1-f),
            # not the stage's 0.50*(1-f), or the strict floor evaporates on frame two.
            floor = admit * factor if record.get("admitted") else admit
            is_admitted = smoothed >= floor
            record["admitted"] = is_admitted
            record["last_frame"] = frame_index
            if is_admitted:
                admitted.append(detection)

        # Age out records nobody saw this frame; `cooldown_frames` is how long a record
        # survives a detector dropout before its window is thrown away.
        cutoff = frame_index - self._config.cooldown_frames
        self._state.set(
            _SMOOTHING_KEY,
            {
                key: record
                for key, record in records.items()
                if key in seen or int(record.get("last_frame", 0)) >= cutoff
            },
            lifetime=Lifetime.PERSISTENT,
        )
        return tuple(admitted)


@register(name="detect")
class Detect:
    """Thresholded class presence and counts for one zone, one frame.

    Publishes, into :attr:`PrimitiveOutput.values`:

    ``<entity>.count``
        Admitted detections of that entity this frame, one key per
        :attr:`DetectConfig.classes` entry.  Always present, ``0`` when the entity is
        absent -- an omitted key would make ``metrics[].source`` unresolvable and turn a
        quiet camera into a manifest load error (``09`` §3).

    ``total``
        The sum of the per-entity counts.

    ``max_confidence``
        The highest admitted confidence, ``0.0`` when nothing was admitted.

    :meth:`window` publishes the same three names **plus** ``<entity>.count_peak`` and
    ``total_peak``.  The un-suffixed names carry the window's *last-frame* value and the
    suffixed ones its *peak*, because a window output is published as-is and therefore has to
    say which reading it is -- ``agg_type`` cannot choose between them.  See :meth:`window`.

    Example:
        >>> from matrice_analytics.engine.state import InMemoryStateStore
        >>> config = DetectConfig(classes=["person"])
        >>> stage = Detect(config, InMemoryStateStore().for_primitive("c1", "a1", "global", "detect"))
        >>> out = stage.process(ctx)                       # doctest: +SKIP
        >>> out.values["person.count"]                     # doctest: +SKIP
        3
    """

    name: ClassVar[str] = "detect"
    Config: ClassVar[type[DetectConfig]] = DetectConfig

    __slots__ = ("_classes", "_config", "_smoother", "_state", "_thresholds")

    def __init__(self, config: DetectConfig, state: StateStore) -> None:
        """Bind a validated config and an already-scoped state store.

        Args:
            config: The stage's validated :class:`DetectConfig`.
            state: A store scoped to ``<camera_id>/<app_id>/<zone>/<primitive>``
                (``09`` §4).  Every mutable value this primitive owns lives here; there is
                deliberately no ``self._counts`` (**D6**).

        Note:
            ``min_confidence`` defaults to ``0.0`` rather than to a guessed model
            threshold.  ``DetectConfig.min_confidence`` documents itself as an *override*
            of ``model.confidence_threshold``, and a primitive cannot see the model block
            (``09`` §1) -- so with no override the pipeline's own thresholding stands and
            this stage adds none of its own.  Inventing a default here would silently drop
            detections the app asked to keep.
        """
        self._config = config
        self._state = state
        self._classes: tuple[str, ...] = tuple(config.classes)
        base: float = 0.0 if config.min_confidence is None else float(config.min_confidence)
        # Per-entity floors, defaulting to the stage floor. `min_confidence_per_class` is an
        # override of an override: model.confidence_threshold -> min_confidence -> this.
        self._thresholds: dict[str, float] = {
            entity: float(config.min_confidence_per_class.get(entity, base)) for entity in config.classes
        }
        self._smoother = _Smoother(config.smoothing, self._thresholds, state)

    # -- per frame ----------------------------------------------------------

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Count this frame's admitted detections, per entity and in total.

        Args:
            ctx: One frame in one zone.  Detections are already entity-remapped and
                zone-assigned, so this reads :attr:`PipelineDetection.entity` and never the
                model's ``category`` (``09`` §3).

        Returns:
            The per-entity counts, the total and the peak confidence.
        """
        candidates = ctx.of_entity(*self._classes)
        if self._config.smoothing.enabled:
            # The smoother owns the threshold: a detection that dips below it for a frame
            # must still be admitted on the strength of its window, which is the entire
            # point of the block. Pre-filtering here would make the hysteresis unreachable.
            admitted = self._smoother.admit(candidates)
        else:
            admitted = tuple(
                d for d in candidates if float(d.confidence) >= self._thresholds.get(d.entity, 0.0)
            )

        counts: dict[str, int] = dict.fromkeys(self._classes, 0)
        for detection in admitted:
            counts[detection.entity] = counts.get(detection.entity, 0) + 1
        total = len(admitted)
        max_confidence = max((float(d.confidence) for d in admitted), default=0.0)

        self._record_window_readings(counts, total, max_confidence)

        values: dict[str, Scalar] = {f"{entity}.count": counts[entity] for entity in self._classes}
        values["total"] = total
        values["max_confidence"] = max_confidence
        return PrimitiveOutput(values=values)

    def _record_window_readings(
        self, counts: dict[str, int], total: int, max_confidence: float
    ) -> None:
        """Keep the window's peak **and** last readings in WINDOW-lifetime state.

        ``09`` §4 rule 2: these are measurements *of* the current window, so they clear at
        :meth:`reset` and never survive it.  They exist so :meth:`window` still reports the
        truth if the runtime hands it an empty ``frames`` sequence.

        Two readings, not one, because ``metrics[].agg_type`` cannot produce the second: the
        window output is published verbatim, so ``agg_type: last`` and ``agg_type: max`` on one
        source are the same number.  ``<entity>.count`` and ``<entity>.count_peak`` are the two
        numbers an app actually wants -- "how many are in view" and "how many at the worst
        moment" -- under two names.
        """
        self._state.set(
            _PEAK_TOTAL_KEY,
            max(int(self._state.get(_PEAK_TOTAL_KEY, 0)), total),
            lifetime=Lifetime.WINDOW,
        )
        self._state.set(
            _PEAK_CONFIDENCE_KEY,
            max(float(self._state.get(_PEAK_CONFIDENCE_KEY, 0.0)), max_confidence),
            lifetime=Lifetime.WINDOW,
        )
        peaks: dict[str, int] = dict(self._state.get(_PEAK_PER_ENTITY_KEY, {}) or {})
        for entity, count in counts.items():
            peaks[entity] = max(int(peaks.get(entity, 0)), count)
        self._state.set(_PEAK_PER_ENTITY_KEY, peaks, lifetime=Lifetime.WINDOW)

        self._state.set(_LAST_TOTAL_KEY, total, lifetime=Lifetime.WINDOW)
        self._state.set(_LAST_PER_ENTITY_KEY, dict(counts), lifetime=Lifetime.WINDOW)

    # -- per window ---------------------------------------------------------

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Publish **both** readings of the window, under two names each -- never a sum.

        A count is a level, not an event: summing 1,500 per-frame "3 people" samples
        publishes 4,500 people.  Conflating the two is exactly **PY-1**, which is why
        :class:`WindowOutput` is a separate type from :class:`PrimitiveOutput` in the first
        place.

        The peak is not the *only* honest collapse of a level, though, and pretending it was
        is a defect of its own.  A :class:`WindowOutput` is published verbatim -- the runtime
        does not re-apply ``metrics[].agg_type`` to a registered primitive, deliberately -- so
        while this method published one number per name, a manifest asking for
        ``current_occupancy`` (``agg_type: last``) and ``peak_occupancy`` (``agg_type: max``)
        off the same source got the *peak* twice and ``current_occupancy`` was simply wrong.
        The rule is: **a stage's window value is what it is; if you need two readings, publish
        two names.**  So:

        ``<entity>.count`` / ``total``
            The value on the window's **last** frame -- "how many are in view now", which is
            what ``agg_type: last`` means.
        ``<entity>.count_peak`` / ``total_peak``
            The window's **high-water mark** -- "how many at the busiest moment", which is what
            ``agg_type: max`` means.
        ``max_confidence``
            The window maximum.  One name, one reading: it is already declared as a maximum, and
            the confidence on an arbitrary last frame answers no question.

        Args:
            frames: This stage's per-frame outputs for the window, in frame order.  Folded into
                the *peaks* so those are right whether or not the runtime retained them; the
                last readings come from the store only, because retention is capped and
                ``frames[-1]`` is therefore not reliably the window's last frame.

        Returns:
            The last and peak per-entity counts, the last and peak totals, and the peak
            confidence.
        """
        peaks: dict[str, int] = {
            entity: int(count) for entity, count in (self._state.get(_PEAK_PER_ENTITY_KEY, {}) or {}).items()
        }
        peak_total = int(self._state.get(_PEAK_TOTAL_KEY, 0))
        max_confidence = float(self._state.get(_PEAK_CONFIDENCE_KEY, 0.0))

        for frame in frames:
            peak_total = max(peak_total, int(_number(frame.values.get("total", 0))))
            max_confidence = max(max_confidence, float(_number(frame.values.get("max_confidence", 0.0))))
            for entity in self._classes:
                observed = int(_number(frame.values.get(f"{entity}.count", 0)))
                peaks[entity] = max(int(peaks.get(entity, 0)), observed)

        last: dict[str, int] = {
            entity: int(count) for entity, count in (self._state.get(_LAST_PER_ENTITY_KEY, {}) or {}).items()
        }
        last_total = int(self._state.get(_LAST_TOTAL_KEY, 0))

        values: dict[str, Scalar] = {}
        for entity in self._classes:
            values[f"{entity}.count"] = int(last.get(entity, 0))
            values[f"{entity}.count_peak"] = int(peaks.get(entity, 0))
        values["total"] = last_total
        values["total_peak"] = peak_total
        values["max_confidence"] = max_confidence
        return WindowOutput(values=values)

    def reset(self) -> None:
        """Clear the window peaks at the aggregation boundary -- and nothing else.

        ``09`` §4 rule 2 in one line: :meth:`StateStore.end_window` drops every
        :attr:`Lifetime.WINDOW` key and leaves the
        :attr:`Lifetime.PERSISTENT` smoothing windows alone.  Clearing those would make
        every object in frame re-ramp its confidence window once a minute, which reads
        downstream as a count that dips at :00 -- a wrong number that looks like flaky
        analytics rather than like a bug.
        """
        self._state.end_window()


def _number(value: object) -> float:
    """Read a ``values`` entry as a number, treating a non-numeric one as absent.

    ``values`` is typed :data:`Scalar`, which admits ``str``.  ``detect`` never publishes
    one, but :meth:`Detect.window` is handed whatever the runtime collected, and a
    ``TypeError`` at the aggregation boundary would lose the whole window.
    """
    if isinstance(value, bool):
        return float(int(value))
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0
