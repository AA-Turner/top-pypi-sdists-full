"""``require_authenticated_or_service`` under the organization-admission rule.

This dependency runs AFTER ``AuthMiddleware`` — as a per-route FastAPI
``Depends`` — to admit a server-to-server call carrying a shared secret
(``ADMIN_API_TOKEN``) plus an optional ``X-Matrx-User-Id`` "act as" header.
Because it runs structurally below the middleware, a service call that names
a real acting user used to become an authenticated ``AppContext`` with NO
organization at all — invisible to the organization gate (8e5ee0b93), which
only ever saw this request as anonymous.

These tests lock:

* a service call naming a real acting user with NO ``X-Organization-Id`` is
  refused (``organization_required``) — never silently admitted org-less
* the same call WITH an organization header is admitted, org-scoped
  (positive control)
* a userless, PURE-SERVICE call (no ``X-Matrx-User-Id``) is held to the
  SAME requirement — until 2026-09-17 it skipped the organization gate
  entirely, which is how a scraper call reached a tenant write path with no
  organization on the wire at all
* the organization is installed on the context as ``organization_admission
  ="none"`` — the honest marker; this primitive verifies no membership and
  must never claim "verified"
* a malformed ``X-Organization-Id`` is refused (``organization_malformed``),
  never silently dropped
* a route that opts out via ``organization_optional=True`` — the ONE lawful
  exemption, a route touching no tenant data — is admitted without a header,
  and still installs one that IS present
* declaring ``organization_optional=True`` with NO stated reason is a
  construction-time error — a silent opt-out is exactly the fallback this
  gate exists to ban
* a request AuthMiddleware already authenticated (with its own verified
  organization) passes through unchanged — this dependency never re-derives
  what the gate already decided
"""

from __future__ import annotations

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from matrx_connect.context.app_context import AppContext, get_app_context
from matrx_connect.middleware.auth import AuthMiddleware
from matrx_connect.service_auth import require_authenticated_or_service

SECRET = "test-approved-server-secret"
ACTING_USER = "88888888-8888-4888-8888-888888888888"
ORG_ID = "99999999-9999-4999-9999-999999999999"


def _app(dependency) -> TestClient:
    """Wraps ``AuthMiddleware`` around the probe, exactly as every real host
    (matrx-scraper included) does — ``request.state.context`` is ALWAYS set
    by the time a route dependency runs in production; a bare
    ``FastAPI()`` with no middleware in front is not a shape this dependency
    is ever actually exercised in."""
    app = FastAPI()

    @app.get("/probe", dependencies=[Depends(dependency)])
    async def probe() -> dict:
        ctx = get_app_context()
        return {"user_id": ctx.user_id, "organization_id": ctx.organization_id}

    app.add_middleware(AuthMiddleware, jwt_secret="unused-in-these-tests", log_requests=False)
    return TestClient(app)


def test_service_call_with_acting_user_and_no_organization_is_refused() -> None:
    dependency = require_authenticated_or_service(SECRET, require_user=True)
    client = _app(dependency)
    response = client.get(
        "/probe",
        headers={"Authorization": f"Bearer {SECRET}", "X-Matrx-User-Id": ACTING_USER},
    )
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "organization_required"


def test_service_call_with_acting_user_and_organization_is_admitted() -> None:
    """Positive control — a dependency that refused every service call would
    also 400 the test above for the wrong reason."""
    dependency = require_authenticated_or_service(SECRET, require_user=True)
    client = _app(dependency)
    response = client.get(
        "/probe",
        headers={
            "Authorization": f"Bearer {SECRET}",
            "X-Matrx-User-Id": ACTING_USER,
            "X-Organization-Id": ORG_ID,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == ACTING_USER
    assert body["organization_id"] == ORG_ID


def test_userless_pure_service_call_with_no_organization_is_refused() -> None:
    """THE FINDING (2026-09-17): the no-actor path skipped the organization
    requirement, so a pure server-to-server call was admitted with no tenant at
    all and each route fell back to a request-BODY field."""
    dependency = require_authenticated_or_service(SECRET, require_user=False)
    client = _app(dependency)
    response = client.get("/probe", headers={"Authorization": f"Bearer {SECRET}"})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "organization_required"
    assert "X-Organization-Id" in response.json()["detail"]["message"]


def test_userless_pure_service_call_with_an_organization_is_admitted() -> None:
    dependency = require_authenticated_or_service(SECRET, require_user=False)
    client = _app(dependency)
    response = client.get(
        "/probe",
        headers={"Authorization": f"Bearer {SECRET}", "X-Organization-Id": ORG_ID},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == ""
    assert body["organization_id"] == ORG_ID


def test_malformed_organization_header_is_refused() -> None:
    dependency = require_authenticated_or_service(SECRET, require_user=True)
    client = _app(dependency)
    response = client.get(
        "/probe",
        headers={
            "Authorization": f"Bearer {SECRET}",
            "X-Matrx-User-Id": ACTING_USER,
            "X-Organization-Id": "not-an-organization",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "organization_malformed"


def test_admitted_organization_is_never_claimed_verified() -> None:
    """This primitive proves no membership — it presents the organization the
    caller named, marked "none", exactly as the user-acting path does."""
    dependency = require_authenticated_or_service(SECRET, require_user=True)
    seen: dict[str, str] = {}

    app = FastAPI()

    @app.get("/probe2", dependencies=[Depends(dependency)])
    async def probe2() -> dict:
        ctx = get_app_context()
        seen["admission"] = ctx.organization_admission
        return {"organization_id": ctx.organization_id}

    app.add_middleware(AuthMiddleware, jwt_secret="unused-in-these-tests", log_requests=False)
    client = TestClient(app)
    response = client.get(
        "/probe2",
        headers={
            "Authorization": f"Bearer {SECRET}",
            "X-Matrx-User-Id": ACTING_USER,
            "X-Organization-Id": ORG_ID,
        },
    )
    assert response.status_code == 200
    assert seen["admission"] == "none"


def test_organization_optional_admits_without_a_header_when_stated() -> None:
    """The ONE lawful exemption: a route that touches no tenant data at all,
    declared at mount time WITH its reason."""
    dependency = require_authenticated_or_service(
        SECRET,
        require_user=True,
        organization_optional=True,
        organization_optional_reason="this route touches no tenant data",
    )
    client = _app(dependency)
    response = client.get(
        "/probe",
        headers={"Authorization": f"Bearer {SECRET}", "X-Matrx-User-Id": ACTING_USER},
    )
    assert response.status_code == 200
    assert response.json()["organization_id"] is None


def test_organization_optional_still_installs_a_header_that_is_present() -> None:
    """An honest caller's organization is never discarded."""
    dependency = require_authenticated_or_service(
        SECRET,
        require_user=True,
        organization_optional=True,
        organization_optional_reason="this route touches no tenant data",
    )
    client = _app(dependency)
    response = client.get(
        "/probe",
        headers={
            "Authorization": f"Bearer {SECRET}",
            "X-Matrx-User-Id": ACTING_USER,
            "X-Organization-Id": ORG_ID,
        },
    )
    assert response.status_code == 200
    assert response.json()["organization_id"] == ORG_ID


def test_organization_optional_without_a_reason_is_a_construction_error() -> None:
    with pytest.raises(ValueError, match="organization_optional_reason"):
        require_authenticated_or_service(SECRET, organization_optional=True)


@pytest.mark.asyncio
async def test_already_authenticated_context_passes_through_unchanged() -> None:
    """A request AuthMiddleware already admitted (organization included, or
    exempt) is not re-derived here — the dependency is a no-op for it."""
    dependency = require_authenticated_or_service(SECRET, require_user=True)

    class _FakeRequest:
        def __init__(self, ctx: AppContext) -> None:
            self.state = type("S", (), {"context": ctx})()
            self.headers: dict[str, str] = {}

    from matrx_connect.emitters.stream_emitter import StreamEmitter

    already_admitted = AppContext(
        emitter=StreamEmitter(debug=False),
        user_id="11111111-1111-4111-8111-111111111111",
        is_authenticated=True,
        organization_id=ORG_ID,
    )
    # Must not raise, and must not require ANY service credentials — the
    # fake request carries no Authorization header at all.
    await dependency(_FakeRequest(already_admitted))


class TestConfirmRequestOrganization:
    """The receiving half: a body value CONFIRMS the admitted organization or
    the request is refused. It never replaces it, and there is no fallback."""

    @staticmethod
    def _ctx(organization_id: str | None) -> AppContext:
        from matrx_connect.emitters.stream_emitter import StreamEmitter

        return AppContext(
            emitter=StreamEmitter(debug=False),
            user_id=ACTING_USER,
            is_authenticated=True,
            auth_type="token",
            organization_id=organization_id,
        )

    def test_body_value_that_agrees_confirms(self) -> None:
        from matrx_connect.service_auth import confirm_request_organization

        assert confirm_request_organization(self._ctx(ORG_ID), ORG_ID) == ORG_ID

    def test_no_body_value_returns_the_admitted_organization(self) -> None:
        from matrx_connect.service_auth import confirm_request_organization

        assert confirm_request_organization(self._ctx(ORG_ID)) == ORG_ID

    def test_disagreeing_body_value_is_a_conflict(self) -> None:
        from fastapi import HTTPException

        from matrx_connect.service_auth import confirm_request_organization

        other = "12345678-1234-4123-8123-123456789012"
        with pytest.raises(HTTPException) as exc:
            confirm_request_organization(self._ctx(ORG_ID), other)
        assert exc.value.status_code == 409
        assert exc.value.detail["code"] == "organization_context_mismatch"

    def test_context_without_an_organization_is_refused_not_defaulted(self) -> None:
        from fastapi import HTTPException

        from matrx_connect.service_auth import confirm_request_organization

        with pytest.raises(HTTPException) as exc:
            confirm_request_organization(self._ctx(None), ORG_ID)
        assert exc.value.status_code == 400
        assert exc.value.detail["code"] == "organization_required"
