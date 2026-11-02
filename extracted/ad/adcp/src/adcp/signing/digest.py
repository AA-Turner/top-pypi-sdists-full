"""Content-Digest (RFC 9530) support for the AdCP request-signing profile.

Only `sha-256` is required. The header value is an RFC 8941 sf-dictionary:
`sha-256=:<base64>:[, sha-512=:<base64>:]`. A digest matches when the sha-256
entry's decoded bytes equal `sha256(body)`.
"""

from __future__ import annotations

import base64
import binascii
import hashlib

from adcp.signing.canonical import split_structured_field


def compute_content_digest_sha256(body: bytes) -> str:
    """Return the Content-Digest header value for a body (sha-256 only)."""
    h = hashlib.sha256(body).digest()
    return f"sha-256=:{base64.b64encode(h).decode('ascii')}:"


def content_digest_matches(header_value: str, body: bytes) -> bool:
    """Return True iff the sha-256 entry in the header matches the body."""
    expected = hashlib.sha256(body).digest()
    for entry in split_structured_field(header_value, ","):
        entry = entry.strip()
        eq = entry.find("=")
        if eq < 0:
            continue
        algo = entry[:eq].strip().lower()
        if algo != "sha-256":
            continue
        val = entry[eq + 1 :].strip()
        if not (val.startswith(":") and val.endswith(":")):
            return False
        b64 = val[1:-1]
        received = _decode_sf_binary(b64)
        if received is None:
            return False
        return received == expected
    return False


def _decode_sf_binary(b64: str) -> bytes | None:
    """Decode an sf-binary payload. Standard base64 per RFC 8941; also tolerate base64url."""
    try:
        return base64.b64decode(b64, validate=True)
    except (ValueError, binascii.Error):
        pass
    try:
        pad = "=" * (-len(b64) % 4)
        return base64.urlsafe_b64decode(b64 + pad)
    except (ValueError, binascii.Error):
        return None
