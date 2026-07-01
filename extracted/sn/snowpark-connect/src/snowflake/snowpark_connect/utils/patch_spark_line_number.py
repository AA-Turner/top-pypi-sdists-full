#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Utility for patching PySpark Connect client to inject stack trace debugging information
into gRPC requests for better error reporting and debugging.

Compatible with PySpark 3.5.3 - uses StringValue and sys._getframe for clean stack traces.
"""

import json
import os
import sys
from collections import namedtuple
from typing import Callable, List, Optional

import pyspark
from google.protobuf.any_pb2 import Any
from google.protobuf.wrappers_pb2 import StringValue
from pyspark.sql.connect.client import SparkConnectClient

CallSite = namedtuple("CallSite", "function file linenum")
PYSPARK_PATH = os.path.dirname(pyspark.__file__)
CURRENT_FILE = __file__


def retrieve_stack_frames() -> Optional[List[CallSite]]:
    """
    Return a list of CallSites representing the relevant user code stack frames.

    Walks frames via ``sys._getframe()`` / ``frame.f_back`` rather than
    ``inspect.stack()`` to avoid the ``linecache``-driven ``os.stat()`` storm
    (this runs on every gRPC request from the client).

    Returns:
        List of CallSite objects representing user code frames, or None if no frames found.
    """

    # Skip the first few frames (this function, the wrapper, etc.) and look for user code
    # Start from frame 3 if available, otherwise start from the beginning
    try:
        frame = sys._getframe(1)
    except ValueError:
        return None

    for _ in range(2):
        if frame is None:
            return None
        frame = frame.f_back

    user_frames: List[CallSite] = []
    try:
        # Limit to reasonable number of frames
        while frame is not None and len(user_frames) < 5:
            filename = frame.f_code.co_filename

            if not (
                filename.startswith(PYSPARK_PATH)
                or filename == CURRENT_FILE
                or "site-packages" in filename
            ):
                user_frames.append(
                    CallSite(
                        function=frame.f_code.co_name,
                        file=filename,
                        linenum=frame.f_lineno,
                    )
                )

            frame = frame.f_back
    finally:
        # Break potential reference cycles from holding onto frame objects.
        del frame

    return user_frames if user_frames else None


def exec_with_debug_info(orig_fn: Callable) -> Callable:
    """
    A closure to inject debug information into gRPC requests made to the server.

    Args:
        orig_fn: The original PySpark Connect function to wrap.

    Returns:
        The modified PySpark Connect function with debug information injection.
    """

    def patched_fn(*args, **kwargs):
        """
        Retrieve the original request object created by PySpark and add debug information.

        Args:
            *args: Arguments to be used with the original function.
            **kwargs: Keyword arguments to be used with the original function.

        Returns:
            The request with debug information attached.
        """
        req = orig_fn(*args, **kwargs)
        stack_frames = retrieve_stack_frames()

        if stack_frames is not None:
            # Add stack trace information as a JSON string for Spark 3.5.3 compatibility
            stack_trace_data = []
            for call_site in stack_frames:
                stack_trace_data.append(
                    {
                        "method_name": call_site.function,
                        "file_name": call_site.file,
                        "line_number": call_site.linenum,
                    }
                )

            # Create a StringValue containing JSON-encoded stack trace
            stack_trace_json = json.dumps(stack_trace_data)
            string_value = StringValue(value=stack_trace_json)

            # Pack the debug information into an Any object and append to request
            any_obj = Any()
            any_obj.Pack(string_value)
            req.user_context.extensions.append(any_obj)
        else:
            # No debug information available, create an empty stack trace
            empty_stack_trace = json.dumps([])
            string_value = StringValue(value=empty_stack_trace)

            # Pack the empty debug information into an Any object
            any_obj = Any()
            any_obj.Pack(string_value)
            req.user_context.extensions.append(any_obj)

        return req

    return patched_fn


def extract_stack_trace_from_extensions(extensions) -> List[dict]:
    """
    Extract stack trace information from user_context.extensions on the server side.

    Args:
        extensions: The extensions field from request.user_context.extensions

    Returns:
        List of dictionaries containing stack trace information, or empty list if none found.
        Each dictionary contains: method_name, file_name, line_number
    """
    for extension in extensions:
        if extension.Is(StringValue.DESCRIPTOR):
            string_value = StringValue()
            extension.Unpack(string_value)
            try:
                stack_trace_data = json.loads(string_value.value)
                if isinstance(stack_trace_data, list):
                    return stack_trace_data
            except (json.JSONDecodeError, ValueError):
                continue
    return []


def patch_pyspark_connect() -> None:
    """
    Patch the PySpark Connect client functions to include debug information in gRPC requests.

    This monkey-patches key SparkConnectClient methods to automatically inject
    stack trace information into all requests sent to the Spark server.

    Compatible with PySpark 3.5.3 - uses JSON-encoded StringValue for stack trace data.
    """
    if getattr(SparkConnectClient, "_scos_stack_trace_patched", False):
        return

    # Patch core request methods to include debug information
    SparkConnectClient._execute_plan_request_with_metadata = exec_with_debug_info(
        SparkConnectClient._execute_plan_request_with_metadata
    )
    SparkConnectClient._analyze_plan_request_with_metadata = exec_with_debug_info(
        SparkConnectClient._analyze_plan_request_with_metadata
    )
    SparkConnectClient._config_request_with_metadata = exec_with_debug_info(
        SparkConnectClient._config_request_with_metadata
    )
    # Patch interrupt request as well (usage uncertain, but included for completeness)
    SparkConnectClient._interrupt_request = exec_with_debug_info(
        SparkConnectClient._interrupt_request
    )
    SparkConnectClient._scos_stack_trace_patched = True


def patch_proto_to_string() -> None:
    """
    Monkeypatch _proto_to_string as a short-term fix for RecursionError on deeply nested plans.

    text_format.MessageToString hits Python's recursion limit on deep protobuf
    plans, and the f-string in logger.info() evaluates eagerly even when logging
    is disabled. This patch prevents the crash by returning a placeholder string.
    """
    _original_proto_to_string = SparkConnectClient._proto_to_string

    def _safe_proto_to_string(self, p):
        try:
            return _original_proto_to_string(self, p)
        except RecursionError:
            return "<plan too deep to serialize>"

    SparkConnectClient._proto_to_string = _safe_proto_to_string
