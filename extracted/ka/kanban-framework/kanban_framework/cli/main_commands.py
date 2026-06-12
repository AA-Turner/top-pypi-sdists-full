"""CLI maintenance commands — stats, update, check-env, sync-agents."""
from __future__ import annotations

import hashlib
import json
import sys
import time


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
