"""Task CLI — init, status, show, clean, promote commands.

Heavy modules extracted:
- task_utils.py: shared helpers (_resolve, _serialize_report, deps, scope, scan)
- task_create.py: cmd_create, _recommend_worktree
- task_edit.py: cmd_task, _cmd_task_edit, _handle_skip_to
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path

from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config
from kanban_framework.domain.task import TaskManager, TaskNotFoundError
from kanban_framework.domain.scanner import scan_project, ScanReport
from kanban_framework.infra.scheduler import Scheduler

# Re-export from extracted modules for backward compatibility
from kanban_framework.cli.task_utils import (  # noqa: F401
    _resolve,
    _serialize_report,
    _check_kb_deps,
    _install_hint,
    _install_superpowers_skills,
    _compute_default_scope,
    _prompt_scope,
    cmd_scan,
    cmd_install_codeburn,
)
from kanban_framework.cli.task_create import cmd_create, _recommend_worktree  # noqa: F401
from kanban_framework.cli.task_edit import (  # noqa: F401
    cmd_task,
    _cmd_task_edit,
    _handle_skip_to,
)


def cmd_init(args: list[str]) -> dict:
    clean_orphaned = "--clean-orphaned" in args
    apply_updates = "--apply" in args
    force_skills = "--force-skills" in args
    non_interactive = "--non-interactive" in args or "--json" in args

    fs, _, _ = _resolve()
    root = Filesystem.find_project_root()

    # Ensure .kanban/ directory structure exists (fix #80)
    required_dirs = [
        fs.kanban_dir,
        fs.kanban_dir / "tasks",
        fs.kanban_dir / "archive",
        fs.kanban_dir / "inbox",
        fs.kanban_dir / "reports",
        fs.kanban_dir / "dashboard",
        fs.kanban_dir / "skills" / "evolved",
        fs.kanban_dir / "workflows",
        fs.kanban_dir / "log",
    ]
    created = []
    for d in required_dirs:
        if not d.exists():
            d.mkdir(parents=True)
            created.append(str(d.relative_to(root)))

    # Copy workflow presets (overwrite to ensure latest version)
    workflows_dir = fs.kanban_dir / "workflows"
    from kanban_framework.infra.filesystem import Filesystem as FS
    skill_src = FS.find_skill_dir()
    # Prefer package workflows/ dir, fall back to skill_src/workflows/
    for preset_src in (Path(__file__).resolve().parent.parent / "workflows",
                       skill_src / "workflows"):
        if preset_src.is_dir():
            copied_one = False
            for preset_file in preset_src.glob("*.json"):
                dst = workflows_dir / preset_file.name
                content = preset_file.read_text(encoding="utf-8")
                if len(content) < 512:  # Skip placeholder files
                    continue
                dst.write_text(content, encoding="utf-8")
                created.append(f"workflows/{preset_file.name}")
                copied_one = True
            if copied_one:
                break

    # Sync skill files: copy entire _skill/ directory to .claude/skills/kanban/
    import shutil
    skill_dst = root / ".claude" / "skills" / "kanban"
    updated: list[str] = []
    added: list[str] = []
    stale: list[str] = []
    pending_updates: list[str] = []
    sync_errors: list[str] = []

    if force_skills and skill_dst.exists():
        shutil.rmtree(str(skill_dst))
        stale.append(str(skill_dst.relative_to(root)))

    try:
        if not skill_dst.exists():
            shutil.copytree(str(skill_src), str(skill_dst),
                            ignore=shutil.ignore_patterns("versions", "templates", "__pycache__", "*.pyc", "__init__.py"))
            added.append(str(skill_dst.relative_to(root)))
        elif apply_updates:
            # Update existing: copy text files, overwriting (skip binary/generated)
            _skip_parts = {"versions", "__pycache__", ".git"}
            _text_suffixes = {".md", ".json", ".py", ".txt", ".yml", ".yaml", ".toml", ".cfg", ".ini", ".css", ".js", ".ts", ".html", ".svg", ".csv"}
            for src_file in skill_src.rglob("*"):
                if src_file.is_file() and _skip_parts.isdisjoint(src_file.parts) and src_file.suffix in _text_suffixes:
                    rel_p = src_file.relative_to(skill_src)
                    dst_file = skill_dst / rel_p
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    dst_file.write_text(src_file.read_text(encoding="utf-8"), encoding="utf-8")
            updated.append(str(skill_dst.relative_to(root)))
        else:
            pending_updates.append(str(skill_dst.relative_to(root)))
    except Exception as exc:
        sync_errors.append(f"{skill_dst.relative_to(root)}: {exc}")

    # Sync templates (config.json, workflow.json) from _skill/templates/
    tmpl_src = skill_src / "templates"
    tmpl_dst = fs.kanban_dir
    if tmpl_src.is_dir():
        for tf in tmpl_src.glob("*.json"):
            dst = tmpl_dst / tf.name
            if tf.name == "config.json" and dst.exists():
                continue
            try:
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_text(tf.read_text(encoding="utf-8"), encoding="utf-8")
                added.append(f"config/{tf.name}")
            except Exception as exc:
                sync_errors.append(f"{tf.name}: {exc}")

    # Sync agents/ to .claude/agents/ so kanban-* agents are available
    agents_src = skill_src / "agents"
    agents_dst = root / ".claude" / "agents"
    agents_synced: list[str] = []
    if agents_src.is_dir():
        try:
            agents_dst.mkdir(parents=True, exist_ok=True)
            for af in agents_src.glob("*.md"):
                dst = agents_dst / af.name
                if not dst.is_file() or dst.read_text(encoding="utf-8") != af.read_text(encoding="utf-8"):
                    dst.write_text(af.read_text(encoding="utf-8"), encoding="utf-8")
                    agents_synced.append(af.name)
        except Exception as exc:
            sync_errors.append(f"agents sync: {exc}")

    # Agent conflicts detection
    # Post-sync validation: SKILL.md must exist after init
    if not (skill_dst / "SKILL.md").is_file():
        return {
            "initialized": False,
            "project_root": str(root),
            "error": (
                f"skill 目录同步失败：{skill_dst}/SKILL.md 未创建。\n"
                f"skill_src={skill_src}\n"
                f"sync_errors={sync_errors}\n"
                "请尝试: pip install --force-reinstall kanban-framework"
            ),
        }

    result: dict = {
        "initialized": True,
        "project_root": str(root),
        "created_dirs": created,
        "synced_files": {
            "added": added,
            "updated": updated,
            "pending_updates": pending_updates,
            "stale_cleaned": stale,
            "errors": sync_errors,
        },
        "agents_synced": agents_synced,
    }

    # Scope setup (interactive unless --json)
    cfg_path = fs.config_file()
    if cfg_path.is_file():
        cfg_data = json.loads(cfg_path.read_text(encoding="utf-8"))
    else:
        cfg_data = {}
    kb_cfg = cfg_data.get("knowledge", {})
    current_scope = kb_cfg.get("scope", "")

    if not current_scope and not non_interactive:
        default = _compute_default_scope()
        scope = _prompt_scope(default)
        kb_cfg["scope"] = scope
        cfg_data["knowledge"] = kb_cfg
        # Sync task_id_base from worker ID numeric part
        from kanban_framework.cli.task_utils import extract_task_base
        task_base = extract_task_base(scope)
        if task_base and not cfg_data.get("task_id_base"):
            cfg_data["task_id_base"] = task_base
        cfg_path.write_text(json.dumps(cfg_data, indent=2, ensure_ascii=False), encoding="utf-8")
        result["scope_set"] = scope
        if task_base:
            result["task_id_base"] = task_base
    elif not current_scope and non_interactive:
        default = _compute_default_scope()
        kb_cfg["scope"] = default
        cfg_data["knowledge"] = kb_cfg
        from kanban_framework.cli.task_utils import extract_task_base
        task_base = extract_task_base(default)
        if task_base and not cfg_data.get("task_id_base"):
            cfg_data["task_id_base"] = task_base
        cfg_path.write_text(json.dumps(cfg_data, indent=2, ensure_ascii=False), encoding="utf-8")
        result["scope_set"] = default
    else:
        result["scope_set"] = current_scope

    # Project scan
    report = scan_project(root)
    result["scan"] = _serialize_report(report)

    # Detect E2E test recommendation for orchestrator display
    if report is not None:
        from kanban_framework.domain.scanner import detect_e2e_recommendation
        e2e_rec = detect_e2e_recommendation(report.language, root)
        result["test_strategy"] = {
            "e2e_enabled": True,
            "e2e_tool": e2e_rec["e2e_tool"],
            "e2e_target": e2e_rec["test_target"],
        }

    # Auto-install superpowers skills if gaps detected
    if report.skill_gaps:
        skill_result = _install_superpowers_skills(root, report.skill_gaps)
        result["superpowers_install"] = skill_result

    # Check if .kanban/ is globally gitignored (blocks phase checkpoints)
    gitignore_path = root / ".gitignore"
    if gitignore_path.exists():
        lines = gitignore_path.read_text(encoding="utf-8").splitlines()
        for line in lines:
            if line.strip() == ".kanban/":
                result["gitignore_warning"] = (
                    ".gitignore 中 '.kanban/' 排除了整个目录，task 数据无法 git 追踪。"
                    "建议改为只排除运行时目录: .kanban/dashboard/ .kanban/reports/ .kanban/skills/"
                )
                break

    # Suggest SessionStart hook for auto kanban context
    settings_path = root / ".claude" / "settings.json"
    hook_configured = False
    if settings_path.exists():
        try:
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
            hooks = settings.get("hooks", {})
            for h in hooks.get("SessionStart", []):
                if "kanban hook" in h.get("command", ""):
                    hook_configured = True
                    break
        except Exception:
            pass
    if not hook_configured:
        result["hook_suggestion"] = {
            "message": "建议配置 SessionStart hook，在每次会话启动时自动注入 kanban 任务上下文",
            "command": "kanban hook install",
            "description": "运行后 .claude/settings.json 会自动添加 hook，之后每次新会话模型都能看到当前任务状态",
        }

    # Add version and date info
    result["version"] = os.environ.get("KANBAN_VERSION", "dev")
    result["date"] = str(date.today())

    result["kb_deps"] = _check_kb_deps()

    # KB seed guide: suggest knowledge entries based on project structure
    result["kb_seed_guide"] = {"suggestions": [], "hint": "Run: kanban knowledge add --demo"}

    return result


# ── Query commands (remain in this file) ────────────────────────────────


def cmd_status(args: list[str]) -> dict:
    _, _, tm = _resolve()
    return tm.status()


def cmd_show(args: list[str]) -> dict:
    if not args:
        return {"error": "task_id required"}
    _, _, tm = _resolve()
    task = tm.show(args[0])
    return {
        "id": task.id, "title": task.title,
        "description": task.description,
        "status": task.status.value, "phase": task.phase.value,
        "iteration": task.iteration, "priority": task.priority,
        "mode": getattr(task, "mode", None),
    }


def cmd_clean(args: list[str]) -> dict:
    if not args:
        return {"error": "task_id or --all required"}
    if args[0] in ("--help", "-h", "help"):
        return {
            "usage": "kanban clean [<task_id>|--all|--before <date>]",
            "examples": [
                "kanban clean TASK-001",
                "kanban clean --all",
                "kanban clean --before 2026-01-01",
            ],
        }
    fs, _, tm = _resolve()

    if "--all" in args:
        import shutil
        cleaned = []
        for d in sorted(fs.kanban_dir.glob("archive/TASK-*")):
            if d.is_dir() and (d / "task.json").is_file():
                task_id = d.name
                shutil.rmtree(d)
                cleaned.append(task_id)
            elif d.is_file() and d.suffix == ".json":
                task_id = d.stem
                d.unlink()
                cleaned.append(task_id)
        # Clean ghost directories (no task.json) in both tasks/ and archive/
        for d in sorted(list(fs.kanban_dir.glob("tasks/TASK-*")) + list(fs.kanban_dir.glob("archive/TASK-*"))):
            if d.is_dir() and not (d / "task.json").is_file():
                shutil.rmtree(d)
        return {"cleaned": cleaned, "count": len(cleaned)}

    if "--before" in args:
        before_idx = args.index("--before")
        if before_idx + 1 < len(args):
            before_date = args[before_idx + 1]
            import shutil, time as _time
            cleaned = []
            cutoff = _time.mktime(_time.strptime(before_date, "%Y-%m-%d"))
            for d in sorted(fs.kanban_dir.glob("archive/TASK-*")):
                if d.is_dir() and (d / "task.json").is_file():
                    data = __import__('json').loads((d / "task.json").read_text(encoding="utf-8"))
                    archived_at = data.get("archived_at", 0)
                    if archived_at < cutoff:
                        shutil.rmtree(d)
                        cleaned.append(d.name)
            return {"cleaned": cleaned, "count": len(cleaned)}
        return {"error": "--before requires a date (YYYY-MM-DD)"}

    task_id = args[0]
    if not task_id.startswith("TASK-"):
        return {"error": f"task_id must start with TASK-: '{task_id}'"}
    # Only clean archived tasks — active tasks must be archived first
    archive_dir = fs.kanban_dir / "archive" / task_id
    if archive_dir.is_dir() and (archive_dir / "task.json").is_file():
        import shutil
        shutil.rmtree(archive_dir)
        return {"message": f"cleaned archived {task_id}"}
    # Check old flat format
    flat_archive = fs.kanban_dir / "archive" / f"{task_id}.json"
    if flat_archive.is_file():
        flat_archive.unlink()
        return {"message": f"cleaned archived {task_id}"}
    # Task is still active — refuse to delete
    task_dir = fs.task_dir(task_id)
    if task_dir.is_dir():
        return {
            "error": f"task {task_id} is still active — archive first",
            "hint": f"kanban decide {task_id} --action approve_and_archive",
        }
    return {"error": f"task {task_id} not found"}


def cmd_promote(args: list[str]) -> dict:
    if not args:
        return {"error": "task_id required"}
    _, _, tm = _resolve()
    task_id = args[0]
    task = tm.show(task_id)
    if task.status.value != "draft":
        return {"error": f"Task {task_id} is not in draft status"}

    task_dir = tm._fs.task_dir(task_id)
    analysis_path = task_dir / "inbox_analysis.json"
    suggested_phase = "plan"
    if analysis_path.is_file():
        analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
        suggested_phase = analysis.get("suggested_phase", "plan")

    tm.update(task_id, status="pending", phase=suggested_phase)
    tm.update(task_id, status="in_progress")
    return {
        "task_id": task_id,
        "promoted": True,
        "phase": suggested_phase,
        "message": f"Task {task_id} promoted from draft to {suggested_phase} phase",
    }
