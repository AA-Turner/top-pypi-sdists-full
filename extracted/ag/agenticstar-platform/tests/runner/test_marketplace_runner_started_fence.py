"""会話 runner の開始済みの印（started fence、``db/started_fence.py``）の契約テスト。

固定する契約（fence を取るのはサイクル型の実行 = execution_data.runtime_protocol が mp-chat/1 だけ）:
    0. 通常の会話と確かめられた実行は従来どおり（印を見ない・書かない・接続プールも要らない）。
       実行行の種類を読めない時はサイクル型として扱う
    1. 印が無ければ 1 行書いてから agent を呼ぶ（印は progress_message の形）
    2. 同じ (CONVERSATION_ID, MESSAGE_ID) の行が既にあれば agent を呼ばず、イベントも送らずに
       MarketplaceRunnerFenceTaken（Pod の作り直しで同じ実行が二重に走らない）
    3. 同時に起動した 2 つの runner は advisory lock で直列になり、agent は 1 回だけ
    4. DB の失敗（ロック・存在確認・書き込み・commit）は agent を呼ばず、イベントも送らずに raise（fail closed）
    5. サイクル型で接続プールの無い data_access のまま既定（started_fence=True）なら設定エラー

synthetic な pool（asyncpg の acquire / transaction / execute / fetchval の契約だけ）で判定を固定し、
実 PostgreSQL の挙動（ロック待ちの後に勝者の commit が見えること）は
環境変数 AGENTICSTAR_SDK_TEST_PG_DSN がある時だけ ``TestRealPostgres`` で確かめる。

実行: python -m pytest tests/runner/test_marketplace_runner_started_fence.py -v
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
import uuid
from typing import Any

import pytest

from agenticstar_platform.db.started_fence import (
    MARKER_KIND,
    StartedFenceTaken,
    fence_lock_key,
    take_started_fence,
)
from agenticstar_platform.runner import (
    MarketplaceRunnerConfigError,
    MarketplaceRunnerFenceTaken,
    arun_marketplace_agent,
    run_marketplace_agent,
)

from .test_marketplace_runner_contract import (
    BASE_ENV,
    FakeDataAccess,
    RecordingHandler,
    make_agent,
)

# ---------------------------------------------------------------------------
# synthetic pool（asyncpg の契約のうち fence が使うものだけ）
# ---------------------------------------------------------------------------


class _Store:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []
        self.locks: dict[int, asyncio.Lock] = {}
        self.fail_on: str | None = None  # "lock" | "select" | "insert" | "commit"
        self.isolations: list[str | None] = []


class _Tx:
    def __init__(self, conn: _Conn, isolation: str | None) -> None:
        self._conn = conn
        conn.store.isolations.append(isolation)

    async def __aenter__(self):
        self._conn.pending = []
        self._conn.held = []
        return self

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if exc_type is None:
                if self._conn.store.fail_on == "commit":
                    raise RuntimeError("synthetic commit failure")
                self._conn.store.rows.extend(self._conn.pending)  # commit
        finally:
            self._conn.pending = []
            for lock in self._conn.held:  # xact lock は commit / rollback で解放
                lock.release()
            self._conn.held = []
        return False


class _Conn:
    def __init__(self, store: _Store) -> None:
        self.store = store
        self.pending: list[dict[str, Any]] = []
        self.held: list[asyncio.Lock] = []
        self.statements: list[str] = []

    def transaction(self, isolation: str | None = None) -> _Tx:
        return _Tx(self, isolation)

    async def execute(self, sql: str, *args: Any) -> str:
        self.statements.append(sql)
        if "pg_advisory_xact_lock" in sql:
            if self.store.fail_on == "lock":
                raise TimeoutError("synthetic lock timeout")
            lock = self.store.locks.setdefault(args[0], asyncio.Lock())
            await lock.acquire()
            self.held.append(lock)
            await asyncio.sleep(0)  # 待っている側に順番を回す
        elif sql.startswith("INSERT INTO execution_messages"):
            if self.store.fail_on == "insert":
                raise RuntimeError("synthetic insert failure")
            user_id, conversation_id, message_id, content = args
            self.pending.append({
                "user_id": user_id, "conversation_id": conversation_id, "message_id": message_id,
                "chunk_type": "progress_message", "content_data": json.loads(content),
            })
        return "OK"

    async def fetchval(self, sql: str, *args: Any) -> Any:
        self.statements.append(sql)
        if self.store.fail_on == "select":
            raise RuntimeError("synthetic select failure")
        conversation_id, message_id = args
        return any(r["conversation_id"] == conversation_id and r["message_id"] == message_id
                   for r in self.store.rows)


class _Pool:
    def __init__(self, store: _Store) -> None:
        self.store = store
        self.conns: list[_Conn] = []

    @contextlib.asynccontextmanager
    async def acquire(self):
        conn = _Conn(self.store)
        self.conns.append(conn)
        yield conn


class _Manager:
    def __init__(self, pool: _Pool) -> None:
        self.pool = pool


class FenceDataAccess(FakeDataAccess):
    """FakeDataAccess + 実行行の種類 + 接続プールを持つ db（runner は ``data_access.db.pool`` で fence を取る）。"""

    def __init__(self, store: _Store | None, protocol: str | None = "mp-chat/1",
                 protocol_query_fails: bool = False, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._protocol = protocol
        self._protocol_query_fails = protocol_query_fails
        if store is not None:
            self.db = _Manager(_Pool(store))

    async def execute_query(self, query: str, params: tuple) -> dict[str, Any]:
        if "runtime_protocol" in query:
            if self._protocol_query_fails:
                return {"success": False, "data": [], "error": "synthetic"}
            return {"success": True, "data": [{"runtime_protocol": self._protocol}]}
        return await super().execute_query(query, params)


async def _run(agent, store: _Store | None, handler: RecordingHandler, protocol: str | None = "mp-chat/1",
               **kwargs):
    return await arun_marketplace_agent(
        agent,
        env=BASE_ENV,
        data_access=FenceDataAccess(store, protocol=protocol,
                                    protocol_query_fails=kwargs.pop("protocol_query_fails", False)),
        event_handler=handler,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# 1〜5
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_free_fence_writes_marker_then_runs_agent() -> None:
    store, handler, agent = _Store(), RecordingHandler(), make_agent("OK")
    assert await _run(agent, store, handler) == "OK"
    assert agent.calls == ["hello agenticstar"]
    assert len(handler.terminal_events()) == 1
    [marker] = store.rows
    assert marker["conversation_id"] == BASE_ENV["CONVERSATION_ID"]
    assert marker["message_id"] == BASE_ENV["MESSAGE_ID"]
    assert marker["user_id"] == BASE_ENV["USER_ID"]
    assert marker["chunk_type"] == "progress_message"
    assert marker["content_data"]["kind"] == MARKER_KIND
    assert marker["content_data"]["execution_id"] == BASE_ENV["EXECUTION_ID"]
    assert isinstance(marker["content_data"]["progress_message"], str)
    # 分離レベルは READ COMMITTED に固定（DB の既定が REPEATABLE READ でも両方が通らない）
    assert store.isolations == ["read_committed"]


@pytest.mark.asyncio
async def test_rerun_after_pod_recreation_does_not_run_agent_or_emit() -> None:
    store = _Store()
    first_handler, first_agent = RecordingHandler(), make_agent()
    await _run(first_agent, store, first_handler)

    # controller が Pod を作り直した = 同じ identity で runner がもう一度起動する
    second_handler, second_agent = RecordingHandler(), make_agent()
    with pytest.raises(MarketplaceRunnerFenceTaken):
        await _run(second_agent, store, second_handler)
    assert second_agent.calls == []
    assert second_handler.events == []  # 失敗のイベントも送らない（終端は executor が決める）
    assert len(store.rows) == 1  # 印は増えない


@pytest.mark.asyncio
async def test_any_existing_event_row_blocks_the_rerun() -> None:
    # 旧版の runner が印を書かずにイベントだけ残した実行でも、二度目は走らせない
    store = _Store()
    store.rows.append({"conversation_id": BASE_ENV["CONVERSATION_ID"], "message_id": BASE_ENV["MESSAGE_ID"],
                       "user_id": BASE_ENV["USER_ID"], "chunk_type": "content", "content_data": {"content": "x"}})
    handler, agent = RecordingHandler(), make_agent()
    with pytest.raises(MarketplaceRunnerFenceTaken):
        await _run(agent, store, handler)
    assert agent.calls == [] and handler.events == []


@pytest.mark.asyncio
async def test_concurrent_runners_run_the_agent_once() -> None:
    store = _Store()
    agents = [make_agent(), make_agent()]
    handlers = [RecordingHandler(), RecordingHandler()]
    results = await asyncio.gather(
        *(_run(a, store, h) for a, h in zip(agents, handlers, strict=True)), return_exceptions=True
    )
    assert sum(len(a.calls) for a in agents) == 1
    assert sum(isinstance(r, MarketplaceRunnerFenceTaken) for r in results) == 1
    assert len(store.rows) == 1


@pytest.mark.asyncio
async def test_other_message_is_independent() -> None:
    store = _Store()
    await _run(make_agent(), store, RecordingHandler())
    other = make_agent()
    await arun_marketplace_agent(
        other, env={**BASE_ENV, "MESSAGE_ID": "msg-0002", "EXECUTION_ID": "exec-0002"},
        data_access=FenceDataAccess(store), event_handler=RecordingHandler(),
    )
    assert len(other.calls) == 1 and len(store.rows) == 2


@pytest.mark.asyncio
@pytest.mark.parametrize("fail_on", ["lock", "select", "insert", "commit"])
async def test_db_failure_is_fail_closed(fail_on: str) -> None:
    store = _Store()
    store.fail_on = fail_on
    handler, agent = RecordingHandler(), make_agent()
    with pytest.raises(Exception) as excinfo:
        await _run(agent, store, handler)
    assert not isinstance(excinfo.value, MarketplaceRunnerFenceTaken)  # 「取られていた」とは言わない
    # 所有を確かめられない runner は終端を送らない（先行の runner が送っていれば二重になる。PO 判断 2026-10-06）
    assert agent.calls == [] and handler.events == []
    assert store.rows == []  # rollback（印を残さない）
    assert all(not lock.locked() for lock in store.locks.values())  # ロックは解放


@pytest.mark.asyncio
async def test_cycle_execution_without_pool_is_a_config_error_by_default() -> None:
    handler, agent = RecordingHandler(), make_agent()
    with pytest.raises(MarketplaceRunnerConfigError, match="started_fence=False"):
        await _run(agent, None, handler)
    assert agent.calls == [] and handler.events == []


@pytest.mark.asyncio
async def test_fence_can_be_turned_off() -> None:
    handler, agent = RecordingHandler(), make_agent()
    await _run(agent, None, handler, started_fence=False)
    assert len(agent.calls) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("protocol", [None, "mp-workflow/1", ""])
async def test_normal_conversation_is_unchanged(protocol) -> None:
    # 通常の会話（restartPolicy=OnFailure）は従来どおり: 既存の行があっても走り直し、印を書かず、プールも要らない
    store = _Store()
    store.rows.append({"conversation_id": BASE_ENV["CONVERSATION_ID"], "message_id": BASE_ENV["MESSAGE_ID"],
                       "user_id": BASE_ENV["USER_ID"], "chunk_type": "content", "content_data": {"content": "x"}})
    handler, agent = RecordingHandler(), make_agent()
    await _run(agent, store, handler, protocol=protocol)
    assert len(agent.calls) == 1 and len(store.rows) == 1 and store.isolations == []
    no_pool_agent = make_agent()
    await _run(no_pool_agent, None, RecordingHandler(), protocol=protocol)
    assert len(no_pool_agent.calls) == 1


@pytest.mark.asyncio
async def test_unreadable_execution_kind_takes_the_fence() -> None:
    # 実行行の種類を読めない時はサイクル型として fence を取る: 初回は印を書いて走り、作り直しの後は拒む
    store = _Store()
    first = make_agent()
    await _run(first, store, RecordingHandler(), protocol_query_fails=True)
    assert len(first.calls) == 1 and len(store.rows) == 1
    second, handler = make_agent(), RecordingHandler()
    with pytest.raises(MarketplaceRunnerFenceTaken):
        await _run(second, store, handler, protocol_query_fails=True)
    assert second.calls == [] and handler.events == []


@pytest.mark.asyncio
@pytest.mark.parametrize("bad", ["raise", "empty", "not_a_list"])
async def test_unreadable_kind_variants_take_the_fence(bad: str) -> None:
    class _Odd(FenceDataAccess):
        async def execute_query(self, query: str, params: tuple) -> dict[str, Any]:
            if "runtime_protocol" in query:
                if bad == "raise":
                    raise RuntimeError("synthetic")
                return {"success": True, "data": [] if bad == "empty" else {"runtime_protocol": None}}
            return await super().execute_query(query, params)

    store = _Store()
    store.rows.append({"conversation_id": BASE_ENV["CONVERSATION_ID"], "message_id": BASE_ENV["MESSAGE_ID"],
                       "user_id": BASE_ENV["USER_ID"], "chunk_type": "content", "content_data": {"content": "x"}})
    agent, handler = make_agent(), RecordingHandler()
    with pytest.raises(MarketplaceRunnerFenceTaken):
        await arun_marketplace_agent(agent, env=BASE_ENV, data_access=_Odd(store), event_handler=handler)
    assert agent.calls == [] and handler.events == []


@pytest.mark.asyncio
async def test_unreadable_kind_without_pool_behaves_as_before() -> None:
    # 種類を読めず印を取る手段も無い時は従来どおり（入力取得に任せる）
    agent = make_agent()
    await _run(agent, None, RecordingHandler(), protocol_query_fails=True)
    assert len(agent.calls) == 1


def test_sync_entry_raises_so_the_process_exits_non_zero() -> None:
    # run_marketplace_agent（Pod の entrypoint）は例外のまま返す = 未捕捉で非0終了（exit 0 は「実行終了」扱い）
    store = _Store()
    asyncio.run(_run(make_agent(), store, RecordingHandler()))
    agent = make_agent()
    with pytest.raises(MarketplaceRunnerFenceTaken):
        run_marketplace_agent(agent, env=BASE_ENV, data_access=FenceDataAccess(store),
                              event_handler=RecordingHandler())
    assert agent.calls == []


@pytest.mark.asyncio
async def test_refused_run_does_not_build_the_default_handler(monkeypatch) -> None:
    # 既定の handler（DB + webhook）を作る前に止まる = webhook も DB 保存も起きない
    import agenticstar_platform.runner as runner_module

    store = _Store()
    await _run(make_agent(), store, RecordingHandler())
    built: list[Any] = []
    monkeypatch.setattr(runner_module, "create_marketplace_handler", lambda **kw: built.append(kw))
    agent = make_agent()
    with pytest.raises(MarketplaceRunnerFenceTaken):
        await arun_marketplace_agent(agent, env=BASE_ENV, data_access=FenceDataAccess(store))
    assert built == [] and agent.calls == []


@pytest.mark.asyncio
async def test_uninitialized_injected_pool_is_initialized_before_the_fence() -> None:
    class _LazyManager:
        def __init__(self, pool: _Pool) -> None:
            self._pool_to_use, self.pool = pool, None

    class _LazyDataAccess(FenceDataAccess):
        async def ensure_initialized(self) -> None:
            self.db.pool = self.db._pool_to_use

    store = _Store()
    da = _LazyDataAccess(None)
    da.db = _LazyManager(_Pool(store))
    agent = make_agent()
    await arun_marketplace_agent(agent, env=BASE_ENV, data_access=da, event_handler=RecordingHandler())
    assert len(agent.calls) == 1 and len(store.rows) == 1


def test_lock_key_is_deterministic_signed_64bit_and_pair_specific() -> None:
    a = fence_lock_key("conv-1", "msg-1")
    assert a == fence_lock_key("conv-1", "msg-1")
    assert -(2 ** 63) <= a < 2 ** 63
    assert a != fence_lock_key("conv-1", "msg-2")
    assert a != fence_lock_key("conv-2", "msg-1")
    # 区切りがあるので連結の境目をずらしても同じにならない
    assert fence_lock_key("ab", "c") != fence_lock_key("a", "bc")


# ---------------------------------------------------------------------------
# 実 PostgreSQL（AGENTICSTAR_SDK_TEST_PG_DSN がある時だけ）
# ---------------------------------------------------------------------------

PG_DSN = os.environ.get("AGENTICSTAR_SDK_TEST_PG_DSN")


@pytest.mark.skipif(not PG_DSN, reason="AGENTICSTAR_SDK_TEST_PG_DSN が無い（実 PostgreSQL の試験は省略）")
class TestRealPostgres:
    @pytest.fixture
    async def pool(self):
        asyncpg = pytest.importorskip("asyncpg")
        schema = f"fence_{uuid.uuid4().hex[:12]}"
        admin = await asyncpg.connect(PG_DSN)
        await admin.execute(f"CREATE SCHEMA {schema}")
        # 本番の表と同じ列（partition は試験に関係しないので省く）
        await admin.execute(f"""
            CREATE TABLE {schema}.execution_messages (
                id bigserial, user_id text NOT NULL, conversation_id text NOT NULL,
                message_id text NOT NULL, chunk_type text NOT NULL, content_data jsonb NOT NULL,
                created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
                PRIMARY KEY (id, created_at))""")
        pool = await asyncpg.create_pool(PG_DSN, min_size=2, max_size=4,
                                         server_settings={"search_path": schema})
        try:
            yield pool
        finally:
            await pool.close()
            await admin.execute(f"DROP SCHEMA {schema} CASCADE")
            await admin.close()

    @staticmethod
    def _ids(**over: str) -> dict[str, str]:
        return {"user_id": "u-1", "conversation_id": "c-1", "message_id": "m-1", "execution_id": "e-1", **over}

    async def test_concurrent_take_has_exactly_one_winner(self, pool) -> None:
        results = await asyncio.gather(*(take_started_fence(pool, **self._ids()) for _ in range(5)),
                                       return_exceptions=True)
        assert sum(r is None for r in results) == 1
        assert sum(isinstance(r, StartedFenceTaken) for r in results) == 4
        assert await pool.fetchval("SELECT count(*) FROM execution_messages") == 1

    async def test_sequential_retake_is_refused_and_other_pair_is_free(self, pool) -> None:
        await take_started_fence(pool, **self._ids())
        with pytest.raises(StartedFenceTaken):
            await take_started_fence(pool, **self._ids())
        await take_started_fence(pool, **self._ids(message_id="m-2", execution_id="e-2"))
        row = await pool.fetchrow("SELECT chunk_type, content_data FROM execution_messages WHERE message_id = 'm-1'")
        assert row["chunk_type"] == "progress_message"
        assert json.loads(row["content_data"])["kind"] == MARKER_KIND

    async def test_repeatable_read_default_still_has_one_winner(self, pool) -> None:
        asyncpg = pytest.importorskip("asyncpg")
        schema = await pool.fetchval("SELECT current_schema()")
        rr_pool = await asyncpg.create_pool(PG_DSN, min_size=2, max_size=6, server_settings={
            "search_path": schema, "default_transaction_isolation": "repeatable read"})
        try:
            results = await asyncio.gather(*(take_started_fence(rr_pool, **self._ids()) for _ in range(5)),
                                           return_exceptions=True)
        finally:
            await rr_pool.close()
        assert sum(r is None for r in results) == 1
        assert sum(isinstance(r, StartedFenceTaken) for r in results) == 4

    async def test_rollback_on_failure_leaves_no_marker_and_releases_the_lock(self, pool) -> None:
        async with pool.acquire() as conn:
            await conn.execute("ALTER TABLE execution_messages ADD CONSTRAINT no_marker CHECK (chunk_type <> 'progress_message')")
        with pytest.raises(Exception) as excinfo:
            await take_started_fence(pool, **self._ids())
        assert not isinstance(excinfo.value, StartedFenceTaken)
        assert await pool.fetchval("SELECT count(*) FROM execution_messages") == 0
        async with pool.acquire() as conn:
            await conn.execute("ALTER TABLE execution_messages DROP CONSTRAINT no_marker")
        await take_started_fence(pool, **self._ids())  # ロックが残っていれば 10 秒で lock_timeout になる
