"""TeamSecretMiddleware exempts the Jira OAuth callback route -- Atlassian's
browser redirect after consent cannot send an X-Team-Secret header (it's a
plain HTTP redirect carrying only code/state query params Atlassian
controls). That route's real security boundary is the signed `state`
parameter, not this header gate. GitHub issue #296."""

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from src.api.middleware.team_secret import (
    TeamSecretMiddleware,
    require_team_secret,
)


def _make_app():
    app = FastAPI()
    app.add_middleware(TeamSecretMiddleware)

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    @app.get("/api/v1/boards/oauth/jira/callback")
    async def callback():
        return {"ok": True}

    @app.get("/api/v1/organizations/org-1/boards")
    async def boards():
        return []

    return app


@pytest.fixture(autouse=True)
def team_secret_env(monkeypatch):
    monkeypatch.setenv("TEAM_ACCESS_SECRET", "correct-secret")


class TestTeamSecretMiddleware:
    def test_oauth_callback_route_is_exempt_with_no_header(self):
        client = TestClient(_make_app())
        response = client.get("/api/v1/boards/oauth/jira/callback")
        assert response.status_code == 200

    def test_health_route_is_exempt_with_no_header(self):
        client = TestClient(_make_app())
        response = client.get("/health")
        assert response.status_code == 200

    def test_other_routes_still_require_the_header(self):
        client = TestClient(_make_app())
        response = client.get("/api/v1/organizations/org-1/boards")
        assert response.status_code == 401

    def test_other_routes_accept_the_correct_header(self):
        client = TestClient(_make_app())
        response = client.get(
            "/api/v1/organizations/org-1/boards",
            headers={"X-Team-Secret": "correct-secret"},
        )
        assert response.status_code == 200

    def test_no_secret_configured_is_a_no_op(self, monkeypatch):
        monkeypatch.delenv("TEAM_ACCESS_SECRET", raising=False)
        client = TestClient(_make_app())
        response = client.get("/api/v1/organizations/org-1/boards")
        assert response.status_code == 200


def _make_dependency_app():
    """A tiny app whose only protection is the require_team_secret dependency
    (no TeamSecretMiddleware), so we test the route-level gate in isolation."""
    app = FastAPI()

    @app.get("/gated", dependencies=[Depends(require_team_secret)])
    async def gated():
        return {"ok": True}

    return app


class TestRequireTeamSecretDependency:
    """The explicit route-level team-secret gate (defense-in-depth on top of
    TeamSecretMiddleware). Same posture: no-op when TEAM_ACCESS_SECRET unset,
    401 on missing/invalid header otherwise."""

    def test_missing_header_is_401(self, monkeypatch):
        monkeypatch.setenv("TEAM_ACCESS_SECRET", "correct-secret")
        client = TestClient(_make_dependency_app())
        response = client.get("/gated")
        assert response.status_code == 401
        assert "X-Team-Secret" in response.json()["detail"]

    def test_invalid_header_is_401(self, monkeypatch):
        monkeypatch.setenv("TEAM_ACCESS_SECRET", "correct-secret")
        client = TestClient(_make_dependency_app())
        response = client.get("/gated", headers={"X-Team-Secret": "wrong"})
        assert response.status_code == 401

    def test_valid_header_passes(self, monkeypatch):
        monkeypatch.setenv("TEAM_ACCESS_SECRET", "correct-secret")
        client = TestClient(_make_dependency_app())
        response = client.get("/gated", headers={"X-Team-Secret": "correct-secret"})
        assert response.status_code == 200

    def test_no_secret_configured_is_a_no_op(self, monkeypatch):
        monkeypatch.delenv("TEAM_ACCESS_SECRET", raising=False)
        client = TestClient(_make_dependency_app())
        response = client.get("/gated")
        assert response.status_code == 200
