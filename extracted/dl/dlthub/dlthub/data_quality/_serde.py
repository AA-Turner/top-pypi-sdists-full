from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TYPE_CHECKING

from dlt.common.json import json
from dlt.common.typing import TypedDict

import sqlglot.serde
from dlt.common.exceptions import ValueErrorWithKnownValues

import dlthub.data_quality as dq
from dlthub.data_quality.checks._base import LazyCheck


if TYPE_CHECKING:
    from sqlglot.serde import Node


class TInlineDataQualityCheck(TypedDict):
    name: str
    arguments: Mapping[str, Any]


class TDataQualityCheck(TInlineDataQualityCheck):
    table_name: str


def check_from_dict(check_dict: TInlineDataQualityCheck) -> LazyCheck:
    if check_dict["name"] not in dq.checks.__all__:
        raise ValueErrorWithKnownValues("check['name']", check_dict["name"], dq.checks.__all__)

    check_class: type = getattr(dq.checks, check_dict["name"])
    check: LazyCheck = check_class(**check_dict["arguments"])
    return check


def check_to_dict(check: LazyCheck) -> TInlineDataQualityCheck:
    return TInlineDataQualityCheck(name=check.name, arguments=check.arguments)


def serialize_check_expr(check: LazyCheck) -> str:
    return json.dumps(sqlglot.serde.dump(check.expr))


def deserialize_check_expr(serialized_check_expr: str) -> Node:
    return sqlglot.serde.load(json.loads(serialized_check_expr))
