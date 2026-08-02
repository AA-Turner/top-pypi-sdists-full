"""Fetch GitLab CI ``include:`` files from remote projects, with a ref-keyed cache.

The cache resolves each ``ref`` (branch / tag / sha) to a commit SHA via the
GitLab API, then stores the file content addressed by ``(project, sha, file)``.
Because content is keyed by SHA, cached files never go stale — a new commit on
the source branch generates a new SHA and a fresh fetch.

Ref → SHA resolution is cached separately with a short TTL so we don't pay an
extra round-trip on every invocation.
"""

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote

from ...config import CACHE_DIR
from .gitlab_api import _run_glab

CACHE_ROOT = CACHE_DIR / "ci_includes"
SHA_CACHE_FILE = CACHE_ROOT / "ref_shas.json"
SHA_TTL_SECONDS = 600  # 10 minutes


def _encode(value: str) -> str:
    """Reduce an arbitrary string to a safe filename component."""
    return re.sub(r"[^A-Za-z0-9_.-]", "_", value)


def _load_sha_cache() -> dict[str, dict[str, Any]]:
    if not SHA_CACHE_FILE.exists():
        return {}
    try:
        raw = SHA_CACHE_FILE.read_text(encoding="utf-8")
    except OSError:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _save_sha_cache(data: dict[str, dict[str, Any]]) -> None:
    try:
        CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    except OSError:
        return
    tmp = SHA_CACHE_FILE.with_suffix(".json.tmp")
    try:
        tmp.write_text(json.dumps(data), encoding="utf-8")
        os.replace(tmp, SHA_CACHE_FILE)
    except OSError:
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass


def resolve_ref_to_sha(project_path: str, ref: str) -> str | None:
    """Resolve a git ref to a commit SHA via ``glab``, with a short-TTL cache.

    Returns ``None`` if the ref cannot be resolved (network failure, missing
    project, unauthorized, etc.).
    """
    cache_key = f"{project_path}|{ref}"
    cache = _load_sha_cache()
    entry = cache.get(cache_key)
    now = time.time()
    if isinstance(entry, dict):
        ts = entry.get("ts")
        sha = entry.get("sha")
        if isinstance(sha, str) and sha and isinstance(ts, (int, float)) and now - ts < SHA_TTL_SECONDS:
            return sha

    encoded_proj = quote(project_path, safe="")
    encoded_ref = quote(ref, safe="")
    raw = _run_glab("api", f"projects/{encoded_proj}/repository/commits/{encoded_ref}")
    if not raw:
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    sha = data.get("id") if isinstance(data, dict) else None
    if not isinstance(sha, str) or not sha:
        return None

    cache[cache_key] = {"sha": sha, "ts": now}
    _save_sha_cache(cache)
    return sha


def fetch_file(project_path: str, file_path: str, ref: str) -> str | None:
    """Fetch a file from a remote GitLab project at ``ref``, caching by SHA.

    The ref is resolved to a commit SHA first; the file is then stored under
    a SHA-addressed cache filename, so a new commit on the source branch
    invalidates the entry naturally.
    """
    sha = resolve_ref_to_sha(project_path, ref)
    if not sha:
        print(f"Could not resolve ref {project_path}@{ref}", file=sys.stderr)
        return None

    cache_file = CACHE_ROOT / f"{_encode(project_path)}__{sha}__{_encode(file_path)}"
    if cache_file.exists():
        try:
            return cache_file.read_text(encoding="utf-8")
        except OSError:
            pass

    encoded_proj = quote(project_path, safe="")
    encoded_file = quote(file_path, safe="")
    content = _run_glab("api", f"projects/{encoded_proj}/repository/files/{encoded_file}/raw?ref={sha}")
    if content is None:
        return None

    try:
        CACHE_ROOT.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(content, encoding="utf-8")
    except OSError:
        pass
    return content


def gather_yaml_documents(local_content: str, repo_root: Path | None = None) -> list[str]:
    """Return all YAML contents pulled in by the local ``.gitlab-ci.yml``.

    Recursively follows ``include:`` for ``project + file`` (remote, cached) and
    ``local:`` (filesystem) entries. ``remote:`` and ``template:`` entries are
    skipped (rare in Pysae). Each project/file/ref triple is fetched at most
    once per call.

    Documents are returned **highest-precedence last**: each file's includes
    come before the file itself, and the local ``.gitlab-ci.yml`` comes last of
    all. This matches GitLab's ``include:`` semantics (the including file
    overrides the files it includes), so callers can merge the list in order
    with a "later overrides earlier" strategy without any reordering.
    """
    from .yaml_parser import parse_includes  # local import to keep the dep graph clean

    documents: list[str] = []
    seen: set[tuple[str, str, str]] = set()
    seen_local: set[Path] = set()
    root = repo_root or Path.cwd()

    def _process(content: str) -> None:
        if not content:
            return
        for include in parse_includes(content):
            project = include.get("project")
            file_value = include.get("file")
            ref = include.get("ref") or "HEAD"
            local = include.get("local")

            if isinstance(project, str) and file_value is not None:
                files = file_value if isinstance(file_value, list) else [file_value]
                for file_entry in files:
                    if not isinstance(file_entry, str):
                        continue
                    key = (project, file_entry, ref)
                    if key in seen:
                        continue
                    seen.add(key)
                    fetched = fetch_file(project, file_entry, ref)
                    if fetched:
                        _process(fetched)
            elif isinstance(local, str):
                local_path = (root / local.lstrip("/")).resolve()
                if local_path in seen_local:
                    continue
                seen_local.add(local_path)
                if local_path.exists():
                    try:
                        _process(local_path.read_text(encoding="utf-8"))
                    except OSError:
                        pass
        documents.append(content)

    _process(local_content)
    return documents
