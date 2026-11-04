"""Data models and S3 helpers for workspace versioning.

Uses DVC-compatible manifest format for S3 storage layout.
No FUSE dependency — safe to import anywhere.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import platform
import shlex
import shutil
import stat as stat_mod
import subprocess
import tempfile
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from plato.chronos.models import DVCManifestEntry

logger = logging.getLogger(__name__)

# Legacy-manifest metadata resolution: max tasks materialized at once
# (memory bound) and max in-flight S3 calls (stampede bound).
_RESOLVE_CHUNK_SIZE = 256
_RESOLVE_CONCURRENCY = 32


def _env_flag_enabled(name: str) -> bool:
    value = os.environ.get(name, "")
    return value.lower() not in {"", "0", "false", "no"}


def _smart_commit_debug(message: str, *args: Any) -> None:
    if _env_flag_enabled("PLATO_SMART_COMMIT_DEBUG"):
        logger.debug("smart_commit_debug: " + message, *args)


def _path_kind_for_debug(path: Path) -> str:
    try:
        st = os.lstat(path)
    except OSError:
        return "missing"
    if stat_mod.S_ISDIR(st.st_mode):
        return "dir"
    if stat_mod.S_ISLNK(st.st_mode):
        return "symlink"
    return "file"


# ============================================================
# Data models
# ============================================================


@dataclass
class S3Config:
    bucket: str
    prefix: str  # e.g. "workspace-repos/<repo-id>"
    credentials: dict[str, str]
    credentials_expires_at: int | None = None
    credential_refresh: dict[str, str | int] | None = None

    @property
    def cache_prefix(self) -> str:
        return f"{self.prefix}/dvc-cache/files/md5"

    def to_dict(self) -> dict:
        aws_creds = {k: v for k, v in self.credentials.items() if k.startswith("AWS_")}
        data: dict[str, object] = {"bucket": self.bucket, "prefix": self.prefix, "credentials": aws_creds}
        if self.credentials_expires_at is not None:
            data["credentials_expires_at"] = self.credentials_expires_at
        if self.credential_refresh is not None:
            data["credential_refresh"] = self.credential_refresh
        return data

    @classmethod
    def from_dict(cls, d: dict) -> S3Config:
        return cls(
            bucket=d["bucket"],
            prefix=d["prefix"],
            credentials=d["credentials"],
            credentials_expires_at=d.get("credentials_expires_at"),
            credential_refresh=d.get("credential_refresh"),
        )


# How many seconds before STS expiry the plato-fuse binary refreshes its credentials.
DEFAULT_CREDENTIAL_REFRESH_MARGIN_S = 300


def credential_refresh_config(
    chronos_url: str,
    repo_id: str,
    api_key: str,
    refresh_margin_seconds: int = DEFAULT_CREDENTIAL_REFRESH_MARGIN_S,
) -> dict[str, str | int]:
    """Build the ``credential_refresh`` block of an :class:`S3Config`.

    Canonical constructor for the contract consumed by the plato-fuse binary
    (``plato-fuse/src/config.rs::CredentialRefreshConfig``): before a lazy download it POSTs
    ``{chronos_url}/api/workspace-repos/{repo_id}/credentials`` with ``X-API-Key: {api_key}``
    to swap in fresh STS credentials. The binary only self-refreshes when the config carries
    BOTH this block and ``credentials_expires_at`` — without either, it silently keeps the
    initial credentials and lazy reads fail with EIO once they expire.
    """
    return {
        "chronos_url": chronos_url.rstrip("/"),
        "repo_id": repo_id,
        "api_key": api_key,
        "refresh_margin_seconds": refresh_margin_seconds,
    }


@dataclass
class DVCManifest:
    entries_list: list[DVCManifestEntry]
    manifest_md5: str

    @classmethod
    async def from_dvc_file(
        cls,
        dvc_content: str,
        s3_config: S3Config,
        *,
        phase_reporter: Callable[[str, float], None] | None = None,
    ) -> DVCManifest:
        """Parse .dvc YAML and download the manifest from S3."""
        started_at = time.monotonic()
        dvc_data = yaml.safe_load(dvc_content)
        if phase_reporter is not None:
            phase_reporter("dvc_yaml_parse", time.monotonic() - started_at)
        outs = dvc_data.get("outs", [])
        if not outs:
            return cls(entries_list=[], manifest_md5="")

        manifest_md5 = outs[0].get("md5", "").replace(".dir", "")
        if not manifest_md5:
            return cls(entries_list=[], manifest_md5="")

        manifest_key = f"{s3_config.cache_prefix}/{manifest_md5[:2]}/{manifest_md5[2:]}.dir"
        started_at = time.monotonic()
        try:
            raw = await s3_download_bytes(s3_config, manifest_key)
        except Exception:
            # Fallback: try without .dir suffix
            manifest_key_alt = f"{s3_config.cache_prefix}/{manifest_md5[:2]}/{manifest_md5[2:]}"
            logger.warning("Manifest not found at %s, trying %s", manifest_key, manifest_key_alt)
            raw = await s3_download_bytes(s3_config, manifest_key_alt)
        if phase_reporter is not None:
            phase_reporter("manifest_download", time.monotonic() - started_at)

        started_at = time.monotonic()
        items = json.loads(raw)
        entries = [DVCManifestEntry(**it) for it in items]
        if phase_reporter is not None:
            phase_reporter("manifest_parse", time.monotonic() - started_at)

        started_at = time.monotonic()
        await cls._resolve_missing_sizes(entries, s3_config)
        if phase_reporter is not None:
            phase_reporter("manifest_resolve_metadata", time.monotonic() - started_at)
        return cls(entries_list=entries, manifest_md5=manifest_md5)

    @staticmethod
    async def _resolve_missing_sizes(entries: list[DVCManifestEntry], s3_config: S3Config) -> None:
        # Bounded fan-out: a fully-legacy manifest ({md5, relpath} only) puts
        # EVERY file entry here — an unbounded gather materializes one task
        # per entry (hundreds of thousands on large datasets) and stampedes
        # S3. Chunked spawning bounds memory; the semaphore caps in-flight
        # S3 calls within a chunk. Mirrors plato-fuse's resolution bound.
        sem = asyncio.Semaphore(_RESOLVE_CONCURRENCY)

        async def _resolve(entry: DVCManifestEntry) -> None:
            if (entry.size or 0) > 0 or entry.isdir:
                return
            if entry.islink:
                if entry.symlink_target is None:
                    if entry.md5:
                        key = dvc_file_key(s3_config, entry.md5)
                        try:
                            raw = await s3_download_bytes(s3_config, key)
                            entry.symlink_target = raw.decode("utf-8")
                            entry.size = len(raw)
                        except Exception as exc:
                            logger.warning(
                                "Could not resolve symlink target for %s from S3: %s",
                                entry.relpath,
                                exc,
                            )
                            entry.size = 0
                    else:
                        entry.size = 0
                    return
                entry.size = len(entry.symlink_target.encode("utf-8"))
                return
            if not entry.md5:
                return

            key = dvc_file_key(s3_config, entry.md5)
            try:
                entry.size = await s3_head_size(s3_config, key)
            except Exception as exc:
                logger.warning(
                    "Could not resolve size for %s from s3://%s/%s: %s",
                    entry.relpath,
                    s3_config.bucket,
                    key,
                    exc,
                )

        async def _bounded(entry: DVCManifestEntry) -> None:
            async with sem:
                await _resolve(entry)

        todo = [entry for entry in entries if (entry.size or 0) == 0]
        for start in range(0, len(todo), _RESOLVE_CHUNK_SIZE):
            await asyncio.gather(*(_bounded(entry) for entry in todo[start : start + _RESOLVE_CHUNK_SIZE]))

    def entries_dict(self) -> dict[str, DVCManifestEntry]:
        return {e.relpath: e for e in self.entries_list}

    def to_dict(self) -> dict:
        return {
            "entries": [e.model_dump(exclude_none=True) for e in self.entries_list],
            "manifest_md5": self.manifest_md5,
        }

    @classmethod
    def from_dict(cls, d: dict) -> DVCManifest:
        return cls(
            entries_list=[DVCManifestEntry(**e) for e in d["entries"]],
            manifest_md5=d["manifest_md5"],
        )


@dataclass
class LazyDVCMount:
    """Handle for a running lazy FUSE mount."""

    mountpoint: Path
    cache_dir: Path
    manifest: DVCManifest
    worker_proc: Any = None
    worker_log_tasks: tuple[Any, ...] | None = None
    # The S3 config the mount was created with. Load-bearing for cross-repo
    # restores: the blobs live under the SOURCE repo's prefix, and the
    # workspace's own repo identity is restored right after restore() —
    # anything re-deriving S3 access for this mount's content (e.g. direct
    # agent-VM fuse mounts) must use THIS config's bucket/prefix/refresh.
    s3_config: S3Config | None = None
    # ``bucket/key`` of every blob smart_commit has uploaded through this mount.
    # The overlay is never drained, so without this every checkpoint re-PUTs
    # every file written since mount. Keys are content-addressed and nothing
    # deletes dvc-cache objects, so a key uploaded once stays valid. Only this
    # process's own uploads count: a restored manifest's blobs may live under
    # another repo's prefix (cross-repo / download-token restores).
    uploaded_keys: set[str] = field(default_factory=set)
    # The last smart_commit's tree, which the next applies plato-fuse's save journal to. None until one
    # finishes in this process: that one scans the whole mount.
    committed: _CommittedTree | None = None
    # Journals taken by smart_commits that didn't finish, oldest first: the next one applies them too.
    pending_journals: list[FuseJournal] = field(default_factory=list)
    # Set when something writes the overlay outside FUSE, which the journal doesn't see: the next
    # smart_commit scans the whole mount.
    journal_invalid: bool = False
    # seq of the last journal taken; a journal whose seq doesn't follow it means one was lost (a take cancelled after
    # plato-fuse had swapped it out). None after a full scan without a journal: any later journal covers that scan.
    journal_seq: int | None = None

    @property
    def meta_path(self) -> Path:
        return self.cache_dir / "meta.json"

    @property
    def overlay_dir(self) -> Path:
        return self.cache_dir / "overlay"


@dataclass
class DirectorySnapshotEntry:
    relpath: str
    mode: int


@dataclass
class DirectoryRenameEntry:
    old_relpath: str
    new_relpath: str


@dataclass
class SmartCommitMetadata:
    modified: set[str]
    deleted: set[str]
    created: set[str]
    directories: list[DirectorySnapshotEntry] | None = None
    dir_renames: list[DirectoryRenameEntry] | None = None


# ============================================================
# S3 helpers
# ============================================================

S5CMD_VERSION = "2.2.2"
S5CMD_RELEASE_BASE_URL = f"https://github.com/peak/s5cmd/releases/download/v{S5CMD_VERSION}"

_s5cmd_checked = False
_s5cmd_binary: str | None = None
_s5cmd_lock = asyncio.Lock()


def _s5cmd_asset_name() -> str:
    system = platform.system()
    machine = platform.machine().lower()

    if system == "Darwin":
        if machine in {"arm64", "aarch64"}:
            return f"s5cmd_{S5CMD_VERSION}_macOS-arm64.tar.gz"
        if machine in {"x86_64", "amd64"}:
            return f"s5cmd_{S5CMD_VERSION}_macOS-64bit.tar.gz"
    elif system == "Linux":
        if machine in {"arm64", "aarch64"}:
            return f"s5cmd_{S5CMD_VERSION}_Linux-arm64.tar.gz"
        if machine in {"x86_64", "amd64"}:
            return f"s5cmd_{S5CMD_VERSION}_Linux-64bit.tar.gz"

    raise RuntimeError(f"Unsupported platform for s5cmd auto-install: {system}/{machine}")


def _s5cmd_release_url() -> str:
    return f"{S5CMD_RELEASE_BASE_URL}/{_s5cmd_asset_name()}"


def _s5cmd_install_path() -> Path:
    global_install = Path("/usr/local/bin/s5cmd")
    if global_install.parent.exists() and os.access(global_install.parent, os.W_OK):
        return global_install

    user_install = Path.home() / ".local" / "bin" / "s5cmd"
    user_install.parent.mkdir(parents=True, exist_ok=True)
    return user_install


def _cached_s5cmd_binary() -> str | None:
    override = os.environ.get("PLATO_S5CMD_BINARY")
    if override:
        override_path = Path(override)
        if not override_path.is_file():
            raise RuntimeError(f"PLATO_S5CMD_BINARY does not exist: {override}")
        return str(override_path)

    binary = shutil.which("s5cmd")
    if binary:
        return binary

    install_path = _s5cmd_install_path()
    if install_path.is_file():
        return str(install_path)
    return None


def _mark_s5cmd_ready(binary: str) -> str:
    global _s5cmd_checked, _s5cmd_binary
    _s5cmd_checked = True
    _s5cmd_binary = binary
    return binary


async def _install_s5cmd_async(binary_path: Path) -> str:
    tmp_dir = Path(tempfile.mkdtemp(prefix="plato-s5cmd-"))
    archive_path = tmp_dir / "s5cmd.tar.gz"
    try:
        download = await asyncio.create_subprocess_exec(
            "curl",
            "-fsSL",
            _s5cmd_release_url(),
            "-o",
            str(archive_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await download.communicate()
        if download.returncode != 0:
            raise RuntimeError(f"Failed to download s5cmd: {stderr.decode().strip()}")

        extract = await asyncio.create_subprocess_exec(
            "tar",
            "-xzf",
            str(archive_path),
            "-C",
            str(tmp_dir),
            "s5cmd",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await extract.communicate()
        if extract.returncode != 0:
            raise RuntimeError(f"Failed to extract s5cmd: {stderr.decode().strip()}")

        binary_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(tmp_dir / "s5cmd", binary_path)
        os.chmod(binary_path, 0o755)
        return str(binary_path)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _install_s5cmd_sync(binary_path: Path) -> str:
    tmp_dir = Path(tempfile.mkdtemp(prefix="plato-s5cmd-"))
    archive_path = tmp_dir / "s5cmd.tar.gz"
    try:
        download = subprocess.run(
            ["curl", "-fsSL", _s5cmd_release_url(), "-o", str(archive_path)],
            capture_output=True,
            text=True,
        )
        if download.returncode != 0:
            raise RuntimeError(f"Failed to download s5cmd: {download.stderr.strip()}")

        extract = subprocess.run(
            ["tar", "-xzf", str(archive_path), "-C", str(tmp_dir), "s5cmd"],
            capture_output=True,
            text=True,
        )
        if extract.returncode != 0:
            raise RuntimeError(f"Failed to extract s5cmd: {extract.stderr.strip()}")

        binary_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(tmp_dir / "s5cmd", binary_path)
        os.chmod(binary_path, 0o755)
        return str(binary_path)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


async def _ensure_s5cmd() -> str:
    """Return an s5cmd binary path, installing it if needed."""
    if _s5cmd_checked and _s5cmd_binary is not None:
        return _s5cmd_binary

    async with _s5cmd_lock:
        if _s5cmd_checked and _s5cmd_binary is not None:
            return _s5cmd_binary

        existing = _cached_s5cmd_binary()
        if existing is not None:
            return _mark_s5cmd_ready(existing)

        install_path = _s5cmd_install_path()
        logger.debug("s5cmd not found, installing to %s", install_path)
        return _mark_s5cmd_ready(await _install_s5cmd_async(install_path))


def _ensure_s5cmd_sync() -> str:
    """Return an s5cmd binary path, installing it if needed."""
    if _s5cmd_checked and _s5cmd_binary is not None:
        return _s5cmd_binary

    existing = _cached_s5cmd_binary()
    if existing is not None:
        return _mark_s5cmd_ready(existing)

    install_path = _s5cmd_install_path()
    logger.debug("s5cmd not found, installing to %s", install_path)
    return _mark_s5cmd_ready(_install_s5cmd_sync(install_path))


def _s3_env(config: S3Config) -> dict[str, str]:
    """Build environment variables for s5cmd calls."""
    env = dict(os.environ)
    env.update({k: v for k, v in config.credentials.items() if k.startswith("AWS_") and v})
    return env


async def s3_download_bytes(config: S3Config, key: str) -> bytes:
    s5cmd_binary = await _ensure_s5cmd()

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        s3_url = f"s3://{config.bucket}/{key}"
        proc = await asyncio.create_subprocess_exec(
            s5cmd_binary,
            "cp",
            s3_url,
            tmp_path,
            env=_s3_env(config),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(f"s5cmd cp failed for {s3_url}: {stderr.decode().strip()}")
        return Path(tmp_path).read_bytes()
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def dvc_files_size_summary(dvc_files: dict[str, str]) -> tuple[int, int]:
    """Total (bytes, file_count) across a ref's dvc-yaml pointers.

    Every smart-commit pointer embeds ``size``/``nfiles`` totals, so a
    workspace ref's full size is known WITHOUT downloading the manifest or
    listing S3 — use this to pick a transport before restoring (large
    read-only datasets belong on an NFS-mounted workspace, not rsync).
    """
    total_bytes = 0
    total_files = 0
    for dvc_yaml in (dvc_files or {}).values():
        try:
            parsed = yaml.safe_load(dvc_yaml)
        except yaml.YAMLError:
            continue
        for out in (parsed or {}).get("outs", []) or []:
            if isinstance(out, dict):
                total_bytes += int(out.get("size") or 0)
                total_files += int(out.get("nfiles") or 0)
    return total_bytes, total_files


async def s3_head_size(config: S3Config, key: str) -> int:
    s5cmd_binary = await _ensure_s5cmd()
    s3_url = f"s3://{config.bucket}/{key}"
    proc = await asyncio.create_subprocess_exec(
        s5cmd_binary,
        "ls",
        s3_url,
        env=_s3_env(config),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    stderr_text = stderr.decode().strip()
    if proc.returncode != 0:
        lower = stderr_text.lower()
        if "not found" in lower or "no object found" in lower or "404" in lower:
            raise FileNotFoundError(s3_url)
        raise RuntimeError(f"s5cmd ls failed for {s3_url}: {stderr_text}")

    lines = [line.strip() for line in stdout.decode().splitlines() if line.strip()]
    if not lines:
        raise FileNotFoundError(s3_url)

    parts = lines[0].split()
    if len(parts) < 4:
        raise RuntimeError(f"unexpected s5cmd ls output for {s3_url}: {lines[0]!r}")

    try:
        return int(parts[-2])
    except ValueError as exc:
        raise RuntimeError(f"unexpected size field in s5cmd ls output for {s3_url}: {lines[0]!r}") from exc


async def s3_upload_bytes(config: S3Config, key: str, data: bytes) -> None:
    s5cmd_binary = await _ensure_s5cmd()

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(data)
        tmp_path = tmp.name

    try:
        s3_url = f"s3://{config.bucket}/{key}"
        proc = await asyncio.create_subprocess_exec(
            s5cmd_binary,
            "cp",
            tmp_path,
            s3_url,
            env=_s3_env(config),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(f"s5cmd cp failed for {s3_url}: {stderr.decode().strip()}")
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


async def s3_upload_batch(config: S3Config, uploads: list[tuple[str, str]]) -> None:
    """Batch upload local files to S3 using s5cmd run."""
    if not uploads:
        return

    s5cmd_binary = await _ensure_s5cmd()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as batch:
        for local_path, s3_key in uploads:
            s3_url = f"s3://{config.bucket}/{s3_key}"
            batch.write(f"cp --raw --if-size-differ {shlex.quote(local_path)} {shlex.quote(s3_url)}\n")
        batch_path = batch.name

    try:
        proc = await asyncio.create_subprocess_exec(
            s5cmd_binary,
            "run",
            batch_path,
            env=_s3_env(config),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(f"s5cmd batch upload failed: {stderr.decode().strip()}")
        logger.debug("Uploaded %d files to S3", len(uploads))
    finally:
        try:
            os.unlink(batch_path)
        except OSError:
            pass


def s3_download_bytes_sync(config: S3Config, key: str) -> bytes:
    """Synchronous S3 download using s5cmd."""
    s5cmd_binary = _ensure_s5cmd_sync()

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        s3_url = f"s3://{config.bucket}/{key}"
        result = subprocess.run(
            [s5cmd_binary, "cp", s3_url, tmp_path],
            env=_s3_env(config),
            capture_output=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"s5cmd cp failed for {s3_url}: {result.stderr.decode().strip()}")
        return Path(tmp_path).read_bytes()
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def s3_download_batch_sync(config: S3Config, downloads: list[tuple[str, str]]) -> None:
    """Batch download S3 objects to local paths using s5cmd run.

    ``downloads`` is a list of ``(s3_key, local_path)`` tuples. s5cmd fetches
    them in parallel and resumes/retries on transient errors; a non-zero exit
    raises so a partial pull never masquerades as success. Callers must create
    parent directories beforehand.
    """
    if not downloads:
        return

    s5cmd_binary = _ensure_s5cmd_sync()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as batch:
        for s3_key, local_path in downloads:
            s3_url = f"s3://{config.bucket}/{s3_key}"
            batch.write(f"cp {shlex.quote(s3_url)} {shlex.quote(local_path)}\n")
        batch_path = batch.name

    try:
        result = subprocess.run(
            [s5cmd_binary, "run", batch_path],
            env=_s3_env(config),
            capture_output=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"s5cmd batch download failed: {result.stderr.decode().strip()}")
    finally:
        try:
            os.unlink(batch_path)
        except OSError:
            pass


def dvc_file_key(s3_config: S3Config, md5: str) -> str:
    """S3 key for a cached file."""
    return f"{s3_config.cache_prefix}/{md5[:2]}/{md5[2:]}"


# ============================================================
# Smart commit
# ============================================================


def _scan_overlay(overlay_dir: Path, ignore_patterns: list[str] | None = None) -> set[str]:
    """Walk the overlay directory and return all file relpaths."""
    result: set[str] = set()
    if not overlay_dir.exists():
        return result

    _ignored_name, _ignored_path = _build_ignore_matchers(ignore_patterns)

    for root, dirs, files in os.walk(overlay_dir):
        rel_root = Path(root).relative_to(overlay_dir)
        kept_dirs: list[str] = []
        for dirname in dirs:
            relpath = str(rel_root / dirname) if str(rel_root) != "." else dirname
            if os.path.islink(os.path.join(root, dirname)):
                # A symlink to a directory is a file entry like any symlink.
                files.append(dirname)
                continue
            if _ignored_name(dirname) or _ignored_path(relpath) or _ignored_path(f"{relpath}/"):
                continue
            kept_dirs.append(dirname)
        dirs[:] = kept_dirs
        for f in files:
            if _ignored_name(f):
                continue
            relpath = str(rel_root / f) if str(rel_root) != "." else f
            if _ignored_path(relpath):
                continue
            result.add(relpath)
    return result


def _build_ignore_matchers(ignore_patterns: list[str] | None = None) -> tuple[Any, Any]:
    import fnmatch as _fnmatch

    bare: list[str] = []
    glob: list[str] = []
    for pattern in ignore_patterns or []:
        pattern = pattern.strip()
        if not pattern or pattern.startswith("#"):
            continue
        if "/" in pattern.rstrip("/"):
            glob.append(pattern.rstrip("/"))
        else:
            bare.append(pattern)

    def _ignored_name(name: str) -> bool:
        return any(_fnmatch.fnmatch(name, pat) for pat in bare)

    def _ignored_path(relpath: str) -> bool:
        return any(_fnmatch.fnmatch(relpath, pat) for pat in glob)

    return _ignored_name, _ignored_path


def _scan_mount_directories(mountpoint: Path, ignore_patterns: list[str] | None = None) -> dict[str, int]:
    """Walk the live mount and return all non-root directory relpaths and modes."""
    result: dict[str, int] = {}
    if not mountpoint.exists():
        return result

    _ignored_name, _ignored_path = _build_ignore_matchers(ignore_patterns)

    for root, dirs, _files in os.walk(mountpoint, followlinks=False):
        rel_root = Path(root).relative_to(mountpoint)
        kept_dirs: list[str] = []
        for dirname in dirs:
            relpath = str(rel_root / dirname) if str(rel_root) != "." else dirname
            full_path = Path(root) / dirname
            if os.path.islink(full_path):
                continue
            if _ignored_name(dirname) or _ignored_path(relpath):
                continue
            try:
                mode = stat_mod.S_IMODE(os.lstat(full_path).st_mode)
            except OSError:
                continue
            kept_dirs.append(dirname)
            result[relpath] = mode
        dirs[:] = kept_dirs
    return result


def _load_smart_commit_metadata(meta_path: Path) -> SmartCommitMetadata:
    if not meta_path.exists():
        return SmartCommitMetadata(modified=set(), deleted=set(), created=set())

    try:
        meta = json.loads(meta_path.read_text())
    except (json.JSONDecodeError, OSError):
        return SmartCommitMetadata(modified=set(), deleted=set(), created=set())

    directories_raw = meta.get("directories")
    dir_renames_raw = meta.get("dir_renames")
    directories = None
    if isinstance(directories_raw, list):
        directories = [
            DirectorySnapshotEntry(relpath=str(entry["relpath"]), mode=int(entry["mode"]))
            for entry in directories_raw
            if isinstance(entry, dict) and "relpath" in entry and "mode" in entry
        ]
    dir_renames = None
    if isinstance(dir_renames_raw, list):
        dir_renames = [
            DirectoryRenameEntry(
                old_relpath=str(entry["old_relpath"]),
                new_relpath=str(entry["new_relpath"]),
            )
            for entry in dir_renames_raw
            if isinstance(entry, dict) and "old_relpath" in entry and "new_relpath" in entry
        ]

    return SmartCommitMetadata(
        modified=set(meta.get("modified", [])),
        deleted=set(meta.get("deleted", [])),
        created=set(meta.get("created", [])),
        directories=directories,
        dir_renames=dir_renames,
    )


def _remap_path_prefix(relpath: str, old_prefix: str, new_prefix: str) -> str:
    if relpath == old_prefix:
        return new_prefix
    old_dir_prefix = f"{old_prefix}/"
    if relpath.startswith(old_dir_prefix):
        return f"{new_prefix}/{relpath.removeprefix(old_dir_prefix)}"
    return relpath


def _apply_dir_renames_to_entries(
    entries: dict[str, DVCManifestEntry],
    dir_renames: list[DirectoryRenameEntry] | None,
) -> dict[str, DVCManifestEntry]:
    if not dir_renames:
        return entries

    remapped: dict[str, DVCManifestEntry] = {}
    # relpath -> depth of the rename that put its entry there (-1: not moved).
    landed_by: dict[str, int] = {}
    ordered_renames = sorted(dir_renames, key=lambda entry: len(entry.old_relpath), reverse=True)
    for entry in entries.values():
        relpath = entry.relpath
        depth = -1
        for rename in ordered_renames:
            new_relpath = _remap_path_prefix(relpath, rename.old_relpath, rename.new_relpath)
            if new_relpath != relpath:
                relpath = new_relpath
                depth = len(rename.new_relpath)
                break
        remapped_entry = entry.model_copy(update={"relpath": relpath})
        existing = remapped.get(relpath)
        if existing is not None and existing != remapped_entry:
            # A rename lands only where nothing is left (rm -r d; mv e d), so the rename into the deeper directory
            # came later and its file is the one there now.
            if depth == landed_by[relpath]:
                raise RuntimeError(f"Directory rename produced conflicting manifest entries for {relpath}")
            if depth < landed_by[relpath]:
                continue
        landed_by[relpath] = depth
        remapped[relpath] = remapped_entry
    return remapped


@dataclass
class FuseJournal:
    """What changed on a plato-fuse mount since the previous ``take-journal`` (its ``ctl.sock``).

    ``touched`` and ``deleted`` are paths in the tree as of the take (earlier names follow the
    ``dir_renames``, applied in order); ``directories`` is every directory at the take."""

    seq: int
    touched: list[str]
    deleted: list[str]
    dir_renames: list[DirectoryRenameEntry]
    directories: list[DirectorySnapshotEntry]

    def is_empty(self) -> bool:
        return not (self.touched or self.deleted or self.dir_renames)


@dataclass
class _CommittedTree:
    """A smart commit's tree: the base the next one applies the mount's journals to."""

    files: dict[str, DVCManifestEntry]
    dir_modes: dict[str, int]
    # The restored manifest's files under their current paths, as restored: a path the overlay doesn't
    # hold keeps its restored entry.
    original: dict[str, DVCManifestEntry]
    # relpath -> the entry's JSON in the manifest, so a commit serializes only the entries that changed.
    fragments: dict[str, str]
    # Paths this commit read from the disk. A dir rename the next journal reports may have moved one between the
    # journal take and the read: the next commit looks at those again under their new names.
    decided: set[str] = field(default_factory=set)
    ignore_patterns: tuple[str, ...] = ()
    # (bucket, cache prefix) the tree's blobs were uploaded to.
    destination: tuple[str, str] = ("", "")
    # The journal directories this tree was built at; None when no journal was taken.
    journal_directories: list[DirectorySnapshotEntry] | None = None
    manifest_md5: str = ""
    total_size: int = 0
    file_count: int = 0


_JOURNAL_TIMEOUT_S = 5.0


async def take_journal(mount: LazyDVCMount) -> FuseJournal | None:
    """Take the mount's save journal from plato-fuse; None without one (no control socket, an older
    binary, an error), and the save then scans the whole mount."""
    sock_path = mount.cache_dir / "ctl.sock"
    if not sock_path.exists():
        return None
    writer: asyncio.StreamWriter | None = None
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_unix_connection(str(sock_path)), _JOURNAL_TIMEOUT_S)
        writer.write(b"take-journal\n")
        await writer.drain()
        payload = json.loads(await asyncio.wait_for(reader.read(), _JOURNAL_TIMEOUT_S))
        if payload.get("version") != 1:
            raise ValueError(f"unsupported journal {str(payload)[:200]}")
        return FuseJournal(
            seq=int(payload["seq"]),
            touched=[str(relpath) for relpath in payload["touched"]],
            deleted=[str(relpath) for relpath in payload["deleted"]],
            dir_renames=[
                DirectoryRenameEntry(old_relpath=str(entry["old_relpath"]), new_relpath=str(entry["new_relpath"]))
                for entry in payload["dir_renames"]
            ],
            directories=[
                DirectorySnapshotEntry(relpath=str(entry["relpath"]), mode=int(entry["mode"]))
                for entry in payload["directories"]
            ],
        )
    except (OSError, ValueError, KeyError, TypeError, AttributeError, TimeoutError) as e:
        logger.warning("No save journal from %s, scanning the whole mount: %r", sock_path, e)
        return None
    finally:
        if writer is not None:
            writer.close()


@dataclass
class _SmartCommitPlan:
    """The part of a smart commit that reads the disk: the new manifest and the blobs to upload."""

    manifest_json: bytes
    manifest_md5: str
    total_size: int
    file_count: int
    dir_count: int
    modified_count: int
    created_count: int
    deleted_count: int
    # (temp path, S3 key) pairs; the temp files hold the bytes that were hashed.
    batch_uploads: list[tuple[str, str]]
    temp_files: list[str]
    queued_keys: set[str]
    tree: _CommittedTree


def _unlink_temp_files(temp_files: list[str]) -> None:
    for tmp_path in temp_files:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def _discard_abandoned_plan(build: asyncio.Future[_SmartCommitPlan]) -> None:
    """Remove the temp files of a plan whose smart_commit was cancelled while the thread ran."""
    if build.cancelled() or build.exception() is not None:
        # A failed build removes its own temp files.
        return
    _unlink_temp_files(build.result().temp_files)


def _dvc_yaml(manifest_md5: str, total_size: int, file_count: int, dir_name: str) -> str:
    return (
        f"outs:\n"
        f"- md5: {manifest_md5}.dir\n"
        f"  size: {total_size}\n"
        f"  nfiles: {file_count}\n"
        f"  hash: md5\n"
        f"  path: {dir_name}\n"
    )


async def smart_commit(
    mount: LazyDVCMount,
    s3_config: S3Config,
    dir_name: str = "data",
    ignore_patterns: list[str] | None = None,
) -> tuple[str, str, bool]:
    """Build a new manifest from overlay changes. Upload only changed files.

    Returns ``(manifest_md5, dvc_yaml_content, changed)``; ``changed`` is False when the manifest is the
    previous smart_commit's on this mount.

    With plato-fuse's journal of what changed since the previous smart_commit, only those paths are read;
    otherwise (first commit of the process, no journal, overlay written outside FUSE) the whole mount is
    scanned. Scan, reads and MD5 run in a worker thread; on the loop they stall merges and heartbeats.
    """
    journal = await take_journal(mount)
    journal_lost = False
    if journal is not None:
        journal_lost = mount.journal_seq is not None and journal.seq != mount.journal_seq + 1
        mount.journal_seq = journal.seq
        mount.pending_journals.append(journal)
    journals = list(mount.pending_journals)
    force_full = mount.journal_invalid or journal_lost
    mount.journal_invalid = False
    base = mount.committed
    patterns = tuple(ignore_patterns or ())
    destination = (s3_config.bucket, s3_config.cache_prefix)
    incremental = (
        journal is not None
        and not force_full
        and base is not None
        and base.ignore_patterns == patterns
        and base.destination == destination
    )
    if (
        incremental
        and base is not None
        and journal is not None
        and all(taken.is_empty() for taken in journals)
        and journal.directories == base.journal_directories
    ):
        del mount.pending_journals[: len(journals)]
        logger.debug("Smart commit: nothing changed, manifest=%s", base.manifest_md5)
        return base.manifest_md5, _dvc_yaml(base.manifest_md5, base.total_size, base.file_count, dir_name), False

    live_worker_running = mount.worker_proc is not None and mount.worker_proc.returncode is None
    try:
        if incremental and base is not None:
            build = asyncio.ensure_future(
                asyncio.to_thread(
                    _build_journal_smart_commit_plan,
                    mount,
                    s3_config,
                    ignore_patterns,
                    base,
                    journals,
                    frozenset(mount.uploaded_keys),
                    live_worker_running,
                )
            )
        else:
            build = asyncio.ensure_future(
                asyncio.to_thread(
                    _build_smart_commit_plan,
                    mount,
                    s3_config,
                    ignore_patterns,
                    live_worker_running,
                    frozenset(mount.uploaded_keys),
                )
            )
        try:
            # The shield keeps the build future alive on a cancel, so the callback
            # can remove the temp files that the thread writes after the cancel.
            plan = await asyncio.shield(build)
        except asyncio.CancelledError:
            build.add_done_callback(_discard_abandoned_plan)
            raise

        try:
            if plan.batch_uploads:
                await s3_upload_batch(s3_config, plan.batch_uploads)
                # Only after the whole batch succeeded: a failed batch raises, so
                # the next checkpoint retries every key it queued.
                mount.uploaded_keys |= plan.queued_keys
        finally:
            _unlink_temp_files(plan.temp_files)

        manifest_json = plan.manifest_json
        manifest_md5 = plan.manifest_md5
        manifest_key = f"{s3_config.cache_prefix}/{manifest_md5[:2]}/{manifest_md5[2:]}.dir"
        manifest_upload_id = f"{s3_config.bucket}/{manifest_key}"
        if manifest_upload_id not in mount.uploaded_keys:
            await s3_upload_bytes(s3_config, manifest_key, manifest_json)

            # Verify manifest was uploaded
            verify = await s3_download_bytes(s3_config, manifest_key)
            if len(verify) != len(manifest_json):
                raise RuntimeError(
                    f"Manifest verification failed: uploaded {len(manifest_json)} bytes but read back {len(verify)} bytes"
                )
            mount.uploaded_keys.add(manifest_upload_id)
    except BaseException:
        # The journals stay pending for the next commit.
        if force_full:
            mount.journal_invalid = True
        raise

    plan.tree.ignore_patterns = patterns
    plan.tree.destination = destination
    if journal is None:
        mount.journal_seq = None
    plan.tree.journal_directories = journal.directories if journal is not None else None
    plan.tree.manifest_md5 = manifest_md5
    plan.tree.total_size = plan.total_size
    plan.tree.file_count = plan.file_count
    mount.committed = plan.tree
    del mount.pending_journals[: len(journals)]
    changed = base is None or base.manifest_md5 != manifest_md5

    logger.debug(
        "Smart commit (%s): %d entries (%d files, %d directories, %d modified, %d new, %d deleted), manifest=%s",
        "journal" if incremental else "full scan",
        plan.file_count + plan.dir_count,
        plan.file_count,
        plan.dir_count,
        plan.modified_count,
        plan.created_count,
        plan.deleted_count,
        manifest_md5,
    )
    return manifest_md5, _dvc_yaml(manifest_md5, plan.total_size, plan.file_count, dir_name), changed


class _OverlayHasher:
    """Reads and hashes overlay files for a plan, queueing the blobs not yet in S3; removes its temp files
    if the plan fails."""

    def __init__(self, overlay_dir: Path, s3_config: S3Config, uploaded_keys: frozenset[str]) -> None:
        self.overlay_dir = overlay_dir
        self.s3_config = s3_config
        self.uploaded_keys = uploaded_keys
        self.batch_uploads: list[tuple[str, str]] = []
        self.temp_files: list[str] = []
        self.queued_keys: set[str] = set()
        self.hashed: set[str] = set()

    def entry(self, relpath: str) -> tuple[DVCManifestEntry, int]:
        self.hashed.add(relpath)
        local_path = self.overlay_dir / relpath
        if not os.path.lexists(local_path):
            raise FileNotFoundError(f"Missing overlay path: {local_path}")

        st = os.lstat(local_path)
        mode = stat_mod.S_IMODE(st.st_mode)
        is_symlink = stat_mod.S_ISLNK(st.st_mode)
        symlink_target = os.readlink(local_path) if is_symlink else None
        if is_symlink:
            if symlink_target is None:
                raise RuntimeError(f"Expected symlink target for {local_path}")
            data = symlink_target.encode("utf-8")
        else:
            data = local_path.read_bytes()
        size = len(data)
        new_md5 = hashlib.md5(data).hexdigest()
        key = dvc_file_key(self.s3_config, new_md5)
        upload_id = f"{self.s3_config.bucket}/{key}"

        if upload_id not in self.uploaded_keys and upload_id not in self.queued_keys:
            # Upload the bytes that were hashed, not the live overlay path: a
            # write landing between the hash and the batch upload would
            # otherwise store different bytes under this md5 key.
            tmp = tempfile.NamedTemporaryFile(delete=False)
            tmp.write(data)
            tmp.close()
            self.temp_files.append(tmp.name)
            self.batch_uploads.append((tmp.name, key))
            self.queued_keys.add(upload_id)

        entry = DVCManifestEntry(
            relpath=relpath,
            md5=new_md5,
            size=size,
            isexec=True if (not is_symlink and mode & 0o111) else None,
            islink=True if is_symlink else None,
            symlink_target=symlink_target,
        )
        return entry, size


def _restored_entry_now(entry: DVCManifestEntry, mountpoint: Path) -> DVCManifestEntry:
    """A restored entry the overlay doesn't hold; one restored without a size takes the mount's."""
    entry_size = entry.size or 0
    if entry_size == 0 and entry.md5:
        try:
            entry_size = os.lstat(mountpoint / entry.relpath).st_size
        except OSError:
            pass
    if entry_size != (entry.size or 0):
        return entry.model_copy(update={"size": entry_size})
    return entry


def _serialize_manifest(
    files: dict[str, DVCManifestEntry], dir_modes: dict[str, int], base: _CommittedTree
) -> tuple[bytes, dict[str, str]]:
    """The manifest JSON of a tree, byte-identical to ``json.dumps`` of its sorted entries, and each entry's JSON.
    Entries unchanged since ``base`` reuse its JSON."""
    conflicts = files.keys() & dir_modes.keys()
    if conflicts:
        raise RuntimeError(f"Smart commit produced conflicting manifest entries for {min(conflicts)}")
    fragments: dict[str, str] = {}
    for relpath, entry in files.items():
        fragment = base.fragments.get(relpath) if base.files.get(relpath) is entry else None
        fragments[relpath] = fragment or json.dumps(entry.model_dump(exclude_none=True))
    for relpath, mode in dir_modes.items():
        fragment = base.fragments.get(relpath) if base.dir_modes.get(relpath) == mode else None
        fragments[relpath] = fragment or json.dumps(
            DVCManifestEntry(relpath=relpath, mode=mode, isdir=True).model_dump(exclude_none=True)
        )
    manifest_json = ("[" + ", ".join(fragments[relpath] for relpath in sorted(fragments)) + "]").encode()
    return manifest_json, fragments


def _build_smart_commit_plan(
    mount: LazyDVCMount,
    s3_config: S3Config,
    ignore_patterns: list[str] | None,
    live_worker_running: bool,
    uploaded_keys: frozenset[str],
) -> _SmartCommitPlan:
    """The full scan: walks the overlay and the mount's directories and hashes every overlay file. Runs in a
    worker thread; removes its temp files if it fails."""
    overlay_dir = mount.overlay_dir
    mountpoint = mount.mountpoint
    original = mount.manifest.entries_dict()
    meta_path = mount.meta_path
    live_dir_renames_path = mount.cache_dir / "live-dir-renames.json"
    _smart_commit_debug(
        "start mountpoint=%s cache_dir=%s live_worker_running=%s original_entries=%d",
        mountpoint,
        mount.cache_dir,
        live_worker_running,
        len(original),
    )
    if live_worker_running:
        meta = _load_smart_commit_metadata(live_dir_renames_path)
    else:
        meta = _load_smart_commit_metadata(meta_path)
    original_files = {relpath: entry for relpath, entry in original.items() if not entry.isdir}
    original_files = _apply_dir_renames_to_entries(original_files, meta.dir_renames)
    if live_worker_running or meta.directories is None:
        dir_modes = _scan_mount_directories(mountpoint, ignore_patterns=ignore_patterns)
    else:
        _ignored_name, _ignored_path = _build_ignore_matchers(ignore_patterns)
        dir_modes = {
            entry.relpath: entry.mode
            for entry in meta.directories
            if not _ignored_name(Path(entry.relpath).name)
            and not _ignored_path(entry.relpath)
            and not _ignored_path(f"{entry.relpath}/")
        }

    def _current_path_kind(relpath: str) -> str:
        if relpath in dir_modes:
            return "dir"
        if os.path.lexists(overlay_dir / relpath):
            return "file"
        try:
            st = os.lstat(mountpoint / relpath)
        except OSError:
            return "missing"
        return "dir" if stat_mod.S_ISDIR(st.st_mode) else "file"

    overlay_files = _scan_overlay(overlay_dir, ignore_patterns=ignore_patterns)
    _smart_commit_debug(
        "scanned overlay_files=%d dir_modes=%d deleted=%d created_meta=%d modified_meta=%d",
        len(overlay_files),
        len(dir_modes),
        len(meta.deleted),
        len(meta.created),
        len(meta.modified),
    )
    overlay_dir_conflicts = sorted(relpath for relpath in overlay_files if relpath in dir_modes)
    if overlay_dir_conflicts:
        sample = [
            f"{relpath}:{_path_kind_for_debug(overlay_dir / relpath)}->{_path_kind_for_debug(mountpoint / relpath)}"
            for relpath in overlay_dir_conflicts[:20]
        ]
        _smart_commit_debug(
            "overlay file paths also visible as directories count=%d sample=%s",
            len(overlay_dir_conflicts),
            sample,
        )
    modified: set[str] = set()
    created: set[str] = set()
    for relpath in overlay_files:
        if relpath in original_files:
            modified.add(relpath)
        else:
            created.add(relpath)

    # A deleted restored path that the overlay doesn't hold shows a file on the mount only when a dir rename moved
    # another restored file there (rm -r d; mv e d): the mount decides below.
    deleted = {
        relpath for relpath in meta.deleted if relpath in original_files and os.path.lexists(overlay_dir / relpath)
    }

    # Files that appear in both meta.deleted and the overlay were deleted then
    # re-created (e.g. cross-device mv overwrites via unlink+create).  The
    # overlay is authoritative — if the file exists there it is not deleted.
    resurrected = deleted & overlay_files
    if resurrected:
        _smart_commit_debug(
            "resurrected files (in deleted AND overlay): count=%d sample=%s",
            len(resurrected),
            list(resurrected)[:5],
        )
        deleted -= resurrected
        modified |= resurrected

    for relpath in original_files:
        if relpath in deleted:
            continue
        current_kind = _current_path_kind(relpath)
        if current_kind != "file":
            _smart_commit_debug(
                "dropping original file relpath=%s because current_kind=%s overlay_kind=%s mount_kind=%s",
                relpath,
                current_kind,
                _path_kind_for_debug(overlay_dir / relpath),
                _path_kind_for_debug(mountpoint / relpath),
            )
            deleted.add(relpath)

    entries_by_relpath: dict[str, DVCManifestEntry] = {}
    total_size = 0
    hasher = _OverlayHasher(overlay_dir, s3_config, uploaded_keys)

    def _store_manifest_entry(entry: DVCManifestEntry) -> None:
        existing = entries_by_relpath.get(entry.relpath)
        if existing is not None and existing != entry:
            _smart_commit_debug(
                "manifest conflict relpath=%s existing=%s new=%s",
                entry.relpath,
                existing,
                entry,
            )
            raise RuntimeError(f"Smart commit produced conflicting manifest entries for {entry.relpath}")
        entries_by_relpath[entry.relpath] = entry

    # Everything that writes temp copies sits inside the try so a failed read
    # never leaves them behind. On success, smart_commit removes them after
    # the upload.
    try:
        for relpath, entry in original_files.items():
            if relpath in deleted:
                continue
            if relpath in modified:
                if _current_path_kind(relpath) != "file":
                    deleted.add(relpath)
                    continue
                new_entry, size = hasher.entry(relpath)
                _store_manifest_entry(new_entry)
                total_size += size
            else:
                entry_size = entry.size or 0
                if entry_size == 0 and entry.md5:
                    try:
                        entry_size = os.lstat(mountpoint / relpath).st_size
                    except OSError:
                        pass
                if entry_size != (entry.size or 0):
                    entry = entry.model_copy(update={"size": entry_size})
                _store_manifest_entry(entry)
                total_size += entry_size

        for relpath in created:
            current_kind = _current_path_kind(relpath)
            if current_kind != "file" or not os.path.lexists(overlay_dir / relpath):
                if os.path.lexists(overlay_dir / relpath):
                    _smart_commit_debug(
                        "skipping created relpath=%s because current_kind=%s overlay_kind=%s mount_kind=%s",
                        relpath,
                        current_kind,
                        _path_kind_for_debug(overlay_dir / relpath),
                        _path_kind_for_debug(mountpoint / relpath),
                    )
                continue
            new_entry, size = hasher.entry(relpath)
            _store_manifest_entry(new_entry)
            total_size += size

        for relpath, mode in dir_modes.items():
            _store_manifest_entry(DVCManifestEntry(relpath=relpath, mode=mode, isdir=True))

        entries = [entries_by_relpath[relpath].model_dump(exclude_none=True) for relpath in sorted(entries_by_relpath)]
        if len(entries) != len({entry["relpath"] for entry in entries}):
            raise RuntimeError("Smart commit produced duplicate manifest relpaths")
        file_count = sum(1 for entry in entries if not entry.get("isdir"))
        _smart_commit_debug(
            "final manifest entries=%d files=%d dirs=%d modified=%d created=%d deleted=%d",
            len(entries),
            file_count,
            len(entries) - file_count,
            len(modified),
            len(created),
            len(deleted),
        )

        manifest_json = json.dumps(entries).encode()
        manifest_md5 = hashlib.md5(manifest_json).hexdigest()
    except BaseException:
        _unlink_temp_files(hasher.temp_files)
        raise

    return _SmartCommitPlan(
        manifest_json=manifest_json,
        manifest_md5=manifest_md5,
        total_size=total_size,
        file_count=file_count,
        dir_count=len(entries) - file_count,
        modified_count=len(modified),
        created_count=len(created),
        deleted_count=len(deleted),
        batch_uploads=hasher.batch_uploads,
        temp_files=hasher.temp_files,
        queued_keys=hasher.queued_keys,
        tree=_CommittedTree(
            files={relpath: entry for relpath, entry in entries_by_relpath.items() if not entry.isdir},
            dir_modes=dict(dir_modes),
            original=original_files,
            fragments={entry["relpath"]: json.dumps(entry) for entry in entries},
            # Hashed files, and restored files the scan found missing (a rename mid-scan can hide either).
            decided=hasher.hashed | (original_files.keys() - entries_by_relpath.keys()),
        ),
    )


class _OverlayWalk:
    """What ``_scan_overlay``'s walk would find at a path, without walking."""

    def __init__(self, overlay_dir: Path, ignore_patterns: list[str] | None) -> None:
        self.overlay_dir = overlay_dir
        self._ignored_name, self._ignored_path = _build_ignore_matchers(ignore_patterns)
        self._walked: dict[str, bool] = {"": True}

    def _walks_into(self, rel_dir: str) -> bool:
        walked = self._walked.get(rel_dir)
        if walked is None:
            parent, _, name = rel_dir.rpartition("/")
            walked = (
                self._walks_into(parent)
                and not self._ignored_name(name)
                and not self._ignored_path(rel_dir)
                and not self._ignored_path(f"{rel_dir}/")
            )
            if walked:
                try:
                    walked = stat_mod.S_ISDIR(os.lstat(self.overlay_dir / rel_dir).st_mode)
                except OSError:
                    walked = False
            self._walked[rel_dir] = walked
        return walked

    def has_file(self, relpath: str) -> bool:
        parent, _, name = relpath.rpartition("/")
        if not self._walks_into(parent) or self._ignored_name(name) or self._ignored_path(relpath):
            return False
        local_path = self.overlay_dir / relpath
        return os.path.lexists(local_path) and (os.path.islink(local_path) or not os.path.isdir(local_path))


def _journal_dir_modes(directories: list[DirectorySnapshotEntry], ignore_patterns: list[str] | None) -> dict[str, int]:
    """The journal's directories as ``_scan_mount_directories`` finds them: without ignored ones or their
    subtrees."""
    _ignored_name, _ignored_path = _build_ignore_matchers(ignore_patterns)
    kept_dirs: dict[str, bool] = {"": True}

    def _kept(relpath: str) -> bool:
        kept = kept_dirs.get(relpath)
        if kept is None:
            parent, _, name = relpath.rpartition("/")
            kept = _kept(parent) and not _ignored_name(name) and not _ignored_path(relpath)
            kept_dirs[relpath] = kept
        return kept

    return {entry.relpath: entry.mode for entry in directories if _kept(entry.relpath)}


def _rename_may_change_ignores(rename: DirectoryRenameEntry, ignore_patterns: list[str] | None) -> bool:
    """Whether the ignore patterns may treat a renamed directory's contents differently at its new path."""
    _ignored_name, _ignored_path = _build_ignore_matchers(ignore_patterns)
    if any(
        "/" in pattern.strip().rstrip("/") for pattern in ignore_patterns or [] if not pattern.strip().startswith("#")
    ):
        return True

    def _ignored_prefix(relpath: str) -> bool:
        parts = relpath.split("/")
        return any(_ignored_name(name) for name in parts)

    return _ignored_prefix(rename.old_relpath) != _ignored_prefix(rename.new_relpath)


def _overlay_paths_under(prefix: str, overlay_dir: Path) -> set[str]:
    """Every path at or under ``prefix`` in the overlay."""
    paths: set[str] = set()
    for root, dirnames, filenames in os.walk(overlay_dir / prefix):
        rel_root = Path(root).relative_to(overlay_dir)
        paths.update(str(rel_root / name) for name in (*dirnames, *filenames))
    return paths


def _paths_under(
    prefix: str, files: dict[str, DVCManifestEntry], original: dict[str, DVCManifestEntry], overlay_dir: Path
) -> set[str]:
    """Every path at or under ``prefix`` that the tree or the overlay holds."""
    dir_prefix = f"{prefix}/"
    paths = {relpath for relpath in (*files, *original) if relpath == prefix or relpath.startswith(dir_prefix)}
    return paths | _overlay_paths_under(prefix, overlay_dir)


def _move_prefix(entries: dict[str, DVCManifestEntry], old_prefix: str, new_prefix: str) -> None:
    """Re-key the entries under a renamed directory; they replace whatever the new paths held."""
    old_dir_prefix = f"{old_prefix}/"
    moved = [relpath for relpath in entries if relpath == old_prefix or relpath.startswith(old_dir_prefix)]
    moved_entries = [entries.pop(relpath) for relpath in moved]
    for relpath, entry in zip(moved, moved_entries, strict=True):
        new_relpath = _remap_path_prefix(relpath, old_prefix, new_prefix)
        entries[new_relpath] = entry.model_copy(update={"relpath": new_relpath})


def _build_journal_smart_commit_plan(
    mount: LazyDVCMount,
    s3_config: S3Config,
    ignore_patterns: list[str] | None,
    base: _CommittedTree,
    journals: list[FuseJournal],
    uploaded_keys: frozenset[str],
    live_worker_running: bool,
) -> _SmartCommitPlan:
    """The last commit's tree with the journals applied: only the paths they name are looked at, each
    decided as the full scan would. Runs in a worker thread; removes its temp files if it fails."""
    overlay_dir = mount.overlay_dir
    mountpoint = mount.mountpoint
    files = dict(base.files)
    original = dict(base.original)
    changed_paths: set[str] = set()
    # Paths the last commit read: one a dir rename moved may have been read mid-move.
    recheck = set(base.decided)
    # Renamed directories whose files the ignore patterns may now treat differently: all looked at again.
    rescan_prefixes: set[str] = set()
    # Renamed directories: files written into one just before it moved may be in no journal under the new name.
    renamed_prefixes: set[str] = set()
    for journal in journals:
        for rename in journal.dir_renames:
            old_prefix, new_prefix = rename.old_relpath, rename.new_relpath
            _move_prefix(files, old_prefix, new_prefix)
            _move_prefix(original, old_prefix, new_prefix)
            changed_paths = {_remap_path_prefix(relpath, old_prefix, new_prefix) for relpath in changed_paths}
            moved = {relpath for relpath in recheck if relpath == old_prefix or relpath.startswith(f"{old_prefix}/")}
            changed_paths.update(_remap_path_prefix(relpath, old_prefix, new_prefix) for relpath in moved)
            recheck = {_remap_path_prefix(relpath, old_prefix, new_prefix) for relpath in recheck}
            rescan_prefixes = {_remap_path_prefix(relpath, old_prefix, new_prefix) for relpath in rescan_prefixes}
            renamed_prefixes = {_remap_path_prefix(relpath, old_prefix, new_prefix) for relpath in renamed_prefixes}
            renamed_prefixes.add(new_prefix)
            if _rename_may_change_ignores(rename, ignore_patterns):
                rescan_prefixes.add(new_prefix)
        changed_paths.update(journal.touched)
        changed_paths.update(journal.deleted)
    for prefix in rescan_prefixes:
        changed_paths.update(_paths_under(prefix, files, original, overlay_dir))
    for prefix in renamed_prefixes - rescan_prefixes:
        changed_paths.update(_overlay_paths_under(prefix, overlay_dir) - files.keys())
    dir_modes = _journal_dir_modes(journals[-1].directories, ignore_patterns)
    overlay = _OverlayWalk(overlay_dir, ignore_patterns)
    hasher = _OverlayHasher(overlay_dir, s3_config, uploaded_keys)

    def _is_file_now(relpath: str) -> bool:
        if os.path.lexists(overlay_dir / relpath):
            return True
        try:
            return not stat_mod.S_ISDIR(os.lstat(mountpoint / relpath).st_mode)
        except OSError:
            return False

    deleted_this_session: set[str] | None = None

    def _deleted_restored() -> set[str]:
        """plato-fuse's session-wide deleted paths: the full scan drops a restored entry the overlay holds there."""
        nonlocal deleted_this_session
        if deleted_this_session is None:
            meta_path = mount.cache_dir / "live-dir-renames.json" if live_worker_running else mount.meta_path
            deleted_this_session = _load_smart_commit_metadata(meta_path).deleted
        return deleted_this_session

    modified_count = created_count = deleted_count = 0
    try:
        for relpath in sorted(changed_paths):
            had_entry = files.pop(relpath, None) is not None
            if relpath in dir_modes:
                deleted_count += had_entry
                continue
            if overlay.has_file(relpath):
                try:
                    files[relpath], _size = hasher.entry(relpath)
                except (FileNotFoundError, NotADirectoryError, IsADirectoryError):
                    # Moved or removed since: that change is in the next journal.
                    deleted_count += had_entry
                    continue
                modified_count += had_entry
                created_count += not had_entry
                continue
            restored = original.get(relpath)
            if (
                restored is not None
                and _is_file_now(relpath)
                and not (os.path.lexists(overlay_dir / relpath) and relpath in _deleted_restored())
            ):
                files[relpath] = _restored_entry_now(restored, mountpoint)
            else:
                deleted_count += had_entry
        manifest_json, fragments = _serialize_manifest(files, dir_modes, base)
        manifest_md5 = hashlib.md5(manifest_json).hexdigest()
        file_count = len(files)
        dir_count = len(dir_modes)
        total_size = sum(entry.size or 0 for entry in files.values())
    except BaseException:
        _unlink_temp_files(hasher.temp_files)
        raise
    _smart_commit_debug(
        "journal plan changed_paths=%d files=%d dirs=%d hashed=%d",
        len(changed_paths),
        file_count,
        dir_count,
        modified_count + created_count,
    )
    return _SmartCommitPlan(
        manifest_json=manifest_json,
        manifest_md5=manifest_md5,
        total_size=total_size,
        file_count=file_count,
        dir_count=dir_count,
        modified_count=modified_count,
        created_count=created_count,
        deleted_count=deleted_count,
        batch_uploads=hasher.batch_uploads,
        temp_files=hasher.temp_files,
        queued_keys=hasher.queued_keys,
        tree=_CommittedTree(
            files=files, dir_modes=dir_modes, original=original, fragments=fragments, decided=changed_paths
        ),
    )


# ============================================================
# Archive commit (single tar.gz)
# ============================================================


def _archive_s3_key(s3_config: S3Config, archive_md5: str) -> str:
    """S3 key for an archive blob."""
    return f"{s3_config.cache_prefix}/{archive_md5[:2]}/{archive_md5[2:]}"


async def smart_commit_archive(
    source_dir: Path,
    s3_config: S3Config,
    dir_name: str = "data",
    ignore_patterns: list[str] | None = None,
) -> tuple[str, str]:
    """Tar.gz the entire source directory and upload as a single S3 object.

    Returns ``(archive_md5, dvc_yaml_content)`` where the YAML includes
    ``format: archive`` so restore knows to download+extract instead of
    using the per-file manifest approach.
    """
    import tarfile

    _ignored_name, _ignored_path = _build_ignore_matchers(ignore_patterns)

    def _tar_filter(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo | None:
        name = tarinfo.name
        parts = Path(name).parts
        for part in parts:
            if _ignored_name(part):
                return None
        if _ignored_path(name) or _ignored_path(f"{name}/"):
            return None
        return tarinfo

    def _tar_and_hash() -> tuple[bytes, str]:
        # The worker makes and removes the temp file itself. A cancel does not
        # stop a to_thread worker, so a temp file that the event loop removes
        # can be written again by the worker after the removal.
        fd, tmp_path = tempfile.mkstemp(suffix=".tar.gz")
        os.close(fd)
        try:
            with tarfile.open(tmp_path, "w:gz") as tar:
                for entry in sorted(os.scandir(source_dir), key=lambda e: e.name):
                    tar.add(
                        entry.path,
                        arcname=entry.name,
                        filter=_tar_filter,
                    )
            data = Path(tmp_path).read_bytes()
            return data, hashlib.md5(data).hexdigest()
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    # Off the loop: a large tree would stall merges and heartbeats (see smart_commit).
    archive_bytes, archive_md5 = await asyncio.to_thread(_tar_and_hash)
    archive_size = len(archive_bytes)

    key = _archive_s3_key(s3_config, archive_md5)
    await s3_upload_bytes(s3_config, key, archive_bytes)

    dvc_yaml = (
        f"outs:\n- md5: {archive_md5}\n  size: {archive_size}\n  hash: md5\n  path: {dir_name}\n  format: archive\n"
    )

    logger.debug(
        "Archive commit: %s (%d bytes), md5=%s",
        dir_name,
        archive_size,
        archive_md5,
    )
    return archive_md5, dvc_yaml


async def restore_archive(
    dvc_content: str,
    s3_config: S3Config,
    target_dir: Path,
) -> None:
    """Download an archive blob from S3 and extract to target_dir."""
    import tarfile

    dvc_data = yaml.safe_load(dvc_content)
    outs = dvc_data.get("outs", [])
    if not outs:
        return

    archive_md5 = outs[0].get("md5", "")
    if not archive_md5:
        return

    key = _archive_s3_key(s3_config, archive_md5)
    archive_bytes = await s3_download_bytes(s3_config, key)

    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
        tmp.write(archive_bytes)
        tmp_path = tmp.name

    try:
        with tarfile.open(tmp_path, "r:gz") as tar:
            import sys

            if sys.version_info >= (3, 12):
                tar.extractall(path=target_dir, filter="data")
            else:
                tar.extractall(path=target_dir)
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

    logger.debug("Archive restore: extracted to %s (%d bytes)", target_dir, len(archive_bytes))


def parse_dvc_format(dvc_content: str) -> str:
    """Return the format of a .dvc file: 'archive' or 'manifest'."""
    dvc_data = yaml.safe_load(dvc_content)
    outs = dvc_data.get("outs", [])
    if not outs:
        return "manifest"
    return outs[0].get("format", "manifest")
