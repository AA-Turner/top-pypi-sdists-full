#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Hive partition pruning at file-listing time (SNOW-3295586 / GAP-018).

When a ``Filter(Read(...))`` plan carries static equality / IN predicates on
leading Hive partition columns, narrow stage paths before ``LIST`` / COPY so
Snowflake scans fewer partition directories.
"""
from __future__ import annotations

import itertools
from contextvars import ContextVar, Token
from dataclasses import dataclass

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto

from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted

# Maximum cartesian product of partition literal combinations; beyond this we
# decline pruning and fall back to a full scan.
_MAX_PRUNED_PATHS = 64

_hive_partition_pruning_hint: ContextVar[HivePartitionPruningHint | None] = ContextVar(
    "hive_partition_pruning_hint", default=None
)

PartitionPredicates = dict[str, set[str]]


@dataclass(frozen=True)
class HivePartitionPruningHint:
    """Thread-local hint consumed by :func:`map_read._read_file`."""

    pruned_clean_source_paths: tuple[str, ...]


def get_hive_partition_pruning_hint() -> HivePartitionPruningHint | None:
    return _hive_partition_pruning_hint.get()


def set_hive_partition_pruning_hint(
    hint: HivePartitionPruningHint,
) -> Token[HivePartitionPruningHint | None]:
    return _hive_partition_pruning_hint.set(hint)


def reset_hive_partition_pruning_hint(
    token: Token[HivePartitionPruningHint | None],
) -> None:
    _hive_partition_pruning_hint.reset(token)


def should_skip_read_cache_for_pruning() -> bool:
    return get_hive_partition_pruning_hint() is not None


def _column_name_from_expr(expr: expressions_proto.Expression) -> str | None:
    attr = expr.unresolved_attribute
    if not attr.unparsed_identifier:
        return None
    return unquote_if_quoted(attr.unparsed_identifier)


def _literal_to_partition_string(expr: expressions_proto.Expression) -> str | None:
    if not expr.HasField("literal"):
        return None
    lit = expr.literal
    lit_type = lit.WhichOneof("literal_type")
    if lit_type == "string":
        return lit.string
    if lit_type == "integer":
        return str(lit.integer)
    if lit_type == "long":
        return str(lit.long)
    if lit_type == "double":
        value = lit.double
        try:
            if value == int(value):
                return str(int(value))
        except (OverflowError, ValueError):
            pass
        return str(value)
    if lit_type == "boolean":
        return str(lit.boolean).lower()
    if lit_type == "decimal":
        return lit.decimal.value
    return None


def _merge_predicates(
    left: PartitionPredicates, right: PartitionPredicates
) -> PartitionPredicates | None:
    merged: PartitionPredicates = {}
    keys = set(left) | set(right)
    for key in keys:
        if key in left and key in right:
            intersection = left[key] & right[key]
            if not intersection:
                return None
            merged[key] = intersection
        elif key in left:
            merged[key] = set(left[key])
        else:
            merged[key] = set(right[key])
    return merged


def _parse_leaf_predicates(
    expr: expressions_proto.Expression,
) -> PartitionPredicates | None:
    if expr.HasField("unresolved_function"):
        func = expr.unresolved_function
        name = func.function_name.lower()
        args = list(func.arguments)
        if name == "==" and len(args) == 2:
            col_name = _column_name_from_expr(args[0])
            value = _literal_to_partition_string(args[1])
            if col_name is None or value is None:
                return {}
            return {col_name: {value}}
        if name == "in" and len(args) >= 2:
            col_name = _column_name_from_expr(args[0])
            if col_name is None:
                return {}
            values: set[str] = set()
            for arg in args[1:]:
                value = _literal_to_partition_string(arg)
                if value is None:
                    return None
                values.add(value)
            if not values:
                return None
            return {col_name: values}
        return None
    return {}


def _parse_predicate_tree(
    expr: expressions_proto.Expression,
) -> PartitionPredicates | None:
    if expr.HasField("unresolved_function"):
        func = expr.unresolved_function
        name = func.function_name.lower()
        args = list(func.arguments)
        if name == "and" and len(args) == 2:
            left = _parse_predicate_tree(args[0])
            right = _parse_predicate_tree(args[1])
            if left is None or right is None:
                return None
            return _merge_predicates(left, right)
    return _parse_leaf_predicates(expr)


def _lookup_parsed_predicate(
    parsed: PartitionPredicates,
    partition_col: str,
    case_sensitive: bool,
) -> set[str] | None:
    if case_sensitive:
        return parsed.get(partition_col)
    fold = partition_col.lower()
    for key, values in parsed.items():
        if key.lower() == fold:
            return values
    return None


def extract_leading_partition_predicates(
    condition: expressions_proto.Expression,
    partition_columns: list[str],
    case_sensitive: bool = True,
) -> PartitionPredicates | None:
    """Return static predicates on a leading prefix of ``partition_columns``.

    Returns ``None`` when no leading partition column is constrained or when
    the expression shape is unsupported (OR, ranges, non-literals, etc.).

    When ``case_sensitive`` is False, predicate column names are matched
    case-insensitively but returned keys use the discovered partition column
    names so path building uses the on-disk Hive directory spelling.
    """
    if not partition_columns:
        return None
    parsed = _parse_predicate_tree(condition)
    if parsed is None:
        return None

    leading: PartitionPredicates = {}
    for col in partition_columns:
        values = _lookup_parsed_predicate(parsed, col, case_sensitive)
        if values is None:
            break
        leading[col] = values
    return leading or None


def _append_hive_partition_suffix(
    base_path: str, segments: list[tuple[str, str]]
) -> str:
    suffix = "".join(f"{col}={value}/" for col, value in segments)
    if base_path.endswith("/"):
        return f"{base_path}{suffix}"
    return f"{base_path}/{suffix}"


def build_pruned_clean_source_paths(
    base_paths: list[str],
    partition_columns: list[str],
    predicates: PartitionPredicates,
) -> list[str]:
    """Expand ``base_paths`` with leading Hive partition directory segments."""
    constrained: list[str] = []
    for col in partition_columns:
        if col not in predicates:
            break
        constrained.append(col)
    if not constrained:
        return list(base_paths)

    value_lists = [sorted(predicates[col]) for col in constrained]
    combinations = list(itertools.product(*value_lists))
    if len(combinations) * len(base_paths) > _MAX_PRUNED_PATHS:
        return list(base_paths)

    pruned: list[str] = []
    for base in base_paths:
        for combo in combinations:
            segments = list(zip(constrained, combo, strict=True))
            pruned.append(_append_hive_partition_suffix(base, segments))
    return pruned
