"""Tests for plato SDK v2 imports and optional dependencies."""


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


class TestChronosCallback:
    """Test ChronosCallback utility class."""

    def test_import_chronos_callback(self):
        """Test importing ChronosCallback."""
        from plato.agents.callback import ChronosCallback

        assert ChronosCallback is not None

    def test_callback_disabled_without_config(self):
        """Test callback is disabled when not configured."""
        from plato.agents.callback import ChronosCallback

        callback = ChronosCallback(callback_url="", session_id="")
        assert not callback.enabled

    def test_callback_enabled_with_config(self):
        """Test callback is enabled when configured."""
        from plato.agents.callback import ChronosCallback

        callback = ChronosCallback(callback_url="http://localhost:8001", session_id="test-session")
        assert callback.enabled

    def test_find_trajectory_returns_none_for_missing_file(self, tmp_path):
        """Test find_trajectory returns None when file doesn't exist."""
        from plato.agents.callback import ChronosCallback

        callback = ChronosCallback(callback_url="http://localhost:8001", session_id="test-session")

        result = callback.find_trajectory(str(tmp_path))
        assert result is None

    def test_find_trajectory_returns_atif(self, tmp_path):
        """Test find_trajectory returns ATIF trajectory when present."""
        import json

        from plato.agents.callback import ChronosCallback

        # Create agent/trajectory.json
        agent_dir = tmp_path / "agent"
        agent_dir.mkdir()
        trajectory_file = agent_dir / "trajectory.json"

        atif_data = {"schema_version": "ATIF-v1.5", "task": {"description": "test"}, "steps": []}
        trajectory_file.write_text(json.dumps(atif_data))

        callback = ChronosCallback(callback_url="http://localhost:8001", session_id="test-session")

        result = callback.find_trajectory(str(tmp_path))
        assert result is not None
        assert result["schema_version"] == "ATIF-v1.5"


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
