"""The lanes in ``AuthMiddleware._build_context`` run in ONE fixed order.

API key -> JWT -> organization -> a refused credential stays anonymous ->
fingerprint guest -> file-session cookie (GET byte routes) -> anonymous.

PF-AUTH S2 split the middleware into one mixin per lane; this pins the ORDER by
behaviour, not by reading source: every request below carries credentials for
several lanes at once, so the lane that answers (and the resolvers that were or
were not consulted) proves which lane ran first.
"""

from __future__ import annotations

import time

import jwt as pyjwt
import pytest
from starlette.requests import Request

from matrx_connect.middleware import session_cookie as sc
from matrx_connect.middleware.auth import ApiKeyIdentity, ApiKeyRefused, AuthMiddleware
from matrx_connect.middleware.session_cookie import mint_session_cookie_value

JWT_SECRET = "lane-order-secret-lane-order-secret-lane-order-secret-0123456789"
FP_SECRET = "lane-order-fingerprint-secret"
JWT_USER = "11111111-1111-4111-8111-111111111111"
KEY_USER = "22222222-2222-4222-8222-222222222222"
GUEST_USER = "33333333-3333-4333-8333-333333333333"
COOKIE_USER = "44444444-4444-4444-8444-444444444444"
KEY_ORG = "55555555-5555-4555-8555-555555555555"
MEMBER_ORG = "66666666-6666-4666-8666-666666666666"
GOOD_KEY = "mx_live_good_" + "k" * 40
REFUSED_KEY = "mx_live_revoked_" + "r" * 40
BYTES_PATH = "/files/abc/download"
FINGERPRINT = "fp-lane-order-browser"


@pytest.fixture(autouse=True)
def _isolate_registered_secret():
    """AuthMiddleware construction mutates the module-global cookie secret."""
    saved = (sc._registered_secret, sc._registered_secret_is_ephemeral)
    yield
    sc._registered_secret, sc._registered_secret_is_ephemeral = saved


class _Calls:
    def __init__(self) -> None:
        self.api_key: list[str] = []
        self.org: list[tuple[str, str | None]] = []
        self.guest: list[str] = []


def _middleware(calls: _Calls, *, guest_known: bool = True) -> AuthMiddleware:
    async def resolve_api_key(token: str) -> ApiKeyIdentity | None:
        calls.api_key.append(token)
        if token == REFUSED_KEY:
            raise ApiKeyRefused("This key was revoked.")
        if token == GOOD_KEY:
            return ApiKeyIdentity(user_id=KEY_USER, organization_id=KEY_ORG, key_id="k1")
        return None

    async def resolve_org(user_id: str, claimed: str | None) -> str | None:
        calls.org.append((user_id, claimed))
        return claimed if (user_id, claimed) == (JWT_USER, MEMBER_ORG) else None

    async def resolve_guest(fp, ip, ua, *, route=None) -> str:
        calls.guest.append(fp)
        return GUEST_USER

    async def has_guest_identity(fp: str) -> bool:
        return guest_known

    return AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        resolve_api_key=resolve_api_key,
        resolve_active_organization=resolve_org,
        resolve_guest=resolve_guest,
        has_guest_identity=has_guest_identity,
        guest_fingerprint_secret=FP_SECRET,
        log_requests=False,
        token_cache_ttl_seconds=0,
    )


def _jwt() -> str:
    return pyjwt.encode(
        {"sub": JWT_USER, "aud": "authenticated", "exp": int(time.time()) + 600},
        JWT_SECRET,
        algorithm="HS256",
    )


def _request(
    *,
    method: str = "GET",
    path: str = BYTES_PATH,
    bearer: str | None = None,
    org: str | None = None,
    fingerprint: bool = False,
    cookie: bool = False,
) -> Request:
    headers: list[tuple[bytes, bytes]] = []
    if bearer is not None:
        headers.append((b"authorization", f"Bearer {bearer}".encode()))
    if org is not None:
        headers.append((b"x-organization-id", org.encode()))
    if fingerprint:
        headers.append((b"x-fingerprint-id", FINGERPRINT.encode()))
    if cookie:
        value = mint_session_cookie_value(COOKIE_USER, FP_SECRET.encode("utf-8"))
        headers.append((b"cookie", f"{sc.SESSION_COOKIE_NAME}={value}".encode()))
    return Request(
        {
            "type": "http",
            "http_version": "1.1",
            "method": method,
            "scheme": "https",
            "path": path,
            "raw_path": path.encode(),
            "query_string": b"",
            "headers": headers,
            "client": ("127.0.0.1", 4242),
            "server": ("testserver", 443),
        }
    )


async def _build(calls: _Calls, request: Request, **kw):
    return await _middleware(calls, **kw)._build_context(request)


@pytest.mark.asyncio
async def test_api_key_lane_answers_before_every_other_lane() -> None:
    calls = _Calls()
    ctx = await _build(calls, _request(bearer=GOOD_KEY, fingerprint=True, cookie=True))
    assert ctx.auth_type == "api_key"
    assert ctx.user_id == KEY_USER
    assert ctx.organization_id == KEY_ORG
    assert calls.api_key == [GOOD_KEY]
    assert calls.org == []  # a service key's org is its own; the membership lane never ran
    assert calls.guest == []


@pytest.mark.asyncio
async def test_jwt_then_organization_answer_before_guest_and_cookie() -> None:
    calls = _Calls()
    ctx = await _build(
        calls, _request(bearer=_jwt(), org=MEMBER_ORG, fingerprint=True, cookie=True)
    )
    assert ctx.auth_type == "token"
    assert ctx.user_id == JWT_USER
    # The organization lane ran AFTER the JWT lane: it saw the JWT's identity.
    assert calls.org == [(JWT_USER, MEMBER_ORG)]
    assert ctx.organization_id == MEMBER_ORG
    assert ctx.organization_admission == "verified"
    assert calls.api_key == []  # a JWT is not mx_-shaped: the key lane declined it
    assert calls.guest == []


@pytest.mark.asyncio
async def test_organization_refusal_is_still_the_jwt_lane_not_a_guest() -> None:
    calls = _Calls()
    ctx = await _build(
        calls, _request(bearer=_jwt(), org=KEY_ORG, fingerprint=True, cookie=True)
    )
    assert ctx.auth_type == "token"
    assert ctx.user_id == JWT_USER
    assert ctx.organization_id is None
    assert ctx.organization_admission == "denied"
    assert calls.guest == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "bearer",
    [REFUSED_KEY, "mx_live_unknown_" + "u" * 40, "not.a-valid.jwt", "garbage"],
    ids=["refused_key", "unknown_key", "bad_jwt", "not_a_jwt"],
)
async def test_a_refused_credential_stays_anonymous(bearer: str) -> None:
    calls = _Calls()
    ctx = await _build(calls, _request(bearer=bearer, fingerprint=True, cookie=True))
    assert not ctx.user_id
    assert not ctx.is_authenticated
    assert ctx.auth_type not in ("fingerprint", "cookie")
    assert calls.guest == []
    assert calls.org == []


@pytest.mark.asyncio
async def test_guest_lane_answers_before_the_cookie_lane() -> None:
    calls = _Calls()
    ctx = await _build(calls, _request(fingerprint=True, cookie=True))
    assert ctx.auth_type == "fingerprint"
    assert ctx.user_id == GUEST_USER
    assert calls.guest == [FINGERPRINT]


@pytest.mark.asyncio
async def test_a_declining_guest_lane_falls_through_to_the_cookie_lane() -> None:
    calls = _Calls()
    ctx = await _build(calls, _request(fingerprint=True, cookie=True), guest_known=False)
    assert calls.guest == []  # a read from an unknown fingerprint mints nothing
    assert ctx.auth_type == "cookie"
    assert ctx.user_id == COOKIE_USER


@pytest.mark.asyncio
async def test_cookie_lane_is_get_byte_routes_only_then_anonymous() -> None:
    calls = _Calls()
    on_bytes = await _build(calls, _request(cookie=True))
    assert (on_bytes.auth_type, on_bytes.user_id) == ("cookie", COOKIE_USER)

    off_route = await _build(calls, _request(cookie=True, path="/files/abc"))
    assert not off_route.user_id
    as_post = await _build(calls, _request(cookie=True, method="POST"))
    assert not as_post.user_id


@pytest.mark.asyncio
async def test_nothing_presented_is_anonymous() -> None:
    calls = _Calls()
    ctx = await _build(calls, _request(method="POST", path="/anything"))
    assert not ctx.user_id
    assert not ctx.is_authenticated
    assert (calls.api_key, calls.org, calls.guest) == ([], [], [])
