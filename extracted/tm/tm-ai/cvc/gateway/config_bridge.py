"""
Config bridge — load CVC's ~/.cvc/config.yaml and translate it into
the format the vendored upstream runtime expects.

Reads:
    primary_provider, default_model, api_keys, base_url, platform_toolsets, ...

Exports to the runtime as:
    provider, model, api_key, base_url, toolsets, ...
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger("cvc.gateway.config_bridge")

CVC_CONFIG = Path(os.environ.get("CVC_CONFIG", "~/.cvc/config.yaml")).expanduser()

# Map CVC provider IDs to vendored provider IDs + env-var key names
PROVIDER_ENV_VARS: dict[str, str] = {
    "minimax": "MINIMAX_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "google": "GOOGLE_API_KEY",
    "gemini": "GOOGLE_API_KEY",
    "copilot": "COPILOT_GITHUB_TOKEN",
    "nvidia": "NVIDIA_API_KEY",
    "groq": "GROQ_API_KEY",
    "xai": "XAI_API_KEY",
    "mistral": "MISTRAL_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
}

PROVIDER_BASE_URLS: dict[str, str] = {
    "minimax": "https://api.minimax.io/anthropic",
    "anthropic": "https://api.anthropic.com",
    "openai": "https://api.openai.com/v1",
    "google": "https://generativelanguage.googleapis.com/v1beta",
    "gemini": "https://generativelanguage.googleapis.com/v1beta",
    "groq": "https://api.groq.com/openai/v1",
    "xai": "https://api.x.ai/v1",
    "mistral": "https://api.mistral.ai/v1",
    "deepseek": "https://api.deepseek.com/v1",
}


def _hermes_catalog_provider_defaults() -> tuple[dict[str, str], dict[str, str]]:
    """Build (env_vars, base_urls) dicts from the Hermes-catalog profiles.

    The catalog (cvc.providers.hermes_catalog) already maps each provider
    to its primary env var and base URL. We surface those into the CVC
    gateway's PROVIDER_ENV_VARS / PROVIDER_BASE_URLS so:
      * `/api/models/current` reports the correct key/URL for any provider.
      * The runtime can resolve an API key + base URL for the ~30 Hermes
        providers without us hand-coding each one here.

    Hand-written entries above win (they're more specific — e.g. `minimax`
    has the `minimax.cn/anthropic` Anthropic-translated URL).

    Returns: (env_vars, base_urls) — both keyed by canonical provider id.
    """
    env_vars: dict[str, str] = {}
    base_urls: dict[str, str] = {}
    try:
        from cvc.providers.hermes_catalog import register_all_hermes_profiles
        register_all_hermes_profiles()
        from cvc.providers.base import all_profiles
        for p in all_profiles():
            if p.env_vars:
                # First env var = primary API key var (convention used by
                # all Hermes overlays and our hand-written profiles).
                env_vars[p.name] = p.env_vars[0]
            if p.base_url:
                base_urls[p.name] = p.base_url
            # Also register aliases so `/model/current?provider=glm` works
            for alias in p.aliases:
                if p.env_vars and alias not in env_vars:
                    env_vars[alias] = p.env_vars[0]
                if p.base_url and alias not in base_urls:
                    base_urls[alias] = p.base_url
    except Exception as exc:  # pragma: no cover
        logger.debug("hermes_catalog provider defaults unavailable: %s", exc)
    return env_vars, base_urls


# Auto-populate from Hermes catalog at import time. Hand-written
# PROVIDER_ENV_VARS / PROVIDER_BASE_URLS above win (merged last).
_HERMES_ENV, _HERMES_URLS = _hermes_catalog_provider_defaults()
PROVIDER_ENV_VARS.update(_HERMES_ENV)
PROVIDER_BASE_URLS.update(_HERMES_URLS)


def _read_cvc_config() -> dict:
    if not CVC_CONFIG.exists():
        logger.debug("CVC config not found at %s", CVC_CONFIG)
        return {}
    try:
        with open(CVC_CONFIG, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        logger.warning("Failed to read %s: %s", CVC_CONFIG, e)
        return {}


def _resolve_api_key(provider: str, cvc_cfg: dict) -> str:
    """Resolve an API key: env var first, then CVC config's api_keys map."""
    provider_lc = (provider or "").lower()
    env_var = PROVIDER_ENV_VARS.get(provider_lc, f"{provider.upper()}_API_KEY")
    env_val = os.environ.get(env_var, "").strip()
    if env_val:
        return env_val
    api_keys = cvc_cfg.get("api_keys") or {}
    key = api_keys.get(provider_lc) or api_keys.get(provider) or ""
    return str(key).strip() if key else ""


def _resolve_base_url(provider: str, cvc_cfg: dict) -> str:
    provider_lc = (provider or "").lower()
    explicit = (cvc_cfg.get("base_url") or "").strip()
    if explicit:
        return explicit
    return PROVIDER_BASE_URLS.get(provider_lc, "")


def load_runtime_config() -> dict[str, Any]:
    """Read ~/.cvc/config.yaml and return a dict the AIAgent factory can consume."""
    cvc_cfg = _read_cvc_config()
    provider = (cvc_cfg.get("primary_provider") or "").strip()
    model = (cvc_cfg.get("default_model") or "").strip()
    api_key = _resolve_api_key(provider, cvc_cfg)
    base_url = _resolve_base_url(provider, cvc_cfg)

    # v3.3.42 — Defensive: reject "looks-like-version" model names.
    #
    # Bug observed (2026-06-25, user's Windows machine): the user reported
    # "4.0.0 unknown model" — the gateway was sending model="4.0.0" to the
    # LLM provider, which obviously doesn't have a model by that name.
    #
    # Root cause: at some point a `cvc upgrade` or config migration
    # overwrote `default_model:` with the CVC version literal. Anything
    # matching a strict semver shape (X.Y.Z) is almost certainly NOT a
    # real model identifier (real models are `MiniMax-M3`, `claude-sonnet-4.6`,
    # `gpt-5.2`, etc. — they don't look like version numbers on their own).
    # Treat such values as corrupt and fall through to the per-provider
    # default rather than forwarding them to the provider as-is.
    import re
    if model and re.fullmatch(r"\d+\.\d+\.\d+", model):
        logger.warning(
            "default_model=%r looks like a version number, not a model name "
            "(this happens when a CVC upgrade accidentally wrote the package "
            "version into default_model). Falling back to provider default.",
            model,
        )
        model = ""

    if not model:
        # Sensible defaults per provider
        model = {
            "minimax": "MiniMax-M3",
            "anthropic": "claude-sonnet-4-5",
            "openai": "gpt-4o",
            "google": "gemini-2.0-flash",
            "gemini": "gemini-2.0-flash",
            "copilot": "gpt-4o",
        }.get(provider.lower(), "gpt-4o")

    # Pass through platform_toolsets (CVC's config) so the vendored runtime
    # sees api_server toolset selection. If absent, vendored falls back to
    # the hermes-api-server default (35+ tools).
    toolsets = cvc_cfg.get("platform_toolsets", {})

    return {
        "provider": provider,
        "model": model,
        "api_key": api_key,
        "base_url": base_url,
        "toolsets": toolsets,
        "raw_cvc_config": cvc_cfg,
    }
