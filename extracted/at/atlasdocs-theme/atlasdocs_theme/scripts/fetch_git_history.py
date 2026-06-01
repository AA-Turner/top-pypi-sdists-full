from __future__ import annotations

"""
Git history provider — single source of truth for all commit history lookups.

Reads a single `git log` call over the entire docs/ tree and merges it with
a JSON cache of source-repo history (written by import_docs). The result is
the `commit_map` dict consumed by prepare_directory_pages and other scripts.
"""

import hashlib
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict


# ── Configuration ──────────────────────────────────────────────────────────────

# Maximum number of commits fetched in a single git log call
GIT_LOG_MAX_COMMITS = 5000

# Seconds before git log is abandoned and cache-only history is used
GIT_LOG_TIMEOUT_SECONDS = 120

# Default location of the source-repo history cache written by import_docs
DEFAULT_CACHE_FILE = Path(".git_history_cache.json")

# Gravatar base URL used by get_gravatar_url()
GRAVATAR_BASE_URL = "https://www.gravatar.com/avatar"

# Commit fields and their git pretty-format specifiers (order is the wire format)
_GIT_COMMIT_FIELDS: list[tuple[str, str]] = [
    ("sha",     "%H"),
    ("author",  "%an"),
    ("email",   "%ae"),
    ("date",    "%cI"),
    ("message", "%s"),
]
_GIT_SEPARATOR = "\x01"
_GIT_FMT = _GIT_SEPARATOR.join(spec for _, spec in _GIT_COMMIT_FIELDS)


# ── Types ──────────────────────────────────────────────────────────────────────

class Commit(TypedDict):
    sha: str
    author: str
    email: str
    date: str
    message: str


# commit_map maps docs-relative file path → list of commits, newest first
CommitMap = dict[str, list[Commit]]


# ── Merge strategy ─────────────────────────────────────────────────────────────

def _merge_histories(cached: CommitMap, fresh: CommitMap) -> CommitMap:
    """Merge cached source-repo history with hub-native git log.

    Hub-native (fresh) takes precedence per file so that any file that exists
    in both repos shows the hub's authoritative history, not the origin's.
    Files only in the cache (not yet re-committed on the hub) keep their
    source-repo history.
    """
    return {**cached, **fresh}


# ── Parser ─────────────────────────────────────────────────────────────────────

def _parse_git_log(output: str, docs_dir: str) -> CommitMap:
    """Parse `git log --pretty=format:... --name-only` output into a CommitMap."""
    index: CommitMap = {}
    current_commit: Commit | None = None
    prefix = f"{docs_dir}/"
    prefix_len = len(prefix)
    field_names = [name for name, _ in _GIT_COMMIT_FIELDS]
    n_fields = len(field_names)

    for line in output.split("\n"):
        if not line:
            continue
        if _GIT_SEPARATOR in line:
            parts = line.split(_GIT_SEPARATOR, n_fields - 1)
            if len(parts) == n_fields:
                current_commit = dict(zip(field_names, parts))  # type: ignore[arg-type]
        elif current_commit and line.startswith(prefix):
            rel_path = line[prefix_len:]
            if rel_path not in index:
                index[rel_path] = []
            index[rel_path].append(current_commit)

    return index


# ── Provider ───────────────────────────────────────────────────────────────────

class LocalGitHistoryProvider:
    """Reads git history from the local repository and an optional JSON cache.

    Call `load()` once to populate, then pass `.commit_map` to the prepare_*
    scripts. `save_cache()` persists the merged index for use in subsequent
    pipeline runs.
    """

    def __init__(
        self,
        cache_file: Path = DEFAULT_CACHE_FILE,
        docs_dir: str = "docs",
        repo_root: str | None = None,
    ) -> None:
        self._cache_file = cache_file
        self._docs_dir = docs_dir
        self._repo_root = repo_root
        self._index: CommitMap | None = None

    @property
    def commit_map(self) -> CommitMap:
        """The loaded index. Calls load() automatically if not yet loaded."""
        if self._index is None:
            self.load(self._docs_dir, self._repo_root)
        return self._index  # type: ignore[return-value]

    def get_history(self, file_path: str, max_entries: int = 50) -> list[Commit]:
        """Return commits for file_path (relative to docs root), newest first."""
        return self.commit_map.get(file_path, [])[:max_entries]

    def get_commit_count(self, file_path: str) -> int:
        """Return total number of commits that touched file_path."""
        return len(self.commit_map.get(file_path, []))

    def load(
        self,
        docs_dir: str = "docs",
        repo_root: str | None = None,
        max_commits: int = GIT_LOG_MAX_COMMITS,
    ) -> None:
        """Populate the in-memory index from git log and the cache file."""
        cached = self._load_cache_file()
        fresh = self._run_git_log(docs_dir, repo_root or os.getcwd(), max_commits)
        self._index = _merge_histories(cached, fresh)

        if cached:
            print(
                f"[git_history] Merged: {len(cached)} cached + {len(fresh)} hub-native "
                f"= {len(self._index)} total files"
            )
        else:
            print(f"[git_history] Loaded {len(self._index)} files from git log")

    def save_cache(self, output_file: Path | None = None) -> None:
        """Write the current index to a JSON cache file."""
        dest = output_file or self._cache_file
        with dest.open("w") as f:
            json.dump(self._index, f, separators=(",", ":"))
        print(f"[git_history] Wrote cache: {dest} ({len(self._index or {})} files)")

    def _load_cache_file(self) -> CommitMap:
        if not self._cache_file.exists():
            return {}
        try:
            with self._cache_file.open() as f:
                data = json.load(f)
            print(f"[git_history] Loaded cache: {self._cache_file} ({len(data)} files)")
            return data
        except Exception as exc:
            print(f"[git_history] Cache unreadable ({exc}), ignoring")
            return {}

    def _run_git_log(
        self,
        docs_dir: str,
        cwd: str,
        max_commits: int,
    ) -> CommitMap:
        start = time.monotonic()
        try:
            result = subprocess.run(
                [
                    "git", "log",
                    f"--pretty=format:{_GIT_FMT}",
                    "--name-only",
                    f"-{max_commits}",
                    "--",
                    f"{docs_dir}/",
                ],
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                timeout=GIT_LOG_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            print("[git_history] git log timed out — using cache only")
            return {}
        except subprocess.CalledProcessError as exc:
            print(f"[git_history] git log failed: {(exc.stderr or '').strip() or exc}")
            return {}
        except FileNotFoundError:
            print("[git_history] git not found on PATH")
            return {}

        index = _parse_git_log(result.stdout, docs_dir)
        print(f"[git_history] git log: {len(index)} files in {time.monotonic() - start:.2f}s")
        return index


# ── Utilities ──────────────────────────────────────────────────────────────────

def get_gravatar_url(email: str, size: int = 80) -> str:
    """Return a Gravatar URL for email, falling back to identicon if no profile exists."""
    if not email:
        return ""
    email_hash = hashlib.md5(email.lower().strip().encode("utf-8")).hexdigest()
    return f"{GRAVATAR_BASE_URL}/{email_hash}?s={size}&d=identicon"


def calculate_update_stats(commits: list[Commit]) -> dict:
    """Return update-frequency statistics derived from a list of commits.

    Keys returned:
        total_commits, avg_days_between_updates, first_commit_date,
        last_commit_date, unique_authors, update_frequency (human-readable)
    """
    stats: dict = {
        "total_commits": 0,
        "avg_days_between_updates": None,
        "first_commit_date": None,
        "last_commit_date": None,
        "unique_authors": [],
        "update_frequency": "unknown",
    }

    if not commits:
        return stats

    stats["total_commits"] = len(commits)

    dates: list[datetime] = []
    authors: set[str] = set()
    for commit in commits:
        authors.add(commit.get("author", "Unknown"))
        date_str = commit.get("date", "")
        if date_str:
            try:
                dates.append(datetime.fromisoformat(date_str))
            except Exception:
                pass

    stats["unique_authors"] = list(authors)

    if not dates:
        return stats

    dates.sort(reverse=True)
    stats["last_commit_date"] = dates[0].strftime("%Y-%m-%d")
    stats["first_commit_date"] = dates[-1].strftime("%Y-%m-%d")

    if len(dates) >= 2:
        avg_days = (dates[0] - dates[-1]).days / (len(dates) - 1)
        stats["avg_days_between_updates"] = round(avg_days, 1)

        if avg_days < 1:        freq = "multiple times per day"
        elif avg_days < 2:      freq = "daily"
        elif avg_days < 7:      freq = f"every {int(avg_days)} days"
        elif avg_days < 14:     freq = "weekly"
        elif avg_days < 30:     freq = f"every {int(avg_days / 7)} weeks"
        elif avg_days < 90:     freq = "monthly"
        elif avg_days < 365:    freq = f"every {int(avg_days / 30)} months"
        else:                   freq = "yearly or less"
        stats["update_frequency"] = freq

    return stats
