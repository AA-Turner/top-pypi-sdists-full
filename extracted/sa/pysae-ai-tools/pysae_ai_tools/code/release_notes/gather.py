"""Git + filesystem data collection feeding the ``release-notes gather`` command.

These helpers read the repository (git log, ``changelogs/``) to produce the raw
material the skill hands to the LLM. Kept apart from the pure logic in
:mod:`.core` and the command layer in :mod:`.cli`.
"""

import re
import subprocess
from pathlib import Path

from .core import ChangelogPendingEntry, CommitInfo


def _run_git(repo_root: Path, *args: str, timeout: int = 15) -> str | None:
    """Run a ``git`` command inside ``repo_root``. Return stdout, or None on failure."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout


def resolve_latest_tag(repo_root: Path) -> str:
    """Return the latest local semver tag (``vX.Y.Z``), or empty string."""
    raw = _run_git(repo_root, "tag", "--list", "v*", "--sort=-v:refname", timeout=5)
    if not raw:
        return ""
    for line in raw.splitlines():
        candidate = line.strip()
        if re.match(r"^v\d+\.\d+\.\d+$", candidate):
            return candidate
    return ""


def list_commits_since_tag(repo_root: Path, tag: str) -> list[CommitInfo]:
    """List commits from ``tag`` (exclusive) to ``HEAD`` (inclusive), newest first.

    A NUL byte separates records (commits can contain newlines in their body).
    ``--no-merges`` skips merge commits to keep the list focused on actual changes.
    """
    sep = "\x1f"  # ASCII unit separator — safe inside commit bodies
    ref_range = f"{tag}..HEAD" if tag else "HEAD"
    raw = _run_git(
        repo_root,
        "log",
        "--no-merges",
        f"--format=%H{sep}%s{sep}%b%x00",
        ref_range,
    )
    if not raw:
        return []
    commits: list[CommitInfo] = []
    for chunk in raw.split("\x00"):
        chunk = chunk.strip("\n")
        if not chunk:
            continue
        parts = chunk.split(sep, 2)
        if len(parts) < 3:
            continue
        sha, subject, body = parts
        commits.append(CommitInfo(sha=sha.strip(), subject=subject.strip(), body=body.strip()))
    return commits


def list_pending_changelog_entries(repo_root: Path) -> list[ChangelogPendingEntry]:
    """Read ``<repo_root>/changelogs/*.md`` and return one entry per file."""
    cl_dir = repo_root / "changelogs"
    if not cl_dir.is_dir():
        return []
    entries: list[ChangelogPendingEntry] = []
    for path in sorted(cl_dir.glob("*.md")):
        content = path.read_text(encoding="utf-8").strip()
        first_line = content.splitlines()[0] if content else ""
        body = first_line.lstrip("*").strip() if first_line.lstrip().startswith("*") else first_line.strip()
        body = re.sub(r"\s*\(#\d+\)\s*$", "", body)
        match = re.match(r"^(\w+):\s*(.+)$", body)
        if match:
            entries.append(
                ChangelogPendingEntry(
                    file=path.name,
                    type=match.group(1).lower(),
                    description=match.group(2).strip(),
                    raw=first_line,
                )
            )
        else:
            entries.append(ChangelogPendingEntry(file=path.name, type="", description=body, raw=first_line))
    return entries
