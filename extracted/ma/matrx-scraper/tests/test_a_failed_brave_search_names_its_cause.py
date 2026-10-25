"""A Brave search that fails returns None (its contract) AND records why, so a caller that reports the
failure names the cause instead of "All search queries failed" — a live failure in ~50 ms left no trace
anywhere because the exception was printed and dropped (2026-10-24)."""

import asyncio

from matrx_scraper.search import search as brave_search


class _Exploding:
    async def search(self, **_kwargs):
        raise ValueError("country 'zz' is not supported")


def test_failure_returns_none_and_records_the_cause(monkeypatch):
    monkeypatch.setattr(brave_search, "get_client", lambda: _Exploding())
    captured: list[str] = []

    async def fake_capture(exc, **kwargs):
        captured.append(kwargs.get("kind", ""))

    monkeypatch.setattr(brave_search, "capture_error", fake_capture)
    result = asyncio.run(brave_search.async_brave_search("pizza near me", country="zz"))
    assert result is None
    assert brave_search.brave_failure_reason("pizza near me") == "ValueError: country 'zz' is not supported"
    assert captured == ["brave_search_failed"]


def test_a_later_success_clears_the_cause(monkeypatch):
    class _Fine:
        async def search(self, **_kwargs):
            return {"web": {"results": []}}

    brave_search._note_failure("coffee", "earlier failure")
    monkeypatch.setattr(brave_search, "get_client", lambda: _Fine())
    assert asyncio.run(brave_search.async_brave_search("coffee")) == {"web": {"results": []}}
    assert brave_search.brave_failure_reason("coffee") is None
