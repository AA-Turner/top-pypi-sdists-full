# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import contextlib
import json
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from contrast_fireball import SpanType

import contrast
from contrast.agent.policy import patch_manager
from contrast.utils.decorators import fail_loudly, fail_quietly
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    get_arg,
    register_module_patcher,
    repatch_module,
    unregister_module_patcher,
    wrap_and_watermark,
)
from contrast_vendor import structlog as logging
from contrast_vendor import wrapt

if TYPE_CHECKING:
    from types import ModuleType

    from strands import Agent
    from strands.types.tools import AgentTool, ToolGenerator, ToolSpec

    from contrast.agent.context import ContrastContext
    from contrast.reporting.fireball import ObservabilityTrace


logger = logging.getLogger("contrast")


def _observability_trace() -> ObservabilityTrace | None:
    context = contrast.CONTEXT.get()
    return context.observability_trace if context is not None else None


def _gen_ai_attrs(operation_name: str, attributes: dict) -> dict:
    """
    Build the standard `gen_ai.*` attribute dict for a Strands operation.

    Common `gen_ai.*` attributes are always set; `attributes` supplies operation-specific
    ones (None values are dropped).
    """
    attrs: dict = {
        "gen_ai.operation.name": operation_name,
        "gen_ai.event.start_time": datetime.now(timezone.utc).isoformat(),
    }
    attrs.update({k: v for k, v in attributes.items() if v is not None})
    return attrs


@contextlib.contextmanager
def _span(
    span_type: SpanType,
    operation_name: str,
    attributes: dict,
):
    """
    Open a Fireball child span of the given `span_type` representing a Strands gen_ai
    operation.

    Yields the span (or None if tracing is unavailable).
    """
    trace = _observability_trace()
    if trace is None:
        yield None
        return

    with trace.child_span(
        span_type,
        attributes=_gen_ai_attrs(operation_name, attributes),
    ) as span:
        try:
            yield span
        finally:
            if span is not None:
                span.update(
                    {"gen_ai.event.end_time": datetime.now(timezone.utc).isoformat()}
                )


def _call_llm_span(model):
    return _span(
        SpanType.AiCallLlm,
        "chat",
        {
            "gen_ai.provider.name": _provider_name(model),
            "gen_ai.request.model": _model_id(model),
        },
    )


def _execute_tool_span(tool_use):
    return _span(
        SpanType.AiExecuteTool,
        "execute_tool",
        _tool_span_attrs(tool_use),
    )


# Maps the name of a `strands.models.<name>` module to a `gen_ai.provider.name`. We only
# report the OTel well-known providers; modules without one are intentionally omitted.
# https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/registry/attributes/gen-ai.md
_PROVIDER_BY_MODEL_MODULE = {
    "anthropic": "anthropic",
    "bedrock": "aws.bedrock",
    "gemini": "gcp.gemini",
    "mistral": "mistral",
    "openai": "openai",
    "openai_responses": "openai",
}

_STRANDS_MODELS_PREFIX = "strands.models."

# `gen_ai.provider.name` is a required attribute, so we need a value even when the model
# isn't one of the built-in Strands models.
_UNKNOWN_PROVIDER = "_OTHER"


def _provider_name(model) -> str:
    """
    Determine `gen_ai.provider.name` from the Strands model class.

    We walk the MRO (most-derived first) and return the first well-known provider
    mapped from a class defined in one of Strands' built-in `strands.models.*` modules.
    This means user subclasses of built-in models resolve to the right provider, and
    models that build on a well-known one (e.g. `LiteLLMModel` is an `OpenAIModel`)
    report that provider. Anything else gets `_OTHER`, since the attribute is required.
    """
    for cls in type(model).__mro__:
        module = getattr(cls, "__module__", None) or ""
        if not module.startswith(_STRANDS_MODELS_PREFIX):
            continue
        name = module.removeprefix(_STRANDS_MODELS_PREFIX).partition(".")[0]
        if (provider := _PROVIDER_BY_MODEL_MODULE.get(name)) is not None:
            return provider
    return _UNKNOWN_PROVIDER


def _model_id(model) -> str | None:
    config = getattr(model, "config", None)
    if isinstance(config, dict):
        return config.get("model_id")
    return None


def _usage_attrs(usage) -> dict:
    """
    Convert a Strands `Usage` dict into `gen_ai.usage.*` span attributes.
    """
    if not isinstance(usage, dict):
        return {}
    attrs = {}
    for src, dst in (
        ("inputTokens", "gen_ai.usage.input_tokens"),
        ("outputTokens", "gen_ai.usage.output_tokens"),
        ("totalTokens", "gen_ai.usage.total_tokens"),
    ):
        if (value := usage.get(src)) is not None:
            attrs[dst] = value
    return attrs


def build__init__patch(orig_func, patch_policy):
    """
    Patch for strands.Agent.__init__

    Unlike our web framework middlewares, there's no request/response cycle to
    instrument here. We only need to make sure agent_state is initialized when a
    Strands agent is created.
    """
    from contrast.agent import agent_state

    def __init__patch(wrapped, instance, args, kwargs) -> None:
        result = wrapped(*args, **kwargs)

        logger.info("Detected application: strands")

        if not agent_state.is_initialized():
            with agent_state.automatic_middleware():
                agent_state.initialize()

        _discover_tools(instance)

        return result

    return wrap_and_watermark(orig_func, __init__patch)


@fail_loudly("Failed to discover tools for Strands agent")
def _discover_tools(agent: Agent) -> None:
    """
    Instrument each discovered tool so we can observe invocations later.

    By the time Agent.__init__ returns, all tools passed to the constructor have been
    processed into the agent's ToolRegistry. We inspect them directly and instrument
    each one.
    """
    for tool in agent.tool_registry.registry.values():
        # currently unused. May want to report detailed tool metadata in the future.
        _ = _extract_tool_metadata(tool)
        _instrument_tool(tool)


def _extract_tool_metadata(tool: AgentTool) -> ToolSpec:
    """
    Extract metadata for a single Strands tool.

    AgentTool (abstract base class) doesn't have a well-known / consistent reference to
    an underlying function object. The closest thing we get is the `stream` method, an
    async generator function that yields tool "events" and finally the tool result. In
    the future we may need to try to do more with this stream method, or perhaps extract
    more specific function object data for well-known AgentTool subclasses that do have
    accessible function references.
    """
    return tool.tool_spec


@fail_quietly("Failed to instrument a Strands tool")
def _instrument_tool(tool: AgentTool) -> None:
    if isinstance(tool.stream, wrapt.FunctionWrapper):
        return

    tool.stream = wrap_and_watermark(tool.stream, _stream_wrapper)


async def _stream_wrapper(wrapped, instance, args, kwargs) -> ToolGenerator:
    """
    Wrapper around `AgentTool.stream`. Used to observe tool use and emit an
    `execute_tool` span.
    """
    tool_use = get_arg(args, kwargs, 0, "tool_use")
    last_event = None
    with _execute_tool_span(tool_use) as span:
        try:
            async for event in wrapped(*args, **kwargs):
                last_event = event
                yield event
        finally:
            if span is not None:
                span.update(_tool_result_attrs(last_event))


def _tool_span_attrs(tool_use) -> dict:
    if not isinstance(tool_use, dict):
        return {}
    return {
        "gen_ai.tool.name": tool_use.get("name"),
        "gen_ai.tool.call.id": tool_use.get("toolUseId"),
        "gen_ai.tool.call.arguments": _to_json(tool_use.get("input")),
    }


def _to_json(value) -> str | None:
    if value is None:
        return None
    return json.dumps(value, default=str)


def _tool_result_attrs(last_event) -> dict:
    """
    Best-effort extraction of the tool's result for the span.

    LIMITATION: `AgentTool.stream` makes no guarantee about the type of its final
    yielded event. Built-in tools yield a `ToolResultEvent` carrying a `tool_result`
    dict, which is what we look for here, but custom tools may yield anything. When we
    can't recognize the result, or the tool did not succeed, we omit the attribute
    (per the OTel spec, the result is only recorded for successful executions).
    """
    tool_result = getattr(last_event, "tool_result", None)
    if not isinstance(tool_result, dict) or tool_result.get("status") != "success":
        return {}
    if (content := _to_json(tool_result.get("content"))) is None:
        return {}
    return {"gen_ai.tool.call.result": content}


def build_invoke_async_patch(orig_func, patch_policy):
    """
    Patch for `strands.Agent.invoke_async`

    This is the primary lifecycle patch for a Strands app. Note that `Agent.__call__` is
    a thin wrapper around `invoke_async`, so we don't instrument that.
    """
    from contrast.agent import agent_state, request_state, scope
    from contrast.agent.context import ContrastContext

    async def invoke_async_patch(wrapped, instance, args, kwargs):
        if (
            not agent_state.is_initialized()
            or agent_state.module.settings is None
            or not agent_state.module.settings.is_agent_config_enabled()
            or contrast.CONTEXT.get() is not None
        ):
            return await wrapped(*args, **kwargs)

        context = ContrastContext(
            event_handlers=agent_state.module.event_handlers,
            assess_enabled=agent_state.module.assess_enabled,
            protect_enabled=agent_state.module.protect_enabled,
            observe_enabled=agent_state.module.observe_enabled,
            shield_enabled=agent_state.module.shield_enabled,
        )

        if context.disabled:
            return await wrapped(*args, **kwargs)

        with contextlib.ExitStack() as stack:
            stack.enter_context(request_state.request_id_context())
            stack.enter_context(context.lifespan())
            if not context.assess_enabled:
                stack.enter_context(scope.propagation_scope())
            _enter_observability_trace(stack, context, instance)

            result = await wrapped(*args, **kwargs)
            if (trace := context.observability_trace) is not None:
                trace.update(
                    {
                        **_agent_result_attrs(result),
                        "gen_ai.event.end_time": datetime.now(timezone.utc).isoformat(),
                    }
                )
            return result

    return wrap_and_watermark(orig_func, invoke_async_patch)


def _enter_observability_trace(
    stack: contextlib.ExitStack, context: ContrastContext, agent: Agent
) -> None:
    from contrast.agent import agent_state

    if not context.observe_enabled:
        return

    fireball_client = agent_state.module.fireball_client
    if fireball_client is None:
        return

    context.observability_trace = stack.enter_context(
        fireball_client.observability_trace(
            send_trace=True,
            root_span_type=SpanType.AiInvokeAgent,
            attributes=_gen_ai_attrs("invoke_agent", _invoke_agent_attrs(agent)),
        )
    )


def _invoke_agent_attrs(agent: Agent) -> dict:
    attrs = {
        "gen_ai.agent.name": agent.name,
        "gen_ai.request.model": _model_id(agent.model),
        "gen_ai.system_instructions": agent.system_prompt,
    }
    if tool_names := agent.tool_names:
        attrs["gen_ai.agent.tools"] = list(tool_names)
    return attrs


def _agent_result_attrs(result) -> dict:
    """
    Extract final attributes from a Strands `AgentResult` for the invoke_agent span.
    """
    attrs = {}
    if (stop_reason := getattr(result, "stop_reason", None)) is not None:
        attrs["gen_ai.response.finish_reasons"] = [str(stop_reason)]
    metrics = getattr(result, "metrics", None)
    attrs.update(_usage_attrs(getattr(metrics, "accumulated_usage", None)))
    return attrs


def build_stream_messages_patch(orig_func, patch_policy):
    """
    Patch for `strands.event_loop.streaming.stream_messages` (an async generator).
    """

    async def stream_messages_patch(wrapped, instance, args, kwargs):
        if _observability_trace() is None:
            async for event in wrapped(*args, **kwargs):
                yield event
            return

        model = get_arg(args, kwargs, 0, "model")
        messages = get_arg(args, kwargs, 2, "messages")
        last_event = None
        with _call_llm_span(model) as span:
            if span is not None:
                span.update(
                    {"gen_ai.input.messages": json.dumps(messages, default=str)}
                )
            async for event in wrapped(*args, **kwargs):
                last_event = event
                yield event
            if span is not None:
                span.update(_stream_stop_attrs(last_event))

    return wrap_and_watermark(orig_func, stream_messages_patch)


def _stream_stop_attrs(last_event) -> dict:
    """
    Extract token usage from `stream_messages`' terminal event.

    The final event carries `event["stop"] = (stop_reason, message, usage, metrics)`.
    """
    try:
        stop_reason, _message, usage, _metrics = last_event["stop"]
    except (TypeError, KeyError, ValueError):
        return {}
    attrs = _usage_attrs(usage)
    if stop_reason is not None:
        attrs["gen_ai.response.finish_reasons"] = [str(stop_reason)]
    return attrs


def patch_strands(strands_module: ModuleType) -> None:
    build_and_apply_patch(strands_module.Agent, "__init__", build__init__patch)
    build_and_apply_patch(
        strands_module.Agent, "invoke_async", build_invoke_async_patch
    )


def patch_streaming(streaming_module: ModuleType) -> None:
    build_and_apply_patch(
        streaming_module, "stream_messages", build_stream_messages_patch
    )


def register_patches() -> None:
    from contrast.agent.settings import Settings

    if (config := Settings().config) is not None and config.get(
        "agent.python.enable_ai_systems_features"
    ) is True:
        register_module_patcher(patch_strands, "strands")
        register_module_patcher(patch_streaming, "strands.event_loop.streaming")
        # event_loop.py imports `stream_messages` by name, so we repatch it. This must
        # be registered after `patch_streaming`.
        register_module_patcher(repatch_module, "strands.event_loop.event_loop")


def reverse_patches() -> None:
    unregister_module_patcher("strands")
    unregister_module_patcher("strands.event_loop.streaming")
    unregister_module_patcher("strands.event_loop.event_loop")

    patch_manager.reverse_class_patches_by_name("strands", "Agent")
    patch_manager.reverse_module_patches_by_name("strands.event_loop.streaming")
    patch_manager.reverse_module_patches_by_name("strands.event_loop.event_loop")
