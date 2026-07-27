"""Tests for the small-model strategy module (C9).

Small local models (3B-7B) lose accuracy when fed long histories or
unranked retrieval. Two helpers move the needle:

  - `compress_history(messages, budget_chars)` keeps recent messages
    verbatim and summarizes older ones into a single condensed message.
  - `rerank_by_relevance(query, snippets, top_k)` ranks retrieval hits
    so only the most relevant ones reach the model.
"""

from __future__ import annotations

import pytest


# ── compress_history ─────────────────────────────────────────────────────


class TestCompressHistory:

    def test_under_budget_returns_unchanged(self):
        from sage.core.small_model_strategy import compress_history
        from sage.providers.base import Message

        msgs = [
            Message(role="user", content="hi"),
            Message(role="assistant", content="hello"),
        ]
        out = compress_history(msgs, budget_chars=10_000)
        assert out == msgs  # nothing to compress

    def test_over_budget_keeps_recent_messages_verbatim(self):
        """The latest user+assistant pair must always be verbatim — that's
        the active turn the model is responding to."""
        from sage.core.small_model_strategy import compress_history
        from sage.providers.base import Message

        msgs = [Message(role="user", content="A" * 1000) for _ in range(10)]
        msgs.append(Message(role="user", content="MOST RECENT QUESTION"))
        out = compress_history(msgs, budget_chars=500)
        # Last message should appear verbatim
        assert any(m.content == "MOST RECENT QUESTION" for m in out)

    def test_over_budget_summarizes_old_messages(self):
        """Old messages collapse into a single summary message tagged
        as system/context so the model knows it's a digest."""
        from sage.core.small_model_strategy import compress_history
        from sage.providers.base import Message

        # Many older messages with substantial content so we comfortably
        # exceed the budget and force compression.
        msgs = [
            Message(role="user", content="Q1: what is X? " + "filler " * 20),
            Message(role="assistant", content="A1: X is foo. " + "context " * 20),
            Message(role="user", content="Q2: change X. " + "more " * 20),
            Message(role="assistant", content="A2: changed. " + "details " * 20),
            Message(role="user", content="Q3: tweak Y. " + "extra " * 20),
            Message(role="assistant", content="A3: tweaked. " + "info " * 20),
            Message(role="user", content="Q4 latest: now what?"),
        ]
        out = compress_history(msgs, budget_chars=200)
        # Output has fewer messages than input (some collapsed)
        assert len(out) < len(msgs)
        # The latest user turn is preserved verbatim
        assert out[-1].content == "Q4 latest: now what?"
        # A summary entry is present
        summary_present = any(
            "earlier" in m.content.lower() or "summary" in m.content.lower()
            for m in out
        )
        assert summary_present

    def test_respects_budget_within_reasonable_margin(self):
        from sage.core.small_model_strategy import compress_history
        from sage.providers.base import Message

        msgs = [
            Message(role="user", content=f"message {i}" + "x" * 200)
            for i in range(20)
        ]
        out = compress_history(msgs, budget_chars=1000)
        total = sum(len(m.content) for m in out)
        # Within 2x the budget — chain-of-density is approximate, not exact
        assert total <= 2000


# ── rerank_by_relevance ──────────────────────────────────────────────────


class TestRerankByRelevance:

    def test_empty_snippets_returns_empty(self):
        from sage.core.small_model_strategy import rerank_by_relevance
        assert rerank_by_relevance("anything", [], top_k=5) == []

    def test_ranks_by_keyword_overlap(self):
        from sage.core.small_model_strategy import rerank_by_relevance
        snippets = [
            "this snippet talks about authentication and sessions",
            "this snippet is about database migrations",
            "this snippet covers authentication tokens and JWT",
        ]
        out = rerank_by_relevance(
            "fix the authentication token handling",
            snippets,
            top_k=2,
        )
        # The two authentication-related snippets should win
        assert len(out) == 2
        joined = " ".join(out)
        assert "authentication" in joined
        # The DB-migrations snippet should NOT be in the top 2
        assert "migrations" not in joined

    def test_top_k_limits_results(self):
        from sage.core.small_model_strategy import rerank_by_relevance
        snippets = [f"foo bar baz quux {i}" for i in range(10)]
        out = rerank_by_relevance("foo", snippets, top_k=3)
        assert len(out) == 3

    def test_returns_input_order_when_query_is_empty(self):
        """Empty query → no ranking signal; preserve input order."""
        from sage.core.small_model_strategy import rerank_by_relevance
        snippets = ["a", "b", "c"]
        out = rerank_by_relevance("", snippets, top_k=10)
        assert out == ["a", "b", "c"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
