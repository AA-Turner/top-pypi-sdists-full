#!/usr/bin/env python3
"""textcharts-specific semantic parity comparator: source YAML corpus vs todo-db export.

Proves every source item/field that todo-db *can* model is preserved exactly
(modulo the importer's documented transforms), and enumerates every source field
the target model intentionally does not carry (so the drop is acknowledged, not
silent). Exit 0 = parity holds for modeled fields; exit 1 = a modeled-field
mismatch (blocks cutover).

Usage: parity_check.py <export.json> <todo_dir> <done_dir>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
STATUS_MAP = {
    "not started": "planning",
    "identified": "planning",
    "in progress": "active",
    "under review": "active",
    "blocked": "active",
}
PRIORITIES = ("critical", "high", "medium-high", "medium", "low")
# Fields present in the legacy YAML that the todo-db schema intentionally does
# NOT model (reported as acknowledged drops, never as parity failures).
UNMODELED = (
    "tags", "owners", "estimated_effort", "impact", "success_metrics",
    "open_questions", "research_value", "files_affected", "context_sections",
    "technical_requirements", "commits", "due_date", "budget_allocated",
    "last_updated", "moved_from", "sections", "id_slug_source",
)


def slugify(raw: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-")
    return s or "item"


def load_items(todo_dir: Path, done_dir: Path):
    items = {}
    for root, archived in ((todo_dir, False), (done_dir, True)):
        if not root or not root.exists():
            continue
        for path in sorted(root.rglob("*.yaml")):
            if "_indexes" in path.parts:
                continue
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                continue
            raw_id = str(data.get("id") or path.stem)
            item_id = raw_id if SLUG_RE.match(raw_id) else slugify(raw_id)
            items[item_id] = (data, archived, path, raw_id)
    return items


def coerce_verifications(v):
    out = []
    if isinstance(v, dict):  # legacy {commands: [...]}
        for c in v.get("commands", []) or []:
            out.append((str(c), None, None))
        return out
    for entry in v or []:
        if isinstance(entry, dict):
            out.append((
                str(entry.get("description") or "").strip(),
                (str(entry["command"]).strip() if entry.get("command") else None),
                (str(entry.get("expected_output") or entry.get("expected") or "").strip() or None),
            ))
        else:
            out.append((str(entry).strip(), None, None))
    return out


def source_state(data, archived):
    status = str(data.get("status") or "").strip().lower()
    if archived or status == "completed":
        return "done"
    return STATUS_MAP.get(status or "not started", "planning")


def index_by_item(rows, key="item_id"):
    out = {}
    for r in rows:
        out.setdefault(r.get(key), []).append(r)
    return out


def main() -> int:
    export = json.load(open(sys.argv[1]))
    todo_dir, done_dir = Path(sys.argv[2]), Path(sys.argv[3])
    src = load_items(todo_dir, done_dir)
    T = export["tables"]
    exp_items = {i["id"]: i for i in T["items"]}
    work = index_by_item(T["work_units"])
    wneeds = index_by_item(T["work_needs"])
    deps = index_by_item(T["item_deps"])
    scope = index_by_item(T["scope_rules"])
    preserves = index_by_item(T["preserves"])
    verifs = index_by_item(T["verifications"])
    antis = index_by_item(T["anti_patterns"])
    defs_by = index_by_item(T["deferrals"], key="from_item")

    mismatches, drops = [], []
    def fail(item, field, want, got):
        mismatches.append(f"[{item}] {field}: source={want!r} export={got!r}")

    # No phantom items in export
    for eid in exp_items:
        if eid not in src:
            mismatches.append(f"[{eid}] present in export but not in source corpus")
    # Count gate
    if len(src) != len(exp_items):
        mismatches.append(f"item count: source={len(src)} export={len(exp_items)}")

    for item_id, (data, archived, path, raw_id) in sorted(src.items()):
        e = exp_items.get(item_id)
        if e is None:
            mismatches.append(f"[{item_id}] MISSING from export ({path})")
            continue
        # id sanitization provenance
        if raw_id != item_id:
            drops.append(f"[{item_id}] id sanitized from {raw_id!r}")
        # scalars
        if archived:
            title = str(data.get("title") or "").strip() or f"Archived item {path.stem}"
        else:
            title = str(data.get("title", ""))
        if title[:200] != (e["title"] or "")[:200]:
            fail(item_id, "title", title, e["title"])
        pr = str(data.get("priority") or "medium").strip().lower()
        pr = pr if pr in PRIORITIES else "medium"
        if pr != e["priority"]:
            fail(item_id, "priority", pr, e["priority"])
        wt = str(data.get("worktree") or path.parent.parent.name)
        if wt != e["worktree"]:
            fail(item_id, "worktree", wt, e["worktree"])
        if (data.get("category") or None) != e["category"]:
            fail(item_id, "category", data.get("category"), e["category"])
        st = source_state(data, archived)
        if st != e["state"]:
            fail(item_id, "state", st, e["state"])
        created = str((data.get("metadata") or {}).get("created_date") or "") or None
        created_at = f"{created}T00:00:00Z" if created and "T" not in created else created
        if created_at != e["created_at"]:
            fail(item_id, "created_at", created_at, e["created_at"])
        if st == "done":
            comp = str(data.get("completed_date") or "") or None
            comp_at = f"{comp}T00:00:00Z" if comp and "T" not in comp else comp
            if comp_at != e["completed_at"]:
                fail(item_id, "completed_at", comp_at, e["completed_at"])
        # work units (valid w-ids only, matching importer)
        s_work = data.get("work") or []
        if isinstance(s_work, dict):
            s_work = list(s_work.values())
        valid = {}
        for u in s_work:
            if not isinstance(u, dict):
                continue
            wid = str(u.get("id") or "")
            if not re.fullmatch(r"w[0-9]{1,3}", wid) or wid in valid:
                continue
            summ = (str(u.get("summary") or u.get("title") or "").strip() or "(no summary recorded)")[:200]
            status = u.get("status", "done" if st == "done" else "pending")
            valid[wid] = (summ, status)
        e_work = {r["wid"]: (r["summary"], r["status"]) for r in work.get(item_id, [])}
        if set(valid) != set(e_work):
            fail(item_id, "work.ids", sorted(valid), sorted(e_work))
        for wid, sv in valid.items():
            if wid in e_work and sv != e_work[wid]:
                fail(item_id, f"work[{wid}]", sv, e_work[wid])
        # work needs
        s_needs = {(u.get("id"), n) for u in s_work if isinstance(u, dict)
                   for n in (u.get("needs") or []) if u.get("id") in valid and n in valid}
        e_needs = {(r["wid"], r["needs_wid"]) for r in wneeds.get(item_id, [])}
        if s_needs != e_needs:
            fail(item_id, "work_needs", sorted(s_needs), sorted(e_needs))
        # item deps
        s_deps = set((data.get("deps") or {}).get("needs", []) if isinstance(data.get("deps"), dict) else [])
        s_deps = {d for d in s_deps if d in src}  # dangling excluded by importer
        e_deps = {r["needs_item"] for r in deps.get(item_id, [])}
        if s_deps != e_deps:
            fail(item_id, "item_deps", sorted(s_deps), sorted(e_deps))
        # scope (deduped sets)
        sd = data.get("scope_limit") or data.get("scope") or {}
        s_scope = {(k, str(g)) for k in ("only_modify", "do_not_modify")
                   for g in (sd.get(k) or [])} if isinstance(sd, dict) else set()
        e_scope = {(r["kind"], r["path_glob"]) for r in scope.get(item_id, [])}
        if s_scope != e_scope:
            fail(item_id, "scope_rules", sorted(s_scope), sorted(e_scope))
        # preserves
        s_pres = {str(x) for x in (data.get("must_preserve") or [])}
        e_pres = {r["behavior"] for r in preserves.get(item_id, [])}
        if s_pres != e_pres:
            fail(item_id, "preserves", sorted(s_pres), sorted(e_pres))
        # verifications (ordered)
        s_ver = coerce_verifications(data.get("verification"))
        e_ver = [(r["description"], r["command"], r["expected"])
                 for r in sorted(verifs.get(item_id, []), key=lambda r: r["seq"])]
        if s_ver != e_ver:
            fail(item_id, "verifications", s_ver, e_ver)
        # anti_patterns (count parity; parsing owned by importer)
        s_anti = len(data.get("anti_patterns") or [])
        e_anti = len(antis.get(item_id, []))
        if s_anti != e_anti:
            fail(item_id, "anti_patterns.count", s_anti, e_anti)
        # deferrals (summary+reason set)
        s_def = {(str(d.get("summary")), str(d.get("reason"))) for d in (data.get("deferred") or [])}
        e_def = {(r["summary"], r["reason"]) for r in defs_by.get(item_id, [])}
        if s_def != e_def:
            fail(item_id, "deferrals", sorted(s_def), sorted(e_def))
        # enumerate intentional drops
        present_unmodeled = [f for f in UNMODELED if f in data
                             or (f in (data.get("metadata") or {}))]
        if present_unmodeled:
            drops.append(f"[{item_id}] unmodeled-dropped: {', '.join(sorted(present_unmodeled))}")

    print("=" * 72)
    print(f"SEMANTIC PARITY: {len(src)} source items vs {len(exp_items)} export items")
    print("=" * 72)
    print(f"MODELED-FIELD MISMATCHES (blocking): {len(mismatches)}")
    for m in mismatches:
        print("  FAIL", m)
    print(f"\nINTENTIONAL / DOCUMENTED DROPS (non-blocking, acknowledged): {len(drops)}")
    for d in drops:
        print("  drop", d)
    print("\nVERDICT:", "PASS — modeled fields fully preserved" if not mismatches
          else "FAIL — modeled-field parity broken")
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
