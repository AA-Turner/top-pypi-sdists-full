#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import functools
import threading
import typing
from collections.abc import Callable
from types import ModuleType
from typing import List, Optional, Tuple, Union

from snowflake.snowpark import Session
from snowflake.snowpark.column import Column
from snowflake.snowpark.functions import call_udf, udaf, udf, udtf
from snowflake.snowpark.types import DataType, StructType
from snowflake.snowpark_connect import tcm
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.error.exceptions import MissingDatabase, MissingSchema
from snowflake.snowpark_connect.utils.telemetry import telemetry
from snowflake.snowpark_connect.utils.upload_java_jar import (
    JAVA_UDFS_JAR_NAME,
    upload_java_udf_jar,
)

_lock = threading.RLock()

_BUILTIN_UDF_PREFIX = "__SC_BUILTIN_"


def init_builtin_udf_cache(session: Session) -> None:
    with _lock:
        session._cached_udfs = {}
        session._cached_udafs = {}
        session._cached_udtfs = {}
        session._cached_java_udfs = {}
        session._cached_sql_udfs = {}
        session._cached_sprocs = {}


def _hash_types(types: list) -> str:
    return f"{abs(hash(tuple(types))):016X}"


def _packages(
    packages: Optional[List[Union[str, ModuleType]]] = None
) -> Optional[List[Union[str, ModuleType]]]:
    if not tcm.TCM_MODE:
        return packages

    if packages is None or "snowflake-snowpark-python" not in packages:
        if packages is None:
            packages = ["snowflake-snowpark-python"]
        else:
            packages.append("snowflake-snowpark-python")
    return packages


def _udxf_name(
    fn: Callable,
    input_types: Optional[List[DataType]] = None,
    output_schema: Optional[DataType] = None,
) -> str:
    """
    Generates a unique name for a UDXF based on the function name, input types and output schema.
    Names are prefixed to be easily searchable in Snowhouse.
    """
    input_types_hash = _hash_types(input_types) if input_types is not None else ""
    output_schema_hash = (
        _hash_types([output_schema]) if output_schema is not None else ""
    )

    return f"{_BUILTIN_UDF_PREFIX}{input_types_hash}_{output_schema_hash}_{fn.__name__.upper()}"


def _build_fully_qualified_name(session: Session, name: str) -> list[str]:
    """
    Build a fully qualified name list ``[database, schema, name]`` for a
    UDF/UDTF/UDAF/stored procedure, using the session's current database and schema.

    Returning a list (rather than a pre-joined string) lets Snowpark quote each
    identifier part individually when calling udf()/udtf()/udaf().  For callers
    that need a plain dot-joined string (e.g. ``call_udf`` or a ``CALL`` statement)
    use ``".".join(_build_fully_qualified_name(session, name))``.

    Raises ``ValueError`` if the session has no current database or schema, or if
    ``name`` is empty, because Snowflake cannot resolve the object without a full
    qualifier context.
    """
    db = session.get_current_database()
    schema = session.get_current_schema()

    if not name:
        exception = ValueError(
            "Cannot register a built-in UDF/UDTF/UDAF/stored procedure: "
            "the object name must not be empty."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    if db is None:
        raise MissingDatabase()

    if schema is None:
        raise MissingSchema()

    return [db, schema, name]


def cached_udaf(
    class_type: typing.Type,
    *,
    input_types: Optional[List[DataType]] = None,
    return_type: Optional[DataType] = None,
    imports: Optional[List[Union[str, Tuple[str, str]]]] = None,
    packages: Optional[List[Union[str, ModuleType]]] = None,
):
    """
    A drop-in replacement for Snowpark's `udaf` that caches the UDAF in the active session.

    The UDAF is cached based on its name and input types. Make sure any new cached functions are unique.
    """
    packages = _packages(packages)

    def _cached_udaf(udaf_type: typing.Type):
        telemetry.report_udf_usage(udaf_type.__name__)
        with _lock:
            cache = Session.get_active_session()._cached_udafs
            name = _udxf_name(udaf_type, input_types, return_type)

            if name in cache:
                return cache[name]

        # Register the function outside the lock to avoid contention
        wrapped_func = udaf(
            udaf_type,
            name=_build_fully_qualified_name(Session.get_active_session(), name),
            return_type=return_type,
            input_types=input_types,
            imports=imports,
            packages=packages,
            is_permanent=False,
            replace=True,
        )

        with _lock:
            cache[name] = wrapped_func

        return wrapped_func

    if class_type is None:
        raise ValueError(
            "[snowpark_connect::internal_error] Type must be provided for cached_udaf. UDAF contains multiple functions hence it has to be represented by a type. Functions are not supported."
        )
    else:
        # return udaf
        return _cached_udaf(class_type)


def cached_udf(
    fn: Callable = None,
    *,
    input_types: Optional[List[DataType]] = None,
    return_type: Optional[DataType] = None,
    imports: Optional[List[Union[str, Tuple[str, str]]]] = None,
    packages: Optional[List[Union[str, ModuleType]]] = None,
):
    """
    A drop-in replacement for Snowpark's `udf` that caches the UDF in the active session.

    The UDF is cached based on its name and input types. Make sure any new cached functions are unique.
    """
    packages = _packages(packages)

    def _cached_udf(func: Callable):
        telemetry.report_udf_usage(func.__name__)
        with _lock:
            cache = Session.get_active_session()._cached_udfs
            name = _udxf_name(func, input_types, return_type)
            # Check if the udf is already cached
            if name in cache:
                return cache[name]

        # Create a wrapper function that handles sqlNullWrapper objects
        from snowflake.snowpark_connect.utils.udf_utils import create_null_safe_wrapper

        _null_safe_wrapper = create_null_safe_wrapper(func)

        # Register the function outside the lock to avoid contention when registering multiple functions.
        # It's possible that multiple threads will try to register the same function,
        # but this will not cause any issues.
        wrapped_func = udf(
            _null_safe_wrapper,
            name=_build_fully_qualified_name(Session.get_active_session(), name),
            return_type=return_type,
            input_types=input_types,
            imports=imports,
            packages=packages,
            is_permanent=False,
            replace=True,
        )

        with _lock:
            # Cache the udf
            cache[name] = wrapped_func

        return wrapped_func

    if fn is None:
        # return decorator
        return _cached_udf
    else:
        # return udf
        return _cached_udf(fn)


def cached_udtf(
    fn: Callable = None,
    *,
    output_schema: Union[StructType, List[str]],
    input_types: Optional[List[DataType]] = None,
    imports: Optional[List[Union[str, Tuple[str, str]]]] = None,
    packages: Optional[List[Union[str, ModuleType]]] = None,
):
    """
    A drop-in replacement for Snowpark's `udtf` that caches the UDTF in the active session.

    The UDTF is cached based on its name and input types. Make sure any new cached functions are unique.
    """
    packages = _packages(packages)

    def _cached_udtf(func: Callable):
        telemetry.report_udf_usage(func.__name__)
        with _lock:
            cache = Session.get_active_session()._cached_udtfs
            name = _udxf_name(func, input_types, output_schema)

            if name in cache:
                return cache[name]

        # Register the function outside the lock to avoid contention
        wrapped_func = udtf(
            func,
            name=_build_fully_qualified_name(Session.get_active_session(), name),
            output_schema=output_schema,
            input_types=input_types,
            imports=imports,
            packages=packages,
            is_permanent=False,
            replace=True,
        )

        with _lock:
            cache[name] = wrapped_func

        return wrapped_func

    if fn is None:
        # return decorator
        return _cached_udtf
    else:
        # return udtf
        return _cached_udtf(fn)


def _create_temporary_java_udf(
    session: Session,
    function_name: str,
    input_types: list[str],
    return_type: str,
    imports: list[str],
    java_handler: str,
    packages: list[str] | None = None,
) -> None:
    args_str = ",".join(f"arg{idx} {type_}" for idx, type_ in enumerate(input_types))
    imports_str = ",".join(f"'{import_}'" for import_ in imports)
    packages_str = ",".join(f"'{pkg}'" for pkg in packages) if packages else ""

    session.sql(
        f"""CREATE OR REPLACE TEMPORARY FUNCTION {function_name}({args_str})
                          RETURNS {return_type}
                          LANGUAGE JAVA
                          IMPORTS = ({imports_str})
                          HANDLER = '{java_handler}'
                          PACKAGES = ({packages_str})
                          RUNTIME_VERSION = 17
      """
    ).collect()


def _create_temporary_sql_udf(
    session: Session,
    function_name: str,
    input_types: list[str],
    return_type: str,
    body: str,
) -> None:
    args_str = ",".join(f"arg{idx} {type_}" for idx, type_ in enumerate(input_types))
    session.sql(
        f"""
        CREATE OR REPLACE TEMPORARY FUNCTION {function_name}({args_str})
            RETURNS {return_type}
            AS
            $$
            {body}
            $$
        """
    ).collect()


def register_cached_sql_udf(
    input_types: list[str],
    return_type: str,
    body: str,
) -> Callable[..., Column]:
    """
    Register a cached SQL UDF
    - `input_types` and `return_type` should be valid sql type names, e.g. STRING, VARCHAR, FLOAT etc.
    - `body` should contain SQL code of the function body. Arguments are named arg0, arg1... etc.
    """

    input_types_hash = _hash_types(input_types)
    fun_name = _hash_types([body])

    telemetry.report_udf_usage(fun_name)

    function_name = f"{_BUILTIN_UDF_PREFIX}{fun_name.upper()}{input_types_hash}"

    with _lock:
        session = Session.get_active_session()
        cache = session._cached_sql_udfs

        udf_is_cached = function_name in cache

    if not udf_is_cached:
        _create_temporary_sql_udf(
            session,
            function_name,
            input_types,
            return_type,
            body,
        )

        with _lock:
            function_identifier = ".".join(
                _build_fully_qualified_name(Session.get_active_session(), function_name)
            )
            cache[function_name] = function_identifier
    else:
        function_identifier = cache[function_name]

    return functools.partial(
        call_udf,
        function_identifier,
    )


def register_cached_java_udf(
    java_handler: str,
    input_types: list[str],
    return_type: str,
    packages: list[str] | None = None,
) -> Callable[..., Column]:
    """
    Register a cached Java UDF. To use it, you need to:
    - Implement a handler function in the java_udfs subproject.
    - Build a jar using `mvn clean package` command and make sure the generated jar isn't too big (couple of KBs).
    - Copy the jar to `snowflake.snowpark_connect.resources`

    input_types and return_type should be valid sql type names, e.g. STRING, VARCHAR, FLOAT etc.
    """

    telemetry.report_udf_usage(java_handler)

    input_types_hash = _hash_types(input_types)
    java_fun_name = java_handler.split(".")[-1]

    function_name = f"{_BUILTIN_UDF_PREFIX}{java_fun_name.upper()}{input_types_hash}"

    with (_lock):
        session = Session.get_active_session()
        cache = session._cached_java_udfs
        stage = session.get_session_stage()

        if len(cache) == 0:
            # This is the first Java UDF being registered, so we need to upload the JAR with UDF definitions first
            upload_java_udf_jar(session)

        udf_is_cached = function_name in cache

    if not udf_is_cached:
        _create_temporary_java_udf(
            session,
            function_name,
            input_types,
            return_type,
            [f"{stage}/snowflake/snowpark_connect/resources/{JAVA_UDFS_JAR_NAME}"],
            java_handler,
            packages,
        )

        with _lock:
            function_identifier = ".".join(
                _build_fully_qualified_name(Session.get_active_session(), function_name)
            )
            cache[function_name] = function_identifier
    else:
        function_identifier = cache[function_name]

    return functools.partial(
        call_udf,
        function_identifier,
    )


def register_cached_sproc(
    sproc_body: str,
    handler_name: str,
    input_arg_types: list[str],
    return_type: str = "STRING",
    runtime_version: str = "3.11",
    packages: list[str] | None = None,
) -> str:
    """
    Register a cached stored procedure that persists across schema/database changes.

    Args:
        sproc_body: The Python code for the stored procedure
        handler_name: Name of the handler function in the sproc_body
        input_arg_types: List of SQL types for input arguments (e.g. ['STRING', 'STRING'])
        return_type: SQL return type (default: 'STRING')
        runtime_version: Python runtime version (default: '3.11')
        packages: List of Python packages to include

    Returns:
        Fully qualified stored procedure name for calling
    """
    if packages is None:
        packages = ["snowflake-snowpark-python"]

    # Create a unique hash based on the procedure content and signature
    content_hash = _hash_types(
        [sproc_body, handler_name, return_type, runtime_version]
        + input_arg_types
        + packages
    )

    # Generate unique procedure name with hash
    sproc_name = f"{_BUILTIN_UDF_PREFIX}SPROC_{content_hash}"

    with _lock:
        session = Session.get_active_session()
        cache = session._cached_sprocs

        if sproc_name in cache:
            return cache[sproc_name]

    # Build the FQN outside the lock (and after the cache-hit early return) so
    # that _build_fully_qualified_name's error check only runs on first registration.
    fully_qualified_name = ".".join(_build_fully_qualified_name(session, sproc_name))

    args_str = ",".join(
        f"arg{idx} {type_}" for idx, type_ in enumerate(input_arg_types)
    )
    packages_str = ",".join(f"'{pkg}'" for pkg in packages)

    session.sql(
        f"""
        CREATE OR REPLACE TEMPORARY PROCEDURE {sproc_name}({args_str})
        RETURNS {return_type}
        LANGUAGE PYTHON
        RUNTIME_VERSION = '{runtime_version}'
        PACKAGES = ({packages_str})
        HANDLER = '{handler_name}'
        AS $$
{sproc_body}
$$
    """
    ).collect()

    with _lock:
        cache[sproc_name] = fully_qualified_name

    return fully_qualified_name
