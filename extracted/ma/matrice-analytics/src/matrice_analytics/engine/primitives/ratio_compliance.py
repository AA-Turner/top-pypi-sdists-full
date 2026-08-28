"""``ratio_compliance`` -- "what fraction of X satisfies Y".

Normative sources: ``_contracts/08-tobe-primitive-catalogue.md`` §2 (the primitive),
``ml-applications/guidelines/FIELD_REFERENCE.md`` §5.6 (the author-facing contract) and recipes D
and F.  Ported from ``analytics/processors/safety.py`` -- the PPE subject/attribute
association logic -- with two deliberate corrections, both flagged below.

The one primitive behind every compliance app: PPE on a construction site, masks in a
clean room, defects on a production line.  One subject entity is counted, a set of
attribute entities is associated to each subject, and the fraction of subjects that
satisfy the rule is published.

Three things this module is careful about:

**It publishes ``violation_pct``** (``08`` §2 omitted it from the output list even though
``FIELD_REFERENCE`` recipe F sources it as ``defect_rate``).  A manifest written from the
guide would otherwise be a *load error* -- ``metrics[].source`` resolution is strict by
design (``09`` §3), so the omission is not a missing number, it is a dead app.  The
manifest layer already models it
(:attr:`~matrice_analytics.engine.manifest.models.RatioComplianceConfig.STATIC_OUTPUTS`);
this module is what makes the source resolve.

**It never touches the wire format** (**PY-3**, objective **O1**).  There is no severity,
no payload and no import of :mod:`matrice_analytics.engine.contract` here.  Compliance
becomes an incident by a manifest threshold
(``severity_from: {violation_count: {'>': 0}}``), which is the runtime's job, so this
primitive raises no :class:`~matrice_analytics.engine.primitives.base.PrimitiveEvent` at
all.

**All timing is frame timing** (**PY-13**).  There is in fact no timing here -- the
computation is per frame and stateless apart from the window accumulators -- but the
accumulators are keyed through the :class:`~matrice_analytics.engine.state.StateStore`
with an explicit :class:`~matrice_analytics.engine.state.Lifetime` rather than a plain
``self._dict`` (``09`` §4 rule 1, **D6**), so ``reset()`` at the 60 s boundary means
exactly one thing.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import ClassVar

from matrice_analytics.engine.manifest.models import RatioComplianceConfig
from matrice_analytics.engine.primitives.base import (
    FrameContext,
    PipelineDetection,
    PrimitiveOutput,
    Scalar,
    WindowOutput,
    register,
)
from matrice_analytics.engine.state import Lifetime, StateStore

__all__ = ["RatioCompliance", "association_score"]


#: Window accumulator: sum of ``compliance_pct`` over frames that actually had a subject.
_PCT_SUM = "compliance_pct_sum"
#: Window accumulator: how many frames contributed to :data:`_PCT_SUM`.
_PCT_FRAMES = "compliance_pct_frames"


def association_score(subject: PipelineDetection, attribute: PipelineDetection) -> float:
    """How strongly ``attribute`` belongs to ``subject``, in ``0..1``.

    **Intersection over the smaller box**, not intersection over union -- and the config
    field is nevertheless called ``iou_threshold``
    (:class:`~matrice_analytics.engine.manifest.models.RatioComplianceConfig`), which is a
    misnomer inherited from the manifest schema.  The reason for the divergence is
    arithmetic, not taste:

    A person box is roughly ``0.10 x 0.60`` of a normalized frame (area ``0.060``); the
    hardhat on their head is roughly ``0.05 x 0.04`` (area ``0.002``).  Even when the
    hardhat is *entirely inside* the person, true IoU is ``0.002 / 0.060 = 0.033`` -- below
    the documented default ``iou_threshold: 0.1``.  Scoring by IoU would therefore
    associate **nothing** at the default, every subject would read non-compliant, and
    ``compliance_pct`` would be a plausible-looking constant 0.  That is exactly the
    silent-wrong-number failure mode this engine exists to remove (``09`` §3), so the score
    is normalised by the smaller of the two areas, for which a fully-contained attribute
    scores ``1.0``.

    Args:
        subject: The detection being assessed, e.g. a ``person``.
        attribute: The detection that may belong to it, e.g. a ``hardhat``.

    Returns:
        ``intersection / min(area(subject), area(attribute))``, or ``0.0`` when the boxes
        are disjoint or either is degenerate.
    """
    a = subject.bounding_box
    b = attribute.bounding_box
    overlap_w = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    overlap_h = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    if overlap_w <= 0.0 or overlap_h <= 0.0:
        return 0.0
    area_a = (a.xmax - a.xmin) * (a.ymax - a.ymin)
    area_b = (b.xmax - b.xmin) * (b.ymax - b.ymin)
    smaller = min(area_a, area_b)
    if smaller <= 0.0:
        # A zero-area box cannot be "on" anything.  Returning 0.0 rather than dividing is
        # the difference between an unassociated attribute and a ZeroDivisionError three
        # hours into a stream.
        return 0.0
    return min(1.0, (overlap_w * overlap_h) / smaller)


@register(name="ratio_compliance")
class RatioCompliance:
    """``ratio_compliance`` -- fraction of ``subject`` detections satisfying the rule.

    A subject is **compliant** when every entity in ``required`` is associated to it *and*
    no entity in ``violations`` is.  With ``required: []`` (recipe F -- a product is fine
    unless a defect is found on it) the first clause is vacuously true, which is why the
    manifest insists at least one of the two lists is non-empty: with both empty every
    subject is trivially compliant and the app publishes a constant 100.

    Outputs (:attr:`PrimitiveOutput.values`), all resolvable as
    ``<stage>.<name>``:

    ``subject_count``
        Subject detections in this zone, this frame.
    ``compliant_count``
        Subjects satisfying the rule.
    ``violation_count``
        ``subject_count - compliant_count``, **plus** orphan violation-class detections --
        violation boxes that belong to no subject.  Single-stage PPE models emit
        ``no_hardhat`` without a ``person`` box at all, and the legacy processor counted
        those directly (``safety.py:154-177``); dropping them would silently under-report
        the exact thing the app exists to find.
    ``compliance_pct``
        ``compliant_count / subject_count * 100``.
    ``violation_pct``
        ``100 - compliance_pct``.  The one output ``08`` §2 forgot; ``FIELD_REFERENCE``
        recipe F sources it as ``defect_rate``.
    ``<attr>_count``
        One per entity in ``required + violations``: how many of that entity were detected
        in this zone this frame.  The name is the raw entity name, un-sanitised, because
        that is what
        :meth:`~matrice_analytics.engine.manifest.models.RatioComplianceConfig.output_names`
        declares and therefore what a ``metrics[].source`` can name.

    With **no subjects in frame** both percentages are ``0.0``, not ``100``/``0`` and not
    ``0``/``100``.  Nothing was assessed, so neither reading is true, and the pair is
    deliberately not complementary in that one degenerate case: publishing
    ``violation_pct: 100`` for an empty conveyor would make recipe F's ``defect_rate``
    read 100% every night, and publishing ``compliance_pct: 100`` for a dead camera would
    hide an outage behind a perfect score.  ``subject_count`` is what distinguishes
    "assessed and fine" from "nothing to assess" -- read it alongside.
    """

    name: ClassVar[str] = "ratio_compliance"
    Config: ClassVar[type[RatioComplianceConfig]] = RatioComplianceConfig

    __slots__ = ("_attributes", "_config", "_emit", "_required", "_state", "_violations")

    def __init__(self, config: RatioComplianceConfig, state: StateStore) -> None:
        """Construct from a validated config and an already-scoped state store.

        Args:
            config: The stage's config, validated by the manifest loader.
            state: A store scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` (``09`` §4).

        Raises:
            ValueError: ``required`` and ``violations`` are both empty.  The manifest model
                rejects this too, but a config built with ``model_construct`` skips
                validators, and a silently-100% compliance app is worse than a loud
                constructor.
        """
        if not config.required and not config.violations:
            raise ValueError(
                "ratio_compliance declares neither 'required' nor 'violations', so every "
                "subject is trivially compliant and compliance_pct is a constant 100. Give "
                "it at least one required attribute (required: [hardhat]) or one violation "
                "class (violations: [defect])."
            )
        self._config = config
        self._state = state
        self._required: tuple[str, ...] = tuple(config.required)
        self._violations: tuple[str, ...] = tuple(config.violations)
        self._attributes: tuple[str, ...] = self._required + self._violations
        self._emit: frozenset[str] | None = (
            frozenset(config.emit) if config.emit is not None else None
        )

    # -- per frame ----------------------------------------------------------

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Assess this zone's subjects for one frame.

        Args:
            ctx: The frame's detections, already entity-remapped and zone-assigned.

        Returns:
            The compliance values for this frame.  Never any events -- compliance becomes
            an incident through a manifest threshold on ``violation_count``, which is the
            runtime's decision, not this primitive's (**O1**).
        """
        subjects = ctx.of_entity(self._config.subject)
        by_attribute: dict[str, tuple[PipelineDetection, ...]] = {
            attribute: ctx.of_entity(attribute) for attribute in self._attributes
        }
        owner = self._associate(subjects, by_attribute)

        compliant = self._count_compliant(subjects, owner)

        subject_count = len(subjects)
        orphans = self._orphan_violations(by_attribute, owner)
        if subject_count:
            violation_count = (subject_count - compliant) + orphans
            compliance_pct = compliant / subject_count * 100.0
            violation_pct = 100.0 - compliance_pct
        else:
            # Nothing was assessed.  See the class docstring: neither percentage is a
            # truthful reading of an empty frame, so both are 0 and subject_count is what
            # tells the reader why.
            violation_count = orphans
            compliance_pct = 0.0
            violation_pct = 0.0

        self._accumulate(subject_count, compliance_pct)

        values: dict[str, Scalar] = {
            "subject_count": subject_count,
            "compliant_count": compliant,
            "violation_count": violation_count,
            "compliance_pct": compliance_pct,
            "violation_pct": violation_pct,
        }
        for attribute, detections in by_attribute.items():
            values[f"{attribute}_count"] = len(detections)
        return PrimitiveOutput(values=self._selected(values))

    # -- association --------------------------------------------------------

    def _associate(
        self,
        subjects: Sequence[PipelineDetection],
        by_attribute: Mapping[str, Sequence[PipelineDetection]],
    ) -> dict[str, dict[int, set[int]]]:
        """Attach each attribute detection to at most one subject.

        Two deployment shapes have to work off one rule (``safety.py`` docstring):

        *Two-stage* -- a person detector plus a PPE model run on the person crop.  The
        harness gives every PPE box the person's ``track_id``, so the association is
        already stated and geometry would only add noise.

        *Single-stage* -- one model emitting ``person`` and ``no_hardhat`` boxes on the
        full frame.  Nothing states the association, so it is geometric.

        The rule: a shared, non-``None`` ``track_id`` wins, **but only if the boxes
        actually overlap at all**.  Some vendored trackers number ids per class, so a
        ``hardhat`` and an unrelated ``person`` can both be track 1; requiring a non-zero
        overlap costs nothing in the two-stage case (worn PPE always overlaps its wearer)
        and blocks that false pairing.  Otherwise the best
        :func:`association_score` above ``iou_threshold`` wins, ties going to the
        earlier subject so the result does not depend on iteration luck.

        Returns:
            ``{attribute_entity: {subject_index: {attribute_index, ...}}}``.
        """
        threshold = self._config.iou_threshold
        result: dict[str, dict[int, set[int]]] = {}
        for attribute, detections in by_attribute.items():
            owned: dict[int, set[int]] = {}
            for attribute_index, detection in enumerate(detections):
                best_subject = -1
                best_score = 0.0
                for subject_index, subject in enumerate(subjects):
                    score = association_score(subject, detection)
                    if score <= 0.0:
                        continue
                    if (
                        detection.track_id is not None
                        and subject.track_id == detection.track_id
                    ):
                        best_subject = subject_index
                        break
                    if score > best_score and score >= threshold:
                        best_score = score
                        best_subject = subject_index
                if best_subject >= 0:
                    owned.setdefault(best_subject, set()).add(attribute_index)
            result[attribute] = owned
        return result

    def _count_compliant(
        self,
        subjects: Sequence[PipelineDetection],
        owner: Mapping[str, Mapping[int, set[int]]],
    ) -> int:
        """How many subjects carry every ``required`` entity and no ``violations`` entity."""
        compliant = 0
        for index in range(len(subjects)):
            if any(index in owner[attribute] for attribute in self._violations):
                continue
            if all(index in owner[attribute] for attribute in self._required):
                compliant += 1
        return compliant

    def _orphan_violations(
        self,
        by_attribute: Mapping[str, Sequence[PipelineDetection]],
        owner: Mapping[str, Mapping[int, set[int]]],
    ) -> int:
        """Violation-class boxes that belong to no subject.

        The single-stage PPE case (``safety.py:246-256``): the model emits ``no_hardhat``
        and no ``person`` at all.  Counting only per-subject violations would report zero
        for a frame full of bare heads.  Distinct ``track_id``\\ s count once; untracked
        boxes count individually, as the legacy counter did.
        """
        total = 0
        for attribute in self._violations:
            detections = by_attribute.get(attribute, ())
            assigned = {
                index for indices in owner.get(attribute, {}).values() for index in indices
            }
            seen: set[int] = set()
            for index, detection in enumerate(detections):
                if index in assigned:
                    continue
                if detection.track_id is None:
                    total += 1
                elif detection.track_id not in seen:
                    seen.add(detection.track_id)
                    total += 1
        return total

    # -- window -------------------------------------------------------------

    def _accumulate(self, subject_count: int, compliance_pct: float) -> None:
        """Fold this frame into the window mean, in the state store.

        ``Lifetime.WINDOW`` because these are measurements *of* the window: carrying them
        past the 60 s boundary averages two windows together (``09`` §4 rule 2).  A plain
        ``self._sum`` would work today and be invisible to a Redis backing tomorrow
        (**D6**), which is why the store is not optional.

        Frames with no subject are excluded from the denominator on purpose: their
        ``compliance_pct`` is the "nothing to assess" 0, and averaging it in is how an
        overnight camera reports a 4% compliant day shift.
        """
        if subject_count <= 0:
            return
        self._state.incr(_PCT_SUM, compliance_pct, lifetime=Lifetime.WINDOW)
        self._state.incr(_PCT_FRAMES, 1, lifetime=Lifetime.WINDOW)

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Collapse the window into the two values ``agg_type`` cannot recover.

        Only the percentages.  A ratio is not summable and it is not the mean of the
        window's totals either -- publishing one as a 60-second ``sum`` is **PY-1** -- so
        the frame-mean is computed here, over the frames that had a subject.

        The counts are deliberately *not* republished: they are honest per-frame samples,
        and ``metrics[].agg_type`` collapses them correctly without help.  Emitting a
        second, differently-derived ``violation_count`` here would give the runtime two
        answers to one question.

        Args:
            frames: This stage's per-frame outputs for the window, in frame order.  Unused
                -- the accumulators in the state store are the same data, already folded,
                and survive a runtime that hands back an empty list.
        """
        del frames
        count = float(self._state.get(_PCT_FRAMES, 0.0) or 0.0)
        if count <= 0:
            return WindowOutput()
        total = float(self._state.get(_PCT_SUM, 0.0) or 0.0)
        compliance_pct = total / count
        return WindowOutput(
            values=self._selected(
                {
                    "compliance_pct": compliance_pct,
                    "violation_pct": 100.0 - compliance_pct,
                }
            )
        )

    def reset(self) -> None:
        """Clear the window accumulators at the aggregation boundary.

        :meth:`~matrice_analytics.engine.state.store.StateStore.end_window`, not
        ``clear()``: this stage keeps no cumulative total, but calling the full reset here
        is the habit that erases one somewhere else (``09`` §4 rule 2, **FROZEN-4**).
        """
        self._state.end_window()

    # -- helpers ------------------------------------------------------------

    def _selected(self, values: dict[str, Scalar]) -> dict[str, Scalar]:
        """Apply ``emit:``, the config's "publish only this subset" filter.

        The manifest has already checked every named key is one this primitive produces,
        so an unknown name here is impossible rather than silently dropped.
        """
        if self._emit is None:
            return values
        return {key: value for key, value in values.items() if key in self._emit}
