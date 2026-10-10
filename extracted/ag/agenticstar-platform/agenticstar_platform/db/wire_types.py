"""DB proxy (cli-api ``/db/execute``) の wire で、params の文字列が date / datetime 由来かを伝える添字。

``_serialize_param`` は date / datetime を ``isoformat()`` の文字列にするので、wire の上では TEXT の
``"2026-10-09"`` と ``date(2026, 10, 9)`` が同じになる。3.0.14 までの cli-api は文字列の形だけで
date / datetime に戻していたため、TEXT 列に入れる ISO 形の文字列が date に変わり asyncpg が
``expected str, got date`` で拒否した（molt prop-20261009-004）。

3.0.15 から SDK は params と同じ並びの ``param_types`` を添える:

- 要素は ``"datetime"`` / ``"date"`` / ``None``
- list / dict は同じ形で入れ子にし、中に date / datetime が無ければ ``None`` に畳む

cli-api は添字があれば文字列の形を見ず、添字が言う型にだけ戻す。添字を知らない cli-api
（3.0.14 までと対になるもの）は未知のキーとして無視し、従来どおり推定する。
"""

from __future__ import annotations

import base64
from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

TYPE_DATETIME = "datetime"
TYPE_DATE = "date"


def serialize_param(value: Any) -> Any:
    """
    SQLパラメータをJSONシリアライズ可能な形式に変換 (3.0.14 まで api_manager._serialize_param。本体は同じ)

    Args:
        value: 変換する値

    Returns:
        JSONシリアライズ可能な値
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, bytes):
        # base64エンコーディングでバイナリデータを安全にシリアライズ
        return {"__bytes__": base64.b64encode(value).decode("ascii")}
    if isinstance(value, (list, tuple)):
        return [serialize_param(v) for v in value]
    if isinstance(value, dict):
        return {k: serialize_param(v) for k, v in value.items()}
    return value


def param_type_hint(value: Any) -> Any:
    """``serialize_param(value)`` と同じ形で、date / datetime の位置だけを示す添字を返す。"""
    if isinstance(value, datetime):  # datetime は date の subclass なので先に見る
        return TYPE_DATETIME
    if isinstance(value, date):
        return TYPE_DATE
    if isinstance(value, (list, tuple)):
        hints = [param_type_hint(v) for v in value]
        return hints if any(h is not None for h in hints) else None
    if isinstance(value, dict):
        hints = {k: param_type_hint(v) for k, v in value.items()}
        return hints if any(h is not None for h in hints.values()) else None
    return None
