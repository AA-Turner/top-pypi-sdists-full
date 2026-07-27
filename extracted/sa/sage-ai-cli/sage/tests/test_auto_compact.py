"""Unit and integration tests for auto_compact.py."""

from __future__ import annotations

import pytest
from sage.core.auto_compact import should_compact, build_compact_prompt


# ==========================================
# UNIT TESTS
# ==========================================

def test_should_compact_various_ratios():
    """Verify should_compact behaves correctly across various token limits and thresholds."""
    # Under threshold (50% token usage, 70% threshold)
    assert should_compact(current_tokens=5000, context_window=10000, threshold=0.7) is False
    
    # Over threshold (80% token usage, 70% threshold)
    assert should_compact(current_tokens=8000, context_window=10000, threshold=0.7) is True
    
    # Exactly at threshold (70% token usage, 70% threshold)
    assert should_compact(current_tokens=7000, context_window=10000, threshold=0.7) is True


def test_should_compact_invalid_bounds():
    """Verify should_compact returns False if context_window is zero or negative."""
    assert should_compact(current_tokens=100, context_window=0) is False
    assert should_compact(current_tokens=100, context_window=-10) is False


def test_build_compact_prompt_truncation():
    """Verify build_compact_prompt formats messages and truncates long individual content and message lists."""
    messages = [
        {"role": "user", "content": "hello " * 200},  # 1200 chars, should truncate to 500
        {"role": "assistant", "content": "hi"},
    ]
    prompt = build_compact_prompt(prior_messages=messages)
    
    # Assert formatting structure is present
    assert "## Decisions made" in prompt
    assert "## Files changed" in prompt
    assert "## Open questions" in prompt
    assert "## Tests / validation" in prompt
    assert "--- conversation ---" in prompt
    
    # Assert assistant response is intact
    assert "assistant: hi" in prompt
    
    # Assert user response is truncated to 500 chars (+ formatting string)
    assert "user: " in prompt
    truncated_content = "hello " * 83 + "he"  # 500 chars
    assert truncated_content in prompt
    assert len(prompt.split("user: ")[1].split("\n")[0]) == 500


def test_build_compact_prompt_cap_at_30():
    """Verify build_compact_prompt only prints the last 30 messages."""
    messages = [{"role": "user", "content": f"msg {i}"} for i in range(50)]
    prompt = build_compact_prompt(prior_messages=messages)
    
    # Message 19 should be filtered out, messages 20 through 49 should be included
    assert "user: msg 19" not in prompt
    assert "user: msg 20" in prompt
    assert "user: msg 49" in prompt


# ==========================================
# INTEGRATION TESTS
# ==========================================

class MockSessionMemory:
    """Mock conversation session manager with auto-compaction logic."""
    def __init__(self, context_window: int = 10000, threshold: float = 0.7):
        self.context_window = context_window
        self.threshold = threshold
        self.messages: list[dict] = []
        self.estimated_tokens = 0
        self.compaction_counter = 0

    def add_message(self, role: str, content: str, tokens: int):
        self.messages.append({"role": role, "content": content})
        self.estimated_tokens += tokens
        self.check_compaction()

    def check_compaction(self):
        if should_compact(current_tokens=self.estimated_tokens,
                          context_window=self.context_window,
                          threshold=self.threshold):
            # Trigger build_compact_prompt
            prompt = build_compact_prompt(prior_messages=self.messages)
            # Mock LLM response for summary
            summary = self._mock_summarize_llm(prompt)
            # Reset conversation to compact representation
            self.messages = [
                {"role": "system", "content": f"Conversation compact summary:\n{summary}"}
            ]
            self.estimated_tokens = len(summary) // 4  # estimate new tokens
            self.compaction_counter += 1

    def _mock_summarize_llm(self, prompt: str) -> str:
        # Generate dummy summary response based on content
        return "## Decisions made\n- Mocked summary compaction decision"


def test_integration_session_auto_compact_flow():
    """Verify integration of auto-compaction within a session memory manager."""
    session = MockSessionMemory(context_window=1000, threshold=0.8)
    
    # Add messages that stay under 80% threshold (estimated tokens = 600)
    session.add_message("user", "Hello", 200)
    session.add_message("assistant", "How can I help you?", 400)
    
    assert session.compaction_counter == 0
    assert len(session.messages) == 2

    # Add another message that pushes it over threshold (estimated tokens = 900 / 1000 = 90%)
    session.add_message("user", "Write a long code module", 300)

    # Verify compaction was triggered
    assert session.compaction_counter == 1
    assert len(session.messages) == 1
    assert session.messages[0]["role"] == "system"
    assert "Conversation compact summary:" in session.messages[0]["content"]
    assert "Mocked summary compaction decision" in session.messages[0]["content"]
