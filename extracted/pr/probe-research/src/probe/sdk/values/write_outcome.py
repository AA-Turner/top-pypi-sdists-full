"""How the CLI says a write did not reach Probe (lineage plan L14).

Stdlib only and tiny, like `key_refusal`: the CLI prints these lines and the
daemon's tools read them; neither imports the other (the CLI module takes ~0.6s to load).

A write that failed but could succeed later (no answer, a 5xx, a credential
refused for now) waits in the outbox: exit 0, stderr line with `QUEUED_PREFIX`;
the daemon's logbook records it as `queued`, never recorded. If the outbox
cannot keep it either: `NOT_QUEUED_PREFIX`, exit 1. A 4xx refusal is neither:
it raises and the CLI exits 1 with the server's message.
"""

from __future__ import annotations

import re

#: Starts the stderr line of a write that is waiting in the outbox.
QUEUED_PREFIX = "probe: queued: "
#: Starts the stderr line of a write that reached neither Probe nor the outbox.
NOT_QUEUED_PREFIX = "probe: NOT queued: "

_QUEUED_LINE = re.compile(r"^" + re.escape(QUEUED_PREFIX), re.MULTILINE)


def queued_line(method: str, path: str, error: str) -> str:
    return (f"{QUEUED_PREFIX}{method} {path} was not delivered ({error}); it waits in the outbox and "
            "is sent once Probe answers - see `probe outbox status`")


def not_queued_line(method: str, path: str, error: str) -> str:
    return (f"{NOT_QUEUED_PREFIX}{method} {path} was not delivered ({error}) and the outbox could not "
            "keep it - nothing was written; run the command again")


def was_queued(stderr: str | None) -> bool:
    """Whether stderr has a queued line. Pass stderr only: stdout can quote anything."""
    return bool(_QUEUED_LINE.search(stderr or ""))
