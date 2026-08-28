"""``incident_quantise`` -- detection magnitude to a severity level.

Normative sources: ``_contracts/08-tobe-primitive-catalogue.md`` §2,
``ml-applications/guidelines/FIELD_REFERENCE.md`` §5.7 and recipe E.  Ported from
``analytics/quant_strategies.py`` (the three strategies, which are correct and are ported
rather than redesigned) and ``analytics/processors/incident.py:53-104``
(``calculate_severity``, the ladder walk).

Two magnitudes, one ladder.  A strategy turns this frame's detections into a
``0..100`` *quant*; the ``levels`` ladder turns the quant into a severity name.  The
interesting decision is not the arithmetic, it is **which strategy** an app picks:

===================  ==========================================  ==================================
Strategy             Use for                                     Because
===================  ==========================================  ==================================
``area_ratio``       fire, smoke, flood, landslide, leaks,        bigger genuinely is worse
                     corrosion
``max_confidence``   weapons, intrusion, PPE violation            one confident detection is
                                                                  critical regardless of size
``count_based``      potholes, litter, defects, crowding          more instances = worse
===================  ==========================================  ==================================

Picking ``area_ratio`` for a weapon app means a pistol held close to the lens outranks one
across the yard; picking ``max_confidence`` for a fire app means a confident wisp of smoke
outranks a wall of flame.  Neither is a bug the code can catch, which is why the table is
reproduced here rather than only in the guide.

**The primitive never touches the wire format** (**PY-3**, objective **O1**).  It raises
:class:`~matrice_analytics.engine.primitives.base.PrimitiveEvent`\\ s -- incident
*candidates* -- and the runtime turns those into ``incident_res`` messages.  There is no
payload building here, no
:class:`~matrice_analytics.engine.contract.schemas.Severity` import, and no incident
lifecycle: confirmation frames, find-or-create on ``incident_id``, up-only escalation and
closing all belong to the runtime.

🔒 **FROZEN-7**: the internal severity name ``significant`` must never reach the wire; the
contract layer maps it to ``high``.  This module cannot produce it -- ``levels[].level`` is
a :data:`~matrice_analytics.engine.manifest.models.SeverityLiteral`, so the manifest
rejects the spelling at load -- and it must stay that way.  :data:`NO_LEVEL` is the only
non-wire string this module publishes, and it is the legacy ``none`` spelling that the
contract already normalises.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar, Final

from matrice_analytics.engine.manifest.models import (
    SEVERITY_LEVELS,
    IncidentQuantiseConfig,
    QuantiseLevel,
)
from matrice_analytics.engine.primitives.base import (
    FrameContext,
    PipelineDetection,
    PrimitiveEvent,
    PrimitiveOutput,
    Scalar,
    WindowOutput,
    register,
)
from matrice_analytics.engine.state import Lifetime, StateStore

__all__ = ["NO_LEVEL", "IncidentQuantise", "level_rank"]


NO_LEVEL: Final[str] = "none"
"""Published as ``level`` when the magnitude reaches no rung of the ladder.

The legacy spelling (``analytics/schemas.py:59``), kept because the contract already
understands it: ``INTERNAL_SEVERITY_ALIASES`` maps ``none`` to ``info``, so a runtime that
passes it to ``parse_severity`` gets a legal wire value rather than a crash.  It is
nevertheless never *meant* to travel: no event is raised at this level, so nothing joins
it to an incident.  ``level_rank`` is ``0`` here, and ``>= 1`` for every real severity.
"""

#: Window peak, so the 60 s summary reports the worst severity seen rather than a
#: meaningless mean of severities.  ``Lifetime.WINDOW`` -- see :meth:`IncidentQuantise.reset`.
_PEAK_RANK = "peak_rank"
_PEAK_LEVEL = "peak_level"


def level_rank(level: str) -> int:
    """Severity as a comparable integer: ``none`` 0, ``info`` 1 ... ``critical`` 5.

    Ranked against the **wire vocabulary**
    (:data:`~matrice_analytics.engine.manifest.models.SEVERITY_LEVELS`), never against the
    position of a rung in ``levels:``.  A config may declare any subset of the ladder in
    either ``order``, so a list-position rank would make ``critical`` outrank ``high`` in
    one app and not in another -- the rank has to mean "how bad", not "how far down the
    YAML".

    Args:
        level: A severity name, or :data:`NO_LEVEL`.

    Returns:
        ``0`` for :data:`NO_LEVEL` or an unknown name, otherwise ``1``-based position in
        ``info, low, medium, high, critical``.
    """
    try:
        return SEVERITY_LEVELS.index(level) + 1
    except ValueError:
        return 0


@register(name="incident_quantise")
class IncidentQuantise:
    """``incident_quantise`` -- magnitude in, severity out.

    Outputs (:attr:`PrimitiveOutput.values`):

    ``level``
        The severity name this frame's magnitude reaches, or :data:`NO_LEVEL`.
    ``level_rank``
        :func:`level_rank` of it -- ``0`` for none, ``5`` for critical.  Publish this, not
        ``level``, to a numeric metric: ``metrics[].data`` is a number and a numeric
        *string* is rejected outright (contract Section 1 rule 6).
    ``area``
        Summed bounding-box area of the quantised detections, as a **fraction of the
        frame** (boxes are normalized 0-1, contract Section 4) -- unless
        :attr:`~matrice_analytics.engine.manifest.models.IncidentQuantiseConfig.area_source` is
        set, in which case this is that stage's ``area_ratio`` (true mask coverage) instead.
    ``confidence``
        Highest detection confidence, ``0-1``.

    Raises one :class:`~matrice_analytics.engine.primitives.base.PrimitiveEvent` per frame
    while the magnitude reaches a rung, and none at :data:`NO_LEVEL`.  An empty frame is
    never an incident: with no detections the strategies would all quantise to ``0``, and a
    ladder with a ``percentage: 0`` rung would then report that rung forever on a camera
    watching an empty room.

    Note:
        The event's ``kind`` is this **stage's name**, not an ``incidents.types[].key``.
        :class:`~matrice_analytics.engine.manifest.models.IncidentQuantiseConfig` carries no
        incident key -- the manifest joins the two the other way round, with
        ``incidents.types[].severity_from: <stage name>`` (``models.py:1891-1903``) -- so
        the stage name is the only identifier this primitive has, and the runtime resolves
        the incident type from it.
    """

    name: ClassVar[str] = "incident_quantise"
    Config: ClassVar[type[IncidentQuantiseConfig]] = IncidentQuantiseConfig

    __slots__ = ("_config", "_kind", "_ladder", "_state")

    def __init__(self, config: IncidentQuantiseConfig, state: StateStore) -> None:
        """Construct from a validated config and an already-scoped state store.

        Args:
            config: The stage's config, validated by the manifest loader.
            state: A store scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` (``09`` §4).

        Raises:
            ValueError: ``strategy: area_ratio`` with a ``threshold_area`` above ``1.0``.
                See :meth:`_quant_area_ratio` -- a pixel² threshold against normalized
                boxes quantises every frame to the bottom of the ladder, and a fire app
                that reports ``low`` during a fire is worse than one that refuses to start.
        """
        if config.strategy == "area_ratio":
            _check_threshold_area(config.threshold_area)
        self._config = config
        self._state = state
        self._kind = config.stage_name
        # Sorted by percentage once, here, rather than per frame: the ladder walk below
        # assumes ascending percentages regardless of the declared `order`, exactly as
        # `calculate_severity` did (`incident.py:74`).
        self._ladder: tuple[QuantiseLevel, ...] = tuple(
            sorted(config.levels, key=lambda rung: rung.percentage)
        )

    # -- per frame ----------------------------------------------------------

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Quantise this zone's detections for one frame.

        Args:
            ctx: The frame's detections, already entity-remapped and zone-assigned.

        Returns:
            The level, its rank, the measured area and the peak confidence, plus one event
            when a rung was reached.

        Note:
            Every detection in the zone is quantised.
            :class:`~matrice_analytics.engine.manifest.models.IncidentQuantiseConfig` has no
            ``classes:`` field, so the narrowing is the *model's* -- recipe E's
            ``detect: {classes: [fire, smoke]}`` documents the intent but does not filter
            what this stage sees.  On a multi-class model that matters; see the workstream
            report.
        """
        detections = ctx.detections
        area = self._area(ctx, detections)
        confidence = _max_confidence(detections)

        if not detections:
            quant = 0.0
            level = NO_LEVEL
        else:
            quant = self._quant(detections, area, confidence)
            level = self._level_for(quant)

        rank = level_rank(level)
        self._record_peak(level, rank)

        values: dict[str, Scalar] = {
            "level": level,
            "level_rank": rank,
            "area": area,
            "confidence": confidence,
        }
        events: tuple[PrimitiveEvent, ...] = ()
        if rank > 0:
            events = (
                PrimitiveEvent(
                    kind=self._kind,
                    ts=ctx.frame_ts,
                    severity=level,
                    zone=ctx.zone,
                    values={
                        "level": level,
                        "level_rank": rank,
                        "quant": quant,
                        "area": area,
                        "confidence": confidence,
                        "count": len(detections),
                    },
                ),
            )
        return PrimitiveOutput(values=values, events=events)

    def _area(self, ctx: FrameContext, detections: Sequence[PipelineDetection]) -> float:
        """This frame's magnitude for ``area_ratio``: a mask stage's reading, or the box sum.

        ``area_source`` names an earlier ``segmentation_area`` stage; ``ctx.previous`` holds
        every stage that ran before this one this frame (``09`` runtime contract), so a stage
        ordered after it in the pipeline is the only requirement -- there is no separate
        wiring. A missing or not-yet-run stage reads as ``0.0`` rather than raising: the same
        "an absent reading is zero, not a crash" contract :meth:`FrameContext.previous` has
        everywhere else, and cheaper than validating pipeline order twice (the loader already
        does at build time via the general stage-reference checks).
        """
        if not self._config.area_source:
            return _total_area(detections)
        upstream = ctx.previous.get(self._config.area_source)
        if upstream is None:
            return 0.0
        return float(upstream.values.get("area_ratio", 0.0) or 0.0)

    # -- the three strategies (ported verbatim in behaviour) ----------------

    def _quant(
        self, detections: Sequence[PipelineDetection], area: float, confidence: float
    ) -> float:
        """Dispatch to the configured strategy.

        No fallback.  ``quant_strategies.compute_quant:131-137`` warned and fell back to
        ``max_confidence`` on an unknown name; here the name is a
        :class:`typing.Literal` on the config, so an unknown one cannot reach this method
        and a silent change of meaning is impossible.
        """
        if self._config.strategy == "area_ratio":
            return self._quant_area_ratio(area)
        if self._config.strategy == "count_based":
            return self._quant_count_based(len(detections))
        return _percent(confidence * 100.0)

    def _quant_area_ratio(self, area: float) -> float:
        """``total_area / threshold_area * 100``, capped at 100.

        ``area`` is a **fraction of the frame**, so ``threshold_area`` is one too:
        ``0.25`` means "a hazard covering a quarter of the frame is a full-scale one".
        The legacy strategy (``quant_strategies.py:50-79``) summed *pixel* areas and
        ``FIELD_REFERENCE`` recipe E still shows ``threshold_area: 250200.0`` from that
        era -- but bounding boxes are normalized 0-1 on this side of the refactor
        (contract Section 4, **BE-10**/**BE-12**) and :class:`FrameContext` carries no
        resolution to convert with.  A pixel² threshold would therefore divide a number
        ``<= 1`` by a number in the hundreds of thousands and pin every frame to the
        bottom rung, so :func:`_check_threshold_area` rejects it at construction instead.
        """
        threshold = self._config.threshold_area or 0.0
        if threshold <= 0:  # pragma: no cover - the config model enforces gt=0
            return 0.0
        return _percent(area / threshold * 100.0)

    def _quant_count_based(self, count: int) -> float:
        """``len(detections) / count_threshold * 100``, capped at 100."""
        threshold = max(1, self._config.count_threshold or 1)
        return _percent(count / threshold * 100.0)

    # -- the ladder ---------------------------------------------------------

    def _level_for(self, quant: float) -> str:
        """Walk the ladder, honouring ``order``.

        Ported from ``incident.py:53-104``, whose two branches mean genuinely different
        things and are easy to mistake for a sort direction:

        ``ascending`` (the default) is a **floor**: the highest rung whose ``percentage``
        the quant has reached.  Below the lowest rung there is no level.

        ``descending`` is a **ceiling**: a quant inside ``[p_i, p_i+1)`` grades to rung
        ``i+1``, i.e. the bracket above, and a quant below the lowest rung takes the
        lowest.  It exists because ladders written top-down in YAML were being read that
        way; the manifest validates the declared ``order`` against the list order, so an
        author cannot get the two out of step (``models.py:938-946``).
        """
        if quant < 0 or not self._ladder:  # pragma: no cover - min_length=1 on the config
            return NO_LEVEL

        if self._config.order == "descending":
            if quant < self._ladder[0].percentage:
                return self._ladder[0].level
            for lower, upper in zip(self._ladder, self._ladder[1:]):
                if lower.percentage <= quant < upper.percentage:
                    return upper.level
            return self._ladder[-1].level

        level = NO_LEVEL
        for rung in self._ladder:
            if quant >= rung.percentage:
                level = rung.level
            else:
                break
        return level

    # -- window -------------------------------------------------------------

    def _record_peak(self, level: str, rank: int) -> None:
        """Remember the worst severity of the current window, in the state store.

        ``Lifetime.WINDOW``: the peak is a measurement *of* this window and carrying it
        into the next one would leave a dashboard stuck at ``critical`` long after the
        fire was out (``09`` §4 rule 2).  In the store rather than a ``self._peak``
        because every piece of primitive state goes through the seam (**D6**).
        """
        if rank <= int(self._state.get(_PEAK_RANK, 0) or 0):
            return
        self._state.set(_PEAK_RANK, rank, lifetime=Lifetime.WINDOW)
        self._state.set(_PEAK_LEVEL, level, lifetime=Lifetime.WINDOW)

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Collapse the window to its worst frame.

        The **peak**, not the mean.  Severity is ordinal: the average of ``critical`` and
        ``none`` is not ``medium``, and publishing a ratio-shaped aggregate of an ordinal
        is the same class of mistake as summing a percentage (**PY-1**).  ``area`` and
        ``confidence`` are the maxima over the window for the same reason -- they are the
        evidence for the peak level.

        No events.  Every candidate was already raised by :meth:`process` at the frame it
        happened on; repeating them here would give the runtime's find-or-create two
        arrivals for one occurrence.

        Args:
            frames: This stage's per-frame outputs for the window, in frame order.
        """
        level = str(self._state.get(_PEAK_LEVEL, NO_LEVEL) or NO_LEVEL)
        rank = int(self._state.get(_PEAK_RANK, 0) or 0)
        area = 0.0
        confidence = 0.0
        for frame in frames:
            area = max(area, float(frame.values.get("area", 0.0) or 0.0))
            confidence = max(confidence, float(frame.values.get("confidence", 0.0) or 0.0))
        return WindowOutput(
            values={
                "level": level,
                "level_rank": rank,
                "area": area,
                "confidence": confidence,
            }
        )

    def reset(self) -> None:
        """Clear the window peak at the aggregation boundary.

        :meth:`~matrice_analytics.engine.state.store.StateStore.end_window`, never
        ``clear()`` -- the distinction is the whole point of
        :class:`~matrice_analytics.engine.state.Lifetime` (``09`` §4 rule 2,
        **FROZEN-4**).
        """
        self._state.end_window()


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _check_threshold_area(threshold_area: float | None) -> None:
    """Reject a pixel² ``threshold_area`` loudly at construction.

    ``09`` §3 in spirit: a magnitude that can never reach the ladder is not a low reading,
    it is a broken app, and it must fail where somebody is watching rather than three
    hours into a stream.
    """
    if threshold_area is None:  # pragma: no cover - the config model requires it
        raise ValueError(
            "incident_quantise.strategy: area_ratio needs threshold_area; it is the "
            "denominator the level percentages are measured against."
        )
    if threshold_area > 1.0:
        raise ValueError(
            f"incident_quantise.threshold_area is {threshold_area}, which is above 1.0. "
            f"Bounding boxes are normalized 0-1 (contract Section 4), so the measured area "
            f"is a fraction of the frame and threshold_area must be one too: write 0.25 for "
            f"'a hazard covering a quarter of the frame is full scale'. A value like "
            f"250200.0 is a pixel-squared threshold from the legacy engine — divide it by "
            f"your source resolution's pixel count (e.g. 250200 / (1920*1080) = 0.121). "
            f"Left as-is, every frame quantises to the bottom of the ladder and the app "
            f"reports the lowest severity during a real incident."
        )


def _percent(value: float) -> float:
    """Clamp a quant to ``0..100``."""
    return min(100.0, max(0.0, value))


def _total_area(detections: Sequence[PipelineDetection]) -> float:
    """Summed bounding-box area as a fraction of the frame.

    Overlapping boxes are counted twice, exactly as the legacy strategy did
    (``quant_strategies.py:59-75``): two half-frame smoke plumes read as a full frame of
    smoke, which is the intended "extent of the hazard" reading.
    """
    total = 0.0
    for detection in detections:
        box = detection.bounding_box
        width = box.xmax - box.xmin
        height = box.ymax - box.ymin
        if width > 0 and height > 0:
            total += width * height
    return total


def _max_confidence(detections: Sequence[PipelineDetection]) -> float:
    """Highest detection confidence, ``0.0`` for an empty frame."""
    return max((detection.confidence for detection in detections), default=0.0)
