from __future__ import annotations

import os
import threading
from collections.abc import Callable, Mapping
from typing import TypedDict
from urllib.parse import urlsplit

from bitfab.git_command import run_git


class CommitRef(TypedDict):
    sha: str
    branch: str | None
    dirty: bool | None
    remote: str | None
    root_sha: str | None


EXPLICIT_SHA_ENV = "BITFAB_COMMIT_SHA"
DISABLE_ENV = "BITFAB_DISABLE_COMMIT_REF"
GIT_TIMEOUT_SECONDS = 2.0

RemoteReader = Callable[[Mapping[str, str]], "str | None"]

_VERCEL_PROVIDER_HOSTS = {
    "github": "github.com",
    "gitlab": "gitlab.com",
    "bitbucket": "bitbucket.org",
}


def _read(env: Mapping[str, str], name: str | None) -> str | None:
    if name is None:
        return None
    value = env.get(name, "").strip()
    return value or None


def _remote_from(*names: str) -> RemoteReader:
    def read(env: Mapping[str, str]) -> str | None:
        parts = [_read(env, name) for name in names]
        if not all(parts):
            return None
        return normalize_remote("/".join(part for part in parts if part))

    return read


def _vercel_remote(env: Mapping[str, str]) -> str | None:
    provider = (_read(env, "VERCEL_GIT_PROVIDER") or "").lower()
    host = _VERCEL_PROVIDER_HOSTS.get(provider)
    owner = _read(env, "VERCEL_GIT_REPO_OWNER")
    slug = _read(env, "VERCEL_GIT_REPO_SLUG")
    if not (host and owner and slug):
        return None
    return f"{host}/{owner}/{slug}"


def _no_remote(env: Mapping[str, str]) -> str | None:
    return None


PLATFORM_ENVS: tuple[tuple[str, str | None, RemoteReader], ...] = (
    ("VERCEL_GIT_COMMIT_SHA", "VERCEL_GIT_COMMIT_REF", _vercel_remote),
    (
        "GITHUB_SHA",
        "GITHUB_REF_NAME",
        _remote_from("GITHUB_SERVER_URL", "GITHUB_REPOSITORY"),
    ),
    ("RAILWAY_GIT_COMMIT_SHA", "RAILWAY_GIT_BRANCH", _no_remote),
    ("RENDER_GIT_COMMIT", "RENDER_GIT_BRANCH", _no_remote),
    ("SOURCE_VERSION", None, _no_remote),
    ("CF_PAGES_COMMIT_SHA", "CF_PAGES_BRANCH", _no_remote),
    ("CI_COMMIT_SHA", "CI_COMMIT_REF_NAME", _remote_from("CI_REPOSITORY_URL")),
    (
        "BUILD_SOURCEVERSION",
        "BUILD_SOURCEBRANCHNAME",
        _remote_from("BUILD_REPOSITORY_URI"),
    ),
    ("CIRCLE_SHA1", "CIRCLE_BRANCH", _remote_from("CIRCLE_REPOSITORY_URL")),
)


def normalize_remote(raw: str | None) -> str | None:
    if raw is None:
        return None
    value = raw.strip()
    if not value:
        return None
    if "://" in value:
        parts = urlsplit(value)
        host = parts.hostname or ""
        path = parts.path
    else:
        head, separator, tail = value.partition(":")
        host = head.rpartition("@")[2] if separator else ""
        path = tail if separator else value
    path = path.strip("/")
    if path.endswith(".git"):
        path = path[: -len(".git")].rstrip("/")
    if not host:
        return path or None
    return f"{host}/{path}" if path else host


def resolve_from_env(env: Mapping[str, str]) -> CommitRef | None:
    explicit = _read(env, EXPLICIT_SHA_ENV)
    platform = next((entry for entry in PLATFORM_ENVS if _read(env, entry[0])), None)
    if platform is None:
        if explicit is None:
            return None
        return {
            "sha": explicit,
            "branch": None,
            "dirty": None,
            "remote": None,
            "root_sha": None,
        }
    sha_env, branch_env, read_remote = platform
    return {
        "sha": explicit or env[sha_env].strip(),
        "branch": _read(env, branch_env),
        "dirty": None,
        "remote": read_remote(env),
        "root_sha": None,
    }


def _git(cwd: str, *args: str) -> str | None:
    out = run_git(cwd, list(args), timeout=GIT_TIMEOUT_SECONDS)
    return out.strip() if out is not None else None


def resolve_from_git(cwd: str) -> CommitRef | None:
    sha = _git(cwd, "rev-parse", "HEAD")
    if not sha:
        return None
    status = _git(cwd, "status", "--porcelain")
    roots = _git(cwd, "rev-list", "--max-parents=0", "HEAD")
    return {
        "sha": sha,
        "branch": _git(cwd, "symbolic-ref", "--short", "-q", "HEAD") or None,
        "dirty": None if status is None else bool(status),
        "remote": normalize_remote(_git(cwd, "remote", "get-url", "origin")),
        "root_sha": min(roots.split()) if roots else None,
    }


_lock = threading.Lock()
_resolved = False
_ref: CommitRef | None = None
_git_thread: threading.Thread | None = None


def _resolve_git_in_background(cwd: str) -> None:
    global _ref, _resolved
    ref = resolve_from_git(cwd)
    with _lock:
        if not _resolved:
            _ref = ref
            _resolved = True


def start_commit_ref_resolution() -> None:
    global _ref, _resolved, _git_thread
    with _lock:
        if _resolved or _git_thread is not None:
            return
        if _read(os.environ, DISABLE_ENV) is not None:
            _resolved = True
            return
        from_env = resolve_from_env(os.environ)
        if from_env is not None:
            _ref = from_env
            _resolved = True
            return
        try:
            cwd = os.getcwd()
        except OSError:
            _resolved = True
            return
        _git_thread = threading.Thread(
            target=_resolve_git_in_background,
            args=(cwd,),
            name="bitfab-commit-ref",
            daemon=True,
        )
        _git_thread.start()


def current_commit_ref() -> CommitRef | None:
    start_commit_ref_resolution()
    with _lock:
        return _ref


def _reset() -> None:
    global _ref, _resolved, _git_thread
    with _lock:
        _ref = None
        _resolved = False
        _git_thread = None
