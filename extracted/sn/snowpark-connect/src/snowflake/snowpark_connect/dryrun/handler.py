#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Dry run handler: validates PySpark workloads without executing queries.

Performs plan translation (map_relation) and SQL compilation (EXPLAIN)
but skips actual data execution and writes.
"""

from typing import Iterator

import pandas
import pyspark.sql.connect.proto.base_pb2 as proto_base
import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake import snowpark
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.dryrun.report import (
    DryRunReport,
    get_dryrun_report,
)
from snowflake.snowpark_connect.execute_plan.utils import (
    pandas_to_arrow_batches_bytes,
)
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    without_internal_columns,
)
from snowflake.snowpark_connect.type_mapping import snowpark_to_proto_type
from snowflake.snowpark_connect.utils.request_utils import (
    get_or_generate_operation_id,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def _explain_sql(session: snowpark.Session, sql: str) -> str | None:
    """
    Run EXPLAIN USING TEXT on a SQL string to validate it compiles.
    Returns None on success, or the error message on failure.
    """
    try:
        session.sql(f"EXPLAIN USING TEXT {sql}").collect()
        return None
    except Exception as e:
        return str(e)


def _build_empty_response(
    request: proto_base.ExecutePlanRequest,
    schema=None,
) -> proto_base.ExecutePlanResponse:
    empty_df = pandas.DataFrame()
    data_bytes = pandas_to_arrow_batches_bytes(empty_df)
    return proto_base.ExecutePlanResponse(
        session_id=request.session_id,
        operation_id=get_or_generate_operation_id(request),
        arrow_batch=proto_base.ExecutePlanResponse.ArrowBatch(
            row_count=0,
            data=data_bytes,
        ),
        schema=schema,
    )


def _get_inner_relation(root: relation_proto.Relation) -> relation_proto.Relation | None:
    """
    Extract the actual input relation from wrapper nodes like ShowString,
    HtmlString, etc. that produce a scalar pandas result. Returns None if
    the root is already a direct DataFrame plan.
    """
    rel_type = root.WhichOneof("rel_type")
    if rel_type == "show_string":
        return root.show_string.input
    if rel_type == "html_string":
        return root.html_string.input
    return None


def _build_show_string_response(
    request: proto_base.ExecutePlanRequest,
    schema_str: str,
    overall_ok: bool,
) -> proto_base.ExecutePlanResponse:
    """Build a response suitable for ShowString (returns a show_string column)."""
    status = "PASS" if overall_ok else "FAIL"
    msg = f"[DRY RUN {status}] Schema: {schema_str}"
    show_df = pandas.DataFrame({"show_string": [msg]})
    data_bytes = pandas_to_arrow_batches_bytes(show_df)
    return proto_base.ExecutePlanResponse(
        session_id=request.session_id,
        operation_id=get_or_generate_operation_id(request),
        arrow_batch=proto_base.ExecutePlanResponse.ArrowBatch(
            row_count=1,
            data=data_bytes,
        ),
    )


def handle_dryrun_root(
    request: proto_base.ExecutePlanRequest,
) -> Iterator[proto_base.ExecutePlanResponse]:
    """
    Dry run handler for 'root' plans (SELECT / DataFrame operations).

    1. Translates the plan via map_relation() (lazy - no SQL execution)
    2. Extracts generated Snowflake SQL
    3. Runs EXPLAIN to validate SQL compilation
    4. Returns empty Arrow batch with correct schema

    Special handling for ShowString/HtmlString: validates the inner
    relation only (avoids query execution) and returns a stub response
    the client can parse.
    """
    report = get_dryrun_report(request.session_id)
    session = snowpark.Session.get_active_session()

    inner_rel = _get_inner_relation(request.plan.root)
    is_show = inner_rel is not None
    plan_to_validate = inner_rel if is_show else request.plan.root

    try:
        result: DataFrameContainer | pandas.DataFrame = map_relation(
            plan_to_validate
        )
    except SnowparkConnectNotImplementedError as e:
        report.record_failure(
            operation="plan_translation",
            detail=f"Unsupported operation: {e}",
        )
        if is_show:
            yield _build_show_string_response(request, "(unknown)", False)
        else:
            yield _build_empty_response(request)
        return
    except Exception as e:
        report.record_failure(
            operation="plan_translation",
            detail=f"Translation error: {type(e).__name__}: {e}",
        )
        if is_show:
            yield _build_show_string_response(request, "(unknown)", False)
        else:
            yield _build_empty_response(request)
        return

    if isinstance(result, pandas.DataFrame):
        report.record_success(
            operation="plan_translation",
            detail="Scalar result (pandas DataFrame)",
        )
        if is_show:
            yield _build_show_string_response(request, "(scalar)", True)
        else:
            yield _build_empty_response(request)
        return

    filtered_result = without_internal_columns(result)
    filtered_df = filtered_result.dataframe
    snowpark_schema = filtered_df.schema

    schema = snowpark_to_proto_type(
        snowpark_schema, filtered_result.column_map, filtered_df
    )

    schema_str = ", ".join(
        f"{f.name}: {f.datatype}" for f in snowpark_schema.fields
    )

    overall_ok = True
    queries = filtered_df.queries.get("queries", [])
    if queries:
        for i, sql in enumerate(queries):
            explain_error = _explain_sql(session, sql)
            if explain_error is None:
                report.record_success(
                    operation=f"sql_compilation[{i}]",
                    detail="EXPLAIN passed",
                    generated_sql=sql,
                    schema_info=schema_str,
                )
            else:
                overall_ok = False
                report.record_failure(
                    operation=f"sql_compilation[{i}]",
                    detail=f"EXPLAIN failed: {explain_error}",
                    generated_sql=sql,
                )
    else:
        report.record_success(
            operation="plan_translation",
            detail="Plan translated (no queries to validate)",
            schema_info=schema_str,
        )

    logger.info(f"[DRYRUN] root plan validated. Schema: {schema_str}")
    if is_show:
        yield _build_show_string_response(request, schema_str, overall_ok)
    else:
        yield _build_empty_response(request, schema=schema)


def handle_dryrun_command(
    request: proto_base.ExecutePlanRequest,
) -> proto_base.ExecutePlanResponse | None:
    """
    Dry run handler for 'command' plans (writes, DDL, UDF registration, etc.).

    Validates the plan without executing side effects.
    """
    report = get_dryrun_report(request.session_id)
    session = snowpark.Session.get_active_session()
    command_type = request.plan.command.WhichOneof("command_type")

    match command_type:
        case "write_operation" | "write_operation_v2":
            _dryrun_write(request, report, session, command_type)

        case "sql_command":
            return _dryrun_sql_command(request, report, session)

        case "create_dataframe_view":
            _dryrun_create_view(request, report)

        case "register_function" | "register_table_function":
            report.record_warning(
                operation=command_type,
                detail="UDF/UDTF registration skipped in dry run (definition not validated against Snowflake)",
            )

        case other:
            report.record_warning(
                operation=str(other),
                detail=f"Command '{other}' skipped in dry run",
            )

    return None


def _dryrun_write(
    request: proto_base.ExecutePlanRequest,
    report: DryRunReport,
    session: snowpark.Session,
    command_type: str,
) -> None:
    """Validate the input relation of a write operation without writing."""
    try:
        if command_type == "write_operation":
            input_rel = request.plan.command.write_operation.input
        else:
            input_rel = request.plan.command.write_operation_v2.input

        result = map_relation(input_rel)

        if isinstance(result, DataFrameContainer):
            df = result.dataframe
            queries = df.queries.get("queries", [])
            for i, sql in enumerate(queries):
                explain_error = _explain_sql(session, sql)
                if explain_error is None:
                    report.record_success(
                        operation=f"write_input_validation[{i}]",
                        detail="Write input SQL compiles",
                        generated_sql=sql,
                    )
                else:
                    report.record_failure(
                        operation=f"write_input_validation[{i}]",
                        detail=f"Write input EXPLAIN failed: {explain_error}",
                        generated_sql=sql,
                    )
        else:
            report.record_success(
                operation="write_input_validation",
                detail="Write input translated successfully",
            )
    except SnowparkConnectNotImplementedError as e:
        report.record_failure(
            operation="write_input_validation",
            detail=f"Unsupported operation in write input: {e}",
        )
    except Exception as e:
        report.record_failure(
            operation="write_input_validation",
            detail=f"Write input error: {type(e).__name__}: {e}",
        )


def _dryrun_sql_command(
    request: proto_base.ExecutePlanRequest,
    report: DryRunReport,
    session: snowpark.Session,
) -> proto_base.ExecutePlanResponse:
    """Validate a SQL command by translating it through map_relation (handles
    SQLGlot translation and temp view resolution) then running EXPLAIN on the
    generated Snowflake SQL."""
    sql_command = request.plan.command.sql_command

    relation = relation_proto.Relation(
        sql=relation_proto.SQL(
            query=sql_command.sql,
            args=sql_command.args,
            pos_args=sql_command.pos_args,
        )
    )

    try:
        result = map_relation(relation)
        if isinstance(result, DataFrameContainer):
            queries = result.dataframe.queries.get("queries", [])
            for i, sql in enumerate(queries):
                explain_error = _explain_sql(session, sql)
                if explain_error is None:
                    report.record_success(
                        operation=f"sql_command[{i}]",
                        detail="SQL compiles successfully",
                        generated_sql=sql,
                    )
                else:
                    report.record_failure(
                        operation=f"sql_command[{i}]",
                        detail=f"SQL EXPLAIN failed: {explain_error}",
                        generated_sql=sql,
                    )
        else:
            report.record_success(
                operation="sql_command",
                detail="SQL translated successfully",
                generated_sql=sql_command.sql,
            )
    except Exception as e:
        report.record_failure(
            operation="sql_command",
            detail=f"SQL translation error: {type(e).__name__}: {e}",
            generated_sql=sql_command.sql,
        )

    return proto_base.ExecutePlanResponse(
        session_id=request.session_id,
        operation_id=get_or_generate_operation_id(request),
        sql_command_result=proto_base.ExecutePlanResponse.SqlCommandResult(
            relation=relation
        ),
    )


def _dryrun_create_view(
    request: proto_base.ExecutePlanRequest,
    report: DryRunReport,
) -> None:
    """
    Actually create the temp view even in dry run mode.

    Temp views are side-effect-free (no data writes) and are needed by
    subsequent SQL queries that reference them.
    """
    from snowflake.snowpark_connect.utils.temporary_view_helper import (
        create_temporary_view_from_dataframe,
    )

    req = request.plan.command.create_dataframe_view
    try:
        input_df_container = without_internal_columns(map_relation(req.input))
        create_temporary_view_from_dataframe(
            input_df_container, req.name, req.is_global, req.replace
        )
        report.record_success(
            operation="create_dataframe_view",
            detail=f"View '{req.name}' created",
        )
    except SnowparkConnectNotImplementedError as e:
        report.record_failure(
            operation="create_dataframe_view",
            detail=f"Unsupported operation in view input: {e}",
        )
    except Exception as e:
        report.record_failure(
            operation="create_dataframe_view",
            detail=f"View input error: {type(e).__name__}: {e}",
        )
