"""Rollout timing logs."""

import contextlib
import json
import logging
import time
from collections.abc import Iterator
from contextvars import ContextVar
from typing import Any

logger = logging.getLogger(__name__)

_timing_fields: ContextVar[dict[str, Any] | None] = ContextVar(
    "timing_fields", default=None
)


@contextlib.contextmanager
def log_timing(operation: str, **fields: Any) -> Iterator[dict[str, Any]]:
    """Log wall time and identifiers; nested operations inherit identifiers."""
    fields = {**(_timing_fields.get() or {}), **fields}
    token = _timing_fields.set(fields)
    started_at = time.time()
    start = time.perf_counter()
    completed = False
    try:
        yield fields
        completed = True
    finally:
        elapsed = time.perf_counter() - start
        _timing_fields.reset(token)
        logger.info(
            "ROLLOUT_TIMING %s",
            json.dumps({
                **fields,
                "operation": operation,
                "started_at": started_at,
                "elapsed_seconds": elapsed,
                "completed": completed,
            }),
        )
