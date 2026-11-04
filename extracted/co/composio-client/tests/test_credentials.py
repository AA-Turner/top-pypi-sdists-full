"""Credential-boundary tests — the Python peer of
``test/unit/credential-boundary.test.ts``.

The four authentication rules the design record makes part of the runtime
contract: HTTPS-or-loopback for a credentialed origin, on-origin-only
attachment, no credential across an origin-changing redirect, and no
credential-bearing value in any message this client constructs.

Deliberate divergence from the Stainless oracle, which enforces none of it, so
this suite has no oracle by construction — like the interceptor-parity suite it
is written against the record, parallel to its TypeScript peer rather than
mechanically coupled to it.
"""

from __future__ import annotations

import warnings

import httpx
import pytest
import respx
from pydantic import BaseModel

from composio_client import (
    APIConnectionError,
    APIStatusError,
    AsyncComposio,
    Composio,
    ComposioDeprecationWarning,
    ComposioError,
    NoAuth,
    ProjectAuth,
    _base_client,
)
from composio_client._base_client import MAX_REDIRECTS
from composio_client._credentials import is_loopback_host

from .conftest import API_KEY, BASE_URL


class Echo(BaseModel):
    ok: bool


@pytest.fixture
def recorded_delays(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    """Replace the kernel sleep seam with a recorder so no test sleeps for real."""
    delays: list[float] = []
    monkeypatch.setattr(_base_client, "_sleep", delays.append)
    return delays


# ---- what counts as loopback ----


@pytest.mark.parametrize(
    "host",
    [
        "localhost",
        "LOCALHOST",
        "api.localhost",
        "127.0.0.1",
        "127.0.0.53",
        "127.255.255.254",
        "::1",
        "[::1]",
        "0:0:0:0:0:0:0:1",
    ],
)
def test_loopback_accepted(host: str) -> None:
    assert is_loopback_host(host) is True


@pytest.mark.parametrize(
    "host",
    [
        # the unspecified address reaches the local host on some platforms and
        # fails on others; a rule that depends on the platform is not a rule
        "0.0.0.0",
        "localhost.evil.example",
        "notlocalhost",
        "128.0.0.1",
        "10.0.0.1",
        "192.168.1.1",
        "::ffff:127.0.0.1",
        "::ffff:7f00:1",
        "example.com",
    ],
)
def test_loopback_rejected(host: str) -> None:
    assert is_loopback_host(host) is False


# ---- rule 1: a credentialed origin must use HTTPS ----


def test_plain_http_origin_with_api_key_is_refused() -> None:
    with pytest.raises(ComposioError, match="must use HTTPS"):
        Composio(auth=ProjectAuth(API_KEY), base_url="http://api.example.com")


def test_refusal_names_the_accepted_loopback_set() -> None:
    with pytest.raises(ComposioError, match=r"127\.0\.0\.0/8"):
        Composio(auth=ProjectAuth(API_KEY), base_url="http://0.0.0.0:9900")


def test_non_http_scheme_with_api_key_is_refused() -> None:
    with pytest.raises(ComposioError, match="must use HTTPS"):
        Composio(auth=ProjectAuth(API_KEY), base_url="ftp://api.example.com")


@pytest.mark.parametrize(
    "base_url",
    [
        "http://localhost:9900",
        "http://127.0.0.1:3000",
        "http://127.0.0.2:3000",
        "http://[::1]:9900",
        "http://api.localhost:9900",
        "https://api.example.com",
    ],
)
def test_credentialed_origins_accepted(base_url: str) -> None:
    client = Composio(auth=ProjectAuth(API_KEY), base_url=base_url)
    assert client.auth_mode == "project"
    client.close()


def test_sanctioned_local_environment_still_works() -> None:
    client = Composio(auth=ProjectAuth(API_KEY), environment="local")
    assert client.base_url == "http://localhost:9900"
    client.close()


def test_uncredentialed_client_may_use_plain_http() -> None:
    client = Composio(auth=NoAuth(), base_url="http://api.example.com")
    assert client.base_url == "http://api.example.com"
    client.close()


def test_async_client_enforces_the_same_rule() -> None:
    with pytest.raises(ComposioError, match="must use HTTPS"):
        AsyncComposio(auth=ProjectAuth(API_KEY), base_url="http://api.example.com")


def test_base_url_is_read_only(client: Composio) -> None:
    with pytest.raises(AttributeError):
        client.base_url = "http://api.example.com"  # type: ignore[misc]
    with pytest.raises(ComposioError, match="must use HTTPS"):
        client.with_options(base_url="http://api.example.com")


# ---- rule 2: attached only on the configured origin ----


def test_key_is_attached_on_origin(client: Composio) -> None:
    prepared = client._prepare(
        "get", "/echo", body=None, body_model=None, query=None, headers=None, options=None
    )
    assert prepared.headers["x-api-key"] == API_KEY


@pytest.mark.parametrize(
    ("path", "expected_url"),
    [
        # a path that does not begin with `/` extends the *authority*, not the
        # path: an attacker-registrable host under a domain they own
        (".evil.example/x", "https://api.test.evil.example/x"),
        # httpx, unlike fetch, happily dispatches a URL with userinfo
        ("@evil.example/x", "https://api.test@evil.example/x"),
        # a port change is an origin change
        (":8443/x", "https://api.test:8443/x"),
    ],
)
def test_key_is_dropped_off_origin(client: Composio, path: str, expected_url: str) -> None:
    prepared = client._prepare(
        "get", path, body=None, body_model=None, query=None, headers=None, options=None
    )
    assert prepared.url == expected_url
    assert "x-api-key" not in prepared.headers
    # the request is still prepared: the record states an attachment rule, not
    # an error, and an off-origin fetch can be legitimate (presigned
    # upload/download URLs live on a storage origin)
    assert prepared.headers["accept"] == "application/json"


def test_key_is_dropped_off_a_loopback_origin_too() -> None:
    client = Composio(auth=ProjectAuth(API_KEY), base_url="http://localhost")
    prepared = client._prepare(
        "get", ".evil.example/x", body=None, body_model=None, query=None, headers=None, options=None
    )
    assert prepared.url == "http://localhost.evil.example/x"
    assert "x-api-key" not in prepared.headers
    client.close()


# ---- rule 3: no credential across an origin-changing redirect ----


def _redirect(location: str, status_code: int = 302) -> httpx.Response:
    return httpx.Response(status_code, headers={"location": location})


@respx.mock
def test_same_origin_redirect_is_followed_with_the_credential(client: Composio) -> None:
    start = respx.get(f"{BASE_URL}/echo").mock(return_value=_redirect(f"{BASE_URL}/moved"))
    moved = respx.get(f"{BASE_URL}/moved").mock(return_value=httpx.Response(200, json={"ok": True}))

    assert client._request("get", "/echo", cast_to=Echo).ok is True

    assert start.call_count == 1
    assert moved.call_count == 1
    assert moved.calls.last.request.headers["x-api-key"] == API_KEY


@respx.mock
def test_relative_location_resolves_against_the_hop_it_arrived_on(client: Composio) -> None:
    respx.get(f"{BASE_URL}/echo").mock(return_value=_redirect("/moved"))
    moved = respx.get(f"{BASE_URL}/moved").mock(return_value=httpx.Response(200, json={"ok": True}))

    client._request("get", "/echo", cast_to=Echo)

    assert moved.call_count == 1


@respx.mock
def test_origin_changing_redirect_is_followed_without_the_credential(client: Composio) -> None:
    respx.get(f"{BASE_URL}/echo").mock(return_value=_redirect("https://evil.example/x"))
    target = respx.get("https://evil.example/x").mock(return_value=httpx.Response(200, json={"ok": True}))

    client._request("get", "/echo", cast_to=Echo)

    # the hop is still made — the rule is about what rides along, not about
    # refusing to hop
    assert target.call_count == 1
    assert "x-api-key" not in target.calls.last.request.headers
    assert target.calls.last.request.headers["accept"] == "application/json"


@respx.mock
def test_callers_own_credential_headers_are_withdrawn_on_an_origin_change() -> None:
    """Rule 2 leaves these alone on the URL the *caller* chose; a redirect
    target is chosen by the server, so the same consent does not extend."""
    start = respx.get(f"{BASE_URL}/echo").mock(return_value=_redirect("https://evil.example/x"))
    target = respx.get("https://evil.example/x").mock(return_value=httpx.Response(200, json={"ok": True}))
    client = Composio(
        auth=ProjectAuth(API_KEY),
        base_url=BASE_URL,
        default_headers={"authorization": "Bearer caller-token", "cookie": "session=abc"},
    )

    client._request("get", "/echo", cast_to=Echo)

    assert start.calls.last.request.headers["authorization"] == "Bearer caller-token"
    assert "authorization" not in target.calls.last.request.headers
    assert "cookie" not in target.calls.last.request.headers
    client.close()


@respx.mock
def test_the_specs_other_two_credential_schemes_are_withdrawn_too() -> None:
    """``UserApiKeyAuth`` and ``OrgApiKeyAuth``.

    Under ``NoAuth`` the credential names are ordinary headers a caller can
    place through ``default_headers``, so the withdrawal set has to cover them.
    Kept in step with the TypeScript twin.
    """
    start = respx.get(f"{BASE_URL}/echo").mock(return_value=_redirect("https://evil.example/x"))
    target = respx.get("https://evil.example/x").mock(return_value=httpx.Response(200, json={"ok": True}))
    client = Composio(
        auth=NoAuth(),
        base_url=BASE_URL,
        default_headers={"x-user-api-key": "uak_caller", "x-org-api-key": "oak_caller"},
    )

    client._request("get", "/echo", cast_to=Echo)

    assert start.calls.last.request.headers["x-user-api-key"] == "uak_caller"
    assert "x-user-api-key" not in target.calls.last.request.headers
    assert "x-org-api-key" not in target.calls.last.request.headers
    client.close()


@respx.mock
def test_credential_is_never_re_attached_after_the_chain_leaves(client: Composio) -> None:
    respx.get(f"{BASE_URL}/echo").mock(return_value=_redirect("https://evil.example/x"))
    respx.get("https://evil.example/x").mock(return_value=_redirect(f"{BASE_URL}/back"))
    back = respx.get(f"{BASE_URL}/back").mock(return_value=httpx.Response(200, json={"ok": True}))

    client._request("get", "/echo", cast_to=Echo)

    assert back.call_count == 1
    assert "x-api-key" not in back.calls.last.request.headers


@respx.mock
@pytest.mark.parametrize(
    ("status_code", "expected_method"),
    [(303, "GET"), (302, "GET"), (307, "POST"), (308, "POST")],
)
def test_redirect_method_rewrite(client: Composio, status_code: int, expected_method: str) -> None:
    respx.post(f"{BASE_URL}/echo").mock(return_value=_redirect(f"{BASE_URL}/moved", status_code))
    moved = respx.route(url=f"{BASE_URL}/moved").mock(return_value=httpx.Response(200, json={"ok": True}))

    client._request("post", "/echo", cast_to=Echo, body={"a": 1})

    request = moved.calls.last.request
    assert request.method == expected_method
    if expected_method == "GET":
        assert request.read() == b""
        assert "content-type" not in request.headers
    else:
        assert request.read() == b'{"a":1}'
        assert request.headers["content-type"] == "application/json"


@respx.mock
def test_3xx_without_a_location_is_handed_back(client: Composio) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(return_value=httpx.Response(302))

    with pytest.raises(APIStatusError) as excinfo:
        client._request("get", "/echo", cast_to=Echo)

    assert excinfo.value.status_code == 302
    assert route.call_count == 1


@respx.mock
def test_3xx_pointing_at_an_unusable_scheme_is_handed_back(client: Composio) -> None:
    # `ftp:` rather than TypeScript's `data:` — httpx precomputes
    # `response.next_request` even with `follow_redirects=False`, so a
    # `Location` it cannot parse into a request raises `httpx.InvalidURL`
    # before the kernel ever sees the response. Noted in `_credentials.py` as
    # an httpx-side asymmetry; the rule under test is the same one.
    route = respx.get(f"{BASE_URL}/echo").mock(return_value=_redirect("ftp://evil.example/x"))

    with pytest.raises(APIStatusError) as excinfo:
        client._request("get", "/echo", cast_to=Echo)

    assert excinfo.value.status_code == 302
    assert route.call_count == 1


@respx.mock
def test_redirect_loop_terminates_at_the_hop_limit(client: Composio) -> None:
    route = respx.get(f"{BASE_URL}/loop").mock(return_value=_redirect(f"{BASE_URL}/loop"))

    with pytest.raises(APIConnectionError, match="redirected more than 20 times"):
        client._request("get", "/loop", cast_to=Echo)

    # 21 hops: the original request plus the 20 the budget allows
    assert route.call_count == MAX_REDIRECTS + 1


@respx.mock
def test_a_chain_does_not_spend_the_retry_budget() -> None:
    """A chain is one attempt, not one attempt per hop — so it works with
    ``max_retries=0``."""
    respx.get(f"{BASE_URL}/echo").mock(return_value=_redirect(f"{BASE_URL}/one"))
    respx.get(f"{BASE_URL}/one").mock(return_value=_redirect(f"{BASE_URL}/two"))
    two = respx.get(f"{BASE_URL}/two").mock(return_value=httpx.Response(200, json={"ok": True}))

    client = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL, max_retries=0)
    assert client._request("get", "/echo", cast_to=Echo).ok is True

    assert two.call_count == 1
    client.close()


@respx.mock
def test_a_retry_re_issues_the_original_request_chain_and_all(
    recorded_delays: list[float],
) -> None:
    start = respx.get(f"{BASE_URL}/echo").mock(return_value=_redirect(f"{BASE_URL}/moved"))
    moved = respx.get(f"{BASE_URL}/moved").mock(
        side_effect=[httpx.Response(500, json={}), httpx.Response(200, json={"ok": True})]
    )

    client = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL, max_retries=1)
    assert client._request("get", "/echo", cast_to=Echo).ok is True

    assert start.call_count == 2
    assert moved.call_count == 2
    assert len(recorded_delays) == 1
    client.close()


@respx.mock
def test_an_injected_client_cannot_hand_the_hop_back_to_httpx() -> None:
    """The only way this rule could have been flipped: a caller-supplied
    ``http_client`` with ``follow_redirects=True``. The kernel passes the flag
    per request, which wins over the client default, so the hop is still the
    kernel's — and still credential-free."""
    respx.get(f"{BASE_URL}/echo").mock(return_value=_redirect("https://evil.example/x"))
    target = respx.get("https://evil.example/x").mock(return_value=httpx.Response(200, json={"ok": True}))

    client = Composio(
        auth=ProjectAuth(API_KEY),
        base_url=BASE_URL,
        http_client=httpx.Client(follow_redirects=True),
    )
    client._request("get", "/echo", cast_to=Echo)

    assert target.call_count == 1
    assert "x-api-key" not in target.calls.last.request.headers
    client.close()


@respx.mock
def test_deprecation_notice_fires_once_per_call_not_once_per_hop(client: Composio) -> None:
    """The once-per-logical-call guarantee the interceptor is built on: the
    chain lives inside one attempt, so the single response exit is reached
    once."""
    respx.get(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(
            302, headers={"location": f"{BASE_URL}/moved", "deprecation": "@1688169599"}
        )
    )
    respx.get(f"{BASE_URL}/moved").mock(
        return_value=httpx.Response(200, headers={"deprecation": "@1688169599"}, json={"ok": True})
    )

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        client._request("get", "/echo", cast_to=Echo)

    assert len([w for w in caught if issubclass(w.category, ComposioDeprecationWarning)]) == 1


@respx.mock
def test_uncredentialed_client_still_follows_redirects() -> None:
    """TypeScript delegates this case to ``fetch`` (the only way a browser can
    follow a redirect); Python has no browser and no opaque redirect, so it
    keeps the hand-rolled loop — and would lose the named, terminal
    ``APIConnectionError`` on a loop if it delegated, since
    ``httpx.TooManyRedirects`` is a ``RequestError`` and would be retried. The
    *behavior* under test is the one both languages owe."""
    respx.get(f"{BASE_URL}/echo").mock(return_value=_redirect("https://storage.example/presigned"))
    target = respx.get("https://storage.example/presigned").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )

    client = Composio(auth=NoAuth(), base_url=BASE_URL)
    assert client._request("get", "/echo", cast_to=Echo).ok is True

    assert target.call_count == 1
    assert "x-api-key" not in target.calls.last.request.headers
    client.close()


@respx.mock
async def test_async_redirect_follows_without_the_credential(async_client: AsyncComposio) -> None:
    respx.get(f"{BASE_URL}/echo").mock(return_value=_redirect("https://evil.example/x"))
    target = respx.get("https://evil.example/x").mock(return_value=httpx.Response(200, json={"ok": True}))

    await async_client._request("get", "/echo", cast_to=Echo)

    assert target.call_count == 1
    assert "x-api-key" not in target.calls.last.request.headers


@respx.mock
async def test_async_same_origin_redirect_keeps_the_credential(
    async_client: AsyncComposio,
) -> None:
    respx.get(f"{BASE_URL}/echo").mock(return_value=_redirect(f"{BASE_URL}/moved"))
    moved = respx.get(f"{BASE_URL}/moved").mock(return_value=httpx.Response(200, json={"ok": True}))

    await async_client._request("get", "/echo", cast_to=Echo)

    assert moved.calls.last.request.headers["x-api-key"] == API_KEY


# ---- rule 4: no credential-bearing value in any message ----


@respx.mock
def test_status_error_message_carries_no_credential() -> None:
    respx.get(f"{BASE_URL}/echo").mock(return_value=httpx.Response(401, json={"error": {"message": "nope"}}))
    client = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)

    with pytest.raises(APIStatusError) as excinfo:
        client._request("get", "/echo", cast_to=Echo, query={"access_token": "sk_query_secret"})

    message = str(excinfo.value)
    assert "401" in message
    assert API_KEY not in message
    assert "sk_query_secret" not in message
    # the raw material is still reachable on the error for a caller who asks —
    # this rule is about what gets *printed*
    assert excinfo.value.response.request.headers["x-api-key"] == API_KEY
    client.close()


@respx.mock
def test_connection_error_message_carries_no_credential() -> None:
    respx.get(f"{BASE_URL}/echo").mock(side_effect=httpx.ConnectError)
    client = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL, max_retries=0)

    with pytest.raises(ComposioError) as excinfo:
        client._request("get", "/echo", cast_to=Echo, query={"access_token": "sk_query_secret"})

    message = str(excinfo.value)
    assert API_KEY not in message
    assert "sk_query_secret" not in message
    client.close()
