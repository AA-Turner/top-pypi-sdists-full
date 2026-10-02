"""Auto-generated stub for module: verification."""
from typing import Any

# Constants
logger: Any

# Classes
class Verification:
    # ``verification`` -- gate (or shadow) a candidate on a VLM verdict, for one bucket.
    #
    #     Outputs, every frame, zeros included: ``verified_rank``, ``verified``,
    #     ``verification_pending``, ``verification_suppressed``, ``verification_rejected``,
    #     ``verification_dropped``, ``verification_skipped``, ``verification_votes_confirmed``,
    #     ``verification_votes_total`` (see
    #     :attr:`~matrice_analytics.engine.manifest.models.VerificationConfig.STATIC_OUTPUTS`).
    #
    #     On a *passing* frame every event the source stage raised under its own name is re-raised
    #     under this stage's name, so ``severity_from: <this stage>`` works exactly like
    #     ``severity_from: incident_quantise``.
    #
    #     The mailbox is ``state.prefix`` -- ``<camera>/<app>/<bucket>/<stage>`` -- which is stable
    #     across a session rebuild, so a verdict submitted by the old instance reaches the new one.

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Bind a validated config to a store already scoped to this bucket and stage.
        
                The worker is **not** built here: an app that never raises a candidate (and the
                validator's synthetic camera, whose id is not an ObjectID) never touches it.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Collect any verdict, then decide this frame.
        
                Collect first, always: a verdict that lands on a quiet frame must still move the state,
                or it is lost on exactly the frame where nothing is detected.
        """
        ...

    def reset(self: Any) -> None:
        """
        Window boundary: clear WINDOW keys only -- every key here is PERSISTENT and survives.
        
                Runs every 60 s, so it must never touch the worker; teardown is
                ``EngineBackend.close()`` -> ``close_all_workers()``.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Each flag as "at any point this window" (its max), the votes as they stand.
        
                ``verified_rank`` is the window's peak passing rank -- the same peak-not-mean reading
                ``incident_quantise`` publishes for its rank (**PY-1**).  The votes are read from the
                store, not ``frames[-1]``, so a capped retention list cannot lose them.
        """
        ...

class VerificationSourceError:
    # ``verification.source`` resolved to a value that is not a number.
    #
    #     A string (``incident_quantise.level``, say) cannot be compared with ``above``; treating it as
    #     zero would make the stage silently never verify anything, so it raises instead (``09`` §3).

    ...
