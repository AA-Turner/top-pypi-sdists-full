"""Centralised credential resolution for CVC providers.

This module exists because we have THREE independent persistence layers
for API keys and one of them (the broken ``cvc.config_store`` import in
``cvc/providers/base.py``) silently swallowed failures, so key updates
via ``cvc setup`` never reached the gateway or the agent runtime.

Sources, in priority order:

  1. An explicit ``api_key`` argument (caller-provided, e.g. CLI flag).
  2. Environment variable(s) — primary env var from the ProviderProfile,
     plus friendly aliases that third-party docs / shell exports use.
     The MiniMax provider in particular has a long history of brand-cased
     exports (``MINIMAX_API_KEY``, ``MINIMAX_TOKEN``, ``MiniMax_API_KEY``,
     ``MINIMAX_KEY``).
  3. ``GlobalConfig.api_keys`` (the JSON config written by ``cvc setup``)
     — keyed by canonical provider id, with friendly aliases accepted
     case-insensitively (so ``MiniMax`` / ``minimaxai`` both work).
  4. ``~/.cvc/config.yaml`` (the gateway YAML written by
     ``_sync_global_to_gateway_yaml``) — same alias handling.

The resolver is intentionally lazy about its imports — ``cvc.core.models``
and the gateway YAML module are loaded only when actually needed, which
keeps import cycles out of cold-start paths (e.g. the gateway chat
handler importing ``cvc.providers.base``).

This module never logs secrets.  When debugging is required, we log only
WHICH source resolved the key, never the key itself.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional

logger = logging.getLogger("cvc.providers.credentials")


# Friendly aliases that map to canonical provider ids.  These cover
# the cases where a user (or third-party doc, or shell snippet) used
# a slightly different spelling of the provider name.  Lookup is
# case-insensitive; both the alias key and the canonical value are
# stored lowercase here and the lookup is done against a lowered input.
_FRIENDLY_PROVIDER_ALIASES: dict[str, str] = {
    # MiniMax provider — canonical id is the 5-letter brand "minimax".
    # Users and third-party docs have arrived under many spellings.
    "minimax": "minimax",
    "minimaxai": "minimax",
    "minimaxi": "minimax",
    # GitHub Copilot — the canonical id is "github" but the dashboard
    # and many docs refer to it as "copilot".
    "copilot": "github",
}


# Env-var names to probe for each canonical provider id.  The first
# match wins.  The list intentionally contains both the canonical name
# (e.g. ``MINIMAX_API_KEY``) and friendly aliases documented in
# third-party setup guides.  New aliases can be added here without
# touching call sites.
_PROVIDER_ENV_VARS: dict[str, tuple[str, ...]] = {
    "minimax": (
        "MINIMAX_API_KEY",
        "MINIMAX_TOKEN",
        "MiniMax_API_KEY",
        "MINIMAX_KEY",
    ),
    "anthropic": ("ANTHROPIC_API_KEY",),
    "openai": ("OPENAI_API_KEY",),
    "google": ("GOOGLE_API_KEY", "GEMINI_API_KEY"),
    "gemini": ("GEMINI_API_KEY", "GOOGLE_API_KEY"),
    "github": ("GITHUB_TOKEN", "GH_TOKEN", "COPILOT_GITHUB_TOKEN"),
    "nvidia": ("NVIDIA_API_KEY", "NIM_API_KEY"),
    "openrouter": ("OPENROUTER_API_KEY",),
    "groq": ("GROQ_API_KEY",),
    "xai": ("XAI_API_KEY",),
    "mistral": ("MISTRAL_API_KEY",),
    "deepseek": ("DEEPSEEK_API_KEY",),
    "passthrough": (),
    "ollama": (),
    "lmstudio": (),
    "vertex": (),
}


# Config-file aliases (api_keys keys in GlobalConfig / config.yaml).
# Same shape as the env-var list but operates on dict keys instead.
_CONFIG_KEY_ALIASES: dict[str, tuple[str, ...]] = {
    "minimax": ("minimax", "MiniMax", "minimaxai", "minimaxi"),
    "github": ("github", "copilot"),
}


def canonical_provider(provider: str) -> str:
    """Map any friendly alias to the canonical provider id used internally.

    ``"MiniMax"`` / ``"minimax"`` → ``"minimax"``;
    ``"copilot"`` → ``"github"``; everything else passes through.
    Case-insensitive.
    """
    if not provider:
        return ""
    p = provider.strip().lower()
    return _FRIENDLY_PROVIDER_ALIASES.get(p, p)


def _env_candidates(provider: str) -> tuple[str, ...]:
    """Return the ordered list of env-var names to probe for *provider*."""
    canonical = canonical_provider(provider)
    explicit = _PROVIDER_ENV_VARS.get(canonical, ())
    # Also probe any provider-profile env_vars (e.g. from
    # cvc.providers.base.ProviderProfile.env_vars), so that newly
    # registered providers automatically benefit from this resolver.
    profile_vars: tuple[str, ...] = ()
    try:
        from cvc.providers.base import get_provider  # local import: avoid cycle
        prof = get_provider(canonical)
        if prof is not None and prof.env_vars:
            # First entry wins (it's the canonical env var).
            profile_vars = tuple(prof.env_vars)
    except Exception:  # pragma: no cover - defensive
        pass
    # Merge, preserve order, dedupe.
    seen: set[str] = set()
    out: list[str] = []
    for name in (*profile_vars, *explicit):
        if name and name not in seen:
            seen.add(name)
            out.append(name)
    return tuple(out)


def _config_key_candidates(provider: str) -> tuple[str, ...]:
    """Return config-file keys to probe for *provider*, including aliases.

    Returns both the canonical lowercased key (most common in code) and
    the explicit aliases as-written (e.g. ``"MiniMax"`` with capital M
    because users will paste that exact string into config).
    """
    canonical = canonical_provider(provider)
    explicit = _CONFIG_KEY_ALIASES.get(canonical, (canonical,))
    seen: set[str] = set()
    out: list[str] = []
    # Canonical lowercased first, then aliases as written, then their
    # lowercased forms — the resolver tries every variant in turn so
    # any of them matches.
    for k in (canonical, *explicit, canonical.lower()):
        if k and k not in seen:
            seen.add(k)
            out.append(k)
    return tuple(out)


def _read_global_config() -> Optional["object"]:
    """Read GlobalConfig from disk without importing it eagerly.

    Lazy import keeps ``cvc.providers.credentials`` importable from the
    gateway (which loads yaml but doesn't need pydantic models) and
    from early CLI paths.  Returns ``None`` on any failure.
    """
    try:
        from cvc.core.models import GlobalConfig  # lazy import
        return GlobalConfig.load()
    except Exception as exc:  # pragma: no cover - defensive
        logger.debug("GlobalConfig load failed: %s", exc)
        return None


def _read_gateway_yaml(yaml_path: Path) -> dict:
    """Read ``~/.cvc/config.yaml`` and return its dict, or ``{}``."""
    try:
        import yaml
        if not yaml_path.exists():
            return {}
        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            return {}
        return data
    except Exception as exc:  # pragma: no cover - defensive
        logger.debug("Gateway YAML read failed: %s", exc)
        return {}


def _resolve_from_dict(
    api_keys: dict,
    canonical: str,
    candidates: tuple[str, ...],
    source_label: str,
) -> str:
    """Probe *api_keys* dict for any candidate, returning the first non-empty.

    *source_label* is used for debug logging only. Matching is
    case-insensitive: ``api_keys["MiniMax"]`` and ``api_keys["minimax"]``
    are treated as the same key.
    """
    if not isinstance(api_keys, dict):
        return ""
    # Build a lowercased view of the dict so any case variant hits.
    lower_keys = {
        (k.lower() if isinstance(k, str) else k): k
        for k in api_keys.keys()
    }
    for key_name in candidates:
        lookup = key_name.lower() if isinstance(key_name, str) else key_name
        original_key = lower_keys.get(lookup)
        if original_key is None:
            continue
        val = api_keys.get(original_key)
        if isinstance(val, str) and val.strip():
            logger.debug(
                "resolve_api_key(%s) hit %s[%s]",
                canonical, source_label, original_key,
            )
            return val.strip()
    return ""


def resolve_api_key(
    provider: str,
    api_key: str = "",
    *,
    yaml_path: Path | None = None,
) -> str:
    """Resolve an API key from all known sources for *provider*.

    Order (first non-empty wins):
      1. Explicit ``api_key`` argument.
      2. Environment variable — first non-empty across the provider's
         canonical + friendly env-var list.
      3. ``GlobalConfig.api_keys`` (JSON config written by ``cvc setup``).
      4. ``~/.cvc/config.yaml`` (gateway YAML).

    Returns the resolved key, or ``""`` if nothing found.  Never raises,
    never logs the secret itself — only the source name.
    """
    if api_key and api_key.strip():
        return api_key.strip()

    canonical = canonical_provider(provider)
    if not canonical:
        return ""

    candidates = _config_key_candidates(canonical)

    # Source 2: environment variables.
    for name in _env_candidates(canonical):
        val = os.getenv(name, "").strip()
        if val:
            logger.debug("resolve_api_key(%s) hit env %s", canonical, name)
            return val

    # Source 3: GlobalConfig JSON.
    gc = _read_global_config()
    if gc is not None:
        api_keys = getattr(gc, "api_keys", None) or {}
        found = _resolve_from_dict(api_keys, canonical, candidates, "GlobalConfig")
        if found:
            return found

    # Source 4: gateway YAML.
    if yaml_path is None:
        yaml_path = Path(os.environ.get("CVC_CONFIG", "~/.cvc/config.yaml")).expanduser()
    yaml_cfg = _read_gateway_yaml(yaml_path)
    if yaml_cfg:
        yaml_keys = yaml_cfg.get("api_keys") or {}
        found = _resolve_from_dict(yaml_keys, canonical, candidates, "config.yaml")
        if found:
            return found

    return ""


__all__ = [
    "canonical_provider",
    "resolve_api_key",
]