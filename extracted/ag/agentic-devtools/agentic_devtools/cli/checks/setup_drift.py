"""Pure-function drift detection for setup-expectations synchronization.

Determines whether a change set that touches setup source files also includes
a corresponding update under ``docs/setup-expectations/``.  The logic is
entirely deterministic for a given input list — no filesystem or git access
is performed by :func:`check_drift`.

:func:`ensure_placeholder_docs` is a separate precondition helper (FR-008)
that ensures at least one non-empty placeholder doc exists under the docs
directory unless that placeholder path was explicitly deleted or renamed
away in the current change set.  It is never called by :func:`check_drift`
itself.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fnmatch import fnmatchcase
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SETUP_SOURCE_GLOBS: tuple[str, ...] = (
    "agentic_devtools/cli/setup/**",
    "agentic_devtools/skill_injector.py",
    "agentic_devtools/cli/setup/script_generators/**",
)
"""Glob patterns identifying setup source files (FR-002)."""

SETUP_DOCS_PREFIX: str = "docs/setup-expectations/"
"""Path prefix for setup expectations documentation."""

_PLACEHOLDER_FILENAMES: tuple[str, ...] = ("README.md", "agdt-setup.md")
"""Recognised placeholder document filenames inside *docs_dir*."""


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DriftResult:
    """Outcome of :func:`check_drift`.

    Attributes:
        passed: ``True`` when no drift is detected.
        triggering_files: Setup source files that triggered the check
            (empty when *passed* is ``True``).
        message: Human-readable explanation of the result.
    """

    passed: bool
    triggering_files: list[str] = field(default_factory=list)
    message: str = ""


@dataclass(frozen=True)
class EnsureResult:
    """Outcome of :func:`ensure_placeholder_docs`.

    Attributes:
        created: Paths of placeholder files created by this call.
        already_present: Paths of placeholder files that were already
            present and non-empty.
    """

    created: list[str] = field(default_factory=list)
    already_present: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def _normalize_path(p: str) -> str:
    """Normalize *p* to a POSIX-style repository-relative path.

    * Backslashes are replaced with forward slashes.
    * Leading ``./`` is stripped.
    * Trailing slashes are stripped.
    """
    p = p.replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return p.rstrip("/")


def _normalize_paths(paths: list[str]) -> list[str]:
    """Normalize, deduplicate, and sort *paths*."""
    seen: set[str] = set()
    result: list[str] = []
    for raw in paths:
        normed = _normalize_path(raw)
        if normed and normed not in seen:
            seen.add(normed)
            result.append(normed)
    result.sort()
    return result


def _is_setup_source(path: str) -> bool:
    """Return ``True`` if *path* matches any :data:`SETUP_SOURCE_GLOBS`."""
    for glob in SETUP_SOURCE_GLOBS:
        if fnmatchcase(path, glob):
            return True
    return False


def _is_setup_doc(path: str) -> bool:
    """Return ``True`` if *path* is under :data:`SETUP_DOCS_PREFIX`."""
    return path.startswith(SETUP_DOCS_PREFIX)


# ---------------------------------------------------------------------------
# Pure drift check
# ---------------------------------------------------------------------------


def check_drift(changed_files: list[str]) -> DriftResult:
    """Determine whether setup source changes are accompanied by doc updates.

    Args:
        changed_files: Repository-relative paths of files changed in a PR.

    Returns:
        A :class:`DriftResult` indicating pass/fail with details.

    The function is pure: it performs no I/O and is deterministic for a
    given *changed_files* input.
    """
    normed = _normalize_paths(changed_files)

    triggering: list[str] = []
    has_doc_change = False

    for p in normed:
        if _is_setup_doc(p):
            has_doc_change = True
        if _is_setup_source(p):
            triggering.append(p)

    if not triggering:
        return DriftResult(passed=True, message="No setup source files changed.")

    if has_doc_change:
        return DriftResult(
            passed=True,
            message="Setup source changes accompanied by docs/setup-expectations/ update.",
        )

    file_list = "\n".join(f"  - {f}" for f in triggering)
    return DriftResult(
        passed=False,
        triggering_files=triggering,
        message=(
            "Setup-expectations drift detected: setup source files changed "
            "without a same-PR update under docs/setup-expectations/.\n"
            f"Triggering files:\n{file_list}\n"
            "Add or update a file under docs/setup-expectations/ in the same PR."
        ),
    )


# ---------------------------------------------------------------------------
# Placeholder-doc precondition (FR-008)
# ---------------------------------------------------------------------------


def ensure_placeholder_docs(
    docs_dir: Path,
    deleted_paths: list[str] | None = None,
) -> EnsureResult:
    """Ensure at least one non-empty placeholder doc exists under *docs_dir*.

    Args:
        docs_dir: Path to the ``docs/setup-expectations/`` directory.
        deleted_paths: Repository-relative paths deleted or renamed away in
            the current change set.  Placeholders appearing here are not
            auto-recreated.

    Returns:
        An :class:`EnsureResult` recording created and already-present files.

    Raises:
        ValueError: When deleted/renamed/empty combinations leave zero valid
            (non-empty, non-deleted) placeholders and auto-creation is blocked
            because the placeholder path appears in *deleted_paths*.
    """
    deleted_set: set[str] = set()
    if deleted_paths:
        deleted_set = {_normalize_path(p) for p in deleted_paths}

    already_present: list[str] = []

    for name in _PLACEHOLDER_FILENAMES:
        rel = f"{SETUP_DOCS_PREFIX}{name}"
        full = docs_dir / name

        if _normalize_path(rel) in deleted_set:
            # Explicitly deleted/renamed away — skip.
            continue

        if full.is_file() and full.read_text(encoding="utf-8").strip():
            already_present.append(rel)

    if already_present:
        # At least one non-empty placeholder doc remains and was not deleted.
        return EnsureResult(already_present=already_present)

    # No valid placeholder remains.  Try to create README.md if not deleted.
    readme_rel = f"{SETUP_DOCS_PREFIX}README.md"
    if _normalize_path(readme_rel) in deleted_set:
        raise ValueError(
            "No non-empty placeholder doc remains under "
            f"{SETUP_DOCS_PREFIX} and auto-creation is blocked because "
            "the placeholder path(s) appear in deleted_paths."
        )

    docs_dir.mkdir(parents=True, exist_ok=True)
    readme_path = docs_dir / "README.md"
    readme_path.write_text(
        "# Setup Expectations\n\nPlaceholder — see sibling docs for details.\n",
        encoding="utf-8",
    )
    return EnsureResult(created=[readme_rel])
