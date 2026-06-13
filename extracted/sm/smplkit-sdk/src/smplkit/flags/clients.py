"""The Smpl Flags client — one unified ``FlagsClient`` / ``AsyncFlagsClient``.

Smpl Flags has two surfaces on a single client, mirroring how the config,
audit, and jobs clients expose their full surface from one class:

* **CRUD surface** — pure CRUD, no live connection:
  ``new_boolean_flag`` / ``new_string_flag`` / ``new_number_flag`` /
  ``new_json_flag`` constructors, ``get`` / ``list`` / ``delete`` CRUD, and
  the flag-declaration discovery buffer (``register`` / ``flush`` /
  ``flush_sync`` / ``pending_count``). The client owns the discovery buffer
  directly.
* **Live surface** — lazily connects to your running service on first use:
  the typed handle declarations (``boolean_flag`` / ``string_flag`` /
  ``number_flag`` / ``json_flag``) whose ``.get()`` evaluates against the
  cached definitions, plus ``refresh`` / ``stats`` / ``on_change``. The
  first live call transparently flushes discovery, fetches all flag
  definitions into the local cache, and opens the live-updates WebSocket —
  no explicit install step.

The client supports two construction shapes:

* **Wired** into :class:`smplkit.SmplClient` — borrows the parent's flags
  transport for both runtime fetch and CRUD, the parent's shared WebSocket
  for the live channel, and ``client.platform.contexts`` for
  evaluation-context registration. This is the common path.
* **Standalone** — ``FlagsClient(api_key=..., base_url=..., ...)`` builds
  and owns its own flags transport and a contexts client (against its own
  app transport), and on first live use opens and owns its own WebSocket.
  ``close()`` / ``aclose()`` tears down only the owned transports and owned
  WebSocket.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import logging
import threading
from collections import OrderedDict
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from smplkit._config import _service_url, resolve_client_config
from smplkit.context import get_context as _get_request_context
from smplkit.errors import (
    ConnectionError,
    NotFoundError,
    TimeoutError,
    ValidationError,
    _raise_for_status,
)
from smplkit._helpers import key_to_display_name, paginate_async, paginate_sync
from smplkit._generated.app.client import AuthenticatedClient as _AppAuthClient
from smplkit._generated.flags.api.flags import (  # noqa: F401  (re-exported for test patches)
    bulk_register_flags,
    create_flag,
    delete_flag,
    get_flag,
    list_flags,
    update_flag,
)
from smplkit._generated.flags.client import AuthenticatedClient
from smplkit._generated.flags.models.flag_bulk_item import FlagBulkItem as _GenFlagBulkItem
from smplkit._generated.flags.models.flag_bulk_request import FlagBulkRequest as _GenFlagBulkRequest
from smplkit.flags.helpers import _build_flag_request_body, _flag_dict_from_json
from smplkit.flags.models import (
    AsyncBooleanFlag,
    AsyncFlag,
    AsyncJsonFlag,
    AsyncNumberFlag,
    AsyncStringFlag,
    BooleanFlag,
    Flag,
    FlagValue,
    JsonFlag,
    NumberFlag,
    StringFlag,
)
from smplkit._buffer import _FLAG_BATCH_FLUSH_SIZE, _FlagRegistrationBuffer
from smplkit._ws import SharedWebSocket

if TYPE_CHECKING:
    from smplkit._metrics import _AsyncMetricsReporter, _MetricsReporter
    from smplkit.clients import AsyncSmplClient, SmplClient
    from smplkit.flags.types import Context, FlagDeclaration
    from smplkit.platform.clients import (
        AsyncContextsClient,
        ContextsClient,
    )

logger = logging.getLogger("smplkit")
ws_logger = logging.getLogger("smplkit.flags.ws")

_CACHE_MAX_SIZE = 10_000


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _check_response_status(status_code: Any, content: bytes) -> None:
    """Map HTTP error status codes to SDK exceptions with full JSON:API error detail."""
    _raise_for_status(int(status_code), content)


def _exc_url(exc: Exception) -> str | None:
    """Extract URL from an httpx exception's associated request, if available."""
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
    if isinstance(exc, (NotFoundError, ValidationError)):
        raise exc


def _contexts_to_eval_dict(contexts: list[Context]) -> dict[str, Any]:
    """Convert a list of Context objects to the nested evaluation dict."""
    result: dict[str, Any] = {}
    for ctx in contexts:
        entry = {"key": ctx.key, **ctx.attributes}
        result[ctx.type] = entry
    return result


def _hash_context(eval_dict: dict[str, Any]) -> str:
    """Compute a stable hash for a context evaluation dict."""
    serialized = json.dumps(eval_dict, sort_keys=True, default=str)
    return hashlib.md5(serialized.encode()).hexdigest()


def _build_flag_bulk_request(batch: list[dict[str, Any]]) -> _GenFlagBulkRequest | None:
    """Build a JSON:API bulk request body from a list of pending flag items.

    Returns ``None`` when *batch* is empty.  Items are not removed from any
    buffer here; callers must commit on a successful send.
    """
    if not batch:
        return None
    items = [
        _GenFlagBulkItem(
            id=b["id"],
            type_=b["type"],
            default=b["default"],
            service=b.get("service"),
            environment=b.get("environment"),
        )
        for b in batch
    ]
    return _GenFlagBulkRequest(flags=items)


def _pagination_kwargs(page_number: int | None, page_size: int | None) -> dict[str, int]:
    kwargs: dict[str, int] = {}
    if page_number is not None:
        kwargs["pagenumber"] = page_number
    if page_size is not None:
        kwargs["pagesize"] = page_size
    return kwargs


def _flags_transport(
    *,
    api_key: str | None,
    base_url: str | None,
    profile: str | None,
    base_domain: str | None,
    scheme: str | None,
    debug: bool | None,
    extra_headers: dict[str, str] | None,
) -> tuple[AuthenticatedClient, _AppAuthClient, str]:
    """Build standalone flags + app transports and resolve the app base URL.

    ``base_url``/``api_key`` are used directly when both are supplied (the
    path a top-level client takes after it has already resolved them);
    otherwise the config resolver fills in whatever is missing
    (``~/.smplkit`` / env vars / defaults). The app transport backs the
    standalone contexts client (evaluation-context registration); the app
    base URL is returned so a standalone client can open its own WebSocket
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
    flags_url = base_url if base_url is not None else _service_url(cfg.scheme, "flags", cfg.base_domain)
    app_url = _service_url(cfg.scheme, "app", cfg.base_domain)
    headers: dict[str, str] = {}
    headers.update(cfg.extra_headers or {})
    headers.update(extra_headers or {})
    flags_http = AuthenticatedClient(base_url=flags_url.rstrip("/"), token=resolved_key, headers=headers)
    app_http = _AppAuthClient(base_url=app_url.rstrip("/"), token=resolved_key, headers=headers)
    return flags_http, app_http, app_url


# ---------------------------------------------------------------------------
# Change event
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True, kw_only=True)
class FlagChangeEvent:
    """Describes a flag definition change.  Frozen — fields are set at construction."""

    id: str
    source: str
    deleted: bool = False


# ---------------------------------------------------------------------------
# Resolution cache + stats
# ---------------------------------------------------------------------------


class _ResolutionCache:
    """Thread-safe LRU resolution cache with hit/miss stats."""

    def __init__(self, max_size: int = _CACHE_MAX_SIZE) -> None:
        self._max_size = max_size
        self._cache: OrderedDict[str, Any] = OrderedDict()
        self._lock = threading.Lock()
        self.cache_hits = 0
        self.cache_misses = 0

    def get(self, cache_key: str) -> tuple[bool, Any]:
        """Return (hit, value).  Moves the key to end on hit."""
        with self._lock:
            if cache_key in self._cache:
                self._cache.move_to_end(cache_key)
                self.cache_hits += 1
                return True, self._cache[cache_key]
            self.cache_misses += 1
            return False, None

    def put(self, cache_key: str, value: Any) -> None:
        with self._lock:
            if cache_key in self._cache:
                self._cache.move_to_end(cache_key)
                self._cache[cache_key] = value
            else:
                self._cache[cache_key] = value
                if len(self._cache) > self._max_size:
                    self._cache.popitem(last=False)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()


class FlagStats:
    """Evaluation statistics for the flags runtime."""

    cache_hits: int
    cache_misses: int

    def __init__(self, *, cache_hits: int, cache_misses: int) -> None:
        self.cache_hits = cache_hits
        self.cache_misses = cache_misses

    def __repr__(self) -> str:
        return f"FlagStats(cache_hits={self.cache_hits}, cache_misses={self.cache_misses})"


# ---------------------------------------------------------------------------
# FlagsClient (sync)
# ---------------------------------------------------------------------------


class FlagsClient:
    """The Smpl Flags client (sync).

    One client exposes the full surface, reachable as ``client.flags``
    (:class:`smplkit.SmplClient`) or constructed directly::

        from smplkit import FlagsClient

        with FlagsClient(environment="production") as flags:
            new_flag = flags.new_boolean_flag("beta", default=False)
            new_flag.save()
            beta = flags.boolean_flag("beta", default=False)
            if beta.get():
                ...

    The CRUD surface (``new_*`` / ``get`` / ``list`` / ``delete`` and
    discovery) is pure CRUD. The live surface (``boolean_flag`` /
    ``string_flag`` / ``number_flag`` / ``json_flag`` / ``refresh`` /
    ``stats`` / ``on_change``) connects lazily on first use — the first call
    flushes discovery, fetches all flag definitions into the local cache, and
    opens the live-updates WebSocket. No explicit install step is required.

    Args:
        api_key: API key. When omitted, resolved from ``SMPLKIT_API_KEY`` or
            ``~/.smplkit``.
        environment: Deployment environment used to resolve runtime flag
            values and to scope discovery declarations. Optional.
        base_url: Full flags-service base URL. Usually resolved from
            ``base_domain``/``scheme``; supplied directly by the top-level
            clients which have already computed it.
        profile: Named ``~/.smplkit`` profile section.
        base_domain: Base domain for API requests (default ``"smplkit.com"``).
        scheme: URL scheme (default ``"https"``).
        debug: Enable SDK debug logging.
        extra_headers: Extra headers attached to every request.
        parent: Internal — the owning :class:`smplkit.SmplClient`. Not for
            direct use.
        transport: Internal — a pre-built flags transport supplied by a
            top-level client so the flags surface shares one connection pool.
            Not for direct use.
        contexts: Internal — ``client.platform.contexts`` used for
            evaluation-context registration. Not for direct use.
        metrics: Internal — the parent's metrics reporter.
    """

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
        contexts: ContextsClient | None = None,
        metrics: _MetricsReporter | None = None,
    ) -> None:
        self._parent = parent
        self._metrics = metrics
        self._environment = parent._environment if parent is not None else environment
        self._service = parent._service if parent is not None else None
        self._standalone_api_key: str | None = None
        self._owns_contexts = False
        if transport is not None:
            self._flags_http = transport
            self._app_base_url: str | None = None
            self._owns_transport = False
            # Wired: borrow client.platform.contexts as the evaluation-context
            # registration seam.
            self._contexts: ContextsClient | None = contexts
        else:
            self._flags_http, app_http, self._app_base_url = _flags_transport(
                api_key=api_key,
                base_url=base_url,
                profile=profile,
                base_domain=base_domain,
                scheme=scheme,
                debug=debug,
                extra_headers=extra_headers,
            )
            self._owns_transport = True
            self._standalone_api_key = api_key if api_key is not None else self._flags_http.token
            # Standalone: build our own contexts client (and own its app transport).
            from smplkit._buffer import _ContextRegistrationBuffer
            from smplkit.platform.clients import ContextsClient

            self._app_http_standalone = app_http
            self._contexts = ContextsClient(app_http, _ContextRegistrationBuffer())
            self._owns_contexts = True

        # Discovery buffer is owned by this client (no management delegation).
        self._buffer = _FlagRegistrationBuffer()

        # Live-surface state.
        self._flag_store: dict[str, dict[str, Any]] = {}
        self._connected = False
        self._ws_subscribed = False
        self._cache = _ResolutionCache()
        self._handles: dict[str, Flag] = {}
        self._global_listeners: list[Callable[[FlagChangeEvent], None]] = []
        self._key_listeners: dict[str, list[Callable[[FlagChangeEvent], None]]] = {}
        self._ws_manager: SharedWebSocket | None = None
        self._owns_ws = False

    def _close(self) -> None:
        """Release resources held by this client (alias for :meth:`close`)."""
        self.close()

    # ------------------------------------------------------------------
    # Management surface: CRUD (no live connection)
    # ------------------------------------------------------------------

    def new_boolean_flag(
        self,
        id: str,
        *,
        default: bool,
        name: str | None = None,
        description: str | None = None,
    ) -> BooleanFlag:
        """Return a new unsaved boolean :class:`BooleanFlag`. Call ``save()`` to persist.

        Args:
            id: Stable flag identifier. Unique per account.
            default: Value served when no environment override or rule applies.
            name: Human-readable display name. Defaults to a title-cased form of
                ``id``.
            description: Optional free-text description of the flag.

        Returns:
            An unsaved :class:`BooleanFlag`; call ``save()`` to persist it.
        """
        return BooleanFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="BOOLEAN",
            default=default,
            values=[FlagValue(name="True", value=True), FlagValue(name="False", value=False)],
            description=description,
        )

    def new_string_flag(
        self,
        id: str,
        *,
        default: str,
        name: str | None = None,
        description: str | None = None,
        values: list[FlagValue] | None = None,
    ) -> StringFlag:
        """Return a new unsaved string :class:`StringFlag`. Call ``save()`` to persist.

        Args:
            id: Stable flag identifier. Unique per account.
            default: Value served when no environment override or rule applies.
            name: Human-readable display name. Defaults to a title-cased form of
                ``id``.
            description: Optional free-text description of the flag.
            values: Optional list of allowed values constraining what the flag may
                serve. When omitted, the flag is unconstrained.

        Returns:
            An unsaved :class:`StringFlag`; call ``save()`` to persist it.
        """
        return StringFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="STRING",
            default=default,
            values=values,
            description=description,
        )

    def new_number_flag(
        self,
        id: str,
        *,
        default: int | float,
        name: str | None = None,
        description: str | None = None,
        values: list[FlagValue] | None = None,
    ) -> NumberFlag:
        """Return a new unsaved numeric :class:`NumberFlag`. Call ``save()`` to persist.

        Args:
            id: Stable flag identifier. Unique per account.
            default: Value served when no environment override or rule applies.
            name: Human-readable display name. Defaults to a title-cased form of
                ``id``.
            description: Optional free-text description of the flag.
            values: Optional list of allowed values constraining what the flag may
                serve. When omitted, the flag is unconstrained.

        Returns:
            An unsaved :class:`NumberFlag`; call ``save()`` to persist it.
        """
        return NumberFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="NUMERIC",
            default=default,
            values=values,
            description=description,
        )

    def new_json_flag(
        self,
        id: str,
        *,
        default: dict[str, Any],
        name: str | None = None,
        description: str | None = None,
        values: list[FlagValue] | None = None,
    ) -> JsonFlag:
        """Return a new unsaved JSON :class:`JsonFlag`. Call ``save()`` to persist.

        Args:
            id: Stable flag identifier. Unique per account.
            default: Value served when no environment override or rule applies.
            name: Human-readable display name. Defaults to a title-cased form of
                ``id``.
            description: Optional free-text description of the flag.
            values: Optional list of allowed values constraining what the flag may
                serve. When omitted, the flag is unconstrained.

        Returns:
            An unsaved :class:`JsonFlag`; call ``save()`` to persist it.
        """
        return JsonFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="JSON",
            default=default,
            values=values,
            description=description,
        )

    def get(self, id: str) -> Flag:
        """Fetch the editable :class:`Flag` resource by id.

        Args:
            id: Identifier of the flag to fetch.

        Returns:
            The :class:`Flag`, ready to mutate and ``save()``.

        Raises:
            NotFoundError: No flag with that id exists for the account.
        """
        try:
            response = get_flag.sync_detailed(id, client=self._flags_http)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._flags_http._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        body = json.loads(response.content)
        return self._model_from_json(body["data"])

    def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[Flag]:
        """List flags for the authenticated account.

        Args:
            page_number: 1-based page index to fetch. When omitted, the server
                default applies.
            page_size: Number of flags per page. When omitted, the server default
                applies.

        Returns:
            The flags on the requested page as a list of :class:`Flag`.
        """
        kwargs = _pagination_kwargs(page_number, page_size)
        try:
            response = list_flags.sync_detailed(client=self._flags_http, **kwargs)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._flags_http._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        body = json.loads(response.content)
        return [self._model_from_json(r) for r in body.get("data", [])]

    def delete(self, id: str) -> None:
        """Delete a flag by id.

        Args:
            id: Identifier of the flag to delete.

        Raises:
            NotFoundError: No flag with that id exists for the account.
        """
        try:
            response = delete_flag.sync_detailed(id, client=self._flags_http)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._flags_http._base_url)
            raise
        _check_response_status(response.status_code, response.content)

    def _create_flag(self, flag: Flag) -> Flag:
        body = _build_flag_request_body(flag, flag_id=flag.id)
        try:
            response = create_flag.sync_detailed(client=self._flags_http, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._flags_http._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        resp_body = json.loads(response.content)
        return self._model_from_json(resp_body["data"])

    def _update_flag(self, *, flag: Flag) -> Flag:
        body = _build_flag_request_body(flag, flag_id=flag.id)
        try:
            response = update_flag.sync_detailed(flag.id, client=self._flags_http, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._flags_http._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        resp_body = json.loads(response.content)
        return self._model_from_json(resp_body["data"])

    def _model_from_json(self, data: dict[str, Any]) -> Flag:
        d = _flag_dict_from_json(data)
        return Flag(self, **d)

    # ------------------------------------------------------------------
    # Management surface: discovery buffer (owned directly)
    # ------------------------------------------------------------------

    def register(
        self,
        items: FlagDeclaration | list[FlagDeclaration],
        *,
        flush: bool = False,
    ) -> None:
        """Buffer flag declarations for bulk-discovery upload; optionally flush now.

        Args:
            items: A single :class:`FlagDeclaration` or a list of them to queue.
            flush: When ``True``, send the buffered declarations immediately via
                :meth:`flush` before returning. When ``False`` (the default), they
                stay buffered and are sent on the next flush — automatic once the
                buffer reaches its batch size, or on the first live call. The async
                client has no ``flush`` parameter because it offers no synchronous
                flush path; on that client always ``await flush()`` to send.
        """
        batch = items if isinstance(items, list) else [items]
        for d in batch:
            self._buffer.add(d.id, d.type, d.default, d.service, d.environment)
        if flush:
            self.flush()
            return
        if self._buffer.pending_count >= _FLAG_BATCH_FLUSH_SIZE:
            threading.Thread(target=self._threshold_flush, daemon=True).start()

    def _threshold_flush(self) -> None:
        try:
            self.flush()
        except Exception as exc:
            logger.warning("Flag registration flush failed: %s", exc)

    def flush(self) -> None:
        """POST pending declarations to the flags bulk endpoint.

        Items remain in the buffer until the request succeeds, so a flush
        against an unhealthy ``flags`` service is automatically retried by
        the next ``flush()`` call (periodic background flush, install retry,
        or final flush on close).
        """
        batch = self._buffer.peek()
        body = _build_flag_bulk_request(batch)
        if body is None:
            return
        try:
            response = bulk_register_flags.sync_detailed(client=self._flags_http, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._flags_http._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        self._buffer.commit([b["id"] for b in batch])

    def flush_sync(self) -> None:
        """Synchronous flush — alias of :meth:`flush` for the periodic-flush path."""
        self.flush()

    @property
    def pending_count(self) -> int:
        """Number of pending flag declarations awaiting flush."""
        return self._buffer.pending_count

    def _observe_declaration(self, flag_id: str, flag_type: str, default: Any) -> None:
        """Queue a declared flag with the owned discovery buffer."""
        from smplkit.flags.types import FlagDeclaration

        self.register(
            FlagDeclaration(
                id=flag_id,
                type=flag_type,
                default=default,
                service=self._service,
                environment=self._environment,
            )
        )

    # ------------------------------------------------------------------
    # Live surface: lazy connect + transport / WebSocket helpers
    # ------------------------------------------------------------------

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

    def _ensure_connected(self) -> None:
        """Open the live connection to the running Smpl Flags service.

        Flushes any buffered discovery declarations, fetches all flag
        definitions into the local cache, opens the shared WebSocket, and
        subscribes to ``flag_changed`` / ``flag_deleted`` / ``flags_changed``
        events.

        Idempotent and internal — every live method calls it on first use, so
        the live surface auto-connects with no explicit step.
        """
        if self._parent is not None:
            self._parent._ensure_started()
        if self._connected:
            return

        # Flush discovered flags BEFORE fetching definitions so the fetch
        # reflects them. Items stay in the buffer until the POST succeeds.
        try:
            self.flush()
        except Exception as exc:
            logger.warning("Flags discovery flush before connect failed: %s", exc)

        self._fetch_all_flags()
        self._cache.clear()
        self._connected = True

        self._ws_manager = self._ensure_ws()
        if not self._ws_subscribed:
            self._ws_manager.on("flag_changed", self._handle_flag_changed)
            self._ws_manager.on("flag_deleted", self._handle_flag_deleted)
            self._ws_manager.on("flags_changed", self._handle_flags_changed)
            self._ws_subscribed = True

    # ------------------------------------------------------------------
    # Live surface: typed flag handles
    # ------------------------------------------------------------------

    def boolean_flag(self, id: str, *, default: bool) -> BooleanFlag:
        """Declare a boolean flag handle for live evaluation. Connects lazily on first use.

        Args:
            id: Identifier of the flag to evaluate.
            default: Value returned by ``handle.get()`` when the flag is unknown or
                no environment override or rule applies.

        Returns:
            A :class:`BooleanFlag` handle whose ``get()`` evaluates against the live
            cache.
        """
        self._ensure_connected()
        handle = BooleanFlag(self, id=id, name=id, type="BOOLEAN", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "BOOLEAN", default)
        return handle

    def string_flag(self, id: str, *, default: str) -> StringFlag:
        """Declare a string flag handle for live evaluation. Connects lazily on first use.

        Args:
            id: Identifier of the flag to evaluate.
            default: Value returned by ``handle.get()`` when the flag is unknown or
                no environment override or rule applies.

        Returns:
            A :class:`StringFlag` handle whose ``get()`` evaluates against the live
            cache.
        """
        self._ensure_connected()
        handle = StringFlag(self, id=id, name=id, type="STRING", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "STRING", default)
        return handle

    def number_flag(self, id: str, *, default: int | float) -> NumberFlag:
        """Declare a numeric flag handle for live evaluation. Connects lazily on first use.

        Args:
            id: Identifier of the flag to evaluate.
            default: Value returned by ``handle.get()`` when the flag is unknown or
                no environment override or rule applies.

        Returns:
            A :class:`NumberFlag` handle whose ``get()`` evaluates against the live
            cache.
        """
        self._ensure_connected()
        handle = NumberFlag(self, id=id, name=id, type="NUMERIC", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "NUMERIC", default)
        return handle

    def json_flag(self, id: str, *, default: dict[str, Any]) -> JsonFlag:
        """Declare a JSON flag handle for live evaluation. Connects lazily on first use.

        Args:
            id: Identifier of the flag to evaluate.
            default: Value returned by ``handle.get()`` when the flag is unknown or
                no environment override or rule applies.

        Returns:
            A :class:`JsonFlag` handle whose ``get()`` evaluates against the live
            cache.
        """
        self._ensure_connected()
        handle = JsonFlag(self, id=id, name=id, type="JSON", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "JSON", default)
        return handle

    # ------------------------------------------------------------------
    # Live surface: refresh / stats / change listeners
    # ------------------------------------------------------------------

    def refresh(self) -> None:
        """Re-fetch all flag definitions and clear cache.

        Connects lazily on first use — no explicit install step.
        """
        self._ensure_connected()
        self._do_refresh("manual")

    def _do_refresh(self, source: str) -> None:
        self._fetch_all_flags()
        self._cache.clear()
        self._fire_change_listeners_all(source)

    def stats(self) -> FlagStats:
        """Return evaluation statistics. Connects lazily on first use."""
        self._ensure_connected()
        return FlagStats(cache_hits=self._cache.cache_hits, cache_misses=self._cache.cache_misses)

    def on_change(self, fn_or_id: Callable[[FlagChangeEvent], None] | str | None = None) -> Any:
        """Register a change listener.

        Supports two forms:

        - ``@client.flags.on_change`` — registers a global listener.
        - ``@client.flags.on_change("flag-id")`` — registers an id-scoped listener.

        Connects lazily on first use — no explicit install step.

        Args:
            fn_or_id: Either the listener callable (used directly as
                ``@on_change``), or a flag id string scoping the listener to that
                flag (used as ``@on_change("flag-id")``). When ``None``, returns a
                decorator that registers a global listener.

        Returns:
            The listener callable when one is passed directly, otherwise a decorator
            that registers the callable it wraps. Each listener receives a
            :class:`FlagChangeEvent`.
        """
        self._ensure_connected()
        if callable(fn_or_id):
            self._global_listeners.append(fn_or_id)
            return fn_or_id
        elif isinstance(fn_or_id, str):
            flag_id = fn_or_id

            def decorator(fn: Callable[[FlagChangeEvent], None]) -> Callable[[FlagChangeEvent], None]:
                self._key_listeners.setdefault(flag_id, []).append(fn)
                return fn

            return decorator
        else:

            def decorator(fn: Callable[[FlagChangeEvent], None]) -> Callable[[FlagChangeEvent], None]:
                self._global_listeners.append(fn)
                return fn

            return decorator

    # ------------------------------------------------------------------
    # Internal: evaluation
    # ------------------------------------------------------------------

    def _evaluate_handle(self, flag_id: str, default: Any, context: list[Context] | None) -> Any:
        """Core evaluation used by flag handles (the ``.get()`` path).

        Connects lazily on first use so ``flag.get()`` works without an
        explicit install step.
        """
        self._ensure_connected()
        if context is not None:
            # Explicit context: register here.  (Implicit set_context registers
            # at the entry point, so the contextvar branch below doesn't need to.)
            if self._contexts is not None:
                self._contexts.register(context)
            eval_dict = _contexts_to_eval_dict(context)
        else:
            contexts = _get_request_context()
            eval_dict = _contexts_to_eval_dict(contexts) if contexts else {}

        # Auto-inject service context if set and not already provided
        if self._service and "service" not in eval_dict:
            eval_dict["service"] = {"key": self._service}

        ctx_hash = _hash_context(eval_dict)
        cache_key = f"{flag_id}:{ctx_hash}"

        hit, cached_value = self._cache.get(cache_key)
        if hit:
            metrics = self._metrics
            if metrics is not None:
                metrics.record("flags.cache_hits", unit="hits")
                metrics.record("flags.evaluations", unit="evaluations", dimensions={"flag": flag_id})
            return cached_value

        flag_def = self._flag_store.get(flag_id)
        if flag_def is None:
            self._cache.put(cache_key, default)
            return default

        value = _evaluate_flag(flag_def, self._environment, eval_dict)
        if value is None:
            value = default

        self._cache.put(cache_key, value)
        metrics = self._metrics
        if metrics is not None:
            metrics.record("flags.cache_misses", unit="misses")
            metrics.record("flags.evaluations", unit="evaluations", dimensions={"flag": flag_id})
        return value

    # ------------------------------------------------------------------
    # Internal: event handlers (called by SharedWebSocket)
    # ------------------------------------------------------------------

    def _handle_flag_changed(self, data: dict[str, Any]) -> None:
        key = data.get("id")
        if not key:
            return
        pre = dict(self._flag_store.get(key, {}))
        new_data = self._fetch_flag_single_data(key)
        self._flag_store[key] = new_data
        self._cache.clear()
        if pre != new_data:
            self._fire_change_listeners(key, "websocket")

    def _handle_flag_deleted(self, data: dict[str, Any]) -> None:
        key = data.get("id")
        if not key:
            return
        existed = key in self._flag_store
        self._flag_store.pop(key, None)
        self._cache.clear()
        if existed:
            self._fire_change_listeners(key, "websocket", deleted=True)

    def _handle_flags_changed(self, data: dict[str, Any]) -> None:
        pre_store = dict(self._flag_store)
        try:
            self._fetch_all_flags()
        except Exception:
            ws_logger.error("Failed to refresh flags after flags_changed WS event", exc_info=True)
            return
        self._cache.clear()
        post_store = self._flag_store
        all_keys = set(pre_store) | set(post_store)
        changed = [k for k in all_keys if pre_store.get(k) != post_store.get(k)]
        if not changed:
            return
        # Global listener fires once
        first_event = FlagChangeEvent(id=changed[0], source="websocket")
        for cb in self._global_listeners:
            try:
                cb(first_event)
            except Exception:
                logger.error("Exception in global flags on_change listener", exc_info=True)
        # Per-key listeners fire for each changed key
        for k in changed:
            deleted = k in pre_store and k not in post_store
            event = FlagChangeEvent(id=k, source="websocket", deleted=deleted)
            for cb in self._key_listeners.get(k, []):
                try:
                    cb(event)
                except Exception:
                    logger.error("Exception in id-scoped flags on_change listener", exc_info=True)

    # ------------------------------------------------------------------
    # Internal: flag store
    # ------------------------------------------------------------------

    def _fetch_flag_single_data(self, key: str) -> dict[str, Any]:
        """Fetch a single flag by key and return a store-format dict."""
        try:
            response = get_flag.sync_detailed(key, client=self._flags_http)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._flags_http._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        body = json.loads(response.content)
        d = _flag_dict_from_json(body["data"])
        return _store_entry(d)

    def _fetch_all_flags(self) -> None:
        flags = self._fetch_flags_list()
        self._flag_store = {f["id"]: f for f in flags}

    def _fetch_flags_list(self) -> list[dict[str, Any]]:
        def fetch_page(page_number: int, page_size: int) -> list[dict[str, Any]]:
            try:
                response = list_flags.sync_detailed(
                    client=self._flags_http,
                    pagenumber=page_number,
                    pagesize=page_size,
                )
            except Exception as exc:
                _maybe_reraise_network_error(exc, self._flags_http._base_url)
                raise
            _check_response_status(response.status_code, response.content)
            body = json.loads(response.content)
            return [_store_entry(_flag_dict_from_json(r)) for r in body.get("data", [])]

        return paginate_sync(fetch_page)

    def _fire_change_listeners(self, flag_id: str | None, source: str, *, deleted: bool = False) -> None:
        if flag_id:
            event = FlagChangeEvent(id=flag_id, source=source, deleted=deleted)
            for cb in self._global_listeners:
                try:
                    cb(event)
                except Exception:
                    logger.error("Exception in global flags on_change listener", exc_info=True)
            for cb in self._key_listeners.get(flag_id, []):
                try:
                    cb(event)
                except Exception:
                    logger.error("Exception in id-scoped flags on_change listener", exc_info=True)

    def _fire_change_listeners_all(self, source: str) -> None:
        for flag_id in self._flag_store:
            self._fire_change_listeners(flag_id, source)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Release resources — only those this client owns.

        Tears down the owned WebSocket (standalone install) and the owned
        flags + app HTTP transports (standalone construction). A wired client
        borrows the parent's transport, WebSocket, and contexts client and
        closes none of them.
        """
        if self._owns_ws and self._ws_manager is not None:
            self._ws_manager.stop()
            self._ws_manager = None
            self._owns_ws = False
        if self._owns_transport:
            client = self._flags_http._client
            if client is not None:
                client.close()
                self._flags_http._client = None
            if self._owns_contexts:
                app_client = self._app_http_standalone._client
                if app_client is not None:
                    app_client.close()
                    self._app_http_standalone._client = None

    def __enter__(self) -> FlagsClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


# ---------------------------------------------------------------------------
# AsyncFlagsClient
# ---------------------------------------------------------------------------


class AsyncFlagsClient:
    """The Smpl Flags client (async) — counterpart of :class:`FlagsClient`.

    Reads, CRUD, and discovery flush perform their network round-trips with
    ``await``. The live surface connects lazily — ``await refresh()`` (or
    ``await client.wait_until_ready()``) opens the connection: it flushes
    discovery, fetches all flag definitions, and opens the WebSocket. The
    synchronous helpers (``boolean_flag`` / ``string_flag`` / ``number_flag``
    / ``json_flag`` / ``stats`` / ``on_change`` and a handle's ``.get()``)
    operate against whatever cache state exists, so warm the cache first via
    an awaitable live method. No explicit install step is required.

    Args:
        api_key: API key. When omitted, resolved from ``SMPLKIT_API_KEY`` or
            ``~/.smplkit``.
        environment: Deployment environment used to resolve runtime flag
            values and to scope discovery declarations. Optional.
        base_url: Full flags-service base URL. Usually resolved from
            ``base_domain``/``scheme``; supplied directly by the top-level
            clients which have already computed it.
        profile: Named ``~/.smplkit`` profile section.
        base_domain: Base domain for API requests (default ``"smplkit.com"``).
        scheme: URL scheme (default ``"https"``).
        debug: Enable SDK debug logging.
        extra_headers: Extra headers attached to every request.
        parent: Internal — the owning :class:`smplkit.AsyncSmplClient`. Not for
            direct use.
        transport: Internal — a pre-built flags transport supplied by a
            top-level client so the flags surface shares one connection pool.
            Not for direct use.
        contexts: Internal — ``client.platform.contexts`` used for
            evaluation-context registration. Not for direct use.
        metrics: Internal — the parent's metrics reporter.
    """

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
        contexts: AsyncContextsClient | None = None,
        metrics: _AsyncMetricsReporter | None = None,
    ) -> None:
        self._parent = parent
        self._metrics = metrics
        self._environment = parent._environment if parent is not None else environment
        self._service = parent._service if parent is not None else None
        self._standalone_api_key: str | None = None
        self._owns_contexts = False
        if transport is not None:
            self._flags_http = transport
            self._app_base_url: str | None = None
            self._owns_transport = False
            self._contexts: AsyncContextsClient | None = contexts
        else:
            self._flags_http, app_http, self._app_base_url = _flags_transport(
                api_key=api_key,
                base_url=base_url,
                profile=profile,
                base_domain=base_domain,
                scheme=scheme,
                debug=debug,
                extra_headers=extra_headers,
            )
            self._owns_transport = True
            self._standalone_api_key = api_key if api_key is not None else self._flags_http.token
            from smplkit._buffer import _ContextRegistrationBuffer
            from smplkit.platform.clients import AsyncContextsClient as _AsyncContextsClient

            self._app_http_standalone = app_http
            self._contexts = _AsyncContextsClient(app_http, _ContextRegistrationBuffer())
            self._owns_contexts = True

        self._buffer = _FlagRegistrationBuffer()

        self._flag_store: dict[str, dict[str, Any]] = {}
        self._connected = False
        self._ws_subscribed = False
        self._cache = _ResolutionCache()
        self._handles: dict[str, AsyncFlag] = {}
        self._global_listeners: list[Callable[[FlagChangeEvent], None]] = []
        self._key_listeners: dict[str, list[Callable[[FlagChangeEvent], None]]] = {}
        self._ws_manager: SharedWebSocket | None = None
        self._owns_ws = False

    def _close(self) -> None:
        """Synchronous teardown of owned transports (no event-loop dependency).

        Closes the owned WebSocket and the underlying sync HTTP clients on
        the owned transports. The async transport is torn down by
        :meth:`aclose`. Called by :class:`AsyncSmplClient.close` which closes
        the async transport pools through the shared service transports.
        """
        if self._owns_ws and self._ws_manager is not None:
            self._ws_manager.stop()
            self._ws_manager = None
            self._owns_ws = False
        if self._owns_transport:
            client = self._flags_http._client
            if client is not None:
                client.close()
                self._flags_http._client = None
            if self._owns_contexts:
                app_client = self._app_http_standalone._client
                if app_client is not None:
                    app_client.close()
                    self._app_http_standalone._client = None

    # ------------------------------------------------------------------
    # Management surface: CRUD (no live connection)
    # ------------------------------------------------------------------

    def new_boolean_flag(
        self,
        id: str,
        *,
        default: bool,
        name: str | None = None,
        description: str | None = None,
    ) -> AsyncBooleanFlag:
        """Return a new unsaved :class:`AsyncBooleanFlag`. Call ``await save()`` to persist.

        Args:
            id: Stable flag identifier. Unique per account.
            default: Value served when no environment override or rule applies.
            name: Human-readable display name. Defaults to a title-cased form of
                ``id``.
            description: Optional free-text description of the flag.

        Returns:
            An unsaved :class:`AsyncBooleanFlag`; call ``await save()`` to persist it.
        """
        return AsyncBooleanFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="BOOLEAN",
            default=default,
            values=[FlagValue(name="True", value=True), FlagValue(name="False", value=False)],
            description=description,
        )

    def new_string_flag(
        self,
        id: str,
        *,
        default: str,
        name: str | None = None,
        description: str | None = None,
        values: list[FlagValue] | None = None,
    ) -> AsyncStringFlag:
        """Return a new unsaved :class:`AsyncStringFlag`. Call ``await save()`` to persist.

        Args:
            id: Stable flag identifier. Unique per account.
            default: Value served when no environment override or rule applies.
            name: Human-readable display name. Defaults to a title-cased form of
                ``id``.
            description: Optional free-text description of the flag.
            values: Optional list of allowed values constraining what the flag may
                serve. When omitted, the flag is unconstrained.

        Returns:
            An unsaved :class:`AsyncStringFlag`; call ``await save()`` to persist it.
        """
        return AsyncStringFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="STRING",
            default=default,
            values=values,
            description=description,
        )

    def new_number_flag(
        self,
        id: str,
        *,
        default: int | float,
        name: str | None = None,
        description: str | None = None,
        values: list[FlagValue] | None = None,
    ) -> AsyncNumberFlag:
        """Return a new unsaved :class:`AsyncNumberFlag`. Call ``await save()`` to persist.

        Args:
            id: Stable flag identifier. Unique per account.
            default: Value served when no environment override or rule applies.
            name: Human-readable display name. Defaults to a title-cased form of
                ``id``.
            description: Optional free-text description of the flag.
            values: Optional list of allowed values constraining what the flag may
                serve. When omitted, the flag is unconstrained.

        Returns:
            An unsaved :class:`AsyncNumberFlag`; call ``await save()`` to persist it.
        """
        return AsyncNumberFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="NUMERIC",
            default=default,
            values=values,
            description=description,
        )

    def new_json_flag(
        self,
        id: str,
        *,
        default: dict[str, Any],
        name: str | None = None,
        description: str | None = None,
        values: list[FlagValue] | None = None,
    ) -> AsyncJsonFlag:
        """Return a new unsaved :class:`AsyncJsonFlag`. Call ``await save()`` to persist.

        Args:
            id: Stable flag identifier. Unique per account.
            default: Value served when no environment override or rule applies.
            name: Human-readable display name. Defaults to a title-cased form of
                ``id``.
            description: Optional free-text description of the flag.
            values: Optional list of allowed values constraining what the flag may
                serve. When omitted, the flag is unconstrained.

        Returns:
            An unsaved :class:`AsyncJsonFlag`; call ``await save()`` to persist it.
        """
        return AsyncJsonFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="JSON",
            default=default,
            values=values,
            description=description,
        )

    async def get(self, id: str) -> AsyncFlag:
        """Fetch the editable :class:`AsyncFlag` resource by id. Awaited.

        Args:
            id: Identifier of the flag to fetch.

        Returns:
            The :class:`AsyncFlag`, ready to mutate and ``await save()``.

        Raises:
            NotFoundError: No flag with that id exists for the account.
        """
        try:
            response = await get_flag.asyncio_detailed(id, client=self._flags_http)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._flags_http._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        body = json.loads(response.content)
        return self._model_from_json(body["data"])

    async def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[AsyncFlag]:
        """List flags for the authenticated account. Awaited.

        Args:
            page_number: 1-based page index to fetch. When omitted, the server
                default applies.
            page_size: Number of flags per page. When omitted, the server default
                applies.

        Returns:
            The flags on the requested page as a list of :class:`AsyncFlag`.
        """
        kwargs = _pagination_kwargs(page_number, page_size)
        try:
            response = await list_flags.asyncio_detailed(client=self._flags_http, **kwargs)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._flags_http._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        body = json.loads(response.content)
        return [self._model_from_json(r) for r in body.get("data", [])]

    async def delete(self, id: str) -> None:
        """Delete a flag by id. Awaited.

        Args:
            id: Identifier of the flag to delete.

        Raises:
            NotFoundError: No flag with that id exists for the account.
        """
        try:
            response = await delete_flag.asyncio_detailed(id, client=self._flags_http)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._flags_http._base_url)
            raise
        _check_response_status(response.status_code, response.content)

    async def _create_flag(self, flag: AsyncFlag) -> AsyncFlag:
        body = _build_flag_request_body(flag, flag_id=flag.id)
        try:
            response = await create_flag.asyncio_detailed(client=self._flags_http, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._flags_http._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        resp_body = json.loads(response.content)
        return self._model_from_json(resp_body["data"])

    async def _update_flag(self, *, flag: AsyncFlag) -> AsyncFlag:
        body = _build_flag_request_body(flag, flag_id=flag.id)
        try:
            response = await update_flag.asyncio_detailed(flag.id, client=self._flags_http, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._flags_http._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        resp_body = json.loads(response.content)
        return self._model_from_json(resp_body["data"])

    def _model_from_json(self, data: dict[str, Any]) -> AsyncFlag:
        d = _flag_dict_from_json(data)
        return AsyncFlag(self, **d)

    # ------------------------------------------------------------------
    # Management surface: discovery buffer (owned directly)
    # ------------------------------------------------------------------

    def register(
        self,
        items: FlagDeclaration | list[FlagDeclaration],
    ) -> None:
        """Buffer flag declarations for bulk-discovery upload.  Call ``await flush()`` to send.

        Unlike the sync client's ``register``, this method has no ``flush``
        parameter: the async client offers no synchronous flush path, so always
        ``await flush()`` to send the buffered declarations. Until then they stay
        buffered and are sent on the next flush — automatic once the buffer reaches
        its batch size, or on the first live call.

        Args:
            items: A single :class:`FlagDeclaration` or a list of them to queue.
        """
        batch = items if isinstance(items, list) else [items]
        for d in batch:
            self._buffer.add(d.id, d.type, d.default, d.service, d.environment)
        if self._buffer.pending_count >= _FLAG_BATCH_FLUSH_SIZE:
            threading.Thread(target=self._threshold_flush_sync, daemon=True).start()

    def _threshold_flush_sync(self) -> None:
        try:
            self.flush_sync()
        except Exception as exc:
            logger.warning("Flag registration flush failed: %s", exc)

    async def flush(self) -> None:
        """POST pending declarations to the flags bulk endpoint (async).

        Items remain in the buffer until the request succeeds; failed
        flushes are retried by the next ``flush()`` call.
        """
        batch = self._buffer.peek()
        body = _build_flag_bulk_request(batch)
        if body is None:
            return
        try:
            response = await bulk_register_flags.asyncio_detailed(client=self._flags_http, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._flags_http._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        self._buffer.commit([b["id"] for b in batch])

    def flush_sync(self) -> None:
        """Synchronous flush from a background thread (final flush, threshold flush)."""
        batch = self._buffer.peek()
        body = _build_flag_bulk_request(batch)
        if body is None:
            return
        try:
            response = bulk_register_flags.sync_detailed(client=self._flags_http, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._flags_http._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        self._buffer.commit([b["id"] for b in batch])

    @property
    def pending_count(self) -> int:
        """Number of pending flag declarations awaiting flush."""
        return self._buffer.pending_count

    def _observe_declaration(self, flag_id: str, flag_type: str, default: Any) -> None:
        """Queue a declared flag with the owned discovery buffer."""
        from smplkit.flags.types import FlagDeclaration

        self.register(
            FlagDeclaration(
                id=flag_id,
                type=flag_type,
                default=default,
                service=self._service,
                environment=self._environment,
            )
        )

    # ------------------------------------------------------------------
    # Live surface: lazy connect + transport / WebSocket helpers
    # ------------------------------------------------------------------

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

    async def _ensure_connected(self) -> None:
        """Open the live connection to the running Smpl Flags service (async).

        See :meth:`FlagsClient._ensure_connected` for the full contract.
        Idempotent and internal — the awaitable live methods call it on first
        use, so the live surface auto-connects with no explicit step.
        """
        if self._parent is not None:
            self._parent._ensure_started()
        if self._connected:
            return

        try:
            await self.flush()
        except Exception as exc:
            logger.warning("Flags discovery flush before connect failed: %s", exc)

        await self._fetch_all_flags()
        self._cache.clear()
        self._connected = True

        self._ws_manager = self._ensure_ws()
        if not self._ws_subscribed:
            self._ws_manager.on("flag_changed", self._handle_flag_changed)
            self._ws_manager.on("flag_deleted", self._handle_flag_deleted)
            self._ws_manager.on("flags_changed", self._handle_flags_changed)
            self._ws_subscribed = True

    # ------------------------------------------------------------------
    # Live surface: typed flag handles
    # ------------------------------------------------------------------

    def boolean_flag(self, id: str, *, default: bool) -> AsyncBooleanFlag:
        """Declare a boolean flag handle for live evaluation.

        Synchronous; warm the cache via ``await refresh()`` /
        ``await client.wait_until_ready()`` for live values.

        Args:
            id: Identifier of the flag to evaluate.
            default: Value returned by ``handle.get()`` when the flag is unknown or
                no environment override or rule applies.

        Returns:
            An :class:`AsyncBooleanFlag` handle whose ``get()`` evaluates against the
            live cache.
        """
        handle = AsyncBooleanFlag(self, id=id, name=id, type="BOOLEAN", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "BOOLEAN", default)
        return handle

    def string_flag(self, id: str, *, default: str) -> AsyncStringFlag:
        """Declare a string flag handle for live evaluation.

        Synchronous; warm the cache via ``await refresh()`` /
        ``await client.wait_until_ready()`` for live values.

        Args:
            id: Identifier of the flag to evaluate.
            default: Value returned by ``handle.get()`` when the flag is unknown or
                no environment override or rule applies.

        Returns:
            An :class:`AsyncStringFlag` handle whose ``get()`` evaluates against the
            live cache.
        """
        handle = AsyncStringFlag(self, id=id, name=id, type="STRING", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "STRING", default)
        return handle

    def number_flag(self, id: str, *, default: int | float) -> AsyncNumberFlag:
        """Declare a numeric flag handle for live evaluation.

        Synchronous; warm the cache via ``await refresh()`` /
        ``await client.wait_until_ready()`` for live values.

        Args:
            id: Identifier of the flag to evaluate.
            default: Value returned by ``handle.get()`` when the flag is unknown or
                no environment override or rule applies.

        Returns:
            An :class:`AsyncNumberFlag` handle whose ``get()`` evaluates against the
            live cache.
        """
        handle = AsyncNumberFlag(self, id=id, name=id, type="NUMERIC", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "NUMERIC", default)
        return handle

    def json_flag(self, id: str, *, default: dict[str, Any]) -> AsyncJsonFlag:
        """Declare a JSON flag handle for live evaluation.

        Synchronous; warm the cache via ``await refresh()`` /
        ``await client.wait_until_ready()`` for live values.

        Args:
            id: Identifier of the flag to evaluate.
            default: Value returned by ``handle.get()`` when the flag is unknown or
                no environment override or rule applies.

        Returns:
            An :class:`AsyncJsonFlag` handle whose ``get()`` evaluates against the
            live cache.
        """
        handle = AsyncJsonFlag(self, id=id, name=id, type="JSON", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "JSON", default)
        return handle

    # ------------------------------------------------------------------
    # Live surface: refresh / stats / change listeners
    # ------------------------------------------------------------------

    async def refresh(self) -> None:
        """Re-fetch all flag definitions and clear cache (async).

        Connects lazily on first use — no explicit install step.
        """
        await self._ensure_connected()
        await self._fetch_all_flags()
        self._cache.clear()
        self._fire_change_listeners_all("manual")

    def stats(self) -> FlagStats:
        """Return evaluation statistics.

        Synchronous; reflects evaluations performed so far.
        """
        return FlagStats(cache_hits=self._cache.cache_hits, cache_misses=self._cache.cache_misses)

    def on_change(self, fn_or_id: Callable[[FlagChangeEvent], None] | str | None = None) -> Any:
        """Register a change listener (global or id-scoped).

        Synchronous; only records the listener. Open the live connection
        first via an awaitable live method or ``client.wait_until_ready()``
        so events flow.

        Args:
            fn_or_id: Either the listener callable (used directly as
                ``@on_change``), or a flag id string scoping the listener to that
                flag (used as ``@on_change("flag-id")``). When ``None``, returns a
                decorator that registers a global listener.

        Returns:
            The listener callable when one is passed directly, otherwise a decorator
            that registers the callable it wraps. Each listener receives a
            :class:`FlagChangeEvent`.
        """
        if callable(fn_or_id):
            self._global_listeners.append(fn_or_id)
            return fn_or_id
        elif isinstance(fn_or_id, str):
            flag_id = fn_or_id

            def decorator(fn: Callable[[FlagChangeEvent], None]) -> Callable[[FlagChangeEvent], None]:
                self._key_listeners.setdefault(flag_id, []).append(fn)
                return fn

            return decorator
        else:

            def decorator(fn: Callable[[FlagChangeEvent], None]) -> Callable[[FlagChangeEvent], None]:
                self._global_listeners.append(fn)
                return fn

            return decorator

    # ------------------------------------------------------------------
    # Internal: evaluation
    # ------------------------------------------------------------------

    def _evaluate_handle(self, flag_id: str, default: Any, context: list[Context] | None) -> Any:
        """Core evaluation used by flag handles.

        Note: This is synchronous so it can be called from the WebSocket
        background thread.  It reads from the already-populated store; the
        async ``install`` performs the initial fetch.
        """
        if context is not None:
            # Explicit context: register here.  (Implicit set_context registers
            # at the entry point, so the contextvar branch below doesn't need to.)
            if self._contexts is not None:
                self._contexts.register(context)
            eval_dict = _contexts_to_eval_dict(context)
        else:
            contexts = _get_request_context()
            eval_dict = _contexts_to_eval_dict(contexts) if contexts else {}

        if self._service and "service" not in eval_dict:
            eval_dict["service"] = {"key": self._service}

        ctx_hash = _hash_context(eval_dict)
        cache_key = f"{flag_id}:{ctx_hash}"

        hit, cached_value = self._cache.get(cache_key)
        if hit:
            metrics = self._metrics
            if metrics is not None:
                metrics.record("flags.cache_hits", unit="hits")
                metrics.record("flags.evaluations", unit="evaluations", dimensions={"flag": flag_id})
            return cached_value

        flag_def = self._flag_store.get(flag_id)
        if flag_def is None:
            self._cache.put(cache_key, default)
            return default

        value = _evaluate_flag(flag_def, self._environment, eval_dict)
        if value is None:
            value = default

        self._cache.put(cache_key, value)
        metrics = self._metrics
        if metrics is not None:
            metrics.record("flags.cache_misses", unit="misses")
            metrics.record("flags.evaluations", unit="evaluations", dimensions={"flag": flag_id})
        return value

    # ------------------------------------------------------------------
    # Internal: flag store
    # ------------------------------------------------------------------

    async def _fetch_all_flags(self) -> None:
        flags = await self._fetch_flags_list()
        self._flag_store = {f["id"]: f for f in flags}

    async def _fetch_flags_list(self) -> list[dict[str, Any]]:
        async def fetch_page(page_number: int, page_size: int) -> list[dict[str, Any]]:
            try:
                response = await list_flags.asyncio_detailed(
                    client=self._flags_http,
                    pagenumber=page_number,
                    pagesize=page_size,
                )
            except Exception as exc:
                _maybe_reraise_network_error(exc, self._flags_http._base_url)
                raise
            _check_response_status(response.status_code, response.content)
            body = json.loads(response.content)
            return [_store_entry(_flag_dict_from_json(r)) for r in body.get("data", [])]

        return await paginate_async(fetch_page)

    def _fetch_all_flags_sync(self) -> None:
        """Sync fetch (used from WS event handlers, which run on a sync thread)."""

        def fetch_page(page_number: int, page_size: int) -> list[dict[str, Any]]:
            try:
                response = list_flags.sync_detailed(
                    client=self._flags_http,
                    pagenumber=page_number,
                    pagesize=page_size,
                )
            except Exception as exc:
                _maybe_reraise_network_error(exc, self._flags_http._base_url)
                raise
            _check_response_status(response.status_code, response.content)
            body = json.loads(response.content)
            return [_store_entry(_flag_dict_from_json(r)) for r in body.get("data", [])]

        self._flag_store = {f["id"]: f for f in paginate_sync(fetch_page)}

    def _fetch_flag_single_data_sync(self, key: str) -> dict[str, Any]:
        """Sync fetch of a single flag by key (used from WS event handlers)."""
        try:
            response = get_flag.sync_detailed(key, client=self._flags_http)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._flags_http._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        body = json.loads(response.content)
        d = _flag_dict_from_json(body["data"])
        return _store_entry(d)

    # ------------------------------------------------------------------
    # Internal: event handlers (called by SharedWebSocket)
    # ------------------------------------------------------------------

    def _handle_flag_changed(self, data: dict[str, Any]) -> None:
        key = data.get("id")
        if not key:
            return
        pre = dict(self._flag_store.get(key, {}))
        try:
            new_data = self._fetch_flag_single_data_sync(key)
        except Exception:
            ws_logger.error("Failed to fetch flag %r after WS event", key, exc_info=True)
            return
        self._flag_store[key] = new_data
        self._cache.clear()
        if pre != new_data:
            self._fire_change_listeners(key, "websocket")

    def _handle_flag_deleted(self, data: dict[str, Any]) -> None:
        key = data.get("id")
        if not key:
            return
        existed = key in self._flag_store
        self._flag_store.pop(key, None)
        self._cache.clear()
        if existed:
            self._fire_change_listeners(key, "websocket", deleted=True)

    def _handle_flags_changed(self, data: dict[str, Any]) -> None:
        pre_store = dict(self._flag_store)
        try:
            self._fetch_all_flags_sync()
        except Exception:
            ws_logger.error("Failed to refresh flags after flags_changed WS event", exc_info=True)
            return
        self._cache.clear()
        post_store = self._flag_store
        all_keys = set(pre_store) | set(post_store)
        changed = [k for k in all_keys if pre_store.get(k) != post_store.get(k)]
        if not changed:
            return
        first_event = FlagChangeEvent(id=changed[0], source="websocket")
        for cb in self._global_listeners:
            try:
                cb(first_event)
            except Exception:
                logger.error("Exception in global flags on_change listener", exc_info=True)
        for k in changed:
            deleted = k in pre_store and k not in post_store
            event = FlagChangeEvent(id=k, source="websocket", deleted=deleted)
            for cb in self._key_listeners.get(k, []):
                try:
                    cb(event)
                except Exception:
                    logger.error("Exception in id-scoped flags on_change listener", exc_info=True)

    def _fire_change_listeners(self, flag_id: str | None, source: str, *, deleted: bool = False) -> None:
        if flag_id:
            event = FlagChangeEvent(id=flag_id, source=source, deleted=deleted)
            for cb in self._global_listeners:
                try:
                    cb(event)
                except Exception:
                    logger.error("Exception in global flags on_change listener", exc_info=True)
            for cb in self._key_listeners.get(flag_id, []):
                try:
                    cb(event)
                except Exception:
                    logger.error("Exception in id-scoped flags on_change listener", exc_info=True)

    def _fire_change_listeners_all(self, source: str) -> None:
        for flag_id in self._flag_store:
            self._fire_change_listeners(flag_id, source)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def aclose(self) -> None:
        """Release async resources — only those this client owns.

        Tears down the owned WebSocket (standalone install) and the owned
        async HTTP transports (standalone construction). A wired client
        borrows the parent's transport, WebSocket, and contexts client and
        closes none of them.
        """
        if self._owns_ws and self._ws_manager is not None:
            self._ws_manager.stop()
            self._ws_manager = None
            self._owns_ws = False
        if self._owns_transport:
            ac = self._flags_http._async_client
            if ac is not None:
                await ac.aclose()
                self._flags_http._async_client = None
            if self._owns_contexts:
                app_ac = self._app_http_standalone._async_client
                if app_ac is not None:
                    await app_ac.aclose()
                    self._app_http_standalone._async_client = None

    async def __aenter__(self) -> AsyncFlagsClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()


# ---------------------------------------------------------------------------
# Flag store entry shaping
# ---------------------------------------------------------------------------


def _store_entry(d: dict[str, Any]) -> dict[str, Any]:
    """Shape a parsed flag dict into the runtime store format."""
    return {
        "id": d["id"],
        "name": d["name"],
        "type": d["type"],
        "default": d["default"],
        "values": d["values"],
        "description": d["description"],
        "environments": d["environments"],
    }


# ---------------------------------------------------------------------------
# JSON Logic evaluation
# ---------------------------------------------------------------------------


def _evaluate_flag(flag_def: dict[str, Any], environment: str | None, eval_dict: dict[str, Any]) -> Any:
    """Evaluate a flag definition against the given context.

    1. Look up the environment.  If missing, return flag-level default.
    2. If disabled, return env default or flag default.
    3. Iterate rules; first match wins.
    4. No match → env default or flag default.
    """
    from json_logic import jsonLogic

    flag_default = flag_def.get("default")
    environments = flag_def.get("environments", {})

    if environment is None or environment not in environments:
        return flag_default

    env_config = environments[environment]
    fallback = env_config.default if env_config.default is not None else flag_default

    if not env_config.enabled:
        return fallback

    for rule in env_config.rules:
        if not rule.logic:
            continue
        try:
            result = jsonLogic(rule.logic, eval_dict)
            if result:
                return rule.value
        except Exception:
            logger.warning("JSON Logic evaluation error for rule %r", rule, exc_info=True)
            continue

    return fallback
