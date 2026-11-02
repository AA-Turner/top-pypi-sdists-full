"""Canonical payload hashing for AdCP idempotency replay detection.

The spec (AdCP #2315) defines payload equivalence as RFC 8785 JSON
Canonicalization Scheme over the request with a closed exclusion list. Two
requests with the same ``idempotency_key`` and the same canonical hash are
replays of each other; same key with different hash is
``IDEMPOTENCY_CONFLICT``.

The exclusion list is **closed** — every other field participates in the hash,
including ``ext``. See
``adcontextprotocol/adcp/docs/building/implementation/security.mdx#idempotency``.
"""

from __future__ import annotations

import copy
import hashlib
from typing import Any

import rfc8785

# Fields the spec excludes from the canonical hash. These are either
# protocol-level metadata (idempotency_key itself is the identifier) or
# routing/auth fields whose presence mustn't force a new resource on replay.
#
# ``push_notification_config.authentication.credentials`` lives under a nested
# path; ``_NESTED_EXCLUSIONS`` captures those.
EXCLUDED_FIELDS: frozenset[str] = frozenset(
    {
        "idempotency_key",
        "context",
        "governance_context",
    }
)

# Nested paths, as dotted strings. Stripped in order.
_NESTED_EXCLUSIONS: tuple[tuple[str, ...], ...] = (
    ("push_notification_config", "authentication", "credentials"),
)


def strip_excluded_fields(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a deep copy of ``payload`` with the spec's exclusion list removed.

    Top-level keys in :data:`EXCLUDED_FIELDS` are dropped. Nested paths in
    ``_NESTED_EXCLUSIONS`` are traversed; the final leaf key is removed if the
    traversal reaches it. Missing intermediate keys are a no-op — the caller's
    payload is free to omit the push_notification_config entirely.

    The input dict is never mutated.
    """
    out: dict[str, Any] = copy.deepcopy(payload)
    for key in EXCLUDED_FIELDS:
        out.pop(key, None)
    for path in _NESTED_EXCLUSIONS:
        _drop_nested(out, path)
    return out


def _drop_nested(obj: dict[str, Any], path: tuple[str, ...]) -> None:
    """Remove the leaf key of ``path`` from ``obj``, walking nested dicts."""
    if not path:
        return
    cursor: Any = obj
    for key in path[:-1]:
        if not isinstance(cursor, dict) or key not in cursor:
            return
        cursor = cursor[key]
    if isinstance(cursor, dict):
        cursor.pop(path[-1], None)


def canonical_json_sha256(payload: dict[str, Any]) -> str:
    """Compute the spec's canonical payload fingerprint.

    1. Strip the spec's exclusion list (see :func:`strip_excluded_fields`).
    2. RFC 8785 JCS canonicalize (stable key order, compact, UTF-8, spec-
       compliant number serialization).
    3. SHA-256 over the canonical bytes; return hex digest.

    The result is stable across all conforming JCS implementations. Two
    payloads whose hashes match are equivalent under AdCP replay semantics;
    two with different hashes are distinct and MUST be treated as a conflict
    when the caller supplies the same ``idempotency_key``.
    """
    stripped = strip_excluded_fields(payload)
    canonical = rfc8785.dumps(stripped)
    return hashlib.sha256(canonical).hexdigest()
