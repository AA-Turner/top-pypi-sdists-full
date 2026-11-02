"""Deterministic error-signature dedup engine (pure functions).

Provides deterministic signature computation, marker embedding, search
query building, and match decision logic for GitHub issue deduplication.
All functions are pure (no I/O, no state) and fully deterministic.
"""

from __future__ import annotations

import hashlib

# Marker format used in issue bodies for dedup detection
_MARKER_TEMPLATE = "<!-- agdt-dedup-sig:{sig} -->"


def build_signature(error_class: str) -> str:
    """Compute a deterministic dedup signature from an error class string.

    Normalizes the input (strip whitespace, lowercase) then returns the
    first 16 hex characters of the SHA-256 hash.

    Args:
        error_class: The error class identifier to hash.

    Returns:
        A 16-character lowercase hex string.
    """
    normalized = error_class.strip().lower()
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return digest[:16]


def embed_marker(body: str, sig: str) -> str:
    """Append a dedup marker to an issue body (idempotent for same sig).

    If the body already contains a marker for the given signature,
    the body is returned unchanged. Multiple different signatures
    can coexist in the same body.

    Args:
        body: The existing issue body text.
        sig: The signature to embed.

    Returns:
        The body with the marker appended (or unchanged if already present).
    """
    marker = _MARKER_TEMPLATE.format(sig=sig)
    if marker in body:
        return body
    if body and not body.endswith("\n"):
        return body + "\n" + marker
    return body + marker


def build_search_query(sig: str) -> str:
    """Build a GitHub search query that finds issues carrying the given signature.

    The query uses ``in:body`` to restrict matching to the issue body field
    and ``is:issue`` to exclude pull requests from results.

    Args:
        sig: The dedup signature to search for.

    Returns:
        A search query string suitable for the GitHub ``/search/issues`` API.
    """
    marker = _MARKER_TEMPLATE.format(sig=sig)
    return f'"{marker}" in:body is:issue'


def decide(matches: list[dict], sig: str) -> dict[str, str | int | None]:
    """Decide whether to create a new issue or upvote/augment an existing one.

    Filters matches to those containing the exact marker for *sig*,
    deduplicates by issue number, and picks the lowest-numbered match
    as the canonical duplicate.

    Args:
        matches: List of issue dicts from the GitHub search API. Each dict
            should have at minimum ``number`` (int) and ``body`` (str) fields.
        sig: The dedup signature to look for in issue bodies.

    Returns:
        ``{"action": "create"}`` when no valid match exists, or
        ``{"action": "upvote-augment", "issue_number": <int>}`` for the
        lowest-numbered matching issue.
    """
    marker = _MARKER_TEMPLATE.format(sig=sig)
    seen: set[int] = set()
    valid_numbers: list[int] = []

    for item in matches:
        number = item.get("number")
        if not isinstance(number, int) or number <= 0:
            continue
        body = item.get("body") or ""
        if marker in body and number not in seen:
            seen.add(number)
            valid_numbers.append(number)

    if not valid_numbers:
        return {"action": "create"}

    return {"action": "upvote-augment", "issue_number": min(valid_numbers)}
