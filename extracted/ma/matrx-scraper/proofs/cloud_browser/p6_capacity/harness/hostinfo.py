"""Host shape + image/tool versions. Phase-0 proof harness (NOT shipped code).

Two capacity reports are only comparable if you know what they ran on. Everything in
RESULTS-TEMPLATE.md's "host shape" and "image versions" sections comes from here, so the
operator never types it by hand and never gets it wrong.
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
from pathlib import Path

from .credits import imds_identity


def _first_line(cmd: list[str], timeout: float = 8.0) -> str | None:
    exe = shutil.which(cmd[0])
    if not exe:
        return None
    try:
        run = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return None
    text = (run.stdout or run.stderr or "").strip()
    return text.splitlines()[0] if text else None


def _meminfo_total_bytes() -> int | None:
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal:"):
                return int(line.split()[1]) * 1024
    except (OSError, ValueError, IndexError):
        pass
    return None


def _cpu_model() -> str | None:
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.lower().startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return None


def _in_container() -> bool:
    if Path("/.dockerenv").exists():
        return True
    try:
        return (
            "docker" in Path("/proc/1/cgroup").read_text()
            or "kubepods" in Path("/proc/1/cgroup").read_text()
        )
    except OSError:
        return False


def _cgroup_limits() -> dict[str, object]:
    """A container's own limits -- if these are tighter than the host, the numbers are
    NOT host capacity numbers and the report says so."""
    out: dict[str, object] = {"cgroup_v2": Path("/sys/fs/cgroup/cgroup.controllers").exists()}
    cpu_max = Path("/sys/fs/cgroup/cpu.max")
    mem_max = Path("/sys/fs/cgroup/memory.max")
    if cpu_max.exists():
        out["cpu_max"] = cpu_max.read_text().strip()
    if mem_max.exists():
        out["memory_max"] = mem_max.read_text().strip()
    return out


def _gpu() -> dict[str, object]:
    smi = shutil.which("nvidia-smi")
    if not smi:
        return {"present": False, "reason": "nvidia-smi not on PATH"}
    line = _first_line(
        ["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"]
    )
    if not line:
        return {"present": False, "reason": "nvidia-smi present but returned nothing"}
    return {"present": True, "gpu": line}


def collect(extra: dict | None = None) -> dict:
    info: dict[str, object] = {
        "collected_by": "p6_capacity/harness/hostinfo.py",
        "hostname": platform.node(),
        "kernel": platform.release(),
        "arch": platform.machine(),
        "python": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "cpu_model": _cpu_model(),
        "mem_total_bytes": _meminfo_total_bytes(),
        "in_container": _in_container(),
        "cgroup": _cgroup_limits(),
        "ec2": imds_identity(),
        "gpu": _gpu(),
        "tools": {
            "docker": _first_line(["docker", "--version"]),
            "ffmpeg": _first_line(["ffmpeg", "-version"]),
            "Xvfb": "present" if shutil.which("Xvfb") else None,
            "xdotool": _first_line(["xdotool", "--version"]),
            "aws": _first_line(["aws", "--version"]),
            "node": _first_line(["node", "--version"]),
        },
        "images": {
            "browser_image": os.environ.get("P6_BROWSER_IMAGE"),
            "sandbox_image": os.environ.get("P6_SANDBOX_IMAGE"),
            "selkies_image": os.environ.get("P6_SELKIES_IMAGE"),
        },
    }
    try:
        from importlib.metadata import version as _pkg_version

        info["playwright_python"] = _pkg_version("playwright")
    except Exception:  # noqa: BLE001 - version probe must never fail a run
        info["playwright_python"] = None
    info["playwright_browsers_path"] = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    chromium = _chromium_version()
    info["chromium"] = chromium
    if extra:
        info.update(extra)
    return info


def _chromium_version() -> str | None:
    root = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"))
    if not root.exists():
        return None
    for entry in sorted(root.glob("chromium-*")):
        exe = entry / "chrome-linux" / "chrome"
        if exe.exists():
            return _first_line([str(exe), "--version"]) or entry.name
    return None


def as_json(info: dict) -> str:
    return json.dumps(info, indent=2, sort_keys=True)
