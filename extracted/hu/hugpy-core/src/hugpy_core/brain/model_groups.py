"""MODEL GROUPS — the console's Priority groups panel, DB-backed (sql/019).

LIFTED from legacy ``abstract_hugpy_dev/comms/priority_groups.py`` (record
shape, alias-tolerant key matching, normalize/validate, put/delete) and
``hugpy_server/app/routes/model_group_routes.py`` (the /llm/model-groups
routes and their status codes). Legacy kept the records in
$PROJECTS_HOME/settings.json; core answered GET /llm/model-groups with a stub
``[]``. Here the records are rows in ``hugpy_core.model_groups`` (DB is truth).

    GET    /llm/model-groups            every group (the hugpy-brain group is
                                        filled from the grades when empty)
    POST   /llm/model-groups            create or replace   {id?, name, members, workers?, enabled?}
    PUT    /llm/model-groups/<id>       replace
    PATCH  /llm/model-groups/<id>       partial update (same validated write)
    DELETE /llm/model-groups/<id>       remove (409 for a static group)
    GET    /llm/model-groups/resolve    honest: core's request routing does not
                                        walk priority groups yet
    POST   /llm/model-groups/<id>/allocate   honest 501 (not lifted yet)

STATIC + ROLE GROUPS (operator 2026-10-06): ``hugpy-brain`` is a static group
(``static``: never deleted or renamed; its members stay editable) with
``role='brain'``: the models the brain may run on, in priority order. A role
group never routes requests, may be empty (the brain refills it from the grades
when it is), and is outside the one-enabled-group-per-key rule.

ROUTING: core's pick/relay does not consult priority groups (it never did since
legacy central went off 2026-10-03). The list payload says so (``routing:
false``) and the panel shows it, rather than implying a fallback that does not
happen.
"""
from __future__ import annotations

import logging
import re
import time
from typing import Any, List, Optional, Tuple


logger = logging.getLogger("hugpy_core.model_groups")


GROUP_REF = "group:"
_SLUG_RE = re.compile(r"[^a-z0-9]+")
_COLS = ("id", "name", "members", "workers", "enabled", "static", "role", "source", "note",
         "by", "created_at", "updated_at")
_ensured = [False]

_DDL = """
CREATE TABLE IF NOT EXISTS model_groups (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    members     JSONB NOT NULL DEFAULT '[]'::jsonb,
    workers     JSONB NOT NULL DEFAULT '[]'::jsonb,
    enabled     BOOLEAN NOT NULL DEFAULT TRUE,
    static      BOOLEAN NOT NULL DEFAULT FALSE,
    role        TEXT,
    source      TEXT NOT NULL DEFAULT 'operator',
    note        TEXT NOT NULL DEFAULT '',
    by          TEXT NOT NULL DEFAULT 'operator',
    created_at  DOUBLE PRECISION NOT NULL,
    updated_at  DOUBLE PRECISION NOT NULL
)"""


def _conn():
    from hugpy_core.models.modeldb import _conn as c
    return c()


def _ensure() -> None:
    if _ensured[0]:
        return
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SET lock_timeout = '5s'")
        cur.execute(_DDL)
        conn.commit()
    _ensured[0] = True


# ── key matching (lifted verbatim in behaviour: workers._match_keys rule) ──────
def key_forms(model_key: Any) -> set:
    """Raw, lowercased, the '/'-tail and the '~'-tail. Suffixes are NEVER
    stripped: '-GGUF' and the bare name are two members the operator ordered."""
    s = str(model_key or "").strip()
    if not s:
        return set()
    forms = {s, s.lower()}
    tail = s.split("/")[-1]
    forms.update({tail, tail.lower()})
    if "~" in s:
        base = s.split("~", 1)[1]
        if base:
            forms.update({base, base.lower()})
    return forms


def keys_match(a: Any, b: Any) -> bool:
    fa, fb = key_forms(a), key_forms(b)
    return bool(fa and fb and (fa & fb))


def slugify(text: Any, fallback: str = "group") -> str:
    s = _SLUG_RE.sub("-", str(text or "").strip().lower()).strip("-")
    return s or fallback


def is_group_ref(member: Any) -> bool:
    return str(member or "").strip().lower().startswith(GROUP_REF)


def ref_id(member: Any) -> str:
    return str(member or "").strip()[len(GROUP_REF):].strip()


# ── reads ──────────────────────────────────────────────────────────────────────
def _row(r: dict) -> dict:
    out = {k: r.get(k) for k in _COLS}
    out["members"] = list(r.get("members") or [])
    out["workers"] = list(r.get("workers") or [])
    out["routes"] = bool(out["enabled"]) and not out["role"]
    return out


def all_groups() -> List[dict]:
    _ensure()
    with _conn() as conn, conn.cursor() as cur:
        cur.execute(f"SELECT {', '.join(_COLS)} FROM model_groups ORDER BY static DESC, name, id")
        return [_row(r) for r in cur.fetchall()]


def get_group(group_id: Any) -> Optional[dict]:
    _ensure()
    with _conn() as conn, conn.cursor() as cur:
        cur.execute(f"SELECT {', '.join(_COLS)} FROM model_groups WHERE id = %s", (str(group_id or ""),))
        r = cur.fetchone()
    return _row(r) if r else None


def expand_members(group: dict, groups: Optional[List[dict]] = None,
                   _seen: Optional[set] = None) -> List[Tuple[str, Optional[str]]]:
    """[(model_key, via_group)] with nested 'group:<id>' members expanded in
    place; cycles are not followed; a repeated key keeps its first position."""
    groups = all_groups() if groups is None else groups
    by_id = {g["id"]: g for g in groups}
    seen = set(_seen or ())
    seen.add(group.get("id"))
    out: List[Tuple[str, Optional[str]]] = []
    have: List[str] = []
    for m in (group.get("members") or []):
        if is_group_ref(m):
            child = by_id.get(ref_id(m))
            if child is None or child["id"] in seen:
                continue
            for key, _via in expand_members(child, groups, seen):
                if not any(keys_match(key, h) for h in have):
                    have.append(key)
                    out.append((key, child["id"]))
        elif not any(keys_match(m, h) for h in have):
            have.append(m)
            out.append((m, None))
    return out


# ── validation (lifted; role groups are the one extension) ─────────────────────
def validate(group_id: str, name: Any, members: Any, enabled: Any, *, role: Optional[str] = None,
             groups: Optional[List[dict]] = None, workers: Any = None) -> Tuple[list, list, list]:
    """(clean_members, clean_workers, errors). THE ONE STRUCTURAL RULE: a model
    key may appear in at most one ENABLED routing group. A role group (the
    hugpy-brain group) never routes, so it neither claims keys nor conflicts,
    and it may be empty (the brain refills it from the grades)."""
    errors: List[str] = []
    gid = str(group_id or "").strip()
    if not gid:
        errors.append("id is required")
    if not str(name or "").strip():
        errors.append("name is required")
    clean: List[str] = []
    if not isinstance(members, (list, tuple)):
        errors.append("members must be a list of model keys, in priority order")
        members = []
    for m in members:
        m = str(m or "").strip()
        if not m:
            continue
        if any(keys_match(m, seen) for seen in clean):
            errors.append(f"duplicate member {m!r} — a member may be listed once")
            continue
        clean.append(m)
    if not clean and not role:
        errors.append("members must contain at least one model key")
    for m in clean:
        if is_group_ref(m) and ref_id(m) == gid:
            errors.append(f"{m!r} — a group cannot contain itself")
    clean_workers: List[str] = []
    if workers is None:
        workers = []
    if not isinstance(workers, (list, tuple)):
        errors.append("workers must be a list of worker ids or names, in priority order")
        workers = []
    for w in workers:
        w = str(w or "").strip()
        if not w:
            continue
        if w.lower() in {s.lower() for s in clean_workers}:
            errors.append(f"duplicate worker {w!r} — a worker may be listed once")
            continue
        clean_workers.append(w)
    if bool(enabled) and not role:
        others = [g for g in (all_groups() if groups is None else groups)
                  if g.get("routes") and g["id"] != gid]
        for m in clean:
            for og in others:
                if any(keys_match(m, om) for om in (og.get("members") or [])):
                    errors.append(f"{m!r} is already a member of the enabled group {og['id']!r} "
                                  f"({og.get('name')}) — a model key may be in at most one enabled group")
    return clean, clean_workers, errors


# ── writes ─────────────────────────────────────────────────────────────────────
def put_group(group_id: Any, *, name: Any, members: Any, enabled: Any = True, workers: Any = None,
              by: Optional[str] = None, source: str = "operator", note: Optional[str] = None
              ) -> Tuple[Optional[dict], list]:
    """Create or REPLACE a group (members/workers are each an ORDER). A static
    group keeps its id, name, role and static flag whatever the body says."""
    from psycopg.types.json import Jsonb
    gid = slugify(group_id or name)
    prior = get_group(gid) or {}
    if prior.get("static"):
        name = prior["name"]
    role = prior.get("role")
    clean, clean_workers, errors = validate(gid, name, members, enabled, role=role, workers=workers)
    if errors:
        return None, errors
    now = time.time()
    with _conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO model_groups (id, name, members, workers, enabled, static, role, source, note, by,"
            " created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            " ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name, members=EXCLUDED.members,"
            " workers=EXCLUDED.workers, enabled=EXCLUDED.enabled, source=EXCLUDED.source,"
            " note=EXCLUDED.note, by=EXCLUDED.by, updated_at=EXCLUDED.updated_at",
            (gid, str(name).strip(), Jsonb(clean), Jsonb(clean_workers), bool(enabled),
             bool(prior.get("static")), role, source,
             prior.get("note", "") if note is None else note, by or "operator",
             prior.get("created_at") or now, now))
        conn.commit()
    logger.info("model group %s: members=%s enabled=%s (by=%s, source=%s)", gid, clean, bool(enabled),
                by or "operator", source)
    return get_group(gid), []


def ensure_static(gid: str, *, name: str, role: str, note: str = "") -> dict:
    """Create a static role group (empty) when it does not exist yet."""
    _ensure()
    now = time.time()
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO model_groups (id, name, members, workers, enabled, static, role, source,"
                    " note, by, created_at, updated_at) VALUES (%s,%s,'[]','[]',TRUE,TRUE,%s,'auto',%s,"
                    "'hugpy-core',%s,%s) ON CONFLICT (id) DO NOTHING", (gid, name, role, note, now, now))
        conn.commit()
    return get_group(gid)


def delete_group(group_id: Any) -> "Tuple[bool, Optional[str]]":
    gid = str(group_id or "").strip()
    g = get_group(gid)
    if g is None:
        return False, None
    if g.get("static"):
        return False, f"{gid!r} is a static group — it cannot be deleted (edit its members instead)"
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM model_groups WHERE id = %s", (gid,))
        conn.commit()
    logger.info("model group deleted: %s", gid)
    return True, None


# ── route handlers (kwargs in, JSON-able out; brain/routes.py mounts them under
#    /llm/model-groups). Former path params (group_id) and body fields arrive as
#    the same-named kwargs; the registrar answers {"result": ...}. ─────────────
_UNSET = object()


def _who() -> str:
    return "operator"      # core's auth posture is open; central auth plugs in here


def model_groups_list():
    """Never raises up: a failed read reports an empty list with the error."""
    try:
        from hugpy_core.brain import brain
        brain.ensure_brain_group()          # static hugpy-brain group, filled when empty
    except Exception as exc:  # noqa: BLE001
        logger.warning("hugpy-brain group ensure failed: %s", exc)
    try:
        return {"groups": all_groups(), "routing": False,
                "routing_note": "core's request routing does not walk priority groups yet; "
                                "groups are stored and the hugpy-brain group drives the brain"}
    except Exception as exc:  # noqa: BLE001
        logger.warning("GET /llm/model-groups failed: %s", exc, exc_info=True)
        return {"groups": [], "error": str(exc)}


def model_groups_resolve(key=None):
    key = (key or "").strip()
    if not key:
        return {"error": "key is required"}
    claim = next((g for g in all_groups() if g.get("routes")
                  and any(keys_match(key, m) for m, _v in expand_members(g))), None)
    return {"requested": key, "group": claim["id"] if claim else None, "candidates": [],
            "chosen": None, "route": None,
            "why": "core's request routing does not walk priority groups yet — the request "
                   "is served as named" + (f" (group {claim['id']!r} is stored, not applied)"
                                           if claim else "")}


def model_groups_create(id=None, name=None, members=None, enabled=True, workers=None):
    rec, errors = put_group(id or name, name=name, members=members, enabled=enabled,
                            workers=workers, by=_who())
    if errors:
        return {"error": "; ".join(errors), "errors": errors}
    return {"group": rec}


def model_groups_update(group_id=None, name=_UNSET, members=_UNSET, enabled=_UNSET, workers=_UNSET):
    cur = get_group(group_id)
    base = cur or {"name": group_id, "members": [], "enabled": True}
    rec, errors = put_group(
        group_id,
        name=(base.get("name") if name is _UNSET else name),
        members=(base.get("members") if members is _UNSET else members),
        enabled=(base.get("enabled", True) if enabled is _UNSET else enabled),
        workers=(base.get("workers") if workers is _UNSET else workers),
        by=_who(),
        source=("operator" if members is not _UNSET else (cur or {}).get("source", "operator")),
    )
    if errors:
        return {"error": "; ".join(errors), "errors": errors}
    return {"group": rec}


def model_groups_delete(group_id=None):
    ok, why = delete_group(group_id)
    if why:
        return {"error": why}
    if not ok:
        return {"error": f"no such priority group: {group_id}"}
    return {"deleted": group_id}


def model_groups_allocate(group_id=None):
    return {"error": "group allocate is not lifted into core yet — designate each model "
                     "from the Workers panel"}
