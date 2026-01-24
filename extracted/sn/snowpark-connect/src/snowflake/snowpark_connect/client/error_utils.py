#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Lightweight error utilities for the Snowpark Connect client.

This is a minimal version of snowflake.snowpark_connect.error.error_utils
that avoids heavy dependencies like jpype that are only needed server-side.
"""

import threading

# Thread-local storage for custom error codes when we can't attach them directly to exceptions
_thread_local = threading.local()


def attach_custom_error_code(exception: Exception, custom_error_code: int) -> Exception:
    """
    Attach a custom error code to any exception instance.
    This allows us to add custom error codes to existing PySpark exceptions.
    """
    if not hasattr(exception, "custom_error_code"):
        try:
            exception.custom_error_code = custom_error_code
        except (AttributeError, TypeError):
            # Some exception types don't allow setting custom attributes
            # Store the error code in thread-local storage for later retrieval
            _thread_local.pending_error_code = custom_error_code
    return exception
