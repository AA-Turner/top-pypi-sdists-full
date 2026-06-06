"""Basic tests for the CLI."""

import os
import re
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import anyio
import pytest
import typer
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData
from typer.testing import CliRunner
import yaml

from runlayer_cli.config import Config
from runlayer_cli.main import app
from runlayer_cli.tls import async_http_client

runner = CliRunner()
REAL_ANYIO_RUN = anyio.run


def strip_ansi(text: str) -> str:
    """Strip ANSI escape codes from text."""
    ansi_escape = re.compile(r"\x1b\[[0-9;]*m")
    return ansi_escape.sub("", text)


def test_help_command():
    """Test that the help command shows usage information."""
    # Test top-level help
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    plain_output = strip_ansi(result.stdout)
    assert "Run MCP servers via HTTP transport" in plain_output
    assert "--version" in plain_output
    assert "--secret" in plain_output
    assert "--host" in plain_output

    # Test run command help
    result = runner.invoke(app, ["run", "--help"])
    assert result.exit_code == 0
    plain_output = strip_ansi(result.stdout)
    assert "Run an MCP server via HTTP transport" in plain_output
    assert "TARGET" in plain_output
    assert "--secret" in plain_output
    assert "--host" in plain_output


def test_root_command_shows_help_by_default():
    """Test that bare root command shows help instead of missing-command error."""
    result = runner.invoke(app, [])
    assert result.exit_code == 0

    plain_output = strip_ansi(result.output)
    assert "Run MCP servers via HTTP transport" in plain_output
    assert "Commands" in plain_output
    assert "run" in plain_output
    assert "scan" in plain_output
    assert "Missing command" not in plain_output


@pytest.mark.parametrize(
    ("args", "expected_text"),
    [
        (["cache"], "clear"),
        (["org-api-key"], "add"),
        (["setup"], "hooks"),
        (["skills"], "add"),
        (["plugins"], "add"),
        (["terraform"], "export"),
    ],
)
def test_group_commands_show_help_by_default(args: list[str], expected_text: str):
    """Test that bare group commands show help instead of missing-command error."""
    result = runner.invoke(app, args)
    assert result.exit_code == 0

    plain_output = strip_ansi(result.output)
    assert "Usage:" in plain_output
    assert expected_text in plain_output
    assert "Missing command" not in plain_output


def test_version_command():
    """Test that the version command shows version information."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    plain_output = strip_ansi(result.stdout)
    assert "runlayer version" in plain_output

    # Test short version flag
    result = runner.invoke(app, ["-v"])
    assert result.exit_code == 0
    plain_output = strip_ansi(result.stdout)
    assert "runlayer version" in plain_output


def test_run_command_requires_arguments():
    """Test that run command requires a target and secret."""
    result = runner.invoke(app, ["run"])
    assert result.exit_code != 0
    plain_output = strip_ansi(result.output)
    assert "Missing argument 'TARGET'" in plain_output
    assert "Usage: root run" in plain_output


def test_default_command_behavior():
    """Test that run command without secret triggers login or fails."""
    with patch("runlayer_cli.commands.auth.login"):
        with patch("runlayer_cli.config.load_config") as mock_load:
            mock_config = type("Config", (), {"secret": None, "host": None})()
            mock_load.return_value = mock_config
            result = runner.invoke(app, ["run", "test-uuid"])
            assert result.exit_code != 0


def test_run_starts_login_when_host_has_no_stored_credentials(tmp_path: Path):
    """Run should start login when --secret is omitted for an unknown host."""
    existing_config = Config(
        default_host="https://saved.runlayer.com",
        hosts={
            "saved.runlayer.com": {
                "url": "https://saved.runlayer.com",
                "secret": "rl_saved_secret",
            }
        },
    )
    post_login_config = Config(
        default_host="https://target.runlayer.com",
        hosts={
            "saved.runlayer.com": {
                "url": "https://saved.runlayer.com",
                "secret": "rl_saved_secret",
            },
            "target.runlayer.com": {
                "url": "https://target.runlayer.com",
                "secret": "rl_target_secret",
            },
        },
    )
    server_details = SimpleNamespace(
        name="Test Server",
        transport_type="stdio",
        url="echo",
        transport_config={},
        sync_required=False,
        catalog_entry_name=None,
    )

    with (
        patch(
            "runlayer_cli.config.load_config",
            side_effect=[existing_config, post_login_config],
        ),
        patch("runlayer_cli.commands.auth.login") as login_mock,
        patch("runlayer_cli.main.setup_logging", return_value=tmp_path / "run.log"),
        patch("runlayer_cli.main.RunlayerClient") as client_class,
        patch("runlayer_cli.main.StdioTransport"),
        patch("runlayer_cli.main.ProxyClient"),
        patch("runlayer_cli.main.FastMCPProxy") as proxy_class,
        patch("runlayer_cli.main.anyio.run"),
    ):
        client_class.return_value.get_server_details.return_value = server_details

        result = runner.invoke(
            app,
            ["run", "test-uuid", "--host", "https://target.runlayer.com"],
        )

    assert result.exit_code == 0
    login_mock.assert_called_once_with(host="https://target.runlayer.com")
    client_class.assert_called_once_with(
        hostname="https://target.runlayer.com",
        secret="rl_target_secret",
    )
    proxy_class.return_value.add_middleware.assert_called_once()


def test_run_uses_stored_credentials_without_login(tmp_path: Path):
    """Run should use host-matching config creds when --secret is omitted."""
    config = Config(
        default_host="https://target.runlayer.com",
        hosts={
            "target.runlayer.com": {
                "url": "https://target.runlayer.com",
                "secret": "rl_target_secret",
            }
        },
    )
    server_details = SimpleNamespace(
        name="Test Server",
        transport_type="stdio",
        url="echo",
        transport_config={},
        sync_required=False,
        catalog_entry_name=None,
    )

    with (
        patch("runlayer_cli.config.load_config", return_value=config),
        patch("runlayer_cli.commands.auth.login") as login_mock,
        patch("runlayer_cli.main.setup_logging", return_value=tmp_path / "run.log"),
        patch("runlayer_cli.main.RunlayerClient") as client_class,
        patch("runlayer_cli.main.StdioTransport"),
        patch("runlayer_cli.main.ProxyClient"),
        patch("runlayer_cli.main.FastMCPProxy") as proxy_class,
        patch("runlayer_cli.main.anyio.run"),
    ):
        client_class.return_value.get_server_details.return_value = server_details

        result = runner.invoke(
            app,
            ["run", "test-uuid", "--host", "https://target.runlayer.com"],
        )

    assert result.exit_code == 0
    login_mock.assert_not_called()
    client_class.assert_called_once_with(
        hostname="https://target.runlayer.com",
        secret="rl_target_secret",
    )
    proxy_class.return_value.add_middleware.assert_called_once()


def test_run_skips_login_when_secret_is_passed(tmp_path: Path):
    """Run should never start login when --secret is provided explicitly."""
    server_details = SimpleNamespace(
        name="Test Server",
        transport_type="stdio",
        url="echo",
        transport_config={},
        sync_required=False,
        catalog_entry_name=None,
    )

    with (
        patch("runlayer_cli.config.load_config", return_value=Config()),
        patch("runlayer_cli.commands.auth.login") as login_mock,
        patch("runlayer_cli.main.setup_logging", return_value=tmp_path / "run.log"),
        patch("runlayer_cli.main.RunlayerClient") as client_class,
        patch("runlayer_cli.main.StdioTransport"),
        patch("runlayer_cli.main.ProxyClient"),
        patch("runlayer_cli.main.FastMCPProxy") as proxy_class,
        patch("runlayer_cli.main.anyio.run"),
    ):
        client_class.return_value.get_server_details.return_value = server_details

        result = runner.invoke(
            app,
            [
                "run",
                "test-uuid",
                "--host",
                "https://target.runlayer.com",
                "--secret",
                "rl_direct_secret",
            ],
        )

    assert result.exit_code == 0
    login_mock.assert_not_called()
    client_class.assert_called_once_with(
        hostname="https://target.runlayer.com",
        secret="rl_direct_secret",
    )
    proxy_class.return_value.add_middleware.assert_called_once()


def test_run_stdio_inherits_parent_env_when_transport_env_missing(tmp_path: Path):
    server_details = SimpleNamespace(
        name="Test Server",
        transport_type="stdio",
        url="echo",
        transport_config={},
        sync_required=False,
        catalog_entry_name=None,
    )

    with (
        patch.dict(os.environ, {"TEST_FOO": "from-shell"}, clear=False),
        patch("runlayer_cli.config.load_config", return_value=Config()),
        patch("runlayer_cli.main.setup_logging", return_value=tmp_path / "run.log"),
        patch("runlayer_cli.main.RunlayerClient") as client_class,
        patch("runlayer_cli.main.StdioTransport") as stdio_transport,
        patch("runlayer_cli.main.ProxyClient"),
        patch("runlayer_cli.main.FastMCPProxy"),
        patch("runlayer_cli.main.anyio.run"),
    ):
        client_class.return_value.get_server_details.return_value = server_details

        result = runner.invoke(
            app,
            [
                "run",
                "test-uuid",
                "--host",
                "https://target.runlayer.com",
                "--secret",
                "rl_direct_secret",
            ],
        )

    assert result.exit_code == 0
    assert stdio_transport.call_args.kwargs["env"]["TEST_FOO"] == "from-shell"


def test_run_stdio_transport_env_overrides_parent_env(tmp_path: Path):
    server_details = SimpleNamespace(
        name="Test Server",
        transport_type="stdio",
        url="echo",
        transport_config={
            "env": {"TEST_BAR": "from-config", "TEST_BAZ": "config-only"}
        },
        sync_required=False,
        catalog_entry_name=None,
    )

    with (
        patch.dict(
            os.environ,
            {"TEST_FOO": "from-shell", "TEST_BAR": "from-shell"},
            clear=False,
        ),
        patch("runlayer_cli.config.load_config", return_value=Config()),
        patch("runlayer_cli.main.setup_logging", return_value=tmp_path / "run.log"),
        patch("runlayer_cli.main.RunlayerClient") as client_class,
        patch("runlayer_cli.main.StdioTransport") as stdio_transport,
        patch("runlayer_cli.main.ProxyClient"),
        patch("runlayer_cli.main.FastMCPProxy"),
        patch("runlayer_cli.main.anyio.run"),
    ):
        client_class.return_value.get_server_details.return_value = server_details

        result = runner.invoke(
            app,
            [
                "run",
                "test-uuid",
                "--host",
                "https://target.runlayer.com",
                "--secret",
                "rl_direct_secret",
            ],
        )

    assert result.exit_code == 0
    env = stdio_transport.call_args.kwargs["env"]
    assert env["TEST_FOO"] == "from-shell"
    assert env["TEST_BAR"] == "from-config"
    assert env["TEST_BAZ"] == "config-only"


def test_run_passes_uuid_target_through_without_resolution(tmp_path: Path):
    server_id = "550e8400-e29b-41d4-a716-446655440000"
    server_details = SimpleNamespace(
        name="Test Server",
        transport_type="stdio",
        url="echo",
        transport_config={},
        sync_required=False,
        catalog_entry_name=None,
    )

    with (
        patch("runlayer_cli.config.load_config", return_value=Config()),
        patch("runlayer_cli.main.setup_logging", return_value=tmp_path / "run.log"),
        patch("runlayer_cli.main.RunlayerClient") as client_class,
        patch("runlayer_cli.main.StdioTransport"),
        patch("runlayer_cli.main.ProxyClient"),
        patch("runlayer_cli.main.FastMCPProxy"),
        patch("runlayer_cli.main.anyio.run"),
    ):
        client = client_class.return_value
        client.get_server_details.return_value = server_details

        result = runner.invoke(
            app,
            [
                "run",
                server_id,
                "--host",
                "https://target.runlayer.com",
                "--secret",
                "rl_direct_secret",
            ],
        )

    assert result.exit_code == 0
    client.resolve_server_target.assert_not_called()
    client.get_server_details.assert_called_once_with(server_id)


def test_run_resolves_alias_before_server_lookup(tmp_path: Path):
    alias = "@runlayer/agent-terminal"
    server_id = "550e8400-e29b-41d4-a716-446655440000"
    server_details = SimpleNamespace(
        name="Test Server",
        transport_type="stdio",
        url="echo",
        transport_config={},
        sync_required=False,
        catalog_entry_name=None,
    )

    with (
        patch("runlayer_cli.config.load_config", return_value=Config()),
        patch("runlayer_cli.main.setup_logging", return_value=tmp_path / "run.log"),
        patch("runlayer_cli.main.RunlayerClient") as client_class,
        patch("runlayer_cli.main.StdioTransport"),
        patch("runlayer_cli.main.ProxyClient"),
        patch("runlayer_cli.main.FastMCPProxy"),
        patch("runlayer_cli.main.anyio.run"),
    ):
        client = client_class.return_value
        client.resolve_server_target.return_value = server_id
        client.get_server_details.return_value = server_details

        result = runner.invoke(
            app,
            [
                "run",
                alias,
                "--host",
                "https://target.runlayer.com",
                "--secret",
                "rl_direct_secret",
            ],
        )

    assert result.exit_code == 0
    client.resolve_server_target.assert_called_once_with(alias)
    client.get_server_details.assert_called_once_with(server_id)


def test_run_sync_uses_resolved_alias_server_id(tmp_path: Path):
    alias = "@runlayer/agent-terminal"
    server_id = "550e8400-e29b-41d4-a716-446655440000"
    server_details = SimpleNamespace(
        name="Test Server",
        transport_type="stdio",
        url="echo",
        transport_config={},
        sync_required=True,
        catalog_entry_name=None,
    )

    with (
        patch("runlayer_cli.config.load_config", return_value=Config()),
        patch("runlayer_cli.main.setup_logging", return_value=tmp_path / "run.log"),
        patch("runlayer_cli.main.RunlayerClient") as client_class,
        patch("runlayer_cli.main.StdioTransport"),
        patch("runlayer_cli.main.ProxyClient"),
        patch("runlayer_cli.main.FastMCPProxy") as proxy_class,
        patch(
            "runlayer_cli.main.sync_local_capabilities", new_callable=AsyncMock
        ) as sync_mock,
        patch(
            "runlayer_cli.main.anyio.run",
            side_effect=lambda func: REAL_ANYIO_RUN(func),
        ),
    ):
        client = client_class.return_value
        client.resolve_server_target.return_value = server_id
        client.get_server_details.return_value = server_details
        proxy_class.return_value.run_stdio_async = AsyncMock()

        result = runner.invoke(
            app,
            [
                "run",
                alias,
                "--host",
                "https://target.runlayer.com",
                "--secret",
                "rl_direct_secret",
            ],
        )

    assert result.exit_code == 0
    sync_mock.assert_awaited_once_with(client, proxy_class.return_value, server_id)


def test_run_continues_when_startup_sync_fails(tmp_path: Path):
    """Regression for ENG-3220: a failing capability sync (e.g. upstream
    ``initialize`` -> ``McpError: Invalid request parameters``) must not abort the
    connector. The run should log and still serve via ``run_stdio_async``.
    """
    server_id = "550e8400-e29b-41d4-a716-446655440000"
    server_details = SimpleNamespace(
        name="Test Server",
        transport_type="stdio",
        url="echo",
        transport_config={},
        sync_required=True,
        catalog_entry_name=None,
    )

    sync_error = McpError(ErrorData(code=-32602, message="Invalid request parameters"))

    with (
        patch("runlayer_cli.config.load_config", return_value=Config()),
        patch("runlayer_cli.main.setup_logging", return_value=tmp_path / "run.log"),
        patch("runlayer_cli.main.RunlayerClient") as client_class,
        patch("runlayer_cli.main.StdioTransport"),
        patch("runlayer_cli.main.ProxyClient"),
        patch("runlayer_cli.main.FastMCPProxy") as proxy_class,
        patch(
            "runlayer_cli.main.sync_local_capabilities",
            new_callable=AsyncMock,
            side_effect=sync_error,
        ) as sync_mock,
        patch(
            "runlayer_cli.main.anyio.run",
            side_effect=lambda func: REAL_ANYIO_RUN(func),
        ),
    ):
        client_class.return_value.get_server_details.return_value = server_details
        proxy_class.return_value.run_stdio_async = AsyncMock()

        result = runner.invoke(
            app,
            [
                "run",
                server_id,
                "--host",
                "https://target.runlayer.com",
                "--secret",
                "rl_direct_secret",
            ],
        )

    assert result.exit_code == 0
    sync_mock.assert_awaited_once()
    proxy_class.return_value.run_stdio_async.assert_awaited_once_with(show_banner=False)


@pytest.mark.parametrize("transport_type", ["sse", "streaming-http"])
def test_run_skips_startup_sync_for_non_stdio_transports(
    tmp_path: Path, transport_type: str
):
    """Startup sync must wait for middleware once non-stdio transports connect."""
    server_details = SimpleNamespace(
        name="Test Server",
        transport_type=transport_type,
        url="https://example.com/mcp",
        transport_config={},
        sync_required=True,
        catalog_entry_name=None,
    )

    with (
        patch("runlayer_cli.config.load_config", return_value=Config()),
        patch("runlayer_cli.main.setup_logging", return_value=tmp_path / "run.log"),
        patch("runlayer_cli.main.RunlayerClient") as client_class,
        patch("runlayer_cli.main.SSETransport") as sse_transport_class,
        patch("runlayer_cli.main.StreamableHttpTransport") as stream_transport_class,
        patch("runlayer_cli.main.ProxyClient"),
        patch("runlayer_cli.main.FastMCPProxy") as proxy_class,
        patch(
            "runlayer_cli.main.sync_local_capabilities", new_callable=AsyncMock
        ) as sync_mock,
        patch(
            "runlayer_cli.main.anyio.run",
            side_effect=lambda func: REAL_ANYIO_RUN(func),
        ),
    ):
        client_class.return_value.get_server_details.return_value = server_details
        proxy_class.return_value.run_stdio_async = AsyncMock()

        result = runner.invoke(
            app,
            [
                "run",
                "test-uuid",
                "--host",
                "https://target.runlayer.com",
                "--secret",
                "rl_direct_secret",
            ],
        )

    assert result.exit_code == 0
    transport_class = (
        sse_transport_class if transport_type == "sse" else stream_transport_class
    )
    assert transport_class.call_args.kwargs["httpx_client_factory"] is async_http_client
    sync_mock.assert_not_awaited()
    proxy_class.return_value.run_stdio_async.assert_awaited_once_with(show_banner=False)


def test_run_command_with_secret_requires_host():
    """Test that run command with server UUID and secret still requires host."""
    result = runner.invoke(app, ["run", "test-uuid", "--secret", "test-secret"])
    assert result.exit_code != 0
    # Should fail because --host is missing (or connection fails)


def test_validate_command_requires_args():
    """Test that validate command requires secret and config."""
    with patch("runlayer_cli.commands.auth.login"):
        with patch("runlayer_cli.config.load_config") as mock_load:
            mock_config = type("Config", (), {"secret": None, "host": None})()
            mock_load.return_value = mock_config
            result = runner.invoke(app, ["deploy", "validate", "--config", "test.yaml"])
            assert result.exit_code != 0

    # Missing config (should work with default)
    result = runner.invoke(app, ["deploy", "validate", "--secret", "test-secret"])
    # May fail due to missing file or connection, but should not fail due to missing args
    assert result.exit_code != 0  # Will fail on file not found or connection


def test_validate_command_success():
    """Test validate command with valid YAML."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        config = {
            "name": "test-service",
            "runtime": "docker",
            "service": {"port": 8000},
        }
        yaml.dump(config, f)
        config_path = f.name

    try:
        with patch("runlayer_cli.commands.deploy.validate_service") as mock_validate:
            runner.invoke(
                app,
                [
                    "deploy",
                    "validate",
                    "--config",
                    config_path,
                    "--secret",
                    "test-secret",
                    "--host",
                    "http://localhost:3000",
                ],
            )
            # Should call validate_service
            mock_validate.assert_called_once_with(
                config_path=config_path,
                secret="test-secret",
                host="http://localhost:3000",
                env_file=None,
            )
    finally:
        Path(config_path).unlink()


def test_validate_command_error():
    """Test validate command with invalid YAML."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("invalid: yaml: content")
        config_path = f.name

    try:
        with patch("runlayer_cli.commands.deploy.validate_service") as mock_validate:
            mock_validate.side_effect = typer.Exit(1)

            result = runner.invoke(
                app,
                [
                    "deploy",
                    "validate",
                    "--config",
                    config_path,
                    "--secret",
                    "test-secret",
                    "--host",
                    "http://localhost:3000",
                ],
            )
            # Should have called validate_service and exited with error
            assert result.exit_code != 0
            mock_validate.assert_called_once()
    finally:
        Path(config_path).unlink()


def test_deploy_bare_command_still_executes_callback():
    """Bare deploy should keep executing its callback, not show help."""
    with (
        patch(
            "runlayer_cli.commands.deploy.resolve_credentials",
            return_value={"secret": "test-secret", "host": "http://localhost:3000"},
        ),
        patch("runlayer_cli.commands.deploy.deploy_service") as mock_deploy,
    ):
        result = runner.invoke(app, ["deploy"])

    assert result.exit_code == 0
    plain_output = strip_ansi(result.output)
    assert "Usage:" not in plain_output
    mock_deploy.assert_called_once_with(
        config_path="runlayer.yaml",
        secret="test-secret",
        host="http://localhost:3000",
        env_file=None,
    )


def test_scan_bare_command_still_executes_callback(tmp_path: Path):
    """Bare scan should keep executing its callback, not show help."""
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
