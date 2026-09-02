"""Issue type resolution and slug normalization.

Provides:
- slugify_type: Converts raw type strings to URL-safe slugs
- resolve_issue_type: 3-step priority chain for type resolution
"""

from __future__ import annotations

import re

from agentic_devtools.adapters.types import NormalizedIssue


def slugify_type(raw_type: str) -> str:
    """Convert a raw issue type string to a normalized slug.

    Algorithm (FR-004), applied in order:
    1. Strip leading/trailing whitespace
    2. Lowercase
    3. Replace whitespace sequences and forward slashes with a single hyphen
    4. Replace every remaining character that is not an ASCII lowercase letter
       (``a``-``z``), ASCII digit (``0``-``9``), or hyphen with a hyphen
    5. Collapse consecutive hyphens to a single hyphen
    6. Strip leading/trailing hyphens

    Args:
        raw_type: The raw issue type string.

    Returns:
        A normalized slug suitable for template matching. May be the empty
        string when the input contains no alphanumeric characters.
    """
    slug = raw_type.strip().lower()
    slug = re.sub(r"[\s/]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    slug = slug.strip("-")
    return slug


def resolve_issue_type(issue: NormalizedIssue, known_types: set[str]) -> str:
    """Resolve the issue type using the FR-005 priority chain.

    Priority (FR-005), operating only on already-normalized top-level fields:
    1. Top-level ``raw["issue_type"]`` when present and its slugified value is
       non-empty. This branch returns the slugified value even when it is NOT
       in ``known_types``, so template selection can fall back to
       ``issue-template.md`` for custom types. ``None`` is treated as absent
       (never passed to :func:`slugify_type`); an empty/whitespace-only value
       or one that slugifies to the empty string is treated as absent.
    2. The first label whose slug matches a ``known_types`` entry.
    3. The literal ``"task"`` as the final fallback.

    Provider-specific nesting (for example Jira's
    ``raw["fields"]["issuetype"]["name"]``) is NOT read here; adapters must
    normalize it into top-level ``raw["issue_type"]`` before resolution.

    Args:
        issue: The normalized issue to resolve type for.
        known_types: Set of registered type slugs from preset.yml.

    Returns:
        The resolved type slug.
    """
    # Step 1: top-level raw["issue_type"] (adapter-normalized), used even when
    # the slug is not in known_types so custom types fall back to the default.
    raw_type = issue.raw.get("issue_type")
    if isinstance(raw_type, str) and raw_type.strip():
        slug = slugify_type(raw_type)
        if slug:
            return slug

    # Step 2: label-based inference
    for label in issue.labels:
        slug = slugify_type(label)
        if slug in known_types:
            return slug

    # Step 3: default fallback
    return "task"
