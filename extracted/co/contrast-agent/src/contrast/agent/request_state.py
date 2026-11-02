# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import contextlib
import uuid
from contextvars import ContextVar
from typing import TYPE_CHECKING

from contrast_vendor import structlog as logging

if TYPE_CHECKING:
    from collections.abc import Generator

logger = logging.getLogger("contrast")


_request_id: ContextVar[object | None] = ContextVar("contrast_request_id", default=None)


@contextlib.contextmanager
def request_id_context() -> Generator[None, None, None]:
    """
    Context manager for request_id. Produces a uuid contextvar for uniquely identifying
    a request across contrast logs. This should be set as early as possible during
    request processing.
    """
    token = _request_id.set(uuid.uuid4().hex)
    try:
        yield
    finally:
        _request_id.reset(token)


def get_request_id() -> object | None:
    return _request_id.get()
