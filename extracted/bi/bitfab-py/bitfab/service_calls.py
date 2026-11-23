from __future__ import annotations

import functools
import sys
import threading
import weakref
from collections.abc import Callable
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

from bitfab.constants import _replay_context, replay_item_is_running
from bitfab.sandbox import SANDBOX_SESSION_KEY
from bitfab.warn_once import warn_once


@dataclass(frozen=True)
class ServiceCall:
    integration: str
    method: str
    params: dict[str, Any]
    send: Callable[[], Any]
    request: Any = None


class ServiceCallHeldBackError(RuntimeError):
    pass


_lock = threading.Lock()
_clients: list[weakref.ReferenceType[Any]] = []
_traced: dict[tuple[int, str], Any] = {}
_current: ContextVar[ServiceCall | None] = ContextVar(
    "bitfab_current_service_call", default=None
)
content_withheld: ContextVar[str | None] = ContextVar(
    "bitfab_service_call_content_withheld", default=None
)


def register_client(client: Any) -> None:
    with _lock:
        _clients[:] = [ref for ref in _clients if ref() is not None]
        _clients.append(weakref.ref(client))


def _alive_clients() -> list[Any]:
    with _lock:
        alive = [ref() for ref in reversed(_clients)]
    return [client for client in alive if client is not None]


def _records(client: Any, integration: str) -> bool:
    return integration not in getattr(client, "_disabled_integrations", ())


def _warn_recording_off_by_default(integration: str) -> None:
    newest = next(iter(_alive_clients()), None)
    if integration not in getattr(newest, "_integrations_off_by_default", ()):
        return
    warn_once(
        f"integration-off-by-default:{integration}",
        f"a {integration} call ran inside a trace and was not recorded, because "
        f"Bitfab records {integration} calls only once you turn them on (they "
        f"carry your users' data). Without them, replays of this trace start "
        f"the {integration} sandbox with nothing the original run read. Turn "
        f'recording on with Bitfab(integrations={{"{integration}": True}}) or '
        f"BITFAB_ENABLED_INTEGRATIONS={integration}; turn it off by name "
        f'(integrations={{"{integration}": False}}) to stop this warning.',
    )


def current_call() -> ServiceCall | None:
    return _current.get()


def replaying() -> bool:
    return _replay_context.get() is not None or replay_item_is_running()


def _inside_trace() -> bool:
    from_client = sys.modules.get("bitfab.client")
    return from_client is not None and bool(from_client._get_span_stack())


def _send_current(**_params: Any) -> Any:
    call = _current.get()
    if call is None:
        raise RuntimeError("Bitfab could not find the service call to send.")
    if replaying():
        raise ServiceCallHeldBackError(
            f"{call.method} was held back during replay so it never reaches the "
            "real service: no sandbox answered it and the original trace has no "
            "recorded output for it. Pass a sandbox for this service to replay, "
            "or record the call on the original trace."
        )
    return call.send()


def _traced_call(client: Any, method: str) -> Any:
    key = (id(client), method)
    traced = _traced.get(key)
    if traced is None:
        runner = functools.partial(_send_current)
        functools.update_wrapper(runner, _send_current)
        runner.__name__ = method.replace(".", "_")  # type: ignore[attr-defined]
        traced = client.get_function(method).span(
            name=method, type="function", mock_on_replay=True
        )(runner)
        _traced[key] = traced
    return traced


def _recording_client(integration: str) -> Any:
    client = next((c for c in _alive_clients() if _records(c, integration)), None)
    if client is not None and _inside_trace():
        return client
    if client is None and _inside_trace():
        _warn_recording_off_by_default(integration)
    return None


def is_recorded(integration: str) -> bool:
    if _replay_context.get() is not None or replay_item_is_running():
        return True
    return _recording_client(integration) is not None


def run(call: ServiceCall) -> Any:
    replay_ctx = _replay_context.get()
    if replay_ctx is not None:
        session = replay_ctx.get(SANDBOX_SESSION_KEY)
        alive = _alive_clients()
        client = getattr(session, "client", None) or (alive[0] if alive else None)
        if client is None:
            raise ServiceCallHeldBackError(
                f"{call.method} was held back during replay: no Bitfab client is set up."
            )
    elif replay_item_is_running():
        raise ServiceCallHeldBackError(
            f"{call.method} was held back: a replay is running in this process and "
            "this call carries no replay context, so Bitfab cannot tell it apart "
            "from a call the replay made. Make the call inside the replayed "
            "function's context, for example by passing it along with "
            "contextvars.copy_context() when handing work to another thread."
        )
    else:
        client = _recording_client(call.integration)
        if client is None:
            return call.send()
    tokens = (
        _current.set(call),
        content_withheld.set(
            None if _records(client, call.integration) else call.integration
        ),
    )
    try:
        return _traced_call(client, call.method)(**call.params)
    finally:
        content_withheld.reset(tokens[1])
        _current.reset(tokens[0])
