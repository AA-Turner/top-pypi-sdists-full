"""Stable, collision-proof file keys for the v2 PR review pipeline.

A ``fileKey`` is a deterministic identifier derived from a repository file path,
used consistently for prompt / answer / marker filenames so that every v2
artifact for a given file can be located by key.

Scheme (decision D8): ``<safe-slug>-<sha256[:8]>`` of the normalized repo path.

- The **slug** is a lowercased, filesystem-safe rendering of the path (readable).
- The **hash** is computed over the *case-preserved* normalized path, so two paths
  that differ only in case (``Foo.ts`` vs ``foo.ts``) produce **different** keys
  even though their slugs are identical — keeping the key collision-proof and
  safe on Windows' case-insensitive filesystem.
"""

from __future__ import annotations

import hashlib
import re

_NON_SLUG_CHARS = re.compile(r"[^a-z0-9]+")
_MAX_SLUG_LENGTH = 60
_FALLBACK_SLUG = "file"


def _normalize_for_key(file_path: str) -> str:
    """Normalize a repo path to a canonical case-preserved form for hashing.

    Converts backslashes to forward slashes and strips surrounding whitespace
    and leading/trailing slashes so that ``/src/a.ts`` and ``src/a.ts`` map to
    the same canonical string ``src/a.ts``.
    """
    return file_path.strip().replace("\\", "/").strip("/")


def build_file_key(file_path: str) -> str:
    """Build a stable, collision-proof file key for *file_path*.

    Args:
        file_path: Repository file path (any slash style, optional leading slash).

    Returns:
        A key of the form ``<safe-slug>-<sha256[:8]>``. The slug is lowercased
        and filesystem-safe; the 8-character hex hash disambiguates case-only
        differences and guards against slug collisions.
    """
    normalized = _normalize_for_key(file_path)
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:8]

    slug = _NON_SLUG_CHARS.sub("-", normalized.lower()).strip("-")
    if len(slug) > _MAX_SLUG_LENGTH:
        slug = slug[:_MAX_SLUG_LENGTH].strip("-")
    if not slug:
        slug = _FALLBACK_SLUG

    return f"{slug}-{digest}"
