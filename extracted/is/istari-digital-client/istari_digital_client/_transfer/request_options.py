"""Per-call transport options for control requests owned by the transfer engine."""

from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar

_control_request: ContextVar[bool] = ContextVar(
    "transfer_control_request", default=False
)


@contextmanager
def control_request_scope() -> Generator[None, None, None]:
    """Let the transfer engine, not urllib3, own retries and redirects.

    Token reset preserves an enclosing scope and isolates unrelated threads and
    asynchronous tasks without changing the shared client's pool configuration.
    """
    token = _control_request.set(True)
    try:
        yield
    finally:
        _control_request.reset(token)


def transport_request_options() -> dict[str, bool]:
    """Return only the per-request overrides required by the active scope."""
    if _control_request.get():
        return {"retries": False, "redirect": False}
    return {}
