"""cvc.setup.registry — Provider spec registry for the setup wizard.

Combines:
  • cvc/providers/base.py ProviderProfile registry (transport / auth / api_mode)
  • Wizard-facing metadata (display name, hue, description, hint, recommended flag)
  • cvc/adapters factory support (whether create_adapter() can build it)

Adding a new provider:
  1. Register a ProviderProfile in cvc/providers/base.py:_bootstrap_defaults()
  2. Add a create_adapter() branch in cvc/adapters/__init__.py
  3. Add an entry to PROVIDER_SPECS below
  ⇒ wizard, dashboard, and `cvc doctor` pick it up automatically.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

from cvc.providers.base import all_profiles, ProviderProfile


@dataclass(frozen=True)
class ProviderSpec:
    """User-facing provider metadata for the setup wizard."""

    key: str                    # canonical name, must match ProviderProfile.name
    display_name: str           # human label shown in menu
    description: str            # one-line summary
    color: str                  # rich color or hex (e.g. "#55AA55", "magenta")
    hint: str = ""              # optional secondary hint shown under description
    recommended: bool = False   # marks the wizard's primary recommendation
    free_tier: bool = False     # true if zero marginal cost (Copilot sub, NVIDIA NIM, local)
    local: bool = False         # true if runs entirely on user's machine
    requires_oauth: bool = False
    default_model: str = ""     # falls back to ProviderProfile.fallback_models[0]

    def env_keys(self) -> list[str]:
        prof = _profile_for(self.key)
        return list(prof.env_vars) if prof else []

    def base_url(self) -> str:
        prof = _profile_for(self.key)
        return prof.base_url if prof else ""

    def auth_type(self) -> str:
        prof = _profile_for(self.key)
        return prof.auth_type if prof else ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["env_keys"] = self.env_keys()
        d["base_url"] = self.base_url()
        d["auth_type"] = self.auth_type()
        return d


# ---------------------------------------------------------------------------
# Wizard-facing metadata.  ORDER = order shown in the menu.
# ---------------------------------------------------------------------------
# Recommended progression for new users:
#   1. passthrough  — zero-config capture for Claude Code / Cursor users
#   2. github       — GitHub Copilot subscription, browser OAuth, no API key
#   3. anthropic    — first-party Claude
#   4. nvidia       — free-tier Nemotron 3 Super 120B (NEW: previously hidden!)
#   5. minimax      — MiniMax M3 / M2 family, Anthropic-Messages-API-compatible
#   6. google       — first-party Gemini
#   7. openai       — first-party GPT-5.x
#   8. vertex       — enterprise Gemini via gcloud ADC
#   9. ollama       — fully local
#  10. lmstudio     — fully local with LM Studio UI
# ---------------------------------------------------------------------------

PROVIDER_SPECS: tuple[ProviderSpec, ...] = (
    ProviderSpec(
        key="passthrough",
        display_name="Passthrough",
        description="No API key — CVC captures context; your tool uses its own auth",
        hint="Best for Claude Code / Cursor / Aider users who want CVC as middleware",
        color="#55AA55",
        recommended=True,
        free_tier=True,
    ),
    ProviderSpec(
        key="github",
        display_name="GitHub Copilot",
        description="Browser OAuth — Sonnet 4.5/4.6, GPT-5, Gemini 2.5 Pro at $0/req",
        hint="Best zero-marginal-cost option if you have a Copilot subscription",
        color="#6E40C9",
        recommended=True,
        free_tier=True,
        requires_oauth=True,
        default_model="claude-sonnet-4.6",
    ),
    ProviderSpec(
        key="anthropic",
        display_name="Anthropic (Claude)",
        description="First-party access to Claude Opus 4.6, Sonnet 4.6, Haiku 4.5",
        color="#CC3333",
        default_model="claude-opus-4-6",
    ),
    ProviderSpec(
        key="nvidia",
        display_name="NVIDIA NIM",
        description="Nemotron 3 Super 120B (262K ctx) + Kimi K2 + MiniMax M2 — free tier",
        hint="Heavy-context / zero-cost workloads; OpenAI-compatible",
        color="#76B900",  # NVIDIA green
        free_tier=True,
        default_model="nvidia/nemotron-3-super-120b-instruct",
    ),
    ProviderSpec(
        key="minimax",
        display_name="MiniMax",
        description="MiniMax M3 (flagship, 1M ctx, multimodal) + M2.7 / M2.5 / M2.1 / M2",
        hint="Anthropic-Messages-API-compatible (https://api.minimax.io/anthropic); M3 = same price as M2.7 ($0.30 / $1.20 per MTok)",
        color="#FF6B35",  # MiniMax orange
        default_model="MiniMax-M3",
    ),
    ProviderSpec(
        key="openrouter",
        display_name="OpenRouter",
        description="One key, 400+ models — Claude, GPT-5, Gemini, DeepSeek, GLM, MiniMax, Grok, Qwen, and more",
        hint="Model ids are namespaced, e.g. anthropic/claude-sonnet-4.6 or z-ai/glm-4.6 — get a key at openrouter.ai/keys",
        color="#6467F2",  # OpenRouter indigo
        default_model="anthropic/claude-sonnet-4.6",
    ),
    ProviderSpec(
        key="google",
        display_name="Google Gemini",
        description="Gemini 3.1 Pro Preview, 2.5 Flash, Flash Lite via Google AI Studio",
        color="#AA8844",
        default_model="gemini-2.5-flash",
    ),
    ProviderSpec(
        key="openai",
        display_name="OpenAI",
        description="GPT-5.3, GPT-5.2, GPT-5.2-codex, GPT-4.1 — direct API",
        color="#CC6666",
        default_model="gpt-5.2",
    ),
    ProviderSpec(
        key="vertex",
        display_name="Google Cloud Vertex AI",
        description="Enterprise Gemini & Model Garden via gcloud ADC (no API key)",
        hint="Requires `gcloud auth application-default login`",
        color="#4285F4",
        requires_oauth=True,
        default_model="gemini-2.5-flash",
    ),
    ProviderSpec(
        key="ollama",
        display_name="Ollama",
        description="Fully local models — no API key, no network, no cost",
        hint="Install Ollama and pull a model first (e.g. `ollama pull qwen2.5-coder`)",
        color="magenta",
        free_tier=True,
        local=True,
        default_model="qwen2.5-coder:7b",
    ),
    ProviderSpec(
        key="lmstudio",
        display_name="LM Studio",
        description="Local models served by the LM Studio app on port 1234",
        hint="Open LM Studio, load a model, start the server",
        color="cyan",
        free_tier=True,
        local=True,
        default_model="loaded-model",
    ),
)


# ---------------------------------------------------------------------------
# Lookups
# ---------------------------------------------------------------------------

def _profile_for(key: str) -> ProviderProfile | None:
    if key == "passthrough":
        return None
    for p in all_profiles():
        if p.name == key or key in (p.aliases or []):
            return p
    return None


def list_provider_specs() -> list[ProviderSpec]:
    """Return all provider specs in wizard menu order."""
    return list(PROVIDER_SPECS)


def get_provider_spec(key: str) -> ProviderSpec | None:
    for s in PROVIDER_SPECS:
        if s.key == key:
            return s
    return None


def registry_snapshot() -> dict[str, Any]:
    """JSON-serialisable snapshot of providers + features — consumed by the dashboard."""
    from cvc.setup.features import list_feature_specs, feature_categories

    feats = list_feature_specs()
    return {
        "providers": [s.to_dict() for s in PROVIDER_SPECS],
        "provider_count": len(PROVIDER_SPECS),
        "features": [f.to_dict() for f in feats],
        "feature_count": len(feats),
        "feature_categories": feature_categories(),
        "schema_version": 1,
    }


def _wizard_color_for(provider_id: str) -> str:
    """Pick a stable color for the wizard chip from a small palette.

    Avoids the cyan/magenta "free tier" hues used by hand-written specs
    so the wizard visually distinguishes hand-written from catalog entries.
    """
    palette = ["#7C5CFF", "#3D9C7C", "#B86F33", "#5E6FAD", "#C2466A", "#5B8AA0"]
    h = sum(ord(c) for c in provider_id)
    return palette[h % len(palette)]


def _hermes_catalog_specs() -> tuple[ProviderSpec, ...]:
    """Build ProviderSpec entries for every Hermes-catalog provider that
    CVC's hand-written registry doesn't already cover.

    Source of truth: ``cvc.providers.hermes_catalog`` — wraps the vendored
    Hermes Agent providers (30+ providers, ~4000 models via models.dev).
    We translate each profile into a wizard-visible ProviderSpec so
    ``cvc setup`` shows z.ai/GLM, Kimi/Moonshot, StepFun, Arcee, GMI Cloud,
    Kilo, OpenCode, Alibaba Coding Plan, AWS Bedrock (when we ship the SDK
    bridge), Azure Foundry, etc. — same catalog Hermes Agent shows in its
    terminal menu, without forcing the user to install Hermes separately.

    No new dependency — the code lives in our vendored tree under
    ``cvc/agent/_vendor/hermes/`` and ships with the wheel.
    """
    try:
        # Importing registers the catalog profiles into the global registry
        # (idempotent). Wrap in try/except so a missing vendor or broken
        # models.dev cache never breaks the wizard.
        from cvc.providers.hermes_catalog import register_all_hermes_profiles, registry_snapshot_for_dashboard
        from cvc.providers.base import get_provider
        register_all_hermes_profiles()
        snap = registry_snapshot_for_dashboard(force_refresh=False)
    except Exception:
        return ()

    specs: list[ProviderSpec] = []
    # Skip names that overlap with the hand-written registry below.
    # (Hand-written specs get richer UX: wizard hints, recommendation badges, etc.)
    reserved = {s.key for s in PROVIDER_SPECS}
    for prov in snap.get("providers", []):
        pid = prov.get("id") or ""
        if not pid or pid in reserved:
            continue
        display_name = prov.get("display_name") or pid.title()
        is_aggregator = bool(prov.get("is_aggregator"))
        model_count = int(prov.get("model_count", 0) or 0)
        # First model id (if any) becomes the spec's default
        models = prov.get("models") or []
        first_model = models[0]["id"] if models else ""
        # Wizard color palette — cycle through safe hues by hash of id
        color = _wizard_color_for(pid)
        desc = (
            f"Aggregator — {model_count} models routed through {display_name}" if is_aggregator
            else f"{display_name} — {model_count} models via models.dev"
        )
        specs.append(ProviderSpec(
            key=pid,
            display_name=display_name,
            description=desc,
            color=color,
            hint="Bundled from Hermes catalog — full model list in dashboard" if model_count else "",
            recommended=False,
            free_tier=is_aggregator,  # aggregators often have free tiers
            default_model=first_model,
        ))
    return tuple(specs)


# Re-export the merged list so the wizard / dashboard / cvc doctor see
# the union automatically without any other code changes.
PROVIDER_SPECS_WITH_CATALOG: tuple[ProviderSpec, ...] = PROVIDER_SPECS + _hermes_catalog_specs()


def list_provider_specs_all() -> list[ProviderSpec]:
    """All providers — hand-written PLUS Hermes-catalog entries."""
    return list(PROVIDER_SPECS_WITH_CATALOG)


__all__ = [
    "ProviderSpec",
    "PROVIDER_SPECS",
    "PROVIDER_SPECS_WITH_CATALOG",
    "list_provider_specs",
    "list_provider_specs_all",
    "get_provider_spec",
    "registry_snapshot",
    "_hermes_catalog_specs",
]  # type: ignore[list-item]  # noqa: F822
