"""Restic-based workspace checkpointing mixin for BaseWorld.

Provides per-step backup and restore of registered workspace directories
using restic for deduplication. The restic repo is tarred and uploaded to
S3 via Chronos presigned URLs alongside the world state.
"""

from __future__ import annotations

import asyncio
import logging
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from plato.worlds.s3 import download_to_file, upload_to_s3

logger = logging.getLogger(__name__)

RESTIC_PASSWORD = "plato"


class WorkspaceSnapshot(BaseModel):
    """Metadata for a single restic snapshot."""

    workspace: str
    step: int
    timestamp: str


class ResticCheckpointMixin:
    """Mixin that adds restic workspace checkpointing to a world.

    Requires the host class to provide:
        - ``self.logger``
        - ``self.config.state.path`` (state directory)
        - ``self._step_count``
        - ``self._get_chronos_base_url() -> str``
        - ``self.session.session_id``
    """

    # Type declarations for attributes provided by the host class (BaseWorld).
    config: Any
    logger: logging.Logger
    session: Any
    _step_count: int

    def _get_chronos_base_url(self) -> str:
        raise NotImplementedError

    def __init_restic__(self) -> None:
        """Initialize restic-related state. Call from ``__init__``."""
        self._workspace_paths: dict[str, str] = {}
        self._workspace_backup_flags: dict[str, bool] = {}
        self._workspace_snapshots: list[WorkspaceSnapshot] = []
        self._restic_initialized = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register_workspace(self, name: str, path: str | Path, backup: bool = True) -> None:
        """Register a workspace directory for restic checkpointing.

        Args:
            name: Logical name for the workspace.
            path: Directory path to back up.
            backup: If False, the workspace is tracked for restore but skipped
                during restic backup (useful for large ephemeral data).
        """
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        self._workspace_paths[name] = str(p)
        self._workspace_backup_flags[name] = backup
        self.logger.info(f"Registered workspace '{name}' at {p} (backup={backup})")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _serialize_workspaces(self) -> dict:
        """Serialize workspace registrations and snapshot metadata."""
        return {
            "paths": self._workspace_paths,
            "backup_flags": self._workspace_backup_flags,
            "snapshots": [s.model_dump() for s in self._workspace_snapshots],
        }

    def _deserialize_workspaces(self, data: dict) -> None:
        """Restore workspace state from previously serialized data."""
        if "paths" in data:
            self._workspace_paths = dict(data["paths"])
            self._workspace_backup_flags = dict(data.get("backup_flags", {}))
            self._workspace_snapshots = [WorkspaceSnapshot(**s) for s in data.get("snapshots", [])]
        else:
            # Legacy format: just a dict of paths
            self._workspace_paths = dict(data)
            self._workspace_snapshots = []
        # Ensure all workspace directories exist (they may not on a fresh VM after resume)
        for path in self._workspace_paths.values():
            Path(path).mkdir(parents=True, exist_ok=True)

    def get_available_snapshots(self) -> list[WorkspaceSnapshot]:
        """Return all recorded workspace snapshots."""
        return list(self._workspace_snapshots)

    def get_resumable_steps(self) -> list[int]:
        """Return sorted list of steps that can be resumed to."""
        steps = {s.step for s in self._workspace_snapshots}
        return sorted(steps)

    # ------------------------------------------------------------------
    # Restic repo management
    # ------------------------------------------------------------------

    async def _ensure_restic(self) -> bool:
        """Ensure restic is installed and the repo is initialized."""
        if self._restic_initialized:
            return True

        proc = await asyncio.create_subprocess_exec(
            "which",
            "restic",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.wait()
        if proc.returncode != 0:
            self.logger.warning("restic not found — workspace checkpointing disabled")
            return False

        repo_path = Path(self.config.state.path) / "restic-repo"
        env = {**os.environ, "RESTIC_REPOSITORY": str(repo_path), "RESTIC_PASSWORD": RESTIC_PASSWORD}

        # If repo exists, verify it's usable. If not, nuke and recreate.
        config_file = repo_path / "config"
        if config_file.exists():
            proc = await asyncio.create_subprocess_exec(
                "restic",
                "cat",
                "config",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
                env=env,
            )
            await proc.wait()
            if proc.returncode == 0:
                self._restic_initialized = True
                return True
            # Repo exists but is corrupted/wrong keys — wipe it
            self.logger.warning("Restic repo corrupted, reinitializing")
            shutil.rmtree(repo_path)

        repo_path.mkdir(parents=True, exist_ok=True)
        proc = await asyncio.create_subprocess_exec(
            "restic",
            "init",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )
        _, stderr = await proc.communicate()
        if proc.returncode != 0:
            self.logger.warning(f"restic init failed: {stderr.decode()}")
            return False

        self._restic_initialized = True
        return True

    # ------------------------------------------------------------------
    # Checkpoint (backup)
    # ------------------------------------------------------------------

    async def _checkpoint_workspaces(self) -> None:
        """Backup all registered workspaces with restic and upload the repo tarball."""
        workspace_paths = self._workspace_paths
        if not workspace_paths:
            return

        if not await self._ensure_restic():
            return

        repo_path = str(Path(self.config.state.path) / "restic-repo")
        env = {**os.environ, "RESTIC_REPOSITORY": repo_path, "RESTIC_PASSWORD": RESTIC_PASSWORD}

        for name, path in workspace_paths.items():
            if not self._workspace_backup_flags.get(name, False):
                self.logger.info(f"Skipping backup for workspace '{name}' (backup=False)")
                continue
            resolved_path = str(Path(path).resolve())
            self.logger.info(f"Backing up workspace '{name}' ({path} -> {resolved_path}) at step {self._step_count}")
            proc = await asyncio.create_subprocess_exec(
                "restic",
                "backup",
                "--tag",
                name,
                "--tag",
                f"step:{self._step_count}",
                "--tag",
                f"session:{self.session.session_id}",
                "--exclude",
                ".venv",
                "--exclude",
                "node_modules",
                "--exclude",
                "__pycache__",
                "--exclude",
                ".pnpm-store",
                resolved_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
            )
            stdout, stderr = await proc.communicate()
            if proc.returncode != 0:
                self.logger.error(
                    f"restic backup failed for '{name}': stdout={stdout.decode()} stderr={stderr.decode()}"
                )
            else:
                self.logger.info(f"restic backup complete for '{name}'")
                self._workspace_snapshots.append(
                    WorkspaceSnapshot(
                        workspace=name,
                        step=self._step_count,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                    )
                )

        await self._upload_workspace_backup()

    async def _upload_workspace_backup(self) -> bool:
        """Tar the restic repo and stream-upload via presigned URL."""
        repo_path = Path(self.config.state.path) / "restic-repo"
        tar_path = Path("/tmp/workspace.tar")

        proc = await asyncio.create_subprocess_exec(
            "tar",
            "cf",
            str(tar_path),
            "-C",
            str(repo_path.parent),
            "restic-repo",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()
        if proc.returncode != 0:
            self.logger.error("Failed to tar restic repo")
            return False

        session_id = self.session.session_id
        if not session_id:
            return False

        base_url = self._get_chronos_base_url()
        if not base_url:
            return False

        # Stream from file — no full read into memory
        return await upload_to_s3(base_url, session_id, "workspace", tar_path, "application/x-tar", timeout=120)

    # ------------------------------------------------------------------
    # Restore
    # ------------------------------------------------------------------

    async def _download_workspace_backup(self, session_id: str) -> bool:
        """Stream-download workspace.tar from a session via presigned URL and untar it."""
        base_url = self._get_chronos_base_url()
        if not base_url:
            return False

        tar_path = Path("/tmp/workspace.tar")

        # Stream directly to file — no full load into memory
        ok = await download_to_file(base_url, session_id, "workspace", tar_path, timeout=120)
        if not ok:
            return False

        state_dir = Path(self.config.state.path)
        state_dir.mkdir(parents=True, exist_ok=True)

        proc = await asyncio.create_subprocess_exec(
            "tar",
            "xf",
            str(tar_path),
            "-C",
            str(state_dir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()
        if proc.returncode != 0:
            self.logger.error("Failed to untar workspace backup")
            return False

        self._restic_initialized = True
        self.logger.info(f"Downloaded workspace backup from session {session_id}")
        return True

    async def _restore_workspaces(self, step: int | None = None) -> None:
        """Restore registered workspaces from restic snapshots."""
        workspace_paths = self._workspace_paths
        if not workspace_paths:
            return

        repo_path = Path(self.config.state.path) / "restic-repo"
        if not repo_path.exists():
            self.logger.debug("No restic repo found — skipping workspace restore")
            return

        if not await self._ensure_restic():
            return

        env = {**os.environ, "RESTIC_REPOSITORY": str(repo_path), "RESTIC_PASSWORD": RESTIC_PASSWORD}

        for name, path in workspace_paths.items():
            if not self._workspace_backup_flags.get(name, False):
                self.logger.info(f"Skipping restore for workspace '{name}' (backup=False)")
                continue
            cmd = ["restic", "restore", "latest", "--tag", name, "--target", "/"]
            if step is not None:
                cmd = ["restic", "restore", "latest", "--tag", name, "--tag", f"step:{step}", "--target", "/"]

            self.logger.info(f"Restoring workspace '{name}' to {path}" + (f" at step {step}" if step else ""))
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
            )
            _, stderr = await proc.communicate()
            if proc.returncode != 0:
                self.logger.error(f"restic restore failed for '{name}': {stderr.decode()}")
            else:
                self.logger.info(f"Restored workspace '{name}'")
