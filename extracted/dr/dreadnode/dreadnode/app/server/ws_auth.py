"""Short-lived, single-use authentication tickets for the runtime websocket.

Browsers cannot set an ``Authorization`` header on a ``WebSocket`` handshake, so
they cannot use the bearer-token path the TUI and Python clients use for
``/api/ws``. Instead, a browser exchanges the runtime bearer token (over HTTP,
where it *can* set the header) for a one-time ticket via ``POST /api/ws/ticket``,
then opens ``wss://<runtime>/api/ws?ticket=<ticket>``.

The store keeps only a SHA-256 hash of each issued ticket keyed to an expiry, and
deletes the entry on first successful validation (single-use). It is process-local:
tickets only validate against the harness process that minted them.
"""

import hashlib
import secrets
import threading
import time
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

_TICKET_BYTES = 32  # entropy for secrets.token_urlsafe


@dataclass(frozen=True)
class WsAuthTicket:
    """A minted websocket ticket. ``ticket`` is the plaintext value returned to
    the caller exactly once; the store never persists it."""

    ticket: str
    expires_at: str  # ISO-8601 UTC, e.g. "2026-06-16T15:04:05Z"


class WsTicketStore:
    """Process-local store of single-use websocket auth tickets.

    Stores only SHA-256 hashes of issued tickets keyed to an epoch expiry.
    Tickets are consumed (deleted) on first successful validation.
    """

    def __init__(self) -> None:
        self._hashes: dict[str, float] = {}  # sha256(ticket) -> expiry epoch
        # Critical sections contain no awaits, so a plain threading.Lock is
        # sufficient to guard concurrent access from event-loop tasks.
        self._lock = threading.Lock()

    def mint(self, *, ttl_seconds: int = 30) -> WsAuthTicket:
        """Issue a new ticket valid for ``ttl_seconds``."""
        raw = secrets.token_urlsafe(_TICKET_BYTES)
        now = time.time()
        expiry = now + ttl_seconds
        with self._lock:
            self._purge_expired(now)
            self._hashes[self._hash(raw)] = expiry
        iso = (datetime.now(UTC) + timedelta(seconds=ttl_seconds)).strftime("%Y-%m-%dT%H:%M:%SZ")
        return WsAuthTicket(ticket=raw, expires_at=iso)

    def consume(self, ticket: str) -> bool:
        """Validate and consume a ticket. Returns ``True`` exactly once per
        minted ticket, and only while it is unexpired."""
        if not ticket:
            return False
        now = time.time()
        digest = self._hash(ticket)
        with self._lock:
            self._purge_expired(now)
            expiry = self._hashes.pop(digest, None)  # single-use: pop on read
            return expiry is not None and expiry >= now

    def _purge_expired(self, now: float) -> None:
        expired = [digest for digest, exp in self._hashes.items() if exp < now]
        for digest in expired:
            del self._hashes[digest]

    @staticmethod
    def _hash(ticket: str) -> str:
        return hashlib.sha256(ticket.encode()).hexdigest()
