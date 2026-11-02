"""Dry-run manifest builder utility.

Assembles a JSON manifest showing what operations *would* be performed,
without actually executing them.  The manifest has two top-level keys:
  - ``"issues"``: Array of issue entries (any nesting must already exist
    in the caller-supplied list).
  - ``"dependencies"``: Array of source→target blocking declarations.

Each entry includes ``"status": "dry-run"`` and the intended operation.
"""

from __future__ import annotations

from typing import Any


def build_dry_run_manifest(
    issues: list[dict[str, Any]],
    dependencies: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a hierarchical dry-run manifest.

    Args:
        issues: List of issue entries.  Each entry should contain at minimum:
            - ``title``: Issue title
            - ``issue_type``: Provider-neutral type
            - ``operation``: The API operation that would be performed
            - ``status``: Always ``"dry-run"``
            Optionally ``children``: nested list of child issue entries.
        dependencies: List of dependency entries.  Each should contain:
            - ``source``: Source issue identifier/title
            - ``target``: Target issue identifier/title
            - ``type``: Relationship type (e.g., ``"blocks"``)
            - ``operation``: The API operation that would be performed
            - ``status``: Always ``"dry-run"``

    Returns:
        A dict with ``"issues"`` and ``"dependencies"`` keys.
    """
    return {
        "issues": issues,
        "dependencies": dependencies,
    }
