import sys
import uuid
from unittest.mock import AsyncMock, Mock

import pytest
import reflex as rx
from reflex.istate.data import RouterData
from reflex.state import BaseState
from starlette.datastructures import Headers
from starlette.requests import Request
from starlette.routing import Route

from reflex_enterprise.app import AppEnterprise
from reflex_enterprise.auth.cookie import HTTPCookie, sync_cookies


@pytest.fixture
def mock_http_cookie_notify_sync(monkeypatch):
    monkeypatch.setattr(HTTPCookie, "notify_sync", Mock())
    return HTTPCookie.notify_sync


def test_bind_cookie_to_state_class():
    """Test binding HTTPCookie to a State subclass."""

    class TestState(BaseState):
        """A test state with a HTTPCookie descriptors."""

        _test_cookie: str = HTTPCookie("test_value", name="browser_name", max_age=100)
        _encoded_cookie: str = HTTPCookie(b"utf-8", "utf-8")
        _encoded_errors_cookie: str = HTTPCookie("😅".encode(), "ascii", "replace")

    assert isinstance(TestState._test_cookie, HTTPCookie)
    assert TestState._test_cookie == "test_value"
    assert TestState._test_cookie.state is TestState
    assert TestState._test_cookie.var_name == "_test_cookie"
    assert TestState._test_cookie.get_cookie_name() == "browser_name"
    assert TestState._test_cookie.max_age == 100
    assert TestState._encoded_cookie == "utf-8"
    assert TestState._encoded_errors_cookie == "����"

    assert "_test_cookie" not in TestState.backend_vars
    assert "_encoded_cookie" not in TestState.backend_vars
    assert "_encoded_errors_cookie" not in TestState.backend_vars


def test_bind_cookie_backend_only():
    """Test using HTTPCookie as a frontend var raises an error."""
    exp_error = TypeError
    if sys.version_info < (3, 12):
        # Older interpreters don't re-raise the inner error.
        exp_error = RuntimeError

    with pytest.raises(exp_error):

        class InvalidState(BaseState):
            """An invalid state with HTTPCookie as a frontend var."""

            invalid_cookie: str = HTTPCookie()


def test_get_skip_vars_cookie_inheritance_hierarchy():
    """Test that get_skip_vars includes only HTTPCookie vars visible to each class."""

    class ParentState(BaseState):
        """Parent state with one cookie."""

        _parent_cookie: str = HTTPCookie("parent")

    class ChildState(ParentState):
        """Child state with its own cookie."""

        _child_cookie: str = HTTPCookie("child")

    class GrandChildState(ChildState):
        """Grandchild state with another cookie."""

        _grandchild_cookie: str = HTTPCookie("grandchild")

    parent_skip_vars = ParentState.get_skip_vars()
    child_skip_vars = ChildState.get_skip_vars()
    grandchild_skip_vars = GrandChildState.get_skip_vars()

    assert "_parent_cookie" not in parent_skip_vars
    assert "_child_cookie" not in parent_skip_vars
    assert "_grandchild_cookie" not in parent_skip_vars

    assert "_parent_cookie" in child_skip_vars
    assert "_child_cookie" not in child_skip_vars
    assert "_grandchild_cookie" not in child_skip_vars

    assert "_parent_cookie" in grandchild_skip_vars
    assert "_child_cookie" in grandchild_skip_vars
    assert "_grandchild_cookie" not in grandchild_skip_vars


def test_set_get_cookie_value(mock_http_cookie_notify_sync):
    """Test setting and getting cookie values."""

    class TestState(BaseState):
        """A test state with an HTTPCookie."""

        _test_cookie: str = HTTPCookie(
            "initial_value", name="browser_name", max_age=100
        )

    state_instance = TestState()

    assert state_instance._test_cookie == "initial_value"
    assert "_test_cookie" not in state_instance.dirty_vars
    assert not TestState._test_cookie.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]

    state_instance._test_cookie = "new_value"
    assert state_instance._test_cookie == "new_value"
    assert "_test_cookie" in state_instance.dirty_vars
    assert TestState._test_cookie.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]

    mock_http_cookie_notify_sync.assert_called_once_with(state_instance)


def test_set_cookie_no_sync(mock_http_cookie_notify_sync):
    """Test setting cookie value with _sync_on_set=False does not notify sync."""

    class TestState(BaseState):
        """A test state with an HTTPCookie."""

        _test_cookie: str = HTTPCookie("initial_value", _sync_on_set=False)
        _test_cookie_explicit_no_sync: str = HTTPCookie("initial_value")

    state_instance = TestState()

    state_instance._test_cookie = "new_value_no_sync"
    assert state_instance._test_cookie == "new_value_no_sync"
    assert "_test_cookie" in state_instance.dirty_vars
    assert TestState._test_cookie.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]
    mock_http_cookie_notify_sync.assert_not_called()

    state_instance.dirty_vars.clear()
    state_instance.__delattr__(TestState._test_cookie.dirty_attribute_name)  # pyright: ignore[reportAttributeAccessIssue]

    # Cannot override the sync value set in the definition
    state_instance._test_cookie = HTTPCookie("new_value_try_sync", _sync_on_set=True)
    assert state_instance._test_cookie == "new_value_try_sync"
    assert "_test_cookie" in state_instance.dirty_vars
    assert TestState._test_cookie.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]
    mock_http_cookie_notify_sync.assert_not_called()

    state_instance.dirty_vars.clear()
    state_instance.__delattr__(TestState._test_cookie.dirty_attribute_name)  # pyright: ignore[reportAttributeAccessIssue]

    # Can disable the sync for a one-off set
    state_instance._test_cookie_explicit_no_sync = HTTPCookie(
        "new_value_no_sync_explicit",
        _sync_on_set=False,
    )
    assert state_instance._test_cookie_explicit_no_sync == "new_value_no_sync_explicit"
    assert "_test_cookie" not in state_instance.dirty_vars
    assert "_test_cookie_explicit_no_sync" in state_instance.dirty_vars
    assert TestState._test_cookie_explicit_no_sync.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]
    mock_http_cookie_notify_sync.assert_not_called()

    state_instance.dirty_vars.clear()
    state_instance.__delattr__(
        TestState._test_cookie_explicit_no_sync.dirty_attribute_name  # pyright: ignore[reportAttributeAccessIssue]
    )

    # The default sync behavior is working when setting just a str
    state_instance._test_cookie_explicit_no_sync = "new_value_sync"
    assert state_instance._test_cookie_explicit_no_sync == "new_value_sync"
    assert "_test_cookie" not in state_instance.dirty_vars
    assert "_test_cookie_explicit_no_sync" in state_instance.dirty_vars
    assert TestState._test_cookie_explicit_no_sync.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]
    mock_http_cookie_notify_sync.assert_called_once_with(state_instance)

    state_instance.dirty_vars.clear()
    state_instance.__delattr__(
        TestState._test_cookie_explicit_no_sync.dirty_attribute_name  # pyright: ignore[reportAttributeAccessIssue]
    )


def test_set_cookie_from_browser(mock_http_cookie_notify_sync):
    """Test setting cookie value from browser sync."""

    class TestState(BaseState):
        """A test state with an HTTPCookie."""

        _test_cookie: str = HTTPCookie("initial_value")

    state_instance = TestState()

    # Simulate pulling cookie value from browser
    TestState._test_cookie.set(  # pyright: ignore[reportAttributeAccessIssue]
        state_instance,
        "updated_value_from_browser",
        from_browser=True,
    )
    assert state_instance._test_cookie == "updated_value_from_browser"
    assert "_test_cookie" in state_instance.dirty_vars
    assert not TestState._test_cookie.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]
    mock_http_cookie_notify_sync.assert_not_called()


def test_get_cookie_from_router_data(mock_http_cookie_notify_sync):
    """Test getting cookie value from router data."""

    class TestState(BaseState):
        """A test state with an HTTPCookie."""

        _test_cookie: str = HTTPCookie("initial_value", name="browser_name")

    state_instance = TestState()
    assert state_instance._test_cookie == "initial_value"

    state_instance.router_data = {
        "headers": {
            "cookie": "other_cookie=other_value; browser_name=value_from_cookie; another_cookie=another_value"
        }
    }
    state_instance.router = RouterData.from_router_data(state_instance.router_data)
    assert state_instance._test_cookie == "value_from_cookie"
    mock_http_cookie_notify_sync.assert_not_called()

    state_instance._test_cookie = "set_explicitly"
    assert state_instance._test_cookie == "set_explicitly"
    mock_http_cookie_notify_sync.assert_called_once_with(state_instance)
    mock_http_cookie_notify_sync.reset_mock()

    # After deleting the cookie, the value from the router_data is ignored.
    del state_instance._test_cookie
    assert state_instance._test_cookie == "initial_value"
    mock_http_cookie_notify_sync.assert_called_once_with(state_instance)


@pytest.mark.usefixtures("mock_http_cookie_notify_sync")
@pytest.mark.asyncio
async def test_get_set_cookie_substates(monkeypatch):
    """Test getting and setting cookies in substates.

    Args:
        monkeypatch: The pytest monkeypatch fixture.
    """

    class ParentState(BaseState):
        """A parent state with an HTTPCookie."""

        _parent_cookie: str = HTTPCookie("parent_value", name="parent_name")

    class ChildState(ParentState):
        """A child state with an HTTPCookie."""

        _child_cookie: str = HTTPCookie("child_value", name="child_name")

    class GrandChildState(ChildState):
        """A grandchild state without its own HTTPCookie."""

        pass

    assert "_parent_cookie" not in ParentState.backend_vars
    assert "_parent_cookie" in ChildState.backend_vars
    assert "_parent_cookie" in ChildState.inherited_vars
    assert "_parent_cookie" in GrandChildState.backend_vars
    assert "_parent_cookie" in GrandChildState.inherited_vars
    assert "_child_cookie" not in ChildState.backend_vars
    assert "_child_cookie" in GrandChildState.backend_vars
    assert "_child_cookie" in GrandChildState.inherited_vars

    app = AppEnterprise()
    monkeypatch.setattr("reflex_enterprise.auth.cookie.State", ParentState)

    async with app.state_manager.modify_state(
        rx.BaseStateToken(ident=str(uuid.uuid4()), cls=GrandChildState)
    ) as state_instance:
        # Test inherited parent cookie
        assert state_instance._parent_cookie == "parent_value"  # pyright: ignore[reportAttributeAccessIssue]
        state_instance._parent_cookie = "new_parent_value"
        assert state_instance._parent_cookie == "new_parent_value"  # pyright: ignore[reportAttributeAccessIssue]

        grandchild = await state_instance.get_state(GrandChildState)
        assert grandchild._parent_cookie == "new_parent_value"

        # Set parent cookie from substate
        grandchild._parent_cookie = "new_parent_value_in_grandchild_instance"
        assert grandchild._parent_cookie == "new_parent_value_in_grandchild_instance"
        assert (
            state_instance._parent_cookie == "new_parent_value_in_grandchild_instance"  # pyright: ignore[reportAttributeAccessIssue]
        )
        grandchild._child_cookie = "new_child_value_in_grandchild_instance"
        child = await state_instance.get_state(ChildState)
        assert child._child_cookie == "new_child_value_in_grandchild_instance"


class HTTPCookieTestState(BaseState):
    """A test state with multiple HTTPCookies."""

    _session_id: str = HTTPCookie("$", name="session_cookie", max_age=3600)
    _no_notify_cookie: str = HTTPCookie(
        "no_notify_value", max_age=3600, _sync_on_set=False
    )
    _temp_cookie: str = HTTPCookie("temp_value", name="temp_cookie", max_age=30)
    _default_name_cookie: str = HTTPCookie()


class HTTPCookieSubTestState(HTTPCookieTestState):
    """A subclass of HTTPCookieTestState to test inheritance."""

    _sub_cookie: str = HTTPCookie("sub_value", name="sub_cookie", max_age=600)


@pytest.fixture
def mock_app(monkeypatch):
    mock_app_module = Mock()
    mock_app = AppEnterprise()
    mock_app._event_namespace = AsyncMock()
    mock_app_module.app = mock_app
    monkeypatch.setattr(
        "reflex_enterprise.auth.cookie.get_app", lambda: mock_app_module
    )
    monkeypatch.setattr("reflex_enterprise.auth.cookie.State", HTTPCookieTestState)
    return mock_app


@pytest.fixture
def token():
    return str(uuid.uuid4())


@pytest.mark.asyncio
async def test_sync_cookies_from_browser(mock_app, token):
    """Test syncing cookies with the browser."""

    request = Mock(spec=Request)
    request.headers = Headers({"X-Reflex-Client-Token": token})
    request.cookies = {
        "session_cookie": "session_value_from_browser",
        "temp_cookie": "temp_value_from_browser",
        "sub_cookie": "sub_value_from_browser",
    }

    response = await sync_cookies(request)
    assert response.headers.get("Set-Cookie") is None

    state_instance = await mock_app.state_manager.get_state(
        rx.BaseStateToken(ident=token, cls=HTTPCookieSubTestState)
    )
    assert state_instance._session_id == "session_value_from_browser"
    assert state_instance._temp_cookie == "temp_value_from_browser"
    assert state_instance._no_notify_cookie == "no_notify_value"
    assert not HTTPCookieTestState._session_id.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]
    assert not HTTPCookieTestState._temp_cookie.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]
    assert not HTTPCookieTestState._no_notify_cookie.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]
    sub_instance = await state_instance.get_state(HTTPCookieSubTestState)
    assert sub_instance._sub_cookie == "sub_value_from_browser"
    assert not HTTPCookieSubTestState._sub_cookie.get_is_dirty(sub_instance)  # pyright: ignore[reportAttributeAccessIssue]


@pytest.mark.asyncio
async def test_sync_cookies_to_browser(mock_app, token):
    """Test syncing cookies to the browser."""

    request = Mock(spec=Request)
    request.headers = Headers({"X-Reflex-Client-Token": token})
    request.cookies = {}

    async with mock_app.state_manager.modify_state(
        rx.BaseStateToken(ident=token, cls=HTTPCookieTestState)
    ) as state_instance:
        state_instance._session_id = "new_session_value"
        state_instance._no_notify_cookie = "new_no_notify_value"
        state_instance._temp_cookie = HTTPCookie("new_temp_value", max_age=666)

    response = await sync_cookies(request)

    set_cookies = dict.fromkeys(response.headers.getlist("Set-Cookie"), True)
    assert set_cookies.pop(
        "session_cookie=new_session_value; HttpOnly; Max-Age=3600; Path=/; SameSite=strict; Secure"
    )
    assert set_cookies.pop(
        "auth___test_cookie___http_cookie_test_state._no_notify_cookie_rx_state_=new_no_notify_value; HttpOnly; Max-Age=3600; Path=/; SameSite=strict; Secure"
    )
    assert set_cookies.pop(
        "temp_cookie=new_temp_value; HttpOnly; Max-Age=666; Path=/; SameSite=strict; Secure"
    )
    assert not set_cookies

    state_instance = await mock_app.state_manager.get_state(
        rx.BaseStateToken(ident=token, cls=HTTPCookieTestState)
    )
    assert not HTTPCookieTestState._session_id.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]
    assert not HTTPCookieTestState._temp_cookie.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]
    assert not HTTPCookieTestState._no_notify_cookie.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]


async def test_sync_cookies_bidirectional(mock_app, token):
    """Test that dirty backend cookies override browser sent cookies."""

    request = Mock(spec=Request)
    request.headers = Headers({"X-Reflex-Client-Token": token})
    request.cookies = {
        "session_cookie": "session_value_from_browser",
        "temp_cookie": "temp_value_from_browser",
    }

    async with mock_app.state_manager.modify_state(
        rx.BaseStateToken(ident=token, cls=HTTPCookieTestState)
    ) as state_instance:
        sub_instance = await state_instance.get_state(HTTPCookieSubTestState)
        sub_instance._session_id = "new_session_value_backend"
        sub_instance._default_name_cookie = "default_name_value_backend"
        assert HTTPCookieTestState._session_id.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]
        assert HTTPCookieTestState._default_name_cookie.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]

    response = await sync_cookies(request)

    set_cookies = dict.fromkeys(response.headers.getlist("Set-Cookie"), True)
    assert set_cookies.pop(
        "session_cookie=new_session_value_backend; HttpOnly; Max-Age=3600; Path=/; SameSite=strict; Secure"
    )
    assert set_cookies.pop(
        "auth___test_cookie___http_cookie_test_state._default_name_cookie_rx_state_=default_name_value_backend; HttpOnly; Path=/; SameSite=strict; Secure"
    )
    assert not set_cookies

    state_instance = await mock_app.state_manager.get_state(
        rx.BaseStateToken(ident=token, cls=HTTPCookieTestState)
    )
    assert not HTTPCookieTestState._session_id.get_is_dirty(state_instance)  # pyright: ignore[reportAttributeAccessIssue]
    assert state_instance._session_id == "new_session_value_backend"
    assert state_instance._temp_cookie == "temp_value_from_browser"
    assert state_instance._no_notify_cookie == "no_notify_value"
    assert state_instance._default_name_cookie == "default_name_value_backend"
    sub_instance = await state_instance.get_state(HTTPCookieSubTestState)
    assert sub_instance._sub_cookie == "sub_value"
    assert sub_instance._session_id == "new_session_value_backend"
    assert sub_instance._temp_cookie == "temp_value_from_browser"
    assert sub_instance._no_notify_cookie == "no_notify_value"
    assert sub_instance._default_name_cookie == "default_name_value_backend"


@pytest.mark.asyncio
async def test_sync_cookies_browser_reset(mock_app, token):
    """Test that cookies deleted in the browser are reset in the backend."""

    request = Mock(spec=Request)
    request.headers = Headers({"X-Reflex-Client-Token": token})
    request.cookies = {}

    async with mock_app.state_manager.modify_state(
        rx.BaseStateToken(ident=token, cls=HTTPCookieTestState)
    ) as state_instance:
        assert state_instance._session_id == "$"
        state_instance._session_id = "new_session_value"

    response = await sync_cookies(request)

    set_cookies = dict.fromkeys(response.headers.getlist("Set-Cookie"), True)
    assert set_cookies.pop(
        "session_cookie=new_session_value; HttpOnly; Max-Age=3600; Path=/; SameSite=strict; Secure"
    )
    assert not set_cookies

    # Sync again, without a dirty cookie, expect it to be deleted.
    response = await sync_cookies(request)
    assert response.headers.get("Set-Cookie") is None
    state_instance = await mock_app.state_manager.get_state(
        rx.BaseStateToken(ident=token, cls=HTTPCookieTestState)
    )
    assert state_instance._session_id == "$"
    assert state_instance._session_id.max_age == 0  # pyright: ignore[reportAttributeAccessIssue]


@pytest.mark.asyncio
async def test_sync_cookies_no_token():
    """Test that sync_cookies returns a response with no Set-Cookie headers if no token is provided."""

    request = Mock(spec=Request)
    request.headers = {}
    request.cookies = {
        "session_cookie": "session_value_from_browser",
        "temp_cookie": "temp_value_from_browser",
    }

    response = await sync_cookies(request)
    assert response.status_code == 400
    assert response.body == b"No client token in request"


def test_unbound_cookie_access():
    """Test that accessing attributes on a free-standing cookie fail."""

    c = HTTPCookie("value")
    with pytest.raises(RuntimeError):
        _ = c.state
    with pytest.raises(RuntimeError):
        _ = c.var_name
    with pytest.raises(RuntimeError):
        _ = c.get_cookie_name()
    with pytest.raises(RuntimeError):
        _ = c.attribute_name
    with pytest.raises(RuntimeError):
        _ = c.dirty_attribute_name


def test_out_of_tree_access():
    """Test that accessing cookie on non-owning state fails."""

    class SomeState(BaseState):
        """A test state with an HTTPCookie."""

        _session_id: str = HTTPCookie("value")

    state_instance = SomeState()

    with pytest.raises(AttributeError):
        HTTPCookieTestState._session_id.__get__(state_instance, HTTPCookieTestState)  # pyright: ignore[reportAttributeAccessIssue]


def test_ensure_handlers_registered(mock_app):
    """Test that ensure_handlers_registered works without error."""
    # Reset the registration flag for testing
    HTTPCookie._has_registered_handlers = False

    exp_route = Route(
        path="/_reflex/cookies/sync",
        endpoint=sync_cookies,
        name="sync_cookies",
        methods=["POST"],
    )
    assert exp_route not in mock_app._api.routes
    routes_before = mock_app._api.routes.copy()

    HTTPCookie.ensure_handlers_registered()
    assert exp_route in mock_app._api.routes
    routes_after_1 = mock_app._api.routes.copy()

    # Shouldn't have registered it multiple times.
    HTTPCookie.ensure_handlers_registered()
    HTTPCookie.ensure_handlers_registered()
    HTTPCookie.ensure_handlers_registered()
    assert routes_after_1 == mock_app._api.routes
    assert len(routes_before) + 1 == len(mock_app._api.routes)


@pytest.mark.asyncio
async def test_notify_send(mock_app, token):
    """Test that notify_sync sends an update to the client."""
    async with mock_app.modify_state(
        rx.BaseStateToken(ident=token, cls=HTTPCookieTestState)
    ) as state_instance:
        state_instance.router_data = {"token": token}
        state_instance.router = RouterData.from_router_data(state_instance.router_data)
    async with mock_app.modify_state(
        rx.BaseStateToken(ident=token, cls=HTTPCookieTestState)
    ) as state_instance:
        state_instance._session_id = "new_value"

    assert mock_app.event_namespace.emit_update.call_args.kwargs["token"] == token
    update = mock_app.event_namespace.emit_update.call_args.kwargs["update"]
    assert not update.delta
    assert update.final is None
    assert len(update.events) == 1
    event = update.events[0]
    assert event.name == "_call_script"
    js_code = event.payload["javascript_code"]
    assert "fetch(" in js_code
    assert '"/_reflex/cookies/sync"' in js_code
    assert '"include"' in js_code
    assert '"POST"' in js_code
    assert not event.payload.get("callback")


def test_var_dependencies_with_http_cookie():
    """Test that computed var dependencies are tracked correctly with HTTPCookie.

    Verifies that a computed var depending on a regular var in a parent state
    is properly registered in the parent state's _var_dependencies dict.
    """

    class ParentState(BaseState):
        """Parent state with an HTTPCookie field and a regular var."""

        _session_cookie: str = HTTPCookie("default_session", name="session_id")
        message: str = "Hello"

    class ChildState(ParentState):
        """Child state with computed vars depending on parent vars."""

        @rx.var
        def greeting(self) -> str:
            """Computed var that depends on the message var."""
            return f"{self.message}, World!"

        @rx.var
        def cookie_upper(self) -> str:
            """Computed var that depends directly on the HTTPCookie var."""
            return self._session_cookie.upper()

    # The message var should have a dependency from the ChildState.greeting computed var
    assert "message" in ParentState._var_dependencies

    # Extract the dependency tuple
    dependencies = ParentState._var_dependencies["message"]
    assert len(dependencies) == 1

    # The dependency should reference ChildState and the greeting computed var
    state_path, computed_var_name = next(iter(dependencies))
    assert ChildState.get_full_name() == state_path
    assert computed_var_name == "greeting"

    # The HTTPCookie var should also appear in _var_dependencies
    assert "_session_cookie" in ParentState._var_dependencies

    cookie_dependencies = ParentState._var_dependencies["_session_cookie"]
    assert len(cookie_dependencies) == 1

    state_path, computed_var_name = next(iter(cookie_dependencies))
    assert ChildState.get_full_name() == state_path
    assert computed_var_name == "cookie_upper"
