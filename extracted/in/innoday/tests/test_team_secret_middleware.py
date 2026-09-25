"""The team secret gates the platform-lifecycle routes and nothing else.

It used to be a global middleware: every route but a short exemption list needed
X-Team-Secret, so `innoday login` got a token and then failed at `/auth/me`
without it. Identity is the Bearer token; the secret is a second lock only where
a platform user or organization is created or destroyed, plus the one
unauthenticated route that sends email (PF-455).
"""

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from src.api.middleware.team_secret import require_team_secret

SECRET = "correct-secret"


@pytest.fixture
def gated(monkeypatch):
    monkeypatch.setenv("TEAM_ACCESS_SECRET", SECRET)


class TestNormalUseNeedsOnlyAToken:
    def test_a_signed_in_request_works_without_the_secret(
        self, client, gated, make_user_with_cli_token
    ):
        """The `innoday login` failure: token in hand, /auth/me 401'd."""
        _user, token = make_user_with_cli_token()
        resp = client.get(
            "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
        )
        assert resp.status_code == 200, resp.text

    def test_no_token_is_refused_by_auth_not_by_the_secret(self, client, gated):
        resp = client.get("/api/v1/organizations")
        assert resp.status_code == 401
        assert "X-Team-Secret" not in resp.text

    def test_the_login_code_flow_needs_no_secret(self, client, gated):
        resp = client.post("/api/v1/device/code", json={"client_id": "innoday-cli"})
        assert resp.status_code == 200, resp.text


class TestTheSecretStillGuards:
    def test_creating_a_user_needs_it(self, client, gated, make_user_with_cli_token):
        _user, token = make_user_with_cli_token()
        resp = client.post(
            "/api/v1/users",
            json={"email": "new@example.com", "full_name": "New"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 401
        assert "X-Team-Secret" in resp.text

    def test_the_sign_in_email_needs_it(self, client, gated):
        """Unauthenticated and it sends email; only innoday-ui's server calls it."""
        body = {"email": "a@example.com", "redirect_to": "https://x/ui/auth/callback"}
        refused = client.post("/api/v1/auth/sign-in-link", json=body)
        assert refused.status_code == 401
        assert "X-Team-Secret" in refused.text
        allowed = client.post(
            "/api/v1/auth/sign-in-link", json=body, headers={"X-Team-Secret": SECRET}
        )
        assert allowed.status_code != 401


def _make_dependency_app():
    """A tiny app whose only protection is the require_team_secret dependency,
    so the route-level gate is tested in isolation."""
    app = FastAPI()

    @app.get("/gated", dependencies=[Depends(require_team_secret)])
    async def gated():
        return {"ok": True}

    return app


class TestRequireTeamSecretDependency:
    """The route-level team-secret gate -- the only one there is. No-op when
    TEAM_ACCESS_SECRET is unset, 401 on a missing/invalid header otherwise."""

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


class TestNothingAnonymousSpendsMoney:
    def test_the_ai_health_probe_needs_a_platform_admin(self, client, gated):
        """It makes a live, paid Claude call. The global gate used to be all that
        kept it from anyone on the internet (found in review of PF-455)."""
        assert client.get("/api/v1/ai/health").status_code == 401
