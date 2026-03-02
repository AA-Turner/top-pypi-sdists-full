"""OpenClaw-style memory retrieval tools.

Provides three tools:
- ``memory_search`` — full-text search over MEMORY.md and daily logs
- ``memory_get`` — exact file content retrieval with line ranges
- ``remember`` — write memories routed through MemoryPolicy
"""

from dataclasses import asdict
from typing import Optional, Protocol, Union

from ..tools.base import BaseTool, ToolCategory, ToolResult
from .memory_index import MemoryIndex, SearchHit
from .memory_policy import classify_memory
from .memory_store import MemoryStore


class MemorySearchBackend(Protocol):
    """Protocol for memory search backends (SQLite or QMD)."""

    def search(self, query: str, limit: int = 5, timeout_ms: int = 3000) -> list[SearchHit]: ...
    def mark_dirty(self, path: str) -> None: ...
    def sync_now(self, reason: str = "boot") -> None: ...


class MemorySearchTool(BaseTool):
    """Search memory files for relevant information.

    Searches MEMORY.md and all daily logs via the FTS index.
    Returns snippets (max ~700 chars each), never full files.
    """

    name = "memory_search"
    category = ToolCategory.LEARNING
    description = (
        "Search your memory (MEMORY.md + daily logs) for stored information. "
        "Returns relevant snippets with file paths and line ranges."
    )

    def __init__(self, index: MemorySearchBackend) -> None:
        super().__init__(connection=False)
        self._index = index

    def get_schema(self) -> dict:
        return self._make_schema(
            properties={
                "query": {
                    "type": "string",
                    "description": "Search query — keywords or phrases to find in memory files.",
                },
            },
            required=["query"],
        )

    def execute(self, query: str = "", **kwargs) -> ToolResult:
        if not query.strip():
            return ToolResult.error_result("Query cannot be empty.")

        try:
            hits = self._index.search(query, limit=5, timeout_ms=3000)
        except Exception as exc:
            return ToolResult.error_result(f"Search failed: {exc}")

        if not hits:
            return ToolResult.success_result(
                data={"results": [], "query": query},
                suggestions=["Try broader keywords or check memory_get for a specific file."],
            )

        results = [asdict(h) for h in hits]
        return ToolResult.success_result(
            data={"results": results, "query": query, "count": len(results)},
        )


class MemoryGetTool(BaseTool):
    """Read exact content from a memory file.

    Only allows access to MEMORY.md and files under memory/.
    Supports optional line range for targeted reads.
    """

    name = "memory_get"
    category = ToolCategory.LEARNING
    description = (
        "Read exact content from a memory file. "
        "Only MEMORY.md and memory/*.md are accessible. "
        "Use startLine/nLines for targeted reads."
    )

    def __init__(self, store: MemoryStore) -> None:
        super().__init__(connection=False)
        self._store = store

    def get_schema(self) -> dict:
        return self._make_schema(
            properties={
                "path": {
                    "type": "string",
                    "description": (
                        "Relative path to the memory file. "
                        'E.g. "MEMORY.md" or "memory/2026-02-18.md".'
                    ),
                },
                "startLine": {
                    "type": "integer",
                    "description": "0-based line offset to start reading from. Default: 0 (beginning).",
                },
                "nLines": {
                    "type": "integer",
                    "description": "Number of lines to read. Default: 0 (all remaining).",
                },
            },
            required=["path"],
        )

    def execute(
        self,
        path: str = "",
        startLine: int = 0,
        nLines: int = 0,
        **kwargs,
    ) -> ToolResult:
        if not path.strip():
            return ToolResult.error_result("Path cannot be empty.")

        try:
            content = self._store.read_range(path, start_line=startLine, n_lines=nLines)
        except ValueError as exc:
            return ToolResult.error_result(str(exc))
        except FileNotFoundError:
            return ToolResult.error_result(
                f"File not found: {path}",
                suggestions=[
                    "Use memory_search to find available files.",
                    "Check the path — only MEMORY.md and memory/*.md are accessible.",
                ],
            )
        except Exception as exc:
            return ToolResult.error_result(f"Read failed: {exc}")

        return ToolResult.success_result(
            data={
                "path": path,
                "startLine": startLine,
                "nLines": nLines,
                "content": content,
                "lineCount": content.count("\n") + (1 if content else 0),
            },
        )


class RememberTool(BaseTool):
    """Store information in memory.

    Routes to either the daily log or MEMORY.md based on content analysis
    (or an explicit target). After writing, marks the file dirty in the
    search index.
    """

    name = "remember"
    category = ToolCategory.LEARNING
    description = (
        "Store information in memory. Routes to daily log (tasks, decisions) "
        "or MEMORY.md (durable preferences, facts) based on content. "
        "You can override routing with the 'target' parameter."
    )

    def __init__(self, store: MemoryStore, index: MemorySearchBackend) -> None:
        super().__init__(connection=False)
        self._store = store
        self._index = index

    def get_schema(self) -> dict:
        return self._make_schema(
            properties={
                "content": {
                    "type": "string",
                    "description": "The information to remember (markdown).",
                },
                "target": {
                    "type": "string",
                    "enum": ["daily", "longterm"],
                    "description": (
                        "Where to store: 'daily' (today's log) or 'longterm' (MEMORY.md). "
                        "If omitted, auto-classified based on content."
                    ),
                },
                "heading": {
                    "type": "string",
                    "description": "Optional heading for the memory block.",
                },
            },
            required=["content"],
        )

    def execute(
        self,
        content: str = "",
        target: Optional[str] = None,
        heading: Optional[str] = None,
        **kwargs,
    ) -> ToolResult:
        if not content.strip():
            return ToolResult.error_result("Content cannot be empty.")

        # Auto-classify if no explicit target
        if target is None:
            target = classify_memory(content)

        try:
            if target == "longterm":
                self._store.append_long_term(content, heading=heading)
                self._index.mark_dirty("MEMORY.md")
                location = "MEMORY.md"
            else:
                path = self._store.append_daily(content, heading=heading)
                rel_path = str(path.relative_to(self._store.workspace_dir))
                self._index.mark_dirty(rel_path)
                location = rel_path
        except Exception as exc:
            return ToolResult.error_result(f"Write failed: {exc}")

        return ToolResult.success_result(
            data={
                "target": target,
                "location": location,
                "message": f"Stored in {location}",
            },
        )
