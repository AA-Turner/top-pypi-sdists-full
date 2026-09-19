"""Hook-side MCP config readers survive deeply nested input (ISS-01 follow-up).

Every path here is user-controlled (project ``.mcp.json``, ``~/.claude.json``,
Cursor / Copilot / Hermes / Goose / Codex configs). Each reader used to catch
only its decoder's documented error; a nested-array file raised
``RecursionError`` out of the lookup, so one planted file stopped every later
candidate from being tried -- under Enforce, a hard deny for a live server.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from runlayer_cli.hook import copilot_cli_mcp_lookup, mcp_lookup
from runlayer_cli.hook.mcp_types import MCPServer
from tests.hostile_inputs import DEEP_NESTING, DEEP_NESTING_TOML


@pytest.fixture
def poisoned(tmp_path: Path) -> Path:
    path = tmp_path / "poisoned.json"
    path.write_text(DEEP_NESTING)
    return path


class TestMcpLookupReaders:
    def test_search_file(self, poisoned: Path):
        assert mcp_lookup._search_file(poisoned, "srv") is None

    def test_search_file_rejects_non_object_document(self, tmp_path: Path):
        path = tmp_path / "list.json"
        path.write_text("[1, 2]")
        assert mcp_lookup._search_file(path, "srv") is None

    def test_read_json_servers(self, poisoned: Path):
        assert mcp_lookup._read_json_servers(poisoned, "mcpServers") == {}

    def test_search_cursor_file(self, poisoned: Path):
        assert mcp_lookup._search_cursor_file(poisoned, "srv") is None

    def test_read_json_object(self, poisoned: Path):
        assert mcp_lookup._read_json_object(poisoned) is None

    def test_read_jsonc_object(self, poisoned: Path):
        assert mcp_lookup._read_jsonc_object(poisoned) is None

    def test_read_text_rejects_non_utf8(self, tmp_path: Path):
        path = tmp_path / "latin1.json"
        path.write_bytes(b'{"a": "\xe9"}')
        assert mcp_lookup._read_json_object(path) is None

    def test_yaml_readers(self, tmp_path: Path):
        path = tmp_path / "config.yaml"
        path.write_text(DEEP_NESTING)
        assert mcp_lookup._search_yaml_key(path, "srv", "mcpServers") is None
        assert mcp_lookup._search_yaml_entry(path, "srv", "extensions") is None

    def test_hermes_reader(self, tmp_path: Path, monkeypatch):
        hermes = tmp_path / ".hermes"
        hermes.mkdir()
        (hermes / "config.yaml").write_text(DEEP_NESTING)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        assert mcp_lookup._read_hermes_mcp_servers() == {}

    def test_codex_toml_reader(self, tmp_path: Path):
        path = tmp_path / "config.toml"
        path.write_text(DEEP_NESTING_TOML)
        assert mcp_lookup._search_codex_toml_file(path, "srv") is None

    def test_codex_toml_reader_still_resolves_valid_config(self, tmp_path: Path):
        path = tmp_path / "config.toml"
        path.write_text('[mcp_servers.srv]\ncommand = "npx"\nargs = ["-y", "x"]\n')
        assert mcp_lookup._search_codex_toml_file(path, "srv") == MCPServer(
            command="npx -y x"
        )


def test_lookup_continues_past_poisoned_claude_json(tmp_path: Path, monkeypatch):
    """``~/.claude.json`` is read before the project ``.mcp.json`` candidates;
    poisoning it must not stop the project file from resolving the server."""
    home = tmp_path / "home"
    home.mkdir()
    (home / ".claude.json").write_text(DEEP_NESTING)
    project = tmp_path / "project"
    project.mkdir()
    (project / ".mcp.json").write_text(
        json.dumps({"mcpServers": {"srv": {"url": "https://mcp.example.com"}}})
    )
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    monkeypatch.setattr(
        mcp_lookup,
        "_claude_managed_mcp_config_path",
        lambda: tmp_path / "missing-managed.json",
    )

    assert mcp_lookup.lookup_mcp_server("srv", str(project)) == MCPServer(
        url="https://mcp.example.com"
    )


class TestCopilotCliReaders:
    def test_read_json_servers(self, poisoned: Path):
        assert copilot_cli_mcp_lookup._read_json_servers(poisoned, "mcpServers") == {}

    def test_read_json_object(self, poisoned: Path):
        assert copilot_cli_mcp_lookup._read_json_object(poisoned) is None

    def test_inline_session_config_value(self):
        maps = list(
            copilot_cli_mcp_lookup._github_copilot_cli_mcp_server_maps_from_value(
                DEEP_NESTING
            )
        )
        assert maps == []

    def test_lookup_continues_past_poisoned_project_file(
        self, tmp_path: Path, monkeypatch
    ):
        """``<cwd>/.mcp.json`` is the first candidate; poisoning it must not
        stop ``<cwd>/.github/mcp.json`` from resolving the server."""
        project = tmp_path / "project"
        (project / ".github").mkdir(parents=True)
        (project / ".mcp.json").write_text(DEEP_NESTING)
        (project / ".github" / "mcp.json").write_text(
            json.dumps({"mcpServers": {"srv": {"url": "https://mcp.example.com"}}})
        )
        monkeypatch.setattr(copilot_cli_mcp_lookup, "_copilot_home_root", lambda: None)

        assert copilot_cli_mcp_lookup.lookup_github_copilot_cli_mcp_server(
            "srv", str(project), home_path=tmp_path / "home"
        ) == MCPServer(url="https://mcp.example.com")
