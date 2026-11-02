"""Sink: where a write lands, chosen from the client's mode (variants in sinks/), and what
every sink does on the way: renew a detached run's lease, report a failure it swallows."""

from __future__ import annotations

import weakref
from typing import TYPE_CHECKING, Any, Protocol

from ...foundation.compat.compat import StrEnum
from .. import routes

if TYPE_CHECKING:
    from .sender import SendPolicy


class SinkKind(StrEnum):
    """Which sink a client's writes land in."""

    DIRECT = "direct"  # sync writes: sent now; the outbox only when sending fails (never under strict)
    QUEUED = "queued"  # async writes: queued in the client's journal (the outbox, or an offline run's queue)
    FANOUT = "fanout"  # the best-effort hardware rail, queued behind the run's own writes


class HeldClient:
    """A delivery object's client, held weakly (`_client = HeldClient()`): the client owns its
    Delivery and sinks, and a strong reference back would keep a dropped client (its HTTP pool,
    its journal) alive until a garbage-collection pass instead of freeing it at once."""

    def __set_name__(self, owner: type, name: str) -> None:
        self._key = f"{name}_ref"

    def __get__(self, holder: Any, owner: type | None = None) -> Any:
        if holder is None:
            return self
        client = holder.__dict__[self._key]()
        if client is None:  # only reachable by keeping a sink after its client
            raise ReferenceError(f"the client this {type(holder).__name__} delivered for is gone")
        return client

    def __set__(self, holder: Any, client: Any) -> None:
        holder.__dict__[self._key] = weakref.ref(client)


class Sink(Protocol):
    """Where a prepared durable write lands. `queues` answers for one call's flags."""

    kind: SinkKind

    def queues(self, *, strict: bool, sync: bool) -> bool:
        """Whether a durable write with these flags is queued rather than sent now."""

    def land(
        self, method: str, path: str, body: dict | None, *, policy: "SendPolicy", blocking: bool, admitted: bool,
    ) -> Any:
        """Send or queue one prepared write under its `SendPolicy`: the parsed response when it
        was sent, else None."""


def _touch_run_lease(
    path: str, *, base_url: str | None = None, spool_dir: str | None = None
) -> None:
    """Renew the auto-update lease of the run this write targets.

    Uses the journal's own `routes.run_ref_of`, so the lease run is the barrier run.
    Never raises: instrumentation must not break the write it rides on.
    """
    try:
        run_ref = routes.run_ref_of(path)
        if not run_ref:
            return
        from probe.foundation.durable import run_lock

        run_lock.renew_lease_if_stale(run_ref)
    except Exception as exc:  # noqa: BLE001 -- see docstring
        # Swallowed, but a lease that stops renewing makes a live run `untracked`.
        _capture_swallowed(exc, site="client.lease_renew", base_url=base_url, spool_dir=spool_dir)


def _capture_swallowed(
    exc: BaseException, *, site: str, base_url: str | None = None, spool_dir: str | None = None
) -> None:
    """Report a swallowed exception; lazy so `import probe` does not pull in the CLI.

    `diagnostics` reaches `probe.cli.telemetry` on its no-run leg. `base_url` is the
    backend THIS client talks to (from `probe.init(base_url=...)` or a named context)
    and gates the report against the self-host egress contract; the CLI config can
    name another backend. Omitted means suppressed, never guessed."""
    try:
        from .. import diagnostics as _diag

        _diag.capture_swallowed(exc, site=site, base_url=base_url, spool_dir=spool_dir)
    except Exception:  # noqa: BLE001 -- a reporter must never break a swallow
        pass
