"""Shared workflow definition resolution — find workflow YAML by ID or path.

Since #924 the authoritative resolver is
:func:`anteroom.services.workflow_registry.resolve_workflow`, which is
pack-aware. This module now exposes a thin back-compat shim:
:func:`resolve_workflow_path` for callers that pre-date the registry
surface and still want a bare ``Path`` return type with no database
awareness. New code should prefer ``resolve_workflow`` directly so
pack-sourced templates are discoverable.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection


def _package_root() -> Path:
    """Return the anteroom package root (src/anteroom/)."""
    return Path(__file__).parent.parent


def _is_safe_workflow_id(workflow_id: str) -> bool:
    """Check that a workflow ID is safe for path construction (no traversal)."""
    return ".." not in workflow_id and "/" not in workflow_id and "\\" not in workflow_id


def resolve_workflow_path(
    workflow_id: str,
    *,
    allow_filesystem: bool = True,
    db: ThreadSafeConnection | None = None,
) -> Path | None:
    """Resolve a workflow definition by ID or path (back-compat shim).

    Delegates to :func:`workflow_registry.resolve_workflow` and returns
    the resolved ``Path`` (the registry's ``WorkflowRef.path``). Kept
    for callers that haven't migrated to the pack-aware registry yet.
    """
    from .workflow_registry import resolve_workflow

    ref = resolve_workflow(workflow_id, db=db, allow_filesystem=allow_filesystem)
    return None if ref is None else ref.path


def builtin_workflow_dirs() -> list[Path]:
    """Return the list of directories where built-in workflows live."""
    pkg_root = _package_root()
    dirs = [pkg_root / "workflows"]
    pkg_examples = pkg_root / "workflows" / "examples"
    if pkg_examples.exists():
        dirs.append(pkg_examples)
    src_examples = pkg_root.parent.parent / "examples" / "workflows"
    if src_examples.exists():
        dirs.append(src_examples)
    return dirs
