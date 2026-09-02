"""Tests for _resolved_provider_default_model."""

from __future__ import annotations

from types import SimpleNamespace

from agentic_devtools.orchestration.review.nodes.review_files import (
    _resolved_provider_default_model,
)


class TestResolvedProviderDefaultModel:
    """Tests for _resolved_provider_default_model."""

    def test_reads_model_attr(self) -> None:
        """Best-effort provider model extraction returns the configured model."""
        provider = SimpleNamespace(_model="gpt-4o")
        assert _resolved_provider_default_model(provider) == "gpt-4o"

    def test_returns_none_when_no_model_attr(self) -> None:
        """Provider without _model attribute returns None."""
        provider = SimpleNamespace()
        assert _resolved_provider_default_model(provider) is None
