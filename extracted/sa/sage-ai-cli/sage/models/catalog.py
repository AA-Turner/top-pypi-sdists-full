"""Curated catalog of downloadable models for local inference.

Supports two backends:
- GGUF: Direct HuggingFace downloads for llama.cpp inference
- Ollama: Models pulled via `ollama pull` command

Auto-update: On startup, clients fetch gs://sage-ai-models/catalog.json
for the latest models. Falls back to the hardcoded catalog below.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path


from sage.models.catalog_base import CatalogModel, _gcs_url, _hf_url, GCS_BUCKET
from sage.models.catalog_part1 import MODEL_CATALOG_PART1
from sage.models.catalog_part2 import MODEL_CATALOG_PART2

MODEL_CATALOG: list[CatalogModel] = MODEL_CATALOG_PART1 + MODEL_CATALOG_PART2

# Quick lookup by name
CATALOG_BY_NAME: dict[str, CatalogModel] = {m.name: m for m in MODEL_CATALOG}


def search_catalog(query: str) -> list[CatalogModel]:
    """Search the catalog by name, family, or description."""
    q = query.lower()
    return [
        m for m in MODEL_CATALOG
        if q in m.name.lower()
        or q in m.family.lower()
        or q in m.display_name.lower()
        or q in m.description.lower()
    ]


def get_recommended_models() -> list[CatalogModel]:
    """Return a curated list of recommended starter models (GGUF)."""
    recs = ["qwen2.5-coder-7b", "deepseek-r1-7b", "llama3.2-3b", "qwen2.5-coder-3b"]
    return [CATALOG_BY_NAME[n] for n in recs if n in CATALOG_BY_NAME]


# ── Ollama catalog helpers ─────────────────────────────────
# Work against MODEL_CATALOG entries with backend="ollama".

# For backwards compat, OllamaModel is just CatalogModel
OllamaModel = CatalogModel


OLLAMA_CATALOG: list[CatalogModel] = [
    m for m in MODEL_CATALOG if m.backend == "ollama"
]

OLLAMA_BY_NAME: dict[str, CatalogModel] = {
    m.name: m for m in OLLAMA_CATALOG
}
# Strip "ollama:" prefix for alternate lookup
OLLAMA_BY_NAME.update({
    m.name.removeprefix("ollama:"): m for m in OLLAMA_CATALOG
})


def search_ollama_catalog(query: str) -> list[CatalogModel]:
    """Search the Ollama catalog by name, category, or description."""
    q = query.lower()
    return [
        m for m in OLLAMA_CATALOG
        if q in m.name.lower()
        or q in m.category.lower()
        or q in m.display_name.lower()
        or q in m.description.lower()
    ]


def get_recommended_ollama_models() -> list[CatalogModel]:
    """Return recommended Ollama models for Sage — the best available."""
    recs = [
        "ollama:qwen3.5",          # Alibaba's latest flagship
        "ollama:gemma4",            # Google's best
        "ollama:glm-5.1",          # Z.ai's best coding agent
        "ollama:devstral",          # Mistral's best coding agent
        "ollama:nemotron-mini",     # NVIDIA's fast reasoning
        "ollama:qwen3",             # Strong all-around
        "ollama:deepseek-r1",       # Best open reasoning
        "ollama:mistral-small",     # Efficient general purpose
        "ollama:phi4-mini",         # Microsoft's small powerhouse
        "ollama:minimax-m2.7",      # MiniMax's best for coding
    ]
    return [CATALOG_BY_NAME[n] for n in recs if n in CATALOG_BY_NAME]


def get_ollama_models_by_category(category: str) -> list[CatalogModel]:
    """Filter Ollama catalog by category."""
    return [m for m in OLLAMA_CATALOG if m.category == category]


def get_default_models() -> list[CatalogModel]:
    """Return models that should be installed by default.
    These are the best models for coding that run well on most hardware.
    GGUF defaults (~11.4 GB): qwen2.5-coder-7b, deepseek-r1-7b, llama3.2-3b
    """
    return [m for m in MODEL_CATALOG if m.default and m.backend == "gguf"]


# Best Ollama models to pre-pull on `sage install`
DEFAULT_OLLAMA_MODELS = [
    "qwen3.5",          # Alibaba's latest flagship — best overall
    "gemma4",           # Google's best — strong reasoning + coding
    "devstral",         # Mistral's best coding agent model
    "nemotron-mini",    # NVIDIA's fast reasoning model
    "deepseek-r1:7b",  # Best open reasoning model
    "phi4-mini",        # Microsoft's strong small model
    "mistral-small",    # Mistral's efficient general model
    "qwen3",            # Alibaba Qwen 3 — strong all-around
]


# Best model rankings for display and recommendations
BEST_MODELS_RANKED = [
    # Tier 1: State-of-the-art (latest flagships)
    "qwen3.5", "gemma4", "devstral", "qwen3",
    # Tier 2: Best reasoning + coding agents
    "deepseek-r1:7b", "nemotron-mini", "mistral-small", "phi4-mini",
    # Tier 3: Best dedicated coding
    "qwen2.5-coder-7b", "codegemma", "deepcoder",
    # Tier 4: General purpose
    "llama3.2-3b", "llama3.1-8b", "qwen2.5-7b",
]


DEFAULT_MODEL_NAME = "qwen2.5-coder-7b"


# ── Remote catalog auto-update ────────────────────────────

GCS_CATALOG_URL = "https://storage.googleapis.com/sage-ai-models/catalog.json"
_CACHE_DIR = Path.home() / ".sage" / "cache"
_CACHE_FILE = _CACHE_DIR / "catalog.json"
_CACHE_TTL_SECONDS = 3600  # 1 hour


def _dict_to_model(d: dict) -> CatalogModel:
    return CatalogModel(
        name=d["name"],
        display_name=d.get("display_name", d["name"]),
        filename=d.get("filename", ""),
        url=d.get("url", ""),
        size_gb=d.get("size_gb", 0),
        params=d.get("params", ""),
        family=d.get("family", ""),
        description=d.get("description", ""),
        backend=d.get("backend", "gguf"),
        tags=tuple(d.get("tags", ())),
        category=d.get("category", "general"),
        default=d.get("default", False),
    )


def fetch_remote_catalog(force: bool = False) -> list[CatalogModel] | None:
    """Fetch the latest catalog from GCS with local cache.

    Returns a list of CatalogModel if successful, or None to use the
    hardcoded catalog as fallback.
    """
    # Check cache first
    if not force and _CACHE_FILE.exists():
        age = time.time() - _CACHE_FILE.stat().st_mtime
        if age < _CACHE_TTL_SECONDS:
            try:
                data = json.loads(_CACHE_FILE.read_text())
                return [_dict_to_model(m) for m in data.get("models", [])]
            except (json.JSONDecodeError, KeyError):
                pass  # Corrupted cache, fetch fresh

    # Fetch from GCS
    try:
        import httpx
        resp = httpx.get(GCS_CATALOG_URL, timeout=10, follow_redirects=True)
        resp.raise_for_status()
        data = resp.json()

        # Cache it
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _CACHE_FILE.write_text(json.dumps(data, indent=2))

        return [_dict_to_model(m) for m in data.get("models", [])]
    except Exception:
        # Network failure — try stale cache
        if _CACHE_FILE.exists():
            try:
                data = json.loads(_CACHE_FILE.read_text())
                return [_dict_to_model(m) for m in data.get("models", [])]
            except (json.JSONDecodeError, KeyError):
                pass

    return None  # Use hardcoded catalog


def get_full_catalog() -> list[CatalogModel]:
    """Return the best available catalog: remote > cache > hardcoded."""
    remote = fetch_remote_catalog()
    if not remote:
        return MODEL_CATALOG
    
    # Merge remote over hardcoded (remote wins on name collision)
    merged = {m.name: m for m in MODEL_CATALOG}
    for m in remote:
        merged[m.name] = m
    return list(merged.values())


def refresh_catalog_from_remote(*, background: bool = False, force: bool = False) -> int:
    """Merge any new entries from the public GCS catalog into the live module
    state (``MODEL_CATALOG``, ``OLLAMA_CATALOG``, ``CATALOG_BY_NAME``,
    ``OLLAMA_BY_NAME``) so users see the latest models without a SAGE upgrade.

    The hardcoded catalog stays as the floor — remote entries with new names
    are appended; remote entries that match an existing name overwrite the
    hardcoded version (so the maintainer can fix size/url/description from
    GCS without code changes).

    Args:
        background: If True, run the fetch on a daemon thread and return
            immediately. Used at sage startup so the network call never
            blocks ``sage --help``.
        force: Bypass the 1-hour local cache.

    Returns:
        The number of models added (0 if the fetch failed or there was no
        new content). When ``background=True`` always returns 0 — the caller
        cannot wait for the result.
    """

    def _do_refresh() -> int:
        try:
            remote = fetch_remote_catalog(force=force)
        except Exception:
            return 0
        if not remote:
            return 0

        added = 0
        for entry in remote:
            existing = CATALOG_BY_NAME.get(entry.name)
            if existing is None:
                MODEL_CATALOG.append(entry)
                added += 1
            elif existing != entry:
                # Replace stale entry in MODEL_CATALOG and OLLAMA_CATALOG.
                for i, m in enumerate(MODEL_CATALOG):
                    if m.name == entry.name:
                        MODEL_CATALOG[i] = entry
                        break
                for i, m in enumerate(OLLAMA_CATALOG):
                    if m.name == entry.name:
                        OLLAMA_CATALOG[i] = entry
                        break
            CATALOG_BY_NAME[entry.name] = entry
            if entry.backend == "ollama":
                OLLAMA_BY_NAME[entry.name] = entry
                OLLAMA_BY_NAME[entry.name.removeprefix("ollama:")] = entry
                if entry not in OLLAMA_CATALOG:
                    OLLAMA_CATALOG.append(entry)
        return added

    if not background:
        return _do_refresh()

    import threading

    threading.Thread(target=_do_refresh, daemon=True, name="sage-catalog-refresh").start()
    return 0

