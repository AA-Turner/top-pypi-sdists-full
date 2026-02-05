"""
CSSL Service Manager - Runtime discovery engine.
Discovers Python/CSSL processes via marker files and psutil process enumeration.
"""
import json
import os
import re
import time
import threading
from pathlib import Path
from typing import Callable, Dict, List, Optional

from .models import RuntimeInfo

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


def _get_share_directory() -> Path:
    """Get the shared objects directory path."""
    if os.name == 'nt':
        base = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
    else:
        base = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config'))
    return base / 'IncludeCPP' / 'shared_objects'


class RuntimeScanner:
    """Discovers and monitors CSSL/Python runtime instances."""

    def __init__(self):
        self.discovered: Dict[str, RuntimeInfo] = {}
        self._lock = threading.Lock()
        self._scanning = False
        self._callbacks: List[Callable] = []

    @property
    def is_scanning(self) -> bool:
        return self._scanning

    def on_update(self, callback: Callable):
        """Register a callback for when scan results change."""
        self._callbacks.append(callback)

    def _notify(self):
        for cb in self._callbacks:
            try:
                cb(self.discovered)
            except Exception:
                pass

    # ── Marker File Scan ──────────────────────────────────────────
    def scan_markers(self) -> List[RuntimeInfo]:
        """Scan shared object marker files for active runtimes."""
        results = []
        share_dir = _get_share_directory()

        if not share_dir.exists():
            return results

        for f in share_dir.glob('*.shareobj*'):
            try:
                with open(f, 'r', encoding='utf-8') as fh:
                    data = json.load(fh)

                name = data.get('name', f.stem)
                obj_type = data.get('type', 'unknown')
                obj_id = data.get('id', 0)
                is_live = data.get('live', False)

                # Try to find the process that owns this object
                pid = self._find_owner_pid(f)
                if pid is None:
                    continue

                rid = f"{pid}_{int(f.stat().st_mtime)}"

                # Check if already known
                if rid in self.discovered:
                    self.discovered[rid].last_seen = time.time()
                    continue

                info = RuntimeInfo(
                    id=rid, pid=pid,
                    name=f"CSSL: {name} ({obj_type})",
                    language="CSSL",
                    status="discovered",
                    marker_file=str(f),
                    create_time=f.stat().st_mtime,
                )

                # Get process stats if psutil available
                if HAS_PSUTIL:
                    try:
                        proc = psutil.Process(pid)
                        info.memory_mb = proc.memory_info().rss / (1024 * 1024)
                        info.cpu_pct = proc.cpu_percent(interval=0.1)
                        info.cmdline = ' '.join(proc.cmdline()[:5])
                        info.uptime = time.time() - proc.create_time()
                        info.create_time = proc.create_time()
                        info.id = f"{pid}_{int(proc.create_time())}"
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

                results.append(info)
            except (json.JSONDecodeError, OSError):
                continue

        return results

    def _find_owner_pid(self, marker_path: Path) -> Optional[int]:
        """Try to find which PID created this marker file."""
        if not HAS_PSUTIL:
            return None

        # Check all Python processes for the marker
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'python' in proc.info['name'].lower():
                    # Check if process has the share directory open
                    try:
                        for f in proc.open_files():
                            if str(marker_path) in f.path:
                                return proc.pid
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        pass
            except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError):
                continue

        # Fallback: any python process that's running
        # (marker file exists = some process created it)
        python_procs = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                name = proc.info.get('name', '')
                if name and 'python' in name.lower():
                    cmdline = proc.info.get('cmdline', []) or []
                    cmd_str = ' '.join(cmdline)
                    if any(k in cmd_str.lower() for k in ['includecpp', 'cssl', 'cssl_bridge', 'cssl_runtime']):
                        python_procs.append(proc.pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if python_procs:
            return python_procs[0]
        return None

    # ── Process Scan ──────────────────────────────────────────────
    def scan_processes(self) -> List[RuntimeInfo]:
        """Scan running processes for Python/CSSL runtimes using psutil."""
        results = []
        if not HAS_PSUTIL:
            return results

        cssl_keywords = ['includecpp', 'cssl', 'cssl_runtime', 'cssl_bridge',
                         'csslruntime', 'cssl_stream']

        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time',
                                          'memory_info', 'status']):
            try:
                info = proc.info
                name = info.get('name', '')
                if not name:
                    continue

                is_python = 'python' in name.lower()
                if not is_python:
                    continue

                pid = info['pid']
                create_time = info.get('create_time', 0) or 0
                rid = f"{pid}_{int(create_time)}"

                # Skip if already discovered
                if rid in self.discovered:
                    # Update stats
                    existing = self.discovered[rid]
                    existing.last_seen = time.time()
                    try:
                        mem = info.get('memory_info')
                        if mem:
                            existing.memory_mb = mem.rss / (1024 * 1024)
                        existing.cpu_pct = proc.cpu_percent(interval=0)
                        existing.uptime = time.time() - create_time
                    except Exception:
                        pass
                    continue

                # Check cmdline for CSSL keywords
                cmdline = info.get('cmdline', []) or []
                cmd_str = ' '.join(cmdline).lower()
                is_cssl = any(k in cmd_str for k in cssl_keywords)

                # Determine language
                if is_cssl:
                    language = "Python/CSSL"
                else:
                    language = "Python"

                # Get memory
                mem_mb = 0.0
                mem = info.get('memory_info')
                if mem:
                    mem_mb = mem.rss / (1024 * 1024)

                display_cmd = ' '.join(cmdline[:5]) if cmdline else name

                runtime = RuntimeInfo(
                    id=rid, pid=pid, name=name,
                    language=language,
                    status="discovered",
                    memory_mb=mem_mb,
                    cpu_pct=0.0,
                    uptime=time.time() - create_time if create_time else 0,
                    cmdline=display_cmd,
                    create_time=create_time,
                )

                # Try to get CPU (non-blocking)
                try:
                    runtime.cpu_pct = proc.cpu_percent(interval=0)
                except Exception:
                    pass

                results.append(runtime)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        return results

    # ── Combined Scan ─────────────────────────────────────────────
    def scan_all(self, callback: Optional[Callable] = None) -> List[RuntimeInfo]:
        """Run all discovery methods and merge results."""
        self._scanning = True
        all_results = []

        try:
            # Marker file scan (fast)
            marker_results = self.scan_markers()
            all_results.extend(marker_results)

            # Process scan (slower)
            proc_results = self.scan_processes()
            all_results.extend(proc_results)

            # Merge into discovered
            with self._lock:
                for info in all_results:
                    if info.id not in self.discovered:
                        self.discovered[info.id] = info

                # Mark dead processes
                self._check_dead()
        finally:
            self._scanning = False

        self._notify()
        if callback:
            callback(all_results)

        return all_results

    def scan_all_async(self, callback: Optional[Callable] = None):
        """Run scan_all in a background thread."""
        t = threading.Thread(target=self.scan_all, args=(callback,), daemon=True)
        t.start()
        return t

    def _check_dead(self):
        """Mark processes that are no longer alive as dead."""
        if not HAS_PSUTIL:
            return

        dead_ids = []
        for rid, info in self.discovered.items():
            if info.status == "dead":
                continue
            if not psutil.pid_exists(info.pid):
                info.status = "dead"
                dead_ids.append(rid)

    def remove_dead(self):
        """Remove all dead runtimes from the discovered list."""
        with self._lock:
            dead = [k for k, v in self.discovered.items() if v.status == "dead"]
            for k in dead:
                del self.discovered[k]
        self._notify()

    def clear(self):
        """Clear all discovered runtimes."""
        with self._lock:
            self.discovered.clear()
        self._notify()

    def get_runtime(self, runtime_id: str) -> Optional[RuntimeInfo]:
        """Get a specific runtime by ID."""
        return self.discovered.get(runtime_id)

    def refresh_stats(self, runtime_id: str):
        """Refresh CPU/memory stats for a specific runtime."""
        info = self.discovered.get(runtime_id)
        if not info or not HAS_PSUTIL:
            return

        try:
            proc = psutil.Process(info.pid)
            info.memory_mb = proc.memory_info().rss / (1024 * 1024)
            info.cpu_pct = proc.cpu_percent(interval=0.1)
            info.uptime = time.time() - proc.create_time()
            info.last_seen = time.time()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            info.status = "dead"

    def kill_process(self, runtime_id: str) -> bool:
        """Kill a runtime process."""
        info = self.discovered.get(runtime_id)
        if not info or not HAS_PSUTIL:
            return False

        try:
            proc = psutil.Process(info.pid)
            proc.terminate()
            proc.wait(timeout=3)
            info.status = "dead"
            self._notify()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            try:
                proc.kill()
                info.status = "dead"
                self._notify()
                return True
            except Exception:
                return False
