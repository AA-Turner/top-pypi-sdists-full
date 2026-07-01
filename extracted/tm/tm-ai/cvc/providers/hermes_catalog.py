"""
cvc.providers.hermes_catalog — Reuse Hermes Agent's vendored provider catalog
to give CVC 30+ providers without adding a runtime dependency.

We import the vendor-tree code (``hermes_cli.providers`` + ``agent.models_dev``)
that already ships inside CVC's wheel under ``cvc/agent/_vendor/hermes/``.
No `pip install hermes-agent` required — the code is local and gets refreshed
only when the user runs `cvc gateway upgrade` (which re-vendors).

Why this exists:
    The CVC user (Jai) runs ~30 providers (z.ai/GLM, Kimi/Moonshot, StepFun,
    Arcee AI, GMI Cloud, Kilo Code, OpenCode, AWS Bedrock, Azure Foundry,
    Alibaba Cloud Coding Plan, etc.). Hand-rolling them in CVC's
    ``cvc/providers/base.py`` means every new model launch means editing
    CVC source. Hermes Agent already has the full catalog wired against
    models.dev (4000+ models, 109+ providers). We reuse that registry.

What this module does:
    1. Imports HermesOverlay dicts (transport type, base_url, env vars,
       aliases) from the vendored providers.py — one canonical source.
    2. Imports ProviderInfo + ModelInfo from vendored models_dev.py —
       backed by https://models.dev/api.json + bundled offline snapshot
       + ~/.cvc/models_dev_cache.json disk cache.
    3. Builds CVC ProviderProfile records by translating Hermes's transport
       strings ("openai_chat" → API_MODE_CHAT_COMPLETIONS,
       "anthropic_messages" → API_MODE_ANTHROPIC).
    4. Registers them into the global ``cvc.providers.base._REGISTRY`` so
       the rest of CVC (chat loop, gateway, setup wizard, dashboard) picks
       them up automatically — same path as the hand-written profiles.
    5. Exposes ``registry_snapshot_for_dashboard()`` so the web UI can
       render the full provider list + per-provider model dropdowns
       populated from models.dev metadata (context windows, capabilities,
       pricing) — the same UX Hermes Agent shows in its terminal menu.

Idempotency: re-importing this module re-registers the same profiles,
overwriting prior entries. Safe to call from anywhere at any time.

Versioning: anchored to the vendored tree (``cvc/agent/_vendor/hermes/``).
When you run `cvc gateway upgrade`, the vendored tree updates and these
profiles pick up new providers / base URL corrections automatically.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


# Lazy resolution — vendor-tree imports happen on first call so missing
# deps (numpy, requests) don't break the rest of CVC at import time.
def _hermes_overlays() -> dict[str, Any]:
    """Return the HermesOverlay dict (or empty dict if vendored tree unavailable)."""
    try:
        from cvc.agent._vendor.hermes.hermes_cli.providers import HERMES_OVERLAYS
        return HERMES_OVERLAYS
    except Exception as exc:  # pragma: no cover
        logger.debug("hermes_catalog: vendor HERMES_OVERLAYS unavailable: %s", exc)
        return {}


def _hermes_aliases() -> dict[str, str]:
    try:
        from cvc.agent._vendor.hermes.hermes_cli.providers import ALIASES
        return ALIASES
    except Exception as exc:  # pragma: no cover
        logger.debug("hermes_catalog: vendor ALIASES unavailable: %s", exc)
        return {}


def _hermes_label_overrides() -> dict[str, str]:
    try:
        from cvc.agent._vendor.hermes.hermes_cli.providers import _LABEL_OVERRIDES
        return _LABEL_OVERRIDES
    except Exception:  # pragma: no cover
        return {}


def fetch_models_dev_catalog(force_refresh: bool = False) -> dict[str, Any]:
    """Wrap the vendored models_dev fetcher.

    Returns the full registry (dict keyed by models.dev provider id, e.g.
    "zai", "anthropic", "minimax"). Each value contains ``models: {id: ModelInfo}``
    plus per-provider metadata (env vars, base URL).

    Cache hierarchy (matches Hermes Agent's design — see vendor source):
      1. In-memory cache (1h TTL)
      2. Disk cache at ``$HERMES_HOME/models_dev_cache.json`` (we redirect
         this to ``~/.cvc/`` via ``hermes_bridge.py``)
      3. Network fetch from https://models.dev/api.json
      4. Stale disk cache as last resort
    """
    try:
        from cvc.agent._vendor.hermes.agent.models_dev import fetch_models_dev
        return fetch_models_dev(force_refresh=force_refresh) or {}
    except Exception as exc:
        logger.warning("hermes_catalog: fetch_models_dev failed: %s", exc)
        return {}


def list_provider_models(provider_id: str) -> list[str]:
    """Return the list of model IDs known for a provider (from models.dev)."""
    try:
        from cvc.agent._vendor.hermes.agent.models_dev import list_provider_models
        out = list_provider_models(provider_id)
        return list(out or [])
    except Exception as exc:
        logger.debug("hermes_catalog: list_provider_models(%s) failed: %s", provider_id, exc)
        return []


def get_model_capabilities(provider_id: str, model_id: str) -> Optional[dict[str, Any]]:
    """Return capabilities dict (reasoning/tool_call/vision/...) for a model.

    Returns a plain dict so it can be JSON-serialised straight to the dashboard.
    """
    try:
        from cvc.agent._vendor.hermes.agent.models_dev import get_model_capabilities
        cap = get_model_capabilities(provider_id, model_id)
        if cap is None:
            return None
        # Convert dataclass to dict — ModelCapabilities has many fields.
        from dataclasses import asdict, is_dataclass
        if is_dataclass(cap):
            return asdict(cap)
        return dict(cap) if hasattr(cap, "__dict__") else None
    except Exception as exc:
        logger.debug("hermes_catalog: get_model_capabilities failed: %s", exc)
        return None


# ---------------------------------------------------------------------------
# CVC-side translation tables
# ---------------------------------------------------------------------------

# Hermes transport string → cvc.providers.base.API_MODE_*
_TRANSPORT_TO_API_MODE = {
    "openai_chat": "chat_completions",
    "anthropic_messages": "anthropic_messages",
    "codex_responses": "codex_responses",
    "bedrock_converse": "bedrock_converse",
}

# Hermes auth_type → cvc.providers.base.AUTH_*
_AUTH_TRANSLATION = {
    "api_key": "bearer",
    "oauth_device_code": "oauth",
    "oauth_external": "oauth",
    "aws_sdk": "bearer",   # AWS SDK is its own thing; we treat as bearer-style
    "external_process": "bearer",
}


def _model_id_to_name(model_id: str) -> str:
    """Friendly display name from a model id like 'claude-sonnet-4.6'."""
    # Heuristic: replace dashes with spaces, title-case-ish but preserve version numerals
    pretty = model_id.replace("-", " ").replace("_", " ")
    # Don't title-case ALL CAPS or version numbers
    return pretty


def _build_cvc_profile(
    *,
    cvc_key: str,
    overlay: Any,
    models_dev_raw: Any | None,
) -> Any:
    """Translate one Hermes overlay + models.dev metadata into a CVC ProviderProfile.

    `models_dev_raw` is a raw dict (from `fetch_models_dev()`) keyed by
    models.dev provider id. It contains ``api``, ``env``, ``models``, etc.
    """
    from cvc.providers.base import (
        ProviderProfile,
        AUTH_BEARER,
        AUTH_OAUTH,
        AUTH_NONE,
        API_MODE_CHAT_COMPLETIONS,
        API_MODE_ANTHROPIC,
        API_MODE_CODEX_RESPONSES,
    )

    auth_type = _AUTH_TRANSLATION.get(overlay.auth_type, AUTH_BEARER)
    api_mode = _TRANSPORT_TO_API_MODE.get(overlay.transport, API_MODE_CHAT_COMPLETIONS)

    # Env vars — start with models.dev's list, append Hermes-specific extras
    env_vars: list[str] = []
    if isinstance(models_dev_raw, dict):
        mdev_env = models_dev_raw.get("env") or []
        if isinstance(mdev_env, (list, tuple)):
            env_vars.extend(list(mdev_env))
    if overlay.extra_env_vars:
        for ev in overlay.extra_env_vars:
            if ev not in env_vars:
                env_vars.append(ev)
    if not env_vars:
        # Fallback: try a sensible convention. Most providers use UPPER_PROVIDER + _API_KEY
        env_vars = [f"{cvc_key.upper().replace('-', '_')}_API_KEY"]

    # Base URL — Hermes override wins, else models.dev, else empty (caller supplies)
    base_url = overlay.base_url_override
    if not base_url and isinstance(models_dev_raw, dict):
        base_url = models_dev_raw.get("api") or ""
    base_url = (base_url or "").rstrip("/")

    # Fallback models — pulled from models.dev if available (raw dict path)
    fallback_models: list[str] = []
    if isinstance(models_dev_raw, dict):
        mdev_models = models_dev_raw.get("models") or {}
        if isinstance(mdev_models, dict):
            fallback_models = list(mdev_models.keys())
        elif isinstance(mdev_models, list):
            fallback_models = [m.get("id") if isinstance(m, dict) else str(m) for m in mdev_models]
    if not fallback_models:
        # Last-resort: try the typed get_provider_info helper which knows
        # how to parse the raw entry.
        try:
            fallback_models = list_provider_models(cvc_key)
        except Exception:
            pass

    # Resolve display name
    display_name = ""
    if isinstance(models_dev_raw, dict):
        display_name = models_dev_raw.get("name") or ""
    if not display_name:
        display_name = _hermes_label_overrides().get(cvc_key, cvc_key.replace("-", " ").title())

    # supports_reasoning: cheap probe across first 3 models
    supports_reasoning = False
    supports_tools = True
    if isinstance(models_dev_raw, dict):
        mdev_models = models_dev_raw.get("models") or {}
        if isinstance(mdev_models, dict):
            for mid in list(mdev_models.keys())[:3]:
                cap = get_model_capabilities(cvc_key, mid)
                if cap and cap.get("reasoning"):
                    supports_reasoning = True
                    break
                if cap and cap.get("tool_call") is False:
                    supports_tools = False

    # doc URL
    doc_url = ""
    if isinstance(models_dev_raw, dict):
        doc_url = models_dev_raw.get("doc") or ""
    model_count = 0
    if isinstance(models_dev_raw, dict):
        model_count = len(models_dev_raw.get("models") or {})

    profile = ProviderProfile(
        name=cvc_key,
        aliases=[],  # populated separately by register_all_hermes_profiles()
        env_vars=env_vars,
        base_url=base_url,
        auth_type=auth_type,
        api_mode=api_mode,
        fallback_models=fallback_models[:25],
        supports_streaming=True,
        supports_tools=supports_tools,
        supports_reasoning=supports_reasoning,
    )
    profile._cvc_meta = {  # type: ignore[attr-defined]
        "source": "hermes_catalog",
        "display_name": display_name,
        "is_aggregator": overlay.is_aggregator,
        "doc_url": doc_url,
        "model_count": model_count,
    }
    return profile


def register_all_hermes_profiles() -> int:
    """Bootstrap-merge every Hermes overlay into the CVC provider registry.

    Skips overlays whose canonical name collides with a profile CVC has
    already registered by hand (anthropic, openai, google, github/copilot,
    nvidia, minimax, ollama, lmstudio, vertex). Hand-written profiles
    stay in charge of their own provider — Hermes's overlay is only used
    as a metadata source if the model list happens to be richer.

    Returns the number of NEW profiles registered.
    """
    from cvc.providers.base import register_provider, get_provider

    overlays = _hermes_overlays()
    aliases = _hermes_aliases()
    if not overlays:
        logger.debug("hermes_catalog: no overlays available; skipping registration")
        return 0

    # Fetch the models.dev catalog once. Offline-first: bundled snapshot
    # → disk cache → network. Failure is non-fatal; we just register
    # profiles without model lists.
    catalog = fetch_models_dev_catalog(force_refresh=False)

    registered = 0
    skipped = 0
    for canonical_id, overlay in overlays.items():
        # Skip transport=bedrock_converse for now — requires AWS SDK,
        # which we don't bundle in CVC. Future: pull boto3 lazily.
        if overlay.transport == "bedrock_converse":
            continue
        # Skip pure OAuth flows that need a separate token-mint path
        # (we have OpenAI/GitHub Copilot OAuth already; others can come later).
        if overlay.auth_type in ("oauth_device_code", "oauth_external", "external_process"):
            # Exception: keep github-copilot which CVC handles via OAuth module.
            if canonical_id not in {"github-copilot"}:
                continue

        # Don't override hand-written CVC profiles.
        if get_provider(canonical_id) is not None:
            skipped += 1
            continue

        mdev_raw = None
        if catalog:
            # Map canonical → models.dev provider id (Hermes maintains
            # PROVIDER_TO_MODELS_DEV for this). Fall back to canonical.
            try:
                from cvc.agent._vendor.hermes.agent.models_dev import PROVIDER_TO_MODELS_DEV
                mdev_id = PROVIDER_TO_MODELS_DEV.get(canonical_id, canonical_id)
                mdev_raw = catalog.get(mdev_id)
            except Exception:
                mdev_raw = catalog.get(canonical_id)

        profile = _build_cvc_profile(
            cvc_key=canonical_id,
            overlay=overlay,
            models_dev_raw=mdev_raw,
        )
        # Resolve aliases — every alias that maps to this canonical id
        # becomes a CVC alias on the profile.
        cvc_aliases: list[str] = []
        for alias, target in aliases.items():
            if target == canonical_id:
                cvc_aliases.append(alias)
        profile.aliases = cvc_aliases

        register_provider(profile)
        registered += 1

    logger.info(
        "hermes_catalog: registered %d new providers (skipped %d that CVC owns by hand)",
        registered,
        skipped,
    )
    return registered


# ---------------------------------------------------------------------------
# Snapshot for the dashboard / API
# ---------------------------------------------------------------------------

def registry_snapshot_for_dashboard(force_refresh: bool = False) -> dict[str, Any]:
    """Return a JSON-serialisable snapshot of every provider we know about.

    Includes both hand-written CVC profiles AND Hermes-catalog providers
    (after ``register_all_hermes_profiles`` has been called once at boot).
    Pulls model lists from models.dev so the dashboard model-picker can
    populate per-provider dropdowns.
    """
    from cvc.providers.base import all_profiles

    catalog = fetch_models_dev_catalog(force_refresh=force_refresh)
    profiles = all_profiles()
    out_providers: list[dict[str, Any]] = []

    for p in profiles:
        meta = getattr(p, "_cvc_meta", {}) or {}
        # Resolve which raw models.dev entry maps to this profile. The
        # catalog is keyed by models.dev provider id; we look up via the
        # profile's canonical name first, then through any alias.
        mdev_id = ""
        mdev_entry: dict[str, Any] | None = None
        candidates = [p.name, *p.aliases]
        try:
            from cvc.agent._vendor.hermes.agent.models_dev import PROVIDER_TO_MODELS_DEV
            for cand in candidates:
                resolved = PROVIDER_TO_MODELS_DEV.get(cand, cand)
                if resolved in catalog:
                    mdev_id = resolved
                    mdev_entry = catalog[resolved]
                    break
        except Exception:
            pass
        if not mdev_entry and p.name in catalog:
            mdev_id = p.name
            mdev_entry = catalog[p.name]

        # Per-model entry list with capabilities (context window, pricing, etc.)
        models_out: list[dict[str, Any]] = []
        for mid in (p.fallback_models or []):
            cap = None
            if mdev_id:
                try:
                    cap = get_model_capabilities(mdev_id, mid)
                except Exception:
                    cap = None
            # `get_model_capabilities` returns a dict (asdict-wrapped):
            # {supports_tools, supports_vision, supports_reasoning,
            #  context_window, max_output_tokens, model_family}
            ctx = 0
            max_out = 0
            cost_in = 0.0
            cost_out = 0.0
            reasoning = False
            tool_call = True
            vision = False
            if isinstance(cap, dict):
                ctx = int(cap.get("context_window", 0) or 0)
                max_out = int(cap.get("max_output_tokens", 0) or 0)
                reasoning = bool(cap.get("supports_reasoning", False))
                tool_call = bool(cap.get("supports_tools", True))
                vision = bool(cap.get("supports_vision", False))
            elif cap is not None:
                ctx = int(getattr(cap, "context_window", 0) or 0)
                max_out = int(getattr(cap, "max_output_tokens", 0) or 0)
                reasoning = bool(getattr(cap, "supports_reasoning", False))
                tool_call = bool(getattr(cap, "supports_tools", True))
                vision = bool(getattr(cap, "supports_vision", False))
            models_out.append({
                "id": mid,
                "name": _model_id_to_name(mid),
                "context_window": ctx,
                "max_output": max_out,
                "reasoning": reasoning,
                "tool_call": tool_call,
                "vision": vision,
                "cost_input": cost_in,
                "cost_output": cost_out,
            })
        # If profile has no fallback_models but models.dev has them, surface those too
        if not models_out and mdev_entry:
            mdev_models = mdev_entry.get("models") or {}
            if isinstance(mdev_models, dict):
                for mid in list(mdev_models.keys())[:25]:
                    raw_m = mdev_models.get(mid) or {}
                    if not isinstance(raw_m, dict):
                        raw_m = {}
                    limit = raw_m.get("limit") or {}
                    cost = raw_m.get("cost") or {}
                    models_out.append({
                        "id": mid,
                        "name": raw_m.get("name") or _model_id_to_name(mid),
                        "context_window": int(limit.get("context", 0) or 0),
                        "max_output": int(limit.get("output", 0) or 0),
                        "reasoning": bool(raw_m.get("reasoning")),
                        "tool_call": bool(raw_m.get("tool_call", True)),
                        "vision": bool(raw_m.get("attachment")),
                        "cost_input": float(cost.get("input", 0) or 0),
                        "cost_output": float(cost.get("output", 0) or 0),
                    })

        out_providers.append({
            "id": p.name,
            "aliases": list(p.aliases),
            "display_name": meta.get("display_name") or _model_id_to_name(p.name),
            "doc_url": meta.get("doc_url", ""),
            "is_aggregator": meta.get("is_aggregator", False),
            "transport": p.api_mode,
            "auth_type": p.auth_type,
            "base_url": p.base_url,
            "env_vars": list(p.env_vars),
            "supports_reasoning": p.supports_reasoning,
            "supports_tools": p.supports_tools,
            "model_count": len(models_out),
            "models": models_out,
        })

    return {
        "providers": out_providers,
        "provider_count": len(out_providers),
        "schema_version": 1,
        "source": "cvc.providers.hermes_catalog",
    }


# ---------------------------------------------------------------------------
# CLI setup-wizard helpers
# ---------------------------------------------------------------------------

def models_for_provider(provider: str, limit: int = 20) -> list[str]:
    """Return a flat list of model ids for ``provider`` from models.dev.

    Used by ``cvc setup`` (and `cvc setup --change-model`) so providers
    added via Hermes catalog (zai, kimi, stepfun, alibaba, arcee, gmi,
    ollama-cloud, …) get a model picker populated from real catalog data
    instead of an empty table.

    Looks up via the CVC ProviderProfile first (fallback_models + aliases),
    then via models.dev catalog directly if needed.
    """
    register_all_hermes_profiles()
    catalog = fetch_models_dev_catalog(force_refresh=False)

    # Resolve provider id through the profile system (handles aliases)
    candidates: list[str] = [provider]
    try:
        from cvc.providers.base import get_provider
        prof = get_provider(provider)
        if prof:
            candidates = [prof.name, *prof.aliases]
    except Exception:
        pass

    # Try the CVC→mdev map (zai→zai, github→github, openrouter→openrouter, etc.)
    try:
        from cvc.agent._vendor.hermes.agent.models_dev import PROVIDER_TO_MODELS_DEV
        for cand in candidates:
            resolved = PROVIDER_TO_MODELS_DEV.get(cand, cand)
            entry = catalog.get(resolved)
            if entry and isinstance(entry.get("models"), dict):
                return list(entry["models"].keys())[:limit]
    except Exception:
        pass

    # Fall back to direct id match (handles providers registered under their own id)
    for cand in candidates:
        entry = catalog.get(cand)
        if entry and isinstance(entry.get("models"), dict):
            return list(entry["models"].keys())[:limit]

    # Last resort: use the profile's fallback_models (may be empty)
    try:
        from cvc.providers.base import get_provider
        prof = get_provider(provider)
        if prof and prof.fallback_models:
            return list(prof.fallback_models)[:limit]
    except Exception:
        pass

    return []


def env_key_for_provider(provider: str) -> str:
    """Return the primary environment variable name for ``provider``'s API key.

    Falls back through the CVC ProviderProfile.env_vars list (priority order)
    so providers like zai that accept ``ZHIPU_API_KEY`` or ``GLM_API_KEY``
    report the right one in `cvc setup`'s API-key step.
    """
    try:
        from cvc.providers.base import get_provider
        prof = get_provider(provider)
        if prof and prof.env_vars:
            return prof.env_vars[0]
    except Exception:
        pass
    return ""


# ---------------------------------------------------------------------------
# Auto-bootstrap
# ---------------------------------------------------------------------------
try:
    register_all_hermes_profiles()
except Exception as exc:
    # Never break CVC at import time because models.dev is unreachable.
    logger.warning("hermes_catalog: bootstrap registration skipped: %s", exc)


__all__ = [
    "register_all_hermes_profiles",
    "registry_snapshot_for_dashboard",
    "fetch_models_dev_catalog",
    "list_provider_models",
    "get_model_capabilities",
    "models_for_provider",
    "env_key_for_provider",
]  # type: ignore[list-item]  # noqa: F822
