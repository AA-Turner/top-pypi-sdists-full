from __future__ import annotations

import contextlib
import contextvars
import functools
import inspect
import json
import sys
import threading
from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass, field
from typing import Any

from bitfab import subtree
from bitfab.client_patching import (
    NODE_OMITS_CALL,
    NODE_RECORDS_CALL,
    PatchingFinder,
    renamed,
    take_node_ownership,
)

CREATE = "create"
PATCHED_MARKER = "_bitfab_provider_call_patched"
CALL_MARKER = "_bitfab_provider_call"
OPENROUTER_HOSTNAME = "openrouter.ai"

_LANGCHAIN_CHAT_MODEL_FRAMES = frozenset(
    {"_generate_with_cache", "_agenerate_with_cache"}
)

_lock = threading.Lock()
_wrapper_call: contextvars.ContextVar[WrapperCall | None] = contextvars.ContextVar(
    "bitfab_provider_wrapper_call", default=None
)


@dataclass(frozen=True)
class ProviderCall:
    provider: str
    module: str
    classes: tuple[str, ...]
    handles: Callable[[Any], bool]
    is_response: Callable[[Any], bool]
    prompt: Callable[[Mapping[str, Any]], str | None]
    usage: Callable[[Mapping[str, Any], Any], dict[str, Any]]


@dataclass
class WrapperCall:
    recorded_responses: list[Any] = field(default_factory=list)

    def recorded(self) -> bool:
        return bool(self.recorded_responses)


@contextlib.contextmanager
def wrapper_call() -> Iterator[WrapperCall]:
    call = WrapperCall()
    token = _wrapper_call.set(call)
    try:
        yield call
    finally:
        _wrapper_call.reset(token)


def _mark_recorded(response: Any) -> None:
    call = _wrapper_call.get()
    if call is not None:
        call.recorded_responses.append(response)


def _field(value: Any, key: str) -> Any:
    if value is None:
        return None
    if isinstance(value, Mapping):
        return value.get(key)
    found = getattr(value, key, None)
    if found is not None:
        return found
    extra = getattr(value, "model_extra", None)
    return extra.get(key) if isinstance(extra, dict) else None


def _number(value: Any) -> int | float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value


def _text(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _as_text(content: Any) -> str:
    return content if isinstance(content, str) else json.dumps(content, default=str)


def _present(values: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


def _rendered_messages(messages: Any) -> list[dict[str, str]]:
    if not isinstance(messages, (list, tuple)):
        return []
    rendered = []
    for message in messages:
        role = _field(message, "role")
        if isinstance(role, str):
            rendered.append(
                {"role": role, "content": _as_text(_field(message, "content"))}
            )
    return rendered


def _system_message(content: Any) -> list[dict[str, str]]:
    if content is None or content == "" or content == []:
        return []
    return [{"role": "system", "content": _as_text(content)}]


def _encoded(rendered: list[dict[str, str]]) -> str | None:
    return json.dumps(rendered) if rendered else None


def _sum_tokens(*counts: int | float | None) -> int | float | None:
    present = [count for count in counts if count is not None]
    return sum(present) if present else None


def _is_openrouter_resource(resource: Any) -> bool:
    base_url = getattr(getattr(resource, "_client", None), "base_url", None)
    host = getattr(base_url, "host", None)
    return isinstance(host, str) and (
        host == OPENROUTER_HOSTNAME or host.endswith(f".{OPENROUTER_HOSTNAME}")
    )


def _any_resource(_resource: Any) -> bool:
    return True


def _is_chat_completion(response: Any) -> bool:
    return isinstance(_field(response, "choices"), (list, tuple))


def _chat_completion_prompt(request: Mapping[str, Any]) -> str | None:
    return _encoded(_rendered_messages(request.get("messages")))


def _openrouter_usage(request: Mapping[str, Any], response: Any) -> dict[str, Any]:
    usage = _field(response, "usage")
    return _present(
        {
            "model": _text(_field(response, "model")) or _text(request.get("model")),
            "upstreamProvider": _text(_field(response, "provider")),
            "inputTokens": _number(_field(usage, "prompt_tokens")),
            "outputTokens": _number(_field(usage, "completion_tokens")),
            "cachedInputTokens": _number(
                _field(_field(usage, "prompt_tokens_details"), "cached_tokens")
            ),
            "reasoningTokens": _number(
                _field(_field(usage, "completion_tokens_details"), "reasoning_tokens")
            ),
            "costUsd": _number(_field(usage, "cost")),
        }
    )


def _is_anthropic_message(response: Any) -> bool:
    return _field(response, "type") == "message" and isinstance(
        _field(response, "content"), (list, tuple)
    )


def _anthropic_prompt(request: Mapping[str, Any]) -> str | None:
    return _encoded(
        _system_message(request.get("system"))
        + _rendered_messages(request.get("messages"))
    )


def _anthropic_usage(request: Mapping[str, Any], response: Any) -> dict[str, Any]:
    usage = _field(response, "usage")
    uncached = _number(_field(usage, "input_tokens"))
    cache_read = _number(_field(usage, "cache_read_input_tokens"))
    cache_creation = _number(_field(usage, "cache_creation_input_tokens"))
    return _present(
        {
            "model": _text(_field(response, "model")) or _text(request.get("model")),
            "inputTokens": _sum_tokens(uncached, cache_read, cache_creation),
            "outputTokens": _number(_field(usage, "output_tokens")),
            "cachedInputTokens": cache_read,
        }
    )


def _is_openai_response(response: Any) -> bool:
    return _field(response, "object") == "response"


def _openai_responses_prompt(request: Mapping[str, Any]) -> str | None:
    request_input = request.get("input")
    turns = (
        [{"role": "user", "content": request_input}]
        if isinstance(request_input, str)
        else _rendered_messages(request_input)
    )
    return _encoded(_system_message(request.get("instructions")) + turns)


def _openai_responses_usage(
    request: Mapping[str, Any], response: Any
) -> dict[str, Any]:
    usage = _field(response, "usage")
    return _present(
        {
            "model": _text(_field(response, "model")) or _text(request.get("model")),
            "inputTokens": _number(_field(usage, "input_tokens")),
            "outputTokens": _number(_field(usage, "output_tokens")),
            "cachedInputTokens": _number(
                _field(_field(usage, "input_tokens_details"), "cached_tokens")
            ),
            "reasoningTokens": _number(
                _field(_field(usage, "output_tokens_details"), "reasoning_tokens")
            ),
            "costUsd": _number(_field(usage, "cost")),
        }
    )


OPENROUTER = ProviderCall(
    provider="openrouter",
    module="openai.resources.chat.completions.completions",
    classes=("Completions", "AsyncCompletions"),
    handles=_is_openrouter_resource,
    is_response=_is_chat_completion,
    prompt=_chat_completion_prompt,
    usage=_openrouter_usage,
)

ANTHROPIC = ProviderCall(
    provider="anthropic",
    module="anthropic.resources.messages.messages",
    classes=("Messages", "AsyncMessages"),
    handles=_any_resource,
    is_response=_is_anthropic_message,
    prompt=_anthropic_prompt,
    usage=_anthropic_usage,
)

OPENAI_RESPONSES = ProviderCall(
    provider="openai",
    module="openai.resources.responses.responses",
    classes=("Responses", "AsyncResponses"),
    handles=_any_resource,
    is_response=_is_openai_response,
    prompt=_openai_responses_prompt,
    usage=_openai_responses_usage,
)

PROVIDER_CALLS = (OPENROUTER, ANTHROPIC, OPENAI_RESPONSES)
_BY_MODULE = {call.module: call for call in PROVIDER_CALLS}


def context_from_response(
    call: ProviderCall, request: Mapping[str, Any], response: Any, duration_ms: int
) -> dict[str, Any]:
    return {
        "provider": call.provider,
        **call.usage(request, response),
        "durationMs": duration_ms,
    }


def request_of(args: tuple[Any, ...], kwargs: Mapping[str, Any]) -> Mapping[str, Any]:
    if "model" in kwargs or not args or not isinstance(args[0], Mapping):
        return kwargs
    return args[0]


def record_completion(
    call: ProviderCall,
    span: Any,
    request: Mapping[str, Any],
    response: Any,
    duration_ms: int,
) -> None:
    if not call.is_response(response):
        return
    with contextlib.suppress(Exception):
        prompt = call.prompt(request)
        if prompt:
            span.set_prompt(prompt)
        span.add_context(context_from_response(call, request, response, duration_ms))


def record_auto_traced_completion(
    call: ProviderCall,
    span: Any,
    request: Mapping[str, Any],
    response: Any,
    duration_ms: int,
) -> None:
    record_completion(call, span, request, response, duration_ms)
    subtree.mark_usage_recorded()
    _mark_recorded(response)


def _langchain_handler_records_call() -> bool:
    frame = sys._getframe(1)
    while frame is not None:
        if frame.f_code.co_name in _LANGCHAIN_CHAT_MODEL_FRAMES and str(
            frame.f_globals.get("__name__", "")
        ).startswith("langchain_core."):
            handlers = getattr(frame.f_locals.get("run_manager"), "handlers", None)
            return any(
                getattr(handler, "records_llm_calls", False)
                for handler in handlers or ()
            )
        frame = frame.f_back
    return False


def framework_records_call() -> bool:
    session = subtree.current_session()
    if session is not None and subtree.framework_llm_call_open(session):
        return True
    return _langchain_handler_records_call()


def _recorded_call(
    call: ProviderCall,
    span_name: str,
    original: Callable[..., Any],
    resource: Any,
    kwargs: Mapping[str, Any],
) -> Any:
    session = subtree.current_session()
    owner = getattr(session, "owner", None)
    ownership = take_node_ownership()
    if (
        session is None
        or owner is None
        or ownership == NODE_OMITS_CALL
        or kwargs.get("stream")
        or not call.handles(resource)
        or framework_records_call()
    ):
        return None
    if ownership == NODE_RECORDS_CALL:
        return owner._provider_auto_run(call, span_name, original)
    if CREATE in session.exclude or span_name in session.exclude:
        return None
    if not subtree.admits_discovered_call(session, span_name):
        return None
    return owner._provider_auto_traced_call(call, span_name, original)


def is_async_create(original: Callable[..., Any]) -> bool:
    return inspect.iscoroutinefunction(inspect.unwrap(original))


def _patched_create(call: ProviderCall, cls: type, original: Callable[..., Any]) -> Any:
    span_name = f"{cls.__name__}.{CREATE}"

    if is_async_create(original):

        @functools.wraps(original)
        async def async_patched(self: Any, *args: Any, **kwargs: Any) -> Any:
            recorded = _recorded_call(call, span_name, original, self, kwargs)
            if recorded is None:
                return await original(self, *args, **kwargs)
            return await recorded(self, *args, **kwargs)

        patched: Callable[..., Any] = async_patched
    else:

        @functools.wraps(original)
        def sync_patched(self: Any, *args: Any, **kwargs: Any) -> Any:
            recorded = _recorded_call(call, span_name, original, self, kwargs)
            if recorded is None:
                return original(self, *args, **kwargs)
            return recorded(self, *args, **kwargs)

        patched = sync_patched

    renamed(patched, CREATE, CALL_MARKER)
    setattr(patched, CALL_MARKER, call)
    return patched


def patch_client_class(call: ProviderCall, cls: type) -> None:
    with _lock:
        if cls.__dict__.get(PATCHED_MARKER) is True:
            return
        original = cls.__dict__.get(CREATE)
        if inspect.isfunction(original):
            setattr(cls, CREATE, _patched_create(call, cls, original))
        setattr(cls, PATCHED_MARKER, True)


def patch_module(module: Any) -> None:
    call = _BY_MODULE.get(getattr(module, "__name__", ""))
    if call is None:
        return
    for class_name in call.classes:
        cls = getattr(module, class_name, None)
        if inspect.isclass(cls):
            patch_client_class(call, cls)


def instrument_loaded_clients() -> None:
    for module_name in _BY_MODULE:
        module = sys.modules.get(module_name)
        if module is None:
            continue
        with contextlib.suppress(Exception):
            patch_module(module)


def provider_of(fn: Any) -> ProviderCall | None:
    call = getattr(fn, CALL_MARKER, None)
    return call if isinstance(call, ProviderCall) else None


def resolve_call_target(fn: Any) -> Any:
    if provider_of(fn) is not None:
        return fn
    resource = getattr(fn, "__self__", None)
    function = getattr(fn, "__func__", None)
    if resource is None or getattr(function, "__name__", None) != CREATE:
        return None
    instrument_loaded_clients()
    cls = type(resource)
    patched = getattr(cls, CREATE, None)
    if provider_of(patched) is None:
        return None
    return patched.__get__(resource, cls)


_finder = PatchingFinder(lambda fullname: fullname in _BY_MODULE, patch_module)


def install_import_hook() -> None:
    _finder.install()
