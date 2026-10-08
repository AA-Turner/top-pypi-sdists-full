"""Record a training rollout as a trace in Chalk's AI Traces.

A rollout is one episode of an agent: the conversation between the model and its environment
plus the reward it earned. `log_rollout` turns one into an OpenInference trace:

    AGENT  "rollout"            the episode: task, step, reward, metrics, why it stopped
    ├─ LLM "model turn N"       the messages the model saw and the message it produced
    └─ TOOL "environment"       what the environment answered to that turn

The dashboard's Conversation tab renders that shape, so every rollout of a training run is
readable from the run's Traces tab, for any model, including the one being trained. Spans go to
the OTLP collector the platform injects into training containers through
``OTEL_EXPORTER_OTLP_ENDPOINT``; outside a Chalk container, or without the ``training`` extra,
calls are no-ops with a warning.
"""

from __future__ import annotations

import atexit
import json
import os
import random
import socket
import threading
import time
import warnings
from collections.abc import Mapping, Sequence
from contextvars import ContextVar
from typing import Any

from chalk.ml.utils import CHALK_TRAINING_RUN_ID_ENV_VAR

CHALK_TRAINING_RUN_NAME_ENV_VAR = "CHALK_TRAINING_RUN_NAME"
MAX_TEXT = 100_000
"""The trace store truncates attribute values at 100 KB; truncating here keeps spans small."""
MAX_HISTORY_MESSAGES = 32
"""How many of the most recent prior messages a model turn lists one by one in
``llm.input_messages.*``. The whole history is always in ``input.value``."""
MAX_SPAN_ATTRIBUTES = 512
"""Room for the listed history plus a caller's extra attributes. The SDK's default of 128 drops the
first-inserted attributes when exceeded, which would be the ones that identify the span."""

_lock = threading.Lock()
_provider: Any = None
_warned = False
_requested_trace_id: ContextVar[int | None] = ContextVar("chalk_rollout_trace_id", default=None)
"""The trace id the next root span takes. A context variable, so concurrent calls cannot swap ids."""


def log_rollout(
    messages: Sequence[Mapping[str, Any]],
    *,
    reward: float,
    step: int | None = None,
    task_id: str | None = None,
    split: str = "train",
    metrics: Mapping[str, float] | None = None,
    model: str | None = None,
    rollout_id: str | None = None,
    stop_reason: str | None = None,
    attributes: Mapping[str, str | int | float | bool] | None = None,
) -> str | None:
    """Record one rollout of the current training run as a trace. Returns its trace id.

    ``messages`` is the episode's conversation in order: mappings with ``role`` and ``content``,
    and optionally ``tool_calls`` / ``tool_call_id`` / ``name`` (OpenAI chat shape), ``timestamp``
    (epoch seconds), ``usage`` (``prompt_tokens`` / ``completion_tokens``) and ``finish_reason``.
    Assistant messages become model turns; every other message after the first model turn is an
    environment response to the most recent one, so parallel tool results each get a span. A tool
    message's ``tool_call_id`` ties it to the matching call on that turn.

    ``rollout_id`` (32 hex characters) is used as the trace id, so traces can be matched to a
    framework's own rollout records; otherwise one is generated. The rollout is always its own
    trace, even when called inside another span. Returns ``None`` when tracing is not configured.
    """
    provider = _get_provider()
    if provider is None:
        return None
    from opentelemetry import trace
    from opentelemetry.context import Context

    tracer = provider.get_tracer("chalk.ml.rollout_traces")
    messages = [dict(m) for m in messages]
    times = _timestamps(messages)
    trace_id = _parse_rollout_id(rollout_id)
    trace_id_hex = format(trace_id, "032x")

    # Caller extras first, the identifying attributes last: if the attribute limit is ever hit,
    # the SDK evicts the earliest-inserted ones.
    root_attributes: dict[str, Any] = dict(attributes or {})
    for name, value in (metrics or {}).items():
        root_attributes[f"metric.{name}"] = float(value)
    first_user = next((m for m in messages if m.get("role") == "user"), None)
    last_assistant = next((m for m in reversed(messages) if m.get("role") == "assistant"), None)
    if first_user is not None:
        root_attributes["input.value"] = _text(first_user.get("content"))
    if last_assistant is not None:
        root_attributes["output.value"] = _text(last_assistant.get("content"))
    if step is not None:
        root_attributes["training.step"] = int(step)
    if task_id is not None:
        root_attributes["task.id"] = str(task_id)
    if stop_reason:
        root_attributes["stop_reason"] = stop_reason
    if model:
        root_attributes["llm.model_name"] = model
    root_attributes.update(
        {
            "training.split": split,
            "reward": float(reward),
            "turn_count": sum(1 for m in messages if m.get("role") == "assistant"),
            "session.title": _title(split, step, task_id),
            "session.id": trace_id_hex,
            "agent.name": "rollout",
            "openinference.span.kind": "AGENT",
        }
    )

    token = _requested_trace_id.set(trace_id)
    try:
        # An empty context makes this a root span even when called inside another span, so the
        # rollout keeps its own trace id instead of joining the caller's trace.
        root = tracer.start_span("rollout", context=Context(), attributes=root_attributes, start_time=_ns(times[0]))
    finally:
        _requested_trace_id.reset(token)
    context = trace.set_span_in_context(root)
    turn = 0
    request: Mapping[str, Any] | None = None  # the model turn the environment is answering
    for index, message in enumerate(messages):
        started = times[index - 1] if index > 0 else times[0]
        if message.get("role") == "assistant":
            turn += 1
            request = message
            span = tracer.start_span(
                f"model turn {turn}",
                context=context,
                attributes=_model_turn_attributes(messages[:index], message, turn, model, trace_id_hex),
                start_time=_ns(started),
            )
            span.end(end_time=_ns(times[index]))
        elif request is not None:
            span = tracer.start_span(
                "environment",
                context=context,
                attributes=_environment_attributes(request, message, turn, trace_id_hex),
                start_time=_ns(started),
            )
            span.end(end_time=_ns(times[index]))
    root.end(end_time=_ns(times[-1]))
    return trace_id_hex


def configure_rollout_tracing(exporter: Any = None) -> None:
    """Send rollout traces through ``exporter`` instead of the platform's collector.

    Mainly for tests and for running outside a Chalk container; pass an OpenTelemetry
    ``SpanExporter``.
    """
    global _provider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor

    with _lock:
        _provider = _new_provider()
        _provider.add_span_processor(SimpleSpanProcessor(exporter))


def flush_rollouts() -> None:
    """Block until every recorded rollout has been exported."""
    if _provider is not None:
        _provider.force_flush()


def _get_provider() -> Any:
    global _provider, _warned
    with _lock:
        if _provider is not None:
            return _provider
        endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
        if not endpoint:
            if not _warned:
                warnings.warn(
                    "OTEL_EXPORTER_OTLP_ENDPOINT is not set; rollouts will not be recorded as traces.",
                    stacklevel=3,
                )
                _warned = True
            return None
        try:
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (  # pyright: ignore[reportMissingImports]
                OTLPSpanExporter,
            )
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
        except ImportError as exc:
            raise ImportError(
                "Recording rollouts needs the OpenTelemetry SDK: pip install 'chalkpy[training]'"
            ) from exc
        _provider = _new_provider()
        # The platform's collector speaks gRPC on a plain-http endpoint.
        _provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=endpoint.startswith("http://")))
        )
        atexit.register(_provider.shutdown)
        return _provider


def _new_provider() -> Any:
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import SpanLimits, TracerProvider
    from opentelemetry.sdk.trace.sampling import ALWAYS_ON

    # Explicit attributes override OTEL_RESOURCE_ATTRIBUTES, so only fill in what it lacks.
    configured = _env_resource_attributes()
    resource: dict[str, str] = {}
    if "service.name" not in configured:
        resource["service.name"] = "chalk-training"
    if run_id := os.environ.get(CHALK_TRAINING_RUN_ID_ENV_VAR):
        resource["chalk.training_run.id"] = run_id
    if run_name := os.environ.get(CHALK_TRAINING_RUN_NAME_ENV_VAR):
        resource["chalk.training_run.name"] = run_name
    # The collector attaches the pod's labels (environment, container) to spans by looking the
    # pod up from this attribute. Chalk services get it from the platform; set it for containers
    # that do not, since without it the run's Traces tab cannot find these spans. A `$(POD_IP)`
    # reference Kubernetes could not expand (POD_IP defined after it) counts as missing.
    pod_ip = configured.get("k8s.pod.ip", "")
    if (not pod_ip or "$(" in pod_ip) and (found := _pod_ip()):
        resource["k8s.pod.ip"] = found
    # Every rollout is recorded: the container's injected sampler (1%) is meant for request
    # traffic, not for a few hundred episodes per step.
    return TracerProvider(
        sampler=ALWAYS_ON,
        resource=Resource.create(resource),
        id_generator=_id_generator(),
        span_limits=SpanLimits(max_attributes=MAX_SPAN_ATTRIBUTES),
    )


def _env_resource_attributes() -> dict[str, str]:
    """The resource attributes the OpenTelemetry SDK reads from the environment."""
    attributes: dict[str, str] = {}
    for entry in os.environ.get("OTEL_RESOURCE_ATTRIBUTES", "").split(","):
        key, _, value = entry.strip().partition("=")
        if key and value:
            attributes[key] = value
    if service_name := os.environ.get("OTEL_SERVICE_NAME"):
        attributes["service.name"] = service_name
    return attributes


def _pod_ip() -> str | None:
    if not os.environ.get("KUBERNETES_SERVICE_HOST"):
        return None
    if pod_ip := os.environ.get("POD_IP"):
        return pod_ip
    try:
        return socket.gethostbyname(socket.gethostname())  # Kubernetes maps the hostname to the pod IP
    except OSError:
        return None


def _parse_rollout_id(rollout_id: str | None) -> int:
    if rollout_id and len(rollout_id) == 32:
        try:
            if trace_id := int(rollout_id, 16):
                return trace_id
        except ValueError:
            pass
    return random.getrandbits(128) or 1


def _id_generator() -> Any:
    """An OpenTelemetry id generator that honours the id requested for the current call."""
    from opentelemetry.sdk.trace.id_generator import RandomIdGenerator

    class RolloutIdGenerator(RandomIdGenerator):
        def generate_trace_id(self) -> int:
            requested = _requested_trace_id.get()
            return requested if requested is not None else super().generate_trace_id()

        def is_trace_id_random(self) -> bool:
            return _requested_trace_id.get() is None

    return RolloutIdGenerator()


def _model_turn_attributes(
    history: Sequence[Mapping[str, Any]], message: Mapping[str, Any], turn: int, model: str | None, trace_id: str
) -> dict[str, Any]:
    # Listed history first, identifying attributes last (see log_rollout).
    attributes: dict[str, Any] = {}
    for i, past in enumerate(history[-MAX_HISTORY_MESSAGES:]):
        attributes[f"llm.input_messages.{i}.message.role"] = str(past.get("role") or "")
        attributes[f"llm.input_messages.{i}.message.content"] = _text(past.get("content"))
    for i, call in enumerate(message.get("tool_calls") or []):
        if not isinstance(call, Mapping):
            continue
        function = call.get("function")
        if not isinstance(function, Mapping):
            function = {}
        prefix = f"llm.output_messages.0.message.tool_calls.{i}.tool_call"
        if call.get("id"):
            attributes[f"{prefix}.id"] = str(call["id"])
        if function.get("name"):
            attributes[f"{prefix}.function.name"] = str(function["name"])
        if function.get("arguments") is not None:
            attributes[f"{prefix}.function.arguments"] = _text(function["arguments"])
    usage = message.get("usage") or {}
    if usage.get("prompt_tokens") is not None:
        attributes["llm.token_count.prompt"] = int(usage["prompt_tokens"])
    if usage.get("completion_tokens") is not None:
        attributes["llm.token_count.completion"] = int(usage["completion_tokens"])
    if message.get("finish_reason"):
        attributes["gen_ai.response.finish_reasons"] = [str(message["finish_reason"])]
    if model:
        attributes["llm.model_name"] = model
    attributes.update(
        {
            "llm.output_messages.0.message.role": "assistant",
            "llm.output_messages.0.message.content": _text(message.get("content")),
            "input.value": _text(json.dumps([_message_json(m) for m in history])),
            "input.mime_type": "application/json",
            "output.value": _text(message.get("content")),
            "turn.index": turn,
            "gen_ai.operation.name": "chat",
            "session.id": trace_id,
            "openinference.span.kind": "LLM",
        }
    )
    return attributes


def _environment_attributes(
    request: Mapping[str, Any], response: Mapping[str, Any], turn: int, trace_id: str
) -> dict[str, Any]:
    call = _tool_call(request, response.get("tool_call_id"))
    function = call.get("function")
    if not isinstance(function, Mapping):
        function = {}
    # A tool result answers one call, so its input is that call's arguments; a plain
    # environment message answers the whole turn.
    request_text = function["arguments"] if function.get("arguments") is not None else request.get("content")
    attributes: dict[str, Any] = {
        "tool.name": str(response.get("name") or function.get("name") or "environment"),
        "input.value": _text(request_text),
        "output.value": _text(response.get("content")),
        "tool.result": _text(response.get("content")),
        "turn.index": turn,
        "session.id": trace_id,
        "openinference.span.kind": "TOOL",
    }
    if response.get("tool_call_id"):
        attributes["tool_call.id"] = str(response["tool_call_id"])
    return attributes


def _tool_call(request: Mapping[str, Any], call_id: Any) -> Mapping[str, Any]:
    if call_id is not None:
        for call in request.get("tool_calls") or []:
            if isinstance(call, Mapping) and call.get("id") == call_id:
                return call
    return {}


def _message_json(message: Mapping[str, Any]) -> dict[str, Any]:
    """The OpenAI-shaped view of a message: role and content plus any tool-call fields."""
    out: dict[str, Any] = {"role": message.get("role"), "content": message.get("content")}
    for key in ("name", "tool_call_id", "tool_calls"):
        if message.get(key) is not None:
            out[key] = message[key]
    return out


def _timestamps(messages: Sequence[Mapping[str, Any]]) -> list[float]:
    """Per-message times; messages without one are placed a millisecond apart, ending now."""
    now = time.time()
    times = [m.get("timestamp") if isinstance(m.get("timestamp"), (int, float)) else None for m in messages]
    if not times:
        return [now]
    filled: list[float] = []
    for index, value in enumerate(times):
        filled.append(float(value) if value is not None else now - (len(times) - index) * 0.001)
    return filled


def _title(split: str, step: int | None, task_id: str | None) -> str:
    parts = [split]
    if step is not None:
        parts.append(f"step {step}")
    if task_id is not None:
        parts.append(f"task {task_id}")
    return " · ".join(parts)


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):  # multi-part content
        value = "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in value)
    text = value if isinstance(value, str) else json.dumps(value, default=str)
    return text if len(text) <= MAX_TEXT else text[:MAX_TEXT] + "… (truncated)"


def _ns(seconds: float) -> int:
    return int(seconds * 1_000_000_000)
