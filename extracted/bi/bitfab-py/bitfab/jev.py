from __future__ import annotations

import contextlib
import contextvars
import functools
import inspect
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

JEV_PROVIDER = "typesafe"
TYPESAFE_MODULE = "typesafe_sdk"
TYPESAFE_CLIENT_CLASSES = ("TypeSafeClient", "AsyncTypeSafeClient")
SYSTEM_ONE = "system_one"
PATCHED_MARKER = "_bitfab_jev_auto_traced"
JEV_CALL_MARKER = "_bitfab_jev_call"

_lock = threading.Lock()
_wrapper_call: contextvars.ContextVar[WrapperCall | None] = contextvars.ContextVar(
    "bitfab_jev_wrapper_call", default=None
)


@dataclass
class WrapperCall:
    recorded_replies: list[Any] = field(default_factory=list)

    def recorded(self) -> bool:
        return bool(self.recorded_replies)


@contextlib.contextmanager
def wrapper_call() -> Iterator[WrapperCall]:
    call = WrapperCall()
    token = _wrapper_call.set(call)
    try:
        yield call
    finally:
        _wrapper_call.reset(token)


def _mark_recorded(reply: Any) -> None:
    call = _wrapper_call.get()
    if call is not None:
        call.recorded_replies.append(reply)


def _field(value: Any, key: str) -> Any:
    if isinstance(value, Mapping):
        return value.get(key)
    return getattr(value, key, None)


def _token_count(usage: Any, key: str) -> int | float | None:
    count = _field(usage, key)
    if isinstance(count, bool) or not isinstance(count, (int, float)):
        return None
    return count


def jev_context(reply: Any, duration_ms: int) -> dict[str, Any] | None:
    if reply is None or isinstance(reply, (str, bytes, int, float)):
        return None
    context: dict[str, Any] = {}
    model = _field(reply, "model")
    if isinstance(model, str):
        context["model"] = model
    context["provider"] = JEV_PROVIDER
    usage = _field(reply, "usage")
    input_tokens = _token_count(usage, "input_tokens")
    output_tokens = _token_count(usage, "output_tokens")
    if input_tokens is not None:
        context["inputTokens"] = input_tokens
    if output_tokens is not None:
        context["outputTokens"] = output_tokens
    context["durationMs"] = duration_ms
    return context


def looks_like_reply(reply: Any) -> bool:
    if reply is None or isinstance(reply, (str, bytes, int, float)):
        return False
    if not isinstance(_field(reply, "model"), str):
        return False
    usage = _field(reply, "usage")
    return usage is not None and not isinstance(usage, (str, bytes, int, float))


def _discovered_context(reply: Any, duration_ms: int) -> dict[str, Any] | None:
    if not looks_like_reply(reply):
        return None
    return jev_context(reply, duration_ms)


def record_reply(span: Any, reply: Any, duration_ms: int) -> None:
    try:
        context = jev_context(reply, duration_ms)
        if context is not None:
            span.add_context(context)
    except Exception:
        pass


def record_auto_traced_reply(span: Any, reply: Any, duration_ms: int) -> None:
    record_reply(span, reply, duration_ms)
    subtree.mark_usage_recorded()
    _mark_recorded(reply)


subtree.read_results_of(
    SYSTEM_ONE,
    subtree.ResultReader(
        read=_discovered_context, span_type="llm", recorded=_mark_recorded
    ),
)


def _recorded_call(span_name: str, original: Callable[..., Any]) -> Any:
    session = subtree.current_session()
    owner = getattr(session, "owner", None)
    ownership = take_node_ownership()
    if session is None or owner is None or ownership == NODE_OMITS_CALL:
        return None
    if ownership == NODE_RECORDS_CALL:
        return owner._jev_auto_run(span_name, original)
    if SYSTEM_ONE in session.exclude:
        return None
    if not subtree.admits_discovered_call(session, span_name):
        return None
    return owner._jev_auto_traced_call(span_name, original)


def _patched_system_one(cls: type, original: Callable[..., Any]) -> Any:
    span_name = f"{cls.__name__}.{SYSTEM_ONE}"

    if inspect.iscoroutinefunction(original):

        @functools.wraps(original)
        async def async_patched(self: Any, *args: Any, **kwargs: Any) -> Any:
            recorded = _recorded_call(span_name, original)
            if recorded is None:
                return await original(self, *args, **kwargs)
            return await recorded(self, *args, **kwargs)

        return renamed(async_patched, SYSTEM_ONE, JEV_CALL_MARKER)

    @functools.wraps(original)
    def sync_patched(self: Any, *args: Any, **kwargs: Any) -> Any:
        recorded = _recorded_call(span_name, original)
        if recorded is None:
            return original(self, *args, **kwargs)
        return recorded(self, *args, **kwargs)

    return renamed(sync_patched, SYSTEM_ONE, JEV_CALL_MARKER)


def patch_client_class(cls: type) -> None:
    with _lock:
        if cls.__dict__.get(PATCHED_MARKER) is True:
            return
        original = cls.__dict__.get(SYSTEM_ONE)
        if inspect.isfunction(original):
            setattr(cls, SYSTEM_ONE, _patched_system_one(cls, original))
        setattr(cls, PATCHED_MARKER, True)


def patch_module(module: Any) -> None:
    for class_name in TYPESAFE_CLIENT_CLASSES:
        cls = getattr(module, class_name, None)
        if inspect.isclass(cls):
            patch_client_class(cls)


def instrument_loaded_clients() -> None:
    module = sys.modules.get(TYPESAFE_MODULE)
    if module is None:
        return
    with contextlib.suppress(Exception):
        patch_module(module)


def resolve_call_target(fn: Any) -> Any:
    if getattr(fn, JEV_CALL_MARKER, False) is True:
        return fn
    client = getattr(fn, "__self__", None)
    function = getattr(fn, "__func__", None)
    if client is None or getattr(function, "__name__", None) != SYSTEM_ONE:
        return None
    instrument_loaded_clients()
    cls = type(client)
    patched = getattr(cls, SYSTEM_ONE, None)
    if getattr(patched, JEV_CALL_MARKER, False) is not True:
        return None
    return patched.__get__(client, cls)


_finder = PatchingFinder(lambda fullname: fullname == TYPESAFE_MODULE, patch_module)


def install_import_hook() -> None:
    _finder.install()
