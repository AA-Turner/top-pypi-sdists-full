"""Tests for agent helper functions."""

import os

from plato.sims.agent_helpers import (
    create_sim_client,
    get_available_sims,
    get_sim_api_docs,
    get_sim_default_auth,
    get_sim_env_requirements,
    setup_sim_env,
)
from plato.sims.registry import registry


class TestSimsRegistry:
    """Test sims registry functionality."""

    def test_list_sims(self):
        """Test listing available sims."""
        sims = registry.list_sims()
        assert "firefly" in sims
        assert "spree" in sims
        assert "espocrm" in sims
        assert "mattermost" in sims

    def test_get_sim_info(self):
        """Test getting sim info."""
        info = registry.get_sim_info("firefly")
        assert info.name == "firefly"
        assert info.auth.type == "bearer_token"
        assert info.auth.env_prefix == "FIREFLY"
        assert "FIREFLY_BASE_URL" in info.auth.env_vars
        assert "FIREFLY_TOKEN" in info.auth.env_vars

    def test_get_endpoints_summary(self):
        """Test getting endpoints summary."""
        endpoints = registry.get_endpoints_summary("firefly")
        assert len(endpoints) > 0
        assert all("method" in e for e in endpoints)
        assert all("path" in e for e in endpoints)


class TestAgentHelpers:
    """Test agent helper functions."""

    def test_get_available_sims(self):
        """Test getting available sims."""
        sims = get_available_sims()
        assert "firefly" in sims
        assert isinstance(sims["firefly"].auth.env_vars, dict)

    def test_get_sim_env_requirements(self):
        """Test getting env requirements."""
        reqs = get_sim_env_requirements("firefly")
        assert "FIREFLY_BASE_URL" in reqs
        assert "FIREFLY_TOKEN" in reqs

    def test_get_sim_default_auth(self):
        """Test getting default auth."""
        defaults = get_sim_default_auth("firefly")
        assert "token" in defaults
        assert defaults["token"] is not None

    def test_setup_sim_env(self):
        """Test setting up sim environment."""
        # Clean env first
        os.environ.pop("FIREFLY_BASE_URL", None)
        os.environ.pop("FIREFLY_TOKEN", None)

        # Setup with defaults
        setup_sim_env("firefly")

        # Check token was set (from defaults)
        assert os.getenv("FIREFLY_TOKEN") is not None

    def test_setup_sim_env_with_artifact_id(self):
        """Test setting up with artifact ID."""
        os.environ.pop("FIREFLY_BASE_URL", None)

        setup_sim_env("firefly", artifact_id="test-123")

        # Should construct base URL from artifact ID
        assert "artifact-test-123" in os.getenv("FIREFLY_BASE_URL", "")

    def test_create_sim_client_sync(self):
        """Test creating sync client."""
        # Set up environment
        os.environ["FIREFLY_BASE_URL"] = "https://test.firefly.local"
        os.environ["FIREFLY_TOKEN"] = "test-token"

        client = create_sim_client("firefly", async_client=False)
        assert client is not None
        assert hasattr(client, "httpx")
        client.close()

    def test_get_sim_api_docs(self):
        """Test getting API documentation."""
        docs = get_sim_api_docs("firefly")
        assert "Firefly III API" in docs
        assert len(docs) > 0

    def test_client_create_without_base_url(self):
        """Test that client.create() works without base_url parameter."""
        # Setup env
        os.environ["FIREFLY_BASE_URL"] = "https://test.firefly.local"
        os.environ["FIREFLY_TOKEN"] = "test-token"

        # Import and create without base_url
        from plato.sims import firefly

        # This should work - base_url read from env
        client = firefly.Client.create()
        assert client is not None
        assert client._base_url == "https://test.firefly.local"
        client.close()
