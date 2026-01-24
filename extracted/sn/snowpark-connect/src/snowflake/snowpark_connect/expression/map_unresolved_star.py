#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
from pyspark.errors.exceptions.base import AnalysisException

import snowflake.snowpark.functions as snowpark_fn
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
)
from snowflake.snowpark.types import StringType, StructType, VariantType
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.column_qualifier import ColumnQualifier
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.typed_column import TypedColumn
from snowflake.snowpark_connect.utils.context import get_outer_dataframes
from snowflake.snowpark_connect.utils.identifiers import (
    split_fully_qualified_spark_name,
)


def check_struct_and_get_field_datatype(field_name, schema):
    if isinstance(schema, StructType):
        if field_name in schema.names:
            return schema.__getitem__(field_name).datatype
        else:
            return None
    else:
        return None


def map_unresolved_star(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[list[str], TypedColumn]:
    if exp.unresolved_star.HasField("unparsed_target"):
        unparsed_target = exp.unresolved_star.unparsed_target
        name_parts = split_fully_qualified_spark_name(unparsed_target)

        assert (
            len(name_parts) > 1 and name_parts[-1] == "*"
        ), f"Unable to parse unparsed_target {unparsed_target}"

        # scenario where it is expanding * to the current dataframe
        if len(name_parts) == 1:
            result_exp = snowpark_fn.sql_expr(
                ", ".join(column_mapping.get_snowpark_columns())
            )
            spark_names = column_mapping.get_spark_columns()
            typed_column = TypedColumn(result_exp, lambda: typer.type(result_exp))
            typed_column.set_multi_col_qualifiers(column_mapping.get_qualifiers())
            return spark_names, typed_column

        # scenario where it is expanding * to mulitple columns
        spark_names: list[str] = []
        snowpark_names: list[str] = []
        qualifiers: list[set[ColumnQualifier]] = []

        target_qualifier = ColumnQualifier(tuple(name_parts[:-1]))
        (
            spark_names,
            snowpark_names,
            qualifiers,
        ) = column_mapping.get_spark_and_snowpark_columns_with_qualifier_for_qualifier(
            target_qualifier
        )

        if len(spark_names) == 0:
            for outer_df_container in get_outer_dataframes():
                column_mapping_for_outer_df = outer_df_container.column_map
                (
                    spark_names,
                    snowpark_names,
                    qualifiers,
                ) = column_mapping_for_outer_df.get_spark_and_snowpark_columns_with_qualifier_for_qualifier(
                    target_qualifier
                )
                if len(spark_names) > 0:
                    break

        if len(spark_names) > 0:
            final_sql_expr = snowpark_fn.sql_expr(", ".join(snowpark_names))
            typed_column = TypedColumn(
                final_sql_expr, lambda: typer.type(final_sql_expr)
            )
            typed_column.set_multi_col_qualifiers(qualifiers)
            return spark_names, typed_column

        # scenario where it is expanding * to a struct field
        # any prefix can be the column name and the rest can be the struct field names
        # we will loop over all the possiblities
        # it should be in form of alis_1.alias_2.column_name.field_1.field_2.*
        # prefix will be name[:i], column would be name[i] and fields would be name[i + 1 : -1] and name[-1] should be "*"
        # column itself can be a struct column in which case prefix will be empty
        for i in range(0, len(name_parts) - 1):
            if i == 0:
                prefix_candidate_str = name_parts[i]
            else:
                prefix_candidate_str = ".".join(
                    quote_name_without_upper_casing(x) for x in name_parts[:i]
                )
                prefix_candidate_str = f"{prefix_candidate_str}.{name_parts[i]}"
            prefix_candidate = (
                column_mapping.get_snowpark_column_name_from_spark_column_name(
                    prefix_candidate_str, allow_non_exists=True
                )
            )
            if prefix_candidate is None:
                for outer_df_container in get_outer_dataframes():
                    prefix_candidate = outer_df_container.column_map.get_snowpark_column_name_from_spark_column_name(
                        prefix_candidate_str, allow_non_exists=True
                    )
                    if prefix_candidate is not None:
                        break

            if prefix_candidate is not None:
                candidate_leaf_field = typer.df.schema
                fields = [prefix_candidate] + name_parts[i + 1 : -1]
                for subfield in fields:
                    if (
                        candidate_leaf_field := check_struct_and_get_field_datatype(
                            subfield, candidate_leaf_field
                        )
                    ) is None:
                        prefix_candidate = None
                        break

                if prefix_candidate is None:
                    continue

                spark_names = candidate_leaf_field.names
                prefix_candidate = ":".join(fields)
                all_snowpark_names = [
                    f"{prefix_candidate}:{spark_name}" for spark_name in spark_names
                ]
                final_sql_expr = snowpark_fn.sql_expr(", ".join(all_snowpark_names))

                typed_column = TypedColumn(
                    final_sql_expr,
                    lambda final_sql_expr=final_sql_expr: typer.type(final_sql_expr),
                )
                typed_column.set_multi_col_qualifiers([set() for _ in spark_names])
                return spark_names, typed_column
    else:
        snowpark_columns = column_mapping.get_snowpark_columns()
        result_exp = snowpark_fn.sql_expr(", ".join(snowpark_columns))
        spark_names = column_mapping.get_spark_columns()
        typed_column = TypedColumn(
            result_exp,
            lambda: [f.datatype for f in typer.df.schema if f.name in snowpark_columns],
        )
        typed_column.set_multi_col_qualifiers(column_mapping.get_qualifiers())
        return spark_names, typed_column

    exception = AnalysisException(
        f"[UNRESOLVED_STAR] The unresolved star expression {exp} is not supported."
    )
    attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
    raise exception


def map_unresolved_star_as_single_column(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[str, TypedColumn]:
    """
    Similar to map_unresolved_star but returns a single tuple containing
    a combined spark column name and a TypedColumn representing a struct instead of many columns. .
    If star resolves to single column, it works the same.
    """
    if exp.unresolved_star.HasField("unparsed_target"):
        names, tc = map_unresolved_star(exp, column_mapping, typer)
        assert len(names) == 1, "Expected single column"
        return names[0], tc
    else:
        snowpark_columns = column_mapping.get_snowpark_columns()
        spark_names = column_mapping.get_spark_columns()

        if len(spark_names) == 1:
            names, tc = map_unresolved_star(exp, column_mapping, typer)
            return names[0], tc

        fields_cols = [
            (
                spark_name,
                TypedColumn(
                    snowpark_fn.sql_expr(snowpark_name),
                    lambda snowpark_name=snowpark_name: typer.type(
                        snowpark_fn.sql_expr(snowpark_name)
                    ),
                ),
            )
            for spark_name, snowpark_name in zip(spark_names, snowpark_columns)
        ]

        result_exp = snowpark_fn.object_construct_keep_null(
            *[
                name_with_col
                for name, typed_col in fields_cols
                for name_with_col in (
                    snowpark_fn.lit(name),
                    typed_col.column(to_semi_structure=True),
                )
            ]
        ).cast(VariantType())

        combined_spark_name = "value"
        typed_column = TypedColumn(
            result_exp,
            lambda: [VariantType()],
        )
        typed_column.set_multi_col_qualifiers([set() for _ in spark_names])
        return combined_spark_name, typed_column


def map_unresolved_star_struct(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[list[str], list[TypedColumn]]:
    unparsed_target = exp.unresolved_star.unparsed_target
    name_parts = split_fully_qualified_spark_name(unparsed_target)

    assert (
        len(name_parts) > 1 and name_parts[-1] == "*"
    ), f"Unable to parse unparsed_target {unparsed_target}"

    expanded_args: list[TypedColumn] = []
    for i in range(0, len(name_parts) - 1):
        if i == 0:
            prefix_candidate_str = name_parts[i]
        else:
            prefix_candidate_str = ".".join(
                quote_name_without_upper_casing(x) for x in name_parts[:i]
            )
            prefix_candidate_str = f"{prefix_candidate_str}.{name_parts[i]}"
        prefix_candidate = (
            column_mapping.get_snowpark_column_name_from_spark_column_name(
                prefix_candidate_str, allow_non_exists=True
            )
        )
        if prefix_candidate is None:
            for outer_df_container in get_outer_dataframes():
                prefix_candidate = outer_df_container.column_map.get_snowpark_column_name_from_spark_column_name(
                    prefix_candidate_str, allow_non_exists=True
                )
                if prefix_candidate is not None:
                    break

        if prefix_candidate is not None:
            candidate_leaf_field = typer.df.schema
            fields = [prefix_candidate] + name_parts[i + 1 : -1]
            for subfield in fields:
                if (
                    candidate_leaf_field := check_struct_and_get_field_datatype(
                        subfield, candidate_leaf_field
                    )
                ) is None:
                    prefix_candidate = None
                    break

            if prefix_candidate is None:
                continue

            spark_names: list[str] = candidate_leaf_field.names
            prefix_candidate = ":".join(fields)

            for struct_field in candidate_leaf_field.fields:
                lit_col = snowpark_fn.lit(struct_field.name)
                expanded_args.append(TypedColumn(lit_col, lambda: [StringType()]))
                field_snowpark_name = f"{prefix_candidate}:{struct_field.name}"
                field_col = snowpark_fn.sql_expr(field_snowpark_name)
                field_type = struct_field.datatype
                expanded_args.append(
                    TypedColumn(field_col, lambda field_type=field_type: [field_type])
                )

    return spark_names, expanded_args
