"""Pysae shared tools for Claude Code skills."""

import re
import subprocess
from importlib.metadata import version as _pkg_version
from pathlib import Path


def compute_version(build: bool = False) -> str:
    """Compute the current version from git describe.

    Args:
        build: If True, return a clean version without .dev suffix (for CI publishing).
               If False (default), append .dev+g<sha> for non-tagged commits.

    Returns:
        Version string like "0.2.17" (build) or "0.2.17.dev+gabcdef" (dev).
    """
    pkg_dir = Path(__file__).resolve().parent
    cwd = str(pkg_dir)

    try:
        # Try git describe first (tag-based)
        desc = subprocess.run(
            ["git", "describe", "--tags", "--long", "--match", "v*"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            cwd=cwd,
        )
        if desc.returncode == 0 and desc.stdout.strip():
            m = re.match(r"^v?(\d+\.\d+\.\d+)-(\d+)-g([0-9a-f]+)$", desc.stdout.strip())
            if m:
                base, dist, sha = m.group(1), int(m.group(2)), m.group(3)
                major, minor, patch = base.split(".")
                if dist == 0:
                    return base
                ver = f"{major}.{minor}.{int(patch) + dist}"
                return ver if build else f"{ver}.dev+g{sha}"

        # No tags: fallback to commit count
        count = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            cwd=cwd,
        )
        sha_short = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            cwd=cwd,
        )
        c = count.stdout.strip() if count.returncode == 0 else "0"
        s = sha_short.stdout.strip() if sha_short.returncode == 0 else ""
        ver = f"0.1.{c}"
        if build or not s:
            return ver
        return f"{ver}.dev+g{s}"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return "0.1.0.dev" if not build else "0.1.0"


# Package version: use metadata for pip-installed, compute for editable
__version__ = _pkg_version("pysae-ai-tools")
if __version__ == "0.1.0":
    __version__ = compute_version(build=False)
