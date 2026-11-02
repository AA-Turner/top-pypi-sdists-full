"""The organization admission gate — the top-of-stack rule.

Identity has always been undeniable because ``AuthMiddleware`` resolves it
before anything routes. Organization was not: it was resolved only when a
caller happened to send one, so every route grew its own late check and a
missing organization surfaced differently (or not at all) in each feature.

These tests lock the rule in one place:

* an authenticated request with NO organization is refused BEFORE routing —
  the downstream app is never entered, and the body carries the
  ``organization_required`` code plus the header the caller must send
* the same request WITH a verified organization is admitted (the positive
  control — without it, a gate that refuses everything would also "pass")
* an ANONYMOUS request is not org-refused: it belongs to the route's own 401,
  and telling a signed-out caller to pick an organization sends them to fix
  the wrong thing
* the exempt paths (liveness, sign-in, the identity probe a client uses before
  it can know its organization) stay reachable
* an exempt PREFIX does not accidentally exempt a longer feature path
* the guest and cookie lanes are ADMITTED without an organization — neither
  can name one (no membership to verify; a browser <img> tag cannot send
  headers at all), so the rule applies only to lanes that can state a tenant
* the gate refuses a claimed organization the resolver did not verify: a
  header is a claim, never a grant — and it refuses with ``organization_forbidden``,
  not ``organization_required``, because a caller who DID name an organization
  must never be told to go name one (``_ADMISSION_REASON_CODES``, 2026-09-07)
"""

from __future__ import annotations

import json
import time

import jwt
import pytest
from matrx_connect.middleware.auth import AuthMiddleware
from matrx_connect.middleware import auth as auth_module

JWT_SECRET = "test-secret-do-not-use-in-prod-test-secret-do-not-use-in-prod-AB"
USER_ID = "11111111-1111-4111-8111-111111111111"
ORG_ID = "33333333-3333-4333-8333-333333333333"
UNVERIFIED_ORG_ID = "44444444-4444-4444-8444-444444444444"


class _App:
    """Terminal ASGI app that records whether it was ever entered."""

    def __init__(self) -> None:
        self.entered = False
        self.context = None

    async def __call__(self, scope, receive, send) -> None:
        self.entered = True
        state = scope.get("state") or {}
        self.context = state.get("context")
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})


def _token(**claims) -> str:
    payload = {
        "sub": USER_ID,
        "aud": "authenticated",
        "exp": int(time.time()) + 3600,
        **claims,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


async def _member_only_resolver(user_id: str, claimed: str | None) -> str | None:
    """Verifies membership: ORG_ID is real for this user, nothing else is."""
    if claimed == ORG_ID and user_id == USER_ID:
        return ORG_ID
    return None


def _scope(path: str, headers: dict[str, str]) -> dict:
    return {
        "type": "http",
        "method": "GET",
        "path": path,
        "query_string": b"",
        "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
        "client": ("127.0.0.1", 12345),
        "state": {},
    }


async def _receive() -> dict:
    return {"type": "http.request", "body": b"", "more_body": False}


async def _call(
    mw: AuthMiddleware, path: str, headers: dict[str, str]
) -> tuple[int, bytes]:
    sent: list[dict] = []

    async def send(message: dict) -> None:
        sent.append(message)

    await mw(_scope(path, headers), _receive, send)
    status = next(m["status"] for m in sent if m["type"] == "http.response.start")
    body = b"".join(m.get("body", b"") for m in sent if m["type"] == "http.response.body")
    return status, body


def _middleware(app: _App) -> AuthMiddleware:
    return AuthMiddleware(
        app,
        jwt_secret=JWT_SECRET,
        resolve_active_organization=_member_only_resolver,
        resolve_guest=_guest_resolver,
        log_requests=False,
    )


async def _guest_resolver(fingerprint: str, ip, user_agent, *, route=None) -> str:
    return "55555555-5555-4555-8555-555555555555"


@pytest.mark.asyncio
async def test_authenticated_request_without_organization_is_refused_before_routing() -> None:
    app = _App()
    mw = _middleware(app)
    status, body = await _call(mw, "/api/anything", {"authorization": f"Bearer {_token()}"})
    assert status == 400
    # The point of a top-of-stack gate: feature code never ran.
    assert app.entered is False
    detail = json.loads(body)
    assert detail["code"] == "organization_required"
    # The remedy names the exact header the caller must send.
    assert "X-Organization-Id" in detail["message"]


@pytest.mark.asyncio
async def test_host_exempt_bridge_shape_reaches_application_without_org() -> None:
    """A bootstrap handler may resolve its exact organization after admission."""
    app = _App()
    mw = AuthMiddleware(
        app,
        jwt_secret=JWT_SECRET,
        resolve_active_organization=_member_only_resolver,
        organization_exempt_paths=("/api/coding-sessions/bridge",),
        log_requests=False,
    )
    status, _ = await _call(
        mw,
        "/api/coding-sessions/bridge",
        {"authorization": f"Bearer {_token()}"},
    )

    assert status == 200
    assert app.entered is True


@pytest.mark.asyncio
async def test_expected_organization_denial_never_enters_error_repair_queue(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A deliberate 400 is WARNING control flow, never an ERROR incident."""
    emitted: list[dict[str, object]] = []

    def _capture(message: object, **kwargs: object) -> None:
        emitted.append({"message": message, **kwargs})

    monkeypatch.setattr(auth_module, "vcprint", _capture)
    app = _App()
    mw = _middleware(app)

    status, _ = await _call(
        mw, "/files/session", {"authorization": f"Bearer {_token()}"}
    )

    assert status == 400
    rejects = [entry for entry in emitted if "[AUTH][REJECT]" in str(entry["message"])]
    assert len(rejects) == 1
    assert rejects[0]["log_level"] == "WARNING"
    assert all(entry.get("log_level") != "ERROR" for entry in rejects)


@pytest.mark.asyncio
async def test_authenticated_request_with_verified_organization_is_admitted() -> None:
    """Positive control — a gate that refused everything would fail here."""
    app = _App()
    mw = _middleware(app)
    status, _ = await _call(
        mw,
        "/api/anything",
        {"authorization": f"Bearer {_token()}", "x-organization-id": ORG_ID},
    )
    assert status == 200
    assert app.entered is True
    assert app.context.organization_id == ORG_ID


@pytest.mark.asyncio
async def test_claimed_but_unverified_organization_is_refused() -> None:
    """A header is a claim. Membership is what grants it.

    And the refusal NAMES the situation. Until 2026-09-07 every admission
    failure answered with the single code ``organization_required`` — the same
    word for "you sent no organization" and for "you sent one you are not in" —
    so a caller could not tell a fixable mistake from a permanent denial, and
    three of the four situations were told to go choose an organization they
    had already chosen. ``_ADMISSION_REASON_CODES`` gave each situation its own
    code; this asserts the one this request earns.
    """
    app = _App()
    mw = _middleware(app)
    status, body = await _call(
        mw,
        "/api/anything",
        {"authorization": f"Bearer {_token()}", "x-organization-id": UNVERIFIED_ORG_ID},
    )
    assert status == 400
    assert app.entered is False
    detail = json.loads(body)
    assert detail["code"] == "organization_forbidden"
    # NOT the no-header code: a caller who DID name an organization must never
    # be told to name one.
    assert detail["code"] != "organization_required"
    # The sentence says why, and says it is not retryable. The id is a machine fact: it rides
    # `claimed_organization_id`, never the sentence (VERIFIER-31 D2, 2026-09-29).
    assert UNVERIFIED_ORG_ID not in detail["message"]
    assert detail["claimed_organization_id"] == UNVERIFIED_ORG_ID
    assert "not a member" in detail["message"]


@pytest.mark.asyncio
async def test_anonymous_request_is_not_organization_refused() -> None:
    app = _App()
    mw = _middleware(app)
    status, _ = await _call(mw, "/api/anything", {})
    # No identity → this is the route's 401 to answer, not the org gate's 400.
    assert status == 200
    assert app.entered is True


@pytest.mark.asyncio
async def test_guest_identity_is_admitted_without_an_organization() -> None:
    """A fingerprint guest CANNOT name an organization — there is no
    iam.memberships row to verify and no picker to choose from. Holding the
    guest lane to the org rule (as this test originally did) turned every
    anonymous surface into a 400 the caller could never satisfy. The org
    admission rule is for lanes that can state a tenant (JWT / API key)."""
    app = _App()
    mw = _middleware(app)
    status, _ = await _call(mw, "/api/anything", {"x-fingerprint-id": "fp-abc-123"})
    assert status == 200
    assert app.entered is True


@pytest.mark.asyncio
async def test_cookie_lane_is_admitted_without_an_organization() -> None:
    """The file-session cookie authenticates <img>/<video> byte GETs, and a
    browser tag CANNOT attach a header. Gating this lane silently 400s every
    private media render — the rule must never apply to it."""
    from matrx_connect.middleware.session_cookie import (
        SESSION_COOKIE_NAME,
        mint_session_cookie_value,
    )

    app = _App()
    mw = _middleware(app)
    cookie = mint_session_cookie_value(USER_ID, mw._guest_fp_secret)
    status, _ = await _call(
        mw,
        "/files/abc/download",
        {"cookie": f"{SESSION_COOKIE_NAME}={cookie}"},
    )
    assert status == 200
    assert app.entered is True


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["/health", "/docs", "/openapi.json", "/auth/whoami"])
async def test_exempt_paths_stay_reachable_without_an_organization(path: str) -> None:
    app = _App()
    mw = _middleware(app)
    status, _ = await _call(mw, path, {"authorization": f"Bearer {_token()}"})
    assert status == 200
    assert app.entered is True


@pytest.mark.asyncio
async def test_exempt_prefix_does_not_leak_into_a_longer_feature_path() -> None:
    """`/health` must not exempt `/healthcare/patients`."""
    app = _App()
    mw = _middleware(app, )
    status, _ = await _call(
        mw, "/healthcare/patients", {"authorization": f"Bearer {_token()}"}
    )
    assert status == 400
    assert app.entered is False


@pytest.mark.asyncio
async def test_host_declared_exemptions_replace_the_defaults() -> None:
    app = _App()
    mw = AuthMiddleware(
        app,
        jwt_secret=JWT_SECRET,
        resolve_active_organization=_member_only_resolver,
        organization_exempt_paths=("/probe",),
        log_requests=False,
    )
    admitted, _ = await _call(mw, "/probe", {"authorization": f"Bearer {_token()}"})
    assert admitted == 200
    refused, _ = await _call(mw, "/health", {"authorization": f"Bearer {_token()}"})
    assert refused == 400


@pytest.mark.asyncio
async def test_refusal_puts_its_reason_where_a_client_reads_it() -> None:
    """THE REASON MUST BE AT THE ROOT (2026-09-14).

    Failing-then-passing guard for a refusal that reached a person as "The
    server refused this request and sent no reason with it". The words were
    always computed — they were nested under a `detail` key, one level below
    every client's reader, so `body.user_message` and `body.message` were both
    undefined and the client fell back to its bare-status sentence.

    This asserts the wire shape the app's own error handler produces for the
    identical refusal raised from a route: `error` / `message` /
    `user_message` at the ROOT, alongside the situation extras.
    """
    app = _App()
    mw = _middleware(app)
    _, body = await _call(
        mw,
        "/seo/brands/6aa4a15c-63d2-4425-a510-037f6207ece8/strategy",
        {"authorization": f"Bearer {_token()}", "x-organization-id": UNVERIFIED_ORG_ID},
    )
    payload = json.loads(body)

    # Nothing is nested: the old shape's one key is gone, not kept alongside.
    assert "detail" not in payload

    assert payload["error"] == "organization_forbidden"
    assert payload["code"] == "organization_forbidden"
    # The sentence a PERSON sees names the situation and the remedy.
    assert "not a member of that organization" in payload["user_message"]
    assert "Switch to an organization you belong to" in payload["user_message"]
    # The diagnostic id is a field, never words in the sentence (VERIFIER-31 D2).
    assert UNVERIFIED_ORG_ID not in payload["message"]
    assert payload["organization_admission"] == "denied"
    assert payload["claimed_organization_id"] == UNVERIFIED_ORG_ID

    # And the client's own reader finds a reason, so it never reaches the
    # "sent no reason" fallback (matrx-frontend lib/api/call-api.ts
    # extractServerErrorMessage: user_message → message → details[] → detail).
    reason = payload.get("user_message") or payload.get("message")
    assert isinstance(reason, str) and reason.strip()
