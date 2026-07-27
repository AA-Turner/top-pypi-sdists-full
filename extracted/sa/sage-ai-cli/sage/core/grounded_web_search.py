"""Perplexity-style web search: query → synthesized answer + cited sources.

This is sage's answer to Perplexity AI's killer feature. The existing
``sage/core/search_provider.py`` returns ranked URLs; this module takes the
next step — feeds the URLs to an LLM that synthesizes a coherent answer
and returns the citations as structured data the UI can render.

Backend: Vertex AI Gemini with the built-in ``googleSearchRetrieval`` tool.
Google grounds the model's answer in live Search results, returning each
cited source as a ``groundingChunk`` with URI + title. No separate search
+ scrape pipeline needed.

Fallback: when Vertex AI is unreachable, falls back to sage's existing
``Internet`` search facade (DuckDuckGo / Brave / SearXNG). User gets
citations without a synthesized answer rather than a hard failure.

Typical use:

    search = GroundedWebSearch()
    result = search.search("how do US tariffs work in 2025")
    print(result.answer)
    for c in result.citations:
        print(f"  [{c.title}] {c.uri}")
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from typing import Any, Protocol

logger = logging.getLogger("sage.grounded_web_search")


# ── Result types ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Citation:
    """A single cited source. URI is the link the user can click;
    title is the page title (may be empty if Gemini didn't extract one)."""
    uri: str
    title: str = ""

    def to_dict(self) -> dict:
        return {"uri": self.uri, "title": self.title}


@dataclass(frozen=True)
class GroundedSearchResult:
    """A search result with synthesized answer + cited sources.

    `answer` is the LLM's prose answer. May be empty when the API failed
    and we fell back to URL-only search (the citations field is still
    populated so the UI can show "we couldn't summarize but here are the
    relevant pages").
    """
    query: str
    answer: str
    citations: list[Citation]
    tokens_used: int

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "answer": self.answer,
            "citations": [c.to_dict() for c in self.citations],
            "tokens_used": self.tokens_used,
        }


# ── Protocols for testability ─────────────────────────────────────────────────


class _GeminiClient(Protocol):
    """Minimal slice of the Vertex AI client we use. Tests inject a fake."""
    def generate_content(self, prompt: str, *, tools: Any = None, **kwargs: Any) -> Any: ...


class _FallbackInternet(Protocol):
    """Minimal slice of sage.core.internet.Internet — search returns ranked
    results. Used when the grounded API is unreachable."""
    def search(self, query: str, k: int = 5) -> list[Any]: ...


# ── The main search class ─────────────────────────────────────────────────────


class GroundedWebSearch:
    """Perplexity-style search backed by Vertex AI Gemini grounding.

    Construct once; call ``search(query)`` per request. Stateless beyond
    the API client reference, safe to share across threads.
    """

    def __init__(
        self,
        api_client: _GeminiClient | None = None,
        fallback_internet: _FallbackInternet | None = None,
        model_id: str = "gemini-1.5-flash",
    ):
        # Lazy default: in production we want the real Vertex AI client,
        # but tests should construct with a stub so they don't hit the
        # network. None means "build on first call" (or "no-op fallback").
        self._client = api_client
        self._fallback = fallback_internet
        self._model_id = model_id

    def search(self, query: str) -> GroundedSearchResult:
        """Synthesize a cited answer to ``query``.

        Empty/whitespace queries raise ValueError immediately — no point
        spending a Gemini call on garbage input.
        """
        if not query or not query.strip():
            raise ValueError("Cannot search with empty query.")

        try:
            return self._search_grounded(query)
        except Exception as exc:
            # Wire-level error (network, quota, auth). Fall back to plain
            # search if a fallback was provided. Log so we notice if the
            # primary path is consistently failing.
            logger.warning("Grounded search failed (%s); falling back to URL-only search", exc)
            if self._fallback is None:
                # No fallback available — propagate. Callers can decide
                # whether to surface "search unavailable" or treat as empty.
                raise
            return self._search_fallback(query)

    # ── Primary path ──────────────────────────────────────────────────────────

    def _search_grounded(self, query: str) -> GroundedSearchResult:
        """Call Vertex AI with the googleSearchRetrieval tool enabled."""
        if self._client is None:
            raise RuntimeError(
                "No Vertex AI client configured. Pass `api_client` or set "
                "GOOGLE_APPLICATION_CREDENTIALS so we can build the default."
            )

        # Prompt the model to answer + cite. Gemini's googleSearchRetrieval
        # tool returns grounding metadata automatically when invoked.
        response = self._client.generate_content(
            prompt=query,
            tools=[{"google_search_retrieval": {}}],
        )

        return self._parse_response(query, response)

    # ── Response parsing ──────────────────────────────────────────────────────

    @staticmethod
    def _parse_response(query: str, response: Any) -> GroundedSearchResult:
        """Extract text + citations from a Vertex AI response.

        The Vertex AI Gemini response shape (simplified):
            response.candidates[0].content.parts[0].text          → answer
            response.candidates[0].grounding_metadata
                .grounding_chunks[].web.uri / .web.title          → citations
            response.usage_metadata.total_token_count             → tokens

        Real responses occasionally omit fields when no grounding fired.
        We defensively coerce missing fields to empty.
        """
        text = ""
        citations: list[Citation] = []
        tokens = 0

        try:
            candidate = response.candidates[0]
            parts = candidate.content.parts
            if parts:
                text = getattr(parts[0], "text", "") or ""

            grounding = getattr(candidate, "grounding_metadata", None)
            if grounding is not None:
                for chunk in getattr(grounding, "grounding_chunks", []) or []:
                    web = getattr(chunk, "web", None)
                    if web is None:
                        continue
                    uri = getattr(web, "uri", "") or ""
                    title = getattr(web, "title", "") or ""
                    if uri:
                        citations.append(Citation(uri=uri, title=title))

            usage = getattr(response, "usage_metadata", None)
            if usage is not None:
                tokens = int(getattr(usage, "total_token_count", 0) or 0)
        except (AttributeError, IndexError, TypeError) as exc:
            logger.warning("Could not fully parse grounded response: %s", exc)

        return GroundedSearchResult(
            query=query,
            answer=text,
            citations=citations,
            tokens_used=tokens,
        )

    # ── Fallback path ────────────────────────────────────────────────────────

    def _search_fallback(self, query: str) -> GroundedSearchResult:
        """When grounding fails, return URL-only results with empty answer.

        The UI should render this as "Showing related pages (couldn't
        synthesize an answer)". Better than throwing a 500.
        """
        results = self._fallback.search(query, k=5)
        citations = []
        for r in results or []:
            uri = getattr(r, "url", "") or getattr(r, "uri", "")
            title = getattr(r, "title", "") or ""
            if uri:
                citations.append(Citation(uri=uri, title=title))
        return GroundedSearchResult(
            query=query,
            answer="",  # Empty signals "no synthesis available" to the UI
            citations=citations,
            tokens_used=0,
        )


__all__ = [
    "Citation",
    "GroundedSearchResult",
    "GroundedWebSearch",
]
