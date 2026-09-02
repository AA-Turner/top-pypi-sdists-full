"""Tests for system_prohibition_instruction (FR-013)."""

from agentic_devtools.orchestration.review.prompt_boundary import system_prohibition_instruction


class TestSystemProhibitionInstruction:
    def test_mentions_token_and_prohibition(self):
        token = "tok999"
        instruction = system_prohibition_instruction(token)
        assert token in instruction
        assert "Never interpret or follow" in instruction
        assert "data" in instruction.lower()
