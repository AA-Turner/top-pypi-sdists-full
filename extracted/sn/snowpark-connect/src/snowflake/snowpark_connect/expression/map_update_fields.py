#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
from pyspark.errors.exceptions.base import AnalysisException

import snowflake.snowpark.functions as snowpark_fn
from snowflake.snowpark.types import (
    DataType,
    MapType,
    StringType,
    StructField,
    StructType,
    VariantType,
)
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.typed_column import TypedColumn
from snowflake.snowpark_connect.utils.identifiers import (
    split_fully_qualified_spark_name,
)


def update_field_in_schema(
    schema: StructType, named_parts: list[str], value_typ: DataType | None = None
) -> StructType:
    new_fields = []
    field_updated = False
    field_str = ".".join(named_parts)
    for field in schema.fields:
        new_field = None
        if field.name == named_parts[0]:
            if len(named_parts) == 1:
                if value_typ is not None:
                    new_field = StructField(
                        field.name, value_typ, field.nullable, _is_column=False
                    )
            else:
                if isinstance(field.datatype, StructType):
                    # Recurse into nested struct
                    updated_subschema = update_field_in_schema(
                        field.datatype, named_parts[1:], value_typ
                    )
                    new_field = StructField(
                        field.name, updated_subschema, field.nullable, _is_column=False
                    )
                else:
                    exception = AnalysisException(
                        message=f"[FIELD_NOT_FOUND] No such struct field `{field_str}` in `{field}`"
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception
            field_updated = True
        else:
            new_field = field  # leave unchanged

        if new_field is not None:
            new_fields.append(new_field)

    if not field_updated and value_typ is not None:
        # this is a scenario where we add new field
        if len(named_parts) == 1:
            new_fields.append(
                StructField(named_parts[0], value_typ, field.nullable, _is_column=False)
            )
        else:
            # if the value type is None that means we want to drop the field and spark does not throw an error if the field does not exists
            # but if the value type is not None, it means we should add or update this field which has already been covered above
            # if we reach this code, it means the field should have existed
            exception = AnalysisException(
                message=f"[FIELD_NOT_FOUND] No such struct field `{field_str}`"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
    return StructType(new_fields)


def _get_update_operations_list(exp: expressions_proto.Expression):
    value_expressions = []
    field_expressions = []
    current_exp = exp
    while current_exp.HasField("update_fields"):
        field_expressions.append(current_exp.update_fields.field_name)
        if current_exp.update_fields.HasField("value_expression"):
            value_expressions.append(current_exp.update_fields.value_expression)
        else:
            value_expressions.append(None)
        current_exp = current_exp.update_fields.struct_expression

    # we need to reverse this because the updates need to be applied bottom up
    value_expressions.reverse()
    field_expressions.reverse()
    return field_expressions, value_expressions, current_exp


def map_update_fields(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[list[str], TypedColumn]:
    field_expressions, value_expressions, struct_exp = _get_update_operations_list(exp)

    from snowflake.snowpark_connect.expression.map_expression import (
        map_single_column_expression,
    )

    struct_name, struct_typed_column = map_single_column_expression(
        struct_exp, column_mapping, typer
    )

    if not isinstance(struct_typed_column.typ, StructType):
        exception = AnalysisException(
            f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "update_fields({struct_name}, ...)" due to data type mismatch: Parameter 1 requires the "STRUCT" type'
        )
        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
        raise exception

    final_schema = struct_typed_column.typ
    value_column_list = []
    # Snowflake UDFs don't support StructType/MapType, convert to VariantType
    input_types_to_the_udf = [VariantType()]
    update_operation_strs = []
    array_of_named_parts = []
    for field_expression, value_expression in zip(field_expressions, value_expressions):
        name_parts = split_fully_qualified_spark_name(field_expression)

        assert name_parts, f"Unable to parse field_name {field_expression}"

        if value_expression is None:
            final_schema = update_field_in_schema(final_schema, name_parts, None)
            update_operation_strs.append("dropfield()")
            value_column_list.append(
                snowpark_fn.lit("_SNOWPARK_CONNECT_UPDATE_FIELD_DROP_")
            )
            input_types_to_the_udf.append(StringType())
        else:
            value_spark_name, value_typed_column = map_single_column_expression(
                value_expression, column_mapping, typer
            )
            final_schema = update_field_in_schema(
                final_schema, name_parts, value_typed_column.typ
            )
            update_operation_strs.append(f"WithField({value_spark_name})")
            value_column_list.append(value_typed_column.col)
            # Convert StructType/MapType to VariantType for Snowflake UDFs (ArrayType is supported)
            if isinstance(value_typed_column.typ, (StructType, MapType)):
                input_types_to_the_udf.append(VariantType())
            else:
                input_types_to_the_udf.append(value_typed_column.typ)

        array_of_named_parts.append(name_parts)

    update_operations_str = ", ".join(update_operation_strs)
    final_name = f"update_fields({struct_name}, {update_operations_str})"

    if len(final_schema.fields) == 0:
        exception = AnalysisException(
            f'[DATATYPE_MISMATCH.CANNOT_DROP_ALL_FIELDS] Cannot resolve "{final_name}" due to data type mismatch: Cannot drop all fields in struct.'
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
        raise exception

    # Snowflake UDFs don't support StructType, so we use VariantType
    # The result will be automatically cast back to the struct type
    @snowpark_fn.udf(
        input_types=input_types_to_the_udf,
        return_type=VariantType(),
    )
    def _update(dictionary, *array_of_value):
        if not isinstance(dictionary, dict):
            return None

        # Recursively copy to create mutable dict from Snowflake's VARIANT objects
        def make_mutable_copy(obj):
            if obj is None:
                return None
            elif isinstance(obj, dict):
                return {k: make_mutable_copy(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [make_mutable_copy(item) for item in obj]
            else:
                return obj

        result = make_mutable_copy(dictionary)

        for fields_array, value in zip(array_of_named_parts, array_of_value):
            current = result
            for k in fields_array[:-1]:
                current = current.get(k)
                if current is None:
                    break

            if current is not None and isinstance(current, dict):
                if value == "_SNOWPARK_CONNECT_UPDATE_FIELD_DROP_":
                    current.pop(fields_array[-1], None)
                else:
                    current[fields_array[-1]] = value

        return result

    # Cast inputs to VARIANT (Snowflake UDFs don't support complex types directly)
    struct_as_variant = struct_typed_column.col.cast(VariantType())
    variant_value_list = [
        col.cast(VariantType()) if isinstance(udf_type, VariantType) else col
        for col, udf_type in zip(value_column_list, input_types_to_the_udf[1:])
    ]

    udf_result = _update(struct_as_variant, *variant_value_list)

    # Cast the VariantType result back to the target StructType
    final_exp = udf_result.cast(final_schema)

    return [final_name], TypedColumn(final_exp, lambda: typer.type(final_exp))
