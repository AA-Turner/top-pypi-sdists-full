"""Tests for _initialize_infrastructure in runner module."""

from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.runner import _initialize_infrastructure


class TestInitializeInfrastructure:
    def test_logs_warning_on_exception(self, capsys, tmp_path):
        with patch(
            "agentic_devtools.orchestration.policies.loader.PolicyLoader",
            side_effect=RuntimeError("config missing"),
        ):
            _initialize_infrastructure(str(tmp_path))
        captured = capsys.readouterr()
        assert "WARNING" in captured.err
        assert "config missing" in captured.err

    def test_warning_includes_state_dir(self, capsys, tmp_path):
        with patch(
            "agentic_devtools.orchestration.policies.loader.PolicyLoader",
            side_effect=RuntimeError("oops"),
        ):
            _initialize_infrastructure(str(tmp_path))
        captured = capsys.readouterr()
        assert str(tmp_path) in captured.err

    def test_logs_policy_values_on_success(self, capsys, tmp_path):
        mock_policy = MagicMock()
        mock_policy.shared.max_tokens = 8000
        mock_policy.work_on_issue.retry_budget = 3
        mock_loader = MagicMock()
        mock_loader.load.return_value = mock_policy
        with patch(
            "agentic_devtools.orchestration.policies.loader.PolicyLoader",
            return_value=mock_loader,
        ):
            _initialize_infrastructure(str(tmp_path))
        captured = capsys.readouterr()
        assert "max_tokens=8000" in captured.err
        assert "retry_budget=3" in captured.err
        assert str(tmp_path) in captured.err
