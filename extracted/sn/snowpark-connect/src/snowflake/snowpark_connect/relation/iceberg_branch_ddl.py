#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Translate Iceberg Spark SQL Extension **branch** DDL to Snowflake SQL.

Background
----------
The Iceberg Spark SQL Extensions add DDL for managing branch refs on Iceberg
tables. This module translates that **branch** subset. The Spark branch DDL
surface (from the Iceberg docs and ``CreateOrReplaceBranch`` / ``DropBranch``
logical plans) includes::

    ALTER TABLE <tbl> CREATE BRANCH <name>
    ALTER TABLE <tbl> CREATE BRANCH IF NOT EXISTS <name>
    ALTER TABLE <tbl> CREATE OR REPLACE BRANCH <name>
    ALTER TABLE <tbl> CREATE BRANCH <name> AS OF VERSION <snapshot_id>
    ALTER TABLE <tbl> REPLACE BRANCH <name> [AS OF VERSION <snapshot_id>]
    ALTER TABLE <tbl> DROP BRANCH <name>
    ALTER TABLE <tbl> DROP BRANCH IF EXISTS <name>

Snowflake's surface (internal design doc, branch section) uses the same
``BRANCH`` keyword (not renamed like ``TAG`` -> ``VERSION_TAG``) and
``ALTER ICEBERG TABLE``::

    ALTER ICEBERG TABLE <tbl> CREATE BRANCH '<name>'
    ALTER ICEBERG TABLE <tbl> CREATE BRANCH '<name>' AS OF VERSION <id>
    ALTER ICEBERG TABLE <tbl> REPLACE BRANCH '<name>' [AS OF VERSION <id>]
    ALTER ICEBERG TABLE <tbl> DROP BRANCH '<name>'
    ALTER ICEBERG TABLE <tbl> DROP BRANCH IF EXISTS '<name>'

Branch names are emitted as single-quoted SQL string literals, matching the
Snowflake doc examples (``'dev'``, ``'dev'`` with ``IF EXISTS``). Spark may
pass branch identifiers with surrounding ``'…'``, ``"…"``, or backtick quotes;
those wrappers are stripped before quoting so Snowflake never sees ``''name''``.

Translation policy
------------------
* Bare ``CREATE BRANCH <name>`` (no snapshot binding) **is** translated.
  Unlike ``VERSION_TAG``, Snowflake accepts a branch create without an
  explicit ``AS OF VERSION`` clause today.
* ``IF NOT EXISTS`` / ``IF EXISTS`` pass through on create / drop.
* ``CREATE OR REPLACE BRANCH`` passes through when Iceberg emits it.
* ``AS OF VERSION <id>`` (snapshot-pinned branch create) is translated to a
  trailing ``AS OF VERSION <id>`` clause on the Snowflake ``CREATE BRANCH``
  statement (server-supported from 10.29.100).
* Other ``BranchOptions`` bindings (``numSnapshots``, retention knobs) raise
  ``UNSUPPORTED_OPERATION``.
* Bare ``REPLACE BRANCH`` (without ``CREATE``) maps one-to-one onto Snowflake's
  own ``REPLACE BRANCH``, with the optional ``AS OF VERSION <id>`` carried
  through. Both sides fail when the branch is missing -- Iceberg by definition,
  Snowflake with ``ICEBERG_BRANCH_NOT_FOUND`` (004595) -- so no lowering to
  ``CREATE OR REPLACE`` is needed and none is done.
* Naming a branch ``main`` (exact match, Iceberg's default ref name) raises
  ``UNSUPPORTED_OPERATION`` for both CREATE and REPLACE — Snowflake rejects the
  built-in ``main`` ref either way (004232, "Reference names ... cannot be
  'main'"). Other case variants (e.g. ``MAIN``) are distinct under Iceberg's
  case-sensitive branch naming and are passed through.
* The emitted SQL always uses ``ALTER ICEBERG TABLE``.

JVM source
----------
* ``org.apache.spark.sql.catalyst.plans.logical.CreateOrReplaceBranch``

  - ``table(): Seq[String]``
  - ``branch(): String``
  - ``branchOptions(): BranchOptions``
  - ``create(): Boolean``
  - ``replace(): Boolean``
  - ``ifNotExists(): Boolean``

* ``org.apache.spark.sql.catalyst.plans.logical.DropBranch``

  - ``table(): Seq[String]``
  - ``branch(): String``
  - ``ifExists(): Boolean``

* ``org.apache.spark.sql.catalyst.plans.logical.BranchOptions``

  - ``snapshotId(): Option[Long]``
  - ``numSnapshots(): Option[Long]``
  - ``snapshotRetain(): Option[Long]``
  - ``snapshotRefRetain(): Option[Long]``
"""

from __future__ import annotations

from typing import Any as TypingAny

from pyspark.errors.exceptions.base import AnalysisException

from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.identifiers import strip_spark_identifier_quotes
from snowflake.snowpark_connect.utils.telemetry import telemetry

_RESERVED_BRANCH_NAMES = frozenset({"main"})


def normalize_branch_name(branch_name: str) -> str:
    """Return the bare branch ref name for Snowflake ``BRANCH => '…'`` literals."""
    return strip_spark_identifier_quotes(str(branch_name))


def quote_branch_name_sql(branch_name: str) -> str:
    """Emit a Snowflake branch identifier as a single-quoted string literal.

    Expects a already-normalized bare name; callers normalize at the boundary.
    """
    escaped = branch_name.replace("'", "''")
    return f"'{escaped}'"


def _branch_options_has_unsupported_binding(options: TypingAny) -> str | None:
    """Return a human-readable binding name if ``options`` carries an unsupported field."""
    for accessor, label in (
        ("numSnapshots", "numSnapshots"),
        ("snapshotRetain", "snapshotRetain"),
        ("snapshotRefRetain", "RETAIN"),
    ):
        if hasattr(options, accessor):
            opt = getattr(options, accessor)()
            if opt.isDefined():
                return label
    return None


def _build_create_branch_action(
    *,
    create: bool,
    replace: bool,
    if_not_exists: bool,
) -> str:
    if create and replace:
        return "CREATE OR REPLACE BRANCH"
    if create:
        action = "CREATE BRANCH"
        if if_not_exists:
            action += " IF NOT EXISTS"
        return action
    if replace:
        return "REPLACE BRANCH"
    exception = AnalysisException(
        "Internal: Iceberg CreateOrReplaceBranch plan has neither "
        "'create' nor 'replace' flag set; this is a parser invariant "
        "violation, please report it."
    )
    attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
    raise exception


def translate_create_or_replace_branch(rel: TypingAny, table_name_sql: str) -> str:
    """Translate ``ALTER TABLE … CREATE/REPLACE BRANCH …`` to Snowflake SQL."""
    branch_name = normalize_branch_name(rel.branch())
    create = bool(rel.create())
    replace = bool(rel.replace())
    if_not_exists = bool(rel.ifNotExists())

    # Both rejections below are reachable from REPLACE as well as CREATE, so
    # quote the verb the customer actually wrote back at them.
    replace_only = replace and not create
    ddl_action = "replace" if replace_only else "create"
    verb = "REPLACE BRANCH" if replace_only else "CREATE BRANCH"

    if branch_name in _RESERVED_BRANCH_NAMES:
        telemetry.report_iceberg_wap(
            op="unsupported",
            surface="sql_call",
            ref_type="branch",
            ddl_action=ddl_action,
            outcome="rejected",
            error_code="UNSUPPORTED_OPERATION",
            detail="reserved_main",
        )
        remediation = (
            "To move the built-in main ref to an earlier snapshot, use "
            "Snowflake-native branch management DDL directly."
            if replace_only
            else "Choose a different branch name or use Snowflake-native "
            "branch management DDL directly."
        )
        exception = AnalysisException(
            f"Iceberg branch name {branch_name!r} is reserved by Snowflake "
            f"(the built-in main branch ref cannot be targeted by {verb}). "
            f"{remediation}"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    options = rel.branchOptions()
    unsupported = _branch_options_has_unsupported_binding(options)
    if unsupported is not None:
        telemetry.report_iceberg_wap(
            op="unsupported",
            surface="sql_call",
            ref_type="branch",
            ddl_action=ddl_action,
            outcome="rejected",
            error_code="UNSUPPORTED_OPERATION",
            detail=unsupported,
        )
        exception = AnalysisException(
            f"Iceberg 'ALTER TABLE … {verb} {branch_name!r}' with "
            f"{unsupported} binding is not translated by Snowpark Connect: "
            "Snowflake's documented branch DDL surface supports bare "
            "CREATE BRANCH / DROP BRANCH and snapshot-pinned "
            "'CREATE BRANCH … AS OF VERSION <id>' today. Configure branch "
            "retention directly through Snowflake."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    snapshot_id_opt = options.snapshotId()
    snapshot_id: int | None
    if snapshot_id_opt.isDefined():
        snapshot_id = int(snapshot_id_opt.get())
    else:
        snapshot_id = None

    action = _build_create_branch_action(
        create=create,
        replace=replace,
        if_not_exists=if_not_exists,
    )
    quoted_branch = quote_branch_name_sql(branch_name)
    telemetry.report_iceberg_wap(
        op="branch_ddl",
        surface="sql_call",
        ref_type="branch",
        ddl_action=ddl_action,
    )
    sql = f"ALTER ICEBERG TABLE {table_name_sql} {action} {quoted_branch}"
    if snapshot_id is not None:
        sql += f" AS OF VERSION {snapshot_id}"
    return sql


def translate_drop_branch(rel: TypingAny, table_name_sql: str) -> str:
    """Translate ``ALTER TABLE … DROP BRANCH [IF EXISTS] <name>`` to Snowflake."""
    branch_name = normalize_branch_name(rel.branch())
    if_exists = bool(rel.ifExists())

    action = "DROP BRANCH"
    if if_exists:
        action += " IF EXISTS"
    quoted_branch = quote_branch_name_sql(branch_name)
    telemetry.report_iceberg_wap(
        op="branch_ddl",
        surface="sql_call",
        ref_type="branch",
        ddl_action="drop",
    )
    return f"ALTER ICEBERG TABLE {table_name_sql} {action} {quoted_branch}"
