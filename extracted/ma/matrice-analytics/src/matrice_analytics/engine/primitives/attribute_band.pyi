"""Auto-generated stub for module: attribute_band."""
from typing import Any

# Classes
class AttributeBand:
    # Per-track running mean of a numeric attribute, banded into named buckets.
    #
    #     Outputs, each resolvable as ``<stage>.<name>``:
    #
    #     ``<band>.count``
    #         Subjects this frame whose (smoothed, where a track id exists) value falls in
    #         ``<band>``.
    #     ``measured_count``
    #         Subjects successfully banded. Sum of the per-band counts.
    #     ``unknown_count``
    #         Subjects carrying no usable numeric value for ``attribute`` this frame.
    #     ``instance_count``
    #         All subjects in this zone this frame, banded or not. The denominator.
    #     ``mean_value``
    #         This frame's average of the (smoothed) measured values; a health diagnostic, not a
    #         metric.
    #
    #     Per-track running-mean history is ``Lifetime.PERSISTENT`` -- a track's smoothed value
    #     must not re-ramp from empty at every window boundary -- and is pruned the same way
    #     ``attribute_vote`` prunes its per-track vote history: against the upstream ``track``
    #     stage's currently-active track ids, never against this stage's own per-frame subset.

    def __init__(self: Any, config: Any, state: Any) -> None: ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Band this zone's subjects by the (smoothed) value of one numeric attribute.
        """
        ...

    def reset(self: Any) -> None:
        """
        ``end_window()``, not ``clear()`` -- per-track running-mean history is
                PERSISTENT and must survive the window boundary, or a track's smoothed value
                re-ramps from empty once per interval.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Republish the last frame's readings -- no separate peak variant (unlike
                ``attribute_count``): a band count is not tracked as a high-water mark here.
        
                Args:
                    frames: Unused -- the state store is authoritative, for the same reason
                        ``attribute_count.window`` ignores it.
        """
        ...

