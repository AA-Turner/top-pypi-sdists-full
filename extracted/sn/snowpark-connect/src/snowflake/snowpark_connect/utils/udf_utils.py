#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

# Note: this class will be loaded in a stored procedure to create a Python UDF with different Python version.
# So its dependencies are restricted to pandas, snowpark, and, pyspark
import functools
import inspect

import pandas
import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
from pyspark.serializers import CloudPickleSerializer

import snowflake.snowpark.context as context
import snowflake.snowpark.functions as snowpark_fn
from snowflake.snowpark._internal.udf_utils import extract_return_input_types
from snowflake.snowpark._internal.utils import TempObjectType
from snowflake.snowpark.types import (
    DataType,
    PandasDataFrameType,
    StructType,
    VariantType,
)

MAP_IN_ARROW_EVAL_TYPE = 207


def create_null_safe_wrapper(func):
    """
    Create a wrapper function that handles sqlNullWrapper objects by converting them to None.
    This is needed because when arguments are cast to VariantType(), Snowflake wraps NULL values
    in sqlNullWrapper objects instead of passing None to UDFs.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Convert sqlNullWrapper objects to None before calling the actual UDF
        processed_args = [
            None if getattr(arg, "is_sql_null", False) else arg for arg in args
        ]
        processed_kwargs = {
            k: (None if getattr(v, "is_sql_null", False) else v)
            for k, v in kwargs.items()
        }
        return func(*processed_args, **processed_kwargs)

    return wrapper


class ProcessCommonInlineUserDefinedFunction:
    def __init__(
        self,
        common_inline_user_defined_function: expressions_proto.CommonInlineUserDefinedFunction,
        called_from: str,
        return_type: DataType,
        input_column_names: list[str] | None = None,
        input_types: list | None = None,
        udf_name: str | None = None,
        replace: bool = False,
        udf_packages: str = "",
        udf_imports: str = "",
        original_return_type: DataType | None = None,
    ) -> None:
        context._use_structured_type_semantics = True
        context._is_snowpark_connect_compatible_mode = True

        self._function_name = common_inline_user_defined_function.function_name
        self._is_deterministic = common_inline_user_defined_function.deterministic
        self._arguments = common_inline_user_defined_function.arguments
        self._function_type = common_inline_user_defined_function.WhichOneof("function")
        self._input_types = input_types
        if self._function_type == "scalar_scala_udf":
            # If the Scala UDF is created via `spark.udf.register`, the input types are not automatically inferred.
            # Pass on the input types from the proto message to the Scala UDF handler.
            self._scala_input_types = (
                common_inline_user_defined_function.scalar_scala_udf.inputTypes
            )
        else:
            self._scala_input_types = None
        self._udf_name = udf_name
        self._replace = replace
        self._called_from = called_from
        self._input_column_names = input_column_names
        self._udf_packages = udf_packages
        self._udf_imports = udf_imports
        self._original_return_type = original_return_type
        self._return_type = return_type
        match self._function_type:
            case "python_udf":
                self._eval_type = (
                    common_inline_user_defined_function.python_udf.eval_type
                )
                self._command = common_inline_user_defined_function.python_udf.command
                self._python_ver = (
                    common_inline_user_defined_function.python_udf.python_ver
                )
            case "scalar_scala_udf":
                self._payload = (
                    common_inline_user_defined_function.scalar_scala_udf.payload
                )
                self._nullable = (
                    common_inline_user_defined_function.scalar_scala_udf.nullable
                )
            case _:
                raise ValueError(
                    f"[snowpark_connect::unsupported_operation] Function type {self._function_type} not supported for common inline user-defined function"
                )

    @property
    def snowpark_udf_args(self):
        if self._column_mapping is not None:
            return self._snowpark_udf_args
        else:
            raise ValueError(
                "[snowpark_connect::internal_error] Column mapping is not provided, cannot get snowpark udf args"
            )

    @property
    def snowpark_udf_arg_names(self):
        if self._column_mapping is not None:
            return self._snowpark_udf_arg_names
        else:
            raise ValueError(
                "[snowpark_connect::internal_error] Column mapping is not provided, cannot get snowpark udf arg names"
            )

    def _create_python_udf(self):
        def update_none_input_types():
            if self._input_types is None:
                # If any of the parameters don't have type hint, we use Snowflake Variant type.
                func_signature = inspect.signature(callable_func)
                self._input_types = [VariantType()] * len(func_signature.parameters)

        (
            callable_func,
            pyspark_output_type,
        ) = CloudPickleSerializer().loads(self._command)

        # Wrap callable with a function which changes the current working directory
        original_callable = callable_func

        def import_staged_files():
            import os
            import shutil
            import sys
            import tarfile
            import zipfile

            # Change directory to the one containing the UDF imported files
            import_path = sys._xoptions["snowflake_import_directory"]
            if os.name == "nt":
                import tempfile

                tmp_path = os.path.join(tempfile.gettempdir(), f"sas-{os.getpid()}")
            else:
                tmp_path = f"/tmp/sas-{os.getpid()}"
            os.makedirs(tmp_path, exist_ok=True)
            os.chdir(tmp_path)
            shutil.copytree(import_path, tmp_path, dirs_exist_ok=True)

            # Extract all archives
            # This has to be done inside the UDF because Snowflake prevents from loading multiple files with the same name
            # even though they are in different paths.
            archives = os.listdir(".")
            for archive in archives:
                if not archive.endswith(".archive"):
                    # Skip files that are not archives
                    continue
                elif archive.endswith(".zip.archive") or archive.endswith(
                    ".jar.archive"
                ):
                    with zipfile.ZipFile(archive, "r") as zip_ref:
                        zip_ref.extractall(archive[: -len(".archive")])
                elif archive.endswith(".tar.gz.archive") or archive.endswith(
                    ".tgz.archive"
                ):
                    with tarfile.open(archive, "r:gz") as tar_ref:
                        tar_ref.extractall(archive[: -len(".archive")])
                elif archive.endswith(".tar.archive"):
                    with tarfile.open(archive, "r") as tar_ref:
                        tar_ref.extractall(archive[: -len(".archive")])
                os.remove(archive)

        if self._udf_packages:
            packages = [p.strip() for p in self._udf_packages.strip("[]").split(",")]
        else:
            packages = []
        if self._udf_imports:
            imports = [i.strip() for i in self._udf_imports.split(",") if i.strip()]
        else:
            imports = []

        def callable_func(*args, **kwargs):
            if imports:
                import_staged_files()
            return original_callable(*args, **kwargs)

        callable_func.__signature__ = inspect.signature(original_callable)
        if hasattr(original_callable, "__annotations__"):
            callable_func.__annotations__ = original_callable.__annotations__

        update_none_input_types()

        struct_positions = [
            i
            for i, t in enumerate(self._input_types or [])
            if isinstance(t, StructType)
        ]

        if struct_positions:

            class StructRowProxy:
                """Row-like object supporting positional and named access for PySpark compatibility."""

                def __init__(self, fields, values) -> None:
                    self._fields = fields
                    self._values = values
                    self._field_to_index = {field: i for i, field in enumerate(fields)}

                def __getitem__(self, key):
                    if isinstance(key, int):
                        return self._values[key]
                    elif isinstance(key, str):
                        if key in self._field_to_index:
                            return self._values[self._field_to_index[key]]
                        raise KeyError(f"Field '{key}' not found in struct")
                    else:
                        raise TypeError(f"Invalid key type: {type(key)}")

                def __getattr__(self, name):
                    if name.startswith("_"):
                        raise AttributeError(f"Attribute '{name}' not found")
                    if name in self._field_to_index:
                        return self._values[self._field_to_index[name]]
                    raise AttributeError(f"Attribute '{name}' not found")

                def __len__(self):
                    return len(self._values)

                def __iter__(self):
                    return iter(self._values)

                def __repr__(self):
                    field_values = [
                        f"{field}={repr(value)}"
                        for field, value in zip(self._fields, self._values)
                    ]
                    return f"Row({', '.join(field_values)})"

                def asDict(self):
                    """Convert to dict (like PySpark Row.asDict())."""
                    return dict(zip(self._fields, self._values))

            def convert_to_row(arg):
                """Convert dict to StructRowProxy. Only called for struct positions."""
                if isinstance(arg, dict) and arg:
                    fields = list(arg.keys())
                    values = [arg[k] for k in fields]
                    return StructRowProxy(fields, values)
                return arg

            def convert_from_row(result):
                """Convert StructRowProxy back to dict for serialization."""
                if isinstance(result, StructRowProxy):
                    return result.asDict()
                return result

        def struct_input_wrapper(*args, **kwargs):
            if struct_positions:
                processed_args = []
                for i, arg in enumerate(args):
                    if i in struct_positions:
                        processed_args.append(convert_to_row(arg))
                    else:
                        processed_args.append(arg)

                processed_kwargs = {k: convert_to_row(v) for k, v in kwargs.items()}
                result = callable_func(*tuple(processed_args), **processed_kwargs)
                # Convert any StructRowProxy in return value back to dict for serialization
                return convert_from_row(result)
            return callable_func(*args, **kwargs)

        needs_struct_conversion = isinstance(self._original_return_type, StructType)

        # Use callable_func directly when there are no struct inputs to avoid closure issues.
        # struct_input_wrapper captures convert_to_row in its closure, but convert_to_row is only
        # defined when struct_positions is truthy. Cloudpickle serializes all closure variables,
        # so using struct_input_wrapper without struct positions would fail during serialization.
        updated_callable_func = (
            struct_input_wrapper if struct_positions else callable_func
        )

        if not needs_struct_conversion:
            return snowpark_fn.udf(
                create_null_safe_wrapper(updated_callable_func),
                return_type=self._return_type,
                input_types=self._input_types,
                name=self._udf_name,
                replace=self._replace,
                packages=packages,
                imports=imports,
                immutable=self._is_deterministic,
            )

        is_pandas_udf, _, return_types, _ = extract_return_input_types(
            callable_func,
            self._original_return_type,
            self._input_types,
            TempObjectType.FUNCTION,
        )
        if is_pandas_udf and isinstance(return_types, PandasDataFrameType):
            # Snowpark Python UDFs only support returning a Pandas Series.
            # We change the return type to make the input callable compatible with Snowpark Python UDFs,
            # and then in the wrapper function we convert the pandas DataFrame of the
            # original callable to a Pandas Series.
            original_callable.__annotations__["return"] = pandas.Series

        field_names = [field.name for field in self._original_return_type.fields]

        def struct_wrapper(*args):
            if struct_positions:
                processed_args = []
                for i, arg in enumerate(args):
                    if i in struct_positions:
                        processed_args.append(convert_to_row(arg))
                    else:
                        processed_args.append(arg)
                args = tuple(processed_args)

            result = callable_func(*args)

            # Convert StructRowProxy back to dict for serialization
            if struct_positions:
                result = convert_from_row(result)

            if isinstance(result, (tuple, list)):
                # Convert tuple/list to dict using struct field names
                if len(result) == len(field_names):
                    return dict(zip(field_names, result))
            return result

        def pandas_struct_wrapper(*args):
            # inspired by the following snowpark modin code to handle Pandas int/bool/null data in Snowflake VariantType
            # https://github.com/snowflakedb/snowpark-python/blob/e095d5a54f3a697416c3f1df87d239def47a5495/src/snowflake/snowpark/modin/plugin/_internal/apply_utils.py#L1309-L1366
            def convert_to_snowflake_compatible_type(value):
                import numpy as np
                from pandas.api.types import is_scalar

                if is_scalar(value) and pandas.isna(value):
                    return None

                return (
                    int(value)
                    if np.issubdtype(type(value), np.integer)
                    else (
                        bool(value) if np.issubdtype(type(value), np.bool_) else value
                    )
                )

            result = callable_func(*args)
            assert len(result) == 1, "Expected result to be a single row DataFrame"
            # df.applymap doesn't help here, the original type was preserved, hence we convert each value
            row_data = [
                convert_to_snowflake_compatible_type(value)
                for value in result.iloc[0].tolist()
            ]
            result = pandas.Series([dict(zip(field_names, row_data))])
            return result

        if is_pandas_udf:
            udf_function = pandas_struct_wrapper
            if isinstance(return_types, PandasDataFrameType):
                udf_function.__annotations__ = original_callable.__annotations__
        else:
            udf_function = create_null_safe_wrapper(struct_wrapper)

        return snowpark_fn.udf(
            udf_function,
            return_type=self._return_type,
            input_types=self._input_types,
            name=self._udf_name,
            replace=self._replace,
            packages=packages,
            imports=imports,
            immutable=self._is_deterministic,
        )

    def create_udf(self):
        match self._function_type:
            case "python_udf":
                return self._create_python_udf()
            case "scalar_scala_udf":
                from snowflake.snowpark_connect.utils.context import (
                    get_is_aggregate_function,
                )

                name, is_aggregate_function = get_is_aggregate_function()
                if is_aggregate_function and name.lower() == "reduce":
                    # Handling of Scala Reduce function requires usage of Java UDAF
                    from snowflake.snowpark_connect.utils.java_udaf_utils import (
                        create_java_udaf_for_reduce_scala_function,
                    )

                    return create_java_udaf_for_reduce_scala_function(self)
                from snowflake.snowpark_connect.utils.scala_udf_utils import (
                    create_scala_udf,
                )

                return create_scala_udf(self)
            case _:
                raise ValueError(
                    f"[snowpark_connect::unsupported_operation] Function type {self._function_type} not supported for common inline user-defined function"
                )
