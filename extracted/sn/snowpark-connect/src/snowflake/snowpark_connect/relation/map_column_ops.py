#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import ast
import json
import sys
from collections import defaultdict

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
import pyspark.sql.connect.proto.relations_pb2 as relation_proto
import pyspark.sql.connect.proto.types_pb2 as types_proto
from pyspark.errors.exceptions.base import AnalysisException
from pyspark.serializers import CloudPickleSerializer

import snowflake.snowpark.functions as snowpark_fn
import snowflake.snowpark.types as snowpark_types
from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark._internal.analyzer.expression import (
    Attribute,
    NamedExpression,
    UnresolvedAttribute,
)

# These internal util functions and classes are unlikely to change in Snowpark, so importing them directly
from snowflake.snowpark._internal.utils import generate_random_alphanumeric
from snowflake.snowpark.column import Column
from snowflake.snowpark.table_function import _ExplodeFunctionCall
from snowflake.snowpark.types import DataType, StructField, StructType, _NumericType
from snowflake.snowpark_connect import tcm
from snowflake.snowpark_connect.column_name_handler import (
    ColumnNameMap,
    ColumnQualifier,
    make_column_names_snowpark_compatible,
    make_unique_snowpark_name,
)
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import (
    SparkException,
    attach_custom_error_code,
)
from snowflake.snowpark_connect.expression.map_expression import (
    map_alias,
    map_expression,
    map_single_column_expression,
)
from snowflake.snowpark_connect.expression.map_unresolved_function import unwrap_literal
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.output_struct_utils import (
    unpack_struct_output_to_container,
)
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    without_internal_columns,
)
from snowflake.snowpark_connect.relation.utils import (
    TYPE_MAP_FOR_TO_SCHEMA,
    snowpark_functions_col,
)
from snowflake.snowpark_connect.type_mapping import (
    map_snowpark_to_pyspark_types,
    proto_to_snowpark_type,
)
from snowflake.snowpark_connect.typed_column import TypedColumn
from snowflake.snowpark_connect.utils import context
from snowflake.snowpark_connect.utils.context import (
    clear_lca_alias_map,
    register_lca_alias,
)
from snowflake.snowpark_connect.utils.expression_transformer import (
    is_child_agg_function_expression,
)
from snowflake.snowpark_connect.utils.identifiers import (
    split_fully_qualified_spark_name,
)
from snowflake.snowpark_connect.utils.udtf_helper import (
    TEST_FLAG_FORCE_CREATE_SPROC,
    create_apply_udtf_in_sproc,
)


def map_drop(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Drop columns from a DataFrame.

    The drop is a list of expressions that is applied to the DataFrame.
    """
    input_container = map_relation(rel.drop.input).without_hidden_columns()
    input_df = input_container.dataframe
    typer = ExpressionTyper(input_df)
    columns_to_drop_with_names = []
    for exp in rel.drop.columns:
        if exp.WhichOneof("expr_type") == "unresolved_attribute":
            try:
                columns_to_drop_with_names.append(
                    map_single_column_expression(exp, input_container.column_map, typer)
                )
            except AnalysisException as e:
                if "[COLUMN_NOT_FOUND]" in e.message:
                    pass  # Ignore columns that are not found
                else:
                    raise
    columns_to_drop: list[Column] = [
        col[1].col for col in columns_to_drop_with_names
    ] + [
        snowpark_functions_col(c, input_container.column_map)
        for c in input_container.column_map.get_snowpark_column_names_from_spark_column_names(
            list(rel.drop.column_names)
        )
        if c is not None
    ]
    # Sometimes we get a drop query with only invalid names. In this case, we return
    # the input DataFrame.
    if len(columns_to_drop) == 0:
        return input_container

    def _get_column_names_to_drop() -> list[str]:
        # more or less copied from Snowpark's DataFrame::drop
        names = []
        for c in columns_to_drop:
            if isinstance(c._expression, Attribute):
                names.append(
                    input_df._plan.expr_to_alias.get(
                        c._expression.expr_id, c._expression.name
                    )
                )
            elif (
                isinstance(c._expression, UnresolvedAttribute)
                and c._expression.df_alias
            ):
                names.append(
                    input_df.self._plan.df_aliased_col_name_to_real_col_name.get(
                        c._expression.name, c._expression.name
                    )
                )
            elif isinstance(c._expression, NamedExpression):
                names.append(c._expression.name)
        return names

    column_map = input_container.column_map
    new_columns = column_map.get_snowpark_columns_after_drop(
        _get_column_names_to_drop()
    )

    if len(new_columns) == 0:
        # Snowpark doesn't allow dropping all columns, so we have to handle this with
        # a custom "empty" dataframe. The projection is to maintain the exact rowcount.
        empty_df = input_df.select(snowpark_fn.lit(None).alias("__DUMMY"))
        return DataFrameContainer.create_with_column_mapping(
            dataframe=empty_df,
            spark_column_names=["__DUMMY"],
            snowpark_column_names=["__DUMMY"],
            parent_column_name_map=column_map,
            column_is_hidden=[True],
        )

    result: snowpark.DataFrame = input_df.drop(*columns_to_drop)
    return DataFrameContainer.create_with_column_mapping(
        dataframe=result,
        spark_column_names=[c.spark_name for c in new_columns],
        snowpark_column_names=[c.snowpark_name for c in new_columns],
        column_qualifiers=[c.qualifiers for c in new_columns],
        parent_column_name_map=column_map,
        equivalent_snowpark_names=[c.equivalent_snowpark_names for c in new_columns],
    )


def map_project(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Project column(s) and return a container.

    Projections come in as expressions, which are mapped to `snowpark.Column` objects.
    """
    if rel.project.HasField("input"):
        input_container = map_relation(rel.project.input)
    else:
        # Create a dataframe to represent a OneRowRelation AST node.
        # XXX: Snowflake does not support 0-column tables, so create a dummy column;
        # its name does not seem to show up anywhere.
        session = snowpark.Session.get_active_session()
        input_container = DataFrameContainer.create_with_column_mapping(
            dataframe=session.create_dataframe([None], ["__DUMMY"]),
            spark_column_names=["__DUMMY"],
            snowpark_column_names=["__DUMMY"],
            column_is_hidden=[True],
        )

    input_df = input_container.dataframe
    context.set_df_before_projection(input_container)
    expressions: list[expressions_proto.Expression] = rel.project.expressions
    if not expressions:
        # XXX: Snowflake does not support 0-column tables, so create a dummy column;
        # its name will unforunately be user-visible.
        expressions = [
            expressions_proto.Expression(
                alias=expressions_proto.Expression.Alias(
                    expr=expressions_proto.Expression(
                        literal=expressions_proto.Expression.Literal(
                            null=types_proto.DataType(null=types_proto.DataType.NULL())
                        )
                    ),
                    name=[""],
                ),
            )
        ]

    select_list = []
    new_spark_columns = []
    new_snowpark_columns = []

    # LCA Support: build DataFrame progressively to allow later expressions to reference earlier aliases
    clear_lca_alias_map()

    # Collect aliases to batch process them
    pending_aliases = []  # List of (spark_name, snowpark_col, aliased_col, alias_types)
    # Track columns that might need aliasing if multi-column generators are present
    # Format: (index_in_select_list, snowpark_column_name, mapper.col)
    conditional_aliases = []

    def _is_attribute(exp: expressions_proto.Expression) -> bool:
        return exp.WhichOneof("expr_type") == "unresolved_attribute"

    # Detect if this is a simple projection (only unqualified column references, no aliases or functions)
    # Qualified column references (with plan_id) should NOT be considered simple projections
    # because they've already been resolved to specific DataFrames
    def _is_simple_projection(exp: expressions_proto.Expression) -> bool:
        return _is_attribute(exp) and not exp.unresolved_attribute.HasField(
            "plan_id"
        )  # No DataFrame qualification

    has_agg_in_input_df = (
        input_df._select_statement
        and input_df._select_statement.projection
        and any(
            is_child_agg_function_expression(exp)
            for exp in input_df._select_statement.projection
        )
    )
    column_types = []
    has_multi_column_alias = False
    qualifiers: list[set[ColumnQualifier]] = []
    equivalent_snowpark_names: list[set[str]] = []

    typer = ExpressionTyper(input_df)

    has_unresolved_star = any(
        exp.WhichOneof("expr_type") == "unresolved_star" for exp in expressions
    )

    for exp in expressions:
        new_spark_names, mapper = map_expression(exp, input_container.column_map, typer)
        if len(new_spark_names) == 1 and not isinstance(
            mapper.col, _ExplodeFunctionCall
        ):
            # For simple projections of existing columns, try to preserve the original Snowpark names
            # But only for truly unqualified column references, not for qualified ones like df.column
            spark_name = new_spark_names[0]

            # Check if this was a qualified column reference (like df_alias.column)
            # by checking if the original expression was an alias lookup
            is_qualified_reference = (
                _is_attribute(exp)
                and "." in exp.unresolved_attribute.unparsed_identifier
            )

            existing_snowpark_name = None
            if (
                _is_simple_projection(exp)
                and not is_qualified_reference
                and not has_unresolved_star
            ):
                # Try to get the existing Snowpark column name for this Spark column
                existing_snowpark_name = input_container.column_map.get_snowpark_column_name_from_spark_column_name(
                    spark_name, allow_non_exists=True
                )

                # Only preserve if we found a unique existing name and it's not already used
                if (
                    existing_snowpark_name is not None
                    and existing_snowpark_name not in new_snowpark_columns
                ):
                    snowpark_column = existing_snowpark_name
                else:
                    # Generate new name if we can't preserve
                    snowpark_column = make_column_names_snowpark_compatible(
                        [spark_name], rel.common.plan_id, len(new_snowpark_columns)
                    )[0]
            else:
                # Not a simple projection or is a qualified reference - generate new names
                snowpark_column = make_column_names_snowpark_compatible(
                    [spark_name], rel.common.plan_id, len(new_snowpark_columns)
                )[0]

            # since unresolved attributes get aliased, we need to retain their original name
            # so that we're able to resolve it later
            if (
                _is_attribute(exp)
                and mapper.col.get_name()
                and mapper.col.get_name() not in new_snowpark_columns
            ):
                old_name = mapper.col.get_name()
                eq_names = set()
                eq_names.update(
                    input_container.column_map.get_equivalent_snowpark_names_for_snowpark_name(
                        old_name
                    )
                )
                if old_name != snowpark_column:
                    eq_names.update({old_name})
                equivalent_snowpark_names.append(eq_names)
            else:
                equivalent_snowpark_names.append(set())

            # TODO: go back to using alias always once SNOW-2203826 is done
            if existing_snowpark_name == snowpark_column and not has_agg_in_input_df:
                aliased_col = mapper.col
                # Store info to potentially re-alias later if multi-column generators appear
                conditional_aliases.append(
                    (len(select_list), snowpark_column, mapper.col)
                )
            else:
                aliased_col = mapper.col.alias(snowpark_column)

            select_list.append(aliased_col)
            new_snowpark_columns.append(snowpark_column)
            new_spark_columns.append(spark_name)
            column_types.extend(mapper.types)
            qualifiers.append(mapper.get_qualifiers())

            # Only update the DataFrame and register LCA for explicit aliases
            if (
                exp.WhichOneof("expr_type") == "alias"
                and not context.is_resolving_subquery_exp()
            ):
                # Collect alias for batch processing
                pending_aliases.append(
                    (spark_name, snowpark_column, aliased_col, mapper.types)
                )

                # Register in LCA map immediately so subsequent expressions can resolve it
                alias_types = mapper.types
                typed_alias = TypedColumn(aliased_col, lambda types=alias_types: types)
                register_lca_alias(spark_name, typed_alias)

                # Also register with the original qualified name if this is an alias of a column reference
                # This handles ORDER BY referencing the original name: SELECT o.date AS order_date ... ORDER BY o.date
                if (
                    exp.alias.HasField("expr")
                    and exp.alias.expr.WhichOneof("expr_type") == "unresolved_attribute"
                ):
                    original_name = (
                        exp.alias.expr.unresolved_attribute.unparsed_identifier
                    )
                    if (
                        original_name != spark_name
                    ):  # Don't register twice with the same name
                        register_lca_alias(original_name, typed_alias)
        elif len(new_spark_names) > 0:
            # Multi-column case ('select *', posexplode, explode, inline, etc.)
            has_multi_column_alias = True
            select_list.append(mapper.col)
            result_columns = input_df.select(mapper.col).columns
            new_snowpark_columns.extend(result_columns)
            new_spark_columns.extend(new_spark_names)
            column_types.extend(mapper.types)
            qualifiers.extend(mapper.get_multi_col_qualifiers(len(new_spark_names)))
            equivalent_snowpark_names.extend(
                [
                    input_container.column_map.get_equivalent_snowpark_names_for_snowpark_name(
                        snowpark_name
                    )
                    for snowpark_name in result_columns
                ]
            )

    # TODO: go back to using alias always once SNOW-2203826 is done
    # If we have multi-column aliases, we need to ensure ALL columns are aliased
    # to avoid Snowpark SQL generation issues
    if has_multi_column_alias and conditional_aliases:
        for idx, snowpark_col_name, col_obj in conditional_aliases:
            select_list[idx] = col_obj.alias(snowpark_col_name)

    if len(select_list) == 0:
        # we've produced a 0-column df, likely because the input was 0-column
        empty_df = input_df.select(snowpark_fn.lit(None).alias("__DUMMY"))
        return DataFrameContainer.create_with_column_mapping(
            dataframe=empty_df,
            spark_column_names=["__DUMMY"],
            snowpark_column_names=["__DUMMY"],
            parent_column_name_map=input_container.column_map,
            column_is_hidden=[True],
        )

    if pending_aliases:
        # LCA case: create intermediate DataFrame with aliases, then do final projection
        # pending_aliases contains (spark_name, snowpark_column, aliased_col, mapper.types)
        old_cols = [alias[1] for alias in pending_aliases]
        new_cols = [alias[2] for alias in pending_aliases]

        intermediate_df = input_df.with_columns(old_cols, new_cols)

        result = intermediate_df.select(*select_list)
    else:
        result = input_df.select(*select_list)

    # Apply toDF renaming for multi-column aliasing
    if has_multi_column_alias:
        # Generate snowpark-compatible column names for multi-column aliases
        final_snowpark_columns = make_column_names_snowpark_compatible(
            new_spark_columns, rel.common.plan_id
        )
        # if there are duplicate snowpark column names, we need to disambiguate them by their index
        if len(new_spark_columns) != len(set(new_spark_columns)):
            result = result.select(
                [f"${i}" for i in range(1, len(new_spark_columns) + 1)]
            )
        result = result.toDF(*final_snowpark_columns)
        new_snowpark_columns = final_snowpark_columns

    return DataFrameContainer.create_with_column_mapping(
        dataframe=result,
        spark_column_names=new_spark_columns,
        snowpark_column_names=new_snowpark_columns,
        snowpark_column_types=column_types,
        column_metadata=input_container.column_map.column_metadata,
        column_qualifiers=qualifiers,
        parent_column_name_map=input_container.column_map,
        table_name=input_container.table_name,
        alias=input_container.alias,
        equivalent_snowpark_names=equivalent_snowpark_names,
    )


def map_sort(
    sort: relation_proto.Sort,
) -> DataFrameContainer:
    """
    Implements DataFrame.sort() and return a container.

    """
    input_container = map_relation(sort.input)
    input_df = input_container.dataframe
    cols = []
    ascending = []  # Ignored if all order values are set to "unspecified".
    order_specified = False
    typer = ExpressionTyper(input_df)

    sort_order = sort.order

    if len(sort_order) == 1:
        parsed_col_name = split_fully_qualified_spark_name(
            sort_order[0].child.unresolved_attribute.unparsed_identifier
        )
        if (
            len(parsed_col_name) == 1
            and parsed_col_name[0].lower() == "all"
            and input_container.column_map.get_snowpark_column_name_from_spark_column_name(
                parsed_col_name[0], allow_non_exists=True
            )
            is None
        ):
            # A single column with the name "all" needs to be expanded to all input columns.
            sort_order = [
                expressions_proto.Expression.SortOrder(
                    child=expressions_proto.Expression(
                        unresolved_attribute=expressions_proto.Expression.UnresolvedAttribute(
                            unparsed_identifier=col
                        )
                    ),
                    direction=sort_order[0].direction,
                    null_ordering=sort_order[0].null_ordering,
                )
                for col in input_container.column_map.get_spark_columns()
            ]

    # Process ORDER BY expressions with a context flag to enable column reuse optimization
    from snowflake.snowpark_connect.utils.context import push_processing_order_by_scope

    with push_processing_order_by_scope():
        for so in sort_order:
            if so.child.HasField("literal"):
                column_index = unwrap_literal(so.child)
                try:
                    if column_index <= 0:
                        exception = IndexError()
                        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                        raise exception
                    col = input_df[column_index - 1]
                except IndexError:
                    exception = AnalysisException(
                        f"""[ORDER_BY_POS_OUT_OF_RANGE] ORDER BY position {column_index} is not in select list (valid range is [1, {len(input_df.columns)})])."""
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception
            else:
                # Check if input came from an aggregate - if so, use hybrid resolution
                # This handles ORDER BY expressions that reference pre-aggregation columns
                # e.g., ORDER BY year(date) when the aggregated result only has 'year' alias
                if (
                    hasattr(input_container, "_aggregate_metadata")
                    and input_container._aggregate_metadata is not None
                ):
                    from snowflake.snowpark_connect.expression.hybrid_column_map import (
                        create_hybrid_column_map_for_order_by,
                    )

                    # Create hybrid map for resolving ORDER BY expressions
                    hybrid_map = create_hybrid_column_map_for_order_by(
                        aggregate_metadata=input_container._aggregate_metadata,
                        aggregated_df=input_df,
                        aggregated_column_map=input_container.column_map,
                    )

                    # Resolve using hybrid context (can access both input and aggregated columns)
                    _, typed_column = hybrid_map.resolve_expression(so.child)
                    col = typed_column.col
                else:
                    # Normal resolution for non-aggregate inputs
                    _, typed_column = map_single_column_expression(
                        so.child, input_container.column_map, typer
                    )
                    col = typed_column.col

            match (so.direction, so.null_ordering):
                case (
                    expressions_proto.Expression.SortOrder.SORT_DIRECTION_ASCENDING,
                    expressions_proto.Expression.SortOrder.SORT_NULLS_FIRST,
                ):
                    col = col.asc_nulls_first()
                case (
                    expressions_proto.Expression.SortOrder.SORT_DIRECTION_ASCENDING,
                    expressions_proto.Expression.SortOrder.SORT_NULLS_LAST,
                ):
                    col = col.asc_nulls_last()
                case (
                    expressions_proto.Expression.SortOrder.SORT_DIRECTION_DESCENDING,
                    expressions_proto.Expression.SortOrder.SORT_NULLS_FIRST,
                ):
                    col = col.desc_nulls_first()
                case (
                    expressions_proto.Expression.SortOrder.SORT_DIRECTION_DESCENDING,
                    expressions_proto.Expression.SortOrder.SORT_NULLS_LAST,
                ):
                    col = col.desc_nulls_last()

            cols.append(col)

            ascending.append(
                so.direction
                == expressions_proto.Expression.SortOrder.SORT_DIRECTION_ASCENDING
            )
            if (
                so.direction
                != expressions_proto.Expression.SortOrder.SORT_DIRECTION_UNSPECIFIED
            ):
                order_specified = True

    # TODO: sort.isglobal.
    if not order_specified:
        ascending = None

    result = input_df.sort(cols, ascending=ascending)

    return DataFrameContainer(
        result,
        input_container.column_map,
        input_container.table_name,
        cached_schema_getter=lambda: input_df.schema,
    )


def map_to_df(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Transform the column names of the input DataFrame and return a container.
    """
    input_container = without_internal_columns(map_relation(rel.to_df.input))
    input_df = input_container.dataframe

    new_column_names = list(rel.to_df.column_names)
    if len(new_column_names) != len(input_container.column_map.columns):
        # TODO: Check error type here
        exception = ValueError(
            "Number of column names must match number of columns in DataFrame"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
        raise exception
    snowpark_new_column_names = make_column_names_snowpark_compatible(
        new_column_names, rel.common.plan_id
    )
    result = input_df.toDF(*snowpark_new_column_names)

    if result._select_statement is not None:
        # do not allow snowpark to flatten the to_df result
        # TODO: remove after SNOW-2203706 is fixed
        result._select_statement.flatten_disabled = True

    def _get_schema():
        return StructType(
            [
                StructField(n, f.datatype, _is_column=False)
                for n, f in zip(snowpark_new_column_names, input_df.schema.fields)
            ]
        )

    result_container = DataFrameContainer.create_with_column_mapping(
        dataframe=result,
        spark_column_names=new_column_names,
        snowpark_column_names=snowpark_new_column_names,
        parent_column_name_map=input_container.column_map,
        table_name=input_container.table_name,
        alias=input_container.alias,
        cached_schema_getter=_get_schema,
        equivalent_snowpark_names=[set()] * len(new_column_names),
    )
    context.set_df_before_projection(result_container)
    return result_container


def map_to_schema(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Transform the column names of the input DataFrame.
    """
    input_container = map_relation(rel.to_schema.input)
    input_df = input_container.dataframe
    new_column_names = [field.name for field in rel.to_schema.schema.struct.fields]
    snowpark_new_column_names = make_column_names_snowpark_compatible(
        new_column_names, rel.common.plan_id
    )
    count_case_insensitive_column_names = defaultdict()
    for key, value in input_container.column_map.spark_to_col.items():
        count_case_insensitive_column_names[
            key.lower()
        ] = count_case_insensitive_column_names.get(key.lower(), 0) + len(value)
    already_existing_columns = [
        column
        for column in new_column_names
        if column.lower() in count_case_insensitive_column_names
    ]
    # If we update the schema of the fields to change the nullable field, we need to check if it's valid or not
    # This only concerns the case of going from nullable = False -> nullable = True and will raise an AnalysisException
    for field in rel.to_schema.schema.struct.fields:
        if field.name in already_existing_columns:
            if count_case_insensitive_column_names[field.name.lower()] > 1:
                exception = AnalysisException(
                    f"[AMBIGUOUS_COLUMN_OR_FIELD] Column or field `{field.name}` is ambiguous and has {len(input_container.column_map.spark_to_col[field.name])} matches."
                )
                attach_custom_error_code(exception, ErrorCodes.AMBIGUOUS_COLUMN_NAME)
                raise exception
            snowpark_name = None
            for name in input_container.column_map.spark_to_col:
                if name.lower() == field.name.lower():
                    snowpark_name = input_container.column_map.spark_to_col[name][
                        0
                    ].snowpark_name
                    break
            # Check nullable and type casting validation
            for snowpark_field in input_df.schema.fields:
                if snowpark_field.name == snowpark_name:
                    # PySpark allows nullable to non-nullable conversion for StructType.
                    if (
                        not field.nullable
                        and snowpark_field.nullable
                        and not isinstance(snowpark_field.datatype, StructType)
                    ):
                        exception = AnalysisException(
                            f"[NULLABLE_COLUMN_OR_FIELD] Column or field `{field.name}` is nullable while it's required to be non-nullable."
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.INVALID_OPERATION
                        )
                        raise exception

                    # Check type casting validation
                    if not _can_cast_column_in_schema(
                        snowpark_field.datatype, proto_to_snowpark_type(field.data_type)
                    ):
                        exception = AnalysisException(
                            f"""[INVALID_COLUMN_OR_FIELD_DATA_TYPE] Column or field `{field.name}` is of type "{map_snowpark_to_pyspark_types(proto_to_snowpark_type(field.data_type))}" while it's required to be "{map_snowpark_to_pyspark_types(snowpark_field.datatype)}"."""
                        )
                        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                        raise exception
    if len(already_existing_columns) == len(new_column_names):
        # All columns already exist, we're doing a simple update.
        snowpark_new_column_names = []
        for column in new_column_names:
            for name in input_container.column_map.spark_to_col:
                if name.lower() == column.lower():
                    snowpark_new_column_names.append(
                        input_container.column_map.spark_to_col[name][0].snowpark_name
                    )
        result = input_df
    elif len(already_existing_columns) == 0:
        # All schema columns are new, drop all old columns and add the new ones.
        new_columns = [
            snowpark_fn.lit(None).alias(column_name)
            for column_name in snowpark_new_column_names
        ]
        result = input_df.select(*new_columns)
    else:
        # Some columns already exist, some columns are new.
        columns_to_add = []
        # This list is created to preserve ordering
        new_snowpark_new_column_names = []
        for spark_column, snowpark_column in zip(
            new_column_names, snowpark_new_column_names
        ):
            # If the column doesn't already exist, append the new Snowpark name to columns_to_add
            if all(
                spark_column.lower() != name.lower()
                for name in input_container.column_map.spark_to_col
            ):
                columns_to_add.append(snowpark_column)
                new_snowpark_new_column_names.append(snowpark_column)
            else:
                for name in input_container.column_map.spark_to_col:
                    # If the column does exist, append the original Snowpark name, We don't need to add this column.
                    if name.lower() == spark_column.lower():
                        new_snowpark_new_column_names.append(
                            input_container.column_map.spark_to_col[name][
                                0
                            ].snowpark_name
                        )
        # Add all columns introduced by the new schema.
        new_columns = [
            (
                snowpark_fn.lit(None).alias(column_name)
                if column_name in columns_to_add
                else column_name
            )
            for column_name in new_snowpark_new_column_names
        ]
        result = input_df.select(*new_columns)
        snowpark_new_column_names = new_snowpark_new_column_names
    new_schema = rel.to_schema.schema
    snowpark_schema: snowpark.types.StructType = proto_to_snowpark_type(new_schema)
    result_with_casting = result.select(
        *[
            snowpark_fn.cast(col_name, snowpark_field.datatype).as_(col_name)
            for col_name, snowpark_field in zip(
                snowpark_new_column_names, snowpark_schema.fields
            )
        ]
    )
    column_metadata = {}
    for field in rel.to_schema.schema.struct.fields:
        if field.metadata:
            try:
                column_metadata[field.name] = ast.literal_eval(field.metadata)
            except (ValueError, SyntaxError):
                column_metadata[field.name] = None
        else:
            column_metadata[field.name] = None
    return DataFrameContainer.create_with_column_mapping(
        dataframe=result_with_casting,
        spark_column_names=new_column_names,
        snowpark_column_names=snowpark_new_column_names,
        snowpark_column_types=[field.datatype for field in snowpark_schema.fields],
        column_metadata=column_metadata,
        parent_column_name_map=input_container.column_map,
        equivalent_snowpark_names=[set()] * len(new_column_names),
    )


def map_with_columns_renamed(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Rename columns in a DataFrame and return a container.
    """
    input_container = without_internal_columns(
        map_relation(rel.with_columns_renamed.input)
    )
    input_df = input_container.dataframe
    rename_columns_map = dict(rel.with_columns_renamed.rename_columns_map)

    if not global_config.spark_sql_caseSensitive:
        # store it as lower case to avoid case sensitivity issues.
        rename_columns_map_original = {}
        for k, v in rename_columns_map.items():
            rename_columns_map_original[k.lower()] = k
            rename_columns_map_original[v.lower()] = v
        rename_columns_map = {
            k.lower(): v.lower() for k, v in rename_columns_map.items()
        }

    column_map = input_container.column_map

    # re-construct the rename chains based on the input dataframe.
    if input_container.column_map.rename_chains:
        for key, value in input_container.column_map.rename_chains.items():
            if key in rename_columns_map:
                # This is to handle the case where the same column is renamed multiple times.
                # df.withColumnRenamed("a", "b").withColumnRenamed("a", "c")
                # the result rename chain should be {"a" -> "c", "b" -> "c"}
                latest_name = rename_columns_map[key]
                rename_columns_map[key] = latest_name
                rename_columns_map[value] = latest_name
            elif value in rename_columns_map:
                # This is to update historic rename chain.
                # df.withColumnRenamed("a", "b").withColumnRenamed("b", "c")
                # The rename chain "a" -> "b" should be updated to "a" -> "c" as b was renamed to c in the second rename.
                # final rename chain should be {"a" -> "c", "b" -> "c"}
                rename_columns_map[key] = rename_columns_map[value]
            else:
                # This just copies the renames from previous computed dataframe
                rename_columns_map[key] = value

    def _column_exists_error(name: str) -> AnalysisException:
        return AnalysisException(
            f"[COLUMN_ALREADY_EXISTS] The column `{name}` already exists. Consider to choose another name or rename the existing column."
        )

    # Validate for naming conflicts
    rename_map = dict(rel.with_columns_renamed.rename_columns_map)
    new_names_list = list(rename_map.values())
    seen = set()
    for new_name in new_names_list:
        # Check if this new name conflicts with existing columns
        # But allow renaming a column to a different case version of itself
        is_case_insensitive_self_rename = False
        if not global_config.spark_sql_caseSensitive:
            # Find the source column(s) that map to this new name
            source_columns = [
                old_name
                for old_name, new_name_candidate in rename_map.items()
                if new_name_candidate == new_name
            ]
            # Check if any source column is the same as new name when case-insensitive
            is_case_insensitive_self_rename = any(
                source_col.lower() == new_name.lower() for source_col in source_columns
            )

        if (
            column_map.has_spark_column(new_name)
            and not is_case_insensitive_self_rename
        ):
            # Spark doesn't allow reusing existing names, even if the result df will not contain duplicate columns
            raise _column_exists_error(new_name)
        if (global_config.spark_sql_caseSensitive and new_name in seen) or (
            not global_config.spark_sql_caseSensitive
            and new_name.lower() in [s.lower() for s in seen]
        ):
            raise _column_exists_error(new_name)
        seen.add(new_name)

    new_spark_names = []
    new_snowpark_names = []
    qualifiers = []
    equivalent_snowpark_names = []
    for c in column_map.columns:
        spark_name = c.spark_name
        new_spark_name = None
        if global_config.spark_sql_caseSensitive:
            new_spark_name = rename_columns_map.get(spark_name, None)
        elif rename_columns_map.get(spark_name.lower(), None) is not None:
            new_spark_name = rename_columns_map_original.get(
                rename_columns_map.get(spark_name.lower())
            )

        if new_spark_name:
            new_spark_names.append(new_spark_name)
            new_snowpark_names.append(make_unique_snowpark_name(new_spark_name))
            qualifiers.append(set())
            equivalent_snowpark_names.append(set())
        else:
            new_spark_names.append(c.spark_name)
            new_snowpark_names.append(c.snowpark_name)
            qualifiers.append(c.qualifiers)
            equivalent_snowpark_names.append(c.equivalent_snowpark_names)

    # Creating a new df to avoid updating the state of cached dataframe.
    new_df = input_df.select("*")
    result_container = DataFrameContainer.create_with_column_mapping(
        dataframe=new_df,
        spark_column_names=new_spark_names,
        snowpark_column_names=input_container.column_map.get_snowpark_columns(),
        column_qualifiers=input_container.column_map.get_qualifiers(),
        parent_column_name_map=input_container.column_map.get_parent_column_name_map(),
        table_name=input_container.table_name,
        alias=input_container.alias,
        equivalent_snowpark_names=equivalent_snowpark_names,
    )
    result_container.column_map.rename_chains = rename_columns_map

    return result_container


def map_with_columns(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Add columns to a DataFrame and return a container.
    """
    input_container = without_internal_columns(map_relation(rel.with_columns.input))
    input_df = input_container.dataframe
    with_columns = []
    for alias in rel.with_columns.aliases:
        spark_names, typed_alias = map_alias(
            alias, input_container.column_map, ExpressionTyper(input_df)
        )
        register_lca_alias(spark_names[0], typed_alias)
        with_columns.append((spark_names, typed_alias))

    # we don't need lateral aliases anymore
    clear_lca_alias_map()

    # TODO: This list needs to contain all unique column names, but the code below doesn't
    # guarantee that.
    with_columns_names = []
    with_columns_exprs = []
    with_columns_types = []
    with_column_offset = len(input_container.column_map.get_spark_columns())
    new_spark_names = []
    seen_columns = set()
    for names_list, expr in with_columns:
        assert (
            len(names_list) == 1
        ), f"Expected single column name, got {len(names_list)}: {names_list}"
        name = names_list[0]
        name_normalized = input_container.column_map._normalized_spark_name(name)
        if name_normalized in seen_columns:
            exception = ValueError(
                f"[COLUMN_ALREADY_EXISTS] The column `{name}` already exists."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception
        seen_columns.add(name_normalized)
        # If the column name is already in the DataFrame, we replace it, so we use the
        # mapping to get the correct column name.
        if input_container.column_map.has_spark_column(name):
            all_instances_of_spark_column_name = input_container.column_map.get_snowpark_column_names_from_spark_column_names(
                [name]
            )
            if len(all_instances_of_spark_column_name) == 0:
                exception = KeyError(f"Spark column name {name} does not exist")
                attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
                raise exception
            with_columns_names.extend(all_instances_of_spark_column_name)
            with_columns_exprs.extend(
                [expr.col] * len(all_instances_of_spark_column_name)
            )
            with_columns_types.extend(
                expr.types * len(all_instances_of_spark_column_name)
            )
            new_spark_names.extend([name] * len(all_instances_of_spark_column_name))
        else:
            with_columns_names.append(
                make_column_names_snowpark_compatible(
                    [name], rel.common.plan_id, with_column_offset
                )[0]
            )
            with_column_offset += 1
            with_columns_exprs.append(expr.col)
            with_columns_types.extend(expr.types)
            new_spark_names.append(name)

    if input_container.has_zero_columns():
        # just select all added columns
        result = input_df.select(
            *[
                col.alias(name)
                for name, col in zip(with_columns_names, with_columns_exprs)
            ]
        )
        return DataFrameContainer.create_with_column_mapping(
            dataframe=result,
            spark_column_names=new_spark_names,
            snowpark_column_names=with_columns_names,
            snowpark_column_types=with_columns_types,
            parent_column_name_map=input_container.column_map,
            table_name=input_container.table_name,
            alias=input_container.alias,
        )

    (
        new_spark_columns,
        new_snowpark_columns,
        qualifiers,
        equivalent_snowpark_names,
    ) = input_container.column_map.with_columns(new_spark_names, with_columns_names)

    # dedup the change in columns at snowpark name level, this is required by the with columns functions
    with_columns_names_deduped = []
    with_columns_exprs_deduped = []
    with_columns_types_deduped = []
    seen = set()
    for i, col_name in enumerate(with_columns_names):
        if col_name not in seen:
            seen.add(col_name)
            with_columns_names_deduped.append(col_name)
            with_columns_exprs_deduped.append(with_columns_exprs[i])
            with_columns_types_deduped.append(with_columns_types[i])
    result = input_df.with_columns(
        with_columns_names_deduped, with_columns_exprs_deduped
    ).select(*new_snowpark_columns)

    # SNOW-2306644: the next projection after a withColumn call can completely remove the added column
    # df.withColumn("new").select("foo").filter("new") will fail with a missing column error
    # the column will be preserved if flattening is disabled
    if hasattr(result, "_select_statement"):
        result._select_statement.flatten_disabled = True

    snowpark_name_to_type = dict(
        [(f.name, f.datatype) for f in input_df.schema.fields]
        + list(zip(with_columns_names, with_columns_types))
    )

    column_metadata = input_container.column_map.column_metadata or {}
    for alias in rel.with_columns.aliases:
        # this logic is triggered for df.withMetadata function.
        if alias.HasField("metadata") and len(alias.metadata.strip()) > 0:
            # spark sends list of alias names with only one element in the list with alias name.
            column_metadata[alias.name[0]] = json.loads(alias.metadata)

    return DataFrameContainer.create_with_column_mapping(
        dataframe=result,
        spark_column_names=new_spark_columns,
        snowpark_column_names=new_snowpark_columns,
        snowpark_column_types=[
            snowpark_name_to_type.get(n) for n in new_snowpark_columns
        ],
        column_metadata=column_metadata,
        column_qualifiers=qualifiers,
        parent_column_name_map=input_container.column_map,
        table_name=input_container.table_name,
        alias=input_container.alias,
        equivalent_snowpark_names=equivalent_snowpark_names,
    )


def map_unpivot(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    # Spark API:    df.unpivot([id_columns], [unpivot_columns], var_column, val_column)
    # Snowpark API: df.unpivot(val_column, var_column, [unpivot_columns])
    if rel.unpivot.HasField("values") and len(rel.unpivot.values.values) == 0:
        exception = SparkException.unpivot_requires_value_columns()
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    input_container = map_relation(rel.unpivot.input)
    input_df = input_container.dataframe

    def get_lease_common_ancestor_classes(types: list[snowpark.types.DataType]) -> set:
        mro_lists = [set(type.__class__.mro()) for type in types]
        common_ancestors = set.intersection(*mro_lists)
        common_ancestors.discard(object)
        common_ancestors.discard(snowpark.types._AtomicType)
        common_ancestors.discard(snowpark.types.DataType)
        return common_ancestors

    def should_cast_type(df: snowpark.DataFrame, col_names: list[str]) -> bool:
        # TODO: Follow the Spark type casting semantics and cast input columns to their common parent type.
        # Snowpark unpivot cannot handle columns with different types. For example, GS throws error
        # CONFLICTING_UNPIVOT_COLUMN_TYPES if unpivot_col_names contains an int column and a double column.
        # But Spark unpivot is able to handle such cases.
        # This function only handles the case where the column list contains more than one numerical types.

        type_column_list = [
            (
                f.datatype,
                input_container.column_map.get_spark_column_name_from_snowpark_column_name(
                    snowpark_functions_col(
                        f.name, input_container.column_map
                    ).get_name()
                ),
            )
            for f in df.schema.fields
            if snowpark_functions_col(f.name, input_container.column_map).get_name()
            in col_names
        ]
        type_iter, _ = zip(*type_column_list)
        type_list = list(type_iter)
        is_same_type = len(set(type_list)) <= 1
        contains_numeric_type = any(
            [isinstance(t, snowpark_types._NumericType) for t in type_list]
        )
        if not get_lease_common_ancestor_classes(type_list):
            # TODO: match exactly how spark shows mismatched columns
            exception = SparkException.unpivot_value_data_type_mismatch(
                ", ".join(
                    [
                        f"{dtype} {column_name}"
                        for (dtype, column_name) in type_column_list
                    ]
                )
            )
            attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
            raise exception
        return not is_same_type and contains_numeric_type

    def get_column_names(
        relation: relation_proto.Relation, df: snowpark.DataFrame
    ) -> tuple[list[str], list[str], list[str], list[str]]:
        """This function takes the input Snowpark dataframe and the input relation,
        and returns the Snowpark and Spark column names.

        Returns:
            spark_columns: contains the Spark column names in the result
            id_col_names: contains the Snowpark id column names
            unpivot_col_names: contains the Snowpark unpivot column names
            unpivot_spark_names: contains the Spark unpivot column names
        """
        spark_columns = []
        id_col_names = []
        typer = ExpressionTyper(input_df)
        for id_col in relation.unpivot.ids:
            spark_name, typed_column = map_single_column_expression(
                id_col, input_container.column_map, typer
            )
            id_col_names.append(typed_column.col.get_name())
            spark_columns.append(spark_name)

        # unpivot_col_names contains the Snowpark column names sent to GS.
        # unpivot_spark_name contains the Spark column names.
        unpivot_col_names = []
        unpivot_spark_names = []
        for v in relation.unpivot.values.values:
            spark_name, typed_column = map_single_column_expression(
                v, input_container.column_map, typer
            )
            unpivot_col_names.append(typed_column.col.get_name())
            unpivot_spark_names.append(spark_name)

        if not rel.unpivot.HasField("values"):
            # When `values` is `None`, all non-id columns will be unpivoted.
            for snowpark_name, spark_name in zip(
                input_container.column_map.get_snowpark_columns(),
                input_container.column_map.get_spark_columns(),
            ):
                if (
                    snowpark_functions_col(
                        snowpark_name, input_container.column_map
                    ).get_name()
                    not in id_col_names
                ):
                    unpivot_col_names.append(
                        snowpark_functions_col(
                            snowpark_name, input_container.column_map
                        ).get_name()
                    )
                    unpivot_spark_names.append(spark_name)

        spark_columns.append(relation.unpivot.variable_column_name)
        spark_columns.append(relation.unpivot.value_column_name)
        return spark_columns, id_col_names, unpivot_col_names, unpivot_spark_names

    (
        spark_columns,
        id_col_names,
        unpivot_col_names,
        unpivot_spark_names,
    ) = get_column_names(rel, input_df)
    (
        snowpark_value_column_name,
        snowpark_variable_column_name,
    ) = make_column_names_snowpark_compatible(
        [rel.unpivot.value_column_name, rel.unpivot.variable_column_name],
        rel.common.plan_id,
        len(spark_columns),
    )
    cast_type = should_cast_type(input_df, unpivot_col_names)

    # column_project is the project that happens before unpivot. This projection is used to
    # 1. preserve the id column, by projecting the id column to a random name.
    # 2. perform type casting of the unpivot columns.
    # column_reverse_project is the project that happens after unpivot. This project is used to
    # 1. project the id column from the random name back to the original name.
    # 2. perform case when postprocessing to fix the column names in the var column.
    column_project = []
    column_reverse_project = []
    snowpark_columns = []
    qualifiers: list[set[ColumnQualifier]] = []
    for c in input_container.column_map.get_snowpark_columns():
        c_name = snowpark_functions_col(c, input_container.column_map).get_name()
        if c_name in unpivot_col_names:
            if cast_type:
                column_project.append(
                    snowpark_functions_col(c, input_container.column_map)
                    .cast("DOUBLE")
                    .alias(c_name)
                )
            else:
                column_project.append(
                    snowpark_functions_col(c, input_container.column_map)
                )
        if c_name in id_col_names:
            id_col_alias = "SES" + generate_random_alphanumeric().upper()
            column_project.append(
                snowpark_functions_col(c, input_container.column_map).alias(
                    id_col_alias
                )
            )
            column_reverse_project.append(
                snowpark_functions_col(id_col_alias, input_container.column_map).alias(
                    c
                )
            )
            snowpark_columns.append(c)
            qualifiers.append(
                input_container.column_map.get_qualifiers_for_snowpark_column(c)
            )

    # Without the case when postprocessing, the result Spark dataframe is:
    # +---+------------+------+
    # |id | var        | val  |
    # +---+------------+------+
    # | 1 | INTSES1    | 10.0 |
    # | 1 | DOUBLESES2 | 1.0  |
    # +---+------------+------+
    # which has wrong column names in the var column. The correct column names should be:
    # +---+--------+------+
    # |id | var    | val  |
    # +---+--------+------+
    # | 1 | int    | 10.0 |
    # | 1 | double | 1.0  |
    # +---+--------+------+
    # We need a case when postprocessing to convert the value in the var column.
    post_process_variable_column = None
    for snowpark_name, spark_name in zip(unpivot_col_names, unpivot_spark_names):
        if post_process_variable_column is None:
            post_process_variable_column = snowpark_fn.when(
                snowpark_functions_col(
                    snowpark_variable_column_name, input_container.column_map
                )
                == unquote_if_quoted(snowpark_name),
                spark_name,
            )
        else:
            post_process_variable_column = post_process_variable_column.when(
                snowpark_functions_col(
                    snowpark_variable_column_name, input_container.column_map
                )
                == unquote_if_quoted(snowpark_name),
                spark_name,
            )

    column_reverse_project.append(
        post_process_variable_column.alias(snowpark_variable_column_name)
    )
    snowpark_columns.append(snowpark_variable_column_name)
    column_reverse_project.append(
        snowpark_functions_col(snowpark_value_column_name, input_container.column_map)
    )
    snowpark_columns.append(snowpark_value_column_name)
    qualifiers.extend([set() for _ in range(2)])

    result = (
        input_df.select(*column_project)
        .unpivot(
            snowpark_value_column_name,
            snowpark_variable_column_name,
            unpivot_col_names,
            include_nulls=True,
        )
        .select(*column_reverse_project)
    )
    return DataFrameContainer.create_with_column_mapping(
        dataframe=result,
        spark_column_names=spark_columns,
        snowpark_column_names=snowpark_columns,
        column_qualifiers=qualifiers,
        parent_column_name_map=input_container.column_map,
        equivalent_snowpark_names=[set()] * len(snowpark_columns),
    )


def _map_sorting_expressions(
    sorting_expressions: list[expressions_proto.Expression],
    column_map: ColumnNameMap,
    typer: ExpressionTyper,
) -> list[snowpark.Column]:
    snowpark_sorting_columns: list[snowpark.Column] = []

    for exp in sorting_expressions:
        if exp.WhichOneof("expr_type") == "unresolved_star":
            raise AnalysisException("Invalid usage of '*' in MapGroups")
        so = exp.sort_order
        _, typed_column = map_single_column_expression(so.child, column_map, typer)
        col = typed_column.col

        match (so.direction, so.null_ordering):
            case (
                expressions_proto.Expression.SortOrder.SORT_DIRECTION_ASCENDING,
                expressions_proto.Expression.SortOrder.SORT_NULLS_FIRST,
            ):
                col = col.asc_nulls_first()
            case (
                expressions_proto.Expression.SortOrder.SORT_DIRECTION_ASCENDING,
                expressions_proto.Expression.SortOrder.SORT_NULLS_LAST,
            ):
                col = col.asc_nulls_last()
            case (
                expressions_proto.Expression.SortOrder.SORT_DIRECTION_DESCENDING,
                expressions_proto.Expression.SortOrder.SORT_NULLS_FIRST,
            ):
                col = col.desc_nulls_first()
            case (
                expressions_proto.Expression.SortOrder.SORT_DIRECTION_DESCENDING,
                expressions_proto.Expression.SortOrder.SORT_NULLS_LAST,
            ):
                col = col.desc_nulls_last()
            case (
                expressions_proto.Expression.SortOrder.SORT_DIRECTION_UNSPECIFIED,
                _,
            ):
                pass
            case _:
                pass

        snowpark_sorting_columns.append(col)

    return snowpark_sorting_columns


def map_group_map(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Maps a function over groups of a DataFrame (applyInPandas or Scala mapGroups).
    """
    from snowflake.snowpark_connect.utils.context import grouping_by_scala_udf_key

    input_container = map_relation(rel.group_map.input)
    input_df = input_container.dataframe
    grouping_expressions = rel.group_map.grouping_expressions
    snowpark_grouping_expressions: list[snowpark.Column] = []
    typer = ExpressionTyper(input_df)
    group_name_list: list[str] = []

    for exp in grouping_expressions:
        with grouping_by_scala_udf_key(
            exp.WhichOneof("expr_type") == "common_inline_user_defined_function"
            and exp.common_inline_user_defined_function.scalar_scala_udf is not None
        ):
            new_name, snowpark_column = map_single_column_expression(
                exp, input_container.column_map, typer
            )
        snowpark_grouping_expressions.append(snowpark_column.col)
        group_name_list.append(new_name)

    sorting_expressions = rel.group_map.sorting_expressions
    snowpark_sorting_columns = _map_sorting_expressions(
        sorting_expressions, input_container.column_map, typer
    )

    func_proto = rel.group_map.func
    function_type = func_proto.WhichOneof("function")

    if function_type == "scalar_scala_udf":
        initial_state_container = None
        initial_grouping_expressions = None
        if rel.group_map.HasField("initial_input"):
            initial_state_container = map_relation(rel.group_map.initial_input)
            initial_grouping_expressions = rel.group_map.initial_grouping_expressions

        return _map_group_map_scala(
            input_container,
            func_proto,
            snowpark_grouping_expressions,
            group_name_list,
            snowpark_sorting_columns,
            initial_state_container=initial_state_container,
            initial_grouping_expressions=initial_grouping_expressions,
        )

    python_major, python_minor = func_proto.python_udf.python_ver.split(".")
    is_compatible_python = sys.version_info.major == int(
        python_major
    ) and sys.version_info.minor == int(python_minor)

    output_type = proto_to_snowpark_type(func_proto.python_udf.output_type)

    if not is_compatible_python or TEST_FLAG_FORCE_CREATE_SPROC or tcm.TCM_MODE:
        original_columns = None
        if input_container.column_map is not None:
            original_columns = [
                column.spark_name for column in input_container.column_map.columns
            ]

        apply_udtf_temp_name = create_apply_udtf_in_sproc(
            func_proto.python_udf,
            func_proto.function_name,
            snowpark_grouping_expressions,
            original_columns,
            input_df.schema,
        )

        group_by_df = input_df.group_by(*snowpark_grouping_expressions)
        inner_df = group_by_df._dataframe

        renamed_columns = [f"snowflake_jtf_{column}" for column in input_df.columns]
        order_by_arg = snowpark_sorting_columns if snowpark_sorting_columns else None
        tfc = snowpark_fn.call_table_function(
            apply_udtf_temp_name, *renamed_columns
        ).over(partition_by=snowpark_grouping_expressions, order_by=order_by_arg)

        result = (
            inner_df.to_df(renamed_columns)
            .join_table_function(tfc)
            .drop(*renamed_columns)
        )
    else:
        (
            callable_func,
            _,
        ) = CloudPickleSerializer().loads(func_proto.python_udf.command)
        result = input_df.group_by(*snowpark_grouping_expressions).apply_in_pandas(
            callable_func, output_type
        )

    return DataFrameContainer.create_with_column_mapping(
        dataframe=result,
        spark_column_names=[field.name for field in output_type],
        snowpark_column_names=result.columns,
        column_qualifiers=None,
        parent_column_name_map=input_container.column_map,
        equivalent_snowpark_names=None,
    )


def _map_group_map_scala(
    input_container: DataFrameContainer,
    func_proto: expressions_proto.CommonInlineUserDefinedFunction,
    snowpark_grouping_expressions: list[snowpark.Column],
    group_name_list: list[str],
    snowpark_sorting_columns: list[snowpark.Column],
    initial_state_container: DataFrameContainer | None = None,
    initial_grouping_expressions=None,
) -> DataFrameContainer:
    """
    Handle group map for Scala UDFs (mapGroups/flatMapGroups).

    The Scala function has signature Function2[K, Iterator[V], TraversableOnce[U]].
    """
    from snowflake.snowpark_connect.utils.context import grouping_by_scala_udf_key
    from snowflake.snowpark_connect.utils.java_udtf_utils import (
        JAVA_UDTF_PREFIX,
        create_java_udtf_for_scala_group_map_handling,
    )

    has_initial_state = initial_state_container is not None
    udtf_name = create_java_udtf_for_scala_group_map_handling(
        func_proto, has_initial_state=has_initial_state
    )

    output_type = proto_to_snowpark_type(func_proto.scalar_scala_udf.outputType)

    input_types = func_proto.scalar_scala_udf.inputTypes
    assert len(input_types) == 2, "Group map function should have exactly 2 input types"

    key_expected_type = proto_to_snowpark_type(input_types[0])
    value_type_kind = input_types[1].WhichOneof("kind")

    materialized_key_col_names: list[str] = []
    select_cols = list(input_container.column_map.get_snowpark_columns())
    for i, (expr, _) in enumerate(zip(snowpark_grouping_expressions, group_name_list)):
        key_col_name = f"__sc_group_key_{i}__"
        materialized_key_col_names.append(key_col_name)
        select_cols.append(expr.alias(key_col_name))

    value_col_name = "__sc_group_value__"
    if value_type_kind == "struct":
        value_expr = snowpark_fn.object_construct_keep_null(
            *[
                item
                for col_map in input_container.column_map.columns
                for item in (
                    snowpark_fn.lit(col_map.spark_name),
                    snowpark_fn.to_variant(snowpark_fn.col(col_map.snowpark_name)),
                )
            ]
        )
        value_expr = snowpark_fn.to_variant(value_expr)
        select_cols.append(value_expr.alias(value_col_name))
        value_arg = snowpark_fn.col(value_col_name)
    elif value_type_kind in ("map", "array"):
        value_col = input_container.column_map.get_snowpark_columns()[0]
        value_expr = snowpark_fn.to_variant(snowpark_fn.col(value_col))
        select_cols.append(value_expr.alias(value_col_name))
        value_arg = snowpark_fn.col(value_col_name)
    else:
        value_col = input_container.column_map.get_snowpark_columns()[0]
        value_expected_type = proto_to_snowpark_type(input_types[1])
        value_arg = snowpark_fn.col(value_col).cast(value_expected_type)

    df_with_keys = input_container.dataframe.select(*select_cols)
    partition_by_cols = [snowpark_fn.col(name) for name in materialized_key_col_names]

    if len(materialized_key_col_names) == 1:
        key_arg = snowpark_fn.col(materialized_key_col_names[0]).cast(key_expected_type)
    else:
        key_arg = snowpark_fn.object_construct(
            *[
                item
                for name, col_name in zip(group_name_list, materialized_key_col_names)
                for item in (snowpark_fn.lit(name), snowpark_fn.col(col_name))
            ]
        )

    initial_state_arg = None
    if has_initial_state:
        initial_state_df = initial_state_container.dataframe
        initial_state_typer = ExpressionTyper(initial_state_df)

        initial_key_col_names: list[str] = []
        initial_key_exprs: list[snowpark.Column] = []
        for i, exp in enumerate(initial_grouping_expressions):
            with grouping_by_scala_udf_key(
                exp.WhichOneof("expr_type") == "common_inline_user_defined_function"
                and exp.common_inline_user_defined_function.scalar_scala_udf is not None
            ):
                _, snowpark_column = map_single_column_expression(
                    exp, initial_state_container.column_map, initial_state_typer
                )
            initial_key_col_name = f"__sc_initial_key_{i}__"
            initial_key_col_names.append(initial_key_col_name)
            initial_key_exprs.append(snowpark_column.col.alias(initial_key_col_name))

        initial_state_col_name = "__sc_initial_state__"
        initial_state_expr = snowpark_fn.object_construct_keep_null(
            *[
                item
                for col_map in initial_state_container.column_map.columns
                for item in (
                    snowpark_fn.lit(col_map.spark_name),
                    snowpark_fn.to_variant(snowpark_fn.col(col_map.snowpark_name)),
                )
            ]
        )
        initial_state_expr = snowpark_fn.to_variant(initial_state_expr)

        initial_state_df_with_keys = initial_state_df.select(
            *initial_key_exprs,
            initial_state_expr.alias(initial_state_col_name),
        )

        join_condition = snowpark_fn.col(
            materialized_key_col_names[0]
        ) == snowpark_fn.col(initial_key_col_names[0])
        for main_key, init_key in zip(
            materialized_key_col_names[1:], initial_key_col_names[1:]
        ):
            join_condition = join_condition & (
                snowpark_fn.col(main_key) == snowpark_fn.col(init_key)
            )

        df_with_keys = df_with_keys.join(
            initial_state_df_with_keys,
            join_condition,
            "left",
        ).drop(*initial_key_col_names)

        partition_by_cols = [
            snowpark_fn.col(name) for name in materialized_key_col_names
        ]
        initial_state_arg = snowpark_fn.col(initial_state_col_name)

    order_by_arg = snowpark_sorting_columns if snowpark_sorting_columns else None
    if has_initial_state:
        tfc = snowpark_fn.call_table_function(
            udtf_name, key_arg, value_arg, initial_state_arg
        ).over(partition_by=partition_by_cols, order_by=order_by_arg)
    else:
        tfc = snowpark_fn.call_table_function(udtf_name, key_arg, value_arg).over(
            partition_by=partition_by_cols, order_by=order_by_arg
        )

    result = df_with_keys.join_table_function(tfc)

    return unpack_struct_output_to_container(
        df=result,
        output_column_name=JAVA_UDTF_PREFIX + "C1",
        output_type=output_type,
        cast_fields=True,
        non_struct_spark_name="value",
    )


def _can_cast_column_in_schema(
    initial_column_type: DataType, column_type_to_cast_to: DataType
) -> bool:
    # This helper function helps determine if a Column type is able to be casted to another type based off the
    # DataFrame.to(schema) function. There is a table tracking in the test_dataframe_to.py file.
    return any(
        isinstance(column_type_to_cast_to, t)
        for t in TYPE_MAP_FOR_TO_SCHEMA[
            type(initial_column_type)
            if not isinstance(initial_column_type, _NumericType)
            else _NumericType
        ]
    )
