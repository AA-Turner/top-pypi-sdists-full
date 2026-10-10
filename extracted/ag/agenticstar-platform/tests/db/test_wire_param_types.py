"""molt prop-20261009-004: DB proxy の wire で TEXT の ISO 形文字列と date / datetime を見分ける添字。

ここで固定する契約 (3.0.15):
- `param_type_hint(value)` は `_serialize_param(value)` と同じ形で "datetime" / "date" / None を返す。
  list / dict は同じ形で入れ子、中に date / datetime が無ければ None に畳む
- `ApiPostgreSQLManager._api_request` は `params` と同じ並びの `param_types` を同じ JSON に添える
- `params` の中身 (isoformat 文字列・bytes の {"__bytes__"} など) は 3.0.14 までと同じ
"""

import base64
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID

import pytest

from agenticstar_platform.db.api_manager import ApiPostgreSQLManager, _serialize_param
from agenticstar_platform.db.config import PostgreSQLConfig
from agenticstar_platform.db.wire_types import (
    TYPE_DATE,
    TYPE_DATETIME,
    param_type_hint,
    serialize_param,
)

JST = timezone(timedelta(hours=9))


def test_wire_vocabulary_is_pinned_literally():
    """cli-api (別のビルド) が読む語彙。定数を変えても通らないよう字面で固定する"""
    assert (TYPE_DATETIME, TYPE_DATE) == ("datetime", "date")
    assert param_type_hint(datetime(2026, 1, 1)) == "datetime" and param_type_hint(date(2026, 1, 1)) == "date"


@pytest.mark.parametrize("value, expected", [
    (datetime(2026, 10, 9, 1, 2, 3), TYPE_DATETIME),
    (datetime(2026, 10, 9, 1, 2, 3, 456, tzinfo=timezone.utc), TYPE_DATETIME),
    (datetime(2026, 10, 9, tzinfo=JST), TYPE_DATETIME),
    (date(2026, 10, 9), TYPE_DATE),
    ("2026-10-09", None),  # TEXT に入れる ISO 形の文字列は文字列のまま (この issue の本体)
    ("2026-10-09T01:02:03+00:00", None),
    ("plain", None),
    (1, None), (1.5, None), (True, None), (None, None),
    (b"\x00\x01", None), (Decimal("1.5"), None), (UUID(int=1), None),
])
def test_hint_for_scalars(value, expected):
    assert param_type_hint(value) == expected


def test_hint_mirrors_nested_shape_and_collapses_when_nothing_to_restore():
    assert param_type_hint([date(2026, 10, 9), "2026-10-09"]) == [TYPE_DATE, None]
    assert param_type_hint((datetime(2026, 1, 1), 1)) == [TYPE_DATETIME, None]  # tuple も list の形
    assert param_type_hint(["2026-10-09", 1, None]) is None
    assert param_type_hint({"a": datetime(2026, 1, 1), "b": "2026-01-01"}) == {"a": TYPE_DATETIME, "b": None}
    assert param_type_hint({"a": "2026-01-01", "b": [1, 2]}) is None
    assert param_type_hint({"a": [{"d": date(2026, 1, 1)}, "x"], "b": 1}) == {"a": [{"d": TYPE_DATE}, None], "b": None}
    assert param_type_hint([]) is None and param_type_hint({}) is None


def test_serializer_moved_to_wire_types_keeps_name_and_wire_values():
    """api_manager._serialize_param は wire_types.serialize_param そのもの。3.0.14 までの wire 値を変えない"""
    assert _serialize_param is serialize_param
    assert serialize_param(None) is None
    assert serialize_param(datetime(2026, 10, 9, 1, 2, 3, 4, tzinfo=timezone.utc)) == "2026-10-09T01:02:03.000004+00:00"
    assert serialize_param(date(2026, 10, 9)) == "2026-10-09"
    assert serialize_param(Decimal("1.50")) == "1.50"  # 数値にしない
    assert serialize_param(UUID(int=5)) == "00000000-0000-0000-0000-000000000005"
    assert serialize_param(b"\x00") == {"__bytes__": "AA=="}
    assert serialize_param((1, "a", [date(2026, 1, 1)])) == [1, "a", ["2026-01-01"]]
    assert serialize_param({"k": date(2026, 1, 1)}) == {"k": "2026-01-01"}
    assert serialize_param(True) is True and serialize_param(1.5) == 1.5 and serialize_param("s") == "s"


def test_hint_lines_up_with_serialized_shape():
    """添字は _serialize_param の出力と同じ位置を指す (list の長さ・dict のキー)"""
    value = [date(2026, 10, 9), {"when": datetime(2026, 10, 9, 1, tzinfo=timezone.utc), "raw": b"\x01"}, ("2026-10-09", 1)]
    serialized = _serialize_param(value)
    hint = param_type_hint(value)
    assert serialized == ["2026-10-09", {"when": "2026-10-09T01:00:00+00:00", "raw": {"__bytes__": base64.b64encode(b"\x01").decode()}}, ["2026-10-09", 1]]
    assert hint == [TYPE_DATE, {"when": TYPE_DATETIME, "raw": None}, None]


class _FakeResponse:
    status_code = 200

    def json(self):
        return {"success": True, "data": []}


class _FakeClient:
    def __init__(self):
        self.calls = []

    async def post(self, url, json=None, headers=None):
        self.calls.append((url, json, headers))
        return _FakeResponse()


@pytest.mark.asyncio
async def test_api_request_sends_param_types_next_to_params(monkeypatch):
    mgr = ApiPostgreSQLManager(PostgreSQLConfig(api_url="http://cli-api:8100/db"), token_provider=lambda: "tok")
    client = _FakeClient()

    async def _client(_timeout):
        return client

    monkeypatch.setattr(mgr, "_get_http_client", _client)
    params = ("2026-10-09", date(2026, 10, 9), datetime(2026, 10, 9, 1, 2, 3, tzinfo=JST), None, b"\x00",
              [date(2026, 1, 1), "s"], {"k": datetime(2026, 1, 1)}, 7)
    out = await mgr._api_request("execute", "INSERT INTO t VALUES ($1, $2, $3, $4, $5, $6, $7, $8)", params)
    assert out == {"success": True, "data": []}
    (url, body, headers), = client.calls
    assert url == "http://cli-api:8100/db/execute" and headers == {"Authorization": "Bearer tok"}
    assert set(body) == {"query", "params", "param_types"}
    assert body["params"] == ["2026-10-09", "2026-10-09", "2026-10-09T01:02:03+09:00", None,
                              {"__bytes__": "AA=="}, ["2026-01-01", "s"], {"k": "2026-01-01T00:00:00"}, 7]
    assert body["param_types"] == [None, TYPE_DATE, TYPE_DATETIME, None, None, [TYPE_DATE, None], {"k": TYPE_DATETIME}, None]
    assert len(body["param_types"]) == len(body["params"]) == len(params)


@pytest.mark.asyncio
async def test_api_request_reads_params_once_so_an_iterator_stays_aligned(monkeypatch):
    """params を 2 度なぞらない (iterator なら 2 度目は空になり param_types が params とずれる)"""
    mgr = ApiPostgreSQLManager(PostgreSQLConfig(api_url="http://cli-api:8100/db"), token_provider=lambda: "tok")
    client = _FakeClient()

    async def _client(_timeout):
        return client

    monkeypatch.setattr(mgr, "_get_http_client", _client)
    await mgr._api_request("execute", "SELECT $1, $2", iter([date(2026, 10, 9), "2026-10-09"]))
    body = client.calls[0][1]
    assert body["params"] == ["2026-10-09", "2026-10-09"] and body["param_types"] == [TYPE_DATE, None]


@pytest.mark.asyncio
async def test_api_request_without_params_sends_empty_param_types(monkeypatch):
    mgr = ApiPostgreSQLManager(PostgreSQLConfig(api_url="http://cli-api:8100/db"), token_provider=lambda: "tok")
    client = _FakeClient()

    async def _client(_timeout):
        return client

    monkeypatch.setattr(mgr, "_get_http_client", _client)
    await mgr._api_request("execute", "SELECT 1", ())
    assert client.calls[0][1] == {"query": "SELECT 1", "params": [], "param_types": []}
