"""Public versioning domain shared by ``changelog`` and ``release_notes``.

Release-tag semantics live here — the regexes, the base/suffix split, the
hotfix vs. store-skipping-prerelease classification, and the prerelease
predecessor lookup used when coalescing a version line into a single section.

This module is the single owner of that logic: ``changelog`` and
``release_notes`` (and the ``ci release`` commands) import its **public** API
instead of reaching for each other's private symbols, so an internal refactor
of either file can no longer break the other.
"""

import re

RELEASE_TAG_RE = re.compile(r"^v\d+\.\d+\.\d+(?:-[0-9A-Za-z][0-9A-Za-z.-]*)?$")
"""A release tag: strict final semver, or a prerelease with a ``-<label>[.<N>]`` suffix."""

TAG_BASE_RE = re.compile(r"^(v\d+\.\d+\.\d+)(?:-[0-9A-Za-z][0-9A-Za-z.-]*)?$")

# A *hotfix* suffix marks a store-bound post-release build of the **same** X.Y.Z:
# an explicit ``-hotfix.N`` or the bare ``-N`` shorthand (``v5.3.16-1``). It mirrors
# the Android versionCode scheme — a hotfix stays at the final stage (7) and is
# published to the stores like a final release — unlike the alpha/beta/rc
# prereleases, which are markdown-only and never reach the stores. The number,
# when present, is ≥ 1 (``…700`` already belongs to the bare release).
HOTFIX_SUFFIX_RE = re.compile(r"^(?:hotfix(?:\.\d+)?|\d+)$", re.IGNORECASE)
TAG_SUFFIX_RE = re.compile(r"^v\d+\.\d+\.\d+-(?P<suffix>[0-9A-Za-z][0-9A-Za-z.-]*)$")


def tag_base(tag: str) -> str | None:
    """Return the final-release base of ``tag`` (``v6.0.0-beta.1`` → ``v6.0.0``), or None."""
    match = TAG_BASE_RE.match(tag)
    return match.group(1) if match else None


def tag_suffix(tag: str) -> str | None:
    """Return the prerelease suffix of ``tag`` (``v6.0.0-beta.1`` → ``beta.1``), or None."""
    match = TAG_SUFFIX_RE.match(tag)
    return match.group("suffix") if match else None


def is_hotfix_tag(tag: str) -> bool:
    """True when ``tag`` is a store-bound hotfix build (``-hotfix.N`` or bare ``-N``).

    A hotfix ships the full store release notes and publishes to the stores, like a
    final release — it is **not** a markdown-only beta. See :data:`HOTFIX_SUFFIX_RE`.
    """
    suffix = tag_suffix(tag)
    return suffix is not None and HOTFIX_SUFFIX_RE.match(suffix) is not None


def is_store_skipping_prerelease(tag: str) -> bool:
    """True for a prerelease that must NOT reach the stores — alpha/beta/rc, not a hotfix.

    These are exactly the versions that get markdown-only release notes and skip
    store publication. A final release (no suffix) and a hotfix both return False.
    """
    base = tag_base(tag)
    return base is not None and base != tag and not is_hotfix_tag(tag)


def find_prerelease_predecessor(content: str, base: str, exclude_tag: str) -> re.Match[str] | None:
    """Locate a ``## [<base>-<label>…] DATE`` prerelease section to coalesce into.

    A prerelease release (``v6.0.0-beta.2``) or the final one (``v6.0.0``) absorbs
    the single section of an earlier prerelease of the **same base** (``v6.0.0-beta.1``)
    rather than stacking a new one — so a version line keeps exactly one section.
    The exact-``tag`` section (handled by ``find_existing_section``) is skipped
    via ``exclude_tag``. A *hotfix* section (``v5.3.16-1``) is never a predecessor:
    a hotfix is a standalone release, so it is neither coalesced into nor dropped.
    Returns ``None`` when no such predecessor exists.
    """
    pattern = re.compile(
        rf"^##\s*\[(?P<tag>{re.escape(base)}-[^\]]+)\]\s*(?P<date>[^\n]*)\n(?P<body>.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    for match in pattern.finditer(content):
        if match.group("tag") != exclude_tag and not is_hotfix_tag(match.group("tag")):
            return match
    return None
