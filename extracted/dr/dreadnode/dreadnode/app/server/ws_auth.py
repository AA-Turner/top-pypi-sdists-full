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


@dataclass(frozen=True)
class _TicketEntry:
    """An issued ticket: when it expires, and which runtime token minted it."""

    expiry: float
    token: str


class WsTicketStore:
    """Process-local store of single-use websocket auth tickets.

    Stores only hashes of issued tickets, each bound to the runtime token that
    authorized the mint. Tickets are consumed (deleted) on first successful
    validation.

    The token binding matters: a ticket outlives the request that minted it (up
    to its TTL), so without it a client whose token was rotated out could still
    redeem a pre-rotation ticket and open a socket — exactly the connection the
    rotation was meant to sever. ``consume`` therefore reports *which* token
    authorized the ticket, and ``purge_for_token`` drops the tickets belonging to
    a token the moment it is retired.
    """

    def __init__(self) -> None:
        self._entries: dict[str, _TicketEntry] = {}  # hash(ticket) -> entry
        # Critical sections contain no awaits, so a plain threading.Lock is
        # sufficient to guard concurrent access from event-loop tasks.
        self._lock = threading.Lock()

    def mint(self, *, token: str, ttl_seconds: int = 30) -> WsAuthTicket:
        """Issue a ticket valid for ``ttl_seconds``, bound to ``token``."""
        raw = secrets.token_urlsafe(_TICKET_BYTES)
        now = time.time()
        with self._lock:
            self._purge_expired(now)
            self._entries[self._hash(raw)] = _TicketEntry(
                expiry=now + ttl_seconds,
                token=token,
            )
        iso = (datetime.now(UTC) + timedelta(seconds=ttl_seconds)).strftime("%Y-%m-%dT%H:%M:%SZ")
        return WsAuthTicket(ticket=raw, expires_at=iso)

    def consume(self, ticket: str) -> str | None:
        """Validate and consume a ticket, returning the token that minted it.

        Returns ``None`` when the ticket is unknown, already used, or expired.
        Succeeds at most once per minted ticket.
        """
        if not ticket:
            return None
        now = time.time()
        digest = self._hash(ticket)
        with self._lock:
            self._purge_expired(now)
            entry = self._entries.pop(digest, None)  # single-use: pop on read
        if entry is None or entry.expiry < now:
            return None
        return entry.token

    def purge_for_token(self, token: str) -> int:
        """Drop every outstanding ticket minted with ``token``; returns the count.

        Called when a token is retired, so a rotation also revokes the tickets
        that token authorized.
        """
        with self._lock:
            stale = [digest for digest, entry in self._entries.items() if entry.token == token]
            for digest in stale:
                del self._entries[digest]
        return len(stale)

    def _purge_expired(self, now: float) -> None:
        expired = [digest for digest, entry in self._entries.items() if entry.expiry < now]
        for digest in expired:
            del self._entries[digest]

    @staticmethod
    def _hash(ticket: str) -> str:
        return hashlib.sha256(ticket.encode()).hexdigest()
