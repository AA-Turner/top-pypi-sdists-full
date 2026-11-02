"""Idempotency-key generation and pagination derivation."""

from __future__ import annotations

import uuid

_MAX_KEY_BYTES = 255


def generate_idempotency_key() -> str:
    """Return a stdlib UUID token without separators."""
    return uuid.uuid4().hex


def validate_idempotency_key(key: str) -> None:
    """Enforce the gateway's 1-255 byte visible-ASCII wire contract."""
    if (
        not key
        or len(key) > _MAX_KEY_BYTES
        or any(ord(char) < 0x21 or ord(char) > 0x7E for char in key)
    ):
        raise ValueError(
            "idempotency_key must be 1-255 bytes of visible ASCII (0x21-0x7e)"
        )


def page_idempotency_key(key: str, page_number: int) -> str:
    """Derive a distinct, valid key for one explicitly keyed page."""
    validate_idempotency_key(key)
    suffix = f"-p{page_number}"
    prefix_length = _MAX_KEY_BYTES - len(suffix)
    if prefix_length < 1:
        raise ValueError("pagination page number is too large for an idempotency key")
    return f"{key[:prefix_length]}{suffix}"
