#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import re

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
from pyspark.errors.exceptions.base import AnalysisException

import snowflake.snowpark.functions as snowpark_fn
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
)
from snowflake.snowpark.types import StringType, StructField, StructType, VariantType
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.column_qualifier import ColumnQualifier
from snowflake.snowpark_connect.config import scope_star_to_source_dataframe
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.map_unresolved_attribute import (
    _try_resolve_column_in_scopes,
)
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.typed_column import FieldType, TypedColumn
from snowflake.snowpark_connect.utils.cache import analyze_memo_get
from snowflake.snowpark_connect.utils.context import (
    get_outer_dataframes,
    get_plan_id_map,
    get_spark_session_id,
    set_plan_id_map,
)
from snowflake.snowpark_connect.utils.identifiers import (
    split_fully_qualified_spark_name,
)

# pyspark 3.5.3 UnresolvedStar has no plan_id field. df["*"] is encoded with
# this target so the server can expand that dataframe only. Spark
# Dataset.col("*") is ResolvedStar of that dataset's analyzed output.
_DF_STAR_TARGET = re.compile(r"^__snowpark_connect_df_star_(\d+)__\.\*$")


def dataframe_star_target(plan_id: int) -> str:
    return f"__snowpark_connect_df_star_{int(plan_id)}__.*"


def dataframe_star_plan_id(exp: expressions_proto.Expression) -> int | None:
    """Plan id encoded on ``df["*"]``, or None for ``*`` and ``qualifier.*``."""
    if exp.WhichOneof("expr_type") != "unresolved_star":
        return None
    if not exp.unresolved_star.HasField("unparsed_target"):
        return None
    match = _DF_STAR_TARGET.match(exp.unresolved_star.unparsed_target)
    if match is None:
        return None
    return int(match.group(1))


def _lookup_plan_container(plan_id: int) -> DataFrameContainer | None:
    target = get_plan_id_map(plan_id)
    if target is not None:
        return target
    target = analyze_memo_get((get_spark_session_id(), plan_id))
    if target is not None:
        set_plan_id_map(plan_id, target)
    return target


def _columns_for_source_plan(
    plan_id: int,
    column_mapping: ColumnNameMap,
) -> tuple[
    list[str], list[str], list[set[ColumnQualifier]], list[ExpressionTyper | None]
]:
    """Visible columns of ``plan_id``, as they appear in ``column_mapping``.

    The last list holds, per column, the typer of the outer scope that resolved
    it, or None when the current scope did.
    """
    target = _lookup_plan_container(plan_id)
    if target is None:
        exception = AnalysisException(
            f"[UNRESOLVED_STAR] Cannot expand columns from dataframe plan {plan_id}."
        )
        attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
        raise exception

    spark_names: list[str] = []
    snowpark_names: list[str] = []
    qualifiers: list[set[ColumnQualifier]] = []
    column_typers: list[ExpressionTyper | None] = []
    for column in target.column_map.columns:
        if not column.is_visible:
            continue
        snowpark_name, found_map, found_typer = _try_resolve_column_in_scopes(
            column.spark_name,
            column_mapping,
            original_snowpark_name=column.snowpark_name,
        )
        if snowpark_name is None or found_map is None:
            exception = AnalysisException(
                f"[UNRESOLVED_COLUMN.WITH_SUGGESTION] A column or function "
                f"parameter with name `{column.spark_name}` cannot be resolved."
            )
            attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
            raise exception
        spark_names.append(column.spark_name)
        snowpark_names.append(snowpark_name)
        qualifiers.append(found_map.get_qualifiers_for_snowpark_column(snowpark_name))
        column_typers.append(found_typer)
    return spark_names, snowpark_names, qualifiers, column_typers


def _field_types_for_projected_columns(
    typer: ExpressionTyper,
    snowpark_columns: tuple[str, ...],
    column_typers: tuple[ExpressionTyper | None, ...],
) -> list[FieldType]:
    """One field type per projected column, in projected-column order.

    The SQL and the spark names follow the source plan. Scanning the current
    relation schema and keeping matching names follows that relation's order
    instead, so a reorder assigns those types to the wrong columns.

    A column resolved in an outer scope is typed against that scope's
    dataframe, as map_unresolved_attribute does. A name missing from the
    schema is typed through its typer rather than skipped: skipping would
    shift every later type onto the wrong column.
    """
    remaining: dict[int, list] = {}
    field_types: list[FieldType] = []
    for name, column_typer in zip(snowpark_columns, column_typers, strict=True):
        source = column_typer if column_typer is not None else typer
        fields = remaining.get(id(source.df))
        if fields is None:
            fields = remaining[id(source.df)] = list(source.df.schema)
        match_at = next(
            (index for index, field in enumerate(fields) if field.name == name),
            None,
        )
        if match_at is not None:
            field = fields.pop(match_at)
            field_types.append(FieldType(field.datatype, field.nullable))
            continue
        typed = source.type(snowpark_fn.col(name))
        if len(typed) != 1:
            exception = AssertionError(
                f"Expected one type for star column {name}, got {len(typed)}."
            )
            attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
            raise exception
        field_types.append(typed[0])
    return field_types


def _typed_star(
    spark_names: list[str],
    snowpark_columns: list[str],
    qualifiers: list[set[ColumnQualifier]],
    typer: ExpressionTyper,
    column_typers: list[ExpressionTyper | None] | None = None,
) -> tuple[list[str], TypedColumn]:
    result_exp = snowpark_fn.sql_expr(", ".join(snowpark_columns))
    names = tuple(snowpark_columns)
    sources = (
        tuple(column_typers) if column_typers is not None else (None,) * len(names)
    )
    typed_column = TypedColumn(
        result_exp,
        lambda: _field_types_for_projected_columns(typer, names, sources),
    )
    typed_column.set_multi_col_qualifiers(qualifiers)
    return spark_names, typed_column


def _unscoped_star(
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[list[str], TypedColumn]:
    snowpark_columns = column_mapping.get_snowpark_columns()
    spark_names = column_mapping.get_spark_columns()
    if not scope_star_to_source_dataframe():
        # Flag off keeps the previous typing: relation schema order, names
        # missing from the schema skipped.
        result_exp = snowpark_fn.sql_expr(", ".join(snowpark_columns))
        typed_column = TypedColumn(
            result_exp,
            lambda: [
                FieldType(f.datatype, f.nullable)
                for f in typer.df.schema
                if f.name in snowpark_columns
            ],
        )
        typed_column.set_multi_col_qualifiers(column_mapping.get_qualifiers())
        return spark_names, typed_column
    return _typed_star(
        spark_names,
        snowpark_columns,
        column_mapping.get_qualifiers(),
        typer,
    )


def _struct_field_path(column: str, field_names: list[str]) -> str:
    """Build ``column:"f1":"f2"`` for a struct column and its nested field names.

    ``column`` must already be a Snowpark SQL column name and is used as is.
    Field names are JSON keys and may contain spaces, dots, colons or dashes, which
    an unquoted path splits or misreads, so each one is double-quoted. Quoting does
    not change matching: Snowflake path keys are case-sensitive either way.
    """
    quoted = [quote_name_without_upper_casing(name) for name in field_names]
    return ":".join([column, *quoted])


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
    plan_id = dataframe_star_plan_id(exp)
    if plan_id is not None:
        # Flag off keeps the previous result: the star expands the whole input.
        if scope_star_to_source_dataframe():
            (
                spark_names,
                snowpark_names,
                qualifiers,
                column_typers,
            ) = _columns_for_source_plan(plan_id, column_mapping)
            return _typed_star(
                spark_names, snowpark_names, qualifiers, typer, column_typers
            )
        return _unscoped_star(column_mapping, typer)

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
                all_snowpark_names = [
                    _struct_field_path(fields[0], [*fields[1:], spark_name])
                    for spark_name in spark_names
                ]
                final_sql_expr = snowpark_fn.sql_expr(", ".join(all_snowpark_names))

                typed_column = TypedColumn(
                    final_sql_expr,
                    lambda leaf=candidate_leaf_field: [
                        FieldType(sf.datatype, sf.nullable) for sf in leaf.fields
                    ],
                )
                typed_column.set_multi_col_qualifiers([set() for _ in spark_names])
                return spark_names, typed_column
    else:
        return _unscoped_star(column_mapping, typer)

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
    plan_id = dataframe_star_plan_id(exp)
    if exp.unresolved_star.HasField("unparsed_target") and plan_id is None:
        names, tc = map_unresolved_star(exp, column_mapping, typer)
        assert len(names) == 1, "Expected single column"
        return names[0], tc
    else:
        if plan_id is not None and scope_star_to_source_dataframe():
            (
                spark_names,
                snowpark_columns,
                _qualifiers,
                _column_typers,
            ) = _columns_for_source_plan(plan_id, column_mapping)
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
            lambda: [
                StructType(
                    [
                        StructField(
                            name,
                            typed_col.typ,
                            nullable=typed_col.nullable,
                            _is_column=False,
                        )
                        for name, typed_col in fields_cols
                    ]
                )
            ],
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

            for struct_field in candidate_leaf_field.fields:
                lit_col = snowpark_fn.lit(struct_field.name)
                expanded_args.append(TypedColumn(lit_col, lambda: [StringType()]))
                field_snowpark_name = _struct_field_path(
                    fields[0], [*fields[1:], struct_field.name]
                )
                field_col = snowpark_fn.sql_expr(field_snowpark_name)
                field_type = FieldType(struct_field.datatype, struct_field.nullable)
                expanded_args.append(TypedColumn(field_col, lambda ft=field_type: [ft]))

    return spark_names, expanded_args
