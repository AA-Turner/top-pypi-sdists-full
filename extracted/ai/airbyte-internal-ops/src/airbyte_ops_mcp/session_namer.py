# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Deterministic friendly-name generation from arbitrary string identifiers.

Generates human-friendly names by hashing an input string and mapping it to
curated word lists stored in a versioned YAML seed file. Two naming schemes
are currently shipped:

- **superhero**: adjective + hero/villain noun (e.g., "Speedy Avenger")
- **silly-buddy**: silly adjective + first name (e.g., "Smelly Fred")

Names are deterministic: the same input string always produces the same name
for a given scheme. The namespace is large enough (~60K+ combinations per
scheme) that collisions are unlikely for moderate volumes (~10K/month).

This module is intentionally generic — it operates on arbitrary string
identifiers, not specifically Devin sessions. Domain-specific wrappers
(e.g., the MCP tool layer) add context like "Devin" suffixes.
"""

from __future__ import annotations

import hashlib
import re
from enum import StrEnum
from functools import lru_cache
from importlib import resources
from typing import Any
from urllib.parse import urlparse

import yaml

# ---------------------------------------------------------------------------
# Naming scheme enum
# ---------------------------------------------------------------------------

_SEED_FILE_NAME = "random_name_seeds-v1.yaml"


class NamingScheme(StrEnum):
    """Available naming schemes."""

    SUPERHERO = "superhero"
    SILLY_BUDDY = "silly-buddy"


# ---------------------------------------------------------------------------
# Seed data loading
# ---------------------------------------------------------------------------

# Maps each scheme to (adjective_key, noun_key) in the YAML file.
_SCHEME_KEYS: dict[NamingScheme, tuple[str, str]] = {
    NamingScheme.SUPERHERO: ("superhero_adjectives", "superhero_nouns"),
    NamingScheme.SILLY_BUDDY: ("silly_buddy_adjectives", "silly_buddy_names"),
}


@lru_cache(maxsize=1)
def _load_seed_data() -> dict[str, Any]:
    """Load and cache the YAML seed file bundled with this package."""
    seed_file = resources.files("airbyte_ops_mcp").joinpath(_SEED_FILE_NAME)
    return yaml.safe_load(seed_file.read_text(encoding="utf-8"))


def _get_word_lists(scheme: NamingScheme) -> tuple[list[str], list[str]]:
    """Return (adjectives, nouns) for the given scheme."""
    data = _load_seed_data()
    adj_key, noun_key = _SCHEME_KEYS[scheme]
    return data[adj_key], data[noun_key]


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
    r"https?://[^/]+/sessions/([0-9a-fA-F-]+)",
)


def extract_session_id(identifier: str) -> str:
    """Extract a bare session ID from a string that may be a URL.

    If *identifier* looks like a Devin session URL
    (e.g. `https://app.devin.ai/sessions/abc123`), the trailing path
    segment is returned.  Otherwise the original string is returned
    unchanged.
    """
    match = _SESSION_URL_PATTERN.search(identifier)
    if match:
        return match.group(1)
    # Also handle generic URLs where the last path segment is the ID.
    parsed = urlparse(identifier)
    if parsed.scheme in ("http", "https") and parsed.path:
        # Return last non-empty path segment.
        segments = [s for s in parsed.path.split("/") if s]
        if segments:
            return segments[-1]
    return identifier


def generate_friendly_name(
    identifier: str,
    scheme: NamingScheme = NamingScheme.SILLY_BUDDY,
) -> str:
    """Generate a deterministic human-friendly name from a string identifier.

    Args:
        identifier: Any string (e.g. a UUID, URL, session key).
        scheme: Which naming scheme to use.

    Returns:
        A Title Case two-word name such as `"Speedy Avenger"`.
    """
    adjectives, nouns = _get_word_lists(scheme)
    adj, noun = _pick_pair(identifier, adjectives, nouns)
    return f"{adj} {noun}".title()


def generate_all_names(identifier: str) -> dict[str, str]:
    """Generate names for an identifier across all schemes.

    Args:
        identifier: Any string to name.

    Returns:
        A dict mapping scheme value to generated name (Title Case).
    """
    return {
        scheme.value: generate_friendly_name(identifier, scheme)
        for scheme in NamingScheme
    }


def get_namespace_size(scheme: NamingScheme) -> int:
    """Return the total number of possible name combinations for a scheme."""
    adjectives, nouns = _get_word_lists(scheme)
    return len(adjectives) * len(nouns)
