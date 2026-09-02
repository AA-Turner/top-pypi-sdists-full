"""SSE parsing tests."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Literal

import pytest
from httpx_sse import ServerSentEvent

from hogland._models import ExecEvent
from hogland._sse import AsyncStreamResult, StreamResult, parse_event

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator

_EventKind = Literal["stdout", "stderr", "exit"]


def _sse(event: str, data: str) -> ServerSentEvent:
    return ServerSentEvent(event=event, data=data)


def test_parse_stdout_event() -> None:
    ev = parse_event(_sse("stdout", "hello\n"))
    assert ev.kind == "stdout"
    assert ev.data == "hello\n"


def test_parse_stderr_event() -> None:
    ev = parse_event(_sse("stderr", "oh no"))
    assert ev.kind == "stderr"
    assert ev.data == "oh no"


def test_parse_exit_event() -> None:
    ev = parse_event(_sse("exit", json.dumps({"code": 0, "duration_ms": 42})))
    assert ev.kind == "exit"
    assert ev.exit_code == 0
    assert ev.duration_ms == 42


def test_parse_exit_event_missing_payload() -> None:
    ev = parse_event(_sse("exit", ""))
    assert ev.kind == "exit"
    assert ev.exit_code is None
    assert ev.duration_ms is None


def test_unknown_event_raises() -> None:
    with pytest.raises(ValueError, match="unknown SSE event kind"):
        parse_event(_sse("ping", "x"))


# ---------- StreamResult ---------------------------------------------------


def _events(*frames: tuple[_EventKind, str | int | None]) -> Iterator[ExecEvent]:
    """Build a synthetic ExecEvent iterator from (kind, payload) tuples.

    For ``stdout`` / ``stderr`` the payload is a string chunk. For
    ``exit`` the payload is the exit_code (or None for missing).
    """
    for kind, payload in frames:
        if kind == "exit":
            yield ExecEvent(
                kind="exit",
                exit_code=payload if isinstance(payload, int) else None,
                duration_ms=42,
            )
        else:
            assert isinstance(payload, str)
            yield ExecEvent(kind=kind, data=payload)


def test_stream_result_yields_stdout_and_buffers_stderr() -> None:
    sr = StreamResult(
        _events(
            ("stdout", "hello "),
            ("stderr", "warn:"),
            ("stdout", "world\n"),
            ("stderr", " bad\n"),
            ("exit", 0),
        ),
    )
    chunks = list(sr.stdout())
    assert chunks == ["hello ", "world\n"]
    assert sr.stderr == "warn: bad\n"
    assert sr.exit_code == 0
    assert sr.duration_ms == 42


def test_stream_result_drain_silences_stdout() -> None:
    sr = StreamResult(
        _events(("stdout", "noise"), ("stderr", "buf"), ("exit", 7)),
    ).drain()
    assert sr.exit_code == 7
    assert sr.stderr == "buf"


def test_stream_result_double_consume_raises() -> None:
    sr = StreamResult(_events(("stdout", "x"), ("exit", 0)))
    list(sr.stdout())
    with pytest.raises(RuntimeError, match="already consumed"):
        list(sr.stdout())


def test_stream_result_handles_no_exit_event() -> None:
    # If the server crashes mid-stream and no exit event arrives, we
    # still surface buffered stderr and leave exit_code/duration_ms None.
    sr = StreamResult(_events(("stdout", "x"), ("stderr", "y")))
    chunks = list(sr.stdout())
    assert chunks == ["x"]
    assert sr.stderr == "y"
    assert sr.exit_code is None
    assert sr.duration_ms is None


# ---------- AsyncStreamResult ----------------------------------------------


async def _aevents(*frames: tuple[_EventKind, str | int | None]) -> AsyncIterator[ExecEvent]:
    for ev in _events(*frames):
        yield ev


async def test_async_stream_result_basic() -> None:
    sr = AsyncStreamResult(
        _aevents(
            ("stdout", "a"),
            ("stderr", "e"),
            ("stdout", "b"),
            ("exit", 1),
        ),
    )
    chunks = [c async for c in sr.stdout()]
    assert chunks == ["a", "b"]
    assert sr.stderr == "e"
    assert sr.exit_code == 1
    assert sr.duration_ms == 42


async def test_async_stream_result_drain() -> None:
    sr = await AsyncStreamResult(_aevents(("stdout", "x"), ("exit", 0))).drain()
    assert sr.exit_code == 0
