"""Auto-generated stub for module: attribute_vote."""
from typing import Any

# Classes
class AttributeVote:
    # Per-track temporal stabilisation of one decoded attribute.
    #
    #     Publishes the decision on :attr:`~matrice_analytics.engine.primitives.base.
    #     PrimitiveOutput.tracks` as ``TrackState.attributes[self._attribute]`` -- the sanctioned
    #     channel for per-track information a later stage reads -- and does not mutate
    #     ``ctx.detections`` (frozen); a primitive that could change the frame the next stage sees
    #     would be action at a distance.
    #
    #     Outputs, each resolvable as ``<stage>.<name>``:
    #
    #     ``stable_count``
    #         Subjects this frame with a committed value (``min_votes`` cleared, or ``method`` is
    #         ``modal``, which commits immediately).
    #     ``undecided_count``
    #         Subjects with no track id, or no history and no usable observation yet.
    #     ``switch_count``
    #         How many committed values **changed** this frame versus their previous commit.
    #     ``switch_total``
    #         Window-scope only: the running sum of ``switch_count`` across the window, cleared by
    #         ``reset()``.
    #     ``tracked_count``
    #         Distinct tracks this stage published a decision for this frame.

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Bind a validated config and an already-scoped state store.
        
                Raises:
                    ValueError: ``config.method == "ema"``. Not implemented by this rollout phase
                        (``classification-primitives.md`` §5.3): ``ema`` needs the full ``top_k``
                        probability vector, which :class:`~matrice_analytics.engine.primitives.base.
                        AttributeRef` does not carry. Refusing loudly here is better than degrading
                        to a one-hot vote that looks like an EMA and is not one.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Stabilise each tracked subject's attribute for one frame.
        
                Publishes the decision on ``PrimitiveOutput.tracks`` as
                ``TrackState.attributes[self._attribute]``.
        """
        ...

    def reset(self: Any) -> None:
        """
        ``end_window()``, not ``clear()`` -- per-track vote history is PERSISTENT and must
                survive the window boundary, or a track's stabilised label re-flickers once per
                interval (``classification-primitives.md`` §5.3).
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window: the last frame's readings, plus the window's switch total.
        
                Args:
                    frames: Unused -- the state store is authoritative, for the same reason
                        ``attribute_count.window`` ignores it.
        """
        ...

