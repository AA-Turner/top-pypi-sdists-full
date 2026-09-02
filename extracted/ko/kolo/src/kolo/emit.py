"""
Emit a trace into a browsable directory structure.

This module creates a human-readable directory tree from a kolo trace,
making it easy to browse and search trace data.
"""

from __future__ import annotations

import hashlib
import logging
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

# Header for emitted .py files - tells tools to ignore these auto-generated files
PY_FILE_HEADER = """\
# type: ignore
# ruff: noqa
# fmt: off
# Kolo trace file (auto-generated)
"""

if TYPE_CHECKING:
    from .navigator import TraceNavigator
    from .node import ProcessedNode
    from .trace import Trace


def sanitize_filename(name: str, max_length: int = 80) -> str:
    """
    Sanitize a string for use as a filename.

    - Replace unsafe characters with underscores
    - Truncate to max_length
    - Handle edge cases
    """
    # Replace path separators and other unsafe chars
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)
    # Replace multiple consecutive underscores/spaces
    name = re.sub(r"[_\s]+", "_", name)
    # Remove leading/trailing underscores and dots
    name = name.strip("_. ")
    # Truncate if too long
    if len(name) > max_length:
        name = name[:max_length].rstrip("_")
    return name


# Maximum path length to avoid ENAMETOOLONG errors
# macOS has a 1024 byte limit, but we need to be conservative due to
# filesystem overhead and the initial path length
MAX_PATH_LENGTH = 600


def _to_base36(num: int, width: int = 4) -> str:
    """Convert a number to base36 string with fixed width."""
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = []
    for _ in range(width):
        result.append(chars[num % 36])
        num //= 36
    return "".join(reversed(result))


def get_sort_prefix(trace: Trace) -> str:
    """
    Generate a short prefix that sorts newest traces first.

    Uses inverted epoch milliseconds encoded in base36 so that newer traces
    have smaller prefix values and appear at the top when sorted alphabetically.

    Format: 5 base36 characters (~16.8 hour rolling window with ms precision).
    """
    timestamp = trace.unprocessed_data.get("timestamp")
    if timestamp is None:
        timestamp = datetime.now(timezone.utc).timestamp()

    # Convert to milliseconds
    epoch_ms = int(timestamp * 1000)

    # 36^5 = 60,466,176 (~16.8 hours of milliseconds)
    # Invert so newer traces get smaller values (sort first)
    max_val = 36**5 - 1
    inverted = max_val - (epoch_ms % (max_val + 1))

    return _to_base36(inverted, width=5)


def get_human_readable_date(trace: Trace) -> str:
    """
    Generate a human-readable date string for the trace in local timezone.

    Format: MonDD_HHMM (e.g., Jan13_1430)
    """
    timestamp = trace.unprocessed_data.get("timestamp")
    if timestamp is None:
        timestamp = datetime.now().timestamp()

    # Get the system's local timezone explicitly
    # (datetime.fromtimestamp alone can be affected by TZ env var)
    local_tz = datetime.now().astimezone().tzinfo
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(local_tz)
    # Format: Jan13_1430
    return dt.strftime("%b%d_%H%M")


def get_trace_folder_name(trace: Trace, root_nodes: List[ProcessedNode]) -> str:
    """
    Generate a folder name for the trace based on its content.

    Format: {sort_prefix}_{date}_{status}_{method}_{path} (for HTTP requests)
    Example: 0a2k_Jan13_1430_200_POST_api_users

    The sort prefix (4 base36 chars) ensures newest traces appear first when sorted.
    The date provides human-readable context.
    The trace ID is stored separately in {trace_id}.txt inside the folder.
    """
    # Start with sort prefix and human-readable date
    prefix = get_sort_prefix(trace)
    date_str = get_human_readable_date(trace)
    parts = [prefix, date_str]

    # Try to extract HTTP request info
    if root_nodes and root_nodes[0].type == "nested_served_http_request":
        req = root_nodes[0].data.get("request", {})
        resp = root_nodes[0].data.get("response", {})

        status = resp.get("status_code")
        method = req.get("method")
        path = req.get("path_info", "")

        if status:
            parts.append(str(status))
        if method:
            parts.append(method)
        if path:
            # Clean up the path for use in folder name
            clean_path = path.strip("/").replace("/", "_")
            clean_path = sanitize_filename(clean_path, max_length=120)
            if clean_path:
                parts.append(clean_path)

    # Try to extract test info for test traces
    elif root_nodes and root_nodes[0].type == "frame_span":
        name = root_nodes[0].name
        # Check if it looks like a test method (e.g., "TestClass.test_method")
        if _looks_like_test_method(name):
            clean_name = sanitize_filename(name, max_length=120)
            parts.append(clean_name)
        elif name == "__main__.<module>":
            # Check children for actual test methods (skip conftest, fixtures, etc.)
            for child in root_nodes[0].children:
                # Tests can be nested_test type or frame_span type
                if child.type in (
                    "frame_span",
                    "nested_test",
                ) and _looks_like_test_method(child.name):
                    clean_name = sanitize_filename(child.name, max_length=120)
                    parts.append(clean_name)
                    break

    # Fallback to trace ID if no descriptive name could be generated
    # (parts[0:2] are sort prefix and date, so check if there's more than that)
    if len(parts) == 2:
        parts.append(trace.id)

    return "_".join(parts)


def _looks_like_test_method(name: str) -> bool:
    """
    Check if a name looks like an actual test method rather than test infrastructure.

    Returns True for things like:
    - TestClass.test_method
    - test_something
    - SomethingTestCase.test_action

    Returns False for:
    - conftest.pytest_sessionstart
    - pytest fixtures
    """
    # Skip common test infrastructure
    if name.startswith("conftest.") or name.startswith("pytest."):
        return False
    if "fixture" in name.lower():
        return False

    # Look for actual test patterns
    # Pattern 1: Contains "Test" and has a ".test_" method
    if "Test" in name and ".test_" in name:
        return True
    # Pattern 2: Starts with "test_"
    if name.startswith("test_") or ".test_" in name:
        return True
    # Pattern 3: TestCase class pattern
    if "TestCase." in name:
        return True

    return False


def get_node_name_for_path(node: ProcessedNode, max_name_length: int = 80) -> str:
    """
    Generate a filename/dirname for a node.

    Format: {index:04d}_{type_hint}_{name}

    Args:
        node: The node to generate a name for
        max_name_length: Maximum length for the resulting name (to avoid path too long errors)
    """
    idx = f"{node.index:04d}"

    # Calculate how much space we have for the variable part
    # Reserve space for index (4 chars), underscores (2)
    reserved = len(idx) + 3
    name_budget = max(20, max_name_length - reserved)

    if node.type == "frame_span":
        # Function call - use qualified name
        name = sanitize_filename(node.name, max_length=name_budget)
        return f"{idx}_{name}"

    elif node.type == "sql_query":
        # SQL query - extract table name if possible
        query = node.data.get("query", "")
        table_match = re.search(
            r'(?:FROM|INTO|UPDATE)\s+"?(\w+)"?', query, re.IGNORECASE
        )
        table = table_match.group(1) if table_match else "query"

        # Determine query type
        query_upper = query.strip().upper()
        if query_upper.startswith("SELECT"):
            query_type = "SELECT"
        elif query_upper.startswith("INSERT"):
            query_type = "INSERT"
        elif query_upper.startswith("UPDATE"):
            query_type = "UPDATE"
        elif query_upper.startswith("DELETE"):
            query_type = "DELETE"
        else:
            query_type = "sql"

        table = sanitize_filename(table, max_length=min(30, name_budget - 10))
        return f"{idx}_sql_{query_type}_{table}"

    elif node.type == "nested_background_job":
        # Celery task
        subtype = node.data.get("subtype", "job")
        name = sanitize_filename(
            node.data.get("name", "task"), max_length=name_budget - 10
        )
        return f"{idx}_{subtype}_{name}"

    elif node.type == "nested_served_http_request":
        # Incoming HTTP request
        request = node.data.get("request", {})
        method = request.get("method", "REQUEST")
        path = sanitize_filename(
            request.get("path_info", ""), max_length=name_budget - 10
        )
        if path:
            return f"{idx}_{method}_{path}"
        return f"{idx}_{method}"

    elif node.type == "outbound_http_request":
        # Outbound HTTP request
        # Data can be in nested "request" dict OR at the top level of node.data
        request = node.data.get("request", {})
        method = request.get("method") or node.data.get("method", "REQUEST")
        url = request.get("url") or node.data.get("url", "")
        # Extract host from URL
        host_match = re.search(r"https?://([^/]+)", url)
        if host_match:
            host = sanitize_filename(
                host_match.group(1), max_length=min(30, name_budget - 15)
            )
            return f"{idx}_http_{method}_{host}"
        return f"{idx}_http_{method}"

    elif node.type == "log_message":
        # Log message
        level = node.data.get("level", "LOG")
        msg = node.data.get("msg", "")
        msg_preview = sanitize_filename(
            str(msg)[:30], max_length=min(30, name_budget - 10)
        )
        return f"{idx}_log_{level}_{msg_preview}"

    elif node.type == "django_template":
        # Django template
        template_name = node.data.get("template") or "template"
        template = sanitize_filename(template_name, max_length=name_budget - 10)
        return f"{idx}_template_{template}"

    elif node.type == "nested_test":
        # Test
        test_name = node.data.get("test_name", "test")
        test_class = node.data.get("test_class", "")
        if test_class:
            name = f"{test_class}.{test_name}"
        else:
            name = test_name
        return f"{idx}_test_{sanitize_filename(name, max_length=name_budget - 10)}"

    elif node.type == "subtree_flushed":
        co_name = str(node.data.get("co_name") or "<unknown>")
        name = sanitize_filename(co_name, max_length=name_budget - 15)
        return f"{idx}_flushed_{name}"

    else:
        # Unknown type - use what we have
        return f"{idx}_{node.type}"


# =============================================================================
# File Content Generators
# =============================================================================


def format_value(value: Any) -> str:
    """
    Format a single value for display.

    Uses pprint for dicts/lists, handles JSON strings specially.
    No truncation - shows full values.
    """
    import json
    import pprint

    # Try to detect and pretty-print JSON strings
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, (dict, list)):
                return json.dumps(parsed, indent=2)
        except (json.JSONDecodeError, ValueError):
            pass
        return repr(value)

    # Use pprint for complex types
    if isinstance(value, (dict, list, set, frozenset, tuple)):
        return pprint.pformat(value, width=100, indent=2, sort_dicts=False)

    return repr(value)


def format_locals(locals_dict: Dict[str, Any], indent: str = "") -> str:
    """
    Format a locals dictionary for display.

    Uses pprint for readable nested structures. No truncation.
    """
    if not locals_dict:
        return f"{indent}(none)"

    lines = []
    for key, value in locals_dict.items():
        formatted = format_value(value)
        # Handle multi-line values with proper indentation
        if "\n" in formatted:
            lines.append(f"{indent}{key}:")
            for line in formatted.split("\n"):
                lines.append(f"{indent}  {line}")
        else:
            lines.append(f"{indent}{key}: {formatted}")
    return "\n".join(lines)


def format_locals_diff(
    call_locals: Dict[str, Any], return_locals: Dict[str, Any]
) -> str:
    """
    Format the difference between call and return locals.

    Shows:
    - Changed values: key: old_value -> new_value
    - New variables: + key: value
    - Deleted variables: - key
    - Summary of unchanged variables
    """
    lines = []
    unchanged_count = 0

    call_keys = set(call_locals.keys())
    return_keys = set(return_locals.keys())

    # Check for changes and unchanged
    for key in sorted(call_keys & return_keys):
        call_val = call_locals[key]
        return_val = return_locals[key]
        if call_val == return_val:
            unchanged_count += 1
        else:
            # Value changed
            old_formatted = format_value(call_val)
            new_formatted = format_value(return_val)
            if "\n" in old_formatted or "\n" in new_formatted:
                lines.append(f"~ {key}:")
                lines.append("  before:")
                for line in old_formatted.split("\n"):
                    lines.append(f"    {line}")
                lines.append("  after:")
                for line in new_formatted.split("\n"):
                    lines.append(f"    {line}")
            else:
                lines.append(f"~ {key}: {old_formatted} -> {new_formatted}")

    # New variables (in return but not in call)
    for key in sorted(return_keys - call_keys):
        formatted = format_value(return_locals[key])
        if "\n" in formatted:
            lines.append(f"+ {key}:")
            for line in formatted.split("\n"):
                lines.append(f"    {line}")
        else:
            lines.append(f"+ {key}: {formatted}")

    # Deleted variables (in call but not in return)
    for key in sorted(call_keys - return_keys):
        lines.append(f"- {key}")

    # Summary
    if unchanged_count > 0:
        lines.append(
            f"\n({unchanged_count} variable{'s' if unchanged_count != 1 else ''} unchanged)"
        )

    if not lines:
        return "(no changes)"

    return "\n".join(lines)


def generate_frame_call_content(
    node: ProcessedNode, navigator: TraceNavigator | None = None
) -> str:
    """Generate call.py content for a frame_span node."""
    call_frame = node.data.get("call_frame", {})
    path = call_frame.get("path")
    qualname = call_frame.get("qualname", "")
    co_name = call_frame.get("co_name", "")
    call_timestamp = call_frame.get("timestamp")
    call_locals = call_frame.get("locals", {})
    user_code_call_site = call_frame.get("user_code_call_site")

    # Use qualname if available, otherwise fall back to node.name
    display_name = qualname or node.name

    lines = [f"=== {display_name} ==="]
    if path:
        lines.append(f"File: {path}")

    # Add function name if qualname is different from co_name
    if qualname and co_name and qualname != co_name:
        lines.append(f"Function: {co_name}")

    lines.append(f"Duration: {node.formatted_duration()}")

    # Add timestamp
    if call_timestamp is not None:
        lines.append(f"Called at: {format_timestamp(call_timestamp)}")

    # Add call site info if available
    if user_code_call_site:
        # Use navigator to resolve path from calling frame (preferred)
        # Fall back to denormalized path field for backward compatibility
        call_site_path = (
            navigator.get_path_from_call_site(user_code_call_site)
            if navigator
            else user_code_call_site.get("path", "")
        )
        call_site_line = user_code_call_site.get("line_number", "")
        if call_site_path and call_site_line:
            lines.append(f"Called from: {call_site_path}:{call_site_line}")

    lines.extend(
        [
            "",
            "--- Locals at Call ---",
            format_locals(call_locals),
        ]
    )

    # Add children summary if this node has children
    if node.children:
        lines.extend(
            [
                "",
                "--- Children ---",
            ]
        )
        for child in node.children:
            child_name = (
                child.compact_tree_line()
                if hasattr(child, "compact_tree_line")
                else child.name
            )
            lines.append(
                f"  {child.index:3d} {child_name} ({child.formatted_duration()})"
            )

    return "\n".join(lines)


def generate_frame_return_content(node: ProcessedNode) -> str:
    """Generate return.py content for a frame_span node."""
    call_frame = node.data.get("call_frame", {})
    return_frame = node.data.get("return_frame", {})
    qualname = call_frame.get("qualname", "")
    call_locals = call_frame.get("locals", {})
    return_locals = return_frame.get("locals", {})
    return_value = return_frame.get("arg", None)
    return_timestamp = return_frame.get("timestamp")

    display_name = qualname or node.name

    lines = [
        f"=== {display_name} - Return ===",
        f"Duration: {node.formatted_duration()}",
    ]

    # Add return timestamp
    if return_timestamp is not None:
        lines.append(f"Returned at: {format_timestamp(return_timestamp)}")

    lines.extend(
        [
            "",
            "--- Return Value ---",
            format_value(return_value) if return_value is not None else "(none)",
            "",
            "--- Locals Changed ---",
            format_locals_diff(call_locals, return_locals),
        ]
    )

    return "\n".join(lines)


def generate_sql_content(
    node: ProcessedNode, navigator: TraceNavigator | None = None
) -> str:
    """Generate content for a SQL query node."""
    query = node.data.get("query", "")
    query_template = node.data.get("query_template", "")
    query_data = node.data.get("query_data")
    database = node.data.get("database")
    call_timestamp = node.data.get("call_timestamp")
    return_timestamp = node.data.get("return_timestamp")
    user_code_call_site = node.data.get("user_code_call_site")

    lines = [
        f"=== SQL Query #{node.index} ===",
        f"Duration: {node.formatted_duration()}",
    ]
    if database:
        lines.append(f"Database: {database}")

    # Add timestamps
    if call_timestamp is not None:
        lines.append(f"Started: {format_timestamp(call_timestamp)}")
    if return_timestamp is not None:
        lines.append(f"Ended: {format_timestamp(return_timestamp)}")

    # Add call site info if available
    if user_code_call_site:
        # Use navigator to resolve path from calling frame (preferred)
        # Fall back to denormalized path field for backward compatibility
        call_site_path = (
            navigator.get_path_from_call_site(user_code_call_site)
            if navigator
            else user_code_call_site.get("path", "")
        )
        call_site_line = user_code_call_site.get("line_number", "")
        call_site_frame_id = user_code_call_site.get("call_frame_id", "")
        if call_site_path and call_site_line:
            lines.append(f"Called from: {call_site_path}:{call_site_line}")
        if call_site_frame_id:
            lines.append(f"Frame ID: {call_site_frame_id}")

    lines.extend(
        [
            "",
            "--- Query (with params) ---",
            query or "(empty query)",
        ]
    )

    # Add query template (parameterized, before substitution)
    if query_template and query_template != query:
        lines.extend(
            [
                "",
                "--- Query Template ---",
                query_template,
            ]
        )

    # Add query parameters if available
    query_params = node.data.get("query_params")
    if query_params:
        lines.extend(
            [
                "",
                "--- Parameters ---",
                repr(query_params),
            ]
        )

    # Add results if available
    if query_data is not None:
        lines.extend(
            [
                "",
                "--- Result ---",
                str(query_data),
            ]
        )

    return "\n".join(lines)


def format_timestamp(timestamp: float | None) -> str:
    """Format a Unix timestamp to a human-readable string."""
    if timestamp is None:
        return "unknown"
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + " UTC"


def generate_http_request_content(node: ProcessedNode) -> str:
    """Generate request.txt content for served HTTP request."""
    request = node.data.get("request", {})

    method = request.get("method", "UNKNOWN")
    path = request.get("path_info", "/")
    scheme = request.get("scheme", "http")
    timestamp = request.get("timestamp")
    headers = request.get("headers", {})
    body = request.get("body", "")
    post_data = request.get("post_data", {})
    query_params = request.get("query_params", {})

    lines = [
        "=== HTTP Request ===",
        f"Method: {method}",
        f"Path: {path}",
        f"Scheme: {scheme}",
    ]

    if timestamp is not None:
        lines.append(f"Timestamp: {format_timestamp(timestamp)}")

    # Add query parameters if present
    if query_params:
        lines.extend(["", "--- Query Parameters ---"])
        for key, value in query_params.items():
            lines.append(f"{key}: {value}")

    lines.extend(["", "--- Headers ---"])

    for key, value in headers.items():
        lines.append(f"{key}: {value}")

    if body:
        lines.extend(
            [
                "",
                "--- Body (raw) ---",
                str(body),
            ]
        )

    if post_data:
        lines.extend(
            [
                "",
                "--- Body (parsed) ---",
            ]
        )
        for key, value in post_data.items():
            lines.append(f"{key}: {value}")

    return "\n".join(lines)


def generate_http_response_content(node: ProcessedNode) -> str:
    """Generate response.txt content for served HTTP request."""
    response = node.data.get("response", {})

    status = response.get("status_code")
    headers = response.get("headers", {})
    content = response.get("content", "")
    duration = response.get("ms_duration", 0)
    timestamp = response.get("timestamp")
    url_pattern = response.get("url_pattern")

    lines = ["=== HTTP Response ==="]
    if status is not None:
        lines.append(f"Status: {status}")
    lines.append(f"Duration: {duration:.2f}ms")

    if timestamp is not None:
        lines.append(f"Timestamp: {format_timestamp(timestamp)}")

    # Add URL pattern / routing info
    if url_pattern:
        lines.extend(["", "--- URL Pattern ---"])
        if url_pattern.get("route"):
            lines.append(f"Route: {url_pattern['route']}")
        if url_pattern.get("url_name"):
            lines.append(f"URL Name: {url_pattern['url_name']}")
        if url_pattern.get("view_qualname"):
            lines.append(f"View: {url_pattern['view_qualname']}")
        if url_pattern.get("namespace"):
            lines.append(f"Namespace: {url_pattern['namespace']}")

        # View params (positional and keyword args passed to the view)
        view_params = url_pattern.get("view_params") or {}
        if view_params.get("positional") or view_params.get("keyword"):
            lines.append("View Parameters:")
            if view_params.get("positional"):
                lines.append(f"  positional: {view_params['positional']}")
            keyword = view_params.get("keyword") or {}
            if keyword:
                for k, v in keyword.items():
                    lines.append(f"  {k}: {v}")

        # Route params (captured and default values)
        route_params = url_pattern.get("route_params") or {}
        if route_params.get("captured") or route_params.get("defaults"):
            captured = route_params.get("captured") or {}
            if captured:
                lines.append("Captured:")
                for k, v in captured.items():
                    lines.append(f"  {k}: {v}")
            defaults = route_params.get("defaults") or {}
            if defaults:
                lines.append("Defaults:")
                for k, v in defaults.items():
                    lines.append(f"  {k}: {v}")

    lines.extend(["", "--- Headers ---"])

    for key, value in headers.items():
        lines.append(f"{key}: {value}")

    if content:
        lines.extend(
            [
                "",
                "--- Body ---",
                str(content),
            ]
        )

    return "\n".join(lines)


def generate_outbound_http_content(node: ProcessedNode) -> str:
    """Generate content for outbound HTTP request node."""
    # Data can be in nested "request"/"response" dicts OR at the top level of node.data
    request = node.data.get("request", {})
    response = node.data.get("response") or {}

    # Fall back to top-level data if nested dicts are empty
    method = request.get("method") or node.data.get("method", "UNKNOWN")
    url = request.get("url") or node.data.get("url", "")
    req_headers = request.get("headers") or node.data.get("headers", {})
    req_body = request.get("body") or node.data.get("body", "")
    req_timestamp = request.get("timestamp") or node.data.get("timestamp")

    lines = [
        f"=== Outbound HTTP Request #{node.index} ===",
        f"Duration: {node.formatted_duration()}",
    ]

    # Add request timestamp if available
    if req_timestamp is not None:
        lines.append(f"Request Timestamp: {format_timestamp(req_timestamp)}")

    # Add response timestamp if available (via node.end)
    if isinstance(node.end, (int, float)):
        lines.append(f"Response Timestamp: {format_timestamp(node.end)}")
    elif node.data.get("incomplete_at_trace_boundary"):
        lines.append(
            "Response: not captured (request was still open at trace boundary)"
        )

    lines.extend(
        [
            "",
            "--- Request ---",
            f"Method: {method}",
            f"URL: {url}",
            "",
            "Headers:",
        ]
    )

    for key, value in req_headers.items():
        lines.append(f"  {key}: {value}")

    if req_body:
        lines.extend(
            [
                "",
                "Body:",
                str(req_body),
            ]
        )

    # Check for response data in nested dict or at top level
    status = response.get("status_code") or node.data.get("status_code")
    resp_headers = response.get("headers") or node.data.get("response_headers", {})
    resp_body = response.get("body") or node.data.get("response_body", "")

    if status is not None or resp_headers or resp_body:
        lines.extend(["", "--- Response ---"])
        if status is not None:
            lines.append(f"Status: {status}")

        if resp_headers:
            lines.extend(["", "Headers:"])
            for key, value in resp_headers.items():
                lines.append(f"  {key}: {value}")

        if resp_body:
            lines.extend(
                [
                    "",
                    "Body:",
                    str(resp_body),
                ]
            )

    return "\n".join(lines)


def generate_log_content(node: ProcessedNode) -> str:
    """Generate content for log message node."""
    level = node.data.get("level", "LOG")
    msg = node.data.get("msg", "")
    # "name" is the logger name from the logging filter
    logger_name = node.data.get("name", "") or node.data.get("logger", "")
    args = node.data.get("args")
    extra = node.data.get("extra")
    stack = node.data.get("stack")
    traceback = node.data.get("traceback")

    lines = [
        f"=== Log Message #{node.index} ===",
        f"Level: {level}",
    ]

    if logger_name:
        lines.append(f"Logger: {logger_name}")

    lines.extend(
        [
            "",
            "--- Message ---",
            str(msg),
        ]
    )

    # Add message formatting arguments if present
    if args:
        lines.extend(
            [
                "",
                "--- Format Arguments ---",
                repr(args),
            ]
        )

    # Add extra context if present
    if extra:
        lines.extend(
            [
                "",
                "--- Extra Context ---",
                format_value(extra),
            ]
        )

    # Add stack trace if present
    if stack:
        lines.extend(
            [
                "",
                "--- Stack ---",
                str(stack),
            ]
        )

    # Add traceback if present (from exc_info)
    if traceback:
        lines.extend(
            [
                "",
                "--- Traceback ---",
                str(traceback),
            ]
        )

    return "\n".join(lines)


def generate_exception_content(node: ProcessedNode) -> str:
    """Generate exception.txt content for a frame_span with an exception."""
    return_frame = node.data.get("return_frame", {})
    exception = return_frame.get("exception", {})

    if not exception:
        return ""

    # Handle case where exception is not a dict (e.g., ExtType from msgpack)
    if not isinstance(exception, dict):
        return f"=== Exception ===\n\n{repr(exception)}"

    # Get exception summary
    exception_summary = exception.get("exception_summary", [])
    summary_text = (
        "".join(exception_summary).strip() if exception_summary else "Unknown exception"
    )

    # Get full traceback
    exception_with_traceback = exception.get("exception_with_traceback", [])
    traceback_text = (
        "".join(exception_with_traceback) if exception_with_traceback else ""
    )

    lines = [
        "=== Exception ===",
        summary_text,
        "",
        "--- Traceback ---",
        traceback_text.strip() if traceback_text else "(no traceback available)",
    ]

    # Add frame locals at each level
    exception_frames = exception.get("exception_frames", [])
    if exception_frames:
        lines.extend(["", "--- Frame Locals ---"])
        for i, exc_frame in enumerate(exception_frames, 1):
            path = exc_frame.get("path")
            co_name = exc_frame.get("co_name")
            frame_locals = exc_frame.get("locals", {})
            expanded_locals = exc_frame.get("expanded_locals", {})

            # Build frame description with available info
            if path and co_name:
                frame_desc = f"{path} in {co_name}"
            elif path:
                frame_desc = path
            elif co_name:
                frame_desc = co_name
            else:
                frame_desc = f"frame {i}"
            lines.append(f"\nFrame {i}: {frame_desc}")
            if frame_locals:
                lines.append(format_locals(frame_locals, indent="  "))
            else:
                lines.append("  (no locals)")

            # Add expanded locals (Django models, etc.)
            if expanded_locals:
                lines.append("  Expanded:")
                for key, value in expanded_locals.items():
                    lines.append(f"    {key}: {format_value(value)}")

    return "\n".join(lines)


def generate_template_content(node: ProcessedNode) -> str:
    """Generate content for a Django template node."""
    template = node.data.get("template")
    call_context = node.data.get("call_context", {})
    return_context = node.data.get("return_context", {})
    call_timestamp = node.data.get("call_timestamp")
    return_timestamp = node.data.get("return_timestamp")

    lines = [f"=== Django Template #{node.index} ==="]
    if template:
        lines.append(f"Template: {template}")
    lines.append(f"Duration: {node.formatted_duration()}")

    # Add timestamps
    if call_timestamp is not None:
        lines.append(f"Started: {format_timestamp(call_timestamp)}")
    if return_timestamp is not None:
        lines.append(f"Ended: {format_timestamp(return_timestamp)}")

    # Add context at call time
    if call_context:
        lines.extend(
            [
                "",
                "--- Context at Render Start ---",
                format_value(call_context),
            ]
        )

    # Add context at return time (if different from call context)
    if return_context and return_context != call_context:
        lines.extend(
            [
                "",
                "--- Context at Render End ---",
                format_value(return_context),
            ]
        )

    return "\n".join(lines)


def generate_background_job_call_content(node: ProcessedNode) -> str:
    """Generate call.py content for background job node."""
    subtype = node.data.get("subtype", "job")
    name = node.data.get("name")
    args = node.data.get("args", [])
    kwargs = node.data.get("kwargs", {})
    call_timestamp = node.data.get("call_timestamp")
    return_timestamp = node.data.get("return_timestamp")

    header = f"=== Background Job: {name} ===" if name else "=== Background Job ==="
    lines = [
        header,
        f"Type: {subtype}",
        f"Duration: {node.formatted_duration()}",
    ]

    # Add timestamps
    if call_timestamp is not None:
        lines.append(f"Started: {format_timestamp(call_timestamp)}")
    if return_timestamp is not None:
        lines.append(f"Ended: {format_timestamp(return_timestamp)}")

    lines.extend(
        [
            "",
            "--- Arguments ---",
            f"args: {repr(args)}",
            f"kwargs: {repr(kwargs)}",
        ]
    )

    if node.children:
        lines.extend(
            [
                "",
                "--- Children ---",
            ]
        )
        for child in node.children:
            child_name = (
                child.compact_tree_line()
                if hasattr(child, "compact_tree_line")
                else child.name
            )
            lines.append(
                f"  {child.index:3d} {child_name} ({child.formatted_duration()})"
            )

    return "\n".join(lines)


def generate_leaf_frame_content(
    node: ProcessedNode, navigator: TraceNavigator | None = None
) -> str:
    """Generate single-file content for a leaf frame_span node."""
    call_frame = node.data.get("call_frame", {})
    return_frame = node.data.get("return_frame", {})

    path = call_frame.get("path")
    qualname = call_frame.get("qualname", "")
    co_name = call_frame.get("co_name", "")
    call_timestamp = call_frame.get("timestamp")
    return_timestamp = return_frame.get("timestamp")
    call_locals = call_frame.get("locals", {})
    return_locals = return_frame.get("locals", {})
    return_value = return_frame.get("arg", None)
    user_code_call_site = call_frame.get("user_code_call_site")

    display_name = qualname or node.name

    lines = [f"=== {display_name} ==="]
    if path:
        lines.append(f"File: {path}")

    # Add function name if qualname is different from co_name
    if qualname and co_name and qualname != co_name:
        lines.append(f"Function: {co_name}")

    lines.append(f"Duration: {node.formatted_duration()}")

    # Add timestamps
    if call_timestamp is not None:
        lines.append(f"Called at: {format_timestamp(call_timestamp)}")
    if return_timestamp is not None:
        lines.append(f"Returned at: {format_timestamp(return_timestamp)}")

    # Add call site info if available
    if user_code_call_site:
        # Use navigator to resolve path from calling frame (preferred)
        # Fall back to denormalized path field for backward compatibility
        call_site_path = (
            navigator.get_path_from_call_site(user_code_call_site)
            if navigator
            else user_code_call_site.get("path", "")
        )
        call_site_line = user_code_call_site.get("line_number", "")
        if call_site_path and call_site_line:
            lines.append(f"Called from: {call_site_path}:{call_site_line}")

    lines.extend(
        [
            "",
            "--- Locals at Call ---",
            format_locals(call_locals),
            "",
            "--- Return Value ---",
            format_value(return_value) if return_value is not None else "(none)",
            "",
            "--- Locals Changed ---",
            format_locals_diff(call_locals, return_locals),
        ]
    )

    return "\n".join(lines)


# =============================================================================
# Root-Level Index Files
# =============================================================================


def generate_overview(trace: Trace, root_nodes: List[ProcessedNode]) -> str:
    """Generate {trace_id}.txt content."""
    meta = trace.unprocessed_data.get("meta", {})
    source = meta.get("source")
    kolo_version = meta.get("version")

    # Get environment info from meta
    environment = meta.get("environment", {})
    python_version = environment.get("py_version") or meta.get("python_version")
    platform_info = environment.get("platform", "")
    system_info = environment.get("system", "")
    machine_info = environment.get("machine", "")

    # Get git commit SHA
    commit_sha = trace.unprocessed_data.get("current_commit_sha", "")

    # Get command line args
    command_line_args = trace.unprocessed_data.get("command_line_args", [])

    # Get timestamp
    timestamp = trace.unprocessed_data.get("timestamp")
    date_str = None
    if timestamp is not None:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        date_str = dt.strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        f"=== Kolo Trace {trace.id} ===",
    ]
    if trace.unprocessed_data.get("recovered"):
        lines.append(
            "WARNING: recovered partial trace; the end of execution "
            "and final metadata may be missing."
        )

    # Add request summary if available
    if root_nodes and root_nodes[0].type == "nested_served_http_request":
        req = root_nodes[0].data.get("request", {})
        resp = root_nodes[0].data.get("response", {})
        status = resp.get("status_code")
        method = req.get("method")
        path = req.get("path_info")
        # Build summary with available parts
        parts = [str(status) if status else "", method or "", path or ""]
        summary = " ".join(p for p in parts if p)
        if summary:
            lines.append(summary)

    if date_str:
        lines.append(f"Date: {date_str}")
    if source and kolo_version:
        lines.append(f"Source: {source} (kolo v{kolo_version})")
    elif source:
        lines.append(f"Source: {source}")
    if python_version:
        lines.append(f"Python: {python_version}")

    # Add platform/OS info
    if platform_info or system_info:
        platform_str = platform_info or f"{system_info} {machine_info}".strip()
        lines.append(f"Platform: {platform_str}")

    # Add git commit SHA
    if commit_sha:
        lines.append(f"Git Commit: {commit_sha}")

    # Add command line args
    if command_line_args:
        lines.extend(
            [
                "",
                "--- Command Line ---",
                " ".join(command_line_args),
            ]
        )

    lines.extend(
        [
            "",
            "--- Tree ---",
        ]
    )

    # Add compact tree
    def add_tree_lines(nodes: List[ProcessedNode], indent: str = ""):
        for node in nodes:
            tree_line = (
                node.compact_tree_line()
                if hasattr(node, "compact_tree_line")
                else node.name
            )
            dur = node.formatted_duration()
            lines.append(f"{indent}{node.index} {tree_line} {dur}")
            add_tree_lines(node.children, indent + "  ")

    add_tree_lines(root_nodes)

    # Collect flushed-subtree placeholders so the user knows where chunks of
    # the live trace were offloaded to separate child traces. Even when emit
    # inlines them on disk, surfacing a summary here makes byte / segment
    # counts greppable in the overview file.
    flushed_entries: List[tuple[ProcessedNode, int]] = []

    def collect_flushed(nodes: List[ProcessedNode]) -> None:
        for node in nodes:
            if node.type == "subtree_flushed":
                flushed_entries.append((node, node.index))
            collect_flushed(node.children)

    collect_flushed(root_nodes)

    if flushed_entries:
        lines.append("")
        lines.append("--- Flushed Subtrees ---")
        total_bytes = 0
        total_segments = 0
        for node, idx in flushed_entries:
            co_name = node.data.get("co_name", "<unknown>")
            flushed_trace_id = node.data.get("flushed_trace_id", "<unknown>")
            flushed_bytes = node.data.get("flushed_bytes", 0) or 0
            segment_count = node.data.get("flushed_segment_count")
            try:
                total_bytes += int(flushed_bytes)
            except (TypeError, ValueError):
                # Malformed trace data — skip this entry's bytes from the
                # rolled-up total but still emit the per-entry line below.
                logger.debug(
                    "non-numeric flushed_bytes %r on entry %s; skipping in total",
                    flushed_bytes,
                    flushed_trace_id,
                )
            # A single placeholder can stand in for multiple flushed segments,
            # so the rolled-up "total segments" line must sum the per-entry
            # `flushed_segment_count`, not just count placeholders. Use an
            # explicit `is None` check (not truthiness) so a real
            # ``flushed_segment_count == 0`` doesn't get silently rounded up
            # to 1, masking malformed trace data.
            if segment_count is None:
                total_segments += 1
            else:
                try:
                    total_segments += int(segment_count)
                except (TypeError, ValueError):
                    logger.debug(
                        "non-numeric flushed_segment_count %r on entry %s;"
                        " skipping in total",
                        segment_count,
                        flushed_trace_id,
                    )
            segment_str = (
                f" segments={segment_count}" if segment_count is not None else ""
            )
            lines.append(
                f"  {idx} {co_name} -> {flushed_trace_id}"
                f" bytes={flushed_bytes} ({_pretty_byte_size(flushed_bytes)})"
                f"{segment_str}"
            )
        lines.append(
            f"  total: {total_segments} segment(s) across"
            f" {len(flushed_entries)} placeholder(s),"
            f" {total_bytes} bytes ({_pretty_byte_size(total_bytes)})"
        )

    return "\n".join(lines)


# =============================================================================
# Main Emit Logic
# =============================================================================


def _load_flushed_subtree(flushed_trace_id: str) -> Optional[tuple[Any, Any]]:
    """
    Load a flushed subtree from the database and build its ProcessedTree.

    Returns a (ProcessedTree, TraceNavigator) pair on success, or None if
    the trace cannot be loaded for any reason (not found, decode failure,
    unexpected shape). Failures are logged at debug level — callers should
    fall back to rendering the placeholder metadata instead of raising.

    The kolo db location is a process-wide singleton (``get_db_path()``
    in ``kolo.db``), and trace msgpack bytes live on disk as
    ``.kolo/.internal/raw/{trace_id}.kolo`` — sqlite is just a
    metadata index. ``load_trace_from_db`` checks the file first, so
    a single global db path is all we need here.
    """
    from .db import TraceNotFoundError, get_db_path, load_trace_from_db
    from .navigator import TraceNavigator
    from .trace_container import load_trace
    from .trace import Trace

    try:
        msgpack_data, _ = load_trace_from_db(get_db_path(), flushed_trace_id)
    except TraceNotFoundError:
        logger.debug("Flushed subtree %s not found in db", flushed_trace_id)
        return None
    except Exception:  # pragma: no cover - defensive
        logger.debug(
            "Failed to load flushed subtree %s", flushed_trace_id, exc_info=True
        )
        return None

    try:
        data = load_trace(msgpack_data)
        trace = Trace(unprocessed_data=data, size=len(msgpack_data))
    except Exception:  # pragma: no cover - defensive
        logger.debug(
            "Failed to decode flushed subtree %s", flushed_trace_id, exc_info=True
        )
        return None

    tree = trace.main_tree
    navigator = TraceNavigator(tree)
    return tree, navigator


def _pretty_byte_size(num: int) -> str:
    """Format a byte count as a short human-readable string."""
    try:
        n = float(num)
    except (TypeError, ValueError):
        return str(num)
    for unit in ("B", "KB", "MB", "GB"):
        if abs(n) < 1024.0:
            if unit == "B":
                return f"{int(n)} {unit}"
            return f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} TB"


def _remove_legacy_flat_flushed_placeholder(parent_dir: Path, node_name: str) -> None:
    """Drop a stale ``{node_name}.txt`` left by a pre-inlining emit.

    Pre-inlining emits rendered flushed-subtree placeholders as a flat
    ``.txt`` file. The inlining path now always writes a directory of
    the same name. If a trace was rendered with the old code and then
    re-emitted with the new code, both shapes would coexist on disk.
    Wipe the legacy file so re-emit is idempotent.
    """
    legacy_file = parent_dir / f"{node_name}.txt"
    try:
        legacy_file.unlink()
    except FileNotFoundError:
        # The legacy flat placeholder is optional, so a missing file is fine.
        pass
    except OSError:
        logger.debug(
            "could not remove legacy flushed placeholder file %s",
            legacy_file,
            exc_info=True,
        )


def _write_flushed_segment_info(
    node: ProcessedNode,
    target_dir: Path,
    *,
    inlined: bool,
    child_root_count: Optional[int] = None,
    load_error: Optional[str] = None,
) -> None:
    """Write the metadata file describing an inlined flushed subtree."""
    co_name = node.data.get("co_name", "<unknown>")
    flushed_trace_id = node.data.get("flushed_trace_id", "<unknown>")
    flushed_bytes = node.data.get("flushed_bytes", 0)
    segment_count = node.data.get("flushed_segment_count")

    lines = ["=== Flushed Segment ==="]
    lines.append("")
    lines.append(f"Function: {co_name}")
    if segment_count is not None:
        lines.append(f"Segments: {segment_count}")
    lines.append(f"Flushed bytes: {flushed_bytes} ({_pretty_byte_size(flushed_bytes)})")
    lines.append(f"Flushed trace ID: {flushed_trace_id}")
    lines.append("")
    if inlined:
        lines.append(
            "This subtree was flushed out of the live buffer during tracing to"
        )
        lines.append("free memory. The frames have been inlined below from the child")
        lines.append("trace saved at the ID above.")
        if child_root_count is not None:
            lines.append("")
            lines.append(f"Inlined root nodes: {child_root_count}")
    else:
        lines.append("This subtree was flushed out of the live buffer during tracing.")
        if load_error:
            lines.append("")
            lines.append(f"Note: could not inline child trace ({load_error}).")

    (target_dir / "_flushed_segment.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def emit_node(
    node: ProcessedNode,
    parent_dir: Path,
    navigator: TraceNavigator,
    current_path_len: int = 0,
    *,
    overflow_dir: Optional[Path] = None,
    flattened: bool = False,
    visited_trace_ids: Optional[Set[str]] = None,
) -> None:
    """
    Recursively create directory/file structure for a node.

    Rule: Nodes with children become directories, leaf nodes become files.

    Args:
        node: The node to emit
        parent_dir: The parent directory to create this node in
        navigator: Navigation context for O(1) lookups
        current_path_len: Current accumulated path length (to avoid ENAMETOOLONG)
        overflow_dir: Fixed directory used to flatten nodes once the readable
            path budget is exhausted.
        flattened: Whether this node belongs to an already-flattened subtree.
        visited_trace_ids: Set of trace ids already inlined on the current
            recursion path. Used to prevent infinite recursion when a flushed
            subtree itself contains (cyclic) flushed references.
    """
    if visited_trace_ids is None:
        visited_trace_ids = set()

    if overflow_dir is None:
        overflow_dir = parent_dir / "_deep_nodes"

    # Once nesting exhausts the readable-name budget, put this node and all of
    # its descendants directly in one fixed directory. Hashing each component
    # alone only slowed path growth; flattening makes maximum path length
    # independent of trace depth. The overview and per-node child summaries
    # retain the parent/child relationship.
    flattened = flattened or _should_flatten_emit_node(current_path_len)
    if flattened:
        parent_dir = overflow_dir
        parent_dir.mkdir(exist_ok=True)
        current_path_len = len(os.fsencode(parent_dir))
        node_name = _get_hashed_emit_node_name(node)
    else:
        node_name = _get_emit_node_name(node, current_path_len)
    new_path_len = current_path_len + len(os.fsencode(node_name)) + 1

    def write_py(path: Path, content: str) -> None:
        """Write content as a .py file with header."""
        path.write_text(PY_FILE_HEADER + content, encoding="utf-8")

    # Special-case: inline flushed subtrees at emit time. This keeps the
    # parent ProcessedTree untouched (so navigators / overview / path budgets
    # see the original placeholder) but materializes the child frames under a
    # directory so users can browse them as if they had never been flushed.
    # ``_load_flushed_subtree`` resolves the single process-wide db path
    # internally, so this branch doesn't need a db_path argument.
    if node.type == "subtree_flushed" and not node.children:
        flushed_trace_id = node.data.get("flushed_trace_id")
        # Drop any legacy ``{node_name}.txt`` flat placeholder left by a
        # pre-inlining emit, and reset the inline directory so stale child
        # frames from a previous successful inline don't linger when this
        # emission takes the load-failure or cycle path. One rule, no
        # bidirectional stale-state reasoning needed.
        _remove_legacy_flat_flushed_placeholder(parent_dir, node_name)
        node_dir = parent_dir / node_name
        if node_dir.exists():
            try:
                shutil.rmtree(node_dir)
            except FileNotFoundError:
                # Another process removed the stale dir after exists() passed.
                pass
            except OSError:
                logger.warning(
                    "could not remove stale flushed inline directory %s",
                    node_dir,
                )
                raise
        node_dir.mkdir(exist_ok=True)
        if flushed_trace_id and flushed_trace_id in visited_trace_ids:
            # Already inlined up-stack — just drop a summary to avoid recursion.
            _write_flushed_segment_info(
                node,
                node_dir,
                inlined=False,
                load_error="already inlined in ancestor",
            )
            return
        loaded = _load_flushed_subtree(flushed_trace_id) if flushed_trace_id else None
        if loaded is None:
            _write_flushed_segment_info(
                node, node_dir, inlined=False, load_error="child trace unavailable"
            )
            return
        child_tree, child_navigator = loaded
        child_roots = list(child_tree.root_nodes)
        _write_flushed_segment_info(
            node, node_dir, inlined=True, child_root_count=len(child_roots)
        )
        assert isinstance(flushed_trace_id, str)
        next_visited: set[str] = visited_trace_ids | {flushed_trace_id}
        for child_root in child_roots:
            emit_node(
                child_root,
                parent_dir if flattened else node_dir,
                child_navigator,
                new_path_len,
                overflow_dir=overflow_dir,
                flattened=flattened,
                visited_trace_ids=next_visited,
            )
        return

    if node.children:
        # This node has children - create a directory
        node_dir = parent_dir / node_name
        node_dir.mkdir(exist_ok=True)

        # Create content files based on node type
        if node.type == "frame_span":
            write_py(node_dir / "call.py", generate_frame_call_content(node, navigator))
            write_py(node_dir / "return.py", generate_frame_return_content(node))

            # Write exception.txt if this frame has an exception
            return_frame = node.data.get("return_frame", {})
            if return_frame.get("exception"):
                (node_dir / "exception.txt").write_text(
                    generate_exception_content(node), encoding="utf-8"
                )
            elif return_frame.get("annotatedExceptionMessage"):
                # Intermediate frame in exception chain
                msg = return_frame.get("annotatedExceptionMessage", "")
                (node_dir / "exception.txt").write_text(
                    f"=== Exception Propagation ===\n\n{msg}\n\n"
                    "(This frame is in the exception propagation path. "
                    "See child frames for full exception details.)",
                    encoding="utf-8",
                )

        elif node.type == "nested_served_http_request":
            # HTTP request/response are not Python - use .txt
            (node_dir / "request.txt").write_text(
                generate_http_request_content(node), encoding="utf-8"
            )
            (node_dir / "response.txt").write_text(
                generate_http_response_content(node), encoding="utf-8"
            )

        elif node.type == "nested_background_job":
            write_py(node_dir / "call.py", generate_background_job_call_content(node))

        elif node.type == "django_template":
            (node_dir / "template.txt").write_text(
                generate_template_content(node), encoding="utf-8"
            )

        # Recursively process children
        for child in node.children:
            emit_node(
                child,
                parent_dir if flattened else node_dir,
                navigator,
                new_path_len,
                overflow_dir=overflow_dir,
                flattened=flattened,
                visited_trace_ids=visited_trace_ids,
            )

    else:
        # Leaf node - create a single file
        # Use .sql for SQL queries, .py for everything else (Python-like content)
        if node.type == "sql_query":
            file_path = parent_dir / f"{node_name}.sql"
            file_path.write_text(
                generate_sql_content(node, navigator), encoding="utf-8"
            )
        elif node.type == "frame_span":
            write_py(
                parent_dir / f"{node_name}.py",
                generate_leaf_frame_content(node, navigator),
            )

            # Write exception file if this frame has an exception
            return_frame = node.data.get("return_frame", {})
            if return_frame.get("exception"):
                (parent_dir / f"{node_name}_exception.txt").write_text(
                    generate_exception_content(node), encoding="utf-8"
                )
            elif return_frame.get("annotatedExceptionMessage"):
                msg = return_frame.get("annotatedExceptionMessage", "")
                (parent_dir / f"{node_name}_exception.txt").write_text(
                    f"=== Exception Propagation ===\n\n{msg}", encoding="utf-8"
                )
        elif node.type == "log_message":
            # Log messages are plain text
            (parent_dir / f"{node_name}.txt").write_text(
                generate_log_content(node), encoding="utf-8"
            )
        elif node.type == "outbound_http_request":
            # HTTP content is not Python
            (parent_dir / f"{node_name}.txt").write_text(
                generate_outbound_http_content(node), encoding="utf-8"
            )
        elif node.type == "nested_background_job":
            write_py(
                parent_dir / f"{node_name}.py",
                generate_background_job_call_content(node),
            )
        elif node.type == "django_template":
            (parent_dir / f"{node_name}.txt").write_text(
                generate_template_content(node), encoding="utf-8"
            )
        else:
            # Generic fallback for unknown types
            (parent_dir / f"{node_name}.txt").write_text(
                f"=== {node.type} #{node.index} ===\n\n{repr(node.data)}",
                encoding="utf-8",
            )


def _get_hashed_emit_node_name(node: ProcessedNode) -> str:
    identity = f"{node.trace_id}\0{node.type}\0{node.frame_id}\0{node.name}".encode(
        "utf-8", errors="surrogatepass"
    )
    digest = hashlib.blake2s(identity, digest_size=8).hexdigest()
    return f"{node.index:04d}_{digest}"


def _should_flatten_emit_node(current_path_len: int) -> bool:
    return MAX_PATH_LENGTH - current_path_len - 50 <= 40


def _truncate_to_filesystem_bytes(name: str, max_bytes: int) -> str:
    while len(os.fsencode(name)) > max_bytes:
        name = name[:-1].rstrip("_")
    return name


def _get_emit_node_name(node: ProcessedNode, current_path_len: int) -> str:
    """Return the node basename using the same budget logic as emit_node."""
    remaining_budget = MAX_PATH_LENGTH - current_path_len - 50
    if remaining_budget > 80:
        max_name_len = 80
    elif remaining_budget > 40:
        max_name_len = remaining_budget
    else:
        return _get_hashed_emit_node_name(node)
    name = get_node_name_for_path(node, max_name_length=max_name_len)
    return _truncate_to_filesystem_bytes(name, max_name_len)


def emit_trace(trace: Trace, output_dir: Path) -> Path:
    """
    Emit a trace into a browsable directory structure.

    ``subtree_flushed`` placeholder nodes are inlined by loading the
    referenced child trace from the kolo db (a process-wide singleton)
    and emitting its frames at the placeholder position. Inlining
    recursion is cycle-guarded against re-entering the current trace
    or any already-inlined ancestor.

    Args:
        trace: The Trace object to emit
        output_dir: Directory where the trace directory will be created

    Returns:
        Path to the created trace directory
    """
    from .navigator import TraceNavigator
    from .trace import ProcessedTree

    # Collect trees and their root nodes from ALL threads
    # We keep track of trees to create navigators for each
    trees_and_nodes: List[tuple[ProcessedTree, List[ProcessedNode]]] = []

    # ``Trace`` owns the thread-to-tree mapping and caches every tree. Keep
    # emit's historical behavior of skipping empty sections and sorting all
    # non-empty trees by their first event below.
    for section in trace.threads:
        nodes = list(section.tree.root_nodes)
        if nodes:
            trees_and_nodes.append((section.tree, nodes))

    # Fallback to main_tree if no threads or no nodes found
    if not trees_and_nodes:
        trees_and_nodes.append((trace.main_tree, list(trace.main_tree.root_nodes)))

    # Sort threads by earliest timestamp (oldest first) for consistent execution order
    def get_earliest_timestamp(
        tree_nodes: tuple[ProcessedTree, List[ProcessedNode]],
    ) -> float:
        _, nodes = tree_nodes
        timestamps = [n.start for n in nodes if n.start is not None]
        return min(timestamps) if timestamps else float("inf")

    trees_and_nodes.sort(key=get_earliest_timestamp)

    # Collect all root nodes for folder naming and overview
    # Prioritize main_tree.root_nodes first to ensure the main thread (where profiling
    # started) is checked first for HTTP/test naming, even if background threads exist
    all_root_nodes: List[ProcessedNode] = list(trace.main_tree.root_nodes)
    for tree, nodes in trees_and_nodes:
        # The main tree is already first. Extending every other thread directly
        # is linear; the old per-node ``node not in all_root_nodes`` membership
        # scan was quadratic for traces with many root calls. ProcessedNode uses
        # identity equality, so that scan did not de-duplicate separately-built
        # main-tree nodes anyway.
        if tree is not trace.main_tree:
            all_root_nodes.extend(nodes)

    # Flatten trees_and_nodes into the de-duplicated set of nodes we
    # will actually write to disk. ``all_root_nodes`` is kept for folder
    # naming because it deliberately prioritizes ``trace.main_tree`` to
    # ensure HTTP/test name detection picks the main thread first —
    # ``emitted_root_nodes`` follows earliest-timestamp sort instead and
    # is the list that matches the emitted directory shape.
    emitted_root_nodes: List[ProcessedNode] = []
    for _, nodes in trees_and_nodes:
        emitted_root_nodes.extend(nodes)

    # Create the main trace directory with descriptive name
    folder_name = get_trace_folder_name(trace, all_root_nodes)
    trace_dir = output_dir / folder_name
    trace_dir.mkdir(parents=True, exist_ok=True)

    # Generate root-level overview file. Use emitted_root_nodes so the
    # overview agrees with the on-disk directory layout —
    # all_root_nodes can double-count a single frame when trace.main_tree
    # and the per-thread tree materialize separate ProcessedNode objects
    # for it.
    (trace_dir / f"{trace.id}.txt").write_text(
        generate_overview(trace, emitted_root_nodes), encoding="utf-8"
    )

    # Calculate initial path length (trace_dir absolute path)
    initial_path_len = len(os.fsencode(trace_dir))

    # Recursively create structure for each root node
    # Each tree gets its own navigator for O(1) frame lookups
    visited_trace_ids: Set[str] = {trace.id}
    overflow_dir = trace_dir / "_deep_nodes"
    if overflow_dir.exists():
        shutil.rmtree(overflow_dir)
    for tree, root_nodes in trees_and_nodes:
        navigator = TraceNavigator(tree)
        for root_node in root_nodes:
            emit_node(
                root_node,
                trace_dir,
                navigator,
                initial_path_len,
                overflow_dir=overflow_dir,
                visited_trace_ids=visited_trace_ids,
            )

    return trace_dir
