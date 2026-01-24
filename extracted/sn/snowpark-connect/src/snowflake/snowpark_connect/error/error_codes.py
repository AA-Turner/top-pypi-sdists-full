#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Error code constants for Snowpark Connect.

This module defines custom error codes that can be attached to exceptions
and included in gRPC error responses.
"""


class ErrorCodes:
    """Constants for Snowpark Connect custom error codes."""

    # 1000-1999: Startup related errors
    MISSING_DATABASE = 1001
    MISSING_SCHEMA = 1002
    RESOURCE_INITIALIZATION_FAILED = 1003
    TCP_PORT_ALREADY_IN_USE = 1004
    INVALID_SPARK_CONNECT_URL = 1005
    INVALID_STARTUP_INPUT = 1006
    INVALID_STARTUP_OPERATION = 1007
    STARTUP_CONNECTION_FAILED = 1008

    # 2000-2999: Configuration related errors
    INVALID_CONFIG_VALUE = 2001
    CONFIG_CHANGE_NOT_ALLOWED = 2002
    CONFIG_NOT_ENABLED = 2003

    # 3000-3999: User code errors
    INVALID_SQL_SYNTAX = 3001
    TYPE_MISMATCH = 3002
    INVALID_CAST = 3003
    INVALID_FUNCTION_ARGUMENT = 3004
    ARRAY_INDEX_OUT_OF_BOUNDS = 3005
    DIVISION_BY_ZERO = 3006
    INVALID_INPUT = 3007
    INVALID_OPERATION = 3008
    INSUFFICIENT_INPUT = 3009

    # 4000-4999: What we don't support
    UNSUPPORTED_OPERATION = 4001
    UNSUPPORTED_TYPE = 4002

    # 5000-5999: Internal errors
    INTERNAL_ERROR = 5001
    TABLE_NOT_FOUND = 5002
    COLUMN_NOT_FOUND = 5003
    AMBIGUOUS_COLUMN_NAME = 5004
