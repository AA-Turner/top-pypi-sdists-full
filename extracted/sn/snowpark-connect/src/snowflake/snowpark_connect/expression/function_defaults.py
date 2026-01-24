#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
from dataclasses import dataclass
from typing import Any

import pyspark.sql.connect.proto.expressions_pb2 as expressions_pb2
import pyspark.sql.connect.proto.types_pb2 as types_pb2

from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code


@dataclass(frozen=True)
class DefaultParameter:
    """Represents a single default parameter for a function."""

    name: str
    value: Any


@dataclass(frozen=True)
class FunctionDefaults:
    """Represents default parameter configuration for a function."""

    total_args: int
    defaults: list[DefaultParameter]


# FUNCTION_DEFAULTS dictionary to hold operation name with default values.
# This is required as non pyspark clients such as scala or sql won't send all the parameters.
# We use this dict to inject the missing parameters before processing the unresolved function.
FUNCTION_DEFAULTS: dict[str, FunctionDefaults] = {
    "aes_decrypt": FunctionDefaults(
        total_args=5,
        defaults=[
            DefaultParameter("mode", "GCM"),  # Spark SQL default: GCM
            DefaultParameter("padding", "NONE"),  # Spark SQL default: NONE for GCM mode
            DefaultParameter("aad", ""),  # Spark SQL default: empty string
        ],
    ),
    "aes_encrypt": FunctionDefaults(
        total_args=6,
        defaults=[
            DefaultParameter("mode", "GCM"),  # Spark SQL default: GCM
            DefaultParameter("padding", "NONE"),  # Spark SQL default: NONE for GCM mode
            DefaultParameter(
                "iv", ""
            ),  # Spark SQL default: empty string (random generated if not provided)
            DefaultParameter("aad", ""),  # Spark SQL default: empty string
        ],
    ),
    "approx_percentile": FunctionDefaults(
        total_args=3,
        defaults=[DefaultParameter("accuracy", 10000)],
    ),
    "bround": FunctionDefaults(
        total_args=2,
        defaults=[DefaultParameter("scale", 0)],
    ),
    "first": FunctionDefaults(
        total_args=2,
        defaults=[DefaultParameter("ignorenulls", False)],
    ),
    "lag": FunctionDefaults(
        total_args=2,
        defaults=[
            DefaultParameter("offset", 1),
        ],
    ),
    "last": FunctionDefaults(
        total_args=2,
        defaults=[DefaultParameter("ignorenulls", False)],
    ),
    "lead": FunctionDefaults(
        total_args=3,
        defaults=[DefaultParameter("offset", 1), DefaultParameter("default", None)],
    ),
    "locate": FunctionDefaults(
        total_args=3,
        defaults=[DefaultParameter("pos", 1)],
    ),
    "months_between": FunctionDefaults(
        total_args=3,
        defaults=[DefaultParameter("roundOff", True)],
    ),
    "nth_value": FunctionDefaults(
        total_args=3,
        defaults=[DefaultParameter("ignoreNulls", False)],
    ),
    "overlay": FunctionDefaults(
        total_args=4,
        defaults=[DefaultParameter("len", -1)],
    ),
    "percentile": FunctionDefaults(
        total_args=3,
        defaults=[DefaultParameter("frequency", 1)],
    ),
    "percentile_approx": FunctionDefaults(
        total_args=3,
        defaults=[DefaultParameter("accuracy", 10000)],
    ),
    "round": FunctionDefaults(
        total_args=2,
        defaults=[DefaultParameter("scale", 0)],
    ),
    "sentences": FunctionDefaults(
        total_args=3,
        defaults=[
            DefaultParameter("language", ""),
            DefaultParameter("country", ""),
        ],
    ),
    "sort_array": FunctionDefaults(
        total_args=2,
        defaults=[DefaultParameter("asc", True)],
    ),
    "split": FunctionDefaults(
        total_args=3,
        defaults=[DefaultParameter("limit", -1)],
    ),
    "str_to_map": FunctionDefaults(
        total_args=3,
        defaults=[
            DefaultParameter(
                "pairDelim", ","
            ),  # Spark SQL default: comma for splitting pairs
            DefaultParameter(
                "keyValueDelim", ":"
            ),  # Spark SQL default: colon for splitting key/value
        ],
    ),
    "try_aes_decrypt": FunctionDefaults(
        total_args=5,
        defaults=[
            DefaultParameter("mode", "GCM"),  # Spark SQL default: GCM
            DefaultParameter("padding", "NONE"),  # Spark SQL default: NONE for GCM mode
            DefaultParameter("aad", ""),  # Spark SQL default: empty string
        ],
    ),
}


def _create_literal_expression(value: Any) -> expressions_pb2.Expression:
    """Create a literal expression for the given value."""
    expr = expressions_pb2.Expression()
    if isinstance(value, bool):
        expr.literal.boolean = value
    elif isinstance(value, int):
        expr.literal.integer = value
    elif isinstance(value, str):
        expr.literal.string = value
    elif isinstance(value, float):
        expr.literal.double = value
    elif value is None:
        null_type = types_pb2.DataType()
        null_type.null.SetInParent()
        expr.literal.null.CopyFrom(null_type)
    else:
        exception = ValueError(f"Unsupported literal type: {value}")
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_TYPE)
        raise exception

    return expr


def inject_function_defaults(
    unresolved_function: expressions_pb2.Expression.UnresolvedFunction,
) -> bool:
    """
    Inject missing default parameters into an UnresolvedFunction protobuf.

    Args:
        unresolved_function: The protobuf UnresolvedFunction to modify

    Returns:
        bool: True if any defaults were injected, False otherwise
    """
    function_name = unresolved_function.function_name.lower()

    if function_name not in FUNCTION_DEFAULTS:
        return False

    func_config = FUNCTION_DEFAULTS[function_name]
    current_arg_count = len(unresolved_function.arguments)
    total_args = func_config.total_args
    defaults = func_config.defaults

    if not defaults or current_arg_count >= total_args:
        return False

    # Calculate how many defaults to append
    missing_arg_count = total_args - current_arg_count

    # Check if any required params are missing.
    if missing_arg_count > len(defaults):
        exception = ValueError(
            f"Function '{function_name}' is missing required arguments. "
            f"Expected {total_args} args, got {current_arg_count}, "
            f"but only {len(defaults)} defaults are defined."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception

    defaults_to_append = defaults[-missing_arg_count:]
    injected = False

    # Simply append the needed default values
    for default_param in defaults_to_append:
        default_expr = _create_literal_expression(default_param.value)
        unresolved_function.arguments.append(default_expr)
        injected = True

    return injected
