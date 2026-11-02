"""Tests for html_discover and _detect_saml_redirect functions."""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.pipeline.discovery.html_strategy import (
    _detect_saml_redirect,
    html_discover,
)
from agentic_devtools.cli.ci.pipeline.discovery.models import DiscoveryOutcome


class TestDetectSamlRedirect:
    """Tests for _detect_saml_redirect helper."""

    def test_detects_403_with_saml_request_indicator(self) -> None:
        assert _detect_saml_redirect(403, {}, "SAMLRequest value here") is True

    def test_detects_403_with_relay_state(self) -> None:
        assert _detect_saml_redirect(403, {}, "RelayState=abc") is True

    def test_no_detection_on_403_without_indicators(self) -> None:
        assert _detect_saml_redirect(403, {}, "Access denied") is False

    def test_detects_sso_location_header(self) -> None:
        headers = {"location": "https://idp.example.com/saml2/login"}
        assert _detect_saml_redirect(302, headers, "") is True

    def test_detects_login_saml_location(self) -> None:
        headers = {"location": "https://example.com/login/saml?return=abc"}
        assert _detect_saml_redirect(302, headers, "") is True

    def test_no_detection_on_normal_redirect(self) -> None:
        headers = {"location": "https://example.com/dashboard"}
        assert _detect_saml_redirect(302, headers, "") is False

    def test_detects_saml_indicator_in_body_any_status(self) -> None:
        assert _detect_saml_redirect(200, {}, "SingleSignOnService url") is True

    def test_no_detection_on_normal_200(self) -> None:
        assert _detect_saml_redirect(200, {}, "Normal page content") is False


class TestHtmlDiscover:
    """Tests for html_discover function."""

    def test_returns_error_when_repo_empty(self) -> None:
        provider = MagicMock()
        suggestions, attempt = html_discover(provider, 1, "")
        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.ERROR
        assert "Repository name" in attempt.error_message

    def test_returns_error_on_import_error(self) -> None:
        provider = MagicMock()
        with patch(
            "agentic_devtools.cli.github.apply_thread_autofix._fetch_suggestions_from_page",
            create=True,
        ):
            # Patch the import to raise ImportError
            import builtins

            real_import = builtins.__import__

            def mock_import(name, *args, **kwargs):
                if name == "agentic_devtools.cli.github.apply_thread_autofix":
                    raise ImportError("Module not found")
                return real_import(name, *args, **kwargs)

            with patch("builtins.__import__", side_effect=mock_import):
                suggestions, attempt = html_discover(provider, 1, "owner/repo")

        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.ERROR
        assert "Import error" in attempt.error_message

    def test_returns_error_on_token_acquisition_failure(self) -> None:
        provider = MagicMock()
        with patch.dict("os.environ", {"GITHUB_TOKEN": "ghp_test1234"}, clear=False):
            with patch(
                "agentic_devtools.cli.github.apply_thread_autofix._get_gh_token",
                side_effect=RuntimeError("no token"),
            ):
                suggestions, attempt = html_discover(provider, 1, "owner/repo")

        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.ERROR
        assert "Token acquisition failed" in attempt.error_message

    def test_token_acquisition_failure_log_does_not_include_token_value(self) -> None:
        provider = MagicMock()
        with (
            patch.dict("os.environ", {"GITHUB_TOKEN": "test_token_value"}, clear=False),
            patch(
                "agentic_devtools.cli.github.apply_thread_autofix._get_gh_token",
                side_effect=RuntimeError("no token"),
            ),
            patch("agentic_devtools.cli.ci.pipeline.discovery.html_strategy.logger.warning") as warning_mock,
        ):
            html_discover(provider, 1, "owner/repo")

        warning_mock.assert_called_once()
        warning_message = warning_mock.call_args[0][0]
        assert "token_suffix" not in warning_message
        assert "github_token_present" in warning_message
        assert "test_token_value" not in warning_message

    def test_returns_error_on_token_failure_without_github_token_env(self) -> None:
        """Cover branch 109->111: GITHUB_TOKEN not set."""
        provider = MagicMock()
        env = {k: v for k, v in os.environ.items() if k != "GITHUB_TOKEN"}
        with patch.dict("os.environ", env, clear=True):
            with patch(
                "agentic_devtools.cli.github.apply_thread_autofix._get_gh_token",
                side_effect=RuntimeError("no token"),
            ):
                suggestions, attempt = html_discover(provider, 1, "owner/repo")

        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.ERROR

    def test_returns_error_on_scrape_exception(self) -> None:
        provider = MagicMock()
        with (
            patch(
                "agentic_devtools.cli.github.apply_thread_autofix._get_gh_token",
                return_value="ghp_token123",
            ),
            patch(
                "agentic_devtools.cli.github.apply_thread_autofix._fetch_suggestions_from_page",
                side_effect=RuntimeError("scrape failed"),
            ),
        ):
            suggestions, attempt = html_discover(provider, 1, "owner/repo")

        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.ERROR
        assert "scrape failed" in attempt.error_message

    def test_returns_empty_when_scrape_returns_none(self) -> None:
        provider = MagicMock()
        with (
            patch(
                "agentic_devtools.cli.github.apply_thread_autofix._get_gh_token",
                return_value="ghp_token123",
            ),
            patch(
                "agentic_devtools.cli.github.apply_thread_autofix._fetch_suggestions_from_page",
                return_value=None,
            ),
        ):
            suggestions, attempt = html_discover(provider, 1, "owner/repo")

        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.EMPTY

    def test_returns_success_attempt_from_raw_data(self) -> None:
        provider = MagicMock()
        raw = [
            {
                "comment_id": 99,
                "diff_entries": [{"path": "src/app.py"}],
            }
        ]
        with (
            patch(
                "agentic_devtools.cli.github.apply_thread_autofix._get_gh_token",
                return_value="ghp_token123",
            ),
            patch(
                "agentic_devtools.cli.github.apply_thread_autofix._fetch_suggestions_from_page",
                return_value=raw,
            ),
        ):
            suggestions, attempt = html_discover(provider, 1, "owner/repo")

        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.SUCCESS
        assert attempt.suggestion_count == 1

    def test_skips_entries_without_diff_entries(self) -> None:
        provider = MagicMock()
        raw = [{"comment_id": 1, "diff_entries": []}]
        with (
            patch(
                "agentic_devtools.cli.github.apply_thread_autofix._get_gh_token",
                return_value="ghp_token123",
            ),
            patch(
                "agentic_devtools.cli.github.apply_thread_autofix._fetch_suggestions_from_page",
                return_value=raw,
            ),
        ):
            suggestions, attempt = html_discover(provider, 1, "owner/repo")

        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.EMPTY

    def test_skips_entries_without_path(self) -> None:
        provider = MagicMock()
        raw = [{"comment_id": 1, "diff_entries": [{"path": ""}]}]
        with (
            patch(
                "agentic_devtools.cli.github.apply_thread_autofix._get_gh_token",
                return_value="ghp_token123",
            ),
            patch(
                "agentic_devtools.cli.github.apply_thread_autofix._fetch_suggestions_from_page",
                return_value=raw,
            ),
        ):
            suggestions, attempt = html_discover(provider, 1, "owner/repo")

        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.EMPTY
