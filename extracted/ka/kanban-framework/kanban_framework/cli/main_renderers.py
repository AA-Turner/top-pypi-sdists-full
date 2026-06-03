"""CLI output renderers — human-readable display functions."""
from __future__ import annotations


def _format_table(rows: list[list[str]], headers: list[str]) -> str:
    """Format aligned table."""
    cols = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            cols[i] = max(cols[i], len(str(cell)))
    lines = ["  ".join(h.ljust(cols[i]) for i, h in enumerate(headers))]
    lines.append("  ".join("─" * cols[i] for i in range(len(headers))))
    for row in rows:
        lines.append("  ".join(str(row[i]).ljust(cols[i]) for i in range(len(row))))
    return "\n".join(lines)


def _render_help():
    print("Usage: kanban <command> [options]\n")
    groups = [
        ("Tasks", [
            ("create   <title>", "Create a new task"),
            ("task edit <id>", "Edit task mode/priority/auto-mode"),
            ("status", "Show kanban board summary"),
            ("show     <id>", "Show task details"),
            ("promote  <id>", "Advance draft to active"),
            ("clean    <id>", "Clean up archived task"),
        ]),
        ("Execution", [
            ("run      <id>", "Execute current phase"),
            ("decide   <id>", "Make a decision"),
            ("subtask  <action>", "Manage subtasks"),
        ]),
        ("Knowledge", [
            ("knowledge search  <kw>", "Search knowledge base"),
            ("knowledge learn   <path>", "Learn from code"),
            ("knowledge backup", "Manual backup of knowledge.db"),
            ("knowledge list", "List knowledge entries"),
            ("knowledge review", "Review draft entries"),
        ]),
        ("Query", [
            ("score    <id>", "Evaluation scores"),
            ("summary  <id>", "Task summary"),
            ("progress <id>", "Subtask progress"),
            ("time     <id>", "Time tracking"),
            ("tokens   <id>", "Token usage"),
        ]),
        ("Inbox", [
            ("inbox add    <id> <text>", "Add feedback"),
            ("inbox analyze <id>", "Analyze inbox items"),
        ]),
    ]
    for group, cmds in groups:
        print(f"[{group}]")
        for cmd, desc in cmds:
            print(f"  {cmd.ljust(26)}{desc}")
        print()
    print("[Options]")
    print("  --json, -o json         Output raw JSON")
    print("  --help, -h              Show this help")
    print()
    print("[Maintenance]")
    print("  update [version]        Upgrade to latest or specified PyPI version")


def _render_status(data: dict):
    tasks = data.get("tasks", [])
    by_status = data.get("by_status", {})
    total = data.get("total", 0)

    print(f"\n  Kanban Board — {total} tasks\n")
    print(f"  In Progress: {by_status.get('in_progress', 0)}")
    print(f"  Completed:   {by_status.get('completed', 0)}")

    if not tasks:
        print("\n  No active tasks.")
        return

    print()
    print(_format_table(
        [[t.get("id",""), t.get("title","")[:30], t.get("phase",""),
          f"v{t.get('iteration',1)}", t.get("status","")]
         for t in tasks if t.get("status") != "archived"],
        ["ID", "TITLE", "PHASE", "ITER", "STATUS"]
    ))


def _render_show(data: dict):
    print(f"\n  Task: {data.get('id', '?')} — {data.get('title', '?')}")
    print(f"  Phase: {data.get('phase', '?')} | Iteration: {data.get('iteration', 1)}")
    print(f"  Status: {data.get('status', '?')}")
    if data.get("description"):
        print(f"\n  {data['description']}")


def _render_create(data: dict):
    print(f"  Created {data.get('id', '?')}: {data.get('title', '?')}")
    print(f"  Phase: {data.get('phase', '?')} | Status: {data.get('status', '?')}")

    assessment = data.get("assessment", {})
    mode_pending = data.get("mode_confirmation_pending", False)
    if assessment and mode_pending:
        mode = assessment.get("recommended_mode", "?")
        reason = assessment.get("reason", "")
        risks = assessment.get("risk_factors", [])
        mode_label = mode if mode else "full"
        print(f"  推荐模式: {mode_label}")
        print(f"  原因: {reason}")
        if risks:
            print(f"  风险: {', '.join(risks)}")

    tc = data.get("test_config")
    if tc:
        level = tc.get("level", "full")
        level_labels = {"full": "完整测试", "quick": "快速验证", "manual": "手动检查"}
        parts = [level_labels.get(level, "full")]
        if tc.get("framework"): parts.append(tc["framework"])
        if tc.get("command"): parts.append(tc["command"])
        if tc.get("coverage"): parts.append(f"coverage {tc['coverage']}")
        print(f"  Test: {' | '.join(parts)}")

    task_id = data.get("id", "")
    desc = data.get("description", "") or "(无)"
    recommended = assessment.get("recommended_mode", "lightweight")

    print(f"\n  ── 确认检查点 ──")
    print(f"  标题: {data.get('title', '?')}")
    if desc and desc != "(无)":
        print(f"  描述: {desc[:80]}{'...' if len(desc) > 80 else ''}")

    if mode_pending:
        alt = "full" if recommended == "lightweight" else "lightweight"
        print(f"\n  ⚠️  等待用户确认运行模式：")
        print(f"     [1] lightweight（推荐）— 跳过 Plan Review/QA Spec，快速迭代")
        print(f"     [2] full — 完整 10 阶段流程，严格质量门禁")
        print(f"  → 选择后执行: kanban task edit {task_id} --mode full")
        print(f"                  kanban task edit {task_id} --mode lightweight")
    else:
        print(f"  模式: {data.get('mode', 'full')}")

    tc = data.get("test_config")
    if tc:
        print(f"  测试: {tc.get('level', 'full')}")

    if mode_pending:
        print(f"\n  → 选择模式后运行: kanban run {task_id}")
    else:
        print(f"\n  → 确认无误？ kanban run {task_id}")
    print(f"  → 修改需求: 编辑 .kanban/tasks/{task_id}/spec.md 后运行")


def _render_init(data: dict):
    sync = data.get("sync", {})
    added = sync.get("added", [])
    updated = sync.get("updated", [])
    stale = sync.get("stale", [])
    created = data.get("created", []) or added + updated

    parts = []
    if added:
        parts.append(f"{len(added)} added")
    if updated:
        parts.append(f"{len(updated)} updated")
    if stale:
        parts.append(f"{len(stale)} stale")

    status = ", ".join(parts) if parts else f"{len(created)} items created"
    print(f"  kanban env ready — {status}")

    agent_sync = data.get("agent_sync", {})
    if agent_sync.get("synced"):
        print(f"  Agents: {len(agent_sync['synced'])} synced to .claude/agents/")
    if agent_sync.get("updated"):
        print(f"  Agents: {len(agent_sync['updated'])} updated in .claude/agents/")

    lang = data.get("language", "unknown")
    if lang and lang != "unknown":
        lang_labels = {"python": "Python", "javascript": "JavaScript", "typescript": "TypeScript", "go": "Go", "rust": "Rust"}
        print(f"  Language: {lang_labels.get(lang, lang)} (auto-detected)")

    if updated:
        for f in updated[:5]:
            print(f"    ~ {f}")
    pending = sync.get("pending_updates", [])
    if pending:
        print(f"\n  ⚠  {len(pending)} files have updates available (not applied)")
        for f in pending[:5]:
            print(f"    → {f}")
        if len(pending) > 5:
            print(f"    ... and {len(pending) - 5} more")
        print(f"  Review changes and run: kanban init --apply")
    if stale:
        print(f"  ⚠  {len(stale)} stale files (not in framework source)")
        for f in stale[:3]:
            print(f"    ? {f}")

    orphaned = data.get("orphaned_links", [])
    if orphaned:
        print(f"\n  ⚠  {len(orphaned)} orphaned agent/rule symlinks from older version")
        print(f"     These waste context in non-kanban sessions.")
        print(f"     Remove with: kanban init --clean-orphaned")

    if data.get("pip_warning"):
        print(f"  ⚠️  {data['pip_warning']}")


def _render_score(data: dict):
    scores = data.get("scores", [])
    avg = data.get("average")
    print(f"\n  Average: {avg}/10" if avg else "\n  No scores yet")
    if scores:
        print(_format_table(
            [[s["role"], f"{s['total']}/10", f"iter {s['iteration']}"] for s in scores],
            ["ROLE", "SCORE", "ITER"]
        ))


def _render_summary(data: dict):
    print(f"\n  Task: {data.get('title', data.get('task_id', '?'))}")
    print(f"  Phase: {data.get('phase', '?')} | Status: {data.get('status', '?')}")
    print(f"  Progress: {data.get('progress', {})}")


def _render_nlp(data: dict):
    print(f"\n  Input: {data.get('input', '')}")
    print(f"  Task ID: {data.get('task_id', '-')}")
    guidance = data.get("routing_guidance", {})
    print(f"  Intent: {guidance.get('intent', '?')}")
    print(f"  Suggested: {guidance.get('suggested_command', '?')}")
    print(f"  Rule: {guidance.get('rule', '')[:120]}")
    cmds = data.get("available_commands", [])
    print(f"\n  Commands ({len(cmds)} total):")
    for c in cmds:
        print(f"    {c.get('command', ''):<24} {c.get('example', '')}")


def _render_time(data: dict):
    t = data.get("time", data)
    print(f"\n  Total: {t.get('total_seconds', 0):.0f}s")
    for phase, info in t.get("phases", {}).items():
        print(f"  {phase}: {info.get('elapsed_seconds', 0):.0f}s")


def _render_tokens(data: dict):
    t = data.get("tokens", data)

    if "text_output" in data:
        print(f"\n{data['text_output']}")
        return

    if "today" in data:
        print(f"\n  Today: {data.get('today',{}).get('cost','?')}  |  Month: {data.get('month',{}).get('cost','?')}")
        return

    if "overview" in data:
        o = data["overview"]
        print(f"\n  Period: {data.get('period','?')}")
        print(f"  Tokens: {o.get('totalTokens',0):,}  |  Cost: {o.get('cost','0')}  |  Sessions: {o.get('sessions',0)}")
        return

    total = t.get("total_tokens", 0)
    budget = "within budget" if t.get("within_budget", True) else "over budget"
    print(f"\n  Total: {total:,} tokens ({budget})")
    for phase, tokens in t.get("by_phase", {}).items():
        print(f"  {phase}: {tokens}")


def _is_pre_release(version: str) -> bool:
    """Check if a version string is a pre-release (PEP 440)."""
    import re
    return bool(re.search(r'(a|b|rc|alpha|beta|dev)\d*', version))


def _render_update(data: dict):
    if data.get("action") == "channels":
        if "error" in data:
            print(f"  Error: {data['error']}")
        else:
            print(f"  Stable (latest 10):")
            for v in data.get("stable", []):
                print(f"    v{v}")
            print(f"  Dev / Pre-release (latest 10):")
            dev = data.get("dev", [])
            if dev:
                for v in dev:
                    print(f"    v{v}")
            else:
                print(f"    (none)")
        return
    if data.get("action") == "list_versions":
        if "error" in data:
            print(f"  Error: {data['error']}")
        else:
            print(f"  All versions ({data.get('count', 0)} total, showing latest 20):")
            for v in data.get("versions", []):
                marker = " [dev]" if _is_pre_release(v) else ""
                print(f"    v{v}{marker}")
        return
    if data.get("success"):
        print(f"  Updated to kanban-framework v{data.get('version', '?')}")
        sync = data.get("skill_sync", {})
        if isinstance(sync, dict) and sync.get("synced"):
            print(f"  Skill files synced to .claude/skills/kanban/")
    else:
        print(f"  Update failed: {data.get('pip_output', data.get('error', 'unknown error'))}")
        print(f"  Try: pip install --upgrade kanban-framework")


def _render_json_fallback(cmd: str, data: dict):
    """Fallback: show key fields in readable format."""
    if isinstance(data, dict):
        for k, v in data.items():
            if k in ("success", "code"):
                continue
            if isinstance(v, (str, int, float, bool)):
                print(f"  {k}: {v}")
            elif isinstance(v, list):
                if len(v) <= 5 and all(isinstance(x, str) for x in v):
                    for x in v:
                        print(f"  - {x}")
                else:
                    print(f"  {k}: [{len(v)} items]")
            elif isinstance(v, dict):
                if len(v) <= 5:
                    for dk, dv in v.items():
                        if isinstance(dv, (str, int, float, bool)):
                            print(f"  {dk}: {dv}")
                        else:
                            print(f"  {dk}: {type(dv).__name__}")
                else:
                    print(f"  {k}: {{{len(v)} keys}}")
    else:
        print(f"  {data}")


from kanban_framework.cli.main_renderers_extra import (  # noqa: F401
    _render_dashboard,
    _render_knowledge,
)
