"""Tests for plato.agents module - initialization, config, and schema."""

from typing import Annotated


class TestAgentImports:
    """Test that agent module imports work correctly."""

    def test_import_base_agent(self):
        """Test importing BaseAgent class."""
        from plato.agents import BaseAgent

        assert BaseAgent is not None

    def test_import_agent_config(self):
        """Test importing AgentConfig class."""
        from plato.agents import AgentConfig

        assert AgentConfig is not None

    def test_import_secret(self):
        """Test importing Secret annotation marker."""
        from plato.agents import Secret

        assert Secret is not None

    def test_import_register_agent(self):
        """Test importing register_agent decorator."""
        from plato.agents import register_agent

        assert register_agent is not None

    def test_import_get_agent(self):
        """Test importing get_agent function."""
        from plato.agents import get_agent

        assert get_agent is not None

    def test_import_get_registered_agents(self):
        """Test importing get_registered_agents function."""
        from plato.agents import get_registered_agents

        assert get_registered_agents is not None

    def test_import_otel_functions(self):
        """Test importing OTel tracing functions."""
        from plato.agents import get_tracer, init_tracing, instrument, shutdown_tracing

        assert init_tracing is not None
        assert shutdown_tracing is not None
        assert get_tracer is not None
        assert instrument is not None


class TestSecretMarker:
    """Test Secret annotation marker."""

    def test_secret_creation(self):
        """Test creating a Secret marker."""
        from plato.agents import Secret

        secret = Secret(description="API key", required=True)
        assert secret.description == "API key"
        assert secret.required is True

    def test_secret_defaults(self):
        """Test Secret default values."""
        from plato.agents import Secret

        secret = Secret()
        assert secret.description == ""
        assert secret.required is False


class TestAgentConfig:
    """Test AgentConfig class."""

    def test_config_creation(self):
        """Test creating a basic AgentConfig."""
        from plato.agents import AgentConfig

        config = AgentConfig()
        assert config.runtime == "docker"

    def test_config_runtime_docker(self):
        """Test runtime defaults to docker."""
        from plato.agents import AgentConfig

        config = AgentConfig()
        assert config.runtime == "docker"

    def test_config_runtime_vm(self):
        """Test setting runtime to vm."""
        from plato.agents import AgentConfig

        config = AgentConfig(runtime="vm")
        assert config.runtime == "vm"

    def test_config_runtime_in_schema(self):
        """Test runtime appears in JSON schema."""
        from plato.agents import AgentConfig

        schema = AgentConfig.get_json_schema()
        assert "runtime" in schema["properties"]

    def test_config_runtime_in_config_dict(self):
        """Test runtime appears in config dict."""
        from plato.agents import AgentConfig

        config = AgentConfig(runtime="vm")
        config_dict = config.get_config_dict()
        assert "runtime" in config_dict
        assert config_dict["runtime"] == "vm"

    def test_import_runtime_type(self):
        """Test importing Runtime type."""
        from plato.agents import Runtime

        assert Runtime is not None

    def test_config_subclass(self):
        """Test creating an AgentConfig subclass."""
        from plato.agents import AgentConfig, Secret

        class MyAgentConfig(AgentConfig):
            model_name: str = "test-model"
            api_key: Annotated[str | None, Secret(description="API key")] = None

        config = MyAgentConfig(model_name="custom-model")
        assert config.model_name == "custom-model"
        assert config.api_key is None

    def test_config_get_field_secrets(self):
        """Test get_field_secrets method."""
        from plato.agents import AgentConfig, Secret

        class MyAgentConfig(AgentConfig):
            model_name: str = "test-model"
            api_key: Annotated[str | None, Secret(description="API key")] = None
            other_secret: Annotated[str | None, Secret(description="Other", required=True)] = None

        secrets = MyAgentConfig.get_field_secrets()
        assert "api_key" in secrets
        assert "other_secret" in secrets
        assert secrets["api_key"].description == "API key"
        assert secrets["other_secret"].required is True
        assert "model_name" not in secrets

    def test_config_get_json_schema(self):
        """Test get_json_schema method."""
        from plato.agents import AgentConfig, Secret

        class MyAgentConfig(AgentConfig):
            model_name: str = "test-model"
            api_key: Annotated[str | None, Secret(description="API key")] = None

        schema = MyAgentConfig.get_json_schema()
        assert "properties" in schema
        assert "secrets" in schema
        assert "model_name" in schema["properties"]
        assert any(s["name"] == "api_key" for s in schema["secrets"])

    def test_config_get_secrets_dict(self):
        """Test get_secrets_dict method."""
        from plato.agents import AgentConfig, Secret

        class MyAgentConfig(AgentConfig):
            api_key: Annotated[str | None, Secret(description="API key")] = None

        config = MyAgentConfig(api_key="test-key")
        secrets = config.get_secrets_dict()
        assert secrets == {"api_key": "test-key"}

    def test_config_get_config_dict(self):
        """Test get_config_dict method."""
        from plato.agents import AgentConfig, Secret

        class MyAgentConfig(AgentConfig):
            model_name: str = "test-model"
            api_key: Annotated[str | None, Secret(description="API key")] = None

        config = MyAgentConfig(model_name="custom-model", api_key="test-key")
        config_dict = config.get_config_dict()
        assert "model_name" in config_dict
        assert config_dict["model_name"] == "custom-model"
        assert "api_key" not in config_dict  # Secrets excluded


class TestBaseAgent:
    """Test BaseAgent class."""

    def test_agent_subclass(self):
        """Test creating a BaseAgent subclass."""
        from plato.agents import AgentConfig, BaseAgent, register_agent

        class TestAgentConfig(AgentConfig):
            test_param: str = "default"

        @register_agent("test-agent-subclass")
        class TestAgent(BaseAgent[TestAgentConfig]):
            name = "test-agent-subclass"
            description = "Test agent"

            async def run(self, instruction: str) -> None:
                pass

        assert TestAgent.name == "test-agent-subclass"
        assert TestAgent.description == "Test agent"

    def test_agent_get_config_class(self):
        """Test get_config_class method."""
        from plato.agents import AgentConfig, BaseAgent

        class TestAgentConfig(AgentConfig):
            test_param: str = "default"

        class TestAgent(BaseAgent[TestAgentConfig]):
            name = "test-get-config"

            async def run(self, instruction: str) -> None:
                pass

        config_cls = TestAgent.get_config_class()
        assert config_cls == TestAgentConfig

    def test_agent_get_schema(self):
        """Test get_schema method."""
        from plato.agents import AgentConfig, BaseAgent, Secret

        class TestAgentConfig(AgentConfig):
            model_name: str = "test-model"
            api_key: Annotated[str | None, Secret(description="API key")] = None

        class TestAgent(BaseAgent[TestAgentConfig]):
            name = "test-schema"

            async def run(self, instruction: str) -> None:
                pass

        schema = TestAgent.get_schema()
        assert "config_schema" in schema
        assert "secrets_schema" in schema
        assert "name" in schema
        assert "image" in schema
        assert "properties" in schema["config_schema"]

    def test_agent_registry(self):
        """Test agent registration and retrieval."""
        from plato.agents import BaseAgent, get_agent, get_registered_agents, register_agent

        @register_agent("registry-test-agent")
        class RegistryTestAgent(BaseAgent):
            name = "registry-test-agent"

            async def run(self, instruction: str) -> None:
                pass

        # Check registration
        agents = get_registered_agents()
        assert "registry-test-agent" in agents

        # Check retrieval
        agent_cls = get_agent("registry-test-agent")
        assert agent_cls == RegistryTestAgent


class TestAgentSchemaModule:
    """Test the agents schema module directly."""

    def test_get_field_secrets(self):
        """Test get_field_secrets function."""
        from plato.agents import AgentConfig, Secret
        from plato.agents.schema import get_field_secrets

        class TestConfig(AgentConfig):
            api_key: Annotated[str | None, Secret(description="API key")] = None

        secrets = get_field_secrets(TestConfig)
        assert "api_key" in secrets

    def test_get_agent_config_schema(self):
        """Test get_agent_config_schema function."""
        from plato.agents import AgentConfig
        from plato.agents.schema import get_agent_config_schema

        class TestConfig(AgentConfig):
            model_name: str = "test"

        schema = get_agent_config_schema(TestConfig)
        assert "$schema" in schema
        assert "properties" in schema
        assert "secrets" in schema

    def test_get_agent_schema(self):
        """Test get_agent_schema function."""
        from plato.agents import BaseAgent
        from plato.agents.schema import get_agent_schema

        class TestAgent(BaseAgent):
            name = "schema-test"

            async def run(self, instruction: str) -> None:
                pass

        schema = get_agent_schema(TestAgent)
        assert "config_schema" in schema
        assert "secrets_schema" in schema
        assert "name" in schema
        assert "image" in schema
