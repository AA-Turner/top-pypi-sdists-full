"""The Smpl Logging client — one unified ``LoggingClient`` / ``AsyncLoggingClient``.

Smpl Logging has two surfaces on a single client, mirroring how the config,
flags, audit, and jobs clients expose their full surface from one class:

* **CRUD surface** — works without :meth:`install`. Two sub-clients:

  * ``client.logging.loggers`` — logger CRUD + discovery: ``new`` / ``list`` /
    ``get`` / ``delete`` plus ``register`` / ``flush`` / ``flush_sync`` /
    ``pending_count``.
  * ``client.logging.log_groups`` — log-group CRUD: ``new`` / ``list`` /
    ``get`` / ``delete``.

  The fused client owns the logger-discovery buffer directly; the ``loggers``
  sub-client shares that same buffer so discovery and explicit registration
  drain through one queue.

* **Live surface** — directly on the client. :meth:`register_adapter` is a
  PRE-install configuration call (allowed before :meth:`install`).
  :meth:`install` opens the live connection (monkey-patches the app's logging
  framework, discovers loggers, fetches + applies levels, opens the shared
  WebSocket). ``on_change`` / ``refresh`` require :meth:`install` first;
  calling them earlier raises :class:`NotInstalledError`.

The client supports two construction shapes:

* **Wired** into :class:`smplkit.SmplClient` — borrows the parent's logging
  transport for both runtime fetch and CRUD and the parent's shared WebSocket
  for the live channel. This is the common path.
* **Standalone** — ``LoggingClient(api_key=..., base_url=..., ...)`` builds and
  owns its own logging transport and an app transport (the WebSocket gateway
  lives on the app service), and on :meth:`install` opens and owns its own
  WebSocket. ``close()`` / ``aclose()`` tears down only the owned transports
  and owned WebSocket.
"""

from __future__ import annotations

import dataclasses
import logging as stdlib_logging
import threading
import traceback
from importlib.metadata import entry_points
from typing import TYPE_CHECKING, Any, Callable

from smplkit._config import _service_url, resolve_client_config
from smplkit._debug import debug
from smplkit.errors import (
    ConflictError,
    ConnectionError,
    NotFoundError,
    NotInstalledError,
    TimeoutError,
    ValidationError,
    _raise_for_status,
)
from smplkit._helpers import key_to_display_name, paginate_async, paginate_sync
from smplkit._generated.app.client import AuthenticatedClient as _AppAuthClient
from smplkit._generated.logging.client import AuthenticatedClient
from smplkit._generated.logging.api.loggers import (  # noqa: F401  (re-exported for tests)
    bulk_register_loggers,
    delete_logger,
    get_logger,
    list_loggers,
    update_logger,
)
from smplkit._generated.logging.api.log_groups import (  # noqa: F401  (re-exported)
    create_log_group,
    delete_log_group,
    get_log_group,
    list_log_groups,
    update_log_group,
)
from smplkit._generated.logging.models.log_group import LogGroup as GenLogGroup  # noqa: F401
from smplkit._generated.logging.models.log_group_resource import LogGroupResource  # noqa: F401
from smplkit._generated.logging.models.log_group_response import LogGroupResponse
from smplkit._generated.logging.models.logger import Logger as GenLogger  # noqa: F401
from smplkit._generated.logging.models.logger_resource import LoggerResource  # noqa: F401
from smplkit._generated.logging.models.logger_response import LoggerResponse
from smplkit.logging._levels import python_level_to_smpl, smpl_level_to_python
from smplkit.logging._normalize import normalize_logger_name
from smplkit.logging.adapters.base import LoggingAdapter
from smplkit.logging.helpers import (  # noqa: F401  (re-exported below)
    _build_log_group_body as _build_group_body,
    _build_logger_body,
    _extract_datetime,
    _extract_environments,
    _extract_sources,
    _logger_resource_to_async_model,
    _logger_resource_to_model,
    _log_group_resource_to_async_model,
    _log_group_resource_to_model,
    _loglevel_value,
    _make_environments,
    _make_group_environments,
    _str_to_log_level,
    _unset_to_none,
)
from smplkit.logging.models import (  # noqa: F401  (re-exported below)
    AsyncSmplLogGroup,
    AsyncSmplLogger,
    SmplLogGroup,
    SmplLogger,
    _environments_to_wire as _logger_environments_to_wire,
)
from smplkit.logging._resolution import resolve_level
from smplkit.logging.sources import LoggerSource
from smplkit._buffer import _LOGGER_BATCH_FLUSH_SIZE, _LoggerRegistrationBuffer
from smplkit._ws import SharedWebSocket

if TYPE_CHECKING:
    from smplkit._metrics import _AsyncMetricsReporter, _MetricsReporter
    from smplkit.clients import AsyncSmplClient, SmplClient

logger = stdlib_logging.getLogger("smplkit")

_DEFAULT_LOGGING_BASE_URL = "https://logging.smplkit.com"

_NOT_INSTALLED_MESSAGE = (
    "Smpl Logging live operations require install() first — this opens a live "
    "connection to your running service and hooks into your application's "
    "logging framework. Call client.logging.install() (await for async) before "
    "on_change()/refresh()."
)


def _check_response_status(status_code: Any, content: bytes) -> None:
    """Map HTTP error status codes to SDK exceptions with full JSON:API error detail."""
    _raise_for_status(int(status_code), content)


def _exc_url(exc: Exception) -> str | None:
    try:
        return str(exc.request.url)  # type: ignore[attr-defined]
    except Exception:
        return None


def _maybe_reraise_network_error(exc: Exception, base_url: str | None = None) -> None:
    """Re-raise httpx exceptions as SDK exceptions if applicable."""
    import httpx

    if isinstance(exc, httpx.TimeoutException):
        url = _exc_url(exc) or base_url
        msg = f"Request timed out connecting to {url}" if url else f"Request timed out: {exc}"
        raise TimeoutError(msg) from exc
    if isinstance(exc, httpx.HTTPError):
        url = _exc_url(exc) or base_url
        msg = f"Cannot connect to {url}: {exc}" if url else f"Connection error: {exc}"
        raise ConnectionError(msg) from exc
    if isinstance(exc, (NotFoundError, ConflictError, ValidationError)):
        raise exc


def _pagination_kwargs(page_number: int | None, page_size: int | None) -> dict[str, int]:
    kwargs: dict[str, int] = {}
    if page_number is not None:
        kwargs["pagenumber"] = page_number
    if page_size is not None:
        kwargs["pagesize"] = page_size
    return kwargs


def _build_logger_bulk_request(buffer: Any) -> Any:
    """Drain the logger-discovery buffer and build a JSON:API bulk request body.

    Returns ``None`` when there is nothing to flush.
    """
    from smplkit._generated.logging.models.logger_bulk_item import LoggerBulkItem
    from smplkit._generated.logging.models.logger_bulk_request import LoggerBulkRequest

    batch = buffer.drain()
    if not batch:
        return None
    items = [
        LoggerBulkItem(
            id=b["id"],
            level=b.get("level"),
            resolved_level=b["resolved_level"],
            service=b.get("service"),
            environment=b.get("environment"),
        )
        for b in batch
    ]
    return LoggerBulkRequest(loggers=items)


def _logging_transport(
    *,
    api_key: str | None,
    base_url: str | None,
    profile: str | None,
    base_domain: str | None,
    scheme: str | None,
    debug: bool | None,
    extra_headers: dict[str, str] | None,
) -> tuple[AuthenticatedClient, _AppAuthClient, str]:
    """Build standalone logging + app transports and resolve the app base URL.

    ``base_url``/``api_key`` are used directly when both are supplied (the
    path a top-level client takes after it has already resolved them);
    otherwise the config resolver fills in whatever is missing
    (``~/.smplkit`` / env vars / defaults). The app transport is needed for
    the WebSocket gateway, which lives on the app service (like flags); the
    app base URL is returned so a standalone client can open its own WebSocket
    against the event gateway.
    """
    cfg = resolve_client_config(
        profile=profile,
        api_key=api_key,
        base_domain=base_domain,
        scheme=scheme,
        debug=debug,
    )
    resolved_key = api_key if api_key is not None else cfg.api_key
    logging_url = base_url if base_url is not None else _service_url(cfg.scheme, "logging", cfg.base_domain)
    app_url = _service_url(cfg.scheme, "app", cfg.base_domain)
    headers: dict[str, str] = {}
    headers.update(cfg.extra_headers or {})
    headers.update(extra_headers or {})
    logging_http = AuthenticatedClient(base_url=logging_url.rstrip("/"), token=resolved_key, headers=headers)
    app_http = _AppAuthClient(base_url=app_url.rstrip("/"), token=resolved_key, headers=headers)
    return logging_http, app_http, app_url


# ---------------------------------------------------------------------------
# Change event
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True, kw_only=True)
class LoggerChangeEvent:
    """Fired once per managed logger whose effective level the SDK just applied.

    Fields:
    - ``id``: the affected logger's normalized id.
    - ``level``: the newly-applied effective smplkit level string (e.g.
      ``"INFO"``, ``"DEBUG"``); same value the resolution algorithm
      returns and that ``smpl_level_to_python`` converts.
    - ``source``: short string identifying the trigger — typically
      ``"websocket"`` or ``"manual"`` (a :meth:`refresh` call).
    """

    id: str
    level: str
    source: str


# ---------------------------------------------------------------------------
# Adapter auto-loading
# ---------------------------------------------------------------------------


def _auto_load_adapters() -> list[LoggingAdapter]:
    """Discover and load adapters registered under the smplkit.logging.adapters entry-point group."""
    adapters: list[LoggingAdapter] = []
    for ep in entry_points(group="smplkit.logging.adapters"):
        try:
            cls = ep.load()
            adapters.append(cls())
            debug("lifecycle", f"Loaded logging adapter: {ep.name}")
        except ImportError:
            debug("lifecycle", f"Skipped logging adapter {ep.name} (dependency not installed)")
        except Exception:
            logger.warning("Failed to load logging adapter %s", ep.name, exc_info=True)
    if not adapters:
        logger.warning("No logging framework detected. Runtime logging control requires a supported framework.")
    return adapters


# ---------------------------------------------------------------------------
# Management sub-clients: loggers
# ---------------------------------------------------------------------------


class LoggersClient:
    """Surface for ``client.logging.loggers.*`` (sync).

    Logger CRUD plus the discovery buffer. The buffer is owned by the fused
    :class:`LoggingClient` and shared here so discovery (driven by
    :meth:`LoggingClient.install`) and explicit :meth:`register` drain through
    one queue.
    """

    def __init__(self, http_client: AuthenticatedClient, *, base_url: str, buffer: _LoggerRegistrationBuffer) -> None:
        self._http_client = http_client
        self._base_url = base_url
        self._buffer = buffer

    def register(
        self,
        items: LoggerSource | list[LoggerSource],
        *,
        flush: bool = False,
    ) -> None:
        """Queue one or more logger sources for registration with the server.

        Sources are buffered locally and sent in a batch. The batch is sent
        automatically once enough sources accumulate; pass ``flush=True`` to
        send the current batch right away instead of waiting.

        Args:
            items: A single logger source, or a list of them, to queue.
            flush: When ``True``, send the buffered sources immediately rather
                than waiting for the batch to fill. The async client has no
                equivalent flag — it has no synchronous flush path, so callers
                there queue and then ``await flush()`` explicitly.
        """
        batch = items if isinstance(items, list) else [items]
        for src in batch:
            self._buffer.add(
                normalize_logger_name(src.name),
                _loglevel_value(src.level, where="register[level]"),
                _loglevel_value(src.resolved_level, where="register[resolved_level]"),
                src.service,
                src.environment,
            )
        if flush:
            self.flush()
            return
        if self._buffer.pending_count >= _LOGGER_BATCH_FLUSH_SIZE:
            threading.Thread(target=self._threshold_flush, daemon=True).start()

    def _threshold_flush(self) -> None:
        try:
            self.flush()
        except Exception as exc:
            logger.warning("Logger registration flush failed: %s", exc)

    def flush(self) -> None:
        """Drain the buffer and POST pending logger sources to the bulk endpoint."""
        body = _build_logger_bulk_request(self._buffer)
        if body is None:
            return
        try:
            response = bulk_register_loggers.sync_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)

    def flush_sync(self) -> None:
        """Synchronous flush — alias of :meth:`flush` for the periodic-flush path."""
        self.flush()

    @property
    def pending_count(self) -> int:
        """Number of sources queued and awaiting flush."""
        return self._buffer.pending_count

    def new(self, id: str, *, managed: bool = True) -> SmplLogger:
        """Build a new unsaved logger.

        The returned :class:`SmplLogger` is local only; call its
        :meth:`SmplLogger.save` to persist it.

        Args:
            id: Identifier for the logger (its normalized name).
            managed: When ``True`` (the default), smplkit controls this
                logger's level at runtime. Set ``False`` to register the
                logger for visibility without taking over its level.

        Returns:
            An unsaved :class:`SmplLogger` bound to this client.
        """
        return SmplLogger(self, id=id, name=id, managed=managed)

    def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[SmplLogger]:
        """List loggers for the authenticated account.

        Args:
            page_number: 1-based page index to fetch. When omitted, the
                server returns the first page.
            page_size: Maximum number of loggers per page. When omitted, the
                server applies its default page size.

        Returns:
            The loggers on the requested page as :class:`SmplLogger` objects.
        """
        kwargs = _pagination_kwargs(page_number, page_size)
        try:
            response = list_loggers.sync_detailed(client=self._http_client, **kwargs)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        if response.parsed is None or not hasattr(response.parsed, "data"):
            return []
        return [_logger_resource_to_model(self, r) for r in response.parsed.data]

    def get(self, id: str) -> SmplLogger:
        """Fetch a single logger by id.

        Args:
            id: Identifier of the logger to fetch.

        Returns:
            The editable :class:`SmplLogger` resource.

        Raises:
            NotFoundError: If no logger with that id exists.
        """
        try:
            response = get_logger.sync_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        if response.parsed is None:
            raise NotFoundError(f"Logger with id {id!r} not found", status_code=404)
        return _logger_resource_to_model(self, response.parsed.data)

    def delete(self, id: str) -> None:
        """Delete a logger by id.

        Args:
            id: Identifier of the logger to delete.
        """
        try:
            response = delete_logger.sync_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)

    def _save_logger(self, lg: SmplLogger) -> SmplLogger:
        body = _build_logger_body(
            logger_id=lg.id,
            name=lg.name,
            level=_loglevel_value(lg.level, where="SmplLogger.save"),
            managed=lg.managed,
            group=lg.group,
            environments=_logger_environments_to_wire(lg._environments) if lg._environments else None,
        )
        try:
            response = update_logger.sync_detailed(lg.id, client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        if response.parsed is None:
            raise ValidationError(
                f"HTTP {int(response.status_code)}: unexpected response", status_code=int(response.status_code)
            )
        return _logger_resource_to_model(self, response.parsed.data)


class AsyncLoggersClient:
    """Surface for ``client.logging.loggers.*`` (async)."""

    def __init__(self, http_client: AuthenticatedClient, *, base_url: str, buffer: _LoggerRegistrationBuffer) -> None:
        self._http_client = http_client
        self._base_url = base_url
        self._buffer = buffer

    def register(
        self,
        items: LoggerSource | list[LoggerSource],
    ) -> None:
        """Queue one or more logger sources for registration with the server.

        Sources are buffered locally and sent in a batch once enough
        accumulate. Unlike the sync client, this method has no ``flush``
        flag — there is no synchronous flush path here, so to send the
        current batch right away call ``await flush()`` explicitly.

        Args:
            items: A single logger source, or a list of them, to queue.
        """
        batch = items if isinstance(items, list) else [items]
        for src in batch:
            self._buffer.add(
                normalize_logger_name(src.name),
                _loglevel_value(src.level, where="register[level]"),
                _loglevel_value(src.resolved_level, where="register[resolved_level]"),
                src.service,
                src.environment,
            )
        if self._buffer.pending_count >= _LOGGER_BATCH_FLUSH_SIZE:
            threading.Thread(target=self._threshold_flush, daemon=True).start()

    def _threshold_flush(self) -> None:
        try:
            self.flush_sync()
        except Exception as exc:
            logger.warning("Logger registration flush failed: %s", exc)

    async def flush(self) -> None:
        """Drain the buffer and POST pending logger sources to the bulk endpoint."""
        body = _build_logger_bulk_request(self._buffer)
        if body is None:
            return
        try:
            response = await bulk_register_loggers.asyncio_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)

    def flush_sync(self) -> None:
        """Synchronous flush from a background thread (final flush, threshold flush)."""
        body = _build_logger_bulk_request(self._buffer)
        if body is None:
            return
        try:
            response = bulk_register_loggers.sync_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)

    @property
    def pending_count(self) -> int:
        """Number of sources queued and awaiting flush."""
        return self._buffer.pending_count

    def new(self, id: str, *, managed: bool = True) -> AsyncSmplLogger:
        """Build a new unsaved logger.

        The returned :class:`AsyncSmplLogger` is local only; ``await`` its
        :meth:`AsyncSmplLogger.save` to persist it.

        Args:
            id: Identifier for the logger (its normalized name).
            managed: When ``True`` (the default), smplkit controls this
                logger's level at runtime. Set ``False`` to register the
                logger for visibility without taking over its level.

        Returns:
            An unsaved :class:`AsyncSmplLogger` bound to this client.
        """
        return AsyncSmplLogger(self, id=id, name=id, managed=managed)

    async def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[AsyncSmplLogger]:
        """List loggers for the authenticated account.

        Awaits the network round-trip.

        Args:
            page_number: 1-based page index to fetch. When omitted, the
                server returns the first page.
            page_size: Maximum number of loggers per page. When omitted, the
                server applies its default page size.

        Returns:
            The loggers on the requested page as :class:`AsyncSmplLogger` objects.
        """
        kwargs = _pagination_kwargs(page_number, page_size)
        try:
            response = await list_loggers.asyncio_detailed(client=self._http_client, **kwargs)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        if response.parsed is None or not hasattr(response.parsed, "data"):
            return []
        return [_logger_resource_to_async_model(self, r) for r in response.parsed.data]

    async def get(self, id: str) -> AsyncSmplLogger:
        """Fetch a single logger by id.

        Awaits the network round-trip.

        Args:
            id: Identifier of the logger to fetch.

        Returns:
            The editable :class:`AsyncSmplLogger` resource.

        Raises:
            NotFoundError: If no logger with that id exists.
        """
        try:
            response = await get_logger.asyncio_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        if response.parsed is None:
            raise NotFoundError(f"Logger with id {id!r} not found", status_code=404)
        return _logger_resource_to_async_model(self, response.parsed.data)

    async def delete(self, id: str) -> None:
        """Delete a logger by id.

        Awaits the network round-trip.

        Args:
            id: Identifier of the logger to delete.
        """
        try:
            response = await delete_logger.asyncio_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)

    async def _save_logger(self, lg: AsyncSmplLogger) -> AsyncSmplLogger:
        body = _build_logger_body(
            logger_id=lg.id,
            name=lg.name,
            level=_loglevel_value(lg.level, where="AsyncSmplLogger.save"),
            managed=lg.managed,
            group=lg.group,
            environments=_logger_environments_to_wire(lg._environments) if lg._environments else None,
        )
        try:
            response = await update_logger.asyncio_detailed(lg.id, client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        if response.parsed is None:
            raise ValidationError(
                f"HTTP {int(response.status_code)}: unexpected response", status_code=int(response.status_code)
            )
        return _logger_resource_to_async_model(self, response.parsed.data)


# ---------------------------------------------------------------------------
# Management sub-clients: log groups
# ---------------------------------------------------------------------------


class LogGroupsClient:
    """Surface for ``client.logging.log_groups.*`` (sync)."""

    def __init__(self, http_client: AuthenticatedClient, *, base_url: str) -> None:
        self._http_client = http_client
        self._base_url = base_url

    def new(self, id: str, *, name: str | None = None, group: str | None = None) -> SmplLogGroup:
        """Build a new unsaved log group.

        The returned :class:`SmplLogGroup` is local only; call its
        :meth:`SmplLogGroup.save` to persist it.

        Args:
            id: Identifier for the log group.
            name: Human-readable display name. Defaults to a title-cased
                version of ``id`` when omitted.
            group: Identifier of the parent log group, when nesting groups.
                ``None`` for a top-level group.

        Returns:
            An unsaved :class:`SmplLogGroup` bound to this client.
        """
        return SmplLogGroup(
            self,
            id=id,
            name=name if name is not None else key_to_display_name(id),
            group=group,
        )

    def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[SmplLogGroup]:
        """List log groups for the authenticated account.

        Args:
            page_number: 1-based page index to fetch. When omitted, the
                server returns the first page.
            page_size: Maximum number of log groups per page. When omitted,
                the server applies its default page size.

        Returns:
            The log groups on the requested page as :class:`SmplLogGroup` objects.
        """
        kwargs = _pagination_kwargs(page_number, page_size)
        try:
            response = list_log_groups.sync_detailed(client=self._http_client, **kwargs)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        if response.parsed is None or not hasattr(response.parsed, "data"):
            return []
        return [_log_group_resource_to_model(self, r) for r in response.parsed.data]

    def get(self, id: str) -> SmplLogGroup:
        """Fetch a single log group by id.

        Args:
            id: Identifier of the log group to fetch.

        Returns:
            The editable :class:`SmplLogGroup` resource.

        Raises:
            NotFoundError: If no log group with that id exists.
        """
        try:
            response = get_log_group.sync_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        if response.parsed is None:
            raise NotFoundError(f"Log group with id {id!r} not found", status_code=404)
        return _log_group_resource_to_model(self, response.parsed.data)

    def delete(self, id: str) -> None:
        """Delete a log group by id.

        Args:
            id: Identifier of the log group to delete.
        """
        try:
            response = delete_log_group.sync_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)

    def _save_group(self, grp: SmplLogGroup) -> SmplLogGroup:
        body = _build_group_body(
            group_id=grp.id,
            name=grp.name,
            level=_loglevel_value(grp.level, where="SmplLogGroup.save"),
            group=grp.group,
            environments=_logger_environments_to_wire(grp._environments) if grp._environments else None,
        )
        try:
            if grp.created_at is None:
                response = create_log_group.sync_detailed(client=self._http_client, body=body)
            else:
                response = update_log_group.sync_detailed(grp.id, client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        if response.parsed is None:
            raise ValidationError(
                f"HTTP {int(response.status_code)}: unexpected response", status_code=int(response.status_code)
            )
        return _log_group_resource_to_model(self, response.parsed.data)


class AsyncLogGroupsClient:
    """Surface for ``client.logging.log_groups.*`` (async)."""

    def __init__(self, http_client: AuthenticatedClient, *, base_url: str) -> None:
        self._http_client = http_client
        self._base_url = base_url

    def new(self, id: str, *, name: str | None = None, group: str | None = None) -> AsyncSmplLogGroup:
        """Build a new unsaved log group.

        The returned :class:`AsyncSmplLogGroup` is local only; ``await`` its
        :meth:`AsyncSmplLogGroup.save` to persist it.

        Args:
            id: Identifier for the log group.
            name: Human-readable display name. Defaults to a title-cased
                version of ``id`` when omitted.
            group: Identifier of the parent log group, when nesting groups.
                ``None`` for a top-level group.

        Returns:
            An unsaved :class:`AsyncSmplLogGroup` bound to this client.
        """
        return AsyncSmplLogGroup(
            self,
            id=id,
            name=name if name is not None else key_to_display_name(id),
            group=group,
        )

    async def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[AsyncSmplLogGroup]:
        """List log groups for the authenticated account.

        Awaits the network round-trip.

        Args:
            page_number: 1-based page index to fetch. When omitted, the
                server returns the first page.
            page_size: Maximum number of log groups per page. When omitted,
                the server applies its default page size.

        Returns:
            The log groups on the requested page as :class:`AsyncSmplLogGroup`
            objects.
        """
        kwargs = _pagination_kwargs(page_number, page_size)
        try:
            response = await list_log_groups.asyncio_detailed(client=self._http_client, **kwargs)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        if response.parsed is None or not hasattr(response.parsed, "data"):
            return []
        return [_log_group_resource_to_async_model(self, r) for r in response.parsed.data]

    async def get(self, id: str) -> AsyncSmplLogGroup:
        """Fetch a single log group by id.

        Awaits the network round-trip.

        Args:
            id: Identifier of the log group to fetch.

        Returns:
            The editable :class:`AsyncSmplLogGroup` resource.

        Raises:
            NotFoundError: If no log group with that id exists.
        """
        try:
            response = await get_log_group.asyncio_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        if response.parsed is None:
            raise NotFoundError(f"Log group with id {id!r} not found", status_code=404)
        return _log_group_resource_to_async_model(self, response.parsed.data)

    async def delete(self, id: str) -> None:
        """Delete a log group by id.

        Awaits the network round-trip.

        Args:
            id: Identifier of the log group to delete.
        """
        try:
            response = await delete_log_group.asyncio_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)

    async def _save_group(self, grp: AsyncSmplLogGroup) -> AsyncSmplLogGroup:
        body = _build_group_body(
            group_id=grp.id,
            name=grp.name,
            level=_loglevel_value(grp.level, where="AsyncSmplLogGroup.save"),
            group=grp.group,
            environments=_logger_environments_to_wire(grp._environments) if grp._environments else None,
        )
        try:
            if grp.created_at is None:
                response = await create_log_group.asyncio_detailed(client=self._http_client, body=body)
            else:
                response = await update_log_group.asyncio_detailed(grp.id, client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        if response.parsed is None:
            raise ValidationError(
                f"HTTP {int(response.status_code)}: unexpected response", status_code=int(response.status_code)
            )
        return _log_group_resource_to_async_model(self, response.parsed.data)


# ---------------------------------------------------------------------------
# LoggingClient (sync)
# ---------------------------------------------------------------------------


class LoggingClient:
    """The Smpl Logging client (sync).

    One client exposes the full surface, reachable as ``client.logging``
    (:class:`smplkit.SmplClient`) or constructed directly::

        from smplkit import LoggingClient

        with LoggingClient(environment="production", service="my-svc") as logging:
            logging.loggers.new("sqlalchemy.engine").save()
            logging.install()

    The CRUD surface (``loggers`` / ``log_groups`` sub-clients) works without
    :meth:`install`. :meth:`register_adapter` is a pre-install configuration call.
    The live surface (``install`` / ``on_change`` / ``refresh``) requires
    :meth:`install` first; calling ``on_change`` / ``refresh`` earlier raises
    :class:`NotInstalledError`.

    Args:
        api_key: API key. When omitted, resolved from ``SMPLKIT_API_KEY`` or
            ``~/.smplkit``.
        environment: Deployment environment used to resolve runtime levels and
            to scope discovery declarations. Optional.
        base_url: Full logging-service base URL. Usually resolved from
            ``base_domain``/``scheme``; supplied directly by the top-level
            clients which have already computed it.
        profile: Named ``~/.smplkit`` profile section.
        base_domain: Base domain for API requests (default ``"smplkit.com"``).
        scheme: URL scheme (default ``"https"``).
        debug: Enable SDK debug logging.
        extra_headers: Extra headers attached to every request.
        parent: Internal — the owning :class:`smplkit.SmplClient`. Not for
            direct use.
        transport: Internal — a pre-built logging transport supplied by a
            top-level client so the logging surface shares one connection pool.
            Not for direct use.
        metrics: Internal — the parent's metrics reporter.
    """

    loggers: LoggersClient
    log_groups: LogGroupsClient

    def __init__(
        self,
        api_key: str | None = None,
        *,
        environment: str | None = None,
        base_url: str | None = None,
        profile: str | None = None,
        base_domain: str | None = None,
        scheme: str | None = None,
        debug: bool | None = None,
        extra_headers: dict[str, str] | None = None,
        parent: SmplClient | None = None,
        transport: AuthenticatedClient | None = None,
        metrics: _MetricsReporter | None = None,
    ) -> None:
        self._parent = parent
        self._metrics = metrics
        self._environment = parent._environment if parent is not None else environment
        self._service = parent._service if parent is not None else None
        self._standalone_api_key: str | None = None
        if transport is not None:
            self._logging_http = transport
            self._logging_base_url = str(transport._base_url)
            self._app_base_url: str | None = None
            self._owns_transport = False
        else:
            self._logging_http, app_http, self._app_base_url = _logging_transport(
                api_key=api_key,
                base_url=base_url,
                profile=profile,
                base_domain=base_domain,
                scheme=scheme,
                debug=debug,
                extra_headers=extra_headers,
            )
            self._logging_base_url = str(self._logging_http._base_url)
            self._app_http_standalone = app_http
            self._owns_transport = True
            self._standalone_api_key = api_key if api_key is not None else self._logging_http.token

        # Discovery buffer is owned by this client; the loggers sub-client
        # shares it so discovery and explicit registration drain together.
        self._buffer = _LoggerRegistrationBuffer()
        self.loggers = LoggersClient(self._logging_http, base_url=self._logging_base_url, buffer=self._buffer)
        self.log_groups = LogGroupsClient(self._logging_http, base_url=self._logging_base_url)

        # Live-surface state.
        self._connected = False
        self._name_map: dict[str, str] = {}  # original_name → normalized_id
        self._loggers_cache: dict[str, dict[str, Any]] = {}  # id → logger data
        self._groups_cache: dict[str, dict[str, Any]] = {}  # id → group data
        self._global_listeners: list[Callable[..., Any]] = []
        self._key_listeners: dict[str, list[Callable[..., Any]]] = {}
        self._adapters: list[LoggingAdapter] = []
        self._explicit_adapters = False
        self._ws_manager: SharedWebSocket | None = None
        self._owns_ws = False

    def _close(self) -> None:
        """Release resources held by this client (alias for :meth:`close`)."""
        self.close()

    # --- Adapter registration (pre-install, ungated) ---

    def register_adapter(self, adapter: LoggingAdapter) -> None:
        """Register a logging adapter. Must be called before :meth:`install`.

        Registering at least one adapter disables auto-loading — only the
        adapters you register explicitly are used. This is a pre-install
        configuration call: it is intentionally NOT gated by :meth:`install`.

        Args:
            adapter: The logging-framework adapter to use for discovering
                loggers and applying levels.

        Raises:
            RuntimeError: If called after :meth:`install`.
        """
        if self._connected:
            raise RuntimeError("Cannot register adapters after install()")
        self._explicit_adapters = True
        self._adapters.append(adapter)

    # --- Live surface: install (gate) + transport / WebSocket helpers ---

    def _require_installed(self) -> None:
        if not self._connected:
            raise NotInstalledError(_NOT_INSTALLED_MESSAGE)

    def _ensure_ws(self) -> SharedWebSocket:
        """Return the shared WebSocket — the parent's when wired, else our own."""
        if self._parent is not None:
            return self._parent._ensure_ws()
        if self._ws_manager is None:
            self._ws_manager = SharedWebSocket(
                app_base_url=self._app_base_url,
                api_key=self._standalone_api_key,
                metrics=self._metrics,
            )
            self._ws_manager.start()
            self._owns_ws = True
        return self._ws_manager

    def install(self) -> None:
        """Hook smplkit into the application's logging machinery.

        Loads adapters, scans existing loggers, applies levels from the
        smplkit server, and wires WebSocket handlers for live updates. This
        IS the explicit consent gate — :meth:`on_change` / :meth:`refresh`
        require it first.

        Idempotent — safe to call multiple times.
        """
        debug("lifecycle", "LoggingClient.install() called")
        if self._parent is not None:
            self._parent._ensure_started()
        if self._connected:
            return

        # 0. Load adapters
        if not self._adapters:
            self._adapters = _auto_load_adapters()

        # 1. Discover existing loggers from all adapters
        for adapter in self._adapters:
            try:
                existing = adapter.discover()
                debug("discovery", f"adapter {adapter.name!r} discovered {len(existing)} existing loggers")
                for name, explicit_level, effective_level in existing:
                    self._name_map[name] = normalize_logger_name(name)
                    self.loggers.register(self._loggersource_for(name, explicit_level, effective_level))
            except Exception:
                logger.warning("Adapter %s discover() failed", adapter.name, exc_info=True)

        # 2. Install continuous discovery hooks
        for adapter in self._adapters:
            try:
                adapter.install_hook(self._on_new_logger)
            except Exception:
                logger.warning("Adapter %s install_hook() failed", adapter.name, exc_info=True)

        # 3. Flush initial batch
        try:
            self.loggers.flush()
        except Exception as exc:
            logger.warning("Bulk logger registration failed: %s", exc)
            debug("registration", traceback.format_exc().strip())

        # 4-6. Fetch, resolve, apply
        try:
            self._fetch_and_apply(trigger="install()")
        except Exception as exc:
            logger.warning(
                "Failed to fetch/apply logging levels during connect (logging: %s): %s",
                self._logging_base_url,
                exc,
            )
            debug("resolution", traceback.format_exc().strip())

        # 7. Register WebSocket event handlers for real-time level updates
        self._ws_manager = self._ensure_ws()
        self._ws_manager.on("logger_changed", self._handle_logger_changed)
        self._ws_manager.on("logger_deleted", self._handle_logger_deleted)
        self._ws_manager.on("group_changed", self._handle_group_changed)
        self._ws_manager.on("group_deleted", self._handle_group_deleted)
        self._ws_manager.on("loggers_changed", self._handle_loggers_changed)

        self._connected = True

    # --- Live surface: change listeners ---

    def on_change(self, fn_or_key: Callable[..., Any] | str | None = None) -> Any:
        """Register a callback fired whenever a logger's effective level changes.

        Used as a decorator in two forms:

        - ``@client.logging.on_change`` — a global listener fired for every
          logger whose level changes.
        - ``@client.logging.on_change("sqlalchemy.engine")`` — a key-scoped
          listener fired only for the named logger.

        The decorated callback receives a :class:`LoggerChangeEvent`.

        Requires :meth:`install` first.

        Args:
            fn_or_key: The callback when used as a bare decorator, or the
                logger id to scope to when called with a string. ``None``
                when used as ``@on_change()`` with empty parentheses, which
                registers a global listener.

        Returns:
            The callback itself (bare-decorator form), or a decorator that
            registers and returns the callback (string / no-argument form).

        Raises:
            NotInstalledError: If called before :meth:`install`.
        """
        self._require_installed()
        if callable(fn_or_key):
            # @on_change (bare decorator)
            self._global_listeners.append(fn_or_key)
            return fn_or_key
        elif isinstance(fn_or_key, str):
            # @on_change("key")
            key = fn_or_key

            def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
                self._key_listeners.setdefault(key, []).append(fn)
                return fn

            return decorator
        else:
            # @on_change() — called with parens but no args

            def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
                self._global_listeners.append(fn)
                return fn

            return decorator

    def refresh(self) -> None:
        """Re-fetch all loggers and groups and fire listener events for any deltas.

        Requires :meth:`install` first; raises :class:`NotInstalledError`
        otherwise.
        """
        self._require_installed()
        debug("resolution", "refresh() called, triggering full resolution pass")
        self._fetch_and_apply_deltas(trigger="refresh()", source="manual")

    def _snapshot_effective_levels(self) -> dict[str, str]:
        """Effective level for every locally-tracked managed logger.

        This is the universe of loggers the adapter applies levels to —
        the only loggers whose listener can fire. A logger not in
        ``_name_map`` (never instantiated locally) or marked
        ``managed=False`` in the cache is excluded.
        """
        snapshot: dict[str, str] = {}
        for normalized_id in self._name_map.values():
            entry = self._loggers_cache.get(normalized_id)
            if entry is None or not entry.get("managed"):
                continue
            snapshot[normalized_id] = resolve_level(
                normalized_id, self._environment, self._loggers_cache, self._groups_cache
            )
        return snapshot

    def _apply_deltas_and_fire(self, pre: dict[str, str], source: str) -> None:
        """Apply + fire per-logger whenever the effective level moved.

        For every locally-tracked managed logger, recompute the effective
        level and compare to ``pre``. On a delta: call ``apply_level`` on
        every adapter AND fire one :class:`LoggerChangeEvent` per affected
        logger — once to each matching key-scoped listener and once to
        every global listener (a global is semantically a key-scoped
        subscription on every logger). No-op when nothing moved: no apply,
        no fire.
        """
        for original_name, normalized_id in self._name_map.items():
            entry = self._loggers_cache.get(normalized_id)
            if entry is None or not entry.get("managed"):
                continue
            new = resolve_level(normalized_id, self._environment, self._loggers_cache, self._groups_cache)
            if pre.get(normalized_id) == new:
                continue
            python_level = smpl_level_to_python(new)
            for adapter in self._adapters:
                try:
                    adapter.apply_level(original_name, python_level)
                except Exception:
                    logger.warning("Adapter %s apply_level() failed for %s", adapter.name, original_name, exc_info=True)
            metrics = self._metrics
            if metrics is not None:
                metrics.record("logging.level_changes", unit="changes", dimensions={"logger": normalized_id})
            self._fire_for_logger(normalized_id, new, source)

    def _fire_for_logger(self, logger_id: str, level: str, source: str) -> None:
        """Fire one :class:`LoggerChangeEvent` to every matching subscriber.

        Both the key-scoped listeners registered for ``logger_id`` and
        every global listener receive the same payload.
        """
        event = LoggerChangeEvent(id=logger_id, level=level, source=source)
        for cb in self._global_listeners:
            try:
                cb(event)
            except Exception:
                logger.error("Exception in global logging on_change listener", exc_info=True)
        for cb in self._key_listeners.get(logger_id, []):
            try:
                cb(event)
            except Exception:
                logger.error("Exception in key-scoped logging on_change listener", exc_info=True)

    # --- Internal: event handlers (called by SharedWebSocket) ---

    def _handle_logger_changed(self, data: dict) -> None:
        key = data.get("id", "")
        debug("websocket", f"logger_changed: fetching logger {key!r}")
        pre = self._snapshot_effective_levels()
        try:
            response = get_logger.sync_detailed(key, client=self._logging_http)
            _check_response_status(response.status_code, response.content)
        except Exception as exc:
            logger.warning("Failed to fetch logger %r after WS event: %s", key, exc)
            debug("websocket", traceback.format_exc().strip())
            return
        if isinstance(response.parsed, LoggerResponse):
            r = response.parsed.data
            attrs = r.attributes
            lid = _unset_to_none(r.id) or key
            self._loggers_cache[lid] = {
                "level": _unset_to_none(attrs.level),
                "group": _unset_to_none(attrs.group),
                "managed": _unset_to_none(attrs.managed),
                "environments": _extract_environments(attrs.environments),
            }
        self._apply_deltas_and_fire(pre, "websocket")

    def _handle_logger_deleted(self, data: dict) -> None:
        key = data.get("id", "")
        debug("websocket", f"logger_deleted: removing logger {key!r}")
        pre = self._snapshot_effective_levels()
        self._loggers_cache.pop(key, None)
        self._apply_deltas_and_fire(pre, "websocket")

    def _handle_group_changed(self, data: dict) -> None:
        key = data.get("id", "")
        debug("websocket", f"group_changed: fetching group {key!r}")
        pre = self._snapshot_effective_levels()
        try:
            response = get_log_group.sync_detailed(key, client=self._logging_http)
            _check_response_status(response.status_code, response.content)
        except Exception as exc:
            logger.warning("Failed to fetch log group %r after WS event: %s", key, exc)
            debug("websocket", traceback.format_exc().strip())
            return
        if isinstance(response.parsed, LogGroupResponse):
            r = response.parsed.data
            attrs = r.attributes
            gid = _unset_to_none(r.id) or key
            self._groups_cache[gid] = {
                "level": _unset_to_none(attrs.level),
                "group": _unset_to_none(attrs.parent_id),
                "environments": _extract_environments(attrs.environments),
            }
        self._apply_deltas_and_fire(pre, "websocket")

    def _handle_group_deleted(self, data: dict) -> None:
        key = data.get("id", "")
        debug("websocket", f"group_deleted: removing group {key!r}")
        pre = self._snapshot_effective_levels()
        self._groups_cache.pop(key, None)
        self._apply_deltas_and_fire(pre, "websocket")

    def _handle_loggers_changed(self, data: dict) -> None:
        debug("websocket", "loggers_changed: full re-fetch")
        try:
            self._fetch_and_apply_deltas(trigger="loggers_changed WS event", source="websocket")
        except Exception as exc:
            logger.warning("Failed to re-fetch/apply logging levels after loggers_changed event: %s", exc)
            debug("websocket", traceback.format_exc().strip())

    def close(self) -> None:
        """Release resources — only those this client owns.

        Uninstalls the adapter hooks, unsubscribes from the WebSocket, and
        tears down the owned WebSocket (standalone install) and the owned
        logging + app HTTP transports (standalone construction). A wired
        client borrows the parent's transport and WebSocket and closes
        neither.
        """
        debug("lifecycle", "LoggingClient.close() called")
        for adapter in self._adapters:
            try:
                adapter.uninstall_hook()
            except Exception:
                logger.warning("Adapter %s uninstall_hook() failed", adapter.name, exc_info=True)
        if self._ws_manager is not None:
            self._ws_manager.off("logger_changed", self._handle_logger_changed)
            self._ws_manager.off("logger_deleted", self._handle_logger_deleted)
            self._ws_manager.off("group_changed", self._handle_group_changed)
            self._ws_manager.off("group_deleted", self._handle_group_deleted)
            self._ws_manager.off("loggers_changed", self._handle_loggers_changed)
            if self._owns_ws:
                self._ws_manager.stop()
                self._owns_ws = False
            self._ws_manager = None
        if self._owns_transport:
            client = self._logging_http._client
            if client is not None:
                client.close()
                self._logging_http._client = None
            app_client = self._app_http_standalone._client
            if app_client is not None:
                app_client.close()
                self._app_http_standalone._client = None

    def __enter__(self) -> LoggingClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    # --- Internal ---

    def _loggersource_for(self, name: str, explicit_level: int | None, effective_level: int) -> LoggerSource:
        """Build a LoggerSource from an adapter's (name, explicit, effective) discovery tuple."""
        from smplkit import LogLevel

        return LoggerSource(
            name=name,
            resolved_level=LogLevel(python_level_to_smpl(effective_level)),
            level=LogLevel(python_level_to_smpl(explicit_level)) if explicit_level is not None else None,
            service=self._service,
            environment=self._environment,
        )

    def _on_new_logger(self, name: str, explicit_level: int | None, effective_level: int) -> None:
        """Callback from adapters when a new logger is created."""
        normalized = normalize_logger_name(name)
        debug("discovery", f"new logger intercepted via callback: {name!r} (normalized: {normalized!r})")
        self._name_map[name] = normalized
        self.loggers.register(self._loggersource_for(name, explicit_level, effective_level))
        debug(
            "registration",
            f"queued {name!r} for bulk registration (buffer size: {self.loggers.pending_count})",
        )

        # If connected, try to apply level from cache
        if self._connected and normalized in self._loggers_cache:
            entry = self._loggers_cache[normalized]
            if entry.get("managed"):
                debug("resolution", f"applying immediate level for newly discovered managed logger {name!r}")
                resolved = resolve_level(normalized, self._environment, self._loggers_cache, self._groups_cache)
                python_level = smpl_level_to_python(resolved)
                for adapter in self._adapters:
                    try:
                        adapter.apply_level(name, python_level)
                    except Exception:
                        logger.warning("Adapter %s apply_level() failed for %s", adapter.name, name, exc_info=True)

    def _fetch_cache(self, trigger: str) -> None:
        """Re-fetch loggers/groups into the cache (no apply, no fire)."""
        debug("resolution", f"full resolution pass starting (trigger: {trigger})")

        def fetch_loggers_page(page_number: int, page_size: int) -> list[tuple[str, dict[str, Any]]]:
            debug("api", f"GET /api/v1/loggers (page {page_number})")
            try:
                response = list_loggers.sync_detailed(
                    client=self._logging_http,
                    pagenumber=page_number,
                    pagesize=page_size,
                )
                _check_response_status(response.status_code, response.content)
            except Exception as exc:
                _maybe_reraise_network_error(exc, self._logging_base_url)
                raise
            page_rows: list[tuple[str, dict[str, Any]]] = []
            if response.parsed is not None and hasattr(response.parsed, "data"):
                for r in response.parsed.data:
                    attrs = r.attributes
                    lid = _unset_to_none(r.id) or ""
                    page_rows.append(
                        (
                            lid,
                            {
                                "level": _unset_to_none(attrs.level),
                                "group": _unset_to_none(attrs.group),
                                "managed": _unset_to_none(attrs.managed),
                                "environments": _extract_environments(attrs.environments),
                            },
                        )
                    )
            debug(
                "api",
                f"GET /api/v1/loggers page {page_number} -> {response.status_code.value} ({len(page_rows)} loggers)",
            )
            return page_rows

        loggers_data: dict[str, dict[str, Any]] = dict(paginate_sync(fetch_loggers_page))

        def fetch_groups_page(page_number: int, page_size: int) -> list[tuple[str, dict[str, Any]]]:
            debug("api", f"GET /api/v1/log-groups (page {page_number})")
            try:
                grp_response = list_log_groups.sync_detailed(
                    client=self._logging_http,
                    pagenumber=page_number,
                    pagesize=page_size,
                )
                _check_response_status(grp_response.status_code, grp_response.content)
            except Exception as exc:
                _maybe_reraise_network_error(exc, self._logging_base_url)
                raise
            page_rows: list[tuple[str, dict[str, Any]]] = []
            if grp_response.parsed is not None and hasattr(grp_response.parsed, "data"):
                for r in grp_response.parsed.data:
                    attrs = r.attributes
                    gid = _unset_to_none(r.id) or ""
                    page_rows.append(
                        (
                            gid,
                            {
                                "level": _unset_to_none(attrs.level),
                                "group": _unset_to_none(attrs.parent_id),
                                "environments": _extract_environments(attrs.environments),
                            },
                        )
                    )
            debug(
                "api",
                f"GET /api/v1/log-groups page {page_number} -> {grp_response.status_code.value} ({len(page_rows)} groups)",
            )
            return page_rows

        groups_data: dict[str, dict[str, Any]] = dict(paginate_sync(fetch_groups_page))

        self._loggers_cache = loggers_data
        self._groups_cache = groups_data

    def _fetch_and_apply(self, trigger: str = "unknown") -> None:
        """Fetch loggers/groups and unconditionally apply levels (initial install path).

        Silent — does not fire change-listener events. Use
        :meth:`_fetch_and_apply_deltas` from the WS / refresh paths to get
        per-logger fanout.
        """
        self._fetch_cache(trigger)
        self._apply_levels()

    def _fetch_and_apply_deltas(self, trigger: str, source: str) -> None:
        """Fetch loggers/groups; apply + fire listeners only on effective-level deltas."""
        pre = self._snapshot_effective_levels()
        self._fetch_cache(trigger)
        self._apply_deltas_and_fire(pre, source)

    def _apply_levels(self) -> None:
        """Apply resolved levels to all managed, locally-present loggers."""
        debug("resolution", f"running full resolution pass for {len(self._name_map)} local loggers")
        for original_name, normalized_id in self._name_map.items():
            entry = self._loggers_cache.get(normalized_id)
            if entry is None:
                continue
            if not entry.get("managed"):
                continue
            resolved = resolve_level(normalized_id, self._environment, self._loggers_cache, self._groups_cache)
            python_level = smpl_level_to_python(resolved)
            for adapter in self._adapters:
                try:
                    adapter.apply_level(original_name, python_level)
                except Exception:
                    logger.warning("Adapter %s apply_level() failed for %s", adapter.name, original_name, exc_info=True)
            metrics = self._metrics
            if metrics is not None:
                metrics.record("logging.level_changes", unit="changes", dimensions={"logger": normalized_id})


# ---------------------------------------------------------------------------
# AsyncLoggingClient
# ---------------------------------------------------------------------------


class AsyncLoggingClient:
    """The Smpl Logging client (async) — counterpart of :class:`LoggingClient`.

    Reads, CRUD, and discovery flush perform their network round-trips with
    ``await``. :meth:`register_adapter` is a pre-install configuration call;
    the live surface (``install`` / ``on_change`` / ``refresh``) requires
    :meth:`install` first; calling ``on_change`` / ``refresh`` earlier raises
    :class:`NotInstalledError`.
    """

    loggers: AsyncLoggersClient
    log_groups: AsyncLogGroupsClient

    def __init__(
        self,
        api_key: str | None = None,
        *,
        environment: str | None = None,
        base_url: str | None = None,
        profile: str | None = None,
        base_domain: str | None = None,
        scheme: str | None = None,
        debug: bool | None = None,
        extra_headers: dict[str, str] | None = None,
        parent: AsyncSmplClient | None = None,
        transport: AuthenticatedClient | None = None,
        metrics: _AsyncMetricsReporter | None = None,
    ) -> None:
        self._parent = parent
        self._metrics = metrics
        self._environment = parent._environment if parent is not None else environment
        self._service = parent._service if parent is not None else None
        self._standalone_api_key: str | None = None
        if transport is not None:
            self._logging_http = transport
            self._logging_base_url = str(transport._base_url)
            self._app_base_url: str | None = None
            self._owns_transport = False
        else:
            self._logging_http, app_http, self._app_base_url = _logging_transport(
                api_key=api_key,
                base_url=base_url,
                profile=profile,
                base_domain=base_domain,
                scheme=scheme,
                debug=debug,
                extra_headers=extra_headers,
            )
            self._logging_base_url = str(self._logging_http._base_url)
            self._app_http_standalone = app_http
            self._owns_transport = True
            self._standalone_api_key = api_key if api_key is not None else self._logging_http.token

        self._buffer = _LoggerRegistrationBuffer()
        self.loggers = AsyncLoggersClient(self._logging_http, base_url=self._logging_base_url, buffer=self._buffer)
        self.log_groups = AsyncLogGroupsClient(self._logging_http, base_url=self._logging_base_url)

        self._connected = False
        self._name_map: dict[str, str] = {}
        self._loggers_cache: dict[str, dict[str, Any]] = {}
        self._groups_cache: dict[str, dict[str, Any]] = {}
        self._global_listeners: list[Callable[..., Any]] = []
        self._key_listeners: dict[str, list[Callable[..., Any]]] = {}
        self._adapters: list[LoggingAdapter] = []
        self._explicit_adapters = False
        self._ws_manager: SharedWebSocket | None = None
        self._owns_ws = False

    def _close(self) -> None:
        """Synchronous teardown of adapter hooks, WS subscription, and owned
        sync transports (no event-loop dependency).

        The async transport pools are torn down by :meth:`aclose`. Called by
        :class:`AsyncSmplClient.close`, which closes the wired async transport
        pools.
        """
        debug("lifecycle", "AsyncLoggingClient._close() called")
        for adapter in self._adapters:
            try:
                adapter.uninstall_hook()
            except Exception:
                logger.warning("Adapter %s uninstall_hook() failed", adapter.name, exc_info=True)
        if self._ws_manager is not None:
            self._ws_manager.off("logger_changed", self._handle_logger_changed)
            self._ws_manager.off("logger_deleted", self._handle_logger_deleted)
            self._ws_manager.off("group_changed", self._handle_group_changed)
            self._ws_manager.off("group_deleted", self._handle_group_deleted)
            self._ws_manager.off("loggers_changed", self._handle_loggers_changed)
            if self._owns_ws:
                self._ws_manager.stop()
                self._owns_ws = False
            self._ws_manager = None
        if self._owns_transport:
            client = self._logging_http._client
            if client is not None:
                client.close()
                self._logging_http._client = None
            app_client = self._app_http_standalone._client
            if app_client is not None:
                app_client.close()
                self._app_http_standalone._client = None

    # --- Adapter registration (pre-install, ungated) ---

    def register_adapter(self, adapter: LoggingAdapter) -> None:
        """Register a logging adapter. Must be called before :meth:`install`.

        Registering at least one adapter disables auto-loading — only the
        adapters you register explicitly are used. This is a pre-install
        configuration call: it is intentionally NOT gated by :meth:`install`,
        and is synchronous (no ``await``).

        Args:
            adapter: The logging-framework adapter to use for discovering
                loggers and applying levels.

        Raises:
            RuntimeError: If called after :meth:`install`.
        """
        if self._connected:
            raise RuntimeError("Cannot register adapters after install()")
        self._explicit_adapters = True
        self._adapters.append(adapter)

    # --- Live surface: install (gate) + transport / WebSocket helpers ---

    def _require_installed(self) -> None:
        if not self._connected:
            raise NotInstalledError(_NOT_INSTALLED_MESSAGE)

    def _ensure_ws(self) -> SharedWebSocket:
        """Return the shared WebSocket — the parent's when wired, else our own."""
        if self._parent is not None:
            return self._parent._ensure_ws()
        if self._ws_manager is None:
            self._ws_manager = SharedWebSocket(
                app_base_url=self._app_base_url,
                api_key=self._standalone_api_key,
                metrics=self._metrics,
            )
            self._ws_manager.start()
            self._owns_ws = True
        return self._ws_manager

    async def install(self) -> None:
        """Hook smplkit into the application's logging machinery.

        Awaits the network work. In order, this:

        1. Loads the registered (or auto-detected) logging adapters.
        2. Scans the application's existing loggers and installs hooks so
           loggers created later are picked up too.
        3. Fetches the configured levels from the smplkit server and applies
           them to the matching loggers.
        4. Opens the shared WebSocket so level changes arrive live.

        This is the explicit consent gate: :meth:`on_change` and
        :meth:`refresh` require :meth:`install` first and otherwise raise
        :class:`NotInstalledError`. Idempotent — calling it again after a
        successful install is a no-op.
        """
        debug("lifecycle", "AsyncLoggingClient.install() called")
        if self._parent is not None:
            self._parent._ensure_started()
        if self._connected:
            return

        # 0. Load adapters
        if not self._adapters:
            self._adapters = _auto_load_adapters()

        # 1. Discover existing loggers from all adapters
        for adapter in self._adapters:
            try:
                existing = adapter.discover()
                debug("discovery", f"adapter {adapter.name!r} discovered {len(existing)} existing loggers")
                for name, explicit_level, effective_level in existing:
                    self._name_map[name] = normalize_logger_name(name)
                    self.loggers.register(self._loggersource_for(name, explicit_level, effective_level))
            except Exception:
                logger.warning("Adapter %s discover() failed", adapter.name, exc_info=True)

        # 2. Install continuous discovery hooks
        for adapter in self._adapters:
            try:
                adapter.install_hook(self._on_new_logger)
            except Exception:
                logger.warning("Adapter %s install_hook() failed", adapter.name, exc_info=True)

        await self._flush_bulk_async()

        try:
            await self._fetch_and_apply(trigger="install()")
        except Exception as exc:
            logger.warning(
                "Failed to fetch/apply logging levels during connect (logging: %s): %s",
                self._logging_base_url,
                exc,
            )
            debug("resolution", traceback.format_exc().strip())

        # Register WebSocket event handlers for real-time level updates
        self._ws_manager = self._ensure_ws()
        self._ws_manager.on("logger_changed", self._handle_logger_changed)
        self._ws_manager.on("logger_deleted", self._handle_logger_deleted)
        self._ws_manager.on("group_changed", self._handle_group_changed)
        self._ws_manager.on("group_deleted", self._handle_group_deleted)
        self._ws_manager.on("loggers_changed", self._handle_loggers_changed)

        self._connected = True

    # --- Live surface: change listeners ---

    def on_change(self, fn_or_key: Callable[..., Any] | str | None = None) -> Any:
        """Register a callback fired whenever a logger's effective level changes.

        Used as a decorator in two forms:

        - ``@client.logging.on_change`` — a global listener fired for every
          logger whose level changes.
        - ``@client.logging.on_change("sqlalchemy.engine")`` — a key-scoped
          listener fired only for the named logger.

        The decorated callback receives a :class:`LoggerChangeEvent`.
        Registration itself is synchronous (no ``await``); the callback is
        invoked when a change arrives over the live connection.

        Requires :meth:`install` first.

        Args:
            fn_or_key: The callback when used as a bare decorator, or the
                logger id to scope to when called with a string. ``None``
                when used as ``@on_change()`` with empty parentheses, which
                registers a global listener.

        Returns:
            The callback itself (bare-decorator form), or a decorator that
            registers and returns the callback (string / no-argument form).

        Raises:
            NotInstalledError: If called before :meth:`install`.
        """
        self._require_installed()
        if callable(fn_or_key):
            # @on_change (bare decorator)
            self._global_listeners.append(fn_or_key)
            return fn_or_key
        elif isinstance(fn_or_key, str):
            # @on_change("key")
            key = fn_or_key

            def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
                self._key_listeners.setdefault(key, []).append(fn)
                return fn

            return decorator
        else:
            # @on_change() — called with parens but no args

            def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
                self._global_listeners.append(fn)
                return fn

            return decorator

    async def refresh(self) -> None:
        """Re-fetch all loggers and groups and fire listener events for any deltas.

        Requires :meth:`install` first; raises :class:`NotInstalledError`
        otherwise.
        """
        self._require_installed()
        debug("resolution", "refresh() called, triggering full resolution pass")
        pre = self._snapshot_effective_levels()
        await self._fetch_cache(trigger="refresh()")
        self._apply_deltas_and_fire(pre, "manual")

    # --- Internal: event handlers (called by SharedWebSocket) ---

    def _handle_logger_changed(self, data: dict) -> None:
        key = data.get("id", "")
        debug("websocket", f"logger_changed: fetching logger {key!r}")
        pre = self._snapshot_effective_levels()
        self._run_ws_handler(self._fetch_logger_and_apply, key, pre)

    def _handle_logger_deleted(self, data: dict) -> None:
        key = data.get("id", "")
        debug("websocket", f"logger_deleted: removing logger {key!r}")
        pre = self._snapshot_effective_levels()
        self._loggers_cache.pop(key, None)
        # Apply + fire on the worker thread so the WS dispatch returns quickly.
        import asyncio as _asyncio

        def _run() -> None:
            try:
                _asyncio.run(self._async_apply_deltas_and_fire(pre, "websocket"))
            except Exception as exc:
                logger.warning("Failed to apply levels after logger_deleted event: %s", exc)

        threading.Thread(target=_run, name="smplkit-logging-ws-deleted", daemon=True).start()

    def _handle_group_changed(self, data: dict) -> None:
        key = data.get("id", "")
        debug("websocket", f"group_changed: fetching group {key!r}")
        pre = self._snapshot_effective_levels()
        self._run_ws_handler(self._fetch_group_and_apply, key, pre)

    def _handle_group_deleted(self, data: dict) -> None:
        key = data.get("id", "")
        debug("websocket", f"group_deleted: removing group {key!r}")
        pre = self._snapshot_effective_levels()
        self._groups_cache.pop(key, None)
        import asyncio as _asyncio

        def _run() -> None:
            try:
                _asyncio.run(self._async_apply_deltas_and_fire(pre, "websocket"))
            except Exception as exc:
                logger.warning("Failed to apply levels after group_deleted event: %s", exc)

        threading.Thread(target=_run, name="smplkit-logging-ws-deleted", daemon=True).start()

    def _handle_loggers_changed(self, data: dict) -> None:
        debug("websocket", "loggers_changed: full re-fetch")
        api_key = self._standalone_api_key if self._parent is None else self._parent._api_key
        logging_base_url = self._logging_base_url
        pre = self._snapshot_effective_levels()

        async def _do_refresh() -> None:
            http = AuthenticatedClient(base_url=logging_base_url, token=api_key)
            try:
                await self._fetch_cache(trigger="loggers_changed WS event", http_client=http)
            finally:
                ac = http._async_client
                if ac is not None:
                    await ac.aclose()
            self._apply_deltas_and_fire(pre, "websocket")

        import asyncio as _asyncio

        def _run() -> None:
            try:
                _asyncio.run(_do_refresh())
            except Exception as exc:
                logger.warning("Failed to re-fetch/apply logging levels after loggers_changed event: %s", exc)
                debug("websocket", traceback.format_exc().strip())

        threading.Thread(target=_run, name="smplkit-logging-ws-refresh", daemon=True).start()

    def _run_ws_handler(self, coro_fn: Any, key: str, pre: dict[str, str]) -> None:
        """Run an async handler in a fresh event loop (WS thread pattern).

        ``pre`` is the effective-level snapshot taken on the main thread
        before this handler kicks off any mutation; the worker uses it as
        the baseline for the post-update apply + fire pass.
        """
        api_key = self._standalone_api_key if self._parent is None else self._parent._api_key
        logging_base_url = self._logging_base_url
        import asyncio as _asyncio

        async def _run_async() -> None:
            http = AuthenticatedClient(base_url=logging_base_url, token=api_key)
            try:
                await coro_fn(key, http, pre)
            finally:
                ac = http._async_client
                if ac is not None:
                    await ac.aclose()

        def _run() -> None:
            try:
                _asyncio.run(_run_async())
            except Exception as exc:
                logger.warning("Failed to handle WS event for %r: %s", key, exc)
                debug("websocket", traceback.format_exc().strip())

        threading.Thread(target=_run, name="smplkit-logging-ws-handler", daemon=True).start()

    async def _fetch_logger_and_apply(self, key: str, http: AuthenticatedClient, pre: dict[str, str]) -> None:
        try:
            response = await get_logger.asyncio_detailed(key, client=http)
            _check_response_status(response.status_code, response.content)
        except Exception as exc:
            logger.warning("Failed to fetch logger %r after WS event: %s", key, exc)
            return
        if isinstance(response.parsed, LoggerResponse):
            r = response.parsed.data
            attrs = r.attributes
            lid = _unset_to_none(r.id) or key
            self._loggers_cache[lid] = {
                "level": _unset_to_none(attrs.level),
                "group": _unset_to_none(attrs.group),
                "managed": _unset_to_none(attrs.managed),
                "environments": _extract_environments(attrs.environments),
            }
        self._apply_deltas_and_fire(pre, "websocket")

    async def _fetch_group_and_apply(self, key: str, http: AuthenticatedClient, pre: dict[str, str]) -> None:
        try:
            response = await get_log_group.asyncio_detailed(key, client=http)
            _check_response_status(response.status_code, response.content)
        except Exception as exc:
            logger.warning("Failed to fetch log group %r after WS event: %s", key, exc)
            return
        if isinstance(response.parsed, LogGroupResponse):
            r = response.parsed.data
            attrs = r.attributes
            gid = _unset_to_none(r.id) or key
            self._groups_cache[gid] = {
                "level": _unset_to_none(attrs.level),
                "group": _unset_to_none(attrs.parent_id),
                "environments": _extract_environments(attrs.environments),
            }
        self._apply_deltas_and_fire(pre, "websocket")

    async def _async_apply_deltas_and_fire(self, pre: dict[str, str], source: str) -> None:
        self._apply_deltas_and_fire(pre, source)

    def _snapshot_effective_levels(self) -> dict[str, str]:
        """Effective level for every locally-tracked managed logger.

        This is the universe of loggers the adapter applies levels to —
        the only loggers whose listener can fire. A logger not in
        ``_name_map`` (never instantiated locally) or marked
        ``managed=False`` in the cache is excluded.
        """
        snapshot: dict[str, str] = {}
        for normalized_id in self._name_map.values():
            entry = self._loggers_cache.get(normalized_id)
            if entry is None or not entry.get("managed"):
                continue
            snapshot[normalized_id] = resolve_level(
                normalized_id, self._environment, self._loggers_cache, self._groups_cache
            )
        return snapshot

    def _apply_deltas_and_fire(self, pre: dict[str, str], source: str) -> None:
        """Apply + fire per-logger whenever the effective level moved.

        See :meth:`LoggingClient._apply_deltas_and_fire` for full semantics.
        """
        for original_name, normalized_id in self._name_map.items():
            entry = self._loggers_cache.get(normalized_id)
            if entry is None or not entry.get("managed"):
                continue
            new = resolve_level(normalized_id, self._environment, self._loggers_cache, self._groups_cache)
            if pre.get(normalized_id) == new:
                continue
            python_level = smpl_level_to_python(new)
            for adapter in self._adapters:
                try:
                    adapter.apply_level(original_name, python_level)
                except Exception:
                    logger.warning("Adapter %s apply_level() failed for %s", adapter.name, original_name, exc_info=True)
            metrics = self._metrics
            if metrics is not None:
                metrics.record("logging.level_changes", unit="changes", dimensions={"logger": normalized_id})
            self._fire_for_logger(normalized_id, new, source)

    def _fire_for_logger(self, logger_id: str, level: str, source: str) -> None:
        """Fire one :class:`LoggerChangeEvent` to every matching subscriber."""
        event = LoggerChangeEvent(id=logger_id, level=level, source=source)
        for cb in self._global_listeners:
            try:
                cb(event)
            except Exception:
                logger.error("Exception in global logging on_change listener", exc_info=True)
        for cb in self._key_listeners.get(logger_id, []):
            try:
                cb(event)
            except Exception:
                logger.error("Exception in key-scoped logging on_change listener", exc_info=True)

    # --- Internal ---

    def _loggersource_for(self, name: str, explicit_level: int | None, effective_level: int) -> LoggerSource:
        """Build a LoggerSource from an adapter's (name, explicit, effective) discovery tuple."""
        from smplkit import LogLevel

        return LoggerSource(
            name=name,
            resolved_level=LogLevel(python_level_to_smpl(effective_level)),
            level=LogLevel(python_level_to_smpl(explicit_level)) if explicit_level is not None else None,
            service=self._service,
            environment=self._environment,
        )

    def _on_new_logger(self, name: str, explicit_level: int | None, effective_level: int) -> None:
        """Callback from adapters when a new logger is created."""
        normalized = normalize_logger_name(name)
        debug("discovery", f"new logger intercepted via callback: {name!r} (normalized: {normalized!r})")
        self._name_map[name] = normalized
        self.loggers.register(self._loggersource_for(name, explicit_level, effective_level))
        debug(
            "registration",
            f"queued {name!r} for bulk registration (buffer size: {self.loggers.pending_count})",
        )

        if self._connected and normalized in self._loggers_cache:
            entry = self._loggers_cache[normalized]
            if entry.get("managed"):
                debug("resolution", f"applying immediate level for newly discovered managed logger {name!r}")
                resolved = resolve_level(normalized, self._environment, self._loggers_cache, self._groups_cache)
                python_level = smpl_level_to_python(resolved)
                for adapter in self._adapters:
                    try:
                        adapter.apply_level(name, python_level)
                    except Exception:
                        logger.warning("Adapter %s apply_level() failed for %s", adapter.name, name, exc_info=True)

    async def _flush_bulk_async(self) -> None:
        """Flush the registration buffer (delegates to the loggers sub-client)."""
        try:
            await self.loggers.flush()
        except Exception as exc:
            status = getattr(exc, "status_code", None)
            if status is not None:
                logger.warning("Bulk logger registration failed: HTTP %s: %s", status, exc)
            else:
                logger.warning("Bulk logger registration failed (logging: %s): %s", self._logging_base_url, exc)
            debug("registration", traceback.format_exc().strip())

    async def _fetch_cache(self, trigger: str, http_client: AuthenticatedClient | None = None) -> None:
        """Re-fetch loggers/groups into the cache (no apply, no fire).

        ``http_client``, when supplied, is used instead of ``self._logging_http``.
        Pass a fresh client when calling from a temporary event loop (e.g. the
        WS-event refresh thread) to prevent cross-loop httpx transport reuse.
        """
        http = http_client if http_client is not None else self._logging_http
        debug("resolution", f"full resolution pass starting (trigger: {trigger})")

        async def fetch_loggers_page(page_number: int, page_size: int) -> list[tuple[str, dict[str, Any]]]:
            debug("api", f"GET /api/v1/loggers (page {page_number})")
            try:
                response = await list_loggers.asyncio_detailed(
                    client=http,
                    pagenumber=page_number,
                    pagesize=page_size,
                )
                _check_response_status(response.status_code, response.content)
            except Exception as exc:
                _maybe_reraise_network_error(exc, http._base_url)
                raise
            page_rows: list[tuple[str, dict[str, Any]]] = []
            if response.parsed is not None and hasattr(response.parsed, "data"):
                for r in response.parsed.data:
                    attrs = r.attributes
                    lid = _unset_to_none(r.id) or ""
                    page_rows.append(
                        (
                            lid,
                            {
                                "level": _unset_to_none(attrs.level),
                                "group": _unset_to_none(attrs.group),
                                "managed": _unset_to_none(attrs.managed),
                                "environments": _extract_environments(attrs.environments),
                            },
                        )
                    )
            debug(
                "api",
                f"GET /api/v1/loggers page {page_number} -> {response.status_code.value} ({len(page_rows)} loggers)",
            )
            return page_rows

        loggers_data: dict[str, dict[str, Any]] = dict(await paginate_async(fetch_loggers_page))

        async def fetch_groups_page(page_number: int, page_size: int) -> list[tuple[str, dict[str, Any]]]:
            debug("api", f"GET /api/v1/log-groups (page {page_number})")
            try:
                grp_response = await list_log_groups.asyncio_detailed(
                    client=http,
                    pagenumber=page_number,
                    pagesize=page_size,
                )
                _check_response_status(grp_response.status_code, grp_response.content)
            except Exception as exc:
                _maybe_reraise_network_error(exc, http._base_url)
                raise
            page_rows: list[tuple[str, dict[str, Any]]] = []
            if grp_response.parsed is not None and hasattr(grp_response.parsed, "data"):
                for r in grp_response.parsed.data:
                    attrs = r.attributes
                    gid = _unset_to_none(r.id) or ""
                    page_rows.append(
                        (
                            gid,
                            {
                                "level": _unset_to_none(attrs.level),
                                "group": _unset_to_none(attrs.parent_id),
                                "environments": _extract_environments(attrs.environments),
                            },
                        )
                    )
            debug(
                "api",
                f"GET /api/v1/log-groups page {page_number} -> {grp_response.status_code.value} ({len(page_rows)} groups)",
            )
            return page_rows

        groups_data: dict[str, dict[str, Any]] = dict(await paginate_async(fetch_groups_page))

        self._loggers_cache = loggers_data
        self._groups_cache = groups_data

    async def _fetch_and_apply(self, trigger: str = "unknown", http_client: AuthenticatedClient | None = None) -> None:
        """Fetch loggers/groups and unconditionally apply levels (initial install path).

        Silent — does not fire change-listener events. Use the
        :meth:`_apply_deltas_and_fire` path from WS handlers / :meth:`refresh`
        to get per-logger fanout.
        """
        await self._fetch_cache(trigger, http_client=http_client)
        self._apply_levels()

    def _apply_levels(self) -> None:
        """Apply resolved levels to all managed, locally-present loggers."""
        debug("resolution", f"running full resolution pass for {len(self._name_map)} local loggers")
        for original_name, normalized_id in self._name_map.items():
            entry = self._loggers_cache.get(normalized_id)
            if entry is None:
                continue
            if not entry.get("managed"):
                continue
            resolved = resolve_level(normalized_id, self._environment, self._loggers_cache, self._groups_cache)
            python_level = smpl_level_to_python(resolved)
            for adapter in self._adapters:
                try:
                    adapter.apply_level(original_name, python_level)
                except Exception:
                    logger.warning("Adapter %s apply_level() failed for %s", adapter.name, original_name, exc_info=True)
            metrics = self._metrics
            if metrics is not None:
                metrics.record("logging.level_changes", unit="changes", dimensions={"logger": normalized_id})

    async def aclose(self) -> None:
        """Release async resources — only those this client owns.

        Uninstalls adapter hooks, unsubscribes from the WebSocket, tears down
        the owned WebSocket (standalone install) and the owned async logging +
        app HTTP transports (standalone construction). A wired client borrows
        the parent's transport and WebSocket and closes neither.
        """
        # Adapter hooks, WS subscription, owned sync clients + WS shutdown.
        self._close()
        if self._owns_transport:
            ac = self._logging_http._async_client
            if ac is not None:
                await ac.aclose()
                self._logging_http._async_client = None
            app_ac = self._app_http_standalone._async_client
            if app_ac is not None:
                await app_ac.aclose()
                self._app_http_standalone._async_client = None

    async def __aenter__(self) -> AsyncLoggingClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()
