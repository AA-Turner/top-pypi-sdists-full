"""Tests for agdt-audit-on-pr-close threshold check logic."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.audit.on_pr_close import check_threshold_and_dispatch


class TestCheckThresholdAndDispatch:
    """Tests for check_threshold_and_dispatch() — FR-011 trigger threshold behavior."""

    def test_threshold_met_returns_true(self) -> None:
        provider = MagicMock()
        provider.count_prs_without_labels.return_value = 10

        result = check_threshold_and_dispatch(provider, threshold=10, repo_path="/tmp")
        assert result is True

    def test_threshold_not_met_returns_false(self) -> None:
        provider = MagicMock()
        provider.count_prs_without_labels.return_value = 5

        result = check_threshold_and_dispatch(provider, threshold=10, repo_path="/tmp")
        assert result is False

    def test_threshold_exceeded_returns_true(self) -> None:
        provider = MagicMock()
        provider.count_prs_without_labels.return_value = 15

        result = check_threshold_and_dispatch(provider, threshold=10, repo_path="/tmp")
        assert result is True

    def test_provider_not_implemented_raises(self) -> None:
        provider = MagicMock()
        provider.count_prs_without_labels.side_effect = NotImplementedError()

        with pytest.raises(NotImplementedError):
            check_threshold_and_dispatch(provider, threshold=10, repo_path="/tmp")

    def test_provider_error_raises(self) -> None:
        provider = MagicMock()
        provider.count_prs_without_labels.side_effect = RuntimeError("API error")

        with pytest.raises(RuntimeError, match="API error"):
            check_threshold_and_dispatch(provider, threshold=10, repo_path="/tmp")

    def test_resolves_threshold_from_config(self) -> None:
        provider = MagicMock()
        provider.count_prs_without_labels.return_value = 5

        with patch(
            "agentic_devtools.cli.audit.on_pr_close.resolve_threshold",
            return_value=5,
        ):
            result = check_threshold_and_dispatch(provider, threshold=None, repo_path="/tmp")
        assert result is True
