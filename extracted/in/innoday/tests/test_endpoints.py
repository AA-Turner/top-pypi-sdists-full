import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.api.app import app
from src.database import get_session
from tests.db_helpers import build_test_engine


class TestFastAPIEndpoints:
    """Test suite for FastAPI endpoints"""

    @pytest.fixture
    def client(self):
        """
        Create FastAPI test client with an isolated in-memory DB.

        /health does a real `SELECT 1` via get_session() -- previously this
        fixture used the real `app` with no override, so the health checks
        depended on whatever DATABASE_URL/filesystem state existed at test
        time. Consistently 503'd in CI (every run, on every branch including
        main) while never reproducing locally despite matching Python
        version and a clean checkout -- the CI runner's environment for the
        default sqlite:///./innoday.db fallback differs in some way that
        was not worth chasing further given every other test file already
        isolates its DB this same way.
        """
        engine = build_test_engine()

        def override_get_session():
            with Session(engine) as session:
                yield session

        app.dependency_overrides[get_session] = override_get_session
        yield TestClient(app)
        app.dependency_overrides.clear()

    @pytest.fixture
    def mock_dev_environment(self, monkeypatch):
        """The dev deployment: ENVIRONMENT=dev (what www.inno.day serves today)"""
        monkeypatch.setenv("ENVIRONMENT", "dev")

    @pytest.fixture
    def mock_prod_environment(self, monkeypatch):
        """Mock production environment"""
        monkeypatch.setenv("ENVIRONMENT", "production")

    def test_root_endpoint(self, client):
        """Test root endpoint structure, content, content-type, and allowed methods"""
        response = client.get("/")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        data = response.json()

        # Check all required fields are present
        required_fields = [
            "message",
            "status",
            "version",
            "description",
            "docs",
            "redoc",
        ]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

        # The KEYS are the contract -- src/cli/client.py parses this response.
        # The values are marketing copy, and asserting on emoji made any wording
        # edit a CI failure. tests/test_root_content_negotiation.py pins the key
        # set properly; the docs paths are asserted below because they are
        # routes, not prose.
        assert data["docs"] == "/docs"
        assert data["redoc"] == "/redoc"

    def test_health_endpoint(self, client):
        """Test health endpoint structure, content, content-type, and allowed methods"""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        data = response.json()

        # Check all required fields are present
        required_fields = [
            "status",
            "service",
            "version",
            "database",
            "environment",
            "port",
        ]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

        # Verify specific content values
        assert data["status"] == "healthy"
        assert data["service"] == "InnoDay Platform"
        assert data["database"] == "connected"

        # (No 405 assertions: method-not-allowed on a GET-only route is
        # Starlette's router, not our code.)

    def test_health_endpoint_reports_the_deployment_environment(
        self, client, mock_dev_environment
    ):
        """`environment` is ENVIRONMENT, not a synonym for "DEBUG is off".

        The three tests this replaces pinned the bug: they set DEBUG and
        asserted development/production, which is what let the dev deployment
        behind www.inno.day answer `production` (#619).
        """
        response = client.get("/health")
        data = response.json()

        assert data["environment"] == "dev"

    def test_health_endpoint_production_environment(
        self, client, mock_prod_environment
    ):
        """Test health endpoint in production environment"""
        response = client.get("/health")
        data = response.json()

        assert data["environment"] == "production"

    def test_health_endpoint_ignores_debug(self, client, monkeypatch):
        """DEBUG must not move `environment`: they answer different questions,
        and conflating them is what made this endpoint lie."""
        monkeypatch.setenv("ENVIRONMENT", "dev")
        monkeypatch.setenv("DEBUG", "True")

        response = client.get("/health")

        assert response.json()["environment"] == "dev"

    def test_health_endpoint_no_environment_var(self, client, monkeypatch):
        """Falls back to production when ENVIRONMENT is unset -- the same
        default /api/v1/public/status has always used."""
        monkeypatch.delenv("ENVIRONMENT", raising=False)

        response = client.get("/health")
        data = response.json()

        assert data["environment"] == "production"

    def test_health_and_public_status_agree_on_environment(self, client, monkeypatch):
        """Measured on www.inno.day, same process, seconds apart: /public/status
        said `dev` and /health said `production` (#619). One resolver now."""
        monkeypatch.setenv("ENVIRONMENT", "dev")

        health = client.get("/health").json()
        status_ = client.get("/api/v1/public/status").json()

        assert health["environment"] == status_["environment"] == "dev"

    def test_health_and_public_status_agree_on_version(self, client, monkeypatch):
        """Same measurement: /public/status said `0.1.0b0`, /health said
        `0.1.0-beta` -- one read installed-distribution metadata directly,
        the other went through get_version().

        INNODAY_VERSION is set because it is a get_version() source that
        `metadata.version()` cannot see. Without it both paths happen to agree
        in a dev checkout, and this test could not fail.
        """
        monkeypatch.setenv("INNODAY_VERSION", "9.9.9-agreement-test")

        health = client.get("/health").json()
        status_ = client.get("/api/v1/public/status").json()
        public_health = client.get("/api/v1/public/health").json()
        version_info = client.get("/api/v1/public/version").json()

        assert (
            health["version"]
            == status_["version"]
            == public_health["version"]
            == version_info["version"]
            == "9.9.9-agreement-test"
        )

    def test_health_endpoint_default_port_without_run_api(self, client):
        """Test health endpoint falls back to a sane port when run_api() was never called"""
        response = client.get("/health")
        data = response.json()

        assert isinstance(data["port"], int)

    def test_nonexistent_endpoint(self, client):
        """Test that non-existent endpoints return 404"""
        response = client.get("/nonexistent")

        assert response.status_code == 404

    def test_public_status_endpoint_structure(self, client):
        """Test /api/v1/public/status returns the new port/env_file/db_host fields"""
        response = client.get("/api/v1/public/status")

        assert response.status_code == 200
        data = response.json()

        required_fields = ["port", "env_file", "db_host"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        assert isinstance(data["port"], int)
        assert isinstance(data["env_file"], str)
        assert isinstance(data["db_host"], str)

    def test_public_status_db_host_has_no_credentials(self, client, monkeypatch):
        """Test db_host is a bare hostname with no username/password/path leaked"""
        monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@myhost:5432/db")
        response = client.get("/api/v1/public/status")
        data = response.json()

        assert data["db_host"] == "myhost"
        assert "@" not in data["db_host"]
        assert ":" not in data["db_host"]
        assert "/" not in data["db_host"]

    def test_public_status_db_host_fallback_on_empty_url(self, client, monkeypatch):
        """Test db_host degrades gracefully when DATABASE_URL is unset"""
        monkeypatch.delenv("DATABASE_URL", raising=False)

        response = client.get("/api/v1/public/status")
        data = response.json()

        assert data["db_host"] == "(unknown)"

    def test_public_status_port_default_without_run_api(self, client):
        """Test /status returns a sane default port when app.state.port was never set"""
        response = client.get("/api/v1/public/status")
        data = response.json()

        assert isinstance(data["port"], int)

    @pytest.mark.asyncio
    async def test_async_endpoint_behavior(self, client):
        """Test that async endpoints work correctly"""
        # Both endpoints are async, test they work properly
        response = client.get("/")
        assert response.status_code == 200

        response = client.get("/health")
        assert response.status_code == 200

    def test_endpoint_error_handling(self, client):
        """Test error handling in endpoints"""
        # Test with malformed requests
        response = client.get("//")  # Double slash
        # Should either redirect to / or return 404, but not crash
        assert response.status_code in [200, 301, 404]

        # Test with very long URLs
        long_path = "/health" + "a" * 1000
        response = client.get(long_path)
        assert response.status_code == 404  # Should handle gracefully

    def test_openapi_docs_accessibility(self, client):
        """Test that OpenAPI documentation endpoints are accessible"""
        # Test Swagger UI
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

        # Test ReDoc
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

        # Test OpenAPI JSON schema
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        # Verify the schema contains our endpoints
        schema = response.json()
        assert "paths" in schema
        assert "/" in schema["paths"]
        assert "/health" in schema["paths"]
