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

OPENROUTER_PROVIDER = "openrouter"
OPENROUTER_HOSTNAME = "openrouter.ai"
OPENAI_COMPLETIONS_MODULE = "openai.resources.chat.completions.completions"
COMPLETIONS_CLASSES = ("Completions", "AsyncCompletions")
CREATE = "create"
PATCHED_MARKER = "_bitfab_openrouter_auto_traced"
OPENROUTER_CALL_MARKER = "_bitfab_openrouter_call"

_LANGCHAIN_CHAT_MODEL_FRAMES = frozenset(
    {"_generate_with_cache", "_agenerate_with_cache"}
)

_lock = threading.Lock()
_wrapper_call: contextvars.ContextVar[WrapperCall | None] = contextvars.ContextVar(
    "bitfab_openrouter_wrapper_call", default=None
)


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


def is_openrouter_resource(resource: Any) -> bool:
    base_url = getattr(getattr(resource, "_client", None), "base_url", None)
    host = getattr(base_url, "host", None)
    return isinstance(host, str) and (
        host == OPENROUTER_HOSTNAME or host.endswith(f".{OPENROUTER_HOSTNAME}")
    )


def looks_like_completion(response: Any) -> bool:
    return isinstance(_field(response, "choices"), (list, tuple))


def prompt_from_request(request: Mapping[str, Any]) -> str | None:
    messages = request.get("messages")
    if not isinstance(messages, (list, tuple)):
        return None
    rendered = []
    for message in messages:
        role = _field(message, "role")
        if not isinstance(role, str):
            continue
        content = _field(message, "content")
        rendered.append(
            {
                "role": role,
                "content": content
                if isinstance(content, str)
                else json.dumps(content, default=str),
            }
        )
    return json.dumps(rendered) if rendered else None


def context_from_response(
    request: Mapping[str, Any], response: Any, duration_ms: int
) -> dict[str, Any]:
    context: dict[str, Any] = {"provider": OPENROUTER_PROVIDER}
    model = _field(response, "model") or request.get("model")
    if isinstance(model, str) and model:
        context["model"] = model
    upstream_provider = _field(response, "provider")
    if isinstance(upstream_provider, str) and upstream_provider:
        context["upstreamProvider"] = upstream_provider

    usage = _field(response, "usage")
    fields = {
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
    context.update({key: value for key, value in fields.items() if value is not None})
    context["durationMs"] = duration_ms
    return context


def request_of(args: tuple[Any, ...], kwargs: Mapping[str, Any]) -> Mapping[str, Any]:
    if "messages" in kwargs or not args or not isinstance(args[0], Mapping):
        return kwargs
    return args[0]


def record_completion(
    span: Any, request: Mapping[str, Any], response: Any, duration_ms: int
) -> None:
    if not looks_like_completion(response):
        return
    with contextlib.suppress(Exception):
        prompt = prompt_from_request(request)
        if prompt:
            span.set_prompt(prompt)
        span.add_context(context_from_response(request, response, duration_ms))


def record_auto_traced_completion(
    span: Any, request: Mapping[str, Any], response: Any, duration_ms: int
) -> None:
    record_completion(span, request, response, duration_ms)
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
        or not is_openrouter_resource(resource)
        or framework_records_call()
    ):
        return None
    if ownership == NODE_RECORDS_CALL:
        return owner._openrouter_auto_run(span_name, original)
    if CREATE in session.exclude or span_name in session.exclude:
        return None
    if not subtree.admits_discovered_call(session, span_name):
        return None
    return owner._openrouter_auto_traced_call(span_name, original)


def is_async_create(original: Callable[..., Any]) -> bool:
    return inspect.iscoroutinefunction(inspect.unwrap(original))


def _patched_create(cls: type, original: Callable[..., Any]) -> Any:
    span_name = f"{cls.__name__}.{CREATE}"

    if is_async_create(original):

        @functools.wraps(original)
        async def async_patched(self: Any, *args: Any, **kwargs: Any) -> Any:
            recorded = _recorded_call(span_name, original, self, kwargs)
            if recorded is None:
                return await original(self, *args, **kwargs)
            return await recorded(self, *args, **kwargs)

        return renamed(async_patched, CREATE, OPENROUTER_CALL_MARKER)

    @functools.wraps(original)
    def sync_patched(self: Any, *args: Any, **kwargs: Any) -> Any:
        recorded = _recorded_call(span_name, original, self, kwargs)
        if recorded is None:
            return original(self, *args, **kwargs)
        return recorded(self, *args, **kwargs)

    return renamed(sync_patched, CREATE, OPENROUTER_CALL_MARKER)


def patch_client_class(cls: type) -> None:
    with _lock:
        if cls.__dict__.get(PATCHED_MARKER) is True:
            return
        original = cls.__dict__.get(CREATE)
        if inspect.isfunction(original):
            setattr(cls, CREATE, _patched_create(cls, original))
        setattr(cls, PATCHED_MARKER, True)


def patch_module(module: Any) -> None:
    for class_name in COMPLETIONS_CLASSES:
        cls = getattr(module, class_name, None)
        if inspect.isclass(cls):
            patch_client_class(cls)


def instrument_loaded_clients() -> None:
    module = sys.modules.get(OPENAI_COMPLETIONS_MODULE)
    if module is None:
        return
    with contextlib.suppress(Exception):
        patch_module(module)


def resolve_call_target(fn: Any) -> Any:
    if getattr(fn, OPENROUTER_CALL_MARKER, False) is True:
        return fn
    resource = getattr(fn, "__self__", None)
    function = getattr(fn, "__func__", None)
    if resource is None or getattr(function, "__name__", None) != CREATE:
        return None
    instrument_loaded_clients()
    cls = type(resource)
    patched = getattr(cls, CREATE, None)
    if getattr(patched, OPENROUTER_CALL_MARKER, False) is not True:
        return None
    return patched.__get__(resource, cls)


_finder = PatchingFinder(
    lambda fullname: fullname == OPENAI_COMPLETIONS_MODULE, patch_module
)


def install_import_hook() -> None:
    _finder.install()
