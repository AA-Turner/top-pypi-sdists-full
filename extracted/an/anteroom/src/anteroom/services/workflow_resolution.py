"""Shared workflow definition resolution — find workflow YAML by ID or path.

Extracted from cli/workflow_cli.py so routers, scheduler, and CLI can all
resolve workflow definitions without duplicating lookup logic.
"""

from __future__ import annotations

from pathlib import Path


def _package_root() -> Path:
    """Return the anteroom package root (src/anteroom/)."""
    return Path(__file__).parent.parent


def _is_safe_workflow_id(workflow_id: str) -> bool:
    """Check that a workflow ID is safe for path construction (no traversal)."""
    return ".." not in workflow_id and "/" not in workflow_id and "\\" not in workflow_id


def resolve_workflow_path(workflow_id: str, *, allow_filesystem: bool = True) -> Path | None:
    """Resolve a workflow definition by ID or path.

    Search order:
    1. Exact filesystem path (if it exists and ends in .yaml/.yml) — only when allow_filesystem=True
    2. Package examples: workflows/examples/ inside the installed package
    3. Source-tree examples: examples/workflows/ (for development)
    4. Built-in workflows: workflows/ inside the package

    Set allow_filesystem=False for web API callers to prevent path traversal.
    ID-based lookups always reject traversal characters (/, \\, ..).
    """
    # Direct filesystem path — CLI only, rejected for web API callers
    if allow_filesystem:
        candidate = Path(workflow_id)
        if candidate.exists() and candidate.suffix in (".yaml", ".yml"):
            return candidate

    # ID-based lookups: reject traversal characters
    if not _is_safe_workflow_id(workflow_id):
        return None

    pkg_root = _package_root()

    # Package-shipped examples (works in installed packages)
    pkg_example_path = pkg_root / "workflows" / "examples" / f"{workflow_id}.yaml"
    if pkg_example_path.exists():
        return pkg_example_path

    # Source-tree examples (works in development/editable installs)
    src_examples_dir = pkg_root.parent.parent / "examples" / "workflows"
    src_example_path = src_examples_dir / f"{workflow_id}.yaml"
    if src_example_path.exists():
        return src_example_path

    # Built-in workflows (generic, shipped in package)
    builtin_path = pkg_root / "workflows" / f"{workflow_id}.yaml"
    if builtin_path.exists():
        return builtin_path

    return None


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
