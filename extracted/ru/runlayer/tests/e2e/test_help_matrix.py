from types import SimpleNamespace
from unittest.mock import patch

import pytest

from runlayer_cli.config import Config
from runlayer_cli.main import app

from .conftest import strip_ansi

pytestmark = pytest.mark.no_backend_e2e


@pytest.mark.parametrize(
    ("args", "expected_text"),
    [
        ([], "Commands"),
        (["cache"], "clear"),
        (["org-api-key"], "add"),
        (["setup"], "hooks"),
        (["skills"], "add"),
        (["plugins"], "add"),
        (["terraform"], "export"),
    ],
)
def test_help_shown_when_needed(runner, args: list[str], expected_text: str):
    result = runner.invoke(app, args)

    assert result.exit_code == 0
    plain_output = strip_ansi(result.output)
    assert "Usage:" in plain_output
    assert expected_text in plain_output
    assert "Missing command" not in plain_output


def test_run_keeps_missing_argument_error(runner):
    result = runner.invoke(app, ["run"])

    assert result.exit_code != 0
    plain_output = strip_ansi(result.output)
    assert "Missing argument 'TARGET'" in plain_output
    assert "Usage: root run" in plain_output


def test_deploy_keeps_callback_behavior(runner):
    with (
        patch(
            "runlayer_cli.commands.deploy.resolve_credentials",
            return_value={"secret": "test-secret", "host": "http://localhost:3000"},
        ),
        patch("runlayer_cli.commands.deploy.deploy_service") as mock_deploy,
    ):
        result = runner.invoke(app, ["deploy"])

    assert result.exit_code == 0
    assert strip_ansi(result.output) == ""
    mock_deploy.assert_called_once_with(
        config_path="runlayer.yaml",
        secret="test-secret",
        host="http://localhost:3000",
        env_file=None,
    )


def test_scan_keeps_callback_behavior(runner, tmp_path):
    scan_result = SimpleNamespace(total_servers=0, total_skills=0, total_plugins=0)

    with (
        patch(
            "runlayer_cli.commands.scan.resolve_credentials",
            return_value={"secret": None, "host": "http://localhost:3000"},
        ),
        patch(
            "runlayer_cli.commands.scan.setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        patch(
            "runlayer_cli.commands.scan.scan_all_clients",
            return_value=scan_result,
        ) as mock_scan,
    ):
        result = runner.invoke(app, ["scan", "--dry-run"])

    assert result.exit_code == 0
    plain_output = strip_ansi(result.output)
    assert "Scanning MCP client configurations and skills..." in plain_output
    assert "No MCP servers, skills, or plugins found." in plain_output
    assert "Usage:" not in plain_output
    mock_scan.assert_called_once()


def test_login_keeps_action_behavior(runner):
    authorize_response = SimpleNamespace(
        status_code=200,
        json=lambda: {
            "device_code": "device-code",
            "user_code": "user-code",
            "verification_uri": "https://example.com/device",
            "verification_uri_complete": "https://example.com/device?code=user-code",
            "expires_in": 60,
            "interval": 1,
        },
    )
    token_response = SimpleNamespace(
        status_code=200,
        json=lambda: {"api_key": "rl_test_secret"},
    )

    class FakeClient:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return None

        def post(self, url, **kwargs):
            if url.endswith("/authorize"):
                return authorize_response
            return token_response

    with (
        patch(
            "runlayer_cli.commands.auth.load_config",
            return_value=Config(default_host="https://example.com"),
        ),
        patch("runlayer_cli.commands.auth.save_config"),
        patch("runlayer_cli.commands.auth.webbrowser.open"),
        patch("runlayer_cli.commands.auth.time.sleep"),
        patch("runlayer_cli.commands.auth.time.time", side_effect=[0, 1]),
        patch("runlayer_cli.commands.auth.httpx.Client", return_value=FakeClient()),
    ):
        result = runner.invoke(app, ["login"])

    assert result.exit_code == 0
    plain_output = strip_ansi(result.output)
    assert "To authenticate, visit:" in plain_output
    assert "Successfully authenticated!" in plain_output
    assert "Usage:" not in plain_output


def test_logout_keeps_action_behavior(runner, runlayer_home):
    result = runner.invoke(app, ["logout"])

    assert result.exit_code == 0
    plain_output = strip_ansi(result.output)
    assert (
        "cleared successfully" in plain_output
        or "No credentials found." in plain_output
    )
    assert "Usage:" not in plain_output
