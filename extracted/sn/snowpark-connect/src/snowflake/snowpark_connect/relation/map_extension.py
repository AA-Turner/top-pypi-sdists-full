#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import copy
from typing import Any

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
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.utils import (
    create_pivot_column_condition,
    get_all_dependent_column_names,
    map_pivot_value_to_spark_column_name,
)
from snowflake.snowpark_connect.typed_column import TypedColumn
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
            func = snowpark_fn.udf(
                pkl.loads(rdd_map.func),
                return_type=return_type,
                input_types=[input_type],
                name="my_udf",
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
            return DataFrameContainer.create_with_column_mapping(
                dataframe=input_df,
                spark_column_names=subquery_aliases.aliases,
                snowpark_column_names=snowpark_col_names,
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
        case other:
            exception = SnowparkConnectNotImplementedError(
                f"Unexpected extension {other}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception


def get_udtf_project(relation: relation_proto.Relation) -> bool:
    """
    Extract UDTF information from a relation if it's a project containing a UDTF call.

    Returns:
        tuple[udtf_obj, udtf_spark_output_names] if UDTF found, None otherwise
    """
    if relation.WhichOneof("rel_type") == "project":
        expressions = relation.project.expressions
        if (
            len(expressions) == 1
            and expressions[0].WhichOneof("expr_type") == "unresolved_function"
        ):
            session = snowpark.Session.get_active_session()
            func = expressions[0].unresolved_function
            udtf_name_lower = func.function_name.lower()
            if udtf_name_lower in session._udtfs:
                return session._udtfs[udtf_name_lower]

    return None


def handle_udtf_with_table_arguments(
    udtf_info: snowflake_proto.UDTFWithTableArguments,
) -> DataFrameContainer:
    """
    Handle UDTF with one or more table arguments using Snowpark's join_table_function.
    For multiple table arguments, this creates a Cartesian product of all input tables.
    """
    session = snowpark.Session.get_active_session()
    udtf_name_lower = udtf_info.function_name.lower()
    if udtf_name_lower not in session._udtfs:
        exception = ValueError(f"UDTF '{udtf_info.function_name}' not found.")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception
    _udtf_obj, udtf_spark_output_names = session._udtfs[udtf_name_lower]

    table_containers = []
    for table_arg_info in udtf_info.table_arguments:
        result = map_relation(table_arg_info.table_argument)
        table_containers.append((result, table_arg_info.table_argument_idx))

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

    scalar_args = []
    typer = ExpressionTyper.dummy_typer(session)
    empty_column_map = ColumnNameMap([], [], None)
    for arg_proto in udtf_info.arguments:
        # UDTF when used with table arguments, the arguments can only be scalar arguments like integer, literals etc. or Table arguments.
        # Using map_expression with dummy typer to resolve the scalar arguments.
        _, typed_column = map_expression(arg_proto, empty_column_map, typer)
        scalar_args.append(typed_column.col)

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

    scalar_args_variant = [snowpark_fn.to_variant(arg) for arg in scalar_args]

    all_args = scalar_args_variant.copy()
    for table_arg_variant, table_arg_idx in sorted(
        table_arg_variants, key=lambda x: x[1]
    ):
        all_args.insert(table_arg_idx, table_arg_variant)

    udtf_func = snowpark_fn.table_function(_udtf_obj.name)
    result_df = base_df.join_table_function(udtf_func(*all_args))

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
    udtf_info: tuple[snowpark.udtf.UserDefinedTableFunction, list],
) -> DataFrameContainer:
    """
    Handle lateral join with UDTF on the right side using join_table_function.
    """
    session = snowpark.Session.get_active_session()

    project = udtf_relation.project
    udtf_func = project.expressions[0].unresolved_function
    _udtf_obj, udtf_spark_output_names = udtf_info

    typer = ExpressionTyper.dummy_typer(session)
    left_column_map = left_result.column_map
    left_df = left_result.dataframe
    table_func = snowpark_fn.table_function(_udtf_obj.name)
    udtf_args = [
        map_expression(arg_proto, left_column_map, typer)[1].col
        for arg_proto in udtf_func.arguments
    ]
    udtf_args_variant = [snowpark_fn.to_variant(arg) for arg in udtf_args]
    result_df = left_df.join_table_function(table_func(*udtf_args_variant))

    return DataFrameContainer.create_with_column_mapping(
        dataframe=result_df,
        spark_column_names=left_result.column_map.get_spark_columns()
        + udtf_spark_output_names,
        snowpark_column_names=result_df.columns,
        column_qualifiers=left_result.column_map.get_qualifiers()
        + [set() for _ in udtf_spark_output_names],
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

    def _map_column(exp: expression_proto.Expression) -> tuple[str, TypedColumn]:
        new_names, snowpark_column = map_expression(
            exp, input_container.column_map, typer
        )
        if len(new_names) != 1:
            exception = SnowparkConnectNotImplementedError(
                "Multi-column aggregate expressions are not supported"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        return new_names[0], snowpark_column

    raw_groupings: list[tuple[str, TypedColumn]] = []
    raw_aggregations: list[tuple[str, TypedColumn, set[ColumnQualifier]]] = []

    if not is_group_by_all:
        raw_groupings = [_map_column(exp) for exp in aggregate.grouping_expressions]

    # Determine grouping columns for context
    # For GROUPING SETS, we need to extract the columns from the sets
    grouping_columns_for_context = []
    if aggregate.group_type == snowflake_proto.Aggregate.GROUP_TYPE_GROUPING_SETS:
        # Use a list to preserve order, avoiding duplicates
        for grouping_set in aggregate.grouping_sets:
            for exp in grouping_set.grouping_set:
                spark_names, _ = map_expression(exp, input_container.column_map, typer)
                # map_expression always returns a list, get the first element
                col_name = spark_names[0]
                if col_name not in grouping_columns_for_context:
                    grouping_columns_for_context.append(col_name)
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
        col = _map_column(exp)
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
            spark_name, snowpark_column = col

            # Register the alias pointing to the result of its expression
            # This handles both simple aliases (k as lca) and complex ones (lca + 1 as col)
            # The snowpark_column already contains the computed expression with its alias wrapper,
            # which is fine - when referenced later, the column's value is what gets used
            register_lca_alias(alias_name, snowpark_column)

        if is_group_by_all:
            new_agg_count = get_sql_aggregate_function_count()
            if new_agg_count == agg_count:
                raw_groupings.append(col)
            else:
                agg_count = new_agg_count

    # Now create column name lists and assign aliases.
    # In case of GROUP BY ALL, even though groupings are a subset of aggregations,
    # they will have their own aliases so we can drop them later.

    spark_columns: list[str] = []
    snowpark_columns: list[str] = []
    snowpark_column_types: list[snowpark_types.DataType] = []
    all_qualifiers: list[set[ColumnQualifier]] = []

    # Use grouping columns directly without aliases
    groupings: list[Column] = [tc.col for _, tc in raw_groupings]

    # Create aliases only for aggregation columns
    aggregations = []
    for i, (spark_name, snowpark_column, qualifiers) in enumerate(raw_aggregations):
        alias = make_column_names_snowpark_compatible([spark_name], plan_id, i)[0]

        spark_columns.append(spark_name)
        snowpark_columns.append(alias)
        snowpark_column_types.append(snowpark_column.typ)
        all_qualifiers.append(qualifiers)

        aggregations.append(snowpark_column.col.alias(alias))

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
            aggregations_pivot = []

            pivot_col_names: set[str] = {col.get_name() for col in pivot_columns}

            agg_columns = get_all_dependent_column_names(aggregations)

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
            else:
                for col in input_container.column_map.columns:
                    if (
                        col.snowpark_name not in pivot_col_names
                        and col.snowpark_name not in agg_columns
                    ):
                        groupings.append(snowpark_fn.col(col.snowpark_name))
                        grouping_columns_qualifiers.append(col.qualifiers)
                        spark_col_names.append(col.spark_name)

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

            result_df = input_df.group_by(*groupings).agg(*aggregations_pivot)

            return DataFrameContainer.create_with_column_mapping(
                dataframe=result_df,
                spark_column_names=spark_col_names,
                snowpark_column_names=result_df.columns,
                snowpark_column_types=[
                    result_df.schema.fields[idx].datatype
                    for idx, _ in enumerate(result_df.columns)
                ],
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
