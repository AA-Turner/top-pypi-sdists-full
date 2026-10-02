"""Versioned, data-only remote exception transport shared by all call modes."""

from __future__ import annotations

import importlib
import json
import traceback
from types import TracebackType


def _user_stack(tb: TracebackType | None) -> traceback.StackSummary:
    frames = []
    entered_user_code = False
    while tb is not None:
        frame = tb.tb_frame
        module = str(frame.f_globals.get("__name__", ""))
        runner_frame = not entered_user_code and module in {
            "asyncio.base_events",
            "asyncio.runners",
            "concurrent.futures._base",
            "concurrent.futures.thread",
        }
        if not (
            runner_frame
            or module == "chalk_remote_call.servicer"
            or module == "chalk_remote_call.errors"
            or module.startswith("chalkcompute.")
            or frame.f_globals.get("__chalk_generated_handler__") is True
        ):
            entered_user_code = True
            filename, lineno = frame.f_code.co_filename, tb.tb_lineno
            source_map = frame.f_globals.get("__chalk_source_map__", {})
            mapped = source_map.get(lineno) if isinstance(source_map, dict) else None
            if isinstance(mapped, tuple) and len(mapped) == 3:
                filename, lineno, source = mapped
            else:
                source = None
            frames.append(traceback.FrameSummary(filename, lineno, frame.f_code.co_name, line=source))
        tb = tb.tb_next
    return traceback.StackSummary.from_list(frames)


def _filter_traceback(summary: traceback.TracebackException, error: BaseException) -> None:
    summary.stack = _user_stack(error.__traceback__)
    if summary.__cause__ is not None and error.__cause__ is not None:
        _filter_traceback(summary.__cause__, error.__cause__)
    if summary.__context__ is not None and error.__context__ is not None:
        _filter_traceback(summary.__context__, error.__context__)
    children = getattr(error, "exceptions", ())
    for child_summary, child in zip(getattr(summary, "exceptions", None) or (), children, strict=False):
        _filter_traceback(child_summary, child)


def serialize_exception(error: BaseException) -> str:
    """Keep chains and groups, without pickling exceptions or their locals."""
    summary = traceback.TracebackException.from_exception(error, capture_locals=False)
    internal = "".join(summary.format())
    _filter_traceback(summary, error)
    payload: dict[str, object] = {
        "chalk_remote_error": 1,
        "exception": {
            "kind": type(error).__name__[:256],
            "message": _safe_message(error),
            "stacktrace": "".join(summary.format()),
            "internal_stacktrace": internal,
        },
    }
    # Include a trace ID when serialization runs with an active trace context.
    try:
        trace = importlib.import_module("opentelemetry.trace")
        context = trace.get_current_span().get_span_context()
        if context.is_valid:
            payload["trace_id"] = format(context.trace_id, "032x")
    except ImportError:
        pass
    # gRPC status messages live in headers. Keep the complete diagnostic in
    # server logs, and bound the wire payload below common 8 KiB header limits.
    encoded = json.dumps(payload, ensure_ascii=True)
    exception = payload["exception"]
    assert isinstance(exception, dict)
    while _status_header_size(encoded) > 6000:
        field = max(exception, key=lambda key: _status_header_size(json.dumps(exception[key], ensure_ascii=True)))
        text = exception[field]
        keep = len(text) // 4
        if keep < 20:
            break
        exception[field] = text[:keep] + "\n... remote traceback truncated ...\n" + text[-keep:]
        encoded = json.dumps(payload, ensure_ascii=True)
    return encoded


def _status_header_size(message: str) -> int:
    # Tonic percent-encodes these ASCII characters in grpc-message. The JSON
    # serializer already escapes controls and non-ASCII code points.
    return len(message) + 2 * sum(char in ' "#%<>`?{}' for char in message)


def _safe_message(error: BaseException) -> str:
    try:
        return str(error)
    except Exception:
        return "<exception message unavailable>"
