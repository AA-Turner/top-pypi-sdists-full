"""CLI maintenance commands — track, stats, update, check-env, sync-agents."""
from __future__ import annotations

import hashlib
import json
import sys
import time


def _is_pre_release(version: str) -> bool:
    """Check if a version string is a pre-release (PEP 440)."""
    import re
    return bool(re.search(r'(a|b|rc|alpha|beta|dev)\d*', version))


def _cmd_track(args: list[str]) -> dict:
    """Record token/time tracking for a task phase."""
    from kanban_framework.infra.filesystem import Filesystem
    from kanban_framework.infra.token_tracking import TokenTracker

    fs = Filesystem(Filesystem.find_project_root())
    reports_dir = fs.kanban_dir / "reports"
    fs.ensure_dir(reports_dir)

    task_id = args[0] if len(args) > 0 else ""
    phase = args[1] if len(args) > 1 else ""
    use_auto = "--auto" in args
    args = [a for a in args if a != "--auto"]
    tokens = int(args[2]) if len(args) > 2 and args[2] != "--auto" else 0
    agent = ""
    model = ""
    duration = 0.0
    step_id = ""
    for i, a in enumerate(args):
        if a == "--agent" and i + 1 < len(args):
            agent = args[i + 1]
        elif a == "--model" and i + 1 < len(args):
            model = args[i + 1]
        elif a == "--duration" and i + 1 < len(args):
            try: duration = float(args[i + 1])
            except ValueError: pass
        elif a == "--step" and i + 1 < len(args):
            step_id = args[i + 1]

    if not task_id or not phase:
        return {"error": "usage: kanban track <task_id> <phase> <tokens> [--agent <name>] [--step <step_id>] [--model <model>] [--duration <seconds>]"}

    import os as _os
    session_id = _os.environ.get("CLAUDE_CODE_SESSION_ID", "")
    for i, a in enumerate(args):
        if a == "--session" and i + 1 < len(args):
            session_id = args[i + 1]

    tt = TokenTracker(reports_dir / "token_tracking.json")

    if use_auto:
        from kanban_framework.domain.task import TaskManager
        tm = TaskManager(fs)
        try:
            task = tm.show(task_id)
            t_min = None; t_max = None
            for h in task.history:
                if h.get("phase") == phase:
                    ts = h.get("started_at")
                    if ts and t_min is None: t_min = ts - 30
                    ts = h.get("completed_at")
                    if ts: t_max = ts + 30 if t_max is None else max(t_max, ts + 30)
            if t_min and t_max:
                stats = tt.auto_collect(task_id, phase, t_min, t_max)
                return {"task_id": task_id, "phase": phase, "auto_collected": True,
                        "tokens": stats.get("total_tokens", 0),
                        "prompts": stats.get("prompt_count", 0)}
        except Exception:
            pass
        return {"task_id": task_id, "phase": phase, "auto_collected": False,
                "error": "Could not auto-collect — no phase history timestamps"}

    tt.track(task_id, tokens, phase, agent, model, duration)

    if session_id:
        entry = tt._data.setdefault(task_id, tt._data.get(task_id, {}))
        entry.setdefault("sessions", [])
        if session_id not in entry["sessions"]:
            entry["sessions"].append(session_id)
        entry.setdefault("session_phases", {})
        entry["session_phases"].setdefault(phase, [])
        if session_id not in entry["session_phases"][phase]:
            entry["session_phases"][phase].append(session_id)
        if step_id:
            entry.setdefault("session_steps", {})
            entry["session_steps"].setdefault(step_id, [])
            if session_id not in entry["session_steps"][step_id]:
                entry["session_steps"][step_id].append(session_id)
        tt._save()

    return {"tracked": task_id, "phase": phase, "tokens": tokens,
            "agent": agent, "model": model, "duration": duration,
            "session_id": session_id, "step": step_id}


def _cmd_stats(args: list[str]) -> dict:
    """Return token/time stats via the configured StatsBackend."""
    from kanban_framework.infra.filesystem import Filesystem
    from kanban_framework.infra.stats_backend import resolve_stats_backend

    fs = Filesystem(Filesystem.find_project_root())
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

    days = int(stats_cfg.get("days", 30))
    return backend.get_stats(days=days)


def _cmd_help(args: list[str], cmd_map: dict) -> dict:
    return {"commands": sorted(cmd_map.keys())}


_STABLE_VERSION = "0.75.2"

def _cmd_update(args: list[str]) -> dict:
    """Upgrade kanban-framework and sync skill files.

    Channels:
      --channel stable (default) → v0.75.2 — last stable before workflow redesign
      --channel latest            → latest PyPI version (v0.96+)
      --channel dev               → latest pre-release
    """
    import subprocess as _sp

    if args and args[0] == "--list":
        try:
            import urllib.request
            url = "https://pypi.org/pypi/kanban-framework/json"
            data = json.loads(urllib.request.urlopen(url, timeout=10).read())
            versions = sorted(data.get("releases", {}).keys(), reverse=True)[:20]
            return {"action": "list_versions", "count": len(versions), "versions": versions}
        except Exception as e:
            return {"action": "list_versions", "error": str(e)}

    if args and args[0] == "--channels":
        try:
            import urllib.request
            url = "https://pypi.org/pypi/kanban-framework/json"
            data = json.loads(urllib.request.urlopen(url, timeout=10).read())
            all_v = sorted(data.get("releases", {}).keys(), reverse=True)
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

    if target:
        cmd = [sys.executable, "-m", "pip", "install", f"kanban-framework=={target}"]
    elif channel == "stable":
        cmd = [sys.executable, "-m", "pip", "install", f"kanban-framework=={_STABLE_VERSION}"]
    elif use_pre:
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "--pre", "kanban-framework"]
    else:
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "kanban-framework"]

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
            [sys.executable, "-m", "kanban_framework", "init", "--apply", "--non-interactive"]
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

    return {
        "project_root": str(root),
        "has_kanban": kanban_dir.is_dir(),
        "kanban_dir": str(kanban_dir),
        "ok": kanban_dir.is_dir(),
        "python": sys.executable,
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


def _files_equal(a: 'Path', b: 'Path') -> bool:
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
