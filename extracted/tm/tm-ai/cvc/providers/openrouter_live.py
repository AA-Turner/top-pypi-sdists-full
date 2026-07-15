"""
cvc.providers.openrouter_live — Full-catalog, tier-aware OpenRouter model
fetching for the `cvc setup` wizard.

Problem this fixes:
    The generic setup-wizard path (`cvc setup`) resolved OpenRouter's model
    list through `cvc.providers.hermes_catalog.models_for_provider()`, which
    reads the offline/cached models.dev snapshot and truncates to 20 models.
    That gave users a stale, arbitrarily-ordered slice of ~20 models instead
    of OpenRouter's actual live catalog (400+ models), and never checked
    whether the pasted API key was a free or paid account before deciding
    which models to surface.

What this module does:
    1. `fetch_key_info(api_key)` — calls OpenRouter's `GET /api/v1/key` to
       determine whether the key is a free-tier or paid/paying account
       (`is_free_tier`, `limit`, `usage`, etc.). Requires the key up front.
    2. `fetch_all_openrouter_models(api_key=None)` — calls the live
       `GET /api/v1/models` endpoint (no cap) and returns every model
       OpenRouter serves, each tagged with:
         - `free`: bool (zero prompt+completion pricing)
         - `tier`: "Free" | "Paid"
         - `supports_tools`: bool (from `supported_parameters`)
       No local allowlist, no 20-model cap, no offline snapshot — this is
       the live catalog, exactly as OpenRouter serves it today.
    3. `partition_by_tier()` — splits the full list into (free_models,
       paid_models) so the wizard can show free models first for free-tier
       keys, or show everything (with tier badges) for paid keys.

Design notes:
    - OpenRouter's `/api/v1/models` endpoint does NOT require auth (it's
      the public catalog), so the model list itself can be fetched before
      the key is even validated. But we still collect the key FIRST in the
      wizard flow so we can call `/api/v1/key` and label free-vs-paid
      correctly, and so a bad key fails fast before the user picks a model
      they can't actually use.
    - Every model OpenRouter returns is included — free and paid alike.
      We do not filter by tool-calling support here (unlike the legacy
      curated-list path) because the user explicitly asked to see the full
      catalog; `supports_tools` is exposed as metadata so the wizard can
      show a warning badge instead of hiding the model outright.
"""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Optional

logger = logging.getLogger(__name__)

OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
_USER_AGENT = "cvc-setup/1.0"


@dataclass
class OpenRouterKeyInfo:
    is_free_tier: bool
    label: str = ""
    limit: Optional[float] = None
    usage: float = 0.0
    limit_remaining: Optional[float] = None
    raw: Optional[dict[str, Any]] = None


@dataclass
class OpenRouterModel:
    id: str
    name: str
    description: str
    free: bool
    tier: str  # "Free" | "Paid"
    supports_tools: bool
    context_length: int
    prompt_price: str
    completion_price: str


def fetch_key_info(api_key: str, timeout: float = 8.0) -> Optional[OpenRouterKeyInfo]:
    """Query GET /api/v1/key to determine free-tier vs paid account.

    Returns None if the key is invalid or the request fails (caller should
    treat that as "couldn't verify — proceed cautiously / re-prompt").
    """
    if not api_key:
        return None
    try:
        req = urllib.request.Request(
            f"{OPENROUTER_API_BASE}/key",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "User-Agent": _USER_AGENT,
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        logger.warning("openrouter_live: /key returned HTTP %s (invalid key?)", exc.code)
        return None
    except Exception as exc:
        logger.warning("openrouter_live: /key fetch failed: %s", exc)
        return None

    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, dict):
        return None

    is_free = bool(data.get("is_free_tier", False))
    limit = data.get("limit")
    usage = float(data.get("usage") or 0.0)
    limit_remaining = data.get("limit_remaining")

    return OpenRouterKeyInfo(
        is_free_tier=is_free,
        label=str(data.get("label") or ""),
        limit=float(limit) if limit is not None else None,
        usage=usage,
        limit_remaining=float(limit_remaining) if limit_remaining is not None else None,
        raw=data,
    )


def _is_free_pricing(pricing: dict[str, Any] | None) -> bool:
    if not isinstance(pricing, dict):
        return False
    try:
        return float(pricing.get("prompt", "0")) == 0 and float(pricing.get("completion", "0")) == 0
    except (TypeError, ValueError):
        return False


def _supports_tools(item: dict[str, Any]) -> bool:
    params = item.get("supported_parameters")
    if not isinstance(params, list):
        return True  # unknown -> permissive, don't hide
    return "tools" in params


def fetch_all_openrouter_models(
    api_key: str | None = None,
    timeout: float = 10.0,
) -> list[OpenRouterModel]:
    """Return EVERY model in OpenRouter's live catalog — no cap, no allowlist.

    This is the actual `GET /api/v1/models` response, mapped into
    OpenRouterModel records with free/paid tagging. Auth is optional (the
    endpoint is public) but we pass the key when available in case
    OpenRouter ever gates account-specific pricing/availability behind it.
    """
    headers = {"Accept": "application/json", "User-Agent": _USER_AGENT}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(f"{OPENROUTER_API_BASE}/models", headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode())

    items = payload.get("data", [])
    if not isinstance(items, list):
        return []

    out: list[OpenRouterModel] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        mid = str(item.get("id") or "").strip()
        if not mid:
            continue
        pricing = item.get("pricing") or {}
        free = _is_free_pricing(pricing) or mid.endswith(":free")
        top_provider = item.get("top_provider") or {}
        out.append(
            OpenRouterModel(
                id=mid,
                name=str(item.get("name") or mid),
                description=str(item.get("description") or "")[:120],
                free=free,
                tier="Free" if free else "Paid",
                supports_tools=_supports_tools(item),
                context_length=int(item.get("context_length") or top_provider.get("context_length") or 0),
                prompt_price=str(pricing.get("prompt", "0")),
                completion_price=str(pricing.get("completion", "0")),
            )
        )
    return out


def partition_by_tier(
    models: list[OpenRouterModel],
) -> tuple[list[OpenRouterModel], list[OpenRouterModel]]:
    """Split into (free_models, paid_models), each preserving catalog order."""
    free = [m for m in models if m.free]
    paid = [m for m in models if not m.free]
    return free, paid


def order_for_account(
    models: list[OpenRouterModel],
    key_info: Optional[OpenRouterKeyInfo],
) -> list[OpenRouterModel]:
    """Order the full catalog for display given the account's tier.

    Free-tier accounts: free models first (since those are the only ones
    they can actually call without adding credit), followed by paid models
    (still shown — the user may want to see what upgrading unlocks).
    Paid accounts: paid/full-capability models first, free models after.
    Unknown tier (key check failed): free models first as the safe default.
    """
    free, paid = partition_by_tier(models)
    if key_info is not None and not key_info.is_free_tier:
        return paid + free
    return free + paid
