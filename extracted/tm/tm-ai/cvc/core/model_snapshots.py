"""
cvc.core.model_snapshots — Append-only user model snapshot history.

Per CVC_FOUNDATION.md H1 (Time Machine UX) and H3 (Brain-portable
identity), the soul must be re-instantiable at any prior moment. The
single user_model.json file doesn't allow this — the past is overwritten
on every save.

This module maintains an append-only snapshot store:

    ~/.cvc/user_model_snapshots/<snapshot_id>.json

Every call to ``save_model()`` writes both the canonical file AND a
timestamped snapshot. Snapshots are NEVER deleted (per the append-only
invariant). The newest snapshot at-or-before any timestamp IS the
historical state at that moment.

This is intentionally a DAG too: every snapshot references its
predecessor's snapshot_id, so a future "soul history browser" can walk
the chain linearly without scanning the filesystem.

File format (per snapshot):

    {
      "snapshot_id": "abc123",
      "timestamp": 1782721755.57,
      "parent_snapshot_id": "def456" | null,
      "model": { ... UserIdentitySnapshot JSON ... },
      "commit_hash": "..." | null,        # cognitive commit that triggered the save
      "trigger": "manual" | "auto" | "post_session" | "correction",
      "size_bytes": 4321
    }

Usage:
    from cvc.core.model_snapshots import SnapshotStore
    store = SnapshotStore(cvc_root)
    store.append(model, trigger="post_session", commit_hash="...")
    history = store.list(limit=20)
    historical = store.reconstruct_at(timestamp=1234567890.0)
"""
from __future__ import annotations

import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any, Literal

logger = logging.getLogger("cvc.model_snapshots")

SNAPSHOT_DIR = "user_model_snapshots"
SNAPSHOT_INDEX = "user_model_snapshots_index.json"

Trigger = Literal["manual", "auto", "post_session", "correction", "preservation_freeze", "import", "per_turn_auto", "per_turn_cleanup", "manual_refresh", "day_canonical"]


class SnapshotStore:
    """Append-only user model snapshot history.

    Maintains a directory of timestamped JSON snapshots PLUS a
    lightweight index for fast listing (without scanning every file).
    Both grow monotonically — old data is never modified or removed.
    """

    def __init__(self, cvc_root: Path) -> None:
        self.cvc_root = Path(cvc_root)
        self._dir = self.cvc_root / SNAPSHOT_DIR
        self._dir.mkdir(parents=True, exist_ok=True)
        self._index_path = self._dir / SNAPSHOT_INDEX
        if not self._index_path.exists():
            self._write_index({"snapshots": [], "schema_version": 1})

    # ── Write path ────────────────────────────────────────────────────────

    def append(
        self,
        model: Any,  # UserIdentitySnapshot; avoid import cycle
        trigger: Trigger = "manual",
        commit_hash: str | None = None,
        snapshot_id: str | None = None,
        **metadata: Any,
    ) -> str:
        """Persist a new snapshot. Returns the snapshot_id.

        v3.5.1 — ``**metadata`` lets callers attach extra fields
        (e.g. ``scope="day"``, ``consolidated_from=[...]``) without
        changing the signature. Stored on the index entry only —
        model JSON stays canonical.
        """
        sid = snapshot_id or uuid.uuid4().hex[:16]
        ts = time.time()
        parent = self._last_snapshot_id()

        model_json = model.model_dump_json(indent=2) if hasattr(model, "model_dump_json") else json.dumps(model)
        size = len(model_json)

        snapshot = {
            "snapshot_id": sid,
            "timestamp": ts,
            "parent_snapshot_id": parent,
            "trigger": trigger,
            "commit_hash": commit_hash,
            "model": json.loads(model_json),
            "size_bytes": size,
            **({"metadata": dict(metadata)} if metadata else {}),
        }
        # Append-only: write the file AND extend the index
        (self._dir / f"{sid}.json").write_text(
            json.dumps(snapshot, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        idx = self._read_index()
        idx_entry = {
            "snapshot_id": sid,
            "timestamp": ts,
            "trigger": trigger,
            "commit_hash": commit_hash,
            "size_bytes": size,
        }
        if metadata:
            idx_entry["metadata"] = dict(metadata)
        idx["snapshots"].append(idx_entry)
        self._write_index(idx)
        logger.debug("snapshot %s appended (%s, %d bytes)", sid, trigger, size)
        return sid

    # ── Read path ─────────────────────────────────────────────────────────

    def list(self, limit: int = 50, trigger: Trigger | None = None) -> list[dict[str, Any]]:
        """Return most-recent snapshots, optionally filtered by trigger."""
        idx = self._read_index()
        snaps = idx.get("snapshots", [])
        if trigger:
            snaps = [s for s in snaps if s.get("trigger") == trigger]
        return list(reversed(snaps[-limit:]))

    def list_by_date(self, date_iso: str) -> list[dict[str, Any]]:
        """Return full snapshots (with model JSON) for a YYYY-MM-DD date.

        v3.5.1 — TIME PORTAL day-scope support. Includes the index
        entry plus the full model payload (via ``get``) so callers
        don't have to do a second roundtrip per snapshot. Sorted
        oldest → newest.
        """
        snaps: list[dict[str, Any]] = []
        for entry in self._read_index().get("snapshots", []):
            ts = entry.get("timestamp", 0)
            if not ts:
                continue
            local = time.localtime(ts)
            stamp = time.strftime("%Y-%m-%d", local)
            if stamp == date_iso:
                full = self.get(entry["snapshot_id"])
                if full:
                    snaps.append(full)
        snaps.sort(key=lambda s: s.get("timestamp", 0))
        return snaps

    def list_day_index(self) -> list[dict[str, Any]]:
        """Return one entry per day with snapshot count + first/last timestamp.

        Used by the Time Portal UI to render the day-row accordion.
        Sorted newest day first. Includes raw snapshot count BEFORE
        day consolidation so the UI can show "47 raw → 1 consolidated".
        """
        idx = self._read_index().get("snapshots", [])
        by_day: dict[str, dict[str, Any]] = {}
        for s in idx:
            ts = s.get("timestamp", 0)
            if not ts:
                continue
            date = time.strftime("%Y-%m-%d", time.localtime(ts))
            entry = by_day.setdefault(date, {
                "date": date,
                "snapshot_count": 0,
                "first_ts": ts,
                "last_ts": ts,
                "first_id": s.get("snapshot_id"),
                "last_id": s.get("snapshot_id"),
            })
            entry["snapshot_count"] += 1
            if ts < entry["first_ts"]:
                entry["first_ts"] = ts
                entry["first_id"] = s.get("snapshot_id")
            if ts > entry["last_ts"]:
                entry["last_ts"] = ts
                entry["last_id"] = s.get("snapshot_id")
        return sorted(by_day.values(), key=lambda d: d["date"], reverse=True)

    def get(self, snapshot_id: str) -> dict[str, Any] | None:
        """Load a full snapshot by id (includes the model JSON)."""
        path = self._dir / f"{snapshot_id}.json"
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            logger.warning("snapshot %s unreadable: %s", snapshot_id, e)
            return None

    def reconstruct_at(self, timestamp: float) -> dict[str, Any] | None:
        """Return the latest snapshot at or before the given timestamp.

        This is the core "time machine" primitive: given any past
        timestamp, return the soul state AS OF that moment. Returns
        None if no snapshot exists before that time.
        """
        idx = self._read_index()
        candidates = [s for s in idx.get("snapshots", []) if s.get("timestamp", 0) <= timestamp]
        if not candidates:
            return None
        # Latest one
        latest = max(candidates, key=lambda s: s["timestamp"])
        return self.get(latest["snapshot_id"])

    def stats(self) -> dict[str, Any]:
        idx = self._read_index()
        snaps = idx.get("snapshots", [])
        return {
            "total": len(snaps),
            "oldest": snaps[0]["timestamp"] if snaps else None,
            "newest": snaps[-1]["timestamp"] if snaps else None,
            "by_trigger": {
                t: sum(1 for s in snaps if s.get("trigger") == t)
                for t in {s.get("trigger") for s in snaps}
            },
            "total_size_bytes": sum(s.get("size_bytes", 0) for s in snaps),
        }

    # ── Internals ─────────────────────────────────────────────────────────

    def _last_snapshot_id(self) -> str | None:
        idx = self._read_index()
        snaps = idx.get("snapshots", [])
        return snaps[-1]["snapshot_id"] if snaps else None

    def _read_index(self) -> dict[str, Any]:
        try:
            return json.loads(self._index_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"snapshots": [], "schema_version": 1}

    def _write_index(self, data: dict[str, Any]) -> None:
        # Atomic-ish: write to temp, rename
        tmp = self._index_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(self._index_path)