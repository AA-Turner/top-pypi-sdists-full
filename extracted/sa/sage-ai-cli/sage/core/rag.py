"""Local RAG over the user's codebase."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import struct
import time
from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "Chunk",
    "Embedder",
    "OllamaEmbedder",
    "RAGIndex",
    "format_chunks_for_prompt",
    "_walk_indexable",
    "_chunk_file",
    "_vec_to_blob",
    "_blob_to_vec",
    "_cosine",
]


_SKIP_DIRS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv", "env",
    "dist", "build", "target", ".next", ".nuxt", ".cache",
    "coverage", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "vendor", "third_party",
}
_SKIP_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico",
    ".mp4", ".mov", ".avi", ".webm", ".mp3", ".wav",
    ".pdf", ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".pyc", ".pyo", ".so", ".dylib", ".dll", ".o", ".a",
    ".gguf", ".bin", ".safetensors", ".pt", ".pth",
    ".lock",
}
_INDEX_EXTS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte",
    ".rs", ".go", ".java", ".kt", ".swift", ".rb", ".php",
    ".c", ".cc", ".cpp", ".h", ".hpp", ".cs", ".scala",
    ".ex", ".exs", ".erl", ".hs", ".ml", ".clj", ".cljs",
    ".sh", ".bash", ".zsh", ".fish",
    ".sql", ".graphql", ".proto",
    ".md", ".rst", ".txt",
    ".json", ".yaml", ".yml", ".toml",
    ".html", ".css", ".scss",
}
_MAX_FILE_BYTES = 256 * 1024
_CHUNK_LINES = 80
_CHUNK_OVERLAP = 12


@dataclass
class Chunk:
    file_path: str
    start_line: int
    end_line: int
    text: str
    score: float = 0.0


class Embedder:
    dim: int = 768
    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError


class OllamaEmbedder(Embedder):
    def __init__(self, model: str = "nomic-embed-text", host: str = "http://127.0.0.1:11434"):
        self.model = model
        self.host = host
        self.dim = 768

    def embed(self, texts: list[str]) -> list[list[float]]:
        try:
            import httpx
        except ImportError as exc:
            raise RuntimeError("httpx required for OllamaEmbedder") from exc

        out: list[list[float]] = []
        with httpx.Client(timeout=60.0) as client:
            for text in texts:
                if not text.strip():
                    out.append([0.0] * self.dim)
                    continue
                resp = client.post(
                    f"{self.host}/api/embeddings",
                    json={"model": self.model, "prompt": text[:8000]},
                )
                resp.raise_for_status()
                vec = resp.json().get("embedding") or []
                if vec and len(vec) != self.dim:
                    self.dim = len(vec)
                out.append(vec)
        return out


def _project_hash(cwd: Path) -> str:
    return hashlib.sha1(str(cwd.resolve()).encode("utf-8")).hexdigest()[:12]


def _walk_indexable(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS and not d.startswith(".")]
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext in _SKIP_EXTS:
                continue
            if _INDEX_EXTS and ext not in _INDEX_EXTS:
                continue
            p = Path(dirpath) / name
            try:
                if p.stat().st_size > _MAX_FILE_BYTES:
                    continue
            except OSError:
                continue
            yield p


def _chunk_file(path: Path, root: Path) -> list[Chunk]:
    try:
        text = path.read_text("utf-8", errors="replace")
    except OSError:
        return []
    lines = text.splitlines()
    if not lines:
        return []
    rel = str(path.relative_to(root))
    chunks: list[Chunk] = []
    i = 0
    while i < len(lines):
        end = min(i + _CHUNK_LINES, len(lines))
        chunk_text = "\n".join(lines[i:end])
        chunks.append(Chunk(
            file_path=rel,
            start_line=i + 1,
            end_line=end,
            text=chunk_text,
        ))
        if end == len(lines):
            break
        i = end - _CHUNK_OVERLAP
    return chunks


def _try_load_sqlite_vec(conn: sqlite3.Connection) -> bool:
    try:
        conn.enable_load_extension(True)
        import sqlite_vec  # type: ignore
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
        return True
    except Exception:
        return False


def _cosine(a: list[float], b: list[float]) -> float:
    import math
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def _vec_to_blob(vec: list[float]) -> bytes:
    return struct.pack(f"<{len(vec)}f", *vec)


def _blob_to_vec(blob: bytes) -> list[float]:
    n = len(blob) // 4
    return list(struct.unpack(f"<{n}f", blob))


class RAGIndex:
    def __init__(self, cwd: Path, embedder: Embedder | None = None):
        self.cwd = cwd.resolve()
        self.embedder = embedder or OllamaEmbedder()
        self.db_dir = Path.home() / ".sage" / "rag"
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.db_dir / f"{_project_hash(self.cwd)}.db"
        self._conn = sqlite3.connect(self.db_path)
        self._has_vec = _try_load_sqlite_vec(self._conn)
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self._conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS files (
                path TEXT PRIMARY KEY,
                mtime REAL NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT NOT NULL,
                start_line INTEGER NOT NULL,
                end_line INTEGER NOT NULL,
                text TEXT NOT NULL,
                embedding BLOB
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_chunks_path ON chunks(path)")
        if self._has_vec:
            try:
                cur.execute(f"""
                    CREATE VIRTUAL TABLE IF NOT EXISTS chunk_vec USING vec0(
                        chunk_id INTEGER PRIMARY KEY,
                        embedding float[{self.embedder.dim}]
                    )
                """)
            except Exception:
                self._has_vec = False
        self._conn.commit()

    def reindex(self, *, force: bool = False, progress=None) -> dict:
        cur = self._conn.cursor()

        existing_mtimes: dict[str, float] = {}
        if not force:
            for row in cur.execute("SELECT path, mtime FROM files"):
                existing_mtimes[row[0]] = row[1]

        new_chunks: list[Chunk] = []
        files_seen: set[str] = set()
        for path in _walk_indexable(self.cwd):
            rel = str(path.relative_to(self.cwd))
            files_seen.add(rel)
            try:
                mtime = path.stat().st_mtime
            except OSError:
                continue
            if not force and existing_mtimes.get(rel) == mtime:
                continue
            cur.execute("DELETE FROM chunks WHERE path = ?", (rel,))
            for c in _chunk_file(path, self.cwd):
                new_chunks.append(c)
            cur.execute(
                "INSERT OR REPLACE INTO files(path, mtime) VALUES (?, ?)",
                (rel, mtime),
            )

        if not force:
            for stale in set(existing_mtimes) - files_seen:
                cur.execute("DELETE FROM chunks WHERE path = ?", (stale,))
                cur.execute("DELETE FROM files WHERE path = ?", (stale,))

        embedded = 0
        if new_chunks:
            BATCH = 32
            for i in range(0, len(new_chunks), BATCH):
                batch = new_chunks[i : i + BATCH]
                vecs = self.embedder.embed([c.text for c in batch])
                for c, vec in zip(batch, vecs):
                    cur.execute(
                        "INSERT INTO chunks(path, start_line, end_line, text, embedding) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (c.file_path, c.start_line, c.end_line, c.text, _vec_to_blob(vec)),
                    )
                    last_id = cur.lastrowid
                    if self._has_vec and last_id is not None:
                        try:
                            cur.execute(
                                "INSERT INTO chunk_vec(chunk_id, embedding) VALUES (?, ?)",
                                (last_id, _vec_to_blob(vec)),
                            )
                        except Exception:
                            self._has_vec = False
                    embedded += 1
                if progress is not None:
                    progress(embedded, len(new_chunks))
        self._conn.commit()
        return {
            "files_seen": len(files_seen),
            "chunks_added": embedded,
            "vec_backend": "sqlite-vec" if self._has_vec else "cosine-fallback",
        }

    def query(self, text: str, top_k: int = 6) -> list[Chunk]:
        if not text.strip():
            return []
        try:
            qvec = self.embedder.embed([text])[0]
        except Exception:
            return []
        cur = self._conn.cursor()

        if self._has_vec:
            try:
                rows = cur.execute(
                    "SELECT c.path, c.start_line, c.end_line, c.text, "
                    "       (1 - vec_distance_cosine(v.embedding, ?)) AS score "
                    "FROM chunk_vec v JOIN chunks c ON c.id = v.chunk_id "
                    "ORDER BY vec_distance_cosine(v.embedding, ?) ASC LIMIT ?",
                    (_vec_to_blob(qvec), _vec_to_blob(qvec), top_k),
                ).fetchall()
                return [Chunk(r[0], r[1], r[2], r[3], r[4]) for r in rows]
            except Exception:
                self._has_vec = False

        scored: list[Chunk] = []
        for row in cur.execute(
            "SELECT path, start_line, end_line, text, embedding FROM chunks"
        ):
            vec = _blob_to_vec(row[4])
            score = _cosine(qvec, vec)
            scored.append(Chunk(row[0], row[1], row[2], row[3], score))
        scored.sort(key=lambda c: c.score, reverse=True)
        return scored[:top_k]


def format_chunks_for_prompt(chunks: list[Chunk], max_chars: int = 6000) -> str:
    if not chunks:
        return ""
    parts: list[str] = ["", "## RETRIEVED CONTEXT (top results from this project)"]
    used = 0
    for c in chunks:
        block = f"\n— {c.file_path}:{c.start_line}-{c.end_line} (score={c.score:.3f})\n```\n{c.text}\n```\n"
        if used + len(block) > max_chars:
            break
        parts.append(block)
        used += len(block)
    parts.append(
        "\n→ This is the project's actual code. Reference real symbols/paths "
        "from above; do NOT invent file paths or import names."
    )
    return "\n".join(parts)
