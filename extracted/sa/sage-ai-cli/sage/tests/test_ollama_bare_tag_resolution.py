"""Regression test for the Ollama bare-name → pulled-tag resolution fix.

Real-task battery on 2026-05-15 found:
  - sage ask --model ollama:deepseek-r1 → 404 from Ollama
  - Because Ollama only had `deepseek-r1:7b` pulled, not bare `deepseek-r1`

OllamaProvider's _ensure_pulled correctly recognized the prefix match,
but then sent the request with the BARE name, which Ollama's /api/chat
rejects.

Fix: _resolve_to_pulled_tag() upgrades the bare name to the real pulled
tag before send. This test locks in the fix.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from sage.providers.openai_compat import OllamaProvider


def _make_provider_with_pulled(pulled_names: list[str]) -> OllamaProvider:
    """Build an OllamaProvider whose _get_pulled_names returns a fixed list."""
    from sage.config import SageConfig

    p = OllamaProvider(SageConfig())
    p._pulled_names = set(pulled_names)
    return p


class TestResolveToPulledTag:
    def test_bare_name_resolves_to_pulled_tag(self):
        """The exact bug from the 2026-05-15 battery."""
        p = _make_provider_with_pulled(["deepseek-r1:7b", "llama3.2:latest"])
        # Bare name "deepseek-r1" → resolved to "deepseek-r1:7b"
        resolved = p._resolve_to_pulled_tag("deepseek-r1")
        assert resolved == "deepseek-r1:7b"

    def test_already_tagged_name_unchanged(self):
        """If user passes the full tag, we don't second-guess them."""
        p = _make_provider_with_pulled(["deepseek-r1:7b"])
        assert p._resolve_to_pulled_tag("deepseek-r1:7b") == "deepseek-r1:7b"

    def test_exact_match_in_pulled_unchanged(self):
        """A pulled model that's already in the bare-name form
        (e.g. some Ollama variants) stays as-is."""
        p = _make_provider_with_pulled(["my-custom-model"])
        assert p._resolve_to_pulled_tag("my-custom-model") == "my-custom-model"

    def test_unpulled_bare_name_returned_as_is(self):
        """If no pulled model matches at all, return the bare name —
        _ensure_pulled will then trigger the actual pull."""
        p = _make_provider_with_pulled(["other:1.0"])
        assert p._resolve_to_pulled_tag("missing") == "missing"

    def test_picks_first_matching_tag(self):
        """When multiple tags exist for the same model, pick deterministically.
        First match in the pulled set wins — sufficient for the common case
        where only one tag is typically pulled per model."""
        p = _make_provider_with_pulled(["foo:7b", "foo:13b"])
        resolved = p._resolve_to_pulled_tag("foo")
        # One of the two — both are acceptable resolutions
        assert resolved in ("foo:7b", "foo:13b")

    def test_resolution_does_not_match_partial_prefix(self):
        """`llama3` should NOT match `llama3.2:latest` — the colon is a
        boundary. Otherwise typo-style misspellings would silently route
        to the wrong model."""
        p = _make_provider_with_pulled(["llama3.2:latest"])
        # `llama3` is a prefix of `llama3.2:latest` but not in the
        # base-name sense — there's no `:` immediately after `llama3`.
        # Confirm we don't false-match.
        # Note: this exact edge case is ambiguous in Ollama's catalog;
        # the rule is "must start with `{name}:`" for the match.
        assert p._resolve_to_pulled_tag("llama3") == "llama3"


class TestProviderUsesResolvedTagInRequests:
    """End-to-end: when generate() / stream() are called with a bare name,
    the HTTP payload to Ollama uses the resolved tag."""

    def test_generate_sends_resolved_tag(self):
        from sage.config import SageConfig
        from sage.providers.base import Message
        import httpx

        p = OllamaProvider(SageConfig())
        p._pulled_names = {"deepseek-r1:7b"}

        captured: dict = {}

        class _FakeResponse:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                return {"message": {"content": "ok", "thinking": ""}}

        class _FakeClient:
            def __init__(self, *a, **kw):
                pass

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def post(self, url, json):
                captured["payload"] = json
                return _FakeResponse()

        with patch("sage.providers.openai_compat.httpx.Client", _FakeClient):
            p.generate(
                [Message(role="user", content="hi")],
                model="deepseek-r1",
                temperature=0.1,
                max_tokens=10,
            )

        # The payload sent to Ollama should use the RESOLVED tag, not
        # the bare name that triggered the 404 bug.
        assert captured["payload"]["model"] == "deepseek-r1:7b"
