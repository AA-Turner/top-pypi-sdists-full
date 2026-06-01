"""Context-enriched logging mixin and logger facade.

``LoggingMixin`` and ``ContextLogger`` provide structured, context-aware
logging for any layer of the application (services, delegates, repositories).

``ContextLogger`` wraps a stdlib :class:`logging.Logger` and automatically
enriches every log message with available request context (``hit_id``,
``user_id``, path params) formatted as ``key=value`` pairs.

``LoggingMixin`` is a mixin class that provides a ``self.log`` property
returning a ``ContextLogger``.  Subclasses can opt into **auto-logging**
of all public methods via ``__init_subclass__``::

    class OrderService(BaseService, LoggingMixin, auto_log=True):
        async def place_order(self, cart: Cart) -> Order:
            # entry + exception logging happens automatically
            ...

    class QuietService(BaseService, LoggingMixin):
        def do_work(self):
            self.log.info("manual log", meta={"item": 42})
"""

import asyncio
import functools
import inspect
import logging
from typing import Any, ClassVar

from csrd.context import get_path_params
from csrd.context.platform import hit_id_context, user_info_context

# ---------------------------------------------------------------------------
# Global debug mode — controls error detail verbosity across csrd packages
# ---------------------------------------------------------------------------

_debug_mode: bool = False


def configure_logging(*, debug: bool = False) -> None:
    """Set the global debug mode for csrd libraries.

    When ``debug=True``, auth error responses and other diagnostics
    include detailed context (e.g. key IDs, provider names).
    When ``debug=False`` (production default), error responses use
    generic messages like ``"Unauthorized"``.

    Call this once during application startup::

        from csrd.logging import configure_logging
        configure_logging(debug=settings.debug)
    """
    global _debug_mode
    _debug_mode = debug


def is_debug() -> bool:
    """Return ``True`` if csrd debug mode is enabled."""
    return _debug_mode


def auth_error_detail(verbose_message: str, *, fallback: str = "Unauthorized") -> str:
    """Return *verbose_message* in debug mode, *fallback* in production.

    Use this in auth components to avoid leaking internal details::

        from csrd.logging import auth_error_detail
        raise HTTPException(
            status_code=401,
            detail=auth_error_detail(f"JWKS kid={kid} not found"),
        )
    """
    return verbose_message if _debug_mode else fallback


def _collect_context() -> dict[str, Any]:
    """Gather available request context as a flat dict."""
    ctx: dict[str, Any] = {}

    hit_id = hit_id_context.get()
    if hit_id and hit_id != "unknown":
        ctx["hit_id"] = hit_id

    user = user_info_context.get()
    if user is not None:
        sub = getattr(user, "sub", None)
        if sub:
            ctx["user_id"] = sub

    path_params = get_path_params()
    if path_params:
        ctx.update(path_params)

    return ctx


def _format_message(message: str, meta: dict[str, Any] | None = None) -> str:
    """Format a message with context and optional meta as key=value pairs."""
    parts: dict[str, Any] = {}
    parts.update(_collect_context())
    if meta:
        parts.update(meta)

    if not parts:
        return message

    kv = " ".join(f"{k}={v}" for k, v in parts.items())
    return f"{message} {kv}"


class ContextLogger:
    """Wraps a stdlib ``Logger`` — auto-enriches messages with request context.

    Usage::

        logger = ContextLogger(logging.getLogger(__name__))
        logger.info("Order created", meta={"order_id": 42})
        # → "Order created hit_id=abc-123 user_id=user1 order_id=42"
    """

    __slots__ = ("_logger",)

    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    @property
    def stdlib_logger(self) -> logging.Logger:
        """Access the underlying stdlib logger directly."""
        return self._logger

    def info(
        self, message: str, *args: Any, meta: dict[str, Any] | None = None, **kwargs: Any
    ) -> None:
        kwargs.setdefault("stacklevel", 2)
        self._logger.info(_format_message(message, meta), *args, **kwargs)

    def error(
        self, message: str, *args: Any, meta: dict[str, Any] | None = None, **kwargs: Any
    ) -> None:
        kwargs.setdefault("stacklevel", 2)
        self._logger.error(_format_message(message, meta), *args, **kwargs)

    def warning(
        self, message: str, *args: Any, meta: dict[str, Any] | None = None, **kwargs: Any
    ) -> None:
        kwargs.setdefault("stacklevel", 2)
        self._logger.warning(_format_message(message, meta), *args, **kwargs)

    def debug(
        self, message: str, *args: Any, meta: dict[str, Any] | None = None, **kwargs: Any
    ) -> None:
        kwargs.setdefault("stacklevel", 2)
        self._logger.debug(_format_message(message, meta), *args, **kwargs)

    def exception(
        self, message: str, *args: Any, meta: dict[str, Any] | None = None, **kwargs: Any
    ) -> None:
        kwargs.setdefault("stacklevel", 2)
        self._logger.exception(_format_message(message, meta), *args, **kwargs)


class LoggingMixin:
    """Mixin that provides a context-enriched :class:`ContextLogger`.

    Compose with any base class::

        class MyService(BaseService, LoggingMixin):
            ...

        class MyDelegate(BaseDelegate, LoggingMixin):
            ...

    **Auto-logging** (opt-in): decorate all public methods with entry/exception
    logging automatically::

        class MyService(BaseService, LoggingMixin, auto_log=True):
            __log_exclude__ = {"health_check"}   # skip noisy methods
            ...
    """

    __log_exclude__: ClassVar[set[str]] = set()

    _context_logger: ContextLogger

    def __init_subclass__(cls, auto_log: bool = False, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not auto_log:
            return

        # Collect excludes from the full MRO
        excludes: set[str] = set()
        for klass in cls.__mro__:
            excludes |= getattr(klass, "__log_exclude__", set())

        logger = logging.getLogger(f"{cls.__module__}.{cls.__qualname__}")

        for attr_name, attr_value in list(cls.__dict__.items()):
            if attr_name.startswith("_") or attr_name in excludes or not callable(attr_value):
                continue

            if asyncio.iscoroutinefunction(attr_value):
                setattr(cls, attr_name, _wrap_async(logger, attr_name, attr_value))
            elif inspect.isfunction(attr_value):
                setattr(cls, attr_name, _wrap_sync(logger, attr_name, attr_value))

    @property
    def log(self) -> ContextLogger:
        """Context-enriched logger for this instance."""
        try:
            return self._context_logger
        except AttributeError:
            name = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
            self._context_logger = ContextLogger(logging.getLogger(name))
            return self._context_logger


def _wrap_async(logger: logging.Logger, method_name: str, fn: Any) -> Any:
    @functools.wraps(fn)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(_format_message(method_name), stacklevel=2)
        try:
            return await fn(*args, **kwargs)
        except Exception:
            logger.exception(
                _format_message(f"{method_name} failed"),
                stacklevel=2,
            )
            raise

    return wrapper


def _wrap_sync(logger: logging.Logger, method_name: str, fn: Any) -> Any:
    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(_format_message(method_name), stacklevel=2)
        try:
            return fn(*args, **kwargs)
        except Exception:
            logger.exception(
                _format_message(f"{method_name} failed"),
                stacklevel=2,
            )
            raise

    return wrapper


__all__ = ("ContextLogger", "LoggingMixin")
