"""MappingStore protocol — caller-held per-session keys (no system secret).

The reversible-redaction subsystem generates a FRESH AES-256-GCM key per mask
operation. The key is RETURNED ONCE to the caller and never persisted. The
store sees only the per-row ciphertext + nonce — even a full DB compromise
yields zero originals without the caller's key.

The matrx-utils layer encrypts ABOVE the store interface, so concrete backends
(pgcrypto-free SQL row, SQLite, in-memory) don't need to handle keys at all.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class MappingRecord:
    """One substitution record. Lives in the redaction_mapping table.

    For modes 'reversible' / 'annotation' the ciphertext + nonce MUST be set
    (encryption happens in mask_with_mapping before this record reaches the
    store). For 'destructive' mode they are None — there is no original to
    recover.
    """

    file_id: str
    redacted_by: str
    session_id: str
    span_id: str
    detector_kind: str
    detector_version: str
    pattern_id: str
    confidence_tier: str
    mode: str  # "reversible" | "destructive" | "annotation"
    ciphertext: bytes | None
    nonce: bytes | None
    cipher: str  # e.g. "aes-256-gcm-v1"
    substitute_value: str
    location: dict[str, Any] = field(default_factory=dict)
    expires_at_iso: str | None = None


class MappingStoreProtocol(Protocol):
    """Host-injected backend for reversible-redaction mappings.

    Note: the store never sees plaintext. Encryption + decryption happen at
    the matrx-utils layer using the per-session key held by the caller.
    """

    async def begin_session(
        self,
        *,
        file_id: str,
        redacted_by: str,
        mode: str,
    ) -> str:
        """Create / reserve a session id and return it."""
        ...

    async def persist_records(self, records: list[MappingRecord]) -> None:
        """INSERT every record. Ciphertext + nonce are pre-encrypted."""
        ...

    async def fetch_session_records(
        self,
        *,
        session_id: str,
    ) -> list[MappingRecord]:
        """Return every non-revoked, non-expired record for the session.

        The store NEVER decrypts — it returns the ciphertext + nonce so the
        caller (who holds the key) can decrypt. Backends MUST enforce RLS at
        SELECT time — but note the boundary is the PARENT FILE, not row
        ownership: `pdf.redaction_mapping` is a canonical `component` of
        `file`, so whoever may view the file may read its mapping rows
        (Arman's ruling, 2026-08-21). That is safe because the rows are inert
        without the per-session key, which lives in the separate, owner-only
        `pdf.pdf_redaction_key_escrow` table. `redacted_by` is an author stamp
        and must NEVER be used to filter.

        Returning an empty list NEVER raises — it just means the caller can't
        restore anything from this session.
        """
        ...

    async def revoke_session(self, *, session_id: str) -> None:
        """Mark every mapping in the session revoked."""
        ...


# ── default in-memory backend (tests + standalone use) ───────────────────────

class InMemoryMappingStore:
    """In-memory store. Stores ciphertext + nonce verbatim — no decryption."""

    def __init__(self) -> None:
        self._sessions: dict[str, list[MappingRecord]] = {}
        self._revoked: set[str] = set()

    async def begin_session(self, *, file_id: str, redacted_by: str, mode: str) -> str:
        sid = str(uuid.uuid4())
        self._sessions[sid] = []
        return sid

    async def persist_records(self, records: list[MappingRecord]) -> None:
        for rec in records:
            self._sessions.setdefault(rec.session_id, []).append(rec)

    async def fetch_session_records(self, *, session_id: str) -> list[MappingRecord]:
        if session_id in self._revoked:
            return []
        return list(self._sessions.get(session_id, []))

    async def revoke_session(self, *, session_id: str) -> None:
        self._revoked.add(session_id)


__all__ = ["MappingRecord", "MappingStoreProtocol", "InMemoryMappingStore"]
