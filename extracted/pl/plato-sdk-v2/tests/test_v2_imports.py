"""Tests for plato SDK v2 imports and optional dependencies."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestV2Imports:
    """Test that v2 SDK imports work correctly."""

    def test_import_async_plato(self):
        """Test importing AsyncPlato client."""
        from plato.v2 import AsyncPlato

        assert AsyncPlato is not None

    def test_import_sync_plato(self):
        """Test importing sync Plato client."""
        from plato.v2 import Plato

        assert Plato is not None

    def test_import_env(self):
        """Test importing Env helper."""
        from plato.v2 import Env

        assert Env is not None
        assert hasattr(Env, "simulator")
        assert hasattr(Env, "artifact")
        assert hasattr(Env, "resource")

    def test_import_session_classes(self):
        """Test importing Session classes."""
        from plato.v2.async_.session import Session as AsyncSession
        from plato.v2.sync.session import Session as SyncSession

        assert AsyncSession is not None
        assert SyncSession is not None

    def test_import_login_result(self):
        """Test importing LoginResult dataclass."""
        from plato.v2.async_.session import LoginResult as AsyncLoginResult
        from plato.v2.sync.session import LoginResult as SyncLoginResult

        assert AsyncLoginResult is not None
        assert SyncLoginResult is not None

    def test_login_result_annotations(self):
        """Test that LoginResult has proper type annotations."""
        from plato.v2.async_.session import LoginResult

        annotations = LoginResult.__annotations__
        assert "context" in annotations
        assert "pages" in annotations
        # With TYPE_CHECKING, these should be string forward references
        assert annotations["context"] == "BrowserContext"
        assert annotations["pages"] == "dict[str, Page]"

    def test_import_environment(self):
        """Test importing Environment class."""
        from plato.v2.async_.environment import Environment as AsyncEnv
        from plato.v2.sync.environment import Environment as SyncEnv

        assert AsyncEnv is not None
        assert SyncEnv is not None

    def test_import_types(self):
        """Test importing type definitions."""
        from plato.v2.types import EnvFromArtifact, EnvFromResource, EnvFromSimulator

        assert EnvFromSimulator is not None
        assert EnvFromArtifact is not None
        assert EnvFromResource is not None


class TestEnvHelpers:
    """Test Env helper methods."""

    def test_env_simulator(self):
        """Test Env.simulator() creates correct type."""
        from plato.v2 import Env
        from plato.v2.types import EnvFromSimulator

        env = Env.simulator("test-sim", alias="test")
        assert isinstance(env, EnvFromSimulator)
        assert env.simulator == "test-sim"
        assert env.alias == "test"

    def test_env_artifact(self):
        """Test Env.artifact() creates correct type."""
        from plato.v2 import Env
        from plato.v2.types import EnvFromArtifact

        env = Env.artifact("artifact-123", alias="test")
        assert isinstance(env, EnvFromArtifact)
        assert env.artifact_id == "artifact-123"
        assert env.alias == "test"

    def test_env_resource(self):
        """Test Env.resource() creates correct type."""
        from plato.v2 import Env
        from plato.v2.types import EnvFromResource, SimConfigCompute

        sim_config = SimConfigCompute(cpus=1, memory=1024, disk=10240)
        env = Env.resource(simulator="test-sim", sim_config=sim_config, alias="test")
        assert isinstance(env, EnvFromResource)
        assert env.simulator == "test-sim"
        assert env.alias == "test"


class TestSessionSerialization:
    """Test Session serialization/deserialization."""

    def test_serialized_session_model(self):
        """Test SerializedSession model."""
        from plato.v2.async_.session import SerializedEnv, SerializedSession

        serialized = SerializedSession(
            session_id="test-session",
            task_public_id=None,
            envs=[SerializedEnv(job_id="job-1", alias="env-1", artifact_id="artifact-1", simulator="test-sim")],
            api_key="test-key",
            base_url="http://localhost:8080",
            closed=False,
        )

        assert serialized.session_id == "test-session"
        assert len(serialized.envs) == 1
        assert serialized.envs[0].alias == "env-1"


class TestChronosSessionStop:
    @patch("plato.v2.sync.chronos.get_session.sync")
    @patch("plato.v2.sync.chronos.close_session.sync")
    def test_sync_stop_default_message_closes_and_fetches(self, mock_close, mock_get):
        from plato.v2.sync.chronos import ChronosSession

        mock_get.return_value = MagicMock()
        client = MagicMock()
        session = ChronosSession(http_client=client, api_key="test-key", session_id="sess-1")

        result = session.stop()

        mock_close.assert_called_once_with(client=client, public_id="sess-1", x_api_key="test-key")
        mock_get.assert_called_once_with(client=client, public_id="sess-1", x_api_key="test-key")
        assert result is mock_get.return_value

    @pytest.mark.anyio
    @patch("plato.v2.async_.chronos.get_session.asyncio", new_callable=AsyncMock)
    @patch("plato.v2.async_.chronos.close_session.asyncio", new_callable=AsyncMock)
    async def test_async_stop_default_message_closes_and_fetches(self, mock_close, mock_get):
        from plato.v2.async_.chronos import ChronosSession

        mock_get.return_value = MagicMock()
        client = MagicMock()
        session = ChronosSession(http_client=client, api_key="test-key", session_id="sess-1")

        result = await session.stop()

        mock_close.assert_awaited_once_with(client=client, public_id="sess-1", x_api_key="test-key")
        mock_get.assert_awaited_once_with(client=client, public_id="sess-1", x_api_key="test-key")
        assert result is mock_get.return_value
