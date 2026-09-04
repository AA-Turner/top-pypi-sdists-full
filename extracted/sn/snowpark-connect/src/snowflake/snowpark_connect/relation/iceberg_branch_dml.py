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

Snowflake WAP **branch** DML uses ``AT (BRANCH => '<name>')`` on the base table
(same clause as branch reads — see ``docs/iceberg-wap-branch-read.md``)::

    INSERT INTO db.t AT (BRANCH => 'audit') SELECT ...
    MERGE INTO db.t AT (BRANCH => 'audit') AS t USING src ...
    UPDATE db.t AT (BRANCH => 'audit') SET ...
    DELETE FROM db.t AT (BRANCH => 'audit') WHERE ...

``tag_<name>`` suffixes are supported for **reads** only
(``AT (VERSION_TAG => ...)``). Snowflake does not expose ``ON (VERSION_TAG => ...)``
for DML; SCOS rejects tag-suffix writes with ``UNSUPPORTED_OPERATION``.

DataFrame API paths (``df.write.insertInto("t.branch_x")``,
``df.writeTo("t.branch_x").append()``) use the same resolution before
Snowpark write/merge/update/delete calls.

Session-level WAP (``spark.wap.branch`` / ``spark.conf.set("spark.wap.branch", ...)``)
redirects plain-table DML to ``AT (BRANCH => '<name>')`` without setting
``has_ref`` — table creation still targets the base table, matching native Spark
WAP semantics (branch commits apply only to existing tables).

Snowpark-python note
--------------------
Table ``merge`` / ``update`` / ``delete`` embed ``self.table_name`` in generated
SQL and do not propagate ``time_travel_config.branch`` for writes today. SCOS
opens the base table for schema metadata and **patches`` ``Table.table_name`` to
the ``AT (BRANCH => ...)`` form before invoking Snowpark DML. A first-class
Snowpark write-side ``branch`` parameter would be cleaner long term.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal, NoReturn

from pyspark.errors.exceptions.base import AnalysisException

from snowflake import snowpark
from snowflake.snowpark_connect.config import (
    global_config,
    is_iceberg_sql_extensions_enabled,
    sessions_config,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.map_sql_expression import as_java_list
from snowflake.snowpark_connect.relation.iceberg_sql_branch_tag_suffix import (
    iceberg_branch_tag_suffix_extensions_disabled_exception,
    try_parse_iceberg_branch_tag_suffix,
    try_parse_iceberg_branch_tag_suffix_parts,
)
from snowflake.snowpark_connect.utils.context import get_spark_session_id
from snowflake.snowpark_connect.utils.telemetry import telemetry

WAP_BRANCH_SPARK_CONFIG = "spark.wap.branch"
_BRANCH_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_\-]+$")


def get_spark_wap_branch() -> str | None:
    """Return the session ``spark.wap.branch`` value when set."""
    session_config = sessions_config[get_spark_session_id()]
    raw = session_config.get(WAP_BRANCH_SPARK_CONFIG) or global_config.get(
        WAP_BRANCH_SPARK_CONFIG
    )
    if raw is None:
        return None
    branch = str(raw).strip()
    return branch or None


def _raise_wap_branch_conflict(
    spark_table_name: str,
    *,
    suffix_branch: str,
    session_branch: str,
) -> NoReturn:
    telemetry.report_iceberg_wap(
        op="unsupported",
        ref_type="branch",
        outcome="rejected",
        error_code="INVALID_CONFIG_VALUE",
        detail="wap_branch_conflict",
    )
    exception = AnalysisException(
        f"Conflicting Iceberg branch targets for {spark_table_name!r}: "
        f"table suffix selects branch {suffix_branch!r} but "
        f"spark.wap.branch is set to {session_branch!r}. Unset "
        "spark.wap.branch or remove the branch suffix from the table name."
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
    raise exception


def _quote_branch_name_sql(branch_name: str) -> str:
    escaped = branch_name.replace("'", "''")
    return f"'{escaped}'"


def snowflake_branch_dml_table_sql(base_table_sql: str, *, branch: str) -> str:
    """Append ``AT (BRANCH => '<name>')`` for Snowflake Iceberg branch DML."""
    return f"{base_table_sql} AT (BRANCH => {_quote_branch_name_sql(branch)})"


def snowflake_fast_forward_sql(
    base_table_sql: str,
    *,
    branch: str,
    from_branch: str,
) -> str:
    """Build Snowflake ``ALTER ICEBERG TABLE … MERGE BRANCH`` for WAP publish."""
    _validate_iceberg_branch_name(branch)
    _validate_iceberg_branch_name(from_branch)
    return (
        f"ALTER ICEBERG TABLE {base_table_sql} "
        f"AT (BRANCH => {_quote_branch_name_sql(branch)}) "
        f"MERGE BRANCH {_quote_branch_name_sql(from_branch)}"
    )


def _raise_tag_dml_not_supported(spark_table_name: str, tag_name: str) -> NoReturn:
    """Snowflake WAP DML is branch-only; tag refs are read-only via AT (VERSION_TAG)."""
    telemetry.report_iceberg_wap(
        op="unsupported",
        ref_type="tag",
        outcome="rejected",
        error_code="UNSUPPORTED_OPERATION",
        detail="tag_dml",
    )
    exception = AnalysisException(
        f"Iceberg version-tag DML target {spark_table_name!r} is not supported. "
        "Snowflake WAP writes use AT (BRANCH => '<name>') on INSERT/UPDATE/DELETE/"
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
    session_wap_branch: str | None = None

    @property
    def has_ref(self) -> bool:
        """True for explicit ``branch_<name>`` suffix targets only."""
        return self.ref_kind is not None

    @property
    def uses_branch_dml(self) -> bool:
        """True when emitted DML SQL carries ``AT (BRANCH => ...)``."""
        return self.dml_snowflake_sql != self.base_snowflake_sql


def _validate_iceberg_branch_name(branch_name: str) -> None:
    """Reject branch names that cannot be safely embedded in Snowflake SQL."""
    if not _BRANCH_NAME_PATTERN.fullmatch(branch_name):
        telemetry.report_iceberg_wap(
            op="unsupported",
            ref_type="branch",
            outcome="rejected",
            error_code="INVALID_INPUT",
            detail="invalid_branch_name",
        )
        exception = AnalysisException(
            f"Invalid Iceberg branch name {branch_name!r}. Branch names may "
            "contain only letters, digits, underscores, and hyphens."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception


def _apply_session_wap_branch_to_target(
    spark_table_name: str,
    base_sql: str,
    dml_op: str | None = None,
) -> IcebergRefDmlTarget:
    session_branch = get_spark_wap_branch()
    if session_branch is None:
        return IcebergRefDmlTarget(
            spark_table_name=spark_table_name,
            base_snowflake_sql=base_sql,
            dml_snowflake_sql=base_sql,
        )
    if not is_iceberg_sql_extensions_enabled():
        raise iceberg_branch_tag_suffix_extensions_disabled_exception()
    _validate_iceberg_branch_name(session_branch)
    telemetry.report_iceberg_wap(
        op="write",
        surface="wap_branch_conf",
        ref_type="branch",
        dml_op=dml_op,
    )
    return IcebergRefDmlTarget(
        spark_table_name=spark_table_name,
        base_snowflake_sql=base_sql,
        dml_snowflake_sql=snowflake_branch_dml_table_sql(
            base_sql, branch=session_branch
        ),
        session_wap_branch=session_branch,
    )


def resolve_iceberg_ref_dml_target(
    spark_table_name: str,
    spark_to_snowflake_fn: Callable[[str], str],
    dml_op: str | None = None,
) -> IcebergRefDmlTarget:
    """Resolve ``table.branch_<name>`` DML targets; reject ``tag_<name>`` writes."""
    parsed = try_parse_iceberg_branch_tag_suffix(spark_table_name)
    if parsed is None:
        base_sql = spark_to_snowflake_fn(spark_table_name)
        return _apply_session_wap_branch_to_target(spark_table_name, base_sql, dml_op)

    if not is_iceberg_sql_extensions_enabled():
        raise iceberg_branch_tag_suffix_extensions_disabled_exception()

    base_spark, options = parsed
    base_sql = spark_to_snowflake_fn(base_spark)
    session_branch = get_spark_wap_branch()
    if "branch" in options:
        branch = options["branch"]
        if session_branch is not None and session_branch != branch:
            _raise_wap_branch_conflict(
                spark_table_name,
                suffix_branch=branch,
                session_branch=session_branch,
            )
        telemetry.report_iceberg_wap(
            op="write",
            surface="df_write",
            ref_type="branch",
            dml_op=dml_op,
        )
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
    dml_op: str | None = None,
) -> IcebergRefDmlTarget:
    """Resolve branch DML targets from Catalyst multipart name segments."""
    parsed = try_parse_iceberg_branch_tag_suffix_parts(parts)
    if parsed is None:
        base_sql = parts_to_snowflake_fn(parts)
        return _apply_session_wap_branch_to_target(spark_table_name, base_sql, dml_op)

    if not is_iceberg_sql_extensions_enabled():
        raise iceberg_branch_tag_suffix_extensions_disabled_exception()

    base_parts, options = parsed
    base_sql = parts_to_snowflake_fn(base_parts)
    session_branch = get_spark_wap_branch()
    if "branch" in options:
        branch = options["branch"]
        if session_branch is not None and session_branch != branch:
            _raise_wap_branch_conflict(
                spark_table_name,
                suffix_branch=branch,
                session_branch=session_branch,
            )
        telemetry.report_iceberg_wap(
            op="write",
            surface="sql_suffix",
            ref_type="branch",
            dml_op=dml_op,
        )
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


def append_dataframe_to_ref_dml_target(
    session: snowpark.Session,
    df: snowpark.DataFrame,
    target: IcebergRefDmlTarget,
) -> None:
    """Append rows via ``INSERT INTO <base> AT (BRANCH => ...) SELECT ...``."""
    queries = df.queries["queries"]
    if len(queries) != 1:
        exception = AnalysisException(
            f"Unexpected number of queries for branch append into "
            f"{target.spark_table_name!r}: {len(queries)}"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception
    session.sql(f"INSERT INTO {target.dml_snowflake_sql} {queries[0]}").collect()


def overwrite_dataframe_to_ref_dml_target(
    session: snowpark.Session,
    df: snowpark.DataFrame,
    target: IcebergRefDmlTarget,
) -> None:
    """Replace all branch rows via ``INSERT OVERWRITE INTO … AT (BRANCH => …)``."""
    queries = df.queries["queries"]
    if len(queries) != 1:
        exception = AnalysisException(
            f"Unexpected number of queries for branch overwrite into "
            f"{target.spark_table_name!r}: {len(queries)}"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception
    session.sql(
        f"INSERT OVERWRITE INTO {target.dml_snowflake_sql} {queries[0]}"
    ).collect()


def overwrite_partitions_dataframe_to_ref_dml_target(
    session: snowpark.Session,
    df: snowpark.DataFrame,
    target: IcebergRefDmlTarget,
    overwrite_condition: snowpark.Column,
) -> None:
    """Partition-targeted branch overwrite via DELETE + INSERT."""
    snowpark_table_for_ref_dml(session, target).delete(overwrite_condition)
    append_dataframe_to_ref_dml_target(session, df, target)


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
