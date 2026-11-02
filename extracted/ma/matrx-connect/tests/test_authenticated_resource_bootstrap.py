"""End-to-end proof for authenticated resource-bootstrap route admission."""

from __future__ import annotations

import asyncio
import time
from typing import Annotated

import jwt
import pytest
from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.testclient import TestClient

from matrx_connect import (
    AuthenticatedResourceRoute,
    authenticated_resource_bootstrap,
    authenticated_resource_routes,
    get_app_context,
)
from matrx_connect.middleware.auth import AuthMiddleware

JWT_SECRET = "test-secret-do-not-use-in-prod-test-secret-do-not-use-in-prod-AB"
USER_ID = "11111111-1111-4111-8111-111111111111"
MEMBER_ORG_ID = "22222222-2222-4222-8222-222222222222"
DENIED_ORG_ID = "33333333-3333-4333-8333-333333333333"


def _token(**claims: object) -> str:
    return jwt.encode(
        {"sub": USER_ID, "aud": "authenticated", "exp": int(time.time()) + 3600, **claims},
        JWT_SECRET,
        algorithm="HS256",
    )


async def _membership(user_id: str, claimed: str | None) -> str | None:
    if user_id == USER_ID and claimed == MEMBER_ORG_ID:
        return MEMBER_ORG_ID
    return None


def _client() -> tuple[TestClient, list[tuple[object, object]]]:
    app = FastAPI()
    observations: list[tuple[object, object]] = []

    outer = APIRouter(prefix="/virtual")
    resources = APIRouter(
        prefix="/notes",
        dependencies=[Depends(authenticated_resource_bootstrap)],
    )

    @resources.get("/{resource_id}/read")
    async def resource_read(
        request: Request,
        expected_organization_id: Annotated[str | None, Depends(authenticated_resource_bootstrap)],
    ) -> dict[str, str | None]:
        context = request.state.context
        observations.append((context, get_app_context()))
        return {
            "expected_organization_id": expected_organization_id,
            "context_organization_id": context.organization_id,
        }

    sibling = APIRouter(prefix="/notes")

    @sibling.get("/literal/sibling")
    async def literal_sibling() -> dict[str, bool]:
        return {"resource": True}

    outer.include_router(resources)
    outer.include_router(sibling)
    app.include_router(outer)

    # Same template, different method: only GET was marked by the nested
    # router dependency. This route remains subject to membership pre-refusal.
    @app.post("/virtual/notes/{resource_id}/read")
    async def same_path_post() -> dict[str, bool]:
        return {"post": True}

    @app.get("/virtual/notes/{resource_id}/read/extra")
    async def trailing_sibling() -> dict[str, bool]:
        return {"extra": True}

    declarations = authenticated_resource_routes(app, authenticated_resource_bootstrap)
    assert {(item.method, item.path) for item in declarations} == {
        ("GET", "/virtual/notes/{resource_id}/read"),
    }
    protected = AuthMiddleware(
        app,
        jwt_secret=JWT_SECRET,
        resolve_active_organization=_membership,
        authenticated_resource_routes=declarations,
        log_requests=False,
    )
    return TestClient(protected), observations


def _headers(token: str | None = None, organization: str | None = None) -> dict[str, str]:
    result: dict[str, str] = {}
    if token is not None:
        result["Authorization"] = f"Bearer {token}"
    if organization is not None:
        result["X-Organization-Id"] = organization
    return result


def test_nested_marked_route_allows_absent_header_without_replacing_context() -> None:
    client, observations = _client()
    response = client.get("/virtual/notes/record/read", headers=_headers(_token()))
    assert response.status_code == 200
    assert response.json() == {"expected_organization_id": None, "context_organization_id": None}
    assert len(observations) == 1
    assert observations[0][0] is observations[0][1]


def test_header_is_literal_claim_not_context_or_jwt_substitute() -> None:
    client, _ = _client()
    claim_only = client.get(
        "/virtual/notes/record/read",
        headers=_headers(_token(organization_id=MEMBER_ORG_ID)),
    )
    assert claim_only.status_code == 200
    assert claim_only.json()["expected_organization_id"] is None

    denied = client.get(
        "/virtual/notes/record/read",
        headers=_headers(_token(), DENIED_ORG_ID),
    )
    assert denied.status_code == 200
    assert denied.json()["expected_organization_id"] == DENIED_ORG_ID
    assert denied.json()["context_organization_id"] is None


@pytest.mark.parametrize("value", ["", "   ", "not-a-uuid"])
def test_empty_or_malformed_header_refuses_before_resource_handler(value: str) -> None:
    client, observations = _client()
    response = client.get(
        "/virtual/notes/record/read",
        headers=_headers(_token(), value),
    )
    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "resource_organization_claim_invalid"
    assert observations == []


def test_duplicate_header_refuses_before_resource_handler() -> None:
    client, observations = _client()
    response = client.get(
        "/virtual/notes/record/read",
        headers=[
            ("Authorization", f"Bearer {_token()}"),
            ("X-Organization-Id", MEMBER_ORG_ID),
            ("X-Organization-Id", MEMBER_ORG_ID),
        ],
    )
    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "resource_organization_claim_invalid"
    assert observations == []


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("POST", "/virtual/notes/record/read"),
        ("GET", "/virtual/notes/record/read/extra"),
        ("GET", "/virtual/notes/record%2Fother/read"),
        ("GET", "/virtual/notes/record%252Fother/read"),
    ],
)
def test_exact_resource_declaration_never_bypasses_on_sibling_or_encoded_path(
    method: str,
    path: str,
) -> None:
    client, observations = _client()
    response = client.request(method, path, headers=_headers(_token()))
    assert response.status_code in {400, 404}
    assert observations == []


def test_raw_path_normalization_never_reaches_the_marked_route() -> None:
    client, observations = _client()
    sent: list[dict[str, object]] = []

    async def receive() -> dict[str, object]:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: dict[str, object]) -> None:
        sent.append(message)

    asyncio.run(
        client.app(
            {
                "type": "http",
                "method": "GET",
                "scheme": "http",
                "path": "/virtual/notes/../notes/record/read",
                "raw_path": b"/virtual/notes/../notes/record/read",
                "query_string": b"",
                "headers": [(b"authorization", f"Bearer {_token()}".encode())],
                "client": ("127.0.0.1", 12345),
                "server": ("testserver", 80),
                "state": {},
            },
            receive,
            send,
        )
    )
    assert next(message["status"] for message in sent if message["type"] == "http.response.start") == 400
    assert observations == []


def test_literal_resource_sibling_and_anonymous_request_are_refused() -> None:
    client, _ = _client()
    sibling = client.get("/virtual/notes/literal/sibling", headers=_headers(_token()))
    assert sibling.status_code == 400
    anonymous = client.get("/virtual/notes/record/read")
    assert anonymous.status_code == 401


def test_normal_organization_free_and_tenant_routes_keep_their_original_behavior() -> None:
    app = FastAPI()

    @app.get("/health")
    async def health() -> dict[str, bool]:
        return {"ok": True}

    @app.get("/tenant")
    async def tenant() -> dict[str, bool]:
        return {"tenant": True}

    client = TestClient(
        AuthMiddleware(
            app,
            jwt_secret=JWT_SECRET,
            resolve_active_organization=_membership,
            log_requests=False,
        )
    )
    assert client.get("/health", headers=_headers(_token())).status_code == 200
    assert client.get("/tenant", headers=_headers(_token())).status_code == 400
    assert client.get("/tenant", headers=_headers(_token(), MEMBER_ORG_ID)).status_code == 200


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("get", "/resources/{resource_id}"),
        ("GET", "resources/{resource_id}"),
        ("GET", "/resources/{resource_id:path}"),
        ("GET", "/resources/{resource_id}/"),
        ("GET", "/resources//{resource_id}"),
    ],
)
def test_invalid_resource_route_declarations_refuse_construction(method: str, path: str) -> None:
    with pytest.raises(ValueError):
        AuthenticatedResourceRoute(method, path)
