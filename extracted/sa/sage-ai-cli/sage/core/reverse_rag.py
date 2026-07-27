"""Item #25 — Reverse-RAG (rank files by relevance to a query)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

__all__ = ["RelevantFile", "find_relevant_files"]


@dataclass
class RelevantFile:
    file_path: str
    score: float
    snippet: str = ""


def find_relevant_files(query: str, project_root: Path, *,
                         top_k: int = 10) -> list[RelevantFile]:
    """Return files most relevant to the query, ranked by aggregate
    chunk score from the project's RAG index."""
    try:
        from sage.core.rag import RAGIndex
    except Exception:
        return []
    try:
        idx = RAGIndex(project_root)
        chunks = idx.query(query, top_k=top_k * 3)
    except Exception:
        return []

    # Aggregate scores by file
    by_file: dict[str, float] = {}
    snippets: dict[str, str] = {}
    for c in chunks:
        prev = by_file.get(c.file_path, 0.0)
        by_file[c.file_path] = prev + c.score
        if c.file_path not in snippets:
            snippets[c.file_path] = c.text[:200]

    sorted_files = sorted(by_file.items(), key=lambda t: t[1], reverse=True)
    return [
        RelevantFile(file_path=fp, score=s, snippet=snippets[fp])
        for fp, s in sorted_files[:top_k]
    ]
