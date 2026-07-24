"""Workspace: a directory with S3 versioning and agent-mountable transport.

The workspace path is always writable — agents write to it via NFS.
Versioning (tracked=True) uses FUSE overlay + S3 for data storage, with Chronos
tracking refs/metadata.
"""

from __future__ import annotations

import asyncio
import gzip
import json
import logging
import os
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx

from plato.agents.mounts import AgentWorkspaceMount
from plato.chronos.api.workspace_repos import bulk_ingest_ref_audit_events
from plato.chronos.models import AuditEventInput, BulkRefAuditEventsRequest
from plato.runtimes.base import RuntimeInfo
from plato.transports.base import Transport
from plato.transports.fuse import FuseDirectTransport
from plato.transports.nfs import NFSTransport
from plato.transports.rsync import RsyncTransport
from plato.transports.sshfs import SSHFSTransport
from plato.utils.audit import read_audit_records
from plato.utils.subprocess import run_local
from plato.worlds.dvc_models import S3Config, credential_refresh_config

logger = logging.getLogger(__name__)

_CHRONOS_REQUEST_MAX_ATTEMPTS = 4
_CHRONOS_REQUEST_CONNECT_TIMEOUT_SECONDS = 10.0
_CHRONOS_REQUEST_TIMEOUT_SECONDS = 30.0
_CHRONOS_REQUEST_INITIAL_BACKOFF_SECONDS = 0.5
_CHRONOS_REQUEST_MAX_BACKOFF_SECONDS = 4.0
_CHRONOS_TRANSIENT_EXCEPTIONS = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadError,
    httpx.ReadTimeout,
)


class Workspace:
    """A workspace directory backed by FUSE overlay + S3.

    Agents see this as a plain writable directory via NFS. The world uses
    commit/restore for versioning between steps.
    """

    def __init__(
        self,
        name: str,
        path: Path,
        *,
        tracked: bool = True,
        mount_path: str | None = None,
        dvcignore: list[str] | None = None,
        s3_bucket: str = "",
        s3_prefix: str = "",
        repo_id: str = "",
        repo_name: str = "",
        chronos_url: str = "",
        api_key: str = "",
        session_id: str = "",
        commit_strategy: str = "manifest",
    ):
        self._repo_root = path
        self.path = path / "data" if tracked else path
        self.name = name
        self.tracked = tracked
        self._mount_path = mount_path
        self._custom_dvcignore = dvcignore or []
        self.s3_bucket = s3_bucket
        self.s3_prefix = s3_prefix
        self.repo_id = repo_id
        self.repo_name = repo_name
        self.chronos_url = chronos_url
        self.api_key = api_key
        self.session_id = session_id
        self.commit_strategy = commit_strategy
        self._transport: Transport | None = None
        self._sts_credentials: dict[str, str] = {}
        self._sts_expires_at: float = 0
        self._sts_credentials_expires_at: int | None = None
        self._last_ref_step: str = ""
        self._last_changed_ref_step: str = ""
        self._lazy_mounts: dict[str, Any] = {}
        self._commit_lock = asyncio.Lock()
        # Gzipped agent-VM fuse worker configs, keyed by (manifest_md5,
        # credentials expiry, mountpoint, cache_dir, manifest_by_ref): the
        # manifest JSON for a large dataset is ~100 MB, so serialize+gzip once
        # per credential window instead of once per agent VM. The by-ref flag
        # keys the config SHAPE so mixed fleets (old + new binaries) each get
        # the right one.
        self._fuse_agent_config_cache: dict[tuple[str, int | None, str, str, bool], bytes] = {}
        # Singleflight for build_agent_fuse_config: a large-fan-out mount has
        # every agent VM request the config near-simultaneously; without the
        # lock each caller misses the cache and serializes+gzips the ~100 MB
        # manifest independently (and a slow builder holding stale credentials
        # could evict a fresher cached entry when it finished last).
        self._fuse_agent_config_lock = asyncio.Lock()
        # Fresh STS credentials for the SOURCE repo of a cross-repo restored
        # mount, keyed by repo_id: (credentials, expires_at_epoch).
        self._agent_fuse_source_creds: dict[str, tuple[dict[str, str], int]] = {}

    @property
    def repo_path(self) -> Path:
        """For git-backed workspaces, returns the git working tree path. Falls back to self.path."""
        if self._transport is not None:
            from plato.transports.git import GitTransport

            if isinstance(self._transport, GitTransport):
                return Path(self._transport.repo_path)
        return self.path

    @property
    def mount_path(self) -> str:
        if self._mount_path is not None:
            return self._mount_path
        return str(self.path)

    @property
    def root_path(self) -> Path:
        """Root directory for workspace metadata and transport state."""
        return self._repo_root

    @property
    def transport(self) -> Transport | None:
        return self._transport

    @transport.setter
    def transport(self, value: Transport | None) -> None:
        self._transport = value

    def clone(self) -> Workspace:
        """Return a shallow copy of this workspace without copying the transport."""
        return Workspace(
            name=self.name,
            path=self._repo_root,
            tracked=self.tracked,
            mount_path=self._mount_path,
            dvcignore=list(self._custom_dvcignore),
            s3_bucket=self.s3_bucket,
            s3_prefix=self.s3_prefix,
            repo_id=self.repo_id,
            repo_name=self.repo_name,
            chronos_url=self.chronos_url,
            api_key=self.api_key,
            session_id=self.session_id,
            commit_strategy=self.commit_strategy,
        )

    def mount(
        self,
        *,
        agent_path: str | None = None,
    ) -> AgentWorkspaceMount:
        """Build an explicit per-agent mount for this workspace."""
        mount = AgentWorkspaceMount.from_workspace(self)
        if agent_path is not None:
            mount = mount.with_agent_path(agent_path)
        return mount

    @staticmethod
    def _cleanup_stale_mount(path: Path) -> None:
        """Unmount a leftover FUSE mount (dead or live) at ``path``.

        Two flavors of staleness:
        - dead mount: the owning FUSE process is gone, ``stat`` raises
          ENOTCONN ("Transport endpoint is not connected");
        - live mount: a previous world process exited without unmounting
          (e.g. a ``chronos dev`` hot-reload restart) and the lazydvc FUSE
          daemon is still serving it. ``stat`` succeeds, but the restore
          that follows must replace the directory wholesale —
          ``shutil.rmtree`` on a mountpoint fails with EBUSY ("Device or
          resource busy"). Unmount it first; the caller re-creates the dir.
        """
        import subprocess

        stale = False
        try:
            path.stat()
        except FileNotFoundError:
            return
        except OSError as e:
            if e.errno == 107:  # ENOTCONN — dead FUSE mount
                stale = True
        if not stale and os.path.ismount(path):
            stale = True
        if not stale:
            return

        logger.warning("Cleaning up stale FUSE mount at %s", path)
        # Use lazy unmount to detach immediately even if busy
        subprocess.run(["fusermount3", "-uz", str(path)], check=False)
        # Remove the stale mount point so mkdir can recreate it
        try:
            path.rmdir()
        except OSError:
            pass

    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------

    async def init(self) -> None:
        """Initialize workspace directory. Idempotent."""
        from plato.markers import WorkspaceMarker

        self._repo_root.mkdir(parents=True, exist_ok=True)

        if not self.tracked:
            return

        await self._ensure_credentials()
        self._cleanup_stale_mount(self.path)
        self.path.mkdir(parents=True, exist_ok=True)
        all_entries = list(WorkspaceMarker.DEFAULT_DVCIGNORE) + self._custom_dvcignore
        self.add_dvcignore(all_entries)

    def add_dvcignore(self, entries: list[str]) -> None:
        """Append entries to .dvcignore at the workspace root (idempotent)."""
        dvcignore_path = self._repo_root / ".dvcignore"
        if dvcignore_path.exists():
            existing = [line.strip() for line in dvcignore_path.read_text().splitlines() if line.strip()]
        else:
            existing = []
        seen = set(existing)
        for entry in entries:
            if entry not in seen:
                existing.append(entry)
                seen.add(entry)
        dvcignore_path.write_text("\n".join(existing) + "\n")

    async def setup_transport(
        self,
        runtime_info: RuntimeInfo,
        *,
        transport_mode: str = "nfs_kernel",
        marker_transport: str | None = None,
        git_config: Any = None,
        nfs_server: NFSTransport | None = None,
        export_fsid: int = 0,
        readonly: bool = False,
    ) -> NFSTransport | None:
        """Create and initialize the transport for this workspace.

        Args:
            runtime_info: The world's runtime environment info.
            transport_mode: Default transport mode ("nfs_kernel" or "sshfs").
            marker_transport: Per-workspace transport override from WorkspaceMarker.
            git_config: GitTransportConfig for git workspaces.
            nfs_server: Existing NFS server to share (for multi-workspace NFS).
                If None and mode is NFS, a new server is created and returned.
            export_fsid: FSID for NFS export (0 for first workspace).

        Returns:
            The NFS server transport if one was created (so caller can pass
            it to subsequent workspaces), or None.
        """
        hostname = runtime_info.hostname
        ssh_key = runtime_info.ssh_key_path
        if not hostname or not ssh_key:
            logger.debug("Workspace '%s': no hostname/ssh_key in runtime_info, skipping transport", self.name)
            return nfs_server

        effective_mode = marker_transport or transport_mode

        if readonly and effective_mode not in ("nfs_kernel", "fuse"):
            raise ValueError(
                f"Workspace '{self.name}': readonly=True is only supported for the NFS and fuse "
                f"transports, got transport '{effective_mode}'"
            )

        if effective_mode == "fuse":
            # Direct per-agent-VM plato-fuse mount of this workspace's
            # immutable manifest. Read-only datasets only: per-agent mounts
            # have no cross-VM coherence, so a writable fuse workspace would
            # silently fork state per agent.
            if not self.tracked:
                raise ValueError(
                    f"Workspace '{self.name}': the fuse transport requires a tracked workspace "
                    "(the agent VM mounts the committed manifest)"
                )
            if not readonly:
                raise ValueError(
                    f"Workspace '{self.name}': the fuse transport is read-only — per-agent "
                    "mounts have no cross-VM coherence. Use NFS/git/rsync for writable workspaces."
                )
            t = FuseDirectTransport(
                str(self.path),
                ssh_key,
                self.build_agent_fuse_config,
                mount_path=self.mount_path,
                workspace_name=self.name,
                readonly=True,
            )
            await t.initialize()
            self.transport = t
            return nfs_server

        if effective_mode == "git":
            from plato.transports.git import GitTransport

            t = GitTransport(str(self.path), hostname, ssh_key, git_config=git_config)
            await t.initialize()
            t.mount_path = self.mount_path
            self.transport = t
            return nfs_server

        if effective_mode == "sshfs":
            t = SSHFSTransport(str(self.path), hostname, ssh_key)
            await t.initialize()
            t.mount_path = self.mount_path
            self.transport = t
            return nfs_server

        if effective_mode == "rsync":
            t = RsyncTransport(str(self.path), ssh_key, mount_path=self.mount_path)
            await t.initialize()
            self.transport = t
            return nfs_server

        # NFS mode — share a single server across workspaces
        if nfs_server is None:
            nfs_server = NFSTransport(str(self.path), hostname, ssh_key, readonly=readonly)
            await nfs_server.initialize()
        else:
            await nfs_server.add_export(str(self.path), fsid=export_fsid, readonly=readonly)

        t = nfs_server.with_path(str(self.path), readonly=readonly)
        t.mount_path = self.mount_path
        self.transport = t
        return nfs_server

    async def ensure_fuse_mount(self) -> None:
        """Mount FUSE overlay. Skips if already mounted."""
        if self._lazy_mounts:
            return

        from plato.worlds.dvc_models import DVCManifest
        from plato.worlds.lazy_dvc import mount_lazy

        if self.tracked:
            await self._ensure_credentials()
            s3_config = self._s3_config()
        else:
            s3_config = S3Config(bucket="", prefix="", credentials={})

        empty_manifest = DVCManifest(entries_list=[], manifest_md5="")
        dir_name = self.path.name
        cache_dir = Path("/tmp/plato-lazy-cache") / self.name / dir_name
        cache_dir.mkdir(parents=True, exist_ok=True)
        self.path.mkdir(parents=True, exist_ok=True)

        # Move existing files into overlay dir so they're visible through FUSE
        overlay_dir = cache_dir / "overlay"
        overlay_dir.mkdir(parents=True, exist_ok=True)
        contents = list(self.path.iterdir())
        if contents:
            logger.debug("Moving %d items from %s into FUSE overlay", len(contents), self.path)
            for item in contents:
                dest = overlay_dir / item.name
                try:
                    os.rename(str(item), str(dest))
                except OSError:
                    # Cross-device rename — fall back to copy + remove
                    import shutil

                    if item.is_dir():
                        shutil.copytree(str(item), str(dest), dirs_exist_ok=True)
                        shutil.rmtree(str(item))
                    else:
                        shutil.copy2(str(item), str(dest))
                        item.unlink()

        mount = await mount_lazy(self.path, empty_manifest, s3_config, cache_dir)
        self._lazy_mounts[dir_name] = mount
        logger.debug("Mounted FUSE at %s", self.path)

    async def materialize_current_tree_into_overlay(self) -> None:
        """Mirror the current mounted tree into the overlay so smart_commit sees git-applied changes."""
        self._require_tracked()
        if not self._lazy_mounts:
            raise RuntimeError(
                f"Workspace '{self.name}' has no FUSE mounts. ensure_fuse_mount() must be called before materializing."
            )

        for mount in self._lazy_mounts.values():
            overlay_dir = mount.overlay_dir
            mountpoint = mount.mountpoint
            overlay_dir.mkdir(parents=True, exist_ok=True)
            exit_code, _, stderr = await run_local(
                " ".join(
                    [
                        "rsync",
                        "-a",
                        "--delete",
                        "--exclude=.git",
                        f"{mountpoint}/",
                        f"{overlay_dir}/",
                    ]
                ),
                timeout=120,
            )
            if exit_code != 0:
                raise RuntimeError(
                    f"Failed to materialize tracked workspace '{self.name}' into overlay: {stderr.strip()}"
                )

    # ------------------------------------------------------------------
    # Commit
    # ------------------------------------------------------------------

    async def commit(self, step_name: str, message: str = "", *, trigger_span_id: str = "") -> str:
        """Snapshot current workspace to S3 via smart commit."""
        logger.info(
            "Checkpoint workspace '%s' at '%s'",
            self.name,
            step_name,
            extra={
                "otel_attributes": {
                    # Discriminator for consumers is `plato.checkpoint.workspace`,
                    # not a sibling `plato.checkpoint=true` boolean — the two
                    # collide in nested-JSON stores (e.g. ClickHouse splits at
                    # dots, then orjson dedupes the duplicate `checkpoint` keys
                    # and the boolean is lost).
                    "plato.checkpoint.workspace": self.name,
                    "plato.checkpoint.label": step_name,
                }
            },
        )
        async with self._commit_lock:
            return await self._commit_inner(step_name, message, trigger_span_id=trigger_span_id)

    async def _snapshot_git_transport(self) -> None:
        """Pack + mirror the git bare into the FUSE mount before snapshotting.

        For git-transport workspaces the active object store lives off FUSE on
        local disk; this writes a packed snapshot into ``{path}/.git-bare`` so
        the workspace checkpoint persists it. No-op for other transports.
        """
        from plato.transports.git import GitTransport

        if isinstance(self._transport, GitTransport):
            await self._transport.snapshot_to_mirror()

    async def _commit_inner(self, step_name: str, message: str = "", *, trigger_span_id: str = "") -> str:
        await self._snapshot_git_transport()

        if self.commit_strategy == "archive":
            return await self._archive_commit(step_name, message, trigger_span_id=trigger_span_id)

        if not self._lazy_mounts:
            raise RuntimeError(
                f"Workspace '{self.name}' has no FUSE mounts. ensure_fuse_mount() must be called before commit()."
            )

        has_changes = any(
            any(mount.overlay_dir.iterdir()) if mount.overlay_dir.exists() else False
            for mount in self._lazy_mounts.values()
        )
        if not has_changes:
            logger.debug("Workspace '%s': no changes at '%s', skipping commit", self.name, step_name)
            dvc_files = self._collect_dvc_files(list(self._lazy_mounts.keys()))
            if dvc_files:
                await self._ensure_credentials()
                try:
                    await self._validate_dvc_files_restorable(dvc_files)
                except Exception as e:
                    logger.warning("Workspace '%s': ref validation failed (no changes): %s", self.name, e)
            return json.dumps({"step": step_name, "changed": False})
        return await self._smart_commit(step_name, message, trigger_span_id=trigger_span_id)

    def _collect_dvc_files(self, dir_names: list[str] | None = None) -> dict[str, str]:
        """Collect .dvc file contents keyed by tracked directory name."""
        dvc_files: dict[str, str] = {}
        if dir_names:
            for dir_name in dir_names:
                dvc_path = self._repo_root / f"{dir_name}.dvc"
                if dvc_path.exists():
                    dvc_files[dir_name] = dvc_path.read_text()
            if dvc_files:
                return dvc_files
        for dvc_path in sorted(self._repo_root.glob("*.dvc")):
            if not dvc_path.is_file():
                continue
            dvc_files[dvc_path.stem] = dvc_path.read_text()
        return dvc_files

    async def _validate_dvc_files_restorable(self, dvc_files: dict[str, str]) -> None:
        """Validate that all manifests referenced by .dvc files exist in S3."""
        if not dvc_files or not self.s3_bucket:
            return

        from plato.worlds.dvc_models import DVCManifest

        await self._ensure_credentials()
        s3_config = self._s3_config()
        for dir_name, dvc_content in dvc_files.items():
            try:
                await DVCManifest.from_dvc_file(dvc_content, s3_config)
            except Exception as e:
                raise RuntimeError(
                    f"Workspace '{self.name}' manifest for '{dir_name}' not restorable (repo={self.repo_name}): {e}"
                ) from e

    # ------------------------------------------------------------------
    # Restore
    # ------------------------------------------------------------------

    async def restore(self, step_name: str, session_id: str | None = None) -> bool:
        """Restore workspace from S3.

        Automatically detects format per directory: archive refs are extracted
        directly, manifest refs are lazy-mounted via FUSE. Returns True when at
        least one tracked directory was restored.
        """
        from plato.worlds.dvc_models import DVCManifest, parse_dvc_format, restore_archive
        from plato.worlds.lazy_dvc import mount_lazy

        self._require_tracked()
        await self._ensure_credentials()

        ref = await self._fetch_workspace_ref(step_name, session_id=session_id)
        if not ref:
            raise RuntimeError(f"No workspace ref found for step '{step_name}'")
        self._last_restored_source_ref_public_id = ref.get("ref_public_id", "")

        dvc_files = ref.get("dvc_files", {})
        self._last_restored_dvc_files = dvc_files
        if not dvc_files:
            logger.debug("Workspace '%s' step '%s' has no DVC files", self.name, step_name)
            self._last_ref_step = step_name
            return True

        s3_config = self._s3_config()

        for dir_name, dvc_content in dvc_files.items():
            fmt = parse_dvc_format(dvc_content)

            if fmt == "archive":
                target_dir = self._repo_root / dir_name
                self._cleanup_stale_mount(target_dir)
                target_dir.mkdir(parents=True, exist_ok=True)
                await restore_archive(dvc_content, s3_config, target_dir)
                dvc_path = self._repo_root / f"{dir_name}.dvc"
                dvc_path.write_text(dvc_content)
            else:
                try:
                    manifest = await DVCManifest.from_dvc_file(dvc_content, s3_config)
                except Exception as e:
                    raise RuntimeError(
                        f"Failed to restore workspace '{self.name}' at step '{step_name}' "
                        f"(repo={self.repo_name}, dir={dir_name}): {e}"
                    ) from e
                mountpoint = self._repo_root / dir_name
                self._cleanup_stale_mount(mountpoint)
                mountpoint.mkdir(parents=True, exist_ok=True)
                cache_dir = Path("/tmp/plato-lazy-cache") / self.name / dir_name
                cache_dir.mkdir(parents=True, exist_ok=True)
                mount = await mount_lazy(mountpoint, manifest, s3_config, cache_dir)
                self._lazy_mounts[dir_name] = mount

                dvc_path = self._repo_root / f"{dir_name}.dvc"
                dvc_path.write_text(dvc_content)

        logger.debug("Restored workspace '%s' step '%s': %d dir(s)", self.name, step_name, len(dvc_files))
        self._last_ref_step = step_name
        return True

    async def _smart_commit(self, step_name: str, message: str = "", *, trigger_span_id: str = "") -> str:
        """Commit with smart diff — only upload changed files."""
        from plato.worlds.dvc_models import smart_commit

        self._require_tracked()
        await self._ensure_credentials()

        s3_config = self._s3_config()

        dvcignore_path = self._repo_root / ".dvcignore"
        ignore_patterns: list[str] = []
        if dvcignore_path.exists():
            ignore_patterns = [
                line.strip()
                for line in dvcignore_path.read_text().splitlines()
                if line.strip() and not line.strip().startswith("#")
            ]

        dvc_files: dict[str, str] = {}
        for dir_name, mount in list(self._lazy_mounts.items()):
            manifest_md5, dvc_yaml = await smart_commit(
                mount, s3_config, dir_name=dir_name, ignore_patterns=ignore_patterns
            )
            dvc_path = self._repo_root / f"{dir_name}.dvc"
            dvc_path.write_text(dvc_yaml)
            dvc_files[dir_name] = dvc_yaml

        await self._validate_dvc_files_restorable(dvc_files)
        ref_public_id = await self._record_workspace_ref(
            step_name, "output", dvc_files, changed=True, trigger_span_id=trigger_span_id
        )
        await self._upload_audit_events(step_name, ref_public_id)

        return json.dumps({"step": step_name, "dvc_files": list(dvc_files.keys())})

    async def _archive_commit(self, step_name: str, message: str = "", *, trigger_span_id: str = "") -> str:
        """Commit workspace as a single tar.gz archive to S3."""
        from plato.worlds.dvc_models import smart_commit_archive

        self._require_tracked()
        await self._ensure_credentials()

        s3_config = self._s3_config()

        dvcignore_path = self._repo_root / ".dvcignore"
        ignore_patterns: list[str] = []
        if dvcignore_path.exists():
            ignore_patterns = [
                line.strip()
                for line in dvcignore_path.read_text().splitlines()
                if line.strip() and not line.strip().startswith("#")
            ]

        dvc_files: dict[str, str] = {}
        # Archive commits operate on the workspace data directories directly.
        # If we have FUSE mounts, use their mountpoints; otherwise use self.path.
        if self._lazy_mounts:
            for dir_name, mount in list(self._lazy_mounts.items()):
                _, dvc_yaml = await smart_commit_archive(
                    mount.mountpoint, s3_config, dir_name=dir_name, ignore_patterns=ignore_patterns
                )
                dvc_path = self._repo_root / f"{dir_name}.dvc"
                dvc_path.write_text(dvc_yaml)
                dvc_files[dir_name] = dvc_yaml
        else:
            dir_name = "data"
            source_dir = self._repo_root / dir_name
            _, dvc_yaml = await smart_commit_archive(
                source_dir, s3_config, dir_name=dir_name, ignore_patterns=ignore_patterns
            )
            dvc_path = self._repo_root / f"{dir_name}.dvc"
            dvc_path.write_text(dvc_yaml)
            dvc_files[dir_name] = dvc_yaml

        ref_public_id = await self._record_workspace_ref(
            step_name, "output", dvc_files, changed=True, trigger_span_id=trigger_span_id
        )
        await self._upload_audit_events(step_name, ref_public_id)

        return json.dumps({"step": step_name, "dvc_files": list(dvc_files.keys())})

    async def to_state_dict(self) -> dict[str, Any]:
        """Snapshot workspace metadata for state persistence."""
        restore_step = self._last_changed_ref_step or self._last_ref_step
        return {
            "name": self.name,
            "path": str(self._repo_root),
            "tracked": self.tracked,
            "repo_name": self.repo_name,
            "s3_bucket": self.s3_bucket,
            "s3_prefix": self.s3_prefix,
            "session_id": self.session_id,
            "steps": [restore_step] if restore_step else [],
        }

    # ------------------------------------------------------------------
    # Chronos integration
    # ------------------------------------------------------------------

    async def _chronos_request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        timeout = httpx.Timeout(
            _CHRONOS_REQUEST_TIMEOUT_SECONDS,
            connect=_CHRONOS_REQUEST_CONNECT_TIMEOUT_SECONDS,
        )
        url = f"{self.chronos_url}{path}"
        for attempt in range(1, _CHRONOS_REQUEST_MAX_ATTEMPTS + 1):
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    resp = await client.request(
                        method,
                        url,
                        headers={"X-API-Key": self.api_key},
                        **kwargs,
                    )
                    resp.raise_for_status()
                    return resp
            except _CHRONOS_TRANSIENT_EXCEPTIONS:
                if attempt == _CHRONOS_REQUEST_MAX_ATTEMPTS:
                    raise
                backoff = min(
                    _CHRONOS_REQUEST_INITIAL_BACKOFF_SECONDS * (2 ** (attempt - 1)),
                    _CHRONOS_REQUEST_MAX_BACKOFF_SECONDS,
                )
                delay = backoff + random.uniform(0, backoff * 0.25)
                logger.warning(
                    "Transient Chronos request failure for %s %s; retrying attempt %s/%s in %.2fs",
                    method,
                    path,
                    attempt + 1,
                    _CHRONOS_REQUEST_MAX_ATTEMPTS,
                    delay,
                    exc_info=True,
                )
                await asyncio.sleep(delay)

        raise RuntimeError("unreachable Chronos request retry state")

    async def _record_workspace_ref(
        self,
        step_name: str,
        direction: str,
        dvc_files: dict[str, str],
        *,
        source_ref_public_id: str | None = None,
        source_session_public_id: str | None = None,
        source_repo_name: str | None = None,
        source_step_name: str | None = None,
        changed: bool | None = None,
        trigger_span_id: str = "",
    ) -> str | None:
        """Record a workspace ref with Chronos. Returns the ref public_id if available."""
        if not self.chronos_url or not self.repo_name or not self.session_id:
            return None
        has_source_ref = bool(source_ref_public_id)
        has_source_parts = any((source_session_public_id, source_repo_name, source_step_name))
        if has_source_ref and has_source_parts:
            raise ValueError("Provide either source_ref_public_id or source_session/repo/step, not both")
        if has_source_parts and not (source_session_public_id and source_repo_name and source_step_name):
            raise ValueError(
                "source_session_public_id, source_repo_name, and source_step_name must be provided together"
            )
        payload: dict[str, Any] = {
            "repo_name": self.repo_name,
            "step_name": step_name,
            "direction": direction,
            "dvc_files": dvc_files,
            "changed": changed,
            # Uploaded by the world runtime during a session (vs "manual" CLI).
            "upload_mode": "runtime",
        }
        if trigger_span_id:
            payload["trigger_span_id"] = trigger_span_id
        if has_source_ref:
            payload["source_ref_public_id"] = source_ref_public_id
        elif has_source_parts:
            payload["source_session_public_id"] = source_session_public_id
            payload["source_repo_name"] = source_repo_name
            payload["source_step_name"] = source_step_name
        resp = await self._chronos_request(
            "POST",
            f"/api/workspace-repos/sessions/{self.session_id}/workspace-refs",
            json=payload,
        )
        self._last_ref_step = step_name
        if changed is True:
            self._last_changed_ref_step = step_name

        # Extract ref public_id from response if available
        try:
            resp_data = resp.json()
            return resp_data.get("public_id") or resp_data.get("ref_public_id")
        except Exception:
            return None

    async def _fetch_workspace_ref(self, step_name: str, session_id: str | None = None) -> dict[str, Any] | None:
        """Fetch a specific workspace ref from Chronos.

        NOTE: The Chronos API returns refs from ALL repos in the session,
        so we must filter by repo_name client-side.
        """
        sid = session_id or self.session_id
        if not self.chronos_url or not self.repo_name or not sid:
            return None
        resp = await self._chronos_request(
            "GET",
            f"/api/workspace-repos/sessions/{sid}/workspace-refs",
            params={"step_name": step_name, "repo_name": self.repo_name},
        )
        refs = resp.json().get("refs", [])
        # Filter by repo_name — the API ignores this param
        for ref in reversed(refs):
            if ref.get("step_name") == step_name and ref.get("repo_name") == self.repo_name:
                return ref
        return None

    async def _refresh_credentials(self) -> None:
        """Fetch STS credentials from Chronos scoped to this repo's S3 prefix."""
        if not self.chronos_url or not self.repo_id:
            return
        resp = await self._chronos_request(
            "POST",
            f"/api/workspace-repos/{self.repo_id}/credentials",
        )
        data = resp.json()
        self._sts_credentials = {
            "AWS_ACCESS_KEY_ID": data["aws_access_key_id"],
            "AWS_SECRET_ACCESS_KEY": data["aws_secret_access_key"],
            "AWS_SESSION_TOKEN": data["aws_session_token"],
            "AWS_DEFAULT_REGION": data.get("region", "us-east-1"),
        }
        expires_at = datetime.fromisoformat(data["expires_at"].replace("Z", "+00:00"))
        self._sts_credentials_expires_at = int(expires_at.timestamp())
        self._sts_expires_at = self._sts_credentials_expires_at - 300
        logger.debug("Refreshed STS credentials for repo '%s'", self.repo_name)

    def _aws_credentials(self) -> dict[str, str]:
        env = dict(os.environ)
        if self._sts_credentials:
            env.update(self._sts_credentials)
        return {k: v for k, v in env.items() if k.startswith("AWS_")}

    def _credential_refresh_config(self) -> dict[str, str | int] | None:
        if not (self.chronos_url and self.repo_id and self.api_key):
            return None
        return credential_refresh_config(self.chronos_url, self.repo_id, self.api_key)

    def _s3_config(self) -> S3Config:
        return S3Config(
            bucket=self.s3_bucket,
            prefix=self.s3_prefix,
            credentials=self._aws_credentials(),
            credentials_expires_at=self._sts_credentials_expires_at,
            credential_refresh=self._credential_refresh_config(),
        )

    async def _agent_fuse_s3_config_dict(self) -> dict[str, Any]:
        """S3 config dict for direct agent-VM fuse mounts of this workspace.

        Load-bearing for cross-repo restores: after ``restore()`` the
        workspace's own repo identity is swapped back in, but the mounted
        content's blobs live under the SOURCE repo's prefix — so the agent
        config must reuse the S3 config captured on the lazy mount (bucket,
        prefix, credential_refresh) with freshly fetched STS credentials for
        that source repo.
        """
        lazy_mount = self._lazy_mounts.get(self.path.name)
        source = lazy_mount.s3_config if lazy_mount is not None else None
        if source is None:
            await self._ensure_credentials()
            return self._s3_config().to_dict()

        refresh = source.credential_refresh
        if not refresh:
            # No Chronos-backed refresh (e.g. unit tests / untracked overlay
            # mounts): pass through the captured credentials as-is.
            return source.to_dict()

        repo_id = str(refresh["repo_id"])
        cached = self._agent_fuse_source_creds.get(repo_id)
        if cached is None or time.time() >= cached[1] - 300:
            resp = await self._chronos_request(
                "POST",
                f"/api/workspace-repos/{repo_id}/credentials",
            )
            data = resp.json()
            credentials = {
                "AWS_ACCESS_KEY_ID": data["aws_access_key_id"],
                "AWS_SECRET_ACCESS_KEY": data["aws_secret_access_key"],
                "AWS_SESSION_TOKEN": data["aws_session_token"],
                "AWS_DEFAULT_REGION": data.get("region", "us-east-1"),
            }
            expires_at = int(datetime.fromisoformat(data["expires_at"].replace("Z", "+00:00")).timestamp())
            cached = (credentials, expires_at)
            self._agent_fuse_source_creds[repo_id] = cached
            logger.debug("Refreshed agent-fuse STS credentials for source repo id '%s'", repo_id)

        return S3Config(
            bucket=source.bucket,
            prefix=source.prefix,
            credentials=cached[0],
            credentials_expires_at=cached[1],
            credential_refresh=refresh,
        ).to_dict()

    async def build_agent_fuse_config(self, mountpoint: str, cache_dir: str, manifest_by_ref: bool = False) -> bytes:
        """Gzipped plato-fuse worker config for a direct agent-VM mount.

        Same shape ``mount_lazy`` writes for the world-side mount — the
        restored manifest plus an :class:`S3Config` dict carrying STS
        credentials, ``credentials_expires_at``, and the ``credential_refresh``
        block (chronos_url/repo_id/api_key) so the agent-side fuse process can
        refresh its own credentials for long runs. Serves the committed
        manifest only: world-side overlay writes are NOT visible to agent VMs
        (datasets are read-only, so this only matters if someone mutates the
        workspace world-side — warned about below).

        With ``manifest_by_ref`` the manifest is sent as a content-hash
        reference (``manifest_ref``) instead of inline and the fuse worker
        fetches the blob from the S3 dvc-cache itself — shrinking the
        per-agent config push from ~30 MB gz to ~1 KB for large datasets.
        Only pass it after probing that the remote binary advertises the
        ``manifest-ref`` capability; empty manifests always go inline (there
        is no blob to reference).
        """
        self._require_tracked()

        dir_name = self.path.name
        lazy_mount = self._lazy_mounts.get(dir_name)
        manifest_ref_md5 = ""
        manifest_dict: dict[str, Any] | None = None
        manifest_md5 = ""
        if lazy_mount is not None:
            manifest_md5 = lazy_mount.manifest.manifest_md5
            if manifest_by_ref and manifest_md5:
                manifest_ref_md5 = manifest_md5
            else:
                # Inline fallback: serializing 835k entries costs seconds and
                # ~100 MB, so skip it entirely when sending by reference.
                manifest_dict = lazy_mount.manifest.to_dict()
            overlay_dir = lazy_mount.overlay_dir
            if overlay_dir.exists() and any(overlay_dir.iterdir()):
                logger.warning(
                    "Workspace '%s': world-side overlay changes exist but agent-VM fuse "
                    "mounts serve the committed manifest only — agents will not see them",
                    self.name,
                )
        elif self.path.exists() and any(self.path.iterdir()):
            # Archive-format restores extract files directly (no lazy manifest
            # mount), so there is no committed manifest to serve — a direct
            # agent-VM fuse mount would silently present an EMPTY dataset
            # (NFS, by contrast, exports the materialized directory). Fail
            # loudly at setup instead.
            raise RuntimeError(
                f"Workspace '{self.name}' has materialized files at {self.path} but no lazy "
                "manifest mount (archive-format restore) — a direct agent-VM fuse mount would "
                'serve an empty dataset. Use mount: "nfs" for this dataset, or re-commit its '
                "ref with the manifest strategy."
            )
        else:
            manifest_dict = {"entries": [], "manifest_md5": ""}

        # Singleflight: serialize builds so concurrent agent mounts share one
        # serialize+gzip pass, and the credential expiry that keys the cache
        # is always read at build time (a slower builder can never insert a
        # config from an older credential window over a fresher one).
        async with self._fuse_agent_config_lock:
            s3_config_dict = await self._agent_fuse_s3_config_dict()

            cache_key = (
                manifest_md5,
                s3_config_dict.get("credentials_expires_at"),
                mountpoint,
                cache_dir,
                bool(manifest_ref_md5),
            )
            cached_config = self._fuse_agent_config_cache.get(cache_key)
            if cached_config is not None:
                return cached_config

            def _serialize() -> bytes:
                payload: dict[str, Any] = {
                    "s3_config": s3_config_dict,
                    "mountpoint": mountpoint,
                    "cache_dir": cache_dir,
                }
                if manifest_ref_md5:
                    payload["manifest_ref"] = {"manifest_md5": manifest_ref_md5}
                else:
                    payload["manifest"] = (
                        manifest_dict if manifest_dict is not None else {"entries": [], "manifest_md5": ""}
                    )
                config_json = json.dumps(payload)
                # Fast compression: the manifest JSON is highly repetitive, so
                # level 1 already shrinks it ~5x and keeps setup latency low.
                return gzip.compress(config_json.encode(), compresslevel=1)

            config_gz = await asyncio.to_thread(_serialize)
            # Evict entries from previous credential windows / manifests; keep
            # sibling mountpoints of the current window (orchestrator + agents).
            for key in list(self._fuse_agent_config_cache):
                if key[0] != cache_key[0] or key[1] != cache_key[1]:
                    del self._fuse_agent_config_cache[key]
            self._fuse_agent_config_cache[cache_key] = config_gz
            return config_gz

    async def _ensure_credentials(self) -> None:
        if self.chronos_url and self.repo_id:
            if not self._sts_credentials or time.time() >= self._sts_expires_at:
                await self._refresh_credentials()

    def _audit_scope_dir(self) -> Path:
        return self._repo_root / ".plato" / "audit" / self.name

    def _audit_scope_files(self) -> list[Path]:
        audit_dir = self._audit_scope_dir()
        if not audit_dir.exists():
            return []
        return sorted(audit_dir.glob("*.jsonl"))

    def _read_audit_scope_events(self, paths: list[Path]) -> list[AuditEventInput]:
        events: list[AuditEventInput] = []
        for path in paths:
            try:
                records = read_audit_records(path)
                events.extend(record.to_audit_event_input() for record in records)
            except FileNotFoundError:
                continue
            except Exception as exc:
                logger.warning(
                    "Skipping invalid audit spool file %s: %s",
                    path,
                    exc,
                )
        return events

    async def _upload_audit_events(self, step_name: str, ref_public_id: str | None) -> None:
        """Upload audit events from local scoped JSONL spool files to Chronos."""
        try:
            if not self.chronos_url or not self.session_id or not self.tracked:
                return

            if not ref_public_id:
                logger.debug(
                    "Skipping audit upload for workspace '%s' at step '%s' because no committed ref_public_id was recorded",
                    self.name,
                    step_name,
                )
                return

            scope_files = self._audit_scope_files()
            if not scope_files:
                return

            events = await asyncio.to_thread(self._read_audit_scope_events, scope_files)
            if not events:
                logger.debug("No audit events to upload for step '%s'", step_name)
                for path in scope_files:
                    try:
                        path.unlink()
                    except OSError:
                        pass
                return

            # Transform paths from agent mount path to workspace-relative paths
            # so they match the file tree in workspace refs.
            # Agent sees: /workspace/input_a.txt (mount_path)
            # Workspace ref stores: /data/input_a.txt (relative to _repo_root)
            mount = self.mount_path.rstrip("/")
            repo_root = str(self._repo_root)
            ws_relative = str(self.path).removeprefix(repo_root)  # e.g. "/data"
            if mount:
                for event in events:
                    if event.path.startswith(mount):
                        event.path = ws_relative + event.path[len(mount) :]
                    if event.new_path and event.new_path.startswith(mount):
                        event.new_path = ws_relative + event.new_path[len(mount) :]

            # Upload in chunks of 500
            chunk_size = 500
            total_uploaded = 0
            async with httpx.AsyncClient(
                base_url=self.chronos_url,
                headers={"X-API-Key": self.api_key},
                timeout=30,
            ) as client:
                for i in range(0, len(events), chunk_size):
                    chunk = events[i : i + chunk_size]
                    payload = BulkRefAuditEventsRequest(events=chunk)
                    await bulk_ingest_ref_audit_events.asyncio(
                        client,
                        ref_public_id=ref_public_id,
                        body=payload,
                    )
                    total_uploaded += len(chunk)

            logger.debug("Uploaded %d audit events for step '%s'", total_uploaded, step_name)

            for path in scope_files:
                try:
                    path.unlink()
                except OSError:
                    pass
        except Exception:
            logger.warning("Failed to upload audit events for step '%s'", step_name, exc_info=True)

    def _require_tracked(self) -> None:
        if not self.tracked:
            raise RuntimeError(f"Workspace '{self.name}' is not tracked (tracked=False)")
