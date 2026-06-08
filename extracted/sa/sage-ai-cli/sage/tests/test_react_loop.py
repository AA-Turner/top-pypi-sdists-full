"""Tests for the tighter ReAct loop primitives (B6).

The engine's current loop generates a multi-step plan and executes it
all in one shot. When step 3 fails, the agent often plows ahead or
replans from scratch. Tighter pattern: model emits actions, engine
executes ONE, feeds the observation back, re-plans. Smaller steps =
more recovery points.

This module provides:
  - `first_tool_action(response)` — extract only the FIRST tool action
    from a model response, ignoring later actions in the same turn.
  - `ReActConfig` — flag toggle the engine can flip on/off without
    refactoring its core loop.
"""

from __future__ import annotations

import pytest


# ── first_tool_action ────────────────────────────────────────────────────


class TestFirstToolAction:

    def test_no_actions_returns_none(self):
        from sage.core.react_loop import first_tool_action
        assert first_tool_action("I have no actions to take.") is None

    def test_single_action_returns_it(self):
        from sage.core.react_loop import first_tool_action
        result = first_tool_action("Let me check.\nRUN: ls -la\n")
        assert result == ("RUN", "ls -la")

    def test_multiple_actions_returns_only_first(self):
        from sage.core.react_loop import first_tool_action
        response = (
            "I'll inspect, then test, then patch.\n"
            "READ: src/main.py\n"
            "SEARCH: def main\n"
            "RUN: pytest -v\n"
            "FILE: src/main.py\n"
            "```python\nprint('hi')\n```\n"
        )
        result = first_tool_action(response)
        assert result == ("READ", "src/main.py")

    def test_extracts_run_with_complex_command(self):
        from sage.core.react_loop import first_tool_action
        response = "Plan:\nRUN: cd /tmp && ls -la | head -5\n"
        result = first_tool_action(response)
        assert result == ("RUN", "cd /tmp && ls -la | head -5")

    def test_skips_prose_lines_that_only_mention_tool(self):
        """A real action must be at column 0 (optionally after a list bullet).
        Prose like 'Then READ:' inline with other words is meta-discussion
        and must not be parsed — same protocol as main.py's extractor."""
        from sage.core.react_loop import first_tool_action
        # Inline "Then READ:" is meta-discussion — should NOT match
        assert first_tool_action("First you should review the docs.\nThen READ: src/x.py is wrong\n") is None
        # READ: at column 0 on its own line should match
        assert first_tool_action("First you should review.\nREAD: src/x.py\n") == ("READ", "src/x.py")

    def test_handles_bullet_prefixed_actions(self):
        from sage.core.react_loop import first_tool_action
        response = (
            "Steps:\n"
            "- READ: src/main.py\n"
            "- RUN: pytest\n"
        )
        result = first_tool_action(response)
        assert result == ("READ", "src/main.py")


# ── ReActConfig ──────────────────────────────────────────────────────────


class TestReActConfig:

    def test_default_is_disabled(self):
        from sage.core.react_loop import ReActConfig
        cfg = ReActConfig()
        assert cfg.one_tool_per_turn is False

    def test_can_be_enabled(self):
        from sage.core.react_loop import ReActConfig
        cfg = ReActConfig(one_tool_per_turn=True)
        assert cfg.one_tool_per_turn is True


# ── Integration: bound actions per turn ──────────────────────────────────


class TestBoundActionsPerTurn:

    def test_returns_all_when_one_tool_per_turn_is_false(self):
        from sage.core.react_loop import ReActConfig, bound_actions
        cfg = ReActConfig(one_tool_per_turn=False)
        actions = [("READ", "a"), ("RUN", "b"), ("SEARCH", "c")]
        assert bound_actions(actions, cfg) == actions

    def test_returns_only_first_when_one_tool_per_turn_is_true(self):
        from sage.core.react_loop import ReActConfig, bound_actions
        cfg = ReActConfig(one_tool_per_turn=True)
        actions = [("READ", "a"), ("RUN", "b"), ("SEARCH", "c")]
        assert bound_actions(actions, cfg) == [("READ", "a")]

    def test_empty_actions_passes_through(self):
        from sage.core.react_loop import ReActConfig, bound_actions
        cfg = ReActConfig(one_tool_per_turn=True)
        assert bound_actions([], cfg) == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
