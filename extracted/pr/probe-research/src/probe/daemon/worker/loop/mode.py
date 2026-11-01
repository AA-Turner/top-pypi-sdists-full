"""the BiteMode interface (build the next bite's prompt and history, usage limits, when to yield) and PROBE_DAEMON_MODE's pick."""

from __future__ import annotations
import os
from probe.foundation.compat.compat import StrEnum
ENV_MODE = "PROBE_DAEMON_MODE"


class Mode(StrEnum):
    """What a bite is (T15): a fresh call built from disk, or the next run of the
    session's one conversation."""

    BITES = "bites"
    CONVERSATION = "conversation"


def daemon_mode() -> Mode:
    """PROBE_DAEMON_MODE: `conversation` (the default: the companion bench measured it
    30-50% cheaper at the same checks, 2026-09-27) or `bites`."""
    raw = (os.environ.get(ENV_MODE) or Mode.CONVERSATION).strip().lower()
    try:
        return Mode(raw)
    except ValueError:
        log.warning("%s=%r is not a mode (%s): running as %s", ENV_MODE, raw, " or ".join(Mode), Mode.CONVERSATION)
        return Mode.CONVERSATION
from probe.daemon.worker.loop.reading import log  # noqa: E402 -- pieces need each other; the front door loads this one first
