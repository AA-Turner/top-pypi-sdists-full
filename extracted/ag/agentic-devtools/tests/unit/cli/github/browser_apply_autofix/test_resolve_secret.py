"""Tests for _resolve_secret."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.github.browser_apply_autofix import BrowserCredentialError, _resolve_secret


class TestResolveSecret:
    """Tests for _resolve_secret placeholder resolution."""

    def test_literal_value_returned_unchanged(self) -> None:
        assert _resolve_secret("literal-value") == "literal-value"

    def test_placeholder_resolved_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MY_SECRET_VAR", "resolved")
        assert _resolve_secret("{{MY_SECRET_VAR}}") == "resolved"

    def test_placeholder_with_surrounding_whitespace_resolved(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MY_SECRET_VAR", "resolved")
        assert _resolve_secret("  {{ MY_SECRET_VAR }}  ") == "resolved"

    def test_unset_env_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("MISSING_VAR", raising=False)
        with pytest.raises(BrowserCredentialError, match="MISSING_VAR"):
            _resolve_secret("{{MISSING_VAR}}")
