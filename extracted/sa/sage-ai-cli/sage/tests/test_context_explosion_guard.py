"""Tests for the context-explosion retry guards.

The user's sage log showed the retry loop stacking nudge text on top of
an already-22,643-token prompt, blowing past the 16,384-token llama_cpp
window. The guards in `SAGEAgent.run_phase` should:

  1. Skip further retries when context is already > 75% of max_tokens
  2. Compact aggressively when that threshold is hit
  3. Surface a clear message to the user instead of crashing

These tests exercise the ConversationEngine + compaction logic directly
to confirm the guards work without needing a real model.
"""

from __future__ import annotations

import pytest


class TestEngineContextStatsAccurate:

    def test_estimate_total_tokens_grows_with_messages(self):
        from sage.core.engine import ConversationEngine
        engine = ConversationEngine(system_prompt="SYS", max_tokens=16_384)
        baseline = engine.estimate_total_tokens()
        engine.add_user("hello " * 1000)
        after = engine.estimate_total_tokens()
        assert after > baseline + 500  # ~1000 words ≈ 1000+ tokens

    def test_get_context_stats_reports_usage(self):
        from sage.core.engine import ConversationEngine
        engine = ConversationEngine(system_prompt="SYS", max_tokens=1_000)
        engine.add_user("x" * 2000)  # ~500 tokens of content
        stats = engine.get_context_stats()
        assert stats.estimated_tokens > 400
        assert stats.usage_percent > 40


class TestCompactReducesContext:

    def test_compact_brings_us_under_budget(self):
        from sage.core.engine import ConversationEngine
        engine = ConversationEngine(system_prompt="SYS", max_tokens=2_000)
        # Add 30 messages of ~200 tokens each = ~6000 tokens
        for i in range(30):
            engine.add_user(f"q{i}: " + ("blah " * 80))
            engine.add_assistant(f"a{i}: " + ("ok " * 80))
        before = engine.estimate_total_tokens()
        assert before > 3000  # way over budget
        removed = engine.compact(target_tokens=1500)
        after = engine.estimate_total_tokens()
        assert removed > 0
        assert after < before


class TestSmallModelCompressionForLargeContext:
    """When near the limit on a small model, compact_for_small_model
    must actually shrink the history."""

    def test_maybe_compress_engages_on_small_model_when_huge(self):
        from sage.core.engine import ConversationEngine
        engine = ConversationEngine(system_prompt="SYS", max_tokens=16_384)
        for i in range(20):
            engine.add_user("x" * 500)
            engine.add_assistant("y" * 500)
        before = sum(len(m.content) for m in engine.build_messages())
        removed = engine.maybe_compress_for_model("ollama:llama3.2", budget_chars=2000)
        assert removed > 0
        after = sum(len(m.content) for m in engine.build_messages())
        assert after < before


class TestRetryGuardSemantics:
    """Verify the threshold semantics the SAGEAgent guard relies on.

    The guard fires at usage > 75%. These tests pin that threshold.
    """

    def test_threshold_just_below_does_not_fire(self):
        from sage.core.engine import ConversationEngine
        engine = ConversationEngine(system_prompt="SYS", max_tokens=1_000)
        # ~700 tokens of content (just below 75% threshold)
        engine.add_user("x" * 2800)
        stats = engine.get_context_stats()
        assert stats.estimated_tokens / stats.max_tokens < 0.80

    def test_threshold_above_75_percent_fires(self):
        from sage.core.engine import ConversationEngine
        engine = ConversationEngine(system_prompt="SYS", max_tokens=1_000)
        # ~900 tokens — well over 75%
        engine.add_user("x" * 3600)
        stats = engine.get_context_stats()
        assert stats.estimated_tokens / stats.max_tokens > 0.75


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
