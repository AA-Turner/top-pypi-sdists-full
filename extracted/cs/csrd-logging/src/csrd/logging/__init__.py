"""Context-enriched logging for all application layers.

Provides :class:`ContextLogger` (a stdlib ``Logger`` wrapper that
auto-enriches messages with request context), :class:`LoggingMixin`
(a mixin with optional auto-instrumentation of public methods), and
:class:`RequestContextFilter` (a stdlib ``logging.Filter`` for
production formatters).

Usable at any tier — services, delegates, repositories::

    from csrd.logging import LoggingMixin

    class OrderService(BaseService, LoggingMixin, auto_log=True):
        ...
"""

from ._filter import RequestContextFilter
from ._logging import ContextLogger, LoggingMixin, auth_error_detail, configure_logging, is_debug

__all__ = (
    "ContextLogger",
    "LoggingMixin",
    "RequestContextFilter",
    "auth_error_detail",
    "configure_logging",
    "is_debug",
)
