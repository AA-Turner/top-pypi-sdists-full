"""Tests for editor config format handling in setup install."""

import json
import os
from pathlib import Path
from typing import Any, cast

import pytest
import typer
from typer.testing import CliRunner

from runlayer_cli.api import PluginListItem, ServerListItem
from runlayer_cli.commands import setup
from runlayer_cli.commands.setup import (
    ConfigParseError,
    InstallClient,
    InstallServerSpec,
    _build_server_entry,
    _get_servers_key_for_client,
    _install_servers_to_client,
    _install_plugins_to_client,
    _read_config_file,
    _write_config_file,
)


class _FakeInstallApiClient:
    def list_servers(self, scope: str) -> list[ServerListItem]:
        assert scope == "accessible"
        return [
            ServerListItem(
                id="abc123",
                name="New Server",
                status="active",
                deployment_mode="hosted",
            )
        ]

    def list_plugins(self) -> list[Any]:
        return []


class _FakeInteractiveInstallApiClient(_FakeInstallApiClient):
    def list_plugins(self) -> list[PluginListItem]:
        return [
            PluginListItem(
                id="plugin123",
                name="New Plugin",
                description="A plugin",
            )
        ]


class _Prompt:
    def __init__(self, value: Any) -> None:
        self.value = value

    def ask(self) -> Any:
        return self.value


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


class TestCodexConfigFormat:
    def test_install_preserves_comments_and_unrelated_tables(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            """# Keep this operator note
model = "gpt-5"

[projects."/tmp/work tree"]
trust_level = "trusted"

[mcp_servers.existing]
command = "npx"
args = ["existing-server"]
"""
        )
        monkeypatch.setattr(
            "runlayer_cli.commands.setup._get_install_client_config_path",
            lambda _: config_file,
        )
        spec = InstallServerSpec(
            server_id="abc123",
            name="New Server",
            proxy_url="https://example.com/mcp",
            host="https://example.com",
            is_local=False,
        )

        assert _install_servers_to_client(InstallClient.CODEX, [spec]) == 1

        updated = config_file.read_text()
        assert "# Keep this operator note" in updated
        assert '[projects."/tmp/work tree"]' in updated
        result = _read_config_file(config_file, "toml")
        assert result["model"] == "gpt-5"
        assert result["projects"]["/tmp/work tree"]["trust_level"] == "trusted"
        assert result["mcp_servers"]["existing"]["command"] == "npx"
        assert result["mcp_servers"]["new-server"]["url"] == ("https://example.com/mcp")
        assert len(list(tmp_path.glob("config.backup_*.toml"))) == 1

    def test_install_does_not_overwrite_malformed_toml(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        config_file = tmp_path / "config.toml"
        original = "[mcp_servers.invalid\nurl ="
        config_file.write_text(original)
        monkeypatch.setattr(
            "runlayer_cli.commands.setup._get_install_client_config_path",
            lambda _: config_file,
        )
        spec = InstallServerSpec(
            server_id="abc123",
            name="New Server",
            proxy_url="https://example.com/mcp",
            host="https://example.com",
            is_local=False,
        )

        with pytest.raises(setup.InstallError, match="Failed to parse TOML config"):
            _install_servers_to_client(InstallClient.CODEX, [spec])
        assert config_file.read_text() == original
        assert list(tmp_path.glob("config.backup_*.toml")) == []

    def test_repeated_install_does_not_rewrite_or_create_backup(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        config_file = tmp_path / "config.toml"
        monkeypatch.setattr(
            "runlayer_cli.commands.setup._get_install_client_config_path",
            lambda _: config_file,
        )
        spec = InstallServerSpec(
            server_id="abc123",
            name="Test Server",
            proxy_url="https://example.com/mcp",
            host="https://example.com",
            is_local=False,
            headers={"Authorization": "Bearer token123"},
        )

        assert _install_servers_to_client(InstallClient.CODEX, [spec]) == 1
        first = config_file.read_text()
        old_mtime_ns = 1_000_000_000
        os.utime(config_file, ns=(old_mtime_ns, old_mtime_ns))
        assert _install_servers_to_client(InstallClient.CODEX, [spec]) == 1

        assert config_file.read_text() == first
        assert config_file.stat().st_mtime_ns == old_mtime_ns
        assert list(tmp_path.glob("config.backup_*.toml")) == []

    def test_non_interactive_install_exits_nonzero_for_malformed_toml(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        config_file = tmp_path / "config.toml"
        config_file.write_text("[mcp_servers.invalid\nurl =")
        monkeypatch.setattr(
            setup,
            "_get_install_client_config_path",
            lambda _: config_file,
        )
        monkeypatch.setattr(
            setup, "set_credentials_in_context", lambda *args, **kwargs: None
        )
        monkeypatch.setattr(
            setup,
            "resolve_credentials",
            lambda *args, **kwargs: {
                "secret": "secret",
                "host": "https://example.com",
            },
        )
        monkeypatch.setattr(
            setup,
            "RunlayerClient",
            lambda *args, **kwargs: _FakeInstallApiClient(),
        )

        with pytest.raises(typer.Exit) as exc_info:
            setup.install(
                ctx=cast(Any, object()),
                client=InstallClient.CODEX,
                server_ids=["abc123"],
                plugin_ids=None,
                header=None,
                interactive=False,
                secret=None,
                host=None,
                yes=True,
            )

        output = capsys.readouterr().out
        assert exc_info.value.exit_code == 1
        assert "Cannot read" in output
        assert "Installation complete" not in output


class TestPluginInstallConfigFormat:
    def test_plugin_entry_has_type_http(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
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


class TestIdempotentInstall:
    def test_repeated_server_install_does_not_rewrite_or_create_backup(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        config_file = tmp_path / "mcp.json"
        monkeypatch.setattr(
            setup,
            "_get_install_client_config_path",
            lambda _: config_file,
        )
        spec = InstallServerSpec(
            server_id="abc123",
            name="Test Server",
            proxy_url="https://example.com/mcp",
            host="https://example.com",
            is_local=False,
        )

        assert _install_servers_to_client(InstallClient.CURSOR, [spec]) == 1
        first = config_file.read_text()
        old_mtime_ns = 1_000_000_000
        os.utime(config_file, ns=(old_mtime_ns, old_mtime_ns))

        assert _install_servers_to_client(InstallClient.CURSOR, [spec]) == 1

        assert config_file.read_text() == first
        assert config_file.stat().st_mtime_ns == old_mtime_ns
        assert list(tmp_path.glob("mcp.backup_*.json")) == []

    def test_repeated_plugin_install_does_not_rewrite_or_create_backup(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        config_file = tmp_path / ".claude.json"
        monkeypatch.setattr(
            setup,
            "_get_install_client_config_path",
            lambda _: config_file,
        )
        plugins = [
            ("id1", "My Plugin", "https://example.com/api/v1/proxy/plugins/id1/mcp"),
        ]

        assert _install_plugins_to_client(InstallClient.CLAUDE_CODE, plugins) == 1
        first = config_file.read_text()
        old_mtime_ns = 1_000_000_000
        os.utime(config_file, ns=(old_mtime_ns, old_mtime_ns))

        assert _install_plugins_to_client(InstallClient.CLAUDE_CODE, plugins) == 1

        assert config_file.read_text() == first
        assert config_file.stat().st_mtime_ns == old_mtime_ns
        assert list(tmp_path.glob(".claude.backup_*.json")) == []


def test_non_interactive_install_exits_nonzero_for_malformed_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config_file = tmp_path / "mcp.json"
    config_file.write_text("{invalid")
    monkeypatch.setattr(
        setup,
        "_get_install_client_config_path",
        lambda _: config_file,
    )
    monkeypatch.setattr(
        setup, "set_credentials_in_context", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        setup,
        "resolve_credentials",
        lambda *args, **kwargs: {
            "secret": "secret",
            "host": "https://example.com",
        },
    )
    monkeypatch.setattr(
        setup,
        "RunlayerClient",
        lambda *args, **kwargs: _FakeInstallApiClient(),
    )

    with pytest.raises(typer.Exit) as exc_info:
        setup.install(
            ctx=cast(Any, object()),
            client=InstallClient.CURSOR,
            server_ids=["abc123"],
            plugin_ids=None,
            header=None,
            interactive=False,
            secret=None,
            host=None,
            yes=True,
        )

    output = capsys.readouterr().out
    assert exc_info.value.exit_code == 1
    assert "Cannot read" in output
    assert "Installation complete" not in output


def test_non_interactive_install_stops_after_filesystem_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config_file = tmp_path / ".claude.json"
    original = '{"mcpServers": {"existing": {"url": "https://existing"}}}'
    config_file.write_text(original)
    real_write = setup._write_config_file
    failed_once = False

    def fail_first_write(
        path: Path, config: dict[str, Any], config_format: str
    ) -> None:
        nonlocal failed_once
        if not failed_once:
            failed_once = True
            path.write_text("")
            raise OSError("disk full")
        real_write(path, config, config_format)

    monkeypatch.setattr(
        setup,
        "_get_install_client_config_path",
        lambda _: config_file,
    )
    monkeypatch.setattr(setup, "_write_config_file", fail_first_write)
    monkeypatch.setattr(
        setup, "set_credentials_in_context", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        setup,
        "resolve_credentials",
        lambda *args, **kwargs: {
            "secret": "secret",
            "host": "https://example.com",
        },
    )
    monkeypatch.setattr(
        setup,
        "RunlayerClient",
        lambda *args, **kwargs: _FakeInteractiveInstallApiClient(),
    )

    with pytest.raises(typer.Exit) as exc_info:
        setup.install(
            ctx=cast(Any, object()),
            client=InstallClient.CLAUDE_CODE,
            server_ids=["abc123"],
            plugin_ids=["plugin123"],
            header=None,
            interactive=False,
            secret=None,
            host=None,
            yes=True,
        )

    output = capsys.readouterr().out
    assert exc_info.value.exit_code == 1
    assert "disk full" in output
    assert "Installation complete" not in output
    assert config_file.read_text() == ""
    backups = list(tmp_path.glob(".claude.backup_*.json"))
    assert len(backups) == 1
    assert backups[0].read_text() == original


def test_successful_install_of_colliding_batch_still_reports_a_count(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A non-empty successful batch never reports zero, even when names collide."""
    config_file = tmp_path / "mcp.json"
    monkeypatch.setattr(
        setup,
        "_get_install_client_config_path",
        lambda _: config_file,
    )
    specs = [
        InstallServerSpec(
            server_id=server_id,
            name=name,
            proxy_url="https://example.com/mcp",
            host="https://example.com",
            is_local=False,
        )
        for server_id, name in (("abc123", "New Server"), ("def456", "new server"))
    ]

    assert _install_servers_to_client(InstallClient.CURSOR, specs) == 1


def test_install_does_not_overwrite_non_mapping_config_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_file = tmp_path / "mcp.json"
    original = '["not", "an", "object"]'
    config_file.write_text(original)
    monkeypatch.setattr(
        setup,
        "_get_install_client_config_path",
        lambda _: config_file,
    )
    spec = InstallServerSpec(
        server_id="abc123",
        name="New Server",
        proxy_url="https://example.com/mcp",
        host="https://example.com",
        is_local=False,
    )

    with pytest.raises(setup.InstallError):
        _install_servers_to_client(InstallClient.CURSOR, [spec])
    assert config_file.read_text() == original
    assert list(tmp_path.glob("mcp.backup_*.json")) == []


def test_install_does_not_overwrite_non_mapping_server_section(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_file = tmp_path / "mcp.json"
    original = '{"mcpServers": ["not", "an", "object"]}'
    config_file.write_text(original)
    monkeypatch.setattr(
        setup,
        "_get_install_client_config_path",
        lambda _: config_file,
    )
    spec = InstallServerSpec(
        server_id="abc123",
        name="New Server",
        proxy_url="https://example.com/mcp",
        host="https://example.com",
        is_local=False,
    )

    with pytest.raises(setup.InstallError):
        _install_servers_to_client(InstallClient.CLAUDE_CODE, [spec])
    assert config_file.read_text() == original
    assert list(tmp_path.glob("mcp.backup_*.json")) == []


def test_interactive_install_exits_nonzero_when_selected_install_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_install(*args: Any, **kwargs: Any) -> int:
        raise setup.InstallError("config unusable")

    monkeypatch.setattr(setup, "_interactive_select", lambda *args, **kwargs: [0])
    monkeypatch.setattr(setup, "_install_servers_to_client", fail_install)

    with pytest.raises(typer.Exit) as exc_info:
        setup._run_interactive_install(
            _FakeInstallApiClient(),
            "https://example.com",
            InstallClient.CURSOR,
            yes=True,
        )

    assert exc_info.value.exit_code == 1


def test_interactive_install_stops_after_filesystem_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    install_types = iter(["servers", "plugins"])
    install_more = iter([True, False])
    attempted: list[str] = []

    def fail_server_install(*args: Any, **kwargs: Any) -> int:
        attempted.append("servers")
        raise OSError("disk full")

    def install_plugins(*args: Any, **kwargs: Any) -> int:
        attempted.append("plugins")
        return 1

    monkeypatch.setattr(
        setup.questionary,
        "select",
        lambda *args, **kwargs: _Prompt(next(install_types)),
    )
    monkeypatch.setattr(
        setup.questionary,
        "confirm",
        lambda *args, **kwargs: _Prompt(next(install_more)),
    )
    monkeypatch.setattr(setup, "_interactive_select", lambda *args, **kwargs: [0])
    monkeypatch.setattr(setup, "_install_servers_to_client", fail_server_install)
    monkeypatch.setattr(setup, "_install_plugins_to_client", install_plugins)

    with pytest.raises(typer.Exit) as exc_info:
        setup._run_interactive_install(
            _FakeInteractiveInstallApiClient(),
            "https://example.com",
            InstallClient.CLAUDE_CODE,
            yes=True,
        )

    output = capsys.readouterr().out
    assert exc_info.value.exit_code == 1
    assert attempted == ["servers"]
    assert "disk full" in output
    assert "Installation complete" not in output
    assert "No items were installed" not in output


def test_interactive_partial_failure_never_reports_installation_complete(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    install_types = iter(["servers", "plugins"])
    install_more = iter([True, False])
    installed_batches: list[str] = []

    def install_servers(*args: Any, **kwargs: Any) -> int:
        installed_batches.append("servers")
        return 1

    def install_plugins(*args: Any, **kwargs: Any) -> int:
        installed_batches.append("plugins")
        raise setup.InstallError("config unusable")

    monkeypatch.setattr(
        setup.questionary,
        "select",
        lambda *args, **kwargs: _Prompt(next(install_types)),
    )
    monkeypatch.setattr(
        setup.questionary,
        "confirm",
        lambda *args, **kwargs: _Prompt(next(install_more)),
    )
    monkeypatch.setattr(setup, "_interactive_select", lambda *args, **kwargs: [0])
    monkeypatch.setattr(
        setup,
        "_install_servers_to_client",
        install_servers,
    )
    monkeypatch.setattr(
        setup,
        "_install_plugins_to_client",
        install_plugins,
    )
    monkeypatch.setattr(
        setup, "set_credentials_in_context", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        setup,
        "resolve_credentials",
        lambda *args, **kwargs: {
            "secret": "secret",
            "host": "https://example.com",
        },
    )
    monkeypatch.setattr(
        setup,
        "RunlayerClient",
        lambda *args, **kwargs: _FakeInteractiveInstallApiClient(),
    )

    result = CliRunner().invoke(
        setup.app,
        [
            "install",
            "--interactive",
            "--client",
            "claude_code",
            "--yes",
        ],
    )

    assert installed_batches == ["servers", "plugins"]
    assert result.exit_code == 1, result.output
    assert "partially failed" in result.output.lower()
    assert "Installation complete" not in result.output
    assert "Restart Claude Code" not in result.output


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

    def test_install_uses_utf8_for_non_ascii_config(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        config_file = tmp_path / "mcp.json"
        config_file.write_text(
            json.dumps({"note": "café", "mcpServers": {}}, ensure_ascii=False),
            encoding="utf-8",
        )
        read_text = Path.read_text
        write_text = Path.write_text

        def require_utf8_read(
            path: Path,
            encoding: str | None = None,
            errors: str | None = None,
        ) -> str:
            if encoding != "utf-8":
                raise UnicodeDecodeError("cp1252", b"\x81", 0, 1, "undefined")
            return read_text(path, encoding=encoding, errors=errors)

        def require_utf8_write(
            path: Path,
            data: str,
            encoding: str | None = None,
            errors: str | None = None,
        ) -> int:
            if encoding != "utf-8":
                raise UnicodeEncodeError("ascii", "é", 0, 1, "undefined")
            return write_text(path, data, encoding=encoding, errors=errors)

        monkeypatch.setattr(Path, "read_text", require_utf8_read)
        monkeypatch.setattr(Path, "write_text", require_utf8_write)
        monkeypatch.setattr(
            setup,
            "_get_install_client_config_path",
            lambda _: config_file,
        )
        spec = InstallServerSpec(
            server_id="abc123",
            name="New Server",
            proxy_url="https://example.com/mcp",
            host="https://example.com",
            is_local=False,
        )

        assert _install_servers_to_client(InstallClient.CURSOR, [spec]) == 1
        final = json.loads(read_text(config_file, encoding="utf-8"))
        assert final["note"] == "café"
        assert "new-server" in final["mcpServers"]
