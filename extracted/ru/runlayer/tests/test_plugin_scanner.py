"""Tests for plugin artifact detection (plugin_scanner.py)."""

import json
from pathlib import Path

import pytest

from runlayer_cli.scan.claude_code_plugins import scan_claude_code_plugins
from runlayer_cli.scan.codex_plugins import scan_codex_plugins
from runlayer_cli.scan.clients import (
    MCPClientDefinition,
    ConfigPath,
    PluginPath,
)
from runlayer_cli.scan.cursor_plugins import scan_cursor_plugins
from runlayer_cli.scan.plugin_scanner import (
    _collect_plugin_files,
    compute_plugin_identifier,
    scan_claude_code_plugin_artifacts,
    scan_claude_desktop_connectors,
    scan_codex_plugin_artifacts,
    scan_cursor_native_plugins,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_installed_plugins(base: Path, plugins: dict) -> Path:
    path = base / ".claude" / "plugins" / "installed_plugins.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"version": 2, "plugins": plugins}))
    return path


def _create_cursor_plugin(
    cache_base: Path,
    name: str,
    commit: str = "abc123",
    plugin_json: dict | None = None,
    mcp_json: dict | None = None,
) -> Path:
    plugin_dir = cache_base / name / commit
    plugin_dir.mkdir(parents=True, exist_ok=True)
    if plugin_json is not None:
        manifest_dir = plugin_dir / ".cursor-plugin"
        manifest_dir.mkdir(exist_ok=True)
        (manifest_dir / "plugin.json").write_text(json.dumps(plugin_json))
    if mcp_json is not None:
        (plugin_dir / "mcp.json").write_text(json.dumps(mcp_json))
    return plugin_dir


def _create_claude_plugin(
    base: Path,
    marketplace: str,
    name: str,
    version: str,
    plugin_json: dict | None = None,
    mcp_json: dict | None = None,
    extra_dirs: list[str] | None = None,
) -> str:
    plugin_dir = base / ".claude" / "plugins" / "cache" / marketplace / name / version
    plugin_dir.mkdir(parents=True, exist_ok=True)
    if plugin_json is not None:
        manifest_dir = plugin_dir / ".claude-plugin"
        manifest_dir.mkdir(exist_ok=True)
        (manifest_dir / "plugin.json").write_text(json.dumps(plugin_json))
    if mcp_json is not None:
        (plugin_dir / ".mcp.json").write_text(json.dumps(mcp_json))
    for d in extra_dirs or []:
        (plugin_dir / d).mkdir(exist_ok=True)
    return str(plugin_dir)


# ===========================================================================
# compute_plugin_identifier
# ===========================================================================


class TestComputePluginIdentifier:
    def test_returns_none_for_empty_dir(self, tmp_path: Path):
        assert compute_plugin_identifier(tmp_path) is None

    def test_hashes_manifest(self, tmp_path: Path):
        manifest_dir = tmp_path / ".cursor-plugin"
        manifest_dir.mkdir()
        (manifest_dir / "plugin.json").write_text(
            json.dumps({"name": "test", "version": "1.0.0"})
        )
        result = compute_plugin_identifier(tmp_path)
        assert result is not None
        assert len(result) == 64

    def test_deterministic(self, tmp_path: Path):
        manifest_dir = tmp_path / ".claude-plugin"
        manifest_dir.mkdir()
        (manifest_dir / "plugin.json").write_text(
            json.dumps({"name": "test", "version": "1.0.0"})
        )
        a = compute_plugin_identifier(tmp_path)
        b = compute_plugin_identifier(tmp_path)
        assert a == b

    def test_different_content_different_hash(self, tmp_path: Path):
        dir_a = tmp_path / "a"
        dir_b = tmp_path / "b"
        for d, version in [(dir_a, "1.0.0"), (dir_b, "2.0.0")]:
            m = d / ".cursor-plugin"
            m.mkdir(parents=True)
            (m / "plugin.json").write_text(
                json.dumps({"name": "test", "version": version})
            )
        assert compute_plugin_identifier(dir_a) != compute_plugin_identifier(dir_b)


# ===========================================================================
# scan_cursor_native_plugins
# ===========================================================================


class TestScanCursorNativePlugins:
    def test_empty_cache(self, tmp_path: Path):
        tmp_path.mkdir(exist_ok=True)
        assert scan_cursor_native_plugins(plugin_cache_base=tmp_path) == []

    def test_nonexistent_cache(self, tmp_path: Path):
        assert (
            scan_cursor_native_plugins(plugin_cache_base=tmp_path / "nonexistent") == []
        )

    def test_plugin_without_manifest(self, tmp_path: Path):
        plugin_dir = tmp_path / "no-manifest" / "abc123"
        plugin_dir.mkdir(parents=True)
        assert scan_cursor_native_plugins(plugin_cache_base=tmp_path) == []

    def test_discovers_plugin(self, tmp_path: Path):
        _create_cursor_plugin(
            tmp_path,
            "my-plugin",
            plugin_json={
                "name": "my-plugin",
                "version": "1.0.0",
                "description": "A test plugin",
                "author": {"name": "Test Author"},
            },
        )
        result = scan_cursor_native_plugins(plugin_cache_base=tmp_path)
        assert len(result) == 1
        p = result[0]
        assert p.name == "my-plugin"
        assert p.version == "1.0.0"
        assert p.description == "A test plugin"
        assert p.author == "Test Author"
        assert p.plugin_type == "cursor_plugin"
        assert p.client == "cursor"
        assert p.marketplace == "cursor-public"
        assert p.identifier is not None

    def test_plugin_with_mcp_servers(self, tmp_path: Path):
        _create_cursor_plugin(
            tmp_path,
            "with-mcp",
            plugin_json={"name": "with-mcp", "version": "1.0.0"},
            mcp_json={"mcpServers": {"server1": {"command": "node"}}},
        )
        result = scan_cursor_native_plugins(plugin_cache_base=tmp_path)
        assert len(result) == 1
        assert result[0].has_mcp_servers is True
        assert len(result[0].mcp_servers) == 1
        assert result[0].mcp_servers[0].name == "server1"
        assert result[0].mcp_servers[0].type == "stdio"

    def test_plugin_mcp_type_http_preserved(self, tmp_path: Path):
        _create_cursor_plugin(
            tmp_path,
            "with-http-mcp",
            plugin_json={"name": "with-http-mcp", "version": "1.0.0"},
            mcp_json={
                "mcpServers": {
                    "server1": {
                        "type": "http",
                        "url": "https://example.com/mcp",
                    }
                }
            },
        )
        result = scan_cursor_native_plugins(plugin_cache_base=tmp_path)
        assert len(result) == 1
        assert len(result[0].mcp_servers) == 1
        assert result[0].mcp_servers[0].type == "http"
        assert result[0].mcp_servers[0].url == "https://example.com/mcp"

    def test_plugin_mcp_server_url_defaults_to_sse(self, tmp_path: Path):
        _create_cursor_plugin(
            tmp_path,
            "with-server-url",
            plugin_json={"name": "with-server-url", "version": "1.0.0"},
            mcp_json={
                "mcpServers": {"server1": {"serverUrl": "https://example.com/mcp"}}
            },
        )
        result = scan_cursor_native_plugins(plugin_cache_base=tmp_path)
        assert len(result) == 1
        assert len(result[0].mcp_servers) == 1
        assert result[0].mcp_servers[0].type == "sse"
        assert result[0].mcp_servers[0].url == "https://example.com/mcp"

    def test_plugin_mcp_transport_streamable_http_normalized(self, tmp_path: Path):
        _create_cursor_plugin(
            tmp_path,
            "with-streamable-http",
            plugin_json={"name": "with-streamable-http", "version": "1.0.0"},
            mcp_json={
                "mcpServers": {
                    "server1": {
                        "transport": "streamable_http",
                        "url": "https://example.com/mcp",
                    }
                }
            },
        )
        result = scan_cursor_native_plugins(plugin_cache_base=tmp_path)
        assert len(result) == 1
        assert len(result[0].mcp_servers) == 1
        assert result[0].mcp_servers[0].type == "streamable-http"
        assert result[0].mcp_servers[0].url == "https://example.com/mcp"

    def test_multiple_plugins(self, tmp_path: Path):
        _create_cursor_plugin(
            tmp_path,
            "plugin-a",
            plugin_json={"name": "plugin-a", "version": "1.0.0"},
        )
        _create_cursor_plugin(
            tmp_path,
            "plugin-b",
            plugin_json={"name": "plugin-b", "version": "2.0.0"},
        )
        result = scan_cursor_native_plugins(plugin_cache_base=tmp_path)
        assert len(result) == 2
        names = {p.name for p in result}
        assert names == {"plugin-a", "plugin-b"}

    def test_uses_first_hash_dir(self, tmp_path: Path):
        _create_cursor_plugin(
            tmp_path,
            "my-plugin",
            commit="aaa111",
            plugin_json={"name": "v1", "version": "1.0.0"},
        )
        _create_cursor_plugin(
            tmp_path,
            "my-plugin",
            commit="bbb222",
            plugin_json={"name": "v2", "version": "2.0.0"},
        )
        result = scan_cursor_native_plugins(plugin_cache_base=tmp_path)
        assert len(result) == 1

    def test_enabled_from_settings(self, tmp_path: Path):
        _create_cursor_plugin(
            tmp_path,
            "slack",
            plugin_json={"name": "slack", "version": "1.0.0"},
        )
        result = scan_cursor_native_plugins(
            plugin_cache_base=tmp_path,
            settings_override={"slack@cursor-public": True},
        )
        assert result[0].enabled is True

    def test_disabled_from_settings(self, tmp_path: Path):
        _create_cursor_plugin(
            tmp_path,
            "slack",
            plugin_json={"name": "slack", "version": "1.0.0"},
        )
        result = scan_cursor_native_plugins(
            plugin_cache_base=tmp_path,
            settings_override={"slack@cursor-public": False},
        )
        assert result[0].enabled is False

    def test_enabled_none_when_not_in_settings(self, tmp_path: Path):
        _create_cursor_plugin(
            tmp_path,
            "unknown",
            plugin_json={"name": "unknown", "version": "1.0.0"},
        )
        result = scan_cursor_native_plugins(
            plugin_cache_base=tmp_path, settings_override={}
        )
        assert result[0].enabled is None

    def test_reads_cursor_settings_not_claude(self, tmp_path: Path, monkeypatch):
        """Without settings_override, reads ~/.cursor/settings.json."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", staticmethod(lambda: fake_home))

        cursor_settings = fake_home / ".cursor" / "settings.json"
        cursor_settings.parent.mkdir(parents=True)
        cursor_settings.write_text(
            json.dumps({"enabledPlugins": {"slack@cursor-public": True}})
        )

        claude_settings = fake_home / ".claude" / "settings.json"
        claude_settings.parent.mkdir(parents=True)
        claude_settings.write_text(
            json.dumps({"enabledPlugins": {"slack@cursor-public": False}})
        )

        _create_cursor_plugin(
            tmp_path / "cache",
            "slack",
            plugin_json={"name": "slack", "version": "1.0.0"},
        )
        result = scan_cursor_native_plugins(plugin_cache_base=tmp_path / "cache")
        assert result[0].enabled is True

    def test_to_api_payload(self, tmp_path: Path):
        _create_cursor_plugin(
            tmp_path,
            "test",
            plugin_json={"name": "test", "version": "1.0.0"},
        )
        result = scan_cursor_native_plugins(plugin_cache_base=tmp_path)
        payload = result[0].to_api_payload()
        assert payload["name"] == "test"
        assert payload["plugin_type"] == "cursor_plugin"
        assert payload["client"] == "cursor"
        assert isinstance(payload["mcp_servers"], list)


# ===========================================================================
# scan_claude_code_plugin_artifacts
# ===========================================================================


class TestScanClaudeCodePluginArtifacts:
    def test_no_registry(self, tmp_path: Path):
        assert (
            scan_claude_code_plugin_artifacts(
                installed_plugins_path=tmp_path / "nonexistent.json"
            )
            == []
        )

    def test_empty_registry(self, tmp_path: Path):
        path = _write_installed_plugins(tmp_path, {})
        assert scan_claude_code_plugin_artifacts(installed_plugins_path=path) == []

    def test_plugin_without_claude_manifest(self, tmp_path: Path):
        plugin_dir = tmp_path / "no-manifest"
        plugin_dir.mkdir()
        installed = _write_installed_plugins(
            tmp_path,
            {"no-manifest@official": [{"installPath": str(plugin_dir)}]},
        )
        assert scan_claude_code_plugin_artifacts(installed_plugins_path=installed) == []

    def test_discovers_plugin(self, tmp_path: Path):
        install_path = _create_claude_plugin(
            tmp_path,
            "official",
            "my-plugin",
            "v1",
            plugin_json={
                "name": "my-plugin",
                "version": "1.0.0",
                "description": "Test",
                "author": {"name": "Author"},
            },
        )
        installed = _write_installed_plugins(
            tmp_path,
            {
                "my-plugin@official": [
                    {
                        "installPath": install_path,
                        "scope": "user",
                        "version": "1.0.0",
                        "installedAt": "2025-12-18T19:21:27.666Z",
                        "lastUpdated": "2025-12-30T01:04:49.036Z",
                    }
                ]
            },
        )
        result = scan_claude_code_plugin_artifacts(installed_plugins_path=installed)
        assert len(result) == 1
        p = result[0]
        assert p.name == "my-plugin"
        assert p.version == "1.0.0"
        assert p.description == "Test"
        assert p.author == "Author"
        assert p.plugin_type == "claude_code_plugin"
        assert p.client == "claude_code"
        assert p.marketplace == "official"
        assert p.scope == "user"
        assert p.installed_at == "2025-12-18T19:21:27.666Z"
        assert p.last_updated == "2025-12-30T01:04:49.036Z"
        assert p.identifier is not None

    def test_plugin_with_mcp_and_components(self, tmp_path: Path):
        install_path = _create_claude_plugin(
            tmp_path,
            "official",
            "full",
            "v1",
            plugin_json={"name": "full", "version": "1.0.0"},
            mcp_json={"mcpServers": {"db": {"command": "db-server"}}},
            extra_dirs=["skills", "commands", "hooks"],
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"full@official": [{"installPath": install_path, "scope": "user"}]},
        )
        result = scan_claude_code_plugin_artifacts(installed_plugins_path=installed)
        assert len(result) == 1
        p = result[0]
        assert p.has_mcp_servers is True
        assert p.has_skills is True
        assert p.has_commands is True
        assert p.has_hooks is True
        assert p.has_rules is False
        assert len(p.mcp_servers) == 1
        assert p.mcp_servers[0].name == "db"

    def test_multiple_plugins(self, tmp_path: Path):
        path_a = _create_claude_plugin(
            tmp_path,
            "official",
            "plugin-a",
            "v1",
            plugin_json={"name": "plugin-a", "version": "1.0.0"},
        )
        path_b = _create_claude_plugin(
            tmp_path,
            "official",
            "plugin-b",
            "v1",
            plugin_json={"name": "plugin-b", "version": "2.0.0"},
        )
        installed = _write_installed_plugins(
            tmp_path,
            {
                "plugin-a@official": [{"installPath": path_a, "scope": "user"}],
                "plugin-b@official": [{"installPath": path_b, "scope": "user"}],
            },
        )
        result = scan_claude_code_plugin_artifacts(installed_plugins_path=installed)
        assert len(result) == 2
        names = {p.name for p in result}
        assert names == {"plugin-a", "plugin-b"}

    def test_enabled_from_settings(self, tmp_path: Path):
        install_path = _create_claude_plugin(
            tmp_path,
            "official",
            "review",
            "v1",
            plugin_json={"name": "review", "version": "1.0.0"},
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"review@official": [{"installPath": install_path, "scope": "user"}]},
        )
        result = scan_claude_code_plugin_artifacts(
            installed_plugins_path=installed,
            settings_override={"review@official": True},
        )
        assert result[0].enabled is True

    def test_project_scope(self, tmp_path: Path):
        install_path = _create_claude_plugin(
            tmp_path,
            "official",
            "proj",
            "v1",
            plugin_json={"name": "proj", "version": "1.0.0"},
        )
        installed = _write_installed_plugins(
            tmp_path,
            {
                "proj@official": [
                    {
                        "installPath": install_path,
                        "scope": "project",
                        "projectPath": "/home/user/myproject",
                    }
                ]
            },
        )
        result = scan_claude_code_plugin_artifacts(installed_plugins_path=installed)
        assert len(result) == 1
        assert result[0].scope == "project"
        assert result[0].project_path == "/home/user/myproject"

    def test_missing_install_path_skipped(self, tmp_path: Path):
        installed = _write_installed_plugins(
            tmp_path,
            {
                "gone@official": [
                    {"installPath": str(tmp_path / "nonexistent"), "scope": "user"}
                ]
            },
        )
        assert scan_claude_code_plugin_artifacts(installed_plugins_path=installed) == []

    def test_reads_claude_settings_not_cursor(self, tmp_path: Path, monkeypatch):
        """Without settings_override, reads ~/.claude/settings.json."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", staticmethod(lambda: fake_home))

        claude_settings = fake_home / ".claude" / "settings.json"
        claude_settings.parent.mkdir(parents=True)
        claude_settings.write_text(
            json.dumps({"enabledPlugins": {"review@official": True}})
        )

        cursor_settings = fake_home / ".cursor" / "settings.json"
        cursor_settings.parent.mkdir(parents=True)
        cursor_settings.write_text(
            json.dumps({"enabledPlugins": {"review@official": False}})
        )

        install_path = _create_claude_plugin(
            tmp_path,
            "official",
            "review",
            "v1",
            plugin_json={"name": "review", "version": "1.0.0"},
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"review@official": [{"installPath": install_path, "scope": "user"}]},
        )
        result = scan_claude_code_plugin_artifacts(installed_plugins_path=installed)
        assert result[0].enabled is True


# ===========================================================================
# scan_claude_desktop_connectors
# ===========================================================================


class TestScanClaudeDesktopConnectors:
    def test_no_config_file(self, tmp_path: Path):
        assert (
            scan_claude_desktop_connectors(
                config_path_override=tmp_path / "nonexistent.json"
            )
            == []
        )

    def test_empty_mcp_servers(self, tmp_path: Path):
        config = tmp_path / "claude_desktop_config.json"
        config.write_text(json.dumps({"mcpServers": {}}))
        assert scan_claude_desktop_connectors(config_path_override=config) == []

    def test_no_mcp_servers_key(self, tmp_path: Path):
        config = tmp_path / "claude_desktop_config.json"
        config.write_text(json.dumps({"other": "data"}))
        assert scan_claude_desktop_connectors(config_path_override=config) == []

    def test_discovers_stdio_connector(self, tmp_path: Path):
        config = tmp_path / "claude_desktop_config.json"
        config.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "filesystem": {
                            "command": "npx",
                            "args": ["-y", "@mcp/server-filesystem", "/tmp"],
                        }
                    }
                }
            )
        )
        result = scan_claude_desktop_connectors(config_path_override=config)
        assert len(result) == 1
        p = result[0]
        assert p.name == "filesystem"
        assert p.plugin_type == "claude_desktop_connector"
        assert p.client == "claude_desktop"
        assert p.scope == "global"
        assert p.has_mcp_servers is True
        assert p.install_path == str(config)
        assert len(p.mcp_servers) == 1
        assert p.mcp_servers[0].name == "filesystem"
        assert p.mcp_servers[0].type == "stdio"
        assert p.mcp_servers[0].command == "npx"
        assert p.identifier is not None

    def test_discovers_http_connector(self, tmp_path: Path):
        config = tmp_path / "claude_desktop_config.json"
        config.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "github": {
                            "url": "https://api.github.com/mcp",
                            "transport": "http",
                        }
                    }
                }
            )
        )
        result = scan_claude_desktop_connectors(config_path_override=config)
        assert len(result) == 1
        assert result[0].mcp_servers[0].type == "http"
        assert result[0].mcp_servers[0].url == "https://api.github.com/mcp"

    def test_multiple_connectors(self, tmp_path: Path):
        config = tmp_path / "claude_desktop_config.json"
        config.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "fs": {"command": "npx", "args": ["fs-server"]},
                        "db": {"command": "npx", "args": ["db-server"]},
                    }
                }
            )
        )
        result = scan_claude_desktop_connectors(config_path_override=config)
        assert len(result) == 2
        names = {p.name for p in result}
        assert names == {"fs", "db"}

    def test_connector_identifier_deterministic(self, tmp_path: Path):
        config = tmp_path / "claude_desktop_config.json"
        config.write_text(
            json.dumps({"mcpServers": {"srv": {"command": "echo", "args": ["hello"]}}})
        )
        r1 = scan_claude_desktop_connectors(config_path_override=config)
        r2 = scan_claude_desktop_connectors(config_path_override=config)
        assert r1[0].identifier == r2[0].identifier

    def test_to_api_payload(self, tmp_path: Path):
        config = tmp_path / "claude_desktop_config.json"
        config.write_text(json.dumps({"mcpServers": {"srv": {"command": "echo"}}}))
        result = scan_claude_desktop_connectors(config_path_override=config)
        payload = result[0].to_api_payload()
        assert payload["name"] == "srv"
        assert payload["plugin_type"] == "claude_desktop_connector"
        assert payload["client"] == "claude_desktop"
        assert len(payload["mcp_servers"]) == 1
        assert payload["mcp_servers"][0]["name"] == "srv"

    def test_malformed_json_skipped(self, tmp_path: Path):
        config = tmp_path / "claude_desktop_config.json"
        config.write_text("{invalid json")
        assert scan_claude_desktop_connectors(config_path_override=config) == []


# ===========================================================================
# Integration: plugin_identifier on MCPClientConfig
# ===========================================================================


class TestPluginIdentifierOnMCPClientConfig:
    def test_cursor_plugin_mcp_config_has_identifier(self, tmp_path: Path):
        base = tmp_path / "plugins"
        plugin_dir = base / "test-plugin" / "abc123"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "mcp.json").write_text(
            json.dumps({"mcpServers": {"s": {"command": "echo"}}})
        )
        manifest_dir = plugin_dir / ".cursor-plugin"
        manifest_dir.mkdir()
        (manifest_dir / "plugin.json").write_text(
            json.dumps({"name": "test-plugin", "version": "1.0.0"})
        )

        client = MCPClientDefinition(
            name="cursor",
            display_name="Cursor",
            paths=[ConfigPath(str(base / "mcp.json"), platform="all")],
            servers_key="mcpServers",
            plugin_paths=[PluginPath(str(base), platform="all")],
        )
        result = scan_cursor_plugins(client)
        assert len(result) == 1
        assert result[0].plugin_identifier is not None
        assert len(result[0].plugin_identifier) == 64

    def test_claude_code_plugin_mcp_config_has_identifier(self, tmp_path: Path):
        install_path = _create_claude_plugin(
            tmp_path,
            "official",
            "ctx",
            "v1",
            plugin_json={
                "name": "ctx",
                "version": "1.0.0",
                "mcpServers": {"ctx": {"command": "npx", "args": ["ctx"]}},
            },
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"ctx@official": [{"scope": "user", "installPath": install_path}]},
        )
        result = scan_claude_code_plugins(installed)
        assert len(result) == 1
        assert result[0].plugin_identifier is not None
        assert len(result[0].plugin_identifier) == 64


# ===========================================================================
# File collection
# ===========================================================================


class TestCollectPluginFiles:
    def test_empty_directory(self, tmp_path: Path):
        files, symlinks, oversized = _collect_plugin_files(tmp_path)
        assert files == []
        assert symlinks == []
        assert oversized is False

    def test_collects_supported_extensions(self, tmp_path: Path):
        (tmp_path / "plugin.json").write_text('{"name": "test"}')
        (tmp_path / "README.md").write_text("# Hello")
        (tmp_path / "config.yaml").write_text("key: value")
        (tmp_path / "binary.bin").write_bytes(b"\x00\x01")
        files, _, _ = _collect_plugin_files(tmp_path)
        titles = {f.title for f in files}
        assert "plugin.json" in titles
        assert "README.md" in titles
        assert "config.yaml" in titles
        assert "binary.bin" not in titles

    def test_collects_nested_files(self, tmp_path: Path):
        subdir = tmp_path / "commands"
        subdir.mkdir()
        (subdir / "status.md").write_text("# Status command")
        files, _, _ = _collect_plugin_files(tmp_path)
        assert any(f.title == "commands/status.md" for f in files)

    def test_skips_node_modules(self, tmp_path: Path):
        nm = tmp_path / "node_modules" / "dep"
        nm.mkdir(parents=True)
        (nm / "index.js").write_text("module.exports = {}")
        (tmp_path / "plugin.json").write_text("{}")
        files, _, _ = _collect_plugin_files(tmp_path)
        assert not any("node_modules" in f.title for f in files)

    def test_oversized_single_file(self, tmp_path: Path):
        big = tmp_path / "big.md"
        big.write_text("x" * (1_048_576 + 1))
        (tmp_path / "small.md").write_text("small")
        files, _, oversized = _collect_plugin_files(tmp_path)
        assert oversized is True
        titles = {f.title for f in files}
        assert "big.md" not in titles
        assert "small.md" in titles

    def test_oversized_total_budget(self, tmp_path: Path):
        for i in range(10):
            (tmp_path / f"file{i}.md").write_text("x" * 600_000)
        files, _, oversized = _collect_plugin_files(tmp_path)
        assert oversized is True
        assert len(files) < 10

    def test_external_symlink_tracked(self, tmp_path: Path):
        external = tmp_path / "external"
        external.mkdir()
        (external / "secret.md").write_text("secret")
        plugin_dir = tmp_path / "plugin"
        plugin_dir.mkdir()
        (plugin_dir / "real.md").write_text("real")
        (plugin_dir / "link.md").symlink_to(external / "secret.md")
        files, symlinks, _ = _collect_plugin_files(plugin_dir)
        assert len(symlinks) == 1
        assert not any(f.title == "link.md" for f in files)
        assert any(f.title == "real.md" for f in files)


class TestPluginFilesInScanResults:
    def test_cursor_plugin_collects_files(self, tmp_path: Path):
        _create_cursor_plugin(
            tmp_path,
            "with-files",
            plugin_json={"name": "with-files", "version": "1.0.0"},
            mcp_json={"mcpServers": {"s": {"command": "echo"}}},
        )
        hash_dir = tmp_path / "with-files" / "abc123"
        (hash_dir / "README.md").write_text("# Plugin readme")
        result = scan_cursor_native_plugins(plugin_cache_base=tmp_path)
        assert len(result) == 1
        assert result[0].file_count >= 2
        titles = {f.title for f in result[0].files}
        assert "README.md" in titles
        assert ".cursor-plugin/plugin.json" in titles

    def test_claude_code_plugin_collects_files(self, tmp_path: Path):
        install_path = _create_claude_plugin(
            tmp_path,
            "official",
            "test",
            "v1",
            plugin_json={"name": "test", "version": "1.0.0"},
            mcp_json={"mcpServers": {"s": {"command": "echo"}}},
        )
        Path(install_path, "README.md").write_text("# Plugin")
        installed = _write_installed_plugins(
            tmp_path,
            {"test@official": [{"installPath": install_path, "scope": "user"}]},
        )
        result = scan_claude_code_plugin_artifacts(installed_plugins_path=installed)
        assert len(result) == 1
        assert result[0].file_count >= 2
        titles = {f.title for f in result[0].files}
        assert ".claude-plugin/plugin.json" in titles
        assert ".mcp.json" in titles

    def test_claude_desktop_connector_has_synthetic_file(self, tmp_path: Path):
        config = tmp_path / "claude_desktop_config.json"
        config.write_text(json.dumps({"mcpServers": {"srv": {"command": "echo"}}}))
        result = scan_claude_desktop_connectors(config_path_override=config)
        assert len(result) == 1
        assert result[0].file_count == 1
        assert result[0].files[0].title == "srv.json"
        assert '"command"' in result[0].files[0].content

    def test_files_in_api_payload(self, tmp_path: Path):
        _create_cursor_plugin(
            tmp_path,
            "payload-test",
            plugin_json={"name": "payload-test", "version": "1.0.0"},
        )
        result = scan_cursor_native_plugins(plugin_cache_base=tmp_path)
        payload = result[0].to_api_payload()
        assert "files" in payload
        assert isinstance(payload["files"], list)
        assert len(payload["files"]) >= 1
        assert "title" in payload["files"][0]
        assert "content" in payload["files"][0]
        assert "file_count" in payload
        assert "oversized" in payload
        assert "symlinks_found" in payload


# ===========================================================================
# Codex plugin helpers
# ===========================================================================


def _create_codex_plugin(
    cache_base: Path,
    marketplace: str,
    name: str,
    version: str,
    plugin_json: dict | None = None,
    mcp_json: dict | None = None,
    extra_dirs: list[str] | None = None,
) -> Path:
    version_dir = cache_base / marketplace / name / version
    version_dir.mkdir(parents=True, exist_ok=True)
    if plugin_json is not None:
        manifest_dir = version_dir / ".codex-plugin"
        manifest_dir.mkdir(exist_ok=True)
        (manifest_dir / "plugin.json").write_text(json.dumps(plugin_json))
    if mcp_json is not None:
        (version_dir / ".mcp.json").write_text(json.dumps(mcp_json))
    for d in extra_dirs or []:
        (version_dir / d).mkdir(exist_ok=True)
    return version_dir


# ===========================================================================
# Codex plugin artifact tests
# ===========================================================================


class TestCodexPluginArtifacts:
    def test_empty_cache_returns_empty(self, tmp_path: Path):
        result = scan_codex_plugin_artifacts(plugin_cache_base=tmp_path)
        assert result == []

    def test_missing_cache_returns_empty(self, tmp_path: Path):
        result = scan_codex_plugin_artifacts(plugin_cache_base=tmp_path / "nonexistent")
        assert result == []

    def test_discovers_codex_plugin(self, tmp_path: Path):
        _create_codex_plugin(
            tmp_path,
            "official",
            "test-plugin",
            "1.0.0",
            plugin_json={"name": "test-plugin", "version": "1.0.0"},
        )
        result = scan_codex_plugin_artifacts(plugin_cache_base=tmp_path)
        assert len(result) == 1
        assert result[0].name == "test-plugin"
        assert result[0].plugin_type == "codex_plugin"
        assert result[0].client == "codex"
        assert result[0].marketplace == "official"
        assert result[0].version == "1.0.0"

    def test_codex_plugin_with_mcp_servers(self, tmp_path: Path):
        _create_codex_plugin(
            tmp_path,
            "official",
            "mcp-plugin",
            "2.0.0",
            plugin_json={"name": "mcp-plugin", "version": "2.0.0"},
            mcp_json={"mcpServers": {"db": {"command": "node", "args": ["db.js"]}}},
        )
        result = scan_codex_plugin_artifacts(plugin_cache_base=tmp_path)
        assert len(result) == 1
        assert result[0].has_mcp_servers is True
        assert len(result[0].mcp_servers) == 1
        assert result[0].mcp_servers[0].name == "db"

    def test_codex_plugin_detects_skills_dir(self, tmp_path: Path):
        _create_codex_plugin(
            tmp_path,
            "official",
            "skill-plugin",
            "1.0.0",
            plugin_json={"name": "skill-plugin"},
            extra_dirs=["skills"],
        )
        result = scan_codex_plugin_artifacts(plugin_cache_base=tmp_path)
        assert len(result) == 1
        assert result[0].has_skills is True

    def test_multiple_marketplaces(self, tmp_path: Path):
        _create_codex_plugin(
            tmp_path,
            "official",
            "plug-a",
            "1.0.0",
            plugin_json={"name": "plug-a"},
        )
        _create_codex_plugin(
            tmp_path,
            "community",
            "plug-b",
            "0.5.0",
            plugin_json={"name": "plug-b"},
        )
        result = scan_codex_plugin_artifacts(plugin_cache_base=tmp_path)
        assert len(result) == 2
        names = {r.name for r in result}
        assert names == {"plug-a", "plug-b"}
        marketplaces = {r.marketplace for r in result}
        assert marketplaces == {"official", "community"}

    def test_uses_latest_version_dir(self, tmp_path: Path):
        _create_codex_plugin(
            tmp_path,
            "official",
            "versioned",
            "1.0.0",
            plugin_json={"name": "versioned", "version": "1.0.0"},
        )
        _create_codex_plugin(
            tmp_path,
            "official",
            "versioned",
            "2.0.0",
            plugin_json={"name": "versioned", "version": "2.0.0"},
        )
        result = scan_codex_plugin_artifacts(plugin_cache_base=tmp_path)
        assert len(result) == 1
        assert result[0].version == "2.0.0"

    def test_uses_latest_version_dir_semver(self, tmp_path: Path):
        """10.0.0 must beat 2.0.0 even though '2' > '1' lexicographically."""
        _create_codex_plugin(
            tmp_path,
            "official",
            "versioned",
            "2.0.0",
            plugin_json={"name": "versioned", "version": "2.0.0"},
        )
        _create_codex_plugin(
            tmp_path,
            "official",
            "versioned",
            "10.0.0",
            plugin_json={"name": "versioned", "version": "10.0.0"},
        )
        result = scan_codex_plugin_artifacts(plugin_cache_base=tmp_path)
        assert len(result) == 1
        assert result[0].version == "10.0.0"

    def test_codex_plugin_collects_files(self, tmp_path: Path):
        version_dir = _create_codex_plugin(
            tmp_path,
            "official",
            "with-files",
            "1.0.0",
            plugin_json={"name": "with-files", "version": "1.0.0"},
            mcp_json={"mcpServers": {"s": {"command": "echo"}}},
        )
        (version_dir / "README.md").write_text("# Plugin readme")
        result = scan_codex_plugin_artifacts(plugin_cache_base=tmp_path)
        assert len(result) == 1
        assert result[0].file_count >= 2
        titles = {f.title for f in result[0].files}
        assert "README.md" in titles
        assert ".codex-plugin/plugin.json" in titles

    def test_codex_plugin_api_payload(self, tmp_path: Path):
        _create_codex_plugin(
            tmp_path,
            "official",
            "payload-test",
            "1.0.0",
            plugin_json={"name": "payload-test", "version": "1.0.0"},
        )
        result = scan_codex_plugin_artifacts(plugin_cache_base=tmp_path)
        payload = result[0].to_api_payload()
        assert payload["plugin_type"] == "codex_plugin"
        assert payload["client"] == "codex"
        assert payload["marketplace"] == "official"
        assert "files" in payload
        assert isinstance(payload["files"], list)


class TestCodexPluginSemverOrdering:
    """Verify scan_codex_plugins picks the highest semver, not lexicographic."""

    def test_scan_codex_plugins_picks_highest_semver(self, tmp_path: Path):
        """10.0.0 must beat 2.0.0 when discovering MCP servers."""
        base = tmp_path / "official" / "my-plugin"
        for ver, cmd in [("2.0.0", "old-cmd"), ("10.0.0", "new-cmd")]:
            d = base / ver
            d.mkdir(parents=True)
            (d / "mcp.json").write_text(
                json.dumps({"mcpServers": {"s": {"command": cmd}}})
            )
        configs = scan_codex_plugins(plugin_cache_base=tmp_path)
        assert len(configs) == 1
        assert configs[0].servers[0].command == "new-cmd"

    def test_prerelease_versions_do_not_crash(self, tmp_path: Path):
        """Mixed int/str segments (e.g. '1.0.0-beta' vs '1.0.0') must not TypeError."""
        base = tmp_path / "official" / "my-plugin"
        for ver, cmd in [("1.0.0-beta", "beta-cmd"), ("1.0.0", "release-cmd")]:
            d = base / ver
            d.mkdir(parents=True)
            (d / "mcp.json").write_text(
                json.dumps({"mcpServers": {"s": {"command": cmd}}})
            )
        configs = scan_codex_plugins(plugin_cache_base=tmp_path)
        assert len(configs) == 1
        assert configs[0].servers[0].command == "release-cmd"

    def test_unset_userprofile_returns_empty(self, monkeypatch: pytest.MonkeyPatch):
        """When USERPROFILE is unset on Windows, must return [] not scan cwd."""
        monkeypatch.setattr(
            "runlayer_cli.scan.plugin_scanner.platform.system", lambda: "Windows"
        )
        monkeypatch.delenv("USERPROFILE", raising=False)
        result = scan_codex_plugin_artifacts()
        assert result == []

    def test_scan_codex_plugins_rc10_beats_rc2(self, tmp_path: Path):
        """rc10 must sort above rc2 (numeric, not lexicographic)."""
        base = tmp_path / "official" / "my-plugin"
        for ver, cmd in [("1.0.0-rc2", "old-cmd"), ("1.0.0-rc10", "new-cmd")]:
            d = base / ver
            d.mkdir(parents=True)
            (d / "mcp.json").write_text(
                json.dumps({"mcpServers": {"s": {"command": cmd}}})
            )
        configs = scan_codex_plugins(plugin_cache_base=tmp_path)
        assert len(configs) == 1
        assert configs[0].servers[0].command == "new-cmd"

    def test_artifact_rc10_beats_rc2(self, tmp_path: Path):
        """scan_codex_plugin_artifacts: rc10 must beat rc2."""
        _create_codex_plugin(
            tmp_path,
            "official",
            "rctest",
            "1.0.0-rc2",
            plugin_json={"name": "rctest", "version": "1.0.0-rc2"},
        )
        _create_codex_plugin(
            tmp_path,
            "official",
            "rctest",
            "1.0.0-rc10",
            plugin_json={"name": "rctest", "version": "1.0.0-rc10"},
        )
        result = scan_codex_plugin_artifacts(plugin_cache_base=tmp_path)
        assert len(result) == 1
        assert result[0].version == "1.0.0-rc10"

    def test_alpha_prerelease_beats_numeric_prerelease(self, tmp_path: Path):
        """SemVer §11.4: alphanumeric identifiers > numeric identifiers."""
        base = tmp_path / "official" / "my-plugin"
        for ver, cmd in [("1.0.0-1", "numeric-cmd"), ("1.0.0-alpha", "alpha-cmd")]:
            d = base / ver
            d.mkdir(parents=True)
            (d / "mcp.json").write_text(
                json.dumps({"mcpServers": {"s": {"command": cmd}}})
            )
        configs = scan_codex_plugins(plugin_cache_base=tmp_path)
        assert len(configs) == 1
        assert configs[0].servers[0].command == "alpha-cmd"

    def test_artifact_alpha_prerelease_beats_numeric(self, tmp_path: Path):
        """scan_codex_plugin_artifacts: 1.0.0-alpha must beat 1.0.0-1 per SemVer."""
        _create_codex_plugin(
            tmp_path,
            "official",
            "semver-test",
            "1.0.0-1",
            plugin_json={"name": "semver-test", "version": "1.0.0-1"},
        )
        _create_codex_plugin(
            tmp_path,
            "official",
            "semver-test",
            "1.0.0-alpha",
            plugin_json={"name": "semver-test", "version": "1.0.0-alpha"},
        )
        result = scan_codex_plugin_artifacts(plugin_cache_base=tmp_path)
        assert len(result) == 1
        assert result[0].version == "1.0.0-alpha"

    def test_artifact_prerelease_versions_do_not_crash(self, tmp_path: Path):
        """scan_codex_plugin_artifacts must not TypeError on prerelease dirs."""
        _create_codex_plugin(
            tmp_path,
            "official",
            "pre",
            "1.0.0-rc1",
            plugin_json={"name": "pre", "version": "1.0.0-rc1"},
        )
        _create_codex_plugin(
            tmp_path,
            "official",
            "pre",
            "1.0.0",
            plugin_json={"name": "pre", "version": "1.0.0"},
        )
        result = scan_codex_plugin_artifacts(plugin_cache_base=tmp_path)
        assert len(result) == 1
        assert result[0].version == "1.0.0"
