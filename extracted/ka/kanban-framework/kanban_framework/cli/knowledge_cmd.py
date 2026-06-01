"""Knowledge review commands — pending, approve, reject."""
from __future__ import annotations
from kanban_framework.domain.knowledge import KnowledgeManager


def handle_pending(km: KnowledgeManager) -> dict:
    """List all pending knowledge entries awaiting review."""
    result = km.list_entries(status="pending")
    return {"pending": result, "count": len(result)}


def handle_approve(km: KnowledgeManager, args: list[str]) -> dict:
    """Approve pending knowledge entries. --all or <id> [<id> ...]."""
    if "--all" in args:
        pending = km.list_entries(status="pending")
        ids = [e["id"] for e in pending]
    else:
        ids = [a for a in args if not a.startswith("--")]
    approved = []
    for eid in ids:
        try:
            km.update_entry(eid, status="active")
            approved.append(eid)
        except Exception:
            pass
    return {"approved": approved, "count": len(approved)}


def handle_reject(km: KnowledgeManager, args: list[str]) -> dict:
    """Reject pending knowledge entries. --all or <id> [<id> ...]."""
    if "--all" in args:
        pending = km.list_entries(status="pending")
        ids = [e["id"] for e in pending]
    else:
        ids = [a for a in args if not a.startswith("--")]
    rejected = []
    for eid in ids:
        try:
            km.update_entry(eid, status="rejected")
            rejected.append(eid)
        except Exception:
            pass
    return {"rejected": rejected, "count": len(rejected)}
