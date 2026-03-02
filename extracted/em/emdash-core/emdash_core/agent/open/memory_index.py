"""MemoryIndex — SQLite FTS5 search index over memory markdown files.

Provides full-text search over:
- ``MEMORY.md``
- ``memory/*.md`` (daily logs)

Files are chunked into ~400-token blocks with ~80-token overlap.
The index is kept in sync via dirty-file tracking and explicit sync calls.
"""

import logging
import os
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Approximate tokens per character (same ratio used elsewhere in codebase)
_CHARS_PER_TOKEN = 4


@dataclass
class SearchHit:
    """A single search result from the memory index."""

    path: str
    start_line: int
    end_line: int
    snippet: str
    score: float


class MemoryIndex:
    """Full-text search index over memory markdown files using SQLite FTS5.

    Usage::

        index = MemoryIndex(db_path, workspace_dir)
        index.sync_now("boot")            # index all files on startup
        index.mark_dirty("memory/2026-02-18.md")  # after a write
        hits = index.search("user preferences")
    """

    # Chunking parameters (in tokens)
    CHUNK_TOKENS = 400
    OVERLAP_TOKENS = 80
    MAX_SNIPPET_CHARS = 700

    def __init__(
        self,
        db_path: Path,
        workspace_dir: Path,
        chunk_tokens: int = 0,
        overlap_tokens: int = 0,
    ) -> None:
        self._db_path = Path(db_path)
        self._workspace = Path(workspace_dir).resolve()
        self._chunk_tokens = chunk_tokens or self.CHUNK_TOKENS
        self._overlap_tokens = overlap_tokens or self.OVERLAP_TOKENS
        self._dirty_paths: set[str] = set()
        self._conn: Optional[sqlite3.Connection] = None

        # Track file mtimes for change detection
        self._known_mtimes: dict[str, float] = {}

        self._ensure_db()

    # ------------------------------------------------------------------
    # Database setup
    # ------------------------------------------------------------------

    def _ensure_db(self) -> None:
        """Create the database and FTS5 table if they don't exist."""
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = self._get_conn()
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT NOT NULL,
                start_line INTEGER NOT NULL,
                end_line INTEGER NOT NULL,
                content TEXT NOT NULL,
                indexed_at REAL NOT NULL
            );

            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
                content,
                content='chunks',
                content_rowid='id',
                tokenize='porter unicode61'
            );

            -- Triggers to keep FTS in sync with content table
            CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
                INSERT INTO chunks_fts(rowid, content)
                VALUES (new.id, new.content);
            END;

            CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, content)
                VALUES ('delete', old.id, old.content);
            END;

            CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, content)
                VALUES ('delete', old.id, old.content);
                INSERT INTO chunks_fts(rowid, content)
                VALUES (new.id, new.content);
            END;

            CREATE INDEX IF NOT EXISTS idx_chunks_path ON chunks(path);
            """
        )
        conn.commit()

    def _get_conn(self) -> sqlite3.Connection:
        """Get or create the database connection."""
        if self._conn is None:
            self._conn = sqlite3.connect(str(self._db_path), timeout=5)
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA synchronous=NORMAL")
        return self._conn

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
        limit: int = 5,
        timeout_ms: int = 3000,
    ) -> list[SearchHit]:
        """Search the memory index for matching chunks.

        Automatically syncs dirty files before searching.

        Args:
            query: Search query string.
            limit: Maximum number of results.
            timeout_ms: Search timeout in milliseconds.

        Returns:
            List of :class:`SearchHit` sorted by relevance score.
        """
        # Sync if there are dirty files
        if self._dirty_paths:
            self.sync_now("onSearch")

        conn = self._get_conn()

        # Escape FTS5 special characters in query
        safe_query = self._sanitize_query(query)
        if not safe_query:
            return []

        try:
            cursor = conn.execute(
                """
                SELECT
                    c.path,
                    c.start_line,
                    c.end_line,
                    snippet(chunks_fts, 0, '', '', '...', 64) AS snip,
                    rank
                FROM chunks_fts
                JOIN chunks c ON c.id = chunks_fts.rowid
                WHERE chunks_fts MATCH ?
                ORDER BY rank
                LIMIT ?
                """,
                (safe_query, limit),
            )
            rows = cursor.fetchall()
        except sqlite3.OperationalError as exc:
            logger.warning("FTS search failed: %s", exc)
            return []

        hits: list[SearchHit] = []
        for path, start_line, end_line, snippet, rank in rows:
            # FTS5 rank is negative (lower = better match)
            score = -rank if rank else 0.0
            # Clamp snippet length
            if len(snippet) > self.MAX_SNIPPET_CHARS:
                snippet = snippet[: self.MAX_SNIPPET_CHARS] + "..."
            hits.append(
                SearchHit(
                    path=path,
                    start_line=start_line,
                    end_line=end_line,
                    snippet=snippet,
                    score=round(score, 4),
                )
            )

        return hits

    @staticmethod
    def _sanitize_query(query: str) -> str:
        """Sanitize a query string for FTS5 MATCH.

        Wraps each word in double quotes to treat them as literal terms,
        avoiding syntax errors from special characters.
        """
        words = query.split()
        if not words:
            return ""
        # Quote each word and join with implicit AND
        return " ".join(f'"{w}"' for w in words if w.strip())

    # ------------------------------------------------------------------
    # Sync / indexing
    # ------------------------------------------------------------------

    def mark_dirty(self, path: str) -> None:
        """Mark a file as needing re-indexing.

        Args:
            path: Relative path within workspace (e.g. ``"memory/2026-02-18.md"``).
        """
        self._dirty_paths.add(path)

    def sync_now(self, reason: str = "boot") -> None:
        """Re-index dirty files, or all files on boot.

        Args:
            reason: Why sync is happening — ``"boot"``, ``"dirty"``,
                ``"interval"``, ``"onSearch"``.
        """
        start = time.monotonic()

        if reason == "boot":
            # Full scan: index everything
            paths = self._discover_memory_files()
        else:
            # Incremental: only dirty files + any new/changed files
            paths = list(self._dirty_paths)
            # Also check for new or changed files
            for p in self._discover_memory_files():
                if p not in self._dirty_paths:
                    file_path = self._workspace / p
                    if file_path.exists():
                        mtime = file_path.stat().st_mtime
                        if self._known_mtimes.get(p, 0) < mtime:
                            paths.append(p)

        if not paths:
            return

        conn = self._get_conn()
        indexed_count = 0

        for rel_path in paths:
            abs_path = self._workspace / rel_path
            if not abs_path.exists():
                # File was deleted — remove from index
                conn.execute("DELETE FROM chunks WHERE path = ?", (rel_path,))
                self._known_mtimes.pop(rel_path, None)
                continue

            try:
                content = abs_path.read_text(encoding="utf-8")
            except OSError as exc:
                logger.warning("Could not read %s for indexing: %s", rel_path, exc)
                continue

            # Remove old chunks for this file
            conn.execute("DELETE FROM chunks WHERE path = ?", (rel_path,))

            # Chunk and insert
            chunks = self._chunk_text(content)
            now = time.time()
            for start_line, end_line, chunk_text in chunks:
                conn.execute(
                    "INSERT INTO chunks (path, start_line, end_line, content, indexed_at) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (rel_path, start_line, end_line, chunk_text, now),
                )

            self._known_mtimes[rel_path] = abs_path.stat().st_mtime
            indexed_count += 1

        conn.commit()
        self._dirty_paths.clear()

        elapsed = time.monotonic() - start
        logger.info(
            "MemoryIndex sync (%s): indexed %d files in %.2fs",
            reason,
            indexed_count,
            elapsed,
        )

    def _discover_memory_files(self) -> list[str]:
        """Discover all indexable memory files in the workspace.

        Returns:
            List of relative paths.
        """
        paths: list[str] = []

        # MEMORY.md
        if self._workspace.joinpath("MEMORY.md").exists():
            paths.append("MEMORY.md")

        # memory/*.md
        memory_dir = self._workspace / "memory"
        if memory_dir.exists():
            for f in memory_dir.iterdir():
                if f.is_file() and f.suffix == ".md":
                    paths.append(f"memory/{f.name}")

        return paths

    def _chunk_text(
        self,
        text: str,
    ) -> list[tuple[int, int, str]]:
        """Split text into overlapping chunks for indexing.

        Args:
            text: Full file content.

        Returns:
            List of ``(start_line, end_line, chunk_text)`` tuples.
        """
        lines = text.splitlines(keepends=True)
        if not lines:
            return []

        chunk_chars = self._chunk_tokens * _CHARS_PER_TOKEN
        overlap_chars = self._overlap_tokens * _CHARS_PER_TOKEN

        chunks: list[tuple[int, int, str]] = []
        i = 0  # current line index

        while i < len(lines):
            # Build a chunk up to chunk_chars
            chunk_lines: list[str] = []
            char_count = 0
            start_line = i

            while i < len(lines) and char_count < chunk_chars:
                chunk_lines.append(lines[i])
                char_count += len(lines[i])
                i += 1

            end_line = i - 1
            chunk_text = "".join(chunk_lines).strip()

            if chunk_text:
                chunks.append((start_line, end_line, chunk_text))

            # Step back by overlap
            if i < len(lines):
                overlap_chars_remaining = overlap_chars
                while i > start_line + 1 and overlap_chars_remaining > 0:
                    i -= 1
                    overlap_chars_remaining -= len(lines[i])

        return chunks

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the database connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None
