"""Auto-generated stub for module: state_machine."""
from typing import Any

# Classes
class StateMachine:
    # N-of-M confirmation with asymmetric recovery, for one zone.
    #
    #     Publishes exactly the four values
    #     :attr:`~matrice_analytics.engine.manifest.models.StateMachineConfig.STATIC_OUTPUTS`
    #     declares:
    #
    #     ==================== ==============================================================
    #     ``state``            :data:`IDLE` / :data:`PENDING` / :data:`CONFIRMED` / :data:`RECOVERING`.
    #     ``active``           ``1`` while confirmed, including through recovery.  ``0`` otherwise.
    #     ``confirmed_frames`` The current evidence counter, capped at ``confirm_frames``.
    #     ``confirmed_new``    ``1`` on the frame the machine newly reaches CONFIRMED, else ``0``.
    #     ==================== ==============================================================
    #
    #     :meth:`window` publishes those four plus ``confirmed_frames_peak``, so the counter's
    #     current value and its window high-water mark have separate names rather than depending on a
    #     ``metrics[].agg_type`` the runtime deliberately does not apply. ``confirmed_new`` at window
    #     scope is the *count* of confirm transitions this window (summed, like ``unique_count.new``),
    #     not a 0/1 flag -- see the field's note on
    #     :attr:`~matrice_analytics.engine.manifest.models.StateMachineConfig.STATIC_WINDOW_OUTPUTS`
    #     for why this is the primitive an episode-counting app should reach for when there is no
    #     object identity to run ``unique_count`` against.
    #
    #     The counter is asymmetric by design:
    #
    #     * **rise** -- ``+1`` per frame the condition holds, capped at ``confirm_frames``.
    #     * **soft decay** (default) -- ``-1`` per clear frame while still unconfirmed.  One
    #       dropped frame must not discard four frames of evidence.
    #     * **hard decay** -- back to ``0`` on the first clear frame.  For conditions where a
    #       single gap genuinely invalidates the evidence.
    #     * **recovery** -- once confirmed, the counter stops mattering; ``recovery_frames``
    #       *consecutive* clear frames drop it.  Any frame in which the condition holds resets
    #       that countdown.
    #
    #     Example:
    #         With ``confirm_frames: 5, recovery_frames: 3, decay: soft`` and a condition that
    #         holds for frames 1-4, misses frame 5, then holds for 6-7::
    #
    #             frame  1  2  3  4  5  6  7
    #             hits   1  2  3  4  3  4  5
    #             active 0  0  0  0  0  0  1
    #
    #         With ``decay: hard`` the same sequence never confirms: frame 5 resets to 0.

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Bind a validated config to a state store already scoped to this stage.
        
                Args:
                    config: The validated ``state_machine:`` block.  ``confirm_frames`` is taken
                        **as written** -- see the PY-11 note in the module docstring.
                    state: Scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` by the runtime.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Advance the machine by one frame.
        
                Args:
                    ctx: This frame, in this zone.  The condition is
                        ``len(ctx.detections) > 0`` -- whatever the stages before this one left in
                        the zone.
        
                Returns:
                    The three declared values, plus a :class:`~.base.TrackState` per tracked object
                    carrying that object's own counter and state.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear window-scoped state only (``09`` §4 rule 2).
        
                ``hits``, ``clear_run``, ``confirmed`` and ``track_counters`` are
                :attr:`Lifetime.PERSISTENT` and survive.  A state confirmed at second 59 is still
                confirmed at second 61; re-qualifying from scratch every minute would make
                ``confirm_frames`` mean "per window", which no manifest says.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window.  ``active`` changes meaning here (**PY-1**).
        
                Per frame ``active`` is "is it held right now"; summing it over a window publishes a
                frame count as if it were a state.  At window scope it is ``1`` when the state was
                held at **any** point -- "did this happen in this minute", which is the question the
                60-second row answers.
        
                ``confirmed_frames`` is the evidence counter, a level, so it gets two window names:
                ``confirmed_frames`` is where the counter **stands** at the boundary (``agg_type:
                last``) and ``confirmed_frames_peak`` is the window's **highest** value (``agg_type:
                max``), from a :attr:`Lifetime.WINDOW` key.  A :class:`WindowOutput` is published
                verbatim, so one name would answer only one of the two and silently mis-answer the
                other.  ``state`` is the state the window *ended* in, so the next window's
                ``idle``-to-``confirmed`` transition is readable in sequence.
        
                Args:
                    frames: This stage's outputs for the window, in frame order.
        """
        ...

