"""FlagsClient and AsyncFlagsClient — runtime evaluation for Smpl Flags.

Runtime: declare typed handles, evaluate via JSON Logic, cache
results, and react to live updates over a shared WebSocket. CRUD has
moved to :class:`smplkit.SmplManagementClient` (``mgmt.flags.*``).
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import logging
import threading
import time
import traceback
from collections import OrderedDict
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from smplkit._context import get_context as _get_request_context
from smplkit._debug import debug
from smplkit._errors import (
    ConnectionError,
    NotFoundError,
    TimeoutError,
    ValidationError,
    _raise_for_status,
)
from smplkit._helpers import paginate_async, paginate_sync
from smplkit._generated.flags.api.flags import (  # noqa: F401  (re-exported)
    bulk_register_flags,
    create_flag,
    delete_flag,
    get_flag,
    list_flags,
    update_flag,
)
from smplkit._generated.flags.client import AuthenticatedClient
from smplkit.flags.helpers import _flag_dict_from_json
from smplkit.flags.models import (
    AsyncBooleanFlag,
    AsyncFlag,
    AsyncJsonFlag,
    AsyncNumberFlag,
    AsyncStringFlag,
    BooleanFlag,
    Flag,
    JsonFlag,
    NumberFlag,
    StringFlag,
)

if TYPE_CHECKING:
    from smplkit._metrics import _AsyncMetricsReporter, _MetricsReporter
    from smplkit._ws import SharedWebSocket
    from smplkit.client import AsyncSmplClient, SmplClient
    from smplkit.flags.types import Context
    from smplkit.management.client import AsyncSmplManagementClient, SmplManagementClient

logger = logging.getLogger("smplkit")
ws_logger = logging.getLogger("smplkit.flags.ws")

_DEFAULT_FLAGS_BASE_URL = "https://flags.smplkit.com"
_DEFAULT_APP_BASE_URL = "https://app.smplkit.com"
_CACHE_MAX_SIZE = 10_000
# Backoff for ``start()`` retries when the flags-service is unhealthy.
_INITIAL_START_RETRY_DELAY = 1.0
_MAX_START_RETRY_DELAY = 60.0


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
    """Synchronous flags runtime namespace.

    Obtained via ``SmplClient(...).flags``. Exposes typed handles
    (``boolean_flag``/``string_flag``/``number_flag``/``json_flag``) and
    runtime control (``refresh``, ``stats``, ``on_change``). CRUD has moved
    to ``mgmt.flags.*``.  Per-request context is set via
    ``client.set_context([...])``.
    """

    def __init__(
        self,
        parent: SmplClient,
        *,
        manage: SmplManagementClient,
        metrics: _MetricsReporter | None,
        flags_base_url: str = _DEFAULT_FLAGS_BASE_URL,
        app_base_url: str = _DEFAULT_APP_BASE_URL,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        self._parent = parent
        self._manage = manage
        self._metrics = metrics
        self._service = parent._service
        self._environment = parent._environment
        self._flags_http = AuthenticatedClient(
            base_url=flags_base_url,
            token=parent._api_key,
            headers={**(extra_headers or {})},
        )

        # Runtime state
        self._flag_store: dict[str, dict[str, Any]] = {}
        self._connected = False
        self._ws_subscribed = False
        self._next_start_attempt_at = 0.0
        self._start_retry_delay = _INITIAL_START_RETRY_DELAY
        self._cache = _ResolutionCache()
        self._handles: dict[str, Flag] = {}
        self._global_listeners: list[Callable[[FlagChangeEvent], None]] = []
        self._key_listeners: dict[str, list[Callable[[FlagChangeEvent], None]]] = {}

        # Shared WebSocket (set during connect)
        self._ws_manager: SharedWebSocket | None = None

    def _close(self) -> None:
        """Release resources held by this client."""

    # ------------------------------------------------------------------
    # Runtime: typed flag handles
    # ------------------------------------------------------------------

    def _observe_declaration(self, flag_id: str, flag_type: str, default: Any) -> None:
        """Queue a declared flag with mgmt for bulk registration."""
        from smplkit.flags.types import FlagDeclaration

        self._manage.flags.register(
            FlagDeclaration(
                id=flag_id,
                type=flag_type,
                default=default,
                service=self._service,
                environment=self._environment,
            )
        )

    def boolean_flag(self, id: str, *, default: bool) -> BooleanFlag:
        """Declare a boolean flag handle for runtime evaluation."""
        handle = BooleanFlag(self, id=id, name=id, type="BOOLEAN", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "BOOLEAN", default)
        return handle

    def string_flag(self, id: str, *, default: str) -> StringFlag:
        """Declare a string flag handle for runtime evaluation."""
        handle = StringFlag(self, id=id, name=id, type="STRING", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "STRING", default)
        return handle

    def number_flag(self, id: str, *, default: int | float) -> NumberFlag:
        """Declare a numeric flag handle for runtime evaluation."""
        handle = NumberFlag(self, id=id, name=id, type="NUMERIC", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "NUMERIC", default)
        return handle

    def json_flag(self, id: str, *, default: dict[str, Any]) -> JsonFlag:
        """Declare a JSON flag handle for runtime evaluation."""
        handle = JsonFlag(self, id=id, name=id, type="JSON", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "JSON", default)
        return handle

    # ------------------------------------------------------------------
    # Runtime: connect / refresh
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Eagerly initialize the flags subclient.

        Flushes any pending flag-declaration buffer, fetches all flag
        definitions, opens the shared WebSocket and subscribes to
        ``flag_changed`` / ``flag_deleted`` / ``flags_changed`` events.

        Idempotent — safe to call multiple times.  Called automatically
        on first ``flag.get()`` evaluation if not invoked manually.

        If the flags-service is unhealthy (e.g. a coordinated rebuild
        where the app pod starts before the schema is loaded), the flush
        or refresh will fail.  Pending declarations stay queued, the
        client remains *not connected*, and the next call retries after
        an exponentially backed-off delay (capped at
        ``_MAX_START_RETRY_DELAY`` seconds).  Evaluations during that
        window fall back to handle defaults rather than raising.
        """
        if self._connected:
            return
        if time.monotonic() < self._next_start_attempt_at:
            return
        self._environment = self._parent._environment

        try:
            # Flush discovered flags BEFORE fetching definitions so the
            # fetch reflects them.  Items remain in the mgmt buffer until
            # the POST succeeds.
            self._flush_flags_sync()
            # Fetch + cache + fire change listeners
            self.refresh()
        except Exception as exc:
            self._schedule_start_retry(exc)
            return

        self._connected = True
        self._start_retry_delay = _INITIAL_START_RETRY_DELAY
        self._next_start_attempt_at = 0.0

        # Register on the shared WebSocket — only once across retry attempts.
        self._ws_manager = self._parent._ensure_ws()
        if not self._ws_subscribed:
            self._ws_manager.on("flag_changed", self._handle_flag_changed)
            self._ws_manager.on("flag_deleted", self._handle_flag_deleted)
            self._ws_manager.on("flags_changed", self._handle_flags_changed)
            self._ws_subscribed = True

    def _schedule_start_retry(self, exc: Exception) -> None:
        """Back off the next ``start()`` attempt after a failure."""
        delay = self._start_retry_delay
        self._next_start_attempt_at = time.monotonic() + delay
        self._start_retry_delay = min(delay * 2, _MAX_START_RETRY_DELAY)
        logger.warning("Flags client start failed (will retry in %.1fs): %s", delay, exc)
        debug("registration", traceback.format_exc().strip())

    def refresh(self) -> None:
        """Re-fetch all flag definitions and clear cache."""
        self._fetch_all_flags()
        self._cache.clear()
        self._fire_change_listeners_all("manual")

    def stats(self) -> FlagStats:
        return FlagStats(cache_hits=self._cache.cache_hits, cache_misses=self._cache.cache_misses)

    # ------------------------------------------------------------------
    # Runtime: change listeners (dual-mode decorator)
    # ------------------------------------------------------------------

    def on_change(self, fn_or_id: Callable[[FlagChangeEvent], None] | str | None = None) -> Any:
        """Register a change listener.

        Supports two forms:

        - ``@client.flags.on_change`` — registers a global listener.
        - ``@client.flags.on_change("flag-id")`` — registers an id-scoped listener.
        """
        if callable(fn_or_id):
            # @on_change (bare decorator)
            self._global_listeners.append(fn_or_id)
            return fn_or_id
        elif isinstance(fn_or_id, str):
            # @on_change("id")
            flag_id = fn_or_id

            def decorator(fn: Callable[[FlagChangeEvent], None]) -> Callable[[FlagChangeEvent], None]:
                self._key_listeners.setdefault(flag_id, []).append(fn)
                return fn

            return decorator
        else:
            # @on_change() — called with parens but no args

            def decorator(fn: Callable[[FlagChangeEvent], None]) -> Callable[[FlagChangeEvent], None]:
                self._global_listeners.append(fn)
                return fn

            return decorator

    # ------------------------------------------------------------------
    # Internal: flag registration flush (one-shot, used during start())
    # ------------------------------------------------------------------

    def _flush_flags_sync(self) -> None:
        """Flush the flag registration buffer (delegates to mgmt.flags).

        Re-raises on failure so ``start()`` can decide whether to retry.
        Items stay in the mgmt buffer until a successful flush, so this
        is safe to call repeatedly.
        """
        self._manage.flags.flush()

    # ------------------------------------------------------------------
    # Internal: evaluation
    # ------------------------------------------------------------------

    def _evaluate_handle(self, flag_id: str, default: Any, context: list[Context] | None) -> Any:
        """Core evaluation used by flag handles.  Lazily connects on first call."""
        if not self._connected:
            self.start()

        if context is not None:
            # Explicit context: register here.  (Implicit set_context registers
            # at the entry point, so the contextvar branch below doesn't need to.)
            self._manage.contexts.register(context)
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
        return {
            "id": d["id"],
            "name": d["name"],
            "type": d["type"],
            "default": d["default"],
            "values": d["values"],
            "description": d["description"],
            "environments": d["environments"],
        }

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
            result = []
            for r in body.get("data", []):
                d = _flag_dict_from_json(r)
                result.append(
                    {
                        "id": d["id"],
                        "name": d["name"],
                        "type": d["type"],
                        "default": d["default"],
                        "values": d["values"],
                        "description": d["description"],
                        "environments": d["environments"],
                    }
                )
            return result

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


# ---------------------------------------------------------------------------
# AsyncFlagsClient
# ---------------------------------------------------------------------------


class AsyncFlagsClient:
    """Asynchronous flags runtime namespace.  Obtained via ``AsyncSmplClient(...).flags``.

    CRUD has moved to ``AsyncSmplManagementClient.flags`` (``mgmt.flags.*``).
    """

    def __init__(
        self,
        parent: AsyncSmplClient,
        *,
        manage: AsyncSmplManagementClient,
        metrics: _AsyncMetricsReporter | None,
        flags_base_url: str = _DEFAULT_FLAGS_BASE_URL,
        app_base_url: str = _DEFAULT_APP_BASE_URL,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        self._parent = parent
        self._manage = manage
        self._metrics = metrics
        self._service = parent._service
        self._environment = parent._environment
        self._flags_http = AuthenticatedClient(
            base_url=flags_base_url,
            token=parent._api_key,
            headers={**(extra_headers or {})},
        )

        # Runtime state
        self._flag_store: dict[str, dict[str, Any]] = {}
        self._connected = False
        self._ws_subscribed = False
        self._next_start_attempt_at = 0.0
        self._start_retry_delay = _INITIAL_START_RETRY_DELAY
        self._cache = _ResolutionCache()
        self._handles: dict[str, AsyncFlag] = {}
        self._global_listeners: list[Callable[[FlagChangeEvent], None]] = []
        self._key_listeners: dict[str, list[Callable[[FlagChangeEvent], None]]] = {}

        # Shared WebSocket (set during connect)
        self._ws_manager: SharedWebSocket | None = None

    def _close(self) -> None:
        """Release resources held by this client."""

    # ------------------------------------------------------------------
    # Runtime: typed flag handles
    # ------------------------------------------------------------------

    def _observe_declaration(self, flag_id: str, flag_type: str, default: Any) -> None:
        """Queue a declared flag with mgmt for bulk registration."""
        from smplkit.flags.types import FlagDeclaration

        self._manage.flags.register(
            FlagDeclaration(
                id=flag_id,
                type=flag_type,
                default=default,
                service=self._service,
                environment=self._environment,
            )
        )

    def boolean_flag(self, id: str, *, default: bool) -> AsyncBooleanFlag:
        handle = AsyncBooleanFlag(self, id=id, name=id, type="BOOLEAN", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "BOOLEAN", default)
        return handle

    def string_flag(self, id: str, *, default: str) -> AsyncStringFlag:
        handle = AsyncStringFlag(self, id=id, name=id, type="STRING", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "STRING", default)
        return handle

    def number_flag(self, id: str, *, default: int | float) -> AsyncNumberFlag:
        handle = AsyncNumberFlag(self, id=id, name=id, type="NUMERIC", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "NUMERIC", default)
        return handle

    def json_flag(self, id: str, *, default: dict[str, Any]) -> AsyncJsonFlag:
        handle = AsyncJsonFlag(self, id=id, name=id, type="JSON", default=default)
        self._handles[id] = handle
        self._observe_declaration(id, "JSON", default)
        return handle

    # ------------------------------------------------------------------
    # Runtime: connect / refresh
    # ------------------------------------------------------------------

    async def start(self) -> None:
        """Eagerly initialize the flags subclient.

        Flushes any pending flag-declaration buffer, fetches all flag
        definitions, opens the shared WebSocket and subscribes to
        ``flag_changed`` / ``flag_deleted`` / ``flags_changed`` events.

        Idempotent.  Called automatically on first ``flag.get()``.

        On failure (e.g. flags-service unhealthy), pending declarations
        stay queued, the client remains *not connected*, and the next
        call retries after an exponentially backed-off delay.
        """
        if self._connected:
            return
        if time.monotonic() < self._next_start_attempt_at:
            return
        self._environment = self._parent._environment

        try:
            # Flush discovered flags BEFORE fetching definitions so the
            # fetch reflects them.  Items remain in the mgmt buffer until
            # the POST succeeds.
            await self._flush_flags_async()
            # Fetch + cache + fire change listeners
            await self.refresh()
        except Exception as exc:
            self._schedule_start_retry(exc)
            return

        self._connected = True
        self._start_retry_delay = _INITIAL_START_RETRY_DELAY
        self._next_start_attempt_at = 0.0

        self._ws_manager = self._parent._ensure_ws()
        if not self._ws_subscribed:
            self._ws_manager.on("flag_changed", self._handle_flag_changed)
            self._ws_manager.on("flag_deleted", self._handle_flag_deleted)
            self._ws_manager.on("flags_changed", self._handle_flags_changed)
            self._ws_subscribed = True

    def _schedule_start_retry(self, exc: Exception) -> None:
        """Back off the next ``start()`` attempt after a failure."""
        delay = self._start_retry_delay
        self._next_start_attempt_at = time.monotonic() + delay
        self._start_retry_delay = min(delay * 2, _MAX_START_RETRY_DELAY)
        logger.warning("Flags client start failed (will retry in %.1fs): %s", delay, exc)
        debug("registration", traceback.format_exc().strip())

    async def refresh(self) -> None:
        """Re-fetch all flag definitions and clear cache."""
        await self._fetch_all_flags()
        self._cache.clear()
        self._fire_change_listeners_all("manual")

    def stats(self) -> FlagStats:
        return FlagStats(cache_hits=self._cache.cache_hits, cache_misses=self._cache.cache_misses)

    # ------------------------------------------------------------------
    # Runtime: change listeners (dual-mode decorator)
    # ------------------------------------------------------------------

    def on_change(self, fn_or_id: Callable[[FlagChangeEvent], None] | str | None = None) -> Any:
        """Register a change listener (global or id-scoped)."""
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
    # Internal: context registration flush (delegates to mgmt.contexts)
    # ------------------------------------------------------------------

    async def _flush_contexts_async(self) -> None:
        try:
            await self._manage.contexts.flush()
        except Exception:
            logger.warning("Context registration flush failed", exc_info=True)

    # ------------------------------------------------------------------
    # Runtime: flag registration flush
    # ------------------------------------------------------------------

    async def _flush_flags_async(self) -> None:
        """Flush the flag registration buffer (delegates to mgmt.flags).

        Re-raises on failure so ``start()`` can decide whether to retry.
        Items stay queued in the mgmt buffer until a successful flush.
        """
        await self._manage.flags.flush()

    def _flush_flags_sync(self) -> None:
        """Flush the flag registration buffer (delegates to mgmt.flags).

        Re-raises on failure so the lazy-init path in
        ``_evaluate_handle`` can decide whether to retry.
        """
        self._manage.flags.flush_sync()

    # ------------------------------------------------------------------
    # Internal: evaluation
    # ------------------------------------------------------------------

    def _evaluate_handle(self, flag_id: str, default: Any, context: list[Context] | None) -> Any:
        """Core evaluation used by flag handles.  Lazily connects on first call.

        Note: This is synchronous.  The async client's start is
        async, so we use sync HTTP calls for the initial fetch (called from
        the WebSocket background thread as well).
        """
        if not self._connected and time.monotonic() >= self._next_start_attempt_at:
            # Lazy init using sync HTTP (safe from any thread).  Mirrors
            # the backoff/retain-on-failure semantics of ``start()``.
            self._environment = self._parent._environment
            try:
                self._flush_flags_sync()
                self._fetch_all_flags_sync()
            except Exception as exc:
                self._schedule_start_retry(exc)
            else:
                self._connected = True
                self._start_retry_delay = _INITIAL_START_RETRY_DELAY
                self._next_start_attempt_at = 0.0
                self._cache.clear()
                self._ws_manager = self._parent._ensure_ws()
                if not self._ws_subscribed:
                    self._ws_manager.on("flag_changed", self._handle_flag_changed)
                    self._ws_manager.on("flag_deleted", self._handle_flag_deleted)
                    self._ws_manager.on("flags_changed", self._handle_flags_changed)
                    self._ws_subscribed = True

        if context is not None:
            # Explicit context: register here.  (Implicit set_context registers
            # at the entry point, so the contextvar branch below doesn't need to.)
            self._manage.contexts.register(context)
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
            result = []
            for r in body.get("data", []):
                d = _flag_dict_from_json(r)
                result.append(
                    {
                        "id": d["id"],
                        "name": d["name"],
                        "type": d["type"],
                        "default": d["default"],
                        "values": d["values"],
                        "description": d["description"],
                        "environments": d["environments"],
                    }
                )
            return result

        return await paginate_async(fetch_page)

    def _fetch_all_flags_sync(self) -> None:
        """Sync fetch for lazy init from _evaluate_handle."""

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
            page_rows: list[dict[str, Any]] = []
            for r in body.get("data", []):
                d = _flag_dict_from_json(r)
                page_rows.append(
                    {
                        "id": d["id"],
                        "name": d["name"],
                        "type": d["type"],
                        "default": d["default"],
                        "values": d["values"],
                        "description": d["description"],
                        "environments": d["environments"],
                    }
                )
            return page_rows

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
        return {
            "id": d["id"],
            "name": d["name"],
            "type": d["type"],
            "default": d["default"],
            "values": d["values"],
            "description": d["description"],
            "environments": d["environments"],
        }

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


# ---------------------------------------------------------------------------
# JSON Logic evaluation
# ---------------------------------------------------------------------------


def _evaluate_flag(flag_def: dict[str, Any], environment: str | None, eval_dict: dict[str, Any]) -> Any:
    """Evaluate a flag definition against the given context.

    Follows ADR-022 §2.6 semantics:
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
