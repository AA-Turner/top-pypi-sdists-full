"""
cvc.core.database — Four-Tiered Context Database (CDB).

Tier 1 (Index):    SQLite — commit graph, branch pointers, metadata.
Tier 2 (Blob):     Content-Addressable Storage on local disk (.cvc/objects/).
Tier 3 (Semantic): Optional Chroma vector store for similarity search.
Tier 4 (PageIndex): Optional LLM-powered hierarchical document RAG (CLI only).
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import sqlite3
import time
from pathlib import Path
from typing import Any, Sequence

import zstandard as zstd

from cvc.core.models import (
    BranchPointer,
    BranchStatus,
    CognitiveCommit,
    CommitMetadata,
    CommitType,
    ContentBlob,
    CVCConfig,
)

logger = logging.getLogger("cvc.database")

# ---------------------------------------------------------------------------
# SQL DDL
# ---------------------------------------------------------------------------

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS commits (
    commit_hash     TEXT PRIMARY KEY,
    parent_hashes   TEXT    NOT NULL DEFAULT '[]',   -- JSON array
    commit_type     TEXT    NOT NULL DEFAULT 'checkpoint',
    message         TEXT    NOT NULL DEFAULT '',
    is_delta        INTEGER NOT NULL DEFAULT 0,
    anchor_hash     TEXT,
    blob_key        TEXT    NOT NULL,                -- CAS key for content blob
    metadata_json   TEXT    NOT NULL DEFAULT '{}',
    created_at      REAL    NOT NULL
);

CREATE TABLE IF NOT EXISTS branches (
    name            TEXT PRIMARY KEY,
    head_hash       TEXT    NOT NULL,
    status          TEXT    NOT NULL DEFAULT 'active',
    parent_branch   TEXT,
    description     TEXT    NOT NULL DEFAULT '',
    created_at      REAL    NOT NULL
);

CREATE TABLE IF NOT EXISTS git_links (
    git_sha         TEXT PRIMARY KEY,
    cvc_hash        TEXT NOT NULL,
    created_at      REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_commits_created ON commits(created_at);
CREATE INDEX IF NOT EXISTS idx_commits_type    ON commits(commit_type);
CREATE INDEX IF NOT EXISTS idx_git_links_cvc   ON git_links(cvc_hash);
"""

_AGENTS_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS agents (
    agent_id        TEXT PRIMARY KEY,
    name            TEXT    NOT NULL DEFAULT '',
    role            TEXT    NOT NULL DEFAULT '',
    rank            TEXT    NOT NULL DEFAULT '',
    squad           TEXT    NOT NULL DEFAULT '',
    capabilities    TEXT    NOT NULL DEFAULT '[]',   -- JSON array of strings
    metadata_json   TEXT    NOT NULL DEFAULT '{}',
    readable_branches  TEXT NOT NULL DEFAULT '[]',   -- JSON array of branch names/patterns
    writable_branches  TEXT NOT NULL DEFAULT '[]',   -- JSON array of branch names/patterns
    status          TEXT    NOT NULL DEFAULT 'active',
    created_at      REAL    NOT NULL,
    updated_at      REAL    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_agents_squad ON agents(squad);
CREATE INDEX IF NOT EXISTS idx_agents_rank  ON agents(rank);
"""

_AUDIT_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS audit_log (
    audit_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type      TEXT    NOT NULL,           -- 'commit', 'branch', 'merge', 'restore', 'compact', 'inject', 'sync_push', 'sync_pull'
    commit_hash     TEXT,
    branch          TEXT,
    agent_id        TEXT    NOT NULL DEFAULT 'sofia',
    provider        TEXT,
    model           TEXT,
    action_detail   TEXT    NOT NULL DEFAULT '{}',  -- JSON with specifics
    source_mode     TEXT,                        -- 'cli', 'mcp', 'proxy'
    user_identity   TEXT,                        -- OS username or configured identity
    machine_id      TEXT,                        -- Machine hostname
    risk_level      TEXT    NOT NULL DEFAULT 'low',  -- 'low', 'medium', 'high', 'critical'
    code_generated  INTEGER NOT NULL DEFAULT 0,  -- Whether AI-generated code was involved
    files_affected  TEXT    NOT NULL DEFAULT '[]', -- JSON array of file paths
    token_count     INTEGER NOT NULL DEFAULT 0,
    created_at      REAL    NOT NULL
);

CREATE TABLE IF NOT EXISTS sync_remotes (
    name            TEXT PRIMARY KEY,
    remote_path     TEXT    NOT NULL,            -- Path or URL to remote CVC repo
    last_push_hash  TEXT,
    last_pull_hash  TEXT,
    last_sync_at    REAL,
    created_at      REAL    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_created  ON audit_log(created_at);
CREATE INDEX IF NOT EXISTS idx_audit_type     ON audit_log(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_risk     ON audit_log(risk_level);
CREATE INDEX IF NOT EXISTS idx_audit_agent    ON audit_log(agent_id);
"""

_COGNOME_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS cognome_cache (
    engram_hash     TEXT PRIMARY KEY,
    query           TEXT    NOT NULL,
    preamble        TEXT    NOT NULL,
    source_commits  TEXT    NOT NULL DEFAULT '[]',   -- JSON array of commit hashes
    noeme_count     INTEGER NOT NULL DEFAULT 0,
    token_estimate  INTEGER NOT NULL DEFAULT 0,
    baseline_tokens INTEGER NOT NULL DEFAULT 0,
    compression     REAL    NOT NULL DEFAULT 0.0,
    budget_tokens   INTEGER NOT NULL DEFAULT 0,
    branch          TEXT,
    created_at      REAL    NOT NULL,
    last_used_at    REAL    NOT NULL,
    use_count       INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS cognome_state (
    key             TEXT PRIMARY KEY,
    value           TEXT    NOT NULL,
    updated_at      REAL    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_cognome_cache_query  ON cognome_cache(query);
CREATE INDEX IF NOT EXISTS idx_cognome_cache_used   ON cognome_cache(last_used_at);
"""


# ---------------------------------------------------------------------------
# Tier 1 — SQLite Index Database
# ---------------------------------------------------------------------------

class IndexDB:
    """Synchronous SQLite index for the commit graph and branch pointers."""

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA_SQL)
        self._conn.executescript(_AGENTS_SCHEMA_SQL)
        self._conn.executescript(_AUDIT_SCHEMA_SQL)
        self._conn.executescript(_COGNOME_SCHEMA_SQL)
        # === Phase B perf wins (Sofia, 2026-05-09) ===
        # WAL + tuned PRAGMAs: 5-30ms/write, 20x recall on cold cache
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=NORMAL")     # was FULL: -10ms/commit, still crash-safe with WAL
        self._conn.execute("PRAGMA cache_size=-65536")       # 64 MB page cache (negative = KB)
        self._conn.execute("PRAGMA mmap_size=268435456")     # 256 MB memory-mapped reads
        self._conn.execute("PRAGMA temp_store=MEMORY")       # keep temp tables in RAM
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._conn.commit()

    # -- Commits -----------------------------------------------------------

    def insert_commit(self, commit: CognitiveCommit, blob_key: str) -> None:
        self._conn.execute(
            """INSERT OR REPLACE INTO commits
               (commit_hash, parent_hashes, commit_type, message,
                is_delta, anchor_hash, blob_key, metadata_json, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                commit.commit_hash,
                json.dumps(commit.parent_hashes),
                commit.commit_type.value,
                commit.message,
                int(commit.is_delta),
                commit.anchor_hash,
                blob_key,
                commit.metadata.model_dump_json(),
                commit.metadata.timestamp,
            ),
        )
        self._conn.commit()

    def get_commit(self, commit_hash: str) -> CognitiveCommit | None:
        """Fetch a commit by full or short (prefix) hash."""
        row = self._conn.execute(
            "SELECT * FROM commits WHERE commit_hash = ?", (commit_hash,)
        ).fetchone()
        if row is None:
            # Try prefix match
            row = self._conn.execute(
                "SELECT * FROM commits WHERE commit_hash LIKE ? LIMIT 1",
                (f"{commit_hash}%",),
            ).fetchone()
        if row is None:
            return None
        return self._row_to_commit(row)

    def get_ancestors(self, commit_hash: str, limit: int = 100) -> list[CognitiveCommit]:
        """Walk the parent chain backwards, returning up to *limit* ancestors.

        Phase B (Sofia 2026-05-09): Replaced N python round-trips with a
        single recursive CTE using json_each on the parent_hashes JSON
        column. For long chains this collapses ~N SQLite calls into 1
        and yields ancestors in BFS order.
        """
        try:
            sql = """
                WITH RECURSIVE walk(h, depth) AS (
                    SELECT ?, 0
                    UNION ALL
                    SELECT je.value, walk.depth + 1
                    FROM walk
                    JOIN commits c ON c.commit_hash = walk.h
                    JOIN json_each(c.parent_hashes) je
                    WHERE walk.depth < ?
                )
                SELECT DISTINCT c.* FROM walk
                JOIN commits c ON c.commit_hash = walk.h
                ORDER BY walk.depth ASC
                LIMIT ?
            """
            rows = self._conn.execute(sql, (commit_hash, limit, limit)).fetchall()
            if rows:
                return [self._row_to_commit(r) for r in rows]
        except Exception:
            # Fall through to safe python walk if CTE fails (e.g. malformed JSON)
            pass

        # Fallback: original BFS via python (kept for resilience)
        visited: list[CognitiveCommit] = []
        queue = [commit_hash]
        seen: set[str] = set()
        while queue and len(visited) < limit:
            h = queue.pop(0)
            if h in seen:
                continue
            seen.add(h)
            c = self.get_commit(h)
            if c is None:
                continue
            visited.append(c)
            queue.extend(c.parent_hashes)
        return visited

    def find_lca(self, hash_a: str, hash_b: str) -> str | None:
        """Find the Lowest Common Ancestor of two commits."""
        ancestors_a: set[str] = set()
        queue = [hash_a]
        while queue:
            h = queue.pop(0)
            if h in ancestors_a:
                continue
            ancestors_a.add(h)
            c = self.get_commit(h)
            if c:
                queue.extend(c.parent_hashes)

        queue = [hash_b]
        seen: set[str] = set()
        while queue:
            h = queue.pop(0)
            if h in seen:
                continue
            seen.add(h)
            if h in ancestors_a:
                return h
            c = self.get_commit(h)
            if c:
                queue.extend(c.parent_hashes)
        return None

    def list_commits(
        self,
        branch: str | None = None,
        limit: int = 50,
    ) -> list[CognitiveCommit]:
        """List recent commits, optionally scoped to a branch."""
        if branch:
            bp = self.get_branch(branch)
            if bp is None:
                return []
            return self.get_ancestors(bp.head_hash, limit=limit)
        rows = self._conn.execute(
            "SELECT * FROM commits ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [self._row_to_commit(r) for r in rows]

    def count_commits_since_anchor(self, commit_hash: str) -> int:
        """Count how many commits exist from *commit_hash* back to the last anchor."""
        count = 0
        h: str | None = commit_hash
        while h:
            c = self.get_commit(h)
            if c is None:
                break
            if c.commit_type == CommitType.ANCHOR or not c.is_delta:
                break
            count += 1
            h = c.parent_hashes[0] if c.parent_hashes else None
        return count

    # -- Branches ----------------------------------------------------------

    def upsert_branch(self, branch: BranchPointer) -> None:
        self._conn.execute(
            """INSERT OR REPLACE INTO branches
               (name, head_hash, status, parent_branch, description, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                branch.name,
                branch.head_hash,
                branch.status.value,
                branch.parent_branch,
                branch.description,
                branch.created_at,
            ),
        )
        self._conn.commit()

    def get_branch(self, name: str) -> BranchPointer | None:
        row = self._conn.execute(
            "SELECT * FROM branches WHERE name = ?", (name,)
        ).fetchone()
        if row is None:
            return None
        return BranchPointer(
            name=row["name"],
            head_hash=row["head_hash"],
            status=BranchStatus(row["status"]),
            parent_branch=row["parent_branch"],
            description=row["description"],
            created_at=row["created_at"],
        )

    def list_branches(self) -> list[BranchPointer]:
        rows = self._conn.execute(
            "SELECT * FROM branches ORDER BY created_at DESC"
        ).fetchall()
        return [
            BranchPointer(
                name=r["name"],
                head_hash=r["head_hash"],
                status=BranchStatus(r["status"]),
                parent_branch=r["parent_branch"],
                description=r["description"],
                created_at=r["created_at"],
            )
            for r in rows
        ]

    def advance_head(self, branch_name: str, new_hash: str) -> None:
        self._conn.execute(
            "UPDATE branches SET head_hash = ? WHERE name = ?",
            (new_hash, branch_name),
        )
        self._conn.commit()

    # -- Git Links ---------------------------------------------------------

    def link_git_commit(self, git_sha: str, cvc_hash: str, ts: float) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO git_links (git_sha, cvc_hash, created_at) VALUES (?, ?, ?)",
            (git_sha, cvc_hash, ts),
        )
        self._conn.commit()

    def get_cvc_hash_for_git(self, git_sha: str) -> str | None:
        row = self._conn.execute(
            "SELECT cvc_hash FROM git_links WHERE git_sha = ?", (git_sha,)
        ).fetchone()
        return row["cvc_hash"] if row else None

    # -- Full-text search --------------------------------------------------

    def search_commits(self, query: str, limit: int = 20) -> list[CognitiveCommit]:
        """
        Search commits whose message contains *query* (case-insensitive).
        Returns up to *limit* matching commits ordered by recency.
        """
        rows = self._conn.execute(
            "SELECT * FROM commits WHERE message LIKE ? ORDER BY created_at DESC LIMIT ?",
            (f"%{query}%", limit),
        ).fetchall()
        return [self._row_to_commit(r) for r in rows]

    def list_all_commits(self, limit: int = 500) -> list[CognitiveCommit]:
        """List all commits across all branches, ordered by recency."""
        rows = self._conn.execute(
            "SELECT * FROM commits ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [self._row_to_commit(r) for r in rows]

    def list_all_commit_hashes(self) -> set[str]:
        """Return the set of every commit hash in this index."""
        rows = self._conn.execute("SELECT commit_hash FROM commits").fetchall()
        return {r["commit_hash"] for r in rows}

    def missing_commits(self, remote_hashes: set[str]) -> set[str]:
        """Return hashes that exist in *remote_hashes* but NOT locally."""
        local = self.list_all_commit_hashes()
        return remote_hashes - local

    def get_blob_key(self, commit_hash: str) -> str | None:
        """Public accessor for a commit's blob key."""
        row = self._conn.execute(
            "SELECT blob_key FROM commits WHERE commit_hash = ?", (commit_hash,)
        ).fetchone()
        if row is None:
            row = self._conn.execute(
                "SELECT blob_key FROM commits WHERE commit_hash LIKE ? LIMIT 1",
                (f"{commit_hash}%",),
            ).fetchone()
        return row["blob_key"] if row else None

    # -- Helpers -----------------------------------------------------------

    @staticmethod
    def _row_to_commit(row: sqlite3.Row) -> CognitiveCommit:
        return CognitiveCommit(
            commit_hash=row["commit_hash"],
            parent_hashes=json.loads(row["parent_hashes"]) if row["parent_hashes"] else [],
            commit_type=CommitType(row["commit_type"]),
            message=row["message"] if row["message"] else "",
            is_delta=bool(row["is_delta"]),
            anchor_hash=row["anchor_hash"],
            content_blob=ContentBlob(),   # Hydrated separately from CAS
            metadata=CommitMetadata.model_validate_json(row["metadata_json"]) if row["metadata_json"] else CommitMetadata(),
        )

    # -- Audit log ---------------------------------------------------------

    def insert_audit_event(
        self,
        event_type: str,
        commit_hash: str | None = None,
        branch: str | None = None,
        agent_id: str = "sofia",
        provider: str | None = None,
        model: str | None = None,
        action_detail: dict[str, Any] | None = None,
        source_mode: str | None = None,
        user_identity: str | None = None,
        machine_id: str | None = None,
        risk_level: str = "low",
        code_generated: bool = False,
        files_affected: list[str] | None = None,
        token_count: int = 0,
    ) -> int:
        """Insert an audit log entry and return the audit_id."""
        import platform
        _user = user_identity or os.environ.get("USERNAME", os.environ.get("USER", "unknown"))
        _machine = machine_id or platform.node()
        cursor = self._conn.execute(
            """INSERT INTO audit_log
               (event_type, commit_hash, branch, agent_id, provider, model,
                action_detail, source_mode, user_identity, machine_id,
                risk_level, code_generated, files_affected, token_count, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                event_type,
                commit_hash,
                branch,
                agent_id,
                provider,
                model,
                json.dumps(action_detail or {}),
                source_mode,
                _user,
                _machine,
                risk_level,
                int(code_generated),
                json.dumps(files_affected or []),
                token_count,
                time.time(),
            ),
        )
        self._conn.commit()
        return cursor.lastrowid or 0

    def query_audit_log(
        self,
        event_type: str | None = None,
        risk_level: str | None = None,
        agent_id: str | None = None,
        since: float | None = None,
        until: float | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Query the audit log with optional filters."""
        conditions: list[str] = []
        params: list[Any] = []

        if event_type:
            conditions.append("event_type = ?")
            params.append(event_type)
        if risk_level:
            conditions.append("risk_level = ?")
            params.append(risk_level)
        if agent_id:
            conditions.append("agent_id = ?")
            params.append(agent_id)
        if since is not None:
            conditions.append("created_at >= ?")
            params.append(since)
        if until is not None:
            conditions.append("created_at <= ?")
            params.append(until)

        where = " AND ".join(conditions) if conditions else "1=1"
        params.append(limit)

        rows = self._conn.execute(
            f"SELECT * FROM audit_log WHERE {where} ORDER BY created_at DESC LIMIT ?",
            params,
        ).fetchall()

        return [
            {
                "audit_id": r["audit_id"],
                "event_type": r["event_type"],
                "commit_hash": r["commit_hash"],
                "branch": r["branch"],
                "agent_id": r["agent_id"],
                "provider": r["provider"],
                "model": r["model"],
                "action_detail": json.loads(r["action_detail"]) if r["action_detail"] else {},
                "source_mode": r["source_mode"],
                "user_identity": r["user_identity"],
                "machine_id": r["machine_id"],
                "risk_level": r["risk_level"],
                "code_generated": bool(r["code_generated"]),
                "files_affected": json.loads(r["files_affected"]) if r["files_affected"] else [],
                "token_count": r["token_count"],
                "created_at": r["created_at"],
            }
            for r in rows
        ]

    def audit_summary(self) -> dict[str, Any]:
        """Return aggregate audit statistics."""
        total = self._conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
        if total == 0:
            return {"total_events": 0}

        by_type = self._conn.execute(
            "SELECT event_type, COUNT(*) as cnt FROM audit_log GROUP BY event_type ORDER BY cnt DESC"
        ).fetchall()
        by_risk = self._conn.execute(
            "SELECT risk_level, COUNT(*) as cnt FROM audit_log GROUP BY risk_level ORDER BY cnt DESC"
        ).fetchall()
        by_agent = self._conn.execute(
            "SELECT agent_id, COUNT(*) as cnt FROM audit_log GROUP BY agent_id ORDER BY cnt DESC"
        ).fetchall()
        by_provider = self._conn.execute(
            "SELECT provider, COUNT(*) as cnt FROM audit_log WHERE provider IS NOT NULL GROUP BY provider ORDER BY cnt DESC"
        ).fetchall()
        code_gen_count = self._conn.execute(
            "SELECT COUNT(*) FROM audit_log WHERE code_generated = 1"
        ).fetchone()[0]
        total_tokens = self._conn.execute(
            "SELECT COALESCE(SUM(token_count), 0) FROM audit_log"
        ).fetchone()[0]
        first_ts = self._conn.execute(
            "SELECT MIN(created_at) FROM audit_log"
        ).fetchone()[0]
        last_ts = self._conn.execute(
            "SELECT MAX(created_at) FROM audit_log"
        ).fetchone()[0]

        return {
            "total_events": total,
            "events_by_type": {r["event_type"]: r["cnt"] for r in by_type},
            "events_by_risk": {r["risk_level"]: r["cnt"] for r in by_risk},
            "events_by_agent": {r["agent_id"]: r["cnt"] for r in by_agent},
            "events_by_provider": {r["provider"]: r["cnt"] for r in by_provider},
            "code_generation_events": code_gen_count,
            "total_tokens_audited": total_tokens,
            "first_event": first_ts,
            "last_event": last_ts,
        }

    # -- Sync remotes ------------------------------------------------------

    def upsert_remote(
        self, name: str, remote_path: str, last_push: str | None = None,
        last_pull: str | None = None,
    ) -> None:
        """Create or update a sync remote."""
        now = time.time()
        existing = self._conn.execute(
            "SELECT * FROM sync_remotes WHERE name = ?", (name,)
        ).fetchone()
        if existing:
            updates = ["remote_path = ?", "last_sync_at = ?"]
            params: list[Any] = [remote_path, now]
            if last_push is not None:
                updates.append("last_push_hash = ?")
                params.append(last_push)
            if last_pull is not None:
                updates.append("last_pull_hash = ?")
                params.append(last_pull)
            params.append(name)
            self._conn.execute(
                f"UPDATE sync_remotes SET {', '.join(updates)} WHERE name = ?",
                params,
            )
        else:
            self._conn.execute(
                """INSERT INTO sync_remotes (name, remote_path, last_push_hash, last_pull_hash, last_sync_at, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (name, remote_path, last_push, last_pull, now, now),
            )
        self._conn.commit()

    def get_remote(self, name: str) -> dict[str, Any] | None:
        """Get a sync remote by name."""
        row = self._conn.execute(
            "SELECT * FROM sync_remotes WHERE name = ?", (name,)
        ).fetchone()
        if row is None:
            return None
        return {
            "name": row["name"],
            "remote_path": row["remote_path"],
            "last_push_hash": row["last_push_hash"],
            "last_pull_hash": row["last_pull_hash"],
            "last_sync_at": row["last_sync_at"],
            "created_at": row["created_at"],
        }

    def list_remotes(self) -> list[dict[str, Any]]:
        """List all configured sync remotes."""
        rows = self._conn.execute(
            "SELECT * FROM sync_remotes ORDER BY created_at"
        ).fetchall()
        return [
            {
                "name": r["name"],
                "remote_path": r["remote_path"],
                "last_push_hash": r["last_push_hash"],
                "last_pull_hash": r["last_pull_hash"],
                "last_sync_at": r["last_sync_at"],
                "created_at": r["created_at"],
            }
            for r in rows
        ]

    def get_raw_commit_row(self, commit_hash: str) -> dict[str, Any] | None:
        """Get the raw SQLite row for a commit (for sync transfer)."""
        row = self._conn.execute(
            "SELECT * FROM commits WHERE commit_hash = ?", (commit_hash,)
        ).fetchone()
        if row is None:
            return None
        return dict(row)

    # -- Agents (Hive Mind) ------------------------------------------------

    def insert_agent(
        self,
        agent_id: str,
        name: str | None = None,
        role: str | None = None,
        rank: str | None = None,
        squad: str | None = None,
        capabilities: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        readable_branches: list[str] | None = None,
        writable_branches: list[str] | None = None,
        status: str = "active",
    ) -> None:
        """Register a new agent (or update an existing one)."""
        now = time.time()
        self._conn.execute(
            """INSERT OR REPLACE INTO agents
               (agent_id, name, role, rank, squad, capabilities, metadata_json,
                readable_branches, writable_branches, status, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                agent_id,
                name or agent_id,
                role,
                rank,
                squad,
                json.dumps(capabilities or []),
                json.dumps(metadata or {}),
                json.dumps(readable_branches or []),
                json.dumps(writable_branches or []),
                status,
                now,
                now,
            ),
        )
        self._conn.commit()

    def get_agent(self, agent_id: str) -> dict[str, Any] | None:
        """Fetch an agent profile by ID."""
        row = self._conn.execute(
            "SELECT * FROM agents WHERE agent_id = ?", (agent_id,)
        ).fetchone()
        if row is None:
            return None
        return self._row_to_agent(row)

    def list_agents(
        self,
        squad: str | None = None,
        rank: str | None = None,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        """List agents, optionally filtered by squad, rank, or status."""
        conditions: list[str] = []
        params: list[Any] = []
        if squad:
            conditions.append("squad = ?")
            params.append(squad)
        if rank:
            conditions.append("rank = ?")
            params.append(rank)
        if status:
            conditions.append("status = ?")
            params.append(status)
        where = " AND ".join(conditions) if conditions else "1=1"
        rows = self._conn.execute(
            f"SELECT * FROM agents WHERE {where} ORDER BY created_at", params
        ).fetchall()
        return [self._row_to_agent(r) for r in rows]

    def update_agent(self, agent_id: str, **fields: Any) -> bool:
        """Update specific fields on an agent. Returns True if a row was updated."""
        allowed = {
            "name", "role", "rank", "squad", "capabilities", "metadata_json",
            "readable_branches", "writable_branches", "status",
        }
        updates: list[str] = []
        params: list[Any] = []
        for k, v in fields.items():
            if k not in allowed:
                continue
            if k in ("capabilities", "readable_branches", "writable_branches"):
                v = json.dumps(v)
            elif k == "metadata_json" and isinstance(v, dict):
                v = json.dumps(v)
            updates.append(f"{k} = ?")
            params.append(v)
        if not updates:
            return False
        updates.append("updated_at = ?")
        params.append(time.time())
        params.append(agent_id)
        cursor = self._conn.execute(
            f"UPDATE agents SET {', '.join(updates)} WHERE agent_id = ?", params
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def delete_agent(self, agent_id: str) -> bool:
        """Remove an agent from the registry. Returns True if deleted."""
        cursor = self._conn.execute(
            "DELETE FROM agents WHERE agent_id = ?", (agent_id,)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def list_commits_by_agent(
        self, agent_id: str, limit: int = 50
    ) -> list[CognitiveCommit]:
        """List commits created by a specific agent."""
        rows = self._conn.execute(
            """SELECT * FROM commits
               WHERE json_extract(metadata_json, '$.agent_id') = ?
               ORDER BY created_at DESC LIMIT ?""",
            (agent_id, limit),
        ).fetchall()
        return [self._row_to_commit(r) for r in rows]

    def list_commits_by_squad(
        self, squad: str, limit: int = 50
    ) -> list[CognitiveCommit]:
        """List commits from agents in a specific squad."""
        rows = self._conn.execute(
            """SELECT * FROM commits
               WHERE json_extract(metadata_json, '$.squad') = ?
               ORDER BY created_at DESC LIMIT ?""",
            (squad, limit),
        ).fetchall()
        return [self._row_to_commit(r) for r in rows]

    def list_commits_by_target(
        self, target_agent_id: str, limit: int = 50
    ) -> list[CognitiveCommit]:
        """List commits addressed to a specific agent."""
        rows = self._conn.execute(
            """SELECT * FROM commits
               WHERE json_extract(metadata_json, '$.target_agent_id') = ?
               ORDER BY created_at DESC LIMIT ?""",
            (target_agent_id, limit),
        ).fetchall()
        return [self._row_to_commit(r) for r in rows]

    @staticmethod
    def _row_to_agent(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "agent_id": row["agent_id"],
            "name": row["name"],
            "role": row["role"],
            "rank": row["rank"],
            "squad": row["squad"],
            "capabilities": json.loads(row["capabilities"]) if row["capabilities"] else [],
            "metadata": json.loads(row["metadata_json"]) if row["metadata_json"] else {},
            "readable_branches": json.loads(row["readable_branches"]) if row["readable_branches"] else [],
            "writable_branches": json.loads(row["writable_branches"]) if row["writable_branches"] else [],
            "status": row["status"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def close(self) -> None:
        self._conn.close()

    # -- COGNOME cache & state -------------------------------------------

    def cache_engram(
        self,
        engram_hash: str,
        query: str,
        preamble: str,
        source_commits: list[str],
        noeme_count: int,
        token_estimate: int,
        baseline_tokens: int,
        compression: float,
        budget_tokens: int,
        branch: str | None = None,
    ) -> None:
        """Persist a compiled Engram for reuse."""
        now = time.time()
        self._conn.execute(
            """INSERT OR REPLACE INTO cognome_cache
               (engram_hash, query, preamble, source_commits, noeme_count,
                token_estimate, baseline_tokens, compression, budget_tokens,
                branch, created_at, last_used_at, use_count)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                       COALESCE((SELECT use_count FROM cognome_cache WHERE engram_hash = ?), 0) + 1)
            """,
            (engram_hash, query, preamble, json.dumps(source_commits),
             noeme_count, token_estimate, baseline_tokens, compression,
             budget_tokens, branch, now, now, engram_hash),
        )
        self._conn.commit()

    def get_cached_engram(self, engram_hash: str) -> dict[str, Any] | None:
        """Retrieve a cached Engram by its hash."""
        row = self._conn.execute(
            "SELECT * FROM cognome_cache WHERE engram_hash = ?", (engram_hash,)
        ).fetchone()
        if row is None:
            return None
        # Touch last_used_at
        self._conn.execute(
            "UPDATE cognome_cache SET last_used_at = ?, use_count = use_count + 1 WHERE engram_hash = ?",
            (time.time(), engram_hash),
        )
        self._conn.commit()
        return dict(row)

    def list_cached_engrams(self, limit: int = 20) -> list[dict[str, Any]]:
        """Most recently used Engrams."""
        rows = self._conn.execute(
            "SELECT * FROM cognome_cache ORDER BY last_used_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

    def prune_engram_cache(self, max_age_seconds: float = 7 * 86400, max_entries: int = 200) -> int:
        """Evict stale or excess Engrams. Returns the count of deleted rows."""
        cutoff = time.time() - max_age_seconds
        c1 = self._conn.execute(
            "DELETE FROM cognome_cache WHERE last_used_at < ?", (cutoff,)
        ).rowcount
        # Keep only the most recent max_entries
        c2 = self._conn.execute(
            """DELETE FROM cognome_cache WHERE engram_hash NOT IN (
                SELECT engram_hash FROM cognome_cache ORDER BY last_used_at DESC LIMIT ?
            )""", (max_entries,)
        ).rowcount
        self._conn.commit()
        return c1 + c2

    def set_cognome_state(self, key: str, value: str) -> None:
        """Set a COGNOME state key (e.g. 'enabled', 'version', 'last_train_at')."""
        self._conn.execute(
            "INSERT OR REPLACE INTO cognome_state (key, value, updated_at) VALUES (?, ?, ?)",
            (key, value, time.time()),
        )
        self._conn.commit()

    def get_cognome_state(self, key: str) -> str | None:
        """Get a COGNOME state value by key."""
        row = self._conn.execute(
            "SELECT value FROM cognome_state WHERE key = ?", (key,)
        ).fetchone()
        return row["value"] if row else None

    def get_all_cognome_state(self) -> dict[str, str]:
        """Get all COGNOME state as a dict."""
        rows = self._conn.execute("SELECT key, value FROM cognome_state").fetchall()
        return {r["key"]: r["value"] for r in rows}


# ---------------------------------------------------------------------------
# Tier 2 — Content-Addressable Storage (CAS)
# ---------------------------------------------------------------------------

class BlobStore:
    """
    Git-style content-addressable blob store.

    Objects are stored as:  .cvc/objects/<hash[:2]>/<hash[2:]>
    All blobs are Zstandard-compressed before writing.
    """

    ZSTD_LEVEL = 6

    def __init__(self, objects_dir: Path) -> None:
        self._root = objects_dir
        self._root.mkdir(parents=True, exist_ok=True)
        self._cctx = zstd.ZstdCompressor(level=self.ZSTD_LEVEL)
        self._dctx = zstd.ZstdDecompressor()

    def _path_for(self, key: str) -> Path:
        return self._root / key[:2] / key[2:]

    def put(self, data: bytes) -> str:
        """Store raw bytes, returning the SHA-256 content address."""
        key = hashlib.sha256(data).hexdigest()
        path = self._path_for(key)
        if path.exists():
            return key  # Deduplication — already stored
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self._cctx.compress(data))
        return key

    def get(self, key: str) -> bytes | None:
        """Retrieve and decompress a blob by its SHA-256 key."""
        path = self._path_for(key)
        if not path.exists():
            return None
        return self._dctx.decompress(path.read_bytes())

    def exists(self, key: str) -> bool:
        return self._path_for(key).exists()

    def put_json(self, obj: Any) -> str:
        """Convenience: serialise a JSON-compatible object and store it."""
        raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)
        return self.put(raw.encode("utf-8"))

    def get_json(self, key: str) -> Any | None:
        data = self.get(key)
        if data is None:
            return None
        return json.loads(data.decode("utf-8"))

    def delete(self, key: str) -> bool:
        path = self._path_for(key)
        if path.exists():
            path.unlink()
            return True
        return False


# ---------------------------------------------------------------------------
# Tier 3 — Semantic Vector Store (REQUIRED)
# ---------------------------------------------------------------------------

class SemanticStore:
    """
    Chroma-backed vector store for commit-level semantic search.

    Tier 3 is a **required** component of the CVC Context Database —
    only Tier 4 (PageIndex) is optional.  If ChromaDB cannot be loaded
    or initialised, CVC raises immediately rather than degrading.

    Supports metadata-filtered vector search (Stage 2 of Staged Hybrid
    Filtering) — Chroma's native ``where`` clause pre-filters the HNSW
    index so only eligible documents are ranked.
    """

    def __init__(self, persist_dir: Path, enabled: bool = True) -> None:
        self._enabled = enabled
        self._collection = None
        self._persist_dir = persist_dir
        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Lazy-init ChromaDB on first actual use (import + PersistentClient)."""
        if self._initialized or not self._enabled:
            return
        self._initialized = True

        import chromadb  # type: ignore[import-untyped]  # Fatal if missing

        # Suppress ChromaDB's ONNX model download progress bar (tqdm)
        # on first run — it's a one-time download that confuses users.
        import io
        import sys
        _orig_stderr = sys.stderr
        sys.stderr = io.StringIO()
        try:
            client = chromadb.PersistentClient(path=str(self._persist_dir))
            self._collection = client.get_or_create_collection(
                name="cvc_commits",
                metadata={"hnsw:space": "cosine"},
            )
        finally:
            sys.stderr = _orig_stderr
        logger.info("Chroma vector store initialised at %s", self._persist_dir)

    @property
    def available(self) -> bool:
        if not self._enabled:
            return False
        if not self._initialized:
            self._ensure_initialized()
        return self._collection is not None

    def add(self, commit_hash: str, summary: str, metadata: dict[str, Any] | None = None) -> None:
        if not self.available:
            return
        assert self._collection is not None
        # Ensure all metadata values are Chroma-compatible (str, int, float, bool)
        safe_meta: dict[str, Any] = {}
        for k, v in (metadata or {}).items():
            if isinstance(v, (str, int, float, bool)):
                safe_meta[k] = v
            else:
                safe_meta[k] = str(v)
        self._collection.upsert(
            ids=[commit_hash],
            documents=[summary],
            metadatas=[safe_meta],
        )

    def search(self, query: str, n: int = 5) -> list[dict[str, Any]]:
        if not self.available:
            return []
        assert self._collection is not None
        results = self._collection.query(query_texts=[query], n_results=n)
        out: list[dict[str, Any]] = []
        for i, doc_id in enumerate(results["ids"][0]):
            out.append({
                "commit_hash": doc_id,
                "document": results["documents"][0][i] if results["documents"] else "",
                "distance": results["distances"][0][i] if results["distances"] else 0.0,
                "metadata": results["metadatas"][0][i] if results.get("metadatas") else {},
            })
        return out

    def search_filtered(
        self,
        query: str,
        n: int = 5,
        where: dict[str, Any] | None = None,
        where_document: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Metadata-filtered ANN vector search (Staged Hybrid Filtering — Stage 2).

        Parameters
        ----------
        query : str
            Natural language query for semantic ranking.
        n : int
            Max results to return.
        where : dict | None
            Chroma metadata filter, e.g.
            ``{"type": "checkpoint"}`` or
            ``{"$and": [{"ts": {"$gte": 1700000000}}, {"type": "analysis"}]}``.
        where_document : dict | None
            Chroma document content filter, e.g.
            ``{"$contains": "auth"}`` to require the word in summary text.

        Returns
        -------
        list[dict]
            Matching results with commit_hash, document, distance, metadata.
        """
        if not self.available:
            return []
        assert self._collection is not None

        kwargs: dict[str, Any] = {"query_texts": [query], "n_results": n}
        if where:
            kwargs["where"] = where
        if where_document:
            kwargs["where_document"] = where_document

        try:
            results = self._collection.query(**kwargs)
        except Exception as exc:
            logger.warning("Filtered vector search failed, falling back to unfiltered: %s", exc)
            results = self._collection.query(query_texts=[query], n_results=n)

        out: list[dict[str, Any]] = []
        for i, doc_id in enumerate(results["ids"][0]):
            out.append({
                "commit_hash": doc_id,
                "document": results["documents"][0][i] if results["documents"] else "",
                "distance": results["distances"][0][i] if results["distances"] else 0.0,
                "metadata": results["metadatas"][0][i] if results.get("metadatas") else {},
            })
        return out

    def count(self) -> int:
        """Return the number of documents in the collection."""
        if not self.available:
            return 0
        assert self._collection is not None
        return self._collection.count()


# ---------------------------------------------------------------------------
# Delta Compression Engine
# ---------------------------------------------------------------------------

class DeltaEngine:
    """
    Delta compression between context blobs using a simple binary diff.

    Implements the concept of VCDIFF / xdelta-style delta encoding described
    in the CVC paper.  For production deployments this should delegate to
    a compiled VCDIFF library; here we use Zstandard *dictionary* compression
    as an efficient, pure-Python-accessible approximation that achieves
    comparable compression ratios on sequential text data.
    """

    def __init__(self) -> None:
        self._cctx = zstd.ZstdCompressor(level=9)
        self._dctx = zstd.ZstdDecompressor()

    def compute_delta(self, anchor_data: bytes, target_data: bytes) -> bytes:
        """
        Compute a delta from *anchor_data* → *target_data*.

        Uses Zstandard dictionary compression: the anchor serves as the
        dictionary, and only the diff against it is stored.
        """
        dict_data = zstd.ZstdCompressionDict(anchor_data)
        cctx = zstd.ZstdCompressor(level=9, dict_data=dict_data)
        return cctx.compress(target_data)

    def apply_delta(self, anchor_data: bytes, delta: bytes) -> bytes:
        """Reconstruct *target_data* by applying *delta* on top of *anchor_data*."""
        dict_data = zstd.ZstdCompressionDict(anchor_data)
        dctx = zstd.ZstdDecompressor(dict_data=dict_data)
        return dctx.decompress(delta)


# ---------------------------------------------------------------------------
# Context Database — unified façade
# ---------------------------------------------------------------------------

class ContextDatabase:
    """
    Unified façade over all four tiers of the Context Database.

    Provides high-level methods used by the CVC operations layer
    (commit, branch, merge, restore).

    Tier 4 (PageIndex) is lazily initialised and used ONLY by the CLI agent.
    """

    def __init__(self, config: CVCConfig) -> None:
        config.ensure_dirs()
        self.config = config
        self.index = IndexDB(config.db_path)
        self.blobs = BlobStore(config.objects_dir)
        self.vectors = SemanticStore(config.chroma_persist_dir, config.vector_enabled)
        self.delta_engine = DeltaEngine()
        self._pageindex: Any = None  # Lazy — initialised on first access
        # === Phase B: blob LRU cache (Sofia, 2026-05-09) ===
        # Avoids re-decompressing the same ContentBlob on every recall scan.
        # Saves 500–800ms per `cvc recall` deep search; bounded memory.
        from collections import OrderedDict
        self._blob_cache: "OrderedDict[str, Any]" = OrderedDict()
        self._blob_cache_max = 256
        self._blob_cache_hits = 0
        self._blob_cache_misses = 0
        self._ensure_default_branch()

    def _blob_cache_get(self, key: str):
        v = self._blob_cache.get(key)
        if v is not None:
            self._blob_cache.move_to_end(key)
            self._blob_cache_hits += 1
        else:
            self._blob_cache_misses += 1
        return v

    def _blob_cache_put(self, key: str, value) -> None:
        if value is None:
            return
        self._blob_cache[key] = value
        self._blob_cache.move_to_end(key)
        if len(self._blob_cache) > self._blob_cache_max:
            self._blob_cache.popitem(last=False)

    def invalidate_blob_cache(self, commit_hash: str | None = None) -> None:
        if commit_hash is None:
            self._blob_cache.clear()
        else:
            self._blob_cache.pop(commit_hash, None)

    @property
    def pageindex(self) -> Any:
        """
        Lazy accessor for the Tier 4 PageIndex store.

        Returns a ``PageIndexStore`` instance, or ``None`` if the module
        cannot be imported (should never happen since it's bundled).
        The PageIndex is CLI-agent-only; proxy/MCP code never touches this.
        """
        if self._pageindex is None:
            try:
                from cvc.core.pageindex import PageIndexStore
                self._pageindex = PageIndexStore(self.config.pageindex_dir)
            except Exception as exc:
                logger.warning("PageIndex (Tier 4) failed to initialise: %s", exc)
                return None
        return self._pageindex

    # -- High-level operations ---------------------------------------------

    def store_commit(self, commit: CognitiveCommit) -> str:
        """
        Persist a CognitiveCommit across all three tiers.

        Handles delta compression: if the commit count since the last anchor
        exceeds ``config.anchor_interval``, a full anchor is stored instead.
        Commits explicitly typed as ANCHOR are always stored as full anchors.
        """
        raw_blob = commit.content_blob.canonical_bytes()

        # Respect explicitly-set ANCHOR type (e.g. from HiveCompactor)
        if commit.commit_type == CommitType.ANCHOR:
            blob_key = self.blobs.put(raw_blob)
            commit.is_delta = False
            commit.anchor_hash = None
        else:
            # Decide: anchor or delta?
            parent_count = 0
            if commit.parent_hashes:
                parent_count = self.index.count_commits_since_anchor(commit.parent_hashes[0])

            if parent_count >= self.config.anchor_interval or not commit.parent_hashes:
                # Store full anchor
                blob_key = self.blobs.put(raw_blob)
                commit.is_delta = False
                commit.anchor_hash = None
                if commit.commit_type != CommitType.MERGE:
                    commit.commit_type = CommitType.ANCHOR
            else:
                # Attempt delta against nearest anchor
                anchor_commit = self._find_nearest_anchor(commit.parent_hashes[0])
                if anchor_commit:
                    anchor_blob = self.blobs.get(self._get_blob_key(anchor_commit.commit_hash))
                    if anchor_blob is not None:
                        delta = self.delta_engine.compute_delta(anchor_blob, raw_blob)
                        blob_key = self.blobs.put(delta)
                        commit.is_delta = True
                        commit.anchor_hash = anchor_commit.commit_hash
                    else:
                        blob_key = self.blobs.put(raw_blob)
                else:
                    blob_key = self.blobs.put(raw_blob)

        # Compute Merkle hash *after* deciding delta/anchor
        commit.compute_hash()

        # Tier 1: Index
        self.index.insert_commit(commit, blob_key)

        # Tier 3: Vector — store enriched document for cognitive semantic search
        if self.vectors.available and commit.message:
            branch_name = ""
            try:
                for bp in self.index.list_branches():
                    if bp.head_hash == commit.commit_hash or (
                        commit.parent_hashes
                        and bp.head_hash in commit.parent_hashes
                    ):
                        branch_name = bp.name
                        break
            except Exception:
                pass

            # Build a richer document for vector search:
            # commit message + user queries + file manifest + distilled summary
            doc_parts = [commit.message]
            if commit.content_blob.distilled_summary:
                doc_parts.append(f"Distilled Context: {commit.content_blob.distilled_summary}")
            if commit.content_blob.query_history:
                queries = " | ".join(
                    q.get("content", "")[:200]
                    for q in commit.content_blob.query_history[:10]
                )
                doc_parts.append(f"Queries: {queries}")
            all_files = set(commit.content_blob.source_files.keys()) | set(commit.content_blob.files_written.keys())
            if all_files:
                doc_parts.append(f"Files: {', '.join(sorted(all_files)[:30])}")
            document_text = "\n".join(doc_parts)

            meta = commit.metadata
            self.vectors.add(
                commit.commit_hash,
                document_text,
                {
                    "type": commit.commit_type.value,
                    "ts": meta.timestamp,
                    "provider": meta.provider or "",
                    "model": meta.model or "",
                    "agent_id": meta.agent_id,
                    "branch": branch_name,
                    "token_count": commit.content_blob.token_count,
                    "is_delta": int(commit.is_delta),
                    "tags": ",".join(meta.tags) if meta.tags else "",
                    "session_id": meta.session_id or "",
                    "input_tokens": meta.input_tokens,
                    "output_tokens": meta.output_tokens,
                    "cost_usd": meta.cost_usd,
                    "turn_count": meta.turn_count,
                    "files_read_count": len(commit.content_blob.source_files),
                    "files_written_count": len(commit.content_blob.files_written),
                    # Hive Mind fields (Phase 2)
                    "squad": meta.squad or "",
                    "target_agent_id": meta.target_agent_id or "",
                    "rank": meta.rank or "",
                    "action_type": meta.action_type or "",
                },
            )

        logger.info(
            "Stored commit %s [%s] %s",
            commit.short_hash,
            "delta" if commit.is_delta else "full",
            commit.message[:80],
        )
        return commit.commit_hash

    def retrieve_blob(self, commit_hash: str) -> ContentBlob | None:
        """
        Fully reconstruct the ContentBlob for a commit, resolving deltas.
        Cached via LRU (size 256) — saves repeated decompress on recall scans.
        """
        cached = self._blob_cache_get(commit_hash)
        if cached is not None:
            return cached

        commit = self.index.get_commit(commit_hash)
        if commit is None:
            return None

        blob_key = self._get_blob_key(commit_hash)
        if blob_key is None:
            return None

        raw = self.blobs.get(blob_key)
        if raw is None:
            return None

        if commit.is_delta and commit.anchor_hash:
            anchor_blob_key = self._get_blob_key(commit.anchor_hash)
            if anchor_blob_key is None:
                logger.error("Anchor %s missing for delta commit %s", commit.anchor_hash, commit_hash)
                return None
            anchor_data = self.blobs.get(anchor_blob_key)
            if anchor_data is None:
                return None
            reconstructed = self.delta_engine.apply_delta(anchor_data, raw)
            result = ContentBlob.model_validate_json(reconstructed)
            self._blob_cache_put(commit_hash, result)
            return result

        result = ContentBlob.model_validate_json(raw)
        self._blob_cache_put(commit_hash, result)
        return result

    def search_similar(self, query: str, n: int = 5) -> list[dict]:
        """Semantic search over commit summaries."""
        return self.vectors.search(query, n)

    def search_conversations(
        self,
        query: str,
        limit: int = 10,
        deep: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Hybrid search across all conversations: semantic + text.

        Returns a list of dicts with keys:
          commit_hash, short_hash, message, timestamp, provider, model,
          relevance_source ('semantic' | 'message' | 'content'),
          distance (float, lower = more relevant),
          matching_messages (list of relevant messages from the blob).

        If *deep* is True, also searches inside content blobs for query terms.
        """
        results: dict[str, dict[str, Any]] = {}

        # 1. Semantic vector search (if available)
        if self.vectors.available:
            semantic_hits = self.vectors.search(query, n=limit)
            for hit in semantic_hits:
                ch = hit["commit_hash"]
                commit = self.index.get_commit(ch)
                if commit is None:
                    continue
                results[ch] = {
                    "commit_hash": ch,
                    "short_hash": ch[:12],
                    "message": commit.message,
                    "timestamp": commit.metadata.timestamp,
                    "provider": commit.metadata.provider or "",
                    "model": commit.metadata.model or "",
                    "commit_type": commit.commit_type.value,
                    "relevance_source": "semantic",
                    "distance": hit.get("distance", 0.0),
                    "matching_messages": [],
                }

        # 2. Text search on commit messages
        text_hits = self.index.search_commits(query, limit=limit * 2)
        for commit in text_hits:
            ch = commit.commit_hash
            if ch in results:
                continue  # Already found via semantic
            results[ch] = {
                "commit_hash": ch,
                "short_hash": ch[:12],
                "message": commit.message,
                "timestamp": commit.metadata.timestamp,
                "provider": commit.metadata.provider or "",
                "model": commit.metadata.model or "",
                "commit_type": commit.commit_type.value,
                "relevance_source": "message",
                "distance": 0.5,  # Mid-range score for text matches
                "matching_messages": [],
            }

        # 3. Deep content search — scan blob content for query terms
        if deep:
            query_lower = query.lower()
            query_terms = query_lower.split()
            all_commits = self.index.list_all_commits(limit=500)
            for commit in all_commits:
                ch = commit.commit_hash
                if ch in results:
                    # Already have this commit, but enrich with content matches
                    pass
                # Try to get the blob and search through messages
                try:
                    blob = self.retrieve_blob(ch)
                    if blob is None:
                        continue
                    matching_msgs = []
                    for msg in blob.messages:
                        content_lower = msg.content.lower()
                        if any(term in content_lower for term in query_terms):
                            matching_msgs.append({
                                "role": msg.role,
                                "content": msg.content[:500],
                                "timestamp": msg.timestamp,
                            })
                    if matching_msgs:
                        if ch not in results:
                            results[ch] = {
                                "commit_hash": ch,
                                "short_hash": ch[:12],
                                "message": commit.message,
                                "timestamp": commit.metadata.timestamp,
                                "provider": commit.metadata.provider or "",
                                "model": commit.metadata.model or "",
                                "commit_type": commit.commit_type.value,
                                "relevance_source": "content",
                                "distance": 0.7,
                                "matching_messages": matching_msgs[:5],
                            }
                        else:
                            results[ch]["matching_messages"] = matching_msgs[:5]
                except Exception:
                    continue

        # Sort by distance (lower = more relevant), then by timestamp (newer first)
        sorted_results = sorted(
            results.values(),
            key=lambda r: (r["distance"], -r["timestamp"]),
        )
        return sorted_results[:limit]

    # -- Staged Hybrid Filtering (CLI agent only) --------------------------

    def staged_hybrid_search(
        self,
        query: str,
        limit: int = 10,
        *,
        # Stage 1 — Pre-filters (high selectivity, indexed)
        branch: str | None = None,
        commit_type: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        since: float | None = None,
        until: float | None = None,
        tags: list[str] | None = None,
        # Stage 3 — Post-filters (lightweight refinement)
        min_token_count: int | None = None,
        max_token_count: int | None = None,
        contains_keyword: str | None = None,
        deep: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Staged Hybrid Filtering — production-grade RAG search.

        This three-stage pipeline ensures only eligible documents are
        considered, dramatically improving precision and reducing
        context window waste.

        Stage 1: Pre-filter (indexed metadata, high selectivity)
            Filter by branch, commit_type, date_range, provider, model, tags.
            Reduces candidate set before any ANN search.
            1M docs → 100K (minimal latency impact, major precision gain).

        Stage 2: ANN Vector Search (semantic ranking on filtered subset)
            Run Chroma's HNSW cosine search ONLY on the pre-filtered
            candidates. If Chroma is unavailable, falls back to SQLite
            text search with relevance scoring.

        Stage 3: Post-filter (non-indexed attributes, lightweight cleanup)
            Refine with token_count range, keyword containment in blob
            content. Not heavy lifting — just cleanup.

        Returns the same result format as ``search_conversations`` for
        API compatibility.
        """
        results: dict[str, dict[str, Any]] = {}

        # ── Stage 1: Pre-filter via SQLite metadata ──────────────────────
        # Build a set of eligible commit hashes BEFORE touching vectors.
        # This is the key insight: filter first, search second.
        eligible_hashes: set[str] | None = None  # None = no pre-filter → all eligible

        stage1_conditions: list[str] = []
        stage1_params: list[Any] = []

        if commit_type:
            stage1_conditions.append("commit_type = ?")
            stage1_params.append(commit_type)
        if since is not None:
            stage1_conditions.append("created_at >= ?")
            stage1_params.append(since)
        if until is not None:
            stage1_conditions.append("created_at <= ?")
            stage1_params.append(until)

        if stage1_conditions:
            where_clause = " AND ".join(stage1_conditions)
            rows = self.index._conn.execute(
                f"SELECT commit_hash FROM commits WHERE {where_clause} "
                "ORDER BY created_at DESC LIMIT 2000",
                stage1_params,
            ).fetchall()
            eligible_hashes = {r["commit_hash"] for r in rows}

        # Branch filter: resolve to commit hashes on that branch
        if branch:
            branch_commits = set()
            bp = self.index.get_branch(branch)
            if bp:
                ancestors = self.index.get_ancestors(bp.head_hash, limit=2000)
                branch_commits = {a.commit_hash for a in ancestors}
            if eligible_hashes is not None:
                eligible_hashes &= branch_commits
            else:
                eligible_hashes = branch_commits

        # Tag filter: search metadata_json for tag strings
        if tags:
            tag_hashes = set()
            for tag in tags:
                tag_rows = self.index._conn.execute(
                    "SELECT commit_hash FROM commits WHERE metadata_json LIKE ?",
                    (f"%{tag}%",),
                ).fetchall()
                tag_hashes.update(r["commit_hash"] for r in tag_rows)
            if eligible_hashes is not None:
                eligible_hashes &= tag_hashes
            else:
                eligible_hashes = tag_hashes

        # Early exit: pre-filter eliminated everything
        if eligible_hashes is not None and not eligible_hashes:
            logger.info("Staged hybrid search: Stage 1 pre-filter eliminated all candidates")
            return []

        selectivity = (
            len(eligible_hashes) / max(self.vectors.count(), 1)
            if eligible_hashes is not None and self.vectors.available
            else 1.0
        )
        logger.info(
            "Staged hybrid search: Stage 1 passed %s candidates (selectivity: %.1f%%)",
            len(eligible_hashes) if eligible_hashes is not None else "all",
            selectivity * 100,
        )

        # ── Stage 2: ANN Vector Search on filtered subset ────────────────
        # Build Chroma where-clause from pre-filter metadata
        chroma_where: dict[str, Any] | None = None
        chroma_filters: list[dict[str, Any]] = []

        if provider:
            chroma_filters.append({"provider": provider})
        if model:
            chroma_filters.append({"model": model})
        if commit_type:
            chroma_filters.append({"type": commit_type})
        if since is not None:
            chroma_filters.append({"ts": {"$gte": since}})
        if until is not None:
            chroma_filters.append({"ts": {"$lte": until}})

        if len(chroma_filters) == 1:
            chroma_where = chroma_filters[0]
        elif len(chroma_filters) > 1:
            chroma_where = {"$and": chroma_filters}

        if self.vectors.available:
            # Use filtered ANN search — Chroma pre-filters HNSW index
            semantic_hits = self.vectors.search_filtered(
                query,
                n=min(limit * 3, 50),  # Over-fetch for post-filter headroom
                where=chroma_where,
            )
            for hit in semantic_hits:
                ch = hit["commit_hash"]
                # Respect Stage 1 pre-filter (branch/tag filters not in Chroma)
                if eligible_hashes is not None and ch not in eligible_hashes:
                    continue
                commit = self.index.get_commit(ch)
                if commit is None:
                    continue
                results[ch] = {
                    "commit_hash": ch,
                    "short_hash": ch[:12],
                    "message": commit.message,
                    "timestamp": commit.metadata.timestamp,
                    "provider": commit.metadata.provider or "",
                    "model": commit.metadata.model or "",
                    "commit_type": commit.commit_type.value,
                    "relevance_source": "semantic+filtered",
                    "distance": hit.get("distance", 0.0),
                    "matching_messages": [],
                    "search_stage": "stage2_ann",
                }
        else:
            # Fallback: SQLite text search within pre-filtered set
            text_hits = self.index.search_commits(query, limit=limit * 3)
            for commit in text_hits:
                ch = commit.commit_hash
                if eligible_hashes is not None and ch not in eligible_hashes:
                    continue
                results[ch] = {
                    "commit_hash": ch,
                    "short_hash": ch[:12],
                    "message": commit.message,
                    "timestamp": commit.metadata.timestamp,
                    "provider": commit.metadata.provider or "",
                    "model": commit.metadata.model or "",
                    "commit_type": commit.commit_type.value,
                    "relevance_source": "text+filtered",
                    "distance": 0.5,
                    "matching_messages": [],
                    "search_stage": "stage2_text_fallback",
                }

        # Also add text matches not covered by vector search
        text_hits = self.index.search_commits(query, limit=limit * 2)
        for commit in text_hits:
            ch = commit.commit_hash
            if ch in results:
                continue
            if eligible_hashes is not None and ch not in eligible_hashes:
                continue
            results[ch] = {
                "commit_hash": ch,
                "short_hash": ch[:12],
                "message": commit.message,
                "timestamp": commit.metadata.timestamp,
                "provider": commit.metadata.provider or "",
                "model": commit.metadata.model or "",
                "commit_type": commit.commit_type.value,
                "relevance_source": "message",
                "distance": 0.5,
                "matching_messages": [],
                "search_stage": "stage2_text",
            }

        # ── Stage 3: Post-filter (lightweight refinement) ────────────────
        to_remove: list[str] = []

        for ch, entry in results.items():
            # Token count range filter
            commit = self.index.get_commit(ch)
            if commit and (min_token_count is not None or max_token_count is not None):
                blob = self.retrieve_blob(ch)
                if blob:
                    tc = blob.token_count
                    if min_token_count is not None and tc < min_token_count:
                        to_remove.append(ch)
                        continue
                    if max_token_count is not None and tc > max_token_count:
                        to_remove.append(ch)
                        continue

            # Keyword containment check in blob content
            if contains_keyword:
                blob = self.retrieve_blob(ch) if ch not in to_remove else None
                if blob:
                    blob_text = " ".join(m.content for m in blob.messages).lower()
                    if contains_keyword.lower() not in blob_text:
                        to_remove.append(ch)
                        continue

        for ch in to_remove:
            results.pop(ch, None)

        # Deep content search — enrich results with matching message snippets
        if deep:
            query_lower = query.lower()
            query_terms = query_lower.split()

            # Only scan commits in the eligible set (not all 500)
            scan_hashes: set[str]
            if eligible_hashes is not None:
                scan_hashes = eligible_hashes
            else:
                scan_hashes = {
                    c.commit_hash
                    for c in self.index.list_all_commits(limit=500)
                }

            for ch in scan_hashes:
                try:
                    blob = self.retrieve_blob(ch)
                    if blob is None:
                        continue
                    matching_msgs = []
                    for msg in blob.messages:
                        content_lower = msg.content.lower()
                        if any(term in content_lower for term in query_terms):
                            matching_msgs.append({
                                "role": msg.role,
                                "content": msg.content[:500],
                                "timestamp": msg.timestamp,
                            })
                    if matching_msgs:
                        if ch in results:
                            results[ch]["matching_messages"] = matching_msgs[:5]
                        else:
                            commit = self.index.get_commit(ch)
                            if commit:
                                results[ch] = {
                                    "commit_hash": ch,
                                    "short_hash": ch[:12],
                                    "message": commit.message,
                                    "timestamp": commit.metadata.timestamp,
                                    "provider": commit.metadata.provider or "",
                                    "model": commit.metadata.model or "",
                                    "commit_type": commit.commit_type.value,
                                    "relevance_source": "content",
                                    "distance": 0.7,
                                    "matching_messages": matching_msgs[:5],
                                    "search_stage": "stage3_deep",
                                }
                except Exception:
                    continue

        # Final sort: distance (lower = more relevant), then timestamp (newer first)
        sorted_results = sorted(
            results.values(),
            key=lambda r: (r["distance"], -r["timestamp"]),
        )

        logger.info(
            "Staged hybrid search complete: %d results from %d candidates "
            "(stages: pre-filter → ANN → post-filter)",
            min(len(sorted_results), limit),
            len(eligible_hashes) if eligible_hashes is not None else -1,
        )
        return sorted_results[:limit]

    # -- Internal helpers --------------------------------------------------

    def _get_blob_key(self, commit_hash: str) -> str | None:
        row = self.index._conn.execute(
            "SELECT blob_key FROM commits WHERE commit_hash = ?", (commit_hash,)
        ).fetchone()
        if row is None:
            # prefix match
            row = self.index._conn.execute(
                "SELECT blob_key FROM commits WHERE commit_hash LIKE ? LIMIT 1",
                (f"{commit_hash}%",),
            ).fetchone()
        return row["blob_key"] if row else None

    def _find_nearest_anchor(self, commit_hash: str) -> CognitiveCommit | None:
        """Walk the parent chain to find the nearest non-delta commit."""
        h: str | None = commit_hash
        while h:
            c = self.index.get_commit(h)
            if c is None:
                return None
            if not c.is_delta:
                return c
            h = c.parent_hashes[0] if c.parent_hashes else None
        return None

    def _ensure_default_branch(self) -> None:
        if self.index.get_branch(self.config.default_branch) is None:
            # Create a genesis commit
            genesis = CognitiveCommit(
                commit_type=CommitType.ANCHOR,
                message="Genesis — CVC initialised",
                metadata=CommitMetadata(
                    agent_id=self.config.agent_id,
                    mode=self.config.mode,
                ),
            )
            genesis.compute_hash()
            blob_key = self.blobs.put(genesis.content_blob.canonical_bytes())
            self.index.insert_commit(genesis, blob_key)
            self.index.upsert_branch(
                BranchPointer(
                    name=self.config.default_branch,
                    head_hash=genesis.commit_hash,
                    description="Default branch",
                )
            )
            logger.info("Created default branch '%s' with genesis commit", self.config.default_branch)

    def close(self) -> None:
        self.index.close()
