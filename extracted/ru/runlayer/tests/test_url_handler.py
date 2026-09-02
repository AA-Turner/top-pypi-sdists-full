from unittest.mock import patch

import pytest
import typer
from typer.testing import CliRunner

from runlayer_cli.config import Config
from runlayer_cli.main import app


runner = CliRunner()


def test_handle_url_command_is_hidden():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "__handle-url" not in result.stdout


def test_handle_url_login_uses_configured_host():
    with (
        patch(
            "runlayer_cli.commands.url_handler._resolve_configured_host",
            return_value="https://app.runlayer.com",
        ),
        patch("runlayer_cli.commands.url_handler.login") as login,
    ):
        result = runner.invoke(app, ["__handle-url", "runlayer://login"])

    assert result.exit_code == 0, result.output
    login.assert_called_once_with(host="https://app.runlayer.com", ca_bundle=None)


def test_handle_url_sync_is_noninteractive():
    with (
        patch(
            "runlayer_cli.commands.url_handler._resolve_configured_host",
            return_value="https://app.runlayer.com",
        ),
        patch("runlayer_cli.commands.url_handler.setup_sync") as setup_sync,
    ):
        result = runner.invoke(app, ["__handle-url", "runlayer://sync"])

    assert result.exit_code == 0, result.output
    setup_sync.assert_called_once()
    kwargs = setup_sync.call_args.kwargs
    assert kwargs == {
        "ctx": setup_sync.call_args.kwargs["ctx"],
        "client": None,
        "header": None,
        "secret": None,
        "host": "https://app.runlayer.com",
        "yes": True,
    }


def test_handle_url_dashboard_prefers_global_host():
    with (
        patch("runlayer_cli.commands.url_handler.load_config") as load_config,
        patch(
            "runlayer_cli.commands.url_handler.webbrowser.open",
            return_value=True,
        ) as open_browser,
    ):
        result = runner.invoke(
            app,
            [
                "--host",
                "https://tenant.runlayer.com/",
                "__handle-url",
                "runlayer://dashboard",
            ],
        )

    assert result.exit_code == 0, result.output
    load_config.assert_not_called()
    open_browser.assert_called_once_with("https://tenant.runlayer.com")


def test_handle_url_login_without_configured_host_is_actionable():
    """The tray relies on this exit code to fall back to its own host prompt."""
    with (
        patch(
            "runlayer_cli.commands.url_handler._resolve_configured_host",
            return_value=None,
        ),
        patch("runlayer_cli.commands.auth.load_config", return_value=Config()),
    ):
        result = runner.invoke(app, ["__handle-url", "runlayer://login"])

    assert result.exit_code == 1
    assert "No host configured" in result.stderr


@pytest.mark.parametrize("exit_code", [0, 1, 2])
def test_handle_url_preserves_inner_command_exit_code(exit_code: int):
    with (
        patch(
            "runlayer_cli.commands.url_handler._resolve_configured_host",
            return_value="https://app.runlayer.com",
        ),
        patch(
            "runlayer_cli.commands.url_handler.setup_sync",
            side_effect=typer.Exit(exit_code),
        ),
    ):
        result = runner.invoke(app, ["__handle-url", "runlayer://sync"])

    assert result.exit_code == exit_code
    assert result.stderr == ""


@pytest.mark.parametrize(
    "url",
    [
        "https://login",
        "runlayer:login",
        "runlayer://unknown",
        "runlayer://login/extra",
        "runlayer://login?host=https://evil.example",
        "runlayer://login#fragment",
        "runlayer://user@login",
        "runlayer://login:80",
        "RUNLAYER://login",
    ],
)
def test_handle_url_rejects_noncanonical_urls(url: str):
    with (
        patch("runlayer_cli.commands.url_handler.login") as login,
        patch("runlayer_cli.commands.url_handler.setup_sync") as setup_sync,
        patch("runlayer_cli.commands.url_handler.webbrowser.open") as open_browser,
    ):
        result = runner.invoke(app, ["__handle-url", url])

    assert result.exit_code == 2
    assert "Unsupported Runlayer URL" in result.stderr
    login.assert_not_called()
    setup_sync.assert_not_called()
    open_browser.assert_not_called()


@pytest.mark.parametrize(
    "host",
    [
        "file:///tmp/dashboard",
        "javascript:alert(1)",
        "https:///missing-host",
    ],
)
def test_handle_url_dashboard_rejects_unsafe_configured_host(host: str):
    with (
        patch(
            "runlayer_cli.commands.url_handler._resolve_configured_host",
            return_value=host,
        ),
        patch("runlayer_cli.commands.url_handler.webbrowser.open") as open_browser,
    ):
        result = runner.invoke(app, ["__handle-url", "runlayer://dashboard"])

    assert result.exit_code == 2
    assert "Dashboard host must be an HTTP(S) URL" in result.stderr
    open_browser.assert_not_called()
