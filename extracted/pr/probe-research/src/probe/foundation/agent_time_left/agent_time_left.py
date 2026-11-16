"""The seconds an agent's command has left, from what the npm launcher puts in its environment (plan I-F1).

The launcher counts its 110 s on a clock that pauses while the computer sleeps and hands the rest on as
SECONDS_LEFT_ENV, with the old absolute DEADLINE_ENV beside it (npx caches old launchers; old CLIs read
only the deadline). Stdlib only: the `probe` shim reads it too.
"""

from __future__ import annotations

import os
import time
from collections.abc import Mapping

#: Seconds left when the launcher started this command (its countdown, which pauses in sleep).
SECONDS_LEFT_ENV = "PROBE_AGENT_SECONDS_LEFT"
#: The same end on the wall clock (epoch s): an old launcher's only form, and how long ago the new one sent it.
DEADLINE_ENV = "PROBE_AGENT_DEADLINE"
#: The most an agent's command is ever given (its whole budget is 110 s); a larger value is ignored.
MAX_SECONDS = 120.0


def get_seconds_left(env: Mapping[str, str] | None = None, now: float | None = None) -> float | None:
    """Seconds left for this agent's command (0 or more), or None: not an agent's call, or nothing usable.

    Seconds left wins; the wall clock takes off the time since the launcher sent it (uv building the CLI's
    env first). A wall clock behind the send (set back) leaves the countdown whole. One already past the end
    is no agent's call, as a passed deadline always was: a value a late child inherited, which a sleep before
    this process started cannot be told apart from. An old launcher's deadline alone counts as before."""
    env = os.environ if env is None else env
    now = time.time() if now is None else now
    seconds = _get_number(env, SECONDS_LEFT_ENV)
    deadline = _get_number(env, DEADLINE_ENV)
    if seconds is not None and 0 <= seconds <= MAX_SECONDS:
        if deadline is None:
            return seconds
        gap = now - (deadline - seconds)
        if gap > seconds:
            return None
        return seconds - max(0.0, gap)
    if deadline is not None and now < deadline <= now + MAX_SECONDS:
        return deadline - now
    return None


def _get_number(env: Mapping[str, str], name: str) -> float | None:
    try:
        return float(env.get(name, ""))
    except ValueError:
        return None
