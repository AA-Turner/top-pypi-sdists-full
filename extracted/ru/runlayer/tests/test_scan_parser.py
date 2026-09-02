"""Tests for config file parsing."""

import hashlib
import json
import os
from pathlib import Path

import pytest

from runlayer_cli.scan.clients import (
    MCPClientDefinition,
    get_all_clients,
    get_client_by_name,
)
from runlayer_cli.scan.config_parser import (
    _ENTRY_PARSERS,
    MCPServerConfig,
    compute_config_hash,
    normalize_transport,
    parse_client_mcp_entries,
    parse_config_file,
)


def make_client_def(servers_key: str = "mcpServers") -> MCPClientDefinition:
    """Create a test client definition."""
    return MCPClientDefinition(
        name="test",
        display_name="Test Client",
        paths=[],
        servers_key=servers_key,
    )


def test_all_client_entry_formats_have_registered_parsers():
    missing = {
        client.entry_format
        for client in get_all_clients()
        if client.entry_format not in _ENTRY_PARSERS
    }
    assert missing == set()


def test_entry_format_selects_parser_independently_of_client_name():
    client = MCPClientDefinition(
        name="custom_opencode_client",
        display_name="Custom OpenCode Client",
        paths=[],
        servers_key="mcp",
        entry_format="opencode",
    )

    servers = parse_client_mcp_entries(
        client,
        {
            "mcp": {
                "filesystem": {
                    "type": "local",
                    "command": ["npx", "-y", "server-filesystem"],
                }
            }
        },
    )

    assert len(servers) == 1
    assert servers[0].command == "npx"
    assert servers[0].args == ["-y", "server-filesystem"]


@pytest.fixture
def fixtures_dir():
    """Return path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.mark.parametrize(
    ("explicit", "has_url", "expected"),
    [
        (None, False, "stdio"),
        ("", False, "stdio"),
        (None, True, "streaming-http"),
        ("stdio", False, "stdio"),
        ("sse", True, "sse"),
        ("http", True, "streaming-http"),
        ("http", False, "http"),
        ("streamable_http", True, "streaming-http"),
        ("streamable-http", True, "streaming-http"),
        ("streamablehttp", True, "streaming-http"),
        ("streaming_http", True, "streaming-http"),
        ("streaming-http", True, "streaming-http"),
        # url-less servers declared with an explicit streamable alias (rare /
        # malformed) still fold to the streaming-http vocabulary, matching the
        # backend's normalize_transport_type so the config_hash stays in lockstep.
        ("streamable_http", False, "streaming-http"),
        ("streamable-http", False, "streaming-http"),
        ("streamablehttp", False, "streaming-http"),
        ("streaming-http", False, "streaming-http"),
    ],
)
def test_normalize_transport(
    explicit: str | None, has_url: bool, expected: str
) -> None:
    assert normalize_transport(explicit, has_url=has_url) == expected


class TestComputeConfigHash:
    def test_same_config_same_hash(self):
        """Same configuration produces same hash."""
        server1 = MCPServerConfig(name="test", type="stdio", command="npx")
        server2 = MCPServerConfig(name="test", type="stdio", command="npx")
        assert compute_config_hash(server1) == compute_config_hash(server2)

    def test_different_name_different_hash(self):
        """Different names produce different hashes."""
        server1 = MCPServerConfig(name="test1", type="stdio", command="npx")
        server2 = MCPServerConfig(name="test2", type="stdio", command="npx")
        assert compute_config_hash(server1) != compute_config_hash(server2)

    def test_env_excluded_from_hash(self):
        """Environment variables don't affect hash."""
        server1 = MCPServerConfig(
            name="test", type="stdio", command="npx", env={"KEY": "value1"}
        )
        server2 = MCPServerConfig(
            name="test", type="stdio", command="npx", env={"KEY": "value2"}
        )
        assert compute_config_hash(server1) == compute_config_hash(server2)

    def test_hash_is_64_chars(self):
        """Hash is full SHA-256 (64 hex chars)."""
        server = MCPServerConfig(name="test", type="stdio", command="npx")
        hash_value = compute_config_hash(server)
        assert len(hash_value) == 64

    def test_non_container_hash_unchanged(self):
        """A plain stdio server hashes exactly as the legacy canonical dict."""
        server = MCPServerConfig(
            name="gh", type="stdio", command="npx", args=["-y", "server-github"]
        )
        expected = hashlib.sha256(
            json.dumps(
                {
                    "name": "gh",
                    "type": "stdio",
                    "command": "npx",
                    "args": ["-y", "server-github"],
                    "url": None,
                },
                sort_keys=True,
            ).encode()
        ).hexdigest()
        assert compute_config_hash(server) == expected

    def test_container_flag_variations_same_image_ref(self):
        """Same image, different docker flags/order → same image_ref.

        config_hash now stays the legacy shape (differs per flag set); the
        backend dedups container servers by image_ref via its container_hash.
        """
        a = MCPServerConfig(
            name="gh", type="stdio", command="docker", args=["run", "-i", "mcp/github"]
        )
        b = MCPServerConfig(
            name="gh",
            type="stdio",
            command="docker",
            args=["run", "--rm", "-e", "TOKEN", "mcp/github"],
        )
        compute_config_hash(a)
        compute_config_hash(b)
        assert a.image_ref == b.image_ref == "oci:mcp/github:latest"

    def test_container_flag_variations_differ_in_config_hash(self):
        """Legacy config_hash reflects the raw command/args (no image fold)."""
        a = MCPServerConfig(
            name="gh", type="stdio", command="docker", args=["run", "-i", "mcp/github"]
        )
        b = MCPServerConfig(
            name="gh",
            type="stdio",
            command="docker",
            args=["run", "--rm", "-e", "TOKEN", "mcp/github"],
        )
        assert compute_config_hash(a) != compute_config_hash(b)

    def test_container_podman_matches_docker_image_ref(self):
        """docker vs podman resolve to the same image_ref."""
        d = MCPServerConfig(
            name="gh", type="stdio", command="docker", args=["run", "mcp/github"]
        )
        p = MCPServerConfig(
            name="gh", type="stdio", command="podman", args=["run", "mcp/github"]
        )
        compute_config_hash(d)
        compute_config_hash(p)
        assert d.image_ref == p.image_ref == "oci:mcp/github:latest"

    def test_container_different_image_different_image_ref(self):
        a = MCPServerConfig(
            name="x", type="stdio", command="docker", args=["run", "mcp/github"]
        )
        b = MCPServerConfig(
            name="x", type="stdio", command="docker", args=["run", "mcp/gitlab"]
        )
        compute_config_hash(a)
        compute_config_hash(b)
        assert a.image_ref != b.image_ref

    def test_container_config_hash_is_legacy_shape(self):
        """A container command still hashes off {name, type, command, args, url}."""
        server = MCPServerConfig(
            name="gh", type="stdio", command="docker", args=["run", "-i", "mcp/github"]
        )
        expected = hashlib.sha256(
            json.dumps(
                {
                    "name": "gh",
                    "type": "stdio",
                    "command": "docker",
                    "args": ["run", "-i", "mcp/github"],
                    "url": None,
                },
                sort_keys=True,
            ).encode()
        ).hexdigest()
        assert compute_config_hash(server) == expected

    def test_compute_hash_populates_container_fields(self):
        """The hash choke point also sets runtime/image identity on the server."""
        server = MCPServerConfig(
            name="gh", type="stdio", command="docker", args=["run", "mcp/github"]
        )
        compute_config_hash(server)
        assert server.runtime == "container"
        assert server.image_ref == "oci:mcp/github:latest"

    def test_compute_hash_resets_fields_for_host_command(self):
        """A stale container classification is cleared when the command changes."""
        server = MCPServerConfig(
            name="gh", type="stdio", command="docker", args=["run", "mcp/github"]
        )
        compute_config_hash(server)
        server.command = "npx"
        server.args = ["-y", "server-github"]
        compute_config_hash(server)
        assert server.runtime == "host"
        assert server.image_ref is None

    @pytest.mark.parametrize(
        "transport", ["sse", "http", "streamable-http", "streaming-http"]
    )
    def test_remote_transports_share_one_identity_hash(self, transport: str):
        """url-bearing transports fold to one identity: a transport flip (e.g.
        the sse -> streaming-http remote default change) must not re-key the
        backend catalog row."""
        flipped = MCPServerConfig(
            name="linear", type=transport, url="https://mcp.linear.app/sse"
        )
        baseline = MCPServerConfig(
            name="linear", type="sse", url="https://mcp.linear.app/sse"
        )
        assert compute_config_hash(flipped) == compute_config_hash(baseline)

    def test_remote_hash_uses_remote_bucket_shape(self):
        """Remote entries hash off {name, "remote", command, args, url} — the
        exact shape the backend and the re-key migration reproduce."""
        server = MCPServerConfig(
            name="linear", type="streamable-http", url="https://mcp.linear.app/sse"
        )
        expected = hashlib.sha256(
            json.dumps(
                {
                    "name": "linear",
                    "type": "remote",
                    "command": None,
                    "args": [],
                    "url": "https://mcp.linear.app/sse",
                },
                sort_keys=True,
            ).encode()
        ).hexdigest()
        assert compute_config_hash(server) == expected

    def test_remote_bucket_does_not_fold_different_urls(self):
        """The fold is transport-only: same name, different url stays distinct."""
        a = MCPServerConfig(name="linear", type="sse", url="https://a.example/sse")
        b = MCPServerConfig(name="linear", type="sse", url="https://b.example/sse")
        assert compute_config_hash(a) != compute_config_hash(b)

    def test_urlless_streamable_hashes_on_streaming_http_bucket(self):
        """A url-less server declared with a streamable alias keeps its declared
        type in the identity bucket (no url -> no "remote" fold). Every alias
        normalizes to streaming-http first, so they share one hash — and that
        hash is byte-identical to the backend's recomputed catalog identity for
        the same fields (see the backend TestRemoteTransportIdentity)."""
        expected = hashlib.sha256(
            json.dumps(
                {
                    "name": "stream",
                    "type": "streaming-http",
                    "command": None,
                    "args": [],
                    "url": None,
                },
                sort_keys=True,
            ).encode()
        ).hexdigest()
        for alias in (
            "streamable-http",
            "streamable_http",
            "streamablehttp",
            "streaming-http",
        ):
            server = MCPServerConfig(
                name="stream",
                type=normalize_transport(alias, has_url=False),
            )
            assert compute_config_hash(server) == expected


class TestParseConfigFile:
    def test_nonexistent_file_returns_none(self, tmp_path):
        """Non-existent file returns None."""
        client_def = make_client_def()
        result = parse_config_file(client_def, tmp_path / "nonexistent.json")
        assert result is None

    def test_invalid_json_returns_none(self, tmp_path):
        """Invalid JSON returns None."""
        config_file = tmp_path / "config.json"
        config_file.write_text("not valid json")
        client_def = make_client_def()
        result = parse_config_file(client_def, config_file)
        assert result is None

    @pytest.mark.skipif(
        os.name == "nt" or getattr(os, "geteuid", lambda: -1)() == 0,
        reason="EACCES-on-cwd repro needs POSIX and a non-root user",
    )
    def test_relative_path_with_unsearchable_cwd_returns_none(self, tmp_path):
        """A candidate path that stats EACCES must be skipped, not crash the scan.

        Repro for the Linux aiwatch fleet crash: run-aiwatch-scan.sh children
        inherit root's cwd (/root via cron), the cline_cli candidate
        "$CLINE_DIR/..." is left unexpanded as a relative path, and on
        Python 3.13 Path.exists() propagates the PermissionError from the
        unsearchable cwd instead of returning False.
        """
        locked = tmp_path / "locked"
        locked.mkdir()
        old_cwd = os.getcwd()
        os.chdir(locked)
        locked.chmod(0)
        try:
            result = parse_config_file(
                make_client_def(),
                Path("$CLINE_DIR/data/settings/cline_mcp_settings.json"),
            )
        finally:
            locked.chmod(0o700)
            os.chdir(old_cwd)
        assert result is None

    def test_empty_json_returns_none(self, tmp_path, caplog):
        """Empty JSON file returns None without a parse-error warning."""
        config_file = tmp_path / "config.json"
        config_file.write_text("")
        client_def = make_client_def()
        result = parse_config_file(client_def, config_file)
        assert result is None
        assert "Failed to parse" not in caplog.text

    def test_whitespace_only_json_returns_none(self, tmp_path, caplog):
        """Whitespace-only JSON file returns None without a parse-error warning."""
        config_file = tmp_path / "config.json"
        config_file.write_text("\n  \n")
        client_def = make_client_def()
        result = parse_config_file(client_def, config_file)
        assert result is None
        assert "Failed to parse" not in caplog.text

    def test_empty_servers_returns_none(self, tmp_path):
        """Config with no servers returns None."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({"mcpServers": {}}))
        client_def = make_client_def()
        result = parse_config_file(client_def, config_file)
        assert result is None

    def test_parses_stdio_server(self, tmp_path):
        """Parses stdio server configuration."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "test-server": {
                            "command": "npx",
                            "args": ["-y", "@modelcontextprotocol/server-test"],
                        }
                    }
                }
            )
        )
        client_def = MCPClientDefinition(
            name="cursor",
            display_name="Cursor",
            paths=[],
            servers_key="mcpServers",
        )
        result = parse_config_file(client_def, config_file)
        assert result is not None
        assert result.client == "cursor"
        assert len(result.servers) == 1
        assert result.servers[0].name == "test-server"
        assert result.servers[0].type == "stdio"
        assert result.servers[0].command == "npx"

    @pytest.mark.parametrize(
        "command",
        ["npx\nrm -rf /", "npx\t--yes", ["npx", "--yes"]],
        ids=["newline", "control-character", "non-string"],
    )
    def test_invalid_command_is_flagged_without_dropping_server(
        self, tmp_path, command
    ):
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps({"mcpServers": {"invalid": {"command": command}}})
        )

        result = parse_config_file(make_client_def(), config_file)

        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].command_invalid is True
        if not isinstance(command, str):
            assert result.servers[0].command is None

    def test_claude_json_newline_command_is_flagged(self, tmp_path):
        config_file = tmp_path / ".claude.json"
        config_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "broken": {
                            "command": "uvx\nmalicious",
                        }
                    }
                }
            )
        )

        result = parse_config_file(get_client_by_name("claude_code"), config_file)

        assert result is not None
        assert len(result.servers) == 1
        server = result.servers[0]
        assert server.command_invalid is True
        assert (
            server.command_invalid_reason
            == "command must not contain newlines or control characters"
        )

    def test_parses_sse_server(self, tmp_path):
        """Parses SSE server configuration."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "remote-server": {
                            "url": "https://example.com/mcp",
                            "transport": "sse",
                        }
                    }
                }
            )
        )
        client_def = make_client_def()
        result = parse_config_file(client_def, config_file)
        assert result is not None
        assert result.servers[0].type == "sse"
        assert result.servers[0].url == "https://example.com/mcp"

    def test_parses_http_server_from_type_field(self, tmp_path):
        """Parses remote server with explicit type=http."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "remote-server": {
                            "type": "http",
                            "url": "https://example.com/mcp",
                        }
                    }
                }
            )
        )
        client_def = make_client_def()
        result = parse_config_file(client_def, config_file)
        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].type == "streaming-http"
        assert result.servers[0].url == "https://example.com/mcp"

    def test_parses_windsurf_server_url_field(self, tmp_path):
        """Parses Windsurf remote server using serverUrl."""
        config_file = tmp_path / "mcp_config.json"
        config_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "runlayer": {
                            "serverUrl": "https://example.com/mcp",
                        }
                    }
                }
            )
        )
        client_def = get_client_by_name("windsurf")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].type == "streaming-http"
        assert result.servers[0].url == "https://example.com/mcp"

    def test_normalizes_streamable_http_transport(self, tmp_path):
        """Normalizes streamable_http transport to streaming-http."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "remote-server": {
                            "transport": "streamable_http",
                            "url": "https://example.com/mcp",
                        }
                    }
                }
            )
        )
        client_def = make_client_def()
        result = parse_config_file(client_def, config_file)
        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].type == "streaming-http"
        assert result.servers[0].url == "https://example.com/mcp"

    def test_parses_custom_servers_key(self, tmp_path):
        """Parses config with non-standard servers key."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps(
                {
                    "mcp": {
                        "servers": {
                            "custom-server": {"command": "node", "args": ["server.js"]}
                        }
                    }
                }
            )
        )
        client_def = make_client_def(servers_key="mcp.servers")
        result = parse_config_file(client_def, config_file)
        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].name == "custom-server"

    def test_parses_root_level_servers(self, tmp_path):
        """Parses config with servers at root level."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps(
                {
                    "my-server": {"command": "npx", "args": ["-y", "some-package"]},
                    "another-server": {"url": "https://api.example.com/mcp"},
                }
            )
        )
        client_def = make_client_def(servers_key="")
        result = parse_config_file(client_def, config_file)
        assert result is not None
        assert len(result.servers) == 2

    def test_parses_cursor_config_with_comments(self, tmp_path):
        """Cursor config with JSONC comments is parsed correctly."""
        config_file = tmp_path / "mcp.json"
        config_file.write_text(
            """// Cursor MCP configuration
{
  // MCP servers
  "mcpServers": {
    "my-server": {
      "command": "npx", // Run with npx
      "args": ["-y", "some-package"]
    }
  }
}
"""
        )
        client_def = get_client_by_name("cursor")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].name == "my-server"

    def test_parses_vscode_config_with_comments(self, tmp_path):
        """VS Code config with JSONC comments is parsed correctly."""
        config_file = tmp_path / "mcp.json"
        config_file.write_text(
            """// VS Code MCP configuration
/* This is a block comment */
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"]
    }
  }
}
"""
        )
        client_def = get_client_by_name("vscode")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].name == "filesystem"

    def test_parses_windsurf_config_with_comments(self, tmp_path):
        """Windsurf config with JSONC comments is parsed correctly."""
        config_file = tmp_path / "mcp_config.json"
        config_file.write_text(
            """// Windsurf MCP configuration
{
  "mcpServers": {
    // Database server
    "database": {
      "command": "node",
      "args": ["server.js"]
    }
  }
}
"""
        )
        client_def = get_client_by_name("windsurf")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].name == "database"

    def test_parses_opencode_local_server(self, tmp_path):
        """OpenCode local servers use type=local and command as an array."""
        config_file = tmp_path / "opencode.json"
        config_file.write_text(
            json.dumps(
                {
                    "mcp": {
                        "runlayer": {
                            "type": "local",
                            "enabled": True,
                            "command": ["uvx", "runlayer", "run", "abc123"],
                            "environment": {"RUNLAYER_HOST": "https://example.com"},
                        }
                    }
                }
            )
        )
        client_def = get_client_by_name("opencode")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is not None
        assert result.client == "opencode"
        assert len(result.servers) == 1
        server = result.servers[0]
        assert server.name == "runlayer"
        assert server.type == "stdio"
        assert server.command == "uvx"
        assert server.args == ["runlayer", "run", "abc123"]
        assert server.env == {"RUNLAYER_HOST": "https://example.com"}
        assert server.url is None

    def test_parses_opencode_remote_server(self, tmp_path):
        """OpenCode remote servers use type=remote with url + headers."""
        config_file = tmp_path / "opencode.json"
        config_file.write_text(
            json.dumps(
                {
                    "mcp": {
                        "runlayer": {
                            "type": "remote",
                            "enabled": True,
                            "url": "https://example.com/mcp",
                            "headers": {"Authorization": "Bearer token"},
                        }
                    }
                }
            )
        )
        client_def = get_client_by_name("opencode")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is not None
        assert len(result.servers) == 1
        server = result.servers[0]
        assert server.name == "runlayer"
        assert server.type == "streaming-http"
        assert server.url == "https://example.com/mcp"
        assert server.headers == {"Authorization": "Bearer token"}

    def test_opencode_skips_disabled_server(self, tmp_path):
        """OpenCode parser skips servers with enabled=false."""
        config_file = tmp_path / "opencode.json"
        config_file.write_text(
            json.dumps(
                {
                    "mcp": {
                        "disabled": {
                            "type": "local",
                            "enabled": False,
                            "command": ["npx", "-y", "x"],
                        }
                    }
                }
            )
        )
        client_def = get_client_by_name("opencode")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is None


class TestParseConfigFileWithFixtures:
    def test_parse_cursor_config(self, fixtures_dir):
        """Parse real Cursor config fixture."""
        client_def = get_client_by_name("cursor")
        assert client_def is not None
        result = parse_config_file(client_def, fixtures_dir / "cursor_config.json")

        assert result is not None
        assert len(result.servers) == 2
        server_names = [s.name for s in result.servers]
        assert "filesystem" in server_names
        assert "github" in server_names

    def test_parse_warp_config(self, fixtures_dir):
        """Parse Warp config fixture (mcpServers with stdio + remote)."""
        client_def = get_client_by_name("warp")
        assert client_def is not None
        result = parse_config_file(client_def, fixtures_dir / "warp_config.json")

        assert result is not None
        assert len(result.servers) == 2
        by_name = {s.name: s for s in result.servers}
        assert by_name["filesystem"].type == "stdio"
        assert by_name["filesystem"].command == "npx"
        assert by_name["github-remote"].type == "streaming-http"
        assert by_name["github-remote"].url == "https://api.githubcopilot.com/mcp/"

    def test_parse_vscode_config_with_servers_key(self, fixtures_dir):
        """Parse VS Code config which uses 'servers' not 'mcpServers'."""
        client_def = get_client_by_name("vscode")
        assert client_def is not None
        result = parse_config_file(client_def, fixtures_dir / "vscode_config.json")

        assert result is not None
        assert len(result.servers) == 2
        server_names = [s.name for s in result.servers]
        assert "github-copilot" in server_names
        assert "filesystem" in server_names

    def test_vscode_config_not_parsed_with_wrong_key(self, fixtures_dir):
        """VS Code config should NOT parse if using wrong servers_key."""
        # Try to parse VS Code config with wrong key
        wrong_client_def = MCPClientDefinition(
            name="test",
            display_name="Test",
            paths=[],
            servers_key="mcpServers",  # Wrong! VS Code uses "servers"
        )
        result = parse_config_file(
            wrong_client_def, fixtures_dir / "vscode_config.json"
        )

        # Should return None because mcpServers key doesn't exist
        assert result is None

    def test_parse_sse_server(self, fixtures_dir):
        """Parse SSE server config fixture."""
        client_def = MCPClientDefinition(
            name="test",
            display_name="Test",
            paths=[],
            servers_key="mcpServers",
        )
        result = parse_config_file(client_def, fixtures_dir / "sse_server_config.json")

        assert result is not None
        assert result.servers[0].type == "sse"
        assert result.servers[0].url == "https://api.example.com/mcp/sse"
        assert result.servers[0].headers is not None

    def test_parse_claude_code_with_projects(self, fixtures_dir):
        """Parse Claude Code config with both global and project servers."""
        client_def = get_client_by_name("claude_code")
        assert client_def is not None
        result = parse_config_file(client_def, fixtures_dir / "claude_code_config.json")

        assert result is not None
        # Should have 3 servers: 1 global + 2 project-specific
        assert len(result.servers) == 3
        server_names = [s.name for s in result.servers]
        assert "global-server" in server_names
        # Project servers are prefixed with project path
        assert any("project-a-server" in name for name in server_names)
        assert any("project-b-server" in name for name in server_names)

    def test_parse_claude_desktop_extensions_format(self, fixtures_dir):
        """Parse Claude Desktop config with extensions format."""
        client_def = get_client_by_name("claude_desktop")
        assert client_def is not None
        result = parse_config_file(
            client_def, fixtures_dir / "claude_desktop_config.json"
        )

        assert result is not None
        assert len(result.servers) == 2
        server_names = [s.name for s in result.servers]
        # Should use display_name from manifest
        assert "Read and Write Apple Notes" in server_names
        assert "Filesystem" in server_names

        # Check that command was parsed from mcp_config
        notes_server = next(
            s for s in result.servers if s.name == "Read and Write Apple Notes"
        )
        assert notes_server.command == "node"
        assert notes_server.args == ["${__dirname}/server/index.js"]
        assert notes_server.type == "stdio"  # "node" is mapped to "stdio"
        assert notes_server.env == {"HOME": "${HOME}"}


class TestParseGooseConfig:
    """Tests for Goose YAML config parsing."""

    def test_parse_goose_config(self, fixtures_dir):
        """Parse Goose config file with enabled MCP extensions."""
        client_def = get_client_by_name("goose")
        assert client_def is not None
        result = parse_config_file(client_def, fixtures_dir / "goose_config.yaml")

        assert result is not None
        assert result.client == "goose"
        # Should have 4 servers: context7, filesystem (stdio), remote_sse (sse),
        # remote_streamable (streamable_http)
        # Should skip: extensionmanager (platform), todo (platform), developer (builtin),
        # disabled_server (disabled), disabled_sse (disabled)
        assert len(result.servers) == 4
        server_names = [s.name for s in result.servers]
        assert "Context7" in server_names
        assert "Filesystem" in server_names
        assert "Remote SSE Server" in server_names
        assert "Remote Streamable HTTP" in server_names

    def test_goose_skips_disabled_extensions(self, fixtures_dir):
        """Goose parser skips extensions with enabled=false."""
        client_def = get_client_by_name("goose")
        assert client_def is not None
        result = parse_config_file(client_def, fixtures_dir / "goose_config.yaml")

        assert result is not None
        server_names = [s.name for s in result.servers]
        # disabled_server and disabled_sse should not be included
        assert "Disabled Server" not in server_names
        assert "Disabled SSE Server" not in server_names

    def test_goose_skips_platform_type(self, fixtures_dir):
        """Goose parser skips extensions with type=platform."""
        client_def = get_client_by_name("goose")
        assert client_def is not None
        result = parse_config_file(client_def, fixtures_dir / "goose_config.yaml")

        assert result is not None
        server_names = [s.name for s in result.servers]
        # Extension Manager and todo are platform type
        assert "Extension Manager" not in server_names
        assert "todo" not in server_names

    def test_goose_skips_builtin_type(self, fixtures_dir):
        """Goose parser skips extensions with type=builtin."""
        client_def = get_client_by_name("goose")
        assert client_def is not None
        result = parse_config_file(client_def, fixtures_dir / "goose_config.yaml")

        assert result is not None
        server_names = [s.name for s in result.servers]
        # developer is builtin type
        assert "developer" not in server_names
        assert "Developer" not in server_names

    def test_goose_maps_cmd_to_command(self, fixtures_dir):
        """Goose parser maps 'cmd' field to 'command'."""
        client_def = get_client_by_name("goose")
        assert client_def is not None
        result = parse_config_file(client_def, fixtures_dir / "goose_config.yaml")

        assert result is not None
        context7_server = next(s for s in result.servers if s.name == "Context7")
        assert context7_server.command == "npx"
        assert context7_server.args == ["-y", "@upstash/context7-mcp"]

    def test_goose_maps_envs_to_env(self, fixtures_dir):
        """Goose parser maps 'envs' field to 'env'."""
        client_def = get_client_by_name("goose")
        assert client_def is not None
        result = parse_config_file(client_def, fixtures_dir / "goose_config.yaml")

        assert result is not None
        filesystem_server = next(s for s in result.servers if s.name == "Filesystem")
        assert filesystem_server.env == {"HOME": "/Users/test"}

    def test_goose_stdio_servers_have_correct_type(self, fixtures_dir):
        """Goose stdio servers should have type 'stdio'."""
        client_def = get_client_by_name("goose")
        assert client_def is not None
        result = parse_config_file(client_def, fixtures_dir / "goose_config.yaml")

        assert result is not None
        context7_server = next(s for s in result.servers if s.name == "Context7")
        assert context7_server.type == "stdio"
        filesystem_server = next(s for s in result.servers if s.name == "Filesystem")
        assert filesystem_server.type == "stdio"

    def test_goose_sse_server_parsed_correctly(self, fixtures_dir):
        """Goose SSE server should have correct type and uri mapped to url."""
        client_def = get_client_by_name("goose")
        assert client_def is not None
        result = parse_config_file(client_def, fixtures_dir / "goose_config.yaml")

        assert result is not None
        sse_server = next(s for s in result.servers if s.name == "Remote SSE Server")
        assert sse_server.type == "sse"
        assert sse_server.url == "https://api.example.com/mcp/sse"
        assert sse_server.command is None
        assert sse_server.args is None
        assert sse_server.headers == {"Authorization": "Bearer token123"}

    def test_goose_streamable_http_server_parsed_correctly(self, fixtures_dir):
        """Goose streamable_http input maps to streaming-http and uri to url."""
        client_def = get_client_by_name("goose")
        assert client_def is not None
        result = parse_config_file(client_def, fixtures_dir / "goose_config.yaml")

        assert result is not None
        stream_server = next(
            s for s in result.servers if s.name == "Remote Streamable HTTP"
        )
        assert stream_server.type == "streaming-http"
        assert stream_server.url == "https://api.example.com/mcp/stream"
        assert stream_server.command is None
        assert stream_server.args is None
        assert stream_server.env == {"API_KEY": "secret"}

    def test_goose_servers_have_config_hash(self, fixtures_dir):
        """Parsed Goose servers should have a config hash."""
        client_def = get_client_by_name("goose")
        assert client_def is not None
        result = parse_config_file(client_def, fixtures_dir / "goose_config.yaml")

        assert result is not None
        for server in result.servers:
            assert server.config_hash != ""
            assert len(server.config_hash) == 64  # SHA-256 hex


class TestParseYAMLConfig:
    """Tests for YAML config file parsing."""

    def test_invalid_yaml_returns_none(self, tmp_path):
        """Invalid YAML returns None."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("invalid: yaml: content: [")
        client_def = MCPClientDefinition(
            name="goose",
            display_name="Goose",
            paths=[],
            servers_key="extensions",
            config_format="yaml",
            entry_format="goose",
        )
        result = parse_config_file(client_def, config_file)
        assert result is None

    def test_empty_yaml_returns_none(self, tmp_path):
        """Empty YAML file returns None."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("")
        client_def = MCPClientDefinition(
            name="goose",
            display_name="Goose",
            paths=[],
            servers_key="extensions",
            config_format="yaml",
            entry_format="goose",
        )
        result = parse_config_file(client_def, config_file)
        assert result is None

    def test_yaml_with_no_enabled_extensions_returns_none(self, tmp_path):
        """YAML with no enabled stdio extensions returns None."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("""
extensions:
  disabled_ext:
    enabled: false
    type: stdio
    cmd: npx
    args: ["-y", "some-package"]
  platform_ext:
    enabled: true
    type: platform
    bundled: true
""")
        client_def = MCPClientDefinition(
            name="goose",
            display_name="Goose",
            paths=[],
            servers_key="extensions",
            config_format="yaml",
            entry_format="goose",
        )
        result = parse_config_file(client_def, config_file)
        assert result is None


class TestParseZedConfig:
    """Tests for Zed context_servers parsing."""

    def test_parse_zed_stdio_server(self, tmp_path):
        """Parse Zed config with stdio (command-based) server."""
        config_file = tmp_path / "settings.json"
        config_file.write_text(
            json.dumps(
                {
                    "context_servers": {
                        "my-mcp-server": {
                            "enabled": True,
                            "command": "npx",
                            "args": ["-y", "@modelcontextprotocol/server-test"],
                            "env": {"TEST_VAR": "value"},
                        }
                    }
                }
            )
        )
        client_def = get_client_by_name("zed")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert result.client == "zed"
        assert len(result.servers) == 1
        assert result.servers[0].name == "my-mcp-server"
        assert result.servers[0].type == "stdio"
        assert result.servers[0].command == "npx"
        assert result.servers[0].args == ["-y", "@modelcontextprotocol/server-test"]
        assert result.servers[0].env == {"TEST_VAR": "value"}

    def test_parse_zed_remote_server(self, tmp_path):
        """Parse Zed config with remote (URL-based) server."""
        config_file = tmp_path / "settings.json"
        config_file.write_text(
            json.dumps(
                {
                    "context_servers": {
                        "remote-server": {
                            "enabled": True,
                            "url": "https://example.com/mcp",
                        }
                    }
                }
            )
        )
        client_def = get_client_by_name("zed")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].name == "remote-server"
        assert result.servers[0].type == "streaming-http"
        assert result.servers[0].url == "https://example.com/mcp"
        assert result.servers[0].command is None

    def test_parse_zed_remote_server_with_headers(self, tmp_path):
        """Parse Zed config with remote server including headers."""
        config_file = tmp_path / "settings.json"
        config_file.write_text(
            json.dumps(
                {
                    "context_servers": {
                        "remote-server": {
                            "enabled": True,
                            "url": "https://example.com/mcp",
                            "headers": {"X_AUTH": "test123", "X-API-Key": "secret"},
                        }
                    }
                }
            )
        )
        client_def = get_client_by_name("zed")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].name == "remote-server"
        assert result.servers[0].url == "https://example.com/mcp"
        assert result.servers[0].headers == {"X_AUTH": "test123", "X-API-Key": "secret"}

    def test_parse_zed_disabled_server(self, tmp_path):
        """Zed parser skips disabled servers."""
        config_file = tmp_path / "settings.json"
        config_file.write_text(
            json.dumps(
                {
                    "context_servers": {
                        "disabled-server": {
                            "enabled": False,
                            "command": "npx",
                            "args": ["-y", "some-package"],
                        },
                        "enabled-server": {
                            "enabled": True,
                            "command": "node",
                            "args": ["server.js"],
                        },
                    }
                }
            )
        )
        client_def = get_client_by_name("zed")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].name == "enabled-server"

    def test_parse_zed_extension_only_skipped(self, tmp_path):
        """Zed parser skips extension-only entries (settings but no command/url)."""
        config_file = tmp_path / "settings.json"
        config_file.write_text(
            json.dumps(
                {
                    "context_servers": {
                        "mcp-server-context7": {
                            "enabled": True,
                            "settings": {"context7_api_key": "secret"},
                        },
                        "real-server": {
                            "enabled": True,
                            "command": "node",
                            "args": ["server.js"],
                        },
                    }
                }
            )
        )
        client_def = get_client_by_name("zed")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        # Should only have the real server, not the extension-only entry
        assert len(result.servers) == 1
        assert result.servers[0].name == "real-server"

    def test_parse_zed_enabled_defaults_to_true(self, tmp_path):
        """Zed parser treats missing 'enabled' as true."""
        config_file = tmp_path / "settings.json"
        config_file.write_text(
            json.dumps(
                {
                    "context_servers": {
                        "no-enabled-field": {
                            "command": "npx",
                            "args": ["-y", "some-package"],
                        }
                    }
                }
            )
        )
        client_def = get_client_by_name("zed")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].name == "no-enabled-field"

    def test_parse_zed_servers_have_config_hash(self, tmp_path):
        """Parsed Zed servers should have a config hash."""
        config_file = tmp_path / "settings.json"
        config_file.write_text(
            json.dumps(
                {
                    "context_servers": {
                        "test-server": {
                            "enabled": True,
                            "command": "npx",
                            "args": ["-y", "test"],
                        }
                    }
                }
            )
        )
        client_def = get_client_by_name("zed")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert result.servers[0].config_hash != ""
        assert len(result.servers[0].config_hash) == 64  # SHA-256 hex

    def test_parse_zed_ignores_other_settings(self, tmp_path):
        """Zed parser ignores non-MCP settings."""
        config_file = tmp_path / "settings.json"
        config_file.write_text(
            json.dumps(
                {
                    "context_servers": {
                        "my-server": {
                            "enabled": True,
                            "command": "node",
                            "args": [],
                        }
                    },
                    "theme": {"mode": "dark"},
                    "ui_font_size": 16,
                    "telemetry": {"diagnostics": False},
                }
            )
        )
        client_def = get_client_by_name("zed")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].name == "my-server"

    def test_parse_zed_multiple_servers(self, tmp_path):
        """Parse Zed config with multiple servers of different types."""
        config_file = tmp_path / "settings.json"
        config_file.write_text(
            json.dumps(
                {
                    "context_servers": {
                        "stdio-server": {
                            "enabled": True,
                            "command": "npx",
                            "args": ["-y", "package1"],
                        },
                        "remote-server": {
                            "enabled": True,
                            "url": "https://api.example.com/mcp",
                        },
                        "another-stdio": {
                            "enabled": True,
                            "command": "node",
                            "args": ["server.js"],
                            "env": {"PORT": "3000"},
                        },
                    }
                }
            )
        )
        client_def = get_client_by_name("zed")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert len(result.servers) == 3
        server_names = [s.name for s in result.servers]
        assert "stdio-server" in server_names
        assert "remote-server" in server_names
        assert "another-stdio" in server_names

    def test_parse_zed_with_comments(self, tmp_path):
        """Zed parser handles JSONC (JSON with Comments)."""
        config_file = tmp_path / "settings.json"
        # Write JSONC content with comments
        config_file.write_text(
            """// Zed settings
// This file contains MCP server configurations
{
  // Context servers for MCP
  "context_servers": {
    "my-server": {
      "enabled": true,
      "command": "npx", // Use npx to run
      "args": ["-y", "some-package"]
    },
    /* This is a block comment */
    "remote-server": {
      "enabled": true,
      "url": "https://example.com/mcp"
    }
  },
  "theme": "dark" // Other settings
}
"""
        )
        client_def = get_client_by_name("zed")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert len(result.servers) == 2
        server_names = [s.name for s in result.servers]
        assert "my-server" in server_names
        assert "remote-server" in server_names


class TestJson5Parsing:
    """Tests for JSONC/JSON5 parsing via json5 library."""

    def test_parses_block_comment_chars_in_string(self, tmp_path):
        """Block comment characters inside strings are preserved.

        This was a bug with our previous custom implementation that used
        regex to strip /* */ comments without respecting string boundaries.
        """
        config_file = tmp_path / "mcp.json"
        config_file.write_text('{"mcpServers": {"test": {"command": "/*pattern*/"}}}')
        client_def = get_client_by_name("cursor")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].command == "/*pattern*/"

    def test_parses_trailing_commas(self, tmp_path):
        """JSON5 trailing commas are supported."""
        config_file = tmp_path / "mcp.json"
        config_file.write_text(
            """{
  "mcpServers": {
    "test": {
      "command": "node",
      "args": ["server.js",],
    },
  },
}"""
        )
        client_def = get_client_by_name("cursor")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].command == "node"

    def test_parses_url_with_comment_after(self, tmp_path):
        """URLs in strings with trailing comments work correctly."""
        config_file = tmp_path / "mcp.json"
        config_file.write_text(
            """{
  "mcpServers": {
    "test": {
      "url": "https://example.com/mcp" // SSE endpoint
    }
  }
}"""
        )
        client_def = get_client_by_name("cursor")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].url == "https://example.com/mcp"

    def test_parses_windows_path_with_comment(self, tmp_path):
        """Windows paths with trailing backslashes and comments work."""
        config_file = tmp_path / "mcp.json"
        # In JSON, \\\\ represents \\, and the // after is a comment
        config_file.write_text(
            '{"mcpServers": {"test": {"command": "C:\\\\node.exe"}}} // comment'
        )
        client_def = get_client_by_name("cursor")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)

        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].command == "C:\\node.exe"


class TestParseCodexConfig:
    """Tests for Codex TOML config parsing."""

    def test_parses_codex_stdio_server(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            '[mcp_servers.my-server]\ncommand = "npx"\nargs = ["-y", "some-pkg"]\n'
        )
        client_def = get_client_by_name("codex")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is not None
        assert result.client == "codex"
        assert len(result.servers) == 1
        server = result.servers[0]
        assert server.name == "my-server"
        assert server.type == "stdio"
        assert server.command == "npx"
        assert server.args == ["-y", "some-pkg"]

    def test_parses_codex_stdio_server_with_env(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            "[mcp_servers.api-server]\n"
            'command = "node"\n'
            'args = ["server.js"]\n\n'
            "[mcp_servers.api-server.env]\n"
            'API_KEY = "sk-abc123"\n'
        )
        client_def = get_client_by_name("codex")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is not None
        server = result.servers[0]
        assert server.command == "node"
        assert server.env == {"API_KEY": "sk-abc123"}

    def test_parses_codex_http_server(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            "[mcp_servers.remote]\n"
            'url = "https://example.com/mcp"\n\n'
            "[mcp_servers.remote.http_headers]\n"
            'X-Api-Key = "secret"\n'
        )
        client_def = get_client_by_name("codex")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is not None
        server = result.servers[0]
        assert server.name == "remote"
        assert server.type == "streaming-http"
        assert server.url == "https://example.com/mcp"
        assert server.headers == {"X-Api-Key": "secret"}

    def test_skips_disabled_codex_server(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            '[mcp_servers.disabled-server]\ncommand = "npx"\nenabled = false\n'
        )
        client_def = get_client_by_name("codex")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is None

    def test_parses_mixed_enabled_disabled(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            '[mcp_servers.active]\ncommand = "npx"\nargs = ["pkg"]\n\n'
            '[mcp_servers.inactive]\ncommand = "node"\nenabled = false\n'
        )
        client_def = get_client_by_name("codex")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].name == "active"

    def test_empty_toml_returns_none(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text("")
        client_def = get_client_by_name("codex")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is None

    def test_invalid_toml_returns_none(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text("[invalid toml ===")
        client_def = get_client_by_name("codex")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is None

    def test_toml_no_mcp_servers_key_returns_none(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text('[some_other_section]\nfoo = "bar"\n')
        client_def = get_client_by_name("codex")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is None

    def test_codex_server_without_command_or_url_skipped(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text("[mcp_servers.bad-server]\nenabled = true\n")
        client_def = get_client_by_name("codex")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is None

    def test_codex_multiple_servers(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            '[mcp_servers.server-a]\ncommand = "npx"\nargs = ["a"]\n\n'
            '[mcp_servers.server-b]\nurl = "https://b.com/mcp"\n'
        )
        client_def = get_client_by_name("codex")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is not None
        assert len(result.servers) == 2
        names = {s.name for s in result.servers}
        assert names == {"server-a", "server-b"}

    def test_codex_env_http_headers_stores_placeholder(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            "[mcp_servers.remote]\n"
            'url = "https://example.com/mcp"\n\n'
            "[mcp_servers.remote.env_http_headers]\n"
            'Authorization = "MY_API_KEY"\n'
        )
        client_def = get_client_by_name("codex")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is not None
        server = result.servers[0]
        assert server.headers == {"Authorization": "${MY_API_KEY}"}

    def test_codex_env_http_headers_merged_with_static(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            "[mcp_servers.remote]\n"
            'url = "https://example.com/mcp"\n\n'
            "[mcp_servers.remote.http_headers]\n"
            'X-Custom = "static-val"\n\n'
            "[mcp_servers.remote.env_http_headers]\n"
            'Authorization = "TOKEN_VAR"\n'
        )
        client_def = get_client_by_name("codex")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is not None
        server = result.servers[0]
        assert server.headers == {
            "X-Custom": "static-val",
            "Authorization": "${TOKEN_VAR}",
        }

    def test_codex_env_http_headers_always_stores_placeholder(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            "[mcp_servers.remote]\n"
            'url = "https://example.com/mcp"\n\n'
            "[mcp_servers.remote.env_http_headers]\n"
            'Authorization = "NONEXISTENT_VAR"\n'
        )
        client_def = get_client_by_name("codex")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is not None
        server = result.servers[0]
        assert server.headers == {"Authorization": "${NONEXISTENT_VAR}"}

    def test_codex_bearer_token_env_var(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            "[mcp_servers.remote]\n"
            'url = "https://api.example.com/mcp/"\n'
            'bearer_token_env_var = "MY_TOKEN"\n'
        )
        client_def = get_client_by_name("codex")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is not None
        server = result.servers[0]
        assert server.headers == {"Authorization": "Bearer ${MY_TOKEN}"}

    def test_codex_bearer_token_env_var_merged_with_headers(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            "[mcp_servers.remote]\n"
            'url = "https://api.example.com/mcp/"\n'
            'bearer_token_env_var = "MY_TOKEN"\n\n'
            "[mcp_servers.remote.http_headers]\n"
            'X-Custom = "val"\n'
        )
        client_def = get_client_by_name("codex")
        assert client_def is not None
        result = parse_config_file(client_def, config_file)
        assert result is not None
        server = result.servers[0]
        assert server.headers == {
            "X-Custom": "val",
            "Authorization": "Bearer ${MY_TOKEN}",
        }

    def test_temp_client_def_with_config_format_parses_toml(self, tmp_path):
        """Regression: project-scan temp MCPClientDefinition must carry config_format."""
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            '[mcp_servers.proj-server]\ncommand = "npx"\nargs = ["pkg"]\n'
        )
        real_def = get_client_by_name("codex")
        assert real_def is not None
        temp_def = MCPClientDefinition(
            name=real_def.name,
            display_name=real_def.display_name,
            paths=[],
            servers_key="mcp_servers",
            config_format=real_def.config_format,
        )
        result = parse_config_file(temp_def, config_file)
        assert result is not None
        assert len(result.servers) == 1
        assert result.servers[0].name == "proj-server"


class TestParseKimiCodeConfig:
    """Kimi Code uses standard mcpServers with inferred transports."""

    def test_parses_stdio_and_remote_servers(self, fixtures_dir):
        client_def = get_client_by_name("kimi_code")
        result = parse_config_file(client_def, fixtures_dir / "kimi_code_config.json")

        assert result is not None
        assert result.client == "kimi_code"
        by_name = {server.name: server for server in result.servers}

        assert by_name["filesystem"].type == "stdio"
        assert by_name["filesystem"].command == "npx"
        assert by_name["filesystem"].env == {"HOME": "/Users/test"}
        # A bare url means streamable HTTP; only legacy servers say sse.
        assert by_name["linear"].type == "streaming-http"
        assert by_name["linear"].url == "https://mcp.linear.app/mcp"
        assert by_name["legacy-events"].type == "sse"


class TestParsePiConfig:
    """Pi servers carry no type/transport field at all."""

    def test_parses_stdio_and_remote_servers(self, fixtures_dir):
        client_def = get_client_by_name("pi")
        result = parse_config_file(client_def, fixtures_dir / "pi_config.json")

        assert result is not None
        assert result.client == "pi"
        by_name = {server.name: server for server in result.servers}

        assert by_name["filesystem"].type == "stdio"
        assert by_name["filesystem"].args == [
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "/tmp",
        ]
        assert by_name["remote-docs"].type == "streaming-http"
        assert by_name["remote-docs"].url == "https://mcp.example.com/mcp"

    def test_sibling_keys_are_not_mistaken_for_servers(self, fixtures_dir):
        """mcp.json also holds `settings` and `imports` alongside mcpServers."""
        client_def = get_client_by_name("pi")
        result = parse_config_file(client_def, fixtures_dir / "pi_config.json")

        names = {server.name for server in result.servers}
        assert "settings" not in names
        assert "imports" not in names
        assert "toolPrefix" not in names


class TestParseJunieConfig:
    """Junie infers local vs remote structurally."""

    def test_parses_stdio_and_remote_servers(self, fixtures_dir):
        client_def = get_client_by_name("junie")
        result = parse_config_file(client_def, fixtures_dir / "junie_config.json")

        assert result is not None
        assert result.client == "junie"
        by_name = {server.name: server for server in result.servers}

        assert by_name["Context7"].type == "stdio"
        assert by_name["Context7"].command == "npx"
        assert by_name["Context7"].env == {"ENV_VAR": "value"}
        assert by_name["RemoteServer"].type == "streaming-http"
        assert by_name["RemoteServer"].headers == {
            "Authorization": "Bearer token_placeholder"
        }


class TestParseDevinCliConfig:
    """Devin CLI uses the standard shape with an explicit transport field."""

    def test_parses_stdio_and_remote_servers(self, fixtures_dir):
        client_def = get_client_by_name("devin_cli")
        result = parse_config_file(client_def, fixtures_dir / "devin_cli_config.json")

        assert result is not None
        assert result.client == "devin_cli"
        by_name = {server.name: server for server in result.servers}

        assert by_name["github"].type == "stdio"
        assert by_name["github"].command == "npx"
        assert by_name["remote-docs"].type == "streaming-http"
        assert by_name["remote-docs"].url == "https://mcp.example.com/mcp"


class TestParseKiloCodeConfig:
    """Kilo Code must parse both live config generations from one file."""

    def test_parses_modern_opencode_shaped_servers(self, fixtures_dir):
        client_def = get_client_by_name("kilo_code")
        result = parse_config_file(client_def, fixtures_dir / "kilo_code_config.jsonc")

        assert result is not None
        assert result.client == "kilo_code"
        by_name = {server.name: server for server in result.servers}

        # command is one list: argv[0] is the executable, the rest are args.
        assert by_name["filesystem"].type == "stdio"
        assert by_name["filesystem"].command == "npx"
        assert by_name["filesystem"].args == [
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "/tmp",
        ]
        assert by_name["filesystem"].env == {"HOME": "/Users/test"}
        assert by_name["remote-docs"].type == "streaming-http"
        assert by_name["remote-docs"].url == "https://mcp.example.com/mcp"

    def test_parses_legacy_cline_shaped_servers(self, fixtures_dir):
        """Legacy mcpServers entries are still merged at runtime, so keep them."""
        client_def = get_client_by_name("kilo_code")
        result = parse_config_file(client_def, fixtures_dir / "kilo_code_config.jsonc")

        by_name = {server.name: server for server in result.servers}
        assert by_name["legacy-stdio"].type == "stdio"
        assert by_name["legacy-stdio"].command == "npx"
        assert by_name["legacy-stdio"].args == [
            "-y",
            "@modelcontextprotocol/server-github",
        ]
        assert by_name["legacy-remote"].type == "streaming-http"
        assert by_name["legacy-remote"].url == "https://legacy.example.com/mcp"

    def test_skips_servers_disabled_in_either_generation(self, fixtures_dir):
        """Modern entries gate on enabled, legacy entries gate on disabled."""
        client_def = get_client_by_name("kilo_code")
        result = parse_config_file(client_def, fixtures_dir / "kilo_code_config.jsonc")

        names = {server.name for server in result.servers}
        assert "turned-off" not in names
        assert "legacy-disabled" not in names
        assert len(result.servers) == 4

    def test_jsonc_comments_do_not_break_parsing(self, fixtures_dir):
        client_def = get_client_by_name("kilo_code")
        result = parse_config_file(client_def, fixtures_dir / "kilo_code_config.jsonc")
        assert result is not None
        assert result.servers


class TestParseRooCodeConfig:
    """Roo Code uses the same standard mcpServers shape as Cline."""

    def test_parses_stdio_and_remote_servers(self, fixtures_dir):
        client_def = get_client_by_name("roo_code")
        result = parse_config_file(client_def, fixtures_dir / "roo_code_config.json")

        assert result is not None
        assert result.client == "roo_code"
        by_name = {server.name: server for server in result.servers}
        assert by_name["filesystem"].type == "stdio"
        assert by_name["filesystem"].command == "npx"
        assert by_name["remote-docs"].type == "streaming-http"
        assert by_name["remote-docs"].url == "https://mcp.example.com/mcp"


class TestNewClientDisabledServerHandling:
    """Pin the enable/disable asymmetry across the newly added clients.

    Standard-format clients inventory a configured-but-disabled server, matching
    every existing standard-format client (cursor, cline, claude_code,
    windsurf): the command or URL is still on disk and re-enabling it is a
    one-key edit. Kilo Code is the exception because its modern entries run
    through the OpenCode parser, which honours ``enabled`` — so its legacy
    entries honour ``disabled`` for intra-client parity. Changing either
    behaviour is a deliberate product decision, not an incidental edit.
    """

    def test_standard_format_clients_still_report_disabled_servers(self, fixtures_dir):
        for client_name, fixture in (
            ("kimi_code", "kimi_code_config.json"),
            ("pi", "pi_config.json"),
            ("devin_cli", "devin_cli_config.json"),
        ):
            client_def = get_client_by_name(client_name)
            result = parse_config_file(client_def, fixtures_dir / fixture)
            names = {server.name for server in result.servers}
            assert "turned-off" in names, client_name

    def test_kilo_code_honours_both_disable_gates(self, fixtures_dir):
        client_def = get_client_by_name("kilo_code")
        result = parse_config_file(client_def, fixtures_dir / "kilo_code_config.jsonc")
        names = {server.name for server in result.servers}
        assert "turned-off" not in names
        assert "legacy-disabled" not in names
