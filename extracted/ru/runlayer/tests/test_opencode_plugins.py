"""Tests for OpenCode plugin scanning (MCP servers + artifacts)."""

import json
from pathlib import Path

from runlayer_cli.scan.opencode_plugins import scan_opencode_plugins
from runlayer_cli.scan.plugin_scanner import scan_opencode_plugin_artifacts


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _create_local_plugin_dir(
    plugins_base: Path,
    name: str,
    mcp_json: dict | None = None,
    package_json: dict | None = None,
) -> Path:
    plugin_dir = plugins_base / name
    plugin_dir.mkdir(parents=True, exist_ok=True)
    if mcp_json is not None:
        (plugin_dir / "mcp.json").write_text(json.dumps(mcp_json))
    if package_json is not None:
        (plugin_dir / "package.json").write_text(json.dumps(package_json))
    return plugin_dir


def _create_npm_plugin(
    npm_cache: Path,
    name: str,
    package_json: dict | None = None,
    mcp_json: dict | None = None,
) -> Path:
    pkg_dir = npm_cache / name
    pkg_dir.mkdir(parents=True, exist_ok=True)
    if package_json is not None:
        (pkg_dir / "package.json").write_text(json.dumps(package_json))
    if mcp_json is not None:
        (pkg_dir / "mcp.json").write_text(json.dumps(mcp_json))
    return pkg_dir


def _write_opencode_config(config_path: Path, data: dict) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(data))


# ===========================================================================
# scan_opencode_plugins (MCP servers from plugins)
# ===========================================================================


class TestScanOpenCodePlugins:
    def test_empty_dirs_returns_empty(self, tmp_path: Path):
        result = scan_opencode_plugins(
            local_plugins_base=tmp_path / "local",
            npm_cache_base=tmp_path / "npm",
            config_path=tmp_path / "opencode.json",
        )
        assert result == []

    def test_discovers_local_plugin_with_mcp(self, tmp_path: Path):
        local = tmp_path / "plugins"
        _create_local_plugin_dir(
            local,
            "my-tool",
            mcp_json={"mcpServers": {"srv": {"command": "echo", "args": ["hi"]}}},
        )
        result = scan_opencode_plugins(
            local_plugins_base=local,
            npm_cache_base=tmp_path / "npm",
            config_path=tmp_path / "opencode.json",
        )
        assert len(result) == 1
        assert result[0].client == "opencode"
        assert result[0].config_scope == "plugin"
        assert len(result[0].servers) == 1
        assert result[0].servers[0].command == "echo"

    def test_skips_local_plugin_without_mcp(self, tmp_path: Path):
        local = tmp_path / "plugins"
        _create_local_plugin_dir(local, "no-mcp")
        result = scan_opencode_plugins(
            local_plugins_base=local,
            npm_cache_base=tmp_path / "npm",
            config_path=tmp_path / "opencode.json",
        )
        assert result == []

    def test_discovers_npm_plugin_with_mcp(self, tmp_path: Path):
        npm = tmp_path / "node_modules"
        config = tmp_path / "opencode.json"
        _write_opencode_config(config, {"plugin": ["opencode-helicone"]})
        _create_npm_plugin(
            npm,
            "opencode-helicone",
            package_json={"name": "opencode-helicone", "version": "1.0.0"},
            mcp_json={"mcpServers": {"helicone": {"command": "node", "args": ["srv"]}}},
        )
        result = scan_opencode_plugins(
            local_plugins_base=tmp_path / "local",
            npm_cache_base=npm,
            config_path=config,
        )
        assert len(result) == 1
        assert result[0].servers[0].name == "helicone"

    def test_config_path_alt_derived_from_config_path(self, tmp_path: Path):
        """config_path_alt must be sibling of config_path, not home-relative."""
        npm = tmp_path / "node_modules"
        config = tmp_path / "opencode.json"
        jsonc = tmp_path / "opencode.jsonc"

        _create_npm_plugin(
            npm,
            "jsonc-only-plugin",
            mcp_json={"mcpServers": {"jc": {"command": "echo", "args": ["jsonc"]}}},
        )
        _write_opencode_config(jsonc, {"plugin": ["jsonc-only-plugin"]})

        result = scan_opencode_plugins(
            local_plugins_base=tmp_path / "local",
            npm_cache_base=npm,
            config_path=config,
        )
        assert len(result) == 1
        assert result[0].servers[0].name == "jc"

    def test_npm_plugin_not_in_config_skipped(self, tmp_path: Path):
        npm = tmp_path / "node_modules"
        config = tmp_path / "opencode.json"
        _write_opencode_config(config, {"plugin": []})
        _create_npm_plugin(
            npm,
            "unlisted-pkg",
            mcp_json={"mcpServers": {"s": {"command": "echo"}}},
        )
        result = scan_opencode_plugins(
            local_plugins_base=tmp_path / "local",
            npm_cache_base=npm,
            config_path=config,
        )
        assert result == []

    def test_combines_local_and_npm(self, tmp_path: Path):
        local = tmp_path / "plugins"
        npm = tmp_path / "node_modules"
        config = tmp_path / "opencode.json"

        _create_local_plugin_dir(
            local,
            "local-tool",
            mcp_json={"mcpServers": {"a": {"command": "cmd-a"}}},
        )
        _write_opencode_config(config, {"plugin": ["npm-tool"]})
        _create_npm_plugin(
            npm,
            "npm-tool",
            mcp_json={"mcpServers": {"b": {"url": "http://x"}}},
        )

        result = scan_opencode_plugins(
            local_plugins_base=local,
            npm_cache_base=npm,
            config_path=config,
        )
        assert len(result) == 2
        names = {r.servers[0].name for r in result}
        assert names == {"a", "b"}


# ===========================================================================
# scan_opencode_plugin_artifacts
# ===========================================================================


class TestScanOpenCodePluginArtifacts:
    def test_empty_dirs_returns_empty(self, tmp_path: Path):
        result = scan_opencode_plugin_artifacts(
            local_plugins_base=tmp_path / "local",
            npm_cache_base=tmp_path / "npm",
            config_path=tmp_path / "opencode.json",
        )
        assert result == []

    def test_discovers_local_dir_plugin(self, tmp_path: Path):
        local = tmp_path / "plugins"
        _create_local_plugin_dir(
            local,
            "toolguard",
            package_json={
                "name": "toolguard",
                "version": "0.2.0",
                "description": "Tool guard plugin",
            },
        )
        result = scan_opencode_plugin_artifacts(
            local_plugins_base=local,
            npm_cache_base=tmp_path / "npm",
            config_path=tmp_path / "opencode.json",
        )
        assert len(result) == 1
        assert result[0].name == "toolguard"
        assert result[0].plugin_type == "opencode_plugin"
        assert result[0].client == "opencode"
        assert result[0].version == "0.2.0"
        assert result[0].description == "Tool guard plugin"

    def test_discovers_local_standalone_js_file(self, tmp_path: Path):
        local = tmp_path / "plugins"
        local.mkdir(parents=True)
        (local / "my-hook.ts").write_text("export const MyHook = () => ({});")

        result = scan_opencode_plugin_artifacts(
            local_plugins_base=local,
            npm_cache_base=tmp_path / "npm",
            config_path=tmp_path / "opencode.json",
        )
        assert len(result) == 1
        assert result[0].name == "my-hook"
        assert result[0].plugin_type == "opencode_plugin"
        assert result[0].file_count == 1

    def test_discovers_npm_plugin_artifact(self, tmp_path: Path):
        npm = tmp_path / "node_modules"
        config = tmp_path / "opencode.json"
        _write_opencode_config(config, {"plugin": ["opencode-wakatime"]})
        _create_npm_plugin(
            npm,
            "opencode-wakatime",
            package_json={
                "name": "opencode-wakatime",
                "version": "1.2.0",
                "author": "wakatime",
            },
        )
        result = scan_opencode_plugin_artifacts(
            local_plugins_base=tmp_path / "local",
            npm_cache_base=npm,
            config_path=config,
        )
        assert len(result) == 1
        assert result[0].name == "opencode-wakatime"
        assert result[0].plugin_type == "opencode_npm_plugin"
        assert result[0].marketplace == "npm"
        assert result[0].version == "1.2.0"
        assert result[0].author == "wakatime"

    def test_npm_plugin_with_mcp_servers(self, tmp_path: Path):
        npm = tmp_path / "node_modules"
        config = tmp_path / "opencode.json"
        _write_opencode_config(config, {"plugin": ["mcp-bundle"]})
        _create_npm_plugin(
            npm,
            "mcp-bundle",
            package_json={"name": "mcp-bundle"},
            mcp_json={"mcpServers": {"db": {"command": "pg-mcp"}}},
        )
        result = scan_opencode_plugin_artifacts(
            local_plugins_base=tmp_path / "local",
            npm_cache_base=npm,
            config_path=config,
        )
        assert len(result) == 1
        assert result[0].has_mcp_servers is True
        assert len(result[0].mcp_servers) == 1
        assert result[0].mcp_servers[0].name == "db"

    def test_api_payload_shape(self, tmp_path: Path):
        local = tmp_path / "plugins"
        _create_local_plugin_dir(
            local,
            "test-plugin",
            package_json={"name": "test-plugin", "version": "0.1.0"},
        )
        result = scan_opencode_plugin_artifacts(
            local_plugins_base=local,
            npm_cache_base=tmp_path / "npm",
            config_path=tmp_path / "opencode.json",
        )
        payload = result[0].to_api_payload()
        assert payload["plugin_type"] == "opencode_plugin"
        assert payload["client"] == "opencode"
        assert isinstance(payload["files"], list)
        assert isinstance(payload["mcp_servers"], list)
