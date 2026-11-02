from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

from matrx_utils import vcprint

from matrx_connect.context.app_context import (
    clear_app_context,
    get_app_context,
    set_app_context,
)
from matrx_connect.context.emitter_protocol import Emitter


@dataclass(frozen=True)
class BufferedErrorEvent:
    error_type: str
    message: str
    user_message: str | None = None
    code: str | None = None
    details: dict[str, Any] | None = None


class BufferedErrorEmitter:
    """Emitter overlay that buffers ERROR events while forwarding everything else."""

    def __init__(self, emitter: Emitter) -> None:
        self._emitter = emitter
        self._errors: list[BufferedErrorEvent] = []

    @property
    def errors(self) -> tuple[BufferedErrorEvent, ...]:
        return tuple(self._errors)

    async def send_error(
        self,
        error_type: str,
        message: str,
        user_message: str | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self._errors.append(
            BufferedErrorEvent(
                error_type=error_type,
                message=message,
                user_message=user_message,
                code=code,
                details=details,
            )
        )

    async def replay(self) -> None:
        errors, self._errors = self._errors, []
        if not errors:
            return
        if len(errors) > 1:
            vcprint(
                {
                    "first_error_type": errors[0].error_type,
                    "suppressed_error_types": [error.error_type for error in errors[1:]],
                },
                "[BufferedErrorEmitter] Multiple terminal errors returned normally; replaying first",
                color="red",
            )
        error = errors[0]
        await self._emitter.send_error(
            error.error_type,
            error.message,
            error.user_message,
            error.code,
            error.details,
        )

    def discard(self) -> None:
        if self._errors:
            vcprint(
                {
                    "count": len(self._errors),
                    "error_types": [error.error_type for error in self._errors],
                },
                "[BufferedErrorEmitter] Discarding provisional errors after exception",
                color="yellow",
                verbose=True,
            )
        self._errors.clear()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._emitter, name)


@asynccontextmanager
async def buffer_error_events() -> AsyncIterator[BufferedErrorEmitter]:
    """Buffer ERROR events, replaying on success and discarding on exception.

    This gives retry owners a scoped error boundary: provisional errors emitted
    by a failing attempt never escape, while a provider that reports an error
    without raising still reaches the client. All non-error events pass through
    immediately.
    """

    context = get_app_context()
    overlay = BufferedErrorEmitter(context.emitter)
    token = set_app_context(context.with_overrides(emitter=overlay))
    try:
        yield overlay
    except BaseException:
        overlay.discard()
        raise
    finally:
        clear_app_context(token)
    await overlay.replay()
