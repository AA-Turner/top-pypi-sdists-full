"""Knowledge CLI — dispatch and query handlers.

Heavy modules extracted:
- knowledge_ingest.py: add, import, learn, teach
- knowledge_share.py: share push/pull
- knowledge_help.py: help docs
"""
from __future__ import annotations

import re

from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.domain.knowledge import KnowledgeManager

from kanban_framework.cli.knowledge_ingest import (
    handle_add, handle_import, handle_learn, handle_teach,
    handle_benchmark,
)
from kanban_framework.cli.knowledge_share import handle_share
from kanban_framework.cli.knowledge_help import handle_help


_scope_prompted = False


def _check_scope(km: KnowledgeManager) -> dict | None:
    """Check if knowledge.scope is configured."""
    import os
    if os.environ.get("KANBAN_KNOWLEDGE_SCOPE"):
        return None
    scope = getattr(km, '_scope', '')
    if not scope:
        return {
            "error": "knowledge.scope 未配置。请先执行 kanban init 或手动设置 config.json 中 knowledge.scope 字段。",
            "code": "SCOPE_REQUIRED",
            "hint": "config.json: {\"knowledge\": {\"scope\": \"your-name\"}}",
            "env_override": "KANBAN_KNOWLEDGE_SCOPE=ci kanban knowledge add ...",
        }
    return None


def _build_summary(results: list[dict], limit: int = 10) -> list[dict]:
    return [
        {"id": r["id"], "title": r.get("title", ""),
         "relevance": r.get("relevance") or r.get("score", 0)}
        for r in results[:limit]
    ]


def _strip_heavy_fields(results: list[dict]) -> list[dict]:
    heavy = {"content", "code_example", "content_segmented", "steps", "embedding"}
    return [{k: v for k, v in r.items() if k not in heavy} for r in results]


def dispatch(args: list[str]) -> dict:
    sub = args[0] if args else "search"

    if sub in ("--help", "-h", "help"):
        root = Filesystem.find_project_root()
        fs = Filesystem(root=root)
        km = KnowledgeManager(fs, read_only=True)
        return handle_help(km, args[1:] if len(args) > 1 else [])

    root = Filesystem.find_project_root()
    fs = Filesystem(root=root)

    _READ_ONLY = {"search", "hybrid", "semantic", "get", "list", "match",
                  "domains", "categories", "similar", "usage", "health",
                  "stale", "gaps", "pending"}
    km = KnowledgeManager(fs, read_only=(sub in _READ_ONLY))

    if sub == "search":
        return _handle_search(km, args[1:])
    if sub == "semantic":
        return _handle_semantic(km, args[1:])
    if sub == "hybrid":
        return _handle_hybrid(km, args[1:])
    if sub == "add":
        return handle_add(km, args[1:])
    if sub == "domains":
        return {"domains": km.get_domains()}
    if sub == "match":
        return _handle_match(km, args[1:])
    if sub == "stale":
        return {"stale_ids": km.mark_stale_entries()}
    if sub == "gaps":
        return {"gaps": km.get_knowledge_gap_report()}
    if sub == "migrate":
        return {"migrated": km.migrate_legacy_log()}
    if sub == "import":
        return handle_import(km, args[1:])
    if sub == "learn":
        return handle_learn(km, args[1:])
    if sub == "similar":
        return _handle_similar(km, args[1:])
    if sub == "usage":
        return _handle_usage(km, args[1:])
    if sub == "teach":
        return handle_teach(km, args[1:])
    if sub == "categories":
        return _handle_categories()
    if sub == "health":
        return _handle_health(km)
    if sub == "share":
        return handle_share(km, args[1:])
    if sub == "backup":
        return _handle_backup(km)
    if sub == "conflicts":
        return _handle_conflicts(km, args[1:])
    if sub == "choose":
        return _handle_choose(km, args[1:])
    if sub == "list":
        return _handle_list(km, args[1:])
    if sub == "get":
        return _handle_get(km, args[1:])
    if sub == "delete":
        return _handle_delete(km, args[1:])
    if sub == "maintenance":
        return _handle_maintenance(km, args[1:])
    if sub == "benchmark":
        return handle_benchmark(km, args[1:])
    if sub == "pending":
        from kanban_framework.cli.knowledge_cmd import handle_pending
        return handle_pending(km)
    if sub == "approve":
        from kanban_framework.cli.knowledge_cmd import handle_approve
        return handle_approve(km, args[1:])
    if sub == "reject":
        from kanban_framework.cli.knowledge_cmd import handle_reject
        return handle_reject(km, args[1:])
    return {"subcommand": sub, "results": []}


# ── Shared helpers ────────────────────────────────────────────────────────

def _summary_only(args: list[str]) -> tuple[list[str], bool]:
    filtered = [a for a in args if a != "--summary-only"]
    return filtered, len(filtered) < len(args)


# ── Query handlers (remain in this file) ──────────────────────────────────

def _handle_search(km: KnowledgeManager, args: list[str]) -> dict:
    args, summary_only = _summary_only(args)
    keyword_parts = []
    domain = None
    tag = None
    task_id = None
    intent = None
    i = 0
    while i < len(args):
        if args[i] == "--domain" and i + 1 < len(args):
            domain = args[i + 1]; i += 2
        elif args[i] == "--tag" and i + 1 < len(args):
            tag = args[i + 1]; i += 2
        elif args[i] == "--task" and i + 1 < len(args):
            task_id = args[i + 1]; i += 2
        elif args[i] == "--intent" and i + 1 < len(args):
            intent = args[i + 1]; i += 2
        else:
            keyword_parts.append(args[i]); i += 1

    keyword = " ".join(keyword_parts) if keyword_parts else ""

    if task_id:
        results = km.search_by_task(task_id)
    elif tag:
        results = km.search_by_tag(tag)
    elif intent and keyword:
        results = km.search_by_intent(intent, keyword, domain=domain)
    elif keyword:
        results = km.search_hybrid(keyword)
    else:
        results = km.list_entries(limit=20)

    if domain and not task_id:
        results = [r for r in results if r.get("domain") == domain]

    return {
        "keyword": keyword, "domain": domain, "tag": tag,
        "task_id": task_id, "intent": intent,
        "results": _strip_heavy_fields(results) if summary_only else results,
        "count": len(results), "summary": _build_summary(results),
        "summary_only": summary_only,
    }


def _handle_semantic(km: KnowledgeManager, args: list[str]) -> dict:
    args, summary_only = _summary_only(args)
    query = " ".join(args) if args else ""
    if not query:
        return {"error": "semantic search requires a query"}
    results = km.search_semantic(query)
    return {"query": query, "count": len(results),
            "results": _strip_heavy_fields(results) if summary_only else results,
            "summary": _build_summary(results), "summary_only": summary_only}


def _handle_hybrid(km: KnowledgeManager, args: list[str]) -> dict:
    args, summary_only = _summary_only(args)
    query = " ".join(args) if args else ""
    if not query:
        return {"error": "hybrid search requires a query"}
    results = km.search_hybrid(query)
    results = [r for r in results if float(r.get("relevance") or r.get("score", 0)) >= 0.1]
    return {"query": query, "count": len(results),
            "results": _strip_heavy_fields(results) if summary_only else results,
            "summary": _build_summary(results), "summary_only": summary_only}


def _handle_match(km: KnowledgeManager, args: list[str]) -> dict:
    text = " ".join(args) if args else ""
    if not text:
        return {"error": "match requires text argument"}
    results = km._search_fts(text, limit=20)
    return {
        "query": text,
        "matched_domains": km.match_domain(text),
        "results": _strip_heavy_fields(results),
        "count": len(results),
    }


def _handle_list(km: KnowledgeManager, args: list[str]) -> dict:
    args, summary_only = _summary_only(args)
    domain = None
    category = None
    status = "active"
    i = 0
    while i < len(args):
        if args[i] == "--domain" and i + 1 < len(args):
            domain = args[i + 1]; i += 2
        elif args[i] == "--category" and i + 1 < len(args):
            category = args[i + 1]; i += 2
        elif args[i] == "--status" and i + 1 < len(args):
            status = args[i + 1]; i += 2
        else:
            i += 1
    results = km.list_entries(domain=domain, category=category, status=status)
    return {
        "domain": domain, "category": category, "status": status,
        "results": _strip_heavy_fields(results) if summary_only else results,
        "count": len(results), "summary": _build_summary(results),
        "summary_only": summary_only,
    }


def _handle_get(km: KnowledgeManager, args: list[str]) -> dict:
    entry_id = args[0] if args else ""
    if not entry_id:
        return {"error": "entry ID required (e.g. K001)"}
    entry = km.get_entry(entry_id)
    if entry is None:
        return {"error": f"entry {entry_id} not found"}
    try:
        task_id = ""
        for a in args[1:]:
            if a.startswith("--task-id="):
                task_id = a.split("=", 1)[1]
                break
        if not task_id:
            for i, a in enumerate(args):
                if a == "--task-id" and i + 1 < len(args):
                    task_id = args[i + 1]
                    break
        if task_id:
            km.record_usage(entry_id, task_id)
    except Exception:
        pass
    return {"entry": entry}


def _handle_delete(km: KnowledgeManager, args: list[str]) -> dict:
    entry_id = args[0] if args else ""
    if not entry_id:
        return {"error": "entry ID required (e.g. K001)"}
    entry = km.get_entry(entry_id)
    if entry is None:
        return {"error": f"entry {entry_id} not found"}
    km.delete_entry(entry_id)
    return {"deleted": entry_id, "title": entry.get("title", "")}


def _handle_similar(km: KnowledgeManager, args: list[str]) -> dict:
    tags: list[str] = []
    i = 0
    while i < len(args):
        if args[i] == "--tags" and i + 1 < len(args):
            tags = args[i + 1].split(","); i += 2
        else:
            i += 1
    results = km.find_similar_pitfalls(tags)
    return {"tags": tags, "similar": results, "count": len(results)}


def _handle_usage(km: KnowledgeManager, args: list[str]) -> dict:
    entry_id = ""
    task_id = ""
    i = 0
    while i < len(args):
        if args[i] == "--entry-id" and i + 1 < len(args):
            entry_id = args[i + 1]; i += 2
        elif args[i] == "--task-id" and i + 1 < len(args):
            task_id = args[i + 1]; i += 2
        else:
            i += 1
    km.record_usage(entry_id, task_id)
    return {"entry_id": entry_id, "task_id": task_id, "recorded": True}


def _handle_categories() -> dict:
    from kanban_framework.domain.knowledge import VALID_CATEGORIES, VALID_SEVERITIES
    return {
        "categories": {k: v["desc"] for k, v in VALID_CATEGORIES.items()},
        "severities": {k: v["desc"] for k, v in VALID_SEVERITIES.items()},
    }


def _handle_health(km: KnowledgeManager) -> dict:
    from collections import Counter
    from datetime import datetime, timezone, timedelta
    from kanban_framework.cli.knowledge_ingest import _title_similarity

    entries = km.list_entries(limit=500, status="active")
    total = len(entries)
    cat_counts = Counter(e.get("category", "(uncategorized)") for e in entries)

    now = datetime.now(timezone.utc)
    week = now + timedelta(days=7)
    expired = []
    expiring_soon = []
    for e in entries:
        sa = e.get("stale_at")
        if not sa:
            continue
        try:
            stale_time = datetime.fromisoformat(sa)
            if stale_time.tzinfo is None:
                stale_time = stale_time.replace(tzinfo=timezone.utc)
            if stale_time < now:
                expired.append({"id": e["id"], "title": e.get("title", ""), "stale_at": sa})
            elif stale_time < week:
                expiring_soon.append({"id": e["id"], "title": e.get("title", ""), "stale_at": sa})
        except (ValueError, TypeError):
            pass

    duplicates = []
    for i, e1 in enumerate(entries):
        t1 = e1.get("title", "")
        if not t1:
            continue
        for e2 in entries[i + 1:]:
            t2 = e2.get("title", "")
            if not t2:
                continue
            ratio = _title_similarity(t1, t2)
            if ratio > 0.6:
                duplicates.append({
                    "pair": [e1["id"], e2["id"]], "titles": [t1, t2],
                    "similarity": round(ratio, 2),
                })

    low_quality = []
    for e in entries:
        content = (e.get("content") or "").strip()
        if not content or len(content) < 20:
            low_quality.append({"id": e["id"], "title": e.get("title", ""), "content_length": len(content)})

    type_groups: dict[str, dict] = {}
    for e in entries:
        etype = e.get("type", "knowledge")
        if etype not in type_groups:
            type_groups[etype] = {"total": 0, "refs": 0}
        type_groups[etype]["total"] += 1
        type_groups[etype]["refs"] += e.get("referenced_count", 0) or 0
    by_type = {}
    for etype, grp in type_groups.items():
        by_type[etype] = {
            "total": grp["total"],
            "avg_refs": round(grp["refs"] / grp["total"], 1) if grp["total"] else 0,
        }

    stale_ids = km.mark_stale_entries()
    gaps = km.get_knowledge_gap_report()

    benchmark_count = sum(1 for e in entries if e.get("benchmark"))
    benchmark_coverage = f"{benchmark_count / total * 100:.1f}%" if total else "0.0%"

    return {
        "total_entries": total,
        "category_distribution": dict(cat_counts.most_common()),
        "by_type": by_type,
        "expired": expired, "expiring_soon": expiring_soon,
        "duplicates": duplicates, "low_quality": low_quality,
        "stale_count": len(stale_ids), "knowledge_gaps": gaps,
        "benchmark": {"total": benchmark_count, "coverage": benchmark_coverage},
    }


def _handle_backup(km: KnowledgeManager) -> dict:
    km._auto_backup()
    bak_dir = km._db_path.parent
    _NUM_SUFFIX = re.compile(r"\.\d+$")
    backups = sorted(
        [f.name for f in bak_dir.glob("knowledge.db.bak.*")
         if _NUM_SUFFIX.search(f.name)],
        key=lambda x: int(x.rsplit(".", 1)[-1])
    )
    return {
        "backed_up": True, "db_path": str(km._db_path),
        "backup_dir": str(bak_dir), "max_backups": km.MAX_BACKUPS,
        "existing_backups": backups,
    }


def _handle_conflicts(km: KnowledgeManager, args: list[str]) -> dict:
    task_id = ""
    i = 0
    while i < len(args):
        if args[i] == "--task-id" and i + 1 < len(args):
            task_id = args[i + 1]; i += 2
        else:
            i += 1
    if not task_id:
        return {"error": "--task-id required"}
    conflicts = km.find_conflicting_solutions(task_id)
    return {"task_id": task_id, "conflicts": conflicts, "count": len(conflicts)}


def _handle_choose(km: KnowledgeManager, args: list[str]) -> dict:
    from datetime import datetime, timezone
    task_id = ""
    choice_id = ""
    selected = ""
    rationale = ""
    i = 0
    while i < len(args):
        if args[i] == "--task-id" and i + 1 < len(args):
            task_id = args[i + 1]; i += 2
        elif args[i] == "--choice-id" and i + 1 < len(args):
            choice_id = args[i + 1]; i += 2
        elif args[i] == "--selected" and i + 1 < len(args):
            selected = args[i + 1]; i += 2
        elif args[i] == "--rationale" and i + 1 < len(args):
            rationale = args[i + 1]; i += 2
        else:
            i += 1
    if not task_id or not choice_id or not selected:
        return {"error": "--task-id, --choice-id, --selected required"}

    fs = km._fs
    task_dir = fs.task_dir(task_id)
    fs.ensure_dir(task_dir)
    choices_path = task_dir / "plan_choices.json"
    import json
    choices = json.loads(choices_path.read_text(encoding="utf-8")) if choices_path.is_file() else {"choices": []}
    choice_id_int = 0
    for c in choices.get("choices", []):
        cid = c.get("choice_id", "")
        try:
            num = int(cid)
        except (ValueError, TypeError):
            num = 0
        choice_id_int = max(choice_id_int, num)
    choice_id_int += 1
    now = datetime.now(timezone.utc).isoformat()
    choices["choices"].append({
        "id": choice_id_int,
        "selected": selected,
        "rationale": rationale,
        "selected_at": now,
    })
    choices_path.write_text(json.dumps(choices, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"task_id": task_id, "choice_id": choice_id, "selected": selected, "recorded": True}


def _handle_maintenance(km: KnowledgeManager, args: list[str]) -> dict:
    from kanban_framework.domain.knowledge_management import (
        find_semantic_duplicates, scan_stale_candidates, vacuum_database,
    )

    # Parse flags
    flags = set()
    threshold = 0.85
    i = 0
    while i < len(args):
        if args[i] == "--threshold" and i + 1 < len(args):
            try:
                threshold = float(args[i + 1])
            except ValueError:
                return {"error": "--threshold requires a float (e.g. 0.85)"}
            i += 2
        elif args[i].startswith("--"):
            flags.add(args[i].lstrip("-"))
            i += 1
        else:
            i += 1

    # Default to report mode if no specific action
    has_action = flags & {"scan-duplicates", "scan-stale", "vacuum", "report"}
    if not has_action:
        flags.add("report")

    result: dict = {"action": "maintenance"}

    if "scan-duplicates" in flags or "report" in flags:
        dup_groups = find_semantic_duplicates(km, threshold=threshold)
        result["duplicates"] = {
            "threshold": threshold,
            "groups_found": len(dup_groups),
            "groups": dup_groups[:20],
        }

    if "scan-stale" in flags or "report" in flags:
        stale = scan_stale_candidates(km)
        result["stale"] = {
            "threshold_days": stale["stale_days_threshold"],
            "candidates_found": len(stale["candidates"]),
            "candidates": stale["candidates"][:20],
        }

    if "vacuum" in flags:
        vac = vacuum_database(km)
        result["vacuum"] = vac

    if "confirm" in flags:
        suggestions = []
        dup_groups = result.get("duplicates", {}).get("groups", [])
        for g in dup_groups:
            entries = g["entries"]
            suggestions.append({
                "type": "duplicate",
                "group_id": g["group_id"],
                "entries": [{"id": e["id"], "title": e["title"]} for e in entries],
                "similarity": g["max_similarity"],
                "suggested_action": "review and merge or keep_both",
            })
        stale_cands = result.get("stale", {}).get("candidates", [])
        for c in stale_cands:
            suggestions.append({
                "type": "stale",
                "id": c["id"],
                "title": c["title"],
                "days_since_reference": c["days_since_reference"],
                "referenced_count": c["referenced_count"],
                "suggested_action": "delete or reactivate",
            })
        result["suggestions"] = suggestions
        result["note"] = "Suggestions listed for human review. No automatic changes applied."

    return result
