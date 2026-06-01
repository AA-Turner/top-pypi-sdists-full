"""Code index backend abstraction — pluggable codebase structure analysis.

Same middleware pattern as stats_backend.py:
  CLI commands / Agent queries (unchanged)
        ↓
  CodeIndexBackend (Protocol)
    └─ CodeReviewGraphBackend → delegate to code-review-graph (Tree-sitter + graph DB)

Switch via config.json: {"code_index": {"backend": "code-review-graph"}}

Feature is entirely optional — not configured means not active.
"""

from __future__ import annotations

import sqlite3
import sys
import time
from pathlib import Path
from typing import Protocol, runtime_checkable


class CodeIndexNotAvailableError(RuntimeError):
    """Raised when the selected code index backend dependency is not installed."""


@runtime_checkable
class CodeIndexBackend(Protocol):
    """Protocol for code indexing backends."""

    def build(self, repo_path: Path) -> dict: ...
    def update(self, repo_path: Path) -> dict: ...
    def status(self, repo_path: Path) -> dict: ...
    def search(self, query: str, repo_path: Path, *, limit: int = 20) -> list[dict]: ...
    def impact_radius(self, node_name: str, repo_path: Path, *, depth: int = 2) -> dict: ...
    def architecture_overview(self, repo_path: Path) -> dict: ...


# ---------------------------------------------------------------------------
# code-review-graph adapter
# ---------------------------------------------------------------------------

_CRG_GRAPH_DB_REL = Path(".code-review-graph") / "graph.db"

_MIN_PYTHON = (3, 10)


def _check_crg_available():
    """Verify code-review-graph is importable and Python version is sufficient."""
    if sys.version_info < _MIN_PYTHON:
        raise CodeIndexNotAvailableError(
            f"code-review-graph requires Python >= {_MIN_PYTHON[0]}.{_MIN_PYTHON[1]}, "
            f"current: {sys.version_info.major}.{sys.version_info.minor}. "
            f"Upgrade Python or use a venv with Python 3.10+."
        )
    try:
        import code_review_graph  # noqa: F401
    except ImportError:
        raise CodeIndexNotAvailableError(
            "code-review-graph is not installed. "
            "Install with: pip install code-review-graph"
        )


def _crg_db_path(repo_path: Path) -> Path:
    return repo_path / _CRG_GRAPH_DB_REL


def _crg_main():
    """Lazy import of code_review_graph.main (avoids import cost until needed)."""
    from code_review_graph import main as crg_main
    return crg_main


class CodeReviewGraphBackend:
    """Adapter for code-review-graph.

    Uses SQLite-based graph database at .code-review-graph/graph.db.
    Nodes: File, Class, Function, Type, Test.
    Edges: CALLS, IMPORTS, INHERITS, IMPLEMENTS, CONTAINS, TESTED_BY, etc.
    """

    def __init__(self) -> None:
        _check_crg_available()

    # ── Build / Update / Status ───────────────────────────────────────

    def build(self, repo_path: Path) -> dict:
        crg = _crg_main()
        t0 = time.monotonic()
        result = crg.build_or_update_graph(full_rebuild=True, repo_root=str(repo_path))
        elapsed = round(time.monotonic() - t0, 2)
        counts = self._count_graph(_crg_db_path(repo_path))
        return {
            "indexed": True,
            "node_count": counts[0],
            "edge_count": counts[1],
            "elapsed_seconds": elapsed,
            "flows": result.get("flows_detected", 0),
            "communities": result.get("communities_detected", 0),
        }

    def update(self, repo_path: Path) -> dict:
        crg = _crg_main()
        t0 = time.monotonic()
        result = crg.build_or_update_graph(full_rebuild=False, repo_root=str(repo_path))
        elapsed = round(time.monotonic() - t0, 2)
        counts = self._count_graph(_crg_db_path(repo_path))
        return {
            "indexed": True,
            "node_count": counts[0],
            "edge_count": counts[1],
            "elapsed_seconds": elapsed,
            "files_updated": result.get("files_updated", 0),
        }

    def status(self, repo_path: Path) -> dict:
        db = _crg_db_path(repo_path)
        if not db.is_file():
            return {
                "indexed": False,
                "node_count": 0,
                "edge_count": 0,
                "db_path": str(db),
                "hint": "Run 'kanban codebase index' to build the code graph.",
            }
        counts = self._count_graph(db)
        return {
            "indexed": True,
            "node_count": counts[0],
            "edge_count": counts[1],
            "db_path": str(db),
            "db_size_kb": round(db.stat().st_size / 1024, 1),
        }

    # ── Search / Impact / Architecture ────────────────────────────────

    def search(self, query: str, repo_path: Path, *, limit: int = 20) -> list[dict]:
        crg = _crg_main()
        # Try semantic search first (requires embeddings)
        try:
            result = crg.semantic_search_nodes(
                query=query, limit=limit, repo_root=str(repo_path),
            )
            if result.get("nodes"):
                return self._normalize_search(result["nodes"])
        except Exception:
            pass
        # Fallback: query graph by name pattern
        try:
            result = crg.query_graph(
                pattern=query, target="name", repo_root=str(repo_path),
            )
            if result.get("nodes"):
                return self._normalize_search(result["nodes"])
        except Exception:
            pass
        # Final fallback: direct SQLite FTS search on graph.db
        return self._sqlite_search(query, _crg_db_path(repo_path), limit)

    def impact_radius(self, node_name: str, repo_path: Path, *, depth: int = 2) -> dict:
        crg = _crg_main()
        db = _crg_db_path(repo_path)
        # Resolve node_name to file path if it's a function/class (#375)
        files = self._resolve_to_files(node_name, db)
        if not files:
            return {"center": node_name, "affected_nodes": 0, "affected_files": [],
                    "hint": f"'{node_name}' not found in index. Try a file path."}
        try:
            result = crg.get_impact_radius(
                changed_files=files,
                max_depth=depth,
                repo_root=str(repo_path),
            )
            result["center"] = node_name
            result["resolved_files"] = files
            return result
        except Exception:
            return {"center": node_name, "affected_nodes": 0, "affected_files": files}

    def architecture_overview(self, repo_path: Path) -> dict:
        crg = _crg_main()
        # Ensure postprocessing has run
        try:
            crg.run_postprocess(flows=True, communities=True, fts=True, repo_root=str(repo_path))
        except Exception:
            pass
        stats = crg.list_graph_stats(repo_root=str(repo_path))
        overview = crg.get_architecture_overview_func(repo_root=str(repo_path))
        communities = crg.list_communities_func(sort_by="size", detail_level="minimal", repo_root=str(repo_path))
        hubs = crg.get_hub_nodes_func(top_n=15, repo_root=str(repo_path))
        flows = crg.list_flows(sort_by="criticality", limit=10, repo_root=str(repo_path))

        return {
            "nodes_by_kind": stats.get("nodes_by_kind", {}),
            "edges_by_kind": stats.get("edges_by_kind", {}),
            "files_count": stats.get("files_count", 0),
            "communities": [
                {
                    "name": c.get("name", ""),
                    "size": c.get("size", 0),
                    "cohesion": round(c.get("cohesion", 0), 3),
                    "description": c.get("description", ""),
                }
                for c in communities.get("communities", [])
            ],
            "hub_nodes": [
                {
                    "name": n.get("name", ""),
                    "kind": n.get("kind", ""),
                    "in_degree": n.get("in_degree", 0),
                    "out_degree": n.get("out_degree", 0),
                    "file": _short_path(n.get("file", "")),
                }
                for n in hubs.get("hub_nodes", [])
                if n.get("kind") != "Test"
            ],
            "top_flows": [
                {
                    "name": f.get("name", ""),
                    "depth": f.get("depth", 0),
                    "nodes": f.get("node_count", 0),
                    "files": f.get("file_count", 0),
                    "criticality": round(f.get("criticality", 0), 3),
                }
                for f in flows.get("flows", [])
            ],
        }

    # ── Helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _count_graph(db_path: Path) -> tuple[int, int]:
        if not db_path.is_file():
            return (0, 0)
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            nodes = conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
            edges = conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
            conn.close()
            return (nodes, edges)
        except Exception:
            return (0, 0)

    @staticmethod
    def _normalize_search(nodes) -> list[dict]:
        out: list[dict] = []
        for r in (nodes or []):
            if isinstance(r, dict):
                out.append({
                    "name": r.get("name", ""),
                    "kind": r.get("kind", ""),
                    "file_path": _short_path(r.get("file_path", r.get("file", ""))),
                    "line_start": r.get("line_start"),
                    "line_end": r.get("line_end"),
                    "score": r.get("score", 0),
                })
        return out

    @staticmethod
    def _resolve_to_files(node_name: str, db_path: Path) -> list[str]:
        """Resolve a function/class name to its containing file paths. (#375)"""
        if not db_path.is_file():
            # If node_name looks like a file path, return as-is
            if "/" in node_name or node_name.endswith(".py"):
                return [node_name]
            return []
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            rows = conn.execute(
                "SELECT DISTINCT file_path FROM nodes "
                "WHERE name LIKE ? AND kind NOT IN ('Test', 'File') "
                "LIMIT 10",
                (f"%{node_name}%",),
            ).fetchall()
            conn.close()
            if rows:
                return [r[0] for r in rows if r[0]]
            # Fallback: if node_name looks like a file path, return as-is
            if "/" in node_name or node_name.endswith(".py"):
                return [node_name]
            return []
        except Exception:
            if "/" in node_name or node_name.endswith(".py"):
                return [node_name]
            return []

    @staticmethod
    def _sqlite_search(query: str, db_path: Path, limit: int) -> list[dict]:
        """Multi-strategy search on graph.db: FTS5 → multi-column LIKE."""
        if not db_path.is_file():
            return []
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            _EXCLUDE_KINDS = ("Test", "File")

            # Strategy 1: FTS5 full-text search across name/qualified_name/signature/file_path
            rows = _fts5_search(conn, query, _EXCLUDE_KINDS, limit)
            if not rows:
                # Strategy 2: Multi-column LIKE fallback
                rows = _like_search(conn, query, _EXCLUDE_KINDS, limit)
            conn.close()
            return rows
        except Exception:
            return []


def _fts5_search(conn, query: str, exclude_kinds: tuple, limit: int) -> list[dict]:
    """FTS5 full-text search on nodes_fts (name, qualified_name, file_path, signature)."""
    fts_query = _escape_fts(query)
    if not fts_query:
        return []
    try:
        rows = conn.execute(
            "SELECT n.name, n.kind, n.file_path, n.line_start, n.line_end "
            "FROM nodes_fts f JOIN nodes n ON f.rowid = n.id "
            "WHERE nodes_fts MATCH ? AND n.kind NOT IN (?, ?) "
            "ORDER BY bm25(nodes_fts) LIMIT ?",
            (fts_query, *exclude_kinds, limit),
        ).fetchall()
    except Exception:
        return []
    return _format_search_rows(rows, score_base=0.8)


def _like_search(conn, query: str, exclude_kinds: tuple, limit: int) -> list[dict]:
    """Multi-column LIKE search across name, qualified_name, signature."""
    try:
        rows = conn.execute(
            "SELECT name, kind, file_path, line_start, line_end FROM nodes "
            "WHERE (name LIKE ? OR qualified_name LIKE ? OR signature LIKE ?) "
            "AND kind NOT IN (?, ?) "
            "ORDER BY CASE kind WHEN 'Class' THEN 0 WHEN 'Function' THEN 1 "
            "WHEN 'Type' THEN 2 ELSE 3 END, name LIMIT ?",
            (f"%{query}%", f"%{query}%", f"%{query}%", *exclude_kinds, limit),
        ).fetchall()
    except Exception:
        return []
    return _format_search_rows(rows, score_base=0.5)


def _escape_fts(query: str) -> str:
    """Escape special FTS5 characters and build OR query for each token."""
    import re
    tokens = re.split(r'\s+', query.strip())
    if not tokens:
        return ""
    parts = []
    for t in tokens:
        escaped = t.replace('"', '""')
        parts.append(f'"{escaped}"')
    return " OR ".join(parts)


def _format_search_rows(rows, score_base: float) -> list[dict]:
    return [
        {
            "name": r[0], "kind": r[1],
            "file_path": _short_path(r[2] or ""),
            "line_start": r[3], "line_end": r[4],
            "score": score_base,
        }
        for r in rows
    ]


def _short_path(path_str: str) -> str:
    """Shorten absolute path to relative from kanban_framework/."""
    marker = "kanban_framework/"
    idx = path_str.find(marker)
    if idx >= 0:
        return path_str[idx:]
    return path_str.rsplit("/", 1)[-1] if "/" in path_str else path_str


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

CODE_INDEX_BACKEND_REGISTRY: dict[str, type] = {
    "code-review-graph": CodeReviewGraphBackend,
    "review_graph": CodeReviewGraphBackend,       # backward compat
    "code_review_graph": CodeReviewGraphBackend,   # backward compat
}


def resolve_code_index_backend(name: str) -> CodeIndexBackend:
    """Resolve a code index backend by name.

    Supported backends (name = project name):
    - "code-review-graph" — Tree-sitter + SQLite graph DB
    - "codegraph" — placeholder for mainstream codegraph integration

    Raises CodeIndexNotAvailableError if the backend or its dependency
    is not installed (including Python version check).
    """
    if name == "codegraph":
        raise CodeIndexNotAvailableError(
            "Backend 'codegraph' is not yet implemented. "
            "Use 'code-review-graph' for Tree-sitter based indexing."
        )
    cls = CODE_INDEX_BACKEND_REGISTRY.get(name)
    if cls is None:
        raise CodeIndexNotAvailableError(
            f"Unknown code index backend: '{name}'. "
            f"Available: {list(CODE_INDEX_BACKEND_REGISTRY.keys())}"
        )
    return cls()
