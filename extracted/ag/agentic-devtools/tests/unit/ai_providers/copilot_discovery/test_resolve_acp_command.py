import os
from unittest.mock import patch

import pytest

from agentic_devtools.ai_providers import copilot_discovery
from agentic_devtools.ai_providers.copilot_discovery import resolve_acp_command
from agentic_devtools.ai_providers.errors import ProviderError


def test_uses_the_environment_override_when_set() -> None:
    with patch.dict(os.environ, {"AGDT_COPILOT_ACP_COMMAND": "/opt/copilot --acp"}, clear=False):
        assert resolve_acp_command() == ["/opt/copilot", "--acp"]


def test_appends_acp_to_the_resolved_binary() -> None:
    with patch.dict(os.environ, {"AGDT_COPILOT_ACP_COMMAND": ""}, clear=False):
        with patch(
            "agentic_devtools.cli.copilot.session._get_copilot_binary",
            return_value="/usr/local/bin/copilot",
        ):
            assert resolve_acp_command() == ["/usr/local/bin/copilot", "--acp"]


def test_returns_none_when_no_binary_is_available() -> None:
    with patch.dict(os.environ, {"AGDT_COPILOT_ACP_COMMAND": ""}, clear=False):
        with patch("agentic_devtools.cli.copilot.session._get_copilot_binary", return_value=None):
            assert resolve_acp_command() is None


def test_raises_provider_error_for_malformed_command_override() -> None:
    with patch.dict(os.environ, {"AGDT_COPILOT_ACP_COMMAND": "'/unterminated"}, clear=False):
        with pytest.raises(ProviderError, match="AGDT_COPILOT_ACP_COMMAND could not be parsed"):
            resolve_acp_command()


def test_uses_windows_command_line_rules_for_quoted_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    override = '"C:\\Program Files\\Copilot\\copilot.exe" --acp'

    monkeypatch.setattr(copilot_discovery.os, "name", "nt")

    with patch.dict(os.environ, {"AGDT_COPILOT_ACP_COMMAND": override}, clear=False):
        assert resolve_acp_command() == [r"C:\Program Files\Copilot\copilot.exe", "--acp"]


def test_windows_override_parser_handles_spaces_backslashes_and_embedded_quotes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(copilot_discovery.os, "name", "nt")

    cases = [
        ('  "C:\\temp\\\\" --acp', ["C:\\temp\\", "--acp"]),
        ('"a\\"b" --acp', ['a"b', "--acp"]),
        ('"a""b" --acp', ['a"b', "--acp"]),
    ]

    for override, expected in cases:
        with patch.dict(os.environ, {"AGDT_COPILOT_ACP_COMMAND": override}, clear=False):
            assert resolve_acp_command() == expected


def test_windows_override_parser_rejects_unterminated_quotes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(copilot_discovery.os, "name", "nt")

    with patch.dict(os.environ, {"AGDT_COPILOT_ACP_COMMAND": '"unterminated'}, clear=False):
        with pytest.raises(ProviderError, match="AGDT_COPILOT_ACP_COMMAND could not be parsed"):
            resolve_acp_command()
