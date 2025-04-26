from datetime import datetime
from typing import Any
from typing import Dict
from typing import List

from pyspark.sql import DataFrame
from pyspark.sql import Row
from pyspark.sql import types as spark_type

from tecton_core import errors
from tecton_core.data_types import Int32Type
from tecton_core.data_types import Int64Type
from tecton_core.schema import Schema
from tecton_spark.schema_spark_utils import schema_from_spark


def validate_df_columns_and_feature_types(
    df: DataFrame, view_schema: Schema, allow_extraneous_columns: bool = True
) -> None:
    df_columns = frozenset(schema_from_spark(df.schema).column_name_and_data_types())
    df_column_names = frozenset([x[0] for x in df_columns])
    fv_columns = view_schema.column_name_and_data_types()
    fv_column_names = frozenset([x[0] for x in fv_columns])

    missing_columns = fv_column_names - df_column_names
    extraneous_columns = df_column_names - fv_column_names

    invalid_column_set = missing_columns or (extraneous_columns and not allow_extraneous_columns)
    if invalid_column_set:
        raise errors.SCHEMA_VALIDATION_INVALID_COLUMNS(
            actual_columns=sorted(df_column_names),
            expected_columns=sorted(fv_column_names),
            extraneous_columns=sorted(extraneous_columns),
            missing_columns=sorted(missing_columns),
        )

    mismatched_columns = []
    for fv_column in fv_columns:
        if fv_column not in df_columns:
            df_column_type = next(x for x in df_columns if x[0] == fv_column[0])[1]
            # Allow Int32 -> Int64 conversion but not vice versa
            if not (isinstance(fv_column[1], Int64Type) and isinstance(df_column_type, Int32Type)):
                mismatched_columns.append((fv_column[0], fv_column[1], df_column_type))

    if mismatched_columns:
        raise errors.SCHEMA_VALIDATION_COLUMN_TYPE_MISMATCH_ERROR(mismatched_columns)


EXPECTED_TYPE_TO_PYTHON_TYPE = {
    spark_type.IntegerType: int,
    spark_type.LongType: int,
    spark_type.StringType: str,
    spark_type.FloatType: float,
    spark_type.DoubleType: float,
    spark_type.BooleanType: bool,
    spark_type.ArrayType: list,
    spark_type.MapType: dict,
    spark_type.TimestampType: datetime,
}


def _is_acceptable_struct_type(
    python_value: Any,  # noqa: ANN401
    expected_struct_type: spark_type.StructType,
    field_path: str,
    odfv_name: str,
) -> None:
    # By default, the input struct value in pyspark udf is represented as `Row` class. Depends on user's transformation,
    # the output type can be a `Row` or a `dict`.
    if isinstance(python_value, Row):
        python_value = python_value.asDict()

    if not isinstance(python_value, dict):
        msg = f"Realtime Feature View '{odfv_name}' has a field '{'.'.join(field_path)}' that is expected to be a struct, but got {type(python_value).__name__}."
        raise TypeError(msg)

    extraneous_fields = set(python_value.keys()) - set(expected_struct_type.fieldNames())
    if extraneous_fields:
        extraneous = ", ".join(extraneous_fields)
        msg = f"Realtime Feature View '{odfv_name}' has extraneous fields in '{'.'.join(field_path)}': {extraneous}"
        raise TypeError(msg)

    for sub_field in expected_struct_type.fields:
        field_name = sub_field.name
        field_type = sub_field.dataType
        if field_name in python_value:
            field_path.append(field_name)
            _is_acceptable_type(python_value[field_name], field_type, field_path, odfv_name)
            field_path.pop()


def _is_acceptable_array_type(
    python_value: Any,  # noqa: ANN401
    expected_array_type: spark_type.ArrayType,
    field_path: List[str],
    odfv_name: str,
) -> None:
    if not isinstance(python_value, list):
        msg = f"Realtime Feature View '{odfv_name}' has a field '{'.'.join(field_path)}' that is expected to be a list, but got {type(python_value).__name__}."
        raise TypeError(msg)

    current_field_name = field_path.pop()
    for i, item in enumerate(python_value):
        field_path.append(f"{current_field_name}[{i}]")
        _is_acceptable_type(item, expected_array_type.elementType, field_path, odfv_name)
        field_path.pop()
    field_path.append(current_field_name)


def _is_acceptable_map_type(
    python_value: Any,  # noqa: ANN401
    expected_map_type: spark_type.MapType,
    field_path: List[str],
    odfv_name: str,
) -> None:
    if not isinstance(python_value, dict):
        msg = f"Realtime Feature View '{odfv_name}' has a field '{'.'.join(field_path)}' that is expected to be a dict, but got {type(python_value).__name__}."
        raise TypeError(msg)

    map_field_name = field_path.pop()
    for key, value in python_value.items():
        field_path.extend([map_field_name, "key"])
        _is_acceptable_type(key, expected_map_type.keyType, field_path, odfv_name)
        field_path.pop()
        field_path.pop()

        field_path.append(f"{map_field_name}[{key}]")
        _is_acceptable_type(value, expected_map_type.valueType, field_path, odfv_name)
        field_path.pop()

    field_path.append(map_field_name)


def _is_acceptable_type(
    python_value: Any,  # noqa: ANN401
    expected_type: spark_type.DataType,
    field_path: List[str],
    odfv_name: str,
) -> None:
    if python_value is None:
        return

    if isinstance(expected_type, spark_type.StructType):
        _is_acceptable_struct_type(python_value, expected_type, field_path, odfv_name)

    elif isinstance(expected_type, spark_type.ArrayType):
        _is_acceptable_array_type(python_value, expected_type, field_path, odfv_name)

    elif isinstance(expected_type, spark_type.MapType):
        _is_acceptable_map_type(python_value, expected_type, field_path, odfv_name)

    # Check non-complex data types
    else:
        expected_python_type = EXPECTED_TYPE_TO_PYTHON_TYPE.get(type(expected_type))
        # Note: We do not use 'isinstance' here because we do _not_ allow sub-types.
        # In particular, a numpy.float64 cannot be returned in place of a float if the expected spark type is Double
        if type(python_value) is not expected_python_type:
            msg = f"Realtime Feature View '{odfv_name}' has a field '{'.'.join(field_path)}' that is expected to be a {expected_python_type.__name__}, but got {type(python_value)}. Please cast the return value to a python {expected_python_type}."
            raise TypeError(msg)


def check_python_odfv_output_schema(
    output_dict: Dict[str, Any], expected_schema: spark_type.StructType, odfv_name: str
) -> None:
    extraneous_fields = set(output_dict.keys()) - set(expected_schema.fieldNames())
    if extraneous_fields:
        msg = f"Realtime Feature View '{odfv_name}' has unexpected columns found in the dataframe schema: {', '.join(list(extraneous_fields))}. Expected schema: {', '.join(list(expected_schema.fieldNames()))}"
        raise TypeError(msg)

    for field_name in output_dict:
        output_py_value = output_dict[field_name]
        expected_spark_type = expected_schema[field_name].dataType
        _is_acceptable_type(output_py_value, expected_spark_type, [field_name], odfv_name)
