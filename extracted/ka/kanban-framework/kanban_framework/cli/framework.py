from __future__ import annotations
from pathlib import Path
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config


def dispatch(args: list[str]) -> dict:
    sub = args[0] if args else "assess"
    if sub == "assess":
        task_id = args[1] if len(args) > 1 else None
        return cmd_assess(task_id)
    return {"subcommand": sub}


def cmd_assess(task_id: str | None = None) -> dict:
    root = Filesystem.find_project_root()
    fs = Filesystem(root=root)
    cfg = Config(fs)

    results = {
        "iron_rules": _assess_iron_rules(fs),
        "agent_coverage": _assess_agent_coverage(cfg),
        "artifacts": {},
    }
    if task_id:
        results["artifacts"] = _assess_task_artifacts(fs, task_id)
    results["overall_score"] = _calc_score(results)
    return results


def _assess_iron_rules(fs: Filesystem) -> dict:
    rules_dir = fs.kanban_dir.parent / ".claude" / "skills" / "kanban" / "rules"
    if not rules_dir.exists():
        rules_dir = fs.kanban_dir.parent / ".claude" / "rules"
    rule_files = list(rules_dir.glob("*.md")) if rules_dir.exists() else []
    defined = len(rule_files)
    expected = 8  # R-001 through R-008
    return {
        "rules_defined": defined,
        "rules_expected": expected,
        "coverage": min(defined / expected, 1.0) if expected else 1.0,
    }


def _assess_agent_coverage(cfg: Config) -> dict:
    workflow = cfg.workflow
    phases = workflow.get("phases", [])
    covered_phases = 0
    roles = set()
    for p in phases:
        agents = p.get("agents", [])
        if agents:
            covered_phases += 1
            for a in agents:
                roles.add(a.get("role", ""))
    total_phases = len(phases)
    return {
        "phases_with_agents": covered_phases,
        "total_phases": total_phases,
        "coverage": covered_phases / total_phases if total_phases else 1.0,
        "unique_roles": sorted(roles),
    }


def _assess_task_artifacts(fs: Filesystem, task_id: str) -> dict:
    task_dir = fs.task_dir(task_id)
    expected = [
        "spec.md", "plan.md", "task_breakdown.json",
        "execution_summary.md", "execution_pitfalls.md",
        "execution_decisions.md", "retrospective.md", "acceptance.md",
    ]
    present = []
    missing = []
    for fname in expected:
        if (task_dir / fname).exists():
            present.append(fname)
        else:
            missing.append(fname)
    return {
        "present": present,
        "missing": missing,
        "completeness": len(present) / len(expected) if expected else 1.0,
    }


def _calc_score(results: dict) -> float:
    scores = []
    if "iron_rules" in results:
        scores.append(results["iron_rules"].get("coverage", 0))
    if "agent_coverage" in results:
        scores.append(results["agent_coverage"].get("coverage", 0))
    if results.get("artifacts"):
        scores.append(results["artifacts"].get("completeness", 0))
    return round(sum(scores) / len(scores) * 10, 1) if scores else 0.0
