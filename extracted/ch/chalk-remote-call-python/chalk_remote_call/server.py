from __future__ import annotations

import logging
import os
from collections.abc import Callable
from typing import Any, Literal

logger = logging.getLogger(__name__)

_BATCHING_MODE_ENV = "CHALK_REMOTE_CALL_BATCHING_MODE"
_VALID_BATCHING_MODES = ("per_caller", "combined")


def _resolve_batching_mode(kwarg: str | None) -> str:
    """Resolve batching mode from kwarg or env var.

    Precedence: explicit kwarg > env var > default "per_caller". The env var
    is the canonical opt-in for combined mode; the kwarg exists so embedders
    can override programmatically.
    """
    if kwarg is not None:
        mode = kwarg
    else:
        mode = (os.environ.get(_BATCHING_MODE_ENV, "") or "per_caller").strip() or "per_caller"
    if mode not in _VALID_BATCHING_MODES:
        raise ValueError(f"batching_mode must be one of {_VALID_BATCHING_MODES}, got {mode!r}")
    return mode


def serve(
    handler: Callable[..., Any],
    host: str = "[::]",
    port: int = 6666,
    workers: int = 10,
    on_startup: Callable[[], None] | None = None,
    on_shutdown: Callable[[], None] | None = None,
    arg_names: list[str] | None = None,
    max_batching_size: int | None = None,
    max_buffer_duration_ms: int | None = None,
    batching_mode: Literal["per_caller", "combined"] | None = None,
) -> None:
    """Start the gRPC server implementing RemoteCallService.

    Args:
        handler: The user's handler function.
            Single-request mode (default): (event, context) -> result.
            Coalesced per-caller mode (when max_batching_size is set and
                batching_mode == "per_caller"):
                (events: list[dict], contexts: list[dict]) -> list[result],
                one result per input.
            Coalesced combined mode (when max_batching_size is set and
                batching_mode == "combined"):
                (combined: pa.RecordBatch, offsets: list[int], contexts: list[dict])
                    -> pa.RecordBatch with combined.num_rows rows.
        host: The host to bind to.
        port: The port to bind to.
        workers: Number of worker threads for the tokio runtime.
        on_startup: Optional startup hook called before the server starts accepting requests.
        on_shutdown: Optional shutdown hook called after the server stops accepting requests.
        arg_names: Parsed CHALK_INPUT_ARGS column names, or None.
        max_batching_size: Maximum number of concurrent requests to coalesce
            before invoking the handler. None/0 disables coalescing.
        max_buffer_duration_ms: Max time in milliseconds to buffer incoming
            requests before flushing even if max_batching_size hasn't been
            reached. Defaults to 1000ms when batching is enabled.
        batching_mode: "per_caller" (default) or "combined". Only effective
            when max_batching_size > 0. Overrides the
            CHALK_REMOTE_CALL_BATCHING_MODE env var when set; otherwise the
            env var (or "per_caller") wins.
    """
    # Keep package imports lightweight so the CLI can configure logging before dependency failures.
    from chalk_remote_call._native import start_server
    from chalk_remote_call.servicer import (
        process_batches,
        process_batches_coalesced,
        process_batches_coalesced_combined,
    )

    if on_startup is not None:
        logger.info("Running startup hook...")
        on_startup()

    mode = _resolve_batching_mode(batching_mode)

    if max_batching_size is not None and max_batching_size > 0:
        process_fn = process_batches_coalesced_combined if mode == "combined" else process_batches_coalesced
        batch_size = max_batching_size
        duration_ms = max_buffer_duration_ms if max_buffer_duration_ms is not None else 1000
        logger.info(
            "Batching enabled: mode=%s max_batching_size=%d max_buffer_duration_ms=%d",
            mode,
            batch_size,
            duration_ms,
        )
    else:
        if mode == "combined":
            raise ValueError("batching_mode='combined' requires max_batching_size > 0")
        process_fn = process_batches
        batch_size = 0
        duration_ms = 0

    logger.info("Starting server on %s:%d", host, port)
    try:
        start_server(
            handler=handler,
            process_fn=process_fn,
            host=host,
            port=port,
            workers=workers,
            arg_names=arg_names,
            max_batching_size=batch_size,
            max_buffer_duration_ms=duration_ms,
        )
    finally:
        if on_shutdown is not None:
            logger.info("Running shutdown hook...")
            on_shutdown()
