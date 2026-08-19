# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from geneva.apply import memory

if TYPE_CHECKING:
    import pytest


def test_release_unused_process_memory_calls_cleanup_hooks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    class _Pool:
        def release_unused(self) -> None:
            calls.append("arrow")

    class _LibC:
        def malloc_trim(self, value: int) -> None:
            calls.append(f"malloc_trim:{value}")

    monkeypatch.setattr(memory.gc, "collect", lambda gen: calls.append(f"gc:{gen}"))
    monkeypatch.setattr(memory.pa, "default_memory_pool", lambda: _Pool())
    monkeypatch.setattr(memory.sys, "platform", "linux")
    monkeypatch.setattr(memory.ctypes, "CDLL", lambda _name: _LibC())

    memory.release_unused_process_memory()

    # Young generations only: a full collect costs far more than it recovers.
    assert calls == ["gc:1", "arrow", "malloc_trim:0"]


def test_release_unused_process_memory_skips_malloc_trim_off_linux(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    class _Pool:
        def release_unused(self) -> None:
            calls.append("arrow")

    def _unexpected_cdll(_name: str) -> Any:
        raise AssertionError("malloc_trim should not be loaded off Linux")

    monkeypatch.setattr(memory.gc, "collect", lambda gen: calls.append(f"gc:{gen}"))
    monkeypatch.setattr(memory.pa, "default_memory_pool", lambda: _Pool())
    monkeypatch.setattr(memory.sys, "platform", "darwin")
    monkeypatch.setattr(memory.ctypes, "CDLL", _unexpected_cdll)

    memory.release_unused_process_memory()

    assert calls == ["gc:1", "arrow"]


def test_release_unused_process_memory_swallows_cleanup_failures(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _Pool:
        def release_unused(self) -> None:
            raise RuntimeError("arrow failed")

    class _LibC:
        def malloc_trim(self, value: int) -> None:
            raise RuntimeError(f"malloc_trim failed: {value}")

    def _fail_gc(gen: int) -> None:
        raise RuntimeError(f"gc failed: {gen}")

    monkeypatch.setattr(memory.gc, "collect", _fail_gc)
    monkeypatch.setattr(memory.pa, "default_memory_pool", lambda: _Pool())
    monkeypatch.setattr(memory.sys, "platform", "linux")
    monkeypatch.setattr(memory.ctypes, "CDLL", lambda _name: _LibC())

    memory.release_unused_process_memory()


def test_get_applier_memory_trim_interval_env_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(memory.APPLIER_MEMORY_TRIM_INTERVAL_ENV, "0")
    assert memory.get_applier_memory_trim_interval() == 0

    monkeypatch.setenv(memory.APPLIER_MEMORY_TRIM_INTERVAL_ENV, "12")
    assert memory.get_applier_memory_trim_interval() == 12

    monkeypatch.setenv(memory.APPLIER_MEMORY_TRIM_INTERVAL_ENV, "-3")
    assert memory.get_applier_memory_trim_interval() == 0

    monkeypatch.setenv(memory.APPLIER_MEMORY_TRIM_INTERVAL_ENV, "not-an-int")
    assert (
        memory.get_applier_memory_trim_interval()
        == memory.DEFAULT_APPLIER_MEMORY_TRIM_INTERVAL
    )
