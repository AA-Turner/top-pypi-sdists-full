"""GCS-backed shared training corpus.

Layout in the bucket (default `gs://sage-ai-models`):

  training-corpus/
    <user_id>/
      <project_hash>/
        snapshot-<YYYYMMDD-HHMMSS>.jsonl  — one example per line
        latest.txt                          — pointer to most recent snapshot
        meta.json                           — project metadata
    shared/
      catalog.json                          — registry of public corpora

Each example is a JSON object:
  {
    "id": "<sha1 hash of text>",
    "instruction": "...",
    "input": "...",
    "output": "...",
    "tags": ["python", "fastapi"],
    "source": {"path": "src/foo.py", "kind": "code|interaction|test"},
    "ts": 1730000000.0
  }

Cost notes:
  - GCS storage is $0.02/GB/mo (Standard) — corpus is tiny (text)
  - Egress is free within the same region; we read once, cache locally
  - We dedup on `id` (content hash) so repeated reuploads are no-ops

Auth: uses gsutil if installed (which already works for the user — they
have sync_models_to_gcs.py running). Falls back to google-cloud-storage
SDK if gsutil isn't on PATH.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from collections.abc import Iterable, Iterator
from dataclasses import asdict, dataclass, field
from pathlib import Path

__all__ = [
    "TrainingExample",
    "ProjectCorpus",
    "CorpusManager",
    "should_include_file",  # ← user-contribution stub
]


@dataclass
class TrainingExample:
    instruction: str
    input: str
    output: str
    tags: list[str] = field(default_factory=list)
    source: dict = field(default_factory=dict)
    ts: float = field(default_factory=time.time)
    id: str = ""

    def __post_init__(self) -> None:
        if not self.id:
            payload = (self.instruction + "\n" + self.input + "\n" + self.output).encode("utf-8")
            self.id = hashlib.sha1(payload).hexdigest()

    def to_jsonl(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


# ── ★ User contribution (learning mode) ─────────────────────────────────
#
# This is the function I asked you to write. It decides which files from
# a project are good training material vs. noise. The signature is fixed
# (a Path → bool); the policy inside is yours.
#
# Trade-offs to weigh:
#   - Tests: include? (teaches API usage but biases toward test patterns)
#   - Generated/migrations: usually skip (formulaic, low signal)
#   - Vendored deps: definitely skip (not the user's idioms)
#   - Lockfiles / large JSON: skip (mostly hashes)
#   - Docs: include (often clearer than the code itself)
#   - Secrets / .env: NEVER include
#
# The current implementation is a deliberately conservative starting point.
# Tune it for what you want the trained model to learn.
def should_include_file(path: Path) -> bool:
    """Return True if `path` should be included in the training corpus.

    TODO(you): refine this. The current rules are placeholders.
    """
    # ★ YOUR CODE HERE — replace this body with your judgment ★
    name = path.name.lower()
    parts = {p.lower() for p in path.parts}

    # Hard skips (security): never train on secrets
    if name in {".env", ".env.local", ".env.production", ".env.staging"}:
        return False
    if name.endswith(".pem") or name.endswith(".key"):
        return False

    # Skip vendored / generated / build output
    skip_dirs = {"node_modules", "vendor", "third_party", "dist", "build",
                 ".next", "__pycache__", "target", ".git"}
    if parts & skip_dirs:
        return False

    # Skip lockfiles
    if name in {"package-lock.json", "yarn.lock", "pnpm-lock.yaml",
                "poetry.lock", "uv.lock", "cargo.lock"}:
        return False

    # Default: include source-y extensions
    return path.suffix.lower() in {
        ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java", ".kt",
        ".rb", ".php", ".swift", ".c", ".cpp", ".h", ".cs", ".scala",
        ".md", ".rst",
    }
# ────────────────────────────────────────────────────────────────────────


def _project_hash(cwd: Path) -> str:
    return hashlib.sha1(str(cwd.resolve()).encode("utf-8")).hexdigest()[:12]


def _have_gsutil() -> bool:
    return shutil.which("gsutil") is not None


def _gcs_cp(src: str, dst: str) -> bool:
    """Copy src → dst using gsutil. Returns True on success."""
    try:
        out = subprocess.run(
            ["gsutil", "-q", "cp", src, dst],
            capture_output=True, text=True, timeout=120,
        )
        return out.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _gcs_ls(uri: str) -> list[str]:
    try:
        out = subprocess.run(
            ["gsutil", "ls", uri],
            capture_output=True, text=True, timeout=30,
        )
        if out.returncode != 0:
            return []
        return [line.strip() for line in out.stdout.splitlines() if line.strip()]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []


@dataclass
class ProjectCorpus:
    """A project's training corpus, locally cached + GCS-mirrored."""

    cwd: Path
    bucket: str = "gs://sage-ai-models"
    user_id: str = "default"

    @property
    def project_hash(self) -> str:
        return _project_hash(self.cwd)

    @property
    def gcs_dir(self) -> str:
        return f"{self.bucket}/training-corpus/{self.user_id}/{self.project_hash}"

    @property
    def local_dir(self) -> Path:
        return Path.home() / ".sage" / "corpus" / self.project_hash

    @property
    def latest_local(self) -> Path:
        return self.local_dir / "latest.jsonl"

    def _ensure_local(self) -> None:
        self.local_dir.mkdir(parents=True, exist_ok=True)


class CorpusManager:
    """Build, upload, and download training corpora."""

    def __init__(self, bucket: str = "gs://sage-ai-models", user_id: str = "default"):
        self.bucket = bucket
        self.user_id = user_id

    def project(self, cwd: Path) -> ProjectCorpus:
        return ProjectCorpus(cwd=cwd.resolve(), bucket=self.bucket, user_id=self.user_id)

    # ── Build (from cwd) ────────────────────────────────────────

    def harvest_from_filesystem(
        self,
        cwd: Path,
        *,
        max_files: int = 500,
        max_chars_per_example: int = 4000,
    ) -> Iterator[TrainingExample]:
        """Walk cwd and yield TrainingExample per included file.

        Each example is shaped as instruction-tuning: the user "asks for" the
        file, the model "writes" it. Crude, but tracks how the user actually
        structures code — which is the entire point.
        """
        from sage.core.project_detect import detect_project, format_for_prompt
        ctx = detect_project(cwd)
        ctx_block = format_for_prompt(ctx).strip()

        seen = 0
        for dirpath, dirnames, filenames in os.walk(cwd):
            dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in {
                "node_modules", "venv", ".venv", "__pycache__", "dist", "build",
            }]
            for name in filenames:
                p = Path(dirpath) / name
                if not should_include_file(p):
                    continue
                try:
                    text = p.read_text("utf-8", errors="replace")
                except OSError:
                    continue
                if not text.strip():
                    continue
                if len(text) > max_chars_per_example:
                    text = text[:max_chars_per_example]
                rel = str(p.relative_to(cwd))
                instruction = f"Write the file {rel}."
                input_block = ctx_block
                yield TrainingExample(
                    instruction=instruction,
                    input=input_block,
                    output=text,
                    tags=ctx.languages + ctx.frameworks,
                    source={"path": rel, "kind": "code"},
                )
                seen += 1
                if seen >= max_files:
                    return

    def write_snapshot(
        self,
        cwd: Path,
        examples: Iterable[TrainingExample],
        *,
        upload: bool = True,
    ) -> Path:
        """Write a deduplicated JSONL snapshot locally; optionally push to GCS."""
        proj = self.project(cwd)
        proj._ensure_local()

        ts = time.strftime("%Y%m%d-%H%M%S")
        snap_path = proj.local_dir / f"snapshot-{ts}.jsonl"
        seen_ids: set[str] = set()
        count = 0
        with snap_path.open("w", encoding="utf-8") as fh:
            for ex in examples:
                if ex.id in seen_ids:
                    continue
                seen_ids.add(ex.id)
                fh.write(ex.to_jsonl() + "\n")
                count += 1

        # Update latest pointer
        proj.latest_local.write_text(snap_path.read_text("utf-8"), "utf-8")
        (proj.local_dir / "meta.json").write_text(json.dumps({
            "user_id": self.user_id,
            "project_hash": proj.project_hash,
            "cwd": str(proj.cwd),
            "examples": count,
            "snapshot": snap_path.name,
            "ts": time.time(),
        }, indent=2), "utf-8")

        if upload and _have_gsutil():
            _gcs_cp(str(snap_path), f"{proj.gcs_dir}/{snap_path.name}")
            _gcs_cp(str(proj.local_dir / "meta.json"), f"{proj.gcs_dir}/meta.json")
            with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as tmp:
                tmp.write(snap_path.name)
                tmp_path = tmp.name
            _gcs_cp(tmp_path, f"{proj.gcs_dir}/latest.txt")
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        return snap_path

    # ── Sync (from GCS) ──────────────────────────────────────────

    def pull_latest(self, cwd: Path) -> Path | None:
        """Download the latest snapshot from GCS into the local cache."""
        proj = self.project(cwd)
        proj._ensure_local()
        if not _have_gsutil():
            return None
        # Download latest.txt to discover the current snapshot name
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as tmp:
            tmp_path = tmp.name
        ok = _gcs_cp(f"{proj.gcs_dir}/latest.txt", tmp_path)
        if not ok:
            return None
        try:
            snapshot_name = Path(tmp_path).read_text("utf-8").strip()
        except OSError:
            return None
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

        local_snap = proj.local_dir / snapshot_name
        if local_snap.exists():
            return local_snap
        if _gcs_cp(f"{proj.gcs_dir}/{snapshot_name}", str(local_snap)):
            return local_snap
        return None

    # ── Hashing for adapter cache ────────────────────────────────

    @staticmethod
    def corpus_hash(jsonl_path: Path) -> str:
        h = hashlib.sha256()
        try:
            with jsonl_path.open("rb") as fh:
                for chunk in iter(lambda: fh.read(65536), b""):
                    h.update(chunk)
        except OSError:
            pass
        return h.hexdigest()[:16]
