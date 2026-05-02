"""Secure cookie implementation for use with authentication secrets."""

import asyncio
import contextlib
from functools import lru_cache
from typing import Any, ClassVar, get_type_hints, overload

import reflex as rx
from reflex.constants.state import FIELD_MARKER
from reflex.event import EventSpec, IndividualEventType, fix_events
from reflex.state import BaseState, State, StateUpdate, _substate_key
from reflex.utils.prerequisites import get_app
from reflex.utils.types import is_optional
from starlette.requests import Request, cookie_parser
from starlette.responses import Response
from starlette.routing import Route

from reflex_enterprise.utils import fetch, get_backend_url
from reflex_enterprise.vars import PromiseVar

# Used to replace the cookie options without replacing the value.
_NotSet = object()

accepts_final_none = is_optional(get_type_hints(StateUpdate).get("final"))


class HTTPCookie(str):
    """Represents a state Var that is stored as a secure cookie in the browser."""

    _sync_tasks: ClassVar[set[asyncio.Task]] = set()
    _has_registered_handlers: ClassVar[bool] = False

    name: str | None
    path: str
    max_age: int | None
    domain: str | None
    secure: bool
    same_site: str
    httponly: bool
    partitioned: bool
    context: dict
    _sync_on_set: bool

    def __new__(
        cls,
        object: Any = "",
        encoding: str | None = None,
        errors: str | None = None,
        /,
        name: str | None = None,
        path: str = "/",
        max_age: int | None = None,
        domain: str | None = None,
        secure: bool = True,
        same_site: str = "strict",
        partitioned: bool = False,
        _sync_on_set: bool = True,
    ):
        """Create a client-side HTTP-only Cookie (str).

        IMPORTANT: calling `.reset()` on a state does NOT clear cookies on the client.
        You must use `del state.cookie_var` to delete the cookie on the client.

        Args:
            object: The initial object.
            encoding: The encoding to use.
            errors: The error handling scheme to use.
            name: The name of the cookie on the client side.
            path: Cookie path. Use / as the path if the cookie should be accessible on all pages.
            max_age: Relative max age of the cookie in seconds from when the client receives it.
            domain: Domain for the cookie (sub.domain.com or .allsubdomains.com).
            secure: Is the cookie only accessible through HTTPS?
            same_site: Whether the cookie is sent with third party requests.
                One of (true|false|none|lax|strict)
            partitioned: Whether the cookie is partitioned (python 3.14+ only).
            _sync_on_set: Whether to sync the cookie to the client when updated.

        Returns:
            The client-side Cookie object.

        Note: expires (absolute Date) is not supported at this time.
        """
        if encoding or errors:
            inst = super().__new__(cls, object, encoding or "utf-8", errors or "strict")
        else:
            inst = super().__new__(cls, object)
        inst.name = name
        inst.path = path
        inst.max_age = max_age
        inst.domain = domain
        inst.secure = secure
        inst.same_site = same_site
        inst.httponly = True
        inst.partitioned = partitioned
        inst.context = {}
        inst._sync_on_set = _sync_on_set
        return inst

    def _replace(self, object: Any = _NotSet, /, **kwargs: Any) -> "HTTPCookie":
        """Create a new HTTPCookie with updated value and/or fields.

        Args:
            object: The new cookie value.
            **kwargs: The fields to update.

        Returns:
            A new HTTPCookie with the updated fields.
        """
        params = {
            "name": self.name,
            "path": self.path,
            "max_age": self.max_age,
            "domain": self.domain,
            "secure": self.secure,
            "same_site": self.same_site,
            "partitioned": self.partitioned,
            "_sync_on_set": self._sync_on_set,
        }
        params.update(kwargs)
        if object is _NotSet:
            object = str(self)
        return type(self)(object, **params)

    def __set_name__(self, owner: type, name: str):
        """Bind the cookie to the owning state."""
        if not name.startswith("_"):
            msg = f"HTTPCookie name must begin with '_', not {name}"
            raise TypeError(msg)
        self.context["owner"] = owner
        self.context["var_name"] = name

        # Patch some owner class methods to use the descriptor __get__ and __set__.
        original_get_skip_vars = owner.get_skip_vars
        original_init_var_dependency_dicts = owner._init_var_dependency_dicts

        @classmethod
        def get_skip_vars(_: type[BaseState]) -> set[str]:
            return original_get_skip_vars() | {name}

        @classmethod
        def _init_var_dependency_dicts(cls: type[BaseState]) -> None:
            """Remove HTTPCookie var from backend_vars after __init_subclass__."""
            original_init_var_dependency_dicts()
            # Ensure no HTTPCookie vars are in backend_vars.
            remove_vars = []
            for var_name, var_value in cls.backend_vars.items():
                if isinstance(var_value, HTTPCookie):
                    remove_vars.append(var_name)
            for name in remove_vars:
                # Hack so State __getattribute__ will pass control to this descriptor.
                cls.backend_vars.pop(name, None)
                # Hack so computed vars can depend on the cookie var.
                cls.vars[name] = rx.Var("")

        owner.get_skip_vars = get_skip_vars
        owner._init_var_dependency_dicts = _init_var_dependency_dicts

    @property
    def state(self) -> type[BaseState]:
        """Get the state that owns this cookie.

        Returns:
            The owning state.
        """
        if (owner := self.context.get("owner")) is None:
            raise RuntimeError("HTTPCookie not bound to a state")
        return owner

    @property
    def var_name(self) -> str:
        """Get the variable name of this cookie in the state.

        Returns:
            The variable name.
        """
        if (var_name := self.context.get("var_name")) is None:
            raise RuntimeError("HTTPCookie not bound to a state")
        return var_name

    @property
    def attribute_name(self) -> str:
        """Get the attribute name used to store the cookie value on the state instance."""
        return f"_http_cookie_{self.var_name}"

    @property
    def dirty_attribute_name(self) -> str:
        """Get the attribute name used to store the dirty flag on the state instance."""
        return f"{self.attribute_name}_is_dirty"

    def get_cookie_name(self) -> str:
        """Get the name of the cookie in the browser.

        Returns:
            The name of the cookie.
        """
        if self.name:
            return self.name
        return f"{self.state.get_full_name()}.{self.var_name}" + FIELD_MARKER

    def get_from_router_data(self, instance: BaseState) -> "str | None":
        """Get the cookie value from the router_data cookies.

        Args:
            instance: The state instance.

        Returns:
            The cookie value if found, None otherwise.
        """
        with contextlib.suppress(Exception):
            parsed_cookies = cookie_parser(instance.router.headers.cookie)
            return parsed_cookies[self.get_cookie_name()]
        return None

    def get_is_dirty(self, instance: BaseState) -> bool:
        """Check if the cookie is dirty for the given state instance.

        Args:
            instance: The state instance.

        Returns:
            True if the cookie needs to be written to the client, False otherwise.
        """
        with contextlib.suppress(AttributeError):
            return object.__getattribute__(instance, self.dirty_attribute_name)
        return False

    def set_is_dirty(self, instance: BaseState, is_dirty: bool) -> None:
        """Set the dirty flag for the cookie on the given state instance.

        Args:
            instance: The state instance.
            is_dirty: Whether the cookie is dirty.
        """
        object.__setattr__(instance, self.dirty_attribute_name, is_dirty)
        instance._was_touched = True  # persist dirtiness to redis

    def get_defining_state(self, instance: BaseState | None) -> BaseState:
        """Get the state that defines this cookie for the given instance.

        Args:
            instance: The state instance.

        Returns:
            The instance of the state that defines this cookie.

        Raises:
            AttributeError: If the cookie is not defined on any state in the hierarchy.
        """
        original_instance_class_name = type(instance).__name__
        while instance is not None and type(instance) is not self.state:
            instance = instance.parent_state
        if instance is None or type(instance) is not self.state:
            raise AttributeError(
                f"HTTPCookie {self.state.__name__}.{self.var_name} accessed on non-owning state {original_instance_class_name}"
            )
        return instance

    @overload
    def __get__(self, instance: None, owner: type[BaseState]) -> "HTTPCookie": ...

    @overload
    def __get__(self, instance: BaseState, owner: type[BaseState]) -> "HTTPCookie": ...

    def __get__(
        self, instance: BaseState | None, owner: type[BaseState]
    ) -> "HTTPCookie":
        """Get the cookie value from the cache or from router_data cookies."""
        if instance is None:
            return self
        # Make sure we're looking at the owning state.
        instance = self.get_defining_state(instance)
        # Start with the default
        cookie_value = self
        # Lookup value cached on the instance.
        with contextlib.suppress(AttributeError):
            cookie_value = object.__getattribute__(instance, self.attribute_name)
        # If the cookie is default/not set, then try to get it from the router data.
        if (
            cookie_value is self
            and (router_data_value := self.get_from_router_data(instance)) is not None
        ):
            cookie_value = router_data_value
        # Always return an HTTPCookie instance.
        if isinstance(cookie_value, HTTPCookie):
            return cookie_value
        return self._replace(cookie_value)

    def __set__(self, instance: BaseState, value: str) -> None:
        """Descriptor setter for the cookie value (always notifies client)."""
        self.set(instance, value)

    def __delete__(self, instance: BaseState) -> None:
        """Delete the cookie from the client by setting max_age=0."""
        self.set(instance, self._replace(max_age=0))

    def set(self, instance: BaseState, value: str, from_browser: bool = False) -> None:
        """Setter for the cookie value with optional client notification.

        Args:
            instance: The state instance.
            value: The value to set.
            from_browser: True when the value is set via a pull-from-browser request.
        """
        # Happens during initialization of EvenMoreBasicState, before parent_state is set.
        if value is self and not hasattr(instance, self.attribute_name):
            # When a cookie has never been set, do nothing.
            return

        # Make sure we're looking at the owning state.
        instance = self.get_defining_state(instance)
        # The caller is setting the default value explicitly.
        if value is self:
            # Check again, now that we're on the actual owning state.
            if not hasattr(instance, self.attribute_name):
                # When a cookie has never been set, do nothing.
                return
            # Otherwise, we want to delete the cookie on the client (and use the server default).
            value = self._replace(max_age=0)

        object.__setattr__(instance, self.attribute_name, value)

        # Dirty state tracking: write touched values to redis regardless of source.
        instance.dirty_vars.add(self.var_name)
        instance._mark_dirty()
        instance._was_touched = True

        # Avoid resending values that originated from the browser.
        if from_browser:
            return

        # Dirty cookie tracking: only push values explicitly set on the backend.
        self.set_is_dirty(instance, True)
        # Notify task to push the cookie to the client if enabled (requires lost+found).
        if self._sync_on_set and (
            not isinstance(value, HTTPCookie) or value._sync_on_set
        ):
            self.notify_sync(instance)

    def notify_sync(self, instance: BaseState) -> asyncio.Task:
        """Notify the client to make an HTTP request to the backend to receive the updated cookies."""
        app = get_app().app
        t = asyncio.create_task(
            app.event_namespace.emit_update(
                update=StateUpdate(
                    events=fix_events(
                        events=[self.sync()],
                        token=instance.router.session.client_token,
                        router_data=instance.router_data,
                    ),
                    final=None if accepts_final_none else True,
                ),
                token=instance.router.session.client_token,
            )
        )
        type(self)._sync_tasks.add(t)
        t.add_done_callback(type(self)._sync_tasks.discard)
        return t

    @classmethod
    def ensure_handlers_registered(cls):
        """Ensure that the cookie sync handler is registered."""
        if cls._has_registered_handlers:
            return
        app = get_app().app
        # Prepend the route to ensure it takes priority over the proxy middleware.
        app._api.routes.insert(
            0,
            Route("/_reflex/cookies/sync", sync_cookies, methods=["POST"]),
        )
        cls._has_registered_handlers = True

    @classmethod
    @lru_cache(maxsize=8)
    def _get_sync_javascript_code(
        cls, extra_headers: tuple[tuple[str, str], ...] | None = None
    ) -> PromiseVar:
        """Get the JavaScript code to sync cookies on the client."""
        return fetch(
            get_backend_url("/_reflex/cookies/sync"),
            {
                "credentials": "include",
                "method": "POST",
                "headers": extra_headers or {},
            },
        )

    @classmethod
    def sync(
        cls,
        callback: IndividualEventType | list[IndividualEventType] | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> EventSpec:
        """Create an event spec to sync cookies with the client.

        Args:
            callback: An optional event callback to run after sync.
            extra_headers: Optional extra headers to include in the request.

        Returns:
            The event spec.
        """
        cls.ensure_handlers_registered()
        return rx.call_script(
            cls._get_sync_javascript_code(
                tuple(extra_headers.items())
                if extra_headers is not None
                else extra_headers
            ),
            callback=callback,
        )


def get_cookies_from_state_recursive(state: type[BaseState]) -> list[HTTPCookie]:
    """Get all HTTPCookie vars from the given state and its substates.

    Args:
        state: The state to get cookies from.

    Returns:
        A list of HTTPCookie descriptors found in the state.
    """
    cookies: list[HTTPCookie] = []
    parent_state = state.get_parent_state()
    for name, field in state.__fields__.items():
        # Only consider HTTPCookie fields not defined in parent states.
        if isinstance(field.default, HTTPCookie) and not hasattr(parent_state, name):
            cookies.append(field.default)
    for substate in state.get_substates():
        cookies.extend(get_cookies_from_state_recursive(substate))
    return cookies


async def sync_cookies(request: Request) -> Response:
    """HTTP Request handler to get/set cookies on the client.

    The client sends its known cookies in the request headers, and
    the server will send all modified cookies to the frontend to be set in
    the browser.

    This sync generally occurs on-demand after the backend updated cookies in
    the state.

    Args:
        request: The incoming HTTP request.

    Returns:
        An HTTP response indicating success or failure.
    """
    client_token = request.headers.get("X-Reflex-Client-Token")
    if not client_token:
        return Response("No client token in request", status_code=400)

    response = Response(status_code=200)

    app = get_app().app

    try:
        token = rx.BaseStateToken(ident=client_token, cls=State)
    except AttributeError:
        token = _substate_key(client_token, State)

    async with app.modify_state(token, background=True) as state:
        for record in get_cookies_from_state_recursive(state):
            cookie_name = record.get_cookie_name()
            cookie_state = await state.get_state(record.state)
            if not record.get_is_dirty(cookie_state):
                # The backend has NOT modified this cookie, so set the backend value to
                # whatever the browser sent us.
                if (cookie_value := request.cookies.get(cookie_name)) is None:
                    # Browser did not send the cookie, reset it to default value.
                    cookie_value = record
                if cookie_value != record.__get__(cookie_state, owner=record.state):
                    # Set cookie value on state if different.
                    record.set(cookie_state, cookie_value, from_browser=True)
                continue
            # The backend HAS modified this cookie, so send the updated value to the browser.
            cookie_value = getattr(cookie_state, record.attribute_name)
            cookie_options = (
                cookie_value if isinstance(cookie_value, HTTPCookie) else record
            )
            response.set_cookie(
                key=record.get_cookie_name(),
                value=str(cookie_value),
                path=cookie_options.path,
                max_age=cookie_options.max_age,
                domain=cookie_options.domain,
                secure=cookie_options.secure,
                httponly=cookie_options.httponly,
                samesite=cookie_options.same_site,  # pyright: ignore[reportArgumentType]
                partitioned=cookie_options.partitioned,
            )
            # Mark the cookie as clean.
            record.set_is_dirty(cookie_state, False)
    return response
