"""Codebase RAG — semantic search over project files via Ollama embeddings.

Indexes the user's project files into a local vector store. The model
can call `search_codebase(query)` to retrieve the top-K relevant chunks.
Storage layout (separate from conversation memory):

  ~/.config/pw-agent/codebase/<project_hash>/
    chunks.json   list of {path, start_line, end_line, content, hash}
    vectors.npy   embedding matrix
    meta.json     project_dir, last_indexed, file_count, embed_model

Files are chunked by line groups (default 50 lines per chunk with 10
lines overlap) so retrieval brings back useful context windows. Big
files get split across many chunks; small files become single chunks.

Re-indexing skips chunks whose content hash hasn't changed.
"""

import hashlib
import json
import os
import time
from typing import Optional

import numpy as np
import requests


DEFAULT_INDEX_DIR = os.path.expanduser("~/.config/pw-agent/codebase")
EMBED_MODEL = "nomic-embed-text"

# Chunking config
CHUNK_LINES = 50
CHUNK_OVERLAP = 10

# Retrieval config
TOP_K = 8
MIN_SIMILARITY = 0.25          # threshold for explicit search_codebase tool calls
MIN_SIMILARITY_AUTO = 0.55     # stricter threshold when auto-injecting into prompt
MAX_AUTO_INJECT_CHARS = 6000   # ~1500 tokens cap on auto-injected code context
AUTO_INJECT_TOP_K = 4          # fewer hits when auto-injecting (vs tool call)
STALE_HOURS = 24               # trigger incremental re-index after this long
BM25_WEIGHT = 0.3              # hybrid score = 0.7 * cosine + 0.3 * bm25

# Files to index by extension
INDEXABLE_EXTENSIONS = {
    ".py", ".pyi", ".pyx",
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".go", ".rs", ".java", ".kt", ".swift", ".m", ".c", ".cc", ".cpp", ".h", ".hpp",
    ".rb", ".php", ".cs", ".scala", ".clj", ".ex", ".exs",
    ".html", ".css", ".scss", ".sass", ".vue", ".svelte",
    ".sh", ".bash", ".zsh", ".fish",
    ".sql", ".graphql", ".proto",
    ".md", ".mdx", ".rst", ".txt",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ".dockerfile", ".tf", ".hcl",
}

# Directories to skip
IGNORED_DIRS = {
    "node_modules", ".git", ".venv", "venv", "env", "__pycache__",
    ".next", ".nuxt", "dist", "build", "out", "target", ".cache",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox",
    "coverage", "htmlcov", ".idea", ".vscode", ".DS_Store",
    "vendor", "bower_components", ".terraform", ".gradle",
    ".planning", ".worktrees", ".auto-claude",
}

# Cap on file size to index (200KB) — larger files are usually generated
MAX_FILE_BYTES = 200_000


class CodebaseIndex:
    """Vector index of project source files with chunked semantic search.

    Embeddings can come from two backends:
      - direct: hits a local Ollama at ollama_url (default localhost:11434)
      - cloud:  proxies through the PastaWater broker which routes to the
                user's active fleet brain. This lets cloud-mode pw-agents
                use /index without needing a local Ollama install.

    Pass an LLMClient via `client=` to enable the cloud path. The class
    auto-detects which path to use based on client.direct_mode.
    """

    def __init__(self, project_dir: str, ollama_url: str = "http://localhost:11434",
                 index_dir: str = "", client=None):
        self.project_dir = os.path.abspath(project_dir)
        self.ollama_url = ollama_url
        self.index_dir = index_dir or DEFAULT_INDEX_DIR
        self.client = client  # Optional LLMClient for cloud-mode embed proxy

        project_hash = hashlib.md5(self.project_dir.encode()).hexdigest()[:12]
        self.store_path = os.path.join(self.index_dir, project_hash)
        os.makedirs(self.store_path, exist_ok=True)

        self.chunks: list[dict] = []
        self.vectors: Optional[np.ndarray] = None
        self._embed_model: Optional[str] = None
        self._load()

    @property
    def size(self) -> int:
        return len(self.chunks)

    @property
    def is_indexed(self) -> bool:
        return self.size > 0 and self.vectors is not None

    def _chunks_path(self) -> str:
        return os.path.join(self.store_path, "chunks.json")

    def _vectors_path(self) -> str:
        return os.path.join(self.store_path, "vectors.npy")

    def _meta_path(self) -> str:
        return os.path.join(self.store_path, "meta.json")

    def _load(self):
        if os.path.exists(self._chunks_path()):
            try:
                with open(self._chunks_path(), "r") as f:
                    self.chunks = json.load(f)
            except Exception:
                self.chunks = []

        if os.path.exists(self._vectors_path()):
            try:
                self.vectors = np.load(self._vectors_path())
            except Exception:
                self.vectors = None

        if os.path.exists(self._meta_path()):
            try:
                with open(self._meta_path(), "r") as f:
                    meta = json.load(f)
                self._embed_model = meta.get("embed_model")
            except Exception:
                pass

    def _save(self):
        with open(self._chunks_path(), "w") as f:
            json.dump(self.chunks, f)
        if self.vectors is not None and len(self.vectors) > 0:
            np.save(self._vectors_path(), self.vectors)
        with open(self._meta_path(), "w") as f:
            json.dump({
                "project_dir": self.project_dir,
                "last_indexed": time.time(),
                "chunk_count": len(self.chunks),
                "embed_model": self._embed_model,
            }, f, indent=2)

    def _use_cloud_embed(self) -> bool:
        """True when we should route embeddings through the broker rather
        than hitting a local Ollama."""
        return bool(self.client) and not getattr(self.client, "direct_mode", False) and bool(getattr(self.client, "token", ""))

    def _embed_batch(self, texts: list[str]) -> Optional[np.ndarray]:
        """Embed a batch of texts. Returns (N, dim) or None on failure.

        Routes to broker /api/v1/agents/embed in cloud mode, falls back to
        local Ollama in direct mode.
        """
        if not texts:
            return None
        model = self._embed_model or EMBED_MODEL

        # Cloud mode: proxy through broker → fleet brain Ollama
        if self._use_cloud_embed():
            try:
                resp = self.client.session.post(
                    f"{self.client.api_url}/api/v1/agents/embed",
                    json={"model": model, "input": texts},
                    timeout=180,
                )
                if resp.status_code == 200:
                    data = resp.json() or {}
                    if data.get("success"):
                        embeddings = data.get("embeddings", [])
                        if embeddings:
                            self._embed_model = data.get("model", model)
                            return np.array(embeddings, dtype=np.float32)
                    # Surface broker errors so the caller can show them
                    err = data.get("error", "")
                    if err:
                        # Stash for caller diagnostics
                        self._last_embed_error = f"broker: {err}"
                        return None
                else:
                    self._last_embed_error = f"broker HTTP {resp.status_code}: {resp.text[:200]}"
                    return None
            except Exception as e:
                self._last_embed_error = f"broker request failed: {e}"
                return None

        # Direct/local mode: hit the brain's /api/embed proxy.
        # If client has a token, send it — brain requires bearer auth.
        headers = {}
        token = getattr(self.client, "token", "") if self.client else ""
        if token:
            headers["Authorization"] = f"Bearer {token}"
        try:
            resp = requests.post(
                f"{self.ollama_url}/api/embed",
                json={"model": model, "input": texts, "options": {"num_gpu": 0}},
                headers=headers,
                timeout=120,
            )
            if resp.status_code == 200:
                data = resp.json()
                embeddings = data.get("embeddings", [])
                if embeddings:
                    self._embed_model = model
                    return np.array(embeddings, dtype=np.float32)
            else:
                self._last_embed_error = f"local Ollama/brain HTTP {resp.status_code}"
        except Exception as e:
            self._last_embed_error = f"local Ollama failed: {e}"
        return None

    def index(self, force: bool = False, max_files: int = 5000) -> dict:
        """Walk the project, chunk files, embed new chunks. Skips unchanged content.

        Returns stats: {files_scanned, files_indexed, chunks_added, chunks_skipped, errors}
        """
        stats = {"files_scanned": 0, "files_indexed": 0, "chunks_added": 0,
                 "chunks_skipped": 0, "errors": 0}

        # Build set of existing chunk hashes for dedup
        existing_hashes = {c.get("hash"): i for i, c in enumerate(self.chunks)}

        # Walk filesystem
        new_chunks = []
        for chunk in self._walk_and_chunk(max_files=max_files):
            stats["files_scanned"] = chunk.get("_files_scanned", stats["files_scanned"])
            if chunk.get("_marker"):
                continue
            chunk_hash = chunk["hash"]
            if not force and chunk_hash in existing_hashes:
                stats["chunks_skipped"] += 1
                continue
            new_chunks.append(chunk)
            stats["chunks_added"] += 1

        if not new_chunks:
            return stats

        stats["files_indexed"] = len({c["path"] for c in new_chunks})

        # Embed in larger batches when going through the broker (one big
        # round-trip is way cheaper than many small ones across the WAN).
        # Local Ollama is fast either way, but bigger batches mean fewer
        # context switches.
        BATCH = 64
        all_vectors = []
        for i in range(0, len(new_chunks), BATCH):
            batch = new_chunks[i:i + BATCH]
            texts = [c["content"] for c in batch]
            vecs = self._embed_batch(texts)
            if vecs is None:
                stats["errors"] += len(batch)
                # Surface the most recent error for the caller
                if hasattr(self, "_last_embed_error"):
                    stats["last_error"] = self._last_embed_error
                continue
            all_vectors.append(vecs)

        if not all_vectors:
            return stats

        new_vec_matrix = np.vstack(all_vectors)

        # Append to existing
        if self.vectors is None or len(self.vectors) == 0:
            self.vectors = new_vec_matrix
            self.chunks = new_chunks
        else:
            # If embed dim changed (model swap), reset
            if self.vectors.shape[1] != new_vec_matrix.shape[1]:
                self.vectors = new_vec_matrix
                self.chunks = new_chunks
            else:
                self.vectors = np.vstack([self.vectors, new_vec_matrix])
                self.chunks = self.chunks + new_chunks

        self._save()
        # Build/refresh the BM25 sidecar for hybrid retrieval
        self.build_bm25()
        return stats

    def _walk_and_chunk(self, max_files: int = 5000, only_paths: Optional[set] = None):
        """Generator yielding chunks dicts. Uses language-aware chunking where
        possible (chunking.chunk_file) and falls back to line-window for files
        that parser doesn't recognize.

        only_paths: if provided, only files whose rel_path is in the set are
        yielded — used for incremental re-indexing."""
        try:
            from chunking import chunk_file
        except Exception:
            chunk_file = None  # module not available; falls back inline below

        files_scanned = 0
        for root, dirs, files in os.walk(self.project_dir):
            # Prune ignored dirs in-place so os.walk doesn't recurse
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".")]

            for fname in files:
                if files_scanned >= max_files:
                    return
                path = os.path.join(root, fname)
                ext = os.path.splitext(fname)[1].lower()
                if ext not in INDEXABLE_EXTENSIONS:
                    continue
                rel_path = os.path.relpath(path, self.project_dir)
                if only_paths is not None and rel_path not in only_paths:
                    continue
                try:
                    if os.path.getsize(path) > MAX_FILE_BYTES:
                        continue
                    with open(path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                except Exception:
                    continue

                files_scanned += 1
                yield {"_marker": True, "_files_scanned": files_scanned}

                if chunk_file is not None:
                    try:
                        for c in chunk_file(rel_path, content):
                            yield c
                        continue
                    except Exception:
                        pass  # fall through to legacy path

                # Legacy fallback: fixed line windows
                lines = content.split("\n")
                if not lines:
                    continue
                step = CHUNK_LINES - CHUNK_OVERLAP
                for start in range(0, len(lines), step):
                    end = min(len(lines), start + CHUNK_LINES)
                    chunk_text = "\n".join(lines[start:end]).strip()
                    if not chunk_text or len(chunk_text) < 30:
                        continue
                    embed_text = f"# {rel_path} (lines {start+1}-{end})\n{chunk_text}"
                    yield {
                        "path": rel_path,
                        "start_line": start + 1,
                        "end_line": end,
                        "content": embed_text,
                        "hash": hashlib.md5(embed_text.encode()).hexdigest()[:16],
                    }
                    if end >= len(lines):
                        break

    def search(self, query: str, top_k: int = TOP_K) -> list[tuple[dict, float]]:
        """Semantic search over indexed chunks. Returns top-K (chunk, score)."""
        if not self.is_indexed:
            return []

        query_vec = self._embed_batch([query])
        if query_vec is None:
            return []

        # Cosine similarity
        q = query_vec / (np.linalg.norm(query_vec, axis=1, keepdims=True) + 1e-8)
        store = self.vectors / (np.linalg.norm(self.vectors, axis=1, keepdims=True) + 1e-8)
        sims = (store @ q.T).flatten()

        indices = np.argsort(sims)[::-1][:top_k]
        results = []
        for idx in indices:
            score = float(sims[idx])
            if score >= MIN_SIMILARITY:
                results.append((self.chunks[idx], score))
        return results

    def format_results(self, query: str, results: list[tuple[dict, float]] = None) -> str:
        """Format search results as readable text for the model."""
        if results is None:
            results = self.search(query)
        if not results:
            return f"No matches in indexed codebase for: {query}"
        lines = [f"Codebase search results for: {query}", ""]
        for chunk, score in results:
            path = chunk.get("path", "?")
            start = chunk.get("start_line", "?")
            end = chunk.get("end_line", "?")
            lines.append(f"━━━ {path}:{start}-{end}  (relevance {score:.2f})")
            content = chunk.get("content", "")
            # Strip the path-prefix line we added before embedding
            content_lines = content.split("\n", 1)
            if content_lines and content_lines[0].startswith("# ") and len(content_lines) > 1:
                content = content_lines[1]
            # Truncate very long chunks
            if len(content) > 1500:
                content = content[:1500] + "..."
            lines.append(content)
            lines.append("")
        return "\n".join(lines).rstrip()

    def clear(self):
        """Wipe the index."""
        self.chunks = []
        self.vectors = None
        for p in [self._chunks_path(), self._vectors_path(), self._meta_path()]:
            if os.path.exists(p):
                os.remove(p)
        # Also clear BM25 sidecar if present
        bm25_path = os.path.join(self.store_path, "bm25.json")
        if os.path.exists(bm25_path):
            try:
                os.remove(bm25_path)
            except OSError:
                pass

    # ═══════════ Auto-index / staleness / incremental ════════════════════

    def _project_file_mtime_map(self) -> dict:
        """Return {rel_path: mtime} for every indexable file in the project."""
        out = {}
        for root, dirs, files in os.walk(self.project_dir):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".")]
            for fname in files:
                ext = os.path.splitext(fname)[1].lower()
                if ext not in INDEXABLE_EXTENSIONS:
                    continue
                path = os.path.join(root, fname)
                try:
                    if os.path.getsize(path) > MAX_FILE_BYTES:
                        continue
                    out[os.path.relpath(path, self.project_dir)] = os.path.getmtime(path)
                except OSError:
                    continue
        return out

    def _read_meta(self) -> dict:
        if not os.path.exists(self._meta_path()):
            return {}
        try:
            with open(self._meta_path(), "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def stale_files(self) -> list:
        """Return the list of rel_paths that have changed since last index.
        Empty list means the index is up-to-date."""
        meta = self._read_meta()
        last = meta.get("last_indexed", 0)
        if not last:
            # Index was never built — everything is "stale"
            return list(self._project_file_mtime_map().keys())
        stale = []
        for rel_path, mtime in self._project_file_mtime_map().items():
            if mtime > last:
                stale.append(rel_path)
        # Also flag files that appear in the index but no longer exist on disk
        indexed_paths = {c.get("path") for c in self.chunks}
        on_disk_paths = set(self._project_file_mtime_map().keys())
        # Don't return deletions here — incremental_reindex handles those separately
        return stale

    def is_stale(self, max_age_hours: float = STALE_HOURS) -> bool:
        """Quick check: True if the index hasn't been refreshed recently
        or if files have clearly changed since the last index."""
        meta = self._read_meta()
        last = meta.get("last_indexed", 0)
        if not last:
            return True
        age_hours = (time.time() - last) / 3600
        if age_hours > max_age_hours:
            return True
        # Fast check: count of current files vs file_count at index time
        if meta.get("chunk_count", 0) != len(self.chunks):
            return True
        return bool(self.stale_files())

    def incremental_reindex(self, max_files: int = 5000) -> dict:
        """Re-embed only files that changed since last index. Also drops
        chunks whose file no longer exists."""
        stats = {"files_rebuilt": 0, "chunks_added": 0, "chunks_removed": 0, "errors": 0}
        changed = set(self.stale_files())

        # Remove chunks for files that are gone OR have changed (they'll be re-added)
        on_disk = set(self._project_file_mtime_map().keys())
        if self.chunks:
            keep_idx = []
            for i, c in enumerate(self.chunks):
                p = c.get("path")
                if p not in on_disk:
                    stats["chunks_removed"] += 1
                    continue
                if p in changed:
                    stats["chunks_removed"] += 1
                    continue
                keep_idx.append(i)
            if len(keep_idx) != len(self.chunks):
                self.chunks = [self.chunks[i] for i in keep_idx]
                if self.vectors is not None and len(self.vectors) > 0:
                    self.vectors = self.vectors[keep_idx]

        if not changed:
            # Nothing to rebuild — just persist the cleanup if any
            if stats["chunks_removed"]:
                self._save()
            return stats

        # Re-walk only the changed files and embed
        new_chunks = []
        for chunk in self._walk_and_chunk(max_files=max_files, only_paths=changed):
            if chunk.get("_marker"):
                continue
            new_chunks.append(chunk)

        if not new_chunks:
            self._save()
            return stats

        stats["files_rebuilt"] = len({c["path"] for c in new_chunks})
        BATCH = 64
        all_vectors = []
        for i in range(0, len(new_chunks), BATCH):
            batch = new_chunks[i:i + BATCH]
            vecs = self._embed_batch([c["content"] for c in batch])
            if vecs is None:
                stats["errors"] += len(batch)
                continue
            all_vectors.append(vecs)

        if all_vectors:
            new_mat = np.vstack(all_vectors)
            stats["chunks_added"] = len(new_mat)
            if self.vectors is None or len(self.vectors) == 0:
                self.vectors = new_mat
                self.chunks = new_chunks
            elif self.vectors.shape[1] != new_mat.shape[1]:
                # Embed dim changed — wipe and start over
                self.vectors = new_mat
                self.chunks = new_chunks
            else:
                self.vectors = np.vstack([self.vectors, new_mat])
                self.chunks = self.chunks + new_chunks

        self._save()
        # Rebuild BM25 sidecar so it reflects the current chunk set
        self.build_bm25()
        return stats

    def ensure_indexed(self, max_files: int = 5000) -> dict:
        """Guarantee the index is ready for retrieval.

        - If empty: do a full index.
        - If stale: do an incremental re-index.
        - Otherwise: no-op.

        Returns stats dict (or {'skipped': True} if nothing to do)."""
        if not self.is_indexed:
            return self.index(max_files=max_files)
        if self.is_stale():
            return self.incremental_reindex(max_files=max_files)
        return {"skipped": True}

    # ═══════════ Hybrid retrieval + auto-inject context ════════════════════

    def _load_bm25(self):
        """Lazily load the BM25 sidecar. Returns a BM25Index or None."""
        if getattr(self, "_bm25", None) is not None:
            return self._bm25
        try:
            from bm25_index import BM25Index
            self._bm25 = BM25Index(self.store_path)
            return self._bm25
        except Exception:
            self._bm25 = None
            return None

    def build_bm25(self) -> None:
        """Build the BM25 sidecar from current chunks. Call after indexing."""
        bm = self._load_bm25()
        if bm is None or not self.chunks:
            return
        try:
            bm.build(self.chunks)
        except Exception:
            pass

    def search_hybrid(self, query: str, top_k: int = TOP_K,
                      min_similarity: float = MIN_SIMILARITY) -> list:
        """Hybrid cosine + BM25 retrieval. Falls back to pure cosine if BM25
        sidecar isn't built. Returns [(chunk, blended_score)]."""
        cosine_hits = self.search(query, top_k=top_k * 2)  # overfetch
        if not cosine_hits:
            return []
        cosine_by_idx = {id(c): (c, s) for c, s in cosine_hits}

        bm = self._load_bm25()
        if bm is None or bm.size == 0:
            # No BM25 available — filter+return cosine hits
            return [(c, s) for c, s in cosine_hits if s >= min_similarity][:top_k]

        # Map chunks → their index in self.chunks so we can look up BM25 hits
        chunk_to_idx = {id(c): i for i, c in enumerate(self.chunks)}

        try:
            bm25_hits = bm.search(query, top_k=top_k * 2)
        except Exception:
            bm25_hits = []
        bm25_by_idx = {idx: score for idx, score in bm25_hits}

        # Build blended scores for every chunk that appears in either list
        blended = {}
        for chunk, cos_score in cosine_hits:
            idx = chunk_to_idx.get(id(chunk), -1)
            bm_score = bm25_by_idx.get(idx, 0.0)
            blended[idx] = (chunk, (1 - BM25_WEIGHT) * cos_score + BM25_WEIGHT * bm_score)
        for idx, bm_score in bm25_hits:
            if idx in blended or idx >= len(self.chunks):
                continue
            # BM25-only hit (not in cosine top list); give it a low cosine floor
            blended[idx] = (self.chunks[idx], BM25_WEIGHT * bm_score)

        # Sort + filter + trim
        ordered = sorted(blended.values(), key=lambda x: x[1], reverse=True)
        return [(c, s) for c, s in ordered if s >= min_similarity][:top_k]

    def format_context(self, query: str, max_chars: int = MAX_AUTO_INJECT_CHARS,
                       top_k: int = AUTO_INJECT_TOP_K,
                       min_similarity: float = MIN_SIMILARITY_AUTO) -> tuple[str, list]:
        """Retrieve + format the top chunks for auto-injection into the system
        prompt. Stricter threshold than search_codebase tool calls; bounded by
        a char cap so it never blows the context budget.

        Returns a (context_str, raw_hits) tuple so the caller can derive stats
        from ``raw_hits`` without issuing a second embed round-trip.
        ``raw_hits`` is the list[tuple[chunk_dict, float]] from search_hybrid.
        """
        if not self.is_indexed:
            return "", []
        hits = self.search_hybrid(query, top_k=top_k, min_similarity=min_similarity)
        if not hits:
            return "", hits
        lines = ["## Relevant code (auto-retrieved):"]
        total = len(lines[0])
        for chunk, score in hits:
            path = chunk.get("path", "?")
            start = chunk.get("start_line", "?")
            end = chunk.get("end_line", "?")
            content = chunk.get("content", "")
            # Strip the embedded path-prefix we added at index time
            parts = content.split("\n", 1)
            if parts and parts[0].startswith("# ") and len(parts) > 1:
                content = parts[1]
            header = f"### {path}:{start}-{end} (relevance {score:.2f})"
            entry = header + "\n" + content
            if total + len(entry) > max_chars:
                break
            lines.append(entry)
            total += len(entry)
        return "\n\n".join(lines), hits
