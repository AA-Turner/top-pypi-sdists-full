"""Tests for _is_config_or_doc_path helper."""

from __future__ import annotations

from agentic_devtools.orchestration.review.nodes.source_context import _is_config_or_doc_path


class TestIsConfigOrDocPath:
    """Tests for _is_config_or_doc_path."""

    def test_blank_path_returns_false(self) -> None:
        """Blank paths are not treated as config/doc files."""
        assert _is_config_or_doc_path("") is False

    def test_supported_suffix_returns_true(self) -> None:
        """Known config/doc suffixes are recognized."""
        assert _is_config_or_doc_path("/pyproject.toml") is True
        assert _is_config_or_doc_path("docs/guide.md") is True

    def test_unsupported_suffix_returns_false(self) -> None:
        """Non config/doc source files are excluded."""
        assert _is_config_or_doc_path("agentic_devtools/state.py") is False
