"""One Core-owned index of model identity and reported physical copies.

Reports are evidence, not permission to delete or transfer bytes. The source
must prove its copy again when a destructive or byte-moving operation runs.
"""
from __future__ import annotations

import json
import logging
import time

from hugpy_core.imports import functions as _F

logger = logging.getLogger("hugpy_core.models.census")


def observe_worker(worker: dict, conn=None) -> None:
    """Replace this worker's copy reports, using the caller's transaction when given."""
    catalog = worker.get('catalog')
    if isinstance(catalog, list):
        if conn is None:
            import psycopg
            with psycopg.connect(_F.core_dsn(), connect_timeout=3) as owned_conn:
                observe_worker(worker, conn=owned_conn)
            return
        from .current_catalog import replace
        replace(conn, "worker:" + str(worker["id"]), catalog)
        for item in sorted(catalog, key=lambda row: str(row.get('id', ''))):
            key = item.get('id')
            if not key or is_staging(key, item):
                continue
            # A published catalog establishes identity, never a physical copy.
            conn.execute(
                "INSERT INTO model_census(model_key,hub_id,framework,primary_task,metadata) "
                "VALUES (%s,%s,%s,%s,%s::jsonb) ON CONFLICT(model_key) DO UPDATE SET "
                "framework=coalesce(EXCLUDED.framework,model_census.framework), "
                "primary_task=coalesce(EXCLUDED.primary_task,model_census.primary_task),updated_at=now()",
                (key, item.get('hub_id'), item.get('framework'), item.get('primary_task'), json.dumps(item)))
    discovered = worker.get("models_discovered")
    if not isinstance(discovered, dict):
        return  # Older beats supply no complete snapshot; unknown is not absent.
    # Central is a storage role, not a transfer of physical ownership to core.
    # Keep these observations in the worker namespace; details retain the role.
    discovered = {**(worker.get("models_central") or {}), **discovered}
    wid = str(worker.get("id") or "")
    if not wid:
        return
    if conn is None:
        import psycopg
        with psycopg.connect(_F.core_dsn(), connect_timeout=3) as owned_conn:
            _write_observation(owned_conn, wid, discovered)
    else:
        _write_observation(conn, wid, discovered)


try:  # the downloader's own staging term: `<dest>.tmp-<pid>` while a download is in flight
    from hugpy_storage.transfer.downloads import _STAGING_SUFFIX_RE as _STAGING_RE
except Exception:  # noqa: BLE001 — same pattern, kept in step with hugpy_storage.transfer.downloads
    import re as _re
    _STAGING_RE = _re.compile(r"\.tmp-(\d+)$")


def is_staging(key, item=None) -> bool:
    """A download-staging directory (`<dest>.tmp-<pid>`) is not a model: once the
    download finishes it is renamed to <dest>, so a census row keyed on it would
    outlive the directory and echo back through presence/aliases."""
    if isinstance(key, str) and _STAGING_RE.search(key):
        return True
    # Only the directory itself counts: a model served from inside a staging
    # parent (e.g. <repo>.tmp-<pid>/<quant>) is a real, currently served model.
    value = item.get("model_dir") if isinstance(item, dict) else None
    if isinstance(value, str) and _STAGING_RE.search(value.rstrip("/").rsplit("/", 1)[-1]):
        return True
    return False


def _write_observation(conn, wid: str, discovered: dict) -> None:
    from .current_catalog import replace
    replace(conn, "worker:" + wid, [{**item, "id": key} for key, item in discovered.items()])
    # Download-staging dirs never become census keys, copies or aliases.
    discovered = {k: v for k, v in discovered.items() if not is_staging(k, v)}
    # All workers report overlapping models. Keep a consistent lock order
    # across their transactions so concurrent heartbeats cannot deadlock
    # while upserting the same census keys in different discovery orders.
    for key, item in sorted(discovered.items(), key=lambda pair: str(pair[0])):
        if not isinstance(key, str) or not key or not isinstance(item, dict):
            continue
        item = {**item, "owner_worker": wid, "source_protocol": "wrapper"}
        marker = item.get("hugpy_json") or {}
        marker = marker if isinstance(marker, dict) else {}
        tasks = marker.get("tasks") or []
        task = marker.get("primary_task") or (tasks[0] if isinstance(tasks, list) and tasks else None)
        conn.execute(
            "INSERT INTO model_census (model_key, hub_id, framework, primary_task, metadata) "
            "VALUES (%s,%s,%s,%s,%s::jsonb) ON CONFLICT (model_key) DO UPDATE SET "
            "hub_id=coalesce(EXCLUDED.hub_id,model_census.hub_id), "
            "framework=coalesce(EXCLUDED.framework,model_census.framework), "
            "primary_task=coalesce(EXCLUDED.primary_task,model_census.primary_task), "
            "updated_at=now()",
            (key, marker.get("hub_id"), marker.get("framework"), task, json.dumps(marker)))
        conn.execute(
            "INSERT INTO model_copies (model_key,location_kind,location_id,path,bytes,details,present,verified,observed_at) "
            "VALUES (%s,'worker',%s,%s,%s,%s::jsonb,true,false,now()) "
            "ON CONFLICT (model_key,location_kind,location_id) DO UPDATE SET "
            "path=EXCLUDED.path,bytes=EXCLUDED.bytes,details=EXCLUDED.details,"
            "present=true,verified=false,observed_at=now()",
            (key, wid, item.get("path"), item.get("bytes"), json.dumps(item)))
    # Only unambiguous, explicit discovery aliases become redirects. Never
    # override a real catalog key or an alias already pointing elsewhere.
    conn.execute("""INSERT INTO model_key_aliases(alias_key,model_key,evidence)
        SELECT h.handle,min(c.model_key),jsonb_build_object('source','discovery.identity.handles')
        FROM model_copies c CROSS JOIN LATERAL
          jsonb_array_elements_text(coalesce(c.details->'identity'->'handles','[]'::jsonb)) h(handle)
        WHERE c.present AND h.handle<>c.model_key AND NOT EXISTS
          (SELECT 1 FROM model_dossier_raw_keys k WHERE k.model_key=h.handle)
        GROUP BY h.handle HAVING count(DISTINCT c.model_key)=1
        ON CONFLICT(alias_key) DO NOTHING""")
    conn.execute(
        "UPDATE model_copies SET present=false,verified=false,observed_at=now() "
        "WHERE location_kind='worker' AND location_id=%s AND present "
        "AND NOT (model_key = ANY(%s))", (wid, sorted(discovered)))


def try_observe_worker(worker: dict) -> None:
    import psycopg
    for attempt in range(3):
        try:
            observe_worker(worker)
            return
        except (psycopg.errors.DeadlockDetected, psycopg.errors.SerializationFailure):
            if attempt == 2:
                logger.exception("worker census update failed after retries for %s", worker.get("id"))
                return
            time.sleep(0.05 * (attempt + 1))
        except Exception:
            logger.exception("worker census update failed for %s", worker.get("id"))
            return


def rows(keys: list[str] | None = None) -> list[dict]:
    import psycopg
    from psycopg.rows import dict_row
    with psycopg.connect(_F.core_dsn(), row_factory=dict_row, connect_timeout=5) as conn:
        if keys is not None and not keys:
            return []
        if keys is None:
            identities = conn.execute(
                "SELECT model_key,hub_id,framework,primary_task,metadata,updated_at "
                "FROM model_census c WHERE NOT EXISTS "
                "(SELECT 1 FROM model_key_aliases a WHERE a.alias_key=c.model_key) ORDER BY model_key").fetchall()
            copies = conn.execute(
                "SELECT coalesce(a.model_key,c.model_key) AS model_key,c.location_kind,c.location_id,"
                "c.path,c.bytes,c.details,c.object_digest,c.verified,c.present,c.observed_at "
                "FROM model_copies c LEFT JOIN model_key_aliases a ON a.alias_key=c.model_key "
                "WHERE c.present ORDER BY model_key,c.location_kind,c.location_id").fetchall()
        else:
            identities = conn.execute(
                "SELECT model_key,hub_id,framework,primary_task,metadata,updated_at "
                "FROM model_census c WHERE model_key = ANY(%s) AND NOT EXISTS "
                "(SELECT 1 FROM model_key_aliases a WHERE a.alias_key=c.model_key) ORDER BY model_key", (keys,)).fetchall()
            copies = conn.execute(
                "SELECT coalesce(a.model_key,c.model_key) AS model_key,c.location_kind,c.location_id,"
                "c.path,c.bytes,c.details,c.object_digest,c.verified,c.present,c.observed_at "
                "FROM model_copies c LEFT JOIN model_key_aliases a ON a.alias_key=c.model_key "
                "WHERE c.present AND coalesce(a.model_key,c.model_key) = ANY(%s) "
                "ORDER BY model_key,c.location_kind,c.location_id", (keys,)).fetchall()
    by_key: dict[str, list] = {}
    for copy in copies:
        by_key.setdefault(copy["model_key"], []).append(dict(copy))
    return [{**dict(row), "copies": by_key.get(row["model_key"], [])} for row in identities]
