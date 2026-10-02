from __future__ import annotations

import argparse
import logging
import os
import sys

from chalk_remote_call.handler_loader import load_function, load_handler
from chalk_remote_call.logging import JsonFormatter
from chalk_remote_call.server import serve


def _env_int(name: str) -> int | None:
    """Read an optional int from the environment; return None if unset/empty."""
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return None
    try:
        return int(raw)
    except ValueError as e:
        raise ValueError(f"{name} must be an integer, got: {raw!r}") from e


def main() -> None:
    log_handler = logging.StreamHandler(sys.stderr)
    log_handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=logging.INFO, handlers=[log_handler], force=True)
    try:
        _run()
    except Exception:
        logging.getLogger(__name__).exception("Remote-call server failed")
        sys.exit(1)


def _run() -> None:
    parser = argparse.ArgumentParser(
        prog="chalk-remote-call",
        description="Start a gRPC server implementing the Chalk RemoteCallService.",
    )
    parser.add_argument(
        "--handler",
        required=True,
        help="Dotted path to the handler function (e.g. my_module.handler)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("CHALK_REMOTE_CALL_PORT", "6666")),
        help="Port to listen on (default: 6666, env: CHALK_REMOTE_CALL_PORT)",
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("CHALK_REMOTE_CALL_HOST", "[::]"),
        help="Host to bind to (default: [::], env: CHALK_REMOTE_CALL_HOST)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=int(os.environ.get("CHALK_REMOTE_CALL_WORKERS", "10")),
        help="Number of worker threads (default: 10, env: CHALK_REMOTE_CALL_WORKERS)",
    )
    parser.add_argument(
        "--on-startup",
        default=None,
        help="Dotted path to a startup function (e.g. my_module.setup)",
    )
    parser.add_argument(
        "--on-shutdown",
        default=None,
        help="Dotted path to a shutdown function (e.g. my_module.cleanup)",
    )
    parser.add_argument(
        "--max-batching-size",
        type=int,
        default=_env_int("CHALK_REMOTE_CALL_MAX_BATCHING_SIZE"),
        help=(
            "Max concurrent requests to coalesce into a single handler "
            "invocation. Unset disables batching. "
            "(env: CHALK_REMOTE_CALL_MAX_BATCHING_SIZE)"
        ),
    )
    parser.add_argument(
        "--max-buffer-duration-ms",
        type=int,
        default=_env_int("CHALK_REMOTE_CALL_MAX_BUFFER_DURATION_MS"),
        help=(
            "Max milliseconds to buffer concurrent requests before flushing, "
            "even if max-batching-size hasn't been reached. Only effective "
            "when --max-batching-size is also set. Defaults to 1000ms when "
            "batching is enabled. "
            "(env: CHALK_REMOTE_CALL_MAX_BUFFER_DURATION_MS)"
        ),
    )
    parser.add_argument(
        "--batching-mode",
        choices=["per_caller", "combined"],
        default=os.environ.get("CHALK_REMOTE_CALL_BATCHING_MODE") or None,
        help=(
            "Coalescing variant when --max-batching-size is set. "
            "'per_caller' (default) passes events as a list of dicts; "
            "'combined' passes a single concatenated RecordBatch with "
            "offsets. (env: CHALK_REMOTE_CALL_BATCHING_MODE)"
        ),
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Log level (default: INFO)",
    )
    args = parser.parse_args()

    logging.getLogger().setLevel(args.log_level)

    from chalk_remote_call.input_transform import parse_input_args

    # Load handler
    try:
        handler, auto_startup, auto_shutdown = load_handler(args.handler)
    except Exception:
        logging.getLogger(__name__).exception("Error loading handler")
        sys.exit(1)

    # Determine startup function
    on_startup = None
    if args.on_startup:
        try:
            on_startup = load_function(args.on_startup, label="Startup")
        except Exception:
            logging.getLogger(__name__).exception("Error loading startup function")
            sys.exit(1)
    elif auto_startup is not None:
        on_startup = auto_startup

    # Determine shutdown function
    on_shutdown = None
    if args.on_shutdown:
        try:
            on_shutdown = load_function(args.on_shutdown, label="Shutdown")
        except Exception:
            logging.getLogger(__name__).exception("Error loading shutdown function")
            sys.exit(1)
    elif auto_shutdown is not None:
        on_shutdown = auto_shutdown

    # Parse input args
    arg_names = parse_input_args()

    serve(
        handler=handler,
        host=args.host,
        port=args.port,
        workers=args.workers,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        arg_names=arg_names,
        max_batching_size=args.max_batching_size,
        max_buffer_duration_ms=args.max_buffer_duration_ms,
        batching_mode=args.batching_mode,
    )
