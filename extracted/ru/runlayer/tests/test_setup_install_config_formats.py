"""Tests for editor config format handling in setup install."""

import json
from pathlib import Path

import pytest

from runlayer_cli.commands.setup import (
    ConfigParseError,
    InstallClient,
    InstallServerSpec,
    _build_server_entry,
    _get_servers_key_for_client,
    _install_plugins_to_client,
    _read_config_file,
    _write_config_file,
)


class TestJSONCParsing:
    """Tests for JSONC (JSON with comments) handling."""

    def test_jsonc_with_comments_preserves_existing(self, tmp_path: Path) -> None:
        config_file = tmp_path / "mcp.json"
        jsonc_content = """{
  // Comment
  "servers": {
    "existing-server": {"type": "stdio", "command": "npx", "args": ["-y", "srv"]}
  }
}"""
        config_file.write_text(jsonc_content)

        result = _read_config_file(config_file, "json")

        assert result != {}
        assert "existing-server" in result["servers"]

    def test_jsonc_with_trailing_comma_parses(self, tmp_path: Path) -> None:
        config_file = tmp_path / "mcp.json"
        config_file.write_text(
            '{"servers": {"s1": {"type": "stdio", "command": "x",},}}'
        )

        result = _read_config_file(config_file, "json")

        assert result != {}
        assert "servers" in result

    def test_invalid_json_raises(self, tmp_path: Path) -> None:
        config_file = tmp_path / "mcp.json"
        config_file.write_text("{this is not json}")

        with pytest.raises(ConfigParseError):
            _read_config_file(config_file, "json")


class TestVSCodeConfigFormat:
    def test_uses_servers_key(self) -> None:
        assert _get_servers_key_for_client(InstallClient.VSCODE) == "servers"

    def test_local_entry_has_type_stdio(self) -> None:
        spec = InstallServerSpec(
            server_id="abc123",
            name="Test",
            proxy_url="https://example.com/mcp",
            host="https://example.com",
            is_local=True,
        )
        entry = _build_server_entry(InstallClient.VSCODE, spec)

        assert entry["type"] == "stdio"
        assert entry["command"] == "uvx"

    def test_remote_entry_has_type_http(self) -> None:
        spec = InstallServerSpec(
            server_id="abc123",
            name="Test",
            proxy_url="https://example.com/mcp",
            host="https://example.com",
            is_local=False,
        )
        entry = _build_server_entry(InstallClient.VSCODE, spec)

        assert entry["type"] == "http"
        assert entry["url"] == "https://example.com/mcp"


class TestClaudeCodeConfigFormat:
    def test_uses_mcpservers_key(self) -> None:
        assert _get_servers_key_for_client(InstallClient.CLAUDE_CODE) == "mcpServers"

    def test_remote_entry_has_type_http(self) -> None:
        spec = InstallServerSpec(
            server_id="abc123",
            name="Test",
            proxy_url="https://example.com/mcp",
            host="https://example.com",
            is_local=False,
        )
        entry = _build_server_entry(InstallClient.CLAUDE_CODE, spec)

        assert entry["type"] == "http"
        assert entry["url"] == "https://example.com/mcp"


class TestGooseConfigFormat:
    def test_remote_uses_streamable_http(self) -> None:
        spec = InstallServerSpec(
            server_id="abc123",
            name="Test",
            proxy_url="https://example.com/mcp",
            host="https://example.com",
            is_local=False,
        )
        entry = _build_server_entry(InstallClient.GOOSE, spec)

        assert entry["type"] == "streamable_http"

    def test_remote_uses_uri_not_url(self) -> None:
        spec = InstallServerSpec(
            server_id="abc123",
            name="Test",
            proxy_url="https://example.com/mcp",
            host="https://example.com",
            is_local=False,
        )
        entry = _build_server_entry(InstallClient.GOOSE, spec)

        assert "uri" in entry
        assert "url" not in entry


class TestWindsurfConfigFormat:
    def test_uses_mcpservers_key(self) -> None:
        assert _get_servers_key_for_client(InstallClient.WINDSURF) == "mcpServers"

    def test_remote_uses_serverurl(self) -> None:
        spec = InstallServerSpec(
            server_id="abc123",
            name="Test",
            proxy_url="https://example.com/mcp",
            host="https://example.com",
            is_local=False,
        )
        entry = _build_server_entry(InstallClient.WINDSURF, spec)

        assert "serverUrl" in entry


class TestZedConfigFormat:
    def test_uses_context_servers_key(self) -> None:
        assert _get_servers_key_for_client(InstallClient.ZED) == "context_servers"


class TestOpenCodeConfigFormat:
    def test_uses_mcp_key(self) -> None:
        assert _get_servers_key_for_client(InstallClient.OPENCODE) == "mcp"

    def test_local_entry_uses_command_array(self) -> None:
        spec = InstallServerSpec(
            server_id="abc123",
            name="Test",
            proxy_url="https://example.com/mcp",
            host="https://example.com",
            is_local=True,
        )
        entry = _build_server_entry(InstallClient.OPENCODE, spec)
        assert entry["type"] == "local"
        assert entry["enabled"] is True
        assert entry["command"] == [
            "uvx",
            "runlayer",
            "run",
            "abc123",
            "--host",
            "https://example.com",
        ]

    def test_remote_entry_uses_url_field(self) -> None:
        spec = InstallServerSpec(
            server_id="abc123",
            name="Test",
            proxy_url="https://example.com/mcp",
            host="https://example.com",
            is_local=False,
        )
        entry = _build_server_entry(InstallClient.OPENCODE, spec)
        assert entry["type"] == "remote"
        assert entry["enabled"] is True
        assert entry["url"] == "https://example.com/mcp"


class TestPluginInstallConfigFormat:
    def test_plugin_entry_has_type_http(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Plugin entries written to Claude Code must include type:http."""
        config_file = tmp_path / ".claude.json"
        config_file.write_text(json.dumps({"mcpServers": {}}))
        monkeypatch.setattr(
            "runlayer_cli.commands.setup._get_install_client_config_path",
            lambda _: config_file,
        )

        plugins = [
            ("id1", "My Plugin", "https://example.com/api/v1/proxy/plugins/id1/mcp"),
        ]
        count = _install_plugins_to_client(InstallClient.CLAUDE_CODE, plugins)

        assert count == 1
        config = json.loads(config_file.read_text())
        entry = config["mcpServers"]["my-plugin"]
        assert entry["type"] == "http"
        assert entry["url"] == "https://example.com/api/v1/proxy/plugins/id1/mcp"


class TestInstallPreservesExistingConfig:
    def test_preserves_existing_servers(self, tmp_path: Path) -> None:
        config_file = tmp_path / "mcp.json"
        config_file.write_text("""{
  // My config
  "servers": {"existing": {"type": "stdio", "command": "npx", "args": ["-y", "srv"]}}
}""")

        config = _read_config_file(config_file, "json")
        config["servers"]["new"] = {"type": "http", "url": "https://example.com/mcp"}
        _write_config_file(config_file, config, "json")

        final = json.loads(config_file.read_text())
        assert "existing" in final["servers"]
        assert "new" in final["servers"]
