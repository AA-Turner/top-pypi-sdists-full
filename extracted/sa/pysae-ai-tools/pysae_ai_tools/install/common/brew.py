"""Helper for installing packages via Homebrew on macOS.

Mirrors :mod:`pysae_ai_tools.install.common.winget`: returns ``None`` if brew
is unavailable so callers fall through to the next strategy. Surfaces a real
error from brew as ``InstallReport(error=...)``.
"""

import shutil
import subprocess

from .base import InstallReport
from .platform import detect


def is_available() -> bool:
    """True when running on macOS and the ``brew`` binary is on PATH."""
    try:
        plat = detect()
    except ValueError:
        return False
    if not plat.is_macos:
        return False
    return shutil.which("brew") is not None


def install(package: str, *, cask: bool = False) -> InstallReport | None:
    """Install ``package`` via brew. ``cask=True`` for GUI applications."""
    if not is_available():
        return None
    cmd = ["brew", "install"]
    if cask:
        cmd.append("--cask")
    cmd.append(package)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)
    if r.returncode != 0:
        return InstallReport(error=f"brew: {r.stderr.strip() or r.stdout.strip()}")
    return InstallReport(method="brew")
