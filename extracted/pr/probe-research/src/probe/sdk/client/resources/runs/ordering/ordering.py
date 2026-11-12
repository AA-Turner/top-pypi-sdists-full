"""Local sort for `iter_runs(order=...)`. The server answers a non-default `order=` as one top-N page with no cursor
(a cursor over a moving value would skip or repeat runs), so a sorted walk of EVERY run reads newest first and sorts
here, by the server's rules: runs without a value last either way, `id` breaks ties (twin: app/runs/listing/ordering.py)."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

#: Newest first: the only order the server pages, and the walk every other order sorts.
DEFAULT_ORDER = "-created_at"


class OrderField(str, Enum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    NAME = "name"
    CONFIG = "config"
    METRIC = "metric"


@dataclass(frozen=True)
class RunOrder:
    """A parsed `order=`: the field (with its config path or metric key) and its direction."""

    field: OrderField
    is_descending: bool
    path: tuple[str, ...] = ()

    @property
    def metric_key(self) -> str | None:
        return self.path[0] if self.field is OrderField.METRIC else None


def parse_run_order(text: str) -> RunOrder:
    """`created_at`, `updated_at`, `name`, `config.<path>` or `metric.<key>`; a leading `-` sorts descending."""
    is_descending = text.startswith("-")
    name = text[1:] if is_descending else text
    head, dot, rest = name.partition(".")
    if dot and head in (OrderField.CONFIG.value, OrderField.METRIC.value) and rest:
        field = OrderField(head)
        path = tuple(rest.split(".")) if field is OrderField.CONFIG else (rest,)
        if all(path):
            return RunOrder(field, is_descending, path)
    elif not dot and name in (OrderField.CREATED_AT.value, OrderField.UPDATED_AT.value, OrderField.NAME.value):
        return RunOrder(OrderField(name), is_descending)
    raise ValueError(
        f"order: {text!r} is not an order; use created_at, updated_at, name, config.<path> or metric.<key>, "
        "with a leading - for descending"
    )


_ABSENT = object()


def sort_runs(rows: Iterable[dict], order: RunOrder) -> list[dict]:
    """`rows` in `order`, as the server would sort them: valued rows by (value, id), then rows without one by id,
    both in the order's direction."""
    valued: list[tuple[Any, dict]] = []
    absent: list[dict] = []
    for row in rows:
        value = _get_sort_value(row, order)
        if value is _ABSENT:
            absent.append(row)
        else:
            valued.append((value, row))
    valued.sort(key=lambda pair: (pair[0], _get_id_key(pair[1])), reverse=order.is_descending)
    absent.sort(key=_get_id_key, reverse=order.is_descending)
    return [row for _, row in valued] + absent


def _get_id_key(row: dict) -> str:
    # A uuid's canonical lowercase text sorts as Postgres sorts the uuid.
    return str(row.get("id") or "").lower()


def _get_sort_value(row: dict, order: RunOrder) -> Any:
    match order.field:
        case OrderField.CREATED_AT | OrderField.UPDATED_AT:
            return _to_time(row.get(order.field.value))
        case OrderField.NAME:
            name = row.get("name")
            return _ABSENT if name is None else str(name)
        case OrderField.CONFIG:
            return _get_config_value(row.get("config"), order.path)
        case OrderField.METRIC:
            # A retention-locked run's `latest_metrics` is null: no value, as the server ranks it.
            final = (row.get("latest_metrics") or {}).get(order.path[0]) or {}
            last = final.get("last") if isinstance(final, dict) else None
            return _ABSENT if last is None else float(last)
    return _ABSENT


def _to_time(value: Any) -> Any:
    if not value:
        return _ABSENT
    if isinstance(value, datetime):
        return value
    text = str(value)
    # Python 3.10's fromisoformat does not read a trailing `Z`.
    return datetime.fromisoformat(text[:-1] + "+00:00" if text.endswith("Z") else text)


#: jsonb's order across types (Postgres: Object > Array > Boolean > Number > String > Null).
_JSON_NULL, _JSON_STRING, _JSON_NUMBER, _JSON_BOOLEAN, _JSON_ARRAY, _JSON_OBJECT = range(6)


def _get_config_value(config: Any, path: tuple[str, ...]) -> Any:
    """`config #> path` as a sortable key: absent when the path is missing (SQL NULL), else its jsonb order key."""
    value = config
    for segment in path:
        if isinstance(value, dict) and segment in value:
            value = value[segment]
        elif isinstance(value, list) and segment.lstrip("-").isdigit() and -len(value) <= int(segment) < len(value):
            value = value[int(segment)]
        else:
            return _ABSENT
    return _get_jsonb_key(value)


def _get_jsonb_key(value: Any) -> tuple:
    """A key that sorts JSON values as Postgres sorts jsonb: by type, then an array by its length and then element by
    element, an object by its pair count and then pair by pair with keys in jsonb's storage order (shorter key
    first, then bytewise), so `{"aa": 1, "c": 1}` sorts after `{"b": 1, "d": 1}`."""
    if value is None:
        return (_JSON_NULL,)
    if isinstance(value, bool):
        return (_JSON_BOOLEAN, value)
    if isinstance(value, (int, float)):
        return (_JSON_NUMBER, value)
    if isinstance(value, str):
        return (_JSON_STRING, value)
    if isinstance(value, list):
        return (_JSON_ARRAY, len(value), tuple(_get_jsonb_key(item) for item in value))
    if isinstance(value, dict):
        keys = sorted(value, key=lambda key: (len(key.encode()), key.encode()))
        pairs = tuple(part for key in keys for part in ((_JSON_STRING, key), _get_jsonb_key(value[key])))
        return (_JSON_OBJECT, len(value), pairs)
    return (_JSON_STRING, str(value))
