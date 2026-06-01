from contextlib import contextmanager
from contextvars import ContextVar
from typing import Generator

import structlog

from mistralai.workflows.core.utils.contextvars import reset_contextvar

logger = structlog.get_logger(__name__)

_context_var_local_activity_enabled: ContextVar[bool] = ContextVar("local_activity_enabled", default=False)


def is_local_activity_enabled() -> bool:
    """
    Check if local activity execution is currently enabled.

    Returns:
        bool: True if local activity execution is enabled in current context.
    """
    return _context_var_local_activity_enabled.get(False)


@contextmanager
def run_activities_locally() -> Generator[None, None, None]:
    """
    Context manager for executing activities as Temporal local activities.

    This context manager enables local activity execution for all activities
    called within its scope.
    """
    token = _context_var_local_activity_enabled.set(True)
    try:
        yield
    finally:
        reset_contextvar(_context_var_local_activity_enabled, token)
