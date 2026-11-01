"""FanOutSink: the best-effort hardware rail, queued behind the run's own writes; a refusal for
room drops it quietly, a broken journal raises for the caller's own buffer."""

from __future__ import annotations

from typing import Any

from .. import sink as _sink
from ..sink import HeldClient, SinkKind


class FanOutSink:
    """The rail's door under async writes (plan 0.3). Holds no state."""

    kind = SinkKind.FANOUT
    _client = HeldClient()

    def __init__(self, client: Any) -> None:
        self._client = client

    def queues(self, *, strict: bool, sync: bool) -> bool:
        return True

    def land(
        self, method: str, path: str, body: dict | None, *, strict: bool, sync: bool, blocking: bool,
        raise_permanent: bool, admitted: bool,
    ) -> Any:
        """Queued, never sent now, so None (`enqueue_best_effort` says whether it was refused)."""
        self.enqueue_best_effort(method, path, body)
        return None

    def enqueue_best_effort(self, method: str, path: str, body: dict | None) -> bool:
        """Queue a best-effort write to a run (the hardware rail's door under async writes;
        plan 0.3, D2). Not public API.

        A write around the journal lands on the run row while the drainer delivers the
        run's metrics, and the server's metric insert takes that row NOWAIT, so the collision
        answers 503: with hardware on, ``finish()`` raised on 4 of 6 short runs (0 of 6 with
        ``PROBE_HW=0``). Queued, it drains FIFO with the run's other ops, one at a time.

        ``blocking=False``: never holds the run's close, so a dead-lettered hardware op
        cannot decide how the run ends.

        Returns False when the journal REFUSED the op for room (``OutboxFull``: op ceiling or
        free-disk floor). Dropped on purpose: spool space belongs to training metrics and a
        refusal retried from a buffer is only refused again. Not the user's data: prints
        nothing, records no capture gap, not counted on ``dropped_writes``
        (``best_effort=True``).

        RAISES when the journal is broken (read-only state dir, ENOSPC mid-write, ``flock``
        ENOSYS): the caller keeps its own bounded buffer for this, and retrying next tick can
        succeed where retrying a refusal cannot.
        """
        client = self._client
        from ..journal.headroom import OutboxFull

        _sink._touch_run_lease(path, base_url=client.settings.base_url, spool_dir=str(client.journal.dir))
        if client._redact is not None and body is not None:
            body = client._redact(body)
        try:
            # append_http normalizes, NUL-checks (a bad body becomes a rejected_http op that
            # dead-letters) and scrubs, as write() does.
            client.journal.append_http(method, path, body, blocking=False, best_effort=True)
        except OutboxFull:
            return False
        client._after_enqueue()
        return True
