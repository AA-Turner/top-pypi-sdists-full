"""DVC data models and S3 helpers — no FUSE dependency.

These are extracted from ``lazy_dvc.py`` so that ``workspace.py`` can import
them without pulling in pyfuse3 (which is only available on the world VM).
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
    """S3 configuration for DVC cache access."""

    bucket: str
    prefix: str  # e.g. "workspace-repos/<repo-id>"
    credentials: dict[str, str]  # AWS_ACCESS_KEY_ID, etc.

    @property
    def cache_prefix(self) -> str:
        """S3 key prefix for DVC file cache (DVC 3.x layout)."""
        return f"{self.prefix}/dvc-cache/files/md5"

    def to_dict(self) -> dict:
        # Only serialize AWS credentials — not the whole env
        aws_creds = {k: v for k, v in self.credentials.items() if k.startswith("AWS_")}
        return {"bucket": self.bucket, "prefix": self.prefix, "credentials": aws_creds}

    @classmethod
    def from_dict(cls, d: dict) -> S3Config:
        return cls(bucket=d["bucket"], prefix=d["prefix"], credentials=d["credentials"])


@dataclass
class DVCFileEntry:
    """A file entry from a DVC .dir manifest."""

    relpath: str
    md5: str
    size: int = 0
    mode: int = 0o644
    is_symlink: bool = False
    symlink_target: str = ""

    def to_dict(self) -> dict:
        data: dict[str, Any] = {"relpath": self.relpath, "md5": self.md5, "size": self.size}
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
    """Parsed DVC .dir manifest — metadata for all files in a tracked directory."""

    entries_list: list[DVCFileEntry]
    manifest_md5: str

    @classmethod
    async def from_dvc_file(cls, dvc_content: str, s3_config: S3Config) -> DVCManifest:
        """Parse .dvc YAML and download the .dir manifest from S3."""
        dvc_data = yaml.safe_load(dvc_content)
        outs = dvc_data.get("outs", [])
        if not outs:
            return cls(entries_list=[], manifest_md5="")

        manifest_md5 = outs[0].get("md5", "").replace(".dir", "")
        if not manifest_md5:
            return cls(entries_list=[], manifest_md5="")

        # DVC 3.x: {cache_prefix}/{hash[:2]}/{hash[2:]}.dir
        manifest_key = f"{s3_config.cache_prefix}/{manifest_md5[:2]}/{manifest_md5[2:]}.dir"
        raw = await s3_download_bytes(s3_config, manifest_key)
        items = json.loads(raw)

        return cls(
            entries_list=[DVCFileEntry.from_dict(it) for it in items],
            manifest_md5=manifest_md5,
        )

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
    """Handle for a running lazy DVC FUSE mount."""

    mountpoint: Path
    cache_dir: Path
    manifest: DVCManifest
    worker_proc: Any = None  # asyncio.subprocess.Process

    @property
    def meta_path(self) -> Path:
        return self.cache_dir / "meta.json"

    @property
    def overlay_dir(self) -> Path:
        return self.cache_dir / "overlay"


# ============================================================
# S3 helpers
# ============================================================


def make_s3_client(config: S3Config):
    import boto3

    return boto3.client(
        "s3",
        aws_access_key_id=config.credentials.get("AWS_ACCESS_KEY_ID", ""),
        aws_secret_access_key=config.credentials.get("AWS_SECRET_ACCESS_KEY", ""),
        aws_session_token=config.credentials.get("AWS_SESSION_TOKEN"),
        region_name=config.credentials.get("AWS_DEFAULT_REGION", "us-east-1"),
    )


async def s3_download_bytes(config: S3Config, key: str) -> bytes:
    def _do():
        client = make_s3_client(config)
        return client.get_object(Bucket=config.bucket, Key=key)["Body"].read()

    return await asyncio.get_event_loop().run_in_executor(None, _do)


async def s3_upload_bytes(config: S3Config, key: str, data: bytes) -> None:
    def _do():
        client = make_s3_client(config)
        client.put_object(Bucket=config.bucket, Key=key, Body=data)

    await asyncio.get_event_loop().run_in_executor(None, _do)


def s3_download_bytes_sync(config: S3Config, key: str) -> bytes:
    client = make_s3_client(config)
    return client.get_object(Bucket=config.bucket, Key=key)["Body"].read()


def dvc_file_key(s3_config: S3Config, md5: str) -> str:
    """S3 key for a DVC cached file (3.x layout)."""
    return f"{s3_config.cache_prefix}/{md5[:2]}/{md5[2:]}"


# ============================================================
# Smart commit (no FUSE dependency)
# ============================================================


async def smart_commit(
    mount: LazyDVCMount,
    s3_config: S3Config,
    dir_name: str = "data",
) -> tuple[str, str]:
    """Build a new DVC manifest from overlay changes.  Upload only changed files.

    Returns ``(manifest_md5, dvc_yaml_content)``.
    """
    overlay_dir = mount.overlay_dir
    meta_path = mount.meta_path
    original = mount.manifest.entries_dict()

    meta: dict[str, Any] = {}
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())

    modified: set[str] = set(meta.get("modified", []))
    deleted: set[str] = set(meta.get("deleted", []))
    created: set[str] = set(meta.get("created", []))

    entries: list[dict[str, Any]] = []
    total_size = 0

    async def _entry_from_overlay(relpath: str) -> tuple[dict[str, Any], int]:
        local_path = overlay_dir / relpath
        if not os.path.lexists(local_path):
            raise FileNotFoundError(f"Missing overlay path for modified entry: {local_path}")

        st = os.lstat(local_path)
        mode = stat_mod.S_IMODE(st.st_mode)
        is_symlink = stat_mod.S_ISLNK(st.st_mode)
        symlink_target = os.readlink(local_path) if is_symlink else ""
        data = symlink_target.encode("utf-8") if is_symlink else local_path.read_bytes()
        size = len(data)
        new_md5 = hashlib.md5(data).hexdigest()
        key = dvc_file_key(s3_config, new_md5)
        await s3_upload_bytes(s3_config, key, data)
        entry = DVCFileEntry(
            relpath=relpath,
            md5=new_md5,
            size=size,
            mode=mode,
            is_symlink=is_symlink,
            symlink_target=symlink_target,
        ).to_dict()
        return entry, size

    # Original manifest entries
    for relpath, entry in original.items():
        if relpath in deleted:
            continue
        if relpath in modified:
            new_entry, size = await _entry_from_overlay(relpath)
            entries.append(new_entry)
            total_size += size
        else:
            # Untouched — reuse original entry (no S3 traffic)
            entries.append(entry.to_dict())
            total_size += entry.size

    # New files
    for relpath in created:
        if relpath in original:
            continue
        local_path = overlay_dir / relpath
        if not os.path.lexists(local_path):
            continue
        new_entry, size = await _entry_from_overlay(relpath)
        entries.append(new_entry)
        total_size += size

    entries.sort(key=lambda e: e["relpath"])

    # Upload new manifest
    manifest_json = json.dumps(entries).encode()
    manifest_md5 = hashlib.md5(manifest_json).hexdigest()
    manifest_key = f"{s3_config.cache_prefix}/{manifest_md5[:2]}/{manifest_md5[2:]}.dir"
    await s3_upload_bytes(s3_config, manifest_key, manifest_json)

    dvc_yaml = (
        f"outs:\n"
        f"- md5: {manifest_md5}.dir\n"
        f"  size: {total_size}\n"
        f"  nfiles: {len(entries)}\n"
        f"  hash: md5\n"
        f"  path: {dir_name}\n"
    )

    logger.info(
        "Smart commit: %d files, %d modified, %d new, %d deleted",
        len(entries),
        len(modified),
        len(created),
        len(deleted),
    )
    return manifest_md5, dvc_yaml
