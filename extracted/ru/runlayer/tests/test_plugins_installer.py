"""Tests for plugins installer."""

from __future__ import annotations

import datetime
import json
from pathlib import Path

import httpx
import pytest

from runlayer_cli.api import (
    PluginDetail,
    PluginSkillRef,
    SkillDetail,
    SkillFileDetail,
    SkillFileMetadata,
)
from runlayer_cli.metrics import InstallationAnalyticsEvent
from runlayer_cli.plugins.installer import (
    CODEX_NATIVE_INSTALL_MODE,
    PluginLockEntry,
    _rewrite_plugin_skill_content,
    _write_plugin_lockfile,
    _write_plugin_manifest,
    _write_plugin_mcp_json,
    install_plugins,
    read_plugin_lockfile,
    uninstall_plugin,
    update_plugins,
)


def _plugin(
    *,
    id: str = "p1",
    name: str = "my-plugin",
    install_name: str | None = None,
    namespace: str | None = "org/repo",
    servers: list[dict] | None = None,
    skills: list[PluginSkillRef] | None = None,
    updated_at: datetime.datetime | None = None,
) -> PluginDetail:
    return PluginDetail(
        id=id,
        name=name,
        install_name=install_name,
        namespace=namespace,
        servers=servers or [{"server_id": "srv-1", "name": "My Server"}],
        skills=skills or [],
        updated_at=updated_at
        or datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
    )


def _lock_entry(
    name: str = "my-plugin",
    *,
    client: str = "claude_code",
    install_mode: str = "native",
) -> PluginLockEntry:
    return PluginLockEntry(
        name=name,
        id="p1",
        namespace="org/repo",
        updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
        client=client,
        install_mode=install_mode,
        server_ids=["srv-1"],
    )


# -- Lockfile tests --


def test_read_plugin_lockfile_empty(tmp_path: Path):
    lockfile = tmp_path / "lock.yml"
    assert read_plugin_lockfile(lockfile) == []


def test_read_write_plugin_lockfile_roundtrip(tmp_path: Path):
    lockfile = tmp_path / "lock" / "plugin-lock.yml"
    entries = [_lock_entry()]
    _write_plugin_lockfile(lockfile, entries)
    loaded = read_plugin_lockfile(lockfile)
    assert len(loaded) == 1
    assert loaded[0].name == "my-plugin"
    assert loaded[0].install_mode == "native"
    assert loaded[0].server_ids == ["srv-1"]


def test_read_plugin_lockfile_invalid_yaml(tmp_path: Path):
    lockfile = tmp_path / "lock.yml"
    lockfile.write_text("{{bad yaml", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid lockfile YAML"):
        read_plugin_lockfile(lockfile)


def test_read_plugin_lockfile_invalid_format(tmp_path: Path):
    lockfile = tmp_path / "lock.yml"
    lockfile.write_text("plugins: notalist", encoding="utf-8")
    with pytest.raises(ValueError, match="must be a list"):
        read_plugin_lockfile(lockfile)


# -- Manifest tests --


def test_write_plugin_manifest(tmp_path: Path):
    plugin = _plugin()
    _write_plugin_manifest(
        tmp_path, "my-plugin", plugin, "claude_code", "https://example.com"
    )
    manifest_path = tmp_path / "my-plugin" / ".claude-plugin" / "plugin.json"
    assert manifest_path.exists()
    data = json.loads(manifest_path.read_text())
    assert data["name"] == "my-plugin"
    assert data["description"] == "Runlayer plugin for my-plugin"
    assert data["version"] == "1.0.0"
    assert "id" not in data
    assert "namespace" not in data
    assert data["mcpServers"]["my-server"] == {
        "url": "https://example.com/api/v1/proxy/srv-1/mcp",
        "type": "http",
    }


def test_write_plugin_manifest_cursor(tmp_path: Path):
    plugin = _plugin()
    _write_plugin_manifest(tmp_path, "my-plugin", plugin, "cursor")
    manifest_path = tmp_path / "my-plugin" / ".cursor-plugin" / "plugin.json"
    assert manifest_path.exists()
    data = json.loads(manifest_path.read_text())
    assert data["id"] == "p1"
    assert data["name"] == "my-plugin"


def test_write_plugin_manifest_vscode(tmp_path: Path):
    plugin = _plugin()
    _write_plugin_manifest(tmp_path, "my-plugin", plugin, "vscode")
    manifest_path = tmp_path / "my-plugin" / ".vscode-plugin" / "plugin.json"
    assert manifest_path.exists()
    data = json.loads(manifest_path.read_text())
    assert data["id"] == "p1"
    assert data["name"] == "my-plugin"


def test_write_plugin_manifest_codex(tmp_path: Path):
    plugin = _plugin(skills=[PluginSkillRef(id="sk1", name="skill-one")])
    _write_plugin_manifest(
        tmp_path, "my-plugin", plugin, "codex", "https://example.com"
    )
    manifest_path = tmp_path / "my-plugin" / ".codex-plugin" / "plugin.json"
    assert manifest_path.exists()
    data = json.loads(manifest_path.read_text())
    assert data["name"] == "my-plugin"
    assert data["description"] is None
    assert data["skills"] == "./skills/"
    assert data["mcpServers"] == "./.mcp.json"
    assert "id" not in data


def test_write_plugin_manifest_codex_preserves_display_name(tmp_path: Path):
    plugin = _plugin(name="My Plugin Name")
    _write_plugin_manifest(
        tmp_path, "my-plugin-name", plugin, "codex", "https://example.com"
    )
    manifest_path = tmp_path / "my-plugin-name" / ".codex-plugin" / "plugin.json"
    assert manifest_path.exists()
    data = json.loads(manifest_path.read_text())
    assert data["name"] == "my-plugin-name"
    assert data["interface"] == {"displayName": "My Plugin Name"}


def test_rewrite_plugin_skill_content_inserts_name_into_existing_frontmatter() -> None:
    content = "---\ndescription: hi\n---\n# hi"
    result = _rewrite_plugin_skill_content(content, "my-skill")
    assert "name: my-skill" in result
    assert "description: hi" in result


def test_rewrite_plugin_skill_content_injects_frontmatter_when_missing() -> None:
    content = "# My Skill\n\nDo stuff."
    result = _rewrite_plugin_skill_content(content, "my-skill")
    assert result.startswith("---\n")
    assert "name: my-skill" in result
    assert result.endswith(content)


def test_write_plugin_mcp_json(tmp_path: Path):
    plugin = _plugin()
    _write_plugin_mcp_json(
        tmp_path, "my-plugin", plugin, "https://example.com", "claude_code"
    )
    mcp_path = tmp_path / "my-plugin" / ".mcp.json"
    assert mcp_path.exists()
    data = json.loads(mcp_path.read_text())
    assert "mcpServers" in data
    servers = data["mcpServers"]
    assert len(servers) == 1
    key = list(servers.keys())[0]
    assert "proxy/srv-1/mcp" in servers[key]["url"]
    assert servers[key]["type"] == "http"


def test_write_plugin_mcp_json_vscode(tmp_path: Path):
    plugin = _plugin()
    _write_plugin_mcp_json(
        tmp_path, "my-plugin", plugin, "https://example.com", "vscode"
    )
    mcp_path = tmp_path / "my-plugin" / ".mcp.json"
    assert mcp_path.exists()
    data = json.loads(mcp_path.read_text())
    assert "mcpServers" in data
    assert "servers" not in data
    servers = data["mcpServers"]
    assert len(servers) == 1
    key = list(servers.keys())[0]
    assert "proxy/srv-1/mcp" in servers[key]["url"]
    assert servers[key]["type"] == "http"


def test_write_plugin_mcp_json_cursor(tmp_path: Path):
    plugin = _plugin()
    _write_plugin_mcp_json(
        tmp_path, "my-plugin", plugin, "https://example.com", "cursor"
    )
    mcp_path = tmp_path / "my-plugin" / ".mcp.json"
    assert mcp_path.exists()
    data = json.loads(mcp_path.read_text())
    assert "mcpServers" in data
    assert "servers" not in data
    servers = data["mcpServers"]
    assert len(servers) == 1
    key = list(servers.keys())[0]
    assert "proxy/srv-1/mcp" in servers[key]["url"]
    assert "type" not in servers[key]


def test_write_plugin_mcp_json_codex(tmp_path: Path):
    plugin = _plugin()
    _write_plugin_mcp_json(
        tmp_path, "my-plugin", plugin, "https://example.com", "codex"
    )
    mcp_path = tmp_path / "my-plugin" / ".mcp.json"
    assert mcp_path.exists()
    data = json.loads(mcp_path.read_text())
    assert "mcpServers" not in data
    assert "mcp_servers" in data
    servers = data["mcp_servers"]
    assert len(servers) == 1
    key = list(servers.keys())[0]
    assert "proxy/srv-1/mcp" in servers[key]["url"]
    assert "type" not in servers[key]


# -- Fake clients --


def _raise_404(*_args, **_kwargs):
    req = httpx.Request("GET", "https://example.com/plugins/p1")
    resp = httpx.Response(404, request=req)
    raise httpx.HTTPStatusError("not found", request=req, response=resp)


class _FakeClient404:
    get_plugin = staticmethod(_raise_404)


class _FakeClientSinglePlugin:
    def __init__(self) -> None:
        self.installation_events: list[InstallationAnalyticsEvent] = []

    def list_plugins_by_namespace(self, namespace: str):
        return [_plugin()]

    def get_plugin(self, plugin_id: str) -> PluginDetail:
        return _plugin(id=plugin_id)

    def get_skill(self, skill_id: str) -> SkillDetail:
        return SkillDetail(
            id=skill_id,
            name="test-skill",
            files=[
                SkillFileMetadata(
                    id="f1",
                    skill_id=skill_id,
                    title="SKILL.md",
                    updated_at=datetime.datetime(
                        2024, 1, 1, tzinfo=datetime.timezone.utc
                    ),
                )
            ],
        )

    def get_skill_file(self, skill_id: str, file_id: str) -> SkillFileDetail:
        return SkillFileDetail(
            id=file_id,
            skill_id=skill_id,
            title="SKILL.md",
            content=f"# {skill_id}",
        )

    def track_installation_events(
        self, events: list[InstallationAnalyticsEvent]
    ) -> dict[str, int]:
        self.installation_events = events
        return {"recorded": len(events)}


class _FakeClientTrackingFails(_FakeClientSinglePlugin):
    def track_installation_events(
        self, events: list[InstallationAnalyticsEvent]
    ) -> dict[str, int]:
        del events
        request = httpx.Request(
            "POST", "https://example.com/api/v1/metrics/cli-install-events"
        )
        raise httpx.ReadTimeout("timeout", request=request)


class _FakeClientWithSkills(_FakeClientSinglePlugin):
    def list_plugins_by_namespace(self, namespace: str):
        return [
            _plugin(
                skills=[
                    PluginSkillRef(id="sk1", name="skill-one"),
                ]
            )
        ]


class _FakeClientCodexNamesWithSpaces(_FakeClientSinglePlugin):
    def list_plugins_by_namespace(self, namespace: str):
        return [
            _plugin(
                name="My Plugin Name",
                skills=[
                    PluginSkillRef(id="sk1", name="Skill Name With Spaces"),
                ],
            )
        ]

    def get_skill(self, skill_id: str) -> SkillDetail:
        return SkillDetail(
            id=skill_id,
            name="Skill Name With Spaces",
            files=[
                SkillFileMetadata(
                    id="f1",
                    skill_id=skill_id,
                    title="SKILL.md",
                    updated_at=datetime.datetime(
                        2024, 1, 1, tzinfo=datetime.timezone.utc
                    ),
                )
            ],
        )

    def get_skill_file(self, skill_id: str, file_id: str) -> SkillFileDetail:
        return SkillFileDetail(
            id=file_id,
            skill_id=skill_id,
            title="SKILL.md",
            content=(
                "---\n"
                "name: Skill Name With Spaces\n"
                "description: test skill\n"
                "---\n"
                "\n"
                "# Skill\n"
            ),
        )


class _FakeClientWithApiInstallName(_FakeClientSinglePlugin):
    def list_plugins_by_namespace(self, namespace: str):
        return [
            _plugin(
                name="Display Plugin Name",
                install_name="api-plugin-name",
                skills=[
                    PluginSkillRef(
                        id="sk1",
                        name="Display Skill Name",
                        install_name="api-skill-name",
                    ),
                ],
            )
        ]

    def get_skill(self, skill_id: str) -> SkillDetail:
        return SkillDetail(
            id=skill_id,
            name="Display Skill Name",
            install_name="api-skill-name",
            files=[
                SkillFileMetadata(
                    id="f1",
                    skill_id=skill_id,
                    title="SKILL.md",
                    updated_at=datetime.datetime(
                        2024, 1, 1, tzinfo=datetime.timezone.utc
                    ),
                )
            ],
        )

    def get_skill_file(self, skill_id: str, file_id: str) -> SkillFileDetail:
        return SkillFileDetail(
            id=file_id,
            skill_id=skill_id,
            title="SKILL.md",
            content=(
                "---\n"
                "name: Display Skill Name\n"
                "description: test skill\n"
                "---\n"
                "\n"
                "# Skill\n"
            ),
        )


class _FakeClientAllAccessible:
    def list_all_plugins(self, *, mine_only: bool):
        assert mine_only is False
        return [
            _plugin(id="p1", name="plugin-one", namespace="org/a"),
            _plugin(id="p2", name="plugin-two", namespace="org/b"),
        ]

    def get_plugin(self, plugin_id: str) -> PluginDetail:
        return _plugin(id=plugin_id)

    def get_skill(self, skill_id: str) -> SkillDetail:
        return SkillDetail(id=skill_id, name="test-skill", files=[])

    def get_skill_file(self, skill_id: str, file_id: str) -> SkillFileDetail:
        return SkillFileDetail(
            id=file_id, skill_id=skill_id, title="SKILL.md", content="# test"
        )

    def track_installation_events(
        self, events: list[InstallationAnalyticsEvent]
    ) -> dict[str, int]:
        return {"recorded": len(events)}


class _FakeClientDuplicateNames:
    def list_plugins_by_namespace(self, namespace: str):
        return [
            _plugin(id="p1", name="dup-plugin", namespace="org/a"),
            _plugin(id="p2", name="dup-plugin", namespace="org/a"),
        ]


class _FakeClientCodexSlugCollision(_FakeClientSinglePlugin):
    def list_plugins_by_namespace(self, namespace: str):
        return [
            _plugin(id="p1", name="My Plugin", namespace="org/a"),
            _plugin(id="p2", name="my_plugin", namespace="org/a"),
        ]


class _FakeClientCodexSlugCollisionWithInstalled(_FakeClientSinglePlugin):
    def list_plugins_by_namespace(self, namespace: str):
        return [_plugin(id="p2", name="my_plugin", namespace="org/repo")]


class _FakeClientApiInstallNameCollisionWithInstalled(_FakeClientSinglePlugin):
    def list_plugins_by_namespace(self, namespace: str):
        return [
            _plugin(
                id="p2",
                name="my_plugin",
                install_name="my-plugin",
                namespace="org/repo",
            )
        ]


class _FakeClientUpdateNewer:
    def get_plugin(self, plugin_id: str) -> PluginDetail:
        return _plugin(
            id=plugin_id,
            updated_at=datetime.datetime(2024, 2, 1, tzinfo=datetime.timezone.utc),
        )

    def get_skill(self, skill_id: str) -> SkillDetail:
        return SkillDetail(id=skill_id, name="test-skill", files=[])


class _FakeClientUpdateNewerWithApiInstallName(_FakeClientUpdateNewer):
    def get_plugin(self, plugin_id: str) -> PluginDetail:
        return _plugin(
            id=plugin_id,
            name="Display Plugin Name",
            install_name="api-plugin-name",
            updated_at=datetime.datetime(2024, 2, 1, tzinfo=datetime.timezone.utc),
        )


# -- Install tests --


@pytest.mark.asyncio
async def test_install_native_creates_file_structure(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    result = await install_plugins(
        client=_FakeClientSinglePlugin(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        host="https://example.com",
    )

    assert result.errors == []
    assert result.installed == ["my-plugin"]

    # Check file structure
    plugin_dir = canonical / "my-plugin"
    assert (plugin_dir / ".claude-plugin" / "plugin.json").exists()
    assert (plugin_dir / ".mcp.json").exists()
    assert (plugin_dir / ".installed").exists()
    manifest = json.loads((plugin_dir / ".claude-plugin" / "plugin.json").read_text())
    assert manifest["name"] == "my-plugin"
    assert manifest["mcpServers"]["my-server"]["type"] == "http"
    assert "proxy/srv-1/mcp" in manifest["mcpServers"]["my-server"]["url"]

    mcp = json.loads((plugin_dir / ".mcp.json").read_text())
    assert "mcpServers" in mcp
    for srv in mcp["mcpServers"].values():
        assert srv.get("type") == "http"

    # Check editor symlink
    assert (editor / "my-plugin").is_symlink()

    # Check lockfile
    entries = read_plugin_lockfile(lockfile)
    assert len(entries) == 1
    assert entries[0].name == "my-plugin"
    assert entries[0].install_mode == "native"


@pytest.mark.asyncio
async def test_install_vscode_mcp_json_and_skill_passthrough(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    result = await install_plugins(
        client=_FakeClientWithSkills(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="vscode",
        host="https://example.com",
    )

    assert result.errors == []
    plugin_dir = canonical / "my-plugin"
    assert (plugin_dir / ".mcp.json").exists()

    mcp = json.loads((plugin_dir / ".mcp.json").read_text())
    assert "mcpServers" in mcp
    for srv in mcp["mcpServers"].values():
        assert srv.get("type") == "http"

    skill_content = (plugin_dir / "skills" / "skill-one" / "SKILL.md").read_text()
    assert not skill_content.startswith("---\n")


@pytest.mark.asyncio
async def test_install_cursor_mcp_json_and_skill_passthrough(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    result = await install_plugins(
        client=_FakeClientWithSkills(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
    )

    assert result.errors == []
    plugin_dir = canonical / "my-plugin"
    assert (plugin_dir / ".mcp.json").exists()

    mcp = json.loads((plugin_dir / ".mcp.json").read_text())
    assert "mcpServers" in mcp
    for srv in mcp["mcpServers"].values():
        assert "type" not in srv

    skill_content = (plugin_dir / "skills" / "skill-one" / "SKILL.md").read_text()
    assert not skill_content.startswith("---\n")


@pytest.mark.asyncio
async def test_install_plugins_tracks_successful_installs(tmp_path: Path) -> None:
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"
    client = _FakeClientSinglePlugin()

    result = await install_plugins(
        client=client,
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
    )

    assert result.installed == ["my-plugin"]
    assert client.installation_events == [
        {
            "resource_type": "plugin",
            "resource_id": "p1",
            "client_name": "cursor",
            "install_scope": "project",
            "install_mode": "native",
        }
    ]


@pytest.mark.asyncio
async def test_install_plugins_ignores_tracking_failure(tmp_path: Path) -> None:
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    result = await install_plugins(
        client=_FakeClientTrackingFails(),
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
    )

    assert result.installed == ["my-plugin"]


@pytest.mark.asyncio
async def test_install_native_with_skills_downloads_files(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    result = await install_plugins(
        client=_FakeClientWithSkills(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        host="https://example.com",
    )

    assert result.errors == []
    assert result.installed == ["my-plugin"]
    skill_dir = canonical / "my-plugin" / "skills" / "skill-one"
    assert skill_dir.exists()
    assert (skill_dir / "SKILL.md").exists()
    skill_content = (skill_dir / "SKILL.md").read_text()
    assert skill_content.startswith("---\n")
    assert "name:" in skill_content


@pytest.mark.asyncio
async def test_install_claude_code_slugifies_plugin_and_skill_names(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    result = await install_plugins(
        client=_FakeClientCodexNamesWithSpaces(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        host="https://example.com",
    )

    assert result.errors == []
    plugin_dir = canonical / "my-plugin-name"
    manifest = json.loads((plugin_dir / ".claude-plugin" / "plugin.json").read_text())
    assert manifest["name"] == "my-plugin-name"
    assert manifest["mcpServers"]["my-server"]["type"] == "http"
    skill_file = plugin_dir / "skills" / "skill-name-with-spaces" / "SKILL.md"
    assert skill_file.exists()
    content = skill_file.read_text(encoding="utf-8")
    assert "name: skill-name-with-spaces" in content
    assert not (canonical / "My Plugin Name").exists()


@pytest.mark.asyncio
async def test_install_native_uses_api_plugin_install_name(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    result = await install_plugins(
        client=_FakeClientWithApiInstallName(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        host="https://example.com",
    )

    assert result.errors == []
    plugin_dir = canonical / "api-plugin-name"
    assert plugin_dir.exists()
    assert not (canonical / "display-plugin-name").exists()
    manifest = json.loads((plugin_dir / ".claude-plugin" / "plugin.json").read_text())
    assert manifest["name"] == "api-plugin-name"
    skill_file = plugin_dir / "skills" / "api-skill-name" / "SKILL.md"
    assert skill_file.exists()
    assert "name: api-skill-name" in skill_file.read_text(encoding="utf-8")

    entries = read_plugin_lockfile(lockfile)
    assert len(entries) == 1
    assert entries[0].name == "Display Plugin Name"
    assert entries[0].install_name == "api-plugin-name"


@pytest.mark.asyncio
async def test_install_claude_code_global_registers_marketplace_and_cache(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setattr(Path, "home", staticmethod(lambda: home))

    canonical = home / ".agents" / "plugins"
    editor = home / ".claude" / "plugins"
    lockfile = home / ".runlayer" / "plugin-lock.yml"

    result = await install_plugins(
        client=_FakeClientCodexNamesWithSpaces(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        host="https://example.com",
        install_scope="global",
    )

    assert result.errors == []
    cache_dir = home / ".claude/plugins/cache/runlayer/my-plugin-name/1.0.0"
    assert (cache_dir / ".claude-plugin" / "plugin.json").exists()
    assert (cache_dir / "skills" / "skill-name-with-spaces" / "SKILL.md").exists()

    installed = json.loads(
        (home / ".claude/plugins/installed_plugins.json").read_text()
    )
    assert installed["plugins"]["my-plugin-name@runlayer"][0]["installPath"] == str(
        cache_dir
    )

    settings = json.loads((home / ".claude/settings.json").read_text())
    assert settings["enabledPlugins"]["my-plugin-name@runlayer"] is True

    known = json.loads((home / ".claude/plugins/known_marketplaces.json").read_text())
    assert known["runlayer"]["source"] == {
        "source": "directory",
        "path": str(home / ".claude/plugins/marketplaces/runlayer"),
    }

    marketplace = json.loads(
        (
            home
            / ".claude/plugins/marketplaces/runlayer/.claude-plugin/marketplace.json"
        ).read_text()
    )
    assert marketplace["plugins"] == [
        {
            "name": "my-plugin-name",
            "description": "Runlayer plugin for My Plugin Name",
            "source": "./plugins/my-plugin-name",
            "category": "productivity",
        }
    ]


@pytest.mark.asyncio
async def test_install_codex_creates_project_marketplace_and_manifest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.chdir(tmp_path)
    canonical = tmp_path / ".agents" / "plugins"
    editor = canonical
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    result = await install_plugins(
        client=_FakeClientWithSkills(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="codex",
        host="https://example.com",
    )

    assert result.errors == []
    assert result.installed == ["my-plugin"]

    plugin_dir = canonical / "my-plugin"
    assert (plugin_dir / ".codex-plugin" / "plugin.json").exists()
    assert (plugin_dir / ".mcp.json").exists()
    assert (plugin_dir / ".installed").exists()
    assert not (editor / "my-plugin").is_symlink()

    mcp = json.loads((plugin_dir / ".mcp.json").read_text())
    assert "mcpServers" not in mcp
    assert "mcp_servers" in mcp
    for srv in mcp["mcp_servers"].values():
        assert "type" not in srv

    skill_dir = plugin_dir / "skills" / "skill-one"
    assert skill_dir.exists()
    skill_content = (skill_dir / "SKILL.md").read_text()
    assert skill_content.startswith("---\n")
    assert "name:" in skill_content

    manifest = json.loads((plugin_dir / ".codex-plugin" / "plugin.json").read_text())
    assert manifest["mcpServers"] == "./.mcp.json"

    marketplace = json.loads((canonical / "marketplace.json").read_text())
    assert marketplace["name"] == "runlayer-local"
    assert marketplace["plugins"] == [
        {
            "name": "my-plugin",
            "source": {
                "source": "local",
                "path": "./.agents/plugins/my-plugin",
            },
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Productivity",
        }
    ]

    entries = read_plugin_lockfile(lockfile)
    assert len(entries) == 1
    assert entries[0].install_mode == CODEX_NATIVE_INSTALL_MODE


@pytest.mark.asyncio
async def test_install_codex_creates_global_marketplace_entry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    home_dir = tmp_path / "home"
    project_dir = tmp_path / "project"
    home_dir.mkdir()
    project_dir.mkdir()
    monkeypatch.setenv("HOME", str(home_dir))
    monkeypatch.chdir(project_dir)

    canonical = home_dir / ".agents" / "plugins"
    editor = canonical
    lockfile = home_dir / ".runlayer" / "plugin-lock.yml"

    result = await install_plugins(
        client=_FakeClientWithSkills(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="codex",
        host="https://example.com",
    )

    assert result.errors == []
    marketplace = json.loads((canonical / "marketplace.json").read_text())
    assert marketplace["plugins"] == [
        {
            "name": "my-plugin",
            "source": {
                "source": "local",
                "path": "./.agents/plugins/my-plugin",
            },
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Productivity",
        }
    ]


@pytest.mark.asyncio
async def test_install_codex_normalizes_plugin_and_skill_names(
    tmp_path: Path,
):
    canonical = tmp_path / "canonical"
    editor = canonical
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    result = await install_plugins(
        client=_FakeClientCodexNamesWithSpaces(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="codex",
        host="https://example.com",
    )

    assert result.errors == []
    assert result.installed == ["My Plugin Name"]

    plugin_dir = canonical / "my-plugin-name"
    assert plugin_dir.exists()
    assert not (canonical / "My Plugin Name").exists()

    manifest = json.loads((plugin_dir / ".codex-plugin" / "plugin.json").read_text())
    assert manifest["name"] == "my-plugin-name"
    assert manifest["interface"] == {"displayName": "My Plugin Name"}

    skill_path = plugin_dir / "skills" / "skill-name-with-spaces" / "SKILL.md"
    assert skill_path.exists()
    skill_content = skill_path.read_text(encoding="utf-8")
    assert "name: skill-name-with-spaces" in skill_content
    assert "name: Skill Name With Spaces" not in skill_content

    marketplace = json.loads((canonical / "marketplace.json").read_text())
    assert marketplace["plugins"] == [
        {
            "name": "my-plugin-name",
            "source": {
                "source": "local",
                "path": "./.agents/plugins/my-plugin-name",
            },
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Productivity",
        }
    ]

    entries = read_plugin_lockfile(lockfile)
    assert len(entries) == 1
    assert entries[0].name == "My Plugin Name"
    assert entries[0].install_name == "my-plugin-name"


@pytest.mark.asyncio
async def test_install_codex_preserves_unrelated_marketplace_entries(
    tmp_path: Path,
):
    canonical = tmp_path / "canonical"
    editor = canonical
    lockfile = tmp_path / "lock" / "plugin-lock.yml"
    canonical.mkdir(parents=True)
    (canonical / "marketplace.json").write_text(
        json.dumps(
            {
                "name": "custom-market",
                "plugins": [
                    {
                        "name": "existing-plugin",
                        "source": {
                            "source": "local",
                            "path": "./plugins/existing-plugin",
                        },
                        "policy": {
                            "installation": "AVAILABLE",
                            "authentication": "ON_INSTALL",
                        },
                        "category": "Productivity",
                    },
                    "non-standard-entry",
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    result = await install_plugins(
        client=_FakeClientSinglePlugin(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="codex",
        host="https://example.com",
    )

    assert result.errors == []
    marketplace = json.loads((canonical / "marketplace.json").read_text())
    assert marketplace["name"] == "custom-market"
    assert marketplace["plugins"] == [
        {
            "name": "existing-plugin",
            "source": {
                "source": "local",
                "path": "./plugins/existing-plugin",
            },
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Productivity",
        },
        "non-standard-entry",
        {
            "name": "my-plugin",
            "source": {
                "source": "local",
                "path": "./.agents/plugins/my-plugin",
            },
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Productivity",
        },
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize("dry_run", [False, True])
async def test_install_all_accessible(tmp_path: Path, dry_run: bool):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    result = await install_plugins(
        client=_FakeClientAllAccessible(),  # type: ignore
        source=None,
        install_all=True,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        host="https://example.com",
        dry_run=dry_run,
    )

    assert result.errors == []
    assert result.installed == ["plugin-one", "plugin-two"]
    if dry_run:
        assert not lockfile.exists()
        assert not (editor / "plugin-one").exists()
    else:
        assert (editor / "plugin-one").is_symlink()
        assert (editor / "plugin-two").is_symlink()


@pytest.mark.asyncio
async def test_install_skips_already_locked(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"
    _write_plugin_lockfile(lockfile, [_lock_entry()])

    result = await install_plugins(
        client=_FakeClientSinglePlugin(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        host="https://example.com",
    )

    assert result.skipped == ["my-plugin"]
    assert result.installed == []


@pytest.mark.asyncio
async def test_install_collision_error(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    result = await install_plugins(
        client=_FakeClientDuplicateNames(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        host="https://example.com",
    )

    assert result.installed == []
    assert result.errors
    assert "multiple plugins named 'dup-plugin'" in result.errors[0]


@pytest.mark.asyncio
async def test_install_codex_slug_collision_error(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = canonical
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    result = await install_plugins(
        client=_FakeClientCodexSlugCollision(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="codex",
        host="https://example.com",
    )

    assert result.installed == []
    assert result.errors
    assert "multiple plugins resolve to install name 'my-plugin'" in result.errors[0]


@pytest.mark.asyncio
async def test_install_codex_slug_conflict_with_existing_lock_entry(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = canonical
    lockfile = tmp_path / "lock" / "plugin-lock.yml"
    _write_plugin_lockfile(
        lockfile,
        [
            PluginLockEntry(
                name="My Plugin",
                id="p1",
                install_name="my-plugin",
                namespace="org/repo",
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
                client="codex",
                install_mode=CODEX_NATIVE_INSTALL_MODE,
                server_ids=["srv-1"],
            )
        ],
    )

    result = await install_plugins(
        client=_FakeClientCodexSlugCollisionWithInstalled(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="codex",
        host="https://example.com",
    )

    assert result.installed == []
    assert result.errors
    assert "install name conflict for 'my_plugin'" in result.errors[0]


@pytest.mark.asyncio
async def test_install_detects_api_install_name_conflict_with_legacy_lock_entry(
    tmp_path: Path,
):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"
    _write_plugin_lockfile(
        lockfile,
        [
            PluginLockEntry(
                name="My Plugin",
                id="p1",
                namespace="org/repo",
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
                client="cursor",
                install_mode="native",
                server_ids=["srv-1"],
            )
        ],
    )

    result = await install_plugins(
        client=_FakeClientApiInstallNameCollisionWithInstalled(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
    )

    assert result.installed == []
    assert result.errors
    assert "install name conflict for 'my_plugin'" in result.errors[0]


# -- Remove tests --


def _setup_installed_plugin(
    tmp_path: Path,
) -> tuple[Path, Path, Path]:
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    plugin_dir = canonical / "my-plugin"
    plugin_dir.mkdir(parents=True)
    (plugin_dir / ".installed").write_text("", encoding="utf-8")
    link = editor / "my-plugin"
    link.parent.mkdir(parents=True)
    link.symlink_to(plugin_dir)
    _write_plugin_lockfile(lockfile, [_lock_entry()])

    return canonical, editor, lockfile


def _setup_installed_plugin_with_invalid_display_name(
    tmp_path: Path,
    *,
    client: str = "claude_code",
    install_mode: str = "native",
) -> tuple[Path, Path, Path]:
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    plugin_dir = canonical / "plugin-p1"
    plugin_dir.mkdir(parents=True)
    (plugin_dir / ".installed").write_text("", encoding="utf-8")
    link = editor / "plugin-p1"
    link.parent.mkdir(parents=True)
    link.symlink_to(plugin_dir)
    _write_plugin_lockfile(
        lockfile,
        [
            PluginLockEntry(
                name="!!!",
                id="p1",
                install_name="plugin-p1",
                namespace="org/repo",
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
                client=client,
                install_mode=install_mode,
                server_ids=["srv-1"],
            )
        ],
    )

    return canonical, editor, lockfile


@pytest.mark.asyncio
async def test_uninstall_removes_files_and_lockfile_entry(tmp_path: Path):
    canonical, editor, lockfile = _setup_installed_plugin(tmp_path)

    await uninstall_plugin("my-plugin", canonical, editor, lockfile, "claude_code")

    assert not (canonical / "my-plugin").exists()
    assert not (editor / "my-plugin").exists()
    entries = read_plugin_lockfile(lockfile)
    assert entries == []


@pytest.mark.asyncio
async def test_uninstall_by_uuid_removes_files_and_lockfile_entry(tmp_path: Path):
    canonical, editor, lockfile = _setup_installed_plugin(tmp_path)
    uuid_id = "11111111-1111-1111-1111-111111111111"
    _write_plugin_lockfile(
        lockfile,
        [
            PluginLockEntry(
                name="my-plugin",
                id=uuid_id,
                namespace="org/repo",
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
                client="claude_code",
                install_mode="native",
                server_ids=["srv-1"],
            )
        ],
    )

    removed_name = await uninstall_plugin(
        uuid_id, canonical, editor, lockfile, "claude_code"
    )

    assert removed_name == "my-plugin"
    assert not (canonical / "my-plugin").exists()
    assert not (editor / "my-plugin").exists()
    entries = read_plugin_lockfile(lockfile)
    assert entries == []


@pytest.mark.asyncio
async def test_uninstall_codex_uses_normalized_install_name(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = canonical
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    plugin_dir = canonical / "my-plugin-name"
    plugin_dir.mkdir(parents=True)
    (plugin_dir / ".installed").write_text("", encoding="utf-8")
    (canonical / "marketplace.json").write_text(
        json.dumps(
            {
                "name": "runlayer-local",
                "plugins": [
                    {
                        "name": "my-plugin-name",
                        "source": {
                            "source": "local",
                            "path": "./.agents/plugins/my-plugin-name",
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    _write_plugin_lockfile(
        lockfile,
        [
            PluginLockEntry(
                name="My Plugin Name",
                id="p1",
                install_name="my-plugin-name",
                namespace="org/repo",
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
                client="codex",
                install_mode=CODEX_NATIVE_INSTALL_MODE,
            )
        ],
    )

    removed_name = await uninstall_plugin(
        "My Plugin Name", canonical, editor, lockfile, "codex"
    )

    assert removed_name == "My Plugin Name"
    assert not plugin_dir.exists()
    marketplace = json.loads((canonical / "marketplace.json").read_text())
    assert marketplace["plugins"] == []
    assert read_plugin_lockfile(lockfile) == []


@pytest.mark.asyncio
async def test_uninstall_handles_invalid_display_name_with_api_install_name(
    tmp_path: Path,
):
    canonical, editor, lockfile = _setup_installed_plugin_with_invalid_display_name(
        tmp_path
    )

    removed_name = await uninstall_plugin(
        "!!!", canonical, editor, lockfile, "claude_code"
    )

    assert removed_name == "!!!"
    assert not (canonical / "plugin-p1").exists()
    assert not (editor / "plugin-p1").exists()
    assert read_plugin_lockfile(lockfile) == []


@pytest.mark.asyncio
async def test_uninstall_not_found_raises(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"
    _write_plugin_lockfile(lockfile, [_lock_entry()])

    with pytest.raises(ValueError, match="not found in lockfile"):
        await uninstall_plugin(
            "nonexistent", canonical, editor, lockfile, "claude_code"
        )


# -- Update tests --


@pytest.mark.asyncio
@pytest.mark.parametrize("dry_run", [False, True])
async def test_update_404_removes(tmp_path: Path, dry_run: bool):
    canonical, editor, lockfile = _setup_installed_plugin(tmp_path)
    plugin_dir = canonical / "my-plugin"

    result = await update_plugins(
        client=_FakeClient404(),  # type: ignore
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        host="https://example.com",
        dry_run=dry_run,
    )

    assert result.removed == ["my-plugin"]
    if dry_run:
        assert plugin_dir.exists()
    else:
        assert not plugin_dir.exists()


@pytest.mark.asyncio
async def test_update_404_handles_invalid_display_name_with_api_install_name(
    tmp_path: Path,
):
    canonical, editor, lockfile = _setup_installed_plugin_with_invalid_display_name(
        tmp_path
    )

    result = await update_plugins(
        client=_FakeClient404(),  # type: ignore
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        host="https://example.com",
    )

    assert result.errors == []
    assert result.removed == ["!!!"]
    assert not (canonical / "plugin-p1").exists()


@pytest.mark.asyncio
async def test_update_up_to_date(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"
    _write_plugin_lockfile(
        lockfile,
        [
            PluginLockEntry(
                name="my-plugin",
                id="p1",
                namespace="org/repo",
                updated_at=datetime.datetime(2024, 3, 1, tzinfo=datetime.timezone.utc),
                client="claude_code",
                install_mode="native",
            )
        ],
    )

    result = await update_plugins(
        client=_FakeClientUpdateNewer(),  # type: ignore
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        host="https://example.com",
    )

    assert result.up_to_date == ["my-plugin"]


@pytest.mark.asyncio
async def test_update_newer_refreshes(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"
    _write_plugin_lockfile(lockfile, [_lock_entry()])

    result = await update_plugins(
        client=_FakeClientUpdateNewer(),  # type: ignore
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        host="https://example.com",
    )

    assert result.updated == ["my-plugin"]
    entries = read_plugin_lockfile(lockfile)
    assert entries[0].updated_at == datetime.datetime(
        2024, 2, 1, tzinfo=datetime.timezone.utc
    )


@pytest.mark.asyncio
async def test_update_newer_refreshes_install_name_from_api(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "plugin-lock.yml"
    _write_plugin_lockfile(lockfile, [_lock_entry("Display Plugin Name")])

    result = await update_plugins(
        client=_FakeClientUpdateNewerWithApiInstallName(),  # type: ignore
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        host="https://example.com",
    )

    assert result.updated == ["Display Plugin Name"]
    assert (canonical / "api-plugin-name").exists()
    entries = read_plugin_lockfile(lockfile)
    assert entries[0].install_name == "api-plugin-name"


@pytest.mark.asyncio
async def test_update_claude_code_global_preserves_installed_at(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    canonical = home / ".agents" / "plugins"
    editor = home / ".claude" / "plugins"
    lockfile = home / ".runlayer" / "plugin-lock.yml"
    _write_plugin_lockfile(lockfile, [_lock_entry()])

    installed_at = "2024-01-01T00:00:00Z"
    registry_path = home / ".claude" / "plugins" / "installed_plugins.json"
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(
        json.dumps(
            {
                "version": 2,
                "plugins": {
                    "my-plugin@runlayer": [
                        {
                            "scope": "user",
                            "installPath": "old-cache",
                            "installedAt": installed_at,
                            "lastUpdated": "2024-01-02T00:00:00Z",
                            "version": "1.0.0",
                        }
                    ]
                },
            }
        ),
        encoding="utf-8",
    )

    result = await update_plugins(
        client=_FakeClientUpdateNewer(),  # type: ignore
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        host="https://example.com",
        install_scope="global",
    )

    assert result.updated == ["my-plugin"]
    registry = json.loads(registry_path.read_text())
    entry = registry["plugins"]["my-plugin@runlayer"][0]
    assert entry["installedAt"] == installed_at
    assert entry["lastUpdated"] != installed_at


@pytest.mark.asyncio
async def test_update_traversal_name_rejected(tmp_path: Path):
    canonical = tmp_path / "canonical"
    canonical.mkdir()
    editor = tmp_path / "editor"
    editor.mkdir()
    lockfile = tmp_path / "lock" / "plugin-lock.yml"

    target = tmp_path / "precious"
    target.mkdir()
    (target / "data.txt").write_text("important")

    _write_plugin_lockfile(lockfile, [_lock_entry("../../precious")])
    result = await update_plugins(
        client=_FakeClient404(),  # type: ignore
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        host="https://example.com",
    )

    assert result.errors
    assert target.exists()
