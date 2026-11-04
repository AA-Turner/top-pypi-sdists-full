"""Rule 0 of the credential boundary — the Python peer of
``test/unit/credential-scheme.test.ts``.

**A request carries exactly one credential header.** Not a design-record rule
but a measured property of the API: probed against production on 2026-08-06,
``GET /toolkits`` answers 200 with ``x-api-key`` alone and **401** with
``x-api-key`` *and* ``x-user-api-key`` together — so there is no additive model
and the client must choose per request.

Since 2.0.0-rc.18 ``auth`` says how that choice is made. A fixed mode
(``ProjectAuth``, ``UserAuth``, ``OrganizationAuth``) sends its one class on
every request and never reads the operation table; ``AutoAuth`` is the
per-operation selection the client made before ``auth`` existed, chosen from
the operation's declared security schemes.
"""

from __future__ import annotations

import re

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
    UserAuth,
    _base_client,
)
from composio_client._credentials import (
    CREDENTIAL_SCHEME_HEADERS,
    Credentials,
    has_alternate_credential,
    select_scheme,
)
from composio_client._operations import Operation

from .conftest import API_KEY, BASE_URL

USER_KEY = "uak_test_123"
ORG_KEY = "oak_test_123"
ALL_AUTO = AutoAuth(project=API_KEY, user=USER_KEY, organization=ORG_KEY)


class Echo(BaseModel):
    ok: bool


def credential_headers(headers: dict[str, str]) -> dict[str, str | None]:
    """Every credential header, so a test asserts on the whole set at once."""
    lowered = {name.lower(): value for name, value in headers.items()}
    return {name: lowered.get(name) for name in ("x-api-key", "x-user-api-key", "x-org-api-key")}


def prepare(client: Composio, method: str, path: str) -> _base_client._Prepared:
    return client._prepare(method, path, body=None, body_model=None, query=None, headers=None, options=None)


# ---- select_scheme: the AutoAuth precedence table, as a pure function ----


ALL_THREE = Credentials(API_KEY, USER_KEY, ORG_KEY)
PROJECT_ONLY = Credentials(API_KEY)
USER_ONLY = Credentials(None, USER_KEY)


@pytest.mark.parametrize(
    ("schemes", "credentials", "expected"),
    [
        # An operation that names nothing keeps today's behaviour.
        (None, ALL_THREE, "ApiKeyAuth"),
        ((), ALL_THREE, "ApiKeyAuth"),
        # `ApiKeyAuth` wins wherever it is an accepted alternative and a project
        # key is held -- 92 of the 111 operations, every wire byte preserved.
        (("ApiKeyAuth",), ALL_THREE, "ApiKeyAuth"),
        (("ApiKeyAuth", "UserApiKeyAuth"), ALL_THREE, "ApiKeyAuth"),
        # ...and only then does the alternative get a turn.
        (("ApiKeyAuth", "UserApiKeyAuth"), USER_ONLY, "UserApiKeyAuth"),
        (("UserApiKeyAuth",), ALL_THREE, "UserApiKeyAuth"),
        (("OrgApiKeyAuth",), ALL_THREE, "OrgApiKeyAuth"),
        # An operation whose only scheme this client holds no key for still
        # sends `x-api-key`, so it fails exactly the way it does today rather
        # than moving to "no credential at all".
        (("UserApiKeyAuth",), PROJECT_ONLY, "ApiKeyAuth"),
        (("OrgApiKeyAuth",), PROJECT_ONLY, "ApiKeyAuth"),
        # An `ApiKeyAuth`-only operation is not something the user key
        # substitutes for; the fallback yields a scheme with no value, so
        # nothing is sent.
        (("ApiKeyAuth",), USER_ONLY, "ApiKeyAuth"),
        # `no_auth` and `workbench_access_key` are referenced by `security` and
        # declared in no `components.securitySchemes`. Those four operations
        # receive `x-api-key` today and are differentially pinned doing so, so
        # an unresolvable name must mean "unchanged", not "no credential".
        (("no_auth",), ALL_THREE, "ApiKeyAuth"),
        (("ApiKeyAuth", "workbench_access_key"), ALL_THREE, "ApiKeyAuth"),
        (("workbench_access_key",), ALL_THREE, "ApiKeyAuth"),
    ],
)
def test_select_scheme(schemes: tuple[str, ...] | None, credentials: Credentials, expected: str) -> None:
    assert select_scheme(schemes, credentials) == expected


def test_has_alternate_credential_is_what_gates_the_table_lookup() -> None:
    assert not has_alternate_credential(PROJECT_ONLY)
    assert not has_alternate_credential(Credentials(None))
    assert has_alternate_credential(USER_ONLY)
    assert has_alternate_credential(Credentials(None, None, ORG_KEY))


# ---- the governing invariant: a project-key client never moves ----


def test_project_key_client_sends_exactly_x_api_key(client: Composio) -> None:
    assert credential_headers(prepare(client, "get", "/echo").headers) == {
        "x-api-key": API_KEY,
        "x-user-api-key": None,
        "x-org-api-key": None,
    }


def test_every_published_operation_carries_exactly_one_credential() -> None:
    """The invariant, measured over the whole published surface.

    This is the rule the API enforces — two credential headers is a 401 — and
    it has to hold on all 111 operations, whichever scheme each resolves to. An
    ``AutoAuth`` client holding all three credentials is the configuration
    that could break it.
    """
    client = Composio(auth=ALL_AUTO, base_url=BASE_URL)
    try:
        for operation in _base_client.OPERATIONS:
            path = re.sub(r"\{[^}]+\}", "p", operation.path)
            placed = [
                name
                for name, value in credential_headers(prepare(client, operation.method, path).headers).items()
                if value is not None
            ]
            assert placed == [CREDENTIAL_SCHEME_HEADERS[select_scheme(operation.schemes, ALL_THREE)]], (
                operation.path
            )
    finally:
        client.close()


def test_the_widened_table_makes_all_three_schemes_reachable() -> None:
    """The selector was inert at ``tool_router`` width — every row declared no
    schemes, so it answered ``ApiKeyAuth`` every time. It is not any more, and
    the distribution is what says so rather than prose."""
    chosen = {select_scheme(operation.schemes, ALL_THREE) for operation in _base_client.OPERATIONS}

    assert chosen == {"ApiKeyAuth", "UserApiKeyAuth", "OrgApiKeyAuth"}


def test_an_org_scoped_operation_sends_the_org_key(respx_mock: respx.MockRouter) -> None:
    """``delete /org/owner/project/{nano_id}`` declares ``OrgApiKeyAuth`` alone,
    so it is the first published operation a project key cannot authenticate."""
    route = respx_mock.delete(f"{BASE_URL}/api/v3.1/org/owner/project/p_1").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )

    client = Composio(auth=AutoAuth(project=API_KEY, organization=ORG_KEY), base_url=BASE_URL)
    try:
        client._request("delete", "/api/v3.1/org/owner/project/p_1", cast_to=Echo)
    finally:
        client.close()

    assert credential_headers(dict(route.calls.last.request.headers)) == {
        "x-api-key": None,
        "x-user-api-key": None,
        "x-org-api-key": ORG_KEY,
    }


def test_generated_call_keeps_identity_when_a_literal_route_overlaps(
    respx_mock: respx.MockRouter,
) -> None:
    route = respx_mock.get(f"{BASE_URL}/api/v3.1/toolkits/categories").mock(
        return_value=httpx.Response(200, json={})
    )
    client = Composio(auth=AutoAuth(user=USER_KEY), base_url=BASE_URL)
    try:
        client.toolkits.with_raw_response.retrieve("categories")
    finally:
        client.close()

    assert credential_headers(dict(route.calls.last.request.headers)) == {
        "x-api-key": None,
        "x-user-api-key": USER_KEY,
        "x-org-api-key": None,
    }


# ---- selection, over a synthetic table ----


SYNTHETIC_OPERATIONS = (
    Operation("get", "/user_scoped", ("user_scoped",), ("UserApiKeyAuth",)),
    Operation("get", "/org_scoped", ("org_scoped",), ("OrgApiKeyAuth",)),
    Operation("get", "/either/{id}", ("either",), ("ApiKeyAuth", "UserApiKeyAuth")),
    Operation("get", "/project_scoped", ("project_scoped",)),
)


@pytest.fixture
def synthetic_table(monkeypatch: pytest.MonkeyPatch) -> None:
    """A table whose rows each declare one shape of ``security``."""
    monkeypatch.setattr(_base_client, "OPERATIONS", SYNTHETIC_OPERATIONS)


@pytest.mark.usefixtures("synthetic_table")
@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/user_scoped", {"x-api-key": None, "x-user-api-key": USER_KEY, "x-org-api-key": None}),
        ("/org_scoped", {"x-api-key": None, "x-user-api-key": None, "x-org-api-key": ORG_KEY}),
        # `ApiKeyAuth` wins on an either-or operation, so nothing already
        # released would move.
        ("/either/7", {"x-api-key": API_KEY, "x-user-api-key": None, "x-org-api-key": None}),
        ("/project_scoped", {"x-api-key": API_KEY, "x-user-api-key": None, "x-org-api-key": None}),
        # Unmatched: an escape-hatch path authenticates the way this client
        # always has.
        ("/not_an_operation", {"x-api-key": API_KEY, "x-user-api-key": None, "x-org-api-key": None}),
    ],
)
def test_auto_selection_routes_by_operation(path: str, expected: dict[str, str | None]) -> None:
    client = Composio(auth=ALL_AUTO, base_url=BASE_URL)
    try:
        assert credential_headers(prepare(client, "get", path).headers) == expected
    finally:
        client.close()


@pytest.mark.usefixtures("synthetic_table")
@pytest.mark.parametrize(
    ("auth", "header", "value"),
    [
        (ProjectAuth(API_KEY), "x-api-key", API_KEY),
        (UserAuth(USER_KEY), "x-user-api-key", USER_KEY),
        (OrganizationAuth(ORG_KEY), "x-org-api-key", ORG_KEY),
    ],
)
@pytest.mark.parametrize("path", ["/user_scoped", "/org_scoped", "/either/7", "/project_scoped", "/raw"])
def test_a_fixed_mode_never_consults_the_operation_table(
    auth: ProjectAuth | UserAuth | OrganizationAuth, header: str, value: str, path: str
) -> None:
    """``UserAuth`` sends ``x-user-api-key`` on a project-only operation, and
    ``ProjectAuth`` sends ``x-api-key`` on a user-only one: the declared
    schemes do not move a fixed mode."""
    client = Composio(auth=auth, base_url=BASE_URL)
    try:
        placed = {
            name: found
            for name, found in credential_headers(prepare(client, "get", path).headers).items()
            if found
        }
        assert placed == {header: value}
    finally:
        client.close()


def test_a_fixed_mode_does_not_read_the_table_at_all(monkeypatch: pytest.MonkeyPatch) -> None:
    """Not just the same answer: the selector is never asked."""

    def fail(*_args: object) -> str:
        raise AssertionError("a fixed mode consulted select_scheme")

    monkeypatch.setattr(_base_client, "select_scheme", fail)
    client = Composio(auth=UserAuth(USER_KEY), base_url=BASE_URL)
    try:
        assert prepare(client, "get", "/api/v3.1/org/list").headers["x-user-api-key"] == USER_KEY
    finally:
        client.close()


@pytest.mark.usefixtures("synthetic_table")
def test_the_scheme_is_decided_once_and_survives_the_hop(respx_mock: respx.MockRouter) -> None:
    """A redirect target is chosen by the server, so it must not be able to
    change which of the caller's credentials goes out. The scheme is resolved
    from the operation the *caller* invoked and carried through the chain."""
    respx_mock.get(f"{BASE_URL}/user_scoped").mock(
        return_value=httpx.Response(307, headers={"location": f"{BASE_URL}/project_scoped"})
    )
    hop = respx_mock.get(f"{BASE_URL}/project_scoped").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )

    client = Composio(auth=AutoAuth(project=API_KEY, user=USER_KEY), base_url=BASE_URL)
    try:
        client._request("get", "/user_scoped", cast_to=Echo)
    finally:
        client.close()

    headers = dict(hop.calls.last.request.headers)
    assert credential_headers(headers) == {
        "x-api-key": None,
        "x-user-api-key": USER_KEY,
        "x-org-api-key": None,
    }


# ---- a caller cannot place a credential beside `auth` ----


@pytest.mark.parametrize("name", ["x-api-key", "x-user-api-key", "X-Org-Api-Key"])
def test_a_configured_auth_reserves_every_credential_header(name: str) -> None:
    """Two credential headers is a 401, and a header ``auth`` writes cannot also
    come through a generic source -- including the in-place ``x-api-key``
    override the client allowed before ``auth``."""
    with pytest.raises(ComposioError, match=r"is set by `auth`"):
        Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL, default_headers={name: USER_KEY})


def test_no_auth_leaves_the_credential_names_to_the_caller() -> None:
    client = Composio(auth=NoAuth(), base_url=BASE_URL, default_headers={"x-user-api-key": USER_KEY})
    try:
        assert credential_headers(prepare(client, "get", "/echo").headers) == {
            "x-api-key": None,
            "x-user-api-key": USER_KEY,
            "x-org-api-key": None,
        }
    finally:
        client.close()


# ---- every configured credential is held to rules 1 and 2 ----


def test_rule_1_covers_a_client_holding_only_a_user_key() -> None:
    with pytest.raises(ComposioError, match="must use HTTPS"):
        Composio(auth=UserAuth(USER_KEY), base_url="http://api.example.com")


def test_rule_1_covers_a_client_holding_only_an_org_key() -> None:
    with pytest.raises(ComposioError, match="must use HTTPS"):
        AsyncComposio(auth=OrganizationAuth(ORG_KEY), base_url="http://api.example.com")


def test_rule_1_covers_a_provider_before_it_is_ever_called() -> None:
    def provider() -> str:
        raise AssertionError("rule 1 is decided without the key")

    with pytest.raises(ComposioError, match="must use HTTPS"):
        Composio(auth=ProjectAuth(provider), base_url="http://api.example.com")


def test_rule_1_still_leaves_a_wholly_uncredentialed_client_alone() -> None:
    client = Composio(auth=NoAuth(), base_url="http://api.example.com")
    assert client.base_url == "http://api.example.com"
    client.close()


def test_rule_2_drops_the_user_key_off_origin() -> None:
    client = Composio(auth=UserAuth(USER_KEY), base_url=BASE_URL)
    try:
        prepared = prepare(client, "get", ".evil.example/user_scoped")
        assert prepared.url == "https://api.test.evil.example/user_scoped"
        assert credential_headers(prepared.headers) == {
            "x-api-key": None,
            "x-user-api-key": None,
            "x-org-api-key": None,
        }
    finally:
        client.close()


def test_the_client_exposes_its_auth_mode_and_no_key() -> None:
    """Changing the credential is ``with_options(auth=...)``; nothing reads one back."""
    client = Composio(auth=AutoAuth(project=API_KEY, user=lambda: USER_KEY), base_url=BASE_URL)
    try:
        assert client.auth_mode == "auto"
        assert not hasattr(client, "api_key")
        assert API_KEY not in repr(vars(client))
        derived = client.with_options(auth=UserAuth(USER_KEY))
        assert derived.auth_mode == "user"
    finally:
        client.close()


# ---- method-level header parameters ----
#
# Four operations declare a header parameter. The credential and scope ones go
# to the kernel on the operation channel (`operation_headers=`), covered in
# test_auth.py; an ordinary one, or any header a raw call names, is a generic
# method header and has to interact with the credential boundary the same way
# `request_options.headers` does.


def test_a_method_header_reaches_the_wire(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.get(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))

    client = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
    try:
        client._request("get", "/echo", cast_to=Echo, headers={"x-org-id": "org_nanoid"})
    finally:
        client.close()

    assert route.calls.last.request.headers["x-org-id"] == "org_nanoid"


def test_a_method_credential_header_is_refused_beside_auth(respx_mock: respx.MockRouter) -> None:
    """A raw call cannot reach the operation channel, so a credential name in
    its ``headers=`` is a generic header, and ``auth`` owns it."""
    route = respx_mock.get(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))

    client = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
    try:
        with pytest.raises(ComposioError, match=r"`x-user-api-key` header is set by `auth`"):
            client._request("get", "/echo", cast_to=Echo, headers={"x-user-api-key": USER_KEY})
    finally:
        client.close()

    assert route.call_count == 0


def test_request_options_headers_outrank_a_method_header(respx_mock: respx.MockRouter) -> None:
    """A method header names something the *operation* declares;
    ``request_options.headers`` is the caller's general escape hatch and stays
    the last word."""
    route = respx_mock.get(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))

    client = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
    try:
        client._request(
            "get",
            "/echo",
            cast_to=Echo,
            headers={"x-org-id": "from_method"},
            options=_base_client.RequestOptions(headers={"x-org-id": "from_options"}),
        )
    finally:
        client.close()

    assert route.calls.last.request.headers["x-org-id"] == "from_options"


def test_a_method_header_outranks_a_client_default(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.get(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))

    client = Composio(
        auth=ProjectAuth(API_KEY), base_url=BASE_URL, default_headers={"x-org-id": "from_default"}
    )
    try:
        client._request("get", "/echo", cast_to=Echo, headers={"x-org-id": "from_method"})
    finally:
        client.close()

    assert route.calls.last.request.headers["x-org-id"] == "from_method"


def test_a_none_method_header_deletes_a_client_default(respx_mock: respx.MockRouter) -> None:
    """``None`` deletes, everywhere a header source is merged."""
    route = respx_mock.get(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))

    client = Composio(
        auth=ProjectAuth(API_KEY), base_url=BASE_URL, default_headers={"x-org-id": "from_default"}
    )
    try:
        client._request("get", "/echo", cast_to=Echo, headers={"x-org-id": None})
    finally:
        client.close()

    assert "x-org-id" not in route.calls.last.request.headers


def test_a_method_credential_header_is_withdrawn_off_origin(respx_mock: respx.MockRouter) -> None:
    """Rule 3: under ``NoAuth`` the caller's own credential is legitimate on the
    URL the caller chose and dropped once the *server* has chosen one. A
    method-level header is the caller's, so it is withdrawn exactly as
    ``request_options.headers`` is."""
    respx_mock.get(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(307, headers={"location": "https://elsewhere.test/echo"})
    )
    hop = respx_mock.get("https://elsewhere.test/echo").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )

    client = Composio(auth=NoAuth(), base_url=BASE_URL)
    try:
        client._request(
            "get",
            "/echo",
            cast_to=Echo,
            headers={"x-user-api-key": USER_KEY, "x-org-id": "org_nanoid"},
        )
    finally:
        client.close()

    headers = dict(hop.calls.last.request.headers)
    assert credential_headers(headers) == {
        "x-api-key": None,
        "x-user-api-key": None,
        "x-org-api-key": None,
    }
    # Only the *credential* is withdrawn; an ordinary declared header is not a
    # secret and travels with the request the server redirected.
    assert headers["x-org-id"] == "org_nanoid"


@pytest.mark.asyncio
async def test_the_async_client_places_a_method_header_too(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.get(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))

    client = AsyncComposio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
    try:
        await client._request("get", "/echo", cast_to=Echo, headers={"x-org-id": "org_nanoid"})
    finally:
        await client.aclose()

    assert route.calls.last.request.headers["x-org-id"] == "org_nanoid"
