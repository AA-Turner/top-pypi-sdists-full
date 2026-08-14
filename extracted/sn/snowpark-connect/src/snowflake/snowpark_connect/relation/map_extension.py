#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import copy
from typing import Any, NamedTuple

import cloudpickle as pkl
import pyspark.sql.connect.proto.expressions_pb2 as expression_proto
import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.base import AnalysisException

import snowflake.snowpark.functions as snowpark_fn
import snowflake.snowpark.types as snowpark_types
import snowflake.snowpark_connect.proto.snowflake_relation_ext_pb2 as snowflake_proto
from snowflake import snowpark
from snowflake.snowpark import Column
from snowflake.snowpark_connect.column_name_handler import (
    ColumnNameMap,
    make_column_names_snowpark_compatible,
    schema_getter,
)
from snowflake.snowpark_connect.column_qualifier import ColumnQualifier
from snowflake.snowpark_connect.config import get_boolean_session_config_param
from snowflake.snowpark_connect.dataframe_container import (
    AggregateMetadata,
    DataFrameContainer,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.literal import get_literal_field_and_name
from snowflake.snowpark_connect.expression.map_expression import (
    map_expression,
    map_single_column_expression,
)
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.relation.map_column_ops import _rekey_column_metadata
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.utils import (
    create_pivot_column_condition,
    get_all_dependent_column_names,
    map_pivot_value_to_spark_column_name,
)
from snowflake.snowpark_connect.typed_column import FieldType, TypedColumn
from snowflake.snowpark_connect.utils.context import (
    get_sql_aggregate_function_count,
    push_outer_dataframe,
    set_current_grouping_columns,
)
from snowflake.snowpark_connect.utils.expression_transformer import (
    inject_condition_to_all_agg_functions,
)
from snowflake.snowpark_connect.utils.identifiers import (
    split_fully_qualified_spark_name,
)
from snowflake.snowpark_connect.utils.python_udf_marshal import (
    encode_native_or_variant_args,
    python_is_native_input,
)
from snowflake.snowpark_connect.utils.spark_session_cache import get_spark_session_cache
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def map_extension(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    The Extension relation type contains any extensions we use for adding new
    functionality to Spark Connect.

    The extension will require new protobuf messages to be defined in the
    snowflake_connect_server/proto directory.
    """
    extension = snowflake_proto.Extension()
    rel.extension.Unpack(extension)
    match extension.WhichOneof("op"):
        case "rdd_map":
            rdd_map = extension.rdd_map
            result = map_relation(rdd_map.input)
            input_df = result.dataframe

            column_name = "_RDD_"
            if len(input_df.columns) > 1:
                input_df = input_df.select(
                    snowpark_fn.array_construct(*input_df.columns).as_(column_name)
                )
                input_type = snowpark_types.ArrayType(snowpark_types.IntegerType())
                return_type = snowpark_types.ArrayType(snowpark_types.IntegerType())
            else:
                input_df = input_df.rename(input_df.columns[0], column_name)
                input_type = snowpark_types.VariantType()
                return_type = snowpark_types.VariantType()
            from snowflake.snowpark_connect.utils.context import get_spark_session_id

            rdd_udf_name = f"my_udf_{get_spark_session_id().replace('-','_')}"
            func = snowpark_fn.udf(
                pkl.loads(rdd_map.func),
                return_type=return_type,
                input_types=[input_type],
                name=rdd_udf_name,
                replace=True,
            )
            result = input_df.select(func(column_name).as_(column_name))
            return DataFrameContainer.create_with_column_mapping(
                dataframe=result,
                spark_column_names=[column_name],
                snowpark_column_names=[column_name],
                snowpark_column_types=[return_type],
            )
        case "subquery_column_aliases":
            subquery_aliases = extension.subquery_column_aliases
            rel.extension.Unpack(subquery_aliases)
            result = map_relation(subquery_aliases.input)
            input_df = result.dataframe
            snowpark_col_names = result.column_map.get_snowpark_columns()
            if len(subquery_aliases.aliases) != len(snowpark_col_names):
                exception = AnalysisException(
                    "Number of column aliases does not match number of columns. "
                    f"Number of column aliases: {len(subquery_aliases.aliases)}; "
                    f"number of columns: {len(snowpark_col_names)}."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                raise exception
            # Re-key column_metadata to preserve UDT metadata through alias rename.
            old_spark_names = result.column_map.get_spark_columns()
            renamed_metadata = _rekey_column_metadata(
                result.column_map.column_metadata,
                old_spark_names,
                list(subquery_aliases.aliases),
            )
            return DataFrameContainer.create_with_column_mapping(
                dataframe=input_df,
                spark_column_names=subquery_aliases.aliases,
                snowpark_column_names=snowpark_col_names,
                column_metadata=renamed_metadata,
                column_qualifiers=result.column_map.get_qualifiers(),
                equivalent_snowpark_names=result.column_map.get_equivalent_snowpark_names(),
            )
        case "lateral_join":
            lateral_join = extension.lateral_join
            left_result = map_relation(lateral_join.left)
            left_df = left_result.dataframe

            udtf_info = get_udtf_project(lateral_join.right)
            if udtf_info:
                return handle_lateral_join_with_udtf(
                    left_result, lateral_join.right, udtf_info
                )

            left_queries = left_df.queries["queries"]
            if len(left_queries) != 1:
                exception = SnowparkConnectNotImplementedError(
                    f"Unexpected number of queries: {len(left_queries)}"
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception
            left_query = left_queries[0]
            with push_outer_dataframe(left_result):
                right_result = map_relation(lateral_join.right)
                right_df = right_result.dataframe
            right_queries = right_df.queries["queries"]
            if len(right_queries) != 1:
                exception = SnowparkConnectNotImplementedError(
                    f"Unexpected number of queries: {len(right_queries)}"
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception
            right_query = right_queries[0]
            # A UDTF invocation that get_udtf_project didn't recognize (e.g. a
            # column-aliased `LATERAL udtf(x) AS t(a, b)`) produces a Project with no input
            # relation, whose query string is empty; interpolating it below yields
            # `... LATERAL ()`, which the parser rejects with an opaque "empty statement"
            # error. Fail loudly with an actionable message instead.
            if not right_query or not right_query.strip():
                exception = SnowparkConnectNotImplementedError(
                    "Unsupported LATERAL join right-hand side. For a table function, use "
                    "`FROM left, LATERAL udtf(args)` with a registered UDTF; the "
                    "column-aliased form `LATERAL udtf(args) AS t(col, ...)` is not yet "
                    "supported in spark.sql() — alias the columns in the SELECT instead."
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception
            input_df_sql = f"WITH __left AS ({left_query}) SELECT * FROM __left INNER JOIN LATERAL ({right_query})"
            session = snowpark.Session.get_active_session()
            input_df = session.sql(input_df_sql)
            return DataFrameContainer.create_with_column_mapping(
                dataframe=input_df,
                spark_column_names=left_result.column_map.get_spark_columns()
                + right_result.column_map.get_spark_columns(),
                snowpark_column_names=left_result.column_map.get_snowpark_columns()
                + right_result.column_map.get_snowpark_columns(),
                column_qualifiers=left_result.column_map.get_qualifiers()
                + right_result.column_map.get_qualifiers(),
                equivalent_snowpark_names=left_result.column_map.get_equivalent_snowpark_names()
                + right_result.column_map.get_equivalent_snowpark_names(),
            )

        case "udtf_with_table_arguments":
            return handle_udtf_with_table_arguments(extension.udtf_with_table_arguments)
        case "aggregate":
            return map_aggregate(extension.aggregate, rel.common.plan_id)
        case "qualify_leading_columns":
            return _map_qualify_leading_columns(extension.qualify_leading_columns)
        case other:
            exception = SnowparkConnectNotImplementedError(
                f"Unexpected extension {other}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception


def _map_qualify_leading_columns(
    op: snowflake_proto.QualifyLeadingColumns,
) -> DataFrameContainer:
    """Add `op.qualifier` to the leading columns of `op.input`.

    Specifically, the qualifier is added to the qualifier set of columns at
    indices `[0, total_columns - op.num_trailing_unqualified_columns)`. The
    trailing `op.num_trailing_unqualified_columns` columns are left untouched
    — they keep their existing qualifiers and do NOT receive `op.qualifier`.
    The underlying Snowpark `DataFrame` is unchanged — only column-name
    metadata is augmented, so column types are preserved.

    SNOW-2845305: This is used to implement Spark's
    `LATERAL VIEW <fn>(args) <alias>` semantics: `relation/map_sql.py` builds
    a Project of the form `[*generator_outputs, *carried_child_columns]` and
    wraps it with this op, so only the generator-output prefix is qualified by
    the lateral-view alias. The previous approach wrapped generator outputs in
    `struct(col) AS <alias>`, which erased the element type
    (e.g., IntegerType became VARIANT/StringType); applying the alias as a
    pure qualifier here preserves the underlying types.
    """
    inner = map_relation(op.input)
    qualifier = ColumnQualifier((op.qualifier,))
    columns = inner.column_map.columns
    num_trailing_unqualified = max(0, op.num_trailing_unqualified_columns)
    num_leading = len(columns) - num_trailing_unqualified
    if num_leading <= 0:
        return inner

    new_qualifiers: list[set[ColumnQualifier]] = []
    for idx, col in enumerate(columns):
        if idx < num_leading:
            new_qualifiers.append(set(col.qualifiers) | {qualifier})
        else:
            new_qualifiers.append(set(col.qualifiers))

    return DataFrameContainer.create_with_column_mapping(
        dataframe=inner.dataframe,
        spark_column_names=[c.spark_name for c in columns],
        snowpark_column_names=[c.snowpark_name for c in columns],
        column_metadata=inner.column_map.column_metadata,
        column_qualifiers=new_qualifiers,
        column_is_internal=[c.is_internal for c in columns],
        column_is_qualified_access_only=[c.is_qualified_access_only for c in columns],
        equivalent_snowpark_names=[c.equivalent_snowpark_names for c in columns],
        parent_column_name_map=inner.column_map.get_parent_column_name_map(),
        cached_schema_getter=schema_getter(inner.dataframe),
    )


class UDTFAliasedProjection(NamedTuple):
    relation: relation_proto.Relation
    alias: str | None


def get_udtf_project(
    relation: relation_proto.Relation,
) -> tuple[
    tuple[snowpark.udtf.UserDefinedTableFunction, list], UDTFAliasedProjection
] | None:
    """
    Extract UDTF information from a relation if it's a project containing a UDTF call.

    Returns:
        tuple[udtf_obj, udtf_spark_output_names] if UDTF found, None otherwise
    """
    aliased_projection: UDTFAliasedProjection | None = None
    if relation.WhichOneof("rel_type") == "subquery_alias":
        alias = relation.subquery_alias.alias
        relation = relation.subquery_alias.input
        aliased_projection = UDTFAliasedProjection(relation=relation, alias=alias)

    if relation.WhichOneof("rel_type") == "project":
        expressions = relation.project.expressions
        if (
            len(expressions) == 1
            and expressions[0].WhichOneof("expr_type") == "unresolved_function"
        ):
            func = expressions[0].unresolved_function
            udtf_name_lower = func.function_name.lower()
            cache = get_spark_session_cache()
            if cache.udtfs.has(udtf_name_lower):
                return cache.udtfs.get(udtf_name_lower), aliased_projection

    return None


def _variant_packed_table_arg_result(
    base_df,
    table_containers: list,
    scalar_typed_args: list,
    _udtf_obj,
    over_kwargs: dict,
):
    """Legacy encoding: pack each table argument's row into a single VARIANT object
    ({"__fields__": [...], "__values__": [...]}) and pass scalar args per the UDTF's
    declared input_types. Used when the native per-column path is not applicable."""
    table_arg_variants = []
    for table_container, table_arg_idx in table_containers:
        table_columns = table_container.column_map.get_snowpark_columns()
        spark_columns = table_container.column_map.get_spark_columns()

        # Create a structure that supports both positional and named access
        # Format: {"__fields__": ["col1", "col2"], "__values__": [val1, val2]}
        # This allows UDTFs to access table arguments both ways: a[0] and a["col1"]
        fields_array = snowpark_fn.array_construct(
            *[snowpark_fn.lit(col) for col in spark_columns]
        )
        values_array = snowpark_fn.array_construct(
            *[snowpark_fn.col(col) for col in table_columns]
        )

        table_arg_variant = snowpark_fn.to_variant(
            snowpark_fn.object_construct(
                snowpark_fn.lit("__fields__"),
                fields_array,
                snowpark_fn.lit("__values__"),
                values_array,
            )
        )
        table_arg_variants.append((table_arg_variant, table_arg_idx))

    # Registered UDTFs are always created with all-VARIANT input types (register_udtf
    # has no call-site types), so every scalar arg is wrapped in VARIANT here. The
    # native per-column encoding is handled separately in _try_native_table_arg_udtf.
    scalar_args_encoded = [snowpark_fn.to_variant(tc.col) for tc in scalar_typed_args]

    all_args = scalar_args_encoded.copy()
    for table_arg_variant, table_arg_idx in sorted(
        table_arg_variants, key=lambda x: x[1]
    ):
        all_args.insert(table_arg_idx, table_arg_variant)

    udtf_func = snowpark_fn.table_function(_udtf_obj.name)
    udtf_call = udtf_func(*all_args)
    if over_kwargs:
        udtf_call = udtf_call.over(**over_kwargs)
    return base_df.join_table_function(udtf_call)


def _try_native_table_arg_udtf(
    cache,
    udtf_name_lower: str,
    base_df,
    table_container_entry: tuple,
    scalar_typed_args: list,
    over_kwargs: dict,
):
    """Attempt the native per-column encoding for a single-table-argument UDTF.

    Passes each table column as an individual native-typed argument (rather than one
    packed VARIANT object) and re-emits the physical function with native per-column
    params via the registration-time recreation closure. The handler-side wrapper
    rebuilds the single Row from the flat args (see ``_regroup_flat_table_args``).

    Returns the joined DataFrame, or ``None`` to signal the caller to fall back to the
    VARIANT-packing path — when there is no recreation closure (e.g. inline UDTFs or
    sproc-mode), a table column is not a native scalar, or the arg layout is unexpected.
    """
    recreate_fn = cache.udtfs.get_recreate_fn(udtf_name_lower)
    if recreate_fn is None:
        return None

    container, table_arg_idx = table_container_entry
    spark_fields = container.column_map.get_spark_columns()
    sf_cols = container.column_map.get_snowpark_columns()
    if not sf_cols or len(sf_cols) != len(spark_fields):
        return None

    # Resolve each table column's Snowpark type from the base DataFrame schema.
    # Prefer an exact name match; fall back to a case/quote-normalized match only when
    # it is unambiguous — two fields sharing a normalized key would otherwise pick the
    # wrong type, so in that case we bail to the safe VARIANT-packing path.
    type_by_name = {f.name: f.datatype for f in base_df.schema.fields}
    norm_counts: dict = {}
    norm_by_name: dict = {}
    for f in base_df.schema.fields:
        key = f.name.strip('"').upper()
        norm_counts[key] = norm_counts.get(key, 0) + 1
        norm_by_name[key] = f.datatype
    col_types = []
    for c in sf_cols:
        dt = type_by_name.get(c)
        if dt is None:
            key = c.strip('"').upper()
            if norm_counts.get(key, 0) == 1:
                dt = norm_by_name.get(key)
        if dt is None or not python_is_native_input(dt):
            return None
        col_types.append(dt)

    total_args = len(scalar_typed_args) + 1  # single table argument
    if not (0 <= table_arg_idx < total_args):
        return None

    flat_cols: list = []
    flat_types: list = []
    table_arg_layout: list = []
    scalar_iter = iter(scalar_typed_args)
    for pos in range(total_args):
        if pos == table_arg_idx:
            for c, dt in zip(sf_cols, col_types):
                flat_cols.append(snowpark_fn.col(c))
                flat_types.append(dt)
            table_arg_layout.append(("row", list(spark_fields)))
        else:
            tc = next(scalar_iter)
            if python_is_native_input(tc.typ):
                flat_cols.append(tc.col)
            else:
                flat_cols.append(snowpark_fn.to_variant(tc.col))
            flat_types.append(tc.typ)
            table_arg_layout.append(("scalar", None))

    signature_key = repr((tuple(repr(t) for t in flat_types), table_arg_layout))
    native_udtf = cache.udtfs.get_native_variant(udtf_name_lower, signature_key)
    if native_udtf is None:
        native_udtf = recreate_fn(flat_types, table_arg_layout)
        if native_udtf is None:
            return None
        cache.udtfs.set_native_variant(udtf_name_lower, signature_key, native_udtf)

    udtf_func = snowpark_fn.table_function(native_udtf.name)
    udtf_call = udtf_func(*flat_cols)
    if over_kwargs:
        udtf_call = udtf_call.over(**over_kwargs)
    return base_df.join_table_function(udtf_call)


def handle_udtf_with_table_arguments(
    udtf_info: snowflake_proto.UDTFWithTableArguments,
) -> DataFrameContainer:
    """
    Handle UDTF with one or more table arguments using Snowpark's join_table_function.
    For multiple table arguments, this creates a Cartesian product of all input tables.
    """
    session = snowpark.Session.get_active_session()
    udtf_name_lower = udtf_info.function_name.lower()
    cache = get_spark_session_cache()
    if not cache.udtfs.has(udtf_name_lower):
        exception = ValueError(f"UDTF '{udtf_info.function_name}' not found.")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception
    _udtf_obj, udtf_spark_output_names = cache.udtfs.get(udtf_name_lower)

    table_containers = []
    table_sort_exprs_list = []
    for table_arg_info in udtf_info.table_arguments:
        result = map_relation(table_arg_info.table_argument)
        table_containers.append((result, table_arg_info.table_argument_idx))
        # sortWithinPartitions ordering carried through the container, so the UDTF
        # can see rows in the intended order via .over(order_by=...).
        table_sort_exprs_list.append(result.sort_exprs)

    if len(table_containers) == 1:
        base_df = table_containers[0][0].dataframe
    else:
        if not get_boolean_session_config_param(
            "spark.sql.tvf.allowMultipleTableArguments.enabled"
        ):
            exception = AnalysisException(
                "[TABLE_VALUED_FUNCTION_TOO_MANY_TABLE_ARGUMENTS] Multiple table arguments are not enabled. "
                "Please set `spark.sql.tvf.allowMultipleTableArguments.enabled` to `true`"
            )
            attach_custom_error_code(exception, ErrorCodes.CONFIG_NOT_ENABLED)
            raise exception

        base_df = table_containers[0][0].dataframe
        first_table_col_count = len(base_df.columns)

        for table_container, _ in table_containers[1:]:
            base_df = base_df.cross_join(table_container.dataframe)

        # Ensure deterministic ordering to match Spark's Cartesian product behavior
        # For two tables A and B, Spark produces: for each B row, iterate through A rows
        # Sort order: B columns first (outer loop), then A columns (inner loop)
        all_columns = base_df.columns
        first_table_cols = all_columns[:first_table_col_count]
        subsequent_table_cols = all_columns[first_table_col_count:]

        base_df = base_df.sort(*(subsequent_table_cols + first_table_cols))

    scalar_typed_args = []
    typer = ExpressionTyper.dummy_typer(session)
    empty_column_map = ColumnNameMap([], [], None)
    for arg_proto in udtf_info.arguments:
        # UDTF when used with table arguments, the arguments can only be scalar arguments like integer, literals etc. or Table arguments.
        # Using map_expression with dummy typer to resolve the scalar arguments.
        _, typed_column = map_expression(arg_proto, empty_column_map, typer)
        scalar_typed_args.append(typed_column)

    # Apply ORDER BY when the single table argument carried sort_exprs from
    # sortWithinPartitions. This does NOT add a PARTITION BY: OSS Spark passes a
    # UDTF's TABLE argument as a single partition unless the SQL explicitly says
    # PARTITION BY, so ordering the single partition is what matches Spark.
    # Multiple-table-arg UDTFs get a Cartesian product; .over() is not meaningful there.
    # sort_exprs are stored as Spark column names + sort metadata; a projection
    # that renames a sort key rewrites the stored name (see map_column_ops), so an
    # aliased key still resolves here and matches Spark's preserved ordering.
    over_kwargs: dict = {}
    if len(table_sort_exprs_list) == 1 and table_sort_exprs_list[0]:
        sort_info = table_sort_exprs_list[0]
        col_map = table_containers[0][0].column_map
        order_cols = []
        for spark_name, direction, null_order in sort_info:
            snp_name = col_map.get_snowpark_column_name_from_spark_column_name(
                spark_name, allow_non_exists=True
            )
            if not snp_name:
                # The sort key was physically dropped by an intervening projection
                # before the UDTF call, so the column no longer exists on the table
                # argument and there is nothing to ORDER BY. Unlike an alias (which
                # we rewrite upstream), a dropped column cannot be recovered here.
                # OSS Spark keeps the physical ordering because its Sort sits below
                # the Project; SCOS re-applies the order at the call site, which is
                # impossible once the column is gone. Fail loudly rather than hand a
                # stateful UDTF rows in an arbitrary order.
                exception = AnalysisException(
                    f"sortWithinPartitions key {spark_name!r} was dropped by a "
                    "projection before the UDTF table argument, so its ordering "
                    "cannot be applied. Keep the sort column (or alias it) in the "
                    "table argument to preserve ordering."
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception
            col = base_df.col(snp_name)
            if direction == "asc":
                col = (
                    col.asc_nulls_first()
                    if null_order == "first"
                    else col.asc_nulls_last()
                )
            else:
                col = (
                    col.desc_nulls_first()
                    if null_order == "first"
                    else col.desc_nulls_last()
                )
            order_cols.append(col)
        if order_cols:
            over_kwargs["order_by"] = order_cols

    # Try the native per-column encoding first (single table argument): pass each table
    # column as an individual native-typed argument and let the handler-side wrapper rebuild
    # the Row, eliminating the VARIANT __fields__/__values__ packing done per row. Falls back
    # to VARIANT packing when the shape isn't supported or a column isn't a native scalar.
    result_df = None
    if len(table_containers) == 1:
        result_df = _try_native_table_arg_udtf(
            cache,
            udtf_name_lower,
            base_df,
            table_containers[0],
            scalar_typed_args,
            over_kwargs,
        )

    if result_df is None:
        result_df = _variant_packed_table_arg_result(
            base_df, table_containers, scalar_typed_args, _udtf_obj, over_kwargs
        )

    # Return only the UDTF output columns
    original_column_count = len(base_df.columns)
    udtf_output_columns = result_df.columns[original_column_count:]

    final_df = result_df.select(*udtf_output_columns)

    return DataFrameContainer.create_with_column_mapping(
        dataframe=final_df,
        spark_column_names=udtf_spark_output_names,
        snowpark_column_names=udtf_output_columns,
    )


def handle_lateral_join_with_udtf(
    left_result: DataFrameContainer,
    udtf_relation: relation_proto.Relation,
    udtf_info: tuple[
        tuple[snowpark.udtf.UserDefinedTableFunction, list],
        UDTFAliasedProjection,
    ],
) -> DataFrameContainer:
    """
    Handle lateral join with UDTF on the right side using join_table_function.
    """
    session = snowpark.Session.get_active_session()

    (_udtf_obj, udtf_spark_output_names), aliased_projection = udtf_info
    udtf_relation = aliased_projection.relation if aliased_projection else udtf_relation

    project = udtf_relation.project
    udtf_func = project.expressions[0].unresolved_function

    typer = ExpressionTyper.dummy_typer(session)
    left_column_map = left_result.column_map
    left_df = left_result.dataframe
    table_func = snowpark_fn.table_function(_udtf_obj.name)
    udtf_typed_args = [
        map_expression(arg_proto, left_column_map, typer)[1]
        for arg_proto in udtf_func.arguments
    ]
    udtf_args_encoded = encode_native_or_variant_args(
        udtf_typed_args,
        getattr(_udtf_obj, "input_types", []),
        variant_encoder=snowpark_fn.to_variant,
    )
    result_df = left_df.join_table_function(table_func(*udtf_args_encoded))

    right_qualifiers = (
        [
            {ColumnQualifier((aliased_projection.alias,))}
            for _ in udtf_spark_output_names
        ]
        if aliased_projection
        else [set() for _ in udtf_spark_output_names]
    )

    return DataFrameContainer.create_with_column_mapping(
        dataframe=result_df,
        spark_column_names=left_result.column_map.get_spark_columns()
        + udtf_spark_output_names,
        snowpark_column_names=result_df.columns,
        column_qualifiers=left_result.column_map.get_qualifiers() + right_qualifiers,
        equivalent_snowpark_names=left_result.column_map.get_equivalent_snowpark_names()
        + [set() for _ in udtf_spark_output_names],
    )


def map_aggregate(
    aggregate: snowflake_proto.Aggregate, plan_id: int
) -> DataFrameContainer:
    input_container = map_relation(aggregate.input)
    input_df: snowpark.DataFrame = input_container.dataframe

    # Detect the "GROUP BY ALL" case:
    # - it's a plain GROUP BY (not ROLLUP, CUBE, etc.)
    # - it's grouped by a single identifier named "ALL"
    # - there is no existing column named "ALL"
    is_group_by_all = False
    if (
        aggregate.group_type == snowflake_proto.Aggregate.GROUP_TYPE_GROUPBY
        and len(aggregate.grouping_expressions) == 1
    ):
        parsed_col_name = split_fully_qualified_spark_name(
            aggregate.grouping_expressions[0].unresolved_attribute.unparsed_identifier
        )
        if (
            len(parsed_col_name) == 1
            and parsed_col_name[0].lower() == "all"
            and input_container.column_map.get_snowpark_column_name_from_spark_column_name(
                parsed_col_name[0], allow_non_exists=True
            )
            is None
        ):
            is_group_by_all = True

    # First, map all groupings and aggregations.
    # In case of GROUP BY ALL, groupings are a subset of the aggregations.

    typer = ExpressionTyper(input_df)

    def _map_columns(
        exp: expression_proto.Expression,
    ) -> list[tuple[str, TypedColumn]]:
        new_names, snowpark_column = map_expression(
            exp, input_container.column_map, typer
        )
        if len(new_names) == 1:
            return [(new_names[0], snowpark_column)]
        results = []
        for name in new_names:
            snowpark_name = input_container.column_map.get_snowpark_column_name_from_spark_column_name(
                name
            )
            col_expr = snowpark_fn.col(snowpark_name)
            col_type = input_df.schema[snowpark_name].datatype
            results.append(
                (
                    name,
                    TypedColumn(
                        col_expr,
                        lambda col_type=col_type: [col_type],
                    ),
                )
            )
        return results

    raw_groupings: list[tuple[str, TypedColumn]] = []
    raw_aggregations: list[tuple[str, TypedColumn, set[ColumnQualifier]]] = []

    if not is_group_by_all:
        if any(
            exp.WhichOneof("expr_type") == "unresolved_star"
            for exp in aggregate.grouping_expressions
        ):
            exception = AnalysisException("Star (*) is not allowed in GROUP BY")
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        for exp in aggregate.grouping_expressions:
            raw_groupings.extend(_map_columns(exp))

    # Determine grouping columns for context
    # For GROUPING SETS, we need to extract the columns from the sets
    grouping_columns_for_context = []
    column_names_per_grouping_set: list[set[str]] = []
    if aggregate.group_type == snowflake_proto.Aggregate.GROUP_TYPE_GROUPING_SETS:
        # Use a list to preserve order, avoiding duplicates
        for grouping_set in aggregate.grouping_sets:
            column_names_in_current_set: set[str] = set()
            for grouping_expr in grouping_set.grouping_set:
                resolved_names, _ = map_expression(
                    grouping_expr, input_container.column_map, typer
                )
                # map_expression always returns a list, get the first element
                col_name = resolved_names[0]
                column_names_in_current_set.add(col_name)
                if col_name not in grouping_columns_for_context:
                    grouping_columns_for_context.append(col_name)
            column_names_per_grouping_set.append(column_names_in_current_set)
    else:
        grouping_columns_for_context = [spark_name for spark_name, _ in raw_groupings]

    # Set grouping columns context for processing aggregate expressions
    # This context is needed for resolving grouping__id references
    # TODO: This should properly handle nested queries with GROUP BY using push/pop
    # Currently, nested queries may interfere with parent queries
    set_current_grouping_columns(grouping_columns_for_context)

    # LCA Support for aggregate expressions: Use the LCA alias map
    # Note: We don't clear the map here to preserve any parent context aliases
    from snowflake.snowpark_connect.utils.context import register_lca_alias

    # If it's an unresolved attribute when its in aggregate.aggregate_expressions, we know it came from the parent map straight away
    # in this case, we should see if the parent map has a qualifier for it and propagate that here, in case the order by references it in
    # a qualified way later.
    agg_count = get_sql_aggregate_function_count()
    for exp in aggregate.aggregate_expressions:
        cols = _map_columns(exp)
        for col in cols:
            if exp.WhichOneof("expr_type") == "unresolved_attribute":
                qualifiers: set[
                    ColumnQualifier
                ] = input_container.column_map.get_qualifiers_for_snowpark_column(
                    col[1].col.get_name()
                )
            else:
                qualifiers = set()

            raw_aggregations.append((col[0], col[1], qualifiers))

        # If this is an alias, register it in the LCA map for subsequent expressions
        if (
            exp.WhichOneof("expr_type") == "alias"
            and exp.alias.name
            and len(exp.alias.name) > 0
        ):
            alias_name = exp.alias.name[0]
            spark_name, snowpark_column = cols[0]

            # Register the alias pointing to the result of its expression
            # This handles both simple aliases (k as lca) and complex ones (lca + 1 as col)
            # The snowpark_column already contains the computed expression with its alias wrapper,
            # which is fine - when referenced later, the column's value is what gets used
            register_lca_alias(alias_name, snowpark_column)

        if is_group_by_all:
            new_agg_count = get_sql_aggregate_function_count()
            if new_agg_count == agg_count:
                for col in cols:
                    raw_groupings.append(col)
            else:
                agg_count = new_agg_count

    # Now create column name lists and assign aliases.
    # In case of GROUP BY ALL, even though groupings are a subset of aggregations,
    # they will have their own aliases so we can drop them later.

    spark_columns: list[str] = []
    snowpark_columns: list[str] = []
    snowpark_column_types: list[FieldType] = []
    all_qualifiers: list[set[ColumnQualifier]] = []

    # Use grouping columns directly without aliases
    groupings: list[Column] = [tc.col for _, tc in raw_groupings]

    # Create aliases only for aggregation columns
    aggregations = []
    for i, (spark_name, snowpark_column, qualifiers) in enumerate(raw_aggregations):
        alias = make_column_names_snowpark_compatible([spark_name], plan_id, i)[0]

        spark_columns.append(spark_name)
        snowpark_columns.append(alias)
        snowpark_column_types.append(snowpark_column.field_type)
        all_qualifiers.append(qualifiers)

        aggregations.append(snowpark_column.col.alias(alias))

    # ROLLUP/CUBE/GROUPING_SETS introduce super-aggregate rows where grouping
    # columns are NULL, so those columns must be nullable in the output schema.
    # For ROLLUP/CUBE every grouping key is omitted in at least one grouping
    # set (the empty set), so all become nullable.  For GROUPING SETS only
    # columns missing from at least one listed set become nullable.
    all_grouping_column_names = set(grouping_columns_for_context)
    if aggregate.group_type in (
        snowflake_proto.Aggregate.GROUP_TYPE_ROLLUP,
        snowflake_proto.Aggregate.GROUP_TYPE_CUBE,
    ):
        for i, spark_name in enumerate(spark_columns):
            if spark_name in all_grouping_column_names:
                preserved_data_type = snowpark_column_types[i].datatype
                snowpark_column_types[i] = FieldType(preserved_data_type, nullable=True)

    elif aggregate.group_type == snowflake_proto.Aggregate.GROUP_TYPE_GROUPING_SETS:
        for i, spark_name in enumerate(spark_columns):
            if spark_name in all_grouping_column_names:
                missing_from_any_set = any(
                    spark_name not in gs_columns
                    for gs_columns in column_names_per_grouping_set
                )
                if missing_from_any_set:
                    preserved_data_type = snowpark_column_types[i].datatype
                    snowpark_column_types[i] = FieldType(
                        preserved_data_type, nullable=True
                    )

    match aggregate.group_type:
        case snowflake_proto.Aggregate.GROUP_TYPE_GROUPBY:
            if groupings:
                # Normal GROUP BY with explicit grouping columns
                result = input_df.group_by(groupings)
            elif not is_group_by_all:
                # No explicit GROUP BY - this is an aggregate over the entire table
                # Use a dummy constant that will be excluded from the final result
                result = input_df.with_column(
                    "__dummy_group__", snowpark_fn.lit(1)
                ).group_by("__dummy_group__")
            else:
                # GROUP BY ALL with only one aggregate column
                # Snowpark doesn't support GROUP BY ALL
                # TODO: Change in future with Snowpark Supported arguments or API for GROUP BY ALL
                result = input_df.group_by()

        case snowflake_proto.Aggregate.GROUP_TYPE_ROLLUP:
            result = input_df.rollup(groupings)
        case snowflake_proto.Aggregate.GROUP_TYPE_CUBE:
            result = input_df.cube(groupings)
        case snowflake_proto.Aggregate.GROUP_TYPE_GROUPING_SETS:
            # Map each grouping set to columns
            sets_mapped = []
            for grouping_set in aggregate.grouping_sets:
                set_cols = []
                for exp in grouping_set.grouping_set:
                    _, typed_col = map_expression(
                        exp, input_container.column_map, typer
                    )
                    set_cols.append(typed_col.col)
                sets_mapped.append(set_cols)

            result = input_df.group_by_grouping_sets(
                snowpark.GroupingSets(*sets_mapped)
            )
        case snowflake_proto.Aggregate.GROUP_TYPE_PIVOT:
            pivot_typed_columns: list[TypedColumn] = [
                map_single_column_expression(
                    pivot_col,
                    input_container.column_map,
                    ExpressionTyper(input_df),
                )[1]
                for pivot_col in aggregate.pivot.pivot_columns
            ]

            pivot_columns = [col.col for col in pivot_typed_columns]
            pivot_column_types = [col.typ for col in pivot_typed_columns]

            pivot_values: list[list[Any]] = []
            pivot_aliases: list[str] = []

            for pivot_value in aggregate.pivot.pivot_values:
                current_values = [
                    get_literal_field_and_name(val)[0] for val in pivot_value.values
                ]
                pivot_values.append(current_values)

                if pivot_value.alias:
                    pivot_aliases.append(pivot_value.alias)

            spark_col_names = []
            final_pivot_names = []
            grouping_columns_qualifiers = []
            grouping_column_types: list[FieldType] = []
            pivot_agg_column_types: list[FieldType] = []
            aggregations_pivot = []

            pivot_col_names: set[str] = {col.get_name() for col in pivot_columns}

            agg_columns = get_all_dependent_column_names(aggregations)

            input_schema_field_types = {
                f.name: FieldType(f.datatype, nullable=f.nullable)
                for f in input_df.schema.fields
            }
            raw_grouping_field_types = {
                tc.col.get_name(): input_schema_field_types.get(
                    tc.col.get_name(),
                    FieldType(tc.typ, nullable=True),
                )
                for _, tc in raw_groupings
            }

            if groupings:
                for col in groupings:
                    snowpark_name = col.get_name()
                    spark_col_name = input_container.column_map.get_spark_column_name_from_snowpark_column_name(
                        snowpark_name
                    )
                    qualifiers = (
                        input_container.column_map.get_qualifiers_for_snowpark_column(
                            snowpark_name
                        )
                    )
                    grouping_columns_qualifiers.append(qualifiers)
                    spark_col_names.append(spark_col_name)
                    grouping_column_types.append(
                        raw_grouping_field_types[snowpark_name]
                    )
            else:
                for col in input_container.column_map.columns:
                    if (
                        col.snowpark_name not in pivot_col_names
                        and col.snowpark_name not in agg_columns
                    ):
                        groupings.append(snowpark_fn.col(col.snowpark_name))
                        grouping_columns_qualifiers.append(col.qualifiers)
                        spark_col_names.append(col.spark_name)
                        grouping_column_types.append(
                            input_schema_field_types[col.snowpark_name]
                        )

            for pivot_value_idx, pivot_value_group in enumerate(pivot_values):
                pivot_values_spark_names = []
                pivot_value_is_null = []

                for val in pivot_value_group:
                    spark_name, is_null = map_pivot_value_to_spark_column_name(val)

                    pivot_values_spark_names.append(spark_name)
                    pivot_value_is_null.append(is_null)

                for agg_idx, agg_expression in enumerate(aggregations):
                    agg_fun_expr = copy.deepcopy(agg_expression._expr1)

                    condition = None
                    for pivot_col_idx, (pivot_col, pivot_val) in enumerate(
                        zip(pivot_columns, pivot_value_group)
                    ):
                        current_condition = create_pivot_column_condition(
                            pivot_col,
                            pivot_val,
                            pivot_value_is_null[pivot_col_idx],
                            pivot_column_types[pivot_col_idx]
                            if isinstance(pivot_val, (list, dict))
                            else None,
                        )

                        condition = (
                            current_condition
                            if condition is None
                            else condition & current_condition
                        )

                    inject_condition_to_all_agg_functions(agg_fun_expr, condition)
                    curr_expression = Column(agg_fun_expr)

                    if pivot_aliases and not any(pivot_value_is_null):
                        aliased_pivoted_column_spark_name = pivot_aliases[
                            pivot_value_idx
                        ]
                    elif len(pivot_values_spark_names) > 1:
                        aliased_pivoted_column_spark_name = (
                            "{" + ", ".join(pivot_values_spark_names) + "}"
                        )
                    else:
                        aliased_pivoted_column_spark_name = pivot_values_spark_names[0]

                    spark_col_name = (
                        f"{aliased_pivoted_column_spark_name}_{raw_aggregations[agg_idx][0]}"
                        if len(aggregations) > 1
                        else f"{aliased_pivoted_column_spark_name}"
                    )

                    snowpark_col_name = make_column_names_snowpark_compatible(
                        [spark_col_name],
                        plan_id,
                        len(aggregations) + len(groupings),
                    )[0]

                    curr_expression = curr_expression.alias(snowpark_col_name)

                    aggregations_pivot.append(curr_expression)
                    spark_col_names.append(spark_col_name)
                    final_pivot_names.append(snowpark_col_name)
                    pivot_agg_column_types.append(
                        FieldType(raw_aggregations[agg_idx][1].typ, nullable=True)
                    )

            result_df = input_df.group_by(*groupings).agg(*aggregations_pivot)

            return DataFrameContainer.create_with_column_mapping(
                dataframe=result_df,
                spark_column_names=spark_col_names,
                snowpark_column_names=[col.get_name() for col in groupings]
                + final_pivot_names,
                snowpark_column_types=grouping_column_types + pivot_agg_column_types,
                column_qualifiers=grouping_columns_qualifiers
                + [set() for _ in final_pivot_names],
                parent_column_name_map=input_container.column_map,
            )

        case other:
            exception = SnowparkConnectNotImplementedError(
                f"Unsupported GROUP BY type: {other}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception

    result = result.agg(*aggregations, exclude_grouping_columns=True)

    # If we added a dummy grouping column, make sure it's excluded
    if not groupings and "__dummy_group__" in result.columns:
        result = result.drop("__dummy_group__")

    # Apply HAVING condition if present
    if aggregate.HasField("having_condition"):
        from snowflake.snowpark_connect.expression.hybrid_column_map import (
            create_hybrid_column_map_for_having,
        )

        # Create aggregated DataFrame column map
        aggregated_column_map = DataFrameContainer.create_with_column_mapping(
            dataframe=result,
            spark_column_names=spark_columns,
            snowpark_column_names=snowpark_columns,
            snowpark_column_types=snowpark_column_types,
            column_qualifiers=all_qualifiers,
            equivalent_snowpark_names=[
                input_container.column_map.get_equivalent_snowpark_names_for_snowpark_name(
                    new_name
                )
                for new_name in snowpark_columns
            ],
        ).column_map

        # Create hybrid column map that can resolve both input and aggregate contexts
        hybrid_map = create_hybrid_column_map_for_having(
            input_df=input_df,
            input_column_map=input_container.column_map,
            aggregated_df=result,
            aggregated_column_map=aggregated_column_map,
            aggregate_expressions=list(aggregate.aggregate_expressions),
            grouping_expressions=list(aggregate.grouping_expressions),
            spark_columns=spark_columns,
            raw_aggregations=[
                (spark_name, col) for spark_name, col, _ in raw_aggregations
            ],
        )

        # Map the HAVING condition using hybrid resolution
        _, having_column = hybrid_map.resolve_expression(aggregate.having_condition)

        # Apply the HAVING filter
        result = result.filter(having_column.col)

    if aggregate.group_type == snowflake_proto.Aggregate.GROUP_TYPE_GROUPING_SETS:
        # Immediately drop extra columns. Unlike other GROUP BY operations,
        # grouping sets don't allow ORDER BY with columns that aren't in the aggregate list.
        result = result.select(result.columns[-len(aggregations) :])

    # Store aggregate metadata for ORDER BY resolution
    # Only for regular GROUP BY - ROLLUP, CUBE, and GROUPING_SETS should NOT allow
    # ORDER BY to reference pre-aggregation columns (Spark compatibility)
    # This enables ORDER BY to resolve expressions that reference pre-aggregation columns
    # (e.g., ORDER BY year(date) when only 'year' alias exists in aggregated result)
    aggregate_metadata = None
    if aggregate.group_type == snowflake_proto.Aggregate.GROUP_TYPE_GROUPBY:
        aggregate_metadata = AggregateMetadata(
            input_column_map=input_container.column_map,
            input_dataframe=input_df,
            grouping_expressions=list(aggregate.grouping_expressions),
            aggregate_expressions=list(aggregate.aggregate_expressions),
            spark_columns=spark_columns,
            raw_aggregations=[
                (spark_name, col) for spark_name, col, _ in raw_aggregations
            ],
        )

    # Return only aggregation columns in the column map
    return DataFrameContainer.create_with_column_mapping(
        dataframe=result,
        spark_column_names=spark_columns,
        snowpark_column_names=snowpark_columns,
        snowpark_column_types=snowpark_column_types,
        parent_column_name_map=input_container.column_map,
        column_qualifiers=all_qualifiers,
        equivalent_snowpark_names=[
            input_container.column_map.get_equivalent_snowpark_names_for_snowpark_name(
                new_name
            )
            for new_name in snowpark_columns
        ],
        aggregate_metadata=aggregate_metadata,
    )
