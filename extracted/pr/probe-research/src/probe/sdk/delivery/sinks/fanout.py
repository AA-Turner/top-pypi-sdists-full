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
        self, method: str, path: str, body: dict | None, *, policy: Any, blocking: bool, admitted: bool,
    ) -> Any:
        """Queued, never sent now, so None (`enqueue_best_effort` says whether it was refused)."""
        self.enqueue_best_effort(method, path, body)
        return None

    def enqueue_best_effort(self, method: str, path: str, body: dict | None) -> bool:
        """Queue a best-effort hardware write to a run (plan 0.3), FIFO with the run's own ops and
        ``blocking=False``, never around the journal (that collided with the metric insert: 503). False
        when the journal refused it for room, dropped quietly; raises when the journal is broken, so the
        caller's own buffer retries."""
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
