#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

# Note: this class will be loaded in a stored procedure to create a Python UDTF with different Python version.
# So its dependencies are restricted to pandas, snowpark, and, pyspark by default
import builtins
import datetime
import decimal
import inspect
from typing import Any

import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.serializers import CloudPickleSerializer

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark.types import StructType, VariantType

# Package names for UDTFs
TELEMETRY_PACKAGE = "snowflake-telemetry-python"

# Flag to enable/disable automatic telemetry wrapper for UDTFs
# When True, UDTFs will automatically emit telemetry events at start/completion
ENABLE_UDTF_TELEMETRY = True


# DUPLICATED CODE from pandas_udtf_utils.py to avoid incorrect loading for stored procedure UDTF creation
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


def create_udtf(
    session: snowpark.Session,
    udtf_proto: relation_proto.CommonInlineUserDefinedTableFunction,
    expected_types: list[tuple[str, Any]],
    output_schema: StructType,
    packages: str,
    imports: str,
    is_arrow_enabled: bool,
    is_spark_compatible_udtf_mode_enabled: bool,
    called_from: str,
    artifact_repository: str | None = None,
    resource_constraint: dict[str, str] | None = None,
    call_site_types: list | None = None,
    table_arg_layout: list[tuple[str, list | None]] | None = None,
) -> str | snowpark.udtf.UserDefinedTableFunction:
    udtf = udtf_proto.python_udtf
    callable_func = CloudPickleSerializer().loads(udtf.command)

    original_func = callable_func.eval
    func_signature = inspect.signature(original_func)
    # Build per-position input_types: use the native Snowpark type for scalar types that
    # Snowflake delivers natively to Python (int, float, str, bool, bytes, date, datetime,
    # Decimal), and VariantType for everything else (struct/map/variant/array).
    # When call_site_types is not provided (e.g. register_udtf has no call-site info),
    # fall back to all-VariantType to preserve existing behavior.
    n_params = len(func_signature.parameters) - 1  # subtract "self"
    if table_arg_layout is not None:
        # Native table-arg path: call_site_types is the FLAT per-column list (one entry
        # per physical function parameter, table Rows already expanded to columns).
        # Emit native SQL types for scalar positions; VARIANT only for genuinely
        # non-native columns. The handler-side wrapper regroups these flat params back
        # into the single Row via table_arg_layout.
        #
        # Imported lazily (not at module scope): this module's source is embedded into
        # the UDTF-creation stored procedure, whose sandbox has no ``snowflake.snowpark_connect``.
        # The native branches only ever run server-side, so the import is safe here.
        from snowflake.snowpark_connect.utils.python_udf_marshal import (  # noqa: PLC0415
            native_or_variant_input_types,
        )

        input_types = native_or_variant_input_types(call_site_types or [])
    elif call_site_types is not None and len(call_site_types) == n_params:
        from snowflake.snowpark_connect.utils.python_udf_marshal import (  # noqa: PLC0415
            native_or_variant_input_types,
        )

        input_types = native_or_variant_input_types(call_site_types)
    else:
        input_types = [VariantType()] * n_params

    if imports:
        # Wrapp callable to allow reading imported files
        callable_func = artifacts_reader_wrapper(callable_func)

    # Get the function name for telemetry
    function_name = udtf_proto.function_name if udtf_proto.function_name else None

    if is_arrow_enabled:
        callable_func = spark_compatible_udtf_wrapper_with_arrow(
            callable_func,
            expected_types,
            function_name,
            enable_telemetry=ENABLE_UDTF_TELEMETRY,
            table_arg_layout=table_arg_layout,
        )
    elif is_spark_compatible_udtf_mode_enabled:
        callable_func = spark_compatible_udtf_wrapper(
            callable_func,
            expected_types,
            function_name,
            enable_telemetry=ENABLE_UDTF_TELEMETRY,
            table_arg_layout=table_arg_layout,
        )
    else:
        # For simple case (no arrow, no spark-compatible mode), add telemetry wrapper.
        # We preserve the original method's signature/annotations for validation by copying
        # them to the wrapper function. This allows Snowpark to validate type hints
        # (e.g., reject Row type parameters) while still emitting telemetry.
        if table_arg_layout is not None:
            # Native table-arg path: regroup the flat native columns into the single Row
            # the handler expects before delegating to the user's eval. The regroup helper
            # is defined locally (via the factory) so it cloudpickles by value.
            #
            # NOTE: unlike the telemetry branch below we deliberately do NOT copy
            # original_func's __signature__ — the physical function has one native param
            # per table column (flat), so eval's single-Row signature would fail
            # Snowpark's arity validation.
            _, regroup_flat_table_args = _create_table_arg_helpers()

            def process_native_table_arg(self, *args, **kwargs):
                if ENABLE_UDTF_TELEMETRY:
                    try:
                        from snowflake import telemetry

                        telemetry.set_span_attribute(
                            "udtf.name", function_name or "anonymous_udtf"
                        )
                        telemetry.add_event("udtf_invocation_start", {})
                    except Exception:
                        pass
                try:
                    regrouped = regroup_flat_table_args(args, table_arg_layout)
                    result = self.eval(*regrouped, **kwargs)
                    if result is not None:
                        yield from result
                finally:
                    if ENABLE_UDTF_TELEMETRY:
                        try:
                            from snowflake import telemetry

                            telemetry.add_event("udtf_invocation_complete", {})
                        except Exception:
                            pass

            callable_func.process = process_native_table_arg
        elif ENABLE_UDTF_TELEMETRY:

            def process_with_telemetry(self, *args, **kwargs):
                try:
                    from snowflake import telemetry

                    telemetry.set_span_attribute(
                        "udtf.name", function_name or "anonymous_udtf"
                    )
                    telemetry.add_event("udtf_invocation_start", {})
                except Exception:
                    pass
                try:
                    # Use self.eval() to properly delegate through any wrappers
                    result = self.eval(*args, **kwargs)
                    # Handle UDTFs where eval() returns None (state accumulation pattern)
                    # and actual output comes from terminate()
                    if result is not None:
                        yield from result
                finally:
                    try:
                        from snowflake import telemetry

                        telemetry.add_event("udtf_invocation_complete", {})
                    except Exception:
                        pass

            # Preserve original signature and annotations for validation
            process_with_telemetry.__signature__ = inspect.signature(original_func)
            process_with_telemetry.__annotations__ = getattr(
                original_func, "__annotations__", {}
            )
            callable_func.process = process_with_telemetry
        else:
            callable_func.process = original_func

        # Map terminate to end_partition - Snowflake uses end_partition, not terminate
        if hasattr(callable_func, "terminate"):
            callable_func.end_partition = callable_func.terminate

    # Add telemetry package if telemetry is enabled
    custom_packages = [TELEMETRY_PACKAGE] if ENABLE_UDTF_TELEMETRY else None
    packages = process_udtf_packages(
        packages,
        is_arrow_enabled,
        artifact_repository=artifact_repository,
        custom_packages=custom_packages,
    )
    imports = process_dependencies_string_array(imports)
    match called_from:
        case "register_udtf":
            return session.udtf.register(
                handler=callable_func,
                output_schema=output_schema,
                input_types=input_types,
                replace=True,
                packages=packages,
                imports=imports,
                artifact_repository=artifact_repository,
                resource_constraint=resource_constraint,
            )
        case "map_common_inline_user_defined_table_function":
            # Check if the number of arguments provided matches the function signature
            expected_arg_count = len(func_signature.parameters) - 1  # Skip self
            actual_arg_count = len(udtf_proto.arguments)

            # Missing arguments
            if actual_arg_count < expected_arg_count:
                param_names = list(func_signature.parameters.keys())[1:]  # Skip self
                missing_params = param_names[actual_arg_count:]
                missing_param_str = ", ".join(f"'{p}'" for p in missing_params)
                return f"eval() missing {len(missing_params)} required positional argument: {missing_param_str}"
            # Too many arguments
            elif actual_arg_count > expected_arg_count:
                total_expected = expected_arg_count + 1  # Add 1 for self
                total_given = actual_arg_count + 1  # Add 1 for self

                return f"eval() takes {total_expected} positional arguments but {total_given} were given"

            return snowpark_fn.udtf(
                handler=callable_func,
                output_schema=output_schema,
                input_types=input_types,
                name=udtf_proto.function_name,
                replace=True,
                packages=packages,
                imports=imports,
                artifact_repository=artifact_repository,
                resource_constraint=resource_constraint,
            )
        case _:
            raise NotImplementedError(
                f"[snowpark_connect::unsupported_operation] {called_from}"
            )


def artifacts_reader_wrapper(user_udtf_cls: type) -> type:
    """
    A wrapper to read artifacts from the user-defined UDTF class.
    This is used to read artifacts in the UDTF execution environment.
    """

    class ArtifactsReaderUDTF:
        def __init__(self, *args, **kwargs) -> None:
            try:
                import fcntl
                import os
                import shutil
                import sys
                import tarfile
                import zipfile

                # Change directory to the one containing the UDF imported files
                import_path = sys._xoptions["snowflake_import_directory"]
                if os.name == "nt":
                    import tempfile

                    tmp_path = os.path.join(tempfile.gettempdir(), "sas")
                else:
                    tmp_path = "/tmp/sas"

                sentinel = os.path.join(tmp_path, ".sas_imports_ready")

                if not os.path.exists(sentinel):
                    os.makedirs(tmp_path, exist_ok=True)
                    lock_path = os.path.join(tmp_path, ".sas_imports.lock")
                    with open(lock_path, "w") as lock_fd:
                        fcntl.flock(lock_fd, fcntl.LOCK_EX)
                        try:
                            if not os.path.exists(sentinel):
                                shutil.copytree(
                                    import_path, tmp_path, dirs_exist_ok=True
                                )

                                # Extract all archives.
                                # This has to be done inside the UDF because Snowflake
                                # prevents from loading multiple files with the same
                                # name even though they are in different paths.
                                for archive in os.listdir(tmp_path):
                                    if not archive.endswith(".archive"):
                                        continue
                                    archive_path = os.path.join(tmp_path, archive)
                                    if archive.endswith(
                                        ".zip.archive"
                                    ) or archive.endswith(".jar.archive"):
                                        with zipfile.ZipFile(
                                            archive_path, "r"
                                        ) as zip_ref:
                                            zip_ref.extractall(
                                                archive_path[: -len(".archive")]
                                            )
                                    elif archive.endswith(
                                        ".tar.gz.archive"
                                    ) or archive.endswith(".tgz.archive"):
                                        with tarfile.open(
                                            archive_path, "r:gz"
                                        ) as tar_ref:
                                            tar_ref.extractall(
                                                archive_path[: -len(".archive")]
                                            )
                                    elif archive.endswith(".tar.archive"):
                                        with tarfile.open(archive_path, "r") as tar_ref:
                                            tar_ref.extractall(
                                                archive_path[: -len(".archive")]
                                            )
                                    os.remove(archive_path)

                                open(sentinel, "w").close()
                        finally:
                            fcntl.flock(lock_fd, fcntl.LOCK_UN)

                os.chdir(tmp_path)

                self._user_instance = user_udtf_cls(*args, **kwargs)
                self._user_method = self._user_instance.eval
            except Exception as e:
                raise RuntimeError(
                    f"[UDTF_EXEC_ERROR] User defined table function encountered an error in the '__init__' method: {e}"
                )

        def eval(self, *args, **kwargs):
            return self._user_method(*args, **kwargs)

        def terminate(self, *args, **kwargs):
            if hasattr(self._user_instance, "terminate") and callable(
                self._user_instance.terminate
            ):
                return self._user_instance.terminate(*args, **kwargs)

    return ArtifactsReaderUDTF


def _create_table_arg_helpers():
    """Create the table-argument helpers used by UDTF wrappers.

    Both the ``TableRowProxy`` class and the helper functions are defined *inside* this
    factory so that cloudpickle serializes them **by value** into the handler sent to
    Snowflake. Defining them at module level would pickle them by reference and the
    sandbox (which has no ``snowflake.snowpark_connect`` package) would fail to import
    them at runtime.
    """

    class TableRowProxy:
        """A Row-like object that supports both positional and named access."""

        def __init__(self, fields: list, values: list) -> None:
            self._fields = fields
            self._values = values
            self._field_to_index = {field: i for i, field in enumerate(fields)}

        def __getitem__(self, key):
            if isinstance(key, int):
                # Positional access: row[0], row[1]
                return self._values[key]
            elif isinstance(key, str):
                # Named access: row["col1"], row["col2"]
                if key in self._field_to_index:
                    return self._values[self._field_to_index[key]]
                raise KeyError(f"[snowpark_connect::invalid_operation] {key}")
            else:
                raise TypeError(
                    f"[snowpark_connect::type_mismatch] Invalid key type: {type(key)}"
                )

        def __getattr__(self, name):
            # Attribute access: row.col1, row.col2
            if name.startswith("_"):
                raise AttributeError(f"[snowpark_connect::invalid_operation] {name}")
            if name in self._field_to_index:
                return self._values[self._field_to_index[name]]
            raise AttributeError(f"[snowpark_connect::invalid_operation] {name}")

        def __len__(self):
            return len(self._values)

        def asDict(self, recursive: bool = False):
            """Return the row as a dict, mirroring ``pyspark.sql.Row.asDict``.

            UDTF handlers written for classic Spark receive a real ``Row`` (which
            exposes ``asDict``) for a ``TABLE(...)`` argument; exposing the same
            method here keeps such handlers working unchanged under the native
            table-arg path. ``recursive`` is accepted for signature parity; nested
            values are already plain Python objects, so no recursion is needed.
            """
            return dict(zip(self._fields, self._values))

        def __iter__(self):
            """Iterate over the values in the row"""
            return iter(self._values)

        def __repr__(self):
            field_values = [
                f"{field}={repr(value)}"
                for field, value in zip(self._fields, self._values)
            ]
            return f"Row({', '.join(field_values)})"

    def regroup_flat_table_args(flat_args, table_arg_layout):
        """Regroup a flat positional arg list back into per-eval-param values.

        ``table_arg_layout`` has one entry per UDTF ``eval`` parameter, in order:
          * ``("scalar", None)``  -> consumes one flat arg, passed through unchanged.
          * ``("row", [names])``  -> consumes ``len(names)`` flat args, packed into a
            ``TableRowProxy`` so the handler's single ``row`` param keeps ``row["col"]``
            / ``row[0]`` access without the VARIANT round-trip.
        """
        regrouped: list = []
        idx = 0
        for kind, field_names in table_arg_layout:
            if kind == "row":
                n = len(field_names)
                regrouped.append(
                    TableRowProxy(field_names, list(flat_args[idx : idx + n]))
                )
                idx += n
            else:
                regrouped.append(flat_args[idx])
                idx += 1
        return regrouped

    def convert_table_argument_to_row(arg):
        """Convert table argument structure to appropriate object type."""
        if isinstance(arg, dict):
            if "__fields__" in arg and "__values__" in arg:
                fields = arg["__fields__"]
                values = arg["__values__"]
                return TableRowProxy(fields, values)
            elif arg.get("__struct_marker__", False):
                # This is a struct from named_struct - convert to TableRowProxy for full Row functionality
                # Extract fields and values, excluding the marker
                fields = [k for k in arg.keys() if k != "__struct_marker__"]
                values = [arg[k] for k in fields]
                return TableRowProxy(fields, values)
            else:
                # This is a map - keep as regular dict
                return arg
        return arg

    return convert_table_argument_to_row, regroup_flat_table_args


def spark_compatible_udtf_wrapper(
    user_udtf_cls: type,
    expected_types: list[tuple[str, Any]],
    udtf_name: str | None = None,
    enable_telemetry: bool = True,
    table_arg_layout: list[tuple[str, list | None]] | None = None,
) -> type:
    """
    UDTF Wrapper class to mimic Spark's output type coercion and error handling.
    """

    convert_table_argument_to_row, regroup_flat_table_args = _create_table_arg_helpers()

    def _coerce_to_bool(val: object) -> bool | None:
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            v_str = val.strip().lower()
            if v_str == "true":
                return True
            if v_str == "false":
                return False
        return None

    def _coerce_to_int(val: object) -> int | None:
        if isinstance(val, bool):
            return 1 if val else 0
        if isinstance(val, int):
            return val
        return None

    def _coerce_to_float(val: object) -> float | None:
        if isinstance(val, float):
            return val
        return None

    def _coerce_to_date(val: object) -> datetime.date | None:
        if isinstance(val, datetime.date):
            return val
        if isinstance(val, datetime.datetime):
            return val.date()
        raise AttributeError(
            f"[snowpark_connect::invalid_input] Invalid date value {val}"
        )

    def _coerce_to_binary(val: object, target_type_name: str = "byte") -> bytes | None:
        if target_type_name == "binary":
            if isinstance(val, (bytes, bytearray)):
                return val
            elif isinstance(val, str):
                return val.encode("utf-8")
            return None

        if target_type_name == "byte":
            if isinstance(val, (bytes, bytearray)):
                return val
            elif isinstance(val, int):
                return str(val).encode("utf-8")

        return None

    def _coerce_to_decimal(val: object) -> decimal.Decimal | None:
        if isinstance(val, decimal.Decimal):
            return val
        return None

    def _coerce_to_py_string(val: object) -> str | None:
        if val is None:
            return None

        # Special handling for dictionaries to match PySpark format
        if isinstance(val, dict):
            # Format dictionaries using "=" instead of ":" for key-value pairs
            dict_items = [f"{k}={v}" for k, v in val.items()]
            return "{" + ", ".join(dict_items) + "}"

        return str(val)

    def _coerce_generic_scalar(
        val: object, target_py_type: str, marker: object = None
    ) -> object | None:
        if val is None:
            return None

        if isinstance(marker, dict) and "dict" in marker:
            # If expected type is a dict but val is not a dict, return None
            if not isinstance(val, dict):
                return None
            key_type_info, value_type_info = marker["dict"]
            return {
                _spark_coerce_value_recursive(
                    k, key_type_info
                ): _spark_coerce_value_recursive(v, value_type_info)
                for k, v in val.items()
            }

        if target_py_type == "object":
            return val
        try:
            typ = getattr(builtins, target_py_type)
            return typ(val)
        except (ValueError, TypeError):
            return None

    def _coerce_to_timestamp(val: object) -> datetime.datetime | None:
        if isinstance(val, datetime.datetime):
            return val
        raise AttributeError(
            f"[snowpark_connect::invalid_input] Invalid time stamp value {val}"
        )

    SCALAR_COERCERS = {
        "bool": _coerce_to_bool,
        "int": _coerce_to_int,
        "float": _coerce_to_float,
        "datetime.date": _coerce_to_date,
        "datetime.datetime": _coerce_to_timestamp,
        "bytes": _coerce_to_binary,
        "bytearray": _coerce_to_binary,
        "decimal.Decimal": _coerce_to_decimal,
        "str": _coerce_to_py_string,
    }

    def _spark_coerce_value_recursive(
        val: object, type_info_tuple: tuple[str, object]
    ) -> object | None:
        """
        We will try to coerce the value returned by the user process method to the expected type.
        """
        kind, py_type_or_struct_info = type_info_tuple

        if kind == "scalar":
            target_py_type, marker = py_type_or_struct_info
            coercer = SCALAR_COERCERS.get(target_py_type)
            if coercer:
                if marker == "binary":
                    return coercer(val, marker)
                return coercer(val)
            return _coerce_generic_scalar(val, target_py_type, marker)

        elif kind == "array":
            element_type_info = py_type_or_struct_info
            if not isinstance(val, (list, tuple)):
                return None
            return [_spark_coerce_value_recursive(v, element_type_info) for v in val]

        elif kind == "struct":
            struct_fields_info = py_type_or_struct_info
            if val is None:
                return {fname: None for fname in struct_fields_info}
            coerced_struct = {}
            if isinstance(val, dict):
                for fname, field_type_info in struct_fields_info.items():
                    coerced_struct[fname] = _spark_coerce_value_recursive(
                        val.get(fname), field_type_info
                    )
            elif isinstance(val, (tuple, list)):
                field_names = list(struct_fields_info.keys())
                for i, fname in enumerate(field_names):
                    field_type_info = struct_fields_info[fname]
                    v = val[i] if i < len(val) else None
                    coerced_struct[fname] = _spark_coerce_value_recursive(
                        v, field_type_info
                    )
            else:
                for fname, field_type_info in struct_fields_info.items():
                    v = getattr(val, fname, None)
                    coerced_struct[fname] = _spark_coerce_value_recursive(
                        v, field_type_info
                    )
            return coerced_struct
        else:
            return val

    class WrappedUDTF:
        def __init__(self, *args, **kwargs) -> None:
            try:
                self._user_instance = user_udtf_cls(*args, **kwargs)
                self._user_method = self._user_instance.eval
            except Exception as e:
                raise RuntimeError(
                    f"[UDTF_EXEC_ERROR] User defined table function encountered an error in the '__init__' method: {e}"
                )

        def process(self, *args, **kwargs):
            # Emit telemetry start event (inline, mirroring UDF pattern)
            if enable_telemetry:
                try:
                    from snowflake import telemetry

                    telemetry.set_span_attribute(
                        "udtf.name", udtf_name or "anonymous_udtf"
                    )
                    telemetry.add_event("udtf_invocation_start", {})
                except Exception:
                    # Silently ignore telemetry errors to not affect UDTF execution
                    pass

            try:
                # Pre-process args and kwargs to convert SqlNullWrapper to None before calling user's eval
                processed_args = [
                    None if type(arg).__name__ == "sqlNullWrapper" else arg
                    for arg in args
                ]
                processed_kwargs = {
                    k: (None if type(v).__name__ == "sqlNullWrapper" else v)
                    for k, v in kwargs.items()
                }

                if table_arg_layout is not None:
                    # Native table-arg path: the physical function has one native column
                    # per table field, so regroup the flat args back into the single Row
                    # the handler expects (no VARIANT __fields__/__values__ round-trip).
                    processed_args = regroup_flat_table_args(
                        tuple(processed_args), table_arg_layout
                    )
                else:
                    # Convert table arguments to Row-like objects that support both positional and named access
                    processed_args = [
                        convert_table_argument_to_row(arg) for arg in processed_args
                    ]
                    processed_kwargs = {
                        k: convert_table_argument_to_row(v)
                        for k, v in processed_kwargs.items()
                    }

                result_iter = self._user_method(*processed_args, **processed_kwargs)
                if result_iter is None:
                    return  # Do not yield anything, so result is []

                for raw_row_tuple in result_iter:
                    if raw_row_tuple is None:
                        yield tuple([None] * len(expected_types))
                        continue

                    if not isinstance(raw_row_tuple, (tuple, list)):
                        raise TypeError(
                            f"[snowpark_connect::type_mismatch] [UDTF_INVALID_OUTPUT_ROW_TYPE] return value should be an iterable object containing tuples, but got {type(raw_row_tuple)}"
                        )

                    if len(raw_row_tuple) != len(expected_types):
                        raise RuntimeError(
                            f"[UDTF_RETURN_SCHEMA_MISMATCH] The number of columns in the result does not match the specified schema. Expected {len(expected_types)} columns, but got {len(raw_row_tuple)}"
                        )

                    # Check for struct type mismatch
                    for i, (val, type_info) in enumerate(
                        zip(raw_row_tuple, expected_types)
                    ):
                        kind, type_marker = type_info
                        # If expected type is struct but received a scalar primitive value
                        if (
                            kind == "struct"
                            and not isinstance(val, (dict, list, tuple))
                            and val is not None
                        ):
                            raise RuntimeError(
                                f"[snowpark_connect::type_mismatch] [UNEXPECTED_TUPLE_WITH_STRUCT] Expected a struct for column at position {i}, but got a primitive value of type {type(val)}"
                            )

                    coerced_row_list = [None] * len(expected_types)
                    for i, (val, type_info) in enumerate(
                        zip(raw_row_tuple, expected_types)
                    ):
                        coerced_row_list[i] = _spark_coerce_value_recursive(
                            val, type_info
                        )

                    yield tuple(coerced_row_list)
            finally:
                # Emit telemetry complete event
                if enable_telemetry:
                    try:
                        from snowflake import telemetry

                        telemetry.add_event("udtf_invocation_complete", {})
                    except Exception:
                        pass

        def end_partition(self, *args, **kwargs):
            if hasattr(self._user_instance, "terminate") and callable(
                self._user_instance.terminate
            ):
                return self._user_instance.terminate(*args, **kwargs)

    return WrappedUDTF


def spark_compatible_udtf_wrapper_with_arrow(
    user_udtf_cls: type,
    expected_types: list[tuple[str, Any]],
    udtf_name: str | None = None,
    enable_telemetry: bool = True,
    table_arg_layout: list[tuple[str, list | None]] | None = None,
) -> type:
    import pyarrow as pa

    convert_table_argument_to_row, regroup_flat_table_args = _create_table_arg_helpers()

    def _python_type_to_arrow_type_impl(
        type_info_tuple: tuple[str, Any],
    ) -> pa.DataType:
        kind, type_marker = type_info_tuple
        if kind == "scalar":
            target_py_type, marker_val = type_marker
            match target_py_type, marker_val:
                case "int", "byte":
                    return pa.int8()
                case "str", _:
                    return pa.string()
                case "bool", _:
                    return pa.bool_()
                case "int", _:
                    return pa.int64()
                case "float", _:
                    return pa.float64()
                case "bytes", _:
                    return pa.binary()
                case "bytearray", _:
                    return pa.binary()
                case "decimal.Decimal", mv:
                    if isinstance(mv, dict) and mv.get("type") == "decimal":
                        precision = mv.get("precision", 10)
                        scale = mv.get("scale", 0)
                        return pa.decimal128(precision, scale)
                    else:
                        return pa.decimal128(38, 18)
                case "datetime.date", _:
                    return pa.date32()
                case "datetime.datetime", _:
                    return pa.timestamp("us", tz=None)
                case _, mv if isinstance(mv, dict) and "dict" in mv:
                    key_info, value_info = marker_val["dict"]
                    key_type = _python_type_to_arrow_type_impl(key_info)
                    value_type = _python_type_to_arrow_type_impl(value_info)
                    return pa.map_(key_type, value_type)
                case _, _:
                    raise TypeError(
                        f"[snowpark_connect::unsupported_type] [UDTF_ARROW_TYPE_CAST_ERROR] Unsupported Python scalar type for Arrow conversion: {target_py_type}"
                    )
        elif kind == "array":
            element_type_info = type_marker
            element_arrow_type = _python_type_to_arrow_type_impl(element_type_info)
            return pa.list_(element_arrow_type)
        elif kind == "struct":
            struct_fields_info = type_marker
            if not isinstance(struct_fields_info, dict):
                raise TypeError(
                    f"[snowpark_connect::type_mismatch] [UDTF_ARROW_TYPE_CAST_ERROR] Invalid struct definition for Arrow: expected dict, got {type(struct_fields_info)}"
                )
            fields = []
            for field_name, field_type_info in struct_fields_info.items():
                field_arrow_type = _python_type_to_arrow_type_impl(field_type_info)
                fields.append(pa.field(field_name, field_arrow_type))
            return pa.struct(fields)
        else:
            raise TypeError(
                f"[snowpark_connect::unsupported_type] [UDTF_ARROW_TYPE_CAST_ERROR] Unsupported data kind for Arrow conversion: {kind}"
            )

    def _convert_to_arrow_value(
        obj: Any, arrow_type: pa.DataType, parent_container_type: str | None = None
    ) -> Any:
        if obj is None:
            return None

        if pa.types.is_list(arrow_type):
            if isinstance(obj, dict):
                # When dict is provided for array type, extract keys
                return [
                    _convert_to_arrow_value(k, arrow_type.value_type, "array")
                    for k in obj.keys()
                ]
            if isinstance(obj, str):
                # When string is provided for array type, split into characters
                return [
                    _convert_to_arrow_value(char, arrow_type.value_type, "array")
                    for char in obj
                ]
            if not isinstance(obj, (list, tuple)):
                raise TypeError(
                    f"[snowpark_connect::type_mismatch] [UDTF_ARROW_TYPE_CAST_ERROR] Expected list or tuple for Arrow array type, got {type(obj).__name__}"
                )
            element_type = arrow_type.value_type
            return [_convert_to_arrow_value(e, element_type, "array") for e in obj]

        if pa.types.is_map(arrow_type):
            if not isinstance(obj, dict):
                raise TypeError(
                    f"[snowpark_connect::type_mismatch] [UDTF_ARROW_TYPE_CAST_ERROR] Expected dict for Arrow map type, got {type(obj).__name__}"
                )
            key_type = arrow_type.key_type
            value_type = arrow_type.item_type
            return {
                _convert_to_arrow_value(k, key_type): _convert_to_arrow_value(
                    v, value_type
                )
                for k, v in obj.items()
            }

        if pa.types.is_struct(arrow_type):
            names = [field.name for field in arrow_type]
            field_arrow_types = [field.type for field in arrow_type]

            if isinstance(obj, dict):
                output_struct_dict = {}
                for i, name in enumerate(names):
                    field_type = field_arrow_types[i]
                    output_struct_dict[name] = _convert_to_arrow_value(
                        obj.get(name), field_type, "struct"
                    )
                return output_struct_dict
            else:
                # If the UDTF yields a list/tuple (or anything not a dict) for a struct column, it's an error.
                raise TypeError(
                    f"[snowpark_connect::type_mismatch] [UDTF_ARROW_TYPE_CAST_ERROR] Expected a dictionary for Arrow struct type column, but got {type(obj).__name__}"
                )

        # Check if a scalar type is expected and if obj is a collection; if so, error out.
        # This must be after handling list, map, struct which are collections themselves.
        if not (
            pa.types.is_list(arrow_type)
            or pa.types.is_map(arrow_type)
            or pa.types.is_struct(arrow_type)
        ):
            if isinstance(obj, (list, tuple, dict)):
                raise TypeError(
                    f"[snowpark_connect::type_mismatch] [UDTF_ARROW_TYPE_CAST_ERROR] Cannot convert Python collection type {type(obj).__name__} to scalar Arrow type {arrow_type}"
                )

        if pa.types.is_boolean(arrow_type):
            if isinstance(obj, bool):
                return obj
            # For array elements, allow conversion from numbers
            if parent_container_type == "array" and isinstance(obj, (int, float)):
                return bool(obj)
            # Only convert numbers 0 and 1 to boolean for non-array contexts
            if isinstance(obj, (int, float)):
                if obj == 0:
                    return False
                elif obj == 1:
                    return True
                raise TypeError(
                    f"[snowpark_connect::type_mismatch] [UDTF_ARROW_TYPE_CAST_ERROR] Cannot convert {obj} to Arrow boolean"
                )
            if isinstance(obj, str):
                v_str = obj.strip().lower()
                if v_str == "true":
                    return True
                if v_str == "false":
                    return False
            raise TypeError(
                f"[snowpark_connect::type_mismatch] [UDTF_ARROW_TYPE_CAST_ERROR] Cannot convert {type(obj).__name__} to Arrow boolean"
            )

        if pa.types.is_integer(arrow_type):
            if isinstance(obj, bool):
                return int(obj)
            if isinstance(obj, int):
                return obj
            if isinstance(obj, float):
                return int(obj)
            if isinstance(obj, str):
                try:
                    return int(obj)
                except ValueError:
                    pass
            raise TypeError(
                f"[snowpark_connect::type_mismatch] [UDTF_ARROW_TYPE_CAST_ERROR] Cannot convert {type(obj).__name__} to Arrow integer"
            )

        if pa.types.is_floating(arrow_type):
            if isinstance(obj, (int, float)):
                return float(obj)
            if isinstance(obj, str):
                try:
                    return float(obj)
                except ValueError:
                    pass
            raise TypeError(
                f"[snowpark_connect::type_mismatch] [UDTF_ARROW_TYPE_CAST_ERROR] Cannot convert {type(obj).__name__} to Arrow float"
            )

        if pa.types.is_string(arrow_type):
            # For array elements and struct fields, allow conversion from numeric types
            if parent_container_type in ["array", "struct"] and isinstance(
                obj, (int, float, bool)
            ):
                return str(obj)
            if isinstance(obj, str):
                return obj
            raise TypeError(
                f"[snowpark_connect::type_mismatch] [UDTF_ARROW_TYPE_CAST_ERROR] Cannot convert {type(obj).__name__} to Arrow string"
            )

        if pa.types.is_binary(arrow_type) or pa.types.is_fixed_size_binary(arrow_type):
            if isinstance(obj, (bytes, bytearray)):
                return bytes(obj)
            if isinstance(obj, str):
                return bytearray(obj.encode("utf-8"))
            if isinstance(obj, int):
                return bytearray([obj])
            raise TypeError(
                f"[snowpark_connect::type_mismatch] [UDTF_ARROW_TYPE_CAST_ERROR] Cannot convert {type(obj).__name__} to Arrow binary"
            )

        if pa.types.is_date(arrow_type):
            if isinstance(obj, datetime.date):
                return obj
            raise TypeError(
                f"[snowpark_connect::type_mismatch] [UDTF_ARROW_TYPE_CAST_ERROR] Cannot convert {type(obj).__name__} to Arrow date. Expected datetime.date."
            )

        if pa.types.is_timestamp(arrow_type):
            if isinstance(obj, datetime.datetime):
                return obj
            raise TypeError(
                f"[snowpark_connect::type_mismatch] [UDTF_ARROW_TYPE_CAST_ERROR] Cannot convert {type(obj).__name__} to Arrow timestamp. Expected datetime.datetime."
            )

        if pa.types.is_decimal(arrow_type):
            if isinstance(obj, decimal.Decimal):
                return obj
            if isinstance(obj, int):
                return decimal.Decimal(obj)
            if isinstance(obj, str):
                try:
                    return decimal.Decimal(obj)
                except decimal.InvalidOperation:
                    pass

            raise TypeError(
                f"[snowpark_connect::type_mismatch] [UDTF_ARROW_TYPE_CAST_ERROR] Cannot convert {type(obj).__name__} to Arrow decimal. Expected decimal.Decimal or compatible int/str."
            )

        raise TypeError(
            f"[snowpark_connect::unsupported_operation] [UDTF_ARROW_TYPE_CAST_ERROR] Unsupported type conversion for {type(obj).__name__} to Arrow type {arrow_type}"
        )

    class WrappedUDTF:
        def __init__(self, *args, **kwargs) -> None:
            try:
                self._user_instance = user_udtf_cls(*args, **kwargs)
                self._user_method = self._user_instance.eval
            except Exception as e:
                raise RuntimeError(
                    f"[UDTF_EXEC_ERROR] User defined table function encountered an error in the '__init__' method: {e}"
                )

        def process(self, *args, **kwargs):
            # Emit telemetry start event (inline, mirroring UDF pattern)
            if enable_telemetry:
                try:
                    from snowflake import telemetry

                    telemetry.set_span_attribute(
                        "udtf.name", udtf_name or "anonymous_udtf"
                    )
                    telemetry.add_event("udtf_invocation_start", {})
                except Exception:
                    # Silently ignore telemetry errors to not affect UDTF execution
                    pass

            try:
                # Pre-process args and kwargs to convert SqlNullWrapper to None before calling user's eval
                processed_args = [
                    None if type(arg).__name__ == "sqlNullWrapper" else arg
                    for arg in args
                ]
                processed_kwargs = {
                    k: (None if type(v).__name__ == "sqlNullWrapper" else v)
                    for k, v in kwargs.items()
                }

                if table_arg_layout is not None:
                    # Native table-arg path: regroup the flat native columns back into
                    # the single Row the handler expects (see plain wrapper for details).
                    processed_args = regroup_flat_table_args(
                        tuple(processed_args), table_arg_layout
                    )
                else:
                    # Convert table arguments and regular dicts to Row-like objects that support both positional and named access
                    processed_args = [
                        convert_table_argument_to_row(arg) for arg in processed_args
                    ]
                    processed_kwargs = {
                        k: convert_table_argument_to_row(v)
                        for k, v in processed_kwargs.items()
                    }

                result_iter = self._user_method(*processed_args, **processed_kwargs)
                if result_iter is None:
                    return  # Do not yield anything, so result is []

                for raw_row_output in result_iter:
                    if not isinstance(raw_row_output, (tuple,)):
                        if len(expected_types) == 1:
                            raw_row_tuple = (raw_row_output,)
                        else:  # If multiple output columns expected, but not a tuple, this is a mismatch
                            raise ValueError(
                                f"[UDTF_RETURN_SCHEMA_MISMATCH] Expected a tuple of length {len(expected_types)} for multiple output columns, but got {type(raw_row_output).__name__}"
                            )
                    else:
                        raw_row_tuple = raw_row_output

                    if len(raw_row_tuple) != len(expected_types):
                        raise ValueError(
                            f"[UDTF_RETURN_SCHEMA_MISMATCH] The number of columns in the result does not match the specified schema. Expected {len(expected_types)} columns, but got {len(raw_row_tuple)}"
                        )

                    coerced_row_list = [None] * len(expected_types)
                    for i, (val, type_info) in enumerate(
                        zip(raw_row_tuple, expected_types)
                    ):
                        arrow_type = _python_type_to_arrow_type_impl(type_info)
                        coerced_row_list[i] = _convert_to_arrow_value(val, arrow_type)

                    yield tuple(coerced_row_list)
            finally:
                # Emit telemetry complete event
                if enable_telemetry:
                    try:
                        from snowflake import telemetry

                        telemetry.add_event("udtf_invocation_complete", {})
                    except Exception:
                        pass

        def end_partition(self, *args, **kwargs):
            if hasattr(self._user_instance, "terminate") and callable(
                self._user_instance.terminate
            ):
                return self._user_instance.terminate(*args, **kwargs)

    return WrappedUDTF
