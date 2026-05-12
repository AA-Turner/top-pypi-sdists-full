"""Tests for stripping reasoning-model thinking blocks before validation.

Background: qwen3-coder-next, deepseek-r1, and other reasoning models emit
their internal plan inside `<think>...</think>` tags. Sage's behavioral
validator was treating that plan as the final response — flagging phrases
like "I need to read..." as "described tools without executing" — and
triggering a retry loop that never let the model produce real output.

The fix: strip those blocks BEFORE any validator runs against the response.
"""

from __future__ import annotations

import pytest


class TestStripThinkingBlocks:

    def test_strips_short_think_tag(self):
        from sage.core.thinking_filter import strip_thinking_blocks
        text = "<think>Let me check the manifest first.</think>READ: package.json"
        assert strip_thinking_blocks(text) == "READ: package.json"

    def test_strips_long_thinking_tag(self):
        from sage.core.thinking_filter import strip_thinking_blocks
        text = "<thinking>I'll plan this out.</thinking>RUN: npm test"
        assert strip_thinking_blocks(text) == "RUN: npm test"

    def test_strips_multiline_thinking(self):
        from sage.core.thinking_filter import strip_thinking_blocks
        text = (
            "<think>\n"
            "First, I need to look at the package.json.\n"
            "Then I'll check the file structure.\n"
            "Finally I'll write the test.\n"
            "</think>\n"
            "READ: package.json\n"
            "SEARCH: jest.config"
        )
        result = strip_thinking_blocks(text)
        assert "READ: package.json" in result
        assert "SEARCH: jest.config" in result
        assert "First, I need to" not in result

    def test_handles_unclosed_thinking_tag(self):
        """Model ran out of tokens mid-think — drop everything after the tag."""
        from sage.core.thinking_filter import strip_thinking_blocks
        text = "Some prelude <think>plan plan plan plan plan..."
        result = strip_thinking_blocks(text)
        assert result == "Some prelude"

    def test_case_insensitive(self):
        from sage.core.thinking_filter import strip_thinking_blocks
        assert strip_thinking_blocks("<Think>x</THINK>after") == "after"

    def test_no_thinking_returns_input(self):
        from sage.core.thinking_filter import strip_thinking_blocks
        text = "READ: foo.py\nRUN: pytest"
        assert strip_thinking_blocks(text) == text


class TestValidatorIgnoresThinking:
    """Integration: behavioral validators must not flag content inside
    thinking blocks as 'described tools instead of executing'."""

    def test_response_with_only_thinking_then_real_tool_is_not_flagged(self):
        """The exact failure mode from the user's sage log."""
        from sage.main import _detect_tool_description_vs_execution
        # Mimics qwen3-coder-next output: long thinking trace, then a real READ.
        response = (
            "<think>\n"
            "Alright, I need to help the user. Let me start by analyzing each task.\n"
            "First, I should look at the package.json to understand the stack.\n"
            "Then I need to read the existing code to see what's there.\n"
            "</think>\n"
            "READ: package.json"
        )
        is_descriptive, _markers = _detect_tool_description_vs_execution(response)
        # Should NOT flag — the <think> block is reasoning, and the actual
        # response is a clean READ: command.
        assert is_descriptive is False, (
            "Reasoning trace inside <think> was treated as the response and "
            "incorrectly flagged. The thinking-strip fix is not active."
        )

    def test_response_describes_code_ignores_thinking(self):
        """`_response_describes_code_without_file_blocks` must also ignore thinking."""
        from sage.main import _response_describes_code_without_file_blocks
        response = (
            "<think>I'll write the LRU cache class with O(1) operations.</think>\n"
            "FILE: lru_cache.py\n"
            "```python\n"
            "class LRUCache: pass\n"
            "```"
        )
        # The FILE: block makes this NOT a description-only response
        assert _response_describes_code_without_file_blocks(response) is False

    def test_extract_tool_commands_skips_thinking_block_mentions(self):
        """Commands mentioned only inside thinking should not be extracted."""
        from sage.main import _extract_tool_commands
        response = (
            "<think>\n"
            "I should probably run RUN: pytest first to see what fails.\n"
            "Then RUN: npm install to update deps.\n"
            "</think>\n"
            "READ: package.json"
        )
        cmds = _extract_tool_commands(response)
        # Only the real READ outside the thinking block should be extracted.
        assert ("READ", "package.json") in cmds
        assert all(not (t == "RUN" and "pytest" in arg) for t, arg in cmds)


class TestFirstTurnGroundingRule:
    """The system prompt must explicitly require the first response to use a
    real tool — not narrate a plan."""

    def test_prompt_mandates_first_turn_read(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        prompt = build_agent_system_prompt(tmp_path, is_local=True, enhanced=False)
        # The first-turn grounding rule must be present
        assert "FIRST-TURN GROUNDING" in prompt or "first output line" in prompt.lower()
        # And must mention concrete fallback discovery commands
        assert "package.json" in prompt or "pyproject.toml" in prompt
        assert "ls -la" in prompt or "READ:" in prompt

    def test_prompt_forbids_narrating_plan(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        prompt = build_agent_system_prompt(tmp_path, is_local=True, enhanced=False)
        # Should warn against the specific failure mode from the log
        body = prompt.lower()
        # Catches the qwen3 pattern of "Let me start by..." narrating
        assert "let me start by" in body or "do not respond" in body or "numbered plan" in body


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
