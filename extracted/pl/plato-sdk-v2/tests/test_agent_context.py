"""Tests for AgentContext."""

from plato.agents.runtime.base import AgentContext


class TestAgentContext:
    """Tests for AgentContext basics."""

    def test_computed_fields(self):
        ctx = AgentContext(
            image="test:latest",
            config={"key": "value"},
            instruction="hello",
        )
        assert ctx.config_b64  # non-empty
        assert ctx.instruction_b64  # non-empty

    def test_serialization_round_trip(self):
        ctx = AgentContext(
            image="test:latest",
            config={"key": "value"},
            instruction="hello",
        )
        data = ctx.model_dump()
        restored = AgentContext(**data)
        assert restored.instruction == "hello"
        assert restored.config == {"key": "value"}

    def test_config_dict_carries_continue_session(self):
        """continue_session flows through the config dict, not as a field."""
        config = {"key": "value", "continue_session": True}
        ctx = AgentContext(
            image="test:latest",
            config=config,
            instruction="continue",
        )
        # The config dict should preserve the continue_session key
        assert ctx.config["continue_session"] is True

        # And it should survive base64 round-trip
        import base64
        import json

        decoded = json.loads(base64.b64decode(ctx.config_b64).decode())
        assert decoded["continue_session"] is True
