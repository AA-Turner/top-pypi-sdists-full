"""Tests for plato.worlds module - initialization, config, and schema."""

from typing import Annotated
from unittest.mock import patch


class TestWorldImports:
    """Test that world module imports work correctly."""

    def test_import_base_world(self):
        """Test importing BaseWorld class."""
        from plato.worlds import BaseWorld

        assert BaseWorld is not None

    def test_import_run_config(self):
        """Test importing RunConfig class."""
        from plato.worlds import RunConfig

        assert RunConfig is not None

    def test_import_agent_config(self):
        """Test importing AgentConfig class."""
        from plato.worlds import AgentConfig

        assert AgentConfig is not None

    def test_import_markers(self):
        """Test importing annotation markers."""
        from plato.worlds import Agent, Env, EnvList, Secret

        assert Agent is not None
        assert Secret is not None
        assert Env is not None
        assert EnvList is not None

    def test_import_models(self):
        """Test importing data models."""
        from plato.worlds import Observation, StepResult

        assert Observation is not None
        assert StepResult is not None

    def test_import_human_annotation_models(self):
        """Test importing human-annotation termination models."""
        from plato.worlds import AnnotationWorkspaceItem, HumanAnnotationRequest, RequiresHumanAnnotation

        assert AnnotationWorkspaceItem is not None
        assert HumanAnnotationRequest is not None
        assert RequiresHumanAnnotation is not None

    def test_import_register_world(self):
        """Test importing register_world decorator."""
        from plato.worlds import register_world

        assert register_world is not None

    def test_import_get_world(self):
        """Test importing get_world function."""
        from plato.worlds import get_world

        assert get_world is not None

    def test_import_get_registered_worlds(self):
        """Test importing get_registered_worlds function."""
        from plato.worlds import get_registered_worlds

        assert get_registered_worlds is not None

    def test_import_env_types(self):
        """Test importing environment types."""
        from plato.worlds import EnvConfig, EnvFromArtifact, EnvFromResource, EnvFromSimulator

        assert EnvConfig is not None
        assert EnvFromArtifact is not None
        assert EnvFromSimulator is not None
        assert EnvFromResource is not None

    def test_import_config_types(self):
        """Test importing config types."""
        from plato.worlds import CheckpointConfig, StateConfig

        assert CheckpointConfig is not None
        assert StateConfig is not None


class TestWorldMarkers:
    """Test world annotation markers."""

    def test_agent_marker(self):
        """Test Agent marker creation."""
        from plato.worlds import Agent

        marker = Agent(description="Coding agent", required=True)
        assert marker.description == "Coding agent"
        assert marker.required is True

    def test_agent_marker_defaults(self):
        """Test Agent marker defaults."""
        from plato.worlds import Agent

        marker = Agent()
        assert marker.description == ""
        assert marker.required is True

    def test_secret_marker(self):
        """Test Secret marker creation."""
        from plato.worlds import Secret

        marker = Secret(description="API key", required=True)
        assert marker.description == "API key"
        assert marker.required is True

    def test_secret_marker_defaults(self):
        """Test Secret marker defaults."""
        from plato.worlds import Secret

        marker = Secret()
        assert marker.description == ""
        assert marker.required is False

    def test_env_marker(self):
        """Test Env marker creation."""
        from plato.worlds import Env

        marker = Env(description="Database server", required=False)
        assert marker.description == "Database server"
        assert marker.required is False

    def test_env_marker_defaults(self):
        """Test Env marker defaults."""
        from plato.worlds import Env

        marker = Env()
        assert marker.description == ""
        assert marker.required is True

    def test_env_list_marker(self):
        """Test EnvList marker creation."""
        from plato.worlds import EnvList

        marker = EnvList(description="Dynamic environments")
        assert marker.description == "Dynamic environments"


class TestObservation:
    """Test Observation model."""

    def test_observation_creation(self):
        """Test creating an Observation."""
        from plato.worlds import Observation

        obs = Observation(data={"key": "value"})
        assert obs.data == {"key": "value"}

    def test_observation_defaults(self):
        """Test Observation default values."""
        from plato.worlds import Observation

        obs = Observation()
        assert obs.data == {}

    def test_observation_extra_fields(self):
        """Test Observation allows extra fields."""
        from plato.worlds import Observation

        obs = Observation(data={"key": "value"}, extra_field="extra")
        assert obs.extra_field == "extra"


class TestStepResult:
    """Test StepResult model."""

    def test_step_result_creation(self):
        """Test creating a StepResult."""
        from plato.worlds import Observation, StepResult

        result = StepResult(observation=Observation(data={"test": 1}), done=True, info={"status": "complete"})
        assert result.done is True
        assert result.observation.data == {"test": 1}
        assert result.info == {"status": "complete"}

    def test_step_result_defaults(self):
        """Test StepResult default values."""
        from plato.worlds import Observation, StepResult

        result = StepResult(observation=Observation())
        assert result.done is False
        assert result.info == {}


class TestHumanAnnotationModels:
    """Test human annotation request models."""

    def test_requires_human_annotation_payload(self):
        """Test RequiresHumanAnnotation payload serialization."""
        from plato.worlds import AnnotationWorkspaceItem, HumanAnnotationRequest, RequiresHumanAnnotation

        request = HumanAnnotationRequest(
            title="Review generated operations",
            instructions="Validate operations.json quality",
            items=[
                AnnotationWorkspaceItem(
                    workspace="recordings",
                    path="session-1/preprocessing/backend_analysis/operations.json",
                    kind="json",
                )
            ],
        )
        exc = RequiresHumanAnnotation(request)
        payload = exc.result_payload()

        assert payload["requires_human_annotation"] is True
        assert payload["annotation_request"]["title"] == "Review generated operations"
        assert payload["annotation_request"]["items"][0]["workspace"] == "recordings"


class TestRunConfig:
    """Test RunConfig class."""

    def test_config_creation(self):
        """Test creating a basic RunConfig."""
        from plato.worlds import RunConfig

        config = RunConfig()
        assert config.checkpoint.enabled is False
        assert config.state.enabled is True
        assert config.state.path == "/state"
        assert config.slack_notifications.enabled is False

    def test_config_subclass(self):
        """Test creating a RunConfig subclass."""
        from plato.worlds import Agent, AgentConfig, RunConfig, Secret

        class TestWorldConfig(RunConfig):
            prompt: str
            agent: Annotated[AgentConfig, Agent(description="Test agent")]
            api_key: Annotated[str | None, Secret(description="API key")] = None

        config = TestWorldConfig(prompt="Test prompt", agent=AgentConfig(image="test-image:latest"), api_key="test-key")
        assert config.prompt == "Test prompt"
        assert config.agent.image == "test-image:latest"
        assert config.api_key == "test-key"

    def test_config_get_field_annotations(self):
        """Test get_field_annotations method."""
        from plato.markers import FieldMarker
        from plato.worlds import Agent, AgentConfig, RunConfig, Secret

        class TestWorldConfig(RunConfig):
            prompt: str
            agent: Annotated[AgentConfig, Agent(description="Test agent")]
            api_key: Annotated[str | None, Secret(description="API key")] = None

        annotations = TestWorldConfig.get_field_annotations()
        assert "agent" in annotations
        assert "api_key" in annotations
        assert isinstance(annotations["agent"], FieldMarker)
        assert annotations["agent"].kind == "agent"
        assert isinstance(annotations["api_key"], FieldMarker)
        assert annotations["api_key"].kind == "secret"
        assert annotations["prompt"] is None  # No marker


class TestBaseWorldHelpers:
    def test_world_llm_uses_world_atif_source(self):
        from plato.worlds import BaseWorld, LLMConfig, Observation, RunConfig, StepResult

        class TestWorld(BaseWorld[RunConfig]):
            name = "demo"

            async def reset(self) -> Observation:
                return Observation()

            async def step(self) -> StepResult:
                return StepResult(observation=Observation())

        world = TestWorld()
        config = LLMConfig(model="openai/gpt-4o")

        with patch("plato.worlds.base.LLMClient") as mock_client:
            result = world.llm(config)

        mock_client.assert_called_once_with(
            config,
            store=None,
            tracer_name="plato.worlds.demo.llm",
            atif_source="world",
        )
        assert result is mock_client.return_value

    def test_config_get_json_schema(self):
        """Test get_json_schema method."""
        from plato.worlds import Agent, AgentConfig, RunConfig, Secret

        class TestWorldConfig(RunConfig):
            prompt: str
            agent: Annotated[AgentConfig, Agent(description="Test agent")]
            api_key: Annotated[str | None, Secret(description="API key")] = None

        schema = TestWorldConfig.get_json_schema()
        assert "properties" in schema
        assert "agents" in schema
        assert "secrets" in schema
        assert "prompt" in schema["properties"]
        assert any(a["name"] == "agent" for a in schema["agents"])
        assert any(s["name"] == "api_key" for s in schema["secrets"])

    def test_config_get_envs(self):
        """Test get_envs method."""
        from plato.worlds import Env, EnvFromSimulator, RunConfig

        class TestWorldConfig(RunConfig):
            database: Annotated[EnvFromSimulator, Env(description="Database")]

        config = TestWorldConfig(database=EnvFromSimulator(simulator="postgres", alias="db"))
        envs = config.get_envs()
        assert len(envs) == 1
        assert envs[0].alias == "db"


class TestBaseWorld:
    """Test BaseWorld class."""

    def test_world_subclass(self):
        """Test creating a BaseWorld subclass."""
        from plato.worlds import BaseWorld, Observation, RunConfig, StepResult, register_world

        class TestWorldConfig(RunConfig):
            prompt: str = "default"

        @register_world("test-world-subclass")
        class TestWorld(BaseWorld[TestWorldConfig]):
            name = "test-world-subclass"
            description = "Test world"

            async def reset(self) -> Observation:
                return Observation()

            async def step(self) -> StepResult:
                return StepResult(observation=Observation(), done=True)

        assert TestWorld.name == "test-world-subclass"
        assert TestWorld.description == "Test world"

    def test_world_get_config_class(self):
        """Test get_config_class method."""
        from plato.worlds import BaseWorld, Observation, RunConfig, StepResult

        class TestWorldConfig(RunConfig):
            prompt: str = "default"

        class TestWorld(BaseWorld[TestWorldConfig]):
            name = "test-get-config"

            async def reset(self) -> Observation:
                return Observation()

            async def step(self) -> StepResult:
                return StepResult(observation=Observation(), done=True)

        config_cls = TestWorld.get_config_class()
        assert config_cls == TestWorldConfig

    def test_world_get_schema(self):
        """Test get_schema method."""
        from plato.worlds import Agent, AgentConfig, BaseWorld, Observation, RunConfig, Secret, StepResult

        class TestWorldConfig(RunConfig):
            prompt: str
            agent: Annotated[AgentConfig, Agent(description="Test agent")]
            api_key: Annotated[str | None, Secret(description="API key")] = None

        class TestWorld(BaseWorld[TestWorldConfig]):
            name = "test-schema"

            async def reset(self) -> Observation:
                return Observation()

            async def step(self) -> StepResult:
                return StepResult(observation=Observation(), done=True)

        schema = TestWorld.get_schema()
        assert "config_schema" in schema
        assert "secrets_schema" in schema
        assert "agents" in schema
        assert "image" in schema
        assert "$schema" in schema["config_schema"]
        assert "properties" in schema["config_schema"]

    def test_world_registry(self):
        """Test world registration and retrieval."""
        from plato.worlds import BaseWorld, Observation, StepResult, get_registered_worlds, get_world, register_world

        @register_world("registry-test-world")
        class RegistryTestWorld(BaseWorld):
            name = "registry-test-world"

            async def reset(self) -> Observation:
                return Observation()

            async def step(self) -> StepResult:
                return StepResult(observation=Observation(), done=True)

        # Check registration
        worlds = get_registered_worlds()
        assert "registry-test-world" in worlds

        # Check retrieval
        world_cls = get_world("registry-test-world")
        assert world_cls == RegistryTestWorld


class TestWorldSchemaModule:
    """Test the worlds schema module directly."""

    def test_get_field_annotations(self):
        """Test get_field_annotations function."""
        from plato.worlds import Agent, AgentConfig, RunConfig
        from plato.worlds.schema import get_field_annotations

        class TestConfig(RunConfig):
            agent: Annotated[AgentConfig, Agent(description="Test")]

        annotations = get_field_annotations(TestConfig)
        assert "agent" in annotations

    def test_get_world_config_schema(self):
        """Test get_world_config_schema function."""
        from plato.worlds import RunConfig
        from plato.worlds.schema import get_world_config_schema

        class TestConfig(RunConfig):
            prompt: str = "test"

        schema = get_world_config_schema(TestConfig)
        assert "properties" in schema
        assert "agents" in schema
        assert "secrets" in schema
        assert "envs" in schema

    def test_get_world_schema(self):
        """Test get_world_schema function."""
        from plato.worlds import BaseWorld, Observation, StepResult
        from plato.worlds.schema import get_world_schema

        class TestWorld(BaseWorld):
            name = "schema-test"

            async def reset(self) -> Observation:
                return Observation()

            async def step(self) -> StepResult:
                return StepResult(observation=Observation(), done=True)

        schema = get_world_schema(TestWorld)
        assert "config_schema" in schema
        assert "secrets_schema" in schema
        assert "agents" in schema
        assert "envs" in schema
        assert "image" in schema
        assert "$schema" in schema["config_schema"]
        assert "properties" in schema["config_schema"]


class TestWorldModelsModule:
    """Test the worlds models module directly."""

    def test_import_from_models(self):
        """Test importing directly from models module."""
        from plato.worlds.models import Observation, StepResult

        assert Observation is not None
        assert StepResult is not None


class TestWorldMarkersModule:
    """Test the worlds markers module directly."""

    def test_import_from_markers(self):
        """Test importing directly from markers module."""
        from plato.markers import Agent, Env, EnvList
        from plato.markers import WorldSecret as Secret

        assert Agent is not None
        assert Secret is not None
        assert Env is not None
        assert EnvList is not None
