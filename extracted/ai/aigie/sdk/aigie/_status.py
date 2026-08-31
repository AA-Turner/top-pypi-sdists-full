"""The runtime half of the span-status contract declared in `aigie.types`.

The `Literal`s there enforce nothing: `"status": "failed"` type-checks clean and
is then dropped at the ingest gateway. `normalize_status` is the runtime check,
placed at the wire boundary (`span_to_proto`) rather than on each emitter. It
corrects rather than raises - this runs in the customer's process, where the
SDK is never the reason their program fails.
"""

from __future__ import annotations

import logging
from typing import Any, get_args

from aigie.types import SpanStatus, TraceStatus

logger = logging.getLogger(__name__)

TRACE_STATUSES: frozenset[str] = frozenset(get_args(TraceStatus))
SPAN_STATUSES: frozenset[str] = frozenset(get_args(SpanStatus))

#: Every status legal on the wire. The union is currently just `TRACE_STATUSES`
#: - `SpanStatus` is a subset - but a span may legitimately carry any trace
#: status, because the worker mints the trace row from the root span. Written as
#: the union so that stays true if either literal changes.
DECLARED_STATUSES: frozenset[str] = TRACE_STATUSES | SPAN_STATUSES

#: Undeclared spellings found in shipped code, mapped to what they meant.
_ALIASES: dict[str, str] = {
    "failed": "failure",
    "running": "in_progress",
}

#: What an unrecognised status degrades to. Never `"success"`: a status we
#: cannot read is not evidence a call succeeded.
_FALLBACK = "error"


def normalize_status(status: Any) -> str | None:
    """Return `status` as a declared status, or `None` if it carries none.

    `None` in means "this payload sets no status" and is passed through
    untouched, leaving the reader's own default in place.
    """
    if status is None:
        return None

    if isinstance(status, str) and status in DECLARED_STATUSES:
        # `str.__str__`, not `str()`: a `str`-Enum member compares and hashes
        # equal to its value, so it lands here untouched - but `str()` on one
        # yields `SpanStatus.PAUSED`, which the gateway rejects. This returns
        # the underlying value for a str subclass and is a no-op for a plain str.
        return str.__str__(status)

    if isinstance(status, str):
        aliased = _ALIASES.get(status)
        if aliased is not None:
            logger.debug(
                "[status] Corrected undeclared span status %r to %r - see aigie.types",
                status,
                aliased,
            )
            return aliased

    logger.debug(
        "[status] Unrecognised span status %r degraded to %r - see aigie.types",
        status,
        _FALLBACK,
    )
    return _FALLBACK
