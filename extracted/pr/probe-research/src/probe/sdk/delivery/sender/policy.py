"""SendPolicy: what one write does when sending fails, resolved once per call from its flags and its
client's own settings (`resolve_policy`)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..ops.classify import classify as _journal_classify


@dataclass(frozen=True)
class SendPolicy:
    """One write's failure rules. Rules, in order (DESIGN.md has why each one exists):

    1. ``strict``: ``None`` takes the client's ``not fail_open``; an explicit value wins.
    2. ``strict`` beats ``sync``: a strict write raises, never queues.
    3. ``raise_permanent``: ``None`` takes the client's, read at call time (the CLI sets it after
       construction).
    4. ``raise_permanent`` raises only what the classifier calls permanent or idempotent, and only
       when the write is sent now; it never makes a write go now.
    5. ``durable=False`` wins over ``strict``: no sink, any failure raises, a non-JSON 2xx too.
    6. A body that fails the NUL check raises under strict, raise_permanent or durable=False;
       otherwise it is queued as a refused op.
    7. A send that fails with anything but our API's errors raises whatever the flags say."""

    strict: bool
    sync: bool
    raise_permanent: bool
    durable: bool

    def should_raise_on_invalid_body(self) -> bool:
        """Rule 6."""
        return self.strict or self.raise_permanent or not self.durable

    def should_raise(self, exc: BaseException) -> bool:
        """Whether a failed send raises ``exc`` instead of queueing the write (rules 2 and 4)."""
        if self.strict:
            return True
        return self.raise_permanent and _journal_classify(exc) in ("permanent", "idempotent")


def resolve_policy(
    client: Any, *, strict: bool | None, sync: bool, durable: bool, raise_permanent: bool | None
) -> SendPolicy:
    """The policy of one `Client.write` call (rules 1 and 3)."""
    if raise_permanent is None:
        raise_permanent = bool(getattr(client, "raise_permanent", False))
    strict = (not client.fail_open) if strict is None else strict
    return SendPolicy(strict=bool(strict), sync=bool(sync), raise_permanent=bool(raise_permanent), durable=bool(durable))
