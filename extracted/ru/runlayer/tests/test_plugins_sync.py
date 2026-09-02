import json
import datetime
import shutil
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from runlayer_cli.api import (
    PluginDetail,
    PluginServerRef,
    PluginSkillRef,
    ServerListItem,
)
from runlayer_cli.plugins.models import DiscoveredPlugin, ServerConnector
from runlayer_cli.plugins.sync_engine import (
    _plugin_changed,
    sync_discovered_plugins,
    sync_plugins,
)
from runlayer_cli.scan.plugin_scanner import compute_plugin_identifier
from runlayer_cli.skills.sync_engine import SyncResult

FIXTURE_ROOT = Path(__file__).parent / "e2e" / "fixtures" / "full_plugin"
NAMESPACE = "myorg/plugins"


def _copy_fixture(tmp_path: Path) -> Path:
    plugin_root = tmp_path / "review-suite"
    shutil.copytree(FIXTURE_ROOT, plugin_root)
    _replace_fixture_placeholders(
        plugin_root,
        server_id="12345678-1234-1234-1234-123456789abc",
        api_key="secret",
    )
    return plugin_root


def _replace_fixture_placeholders(
    plugin_root: Path, *, server_id: str, api_key: str
) -> None:
    for path in [
        plugin_root / ".mcp.json",
        plugin_root / ".claude-plugin" / "plugin.json",
    ]:
        raw = path.read_text()
        raw = raw.replace("__SERVER_ID__", server_id).replace("__API_KEY__", api_key)
        path.write_text(raw)


def _write_fixture_mcp_servers(
    plugin_root: Path, mcp_servers: dict[str, object]
) -> None:
    mcp_payload = {"mcpServers": mcp_servers}
    (plugin_root / ".mcp.json").write_text(json.dumps(mcp_payload, indent=2))
    manifest_path = plugin_root / ".claude-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["mcpServers"] = mcp_servers
    manifest_path.write_text(json.dumps(manifest, indent=2))


def _client() -> MagicMock:
    client = MagicMock()
    client.list_plugins_detailed.return_value = []
    client.list_skills.return_value = []
    client.list_servers_for_resolution.return_value = [
        ServerListItem(
            id="12345678-1234-1234-1234-123456789abc",
            name="alpha",
            status="active",
        )
    ]
    client.list_server_tools.return_value = [
        {"name": "search"},
        {"name": "create_ticket"},
    ]
    return client


def _ts() -> datetime.datetime:
    return datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc)


def _make_plugin(
    root: Path,
    *,
    name: str = "demo-plugin",
    description: str | None = "demo description",
) -> Path:
    plugin_root = root / name
    manifest_dir = plugin_root / ".claude-plugin"
    manifest_dir.mkdir(parents=True)
    description_json = "null" if description is None else f'"{description}"'
    (manifest_dir / "plugin.json").write_text(
        f'{{"name":"{name}","version":"1.0.0","description":{description_json}}}'
    )
    return plugin_root


@pytest.mark.asyncio
async def test_sync_plugins_creates_plugin_and_filters_missing_servers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _copy_fixture(tmp_path)
    client = _client()
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(
            return_value=SyncResult(
                created=3,
                ids_by_path={
                    "review-suite/code-review": "skill-1",
                    "review-suite/__root__": "skill-2",
                    "review-suite/ticket-triage": "skill-3",
                },
            )
        ),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.created == 1
    assert any(
        "missing server 00000000-0000-0000-0000-000000000000 skipped" in w
        for w in result.warnings
    )
    client.create_plugin.assert_called_once()
    kwargs = client.create_plugin.call_args.kwargs
    assert kwargs["namespace"] == NAMESPACE
    assert kwargs["path"] == "review-suite"
    assert kwargs["skill_ids"] == ["skill-1", "skill-3", "skill-2"]
    assert kwargs["servers"] == [
        PluginServerRef(
            server_id="12345678-1234-1234-1234-123456789abc",
            tool_names=["search", "create_ticket"],
        )
    ]


@pytest.mark.asyncio
async def test_sync_plugins_update_preserves_existing_connector_tools(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plugin_root = _copy_fixture(tmp_path)
    identifier = compute_plugin_identifier(plugin_root)
    client = _client()
    client.list_plugins_detailed.return_value = [
        PluginDetail(
            id="plugin-1",
            name="review-suite",
            path="review-suite",
            namespace=NAMESPACE,
            description="Review, triage, hooks, agents, and connector coverage",
            identifier=identifier,
            servers=[
                {
                    "id": "12345678-1234-1234-1234-123456789abc",
                    "tools": [{"name": "search"}],
                }
            ],
            skills=[
                PluginSkillRef(id="skill-1", name="code-review"),
                PluginSkillRef(id="skill-2", name="review-suite"),
                PluginSkillRef(id="skill-3", name="ticket-triage"),
            ],
            created_at=_ts(),
            updated_at=_ts(),
        )
    ]
    client.list_skills.return_value = [
        MagicMock(path="review-suite/code-review", id="skill-1"),
        MagicMock(path="review-suite/__root__", id="skill-2"),
        MagicMock(path="review-suite/ticket-triage", id="skill-3"),
    ]
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(
            return_value=SyncResult(
                ids_by_path={
                    "review-suite/code-review": "skill-1",
                    "review-suite/__root__": "skill-2",
                    "review-suite/ticket-triage": "skill-3",
                }
            )
        ),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.unchanged == 1
    client.list_server_tools.assert_not_called()


@pytest.mark.asyncio
async def test_sync_plugins_update_reads_existing_connector_tools_when_detail_omits_them(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _copy_fixture(tmp_path)
    client = _client()
    client.list_plugins_detailed.return_value = [
        PluginDetail(
            id="plugin-1",
            name="review-suite",
            path="review-suite",
            namespace=NAMESPACE,
            description="old description",
            servers=[{"id": "12345678-1234-1234-1234-123456789abc"}],
            skills=[
                PluginSkillRef(id="skill-1", name="code-review"),
                PluginSkillRef(id="skill-2", name="review-suite"),
                PluginSkillRef(id="skill-3", name="ticket-triage"),
            ],
            created_at=_ts(),
            updated_at=_ts(),
        )
    ]
    client.get_plugin_server_tools.return_value = ["search"]
    client.list_skills.return_value = [
        MagicMock(path="review-suite/code-review", id="skill-1"),
        MagicMock(path="review-suite/__root__", id="skill-2"),
        MagicMock(path="review-suite/ticket-triage", id="skill-3"),
    ]
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(
            return_value=SyncResult(
                ids_by_path={
                    "review-suite/code-review": "skill-1",
                    "review-suite/__root__": "skill-2",
                    "review-suite/ticket-triage": "skill-3",
                }
            )
        ),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.updated == 1
    client.get_plugin_server_tools.assert_called_once_with(
        "plugin-1", "12345678-1234-1234-1234-123456789abc"
    )
    assert client.update_plugin.call_args.kwargs["servers"] == [
        PluginServerRef(
            server_id="12345678-1234-1234-1234-123456789abc",
            tool_names=["search"],
        )
    ]


@pytest.mark.asyncio
async def test_sync_plugins_wraps_existing_connector_tool_lookup_timeout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _copy_fixture(tmp_path)
    client = _client()
    client.list_plugins_detailed.return_value = [
        PluginDetail(
            id="plugin-1",
            name="review-suite",
            path="review-suite",
            namespace=NAMESPACE,
            description="old description",
            servers=[{"id": "12345678-1234-1234-1234-123456789abc"}],
            skills=[
                PluginSkillRef(id="skill-1", name="code-review"),
                PluginSkillRef(id="skill-2", name="review-suite"),
                PluginSkillRef(id="skill-3", name="ticket-triage"),
            ],
            created_at=_ts(),
            updated_at=_ts(),
        )
    ]
    client.get_plugin_server_tools.side_effect = httpx.ReadTimeout(
        "The read operation timed out"
    )
    client.list_skills.return_value = [
        MagicMock(path="review-suite/code-review", id="skill-1"),
        MagicMock(path="review-suite/__root__", id="skill-2"),
        MagicMock(path="review-suite/ticket-triage", id="skill-3"),
    ]
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(
            return_value=SyncResult(
                ids_by_path={
                    "review-suite/code-review": "skill-1",
                    "review-suite/__root__": "skill-2",
                    "review-suite/ticket-triage": "skill-3",
                }
            )
        ),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.errors == [
        "review-suite: failed to resolve tools for connector "
        "12345678-1234-1234-1234-123456789abc; plugin not synced"
    ]
    client.update_plugin.assert_not_called()


@pytest.mark.asyncio
async def test_sync_plugins_preserves_skill_visibility_without_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _copy_fixture(tmp_path)
    client = _client()
    sync_skills_mock = AsyncMock(
        return_value=SyncResult(
            ids_by_path={
                "review-suite/code-review": "skill-1",
                "review-suite/__root__": "skill-2",
                "review-suite/ticket-triage": "skill-3",
            }
        )
    )
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        sync_skills_mock,
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.errors == []
    assert sync_skills_mock.await_args.kwargs["is_public"] is None


@pytest.mark.asyncio
async def test_sync_plugins_skips_remote_server_entries_without_id_in_change_detection(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plugin_root = _copy_fixture(tmp_path)
    identifier = compute_plugin_identifier(plugin_root)
    client = _client()
    client.list_plugins_detailed.return_value = [
        PluginDetail(
            id="plugin-1",
            name="review-suite",
            path="review-suite",
            namespace=NAMESPACE,
            description="Review, triage, hooks, agents, and connector coverage",
            identifier=identifier,
            servers=[
                {},
                {
                    "id": "12345678-1234-1234-1234-123456789abc",
                    "tools": [{"name": "search"}],
                },
            ],
            skills=[
                PluginSkillRef(id="skill-1", name="code-review"),
                PluginSkillRef(id="skill-2", name="review-suite"),
                PluginSkillRef(id="skill-3", name="ticket-triage"),
            ],
            created_at=_ts(),
            updated_at=_ts(),
        )
    ]
    client.list_skills.return_value = [
        MagicMock(path="review-suite/code-review", id="skill-1"),
        MagicMock(path="review-suite/__root__", id="skill-2"),
        MagicMock(path="review-suite/ticket-triage", id="skill-3"),
    ]
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(
            return_value=SyncResult(
                ids_by_path={
                    "review-suite/code-review": "skill-1",
                    "review-suite/__root__": "skill-2",
                    "review-suite/ticket-triage": "skill-3",
                }
            )
        ),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.errors == []
    assert result.unchanged == 1


@pytest.mark.asyncio
async def test_sync_plugins_skips_remote_server_entries_without_id_in_warning_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _make_plugin(tmp_path, name="review-suite")
    client = _client()
    client.list_plugins_detailed.return_value = [
        PluginDetail(
            id="plugin-1",
            name="review-suite",
            path="review-suite",
            namespace=NAMESPACE,
            description="demo description",
            servers=[{}, {"id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"}],
            skills=[],
            created_at=_ts(),
            updated_at=_ts(),
        )
    ]
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(return_value=SyncResult()),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.errors == []
    assert result.updated == 1
    assert result.warnings == [
        "review-suite: push will remove remote connectors not present in local plugin state: aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    ]


@pytest.mark.asyncio
async def test_sync_plugins_update_adds_all_tools_for_new_connector(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _copy_fixture(tmp_path)
    client = _client()
    client.list_plugins_detailed.return_value = [
        PluginDetail(
            id="plugin-1",
            name="review-suite",
            path="review-suite",
            namespace=NAMESPACE,
            description="Review, triage, hooks, agents, and connector coverage",
            servers=[],
            skills=[
                PluginSkillRef(id="skill-1", name="code-review"),
                PluginSkillRef(id="skill-2", name="review-suite"),
                PluginSkillRef(id="skill-3", name="ticket-triage"),
            ],
            created_at=_ts(),
            updated_at=_ts(),
        )
    ]
    client.list_skills.return_value = [
        MagicMock(path="review-suite/code-review", id="skill-1"),
        MagicMock(path="review-suite/__root__", id="skill-2"),
        MagicMock(path="review-suite/ticket-triage", id="skill-3"),
    ]
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(
            return_value=SyncResult(
                ids_by_path={
                    "review-suite/code-review": "skill-1",
                    "review-suite/__root__": "skill-2",
                    "review-suite/ticket-triage": "skill-3",
                }
            )
        ),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.updated == 1
    assert client.update_plugin.call_args.kwargs["servers"] == [
        PluginServerRef(
            server_id="12345678-1234-1234-1234-123456789abc",
            tool_names=["search", "create_ticket"],
        )
    ]


@pytest.mark.asyncio
async def test_sync_plugins_prune_scopes_skill_deletes_to_plugin_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _copy_fixture(tmp_path)
    client = _client()
    client.list_plugins_detailed.return_value = [
        PluginDetail(
            id="plugin-1",
            name="review-suite",
            path="review-suite",
            namespace=NAMESPACE,
            servers=[],
            skills=[],
            created_at=_ts(),
            updated_at=_ts(),
        )
    ]
    client.list_skills.return_value = [
        MagicMock(path="review-suite/__root__", id="skill-root"),
        MagicMock(path="review-suite/code-review", id="skill-child"),
        MagicMock(path="standalone/keep-me", id="skill-keep"),
    ]
    sync_mock = AsyncMock(return_value=SyncResult())
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills", sync_mock
    )

    await sync_plugins(tmp_path, client, namespace=NAMESPACE, prune=True)

    assert sync_mock.await_args.kwargs["prune"] is False
    assert "prune_remote_paths" not in sync_mock.await_args.kwargs


@pytest.mark.asyncio
async def test_sync_plugins_create_409_retries_as_update(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _copy_fixture(tmp_path)
    client = _client()
    response_409 = httpx.Response(409, request=httpx.Request("POST", "http://test"))
    client.create_plugin.side_effect = httpx.HTTPStatusError(
        "Conflict", request=response_409.request, response=response_409
    )
    client.list_plugins_detailed.side_effect = [
        [],
        [
            PluginDetail(
                id="plugin-1",
                name="review-suite",
                path="review-suite",
                namespace=NAMESPACE,
                description="old",
                servers=[],
                skills=[],
                created_at=_ts(),
                updated_at=_ts(),
            )
        ],
    ]
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(
            return_value=SyncResult(
                ids_by_path={
                    "review-suite/code-review": "skill-1",
                    "review-suite/__root__": "skill-2",
                    "review-suite/ticket-triage": "skill-3",
                }
            )
        ),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.updated == 1
    client.update_plugin.assert_called_once()


@pytest.mark.asyncio
async def test_sync_plugins_create_409_retry_finds_shared_resource(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """409 retry must find plugins shared (CAN_EDIT) but not owned.

    Repro for the Opendoor owner_required bug: a service account granted
    CAN_EDIT pushes a plugin it doesn't own. create_plugin 409s (path exists);
    the retry lookup must use filter="all", since the owned-only default
    ("created_by_me") hides shared plugins and re-raises the 409 as a failure.
    """
    _copy_fixture(tmp_path)
    client = _client()
    response_409 = httpx.Response(409, request=httpx.Request("POST", "http://test"))
    client.create_plugin.side_effect = httpx.HTTPStatusError(
        "Conflict", request=response_409.request, response=response_409
    )

    shared_plugin = PluginDetail(
        id="plugin-1",
        name="review-suite",
        path="review-suite",
        namespace=NAMESPACE,
        description="old",
        can_edit=True,
        is_owned_by_me=False,
        servers=[],
        skills=[],
        created_at=_ts(),
        updated_at=_ts(),
    )

    def _list_plugins(namespace=None, *, filter="created_by_me", query=None):
        # Mirror backend semantics: shared-but-not-owned plugins only appear
        # under filter="all" / "shared_with_me", never "created_by_me".
        if filter == "created_by_me":
            return []
        return [shared_plugin]

    client.list_plugins_detailed.side_effect = _list_plugins
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(
            return_value=SyncResult(
                ids_by_path={
                    "review-suite/code-review": "skill-1",
                    "review-suite/__root__": "skill-2",
                    "review-suite/ticket-triage": "skill-3",
                }
            )
        ),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.errors == []
    assert result.updated == 1
    client.update_plugin.assert_called_once()


@pytest.mark.asyncio
async def test_sync_plugins_prunes_removed_child_skill_without_global_prune(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plugin_root = _copy_fixture(tmp_path)
    shutil.rmtree(plugin_root / "skills" / "ticket-triage")

    client = _client()
    client.list_skills.return_value = [
        MagicMock(path="review-suite/__root__", id="skill-root"),
        MagicMock(path="review-suite/code-review", id="skill-child"),
        MagicMock(path="review-suite/ticket-triage", id="skill-removed"),
        MagicMock(path="standalone/keep-me", id="skill-keep"),
    ]
    sync_mock = AsyncMock(
        return_value=SyncResult(
            ids_by_path={
                "review-suite/code-review": "skill-1",
                "review-suite/__root__": "skill-2",
            }
        )
    )
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills", sync_mock
    )

    await sync_plugins(tmp_path, client, namespace=NAMESPACE, prune=False)

    assert sync_mock.await_args.kwargs["prune"] is False
    assert "prune_remote_paths" not in sync_mock.await_args.kwargs


@pytest.mark.asyncio
async def test_sync_plugins_updates_plugin_before_deleting_removed_child_skill(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plugin_root = _copy_fixture(tmp_path)
    shutil.rmtree(plugin_root / "skills" / "ticket-triage")

    client = _client()
    client.list_plugins_detailed.return_value = [
        PluginDetail(
            id="plugin-1",
            name="review-suite",
            path="review-suite",
            namespace=NAMESPACE,
            description="Review, triage, hooks, agents, and connector coverage",
            servers=[{"id": "12345678-1234-1234-1234-123456789abc"}],
            skills=[
                PluginSkillRef(id="skill-1", name="code-review"),
                PluginSkillRef(id="skill-2", name="review-suite"),
                PluginSkillRef(id="skill-3", name="ticket-triage"),
            ],
            created_at=_ts(),
            updated_at=_ts(),
        )
    ]
    client.list_skills.return_value = [
        MagicMock(path="review-suite/code-review", id="skill-1"),
        MagicMock(path="review-suite/__root__", id="skill-2"),
        MagicMock(path="review-suite/ticket-triage", id="skill-3"),
    ]
    sync_mock = AsyncMock(
        return_value=SyncResult(
            ids_by_path={
                "review-suite/code-review": "skill-1",
                "review-suite/__root__": "skill-2",
            }
        )
    )
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills", sync_mock
    )

    calls: list[str] = []

    def _update_plugin(*args, **kwargs) -> None:
        calls.append("update_plugin")

    def _delete_skill(skill_id: str) -> None:
        calls.append(f"delete_skill:{skill_id}")

    client.update_plugin.side_effect = _update_plugin
    client.delete_skill.side_effect = _delete_skill

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE, prune=False)

    assert result.errors == []
    assert calls == ["update_plugin", "delete_skill:skill-3"]


@pytest.mark.asyncio
async def test_sync_plugins_does_not_delete_removed_child_skill_if_update_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plugin_root = _copy_fixture(tmp_path)
    shutil.rmtree(plugin_root / "skills" / "ticket-triage")

    client = _client()
    client.list_plugins_detailed.return_value = [
        PluginDetail(
            id="plugin-1",
            name="review-suite",
            path="review-suite",
            namespace=NAMESPACE,
            description="Review, triage, hooks, agents, and connector coverage",
            servers=[
                {
                    "id": "12345678-1234-1234-1234-123456789abc",
                    "tools": [{"name": "search"}],
                }
            ],
            skills=[
                PluginSkillRef(id="skill-1", name="code-review"),
                PluginSkillRef(id="skill-2", name="review-suite"),
                PluginSkillRef(id="skill-3", name="ticket-triage"),
            ],
            created_at=_ts(),
            updated_at=_ts(),
        )
    ]
    client.list_skills.return_value = [
        MagicMock(path="review-suite/code-review", id="skill-1"),
        MagicMock(path="review-suite/__root__", id="skill-2"),
        MagicMock(path="review-suite/ticket-triage", id="skill-3"),
    ]
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(
            return_value=SyncResult(
                ids_by_path={
                    "review-suite/code-review": "skill-1",
                    "review-suite/__root__": "skill-2",
                }
            )
        ),
    )
    response_409 = httpx.Response(409, request=httpx.Request("PUT", "http://test"))
    client.update_plugin.side_effect = httpx.HTTPStatusError(
        "Conflict", request=response_409.request, response=response_409
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE, prune=False)

    assert result.errors
    client.delete_skill.assert_not_called()


@pytest.mark.asyncio
async def test_sync_plugins_prune_does_not_delete_linked_skills_if_plugin_delete_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _make_plugin(tmp_path, name="local-only")
    client = _client()
    client.list_plugins_detailed.return_value = [
        PluginDetail(
            id="plugin-remote",
            name="remote-only",
            path="remote-only",
            namespace=NAMESPACE,
            description="remote plugin",
            servers=[],
            skills=[
                PluginSkillRef(id="skill-remote-1", name="remote-only"),
                PluginSkillRef(id="skill-remote-2", name="child"),
            ],
            created_at=_ts(),
            updated_at=_ts(),
        )
    ]
    client.list_skills.return_value = [
        MagicMock(path="remote-only/__root__", id="skill-remote-1"),
        MagicMock(path="remote-only/child", id="skill-remote-2"),
    ]
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(return_value=SyncResult()),
    )
    response_409 = httpx.Response(409, request=httpx.Request("DELETE", "http://test"))
    client.delete_plugin.side_effect = httpx.HTTPStatusError(
        "Conflict", request=response_409.request, response=response_409
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE, prune=True)

    assert result.errors
    client.delete_skill.assert_not_called()


@pytest.mark.asyncio
async def test_sync_plugins_does_not_delete_same_prefix_standalone_skill(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plugin_root = _copy_fixture(tmp_path)
    shutil.rmtree(plugin_root / "skills" / "ticket-triage")

    client = _client()
    client.list_plugins_detailed.return_value = [
        PluginDetail(
            id="plugin-1",
            name="review-suite",
            path="review-suite",
            namespace=NAMESPACE,
            description="Review, triage, hooks, agents, and connector coverage",
            servers=[{"id": "12345678-1234-1234-1234-123456789abc"}],
            skills=[
                PluginSkillRef(id="skill-1", name="code-review"),
                PluginSkillRef(id="skill-2", name="review-suite"),
            ],
            created_at=_ts(),
            updated_at=_ts(),
        )
    ]
    client.list_skills.return_value = [
        MagicMock(path="review-suite/code-review", id="skill-1"),
        MagicMock(path="review-suite/__root__", id="skill-2"),
        MagicMock(path="review-suite/custom-playbook", id="standalone-skill"),
    ]
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(
            return_value=SyncResult(
                ids_by_path={
                    "review-suite/code-review": "skill-1",
                    "review-suite/__root__": "skill-2",
                }
            )
        ),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE, prune=False)

    assert result.errors == []
    client.delete_skill.assert_not_called()


@pytest.mark.asyncio
async def test_sync_plugins_warns_before_removing_remote_connectors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _copy_fixture(tmp_path)
    client = _client()
    client.list_plugins_detailed.return_value = [
        PluginDetail(
            id="plugin-1",
            name="review-suite",
            path="review-suite",
            namespace=NAMESPACE,
            description="Review, triage, hooks, agents, and connector coverage",
            servers=[
                {"id": "12345678-1234-1234-1234-123456789abc"},
                {"id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"},
            ],
            skills=[
                PluginSkillRef(id="skill-1", name="code-review"),
                PluginSkillRef(id="skill-2", name="review-suite"),
                PluginSkillRef(id="skill-3", name="ticket-triage"),
            ],
            created_at=_ts(),
            updated_at=_ts(),
        )
    ]
    client.list_skills.return_value = [
        MagicMock(path="review-suite/code-review", id="skill-1"),
        MagicMock(path="review-suite/__root__", id="skill-2"),
        MagicMock(path="review-suite/ticket-triage", id="skill-3"),
    ]
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(
            return_value=SyncResult(
                ids_by_path={
                    "review-suite/code-review": "skill-1",
                    "review-suite/__root__": "skill-2",
                    "review-suite/ticket-triage": "skill-3",
                }
            )
        ),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert any(
        "review-suite: push will remove remote connectors not present in local plugin state: aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        == warning
        for warning in result.warnings
    )


@pytest.mark.asyncio
async def test_sync_plugins_dry_run_uses_same_remote_change_detection_without_get_skill(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plugin_root = _copy_fixture(tmp_path)
    identifier = compute_plugin_identifier(plugin_root)
    client = _client()
    client.list_plugins_detailed.return_value = [
        PluginDetail(
            id="plugin-1",
            name="review-suite",
            path="review-suite",
            namespace=NAMESPACE,
            description="Review, triage, hooks, agents, and connector coverage",
            identifier=identifier,
            servers=[{"id": "12345678-1234-1234-1234-123456789abc"}],
            skills=[
                PluginSkillRef(id="skill-1", name="code-review"),
                PluginSkillRef(id="skill-2", name="review-suite"),
                PluginSkillRef(id="skill-3", name="ticket-triage"),
            ],
            created_at=_ts(),
            updated_at=_ts(),
        )
    ]
    client.list_skills.return_value = [
        MagicMock(path="review-suite/code-review", id="skill-1"),
        MagicMock(path="review-suite/__root__", id="skill-2"),
        MagicMock(path="review-suite/ticket-triage", id="skill-3"),
    ]
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(return_value=SyncResult(created=3)),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE, dry_run=True)

    assert result.errors == []
    assert result.unchanged == 1
    client.get_skill.assert_not_called()


@pytest.mark.asyncio
async def test_sync_plugins_updates_when_description_removed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plugin_root = _copy_fixture(tmp_path)
    manifest_path = plugin_root / ".claude-plugin" / "plugin.json"
    manifest_path.write_text('{"name":"review-suite","version":"1.0.0"}')

    client = _client()
    client.list_plugins_detailed.return_value = [
        PluginDetail(
            id="plugin-1",
            name="review-suite",
            path="review-suite",
            namespace=NAMESPACE,
            description="Review and triage code",
            servers=[],
            skills=[
                PluginSkillRef(id="skill-1", name="code-review"),
                PluginSkillRef(id="skill-2", name="review-suite"),
                PluginSkillRef(id="skill-3", name="ticket-triage"),
            ],
            created_at=_ts(),
            updated_at=_ts(),
        )
    ]
    client.list_skills.return_value = [
        MagicMock(path="review-suite/code-review", id="skill-1"),
        MagicMock(path="review-suite/__root__", id="skill-2"),
        MagicMock(path="review-suite/ticket-triage", id="skill-3"),
    ]
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(
            return_value=SyncResult(
                ids_by_path={
                    "review-suite/code-review": "skill-1",
                    "review-suite/__root__": "skill-2",
                    "review-suite/ticket-triage": "skill-3",
                }
            )
        ),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.updated == 1
    assert client.update_plugin.call_args.kwargs["description"] is None


@pytest.mark.asyncio
async def test_sync_plugins_dry_run_does_not_require_skill_ids(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _copy_fixture(tmp_path)
    client = _client()
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(return_value=SyncResult(created=3)),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE, dry_run=True)

    assert result.errors == []
    assert result.created == 1


@pytest.mark.asyncio
async def test_sync_plugins_truncates_long_description_before_create(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _make_plugin(tmp_path, description="x" * 1025)
    client = _client()
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(return_value=SyncResult()),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.created == 1
    assert client.create_plugin.call_args.kwargs["description"] == "x" * 1024


@pytest.mark.asyncio
async def test_sync_plugins_includes_discovery_mcp_warnings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plugin_root = _copy_fixture(tmp_path)
    _write_fixture_mcp_servers(
        plugin_root,
        {
            "external-http": {
                "type": "http",
                "url": "https://example.com/mcp",
            }
        },
    )
    client = _client()
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(return_value=SyncResult()),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.warnings == [
        "review-suite: skipped MCP server external-http with non-Runlayer URL https://example.com/mcp"
    ]


@pytest.mark.asyncio
async def test_sync_plugins_surfaces_422_detail_from_backend(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _make_plugin(tmp_path)
    client = _client()
    response = httpx.Response(
        422,
        request=httpx.Request("POST", "http://test"),
        json={"detail": "description too long"},
    )
    client.create_plugin.side_effect = httpx.HTTPStatusError(
        "Unprocessable Content",
        request=response.request,
        response=response,
    )
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(return_value=SyncResult()),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.errors == ["demo-plugin: description too long"]


@pytest.mark.asyncio
async def test_sync_plugins_surfaces_422_validation_list_from_backend(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _make_plugin(tmp_path)
    client = _client()
    response = httpx.Response(
        422,
        request=httpx.Request("POST", "http://test"),
        json={
            "detail": [
                {
                    "type": "string_too_long",
                    "loc": ["body", "description"],
                    "msg": "String should have at most 1024 characters",
                },
                {
                    "type": "uuid_parsing",
                    "loc": ["body", "servers", 0, "server_id"],
                    "msg": "Input should be a valid UUID",
                },
            ]
        },
    )
    client.create_plugin.side_effect = httpx.HTTPStatusError(
        "Unprocessable Content",
        request=response.request,
        response=response,
    )
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(return_value=SyncResult()),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.errors == [
        "demo-plugin: description: String should have at most 1024 characters; "
        "servers.0.server_id: Input should be a valid UUID"
    ]


@pytest.mark.asyncio
async def test_sync_plugins_skips_malformed_runlayer_connector_before_create(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plugin_root = _make_plugin(tmp_path, name="demo-plugin")
    mcp_path = plugin_root / ".mcp.json"
    mcp_path.write_text(
        json.dumps(
            {
                "mcpServers": {
                    "bad-runlayer": {
                        "url": (
                            "https://app.runlayer.com/api/v1/proxy/"
                            "12345678123412341234123456789abcdef0/mcp"
                        )
                    }
                }
            }
        )
    )
    client = _client()
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(return_value=SyncResult()),
    )

    result = await sync_plugins(tmp_path, client, namespace=NAMESPACE)

    assert result.errors == []
    assert result.created == 1
    assert result.warnings == [
        "demo-plugin: skipped MCP server bad-runlayer with malformed Runlayer "
        "server id 12345678123412341234123456789abcdef0"
    ]
    assert client.create_plugin.call_args.kwargs["servers"] == []
    client.list_server_tools.assert_not_called()


@pytest.mark.asyncio
async def test_sync_discovered_plugins_continues_after_connector_tool_lookup_timeout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = _client()
    client.list_server_tools.side_effect = httpx.ReadTimeout(
        "The read operation timed out"
    )
    plugins = [
        DiscoveredPlugin(
            root=tmp_path / "timed-out-plugin",
            path="timed-out-plugin",
            name="timed-out-plugin",
            server_connectors=[
                ServerConnector(
                    server_id="12345678-1234-1234-1234-123456789abc",
                    entry_name="alpha",
                )
            ],
            skills=[],
        ),
        DiscoveredPlugin(
            root=tmp_path / "healthy-plugin",
            path="healthy-plugin",
            name="healthy-plugin",
            skills=[],
        ),
    ]
    monkeypatch.setattr(
        "runlayer_cli.plugins.sync_engine.sync_discovered_skills",
        AsyncMock(return_value=SyncResult()),
    )

    result = await sync_discovered_plugins(plugins, client, namespace=NAMESPACE)

    assert result.created == 1
    assert result.errors == [
        "timed-out-plugin: failed to resolve tools for connector "
        "12345678-1234-1234-1234-123456789abc; plugin not synced"
    ]
    assert client.create_plugin.call_count == 1
    assert client.create_plugin.call_args.kwargs["path"] == "healthy-plugin"


class TestPluginChangedIdentifier:
    """_plugin_changed must detect identifier transitions involving None."""

    @staticmethod
    def _base_remote(**overrides: object) -> PluginDetail:
        defaults: dict[str, object] = dict(
            id="p1",
            name="p",
            path="p",
            namespace="ns",
            description="d",
            is_public=False,
            use_dynamic_tools=False,
            servers=[],
            skills=[],
            identifier=None,
        )
        defaults.update(overrides)
        return PluginDetail(**defaults)  # type: ignore[arg-type]

    @staticmethod
    def _base_local(**overrides: object) -> DiscoveredPlugin:
        defaults: dict[str, object] = dict(
            root=Path("/tmp/p"),
            path="p",
            name="p",
            description="d",
            identifier=None,
        )
        defaults.update(overrides)
        return DiscoveredPlugin(**defaults)  # type: ignore[arg-type]

    def _changed(self, remote: PluginDetail, local: DiscoveredPlugin) -> bool:
        return _plugin_changed(
            remote,
            local,
            namespace=remote.namespace or "",
            desired_skill_membership=[],
            remote_skill_membership=[],
            servers=[],
            is_public=remote.is_public,
            use_dynamic_tools=remote.use_dynamic_tools,
        )

    def test_both_none_unchanged(self) -> None:
        assert not self._changed(self._base_remote(), self._base_local())

    def test_same_value_unchanged(self) -> None:
        assert not self._changed(
            self._base_remote(identifier="abc"),
            self._base_local(identifier="abc"),
        )

    def test_remote_none_local_set_is_changed(self) -> None:
        assert self._changed(
            self._base_remote(identifier=None),
            self._base_local(identifier="abc"),
        )

    def test_remote_set_local_none_is_changed(self) -> None:
        assert self._changed(
            self._base_remote(identifier="abc"),
            self._base_local(identifier=None),
        )

    def test_different_values_is_changed(self) -> None:
        assert self._changed(
            self._base_remote(identifier="abc"),
            self._base_local(identifier="def"),
        )
