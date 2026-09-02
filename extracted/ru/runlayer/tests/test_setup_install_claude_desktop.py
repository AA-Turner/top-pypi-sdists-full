"""Focused tests for Claude Desktop setup install behavior."""

from __future__ import annotations

import pytest
import typer

from runlayer_cli.api import ServerListItem
from runlayer_cli.commands.setup import InstallClient, _run_non_interactive_install


class _FakeApiClient:
    def list_servers(self, scope: str):
        assert scope == "accessible"
        return [
            ServerListItem(
                id="srv-remote",
                name="Remote Server",
                status="active",
                deployment_mode="remote",
            )
        ]


def test_claude_desktop_remote_server_error_mentions_connectors(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(typer.Exit):
        _run_non_interactive_install(
            api_client=_FakeApiClient(),  # type: ignore[arg-type]
            host="https://example.com",
            client=InstallClient.CLAUDE_DESKTOP,
            server_ids=["srv-remote"],
            plugin_ids=[],
            yes=True,
        )

    captured = capsys.readouterr()
    assert "Settings > Connectors" in captured.err
    assert "organization admin" not in captured.err
