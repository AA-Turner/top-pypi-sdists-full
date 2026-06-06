"""Knowledge share/sync management — push/pull to shared DB."""
from __future__ import annotations

from kanban_framework.domain.knowledge import KnowledgeManager


def handle_share(km: KnowledgeManager, args: list[str]) -> dict:
    if not args:
        return {"error": "usage: kanban knowledge share --init <path> | --status | --list | --push"}

    if args[0] == "--init":
        target = args[1] if len(args) > 1 else None
        if not target:
            return {"error": "path required: kanban knowledge share --init <path>"}
        from kanban_framework.domain.knowledge_backend import ShareBackend
        result = ShareBackend.init_db(target)
        if result.get("error"):
            return result
        try:
            import json
            cfg_path = km._fs.config_file()
            if cfg_path.is_file():
                cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
                kb_cfg = cfg.setdefault("knowledge", {})
                share_cfg = kb_cfg.setdefault("share", {})
                share_cfg["enabled"] = True
                share_cfg["path"] = target
                cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
                result["config_updated"] = True
        except Exception:
            pass
        return result

    if args[0] == "--status":
        backend = getattr(km, '_backend', None)
        if hasattr(backend, '_secondary') and backend._secondary is not None:
            return {"share_enabled": True, "type": type(backend._secondary).__name__}
        return {"share_enabled": False}

    if args[0] == "--list":
        share_be = _get_share_backend(km)
        if isinstance(share_be, dict):
            return share_be
        list_domain = None
        i = 1
        while i < len(args):
            if args[i] == "--domain" and i + 1 < len(args):
                list_domain = args[i + 1]; i += 2
            else:
                i += 1
        entries = share_be.list_entries(domain=list_domain)
        for e in entries:
            local = km.list_entries(domain=e.get("domain", ""))
            titles = {x.get("title", "").strip() for x in local}
            e["local_exists"] = e.get("title", "").strip() in titles
        return {"entries": entries, "count": len(entries)}

    if args[0] == "--push":
        share_be = _get_share_backend(km)
        if isinstance(share_be, dict):
            return share_be
        force = "--force" in args
        if "--all" in args:
            filters = parse_push_filters(args)
            entries = km.list_entries(status="active")
            filtered = apply_push_filters(entries, filters)
            if filters.get("dry_run"):
                return {"dry_run": True, "would_push": len(filtered), "entries": [
                    {"id": e.get("id"), "title": e.get("title"), "domain": e.get("domain")}
                    for e in filtered
                ]}
            pushed = 0
            skipped = 0
            conflicts = 0
            errors = 0
            for e in filtered:
                try:
                    r = share_be.add_entry(force=force, **e)
                    if r.get("merged"):
                        skipped += 1
                    elif r.get("status") == "conflict":
                        conflicts += 1
                    else:
                        pushed += 1
                except Exception:
                    errors += 1
            return {"pushed": pushed, "skipped": skipped, "conflicts": conflicts,
                    "errors": errors, "total": len(filtered)}
        else:
            entry_id = args[1] if len(args) > 1 else ""
            if not entry_id:
                return {"error": "entry_id required"}
            entry = km.get_entry(entry_id)
            if entry is None:
                return {"error": f"entry {entry_id} not found"}
            result = share_be.add_entry(force=force, **entry)
            return result

    if args[0] == "--resolve":
        share_be = _get_share_backend(km)
        if isinstance(share_be, dict):
            return share_be
        resolve_args = args[1:]
        if len(resolve_args) < 2:
            return {"error": "usage: kanban knowledge share --resolve <existing_id> <action> [--content-file <path>]\n"
                             "  actions: keep_existing, keep_incoming, merge_both, skip"}
        existing_id = resolve_args[0]
        action = resolve_args[1]
        merged_content = None
        for i, a in enumerate(resolve_args):
            if a == "--content-file" and i + 1 < len(resolve_args):
                from pathlib import Path
                cf = Path(resolve_args[i + 1])
                if cf.is_file():
                    merged_content = cf.read_text(encoding="utf-8")
                else:
                    return {"error": f"content file not found: {cf}"}
        try:
            return share_be.resolve_conflict(existing_id, action, merged_content=merged_content)
        except ValueError as e:
            return {"error": str(e)}

    return {"error": f"unknown option: {args[0]}"}


def _get_share_backend(km: KnowledgeManager):
    backend = getattr(km, '_backend', None)
    if hasattr(backend, '_secondary'):
        return backend._secondary
    return {"error": "Share not configured. Set knowledge.share.enabled=true and knowledge.share.path in config.json"}


def parse_push_filters(args: list[str]) -> dict:
    filters = {}
    i = 0
    while i < len(args):
        if args[i] == "--domain" and i + 1 < len(args):
            filters["domain"] = args[i + 1]; i += 2
        elif args[i] == "--category" and i + 1 < len(args):
            filters["category"] = args[i + 1]; i += 2
        elif args[i] == "--severity" and i + 1 < len(args):
            filters["severity"] = args[i + 1]; i += 2
        elif args[i] == "--since" and i + 1 < len(args):
            filters["since"] = args[i + 1]; i += 2
        elif args[i] == "--biz" and i + 1 < len(args):
            filters.setdefault("biz_list", []).append(args[i + 1]); i += 2
        elif args[i] == "--dry-run":
            filters["dry_run"] = True; i += 1
        else:
            i += 1
    return filters


def apply_push_filters(entries: list[dict], filters: dict) -> list[dict]:
    result = entries
    if "domain" in filters:
        result = [e for e in result if e.get("domain") == filters["domain"]]
    if "category" in filters:
        result = [e for e in result if e.get("category") == filters["category"]]
    if "severity" in filters:
        result = [e for e in result if e.get("severity") == filters["severity"]]
    if "biz_list" in filters:
        result = [e for e in result if e.get("biz_context", "") in filters["biz_list"]]
    if "since" in filters:
        from datetime import datetime
        try:
            since = datetime.fromisoformat(filters["since"])
            filtered = []
            for e in result:
                try:
                    created = datetime.fromisoformat(e.get("created_at", "").replace("Z", "+00:00"))
                    if created >= since:
                        filtered.append(e)
                except (ValueError, TypeError):
                    pass
            result = filtered
        except ValueError:
            pass
    return result
