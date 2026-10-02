"""Refs molt#1636: ai_telemetry.tools_used を metadata 落ちから named column へ昇格した契約。

背景: tools_used は DB 側に integer 列が存在し、producer (autonomous の React Agent)
も値を算出していたが、save_telemetry の known_fields / INSERT に列が無かったため
metadata jsonb へ落ちていた。結果、Admin 詳細の「使用ツール」と extapi の toolsUsed が
常時 null になっていた。

ここで固定する契約:
- tools_used は named column へ入る (metadata へは重複させない)
- 列の型は int ひとつ。list/tuple を渡された場合は要素数へ正規化する
- 未計測 (キー無し) は NULL、計測して 0 回だった場合は 0。両者を混同しない
- 正規化できない値でも telemetry 保存自体は落とさない (列は NULL)
"""

import json
import re
from datetime import datetime

import pytest

from agenticstar_platform.db.telemetry_access import TelemetryAccess


class FakeDB:
    """execute_query の query/params を捕捉するだけの最小スタブ。"""

    def __init__(self):
        self.last_query = None
        self.last_params = None

    async def execute_query(self, query, params=()):
        self.last_query = query
        self.last_params = params
        return {"success": True, "data": [{"id": 1}]}


def _column_index(query: str, column: str) -> int:
    """INSERT 文の列並びから column の 0-origin 位置を求める (位置決め打ちを避ける)。"""
    columns_block = re.search(r"INSERT INTO ai_telemetry \((.*?)\) VALUES", query, re.S)
    assert columns_block, "INSERT 文の列リストを解釈できない"
    columns = [c.strip() for c in columns_block.group(1).split(",") if c.strip()]
    assert column in columns, f"{column} が INSERT の列リストに無い: {columns}"
    return columns.index(column)


def _metadata(query: str, params) -> dict:
    idx = _column_index(query, "metadata")
    raw = params[idx]
    return json.loads(raw) if raw else {}


async def _save(telemetry_data):
    db = FakeDB()
    result = await TelemetryAccess(db).save_telemetry(telemetry_data)
    return result, db


def _base(**overrides):
    data = {"conversation_id": "conv-1636", "agent_type": "react"}
    data.update(overrides)
    return data


class TestToolsUsedReachesColumn:
    async def test_int_count_lands_in_named_column(self):
        result, db = await _save(_base(tools_used=3))
        assert result["success"] is True
        idx = _column_index(db.last_query, "tools_used")
        assert db.last_params[idx] == 3

    async def test_placeholders_are_sequential_and_match_columns(self):
        """列・placeholder・params の3者がズレると別の列に値が入る (最悪の事故)。"""
        _, db = await _save(_base(tools_used=1))
        columns_block = re.search(
            r"INSERT INTO ai_telemetry \((.*?)\) VALUES \((.*?)\)", db.last_query, re.S
        )
        columns = [c.strip() for c in columns_block.group(1).split(",") if c.strip()]
        placeholders = [p.strip() for p in columns_block.group(2).split(",") if p.strip()]
        assert len(columns) == len(placeholders) == len(db.last_params)
        # $1..$N が順番どおり (入れ替え・重複・欠番を検出する)
        assert placeholders == [f"${i}" for i in range(1, len(columns) + 1)]

    async def test_every_column_receives_its_own_value(self):
        """全列に相異なる sentinel を入れて params の並びを 1 対 1 で照合する。

        tools_used の挿入で後続列 (success 以降) が 1 つずつズレていないかを
        件数比較ではなく実値で検出する。
        """
        sentinels = {
            "timestamp": datetime(2026, 8, 27, 1, 2, 3),
            "service": "svc-sentinel",
            "operation": "op-sentinel",
            "duration_ms": 1111.5,
            "conversation_id": "conv-sentinel",
            "intent_type": "intent-sentinel",
            "confidence_score": 0.25,
            "tools_used": 42,
            "success": False,
            "agent_type": "agent-sentinel",
            "agent_level": "level-sentinel",
            "task_complexity": "complexity-sentinel",
            "current_message": "current-sentinel",
            "context_summary": "context-sentinel",
            "suggested_approach": "approach-sentinel",
            "conversation_goal": "goal-sentinel",
            "final_content": "final-sentinel",
        }
        _, db = await _save(dict(sentinels))

        for column, expected in sentinels.items():
            idx = _column_index(db.last_query, column)
            assert db.last_params[idx] == expected, f"{column} の位置がズレている"

        # 生成列: metadata は jsonb 文字列 or None、created_at は書き込み時刻
        assert db.last_params[_column_index(db.last_query, "created_at")] is not None
        metadata_idx = _column_index(db.last_query, "metadata")
        assert db.last_params[metadata_idx] is None or isinstance(
            db.last_params[metadata_idx], str
        )


class TestMeasuredZeroVsUnmeasured:
    """AC3: 未計測 (NULL) と計測済みゼロ (0) を混同しない。"""

    async def test_measured_zero_is_stored_as_zero(self):
        _, db = await _save(_base(tools_used=0))
        idx = _column_index(db.last_query, "tools_used")
        assert db.last_params[idx] == 0

    async def test_unmeasured_is_stored_as_null(self):
        # intent / guardrail / subprocess 行のように tools_used を持たない producer
        _, db = await _save(_base(agent_type="intent"))
        idx = _column_index(db.last_query, "tools_used")
        assert db.last_params[idx] is None

    async def test_explicit_none_is_stored_as_null(self):
        _, db = await _save(_base(tools_used=None))
        idx = _column_index(db.last_query, "tools_used")
        assert db.last_params[idx] is None


class TestTypeNormalization:
    """count / list のどちらを渡されても列の型は int に固定する。"""

    @pytest.mark.parametrize(
        "value,expected",
        [
            (["read", "perplexity"], 2),
            ((), 0),
            (7, 7),
        ],
    )
    async def test_normalized_to_int(self, value, expected):
        _, db = await _save(_base(tools_used=value))
        idx = _column_index(db.last_query, "tools_used")
        assert db.last_params[idx] == expected

    @pytest.mark.parametrize("value", ["three", 3.5, {"read": 1}, -1, True, False])
    async def test_uninterpretable_value_is_null_and_save_still_succeeds(self, value):
        """列を汚さず NULL にし、telemetry 保存自体は落とさない (AC4 の非回帰)。"""
        result, db = await _save(_base(tools_used=value))
        assert result["success"] is True
        idx = _column_index(db.last_query, "tools_used")
        assert db.last_params[idx] is None

    @pytest.mark.parametrize(
        "value,expected",
        [(2_147_483_647, 2_147_483_647), (2_147_483_648, None), (10**30, None)],
        ids=["int4-max", "int4-max+1", "far-out-of-range"],
    )
    async def test_postgres_integer_range_is_enforced(self, value, expected):
        """int4 の範囲外を渡すと asyncpg が落ちて行ごと失われるので列を NULL にする。"""
        result, db = await _save(_base(tools_used=value))
        assert result["success"] is True
        idx = _column_index(db.last_query, "tools_used")
        assert db.last_params[idx] == expected


class TestBreakdownIsNotLost:
    """0.5.37 以前は list をそのまま metadata に入れていた。内訳を失わせない。"""

    async def test_list_breakdown_is_kept_in_metadata(self):
        _, db = await _save(_base(tools_used=["read", "perplexity"]))
        idx = _column_index(db.last_query, "tools_used")
        assert db.last_params[idx] == 2  # 列は件数
        assert _metadata(db.last_query, db.last_params)["tools_used"] == ["read", "perplexity"]

    @pytest.mark.parametrize("value", [3, 0])
    async def test_plain_int_is_not_duplicated_into_metadata(self, value):
        """plain int は列が完全な表現なので metadata へ二重に置かない。"""
        _, db = await _save(_base(tools_used=value))
        assert "tools_used" not in _metadata(db.last_query, db.last_params)

    @pytest.mark.parametrize(
        "value",
        ["three", 3.5, {"read": 1}, -1, True, 2_147_483_648],
        ids=["str", "float", "dict", "negative", "bool", "out-of-int4-range"],
    )
    async def test_values_the_column_cannot_hold_are_kept_in_metadata(self, value):
        """列に入らない生値を metadata からも消すと 0.5.37 以前より情報が減ってしまう。"""
        _, db = await _save(_base(tools_used=value))
        idx = _column_index(db.last_query, "tools_used")
        assert db.last_params[idx] is None
        assert _metadata(db.last_query, db.last_params)["tools_used"] == value

    async def test_top_level_value_overwrites_metadata_key(self):
        """0.5.37 以前は未知フィールドの代入で top-level 値が metadata 側を上書きしていた。

        退避を setdefault にすると衝突時に top-level の生値が失われ、後方互換にならない。
        """
        _, db = await _save(
            _base(tools_used=["read"], metadata={"tools_used": ["stale"]})
        )
        assert _metadata(db.last_query, db.last_params)["tools_used"] == ["read"]

    async def test_raw_value_is_never_compared(self):
        """生値は任意型でありうる。退避要否の判定に ==/!= を使うと相手の __eq__ が走り、

        numpy 配列のように「真偽が曖昧」な型では telemetry 保存ごと落ちる。
        判定が型ベースであることを、比較すると必ず例外になる型で固定する。
        (dict サブクラスなので json 化は通り、比較さえしなければ保存は成功する)
        """

        class ComparisonExplodes(dict):
            __hash__ = None

            def __eq__(self, other):
                raise AssertionError("生値を比較してはいけない")

        value = ComparisonExplodes(read=1)
        result, db = await _save(_base(tools_used=value))
        assert result["success"] is True
        assert db.last_params[_column_index(db.last_query, "tools_used")] is None
        assert _metadata(db.last_query, db.last_params)["tools_used"] == {"read": 1}


class TestListTelemetrySelectsColumn:
    async def test_list_telemetry_selects_tools_used(self):
        db = FakeDB()
        await TelemetryAccess(db).list_telemetry(limit=1)
        assert "tools_used" in db.last_query
