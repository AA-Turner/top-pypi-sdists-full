"""Refs #1959: DataAccess の識別子検証がエラー返し(dict)に統一されたことを検証。

- 識別子検証の失敗は raise せず {"success": False, "error_code": "INVALID_IDENTIFIER"} を返す
- 検証ロジックは common.validation へ委譲(SQLInjectionError は廃止)
"""

import pytest

from agenticstar_platform.db.data_access import DataAccess
from agenticstar_platform.common.validation import IdentifierValidationError


class FakeDB:
    """execute_query が常に成功 dict を返す最小スタブ(検証層のみを試験する目的)。"""

    def __init__(self):
        self.last_query = None

    async def initialize(self):
        pass

    async def close(self):
        pass

    async def execute_query(self, query, params=()):
        self.last_query = query
        return {"success": True, "data": [{"id": 1}], "query": query}


def _da():
    return DataAccess(FakeDB())


class TestValidIdentifiers:
    async def test_select_valid_returns_success(self):
        da = _da()
        result = await da.select("users", columns=["id", "name"])
        assert result["success"] is True
        assert "SELECT id, name FROM users" in result["query"]

    async def test_dotted_identifier_is_allowed(self):
        # common の検証はスキーマ修飾(schema.table)を許可する
        da = _da()
        result = await da.select("public.users", columns=["id"])
        assert result["success"] is True
        assert "public.users" in result["query"]


class TestInvalidIdentifierReturnsErrorDict:
    """不正識別子は例外を送出せず INVALID_IDENTIFIER の dict を返す。"""

    @pytest.mark.parametrize(
        "coro_factory",
        [
            lambda da: da.select("users; DROP TABLE users;--"),
            lambda da: da.insert("1bad_table", {"a": 1}),
            lambda da: da.upsert("t", {"a": 1}, conflict_columns=["b; --"]),
            lambda da: da.update("t", {"a": 1}, where={"x y": 1}),
            lambda da: da.delete("t", where={"col--": 1}),
            lambda da: da.select("users", order_by="name; DROP TABLE users"),
            lambda da: da.select("users", columns=["ok", "bad col"]),
        ],
    )
    async def test_returns_invalid_identifier_dict(self, coro_factory):
        da = _da()
        result = await coro_factory(da)
        assert isinstance(result, dict)
        assert result["success"] is False
        assert result["error_code"] == "INVALID_IDENTIFIER"
        assert set(result.keys()) >= {"success", "data", "error", "error_code"}

    async def test_no_query_is_executed_on_invalid_identifier(self):
        # fail-closed: 検証段で弾かれ、DB へクエリは渡らない
        db = FakeDB()
        da = DataAccess(db)
        result = await da.select("bad;--")
        assert result["error_code"] == "INVALID_IDENTIFIER"
        assert db.last_query is None

    async def test_does_not_raise(self):
        da = _da()
        try:
            result = await da.delete("bad;--", where={"id": 1})
        except IdentifierValidationError:
            pytest.fail("IdentifierValidationError が外部に漏れている(dict返し違反)")
        assert result["success"] is False


class TestSelectOne:
    async def test_select_one_returns_none_on_invalid_identifier(self):
        # select_one は Optional[Dict] 契約(row-or-None)で、検索失敗時も None を返す
        # 文書化された挙動。エラー詳細が必要なら select() を使う。
        da = _da()
        assert await da.select_one("bad;--", where={"id": 1}) is None

    async def test_select_returns_error_dict_for_same_case(self):
        # select_one では潰れる情報が、select() では error_code で取得できることを担保
        da = _da()
        result = await da.select("bad;--", where={"id": 1})
        assert result["success"] is False
        assert result["error_code"] == "INVALID_IDENTIFIER"


class TestSQLInjectionErrorRemoved:
    async def test_symbol_removed_from_module(self):
        # SQLInjectionError は data_access モジュールで定義されていたが廃止済み。
        # （db パッケージへは元々未 export のため、モジュールレベルで検証する）
        import agenticstar_platform.db.data_access as mod
        assert not hasattr(mod, "SQLInjectionError")

    async def test_validation_is_delegated_to_common(self):
        # 二重実装廃止の担保: data_access は common.validation を参照している
        import agenticstar_platform.db.data_access as mod
        assert mod.validate_identifier.__module__ == "agenticstar_platform.common.validation"
