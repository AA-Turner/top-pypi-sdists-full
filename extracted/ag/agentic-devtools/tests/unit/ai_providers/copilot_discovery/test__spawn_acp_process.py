import subprocess
from unittest.mock import patch

import pytest

from agentic_devtools.ai_providers.copilot_discovery import _spawn_acp_process
from agentic_devtools.ai_providers.errors import ProviderError


def test_spawns_the_command_with_stdio_pipes(tmp_path: object) -> None:
    with patch("agentic_devtools.ai_providers.copilot_discovery.subprocess.Popen") as mock_popen:
        process = _spawn_acp_process(["copilot", "--acp"], str(tmp_path))

    assert process is mock_popen.return_value
    args, kwargs = mock_popen.call_args
    assert args[0] == ["copilot", "--acp"]
    assert kwargs["stdin"] is subprocess.PIPE
    assert kwargs["stdout"] is subprocess.PIPE
    assert kwargs["cwd"] == str(tmp_path)
    assert kwargs["shell"] is False


def test_raises_a_provider_error_when_the_binary_is_missing(tmp_path: object) -> None:
    with patch(
        "agentic_devtools.ai_providers.copilot_discovery.subprocess.Popen",
        side_effect=OSError("No such file"),
    ):
        with pytest.raises(ProviderError, match="Failed to spawn the Copilot ACP process"):
            _spawn_acp_process(["copilot", "--acp"], str(tmp_path))
