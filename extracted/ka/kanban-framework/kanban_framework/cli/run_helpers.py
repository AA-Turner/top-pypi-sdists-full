from __future__ import annotations
import json
import time
from pathlib import Path
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config
from kanban_framework.infra.git import Git, GitError
from kanban_framework.infra.worktree import Worktree, WorktreeError
from kanban_framework.infra.scheduler import Scheduler
from kanban_framework.domain.task import TaskManager
from kanban_framework.domain.workflow import WorkflowEngine
from kanban_framework.domain.guard import Guard
from kanban_framework.types import Phase
from kanban_framework.infra.consts import Consts


_BRAINSTORMING_ELEMENTS = [
    ("技术栈选型", "tech_stack"),
    ("核心功能清单", "feature_list"),
    ("验收标准", "acceptance_criteria"),
    ("约束条件", "constraints"),
]

_KEYWORDS_MAP = {
    "tech_stack": ["技术栈", "tech stack", "使用 python", "使用 react", "使用 node", "使用 go",
                   "使用 rust", "使用 typescript", "用 python", "用 react", "用 node"],
    "feature_list": ["功能清单", "功能列表", "feature list", "包含以下", "支持以下",
                     "实现以下", "功能需求", "核心功能"],
    "acceptance_criteria": ["验收标准", "acceptance criteria", "预期行为", "shall",
                            "must", "通过标准", "验收条件"],
    "constraints": ["约束条件", "限制条件", "constraint", "代码放在", "必须放在",
                    "禁止", "不得超过", "不低于"],
}


def _validate_fsm_state(task, tm) -> dict | None:
    """Validate task's FSM state before executing CLI commands.
    Returns error dict if state is inconsistent, None if OK."""
    mode = getattr(task, 'mode', '') or Consts.DEFAULT_MODE
    workflow = tm._cfg.workflow if tm._cfg else None
    order = Scheduler.dispatch_order(
        mode=mode,
        workflow=workflow,
        kanban_dir=tm._fs.kanban_dir,
    )
    mode_label = mode
    completed_phases = {
        h["phase"] for h in task.history
        if h.get("status") == "completed"
    }
    current_phase = task.phase

    # Check if current phase is valid — allow recovery from invalid phases
    if current_phase not in order:
        # Current phase not in mode's phase order (e.g., after a mode switch
        # or a buggy complete-phase). Allow the operation to proceed so the
        # user can recover by transitioning to a valid phase.
        return None

    # Check for skipped phases before current
    current_idx = order.index(current_phase)
    for i in range(current_idx):
        if order[i].value not in completed_phases:
            return {
                "error": f"phase '{order[i].value}' was skipped (expected before '{current_phase.value}')",
                "skipped_phase": order[i].value,
                "current_phase": current_phase.value,
                "completed_phases": sorted(completed_phases),
                "fix": "kanban workflow next-step " + task.id,
            }

    return None


def _get_agents_for_phase(fs: Filesystem, phase_id: str,
                          task_description: str = "",
                          mode: str | None = None) -> list[dict]:
    cfg = Config(fs)
    workflow = cfg.workflow
    for p in workflow.get("phases", []):
        if p.get("id") == phase_id:
            agents = p.get("agents", [])
            return _apply_trigger_conditions(agents, task_description)
    if phase_id == "evaluate":
        from kanban_framework.infra.scheduler import Scheduler
        return Scheduler.eval_roles(mode=mode, kanban_dir=fs.kanban_dir)
    if phase_id == "retrospective":
        from kanban_framework.infra.scheduler import Scheduler
        return Scheduler.retrospective_roles(mode=mode)
    # Check workflow extensions for custom phase agents
    from kanban_framework.domain.workflow_extensions import WorkflowExtension
    ext = WorkflowExtension(workflow)
    custom_agents = ext.get_agents_for_phase(phase_id)
    if custom_agents is not None:
        return custom_agents
    return []


def _apply_trigger_conditions(agents: list[dict],
                               description: str) -> list[dict]:
    """Filter agents: required ones always pass; optional ones are skipped
    unless their trigger_condition keywords match the task description."""
    result = []
    for agent in agents:
        if agent.get("required", True):
            result.append(agent)
            continue
        trigger = agent.get("trigger_condition")
        if not trigger:
            continue  # optional + no trigger → skip (#116)
        keywords = trigger.get("keywords", [])
        match_field = trigger.get("match_field", "description")
        if match_field == "description" and keywords:
            desc_lower = description.lower()
            if any(kw.lower() in desc_lower for kw in keywords):
                result.append(agent)
    return result


def _track_phase_time(task_id: str, phase: str, action: str) -> None:
    """Record phase start/end time to time_tracking.json."""
    try:
        root = Filesystem.find_project_root()
        reports_dir = root / ".kanban" / "reports"
        from kanban_framework.infra.time_tracking import TimeTracker
        tracker = TimeTracker(reports_dir / "time_tracking.json")
        if action == "start":
            tracker.start_phase(task_id, phase)
        elif action == "end":
            tracker.end_phase(task_id, phase)
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        import logging
        logging.getLogger("kanban").warning("time_tracking %s/%s failed: %s", task_id, phase, exc)


def _move_to_archive(fs: Filesystem, task_id: str) -> None:
    """Move entire task directory to archive.

    Uses rename first (fast, same-filesystem), falls back to copytree+remove
    (cross-filesystem or when rename fails, e.g. Windows file locks).
    """
    import shutil
    archive_task_dir = fs.archive_dir() / task_id

    # Remove existing archive if present
    if archive_task_dir.exists():
        shutil.rmtree(archive_task_dir)

    task_dir = fs.task_dir(task_id)
    if not task_dir.exists():
        return
    fs.ensure_dir(archive_task_dir.parent)
    try:
        task_dir.rename(archive_task_dir)
    except OSError:
        # Cross-filesystem or locked files — copy then remove
        shutil.copytree(str(task_dir), str(archive_task_dir))
        shutil.rmtree(str(task_dir), ignore_errors=True)
        # Verify cleanup — remove residual files if rmtree partially failed
        if task_dir.exists():
            shutil.rmtree(str(task_dir), ignore_errors=True)


def _knowledge_health_on_archive(task_id: str) -> None:
    """Run knowledge health check on archive — mark stale, cleanup zombies, report gaps.

    Archive also migrates any task-level knowledge-log.md into DB (#166).
    Tracks knowledge effectiveness based on task evaluation scores.
    """
    try:
        root = Filesystem.find_project_root()
        fs = Filesystem(root=root)
        from kanban_framework.domain.knowledge import KnowledgeManager
        km = KnowledgeManager(fs)
        # Import task-level knowledge into DB
        migrated = km.migrate_legacy_log()
        if migrated:
            import sys
            print(f"KNOWLEDGE: {migrated} entries migrated to DB for {task_id}", file=sys.stderr)
        stale_ids = km.mark_stale_entries()
        gaps = km.get_knowledge_gap_report()
        if stale_ids:
            import sys
            print(f"KNOWLEDGE HEALTH: {len(stale_ids)} stale entries marked for {task_id}", file=sys.stderr)
        if gaps:
            import sys
            print(f"KNOWLEDGE HEALTH: knowledge gaps detected for {task_id}: {list(gaps.keys())}", file=sys.stderr)

        # Zombie cleanup: remove entries never referenced in 60+ days (#543)
        zombie_ids = km.cleanup_zombies(min_age_days=60)
        if zombie_ids:
            import sys
            print(f"KNOWLEDGE CLEANUP: {len(zombie_ids)} zombie entries removed for {task_id}", file=sys.stderr)

        # Knowledge effectiveness tracking: correlate knowledge_used.json with eval scores
        _track_knowledge_effectiveness(fs, km, task_id)

        # Skills auto-evolution: extract improvements from framework_assessment
        from kanban_framework.domain.skills import SkillManager
        sm = SkillManager(fs.kanban_dir)
        archive_dir = fs.archive_dir()
        candidates = sm.process_assessment(task_id, archive_dir)
        if candidates:
            import sys
            print(f"SKILLS EVOLUTION: {len(candidates)} candidate(s) from {task_id}", file=sys.stderr)
    except Exception as exc:
        import sys
        print(f"WARNING: knowledge health check failed for {task_id}: {exc}", file=sys.stderr)


def _track_knowledge_effectiveness(fs: Filesystem, km, task_id: str) -> None:
    """Correlate knowledge_used.json with evaluation scores and update effectiveness.

    Falls back to scanning task artifacts (spec.md, plan/*.md) for K-NNN references
    when knowledge_used.json is missing — agent doesn't always produce this file (#575).
    """
    import json as _json
    task_dir = fs.task_dir(task_id)
    ku_path = task_dir / "plan" / "knowledge_used.json"

    matched = []
    if ku_path.is_file():
        try:
            ku = _json.loads(ku_path.read_text(encoding="utf-8"))
        except Exception:
            ku = {}
        from kanban_framework.domain.guard_checks import _extract_matched_entries
        matched = _extract_matched_entries(ku)

    if not matched:
        matched = _extract_knowledge_refs_from_artifacts(fs, km, task_dir)

    if not matched:
        return

    # Get task's latest evaluation score
    avg_score = 0.0
    try:
        from kanban_framework.domain.task import TaskManager
        from kanban_framework.infra.config import Config
        cfg = Config(fs)
        tm = TaskManager(fs, cfg)
        task = tm.show(task_id)
        if task.score_history:
            latest = task.score_history[-1] if task.score_history else {}
            avg_score = latest.get("average", 0.0)
    except Exception:
        pass

    if avg_score <= 0:
        return

    for m in matched:
        eid = m.get("id", "")
        if not eid:
            continue
        try:
            km.update_effectiveness(eid, task_id, avg_score)
        except Exception:
            pass


def _extract_knowledge_refs_from_artifacts(fs, km, task_dir) -> list[dict]:
    """Scan task artifacts for K-NNN / scope-NNN references as fallback.

    Used when plan/knowledge_used.json is not produced by the agent (#575).
    Only returns IDs that actually exist in the knowledge base.
    """
    import re
    import sys

    found: set[str] = set()
    # Match K001, K042, alice001, scope-NNN patterns
    pattern = re.compile(r'\b(?:K|[a-z][a-z0-9]{0,14})(\d{3,})\b', re.IGNORECASE)

    for glob_pat in ['spec.md', 'plan/*.md', 'execution_summary.md']:
        for f in task_dir.glob(glob_pat):
            try:
                text = f.read_text(encoding='utf-8')
                for m in pattern.finditer(text):
                    found.add(m.group(0))
            except Exception:
                pass

    if not found:
        return []

    # Validate against actual KB entries
    result = []
    for ref_id in sorted(found):
        try:
            entry = km.get_entry(ref_id)
            if entry:
                result.append({"id": ref_id, "title": entry.get("title", ""), "source": "artifact_scan"})
        except Exception:
            pass

    if result:
        print(
            f"KNOWLEDGE FALLBACK: {len(result)} KB ref(s) extracted from "
            f"task artifacts for {task_dir.name} (knowledge_used.json missing)",
            file=sys.stderr,
        )
    return result


def _fmt_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.0f}s"
    m, s = divmod(int(seconds), 60)
    if m < 60:
        return f"{m}m {s}s"
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"


def _get_time_summary(task_id: str) -> dict:
    try:
        root = Filesystem.find_project_root()
        fs = Filesystem(root=root)
        from kanban_framework.infra.time_tracking import TimeTracker
        tracker = TimeTracker(fs.kanban_dir / "reports" / "time_tracking.json")
        data = tracker.report(task_id)
        phases = data.get("phases", {})
        total = data.get("total_seconds", 0)
        return {
            "total_seconds": round(total, 1),
            "total_human": _fmt_duration(total),
            "phases": {
                name: {
                    "elapsed_seconds": round(info.get("elapsed_seconds", 0), 1),
                    "elapsed_human": _fmt_duration(info.get("elapsed_seconds", 0)),
                }
                for name, info in sorted(phases.items())
            },
        }
    except Exception:
        return {"total_seconds": 0, "total_human": "unknown", "phases": {}}


def _append_time_to_retrospective(task_id: str) -> None:
    """Append time consumption summary to retrospective.md at archive time.

    Called during archive as a safety net — the knowledge-manager agent should
    already include this data, but this ensures it's always present.
    """
    try:
        root = Filesystem.find_project_root()
        fs = Filesystem(root=root)
        retro_path = fs.archive_dir() / task_id / "retrospective.md"
        # Also check task dir (before move) if archive doesn't have it yet
        if not retro_path.is_file():
            retro_path = fs.task_dir(task_id) / "retrospective.md"
        if not retro_path.is_file():
            return

        from kanban_framework.infra.time_tracking import TimeTracker
        import os

        reports_dir = fs.kanban_dir / "reports"
        time_tracker = TimeTracker(reports_dir / "time_tracking.json")

        time_data = time_tracker.report(task_id)

        existing = retro_path.read_text(encoding="utf-8")

        # Skip if time section already exists
        if "## 时间消耗" in existing:
            return

        lines = []
        # Time section
        total_seconds = time_data.get("total_seconds", 0)
        phases = time_data.get("phases", {})
        if total_seconds > 0:
            lines.append("\n## 时间消耗")
            lines.append("| 阶段 | 耗时 |")
            lines.append("|------|------|")
            for phase_name, info in sorted(phases.items()):
                elapsed = info.get("elapsed_seconds", 0)
                lines.append(f"| {phase_name} | {_fmt_duration(elapsed)} |")
            lines.append(f"\n- **总计**: {_fmt_duration(total_seconds)}")

        if lines:
            retro_path.write_text(existing + "\n".join(lines) + "\n", encoding="utf-8")
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        import logging
        logging.getLogger("kanban").warning("retrospective time append failed: %s", exc)


def _collect_iteration_artifacts(fs: Filesystem, task_id: str) -> dict:
    """Collect execution artifacts from all iteration directories for archive summarization.

    Returns a dict mapping artifact names to lists of (iteration, content) pairs.
    The orchestrator uses this to LLM-summarize across all iterations.
    """
    task = TaskManager(fs, Config(fs)).show(task_id)
    artifacts = {}
    for it in range(1, task.iteration + 1):
        it_dir = fs.iteration_dir(task_id, it)
        if not it_dir.exists():
            continue
        for fname in ["execution_summary.md", "execution_pitfalls.md", "execution_decisions.md"]:
            fpath = it_dir / fname
            if fs.file_exists(fpath):
                artifacts.setdefault(fname, []).append({
                    "iteration": it,
                    "path": str(fpath),
                    "content": fpath.read_text(encoding="utf-8"),
                })
    return artifacts


def _check_brainstorming_gate(description: str, workflow: dict | None = None, mode: str | None = None,
                               kanban_dir: Path | None = None) -> dict:
    """IR-16: Check if task description has all 4 required elements for pass-through.

    Configurable via:
      modes.<mode>.gates.brainstorming: false — disable gate for this mode
      workflow.gates.brainstorming.enabled: false — disable gate globally
      .kanban/workflows/<mode>.json gates.brainstorming: false — per-file config
    """
    # Check if brainstorming gate is disabled via config
    if workflow and isinstance(workflow, dict):
        if mode:
            mode_cfg = workflow.get("modes", {}).get(mode, {}) if isinstance(workflow.get("modes"), dict) else {}
            mode_gates = mode_cfg.get("gates", {}) if isinstance(mode_cfg, dict) else {}
            if isinstance(mode_gates, dict) and mode_gates.get("brainstorming") is False:
                return {"passed": True, "skipped": "disabled in mode config"}
        top_gates = workflow.get("gates", {})
        if isinstance(top_gates, dict) and top_gates.get("brainstorming", {}).get("enabled") is False:
            return {"passed": True, "skipped": "disabled in workflow config"}
    # Check directory workflow files
    if mode and kanban_dir:
        try:
            from kanban_framework.domain.workflow_loader import merge_workflow_modes
            dir_modes = merge_workflow_modes(workflow or {}, kanban_dir)
            if mode in dir_modes:
                g = dir_modes[mode].get("gates", {})
                if isinstance(g, dict) and g.get("brainstorming") is False:
                    return {"passed": True, "skipped": "disabled in workflow file"}
        except Exception:
            pass
    # Default: perform the hardcoded check
    desc = (description or "").strip()
    if not desc:
        return {
            "passed": False,
            "missing": [{"label": l, "key": k} for l, k in _BRAINSTORMING_ELEMENTS],
            "hint": "task description 为空。请在 task.json 中补充 description，"
                    "包含技术栈、功能清单、验收标准、约束条件，或执行 brainstorming step。",
        }
    desc_lower = desc.lower()
    missing = []
    for label, key in _BRAINSTORMING_ELEMENTS:
        if not any(kw in desc_lower for kw in _KEYWORDS_MAP[key]):
            missing.append({"label": label, "key": key})
    return {"passed": len(missing) == 0, "missing": missing}


def _resolve() -> tuple[Filesystem, Config, TaskManager, WorkflowEngine]:
    root = Filesystem.find_project_root()
    fs = Filesystem(root=root)
    cfg = Config(fs)
    tm = TaskManager(fs, cfg)
    guard = Guard(fs, cfg)
    we = WorkflowEngine(fs, cfg, guard=guard)
    return fs, cfg, tm, we


def _resolve_worktree() -> tuple[Git, Worktree]:
    root = Filesystem.find_project_root()
    fs = Filesystem(root=root)
    cfg = Config(fs)
    g = Git(repo_root=root)
    wt_base = cfg.worktree_base_dir
    wt = Worktree(git=g, repo_root=root, worktree_base=wt_base)
    return g, wt

