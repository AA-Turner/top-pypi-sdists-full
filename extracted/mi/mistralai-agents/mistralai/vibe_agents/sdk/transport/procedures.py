"""The App Server procedures an Agents SDK session can call, on every host."""

from collections.abc import AsyncIterator
from typing import cast

from mistralai.vibe.harness.app_server.session import (
    CallbacksTreeParams,
    CallbacksTreeResponse,
    ClientTransportStreamItem,
    EventsReadParams,
    InfoResponse,
    SessionModel,
    SessionTransport,
)
from mistralai.vibe_agents.sdk.authoring.errors import UnsupportedSessionProcedureError

SESSION_PROCEDURES = (
    "app_server/session/start",
    "app_server/session/read",
    "app_server/session/history/list",
    "app_server/session/turns/list",
    "app_server/session/message/send",
    "app_server/session/turn/start",
    "app_server/session/turn/steer",
    "app_server/session/turn/interrupt",
    "app_server/session/cancel",
    "app_server/session/callback/result",
    "app_server/session/callbacks/tree",
    "app_server/session/events/read",
)
SDK_PROCEDURES = frozenset(
    {
        "app_server/info",
        "app_server/subagents/list",
        "app_server/catalog/list",
        "app_server/catalog/rename",
        "app_server/catalog/archive",
        *SESSION_PROCEDURES,
    }
)
# Editing a session's configuration works only where the session runs in this process.
LOCAL_PROCEDURES = SDK_PROCEDURES | {"app_server/session/config/read", "app_server/session/config/write"}


def refuse_unlisted_procedure(method: str, *, backend: str, procedures: frozenset[str] = SDK_PROCEDURES) -> None:
    """Raise if `method` is not in `procedures`, the ones a session can call on this host."""
    if method not in procedures:
        raise UnsupportedSessionProcedureError(
            method=method,
            backend=backend,
            reason=(
                "the Agents SDK calls this procedure only on local sessions"
                if method in LOCAL_PROCEDURES
                else "the Agents SDK does not call this procedure"
            ),
        )


def _advertise_sdk_procedures(info: InfoResponse, allowed: frozenset[str]) -> InfoResponse:
    """Keep only the procedures in `allowed` in the host's capabilities."""
    capabilities = {}
    for namespace, capability in info.capabilities.items():
        procedures = capability.get("procedures")
        if isinstance(procedures, list):
            capability = {**capability, "procedures": [method for method in procedures if method in allowed]}
        capabilities[namespace] = capability
    return info.model_copy(update={"capabilities": capabilities})


class AllowlistedSessionTransport(SessionTransport):
    """Pass the calls to the given procedures, `SDK_PROCEDURES` by default, to another transport; refuse the others."""

    def __init__(
        self, transport: SessionTransport, *, backend: str, procedures: frozenset[str] = SDK_PROCEDURES
    ) -> None:
        self._transport = transport
        self._backend = backend
        self._procedures = procedures

    @property
    def inner(self) -> SessionTransport:
        """The transport under this guard."""
        return self._transport

    async def request[ResultT: SessionModel](
        self, method: str, params: SessionModel, result_type: type[ResultT]
    ) -> ResultT:
        refuse_unlisted_procedure(method, backend=self._backend, procedures=self._procedures)
        result = await self._transport.request(method, params, result_type)
        if isinstance(result, InfoResponse):
            return cast(ResultT, _advertise_sdk_procedures(result, self._procedures))
        return result

    def read_events(self, params: EventsReadParams) -> AsyncIterator[ClientTransportStreamItem]:
        return self._transport.read_events(params)

    def watch_callbacks_tree(self, params: CallbacksTreeParams) -> AsyncIterator[CallbacksTreeResponse]:
        method = "app_server/session/callbacks/tree"
        refuse_unlisted_procedure(method, backend=self._backend, procedures=self._procedures)
        # A transport that follows `SessionTransport` without subclassing it may not watch the tree.
        watch = getattr(self._transport, "watch_callbacks_tree", None)
        if watch is None:
            raise UnsupportedSessionProcedureError(
                method=method,
                backend=self._backend,
                reason="this transport cannot follow the callbacks of a Session tree",
            )
        return watch(params)

    async def close(self) -> None:
        await self._transport.close()


__all__ = [
    "LOCAL_PROCEDURES",
    "SDK_PROCEDURES",
    "SESSION_PROCEDURES",
    "AllowlistedSessionTransport",
    "refuse_unlisted_procedure",
]
