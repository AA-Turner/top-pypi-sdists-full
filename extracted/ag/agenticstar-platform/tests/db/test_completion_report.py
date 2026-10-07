"""サイクル型の完遂報告（``db/completion_report.py``）の契約テスト。

固定する契約（devdocs 3.1req 指示書 37）:
    1. 報告すると ``execution_messages`` に 1 行書く（印と同じ progress_message の形 + 報告の中身）
    2. ``outcome`` の語彙外は ``ValueError``（呼び出し側の誤り）。DB には触らない
    3. 報告は 1 回。同じ実行に報告が既にあれば書かずに False（最初の報告を残す）
    4. **DB の失敗で例外を投げない**（握って False。Agent の処理を失敗させない。印の fail closed とは逆）
    5. ``reason`` を省略すると ``outcome`` と同じ値になる
    6. 同じ実行に同時に 2 回報告しても 1 行だけ（advisory lock で直列にしてから存在を確かめる。
       READ COMMITTED・接続の取得とロック待ちに上限）
    7. ``reason`` は workflow runner と同じ短い snake_case に正規化し、合わない値（文章・長い値）は ``outcome``
       に置き換える（executor の ``outcome_reason_code`` は VARCHAR(64)。長い値で終端を壊さない）。例外は投げない

synthetic な pool（asyncpg の acquire / transaction / execute / fetchval の契約だけ）で固定する。

実行: python -m pytest sdk/tests/db/test_completion_report.py -v
"""

from __future__ import annotations

import asyncio
import contextlib
import enum
import json
from typing import Any

import pytest

from agenticstar_platform.db.completion_report import (
    ACQUIRE_TIMEOUT_SECONDS,
    OUTCOMES,
    REPORT_KIND,
    report_completion,
    report_content,
    report_lock_key,
)
from agenticstar_platform.db.started_fence import fence_lock_key

IDENT = {
    "user_id": "u-1",
    "conversation_id": "c-1",
    "message_id": "m-1",
    "execution_id": "e-1",
}


class _Conn:
    """advisory lock は transaction の終わりまで持つ（pg_advisory_xact_lock と同じ）。"""

    def __init__(self, store: "_Store") -> None:
        self._store = store
        self._held: list[asyncio.Lock] = []

    @contextlib.asynccontextmanager
    async def transaction(self, **kw: Any):
        if self._store.fail_on == "transaction":
            raise RuntimeError("transaction failed")
        self._store.calls.append(("transaction", kw))
        try:
            yield
            if self._store.fail_on == "commit":
                raise RuntimeError("commit failed")
        except BaseException:
            if self._store.fail_on == "cancel_then_rollback_fails":
                raise RuntimeError("rollback failed")  # noqa: B904 — 取消を置き換える後片付けの失敗を再現する
            if self._store.fail_on == "cancel_then_rollback_fails_with_cause":
                # cause が付いていても、取消は context 側に残っている
                raise RuntimeError("rollback failed") from OSError("connection reset")
            raise
        finally:
            while self._held:
                self._held.pop().release()

    async def execute(self, sql: str, *args: Any) -> None:
        if sql.startswith("SET LOCAL"):
            self._store.calls.append(("set", sql))
            return
        if sql.startswith("SELECT pg_advisory_xact_lock"):
            if self._store.fail_on == "lock":
                raise RuntimeError("canceling statement due to lock timeout")
            self._store.calls.append(("lock", args[0]))
            lock = self._store.locks.setdefault(args[0], asyncio.Lock())
            await lock.acquire()
            self._held.append(lock)
            return
        if self._store.fail_on == "insert":
            raise RuntimeError("insert failed")
        self._store.rows.append({"sql": sql, "args": args})

    async def fetchval(self, sql: str, *args: Any) -> Any:
        if self._store.fail_on == "select":
            raise RuntimeError("select failed")
        if self._store.fail_on in ("cancel", "cancel_then_rollback_fails", "cancel_then_rollback_fails_with_cause"):
            raise asyncio.CancelledError()
        self._store.calls.append(("select", None))
        conversation_id, message_id, kind = args
        exists = any(
            r["args"][1] == conversation_id
            and r["args"][2] == message_id
            and json.loads(r["args"][3]).get("kind") == kind
            for r in self._store.rows
        )
        # 確認と INSERT の間で他の task に順番を渡す（ロックが無ければ 2 つとも「無い」と読んで書く）
        await asyncio.sleep(0)
        return exists


class _Store:
    def __init__(self, fail_on: str | None = None) -> None:
        self.rows: list[dict[str, Any]] = []
        self.fail_on = fail_on
        self.calls: list[tuple[str, Any]] = []
        self.locks: dict[int, asyncio.Lock] = {}
        self.acquire_kwargs: list[dict[str, Any]] = []

    @contextlib.asynccontextmanager
    async def acquire(self, **kw: Any):
        if self.fail_on == "acquire":
            raise RuntimeError("acquire failed")
        self.acquire_kwargs.append(kw)
        yield _Conn(self)
        if self.fail_on == "release":
            raise RuntimeError("release failed")

    @property
    def inserted(self) -> list[dict[str, Any]]:
        return [json.loads(r["args"][3]) for r in self.rows]


@pytest.mark.asyncio
async def test_writes_one_row_in_the_marker_shape():
    pool = _Store()
    assert await report_completion(pool, outcome="completed", summary="done", **IDENT) is True
    assert len(pool.rows) == 1
    content = pool.inserted[0]
    assert content["kind"] == REPORT_KIND
    assert content["outcome"] == "completed"
    assert content["outcome_reason_code"] == "completed"
    assert content["execution_id"] == "e-1"
    assert content["summary"] == "done"
    # 印と同じ形（progress_message を持つ）であること
    assert "progress_message" in content
    sql = pool.rows[0]["sql"]
    assert "INSERT INTO execution_messages" in sql
    assert "'progress_message'" in sql


@pytest.mark.asyncio
@pytest.mark.parametrize("outcome", list(OUTCOMES))
async def test_accepts_every_value_of_the_saved_vocabulary(outcome):
    pool = _Store()
    assert await report_completion(pool, outcome=outcome, **IDENT) is True
    assert pool.inserted[0]["outcome"] == outcome


@pytest.mark.asyncio
async def test_unknown_outcome_is_a_caller_error_and_touches_nothing():
    pool = _Store()
    with pytest.raises(ValueError):
        await report_completion(pool, outcome="success", **IDENT)
    assert pool.rows == []


@pytest.mark.asyncio
async def test_reports_only_once_and_keeps_the_first():
    pool = _Store()
    assert await report_completion(pool, outcome="completed", **IDENT) is True
    assert await report_completion(pool, outcome="failed", **IDENT) is False
    assert len(pool.rows) == 1
    assert pool.inserted[0]["outcome"] == "completed"


@pytest.mark.asyncio
async def test_concurrent_reports_write_one_row():
    pool = _Store()
    results = await asyncio.gather(
        report_completion(pool, outcome="completed", **IDENT),
        report_completion(pool, outcome="failed", **IDENT),
    )
    assert sorted(results) == [False, True]
    assert len(pool.rows) == 1
    assert pool.inserted[0]["outcome"] == "completed"


@pytest.mark.asyncio
async def test_each_execution_gets_its_own_report():
    pool = _Store()
    other = dict(IDENT, message_id="m-2", execution_id="e-2")
    results = await asyncio.gather(
        report_completion(pool, outcome="completed", **IDENT),
        report_completion(pool, outcome="failed", **other),
    )
    assert results == [True, True]
    assert sorted(c["outcome"] for c in pool.inserted) == ["completed", "failed"]


@pytest.mark.asyncio
@pytest.mark.parametrize("bad", [None, 123, "c-\ud800"])
async def test_malformed_ids_do_not_raise(bad):
    pool = _Store()
    ident = dict(IDENT, conversation_id=bad)
    assert await report_completion(pool, outcome="completed", **ident) is False
    assert pool.rows == []


@pytest.mark.asyncio
async def test_lock_is_taken_before_the_existence_check_in_read_committed():
    pool = _Store()
    await report_completion(pool, outcome="completed", **IDENT)
    kinds = [c[0] for c in pool.calls]
    assert kinds.index("lock") < kinds.index("select")
    assert ("transaction", {"isolation": "read_committed"}) in pool.calls
    assert any(c == ("set", "SET LOCAL lock_timeout = '10s'") for c in pool.calls)
    assert ("lock", report_lock_key("c-1", "m-1")) in pool.calls
    assert pool.acquire_kwargs == [{"timeout": ACQUIRE_TIMEOUT_SECONDS}]


def test_lock_key_is_stable_and_separate_from_the_started_fence():
    assert report_lock_key("c-1", "m-1") == report_lock_key("c-1", "m-1")
    assert report_lock_key("c-1", "m-1") != report_lock_key("c-1", "m-2")
    assert report_lock_key("c-1", "m-1") != fence_lock_key("c-1", "m-1")
    assert -(2**63) <= report_lock_key("c-1", "m-1") < 2**63


@pytest.mark.asyncio
@pytest.mark.parametrize("fail_on", ["acquire", "transaction", "lock", "select", "insert", "commit", "release"])
async def test_db_failure_does_not_raise_and_does_not_fail_the_agent(fail_on):
    pool = _Store(fail_on=fail_on)
    assert await report_completion(pool, outcome="completed", **IDENT) is False


@pytest.mark.asyncio
async def test_reason_defaults_to_the_outcome_and_can_be_given():
    pool = _Store()
    await report_completion(pool, outcome="incomplete", **IDENT)
    assert pool.inserted[0]["outcome_reason_code"] == "incomplete"
    pool2 = _Store()
    await report_completion(pool2, outcome="incomplete", reason="goal_unreachable", **IDENT)
    assert pool2.inserted[0]["outcome_reason_code"] == "goal_unreachable"


@pytest.mark.asyncio
async def test_had_mutating_success_is_carried_as_given():
    for value in (True, False, None):
        pool = _Store()
        await report_completion(pool, outcome="completed", had_mutating_success=value, **IDENT)
        assert pool.inserted[0]["had_mutating_success"] is value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("reason", "expected"),
    [
        ("Goal-Unreachable", "goal_unreachable"),
        ("  no new items ", "no_new_items"),
        ("a" * 32, "a" * 32),
        ("a" * 33, "incomplete"),
        ("x" * 71, "incomplete"),
        ("Traceback (most recent call last): KeyError('x')", "incomplete"),
        ("1st_try", "incomplete"),
        ("", "incomplete"),
        (123, "incomplete"),
        (False, "incomplete"),
    ],
)
async def test_reason_is_normalized_and_falls_back_to_the_outcome(reason, expected):
    pool = _Store()
    assert await report_completion(pool, outcome="incomplete", reason=reason, **IDENT) is True
    code = pool.inserted[0]["outcome_reason_code"]
    assert code == expected
    assert len(code) <= 64


class _Outcome(enum.StrEnum):
    COMPLETED = "completed"


class _Reason(str, enum.Enum):  # noqa: UP042 — str を混ぜた Enum（StrEnum でない）の値の扱いを固定する
    GOAL_UNREACHABLE = "goal_unreachable"


class _HostileStr(str):
    def __eq__(self, other: object) -> bool:
        raise RuntimeError("hostile __eq__")

    __hash__ = str.__hash__


@pytest.mark.asyncio
async def test_str_enum_outcome_is_accepted_as_its_value():
    pool = _Store()
    assert await report_completion(pool, outcome=_Outcome.COMPLETED, **IDENT) is True
    assert pool.inserted[0]["outcome"] == "completed"
    assert type(pool.inserted[0]["outcome"]) is str


@pytest.mark.asyncio
async def test_str_enum_reason_is_taken_as_its_value():
    pool = _Store()
    assert await report_completion(pool, outcome="incomplete", reason=_Reason.GOAL_UNREACHABLE, **IDENT) is True
    assert pool.inserted[0]["outcome_reason_code"] == "goal_unreachable"


@pytest.mark.asyncio
@pytest.mark.parametrize("bad", [123, None, _HostileStr("success"), _HostileStr("completedx")])
async def test_only_value_error_for_a_bad_outcome(bad):
    pool = _Store()
    with pytest.raises(ValueError):
        await report_completion(pool, outcome=bad, **IDENT)
    assert pool.rows == []


@pytest.mark.asyncio
async def test_broken_values_besides_the_outcome_return_false():
    nested: list = []
    for _ in range(100_000):
        nested = [nested]
    for kwargs in (
        dict(IDENT, execution_id=nested),
        dict(IDENT, execution_id=object()),
        dict(IDENT, summary=object()),
    ):
        pool = _Store()
        assert await report_completion(pool, outcome="completed", **kwargs) is False


@pytest.mark.asyncio
@pytest.mark.parametrize("fail_on", ["cancel", "cancel_then_rollback_fails", "cancel_then_rollback_fails_with_cause"])
async def test_cancellation_propagates_even_when_cleanup_fails(fail_on):
    pool = _Store(fail_on=fail_on)
    with pytest.raises(asyncio.CancelledError):
        await report_completion(pool, outcome="completed", **IDENT)


def test_report_content_omits_summary_when_not_given():
    assert "summary" not in report_content("e-1", "completed", "completed")
