from __future__ import annotations

import os
import re
import shutil
import tempfile
from typing import TypedDict

from bitfab.git_command import run_git

GIT_TIMEOUT_SECONDS = 30
DISABLE_ENV = "BITFAB_DISABLE_GIT_STATE"

_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")


class GitState(TypedDict):
    githubEmail: str | None
    branch: str | None
    commitSha: str | None
    baseSha: str | None
    experimentSha: str | None


def _text(value: str | None) -> str | None:
    trimmed = value.strip() if value is not None else None
    return trimmed or None


def _sha(value: str | None) -> str | None:
    trimmed = _text(value)
    return trimmed if trimmed and _SHA_PATTERN.match(trimmed) else None


def _git(cwd: str, *args: str, env: dict[str, str] | None = None) -> str | None:
    out = run_git(cwd, list(args), timeout=GIT_TIMEOUT_SECONDS, env=env)
    return out.strip() if out is not None else None


def is_empty_git_state(state: GitState) -> bool:
    return all(value is None for value in state.values())


def resolve_working_tree_sha(root: str) -> str | None:
    directory = None
    try:
        directory = tempfile.mkdtemp(prefix="bitfab-git-")
        env = {"GIT_INDEX_FILE": os.path.join(directory, "index")}
        if _git(root, "read-tree", "HEAD", env=env) is None:
            return None
        if _git(root, "add", "-A", "--", root, env=env) is None:
            return None
        return _sha(_git(root, "write-tree", env=env))
    except Exception:
        return None
    finally:
        if directory:
            shutil.rmtree(directory, ignore_errors=True)


def resolve_git_state(cwd: str) -> GitState | None:
    refs = _git(cwd, "rev-parse", "--show-toplevel", "HEAD", "HEAD^{tree}")
    lines = refs.split("\n") if refs else []
    root = lines[0].strip() if lines else None
    if not root:
        return None

    state: GitState = {
        "githubEmail": _text(_git(cwd, "config", "user.email")),
        "branch": _text(_git(cwd, "symbolic-ref", "--short", "-q", "HEAD")),
        "commitSha": _sha(lines[1] if len(lines) > 1 else None),
        "baseSha": _sha(lines[2] if len(lines) > 2 else None),
        "experimentSha": resolve_working_tree_sha(root),
    }
    return None if is_empty_git_state(state) else state


def resolved_git_state() -> GitState | None:
    if os.environ.get(DISABLE_ENV):
        return None
    try:
        return resolve_git_state(os.getcwd())
    except Exception:
        return None
