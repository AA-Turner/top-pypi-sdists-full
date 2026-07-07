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
    if result is None:
        return None
    message = getattr(result, "message", None)
    return truncate(message if message is not None else str(result), limit)


# Resolve a model id across strands model providers/versions: get_config(), then
# plain attributes. Module-level so the tuple isn't rebuilt on every model call.
_MODEL_ID_GETTERS = (
    lambda m: m.get_config().get("model_id"),
    lambda m: getattr(m, "model_id", None),
    lambda m: (getattr(m, "config", None) or {}).get("model_id"),
)


def _model_id(model: Any) -> str | None:
    for getter in _MODEL_ID_GETTERS:
        try:
            value = getter(model)
        except Exception:  # noqa: BLE001, S112 - try the next resolver, never break tracing
            continue
        if value:
            return str(value)
    return None


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


def node_failure(source: Any, node_id: str) -> BaseException | None:
    """Return the exception a graph/swarm node raised, if recorded."""
    results = getattr(getattr(source, "state", None), "results", None)
    node_result = results.get(node_id) if isinstance(results, dict) else None
    if getattr(getattr(node_result, "status", None), "value", None) != "failed":
        return None
    result = getattr(node_result, "result", None)
    if isinstance(result, BaseException):
        return result
    return RuntimeError(str(result) if result is not None else "node failed")


def node_ids(source: Any) -> tuple[str, ...]:
    """Return graph/swarm node ids when available."""
    nodes = getattr(source, "nodes", None)
    return tuple(nodes) if isinstance(nodes, dict) else ()


def usage_metadata(result: Any) -> dict[str, Any]:
    metrics = getattr(result, "metrics", None)
    usage = getattr(metrics, "accumulated_usage", None)
    return _usage_to_metadata(usage)


def _call_usage(stop_response: Any) -> dict[str, Any] | None:
    """The per-call usage dict Strands stashes on the assistant message metadata
    (``message["metadata"]["usage"]``), or None."""
    message = getattr(stop_response, "message", None)
    meta = message.get("metadata") if isinstance(message, dict) else None
    usage = meta.get("usage") if isinstance(meta, dict) else None
    return usage if isinstance(usage, dict) else None


def model_id(agent: Any) -> str | None:
    """The model id of the agent's bound model, for an LLM-call span."""
    return _model_id(getattr(agent, "model", None))


def usage_mapping(stop_response: Any) -> dict[str, Any] | None:
    """This model call's token usage as a snake-key mapping (or None) — Strands
    stashes it on the assistant message metadata. Shaped onto the wire by the
    shared ``aigie.tracing.usage.llm_span_payload``."""
    raw = _call_usage(stop_response)
    return _normalize_usage_keys(raw) if raw else None


def _normalize_usage_keys(usage: dict[str, Any]) -> dict[str, Any]:
    return {
        "input_tokens": usage.get("inputTokens"),
        "output_tokens": usage.get("outputTokens"),
        "total_tokens": usage.get("totalTokens"),
    }


def _usage_to_metadata(usage: Any) -> dict[str, Any]:
    if not usage or not isinstance(usage, dict):
        return {}
    return Usage.from_mapping(_normalize_usage_keys(usage)).to_metadata()
