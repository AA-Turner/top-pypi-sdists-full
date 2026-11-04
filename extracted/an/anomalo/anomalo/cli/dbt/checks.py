from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List, Tuple

from ..state.models import Check


CHECK_REF_PREFIX = "dbt__"
# Anomalo's custom SQL check drops these shared params on save, so sending them would
# show as a change on every apply. dbt's compiled SQL already applies the test's `where`.
CUSTOM_ZERO_UNSUPPORTED_PARAMS = (
    "custom_where_sql",
    "pass_on_no_data_error",
    "time_when_lag_intervals",
)
DEFAULT_FAIL_CALC = "count(*)"
DEFAULT_FAILURE_CONDITIONS = frozenset({"!=0", "<>0", ">0"})
MAX_REF_LENGTH = 200
MAX_TITLE_LENGTH = 250
SEVERITY_TO_PRIORITY = {"error": "high", "warn": "low"}
# dbt writes a source test's `model` argument as
# "{{ get_where_subquery(source('<source>', '<table>')) }}".
SOURCE_CALL = re.compile(
    r"""\bsource\(\s*['"]([^'"]+)['"]\s*,\s*['"]([^'"]+)['"]\s*\)"""
)


def _ref_prefix(test: Dict[str, Any]) -> str:
    """The ref namespace for the dbt project that defined the test.

    Two projects can monitor the same table, so the project is part of each ref.
    Without it their checks would share a ref and overwrite each other.
    """
    return f"{CHECK_REF_PREFIX}{test['package_name']}__"


def dbt_test_kind(test: Dict[str, Any]) -> str:
    """`unique`, `dbt_utils.accepted_range`, ..., or the test's own name for a singular test."""
    metadata = test.get("test_metadata") or {}
    if not metadata:
        return test["name"]
    return ".".join(
        part for part in (metadata.get("namespace"), metadata["name"]) if part
    )


def dbt_test_columns(test: Dict[str, Any]) -> List[str]:
    kwargs = (test.get("test_metadata") or {}).get("kwargs") or {}
    if test.get("column_name"):
        return [test["column_name"]]
    if kwargs.get("combination_of_columns"):
        return list(kwargs["combination_of_columns"])
    if kwargs.get("field"):
        return [kwargs["field"]]
    return []


def stable_ref(test: Dict[str, Any], override: str | None) -> str:
    """A check ref that survives edits to a test's arguments.

    dbt names generic tests from their arguments, so adding a value to an
    `accepted_values` list renames the test. Keying on the test type and columns
    keeps the Anomalo check, and its history, through that edit. An explicit
    `anomalo_ref`, a custom dbt test name, or a singular test keeps its own name.
    """
    if override:
        return _bounded_ref(f"{_ref_prefix(test)}{override}", test)
    if not test.get("test_metadata") or has_custom_name(test):
        return name_ref(test)
    parts = [dbt_test_kind(test).replace(".", "_"), *dbt_test_columns(test)]
    return _bounded_ref(_ref_prefix(test) + "__".join(parts), test)


def name_ref(test: Dict[str, Any]) -> str:
    return _bounded_ref(f"{_ref_prefix(test)}{test['name']}", test)


def declaring_source_id(test: Dict[str, Any]) -> str | None:
    """The unique id of the source a generic test is declared on, if it is on one.

    dbt sets no `attached_node` on a test of a source, so the `model` argument is
    what names the table the test is declared on.
    """
    kwargs = (test.get("test_metadata") or {}).get("kwargs") or {}
    match = SOURCE_CALL.search(str(kwargs.get("model") or ""))
    if match is None:
        return None
    source_name, table_name = match.groups()
    return f"source.{test.get('package_name')}.{source_name}.{table_name}"


def has_custom_name(test: Dict[str, Any]) -> bool:
    """Whether a generic test was given its own `name:` instead of dbt's generated one."""
    metadata = test.get("test_metadata") or {}
    generated = [metadata["name"]]
    if metadata.get("namespace"):
        generated.insert(0, f"{metadata['namespace']}_{metadata['name']}")
    prefixes = tuple(
        f"{source}{name}_" for name in generated for source in ("", "source_")
    )
    return not test["name"].startswith(prefixes)


def map_test(
    test: Dict[str, Any], relation_names: Dict[str, str]
) -> Tuple[str, Dict[str, Any]] | None:
    """The native Anomalo check type and its check-specific params, or None."""
    metadata = test.get("test_metadata") or {}
    kind = dbt_test_kind(test) if metadata else None
    kwargs = metadata.get("kwargs") or {}
    column = test.get("column_name") or kwargs.get("column_name")
    if kind == "unique" and column:
        return "ColumnUnique", {"column": column}
    if kind == "not_null" and column:
        return "ColumnNeverNull", {"column": column}
    if kind == "accepted_values" and column:
        return "ColumnDistinctInSet", _value_set(column, kwargs)
    if kind == "dbt_utils.not_accepted_values" and column:
        return "ColumnDistinctNotInSet", _value_set(column, kwargs)
    if kind in ("relationships", "dbt_utils.relationships_where") and column:
        return _relationship(test, column, kwargs, relation_names)
    if kind == "dbt_utils.accepted_range" and column:
        return _accepted_range(column, kwargs)
    if kind == "dbt_utils.not_empty_string" and column:
        if kwargs.get("trim_whitespace", True):
            statement = f"{column} is null or trim({column}) != ''"
            return "CustomAlways", {"custom_sql_statement": statement}
        return "ColumnNeverEmptyString", {"column": column}
    if kind == "dbt_utils.unique_combination_of_columns":
        return _unique_combination(kwargs)
    # `dbt_utils.expression_is_true` and `dbt_utils.recency` have no native check that
    # keeps dbt's rules. CustomAlways fails a row the expression evaluates to NULL on,
    # which dbt's `where not(...)` excludes, and TimeColumnNearNowSome rejects a
    # timestamp dbt's recency accepts, such as a future one. dbt's compiled SQL runs.
    return None


def non_default_threshold(test: Dict[str, Any]) -> Tuple[str, str] | None:
    """(fail_calc, condition) when the test doesn't simply fail on any returned row."""
    config = test.get("config") or {}
    fail_calc = config.get("fail_calc") or DEFAULT_FAIL_CALC
    is_warn = str(config.get("severity", "error")).lower() == "warn"
    condition = config.get("warn_if" if is_warn else "error_if") or "!= 0"
    if (
        _squash(fail_calc) == DEFAULT_FAIL_CALC
        and _squash(condition) in DEFAULT_FAILURE_CONDITIONS
    ):
        return None
    return fail_calc, condition


def compiled_sql_check(test: Dict[str, Any]) -> Tuple[str, Dict[str, Any]] | None:
    """dbt's own test SQL as a "Custom SQL returns no rows" check.

    A dbt data test passes exactly when its compiled SQL returns no rows, which is
    what CustomZero checks, and the test's `where` is already applied inside it.
    """
    code = (test.get("compiled_code") or "").strip().rstrip(";").strip()
    if not code:
        return None
    threshold = non_default_threshold(test)
    if threshold:
        fail_calc, condition = threshold
        code = (
            f"select * from (\n  select {fail_calc} as failures from (\n{code}\n"
            f"  ) as dbt_test\n) as dbt_test_result\nwhere failures {condition}"
        )
    message = " ".join((test.get("description") or "").split()) or test["name"]
    return "CustomZero", {"custom_message": message, "custom_sql": code}


def build_check(
    test: Dict[str, Any],
    check_type: str,
    specific: Dict[str, Any],
    *,
    owner_label: str,
    priority: str | None,
    is_time_based: bool,
) -> Check:
    params = {
        **specific,
        "alert_default_notif_channel": True,
        "custom_check_title": _title(test),
        "custom_where_sql": _where(test, check_type, specific),
        # dbt tests pass on an empty table.
        "pass_on_no_data_error": True,
        "priority_level": priority or _severity_priority(test),
        "time_based": is_time_based,
        "time_when_lag_intervals": 0,
    }
    if check_type == "CustomZero":
        params = {
            key: value
            for key, value in params.items()
            if key not in CUSTOM_ZERO_UNSUPPORTED_PARAMS
        }
    return Check(check_type=check_type, params=params, labels=[owner_label])


def _bounded_ref(ref: str, test: Dict[str, Any]) -> str:
    if len(ref) <= MAX_REF_LENGTH:
        return ref
    digest = hashlib.sha1(test["unique_id"].encode()).hexdigest()[:10]
    return f"{ref[: MAX_REF_LENGTH - 11]}_{digest}"


def _value_set(column: str, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "case_sensitive": True,
        "column": column,
        "expected_set": list(kwargs.get("values") or []),
    }


def _relationship(
    test: Dict[str, Any],
    column: str,
    kwargs: Dict[str, Any],
    relation_names: Dict[str, str],
) -> Tuple[str, Dict[str, Any]] | None:
    # The parent is whichever dependency isn't the table the test is declared on.
    # dbt gives no attached_node to a test of a source, so read that from `model`.
    child_id = test.get("attached_node") or declaring_source_id(test)
    parents = [
        relation_names[node_id]
        for node_id in (test.get("depends_on") or {}).get("nodes") or []
        if node_id != child_id and node_id in relation_names
    ]
    if not parents:
        return None
    params: Dict[str, Any] = {
        "column": column,
        "column_right": kwargs.get("field") or column,
        "table_right": parents[0],
    }
    to_condition = str(kwargs.get("to_condition") or "1=1").strip()
    if _squash(to_condition) != "1=1":
        params["custom_where_sql_right"] = to_condition
    return "JoinLeftAtLeastOne", params


def _accepted_range(
    column: str, kwargs: Dict[str, Any]
) -> Tuple[str, Dict[str, Any]] | None:
    low, high = kwargs.get("min_value"), kwargs.get("max_value")
    if low is None and high is None:
        return None
    is_inclusive = kwargs.get("inclusive", True)
    if is_inclusive and all(
        value is None or _is_number(value) for value in (low, high)
    ):
        params: Dict[str, Any] = {"column": column}
        if low is not None:
            params["low"] = low
        if high is not None:
            params["high"] = high
        return "ColumnRange", params
    lower_op, upper_op = (">=", "<=") if is_inclusive else (">", "<")
    bounds = []
    if low is not None:
        bounds.append(f"{column} {lower_op} {low}")
    if high is not None:
        bounds.append(f"{column} {upper_op} {high}")
    statement = f"{column} is null or ({' and '.join(bounds)})"
    return "CustomAlways", {"custom_sql_statement": statement}


def _unique_combination(kwargs: Dict[str, Any]) -> Tuple[str, Dict[str, Any]] | None:
    columns = list(kwargs.get("combination_of_columns") or [])
    if not columns:
        return None
    params: Dict[str, Any] = {
        "column": columns[0],
        "null_treatment": "Include NULL values",
    }
    if len(columns) > 1:
        params["column_b"] = columns[1]
    if len(columns) > 2:
        params["column_c"] = columns[2]
    if len(columns) > 3:
        params["list_of_columns"] = columns[3:]
    return "MultiColumnUnique", params


def _where(
    test: Dict[str, Any], check_type: str, specific: Dict[str, Any]
) -> str | None:
    where = (test.get("config") or {}).get("where")
    if check_type != "JoinLeftAtLeastOne":
        return where or None
    # dbt's relationships tests skip rows whose child column is null.
    kwargs = (test.get("test_metadata") or {}).get("kwargs") or {}
    from_condition = str(kwargs.get("from_condition") or "1=1").strip()
    conditions = [where] if where else []
    if _squash(from_condition) != "1=1":
        conditions.append(from_condition)
    conditions.append(f"{specific['column']} is not null")
    if len(conditions) == 1:
        return conditions[0]
    return " and ".join(f"({condition})" for condition in conditions)


def _title(test: Dict[str, Any]) -> str:
    columns = ", ".join(dbt_test_columns(test))
    title = (
        f"dbt: {dbt_test_kind(test)}({columns})"
        if columns
        else f"dbt: {dbt_test_kind(test)}"
    )
    description = " ".join((test.get("description") or "").split())
    if description:
        title = f"{title}: {description.split('. ')[0].rstrip('.')}"
    if len(title) <= MAX_TITLE_LENGTH:
        return title
    return f"{title[: MAX_TITLE_LENGTH - 1]}…"


def _severity_priority(test: Dict[str, Any]) -> str:
    severity = str((test.get("config") or {}).get("severity", "error")).lower()
    return SEVERITY_TO_PRIORITY.get(severity, "normal")


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _squash(sql: Any) -> str:
    return "".join(str(sql).split()).lower()
