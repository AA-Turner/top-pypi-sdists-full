# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Deterministic friendly-name generation from arbitrary string identifiers.

Generates human-friendly names by hashing an input string and mapping it to
curated adjective and noun lists. The lists pair serious adjectives with
heroic or professional nouns.

Names are deterministic: the same input string always produces the same name
for a given identifier. The namespace is 22,464 combinations, so a name is a
readable handle rather than a unique key — with thousands of names drawn per
month, repeats are expected (roughly `n**2 / (2 * N)` collisions for `n` names
over a namespace of `N`). Callers that need uniqueness must use the identifier
itself, not the name.

This module is intentionally generic — it operates on arbitrary string
identifiers, not specifically Devin sessions. Domain-specific wrappers
(e.g., the MCP tool layer) add context like "Devin" suffixes.
"""

from __future__ import annotations

import hashlib
import re
from functools import lru_cache
from importlib import resources
from typing import Any
from urllib.parse import urlparse

import yaml

_SEED_FILE_NAME = "friendly_name_words.yaml"


# ---------------------------------------------------------------------------
# Seed data loading
# ---------------------------------------------------------------------------


@lru_cache(maxsize=1)
def _load_seed_data() -> dict[str, Any]:
    """Load and cache the YAML seed file bundled with this package."""
    seed_file = resources.files("airbyte_ops_mcp").joinpath(_SEED_FILE_NAME)
    return yaml.safe_load(seed_file.read_text(encoding="utf-8"))


def _get_word_lists() -> tuple[list[str], list[str]]:
    """Return the adjective and noun lists."""
    data = _load_seed_data()
    return data["adjectives"], data["nouns"]


# ---------------------------------------------------------------------------
# Core naming logic
# ---------------------------------------------------------------------------


def _pick_pair(
    identifier: str, adjectives: list[str], nouns: list[str]
) -> tuple[str, str]:
    """Deterministically select an (adjective, noun) pair from a string identifier.

    Uses SHA-256 of the identifier string.  The first 8 bytes of the digest
    are split into two 4-byte integers used to index into the word lists.
    """
    digest = hashlib.sha256(identifier.encode()).digest()
    adj_idx = int.from_bytes(digest[0:4], "big") % len(adjectives)
    noun_idx = int.from_bytes(digest[4:8], "big") % len(nouns)
    return adjectives[adj_idx], nouns[noun_idx]


# ---------------------------------------------------------------------------
# URL-to-ID extraction
# ---------------------------------------------------------------------------

_SESSION_URL_PATTERN = re.compile(
    r"https?://[^/]+/sessions/([^/?#]+)",
)
_SESSION_ID_PATTERN = re.compile(r"[0-9a-fA-F-]+")


def extract_session_id(identifier: str) -> str:
    """Extract a bare session ID from a URL or Devin ID.

    Session URLs may include query parameters, fragments, or trailing path
    segments. A `devin-` prefix is removed when its suffix looks like a
    session ID. Other unrecognized input is returned unchanged.
    """
    match = _SESSION_URL_PATTERN.search(identifier)
    if match:
        candidate = _normalize_session_id(match.group(1))
        return candidate if candidate is not None else identifier

    # Also handle generic URLs where the last path segment is the ID.
    parsed = urlparse(identifier)
    if parsed.scheme in ("http", "https") and parsed.path:
        # Return last non-empty path segment.
        segments = [s for s in parsed.path.split("/") if s]
        candidate = segments[-1] if segments else identifier
        fallback = candidate
    else:
        candidate = identifier
        fallback = identifier
    normalized = _normalize_session_id(candidate)
    return normalized if normalized is not None else fallback


def _normalize_session_id(candidate: str) -> str | None:
    """Return a normalized session ID, or `None` for an invalid candidate."""
    if candidate.startswith("devin-"):
        candidate = candidate.removeprefix("devin-")
    return candidate if _SESSION_ID_PATTERN.fullmatch(candidate) else None


def generate_friendly_name(identifier: str) -> str:
    """Generate a deterministic human-friendly name from a string identifier.

    Args:
        identifier: Any string (e.g. a UUID, URL, session key).

    Returns a Title Case two-word name.
    """
    adjectives, nouns = _get_word_lists()
    adj, noun = _pick_pair(identifier, adjectives, nouns)
    return f"{adj} {noun}".title()


def get_namespace_size() -> int:
    """Return the total number of possible name combinations."""
    adjectives, nouns = _get_word_lists()
    return len(adjectives) * len(nouns)
