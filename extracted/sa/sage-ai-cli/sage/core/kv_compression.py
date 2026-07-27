"""Item #11 — KV-cache compression."""

from __future__ import annotations

import zlib

__all__ = ["compress_kv", "decompress_kv"]


def compress_kv(payload: bytes) -> bytes:
    return zlib.compress(payload, level=6)


def decompress_kv(payload: bytes) -> bytes:
    return zlib.decompress(payload)
