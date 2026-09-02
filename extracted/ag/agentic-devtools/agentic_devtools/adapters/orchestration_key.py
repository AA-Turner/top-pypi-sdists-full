"""Orchestration key generation and embedding utilities.

An orchestration key is a deterministic SHA-256 hash derived from:
  - operation_type: The operation name (e.g., "create_issue", "link_subissue")
  - refs: One or more ref values in canonical order matching the IssueProvider
    method signature for the given operation

Algorithm: SHA-256 of the UTF-8 encoding of the NUL-separated (``\\x00``)
concatenation of ``operation_type`` followed by all ref values in signature order.

The key is embedded in issue bodies as an HTML comment:
  ``<!-- agdt-orch-key:SHA256_HEX -->``

This enables idempotent find-before-create semantics — the provider can search
for an existing issue bearing the same orchestration key before creating a new one.

Compatibility: The pre-#2114 algorithm (colon-separated ``source:position:content_hash``)
is explicitly **not** backward-compatible. Orchestration keys generated with the prior
algorithm will not match keys from this implementation. The embedding format
(``<!-- agdt-orch-key:<64hex> -->``) remains unchanged (NFR-002).
"""

from __future__ import annotations

import hashlib
import re

# Regex for extracting orchestration keys from text
_ORCH_KEY_PATTERN = re.compile(r"<!-- agdt-orch-key:([a-f0-9]{64}) -->", re.IGNORECASE)


def generate_orchestration_key(operation_type: str, *refs: str) -> str:
    """Generate a deterministic SHA-256 orchestration key.

    Algorithm: SHA-256 of UTF-8 encoding of the NUL-separated concatenation
    of operation_type followed by all ref values in signature order.

    Args:
        operation_type: The operation name (e.g., "create_issue").
        *refs: Ref values in the canonical order matching the IssueProvider
            method signature for this operation.

    Returns:
        A 64-character lowercase hex SHA-256 digest.

    Raises:
        ValueError: If operation_type is not a string, empty/whitespace-only,
            or if operation_type or any ref contains a NUL byte (``\\x00``).
            If any ref is not a string.
    """
    if not isinstance(operation_type, str):
        raise ValueError(f"operation_type must be a string, got {type(operation_type).__name__}")
    if not operation_type or not operation_type.strip():
        raise ValueError("operation_type must be a non-empty string")
    if "\x00" in operation_type:
        raise ValueError("operation_type must not contain NUL bytes")
    for ref in refs:
        if not isinstance(ref, str):
            raise ValueError(f"each ref must be a string, got {type(ref).__name__}")
        if "\x00" in ref:
            raise ValueError("refs must not contain NUL bytes")

    payload = "\x00".join((operation_type, *refs))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def embed_orchestration_key(body: str, key: str) -> str:
    """Append an orchestration key marker to an issue body.

    If the body already contains the same key, it is returned unchanged.
    If it contains a different key, the old one is replaced.

    Args:
        body: The issue body text.
        key: The 64-char hex orchestration key.

    Returns:
        The body with the orchestration key marker appended (or replaced).
    """
    normalized_key = key.lower()
    marker = f"<!-- agdt-orch-key:{normalized_key} -->"
    existing = _ORCH_KEY_PATTERN.search(body)
    if existing:
        if existing.group(1).lower() == normalized_key and existing.group(0) == marker:
            return body
        return _ORCH_KEY_PATTERN.sub(marker, body)
    # Append with a blank line separator if body is non-empty
    if body and not body.endswith("\n"):
        return f"{body}\n\n{marker}"
    if body:
        return f"{body}\n{marker}"
    return marker


def extract_orchestration_key(body: str) -> str | None:
    """Extract an orchestration key from an issue body.

    Args:
        body: The issue body text.

    Returns:
        The 64-char hex key if found, else ``None``.
    """
    match = _ORCH_KEY_PATTERN.search(body)
    return match.group(1).lower() if match else None
