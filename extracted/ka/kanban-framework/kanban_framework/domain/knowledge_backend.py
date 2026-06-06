"""Knowledge backend adapter protocol and built-in implementations.

Defines a standard interface for knowledge base backends so the kanban
framework can switch between different storage engines (SQLite FTS5,
LightRAG, KAG, etc.) without changing agent prompts or CLI commands.
"""

from __future__ import annotations
from typing import Protocol, runtime_checkable

# Re-exports for backward compatibility
from kanban_framework.domain.knowledge_multi_backend import MultiBackend  # noqa: F401
from kanban_framework.domain.knowledge_share_backend import ShareBackend  # noqa: F401


@runtime_checkable
class KnowledgeBackend(Protocol):
    """Protocol that all knowledge backend adapters must implement."""

    def search(self, keyword: str, limit: int = 20, *, biz_context: str | None = None) -> list[dict]:
        """Full-text keyword search.

        Returns list of dicts, each containing at minimum:
          {id, title, content, relevance (0-1 normalized), score (raw), ...}
        """
        ...

    def search_semantic(self, query: str, limit: int = 20, *, biz_context: str | None = None) -> list[dict]:
        """Semantic (vector embedding) search.

        Returns list of dicts with 'relevance' (0-1) field.
        """
        ...

    def search_hybrid(self, keyword: str, limit: int = 20, *, biz_context: str | None = None) -> list[dict]:
        """Hybrid search combining keyword and semantic results.

        Returns list of dicts with 'relevance' (0-1) field.
        """
        ...

    def add_entry(self, **kwargs) -> dict:
        """Add a knowledge entry. Returns the created entry dict."""
        ...

    def list_entries(
        self, domain: str | None = None, category: str | None = None,
        status: str = "active", limit: int = 50, offset: int = 0,
        biz_context: str | None = None,
    ) -> list[dict]:
        """List entries with optional filters."""
        ...

    def get_entry(self, entry_id: str) -> dict | None:
        """Get a single entry by ID, or None if not found."""
        ...


class BuiltinBackend:
    """Adapter wrapping the existing KnowledgeManager's storage methods."""

    def __init__(self, knowledge_manager):
        self._km = knowledge_manager

    def search(self, keyword: str, limit: int = 20, *, biz_context: str | None = None) -> list[dict]:
        return self._km._search_fts(keyword, limit=limit, biz_context=biz_context)

    def search_semantic(self, query: str, limit: int = 20, *, biz_context: str | None = None) -> list[dict]:
        return self._km._search_semantic(query, limit=limit, biz_context=biz_context)

    def search_hybrid(self, keyword: str, limit: int = 20, *, biz_context: str | None = None) -> list[dict]:
        return self._km._search_hybrid(keyword, limit=limit, biz_context=biz_context)

    def add_entry(self, **kwargs) -> dict:
        return self._km._add_entry_internal(**kwargs)

    def list_entries(
        self, domain: str | None = None, category: str | None = None,
        status: str = "active", limit: int = 50, offset: int = 0,
        biz_context: str | None = None,
    ) -> list[dict]:
        return self._km._list_entries_internal(
            domain=domain, category=category, status=status,
            limit=limit, offset=offset, biz_context=biz_context,
        )

    def get_entry(self, entry_id: str) -> dict | None:
        return self._km._get_entry_internal(entry_id)


class MemoryBackend:
    """In-memory dict backend for testing and protocol validation."""

    def __init__(self):
        self._entries: dict[str, dict] = {}

    def search(self, keyword: str, limit: int = 20, *, biz_context: str | None = None) -> list[dict]:
        kw = keyword.lower()
        results = []
        for e in self._entries.values():
            if kw in e.get("title", "").lower() or kw in e.get("content", "").lower():
                e["relevance"] = 0.5
                e["score"] = 0.5
                results.append(e)
        if biz_context is not None:
            allowed = set(biz_context.split(","))
            results = [r for r in results
                       if r.get("biz_context") is None
                       or allowed & set((r.get("biz_context") or "").split(","))]
        return results[:limit]

    def search_semantic(self, query: str, limit: int = 20, *, biz_context: str | None = None) -> list[dict]:
        return self.search(query, limit=limit, biz_context=biz_context)

    def search_hybrid(self, keyword: str, limit: int = 20, *, biz_context: str | None = None) -> list[dict]:
        return self.search(keyword, limit=limit, biz_context=biz_context)

    def add_entry(self, **kwargs) -> dict:
        eid = kwargs.get("id", str(len(self._entries) + 1))
        self._entries[eid] = dict(kwargs)
        return self._entries[eid]

    def list_entries(self, domain=None, category=None, status="active",
                     limit=50, offset=0) -> list[dict]:
        results = list(self._entries.values())
        if domain:
            results = [e for e in results if e.get("domain") == domain]
        if category:
            results = [e for e in results if e.get("category") == category]
        return results[offset:offset + limit]

    def get_entry(self, entry_id: str) -> dict | None:
        return self._entries.get(entry_id)


class ChromaDBBackend:
    """ChromaDB embedding + SQLite FTS5 hybrid backend."""

    def __init__(self, knowledge_manager):
        self._km = knowledge_manager

    def search(self, keyword: str, limit: int = 20, *, biz_context: str | None = None) -> list[dict]:
        return self._km._search_fts(keyword, limit=limit, biz_context=biz_context)

    def search_semantic(self, query: str, limit: int = 20, *, biz_context: str | None = None) -> list[dict]:
        return self._km._search_semantic(query, limit=limit, biz_context=biz_context)

    def search_hybrid(self, keyword: str, limit: int = 20, *, biz_context: str | None = None) -> list[dict]:
        results = self.search_semantic(keyword, limit=limit * 2, biz_context=biz_context)
        if not results:
            results = self.search(keyword, limit=limit, biz_context=biz_context)
        return results[:limit]

    def add_entry(self, **kwargs) -> dict:
        return self._km._add_entry_internal(**kwargs)

    def list_entries(self, domain=None, category=None, status="active",
                     limit=50, offset=0, biz_context=None) -> list[dict]:
        return self._km._list_entries_internal(
            domain=domain, category=category, status=status,
            limit=limit, offset=offset, biz_context=biz_context)

    def get_entry(self, entry_id: str) -> dict | None:
        return self._km._get_entry_internal(entry_id)


BACKEND_REGISTRY = {
    "builtin": BuiltinBackend,
    "memory": MemoryBackend,
    "chromadb": ChromaDBBackend,
}


def resolve_backend(name: str, knowledge_manager):
    """Resolve a backend name to an instance. Falls back to builtin."""
    import sys as _sys
    cls = BACKEND_REGISTRY.get(name)
    if cls is None:
        import warnings
        warnings.warn(f"Unknown knowledge backend '{name}', falling back to builtin")
        cls = BuiltinBackend
    if cls is MemoryBackend:
        msg = ("WARNING: MemoryBackend is in-memory only. All data will be lost on process exit. "
               "Use 'builtin' (default) for production.")
        print(f"⚠️  {msg}", file=_sys.stderr)
        return cls()
    return cls(knowledge_manager)
