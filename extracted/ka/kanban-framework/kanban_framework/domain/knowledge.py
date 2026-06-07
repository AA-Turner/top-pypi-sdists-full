"""Knowledge management backed by SQLite (stdlib, zero deps).

Single .db file replaces entries/*.json, index.json, usage-log.json, domains.json.
FTS5 provides full-text search with BM25 ranking.
jieba (optional) provides Chinese tokenization for FTS5 search.
fastembed (optional, ONNX-based) provides semantic vector search.
"""
from __future__ import annotations
import json
import sqlite3
import time
from datetime import datetime, timezone, timedelta

# ── Re-exports from extracted modules for backward compatibility ──────────
from kanban_framework.domain.knowledge_lazy import (  # noqa: F401
    _get_jieba, _get_chromadb, _get_embed_model,
    _embed, _unpack_embedding, _cosine_similarity, _segment,
    DEFAULT_DOMAINS, VALID_CATEGORIES, VALID_SEVERITIES,
    STALE_DAYS, DEFAULT_SCORE_THRESHOLD,
    TECH_ABBREVIATIONS, _expand_abbreviations,
    _stale_penalty, _substring_match_score,
    _EMBED_FAILED,
)
from kanban_framework.domain.knowledge_schema import (
    ensure_schema as _ensure_schema_impl,
    ensure_domains as _ensure_domains_impl,
    migrate_legacy_db as _migrate_legacy_db_impl,
    migrate_stale_at as _migrate_stale_at_impl,
)
from kanban_framework.domain.knowledge_chroma import (
    ensure_chroma as _ensure_chroma_impl,
    defer_embed_and_chroma as _defer_embed_and_chroma_impl,
    chroma_delete_entry as _chroma_delete_entry_impl,
)
from kanban_framework.domain.knowledge_search import (
    search_fts as _search_fts_impl,
    search_semantic as _search_semantic_impl,
    search_hybrid as _search_hybrid_impl,
    search_by_intent as _search_by_intent_impl,
)
from kanban_framework.domain.knowledge_management import (
    record_usage as _record_usage_impl,
    mark_stale_entries as _mark_stale_entries_impl,
    get_domains as _get_domains_impl,
    match_domain as _match_domain_impl,
    find_similar_pitfalls as _find_similar_pitfalls_impl,
    find_conflicting_solutions as _find_conflicting_solutions_impl,
    get_knowledge_gap_report as _get_knowledge_gap_report_impl,
    migrate_legacy_log as _migrate_legacy_log_impl,
    find_semantic_duplicates as _find_semantic_duplicates_impl,
    scan_stale_candidates as _scan_stale_candidates_impl,
    vacuum_database as _vacuum_database_impl,
)


def _tag_source(results: list[dict]) -> None:
    """Tag search results with _source if not already set by MultiBackend."""
    for r in results:
        if "_source" not in r:
            r["_source"] = "local"


class KnowledgeManager:
    def __init__(self, fs, backend=None, read_only=False):
        self._fs = fs
        self._read_only = read_only
        db_dir = fs.kanban_dir / "knowledge"
        fs.ensure_dir(db_dir)
        self._scope = self._read_scope(fs)
        db_name = f"knowledge-{self._scope}.db" if self._scope else "knowledge.db"
        self._db_path = db_dir / db_name
        _migrate_legacy_db_impl(self._db_path, self._scope, db_dir)
        self._conn = sqlite3.connect(str(self._db_path), timeout=5)
        self._conn.row_factory = sqlite3.Row
        self._conn.text_factory = str  # Fix #212: Chinese garbled on Windows
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA busy_timeout=10000")  # #536-001: 10s for concurrent writes
        self._chroma_client = None
        self._chroma_collection = None

        if read_only:
            try:
                self._conn.execute("SELECT 1 FROM entries LIMIT 1")
            except sqlite3.OperationalError:
                _ensure_schema_impl(self._conn)
            from kanban_framework.domain.knowledge_backend import BuiltinBackend
            self._backend = BuiltinBackend(self)
            import threading
            threading.Thread(target=_get_jieba, daemon=True).start()
        else:
            _ensure_schema_impl(self._conn)
            _ensure_domains_impl(self._conn)
            _migrate_stale_at_impl(self._conn)
            import threading
            threading.Thread(target=self._auto_backup, daemon=True).start()
            self._init_backend(fs, backend)

    def _init_backend(self, fs, backend):
        from kanban_framework.domain.knowledge_backend import resolve_backend, MultiBackend, ShareBackend

        if backend is None:
            backend_name = "builtin"
            share_path = None
            try:
                cfg_path = fs.config_file()
                if cfg_path.is_file():
                    raw = json.loads(cfg_path.read_text(encoding="utf-8"))
                    kb_cfg = raw.get("knowledge", {})
                    if isinstance(kb_cfg, dict):
                        backend_name = kb_cfg.get("backend", "builtin")
                        share_cfg = kb_cfg.get("share", {})
                        if isinstance(share_cfg, dict) and share_cfg.get("enabled"):
                            share_path = share_cfg.get("path")
            except Exception:
                pass

            primary = resolve_backend(backend_name, self)
            if share_path:
                share = ShareBackend(self, share_path)
                self._backend = MultiBackend(primary, share)
            else:
                self._backend = primary
        else:
            self._backend = backend

    _SCOPE_RE = __import__('re').compile(r"^[a-z0-9][a-z0-9-]{1,15}$")

    @staticmethod
    def _read_scope(fs) -> str:
        try:
            cfg_path = fs.config_file()
            if cfg_path.is_file():
                raw = json.loads(cfg_path.read_text(encoding="utf-8"))
                kb_cfg = raw.get("knowledge", {})
                if isinstance(kb_cfg, dict):
                    scope = kb_cfg.get("scope", "")
                    if isinstance(scope, str) and scope and KnowledgeManager._SCOPE_RE.match(scope):
                        return scope
        except Exception:
            pass
        return ""

    # ── Backup ────────────────────────────────────────────────────────────

    MAX_BACKUPS = 5

    def _auto_backup(self) -> None:
        import shutil
        try:
            src = self._db_path
            if not src.is_file() or src.stat().st_size == 0:
                return
            bak_prefix = src.stem
            newest = src.parent / f"{bak_prefix}.db.bak.1"
            if newest.is_file():
                age_s = time.time() - newest.stat().st_mtime
                if age_s < 3600:
                    return
            self._conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            for i in range(self.MAX_BACKUPS, 0, -1):
                old = src.parent / f"{bak_prefix}.db.bak.{i}"
                if old.is_file():
                    if i == self.MAX_BACKUPS:
                        old.unlink()
                    else:
                        new = src.parent / f"{bak_prefix}.db.bak.{i + 1}"
                        shutil.move(str(old), str(new))
            bak_path = src.parent / f"{bak_prefix}.db.bak.1"
            dst = sqlite3.connect(str(bak_path))
            self._conn.backup(dst)
            dst.close()
        except Exception:
            pass

    # ── CRUD ──────────────────────────────────────────────────────────────

    MAX_CONTENT_LENGTH = 3000
    MAX_CODE_EXAMPLE_LENGTH = 2000

    def add_entry(self, *, domain, category, title, content,
                  tags=None, severity="medium", source=None, code_example="",
                  status="active", upsert=False, ttl_days=None,
                  entry_type="knowledge", steps=None, benchmark=None,
                  biz_context=None, entry_id=None, evidence=None):
        if not title.strip() and not content.strip():
            raise ValueError("at least title or content is required")
        if len(content) > self.MAX_CONTENT_LENGTH:
            content = content[:self.MAX_CONTENT_LENGTH]
        if len(code_example) > self.MAX_CODE_EXAMPLE_LENGTH:
            code_example = code_example[:self.MAX_CODE_EXAMPLE_LENGTH]
        if category not in VALID_CATEGORIES:
            raise ValueError(
                f"invalid category '{category}'. Valid: {sorted(VALID_CATEGORIES.keys())}"
            )
        if severity not in VALID_SEVERITIES:
            raise ValueError(
                f"invalid severity '{severity}'. Valid: {sorted(VALID_SEVERITIES.keys())}"
            )
        tags = tags or []
        source = source or {}
        now = datetime.now(timezone.utc).isoformat()
        segmented = _segment(title) + " " + _segment(content)
        if code_example:
            segmented += " " + _segment(code_example)
        stale_at = None
        if ttl_days is not None and ttl_days > 0:
            stale_at = (datetime.now(timezone.utc) + timedelta(days=ttl_days)).isoformat()

        existing = self._conn.execute(
            "SELECT id FROM entries WHERE title=? AND domain=? LIMIT 1",
            (title.strip(), domain),
        ).fetchone()
        if existing:
            if not upsert:
                return {"id": existing[0], "skipped": True, "reason": "duplicate", "existing_id": existing[0]}
            # Snapshot old version before overwriting (#482)
            self._snapshot_version(existing[0], now, "upsert")
            self._conn.execute(
                """UPDATE entries SET category=?, content=?, content_segmented=?,
                   embedding=?, code_example=?, tags=?, source=?, severity=?,
                   status=?, updated_at=?, stale_at=?, type=?, steps=?, benchmark=?,
                   biz_context=?, evidence=?
                   WHERE id=?""",
                (category, content, segmented, None, code_example,
                 json.dumps(tags), json.dumps(source), severity, status, now,
                 stale_at, entry_type, json.dumps(steps) if steps else None,
                 json.dumps(benchmark) if benchmark else None,
                 biz_context, evidence, existing[0]),
            )
            self._conn.commit()
            entry = self.get_entry(existing[0])
            _defer_embed_and_chroma_impl(self, existing[0], title, content, domain, category, status, biz_context=biz_context)
            return entry

        eid = entry_id if entry_id else self._next_id()
        self._conn.execute(
            """INSERT INTO entries(id, domain, category, title, content, content_segmented,
               embedding, code_example, tags, source, severity, status,
               created_at, updated_at, stale_at, type, steps, benchmark, biz_context,
               evidence)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (eid, domain, category, title, content, segmented, None, code_example,
             json.dumps(tags), json.dumps(source), severity, status, now, now, stale_at,
             entry_type, json.dumps(steps) if steps else None,
             json.dumps(benchmark) if benchmark else None, biz_context, evidence),
        )
        self._conn.commit()
        entry = self.get_entry(eid)
        _defer_embed_and_chroma_impl(self, eid, title, content, domain, category, status, biz_context=biz_context)
        return entry

    def get_entry(self, entry_id):
        row = self._conn.execute("SELECT * FROM entries WHERE id=?", (entry_id,)).fetchone()
        return self._row_to_dict(row) if row else None

    def _snapshot_version(self, entry_id: str, snapshot_at: str, reason: str = "upsert") -> None:
        """Save current entry state to entry_versions before overwriting. (#482)"""
        row = self._conn.execute("SELECT * FROM entries WHERE id=?", (entry_id,)).fetchone()
        if not row:
            return
        d = self._row_to_dict(row)
        self._conn.execute(
            """INSERT INTO entry_versions(entry_id, content, code_example, tags, source,
               severity, snapshot_at, snapshot_reason, evidence)
               VALUES(?,?,?,?,?,?,?,?,?)""",
            (entry_id, d.get("content", ""), d.get("code_example", ""),
             json.dumps(d.get("tags", [])), json.dumps(d.get("source", {})),
             d.get("severity", "medium"), snapshot_at, reason,
             d.get("evidence")),
        )

    def list_versions(self, entry_id: str, limit: int = 20) -> list[dict]:
        """List version history for an entry. (#482)"""
        rows = self._conn.execute(
            """SELECT version_id, content, code_example, tags, severity,
               snapshot_at, snapshot_reason
               FROM entry_versions WHERE entry_id=?
               ORDER BY version_id DESC LIMIT ?""",
            (entry_id, limit),
        ).fetchall()
        results = []
        for r in rows:
            tags = r[3]
            try:
                tags = json.loads(tags) if isinstance(tags, str) else tags
            except (json.JSONDecodeError, TypeError):
                tags = []
            results.append({
                "version_id": r[0],
                "content": r[1],
                "code_example": r[2],
                "tags": tags,
                "severity": r[4],
                "snapshot_at": r[5],
                "snapshot_reason": r[6],
            })
        return results

    def restore_version(self, entry_id: str, version_id: int) -> dict:
        """Restore an entry to a specific version. (#482)"""
        entry = self.get_entry(entry_id)
        if not entry:
            raise ValueError(f"entry {entry_id} not found")
        ver = self._conn.execute(
            "SELECT * FROM entry_versions WHERE version_id=? AND entry_id=?",
            (version_id, entry_id),
        ).fetchone()
        if not ver:
            raise ValueError(f"version {version_id} not found for entry {entry_id}")
        now = datetime.now(timezone.utc).isoformat()
        # Snapshot current before restoring
        self._snapshot_version(entry_id, now, "restore")
        ver_dict = self._row_to_dict(ver) if not isinstance(ver, dict) else ver
        content = ver_dict.get("content", "")
        segmented = _segment(entry.get("title", "")) + " " + _segment(content)
        self._conn.execute(
            """UPDATE entries SET content=?, content_segmented=?, code_example=?,
               tags=?, severity=?, updated_at=?
               WHERE id=?""",
            (content, segmented,
             ver_dict.get("code_example", ""),
             json.dumps(ver_dict.get("tags", [])),
             ver_dict.get("severity", "medium"),
             now, entry_id),
        )
        self._conn.commit()
        _defer_embed_and_chroma_impl(self, entry_id, entry.get("title", ""),
                                     content, entry.get("domain", ""),
                                     entry.get("category", ""), entry.get("status", "active"),
                                     biz_context=entry.get("biz_context"))
        return self.get_entry(entry_id)

    def delete_entry(self, entry_id):
        # Delete FTS first (needs rowid from entries table)
        self._conn.execute("DELETE FROM entries_fts WHERE rowid=(SELECT rowid FROM entries WHERE id=?)", (entry_id,))
        self._conn.execute("DELETE FROM entries WHERE id=?", (entry_id,))
        self._conn.commit()
        # Synchronous ChromaDB delete to avoid inconsistency window (#480)
        try:
            _ensure_chroma_impl(self)
            _chroma_delete_entry_impl(self, entry_id)
        except Exception:
            pass

    def update_benchmark_evaluation(self, entry_id: str, evaluation: dict) -> dict:
        """Append evaluation result to benchmark.evaluations array. (#397)"""
        entry = self.get_entry(entry_id)
        if not entry:
            raise ValueError(f"entry {entry_id} not found")
        benchmark = entry.get("benchmark") or {}
        if not isinstance(benchmark, dict):
            benchmark = {}
        if "evaluations" not in benchmark:
            benchmark["evaluations"] = []
        from datetime import datetime, timezone
        evaluation["timestamp"] = datetime.now(timezone.utc).isoformat()
        benchmark["evaluations"].append(evaluation)
        self._conn.execute(
            "UPDATE entries SET benchmark = ? WHERE id = ?",
            (json.dumps(benchmark, ensure_ascii=False), entry_id),
        )
        self._conn.commit()
        return {
            "entry_id": entry_id,
            "evaluation_added": True,
            "total_evaluations": len(benchmark["evaluations"]),
        }

    def update_entry(self, entry_id: str, **kwargs) -> dict:
        """Update fields on a knowledge entry. Returns updated entry dict."""
        entry = self.get_entry(entry_id)
        if not entry:
            raise ValueError(f"entry {entry_id} not found")
        allowed = {"status", "severity", "domain", "category", "title", "content",
                   "tags", "code_example", "benchmark", "biz_context", "effectiveness"}
        for key, value in kwargs.items():
            if key not in allowed:
                raise ValueError(f"cannot update field: {key}")
            if key == "tags" and isinstance(value, list):
                value = json.dumps(value, ensure_ascii=False)
            self._conn.execute(
                f"UPDATE entries SET {key} = ?, updated_at = datetime('now') WHERE id = ?",
                (value, entry_id),
            )
        self._conn.commit()
        return self.get_entry(entry_id) or {}

    def list_entries(self, domain=None, category=None, status="active", limit=50, offset=0, biz_context=None):
        conditions = []
        params = []
        if domain:
            conditions.append("domain = ?")
            params.append(domain)
        if category:
            conditions.append("category = ?")
            params.append(category)
        if status:
            conditions.append("status = ?")
            params.append(status)
        if biz_context:
            conditions.append("(biz_context IS NULL OR biz_context = ?)")
            params.append(biz_context)
        where = " AND ".join(conditions) if conditions else "1=1"
        query = f"SELECT * FROM entries WHERE {where} ORDER BY id LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        rows = self._conn.execute(query, params).fetchall()
        return [self._row_to_dict(r) for r in rows]

    # ── Public search methods ─────────────────────────────────────────────

    def search(self, keyword, domain=None, limit=20, biz_context=None):
        if not keyword:
            return []
        results = self._backend.search(keyword, limit=limit, biz_context=biz_context) if self._backend else self._search_fts(keyword, limit=limit, biz_context=biz_context)
        if domain:
            results = [r for r in results if r.get("domain") == domain]
        _tag_source(results)
        return results

    def search_by_domain(self, domain, severity=None, status="active", limit=20):
        rows = self._conn.execute(
            """SELECT * FROM entries WHERE domain=? AND status=?
               {} ORDER BY referenced_count DESC LIMIT ?""".format(
                "AND severity=?" if severity else ""),
            (domain, status, *([severity] if severity else []), limit),
        ).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def search_by_tag(self, tag):
        rows = self._conn.execute(
            "SELECT * FROM entries WHERE tags LIKE ?", (f'%"{tag}"%',)
        ).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def search_by_task(self, task_id):
        rows = self._conn.execute(
            "SELECT * FROM entries WHERE source LIKE ?", (f'%"{task_id}"%',)
        ).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def search_semantic(self, query: str, limit: int = 20, biz_context: str | None = None) -> list[dict]:
        if self._backend is not None:
            results = self._backend.search_semantic(query, limit=limit, biz_context=biz_context)
        else:
            results = self._search_semantic(query, limit=limit, biz_context=biz_context)
        _tag_source(results)
        return results

    def search_hybrid(self, keyword: str, limit: int = 20,
                      relevance_threshold: float | None = None,
                      score_threshold: float | None = None,
                      biz_context: str | None = None) -> list[dict]:
        threshold = relevance_threshold if relevance_threshold is not None else score_threshold
        if threshold is None:
            threshold = DEFAULT_SCORE_THRESHOLD
        if self._backend is not None:
            results = self._backend.search_hybrid(keyword, limit=limit * 2, biz_context=biz_context)
        else:
            results = self._search_hybrid(keyword, limit=limit * 2, biz_context=biz_context)
        if threshold > 0:
            results = [r for r in results
                       if r.get("relevance", 0) >= threshold]
        _tag_source(results)
        return results[:limit]

    # ── Internal search delegates (called by BuiltinBackend) ──────────────

    def _search_fts(self, keyword, limit=20, *, biz_context=None):
        return _search_fts_impl(self, keyword, limit=limit, biz_context=biz_context)

    def _search_semantic(self, query, limit=20, *, biz_context=None):
        return _search_semantic_impl(self, query, limit=limit, biz_context=biz_context)

    def _search_hybrid(self, keyword, limit=20, *, biz_context=None):
        return _search_hybrid_impl(self, keyword, limit=limit, biz_context=biz_context)

    def _ensure_chroma(self):
        return _ensure_chroma_impl(self)

    def _chroma_upsert_entry(self, entry_id, title, content, domain, category, status):
        from kanban_framework.domain.knowledge_chroma import chroma_upsert_entry
        chroma_upsert_entry(self, entry_id, title, content, domain, category, status)

    def _migrate_stale_at(self):
        _migrate_stale_at_impl(self._conn)

    # ── Internal CRUD delegates (called by BuiltinBackend) ────────────────

    def _add_entry_internal(self, **kwargs) -> dict:
        return self.add_entry(**kwargs)

    def _list_entries_internal(
        self, domain=None, category=None, status="active",
        limit=50, offset=0, biz_context=None,
    ) -> list[dict]:
        return self.list_entries(
            domain=domain, category=category, status=status,
            limit=limit, offset=offset, biz_context=biz_context,
        )

    def _get_entry_internal(self, entry_id: str) -> dict | None:
        try:
            return self.get_entry(entry_id)
        except Exception:
            return None

    # ── Intent-based search ───────────────────────────────────────────────

    def search_by_intent(self, intent: str, query: str, limit: int = 20, *, biz_context: str | None = None, **context) -> list[dict]:
        return _search_by_intent_impl(self, intent, query, limit=limit, biz_context=biz_context, **context)

    # ── Management methods (thin delegates) ───────────────────────────────

    def record_usage(self, entry_id, task_id):
        _record_usage_impl(self, entry_id, task_id)

    def update_effectiveness(self, entry_id: str, task_id: str,
                             score: float, phase: str = "") -> None:
        """Record a positive or negative effectiveness signal for a knowledge entry.

        Stores result in the entry's effectiveness JSON field:
        {"positive": N, "negative": M, "history": [{task_id, score, phase, ts}]}
        """
        entry = self.get_entry(entry_id)
        if not entry:
            return
        eff = entry.get("effectiveness")
        if isinstance(eff, str):
            try:
                eff = json.loads(eff)
            except (json.JSONDecodeError, TypeError):
                eff = None
        if not isinstance(eff, dict):
            eff = {"positive": 0, "negative": 0, "history": []}

        PASS_THRESHOLD = 8.0
        if score >= PASS_THRESHOLD:
            eff["positive"] = eff.get("positive", 0) + 1
        else:
            eff["negative"] = eff.get("negative", 0) + 1

        from datetime import datetime, timezone
        eff["history"].append({
            "task_id": task_id, "score": score, "phase": phase,
            "ts": datetime.now(timezone.utc).isoformat(),
        })
        # Keep last 20 history entries
        if len(eff["history"]) > 20:
            eff["history"] = eff["history"][-20:]

        total = eff["positive"] + eff["negative"]
        eff["score"] = round(eff["positive"] / total, 3) if total > 0 else None
        self._conn.execute(
            "UPDATE entries SET effectiveness=? WHERE id=?",
            (json.dumps(eff, ensure_ascii=False), entry_id),
        )
        self._conn.commit()

    def mark_stale_entries(self):
        return _mark_stale_entries_impl(self)

    def get_domains(self):
        return _get_domains_impl(self)

    def match_domain(self, text):
        return _match_domain_impl(self, text)

    def find_similar_pitfalls(self, tags, min_tag_overlap=2):
        return _find_similar_pitfalls_impl(self, tags, min_tag_overlap=min_tag_overlap)

    def find_conflicting_solutions(self, task_id=""):
        return _find_conflicting_solutions_impl(self, task_id=task_id)

    def get_knowledge_gap_report(self):
        return _get_knowledge_gap_report_impl(self)

    def migrate_legacy_log(self):
        return _migrate_legacy_log_impl(self)

    def find_semantic_duplicates(self, threshold=0.85):
        return _find_semantic_duplicates_impl(self, threshold=threshold)

    def scan_stale_candidates(self):
        return _scan_stale_candidates_impl(self)

    def vacuum_database(self):
        return _vacuum_database_impl(self)

    # ── Helpers ───────────────────────────────────────────────────────────

    def _next_id(self):
        prefix = self._scope
        if prefix:
            row = self._conn.execute(
                "SELECT id FROM entries WHERE id LIKE ? ORDER BY LENGTH(id) DESC, id DESC LIMIT 1",
                (f"{prefix}%",)
            ).fetchone()
            if not row:
                return f"{prefix}001"
            try:
                num_str = row[0][len(prefix):]
                num = int(num_str)
                if num < 0:
                    return f"{prefix}001"
                return f"{prefix}{num + 1:03d}"
            except ValueError:
                return f"{prefix}001"
        else:
            row = self._conn.execute(
                "SELECT id FROM entries WHERE id GLOB 'K[0-9]*' "
                "ORDER BY CAST(SUBSTR(id, 2) AS INTEGER) DESC LIMIT 1"
            ).fetchone()
            if not row:
                return "K001"
            try:
                return f"K{int(row[0][1:]) + 1:03d}"
            except ValueError:
                return "K001"

    def _row_to_dict(self, row):
        d = dict(row)
        for key, val in list(d.items()):
            if isinstance(val, bytes):
                d[key] = val.decode("utf-8", errors="replace")
        for field in ("tags", "source", "steps"):
            if field in d and isinstance(d[field], str):
                try:
                    d[field] = json.loads(d[field])
                except (json.JSONDecodeError, TypeError):
                    d[field] = [] if field in ("tags", "steps") else {}
        if "benchmark" in d and isinstance(d.get("benchmark"), str):
            try:
                d["benchmark"] = json.loads(d["benchmark"])
            except (json.JSONDecodeError, TypeError):
                pass
        d.pop("embedding", None)
        return d

    def _all_entry_ids(self):
        return [r[0] for r in self._conn.execute("SELECT id FROM entries ORDER BY id")]

    def close(self):
        try:
            self._conn.close()
        except Exception:
            pass
        try:
            if self._chroma_client:
                self._chroma_client = None
                self._chroma_collection = None
        except Exception:
            pass

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
