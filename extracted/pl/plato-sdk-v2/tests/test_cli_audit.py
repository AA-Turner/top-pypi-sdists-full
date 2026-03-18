"""Tests for the `plato chronos audit` CLI command."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from plato.cli.chronos.main import chronos_app

runner = CliRunner()

_SAMPLE_EVENTS = [
    {
        "timestamp": "2026-03-12T10:00:00Z",
        "operation": "opened-file",
        "path": "/workspace/code/main.py",
        "agent_name": "claude-code",
        "exe": "/usr/bin/python3",
        "trace_id": "abc123def456789",
        "repo_name": "code",
        "step_name": "step1",
    },
    {
        "timestamp": "2026-03-12T10:01:00Z",
        "operation": "deleted",
        "path": "/workspace/code/utils.py",
        "agent_name": "claude-code",
        "exe": "/usr/bin/rm",
        "trace_id": "def456abc789012",
        "repo_name": "code",
        "step_name": "step1",
    },
]


def _make_mock_client(events: list[dict[str, str]] | None = None) -> MagicMock:
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.model_dump.return_value = {
        "events": events or [],
        "total": len(events or []),
    }
    mock_client.get_audit_events.return_value = mock_response
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    return mock_client


class TestAuditCommand:
    """Test the audit CLI command."""

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.chronos.main.Chronos")
    def test_audit_table_output(self, mock_chronos_cls: MagicMock) -> None:
        """Table output should display event rows."""
        mock_chronos_cls.return_value = _make_mock_client(_SAMPLE_EVENTS)

        result = runner.invoke(chronos_app, ["audit", "test-session-id"])
        assert result.exit_code == 0
        assert "Audit Events for test-session" in result.output
        assert "opened-f" in result.output
        assert "claude-co" in result.output

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.chronos.main.Chronos")
    def test_audit_json_output(self, mock_chronos_cls: MagicMock) -> None:
        """JSON format should output valid JSON with events."""
        mock_chronos_cls.return_value = _make_mock_client(_SAMPLE_EVENTS)

        result = runner.invoke(chronos_app, ["audit", "test-session-id", "--format", "json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data["events"]) == 2
        assert data["events"][0]["operation"] == "opened-file"

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.chronos.main.Chronos")
    def test_audit_json_output_to_file(self, mock_chronos_cls: MagicMock, tmp_path) -> None:
        """JSON format with --output should write to file."""
        mock_chronos_cls.return_value = _make_mock_client(_SAMPLE_EVENTS)

        out = tmp_path / "audit.json"
        result = runner.invoke(chronos_app, ["audit", "test-session-id", "--format", "json", "--output", str(out)])
        assert result.exit_code == 0
        data = json.loads(out.read_text())
        assert len(data["events"]) == 2

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.chronos.main.Chronos")
    def test_audit_filters_passed(self, mock_chronos_cls: MagicMock) -> None:
        """Query params should include all provided filters."""
        mock_client = _make_mock_client(_SAMPLE_EVENTS)
        mock_chronos_cls.return_value = mock_client

        result = runner.invoke(
            chronos_app,
            [
                "audit",
                "test-session-id",
                "--step",
                "step1",
                "--repo",
                "code",
                "--path",
                "/workspace",
                "--trace",
                "trace-abc",
                "--agent",
                "claude-code",
                "--limit",
                "100",
                "--format",
                "json",
            ],
        )
        assert result.exit_code == 0

        mock_client.get_audit_events.assert_called_once_with(
            "test-session-id",
            step_name="step1",
            repo_name="code",
            path="/workspace",
            trace_id="trace-abc",
            agent_name="claude-code",
            operation=None,
            limit=100,
        )

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.chronos.main.Chronos")
    def test_audit_operation_filter_passed(self, mock_chronos_cls: MagicMock) -> None:
        """Operation filter should be passed through to the SDK method."""
        mock_client = _make_mock_client(_SAMPLE_EVENTS)
        mock_chronos_cls.return_value = mock_client

        result = runner.invoke(
            chronos_app,
            [
                "audit",
                "test-session-id",
                "--operation",
                "opened-file",
                "--format",
                "json",
            ],
        )
        assert result.exit_code == 0
        mock_client.get_audit_events.assert_called_once_with(
            "test-session-id",
            step_name=None,
            repo_name=None,
            path=None,
            trace_id=None,
            agent_name=None,
            operation="opened-file",
            limit=500,
        )

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.chronos.main.Chronos")
    def test_audit_empty_results(self, mock_chronos_cls: MagicMock) -> None:
        """Empty events should show a message and exit cleanly."""
        mock_chronos_cls.return_value = _make_mock_client([])

        result = runner.invoke(chronos_app, ["audit", "test-session-id"])
        assert result.exit_code == 0
        assert "No audit events found" in result.output
