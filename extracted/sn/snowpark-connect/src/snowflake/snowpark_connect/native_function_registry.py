#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Resolution of a native-function alias declared in the session configuration.

Turns a ``snowpark.connect.nativeFunction.<name>`` entry (see ``native_function_target``)
into the :class:`NativeFunctionUdf` handle that rewrites calls to ``<name>`` into a direct
call to the Snowflake function it names.

Resolution is **lazy**, driven by a lookup miss in ``UdfMonitor``. That keeps the whole
mechanism out of the Config RPC -- no Snowflake round trip on ``conf.set``, no dependence on
request context being available while a config is applied, and no ordering constraint
between declaring an alias and creating the function it points at.
"""

from snowflake.snowpark.types import DataType
from snowflake.snowpark_connect.config import (
    is_native_function_calls_enabled,
    sessions_config,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.native_function_target import (
    conf_key_for,
    parse_conf_value,
)
from snowflake.snowpark_connect.type_mapping import (
    map_single_type_string_to_snowpark_type,
)
from snowflake.snowpark_connect.utils.context import get_spark_session_id
from snowflake.snowpark_connect.utils.jvm_udf_utils import UdfKind
from snowflake.snowpark_connect.utils.telemetry import telemetry
from snowflake.snowpark_connect.utils.udf_helper import NativeFunctionUdf


def current_declaration(name: str) -> str | None:
    """The config value currently declaring ``name``, or ``None`` if it is not declared.

    ``name`` must be the lower-cased Spark-side function name, which is how function lookup
    presents it. That is what makes this a single dictionary lookup on a synthesised key:
    the session store normalises the name half of the key on write (see
    ``normalize_native_function_key``), so the case reconciliation is already done and there
    is nothing to scan. Passing a mixed-case name here simply will not match.

    Returns ``None`` when the mechanism is switched off, so a kill switch withdraws every
    declaration without the user having to unset any of them.
    """
    if not is_native_function_calls_enabled():
        return None
    return sessions_config[get_spark_session_id()].get(conf_key_for(name)) or None


def resolve_native_function(name: str) -> NativeFunctionUdf | None:
    """The handle for native-function alias ``name``, or ``None`` if there is no such alias."""
    value = current_declaration(name)
    if value is None:
        return None

    target, return_type = _parse(name, value)
    telemetry.report_native_function_target(target)
    return NativeFunctionUdf(
        name=name,
        # There is no DDL, so only the original type matters -- it is what the native result
        # is cast to. Using it for both avoids implying a VARIANT-returning function exists.
        return_type=return_type,
        original_return_type=return_type,
        kind=UdfKind.NATIVE_FUNCTION,
        cast_to_original_return_type=True,
        target=target,
        declaration=value,
    )


def _parse(name: str, value: str) -> tuple[str, DataType]:
    """Split and type-check a declaration, reporting failures against the conf key."""
    try:
        target, type_string = parse_conf_value(value)
    except ValueError as e:
        raise _invalid(name, str(e)) from e

    if type_string is None:
        # Accepted by the grammar but not yet implemented, so that adding inference later
        # gives meaning to a value that is already syntactically valid rather than changing
        # what a previously-rejected value does.
        raise _invalid(
            name,
            f"no return type given. Declare one as '{target}:<type>' -- for example "
            f"'{target}:double'. Inferring it from Snowflake is not implemented yet.",
        )

    try:
        return target, map_single_type_string_to_snowpark_type(type_string)
    except Exception as e:
        raise _invalid(name, f"{type_string!r} is not a valid Spark type: {e}") from e


def _invalid(name: str, detail: str) -> Exception:
    exception = ValueError(
        f"Invalid native function declaration for '{conf_key_for(name)}': {detail}"
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
    return exception
