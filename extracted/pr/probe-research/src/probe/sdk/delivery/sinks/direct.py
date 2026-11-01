"""DirectSink: a sync client's writes go out now and fall back to the outbox (never under
`strict`); below the free-space floor any client's write may go around the queue."""

from __future__ import annotations

import time
from typing import Any

from ... import errors
from ..journal.journal import Journal
from ..ops.classify import classify as _journal_classify
from ..ops.ops import run_ref_for_path
from ..sink import HeldClient, SinkKind


class DirectSink:
    """Sends now through the client's transport. Holds no state: the client keeps its counters."""

    kind = SinkKind.DIRECT
    _client = HeldClient()

    def __init__(self, client: Any) -> None:
        self._client = client

    def queues(self, *, strict: bool, sync: bool) -> bool:
        return False

    def land(
        self, method: str, path: str, body: dict | None, *, strict: bool, sync: bool, blocking: bool,
        raise_permanent: bool, admitted: bool,
    ) -> Any:
        """Send now; a failure that could succeed later is queued (`write`'s fail-open path)."""
        client = self._client
        try:
            resp = client.transport.request(method, path, json_body=body)
            # A 2xx with a non-JSON body raises ValueError, not RosError (`Transport.delete`
            # defends the same: "an ingress/CDN HTML interstitial in front of the API").
            # On the door every write uses, it took down the training loop instead of spooling.
            if not resp.content:
                return None
            try:
                return resp.json()
            except ValueError:
                return None
        except errors.RosError as exc:
            if strict:
                raise
            if raise_permanent and _journal_classify(exc) in ("permanent", "idempotent"):
                raise
            landed = client._enqueue(method, path, body, blocking=blocking, prepared=True, admitted=admitted)
            client._note_undelivered(method, path, exc, queued=landed)
            return None

    def send_instead_of_queueing(
        self, method: str, path: str, body: dict | None, *, out_of_space: bool = False
    ) -> bool:
        """Below the outbox's free-space floor, deliver ``body`` directly rather than drop it
        (plan 1.5). True when delivered.

        Only while the run has NOTHING queued: the metric insert keeps the first write of a
        (series, step), so a direct `loss=2` at step 10 ahead of a queued `loss=1` at step 10
        would replace the original (Codex, round 2). Bounded: at most
        `DIRECT_SEND_TIMEOUT_SECONDS` on the training thread, and after a failure none for a
        minute, doubling to ten. Otherwise queued (under the floor the journal refuses and
        the caller drops with a capture gap, as before).

        ``out_of_space``: the append itself just failed with ENOSPC/EDQUOT (disk filled
        between free-space samples, or the floor is off).

        Never for a queue only `probe sync` drains (``_drains_by_hand``: an offline run, plan
        2.12, must not touch the network)."""
        client = self._client
        if getattr(client, "_drains_by_hand", False):
            return False
        journal = client.journal
        if not out_of_space:
            try:
                if journal.below_floor() is None:
                    return False
            except Exception:  # noqa: BLE001 -- the journal decides on its own below
                return False
        from ..journal.run_ops import RunOps

        run_ref = run_ref_for_path(path)
        now = time.monotonic()
        with client._direct_lock:
            if run_ref is None or now < client._direct_closed_until:
                return False
        try:
            # Proving the run clear parses queued op files on first ask (this thread). A
            # deep queue means delivery is behind anyway: no direct send, no seconds-long
            # first scan (review of #2054).
            status = Journal.read_status(journal.dir, include_receipts=False) or {}
            if int(status.get("pending") or 0) > client.DIRECT_SEND_MAX_QUEUED:
                return False
            with client._direct_lock:
                lane = client._lanes.get(run_ref)
                if lane is None:
                    # Every queue of the outbox: a write of this run queued under another
                    # credential (#2035) is overtaken just the same (#2041 round 4).
                    lane = client._lanes[run_ref] = RunOps(
                        journal, run_ref, blocking_only=False, queues=journal.outbox_queues()
                    )
            if lane.pending():
                # Queued ops hold this write back, and on a full disk it is dropped before
                # queueing, so no enqueue will kick the drainer. Kick it here (throttled), or
                # an op whose worker exited strands and every later write of the run is
                # dropped behind it (7-day soak, 0.200.2).
                client._kick_drainer()
                return False
        except Exception:  # noqa: BLE001 -- cannot prove the run is clear: queue it
            return False
        from ..transport.deadlines import deadline_scope

        try:
            with deadline_scope(now + client.DIRECT_SEND_TIMEOUT_SECONDS):
                client.transport.request(method, path, json_body=body)
        except Exception as exc:  # noqa: BLE001 -- the write falls back to the queue
            try:
                # Only a failure saying the SERVER is down or refusing everyone opens the
                # breaker. A 422/409 is about this write: closing direct sends for every run
                # dropped every good write under low disk for minutes (review of #2054).
                if _journal_classify(exc) in ("transient", "auth"):
                    with client._direct_lock:
                        client._direct_failures += 1
                        first, ceiling = client.DIRECT_SEND_BACKOFF
                        wait = min(ceiling, first * 2 ** (client._direct_failures - 1))
                        client._direct_closed_until = time.monotonic() + wait
            except Exception:  # noqa: BLE001 -- the breaker may never raise out of write()
                pass
            return False
        with client._direct_lock:
            client._direct_failures = 0
            client.direct_sends += 1
        return True
