import subprocess
import sys
from datetime import datetime, timezone
from tempfile import NamedTemporaryFile

import msgpack


def pretty_byte_size(size_bytes):
    """Format byte size as a short, readable string.

    Uses 2-digit format with rounding to keep output compact:
    - 856000 bytes → "0.8 MB" (not "856.0 KB")
    - 499 bytes → "0.5 KB" (not "499 B")
    """
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

    # Start with bytes
    ratio = float(size_bytes)
    index = 0

    # Keep dividing by 1024 until we get a value < 100 (2 digits max)
    # or we run out of units
    while ratio >= 100 and index < len(size_name) - 1:
        ratio /= 1024
        index += 1

    # Format with one decimal place, no padding
    if ratio >= 10:
        # For 10-99.9, show no decimal to keep it short
        return f"{ratio:.0f} {size_name[index]}"
    else:
        # For 0.1-9.9, show one decimal place
        return f"{ratio:.1f} {size_name[index]}"


def maybe_format(rendered):
    rendered = maybe_isort(rendered)

    try:
        import ruff  # noqa: F401
    except ImportError:
        if len(rendered) <= 1_000_000:
            rendered = maybe_black(rendered)
        return rendered

    with NamedTemporaryFile("w+", delete=False) as f:
        f.write(rendered)
        name = f.name

    subprocess.run(
        [
            sys.executable,
            "-m",
            "ruff",
            "format",
            name,
            "--config",
            "format.skip-magic-trailing-comma=true",
        ],
        check=True,
    )
    with open(name) as f:
        rendered = f.read()

    return rendered


def maybe_black(rendered):
    try:
        from black import format_file_contents
        from black.mode import Mode
        from black.parsing import InvalidInput
        from black.report import NothingChanged
    except ImportError:
        return rendered

    try:
        return format_file_contents(
            rendered, fast=True, mode=Mode(magic_trailing_comma=False)
        )
    except (InvalidInput, NothingChanged):
        return rendered


def maybe_isort(rendered):
    try:
        import ruff  # noqa: F401
    except ImportError:
        # Fallback to isort if Ruff is not available
        try:
            from isort.api import sort_code_string
        except ImportError:
            return rendered
        return sort_code_string(rendered)

    with NamedTemporaryFile("w+", delete=False) as f:
        f.write(rendered)
        name = f.name

    subprocess.run(
        [sys.executable, "-m", "ruff", "check", name, "--select", "I", "--fix"],
        check=False,  # Don't fail if there are unfixable issues
    )
    with open(name) as f:
        rendered = f.read()

    return rendered


def extract_main_frames_from_data(data):
    if "config" not in data["meta"]:
        # config is not present in old traces
        return data["frames_of_interest"]

    if data.get("threads"):
        current_thread_id = data["current_thread_id"]
        if current_thread_id in data["threads"]:
            return data["threads"][current_thread_id]["frames"]
        else:
            return []
    else:
        return data["frames_of_interest"]


def extract_http_trace_name(frames_by_thread, current_thread_id):
    """
    Extract HTTP request/response information from frames to set a trace name.
    Looks for django_request and django_response frame types from the Django filter.

    Returns:
        A formatted trace name string or None if no HTTP information found
    """
    request_frame = None
    response_frame = None

    frames_from_current_thread = frames_by_thread.get(current_thread_id, [])
    first_three = frames_from_current_thread[:3]
    last_three = frames_from_current_thread[-3:]

    relevant_frames = first_three + last_three

    unpacked_frames = [
        msgpack.unpackb(f, strict_map_key=False) for f in relevant_frames
    ]

    for frame in unpacked_frames:
        if frame.get("type") == "django_request":
            if request_frame is None:
                # first frame wins
                request_frame = frame
        elif frame.get("type") == "django_response":
            # last frame wins
            response_frame = frame

    if request_frame and response_frame:
        method = request_frame.get("method")
        path = request_frame.get("path_info")
        status_code = response_frame.get("status_code")

        if method and path and status_code:
            return f"{status_code} {method} {path}"

    return None


def extract_test_trace_name(frames_by_thread, current_thread_id):
    """
    Extract test name information from frames to set a trace name.
    Looks for start_test frame type from the pytest filter.

    Returns:
        A formatted trace name string or None if no test information found
    """
    frames_from_current_thread = frames_by_thread.get(current_thread_id, [])
    if not frames_from_current_thread:
        return None

    # Look at first and last few frames to be safe
    first_three = frames_from_current_thread[:3]
    last_three = frames_from_current_thread[-3:]

    relevant_frames = first_three + last_three

    unpacked_frames = [
        msgpack.unpackb(f, strict_map_key=False) for f in relevant_frames
    ]

    start_frame = None
    end_frame = None

    for frame in unpacked_frames:
        if frame.get("type") == "start_test":
            if start_frame is None:
                # first frame wins
                start_frame = frame
        elif frame.get("type") == "end_test":
            # last frame wins
            end_frame = frame

    # We want both start and end frames to be present to ensure we have a complete test
    if start_frame and end_frame:
        test_name = start_frame.get("test_name")
        test_class = start_frame.get("test_class")

        if test_name:
            if test_class:
                return f"{test_class}.{test_name}"
            return test_name

    return None


def relative_time(timestamp: datetime) -> str:
    now = datetime.now(timezone.utc)

    delta = now - timestamp
    if delta.days > 7:
        relative_time = timestamp.strftime("%Y-%m-%d")
    elif delta.days > 0:
        relative_time = f"{delta.days}d ago"
    elif delta.seconds > 3600:
        relative_time = f"{delta.seconds // 3600}h ago"
    elif delta.seconds > 60:
        relative_time = f"{delta.seconds // 60}m ago"
    elif delta.seconds >= 1:
        relative_time = f"{delta.seconds}s ago"
    else:
        relative_time = f"{delta.microseconds // 1000}ms ago"

    return relative_time
