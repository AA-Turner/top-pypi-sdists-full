"""Auto-pick the best installed local model for Sage.

The default in config.py is `llama_cpp:llama3.2-3b` — fine as a fallback,
but if the user has pulled a larger coding-specialist model (qwen3-coder,
deepseek-coder, codestral, devstral, codellama, starcoder), we should
prefer it for `sage run` instead of forcing them to remember `sage use`.

Scoring rules:
  +100  for a coding-specialist family
  +size_gb  for raw capability (capped at 80, so a 405B doesn't dominate
            unrealistically when RAM is tight)
   −40  if the model won't fit in available RAM (heuristic: model_gb < ram_gb * 0.7)
   −5   if the model is currently running on Ollama (slight tie-breaker)

Returns a fully-qualified model id like "ollama:qwen3-coder-next" or
"llama_cpp:qwen2.5-coder-3b" — same shape config.default_model expects.
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "Candidate",
    "list_installed_models",
    "pick_best_coder",
    "auto_pick_default_model",
]


_CODER_FAMILIES = (
    "qwen3-coder", "qwen2.5-coder", "qwen-coder",
    "deepseek-coder", "deepseek-v2-coder",
    "codellama", "codestral", "devstral",
    "starcoder", "starcoder2",
    "phind-codellama", "wizardcoder",
)


@dataclass(frozen=True)
class Candidate:
    """A locally installed model we can route to."""
    qualified_id: str       # "ollama:qwen3-coder-next" or "llama_cpp:qwen2.5-coder-3b"
    backend: str            # "ollama" | "llama_cpp"
    base_name: str          # "qwen3-coder-next"
    size_gb: float
    is_coder: bool

    @property
    def score(self) -> float:
        s = min(self.size_gb, 80.0)
        if self.is_coder:
            s += 100.0
        return s


def _is_coder(name: str) -> bool:
    n = name.lower()
    return any(fam in n for fam in _CODER_FAMILIES)


def _available_ram_gb() -> float:
    """Best-effort available RAM in GB; conservative fallback if probe fails."""
    try:
        import psutil  # type: ignore
        return float(psutil.virtual_memory().available) / (1024 ** 3)
    except Exception:
        pass
    # Last-resort: parse uname/sysctl. If everything fails, assume 16 GB.
    try:
        if os.uname().sysname == "Darwin":
            out = subprocess.run(
                ["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, timeout=2,
            )
            if out.returncode == 0:
                return int(out.stdout.strip()) / (1024 ** 3)
    except Exception:
        pass
    return 16.0


def _ollama_models() -> list[Candidate]:
    """Query Ollama for installed models. Returns [] if Ollama isn't running."""
    try:
        import httpx
        r = httpx.get("http://127.0.0.1:11434/api/tags", timeout=2.0)
        if r.status_code != 200:
            return []
        models = r.json().get("models") or []
    except Exception:
        return []

    out: list[Candidate] = []
    for m in models:
        if not isinstance(m, dict):
            continue
        full_name = m.get("name") or ""
        if not full_name:
            continue
        base = full_name.split(":")[0]
        size_bytes = int(m.get("size") or 0)
        size_gb = size_bytes / (1024 ** 3)
        out.append(Candidate(
            qualified_id=f"ollama:{full_name}",
            backend="ollama",
            base_name=base,
            size_gb=size_gb,
            is_coder=_is_coder(base),
        ))
    return out


def _llama_cpp_models(models_dir: Path) -> list[Candidate]:
    """Scan ~/.sage/models/*.gguf."""
    if not models_dir.is_dir():
        return []
    out: list[Candidate] = []
    for p in models_dir.glob("*.gguf"):
        try:
            sz = p.stat().st_size / (1024 ** 3)
        except OSError:
            continue
        if sz < 0.05:  # Skip empty/partial downloads
            continue
        name = p.stem
        out.append(Candidate(
            qualified_id=f"llama_cpp:{name}",
            backend="llama_cpp",
            base_name=name,
            size_gb=sz,
            is_coder=_is_coder(name),
        ))
    return out


def list_installed_models(models_dir: Path | None = None) -> list[Candidate]:
    """All locally installed models across both backends."""
    if models_dir is None:
        models_dir = Path.home() / ".sage" / "models"
    return _ollama_models() + _llama_cpp_models(models_dir)


def pick_best_coder(
    candidates: list[Candidate] | None = None,
    available_ram_gb: float | None = None,
) -> Candidate | None:
    """Pick the best coder model that fits in RAM. Returns None if nothing usable.

    Apple Silicon / Linux mmap behaviour: models 2-3x larger than free RAM
    still run via OS paging. Ollama in particular handles oversize models
    gracefully. We trust Ollama-served models regardless of size and only
    apply the RAM filter to llama_cpp models (which load weights eagerly).
    """
    if candidates is None:
        candidates = list_installed_models()
    if not candidates:
        return None
    if available_ram_gb is None:
        available_ram_gb = _available_ram_gb()

    # Generous cap: total system RAM × 1.5. mmap + swap can absorb
    # the rest. Models bigger than that genuinely won't load.
    cap = available_ram_gb * 1.5
    fits = [
        c for c in candidates
        if c.backend == "ollama" or c.size_gb <= cap
    ]
    pool = fits or candidates
    return max(pool, key=lambda c: c.score)


def auto_pick_default_model(current_default: str = "") -> str:
    """Return the qualified model id to use as default.

    Honours the existing default if the user has explicitly set one to a
    coder model — we don't want to override a deliberate choice. Otherwise,
    we pick the strongest installed coder model.
    """
    # If user has already chosen a coder model, leave it alone.
    if current_default:
        bare = re.sub(r"^[a-z_]+:", "", current_default).split(":")[0].lower()
        if _is_coder(bare):
            return current_default

    pick = pick_best_coder()
    if pick is None:
        return current_default or "llama_cpp:llama3.2-3b"
    return pick.qualified_id
