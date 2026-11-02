from __future__ import annotations

from typing import Any

import pytest
from matrx_connect.context.app_context import (
    AppContext,
    clear_app_context,
    get_app_context,
    set_app_context,
)
from matrx_connect.context.error_buffer import buffer_error_events


class _RecordingEmitter:
    def __init__(self) -> None:
        self.errors: list[dict[str, Any]] = []
        self.data: list[Any] = []

    async def send_error(
        self,
        error_type: str,
        message: str,
        user_message: str | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.errors.append(
            {
                "error_type": error_type,
                "message": message,
                "user_message": user_message,
                "code": code,
                "details": details,
            }
        )

    async def send_data(self, payload: Any) -> None:
        self.data.append(payload)


@pytest.mark.asyncio
async def test_buffer_replays_errors_after_success_and_forwards_other_events() -> None:
    emitter = _RecordingEmitter()
    context = AppContext(emitter=emitter)
    token = set_app_context(context)
    try:
        async with buffer_error_events() as buffer:
            scoped_emitter = get_app_context().emitter
            await scoped_emitter.send_data({"progress": 1})
            await scoped_emitter.send_error("provider_stream", "stream failed")
            assert emitter.errors == []
            assert len(buffer.errors) == 1

        assert get_app_context() is context
        assert emitter.data == [{"progress": 1}]
        assert [error["error_type"] for error in emitter.errors] == ["provider_stream"]
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_buffer_discards_errors_after_exception_and_restores_context() -> None:
    emitter = _RecordingEmitter()
    context = AppContext(emitter=emitter)
    token = set_app_context(context)
    try:
        with pytest.raises(RuntimeError, match="retry me"):
            async with buffer_error_events():
                await get_app_context().emitter.send_error("rate_limit", "provisional")
                raise RuntimeError("retry me")

        assert get_app_context() is context
        assert emitter.errors == []
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_nested_buffers_restore_exact_context_and_replay_once() -> None:
    emitter = _RecordingEmitter()
    context = AppContext(emitter=emitter)
    token = set_app_context(context)
    try:
        async with buffer_error_events():
            outer_emitter = get_app_context().emitter
            async with buffer_error_events():
                await get_app_context().emitter.send_error("terminal", "reported")
            assert get_app_context().emitter is outer_emitter
            assert emitter.errors == []

        assert get_app_context() is context
        assert [error["error_type"] for error in emitter.errors] == ["terminal"]
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_direct_error_outside_buffer_is_not_suppressed() -> None:
    emitter = _RecordingEmitter()
    await emitter.send_error("direct_media_error", "failed")
    assert [error["error_type"] for error in emitter.errors] == ["direct_media_error"]


@pytest.mark.asyncio
async def test_successful_scope_replays_at_most_one_terminal_error() -> None:
    emitter = _RecordingEmitter()
    token = set_app_context(AppContext(emitter=emitter))
    try:
        async with buffer_error_events():
            await get_app_context().emitter.send_error("first", "first")
            await get_app_context().emitter.send_error("duplicate", "duplicate")
    finally:
        clear_app_context(token)

    assert [error["error_type"] for error in emitter.errors] == ["first"]
