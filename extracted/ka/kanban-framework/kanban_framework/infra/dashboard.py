from __future__ import annotations

# Backward compat alias
DashboardBuilder = None  # resolved after class definition
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
from pathlib import Path

_SKIP_NAMES = {"node_modules", "__pycache__", ".DS_Store"}
_SKIP_EXTS = {".pid", ".log"}
_SCRIPTS = {"server.js", "package.json"}
_ASSET_DIRS = {"css", "js", "tests"}


def _source_dir() -> Path:
    """Locate the dashboard files shipped inside the kanban_framework package."""
    # 1. importlib.resources (Python 3.9+)
    try:
        import importlib.resources as ir
        base = ir.files("kanban_framework")
        d = base / "dashboard"
        if (d / "server.js").is_file():
            return d
    except Exception:
        pass
    # 2. Fallback via __file__
    d = Path(__file__).resolve().parent.parent / "dashboard"
    if (d / "server.js").is_file():
        return d
    # 3. Dev layout: .claude/skills/kanban/kanban_framework/dashboard/
    d = Path(__file__).resolve().parent.parent.parent / "dashboard"
    if (d / "server.js").is_file():
        return d
    raise FileNotFoundError("dashboard source not found in kanban_framework package")


class DashboardManager:
    """Deploy dashboard files from the pip package to .kanban/dashboard/ and manage the server."""

    def __init__(self, kanban_dir: Path):
        self._kanban_dir = Path(kanban_dir)
        self._deploy_dir = self._kanban_dir / "dashboard"
        self._source = _source_dir()

    # ── Data query (backward compat) ──

    def build(self) -> dict:
        """Return dashboard summary data (legacy behavior)."""
        tasks = []
        for f in sorted(self._kanban_dir.joinpath("tasks").glob("TASK-*.json")):
            tasks.append(json.loads(f.read_text(encoding="utf-8")))
        by_status: dict[str, int] = {}
        by_phase: dict[str, int] = {}
        for t in tasks:
            by_status[t.get("status", "unknown")] = by_status.get(t.get("status", "unknown"), 0) + 1
            by_phase[t.get("phase", "unknown")] = by_phase.get(t.get("phase", "unknown"), 0) + 1
        return {
            "total": len(tasks),
            "by_status": by_status,
            "by_phase": by_phase,
            "tasks": [{"id": t["id"], "title": t["title"], "status": t.get("status")} for t in tasks],
        }

    # ── Deploy ──

    def deploy(self) -> dict:
        """Copy dashboard files from package to .kanban/dashboard/.

        Always performs a full sync: removes stale files from the deploy
        directory (preserving node_modules/) before copying fresh files.
        This guarantees the deployed dashboard exactly matches the installed
        package version.
        """
        # Preserve node_modules and runtime files across redeploys
        preserved = self._stash_runtime_files()
        # Wipe everything except node_modules
        self._clean_deploy_dir()
        # Restore runtime files
        self._restore_runtime_files(preserved)
        self._deploy_dir.mkdir(parents=True, exist_ok=True)
        copied, skipped = self._sync(self._source, self._deploy_dir)
        gitignore_status = self._ensure_gitignored()
        return {
            "deployed_to": str(self._deploy_dir),
            "copied": copied, "skipped": skipped,
            **gitignore_status,
        }

    def _stash_runtime_files(self) -> dict[str, bytes]:
        """Read runtime files (pid, port, log) into memory before cleanup."""
        stash = {}
        for name in ("server.pid", "server.port", "server.log"):
            p = self._deploy_dir / name
            if p.is_file():
                try:
                    stash[name] = p.read_bytes()
                except OSError:
                    pass
        return stash

    def _restore_runtime_files(self, stash: dict[str, bytes]) -> None:
        """Write back runtime files after cleanup."""
        for name, data in stash.items():
            p = self._deploy_dir / name
            try:
                p.write_bytes(data)
            except OSError:
                pass

    def _clean_deploy_dir(self) -> None:
        """Remove all files under deploy dir except node_modules/."""
        if not self._deploy_dir.is_dir():
            return
        for item in list(self._deploy_dir.iterdir()):
            if item.name == "node_modules":
                continue  # preserve npm dependencies
            if item.is_dir():
                shutil.rmtree(str(item), ignore_errors=True)
            else:
                try:
                    item.unlink()
                except OSError:
                    pass

    def _ensure_gitignored(self) -> dict:
        """Append .kanban/dashboard/ to project .gitignore if missing."""
        project_root = self._kanban_dir.parent
        gitignore = project_root / ".gitignore"
        entry = ".kanban/dashboard/"
        # Collect existing lines
        lines = []
        if gitignore.is_file():
            lines = gitignore.read_text(encoding="utf-8").splitlines()
            # Already present? (match whole line after stripping)
            for line in lines:
                if line.strip() == entry:
                    return {"gitignore": "already_present"}
        # Append
        content = "\n".join(lines)
        if content and not content.endswith("\n"):
            content += "\n"
        content += entry + "\n"
        gitignore.write_text(content, encoding="utf-8")
        return {"gitignore": "added"}

    def _sync(self, src: Path, dst: Path) -> tuple[int, int]:
        """Full copy of all source files to deploy directory."""
        copied = 0
        skipped = 0

        for item in src.rglob("*"):
            rel = item.relative_to(src)
            if any(p in _SKIP_NAMES for p in rel.parts):
                continue
            if rel.suffix in _SKIP_EXTS:
                continue
            if rel.name == "package-lock.json":
                continue
            target = dst / rel
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(item), str(target))
            copied += 1
        return copied, skipped

    # ── Start / Stop / Status ──

    def _pid_file(self) -> Path:
        return self._deploy_dir / "server.pid"

    def _port_file(self) -> Path:
        return self._deploy_dir / "server.port"

    def _log_file(self) -> Path:
        return self._deploy_dir / "server.log"

    def _read_pid(self) -> int | None:
        pid_path = self._pid_file()
        if not pid_path.exists():
            return None
        try:
            return int(pid_path.read_text().strip())
        except (ValueError, OSError):
            return None

    @staticmethod
    def _is_windows() -> bool:
        return sys.platform == "win32"

    @staticmethod
    def _kill_process(pid: int) -> None:
        """Kill a process by PID, cross-platform."""
        if sys.platform == "win32":
            try:
                subprocess.run(
                    ["taskkill", "/PID", str(pid), "/F", "/T"],
                    capture_output=True, timeout=10
                )
            except Exception:
                try:
                    os.kill(pid, 9)  # SIGKILL equivalent on Windows
                except Exception:
                    pass
        else:
            try:
                os.killpg(os.getpgid(pid), signal.SIGTERM)
            except (ProcessLookupError, OSError):
                try:
                    os.kill(pid, signal.SIGTERM)
                except Exception:
                    pass

    def _is_running(self, pid: int | None) -> bool:
        if pid is None:
            return False
        try:
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, PermissionError, OSError):
            return False

    def check_env(self) -> dict:
        """Pre-flight check: verify dashboard can start."""
        import shutil as _shutil
        issues = []
        ok = []
        # Node.js
        node = _shutil.which("node")
        if node:
            ok.append(f"node ({node})")
        else:
            issues.append("Node.js not found — install from https://nodejs.org")
        # npm
        npm = _shutil.which("npm")
        if npm:
            ok.append(f"npm ({npm})")
        else:
            issues.append("npm not found")
        # Express (key dependency)
        express = self._deploy_dir / "node_modules" / "express" / "index.js"
        if express.is_file():
            ok.append("express (installed)")
        else:
            issues.append("express not installed — run: kanban dashboard start")
        return {
            "ready": len(issues) == 0,
            "ok": ok,
            "issues": issues,
            "fix_hint": "kanban dashboard start" if issues else None,
        }

    def _ensure_node_modules(self) -> None:
        """Install npm dependencies if node_modules is missing or incomplete."""
        nm = self._deploy_dir / "node_modules"
        # Check for key dependency (express), not just directory existence
        express_index = nm / "express" / "index.js"
        if nm.is_dir() and express_index.is_file():
            return
        # npm available?
        npm = shutil.which("npm")
        if not npm:
            raise RuntimeError(
                "npm not found — install Node.js (https://nodejs.org) to use the dashboard"
            )
        # Remove stale node_modules if exists but incomplete
        if nm.is_dir() and not express_index.is_file():
            shutil.rmtree(str(nm), ignore_errors=True)
        # Install — bypass npm proxy to avoid connection failures (#241)
        env = os.environ.copy()
        for proxy_var in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"):
            env.pop(proxy_var, None)
        env["NPM_CONFIG_PROXY"] = ""
        env["NPM_CONFIG_HTTPS-PROXY"] = ""
        result = subprocess.run(
            [npm, "install"],
            cwd=str(self._deploy_dir),
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            env=env,
        )
        if result.returncode != 0:
            err = result.stderr.strip() or "npm install failed"
            raise RuntimeError(f"npm install failed: {err}")

    def status(self) -> dict:
        pid = self._read_pid()
        running = self._is_running(pid)
        deployed = (self._deploy_dir / "server.js").is_file()
        port_file = self._port_file()
        saved_port = int(port_file.read_text().strip()) if port_file.exists() else 3000
        return {
            "deployed": deployed,
            "running": running,
            "pid": pid if running else None,
            "port": saved_port,
            "deploy_dir": str(self._deploy_dir),
        }

    @staticmethod
    def _port_in_use(port: int) -> bool:
        """Check if a TCP port is already in use."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex(("127.0.0.1", port)) == 0

    def start(self, port: int | None = None) -> dict:
        # Deploy first
        self.deploy()
        # Install deps
        self._ensure_node_modules()
        # Check if already running
        pid = self._read_pid()
        if self._is_running(pid):
            return {"started": False, "reason": "already_running", "pid": pid}
        # Check for port conflict from other projects
        actual_port = port or 3000
        if self._port_in_use(actual_port):
            return {
                "started": False,
                "reason": "port_in_use",
                "port": actual_port,
                "hint": f"Port {actual_port} is occupied by another process. Stop it first or use --port to pick a different one.",
            }
        # Start server
        env = os.environ.copy()
        env["KANBAN_ROOT"] = str(self._kanban_dir)
        if port:
            env["PORT"] = str(port)
        log = open(self._log_file(), "w")
        kwargs = {
            "cwd": str(self._deploy_dir),
            "stdout": log,
            "stderr": log,
            "env": env,
        }
        if self._is_windows():
            # Windows: detach from console without requiring process group
            flags = 0
            for attr in ("CREATE_NEW_PROCESS_GROUP", "DETACHED_PROCESS", "CREATE_NO_WINDOW"):
                if hasattr(subprocess, attr):
                    flags |= getattr(subprocess, attr)
            if flags:
                kwargs["creationflags"] = flags
            kwargs["start_new_session"] = True
        proc = subprocess.Popen(["node", "server.js"], **kwargs)
        self._pid_file().write_text(str(proc.pid))
        self._port_file().write_text(str(port or 3000))
        return {"started": True, "pid": proc.pid, "port": port or 3000, "deploy_dir": str(self._deploy_dir)}

    def stop(self) -> dict:
        pid = self._read_pid()
        if not self._is_running(pid):
            self._pid_file().unlink(missing_ok=True)
            return {"stopped": False, "reason": "not_running"}
        self._kill_process(pid)
        self._pid_file().unlink(missing_ok=True)
        return {"stopped": True, "pid": pid}

    def restart(self, port: int | None = None) -> dict:
        self.stop()
        return self.start(port)


# Backward compat: DashboardBuilder wraps DashboardManager.build()
class DashboardBuilder:
    """Legacy alias — use DashboardManager instead."""
    def __init__(self, tasks_dir: Path):
        kanban_dir = tasks_dir.parent
        self._mgr = DashboardManager(kanban_dir)

    def build(self) -> dict:
        return self._mgr.build()
