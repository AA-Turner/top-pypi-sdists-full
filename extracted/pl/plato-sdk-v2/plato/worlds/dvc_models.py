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
import stat as stat_mod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


# ============================================================
# Data models
# ============================================================


@dataclass
class S3Config:
    bucket: str
    prefix: str  # e.g. "workspace-repos/<repo-id>"
    credentials: dict[str, str]

    @property
    def cache_prefix(self) -> str:
        return f"{self.prefix}/dvc-cache/files/md5"

    def to_dict(self) -> dict:
        aws_creds = {k: v for k, v in self.credentials.items() if k.startswith("AWS_")}
        return {"bucket": self.bucket, "prefix": self.prefix, "credentials": aws_creds}

    @classmethod
    def from_dict(cls, d: dict) -> S3Config:
        return cls(bucket=d["bucket"], prefix=d["prefix"], credentials=d["credentials"])


@dataclass
class DVCFileEntry:
    relpath: str
    md5: str
    size: int = 0
    mode: int = 0o644
    is_symlink: bool = False
    symlink_target: str = ""

    def to_dict(self) -> dict:
        data: dict[str, Any] = {
            "relpath": self.relpath,
            "md5": self.md5,
            "size": self.size,
        }
        if not self.is_symlink and self.mode & 0o111:
            data["isexec"] = True
        if self.is_symlink:
            data["islink"] = True
            if self.symlink_target:
                data["symlink_target"] = self.symlink_target
        return data

    @classmethod
    def from_dict(cls, d: dict) -> DVCFileEntry:
        mode = 0o755 if d.get("isexec") else 0o644
        return cls(
            relpath=d["relpath"],
            md5=d["md5"],
            size=d.get("size", 0),
            mode=mode,
            is_symlink=bool(d.get("islink")),
            symlink_target=str(d.get("symlink_target") or ""),
        )


@dataclass
class DVCManifest:
    entries_list: list[DVCFileEntry]
    manifest_md5: str

    @classmethod
    async def from_dvc_file(cls, dvc_content: str, s3_config: S3Config) -> DVCManifest:
        """Parse .dvc YAML and download the manifest from S3."""
        dvc_data = yaml.safe_load(dvc_content)
        outs = dvc_data.get("outs", [])
        if not outs:
            return cls(entries_list=[], manifest_md5="")

        manifest_md5 = outs[0].get("md5", "").replace(".dir", "")
        if not manifest_md5:
            return cls(entries_list=[], manifest_md5="")

        manifest_key = f"{s3_config.cache_prefix}/{manifest_md5[:2]}/{manifest_md5[2:]}.dir"
        try:
            raw = await s3_download_bytes(s3_config, manifest_key)
        except Exception:
            # Fallback: try without .dir suffix
            manifest_key_alt = f"{s3_config.cache_prefix}/{manifest_md5[:2]}/{manifest_md5[2:]}"
            logger.warning("Manifest not found at %s, trying %s", manifest_key, manifest_key_alt)
            raw = await s3_download_bytes(s3_config, manifest_key_alt)
        items = json.loads(raw)
        entries = [DVCFileEntry.from_dict(it) for it in items]

        return cls(entries_list=entries, manifest_md5=manifest_md5)

    def entries_dict(self) -> dict[str, DVCFileEntry]:
        return {e.relpath: e for e in self.entries_list}

    def to_dict(self) -> dict:
        return {
            "entries": [e.to_dict() for e in self.entries_list],
            "manifest_md5": self.manifest_md5,
        }

    @classmethod
    def from_dict(cls, d: dict) -> DVCManifest:
        return cls(
            entries_list=[DVCFileEntry.from_dict(e) for e in d["entries"]],
            manifest_md5=d["manifest_md5"],
        )


@dataclass
class LazyDVCMount:
    """Handle for a running lazy FUSE mount."""

    mountpoint: Path
    cache_dir: Path
    manifest: DVCManifest
    worker_proc: Any = None

    @property
    def meta_path(self) -> Path:
        return self.cache_dir / "meta.json"

    @property
    def overlay_dir(self) -> Path:
        return self.cache_dir / "overlay"


# ============================================================
# S3 helpers
# ============================================================

_s5cmd_checked = False


async def _ensure_s5cmd() -> None:
    """Install s5cmd if not found on PATH."""
    global _s5cmd_checked
    if _s5cmd_checked:
        return
    import shutil

    if shutil.which("s5cmd"):
        _s5cmd_checked = True
        return

    logger.info("s5cmd not found, installing...")
    proc = await asyncio.create_subprocess_exec(
        "bash",
        "-c",
        "curl -fsSL https://github.com/peak/s5cmd/releases/download/v2.2.2/s5cmd_2.2.2_Linux-64bit.tar.gz "
        "| tar xzf - -C /usr/local/bin s5cmd",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"Failed to install s5cmd: {stderr.decode().strip()}")
    _s5cmd_checked = True
    logger.info("Installed s5cmd to /usr/local/bin/s5cmd")


def _s3_env(config: S3Config) -> dict[str, str]:
    """Build environment variables for s5cmd calls."""
    env = dict(os.environ)
    env.update({k: v for k, v in config.credentials.items() if k.startswith("AWS_") and v})
    return env


async def s3_download_bytes(config: S3Config, key: str) -> bytes:
    await _ensure_s5cmd()
    import tempfile

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        s3_url = f"s3://{config.bucket}/{key}"
        proc = await asyncio.create_subprocess_exec(
            "s5cmd",
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


async def s3_upload_bytes(config: S3Config, key: str, data: bytes) -> None:
    await _ensure_s5cmd()
    import tempfile

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(data)
        tmp_path = tmp.name

    try:
        s3_url = f"s3://{config.bucket}/{key}"
        proc = await asyncio.create_subprocess_exec(
            "s5cmd",
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

    await _ensure_s5cmd()
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as batch:
        for local_path, s3_key in uploads:
            s3_url = f"s3://{config.bucket}/{s3_key}"
            batch.write(f"cp {local_path} {s3_url}\n")
        batch_path = batch.name

    try:
        proc = await asyncio.create_subprocess_exec(
            "s5cmd",
            "run",
            batch_path,
            env=_s3_env(config),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(f"s5cmd batch upload failed: {stderr.decode().strip()}")
        logger.info("Uploaded %d files to S3", len(uploads))
    finally:
        try:
            os.unlink(batch_path)
        except OSError:
            pass


def s3_download_bytes_sync(config: S3Config, key: str) -> bytes:
    """Synchronous S3 download using s5cmd."""
    import subprocess
    import tempfile

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        s3_url = f"s3://{config.bucket}/{key}"
        result = subprocess.run(
            ["s5cmd", "cp", s3_url, tmp_path],
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

    import fnmatch as _fnmatch

    bare: list[str] = []
    glob: list[str] = []
    for p in ignore_patterns or []:
        p = p.strip()
        if not p or p.startswith("#"):
            continue
        if "/" in p.rstrip("/"):
            glob.append(p.rstrip("/"))
        else:
            bare.append(p)

    def _ignored_name(name: str) -> bool:
        return any(_fnmatch.fnmatch(name, pat) for pat in bare)

    def _ignored_path(relpath: str) -> bool:
        return any(_fnmatch.fnmatch(relpath, pat) for pat in glob)

    for root, dirs, files in os.walk(overlay_dir):
        dirs[:] = [d for d in dirs if not _ignored_name(d)]
        rel_root = Path(root).relative_to(overlay_dir)
        for f in files:
            if _ignored_name(f):
                continue
            relpath = str(rel_root / f) if str(rel_root) != "." else f
            if glob and _ignored_path(relpath):
                continue
            result.add(relpath)
    return result


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
    original = mount.manifest.entries_dict()

    overlay_files = _scan_overlay(overlay_dir, ignore_patterns=ignore_patterns)
    modified: set[str] = set()
    created: set[str] = set()
    for relpath in overlay_files:
        if relpath in original:
            modified.add(relpath)
        else:
            created.add(relpath)

    meta_path = mount.meta_path
    deleted: set[str] = set()
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text())
            deleted = set(meta.get("deleted", []))
        except (json.JSONDecodeError, OSError):
            pass

    mountpoint = mount.mountpoint
    for relpath in original:
        if relpath in modified or relpath in deleted:
            continue
        if not os.path.lexists(mountpoint / relpath):
            deleted.add(relpath)

    entries: list[dict[str, Any]] = []
    total_size = 0
    import tempfile

    batch_uploads: list[tuple[str, str]] = []
    temp_files: list[str] = []

    def _process_overlay_file(relpath: str) -> tuple[dict[str, Any], int]:
        local_path = overlay_dir / relpath
        if not os.path.lexists(local_path):
            raise FileNotFoundError(f"Missing overlay path: {local_path}")

        st = os.lstat(local_path)
        mode = stat_mod.S_IMODE(st.st_mode)
        is_symlink = stat_mod.S_ISLNK(st.st_mode)
        symlink_target = os.readlink(local_path) if is_symlink else ""
        data = symlink_target.encode("utf-8") if is_symlink else local_path.read_bytes()
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

        entry = DVCFileEntry(
            relpath=relpath,
            md5=new_md5,
            size=size,
            mode=mode,
            is_symlink=is_symlink,
            symlink_target=symlink_target,
        ).to_dict()
        return entry, size

    for relpath, entry in original.items():
        if relpath in deleted:
            continue
        if relpath in modified:
            new_entry, size = _process_overlay_file(relpath)
            entries.append(new_entry)
            total_size += size
        else:
            if entry.size == 0 and entry.md5:
                try:
                    entry.size = os.lstat(mountpoint / relpath).st_size
                except OSError:
                    pass
            entries.append(entry.to_dict())
            total_size += entry.size

    for relpath in created:
        if relpath in original:
            continue
        if not os.path.lexists(overlay_dir / relpath):
            continue
        new_entry, size = _process_overlay_file(relpath)
        entries.append(new_entry)
        total_size += size

    if batch_uploads:
        await s3_upload_batch(s3_config, batch_uploads)

    for tmp_path in temp_files:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

    entries.sort(key=lambda e: e["relpath"])

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
        f"  nfiles: {len(entries)}\n"
        f"  hash: md5\n"
        f"  path: {dir_name}\n"
    )

    logger.info(
        "Smart commit: %d files (%d modified, %d new, %d deleted), manifest=%s",
        len(entries),
        len(modified),
        len(created),
        len(deleted),
        manifest_md5,
    )
    return manifest_md5, dvc_yaml
