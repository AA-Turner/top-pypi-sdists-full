"""Adapter cache: don't retrain when (base, corpus) pair already exists.

Layout:
  Local:  ~/.sage/adapters/<base_name>/<corpus_hash>/
  GCS:    <bucket>/adapters/<base_name>/<corpus_hash>/

Each adapter dir contains:
  adapter.safetensors  — the LoRA weights
  config.json          — training config snapshot
  README.md            — provenance (base model, corpus, steps, time)

The cache is the cost-control linchpin. With 200+ models and N projects, we
do NOT want to retrain on every invocation. Instead, every (base_model,
corpus_hash) pair is content-addressed — same inputs ⇒ same adapter ⇒
download instead of train.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path

__all__ = ["AdapterRef", "AdapterCache"]


@dataclass(frozen=True)
class AdapterRef:
    base_name: str
    corpus_hash: str

    def local_dir(self) -> Path:
        return Path.home() / ".sage" / "adapters" / self.base_name / self.corpus_hash

    def gcs_dir(self, bucket: str) -> str:
        return f"{bucket}/adapters/{self.base_name}/{self.corpus_hash}"


@dataclass
class AdapterMeta:
    base_name: str
    corpus_hash: str
    steps: int
    created_ts: float
    train_seconds: float
    backend: str  # "mlx" | "unsloth" | "peft"
    notes: str = ""


class AdapterCache:
    def __init__(self, bucket: str = "gs://sage-ai-models"):
        self.bucket = bucket

    def has_local(self, ref: AdapterRef) -> bool:
        return (ref.local_dir() / "adapter.safetensors").is_file()

    def has_remote(self, ref: AdapterRef) -> bool:
        try:
            out = subprocess.run(
                ["gsutil", "ls", f"{ref.gcs_dir(self.bucket)}/adapter.safetensors"],
                capture_output=True, text=True, timeout=15,
            )
            return out.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def pull(self, ref: AdapterRef) -> bool:
        """Download adapter from GCS if available."""
        if not self.has_remote(ref):
            return False
        ref.local_dir().mkdir(parents=True, exist_ok=True)
        try:
            out = subprocess.run(
                ["gsutil", "-q", "-m", "cp", "-r",
                 f"{ref.gcs_dir(self.bucket)}/*", str(ref.local_dir()) + "/"],
                capture_output=True, text=True, timeout=300,
            )
            return out.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def push(self, ref: AdapterRef, meta: AdapterMeta) -> bool:
        """Upload locally trained adapter to GCS for future reuse."""
        local = ref.local_dir()
        if not (local / "adapter.safetensors").is_file():
            return False
        # Persist meta
        (local / "meta.json").write_text(json.dumps(asdict(meta), indent=2), "utf-8")
        try:
            out = subprocess.run(
                ["gsutil", "-q", "-m", "cp", "-r",
                 str(local) + "/", ref.gcs_dir(self.bucket)],
                capture_output=True, text=True, timeout=600,
            )
            return out.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def get_or_resolve(self, ref: AdapterRef) -> Path | None:
        """Return path to a usable adapter, pulling from GCS if needed.

        Caller-side cheap-vs-expensive decision lives here:
          1. Local hit → free
          2. Remote hit → pull (cents in egress, seconds of download)
          3. Miss → caller must train
        """
        if self.has_local(ref):
            return ref.local_dir()
        if self.pull(ref):
            return ref.local_dir()
        return None
