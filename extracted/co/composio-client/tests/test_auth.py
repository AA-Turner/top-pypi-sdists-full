"""``auth`` and ``scope`` (2.0.0-rc.18): the Python peer of the TypeScript
``Auth`` / ``Scope`` contract.

What is pinned here: the value types and their validation, how a configured
``auth`` and ``scope`` reach the wire, the reserved-header rule as a function of
what is configured, credential providers resolved once per logical call, the
operation channel that generated security and scope parameters travel on, and
``with_options`` re-running every validation.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Callable

import httpx
import pytest
import respx
from pydantic import BaseModel

from composio_client import (
    AsyncComposio,
    AutoAuth,
    Composio,
    ComposioError,
    NoAuth,
    OrganizationAuth,
    ProjectAuth,
    RequestOptions,
    Scope,
    UserAuth,
    auth_from_credentials,
)

from .conftest import API_KEY, BASE_URL

USER_KEY = "uak_test_123"
ORG_KEY = "oak_test_123"
CREDENTIAL_NAMES = ("x-api-key", "x-user-api-key", "x-org-api-key")


class Echo(BaseModel):
    ok: bool


def credential_headers(request: httpx.Request) -> dict[str, str]:
    return {name: request.headers[name] for name in CREDENTIAL_NAMES if name in request.headers}


class Counter:
    """A credential provider that counts its calls."""

    def __init__(self, value: object = API_KEY) -> None:
        self.calls = 0
        self.value = value

    def __call__(self) -> str:
        self.calls += 1
        return self.value  # type: ignore[return-value]


# ---- the value types ----


@pytest.mark.parametrize("auth_type", [ProjectAuth, UserAuth, OrganizationAuth])
@pytest.mark.parametrize("bad", ["", "   ", "a\nb", "a\rb", "a\x00b", "k€y"])
def test_a_string_credential_must_be_a_sendable_key(auth_type: type[ProjectAuth], bad: str) -> None:
    with pytest.raises(ValueError, match="non-whitespace"):
        auth_type(bad)


@pytest.mark.parametrize("auth_type", [ProjectAuth, UserAuth, OrganizationAuth])
def test_a_credential_is_a_string_or_a_provider(auth_type: type[ProjectAuth]) -> None:
    with pytest.raises(TypeError, match="string or a function"):
        auth_type(42)  # type: ignore[arg-type]
    assert auth_type(" key with spaces is sent exactly ").credential == " key with spaces is sent exactly "
    assert callable(auth_type(lambda: API_KEY).credential)


def test_auto_auth_needs_at_least_one_credential() -> None:
    with pytest.raises(ValueError, match="at least one"):
        AutoAuth()
    with pytest.raises(ValueError, match="non-whitespace"):
        AutoAuth(project="ak", user=" ")


@pytest.mark.parametrize(
    "auth",
    [
        ProjectAuth("ak_secret_value"),
        UserAuth("ak_secret_value"),
        OrganizationAuth("ak_secret_value"),
        AutoAuth(project="ak_secret_value", user="ak_secret_value", organization="ak_secret_value"),
    ],
)
def test_repr_never_shows_a_credential(auth: object) -> None:
    assert "ak_secret_value" not in repr(auth)
    assert "ak_secret_value" not in str(auth)


def test_auth_and_scope_are_frozen_values() -> None:
    with pytest.raises(dataclasses.FrozenInstanceError):
        ProjectAuth("ak").credential = "other"  # type: ignore[misc]
    with pytest.raises(dataclasses.FrozenInstanceError):
        Scope(project_id="p").project_id = "q"  # type: ignore[misc]
    assert ProjectAuth("ak") == ProjectAuth("ak")
    assert NoAuth() == NoAuth()
    assert {NoAuth().mode, ProjectAuth("a").mode, UserAuth("a").mode} == {"none", "project", "user"}
    assert (OrganizationAuth("a").mode, AutoAuth(user="a").mode) == ("organization", "auto")


def test_scope_needs_an_id_and_validates_shape_only() -> None:
    with pytest.raises(ValueError, match="needs an `organization_id`"):
        Scope()
    for bad in ("", " org_1", "org_1 ", "org\n1"):
        with pytest.raises(ValueError, match="non-empty"):
            Scope(organization_id=bad)
        with pytest.raises(ValueError, match="non-empty"):
            Scope(project_id=bad)
    # A project without its organization is a valid scope: the API derives it.
    assert Scope(project_id="pr_1").organization_id is None
    assert Scope(organization_id="org_1", project_id="pr_1").project_id == "pr_1"


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        ({}, NoAuth()),
        ({"project": "ak"}, ProjectAuth("ak")),
        ({"user": "uak"}, UserAuth("uak")),
        ({"organization": "oak"}, OrganizationAuth("oak")),
        ({"project": "ak", "organization": "oak"}, AutoAuth(project="ak", organization="oak")),
        ({"user": "uak", "organization": "oak"}, AutoAuth(user="uak", organization="oak")),
    ],
)
def test_auth_from_credentials(given: dict[str, str], expected: object) -> None:
    assert auth_from_credentials(**given) == expected


# ---- construction ----


def test_auth_is_required_and_typed() -> None:
    with pytest.raises(TypeError, match="auth"):
        Composio(base_url=BASE_URL)  # type: ignore[call-arg]
    with pytest.raises(TypeError, match="`auth` must be"):
        Composio(auth=API_KEY, base_url=BASE_URL)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="`scope` must be"):
        Composio(auth=NoAuth(), scope={"organization_id": "o"}, base_url=BASE_URL)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "removed", ["api_key", "user_api_key", "org_api_key", "default_query", "_environment_variables"]
)
def test_the_removed_keywords_are_refused_by_name(removed: str) -> None:
    with pytest.raises(TypeError, match=removed):
        Composio(auth=NoAuth(), base_url=BASE_URL, **{removed: "x"})  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("auth", "mode"),
    [
        (NoAuth(), "none"),
        (ProjectAuth("ak"), "project"),
        (UserAuth("uak"), "user"),
        (OrganizationAuth("oak"), "organization"),
        (AutoAuth(project="ak"), "auto"),
    ],
)
def test_auth_mode_is_readable(auth: NoAuth, mode: str) -> None:
    client = Composio(auth=auth, base_url=BASE_URL)
    try:
        assert client.auth_mode == mode
        assert client.scope is None
    finally:
        client.close()


async def _async_key() -> str:
    return USER_KEY


def test_the_sync_client_refuses_an_async_provider() -> None:
    with pytest.raises(TypeError, match="AsyncComposio"):
        Composio(auth=UserAuth(_async_key), base_url=BASE_URL)
    with pytest.raises(TypeError, match="AsyncComposio"):
        Composio(auth=AutoAuth(project="ak", user=_async_key), base_url=BASE_URL)


# ---- scope on the wire ----


@respx.mock
def test_scope_is_sent_to_the_api_origin_only() -> None:
    api = respx.get(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))
    elsewhere = respx.get("https://api.test.evil.example/x").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    client = Composio(auth=ProjectAuth(API_KEY), scope=Scope(organization_id="org_1"), base_url=BASE_URL)
    try:
        client._request("get", "/echo", cast_to=Echo)
        client.get(".evil.example/x")
    finally:
        client.close()
    assert api.calls.last.request.headers["x-org-id"] == "org_1"
    assert "x-project-id" not in api.calls.last.request.headers
    assert "x-org-id" not in elsewhere.calls.last.request.headers
    assert credential_headers(elsewhere.calls.last.request) == {}


@respx.mock
def test_scope_does_not_follow_a_redirect_off_origin() -> None:
    respx.get(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(307, headers={"location": "https://elsewhere.test/echo"})
    )
    hop = respx.get("https://elsewhere.test/echo").mock(return_value=httpx.Response(200, json={"ok": True}))
    client = Composio(
        auth=ProjectAuth(API_KEY), scope=Scope(organization_id="org_1", project_id="pr_1"), base_url=BASE_URL
    )
    try:
        client._request("get", "/echo", cast_to=Echo)
    finally:
        client.close()
    headers = hop.calls.last.request.headers
    assert "x-org-id" not in headers and "x-project-id" not in headers
    assert credential_headers(hop.calls.last.request) == {}


@respx.mock
def test_a_project_scope_alone_sends_the_project_id_alone() -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))
    client = Composio(auth=NoAuth(), scope=Scope(project_id="pr_1"), base_url=BASE_URL)
    try:
        client._request("get", "/echo", cast_to=Echo)
    finally:
        client.close()
    assert route.calls.last.request.headers["x-project-id"] == "pr_1"
    assert "x-org-id" not in route.calls.last.request.headers


# ---- reserved headers are a function of what is configured ----


@pytest.mark.parametrize(
    ("auth", "scope", "name", "owner"),
    [
        (ProjectAuth("ak"), None, "x-api-key", "auth"),
        (UserAuth("uak"), None, "X-Org-Api-Key", "auth"),
        (AutoAuth(user="uak"), None, "x-user-api-key", "auth"),
        (NoAuth(), Scope(organization_id="o"), "x-org-id", "scope"),
        (NoAuth(), Scope(project_id="p"), "x-project-id", "scope"),
        (NoAuth(), None, "x-client-library", "the client"),
    ],
)
def test_a_reserved_default_header_fails_construction(
    auth: NoAuth, scope: Scope | None, name: str, owner: str
) -> None:
    with pytest.raises(ComposioError, match=f"set by `?{owner}`?"):
        Composio(auth=auth, scope=scope, base_url=BASE_URL, default_headers={name: "x"})
    with pytest.raises(ComposioError, match=f"set by `?{owner}`?"):
        Composio(auth=auth, scope=scope, base_url=BASE_URL, default_headers={name: None})


def test_with_no_owner_the_credential_and_scope_names_are_ordinary_headers() -> None:
    names = {
        "x-api-key": "a",
        "x-user-api-key": "b",
        "x-org-api-key": "c",
        "x-org-id": "o",
        "x-project-id": "p",
    }
    client = Composio(auth=NoAuth(), base_url=BASE_URL, default_headers=names)
    try:
        assert client.default_headers == names
    finally:
        client.close()
    # Credential names stay ordinary with only a scope; scope names with only auth.
    Composio(
        auth=NoAuth(), scope=Scope(project_id="p"), base_url=BASE_URL, default_headers={"x-api-key": "a"}
    ).close()
    Composio(auth=ProjectAuth("ak"), base_url=BASE_URL, default_headers={"x-org-id": "o"}).close()


@pytest.mark.parametrize(
    "send",
    [
        pytest.param(lambda c, h: c.get("/echo", headers=h), id="raw-headers"),
        pytest.param(
            lambda c, h: c.get("/echo", options=RequestOptions(headers=h)), id="raw-request-options"
        ),
        pytest.param(
            lambda c, h: c.toolkits.list(request_options=RequestOptions(headers=h)),
            id="generated-request-options",
        ),
        pytest.param(lambda c, h: c.toolkits.list(extra_headers=h), id="generated-extra-headers"),
    ],
)
@pytest.mark.parametrize("name", ["x-api-key", "x-org-id"])
def test_a_reserved_per_call_header_fails_before_any_network_work(
    respx_mock: respx.MockRouter, send: Callable[[Composio, dict[str, str]], object], name: str
) -> None:
    route = respx_mock.route().mock(return_value=httpx.Response(200, json={"ok": True}))
    client = Composio(auth=ProjectAuth(API_KEY), scope=Scope(organization_id="org_1"), base_url=BASE_URL)
    try:
        with pytest.raises(ComposioError, match="cannot be passed in `headers`"):
            send(client, {name: "x"})
    finally:
        client.close()
    assert route.call_count == 0


@pytest.mark.asyncio
async def test_the_async_client_refuses_a_reserved_per_call_header(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.route().mock(return_value=httpx.Response(200, json={"ok": True}))
    client = AsyncComposio(auth=UserAuth(USER_KEY), base_url=BASE_URL)
    try:
        with pytest.raises(ComposioError, match="set by `auth`"):
            await client.get("/echo", headers={"x-user-api-key": "other"})
    finally:
        await client.close()
    assert route.call_count == 0


# ---- credential providers ----


@respx.mock
def test_a_provider_is_resolved_once_across_a_retry_and_a_redirect() -> None:
    respx.get(f"{BASE_URL}/echo").mock(
        side_effect=[
            httpx.Response(503, headers={"retry-after-ms": "0"}),
            httpx.Response(307, headers={"location": f"{BASE_URL}/landed"}),
        ]
    )
    landed = respx.get(f"{BASE_URL}/landed").mock(return_value=httpx.Response(200, json={"ok": True}))
    provider = Counter()
    client = Composio(auth=ProjectAuth(provider), base_url=BASE_URL)
    try:
        assert client._request("get", "/echo", cast_to=Echo).ok is True
        assert provider.calls == 1
        assert landed.calls.last.request.headers["x-api-key"] == API_KEY
        # A second logical call resolves again.
        client._request("get", "/landed", cast_to=Echo)
        assert provider.calls == 2
    finally:
        client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize("asynchronous", [True, False])
async def test_the_async_client_resolves_a_provider_once(
    respx_mock: respx.MockRouter, asynchronous: bool
) -> None:
    respx_mock.get(f"{BASE_URL}/echo").mock(
        side_effect=[
            httpx.Response(503, headers={"retry-after-ms": "0"}),
            httpx.Response(307, headers={"location": f"{BASE_URL}/landed"}),
        ]
    )
    landed = respx_mock.get(f"{BASE_URL}/landed").mock(return_value=httpx.Response(200, json={"ok": True}))
    calls = 0

    async def async_provider() -> str:
        nonlocal calls
        calls += 1
        return USER_KEY

    def sync_provider() -> str:
        nonlocal calls
        calls += 1
        return USER_KEY

    client = AsyncComposio(
        auth=UserAuth(async_provider if asynchronous else sync_provider), base_url=BASE_URL
    )
    try:
        assert (await client._request("get", "/echo", cast_to=Echo)).ok is True
    finally:
        await client.close()
    assert calls == 1
    assert credential_headers(landed.calls.last.request) == {"x-user-api-key": USER_KEY}


@respx.mock
def test_a_provider_is_not_called_for_a_request_off_the_api_origin() -> None:
    route = respx.get("https://api.test.evil.example/x").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    provider = Counter()
    client = Composio(auth=ProjectAuth(provider), base_url=BASE_URL)
    try:
        client.get(".evil.example/x")
    finally:
        client.close()
    assert provider.calls == 0
    assert credential_headers(route.calls.last.request) == {}


@pytest.mark.parametrize("value", ["", "  ", None, 42, "a\nb"])
def test_a_provider_must_return_a_sendable_key(respx_mock: respx.MockRouter, value: object) -> None:
    route = respx_mock.route().mock(return_value=httpx.Response(200, json={"ok": True}))
    client = Composio(auth=ProjectAuth(Counter(value)), base_url=BASE_URL)
    try:
        with pytest.raises(ComposioError, match="is not a usable key") as caught:
            client.get("/echo")
    finally:
        client.close()
    assert route.call_count == 0
    # The message names the header, never what the provider returned.
    assert str(caught.value).startswith("The `x-api-key` credential is not a usable key")
    assert "a\nb" not in str(caught.value)


def test_a_provider_failure_is_a_composio_error_with_its_cause(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.route().mock(return_value=httpx.Response(200, json={"ok": True}))

    def failing() -> str:
        raise RuntimeError("vault unreachable")

    client = Composio(auth=ProjectAuth(failing), base_url=BASE_URL)
    try:
        with pytest.raises(ComposioError, match="provider failed") as caught:
            client.get("/echo")
    finally:
        client.close()
    assert isinstance(caught.value.__cause__, RuntimeError)
    assert route.call_count == 0


def test_the_sync_client_refuses_a_provider_that_returns_an_awaitable(respx_mock: respx.MockRouter) -> None:
    respx_mock.route().mock(return_value=httpx.Response(200, json={"ok": True}))
    client = Composio(auth=ProjectAuth(lambda: _async_key()), base_url=BASE_URL)  # type: ignore[arg-type,return-value]
    try:
        with pytest.raises(ComposioError, match="AsyncComposio"):
            client.get("/echo")
    finally:
        client.close()


# ---- the operation channel: generated security and scope parameters ----


@pytest.mark.parametrize(
    "auth",
    [
        NoAuth(),
        ProjectAuth(API_KEY),
        OrganizationAuth(ORG_KEY),
        AutoAuth(project=API_KEY, user="uak_configured"),
    ],
)
def test_an_operation_credential_replaces_the_configured_auth(
    respx_mock: respx.MockRouter, auth: NoAuth
) -> None:
    route = respx_mock.get(f"{BASE_URL}/api/v3.1/org/consumer/connected_toolkits").mock(
        return_value=httpx.Response(200, json={})
    )
    client = Composio(auth=auth, base_url=BASE_URL)
    try:
        client._internal.org.consumer.with_raw_response.list_connected_toolkits(
            user_id="u_1", x_user_api_key=USER_KEY, x_org_id="org_1"
        )
    finally:
        client.close()
    request = route.calls.last.request
    assert credential_headers(request) == {"x-user-api-key": USER_KEY}
    assert request.headers["x-org-id"] == "org_1"


def test_a_replaced_provider_is_never_called(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.post(f"{BASE_URL}/api/v3.1/cli/codact_failures").mock(
        return_value=httpx.Response(200, json={})
    )
    provider = Counter()
    client = Composio(auth=ProjectAuth(provider), base_url=BASE_URL)
    try:
        client._internal.cli.with_raw_response.create_codact_failure(
            failure_type="wrong_tool_slug", ctx={}, session={}, x_user_api_key=USER_KEY
        )
    finally:
        client.close()
    assert provider.calls == 0
    assert credential_headers(route.calls.last.request) == {"x-user-api-key": USER_KEY}


def test_the_declared_headers_mapping_reaches_the_channel_too(respx_mock: respx.MockRouter) -> None:
    """A generated method's ``headers=`` mapping is its declared header group, so
    a credential named there is the operation's, not a generic header."""
    route = respx_mock.post(f"{BASE_URL}/api/v3.1/org/consumer/project/resolve").mock(
        return_value=httpx.Response(200, json={})
    )
    client = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
    try:
        client._internal.org.consumer.project.with_raw_response.resolve(
            headers={"x-user-api-key": USER_KEY, "x-org-id": "org_1"}
        )
    finally:
        client.close()
    assert credential_headers(route.calls.last.request) == {"x-user-api-key": USER_KEY}


def test_an_agreeing_operation_scope_is_sent_once(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.post(f"{BASE_URL}/api/v3.1/org/consumer/project/resolve").mock(
        return_value=httpx.Response(200, json={})
    )
    client = Composio(
        auth=UserAuth(USER_KEY), scope=Scope(organization_id="org_1", project_id="pr_1"), base_url=BASE_URL
    )
    try:
        client._internal.org.consumer.project.with_raw_response.resolve(
            x_user_api_key=USER_KEY, x_org_id="org_1"
        )
    finally:
        client.close()
    headers = route.calls.last.request.headers
    assert headers.get_list("x-org-id") == ["org_1"]
    assert headers["x-project-id"] == "pr_1"


def test_an_operation_scope_fills_a_field_the_scope_leaves_unset(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.post(f"{BASE_URL}/api/v3.1/org/consumer/project/resolve").mock(
        return_value=httpx.Response(200, json={})
    )
    client = Composio(auth=UserAuth(USER_KEY), scope=Scope(project_id="pr_1"), base_url=BASE_URL)
    try:
        client._internal.org.consumer.project.with_raw_response.resolve(
            x_user_api_key=USER_KEY, x_org_id="org_2"
        )
    finally:
        client.close()
    headers = route.calls.last.request.headers
    assert (headers["x-org-id"], headers["x-project-id"]) == ("org_2", "pr_1")


@pytest.mark.asyncio
async def test_a_disagreeing_operation_scope_fails_before_dispatch(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.route().mock(return_value=httpx.Response(200, json={}))
    client = AsyncComposio(auth=UserAuth(USER_KEY), scope=Scope(organization_id="org_1"), base_url=BASE_URL)
    try:
        with pytest.raises(ComposioError, match="disagrees with the client.s `scope`"):
            await client._internal.org.consumer.project.resolve(x_user_api_key=USER_KEY, x_org_id="org_2")
    finally:
        await client.close()
    assert route.call_count == 0


def test_a_missing_required_operation_header_fails_before_dispatch(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.route().mock(return_value=httpx.Response(200, json={}))
    client = Composio(auth=UserAuth(USER_KEY), scope=Scope(organization_id="org_1"), base_url=BASE_URL)
    try:
        # The configured auth and scope do not stand in for a required one.
        with pytest.raises((TypeError, ValueError), match="x[-_]user[-_]api[-_]key"):
            client._internal.org.consumer.project.resolve(x_org_id="org_1")  # type: ignore[call-overload]
    finally:
        client.close()
    assert route.call_count == 0


def test_an_unsendable_operation_credential_fails_before_dispatch(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.route().mock(return_value=httpx.Response(200, json={}))
    client = Composio(auth=NoAuth(), base_url=BASE_URL)
    try:
        with pytest.raises(ComposioError, match="is not a usable key"):
            client._internal.org.consumer.project.resolve(x_user_api_key=" ", x_org_id="org_1")
    finally:
        client.close()
    assert route.call_count == 0


def test_a_raw_call_cannot_reach_the_operation_channel(respx_mock: respx.MockRouter) -> None:
    """A raw caller who needs a different credential derives a client."""
    route = respx_mock.post(f"{BASE_URL}/api/v3.1/org/consumer/project/resolve").mock(
        return_value=httpx.Response(200, json={})
    )
    client = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
    try:
        with pytest.raises(ComposioError, match="set by `auth`"):
            client.post("/api/v3.1/org/consumer/project/resolve", headers={"x-user-api-key": USER_KEY})
        client.with_options(auth=UserAuth(USER_KEY)).post("/api/v3.1/org/consumer/project/resolve")
    finally:
        client.close()
    assert credential_headers(route.calls.last.request) == {"x-user-api-key": USER_KEY}


# ---- with_options re-runs every validation ----


def test_with_options_inherits_auth_and_scope() -> None:
    client = Composio(auth=ProjectAuth(API_KEY), scope=Scope(organization_id="org_1"), base_url=BASE_URL)
    derived = client.with_options(max_retries=0)
    try:
        assert (derived.auth_mode, derived.scope) == ("project", Scope(organization_id="org_1"))
        assert client.with_options(scope=None).scope is None
        assert client.with_options(scope=Scope(project_id="pr_2")).scope == Scope(project_id="pr_2")
        assert client.with_options(auth=NoAuth()).auth_mode == "none"
    finally:
        client.close()


def test_with_options_holds_a_new_base_url_to_the_credential_rule() -> None:
    client = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
    try:
        with pytest.raises(ComposioError, match="must use HTTPS"):
            client.with_options(base_url="http://api.example.com")
        # Without a credential, a plain-HTTP origin is allowed.
        assert client.with_options(auth=NoAuth(), base_url="http://api.example.com").base_url == (
            "http://api.example.com"
        )
    finally:
        client.close()


def test_with_options_holds_inherited_headers_to_a_new_owner() -> None:
    client = Composio(
        auth=NoAuth(), base_url=BASE_URL, default_headers={"x-org-id": "org_1", "x-api-key": "dash"}
    )
    try:
        with pytest.raises(ComposioError, match="`x-org-id` header is set by `scope`"):
            client.with_options(scope=Scope(organization_id="org_1"))
        with pytest.raises(ComposioError, match="`x-api-key` header is set by `auth`"):
            client.with_options(auth=ProjectAuth(API_KEY))
        # Replacing the headers in the same call is how the caller moves them.
        moved = client.with_options(
            auth=ProjectAuth(API_KEY), scope=Scope(organization_id="org_1"), set_default_headers={}
        )
        assert (moved.auth_mode, moved.default_headers) == ("project", {})
    finally:
        client.close()


@pytest.mark.asyncio
async def test_async_with_options_validates_too() -> None:
    client = AsyncComposio(auth=UserAuth(_async_key), base_url=BASE_URL)
    try:
        with pytest.raises(ComposioError, match="must use HTTPS"):
            client.with_options(base_url="http://api.example.com")
        assert client.with_options(scope=Scope(project_id="pr_1")).scope == Scope(project_id="pr_1")
    finally:
        await client.close()
