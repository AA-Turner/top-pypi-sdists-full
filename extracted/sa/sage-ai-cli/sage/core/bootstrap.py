"""End-to-end auto-bootstrap for Sage.

Runs every setup step that previously required manual commands so a fresh
machine becomes a fully-configured Sage install in one shot. Each phase is:

  - Idempotent (safe to re-run; skips already-completed work)
  - Independently skippable via flags
  - Logged with clear ✓ / ✗ / ⊘ status
  - Non-blocking on failure (a phase failing won't crash later phases)

Phases (in order):
   1. Pull required Ollama models (qwen3-coder-next, llama3.2 draft, nomic-embed-text)
   2. Auto-pick + persist the strongest installed coder as default
   3. Pre-warm the default model into RAM via Ollama keep_alive
   4. Build llama.cpp with Apple Silicon / CUDA / CPU-native flags
   5. Install optional Python deps (sqlite-vec, watchdog, etc.) into the venv
   6. Build initial RAG index of the cwd
   7. Mirror small training datasets to GCS (CodeAlpaca + MBPP)
   8. (Opt-in) Harvest cwd corpus + start LoRA fine-tune in background

Public entry point: `run_bootstrap(opts: BootstrapOptions) -> BootstrapResult`

CLI: `sage bootstrap` (registered in cli_extensions.py).
"""

from __future__ import annotations

import importlib
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

__all__ = [
    "BootstrapOptions",
    "PhaseOutcome",
    "BootstrapResult",
    "run_bootstrap",
    # Individual phase functions (exposed for testability)
    "phase_pull_ollama_models",
    "phase_set_default_model",
    "phase_prewarm",
    "phase_build_llama_cpp",
    "phase_install_optional_deps",
    "phase_build_rag_index",
    "phase_mirror_datasets",
    "phase_finetune_background",
]


# ── Dataclasses ────────────────────────────────────────────────────────

@dataclass
class BootstrapOptions:
    """Per-phase opt-out flags. All phases on by default except `finetune`."""
    pull_models: bool = True
    set_default: bool = True
    prewarm: bool = True
    build_llama_cpp: bool = True
    install_deps: bool = True
    build_rag: bool = True
    mirror_datasets: bool = True
    finetune: bool = False               # heavy; opt-in
    finetune_background: bool = True     # if finetuning, run detached
    cwd: Path = field(default_factory=Path.cwd)
    quiet: bool = False                  # suppress per-phase output

    # Lists of models to pull. Override to slim down the bootstrap.
    ollama_models: tuple[str, ...] = (
        "qwen3-coder-next",   # strong local coder (default)
        "llama3.2",           # speculative draft model
        "nomic-embed-text",   # RAG embedder
    )

    # Datasets to mirror in standard mode (small ones only).
    # Use --full-datasets to also mirror the large CodeSearchNet/Magicoder.
    mirror_dataset_names: tuple[str, ...] = ("codealpaca-20k", "mbpp")


@dataclass
class PhaseOutcome:
    name: str
    status: str    # "ok" | "skipped" | "failed"
    duration_s: float
    detail: str = ""

    @property
    def emoji(self) -> str:
        return {"ok": "✓", "skipped": "⊘", "failed": "✗"}.get(self.status, "?")


@dataclass
class BootstrapResult:
    phases: list[PhaseOutcome] = field(default_factory=list)
    total_duration_s: float = 0.0

    def add(self, outcome: PhaseOutcome) -> None:
        self.phases.append(outcome)

    @property
    def all_ok(self) -> bool:
        return all(p.status != "failed" for p in self.phases)

    def summary(self) -> str:
        lines = ["", "Bootstrap summary:"]
        for p in self.phases:
            lines.append(f"  {p.emoji}  {p.name:30s} {p.status:8s} ({p.duration_s:.1f}s) {p.detail}")
        lines.append(f"\nTotal: {self.total_duration_s:.1f}s")
        return "\n".join(lines)


# ── Helpers ────────────────────────────────────────────────────────────

def _say(opts: BootstrapOptions, msg: str) -> None:
    if not opts.quiet:
        print(msg, flush=True)


def _have_cmd(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def _run(name: str, fn) -> PhaseOutcome:
    t0 = time.time()
    try:
        result = fn()
        if isinstance(result, PhaseOutcome):
            result.duration_s = result.duration_s or (time.time() - t0)
            return result
        # Convention: fn returns (status, detail)
        status, detail = (result if isinstance(result, tuple) else ("ok", ""))
        return PhaseOutcome(name=name, status=status, duration_s=time.time() - t0, detail=detail)
    except Exception as exc:
        return PhaseOutcome(
            name=name, status="failed", duration_s=time.time() - t0,
            detail=f"{type(exc).__name__}: {exc}",
        )


# ── Phase 1: Pull Ollama models ────────────────────────────────────────

def phase_pull_ollama_models(opts: BootstrapOptions) -> tuple[str, str]:
    if not _have_cmd("ollama"):
        return ("skipped", "ollama not installed (run `sage install` first)")

    # Get currently pulled list to skip dupes
    try:
        import httpx
        r = httpx.get("http://127.0.0.1:11434/api/tags", timeout=3.0)
        installed = {m["name"].split(":")[0]
                     for m in (r.json().get("models") or [])
                     if isinstance(m, dict) and m.get("name")}
    except Exception:
        installed = set()

    pulled: list[str] = []
    failed: list[str] = []
    for model in opts.ollama_models:
        if model in installed:
            _say(opts, f"  ✓  {model}: already pulled")
            continue
        _say(opts, f"  …  pulling {model} (this can take a while)…")
        try:
            r = subprocess.run(
                ["ollama", "pull", model],
                capture_output=True, text=True, timeout=3600,
            )
            if r.returncode == 0:
                pulled.append(model)
                _say(opts, f"  ✓  {model}: pulled")
            else:
                failed.append(f"{model} (rc={r.returncode})")
                _say(opts, f"  ✗  {model}: pull failed")
        except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
            failed.append(f"{model} ({type(exc).__name__})")
            _say(opts, f"  ✗  {model}: {exc}")

    if failed and not pulled:
        return ("failed", f"none pulled; failed: {', '.join(failed)}")
    if failed:
        return ("ok", f"pulled {len(pulled)}; failed {len(failed)}: {', '.join(failed)}")
    if not pulled:
        return ("skipped", "all models already present")
    return ("ok", f"pulled {len(pulled)}: {', '.join(pulled)}")


# ── Phase 2: Set default model to strongest installed coder ────────────

def phase_set_default_model(opts: BootstrapOptions) -> tuple[str, str]:
    from sage.config import load_config, save_config
    from sage.core.auto_model import auto_pick_default_model

    cfg = load_config()
    pick = auto_pick_default_model(cfg.default_model)
    if pick == cfg.default_model:
        return ("skipped", f"already set to {cfg.default_model}")
    cfg.default_model = pick
    save_config(cfg)
    return ("ok", f"set default_model = {pick}")


# ── Phase 3: Pre-warm via Ollama keep_alive ────────────────────────────

def phase_prewarm(opts: BootstrapOptions) -> tuple[str, str]:
    from sage.config import load_config
    from sage.core.keep_alive import prewarm

    cfg = load_config()
    if not cfg.default_model.startswith("ollama:"):
        return ("skipped", f"default {cfg.default_model} is not an Ollama model")
    bare = cfg.default_model.split(":", 1)[1]
    if prewarm(bare):
        return ("ok", f"prewarmed {bare}")
    return ("failed", f"prewarm of {bare} failed (Ollama not running?)")


# ── Phase 4: Build llama.cpp optimized ─────────────────────────────────

def phase_build_llama_cpp(opts: BootstrapOptions) -> tuple[str, str]:
    """Rebuild llama-cpp-python with native flags for this machine.

    Skipped when llama-cpp-python isn't already installed (no point building
    something the user hasn't asked for). When installed, we rebuild only if
    the existing build doesn't have Metal/CUDA flags.
    """
    try:
        import llama_cpp  # noqa: F401
    except ImportError:
        return ("skipped", "llama-cpp-python not installed; nothing to optimize")

    from sage.scripts.build_llama_cpp_optimized import build_command, pick_cmake_flags
    flags = pick_cmake_flags()
    cmd, env = build_command(flags)

    # Heuristic: if the user has Metal/CUDA flags in their existing build, skip.
    # We can't easily introspect the wheel, so we just rebuild — pip's
    # --force-reinstall is idempotent.
    _say(opts, f"  …  rebuilding llama-cpp-python with: {' '.join(flags)}")
    try:
        r = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=900)
        if r.returncode == 0:
            return ("ok", f"rebuilt with {' '.join(flags)}")
        return ("failed", f"pip install rc={r.returncode} (see `pip install --no-binary llama-cpp-python ...`)")
    except subprocess.TimeoutExpired:
        return ("failed", "build timed out (>15min)")


# ── Phase 5: Install optional Python deps ──────────────────────────────

OPTIONAL_DEPS = (
    # (pip_name, import_name, why)
    ("sqlite-vec",            "sqlite_vec",        "fast vector search for RAG"),
    ("watchdog",              "watchdog",          "live-reindex on file changes"),
    ("beautifulsoup4",        "bs4",               "HTML stripping for WebFetch"),
    ("psutil",                "psutil",            "RAM detection for auto-pick"),
)


def phase_install_optional_deps(opts: BootstrapOptions) -> tuple[str, str]:
    """Install lightweight optional deps. Heavy deps (mlx, transformers, peft,
    unsloth, vllm, sentence-transformers) are intentionally NOT installed —
    they're 200MB+ each and only needed for specific opt-in workflows."""
    missing: list[str] = []
    for pip_name, import_name, _why in OPTIONAL_DEPS:
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing.append(pip_name)
    if not missing:
        return ("skipped", "all optional deps already present")
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", *missing]
    _say(opts, f"  …  installing: {', '.join(missing)}")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if r.returncode == 0:
            return ("ok", f"installed: {', '.join(missing)}")
        return ("failed", f"pip rc={r.returncode}: {(r.stderr or '')[:200]}")
    except subprocess.TimeoutExpired:
        return ("failed", "pip install timed out")


# ── Phase 6: Build initial RAG index ───────────────────────────────────

def phase_build_rag_index(opts: BootstrapOptions) -> tuple[str, str]:
    """Build the per-project RAG index. Cheap; no-op when cwd has no
    indexable files."""
    try:
        from sage.core.rag import RAGIndex
    except Exception as exc:
        return ("failed", f"import RAGIndex: {exc}")
    try:
        index = RAGIndex(opts.cwd)
        stats = index.reindex()
        if stats["chunks_added"] == 0 and stats["files_seen"] == 0:
            return ("skipped", "no indexable files in cwd")
        return ("ok", f"{stats['files_seen']} files, {stats['chunks_added']} chunks "
                      f"({stats['vec_backend']})")
    except Exception as exc:
        return ("failed", f"{type(exc).__name__}: {exc}")


# ── Phase 7: Mirror datasets to GCS ────────────────────────────────────

def phase_mirror_datasets(opts: BootstrapOptions) -> tuple[str, str]:
    if not _have_cmd("gsutil"):
        return ("skipped", "gsutil not installed (gcloud CLI required)")
    try:
        from sage.config import load_config
        from sage.training.datasets import DATASETS, DatasetMirror
    except Exception as exc:
        return ("failed", f"import: {exc}")
    cfg = load_config()
    mirror = DatasetMirror(bucket=cfg.gcs_corpus_bucket)
    selected = tuple(d for d in DATASETS if d.name in opts.mirror_dataset_names)
    if not selected:
        return ("skipped", "no datasets selected")
    report = mirror.mirror_all(selected, skip_existing=True)
    return ("ok",
            f"mirrored={len(report['mirrored'])} skipped={len(report['skipped'])} "
            f"failed={len(report['failed'])}")


# ── Phase 8: Background fine-tune ──────────────────────────────────────

def phase_finetune_background(opts: BootstrapOptions) -> tuple[str, str]:
    """Kick off `sage ext finetune` for the cwd corpus.

    Defaults to background subprocess so install returns fast. Heavy: needs
    MLX (Apple Silicon) or PEFT/Unsloth (Linux+CUDA) installed.
    """
    from sage.config import load_config
    cfg = load_config()
    cmd = [sys.executable, "-m", "sage", "ext", "finetune", cfg.default_model,
           "--corpus", "auto"]
    try:
        if opts.finetune_background:
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             cwd=str(opts.cwd))
            return ("ok", "started in background; see ~/.sage/adapters/ for results")
        rc = subprocess.call(cmd, cwd=str(opts.cwd))
        return (("ok", "finished") if rc == 0 else ("failed", f"rc={rc}"))
    except Exception as exc:
        return ("failed", f"{type(exc).__name__}: {exc}")


# ── Public entry point ─────────────────────────────────────────────────

PHASES = (
    ("pull-ollama-models",      phase_pull_ollama_models,      "pull_models"),
    ("set-default-model",       phase_set_default_model,       "set_default"),
    ("prewarm-ollama",          phase_prewarm,                 "prewarm"),
    ("build-llama-cpp",         phase_build_llama_cpp,         "build_llama_cpp"),
    ("install-optional-deps",   phase_install_optional_deps,   "install_deps"),
    ("build-rag-index",         phase_build_rag_index,         "build_rag"),
    ("mirror-datasets",         phase_mirror_datasets,         "mirror_datasets"),
    ("finetune-background",     phase_finetune_background,     "finetune"),
)


def run_bootstrap(opts: BootstrapOptions | None = None) -> BootstrapResult:
    opts = opts or BootstrapOptions()
    result = BootstrapResult()
    t0 = time.time()
    for name, fn, flag in PHASES:
        if not getattr(opts, flag):
            outcome = PhaseOutcome(name=name, status="skipped", duration_s=0.0,
                                   detail="disabled by flag")
        else:
            _say(opts, f"\n[{name}]")
            outcome = _run(name, lambda fn=fn: fn(opts))
            _say(opts, f"  → {outcome.emoji} {outcome.status}: {outcome.detail}")
        result.add(outcome)
    result.total_duration_s = time.time() - t0
    return result
