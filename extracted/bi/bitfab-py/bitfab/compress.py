"""Request body compression for Bitfab API requests."""

from __future__ import annotations

import gzip
import os
from dataclasses import dataclass

DISABLE_COMPRESSION_ENV = "BITFAB_DISABLE_COMPRESSION"

# Below this, compressing costs more than the saved bytes are worth, so small
# requests (function lookups, replay status polls, single-span batches) ride
# uncompressed.
MIN_COMPRESSED_BYTES = 8_192
COMPRESSION_LEVEL = 6


@dataclass(frozen=True)
class PreparedRequest:
    body: bytes
    content_encoding: str | None
    raw_bytes: int
    wire_bytes: int


def prepare_request_body(body: str) -> PreparedRequest:
    """Prepare one body once so sizing and sending use the same bytes."""
    encoded = body.encode("utf-8")
    if os.environ.get(DISABLE_COMPRESSION_ENV) or len(encoded) < MIN_COMPRESSED_BYTES:
        return PreparedRequest(encoded, None, len(encoded), len(encoded))
    try:
        compressed = gzip.compress(encoded, compresslevel=COMPRESSION_LEVEL)
        if len(compressed) >= len(encoded):
            return PreparedRequest(encoded, None, len(encoded), len(encoded))
        return PreparedRequest(compressed, "gzip", len(encoded), len(compressed))
    except Exception:
        return PreparedRequest(encoded, None, len(encoded), len(encoded))


def encode_request_body(body: str) -> tuple[bytes, str | None]:
    """Encode a request body, compressing it when it is large enough to pay off.

    Returns the bytes to send and the ``Content-Encoding`` they carry, or
    ``None`` when the body is sent as-is. Compression is best-effort: any
    failure sends the original body rather than dropping the span.
    """
    prepared = prepare_request_body(body)
    return prepared.body, prepared.content_encoding
