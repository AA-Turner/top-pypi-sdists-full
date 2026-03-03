"""Workspace: a directory with optional DVC versioning and agent-mountable transport.

The workspace path is always writable — agents write to it via NFS.
Versioning (tracked=True) uses DVC + S3 for data storage, with Chronos
tracking refs/metadata. Git exists only as local scaffolding required by DVC.

    workspace/              <- writable, agent sees via NFS
    workspace/.snapshots/
        capture/            <- read-only, lazy-loaded from S3 (world-side only)
        scrutinize/         <- read-only, lazy-loaded from S3 (world-side only)
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any

import httpx

if TYPE_CHECKING:
    from plato.agents.runtime.transport import Transport

logger = logging.getLogger(__name__)


class Workspace:
    """A workspace directory.

    Agents see this as a plain writable directory via NFS. The world uses
    commit/restore/snapshot for versioning between steps.

    Data flow on commit:
      1. dvc add <dirs>  — hashes data, writes .dvc pointer files
      2. dvc push         — uploads data to S3
      3. Chronos ref      — stores step name, .dvc file contents (for restore)

    Data flow on restore:
      1. Chronos ref      — fetches .dvc file contents for the target step
      2. Write .dvc files — reconstructs pointer files locally
      3. dvc pull          — downloads data from S3
    """

    def __init__(
        self,
        name: str,
        path: Path,
        *,
        tracked: bool = True,
        mount: str = "",
        backup: bool = True,
        s3_bucket: str = "",
        s3_prefix: str = "",
        repo_id: str = "",
        repo_name: str = "",
        chronos_url: str = "",
        api_key: str = "",
        session_id: str = "",
    ):
        self.name = name
        self.path = path
        self.tracked = tracked
        self.mount = mount or str(path)
        self.backup = backup
        self.s3_bucket = s3_bucket
        self.s3_prefix = s3_prefix
        self.repo_id = repo_id
        self.repo_name = repo_name
        self.chronos_url = chronos_url
        self.api_key = api_key
        self.session_id = session_id
        self.transport: Transport | None = None
        # STS credential cache
        self._sts_credentials: dict[str, str] = {}
        self._sts_expires_at: float = 0
        self._last_ref_step: str = ""
        self._last_changed_ref_step: str = ""

    @property
    def data_path(self) -> Path:
        """Path to the content directory (data/ for tracked workspaces, root otherwise)."""
        if self.tracked:
            p = self.path / "data"
            self._cleanup_stale_mount(p)
            p.mkdir(parents=True, exist_ok=True)
            return p
        return self.path

    @staticmethod
    def _cleanup_stale_mount(path: Path) -> None:
        """Unmount a stale FUSE mount if present."""
        try:
            path.stat()
        except OSError as e:
            if e.errno == 107:  # ENOTCONN — dead FUSE mount
                import subprocess

                logger.warning(f"Cleaning up stale FUSE mount at {path}")
                subprocess.run(["fusermount3", "-u", str(path)], check=False)
        except FileNotFoundError:
            pass

    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------

    async def init(self) -> None:
        """Initialize workspace directory and DVC repo if tracked.

        Idempotent — safe to call on restarts. Git exists only as local
        scaffolding that DVC requires; it never leaves the container.
        """
        self.path.mkdir(parents=True, exist_ok=True)

        if not self.tracked:
            return

        # NFS mount points confuse git/DVC repo discovery
        os.environ["GIT_DISCOVERY_ACROSS_FILESYSTEM"] = "1"

        # Ensure STS credentials are available before any S3 operations
        await self._ensure_credentials()

        # Already initialized — nothing to do
        if (self.path / ".dvc").exists():
            return

        # Fresh init — git is just scaffolding for DVC
        if not (self.path / ".git").is_dir():
            git_path = self.path / ".git"
            if git_path.exists():
                git_path.unlink()
            await _run("git", "init", cwd=self.path)

        await _run("git", "config", "--global", "--add", "safe.directory", str(self.path), cwd=self.path)
        await _run("git", "config", "user.email", "plato@plato.so", cwd=self.path)
        await _run("git", "config", "user.name", "plato", cwd=self.path)

        await _run("dvc", "init", cwd=self.path)
        if self.s3_bucket:
            await _run(
                "dvc",
                "remote",
                "add",
                "-d",
                "s3",
                f"s3://{self.s3_bucket}/{self.s3_prefix}/dvc-cache",
                cwd=self.path,
            )
        # Commit DVC scaffolding so dvc add/push work
        await _run("git", "add", ".", cwd=self.path)
        await _run("git", "commit", "-m", "init dvc", cwd=self.path)

    # ------------------------------------------------------------------
    # Commit
    # ------------------------------------------------------------------

    async def commit(self, step_name: str, message: str = "") -> str:
        """Snapshot current workspace to S3 via DVC. Returns DVC ref hash.

        1. dvc add on all data directories -> creates .dvc pointer files
        2. git commit the pointer files (local only, DVC requires this)
        3. dvc push -> uploads actual data to S3
        4. Records ref in Chronos with .dvc file contents for cross-container restore

        If this workspace was lazily restored, uses smart commit (only
        uploads changed files) instead of the full dvc add/push cycle.
        """
        if hasattr(self, "_lazy_mounts") and self._lazy_mounts:
            # Skip commit if the lazy mount has no modifications (overlay is empty)
            has_changes = any(
                any(mount.overlay_dir.iterdir()) if mount.overlay_dir.exists() else False
                for mount in self._lazy_mounts.values()
            )
            if not has_changes:
                logger.debug("Workspace '%s': lazy mount has no changes, skipping commit", self.name)
                # Still record a workspace ref so resume can find this step
                dir_names = list(self._lazy_mounts.keys())
                dvc_files = self._collect_dvc_files(dir_names)
                if dvc_files:
                    await self._ensure_credentials()
                    await self._validate_dvc_files_restorable(dvc_files)
                    await self._record_workspace_ref(step_name, "output", dvc_files, changed=False)
                return json.dumps({"step": step_name, "changed": False})
            return await self._smart_commit(step_name, message)

        self._require_tracked()
        await self._ensure_credentials()

        # Verify DVC repo exists (init must have run)
        dvc_dir = self.path / ".dvc"
        if not dvc_dir.is_dir():
            contents = [p.name for p in self.path.iterdir()]
            raise RuntimeError(
                f"DVC repo not found at {self.path}. Expected {dvc_dir} to be a directory. Contents: {contents}"
            )

        # DVC-track all non-hidden directories
        tracked_dirs: list[str] = []
        for child in sorted(self.path.iterdir()):
            if child.name.startswith(".") or child.name.endswith(".dvc") or child.name == ".gitignore":
                continue
            if child.is_dir() and any(child.iterdir()):
                await _run("dvc", "add", child.name, "--force", cwd=self.path)
                tracked_dirs.append(child.name)

        # Git commit pointer files if anything changed (local scaffolding, never pushed)
        await _run("git", "add", ".", cwd=self.path)
        status = (await _run("git", "status", "--porcelain", cwd=self.path)).stdout_text
        if not status.strip():
            logger.debug("Workspace '%s': no changes for step '%s', skipping", self.name, step_name)
            # Still record a workspace ref so resume can find this step
            dvc_files = self._collect_dvc_files(tracked_dirs if tracked_dirs else None)
            if dvc_files:
                try:
                    await self._validate_dvc_files_restorable(dvc_files)
                except Exception:
                    logger.warning(
                        "Workspace '%s': no-change checkpoint '%s' has missing DVC objects; "
                        "running dvc push before recording ref",
                        self.name,
                        step_name,
                    )
                    if self.s3_bucket:
                        await _run("dvc", "push", cwd=self.path, env=self._s3_env())
                    await self._validate_dvc_files_restorable(dvc_files)
                await self._record_workspace_ref(step_name, "output", dvc_files, changed=False)
            return json.dumps({"step": step_name, "changed": False})

        msg = message or f"step: {step_name}"
        await _run("git", "commit", "-m", msg, cwd=self.path)

        # Push actual data to S3
        if self.s3_bucket:
            await _run("dvc", "push", cwd=self.path, env=self._s3_env())

        # Collect .dvc file contents so Chronos can reconstruct on restore
        dvc_files = self._collect_dvc_files(tracked_dirs if tracked_dirs else None)
        await self._validate_dvc_files_restorable(dvc_files)

        # Register ref with Chronos (only when there were actual changes)
        await self._record_workspace_ref(step_name, "output", dvc_files, changed=True)

        return json.dumps({"step": step_name, "dvc_files": list(dvc_files.keys())})

    def _collect_dvc_files(self, dir_names: list[str] | None = None) -> dict[str, str]:
        """Collect .dvc file contents keyed by tracked directory name."""
        dvc_files: dict[str, str] = {}
        if dir_names:
            for dir_name in dir_names:
                dvc_path = self.path / f"{dir_name}.dvc"
                if dvc_path.exists():
                    dvc_files[dir_name] = dvc_path.read_text()
            if dvc_files:
                return dvc_files
        for dvc_path in sorted(self.path.glob("*.dvc")):
            if not dvc_path.is_file():
                continue
            dvc_files[dvc_path.stem] = dvc_path.read_text()
        return dvc_files

    async def _validate_dvc_files_restorable(self, dvc_files: dict[str, str]) -> None:
        """Validate that all DVC manifests referenced by .dvc files exist in S3."""
        from plato.worlds.lazy_dvc import DVCManifest, S3Config

        if not dvc_files:
            return

        await self._ensure_credentials()
        s3_config = S3Config(
            bucket=self.s3_bucket,
            prefix=self.s3_prefix,
            credentials=self._aws_credentials(),
        )
        for dir_name, dvc_content in dvc_files.items():
            try:
                await DVCManifest.from_dvc_file(dvc_content, s3_config)
            except Exception as e:
                raise RuntimeError(
                    f"Workspace '{self.name}' DVC pointer for dir '{dir_name}' is not restorable "
                    f"(repo={self.repo_name}): {e}"
                ) from e

    # ------------------------------------------------------------------
    # Restore: pull data from S3 for a previous step
    # ------------------------------------------------------------------

    async def restore(self, step_name: str) -> bool:
        """Restore workspace lazily via FUSE.

        Returns True when at least one tracked directory was mounted, False when
        the ref exists but has no DVC files.
        """
        from plato.worlds.lazy_dvc import DVCManifest, S3Config, mount_lazy

        self._require_tracked()
        await self._ensure_credentials()

        ref = await self._fetch_workspace_ref(step_name)
        if not ref:
            raise RuntimeError(f"No workspace ref found for step '{step_name}'")
        self._last_restored_source_ref_public_id = ref.get("ref_public_id", "")

        dvc_files = ref.get("dvc_files", {})
        if not dvc_files:
            logger.warning(f"No DVC files in ref for step '{step_name}', nothing to restore")
            return False

        s3_config = S3Config(
            bucket=self.s3_bucket,
            prefix=self.s3_prefix,
            credentials=self._aws_credentials(),
        )

        if not hasattr(self, "_lazy_mounts"):
            self._lazy_mounts: dict[str, Any] = {}

        for dir_name, dvc_content in dvc_files.items():
            try:
                manifest = await DVCManifest.from_dvc_file(dvc_content, s3_config)
            except Exception as e:
                raise RuntimeError(
                    f"Failed to restore workspace '{self.name}' at step '{step_name}' "
                    f"(repo={self.repo_name}, dir={dir_name}): {e}"
                ) from e
            mountpoint = self.path / dir_name
            mountpoint.mkdir(parents=True, exist_ok=True)
            cache_dir = self.path / ".lazy_cache" / dir_name
            cache_dir.mkdir(parents=True, exist_ok=True)
            mount = await mount_lazy(mountpoint, manifest, s3_config, cache_dir)
            self._lazy_mounts[dir_name] = mount

            # Write .dvc pointer file so git scaffolding stays consistent
            dvc_path = self.path / f"{dir_name}.dvc"
            dvc_path.write_text(dvc_content)

        logger.info("Lazy restore complete for step '%s': %d mount(s)", step_name, len(dvc_files))
        self._last_ref_step = step_name
        return True

    async def _smart_commit(self, step_name: str, message: str = "") -> str:
        """Commit with smart diff — only upload changed files."""
        from plato.worlds.lazy_dvc import DVCManifest, S3Config, mount_lazy, smart_commit, unmount_lazy

        self._require_tracked()
        await self._ensure_credentials()

        s3_config = S3Config(
            bucket=self.s3_bucket,
            prefix=self.s3_prefix,
            credentials=self._aws_credentials(),
        )

        dvc_files: dict[str, str] = {}
        for dir_name, mount in list(self._lazy_mounts.items()):
            await unmount_lazy(mount)
            manifest_md5, dvc_yaml = await smart_commit(mount, s3_config, dir_name=dir_name)

            dvc_path = self.path / f"{dir_name}.dvc"
            dvc_path.write_text(dvc_yaml)
            dvc_files[dir_name] = dvc_yaml

            # Re-mount with updated manifest, reusing warm cache
            meta_path = mount.cache_dir / "meta.json"
            if meta_path.exists():
                meta_path.unlink()

            new_manifest = await DVCManifest.from_dvc_file(dvc_yaml, s3_config)
            mountpoint = self.path / dir_name
            mountpoint.mkdir(parents=True, exist_ok=True)
            new_mount = await mount_lazy(mountpoint, new_manifest, s3_config, mount.cache_dir)
            self._lazy_mounts[dir_name] = new_mount

        # Git commit pointer files
        await _run("git", "add", ".", cwd=self.path)
        msg = message or f"step: {step_name}"
        await _run("git", "commit", "-m", msg, "--allow-empty", cwd=self.path)

        # Record ref in Chronos
        await self._record_workspace_ref(step_name, "output", dvc_files, changed=True)

        return json.dumps({"step": step_name, "dvc_files": list(dvc_files.keys())})

    async def to_state_dict(self) -> dict[str, Any]:
        """Snapshot workspace metadata for state persistence."""
        restore_step = self._last_changed_ref_step or self._last_ref_step
        return {
            "name": self.name,
            "path": str(self.path),
            "tracked": self.tracked,
            "repo_name": self.repo_name,
            "s3_bucket": self.s3_bucket,
            "s3_prefix": self.s3_prefix,
            "session_id": self.session_id,
            "steps": [restore_step] if restore_step else [],
        }

    async def list_steps(self) -> list[str]:
        """List all committed step names from Chronos."""
        if not self.chronos_url or not self.repo_name or not self.session_id:
            return []
        refs = await self._list_workspace_refs()
        return [r["step_name"] for r in refs]

    # ------------------------------------------------------------------
    # Chronos integration
    # ------------------------------------------------------------------

    async def _chronos_request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        """Send an HTTP request to the Chronos API."""
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.request(
                method,
                f"{self.chronos_url}{path}",
                headers={"X-API-Key": self.api_key},
                **kwargs,
            )
            resp.raise_for_status()
            return resp

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
    ) -> None:
        """Record a workspace ref with Chronos, including DVC file contents."""
        if not self.chronos_url or not self.repo_name or not self.session_id:
            return
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
        }
        if has_source_ref:
            payload["source_ref_public_id"] = source_ref_public_id
        elif has_source_parts:
            payload["source_session_public_id"] = source_session_public_id
            payload["source_repo_name"] = source_repo_name
            payload["source_step_name"] = source_step_name
        await self._chronos_request(
            "POST",
            f"/api/workspace-repos/sessions/{self.session_id}/workspace-refs",
            json=payload,
        )
        self._last_ref_step = step_name
        if changed is True:
            self._last_changed_ref_step = step_name

    async def _fetch_workspace_ref(self, step_name: str) -> dict[str, Any] | None:
        """Fetch a specific workspace ref from Chronos."""
        if not self.chronos_url or not self.repo_name or not self.session_id:
            return None
        resp = await self._chronos_request(
            "GET",
            f"/api/workspace-repos/sessions/{self.session_id}/workspace-refs",
            params={"step_name": step_name, "repo_name": self.repo_name},
        )
        data = resp.json()
        refs = data.get("refs", [])
        for ref in reversed(refs):
            if ref.get("step_name") == step_name:
                return ref
        return None

    async def _list_workspace_refs(self) -> list[dict[str, Any]]:
        """List all workspace refs for this session from Chronos."""
        resp = await self._chronos_request(
            "GET",
            f"/api/workspace-repos/sessions/{self.session_id}/workspace-refs",
            params={"repo_name": self.repo_name},
        )
        return resp.json().get("refs", [])

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
        from datetime import datetime

        expires_at = datetime.fromisoformat(data["expires_at"].replace("Z", "+00:00"))
        self._sts_expires_at = expires_at.timestamp() - 300
        logger.info(f"Refreshed STS credentials for repo '{self.repo_name}'")

    def _s3_env(self) -> dict[str, str]:
        """Return environment variables for AWS CLI calls with STS creds."""
        env = dict(os.environ)
        if self._sts_credentials:
            env.update(self._sts_credentials)
        return env

    def _aws_credentials(self) -> dict[str, str]:
        """Return only AWS_* credentials for boto3 / S3Config use."""
        return {k: v for k, v in self._s3_env().items() if k.startswith("AWS_")}

    async def _ensure_credentials(self) -> None:
        """Refresh STS credentials if expired or missing."""
        if self.chronos_url and self.repo_id:
            if not self._sts_credentials or time.time() >= self._sts_expires_at:
                await self._refresh_credentials()

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _require_tracked(self) -> None:
        if not self.tracked:
            raise RuntimeError(f"Workspace '{self.name}' is not tracked (tracked=False)")


# ------------------------------------------------------------------
# Subprocess helpers
# ------------------------------------------------------------------


class _ProcessResult:
    def __init__(self, stdout_text: str):
        self.stdout_text = stdout_text


async def _run(*args: str, cwd: Path, env: dict[str, str] | None = None) -> _ProcessResult:
    """Run a subprocess, raise on failure."""
    run_env = env if env is not None else dict(os.environ)
    # Always set — DVC stops at mount boundaries without this
    run_env["GIT_DISCOVERY_ACROSS_FILESYSTEM"] = "1"
    proc = await asyncio.create_subprocess_exec(
        *args,
        cwd=str(cwd),
        env=run_env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"Command {args} failed: {stderr.decode()}")
    return _ProcessResult(stdout.decode())
