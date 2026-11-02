"""Smoke tests run by the independence gate inside the bare venv.

These are the executable proof of INDEPENDENCE.md: the package imports, boots
its standalone app, and serves its own routes with zero host code present.
Add package-specific smoke tests here as real capability lands — every major
feature earns at least one bare-venv smoke test.
"""

from __future__ import annotations

import os
import subprocess
import sys
import textwrap

import pytest

#: Every variable that wires the standalone app to a database, storage or auth. The gate runs
#: these tests in a bare venv with none of them; inside the monorepo the developer's ``.env`` (and
#: matrx-orm's live-database guard, which repoints ``SUPABASE_MATRIX_*`` at a test database) sets
#: some of them, and a half-set environment is exactly what ``create_app`` refuses as PARTIAL.
_WIRING_PREFIXES = ("SUPABASE_MATRIX_",)
_WIRING_KEYS = (
    "AWS_S3_DEFAULT_BUCKET",
    "SUPABASE_URL",
    "SUPABASE_JWT_SECRET",
    "MATRX_SESSION_AUTHORITY_URL",
    "MATRX_FILE_SESSION_AUTHORITY_URL",
    "MATRX_FILE_SESSION_MINT_URL",
    "MATRX_FILES_CORS_ALLOWED_ORIGINS",
    "MATRX_FILES_CORS_ALLOWED_ORIGIN_REGEX",
)


def _is_wiring(key: str) -> bool:
    return key in _WIRING_KEYS or key.startswith(_WIRING_PREFIXES)


@pytest.fixture(autouse=True)
def _bare_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """These are BARE-venv smoke tests: run them with the wiring the gate's venv has — none."""
    for key in list(os.environ):
        if _is_wiring(key):
            monkeypatch.delenv(key, raising=False)


def test_package_imports_without_host() -> None:
    import matrx_files  # noqa: F401


def test_unconfigured_access_screams() -> None:
    from matrx_files._config import IndependenceConfigError, get_config, is_configured

    if is_configured():  # a prior test configured; the law still holds
        return
    with pytest.raises(IndependenceConfigError):
        get_config()


def test_standalone_app_boots_and_serves() -> None:
    """Boot in a FRESH interpreter with no wiring: health 200, ready 503 (no database).

    A subprocess, because readiness probes the process's bound database: inside the monorepo
    suite an earlier test has already bound one, and "not ready" can only be proven in a process
    that never had it — which is what the gate's bare venv is.
    """
    script = textwrap.dedent(
        """
        from fastapi.testclient import TestClient
        from matrx_files.standalone.app import create_app

        app = create_app()
        with TestClient(app) as client:
            resp = client.get("/files-service/health")
            assert resp.status_code == 200, resp.status_code
            assert resp.json()["package"] == "matrx-files"
            ready = client.get("/files-service/ready")
            assert ready.status_code == 503, (ready.status_code, ready.json())
            assert ready.json()["status"] == "not_ready"
        print("BOOTED")
        """
    )
    env = {k: v for k, v in os.environ.items() if not _is_wiring(k)}
    done = subprocess.run(
        [sys.executable, "-c", script], env=env, capture_output=True, text=True, timeout=120
    )
    assert done.returncode == 0 and "BOOTED" in done.stdout, done.stderr[-2000:]


def test_standalone_auth_uses_deployment_guest_fingerprint_secret(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_files.standalone.app import _env_config

    monkeypatch.setenv("GUEST_FINGERPRINT_SECRET", "shared-cookie-secret")

    assert _env_config()["guest_fingerprint_secret"] == "shared-cookie-secret"


def test_standalone_cors_allows_local_browser_preflight() -> None:
    from fastapi.testclient import TestClient

    from matrx_files.standalone.app import create_app

    app = create_app()
    with TestClient(app) as client:
        response = client.options(
            "/files/upload",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": (
                    "authorization,content-type,x-request-id,x-idempotency-key,"
                    "x-guest-fingerprint,x-cloud-files-bypass"
                ),
            },
        )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "authorization" in response.headers["access-control-allow-headers"].lower()


def test_deployment_declared_origin_passes_preflight(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A DEPLOYMENT declares its browser origins; the PACKAGE ships none of ours.

    This used to assert `https://www.aimatrx.com` passed straight out of the box,
    i.e. the package carried AI Dream's identity — the "package hardwired to us"
    failure in common-docs/policies/package-vs-implementation.md. Our production
    host sets MATRX_FILES_CORS_ALLOWED_ORIGIN_REGEX (2026-08-09), exactly as a
    customer running this service themselves would.
    """
    from fastapi.testclient import TestClient

    from matrx_files.standalone.app import create_app

    monkeypatch.setenv(
        "MATRX_FILES_CORS_ALLOWED_ORIGINS", "https://www.aimatrx.com"
    )
    app = create_app()
    with TestClient(app) as client:
        response = client.options(
            "/files/upload",
            headers={
                "Origin": "https://www.aimatrx.com",
                "Access-Control-Request-Method": "POST",
            },
        )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://www.aimatrx.com"


def test_package_default_refuses_a_matrx_domain() -> None:
    """With NO deployment config, our own domain must NOT be allowed."""
    from fastapi.testclient import TestClient

    from matrx_files.standalone.app import create_app

    app = create_app()
    with TestClient(app) as client:
        response = client.options(
            "/files/upload",
            headers={
                "Origin": "https://www.aimatrx.com",
                "Access-Control-Request-Method": "POST",
            },
        )

    assert response.headers.get("access-control-allow-origin") is None, (
        "the shipped default allows an AI Dream domain; a deployment must declare "
        "its own origins via MATRX_FILES_CORS_ALLOWED_ORIGINS/_REGEX"
    )


def test_standalone_cors_allows_any_lane_localhost_subdomain() -> None:
    """Every lane's shared preview browses through http://<lane>.localhost:3001.

    With NO deployment origins configured (the default regex), any subdomain of
    `localhost` must pass preflight — this is the CLASS fix (a pattern, not a
    per-lane name list) for the CORS errors every lane's headless walk logged
    against this standalone files service.
    """
    from fastapi.testclient import TestClient

    from matrx_files.standalone.app import create_app

    app = create_app()
    with TestClient(app) as client:
        for origin in (
            "http://any-lane.localhost:3001",
            "http://another-lane.localhost:3001",
            "http://localhost:3001",
        ):
            response = client.options(
                "/files/upload",
                headers={
                    "Origin": origin,
                    "Access-Control-Request-Method": "POST",
                },
            )
            assert response.status_code == 200, (origin, response.status_code)
            assert response.headers["access-control-allow-origin"] == origin, origin


def test_standalone_cors_rejects_evil_domain_even_with_localhost_substring() -> None:
    """A lookalike/attacker origin must never pass just because it contains 'localhost'."""
    from fastapi.testclient import TestClient

    from matrx_files.standalone.app import create_app

    app = create_app()
    with TestClient(app) as client:
        for origin in ("https://evil.example", "http://localhost.evil.example"):
            response = client.options(
                "/files/upload",
                headers={
                    "Origin": origin,
                    "Access-Control-Request-Method": "POST",
                },
            )
            assert response.headers.get("access-control-allow-origin") is None, origin


def test_standalone_cors_rejects_unknown_origin() -> None:
    from fastapi.testclient import TestClient

    from matrx_files.standalone.app import create_app

    app = create_app()
    with TestClient(app) as client:
        response = client.options(
            "/files/upload",
            headers={
                "Origin": "https://untrusted.example",
                "Access-Control-Request-Method": "POST",
            },
        )

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_standalone_cors_rejects_wildcard_credentials_override(monkeypatch) -> None:
    from matrx_files._config import IndependenceConfigError
    from matrx_files.standalone.app import create_app

    monkeypatch.setenv("MATRX_FILES_CORS_ALLOWED_ORIGINS", "*")

    with pytest.raises(IndependenceConfigError, match="cannot contain '\\*'"):
        create_app()
