"""Models shared across services."""

from __future__ import annotations

from pydantic import BaseModel

from plato.rpc.protocol import MAX_BODY_BYTES, SPOOL_CAP_BYTES


class Limits(BaseModel):
    """Server-side size limits, advertised in the handshake so clients can
    bound payloads without trial and error."""

    max_body_bytes: int = MAX_BODY_BYTES
    spool_cap_bytes: int = SPOOL_CAP_BYTES


class Ack(BaseModel):
    """Generic success response for operations with no interesting payload."""

    ok: bool = True
