"""Serve a schedule function by calling the `@schedule` handlers it imported.

A Python schedule in `vercel.json` names a module. Importing it registers its
schedules with `vercel.schedules`, and the build deploys each one as
`<service>.<schedule name>` after the schedule's service. The build packs
schedules with the same function settings into one function. Each firing is a
binary-mode CloudEvent with no body, and its schedule name selects the handler.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable, Collection, Mapping
from contextlib import AbstractContextManager
from importlib import import_module
from typing import Any, Protocol, cast

type _ASGIMessage = dict[str, Any]
type _ASGIReceive = Callable[[], Awaitable[_ASGIMessage]]
type _ASGISend = Callable[[_ASGIMessage], Awaitable[None]]


class _Metadata(Protocol):
    @property
    def name(self) -> str: ...


class _Handler(Protocol):
    @property
    def name(self) -> str: ...

    def run(self, metadata: Any, /) -> Awaitable[None]: ...


type _FromHeaders = Callable[[Mapping[str, str]], _Metadata]
type _HeadersContext = Callable[
    [Mapping[str, str]], AbstractContextManager[None]
]

_schedule_log = logging.getLogger("vercel.schedules")


class _ScheduleServiceApp:
    """Platform-owned ASGI app that runs one `@schedule` handler per firing."""

    def __init__(
        self,
        *,
        handlers: Mapping[str, _Handler],
        unregistered: Collection[str],
        from_headers: _FromHeaders,
        headers_context: _HeadersContext,
        bad_request_exceptions: tuple[type[BaseException], ...],
    ) -> None:
        self._handlers = dict(handlers)
        self._unregistered = frozenset(unregistered)
        self._from_headers = from_headers
        self._headers_context = headers_context
        self._bad_request_exceptions = bad_request_exceptions

    async def __call__(
        self,
        scope: dict[str, Any],
        receive: _ASGIReceive,
        send: _ASGISend,
    ) -> None:
        scope_type = scope.get("type")
        if scope_type == "lifespan":
            await _handle_lifespan(receive, send)
            return
        if scope_type != "http":
            raise RuntimeError(
                f'unsupported schedule ASGI scope type "{scope_type}"'
            )
        if scope.get("method") != "POST":
            await _send_status(send, 405)
            return

        headers = _headers_from_scope(scope)
        try:
            metadata = self._from_headers(headers)
        except self._bad_request_exceptions as exc:
            _schedule_log.warning("schedule dispatch rejected: %s", exc)
            await _send_status(send, 400)
            return
        handler = self._handlers.get(metadata.name)
        if handler is None and metadata.name in self._unregistered:
            # The build deployed this schedule, so the module is at fault, not
            # the firing.
            _schedule_log.error(
                'could not run schedule "%s": its module registered it at '
                "build but not at runtime",
                metadata.name,
            )
            await _send_status(send, 500)
            return
        if handler is None:
            served = ", ".join(f'"{name}"' for name in sorted(self._handlers))
            _schedule_log.warning(
                'schedule dispatch rejected: unrecognized schedule "%s": '
                "this function runs %s",
                metadata.name,
                served,
            )
            await _send_status(send, 400)
            return

        try:
            # SDK clients in the handler read the firing's OIDC token from the
            # request headers.
            with self._headers_context(headers):
                await handler.run(metadata)
        except Exception:
            _schedule_log.exception('schedule "%s" failed', metadata.name)
            await _send_status(send, 500)
            return
        await _send_status(send, 200)


async def _handle_lifespan(receive: _ASGIReceive, send: _ASGISend) -> None:
    while True:
        message = await receive()
        message_type = message.get("type")
        if message_type == "lifespan.startup":
            await send({"type": "lifespan.startup.complete"})
        elif message_type == "lifespan.shutdown":
            await send({"type": "lifespan.shutdown.complete"})
            return


def _headers_from_scope(scope: Mapping[str, Any]) -> dict[str, str]:
    raw_headers = cast("list[tuple[bytes, bytes]]", scope.get("headers", []))
    return {
        name.decode("latin-1").lower(): value.decode("latin-1")
        for name, value in raw_headers
    }


async def _send_status(send: _ASGISend, status: int) -> None:
    headers = [(b"allow", b"POST")] if status == 405 else []
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": headers,
        }
    )
    await send({"type": "http.response.body", "body": b""})


def create_schedule_service_app(
    service: str, schedules: Collection[str] | None = None
) -> object:
    """Create the app that serves the schedules registered so far.

    Each schedule is deployed as `<service>.<schedule name>`. The build packs
    schedules with different function settings into different functions, and
    passes each function the names of its `schedules`.
    """
    try:
        headers_module = cast("Any", import_module("vercel.headers"))
        schedules_module = cast("Any", import_module("vercel.schedules"))
    except ImportError as exc:
        raise RuntimeError(
            'Unable to serve schedules because "vercel-schedules" is '
            'missing. Install "vercel-schedules" to declare schedules with '
            "@schedule."
        ) from exc

    registered = cast(
        "tuple[_Handler, ...]", schedules_module.get_registered_schedules()
    )
    served = [
        handler
        for handler in registered
        if schedules is None or handler.name in schedules
    ]
    if not served:
        raise RuntimeError(
            f'service "{service}" registered no schedules: its entrypoint '
            "must declare at least one with @schedule"
        )
    unregistered = set(schedules or ()) - {handler.name for handler in served}
    headers_context_type = headers_module.HeadersContext

    def use_headers(
        headers: Mapping[str, str],
    ) -> AbstractContextManager[None]:
        context = headers_context_type(headers).use()
        return cast("AbstractContextManager[None]", context)

    return _ScheduleServiceApp(
        handlers={f"{service}.{handler.name}": handler for handler in served},
        unregistered={f"{service}.{name}" for name in unregistered},
        from_headers=cast(
            "_FromHeaders", schedules_module.ScheduleMetadata.from_headers
        ),
        headers_context=use_headers,
        bad_request_exceptions=(schedules_module.ScheduleEventParseError,),
    )
