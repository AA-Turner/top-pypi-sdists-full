"""Tests for Chronos CLI commands."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from plato.chronos.models import OTelTraceResponse
from plato.cli.chronos.main import chronos_app

runner = CliRunner()


def _mock_trace_response() -> OTelTraceResponse:
    return OTelTraceResponse(
        session_id="test-session-id",
        spans=[],
        total_count=0,
        filtered_count=0,
        has_more=False,
        cursor=None,
    )


class TestTracesCommand:
    """Test the traces CLI command."""

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.chronos.main.Chronos")
    def test_traces_no_filters(self, mock_chronos_cls, tmp_path):
        """Output should not contain 'filters' key when no filters applied."""
        mock_client = MagicMock()
        mock_client.get_traces.return_value = _mock_trace_response()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_chronos_cls.return_value = mock_client

        out = tmp_path / "traces.json"
        result = runner.invoke(chronos_app, ["traces", "test-session-id", "--output", str(out)])
        assert result.exit_code == 0

        data = json.loads(out.read_text())
        assert "filters" not in data
        assert data["session_id"] == "test-session-id"

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.chronos.main.Chronos")
    def test_traces_with_atif_only(self, mock_chronos_cls, tmp_path):
        """Output should contain filters.atif_only when --atif-only is passed."""
        mock_client = MagicMock()
        mock_client.get_traces.return_value = _mock_trace_response()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_chronos_cls.return_value = mock_client

        out = tmp_path / "traces.json"
        result = runner.invoke(chronos_app, ["traces", "test-session-id", "--atif-only", "--output", str(out)])
        assert result.exit_code == 0

        data = json.loads(out.read_text())
        assert data["filters"]["atif_only"] is True

        mock_client.get_traces.assert_called_once_with(
            "test-session-id", atif_only=True, errors_only=False, search=None
        )

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.chronos.main.Chronos")
    def test_traces_with_errors_only(self, mock_chronos_cls, tmp_path):
        """Output should contain filters.errors_only when --errors-only is passed."""
        mock_client = MagicMock()
        mock_client.get_traces.return_value = _mock_trace_response()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_chronos_cls.return_value = mock_client

        out = tmp_path / "traces.json"
        result = runner.invoke(chronos_app, ["traces", "test-session-id", "--errors-only", "--output", str(out)])
        assert result.exit_code == 0

        data = json.loads(out.read_text())
        assert data["filters"]["errors_only"] is True

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.chronos.main.Chronos")
    def test_traces_with_search(self, mock_chronos_cls, tmp_path):
        """Output should contain filters.search when --search is passed."""
        mock_client = MagicMock()
        mock_client.get_traces.return_value = _mock_trace_response()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_chronos_cls.return_value = mock_client

        out = tmp_path / "traces.json"
        result = runner.invoke(
            chronos_app, ["traces", "test-session-id", "--search", "error in step", "--output", str(out)]
        )
        assert result.exit_code == 0

        data = json.loads(out.read_text())
        assert data["filters"]["search"] == "error in step"

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.chronos.main.Chronos")
    def test_traces_with_multiple_filters(self, mock_chronos_cls, tmp_path):
        """Multiple filters should all appear in the filters dict."""
        mock_client = MagicMock()
        mock_client.get_traces.return_value = _mock_trace_response()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_chronos_cls.return_value = mock_client

        out = tmp_path / "traces.json"
        result = runner.invoke(
            chronos_app,
            ["traces", "test-session-id", "--atif-only", "--errors-only", "--search", "foo", "--output", str(out)],
        )
        assert result.exit_code == 0

        data = json.loads(out.read_text())
        assert data["filters"] == {"atif_only": True, "errors_only": True, "search": "foo"}
        # filters should be the first key
        assert list(data.keys())[0] == "filters"
