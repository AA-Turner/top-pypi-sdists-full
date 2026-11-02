"""Crypto / identity pack: ``crypto.hash``, ``crypto.uuid``, ``crypto.random_string``.

Non-secret-grade primitives for deduplication keys, cache keys, and
placeholder identifiers. Declared appropriately:

- ``crypto.hash``          — PURE (same input → same digest)
- ``crypto.uuid``          — NON_DETERMINISTIC + re_execute_on_resume
- ``crypto.random_string`` — NON_DETERMINISTIC + re_execute_on_resume

Authors who want stable UUIDs across resumes (e.g. idempotency keys that
shouldn't regenerate) should compute them from a content hash via
``crypto.hash`` instead.
"""

from matrx_graph.nodes.crypto.ops import (
    HashExecutor,
    RandomStringExecutor,
    UuidExecutor,
)

__all__ = [
    "HashExecutor",
    "RandomStringExecutor",
    "UuidExecutor",
]
