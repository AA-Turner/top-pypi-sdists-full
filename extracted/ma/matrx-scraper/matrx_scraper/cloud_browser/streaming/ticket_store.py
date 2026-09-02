"""Single-use ticket-hash store (S4 §3.3).

The raw ticket is NEVER stored, logged, written to an event, returned to a
model, or rendered. What is stored is ``sha256(ticket)`` hex plus lifecycle.
Claim is one atomic compare-and-swap — the whole single-use guarantee lives
here, not in application logic.

The interface is a Protocol so the real Browser Manager backs it with the
``browser.stream_ticket`` table (OPEN(S1-stream-ticket-table)); WS-4 ships the
in-memory implementation with identical CAS semantics for standalone proof.
"""

from __future__ import annotations

import hashlib
import threading
import time
from dataclasses import dataclass
from typing import Protocol

from .errors import (
    STREAM_TICKET_ALREADY_CLAIMED,
    STREAM_TICKET_REVOKED,
    StreamError,
)


def ticket_hash(ticket: str) -> str:
    return hashlib.sha256(ticket.encode("utf-8")).hexdigest()


@dataclass
class TicketRecord:
    ticket_hash: str
    run_id: str
    profile_id: str
    user_id: str
    mode: str
    stream_session_id: str
    handoff_id: str | None
    control_revision: int | None
    grant_revision: int
    minted_at: float
    expires_at: float
    claimed_at: float | None = None
    revoked_at: float | None = None
    revoke_reason: str | None = None


class TicketStore(Protocol):
    def record(self, rec: TicketRecord) -> None: ...
    def claim(self, ticket_hash_hex: str) -> TicketRecord: ...
    def revoke_for_session(self, stream_session_id: str, reason: str) -> int: ...
    def revoke_unclaimed_for_user_profile(
        self, user_id: str, profile_id: str, reason: str
    ) -> int: ...
    def purge_expired(self, now: float | None = None) -> int: ...


class InMemoryTicketStore:
    """Thread-safe in-memory store with the exact CAS of S4 §3.3."""

    def __init__(self) -> None:
        self._by_hash: dict[str, TicketRecord] = {}
        self._lock = threading.Lock()

    def record(self, rec: TicketRecord) -> None:
        with self._lock:
            self._by_hash[rec.ticket_hash] = rec

    def claim(self, ticket_hash_hex: str) -> TicketRecord:
        """Atomic single-use claim. Mirrors the SQL:

            UPDATE ... SET claimed_at = now()
             WHERE ticket_hash = $1 AND claimed_at IS NULL
               AND revoked_at IS NULL AND expires_at > now()
            RETURNING *;

        Zero rows -> reject; a second, read-only lookup chooses the error
        message (never authorizes)."""
        now = time.time()
        with self._lock:
            rec = self._by_hash.get(ticket_hash_hex)
            if (
                rec is not None
                and rec.claimed_at is None
                and rec.revoked_at is None
                and rec.expires_at > now
            ):
                rec.claimed_at = now
                return rec
            # Distinguish the cause for the message only.
            if rec is None:
                raise StreamError(STREAM_TICKET_ALREADY_CLAIMED, "ticket unknown or purged")
            if rec.revoked_at is not None:
                raise StreamError(STREAM_TICKET_REVOKED, "ticket was revoked")
            if rec.claimed_at is not None:
                raise StreamError(STREAM_TICKET_ALREADY_CLAIMED, "ticket already claimed")
            # expired: verify() normally catches this first; keep a definite code.
            raise StreamError(STREAM_TICKET_ALREADY_CLAIMED, "ticket expired")

    def revoke_for_session(self, stream_session_id: str, reason: str) -> int:
        now = time.time()
        n = 0
        with self._lock:
            for rec in self._by_hash.values():
                if rec.stream_session_id == stream_session_id and rec.revoked_at is None:
                    rec.revoked_at = now
                    rec.revoke_reason = reason
                    n += 1
        return n

    def revoke_unclaimed_for_user_profile(self, user_id: str, profile_id: str, reason: str) -> int:
        now = time.time()
        n = 0
        with self._lock:
            for rec in self._by_hash.values():
                if (
                    rec.user_id == user_id
                    and rec.profile_id == profile_id
                    and rec.claimed_at is None
                    and rec.revoked_at is None
                ):
                    rec.revoked_at = now
                    rec.revoke_reason = reason
                    n += 1
        return n

    def revoke_unclaimed_for_user_run_mode(
        self, user_id: str, run_id: str, mode: str, reason: str
    ) -> int:
        """S4 §7.1: minting a new ticket revokes that user's prior UNCLAIMED
        tickets for the same (run_id, user_id, mode)."""
        now = time.time()
        n = 0
        with self._lock:
            for rec in self._by_hash.values():
                if (
                    rec.user_id == user_id
                    and rec.run_id == run_id
                    and rec.mode == mode
                    and rec.claimed_at is None
                    and rec.revoked_at is None
                ):
                    rec.revoked_at = now
                    rec.revoke_reason = reason
                    n += 1
        return n

    def purge_expired(self, now: float | None = None) -> int:
        cutoff = now or time.time()
        n = 0
        with self._lock:
            dead = [h for h, r in self._by_hash.items() if r.expires_at < cutoff]
            for h in dead:
                del self._by_hash[h]
                n += 1
        return n
