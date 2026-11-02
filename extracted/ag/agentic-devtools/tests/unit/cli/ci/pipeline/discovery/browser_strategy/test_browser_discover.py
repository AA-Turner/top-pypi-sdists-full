"""Tests for browser_discover."""

from __future__ import annotations

import builtins
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.pipeline.discovery.browser_strategy import browser_discover
from agentic_devtools.cli.ci.pipeline.discovery.models import DiscoveryOutcome
from agentic_devtools.cli.github.browser_apply_autofix import BrowserAutofixUnavailable, BrowserCredentialError

_COUNT_TARGET = "agentic_devtools.cli.github.browser_apply_autofix.count_browser_autofix_candidates"


class TestBrowserDiscover:
    """Tests for browser_discover."""

    def test_error_when_repo_empty(self) -> None:
        suggestions, attempt = browser_discover(MagicMock(), 1, "")
        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.ERROR
        assert "Repository name" in attempt.error_message

    def test_error_on_import_error(self) -> None:
        real_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if name == "agentic_devtools.cli.github.browser_apply_autofix":
                raise ImportError("Module not found")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=fake_import):
            suggestions, attempt = browser_discover(MagicMock(), 1, "owner/repo")

        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.ERROR
        assert "Import error" in attempt.error_message

    def test_empty_when_dependencies_unavailable(self) -> None:
        with patch(_COUNT_TARGET, side_effect=BrowserAutofixUnavailable("no playwright")):
            suggestions, attempt = browser_discover(MagicMock(), 1, "owner/repo")
        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.EMPTY
        assert attempt.details["reason"] == "browser dependencies not installed"

    def test_empty_when_credentials_not_configured(self) -> None:
        with patch(_COUNT_TARGET, side_effect=BrowserCredentialError("GH_BROWSER_USERNAME not set")):
            suggestions, attempt = browser_discover(MagicMock(), 1, "owner/repo")
        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.EMPTY
        assert attempt.details["reason"] == "browser credentials not configured"

    def test_error_on_generic_exception(self) -> None:
        with patch(_COUNT_TARGET, side_effect=RuntimeError("boom")):
            suggestions, attempt = browser_discover(MagicMock(), 1, "owner/repo")
        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.ERROR
        assert "boom" in attempt.error_message

    def test_success_when_candidates_found(self) -> None:
        with patch(_COUNT_TARGET, return_value=3):
            suggestions, attempt = browser_discover(MagicMock(), 1, "owner/repo")
        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.SUCCESS
        assert attempt.suggestion_count == 3

    def test_empty_when_no_candidates(self) -> None:
        with patch(_COUNT_TARGET, return_value=0):
            suggestions, attempt = browser_discover(MagicMock(), 1, "owner/repo")
        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.EMPTY
