#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

# Note: this class will be loaded in a stored procedure to create a Python UDF with different Python version.
# So its dependencies are restricted to pandas, snowpark, and, pyspark
import functools
import inspect
import logging
from typing import Callable

import pandas
import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
from pyspark.serializers import CloudPickleSerializer

import snowflake.snowpark.context as context
import snowflake.snowpark.functions as snowpark_fn
from snowflake.snowpark._internal.udf_utils import extract_return_input_types
from snowflake.snowpark._internal.utils import TempObjectType
from snowflake.snowpark.types import (
    ArrayType,
    DataType,
    MapType,
    PandasDataFrameType,
    StringType,
    StructType,
    TimestampTimeZone,
    TimestampType,
    VariantType,
)

MAP_IN_ARROW_EVAL_TYPE = 207

# Package names for UDFs
TELEMETRY_PACKAGE = "snowflake-telemetry-python"

# Flag to enable/disable automatic telemetry wrapper for UDFs
# When True, UDFs will automatically emit telemetry events at start/completion
ENABLE_UDF_TELEMETRY = True

logger = logging.getLogger(__name__)


def create_telemetry_wrapper(func, udf_name):
    """
    Create a wrapper function that adds telemetry tracing to UDF execution.
    Uses Snowflake's built-in telemetry API to record trace events to the Event Table.

    NOTE: Uses module-level functions (telemetry.add_event, telemetry.set_span_attribute)
    as per Snowflake documentation, NOT get_active_span() which is an OpenTelemetry pattern.
    """

    @functools.wraps(func)
    def telemetry_wrapper(*args, **kwargs):
        try:
            from snowflake import telemetry

            telemetry.set_span_attribute("udf.name", udf_name or "anonymous_udf")
            telemetry.add_event("udf_invocation_start", {})
        except Exception:
            # Silently ignore telemetry errors to not affect UDF execution
            pass

        result = func(*args, **kwargs)

        try:
            from snowflake import telemetry

            telemetry.add_event("udf_invocation_complete", {})
        except Exception:
            pass

        return result

    return telemetry_wrapper


def _get_resource_constraint() -> dict[str, str] | None:
    """Get resource constraint from config if enabled.

    Returns:
        A dict with architecture constraint (e.g., {"architecture": "x86"}) if configured,
        otherwise None.
    """
    from snowflake.snowpark_connect.config import global_config

    arch = global_config.get("snowpark.connect.udf.resource_constraint.architecture")
    if arch:
        return {"architecture": arch}
    return None


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


def build_timestamp_return_descriptor(sf_type):
    """
    Build a lightweight, cloudpickle-safe descriptor of the TimestampType leaves
    within a Snowpark return type, or None when the type contains no timestamp.

    The descriptor drives ``create_timestamp_return_wrapper`` so that timestamps
    nested in Array/Map/Struct return values are normalised (not just scalar
    TIMESTAMP returns). Shapes:
      - timestamp:  ("ts", is_ntz)
      - array:      ("array", element_desc)
      - map:        ("map", key_desc, value_desc)
      - struct:     ("struct", [(field_name, field_desc), ...])
    """
    if isinstance(sf_type, TimestampType):
        return ("ts", sf_type.tz == TimestampTimeZone.NTZ)
    if isinstance(sf_type, ArrayType):
        inner = build_timestamp_return_descriptor(sf_type.element_type)
        return ("array", inner) if inner is not None else None
    if isinstance(sf_type, MapType):
        key_desc = build_timestamp_return_descriptor(sf_type.key_type)
        val_desc = build_timestamp_return_descriptor(sf_type.value_type)
        if key_desc is not None or val_desc is not None:
            return ("map", key_desc, val_desc)
        return None
    if isinstance(sf_type, StructType):
        fields = [
            (f.name, build_timestamp_return_descriptor(f.datatype))
            for f in sf_type.fields
        ]
        if any(d is not None for _, d in fields):
            return ("struct", fields)
        return None
    return None


def create_timestamp_return_wrapper(func: Callable, descriptor) -> Callable:
    """
    Convert the ``datetime`` values in a UDF's return to the naive form the
    TIMESTAMP return column expects, matching PySpark (verified against
    test_function_year / test_function_year_plus) and mirroring the Scala
    UdfPacketUtils rule (LTZ uses the session timezone, NTZ uses UTC). Handles
    timestamps nested inside Array/Map/Struct via ``descriptor`` (built by
    ``build_timestamp_return_descriptor``).

    Per timestamp leaf:
      - TIMESTAMP_NTZ: the value is the wall clock. A naive datetime is returned
        unchanged; a tz-aware one is converted to UTC and stripped.
      - TIMESTAMP_LTZ / default: the value denotes a UTC instant (a naive value
        is treated as UTC), expressed in the explicit session timezone ($TZ)
        with tzinfo dropped, so TIMESTAMP_LTZ (which re-interprets the naive
        value in the session timezone) stores the same instant. E.g. a returned
        2025-03-01 15:30:00 displays as 07:30 in America/Los_Angeles.

    This also avoids Snowflake rejecting a tz-aware datetime on the return path
    ("Datetime object must be naive to be convertible to TIMESTAMP_LTZ").
    """
    import datetime as _dt
    import os as _os

    import pytz as _pytz

    def _conv_leaf(value, is_ntz, session_zone):
        if not isinstance(value, _dt.datetime):
            return value
        if is_ntz:
            if value.tzinfo is not None:
                return value.astimezone(_pytz.utc).replace(tzinfo=None)
            return value
        if value.tzinfo is None:
            value = _pytz.utc.localize(value)
        return value.astimezone(session_zone).replace(tzinfo=None)

    def _walk(value, desc, session_zone):
        if value is None or desc is None:
            return value
        kind = desc[0]
        if kind == "ts":
            return _conv_leaf(value, desc[1], session_zone)
        if kind == "array":
            if isinstance(value, (list, tuple)):
                return [_walk(v, desc[1], session_zone) for v in value]
            return value
        if kind == "map":
            if isinstance(value, dict):
                key_desc, val_desc = desc[1], desc[2]
                return {
                    (
                        _walk(k, key_desc, session_zone) if key_desc is not None else k
                    ): _walk(v, val_desc, session_zone)
                    for k, v in value.items()
                }
            return value
        if kind == "struct":
            fields = desc[1]
            if isinstance(value, dict):
                # struct results are dicts keyed by field name (case may differ).
                lower_to_actual = {k.lower(): k for k in value}
                result = dict(value)
                for fname, fdesc in fields:
                    if fdesc is None:
                        continue
                    actual = lower_to_actual.get(fname.lower())
                    if actual is not None:
                        result[actual] = _walk(result[actual], fdesc, session_zone)
                return result
            if isinstance(value, (list, tuple)) and len(value) == len(fields):
                return type(value)(
                    _walk(v, fdesc, session_zone) if fdesc is not None else v
                    for (_, fdesc), v in zip(fields, value)
                )
            return value
        return value

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Resolve the session timezone once per invocation (not per leaf).
        return _walk(
            func(*args, **kwargs),
            descriptor,
            _pytz.timezone(_os.environ.get("TZ", "UTC")),
        )

    return wrapper


def create_schema_json_coercion_wrapper(func: Callable) -> Callable:
    """
    Wrap a UDF to coerce its arguments based on a per-call schema_json sidecar
    appended as the last positional argument by the call site.

    This works around the type information lost when Snowflake VARIANT
    round-trips Python values:
    - FLOAT/DOUBLE: integer-valued floats (e.g. ``1.0``) collapse to ``int``.
    - TIMESTAMP*: timestamps become ISO-formatted strings instead of
      ``datetime.datetime``.  The UDF receives the naive wall-clock value (any
      LTZ offset is stripped), matching PySpark's Python-UDF contract for both
      TIMESTAMP_NTZ and TIMESTAMP_LTZ.
    - DATE: dates become date strings instead of ``datetime.date``.
    - Compound types (array, map, struct) are handled recursively, so
      timestamps nested inside lists or dicts are also restored.

    PySpark always passes the call-site Spark type to Python, so we restore
    that contract on the SAS side using the type metadata captured at
    SQL-resolution time.

    The schema_json (a JSON-encoded list of Spark type descriptors, one per
    real argument) is appended by ``map_unresolved_function`` whenever the
    wrapped UDF has ``attach_schema_json=True``. Values whose type needs no
    special handling are passed through unchanged.

    IMPORTANT: helpers are defined as nested functions (not module-level
    references) so that cloudpickle serialises them as code objects. If they
    were referenced as module-level globals, cloudpickle would try to resolve
    them via ``import snowflake.snowpark_connect.utils.udf_utils``, which is
    not available inside Snowflake's UDF runtime.
    """
    import datetime as _dt
    import json as _json
    import re as _re

    _TS_TYPES = frozenset(
        {"timestamp", "timestamp_ntz", "timestamp_ltz", "timestamp_tz"}
    )
    _TZ_RE = _re.compile(r"\s+([+-]\d{2}:?\d{2}|UTC|Z)$")

    def _parse_ts(s):
        # Match the datetime PySpark delivers to a Python UDF. The
        # distinguishing signal is whether the VARIANT string carries a UTC
        # offset, not the declared type:
        #   - offset present (LTZ / instant): convert to UTC and drop tzinfo,
        #     e.g. "2025-03-01 07:30:00 -0800" -> 2025-03-01 15:30:00.
        #   - no offset (NTZ / wall clock): return the naive value as-is,
        #     e.g. "2025-03-01 10:30:00" -> 2025-03-01 10:30:00.
        # Remove the space before a trailing offset and normalise the offset so
        # datetime.fromisoformat accepts it on every supported runtime: map
        # " UTC"/" Z" to "+00:00" and insert a colon into colon-less offsets
        # ("-0800" -> "-08:00"). Python < 3.11 rejects colon-less offsets and
        # bare "Z", so without this the LTZ path would silently fall back to the
        # raw string on 3.10 clients.
        def _norm_offset(m):
            tok = m.group(1)
            if tok in ("UTC", "Z"):
                return "+00:00"
            return tok if ":" in tok else tok[:3] + ":" + tok[3:]

        normalized = _TZ_RE.sub(_norm_offset, s)
        try:
            parsed = _dt.datetime.fromisoformat(normalized)
        except ValueError:
            return s
        if parsed.tzinfo is not None:
            return parsed.astimezone(_dt.timezone.utc).replace(tzinfo=None)
        return parsed

    def _coerce(value, type_desc):
        if value is None:
            return None
        if isinstance(type_desc, str):
            if type_desc in ("double", "float"):
                if not isinstance(value, float):
                    try:
                        return float(value)
                    except (TypeError, ValueError):
                        return value
            elif type_desc in _TS_TYPES:
                if isinstance(value, str):
                    return _parse_ts(value)
            elif type_desc == "date":
                if isinstance(value, str):
                    try:
                        return _dt.date.fromisoformat(value)
                    except ValueError:
                        return value
            return value
        if isinstance(type_desc, dict):
            kind = type_desc.get("type")
            if kind == "array" and isinstance(value, list):
                elem_type = type_desc.get("element_type")
                if elem_type is not None:
                    return [_coerce(v, elem_type) for v in value]
            elif kind == "map" and isinstance(value, dict):
                key_type = type_desc.get("key_type")
                val_type = type_desc.get("value_type")
                if val_type is not None:
                    if key_type is not None:
                        return {
                            _coerce(k, key_type): _coerce(v, val_type)
                            for k, v in value.items()
                        }
                    return {k: _coerce(v, val_type) for k, v in value.items()}
            elif kind == "struct" and isinstance(value, dict):
                fields = type_desc.get("fields", [])
                if fields:
                    # Snowpark upper-cases field names; match case-insensitively.
                    lower_to_actual = {k.lower(): k for k in value}
                    result = dict(value)
                    for field in fields:
                        desc_name = field.get("name", "")
                        actual_key = lower_to_actual.get(desc_name.lower())
                        if actual_key is not None:
                            result[actual_key] = _coerce(
                                value[actual_key], field.get("type")
                            )
                    return result
        return value

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not args:
            return func(*args, **kwargs)
        *real_args, schema_json = args
        if isinstance(schema_json, str) and schema_json:
            try:
                schema = _json.loads(schema_json)
            except (ValueError, TypeError):
                logger.debug(
                    "schema_json sidecar failed to parse; skipping UDF arg coercion",
                    exc_info=True,
                )
                schema = None
            if isinstance(schema, list) and len(schema) == len(real_args):
                real_args = [_coerce(v, t) for v, t in zip(real_args, schema)]
        return func(*real_args, **kwargs)

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
        artifact_repository: str | None = None,
        resource_constraint: dict[str, str] | None = None,
        coerce_via_schema_json: bool = False,
    ) -> None:
        context._use_structured_type_semantics = True
        context._is_snowpark_connect_compatible_mode = True

        self._function_name = common_inline_user_defined_function.function_name
        self._is_deterministic = common_inline_user_defined_function.deterministic
        self._arguments = common_inline_user_defined_function.arguments
        self._function_type = common_inline_user_defined_function.WhichOneof("function")
        self._input_types = input_types
        # When True (set for UDFs registered via spark.udf.register that have
        # no explicit input types), the registered UDF accepts an extra
        # trailing string argument carrying the call-site Spark types as
        # JSON; the wrapper uses it to coerce values whose precise type is
        # lost when round-tripping through Snowflake VARIANT (notably
        # integer-valued FloatType/DoubleType).  See
        # ``create_schema_json_coercion_wrapper``.
        self._coerce_via_schema_json = coerce_via_schema_json
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
        self._artifact_repository = artifact_repository
        self._resource_constraint = resource_constraint
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
        defaulted_input_types_to_variant = False

        def update_none_input_types():
            nonlocal defaulted_input_types_to_variant
            if self._input_types is None:
                # If any of the parameters don't have type hint, we use Snowflake Variant type.
                func_signature = inspect.signature(callable_func)
                self._input_types = [VariantType()] * len(func_signature.parameters)
                defaulted_input_types_to_variant = True

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

                tmp_path = os.path.join(tempfile.gettempdir(), "sas")
            else:
                tmp_path = "/tmp/sas"

            sentinel = os.path.join(tmp_path, ".sas_imports_ready")

            # Fast path: if a previous invocation already prepared the directory, just chdir.
            if os.path.exists(sentinel):
                os.chdir(tmp_path)
                return

            # Acquire an exclusive lock so only one process/thread copies and extracts.
            import fcntl

            os.makedirs(tmp_path, exist_ok=True)
            lock_path = os.path.join(tmp_path, ".sas_imports.lock")
            with open(lock_path, "w") as lock_fd:
                fcntl.flock(lock_fd, fcntl.LOCK_EX)
                try:
                    # Re-check after acquiring the lock (another process may have finished).
                    if not os.path.exists(sentinel):
                        shutil.copytree(import_path, tmp_path, dirs_exist_ok=True)

                        # Extract all archives.
                        # This has to be done inside the UDF because Snowflake prevents
                        # from loading multiple files with the same name even though they
                        # are in different paths.
                        for archive in os.listdir(tmp_path):
                            if not archive.endswith(".archive"):
                                continue
                            archive_path = os.path.join(tmp_path, archive)
                            if archive.endswith(".zip.archive") or archive.endswith(
                                ".jar.archive"
                            ):
                                with zipfile.ZipFile(archive_path, "r") as zip_ref:
                                    zip_ref.extractall(archive_path[: -len(".archive")])
                            elif archive.endswith(
                                ".tar.gz.archive"
                            ) or archive.endswith(".tgz.archive"):
                                with tarfile.open(archive_path, "r:gz") as tar_ref:
                                    tar_ref.extractall(archive_path[: -len(".archive")])
                            elif archive.endswith(".tar.archive"):
                                with tarfile.open(archive_path, "r") as tar_ref:
                                    tar_ref.extractall(archive_path[: -len(".archive")])
                            os.remove(archive_path)

                        # Signal that the directory is ready for all subsequent calls.
                        open(sentinel, "w").close()
                finally:
                    fcntl.flock(lock_fd, fcntl.LOCK_UN)

            os.chdir(tmp_path)

        if self._udf_packages:
            packages = [p.strip() for p in self._udf_packages.strip("[]").split(",")]
        else:
            packages = []
        # TODO: Remove this once Snowpark Python automatically includes cloudpickle when artifact_repository is set.
        # cloudpickle is required for serialization/deserialization of UDFs but is not automatically
        # added by Snowflake when using a custom artifact_repository.
        if self._artifact_repository and "cloudpickle" not in packages:
            packages.append("cloudpickle")

        # Add telemetry package for UDF tracing (only if telemetry is enabled)
        if ENABLE_UDF_TELEMETRY and TELEMETRY_PACKAGE not in packages:
            packages.append(TELEMETRY_PACKAGE)
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

        # eval_type 200 = SQL_SCALAR_PANDAS_UDF: the function should receive
        # and return pd.Series (vectorized). Force annotations when the user
        # omitted type hints so Snowpark creates a vectorized UDF.
        if self._eval_type == 200:
            existing = getattr(original_callable, "__annotations__", {})
            has_pandas_hints = any(
                v in (pandas.Series, pandas.DataFrame) for v in existing.values()
            )
            if not has_pandas_hints:
                sig = inspect.signature(original_callable)
                callable_func.__annotations__ = {
                    p: pandas.Series for p in sig.parameters
                }
                callable_func.__annotations__["return"] = pandas.Series

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

        # SNOW-3381818/SNOW-3595424: when the caller asked for schema-driven
        # coercion AND we ended up defaulting to all-Variant inputs, splice in
        # an extra trailing StringType input that carries the call-site Spark
        # type metadata and wrap the user callable so it strips and consumes
        # that arg.  This restores type fidelity for values that VARIANT
        # round-trip silently changes: float/double integer-valued collapse,
        # timestamps arriving as strings, dates arriving as strings, and any
        # of these nested inside array/map/struct compound types.
        apply_schema_coercion = (
            self._coerce_via_schema_json
            and defaulted_input_types_to_variant
            and not struct_positions
        )
        if apply_schema_coercion:
            self._input_types = list(self._input_types) + [StringType()]
            updated_callable_func = create_schema_json_coercion_wrapper(
                updated_callable_func
            )

        # Descriptor of TimestampType leaves in the return type (scalar or
        # nested in Array/Map/Struct). Drives return-value normalisation and
        # requires pytz in the UDF runtime for the session-timezone conversion.
        ts_return_desc = build_timestamp_return_descriptor(self._original_return_type)
        if ts_return_desc is not None and "pytz" not in packages:
            packages.append("pytz")

        if not needs_struct_conversion:
            # Apply null-safe wrapper first, then telemetry wrapper (if enabled)
            wrapped_func = create_null_safe_wrapper(updated_callable_func)
            # Normalise TIMESTAMP values in the return (LTZ -> session tz,
            # NTZ -> UTC), including timestamps nested in Array/Map/Struct.
            if ts_return_desc is not None:
                wrapped_func = create_timestamp_return_wrapper(
                    wrapped_func, ts_return_desc
                )
            if ENABLE_UDF_TELEMETRY:
                wrapped_func = create_telemetry_wrapper(
                    wrapped_func, self._function_name
                )
            return snowpark_fn.udf(
                wrapped_func,
                return_type=self._return_type,
                input_types=self._input_types,
                name=self._udf_name,
                replace=self._replace,
                packages=packages,
                imports=imports,
                immutable=self._is_deterministic,
                artifact_repository=self._artifact_repository,
                resource_constraint=self._resource_constraint,
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
                # Inline UDF with struct inputs: decompose to Row proxies,
                # call the original callable, then convert the result back.
                processed_args = []
                for i, arg in enumerate(args):
                    if i in struct_positions:
                        processed_args.append(convert_to_row(arg))
                    else:
                        processed_args.append(arg)
                result = callable_func(*tuple(processed_args))
                result = convert_from_row(result)
            else:
                # Registered UDF (all-VARIANT inputs, no struct decomposition):
                # use updated_callable_func so that the schema-json coercion
                # wrapper (if applied) correctly restores timestamps / dates
                # in the input before the user function sees them.
                result = updated_callable_func(*args)

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
            # Normalise TIMESTAMP values nested in the returned struct
            # (LTZ -> session tz, NTZ -> UTC).
            if ts_return_desc is not None:
                udf_function = create_timestamp_return_wrapper(
                    udf_function, ts_return_desc
                )

        # Apply telemetry wrapper (if enabled)
        if ENABLE_UDF_TELEMETRY:
            udf_function = create_telemetry_wrapper(udf_function, self._function_name)

        return snowpark_fn.udf(
            udf_function,
            return_type=self._return_type,
            input_types=self._input_types,
            name=self._udf_name,
            replace=self._replace,
            packages=packages,
            imports=imports,
            immutable=self._is_deterministic,
            artifact_repository=self._artifact_repository,
            resource_constraint=self._resource_constraint,
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
