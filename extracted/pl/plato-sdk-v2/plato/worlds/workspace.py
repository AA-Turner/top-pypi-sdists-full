"""Workspace: a directory with S3 versioning and agent-mountable transport.

The workspace path is always writable — agents write to it via NFS.
Versioning (tracked=True) uses FUSE overlay + S3 for data storage, with Chronos
tracking refs/metadata.
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
        backup: bool = True,
        dvcignore: list[str] | None = None,
        s3_bucket: str = "",
        s3_prefix: str = "",
        repo_id: str = "",
        repo_name: str = "",
        chronos_url: str = "",
        api_key: str = "",
        session_id: str = "",
    ):
        self._repo_root = path
        self.path = path / "data" if tracked else path
        self.name = name
        self.tracked = tracked
        self._mount_path = mount_path
        self.backup = backup
        self._custom_dvcignore = dvcignore or []
        self.s3_bucket = s3_bucket
        self.s3_prefix = s3_prefix
        self.repo_id = repo_id
        self.repo_name = repo_name
        self.chronos_url = chronos_url
        self.api_key = api_key
        self.session_id = session_id
        self.transport: Transport | None = None
        self._sts_credentials: dict[str, str] = {}
        self._sts_expires_at: float = 0
        self._last_ref_step: str = ""
        self._last_changed_ref_step: str = ""
        self._lazy_mounts: dict[str, Any] = {}
        self._commit_lock = asyncio.Lock()

    @property
    def mount_path(self) -> str:
        if self._mount_path is not None:
            return self._mount_path
        return str(self.path)

    @staticmethod
    def _cleanup_stale_mount(path: Path) -> None:
        """Unmount a stale FUSE mount if present."""
        try:
            path.stat()
        except OSError as e:
            if e.errno == 107:  # ENOTCONN — dead FUSE mount
                import subprocess

                logger.warning("Cleaning up stale FUSE mount at %s", path)
                # Use lazy unmount to detach immediately even if busy
                subprocess.run(["fusermount3", "-uz", str(path)], check=False)
                # Remove the stale mount point so mkdir can recreate it
                try:
                    path.rmdir()
                except OSError:
                    pass
        except FileNotFoundError:
            pass

    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------

    async def init(self) -> None:
        """Initialize workspace directory. Idempotent."""
        from plato.markers import WorkspaceMarker

        self._repo_root.mkdir(parents=True, exist_ok=True)

        # Remove legacy .lazy_cache from repo root (now lives in /tmp)
        legacy_cache = self._repo_root / ".lazy_cache"
        if legacy_cache.exists():
            import shutil

            shutil.rmtree(legacy_cache, ignore_errors=True)

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

    async def ensure_fuse_mount(self) -> None:
        """Mount FUSE overlay. Skips if already mounted."""
        if self._lazy_mounts:
            return

        from plato.worlds.dvc_models import DVCManifest, S3Config
        from plato.worlds.lazy_dvc import mount_lazy

        if self.tracked:
            await self._ensure_credentials()
            s3_config = S3Config(
                bucket=self.s3_bucket,
                prefix=self.s3_prefix,
                credentials=self._aws_credentials(),
            )
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
            logger.info("Moving %d items from %s into FUSE overlay", len(contents), self.path)
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
        logger.info("Mounted FUSE at %s", self.path)

    # ------------------------------------------------------------------
    # Commit
    # ------------------------------------------------------------------

    async def commit(self, step_name: str, message: str = "") -> str:
        """Snapshot current workspace to S3 via smart commit."""
        async with self._commit_lock:
            return await self._commit_inner(step_name, message)

    async def _commit_inner(self, step_name: str, message: str = "") -> str:
        if not self._lazy_mounts:
            raise RuntimeError(
                f"Workspace '{self.name}' has no FUSE mounts. ensure_fuse_mount() must be called before commit()."
            )

        has_changes = any(
            any(mount.overlay_dir.iterdir()) if mount.overlay_dir.exists() else False
            for mount in self._lazy_mounts.values()
        )
        if not has_changes:
            logger.info("Workspace '%s': no changes at '%s', skipping commit", self.name, step_name)
            dvc_files = self._collect_dvc_files(list(self._lazy_mounts.keys()))
            if dvc_files:
                await self._ensure_credentials()
                try:
                    await self._validate_dvc_files_restorable(dvc_files)
                except Exception as e:
                    logger.warning("Workspace '%s': ref validation failed (no changes): %s", self.name, e)
            return json.dumps({"step": step_name, "changed": False})
        return await self._smart_commit(step_name, message)

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

        from plato.worlds.dvc_models import DVCManifest, S3Config

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
                    f"Workspace '{self.name}' manifest for '{dir_name}' not restorable (repo={self.repo_name}): {e}"
                ) from e

    # ------------------------------------------------------------------
    # Restore
    # ------------------------------------------------------------------

    async def restore(self, step_name: str, session_id: str | None = None) -> bool:
        """Restore workspace lazily via FUSE.

        Returns True when at least one tracked directory was mounted, False when
        the ref exists but has no DVC files.
        """
        from plato.worlds.dvc_models import DVCManifest, S3Config
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
            logger.info("Workspace '%s' step '%s' has no DVC files", self.name, step_name)
            self._last_ref_step = step_name
            return True

        s3_config = S3Config(
            bucket=self.s3_bucket,
            prefix=self.s3_prefix,
            credentials=self._aws_credentials(),
        )

        for dir_name, dvc_content in dvc_files.items():
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

        logger.info("Restored workspace '%s' step '%s': %d mount(s)", self.name, step_name, len(dvc_files))
        self._last_ref_step = step_name
        return True

    async def _smart_commit(self, step_name: str, message: str = "") -> str:
        """Commit with smart diff — only upload changed files."""
        from plato.worlds.dvc_models import S3Config, smart_commit

        self._require_tracked()
        await self._ensure_credentials()

        s3_config = S3Config(
            bucket=self.s3_bucket,
            prefix=self.s3_prefix,
            credentials=self._aws_credentials(),
        )

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
        await self._record_workspace_ref(step_name, "output", dvc_files, changed=True)

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
        """Record a workspace ref with Chronos."""
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

    async def _list_workspace_refs(self, session_id: str | None = None) -> list[dict[str, Any]]:
        sid = session_id or self.session_id
        resp = await self._chronos_request(
            "GET",
            f"/api/workspace-repos/sessions/{sid}/workspace-refs",
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
        logger.info("Refreshed STS credentials for repo '%s'", self.repo_name)

    def _aws_credentials(self) -> dict[str, str]:
        env = dict(os.environ)
        if self._sts_credentials:
            env.update(self._sts_credentials)
        return {k: v for k, v in env.items() if k.startswith("AWS_")}

    async def _ensure_credentials(self) -> None:
        if self.chronos_url and self.repo_id:
            if not self._sts_credentials or time.time() >= self._sts_expires_at:
                await self._refresh_credentials()

    def _require_tracked(self) -> None:
        if not self.tracked:
            raise RuntimeError(f"Workspace '{self.name}' is not tracked (tracked=False)")
