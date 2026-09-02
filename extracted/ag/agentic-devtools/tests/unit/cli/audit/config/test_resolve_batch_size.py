"""Tests for audit config resolution."""

from unittest.mock import patch

from agentic_devtools.cli.audit.config import (
    DEFAULT_BATCH_SIZE,
    DEFAULT_THRESHOLD,
    resolve_batch_size,
    resolve_threshold,
)


class TestResolveBatchSize:
    """Tests for resolve_batch_size() covering CLI > config > default precedence."""

    def test_cli_arg_takes_precedence(self) -> None:
        result = resolve_batch_size(cli_arg=5, repo_path="/tmp/repo")
        assert result == 5

    def test_config_file_used_when_no_cli_arg(self) -> None:
        with patch(
            "agentic_devtools.cli.audit.config.load_repo_config",
            return_value={"audit": {"batch-size": 15}},
        ):
            result = resolve_batch_size(cli_arg=None, repo_path="/tmp/repo")
        assert result == 15

    def test_default_when_no_cli_or_config(self) -> None:
        with patch(
            "agentic_devtools.cli.audit.config.load_repo_config",
            return_value={},
        ):
            result = resolve_batch_size(cli_arg=None, repo_path="/tmp/repo")
        assert result == DEFAULT_BATCH_SIZE

    def test_invalid_cli_arg_zero(self) -> None:
        with patch(
            "agentic_devtools.cli.audit.config.load_repo_config",
            return_value={},
        ):
            result = resolve_batch_size(cli_arg=0, repo_path="/tmp/repo")
        assert result == DEFAULT_BATCH_SIZE

    def test_invalid_config_value(self) -> None:
        with patch(
            "agentic_devtools.cli.audit.config.load_repo_config",
            return_value={"audit": {"batch-size": "not_a_number"}},
        ):
            result = resolve_batch_size(cli_arg=None, repo_path="/tmp/repo")
        assert result == DEFAULT_BATCH_SIZE

    def test_non_dict_audit_config_falls_through_to_default(self) -> None:
        with patch(
            "agentic_devtools.cli.audit.config.load_repo_config",
            return_value={"audit": "not_a_dict"},
        ):
            result = resolve_batch_size(cli_arg=None, repo_path="/tmp/repo")
        assert result == DEFAULT_BATCH_SIZE

    def test_negative_cli_arg_uses_default(self) -> None:
        with patch(
            "agentic_devtools.cli.audit.config.load_repo_config",
            return_value={},
        ):
            result = resolve_batch_size(cli_arg=-1, repo_path="/tmp/repo")
        assert result == DEFAULT_BATCH_SIZE


class TestResolveThreshold:
    """Tests for resolve_threshold() covering CLI > config > default precedence."""

    def test_cli_arg_takes_precedence(self) -> None:
        result = resolve_threshold(cli_arg=20, repo_path="/tmp/repo")
        assert result == 20

    def test_config_file_used_when_no_cli_arg(self) -> None:
        with patch(
            "agentic_devtools.cli.audit.config.load_repo_config",
            return_value={"audit": {"threshold": 5}},
        ):
            result = resolve_threshold(cli_arg=None, repo_path="/tmp/repo")
        assert result == 5

    def test_default_when_no_cli_or_config(self) -> None:
        with patch(
            "agentic_devtools.cli.audit.config.load_repo_config",
            return_value={},
        ):
            result = resolve_threshold(cli_arg=None, repo_path="/tmp/repo")
        assert result == DEFAULT_THRESHOLD

    def test_non_dict_audit_config_falls_through_to_default(self) -> None:
        with patch(
            "agentic_devtools.cli.audit.config.load_repo_config",
            return_value={"audit": "not_a_dict"},
        ):
            result = resolve_threshold(cli_arg=None, repo_path="/tmp/repo")
        assert result == DEFAULT_THRESHOLD
