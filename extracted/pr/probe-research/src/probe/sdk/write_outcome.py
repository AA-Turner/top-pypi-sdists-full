"""How the CLI says a write did not reach Probe (lineage plan L14).

Stdlib only, and tiny on purpose, like `key_refusal`: the CLI (`probe.cli.main`)
prints these lines and the Probe daemon's tools read them, and neither imports
the other (the CLI's module takes ~0.6s to load).

A CLI write whose request failed in a way that could still succeed later (no
answer, a 5xx, a credential the server refused for now) is kept in the outbox
and delivered later: the command exits 0 and says so on stderr with
`QUEUED_PREFIX`. The daemon's logbook records such a command as `queued`, never
as recorded. A write the outbox could not keep either is lost: `NOT_QUEUED_PREFIX`,
exit 1. A refusal (a 4xx) is neither: it raises, and the CLI exits 1 with the
server's message.
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
    """Did the CLI say (on a STDERR line of its own) that it queued a write?
    Pass stderr only: stdout is the record the command printed, which can
    quote anything."""
    return bool(_QUEUED_LINE.search(stderr or ""))
