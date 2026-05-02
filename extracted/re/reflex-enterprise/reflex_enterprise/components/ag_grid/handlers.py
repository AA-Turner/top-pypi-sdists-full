"""Handlers for the Reflex Enterprise AG Grid component."""

import datetime
from types import SimpleNamespace
from typing import Any, Type, TypeVar

import reflex as rx
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.roles import WhereHavingRole
from sqlmodel import and_, not_, or_, select
from sqlmodel.sql.expression import SelectOfScalar

M = TypeVar("M", bound=rx.Model)


def handle_text_filter(value: str, filter_def: dict[str, str]) -> bool:
    """Handle text filter."""
    type = filter_def.get("type", "contains")
    filter = filter_def.get("filter", "")
    match type:
        case "contains":
            return filter in value
        case "notContains":
            return filter not in value
        case "equals":
            return value == filter
        case "notEqual":
            return value != filter
        case "startsWith":
            return value.startswith(filter)
        case "endsWith":
            return value.endswith(filter)
        case "blank":
            return not value
        case "notBlank":
            return bool(value)
        case _:
            raise TypeError(f"type {type} does not exist")


def handle_number_filter(value: int, filter_def: dict) -> bool:
    """Handle number filter."""
    type = filter_def.get("type", "equals")
    filter = filter_def.get("filter")
    match type:
        case "equals":
            return value == filter
        case "notEqual":
            return value != filter
        case "greaterThan":
            return value > filter  # pyright: ignore [reportOperatorIssue]
        case "greaterThanOrEqual":
            return value >= filter  # pyright: ignore [reportOperatorIssue]
        case "lessThan":
            return value < filter  # pyright: ignore [reportOperatorIssue]
        case "lessThanOrEqual":
            return value <= filter  # pyright: ignore [reportOperatorIssue]
        case "inRange":
            return filter <= value <= filter_def.get("filterTo")  # pyright: ignore [reportOperatorIssue, reportOptionalOperand]
        case "blank":
            return not value
        case "notBlank":
            return bool(value)
        case _:
            raise TypeError(f"type {type} does not exist")


def handle_filter_def(value: Any, filter_def: dict) -> bool:
    """Handle filter definition."""
    if not filter_def:
        return True

    match filter_def.get("operator", "").lower():
        case "and":
            return all(
                handle_filter_def(value, sub_filter)
                for sub_filter in filter_def.get("conditions", [])
            )
        case "or":
            return any(
                handle_filter_def(value, sub_filter)
                for sub_filter in filter_def.get("conditions", [])
            )
        case _:
            pass

    match filter_def.get("filterType", "text"):
        case "text":
            return handle_text_filter(value, filter_def)
        case "number":
            return handle_number_filter(value, filter_def)
        case _:
            return False


def handle_filter_model(row: list, filter_model: dict) -> bool:
    """Handle filter model."""
    if not filter_model:
        return True
    field, filter_def = None, None
    try:
        for field, filter_def in filter_model.items():
            if not handle_filter_def(row[field], filter_def):
                return False
    except Exception as e:
        print(f"Error filtering {field} of {row}: {e}")  # noqa: T201
        return False
    return True


_sql_operations = {
    "and": and_,
    "or": or_,
}


def where_text_filter(
    value: InstrumentedAttribute, filter_def: dict[str, str]
) -> WhereHavingRole:
    """Where filter for text."""
    type = filter_def.get("type", "contains")
    filter = filter_def.get("filter", "")
    if type == "contains":
        return value.contains(filter)
    if type == "notContains":
        return not_(value.contains(filter))
    if type == "equals":
        return value == filter
    if type == "notEqual":
        return value != filter
    if type == "startsWith":
        return value.startswith(filter)
    if type == "endsWith":
        return value.endswith(filter)
    if type == "blank":
        return or_(value == None, value == "")  # noqa: E711
    if type == "notBlank":
        return and_(value != None, value != "")  # noqa: E711
    raise TypeError(f"type {type} does not exist")


def where_number_filter(
    value: InstrumentedAttribute, filter_def: dict[str, str | int | float]
) -> WhereHavingRole:
    """Where filter for numbers."""
    type = filter_def.get("type", "equals")
    to_filter = None
    if filter_def.get("filterType") == "date":
        filter = datetime.datetime.fromisoformat(filter_def.get("dateFrom"))  # pyright: ignore [reportArgumentType]
        if filter_def.get("dateTo"):
            to_filter = datetime.datetime.fromisoformat(filter_def.get("dateTo"))  # pyright: ignore [reportArgumentType]
    else:
        filter = filter_def.get("filter", 0)
        if filter_def.get("filterTo"):
            to_filter = filter_def.get("filterTo")
    if type == "equals":
        return value == filter
    if type == "notEqual":
        return value != filter
    if type == "greaterThan":
        return value > filter
    if type == "greaterThanOrEqual":
        return value >= filter
    if type == "lessThan":
        return value < filter
    if type == "lessThanOrEqual":
        return value <= filter
    if type == "inRange":
        return and_(
            value >= filter,
            value <= to_filter,
        )
    if type == "blank":
        return value == None  # noqa: E711
    if type == "notBlank":
        return value != None  # noqa: E711
    if type == "true":
        return value == True  # noqa: E712
    if type == "false":
        return value == False  # noqa: E712

    raise TypeError(f"type {type} does not exist")


def where_filter_def(
    value: InstrumentedAttribute, filter_def: dict[str, Any]
) -> WhereHavingRole | None:
    """Where filter definition."""
    if not filter_def:
        return
    operator = _sql_operations.get(
        filter_def.get("operator", "").lower(),
    )
    if operator:
        return operator(
            *(
                where_filter_def(value, sub_filter)
                for sub_filter in filter_def.get("conditions", [])
            )
        )
    filter_type = filter_def.get("filterType", "text")
    if filter_type == "text":
        return where_text_filter(value, filter_def)
    if filter_type in ("number", "date", "boolean"):
        return where_number_filter(value, filter_def)


def where_filter_outer_def(
    model: Type[M], filter_def: dict[str, Any]
) -> WhereHavingRole | None:
    """Where filter definition for supporting Advanced Filter model."""
    # Top-level advanced filter
    filter_type = filter_def.get("filterType", "text")
    if filter_type == "join":
        operator = _sql_operations.get(
            filter_def.get("type", "").lower(),
        )
        if operator:
            return operator(
                *(
                    where_filter_outer_def(model, sub_filter)
                    for sub_filter in filter_def.get("conditions", [])
                )
            )
    value = getattr(model, filter_def.get("colId"))  # pyright: ignore [reportArgumentType]
    if filter_type == "text":
        return where_text_filter(value, filter_def)
    if filter_type in ("number", "date", "boolean"):
        return where_number_filter(value, filter_def)


def apply_filter_model(
    model: Type[M], filter_model: dict[str, dict[str, Any]]
) -> SelectOfScalar[M]:
    """Apply filter model to a model."""
    query = select(model)
    if "filterType" in filter_model and "type" in filter_model:
        # Top-level advanced filter
        filter_applies = where_filter_outer_def(model, filter_model)
        if filter_applies is not None:
            return query.where(filter_applies)  # pyright: ignore [reportArgumentType]
    for field, filter_def in filter_model.items():
        filter_applies = where_filter_def(
            value=getattr(model, field),
            filter_def=filter_def,
        )
        if filter_applies is not None:
            query = query.where(filter_applies)  # pyright: ignore [reportArgumentType]
    return query


def apply_sort_model(
    model: Type[M], query: SelectOfScalar[M], sort_model: list[dict[str, str]]
) -> SelectOfScalar[M]:
    """Apply sort model to a query."""
    for sort_spec in sort_model:
        field = getattr(model, sort_spec["colId"], None)
        if field is None:
            continue
        query = query.order_by(
            field.desc() if sort_spec["sort"] == "desc" else field.asc()
        )
    return query


class HandlerNamespace(SimpleNamespace):
    """Namespace for handlers."""

    text_filter = handle_text_filter
