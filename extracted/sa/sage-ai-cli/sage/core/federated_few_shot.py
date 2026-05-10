"""Federated few-shot — share accepted/rejected patterns across machines via GCS.

Local store from `core/few_shot.py` is per-machine. This module syncs
those examples to `<bucket>/few_shot/<user_id>/<project_hash>.json` so
sage on machine A learns from machine B's accepted code.

Safety:
  - Sharing is opt-in (cfg.few_shot_share = True; default False)
  - Examples are de-duplicated by content hash
  - Local examples always take precedence on conflict
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from dataclasses import asdict
from pathlib import Path

from sage.config import SageConfig
from sage.core.few_shot import FewShotExample, FewShotStore

__all__ = ["FederatedFewShot"]


def _have_gsutil() -> bool:
    return shutil.which("gsutil") is not None


def _project_hash(cwd: Path) -> str:
    return hashlib.sha1(str(cwd.resolve()).encode("utf-8")).hexdigest()[:12]


class FederatedFewShot:
    def __init__(self, cwd: Path, cfg: SageConfig | None = None,
                 user_id: str = "default"):
        self.cwd = cwd.resolve()
        if cfg is None:
            from sage.config import load_config
            cfg = load_config()
        self.cfg = cfg
        self.user_id = user_id
        self.local = FewShotStore(self.cwd)

    def gcs_uri(self) -> str:
        return f"{self.cfg.gcs_corpus_bucket}/few_shot/{self.user_id}/{_project_hash(self.cwd)}.json"

    def push(self) -> bool:
        """Upload local store to GCS. Returns False if gsutil missing."""
        if not _have_gsutil():
            return False
        if not self.local.path.is_file():
            return False
        try:
            r = subprocess.run(
                ["gsutil", "-q", "cp", str(self.local.path), self.gcs_uri()],
                capture_output=True, text=True, timeout=60,
            )
            return r.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def pull_and_merge(self) -> int:
        """Download remote store and merge into local. Returns # examples added.

        Conflict resolution: local wins on dup id; remote-only entries are
        appended.
        """
        if not _have_gsutil():
            return 0
        import tempfile
        with tempfile.NamedTemporaryFile("rb", delete=False, suffix=".json") as tmp:
            tmp_path = Path(tmp.name)
        try:
            r = subprocess.run(
                ["gsutil", "-q", "cp", self.gcs_uri(), str(tmp_path)],
                capture_output=True, text=True, timeout=60,
            )
            if r.returncode != 0:
                return 0
            try:
                remote_data = json.loads(tmp_path.read_text("utf-8"))
            except (json.JSONDecodeError, OSError):
                return 0
        finally:
            tmp_path.unlink(missing_ok=True)

        # Local example fingerprints (prompt+response hash) for dup detection
        seen = {self._fingerprint(e) for e in self.local._examples}
        added = 0
        for d in remote_data.get("examples", []):
            try:
                ex = FewShotExample(**d)
            except (TypeError, KeyError):
                continue
            if self._fingerprint(ex) in seen:
                continue
            self.local._examples.append(ex)
            added += 1
        if added > 0:
            self.local._save()
        return added

    @staticmethod
    def _fingerprint(ex: FewShotExample) -> str:
        return hashlib.sha1((ex.prompt + "|" + ex.response).encode("utf-8")).hexdigest()[:16]
