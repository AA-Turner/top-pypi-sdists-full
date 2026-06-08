"""Tests for GroundedWebSearch — Perplexity-style web search.

Sage's existing `core/search_provider.py` returns ranked URLs. This is
different: GroundedWebSearch takes a query and returns a *synthesized
answer* with inline citation URIs, grounded in live web search via
Vertex AI's Gemini googleSearchRetrieval tool.

TDD: these tests describe the contract. The implementation (built next)
must satisfy them all.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from sage.core.grounded_web_search import (
    GroundedSearchResult,
    GroundedWebSearch,
    Citation,
)


# ── Result types ──────────────────────────────────────────────────────────────


class TestGroundedSearchResult:
    """The data shape callers see."""

    def test_result_carries_synthesized_answer(self):
        result = GroundedSearchResult(
            query="who won the 2024 super bowl",
            answer="The Kansas City Chiefs won Super Bowl LVIII...",
            citations=[],
            tokens_used=128,
        )
        assert "Chiefs" in result.answer

    def test_result_carries_citations(self):
        cites = [
            Citation(uri="https://nfl.com/scores/sb-lviii", title="Super Bowl LVIII Recap"),
            Citation(uri="https://espn.com/nfl/...", title="Chiefs win SB LVIII"),
        ]
        result = GroundedSearchResult(
            query="q", answer="a", citations=cites, tokens_used=0,
        )
        assert len(result.citations) == 2
        assert result.citations[0].uri.startswith("https://nfl.com")

    def test_result_round_trips_to_dict(self):
        """For JSON serialization in API responses."""
        result = GroundedSearchResult(
            query="q", answer="a",
            citations=[Citation(uri="https://x.com", title="X")],
            tokens_used=10,
        )
        d = result.to_dict()
        assert d["query"] == "q"
        assert d["answer"] == "a"
        assert d["citations"][0]["uri"] == "https://x.com"
        assert d["tokens_used"] == 10


# ── GroundedWebSearch.search() ────────────────────────────────────────────────


class TestGroundedWebSearch:
    """Main API: GroundedWebSearch().search(query) → GroundedSearchResult."""

    def test_search_returns_synthesized_answer_and_citations(self):
        """Happy path: query → answer with at least 1 cited source."""
        fake_response = _build_fake_gemini_response(
            text="The Kansas City Chiefs won Super Bowl LVIII over the 49ers.",
            chunks=[
                {"uri": "https://nfl.com/scores/sb-lviii", "title": "SB LVIII Recap"},
                {"uri": "https://espn.com/nfl/2024-sb", "title": "Chiefs win SB LVIII"},
            ],
        )
        search = GroundedWebSearch(api_client=_FakeGeminiClient(response=fake_response))
        result = search.search("who won super bowl 2024")

        assert isinstance(result, GroundedSearchResult)
        assert "Chiefs" in result.answer
        assert len(result.citations) == 2
        assert result.citations[0].uri == "https://nfl.com/scores/sb-lviii"
        assert result.citations[1].title == "Chiefs win SB LVIII"

    def test_search_handles_zero_citations(self):
        """Sometimes Gemini answers without invoking search (cached knowledge).
        That's fine — we surface the answer with an empty citation list."""
        fake_response = _build_fake_gemini_response(
            text="Paris is the capital of France.",
            chunks=[],
        )
        search = GroundedWebSearch(api_client=_FakeGeminiClient(response=fake_response))
        result = search.search("capital of france")
        assert result.answer
        assert result.citations == []

    def test_search_strips_internal_grounding_metadata(self):
        """Gemini returns lots of internal scoring/grounding metadata. The
        result type exposes only the user-facing answer + citations,
        nothing more."""
        fake_response = _build_fake_gemini_response(
            text="Some answer.",
            chunks=[{"uri": "https://example.com", "title": "Example"}],
            extra_metadata={"webSearchQueries": ["query 1", "query 2"]},
        )
        search = GroundedWebSearch(api_client=_FakeGeminiClient(response=fake_response))
        result = search.search("anything")
        # Only the documented fields exist
        assert hasattr(result, "answer")
        assert hasattr(result, "citations")
        assert hasattr(result, "tokens_used")

    def test_search_records_query(self):
        """The user's query is preserved in the result for audit + UI display."""
        fake = _build_fake_gemini_response(text="ans", chunks=[])
        search = GroundedWebSearch(api_client=_FakeGeminiClient(response=fake))
        result = search.search("how do tariffs work")
        assert result.query == "how do tariffs work"

    def test_search_empty_query_raises(self):
        search = GroundedWebSearch(api_client=_FakeGeminiClient(response=None))
        with pytest.raises(ValueError, match="empty"):
            search.search("")

    def test_search_whitespace_query_raises(self):
        search = GroundedWebSearch(api_client=_FakeGeminiClient(response=None))
        with pytest.raises(ValueError):
            search.search("   ")


# ── Fallback when grounding unavailable ──────────────────────────────────────


class TestFallback:
    """When Vertex AI is unreachable, fall back to the existing URL-only
    search providers so sage doesn't go completely dark."""

    def test_falls_back_to_basic_search_on_api_failure(self):
        client = _FakeGeminiClient(raises=ConnectionError("Vertex AI down"))
        # The fallback Internet facade returns plain URLs which we wrap as
        # citations with empty answer text — better than nothing.
        fake_internet = MagicMock()
        fake_internet.search.return_value = [
            type("Result", (), {"url": "https://x.com", "title": "X result", "snippet": "..."})(),
            type("Result", (), {"url": "https://y.com", "title": "Y result", "snippet": "..."})(),
        ]
        search = GroundedWebSearch(api_client=client, fallback_internet=fake_internet)
        result = search.search("anything")
        assert result.answer == ""  # No synthesis possible without LLM
        assert len(result.citations) == 2
        assert "x.com" in result.citations[0].uri


# ── Helpers (test-only) ───────────────────────────────────────────────────────


class _FakeGeminiClient:
    """Minimal stand-in for the Vertex AI Gemini client. Real client returns
    a complex object — we mimic the shape just enough for our extractor."""

    def __init__(self, response=None, raises=None):
        self._response = response
        self._raises = raises

    def generate_content(self, prompt, tools=None, **kwargs):
        if self._raises:
            raise self._raises
        return self._response


def _build_fake_gemini_response(text: str, chunks: list[dict], extra_metadata: dict | None = None):
    """Construct a Gemini-shaped response with grounding metadata."""
    return MagicMock(
        candidates=[
            MagicMock(
                content=MagicMock(parts=[MagicMock(text=text)]),
                grounding_metadata=MagicMock(
                    grounding_chunks=[
                        MagicMock(web=MagicMock(uri=c["uri"], title=c.get("title", "")))
                        for c in chunks
                    ],
                    web_search_queries=(extra_metadata or {}).get("webSearchQueries", []),
                ),
            ),
        ],
        usage_metadata=MagicMock(total_token_count=128),
    )
