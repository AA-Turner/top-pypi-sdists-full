"""Dynamic OpenRouter free-model catalog.

OpenRouter's free model list churns weekly — new models get added, old
ones get promoted to paid tier, experimental models come and go. A
hardcoded list goes stale fast.

This module fetches the live model list from
`https://openrouter.ai/api/v1/models`, filters to models with
`pricing.prompt == 0 AND pricing.completion == 0` (the truly free ones,
not just discounted), and caches the result to `~/.sage/cache/`.
Refreshed once per 24h by default.

Falls back to a small hardcoded "essentials" list if the API is down,
so sage stays usable offline.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from sage.providers.base import ModelInfo


# Where the cached catalog lives (refreshed daily)
_CACHE_PATH = Path.home() / ".sage" / "cache" / "openrouter_free_models.json"
_CACHE_TTL_SECONDS = 24 * 3600  # 24 hours


# Minimal fallback set so sage works offline / when API fails. These IDs
# have been stable for months; if any becomes paid we just stop using it
# and the rate-limited error tells the user to swap.
_FALLBACK_FREE_IDS: tuple[str, ...] = (
    "qwen/qwen3-coder:free",
    "qwen/qwen-2.5-coder-32b-instruct:free",
    "deepseek/deepseek-r1:free",
    "deepseek/deepseek-chat-v3-0324:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "google/gemini-2.0-flash-exp:free",
    "google/gemma-3-27b-it:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
    "qwen/qwen3-235b-a22b:free",
    "meta-llama/llama-3.2-3b-instruct:free",
)


# Keywords → category for prose generation in `name`/`description`
_CATEGORY_KEYWORDS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bcoder?\b", re.I), "Coder"),
    (re.compile(r"\bcodellama\b|deepcoder|codestral", re.I), "Coder"),
    (re.compile(r"\bvision\b|\bvl\b|multimodal", re.I), "Vision"),
    (re.compile(r"\br1\b|reasoning|qwq|think", re.I), "Reasoning"),
    (re.compile(r"\bflash\b|nano|mini|small|1\.?5b|1\.?7b|3b|7b|8b", re.I), "Fast"),
)


def _humanize_id(model_id: str) -> str:
    """`qwen/qwen-2.5-coder-32b-instruct:free` → `Qwen 2.5 Coder 32B (Free)`."""
    base = model_id.split("/", 1)[-1].removesuffix(":free")
    # Convert dashes to spaces, capitalize
    parts = [p.capitalize() if not re.match(r"^[\d.]+b?$", p, re.I) else p.upper()
             for p in base.split("-")]
    name = " ".join(parts)
    if model_id.endswith(":free"):
        name += " (Free)"
    return name


def _category_for(model: dict) -> str:
    """Classify a model for sage's table — returns one-liner."""
    blob = " ".join([
        model.get("id", ""),
        model.get("name", "") or "",
        model.get("description", "") or "",
    ])
    matches = []
    for pat, label in _CATEGORY_KEYWORDS:
        if pat.search(blob):
            matches.append(label)
    return ", ".join(matches) or "General"


def _model_dict_to_info(model: dict) -> dict:
    """Convert OpenRouter API model entry to ModelInfo-compatible dict."""
    return {
        "id": model["id"],
        "provider": "openrouter",
        "name": _humanize_id(model["id"]),
        "local": False,
        "description": (model.get("description") or "")[:200],
        "pros": _category_for(model),
        "cons": "Rate limited (free tier)",
    }


def _is_free(model: dict) -> bool:
    """True if both prompt + completion price are zero."""
    pricing = model.get("pricing", {})
    try:
        prompt = float(pricing.get("prompt", "1") or "1")
        completion = float(pricing.get("completion", "1") or "1")
    except (ValueError, TypeError):
        return False
    return prompt == 0 and completion == 0


def _read_cache() -> list[dict] | None:
    """Return cached models if fresh, else None."""
    if not _CACHE_PATH.exists():
        return None
    age = time.time() - _CACHE_PATH.stat().st_mtime
    if age >= _CACHE_TTL_SECONDS:
        return None
    try:
        return json.loads(_CACHE_PATH.read_text("utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _write_cache(models: list[dict]) -> None:
    try:
        _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        _CACHE_PATH.write_text(json.dumps(models, indent=2), encoding="utf-8")
    except OSError:
        pass  # Cache is an optimization — never crash on cache failures


def _fetch_live(api_key: str | None, timeout: float) -> list[dict] | None:
    """Hit OpenRouter's /models endpoint. Return list of model dicts or None."""
    try:
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        response = httpx.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers,
            timeout=timeout,
        )
        response.raise_for_status()
        data = response.json().get("data") or []
        if not isinstance(data, list):
            return None
        return [m for m in data if isinstance(m, dict) and "id" in m]
    except Exception:  # noqa: BLE001 — network/parse errors must never crash startup
        return None


def fetch_free_models(
    api_key: str | None = None,
    *,
    timeout: float = 5.0,
    force_refresh: bool = False,
) -> list[dict]:
    """Return ModelInfo-compatible dicts for every currently-free OpenRouter model.

    Cached for 24h. Falls back to hardcoded essentials if API + cache
    both unavailable.
    """
    # 1. Fresh cache wins
    if not force_refresh:
        cached = _read_cache()
        if cached is not None:
            return cached

    # 2. Live fetch
    raw = _fetch_live(api_key, timeout=timeout)
    if raw is not None:
        free = [m for m in raw if _is_free(m)]
        infos = [_model_dict_to_info(m) for m in free]
        # Sort: coder first, then reasoning, then by id
        def _sort_key(info: dict) -> tuple:
            pros = info.get("pros", "")
            priority = 0 if "Coder" in pros else (1 if "Reasoning" in pros else 2)
            return (priority, info["id"])
        infos.sort(key=_sort_key)
        _write_cache(infos)
        return infos

    # 3. Stale cache is better than nothing
    if _CACHE_PATH.exists():
        try:
            return json.loads(_CACHE_PATH.read_text("utf-8"))
        except (OSError, json.JSONDecodeError):
            pass

    # 4. Last resort: hardcoded essentials
    return [
        {
            "id": mid,
            "provider": "openrouter",
            "name": _humanize_id(mid),
            "local": False,
            "description": "(fallback — live OpenRouter API unreachable)",
            "pros": _category_for({"id": mid, "name": "", "description": ""}),
            "cons": "Rate limited (free tier)",
        }
        for mid in _FALLBACK_FREE_IDS
    ]


__all__ = ["fetch_free_models"]
