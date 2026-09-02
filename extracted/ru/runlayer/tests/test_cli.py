"""Basic tests for the CLI."""

import os
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import ANY, AsyncMock, Mock, patch

import anyio
import pytest
import typer
import yaml
from typer.testing import CliRunner

from runlayer_cli import regex_safe
from runlayer_cli.config import Config
from runlayer_cli.main import _oauth_for_server, app
from runlayer_cli.models import ServerDetails
from runlayer_cli.scan.resource_governor import (
    DEFAULT_CPU_PERCENT,
    DEFAULT_MEMORY_LIMIT_MB,
    MAX_CPU_CORES,
    MAX_CPU_PERCENT,
    MAX_MEMORY_LIMIT_MB,
    MIN_CPU_PERCENT,
    MIN_MEMORY_LIMIT_MB,
    default_cpu_cores,
)
from runlayer_cli.tls import async_http_client

runner = CliRunner()
REAL_ANYIO_RUN = anyio.run


def strip_ansi(text: str) -> str:
    """Strip ANSI escape codes from text."""
    ansi_escape = regex_safe.compile(r"\x1b\[[0-9;]*m")
    return ansi_escape.sub("", text)


def test_manual_oauth_requires_client_id() -> None:
    details = ServerDetails(
        id="server-id",
        name="Manual OAuth server",
        url="https://example.com/mcp",
        transport_type="streaming-http",
        requires_manual_oauth_setup=True,
    )

    with pytest.raises(
        ValueError,
        match="Manual OAuth setup is incomplete.*client ID",
    ):
        _oauth_for_server(details)


def test_manual_oauth_public_client_without_secret() -> None:
    # Public PKCE client (e.g. an Okta app with no secret): id-only manual
    # setup is valid and must not fall back to dynamic client registration.
    details = ServerDetails(
        id="server-id",
        name="Manual OAuth server",
        url="https://example.com/mcp",
        transport_type="streaming-http",
        requires_manual_oauth_setup=True,
        manual_oauth_client_id="configured-client",
    )

    with patch("runlayer_cli.main.OAuth") as oauth:
        result = _oauth_for_server(details)

    assert result is oauth.return_value
    # oauth.py derives token_endpoint_auth_method="none" from the missing
    # secret; main.py passes the (absent) server preference through untouched.
    oauth.assert_called_once_with(
        mcp_url="https://example.com/mcp",
        client_name=ANY,
        callback_port=None,
        manual_client_id="configured-client",
        manual_client_secret=None,
        scopes=None,
        token_endpoint_auth_method=None,
    )


def test_manual_oauth_callback_port_from_server() -> None:
    details = ServerDetails(
        id="server-id",
        name="Manual OAuth server",
        url="https://example.com/mcp",
        transport_type="streaming-http",
        requires_manual_oauth_setup=True,
        manual_oauth_client_id="configured-client",
        manual_oauth_callback_port=8080,
    )

    with patch("runlayer_cli.main.OAuth") as oauth:
        _oauth_for_server(details)
    assert oauth.call_args.kwargs["callback_port"] == 8080

    # An explicit --oauth-callback-port wins over the server-configured port.
    with patch("runlayer_cli.main.OAuth") as oauth:
        _oauth_for_server(details, callback_port=9999)
    assert oauth.call_args.kwargs["callback_port"] == 9999

    # A stale stored port must not constrain DCR/broker flows after the
    # server leaves manual registration.
    details_dcr = details.model_copy(update={"requires_manual_oauth_setup": False})
    with patch("runlayer_cli.main.OAuth") as oauth:
        _oauth_for_server(details_dcr)
    assert oauth.call_args.kwargs["callback_port"] is None


def test_manual_oauth_uses_configured_client_credentials() -> None:
    details = ServerDetails(
        id="server-id",
        name="Manual OAuth server",
        url="https://example.com/mcp",
        transport_type="streaming-http",
        requires_manual_oauth_setup=True,
        manual_oauth_client_id="configured-client",
        manual_oauth_client_secret="configured-secret",
        manual_oauth_scopes="read:incidents write:incidents",
        preferred_token_endpoint_auth_method="client_secret_basic",
    )

    with patch("runlayer_cli.main.OAuth") as oauth:
        result = _oauth_for_server(details)

    assert result is oauth.return_value
    oauth.assert_called_once_with(
        mcp_url="https://example.com/mcp",
        client_name=ANY,
        callback_port=None,
        manual_client_id="configured-client",
        manual_client_secret="configured-secret",
        scopes="read:incidents write:incidents",
        token_endpoint_auth_method="client_secret_basic",
    )


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
        identity_forward=None,
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
        flow_queue=ANY,
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
        identity_forward=None,
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
        flow_queue=ANY,
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
        identity_forward=None,
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
        flow_queue=ANY,
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
        identity_forward=None,
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
        identity_forward=None,
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
        identity_forward=None,
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
        identity_forward=None,
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


def test_run_kicks_background_sync_at_startup(tmp_path: Path):
    """Sync must start without waiting for tools/list: clients cache the tool
    list across reconnects, so the middleware list hook alone may never fire.
    """
    server_id = "550e8400-e29b-41d4-a716-446655440000"
    server_details = SimpleNamespace(
        id=server_id,
        name="Test Server",
        transport_type="stdio",
        url="echo",
        transport_config={},
        version=7,
        sync_required=True,
        catalog_entry_name=None,
        identity_forward=None,
    )

    with (
        patch("runlayer_cli.config.load_config", return_value=Config()),
        patch("runlayer_cli.main.setup_logging", return_value=tmp_path / "run.log"),
        patch("runlayer_cli.main.RunlayerClient") as client_class,
        patch("runlayer_cli.main.StdioTransport"),
        patch("runlayer_cli.main.ProxyClient"),
        patch("runlayer_cli.main.FastMCPProxy") as proxy_class,
        patch(
            "runlayer_cli.middleware.sync_local_capabilities", new_callable=AsyncMock
        ) as sync_mock,
        patch(
            "runlayer_cli.main.anyio.run",
            side_effect=lambda func: REAL_ANYIO_RUN(func),
        ),
    ):
        client_class.return_value.get_server_details.return_value = server_details

        async def serve_briefly(**kwargs):
            await anyio.sleep(0.05)

        proxy_class.return_value.run_stdio_async = AsyncMock(side_effect=serve_briefly)

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
    sync_mock.assert_awaited_once_with(
        client_class.return_value,
        proxy_class.return_value,
        server_id,
        server_version=7,
    )


@pytest.mark.parametrize("transport_type", ["sse", "streaming-http"])
def test_run_uses_tls_http_client_for_remote_transports(
    tmp_path: Path, transport_type: str
):
    """Capability sync is middleware-owned for every transport; run() only serves."""
    server_details = SimpleNamespace(
        name="Test Server",
        transport_type=transport_type,
        url="https://example.com/mcp",
        transport_config={},
        sync_required=True,
        catalog_entry_name=None,
        identity_forward=None,
        requires_manual_oauth_setup=False,
        manual_oauth_client_id=None,
        manual_oauth_client_secret=None,
        manual_oauth_callback_port=None,
        preferred_token_endpoint_auth_method=None,
    )

    with (
        patch("runlayer_cli.config.load_config", return_value=Config()),
        patch("runlayer_cli.main.setup_logging", return_value=tmp_path / "run.log"),
        patch("runlayer_cli.main.RunlayerClient") as client_class,
        patch("runlayer_cli.main.OAuth"),
        patch("runlayer_cli.main.SSETransport") as sse_transport_class,
        patch("runlayer_cli.main.StreamableHttpTransport") as stream_transport_class,
        patch("runlayer_cli.main.ProxyClient"),
        patch("runlayer_cli.main.FastMCPProxy") as proxy_class,
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
    proxy_class.return_value.run_stdio_async.assert_awaited_once_with(show_banner=False)


def _invoke_streaming_http_run(
    tmp_path: Path, args: list[str], env: dict[str, str | None] | None = None
):
    server_details = ServerDetails(
        id="server-id",
        name="Test Server",
        transport_type="streaming-http",
        url="https://example.com/mcp",
        transport_config={},
        sync_required=False,
        catalog_entry_name=None,
        identity_forward=None,
    )

    with (
        patch("runlayer_cli.config.load_config", return_value=Config()),
        patch("runlayer_cli.main.setup_logging", return_value=tmp_path / "run.log"),
        patch("runlayer_cli.main.RunlayerClient") as client_class,
        patch("runlayer_cli.main.OAuth") as oauth_class,
        patch("runlayer_cli.main.StreamableHttpTransport"),
        patch("runlayer_cli.main.ProxyClient"),
        patch("runlayer_cli.main.FastMCPProxy"),
        patch("runlayer_cli.main.anyio.run"),
    ):
        client_class.return_value.get_server_details.return_value = server_details

        result = runner.invoke(app, args, env=env)

    assert result.exit_code == 0, result.output
    return oauth_class.call_args.kwargs


def test_run_passes_oauth_callback_port_to_streaming_http(tmp_path: Path):
    kwargs = _invoke_streaming_http_run(
        tmp_path,
        [
            "run",
            "test-uuid",
            "--host",
            "https://target.runlayer.com",
            "--secret",
            "rl_direct_secret",
            "--oauth-callback-port",
            "9137",
        ],
        env={"RUNLAYER_OAUTH_CALLBACK_PORT": None},
    )

    assert kwargs["callback_port"] == 9137


def test_run_reads_oauth_callback_port_from_env(tmp_path: Path):
    kwargs = _invoke_streaming_http_run(
        tmp_path,
        [
            "run",
            "test-uuid",
            "--host",
            "https://target.runlayer.com",
            "--secret",
            "rl_direct_secret",
        ],
        env={"RUNLAYER_OAUTH_CALLBACK_PORT": "9137"},
    )

    assert kwargs["callback_port"] == 9137


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
    scan_result = SimpleNamespace(
        total_servers=0,
        total_detected_clients=0,
        detected_clients=[],
        total_skills=0,
        total_plugins=0,
        agents=[],
        processes=[],
        containers=[],
        containers_scanned=False,
        wsl_distros=[],
        wsl_scanned=False,
    )

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
    assert (
        "No AI clients, MCP servers, skills, plugins, agents, processes, "
        "or containers found." in plain_output
    )
    assert "Usage:" not in plain_output
    mock_scan.assert_called_once()


def _scan_capturing_project_bounds(
    tmp_path: Path, args: list[str], env: dict[str, str | None] | None = None
) -> dict:
    """Invoke `scan --dry-run` and return the kwargs passed to scan_all_clients.

    Always clears the two project env vars first so each case is hermetic; any
    provided *env* overrides on top.
    """
    base_env: dict[str, str | None] = {
        "RUNLAYER_PROJECT_DEPTH": None,
        "RUNLAYER_PROJECT_TIMEOUT": None,
        "RUNLAYER_DETECT_CONTAINERS": None,
        "RUNLAYER_DETECT_DISGUISED_SKILLS": None,
        "RUNLAYER_ARTIFACT_LOOKUP_CACHE": None,
    }
    if env:
        base_env.update(env)
    scan_result = SimpleNamespace(
        total_servers=0,
        total_detected_clients=0,
        detected_clients=[],
        total_skills=0,
        total_plugins=0,
        agents=[],
        processes=[],
        containers=[],
        containers_scanned=False,
        wsl_distros=[],
        wsl_scanned=False,
    )
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
        result = runner.invoke(app, ["scan", "--dry-run", *args], env=base_env)
    assert result.exit_code == 0, result.output
    mock_scan.assert_called_once()
    return mock_scan.call_args.kwargs


def test_scan_project_bounds_default_when_unset(tmp_path: Path):
    kwargs = _scan_capturing_project_bounds(tmp_path, [])
    assert kwargs["project_scan_depth"] == 7
    assert kwargs["project_scan_timeout"] == 60


def test_scan_project_bounds_from_env(tmp_path: Path):
    kwargs = _scan_capturing_project_bounds(
        tmp_path,
        [],
        env={"RUNLAYER_PROJECT_DEPTH": "10", "RUNLAYER_PROJECT_TIMEOUT": "120"},
    )
    assert kwargs["project_scan_depth"] == 10
    assert kwargs["project_scan_timeout"] == 120


def test_scan_detect_containers_is_off_by_default(tmp_path: Path):
    kwargs = _scan_capturing_project_bounds(tmp_path, [])
    assert kwargs["detect_containers"] is False


def test_scan_detect_containers_from_flag(tmp_path: Path):
    kwargs = _scan_capturing_project_bounds(tmp_path, ["--detect-containers"])
    assert kwargs["detect_containers"] is True


def test_scan_detect_containers_from_env(tmp_path: Path):
    kwargs = _scan_capturing_project_bounds(
        tmp_path,
        [],
        env={"RUNLAYER_DETECT_CONTAINERS": "true"},
    )
    assert kwargs["detect_containers"] is True


def test_scan_detect_disguised_skills_is_off_by_default(tmp_path: Path):
    kwargs = _scan_capturing_project_bounds(tmp_path, [])
    assert kwargs["detect_disguised_skills"] is False


def test_scan_detect_disguised_skills_from_flag(tmp_path: Path):
    kwargs = _scan_capturing_project_bounds(tmp_path, ["--detect-disguised-skills"])
    assert kwargs["detect_disguised_skills"] is True


def test_scan_detect_disguised_skills_from_env(tmp_path: Path):
    kwargs = _scan_capturing_project_bounds(
        tmp_path,
        [],
        env={"RUNLAYER_DETECT_DISGUISED_SKILLS": "true"},
    )
    assert kwargs["detect_disguised_skills"] is True


def test_scan_no_detect_disguised_skills_overrides_env(tmp_path: Path):
    kwargs = _scan_capturing_project_bounds(
        tmp_path,
        ["--no-detect-disguised-skills"],
        env={"RUNLAYER_DETECT_DISGUISED_SKILLS": "true"},
    )
    assert kwargs["detect_disguised_skills"] is False


def _scan_capturing_command_options(
    tmp_path: Path,
    args: list[str],
    env: dict[str, str | None] | None = None,
) -> dict:
    invocation_env = {"RUNLAYER_ARTIFACT_LOOKUP_CACHE": None}
    if env:
        invocation_env.update(env)
    with (
        patch(
            "runlayer_cli.commands.scan.resolve_credentials",
            return_value={"secret": None, "host": "http://localhost:3000"},
        ),
        patch(
            "runlayer_cli.commands.scan.setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        patch("runlayer_cli.commands.scan._run_scan") as mock_run,
    ):
        result = runner.invoke(app, ["scan", "--dry-run", *args], env=invocation_env)
    assert result.exit_code == 0, result.output
    mock_run.assert_called_once()
    return mock_run.call_args.kwargs


def test_scan_artifact_lookup_cache_is_off_by_default(tmp_path: Path):
    kwargs = _scan_capturing_command_options(tmp_path, [])
    assert kwargs["artifact_lookup_cache"] is False


def test_scan_artifact_lookup_cache_from_env(tmp_path: Path):
    kwargs = _scan_capturing_command_options(
        tmp_path,
        [],
        env={"RUNLAYER_ARTIFACT_LOOKUP_CACHE": "true"},
    )
    assert kwargs["artifact_lookup_cache"] is True


def test_scan_no_artifact_lookup_cache_overrides_env(tmp_path: Path):
    kwargs = _scan_capturing_command_options(
        tmp_path,
        ["--no-artifact-lookup-cache"],
        env={"RUNLAYER_ARTIFACT_LOOKUP_CACHE": "true"},
    )
    assert kwargs["artifact_lookup_cache"] is False


def test_scan_explicit_flag_overrides_env_project_bounds(tmp_path: Path):
    kwargs = _scan_capturing_project_bounds(
        tmp_path,
        ["--project-depth", "5", "--project-timeout", "45"],
        env={"RUNLAYER_PROJECT_DEPTH": "10", "RUNLAYER_PROJECT_TIMEOUT": "120"},
    )
    assert kwargs["project_scan_depth"] == 5
    assert kwargs["project_scan_timeout"] == 45


def test_scan_clamps_out_of_range_flags(tmp_path: Path):
    kwargs = _scan_capturing_project_bounds(
        tmp_path, ["--project-depth", "50", "--project-timeout", "999"]
    )
    assert kwargs["project_scan_depth"] == 20
    assert kwargs["project_scan_timeout"] == 300


def test_scan_clamps_out_of_range_env(tmp_path: Path):
    kwargs = _scan_capturing_project_bounds(
        tmp_path,
        [],
        env={"RUNLAYER_PROJECT_DEPTH": "50", "RUNLAYER_PROJECT_TIMEOUT": "999"},
    )
    assert kwargs["project_scan_depth"] == 20
    assert kwargs["project_scan_timeout"] == 300


def _scan_capturing_resource_caps(
    tmp_path: Path, args: list[str], env: dict[str, str | None] | None = None
) -> dict:
    """Invoke `scan --dry-run` and return the kwargs passed to scan_all_clients.

    Clears the three resource-cap env vars first so each case is hermetic; any
    provided *env* overrides on top.
    """
    base_env: dict[str, str | None] = {
        "RUNLAYER_CPU_CORES": None,
        "RUNLAYER_MAX_CPU_PERCENT": None,
        "RUNLAYER_MEMORY_LIMIT_MB": None,
    }
    if env:
        base_env.update(env)
    scan_result = SimpleNamespace(
        total_servers=0,
        total_detected_clients=0,
        detected_clients=[],
        total_skills=0,
        total_plugins=0,
        agents=[],
        processes=[],
        containers=[],
        containers_scanned=False,
        wsl_distros=[],
        wsl_scanned=False,
    )
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
        result = runner.invoke(app, ["scan", "--dry-run", *args], env=base_env)
    assert result.exit_code == 0, result.output
    mock_scan.assert_called_once()
    return mock_scan.call_args.kwargs


def test_scan_resource_caps_default_when_unset(tmp_path: Path):
    kwargs = _scan_capturing_resource_caps(tmp_path, [])
    assert kwargs["cpu_cores"] == default_cpu_cores()
    assert kwargs["max_cpu_percent"] == DEFAULT_CPU_PERCENT
    assert kwargs["memory_limit_mb"] == DEFAULT_MEMORY_LIMIT_MB


def test_scan_resource_caps_from_env(tmp_path: Path):
    kwargs = _scan_capturing_resource_caps(
        tmp_path,
        [],
        env={
            "RUNLAYER_CPU_CORES": "1",
            "RUNLAYER_MAX_CPU_PERCENT": "20",
            "RUNLAYER_MEMORY_LIMIT_MB": "256",
        },
    )
    assert kwargs["cpu_cores"] == 1
    assert kwargs["max_cpu_percent"] == 20
    assert kwargs["memory_limit_mb"] == MIN_MEMORY_LIMIT_MB


def test_scan_explicit_flag_overrides_env_resource_caps(tmp_path: Path):
    kwargs = _scan_capturing_resource_caps(
        tmp_path,
        ["--cpu-cores", "1", "--max-cpu-percent", "30", "--memory-limit-mb", "512"],
        env={
            "RUNLAYER_CPU_CORES": "8",
            "RUNLAYER_MAX_CPU_PERCENT": "90",
            "RUNLAYER_MEMORY_LIMIT_MB": "4096",
        },
    )
    assert kwargs["cpu_cores"] == 1
    assert kwargs["max_cpu_percent"] == 30
    assert kwargs["memory_limit_mb"] == 512


def test_scan_clamps_out_of_range_resource_flags(tmp_path: Path):
    kwargs = _scan_capturing_resource_caps(
        tmp_path,
        [
            "--cpu-cores",
            "99999",
            "--max-cpu-percent",
            "500",
            "--memory-limit-mb",
            "999999",
        ],
    )
    assert kwargs["cpu_cores"] == MAX_CPU_CORES
    assert kwargs["max_cpu_percent"] == MAX_CPU_PERCENT
    assert kwargs["memory_limit_mb"] == MAX_MEMORY_LIMIT_MB


def test_scan_clamps_below_min_resource_flags(tmp_path: Path):
    kwargs = _scan_capturing_resource_caps(
        tmp_path,
        ["--max-cpu-percent", "1", "--memory-limit-mb", "1"],
    )
    assert kwargs["max_cpu_percent"] == MIN_CPU_PERCENT
    assert kwargs["memory_limit_mb"] == MIN_MEMORY_LIMIT_MB


def test_scan_clamps_out_of_range_resource_env(tmp_path: Path):
    kwargs = _scan_capturing_resource_caps(
        tmp_path,
        [],
        env={
            "RUNLAYER_MAX_CPU_PERCENT": "500",
            "RUNLAYER_MEMORY_LIMIT_MB": "999999",
        },
    )
    assert kwargs["max_cpu_percent"] == MAX_CPU_PERCENT
    assert kwargs["memory_limit_mb"] == MAX_MEMORY_LIMIT_MB


def _scan_result(
    *,
    servers: int,
    skills: int = 0,
    plugins: int = 0,
) -> SimpleNamespace:
    server_items = [SimpleNamespace(name=f"server-{idx}") for idx in range(servers)]
    config = SimpleNamespace(servers=server_items)
    return SimpleNamespace(
        total_servers=servers,
        total_detected_clients=0,
        detected_clients=[],
        total_skills=skills,
        total_plugins=plugins,
        total_agents=0,
        total_agent_definitions=0,
        total_processes=0,
        total_containers=0,
        total_wsl_distros=0,
        device_id="device-1",
        hostname="host-1",
        os="darwin",
        os_version="15.0",
        username="user-1",
        org_device_id=None,
        serial_number=None,
        tools=[],
        skills=[SimpleNamespace(name=f"skill-{idx}") for idx in range(skills)],
        plugins=[SimpleNamespace(name=f"plugin-{idx}") for idx in range(plugins)],
        configurations=[config] if servers else [],
        global_configs=[config] if servers else [],
        project_configs=[],
        wsl_configs=[],
        agents=[],
        agent_definitions=[],
        processes=[],
        containers=[],
        containers_scanned=False,
        stopped_containers=[],
        stopped_containers_scanned=False,
        container_images=[],
        container_images_scanned=False,
        wsl_distros=[],
        wsl_scanned=False,
        to_api_payload=lambda: {"device_id": "device-1"},
    )


def test_scan_with_servers_lets_scan_submission_own_detect_checkin(tmp_path: Path):
    scan_result = _scan_result(servers=1)
    client = SimpleNamespace(
        submit_mcp_watch_scan=lambda payload: {
            "servers_processed": 1,
            "shadow_servers_found": 0,
            "managed_servers_matched": 0,
        }
    )

    with (
        patch(
            "runlayer_cli.commands.scan.resolve_credentials",
            return_value={"secret": "rl_org_test", "host": "http://localhost:3000"},
        ),
        patch(
            "runlayer_cli.commands.scan.setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        patch("runlayer_cli.commands.scan.scan_all_clients", return_value=scan_result),
        patch("runlayer_cli.commands.scan.RunlayerClient", return_value=client),
        patch("runlayer_cli.aiwatch_checkin.submit_detect_checkin") as mock_detect,
        patch("runlayer_cli.aiwatch_checkin.submit_enforce_validation_checkin"),
        patch("runlayer_cli.aiwatch_checkin.submit_sessions_validation_checkin"),
    ):
        result = runner.invoke(app, ["scan", "--no-projects"])

    assert result.exit_code == 0, result.output
    assert "Scan complete" in strip_ansi(result.output)
    mock_detect.assert_not_called()


def test_scan_empty_submission_uses_detect_checkin_for_liveness(tmp_path: Path):
    scan_result = _scan_result(servers=0)
    client = SimpleNamespace()

    with (
        patch(
            "runlayer_cli.commands.scan.resolve_credentials",
            return_value={"secret": "rl_org_test", "host": "http://localhost:3000"},
        ),
        patch(
            "runlayer_cli.commands.scan.setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        patch("runlayer_cli.commands.scan.scan_all_clients", return_value=scan_result),
        patch("runlayer_cli.commands.scan.RunlayerClient", return_value=client),
        patch("runlayer_cli.aiwatch_checkin.submit_detect_checkin") as mock_detect,
        patch("runlayer_cli.aiwatch_checkin.submit_enforce_validation_checkin"),
        patch("runlayer_cli.aiwatch_checkin.submit_sessions_validation_checkin"),
    ):
        result = runner.invoke(app, ["scan", "--no-projects"])

    assert result.exit_code == 0, result.output
    assert (
        "No AI clients, MCP servers, skills, plugins, agents, processes, "
        "or containers found." in strip_ansi(result.output)
    )
    mock_detect.assert_called_once_with(client, scan_result)


def test_scan_artifact_only_submission_uses_detect_checkin_fallback(tmp_path: Path):
    scan_result = _scan_result(servers=0, skills=1)
    client = SimpleNamespace()

    with (
        patch(
            "runlayer_cli.commands.scan.resolve_credentials",
            return_value={"secret": "rl_org_test", "host": "http://localhost:3000"},
        ),
        patch(
            "runlayer_cli.commands.scan.setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        patch("runlayer_cli.commands.scan.scan_all_clients", return_value=scan_result),
        patch("runlayer_cli.commands.scan.RunlayerClient", return_value=client),
        patch("runlayer_cli.aiwatch_checkin.submit_detect_checkin") as mock_detect,
        patch("runlayer_cli.aiwatch_checkin.submit_enforce_validation_checkin"),
        patch("runlayer_cli.aiwatch_checkin.submit_sessions_validation_checkin"),
        patch(
            "runlayer_cli.scan.service.submit_discovered_skills",
            return_value="success",
        ),
    ):
        result = runner.invoke(app, ["scan", "--no-projects"])

    assert result.exit_code == 0, result.output
    assert "Scan complete" in strip_ansi(result.output)
    mock_detect.assert_called_once_with(client, scan_result)


def test_scan_continues_when_enforce_validation_checkin_fails(tmp_path: Path):
    scan_result = _scan_result(servers=1, skills=1, plugins=1)
    client = SimpleNamespace(
        submit_mcp_watch_scan=Mock(
            return_value={
                "servers_processed": 1,
                "shadow_servers_found": 0,
                "managed_servers_matched": 0,
            }
        )
    )

    with (
        patch(
            "runlayer_cli.commands.scan.resolve_credentials",
            return_value={"secret": "rl_org_test", "host": "http://localhost:3000"},
        ),
        patch(
            "runlayer_cli.commands.scan.setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        patch("runlayer_cli.commands.scan.scan_all_clients", return_value=scan_result),
        patch("runlayer_cli.commands.scan.RunlayerClient", return_value=client),
        patch(
            "runlayer_cli.aiwatch_checkin.submit_enforce_validation_checkin",
            side_effect=RuntimeError("corrupt MDM plist"),
        ),
        patch("runlayer_cli.aiwatch_checkin.submit_sessions_validation_checkin"),
        patch(
            "runlayer_cli.scan.service.submit_discovered_skills",
            return_value="success",
        ) as mock_submit_skills,
        patch(
            "runlayer_cli.scan.service.submit_discovered_plugins",
            return_value="success",
        ) as mock_submit_plugins,
    ):
        result = runner.invoke(app, ["scan", "--no-projects"])

    assert result.exit_code == 0, result.output
    assert "Scan complete" in strip_ansi(result.output)
    client.submit_mcp_watch_scan.assert_called_once_with({"device_id": "device-1"})
    mock_submit_skills.assert_called_once_with(
        client,
        scan_result.skills,
        scan_result,
        artifact_cache=None,
    )
    mock_submit_plugins.assert_called_once_with(
        client,
        scan_result.plugins,
        scan_result,
        artifact_cache=None,
    )


def test_scan_continues_when_detect_checkin_fails(tmp_path: Path):
    # total_servers == 0 triggers the detect check-in fallback. If it raises an
    # exception not caught by its internal handler, the best-effort check-in must
    # not abort the scan or block skill/plugin submission (data loss).
    scan_result = _scan_result(servers=0, skills=1, plugins=1)
    client = SimpleNamespace()

    with (
        patch(
            "runlayer_cli.commands.scan.resolve_credentials",
            return_value={"secret": "rl_org_test", "host": "http://localhost:3000"},
        ),
        patch(
            "runlayer_cli.commands.scan.setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        patch("runlayer_cli.commands.scan.scan_all_clients", return_value=scan_result),
        patch("runlayer_cli.commands.scan.RunlayerClient", return_value=client),
        patch(
            "runlayer_cli.aiwatch_checkin.submit_detect_checkin",
            side_effect=RuntimeError("unexpected detect failure"),
        ),
        patch("runlayer_cli.aiwatch_checkin.submit_enforce_validation_checkin"),
        patch("runlayer_cli.aiwatch_checkin.submit_sessions_validation_checkin"),
        patch(
            "runlayer_cli.scan.service.submit_discovered_skills",
            return_value="success",
        ) as mock_submit_skills,
        patch(
            "runlayer_cli.scan.service.submit_discovered_plugins",
            return_value="success",
        ) as mock_submit_plugins,
    ):
        result = runner.invoke(app, ["scan", "--no-projects"])

    assert result.exit_code == 0, result.output
    assert "Scan complete" in strip_ansi(result.output)
    mock_submit_skills.assert_called_once_with(
        client,
        scan_result.skills,
        scan_result,
        artifact_cache=None,
    )
    mock_submit_plugins.assert_called_once_with(
        client,
        scan_result.plugins,
        scan_result,
        artifact_cache=None,
    )


def test_scan_all_users_rejects_dry_run(tmp_path: Path):
    """``--all-users --dry-run`` must be rejected, not run real child scans.

    The fan-out scans each profile in an isolated child whose output is never
    surfaced, so a forwarded --dry-run would read every profile yet print
    nothing. The combo must fail before the orchestrator runs (exit 2) so the
    flag never silently triggers real per-profile scans/submissions.
    """
    with (
        patch(
            "runlayer_cli.commands.scan.setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        patch("runlayer_cli.scan.windows_users.run_all_users_scan") as mock_run,
    ):
        result = runner.invoke(app, ["scan", "--all-users", "--dry-run"])

    assert result.exit_code == 2, result.output
    mock_run.assert_not_called()
    combined = strip_ansi(result.stdout + result.stderr)
    assert "--dry-run cannot be combined with --all-users" in combined


def test_scan_all_users_invokes_orchestrator(tmp_path: Path):
    """Without --dry-run, ``--all-users`` hands off to the fan-out orchestrator."""
    with (
        patch(
            "runlayer_cli.commands.scan.setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        patch(
            "runlayer_cli.scan.windows_users.run_all_users_scan",
            return_value=0,
        ) as mock_run,
    ):
        result = runner.invoke(app, ["scan", "--all-users"])

    assert result.exit_code == 0, result.output
    mock_run.assert_called_once_with(
        scan_projects=True,
        project_timeout=60,
        project_depth=7,
        cpu_cores=default_cpu_cores(),
        max_cpu_percent=DEFAULT_CPU_PERCENT,
        memory_limit_mb=DEFAULT_MEMORY_LIMIT_MB,
        artifact_lookup_cache=False,
    )


def test_scan_all_users_forwards_artifact_cache_setting(tmp_path: Path):
    with (
        patch(
            "runlayer_cli.commands.scan.setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        patch(
            "runlayer_cli.scan.windows_users.run_all_users_scan",
            return_value=0,
        ) as mock_run,
    ):
        result = runner.invoke(
            app,
            ["scan", "--all-users", "--artifact-lookup-cache"],
        )

    assert result.exit_code == 0, result.output
    assert mock_run.call_args.kwargs["artifact_lookup_cache"] is True


def test_scan_all_users_forwards_resource_caps(tmp_path: Path):
    """Resource-cap flags forward through the --all-users fan-out so each
    per-profile child self-governs with the operator's caps."""
    with (
        patch(
            "runlayer_cli.commands.scan.setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        patch(
            "runlayer_cli.scan.windows_users.run_all_users_scan",
            return_value=0,
        ) as mock_run,
    ):
        result = runner.invoke(
            app,
            [
                "scan",
                "--all-users",
                "--cpu-cores",
                "1",
                "--max-cpu-percent",
                "25",
                "--memory-limit-mb",
                "512",
            ],
        )

    assert result.exit_code == 0, result.output
    mock_run.assert_called_once_with(
        scan_projects=True,
        project_timeout=60,
        project_depth=7,
        cpu_cores=1,
        max_cpu_percent=25,
        memory_limit_mb=512,
        artifact_lookup_cache=False,
    )
