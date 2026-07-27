"""T8 — Run RAG indexing BEFORE the first turn, not on demand.

The Novellia run had no project context because RAG was never built. This
helper checks whether the per-project index exists + is fresh, builds it
if needed, and is cheap to call at the top of every `sage run` boot.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass
from pathlib import Path

__all__ = ["RagPreturnResult", "ensure_rag_indexed"]


@dataclass
class RagPreturnResult:
    indexed: bool       # True iff we ran reindex this call
    skipped: bool       # True iff we left an existing index alone
    reason: str = ""
    files_seen: int = 0
    chunks_added: int = 0


def _project_db_path(cwd: Path) -> Path:
    h = hashlib.sha1(str(cwd.resolve()).encode("utf-8")).hexdigest()[:12]
    return Path.home() / ".sage" / "rag" / f"{h}.db"


def ensure_rag_indexed(cwd: Path, *, max_age_seconds: int = 3600) -> RagPreturnResult:
    """Build/refresh the RAG index for `cwd`.

    Skip when the per-project DB exists and is younger than max_age_seconds.
    """
    db = _project_db_path(cwd)
    if db.exists():
        try:
            age = time.time() - db.stat().st_mtime
        except OSError:
            age = 0.0
        if age < max_age_seconds:
            return RagPreturnResult(indexed=False, skipped=True,
                                    reason=f"index exists, age {age:.0f}s < {max_age_seconds}s")

    try:
        from sage.core.rag import RAGIndex
    except Exception as exc:
        return RagPreturnResult(indexed=False, skipped=False,
                                reason=f"import failed: {exc}")
    try:
        idx = RAGIndex(cwd)
        stats = idx.reindex()
        return RagPreturnResult(
            indexed=True, skipped=False,
            files_seen=stats.get("files_seen", 0),
            chunks_added=stats.get("chunks_added", 0),
        )
    except Exception as exc:
        return RagPreturnResult(indexed=False, skipped=False,
                                reason=f"reindex failed: {exc}")
