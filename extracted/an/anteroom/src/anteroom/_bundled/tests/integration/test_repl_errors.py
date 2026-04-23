from __future__ import annotations

from unittest.mock import MagicMock, patch

from anteroom.cli.repl import _handle_config_command
from anteroom.config import AIConfig, AppConfig


def test_config_error_path_routes_through_renderer_error() -> None:
    config = AppConfig(ai=AIConfig(base_url="http://localhost:1/v1", api_key="test-key", model="test-model"))
    render_error = MagicMock()

    with patch("anteroom.cli.repl.renderer.render_error", render_error):
        _handle_config_command(
            "/config set ai.model gpt-5.4-mini --scope nonsense",
            config=config,
            db=None,
            active_space=None,
            working_dir=".",
            ai_service=MagicMock(),
            toolbar_refresh=lambda: None,
        )

    render_error.assert_called_once_with("Invalid scope: 'nonsense'. Must be personal, space, or project.")
