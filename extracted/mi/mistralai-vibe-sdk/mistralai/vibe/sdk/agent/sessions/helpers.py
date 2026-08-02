"""Session helper functions and types."""

import uuid
from collections.abc import Callable

type IdFactory = Callable[[], str]


def default_id_factory() -> str:
    """Return a random UUID string for session and task identifiers."""
    return str(uuid.uuid4())
