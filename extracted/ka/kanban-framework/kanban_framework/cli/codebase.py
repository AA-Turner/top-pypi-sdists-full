"""CLI dispatch for kanban codebase commands.

Usage:
    kanban codebase index [--full]    Build or update code index
    kanban codebase search <query>    Search code nodes
    kanban codebase impact <node>     Change impact analysis
    kanban codebase overview          Architecture overview
    kanban codebase status            Index status

Requires config.json: {"code_index": {"backend": "code-review-graph"}}
Optional dependency: pip install kanban-framework[code-index]
"""

from __future__ import annotations

from pathlib import Path

_SETUP_HINT = (
    'Enable code indexing by adding to .kanban/config.json: '
    '{"code_index": {"backend": "code-review-graph"}}'
)


def dispatch(args: list[str]) -> dict:
    """Entry point for `kanban codebase` commands."""
    sub = args[0] if args else "status"

    if sub in ("--help", "-h", "help"):
        return {"commands": ["index", "search", "impact", "overview", "status"]}

    from kanban_framework.infra.filesystem import Filesystem
    from kanban_framework.infra.config import Config

    root = Filesystem.find_project_root()
    fs = Filesystem(root=root)
    cfg = Config(fs)
    backend_name = cfg.code_index_backend

    if not backend_name:
        return {
            "error": "code_index.backend not configured",
            "hint": _SETUP_HINT,
        }

    from kanban_framework.infra.code_index_backend import (
        resolve_code_index_backend,
        CodeIndexNotAvailableError,
    )

    try:
        backend = resolve_code_index_backend(backend_name)
    except CodeIndexNotAvailableError as exc:
        return {"error": str(exc)}

    repo_path = root

    if sub == "index":
        return _handle_index(backend, repo_path, args[1:])
    if sub == "search":
        return _handle_search(backend, repo_path, args[1:])
    if sub == "impact":
        return _handle_impact(backend, repo_path, args[1:])
    if sub == "overview":
        return _handle_overview(backend, repo_path)
    if sub == "status":
        return backend.status(repo_path)

    return {"error": f"unknown subcommand: {sub}", "available": ["index", "search", "impact", "overview", "status"]}


def _handle_index(backend, repo_path: Path, args: list[str]) -> dict:
    full = "--full" in args
    if full:
        result = backend.build(repo_path)
    else:
        status = backend.status(repo_path)
        if not status.get("indexed"):
            result = backend.build(repo_path)
        else:
            result = backend.update(repo_path)
    # Hint if index seems small (#376)
    node_count = result.get("node_count", 0)
    if node_count > 0 and node_count < 50:
        result["hint"] = (
            f"Only {node_count} nodes indexed — some directories may be excluded by .gitignore. "
            "Ensure all source directories are tracked by git."
        )
    return result


def _handle_search(backend, repo_path: Path, args: list[str]) -> dict:
    query = " ".join(args) if args else ""
    if not query:
        return {"error": "search requires a query argument", "usage": "kanban codebase search <query>"}
    limit = 20
    results = backend.search(query, repo_path, limit=limit)
    return {"query": query, "count": len(results), "results": results}


def _handle_impact(backend, repo_path: Path, args: list[str]) -> dict:
    if not args:
        return {"error": "impact requires a node name", "usage": "kanban codebase impact <node>"}
    node = args[0]
    depth = 2
    for a in args[1:]:
        if a.startswith("--depth="):
            try:
                depth = int(a.split("=", 1)[1])
            except ValueError:
                pass
    return backend.impact_radius(node, repo_path, depth=depth)


def _handle_overview(backend, repo_path: Path) -> dict:
    return backend.architecture_overview(repo_path)
