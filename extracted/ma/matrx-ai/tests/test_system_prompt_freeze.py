from matrx_ai.config import UnifiedConfig
from matrx_ai.instructions.core import SystemInstruction


def test_first_turn_storage_preserves_rendered_system_prefix() -> None:
    instruction = SystemInstruction(
        base_instruction="Base instruction.",
        prepend_sections=["<available_skills>skill inventory</available_skills>"],
        action_types=["create_task"],
    )
    config = UnifiedConfig(
        model="test-model",
        messages=[{"role": "user", "content": "Hello"}],
        system_instruction=instruction,
    )

    stored = config.to_storage_dict()["system_instruction"]

    assert "<available_skills>skill inventory</available_skills>" in stored
    assert "Available Kind Directives" in stored
    assert stored == str(instruction)


def test_system_prompt_frozen_round_trips_in_conversation_config() -> None:
    config = UnifiedConfig(
        model="test-model",
        messages=[{"role": "user", "content": "Hello"}],
        system_instruction="Base instruction.",
        system_prompt_frozen=True,
    )

    stored = config.to_storage_dict()
    restored = UnifiedConfig.from_dict(
        {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}],
            "system_instruction": stored["system_instruction"],
            **stored["config"],
        }
    )

    assert restored.system_prompt_frozen is True
