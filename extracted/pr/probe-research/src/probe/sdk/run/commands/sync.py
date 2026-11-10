"""`probe.commands.sync()`: the point in a plain multi-process script where every rank takes the run's commands
together (agentic W&B C.1). Call it on every rank at the same place in the loop (every N steps is enough); rank 0's
claimed commands reach every rank and each rank runs its own `run.on` handler. Why: DESIGN.md "Every rank"."""

from __future__ import annotations

from typing import Any


def sync(run: Any = None) -> int:
    """Hand the commands rank 0 claimed to every rank and run them here; how many ran. Every rank must call it at
    the same point, or the job hangs. ``run``: the handle (default: the active run); without one, a no-op that still
    joins the hand-off, so ranks that opened no run keep step."""
    from ...fluent.fluent import active_run
    from .ranks import send_to_every_rank

    handle = run if run is not None else active_run()
    if handle is None or not hasattr(handle, "sync_commands"):
        send_to_every_rank([])
        return 0
    return handle.sync_commands()


__all__ = ["sync"]
