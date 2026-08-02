# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# compat-skip-retention: test scaffolding (async helpers/fixtures), not a migration model

"""Unit tests for ``omnibase_compat.concurrency.run_coro_sync``.

Covers the three invariants from OMN-9237 / OMN-9235 Runtime Boot Resilience
plan Task 2:

(a) Called from a sync context (no running event loop), the helper returns the
    coroutine result via the cheap ``asyncio.run`` path.
(b) Called from inside a running event loop, the helper dispatches the
    coroutine to a short-lived worker thread and returns the result WITHOUT
    raising ``RuntimeError: asyncio.run() cannot be called from a running
    event loop``.
(c) Exceptions raised inside the coroutine propagate unchanged to the caller.
"""

from __future__ import annotations

import asyncio

import pytest

from omnibase_compat.concurrency import run_coro_sync


@pytest.mark.unit
def test_run_coro_sync_returns_result_from_sync_context() -> None:
    """No running loop -> cheap path via ``asyncio.run``; result returned."""

    async def produce() -> int:
        return 42

    assert run_coro_sync(produce()) == 42


@pytest.mark.unit
def test_run_coro_sync_returns_result_from_inside_running_loop() -> None:
    """Running loop detected -> worker-thread dispatch; no RuntimeError."""

    async def outer() -> str:
        # We are now inside a running event loop. Calling run_coro_sync with
        # another coroutine MUST NOT raise "asyncio.run() cannot be called
        # from a running event loop" — this is the whole point of the helper.
        async def inner() -> str:
            return "hello-from-inner"

        return run_coro_sync(inner())

    result = asyncio.run(outer())
    assert result == "hello-from-inner"


@pytest.mark.unit
def test_run_coro_sync_propagates_exception_from_sync_context() -> None:
    """Coroutine-raised exception must surface unchanged to sync caller."""

    class BoomError(RuntimeError):
        pass

    async def explode() -> None:
        raise BoomError("kaboom")

    with pytest.raises(BoomError, match="kaboom"):
        run_coro_sync(explode())


@pytest.mark.unit
def test_run_coro_sync_propagates_exception_from_running_loop() -> None:
    """Coroutine-raised exception must surface unchanged when worker-thread path is used."""

    class BoomError(RuntimeError):
        pass

    async def explode() -> None:
        raise BoomError("kaboom-inside-loop")

    async def outer() -> None:
        run_coro_sync(explode())

    with pytest.raises(BoomError, match="kaboom-inside-loop"):
        asyncio.run(outer())


@pytest.mark.unit
def test_run_coro_sync_preserves_coroutine_return_type() -> None:
    """Generic T is preserved — complex return values round-trip intact."""

    async def produce() -> dict[str, list[int]]:
        return {"answers": [1, 2, 3]}

    result = run_coro_sync(produce())
    assert result == {"answers": [1, 2, 3]}
