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

_SKIP_NAMES = {"node_modules", "__pycache__", ".DS_Store", "src"}
_SKIP_EXTS = {".pid", ".log"}
_SCRIPTS = {"api.py"}
_ASSET_DIRS = {"css", "static"}


def _source_dir() -> Path:
    """Locate the dashboard files shipped inside the kanban_framework package."""
    # 1. importlib.resources (Python 3.9+)
    try:
        import importlib.resources as ir
        base = ir.files("kanban_framework")
        d = base / "dashboard"
        if (d / "api.py").is_file():
            return d
    except Exception:
        pass
    # 2. Fallback via __file__
    d = Path(__file__).resolve().parent.parent / "dashboard"
    if (d / "api.py").is_file():
        return d
    # 3. Dev layout: .claude/skills/kanban/kanban_framework/dashboard/
    d = Path(__file__).resolve().parent.parent.parent / "dashboard"
    if (d / "api.py").is_file():
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

    def _find_by_port(self, port: int) -> int | None:
        """Find PID of process listening on a port. Cross-platform."""
        if sys.platform == "win32":
            try:
                result = subprocess.run(
                    ["netstat", "-ano", "-p", "TCP"],
                    capture_output=True, text=True, timeout=10
                )
                for line in result.stdout.splitlines():
                    if f":{port}" in line and "LISTENING" in line:
                        parts = line.strip().split()
                        return int(parts[-1])
            except Exception:
                pass
        else:
            try:
                result = subprocess.run(
                    ["lsof", "-ti", f":{port}"],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0 and result.stdout.strip():
                    return int(result.stdout.strip().split()[0])
            except Exception:
                pass
        return None

    def check_env(self) -> dict:
        """Pre-flight check: verify dashboard can start."""
        issues = []
        ok = []
        # Python (always available since we're running in it)
        ok.append(f"python ({Filesystem.resolve_python()[0]})")
        # FastAPI
        try:
            import fastapi
            ok.append(f"fastapi ({fastapi.__version__})")
        except ImportError:
            issues.append("fastapi not installed — pip install kanban-framework")
        # uvicorn
        try:
            import uvicorn
            ok.append(f"uvicorn ({uvicorn.__version__})")
        except ImportError:
            issues.append("uvicorn not installed")
        return {
            "ready": len(issues) == 0,
            "ok": ok,
            "issues": issues,
            "fix_hint": "pip install kanban-framework" if issues else None,
        }

    def _ensure_node_modules(self) -> None:
        """No-op — FastAPI dashboard has no npm dependencies."""
        pass

    def status(self) -> dict:
        pid = self._read_pid()
        running = self._is_running(pid)
        deployed = (self._deploy_dir / "api.py").is_file()
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

    # Ports blocked by Chrome/Firefox — browser refuses connection
    _UNSAFE_PORTS = frozenset({
        1, 7, 9, 11, 13, 15, 17, 19, 20, 21, 22, 23, 25, 37, 42, 43, 53, 69, 77, 79,
        87, 95, 101, 102, 103, 104, 109, 110, 111, 113, 115, 117, 119, 123, 135, 137,
        139, 143, 161, 179, 389, 427, 465, 512, 513, 514, 515, 526, 530, 531, 532,
        540, 548, 554, 556, 563, 587, 601, 636, 989, 990, 993, 995, 1719, 1720, 1723,
        2049, 3659, 4045, 4190, 5060, 5061, 6000, 6566, 6665, 6666, 6667, 6668, 6669,
        6697, 10080,
    })

    def start(self, port: int | None = None) -> dict:
        # Deploy first
        self.deploy()
        # Validate port
        actual_port = port or self._read_port() or 3000
        if actual_port in self._UNSAFE_PORTS:
            return {
                "started": False,
                "reason": "unsafe_port",
                "port": actual_port,
                "hint": f"Port {actual_port} is blocked by browsers (Chrome/Firefox). Use a different port.",
            }
        pid = self._read_pid()
        if self._is_running(pid):
            return {"started": False, "reason": "already_running", "pid": pid}
        # Clean up stale PID file
        if pid and not self._is_running(pid):
            self._pid_file().unlink(missing_ok=True)
            pid = None
        # Check for port conflict from stale/crashed process
        if self._port_in_use(actual_port):
            port_pid = self._find_by_port(actual_port)
            if port_pid and port_pid != pid:
                self._kill_process(port_pid)
                import time
                time.sleep(0.5)
                if self._port_in_use(actual_port):
                    return {
                        "started": False,
                        "reason": "port_in_use",
                        "port": actual_port,
                        "hint": f"Port {actual_port} is occupied and could not be freed.",
                    }
            else:
                return {
                    "started": False,
                    "reason": "port_in_use",
                    "port": actual_port,
                    "hint": f"Port {actual_port} is occupied by another process.",
                }
        # Start uvicorn with FastAPI app
        env = os.environ.copy()
        env["KANBAN_ROOT"] = str(self._kanban_dir)
        log = open(self._log_file(), "w")
        kwargs = {
            "cwd": str(self._deploy_dir),
            "stdout": log,
            "stderr": log,
            "env": env,
        }
        if self._is_windows():
            flags = 0
            for attr in ("CREATE_NEW_PROCESS_GROUP", "DETACHED_PROCESS", "CREATE_NO_WINDOW"):
                if hasattr(subprocess, attr):
                    flags |= getattr(subprocess, attr)
            if flags:
                kwargs["creationflags"] = flags
            kwargs["start_new_session"] = True
        # Launch uvicorn with the FastAPI app
        _py_bin, _ = Filesystem.resolve_python()
        proc = subprocess.Popen([
            _py_bin, "-m", "uvicorn",
            "kanban_framework.dashboard.api:create_app",
            "--factory",
            "--host", "127.0.0.1",
            "--port", str(actual_port),
            "--no-access-log",
        ], **kwargs)
        self._pid_file().write_text(str(proc.pid))
        self._port_file().write_text(str(actual_port))
        return {"started": True, "pid": proc.pid, "port": actual_port, "deploy_dir": str(self._deploy_dir)}

    def stop(self) -> dict:
        pid = self._read_pid()
        port = self._read_port()
        if not self._is_running(pid):
            # PID stale — try to find and kill by port
            self._pid_file().unlink(missing_ok=True)
            if port:
                port_pid = self._find_by_port(port)
                if port_pid:
                    self._kill_process(port_pid)
                    self._port_file().unlink(missing_ok=True)
                    return {"stopped": True, "pid": port_pid, "reason": "killed_by_port"}
            return {"stopped": False, "reason": "not_running"}
        self._kill_process(pid)
        self._pid_file().unlink(missing_ok=True)
        self._port_file().unlink(missing_ok=True)
        return {"stopped": True, "pid": pid}

    def _read_port(self) -> int | None:
        port_path = self._port_file()
        if not port_path.exists():
            return None
        try:
            return int(port_path.read_text().strip())
        except (ValueError, OSError):
            return None

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
