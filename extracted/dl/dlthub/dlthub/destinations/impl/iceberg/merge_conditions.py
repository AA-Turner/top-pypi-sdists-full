import string
from datetime import date, datetime, time
from typing import Any, Dict, List, Optional, cast

from pyiceberg.expressions import (
    AlwaysFalse,
    AlwaysTrue,
    And,
    BooleanExpression,
    BoundPredicate,
    EqualTo,
    In,
    LiteralPredicate,
    Not,
    NotEqualTo,
    NotIn,
    Or,
    SetPredicate,
    UnboundPredicate,
)
from pyiceberg.expressions.parser import parse
from pyiceberg.expressions.visitors import BooleanExpressionVisitor, visit

from dlt.common import Decimal
from dlt.common.destination.capabilities import DestinationCapabilitiesContext
from dlt.common.destination.utils import expand_merge_condition, get_merge_placeholder_values
from dlt.common.exceptions import TerminalValueError

# an empty list placeholder renders as this single item, see `_EmptyListRewriter`
_EMPTY_LIST_SENTINEL = "__dlt_empty_list_placeholder__"


def escape_pyiceberg_literal(v: Any) -> str:
    """Escapes `v` as a literal of the pyiceberg row filter syntax. Dates and timestamps are ISO
    strings that pyiceberg binds to the column type."""
    if isinstance(v, str):
        return "'" + v.replace("'", "''") + "'"
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, (datetime, date, time)):
        return "'" + v.isoformat() + "'"
    if isinstance(v, (int, float, Decimal)):
        return str(v)
    raise TerminalValueError(
        f"Value `{v!r}` of type `{type(v).__name__}` cannot be used in an iceberg row filter."
        " Use a string, number, bool, date or datetime."
    )


def render_destination_scope(
    root_table_name: str,
    destination_scope: str,
    caps: DestinationCapabilitiesContext,
) -> BooleanExpression:
    """Returns `destination_scope` as a pyiceberg row filter. `{table}.` is removed, so it names
    the columns of the destination table, and value placeholders are filled from the load package.

    Raises:
        ValueError: If the condition uses an unknown placeholder, `{table}` without a column or
            is not a valid pyiceberg row filter.
    """
    values: Dict[str, Any] = {
        name: [_EMPTY_LIST_SENTINEL] if isinstance(value, (list, tuple)) and not value else value
        for name, value in get_merge_placeholder_values(root_table_name).items()
    }
    expanded = expand_merge_condition(
        "destination_scope",
        _remove_table_qualifier(destination_scope),
        {},
        values,
        escape_pyiceberg_literal,
        caps.supports_tz_aware_datetime,
        caps.timestamp_precision,
    )
    try:
        expression = parse(expanded)
    except Exception as parse_ex:
        raise ValueError(
            f"`destination_scope` `{expanded}` is not a valid iceberg row filter: {parse_ex}."
            " The iceberg destination accepts comparisons, `IN`, `IS NULL`, `LIKE 'prefix%'`,"
            " `AND`, `OR` and `NOT` on columns of the table, and no subqueries or functions."
        ) from parse_ex
    return visit(expression, _EmptyListRewriter())


def render_source_filter(
    root_table_name: str,
    source_filter: str,
    staging_relation: str,
    caps: DestinationCapabilitiesContext,
) -> str:
    """Returns `source_filter` as a duckdb condition on `staging_relation`, the loaded rows.
    Value placeholders are filled from the load package as duckdb literals."""
    return expand_merge_condition(
        "source_filter",
        source_filter,
        {"staging_table": staging_relation},
        get_merge_placeholder_values(root_table_name),
        caps.escape_literal,
        caps.supports_tz_aware_datetime,
        caps.timestamp_precision,
    )


def _remove_table_qualifier(condition: str) -> str:
    """Removes `{table}.` from `condition` and keeps the other placeholders and escaped braces."""
    parts: List[str] = []
    strip_dot = False
    for literal_text, field_name, format_spec, conversion in string.Formatter().parse(condition):
        if strip_dot:
            if not literal_text.startswith("."):
                raise ValueError(
                    "`destination_scope` uses `{table}` without a column. Write `{table}.column`"
                    " or the bare column name."
                )
            literal_text = literal_text[1:]
            strip_dot = False
        parts.append(literal_text.replace("{", "{{").replace("}", "}}"))
        if field_name is None:
            continue
        if field_name == "table":
            strip_dot = True
            continue
        conversion_text = f"!{conversion}" if conversion else ""
        spec_text = f":{format_spec}" if format_spec else ""
        parts.append("{" + field_name + conversion_text + spec_text + "}")
    if strip_dot:
        raise ValueError(
            "`destination_scope` uses `{table}` without a column. Write `{table}.column`"
            " or the bare column name."
        )
    return "".join(parts)


class _EmptyListRewriter(BooleanExpressionVisitor[BooleanExpression]):
    """Replaces predicates on an empty list placeholder: `IN` matches no row, `NOT IN` every row,
    same as `IN (NULL)` on SQL destinations."""

    def visit_true(self) -> BooleanExpression:
        return AlwaysTrue()

    def visit_false(self) -> BooleanExpression:
        return AlwaysFalse()

    def visit_not(self, child_result: BooleanExpression) -> BooleanExpression:
        return Not(child_result)

    def visit_and(
        self, left_result: BooleanExpression, right_result: BooleanExpression
    ) -> BooleanExpression:
        return And(left_result, right_result)

    def visit_or(
        self, left_result: BooleanExpression, right_result: BooleanExpression
    ) -> BooleanExpression:
        return Or(left_result, right_result)

    def visit_unbound_predicate(self, predicate: "UnboundPredicate[Any]") -> BooleanExpression:
        literals: Optional[List[Any]] = None
        if isinstance(predicate, SetPredicate):
            literals = [lit.value for lit in predicate.literals]
        elif isinstance(predicate, LiteralPredicate):
            literals = [predicate.literal.value]
        if literals != [_EMPTY_LIST_SENTINEL]:
            return predicate
        # a one item `IN` list parses to `EqualTo`
        if isinstance(predicate, (In, EqualTo)):
            return AlwaysFalse()
        if isinstance(predicate, (NotIn, NotEqualTo)):
            return AlwaysTrue()
        return predicate

    def visit_bound_predicate(self, predicate: "BoundPredicate[Any]") -> BooleanExpression:
        return cast(BooleanExpression, predicate)
