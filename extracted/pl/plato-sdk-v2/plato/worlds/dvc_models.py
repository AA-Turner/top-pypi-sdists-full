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
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from plato.chronos.models import DVCManifestEntry

logger = logging.getLogger(__name__)


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

        await asyncio.gather(*(_resolve(entry) for entry in entries if (entry.size or 0) == 0))

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
            batch.write(f"cp --raw {shlex.quote(local_path)} {shlex.quote(s3_url)}\n")
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
    ordered_renames = sorted(dir_renames, key=lambda entry: len(entry.old_relpath), reverse=True)
    for entry in entries.values():
        relpath = entry.relpath
        for rename in ordered_renames:
            new_relpath = _remap_path_prefix(relpath, rename.old_relpath, rename.new_relpath)
            if new_relpath != relpath:
                relpath = new_relpath
                break
        remapped_entry = entry.model_copy(update={"relpath": relpath})
        existing = remapped.get(relpath)
        if existing is not None and existing != remapped_entry:
            raise RuntimeError(f"Directory rename produced conflicting manifest entries for {relpath}")
        remapped[relpath] = remapped_entry
    return remapped


async def smart_commit(
    mount: LazyDVCMount,
    s3_config: S3Config,
    dir_name: str = "data",
    ignore_patterns: list[str] | None = None,
) -> tuple[str, str]:
    """Build a new manifest from overlay changes. Upload only changed files.

    Returns ``(manifest_md5, dvc_yaml_content)``.
    """
    overlay_dir = mount.overlay_dir
    mountpoint = mount.mountpoint
    original = mount.manifest.entries_dict()
    meta_path = mount.meta_path
    live_dir_renames_path = mount.cache_dir / "live-dir-renames.json"
    live_worker_running = mount.worker_proc is not None and mount.worker_proc.returncode is None
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

    deleted = set(meta.deleted)

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
    import tempfile

    batch_uploads: list[tuple[str, str]] = []
    temp_files: list[str] = []

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

    def _process_overlay_file(relpath: str) -> tuple[DVCManifestEntry, int]:
        local_path = overlay_dir / relpath
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
        key = dvc_file_key(s3_config, new_md5)

        if is_symlink:
            tmp = tempfile.NamedTemporaryFile(delete=False)
            tmp.write(data)
            tmp.close()
            temp_files.append(tmp.name)
            batch_uploads.append((tmp.name, key))
        else:
            batch_uploads.append((str(local_path), key))

        entry = DVCManifestEntry(
            relpath=relpath,
            md5=new_md5,
            size=size,
            isexec=True if (not is_symlink and mode & 0o111) else None,
            islink=True if is_symlink else None,
            symlink_target=symlink_target,
        )
        return entry, size

    for relpath, entry in original_files.items():
        if relpath in deleted:
            continue
        if relpath in modified:
            if _current_path_kind(relpath) != "file":
                deleted.add(relpath)
                continue
            new_entry, size = _process_overlay_file(relpath)
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
        new_entry, size = _process_overlay_file(relpath)
        _store_manifest_entry(new_entry)
        total_size += size

    for relpath, mode in dir_modes.items():
        _store_manifest_entry(DVCManifestEntry(relpath=relpath, mode=mode, isdir=True))

    if batch_uploads:
        await s3_upload_batch(s3_config, batch_uploads)

    for tmp_path in temp_files:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

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
    manifest_key = f"{s3_config.cache_prefix}/{manifest_md5[:2]}/{manifest_md5[2:]}.dir"
    await s3_upload_bytes(s3_config, manifest_key, manifest_json)

    # Verify manifest was uploaded
    verify = await s3_download_bytes(s3_config, manifest_key)
    if len(verify) != len(manifest_json):
        raise RuntimeError(
            f"Manifest verification failed: uploaded {len(manifest_json)} bytes but read back {len(verify)} bytes"
        )

    dvc_yaml = (
        f"outs:\n"
        f"- md5: {manifest_md5}.dir\n"
        f"  size: {total_size}\n"
        f"  nfiles: {file_count}\n"
        f"  hash: md5\n"
        f"  path: {dir_name}\n"
    )

    logger.debug(
        "Smart commit: %d entries (%d files, %d directories, %d modified, %d new, %d deleted), manifest=%s",
        len(entries),
        file_count,
        len(entries) - file_count,
        len(modified),
        len(created),
        len(deleted),
        manifest_md5,
    )
    return manifest_md5, dvc_yaml


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

    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        with tarfile.open(tmp_path, "w:gz") as tar:
            for entry in sorted(os.scandir(source_dir), key=lambda e: e.name):
                tar.add(
                    entry.path,
                    arcname=entry.name,
                    filter=_tar_filter,
                )

        archive_bytes = Path(tmp_path).read_bytes()
        archive_size = len(archive_bytes)
        archive_md5 = hashlib.md5(archive_bytes).hexdigest()

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
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


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
