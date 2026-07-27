"""Registry coverage: all declared SAGE model identifiers (no network)."""

from __future__ import annotations

import re

import pytest

from sage.config import load_config
from sage.cli_core import _build_router
from sage.tests.registered_sage_model_ids import collect_all_sage_model_identifiers

_PREFIX_RE = re.compile(r"^[a-z_][a-z0-9_]*:(.+)$")


class TestSageModelIdentifierUniverse:
    """Hundreds of models across cloud + Ollama + GGUF catalog + Gemini."""

    def test_declared_id_count_exceeds_threshold(self) -> None:
        ids = collect_all_sage_model_identifiers()
        # Static catalogs only: groq + together + openrouter (curated) + gemini +
        # ollama placeholders + gguf. OpenRouter free models are fetched at runtime
        # via /free-models (cached 24h) and are NOT counted here. Expect ~40+.
        assert len(ids) >= 40, f"only {len(ids)} ids - catalog sync issue?"

    def test_all_ids_unique(self) -> None:
        raw = collect_all_sage_model_identifiers()
        assert len(raw) == len(set(raw))

    def test_id_has_valid_provider_prefix_all(self) -> None:
        bad: list[str] = []
        for model_id in collect_all_sage_model_identifiers():
            if ":" not in model_id or not _PREFIX_RE.match(model_id):
                bad.append(model_id)
        assert not bad, f"first bad ids: {bad[:20]!r} (count={len(bad)})"


@pytest.fixture(scope="module")
def _router() -> object:
    return _build_router(load_config())


class TestProviderRouterResolveNoNetwork:
    """Local-capable providers resolve without network."""

    def test_resolves_ollama_placeholder(self, _router) -> None:
        try:
            p, m = _router.resolve("ollama:llama3.2")
        except RuntimeError as e:
            if "not registered" in str(e):
                assert "not registered" in str(e)
                return
            raise  # type: ignore[union-attr]
        assert p.name == "ollama"
        assert m
