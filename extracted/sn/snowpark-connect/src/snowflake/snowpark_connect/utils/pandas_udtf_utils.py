#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import hashlib
import inspect
import json
import os
import threading
from typing import Any, Callable, Iterator

import cloudpickle
import pandas as pd
import pyarrow as pa
from pyspark.sql.connect.proto.expressions_pb2 import CommonInlineUserDefinedFunction

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark.types import (
    ByteType,
    DoubleType,
    FloatType,
    IntegerType,
    LongType,
    PandasDataFrameType,
    ShortType,
    StructType,
    VariantType,
)

# Removed error imports to avoid UDF serialization issues
# from snowflake.snowpark_connect.error.error_codes import ErrorCodes
# from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code

# Package name for telemetry
TELEMETRY_PACKAGE = "snowflake-telemetry-python"


# DUPLICATED from udtf_utils.py. This module is inlined verbatim into the create-pandas-UDTF
# and cogroup-UDTF stored procedures, which lack snowpark_connect and so cannot import
# udtf_utils; each *_utils module inlined into a sproc carries its own copy of the patch.
# Server-side, the native_app_mode config callback reuses udtf_utils' copy.
_VERSION_STAGE_IMPORT_PATCH_LOCK = threading.Lock()


def _is_version_stage_relative(path: str) -> bool:
    """A ``/...`` path that is not an existing local file. A local absolute path also starts
    with ``/`` but exists on disk and must upload normally, so it is excluded."""
    trimmed = path.strip()
    return trimmed.startswith("/") and not os.path.exists(trimmed)


def apply_version_stage_import_passthrough() -> None:
    """Make Snowpark's import resolver emit version-stage-relative (``/...``) imports verbatim
    rather than treating them as missing local files, so a pandas UDTF created in the
    versioned-schema create-UDTF sproc can import files bundled at the version stage root.
    Idempotent and lock-guarded; only ``/``-paths that aren't local files are intercepted."""
    import snowflake.snowpark.session as _sp_session

    session_cls = _sp_session.Session
    with _VERSION_STAGE_IMPORT_PATCH_LOCK:
        if getattr(session_cls, "_scos_version_stage_import_patch", False):
            return

        _orig_resolve_import_path = session_cls._resolve_import_path
        _orig_resolve_imports = session_cls._resolve_imports

        def _resolve_import_path(
            path: str,
            import_path: str | None = None,
            chunk_size: int = 8192,
            whole_file_hash: bool = False,
        ) -> tuple[str, None, None]:
            if _is_version_stage_relative(path):
                return path.strip(), None, None
            return _orig_resolve_import_path(
                path, import_path, chunk_size, whole_file_hash
            )

        def _resolve_imports(
            self,
            import_only_stage: str,
            upload_and_import_stage: str,
            udf_level_import_paths: dict[str, tuple] | None = None,
            *,
            statement_params: dict[str, str] | None = None,
        ) -> list[str]:
            if udf_level_import_paths:
                version_stage = [
                    p for p in udf_level_import_paths if _is_version_stage_relative(p)
                ]
                rest = {
                    p: v
                    for p, v in udf_level_import_paths.items()
                    if not _is_version_stage_relative(p)
                }
            else:
                version_stage = []
                rest = udf_level_import_paths
            resolved = list(version_stage)
            if rest or udf_level_import_paths is None:
                resolved += _orig_resolve_imports(
                    self,
                    import_only_stage,
                    upload_and_import_stage,
                    rest if udf_level_import_paths is not None else None,
                    statement_params=statement_params,
                )
            return resolved

        session_cls._resolve_import_path = staticmethod(_resolve_import_path)
        session_cls._resolve_imports = _resolve_imports
        session_cls._scos_version_stage_import_patch = True


def _ensure_version_stage_imports_passthrough(imports: list[str]) -> None:
    """Sproc path: apply the passthrough when a version-stage import is present. Keyed on the
    ``/`` import (not is_native_app_mode, which is unavailable in the inlined sproc)."""
    if any(_is_version_stage_relative(i) for i in imports):
        apply_version_stage_import_passthrough()


# DUPLICATED CODE from udtf_utils.py to avoid incorrect loading for stored procedure UDTF creation
def process_dependencies_string_array(input_str: str) -> list[str]:
    """
    Parse a string representation of a dependency array into a list of strings.

    Converts a bracket-enclosed, comma-separated string (e.g., "[scipy, pandas, numpy]")
    into a list of trimmed package names (e.g., ["scipy", "pandas", "numpy"]).

    Args:
        input_str: A string in the format "[item1, item2, ...]" or "item1, item2, ...".
                   Can also be empty or None.

    Returns:
        A list of trimmed dependency names. Returns an empty list if input is empty or None.

    Examples:
        >>> process_dependencies_string_array("[scipy, pandas]")
        ['scipy', 'pandas']
        >>> process_dependencies_string_array("numpy, pyarrow")
        ['numpy', 'pyarrow']
        >>> process_dependencies_string_array("")
        []
    """
    if input_str and len(input_str) > 0:
        return [i.strip() for i in input_str.strip("[] ").split(",") if i.strip()]
    return []


def process_udtf_packages(
    packages_str: str,
    is_arrow_enabled: bool = False,
    custom_packages: list[str] | None = None,
    artifact_repository: str | None = None,
) -> list[str]:
    packages = process_dependencies_string_array(packages_str)
    # Include pyarrow in packages when using Arrow-enabled UDTF
    if is_arrow_enabled and "pyarrow" not in packages:
        packages += ["pyarrow"]

    # TODO: Remove this once Snowpark Python automatically includes cloudpickle when artifact_repository is set.
    # cloudpickle is required for serialization/deserialization of UDTFs but is not automatically
    # added by Snowflake when using a custom artifact_repository.
    if artifact_repository and "cloudpickle" not in packages:
        packages += ["cloudpickle"]

    if "pyspark" not in packages:
        # need this to support table argument in UDTF.
        packages += ["pyspark"]

    if custom_packages:
        for custom_package in custom_packages:
            if custom_package not in packages:
                packages.append(custom_package)

    return packages


def get_map_in_arrow_udtf(
    user_function: Callable,
    spark_column_names: list[str],
    output_column_names: list[str],
) -> Any:
    """
    Create and return a MapInArrowUDTF class with the given parameters.

    Args:
        user_function: Arrow function that processes RecordBatch iterators
        spark_column_names: List of spark column names of the given dataframe.
        output_column_names: List of expected output column names

    Returns:
        MapInArrowUDTF class that can be used with pandas_udtf
    """

    class MapInArrowUDTF:
        def __init__(self) -> None:
            self.user_function = user_function
            self.output_column_names = output_column_names
            self.spark_column_names = spark_column_names

        def end_partition(self, df: pd.DataFrame):
            if df.empty:
                empty_df = pd.DataFrame(columns=self.output_column_names)
                yield empty_df
                return

            df_without_dummy = df.drop(
                columns=["_DUMMY_PARTITION_KEY"], errors="ignore"
            )
            df_without_dummy.columns = self.spark_column_names

            # Convert pandas DataFrame to Arrow format
            table = pa.Table.from_pandas(df_without_dummy, preserve_index=False)
            batch_iterator = table.to_batches()

            result_iterator = self.user_function(batch_iterator)

            result_batches = []

            if not isinstance(result_iterator, Iterator) and not hasattr(
                result_iterator, "__iter__"
            ):
                raise RuntimeError(
                    f"[snowpark_connect::type_mismatch] Return type of the user-defined function should be "
                    f"iterator of pyarrow.RecordBatch, but is {type(result_iterator).__name__}"
                )

            for batch in result_iterator:
                if not isinstance(batch, pa.RecordBatch):
                    raise RuntimeError(
                        f"[snowpark_connect::type_mismatch] Return type of the user-defined function should "
                        f"be iterator of pyarrow.RecordBatch, but is iterator of {type(batch).__name__}"
                    )
                if batch.num_rows > 0:
                    result_batches.append(batch)

            if result_batches:
                combined_table = pa.Table.from_batches(result_batches)
                result_df = combined_table.to_pandas()
                yield result_df
            else:
                empty_df = pd.DataFrame(columns=self.output_column_names)
                yield empty_df

    return MapInArrowUDTF


def _spark_numeric_numpy_dtype(datatype) -> str | None:
    """Numpy dtype OSS Spark's mapInPandas would hand a column of this type.

    Snowflake's vectorized UDTF may materialize a small integer column as a
    narrower numpy dtype (e.g. int16) than Spark's fixed widths, so arithmetic
    inside the user function (e.g. value ** 2) can overflow where it would not
    in Spark. Returning the Spark width lets end_partition widen the batch to
    match Spark before calling the user function. Returns None for types we
    leave untouched (strings, decimals, nested, etc.).
    """
    if isinstance(datatype, ByteType):
        return "int8"
    if isinstance(datatype, ShortType):
        return "int16"
    if isinstance(datatype, IntegerType):
        return "int32"
    if isinstance(datatype, LongType):
        return "int64"
    if isinstance(datatype, FloatType):
        return "float32"
    if isinstance(datatype, DoubleType):
        return "float64"
    return None


def create_pandas_udtf(
    udtf_proto: CommonInlineUserDefinedFunction,
    spark_column_names: list[str],
    input_schema: StructType,
    return_schema: StructType,
    udtf_packages: str,
    udtf_imports: str,
    artifact_repository: str | None = None,
    session_id: str = "",
):
    user_function, _ = cloudpickle.loads(udtf_proto.python_udf.command)
    output_column_names = [field.name for field in return_schema.fields]
    output_column_original_names = [
        field.original_column_identifier for field in return_schema.fields
    ]
    # Numpy dtype each input column should carry to match OSS Spark's mapInPandas
    # batch (computed here where the Snowpark types are available; the resulting
    # plain-string list is captured into the serialized UDTF).
    input_numpy_dtypes = [
        _spark_numeric_numpy_dtype(field.datatype) for field in input_schema.fields
    ]

    class MapPandasUDTF:
        def __init__(self) -> None:
            self.user_function = user_function
            self.output_column_names = output_column_names
            self.spark_column_names = spark_column_names
            self.output_column_original_names = output_column_original_names
            self.input_numpy_dtypes = input_numpy_dtypes

        def end_partition(self, df: pd.DataFrame):
            if df.empty:
                empty_df = pd.DataFrame(columns=self.output_column_names)
                yield empty_df
                return

            df_without_dummy = df.drop(
                columns=["_DUMMY_PARTITION_KEY"], errors="ignore"
            )
            df_without_dummy.columns = self.spark_column_names
            # Widen numeric columns to the dtype Spark would use so user-function
            # arithmetic (e.g. value ** 2) does not overflow a narrower Snowflake
            # dtype. Integer casts are skipped when the column has nulls, since a
            # NaN cannot be represented in a numpy integer column.
            for col_name, np_dtype in zip(
                self.spark_column_names, self.input_numpy_dtypes
            ):
                if np_dtype is None:
                    continue
                col = df_without_dummy[col_name]
                if str(col.dtype) == np_dtype:
                    continue
                if np_dtype.startswith("int") and col.isnull().any():
                    continue
                df_without_dummy[col_name] = col.astype(np_dtype)
            # Spark's mapInPandas contract: the user function receives an
            # iterator of DataFrames (one per partition batch), not one
            # single-row DataFrame per row.
            result_iterator = self.user_function(iter([df_without_dummy]))

            if not isinstance(result_iterator, Iterator) and not hasattr(
                result_iterator, "__iter__"
            ):
                raise RuntimeError(
                    f"[snowpark_connect::type_mismatch] Return type of the user-defined function should be "
                    f"iterator of pandas.DataFrame, but is {type(result_iterator).__name__}"
                )

            output_df = pd.concat(result_iterator)
            generated_output_column_names = list(output_df.columns)

            missing_columns = []
            for original_column in self.output_column_original_names:
                if original_column not in generated_output_column_names:
                    missing_columns.append(original_column)

            if missing_columns:
                unexpected_columns = [
                    column
                    for column in generated_output_column_names
                    if column not in self.output_column_original_names
                ]
                raise RuntimeError(
                    f"[snowpark_connect::invalid_operation] [RESULT_COLUMNS_MISMATCH_FOR_PANDAS_UDF] Column names of the returned pandas.DataFrame do not match specified schema. Missing: {', '.join(sorted(missing_columns))}. Unexpected: {', '.join(sorted(unexpected_columns))}"
                    "."
                )
            reordered_df = output_df[self.output_column_original_names]
            reordered_df.columns = self.output_column_names
            yield reordered_df

    # Native App: '/'-relative imports must pass through Snowpark verbatim. Applied here
    # so it also covers the in-sproc pandas-UDTF path, which inlines this module but lacks
    # the server's snowpark_connect patch.
    _ensure_version_stage_imports_passthrough(
        process_dependencies_string_array(udtf_imports)
    )
    return snowpark_fn.pandas_udtf(
        MapPandasUDTF,
        output_schema=PandasDataFrameType(
            [field.datatype for field in return_schema.fields],
            [field.name for field in return_schema.fields],
        ),
        input_types=[
            PandasDataFrameType(
                [field.datatype for field in input_schema.fields] + [IntegerType()]
            )
        ],
        input_names=[field.name for field in input_schema.fields]
        + ["_DUMMY_PARTITION_KEY"],
        name=f"map_pandas_udtf_{session_id.replace('-','_')}",
        replace=True,
        packages=process_udtf_packages(
            udtf_packages,
            custom_packages=["pandas", TELEMETRY_PACKAGE],
            artifact_repository=artifact_repository,
        ),
        imports=process_dependencies_string_array(udtf_imports),
        is_permanent=False,
        artifact_repository=artifact_repository,
    )


def create_pandas_udtf_with_arrow(
    udtf_proto: CommonInlineUserDefinedFunction,
    spark_column_names: list[str],
    input_schema: StructType,
    return_schema: StructType,
    udtf_packages: str,
    udtf_imports: str,
    artifact_repository: str | None = None,
    session_id: str = "",
) -> str | snowpark.udtf.UserDefinedTableFunction:

    user_function, _ = cloudpickle.loads(udtf_proto.python_udf.command)
    output_column_names = [field.name for field in return_schema.fields]

    MapInArrowUDTF = get_map_in_arrow_udtf(
        user_function, spark_column_names, output_column_names
    )

    _ensure_version_stage_imports_passthrough(
        process_dependencies_string_array(udtf_imports)
    )
    return snowpark_fn.pandas_udtf(
        MapInArrowUDTF,
        output_schema=PandasDataFrameType(
            [field.datatype for field in return_schema.fields],
            [field.name for field in return_schema.fields],
        ),
        input_types=[
            PandasDataFrameType(
                [field.datatype for field in input_schema.fields] + [IntegerType()]
            )
        ],
        input_names=[field.name for field in input_schema.fields]
        + ["_DUMMY_PARTITION_KEY"],
        name=f"mapinarrow_udtf_{session_id.replace('-','_')}",
        replace=True,
        packages=process_udtf_packages(
            udtf_packages,
            is_arrow_enabled=True,
            custom_packages=["pandas", TELEMETRY_PACKAGE],
            artifact_repository=artifact_repository,
        ),
        imports=process_dependencies_string_array(udtf_imports),
        is_permanent=False,
        artifact_repository=artifact_repository,
    )


def get_cogroup_pandas_udtf(
    user_function: Callable,
    input1_spark_column_names: list[str],
    input2_spark_column_names: list[str],
    output_column_names: list[str],
    output_column_original_names: list[str],
    grouping_column_names: list[str] | None = None,
) -> Any:
    """
    Create and return a CoGroupPandasUDTF class with the given parameters.

    Args:
        user_function: User function that takes two pandas DataFrames and returns one
        input1_spark_column_names: Column names for the first DataFrame
        input2_spark_column_names: Column names for the second DataFrame
        output_column_names: List of expected output column names (snowflake names)
        output_column_original_names: List of original column names from user schema
        grouping_column_names: Grouping column names for key construction

    Returns:
        CoGroupPandasUDTF class that can be used with pandas_udtf
    """
    sig = inspect.signature(user_function)
    expects_key = len(sig.parameters) == 3
    _grouping_column_names = grouping_column_names or []

    class CoGroupPandasUDTF:
        def __init__(self) -> None:
            self.user_function = user_function
            self.output_column_names = output_column_names
            self.output_column_original_names = output_column_original_names
            self.input1_spark_column_names = input1_spark_column_names
            self.input2_spark_column_names = input2_spark_column_names
            self.value_col = "__SC_COGROUP_VALUE__"
            self.source_col = "__SC_COGROUP_SOURCE__"
            self.expects_key = expects_key
            self.grouping_column_names = _grouping_column_names

        def end_partition(self, df: pd.DataFrame):
            if df.empty:
                empty_df = pd.DataFrame(columns=self.output_column_names)
                yield empty_df
                return

            df1_rows = df[df[self.source_col] == 1]
            df2_rows = df[df[self.source_col] == 2]

            df1_values = df1_rows[self.value_col].tolist()
            df1_records = []
            for val in df1_values:
                if isinstance(val, str):
                    df1_records.append(json.loads(val))
                elif isinstance(val, dict):
                    df1_records.append(val)
                else:
                    df1_records.append({})

            df2_values = df2_rows[self.value_col].tolist()
            df2_records = []
            for val in df2_values:
                if isinstance(val, str):
                    df2_records.append(json.loads(val))
                elif isinstance(val, dict):
                    df2_records.append(val)
                else:
                    df2_records.append({})

            df1_data = pd.DataFrame(df1_records, columns=self.input1_spark_column_names)
            df2_data = pd.DataFrame(df2_records, columns=self.input2_spark_column_names)

            if self.expects_key:
                source_df = df1_data if len(df1_data) > 0 else df2_data
                if len(source_df) > 0:
                    key = tuple(
                        source_df[col].iloc[0]
                        for col in self.grouping_column_names
                        if col in source_df.columns
                    )
                else:
                    key = tuple(None for _ in self.grouping_column_names)
                result_df = self.user_function(key, df1_data, df2_data)
            else:
                result_df = self.user_function(df1_data, df2_data)

            if result_df is not None and not isinstance(result_df, pd.DataFrame):
                raise RuntimeError(
                    f"[snowpark_connect::type_mismatch] Return type of the co-group function should be "
                    f"pandas.DataFrame, but is {type(result_df).__name__}"
                )

            if result_df is None or result_df.empty:
                empty_df = pd.DataFrame(columns=self.output_column_names)
                yield empty_df
                return

            generated_output_column_names = list(result_df.columns)

            missing_columns = []
            for original_column in self.output_column_original_names:
                if original_column not in generated_output_column_names:
                    missing_columns.append(original_column)

            if missing_columns:
                unexpected_columns = [
                    column
                    for column in generated_output_column_names
                    if column not in self.output_column_original_names
                ]
                raise RuntimeError(
                    f"[snowpark_connect::invalid_operation] [RESULT_COLUMNS_MISMATCH_FOR_PANDAS_UDF] Column names of the returned pandas.DataFrame do not match specified schema. Missing: {', '.join(sorted(missing_columns))}. Unexpected: {', '.join(sorted(unexpected_columns))}"
                    "."
                )
            reordered_df = result_df[self.output_column_original_names]
            reordered_df.columns = self.output_column_names
            yield reordered_df

    return CoGroupPandasUDTF


def create_cogroup_pandas_udtf(
    udtf_proto: CommonInlineUserDefinedFunction,
    input1_spark_column_names: list[str],
    input2_spark_column_names: list[str],
    return_schema: StructType,
    udtf_packages: str,
    udtf_imports: str,
    artifact_repository: str | None = None,
    session_id: str = "",
    grouping_column_names: list[str] | None = None,
):
    """
    Create a pandas UDTF for co-group operations (applyInPandas on cogrouped data).

    The UDTF receives rows from a UNION ALL of both DataFrames with a source marker.
    Each row has: value (JSON object with column data), source (1 or 2).
    It separates the rows by source, reconstructs two pandas DataFrames, and calls
    the user function with both DataFrames.
    """
    base_name = (
        "cogroup_pandas_udtf_" + hashlib.md5(udtf_proto.python_udf.command).hexdigest()
    )
    udtf_name = f"{base_name}_{session_id.replace('-','_')}"

    user_function, _ = cloudpickle.loads(udtf_proto.python_udf.command)
    output_column_names = [field.name for field in return_schema.fields]
    output_column_original_names = [
        field.original_column_identifier for field in return_schema.fields
    ]

    CoGroupPandasUDTF = get_cogroup_pandas_udtf(
        user_function,
        input1_spark_column_names,
        input2_spark_column_names,
        output_column_names,
        output_column_original_names,
        grouping_column_names=grouping_column_names,
    )

    from snowflake.snowpark_connect.relation.map_cogroup_map import (
        SOURCE_COL_NAME,
        VALUE_COL_NAME,
    )

    _ensure_version_stage_imports_passthrough(
        process_dependencies_string_array(udtf_imports)
    )
    return snowpark_fn.pandas_udtf(
        CoGroupPandasUDTF,
        output_schema=PandasDataFrameType(
            [field.datatype for field in return_schema.fields],
            [field.name for field in return_schema.fields],
        ),
        input_types=[PandasDataFrameType([VariantType(), IntegerType()])],
        input_names=[VALUE_COL_NAME, SOURCE_COL_NAME],
        name=udtf_name,
        replace=True,
        packages=process_udtf_packages(
            udtf_packages,
            custom_packages=["pandas", TELEMETRY_PACKAGE],
            artifact_repository=artifact_repository,
        ),
        imports=process_dependencies_string_array(udtf_imports),
        is_permanent=False,
        artifact_repository=artifact_repository,
    )
