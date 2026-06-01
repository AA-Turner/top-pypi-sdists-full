"""Share backend — shared knowledge base at an external path. (#237)"""
from __future__ import annotations


class ShareBackend:
    """Backend wrapping a shared knowledge base at an external path. (#237)

    Points to another kanban knowledge.db (e.g. ~/.kanban/knowledge_share/knowledge.db).
    Uses the same SQLite schema as builtin — just a different database file.
    """

    def __init__(self, knowledge_manager, share_path):
        self._km = knowledge_manager
        self._share_km = None
        self._share_path = share_path
        self._init_share()

    def _init_share(self):
        import sqlite3
        from pathlib import Path
        db_path = Path(self._share_path).expanduser().resolve()
        if db_path.suffix != '.db':
            db_path = db_path.with_suffix(db_path.suffix + '.db')
        if not db_path.is_file():
            self._share_km = None
            return
        try:
            self._share_conn = sqlite3.connect(str(db_path))
            self._share_conn.row_factory = sqlite3.Row
        except Exception:
            self._share_conn = None

    def _search_share(self, keyword, limit=20):
        if not hasattr(self, '_share_conn') or self._share_conn is None:
            return []
        fts_query = keyword
        if any('一' <= c <= '鿿' for c in keyword):
            try:
                from kanban_framework.domain.knowledge import _get_jieba
                jieba = _get_jieba()
                if jieba:
                    segmented = " ".join(w for w in jieba.cut(keyword) if w.strip())
                    fts_query = segmented.replace(" ", " OR ")
            except Exception:
                pass
        try:
            fts_rows = self._share_conn.execute(
                "SELECT e.*, bm25(entries_fts) as score FROM entries e "
                "JOIN entries_fts ON e.rowid = entries_fts.rowid "
                "WHERE entries_fts MATCH ? AND e.status='active' "
                "ORDER BY score LIMIT ?",
                (fts_query, limit)
            ).fetchall()
            results = [dict(r) for r in fts_rows]
            fts_ids = {r['id'] for r in results}
            remaining = limit - len(results)
            if remaining > 0:
                like_rows = self._share_conn.execute(
                    "SELECT *, 0.3 as score FROM entries WHERE status='active' "
                    "AND (title LIKE ? OR content LIKE ?) LIMIT ?",
                    (f"%{keyword}%", f"%{keyword}%", remaining + len(fts_ids))
                ).fetchall()
                for r in like_rows:
                    d = dict(r)
                    if d['id'] not in fts_ids:
                        results.append(d)
                        if len(results) >= limit:
                            break
            if results:
                return results
            return []
        except Exception:
            try:
                rows = self._share_conn.execute(
                    "SELECT *, 0.3 as score FROM entries WHERE status='active' "
                    "AND (title LIKE ? OR content LIKE ?) LIMIT ?",
                    (f"%{keyword}%", f"%{keyword}%", limit)
                ).fetchall()
                return [dict(r) for r in rows]
            except Exception:
                return []

    def search(self, keyword, limit=20):
        return self._search_share(keyword, limit=limit)

    def search_semantic(self, query, limit=20):
        return self._search_share(query, limit=limit)

    def search_hybrid(self, keyword, limit=20):
        return self._search_share(keyword, limit=limit)

    def add_entry(self, **kwargs):
        """Push entry to shared knowledge base. (#237)"""
        if not hasattr(self, '_share_conn') or self._share_conn is None:
            raise RuntimeError("Share backend not available")
        import json
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        title = kwargs.get("title", "")
        domain = kwargs.get("domain", "")
        content = kwargs.get("content", "")

        existing = self._share_conn.execute(
            "SELECT id, content, tags, source FROM entries WHERE title=? AND domain=? AND status='active' LIMIT 1",
            (title, domain)
        ).fetchone()

        if existing:
            existing_id = existing[0]
            existing_content = existing[1] or ""
            existing_tags = json.loads(existing[2]) if existing[2] else []
            existing_source = json.loads(existing[3]) if existing[3] else {}

            new_tags = list(set(existing_tags + kwargs.get("tags", [])))
            merged_content = existing_content
            if content and content not in existing_content:
                merged_content = existing_content + "\n\n---\n[补充] " + content

            new_source = dict(kwargs.get("source", {})) if kwargs.get("source") else {}
            if isinstance(new_source, str):
                try:
                    new_source = json.loads(new_source)
                except (json.JSONDecodeError, TypeError):
                    new_source = {}
            origin_id = kwargs.get("id", "")
            if origin_id:
                new_source["origin_id"] = origin_id
            scope = getattr(self._km, '_scope', '')
            if scope:
                new_source["origin_scope"] = scope
            origins = existing_source.get("merged_origins", [])
            if existing_source.get("origin_scope"):
                origins.append(existing_source["origin_scope"])
            if new_source.get("origin_scope") and new_source["origin_scope"] not in origins:
                origins.append(new_source["origin_scope"])
            merged_source = {**existing_source, **new_source, "merged_origins": origins}

            try:
                from kanban_framework.domain.knowledge import _get_jieba
                jieba = _get_jieba()
                content_segmented = ' '.join(jieba.cut(title + ' ' + merged_content))
            except Exception:
                content_segmented = ''

            self._share_conn.execute(
                """UPDATE entries SET content=?, content_segmented=?, code_example=?,
                   tags=?, source=?, severity=?, updated_at=? WHERE id=?""",
                (merged_content, content_segmented,
                 kwargs.get("code_example", ""),
                 json.dumps(new_tags), json.dumps(merged_source),
                 kwargs.get("severity", "medium"), now.isoformat(), existing_id)
            )
            self._share_conn.commit()
            return {**kwargs, "id": existing_id, "source": merged_source, "merged": True}

        eid = f"S{now.strftime('%Y%m%d%H%M%S')}-{now.microsecond // 1000:03d}"
        source = dict(kwargs.get("source", {})) if kwargs.get("source") else {}
        if isinstance(source, str):
            try:
                source = json.loads(source)
            except (json.JSONDecodeError, TypeError):
                source = {}
        origin_id = kwargs.get("id", "")
        if origin_id:
            source["origin_id"] = origin_id
        scope = getattr(self._km, '_scope', '')
        if scope:
            source["origin_scope"] = scope
        try:
            from kanban_framework.domain.knowledge import _get_jieba
            jieba = _get_jieba()
            content_segmented = ' '.join(jieba.cut(title + ' ' + content))
        except Exception:
            content_segmented = ''
        self._share_conn.execute(
            """INSERT INTO entries(id, domain, category, title, content,
               content_segmented, code_example, tags, source, severity,
               status, created_at, type, steps)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (eid, domain, kwargs.get("category", ""),
             title, content, content_segmented,
             kwargs.get("code_example", ""),
             json.dumps(kwargs.get("tags", [])),
             json.dumps(source),
             kwargs.get("severity", "medium"), "active", now.isoformat(),
             kwargs.get("entry_type", "knowledge"),
             json.dumps(kwargs.get("steps")) if kwargs.get("steps") else None)
        )
        self._share_conn.commit()
        return {**kwargs, "id": eid, "source": source}

    def list_entries(self, domain=None, category=None, status="active", limit=50, offset=0):
        if not hasattr(self, '_share_conn') or self._share_conn is None:
            return []
        try:
            clauses = ["status=?"]
            params = [status]
            if domain:
                clauses.append("domain=?")
                params.append(domain)
            if category:
                clauses.append("category=?")
                params.append(category)
            where = " AND ".join(clauses)
            params.extend([limit, offset])
            rows = self._share_conn.execute(
                f"SELECT * FROM entries WHERE {where} LIMIT ? OFFSET ?",
                params
            ).fetchall()
            import json
            results = []
            for r in rows:
                d = dict(r)
                for field in ("tags", "source", "steps"):
                    if field in d and isinstance(d[field], str):
                        try:
                            d[field] = json.loads(d[field])
                        except (json.JSONDecodeError, TypeError):
                            d[field] = [] if field in ("tags", "steps") else {}
                d.pop("embedding", None)
                results.append(d)
            return results
        except Exception:
            return []

    def get_entry(self, entry_id):
        if not hasattr(self, '_share_conn') or self._share_conn is None:
            return None
        row = self._share_conn.execute("SELECT * FROM entries WHERE id=?",
                                        (entry_id,)).fetchone()
        return dict(row) if row else None

    @staticmethod
    def init_db(path: str) -> dict:
        """Create a new shared knowledge database with full schema."""
        from pathlib import Path
        import sqlite3
        db_path = Path(path).expanduser().resolve()
        if db_path.suffix != '.db':
            db_path = db_path.with_suffix(db_path.suffix + '.db')
        if db_path.is_file():
            return {"error": f"File already exists: {db_path}"}
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(db_path))
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS entries (
                id TEXT PRIMARY KEY, domain TEXT NOT NULL, category TEXT NOT NULL,
                title TEXT NOT NULL, content TEXT NOT NULL,
                content_segmented TEXT DEFAULT '', code_example TEXT DEFAULT '',
                tags TEXT DEFAULT '[]', source TEXT DEFAULT '{}',
                severity TEXT DEFAULT 'medium', status TEXT DEFAULT 'active',
                created_at TEXT NOT NULL, updated_at TEXT, stale_at TEXT,
                referenced_count INTEGER DEFAULT 0, last_referenced_at TEXT,
                last_referenced_by TEXT, type TEXT DEFAULT 'knowledge',
                steps TEXT DEFAULT NULL, embedding BLOB DEFAULT NULL
            );
            CREATE TABLE IF NOT EXISTS usage_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_id TEXT NOT NULL, task_id TEXT NOT NULL, timestamp TEXT NOT NULL
            );
            CREATE VIRTUAL TABLE entries_fts USING fts5(
                title, content, content_segmented, code_example, tags,
                content=entries, content_rowid=rowid
            );
            CREATE TABLE IF NOT EXISTS domains (name TEXT PRIMARY KEY, label TEXT, keywords TEXT);
        """)
        conn.executescript("""
            CREATE TRIGGER entries_ai AFTER INSERT ON entries BEGIN
                INSERT INTO entries_fts(rowid, title, content, content_segmented, code_example, tags)
                VALUES (new.rowid, new.title, new.content, new.content_segmented, new.code_example, new.tags);
            END;
            CREATE TRIGGER entries_ad AFTER DELETE ON entries BEGIN
                INSERT INTO entries_fts(entries_fts, rowid, title, content, content_segmented, code_example, tags)
                VALUES ('delete', old.rowid, old.title, old.content, old.content_segmented, old.code_example, old.tags);
            END;
            CREATE TRIGGER entries_au AFTER UPDATE ON entries BEGIN
                INSERT INTO entries_fts(entries_fts, rowid, title, content, content_segmented, code_example, tags)
                VALUES ('delete', old.rowid, old.title, old.content, old.content_segmented, old.code_example, old.tags);
                INSERT INTO entries_fts(rowid, title, content, content_segmented, code_example, tags)
                VALUES (new.rowid, new.title, new.content, new.content_segmented, new.code_example, new.tags);
            END;
        """)
        conn.commit()
        conn.close()
        return {"created": str(db_path)}

    def close(self):
        if hasattr(self, '_share_conn') and self._share_conn is not None:
            try:
                self._share_conn.close()
            except Exception:
                pass
            self._share_conn = None

    def __del__(self):
        self.close()
