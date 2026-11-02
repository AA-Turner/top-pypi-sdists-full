"""Write one box's telemetry into core's mirror of the wrapper tables (sql/021, 022).

The box's store is SQLite (epoch seconds, 0/1 booleans, JSON as text or decoded by
the API); the mirror is Postgres (timestamptz, boolean, jsonb, arrays, inet). Each
value is converted by the TARGET column's type, read from the catalog once.

  state tables  the box's whole snapshot each time: every row upserted by the
                table's primary key, rows the box no longer has deleted (an
                evicted resident, a removed model)
  log tables    upserted by (worker, box_id); box_id is the row's id in the box's
                store, the mirror keeps its own id

A row is rewritten only when a value differs (IS DISTINCT FROM), so the legacy
triggers (facts / model_rows / live NOTIFYs) fire on real changes, as they did when
the wrapper wrote Postgres itself. Generated and identity columns are never written.
"""
from __future__ import annotations

import datetime as _dt
import ipaddress
import json
import logging
import math
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

logger = logging.getLogger("hugpy_core.intake")

STATE_TABLES = ("gpu_state", "host_state", "cpu_state", "residents", "models", "gguf_projection_facts",
                "cuda_context_facts", "tf_structure", "tf_measure_facts", "kv_structure", "ctx_probe_facts",
                "projector_facts", "load_estimates")
# Incoming wrapper table names remain stable. Core retains per-worker disk
# observations under an explicit name; public `models` is the fleet dossier.
MIRROR_TABLES = {"models": "worker_model_copies"}
# log table -> rows that can still change (re-read until they settle).
# call_log: a row is non-terminal while call_state is NULL (just inserted),
# 'pending' (accepted, not yet running) or 'running' (prefill/decode in flight);
# the wrapper only stamps its timings (prompt_n/ms, predicted_n/ms, cache_n, …)
# and its inline derivation (load_s, load_class, load_cached_bytes, predicted_*,
# derived_v — fitevict adapters/db.upsert calls serve/eta.derive_call before the
# terminal write) at the moment it turns terminal. Terminal = done | failed |
# interrupted | cancelled (fitevict/serve/front_door.py + adapters/db.mark_interrupted);
# every other value (incl. 'running') must keep being re-read or the mirror
# freezes a row with NULL timings. Because the derivation is written in the SAME
# upsert that sets the terminal state, a terminal row already carries its derived
# columns — there is no post-terminal settling window to wait on per call.
LOG_TABLES = {
    "call_log": "call_state IS NULL OR call_state IN ('pending', 'running')",
    "resource_log": None,
    "evictions": "released_at IS NULL",
    "operator_actions": "done_at IS NULL",
}
# the box keeps these as core's copies (core -> box); core's own tables are the truth
NOT_MIRRORED = ("pair_settings", "model_quant_facts", "env_profiles", "api_keys")


class Columns:
    """Writable columns and their types per mirror table, plus primary keys."""

    def __init__(self, conn):
        self.types: Dict[str, Dict[str, str]] = {}
        self.pk: Dict[str, Tuple[str, ...]] = {}
        rows = conn.execute(
            "SELECT table_name, column_name, data_type, udt_name FROM information_schema.columns"
            " WHERE table_schema = 'public' AND is_generated = 'NEVER' AND is_identity = 'NO'"
            "   AND table_name = ANY(%s) ORDER BY table_name, ordinal_position",
            (list(dict.fromkeys(MIRROR_TABLES.get(t, t) for t in STATE_TABLES)) + list(LOG_TABLES),)).fetchall()
        physical_types = {}
        for t, c, dt, udt in rows:
            physical_types.setdefault(t, {})[c] = udt if dt == "ARRAY" else dt
        for t in LOG_TABLES:
            if t in physical_types:
                self.types[t] = physical_types[t]
        for t in STATE_TABLES:
            physical = MIRROR_TABLES.get(t, t)
            if physical in physical_types:
                self.types[t] = physical_types[physical]
            pk = conn.execute(
                "SELECT a.attname FROM pg_index i JOIN pg_attribute a ON a.attrelid = i.indrelid"
                " AND a.attnum = ANY(i.indkey) WHERE i.indrelid = %s::regclass AND i.indisprimary"
                " ORDER BY array_position(i.indkey, a.attnum)", (physical,)).fetchall()
            self.pk[t] = tuple(r[0] for r in pk)


def _ts(v):
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return _dt.datetime.fromtimestamp(float(v), tz=_dt.timezone.utc)
    return v


def without_nul(value):
    """Normalize worker metadata to PostgreSQL-compatible JSON values."""
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, str):
        return value.replace("\x00", "")
    if isinstance(value, list):
        return [without_nul(item) for item in value]
    if isinstance(value, tuple):
        return tuple(without_nul(item) for item in value)
    if isinstance(value, dict):
        return {without_nul(key): without_nul(item) for key, item in value.items()}
    return value


def convert(v: Any, typ: str) -> Any:
    """A box value as the mirror column ``typ`` wants it."""
    from psycopg.types.json import Jsonb
    if v is None:
        return None
    if typ == "timestamp with time zone":
        return _ts(v)
    if typ == "boolean":
        return bool(v) if not isinstance(v, str) else v.lower() in ("1", "t", "true", "yes")
    if typ in ("jsonb", "json"):
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except ValueError:
                pass
        return Jsonb(without_nul(v))
    if typ.startswith("_"):                      # array (udt _int4, _text, …)
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except ValueError:
                v = [v]
        return list(v) if isinstance(v, (list, tuple)) else [v]
    if typ == "inet":
        try:
            return str(ipaddress.ip_address(str(v)))
        except ValueError:
            return None
    if typ in ("text", "character varying") and isinstance(v, (dict, list)):
        return json.dumps(without_nul(v))
    if typ in ("text", "character varying") and isinstance(v, str):
        return without_nul(v)
    if typ in ("integer", "bigint", "smallint") and isinstance(v, float) and v.is_integer():
        return int(v)
    return v


def _upsert_sql(table: str, cols: Sequence[str], key: Sequence[str]) -> str:
    q = lambda c: '"%s"' % c                                     # noqa: E731
    sets = [c for c in cols if c not in key]
    sql = (f"INSERT INTO {table} ({', '.join(map(q, cols))}) VALUES ({', '.join(['%s'] * len(cols))})"
           f" ON CONFLICT ({', '.join(map(q, key))})")
    if not sets:
        return sql + " DO NOTHING"
    return (sql + f" DO UPDATE SET {', '.join(f'{q(c)} = EXCLUDED.{q(c)}' for c in sets)}"
            f" WHERE ({', '.join(f'{table}.{q(c)}' for c in sets)})"
            f" IS DISTINCT FROM ({', '.join(f'EXCLUDED.{q(c)}' for c in sets)})")


def _rows_for(table: str, rows: Iterable[dict], types: Dict[str, str], worker: str,
              extra: Optional[Dict[str, str]] = None) -> Tuple[List[str], List[tuple]]:
    """(columns, value tuples) for the columns both the rows and the mirror have."""
    rows = [dict(r) for r in rows]
    # Mixed fleets: an old worker's facts remain in the legacy partition.
    # Supplying every PK component also makes snapshot deletion deterministic.
    for r in rows:
        if "artifact_fingerprint" in types:
            r["artifact_fingerprint"] = r.get("artifact_fingerprint") or ""
        if "variant" in types and "bnb4" in types and not r.get("variant"):
            r["variant"] = "gpu:bnb4" if convert(r.get("bnb4"), "boolean") else "gpu"
    extra = extra or {}
    seen: List[str] = []
    for r in rows:
        for k in r:
            k2 = extra.get(k, k)
            if k2 in types and k2 not in seen:
                seen.append(k2)
    if "worker" in types and "worker" not in seen:
        seen.append("worker")
    back = {v: k for k, v in extra.items()}
    out = []
    for r in rows:
        vals = []
        for c in seen:
            v = r.get(back.get(c, c))
            if c == "worker" and not v:
                v = worker
            vals.append(convert(v, types[c]))
        out.append(tuple(vals))
    return seen, out


def _norm(v):
    """A value as both sides compare it: what psycopg reads back (dict, Decimal,
    datetime, inet) and what convert() writes (Jsonb, float, datetime, str)."""
    import decimal
    from psycopg.types.json import Jsonb
    if isinstance(v, Jsonb):
        v = v.obj
    if isinstance(v, (dict, list, tuple)):
        return json.dumps(v, sort_keys=True, default=str)
    if isinstance(v, bool) or v is None:
        return v
    if isinstance(v, _dt.datetime):
        return round(v.timestamp(), 6)
    if isinstance(v, (int, float, decimal.Decimal)):
        return round(float(v), 6)
    return str(v)


def _changed(conn, table: str, names: List[str], values: List[tuple], key: Sequence[str],
             where: str, params: tuple) -> "tuple[List[tuple], Dict[tuple, tuple]]":
    """(rows that differ from what the mirror holds, {key: stored row}) — so a pass
    that brings nothing new issues NO statement: the legacy statement-level triggers
    (residents_live, fitevict_notify, evictions_notify, call_log live) fire per
    statement, changed rows or not, and a write every pass made the console's live
    versions tick ~2/s (its Call log panel then dropped every reply as stale)."""
    q = ", ".join('"%s"' % c for c in names)
    stored, raw_keys = {}, {}
    for row in conn.execute(f"SELECT {q} FROM {table} WHERE {where}", params).fetchall():
        rec = dict(zip(names, row))
        k = tuple(_norm(rec[c]) for c in key)
        stored[k] = tuple(_norm(x) for x in row)
        raw_keys[k] = tuple(rec[c] for c in key)
    out = []
    for v in values:
        rec = dict(zip(names, v))
        k = tuple(_norm(rec[c]) for c in key)
        if stored.get(k) != tuple(_norm(x) for x in v):
            out.append(v)
    return out, raw_keys


def apply_state(conn, cols: Columns, worker: str, snapshot: Dict[str, List[dict]]) -> Dict[str, int]:
    """The box's snapshot tables into the mirror. The caller wraps the whole pass in
    one transaction; each table is a savepoint within it, so one table's change-test
    SELECT or write never holds back the others (or aborts the batch)."""
    counts: Dict[str, int] = {}
    for t in STATE_TABLES:
        if t not in snapshot or t not in cols.types:
            continue
        try:
            with conn.transaction():          # a savepoint inside the pass's transaction
                counts[t] = _apply_table(conn, cols, worker, t, snapshot[t])
        except Exception:  # noqa: BLE001 — one table never holds back the others (or takes the box offline)
            logger.exception("intake %s: %s not mirrored", worker, t)
            counts[t] = -1
    return counts


def _apply_table(conn, cols: Columns, worker: str, t: str, snap: List[dict]) -> int:
    """One snapshot table: rows that changed are upserted, rows the box no longer has
    are deleted — and nothing is written when nothing changed."""
    types, key = cols.types[t], cols.pk[t]
    rows = [r for r in snap if (r.get("worker") or worker) == worker]
    names, values = _rows_for(t, rows, types, worker)
    if values and not all(k in names for k in key):
        return 0
    if not values:
        names = list(key)
    physical = MIRROR_TABLES.get(t, t)
    changed, stored = _changed(conn, physical, names, values, key, "worker = %s", (worker,))
    have = {tuple(_norm(dict(zip(names, v))[k]) for k in key) for v in values}
    gone = [raw for k, raw in stored.items() if k not in have]
    if not changed and not gone:
        return 0
    cond = " AND ".join('"%s" IS NOT DISTINCT FROM %%s' % c for c in key)
    if changed:
        conn.cursor().executemany(_upsert_sql(physical, names, key), changed)
    if gone:
        conn.cursor().executemany(f"DELETE FROM {physical} WHERE {cond}", gone)
    return len(changed) + len(gone)


def apply_log(conn, cols: Columns, worker: str, table: str, rows: List[dict], store_id: str = "") -> int:
    """Source row ids are scoped to the persistent SQLite store incarnation.
    Calls additionally have globally stable request ids, so adopting a pre-ID
    store updates the existing call instead of duplicating its history."""
    if not rows or table not in cols.types:
        return 0
    types = dict(cols.types[table])
    types.pop("id", None)
    rows = [{**r, "box_store_id": store_id} for r in rows]
    names, values = _rows_for(table, rows, types, worker, extra={"id": "box_id"})
    if "box_id" not in names:
        return 0
    with conn.transaction():
        if table == "call_log":
            if "request_id" not in names or any(not r.get("request_id") for r in rows):
                raise ValueError("call_log: a stable request_id is required")
            ids = [r["request_id"] for r in rows]
            foreign = conn.execute("SELECT request_id FROM call_log WHERE request_id = ANY(%s) "
                                   "AND worker IS NOT NULL AND worker <> %s LIMIT 1", (ids, worker)).fetchone()
            if foreign:
                raise ValueError("call_log: request_id already belongs to another worker")
            key = ("request_id",)
            where, params = "request_id = ANY(%s)", (ids,)
        else:
            ids = [dict(zip(names, v))["box_id"] for v in values]
            key = ("worker", "box_store_id", "box_id")
            where, params = "worker = %s AND box_store_id = %s AND box_id = ANY(%s)", (worker, store_id, ids)
        changed, _stored = _changed(conn, table, names, values, key, where, params)
        if changed:
            conn.cursor().executemany(_upsert_sql(table, names, key), changed)
    return len(changed)


def cursor(conn, worker: str, table: str, store_id: str = "") -> int:
    """Resume only the current source store; historical store rows are retained."""
    open_rows = LOG_TABLES.get(table)
    if open_rows:
        r = conn.execute(f"SELECT min(box_id) FROM {table} WHERE worker = %s AND box_store_id = %s AND ({open_rows})",
                         (worker, store_id)).fetchone()
        if r and r[0] is not None:
            return int(r[0]) - 1
    r = conn.execute(f"SELECT max(box_id) FROM {table} WHERE worker = %s AND box_store_id = %s",
                     (worker, store_id)).fetchone()
    return int(r[0]) if r and r[0] is not None else 0


__all__ = ["Columns", "apply_state", "apply_log", "cursor", "convert", "STATE_TABLES", "LOG_TABLES"]
