"""Artifact capture helpers for CUA agents."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class ArtifactCaptureMixin:
    async def _capture_artifacts(self: Any, context: Any) -> None:
        """Capture uploaded files and their post-run state from the sandbox."""
        if self.task_dir is None:
            return
        manifest_path = self.task_dir / "tests" / "setup" / "files" / "manifest.json"
        if not manifest_path.exists():
            return
        try:
            entries = json.loads(manifest_path.read_text())
        except Exception as e:
            self.logger.warning(f"artifacts: manifest parse failed: {e}")
            return
        if not entries:
            return

        artifacts_dir = self.logs_dir.parent / "artifacts"
        uploaded_dir = artifacts_dir / "uploaded"
        final_dir = artifacts_dir / "final"
        uploaded_dir.mkdir(parents=True, exist_ok=True)
        final_dir.mkdir(parents=True, exist_ok=True)

        captured: list[dict[str, Any]] = []
        for entry in entries:
            remote = entry.get("remote_path")
            local_name = entry.get("local_name")
            if not remote or not local_name:
                continue
            src_local = self.task_dir / "tests" / "setup" / "files" / local_name
            basename = Path(remote).name
            uploaded_target = uploaded_dir / basename
            final_target = final_dir / basename
            uploaded_sha: str | None = None
            final_sha: str | None = None
            uploaded_size = 0
            final_size = 0

            try:
                if src_local.exists():
                    data = src_local.read_bytes()
                    uploaded_target.write_bytes(data)
                    uploaded_sha = hashlib.sha256(data).hexdigest()
                    uploaded_size = len(data)
            except Exception as e:
                self.logger.warning(f"artifacts: copy uploaded {basename} failed: {e}")

            try:
                sandbox = self.sandbox
                if sandbox is None:
                    return
                download_file = getattr(sandbox, "download_file", None)
                if download_file is None:
                    self.logger.warning("artifacts: sandbox cannot download files")
                    return
                await download_file(remote, final_target)
                fbytes = final_target.read_bytes()
                final_sha = hashlib.sha256(fbytes).hexdigest()
                final_size = len(fbytes)
            except Exception as e:
                self.logger.warning(f"artifacts: download final {remote} failed: {e}")

            captured.append(
                {
                    "name": basename,
                    "remote_path": remote,
                    "uploaded_size": uploaded_size,
                    "final_size": final_size,
                    "changed": (
                        uploaded_sha is not None
                        and final_sha is not None
                        and uploaded_sha != final_sha
                    ),
                    "uploaded_sha256": uploaded_sha,
                    "final_sha256": final_sha,
                }
            )

        if captured:
            (artifacts_dir / "uploaded_files.json").write_text(json.dumps(captured, indent=2))
            self.logger.info(f"artifacts: captured {len(captured)} file(s) under {artifacts_dir}")
