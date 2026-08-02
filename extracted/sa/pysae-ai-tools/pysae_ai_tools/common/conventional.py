"""Conventional Commits type vocabulary, shared across the package.

Single source of truth for the commit/MR-title types Pysae accepts. The
per-repo commitlint configs (JS) and conventional-pre-commit hooks (Python)
mirror this exact set.
"""

import re

# Commit message / MR title types accepted by commitlint: the Conventional
# Commits base plus Pysae's ``tech`` and the commit-only ``release``. Never
# ``bump`` (removed).
COMMIT_TYPES: tuple[str, ...] = (
    "build",
    "chore",
    "ci",
    "docs",
    "feat",
    "fix",
    "perf",
    "refactor",
    "revert",
    "style",
    "test",
    "tech",
    "release",
)

# Changelog entry types: the same set minus ``release`` (a release commit
# produces no changelog entry).
CHANGELOG_TYPES: tuple[str, ...] = tuple(t for t in COMMIT_TYPES if t != "release")

# A single-line Conventional Commits header: ``type(scope)!: subject``. The
# scope and the breaking-change ``!`` are optional; the subject must be
# non-empty and separated from the colon by a space.
_HEADER_RE = re.compile(r"^(?P<type>[a-z]+)(?:\([^)]+\))?!?: \S.*$")


def is_valid_commit_header(header: str, types: tuple[str, ...] = COMMIT_TYPES) -> bool:
    """Return True if ``header`` is a valid Conventional Commits header.

    Checks the ``type(scope)!: subject`` shape and that ``type`` is one of the
    allowed ``types`` (defaults to the full commit/MR-title set).
    """
    match = _HEADER_RE.match(header.strip())
    return match is not None and match.group("type") in types
