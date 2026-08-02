"""Disk-cached ``glab api`` wrapper and repo-path primitives shared inside common/.

Low-level helpers with no project-config knowledge: a thin ``glab api`` runner, a
TTL disk cache for stable cross-repo GitLab lookups, and the origin-remote →
GitLab path resolver. Extracted from :mod:`project_config` so :mod:`group` can use
them without importing ``project_config`` (which itself imports ``group``) — that
is what used to force a cycle-breaking local import.
"""

import hashlib
import json
import subprocess
import time
from pathlib import Path

from .glab.runner import run_glab


def _glab_api(*args: str) -> tuple[int, str, str]:
    """Run ``glab api <args>``; return (returncode, stdout, stderr). rc 127 if glab is absent."""
    res = run_glab("api", *args, timeout=20)
    return res.returncode, res.stdout, res.stderr


# A repo's config on GitLab is stable data — cache it on disk (TTL) so repeated
# cross-repo lookups (`project show --project`, `project list`) don't re-hit GitLab.
# The LOCAL read path is never cached (it must reflect uncommitted edits). `--refresh`
# bypasses the cache. The dynamic branch context (detect-context) is never cached.
CACHE_DIR = Path.home() / ".cache" / "pysae-ai-tools" / "project-config"
CACHE_TTL_SECONDS = 300  # 5 min


def _cache_file(key: str) -> Path:
    return CACHE_DIR / f"{hashlib.sha256(key.encode()).hexdigest()[:16]}.json"


def _cache_read(key: str) -> dict[str, object] | None:
    path = _cache_file(key)
    if not path.exists() or time.time() - path.stat().st_mtime > CACHE_TTL_SECONDS:
        return None
    try:
        data: dict[str, object] = json.loads(path.read_text(encoding="utf-8"))
        return data
    except (json.JSONDecodeError, OSError):
        return None


def _cache_write(key: str, data: dict[str, object]) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _cache_file(key).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass


def current_project_path(root: Path | None = None) -> str:
    """Return a repo's GitLab path (``group/repo``) from its ``origin`` remote.

    Runs ``git remote get-url origin`` in ``root`` (or the process cwd). Returns ``""``
    outside a repo, when origin is missing, or when the URL has no path component. Used
    to resolve stable routing for a repo without a glab round-trip.
    """
    try:
        out = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=str(root) if root is not None else None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""
    url = out.stdout.strip()
    if not url:
        return ""
    # git@gitlab.com:pysae/api.git  |  https://gitlab.com/pysae/api.git  |  ssh://git@host/grp/repo.git
    tail = url.split(":", 1)[1] if url.startswith("git@") else url.split("//", 1)[-1].split("/", 1)[-1]
    tail = tail.removesuffix(".git").strip("/")
    return tail if "/" in tail else ""  # a path-less host (e.g. "gitlab.com") is not a project path
