from __future__ import annotations

from dataclasses import fields as dc_fields
from typing import Any, Callable, Type, TypeVar, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .db import Collection
    from .task_types import TaskDescriptor

from .channels import Chat, ChannelRef, _DeprecatedChannel, API
from .constants import (
    ACCESS_AUTHENTICATED, ACCESS_PUBLIC, AccessLevel,
    CollectionDecl, CollectionScope, Column, _normalize_columns,
    KV_KEY_FIELD,
    SettingDecl, SettingScope,
    PAGE_TYPE_DSL, PAGE_TYPE_REACT,
    PRICING_ONE_TIME, PricingType,
    SCOPE_APP, VALID_SCOPES, VALID_SETTING_SCOPES,
    _TYPE_TO_STR,
)
from .db import CollectionRef
from .filesystem import FileSystem
from .home import HomeConfig, Suggestion
from .image import Image
from .integration import (
    IntegrationConfig,
    KNOWN_SECRET_INTEGRATIONS,
    MODE_OAUTH,
    MODE_SECRET,
    Integration,
)
from .decorators import (
    _BOOT_ATTR, _SHUTDOWN_ATTR, _ENTER_ATTR, _EXIT_ATTR,
    _MESSAGE_ATTR, _SCHEDULE_ATTR, _ENDPOINT_ATTR, _ASGI_ATTR,
)
from .secret import Secret
from .theme import PresetName, Radius, Theme, resolve_theme
from .workflow import Workflow

ChannelLike = Union[Chat, ChannelRef, _DeprecatedChannel, API]

F = TypeVar("F", bound=Callable)
T = TypeVar("T")

_REGISTERED_CLASSES: list[dict[str, Any]] = []
_DATA_REGISTRY: dict[str, Callable] = {}
_HOME_SUGGESTIONS_REGISTRY: dict[str, Callable] = {}

_DATA_ATTR = "__cpsl_data__"
_ACCESS_ATTR = "_cpsl_access"
_SHELL_HOME_VALUES = {"default", "hidden", "chat"}


def _collect_channel_secrets(channels: list[ChannelLike]) -> list[str]:
    """Extract secret names from channel credential fields."""
    names: list[str] = []
    for ch in channels:
        if isinstance(ch, (Chat, ChannelRef, API)):
            continue
        for f in dc_fields(ch):
            v = getattr(ch, f.name)
            if isinstance(v, Secret) and v.name:
                names.append(v.name)
    return names


def _serialize_filesystems(filesystems: dict[str, FileSystem] | None) -> dict[str, dict[str, Any]]:
    fs_map: dict[str, dict[str, Any]] = {}
    if filesystems:
        for mount_path, fs_obj in filesystems.items():
            fs_obj._bind_mount_path(mount_path)
            fs_map[mount_path] = fs_obj.to_dict()
    return fs_map


def _count_widget_type(node: dict[str, Any], widget_type: str) -> int:
    total = 1 if node.get("type") == widget_type else 0
    children = node.get("children")
    if isinstance(children, list):
        for child in children:
            if isinstance(child, dict):
                total += _count_widget_type(child, widget_type)
    return total


class App:
    """Deployment namespace for capsule apps.

    Class-based (existing):
        app = App(name="foo")

        @app.cls(image=Image(), channels=[Chat()])
        class Foo: ...

    Functional (new):
        app = App(name="foo", image=Image(), channels=[Chat()])

        @app.message()
        async def handle(session, msg): ...

    Args:
        name: Unique app identifier.
        image: Environment specification (packages, commands).
        channels: Communication channels (Chat, API, etc.).
        keep_warm_seconds: Seconds to keep the instance warm after last activity.
        secrets: Secret names to inject as environment variables.
        filesystems: Mount paths mapped to FileSystem names.
        cpu: Number of vCPUs allocated to the sandbox (default 0.25).
        memory: MiB of RAM allocated to the sandbox (default 512).
        price: Price in cents charged per interaction.
        pricing_type: ``"one_time"`` or ``"monthly"``.
    """

    def __init__(
        self,
        name: str,
        *,
        image: Image | None = None,
        channels: list[ChannelLike] | None = None,
        keep_warm_seconds: int = 0,
        secrets: list[str] | None = None,
        filesystems: dict[str, FileSystem] | None = None,
        cpu: float = 0.25,
        memory: int = 512,
        price: int = 0,
        pricing_type: PricingType = PRICING_ONE_TIME,
    ) -> None:
        self.name = name
        self._integrations: list[IntegrationConfig] = []
        self._pages: list[dict[str, Any]] = []
        self._collections: list[CollectionDecl] = []
        self._collection_refs: list[CollectionRef] = []
        self._data_sources: dict[str, Callable] = {}
        self._settings: dict[str, SettingDecl] = {}
        self._page_order: int = 0
        self._theme: Theme | None = None
        self._workflows: list[Workflow] = []
        self._home_title: str | None = None
        self._home_subtitle: str | None = None
        self._home_suggestions: tuple[Suggestion, ...] = ()
        self._home_widget_tree: dict[str, Any] | None = None
        self._home_access: AccessLevel = ACCESS_PUBLIC
        self._home_suggestions_handler: Callable | None = None
        self._home_suggestions_access: AccessLevel = ACCESS_PUBLIC
        self._home_suggestions_ttl: int = 0
        self._chat_widget_tree: dict[str, Any] | None = None
        self._shell_config: dict[str, Any] | None = None

        from .settings import SettingsAccessor
        self.settings = SettingsAccessor(self)
        self._kv: Collection | None = None

        # Functional mode: image provided at init time (no @app.cls needed).
        self._functional = image is not None
        self._has_cls = False
        if self._functional:
            all_channels = channels or []
            all_secrets = list(secrets or [])
            for s in _collect_channel_secrets(all_channels):
                if s not in all_secrets:
                    all_secrets.append(s)

            fs_map = _serialize_filesystems(filesystems)

            self._cpsl_config: dict[str, Any] = {
                "app_name": name,
                "image": image.to_dict(),
                "price": price,
                "pricing_type": pricing_type,
                "channels": [c.to_dict() for c in all_channels],
                "keep_warm_seconds": keep_warm_seconds,
                "secrets": all_secrets,
                "filesystems": fs_map,
                "cpu": cpu,
                "memory": memory,
                "integrations": [],
                "schedules": [],
                "pages": [],
                "collections": [],
                "collection_refs": [],
                "data_sources": [],
                "settings": [],
                "workflows": [],
                "home": None,
                "chat": None,
                "shell": None,
                "has_message_handler": False,
                "theme": None,
                "module": None,
                "class_name": None,
            }
            _REGISTERED_CLASSES.append(self._cpsl_config)

    # -- collections ---------------------------------------------------------

    def collection(
        self,
        name: str,
        *,
        columns: list[str | Column] | None = None,
        scope: CollectionScope = SCOPE_APP,
        sortable: bool = False,
        filterable: bool = False,
        paginate: int = 0,
    ) -> CollectionRef:
        """Declare a collection and return a ``CollectionRef`` handle.

        Columns accept plain strings or ``Column(key, type=...)`` objects::

            app.collection("venues", columns=[
                Column("name"),
                Column("status", type="status"),
                Column("revenue", type="currency"),
            ])

        Scopes: ``"app"`` (shared), ``"user"`` (per individual),
        ``"owner"`` (per org/individual), ``"session"`` (per chat session).
        """
        if scope not in VALID_SCOPES:
            raise ValueError(f"scope must be one of {VALID_SCOPES}, got {scope!r}")
        decl = CollectionDecl(
            name=name,
            scope=scope,
            columns=_normalize_columns(tuple(columns)) if columns else None,
            sortable=sortable,
            filterable=filterable,
            paginate=paginate,
        )
        self._collections.append(decl)
        ref = CollectionRef(name=name, decl=decl)
        self._collection_refs.append(ref)
        return ref

    # -- settings ------------------------------------------------------------

    def setting(
        self,
        name: str,
        *,
        scope: SettingScope = SCOPE_APP,
        type: type = str,
        default: Any = None,
        options: list[str] | None = None,
        label: str | None = None,
    ) -> None:
        """Declare a named setting for the app.

        Settings are scoped key-value pairs stored in MongoDB and editable
        via UI widgets (``ui.Toggle``, ``ui.TextInput``, etc.).

        Args:
            name: Unique key for this setting.
            scope: ``"app"`` (shared), ``"owner"`` (per org), or ``"user"`` (per user).
            type: Python type — ``bool``, ``str``, ``int``, or ``float``.
            default: Default value when the setting has not been explicitly set.
            options: Allowed values (makes this a select/dropdown setting).
            label: Human-readable label for the UI (defaults to *name*).
        """
        if scope not in VALID_SETTING_SCOPES:
            raise ValueError(f"setting scope must be one of {VALID_SETTING_SCOPES}, got {scope!r}")
        if type not in _TYPE_TO_STR:
            raise ValueError(f"setting type must be bool, str, int, or float — got {type!r}")
        if name in self._settings:
            raise ValueError(f"setting {name!r} is already declared")
        decl = SettingDecl(
            name=name,
            scope=scope,
            type=type,
            default=default,
            options=tuple(options) if options else None,
            label=label,
        )
        self._settings[name] = decl

    # -- key-value store -----------------------------------------------------

    def _require_kv(self) -> Collection:
        if self._kv is None:
            raise RuntimeError("app KV not available (database not configured)")
        return self._kv

    async def get(self, key: str, default: Any = None) -> Any:
        """Read a value from the app-global persistent KV store.

        Available in ``@app.boot()``, ``@app.message()``, scheduled handlers,
        and anywhere the ``app`` object is accessible. Values persist across
        runtime cold starts.

        Args:
            key: The key to look up.
            default: Returned when the key does not exist.
        """
        doc = await self._require_kv().find_one({KV_KEY_FIELD: key})
        return doc.get("value", default) if doc else default

    async def set(self, key: str, value: Any) -> None:
        """Write a value to the app-global persistent KV store (upsert).

        Args:
            key: The key to store under.
            value: Any JSON-serializable value.
        """
        filt = {KV_KEY_FIELD: key}
        await self._require_kv().update_one(filt, {"$set": {"value": value, **filt}}, upsert=True)

    async def delete(self, key: str) -> None:
        """Remove a key from the app-global persistent KV store.

        Args:
            key: The key to delete.
        """
        await self._require_kv().delete_one({KV_KEY_FIELD: key})

    # -- theme ---------------------------------------------------------------

    def theme(
        self,
        *,
        preset: PresetName | None = None,
        logo: str | None = None,
        logo_background: str | None = None,
        tagline: str | None = None,
        title: str | None = None,
        description: str | None = None,
        site_name: str | None = None,
        preview_image: str | None = None,
        favicon: str | None = None,
        primary: str | None = None,
        accent: str | None = None,
        background: str | None = None,
        foreground: str | None = None,
        sidebar: str | None = None,
        surface: str | None = None,
        border: str | None = None,
        muted: str | None = None,
        danger: str | None = None,
        success: str | None = None,
        font_sans: str | None = None,
        font_mono: str | None = None,
        radius: Radius | None = None,
    ) -> None:
        """Configure the visual theme for the subdomain app.

        Args:
            preset: Start from a built-in theme — ``"dark"``, ``"light"``,
                ``"midnight"``, or ``"warm"``.
            logo: Path to a logo image (relative to app root) or a URL.
            logo_background: Background color behind the logo (hex). Useful
                for transparent SVGs/PNGs that need contrast.
            tagline: Short text displayed below the app name in the sidebar.
            title: Browser and link-preview title. Defaults to the app name.
            description: Meta/OpenGraph/Twitter description.
            site_name: OpenGraph site name. Defaults to the app name.
            preview_image: OpenGraph/Twitter preview image URL or asset path.
            favicon: Browser favicon URL or asset path.
            primary: Interactive elements — links, buttons, focus rings (hex).
            accent: Warm highlight for emphasis (hex). Use sparingly.
            background: Page background color (hex).
            foreground: Primary text color (hex).
            sidebar: Sidebar / navigation background (hex).
            surface: Raised surface color for cards and panels (hex).
            border: Borders, dividers, and separators (hex).
            muted: Secondary / de-emphasized text (hex).
            danger: Destructive actions and error states (hex).
            success: Success states and confirmations (hex).
            font_sans: CSS ``font-family`` for body text.
            font_mono: CSS ``font-family`` for code and data values.
            radius: Border-radius scale — ``"sm"``, ``"md"``, or ``"lg"``.
        """
        overrides = {
            k: v for k, v in {
                "logo": logo, "logo_background": logo_background, "tagline": tagline,
                "title": title, "description": description,
                "site_name": site_name, "preview_image": preview_image, "favicon": favicon,
                "primary": primary, "accent": accent, "background": background,
                "foreground": foreground, "sidebar": sidebar, "surface": surface,
                "border": border, "muted": muted, "danger": danger, "success": success,
                "font_sans": font_sans, "font_mono": font_mono, "radius": radius,
            }.items() if v is not None
        }
        self._theme = resolve_theme(preset=preset, **overrides)

    # -- home ---------------------------------------------------------------

    def _serialize_home(self) -> dict[str, Any] | None:
        dynamic = self._home_suggestions_handler is not None
        if (
            not self._home_title
            and not self._home_subtitle
            and not self._home_suggestions
            and not self._home_widget_tree
            and not dynamic
        ):
            return None
        return HomeConfig(
            title=self._home_title,
            subtitle=self._home_subtitle,
            suggestions=self._home_suggestions,
            widget_tree=self._home_widget_tree,
            dynamic_suggestions=dynamic,
            dynamic_suggestions_access=self._home_suggestions_access,
            dynamic_suggestions_ttl=self._home_suggestions_ttl,
            access=self._home_access,
        ).to_dict()

    def home(
        self,
        *,
        title: str | None = None,
        subtitle: str | None = None,
        suggestions: list[Suggestion] | tuple[Suggestion, ...] | None = None,
        access: AccessLevel = ACCESS_PUBLIC,
    ) -> None:
        """Configure the cached home screen shell and static suggestions."""
        if access not in (ACCESS_PUBLIC, ACCESS_AUTHENTICATED):
            raise ValueError("home access must be 'public' or 'authenticated'")
        self._home_title = title
        self._home_subtitle = subtitle
        self._home_suggestions = tuple(suggestions or ())
        self._home_access = access

    def home_body(self, *, access: AccessLevel = ACCESS_PUBLIC) -> Callable[[Callable], Callable]:
        """Decorator for the cached home body. The function must return a ui.Page."""
        if access not in (ACCESS_PUBLIC, ACCESS_AUTHENTICATED):
            raise ValueError("home body access must be 'public' or 'authenticated'")
        self._home_access = access

        def decorator(fn: Callable) -> Callable:
            widget_tree = fn()
            if not hasattr(widget_tree, "to_dict"):
                raise TypeError(
                    f"@app.home_body() handler must return a ui.Page widget, "
                    f"got {type(widget_tree).__name__}"
                )
            self._home_widget_tree = widget_tree.to_dict()
            return fn

        return decorator

    def home_suggestions(
        self,
        *,
        ttl: int = 0,
        access: AccessLevel = ACCESS_PUBLIC,
    ) -> Callable[[F], F]:
        """Register a function that returns dynamic home suggestions.

        The handler may accept ``ctx: cpsl.HomeContext`` and branch on
        ``ctx.authenticated`` to return different suggestions for guests and
        signed-in users. Leave ``access`` as ``"public"`` for that normal
        pattern; set ``access="authenticated"`` only when the endpoint itself
        should not run for guests.
        """
        if access not in (ACCESS_PUBLIC, ACCESS_AUTHENTICATED):
            raise ValueError("home suggestions access must be 'public' or 'authenticated'")
        if ttl < 0:
            raise ValueError("home suggestions ttl must be >= 0")
        self._home_suggestions_access = access
        self._home_suggestions_ttl = ttl

        def decorator(fn: F) -> F:
            self._home_suggestions_handler = fn
            _HOME_SUGGESTIONS_REGISTRY[self.name] = fn
            return fn

        return decorator

    # -- integrations --------------------------------------------------------

    def add_integration(
        self,
        integration_type: str | Integration | IntegrationConfig,
        *,
        client_id: str | Secret = "",
        client_secret: str | Secret = "",
        scopes: list[str] | None = None,
        fields: list[str] | None = None,
    ) -> None:
        """Declare an integration the app requires from end users.

        OAuth integrations need ``client_id`` and ``client_secret``.
        Secret-based integrations (``tailscale``, ``aws``, or custom with
        ``fields=``) need neither — the user submits credentials via a form.
        """
        if isinstance(integration_type, IntegrationConfig):
            if client_id or client_secret or scopes or fields is not None:
                raise ValueError("IntegrationConfig cannot be combined with client_id/client_secret/scopes/fields")
            config = integration_type
        else:
            type_name = integration_type.value if isinstance(integration_type, Integration) else str(integration_type)
            is_secret = fields is not None or type_name in KNOWN_SECRET_INTEGRATIONS
            config = IntegrationConfig(
                type=type_name,
                client_id=client_id,
                client_secret=client_secret,
                scopes=scopes or [],
                fields=fields,
                mode=MODE_SECRET if is_secret else MODE_OAUTH,
            )

        is_secret = config.mode == MODE_SECRET
        if is_secret and (config.client_id or config.client_secret):
            raise ValueError(f"Secret integration '{config.type}' must not set client_id or client_secret")
        if is_secret and config.type not in KNOWN_SECRET_INTEGRATIONS and not config.fields:
            raise ValueError(f"Custom secret integration '{config.type}' requires fields")
        if not is_secret and (not config.client_id or not config.client_secret):
            raise ValueError(
                f"OAuth integration '{config.type}' requires client_id and client_secret"
            )
        self._integrations.append(config)

    # -- pages ---------------------------------------------------------------

    def add_page(
        self,
        name: str,
        *,
        icon: str = "file",
        component: str,
        packages: list[str] | None = None,
        order: int | None = None,
        access: AccessLevel = ACCESS_PUBLIC,
    ) -> None:
        """Declare a React/TSX page that appears in the subdomain sidebar.

        ``access`` controls who can view the page:
        ``"public"`` (default) — anyone, ``"authenticated"`` — logged-in users only.
        """
        if order is None:
            order = self._page_order
        self._page_order = max(self._page_order, order) + 1
        self._pages.append({
            "name": name,
            "icon": icon,
            "type": PAGE_TYPE_REACT,
            "component": component,
            "packages": packages or [],
            "order": order,
            "access": access,
        })

    def page(
        self,
        name: str,
        *,
        icon: str = "file",
        order: int | None = None,
        access: AccessLevel = ACCESS_PUBLIC,
    ) -> Callable[[Callable], Callable]:
        """Decorator for Python DSL pages. The function must return a ui.Page widget tree.

        ``access`` controls who can view the page:
        ``"public"`` (default) — anyone, ``"authenticated"`` — logged-in users only.
        """
        if order is None:
            order = self._page_order
        self._page_order = max(self._page_order, order) + 1
        _order = order
        _access = access

        def decorator(fn: Callable) -> Callable:
            widget_tree = fn()
            if not hasattr(widget_tree, "to_dict"):
                raise TypeError(
                    f"@app.page('{name}') handler must return a ui.Page widget, "
                    f"got {type(widget_tree).__name__}"
                )
            tree_dict = widget_tree.to_dict()
            self._pages.append({
                "name": name,
                "icon": icon,
                "type": PAGE_TYPE_DSL,
                "widget_tree": tree_dict,
                "order": _order,
                "access": _access,
            })
            return fn

        return decorator

    # -- chat shell ----------------------------------------------------------

    def chat_page(self) -> Callable[[Callable], Callable]:
        """Decorator for the app-wide chat surface.

        The function must return a ``ui.Page`` widget tree containing exactly
        one ``ui.ChatPanel``. That panel is replaced by the active session's
        normal chat stream and composer at runtime.
        """

        def decorator(fn: Callable) -> Callable:
            widget_tree = fn()
            if not hasattr(widget_tree, "to_dict"):
                raise TypeError(
                    f"@app.chat_page() handler must return a ui.Page widget, "
                    f"got {type(widget_tree).__name__}"
                )
            tree_dict = widget_tree.to_dict()
            count = _count_widget_type(tree_dict, "chat_panel")
            if count != 1:
                raise ValueError("@app.chat_page() must contain exactly one cpsl.ui.ChatPanel")
            self._chat_widget_tree = tree_dict
            return fn

        return decorator

    def shell(
        self,
        *,
        home: str = "default",
        show_sidebar: bool = True,
        show_pages: bool = True,
    ) -> None:
        """Configure hosted app shell/navigation chrome.

        ``home`` may be ``"default"``, ``"hidden"``, or ``"chat"``.
        """
        if home not in _SHELL_HOME_VALUES:
            raise ValueError("shell home must be 'default', 'hidden', or 'chat'")
        self._shell_config = {
            "home": home,
            "show_sidebar": bool(show_sidebar),
            "show_pages": bool(show_pages),
        }

    # -- data sources --------------------------------------------------------

    def data(self, name: str, *, access: AccessLevel = ACCESS_PUBLIC) -> Callable[[Callable], Callable]:
        """Register a named data source endpoint. The function is called on
        ``GET /data/<name>`` and should return JSON-serializable data.

        ``access`` controls who can call the endpoint:
        ``"public"`` (default) — anyone, ``"authenticated"`` — logged-in users only.
        """
        _access = access

        def decorator(fn: Callable) -> Callable:
            self._data_sources[name] = fn
            _DATA_REGISTRY[name] = fn
            setattr(fn, _DATA_ATTR, name)
            setattr(fn, _ACCESS_ATTR, _access)
            return fn
        return decorator

    # -- functional handler decorators ----------------------------------------

    def _require_functional(self, decorator_name: str) -> None:
        if self._has_cls:
            raise RuntimeError(
                f"@app.{decorator_name}() cannot be used with @app.cls — "
                "use either functional or class-based style, not both"
            )
        if not self._functional:
            raise RuntimeError(
                f"@app.{decorator_name}() requires an image. "
                "Pass image= to App() or use @app.cls with a class instead."
            )

    def _hook_decorator(self, attr: str, name: str) -> Callable[[F], F]:
        self._require_functional(name)

        def decorator(fn: F) -> F:
            setattr(fn, attr, True)
            setattr(self, f"_{name}_handler", fn)
            if attr == _MESSAGE_ATTR:
                self._cpsl_config["has_message_handler"] = True
            return fn
        return decorator

    def boot(self) -> Callable[[F], F]:
        """Register a boot handler (functional apps)."""
        return self._hook_decorator(_BOOT_ATTR, "boot")

    def shutdown(self) -> Callable[[F], F]:
        """Register a shutdown handler (functional apps)."""
        return self._hook_decorator(_SHUTDOWN_ATTR, "shutdown")

    def enter(self) -> Callable[[F], F]:
        """Register a session-enter handler (functional apps)."""
        return self._hook_decorator(_ENTER_ATTR, "enter")

    def exit(self) -> Callable[[F], F]:
        """Register a session-exit handler (functional apps)."""
        return self._hook_decorator(_EXIT_ATTR, "exit")

    def message(self) -> Callable[[F], F]:
        """Register the message handler (functional apps)."""
        return self._hook_decorator(_MESSAGE_ATTR, "message")

    def schedule(self, cron: str) -> Callable[[F], F]:
        """Register a handler that runs on a cron schedule.

        Args:
            cron: Cron expression (e.g. ``"*/5 * * * *"`` for every 5 minutes,
                ``"0 9 * * 1-5"`` for weekday mornings at 9 AM UTC).
        """
        self._require_functional("schedule")

        def decorator(fn: F) -> F:
            setattr(fn, _SCHEDULE_ATTR, cron)
            attr_name = fn.__name__
            setattr(self, attr_name, fn)
            self._cpsl_config["schedules"].append({"name": attr_name, "cron": cron})
            return fn
        return decorator

    def endpoint(self, method: str = "GET", path: str = "/", authorized: bool = True) -> Callable[[F], F]:
        """Register an HTTP endpoint handler.

        Args:
            method: HTTP method (``"GET"``, ``"POST"``, ``"PUT"``, etc.).
            path: URL path to mount the handler at (e.g. ``"/webhook"``).
            authorized: If ``True``, requests require a valid session token.
        """
        self._require_functional("endpoint")

        def decorator(fn: F) -> F:
            setattr(fn, _ENDPOINT_ATTR, {"method": method, "path": path, "authorized": authorized})
            setattr(self, fn.__name__, fn)
            return fn
        return decorator

    def asgi(self, path: str = "/app") -> Callable[[F], F]:
        """Mount an ASGI application (e.g. FastAPI, Starlette).

        Args:
            path: URL prefix where the ASGI app is served.
        """
        self._require_functional("asgi")

        def decorator(fn: F) -> F:
            setattr(fn, _ASGI_ATTR, {"path": path})
            setattr(self, fn.__name__, fn)
            return fn
        return decorator

    def task(
        self,
        retries: int = 0,
        timeout: int = 0,
        lock: str | None = None,
        retry_for: list[Type[Exception]] | None = None,
        callback_url: str | None = None,
        process: bool = False,
    ) -> Callable[..., TaskDescriptor]:
        """Register a background task.

        The decorated function becomes a :class:`TaskDescriptor` with
        ``.submit()``, ``.schedule()``, ``.find()``, ``.count()``, and
        ``.cancel()`` methods.

        Args:
            retries: Max retry attempts on failure.
            timeout: Seconds before the task is killed (``0`` = no limit).
            lock: Lock template for distributed locking (e.g.
                ``"user:{user_id}"``).
            retry_for: Exception types that trigger a retry instead of
                permanent failure.
            callback_url: URL to POST task result on completion/failure.
            process: Run the task in a **separate OS process** for true
                CPU parallelism and crash isolation. The child receives
                a fully re-hydrated ``Session``.

        Example::

            @app.task(retries=2, timeout=60)
            async def send_email(session: cpsl.Session, to: str, body: str):
                ...

            @app.task(process=True, timeout=300)
            async def heavy_compute(session: cpsl.Session, data: dict):
                # runs on its own core, isolated from the main runner
                ...

            handle = await send_email.submit(session=session, to="a@b.c", body="Hi")
        """
        self._require_functional("task")
        from .task_types import TaskDescriptor as _TD, _TASK_ATTR

        def decorator(fn: Callable) -> TaskDescriptor:
            desc = _TD(
                fn, retries=retries, timeout=timeout, lock=lock,
                retry_for=retry_for, callback_url=callback_url,
                functional=True, process=process,
            )
            setattr(desc, _TASK_ATTR, True)
            setattr(self, fn.__name__, desc)
            return desc
        return decorator

    # -- workflows -----------------------------------------------------------

    def workflow(
        self,
        name: str,
        *,
        scope: str = "user",
        icon: str = "workflow",
        description: str = "",
    ) -> Workflow:
        """Define a named workflow surface.

        Returns a :class:`Workflow` object whose decorators (``@wf.ui()``,
        ``@wf.start()``, ``@wf.action(name)``, ``@wf.message()``) register
        the workflow's lifecycle handlers.

        Args:
            name: Human-readable workflow name shown in the sidebar.
            scope: ``"user"`` (per user), ``"owner"`` (per org), or
                ``"app"`` (global).
            icon: Lucide icon name for the sidebar entry.
            description: Short explanation shown above the composer when
                the workflow has no launcher UI.
        """
        self._require_functional("workflow")
        wf = Workflow(name, scope=scope, icon=icon, description=description)
        self._workflows.append(wf)
        return wf

    # -- cls decorator -------------------------------------------------------

    def cls(
        self,
        *,
        image: Image,
        price: int = 0,
        pricing_type: PricingType = PRICING_ONE_TIME,
        channels: list[ChannelLike] | None = None,
        keep_warm_seconds: int = 0,
        secrets: list[str] | None = None,
        filesystems: dict[str, FileSystem] | None = None,
        cpu: float = 0.25,
        memory: int = 512,
    ) -> Callable[[type[T]], type[T]]:
        """Decorator for class-based apps. Captures deploy config.

        Args:
            image: Environment specification (packages, commands).
            price: Price in cents charged per interaction.
            pricing_type: ``"one_time"`` or ``"monthly"``.
            channels: Communication channels (Chat, API, etc.).
            keep_warm_seconds: Seconds to keep the instance warm after last activity.
            secrets: Secret names to inject as environment variables.
            filesystems: Mount paths mapped to FileSystem names.
            cpu: Number of vCPUs allocated to the sandbox (default 0.25).
            memory: MiB of RAM allocated to the sandbox (default 512).
        """
        if self._functional:
            raise RuntimeError(
                "@app.cls cannot be used on an App with image= set — "
                "use either functional or class-based style, not both"
            )
        self._has_cls = True

        app_name = self.name
        all_channels = channels or []
        all_secrets = list(secrets or [])
        for name in _collect_channel_secrets(all_channels):
            if name not in all_secrets:
                all_secrets.append(name)

        fs_map = _serialize_filesystems(filesystems)

        integrations = [ig.to_dict() for ig in self._integrations]
        pages = sorted(self._pages, key=lambda p: p.get("order", 0))
        data_source_names = list(self._data_sources.keys())
        collections = [c.to_dict() for c in self._collections]
        collection_refs = list(self._collection_refs)
        settings = [s.to_dict() for s in self._settings.values()]
        theme_dict = self._theme.to_dict() if self._theme else None
        home_dict = self._serialize_home()
        chat_dict = {"widget_tree": self._chat_widget_tree} if self._chat_widget_tree else None

        def decorator(klass: type[T]) -> type[T]:
            schedule_specs: list[dict[str, str]] = []
            for attr_name in dir(klass):
                fn = getattr(klass, attr_name, None)
                cron_val = getattr(fn, _SCHEDULE_ATTR, None)
                if cron_val and isinstance(cron_val, str):
                    schedule_specs.append({"name": attr_name, "cron": cron_val})

            config = {
                "app_name": app_name,
                "image": image.to_dict(),
                "price": price,
                "pricing_type": pricing_type,
                "channels": [c.to_dict() for c in all_channels],
                "keep_warm_seconds": keep_warm_seconds,
                "secrets": all_secrets,
                "filesystems": fs_map,
                "cpu": cpu,
                "memory": memory,
                "integrations": integrations,
                "schedules": schedule_specs,
                "pages": pages,
                "collections": collections,
                "collection_refs": collection_refs,
                "data_sources": data_source_names,
                "settings": settings,
                "workflows": [w.to_dict() for w in self._workflows],
                "home": home_dict,
                "chat": chat_dict,
                "shell": self._shell_config,
                "has_message_handler": any(
                    getattr(getattr(klass, attr_name, None), _MESSAGE_ATTR, False)
                    for attr_name in dir(klass)
                ),
                "theme": theme_dict,
                "module": klass.__module__,
                "class_name": klass.__qualname__,
            }
            klass._cpsl_config = config  # type: ignore[attr-defined]
            _REGISTERED_CLASSES.append(config)
            return klass

        return decorator

    # -- config finalization -------------------------------------------------

    def _finalize_config(self) -> None:
        """Snapshot mutable state into the config dict (functional apps only).

        Called by resolve_entry_point / Runner before reading the config,
        so collections, pages, integrations, and data sources declared
        after __init__ are captured.
        """
        if not self._functional:
            return
        cfg = self._cpsl_config
        cfg["integrations"] = [ig.to_dict() for ig in self._integrations]
        cfg["pages"] = sorted(self._pages, key=lambda p: p.get("order", 0))
        cfg["data_sources"] = list(self._data_sources.keys())
        cfg["collections"] = [c.to_dict() for c in self._collections]
        cfg["collection_refs"] = list(self._collection_refs)
        cfg["settings"] = [s.to_dict() for s in self._settings.values()]
        cfg["workflows"] = [w.to_dict() for w in self._workflows]
        cfg["home"] = self._serialize_home()
        cfg["chat"] = {"widget_tree": self._chat_widget_tree} if self._chat_widget_tree else None
        cfg["shell"] = self._shell_config
        cfg["has_message_handler"] = hasattr(self, "_message_handler")
        cfg["theme"] = self._theme.to_dict() if self._theme else None

    def _serialize(self) -> dict[str, Any] | None:
        """Return the deploy spec for the class registered under this app."""
        self._finalize_config()
        for cfg in _REGISTERED_CLASSES:
            if cfg["app_name"] == self.name:
                return cfg
        return None
