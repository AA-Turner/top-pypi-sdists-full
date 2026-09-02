"""`/health/version` — build identity for the standalone scraper service.

The scraper deploys independently of aidream (Coolify, EC2 image); before this
endpoint existed there was no way to answer "what version is the scraper
running?" without shell access. Mirrors aidream's `/health/version` contract:
package version always present, git SHA from `GIT_SHA`/`SOURCE_COMMIT` when
the deploy provides one, degrades to "unknown" — never raises.
"""

from __future__ import annotations

import pytest

fastapi = pytest.importorskip("fastapi", reason="server extra not installed")

from fastapi.testclient import TestClient  # noqa: E402

from matrx_scraper.server.app import PACKAGE_VERSION, create_app  # noqa: E402
from matrx_scraper.server.config import ServerConfig  # noqa: E402


def _client() -> TestClient:
    app = create_app(ServerConfig())
    # No lifespan: /health/version must answer without DB/browser/startup wiring.
    return TestClient(app)


def test_health_version_reports_package_version(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GIT_SHA", raising=False)
    monkeypatch.delenv("SOURCE_COMMIT", raising=False)
    monkeypatch.delenv("BUILD_TIME", raising=False)
    response = _client().get("/health/version")
    assert response.status_code == 200
    payload = response.json()
    assert payload["service"] == "matrx-scraper"
    assert payload["version"] == PACKAGE_VERSION
    assert payload["git_sha"] == "unknown"
    assert payload["built_at"] == "unknown"


def test_health_version_prefers_build_args_then_coolify(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SOURCE_COMMIT", "coolify-sha")
    monkeypatch.setenv("GIT_SHA", "build-arg-sha")
    payload = _client().get("/health/version").json()
    assert payload["git_sha"] == "build-arg-sha"

    monkeypatch.delenv("GIT_SHA")
    payload = _client().get("/health/version").json()
    assert payload["git_sha"] == "coolify-sha"


def test_health_version_requires_no_auth() -> None:
    # Like /health and /health/ready: an ops probe, mounted outside the
    # authenticated routers.
    response = _client().get("/health/version")
    assert response.status_code == 200
