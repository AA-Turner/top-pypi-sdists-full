"""`/` answers a browser and an API client differently, on purpose.

Typing the bare domain used to return raw JSON — and so did the Supabase
Site-URL fallback, which lands here when a redirect target is not allowlisted.
Both should end at the sign-in page.

It cannot just redirect, though. `innoday ping api` GETs this exact path and
parses the JSON (`src/cli/client.py:141`) with `follow_redirects=True`, so a
blanket redirect hands every already-installed CLI an HTML page it cannot
parse. Deployed clients are not upgraded in lockstep with the server, so the
JSON contract has to survive.
"""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.api.app import app
from src.page_paths import UI_PREFIX

BROWSER = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"


@pytest.fixture
def client():
    """A client whose startup does not touch a database.

    Entering `TestClient` as a context manager runs the app's lifespan, which
    can reach the database — a real connection to whatever `DATABASE_URL`
    resolves to. On a dev machine one happens to be listening, so these tests
    passed locally while failing in CI, where nothing is on that port. Nothing
    here needs a database: `/` reads one only to decorate the JSON with platform
    branding, inside its own try/except. Patching startup is the repo's existing
    convention for exactly this (see `tests/test_releases_router.py`).
    """
    with patch("src.api.app._assert_schema_at_head"):
        with TestClient(app) as c:
            yield c


class TestBrowsersGetTheUI:
    def test_a_browser_is_redirected(self, client):
        response = client.get("/", headers={"accept": BROWSER}, follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == UI_PREFIX

    def test_the_redirect_lands_somewhere_real(self, client):
        """A redirect to a 404 would be worse than the JSON it replaced."""
        response = client.get("/", headers={"accept": BROWSER})
        assert response.status_code < 400


class TestApiClientsKeepTheirJson:
    def test_an_explicit_json_accept_still_gets_json(self, client):
        response = client.get(
            "/", headers={"accept": "application/json"}, follow_redirects=False
        )
        assert response.status_code == 200
        assert "message" in response.json()

    def test_a_client_sending_no_accept_still_gets_json(self, client):
        """httpx defaults to `*/*`; treating that as a browser would break ping."""
        response = client.get("/", headers={"accept": "*/*"}, follow_redirects=False)
        assert response.status_code == 200
        assert response.json()["status"]

    def test_the_ping_contract_is_intact(self, client):
        """The exact keys `innoday ping api` reads off this response."""
        payload = client.get("/", headers={"accept": "*/*"}).json()
        for key in ("message", "status", "version", "api_version"):
            assert key in payload
