"""Tests for server install entry generation per editor."""

from runlayer_cli.commands.setup import (
    InstallClient,
    InstallServerSpec,
    _build_server_entry,
)


# =============================================================================
# Goose (YAML format)
# =============================================================================


def test_build_server_entry_goose_local() -> None:
    spec = InstallServerSpec(
        server_id="abc123",
        name="My Local Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=True,
    )
    assert _build_server_entry(InstallClient.GOOSE, spec) == {
        "enabled": True,
        "type": "stdio",
        "name": "my-local-server",
        "cmd": "uvx",
        "args": ["runlayer", "run", "abc123", "--host", "https://example.com"],
        "envs": {},
        "timeout": 300,
    }


def test_build_server_entry_goose_remote() -> None:
    """Goose remote uses streamable_http + uri per Goose docs."""
    spec = InstallServerSpec(
        server_id="abc123",
        name="My Local Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=False,
    )
    assert _build_server_entry(InstallClient.GOOSE, spec) == {
        "enabled": True,
        "type": "streamable_http",
        "name": "my-local-server",
        "uri": "https://example.com/api/v1/proxy/abc123/mcp",
        "envs": {},
        "timeout": 300,
    }


# =============================================================================
# VS Code (requires type field per docs)
# =============================================================================


def test_build_server_entry_vscode_local() -> None:
    """VS Code local entry requires type: stdio per docs."""
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=True,
    )
    assert _build_server_entry(InstallClient.VSCODE, spec) == {
        "type": "stdio",
        "command": "uvx",
        "args": ["runlayer", "run", "abc123", "--host", "https://example.com"],
    }


def test_build_server_entry_vscode_remote() -> None:
    """VS Code remote entry requires type: http per docs."""
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=False,
    )
    assert _build_server_entry(InstallClient.VSCODE, spec) == {
        "type": "http",
        "url": "https://example.com/api/v1/proxy/abc123/mcp",
    }


# =============================================================================
# Claude Code (remote requires type: http per docs)
# =============================================================================


def test_build_server_entry_claude_code_local() -> None:
    """Claude Code local entry uses command/args without type."""
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=True,
    )
    assert _build_server_entry(InstallClient.CLAUDE_CODE, spec) == {
        "command": "uvx",
        "args": ["runlayer", "run", "abc123", "--host", "https://example.com"],
    }


def test_build_server_entry_claude_code_remote() -> None:
    """Claude Code remote entry requires type: http per docs."""
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=False,
    )
    assert _build_server_entry(InstallClient.CLAUDE_CODE, spec) == {
        "type": "http",
        "url": "https://example.com/api/v1/proxy/abc123/mcp",
    }


# =============================================================================
# Cursor (omits type per docs examples)
# =============================================================================


def test_build_server_entry_cursor_local() -> None:
    """Cursor local entry uses command/args without type."""
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=True,
    )
    assert _build_server_entry(InstallClient.CURSOR, spec) == {
        "command": "uvx",
        "args": ["runlayer", "run", "abc123", "--host", "https://example.com"],
    }


def test_build_server_entry_cursor_remote() -> None:
    """Cursor remote entry uses url without type."""
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=False,
    )
    assert _build_server_entry(InstallClient.CURSOR, spec) == {
        "url": "https://example.com/api/v1/proxy/abc123/mcp",
    }


# =============================================================================
# Windsurf (remote uses serverUrl per docs)
# =============================================================================


def test_build_server_entry_windsurf_local() -> None:
    """Windsurf local entry uses command/args."""
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=True,
    )
    assert _build_server_entry(InstallClient.WINDSURF, spec) == {
        "command": "uvx",
        "args": ["runlayer", "run", "abc123", "--host", "https://example.com"],
    }


def test_build_server_entry_windsurf_remote() -> None:
    """Windsurf remote entry uses serverUrl per docs."""
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=False,
    )
    assert _build_server_entry(InstallClient.WINDSURF, spec) == {
        "serverUrl": "https://example.com/api/v1/proxy/abc123/mcp",
    }


# =============================================================================
# Zed (context_servers format, includes env:{} for local)
# =============================================================================


def test_build_server_entry_zed_local() -> None:
    """Zed local entry uses command/args/env."""
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=True,
    )
    assert _build_server_entry(InstallClient.ZED, spec) == {
        "command": "uvx",
        "args": ["runlayer", "run", "abc123", "--host", "https://example.com"],
        "env": {},
    }


def test_build_server_entry_zed_remote() -> None:
    """Zed remote entry uses url."""
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=False,
    )
    assert _build_server_entry(InstallClient.ZED, spec) == {
        "url": "https://example.com/api/v1/proxy/abc123/mcp",
    }


# =============================================================================
# Claude Desktop (local only, mcpServers format)
# =============================================================================


def test_build_server_entry_claude_desktop_local() -> None:
    """Claude Desktop entry uses command/args."""
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=True,
    )
    assert _build_server_entry(InstallClient.CLAUDE_DESKTOP, spec) == {
        "command": "uvx",
        "args": ["runlayer", "run", "abc123", "--host", "https://example.com"],
    }


def test_build_server_entry_claude_desktop_remote_fallback() -> None:
    """Claude Desktop returns local config even for remote (remote not supported)."""
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=False,
    )
    # Claude Desktop doesn't support remote, so builder returns local format
    assert _build_server_entry(InstallClient.CLAUDE_DESKTOP, spec) == {
        "command": "uvx",
        "args": ["runlayer", "run", "abc123", "--host", "https://example.com"],
    }


# =============================================================================
# OpenCode (mcp format with type=local|remote, command as array)
# =============================================================================


def test_build_server_entry_opencode_local() -> None:
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=True,
    )
    assert _build_server_entry(InstallClient.OPENCODE, spec) == {
        "enabled": True,
        "type": "local",
        "command": ["uvx", "runlayer", "run", "abc123", "--host", "https://example.com"],
    }


def test_build_server_entry_opencode_remote() -> None:
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=False,
    )
    assert _build_server_entry(InstallClient.OPENCODE, spec) == {
        "enabled": True,
        "type": "remote",
        "url": "https://example.com/api/v1/proxy/abc123/mcp",
    }


# =============================================================================
# Codex (TOML mcp_servers tables)
# =============================================================================


def test_build_server_entry_codex_local() -> None:
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=True,
    )
    assert _build_server_entry(InstallClient.CODEX, spec) == {
        "command": "uvx",
        "args": ["runlayer", "run", "abc123", "--host", "https://example.com"],
    }


def test_build_server_entry_codex_remote_with_headers() -> None:
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=False,
        headers={"Authorization": "Bearer token123"},
    )
    assert _build_server_entry(InstallClient.CODEX, spec) == {
        "url": "https://example.com/api/v1/proxy/abc123/mcp",
        "http_headers": {"Authorization": "Bearer token123"},
    }


# =============================================================================
# Headers support
# =============================================================================


def test_build_server_entry_with_headers() -> None:
    """Remote entries should include headers when provided."""
    spec = InstallServerSpec(
        server_id="abc123",
        name="Test Server",
        proxy_url="https://example.com/api/v1/proxy/abc123/mcp",
        host="https://example.com",
        is_local=False,
        headers={"Authorization": "Bearer token123"},
    )
    # VS Code includes headers
    entry = _build_server_entry(InstallClient.VSCODE, spec)
    assert entry["headers"] == {"Authorization": "Bearer token123"}

    # Claude Code includes headers
    entry = _build_server_entry(InstallClient.CLAUDE_CODE, spec)
    assert entry["headers"] == {"Authorization": "Bearer token123"}

    # Cursor includes headers
    entry = _build_server_entry(InstallClient.CURSOR, spec)
    assert entry["headers"] == {"Authorization": "Bearer token123"}

    # Windsurf includes headers
    entry = _build_server_entry(InstallClient.WINDSURF, spec)
    assert entry["headers"] == {"Authorization": "Bearer token123"}

    # Zed includes headers
    entry = _build_server_entry(InstallClient.ZED, spec)
    assert entry["headers"] == {"Authorization": "Bearer token123"}

    # Goose includes headers
    entry = _build_server_entry(InstallClient.GOOSE, spec)
    assert entry["headers"] == {"Authorization": "Bearer token123"}

    # OpenCode includes headers (remote)
    entry = _build_server_entry(InstallClient.OPENCODE, spec)
    assert entry["headers"] == {"Authorization": "Bearer token123"}
