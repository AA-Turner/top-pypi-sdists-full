"""aget_db hands agno a shared pooled engine (db_engine), not a raw db_url."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from xpander_sdk.models.frameworks import Framework
from xpander_sdk.modules.agents.sub_modules.agent import Agent

RAW_URI = "postgresql://u:p@host/db"


def _fake_self():
    """Minimal object exposing only what aget_db reads off self."""
    conn = SimpleNamespace(connection_uri=SimpleNamespace(uri=RAW_URI))

    async def aget_connection_string():
        return conn

    return SimpleNamespace(
        id="agent-1",
        framework=Framework.Agno,
        agno_settings=SimpleNamespace(session_storage=True),
        aget_connection_string=aget_connection_string,
    )


@pytest.mark.asyncio
async def test_async_db_passes_db_engine_not_db_url():
    fake = _fake_self()
    sentinel_engine = MagicMock(name="async-engine")
    async_db_cls = MagicMock(name="AsyncPostgresDb")
    sync_db_cls = MagicMock(name="PostgresDb")

    with patch(
        "xpander_sdk.utils.db.get_or_create_engine",
        return_value=sentinel_engine,
    ) as get_engine, patch.dict(
        "sys.modules",
        {"agno.db.postgres": SimpleNamespace(
            AsyncPostgresDb=async_db_cls, PostgresDb=sync_db_cls
        )},
    ):
        await Agent.aget_db(fake, async_db=True)

    # Engine built from the async-rewritten URL, in async mode.
    get_engine.assert_called_once()
    args, kwargs = get_engine.call_args
    assert args[0] == "postgresql+psycopg_async://u:p@host/db"
    assert kwargs["async_engine"] is True

    # agno receives db_engine (not db_url) plus the schema.
    async_db_cls.assert_called_once()
    _, db_kwargs = async_db_cls.call_args
    assert db_kwargs["db_engine"] is sentinel_engine
    assert "db_url" not in db_kwargs
    assert db_kwargs["db_schema"] == "ag_agent_1"
    sync_db_cls.assert_not_called()


@pytest.mark.asyncio
async def test_sync_db_passes_db_engine_not_db_url():
    fake = _fake_self()
    sentinel_engine = MagicMock(name="sync-engine")
    async_db_cls = MagicMock(name="AsyncPostgresDb")
    sync_db_cls = MagicMock(name="PostgresDb")

    with patch(
        "xpander_sdk.utils.db.get_or_create_engine",
        return_value=sentinel_engine,
    ) as get_engine, patch.dict(
        "sys.modules",
        {"agno.db.postgres": SimpleNamespace(
            AsyncPostgresDb=async_db_cls, PostgresDb=sync_db_cls
        )},
    ):
        await Agent.aget_db(fake, async_db=False)

    args, kwargs = get_engine.call_args
    assert args[0] == "postgresql+psycopg://u:p@host/db"
    assert kwargs["async_engine"] is False

    sync_db_cls.assert_called_once()
    _, db_kwargs = sync_db_cls.call_args
    assert db_kwargs["db_engine"] is sentinel_engine
    assert "db_url" not in db_kwargs
    async_db_cls.assert_not_called()


@pytest.mark.asyncio
async def test_falls_back_to_db_url_when_engine_creation_fails():
    fake = _fake_self()
    async_db_cls = MagicMock(name="AsyncPostgresDb")
    sync_db_cls = MagicMock(name="PostgresDb")

    with patch(
        "xpander_sdk.utils.db.get_or_create_engine",
        side_effect=RuntimeError("boom"),
    ), patch.dict(
        "sys.modules",
        {"agno.db.postgres": SimpleNamespace(
            AsyncPostgresDb=async_db_cls, PostgresDb=sync_db_cls
        )},
    ):
        await Agent.aget_db(fake, async_db=True)

    async_db_cls.assert_called_once()
    _, db_kwargs = async_db_cls.call_args
    assert "db_engine" not in db_kwargs
    assert db_kwargs["db_url"] == "postgresql+psycopg_async://u:p@host/db"
    assert db_kwargs["db_schema"] == "ag_agent_1"
