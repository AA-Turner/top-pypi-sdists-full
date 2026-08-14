#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Translate Iceberg WAP **branch** DML targets to Snowflake SQL.

Spark/Iceberg writes to a branch ref by appending a ``branch_<name>`` suffix
to the table identifier (same rule as reads)::

    INSERT INTO db.t.branch_audit VALUES (1);
    MERGE INTO db.t.branch_audit target USING src ...
    UPDATE db.t.branch_audit SET ...
    DELETE FROM db.t.branch_audit WHERE ...

Snowflake WAP **branch** DML uses ``ON (BRANCH => '<name>')`` on the base table
(reads use ``AT (BRANCH => ...)`` — see ``docs/iceberg-wap-branch-read.md``)::

    INSERT INTO db.t ON (BRANCH => 'audit') SELECT ...
    MERGE INTO db.t ON (BRANCH => 'audit') AS t USING src ...
    UPDATE db.t ON (BRANCH => 'audit') SET ...
    DELETE FROM db.t ON (BRANCH => 'audit') WHERE ...

``tag_<name>`` suffixes are supported for **reads** only
(``AT (VERSION_TAG => ...)``). Snowflake does not expose ``ON (VERSION_TAG => ...)``
for DML; SCOS rejects tag-suffix writes with ``UNSUPPORTED_OPERATION``.

DataFrame API paths (``df.write.insertInto("t.branch_x")``,
``df.writeTo("t.branch_x").append()``) use the same resolution before
Snowpark write/merge/update/delete calls.

Snowpark-python note
--------------------
Table ``merge`` / ``update`` / ``delete`` embed ``self.table_name`` in generated
SQL and do not propagate ``time_travel_config.branch`` for writes today. SCOS
opens the base table for schema metadata and **patches`` ``Table.table_name`` to
the ``ON (BRANCH => ...)`` form before invoking Snowpark DML. A first-class
Snowpark write-side ``branch`` parameter would be cleaner long term.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal, NoReturn

from pyspark.errors.exceptions.base import AnalysisException

from snowflake import snowpark
from snowflake.snowpark_connect.config import is_iceberg_sql_extensions_enabled
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.map_sql_expression import as_java_list
from snowflake.snowpark_connect.relation.iceberg_sql_branch_tag_suffix import (
    iceberg_branch_tag_suffix_extensions_disabled_exception,
    try_parse_iceberg_branch_tag_suffix,
    try_parse_iceberg_branch_tag_suffix_parts,
)


def _quote_branch_name_sql(branch_name: str) -> str:
    escaped = branch_name.replace("'", "''")
    return f"'{escaped}'"


def snowflake_branch_dml_table_sql(base_table_sql: str, *, branch: str) -> str:
    """Append ``ON (BRANCH => '<name>')`` for Snowflake Iceberg branch DML."""
    return f"{base_table_sql} ON (BRANCH => {_quote_branch_name_sql(branch)})"


def _raise_tag_dml_not_supported(spark_table_name: str, tag_name: str) -> NoReturn:
    """Snowflake WAP DML is branch-only; tag refs are read-only via AT (VERSION_TAG)."""
    exception = AnalysisException(
        f"Iceberg version-tag DML target {spark_table_name!r} is not supported. "
        "Snowflake WAP writes use ON (BRANCH => '<name>') on INSERT/UPDATE/DELETE/"
        "MERGE; version tags support AT (VERSION_TAG => ...) reads only. Use a "
        f"branch suffix instead (e.g. ...branch_{tag_name})."
    )
    attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
    raise exception


@dataclass(frozen=True)
class IcebergRefDmlTarget:
    """Resolved Spark table identifier and Snowflake DML table references."""

    spark_table_name: str
    base_snowflake_sql: str
    dml_snowflake_sql: str
    ref_kind: Literal["branch"] | None = None
    ref_name: str | None = None

    @property
    def has_ref(self) -> bool:
        return self.ref_kind is not None


def resolve_iceberg_ref_dml_target(
    spark_table_name: str,
    spark_to_snowflake_fn: Callable[[str], str],
) -> IcebergRefDmlTarget:
    """Resolve ``table.branch_<name>`` DML targets; reject ``tag_<name>`` writes."""
    parsed = try_parse_iceberg_branch_tag_suffix(spark_table_name)
    if parsed is None:
        snowflake_sql = spark_to_snowflake_fn(spark_table_name)
        return IcebergRefDmlTarget(
            spark_table_name=spark_table_name,
            base_snowflake_sql=snowflake_sql,
            dml_snowflake_sql=snowflake_sql,
        )

    if not is_iceberg_sql_extensions_enabled():
        raise iceberg_branch_tag_suffix_extensions_disabled_exception()

    base_spark, options = parsed
    base_sql = spark_to_snowflake_fn(base_spark)
    if "branch" in options:
        branch = options["branch"]
        return IcebergRefDmlTarget(
            spark_table_name=spark_table_name,
            base_snowflake_sql=base_sql,
            dml_snowflake_sql=snowflake_branch_dml_table_sql(base_sql, branch=branch),
            ref_kind="branch",
            ref_name=branch,
        )
    _raise_tag_dml_not_supported(spark_table_name, options["tag"])


def resolve_iceberg_ref_dml_target_from_parts(
    parts: list[str],
    *,
    spark_table_name: str,
    parts_to_snowflake_fn: Callable[[list[str]], str],
) -> IcebergRefDmlTarget:
    """Resolve branch DML targets from Catalyst multipart name segments."""
    parsed = try_parse_iceberg_branch_tag_suffix_parts(parts)
    if parsed is None:
        snowflake_sql = parts_to_snowflake_fn(parts)
        return IcebergRefDmlTarget(
            spark_table_name=spark_table_name,
            base_snowflake_sql=snowflake_sql,
            dml_snowflake_sql=snowflake_sql,
        )

    if not is_iceberg_sql_extensions_enabled():
        raise iceberg_branch_tag_suffix_extensions_disabled_exception()

    base_parts, options = parsed
    base_sql = parts_to_snowflake_fn(base_parts)
    if "branch" in options:
        branch = options["branch"]
        return IcebergRefDmlTarget(
            spark_table_name=spark_table_name,
            base_snowflake_sql=base_sql,
            dml_snowflake_sql=snowflake_branch_dml_table_sql(base_sql, branch=branch),
            ref_kind="branch",
            ref_name=branch,
        )
    _raise_tag_dml_not_supported(spark_table_name, options["tag"])


def relation_identifier_parts(name_obj: Any, *, is_multi_part: bool) -> list[str]:
    """Return Catalyst multipart identifier segments as plain strings."""
    if name_obj.getClass().getSimpleName() in (
        "PlanWithUnresolvedIdentifier",
        "ExpressionWithUnresolvedIdentifier",
    ):
        return [str(name_obj.name())]
    if is_multi_part:
        try:
            parts = name_obj.multipartIdentifier()
        except AttributeError:
            parts = name_obj.nameParts()
    else:
        parts = name_obj.nameParts()
    return [str(part) for part in as_java_list(parts)]


def spark_table_name_from_relation_identifier(
    name_obj: Any, *, is_multi_part: bool
) -> str:
    """Build a dot-separated Spark table name from a Catalyst identifier object."""
    return ".".join(relation_identifier_parts(name_obj, is_multi_part=is_multi_part))


def snowpark_table_for_ref_dml(
    session: snowpark.Session,
    target: IcebergRefDmlTarget,
) -> snowpark.Table:
    """Open the base table for schema metadata; patch the DML table name for SQL."""
    table = session.table(target.base_snowflake_sql)
    if target.has_ref:
        table.table_name = target.dml_snowflake_sql
    return table


def reject_ref_dml_table_creation(target: IcebergRefDmlTarget, operation: str) -> None:
    """Branch DML targets must write to an existing base table."""
    if not target.has_ref:
        return
    exception = AnalysisException(
        f"Cannot {operation} Iceberg table {target.spark_table_name!r}: "
        f"'branch_{target.ref_name}' is a branch ref suffix, "
        "not a creatable table name. Create the base table first, then write with "
        f"the branch suffix (e.g. INSERT INTO base.branch_{target.ref_name})."
    )
    attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
    raise exception
