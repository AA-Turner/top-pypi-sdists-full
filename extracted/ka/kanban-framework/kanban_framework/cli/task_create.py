"""Task creation command — create, assess, and configure new tasks."""
from __future__ import annotations

import argparse
import logging

from kanban_framework.cli.task_utils import _resolve


def cmd_create(args: list[str]) -> dict:
    from kanban_framework.types import AutoMode

    # Scan for --control-mode and legacy --mode manual before argparse
    control_mode = None
    filtered_args: list[str] = []
    skip_next = False
    for i, arg in enumerate(args):
        if skip_next:
            skip_next = False
            continue
        if arg == "--control-mode" and i + 1 < len(args):
            value = args[i + 1]
            if value in ("auto", "semi", "manual"):
                control_mode = value
            skip_next = True
            continue
        if arg == "--mode" and i + 1 < len(args):
            if args[i + 1] == "manual":
                control_mode = "manual"
                skip_next = True
                continue
        filtered_args.append(arg)

    parser = argparse.ArgumentParser(prog="kanban create", add_help=False)
    parser.add_argument("title", nargs="*", default=[], help="Task title")
    parser.add_argument("--desc", nargs="*", default=[], help="Task description")
    parser.add_argument("--mode", type=str, default=None,                         help="Task mode: lightweight, quick, custom, or any custom mode from workflow.json")
    parser.add_argument("--lightweight", action="store_true", default=False,
                        help="Shorthand for --mode lightweight")
    parser.add_argument("--auto-mode", nargs="*", default=[], dest="auto_mode",
                        help="Auto-mode flags: all, brainstorm, iteration, lightweight, archive, worktree")
    parser.add_argument("--priority", type=int, default=5, dest="priority",
                        help="Task priority (0-10, default 5)")
    parser.add_argument("--test-level", type=str, default=None,
                        choices=["quick", "manual"],
                        help="Test verification level: quick (basic tests), manual (verify runs)")
    parser.add_argument("--test-cmd", type=str, default=None, dest="test_cmd",
                        help="Test command (e.g. 'pytest tests/ -v')")
    parser.add_argument("--test-framework", type=str, default=None, dest="test_framework",
                        help="Test framework (e.g. pytest, unittest, jest)")
    parser.add_argument("--coverage", type=str, default=None,
                        help="Coverage target (e.g. '80%')")
    parser.add_argument("--draft", action="store_true", default=False,
                        help="Create as draft placeholder task")
    parser.add_argument("--no-knowledge", action="store_true", default=False,
                        dest="no_knowledge",
                        help="Skip auto knowledge search on create")
    parser.add_argument("--manual", action="store_true", default=False,
                        help="Create with scaffolded spec/plan templates, user edits spec then run")
    parser.add_argument("--biz", type=str, default=None, dest="biz",
                        help="Business context tag for knowledge isolation")

    parsed = parser.parse_args(filtered_args)
    title = " ".join(parsed.title) if parsed.title else "Untitled"
    desc = " ".join(parsed.desc) if parsed.desc else ""
    auto_mode_flags = parsed.auto_mode

    # ── Resolve filesystem and config (early, for default_mode) ──
    fs, _, tm = _resolve()
    from kanban_framework.domain.assessment import assess_task
    ai = assess_task(title, desc)

    _default_mode = tm._cfg.default_mode if tm._cfg else Consts.DEFAULT_MODE

    task_mode = parsed.mode
    user_specified_mode = bool(task_mode or parsed.lightweight)

    if task_mode == _default_mode or parsed.lightweight:
        task_mode = _default_mode
    if task_mode is None:
        task_mode = ai["recommended_mode"]

    # Parse auto_mode flags
    auto_mode = AutoMode()
    if auto_mode_flags:
        if "all" in auto_mode_flags:
            auto_mode = AutoMode(
                auto_brainstorm=True,
                auto_iteration=True,
                auto_lightweight=True,
                auto_archive=True,
                auto_worktree=True,
            )
        else:
            _valid_flags = {"brainstorm", "iteration", "lightweight", "archive", "worktree"}
            for flag in auto_mode_flags:
                if flag in _valid_flags:
                    setattr(auto_mode, f"auto_{flag}", True)
                else:
                    logging.getLogger("kanban").warning(
                        f"unknown --auto-mode flag: '{flag}'. Valid: {', '.join(sorted(_valid_flags))}")
                    return {
                        "id": None, "title": title,
                        "error": f"unknown --auto-mode flag: '{flag}'. Valid values: {', '.join(sorted(_valid_flags))}",
                    }

    # ── Test config ──
    test_config = None
    test_level = parsed.test_level
    if test_level is None:
        test_level = "quick"

    if parsed.test_cmd or parsed.test_framework or parsed.coverage or test_level != "quick":
        test_config = {
            "level": test_level,
        }
        if parsed.test_cmd:
            test_config["command"] = parsed.test_cmd
        if parsed.test_framework:
            test_config["framework"] = parsed.test_framework
        if parsed.coverage:
            test_config["coverage"] = parsed.coverage

    priority = max(0, min(10, parsed.priority))

    recommendation = _recommend_worktree(title, desc)

    if parsed.draft:
        task = tm.create(title, desc, draft=True)
        tm.update(task.id, priority=priority)
        return {
            "id": task.id,
            "title": task.title,
            "phase": None,
            "status": "draft",
            "auto_mode": None,
            "recommendation": {
                "use_worktree": False,
                "use_lightweight": True,
                "reason": "draft 任务暂不需要隔离工作区，promote 时重新评估",
            },
            "message": f"Draft task {task.id} created. Add requirements via inbox, then promote when ready.",
        }

    task = tm.create(title, desc)
    _log = logging.getLogger("kanban")
    _log.info("create: task=%s mode=%s", task.id, task_mode)

    if task_mode == "quick":
        qr = ai.get("quick_requires") or {}
        scope_note = (
            f"\n\n[Quick Scope] change_type={qr.get('change_type') or 'fix'}, "
            f"expected_lines≤{qr.get('expected_lines', 10)}"
        )
        tm.update(task.id, description=desc + scope_note)

    # ── Core update (unaffected by manual mode) ──
    # Derive start phase from mode's phase_order (first phase is the start)
    from kanban_framework.infra.scheduler import Scheduler
    mode_phases = Scheduler.dispatch_order(mode=task_mode,
                                            workflow=tm._cfg.workflow if tm._cfg else None,
                                            kanban_dir=fs.kanban_dir)
    start_phase = mode_phases[0].value if mode_phases else "plan"
    update_kwargs: dict = {"phase": start_phase, "status": "in_progress",
                            "auto_mode": auto_mode, "priority": priority}
    if task_mode:
        update_kwargs["mode"] = task_mode
    if test_config:
        update_kwargs["test_config"] = test_config
    tm.update(task.id, **update_kwargs)

    if control_mode:
        tm.update(task.id, control_mode=control_mode)

    # Apply biz_tag if provided
    parsed_biz = parsed.biz
    if parsed_biz:
        tm.update(task.id, biz_tag=parsed_biz)

    mode_confirmation_pending = not user_specified_mode
    recommended_mode = task_mode or _default_mode
    mode_msg = f"Mode: {recommended_mode}" if task_mode else f"Select mode (lightweight/quick/custom) before running"

    # Scan for custom modes from workflow.json + .kanban/workflows/ directory
    # Priority: custom modes first, then built-in modes (AskUserQuestion limits to 4)
    custom_mode_names = []
    try:
        from kanban_framework.domain.workflow_loader import scan_workflows
        custom = scan_workflows(fs.kanban_dir)
        from kanban_framework.infra.config import Config
        cfg = Config(fs)
        wf_modes = cfg.workflow.get("modes", {})
        for name in sorted(set(list(custom.keys()) + list(wf_modes.keys()))):
            custom_mode_names.append(name)
    except Exception:
        pass

    # Build available list: custom modes first, then discovered modes, max 4 total
    available_modes = list(custom_mode_names)
    # Add any modes discovered by scheduler (package templates + directory files)
    try:
        from kanban_framework.infra.scheduler import Scheduler
        discovered = list(Scheduler.get_modes(workflow=cfg.workflow,
                                               kanban_dir=fs.kanban_dir).keys())
        for name in discovered:
            if name not in available_modes and len(available_modes) < 4:
                available_modes.append(name)
    except Exception:
        pass
    # Ensure at least one mode is available
    if not available_modes:
        from kanban_framework.infra.consts import Consts
        available_modes = [_default_mode]

    knowledge_hints = []
    if not parsed.draft and not parsed.no_knowledge:
        try:
            from kanban_framework.domain.knowledge import KnowledgeManager
            km = KnowledgeManager(fs)
            combined = f"{title} {desc}"
            k_results = km.search_hybrid(combined, limit=10, biz_context=parsed_biz)
            pitfall_results = km.search_by_intent("pitfall_check", combined, limit=5, biz_context=parsed_biz)
            # Infer project domains from existing entries for relevance filtering
            project_domains = set()
            try:
                for d in km.get_domains():
                    if isinstance(d, dict) and d.get("count", 0) >= 2:
                        project_domains.add(d.get("name", d.get("domain", "")))
            except Exception:
                pass
            seen_ids = set()
            # Sort: project-domain entries first, then others
            all_results = pitfall_results + k_results
            if project_domains:
                all_results.sort(
                    key=lambda r: (0 if r.get("domain", "") in project_domains else 1),
                )
            for r in all_results:
                if r["id"] not in seen_ids and len(knowledge_hints) < 5:
                    seen_ids.add(r["id"])
                    knowledge_hints.append({
                        "id": r["id"],
                        "title": r.get("title", ""),
                        "domain": r.get("domain", ""),
                        "category": r.get("category", ""),
                        "severity": r.get("severity", ""),
                    })
        except Exception:
            pass

    # ── Post-create hook: manual scaffold (isolated) ──
    scaffold_info = None
    if parsed.manual:
        from kanban_framework.cli.task_manual import scaffold_manual
        scaffold_info = scaffold_manual(fs, tm, task.id, title, desc)

    result = {
        "id": task.id,
        "title": task.title,
        "phase": start_phase,
        "status": "in_progress",
        "mode": task_mode or _default_mode,
        "control_mode": control_mode or "semi",
        "assessment": ai,
        "user_specified_mode": user_specified_mode,
        "test_config": test_config,
        "auto_mode": {
            "auto_brainstorm": auto_mode.auto_brainstorm,
            "auto_iteration": auto_mode.auto_iteration,
            "auto_lightweight": auto_mode.auto_lightweight,
            "auto_archive": auto_mode.auto_archive,
            "auto_worktree": auto_mode.auto_worktree,
        },
        "knowledge_hints": knowledge_hints,
        "recommendation": recommendation,
        "mode_confirmation_pending": mode_confirmation_pending,
        "mode_options": {
            "available": available_modes,
            "recommended": recommended_mode,
            "recommendation_reason": ai.get("reason", ""),
            "prompt": (
                f"请用 AskUserQuestion 展示以下 {len(available_modes)} 个模式选项供用户选择"
                f"（必须全部展示，禁止截断）: "
                + ", ".join(f"{'✓ ' if m == recommended_mode else ''}{m}" for m in available_modes)
            ),
        },
        "scaffold": scaffold_info,
    }

    if scaffold_info:
        result["message"] = (
            f"Task {task.id} created with manual scaffold. "
            f"Edit templates in {scaffold_info['task_dir']}, then `kanban run {task.id}`."
        )
    else:
        if mode_confirmation_pending:
            mode_list = ", ".join(available_modes)
            result["message"] = (
                f"Task {task.id} created. 请从以下模式中选择一个: [{mode_list}] "
                f"(推荐: {recommended_mode})。"
                f"选择后执行: `kanban task edit {task.id} --mode <模式>` → `kanban run {task.id}`"
            )
        else:
            result["message"] = f"Task {task.id} created. {mode_msg}."

    return result


def _recommend_worktree(title: str, desc: str) -> dict:
    """Recommend whether to use git worktree based on task characteristics."""
    text = f"{title} {desc}".lower()

    heavy_kw = ["游戏", "game", "web", "dashboard", "前端", "后端", "数据库", "database",
                "重构", "refactor", "迁移", "migration", "多模块", "multi-module",
                "完整项目", "full project", "系统", "system"]
    light_kw = ["脚本", "script", "工具函数", "utility", "单文件", "single file",
                "修复", "fix", "补丁", "patch", "文档", "doc", "配置", "config"]

    heavy_score = sum(1 for kw in heavy_kw if kw in text)
    light_score = sum(1 for kw in light_kw if kw in text)

    if heavy_score > light_score:
        return {
            "use_worktree": True,
            "use_lightweight": False,
            "reason": f"检测到复杂任务特征（{'/'.join(kw for kw in heavy_kw if kw in text)[:60]}），建议使用 git worktree 隔离开发环境",
        }
    elif light_score > heavy_score:
        return {
            "use_worktree": False,
            "use_lightweight": True,
            "reason": f"检测到简单任务特征（{'/'.join(kw for kw in light_kw if kw in text)[:60]}），轻量模式即可，无需 worktree",
        }
    return {
        "use_worktree": False,
        "use_lightweight": False,
        "reason": "无法自动判断复杂度，建议手动选择是否使用 worktree",
    }
