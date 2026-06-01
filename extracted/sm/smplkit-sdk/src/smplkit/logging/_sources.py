"""LoggerSource — explicit logger registration descriptor."""

from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from smplkit import LogLevel


@dataclasses.dataclass
class LoggerSource:
    """Describes a logger to register via :meth:`SmplManagementClient.loggers.register`.

    Used both for buffered runtime discovery (called by ``SmplClient`` as adapters
    discover loggers) and for explicit registration from setup scripts that already
    know the ``(service, environment)`` they belong to.

    Args:
        name: Logger name (e.g. ``"sqlalchemy.engine"``).  Normalized to lowercase
            with slashes and colons replaced by dots before sending to the API.
        resolved_level: Effective log level for this source.
        level: Explicit (configured) log level, if different from ``resolved_level``.
            Pass ``None`` when the level is inherited.
        service: Service name this source belongs to (optional).
        environment: Environment name this source belongs to (optional).
    """

    name: str
    resolved_level: LogLevel
    level: LogLevel | None = None
    service: str | None = None
    environment: str | None = None
