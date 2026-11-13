"""Sender: send one prepared write now and give back the server's answer; on a failure its policy
does not raise, the write falls back to the outbox. The sink of a sync client, and every queueing
sink's way of sending a strict or sync write now."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

from ... import errors
from ..sink import HeldClient, SinkKind
from .policy import SendPolicy


#: True inside `queue_only()`: this thread's writes are queued, never sent (a sync client's included).
_queue_only: ContextVar[bool] = ContextVar("probe_queue_only", default=False)


@contextmanager
def queue_only() -> Iterator[None]:
    """Writes in this block are journal appends only, never a network call: for a caller that
    holds a lock a close waits on (the run-open snapshot's gate). A write the outbox refuses is
    dropped and counted, as any refused write is."""
    token = _queue_only.set(True)
    try:
        yield
    finally:
        _queue_only.reset(token)


def is_queue_only() -> bool:
    """Whether this thread is inside `queue_only()`."""
    return _queue_only.get()


class Sender:
    """Sends through the client's transport. Holds no state: the client keeps its counters."""

    kind = SinkKind.DIRECT
    _client = HeldClient()

    def __init__(self, client: Any) -> None:
        self._client = client

    def queues(self, *, strict: bool, sync: bool) -> bool:
        return False

    def land(
        self, method: str, path: str, body: dict | None, *, policy: SendPolicy, blocking: bool, admitted: bool,
    ) -> Any:
        """Send now: the parsed answer (None for an empty or non-JSON 2xx). A failure of our API
        the policy does not raise is queued and reported (`write`'s fail-open path)."""
        client = self._client
        if _queue_only.get():
            # Under a lock a close waits on (the run-open snapshot gate): queued, never sent.
            client._enqueue(method, path, body, blocking=blocking, prepared=True, admitted=admitted)
            return None
        try:
            from ..ops.op_handler import gate_samples_body

            resp = client.transport.request(method, path, json_body=gate_samples_body(client, method, path, body))
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
            if policy.should_raise(exc):
                raise
            landed = client._enqueue(method, path, body, blocking=blocking, prepared=True, admitted=admitted)
            client._note_undelivered(method, path, exc, queued=landed)
            return None
