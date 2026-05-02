"""Model catalog — curated list of free, open-weight models from GitHub.

Reads config/model_catalog.json and exposes model metadata for:
- The download/bootstrap script
- The CLI `ai model catalog` command
- The web UI model browser
- Auto-registration of tracked sources
"""

import json
import logging
from pathlib import Path

from .config import settings

logger = logging.getLogger("ai-platform.catalog")

_BASE = Path(__file__).resolve().parent.parent
_CATALOG_PATH = _BASE / "config" / "model_catalog.json"

_catalog_cache: dict | None = None


def load_catalog() -> dict:
    """Load the model catalog from disk."""
    global _catalog_cache
    if _catalog_cache is not None:
        return _catalog_cache

    if not _CATALOG_PATH.exists():
        logger.warning("No model catalog found at %s", _CATALOG_PATH)
        return {"models": [], "default_models": {}, "recommended_first_download": []}

    try:
        _catalog_cache = json.loads(_CATALOG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        logger.error("Corrupt model catalog at %s: %s", _CATALOG_PATH, e)
        return {"models": [], "default_models": {}, "recommended_first_download": []}
    logger.info("Loaded catalog with %d models", len(_catalog_cache.get("models", [])))
    return _catalog_cache


def list_catalog_models() -> list[dict]:
    """Return all models in the catalog."""
    return load_catalog().get("models", [])


def get_catalog_model(model_id: str) -> dict | None:
    """Get a specific model from the catalog by ID."""
    for m in list_catalog_models():
        if m["model_id"] == model_id:
            return m
    return None


def get_recommended_models() -> list[dict]:
    """Return the recommended first-download models."""
    catalog = load_catalog()
    rec_ids = catalog.get("recommended_first_download", [])
    return [m for m in catalog.get("models", []) if m["model_id"] in rec_ids]


def get_default_model(use_case: str) -> dict | None:
    """Get the default model for a use case (coding, chat, lightweight)."""
    catalog = load_catalog()
    defaults = catalog.get("default_models", {})
    model_id = defaults.get(use_case)
    if model_id:
        return get_catalog_model(model_id)
    return None


def filter_by_ram(max_ram_gb: float) -> list[dict]:
    """Return models that fit within a RAM budget."""
    return [m for m in list_catalog_models() if m.get("min_ram_gb", 0) <= max_ram_gb]


def filter_by_use_case(use_case: str) -> list[dict]:
    """Return models tagged for a specific use case."""
    return [m for m in list_catalog_models() if use_case in m.get("use_case", [])]


def clear_cache() -> None:
    """Clear the catalog cache."""
    global _catalog_cache
    _catalog_cache = None
