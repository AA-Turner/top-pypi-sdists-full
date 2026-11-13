"""Mirror complete discovery catalogs; keep historical evidence out of membership."""
from __future__ import annotations

import hashlib
import json
import logging

log = logging.getLogger(__name__)


def replace(conn, source, rows):
    """Replace one successful source snapshot in the caller's transaction.

    Empty is authoritative; an unavailable source must not call this function.
    Membership never establishes physical ownership or permission to route.
    """
    if not isinstance(rows, list):
        raise ValueError("catalog snapshot must be a list")
    entries = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("invalid catalog row")
        key = row.get("id") or row.get("key")
        if not isinstance(key, str) or not key:
            raise ValueError("catalog row requires a model key")
        from .census import is_staging
        if is_staging(key, row):
            continue
        marker = row.get("hugpy_json")
        metadata = {**(marker if isinstance(marker, dict) else {}), **row}
        tasks = metadata.get("tasks") or []
        primary = metadata.get("primary_task")
        metadata["tasks"] = list(dict.fromkeys([*(tasks if isinstance(tasks, list) else []),
                                                *([primary] if primary else [])]))
        entries[key] = metadata
    fingerprint = hashlib.sha256(json.dumps(entries, sort_keys=True, default=str).encode()).hexdigest()
    conn.execute("INSERT INTO model_catalog_sources(source,fingerprint) VALUES (%s,'') "
                 "ON CONFLICT(source) DO NOTHING", (source,))
    previous = conn.execute("SELECT fingerprint FROM model_catalog_sources WHERE source=%s FOR UPDATE",
                            (source,)).fetchone()
    if (previous.get("fingerprint") if isinstance(previous, dict) else previous[0]) == fingerprint:
        return False
    for key, metadata in sorted(entries.items()):
        conn.execute(
            "INSERT INTO model_census(model_key,hub_id,framework,primary_task,metadata) "
            "VALUES (%s,%s,%s,%s,%s::jsonb) ON CONFLICT(model_key) DO UPDATE SET "
            "hub_id=coalesce(EXCLUDED.hub_id,model_census.hub_id), "
            "framework=coalesce(EXCLUDED.framework,model_census.framework), "
            "primary_task=coalesce(EXCLUDED.primary_task,model_census.primary_task), "
            "metadata=model_census.metadata || EXCLUDED.metadata,updated_at=now()",
            (key, metadata.get("hub_id"), metadata.get("framework"),
             metadata.get("primary_task"), json.dumps(metadata)))
    conn.execute("DELETE FROM model_catalog_entries WHERE source=%s", (source,))
    if entries:
        with conn.cursor() as cursor:
            cursor.executemany("INSERT INTO model_catalog_entries(source,model_key) VALUES (%s,%s)",
                               [(source, key) for key in sorted(entries)])
    conn.execute("UPDATE model_catalog_sources SET fingerprint=%s,observed_at=now() WHERE source=%s",
                 (fingerprint, source))
    return True


def refresh_local():
    """Publish the local wrapper/discovery snapshot, retaining it on read failure."""
    from . import catalog_live
    from hugpy_core.intake.store import store
    try:
        rows = catalog_live.catalog_index()["data"]
        with store().connect() as conn:
            replace(conn, "discovery:local", rows)
    except Exception:
        log.exception("Could not refresh discovery catalog; retaining previous snapshot")
