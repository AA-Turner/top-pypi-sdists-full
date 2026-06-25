"""Chronos workspace upload commands."""

from __future__ import annotations

import asyncio
import json
import os
import secrets
import shutil
import subprocess
import sys
import tarfile
import tempfile
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Any, BinaryIO

import httpx
import typer
import yaml

from plato.chronos.api.sessions import get_session_workspace_download_url, get_session_workspace_upload_url
from plato.chronos.api.workspace_repos import (
    create_workspace_ref,
    get_workspace_repo_credentials,
    list_workspace_refs,
    resolve_workspace_repo,
)
from plato.chronos.models import CreateWorkspaceRefRequest, WorkspaceRefResponse, WorkspaceRepoResolveRequest
from plato.cli.chronos.settings import get_settings
from plato.cli.utils import console
from plato.git_ops.repo import trust_git_directory
from plato.markers import WorkspaceMarker
from plato.worlds.dvc_models import (
    S3Config,
    _archive_s3_key,
    _build_ignore_matchers,
    parse_dvc_format,
    s3_download_bytes_sync,
    smart_commit_archive,
)

workspace_app = typer.Typer(help="Workspace utilities.")
workspace_upload_app = typer.Typer(help="Upload workspace snapshots.")
workspace_app.add_typer(workspace_upload_app, name="upload")

_CHUNK_SIZE = 256 * 1024
_PLATO_GIT_ENV = {
    "GIT_AUTHOR_NAME": "Plato",
    "GIT_AUTHOR_EMAIL": "plato@plato.dev",
    "GIT_COMMITTER_NAME": "Plato",
    "GIT_COMMITTER_EMAIL": "plato@plato.dev",
}

# Round-trip marker dropped into the extracted payload dir by ``download
# --extract`` and read back by ``upload git`` so the dvc ``dir_name`` (the
# restore target the world expects, e.g. ``data``) and the workspace repo
# survive an edit cycle without the user having to remember them.
_WORKSPACE_MARKER = ".plato-workspace.json"
# Default dvc archive dir name used by the world runtime's ``_archive_commit``
# when a workspace has no FUSE mounts (see plato/worlds/workspace.py).
_DEFAULT_DIR_NAME = "data"
# Prefix marking a checkpoint produced by a manual (human) ``upload git`` rather
# than the agent pipeline. ``register_git_workspace_ref`` keeps the bare
# ``_DEFAULT_STEP_NAME`` for direct API callers; ``_resolve_upload_target``
# generates a unique ``manual-upload-<rand>`` name so a hand upload never
# silently overwrites the pipeline checkpoint recorded in the round-trip marker.
_MANUAL_STEP_PREFIX = "manual-upload"
_DEFAULT_STEP_NAME = "manual-git-upload"


def _generate_manual_step_name() -> str:
    """A unique, clearly-labeled checkpoint name for a manual git upload.

    Defaulting to this (instead of the marker's original step) keeps a hand
    upload from clobbering the agent-produced checkpoint it was downloaded from.
    Pass ``--step`` to register under a specific name (e.g. to resume one).
    """
    return f"{_MANUAL_STEP_PREFIX}-{secrets.token_hex(4)}"


@dataclass(frozen=True, slots=True)
class GitWorkspaceArchive:
    path: Path
    head_sha: str
    size_bytes: int


class _FileStream:
    """Reusable file stream for httpx request bodies."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def __iter__(self) -> Iterator[bytes]:
        with self.path.open("rb") as handle:
            yield from _read_chunks(handle)


def _read_chunks(handle: BinaryIO) -> Iterator[bytes]:
    while True:
        chunk = handle.read(_CHUNK_SIZE)
        if not chunk:
            break
        yield chunk


def _run_git(args: list[str], *, cwd: Path | None = None) -> str:
    env = {**os.environ, **_PLATO_GIT_ENV}
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        command = " ".join(["git", *args])
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"{command} failed: {detail}")
    return result.stdout.strip()


def _is_git_workspace_root(path: Path) -> bool:
    return (path / "repo" / ".git").is_dir() and (path / ".git-bare" / "HEAD").exists()


def _require_git_workspace_root(path: Path) -> tuple[Path, Path]:
    """Resolve ``path`` to the (repo_dir, bare_dir) of a git workspace payload.

    The payload dir is always ``bare_dir.parent`` — i.e. the directory whose
    children (``repo/``, ``.git-bare/``, and any sidecars) become the archive's
    top level and which the world restores into ``<repo_root>/<dir_name>``.
    """
    root = path.expanduser().resolve()
    if _is_git_workspace_root(root):
        return root / "repo", root / ".git-bare"
    if (root / ".git").is_dir() and root.name == "repo" and (root.parent / ".git-bare" / "HEAD").exists():
        return root, root.parent / ".git-bare"
    raise ValueError(
        "Expected a git workspace root containing repo/ and .git-bare/, or the repo/ directory inside that workspace."
    )


def _find_nested_payload(repo_dir: Path) -> Path | None:
    """Return a child of ``repo_dir`` that is itself a git workspace payload.

    Used to catch the "wrong nesting level" footgun: if the working tree we are
    about to archive *contains* another ``repo/`` + ``.git-bare/`` pair, the
    caller almost certainly pointed at an outer transport layer and meant the
    inner directory.
    """
    if not repo_dir.is_dir():
        return None
    for child in sorted(repo_dir.iterdir()):
        if child.is_dir() and _is_git_workspace_root(child):
            return child
    return None


def _guard_no_nested_workspace_commit(repo_dir: Path) -> None:
    """Refuse to ``git add -A`` a working tree carrying a nested workspace.

    A directory inside the working tree that holds its own ``.git-bare/`` is a
    nested workspace copy (e.g. a downloaded checkpoint dropped back inside the
    repo). Committing it recursively self-includes the whole workspace — every
    re-upload then re-commits it, ballooning history into tens of thousands of
    loose objects and making restore crawl. Catch it before the commit unless
    git is already ignoring it.
    """
    for child in sorted(repo_dir.iterdir()):
        if not child.is_dir() or not (child / ".git-bare").is_dir():
            continue
        ignored = subprocess.run(
            ["git", "-C", str(repo_dir), "check-ignore", "-q", child.name],
            env={**os.environ, **_PLATO_GIT_ENV},
            capture_output=True,
            check=False,
        )
        if ignored.returncode != 0:  # 0 == ignored; non-zero == would be committed
            raise RuntimeError(
                f"Working tree '{repo_dir}' contains a nested workspace at '{child.name}/' "
                f"(it has its own .git-bare/). 'git add -A' would recursively commit it and "
                f"bloat the archive. Remove it or add '{child.name}/' to .gitignore before uploading."
            )


def _prune_bare_garbage(bare_dir: Path) -> None:
    """Drop unreferenced loose objects from the bare without packing it.

    Webclone keeps git-backed bares in loose-object form on purpose
    (``gc_bare_repo`` / ``repair_bare_repo`` explode packs back to loose because
    packed objects are a corruption failure mode for these workspaces), so we
    must NOT ``gc``/repack here — that would just be undone on the next reset.
    Pruning dangling objects is safe and keeps the archive from shipping garbage.
    A high surviving object count means the *history* is bloated (see
    ``_guard_no_nested_workspace_commit``), which pruning alone cannot fix.
    """
    for args in (
        ["--git-dir", str(bare_dir), "reflog", "expire", "--expire=now", "--all"],
        ["--git-dir", str(bare_dir), "prune", "--expire=now"],
    ):
        subprocess.run(
            ["git", *args],
            env={**os.environ, **_PLATO_GIT_ENV},
            capture_output=True,
            check=False,
        )
    count = subprocess.run(
        ["git", "--git-dir", str(bare_dir), "count-objects"],
        env={**os.environ, **_PLATO_GIT_ENV},
        capture_output=True,
        text=True,
        check=False,
    )
    loose = 0
    if count.returncode == 0 and count.stdout.split():
        try:
            loose = int(count.stdout.split()[0])
        except ValueError:
            loose = 0
    if loose > 20000:
        console.print(
            f"[yellow]Warning: bare has {loose} loose objects — the source history is bloated "
            "(likely a nested workspace committed into it). Restore will be slow; consider "
            "rebuilding the bare from a clean tree.[/yellow]"
        )


@dataclass(frozen=True, slots=True)
class _UploadTarget:
    payload_dir: Path  # archived; its children become the tar top level
    repo_dir: Path  # payload_dir/repo (inner working tree to sync)
    bare_dir: Path  # payload_dir/.git-bare (inner bare)
    dir_name: str  # dvc_files key / world restore target name
    repo_name: str  # Chronos workspace repo for ref registration
    step_name: str  # workspace ref step name (resume restore matches it exactly)


def _read_marker(payload_dir: Path) -> dict | None:
    marker_path = payload_dir / _WORKSPACE_MARKER
    if not marker_path.is_file():
        return None
    try:
        data = json.loads(marker_path.read_text())
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def _write_marker(payload_dir: Path, *, dir_name: str, repo_name: str, session_id: str, step_name: str | None) -> None:
    marker = {"dir_name": dir_name, "repo_name": repo_name, "session_id": session_id, "step_name": step_name}
    (payload_dir / _WORKSPACE_MARKER).write_text(json.dumps(marker, indent=2) + "\n")


def _resolve_upload_target(
    source: Path,
    *,
    dir_name: str | None,
    repo_name: str | None,
    step_name: str | None = None,
) -> _UploadTarget:
    """Resolve the upload source into an unambiguous archive target.

    Precedence for ``dir_name``/``repo_name``: explicit CLI flag > round-trip
    marker written by ``download --extract`` > inferred default. The marker pins
    *where* the upload lands (same repo + restore dir) so a download → edit →
    upload cycle round-trips cleanly.

    ``step_name`` is deliberately NOT taken from the marker: an explicit
    ``--step`` wins, otherwise a fresh ``manual-upload-<rand>`` checkpoint is
    generated so a hand upload registers a new, clearly-labeled ref instead of
    silently overwriting the agent-produced step it was downloaded from.

    When neither a flag nor a marker pins the layout, a nested payload under the
    working tree is treated as the caller pointing one level too high and is
    rejected with a pointer to the correct directory.
    """
    repo_dir, bare_dir = _require_git_workspace_root(source)
    payload_dir = bare_dir.parent
    marker = _read_marker(payload_dir)

    pinned = dir_name is not None or marker is not None
    if not pinned:
        nested = _find_nested_payload(repo_dir)
        if nested is not None:
            raise ValueError(
                f"'{source}' looks like an outer transport layer: its working tree contains a nested "
                f"git workspace at '{nested}'. Point at that directory instead, or pass --dir-name to override."
            )

    resolved_dir_name = dir_name or (marker or {}).get("dir_name") or _DEFAULT_DIR_NAME
    resolved_repo_name = repo_name or (marker or {}).get("repo_name") or "code"
    resolved_step_name = step_name or _generate_manual_step_name()
    return _UploadTarget(
        payload_dir=payload_dir,
        repo_dir=repo_dir,
        bare_dir=bare_dir,
        dir_name=resolved_dir_name,
        repo_name=resolved_repo_name,
        step_name=resolved_step_name,
    )


def _read_dvcignore(payload_dir: Path) -> list[str]:
    """Merge the world's ignore rules: defaults + any ``.dvcignore`` in scope.

    The world runtime reads ``.dvcignore`` from the workspace repo root, which
    is the parent of the dvc ``dir_name`` directory; we also honor one inside
    the payload itself. Patterns are de-duplicated, defaults first.
    """
    patterns: list[str] = list(WorkspaceMarker.DEFAULT_DVCIGNORE)
    seen = set(patterns)
    for candidate in (payload_dir.parent / ".dvcignore", payload_dir / ".dvcignore"):
        if not candidate.is_file():
            continue
        for line in candidate.read_text().splitlines():
            entry = line.strip()
            if entry and not entry.startswith("#") and entry not in seen:
                patterns.append(entry)
                seen.add(entry)
    return patterns


def _build_s3_config(
    repo_name: str,
    *,
    chronos_url: str,
    api_key: str,
    timeout: float = 60.0,
) -> S3Config:
    """Resolve a workspace repo and build its S3Config in one place.

    Mirrors ``Workspace._s3_config`` (including ``credential_refresh`` so a
    long transfer can re-fetch STS creds) instead of hand-assembling the config
    at each call site.
    """
    with httpx.Client(base_url=chronos_url.rstrip("/"), timeout=timeout, headers={"X-API-Key": api_key}) as client:
        resolved = resolve_workspace_repo.sync(
            client, body=WorkspaceRepoResolveRequest(name=repo_name), x_api_key=api_key
        )
        creds = get_workspace_repo_credentials.sync(client, repo_public_id=resolved.repo_id, x_api_key=api_key)
    return S3Config(
        bucket=creds.bucket,
        prefix=creds.prefix,
        credentials={
            "AWS_ACCESS_KEY_ID": creds.aws_access_key_id,
            "AWS_SECRET_ACCESS_KEY": creds.aws_secret_access_key,
            "AWS_SESSION_TOKEN": creds.aws_session_token,
            "AWS_DEFAULT_REGION": creds.region,
        },
        credential_refresh={
            "chronos_url": chronos_url.rstrip("/"),
            "repo_id": resolved.repo_id,
            "api_key": api_key,
            "refresh_margin_seconds": 300,
        },
    )


def _tar_payload_children(payload_dir: Path, dest: Path, ignore_patterns: list[str] | None) -> None:
    """Tar.gz the children of ``payload_dir`` exactly as ``smart_commit_archive`` does.

    Keeps the dry-run / local-archive output byte-compatible with what the real
    upload pushes to S3 (same membership, same ``.dvcignore`` filtering).
    """
    ignored_name, ignored_path = _build_ignore_matchers(ignore_patterns)

    def _filter(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo | None:
        for part in Path(tarinfo.name).parts:
            if ignored_name(part):
                return None
        if ignored_path(tarinfo.name) or ignored_path(f"{tarinfo.name}/"):
            return None
        return tarinfo

    with tarfile.open(dest, "w:gz") as tar:
        for entry in sorted(os.scandir(payload_dir), key=lambda e: e.name):
            tar.add(entry.path, arcname=entry.name, filter=_filter)


def _reclone_repo_from_bare(payload_dir: Path) -> Path:
    """Re-clone ``repo/`` from ``.git-bare`` with a portable relative origin.

    Shared by the extract and download paths: the ``repo/.git`` captured in an
    archive may be incomplete (objects can live only in the bare), so we always
    drop the captured working tree and clone fresh. Mirrors
    ``GitTransport._init_bare_repo`` / ``_set_origin_to_bare``.
    """
    bare_dir = payload_dir / ".git-bare"
    repo_dir = payload_dir / "repo"
    if not bare_dir.exists():
        raise ValueError(f"Archive does not contain .git-bare/: {payload_dir}")
    if repo_dir.exists():
        shutil.rmtree(repo_dir)
    trust_git_directory(bare_dir)
    _run_git(["clone", str(bare_dir), str(repo_dir)])
    _run_git(["remote", "set-url", "origin", "../.git-bare"], cwd=repo_dir)
    return repo_dir


def _ensure_bare_push_settings(bare_dir: Path) -> None:
    _run_git(["--git-dir", str(bare_dir), "config", "receive.unpackLimit", "100000"])
    _run_git(["--git-dir", str(bare_dir), "config", "transfer.unpackLimit", "100000"])


def _set_origin_to_bare(repo_dir: Path, bare_dir: Path) -> None:
    relative_bare = os.path.relpath(bare_dir, start=repo_dir)
    remotes = _run_git(["remote"], cwd=repo_dir).splitlines()
    if "origin" in remotes:
        _run_git(["remote", "set-url", "origin", relative_bare], cwd=repo_dir)
    else:
        _run_git(["remote", "add", "origin", relative_bare], cwd=repo_dir)


def _sync_repo_to_bare(repo_dir: Path, bare_dir: Path, *, commit_message: str) -> str:
    trust_git_directory(repo_dir)
    trust_git_directory(bare_dir)
    _ensure_bare_push_settings(bare_dir)
    _run_git(["config", "user.email", _PLATO_GIT_ENV["GIT_AUTHOR_EMAIL"]], cwd=repo_dir)
    _run_git(["config", "user.name", _PLATO_GIT_ENV["GIT_AUTHOR_NAME"]], cwd=repo_dir)
    _set_origin_to_bare(repo_dir, bare_dir)
    _guard_no_nested_workspace_commit(repo_dir)
    _run_git(["add", "-A"], cwd=repo_dir)
    status = _run_git(["status", "--porcelain"], cwd=repo_dir)
    if status:
        _run_git(["commit", "-m", commit_message], cwd=repo_dir)
    # Push without --force so the previous commit (baseline) is preserved
    # as the parent.  This lets reviewers diff HEAD~1..HEAD to see what
    # the contractor changed.  If the push is rejected (non-fast-forward
    # because the bare was updated by another process), fall back to a
    # force push so the upload still succeeds.
    result = subprocess.run(
        ["git", "push", str(bare_dir), "HEAD:refs/heads/main"],
        cwd=str(repo_dir),
        env={**os.environ, **_PLATO_GIT_ENV},
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        _run_git(["push", "--force", str(bare_dir), "HEAD:refs/heads/main"], cwd=repo_dir)
    _run_git(["--git-dir", str(bare_dir), "symbolic-ref", "HEAD", "refs/heads/main"])
    _prune_bare_garbage(bare_dir)
    return _run_git(["--git-dir", str(bare_dir), "rev-parse", "main"])


def _sync_git_workspace(source: Path, *, commit_message: str) -> tuple[Path, Path, str]:
    """Push repo/ to .git-bare and return (repo_dir, bare_dir, head_sha)."""
    repo_dir, bare_dir = _require_git_workspace_root(source)
    head_sha = _sync_repo_to_bare(repo_dir, bare_dir, commit_message=commit_message)
    return repo_dir, bare_dir, head_sha


def create_git_workspace_archive(
    source: Path,
    *,
    commit_message: str = "Upload Chronos git workspace",
    output: Path | None = None,
    ignore_patterns: list[str] | None = None,
) -> GitWorkspaceArchive:
    """Push repo/ to .git-bare and tar.gz the payload dir.

    Produces the same tar membership and ``.dvcignore`` filtering as the real
    S3 upload (``smart_commit_archive``), so ``--dry-run`` / ``--output-archive``
    reflect exactly what would be uploaded and what ``--extract`` restores.
    """
    repo_dir, bare_dir, head_sha = _sync_git_workspace(source, commit_message=commit_message)
    payload_dir = bare_dir.parent
    if ignore_patterns is None:
        ignore_patterns = _read_dvcignore(payload_dir)

    if output is None:
        tmp = tempfile.NamedTemporaryFile(prefix="plato-git-workspace-", suffix=".tar.gz", delete=False)
        archive_path = Path(tmp.name)
        tmp.close()
    else:
        archive_path = output.expanduser().resolve()
        archive_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        _tar_payload_children(payload_dir, archive_path, ignore_patterns)
    except Exception:
        if output is None:
            archive_path.unlink(missing_ok=True)
        raise

    return GitWorkspaceArchive(path=archive_path, head_sha=head_sha, size_bytes=archive_path.stat().st_size)


def upload_git_workspace_archive(
    archive: Path,
    *,
    session_id: str,
    name: str,
    chronos_url: str,
    api_key: str,
    timeout: float = 60.0,
) -> None:
    with httpx.Client(base_url=chronos_url.rstrip("/"), timeout=timeout, headers={"X-API-Key": api_key}) as client:
        payload = get_session_workspace_upload_url.sync(client, public_id=session_id, name=name)
        upload_url = payload["url"]
    headers = {
        "Content-Type": "application/x-tar",
        "Content-Length": str(archive.stat().st_size),
    }
    with httpx.Client(timeout=max(timeout, 300.0)) as client:
        response = client.put(upload_url, content=_FileStream(archive), headers=headers)
        response.raise_for_status()


def upload_git_workspace_via_archive(
    payload_dir: Path,
    *,
    repo_name: str,
    dir_name: str = _DEFAULT_DIR_NAME,
    chronos_url: str,
    api_key: str,
    ignore_patterns: list[str] | None = None,
    timeout: float = 60.0,
) -> tuple[str, str]:
    """Upload the payload dir as a DVC archive (tar.gz) to S3 via s5cmd.

    Uses ``smart_commit_archive`` so the archive is stored at a
    content-addressed S3 key and the returned ``dvc_yaml`` carries
    ``format: archive`` — making it restorable by webclone's
    ``Workspace.restore()`` path under ``dir_name``.
    """
    s3_config = _build_s3_config(repo_name, chronos_url=chronos_url, api_key=api_key, timeout=timeout)
    return asyncio.run(
        smart_commit_archive(
            payload_dir,
            s3_config,
            dir_name=dir_name,
            ignore_patterns=ignore_patterns,
        )
    )


def download_session_workspace_archive(
    destination: Path,
    *,
    session_id: str,
    name: str,
    chronos_url: str,
    api_key: str,
    timeout: float = 60.0,
) -> int:
    with httpx.Client(base_url=chronos_url.rstrip("/"), timeout=timeout, headers={"X-API-Key": api_key}) as client:
        payload = get_session_workspace_download_url.sync(client, public_id=session_id, name=name)
        download_url = payload["url"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with httpx.Client(timeout=max(timeout, 300.0)) as client:
        with client.stream("GET", download_url) as response:
            response.raise_for_status()
            with destination.open("wb") as handle:
                for chunk in response.iter_bytes(_CHUNK_SIZE):
                    handle.write(chunk)
                    total += len(chunk)
    return total


def extract_git_workspace_archive(
    archive: Path,
    destination: Path,
) -> Path:
    """Extract a git workspace tar and re-clone repo/ from the bare.

    The archive contains ``.git-bare/`` and ``repo/``.  The ``repo/.git``
    captured in the tar may be incomplete (missing ``objects/``) because
    the uploader's working tree often shares objects with the bare.  To
    guarantee a fully-functional local clone we remove the captured
    ``repo/`` and re-clone from ``.git-bare``, then set a relative origin
    so the workspace is portable.

    Returns the path to the restored ``repo/`` directory.
    """
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r") as tar:
        if sys.version_info >= (3, 12):
            tar.extractall(destination, filter="data")
        else:
            tar.extractall(destination)

    return _reclone_repo_from_bare(destination)


def _latest_ref(refs: list[WorkspaceRefResponse]) -> WorkspaceRefResponse:
    """Pick the newest ref by ``created_at`` rather than trusting list order.

    The list endpoint does not guarantee chronological ordering, so ``refs[-1]``
    could return an older checkpoint. Refs missing ``created_at`` sort last so a
    timestamped ref always wins; ties fall back to original order.
    """
    return max(
        enumerate(refs),
        key=lambda ir: (ir[1].created_at is not None, ir[1].created_at, ir[0]),
    )[1]


def ref_has_archive_dvc(ref: dict[str, Any]) -> bool:
    """True if a workspace ref dict carries any ``format: archive`` dvc entry.

    Used by ``plato chronos download`` to auto-route git/archive workspaces
    through the extract + clone-from-``.git-bare`` path (instead of the legacy
    server-side ZIP), so callers don't have to remember ``--extract``.
    """
    dvc_files = ref.get("dvc_files") or {}
    return any(parse_dvc_format(v) == "archive" for v in dvc_files.values())


def _select_archive_dvc(dvc_files: dict[str, str], *, dir_name: str | None, ref_id: str | None) -> tuple[str, str]:
    """Pick the ``format: archive`` dvc entry to restore from a ref's dvc_files.

    A ref can carry multiple dvc_files (e.g. a manifest-mounted dir plus an
    archive dir). ``--extract`` only handles archive blobs, so select that entry
    explicitly — preferring ``dir_name`` when given — instead of an arbitrary
    dict key.
    """
    archive_entries = {k: v for k, v in dvc_files.items() if parse_dvc_format(v) == "archive"}
    if not archive_entries:
        raise ValueError(
            f"Workspace ref {ref_id} has no 'format: archive' dvc_files (found keys {list(dvc_files)}). "
            "--extract only supports archive refs; use --session-workspace for legacy presigned-URL downloads."
        )
    if dir_name and dir_name in archive_entries:
        return dir_name, archive_entries[dir_name]
    return next(iter(archive_entries.items()))


def download_git_workspace_via_archive(
    destination: Path,
    *,
    session_id: str,
    repo_name: str,
    step_name: str | None = None,
    dir_name: str | None = None,
    chronos_url: str,
    api_key: str,
    timeout: float = 60.0,
) -> Path:
    """Download a git workspace from DVC archive and extract.

    Fetches the workspace ref, reads ``dvc_files`` to find the archive
    md5, downloads the tar.gz from S3 via s5cmd, extracts it, and
    re-clones ``repo/`` from ``.git-bare``.

    Returns the path to the restored ``repo/`` directory.
    """
    with httpx.Client(base_url=chronos_url.rstrip("/"), timeout=timeout, headers={"X-API-Key": api_key}) as client:
        refs_response = list_workspace_refs.sync(client, session_public_id=session_id, x_api_key=api_key)
        refs = [r for r in refs_response.refs if r.repo_name == repo_name]
        if not refs:
            raise ValueError(f"No workspace refs found for repo '{repo_name}' in session {session_id}")
        if step_name:
            refs = [r for r in refs if r.step_name == step_name]
            if not refs:
                raise ValueError(
                    f"No workspace refs found for step '{step_name}' in repo '{repo_name}' for session {session_id}"
                )
        ref = _latest_ref(refs)
        dvc_files = ref.dvc_files or {}
        if not dvc_files:
            raise ValueError(
                f"Workspace ref {ref.ref_public_id} has no dvc_files — "
                "use --session-workspace for legacy presigned-URL downloads"
            )
        dir_name, dvc_content = _select_archive_dvc(dvc_files, dir_name=dir_name, ref_id=ref.ref_public_id)

        dvc_data = yaml.safe_load(dvc_content)
        outs = dvc_data.get("outs", [])
        if not outs:
            raise ValueError("dvc_yaml has no outs entry")
        archive_md5 = outs[0].get("md5", "")
        if not archive_md5:
            raise ValueError("dvc_yaml out has no md5")
        ref_step_name = ref.step_name

    # Validate the destination BEFORE the (potentially large) S3 download.
    dest_resolved = destination.resolve()
    cwd_resolved = Path.cwd().resolve()
    if dest_resolved == cwd_resolved or dest_resolved in cwd_resolved.parents:
        raise ValueError(
            f"Destination '{destination}' is the current directory or an ancestor of it. "
            "Use a subdirectory like ./workspace-download instead."
        )
    if destination.exists() and not destination.is_dir():
        raise ValueError(f"Destination '{destination}' exists and is not a directory")

    s3_config = _build_s3_config(repo_name, chronos_url=chronos_url, api_key=api_key, timeout=timeout)
    key = _archive_s3_key(s3_config, archive_md5)
    archive_bytes = s3_download_bytes_sync(s3_config, key)

    if destination.exists() and any(destination.iterdir()):
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
        tmp.write(archive_bytes)
        tmp_path = tmp.name

    try:
        with tarfile.open(tmp_path, "r:gz") as tar:
            if sys.version_info >= (3, 12):
                tar.extractall(destination, filter="data")
            else:
                tar.extractall(destination)
    finally:
        os.unlink(tmp_path)

    # Auto-routed archive refs may not be git workspaces; only re-clone when a
    # bare is actually present, otherwise leave the extracted tree as-is.
    if (destination / ".git-bare").exists():
        repo_dir = _reclone_repo_from_bare(destination)
    else:
        repo_dir = destination
    # Record the dvc dir_name + repo so a later ``upload git`` round-trip
    # restores into the same target the world expects, without the user
    # having to remember either.
    _write_marker(
        destination,
        dir_name=dir_name,
        repo_name=repo_name,
        session_id=session_id,
        step_name=ref_step_name,
    )
    return repo_dir


def register_git_workspace_ref(
    *,
    session_id: str,
    repo_name: str,
    head_sha: str,
    dvc_files: dict[str, str] | None = None,
    step_name: str = _DEFAULT_STEP_NAME,
    chronos_url: str,
    api_key: str,
    timeout: float = 60.0,
) -> WorkspaceRefResponse:
    """Register a workspace ref in Chronos after a manual git upload.

    This mirrors what the world runtime does via ``_record_workspace_ref``
    so manual uploads are discoverable via ``list_workspace_refs`` the same
    way dvc-based checkpoints are.

    ``repo_name`` is the Chronos workspace repo name (e.g. ``code``), NOT
    the S3 tarball key — this ensures the ref shows up in the default
    ``plato chronos download <session-id>`` lookup path.

    ``dvc_files`` carries the DVC YAML (with ``format: archive``) so
    webclone's ``Workspace.restore()`` can download+extract the archive.
    """
    with httpx.Client(base_url=chronos_url.rstrip("/"), timeout=timeout, headers={"X-API-Key": api_key}) as client:
        return create_workspace_ref.sync(
            client,
            session_public_id=session_id,
            body=CreateWorkspaceRefRequest(
                repo_name=repo_name,
                step_name=step_name,
                direction="output",
                dvc_files=dvc_files,
                git_hash=head_sha,
                branch="main",
                changed=True,
            ),
        )


@workspace_upload_app.command("git")
def upload_git(
    session_id: Annotated[str, typer.Argument(help="Chronos session ID")],
    source: Annotated[
        Path,
        typer.Argument(
            help="Git workspace root containing repo/ and .git-bare/, or the repo/ directory inside it.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
        ),
    ] = Path("."),
    repo_name: Annotated[
        str | None,
        typer.Option(
            "--repo",
            "-r",
            help="Chronos workspace repo name for ref registration (default: round-trip marker, else 'code')",
        ),
    ] = None,
    dir_name: Annotated[
        str | None,
        typer.Option(
            "--dir-name",
            help="DVC archive dir name / restore target (default: round-trip marker, else 'data'). "
            "Overrides the nested-layer guard.",
        ),
    ] = None,
    step_name: Annotated[
        str | None,
        typer.Option(
            "--step",
            help="Checkpoint (workspace ref step) name to register under, matched exactly on resume "
            "restore (default: a generated 'manual-upload-<rand>' name marking a manual upload)",
        ),
    ] = None,
    yes: Annotated[bool, typer.Option("--yes", "-y", help="Skip the pre-upload confirmation prompt")] = False,
    commit_message: Annotated[str, typer.Option("--message", "-m", help="Auto-commit message")] = (
        "Upload Chronos git workspace"
    ),
    output: Annotated[
        Path | None, typer.Option("--output-archive", help="Also write the generated tar to this path")
    ] = (None),
    keep_archive: Annotated[bool, typer.Option("--keep-archive", help="Keep the temporary tar after upload")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Create the tar and skip Chronos upload")] = False,
    chronos_url: Annotated[
        str | None, typer.Option("--url", "-u", envvar="CHRONOS_URL", help="Chronos API URL")
    ] = None,
    api_key: Annotated[
        str | None,
        typer.Option("--api-key", "-k", envvar="PLATO_API_KEY", help="Plato API key for authentication"),
    ] = None,
) -> None:
    """Upload a git-backed workspace to Chronos via DVC archive.

    Resolves the dvc payload dir (honoring a round-trip marker / ``--dir-name``
    and rejecting an outer transport layer), pushes repo/ to .git-bare, tars the
    payload's children as a tar.gz, uploads to S3 at a content-addressed key via
    s5cmd, and registers a workspace ref keyed by ``dir_name`` so webclone can
    restore it natively.
    """
    resolved_api_key = api_key or os.environ.get("PLATO_API_KEY")
    if not dry_run and not resolved_api_key:
        console.print("[red]No API key provided[/red]")
        console.print("Set PLATO_API_KEY environment variable or use --api-key")
        raise typer.Exit(1)

    archive: GitWorkspaceArchive | None = None
    try:
        target = _resolve_upload_target(source, dir_name=dir_name, repo_name=repo_name, step_name=step_name)
        ignore_patterns = _read_dvcignore(target.payload_dir)
        console.print(f"[dim]Archiving '{target.payload_dir}' (dir_name='{target.dir_name}')[/dim]")
        console.print("[bold]Upload[/bold]")
        console.print(f"  Session:   {session_id}")
        console.print(f"  Repo:      {target.repo_name}")
        console.print(f"  Step:      {target.step_name}")
        console.print("  Direction: output")
        console.print("  Branch:    main")

        # Confirm before the (mutating) push-to-bare + S3 upload. --yes / --dry-run skip.
        if not dry_run and not yes and not typer.confirm("Proceed with upload?", default=True):
            console.print("[yellow]Aborted.[/yellow]")
            raise typer.Exit(0)

        if dry_run:
            archive = create_git_workspace_archive(
                target.payload_dir,
                commit_message=commit_message,
                output=output,
                ignore_patterns=ignore_patterns,
            )
            console.print(f"[green]Created git workspace archive[/green] {archive.path}")
            console.print(f"[dim]SHA: {archive.head_sha[:12]}[/dim]")
            console.print(f"[dim]Archive size: {archive.size_bytes / 1024 / 1024:.1f} MB[/dim]")
        else:
            head_sha = _sync_repo_to_bare(target.repo_dir, target.bare_dir, commit_message=commit_message)
            resolved_chronos_url = chronos_url or get_settings().chronos_url

            _archive_md5, dvc_yaml = upload_git_workspace_via_archive(
                target.payload_dir,
                repo_name=target.repo_name,
                dir_name=target.dir_name,
                chronos_url=resolved_chronos_url,
                api_key=resolved_api_key or "",
                ignore_patterns=ignore_patterns,
            )
            console.print("[green]Uploaded git workspace via DVC archive[/green]")
            console.print(f"[dim]SHA: {head_sha[:12]}[/dim]")

            try:
                ref = register_git_workspace_ref(
                    session_id=session_id,
                    repo_name=target.repo_name,
                    head_sha=head_sha,
                    dvc_files={target.dir_name: dvc_yaml},
                    step_name=target.step_name,
                    chronos_url=resolved_chronos_url,
                    api_key=resolved_api_key or "",
                )
                console.print(f"[dim]Ref ID: {ref.ref_public_id}[/dim]")
                console.print(f"[dim]Repo: {ref.repo_name}[/dim]")
                console.print(f"[dim]Step: {ref.step_name}[/dim]")
                console.print(f"[dim]Direction: {ref.direction}[/dim]")
                console.print(f"[dim]Branch: {ref.branch}[/dim]")
                console.print(f"[dim]Git hash: {ref.git_hash}[/dim]")
                console.print(f"[dim]Created at: {ref.created_at}[/dim]")
            except Exception as ref_exc:
                console.print(f"[yellow]Warning: archive uploaded but ref registration failed: {ref_exc}[/yellow]")

            if output is not None:
                # Tar the already-synced payload directly — do NOT run a second
                # _sync_repo_to_bare, or the local copy could diverge from the
                # tarball already pushed to S3. Same membership/filtering as the
                # uploaded archive.
                local_path = output.expanduser().resolve()
                local_path.parent.mkdir(parents=True, exist_ok=True)
                _tar_payload_children(target.payload_dir, local_path, ignore_patterns)
                archive = GitWorkspaceArchive(path=local_path, head_sha=head_sha, size_bytes=local_path.stat().st_size)
                console.print(f"[dim]Local archive: {archive.path}[/dim]")
    except typer.Exit:
        raise
    except Exception as exc:
        console.print(f"[red]Failed: {exc}[/red]")
        raise typer.Exit(1) from exc
    finally:
        if archive is not None and output is None and not keep_archive and not dry_run:
            archive.path.unlink(missing_ok=True)
