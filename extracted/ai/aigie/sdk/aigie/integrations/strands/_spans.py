"""Pure extraction helpers shared by the Strands native callback."""

from __future__ import annotations

from typing import Any

from aigie.tracing.llm_metadata import normalize_provider
from aigie.tracing.usage import Usage

_OPENAI_COMPATIBLE = {"openai", "litellm"}

_BASE_URL_PROVIDERS: tuple[tuple[str, str], ...] = (
    ("groq.com", "groq"),
    ("together.xyz", "together"),
    ("together.ai", "together"),
    ("fireworks.ai", "fireworks"),
    ("deepseek.com", "deepseek"),
    ("api.x.ai", "xai"),
    ("cerebras.ai", "cerebras"),
    ("sambanova.ai", "sambanova"),
)


def truncate(value: Any, limit: int) -> Any:
    if isinstance(value, str) and limit and len(value) > limit:
        return value[:limit] + "…"
    return value


def messages_to_input(messages: Any, limit: int) -> Any:
    if messages is None:
        return None
    return truncate(messages if isinstance(messages, (list, dict)) else str(messages), limit)


def agent_name(agent: Any) -> str:
    return getattr(agent, "name", None) or "Strands Agent"


def tool_span_name(tool_use: dict[str, Any]) -> str:
    return tool_use.get("name") or "tool"


def result_output(result: Any, limit: int) -> Any:
    message = getattr(result, "message", None)
    return truncate(message if message is not None else str(result), limit)


def _model_id(model: Any) -> str | None:
    try:
        cfg = model.get_config()
    except Exception:  # noqa: BLE001 - never break tracing on a custom model
        return None
    return cfg.get("model_id") if isinstance(cfg, dict) else None


def _base_url(model: Any) -> str:
    args = getattr(model, "client_args", None)
    if isinstance(args, dict) and args.get("base_url"):
        return str(args["base_url"])
    client = getattr(model, "_custom_client", None)
    return str(getattr(client, "base_url", "") or "")


def _provider(model: Any) -> str | None:
    """Derive the LLM provider from the model class and base URL."""
    module = type(model).__module__.rsplit(".", 1)[-1]
    if module == "openai_responses":
        module = "openai"
    if module in _OPENAI_COMPATIBLE:
        host = _base_url(model).lower()
        for needle, provider in _BASE_URL_PROVIDERS:
            if needle in host:
                return normalize_provider(provider)
    return normalize_provider(module)


def model_metadata(agent: Any) -> dict[str, Any]:
    """Provider and model metadata for the agent's bound model."""
    model = getattr(agent, "model", None)
    if model is None:
        return {}
    out: dict[str, Any] = {}
    if provider := _provider(model):
        out["provider"] = provider
    if model_id := _model_id(model):
        out["model"] = model_id
    return out


def usage_metadata(result: Any) -> dict[str, Any]:
    metrics = getattr(result, "metrics", None)
    usage = getattr(metrics, "accumulated_usage", None)
    if not usage or not isinstance(usage, dict):
        return {}
    return Usage.from_mapping(
        {
            "input_tokens": usage.get("inputTokens"),
            "output_tokens": usage.get("outputTokens"),
            "total_tokens": usage.get("totalTokens"),
        }
    ).to_metadata()
