"""
cvc.gateway.catalog — Dashboard-facing provider catalog endpoint.

Wraps ``cvc.providers.hermes_catalog.registry_snapshot_for_dashboard`` so
the React UI can render one giant provider/model picker with every Hermes
Agent supported provider (30+) and every model from models.dev (~4000).

No new runtime dependency — the catalog itself comes from the vendored
Hermes Agent tree plus the on-disk models.dev cache at
``~/.cvc/models_dev_cache.json``. After a fresh install the user runs
``cvc setup`` (now showing all catalog providers in one menu); the cache
hydrates on first import.

Endpoints:
    GET  /api/catalog/providers  — full provider+model list
    POST /api/catalog/refresh    — force-refresh models.dev from network
    GET  /api/catalog/health     — sanity check + cache age
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

from fastapi import APIRouter

logger = logging.getLogger("cvc.gateway.catalog")

router = APIRouter()


@router.get("/catalog/flat")
async def list_providers_flat():
    """Flat provider→models shape — same wire format as /api/models/catalog.

    Some dashboard code (ModelPicker) expects ``{providers: {id: [models]},
    provider_labels: {id: label}}``. This endpoint bridges the rich
    per-provider snapshot to that shape so the existing picker lights
    up immediately with the new providers from the Hermes catalog.
    """
    try:
        from cvc.providers.hermes_catalog import registry_snapshot_for_dashboard
        snap = registry_snapshot_for_dashboard(force_refresh=False)
    except Exception as exc:
        logger.exception("catalog/flat: failed: %s", exc)
        return {"providers": {}, "provider_labels": {}, "provider_count": 0, "error": str(exc)}

    out_providers: dict[str, list[dict[str, Any]]] = {}
    out_labels: dict[str, str] = {}
    for prov in snap.get("providers", []):
        pid = prov.get("id") or ""
        if not pid:
            continue
        models = []
        for m in prov.get("models", []):
            models.append({
                "id": m.get("id", ""),
                "name": m.get("name") or m.get("id", ""),
                "description": (
                    f"context {m.get('context_window', 0)} · "
                    f"{'reasoning' if m.get('reasoning') else 'no-reasoning'} · "
                    f"{'tools' if m.get('tool_call', True) else 'no-tools'} · "
                    f"{'vision' if m.get('vision') else 'text-only'}"
                ),
                "context_window": int(m.get("context_window", 0) or 0),
                "supports_reasoning": bool(m.get("reasoning", False)),
                "supports_vision": bool(m.get("vision", False)),
                "provider_label": prov.get("display_name", pid),
            })
        out_providers[pid] = models
        out_labels[pid] = prov.get("display_name", pid)
        # Also register under every alias so the picker accepts "glm" / "z.ai" / "zhipu"
        for alias in prov.get("aliases", []) or []:
            if alias not in out_providers:
                out_providers[alias] = list(models)  # shallow copy
            if alias not in out_labels:
                out_labels[alias] = prov.get("display_name", pid)
    return {
        "providers": out_providers,
        "provider_labels": out_labels,
        "provider_count": len(snap.get("providers", [])),
        "schema_version": 1,
        "source": "cvc.providers.hermes_catalog (flat)",
    }


@router.get("/catalog/providers")
async def list_providers():
    """Return every provider CVC can route to, with model dropdowns.

    Combines hand-written CVC profiles (anthropic, openai, github/copilot,
    nvidia, minimax, etc.) with Hermes-catalog providers (z.ai, kimi,
    stepfun, alibaba, opencode, kilo, arcee, gmi, ollama-cloud, xai,
    xiaomi, tencent-tokenhub, huggingface, novita, deepseek, azure-foundry).

    Each provider entry contains a ``models`` list with id, name,
    context_window, max_output, capability flags. The dashboard uses
    this to populate per-provider model dropdowns.

    Response shape:
        {
          "providers": [
            {"id": "zai", "display_name": "Z.AI", "base_url": "...",
             "env_vars": [...], "model_count": 14, "models": [...]},
            ...
          ],
          "provider_count": 29,
          "schema_version": 1,
          "source": "cvc.providers.hermes_catalog",
          "cached_at": 1700000000.0
        }
    """
    try:
        # Lazy import so the endpoint survives a missing vendor tree.
        from cvc.providers.hermes_catalog import registry_snapshot_for_dashboard

        snap = registry_snapshot_for_dashboard(force_refresh=False)
        snap["cached_at"] = time.time()
        return snap
    except Exception as exc:
        logger.exception("catalog: list_providers failed: %s", exc)
        # Fall back to just the hand-written setup registry so the
        # dashboard never gets an empty response.
        try:
            from cvc.setup import registry_snapshot
            return registry_snapshot()
        except Exception:
            return {"providers": [], "provider_count": 0, "error": str(exc)}


@router.post("/catalog/refresh")
async def refresh_catalog():
    """Force-refresh the models.dev cache from the network.

    Bypasses the in-memory + disk TTL. Used by the dashboard "refresh"
    button when the user has added a brand-new model on their provider
    and wants the picker to surface it without waiting an hour.

    Returns:
        { "ok": bool, "providers_added": [...], "duration_ms": float }
    """
    t0 = time.time()
    try:
        from cvc.providers.hermes_catalog import (
            registry_snapshot_for_dashboard,
            fetch_models_dev_catalog,
        )
        fetch_models_dev_catalog(force_refresh=True)
        snap = registry_snapshot_for_dashboard(force_refresh=False)
        return {
            "ok": True,
            "provider_count": snap.get("provider_count", 0),
            "duration_ms": int((time.time() - t0) * 1000),
        }
    except Exception as exc:
        logger.exception("catalog: refresh failed: %s", exc)
        return {"ok": False, "error": str(exc), "duration_ms": int((time.time() - t0) * 1000)}


@router.get("/catalog/health")
async def catalog_health():
    """Sanity check — is the catalog loaded? How old is the disk cache?"""
    info: dict[str, object] = {
        "ok": False,
        "disk_cache_exists": False,
        "disk_cache_age_seconds": None,
        "disk_cache_path": "",
        "provider_count": 0,
    }
    try:
        cache_path = Path.home() / ".cvc" / "models_dev_cache.json"
        info["disk_cache_path"] = str(cache_path)
        if cache_path.exists():
            info["disk_cache_exists"] = True
            info["disk_cache_age_seconds"] = time.time() - cache_path.stat().st_mtime
        from cvc.providers.hermes_catalog import registry_snapshot_for_dashboard
        snap = registry_snapshot_for_dashboard(force_refresh=False)
        info["provider_count"] = snap.get("provider_count", 0)
        info["ok"] = True
    except Exception as exc:
        info["error"] = str(exc)
    return info


# ─── Dynamic Copilot Models ─────────────────────────────────────────────────
#
# GitHub Copilot's available model set is account-scoped — different
# plans (Individual / Business / Enterprise) and different orgs enable
# different models. The static fallback_models in cvc/providers/base.py
# is just a hint and is wrong whenever a new model launches.
#
# This endpoint hits GitHub Copilot's ``GET /models`` endpoint with the
# exchanged API token, returns the live list, and caches it for 10 min.
# The dashboard uses this to populate the model dropdown for the
# ``github``/``copilot`` provider AND to short-circuit requests that
# would otherwise 400 because of a wrong model pick.
#
# If the user has no Copilot token configured (no
# COPILOT_GITHUB_TOKEN / GH_TOKEN / GITHUB_TOKEN env var and no
# ``gh auth token``), we return an empty list — the catalog endpoint
# already serves the static fallback list as a backup.

@router.get("/providers/copilot/models")
async def list_copilot_models(force_refresh: bool = False):
    """Return the live list of models available on the user's Copilot plan.

    Args:
        force_refresh: if True, bypass the 10-min in-process cache.

    Returns:
        {
          "ok": bool,
          "models": [
            {"id": "claude-sonnet-5", "name": "...", "owned_by": "anthropic",
             "capabilities": {...}, "billing": {...}, "version": "..."},
            ...
          ],
          "source": "copilot_api" | "cache" | "static_fallback",
          "cached_at": float | None,
          "account": "individual" | "business" | "enterprise" | "unknown"
        }
    """
    t0 = time.time()
    try:
        from cvc.auth.copilot_auth import (
            resolve_copilot_token,
            list_copilot_models as _list_copilot_models,
            clear_copilot_models_cache,
        )
    except Exception as exc:
        return {
            "ok": False,
            "models": [],
            "source": "unavailable",
            "error": f"copilot_auth import failed: {exc}",
            "duration_ms": int((time.time() - t0) * 1000),
        }

    try:
        token, source = resolve_copilot_token()
    except Exception as exc:
        token, source = "", ""

    if not token:
        # No Copilot credentials — return empty; the frontend should
        # fall back to the static list from /api/catalog/providers.
        return {
            "ok": True,
            "models": [],
            "source": "no_token",
            "cached_at": None,
            "account": "unknown",
            "note": "no COPILOT_GITHUB_TOKEN/GH_TOKEN/GITHUB_TOKEN env var and no gh auth token",
            "duration_ms": int((time.time() - t0) * 1000),
        }

    if force_refresh:
        clear_copilot_models_cache(token)

    try:
        models = _list_copilot_models(token, force_refresh=force_refresh)
    except Exception as exc:
        logger.exception("copilot/models: list failed: %s", exc)
        return {
            "ok": False,
            "models": [],
            "source": "error",
            "error": str(exc),
            "duration_ms": int((time.time() - t0) * 1000),
        }

    # Determine account type from the api_url returned by the exchange
    account = "unknown"
    try:
        from cvc.auth.copilot_auth import _jwt_cache, _token_fingerprint
        fp = _token_fingerprint(token)
        cached = _jwt_cache.get(fp)
        if cached and len(cached) == 3:
            api_url = cached[2]
            if "business" in api_url:
                account = "business"
            elif "enterprise" in api_url:
                account = "enterprise"
            elif "individual" in api_url:
                account = "individual"
    except Exception:
        pass

    return {
        "ok": True,
        "models": models,
        "source": "copilot_api" if not force_refresh else "copilot_api_refresh",
        "cached_at": time.time(),
        "account": account,
        "token_source": source,
        "duration_ms": int((time.time() - t0) * 1000),
    }
