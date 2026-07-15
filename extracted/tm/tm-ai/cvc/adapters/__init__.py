"""
cvc.adapters — LLM provider adapter registry.

Provides a ``create_adapter()`` factory that returns the correct adapter
based on the CVC_PROVIDER environment variable (or ``CVCConfig.provider``).

Supported providers:
    - ``anthropic``  — Claude Opus 4.6 / Opus 4.5 / Sonnet 4.6 / Sonnet 4.5 / Haiku 4.5
    - ``openai``     — GPT-5.3 / GPT-5.2 / GPT-5.2-Codex / GPT-5-mini
    - ``google``     — Gemini 3 Pro / Gemini 3 Flash / 2.5 Pro / 2.5 Flash
    - ``vertex``     — Google Cloud Vertex AI (gcloud ADC)
    - ``ollama``     — Qwen 2.5 Coder / Qwen 3 Coder / DeepSeek-R1 (local)
    - ``lmstudio``   — Any model loaded in LM Studio's local server (local)
    - ``github``     — GitHub Models API (Azure AI inference endpoint)
    - ``copilot``    — GitHub Copilot API (api.githubcopilot.com, COPILOT_GITHUB_TOKEN)
    - ``nvidia``     — NVIDIA NIM (Nemotron, Kimi K2, MiniMax M2, etc.)
    - ``minimax``  — MiniMax (M3 / M2.7 / M2.5 / M2.1 / M2) — OpenAI-compatible
    - ``openrouter`` — OpenRouter aggregator (400+ models, namespaced ids e.g. anthropic/claude-sonnet-4.6)
    - ``passthrough``— No internal LLM; the AI tool's own key is forwarded as-is"""

from __future__ import annotations

from cvc.adapters.base import BaseAdapter
from cvc.adapters.vertex import VERTEX_MODELS

# ---- Default models per provider (verified Feb 2026) ---------------------
PROVIDER_DEFAULTS: dict[str, dict[str, str]] = {
    "anthropic": {
        "model": "claude-opus-4-6",
        "env_key": "ANTHROPIC_API_KEY",
    },
    "openai": {
        "model": "gpt-5.2",
        "env_key": "OPENAI_API_KEY",
    },
    "google": {
        "model": "gemini-2.5-flash",
        "env_key": "GOOGLE_API_KEY",
    },
    "ollama": {
        "model": "qwen2.5-coder:7b",
        "env_key": "",  # No API key needed for local models
    },
    "lmstudio": {
        "model": "loaded-model",
        "env_key": "",  # No API key needed — LM Studio accepts any value
    },
    "vertex": {
        "model": "gemini-2.5-flash",
        "env_key": "",  # Uses gcloud ADC — no API key needed
    },
    "github": {
        "model": "gpt-4o",
        "env_key": "GITHUB_TOKEN",
    },
    "copilot": {
        "model": "claude-sonnet-4.6",
        "env_key": "COPILOT_GITHUB_TOKEN",
    },
    "nvidia": {
        "model": "nvidia/nemotron-3-super-120b-instruct",
        "env_key": "NVIDIA_API_KEY",
    },
    "minimax": {
        "model": "MiniMax-M2.7",
        "env_key": "MINIMAX_API_KEY",
    },
    "openrouter": {
        "model": "anthropic/claude-sonnet-4.6",
        "env_key": "OPENROUTER_API_KEY",
    },
    # Passthrough: CVC captures context but does not call any LLM itself.
    # The AI tool (e.g. Claude Code) uses its own subscription/API key.
    "passthrough": {
        "model": "",
        "env_key": "",
    },
}


def create_adapter(
    provider: str,
    api_key: str = "",
    model: str = "",
    base_url: str = "",
) -> BaseAdapter:
    """
    Factory function that returns the correct adapter for the given provider.

    Parameters
    ----------
    provider :
        One of ``"anthropic"``, ``"openai"``, ``"google"``, ``"ollama"``.
    api_key :
        API key for the provider (not needed for Ollama).
    model :
        Model identifier. Falls back to the provider's default.
    base_url :
        Optional base URL override (useful for Ollama on a non-standard port).
    """
    provider = provider.lower().strip()
    defaults = PROVIDER_DEFAULTS.get(provider)
    if defaults is None:
        # v3.3.43 — Don't reject unknown providers outright. Try the
        # Hermes catalog fallback (generic OpenAI-compat) before raising.
        # The catalog adds 30+ providers (zai, kimi, stepfun, arcee, gmi,
        # ollama-cloud, azure-foundry, …) that don't have hand-written
        # PROVIDER_DEFAULTS entries.
        try:
            # Bootstrap-register catalog profiles if not already done.
            import cvc.providers.hermes_catalog  # noqa: F401  (side-effect import)
            from cvc.providers.base import get_provider as _cvc_get_provider
            profile = _cvc_get_provider(provider)
        except Exception:
            profile = None
        if profile is not None and profile.base_url:
            # Per-provider completion-path override table. Most OpenAI-
            # compat services expose /v1/chat/completions; some (z.ai,
            # alibaba's bailian, some StepFun deployments) use a
            # versioned path like /api/paas/v4/chat/completions. Without
            # this override the request would land at /v4/v1/chat/completions
            # (404) or /v4/chat/completions only by luck.
            path_overrides = {
                "zai": "/chat/completions",            # api.z.ai/api/paas/v4/chat/completions
                "alibaba": "/compatible-mode/v1/chat/completions",  # bailian/aliyun dashscope
                "alibaba-coding-plan": "/compatible-mode/v1/chat/completions",
                "minimax-cn": "/v1/chat/completions",
                "azure-foundry": "/v1/chat/completions",
                "ollama-cloud": "/v1/chat/completions",
            }
            chat_path = path_overrides.get(profile.name, "/v1/chat/completions")
            model = model or (profile.fallback_models[0] if profile.fallback_models else "default")
            from cvc.adapters.openai import OpenAIAdapter
            return OpenAIAdapter(
                api_key=api_key or "missing",
                model=model,
                base_url=profile.base_url,
                chat_completions_path=chat_path,
            )
        raise ValueError(
            f"Unknown provider: '{provider}'. "
            f"Supported: {', '.join(PROVIDER_DEFAULTS)}"
        )

    if provider == "passthrough":
        raise ValueError(
            "CVC is configured in 'passthrough' mode — no internal LLM adapter. "
            "Use 'cvc setup' to configure a provider for CVC agent features, "
            "or use 'cvc launch <tool>' to route your AI tool through CVC."
        )

    model = model or defaults["model"]

    if provider == "anthropic":
        from cvc.adapters.anthropic import AnthropicAdapter

        return AnthropicAdapter(api_key=api_key, model=model)

    elif provider == "openai":
        from cvc.adapters.openai import OpenAIAdapter

        return OpenAIAdapter(api_key=api_key, model=model)

    elif provider == "google":
        from cvc.adapters.google import GeminiAdapter

        return GeminiAdapter(api_key=api_key, model=model)

    elif provider == "ollama":
        from cvc.adapters.ollama import OllamaAdapter

        return OllamaAdapter(
            api_key=api_key,
            model=model,
            base_url=base_url or "http://localhost:11434",
        )

    elif provider == "lmstudio":
        from cvc.adapters.lmstudio import LMStudioAdapter

        return LMStudioAdapter(
            api_key=api_key or "lm-studio",
            model=model,
            base_url=base_url or "http://localhost:1234",
        )

    elif provider == "vertex":
        from cvc.adapters.vertex import VertexAIAdapter
        from cvc.core.models import GlobalConfig

        gc = GlobalConfig.load()
        project_id = gc.vertex_project_id or ""
        location = gc.vertex_location or "us-central1"
        return VertexAIAdapter(
            model=model,
            project_id=project_id,
            location=location,
        )

    elif provider == "github":
        from cvc.adapters.github import GitHubAdapter

        return GitHubAdapter(api_key=api_key, model=model)

    elif provider == "copilot":
        from cvc.adapters.copilot import CopilotAdapter

        return CopilotAdapter(api_key=api_key, model=model)

    elif provider in ("nvidia", "nim", "nemotron"):
        from cvc.adapters.nvidia import NvidiaAdapter

        return NvidiaAdapter(api_key=api_key, model=model)

    elif provider in ("minimax", "MiniMax"):
        from cvc.adapters.minimax import (
            MiniMaxAdapter,
            MINIMAX_API_BASE,
            MINIMAX_API_BASE_CN,
        )

        # Use the international endpoint as the default. If the user
        # explicitly passed a base_url (e.g. the China endpoint or a
        # self-hosted proxy), honour it -- this also lets users in
        # China use the local endpoint without code changes.
        effective_base = base_url or MINIMAX_API_BASE
        return MiniMaxAdapter(api_key=api_key, model=model, base_url=effective_base)

    elif provider == "openrouter":
        from cvc.adapters.openai import OpenAIAdapter

        # OpenRouter speaks the OpenAI Chat Completions wire format at
        # https://openrouter.ai/api/v1/chat/completions. Model ids are
        # namespaced ("anthropic/claude-sonnet-4.6", "openai/gpt-5.2",
        # "z-ai/glm-4.6", "minimax/minimax-m2", ...) so routing through
        # here never collides with the native anthropic/openai/minimax/
        # zai adapters above — those are matched by exact provider name
        # BEFORE this branch and take priority when the user picks the
        # native provider instead of the OpenRouter aggregator.
        return OpenAIAdapter(
            api_key=api_key,
            model=model,
            base_url=base_url or "https://openrouter.ai/api",
        )

    # v3.3.43 — Generic OpenAI-compatible fallback for any provider in
    # the Hermes catalog. The 30+ providers shipped via
    # cvc.providers.hermes_catalog (z.ai/GLM, Kimi, StepFun, OpenCode,
    # Kilo, Arcee, GMI, Ollama Cloud, Alibaba Coding Plan, …) all speak
    # the OpenAI Chat Completions wire format; only their base URL +
    # auth header differ. We already know both from the catalog profile.
    try:
        from cvc.providers.base import get_provider as _cvc_get_provider
        profile = _cvc_get_provider(provider)
    except Exception:
        profile = None
    if profile is not None and profile.base_url:
        from cvc.adapters.openai import OpenAIAdapter
        # User-supplied base_url wins over the catalog default. The
        # OpenAIAdapter strips a trailing /v1 internally and re-appends
        # it to /chat/completions, so we just hand the raw URL.
        base = (base_url or profile.base_url)
        return OpenAIAdapter(api_key=api_key or "missing", model=model, base_url=base)

    raise ValueError(f"Unknown provider: '{provider}'")


__all__ = ["BaseAdapter", "create_adapter", "PROVIDER_DEFAULTS", "VERTEX_MODELS"]
