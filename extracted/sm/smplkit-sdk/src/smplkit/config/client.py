"""ConfigClient and AsyncConfigClient — runtime operations for configs.

Runtime config operations: lazy-fetch all configs for the SDK's
current environment, resolve values down the inheritance chain, and
emit change events when the server's WebSocket signals a refresh.
CRUD lives on :class:`smplkit.SmplManagementClient`.

The runtime client exposes two ways to read config values:

- :meth:`ConfigClient.bind` — declarative, schema-first. Pass a Pydantic
  ``BaseModel`` instance with the in-code defaults; the SDK registers the
  schema and values, then mutates the *same* instance in place when the
  server pushes updates. Reads are plain attribute access on a real
  Pydantic instance — no proxy indirection, full IDE type-checking.
- :meth:`ConfigClient.get` — lookup-only escape hatch. Returns a
  :class:`LiveConfigProxy`, a read-only dict-like view of resolved values.
  Raises :class:`NotFoundError` when the id is unknown.
"""

from __future__ import annotations


import dataclasses
import logging
import threading
from collections.abc import Callable
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, TypeVar, overload

from pydantic import BaseModel

from smplkit._errors import (
    ConflictError,
    ConnectionError,
    NotFoundError,
    TimeoutError,
    ValidationError,
    _raise_for_status,
)
from smplkit._helpers import PAGE_SIZE, paginate_async, paginate_sync
from smplkit._resolver import resolve
from smplkit._generated.config.api.configs import (  # noqa: F401  (re-exported for test patches)
    create_config,
    delete_config,
    get_config,
    list_configs,
    update_config,
)
from smplkit.config.helpers import _resource_to_async_config, _resource_to_config
from smplkit.config.models import AsyncConfig, Config

if TYPE_CHECKING:
    from smplkit._metrics import _AsyncMetricsReporter, _MetricsReporter
    from smplkit._ws import SharedWebSocket
    from smplkit.client import AsyncSmplClient, SmplClient
    from smplkit.management.client import AsyncSmplManagementClient, SmplManagementClient

logger = logging.getLogger("smplkit")
ws_logger = logging.getLogger("smplkit.config.ws")

# Type var for ``bind()``: bound widens to ``BaseModel | dict[str, Any]``
# so the IDE preserves the caller's exact type — Pydantic users see their
# subclass on the way out, dict users see ``dict[str, Any]``.
_T = TypeVar("_T", bound="BaseModel | dict[str, Any]")

# Sentinel that distinguishes "no default supplied" from "default is None"
# in the two-arg ``get(id, key)`` form. Using a module-level object so we
# can identity-compare against it without any risk of collision with
# legitimate caller-supplied values.
_MISSING: Any = object()


def _check_response_status(status_code: HTTPStatus, content: bytes) -> None:
    """Map HTTP error status codes to SDK exceptions with full JSON:API error detail."""
    _raise_for_status(int(status_code), content)


def _pydantic_field_type(annotation: Any) -> str:
    """Map a Pydantic field annotation to a smplkit Config item type.

    Falls back to ``STRING`` for any annotation that isn't a clear
    primitive — unions, lists, dicts, and unknown types. STRING is the
    safest universal fallback: any value coerces cleanly to a string in
    the console, and the admin can retype the item to ``JSON``,
    ``NUMBER``, or ``BOOLEAN`` later.
    """
    if annotation is bool:
        return "BOOLEAN"
    if annotation is int or annotation is float:
        return "NUMBER"
    if annotation is str:
        return "STRING"
    return "STRING"


def _value_to_item_type(value: Any) -> str:
    """Map a runtime value (dict-bind or get-default) to a Config item type.

    Used when there is no Pydantic annotation to consult — for dict bind
    values and single-value ``get`` defaults. ``bool`` is checked before
    ``int`` because ``bool`` is a subclass of ``int`` in Python.
    """
    if isinstance(value, bool):
        return "BOOLEAN"
    if isinstance(value, (int, float)):
        return "NUMBER"
    if isinstance(value, str):
        return "STRING"
    return "STRING"


def _is_pydantic_model(cls: Any) -> bool:
    return isinstance(cls, type) and hasattr(cls, "model_fields") and hasattr(cls, "model_validate")


def _iter_pydantic_items_from_instance(
    instance: BaseModel,
    *,
    explicit_only: bool,
    prefix: str = "",
) -> list[tuple[str, str, Any, str | None]]:
    """Walk a Pydantic instance and yield ``(key, type, value, description)`` tuples.

    Nested Pydantic models flatten to dot-notation. Values come from the
    *instance* (not the class default) so each bound instance carries its
    own per-tier defaults into the discovery payload.

    When ``explicit_only`` is ``True`` (the parent-bound case), only fields
    the caller explicitly passed to the constructor are yielded —
    determined by ``model_fields_set`` at each nesting level. Fields that
    took their class default are skipped so the resolver inherits them
    from the parent config. When ``explicit_only`` is ``False`` (the root
    case, no parent), every field is yielded — there is nowhere to
    inherit from.
    """
    model_class = type(instance)
    if not _is_pydantic_model(model_class):
        return []

    set_fields: set[str] | None = instance.model_fields_set if explicit_only else None
    items: list[tuple[str, str, Any, str | None]] = []
    for field_name, field_info in model_class.model_fields.items():
        if set_fields is not None and field_name not in set_fields:
            continue

        flat_key = f"{prefix}{field_name}"
        value = getattr(instance, field_name)
        annotation = field_info.annotation

        if isinstance(value, BaseModel):
            items.extend(
                _iter_pydantic_items_from_instance(
                    value,
                    explicit_only=explicit_only,
                    prefix=f"{flat_key}.",
                )
            )
            continue

        item_type = _pydantic_field_type(annotation)
        description = field_info.description
        items.append((flat_key, item_type, value, description))
    return items


def _iter_dict_items(
    d: dict[str, Any],
    *,
    prefix: str = "",
) -> list[tuple[str, str, Any, str | None]]:
    """Walk a dict bound to a config; yield ``(key, type, value, description)`` tuples.

    Nested dicts flatten to dot-notation (matching the Pydantic-instance
    walk). Every key in the dict is treated as explicit — dicts have no
    notion of "took the class default," so the omitted-equals-inherited
    semantic comes from keys the caller simply *didn't put in the dict*.

    Item types are inferred from each value. No descriptions are produced
    (dicts carry no per-key metadata); operators add descriptions in the
    smplkit console.
    """
    items: list[tuple[str, str, Any, str | None]] = []
    for raw_key, value in d.items():
        key_str = str(raw_key)
        flat_key = f"{prefix}{key_str}"
        if isinstance(value, dict):
            items.extend(_iter_dict_items(value, prefix=f"{flat_key}."))
            continue
        item_type = _value_to_item_type(value)
        items.append((flat_key, item_type, value, None))
    return items


def _apply_change_to_target(
    target: BaseModel | dict[str, Any],
    dotted_key: str,
    value: Any,
) -> None:
    """Apply a server-pushed value to a bound target in place.

    Handles both Pydantic instances (mutates via :func:`object.__setattr__`
    to bypass ``frozen=True`` / ``validate_assignment=True``) and dicts
    (mutates via ``__setitem__``). Walks the dotted key path to the
    leaf's parent, gracefully bailing if any intermediate is missing.

    The server has already enforced types and constraints, so the SDK
    trusts the value as-is on either path.
    """
    parts = dotted_key.split(".")
    current: Any = target
    for part in parts[:-1]:
        if isinstance(current, BaseModel):
            try:
                current = getattr(current, part)
            except AttributeError:
                return
        elif isinstance(current, dict):
            if part not in current:
                return
            current = current[part]
        else:
            return

    last = parts[-1]
    if isinstance(current, BaseModel):
        try:
            object.__setattr__(current, last, value)
            fields_set = getattr(current, "__pydantic_fields_set__", None)
            if isinstance(fields_set, set):
                fields_set.add(last)
        except (
            Exception
        ):  # pragma: no cover - defensive: object.__setattr__ on BaseModel for a known field is not expected to raise
            logger.warning(
                "Failed to apply config change %r=%r to bound instance",
                dotted_key,
                value,
                exc_info=True,
            )
    elif isinstance(current, dict):
        current[last] = value


def _build_chain_sync(model: Any, models_by_id: dict[str, Any]) -> list[dict[str, Any]]:
    """Build a parent chain from pre-fetched models without async calls."""
    from smplkit.config.models import _environments_to_wire

    chain = [
        {
            "id": model.id,
            "items": model._items_raw,
            "environments": _environments_to_wire(model._environments),
        }
    ]
    current = model
    while current.parent is not None:
        parent = models_by_id.get(current.parent)
        if parent is None:
            break
        chain.append(
            {
                "id": parent.id,
                "items": parent._items_raw,
                "environments": _environments_to_wire(parent._environments),
            }
        )
        current = parent
    return chain


@dataclasses.dataclass(frozen=True, kw_only=True)
class ConfigChangeEvent:
    """Describes a single config value change.

    Frozen — fields are set at construction and cannot be mutated afterward.

    Attributes:
        config_id: The config id that changed.
        item_key: The item key within the config that changed.
        old_value: The previous value.
        new_value: The updated value.
        source: How the change was delivered (``"websocket"`` or ``"manual"``).
    """

    config_id: str
    item_key: str
    old_value: Any
    new_value: Any
    source: str


class LiveConfigProxy:
    """A live, dict-like view of resolved config values.

    Returned by :meth:`ConfigClient.get` and :meth:`AsyncConfigClient.get`.
    Always reflects the latest server-pushed state — every read sees
    current values.

    Implements the ``Mapping`` API: ``proxy["key"]``, ``key in proxy``,
    ``len(proxy)``, ``for k in proxy``, ``proxy.keys()``, ``proxy.values()``,
    ``proxy.items()``, ``proxy.get(key, default)``. Read-only; any write
    attempt raises.

    For typed access via a Pydantic schema, use :meth:`ConfigClient.bind`
    instead — bound instances stay live on the same WebSocket cache, with
    attribute access typed by the Pydantic class.

    Note: customer config items whose names collide with ``Mapping`` method
    names (``keys``, ``values``, ``items``, ``get``) are shadowed for
    attribute access — use subscript (``proxy["values"]``) for those.
    """

    def __init__(
        self,
        client: ConfigClient | AsyncConfigClient,
        config_id: str,
    ) -> None:
        object.__setattr__(self, "_client", client)
        object.__setattr__(self, "_config_id", config_id)

    def _current_values(self) -> dict[str, Any]:
        """Read the current resolved values from the client cache."""
        client = object.__getattribute__(self, "_client")
        config_id = object.__getattribute__(self, "_config_id")
        return dict(client._config_cache.get(config_id, {}))

    def on_change(self, fn_or_key: Callable[[ConfigChangeEvent], None] | str | None = None) -> Any:
        """Register a change listener scoped to this config.

        Supports three forms:

        - ``@proxy.on_change`` — fires on any change to this config.
        - ``@proxy.on_change("item_key")`` — fires only when ``item_key`` changes.
        - ``@proxy.on_change()`` — same as the bare-decorator form.

        Equivalent to ``client.config.on_change(self._config_id, ...)``;
        offered as sugar so callers who already have a live proxy can
        register listeners without re-stating the config id.
        """
        client = object.__getattribute__(self, "_client")
        config_id = object.__getattribute__(self, "_config_id")
        if callable(fn_or_key):
            return client.on_change(config_id)(fn_or_key)
        if isinstance(fn_or_key, str):
            return client.on_change(config_id, item_key=fn_or_key)
        return client.on_change(config_id)

    def __getattr__(self, name: str) -> Any:
        values = self._current_values()
        try:
            return values[name]
        except KeyError:
            raise AttributeError(f"No config item {name!r}") from None

    def __getitem__(self, key: str) -> Any:
        values = self._current_values()
        return values[key]

    def __iter__(self):
        return iter(self._current_values())

    def __contains__(self, key: object) -> bool:
        return key in self._current_values()

    def __len__(self) -> int:
        return len(self._current_values())

    def keys(self):
        return self._current_values().keys()

    def values(self):
        return self._current_values().values()

    def items(self):
        return self._current_values().items()

    def get(self, key: str, default: Any = None) -> Any:
        return self._current_values().get(key, default)

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError(
            f"LiveConfigProxy is read-only; cannot set {name!r}. Mutate config values via client.manage.config.*"
        )

    def __setitem__(self, key: str, value: Any) -> None:
        raise TypeError(
            f"LiveConfigProxy is read-only; cannot set {key!r}. Mutate config values via client.manage.config.*"
        )

    def __delattr__(self, name: str) -> None:
        raise AttributeError(f"LiveConfigProxy is read-only; cannot delete {name!r}.")

    def __delitem__(self, key: str) -> None:
        raise TypeError(f"LiveConfigProxy is read-only; cannot delete {key!r}.")

    def __repr__(self) -> str:
        config_id = object.__getattribute__(self, "_config_id")
        return f"LiveConfigProxy(config_id={config_id!r})"


class ConfigClient:
    """Synchronous runtime client for Smpl Config.

    Obtained via ``SmplClient(...).config``. Exposes :meth:`bind` (the
    recommended declarative API), :meth:`get` (lookup-only escape hatch),
    :meth:`refresh`, and :meth:`on_change`. CRUD lives on
    :class:`smplkit.SmplManagementClient` (``mgmt.config.*``).
    """

    def __init__(
        self,
        parent: SmplClient,
        *,
        manage: SmplManagementClient,
        metrics: _MetricsReporter | None,
    ) -> None:
        self._parent = parent
        self._manage = manage
        self._metrics = metrics
        self._service = parent._service
        self._environment = parent._environment
        self._config_cache: dict[str, dict[str, Any]] = {}
        self._raw_config_cache: dict[str, Any] = {}
        # LiveConfigProxy instances for ``get(id)`` callers; one per config id.
        self._proxies: dict[str, LiveConfigProxy] = {}
        # Pydantic instances bound via ``bind(id, ...)``; one per config id.
        # WebSocket dispatch mutates these in place when values change.
        self._bindings: dict[str, BaseModel] = {}
        self._connected = False
        self._cache_lock = threading.Lock()
        self._listeners: list[tuple[Callable[[ConfigChangeEvent], None], str | None, str | None]] = []
        self._ws_manager: SharedWebSocket | None = None

    def start(self) -> None:
        """Eagerly initialize the config subclient.

        Fetches all configs, resolves environment-scoped values into the local
        cache, opens the shared WebSocket and subscribes to ``config_changed``
        / ``config_deleted`` / ``configs_changed`` events.

        Idempotent — safe to call multiple times.  Called automatically on
        first ``config.get()`` or ``config.bind()`` if not invoked manually.
        """
        if self._connected:
            return

        # Flush any buffered discovery declarations BEFORE the initial fetch,
        # so newly-discovered configs appear in the cache on first read.
        try:
            self._manage.config.flush()
        except Exception as exc:
            logger.warning("Pre-start config discovery flush failed: %s", exc)

        # Fetch + resolve + cache + fire change listeners (against empty old_cache,
        # so any registered listeners see "initial" events).
        self._do_refresh("initial")
        self._connected = True

        self._ws_manager = self._parent._ensure_ws()
        self._ws_manager.on("config_changed", self._handle_config_changed)
        self._ws_manager.on("config_deleted", self._handle_config_deleted)
        self._ws_manager.on("configs_changed", self._handle_configs_changed)

    def _fetch_all_configs(self) -> list[Config]:
        """List configs directly from the API (no management indirection)."""

        def fetch_page(page_number: int, page_size: int) -> list[Config]:
            try:
                response = list_configs.sync_detailed(
                    client=self._parent._http_client,
                    pagenumber=page_number,
                    pagesize=page_size,
                )
            except Exception as exc:
                _maybe_reraise_network_error(exc, self._parent._http_client._base_url)
                raise
            _check_response_status(response.status_code, response.content)
            if response.parsed is None or not hasattr(response.parsed, "data"):
                return []
            return [_resource_to_config(None, r) for r in response.parsed.data]

        return paginate_sync(fetch_page)

    def _fetch_config(self, config_id: str) -> Config | None:
        """Fetch a single config from the API. Returns ``None`` on missing data."""
        try:
            response = get_config.sync_detailed(config_id, client=self._parent._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._parent._http_client._base_url)
            raise
        _check_response_status(response.status_code, response.content)
        if response.parsed is None or not hasattr(response.parsed, "data"):
            return None
        return _resource_to_config(None, response.parsed.data)

    # ------------------------------------------------------------------
    # Public API: bind, get
    # ------------------------------------------------------------------

    def bind(
        self,
        id: str,
        config: _T,
        *,
        parent: BaseModel | dict[str, Any] | None = None,
    ) -> _T:
        """Bind a Pydantic instance or dict to a config id; return it live.

        Declarative, code-first API. Two flavors:

        - **Pydantic instance**: the class is the schema; the instance
          carries the defaults. With ``parent`` set, only fields the
          caller explicitly passed to the constructor are registered as
          overrides — fields that took their class default are left to
          inherit from the parent (driven by ``model_fields_set``).
        - **Dict**: every key in the dict is a leaf to register, with its
          value as the in-code default. Nested dicts flatten to
          dot-notation. There is no class-default concept — keys the
          caller wants to inherit are simply omitted from the dict.

        On first boot the schema and values are registered with the
        server. The bound object's values are then synced from the cache
        (in case the server has overrides from a previous run). On every
        WebSocket-delivered change thereafter the bound object is mutated
        in place — Pydantic instances via ``object.__setattr__``, dicts
        via ``__setitem__``. Readers always see the current resolved
        value with no proxy indirection.

        Idempotent. Repeated calls with the same ``id`` return the
        originally-bound object; the new ``config`` argument is ignored.

        Args:
            id: The config id to register under.
            config: A populated Pydantic ``BaseModel`` instance or a dict.
                Both supply the schema (via ``type(config)`` or the dict's
                keys) and the in-code defaults.
            parent: Optional parent — any object previously returned from a
                :meth:`bind` call (Pydantic or dict). Activates
                parent-chain inheritance for fields the caller omitted.

        Returns:
            The same ``config`` object, registered and live.

        Raises:
            TypeError: If ``config`` is neither a ``BaseModel`` nor a ``dict``.
            ValueError: If ``parent`` is provided but was not previously
                bound via :meth:`bind`.
        """
        if not isinstance(config, (BaseModel, dict)):
            raise TypeError(f"bind() requires a Pydantic BaseModel instance or dict; got {type(config).__name__}")

        if id in self._bindings:
            return self._bindings[id]  # type: ignore[return-value]

        parent_id: str | None = None
        if parent is not None:
            parent_id = self._config_id_for(parent)
            if parent_id is None:
                raise ValueError(
                    "bind(): parent must be an object previously returned "
                    "from client.config.bind(). Bind the parent first."
                )

        config_name: str | None
        config_description: str | None
        if isinstance(config, BaseModel):
            model_class = type(config)
            config_name = model_class.__name__
            config_description = (model_class.__doc__ or "").strip() or None
        else:
            # Dict bind: no class to introspect for name/description.
            config_name = None
            config_description = None

        self._observe_config_declaration(
            id,
            parent=parent_id,
            name=config_name,
            description=config_description,
        )

        if isinstance(config, BaseModel):
            explicit_only = parent_id is not None
            items_iter = _iter_pydantic_items_from_instance(config, explicit_only=explicit_only)
        else:
            items_iter = _iter_dict_items(config)

        for item_key, item_type, value, description in items_iter:
            self._observe_item_declaration(id, item_key, item_type, value, description)

        # Register the binding BEFORE start() so WebSocket dispatch (which can
        # fire during the initial fetch) finds it.
        self._bindings[id] = config

        self.start()
        self._sync_target_from_cache(config, id)
        return config

    @overload
    def get(self, id: str) -> LiveConfigProxy: ...
    @overload
    def get(self, id: str, key: str) -> Any: ...
    @overload
    def get(self, id: str, key: str, *, default: Any) -> Any: ...
    def get(
        self,
        id: str,
        key: str | None = None,
        *,
        default: Any = _MISSING,
    ) -> Any:
        """Read a config (full) or a single value within a config.

        Three forms dispatched by argument count:

        - ``get(id)`` returns a :class:`LiveConfigProxy` — a live dict-like
          view of the resolved values for ``id``. Raises
          :class:`NotFoundError` if the config is missing. No registration.
        - ``get(id, key)`` returns the resolved value of ``key`` within
          ``id``. Raises :class:`NotFoundError` if the config is missing
          and :class:`KeyError` if the key is missing. No registration.
        - ``get(id, key, default=X)`` returns the resolved value, falling
          back to ``X`` if either the config or the key is missing.
          Never raises. **Registers** the config (if new) and the key
          (with ``X`` as the default value) for code-first observability,
          so the operator sees the reference in the smplkit console.

        For typed access via a Pydantic schema, use :meth:`bind` instead.
        """
        self.start()

        if key is None:
            # Form 1: full-config lookup.
            if id not in self._config_cache:
                raise NotFoundError(f"Config with id '{id}' not found", status_code=404)
            metrics = self._metrics
            if metrics is not None:
                metrics.record("config.resolutions", unit="resolutions", dimensions={"config": id})
            return self._cached_proxy(id)

        # Forms 2 and 3: single-value lookup.
        has_default = default is not _MISSING
        if has_default:
            # Register the config + key so the reference shows up in the
            # console even if it's never been declared via bind(). The
            # buffer is idempotent at the (config_id, item_key) level.
            self._observe_config_declaration(id, parent=None, name=None, description=None)
            self._observe_item_declaration(id, key, _value_to_item_type(default), default, None)

        if id not in self._config_cache:
            if has_default:
                return default
            raise NotFoundError(f"Config with id '{id}' not found", status_code=404)
        values = self._config_cache[id]
        if key not in values:
            if has_default:
                return default
            raise KeyError(f"Config item '{key}' not found in config '{id}'")
        return values[key]

    # ------------------------------------------------------------------
    # Internal: binding helpers
    # ------------------------------------------------------------------

    def _config_id_for(self, target: BaseModel | dict[str, Any]) -> str | None:
        """Return the config_id this target was bound under, or None."""
        for cid, bound in self._bindings.items():
            if bound is target:
                return cid
        return None

    def _sync_target_from_cache(self, target: BaseModel | dict[str, Any], config_id: str) -> None:
        """Apply current cached values to a freshly-bound target.

        Handles the existing-config case: on restart, server-side values
        override the in-code defaults from the constructor (or dict).
        """
        cache = self._config_cache.get(config_id, {})
        for dotted_key, value in cache.items():
            _apply_change_to_target(target, dotted_key, value)

    def _cached_proxy(self, id: str) -> LiveConfigProxy:
        """Return (and cache) the canonical proxy for a config id."""
        proxy = self._proxies.get(id)
        if proxy is None:
            proxy = LiveConfigProxy(self, id)
            self._proxies[id] = proxy
        return proxy

    def _observe_config_declaration(
        self,
        config_id: str,
        *,
        parent: str | None,
        name: str | None,
        description: str | None,
    ) -> None:
        """Queue a config declaration with the management buffer."""
        self._manage.config.register_config(
            config_id,
            service=self._service,
            environment=self._environment,
            parent=parent,
            name=name,
            description=description,
        )

    def _observe_item_declaration(
        self,
        config_id: str,
        item_key: str,
        item_type: str,
        default: Any,
        description: str | None,
    ) -> None:
        """Queue a config item declaration with the management buffer."""
        self._manage.config.register_config_item(config_id, item_key, item_type, default, description)

    # ------------------------------------------------------------------
    # Runtime: refresh / change listeners
    # ------------------------------------------------------------------

    def refresh(self) -> None:
        """Re-fetch all configs and update resolved values.

        Fires change listeners for any values that differ from the previous state.

        Raises:
            ConnectionError: If the fetch fails.
        """
        self._do_refresh("manual")

    def _do_refresh(self, source: str) -> None:
        configs = self._fetch_all_configs()
        environment = self._parent._environment
        new_cache: dict[str, dict[str, Any]] = {}
        for cfg in configs:
            chain = cfg._build_chain(configs)
            new_cache[cfg.id] = resolve(chain, environment)
        with self._cache_lock:
            old_cache = self._config_cache
            self._config_cache = new_cache
            self._raw_config_cache = {cfg.id: cfg for cfg in configs}
        self._fire_change_listeners(old_cache, new_cache, source=source)

    def on_change(
        self, fn_or_id: Callable[[ConfigChangeEvent], None] | str | None = None, *, item_key: str | None = None
    ) -> Any:
        """Register a change listener.

        Supports three forms:

        - ``@client.config.on_change`` — global listener (bare decorator).
        - ``@client.config.on_change("id")`` — config-scoped listener.
        - ``@client.config.on_change("id", item_key="field")`` — item-scoped.
        """
        if callable(fn_or_id):
            self._listeners.append((fn_or_id, None, None))
            return fn_or_id
        elif isinstance(fn_or_id, str):
            config_id = fn_or_id

            def decorator(fn: Callable[[ConfigChangeEvent], None]) -> Callable[[ConfigChangeEvent], None]:
                self._listeners.append((fn, config_id, item_key))
                return fn

            return decorator
        else:

            def decorator(fn: Callable[[ConfigChangeEvent], None]) -> Callable[[ConfigChangeEvent], None]:
                self._listeners.append((fn, None, None))
                return fn

            return decorator

    def _fire_change_listeners(
        self,
        old_cache: dict[str, dict[str, Any]],
        new_cache: dict[str, dict[str, Any]],
        *,
        source: str,
    ) -> None:
        """Diff two caches, apply changes to bound instances, fire listeners."""
        all_config_ids = set(old_cache.keys()) | set(new_cache.keys())
        for cfg_id in all_config_ids:
            old_items = old_cache.get(cfg_id, {})
            new_items = new_cache.get(cfg_id, {})
            all_item_keys = set(old_items.keys()) | set(new_items.keys())
            target = self._bindings.get(cfg_id)
            for i_key in all_item_keys:
                old_val = old_items.get(i_key)
                new_val = new_items.get(i_key)
                if old_val == new_val:
                    continue
                # Apply to bound target first so listeners reading the
                # object see the new value.
                if target is not None:
                    _apply_change_to_target(target, i_key, new_val)
                metrics = self._metrics
                if metrics is not None:
                    metrics.record("config.changes", unit="changes", dimensions={"config": cfg_id})
                event = ConfigChangeEvent(
                    config_id=cfg_id,
                    item_key=i_key,
                    old_value=old_val,
                    new_value=new_val,
                    source=source,
                )
                for callback, ck_filter, ik_filter in self._listeners:
                    if ck_filter is not None and ck_filter != cfg_id:
                        continue
                    if ik_filter is not None and ik_filter != i_key:
                        continue
                    try:
                        callback(event)
                    except Exception:
                        logger.error(
                            "Exception in on_change listener for %s.%s",
                            cfg_id,
                            i_key,
                            exc_info=True,
                        )

    # ------------------------------------------------------------------
    # Internal: event handlers (called by SharedWebSocket)
    # ------------------------------------------------------------------

    def _rebuild_resolved_cache(self, raw_cache: dict[str, Config], source: str) -> None:
        """Re-resolve every config in ``raw_cache`` and fire change listeners.

        Inheritance means a single config change can shift descendants' resolved
        values too — so whenever ``raw_cache`` is mutated (config added, updated,
        or deleted), every config gets re-resolved against the new snapshot.
        """
        environment = self._parent._environment
        raw_list = list(raw_cache.values())
        new_cache: dict[str, dict[str, Any]] = {}
        for cfg_id, cfg in raw_cache.items():
            chain = cfg._build_chain(raw_list)
            new_cache[cfg_id] = resolve(chain, environment)
        with self._cache_lock:
            old_cache = self._config_cache
            self._config_cache = new_cache
            self._raw_config_cache = raw_cache
        self._fire_change_listeners(old_cache, new_cache, source=source)

    def _handle_config_changed(self, data: dict[str, Any]) -> None:
        key = data.get("id")
        if not key:
            self._handle_configs_changed(data)
            return
        with self._cache_lock:
            raw_cache = dict(self._raw_config_cache)
        try:
            cfg = self._fetch_config(key)
        except Exception:
            ws_logger.error("Failed to fetch config %r after WS event", key, exc_info=True)
            return
        if cfg is None:
            return
        raw_cache[key] = cfg
        self._rebuild_resolved_cache(raw_cache, source="websocket")

    def _handle_config_deleted(self, data: dict[str, Any]) -> None:
        key = data.get("id")
        if not key:
            self._handle_configs_changed(data)
            return
        with self._cache_lock:
            raw_cache = dict(self._raw_config_cache)
        if raw_cache.pop(key, None) is None:
            return
        self._rebuild_resolved_cache(raw_cache, source="websocket")

    def _handle_configs_changed(self, data: dict[str, Any]) -> None:
        try:
            self._do_refresh("websocket")
        except Exception:
            ws_logger.error("Failed to refresh configs after WS event", exc_info=True)


class AsyncConfigClient:
    """Asynchronous runtime client for Smpl Config.

    Obtained via ``AsyncSmplClient(...).config``. Mirrors
    :class:`ConfigClient` with awaitable variants. CRUD lives on
    :class:`smplkit.AsyncSmplManagementClient` (``mgmt.config.*``).
    """

    def __init__(
        self,
        parent: AsyncSmplClient,
        *,
        manage: AsyncSmplManagementClient,
        metrics: _AsyncMetricsReporter | None,
    ) -> None:
        self._parent = parent
        self._manage = manage
        self._metrics = metrics
        self._service = parent._service
        self._environment = parent._environment
        self._config_cache: dict[str, dict[str, Any]] = {}
        self._raw_config_cache: dict[str, Any] = {}
        self._proxies: dict[str, LiveConfigProxy] = {}
        self._bindings: dict[str, BaseModel] = {}
        self._connected = False
        self._cache_lock = threading.Lock()
        self._listeners: list[tuple[Callable[[ConfigChangeEvent], None], str | None, str | None]] = []
        self._ws_manager: SharedWebSocket | None = None

    async def start(self) -> None:
        """Eagerly initialize the config subclient.

        Fetches all configs, resolves environment-scoped values into the local
        cache, opens the shared WebSocket and subscribes to ``config_changed``
        / ``config_deleted`` / ``configs_changed`` events.

        Idempotent — safe to call multiple times.  Called automatically on
        first ``config.get()`` or ``config.bind()`` if not invoked manually.
        """
        if self._connected:
            return

        try:
            await self._manage.config.flush()
        except Exception as exc:
            logger.warning("Pre-start config discovery flush failed: %s", exc)

        await self._do_refresh("initial")
        self._connected = True

        self._ws_manager = self._parent._ensure_ws()
        self._ws_manager.on("config_changed", self._handle_config_changed)
        self._ws_manager.on("config_deleted", self._handle_config_deleted)
        self._ws_manager.on("configs_changed", self._handle_configs_changed)

    async def _fetch_all_configs_async(self) -> list[AsyncConfig]:
        async def fetch_page(page_number: int, page_size: int) -> list[AsyncConfig]:
            try:
                response = await list_configs.asyncio_detailed(
                    client=self._parent._http_client,
                    pagenumber=page_number,
                    pagesize=page_size,
                )
            except Exception as exc:
                _maybe_reraise_network_error(exc, self._parent._http_client._base_url)
                raise
            _check_response_status(response.status_code, response.content)
            if response.parsed is None or not hasattr(response.parsed, "data"):
                return []
            return [_resource_to_async_config(None, r) for r in response.parsed.data]

        return await paginate_async(fetch_page)

    # ------------------------------------------------------------------
    # Public API: bind, get
    # ------------------------------------------------------------------

    async def bind(
        self,
        id: str,
        config: _T,
        *,
        parent: BaseModel | dict[str, Any] | None = None,
    ) -> _T:
        """Bind a Pydantic instance or dict to a config id; return it live.

        See :meth:`ConfigClient.bind` for the full contract.
        """
        if not isinstance(config, (BaseModel, dict)):
            raise TypeError(f"bind() requires a Pydantic BaseModel instance or dict; got {type(config).__name__}")

        if id in self._bindings:
            return self._bindings[id]  # type: ignore[return-value]

        parent_id: str | None = None
        if parent is not None:
            parent_id = self._config_id_for(parent)
            if parent_id is None:
                raise ValueError(
                    "bind(): parent must be an object previously returned "
                    "from client.config.bind(). Bind the parent first."
                )

        config_name: str | None
        config_description: str | None
        if isinstance(config, BaseModel):
            model_class = type(config)
            config_name = model_class.__name__
            config_description = (model_class.__doc__ or "").strip() or None
        else:
            config_name = None
            config_description = None

        self._observe_config_declaration(
            id,
            parent=parent_id,
            name=config_name,
            description=config_description,
        )

        if isinstance(config, BaseModel):
            explicit_only = parent_id is not None
            items_iter = _iter_pydantic_items_from_instance(config, explicit_only=explicit_only)
        else:
            items_iter = _iter_dict_items(config)

        for item_key, item_type, value, description in items_iter:
            self._observe_item_declaration(id, item_key, item_type, value, description)

        self._bindings[id] = config

        await self.start()
        self._sync_target_from_cache(config, id)
        return config

    @overload
    async def get(self, id: str) -> LiveConfigProxy: ...
    @overload
    async def get(self, id: str, key: str) -> Any: ...
    @overload
    async def get(self, id: str, key: str, *, default: Any) -> Any: ...
    async def get(
        self,
        id: str,
        key: str | None = None,
        *,
        default: Any = _MISSING,
    ) -> Any:
        """Read a config (full) or a single value within a config.

        See :meth:`ConfigClient.get` for the full contract.
        """
        await self.start()

        if key is None:
            if id not in self._config_cache:
                raise NotFoundError(f"Config with id '{id}' not found", status_code=404)
            metrics = self._metrics
            if metrics is not None:
                metrics.record("config.resolutions", unit="resolutions", dimensions={"config": id})
            return self._cached_proxy(id)

        has_default = default is not _MISSING
        if has_default:
            self._observe_config_declaration(id, parent=None, name=None, description=None)
            self._observe_item_declaration(id, key, _value_to_item_type(default), default, None)

        if id not in self._config_cache:
            if has_default:
                return default
            raise NotFoundError(f"Config with id '{id}' not found", status_code=404)
        values = self._config_cache[id]
        if key not in values:
            if has_default:
                return default
            raise KeyError(f"Config item '{key}' not found in config '{id}'")
        return values[key]

    # ------------------------------------------------------------------
    # Internal: binding helpers
    # ------------------------------------------------------------------

    def _config_id_for(self, target: BaseModel | dict[str, Any]) -> str | None:
        for cid, bound in self._bindings.items():
            if bound is target:
                return cid
        return None

    def _sync_target_from_cache(self, target: BaseModel | dict[str, Any], config_id: str) -> None:
        cache = self._config_cache.get(config_id, {})
        for dotted_key, value in cache.items():
            _apply_change_to_target(target, dotted_key, value)

    def _cached_proxy(self, id: str) -> LiveConfigProxy:
        proxy = self._proxies.get(id)
        if proxy is None:
            proxy = LiveConfigProxy(self, id)
            self._proxies[id] = proxy
        return proxy

    def _observe_config_declaration(
        self,
        config_id: str,
        *,
        parent: str | None,
        name: str | None,
        description: str | None,
    ) -> None:
        self._manage.config.register_config(
            config_id,
            service=self._service,
            environment=self._environment,
            parent=parent,
            name=name,
            description=description,
        )

    def _observe_item_declaration(
        self,
        config_id: str,
        item_key: str,
        item_type: str,
        default: Any,
        description: str | None,
    ) -> None:
        self._manage.config.register_config_item(config_id, item_key, item_type, default, description)

    # ------------------------------------------------------------------
    # Runtime: refresh / change listeners
    # ------------------------------------------------------------------

    async def refresh(self) -> None:
        """Re-fetch all configs and update resolved values.

        Fires change listeners for any values that differ from the previous state.

        Raises:
            ConnectionError: If the fetch fails.
        """
        await self._do_refresh("manual")

    async def _do_refresh(self, source: str) -> None:
        configs = await self._fetch_all_configs_async()
        environment = self._parent._environment
        new_cache: dict[str, dict[str, Any]] = {}
        for cfg in configs:
            chain = await cfg._build_chain(configs)
            new_cache[cfg.id] = resolve(chain, environment)
        with self._cache_lock:
            old_cache = self._config_cache
            self._config_cache = new_cache
            self._raw_config_cache = {cfg.id: cfg for cfg in configs}
        self._fire_change_listeners(old_cache, new_cache, source=source)

    def on_change(
        self, fn_or_id: Callable[[ConfigChangeEvent], None] | str | None = None, *, item_key: str | None = None
    ) -> Any:
        """Register a change listener.

        See :meth:`ConfigClient.on_change` for the full contract.
        """
        if callable(fn_or_id):
            self._listeners.append((fn_or_id, None, None))
            return fn_or_id
        elif isinstance(fn_or_id, str):
            config_id = fn_or_id

            def decorator(fn: Callable[[ConfigChangeEvent], None]) -> Callable[[ConfigChangeEvent], None]:
                self._listeners.append((fn, config_id, item_key))
                return fn

            return decorator
        else:

            def decorator(fn: Callable[[ConfigChangeEvent], None]) -> Callable[[ConfigChangeEvent], None]:
                self._listeners.append((fn, None, None))
                return fn

            return decorator

    def _fire_change_listeners(
        self,
        old_cache: dict[str, dict[str, Any]],
        new_cache: dict[str, dict[str, Any]],
        *,
        source: str,
    ) -> None:
        """Diff two caches, apply changes to bound instances, fire listeners."""
        all_config_ids = set(old_cache.keys()) | set(new_cache.keys())
        for cfg_id in all_config_ids:
            old_items = old_cache.get(cfg_id, {})
            new_items = new_cache.get(cfg_id, {})
            all_item_keys = set(old_items.keys()) | set(new_items.keys())
            target = self._bindings.get(cfg_id)
            for i_key in all_item_keys:
                old_val = old_items.get(i_key)
                new_val = new_items.get(i_key)
                if old_val == new_val:
                    continue
                if target is not None:
                    _apply_change_to_target(target, i_key, new_val)
                metrics = self._metrics
                if metrics is not None:
                    metrics.record("config.changes", unit="changes", dimensions={"config": cfg_id})
                event = ConfigChangeEvent(
                    config_id=cfg_id,
                    item_key=i_key,
                    old_value=old_val,
                    new_value=new_val,
                    source=source,
                )
                for callback, ck_filter, ik_filter in self._listeners:
                    if ck_filter is not None and ck_filter != cfg_id:
                        continue
                    if ik_filter is not None and ik_filter != i_key:
                        continue
                    try:
                        callback(event)
                    except Exception:
                        logger.error(
                            "Exception in on_change listener for %s.%s",
                            cfg_id,
                            i_key,
                            exc_info=True,
                        )

    # ------------------------------------------------------------------
    # Internal: event handlers (called by SharedWebSocket)
    # ------------------------------------------------------------------

    def _rebuild_resolved_cache(self, raw_cache: dict[str, AsyncConfig], source: str) -> None:
        """Re-resolve every config in ``raw_cache`` and fire change listeners.

        Inheritance means a single config change can shift descendants' resolved
        values too — so whenever ``raw_cache`` is mutated (config added, updated,
        or deleted), every config gets re-resolved against the new snapshot.

        Sync-shaped because the WS dispatch thread is sync; ``_build_chain_sync``
        avoids any awaits and works against the already-loaded models.
        """
        environment = self._parent._environment
        new_cache: dict[str, dict[str, Any]] = {}
        for cfg_id, cfg in raw_cache.items():
            chain = _build_chain_sync(cfg, raw_cache)
            new_cache[cfg_id] = resolve(chain, environment)
        with self._cache_lock:
            old_cache = self._config_cache
            self._config_cache = new_cache
            self._raw_config_cache = raw_cache
        self._fire_change_listeners(old_cache, new_cache, source=source)

    def _handle_config_changed(self, data: dict[str, Any]) -> None:
        key = data.get("id")
        if not key:
            self._handle_configs_changed(data)
            return
        with self._cache_lock:
            raw_cache = dict(self._raw_config_cache)
        try:
            response = get_config.sync_detailed(key, client=self._parent._http_client)
            _check_response_status(response.status_code, response.content)
            if response.parsed is None or not hasattr(response.parsed, "data"):
                return
            cfg = _resource_to_async_config(None, response.parsed.data)
        except Exception:
            ws_logger.error("Failed to fetch config %r after WS event", key, exc_info=True)
            return
        raw_cache[key] = cfg
        self._rebuild_resolved_cache(raw_cache, source="websocket")

    def _handle_config_deleted(self, data: dict[str, Any]) -> None:
        key = data.get("id")
        if not key:
            self._handle_configs_changed(data)
            return
        with self._cache_lock:
            raw_cache = dict(self._raw_config_cache)
        if raw_cache.pop(key, None) is None:
            return
        self._rebuild_resolved_cache(raw_cache, source="websocket")

    def _handle_configs_changed(self, data: dict[str, Any]) -> None:
        try:
            models: list[AsyncConfig] = []
            page = 1
            while True:
                response = list_configs.sync_detailed(
                    client=self._parent._http_client,
                    pagenumber=page,
                    pagesize=PAGE_SIZE,
                )
                _check_response_status(response.status_code, response.content)
                if response.parsed is None or not hasattr(response.parsed, "data"):
                    return
                page_rows = [_resource_to_async_config(None, r) for r in response.parsed.data]
                models.extend(page_rows)
                if len(page_rows) < PAGE_SIZE:
                    break
                page += 1
            raw_cache = {m.id: m for m in models}
            self._rebuild_resolved_cache(raw_cache, source="websocket")
        except Exception:
            ws_logger.error("Failed to refresh configs after WS event", exc_info=True)


def _exc_url(exc: Exception) -> str | None:
    """Extract URL from an httpx exception's associated request, if available."""
    try:
        return str(exc.request.url)  # type: ignore[attr-defined]
    except Exception:
        return None


def _maybe_reraise_network_error(exc: Exception, base_url: str | None = None) -> None:
    """Re-raise httpx exceptions as SDK exceptions if applicable.

    Args:
        exc: The exception to inspect.
        base_url: Fallback URL to include in the error message when the exception
            does not carry request context (e.g. DNS failures before a request
            object is attached by httpx).
    """
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
