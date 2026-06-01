from __future__ import annotations
import re
from datetime import datetime
from pathlib import Path
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.domain.task import TaskManager, TaskNotFoundError
from kanban_framework.infra.config import Config


class InboxError(Exception):
    pass


# Tag patterns for verified feedback items
TAG_DONE = re.compile(r'done:(\S+)')
TAG_MIGRATED = re.compile(r'migrated:(\S+)')
TAG_WONTFIX = re.compile(r'wontfix:(.+?)(?:-->|$)')


def _has_verification_tag(line: str) -> bool:
    """Check if a checked item has a done:/migrated:/wontfix: tag."""
    return bool(TAG_DONE.search(line) or TAG_MIGRATED.search(line) or TAG_WONTFIX.search(line))


def dispatch(args: list[str]) -> dict:
    sub = args[0] if args else "list"
    root = Filesystem.find_project_root()
    fs = Filesystem(root=root)

    if sub == "list":
        return _list_inbox(fs)
    if sub == "add":
        return _add_to_task_inbox(fs, args[1:])
    if sub == "archive":
        return _archive_task_inbox(fs, args[1:])
    if sub == "analyze":
        return _analyze_task_inbox(fs, args[1:])
    if sub == "process":
        return _process_inbox(fs, args[1:])
    if sub == "add-subtasks":
        return _add_subtasks(fs, args[1:])
    return {"subcommand": sub}


# ── cmd_feedback (global inbox.json) ──────────────────────────────

def cmd_feedback(args: list[str]) -> dict:
    task_id = args[0] if args else None
    if not task_id:
        return {"error": "task_id required"}
    text = " ".join(args[1:]) if len(args) > 1 else ""

    root = Filesystem.find_project_root()
    fs = Filesystem(root=root)
    inbox_file = fs.inbox_file()
    fs.ensure_dir(inbox_file.parent)

    entries = []
    if fs.file_exists(inbox_file):
        entries = fs.read_json(inbox_file)

    entries.append({
        "task_id": task_id,
        "text": text,
        "type": "feedback",
    })
    fs.write_json(inbox_file, entries)
    return {"task_id": task_id, "feedback": text, "saved": True}


# ── list ──────────────────────────────────────────────────────────

def _list_inbox(fs: Filesystem) -> dict:
    inbox_file = fs.inbox_file()
    if not fs.file_exists(inbox_file):
        return {"inbox": [], "count": 0}
    entries = fs.read_json(inbox_file)
    return {"inbox": entries, "count": len(entries)}


# ── add ───────────────────────────────────────────────────────────

def _add_to_task_inbox(fs: Filesystem, args: list[str]) -> dict:
    """Add a feedback item to a task's inbox.md file.

    Usage:
        kanban inbox add <task_id> "<text>"    # Add to task inbox
        kanban inbox add "<text>"              # Add to global issues (#220)
    """
    if not args:
        raise InboxError("task_id or text required")

    text = ""
    task_id = None

    # Check if first arg looks like a task_id (TASK-NNN format)
    if args and args[0].startswith("TASK-"):
        task_id = args[0]
        text = " ".join(args[1:]) if len(args) > 1 else ""
    else:
        # No task_id — save to global .kanban/issues.md (#220)
        text = " ".join(args)
        if not text:
            raise InboxError("feedback text required")

        issues_path = fs.kanban_dir / "issues.md"
        fs.ensure_dir(fs.kanban_dir)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_entry = f"- [ ] {text} <!-- {timestamp} -->\n"

        if fs.file_exists(issues_path):
            content = issues_path.read_text(encoding="utf-8")
            issues_path.write_text(content + new_entry, encoding="utf-8")
        else:
            issues_path.write_text(
                f"# Framework Issues\n\n"
                f"全局反馈和框架问题追踪。通过 `kanban inbox add \"<text>\"` 添加。\n\n"
                f"{new_entry}",
                encoding="utf-8"
            )
        return {
            "task_id": None,
            "action": "added_global",
            "text": text,
            "inbox_file": str(issues_path),
        }

    if not text:
        raise InboxError("feedback text required")

    task_dir = fs.task_dir(task_id)
    inbox_path = task_dir / "inbox.md"

    # Ensure task directory exists
    fs.ensure_dir(task_dir)

    # Create or append to inbox.md
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_entry = f"- [ ] {text} <!-- {timestamp} -->\n"

    if fs.file_exists(inbox_path):
        content = inbox_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        insert_pos = 0
        for i, line in enumerate(lines):
            if line.startswith("#"):
                insert_pos = i + 1
            elif line.strip() and not line.startswith("#"):
                break
        lines.insert(insert_pos, "")
        lines.insert(insert_pos + 1, new_entry)
        inbox_path.write_text("\n".join(lines), encoding="utf-8")
    else:
        inbox_path.write_text(
            f"# Task Inbox — {task_id}\n\n"
            f"用户反馈和待办事项。\n\n"
            f"{new_entry}",
            encoding="utf-8"
        )

    return {
        "task_id": task_id,
        "action": "added",
        "text": text,
        "inbox_file": str(inbox_path)
    }


# ── process (read-only analysis) ──────────────────────────────────

def _process_inbox(fs: Filesystem, args: list[str]) -> dict:
    """Analyze inbox items without modifying any files."""
    from kanban_framework.domain.inbox_analyzer import InboxAnalyzer
    if not args:
        raise InboxError("task_id required")
    task_id = args[0]

    # --semantic flag — future hook for planner-agent based conflict check
    semantic = "--semantic" in args

    analyzer = InboxAnalyzer(fs)
    try:
        analysis = analyzer.generate_analysis(task_id)
        if semantic:
            analysis["semantic_check"] = "pending"
            analysis["message"] = (
                "语义冲突检测需 spawn planner agent，当前为结构性分析结果。"
                "请根据 conflicts 字段评估是否需要更新 spec.md 和 plan/。"
            )
        return analysis
    except Exception as e:
        return {"error": str(e), "task_id": task_id}


# ── analyze (backward compat, now read-only) ──────────────────────

def _analyze_task_inbox(fs: Filesystem, args: list[str]) -> dict:
    """Read-only analysis.  No longer auto-checks items."""
    from kanban_framework.domain.inbox_analyzer import InboxAnalyzer
    if not args:
        return {"error": "task_id required"}
    task_id = args[0]
    analyzer = InboxAnalyzer(fs)
    try:
        analysis = analyzer.generate_analysis(task_id)
        return analysis
    except Exception as e:
        return {"error": str(e)}


# ── archive (with verification) ───────────────────────────────────

def _archive_task_inbox(fs: Filesystem, args: list[str]) -> dict:
    """Archive verified completed items from inbox.md to inbox-archive.md.

    Only items with done:/migrated:/wontfix: tags are archived.
    Unverified [x] items are rejected with an error listing them.
    """
    if not args:
        raise InboxError("task_id required")
    task_id = args[0]
    force = "--force" in args  # allow force-archive without tags (non-interactive only)

    task_dir = fs.task_dir(task_id)
    inbox_path = task_dir / "inbox.md"
    archive_path = task_dir / "inbox-archive.md"

    if not fs.file_exists(inbox_path):
        return {
            "task_id": task_id,
            "action": "archive",
            "archived_count": 0,
            "message": "inbox.md not found",
        }

    content = inbox_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    verified = []        # [x] with tags → archive
    unverified = []      # [x] without tags → REJECT
    remaining = []       # [ ] and non-task lines
    pending_items = []   # unchecked items

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- [x]") or stripped.startswith("* [x]"):
            if _has_verification_tag(stripped) or force:
                verified.append(line)
            else:
                unverified.append(stripped)
        elif stripped.startswith("- [ ]") or stripped.startswith("* [ ]"):
            remaining.append(line)
            pending_items.append(stripped)
        else:
            remaining.append(line)

    # Reject if unverified items exist (unless --force)
    if unverified and not force:
        return {
            "task_id": task_id,
            "action": "archive",
            "archived_count": 0,
            "verified_count": len(verified),
            "pending_count": len(pending_items),
            "error": "unverified_items",
            "message": (
                f"{len(unverified)} checked item(s) have no verification tag. "
                "Add done:<path>, migrated:<TASK-NNN>, or wontfix:<reason> tag before archiving."
            ),
            "unverified_items": unverified,
        }

    if not verified:
        return {
            "task_id": task_id,
            "action": "archive",
            "archived_count": 0,
            "pending_count": len(pending_items),
            "message": "no verified items to archive",
        }

    # Write archive
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    archive_header = f"\n## Archive — {timestamp}\n\n"
    archive_content = archive_header + "\n".join(verified)

    if fs.file_exists(archive_path):
        existing = archive_path.read_text(encoding="utf-8")
        archive_path.write_text(existing + archive_content, encoding="utf-8")
    else:
        archive_path.write_text(
            f"# Inbox Archive — {task_id}\n\n"
            f"已归档的用户反馈和待办事项。\n"
            f"{archive_content}",
            encoding="utf-8"
        )

    # Update inbox.md with only remaining (pending) items
    inbox_path.write_text("\n".join(remaining), encoding="utf-8")

    return {
        "task_id": task_id,
        "action": "archived",
        "archived_count": len(verified),
        "pending_count": len(pending_items),
        "archive_file": str(archive_path),
    }


# ── add-subtasks ──────────────────────────────────────────────────

def _add_subtasks(fs: Filesystem, args: list[str]) -> dict:
    """Generate supplemental ST-NNN subtasks from inbox process results.

    Reads inbox process output, extracts scope:current items,
    appends new subtasks to task_breakdown.json and updates plan/index.md.
    """
    if not args:
        raise InboxError("task_id required")
    task_id = args[0]

    from kanban_framework.domain.inbox_analyzer import InboxAnalyzer
    analyzer = InboxAnalyzer(fs)
    analysis = analyzer.generate_analysis(task_id)

    current_items = [
        c for c in analysis.get("scope_classifications", [])
        if c.get("scope") == "current"
    ]

    if not current_items:
        return {
            "task_id": task_id,
            "action": "add-subtasks",
            "added": 0,
            "message": "no scope:current items to create subtasks for",
        }

    task_dir = fs.task_dir(task_id)
    breakdown_path = task_dir / "task_breakdown.json"

    import json
    breakdown = {}
    if fs.file_exists(breakdown_path):
        breakdown = json.loads(breakdown_path.read_text(encoding="utf-8"))

    existing_subtasks = breakdown.get("subtasks", [])
    max_st_num = _max_st_num(existing_subtasks)

    new_subtasks = []
    for idx, item in enumerate(current_items):
        st_num = max_st_num + idx + 1
        st_id = f"ST-{st_num:03d}"
        new_subtasks.append({
            "id": st_id,
            "title": item.get("requirement", f"inbox-{st_num}")[:80],
            "description": f"来自 inbox 反馈: {item.get('requirement', '')}",
            "source": "inbox",
            "domain": item.get("domain", "infra"),
            "priority": item.get("priority", "medium"),
            "plan_file": f"plan/{st_id}_inbox.md",
            "parallelizable": True,
            "estimated_files": [],
            "file_ownership": [],
            "dependencies": [],
        })

    # Append to breakdown
    breakdown["subtasks"] = existing_subtasks + new_subtasks
    breakdown_path.write_text(json.dumps(breakdown, ensure_ascii=False, indent=2), encoding="utf-8")

    # Update plan/index.md
    plan_index = task_dir / "plan" / "index.md"
    if fs.file_exists(plan_index):
        plan_content = plan_index.read_text(encoding="utf-8")
        append_lines = ["\n## 补充 Subtask（来自 inbox 反馈）\n"]
        for st in new_subtasks:
            append_lines.append(f"- **{st['id']}** [{st.get('priority', 'medium')}]: {st['title']}")
        plan_index.write_text(plan_content + "\n".join(append_lines), encoding="utf-8")

    # Check for file_ownership conflicts if task is in execute phase
    in_execute = _task_in_phase(fs, task_id, ("execute",))
    conflict_warning = None
    if in_execute:
        current_owned = set()
        for st in existing_subtasks:
            for fo in st.get("file_ownership", []):
                current_owned.add(fo)
        new_owned = set()
        for st in new_subtasks:
            for fo in st.get("file_ownership", []):
                new_owned.add(fo)
        overlap = current_owned & new_owned
        if overlap:
            conflict_warning = (
                f"New inbox subtasks share files with current batch: {overlap}. "
                "Consider completing the current batch first."
            )

    result = {
        "task_id": task_id,
        "action": "add-subtasks",
        "added": len(new_subtasks),
        "subtask_ids": [st["id"] for st in new_subtasks],
        "breakdown_file": str(breakdown_path),
    }
    if conflict_warning:
        result["warning"] = conflict_warning
    return result


def _max_st_num(subtasks: list[dict]) -> int:
    max_n = 0
    for st in subtasks:
        sid = st.get("id", "")
        if sid.startswith("ST-"):
            try:
                n = int(sid[3:])
                if n > max_n:
                    max_n = n
            except ValueError:
                pass
    return max_n


# ── helpers ───────────────────────────────────────────────────────

def _task_in_phase(fs: Filesystem, task_id: str, phases: tuple[str, ...]) -> bool:
    import json
    task_json = fs.task_dir(task_id) / "task.json"
    if not fs.file_exists(task_json):
        return False
    try:
        data = json.loads(task_json.read_text(encoding="utf-8"))
        return data.get("phase", "") in phases
    except Exception:
        return False


# ── archive_on_task_completion ─────────────────────────────────────

def archive_on_task_completion(task_id: str) -> dict:
    """
    Auto-archive inbox items when task is completed/archived.
    Called by cmd_decide when action is approve_and_archive.

    Uses --force to bypass verification since at this point
    the task has been completed (all feedback should be resolved).
    """
    root = Filesystem.find_project_root()
    fs = Filesystem(root=root)
    return _archive_task_inbox(fs, [task_id, "--force"])
