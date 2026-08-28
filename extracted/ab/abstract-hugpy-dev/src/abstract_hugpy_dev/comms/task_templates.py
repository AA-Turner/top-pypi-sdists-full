"""TASK TEMPLATES — the operator's task blueprint over groups and workers.

Operator concept (2026-08-26): "Templates => worker groups && => module groups
— handle specific tasks by mapping out what groups are needed and reserving
the pool for their non-interrupted execution."

A template names the MODULE GROUPS (``comms.priority_groups`` records) a task
needs and the WORKERS that should host them. ACTIVATING a template:

  1. sets each listed worker's ``pool`` to the template id — the existing
     exact-match reservation: a pooled worker serves ONLY traffic tagged with
     that pool, and general traffic can no longer land on it (the
     "non-interrupted execution" half);
  2. allocates every listed group (expanded, nested modules included) to those
     workers — the designation swath (the "what groups are needed" half).

DEACTIVATING clears the pool tag on every worker still carrying it.
Designations are deliberately LEFT IN PLACE — they are cheap registry state
(see the k119 doctrine: generous designation, honest serving), and the next
activation is instant because of them.

Storage mirrors ``priority_groups``: the F4 settings store, namespace
``task_templates``, one validated write path (``put_template``). Activation
ORCHESTRATION lives in the route layer (it needs the worker store); this
module owns only the records and the derivations.

RECORD SHAPE
------------
    {"id": str, "name": str,
     "groups": [str, ...],   # priority-group ids, in display order
     "workers": [str, ...],  # ORDERED worker ids/names; [] = derive from the
                             # groups' effective_workers at activation time
     "active": bool,         # last activation state (informational; the pool
                             # tags on the workers are the ground truth)
     "activated_at": float|None,
     "created_at": float, "updated_at": float, "by": str}
"""
from __future__ import annotations

import logging
import time
from typing import Any, List, Optional, Tuple

from .priority_groups import (all_groups, effective_workers, get_group,
                              slugify)
from .settings import settings_store

logger = logging.getLogger(__name__)

NS = "task_templates"


def _normalize(tid: str, raw: Any) -> Optional[dict]:
    if not isinstance(raw, dict):
        return None
    groups: List[str] = []
    for g in (raw.get("groups") or []):
        g = str(g or "").strip()
        if g and g not in groups:
            groups.append(g)
    workers: List[str] = []
    for w in (raw.get("workers") or []):
        w = str(w or "").strip()
        if w and w.lower() not in {s.lower() for s in workers}:
            workers.append(w)
    return {
        "id": str(tid),
        "name": str(raw.get("name") or tid),
        "groups": groups,
        "workers": workers,
        "active": bool(raw.get("active", False)),
        "activated_at": raw.get("activated_at"),
        "created_at": raw.get("created_at"),
        "updated_at": raw.get("updated_at"),
        "by": raw.get("by") or "operator",
    }


def all_templates() -> List[dict]:
    try:
        raw = settings_store.all(NS) or {}
    except Exception as exc:  # noqa: BLE001 — a read must never break a caller
        logger.warning("task templates: read failed (%s) — none", exc)
        return []
    out = []
    for tid, rec in raw.items():
        norm = _normalize(str(tid), rec)
        if norm is not None:
            out.append(norm)
    out.sort(key=lambda t: (str(t.get("name") or "").lower(), t["id"]))
    return out


def get_template(template_id: Any) -> Optional[dict]:
    tid = str(template_id or "").strip()
    if not tid:
        return None
    try:
        return _normalize(tid, settings_store.get(NS, tid))
    except Exception as exc:  # noqa: BLE001
        logger.warning("task templates: read failed for %s (%s)", tid, exc)
        return None


def derive_workers(template: dict) -> List[str]:
    """The workers an activation will reserve: the template's own ordered list
    when set, else the order-preserving union of every listed group's
    ``effective_workers`` — so a template of allocated groups needs no worker
    list of its own. Never raises."""
    own = [w for w in (template.get("workers") or []) if str(w).strip()]
    if own:
        return own
    try:
        groups = all_groups()
    except Exception:  # noqa: BLE001
        return []
    out: List[str] = []
    for gid in (template.get("groups") or []):
        g = next((x for x in groups if x["id"] == gid), None)
        if not g:
            continue
        for w in effective_workers(g, groups):
            if w.lower() not in {s.lower() for s in out}:
                out.append(w)
    return out


def validate(template_id: str, name: Any, groups: Any,
             workers: Any) -> Tuple[list, list, list]:
    """``(clean_groups, clean_workers, errors)``. A referenced group must
    exist — a template is an execution blueprint, and activating a blueprint
    with a dangling cast member is a typed failure the operator should get at
    WRITE time, not mid-run (contrast: nested ``group:`` members tolerate
    dangling because the walk reports them per-request)."""
    errors: List[str] = []
    if not str(template_id or "").strip():
        errors.append("id is required")
    if not str(name or "").strip():
        errors.append("name is required")

    clean_groups: List[str] = []
    if not isinstance(groups, (list, tuple)):
        errors.append("groups must be a list of priority-group ids")
        groups = []
    for g in groups:
        g = str(g or "").strip()
        if not g:
            continue
        if g in clean_groups:
            errors.append(f"duplicate group {g!r}")
            continue
        if get_group(g) is None:
            errors.append(f"no such priority group: {g!r}")
            continue
        clean_groups.append(g)
    if not clean_groups:
        errors.append("groups must name at least one priority group")

    clean_workers: List[str] = []
    if workers is None:
        workers = []
    if not isinstance(workers, (list, tuple)):
        errors.append("workers must be a list of worker ids or names")
        workers = []
    for w in workers:
        w = str(w or "").strip()
        if not w:
            continue
        if w.lower() in {s.lower() for s in clean_workers}:
            errors.append(f"duplicate worker {w!r}")
            continue
        clean_workers.append(w)
    return clean_groups, clean_workers, errors


def put_template(template_id: Any, *, name: Any, groups: Any,
                 workers: Any = None,
                 by: Optional[str] = None) -> Tuple[Optional[dict], list]:
    """Create or REPLACE a template — the one validated write path."""
    tid = slugify(template_id or name, fallback="template")
    clean_groups, clean_workers, errors = validate(tid, name, groups, workers)
    if errors:
        return None, errors
    prior = get_template(tid) or {}
    now = time.time()
    rec = {
        "id": tid,
        "name": str(name).strip(),
        "groups": clean_groups,
        "workers": clean_workers,
        "active": bool(prior.get("active", False)),
        "activated_at": prior.get("activated_at"),
        "created_at": prior.get("created_at") or now,
        "updated_at": now,
        "by": by or "operator",
    }
    settings_store.set(NS, tid, rec)
    logger.info("task template %s: groups=%s workers=%s (by=%s)",
                tid, clean_groups, clean_workers, rec["by"])
    return rec, []


def mark_active(template_id: Any, active: bool) -> Optional[dict]:
    """Flip the informational active flag (the pool tags are ground truth)."""
    rec = get_template(template_id)
    if rec is None:
        return None
    rec["active"] = bool(active)
    rec["activated_at"] = time.time() if active else rec.get("activated_at")
    rec["updated_at"] = time.time()
    settings_store.set(NS, rec["id"], rec)
    return rec


def delete_template(template_id: Any) -> bool:
    tid = str(template_id or "").strip()
    if not tid:
        return False
    existed = settings_store.delete(NS, tid)
    if existed:
        logger.info("task template deleted: %s", tid)
    return bool(existed)
