import re
from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
import pytest
import typer
from typer.testing import CliRunner

from runlayer_cli.api import PluginDetail
from runlayer_cli.config import Config
from runlayer_cli.main import app
from runlayer_cli.plugins.installer import PluginInstallResult, PluginLockEntry
from runlayer_cli.plugins.models import DiscoveredPlugin
from runlayer_cli.plugins.sync_engine import PluginSyncResult
from runlayer_cli.skills.sync_engine import SyncResult
from runlayer_cli.tls import async_http_client

runner = CliRunner()
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
PLUGIN_ID = "550e8400-e29b-41d4-a716-446655440000"


def _strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)


def _http_error(status_code: int) -> httpx.HTTPStatusError:
    request = httpx.Request("GET", "https://example.com/api/v1/plugins/plugin-id")
    response = httpx.Response(status_code, request=request)
    return httpx.HTTPStatusError(
        f"{status_code} error",
        request=request,
        response=response,
    )


def test_plugins_run_uses_plugin_proxy_endpoint_and_config_credentials(
    tmp_path: Path,
) -> None:
    config = Config(
        default_host="https://tenant.runlayer.com",
        hosts={
            "tenant.runlayer.com": {
                "url": "https://tenant.runlayer.com",
                "secret": "rl_config_secret",
            }
        },
    )
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch("runlayer_cli.commands.plugins.load_config", return_value=config),
        patch("runlayer_cli.commands.plugins.RunlayerClient") as client_class,
        patch(
            "runlayer_cli.commands.plugins.StreamableHttpTransport"
        ) as transport_class,
        patch("runlayer_cli.commands.plugins.ProxyClient"),
        patch("runlayer_cli.commands.plugins.FastMCPProxy"),
        patch("runlayer_cli.commands.plugins.anyio.run") as anyio_run,
    ):
        result = runner.invoke(
            app,
            ["plugins", "run", PLUGIN_ID],
            env={"RUNLAYER_HOST": None, "RUNLAYER_API_KEY": None},
        )

    assert result.exit_code == 0
    client_class.assert_called_once_with(
        hostname="https://tenant.runlayer.com", secret="rl_config_secret"
    )
    client_class.return_value.get_plugin.assert_called_once_with(PLUGIN_ID)
    transport_class.assert_called_once()
    assert transport_class.call_args.kwargs["url"] == (
        f"https://tenant.runlayer.com/api/v1/proxy/plugins/{PLUGIN_ID}/mcp"
    )
    assert transport_class.call_args.kwargs["headers"]["x-runlayer-api-key"] == (
        "rl_config_secret"
    )
    assert transport_class.call_args.kwargs["httpx_client_factory"] is async_http_client
    anyio_run.assert_called_once()


def test_plugins_run_uses_explicit_host_and_secret(tmp_path: Path) -> None:
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch("runlayer_cli.commands.plugins.load_config", return_value=Config()),
        patch("runlayer_cli.commands.plugins.RunlayerClient") as client_class,
        patch(
            "runlayer_cli.commands.plugins.StreamableHttpTransport"
        ) as transport_class,
        patch("runlayer_cli.commands.plugins.ProxyClient"),
        patch("runlayer_cli.commands.plugins.FastMCPProxy"),
        patch("runlayer_cli.commands.plugins.anyio.run"),
    ):
        result = runner.invoke(
            app,
            [
                "plugins",
                "run",
                PLUGIN_ID,
                "--host",
                "https://tenant.runlayer.com/",
                "--secret",
                "rl_direct_secret",
            ],
        )

    assert result.exit_code == 0
    client_class.assert_called_once_with(
        hostname="https://tenant.runlayer.com", secret="rl_direct_secret"
    )
    assert transport_class.call_args.kwargs["url"] == (
        f"https://tenant.runlayer.com/api/v1/proxy/plugins/{PLUGIN_ID}/mcp"
    )


def test_plugins_run_uses_env_host_and_secret(tmp_path: Path) -> None:
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch("runlayer_cli.commands.plugins.load_config", return_value=Config()),
        patch("runlayer_cli.commands.plugins.RunlayerClient") as client_class,
        patch(
            "runlayer_cli.commands.plugins.StreamableHttpTransport"
        ) as transport_class,
        patch("runlayer_cli.commands.plugins.ProxyClient"),
        patch("runlayer_cli.commands.plugins.FastMCPProxy"),
        patch("runlayer_cli.commands.plugins.anyio.run"),
    ):
        result = runner.invoke(
            app,
            ["plugins", "run", PLUGIN_ID],
            env={
                "RUNLAYER_HOST": "https://env-tenant.runlayer.com/",
                "RUNLAYER_API_KEY": "rl_env_secret",
            },
        )

    assert result.exit_code == 0
    client_class.assert_called_once_with(
        hostname="https://env-tenant.runlayer.com", secret="rl_env_secret"
    )
    assert transport_class.call_args.kwargs["url"] == (
        f"https://env-tenant.runlayer.com/api/v1/proxy/plugins/{PLUGIN_ID}/mcp"
    )


def test_plugins_run_missing_config_prints_setup_message(tmp_path: Path) -> None:
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch("runlayer_cli.commands.plugins.load_config", return_value=Config()),
        patch("runlayer_cli.commands.plugins.RunlayerClient") as client_class,
    ):
        result = runner.invoke(
            app,
            ["plugins", "run", PLUGIN_ID],
            env={"RUNLAYER_HOST": None, "RUNLAYER_API_KEY": None},
        )

    output = _strip_ansi(result.output)
    assert result.exit_code == 1
    assert "Runlayer is not configured." in output
    assert "uvx runlayer login --host https://YOUR-TENANT.runlayer.com" in output
    client_class.assert_not_called()


def test_plugins_run_missing_secret_prints_setup_message_for_host(
    tmp_path: Path,
) -> None:
    config = Config(
        default_host="https://tenant.runlayer.com",
        hosts={"tenant.runlayer.com": {"url": "https://tenant.runlayer.com"}},
    )
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch("runlayer_cli.commands.plugins.load_config", return_value=config),
        patch("runlayer_cli.commands.plugins.RunlayerClient") as client_class,
    ):
        result = runner.invoke(
            app,
            ["plugins", "run", PLUGIN_ID],
            env={"RUNLAYER_HOST": None, "RUNLAYER_API_KEY": None},
        )

    output = _strip_ansi(result.output)
    assert result.exit_code == 1
    assert "Runlayer is not configured." in output
    assert "uvx runlayer login --host https://tenant.runlayer.com" in output
    client_class.assert_not_called()


def test_plugins_run_invalid_id_prints_plugin_not_accessible(tmp_path: Path) -> None:
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch("runlayer_cli.commands.plugins.RunlayerClient") as client_class,
    ):
        result = runner.invoke(app, ["plugins", "run", "not-a-uuid"])

    output = _strip_ansi(result.output)
    assert result.exit_code == 1
    assert "Plugin MCP not found or not accessible: not-a-uuid" in output
    client_class.assert_not_called()


def test_plugins_run_auth_failure_prints_login_message(tmp_path: Path) -> None:
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch("runlayer_cli.commands.plugins.load_config", return_value=Config()),
        patch("runlayer_cli.commands.plugins.RunlayerClient") as client_class,
    ):
        client_class.return_value.get_plugin.side_effect = _http_error(401)
        result = runner.invoke(
            app,
            [
                "plugins",
                "run",
                PLUGIN_ID,
                "--host",
                "https://tenant.runlayer.com",
                "--secret",
                "bad_secret",
            ],
        )

    output = _strip_ansi(result.output)
    assert result.exit_code == 1
    assert "Runlayer authentication failed for https://tenant.runlayer.com. Run:" in (
        output
    )
    assert "uvx runlayer login --host https://tenant.runlayer.com" in output


@pytest.mark.parametrize("status_code", [403, 404, 422])
def test_plugins_run_inaccessible_plugin_prints_not_accessible(
    tmp_path: Path, status_code: int
) -> None:
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch("runlayer_cli.commands.plugins.load_config", return_value=Config()),
        patch("runlayer_cli.commands.plugins.RunlayerClient") as client_class,
    ):
        client_class.return_value.get_plugin.side_effect = _http_error(status_code)
        result = runner.invoke(
            app,
            [
                "plugins",
                "run",
                PLUGIN_ID,
                "--host",
                "https://tenant.runlayer.com",
                "--secret",
                "rl_direct_secret",
            ],
        )

    output = _strip_ansi(result.output)
    assert result.exit_code == 1
    assert f"Plugin MCP not found or not accessible: {PLUGIN_ID}" in output


def test_plugins_push_outputs_summary_and_done(tmp_path: Path) -> None:
    discovered = [
        DiscoveredPlugin(
            root=tmp_path, path="review-suite", name="review-suite", skills=[]
        ),
    ]
    sync_mock = AsyncMock(
        return_value=PluginSyncResult(
            discovered_plugins=1,
            discovered_skills=2,
            created=1,
            warnings=["review-suite: warning"],
        )
    )
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.plugins.RunlayerClient"),
        patch(
            "runlayer_cli.commands.plugins.discover_plugins", return_value=discovered
        ),
        patch("runlayer_cli.commands.plugins.sync_discovered_plugins", new=sync_mock),
    ):
        result = runner.invoke(
            app,
            ["plugins", "push", str(tmp_path), "--namespace", "myorg/repo"],
        )

    assert result.exit_code == 0
    assert "Found 1 plugins, 0 skills" in result.output
    assert "1 plugins created" in result.output


def test_plugins_find_installs_selected_plugins_for_multiple_clients(
    tmp_path: Path,
) -> None:
    install_mock = AsyncMock(
        return_value=PluginInstallResult(installed=["review-suite"])
    )
    selected_plugin = PluginDetail(
        id="plugin-1",
        name="review-suite",
        namespace="Org/Repo",
        description="Review plugin",
    )
    selected_plugin_two = PluginDetail(
        id="plugin-2",
        name="deploy-suite",
        namespace="Org/Repo",
        description="Deploy plugin",
    )

    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_plugin_dirs",
            return_value=(
                tmp_path / "canonical",
                tmp_path / "editor",
                tmp_path / "lock.yml",
            ),
        ) as resolve_dirs_mock,
        patch("runlayer_cli.commands.plugins.RunlayerClient") as client_class,
        patch(
            "runlayer_cli.commands.plugins.install_plugins",
            new=install_mock,
        ),
        patch(
            "runlayer_cli.commands.plugins.prompt_items",
            return_value=[selected_plugin, selected_plugin_two],
        ),
        patch(
            "runlayer_cli.commands.plugins.prompt_clients",
            return_value=["codex", "cursor"],
        ),
        patch(
            "runlayer_cli.commands.plugins.prompt_scope",
            return_value="global",
        ),
        patch("runlayer_cli.commands.plugins.confirm_install"),
        patch("runlayer_cli.commands.plugins.console.status") as status_mock,
    ):
        client_class.return_value.list_plugins_detailed.return_value = [
            selected_plugin,
            selected_plugin_two,
        ]
        result = runner.invoke(app, ["plugins", "find"])

    assert result.exit_code == 0
    status_mock.assert_called_once_with("Loading plugins...")
    client_class.return_value.list_plugins_detailed.assert_called_once_with(
        filter="all"
    )
    assert resolve_dirs_mock.call_count == 2
    assert resolve_dirs_mock.call_args_list[0].args[0] == "codex"
    assert resolve_dirs_mock.call_args_list[1].args[0] == "cursor"
    assert all(call.args[1] is True for call in resolve_dirs_mock.call_args_list)
    assert install_mock.await_count == 4
    calls = install_mock.await_args_list
    assert calls[0].kwargs["source"] == "plugin-1"
    assert calls[1].kwargs["source"] == "plugin-2"
    assert calls[2].kwargs["source"] == "plugin-1"
    assert calls[3].kwargs["source"] == "plugin-2"
    assert calls[0].kwargs["client_name"] == "codex"
    assert calls[2].kwargs["client_name"] == "cursor"
    assert all(call.kwargs["install_scope"] == "global" for call in calls)


def test_plugins_find_handles_empty_catalog(tmp_path: Path) -> None:
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.plugins.RunlayerClient") as client_class,
    ):
        client_class.return_value.list_plugins_detailed.return_value = []
        result = runner.invoke(app, ["plugins", "find"])

    assert result.exit_code == 0
    assert "No plugins available." in result.output


def test_plugins_find_cancelled_before_install(tmp_path: Path) -> None:
    install_mock = AsyncMock(
        return_value=PluginInstallResult(installed=["review-suite"])
    )
    selected_plugin = PluginDetail(
        id="plugin-1",
        name="review-suite",
        namespace="Org/Repo",
        description="Review plugin",
    )

    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.plugins.RunlayerClient") as client_class,
        patch(
            "runlayer_cli.commands.plugins.install_plugins",
            new=install_mock,
        ),
        patch(
            "runlayer_cli.commands.plugins.prompt_items",
            return_value=[selected_plugin],
        ),
        patch(
            "runlayer_cli.commands.plugins.prompt_clients",
            return_value=["claude_code"],
        ),
        patch(
            "runlayer_cli.commands.plugins.prompt_scope",
            return_value="project",
        ),
        patch(
            "runlayer_cli.commands.plugins.confirm_install",
            side_effect=typer.Exit(0),
        ),
    ):
        client_class.return_value.list_plugins_detailed.return_value = [selected_plugin]
        result = runner.invoke(app, ["plugins", "find"])

    assert result.exit_code == 0
    install_mock.assert_not_awaited()


def test_plugins_push_prints_pushing_header_before_progress(tmp_path: Path) -> None:
    discovered = [
        DiscoveredPlugin(
            root=tmp_path, path="review-suite", name="review-suite", skills=[]
        ),
    ]

    async def _sync(*args, **kwargs) -> PluginSyncResult:
        kwargs["on_skill_progress"]("review-suite/code-review", "created")
        kwargs["on_plugin_progress"]("review-suite", "created")
        return PluginSyncResult(created=1)

    sync_mock = AsyncMock(side_effect=_sync)
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.plugins.RunlayerClient"),
        patch(
            "runlayer_cli.commands.plugins.discover_plugins", return_value=discovered
        ),
        patch("runlayer_cli.commands.plugins.sync_discovered_plugins", new=sync_mock),
    ):
        result = runner.invoke(
            app,
            ["plugins", "push", str(tmp_path), "--namespace", "myorg/repo"],
        )

    assert result.exit_code == 0
    pushing_header = result.output.index("Pushing...")
    skill_progress = result.output.index("  review-suite/code-review: created")
    plugin_progress = result.output.index("  review-suite: created")
    assert pushing_header < skill_progress < plugin_progress


def test_plugins_push_prints_pushing_header_once(tmp_path: Path) -> None:
    discovered = [
        DiscoveredPlugin(
            root=tmp_path, path="review-suite", name="review-suite", skills=[]
        ),
    ]

    async def _sync(*args, **kwargs) -> PluginSyncResult:
        kwargs["on_skill_progress"]("review-suite/code-review", "created")
        kwargs["on_plugin_progress"]("review-suite", "updated")
        kwargs["on_plugin_progress"]("ops-suite", "created")
        return PluginSyncResult(created=1, updated=1)

    sync_mock = AsyncMock(side_effect=_sync)
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.plugins.RunlayerClient"),
        patch(
            "runlayer_cli.commands.plugins.discover_plugins", return_value=discovered
        ),
        patch("runlayer_cli.commands.plugins.sync_discovered_plugins", new=sync_mock),
    ):
        result = runner.invoke(
            app,
            ["plugins", "push", str(tmp_path), "--namespace", "myorg/repo"],
        )

    assert result.exit_code == 0
    assert result.output.count("Pushing...") == 1


def test_plugins_push_dry_run_requires_auth_up_front(tmp_path: Path) -> None:
    discovered = [
        DiscoveredPlugin(
            root=tmp_path, path="review-suite", name="review-suite", skills=[]
        ),
    ]
    sync_mock = AsyncMock(return_value=PluginSyncResult())
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch("runlayer_cli.commands.plugins.resolve_credentials") as resolve_mock,
        patch("runlayer_cli.commands.plugins.RunlayerClient"),
        patch(
            "runlayer_cli.commands.plugins.discover_plugins", return_value=discovered
        ),
        patch("runlayer_cli.commands.plugins.sync_discovered_plugins", new=sync_mock),
    ):
        resolve_mock.return_value = {"host": "https://example.com", "secret": "rl_test"}
        result = runner.invoke(
            app,
            [
                "plugins",
                "push",
                str(tmp_path),
                "--namespace",
                "myorg/repo",
                "--dry-run",
            ],
        )

    assert result.exit_code == 0
    assert resolve_mock.call_args.kwargs["require_auth"] is True


def test_plugins_push_discovers_once_and_passes_plugins_to_sync(tmp_path: Path) -> None:
    discovered = [
        DiscoveredPlugin(
            root=tmp_path, path="review-suite", name="review-suite", skills=[]
        ),
    ]
    sync_mock = AsyncMock(return_value=PluginSyncResult())
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.plugins.RunlayerClient"),
        patch(
            "runlayer_cli.commands.plugins.discover_plugins", return_value=discovered
        ) as discover_mock,
        patch("runlayer_cli.commands.plugins.sync_discovered_plugins", new=sync_mock),
    ):
        result = runner.invoke(
            app,
            ["plugins", "push", str(tmp_path), "--namespace", "myorg/repo"],
        )

    assert result.exit_code == 0
    discover_mock.assert_called_once_with(tmp_path.resolve())
    assert sync_mock.await_args.args[0] == discovered


def test_plugins_push_prints_mcp_skip_warning(tmp_path: Path) -> None:
    discovered = [
        DiscoveredPlugin(
            root=tmp_path,
            path="review-suite",
            name="review-suite",
            skills=[],
        ),
    ]
    sync_mock = AsyncMock(
        return_value=PluginSyncResult(
            warnings=[
                "review-suite: skipped MCP server external-http with non-Runlayer URL https://example.com/mcp"
            ]
        )
    )
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.plugins.RunlayerClient"),
        patch(
            "runlayer_cli.commands.plugins.discover_plugins", return_value=discovered
        ),
        patch("runlayer_cli.commands.plugins.sync_discovered_plugins", new=sync_mock),
    ):
        result = runner.invoke(
            app,
            ["plugins", "push", str(tmp_path), "--namespace", "myorg/repo"],
        )

    assert result.exit_code == 0
    assert (
        "Warning: review-suite: skipped MCP server external-http with non-Runlayer URL https://example.com/mcp"
        in result.output
    )


def test_plugins_push_prints_manifest_warning_without_structlog_noise(
    tmp_path: Path,
) -> None:
    discovered = [
        DiscoveredPlugin(
            root=tmp_path,
            path="review-suite",
            name="review-suite",
            skills=[],
            manifest_warnings=[
                "review-suite: truncated plugin description to 1024 characters"
            ],
        ),
    ]
    sync_mock = AsyncMock(
        return_value=PluginSyncResult(
            warnings=["review-suite: truncated plugin description to 1024 characters"]
        )
    )
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.plugins.RunlayerClient"),
        patch(
            "runlayer_cli.commands.plugins.discover_plugins", return_value=discovered
        ),
        patch("runlayer_cli.commands.plugins.sync_discovered_plugins", new=sync_mock),
    ):
        result = runner.invoke(
            app,
            ["plugins", "push", str(tmp_path), "--namespace", "myorg/repo"],
        )

    assert result.exit_code == 0
    assert (
        "Warning: review-suite: truncated plugin description to 1024 characters"
        in result.output
    )
    assert "[warning" not in result.output


def test_plugins_push_suppresses_unchanged_lines(tmp_path: Path) -> None:
    """Unchanged items should not appear in output."""
    discovered = [
        DiscoveredPlugin(
            root=tmp_path, path="review-suite", name="review-suite", skills=[]
        ),
    ]

    async def _sync(*args, **kwargs) -> PluginSyncResult:
        kwargs["on_skill_progress"]("review-suite/code-review", "unchanged")
        kwargs["on_skill_progress"]("review-suite/design-review", "updated")
        kwargs["on_plugin_progress"]("review-suite", "unchanged")
        return PluginSyncResult(
            unchanged=1,
            skill_result=SyncResult(updated=1, unchanged=1),
        )

    sync_mock = AsyncMock(side_effect=_sync)
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.plugins.RunlayerClient"),
        patch(
            "runlayer_cli.commands.plugins.discover_plugins", return_value=discovered
        ),
        patch("runlayer_cli.commands.plugins.sync_discovered_plugins", new=sync_mock),
    ):
        result = runner.invoke(
            app,
            ["plugins", "push", str(tmp_path), "--namespace", "myorg/repo"],
        )

    assert result.exit_code == 0
    assert "unchanged" not in result.output.split("Done")[0]
    assert "design-review: updated" in result.output
    assert "1 skills updated" in result.output
    assert "(2 unchanged)" in result.output


def test_plugins_push_everything_up_to_date(tmp_path: Path) -> None:
    discovered = [
        DiscoveredPlugin(
            root=tmp_path, path="review-suite", name="review-suite", skills=[]
        ),
    ]
    sync_mock = AsyncMock(
        return_value=PluginSyncResult(
            unchanged=1,
            skill_result=SyncResult(unchanged=3),
        )
    )
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.plugins.RunlayerClient"),
        patch(
            "runlayer_cli.commands.plugins.discover_plugins", return_value=discovered
        ),
        patch("runlayer_cli.commands.plugins.sync_discovered_plugins", new=sync_mock),
    ):
        result = runner.invoke(
            app,
            ["plugins", "push", str(tmp_path), "--namespace", "myorg/repo"],
        )

    assert result.exit_code == 0
    assert "everything up to date" in result.output


def test_plugins_push_reports_handled_sync_errors_without_traceback(
    tmp_path: Path,
) -> None:
    discovered = [
        DiscoveredPlugin(
            root=tmp_path, path="review-suite", name="review-suite", skills=[]
        ),
    ]
    sync_mock = AsyncMock(
        return_value=PluginSyncResult(
            errors=[
                "review-suite: failed to resolve tools for connector "
                "12345678-1234-1234-1234-123456789abc; plugin not synced"
            ]
        )
    )
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.plugins.RunlayerClient"),
        patch(
            "runlayer_cli.commands.plugins.discover_plugins", return_value=discovered
        ),
        patch("runlayer_cli.commands.plugins.sync_discovered_plugins", new=sync_mock),
    ):
        result = runner.invoke(
            app,
            ["plugins", "push", str(tmp_path), "--namespace", "myorg/repo"],
        )

    assert result.exit_code == 1
    assert (
        "Error: review-suite: failed to resolve tools for connector "
        "12345678-1234-1234-1234-123456789abc; plugin not synced"
        in _strip_ansi(result.output)
    )
    assert "Traceback" not in result.output


# -- Plugin add/list/remove/update command tests --


def _entry(name: str, *, client: str = "claude_code") -> PluginLockEntry:
    return PluginLockEntry(name=name, id=f"id-{name}", client=client)


def _resolve_dirs(tmp_path: Path) -> tuple[Path, Path, Path]:
    return (
        tmp_path / "canonical",
        tmp_path / "editor",
        tmp_path / "lock.yml",
    )


def test_add_all_works_without_source(tmp_path: Path):
    install_mock = AsyncMock(return_value=PluginInstallResult(installed=["a"]))
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_plugin_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch("runlayer_cli.commands.plugins.RunlayerClient"),
        patch(
            "runlayer_cli.commands.plugins.install_plugins",
            new=install_mock,
        ),
    ):
        result = runner.invoke(
            app,
            ["plugins", "add", "--all"],
        )

    assert result.exit_code == 0
    install_mock.assert_awaited_once()
    kwargs = install_mock.await_args_list[0].kwargs
    assert kwargs["install_all"] is True
    assert kwargs["source"] is None
    assert "project scope" in result.output
    assert "claude_code" in result.output
    assert "runlayer plugins list" not in result.output


def test_add_global_mentions_global_list_hint(tmp_path: Path):
    install_mock = AsyncMock(return_value=PluginInstallResult(installed=["a"]))
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_plugin_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch("runlayer_cli.commands.plugins.RunlayerClient"),
        patch(
            "runlayer_cli.commands.plugins.install_plugins",
            new=install_mock,
        ),
    ):
        result = runner.invoke(
            app,
            ["plugins", "add", "--all", "--global", "--client", "cursor"],
        )

    assert result.exit_code == 0
    assert "global scope" in result.output
    assert "cursor" in result.output
    assert "runlayer plugins list --global" not in result.output


@pytest.mark.parametrize(
    ("args", "expected_message"),
    [
        (["plugins", "add", "org/repo", "--all"], "either SOURCE or --all"),
        (["plugins", "add"], "Use SOURCE or --all"),
    ],
)
def test_add_arg_validation(args: list[str], expected_message: str):
    result = runner.invoke(app, args)
    assert result.exit_code == 1
    assert expected_message in result.output


def test_remove_all_prompts_and_aborts_on_no(tmp_path: Path):
    uninstall_mock = AsyncMock()
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_plugin_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch(
            "runlayer_cli.commands.plugins.read_plugin_lockfile",
            return_value=[_entry("a"), _entry("b")],
        ),
        patch("runlayer_cli.commands.plugins.typer.confirm", return_value=False),
        patch(
            "runlayer_cli.commands.plugins.uninstall_plugin",
            new=uninstall_mock,
        ),
    ):
        result = runner.invoke(app, ["plugins", "remove", "--all"])

    assert result.exit_code == 0
    assert "Aborted." in result.output
    uninstall_mock.assert_not_called()


def test_remove_all_yes_removes_without_prompt(tmp_path: Path):
    uninstall_mock = AsyncMock()
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_plugin_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch(
            "runlayer_cli.commands.plugins.read_plugin_lockfile",
            return_value=[_entry("a"), _entry("b")],
        ),
        patch("runlayer_cli.commands.plugins.typer.confirm") as confirm_mock,
        patch(
            "runlayer_cli.commands.plugins.uninstall_plugin",
            new=uninstall_mock,
        ),
    ):
        result = runner.invoke(app, ["plugins", "remove", "--all", "--yes"])

    assert result.exit_code == 0
    assert "Done: 2 removed" in result.output
    confirm_mock.assert_not_called()
    assert uninstall_mock.await_count == 2


def test_remove_prints_resolved_plugin_name(tmp_path: Path):
    uninstall_mock = AsyncMock(return_value="OneLayer")
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_plugin_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch(
            "runlayer_cli.commands.plugins.uninstall_plugin",
            new=uninstall_mock,
        ),
    ):
        result = runner.invoke(app, ["plugins", "remove", "p1"])

    assert result.exit_code == 0
    assert "Removed: OneLayer" in result.output


@pytest.mark.parametrize(
    ("args", "expected_message"),
    [
        (["plugins", "remove", "my-plugin", "--all"], "either PLUGIN_REF or --all"),
        (["plugins", "remove"], "Use PLUGIN_REF or --all"),
    ],
)
def test_remove_arg_validation(args: list[str], expected_message: str):
    result = runner.invoke(app, args)
    assert result.exit_code == 1
    assert expected_message in result.output


def test_list_shows_installed_plugins(tmp_path: Path):
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_plugin_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch(
            "runlayer_cli.commands.plugins.read_plugin_lockfile",
            return_value=[
                PluginLockEntry(
                    name="my-plugin",
                    id="p1",
                    namespace="org/repo",
                    client="claude_code",
                    install_mode="native",
                )
            ],
        ),
    ):
        result = runner.invoke(app, ["plugins", "list"])

    assert result.exit_code == 0
    assert "my-plugin" in result.output
    assert "org/repo" in result.output
    assert "claude_code" in result.output
    assert "1 plugin(s) installed" in result.output


def test_list_merges_clients_for_same_plugin(tmp_path: Path):
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_plugin_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch(
            "runlayer_cli.commands.plugins.read_plugin_lockfile",
            return_value=[
                PluginLockEntry(
                    name="my-plugin",
                    id="p1",
                    namespace="org/repo",
                    client="claude_code",
                    install_mode="native",
                ),
                PluginLockEntry(
                    name="my-plugin",
                    id="p1",
                    namespace="org/repo",
                    client="cursor",
                    install_mode="native",
                ),
            ],
        ),
    ):
        result = runner.invoke(app, ["plugins", "list"])

    assert result.exit_code == 0
    assert result.output.count("my-plugin") == 1
    assert "claude_code" in result.output
    assert "cursor" in result.output
    assert "1 plugin(s) installed" in result.output


def test_list_keeps_distinct_rows_for_same_name_with_different_ids(tmp_path: Path):
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_plugin_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch(
            "runlayer_cli.commands.plugins.read_plugin_lockfile",
            return_value=[
                PluginLockEntry(
                    name="my-plugin",
                    id="p1",
                    namespace="org/repo",
                    client="claude_code",
                    install_mode="native",
                ),
                PluginLockEntry(
                    name="my-plugin",
                    id="p2",
                    namespace="org/other",
                    client="cursor",
                    install_mode="native",
                ),
            ],
        ),
    ):
        result = runner.invoke(app, ["plugins", "list"])

    assert result.exit_code == 0
    assert result.output.count("my-plugin") == 2
    assert "org/repo" in result.output
    assert "org/other" in result.output
    assert "2 plugin(s) installed" in result.output


def test_list_filters_by_client(tmp_path: Path):
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_plugin_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch(
            "runlayer_cli.commands.plugins.read_plugin_lockfile",
            return_value=[
                PluginLockEntry(
                    name="claude-plugin",
                    id="p1",
                    client="claude_code",
                    install_mode="native",
                ),
                PluginLockEntry(
                    name="cursor-plugin",
                    id="p2",
                    client="cursor",
                    install_mode="native",
                ),
            ],
        ),
    ):
        result = runner.invoke(app, ["plugins", "list", "--client", "cursor"])

    assert result.exit_code == 0
    assert "cursor-plugin" in result.output
    assert "claude-plugin" not in result.output
    assert "cursor" in result.output
    assert "1 plugin(s) installed" in result.output


def test_list_no_plugins_in_project_scope(tmp_path: Path):
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_plugin_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch(
            "runlayer_cli.commands.plugins.read_plugin_lockfile",
            return_value=[],
        ),
    ):
        result = runner.invoke(app, ["plugins", "list"])

    assert result.exit_code == 0
    assert "No plugins installed in project scope." in result.output


def test_list_global_reads_global_scope_only(tmp_path: Path):
    project_dirs = (
        tmp_path / "project-canonical",
        tmp_path / "project-editor",
        tmp_path / "project-lock.yml",
    )
    global_dirs = (
        tmp_path / "global-canonical",
        tmp_path / "global-editor",
        tmp_path / "global-lock.yml",
    )

    def _resolve(
        client_name: str, global_install: bool, cwd: Path
    ) -> tuple[Path, Path, Path]:
        assert client_name == "claude_code"
        assert cwd == Path.cwd()
        return global_dirs if global_install else project_dirs

    def _read(lockfile: Path) -> list[PluginLockEntry]:
        if lockfile == project_dirs[2]:
            return [
                PluginLockEntry(
                    name="project-plugin",
                    id="project-id",
                    client="claude_code",
                    install_mode="native",
                )
            ]
        if lockfile == global_dirs[2]:
            return [
                PluginLockEntry(
                    name="global-plugin",
                    id="global-id",
                    client="cursor",
                    install_mode="native",
                )
            ]
        return []

    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_plugin_dirs",
            side_effect=_resolve,
        ),
        patch(
            "runlayer_cli.commands.plugins.read_plugin_lockfile",
            side_effect=_read,
        ),
    ):
        result = runner.invoke(app, ["plugins", "list", "--global"])

    assert result.exit_code == 0
    assert "global-plugin" in result.output
    assert "project-plugin" not in result.output
    assert "cursor" in result.output


def test_list_help_describes_scope_and_client_behavior():
    result = runner.invoke(app, ["plugins", "list", "--help"])
    help_text = " ".join(_strip_ansi(result.output).split())

    assert result.exit_code == 0
    assert "List installed plugins in the selected scope." in help_text
    assert "By default, lists project plugins for all clients." in help_text
    assert "Use --global to list global plugins instead." in help_text
    assert "Use --client to filter to one client." in help_text


def test_remove_all_filters_by_client(tmp_path: Path):
    entries = [
        PluginLockEntry(name="a", id="id-a", client="claude_code"),
        PluginLockEntry(
            name="b", id="id-b", client="cursor", install_mode="mcp_fallback"
        ),
    ]
    uninstall_mock = AsyncMock()
    with (
        patch(
            "runlayer_cli.commands.plugins.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.plugins.resolve_plugin_dirs",
            return_value=_resolve_dirs(tmp_path),
        ),
        patch(
            "runlayer_cli.commands.plugins.read_plugin_lockfile",
            return_value=entries,
        ),
        patch(
            "runlayer_cli.commands.plugins.uninstall_plugin",
            new=uninstall_mock,
        ),
    ):
        result = runner.invoke(
            app,
            ["plugins", "remove", "--all", "--yes", "--client", "cursor"],
        )

    assert result.exit_code == 0
    assert "Done: 1 removed" in result.output
    uninstall_mock.assert_awaited_once()
    args = uninstall_mock.await_args_list[0].args
    assert args[0] == "b"
    assert args[-1] == "cursor"
