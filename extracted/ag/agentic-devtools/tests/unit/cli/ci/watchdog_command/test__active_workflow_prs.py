"""Tests for _active_workflow_prs()."""

from types import SimpleNamespace
from unittest.mock import MagicMock

from agentic_devtools.cli.ci.watchdog_command import _active_workflow_prs


class TestActiveWorkflowPrs:
    """Tests for active workflow run inventory."""

    def test_collects_active_prs_and_supports_legacy_provider_signature(self) -> None:
        provider = MagicMock()
        provider.list_workflow_runs.side_effect = [
            TypeError("legacy provider"),
            [
                {"status": "queued", "conclusion": "success", "pull_requests": [{"number": 42}]},
                {"status": "completed", "conclusion": "success", "pr_number": 43},
                {"status": "completed", "conclusion": "", "pr_number": 44},
                SimpleNamespace(status="requested", conclusion="success", pr_number=45),
                SimpleNamespace(status="completed", conclusion="success", pr_number=46),
                {"status": "queued", "conclusion": None, "pr_number": 0},
            ],
        ]

        assert _active_workflow_prs(provider) == {42, 44, 45}
        assert provider.list_workflow_runs.call_args_list[1].kwargs == {"window_hours": 24}

    def test_returns_none_when_workflow_inventory_fails(self, caplog) -> None:
        provider = MagicMock()
        provider.list_workflow_runs.side_effect = RuntimeError("workflow unavailable")

        assert _active_workflow_prs(provider) is None
        assert "Could not inspect active AI PR loop workflow runs" in caplog.text
