"""Marketplace runner の contract テスト（molt #1409）。

固定する契約:
    1. 同一 agent 関数が local サンプルと Marketplace runner の双方で動く
       （agent 側は ID parsing / DB write / webhook / cleanup を実装しない）
    2. identity env 欠落時は agent を呼ばずに設定エラーへ収束する
    3. success / agent 例外 / 入力取得失敗 / 保存失敗 / webhook 失敗 のどの分岐でも
       terminal イベントは正確に 1 回、cleanup は 1 回
    4. identity env の必須集合は executer-marketplace が実際に注入する集合の部分集合
       （契約の正本: executer-marketplace src/k8s_manager/pod_manager.py
       _build_dynamic_env — 変更したらこのテストも更新すること）
    5. 出力（イベント本文 / stdout）に traceback を漏らさない

実行: python -m pytest tests/runner/ -v
"""

from __future__ import annotations

from typing import Any

import pytest

from agenticstar_platform.events import EventType
from agenticstar_platform.events.handlers import (
    CompositeEventHandler,
    DatabaseEventHandler,
)
from agenticstar_platform.runner import (
    OPTIONAL_IDENTITY_ENV,
    REQUIRED_IDENTITY_ENV,
    MarketplaceRunnerConfigError,
    arun_marketplace_agent,
)

# ---------------------------------------------------------------------------
# fixtures / fakes（synthetic Marketplace adapter）
# ---------------------------------------------------------------------------

BASE_ENV = {
    "EXECUTION_ID": "exec-0001",
    "CONVERSATION_ID": "conv-0001",
    "USER_ID": "user-0001",
    "MESSAGE_ID": "msg-0001",
    "WEBHOOK_URL": "http://synthetic.invalid/webhook",
}

DEFAULT_MESSAGES = [
    {"role": "user", "content": "hello agenticstar"},
]


class FakeDataAccess:
    """DataAccess の synthetic 実装（execute_query = 入力取得, insert = 保存）。"""

    def __init__(
        self,
        messages: list | None = None,
        query_success: bool = True,
        insert_raises: bool = False,
    ):
        self._messages = DEFAULT_MESSAGES if messages is None else messages
        self._query_success = query_success
        self._insert_raises = insert_raises
        self.inserted: list[dict[str, Any]] = []

    async def execute_query(self, query: str, params: tuple) -> dict[str, Any]:
        if not self._query_success:
            return {"success": False, "data": []}
        return {"success": True, "data": [{"messages": self._messages}]}

    async def insert(self, table: str, data: dict[str, Any]) -> dict[str, Any]:
        if self._insert_raises:
            raise RuntimeError("synthetic DB persistence failure")
        self.inserted.append({"table": table, **data})
        return {"success": True}


class RecordingHandler:
    """イベントを記録するだけの synthetic webhook 相当ハンドラ。"""

    def __init__(self, raises: bool = False):
        self.events: list[Any] = []
        self._raises = raises

    async def __call__(self, event) -> str | None:
        self.events.append(event)
        if self._raises:
            raise RuntimeError("synthetic webhook failure")
        return None

    def terminal_events(self) -> list[Any]:
        return [
            e
            for e in self.events
            if e.event_type
            in (EventType.COMPLETION_SUCCESS, EventType.COMPLETION_FAILURE)
        ]


def make_agent(result: str = "RESULT"):
    """呼び出し回数を記録する最小 agent（ID/DB/webhook/cleanup を一切書かない）。"""
    calls: list[str] = []

    async def agent(emitter, message: str) -> str:
        calls.append(message)
        return result

    agent.calls = calls  # type: ignore[attr-defined]
    return agent


async def _run(agent, *, env=None, data_access=None, handler=None, **kwargs):
    return await arun_marketplace_agent(
        agent,
        env=BASE_ENV if env is None else env,
        data_access=FakeDataAccess() if data_access is None else data_access,
        event_handler=handler,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# 4. env 契約の pin（executor 実装との drift 検出用アンカー）
# ---------------------------------------------------------------------------

# executer-marketplace src/k8s_manager/pod_manager.py _build_dynamic_env が
# SandboxClaim spec.env として agent コンテナに注入する env（2026-08-01 時点）。
# executor 側でこのリストを変えたら、ここと runner の契約を同時に見直すこと。
EXECUTOR_INJECTED_REQUIRED = {
    "EXECUTION_ID",
    "CONVERSATION_ID",
    "USER_ID",
    "REQUEST_SOURCE",
    "AGENT_ID",
}
EXECUTOR_INJECTED_OPTIONAL = {
    "MESSAGE_ID",
    "USER_ORGANIZATION_ID",
    "USER_ORGANIZATION_LABEL",
    "USER_JOB_ROLE",
    "USER_JOB_LABEL",
    "USER_BIO",
    "USER_LANGUAGE",
}


def test_identity_env_contract_is_subset_of_executor_injection() -> None:
    """runner が要求する env は executor が実際に注入する集合に含まれること。"""
    injected = EXECUTOR_INJECTED_REQUIRED | EXECUTOR_INJECTED_OPTIONAL
    assert set(REQUIRED_IDENTITY_ENV) <= injected
    assert set(OPTIONAL_IDENTITY_ENV) <= injected


# ---------------------------------------------------------------------------
# 1. success 分岐
# ---------------------------------------------------------------------------

async def test_success_terminal_once_and_result_returned() -> None:
    agent = make_agent("ANSWER")
    webhook = RecordingHandler()
    result = await _run(agent, handler=webhook)

    assert result == "ANSWER"
    assert agent.calls == ["hello agenticstar"], "agent は入力 1 回で呼ばれる"
    terminals = webhook.terminal_events()
    assert len(terminals) == 1, "terminal は正確に 1 回"
    assert terminals[0].event_type == EventType.COMPLETION_SUCCESS
    assert terminals[0].message == "ANSWER"


async def test_success_persists_terminal_via_database_handler() -> None:
    """実 DatabaseEventHandler 経由で terminal が execution_messages へ保存されること。"""
    da = FakeDataAccess()
    db_handler = DatabaseEventHandler(
        data_access=da,
        user_id=BASE_ENV["USER_ID"],
        conversation_id=BASE_ENV["CONVERSATION_ID"],
        message_id=BASE_ENV["MESSAGE_ID"],
    )
    webhook = RecordingHandler()
    await _run(
        make_agent("SAVED"),
        data_access=da,
        handler=CompositeEventHandler([db_handler, webhook]),
    )

    completion_rows = [
        row for row in da.inserted if "SAVED" in str(row)
    ]
    assert len(completion_rows) == 1, "terminal は DB に 1 行だけ保存される"
    assert completion_rows[0]["table"] == "execution_messages"
    assert len(webhook.terminal_events()) == 1


# ---------------------------------------------------------------------------
# 2. identity / infra 欠落分岐（agent 未呼出で収束）
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("missing", list(REQUIRED_IDENTITY_ENV))
async def test_missing_identity_env_rejects_before_agent(missing: str) -> None:
    agent = make_agent()
    webhook = RecordingHandler()
    env = {k: v for k, v in BASE_ENV.items() if k != missing}

    with pytest.raises(MarketplaceRunnerConfigError) as exc_info:
        await _run(agent, env=env, handler=webhook)

    assert missing in str(exc_info.value), "どの env が欠けたか actionable に示す"
    assert agent.calls == [], "agent 関数は呼ばれない"
    assert webhook.events == [], "イベントは一切送信されない"


async def test_missing_webhook_url_rejects_before_agent() -> None:
    agent = make_agent()
    env = {k: v for k, v in BASE_ENV.items() if k != "WEBHOOK_URL"}

    with pytest.raises(MarketplaceRunnerConfigError) as exc_info:
        # event_handler を渡さない = 実 create_marketplace_handler 経路
        await arun_marketplace_agent(agent, env=env, data_access=FakeDataAccess())

    assert "WEBHOOK_URL" in str(exc_info.value)
    assert agent.calls == []


# ---------------------------------------------------------------------------
# 3. 入力取得失敗分岐（agent 未呼出 + terminal failure 1 回）
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "data_access",
    [
        FakeDataAccess(query_success=False),
        FakeDataAccess(messages=[]),
        FakeDataAccess(messages=[{"role": "assistant", "content": "no user turn"}]),
    ],
    ids=["query-fails", "no-messages", "no-user-message"],
)
async def test_input_fetch_failure_terminal_failure_without_agent(data_access) -> None:
    agent = make_agent()
    webhook = RecordingHandler()
    result = await _run(agent, data_access=data_access, handler=webhook)

    assert result is None
    assert agent.calls == [], "入力が取れない実行では agent を呼ばない"
    terminals = webhook.terminal_events()
    assert len(terminals) == 1
    assert terminals[0].event_type == EventType.COMPLETION_FAILURE
    assert "input fetch failed" in terminals[0].message


# ---------------------------------------------------------------------------
# 4. agent 例外分岐（terminal failure 1 回・traceback 非露出）
# ---------------------------------------------------------------------------

async def test_agent_exception_terminal_failure_once_without_traceback(capsys) -> None:
    async def failing_agent(emitter, message: str) -> str:
        raise ValueError("boom")

    webhook = RecordingHandler()
    result = await _run(failing_agent, handler=webhook)

    assert result is None
    terminals = webhook.terminal_events()
    assert len(terminals) == 1
    assert terminals[0].event_type == EventType.COMPLETION_FAILURE
    assert "ValueError" in terminals[0].message
    assert "boom" in terminals[0].message
    assert "Traceback" not in terminals[0].message, "traceback は logger のみ"
    captured = capsys.readouterr()
    assert "Traceback" not in captured.out, "stdout に traceback を出さない"


# ---------------------------------------------------------------------------
# 5. 保存失敗 / webhook 失敗分岐（他ハンドラは継続・terminal 1 回・例外非伝播）
# ---------------------------------------------------------------------------

async def test_persistence_failure_webhook_still_notified() -> None:
    da = FakeDataAccess(insert_raises=True)
    db_handler = DatabaseEventHandler(
        data_access=da,
        user_id=BASE_ENV["USER_ID"],
        conversation_id=BASE_ENV["CONVERSATION_ID"],
        message_id=BASE_ENV["MESSAGE_ID"],
    )
    webhook = RecordingHandler()
    result = await _run(
        make_agent("OK"),
        data_access=da,
        handler=CompositeEventHandler([db_handler, webhook]),
    )

    assert result == "OK", "DB 保存失敗でも実行は完了する"
    terminals = webhook.terminal_events()
    assert len(terminals) == 1, "webhook へは terminal が 1 回届く"
    assert terminals[0].event_type == EventType.COMPLETION_SUCCESS
    assert da.inserted == [], "DB 側は失敗している（握り潰されて継続）"


async def test_webhook_failure_db_still_persisted() -> None:
    da = FakeDataAccess()
    db_handler = DatabaseEventHandler(
        data_access=da,
        user_id=BASE_ENV["USER_ID"],
        conversation_id=BASE_ENV["CONVERSATION_ID"],
        message_id=BASE_ENV["MESSAGE_ID"],
    )
    failing_webhook = RecordingHandler(raises=True)
    result = await _run(
        make_agent("OK"),
        data_access=da,
        handler=CompositeEventHandler([db_handler, failing_webhook]),
    )

    assert result == "OK", "webhook 失敗でも実行は完了する"
    assert len(failing_webhook.terminal_events()) == 1, "webhook 試行は 1 回"
    completion_rows = [row for row in da.inserted if "OK" in str(row)]
    assert len(completion_rows) == 1, "DB へは terminal が 1 行保存される"


# ---------------------------------------------------------------------------
# 6. local サンプル互換（agent が自前で terminal を emit しても二重にならない）
# ---------------------------------------------------------------------------

async def test_agent_emitting_own_terminal_is_not_duplicated() -> None:
    """README local サンプル形式（terminal を自前 emit）の関数がそのまま動くこと。"""

    async def local_style_agent(emitter, message: str) -> None:
        await emitter.emit_event(EventType.PHASE_START, f"received: {message}")
        await emitter.emit_event(EventType.COMPLETION_SUCCESS, message.upper())

    webhook = RecordingHandler()
    await _run(local_style_agent, handler=webhook)

    terminals = webhook.terminal_events()
    assert len(terminals) == 1, "runner は二重 terminal を送らない"
    assert terminals[0].message == "HELLO AGENTICSTAR"
    types = [e.event_type for e in webhook.events]
    assert types == [EventType.PHASE_START, EventType.COMPLETION_SUCCESS]


async def test_agent_double_terminal_is_suppressed() -> None:
    """agent が誤って terminal を 2 回 emit しても配信は 1 回に抑える。"""

    async def double_terminal_agent(emitter, message: str) -> None:
        await emitter.emit_event(EventType.COMPLETION_SUCCESS, "first")
        await emitter.emit_event(EventType.COMPLETION_SUCCESS, "second")

    webhook = RecordingHandler()
    await _run(double_terminal_agent, handler=webhook)

    terminals = webhook.terminal_events()
    assert len(terminals) == 1
    assert terminals[0].message == "first"


# ---------------------------------------------------------------------------
# 7. イベント順序（進捗 → terminal）と terminal 後の後続なし
# ---------------------------------------------------------------------------

async def test_progress_events_precede_single_terminal() -> None:
    async def progressive_agent(emitter, message: str) -> str:
        await emitter.emit_event(EventType.PHASE_START, "start")
        await emitter.emit_event(EventType.PROGRESS_UPDATE, "working")
        return "done"

    webhook = RecordingHandler()
    await _run(progressive_agent, handler=webhook)

    types = [e.event_type for e in webhook.events]
    assert types == [
        EventType.PHASE_START,
        EventType.PROGRESS_UPDATE,
        EventType.COMPLETION_SUCCESS,
    ], "進捗イベントの後に terminal が 1 回だけ来る（terminal 後の後続なし）"


async def test_events_after_terminal_are_suppressed() -> None:
    """terminal 送信後の進捗イベントは配信されない（terminal が真に最終）。"""

    async def chatty_after_terminal(emitter, message: str) -> None:
        await emitter.emit_event(EventType.COMPLETION_SUCCESS, "done")
        await emitter.emit_event(EventType.PROGRESS_UPDATE, "late progress")

    webhook = RecordingHandler()
    await _run(chatty_after_terminal, handler=webhook)

    types = [e.event_type for e in webhook.events]
    assert types == [EventType.COMPLETION_SUCCESS], (
        "terminal の後に積まれたイベントは破棄される"
    )


async def test_agent_raising_after_own_terminal_keeps_success() -> None:
    """agent が terminal 送信後に例外を投げても、配信済みの success は変わらない。"""

    async def terminal_then_raise(emitter, message: str) -> None:
        await emitter.emit_event(EventType.COMPLETION_SUCCESS, "committed")
        raise RuntimeError("post-terminal crash")

    webhook = RecordingHandler()
    result = await _run(terminal_then_raise, handler=webhook)

    assert result is None
    terminals = webhook.terminal_events()
    assert len(terminals) == 1
    assert terminals[0].event_type == EventType.COMPLETION_SUCCESS
    assert terminals[0].message == "committed"


async def test_cancellation_mid_agent_delivers_failure_and_propagates() -> None:
    """実行中の cancel（Pod 停止等）でも terminal failure を 1 回配信して伝播する。"""
    import asyncio

    started = asyncio.Event()

    async def hanging_agent(emitter, message: str) -> str:
        started.set()
        await asyncio.sleep(60)
        return "never"

    webhook = RecordingHandler()
    task = asyncio.create_task(_run(hanging_agent, handler=webhook))
    await started.wait()
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    terminals = webhook.terminal_events()
    assert len(terminals) == 1, "cancel 時も terminal failure が 1 回配信される"
    assert terminals[0].event_type == EventType.COMPLETION_FAILURE


async def test_cancellation_during_delivery_completes_terminal() -> None:
    """配信（drain）中に cancel されても、処理中の terminal は届けきってから伝播する。"""
    import asyncio

    class SlowTerminalHandler(RecordingHandler):
        def __init__(self):
            super().__init__()
            self.terminal_started = asyncio.Event()
            self.terminal_finished = False

        async def __call__(self, event):
            if event.event_type in (
                EventType.COMPLETION_SUCCESS,
                EventType.COMPLETION_FAILURE,
            ):
                self.terminal_started.set()
                await asyncio.sleep(0.3)
                self.terminal_finished = True
            return await super().__call__(event)

    handler = SlowTerminalHandler()
    task = asyncio.create_task(_run(make_agent("SLOW"), handler=handler))
    await handler.terminal_started.wait()
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    assert handler.terminal_finished, "処理中だった terminal 配信は完了している"
    assert len(handler.terminal_events()) == 1
