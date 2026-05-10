"""Per-project LoRA hot-swap.

When you `cd` into a project, Sage looks up "is there a LoRA adapter for
this (base_model, project_corpus) in cache?" — if yes, load it; if no,
schedule training in the background. The first turn in a fresh project
is fast (no adapter); subsequent turns get the project-specific weights.

Usage:
    swap = LoraSwap(cfg)
    adapter_path = swap.adapter_for(cwd, base_model="ollama:qwen3-coder-next")
    if adapter_path:
        ... # apply adapter to running model

Adapters are managed by training.cache.AdapterCache (already exists).
This module is the *project-aware lookup* layer on top.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sage.config import SageConfig
from sage.training.cache import AdapterCache, AdapterRef
from sage.training.corpus import CorpusManager

__all__ = ["LoraSwap", "ResolvedAdapter"]


@dataclass
class ResolvedAdapter:
    base_model: str
    corpus_hash: str
    adapter_dir: Path | None
    source: str  # "local" | "gcs" | "missing"


class LoraSwap:
    """Resolve the right adapter for a (base_model, project) pair."""

    def __init__(self, cfg: SageConfig | None = None):
        if cfg is None:
            from sage.config import load_config
            cfg = load_config()
        self.cfg = cfg
        self.cache = AdapterCache(bucket=cfg.gcs_corpus_bucket)
        self.corpus_mgr = CorpusManager(bucket=cfg.gcs_corpus_bucket)

    def _ref_for(self, cwd: Path, base_model: str) -> AdapterRef | None:
        """Build an AdapterRef from (cwd, base) using the latest local corpus."""
        proj = self.corpus_mgr.project(cwd)
        if not proj.latest_local.exists():
            return None
        corpus_hash = CorpusManager.corpus_hash(proj.latest_local)
        bare = base_model.split(":", 1)[-1].split(":")[0]
        return AdapterRef(base_name=bare, corpus_hash=corpus_hash)

    def adapter_for(self, cwd: Path, *, base_model: str) -> ResolvedAdapter:
        """Look up a usable adapter for this project + base model.

        Order: local cache → GCS pull → missing (caller may schedule training).
        """
        ref = self._ref_for(cwd, base_model)
        if ref is None:
            return ResolvedAdapter(
                base_model=base_model, corpus_hash="",
                adapter_dir=None, source="missing",
            )
        if self.cache.has_local(ref):
            return ResolvedAdapter(
                base_model=base_model, corpus_hash=ref.corpus_hash,
                adapter_dir=ref.local_dir(), source="local",
            )
        if self.cache.pull(ref):
            return ResolvedAdapter(
                base_model=base_model, corpus_hash=ref.corpus_hash,
                adapter_dir=ref.local_dir(), source="gcs",
            )
        return ResolvedAdapter(
            base_model=base_model, corpus_hash=ref.corpus_hash,
            adapter_dir=None, source="missing",
        )

    def schedule_training_if_missing(self, cwd: Path, *, base_model: str,
                                     in_background: bool = True) -> ResolvedAdapter:
        """Resolve, and if missing, kick off training (background by default).

        Background scheduling uses a subprocess so the foreground sage run
        isn't blocked. The caller still gets back a ResolvedAdapter — with
        source='missing' and adapter_dir=None — so they know the adapter
        won't be ready for *this* turn but should be available next time.
        """
        resolved = self.adapter_for(cwd, base_model=base_model)
        if resolved.source != "missing":
            return resolved

        import subprocess
        import sys
        cmd = [
            sys.executable, "-m", "sage", "ext", "finetune", base_model,
            "--corpus", "auto",
        ]
        if in_background:
            try:
                subprocess.Popen(
                    cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    cwd=str(cwd),
                )
            except Exception:
                pass
        else:
            subprocess.call(cmd, cwd=str(cwd))
        return resolved
