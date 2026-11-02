"""POST /files/session carries ``secret_source`` — ephemeral-secret honesty.

Part of the 2026-08-30 private-file outage hardening: a mint response saying
``"secret_source": "ephemeral"`` tells the client its cookie was signed by a
per-process random fallback secret (invalid on every other container, dead
after restart) so the client can scream instead of failing silently.
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from matrx_connect.middleware import session_cookie as sc
from matrx_connect.middleware.session_cookie import (
    SESSION_COOKIE_NAME,
    SESSION_COOKIE_TTL_SECONDS,
    register_session_cookie_secret,
)

from matrx_files.api.router_files import build_file_router


@pytest.fixture(autouse=True)
def _isolate_registered_secret():
    saved = (sc._registered_secret, sc._registered_secret_is_ephemeral)
    sc._registered_secret, sc._registered_secret_is_ephemeral = None, False
    yield
    sc._registered_secret, sc._registered_secret_is_ephemeral = saved


def _client() -> TestClient:
    app = FastAPI()
    # file_service is unused by the /session route; the router factory only
    # needs it for the storage endpoints.
    app.include_router(build_file_router(file_service=None))
    return TestClient(app)


def test_mint_response_reports_stable_secret() -> None:
    register_session_cookie_secret(b"one-stable-secret-on-every-container")
    resp = _client().post("/files/session")
    assert resp.status_code == 200
    assert resp.json() == {
        "ok": True,
        "expires_in": SESSION_COOKIE_TTL_SECONDS,
        "secret_source": "stable",
    }
    assert SESSION_COOKIE_NAME in resp.headers.get("set-cookie", "")


def test_mint_response_reports_ephemeral_secret() -> None:
    register_session_cookie_secret(b"per-process-random-fallback", ephemeral=True)
    resp = _client().post("/files/session")
    assert resp.status_code == 200
    assert resp.json()["secret_source"] == "ephemeral"
