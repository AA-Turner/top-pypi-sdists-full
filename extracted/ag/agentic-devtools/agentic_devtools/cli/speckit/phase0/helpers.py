"""Pure derivation helpers for the Speckit Phase 0 workflow core.

These functions are deterministic and free of state/config reads (except
:func:`resolve_phase_0_enabled`, which reads the repository configuration).
Keeping derivation pure guarantees that independent trigger and recovery runs
compute identical branch names, artifact paths, and issue keys (FR-003,
FR-010).
"""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.config import (
    ARTIFACT_PATH_TEMPLATE,
    BRANCH_NAME_TEMPLATE,
)

__all__ = [
    "derive_issue_key",
    "derive_branch_name",
    "derive_artifact_location",
    "resolve_phase_0_enabled",
]


def derive_issue_key(issue: int | str) -> str:
    """Derive the canonical Phase 0 issue key from an issue reference.

    The issue key is the bare GitHub issue number with no ``#`` prefix, used
    verbatim in both the branch name and the artifact path (FR-010).

    Args:
        issue: The source issue reference — an integer issue number or a string
            such as ``"1799"``, ``"#1799"``, or ``" 1799 "``.

    Returns:
        The bare issue number as a string (e.g., ``"1799"``).

    Raises:
        ValueError: If ``issue`` is not a positive integer once normalized
            (empty, non-numeric, zero, or negative values are rejected).
    """
    if isinstance(issue, bool):
        # bool is an int subclass; reject it explicitly to avoid True -> "1".
        raise ValueError(f"Invalid issue reference: {issue!r}")

    if isinstance(issue, int):
        number = issue
    else:
        text = issue.strip()
        if text.startswith("#"):
            text = text[1:].strip()
        if not text.isdigit():
            raise ValueError(f"Invalid issue reference: {issue!r}")
        number = int(text)

    if number <= 0:
        raise ValueError(f"Invalid issue reference: {issue!r}")

    return str(number)


def derive_branch_name(issue: int | str) -> str:
    """Derive the deterministic Phase 0 branch name for an issue (FR-010).

    Args:
        issue: The source issue reference (see :func:`derive_issue_key`).

    Returns:
        The branch name ``speckit/{issue-key}/phase-0-normalize``.

    Raises:
        ValueError: If the issue reference is invalid.
    """
    return BRANCH_NAME_TEMPLATE.format(issue_key=derive_issue_key(issue))


def derive_artifact_location(issue: int | str) -> str:
    """Derive the canonical ``issue.md`` path for an issue (FR-003).

    Args:
        issue: The source issue reference (see :func:`derive_issue_key`).

    Returns:
        The artifact path ``.speckit/issues/{issue-key}/issue.md``.

    Raises:
        ValueError: If the issue reference is invalid.
    """
    return ARTIFACT_PATH_TEMPLATE.format(issue_key=derive_issue_key(issue))


def resolve_phase_0_enabled(repo_path: str) -> bool:
    """Resolve whether Phase 0 is enabled for the repository (FR-001, FR-005).

    Reads ``platform.phase_0.enabled`` from the repository configuration,
    returning ``False`` when the setting is absent or disabled so that
    automation falls back to dispatching Phase 1 directly.

    Args:
        repo_path: Path to the root of the target repository.

    Returns:
        ``True`` when ``platform.phase_0.enabled`` is ``true``; ``False`` when
        it is ``false`` or absent.
    """
    from agentic_devtools.config import load_platform_config

    phase_0 = load_platform_config(repo_path).get("phase_0", {})
    return bool(phase_0.get("enabled", False))
