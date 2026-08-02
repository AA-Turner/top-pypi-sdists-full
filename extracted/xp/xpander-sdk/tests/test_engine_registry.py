"""Tests for the shared Postgres engine registry."""

from __future__ import annotations

import threading
from unittest.mock import MagicMock, patch

import pytest

from xpander_sdk.utils.db import engine_registry
from xpander_sdk.utils.db.engine_registry import get_or_create_engine

SYNC_URL = "postgresql+psycopg://u:p@host/db"
ASYNC_URL = "postgresql+psycopg_async://u:p@host/db"


@pytest.fixture(autouse=True)
def _clear_registry():
    engine_registry._engines.clear()
    yield
    engine_registry._engines.clear()


def _fake_engine_factories():
    """Patch create_engine/create_async_engine to return unique sentinels."""
    sync_mock = MagicMock(side_effect=lambda *a, **k: MagicMock(name="sync-engine"))
    async_mock = MagicMock(side_effect=lambda *a, **k: MagicMock(name="async-engine"))
    return sync_mock, async_mock


def test_same_url_and_mode_returns_same_engine():
    sync_mock, async_mock = _fake_engine_factories()
    with patch.object(engine_registry, "create_engine", sync_mock), patch.object(
        engine_registry, "create_async_engine", async_mock
    ):
        first = get_or_create_engine(SYNC_URL, async_engine=False)
        second = get_or_create_engine(SYNC_URL, async_engine=False)

    assert first is second
    assert sync_mock.call_count == 1


def test_rotated_url_builds_new_engine():
    sync_mock, async_mock = _fake_engine_factories()
    rotated = "postgresql+psycopg://u:p@host/db2"
    with patch.object(engine_registry, "create_engine", sync_mock), patch.object(
        engine_registry, "create_async_engine", async_mock
    ):
        first = get_or_create_engine(SYNC_URL, async_engine=False)
        second = get_or_create_engine(rotated, async_engine=False)

    assert first is not second
    assert sync_mock.call_count == 2


def test_mode_is_part_of_key():
    sync_mock, async_mock = _fake_engine_factories()
    with patch.object(engine_registry, "create_engine", sync_mock), patch.object(
        engine_registry, "create_async_engine", async_mock
    ):
        sync_engine = get_or_create_engine(SYNC_URL, async_engine=False)
        async_engine = get_or_create_engine(ASYNC_URL, async_engine=True)

    assert sync_engine is not async_engine
    assert sync_mock.call_count == 1
    assert async_mock.call_count == 1


def test_pool_kwargs_on_sync_engine():
    sync_mock, async_mock = _fake_engine_factories()
    with patch.object(engine_registry, "create_engine", sync_mock), patch.object(
        engine_registry, "create_async_engine", async_mock
    ):
        get_or_create_engine(SYNC_URL, async_engine=False)

    _, kwargs = sync_mock.call_args
    assert kwargs["pool_pre_ping"] is True
    assert kwargs["pool_recycle"] == engine_registry.POOL_RECYCLE
    assert kwargs["pool_size"] == engine_registry.POOL_SIZE
    assert kwargs["max_overflow"] == engine_registry.MAX_OVERFLOW
    assert kwargs["pool_timeout"] == engine_registry.POOL_TIMEOUT


def test_pool_kwargs_on_async_engine():
    sync_mock, async_mock = _fake_engine_factories()
    with patch.object(engine_registry, "create_engine", sync_mock), patch.object(
        engine_registry, "create_async_engine", async_mock
    ):
        get_or_create_engine(ASYNC_URL, async_engine=True)

    args, kwargs = async_mock.call_args
    assert args[0] == ASYNC_URL
    assert kwargs["pool_pre_ping"] is True
    assert kwargs["pool_recycle"] == engine_registry.POOL_RECYCLE
    assert kwargs["pool_size"] == engine_registry.POOL_SIZE
    assert kwargs["max_overflow"] == engine_registry.MAX_OVERFLOW
    assert kwargs["pool_timeout"] == engine_registry.POOL_TIMEOUT


def test_url_is_normalized():
    sync_mock, async_mock = _fake_engine_factories()
    with patch.object(engine_registry, "create_engine", sync_mock), patch.object(
        engine_registry, "create_async_engine", async_mock
    ):
        a = get_or_create_engine(SYNC_URL, async_engine=False)
        b = get_or_create_engine(f"  {SYNC_URL}  ", async_engine=False)

    assert a is b
    assert sync_mock.call_count == 1


def test_concurrent_get_or_create_builds_once():
    sync_mock, async_mock = _fake_engine_factories()
    results = []
    barrier = threading.Barrier(8)

    def worker():
        barrier.wait()
        results.append(get_or_create_engine(SYNC_URL, async_engine=False))

    with patch.object(engine_registry, "create_engine", sync_mock), patch.object(
        engine_registry, "create_async_engine", async_mock
    ):
        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    assert sync_mock.call_count == 1
    assert all(r is results[0] for r in results)


def test_dispose_all_disposes_and_clears():
    sync_mock, async_mock = _fake_engine_factories()
    with patch.object(engine_registry, "create_engine", sync_mock), patch.object(
        engine_registry, "create_async_engine", async_mock
    ):
        engine = get_or_create_engine(SYNC_URL, async_engine=False)
        engine_registry.dispose_all()

    engine.dispose.assert_called_once()
    assert engine_registry._engines == {}
