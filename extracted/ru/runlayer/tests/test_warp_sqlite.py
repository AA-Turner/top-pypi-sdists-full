"""Tests for Warp sqlite MCP server scanning."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from unittest import mock

from runlayer_cli.scan.config_parser import (
    MCPClientConfig,
    MCPServerConfig,
    compute_config_hash,
)
from runlayer_cli.scan.warp_sqlite import (
    _build_variable_map,
    _merge_into_global_warp,
    _parse_installation_row,
    _row_disabled,
    _substitute,
    _warp_sqlite_paths,
    enrich_configurations_with_warp_sqlite,
    scan_warp_sqlite,
)


def _installation_blob(
    name: str,
    inner: dict,
    variables: list[dict] | None = None,
) -> str:
    """Build a Warp installation JSON blob with a nested template.json string."""
    return json.dumps(
        {
            "uuid": "861d4a5d-8e05-4a15-aef4-30c1f71a951f",
            "name": name,
            "description": None,
            "template": {
                "json": json.dumps(inner),
                "variables": variables or [],
            },
            "version": 1780493519,
            "gallery_data": {"gallery_item_id": "x", "version": 1},
        }
    )


def _make_warp_db(path: Path, rows: list[tuple]) -> None:
    """Create a warp.sqlite with the mcp_server_installations table + rows."""
    conn = sqlite3.connect(str(path))
    try:
        conn.execute(
            "CREATE TABLE mcp_server_installations ("
            "id TEXT, installation TEXT, created_at TEXT, "
            "variable_values TEXT, enabled INTEGER, updated_at TEXT)"
        )
        conn.executemany(
            "INSERT INTO mcp_server_installations VALUES (?, ?, ?, ?, ?, ?)",
            rows,
        )
        conn.commit()
    finally:
        conn.close()


class TestVariableSubstitution:
    def test_build_variable_map_extracts_string_values(self):
        values = {
            "test": {"variable_type": "Text", "value": "resolved"},
            "skip": {"variable_type": "Text", "value": 123},
        }
        result = _build_variable_map(values)
        assert result == {"test": "resolved"}

    def test_build_variable_map_empty(self):
        assert _build_variable_map(None) == {}
        assert _build_variable_map({}) == {}

    def test_substitute_string(self):
        assert _substitute("{{test}}", {"test": "abc"}) == "abc"

    def test_substitute_nested(self):
        value = {"env": {"KEY": "{{test}}"}, "args": ["{{test}}", "static"]}
        result = _substitute(value, {"test": "abc"})
        assert result == {"env": {"KEY": "abc"}, "args": ["abc", "static"]}

    def test_substitute_unknown_left_as_is(self):
        assert _substitute("{{missing}}", {}) == "{{missing}}"


def _installation_row(
    installation: str,
    variable_values: str | None = None,
    enabled: int = 1,
) -> sqlite3.Row:
    """Build a row using Warp's real column names."""
    return _row(
        {
            "id": "id",
            "installation": installation,
            "created_at": "ts",
            "variable_values": variable_values,
            "enabled": enabled,
            "updated_at": "ts",
        }
    )


class TestParseInstallationRow:
    def test_stdio_server_with_variable(self):
        inner = {
            "Context7": {
                "command": "npx",
                "args": ["-y", "@upstash/context7-mcp"],
                "env": {"test": "{{test}}"},
                "start_on_launch": True,
                "working_directory": None,
            }
        }
        row = _installation_row(
            _installation_blob("Context7", inner, [{"key": "test"}]),
            json.dumps({"test": {"variable_type": "Text", "value": "secret"}}),
        )
        servers = _parse_installation_row(row)
        assert len(servers) == 1
        server = servers[0]
        assert server.name == "Context7"
        assert server.type == "stdio"
        assert server.command == "npx"
        assert server.args == ["-y", "@upstash/context7-mcp"]
        assert server.env == {"test": "secret"}

    def test_remote_url_server(self):
        inner = {"Figma": {"url": "https://mcp.figma.com/mcp"}}
        row = _installation_row(_installation_blob("Figma", inner))
        servers = _parse_installation_row(row)
        assert len(servers) == 1
        assert servers[0].name == "Figma"
        assert servers[0].type == "sse"
        assert servers[0].url == "https://mcp.figma.com/mcp"

    def test_multiple_servers_in_template(self):
        inner = {
            "a": {"command": "npx"},
            "b": {"url": "https://example.com/mcp"},
        }
        row = _installation_row(_installation_blob("multi", inner))
        servers = _parse_installation_row(row)
        assert {s.name for s in servers} == {"a", "b"}

    def test_non_json_cells_tolerated(self):
        row = _installation_row("not json", "also not json")
        assert _parse_installation_row(row) == []

    def test_missing_template_json(self):
        blob = json.dumps({"name": "x", "template": {"variables": []}})
        row = _installation_row(blob)
        assert _parse_installation_row(row) == []

    def test_sniffs_blob_when_columns_unnamed(self):
        """Schema drift fallback: locate the blob by shape, not column name."""
        inner = {"Ctx": {"command": "npx"}}
        row = _row(
            {
                "pk": "id",
                "payload": _installation_blob("Ctx", inner),
                "vars": json.dumps({"test": {"variable_type": "Text", "value": "v"}}),
            }
        )
        servers = _parse_installation_row(row)
        assert [s.name for s in servers] == ["Ctx"]


def _row(values: dict) -> sqlite3.Row:
    """Build a sqlite3.Row from a column->value mapping (in-memory db)."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cols = list(values)
    conn.execute(f"CREATE TABLE t ({', '.join(cols)})")
    conn.execute(
        f"INSERT INTO t VALUES ({', '.join('?' for _ in cols)})",
        [values[c] for c in cols],
    )
    return conn.execute("SELECT * FROM t").fetchone()


class TestRowDisabled:
    def test_enabled_zero_is_disabled(self):
        assert _row_disabled(_row({"id": "a", "enabled": 0})) is True

    def test_enabled_one_is_enabled(self):
        assert _row_disabled(_row({"id": "a", "enabled": 1})) is False

    def test_enabled_null_treated_as_enabled(self):
        assert _row_disabled(_row({"id": "a", "enabled": None})) is False

    def test_missing_enabled_column_treated_as_enabled(self):
        assert _row_disabled(_row({"id": "a", "installation": "x"})) is False


class TestScanWarpSqlite:
    def test_returns_none_when_no_db(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "runlayer_cli.scan.warp_sqlite._warp_sqlite_paths",
            lambda: [tmp_path / "warp.sqlite"],
        )
        assert scan_warp_sqlite() is None

    def test_returns_none_when_table_missing(self, tmp_path, monkeypatch):
        db = tmp_path / "warp.sqlite"
        conn = sqlite3.connect(str(db))
        conn.execute("CREATE TABLE other (id TEXT)")
        conn.commit()
        conn.close()
        monkeypatch.setattr(
            "runlayer_cli.scan.warp_sqlite._warp_sqlite_paths", lambda: [db]
        )
        assert scan_warp_sqlite() is None

    def test_scans_servers(self, tmp_path, monkeypatch):
        db = tmp_path / "warp.sqlite"
        inner = {"Context7": {"command": "npx", "args": ["-y", "ctx"]}}
        _make_warp_db(
            db,
            [("id", _installation_blob("Context7", inner), "ts", None, 1, "ts")],
        )
        monkeypatch.setattr(
            "runlayer_cli.scan.warp_sqlite._warp_sqlite_paths", lambda: [db]
        )
        config = scan_warp_sqlite()
        assert config is not None
        assert config.client == "warp"
        assert config.config_scope == "global"
        assert config.config_path == str(db)
        assert len(config.servers) == 1
        assert config.servers[0].name == "Context7"

    def test_disabled_rows_excluded_from_scan(self, tmp_path, monkeypatch):
        db = tmp_path / "warp.sqlite"
        enabled_inner = {"Enabled": {"command": "npx"}}
        disabled_inner = {"Disabled": {"command": "npx"}}
        _make_warp_db(
            db,
            [
                (
                    "a",
                    _installation_blob("Enabled", enabled_inner),
                    "ts",
                    None,
                    1,
                    "ts",
                ),
                (
                    "b",
                    _installation_blob("Disabled", disabled_inner),
                    "ts",
                    None,
                    0,
                    "ts",
                ),
            ],
        )
        monkeypatch.setattr(
            "runlayer_cli.scan.warp_sqlite._warp_sqlite_paths", lambda: [db]
        )
        config = scan_warp_sqlite()
        assert config is not None
        assert [s.name for s in config.servers] == ["Enabled"]

    def test_returns_none_when_all_rows_disabled(self, tmp_path, monkeypatch):
        db = tmp_path / "warp.sqlite"
        inner = {"Disabled": {"command": "npx"}}
        _make_warp_db(
            db,
            [("id", _installation_blob("Disabled", inner), "ts", None, 0, "ts")],
        )
        monkeypatch.setattr(
            "runlayer_cli.scan.warp_sqlite._warp_sqlite_paths", lambda: [db]
        )
        assert scan_warp_sqlite() is None

    def test_prefers_first_existing_db(self, tmp_path, monkeypatch):
        missing = tmp_path / "missing" / "warp.sqlite"
        db = tmp_path / "warp.sqlite"
        inner = {"S": {"command": "node"}}
        _make_warp_db(db, [("id", _installation_blob("S", inner), "ts", None, 1, "ts")])
        monkeypatch.setattr(
            "runlayer_cli.scan.warp_sqlite._warp_sqlite_paths",
            lambda: [missing, db],
        )
        config = scan_warp_sqlite()
        assert config is not None
        assert config.config_path == str(db)

    def test_merges_servers_across_multiple_dbs(self, tmp_path, monkeypatch):
        """Stable + Preview both populated: union of servers, deduped by hash."""
        stable = tmp_path / "stable" / "warp.sqlite"
        preview = tmp_path / "preview" / "warp.sqlite"
        stable.parent.mkdir()
        preview.parent.mkdir()
        shared = {"Shared": {"command": "npx", "args": ["-y", "shared"]}}
        preview_only = {"PreviewOnly": {"command": "node"}}
        _make_warp_db(
            stable,
            [("a", _installation_blob("Shared", shared), "ts", None, 1, "ts")],
        )
        _make_warp_db(
            preview,
            [
                ("b", _installation_blob("Shared", shared), "ts", None, 1, "ts"),
                (
                    "c",
                    _installation_blob("PreviewOnly", preview_only),
                    "ts",
                    None,
                    1,
                    "ts",
                ),
            ],
        )
        monkeypatch.setattr(
            "runlayer_cli.scan.warp_sqlite._warp_sqlite_paths",
            lambda: [stable, preview],
        )
        config = scan_warp_sqlite()
        assert config is not None
        names = sorted(s.name for s in config.servers)
        assert names == ["PreviewOnly", "Shared"]
        # config_path points at the first db that contributed servers.
        assert config.config_path == str(stable)


class TestWarpSqlitePaths:
    @mock.patch("platform.system", return_value="Darwin")
    def test_macos_paths(self, _sys):
        paths = _warp_sqlite_paths()
        joined = [str(p) for p in paths]
        assert any("dev.warp.Warp-Stable/warp.sqlite" in p for p in joined)
        assert any("dev.warp.Warp-Preview/warp.sqlite" in p for p in joined)
        assert any("2BBY89MBSN.dev.warp" in p for p in joined)

    @mock.patch("platform.system", return_value="Linux")
    def test_linux_paths_respect_xdg_state_home(self, _sys, monkeypatch):
        monkeypatch.setenv("XDG_STATE_HOME", "/custom/state")
        paths = [str(p) for p in _warp_sqlite_paths()]
        assert "/custom/state/warp-terminal/warp.sqlite" in paths
        assert "/custom/state/warp-terminal-preview/warp.sqlite" in paths

    @mock.patch("platform.system", return_value="Linux")
    def test_linux_paths_default_state_dir(self, _sys, monkeypatch):
        monkeypatch.delenv("XDG_STATE_HOME", raising=False)
        paths = [str(p) for p in _warp_sqlite_paths()]
        expected = str(Path.home() / ".local/state/warp-terminal/warp.sqlite")
        assert expected in paths

    @mock.patch("platform.system", return_value="Windows")
    def test_windows_paths(self, _sys, monkeypatch):
        monkeypatch.setenv("LOCALAPPDATA", "C:/Users/Test/AppData/Local")
        with mock.patch(
            "runlayer_cli.scan.clients._is_windows_with_wsl", return_value=False
        ):
            paths = [str(p) for p in _warp_sqlite_paths()]
        assert any("warp" in p and "warp.sqlite" in p for p in paths)

    @mock.patch("platform.system", return_value="Windows")
    def test_windows_with_wsl_includes_linux_sqlite_paths(self, _sys, monkeypatch):
        monkeypatch.setenv("LOCALAPPDATA", "C:/Users/Test/AppData/Local")
        homes = [
            Path(R"\\wsl.localhost\Ubuntu\home\alex"),
            Path(R"\\wsl.localhost\Debian\home\sam"),
        ]
        with (
            mock.patch(
                "runlayer_cli.scan.clients._is_windows_with_wsl", return_value=True
            ),
            mock.patch("runlayer_cli.scan.clients._wsl_homes", return_value=homes),
        ):
            paths = _warp_sqlite_paths()
        for home in homes:
            assert home / ".local/state/warp-terminal/warp.sqlite" in paths
            assert home / ".local/state/warp-terminal-preview/warp.sqlite" in paths
        joined = [str(p) for p in paths]
        # %LOCALAPPDATA% stays literal under posixpath.expandvars on non-Windows
        # CI hosts (it expands on a real Windows host).
        assert any("LOCALAPPDATA" in p and "warp.sqlite" in p for p in joined)


class TestMergeIntoGlobalWarp:
    def _server(self, name: str) -> MCPServerConfig:
        s = MCPServerConfig(name=name, type="stdio", command="npx")
        s.config_hash = compute_config_hash(s)
        return s

    def test_appends_when_no_existing_warp_config(self):
        configs: list[MCPClientConfig] = []
        sqlite_config = MCPClientConfig(
            client="warp", config_scope="global", servers=[self._server("a")]
        )
        _merge_into_global_warp(configs, sqlite_config)
        assert len(configs) == 1
        assert configs[0] is sqlite_config

    def test_dedups_against_existing_by_config_hash(self):
        shared = self._server("shared")
        existing = MCPClientConfig(
            client="warp", config_scope="global", servers=[shared]
        )
        configs = [existing]
        sqlite_config = MCPClientConfig(
            client="warp",
            config_scope="global",
            servers=[self._server("shared"), self._server("new")],
        )
        _merge_into_global_warp(configs, sqlite_config)
        # No new warp config appended; merged into existing.
        assert len(configs) == 1
        names = [s.name for s in existing.servers]
        assert names.count("shared") == 1
        assert "new" in names


class TestEnrichConfigurations:
    def test_noop_when_no_sqlite_servers(self, monkeypatch):
        monkeypatch.setattr(
            "runlayer_cli.scan.warp_sqlite.scan_warp_sqlite", lambda: None
        )
        configs: list[MCPClientConfig] = []
        enrich_configurations_with_warp_sqlite(configs)
        assert configs == []

    def test_merges_sqlite_into_configurations(self, monkeypatch):
        server = MCPServerConfig(name="gallery", type="stdio", command="npx")
        server.config_hash = compute_config_hash(server)
        monkeypatch.setattr(
            "runlayer_cli.scan.warp_sqlite.scan_warp_sqlite",
            lambda: MCPClientConfig(
                client="warp", config_scope="global", servers=[server]
            ),
        )
        configs: list[MCPClientConfig] = []
        enrich_configurations_with_warp_sqlite(configs)
        assert len(configs) == 1
        assert configs[0].client == "warp"
        assert [s.name for s in configs[0].servers] == ["gallery"]


class TestScanServiceIntegration:
    """Warp sqlite supplement flows through scan_all_clients (Phase 1 path)."""

    @mock.patch("runlayer_cli.scan.service.get_all_clients", return_value=[])
    @mock.patch(
        "runlayer_cli.scan.service.get_clients_with_project_configs", return_value=[]
    )
    def test_sqlite_servers_appear_as_global_warp_config(
        self, _project_clients, _clients, tmp_path, monkeypatch
    ):
        from runlayer_cli.scan.service import scan_all_clients

        db = tmp_path / "warp.sqlite"
        inner = {"Context7": {"command": "npx", "args": ["-y", "ctx"]}}
        _make_warp_db(
            db,
            [("id", _installation_blob("Context7", inner), "ts", None, 1, "ts")],
        )
        monkeypatch.setattr(
            "runlayer_cli.scan.warp_sqlite._warp_sqlite_paths", lambda: [db]
        )

        result = scan_all_clients(scan_projects=False)

        warp_configs = [
            c
            for c in result.configurations
            if c.client == "warp" and c.config_scope == "global"
        ]
        assert len(warp_configs) == 1
        assert [s.name for s in warp_configs[0].servers] == ["Context7"]
