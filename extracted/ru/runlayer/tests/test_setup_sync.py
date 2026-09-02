from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest
import typer

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10
    import tomli as tomllib

from runlayer_cli.api import PluginDetail, PluginListFilter, ServerListItem
from runlayer_cli.commands import setup


class _FakeApiClient:
    def __init__(self, plugins: list[PluginDetail] | None = None) -> None:
        self.scopes: list[str] = []
        self.plugin_filters: list[str] = []
        self.plugins = (
            plugins
            if plugins is not None
            else [
                PluginDetail(
                    id="plugin-auto-sync",
                    name="OneLayer",
                    use_dynamic_tools=True,
                )
            ]
        )

    def list_servers(self, scope: str, limit: int = 100) -> list[ServerListItem]:
        self.scopes.append(scope)
        assert limit == 100
        return [
            ServerListItem(
                id="srv-auto-sync",
                name="Auto Sync Server",
                status="active",
                deployment_mode="hosted",
            )
        ]

    def list_plugins_detailed(self, *, filter: PluginListFilter) -> list[PluginDetail]:
        self.plugin_filters.append(filter)
        return self.plugins

    def list_auto_sync(self, entity_type: str) -> None:
        raise AssertionError("setup sync must not read the admin auto-sync endpoint")

    def get_plugin(self, plugin_id: str) -> None:
        raise AssertionError("setup sync must not fetch plugins one at a time")


def _sync_with_fake_api(
    monkeypatch: pytest.MonkeyPatch,
    fake_api: _FakeApiClient,
    *,
    client: setup.InstallClient | None,
) -> None:
    monkeypatch.setattr(
        setup, "set_credentials_in_context", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        setup,
        "resolve_credentials",
        lambda *args, **kwargs: {"secret": "secret", "host": "https://example.com"},
    )
    monkeypatch.setattr(setup, "RunlayerClient", lambda *args, **kwargs: fake_api)
    setup.sync(
        ctx=cast(Any, object()),
        client=client,
        header=None,
        secret=None,
        host=None,
        yes=True,
    )


def _record_installs(
    installed: list[tuple[setup.InstallClient, list[setup.InstallServerSpec]]],
):
    def install(
        client: setup.InstallClient, specs: list[setup.InstallServerSpec]
    ) -> int:
        installed.append((client, specs))
        return len(specs)

    return install


def test_setup_sync_fetches_auto_synced_servers_and_plugins(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_api = _FakeApiClient()
    installed: list[tuple[setup.InstallClient, list[setup.InstallServerSpec]]] = []

    monkeypatch.setattr(
        setup, "set_credentials_in_context", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        setup,
        "resolve_credentials",
        lambda *args, **kwargs: {"secret": "secret", "host": "https://example.com"},
    )
    monkeypatch.setattr(setup, "RunlayerClient", lambda *args, **kwargs: fake_api)
    monkeypatch.setattr(
        setup,
        "_install_servers_to_client",
        _record_installs(installed),
    )

    setup.sync(
        ctx=cast(Any, object()),
        client=setup.InstallClient.CURSOR,
        header=None,
        secret=None,
        host=None,
        yes=True,
    )

    assert fake_api.scopes == ["accessible_and_auto_sync"]
    assert fake_api.plugin_filters == ["accessible_and_auto_sync"]
    assert len(installed) == 1
    assert installed[0][0] == setup.InstallClient.CURSOR
    assert [spec.server_id for spec in installed[0][1]] == [
        "srv-auto-sync",
        "plugin-auto-sync",
    ]
    assert installed[0][1][1].proxy_url == (
        "https://example.com/api/v1/proxy/plugins/plugin-auto-sync/mcp"
    )
    assert installed[0][1][0].is_dynamic_plugin is False
    assert installed[0][1][1].is_dynamic_plugin is True


def test_setup_sync_codex_omits_deferred_for_dynamic_plugin(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_api = _FakeApiClient()
    config_path = tmp_path / ".codex" / "config.toml"
    monkeypatch.setattr(
        setup,
        "_get_install_client_config_paths",
        lambda _: [config_path],
    )
    _sync_with_fake_api(monkeypatch, fake_api, client=setup.InstallClient.CODEX)

    with config_path.open("rb") as config_file:
        config = tomllib.load(config_file)
    assert config["mcp_servers"] == {
        "auto-sync-server": {
            "url": "https://example.com/api/v1/proxy/srv-auto-sync/mcp"
        },
        "onelayer": {
            "url": "https://example.com/api/v1/proxy/plugins/plugin-auto-sync/mcp",
            "omit_tools_from": ["deferred"],
        },
    }


def test_setup_sync_codex_leaves_non_dynamic_plugin_deferred(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_api = _FakeApiClient(
        plugins=[
            PluginDetail(
                id="plugin-static",
                name="Static Plugin",
                use_dynamic_tools=False,
            )
        ]
    )
    config_path = tmp_path / ".codex" / "config.toml"
    monkeypatch.setattr(
        setup,
        "_get_install_client_config_paths",
        lambda _: [config_path],
    )
    _sync_with_fake_api(monkeypatch, fake_api, client=setup.InstallClient.CODEX)

    with config_path.open("rb") as config_file:
        config = tomllib.load(config_file)
    assert config["mcp_servers"]["static-plugin"] == {
        "url": "https://example.com/api/v1/proxy/plugins/plugin-static/mcp"
    }


def test_setup_sync_invalid_codex_config_exits_nonzero(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fake_api = _FakeApiClient()
    config_path = tmp_path / ".codex" / "config.toml"
    monkeypatch.setattr(
        setup,
        "_get_install_client_config_paths",
        lambda _: [config_path],
    )
    config_path.parent.mkdir()
    invalid_config = '[mcp_servers."broken"\nurl = "https://example.com"\n'
    config_path.write_text(invalid_config)

    with pytest.raises(typer.Exit) as exc_info:
        _sync_with_fake_api(monkeypatch, fake_api, client=setup.InstallClient.CODEX)

    output = capsys.readouterr().out
    assert exc_info.value.exit_code == 1
    assert f"Cannot read {config_path}" in output
    assert "Sync failed for: codex" in output
    assert config_path.read_text() == invalid_config
    assert list(config_path.parent.glob("config.backup_*")) == []


def test_setup_sync_continues_after_a_client_install_fails(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fake_api = _FakeApiClient()
    attempted: list[setup.InstallClient] = []
    monkeypatch.setattr(
        setup,
        "_detect_installed_clients",
        lambda: [setup.InstallClient.OPENCODE, setup.InstallClient.CURSOR],
    )

    def install(
        client: setup.InstallClient, specs: list[setup.InstallServerSpec]
    ) -> int:
        attempted.append(client)
        if client == setup.InstallClient.OPENCODE:
            raise setup.InstallError("config unusable")
        return len(specs)

    monkeypatch.setattr(setup, "_install_servers_to_client", install)

    with pytest.raises(typer.Exit) as exc_info:
        _sync_with_fake_api(monkeypatch, fake_api, client=None)

    assert exc_info.value.exit_code == 1
    assert attempted == [setup.InstallClient.OPENCODE, setup.InstallClient.CURSOR]
    assert "Sync failed for: opencode" in capsys.readouterr().out


def test_setup_sync_continues_after_a_client_filesystem_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fake_api = _FakeApiClient()
    attempted: list[setup.InstallClient] = []
    monkeypatch.setattr(
        setup,
        "_detect_installed_clients",
        lambda: [setup.InstallClient.OPENCODE, setup.InstallClient.CURSOR],
    )

    def install(
        client: setup.InstallClient, specs: list[setup.InstallServerSpec]
    ) -> int:
        attempted.append(client)
        if client == setup.InstallClient.OPENCODE:
            raise PermissionError("read-only config")
        return len(specs)

    monkeypatch.setattr(setup, "_install_servers_to_client", install)

    with pytest.raises(typer.Exit) as exc_info:
        _sync_with_fake_api(monkeypatch, fake_api, client=None)

    output = capsys.readouterr().out
    assert exc_info.value.exit_code == 1
    assert attempted == [setup.InstallClient.OPENCODE, setup.InstallClient.CURSOR]
    assert "read-only config" in output
    assert "Sync failed for: opencode" in output


def test_setup_sync_continues_after_a_client_has_non_mapping_server_section(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fake_api = _FakeApiClient()
    claude_config = tmp_path / ".claude.json"
    cursor_config = tmp_path / "mcp.json"
    claude_config.write_text('{"mcpServers": []}')
    config_paths = {
        setup.InstallClient.CLAUDE_CODE: claude_config,
        setup.InstallClient.CURSOR: cursor_config,
    }
    monkeypatch.setattr(
        setup,
        "_detect_installed_clients",
        lambda: [setup.InstallClient.CLAUDE_CODE, setup.InstallClient.CURSOR],
    )
    monkeypatch.setattr(
        setup,
        "_get_install_client_config_path",
        config_paths.__getitem__,
    )

    with pytest.raises(typer.Exit) as exc_info:
        _sync_with_fake_api(monkeypatch, fake_api, client=None)

    output = capsys.readouterr().out
    assert exc_info.value.exit_code == 1
    assert "'mcpServers' must be an object or table" in output
    assert "Sync failed for: claude_code" in output
    assert json.loads(cursor_config.read_text())["mcpServers"]["auto-sync-server"] == {
        "url": "https://example.com/api/v1/proxy/srv-auto-sync/mcp",
    }


def test_setup_sync_skips_auto_synced_plugins_for_local_only_clients(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_api = _FakeApiClient()
    installed: list[tuple[setup.InstallClient, list[setup.InstallServerSpec]]] = []

    monkeypatch.setattr(
        setup, "set_credentials_in_context", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        setup,
        "resolve_credentials",
        lambda *args, **kwargs: {"secret": "secret", "host": "https://example.com"},
    )
    monkeypatch.setattr(setup, "RunlayerClient", lambda *args, **kwargs: fake_api)
    monkeypatch.setattr(
        setup,
        "_install_servers_to_client",
        _record_installs(installed),
    )

    setup.sync(
        ctx=cast(Any, object()),
        client=setup.InstallClient.CLAUDE_DESKTOP,
        header=None,
        secret=None,
        host=None,
        yes=True,
    )

    assert installed == []


def test_setup_sync_auto_detects_opencode_from_config_dir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_api = _FakeApiClient()
    installed: list[tuple[setup.InstallClient, list[setup.InstallServerSpec]]] = []
    opencode_dir = tmp_path / ".config" / "opencode"
    opencode_dir.mkdir(parents=True)

    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(
        setup, "set_credentials_in_context", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        setup,
        "resolve_credentials",
        lambda *args, **kwargs: {"secret": "secret", "host": "https://example.com"},
    )
    monkeypatch.setattr(setup, "RunlayerClient", lambda *args, **kwargs: fake_api)
    monkeypatch.setattr(
        setup,
        "_install_servers_to_client",
        _record_installs(installed),
    )

    setup.sync(
        ctx=cast(Any, object()),
        client=None,
        header=None,
        secret=None,
        host=None,
        yes=True,
    )

    assert len(installed) == 1
    assert installed[0][0] == setup.InstallClient.OPENCODE


def test_setup_sync_auto_detects_and_updates_existing_opencode_jsonc(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_api = _FakeApiClient()
    opencode_dir = tmp_path / ".config" / "opencode"
    json_path = opencode_dir / "opencode.json"
    jsonc_path = opencode_dir / "opencode.jsonc"
    opencode_dir.mkdir(parents=True)
    jsonc_path.write_text('{"mcp": {}}\n')

    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(
        setup, "set_credentials_in_context", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        setup,
        "resolve_credentials",
        lambda *args, **kwargs: {"secret": "secret", "host": "https://example.com"},
    )
    monkeypatch.setattr(setup, "RunlayerClient", lambda *args, **kwargs: fake_api)

    setup.sync(
        ctx=cast(Any, object()),
        client=None,
        header=None,
        secret=None,
        host=None,
        yes=True,
    )

    config = json.loads(jsonc_path.read_text())
    assert not json_path.exists()
    assert set(config["mcp"]) == {"auto-sync-server", "onelayer"}
