"""CLI maintenance commands — stats, update, check-env, sync-agents."""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path


def _is_pre_release(version: str) -> bool:
    """Check if a version string is a pre-release (PEP 440)."""
    import re
    return bool(re.search(r'(a|b|rc|alpha|beta|dev)\d*', version))


def _version_key(v: str):
    """Sort key for semantic version strings (e.g. '0.158.6' > '0.99.9')."""
    import re
    nums = re.match(r'v?(\d+(?:\.\d+)*)', v)
    if nums:
        return tuple(int(x) for x in nums.group(1).split('.'))
    return (0,)


def _cmd_stats(args: list[str]) -> dict:
    """Return token/time stats via the configured StatsBackend.

    Flags:
      --task TASK-ID          Per-task stats (legacy backend)
      --llm-task TASK-ID      Per-task LLM call attribution (command-segment)
      --breakdown TASK-ID     Per-command segment breakdown for one task
      --by-mode               Per-mode aggregation (LLM call attribution)
      --top-tasks [N]         Top N tasks by LLM calls (default 10)
      --sort calls|tokens     Sort key for --top-tasks (default: calls)
      --days N                Global stats window (default 30 days)
    """
    from kanban_framework.infra.filesystem import Filesystem

    fs = Filesystem(Filesystem.find_project_root())

    # New LLM call attribution via command-segment analysis
    for i, a in enumerate(args):
        if a == "--llm-task" and i + 1 < len(args):
            from kanban_framework.domain.llm_stats import LLMStatsReader
            reader = LLMStatsReader(fs.kanban_dir.parent)
            # v0.190: Use two-step region+filter algorithm for accurate counts
            data = reader.get_task_api_calls(args[i + 1])
            data["meta"] = {
                "command": "stats --llm-task",
                "scope": "task",
                "truncated": False,
                "total_available": 1,
            }
            return data
        if a == "--task-issues" and i + 1 < len(args):
            from kanban_framework.domain.llm_stats import LLMStatsReader
            reader = LLMStatsReader(fs.kanban_dir.parent)
            return reader.get_task_issues(args[i + 1])
        if a == "--export-logs" and i + 1 < len(args):
            from kanban_framework.domain.llm_stats import LLMStatsReader
            reader = LLMStatsReader(fs.kanban_dir.parent)
            task_id = args[i + 1]
            output_dir = fs.kanban_dir / "tasks" / task_id / "logs"
            return reader.export_task_logs(task_id, output_dir)
        if a == "--breakdown" and i + 1 < len(args):
            from kanban_framework.domain.llm_stats import LLMStatsReader
            reader = LLMStatsReader(fs.kanban_dir.parent)
            task_id = args[i + 1]
            # Optional --max N: limit returned segments (top N by tokens)
            max_n = None
            for j, b in enumerate(args):
                if b == "--max" and j + 1 < len(args) and args[j + 1].isdigit():
                    max_n = int(args[j + 1])
                    break
            breakdown = reader.get_task_breakdown(task_id)
            full_count = len(breakdown["segments"])
            if max_n is not None and max_n > 0:
                full = sorted(
                    breakdown["segments"],
                    key=lambda s: s["input_tokens"] + s["output_tokens"],
                    reverse=True,
                )
                truncated = len(full) > max_n
                breakdown["segments"] = full[:max_n]
            else:
                truncated = False
            # v0.186.1: standardized fields (kept legacy names as aliases)
            breakdown["truncated"] = truncated
            breakdown["total_segments_available"] = full_count
            breakdown["total_available"] = full_count  # standardized alias
            breakdown["meta"] = {
                "command": "stats --breakdown",
                "scope": "task_breakdown",
                "truncated": truncated,
                "total_available": full_count,
            }
            return breakdown
        if a == "--by-mode":
            from kanban_framework.domain.llm_stats import LLMStatsReader
            reader = LLMStatsReader(fs.kanban_dir.parent)
            mode_stats = reader.get_mode_stats()
            total_calls = sum(s.total_calls for s in mode_stats.values())
            total_tasks = sum(s.task_count for s in mode_stats.values())
            return {
                "modes": {m: s.to_dict() for m, s in mode_stats.items()},
                "summary": {
                    "total_tasks_attributed": total_tasks,
                    "total_calls": total_calls,
                },
                # v0.186.1: standardized meta block
                "meta": {
                    "command": "stats --by-mode",
                    "scope": "mode",
                    "truncated": False,
                    "total_available": len(mode_stats),
                },
            }
        if a == "--top-tasks":
            # Optional N argument after the flag (default 10)
            limit = 10
            if i + 1 < len(args) and args[i + 1].isdigit():
                limit = int(args[i + 1])
            sort_by = "calls"
            for j, b in enumerate(args):
                if b == "--sort" and j + 1 < len(args):
                    if args[j + 1] in ("calls", "tokens"):
                        sort_by = args[j + 1]
                    break
            return _build_top_tasks(fs, limit, sort_by)

    # Legacy backend (token/time from JSONL estimation)
    from kanban_framework.infra.stats_backend import resolve_stats_backend
    cfg = {}
    try:
        cfg_path = fs.config_file()
        if cfg_path.is_file():
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except Exception:
        pass

    stats_cfg = cfg.get("stats", {}) if isinstance(cfg, dict) else {}
    backend_name = stats_cfg.get("backend", "native")
    backend = resolve_stats_backend(backend_name, fs.kanban_dir.parent)

    for i, a in enumerate(args):
        if a == "--task" and i + 1 < len(args):
            return backend.get_task_stats(args[i + 1])


def _build_top_tasks(fs, limit: int, sort_by: str) -> dict:
    """Build the --top-tasks response by aggregating LLM call attribution.

    Reuses LLMStatsReader.list_attributable_tasks() for the ranking, then
    enriches each top task with full stats + mode (from task.json).
    """
    import json as _json
    from kanban_framework.domain.llm_stats import LLMStatsReader

    reader = LLMStatsReader(fs.kanban_dir.parent)
    ranked = reader.list_attributable_tasks()  # {task_id: call_count}, sorted desc

    # Build mode lookup from active + archived task.json files
    mode_lookup: dict[str, str] = {}
    for tasks_dir in [fs.kanban_dir / "tasks", fs.kanban_dir / "archive"]:
        if not tasks_dir.is_dir():
            continue
        for task_dir in tasks_dir.iterdir():
            if not task_dir.is_dir():
                continue
            tj = task_dir / "task.json"
            if not tj.is_file():
                continue
            try:
                data = _json.loads(tj.read_text(encoding="utf-8"))
                mode_lookup[task_dir.name] = data.get("mode") or "unknown"
            except (_json.JSONDecodeError, OSError):
                continue

    top_items = list(ranked.items())[:limit]
    top_tasks = []
    for task_id, _call_count in top_items:
        stats = reader.get_task_stats(task_id)
        top_tasks.append({
            "task_id": task_id,
            "mode": mode_lookup.get(task_id, "unknown"),
            "total_calls": stats.total_calls,
            "main_agent_calls": stats.main_agent_calls,
            "sub_agent_calls": stats.sub_agent_calls,
            "tokens_total": stats.input_tokens + stats.output_tokens,
            "input_tokens": stats.input_tokens,
            "output_tokens": stats.output_tokens,
            "kanban_commands": stats.kanban_commands,
            "sessions_count": stats.sessions_count,
            "first_activity_at": stats.first_activity_at,
            "last_activity_at": stats.last_activity_at,
        })

    # Apply secondary sort if user requested tokens
    if sort_by == "tokens":
        top_tasks.sort(key=lambda x: x["tokens_total"], reverse=True)

    return {
        "top_tasks": top_tasks,
        "sort_by": sort_by,
        "limit": limit,
        "total_tasks_considered": len(ranked),  # legacy alias (kept for compat)
        "total_available": len(ranked),  # v0.186.1: standardized name
        "meta": {
            "command": "stats --top-tasks",
            "scope": "top_tasks",
            "truncated": len(top_tasks) < len(ranked),
            "total_available": len(ranked),
        },
    }


def _cmd_help(args: list[str], cmd_map: dict) -> dict:
    return {"commands": sorted(cmd_map.keys())}


def _cmd_update(args: list[str]) -> dict:
    """Upgrade kanban-framework and sync skill files.

    Channels:
      --channel stable (default) → latest stable PyPI version
      --channel dev              → latest pre-release
    """
    import subprocess as _sp

    if args and args[0] == "--list":
        try:
            import urllib.request
            url = "https://pypi.org/pypi/kanban-framework/json"
            data = json.loads(urllib.request.urlopen(url, timeout=10).read())
            versions = sorted(data.get("releases", {}).keys(), key=_version_key, reverse=True)[:20]
            return {"action": "list_versions", "count": len(versions), "versions": versions}
        except Exception as e:
            return {"action": "list_versions", "error": str(e)}

    if args and args[0] == "--channels":
        try:
            import urllib.request
            url = "https://pypi.org/pypi/kanban-framework/json"
            data = json.loads(urllib.request.urlopen(url, timeout=10).read())
            all_v = sorted(data.get("releases", {}).keys(), key=_version_key, reverse=True)
            stable = [v for v in all_v if not _is_pre_release(v)][:10]
            dev = [v for v in all_v if _is_pre_release(v)][:10]
            return {"action": "channels", "stable": stable, "dev": dev}
        except Exception as e:
            return {"action": "channels", "error": str(e)}

    use_pre = False
    channel = "stable"
    target = None
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--channel", "-c") and i + 1 < len(args):
            channel = args[i + 1]; i += 2
        elif a == "dev":
            use_pre = True; i += 1
        elif a == "stable":
            channel = "stable"; i += 1
        elif a == "latest":
            channel = "latest"; i += 1
        elif not a.startswith("-"):
            target = a; i += 1
        else:
            i += 1

    from kanban_framework.infra.filesystem import Filesystem
    _python_bin, _ = Filesystem.resolve_python()

    if target:
        cmd = [_python_bin, "-m", "pip", "install", f"kanban-framework=={target}"]
    elif channel == "stable":
        cmd = [_python_bin, "-m", "pip", "install", "--upgrade", "kanban-framework"]
    elif use_pre:
        cmd = [_python_bin, "-m", "pip", "install", "--upgrade", "--pre", "kanban-framework"]
    else:
        cmd = [_python_bin, "-m", "pip", "install", "--upgrade", "kanban-framework"]

    _UPDATE_TIMEOUT = 300

    popen_kw: dict = {
        "stdout": _sp.PIPE,
        "stderr": _sp.STDOUT,
        "text": True,
        "encoding": "utf-8",
        "errors": "replace",
    }
    if sys.platform == "win32":
        _flags = 0
        for _attr in ("CREATE_NO_WINDOW", "CREATE_NEW_PROCESS_GROUP"):
            if hasattr(_sp, _attr):
                _flags |= getattr(_sp, _attr)
        if _flags:
            popen_kw["creationflags"] = _flags

    pip_rc = -1
    pip_last_line = ""
    try:
        proc = _sp.Popen(cmd, **popen_kw)
        deadline = time.monotonic() + _UPDATE_TIMEOUT
        for line in proc.stdout:
            pip_last_line = line.strip()
            if pip_last_line:
                print(f"  {pip_last_line}", flush=True)
            if time.monotonic() > deadline:
                proc.kill()
                pip_last_line = f"升级超时（{_UPDATE_TIMEOUT}秒），请检查网络后重试"
                break
        proc.wait(timeout=30)
        pip_rc = proc.returncode
    except Exception as exc:
        pip_last_line = f"升级失败: {exc}"

    from importlib.metadata import version as _pkg_version
    try:
        new_ver = _pkg_version("kanban-framework")
    except Exception:
        new_ver = "unknown"

    init_result = None
    if pip_rc == 0:
        from kanban_framework.infra.filesystem import Filesystem
        init_result = Filesystem.run_no_window(
            [_python_bin, "-m", "kanban_framework", "init", "--apply", "--non-interactive"]
        )
        if init_result.returncode != 0:
            init_result = {"error": init_result.stderr.strip()}
        else:
            init_result = {"synced": True}

    from pathlib import Path
    dashboard_updated = False
    try:
        from kanban_framework.infra.filesystem import Filesystem
        root = Filesystem.find_project_root()
        fs = Filesystem(root)
        from kanban_framework.infra.dashboard import DashboardManager
        DashboardManager(fs.kanban_dir).deploy()
        dashboard_updated = True
    except Exception:
        pass

    return {
        "success": pip_rc == 0,
        "version": new_ver,
        "pip_output": pip_last_line,
        "skill_sync": init_result,
        "dashboard_redeployed": dashboard_updated,
    }


def _cmd_check_env(args: list[str]) -> dict:
    from pathlib import Path
    from kanban_framework.infra.filesystem import Filesystem
    from kanban_framework.infra.config import Config
    root = Filesystem.find_project_root()
    kanban_dir = root / ".kanban"

    agent_sync_issues = _check_agent_sync()

    task_id_base = 0
    if kanban_dir.is_dir():
        try:
            fs = Filesystem(root)
            cfg = Config(fs)
            task_id_base = cfg.task_id_base
        except Exception:
            pass

    from kanban_framework.infra.filesystem import Filesystem as _FS
    _py_bin, _ = _FS.resolve_python()

    return {
        "project_root": str(root),
        "has_kanban": kanban_dir.is_dir(),
        "kanban_dir": str(kanban_dir),
        "ok": kanban_dir.is_dir(),
        "python": _py_bin,
        "agent_sync": {"in_sync": len(agent_sync_issues) == 0, "issues": agent_sync_issues},
        "config_suggestions": [] if task_id_base else ["task_id_base not set — run kanban init and enter your worker ID (e.g. worker ID 6696 → TASK-669601)"],
    }


def _check_agent_sync() -> list[str]:
    from pathlib import Path
    kanban_root = Path(__file__).resolve().parent.parent.parent
    agents_dir = kanban_root / "agents"
    skill_dir = kanban_root / "kanban_framework" / "_skill" / "agents"
    issues = []
    if not agents_dir.is_dir() or not skill_dir.is_dir():
        return issues
    for f in agents_dir.glob("*.md"):
        other = skill_dir / f.name
        if not other.is_file():
            issues.append(f"{f.name}: missing in _skill/agents/")
        elif not _files_equal(f, other):
            issues.append(f"{f.name}: out of sync")
    return issues


def _files_equal(a: Path, b: Path) -> bool:
    return hashlib.md5(a.read_bytes()).hexdigest() == hashlib.md5(b.read_bytes()).hexdigest()


def _cmd_sync_agents(args: list[str]) -> dict:
    from pathlib import Path
    kanban_root = Path(__file__).resolve().parent.parent.parent
    agents_dir = kanban_root / "agents"
    skill_dir = kanban_root / "kanban_framework" / "_skill" / "agents"
    if not agents_dir.is_dir():
        return {"error": "agents/ directory not found"}

    skill_dir.mkdir(parents=True, exist_ok=True)
    synced = []
    for f in agents_dir.glob("*.md"):
        target = skill_dir / f.name
        target.write_bytes(f.read_bytes())
        synced.append(f.name)
    return {"synced": synced, "count": len(synced)}
