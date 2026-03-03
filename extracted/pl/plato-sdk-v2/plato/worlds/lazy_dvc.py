"""Lazy DVC workspace via FUSE — files appear present but content downloads on first read.

Each lazy mount runs as a subprocess to avoid asyncio deadlocks between
the world's event loop and FUSE handlers.  The worker process owns the
pyfuse3 event loop; the parent interacts with the mount like a normal
filesystem.

On commit, ``smart_commit()`` builds a new .dir manifest without
re-downloading untouched files — only modified/new files are uploaded.

Requires: libfuse3-dev, fuse3 (system), pyfuse3>=3.3 (Python).  Linux only.
"""

from __future__ import annotations

import asyncio
import errno
import hashlib
import json
import logging
import os
import stat as stat_mod
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, cast

import yaml

logger = logging.getLogger(__name__)


class _PyFuse3Module(Protocol):
    Operations: type
    ROOT_INODE: int
    EntryAttributes: type
    FileInfo: type
    StatvfsData: type
    FUSEError: type[Exception]
    default_options: set[str]

    def readdir_reply(self, token: Any, name: bytes, attrs: Any, next_id: int) -> bool: ...

    def init(self, operations: Any, mountpoint: str, options: set[str]) -> None: ...

    async def main(self) -> None: ...

    def close(self) -> None: ...


# pyfuse3 is optional — only needed on the world VM for lazy restore
try:
    import pyfuse3 as _pyfuse3_raw

    _pyfuse3: _PyFuse3Module | None = cast(_PyFuse3Module, _pyfuse3_raw)
    HAS_PYFUSE3 = True
except ImportError:
    HAS_PYFUSE3 = False
    _pyfuse3 = None

pyfuse3 = _pyfuse3


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

    def to_dict(self) -> dict:
        return {"relpath": self.relpath, "md5": self.md5, "size": self.size}

    @classmethod
    def from_dict(cls, d: dict) -> DVCFileEntry:
        return cls(relpath=d["relpath"], md5=d["md5"], size=d.get("size", 0))


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
        raw = await _s3_download_bytes(s3_config, manifest_key)
        items = json.loads(raw)

        return cls(
            entries_list=[DVCFileEntry(relpath=it["relpath"], md5=it["md5"], size=it.get("size", 0)) for it in items],
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


# ============================================================
# S3 helpers
# ============================================================


def _make_s3_client(config: S3Config):
    import boto3

    return boto3.client(
        "s3",
        aws_access_key_id=config.credentials.get("AWS_ACCESS_KEY_ID", ""),
        aws_secret_access_key=config.credentials.get("AWS_SECRET_ACCESS_KEY", ""),
        aws_session_token=config.credentials.get("AWS_SESSION_TOKEN"),
        region_name=config.credentials.get("AWS_DEFAULT_REGION", "us-east-1"),
    )


async def _s3_download_bytes(config: S3Config, key: str) -> bytes:
    def _do():
        client = _make_s3_client(config)
        return client.get_object(Bucket=config.bucket, Key=key)["Body"].read()

    return await asyncio.get_event_loop().run_in_executor(None, _do)


async def _s3_upload_bytes(config: S3Config, key: str, data: bytes) -> None:
    def _do():
        client = _make_s3_client(config)
        client.put_object(Bucket=config.bucket, Key=key, Body=data)

    await asyncio.get_event_loop().run_in_executor(None, _do)


def _s3_download_bytes_sync(config: S3Config, key: str) -> bytes:
    client = _make_s3_client(config)
    return client.get_object(Bucket=config.bucket, Key=key)["Body"].read()


def _dvc_file_key(s3_config: S3Config, md5: str) -> str:
    """S3 key for a DVC cached file (3.x layout)."""
    return f"{s3_config.cache_prefix}/{md5[:2]}/{md5[2:]}"


# ============================================================
# Public API (used by workspace.py)
# ============================================================


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


async def mount_lazy(
    mountpoint: Path,
    manifest: DVCManifest,
    s3_config: S3Config,
    cache_dir: Path,
) -> LazyDVCMount:
    """Mount a lazy FUSE filesystem at *mountpoint*.

    The FUSE loop runs in a child process so the parent's asyncio
    loop is never blocked by filesystem operations on the mount.
    """
    if not HAS_PYFUSE3:
        raise RuntimeError(
            "pyfuse3 is not installed. Install with: pip install 'plato-sdk-v2[worlds]'\n"
            "Also need: apt-get install libfuse3-dev fuse3"
        )

    # Write config for the worker process
    config_path = cache_dir / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "manifest": manifest.to_dict(),
                "s3_config": s3_config.to_dict(),
                "mountpoint": str(mountpoint),
                "cache_dir": str(cache_dir),
            }
        )
    )

    (cache_dir / "overlay").mkdir(parents=True, exist_ok=True)
    (cache_dir / "cache").mkdir(parents=True, exist_ok=True)

    # Start worker subprocess
    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        "plato.worlds.lazy_dvc",
        str(config_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # Wait for the mount to appear (up to ~10 s)
    for _ in range(100):
        if os.path.ismount(str(mountpoint)):
            break
        await asyncio.sleep(0.1)
    else:
        try:
            proc.kill()
            _, stderr = await asyncio.wait_for(proc.communicate(), timeout=5)
            err = stderr.decode() if stderr else "unknown"
        except Exception:
            err = "unknown"
        raise RuntimeError(f"FUSE mount at {mountpoint} did not appear: {err}")

    logger.info("Lazy DVC mounted at %s (%d files)", mountpoint, len(manifest.entries_list))
    return LazyDVCMount(
        mountpoint=mountpoint,
        cache_dir=cache_dir,
        manifest=manifest,
        worker_proc=proc,
    )


async def unmount_lazy(mount: LazyDVCMount) -> None:
    """Unmount a lazy FUSE filesystem and wait for the worker to write metadata."""
    proc = await asyncio.create_subprocess_exec(
        "fusermount3",
        "-u",
        str(mount.mountpoint),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await proc.wait()

    if mount.worker_proc:
        try:
            await asyncio.wait_for(mount.worker_proc.wait(), timeout=10)
        except asyncio.TimeoutError:
            mount.worker_proc.kill()
            await mount.worker_proc.wait()

    logger.debug("Lazy DVC unmounted from %s", mount.mountpoint)


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

    entries: list[dict] = []
    total_size = 0

    # Original manifest entries
    for relpath, entry in original.items():
        if relpath in deleted:
            continue
        if relpath in modified:
            local_path = overlay_dir / relpath
            data = local_path.read_bytes()
            new_md5 = hashlib.md5(data).hexdigest()
            key = _dvc_file_key(s3_config, new_md5)
            await _s3_upload_bytes(s3_config, key, data)
            size = len(data)
            entries.append({"md5": new_md5, "relpath": relpath})
            total_size += size
        else:
            # Untouched — reuse original entry (no S3 traffic)
            entries.append({"md5": entry.md5, "relpath": relpath})
            total_size += entry.size

    # New files
    for relpath in created:
        if relpath in original:
            continue
        local_path = overlay_dir / relpath
        if not local_path.exists():
            continue
        data = local_path.read_bytes()
        new_md5 = hashlib.md5(data).hexdigest()
        key = _dvc_file_key(s3_config, new_md5)
        await _s3_upload_bytes(s3_config, key, data)
        size = len(data)
        entries.append({"md5": new_md5, "relpath": relpath})
        total_size += size

    entries.sort(key=lambda e: e["relpath"])

    # Upload new manifest
    manifest_json = json.dumps(entries).encode()
    manifest_md5 = hashlib.md5(manifest_json).hexdigest()
    manifest_key = f"{s3_config.cache_prefix}/{manifest_md5[:2]}/{manifest_md5[2:]}.dir"
    await _s3_upload_bytes(s3_config, manifest_key, manifest_json)

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


# ============================================================
# FUSE filesystem implementation (runs in worker subprocess)
# ============================================================

if HAS_PYFUSE3:
    assert pyfuse3 is not None
    _fuse = pyfuse3
    OperationsBase = cast(Any, _fuse.Operations)

    @dataclass
    class _InodeInfo:
        ino: int
        name: str  # basename
        parent: int  # parent inode (0 for root)
        is_dir: bool
        md5: str = ""
        size: int = 0
        overlay: bool = False
        deleted: bool = False

    class LazyDVCFS(OperationsBase):
        """pyfuse3 Operations for a lazily-loaded DVC directory."""

        def __init__(
            self,
            manifest: DVCManifest,
            s3_config: S3Config,
            cache_dir: Path,
        ):
            super().__init__()
            self._manifest = manifest
            self._s3_config = s3_config
            self._cache_dir = cache_dir
            self._overlay_dir = cache_dir / "overlay"
            self._file_cache_dir = cache_dir / "cache"
            self._download_sem = asyncio.Semaphore(8)

            # Inode bookkeeping
            self._inodes: dict[int, _InodeInfo] = {}
            self._children: dict[int, dict[str, int]] = {}  # parent → {name: ino}
            self._next_inode = _fuse.ROOT_INODE + 1

            # Open file handles
            self._open_files: dict[int, _InodeInfo] = {}
            self._next_fh = 1

            # Modification tracking
            self._modified: set[str] = set()
            self._deleted: set[str] = set()
            self._created: set[str] = set()

            self._build_tree()

        # ---- tree construction ----

        def _alloc_inode(self) -> int:
            ino = self._next_inode
            self._next_inode += 1
            return ino

        def _alloc_fh(self) -> int:
            fh = self._next_fh
            self._next_fh += 1
            return fh

        def _build_tree(self) -> None:
            root = _InodeInfo(ino=_fuse.ROOT_INODE, name="", parent=0, is_dir=True)
            self._inodes[root.ino] = root
            self._children[root.ino] = {}

            for entry in self._manifest.entries_list:
                parts = Path(entry.relpath).parts
                parent_ino = _fuse.ROOT_INODE

                for part in parts[:-1]:
                    children = self._children.setdefault(parent_ino, {})
                    if part in children:
                        parent_ino = children[part]
                    else:
                        ino = self._alloc_inode()
                        info = _InodeInfo(ino=ino, name=part, parent=parent_ino, is_dir=True)
                        self._inodes[ino] = info
                        self._children[ino] = {}
                        children[part] = ino
                        parent_ino = ino

                fname = parts[-1]
                children = self._children.setdefault(parent_ino, {})
                ino = self._alloc_inode()
                info = _InodeInfo(
                    ino=ino,
                    name=fname,
                    parent=parent_ino,
                    is_dir=False,
                    md5=entry.md5,
                    size=entry.size,
                )
                self._inodes[ino] = info
                children[fname] = ino

        def _get_relpath(self, ino: int) -> str:
            parts: list[str] = []
            cur = self._inodes[ino]
            while cur.parent != 0:
                parts.append(cur.name)
                cur = self._inodes[cur.parent]
            parts.reverse()
            return "/".join(parts)

        # ---- data access ----

        async def _fetch_data(self, info: _InodeInfo) -> bytes:
            relpath = self._get_relpath(info.ino)

            overlay_path = self._overlay_dir / relpath
            if overlay_path.exists():
                return await asyncio.to_thread(overlay_path.read_bytes)

            cache_path = self._file_cache_dir / relpath
            if cache_path.exists():
                return await asyncio.to_thread(cache_path.read_bytes)

            if info.md5:
                async with self._download_sem:
                    key = _dvc_file_key(self._s3_config, info.md5)
                    data = await asyncio.to_thread(_s3_download_bytes_sync, self._s3_config, key)
                    cache_path.parent.mkdir(parents=True, exist_ok=True)
                    await asyncio.to_thread(cache_path.write_bytes, data)
                    return data

            return b""

        # ---- helpers ----

        def _make_attrs(self, info: _InodeInfo) -> Any:
            attrs = _fuse.EntryAttributes()
            attrs.st_ino = info.ino
            attrs.generation = 0
            attrs.entry_timeout = 300
            attrs.attr_timeout = 300

            now_ns = int(time.time() * 1e9)
            attrs.st_atime_ns = now_ns
            attrs.st_mtime_ns = now_ns
            attrs.st_ctime_ns = now_ns

            if info.is_dir:
                attrs.st_mode = stat_mod.S_IFDIR | 0o755
                attrs.st_nlink = 2
                attrs.st_size = 4096
            else:
                attrs.st_mode = stat_mod.S_IFREG | 0o644
                attrs.st_nlink = 1
                if info.overlay:
                    relpath = self._get_relpath(info.ino)
                    overlay_path = self._overlay_dir / relpath
                    if overlay_path.exists():
                        attrs.st_size = overlay_path.stat().st_size
                    else:
                        attrs.st_size = info.size
                else:
                    attrs.st_size = info.size

            attrs.st_uid = 1000
            attrs.st_gid = 1000
            attrs.st_blksize = 4096
            attrs.st_blocks = (attrs.st_size + 511) // 512
            return attrs

        # ---- FUSE operations ----

        async def getattr(self, inode, ctx=None):
            if inode not in self._inodes:
                raise _fuse.FUSEError(errno.ENOENT)
            info = self._inodes[inode]
            if info.deleted:
                raise _fuse.FUSEError(errno.ENOENT)
            return self._make_attrs(info)

        async def lookup(self, parent_inode, name, ctx=None):
            name_str = name.decode() if isinstance(name, bytes) else name
            children = self._children.get(parent_inode, {})
            if name_str not in children:
                raise _fuse.FUSEError(errno.ENOENT)
            child_ino = children[name_str]
            info = self._inodes[child_ino]
            if info.deleted:
                raise _fuse.FUSEError(errno.ENOENT)
            return self._make_attrs(info)

        async def opendir(self, inode, ctx):
            if inode not in self._inodes or not self._inodes[inode].is_dir:
                raise _fuse.FUSEError(errno.ENOTDIR)
            return inode

        async def readdir(self, inode, off, token):
            children = self._children.get(inode, {})
            entries = [(name, cino) for name, cino in sorted(children.items()) if not self._inodes[cino].deleted]
            for i, (name, cino) in enumerate(entries[off:], off):
                attrs = self._make_attrs(self._inodes[cino])
                if not _fuse.readdir_reply(token, name.encode(), attrs, i + 1):
                    break

        async def open(self, inode, flags, ctx):
            if inode not in self._inodes:
                raise _fuse.FUSEError(errno.ENOENT)
            info = self._inodes[inode]
            if info.deleted:
                raise _fuse.FUSEError(errno.ENOENT)

            fh = self._alloc_fh()
            self._open_files[fh] = info

            fi = _fuse.FileInfo()
            fi.fh = fh
            fi.direct_io = True  # required: manifest may not have sizes
            fi.keep_cache = False
            return fi

        async def read(self, fh, off, size):
            if fh not in self._open_files:
                raise _fuse.FUSEError(errno.EBADF)
            data = await self._fetch_data(self._open_files[fh])
            return data[off : off + size]

        async def write(self, fh, off, buf):
            if fh not in self._open_files:
                raise _fuse.FUSEError(errno.EBADF)
            info = self._open_files[fh]
            relpath = self._get_relpath(info.ino)
            overlay_path = self._overlay_dir / relpath
            overlay_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy-on-write for manifest files
            if not overlay_path.exists() and info.md5:
                existing = await self._fetch_data(info)
                overlay_path.write_bytes(existing)

            if off == 0 and not overlay_path.exists():
                overlay_path.write_bytes(buf)
            else:
                mode = "r+b" if overlay_path.exists() else "wb"
                with open(overlay_path, mode) as f:
                    f.seek(off)
                    f.write(buf)

            info.overlay = True
            if relpath in self._manifest.entries_dict():
                self._modified.add(relpath)
            else:
                self._created.add(relpath)
            return len(buf)

        async def create(self, parent_inode, name, mode, flags, ctx):
            name_str = name.decode() if isinstance(name, bytes) else name

            ino = self._alloc_inode()
            info = _InodeInfo(ino=ino, name=name_str, parent=parent_inode, is_dir=False, overlay=True)
            self._inodes[ino] = info
            children = self._children.setdefault(parent_inode, {})
            children[name_str] = ino

            relpath = self._get_relpath(ino)
            overlay_path = self._overlay_dir / relpath
            overlay_path.parent.mkdir(parents=True, exist_ok=True)
            overlay_path.touch()
            self._created.add(relpath)

            fh = self._alloc_fh()
            self._open_files[fh] = info

            fi = _fuse.FileInfo()
            fi.fh = fh
            fi.direct_io = True
            fi.keep_cache = False
            return (fi, self._make_attrs(info))

        async def unlink(self, parent_inode, name, ctx):
            name_str = name.decode() if isinstance(name, bytes) else name
            children = self._children.get(parent_inode, {})
            if name_str not in children:
                raise _fuse.FUSEError(errno.ENOENT)

            ino = children[name_str]
            info = self._inodes[ino]
            info.deleted = True
            relpath = self._get_relpath(ino)
            self._deleted.add(relpath)

            overlay_path = self._overlay_dir / relpath
            if overlay_path.exists():
                overlay_path.unlink()

        async def mkdir(self, parent_inode, name, mode, ctx):
            name_str = name.decode() if isinstance(name, bytes) else name
            ino = self._alloc_inode()
            info = _InodeInfo(ino=ino, name=name_str, parent=parent_inode, is_dir=True)
            self._inodes[ino] = info
            self._children[ino] = {}
            children = self._children.setdefault(parent_inode, {})
            children[name_str] = ino
            return self._make_attrs(info)

        async def setattr(self, inode, attr, fields, fh, ctx):
            if fields.update_size:
                info = self._inodes.get(inode)
                if info and not info.is_dir:
                    relpath = self._get_relpath(info.ino)
                    overlay_path = self._overlay_dir / relpath
                    overlay_path.parent.mkdir(parents=True, exist_ok=True)

                    if not overlay_path.exists():
                        if info.md5:
                            data = await self._fetch_data(info)
                            overlay_path.write_bytes(data)
                        else:
                            overlay_path.touch()

                    with open(overlay_path, "r+b") as f:
                        f.truncate(attr.st_size)

                    info.overlay = True
                    info.size = attr.st_size
                    if relpath in self._manifest.entries_dict():
                        self._modified.add(relpath)
                    else:
                        self._created.add(relpath)

            return await self.getattr(inode)

        async def release(self, fh):
            self._open_files.pop(fh, None)

        async def releasedir(self, fh):
            pass

        async def statfs(self, ctx):
            s = _fuse.StatvfsData()
            s.f_bsize = 4096
            s.f_frsize = 4096
            s.f_blocks = 1024 * 1024
            s.f_bfree = 512 * 1024
            s.f_bavail = 512 * 1024
            s.f_files = len(self._inodes)
            s.f_ffree = 1_000_000
            s.f_favail = 1_000_000
            s.f_namemax = 255
            return s

        def write_metadata(self) -> None:
            """Persist modification info for ``smart_commit()``."""
            meta = {
                "modified": sorted(self._modified),
                "deleted": sorted(self._deleted),
                "created": sorted(self._created),
            }
            (self._cache_dir / "meta.json").write_text(json.dumps(meta))


# ============================================================
# Worker entry point — run as:  python -m plato.worlds.lazy_dvc <config>
# ============================================================


def _worker_main(config_path: str) -> None:
    """FUSE worker process."""
    import pyfuse3

    try:
        import pyfuse3.asyncio as _pa
    except (ImportError, AttributeError):
        import pyfuse3_asyncio as _pa

    _pa.enable()

    config = json.loads(Path(config_path).read_text())
    manifest = DVCManifest.from_dict(config["manifest"])
    s3_config = S3Config.from_dict(config["s3_config"])
    mountpoint = config["mountpoint"]
    cache_dir = Path(config["cache_dir"])

    ops = LazyDVCFS(manifest, s3_config, cache_dir)

    fuse_options = set(pyfuse3.default_options)
    fuse_options.add("fsname=lazydvc")
    fuse_options.add("allow_other")

    pyfuse3.init(ops, mountpoint, fuse_options)

    async def _run() -> None:
        try:
            await pyfuse3.main()
        finally:
            ops.write_metadata()
            try:
                pyfuse3.close()
            except Exception:
                pass

    asyncio.run(_run())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <config_path>", file=sys.stderr)
        sys.exit(1)
    _worker_main(sys.argv[1])
