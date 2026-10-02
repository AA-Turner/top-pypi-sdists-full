"""db_config / from_env フォールバック経路の回帰テスト（0.5.29 AttributeError）。

0.5.29 では ``data_access`` 省略時に生の ``PostgreSQLConfig`` を ``DataAccess``
へ渡していたため、フォールバック経路が ``'PostgreSQLConfig' object has no
attribute 'initialize'`` で必ず落ちた（CoE 報告 2026-08-07）。contract テストは
全ケースで ``data_access=`` を注入していたため本経路のカバレッジがゼロだった。

固定する契約:
    1. ``db_config`` 指定（api_url なし）→ ``create_postgresql_manager`` で
       マネージャ化され、initialize → 実行 → close が DataAccess 経由で回る
    2. api_url 設定時は agent を呼ばずに ``MarketplaceRunnerConfigError``
       （runner は token_provider を供給できない）
    3. 明示 ``data_access=`` 指定時は factory を呼ばず接続の開閉も行わない

実行: python -m pytest tests/runner/ -v
"""

from __future__ import annotations

from typing import Any

import pytest

import agenticstar_platform.runner as runner_module
from agenticstar_platform.db import PostgreSQLConfig
from agenticstar_platform.events import EventType
from agenticstar_platform.runner import (
    MarketplaceRunnerConfigError,
    arun_marketplace_agent,
)

from .test_marketplace_runner_contract import (
    BASE_ENV,
    DEFAULT_MESSAGES,
    FakeDataAccess,
    RecordingHandler,
    make_agent,
)


class FakePostgreSQLManager:
    """PostgreSQLManager の synthetic 実装（DataAccess が要求する契約のみ）。

    契約の正本: DataAccess.__init__ docstring — initialize() / close() /
    execute_query() / fetch_one() / fetch_all() を実装していること。
    """

    def __init__(self, messages: list | None = None):
        self._messages = DEFAULT_MESSAGES if messages is None else messages
        self.initialized = False
        self.closed = False
        self.queries: list[tuple[str, tuple]] = []

    async def initialize(self) -> None:
        self.initialized = True

    async def close(self) -> None:
        self.closed = True

    async def execute_query(self, query: str, params: tuple = ()) -> dict[str, Any]:
        self.queries.append((query, params))
        return {"success": True, "data": [{"messages": self._messages}]}

    async def fetch_one(self, query: str, params: tuple = ()) -> dict[str, Any] | None:
        result = await self.execute_query(query, params)
        return result["data"][0] if result["data"] else None

    async def fetch_all(self, query: str, params: tuple = ()) -> list[dict[str, Any]]:
        result = await self.execute_query(query, params)
        return result["data"]


def _direct_db_config() -> PostgreSQLConfig:
    return PostgreSQLConfig(
        host="synthetic.invalid",
        database="synthetic_db",
        username="synthetic",
        password="synthetic",
    )


async def test_db_config_fallback_builds_manager_and_runs_lifecycle(monkeypatch):
    """回帰: db_config 指定で AttributeError なく initialize→実行→close が回る。"""
    manager = FakePostgreSQLManager()
    factory_calls: list[PostgreSQLConfig] = []

    def fake_factory(config, **kwargs):
        factory_calls.append(config)
        return manager

    monkeypatch.setattr(runner_module, "create_postgresql_manager", fake_factory)

    agent = make_agent()
    handler = RecordingHandler()
    config = _direct_db_config()

    result = await arun_marketplace_agent(
        agent,
        env=BASE_ENV,
        db_config=config,
        event_handler=handler,
    )

    assert result == "RESULT"
    assert agent.calls == [DEFAULT_MESSAGES[0]["content"]]
    # config はマネージャ化されてから DataAccess へ渡る（0.5.29 は生 config を渡していた）
    assert factory_calls == [config]
    assert manager.initialized is True
    assert manager.closed is True
    # 入力取得（execution_data SELECT）が実 DataAccess → マネージャ経由で走っている
    assert any("execution_data" in q for q, _ in manager.queries)
    assert len(handler.terminal_events()) == 1


async def test_from_env_fallback_builds_manager(monkeypatch):
    """db_config 省略時も from_env() → マネージャ化の同一経路を通る。"""
    manager = FakePostgreSQLManager()
    monkeypatch.setattr(
        runner_module, "create_postgresql_manager", lambda config, **kw: manager
    )
    # from_env()（既定 prefix "DB_"）が api_url を拾わないよう明示的に外す
    monkeypatch.delenv("DB_API_PROXY_URL", raising=False)

    agent = make_agent()
    handler = RecordingHandler()

    result = await arun_marketplace_agent(
        agent,
        env=BASE_ENV,
        event_handler=handler,
    )

    assert result == "RESULT"
    assert manager.initialized is True
    assert manager.closed is True


async def test_agent_exception_still_closes_owned_manager(monkeypatch):
    """agent 例外時も runner 所有のマネージャは close される（terminal は failure）。"""
    manager = FakePostgreSQLManager()
    monkeypatch.setattr(
        runner_module, "create_postgresql_manager", lambda config, **kw: manager
    )

    async def failing_agent(emitter, message: str) -> str:
        raise RuntimeError("synthetic agent failure")

    handler = RecordingHandler()

    result = await arun_marketplace_agent(
        failing_agent,
        env=BASE_ENV,
        db_config=_direct_db_config(),
        event_handler=handler,
    )

    assert result is None
    assert manager.initialized is True
    assert manager.closed is True
    terminals = handler.terminal_events()
    assert len(terminals) == 1
    assert terminals[0].event_type is EventType.COMPLETION_FAILURE


async def test_from_env_api_url_is_rejected(monkeypatch):
    """from_env() 経由でも DB_API_PROXY_URL 設定は agent 未呼出で拒否される。"""
    monkeypatch.setenv("DB_API_PROXY_URL", "http://cli-api.synthetic.invalid")

    agent = make_agent()
    handler = RecordingHandler()

    with pytest.raises(MarketplaceRunnerConfigError, match="DB_API_PROXY_URL"):
        await arun_marketplace_agent(
            agent,
            env=BASE_ENV,
            event_handler=handler,
        )

    assert agent.calls == []
    assert handler.events == []


async def test_api_url_config_is_rejected_before_agent_runs():
    """api_url 設定は agent 未呼出のまま MarketplaceRunnerConfigError。"""
    agent = make_agent()
    handler = RecordingHandler()
    config = _direct_db_config()
    config.api_url = "http://cli-api.synthetic.invalid"

    with pytest.raises(MarketplaceRunnerConfigError, match="api_url"):
        await arun_marketplace_agent(
            agent,
            env=BASE_ENV,
            db_config=config,
            event_handler=handler,
        )

    assert agent.calls == []
    assert handler.events == []


async def test_explicit_data_access_skips_factory(monkeypatch):
    """data_access 明示時は factory を呼ばない（接続の開閉は caller 責務）。"""

    def exploding_factory(config, **kwargs):  # pragma: no cover - 呼ばれたら契約違反
        raise AssertionError("create_postgresql_manager must not be called")

    monkeypatch.setattr(
        runner_module, "create_postgresql_manager", exploding_factory
    )

    agent = make_agent()
    handler = RecordingHandler()

    result = await arun_marketplace_agent(
        agent,
        env=BASE_ENV,
        data_access=FakeDataAccess(),
        event_handler=handler,
    )

    assert result == "RESULT"
    assert len(handler.terminal_events()) == 1
