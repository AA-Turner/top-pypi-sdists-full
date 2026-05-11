"""TC — Per-project LoRA hot-swap."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

__all__ = ["LoraSwap", "ResolvedAdapter"]


@dataclass
class ResolvedAdapter:
    base_model: str
    corpus_hash: str
    adapter_dir: Path | None
    source: str  # "local" | "gcs" | "missing"


class LoraSwap:
    def __init__(self, cfg=None):
        if cfg is None:
            from sage.config import load_config
            cfg = load_config()
        self.cfg = cfg
        try:
            from sage.training.cache import AdapterCache
            from sage.training.corpus import CorpusManager
            self.cache = AdapterCache(bucket=cfg.gcs_corpus_bucket)
            self.corpus_mgr = CorpusManager(bucket=cfg.gcs_corpus_bucket)
        except Exception:
            self.cache = None
            self.corpus_mgr = None

    def _ref_for(self, cwd: Path, base_model: str):
        if self.corpus_mgr is None:
            return None
        from sage.training.cache import AdapterRef
        from sage.training.corpus import CorpusManager
        proj = self.corpus_mgr.project(cwd)
        if not proj.latest_local.exists():
            return None
        corpus_hash = CorpusManager.corpus_hash(proj.latest_local)
        bare = base_model.split(":", 1)[-1].split(":")[0]
        return AdapterRef(base_name=bare, corpus_hash=corpus_hash)

    def adapter_for(self, cwd: Path, *, base_model: str) -> ResolvedAdapter:
        ref = self._ref_for(cwd, base_model)
        if ref is None or self.cache is None:
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
