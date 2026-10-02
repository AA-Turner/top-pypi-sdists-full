"""Refs agentcore#330: PostgreSQLManager.execute_query() が結果セットの有無を
クエリ文字列の先頭語（"SELECT" / "RETURNING" 含有）で判定していたため、
WITH ... SELECT / VALUES / TABLE など行を返す文が conn.execute() 側へ流れ、
行が黙って捨てられていた（success=True のまま data={"result": "SELECT 1"}）。

ここで固定する契約:
- 結果セットの有無はサーバの Describe（PreparedStatement.get_attributes()）
  または「行が返ったこと」で決める（0 列 SELECT も行を保持する）
- 結果セットを持つ文は先頭語に関係なく List[Dict] を返す
- 結果セットを持たない文（INSERT/UPDATE/DDL、RETURNING 無しの data-modifying CTE）は
  従来どおり {"result": <status>} を返す
- prepare は無名 statement（name=""）で、command_timeout は prepare/fetch で共有する
- ";" 区切りの複数文は、旧実装で simple protocol に流れていた経路
  （パラメータ無し・先頭が SELECT でなく RETURNING を含まない）だけフォールバックする。
  それ以外は従来どおり success=False
- 例外は success=False / error_code="DB_QUERY_ERROR" に畳む（従来契約）
"""

from contextlib import asynccontextmanager

import asyncpg
import pytest

from agenticstar_platform.db.config import PostgreSQLConfig
from agenticstar_platform.db.manager import (
    PostgreSQLManager,
    _is_multi_command_error,
    _legacy_dispatch_used_fetch,
    _looks_row_producing,
)


class FakeRecord(dict):
    """asyncpg.Record の代替（dict(row) で辞書化できれば十分）。"""


class FakeStatement:
    def __init__(self, attributes, rows, status):
        self._attributes = attributes
        self._rows = rows
        self._status = status
        self.fetch_args = None
        self.fetch_timeout = "unset"

    async def fetch(self, *params, timeout=None):
        self.fetch_args = params
        self.fetch_timeout = timeout
        return [FakeRecord(r) for r in self._rows]

    def get_attributes(self):
        return self._attributes

    def get_statusmsg(self):
        return self._status


class FakeConn:
    """prepare()/execute() の呼び出しを捕捉する最小スタブ。

    statements: {query: FakeStatement | Exception}
    """

    def __init__(self, statements):
        self._statements = statements
        self.executed = []
        self.prepare_calls = []

    async def prepare(self, query, *, name=None, timeout=None):
        self.prepare_calls.append({"query": query, "name": name, "timeout": timeout})
        stmt = self._statements[query]
        if isinstance(stmt, Exception):
            raise stmt
        return stmt

    async def execute(self, query, *params):
        self.executed.append((query, params))
        return "CREATE TABLE"


class FakePool:
    def __init__(self, conn):
        self._conn = conn

    @asynccontextmanager
    async def acquire(self):
        yield self._conn


def _manager(conn, command_timeout=60) -> PostgreSQLManager:
    cfg = PostgreSQLConfig(
        host="h", database="d", username="u", password="p", command_timeout=command_timeout
    )
    m = PostgreSQLManager(cfg)
    m.pool = FakePool(conn)

    async def _noop():
        return None

    m._ensure_initialized = _noop  # type: ignore[method-assign]
    return m


def _multi_command_error() -> asyncpg.PostgresSyntaxError:
    return asyncpg.PostgresSyntaxError(
        "cannot insert multiple commands into a prepared statement"
    )


# --- 結果セットを持つ文は先頭語に関係なく行を返す ----------------------------


@pytest.mark.parametrize(
    ("query", "params"),
    [
        ("WITH t AS (SELECT 1 AS n) SELECT * FROM t", ()),   # issue の再現ケース
        ("VALUES (1, 'a')", ()),
        ("TABLE some_table", ()),
        ("-- comment\n(SELECT 1 AS n)", ()),
        ("SHOW server_version", ()),
        ("EXPLAIN SELECT 1", ()),
        ("SELECT $1::int AS n", (1,)),
        ("INSERT INTO t(v) VALUES ($1) RETURNING n", ("v",)),
    ],
)
async def test_row_producing_statement_returns_rows_regardless_of_prefix(query, params):
    stmt = FakeStatement(attributes=("n",), rows=[{"n": 1}], status="SELECT 1")
    conn = FakeConn({query: stmt})

    result = await _manager(conn).execute_query(query, params)

    assert result == {"success": True, "data": [{"n": 1}]}
    assert stmt.fetch_args == params
    assert conn.executed == [], "結果セットを持つ文が conn.execute() へ流れている（行喪失）"


async def test_row_producing_statement_with_zero_rows_returns_empty_list():
    query = "TABLE empty_table"
    conn = FakeConn({query: FakeStatement(attributes=("id",), rows=[], status="SELECT 0")})

    result = await _manager(conn).execute_query(query)

    # 「0 行の結果セット」は [] であり、status dict に化けない
    assert result == {"success": True, "data": []}


async def test_zero_column_result_set_keeps_rows():
    # SELECT FROM generate_series(1, 3): 列は無いが行は 3 つある（attributes は空）
    query = "SELECT FROM generate_series(1, 3)"
    conn = FakeConn({query: FakeStatement(attributes=(), rows=[{}, {}, {}], status="SELECT 3")})

    result = await _manager(conn).execute_query(query)

    assert result == {"success": True, "data": [{}, {}, {}]}


async def test_params_are_passed_to_fetch_after_nul_sanitization():
    query = "SELECT $1::text AS s"
    stmt = FakeStatement(attributes=("s",), rows=[{"s": "ab"}], status="SELECT 1")
    conn = FakeConn({query: stmt})

    result = await _manager(conn).execute_query(query, ("a\x00b",))

    assert result["success"] is True
    assert stmt.fetch_args == ("ab",)  # 既存の NUL 除去はそのまま効く


# --- prepared statement の使い方（無名 / タイムアウト共有） ------------------------


async def test_prepare_uses_unnamed_statement_and_shares_command_timeout():
    query = "SELECT 1 AS n"
    stmt = FakeStatement(attributes=("n",), rows=[{"n": 1}], status="SELECT 1")
    conn = FakeConn({query: stmt})

    await _manager(conn, command_timeout=30).execute_query(query)

    # asyncpg 0.29/0.30 は prepare() 既定で名前付き statement を作るため name="" を明示する
    assert conn.prepare_calls == [{"query": query, "name": "", "timeout": 30}]
    # fetch には prepare で消費した分を差し引いた残り予算が渡る（別予算にしない）
    assert stmt.fetch_timeout is not None
    assert 0 < stmt.fetch_timeout <= 30


async def test_unset_command_timeout_means_no_deadline():
    # asyncpg は command_timeout<=0 を pool 初期化で拒否するので、無期限は None で表す
    query = "SELECT 1 AS n"
    stmt = FakeStatement(attributes=("n",), rows=[{"n": 1}], status="SELECT 1")
    conn = FakeConn({query: stmt})

    await _manager(conn, command_timeout=None).execute_query(query)

    assert conn.prepare_calls[0]["timeout"] is None
    assert stmt.fetch_timeout is None


async def test_budget_exhausted_by_prepare_is_reported_as_failure(monkeypatch):
    query = "SELECT 1 AS n"
    stmt = FakeStatement(attributes=("n",), rows=[{"n": 1}], status="SELECT 1")
    conn = FakeConn({query: stmt})

    import agenticstar_platform.db.manager as mod

    ticks = [100.0, 100.0 + 5.0]  # prepare だけで 5 秒消費 → 予算 (1s) 超過

    def fake_monotonic():
        return ticks.pop(0) if len(ticks) > 1 else ticks[0]

    monkeypatch.setattr(mod.time, "monotonic", fake_monotonic)

    result = await _manager(conn, command_timeout=1).execute_query(query)

    assert result["success"] is False
    assert result["error_code"] == "DB_QUERY_ERROR"
    assert stmt.fetch_args is None, "予算超過後に fetch を発行してはいけない"


# --- 結果セットを持たない文は従来どおり status dict ---------------------------


@pytest.mark.parametrize(
    ("query", "params", "status"),
    [
        ("INSERT INTO t(v) VALUES ($1)", ("x",), "INSERT 0 1"),
        ("UPDATE t SET v = 1", (), "UPDATE 3"),
        ("DELETE FROM t", (), "DELETE 0"),
        ("CREATE TABLE IF NOT EXISTS t(id int)", (), "CREATE TABLE"),
        # RETURNING 無しの data-modifying CTE: 先頭が WITH でも結果セットは無い
        ("WITH s AS (SELECT 'c' AS v) INSERT INTO t(v) SELECT v FROM s", (), "INSERT 0 1"),
    ],
)
async def test_non_row_statement_returns_status_dict(query, params, status):
    conn = FakeConn({query: FakeStatement(attributes=(), rows=[], status=status)})

    result = await _manager(conn).execute_query(query, params)

    assert result == {"success": True, "data": {"result": status}}


# --- 複数文フォールバック ---------------------------------------------------------


async def test_multi_statement_ddl_without_params_falls_back_to_simple_protocol(caplog):
    query = "CREATE TABLE IF NOT EXISTS a(id int); CREATE TABLE IF NOT EXISTS b(id int)"
    conn = FakeConn({query: _multi_command_error()})

    with caplog.at_level("WARNING", logger="agenticstar_platform.db.manager"):
        result = await _manager(conn).execute_query(query)

    assert result == {"success": True, "data": {"result": "CREATE TABLE"}}
    assert conn.executed == [(query, ())]
    assert not [r for r in caplog.records if "rows are not returned" in r.message]


async def test_multi_statement_fallback_warns_when_rows_would_be_dropped(caplog):
    # 旧実装でも simple protocol に流れていた（先頭が SELECT でない）batch。行は返らない
    query = "SET search_path TO public; SELECT 1"
    conn = FakeConn({query: _multi_command_error()})

    with caplog.at_level("WARNING", logger="agenticstar_platform.db.manager"):
        result = await _manager(conn).execute_query(query)

    assert result == {"success": True, "data": {"result": "CREATE TABLE"}}
    assert any("rows are not returned" in r.message for r in caplog.records)


@pytest.mark.parametrize(
    ("query", "params"),
    [
        ("SELECT $1::int; SELECT 2", (1,)),          # パラメータ付き
        ("SELECT $1::int; SELECT 2", [1]),           # list で渡されても「パラメータあり」
        ("SELECT 1; SELECT 2", ()),                  # 旧実装は fetch 側 → 同じエラーで失敗していた
        ("INSERT INTO t(v) VALUES ('a'); INSERT INTO t(v) VALUES ('b') RETURNING id", ()),
    ],
)
async def test_multi_statement_previously_rejected_stays_rejected(query, params):
    conn = FakeConn({query: _multi_command_error()})

    result = await _manager(conn).execute_query(query, params)

    assert result["success"] is False
    assert result["error_code"] == "DB_QUERY_ERROR"
    assert "multiple commands" in result["error"]
    assert conn.executed == [], "従来失敗していた複数文を simple protocol へ流してはいけない"


async def test_other_syntax_error_is_not_treated_as_multi_statement():
    query = "SELEKT 1"
    conn = FakeConn({query: asyncpg.PostgresSyntaxError('syntax error at or near "SELEKT"')})

    result = await _manager(conn).execute_query(query)

    assert result["success"] is False
    assert result["error_code"] == "DB_QUERY_ERROR"
    assert conn.executed == []


async def test_fetch_error_is_folded_into_db_query_error():
    query = "INSERT INTO t(v) VALUES ($1)"

    class BoomStatement(FakeStatement):
        async def fetch(self, *params, timeout=None):
            raise asyncpg.UniqueViolationError("duplicate key value violates unique constraint")

    conn = FakeConn({query: BoomStatement(attributes=(), rows=[], status="INSERT 0 1")})

    result = await _manager(conn).execute_query(query, ("dup",))

    assert result["success"] is False
    assert result["error_code"] == "DB_QUERY_ERROR"
    assert "duplicate key" in result["error"]


# --- ヘルパ ---------------------------------------------------------------------------


def test_is_multi_command_error_matches_only_the_multi_command_message():
    assert _is_multi_command_error(_multi_command_error())
    assert not _is_multi_command_error(
        asyncpg.PostgresSyntaxError('syntax error at or near "SELEKT"')
    )


def test_legacy_dispatch_used_fetch_mirrors_the_old_text_classifier():
    assert _legacy_dispatch_used_fetch("  select 1; select 2")
    assert _legacy_dispatch_used_fetch("INSERT INTO t VALUES (1) RETURNING id; SELECT 1")
    assert not _legacy_dispatch_used_fetch("CREATE TABLE a(id int); CREATE TABLE b(id int)")
    assert not _legacy_dispatch_used_fetch("SET a TO b; SELECT 1")


def test_looks_row_producing_heuristic():
    assert _looks_row_producing("SET a TO b; SELECT 1")
    assert not _looks_row_producing("CREATE TABLE a(id int); CREATE INDEX i ON a(id)")
