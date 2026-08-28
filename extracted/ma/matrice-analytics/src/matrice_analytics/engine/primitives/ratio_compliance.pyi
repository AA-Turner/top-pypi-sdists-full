"""Auto-generated stub for module: ratio_compliance."""
from typing import Any

# Functions
def association_score(subject: Any, attribute: Any) -> float:
    """
    How strongly ``attribute`` belongs to ``subject``, in ``0..1``.
    
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
    ...

# Classes
class RatioCompliance:
    # ``ratio_compliance`` -- fraction of ``subject`` detections satisfying the rule.
    #
    #     A subject is **compliant** when every entity in ``required`` is associated to it *and*
    #     no entity in ``violations`` is.  With ``required: []`` (recipe F -- a product is fine
    #     unless a defect is found on it) the first clause is vacuously true, which is why the
    #     manifest insists at least one of the two lists is non-empty: with both empty every
    #     subject is trivially compliant and the app publishes a constant 100.
    #
    #     Outputs (:attr:`PrimitiveOutput.values`), all resolvable as
    #     ``<stage>.<name>``:
    #
    #     ``subject_count``
    #         Subject detections in this zone, this frame.
    #     ``compliant_count``
    #         Subjects satisfying the rule.
    #     ``violation_count``
    #         ``subject_count - compliant_count``, **plus** orphan violation-class detections --
    #         violation boxes that belong to no subject.  Single-stage PPE models emit
    #         ``no_hardhat`` without a ``person`` box at all, and the legacy processor counted
    #         those directly (``safety.py:154-177``); dropping them would silently under-report
    #         the exact thing the app exists to find.
    #     ``compliance_pct``
    #         ``compliant_count / subject_count * 100``.
    #     ``violation_pct``
    #         ``100 - compliance_pct``.  The one output ``08`` §2 forgot; ``FIELD_REFERENCE``
    #         recipe F sources it as ``defect_rate``.
    #     ``<attr>_count``
    #         One per entity in ``required + violations``: how many of that entity were detected
    #         in this zone this frame.  The name is the raw entity name, un-sanitised, because
    #         that is what
    #         :meth:`~matrice_analytics.engine.manifest.models.RatioComplianceConfig.output_names`
    #         declares and therefore what a ``metrics[].source`` can name.
    #
    #     With **no subjects in frame** both percentages are ``0.0``, not ``100``/``0`` and not
    #     ``0``/``100``.  Nothing was assessed, so neither reading is true, and the pair is
    #     deliberately not complementary in that one degenerate case: publishing
    #     ``violation_pct: 100`` for an empty conveyor would make recipe F's ``defect_rate``
    #     read 100% every night, and publishing ``compliance_pct: 100`` for a dead camera would
    #     hide an outage behind a perfect score.  ``subject_count`` is what distinguishes
    #     "assessed and fine" from "nothing to assess" -- read it alongside.

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Construct from a validated config and an already-scoped state store.
        
                Args:
                    config: The stage's config, validated by the manifest loader.
                    state: A store scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` (``09`` §4).
        
                Raises:
                    ValueError: ``required`` and ``violations`` are both empty.  The manifest model
                        rejects this too, but a config built with ``model_construct`` skips
                        validators, and a silently-100% compliance app is worse than a loud
                        constructor.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Assess this zone's subjects for one frame.
        
                Args:
                    ctx: The frame's detections, already entity-remapped and zone-assigned.
        
                Returns:
                    The compliance values for this frame.  Never any events -- compliance becomes
                    an incident through a manifest threshold on ``violation_count``, which is the
                    runtime's decision, not this primitive's (**O1**).
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear the window accumulators at the aggregation boundary.
        
                :meth:`~matrice_analytics.engine.state.store.StateStore.end_window`, not
                ``clear()``: this stage keeps no cumulative total, but calling the full reset here
                is the habit that erases one somewhere else (``09`` §4 rule 2, **FROZEN-4**).
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window into the two values ``agg_type`` cannot recover.
        
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
        ...

