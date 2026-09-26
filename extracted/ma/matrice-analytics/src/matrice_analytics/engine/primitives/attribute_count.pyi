"""Auto-generated stub for module: attribute_count."""
from typing import Any

# Classes
class AttributeCount:
    # Per-value counts of one decoded attribute, for one zone, one frame.
    #
    #     Outputs (:attr:`~matrice_analytics.engine.primitives.base.PrimitiveOutput.values`), each
    #     resolvable as ``<stage>.<name>``:
    #
    #     ``<value>.count``
    #         Detections of ``subject`` in this zone counted as ``<value>``. For a tracked
    #         subject, this is a same-attribute ``attribute_vote`` stage's stabilised decision
    #         when one ran earlier in the pipeline (see :meth:`_resolve`); otherwise the raw
    #         intake-decoded attribute, gated by ``min_confidence``.
    #     ``<value>.new``
    #         Tracks resolved to ``<value>`` for the **first time ever** during this window --
    #         a WINDOW-lifetime event count, disjoint per frame, so ``metrics[].agg_type: sum``
    #         over it reproduces the window figure exactly. Mirrors ``unique_count``'s own
    #         ``new``/``total`` split and its explicit philosophy: once a track's first-ever
    #         decision for this attribute is counted, it is never counted again -- not on a
    #         later frame with the same value, and not if the value later switches (an
    #         ``attribute_vote`` ``switch_count``). Retroactively moving a track's ``.new``
    #         event to a different value after a switch would un-sum an already-reported
    #         window, which is exactly the invariant ``unique_count``'s own docstring refuses
    #         to break for the same reason. Untracked detections (no ``track_id``) cannot be
    #         deduplicated and never contribute here, same as ``unique_count``.
    #     ``other_new``
    #         The ``.new`` counterpart to ``other_count`` -- first-ever decisions whose label
    #         is real but not in ``values``.
    #     ``labelled_count``
    #         How many carried *any* declared value. Sum of the per-value counts.
    #     ``unknown_count``
    #         Subjects carrying **no** attribute, or one below ``min_confidence``.
    #     ``other_count``
    #         Subjects whose label is real but not in ``values`` -- the vocabulary-drift signal.
    #     ``instance_count``
    #         All subjects in this zone this frame, labelled or not. The denominator.
    #     ``max_confidence``
    #         The highest attribute confidence this frame; a health diagnostic, not a metric.
    #
    #     **``unknown_count == instance_count`` is the classifier-outage signal.**  A dead
    #     classifier chain and a frame full of unclassifiable crops look identical in per-value
    #     counts alone, so this primitive counts absence explicitly rather than letting every
    #     bucket read ``0``.
    #
    #     Not here, on purpose: temporal stabilisation (``attribute_vote``), banding a numeric
    #     attribute (``attribute_band``), uniqueness over time (``unique_count``, which dedupes on
    #     ``(entity, track_id)`` and is unchanged by any of this), and severity
    #     (``incident_quantise``).

    def __init__(self: Any, config: Any, state: Any) -> None: ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Count this zone's subjects by attribute value for one frame.
        
                No clock call, no ``require_resolution`` -- but not "reads only ``ctx.detections``"
                any more: see :meth:`_resolve`.
        """
        ...

    def reset(self: Any) -> None:
        """
        ``end_window()``, not ``clear()`` -- this stage keeps no cumulative total, and
                reaching for the full reset is the habit that erases one somewhere else
                (``09`` §4 rule 2, **FROZEN-4**).
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window. Every count is a level, so each gets **two** names (**PY-1**).
        
                Args:
                    frames: Unused -- the accumulators hold the same data already folded, and they
                        survive a window whose retained frames were capped by
                        ``runtime/window.py``'s ``max_frames`` truncation, which would silently
                        lower a peak recomputed from this list.
        """
        ...

