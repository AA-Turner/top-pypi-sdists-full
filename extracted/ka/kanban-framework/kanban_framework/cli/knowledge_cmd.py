"""Knowledge review commands — pending, approve, reject, validate-pending."""
from __future__ import annotations
from kanban_framework.domain.knowledge import KnowledgeManager


def handle_pending(km: KnowledgeManager) -> dict:
    """List all pending knowledge entries awaiting review."""
    result = km.list_entries(status="pending")
    return {"results": result, "count": len(result), "pending": result}


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


def handle_validate_pending(km: KnowledgeManager, args: list[str]) -> dict:
    """Validate all pending knowledge entries via benchmark.

    One-command flow:
      1. List pending entries
      2. Generate benchmark case for each
      3. Assemble suite and run benchmark
      4. Report: which entries passed/failed, suggest approve/reject

    Usage:
      kanban knowledge validate-pending             # dry-run: list + generate only
      kanban knowledge validate-pending --run        # create tasks + run benchmark
    """
    import json as _json
    import tempfile
    from pathlib import Path
    from kanban_framework.cli.knowledge_ingest import _generate_benchmark_case

    pending = km.list_entries(status="pending")
    if not pending:
        return {
            "validated": 0,
            "message": "No pending entries to validate. "
                       "Entries are added via evaluate.capture_knowledge step or "
                       "`kanban knowledge add --status pending`.",
        }

    dry_run = "--run" not in args

    # Generate benchmark cases from pending entries
    cases = []
    for entry in pending:
        case_yaml = _generate_benchmark_case(entry, "")
        cases.append({
            "entry_id": entry["id"],
            "title": entry.get("title", ""),
            "domain": entry.get("domain", ""),
            "category": entry.get("category", ""),
            "case_yaml": case_yaml.get("yaml", ""),
        })

    if dry_run:
        return {
            "validated": 0,
            "pending_count": len(pending),
            "cases": cases,
            "message": (
                f"Found {len(pending)} pending entries. "
                f"Run with --run to execute benchmark validation."
            ),
            "next": "kanban knowledge validate-pending --run",
        }

    # --run: execute benchmark
    yaml_content = "mode: lightweight\n\ncases:\n"
    for c in cases:
        # Extract just the case YAML block (skip "cases:" header)
        yaml_content += c["case_yaml"].replace("cases:\n", "")

    suite_path = Path(tempfile.mktemp(suffix="_validate.yml"))
    suite_path.write_text(yaml_content, encoding="utf-8")

    from kanban_framework.domain.benchmark_runner import BenchmarkRunner
    runner = BenchmarkRunner()
    report = runner.execute(suite_path)

    # Map benchmark results back to pending entries
    results = []
    for c in report.get("cases", []):
        entry_id = c["id"].replace("verify_", "")
        verdict = c.get("verdict", "error")
        score = c.get("score", 0)
        suggested = (
            "approve" if verdict == "pass" and score >= 8.0
            else "review" if verdict == "pass" and score >= 6.0
            else "reject"
        )
        results.append({
            "entry_id": entry_id,
            "verdict": verdict,
            "score": score,
            "suggested_action": suggested,
            "dimensions": c.get("dimensions", {}),
        })

    try:
        suite_path.unlink()
    except Exception:
        pass

    return {
        "validated": len(results),
        "results": results,
        "summary": {
            "approve": sum(1 for r in results if r["suggested_action"] == "approve"),
            "review": sum(1 for r in results if r["suggested_action"] == "review"),
            "reject": sum(1 for r in results if r["suggested_action"] == "reject"),
        },
        "next": (
            "Review results above. To approve: kanban knowledge approve <id>.\n"
            "To re-run validation: kanban knowledge validate-pending --run"
        ),
    }
