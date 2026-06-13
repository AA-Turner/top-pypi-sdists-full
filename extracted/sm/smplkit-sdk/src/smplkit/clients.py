"""Top-level SDK clients — SmplClient (sync) and AsyncSmplClient (async)."""

from __future__ import annotations

import asyncio
import logging
import threading
import time
import traceback
from typing import TYPE_CHECKING

from smplkit._config import _service_url, resolve_config
from smplkit.context import ContextScope, set_context as _set_context
from smplkit.errors import TimeoutError
from smplkit._debug import debug, enable_debug
from smplkit._generated.app.api.contexts import bulk_register_contexts as gen_bulk_register_contexts
from smplkit._generated.app.models.context_bulk_item import ContextBulkItem
from smplkit._generated.app.models.context_bulk_item_attributes import ContextBulkItemAttributes
from smplkit._generated.app.models.context_bulk_register import ContextBulkRegister
from smplkit._metrics import _AsyncMetricsReporter, _MetricsReporter
from smplkit._transport import _to_transport_config, build_service_transports
from smplkit._ws import SharedWebSocket
from smplkit.account.clients import AccountClient, AsyncAccountClient
from smplkit.audit.clients import AsyncAuditClient, AuditClient
from smplkit.jobs.clients import AsyncJobsClient, JobsClient
from smplkit.config.clients import AsyncConfigClient, ConfigClient
from smplkit.flags.clients import AsyncFlagsClient, FlagsClient
from smplkit.logging.clients import AsyncLoggingClient, LoggingClient
from smplkit.platform.clients import AsyncPlatformClient, PlatformClient

if TYPE_CHECKING:
    from smplkit.flags.types import Context

logger = logging.getLogger("smplkit")

# Periodic flush of all sub-client registration buffers (contexts, flags,
# loggers).  Threshold flushes still fire immediately when buffers fill up;
# this timer is the liveness guarantee for the tail.
_PERIODIC_FLUSH_INTERVAL = 60.0  # seconds


class SmplClient:
    """Synchronous entry point for the smplkit SDK.

    Usage::

        from smplkit import SmplClient

        with SmplClient(environment="production", service="my-svc") as client:
            checkout_v2 = client.flags.boolean_flag("checkout-v2", default=False)
            if checkout_v2.get(): ...

    All parameters are optional. When omitted, the SDK resolves each one in
    precedence order, lowest to highest: built-in defaults, then the
    ``~/.smplkit`` configuration file, then ``SMPLKIT_*`` environment
    variables, then the explicit constructor arguments below (a value
    supplied at a higher level overrides the lower ones).

    Args:
        api_key: API key for authenticating with the smplkit platform.
        environment: The environment to connect to (e.g. ``"production"``).
        service: Service name (e.g. ``"user-service"``).
        profile: Named profile section to read from ``~/.smplkit``.
        base_domain: Base domain for API requests (default ``"smplkit.com"``).
        scheme: URL scheme (default ``"https"``).
        debug: Enable debug logging in the SDK.
        telemetry: Enable anonymous usage telemetry (default ``True``).
        extra_headers: Extra HTTP headers attached to every request the
            client sends.
    """

    platform: PlatformClient
    account: AccountClient
    config: ConfigClient
    flags: FlagsClient
    logging: LoggingClient
    audit: AuditClient
    jobs: JobsClient

    def __init__(
        self,
        api_key: str | None = None,
        *,
        environment: str | None = None,
        service: str | None = None,
        profile: str | None = None,
        base_domain: str | None = None,
        scheme: str | None = None,
        debug: bool | None = None,
        telemetry: bool | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        cfg = resolve_config(
            profile=profile,
            api_key=api_key,
            base_domain=base_domain,
            scheme=scheme,
            environment=environment,
            service=service,
            debug=debug,
            telemetry=telemetry,
        )
        if cfg.debug:
            enable_debug()

        self._api_key = cfg.api_key
        self._environment = cfg.environment
        self._service = cfg.service
        self._base_domain = cfg.base_domain
        self._scheme = cfg.scheme
        self._extra_headers = extra_headers

        if cfg.debug:
            logger.setLevel(logging.DEBUG)

        masked_key = cfg.api_key[:10] + "..." if len(cfg.api_key) > 10 else cfg.api_key
        _debug(
            "lifecycle",
            f"SmplClient init: api_key={masked_key}"
            f" env={cfg.environment!r} service={cfg.service!r}"
            f" base_domain={cfg.base_domain!r} scheme={cfg.scheme!r}"
            f" debug={cfg.debug} telemetry={cfg.telemetry}",
        )

        # Build the per-service HTTP transports + the context-registration
        # buffer. Side-effect-free: each transport connects lazily on first
        # call. client.platform owns the buffer; client.config/flags/logging/
        # jobs borrow their transports from here.
        self._transports = build_service_transports(_to_transport_config(cfg, extra_headers))

        app_url = self._transports.app_url
        audit_url = _service_url(cfg.scheme, "audit", cfg.base_domain)

        # Alias the shared HTTP transports — single connection pool per service.
        self._http_client = self._transports.config_http
        self._app_http = self._transports.app_http
        self._app_base_url = app_url

        # Metrics reporter
        if cfg.telemetry:
            self._metrics: _MetricsReporter | None = _MetricsReporter(
                http_client=self._app_http,
                environment=cfg.environment,
                service=cfg.service,
            )
        else:
            self._metrics = None

        self._ws_manager: SharedWebSocket | None = None
        # Platform's cross-cutting CRUD on one client; wired into this parent
        # so it borrows the shared app transport, and owns the
        # context-registration buffer. Built BEFORE flags so the contexts
        # seam below is available.
        self.platform = PlatformClient(app_transport=self._app_http)
        # Account-level settings on one client; built from the app url + api
        # key (the settings sub-client uses httpx directly).
        self.account = AccountClient(api_key=cfg.api_key, base_url=app_url, extra_headers=extra_headers)
        # Config's full surface on one client; wired into this parent so it
        # borrows the shared config transport and WebSocket.
        self.config = ConfigClient(parent=self, transport=self._transports.config_http, metrics=self._metrics)
        # Flags' full surface on one client; wired into this parent so it
        # borrows the shared flags transport and WebSocket. ``contexts`` is the
        # injection seam for evaluation-context registration, wired to
        # ``client.platform.contexts``.
        self.flags = FlagsClient(
            parent=self,
            transport=self._transports.flags_http,
            contexts=self.platform.contexts,
            metrics=self._metrics,
        )
        # Logging's full surface on one client; wired into this parent so it
        # borrows the shared logging transport and WebSocket. The two
        # management sub-clients live at client.logging.loggers /
        # client.logging.log_groups.
        self.logging = LoggingClient(
            parent=self,
            transport=self._transports.logging_http,
            metrics=self._metrics,
        )
        # Audit's full surface on one client; this runtime instance carries
        # the configured environment as ``X-Smplkit-Environment`` and owns its
        # own transport (closed in ``close()``).
        self.audit = AuditClient(
            api_key=cfg.api_key,
            base_url=audit_url,
            environment=cfg.environment,
            extra_headers=extra_headers,
        )
        # Jobs has no runtime/management split — reuse the shared jobs
        # transport (single connection pool) so ``client.jobs`` is one-stop.
        self.jobs = JobsClient(auth_client=self._transports.jobs_http)

        # Construction is side-effect-free: no background threads, no
        # phone-home. The periodic registration-buffer flush and the
        # service-context registration are deferred until the first
        # config/flags/logging operation or set_context via
        # ``_ensure_started`` — so an audit-only or jobs-only customer pays
        # zero threads and zero network at construction.
        self._closed = False
        self._started = False
        self._start_lock = threading.Lock()
        self._flush_timer: threading.Timer | None = None
        self._init_thread: threading.Thread | None = None

    def _ensure_started(self) -> None:
        """Start the deferred background machinery exactly once.

        Idempotent and thread-safe (lock + flag, mirroring
        ``_MetricsReporter._maybe_start_timer``); a no-op after ``close()``.
        Triggered by the first config/flags/logging operation, ``set_context``,
        ``wait_until_ready``, or WebSocket open — never at construction.
        """
        with self._start_lock:
            if self._started or self._closed:
                return
            self._started = True
        self._schedule_periodic_flush()
        self._init_thread = threading.Thread(target=self._register_service_context, daemon=True)
        self._init_thread.start()

    def _schedule_periodic_flush(self) -> None:
        """Tick the periodic registration-buffer flush.  Self-rescheduling."""

        def _tick() -> None:
            if self._closed:
                return
            try:
                self.platform.contexts.flush()
                self.flags.flush()
                self.logging.loggers.flush()
                self.config.flush()
            except Exception as exc:
                logger.warning("Periodic registration flush failed: %s", exc)
                debug("registration", traceback.format_exc().strip())
            if not self._closed:
                self._schedule_periodic_flush()

        self._flush_timer = threading.Timer(_PERIODIC_FLUSH_INTERVAL, _tick)
        self._flush_timer.daemon = True
        self._flush_timer.start()

    def _final_flush(self) -> None:
        """Drain every registration buffer one last time on close."""
        for fn in (
            self.platform.contexts.flush,
            self.flags.flush,
            self.logging.loggers.flush,
            self.config.flush,
        ):
            try:
                fn()
            except Exception as exc:
                logger.warning("Final registration flush failed: %s", exc)
                debug("registration", traceback.format_exc().strip())

    def _register_service_context(self) -> None:
        """Register the environment and/or service as context instances.

        Only the values that are set are registered; if neither environment
        nor service was provided the POST is skipped entirely (an audit/jobs-only
        customer has nothing to register)."""
        try:
            items: list[ContextBulkItem] = []
            if self._environment is not None:
                items.append(ContextBulkItem(type_="environment", key=self._environment))
            if self._service is not None:
                svc_attrs = ContextBulkItemAttributes()
                svc_attrs.additional_properties = {"name": self._service}
                items.append(ContextBulkItem(type_="service", key=self._service, attributes=svc_attrs))
            if not items:
                return
            body = ContextBulkRegister(contexts=items)
            gen_bulk_register_contexts.sync_detailed(client=self._app_http, body=body)
        except Exception as exc:
            logger.warning("Failed to register service context (app: %s): %s", self._app_base_url, exc)
            debug("lifecycle", traceback.format_exc().strip())

    def _ensure_ws(self) -> SharedWebSocket:
        """Lazily create and start the shared WebSocket."""
        self._ensure_started()
        if self._ws_manager is None:
            self._ws_manager = SharedWebSocket(
                app_base_url=self._app_base_url,
                api_key=self._api_key,
                metrics=self._metrics,
            )
            self._ws_manager.start()
        return self._ws_manager

    def wait_until_ready(self, timeout: float = 10.0) -> None:
        """Optionally pre-warm the SDK and block until the live socket is up.

        Eagerly connects config and flags — flushing discovery, pre-fetching
        all flags and configs into the local cache, opening the live-updates
        WebSocket — and waits for the handshake to complete. After this
        returns, ``flag.get()`` / ``client.config.subscribe()`` hit cache (no
        first-request connect tax) and any ``on_change`` listeners receive
        every server event from this point forward.

        Optional: config and flags connect lazily on first live use, so this
        is purely a pre-warm / WebSocket-ready barrier. Logging integration is
        *not* connected here — call ``client.logging.install()`` separately if
        you want it (it installs adapters and hooks into your application's
        logger, which should be opt-in).

        Args:
            timeout: Maximum seconds to wait for the live-updates WebSocket
                handshake before giving up. Defaults to ``10.0``.

        Raises:
            TimeoutError: If the WebSocket fails to connect within *timeout* seconds.
        """
        self.flags._ensure_connected()
        self.config._ensure_connected()
        ws = self._ensure_ws()
        deadline = time.monotonic() + timeout
        while ws.connection_status != "connected":
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"Live-updates websocket did not connect within {timeout}s (status: {ws.connection_status!r})"
                )
            time.sleep(0.05)

    def set_context(self, contexts: list[Context]) -> ContextScope:
        """Stash *contexts* as the current request's evaluation context.

        Typical use is from middleware — set the context once at request entry
        and every ``flag.get()`` (and other context-sensitive evaluations) inside
        that request automatically picks it up.  ``contextvars`` provides per-task
        / per-thread isolation so concurrent requests don't cross-contaminate.

        Each unique ``(type, key)`` is also registered with the platform
        (deduplicated via an LRU; sent in the background).

        Two usage shapes::

            # Fire-and-forget (typical middleware)
            client.set_context([Context("user", ...), Context("account", ...)])

            # Scoped block (e.g. impersonation or one-off override)
            with client.set_context([Context("user", "impersonated")]):
                ...
            # original context restored here

        Args:
            contexts: The contexts to make active for the current task/thread
                (e.g. the request's user and account). An empty list clears
                any registration step but still returns a scope.

        Returns:
            A ``ContextScope`` you can ignore for fire-and-forget use, or
            enter as a ``with`` block to restore the previous context on exit.
        """
        self._ensure_started()
        if contexts:
            self.platform.contexts.register(contexts)
        return _set_context(contexts)

    def close(self) -> None:
        """Release all resources held by this client."""
        _debug("lifecycle", "SmplClient.close() called")
        self._closed = True
        if self._flush_timer is not None:
            self._flush_timer.cancel()
            self._flush_timer = None
        self._final_flush()
        if self._metrics is not None:
            self._metrics.close()
        self.logging._close()
        self.flags._close()
        self.audit._close()
        if self._ws_manager is not None:
            self._ws_manager.stop()
            self._ws_manager = None
        # Close the shared per-service HTTP transports (app/config/flags/
        # logging/jobs). client.platform/account borrow the app transport and
        # close nothing; client.audit owns and closed its own transport above.
        self._transports.close()

    def __enter__(self) -> SmplClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncSmplClient:
    """Asynchronous entry point for the smplkit SDK.

    Usage::

        from smplkit import AsyncSmplClient

        async with AsyncSmplClient(environment="production", service="my-svc") as client:
            checkout_v2 = client.flags.boolean_flag("checkout-v2", default=False)
            if checkout_v2.get(): ...

    All parameters are optional. When omitted, the SDK resolves each one in
    precedence order, lowest to highest: built-in defaults, then the
    ``~/.smplkit`` configuration file, then ``SMPLKIT_*`` environment
    variables, then the explicit constructor arguments below (a value
    supplied at a higher level overrides the lower ones).

    Args:
        api_key: API key for authenticating with the smplkit platform.
        environment: The environment to connect to (e.g. ``"production"``).
        service: Service name (e.g. ``"user-service"``).
        profile: Named profile section to read from ``~/.smplkit``.
        base_domain: Base domain for API requests (default ``"smplkit.com"``).
        scheme: URL scheme (default ``"https"``).
        debug: Enable debug logging in the SDK.
        telemetry: Enable anonymous usage telemetry (default ``True``).
        extra_headers: Extra HTTP headers attached to every request the
            client sends.
    """

    platform: AsyncPlatformClient
    account: AsyncAccountClient
    config: AsyncConfigClient
    flags: AsyncFlagsClient
    logging: AsyncLoggingClient
    audit: AsyncAuditClient
    jobs: AsyncJobsClient

    def __init__(
        self,
        api_key: str | None = None,
        *,
        environment: str | None = None,
        service: str | None = None,
        profile: str | None = None,
        base_domain: str | None = None,
        scheme: str | None = None,
        debug: bool | None = None,
        telemetry: bool | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        cfg = resolve_config(
            profile=profile,
            api_key=api_key,
            base_domain=base_domain,
            scheme=scheme,
            environment=environment,
            service=service,
            debug=debug,
            telemetry=telemetry,
        )
        if cfg.debug:
            enable_debug()

        self._api_key = cfg.api_key
        self._environment = cfg.environment
        self._service = cfg.service
        self._base_domain = cfg.base_domain
        self._scheme = cfg.scheme
        self._extra_headers = extra_headers

        if cfg.debug:
            logger.setLevel(logging.DEBUG)

        masked_key = cfg.api_key[:10] + "..." if len(cfg.api_key) > 10 else cfg.api_key
        _debug(
            "lifecycle",
            f"AsyncSmplClient init: api_key={masked_key}"
            f" env={cfg.environment!r} service={cfg.service!r}"
            f" base_domain={cfg.base_domain!r} scheme={cfg.scheme!r}"
            f" debug={cfg.debug} telemetry={cfg.telemetry}",
        )

        # Build the per-service HTTP transports + context-registration buffer.
        # Side-effect-free; client.platform owns the buffer, the product
        # clients borrow their transports from here.
        self._transports = build_service_transports(_to_transport_config(cfg, extra_headers))

        app_url = self._transports.app_url
        audit_url = _service_url(cfg.scheme, "audit", cfg.base_domain)

        self._http_client = self._transports.config_http
        self._app_http = self._transports.app_http
        self._app_base_url = app_url

        # Metrics reporter
        if cfg.telemetry:
            self._metrics: _AsyncMetricsReporter | None = _AsyncMetricsReporter(
                http_client=self._app_http,
                environment=cfg.environment,
                service=cfg.service,
            )
        else:
            self._metrics = None

        self._ws_manager: SharedWebSocket | None = None
        # Platform's cross-cutting CRUD on one client; wired into this parent
        # so it borrows the shared app transport and owns the
        # context-registration buffer. Built BEFORE flags so the contexts seam
        # below is available.
        self.platform = AsyncPlatformClient(app_transport=self._app_http)
        # Account-level settings; built from the app url + api key.
        self.account = AsyncAccountClient(api_key=cfg.api_key, base_url=app_url, extra_headers=extra_headers)
        # Config's full surface on one client; wired into this parent so it
        # borrows the shared config transport and WebSocket.
        self.config = AsyncConfigClient(parent=self, transport=self._transports.config_http, metrics=self._metrics)
        # Flags' full surface on one client; wired into this parent so it
        # borrows the shared flags transport and WebSocket. ``contexts`` is the
        # injection seam for evaluation-context registration, wired to
        # ``client.platform.contexts``.
        self.flags = AsyncFlagsClient(
            parent=self,
            transport=self._transports.flags_http,
            contexts=self.platform.contexts,
            metrics=self._metrics,
        )
        # Logging's full surface on one client; wired into this parent so it
        # borrows the shared logging transport and WebSocket. The two
        # management sub-clients live at client.logging.loggers /
        # client.logging.log_groups.
        self.logging = AsyncLoggingClient(
            parent=self,
            transport=self._transports.logging_http,
            metrics=self._metrics,
        )
        self.audit = AsyncAuditClient(
            api_key=cfg.api_key,
            base_url=audit_url,
            environment=cfg.environment,
            extra_headers=extra_headers,
        )
        # Jobs has no runtime/management split — reuse the shared jobs
        # transport (single connection pool) so ``client.jobs`` is one-stop.
        self.jobs = AsyncJobsClient(auth_client=self._transports.jobs_http)

        # Construction is side-effect-free (see SmplClient): the flush timer
        # and service-context phone-home are deferred to ``_ensure_started``,
        # triggered by the first config/flags/logging op or set_context.
        self._closed = False
        self._started = False
        self._start_lock = threading.Lock()
        self._flush_timer: threading.Timer | None = None
        self._init_thread: threading.Thread | None = None

    def _ensure_started(self) -> None:
        """Start the deferred background machinery exactly once (idempotent,
        no-op after close). The registration runs on a sync daemon thread, so
        there is no event-loop dependency at trigger time."""
        with self._start_lock:
            if self._started or self._closed:
                return
            self._started = True
        self._schedule_periodic_flush()
        self._init_thread = threading.Thread(target=self._register_service_context_sync, daemon=True)
        self._init_thread.start()

    def _schedule_periodic_flush(self) -> None:
        """Tick the periodic registration-buffer flush.  Self-rescheduling.

        Runs on a daemon thread; calls the sync flush variants on each
        sub-client so we don't block waiting for an event loop.
        """

        def _tick() -> None:
            if self._closed:
                return
            for fn in (
                self.platform.contexts.flush_sync,
                self.flags.flush_sync,
                self.logging.loggers.flush_sync,
                self.config.flush_sync,
            ):
                try:
                    fn()
                except Exception as exc:
                    logger.warning("Periodic registration flush failed: %s", exc)
                    debug("registration", traceback.format_exc().strip())
            if not self._closed:
                self._schedule_periodic_flush()

        self._flush_timer = threading.Timer(_PERIODIC_FLUSH_INTERVAL, _tick)
        self._flush_timer.daemon = True
        self._flush_timer.start()

    async def _final_flush(self) -> None:
        """Drain every registration buffer one last time on close."""
        for fn in (
            self.platform.contexts.flush,
            self.flags.flush,
            self.logging.loggers.flush,
            self.config.flush,
        ):
            try:
                await fn()
            except Exception as exc:
                logger.warning("Final registration flush failed: %s", exc)
                debug("registration", traceback.format_exc().strip())

    def _register_service_context_sync(self) -> None:
        """Sync wrapper for context registration (runs in background thread)."""
        try:
            items: list[ContextBulkItem] = []
            if self._environment is not None:
                items.append(ContextBulkItem(type_="environment", key=self._environment))
            if self._service is not None:
                svc_attrs = ContextBulkItemAttributes()
                svc_attrs.additional_properties = {"name": self._service}
                items.append(ContextBulkItem(type_="service", key=self._service, attributes=svc_attrs))
            if not items:
                return
            body = ContextBulkRegister(contexts=items)
            gen_bulk_register_contexts.sync_detailed(client=self._app_http, body=body)
        except Exception as exc:
            logger.warning("Failed to register service context (app: %s): %s", self._app_base_url, exc)
            debug("lifecycle", traceback.format_exc().strip())

    async def _register_service_context(self) -> None:
        """Register the environment and service as context instances on the app service."""
        try:
            items: list[ContextBulkItem] = []
            if self._environment is not None:
                items.append(ContextBulkItem(type_="environment", key=self._environment))
            if self._service is not None:
                svc_attrs = ContextBulkItemAttributes()
                svc_attrs.additional_properties = {"name": self._service}
                items.append(ContextBulkItem(type_="service", key=self._service, attributes=svc_attrs))
            if not items:
                return
            body = ContextBulkRegister(contexts=items)
            await gen_bulk_register_contexts.asyncio_detailed(client=self._app_http, body=body)
        except Exception as exc:
            logger.warning("Failed to register service context (app: %s): %s", self._app_base_url, exc)
            debug("lifecycle", traceback.format_exc().strip())

    def _ensure_ws(self) -> SharedWebSocket:
        """Lazily create and start the shared WebSocket."""
        self._ensure_started()
        if self._ws_manager is None:
            self._ws_manager = SharedWebSocket(
                app_base_url=self._app_base_url,
                api_key=self._api_key,
                metrics=self._metrics,
            )
            self._ws_manager.start()
        return self._ws_manager

    async def wait_until_ready(self, timeout: float = 10.0) -> None:
        """Optionally pre-warm the SDK and wait until the live socket is up.

        Eagerly connects config and flags — flushing discovery, pre-fetching
        all flags and configs into the local cache, opening the live-updates
        WebSocket — and waits for the handshake to complete. After this
        returns, ``flag.get()`` / ``client.config.subscribe()`` hit cache (no
        first-request connect tax) and any ``on_change`` listeners receive
        every server event from this point forward.

        Optional: config and flags connect lazily on first live use, so this
        is purely a pre-warm / WebSocket-ready barrier. Logging integration is
        *not* connected here — call ``await client.logging.install()``
        separately if you want it (it installs adapters and hooks into your
        application's logger, which should be opt-in).

        Args:
            timeout: Maximum seconds to wait for the live-updates WebSocket
                handshake before giving up. Defaults to ``10.0``.

        Raises:
            TimeoutError: If the WebSocket fails to connect within *timeout* seconds.
        """
        await self.flags._ensure_connected()
        await self.config._ensure_connected()
        ws = self._ensure_ws()
        deadline = time.monotonic() + timeout
        while ws.connection_status != "connected":
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"Live-updates websocket did not connect within {timeout}s (status: {ws.connection_status!r})"
                )
            await asyncio.sleep(0.05)

    def set_context(self, contexts: list[Context]) -> ContextScope:
        """Stash *contexts* as the current request's evaluation context.

        Typical use is from middleware — set the context once at request entry
        and every ``flag.get()`` (and other context-sensitive evaluations) inside
        that request automatically picks it up.  ``contextvars`` provides per-task
        / per-thread isolation so concurrent requests don't cross-contaminate.

        Each unique ``(type, key)`` is also registered with the platform
        (deduplicated via an LRU; sent in the background).

        Two usage shapes::

            # Fire-and-forget (typical middleware)
            client.set_context([Context("user", ...), Context("account", ...)])

            # Scoped block (use ``async with`` if you want async semantics)
            with client.set_context([Context("user", "impersonated")]):
                ...
            # original context restored here

        Args:
            contexts: The contexts to make active for the current task/thread
                (e.g. the request's user and account). An empty list clears
                any registration step but still returns a scope.

        Returns:
            A ``ContextScope`` you can ignore for fire-and-forget use, or
            enter as a ``with`` / ``async with`` block to restore the previous
            context on exit.
        """
        self._ensure_started()
        if contexts:
            self.platform.contexts.register(contexts)
        return _set_context(contexts)

    async def close(self) -> None:
        """Release all resources held by this client."""
        _debug("lifecycle", "AsyncSmplClient.close() called")
        self._closed = True
        if self._flush_timer is not None:
            self._flush_timer.cancel()
            self._flush_timer = None
        await self._final_flush()
        if self._metrics is not None:
            await self._metrics.close()
        self.logging._close()
        self.flags._close()
        await self.audit._close()
        if self._ws_manager is not None:
            self._ws_manager.stop()
            self._ws_manager = None
        # Close the shared per-service async HTTP transports.
        await self._transports.aclose()

    async def __aenter__(self) -> AsyncSmplClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()


# Use the existing debug function from _debug module.
_debug = debug
