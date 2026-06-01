from __future__ import annotations

from typing import Any, cast

import pytest
from runlayer_cli.api import AutoSyncItem, PluginListItem, ServerListItem
from runlayer_cli.commands import setup


class _FakeApiClient:
    def __init__(self) -> None:
        self.scopes: list[str] = []
        self.auto_sync_entity_types: list[str] = []

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

    def list_auto_sync(self, entity_type: str) -> list[AutoSyncItem]:
        self.auto_sync_entity_types.append(entity_type)
        return [AutoSyncItem(entity_type="plugin", entity_id="plugin-auto-sync")]

    def get_plugin(self, plugin_id: str) -> PluginListItem:
        assert plugin_id == "plugin-auto-sync"
        return PluginListItem(id=plugin_id, name="OneLayer")


def test_setup_sync_fetches_auto_synced_servers_and_plugins(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_api = _FakeApiClient()
    installed: list[tuple[setup.InstallClient, list[setup.InstallServerSpec]]] = []

    monkeypatch.setattr(setup, "set_credentials_in_context", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        setup,
        "resolve_credentials",
        lambda *args, **kwargs: {"secret": "secret", "host": "https://example.com"},
    )
    monkeypatch.setattr(setup, "RunlayerClient", lambda *args, **kwargs: fake_api)
    monkeypatch.setattr(
        setup,
        "_install_servers_to_client",
        lambda client, specs: installed.append((client, specs)),
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
    assert fake_api.auto_sync_entity_types == ["plugin"]
    assert len(installed) == 1
    assert installed[0][0] == setup.InstallClient.CURSOR
    assert [spec.server_id for spec in installed[0][1]] == [
        "srv-auto-sync",
        "plugin-auto-sync",
    ]
    assert installed[0][1][1].proxy_url == (
        "https://example.com/api/v1/proxy/plugins/plugin-auto-sync/mcp"
    )


def test_setup_sync_skips_auto_synced_plugins_for_local_only_clients(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_api = _FakeApiClient()
    installed: list[tuple[setup.InstallClient, list[setup.InstallServerSpec]]] = []

    monkeypatch.setattr(setup, "set_credentials_in_context", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        setup,
        "resolve_credentials",
        lambda *args, **kwargs: {"secret": "secret", "host": "https://example.com"},
    )
    monkeypatch.setattr(setup, "RunlayerClient", lambda *args, **kwargs: fake_api)
    monkeypatch.setattr(
        setup,
        "_install_servers_to_client",
        lambda client, specs: installed.append((client, specs)),
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
