"""Declarative ProviderProfile dataclass + registry.

Eliminates the giant if/else chains in cvc/agent/llm.py by registering each
provider as a single ProviderProfile object describing all its quirks.

Hooks (callable fields):
    build_api_kwargs_extras(model, base_kwargs)  → extra kwargs (e.g. headers, extra_body)
    prepare_messages(messages, model)            → mutated messages (e.g. cache_control)
    fetch_models()                               → list[str] of available model IDs
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional


# ── Auth types ────────────────────────────────────────────────────────

AUTH_BEARER = "bearer"        # Authorization: Bearer <key>
AUTH_X_API_KEY = "x_api_key"  # x-api-key: <key>  (Anthropic native)
AUTH_OAUTH = "oauth"          # OAuth flow (Copilot, Codex)
AUTH_NONE = "none"            # No auth (local Ollama/LM Studio)


# ── API mode ──────────────────────────────────────────────────────────

API_MODE_CHAT_COMPLETIONS = "chat_completions"   # OpenAI standard
API_MODE_CODEX_RESPONSES = "codex_responses"     # GPT-5+/Codex new shape
API_MODE_ANTHROPIC = "anthropic_messages"        # Native Anthropic
API_MODE_GEMINI = "gemini_generate"              # Google Gemini
API_MODE_OLLAMA = "ollama_chat"


# ── Profile dataclass ────────────────────────────────────────────────

@dataclass
class ProviderProfile:
    """Declarative description of one provider."""
    name: str
    aliases: list[str] = field(default_factory=list)
    env_vars: list[str] = field(default_factory=list)  # Priority order
    base_url: str = ""
    auth_type: str = AUTH_BEARER
    api_mode: str = API_MODE_CHAT_COMPLETIONS
    fallback_models: list[str] = field(default_factory=list)
    fixed_temperature: Optional[float] = None
    default_max_tokens: int = 4096
    supports_streaming: bool = True
    supports_tools: bool = True
    supports_reasoning: bool = False
    supports_prompt_cache: bool = False

    # Per-model api_mode override map (e.g. {"gpt-5*": "codex_responses"})
    per_model_api_mode: dict[str, str] = field(default_factory=dict)

    # Hooks (optional)
    build_api_kwargs_extras: Optional[Callable[[str, dict[str, Any]], dict[str, Any]]] = None
    prepare_messages: Optional[Callable[[list[dict], str], list[dict]]] = None
    fetch_models: Optional[Callable[[], list[str]]] = None
    fetch_token: Optional[Callable[[], str]] = None  # For OAuth providers

    # Editor-attribution headers (Copilot)
    extra_headers: dict[str, str] = field(default_factory=dict)

    def resolve_api_mode(self, model: str) -> str:
        """Pick api_mode for a specific model (per_model overrides → default)."""
        for pattern, mode in self.per_model_api_mode.items():
            if pattern.endswith("*"):
                if model.startswith(pattern[:-1]):
                    return mode
            elif pattern == model:
                return mode
        return self.api_mode


# ── Global registry ───────────────────────────────────────────────────

_REGISTRY: dict[str, ProviderProfile] = {}


def register_provider(profile: ProviderProfile) -> None:
    """Register a provider profile. Aliases are also indexed."""
    _REGISTRY[profile.name.lower()] = profile
    for alias in profile.aliases:
        _REGISTRY[alias.lower()] = profile


def get_provider(name: str) -> Optional[ProviderProfile]:
    return _REGISTRY.get(name.lower())


def list_providers() -> list[str]:
    """Distinct provider names (deduped via id())."""
    seen: set[int] = set()
    out: list[str] = []
    for k, v in _REGISTRY.items():
        if id(v) in seen:
            continue
        seen.add(id(v))
        out.append(v.name)
    return out


def all_profiles() -> list[ProviderProfile]:
    seen: set[int] = set()
    out: list[ProviderProfile] = []
    for v in _REGISTRY.values():
        if id(v) in seen:
            continue
        seen.add(id(v))
        out.append(v)
    return out


# ── Bootstrap default profiles ────────────────────────────────────────

def _bootstrap_defaults() -> None:
    """Register CVC's built-in providers."""
    if _REGISTRY:
        return  # Already bootstrapped

    register_provider(ProviderProfile(
        name="anthropic",
        aliases=["claude"],
        env_vars=["ANTHROPIC_API_KEY"],
        base_url="https://api.anthropic.com",
        auth_type=AUTH_X_API_KEY,
        api_mode=API_MODE_ANTHROPIC,
        fallback_models=["claude-sonnet-4-6", "claude-haiku-4-5"],
        default_max_tokens=8192,
        supports_reasoning=True,
        supports_prompt_cache=True,
    ))

    register_provider(ProviderProfile(
        name="openai",
        env_vars=["OPENAI_API_KEY"],
        base_url="https://api.openai.com",
        auth_type=AUTH_BEARER,
        api_mode=API_MODE_CHAT_COMPLETIONS,
        per_model_api_mode={"gpt-5*": API_MODE_CODEX_RESPONSES, "o1*": API_MODE_CODEX_RESPONSES},
        supports_reasoning=True,
    ))

    register_provider(ProviderProfile(
        name="google",
        aliases=["gemini"],
        env_vars=["GOOGLE_API_KEY", "GEMINI_API_KEY"],
        base_url="https://generativelanguage.googleapis.com",
        auth_type=AUTH_BEARER,
        api_mode=API_MODE_GEMINI,
        fallback_models=["gemini-3-flash-preview"],
        supports_reasoning=True,
    ))

    register_provider(ProviderProfile(
        name="github",
        aliases=["copilot"],
        env_vars=["COPILOT_GITHUB_TOKEN", "GH_TOKEN", "GITHUB_TOKEN"],
        base_url="https://api.individual.githubcopilot.com",
        auth_type=AUTH_OAUTH,
        api_mode=API_MODE_CHAT_COMPLETIONS,
        per_model_api_mode={
            "gpt-5*": API_MODE_CODEX_RESPONSES,
            "codex*": API_MODE_CODEX_RESPONSES,
        },
        # Static fallback list — the dashboard's primary source for
        # model dropdowns when no Copilot token is available. The live
        # account-scoped list is fetched at runtime via
        # GET /api/providers/copilot/models and merged with this list.
        # Keep this in sync with the models Copilot typically enables;
        # the dynamic endpoint is the source of truth, not this list.
        fallback_models=[
            # Anthropic (most recent first)
            "claude-sonnet-5",
            "claude-sonnet-4.6",
            "claude-opus-4.7",
            "claude-opus-4.6",
            "claude-haiku-4.5",
            # OpenAI GPT-5 family
            "gpt-5.5",
            "gpt-5",
            "gpt-5-mini",
            "gpt-5-codex",
            # OpenAI GPT-4 family
            "gpt-4.1",
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4o-mini-2024-07-18",
            "gpt-4",
            "gpt-4-0613",
            # Older GPT-3.5
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-0613",
            # Copilot previews (org-rollout names that appear on Business plans)
            "copilot-preview-4o-mini-a1cfd608",
            "copilot-preview-gpt4-centralus",
        ],
        supports_reasoning=True,
        supports_prompt_cache=True,  # Claude on Copilot still supports cache_control
        extra_headers={
            "Editor-Version": "vscode/1.95.0",
            "Editor-Plugin-Version": "copilot-chat/0.22.0",
            "Copilot-Integration-Id": "vscode-chat",
            "User-Agent": "GitHubCopilotChat/0.22.0",
        },
    ))

    register_provider(ProviderProfile(
        name="nvidia",
        aliases=["nim", "nemotron"],
        env_vars=["NVIDIA_API_KEY", "NIM_API_KEY"],
        base_url="https://integrate.api.nvidia.com",
        auth_type=AUTH_BEARER,
        api_mode=API_MODE_CHAT_COMPLETIONS,
        fallback_models=[
            "nvidia/nemotron-3-super-120b-instruct",
            "moonshotai/kimi-k2-instruct",
            "minimaxai/minimax-m2",
        ],
        default_max_tokens=8192,
    ))

    # MiniMax — Anthropic-Messages-API-compatible (NOT OpenAI-compat)
    # Base URL: https://api.minimax.io (host only) — AgentLLM adds /anthropic/v1/messages
    # Auth: Authorization: Bearer *** (NOT x-api-key — see upstream _requires_bearer_auth)
    # Docs: https://platform.minimax.io/docs/guides/models-intro
    # Pricing: https://platform.minimax.io/docs/guides/pricing-paygo (Jun 2026)
    # Models: MiniMax-M3 (flagship, 1M ctx, multimodal), M2.7, M2.5, M2.1, M2
    # Default: M3 — same price as M2.7 ($0.30 / $1.20 per MTok), full 1M ctx
    register_provider(ProviderProfile(
        name="minimax",
        aliases=["minimax", "MiniMax"],
        env_vars=["MINIMAX_API_KEY"],
        base_url="https://api.minimax.io",
        auth_type=AUTH_BEARER,
        api_mode=API_MODE_ANTHROPIC,
        fallback_models=[
            "MiniMax-M3",
            "MiniMax-M2.7",
            "MiniMax-M2.7-highspeed",
            "MiniMax-M2.5",
            "MiniMax-M2.5-highspeed",
            "MiniMax-M2.1",
            "MiniMax-M2.1-highspeed",
            "MiniMax-M2",
        ],
        default_max_tokens=8192,
    ))

    register_provider(ProviderProfile(
        name="openrouter",
        aliases=[],
        env_vars=["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api",
        auth_type=AUTH_BEARER,
        api_mode=API_MODE_CHAT_COMPLETIONS,
        fallback_models=[
            "anthropic/claude-sonnet-4.6",
            "anthropic/claude-opus-4.6",
            "openai/gpt-5.2",
            "openai/gpt-5.2-codex",
            "google/gemini-3-pro-preview",
            "google/gemini-3-flash-preview",
            "deepseek/deepseek-v3.2",
            "x-ai/grok-4",
            "qwen/qwen3-max",
            "minimax/minimax-m2",
            "z-ai/glm-4.6",
        ],
        default_max_tokens=8192,
        supports_reasoning=True,
    ))

    register_provider(ProviderProfile(
        name="ollama",
        env_vars=[],
        base_url="http://localhost:11434",
        auth_type=AUTH_NONE,
        api_mode=API_MODE_OLLAMA,
    ))

    register_provider(ProviderProfile(
        name="lmstudio",
        env_vars=[],
        base_url="http://localhost:1234",
        auth_type=AUTH_BEARER,
        api_mode=API_MODE_CHAT_COMPLETIONS,
    ))

    register_provider(ProviderProfile(
        name="vertex",
        env_vars=["GOOGLE_APPLICATION_CREDENTIALS"],
        base_url="",
        auth_type=AUTH_OAUTH,
        api_mode=API_MODE_CHAT_COMPLETIONS,
    ))


_bootstrap_defaults()


__all__ = [
    "ProviderProfile",
    "register_provider",
    "get_provider",
    "list_providers",
    "all_profiles",
    "AUTH_BEARER", "AUTH_X_API_KEY", "AUTH_OAUTH", "AUTH_NONE",
    "API_MODE_CHAT_COMPLETIONS", "API_MODE_CODEX_RESPONSES",
    "API_MODE_ANTHROPIC", "API_MODE_GEMINI", "API_MODE_OLLAMA",
]
