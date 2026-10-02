"""Standalone-boot contract (replaces the old persistence-quarantine pins).

The standalone service is REAL now: construction succeeds with no environment,
the collection routes exist behind JWT auth, and lifespan startup refuses
loudly when the env contract (JWT material, SUPABASE_MATRIX_*,
CREDENTIALS_ENCRYPTION_KEY) is not met.
"""

from __future__ import annotations

import re
from importlib.metadata import version as distribution_version
from pathlib import Path
from types import SimpleNamespace

import pytest

_ENV_KEYS = (
    "CREDENTIALS_ENCRYPTION_KEY",
    "SUPABASE_MATRIX_URL",
    "SUPABASE_URL",
    "SUPABASE_JWT_SECRET",
    "SUPABASE_MATRIX_JWT_SECRET",
    "SUPABASE_MATRIX_HOST",
    "SUPABASE_MATRIX_PORT",
    "SUPABASE_MATRIX_DATABASE_NAME",
    "SUPABASE_MATRIX_USER",
    "SUPABASE_MATRIX_PASSWORD",
)


@pytest.fixture
def bare_env(monkeypatch: pytest.MonkeyPatch) -> pytest.MonkeyPatch:
    for key in _ENV_KEYS:
        monkeypatch.delenv(key, raising=False)
    return monkeypatch


def test_create_app_constructs_without_environment(bare_env: pytest.MonkeyPatch) -> None:
    from matrx_seo.standalone.app import create_app

    app = create_app()
    assert app.version == distribution_version("matrx-seo")
    routes = {getattr(route, "path", None) for route in app.routes}
    assert {
        "/health",
        "/health/ready",
        "/collections",
        "/collections/{run_id}",
        "/collections/{run_id}/evidence",
        "/providers/dataforseo/operations",
        "/sites/{site_id}/backlinks/refresh",
    } <= routes


def test_adapter_registry_constructs_every_declared_provider() -> None:
    from matrx_seo.standalone.app import ADAPTER_FACTORIES

    assert ADAPTER_FACTORIES
    for name, factory in ADAPTER_FACTORIES.items():
        adapter = factory()
        assert adapter.provider == name
        assert adapter.capabilities


async def test_collection_authorizer_requires_active_org_membership(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_seo.contracts import CollectionRequest, SeoCapability
    from matrx_seo.standalone.app import _standalone_collection_authorizer

    request = CollectionRequest(
        organization_id="org-1",
        created_by="user-1",
        capability=SeoCapability.SERP_RANK,
        operation="search",
        target_ref="example",
        observation_period="test",
    )

    seen_calls: list[tuple[object, ...]] = []

    async def deny(*args: object) -> bool:
        seen_calls.append(args)
        return False

    monkeypatch.setattr("matrx_orm.call_function", deny)
    with pytest.raises(PermissionError, match="active membership"):
        await _standalone_collection_authorizer(request)
    assert seen_calls == [("matrx_seo", "iam", "has_org_access_for", "user-1", "org-1")]

    async def allow(*args: object) -> bool:
        seen_calls.append(args)
        return True

    monkeypatch.setattr("matrx_orm.call_function", allow)
    assert await _standalone_collection_authorizer(request) == request
    assert seen_calls[-1] == (
        "matrx_seo",
        "iam",
        "has_org_access_for",
        "user-1",
        "org-1",
    )


async def test_startup_without_any_env_refuses_on_jwt_material(
    bare_env: pytest.MonkeyPatch,
) -> None:
    from matrx_seo.standalone.app import create_app

    app = create_app()
    with pytest.raises(RuntimeError, match="JWT verification material"):
        async with app.router.lifespan_context(app):
            raise AssertionError("startup must not succeed without env")


async def test_startup_without_postgres_env_refuses_at_db_gate(
    bare_env: pytest.MonkeyPatch,
) -> None:
    from matrx_orm import is_database_registered

    if is_database_registered("matrx_seo"):
        pytest.skip("matrx_seo database already registered in-process (live-test run)")
    bare_env.setenv("SUPABASE_JWT_SECRET", "test-secret")
    from matrx_seo.standalone.app import create_app

    app = create_app()
    with pytest.raises(RuntimeError, match="SUPABASE_MATRIX"):
        async with app.router.lifespan_context(app):
            raise AssertionError("startup must not succeed without the svc_seo pool env")


def test_routes_require_authentication(bare_env: pytest.MonkeyPatch) -> None:
    from fastapi.testclient import TestClient

    from matrx_seo.standalone.app import create_app

    client = TestClient(create_app())  # no `with` — lifespan intentionally not run
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["version"] == distribution_version("matrx-seo")
    assert client.get("/health/ready").status_code == 503
    assert client.post("/collections", json={}).status_code == 401
    assert client.get("/collections", params={"organization_id": "org"}).status_code == 401
    assert client.get("/collections/00000000-0000-0000-0000-000000000000").status_code == 401
    assert client.get("/providers/dataforseo/operations").status_code == 401
    assert (
        client.post(
            "/sites/00000000-0000-0000-0000-000000000000/backlinks/refresh",
            json={},
        ).status_code
        == 401
    )
    assert (
        client.get("/collections/00000000-0000-0000-0000-000000000000/evidence").status_code == 401
    )


async def test_readiness_fails_when_live_database_probe_fails(
    bare_env: pytest.MonkeyPatch,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_orm.core.async_db_manager import AsyncDatabaseManager

    from matrx_seo.standalone.app import _readiness_snapshot, create_app

    async def fail_probe(_config_name: str) -> None:
        raise ConnectionError("database unavailable")

    monkeypatch.setattr(AsyncDatabaseManager, "connection_identity", fail_probe)
    monkeypatch.setattr("matrx_seo.standalone.app._credentials_encryption_healthy", lambda: True)
    app = create_app()
    app.state.seo_service = object()

    payload, status_code = await _readiness_snapshot(app)

    assert status_code == 503
    assert payload["database"] is False
    assert payload["service_role"] is False
    assert payload["local_dev_database_override"] is False
    assert {"database", "database_role"} <= set(payload["failed_components"])


async def test_readiness_rejects_live_service_role_drift(
    bare_env: pytest.MonkeyPatch,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_orm.core.async_db_manager import AsyncDatabaseManager

    from matrx_seo.standalone.app import _readiness_snapshot, create_app

    async def broad_role(_config_name: str) -> SimpleNamespace:
        return SimpleNamespace(current_user="postgres")

    monkeypatch.setattr(AsyncDatabaseManager, "connection_identity", broad_role)
    monkeypatch.setattr("matrx_seo.standalone.app._credentials_encryption_healthy", lambda: True)
    app = create_app()
    app.state.seo_service = object()
    app.state.service_role_asserted = True

    payload, status_code = await _readiness_snapshot(app)

    assert status_code == 503
    assert payload["database"] is True
    assert payload["service_role"] is False
    assert payload["local_dev_database_override"] is False
    assert payload["failed_components"] == ["database_role"]


async def test_readiness_preserves_explicit_local_dev_role_override(
    bare_env: pytest.MonkeyPatch,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_orm.core.async_db_manager import AsyncDatabaseManager

    from matrx_seo.standalone.app import _readiness_snapshot, create_app

    async def broad_role(_config_name: str) -> SimpleNamespace:
        return SimpleNamespace(current_user="postgres")

    monkeypatch.setattr(AsyncDatabaseManager, "connection_identity", broad_role)
    monkeypatch.setattr("matrx_seo.standalone.app._credentials_encryption_healthy", lambda: True)
    app = create_app()
    app.state.seo_service = object()
    app.state.local_dev_enabled = True

    payload, status_code = await _readiness_snapshot(app)

    assert status_code == 200
    assert payload["database"] is True
    assert payload["service_role"] is False
    assert payload["local_dev_database_override"] is True
    assert payload["failed_components"] == []


def test_local_frontend_cors_preflight(bare_env: pytest.MonkeyPatch) -> None:
    from fastapi.testclient import TestClient

    from matrx_seo.standalone.app import create_app

    client = TestClient(create_app())
    response = client.options(
        "/collections",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization,content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_deployment_names_its_own_browser_origins(bare_env: pytest.MonkeyPatch) -> None:
    """A DEPLOYMENT declares its origins; the PACKAGE never ships ours.

    This used to assert that `https://www.aimatrx.com` was allowed straight out
    of the box — i.e. the package carried AI Dream's identity, the "package
    hardwired to us" failure in
    common-docs/policies/package-vs-implementation.md. Our production host now
    sets MATRX_SEO_ALLOWED_ORIGINS (2026-08-09), exactly as a customer running
    this service themselves would.
    """
    from fastapi.testclient import TestClient

    from matrx_seo.standalone.app import create_app

    origins = [
        "https://www.aimatrx.com",
        "https://aimatrx.com",
        "https://demos.aimatrx.com",
    ]
    bare_env.setenv("MATRX_SEO_ALLOWED_ORIGINS", ",".join(origins))
    client = TestClient(create_app())
    for origin in origins:
        response = client.options(
            "/providers/dataforseo/operations",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "authorization",
            },
        )
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == origin


def test_tag_deployment_injects_and_verifies_every_browser_origin() -> None:
    """The automatic tag deploy must preserve the manual deploy's CORS contract."""
    repository_root = Path(__file__).resolve().parents[3]
    deploy_script = (repository_root / "packages/matrx-seo/deploy.sh").read_text()
    workflow = (repository_root / ".github/workflows/publish-package.yml").read_text()

    deploy_origins = re.search(
        r'^PRODUCTION_CORS_ORIGINS="([^"]+)"$', deploy_script, re.MULTILINE
    )
    workflow_origins = re.search(
        r"^      PRODUCTION_CORS_ORIGINS: (.+)$", workflow, re.MULTILINE
    )
    assert deploy_origins is not None
    assert workflow_origins is not None
    assert workflow_origins.group(1) == deploy_origins.group(1)
    assert "https://demos.aimatrx.com" in workflow_origins.group(1).split(",")
    assert workflow.count(
        '-e "MATRX_SEO_ALLOWED_ORIGINS=$PRODUCTION_CORS_ORIGINS"'
    ) == 2
    assert workflow.count(
        "done < <(printf '%s' \"$PRODUCTION_CORS_ORIGINS\" | tr ',' '\\n')"
    ) == 2
    assert workflow.count(
        'grep -Fqi "access-control-allow-origin: $origin"'
    ) == 2


def test_shared_actor_stamp_runs_as_its_trusted_owner() -> None:
    """Service-owned entity tables must stamp actors without auth schema reach."""
    repository_root = Path(__file__).resolve().parents[3]
    migration = (
        repository_root
        / "db/migrations/0530_stamp_actor_trusted_execution_context.sql"
    ).read_text()

    assert "alter function platform._stamp_actor() security definer" in migration.lower()
    assert (
        "alter function platform._stamp_actor() set search_path = pg_catalog"
        in migration.lower()
    )
    assert "grant select on platform.feature_knob to svc_seo" in migration.lower()
    assert "iam.has_access_for(uuid, text, uuid, permission_level)" in migration.lower()


def test_package_default_ships_no_matrx_domain(bare_env: pytest.MonkeyPatch) -> None:
    """The shipped default is local development ONLY — never our production domains."""
    from matrx_seo.standalone.app import _cors_origins

    defaults = _cors_origins()

    assert defaults, "the package must still work out of the box for a developer"
    for origin in defaults:
        assert "aimatrx" not in origin and "matrxserver" not in origin, (
            f"package default ships an AI Dream domain ({origin}); a deployment "
            "names its own origins via MATRX_SEO_ALLOWED_ORIGINS"
        )
    assert any("localhost" in origin for origin in defaults)


def test_dataforseo_catalog_exposes_endpoint_scoped_examples() -> None:
    from matrx_seo.api_contracts import dataforseo_operations_catalog

    catalog = dataforseo_operations_catalog()
    examples = [
        example for operation in catalog.operations for example in operation.endpoint_examples
    ]
    assert len(examples) == 69
    assert len({example.endpoint for example in examples}) == 69
    instant = next(
        example for example in examples if example.endpoint == "/v3/on_page/instant_pages"
    )
    assert instant.workflow == "live"
    assert instant.task == {"url": "https://dataforseo.com/"}
