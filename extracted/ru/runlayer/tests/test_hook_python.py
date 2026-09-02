"""Unit tests for the Python hook modules (replaces bash subprocess tests)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from runlayer_cli.hook.clients import (
    EVENT_NORMALIZE,
    Client,
    HookResponse,
    detect_client,
    normalize_event_name,
    should_noop_for_cursor,
    should_noop_for_devin,
)
from runlayer_cli.hook.file_policy import (
    FilePolicyViolation,
    check_bash_command,
    check_file_read,
)
from runlayer_cli.hook import (
    _transcript_stream_worker,
    hook_io,
    mcp_lookup,
    messages,
    relay,
    transcript_stream,
)
from runlayer_cli.hook import __main__ as hook_main
from runlayer_cli.hook import dispatch as hook_dispatch
from runlayer_cli.hook.mcp_lookup import (
    _claude_enabled_plugins,
    cline_cli_tool_resolves_mcp_source,
    is_goose_mcp_extension,
    lookup_codex_mcp_server,
    lookup_cursor_mcp_server,
    lookup_devin_cli_mcp_server,
    lookup_gemini_cli_mcp_server,
    lookup_github_copilot_cli_mcp_server,
    lookup_goose_mcp_server,
    lookup_grok_cli_mcp_server,
    lookup_mcp_server,
    lookup_windsurf_mcp_server,
    resolve_gemini_cli_mcp_tool,
    resolve_cline_cli_mcp_tool,
    resolve_github_copilot_cli_mcp_tool,
    resolve_hermes_mcp_tool,
)
from runlayer_cli.hook.windsurf_payload import (
    adapt_windsurf_payload,
    windsurf_mcp_tool_name,
)
from runlayer_cli.mdm_config import AIWatchMode


def _windows_path_mock(parent_str: str) -> type:
    """Stand-in for `pathlib.Path` that mimics Windows resolution.

    Returns a callable so that `Path(sys.argv[0]).absolute().parent` stringifies
    to the given backslash-separated `parent_str` regardless of host OS.
    """

    class _FakeParent:
        def __str__(self) -> str:
            return parent_str

    class _FakePath:
        def __init__(self, _arg: str) -> None:
            pass

        def absolute(self) -> "_FakePath":
            return self

        @property
        def parent(self) -> _FakeParent:
            return _FakeParent()

    return _FakePath


# =========================================================================
# file_policy tests
# =========================================================================


class TestCheckFileRead:
    def test_blocks_dot_env(self):
        with pytest.raises(FilePolicyViolation) as exc:
            check_file_read("/project/.env")
        assert "environment files" in exc.value.user_msg

    def test_blocks_env_production(self):
        with pytest.raises(FilePolicyViolation):
            check_file_read("/project/.env.production")

    def test_blocks_envrc(self):
        with pytest.raises(FilePolicyViolation):
            check_file_read("/project/.envrc")

    def test_blocks_star_dot_env(self):
        with pytest.raises(FilePolicyViolation):
            check_file_read("/project/staging.env")

    def test_blocks_mcp_json(self):
        with pytest.raises(FilePolicyViolation) as exc:
            check_file_read("/project/mcp.json")
        assert "MCP configuration" in exc.value.user_msg

    def test_blocks_dot_mcp_json(self):
        with pytest.raises(FilePolicyViolation):
            check_file_read("/project/.mcp.json")

    def test_blocks_mcp_config_json(self):
        with pytest.raises(FilePolicyViolation):
            check_file_read("/project/mcp_config.json")

    def test_blocks_mcp_dash_config_json(self):
        with pytest.raises(FilePolicyViolation):
            check_file_read("/project/mcp-config.json")

    def test_blocks_mcp_yaml(self):
        with pytest.raises(FilePolicyViolation):
            check_file_read("/project/mcp.yaml")

    def test_blocks_mcp_yml(self):
        with pytest.raises(FilePolicyViolation):
            check_file_read("/project/mcp.yml")

    def test_blocks_claude_json(self):
        with pytest.raises(FilePolicyViolation):
            check_file_read("/home/user/.claude.json")

    def test_blocks_claude_desktop_config(self):
        with pytest.raises(FilePolicyViolation):
            check_file_read(
                "/Library/Application Support/Claude/claude_desktop_config.json"
            )

    def test_blocks_claude_settings_json(self):
        with pytest.raises(FilePolicyViolation) as exc:
            check_file_read("/home/user/.claude/settings.json")
        assert "Claude Code settings" in exc.value.user_msg

    def test_blocks_claude_settings_case_insensitive(self):
        with pytest.raises(FilePolicyViolation):
            check_file_read("/home/user/.Claude/settings.json")

    def test_blocks_claude_settings_windows_backslashes(self):
        """Regression: Windows paths use backslashes, not forward slashes.

        Without backslash normalization the substring check for
        ``/.claude/settings.json`` fails on Windows, bypassing the Claude
        settings protection in ENFORCE mode.  ``ntpath`` simulates
        ``os.path`` on Windows so the basename check extracts
        ``settings.json`` the same way it would on a real Windows host.
        """
        import ntpath

        with patch("runlayer_cli.hook.file_policy.os.path", ntpath):
            with pytest.raises(FilePolicyViolation) as exc:
                check_file_read(r"C:\Users\user\.claude\settings.json")
        assert "Claude Code settings" in exc.value.user_msg

    def test_blocks_claude_settings_mixed_separators(self):
        """Edge case: mixed forward/backward slashes still match after normalization."""
        import ntpath

        with patch("runlayer_cli.hook.file_policy.os.path", ntpath):
            with pytest.raises(FilePolicyViolation):
                check_file_read(r"C:/Users/user\.claude/settings.json")

    def test_allows_vscode_settings_json(self):
        check_file_read("/project/.vscode/settings.json")

    def test_allows_normal_file(self):
        check_file_read("/project/src/main.py")

    def test_allows_empty_path(self):
        check_file_read("")

    def test_allows_none_coerced(self):
        check_file_read("")


class TestCheckBashCommand:
    def test_blocks_cat_dot_env(self):
        with pytest.raises(FilePolicyViolation):
            check_bash_command("cat .env")

    def test_blocks_head_env_production(self):
        with pytest.raises(FilePolicyViolation):
            check_bash_command("head -n 10 .env.production")

    def test_blocks_cat_dot_mcp_json(self):
        with pytest.raises(FilePolicyViolation):
            check_bash_command("cat .mcp.json")

    def test_blocks_double_quoted_env(self):
        with pytest.raises(FilePolicyViolation):
            check_bash_command('cat ".env"')

    def test_blocks_single_quoted_env(self):
        with pytest.raises(FilePolicyViolation):
            check_bash_command("cat '.env'")

    def test_blocks_piped_env(self):
        with pytest.raises(FilePolicyViolation):
            check_bash_command("cat .env | jq .")

    def test_blocks_subshell_env(self):
        with pytest.raises(FilePolicyViolation):
            check_bash_command("echo $(cat .env)")

    def test_allows_normal_command(self):
        check_bash_command("ls -la /project/src")

    def test_allows_empty(self):
        check_bash_command("")

    def test_skips_flags_and_numbers(self):
        check_bash_command("head -n 10 README.md")

    def test_blocks_double_quoted_env_production(self):
        with pytest.raises(FilePolicyViolation):
            check_bash_command('head -n 10 ".env.production"')


# =========================================================================
# mcp_lookup tests
# =========================================================================


class TestClineCliMCPLookup:
    """Cline flattens MCP tools to ``<server>__<tool>`` with no ``mcp__`` prefix.

    The transform is lossy (sanitize + sha1 truncation past 64 chars) and ``__``
    is legal inside names, so resolution matches against the configured server
    inventory instead of splitting the string.
    """

    def _write_settings(self, root: Path, servers: dict) -> None:
        settings = root / "data" / "settings" / "cline_mcp_settings.json"
        settings.parent.mkdir(parents=True, exist_ok=True)
        settings.write_text(json.dumps({"mcpServers": servers}))

    def test_resolves_flat_server_tool_name(self, tmp_path, monkeypatch):
        monkeypatch.setenv("CLINE_DIR", str(tmp_path))
        self._write_settings(
            tmp_path, {"myserver": {"url": "https://mcp.example.com/sse"}}
        )

        resolved = resolve_cline_cli_mcp_tool("myserver__search_docs")

        assert resolved is not None
        server_name, server = resolved
        assert server_name == "myserver"
        assert server["url"] == "https://mcp.example.com/sse"

    def test_unconfigured_server_does_not_resolve(self, tmp_path, monkeypatch):
        monkeypatch.setenv("CLINE_DIR", str(tmp_path))
        self._write_settings(tmp_path, {"myserver": {"url": "https://x/sse"}})

        assert resolve_cline_cli_mcp_tool("otherserver__tool") is None
        assert not cline_cli_tool_resolves_mcp_source("otherserver__tool")

    def test_plain_local_tool_name_is_not_mcp(self, tmp_path, monkeypatch):
        monkeypatch.setenv("CLINE_DIR", str(tmp_path))
        self._write_settings(tmp_path, {"myserver": {"url": "https://x/sse"}})

        # Cline's built-in tools carry no "__" at all.
        assert resolve_cline_cli_mcp_tool("run_commands") is None
        assert resolve_cline_cli_mcp_tool("read_files") is None

    def test_truncated_hashed_name_still_resolves_by_prefix(
        self, tmp_path, monkeypatch
    ):
        # Over 64 chars, Cline truncates to 55 + "_" + 8 hex sha1. Truncation
        # removes the TAIL, so the server prefix survives.
        monkeypatch.setenv("CLINE_DIR", str(tmp_path))
        self._write_settings(tmp_path, {"myserver": {"url": "https://x/sse"}})
        mangled = "myserver__a_very_long_tool_name_that_got_truncated_here_1a2b3c4d"

        resolved = resolve_cline_cli_mcp_tool(mangled)

        assert resolved is not None
        assert resolved[0] == "myserver"

    def test_server_name_with_bad_chars_matches_sanitized_form(
        self, tmp_path, monkeypatch
    ):
        # Cline replaces characters outside [a-zA-Z0-9_-] with "_", including in
        # the server name, so the emitted prefix differs from the configured key.
        monkeypatch.setenv("CLINE_DIR", str(tmp_path))
        self._write_settings(tmp_path, {"my.server": {"url": "https://x/sse"}})

        resolved = resolve_cline_cli_mcp_tool("my_server__search")

        assert resolved is not None
        assert resolved[0] == "my.server"

    def test_longest_server_name_wins_over_shorter_prefix(self, tmp_path, monkeypatch):
        monkeypatch.setenv("CLINE_DIR", str(tmp_path))
        self._write_settings(
            tmp_path,
            {
                "linear": {"url": "https://short/sse"},
                "linear__extra": {"url": "https://long/sse"},
            },
        )

        resolved = resolve_cline_cli_mcp_tool("linear__extra__search")

        assert resolved is not None
        assert resolved[0] == "linear__extra"
        assert resolved[1]["url"] == "https://long/sse"

    def test_missing_settings_file_resolves_nothing(self, tmp_path, monkeypatch):
        monkeypatch.setenv("CLINE_DIR", str(tmp_path))

        assert resolve_cline_cli_mcp_tool("myserver__tool") is None


class TestMCPLookup:
    def test_finds_url_in_project_mcp_json(self):
        with tempfile.TemporaryDirectory() as td:
            mcp_file = Path(td) / ".mcp.json"
            mcp_file.write_text(
                json.dumps(
                    {"mcpServers": {"myserver": {"url": "https://mcp.example.com/sse"}}}
                )
            )
            result = lookup_mcp_server("myserver", td)
            assert result is not None
            assert result["url"] == "https://mcp.example.com/sse"

    def test_finds_command_in_project_mcp_json(self):
        with tempfile.TemporaryDirectory() as td:
            mcp_file = Path(td) / ".mcp.json"
            mcp_file.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "myserver": {"command": "npx", "args": ["-y", "my-mcp"]}
                        }
                    }
                )
            )
            result = lookup_mcp_server("myserver", td)
            assert result is not None
            assert result["command"] == "npx -y my-mcp"

    def test_finds_url_in_claude_json_projects(self):
        with tempfile.TemporaryDirectory() as td:
            claude_json = Path(td) / ".claude.json"
            claude_json.write_text(
                json.dumps(
                    {
                        "projects": {
                            "/my/project": {
                                "mcpServers": {
                                    "myserver": {"url": "https://project.example.com"}
                                }
                            }
                        }
                    }
                )
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_mcp_server("myserver", "/my/project")
            assert result is not None
            assert result["url"] == "https://project.example.com"

    def test_finds_url_in_claude_json_global(self):
        with tempfile.TemporaryDirectory() as td:
            claude_json = Path(td) / ".claude.json"
            claude_json.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "globalserver": {"url": "https://global.example.com"}
                        }
                    }
                )
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_mcp_server("globalserver", "/nonexistent")
            assert result is not None
            assert result["url"] == "https://global.example.com"

    def test_project_mcp_json_takes_precedence(self):
        with tempfile.TemporaryDirectory() as td:
            project_mcp = Path(td) / ".mcp.json"
            project_mcp.write_text(
                json.dumps(
                    {"mcpServers": {"myserver": {"url": "https://project-level.com"}}}
                )
            )
            claude_json = Path(td) / ".claude.json"
            claude_json.write_text(
                json.dumps(
                    {"mcpServers": {"myserver": {"url": "https://global-level.com"}}}
                )
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_mcp_server("myserver", td)
            assert result is not None
            assert result["url"] == "https://project-level.com"

    def test_returns_none_for_unknown_server(self):
        with tempfile.TemporaryDirectory() as td:
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_mcp_server("unknown", td)
            assert result is None

    def test_non_object_claude_json_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / ".claude.json").write_text("[]")
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_mcp_server("unknown", td)
            assert result is None

    def test_finds_url_in_claude_managed_mcp_json(self):
        # Enterprise managed MCP config (MDM-deployed): servers defined only in
        # managed-mcp.json must resolve, else enforce denies Runlayer-managed
        # proxies as "not registered".
        with tempfile.TemporaryDirectory() as td:
            managed_file = Path(td) / "managed-mcp.json"
            managed_file.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "jira": {
                                "type": "http",
                                "url": "https://acme.runlayer.com/api/v1/proxy/7a76c0fc/mcp",
                            }
                        }
                    }
                )
            )
            with (
                patch(
                    "runlayer_cli.hook.mcp_lookup.Path.home",
                    return_value=Path(td) / "home",
                ),
                patch(
                    "runlayer_cli.hook.mcp_lookup._claude_managed_mcp_config_path",
                    return_value=managed_file,
                ),
            ):
                result = lookup_mcp_server("jira", td)
            assert result is not None
            assert (
                result["url"] == "https://acme.runlayer.com/api/v1/proxy/7a76c0fc/mcp"
            )

    def test_finds_command_in_claude_managed_mcp_json(self):
        with tempfile.TemporaryDirectory() as td:
            managed_file = Path(td) / "managed-mcp.json"
            managed_file.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "local-tool": {
                                "type": "stdio",
                                "command": "uvx",
                                "args": ["runlayer", "run", "some-uuid"],
                            }
                        }
                    }
                )
            )
            with (
                patch(
                    "runlayer_cli.hook.mcp_lookup.Path.home",
                    return_value=Path(td) / "home",
                ),
                patch(
                    "runlayer_cli.hook.mcp_lookup._claude_managed_mcp_config_path",
                    return_value=managed_file,
                ),
            ):
                result = lookup_mcp_server("local-tool", td)
            assert result is not None
            assert result["command"] == "uvx runlayer run some-uuid"

    def test_claude_managed_mcp_json_wins_name_collision(self):
        # When managed-mcp.json exists Claude Code treats it as exclusive, so
        # the managed definition is what tool calls actually route to.
        with tempfile.TemporaryDirectory() as td:
            project_mcp = Path(td) / ".mcp.json"
            project_mcp.write_text(
                json.dumps(
                    {"mcpServers": {"myserver": {"url": "https://project-level.com"}}}
                )
            )
            managed_file = Path(td) / "managed-mcp.json"
            managed_file.write_text(
                json.dumps(
                    {"mcpServers": {"myserver": {"url": "https://managed-level.com"}}}
                )
            )
            with (
                patch(
                    "runlayer_cli.hook.mcp_lookup.Path.home",
                    return_value=Path(td) / "home",
                ),
                patch(
                    "runlayer_cli.hook.mcp_lookup._claude_managed_mcp_config_path",
                    return_value=managed_file,
                ),
            ):
                result = lookup_mcp_server("myserver", td)
            assert result is not None
            assert result["url"] == "https://managed-level.com"

    def test_broken_claude_managed_mcp_json_falls_through(self):
        with tempfile.TemporaryDirectory() as td:
            project_mcp = Path(td) / ".mcp.json"
            project_mcp.write_text(
                json.dumps(
                    {"mcpServers": {"myserver": {"url": "https://project-level.com"}}}
                )
            )
            managed_file = Path(td) / "managed-mcp.json"
            managed_file.write_text("{not valid json")
            with (
                patch(
                    "runlayer_cli.hook.mcp_lookup.Path.home",
                    return_value=Path(td) / "home",
                ),
                patch(
                    "runlayer_cli.hook.mcp_lookup._claude_managed_mcp_config_path",
                    return_value=managed_file,
                ),
            ):
                result = lookup_mcp_server("myserver", td)
            assert result is not None
            assert result["url"] == "https://project-level.com"

    def test_claude_managed_mcp_config_path_per_platform(self, monkeypatch):
        monkeypatch.setattr("platform.system", lambda: "Darwin")
        assert mcp_lookup._claude_managed_mcp_config_path() == Path(
            "/Library/Application Support/ClaudeCode/managed-mcp.json"
        )

        monkeypatch.setattr("platform.system", lambda: "Windows")
        monkeypatch.setenv("PROGRAMFILES", r"C:\Program Files")
        assert (
            mcp_lookup._claude_managed_mcp_config_path()
            == Path(r"C:\Program Files") / "ClaudeCode" / "managed-mcp.json"
        )

        monkeypatch.setattr("platform.system", lambda: "Linux")
        assert mcp_lookup._claude_managed_mcp_config_path() == Path(
            "/etc/claude-code/managed-mcp.json"
        )

    def test_resolves_claude_ai_connector_from_ever_connected(self):
        """claude.ai account connectors carry no local URL; recognize them by name
        from `claudeAiMcpEverConnected` and forward them as a trusted source."""
        with tempfile.TemporaryDirectory() as td:
            claude_json = Path(td) / ".claude.json"
            claude_json.write_text(
                json.dumps(
                    {
                        "mcpServers": {},
                        "claudeAiMcpEverConnected": [
                            "claude.ai Granola",
                            "claude.ai Linear",
                            "claude.ai GDrive",
                        ],
                    }
                )
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_mcp_server("claude_ai_linear_2", td)
            assert result is not None
            assert result.get("source") == "claude-ai-connector"
            assert "url" not in result
            assert "command" not in result

    def test_claude_ai_connector_requires_ever_connected_entry(self):
        """A `claude_ai_*` tool whose connector is NOT in `claudeAiMcpEverConnected`
        still fails closed (unknown / spoofed server)."""
        with tempfile.TemporaryDirectory() as td:
            claude_json = Path(td) / ".claude.json"
            claude_json.write_text(
                json.dumps({"claudeAiMcpEverConnected": ["claude.ai Linear"]})
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_mcp_server("claude_ai_notreal", td)
            assert result is None

    def test_registered_server_wins_over_claude_ai_connector(self):
        """A genuinely-registered same-named server resolves to its URL, not the
        source-only connector fallback."""
        with tempfile.TemporaryDirectory() as td:
            claude_json = Path(td) / ".claude.json"
            claude_json.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "claude_ai_linear_2": {"url": "https://proxy.example.com"}
                        },
                        "claudeAiMcpEverConnected": ["claude.ai Linear"],
                    }
                )
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_mcp_server("claude_ai_linear_2", td)
            assert result is not None
            assert result["url"] == "https://proxy.example.com"
            assert result.get("source") is None

    def test_unregistered_uuid_named_server_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            claude_json = Path(td) / ".claude.json"
            claude_json.write_text(json.dumps({"mcpServers": {}}))
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_mcp_server("ca0566ef-4a4c-4e61-b085-67209e651810", td)
            assert result is None

    def test_registered_uuid_named_server_resolves_from_config(self):
        with tempfile.TemporaryDirectory() as td:
            claude_json = Path(td) / ".claude.json"
            claude_json.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "ca0566ef-4a4c-4e61-b085-67209e651810": {
                                "url": "https://proxy.example.com"
                            }
                        }
                    }
                )
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_mcp_server("ca0566ef-4a4c-4e61-b085-67209e651810", td)
            assert result is not None
            assert result["url"] == "https://proxy.example.com"
            assert result.get("source") is None

    def test_malformed_claude_json_still_fails_closed_for_unknown_names(self):
        """Corrupt config must not weaken anything else: unknown names and
        ever-connected-dependent claude_ai_* names still fail closed."""
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / ".claude.json").write_text("{not json")
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                assert lookup_mcp_server("some_random_server", td) is None
                assert lookup_mcp_server("claude_ai_linear_2", td) is None

    def test_resolves_github_copilot_cli_builtin_mcp_server_without_config(self):
        with tempfile.TemporaryDirectory() as td:
            result = resolve_github_copilot_cli_mcp_tool(
                "github-mcp-server-list_repos", td
            )

        assert result is not None
        server_name, server = result
        assert server_name == "github-mcp-server"
        assert server["name"] == "github-mcp-server"
        assert server["source"] == "github-copilot-cli-built-in"

    def test_resolves_github_copilot_cli_sanitized_mcp_server_prefix(self):
        with tempfile.TemporaryDirectory() as td:
            project_mcp = Path(td) / ".github" / "mcp.json"
            project_mcp.parent.mkdir()
            project_mcp.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "My Server!": {"url": "https://mcp.example.com/sse"},
                        }
                    }
                )
            )

            result = resolve_github_copilot_cli_mcp_tool("My-Server--search", td)

        assert result is not None
        server_name, server = result
        assert server_name == "My Server!"
        assert server["url"] == "https://mcp.example.com/sse"

    def test_resolves_github_copilot_cli_truncated_mcp_server_prefix(self):
        with tempfile.TemporaryDirectory() as td:
            project_mcp = Path(td) / ".github" / "mcp.json"
            project_mcp.parent.mkdir()
            server_name = "a" * 70
            project_mcp.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            server_name: {"url": "https://mcp.example.com/sse"},
                        }
                    }
                )
            )

            result = resolve_github_copilot_cli_mcp_tool("a" * 64, td)

        assert result is not None
        resolved_server_name, server = result
        assert resolved_server_name == server_name
        assert server["url"] == "https://mcp.example.com/sse"

    def test_resolves_github_copilot_cli_truncated_mcp_server_prefix_with_suffix(
        self,
    ):
        with tempfile.TemporaryDirectory() as td:
            project_mcp = Path(td) / ".github" / "mcp.json"
            project_mcp.parent.mkdir()
            server_name = "b" * 70
            project_mcp.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            server_name: {"url": "https://mcp.example.com/sse"},
                        }
                    }
                )
            )

            result = resolve_github_copilot_cli_mcp_tool(f"{'b' * 63}2", td)

        assert result is not None
        resolved_server_name, server = result
        assert resolved_server_name == server_name
        assert server["url"] == "https://mcp.example.com/sse"

    def test_claude_enabled_plugins_only_explicit_false_disables(self):
        with tempfile.TemporaryDirectory() as td:
            settings = Path(td) / ".claude" / "settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text(
                json.dumps(
                    {
                        "enabledPlugins": {
                            "false-plugin@runlayer": False,
                            "null-plugin@runlayer": None,
                            "string-plugin@runlayer": "false",
                        }
                    }
                )
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                enabled = _claude_enabled_plugins(td)

            assert enabled["false-plugin@runlayer"] is False
            assert enabled["null-plugin@runlayer"] is True
            assert enabled["string-plugin@runlayer"] is True

    def test_finds_url_in_claude_code_installed_plugin_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            project = Path(td) / "project"
            subdir = project / "src"
            subdir.mkdir(parents=True)
            project_settings = project / ".claude" / "settings.json"
            project_settings.parent.mkdir(parents=True)
            other_plugin_root = (
                home
                / ".claude"
                / "plugins"
                / "cache"
                / "runlayer"
                / "other-plugin"
                / "1.0.0"
            )
            other_plugin_root.mkdir(parents=True)
            (other_plugin_root / ".claude-plugin").mkdir()
            (other_plugin_root / ".claude-plugin" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "other-plugin",
                        "version": "1.0.0",
                        "mcpServers": {
                            "plugin_runlayer-test_linear-44": {
                                "url": "https://wrong.example.com/mcp"
                            }
                        },
                    }
                )
            )
            global_plugin_root = (
                home
                / ".claude"
                / "plugins"
                / "cache"
                / "runlayer"
                / "runlayer-test"
                / "global"
            )
            global_plugin_root.mkdir(parents=True)
            (global_plugin_root / ".claude-plugin").mkdir()
            (global_plugin_root / ".claude-plugin" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "runlayer-test",
                        "version": "1.0.0",
                        "mcpServers": {
                            "linear-44": {"url": "https://global-wrong.example.com/mcp"}
                        },
                    }
                )
            )
            plugin_root = (
                home
                / ".claude"
                / "plugins"
                / "cache"
                / "runlayer"
                / "runlayer-test"
                / "1.0.0"
            )
            plugin_root.mkdir(parents=True)
            (plugin_root / ".claude-plugin").mkdir()
            (plugin_root / ".claude-plugin" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "runlayer-test",
                        "description": "Runlayer plugin for repro",
                        "version": "1.0.0",
                        "mcpServers": {
                            "linear-44": {
                                "url": "https://example.runlayer.com/api/v1/proxy/servers/server-123/mcp"
                            }
                        },
                    }
                )
            )

            installed_plugins = home / ".claude" / "plugins" / "installed_plugins.json"
            installed_plugins.write_text(
                json.dumps(
                    {
                        "version": 2,
                        "plugins": {
                            "other-plugin@runlayer": [
                                {
                                    "scope": "project",
                                    "installPath": str(other_plugin_root),
                                    "projectPath": str(project),
                                    "version": "1.0.0",
                                }
                            ],
                            "runlayer-test@runlayer": [
                                {
                                    "scope": "user",
                                    "installPath": str(global_plugin_root),
                                    "version": "1.0.0",
                                },
                                {
                                    "scope": "project",
                                    "installPath": str(plugin_root),
                                    "projectPath": str(project),
                                    "version": "1.0.0",
                                },
                            ],
                        },
                    }
                )
            )
            settings = home / ".claude" / "settings.json"
            settings.write_text(
                json.dumps({"enabledPlugins": {"runlayer-test@runlayer": False}})
            )
            project_settings.write_text(
                json.dumps(
                    {
                        "enabledPlugins": {
                            "other-plugin@runlayer": True,
                            "runlayer-test@runlayer": True,
                        }
                    }
                )
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server(
                    "plugin_runlayer-test_linear-44", str(subdir)
                )

            assert result is not None
            assert result["url"] == (
                "https://example.runlayer.com/api/v1/proxy/servers/server-123/mcp"
            )

    def test_user_scope_claude_plugin_uses_project_settings_from_subdir(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            project = Path(td) / "project"
            subdir = project / "src"
            subdir.mkdir(parents=True)
            plugin_root = (
                home
                / ".claude"
                / "plugins"
                / "cache"
                / "runlayer"
                / "activity-recap"
                / "1.0.0"
            )
            plugin_root.mkdir(parents=True)
            (plugin_root / ".claude-plugin").mkdir()
            (plugin_root / ".claude-plugin" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "activity-recap",
                        "version": "1.0.0",
                        "mcpServers": {
                            "slack": {"url": "https://example.runlayer.com/mcp"}
                        },
                    }
                )
            )
            installed_plugins = home / ".claude" / "plugins" / "installed_plugins.json"
            installed_plugins.write_text(
                json.dumps(
                    {
                        "plugins": {
                            "activity-recap@runlayer": [
                                {
                                    "scope": "user",
                                    "installPath": str(plugin_root),
                                }
                            ]
                        }
                    }
                )
            )
            user_settings = home / ".claude" / "settings.json"
            user_settings.parent.mkdir(parents=True, exist_ok=True)
            user_settings.write_text(
                json.dumps({"enabledPlugins": {"activity-recap@runlayer": False}})
            )
            project_settings = project / ".claude" / "settings.json"
            project_settings.parent.mkdir(parents=True)
            project_settings.write_text(
                json.dumps({"enabledPlugins": {"activity-recap@runlayer": True}})
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server("plugin_activity-recap_slack", str(subdir))

            assert result is not None
            assert result["url"] == "https://example.runlayer.com/mcp"

    def test_serverurl_in_project_mcp_json_is_accepted(self):
        """Python hook accepts `serverUrl` (Windsurf) in JSON `.mcp.json`."""
        with tempfile.TemporaryDirectory() as td:
            mcp_file = Path(td) / ".mcp.json"
            mcp_file.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "myserver": {"serverUrl": "https://mcp.example.com/sse"}
                        }
                    }
                )
            )
            result = lookup_mcp_server("myserver", td)
            assert result is not None
            assert result["url"] == "https://mcp.example.com/sse"

    def test_uri_in_project_mcp_json_is_accepted(self):
        """Python hook accepts `uri` (Goose) in JSON `.mcp.json`."""
        with tempfile.TemporaryDirectory() as td:
            mcp_file = Path(td) / ".mcp.json"
            mcp_file.write_text(
                json.dumps(
                    {"mcpServers": {"myserver": {"uri": "https://mcp.example.com/sse"}}}
                )
            )
            result = lookup_mcp_server("myserver", td)
            assert result is not None
            assert result["url"] == "https://mcp.example.com/sse"

    def test_serverurl_in_claude_json_projects_is_accepted(self):
        """Python hook accepts `serverUrl` in `.claude.json` project entries."""
        with tempfile.TemporaryDirectory() as td:
            claude_json = Path(td) / ".claude.json"
            claude_json.write_text(
                json.dumps(
                    {
                        "projects": {
                            "/my/project": {
                                "mcpServers": {
                                    "myserver": {
                                        "serverUrl": "https://project.example.com"
                                    }
                                }
                            }
                        }
                    }
                )
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_mcp_server("myserver", "/my/project")
            assert result is not None
            assert result["url"] == "https://project.example.com"

    def test_uri_in_claude_json_global_is_accepted(self):
        """Python hook accepts `uri` in `.claude.json` global entries."""
        with tempfile.TemporaryDirectory() as td:
            claude_json = Path(td) / ".claude.json"
            claude_json.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "globalserver": {"uri": "https://global.example.com"}
                        }
                    }
                )
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_mcp_server("globalserver", "/nonexistent")
            assert result is not None
            assert result["url"] == "https://global.example.com"

    def test_cursor_lookup_resolves_workspace_url_with_user_prefix(self):
        with tempfile.TemporaryDirectory() as td:
            cursor_file = Path(td) / ".cursor" / "mcp.json"
            cursor_file.parent.mkdir()
            cursor_file.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "linear-44": {"url": "https://mcp.example.com/sse"}
                        }
                    }
                )
            )

            result = lookup_cursor_mcp_server(
                "user-Linear44", {"workspace_roots": [td]}
            )

            assert result is not None
            assert result["url"] == "https://mcp.example.com/sse"

    def test_cursor_lookup_resolves_stdio_command_from_cwd(self):
        with tempfile.TemporaryDirectory() as td:
            cursor_file = Path(td) / ".cursor" / "mcp.json"
            cursor_file.parent.mkdir()
            cursor_file.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "local-runlayer": {
                                "command": "runlayer",
                                "args": ["run", "server-123"],
                            }
                        }
                    }
                )
            )

            result = lookup_cursor_mcp_server("local-runlayer", {"cwd": td})

            assert result is not None
            assert result["command"] == "runlayer run server-123"

    def test_cursor_lookup_returns_none_for_unknown_server(self):
        with tempfile.TemporaryDirectory() as td:
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_cursor_mcp_server("unknown", {"cwd": td})
            assert result is None

    def test_codex_lookup_finds_url_in_config_toml(self):
        with tempfile.TemporaryDirectory() as td:
            codex_file = Path(td) / ".codex" / "config.toml"
            codex_file.parent.mkdir()
            codex_file.write_text(
                '[mcp_servers.linear-44]\nurl = "https://mcp.example.com/sse"\n'
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_codex_mcp_server("linear-44")
            assert result is not None
            assert result["url"] == "https://mcp.example.com/sse"

    def test_codex_lookup_finds_normalized_stdio_command_in_managed_config(self):
        with tempfile.TemporaryDirectory() as td:
            codex_file = Path(td) / ".codex" / "managed_config.toml"
            codex_file.parent.mkdir()
            codex_file.write_text(
                "[mcp_servers.runlayer-local-stdio-smoke]\n"
                'command = "runlayer"\n'
                'args = ["run", "server-123"]\n'
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_codex_mcp_server("runlayer_local_stdio_smoke")
            assert result is not None
            assert result["command"] == "runlayer run server-123"

    def test_goose_lookup_finds_uri_in_config_yaml(self):
        with tempfile.TemporaryDirectory() as td:
            goose_file = Path(td) / ".config" / "goose" / "config.yaml"
            goose_file.parent.mkdir(parents=True)
            goose_file.write_text(
                "extensions:\n  linear-44:\n    uri: https://mcp.example.com/sse\n"
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_goose_mcp_server("linear-44")
                is_mcp = is_goose_mcp_extension("linear-44")
            assert result is not None
            assert result["url"] == "https://mcp.example.com/sse"
            assert is_mcp is True

    def test_goose_lookup_skips_platform_extension(self):
        with tempfile.TemporaryDirectory() as td:
            goose_file = Path(td) / ".config" / "goose" / "config.yaml"
            goose_file.parent.mkdir(parents=True)
            goose_file.write_text(
                "extensions:\n"
                "  todo:\n"
                "    enabled: true\n"
                "    type: platform\n"
                "    name: todo\n"
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_goose_mcp_server("todo")
                is_mcp = is_goose_mcp_extension("todo")
            assert result is None
            assert is_mcp is False

    def test_goose_lookup_skips_disabled_extension(self):
        with tempfile.TemporaryDirectory() as td:
            goose_file = Path(td) / ".config" / "goose" / "config.yaml"
            goose_file.parent.mkdir(parents=True)
            goose_file.write_text(
                "extensions:\n"
                "  disabled-server:\n"
                "    enabled: false\n"
                "    type: stdio\n"
                "    cmd: npx\n"
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_goose_mcp_server("disabled-server")
                is_mcp = is_goose_mcp_extension("disabled-server")
            assert result is None
            assert is_mcp is False

    def test_github_copilot_cli_lookup_finds_project_mcp_json(self):
        with tempfile.TemporaryDirectory() as td:
            project_mcp = Path(td) / ".github" / "mcp.json"
            project_mcp.parent.mkdir()
            project_mcp.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "linear-44": {"url": "https://mcp.example.com/sse"}
                        }
                    }
                )
            )

            result = lookup_github_copilot_cli_mcp_server("linear-44", td)

            assert result is not None
            assert result["url"] == "https://mcp.example.com/sse"

    def test_github_copilot_cli_lookup_uses_copilot_home(self):
        with tempfile.TemporaryDirectory() as td:
            copilot_home = Path(td) / "copilot-home"
            copilot_home.mkdir()
            (copilot_home / "mcp-config.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "local-runlayer": {
                                "command": "runlayer",
                                "args": ["run", "server-123"],
                            }
                        }
                    }
                )
            )

            with patch.dict(os.environ, {"COPILOT_HOME": str(copilot_home)}):
                result = lookup_github_copilot_cli_mcp_server(
                    "local-runlayer", "/project"
                )

            assert result is not None
            assert result["command"] == "runlayer run server-123"

    def test_github_copilot_cli_lookup_prefers_additional_mcp_config_payload(self):
        with tempfile.TemporaryDirectory() as td:
            copilot_root = Path(td) / ".copilot"
            copilot_root.mkdir()
            (copilot_root / "mcp-config.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "session-only": {"url": "https://stale.example/sse"}
                        }
                    }
                )
            )
            payload = {
                "additional_mcp_config": json.dumps(
                    {
                        "mcpServers": {
                            "session-only": {"url": "https://session.example/sse"}
                        }
                    }
                )
            }

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_github_copilot_cli_mcp_server(
                    "session-only",
                    "/project",
                    payload,
                )

            assert result is not None
            assert result["url"] == "https://session.example/sse"

    def test_resolves_github_copilot_cli_additional_mcp_config_file_from_env(self):
        with tempfile.TemporaryDirectory() as td:
            session_config = Path(td) / "session-mcp.json"
            session_config.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "session-only": {"url": "https://session.example/sse"}
                        }
                    }
                )
            )

            with patch.dict(
                os.environ,
                {
                    "RUNLAYER_GITHUB_COPILOT_CLI_ADDITIONAL_MCP_CONFIG": (
                        f"@{session_config}"
                    )
                },
            ):
                result = resolve_github_copilot_cli_mcp_tool(
                    "session-only-search",
                    "/repo",
                )

        assert result is not None
        server_name, server = result
        assert server_name == "session-only"
        assert server["url"] == "https://session.example/sse"

    def test_relative_additional_mcp_config_uses_daemon_request_cwd(self):
        with tempfile.TemporaryDirectory() as td:
            request_cwd = Path(td) / "request"
            request_cwd.mkdir()
            (request_cwd / "session-mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "session-only": {"url": "https://session.example/sse"}
                        }
                    }
                )
            )
            request_io = hook_io.HookIO(
                cwd=str(request_cwd),
                env={
                    "RUNLAYER_GITHUB_COPILOT_CLI_ADDITIONAL_MCP_CONFIG": (
                        "@session-mcp.json"
                    )
                },
            )

            with hook_io.scoped(request_io):
                result = resolve_github_copilot_cli_mcp_tool(
                    "session-only-search",
                    str(request_cwd),
                )

        assert result is not None
        server_name, server = result
        assert server_name == "session-only"
        assert server["url"] == "https://session.example/sse"

    def test_resolves_github_copilot_cli_installed_plugin_mcp_server(self):
        with tempfile.TemporaryDirectory() as td:
            plugin_dir = (
                Path(td) / ".copilot" / "installed-plugins" / "work-iq" / "workiq"
            )
            plugin_dir.mkdir(parents=True)
            (plugin_dir / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "workiq": {"url": "https://mcp.workiq.example/sse"}
                        }
                    }
                )
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = resolve_github_copilot_cli_mcp_tool("workiq-search", "/repo")

        assert result is not None
        server_name, server = result
        assert server_name == "workiq"
        assert server["url"] == "https://mcp.workiq.example/sse"

    def test_github_copilot_cli_plugin_mcp_overrides_user_config(self):
        with tempfile.TemporaryDirectory() as td:
            copilot_root = Path(td) / ".copilot"
            copilot_root.mkdir()
            (copilot_root / "mcp-config.json").write_text(
                json.dumps(
                    {"mcpServers": {"workiq": {"url": "https://stale.example/sse"}}}
                )
            )
            plugin_dir = copilot_root / "installed-plugins" / "work-iq" / "workiq"
            plugin_dir.mkdir(parents=True)
            (plugin_dir / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "workiq": {"url": "https://mcp.workiq.example/sse"}
                        }
                    }
                )
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = resolve_github_copilot_cli_mcp_tool("workiq-search", "/repo")

        assert result is not None
        _server_name, server = result
        assert server["url"] == "https://mcp.workiq.example/sse"

    def test_github_copilot_cli_plugin_mcp_uses_last_loaded_duplicate_server(self):
        with tempfile.TemporaryDirectory() as td:
            plugins_root = Path(td) / ".copilot" / "installed-plugins" / "marketplace"
            older_plugin = plugins_root / "aaa-workiq"
            newer_plugin = plugins_root / "zzz-workiq"
            older_plugin.mkdir(parents=True)
            newer_plugin.mkdir(parents=True)
            (older_plugin / ".mcp.json").write_text(
                json.dumps(
                    {"mcpServers": {"workiq": {"url": "https://old.example/sse"}}}
                )
            )
            (newer_plugin / ".mcp.json").write_text(
                json.dumps(
                    {"mcpServers": {"workiq": {"url": "https://new.example/sse"}}}
                )
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = resolve_github_copilot_cli_mcp_tool("workiq-search", "/repo")

        assert result is not None
        _server_name, server = result
        assert server["url"] == "https://new.example/sse"

    def test_resolves_github_copilot_cli_plugin_manifest_mcp_path(self):
        with tempfile.TemporaryDirectory() as td:
            plugin_dir = (
                Path(td) / ".copilot" / "installed-plugins" / "marketplace" / "plugin-a"
            )
            (plugin_dir / ".plugin").mkdir(parents=True)
            (plugin_dir / "custom").mkdir()
            (plugin_dir / ".plugin" / "plugin.json").write_text(
                json.dumps({"mcpServers": "custom/mcp.json"})
            )
            (plugin_dir / "custom" / "mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "server-a": {"url": "https://mcp.plugin.example/sse"}
                        }
                    }
                )
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = resolve_github_copilot_cli_mcp_tool("server-a-search", "/repo")

        assert result is not None
        server_name, server = result
        assert server_name == "server-a"
        assert server["url"] == "https://mcp.plugin.example/sse"

    def test_goose_lookup_finds_normalized_stdio_cmd(self):
        with tempfile.TemporaryDirectory() as td:
            goose_file = Path(td) / ".config" / "goose" / "config.yaml"
            goose_file.parent.mkdir(parents=True)
            goose_file.write_text(
                "extensions:\n"
                "  runlayer-local-stdio-smoke:\n"
                "    cmd: runlayer\n"
                "    args: [run, server-123]\n"
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_goose_mcp_server("runlayer_local_stdio_smoke")
            assert result is not None
            assert result["command"] == "runlayer run server-123"

    def test_hermes_tool_lookup_uses_longest_normalized_server_prefix(self):
        with tempfile.TemporaryDirectory() as td:
            hermes_file = Path(td) / ".hermes" / "config.yaml"
            hermes_file.parent.mkdir()
            hermes_file.write_text(
                "mcp_servers:\n"
                "  linear:\n"
                "    url: https://short.example.com/sse\n"
                "  linear-44:\n"
                "    command: runlayer\n"
                "    args: [run, server-123]\n"
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = resolve_hermes_mcp_tool("mcp_linear_44_list_issues")

            assert result is not None
            server_name, server = result
            assert server_name == "linear-44"
            assert server["command"] == "runlayer run server-123"

    def test_hermes_tool_lookup_handles_numeric_server_key(self):
        with tempfile.TemporaryDirectory() as td:
            hermes_file = Path(td) / ".hermes" / "config.yaml"
            hermes_file.parent.mkdir()
            hermes_file.write_text(
                "mcp_servers:\n  12306:\n    url: https://mcp.example.com/sse\n"
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = resolve_hermes_mcp_tool("mcp_12306_list_trains")

            assert result is not None
            server_name, server = result
            assert server_name == "12306"
            assert server["url"] == "https://mcp.example.com/sse"

    def test_gemini_cli_tool_lookup_uses_longest_normalized_server_prefix(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            project = Path(td) / "project"
            settings = project / ".gemini" / "settings.json"
            settings.parent.mkdir(parents=True)
            home.mkdir()
            settings.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "linear": {"url": "https://short.example.com/sse"},
                            "linear-44": {
                                "command": "runlayer",
                                "args": ["run", "server-123"],
                            },
                        }
                    }
                )
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = resolve_gemini_cli_mcp_tool(
                    "mcp_linear_44_list_issues", str(project)
                )

            assert result is not None
            server_name, server = result
            assert server_name == "linear-44"
            assert server["command"] == "runlayer run server-123"

    def test_gemini_cli_tool_lookup_reads_user_settings(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            settings = home / ".gemini" / "settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text(
                json.dumps(
                    {
                        "security": {"auth": {"selectedType": "oauth-personal"}},
                        "mcpServers": {
                            "linear": {"url": "https://mcp.example.com/sse"}
                        },
                    }
                )
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = resolve_gemini_cli_mcp_tool(
                    "mcp_linear_list_issues", str(Path(td) / "project")
                )

            assert result is not None
            server_name, server = result
            assert server_name == "linear"
            assert server["url"] == "https://mcp.example.com/sse"

    def test_gemini_cli_tool_lookup_resolves_http_url_only_entry(self):
        """Regression guard: Gemini's streamable-HTTP servers use ``httpUrl``,
        which ``_extract_server_entry`` must accept alongside ``url``/``uri``."""
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            settings = home / ".gemini" / "settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "linear": {"httpUrl": "https://mcp.example.com/mcp"}
                        }
                    }
                )
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = resolve_gemini_cli_mcp_tool(
                    "mcp_linear_list_issues", str(Path(td) / "project")
                )

            assert result is not None
            assert result[1]["url"] == "https://mcp.example.com/mcp"

    def test_gemini_cli_project_settings_win_over_user_settings(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            project = Path(td) / "project"
            for root, url in (
                (home / ".gemini", "https://user.example.com/sse"),
                (project / ".gemini", "https://project.example.com/sse"),
            ):
                root.mkdir(parents=True)
                (root / "settings.json").write_text(
                    json.dumps({"mcpServers": {"linear": {"url": url}}})
                )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_gemini_cli_mcp_server("linear", str(project))

            assert result is not None
            assert result["url"] == "https://project.example.com/sse"

    def test_gemini_cli_system_settings_win_over_project_and_user_settings(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            project = Path(td) / "project"
            system = Path(td) / "system"
            for root, url in (
                (home / ".gemini", "https://user.example.com/sse"),
                (project / ".gemini", "https://project.example.com/sse"),
                (system, "https://system.example.com/sse"),
            ):
                root.mkdir(parents=True)
                (root / "settings.json").write_text(
                    json.dumps({"mcpServers": {"linear": {"url": url}}})
                )

            with (
                patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home),
                patch(
                    "runlayer_cli.hook.mcp_lookup._gemini_cli_system_settings_dir",
                    return_value=system,
                ),
            ):
                result = lookup_gemini_cli_mcp_server("linear", str(project))

            assert result is not None
            assert result["url"] == "https://system.example.com/sse"

    def test_gemini_cli_lookup_returns_none_for_unregistered_server(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            settings = home / ".gemini" / "settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text(
                json.dumps({"mcpServers": {"linear": {"url": "https://x.example/sse"}}})
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                assert (
                    resolve_gemini_cli_mcp_tool(
                        "mcp_unknown_list_issues", str(Path(td) / "project")
                    )
                    is None
                )
                assert (
                    lookup_gemini_cli_mcp_server("unknown", str(Path(td) / "project"))
                    is None
                )

    def test_gemini_cli_tool_lookup_ignores_non_mcp_prefixed_names(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            home.mkdir()
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                assert resolve_gemini_cli_mcp_tool("run_shell_command", str(td)) is None

    def test_hermes_tool_lookup_ignores_non_mapping_yaml_root(self):
        with tempfile.TemporaryDirectory() as td:
            hermes_file = Path(td) / ".hermes" / "config.yaml"
            hermes_file.parent.mkdir()
            hermes_file.write_text("- not\n- a\n- mapping\n")

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = resolve_hermes_mcp_tool("mcp_linear_44_list_issues")

            assert result is None

    def test_resolves_claude_plugin_server_not_in_installed_plugins_json(self):
        """ENG-3439 repro: enforce fails closed for plugin-defined MCP servers.

        Claude Code passes only the namespaced server name
        (``mcp__plugin_<plugin>_<server>__<tool>``). When the plugin is active
        on disk but absent from ``installed_plugins.json`` (the Cowork/managed
        install case, e.g. the ``box`` / ``runlayer`` plugins), the hook can't
        match the name back to the plugin's defined MCP server config, returns
        None, and the call is hard-blocked ("Only Runlayer-managed MCP servers
        are allowed").

        Verified live: ``plugin_runlayer_onelayer`` / ``plugin_runlayer_runlayer``
        resolve to None on this machine while ``plugin_activity-recap_*`` (which
        IS in installed_plugins.json) resolve fine.
        """
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            project = Path(td) / "project"
            project.mkdir(parents=True)

            # Plugin is installed on disk (canonical top-level plugin dir, as a
            # symlinked/marketplace plugin would be) and defines an MCP server
            # pointing at the Runlayer proxy.
            box_root = home / ".claude" / "plugins" / "box"
            (box_root / ".claude-plugin").mkdir(parents=True)
            (box_root / ".claude-plugin" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "box",
                        "version": "1.0.0",
                        "mcpServers": {
                            "box": {
                                "url": "https://example.runlayer.com/api/v1/proxy/0a5f7d71-a62d-44b6-bd1b-4591b4deb8ac/mcp",
                                "type": "http",
                            }
                        },
                    }
                )
            )

            # Registry knows about a *different* plugin only -- "box" was
            # installed by a channel that never wrote installed_plugins.json.
            installed_plugins = home / ".claude" / "plugins" / "installed_plugins.json"
            installed_plugins.write_text(json.dumps({"version": 2, "plugins": {}}))
            settings = home / ".claude" / "settings.json"
            settings.write_text(json.dumps({"enabledPlugins": {"box@runlayer": True}}))

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server("plugin_box_box", str(project))

            assert result is not None, (
                "enforce hook could not resolve a plugin-defined MCP server "
                "(ENG-3439) -> would fail closed and block the call"
            )
            assert result["url"] == (
                "https://example.runlayer.com/api/v1/proxy/0a5f7d71-a62d-44b6-bd1b-4591b4deb8ac/mcp"
            )

    def test_resolves_claude_marketplace_external_plugin_server(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            project = Path(td) / "project"
            project.mkdir(parents=True)
            plugin_root = (
                home
                / ".claude"
                / "plugins"
                / "marketplaces"
                / "claude-plugins-official"
                / "external_plugins"
                / "linear"
            )
            manifest_dir = plugin_root / ".claude-plugin"
            manifest_dir.mkdir(parents=True)
            (manifest_dir / "plugin.json").write_text(json.dumps({"name": "linear"}))
            (plugin_root / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "linear": {
                                "url": "https://linear.example/mcp",
                            }
                        }
                    }
                )
            )
            plugins_dir = home / ".claude" / "plugins"
            (plugins_dir / "installed_plugins.json").write_text(
                json.dumps({"version": 2, "plugins": {}})
            )
            settings = home / ".claude" / "settings.json"
            settings.write_text(
                json.dumps(
                    {
                        "enabledPlugins": {
                            "linear@claude-plugins-official": True,
                        }
                    }
                )
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server("plugin_linear_linear", str(project))

            assert result is not None
            assert result["url"] == "https://linear.example/mcp"

    def test_resolves_claude_plugin_server_from_install_cache(self):
        """ENG-3439: a plugin cached on disk but missing from the registry
        resolves via the install-cache scan."""
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            project = Path(td) / "project"
            project.mkdir(parents=True)

            cache_root = (
                home
                / ".claude"
                / "plugins"
                / "cache"
                / "runlayer"
                / "runlayer"
                / "1.0.0"
            )
            (cache_root / ".claude-plugin").mkdir(parents=True)
            (cache_root / ".claude-plugin" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "runlayer",
                        "version": "1.0.0",
                        "mcpServers": {
                            "onelayer": {
                                "url": "https://acme.runlayer.com/api/v1/proxy/abc/mcp",
                                "type": "http",
                            }
                        },
                    }
                )
            )
            installed_plugins = home / ".claude" / "plugins" / "installed_plugins.json"
            installed_plugins.write_text(json.dumps({"version": 2, "plugins": {}}))

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server("plugin_runlayer_onelayer", str(project))

            assert result is not None
            assert result["url"] == "https://acme.runlayer.com/api/v1/proxy/abc/mcp"

    def test_registry_disabled_plugin_not_resolved_via_filesystem_fallback(self):
        """A plugin the registry lists as disabled must stay unresolved -- the
        filesystem fallback must not silently re-enable it."""
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            project = Path(td) / "project"
            project.mkdir(parents=True)

            cache_root = (
                home / ".claude" / "plugins" / "cache" / "runlayer" / "box" / "1.0.0"
            )
            (cache_root / ".claude-plugin").mkdir(parents=True)
            (cache_root / ".claude-plugin" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "box",
                        "version": "1.0.0",
                        "mcpServers": {
                            "box": {
                                "url": "https://acme.runlayer.com/api/v1/proxy/xyz/mcp"
                            }
                        },
                    }
                )
            )
            installed_plugins = home / ".claude" / "plugins" / "installed_plugins.json"
            installed_plugins.write_text(
                json.dumps(
                    {
                        "version": 2,
                        "plugins": {
                            "box@runlayer": [
                                {
                                    "scope": "user",
                                    "installPath": str(cache_root),
                                    "version": "1.0.0",
                                }
                            ]
                        },
                    }
                )
            )
            settings = home / ".claude" / "settings.json"
            settings.write_text(json.dumps({"enabledPlugins": {"box@runlayer": False}}))

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server("plugin_box_box", str(project))

            assert result is None

    def test_plugin_registered_for_other_project_resolves_via_filesystem(self):
        """ENG-3439: a plugin registered only for a *different* project must
        still resolve from disk in the current cwd. A same-named registry entry
        for another project must not suppress the filesystem fallback (only an
        explicit disable does)."""
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            other_project = Path(td) / "other-project"
            this_project = Path(td) / "this-project"
            other_project.mkdir(parents=True)
            this_project.mkdir(parents=True)

            # box is on disk (top-level / symlinked install)...
            plugin_root = home / ".claude" / "plugins" / "box"
            (plugin_root / ".claude-plugin").mkdir(parents=True)
            (plugin_root / ".claude-plugin" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "box",
                        "version": "1.0.0",
                        "mcpServers": {
                            "box": {
                                "url": "https://acme.runlayer.com/api/v1/proxy/abc/mcp"
                            }
                        },
                    }
                )
            )
            # ...but registered only for a *different* project.
            installed_plugins = home / ".claude" / "plugins" / "installed_plugins.json"
            installed_plugins.write_text(
                json.dumps(
                    {
                        "version": 2,
                        "plugins": {
                            "box@runlayer": [
                                {
                                    "scope": "project",
                                    "installPath": str(plugin_root),
                                    "projectPath": str(other_project),
                                    "version": "1.0.0",
                                }
                            ]
                        },
                    }
                )
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server("plugin_box_box", str(this_project))

            assert result is not None
            assert result["url"] == "https://acme.runlayer.com/api/v1/proxy/abc/mcp"

    def test_project_reenable_overrides_global_disable_in_fallback(self):
        """ENG-3439: a project-level re-enable overrides a global disable, so the
        filesystem fallback still resolves the on-disk plugin (last-file-wins,
        consistent with the bash hook)."""
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            project = Path(td) / "project"
            (project / ".claude").mkdir(parents=True)

            plugin_root = home / ".claude" / "plugins" / "box"
            (plugin_root / ".claude-plugin").mkdir(parents=True)
            (plugin_root / ".claude-plugin" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "box",
                        "version": "1.0.0",
                        "mcpServers": {
                            "box": {
                                "url": "https://acme.runlayer.com/api/v1/proxy/abc/mcp"
                            }
                        },
                    }
                )
            )
            (home / ".claude" / "settings.json").write_text(
                json.dumps({"enabledPlugins": {"box@runlayer": False}})
            )
            (project / ".claude" / "settings.json").write_text(
                json.dumps({"enabledPlugins": {"box@runlayer": True}})
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server("plugin_box_box", str(project))

            assert result is not None
            assert result["url"] == "https://acme.runlayer.com/api/v1/proxy/abc/mcp"


def _make_linked_worktree(
    main: Path, worktree: Path, *, relative_gitdir: bool = False
) -> None:
    """Lay out a ``git worktree add``-shaped link on disk without running git."""
    admin = main / ".git" / "worktrees" / worktree.name
    admin.mkdir(parents=True)
    (admin / "commondir").write_text("../..\n")
    (admin / "gitdir").write_text(f"{worktree / '.git'}\n")
    worktree.mkdir(parents=True, exist_ok=True)
    pointer = os.path.relpath(admin, worktree) if relative_gitdir else str(admin)
    (worktree / ".git").write_text(f"gitdir: {pointer}\n")


def _write_claude_json_projects(home: Path, projects: dict[str, str]) -> None:
    """Write ``~/.claude.json`` with a ``myserver`` entry per project root."""
    home.mkdir(parents=True, exist_ok=True)
    (home / ".claude.json").write_text(
        json.dumps(
            {
                "projects": {
                    root: {"mcpServers": {"myserver": {"url": url}}}
                    for root, url in projects.items()
                }
            }
        )
    )


class TestMCPLookupWorktree:
    """Sessions in git worktrees must resolve servers registered for the main
    checkout. ``projects`` in ``~/.claude.json`` is keyed by the main checkout
    path while the hook payload cwd is the worktree path, so an exact-cwd-only
    lookup fail-closes ("not registered ... cannot be verified") on servers the
    client itself loaded fine."""

    def test_external_worktree_resolves_main_checkout_project_servers(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            main = Path(td) / "workspace" / "Runlayer"
            worktree = Path(td) / "worktrees" / "Runlayer" / "feature-x"
            _make_linked_worktree(main, worktree)
            _write_claude_json_projects(home, {str(main): "https://main.example.com"})

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server("myserver", str(worktree))

            assert result is not None, (
                "server registered for the main checkout must resolve from a "
                "linked worktree cwd -> None fail-closes and blocks the call"
            )
            assert result["url"] == "https://main.example.com"

    def test_in_repo_worktree_resolves_main_checkout_project_servers(self):
        # Claude Code's own worktree layout: <repo>/.claude/worktrees/<name>
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            main = Path(td) / "Runlayer"
            worktree = main / ".claude" / "worktrees" / "jovial-hopper"
            _make_linked_worktree(main, worktree)
            _write_claude_json_projects(home, {str(main): "https://main.example.com"})

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server("myserver", str(worktree))

            assert result is not None
            assert result["url"] == "https://main.example.com"

    def test_worktree_subdir_cwd_resolves_main_checkout_project_servers(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            main = Path(td) / "Runlayer"
            worktree = Path(td) / "wt"
            _make_linked_worktree(main, worktree)
            subdir = worktree / "backend" / "app"
            subdir.mkdir(parents=True)
            _write_claude_json_projects(home, {str(main): "https://main.example.com"})

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server("myserver", str(subdir))

            assert result is not None
            assert result["url"] == "https://main.example.com"

    def test_subdir_cwd_resolves_repo_root_project_servers(self):
        # Plain repo (.git directory), cwd below the registered root.
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            main = Path(td) / "Runlayer"
            (main / ".git").mkdir(parents=True)
            subdir = main / "backend" / "app"
            subdir.mkdir(parents=True)
            _write_claude_json_projects(home, {str(main): "https://main.example.com"})

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server("myserver", str(subdir))

            assert result is not None
            assert result["url"] == "https://main.example.com"

    def test_relative_gitdir_pointer_resolves_main_checkout(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            main = Path(td) / "Runlayer"
            worktree = main / ".claude" / "worktrees" / "wt"
            _make_linked_worktree(main, worktree, relative_gitdir=True)
            _write_claude_json_projects(home, {str(main): "https://main.example.com"})

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server("myserver", str(worktree))

            assert result is not None
            assert result["url"] == "https://main.example.com"

    def test_worktree_resolves_main_checkout_mcp_json(self):
        # .mcp.json only present at the main checkout root (e.g. gitignored).
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            main = Path(td) / "Runlayer"
            worktree = Path(td) / "wt"
            _make_linked_worktree(main, worktree)
            (main / ".mcp.json").write_text(
                json.dumps(
                    {"mcpServers": {"myserver": {"url": "https://mcpjson.example.com"}}}
                )
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server("myserver", str(worktree))

            assert result is not None
            assert result["url"] == "https://mcpjson.example.com"

    def test_exact_cwd_registration_beats_main_checkout_registration(self):
        # Regression guard: widening candidates must not reorder precedence.
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            main = Path(td) / "Runlayer"
            worktree = Path(td) / "wt"
            _make_linked_worktree(main, worktree)
            _write_claude_json_projects(
                home,
                {
                    str(worktree): "https://worktree.example.com",
                    str(main): "https://main.example.com",
                },
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server("myserver", str(worktree))

            assert result is not None
            assert result["url"] == "https://worktree.example.com"

    def test_garbage_git_file_is_ignored(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            for name, content in (
                ("junk", "not a gitdir pointer\n"),
                (
                    "dangling",
                    f"gitdir: {Path(td) / 'nope' / '.git' / 'worktrees' / 'x'}\n",
                ),
                ("empty", ""),
            ):
                cwd = Path(td) / name
                cwd.mkdir()
                (cwd / ".git").write_text(content)
                with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                    assert lookup_mcp_server("myserver", str(cwd)) is None

    def test_plugin_project_scoped_installation_applies_in_external_worktree(self):
        # Registry entry scoped to the main checkout (installPath outside
        # ~/.claude/plugins, so the filesystem fallback can't rescue it).
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / "home"
            main = Path(td) / "Runlayer"
            worktree = Path(td) / "wt"
            _make_linked_worktree(main, worktree)

            plugin_root = Path(td) / "devplugin"
            (plugin_root / ".claude-plugin").mkdir(parents=True)
            (plugin_root / ".claude-plugin" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "box",
                        "version": "1.0.0",
                        "mcpServers": {
                            "box": {
                                "url": "https://acme.runlayer.com/api/v1/proxy/abc/mcp"
                            }
                        },
                    }
                )
            )
            plugins_dir = home / ".claude" / "plugins"
            plugins_dir.mkdir(parents=True)
            (plugins_dir / "installed_plugins.json").write_text(
                json.dumps(
                    {
                        "version": 2,
                        "plugins": {
                            "box@runlayer": [
                                {
                                    "scope": "project",
                                    "projectPath": str(main),
                                    "installPath": str(plugin_root),
                                    "version": "1.0.0",
                                }
                            ]
                        },
                    }
                )
            )

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_mcp_server("plugin_box_box", str(worktree))

            assert result is not None, (
                "project-scoped plugin for the main checkout must apply in its "
                "worktree cwd"
            )
            assert result["url"] == "https://acme.runlayer.com/api/v1/proxy/abc/mcp"


class TestWindsurfMCPLookup:
    """Cascade reads ``mcpServers`` from the Codeium profile dir + workspace."""

    def test_finds_url_in_codeium_profile_config(self):
        with tempfile.TemporaryDirectory() as td:
            profile = Path(td) / ".codeium" / "windsurf" / "mcp_config.json"
            profile.parent.mkdir(parents=True)
            profile.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "linear-44": {"url": "https://mcp.example.com/sse"}
                        }
                    }
                )
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_windsurf_mcp_server("linear-44", "/nonexistent")

            assert result is not None
            assert result["url"] == "https://mcp.example.com/sse"

    def test_finds_server_url_key_in_profile_config(self):
        """Windsurf writes remote servers as ``serverUrl``, not ``url``."""
        with tempfile.TemporaryDirectory() as td:
            profile = Path(td) / ".codeium" / "windsurf" / "mcp_config.json"
            profile.parent.mkdir(parents=True)
            profile.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "linear-44": {"serverUrl": "https://mcp.example.com/sse"}
                        }
                    }
                )
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_windsurf_mcp_server("linear-44", "")

            assert result is not None
            assert result["url"] == "https://mcp.example.com/sse"

    def test_finds_command_in_workspace_config(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = Path(td) / "repo"
            config = workspace / ".windsurf" / "mcp_config.json"
            config.parent.mkdir(parents=True)
            config.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "myserver": {"command": "npx", "args": ["-y", "my-mcp"]}
                        }
                    }
                )
            )
            home = Path(td) / "home"
            home.mkdir()
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
                result = lookup_windsurf_mcp_server("myserver", str(workspace))

            assert result is not None
            assert result["command"] == "npx -y my-mcp"

    def test_workspace_config_takes_precedence_over_profile(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = Path(td) / "repo"
            workspace_config = workspace / ".windsurf" / "mcp_config.json"
            workspace_config.parent.mkdir(parents=True)
            workspace_config.write_text(
                json.dumps(
                    {"mcpServers": {"myserver": {"url": "https://workspace.example"}}}
                )
            )
            profile = Path(td) / ".codeium" / "windsurf" / "mcp_config.json"
            profile.parent.mkdir(parents=True)
            profile.write_text(
                json.dumps(
                    {"mcpServers": {"myserver": {"url": "https://profile.example"}}}
                )
            )
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = lookup_windsurf_mcp_server("myserver", str(workspace))

            assert result is not None
            assert result["url"] == "https://workspace.example"

    def test_returns_none_when_server_absent(self):
        with tempfile.TemporaryDirectory() as td:
            profile = Path(td) / ".codeium" / "windsurf" / "mcp_config.json"
            profile.parent.mkdir(parents=True)
            profile.write_text(json.dumps({"mcpServers": {}}))
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                assert lookup_windsurf_mcp_server("unknown", str(Path(td))) is None

    def test_returns_none_when_no_config_exists(self):
        with tempfile.TemporaryDirectory() as td:
            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                assert lookup_windsurf_mcp_server("linear-44", str(Path(td))) is None


# =========================================================================
# clients tests
# =========================================================================


class TestClientDetection:
    @pytest.mark.parametrize(
        ("client_name", "expected"),
        [
            ("cursor", Client.CURSOR),
            ("vscode", Client.VSCODE),
            ("claude_code", Client.CLAUDE_CODE),
            ("codex", Client.CODEX),
            ("hermes", Client.HERMES),
            ("goose", Client.GOOSE),
            ("github-copilot-cli", Client.GITHUB_COPILOT_CLI),
            ("windsurf", Client.WINDSURF),
            ("qwen-code", Client.QWEN_CODE),
            ("gemini-cli", Client.GEMINI_CLI),
            ("grok-cli", Client.GROK_CLI),
            ("cline-cli", Client.CLINE_CLI),
        ],
    )
    def test_detect_client_from_explicit_arg(self, client_name, expected):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch(
                "sys.argv",
                [
                    "/usr/local/lib/runlayer/aiwatch/aiwatch-hook",
                    "--client",
                    client_name,
                ],
            ):
                assert detect_client() == expected

    def test_detect_cursor(self):
        with patch.dict(os.environ, {"CURSOR_VERSION": "1.0.0"}):
            assert detect_client() == Client.CURSOR

    def test_detect_cursor_from_enterprise_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch(
                "sys.argv",
                ["/Library/Application Support/Cursor/hooks/aiwatch-hook"],
            ):
                assert detect_client() == Client.CURSOR

    def test_detect_vscode_from_copilot_hook_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", ["/home/user/.copilot/hooks/aiwatch-hook"]):
                assert detect_client() == Client.VSCODE

    def test_detect_claude_code_fallback(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", ["/home/user/hooks/aiwatch-enforce"]):
                assert detect_client() == Client.CLAUDE_CODE

    def test_detect_codex_from_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", ["/home/user/.codex/hooks/aiwatch-enforce"]):
                assert detect_client() == Client.CODEX

    def test_detect_codex_from_enterprise_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", ["/etc/codex/hooks/aiwatch-hook"]):
                assert detect_client() == Client.CODEX

    def test_detect_hermes_from_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch(
                "sys.argv",
                ["/home/user/.hermes/agent-hooks/aiwatch-enforce"],
            ):
                assert detect_client() == Client.HERMES

    def test_detect_windsurf_from_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch(
                "sys.argv",
                ["/home/user/.codeium/windsurf/hooks/aiwatch-hook"],
            ):
                assert detect_client() == Client.WINDSURF

    def test_detect_windsurf_from_enterprise_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch(
                "sys.argv",
                ["/Library/Application Support/Windsurf/hooks/aiwatch-hook"],
            ):
                assert detect_client() == Client.WINDSURF

    def test_detect_goose_from_plugin_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch(
                "sys.argv",
                ["/home/user/.agents/plugins/runlayer-hooks/scripts/aiwatch-enforce"],
            ):
                assert detect_client() == Client.GOOSE

    def test_detect_github_copilot_cli_from_policy_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", ["/etc/github-copilot/policy.d/aiwatch-hook"]):
                assert detect_client() == Client.GITHUB_COPILOT_CLI

    def test_detect_github_copilot_cli_from_user_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", ["/home/user/.copilot/aiwatch-hook"]):
                assert detect_client() == Client.GITHUB_COPILOT_CLI

    def test_detect_github_copilot_cli_from_copilot_home(self):
        env = {
            k: v
            for k, v in os.environ.items()
            if k not in ("CURSOR_VERSION", "COPILOT_HOME")
        }
        env["COPILOT_HOME"] = "/opt/custom-copilot"
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", ["/opt/custom-copilot/bin/aiwatch-hook"]):
                assert detect_client() == Client.GITHUB_COPILOT_CLI

    def test_detect_cline_cli_from_user_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", ["/home/user/.cline/hooks/PreToolUse"]):
                assert detect_client() == Client.CLINE_CLI

    def test_detect_cline_cli_from_cline_dir(self):
        env = {
            k: v
            for k, v in os.environ.items()
            if k not in ("CURSOR_VERSION", "CLINE_DIR")
        }
        env["CLINE_DIR"] = "/opt/custom-cline"
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", ["/opt/custom-cline/hooks/PreToolUse"]):
                assert detect_client() == Client.CLINE_CLI

    def test_detect_qwen_code_from_user_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", ["/home/user/.qwen/aiwatch-hook"]):
                assert detect_client() == Client.QWEN_CODE

    @pytest.mark.parametrize(
        "system_path",
        [
            "/etc/qwen-code/aiwatch-hook",
            "/Library/Application Support/QwenCode/aiwatch-hook",
            "C:/ProgramData/qwen-code/aiwatch-hook",
        ],
    )
    def test_detect_qwen_code_from_system_paths(self, system_path):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", [system_path]):
                assert detect_client() == Client.QWEN_CODE

    def test_detect_qwen_code_from_qwen_home(self):
        env = {
            k: v
            for k, v in os.environ.items()
            if k not in ("CURSOR_VERSION", "QWEN_HOME")
        }
        env["QWEN_HOME"] = "/opt/custom-qwen"
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", ["/opt/custom-qwen/bin/aiwatch-hook"]):
                assert detect_client() == Client.QWEN_CODE

    def test_detect_gemini_cli_from_user_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", ["/home/user/.gemini/aiwatch-hook"]):
                assert detect_client() == Client.GEMINI_CLI

    def test_detect_gemini_cli_from_linux_system_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", ["/etc/gemini-cli/aiwatch-hook"]):
                assert detect_client() == Client.GEMINI_CLI

    def test_detect_gemini_cli_from_macos_system_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch(
                "sys.argv",
                ["/Library/Application Support/GeminiCli/aiwatch-hook"],
            ):
                assert detect_client() == Client.GEMINI_CLI

    def test_detect_gemini_cli_from_windows_programdata_path(self):
        """Backslash paths must normalize so Gemini doesn't fall through to Claude."""
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch(
                "runlayer_cli.hook.clients.Path",
                _windows_path_mock("C:\\ProgramData\\gemini-cli"),
            ):
                assert detect_client() == Client.GEMINI_CLI

    def test_detect_codex_from_windows_path(self):
        """Regression: Path.resolve() on Windows yields backslash paths.

        The detection patterns must normalize separators so '/.codex/' matches
        'c:\\users\\user\\.codex\\hooks' and Codex doesn't fall through to
        CLAUDE_CODE response shaping.
        """
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch(
                "runlayer_cli.hook.clients.Path",
                _windows_path_mock("C:\\Users\\user\\.codex\\hooks"),
            ):
                assert detect_client() == Client.CODEX

    @pytest.mark.skipif(sys.platform == "win32", reason="POSIX symlink semantics")
    def test_detect_codex_when_invoked_via_symlink_to_shared_binary(
        self, tmp_path: Path
    ) -> None:
        """Regression: MDM ships one shared binary at /usr/local/lib/runlayer/...
        and clients invoke it via a symlink in their own hooks dir.

        Path.resolve() follows symlinks, hiding the .codex/ path component and
        misidentifying Codex as Claude Code (wrong deny response shape).
        Detection must use the invoked path, not the symlink target.
        """
        real_dir = tmp_path / "lib" / "runlayer" / "aiwatch-enforce"
        real_dir.mkdir(parents=True)
        real_bin = real_dir / "aiwatch-enforce"
        real_bin.write_text("")
        codex_hooks = tmp_path / ".codex" / "hooks"
        codex_hooks.mkdir(parents=True)
        symlink = codex_hooks / "aiwatch-enforce"
        symlink.symlink_to(real_bin)

        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", [str(symlink)]):
                assert detect_client() == Client.CODEX


class TestShouldNoopForCursor:
    def test_cursor_cli_explicit_client_does_not_require_cursor_version(self):
        env = {
            key: value for key, value in os.environ.items() if key != "CURSOR_VERSION"
        }
        with (
            patch.dict(os.environ, env, clear=True),
            patch(
                "sys.argv",
                [
                    "/usr/local/lib/runlayer/aiwatch/aiwatch-hook",
                    "--client",
                    "cursor",
                ],
            ),
        ):
            assert detect_client() == Client.CURSOR
            assert should_noop_for_cursor(Client.CURSOR) is False

    def test_noop_when_cursor_loads_explicit_non_cursor_hook(self):
        with patch.dict(os.environ, {"CURSOR_VERSION": "1.0.0"}):
            with patch(
                "sys.argv",
                ["/home/user/.claude/hooks/aiwatch-hook", "--client", "claude_code"],
            ):
                assert should_noop_for_cursor(Client.CLAUDE_CODE) is True

    def test_noop_when_cursor_loads_claude_hook(self):
        with patch("sys.argv", ["/home/user/.claude/hooks/aiwatch-enforce"]):
            assert should_noop_for_cursor(Client.CURSOR) is True

    def test_no_noop_when_cursor_loads_cursor_hook(self):
        with patch("sys.argv", ["/home/user/.cursor/hooks/aiwatch-enforce"]):
            assert should_noop_for_cursor(Client.CURSOR) is False

    def test_no_noop_for_claude_code(self):
        assert should_noop_for_cursor(Client.CLAUDE_CODE) is False

    def test_no_noop_when_cursor_hook_path_uses_windows_backslashes(self):
        """Regression: Path.resolve() on Windows yields backslash paths.

        Without backslash normalization the noop guard always fires on Windows,
        silently disabling Cursor enforcement (hook returns 'allow' for everything).
        """
        with patch(
            "runlayer_cli.hook.clients.Path",
            _windows_path_mock("C:\\Users\\user\\.cursor\\hooks"),
        ):
            assert should_noop_for_cursor(Client.CURSOR) is False

    def test_no_noop_when_cursor_hook_in_programdata_with_backslashes(self):
        with patch(
            "runlayer_cli.hook.clients.Path",
            _windows_path_mock("C:\\ProgramData\\Cursor\\hooks"),
        ):
            assert should_noop_for_cursor(Client.CURSOR) is False

    def test_noop_when_cursor_loads_claude_hook_on_windows(self):
        with patch(
            "runlayer_cli.hook.clients.Path",
            _windows_path_mock("C:\\Users\\user\\.claude\\hooks"),
        ):
            assert should_noop_for_cursor(Client.CURSOR) is True

    @pytest.mark.skipif(sys.platform == "win32", reason="POSIX symlink semantics")
    def test_no_noop_when_cursor_invokes_via_symlink_to_shared_binary(
        self, tmp_path: Path
    ) -> None:
        """Regression: MDM-installed binary lives at /usr/local/lib/runlayer/...
        and Cursor invokes it via a symlink inside ~/.cursor/hooks/.

        Path.resolve() follows the symlink, returning a parent that doesn't
        contain '/.cursor/'. The noop guard then fires for Cursor, silently
        returning 'allow' for every event and disabling all enforcement.
        Match bash `dirname "$0"`: do not follow symlinks.
        """
        real_dir = tmp_path / "lib" / "runlayer" / "aiwatch-enforce"
        real_dir.mkdir(parents=True)
        real_bin = real_dir / "aiwatch-enforce"
        real_bin.write_text("")
        cursor_hooks = tmp_path / ".cursor" / "hooks"
        cursor_hooks.mkdir(parents=True)
        symlink = cursor_hooks / "aiwatch-enforce"
        symlink.symlink_to(real_bin)

        with patch("sys.argv", [str(symlink)]):
            assert should_noop_for_cursor(Client.CURSOR) is False

    def test_no_noop_when_frozen_binary_in_non_cursor_dir(self):
        """Regression: frozen aiwatch-hook is a single shared exe wired into
        every client's config. Its parent dir (/usr/local/lib/runlayer/aiwatch)
        matches no Cursor-config pattern, so the path-based guard would fire
        and silently no-op every Cursor event. Frozen path must trust MDM wiring.
        """
        with patch.object(sys, "frozen", True, create=True):
            with patch("sys.argv", ["/usr/local/lib/runlayer/aiwatch/aiwatch-hook"]):
                assert should_noop_for_cursor(Client.CURSOR) is False

    def test_no_noop_when_frozen_binary_under_claude_config(self):
        """Documents intentional shared-binary semantics: the frozen binary
        runs for Cursor regardless of which client's config dir Cursor loaded
        it from, because argv[0] can't distinguish them in a shared-exe install.
        """
        with patch.object(sys, "frozen", True, create=True):
            with patch("sys.argv", ["/home/user/.claude/hooks/aiwatch-hook"]):
                assert should_noop_for_cursor(Client.CURSOR) is False


class TestHookResponse:
    def test_cursor_deny(self):
        r = HookResponse(Client.CURSOR, "PreToolUse")
        output = json.loads(r.deny("blocked", "agent reason"))
        assert output["permission"] == "deny"
        assert output["continue"] is True
        assert output["user_message"] == "blocked"
        assert output["agentMessage"] == "agent reason"

    def test_cursor_allow(self):
        r = HookResponse(Client.CURSOR, "PreToolUse")
        assert json.loads(r.allow()) == {"permission": "allow"}

    def test_claude_code_deny(self):
        r = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        output = json.loads(r.deny("blocked", "agent reason"))
        hso = output["hookSpecificOutput"]
        assert hso["hookEventName"] == "PreToolUse"
        assert hso["permissionDecision"] == "deny"
        assert hso["permissionDecisionReason"] == "agent reason"

    def test_claude_code_allow_is_none(self):
        r = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        assert r.allow() is None

    def test_goose_deny_uses_block_shape(self):
        r = HookResponse(Client.GOOSE, "PreToolUse")
        output = json.loads(r.deny("blocked", "agent reason"))
        assert output == {"decision": "block", "reason": "agent reason"}
        assert r.allow() is None

    def test_vscode_deny_uses_hook_specific_output(self):
        r = HookResponse(Client.VSCODE, "PreToolUse")
        output = json.loads(r.deny("blocked", "agent reason"))
        hso = output["hookSpecificOutput"]
        assert hso["hookEventName"] == "PreToolUse"
        assert hso["permissionDecision"] == "deny"
        assert hso["permissionDecisionReason"] == "agent reason"

    def test_vscode_allow_is_none(self):
        r = HookResponse(Client.VSCODE, "PreToolUse")
        assert r.allow() is None

    def test_vscode_allow_with_updated_input(self):
        r = HookResponse(Client.VSCODE, "PreToolUse")
        output = json.loads(r.allow_with_updated_input({"command": "echo redacted"}))
        hso = output["hookSpecificOutput"]
        assert hso["hookEventName"] == "PreToolUse"
        assert hso["permissionDecision"] == "allow"
        assert hso["updatedInput"] == {"command": "echo redacted"}

    def test_cline_cli_deny_uses_prefixed_control_line(self):
        # Cline scans stdout for HOOK_CONTROL-prefixed lines; without the prefix
        # it requires the ENTIRE stdout to be valid JSON, so any stray logging
        # would corrupt the decision. Always emit the prefix.
        r = HookResponse(Client.CLINE_CLI, "PreToolUse")
        output = r.deny("blocked", "agent reason")
        assert output.startswith("HOOK_CONTROL\t")
        assert json.loads(output.split("\t", 1)[1]) == {
            "cancel": True,
            "errorMessage": "agent reason",
        }

    def test_cline_cli_allow_emits_empty_control_object(self):
        r = HookResponse(Client.CLINE_CLI, "PreToolUse")
        output = r.allow()
        assert output is not None
        assert output.startswith("HOOK_CONTROL\t")
        assert json.loads(output.split("\t", 1)[1]) == {}

    def test_cline_cli_allow_with_updated_input_uses_override_input(self):
        r = HookResponse(Client.CLINE_CLI, "PreToolUse")
        output = r.allow_with_updated_input({"command": "echo redacted"})
        assert output is not None
        assert json.loads(output.split("\t", 1)[1]) == {
            "overrideInput": {"command": "echo redacted"}
        }

    def test_cline_cli_has_no_post_output_rewrite_path(self):
        # Non-PreToolUse hooks are spawned detached with stdout discarded, so the
        # capability row reports post-tool block/rewrite as unsupported.
        r = HookResponse(Client.CLINE_CLI, "PostToolUse")
        assert r.mask_output("SSN [REDACTED]") is None

    def test_qwen_code_pretooluse_deny_uses_claude_hook_specific_output(self):
        # Qwen requires BOTH permissionDecision and permissionDecisionReason.
        # It reuses the Claude-shaped default branch, which is also what every
        # internal error path emits — so a dispatch failure still produces a
        # valid Qwen deny rather than a malformed payload Qwen would ignore.
        r = HookResponse(Client.QWEN_CODE, "PreToolUse")
        output = json.loads(r.deny("blocked", "agent reason"))
        assert output == {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "agent reason",
            }
        }

    def test_qwen_code_cannot_apply_updated_input(self):
        r = HookResponse(Client.QWEN_CODE, "PreToolUse")
        assert r.allow_with_updated_input({"command": "echo redacted"}) is None

    def test_qwen_code_post_tool_block_stops_execution(self):
        r = HookResponse(Client.QWEN_CODE, "PostToolUse")
        output = json.loads(r.block_output("secret in output"))
        assert output == {"continue": False, "reason": "secret in output"}

    def test_qwen_code_has_no_post_output_rewrite_path(self):
        # Capability row reports output_rewrite_hide_support as unsupported;
        # assert the adapter really has no rewrite shape so the row stays honest.
        r = HookResponse(Client.QWEN_CODE, "PostToolUse")
        assert r.mask_output("SSN [REDACTED]") is None

    def test_github_copilot_cli_pretooluse_deny_uses_direct_fields(self):
        r = HookResponse(Client.GITHUB_COPILOT_CLI, "PreToolUse")
        output = json.loads(r.deny("blocked", "agent reason"))
        assert output == {
            "permissionDecision": "deny",
            "permissionDecisionReason": "agent reason",
        }

    def test_github_copilot_cli_permission_request_deny_uses_direct_fields(self):
        r = HookResponse(Client.GITHUB_COPILOT_CLI, "PermissionRequest")
        output = json.loads(r.deny("blocked", "agent reason"))
        assert output == {"behavior": "deny", "message": "blocked"}

    def test_github_copilot_cli_allow_with_updated_input_uses_modified_args(self):
        r = HookResponse(Client.GITHUB_COPILOT_CLI, "PreToolUse")
        output = json.loads(r.allow_with_updated_input({"command": "echo redacted"}))
        assert output == {
            "permissionDecision": "allow",
            "modifiedArgs": {"command": "echo redacted"},
        }

    def test_github_copilot_cli_mask_output_uses_modified_result(self):
        r = HookResponse(Client.GITHUB_COPILOT_CLI, "PostToolUse")
        output = json.loads(r.mask_output("SSN [REDACTED]"))
        assert output["modifiedResult"]["textResultForLlm"] == "SSN [REDACTED]"

    def test_github_copilot_cli_failed_tool_block_uses_additional_context(self):
        r = HookResponse(Client.GITHUB_COPILOT_CLI, "PostToolUseFailure")
        output = json.loads(r.block_output("secret in error output"))
        assert "modifiedResult" not in output
        assert "cannot suppress the original error" in output["additionalContext"]
        assert "secret in error output" in output["additionalContext"]

    def test_github_copilot_cli_failed_tool_cannot_claim_masking(self):
        r = HookResponse(Client.GITHUB_COPILOT_CLI, "PostToolUseFailure")
        assert r.mask_output("SSN [REDACTED]") is None

    def test_gemini_cli_deny_uses_decision_reason_and_system_message(self):
        r = HookResponse(Client.GEMINI_CLI, "PreToolUse")
        output = json.loads(r.deny("blocked", "agent reason"))
        assert output == {
            "decision": "deny",
            "reason": "agent reason",
            "systemMessage": "blocked",
        }

    def test_gemini_cli_deny_shape_is_event_independent(self):
        """Gemini reads the same top-level decision/reason pair on every event."""
        r = HookResponse(Client.GEMINI_CLI, "Stop")
        output = json.loads(r.deny("blocked", "agent reason"))
        assert output["decision"] == "deny"
        assert output["systemMessage"] == "blocked"

    def test_gemini_cli_allow_is_none(self):
        r = HookResponse(Client.GEMINI_CLI, "PreToolUse")
        assert r.allow() is None

    def test_gemini_cli_allow_with_updated_input_uses_gemini_event_name(self):
        r = HookResponse(Client.GEMINI_CLI, "PreToolUse")
        output = json.loads(r.allow_with_updated_input({"command": "echo redacted"}))
        # The discriminator carries Gemini's own event name, not the normalized one.
        assert output == {
            "hookSpecificOutput": {
                "hookEventName": "BeforeTool",
                "tool_input": {"command": "echo redacted"},
            }
        }

    def test_gemini_cli_allow_with_updated_input_only_on_pre_tool_use(self):
        r = HookResponse(Client.GEMINI_CLI, "PostToolUse")
        assert r.allow_with_updated_input({"command": "echo redacted"}) is None

    def test_gemini_cli_mask_output_is_none(self):
        """Gemini has no non-blocking output-rewrite channel, so masking is a no-op."""
        r = HookResponse(Client.GEMINI_CLI, "PostToolUse")
        assert r.mask_output("SSN [REDACTED]") is None

    def test_gemini_cli_block_output_falls_through_to_generic_block(self):
        r = HookResponse(Client.GEMINI_CLI, "PostToolUse")
        output = json.loads(r.block_output("secret in tool output"))
        assert output["decision"] == "block"
        assert "secret in tool output" in output["reason"]

    def test_grok_cli_pre_tool_deny_uses_native_top_level_shape(self):
        response = HookResponse(Client.GROK_CLI, "PreToolUse")

        assert json.loads(response.deny("blocked", "agent reason")) == {
            "decision": "deny",
            "reason": "agent reason",
        }

    def test_grok_cli_has_no_rewrite_or_post_block_channel(self):
        response = HookResponse(Client.GROK_CLI, "PostToolUse")

        assert response.allow_with_updated_input({"command": "redacted"}) is None
        assert response.mask_output("redacted") is None
        assert response.observational() is None


def test_adapt_grok_payload_normalizes_native_camel_case_fields():
    assert hook_dispatch._adapt_grok_payload(
        {
            "hookEventName": "pre_tool_use",
            "sessionId": "session-1",
            "workspaceRoot": "/repo",
            "toolName": "run_terminal_cmd",
            "toolInput": {"command": "echo ok"},
            "toolUseId": "tool-1",
        }
    ) == {
        "hookEventName": "pre_tool_use",
        "sessionId": "session-1",
        "workspaceRoot": "/repo",
        "toolName": "run_terminal_cmd",
        "toolInput": {"command": "echo ok"},
        "toolUseId": "tool-1",
        "hook_event_name": "pre_tool_use",
        "session_id": "session-1",
        "workspace_root": "/repo",
        "cwd": "/repo",
        "tool_name": "run_terminal_cmd",
        "tool_input": {"command": "echo ok"},
        "tool_use_id": "tool-1",
    }


def test_lookup_grok_cli_mcp_server_reads_native_toml(tmp_path, monkeypatch):
    grok_home = tmp_path / ".grok"
    grok_home.mkdir()
    (grok_home / "config.toml").write_text(
        '[mcp_servers.linear]\nurl = "https://mcp.example.com/sse"\n'
    )
    monkeypatch.setenv("GROK_HOME", str(grok_home))

    server = lookup_grok_cli_mcp_server("linear", str(tmp_path))

    assert server == {"url": "https://mcp.example.com/sse"}


class TestGeminiCLIEventNormalization:
    """Gemini renames every lifecycle event; the runtime maps them to the
    canonical Claude-shaped names the dispatcher switches on."""

    @pytest.mark.parametrize(
        ("gemini_event", "normalized"),
        [
            ("BeforeTool", "PreToolUse"),
            ("AfterTool", "PostToolUse"),
            ("BeforeAgent", "UserPromptSubmit"),
            ("AfterAgent", "Stop"),
            ("PreCompress", "PreCompact"),
        ],
    )
    def test_event_normalize_maps_gemini_event(self, gemini_event, normalized):
        assert EVENT_NORMALIZE[gemini_event] == normalized

    def test_shared_event_names_are_not_remapped(self):
        """``SessionStart``/``SessionEnd``/``Notification`` are already canonical."""
        for event in ("SessionStart", "SessionEnd", "Notification"):
            assert EVENT_NORMALIZE.get(event, event) == event

    def test_codex_pretooluse_deny_uses_hook_specific_output(self):
        """Regression: Codex PreToolUse must emit the documented
        ``hookSpecificOutput`` shape, matching the bash hook (runlayer-hook.sh
        lines 100-107). Falling through to ``{decision: block, reason: ...}``
        is silently misinterpreted by Codex and may allow blocked actions.
        """
        r = HookResponse(Client.CODEX, "PreToolUse")
        output = json.loads(r.deny("blocked"))
        hso = output["hookSpecificOutput"]
        assert hso["hookEventName"] == "PreToolUse"
        assert hso["permissionDecision"] == "deny"
        assert hso["permissionDecisionReason"] == "blocked"

    def test_codex_pretooluse_camelcase_deny_uses_hook_specific_output(self):
        """Cursor-style ``preToolUse`` casing must produce the same shape — the
        bash hook accepts both spellings."""
        r = HookResponse(Client.CODEX, "preToolUse")
        output = json.loads(r.deny("blocked"))
        hso = output["hookSpecificOutput"]
        assert hso["hookEventName"] == "PreToolUse"
        assert hso["permissionDecision"] == "deny"

    def test_codex_other_event_deny_uses_block_shape(self):
        r = HookResponse(Client.CODEX, "SessionEnd")
        output = json.loads(r.deny("blocked"))
        assert output == {"decision": "block", "reason": "blocked"}

    def test_claude_code_camelcase_event_normalized_to_pascal(self):
        """Regression: Claude Code expects PascalCase ``hookEventName`` in the
        deny response. If HookResponse is ever constructed with a Cursor-style
        camelCase event (e.g. via the pre-normalization dispatch path), the
        emitted response must still carry PascalCase — not silently echo back
        the raw input.
        """
        r = HookResponse(Client.CLAUDE_CODE, "preToolUse")
        output = json.loads(r.deny("blocked", "agent reason"))
        assert output["hookSpecificOutput"]["hookEventName"] == "PreToolUse"

    def test_claude_code_camelcase_post_tool_use_normalized(self):
        r = HookResponse(Client.CLAUDE_CODE, "postToolUseFailure")
        output = json.loads(r.deny("blocked", "agent reason"))
        assert output["hookSpecificOutput"]["hookEventName"] == "PostToolUseFailure"

    def test_codex_permission_request_deny(self):
        r = HookResponse(Client.CODEX, "PermissionRequest")
        output = json.loads(r.deny("blocked"))
        assert output["hookSpecificOutput"]["decision"]["behavior"] == "deny"
        assert output["hookSpecificOutput"]["decision"]["message"] == "blocked"

    def test_hermes_deny_uses_shell_hook_block_shape(self):
        r = HookResponse(Client.HERMES, "pre_tool_call")
        output = json.loads(r.deny("blocked"))
        assert output["action"] == "block"
        assert output["message"] == "blocked"

    def test_hermes_block_output_returns_json_string_replacement(self):
        r = HookResponse(Client.HERMES, "transform_tool_result")
        assert json.loads(r.block_output("output blocked")) == "output blocked"

    def test_goose_block_output_uses_native_block_contract(self):
        r = HookResponse(Client.GOOSE, "PostToolUse")
        output = json.loads(r.block_output("output blocked"))
        assert output["decision"] == "block"
        assert output["reason"] == "output blocked"
        assert "hookSpecificOutput" not in output

    def test_goose_mask_output_has_no_replacement_schema(self):
        r = HookResponse(Client.GOOSE, "PostToolUse")
        assert r.mask_output("SSN [REDACTED]") is None

    def test_cursor_observational(self):
        r = HookResponse(Client.CURSOR, "PostToolUse")
        assert r.observational() == "{}"

    def test_claude_code_observational_is_none(self):
        r = HookResponse(Client.CLAUDE_CODE, "PostToolUse")
        assert r.observational() is None

    def test_allow_with_ids(self):
        r = HookResponse(Client.CURSOR, "PreToolUse")
        output = json.loads(r.allow_with_ids({"key": "val"}, "session-1"))
        assert output["permission"] == "allow"
        assert output["updated_input"]["key"] == "val"
        assert output["updated_input"]["_runlayer_session_id"] == "session-1"

    def test_allow_with_ids_no_session(self):
        r = HookResponse(Client.CURSOR, "PreToolUse")
        output = json.loads(r.allow_with_ids({"key": "val"}, ""))
        assert output == {"permission": "allow"}

    def test_windsurf_deny_stderr_joins_user_and_agent_message(self):
        """Cascade never parses hook stdout: the deny reason must be stderr text."""
        r = HookResponse(Client.WINDSURF, "pre_mcp_tool_use")
        assert r.deny_stderr("blocked", "agent reason") == "blocked\n\nagent reason"

    def test_windsurf_deny_stderr_falls_back_to_default_agent_msg(self):
        r = HookResponse(Client.WINDSURF, "pre_read_code")
        output = r.deny_stderr("blocked")
        assert output.startswith("blocked\n\n")
        assert "Security Violation Detected" in output

    def test_windsurf_deny_stderr_does_not_duplicate_identical_messages(self):
        r = HookResponse(Client.WINDSURF, "pre_run_command")
        assert r.deny_stderr("blocked", "blocked") == "blocked"

    def test_windsurf_allow_writes_nothing(self):
        r = HookResponse(Client.WINDSURF, "pre_read_code")
        assert r.allow() is None
        assert r.observational() is None

    @pytest.mark.parametrize(
        "client",
        [c for c in Client if c is not Client.WINDSURF],
        ids=lambda c: c.value,
    )
    def test_deny_stderr_is_none_for_stdout_deny_clients(self, client):
        """Every other client encodes the deny in stdout JSON, not stderr."""
        r = HookResponse(client, "PreToolUse")
        assert r.deny_stderr("blocked", "agent reason") is None


class TestCursorEventNormalization:
    def test_cursor_tab_file_events_normalize(self) -> None:
        assert normalize_event_name("beforeTabFileRead") == "BeforeReadFile"
        assert normalize_event_name("afterTabFileEdit") == "AfterFileEdit"


class TestWindsurfEventNormalization:
    """Every registered Cascade event must map onto a canonical event name.

    An unmapped name passes through ``normalize_event_name`` untouched and then
    misses ``_DISPATCH_TABLE`` entirely, silently degrading the hook to a no-op.
    """

    @pytest.mark.parametrize(
        ("raw_event", "expected"),
        [
            ("pre_mcp_tool_use", "PreToolUse"),
            ("post_mcp_tool_use", "PostToolUse"),
            ("pre_run_command", "BeforeShellExecution"),
            ("post_run_command", "AfterShellExecution"),
            ("pre_read_code", "BeforeReadFile"),
            ("post_write_code", "AfterFileEdit"),
            ("pre_user_prompt", "UserPromptSubmit"),
            ("post_cascade_response", "Stop"),
        ],
    )
    def test_cascade_event_normalizes(self, raw_event, expected):
        assert normalize_event_name(raw_event) == expected


class TestWindsurfPayloadAdapter:
    """Cascade nests per-event detail under ``tool_info``; the dispatcher and
    relay only read the flat Claude-shaped field names."""

    def test_execution_id_is_not_used_as_tool_use_id(self):
        """Cascade reuses one execution id across actions in an agent turn."""
        payloads = [
            {
                "agent_action_name": "pre_run_command",
                "trajectory_id": "traj-1",
                "execution_id": "exec-42",
                "tool_info": {"command_line": "ls"},
            },
            {
                "agent_action_name": "pre_read_code",
                "trajectory_id": "traj-1",
                "execution_id": "exec-42",
                "tool_info": {"file_path": "/repo/README.md"},
            },
        ]

        adapted = [adapt_windsurf_payload(payload) for payload in payloads]

        assert all("tool_use_id" not in event for event in adapted)
        assert {event["execution_id"] for event in adapted} == {"exec-42"}

    def test_missing_execution_id_yields_no_tool_use_id(self):
        adapted = adapt_windsurf_payload(
            {
                "agent_action_name": "pre_run_command",
                "trajectory_id": "traj-1",
                "tool_info": {"command_line": "ls"},
            }
        )

        assert "tool_use_id" not in adapted

    def test_cascade_response_also_populates_last_assistant_message(self):
        """The Stop normalizer reads ``last_assistant_message``, not ``response``."""
        adapted = adapt_windsurf_payload(
            {
                "agent_action_name": "post_cascade_response",
                "trajectory_id": "traj-1",
                "tool_info": {"response": "done thinking"},
            }
        )

        assert adapted["response"] == "done thinking"
        assert adapted["last_assistant_message"] == "done thinking"

    def test_mcp_tool_use_flattens_to_canonical_tool_name_and_input(self):
        adapted = adapt_windsurf_payload(
            {
                "agent_action_name": "pre_mcp_tool_use",
                "trajectory_id": "traj-1",
                "execution_id": "exec-1",
                "model_name": "SWE-1",
                "tool_info": {
                    "mcp_server_name": "linear-44",
                    "mcp_tool_name": "list_issues",
                    "mcp_tool_arguments": {"limit": 3},
                },
            }
        )

        assert adapted["hook_event_name"] == "pre_mcp_tool_use"
        assert adapted["tool_name"] == "mcp__linear-44__list_issues"
        assert adapted["mcp_server_name"] == "linear-44"
        assert adapted["tool_input"] == {"limit": 3}
        assert adapted["session_id"] == "traj-1"
        assert adapted["conversation_id"] == "traj-1"
        assert adapted["model"] == "SWE-1"
        # Native Cascade keys survive: the backend normalizer reads them.
        assert adapted["tool_info"]["mcp_tool_name"] == "list_issues"
        assert adapted["execution_id"] == "exec-1"

    def test_post_mcp_tool_use_flattens_result(self):
        adapted = adapt_windsurf_payload(
            {
                "agent_action_name": "post_mcp_tool_use",
                "trajectory_id": "traj-1",
                "tool_info": {
                    "mcp_server_name": "linear-44",
                    "mcp_tool_name": "list_issues",
                    "mcp_result": {"issues": []},
                },
            }
        )

        assert adapted["tool_name"] == "mcp__linear-44__list_issues"
        assert adapted["tool_response"] == {"issues": []}

    def test_half_named_mcp_tool_yields_no_tool_name(self):
        adapted = adapt_windsurf_payload(
            {
                "agent_action_name": "pre_mcp_tool_use",
                "tool_info": {"mcp_server_name": "linear-44"},
            }
        )

        assert "tool_name" not in adapted
        assert windsurf_mcp_tool_name("linear-44", "") == ""

    def test_run_command_flattens_command_line(self):
        adapted = adapt_windsurf_payload(
            {
                "agent_action_name": "pre_run_command",
                "trajectory_id": "traj-2",
                "tool_info": {"command_line": "cat .env", "cwd": "/repo"},
            }
        )

        assert adapted["command"] == "cat .env"
        assert adapted["cwd"] == "/repo"
        assert adapted["session_id"] == "traj-2"

    def test_read_code_flattens_file_path(self):
        adapted = adapt_windsurf_payload(
            {
                "agent_action_name": "pre_read_code",
                "tool_info": {"file_path": "/repo/.env"},
            }
        )

        assert adapted["file_path"] == "/repo/.env"

    def test_user_prompt_flattens_prompt(self):
        adapted = adapt_windsurf_payload(
            {
                "agent_action_name": "pre_user_prompt",
                "tool_info": {"user_prompt": "ship the hook"},
            }
        )

        assert adapted["prompt"] == "ship the hook"

    def test_existing_flat_keys_are_never_overwritten(self):
        """A future Cascade release that emits flat names must win."""
        adapted = adapt_windsurf_payload(
            {
                "agent_action_name": "pre_run_command",
                "hook_event_name": "already_flat",
                "trajectory_id": "traj-3",
                "session_id": "flat-session",
                "command": "echo flat",
                "tool_info": {"command_line": "cat .env"},
            }
        )

        assert adapted["hook_event_name"] == "already_flat"
        assert adapted["session_id"] == "flat-session"
        assert adapted["command"] == "echo flat"
        # Derived-only fields still fill in.
        assert adapted["conversation_id"] == "traj-3"

    def test_non_dict_tool_info_is_tolerated(self):
        adapted = adapt_windsurf_payload(
            {
                "agent_action_name": "pre_run_command",
                "trajectory_id": "traj-4",
                "tool_info": "not-a-dict",
            }
        )

        assert adapted["hook_event_name"] == "pre_run_command"
        assert adapted["session_id"] == "traj-4"
        assert "command" not in adapted

    def test_missing_tool_info_and_ids_are_tolerated(self):
        assert adapt_windsurf_payload({}) == {}
        adapted = adapt_windsurf_payload({"agent_action_name": "pre_user_prompt"})
        assert adapted["hook_event_name"] == "pre_user_prompt"
        assert "session_id" not in adapted
        assert "prompt" not in adapted

    def test_non_string_fields_are_ignored(self):
        adapted = adapt_windsurf_payload(
            {
                "agent_action_name": 7,
                "trajectory_id": None,
                "tool_info": {"file_path": ["/repo/.env"]},
            }
        )

        assert "hook_event_name" not in adapted
        assert "session_id" not in adapted
        assert "file_path" not in adapted


# =========================================================================
# messages tests
# =========================================================================


class TestAuthRequiredMessage:
    """Regression: bash hook always tells user to run 'runlayer login'.

    The Python `auth_required()` previously branched on tool_name and used
    `_violation()` (generic 'contact administrator' footer) when tool_name
    was empty -- producing a less actionable message than the bash equivalent
    for the same fail-closed auth failure.
    """

    _LOGIN_FOOTER = "Run 'runlayer login' to set up authentication, then retry."

    def test_includes_login_footer_without_tool_name(self):
        _, agent_msg = messages.auth_required()
        assert self._LOGIN_FOOTER in agent_msg
        assert "contact your Runlayer administrator" not in agent_msg

    def test_includes_login_footer_with_tool_name(self):
        _, agent_msg = messages.auth_required(tool_name="mcp__github__list_repos")
        assert self._LOGIN_FOOTER in agent_msg
        assert "- Tool: mcp__github__list_repos" in agent_msg


# =========================================================================
# End-to-end integration via `python -m runlayer_cli.hook`
# =========================================================================


def _run_python_hook(
    input_json: str,
    *,
    config_dir: str,
    client: str = "claude_code",
    enforcement: bool = True,
    extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess:
    """Run the Python hook entrypoint as a subprocess.

    When CURSOR_VERSION is in extra_env, sets up a .cursor/hooks/ directory
    so the third-party hook guard doesn't trigger.
    """
    is_cursor = extra_env and "CURSOR_VERSION" in extra_env

    if is_cursor or client == "cursor":
        hook_dir = Path(config_dir) / ".cursor" / "hooks"
    elif client == "codex":
        hook_dir = Path(config_dir) / ".codex" / "hooks"
    elif client == "hermes":
        hook_dir = Path(config_dir) / ".hermes" / "agent-hooks"
    elif client == "goose":
        hook_dir = (
            Path(config_dir) / ".agents" / "plugins" / "runlayer-hooks" / "scripts"
        )
    elif client == "grok-cli":
        hook_dir = Path(config_dir) / ".grok" / "hooks"
    elif client == "windsurf":
        hook_dir = Path(config_dir) / ".codeium" / "windsurf" / "hooks"
    else:
        hook_dir = Path(config_dir) / "hooks"
    hook_dir.mkdir(parents=True, exist_ok=True)

    config_path = hook_dir / "runlayer-config.json"
    config_path.write_text(json.dumps({"enforcement": enforcement}))

    # Write a thin wrapper so sys.argv[0] is inside the correct client dir
    wrapper = hook_dir / "aiwatch-enforce-wrapper.py"
    wrapper.write_text(
        "import sys, os\n"
        f"sys.argv[0] = {str(wrapper)!r}\n"
        f"os.chdir({str(hook_dir)!r})\n"
        "from runlayer_cli.hook.__main__ import main\n"
        "main()\n"
    )

    env = {**os.environ}
    if "CURSOR_VERSION" in env:
        del env["CURSOR_VERSION"]
    if extra_env:
        env.update(extra_env)

    return subprocess.run(
        [sys.executable, str(wrapper)],
        input=input_json,
        capture_output=True,
        text=True,
        env=env,
        cwd=str(hook_dir),
    )


class TestEndToEndFilePolicy:
    def test_cursor_before_read_file_blocks_env(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps(
                    {"hook_event_name": "beforeReadFile", "file_path": "/project/.env"}
                ),
                config_dir=td,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"

    def test_cursor_before_tab_file_read_blocks_env(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps(
                    {
                        "hook_event_name": "beforeTabFileRead",
                        "file_path": "/project/.env",
                    }
                ),
                config_dir=td,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"

    def test_cursor_before_read_file_allows_normal(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps(
                    {
                        "hook_event_name": "beforeReadFile",
                        "file_path": "/project/README.md",
                    }
                ),
                config_dir=td,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output == {"permission": "allow"}

    def test_claude_code_pretooluse_read_env_denied(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps(
                    {
                        "hook_event_name": "PreToolUse",
                        "tool_name": "Read",
                        "tool_input": {"file_path": "/project/.env"},
                    }
                ),
                config_dir=td,
                extra_env={"HOOK_EVENT_NAME": "PreToolUse"},
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            hso = output["hookSpecificOutput"]
            assert hso["permissionDecision"] == "deny"
            assert "environment files" in hso["permissionDecisionReason"]

    def test_claude_code_bash_cat_env_denied(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps(
                    {
                        "hook_event_name": "PreToolUse",
                        "tool_name": "Bash",
                        "tool_input": {"command": "cat .env"},
                    }
                ),
                config_dir=td,
                extra_env={"HOOK_EVENT_NAME": "PreToolUse"},
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_hermes_terminal_cat_env_denied(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps(
                    {
                        "hook_event_name": "pre_tool_call",
                        "tool_name": "terminal",
                        "tool_input": {"command": "cat .env"},
                    }
                ),
                config_dir=td,
                client="hermes",
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["action"] == "block"
            assert "environment files" in output["message"]

    def test_goose_pretooluse_bash_cat_env_denied(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps(
                    {
                        "event": "PreToolUse",
                        "tool_name": "Bash",
                        "tool_input": {"command": "cat .env"},
                    }
                ),
                config_dir=td,
                client="goose",
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["decision"] == "block"
            assert "environment files" in output["reason"]

    def test_grok_cli_pre_tool_deny_exits_two_with_native_json(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps(
                    {
                        "hookEventName": "pre_tool_use",
                        "toolName": "run_terminal_cmd",
                        "toolInput": {"command": "cat .env"},
                    }
                ),
                config_dir=td,
                client="grok-cli",
            )

            assert result.returncode == 2
            output = json.loads(result.stdout)
            assert output["decision"] == "deny"
            assert "environment files" in output["reason"]

    def test_goose_before_shell_execution_uses_matcher_context(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps(
                    {
                        "event": "BeforeShellExecution",
                        "matcher_context": "cat .env",
                    }
                ),
                config_dir=td,
                client="goose",
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["decision"] == "block"
            assert "environment files" in output["reason"]


class TestEndToEndEventNormalization:
    def test_cursor_pretooluse_normalized(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps(
                    {
                        "hook_event_name": "preToolUse",
                        "tool_name": "Read",
                        "tool_input": {"file_path": "/project/.env"},
                    }
                ),
                config_dir=td,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"

    def test_missing_hook_event_name_exits_silently(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps({"tool_name": "Read", "tool_input": {}}),
                config_dir=td,
            )
            assert result.returncode == 0
            assert result.stdout.strip() == ""


class TestEndToEndCodexDeny:
    def test_codex_pretooluse_blocks_bash_env(self):
        with tempfile.TemporaryDirectory() as td:
            codex_dir = Path(td) / ".codex" / "hooks"
            codex_dir.mkdir(parents=True)
            (codex_dir / "runlayer-config.json").write_text(
                json.dumps({"enforcement": True})
            )

            env = {**os.environ}
            if "CURSOR_VERSION" in env:
                del env["CURSOR_VERSION"]

            result = subprocess.run(
                [sys.executable, "-m", "runlayer_cli.hook"],
                input=json.dumps(
                    {
                        "hook_event_name": "PreToolUse",
                        "tool_name": "Bash",
                        "tool_input": {"command": "cat .env"},
                    }
                ),
                capture_output=True,
                text=True,
                env={**env, "HOOK_EVENT_NAME": "PreToolUse"},
                cwd=str(codex_dir),
            )
            assert result.returncode == 0
            payload = json.loads(result.stdout)
            hso = payload["hookSpecificOutput"]
            assert hso["hookEventName"] == "PreToolUse"
            assert hso["permissionDecision"] == "deny"
            assert "environment files" in hso["permissionDecisionReason"]

    def test_codex_permission_request_deny_shape(self):
        with tempfile.TemporaryDirectory() as td:
            codex_dir = Path(td) / ".codex" / "hooks"
            codex_dir.mkdir(parents=True)
            (codex_dir / "runlayer-config.json").write_text(
                json.dumps({"enforcement": True})
            )

            env = {**os.environ}
            if "CURSOR_VERSION" in env:
                del env["CURSOR_VERSION"]

            result = subprocess.run(
                [sys.executable, "-m", "runlayer_cli.hook"],
                input=json.dumps(
                    {
                        "hook_event_name": "PermissionRequest",
                        "tool_name": "Bash",
                        "tool_input": {"command": "cat .env"},
                    }
                ),
                capture_output=True,
                text=True,
                env={**env, "HOOK_EVENT_NAME": "PermissionRequest"},
                cwd=str(codex_dir),
            )
            assert result.returncode == 0


class TestEndToEndWindsurfDeny:
    """Windsurf/Cascade blocks on process exit status, not on stdout JSON.

    Cascade parses no hook stdout: a pre-hook denies only by exiting 2, and the
    hook's stderr is what the user sees. Writing deny JSON to stdout and exiting
    0 (every other client's contract) would silently allow the action.
    """

    def test_pre_read_code_deny_exits_two_with_stderr_reason(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps(
                    {
                        "agent_action_name": "pre_read_code",
                        "trajectory_id": "traj-1",
                        "tool_info": {"file_path": "/project/.env"},
                    }
                ),
                config_dir=td,
                client="windsurf",
            )

            assert result.returncode == 2
            assert result.stdout == ""
            assert "environment files" in result.stderr

    def test_pre_run_command_deny_exits_two_with_stderr_reason(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps(
                    {
                        "agent_action_name": "pre_run_command",
                        "trajectory_id": "traj-1",
                        "tool_info": {"command_line": "cat .env"},
                    }
                ),
                config_dir=td,
                client="windsurf",
            )

            assert result.returncode == 2
            assert result.stdout == ""
            assert "environment files" in result.stderr

    def test_monitor_read_exits_zero_with_empty_stdout(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps(
                    {
                        "agent_action_name": "pre_read_code",
                        "trajectory_id": "traj-1",
                        "tool_info": {"file_path": "/project/README.md"},
                    }
                ),
                config_dir=td,
                client="windsurf",
                enforcement=False,
            )

            assert result.returncode == 0
            assert result.stdout == ""


class TestHookDeviceContext:
    def test_build_device_context_uses_managed_identity_overrides(self, monkeypatch):
        monkeypatch.setattr(
            relay,
            "read_managed_config",
            lambda: {
                "username": "alice@example.com",
                "device_name": "Alice MacBook",
            },
        )
        monkeypatch.setattr(
            "runlayer_cli.scan.device.get_device_metadata",
            lambda: {
                "hostname": "os-hostname",
                "os": "darwin",
                "os_version": "25.0.0",
                "username": "alice",
            },
        )
        monkeypatch.setattr(
            "runlayer_cli.scan.device.get_or_create_device_id",
            lambda: "device-123",
        )

        assert relay._build_device_context() == {
            "device_id": "device-123",
            "hostname": "Alice MacBook",
            "os": "darwin",
            "os_version": "25.0.0",
            "username": "alice@example.com",
            "serial_number": None,
        }


class TestForwardPost:
    """Fire-and-forget event POSTs run synchronously in-process.

    Earlier versions re-execed the binary with a `__relay_worker__` argv[1]
    sentinel so the POST could outlive the parent. Since `aiwatch-hook` is
    invoked once per hook event and ships that one event before exiting,
    there's no benefit to a detached subprocess — synchronous in-process
    is simpler and behaves identically from the AI client's POV.
    """

    def test_forward_post_calls_post_inline(self, monkeypatch):
        captured: dict = {}

        def _fake_load_credentials():
            return ("https://api.example.com", "rl_user_xyz")

        def _fake_post(host, secret, payload, *, target, timeout, debug):
            captured["host"] = host
            captured["secret"] = secret
            captured["payload"] = payload
            captured["target"] = target
            captured["timeout"] = timeout
            return ""

        monkeypatch.setattr(relay, "_load_credentials", _fake_load_credentials)
        monkeypatch.setattr(relay, "_post", _fake_post)

        relay._forward_post("event", '{"hello": "world"}')

        assert captured["host"] == "https://api.example.com"
        assert captured["secret"] == "rl_user_xyz"
        assert captured["payload"] == '{"hello": "world"}'
        assert captured["target"] == "event"
        assert captured["timeout"] is None

    def test_forward_post_swallows_relay_errors(self, monkeypatch):
        def _raise_credentials():
            raise relay.RelayError(1, "no host")

        monkeypatch.setattr(relay, "_load_credentials", _raise_credentials)
        relay._forward_post("event", "{}")

    def test_forward_post_swallows_post_exceptions(self, monkeypatch):
        monkeypatch.setattr(
            relay,
            "_load_credentials",
            lambda: ("https://api.example.com", "rl_user_xyz"),
        )

        def _raise_runtime(*args, **kwargs):
            raise RuntimeError("boom")

        monkeypatch.setattr(relay, "_post", _raise_runtime)
        relay._forward_post("event", "{}")


class TestTranscriptStreamSpawn:
    """The transcript-stream tailer is the only worker that re-execs the
    binary — it must outlive the parent hook process for the whole Claude
    Code prompt turn. Frozen binaries spawn `[exe, "__transcript_stream_worker__"]`
    and route that argv shape inside `__main__.main()`.
    """

    def test_start_transcript_stream_uses_sentinel_argv_when_frozen(
        self, monkeypatch, tmp_path: Path
    ):
        captured: dict = {}
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("")

        class _FakeStdin:
            def write(self, data):
                captured["stdin"] = data

            def close(self):
                captured["closed"] = True

        class _FakePopen:
            def __init__(self, args, **kwargs):
                captured["args"] = args
                captured["kwargs"] = kwargs
                self.stdin = _FakeStdin()

        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(sys, "frozen", True, raising=False)
        monkeypatch.setattr(sys, "executable", "/opt/aiwatch-enforce/aiwatch-enforce")
        monkeypatch.setattr(relay.subprocess, "Popen", _FakePopen)

        started = relay.start_transcript_stream(
            "claude_code",
            {"session_id": "stream-s1", "transcript_path": str(transcript_path)},
        )

        assert started is True
        assert captured["args"] == [
            "/opt/aiwatch-enforce/aiwatch-enforce",
            "__transcript_stream_worker__",
        ]
        assert "-m" not in captured["args"]
        wrapper = json.loads(captured["stdin"].decode("utf-8"))
        assert wrapper["client"] == "claude_code"
        assert wrapper["payload"]["session_id"] == "stream-s1"
        assert not transcript_stream.is_transcript_stream_active(wrapper["payload"])

    def test_start_transcript_stream_supports_codex(self, monkeypatch, tmp_path: Path):
        captured: dict = {}
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("")

        class _FakeStdin:
            def write(self, data):
                captured["stdin"] = data

            def close(self):
                captured["closed"] = True

        class _FakePopen:
            def __init__(self, args, **kwargs):
                captured["args"] = args
                captured["kwargs"] = kwargs
                self.stdin = _FakeStdin()

        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(sys, "frozen", True, raising=False)
        monkeypatch.setattr(sys, "executable", "/opt/aiwatch/aiwatch")
        monkeypatch.setattr(relay.subprocess, "Popen", _FakePopen)

        started = relay.start_transcript_stream(
            "codex",
            {"session_id": "codex-stream-s1", "transcript_path": str(transcript_path)},
        )

        assert started is True
        assert captured["args"] == [
            "/opt/aiwatch/aiwatch",
            "__transcript_stream_worker__",
        ]
        wrapper = json.loads(captured["stdin"].decode("utf-8"))
        assert wrapper["client"] == "codex"
        assert wrapper["payload"]["session_id"] == "codex-stream-s1"

    def test_concurrent_start_claims_session_before_spawning(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("")
        payload = {
            "session_id": "shared-session",
            "transcript_path": str(transcript_path),
        }
        spawn_count = 0

        class _FakeStdin:
            def write(self, _data):
                return None

            def close(self):
                return None

        class _FakePopen:
            def __init__(self, _args, **_kwargs):
                nonlocal spawn_count
                spawn_count += 1
                self.stdin = _FakeStdin()

        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(relay.subprocess, "Popen", _FakePopen)

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(
                executor.map(
                    lambda _index: relay.start_transcript_stream(
                        "claude_code", payload
                    ),
                    range(2),
                )
            )

        assert results == [True, True]
        assert spawn_count == 1

    def test_concurrent_start_replaces_one_stale_claim(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("")
        payload = {
            "session_id": "stale-session",
            "transcript_path": str(transcript_path),
        }
        spawn_count = 0

        class _FakeStdin:
            def write(self, _data):
                return None

            def close(self):
                return None

        class _FakePopen:
            def __init__(self, _args, **_kwargs):
                nonlocal spawn_count
                spawn_count += 1
                self.stdin = _FakeStdin()

        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(transcript_stream.time, "time", lambda: 100.0)
        monkeypatch.setattr(relay.subprocess, "Popen", _FakePopen)
        claim = transcript_stream.transcript_claim_marker_path(payload)
        assert claim is not None
        claim.parent.mkdir(parents=True)
        claim.write_text("69")

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(
                executor.map(
                    lambda _index: relay.start_transcript_stream(
                        "claude_code", payload
                    ),
                    range(2),
                )
            )

        assert results == [True, True]
        assert spawn_count == 1
        assert transcript_stream.is_transcript_stream_claimed(payload)

    def test_live_worker_renews_claim_before_it_expires(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("")
        payload = {
            "session_id": "live-session",
            "transcript_path": str(transcript_path),
        }
        clock = {"epoch": 100.0, "monotonic": 0.0}
        second_start_results: list[bool] = []
        spawn_count = 0

        class _FakeStdin:
            def write(self, _data):
                return None

            def close(self):
                return None

        class _FakePopen:
            def __init__(self, _args, **_kwargs):
                nonlocal spawn_count
                spawn_count += 1
                self.stdin = _FakeStdin()

        def sleep(seconds: float) -> None:
            clock["epoch"] += seconds
            clock["monotonic"] += seconds
            if clock["monotonic"] >= 40 and not second_start_results:
                second_start_results.append(
                    relay.start_transcript_stream("claude_code", payload)
                )

        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(transcript_stream.time, "time", lambda: clock["epoch"])
        monkeypatch.setattr(
            transcript_stream.time, "monotonic", lambda: clock["monotonic"]
        )
        monkeypatch.setattr(transcript_stream.time, "sleep", sleep)
        monkeypatch.setattr(relay.subprocess, "Popen", _FakePopen)
        claim_token = transcript_stream.claim_transcript_stream(payload)
        assert claim_token

        transcript_stream.run_transcript_stream(
            client_name="claude_code",
            payload=payload,
            post_event=lambda *_args: None,
            max_seconds=40,
            idle_seconds=100,
            poll_seconds=10,
            claim_token=claim_token,
        )

        assert second_start_results == [True]
        assert spawn_count == 0

    def test_live_worker_retries_failed_claim_heartbeat_before_expiry(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("")
        payload = {
            "session_id": "heartbeat-retry-session",
            "transcript_path": str(transcript_path),
        }
        clock = {"epoch": 100.0, "monotonic": 0.0}
        heartbeat_attempts = 0
        successor_claims: list[str | None] = []
        original_heartbeat = transcript_stream.heartbeat_transcript_stream_claim

        def heartbeat(candidate_payload: dict, token: str) -> bool:
            nonlocal heartbeat_attempts
            heartbeat_attempts += 1
            if heartbeat_attempts <= 3:
                return False
            return original_heartbeat(candidate_payload, token)

        def sleep(seconds: float) -> None:
            clock["epoch"] += seconds
            clock["monotonic"] += seconds
            if clock["monotonic"] >= 31 and not successor_claims:
                successor_claims.append(
                    transcript_stream.claim_transcript_stream(payload)
                )

        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(transcript_stream.time, "time", lambda: clock["epoch"])
        monkeypatch.setattr(
            transcript_stream.time, "monotonic", lambda: clock["monotonic"]
        )
        monkeypatch.setattr(transcript_stream.time, "sleep", sleep)
        monkeypatch.setattr(
            transcript_stream, "heartbeat_transcript_stream_claim", heartbeat
        )
        claim_token = transcript_stream.claim_transcript_stream(payload)
        assert claim_token

        transcript_stream.run_transcript_stream(
            client_name="claude_code",
            payload=payload,
            post_event=lambda *_args: None,
            max_seconds=31,
            idle_seconds=100,
            poll_seconds=1,
            claim_token=claim_token,
        )

        assert heartbeat_attempts >= 4
        assert successor_claims == [None]

    def test_stale_claim_cleanup_lock_does_not_block_future_workers(
        self, monkeypatch, tmp_path: Path
    ):
        payload = {"session_id": "stale-cleanup"}
        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(transcript_stream.time, "time", lambda: 100.0)
        claim = transcript_stream.transcript_claim_marker_path(payload)
        cleanup = transcript_stream._transcript_claim_cleanup_marker_path(payload)
        assert claim is not None
        assert cleanup is not None
        claim.parent.mkdir(parents=True)
        claim.write_text("69")
        cleanup.write_text("69")

        assert transcript_stream.claim_transcript_stream(payload)
        assert transcript_stream.is_transcript_stream_claimed(payload)

    def test_start_transcript_stream_clears_claim_on_stdin_failure(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("")
        payload = {
            "session_id": "failed-session",
            "transcript_path": str(transcript_path),
        }
        wait_called = threading.Event()

        class _FailingStdin:
            def write(self, _data):
                raise OSError("broken pipe")

        class _FakePopen:
            def __init__(self, _args, **_kwargs):
                self.stdin = _FailingStdin()

            def wait(self):
                wait_called.set()

        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(relay.subprocess, "Popen", _FakePopen)

        assert relay.start_transcript_stream("claude_code", payload) is False
        assert wait_called.wait(timeout=1)
        assert not transcript_stream.is_transcript_stream_claimed(payload)

    def test_start_transcript_stream_clears_claim_on_popen_failure(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("")
        payload = {
            "session_id": "popen-failed-session",
            "transcript_path": str(transcript_path),
        }

        def _failing_popen(*_args, **_kwargs):
            raise OSError("spawn failed")

        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(relay.subprocess, "Popen", _failing_popen)

        assert relay.start_transcript_stream("claude_code", payload) is False
        assert not transcript_stream.is_transcript_stream_claimed(payload)

    def test_start_transcript_stream_reaps_spawned_worker(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("")
        payload = {
            "session_id": "reaped-session",
            "transcript_path": str(transcript_path),
        }
        wait_called = threading.Event()

        class _FakeStdin:
            def write(self, _data):
                return None

            def close(self):
                return None

        class _FakePopen:
            def __init__(self, _args, **_kwargs):
                self.stdin = _FakeStdin()

            def wait(self):
                wait_called.set()

        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(relay.subprocess, "Popen", _FakePopen)

        assert relay.start_transcript_stream("claude_code", payload) is True
        assert wait_called.wait(timeout=1)

    def test_transcript_worker_clears_claim_after_quick_completion(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("")
        payload = {
            "session_id": "quick-session",
            "transcript_path": str(transcript_path),
        }
        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        claim_token = transcript_stream.claim_transcript_stream(payload)
        assert claim_token
        wrapper = json.dumps(
            {
                "client": "claude_code",
                "payload": payload,
                "start_offset": 0,
                "claim_token": claim_token,
            }
        )

        monkeypatch.setattr(sys, "argv", ["worker"])
        monkeypatch.setattr(sys, "stdin", StringIO(wrapper))
        monkeypatch.setattr(
            _transcript_stream_worker, "_flush_backlog", lambda *_a, **_k: None
        )
        monkeypatch.setattr(
            _transcript_stream_worker, "run_transcript_stream", lambda **_k: None
        )

        _transcript_stream_worker.main()

        assert not transcript_stream.is_transcript_stream_claimed(payload)

    def test_exiting_worker_does_not_clear_successor_claim(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("")
        payload = {
            "session_id": "successor-session",
            "transcript_path": str(transcript_path),
        }
        clock = {"epoch": 100.0}

        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(transcript_stream.time, "time", lambda: clock["epoch"])
        first_token = transcript_stream.claim_transcript_stream(payload)
        assert first_token
        clock["epoch"] += transcript_stream._CLAIM_MARKER_MAX_AGE_SECONDS + 1
        successor_token = transcript_stream.claim_transcript_stream(payload)
        assert successor_token
        assert successor_token != first_token

        wrapper = json.dumps(
            {
                "client": "claude_code",
                "payload": payload,
                "start_offset": 0,
                "claim_token": first_token,
            }
        )
        monkeypatch.setattr(sys, "argv", ["worker"])
        monkeypatch.setattr(sys, "stdin", StringIO(wrapper))
        monkeypatch.setattr(
            _transcript_stream_worker, "_flush_backlog", lambda *_a, **_k: None
        )
        monkeypatch.setattr(
            _transcript_stream_worker, "run_transcript_stream", lambda **_k: None
        )

        _transcript_stream_worker.main()

        assert transcript_stream.heartbeat_transcript_stream_claim(
            payload, successor_token
        )
        assert transcript_stream.is_transcript_stream_claimed(payload)

    def test_transcript_worker_clears_claim_for_malformed_wrapper(
        self, monkeypatch, tmp_path: Path
    ):
        payload = {"session_id": "malformed-session"}
        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        claim_token = transcript_stream.claim_transcript_stream(payload)
        assert claim_token
        wrapper = json.dumps(
            {"client": 7, "payload": payload, "claim_token": claim_token}
        )
        monkeypatch.setattr(sys, "argv", ["worker"])
        monkeypatch.setattr(sys, "stdin", StringIO(wrapper))

        _transcript_stream_worker.main()

        assert not transcript_stream.is_transcript_stream_claimed(payload)

    def test_transcript_worker_clears_claim_after_exception(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("")
        payload = {
            "session_id": "exception-session",
            "transcript_path": str(transcript_path),
        }
        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        claim_token = transcript_stream.claim_transcript_stream(payload)
        assert claim_token
        wrapper = json.dumps(
            {
                "client": "claude_code",
                "payload": payload,
                "start_offset": 0,
                "claim_token": claim_token,
            }
        )

        def _raise(**_kwargs):
            raise RuntimeError("worker failed")

        monkeypatch.setattr(sys, "argv", ["worker"])
        monkeypatch.setattr(sys, "stdin", StringIO(wrapper))
        monkeypatch.setattr(
            _transcript_stream_worker, "_flush_backlog", lambda *_a, **_k: None
        )
        monkeypatch.setattr(_transcript_stream_worker, "run_transcript_stream", _raise)

        _transcript_stream_worker.main()

        assert not transcript_stream.is_transcript_stream_claimed(payload)

    def test_main_routes_sentinel_argv_to_transcript_stream_worker(self, monkeypatch):
        called: dict = {"hook_main_ran": False, "stream_args": None}

        def _fake_stream_main():
            called["stream_args"] = list(sys.argv)

        original_dispatch = hook_dispatch._dispatch

        def _spy_dispatch(*args, **kwargs):
            called["hook_main_ran"] = True
            return original_dispatch(*args, **kwargs)

        monkeypatch.setattr(_transcript_stream_worker, "main", _fake_stream_main)
        monkeypatch.setattr(hook_dispatch, "_dispatch", _spy_dispatch)
        monkeypatch.setattr(
            sys,
            "argv",
            ["/opt/aiwatch/aiwatch-hook", "__transcript_stream_worker__"],
        )
        monkeypatch.setenv("HOOK_EVENT_NAME", "UserPromptSubmit")

        hook_main.main()

        assert called["hook_main_ran"] is False
        assert called["stream_args"] == ["/opt/aiwatch/aiwatch-hook"]


class TestUnfrozenHookEntrypointRuntime:
    """The unfrozen ``python -m runlayer_cli.hook`` path is the pip-installed
    ``runlayer`` package, not the MDM-deployed aiwatch binary. It must NOT flag
    the process as the aiwatch runtime, so ``config.load_config`` keeps reading
    ``~/.runlayer/config.yaml`` for host + credential resolution on dev setups.
    """

    def test_hook_main_does_not_mark_aiwatch_runtime(self, monkeypatch):
        from runlayer_cli import runtime

        runtime.reset_aiwatch_runtime()
        monkeypatch.setattr(hook_main, "run_hook", lambda: None)
        monkeypatch.setattr(sys, "argv", ["runlayer-hook"])

        hook_main.main()

        assert runtime.is_aiwatch_runtime() is False

    def test_transcript_worker_main_does_not_mark_aiwatch_runtime(self, monkeypatch):
        import io

        from runlayer_cli import runtime

        runtime.reset_aiwatch_runtime()
        monkeypatch.setattr(sys, "argv", ["worker"])
        monkeypatch.setattr(sys, "stdin", io.StringIO("{}"))

        _transcript_stream_worker.main()

        assert runtime.is_aiwatch_runtime() is False


class TestTranscriptStream:
    def test_transcript_line_events_extract_thoughts_and_responses(self):
        events = transcript_stream.transcript_line_events(
            json.dumps(
                {
                    "session_id": "s1",
                    "timestamp": "2026-05-12T12:00:00Z",
                    "type": "assistant",
                    "message": {
                        "role": "assistant",
                        "content": [
                            {
                                "type": "thinking",
                                "thinking": "Plan the repository inspection.",
                                "signature": "integrity-token",
                            },
                            {
                                "type": "redacted_thinking",
                                "data": "encrypted-thinking",
                            },
                            {
                                "type": "text",
                                "text": "I will inspect the source files.",
                            },
                        ],
                    },
                }
            ),
            fallback_session_id="fallback",
        )

        assert [name for name, _ in events] == [
            "message.part.delta",
            "message.updated",
        ]
        assert events[0][1]["part"] == {
            "type": "reasoning",
            "text": "Plan the repository inspection.",
        }
        assert events[1][1]["message"] == {
            "content": "I will inspect the source files."
        }

    def test_transcript_line_events_forwards_codex_token_count(self):
        events = transcript_stream.transcript_line_events(
            json.dumps(
                {
                    "timestamp": "2026-06-01T10:20:09Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "token_count",
                        "info": {
                            "total_token_usage": {"total_tokens": 430},
                            "last_token_usage": {
                                "input_tokens": 200,
                                "cached_input_tokens": 50,
                                "output_tokens": 80,
                                "reasoning_output_tokens": 12,
                                "total_tokens": 280,
                            },
                            "model_context_window": 258400,
                        },
                    },
                }
            ),
            fallback_session_id="sess-1",
        )

        assert len(events) == 1
        name, payload = events[0]
        assert name == "message.token_count"
        # Per-turn delta (last_token_usage), mapped to canonical flat keys.
        assert payload["input_tokens"] == 200
        assert payload["output_tokens"] == 80
        assert payload["reasoning_tokens"] == 12
        assert payload["cache_read_tokens"] == 50
        assert payload["total_tokens"] == 280
        assert payload["token_source"] == "provider"
        assert payload["token_origin"] == "client_transcript"
        # Stable id derived from the cumulative total, for backfill dedupe.
        assert payload["external_message_id"] == "codex-token-count:sess-1:430"

    def test_transcript_line_events_stamps_turn_context_model(self):
        # Codex omits the model from token_count lines; it lives on the preceding
        # turn_context. With stream_state tracking, the usage event inherits it.
        stream_state: dict = {}
        turn_context = transcript_stream.transcript_line_events(
            json.dumps(
                {
                    "timestamp": "2026-06-01T10:20:05Z",
                    "type": "turn_context",
                    "payload": {"turn_id": "t-1", "model": "gpt-5.5"},
                }
            ),
            fallback_session_id="sess-1",
            stream_state=stream_state,
        )
        # turn_context itself forwards nothing but updates the tracked model.
        assert turn_context == []
        assert stream_state["model"] == "gpt-5.5"

        events = transcript_stream.transcript_line_events(
            json.dumps(
                {
                    "timestamp": "2026-06-01T10:20:09Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "token_count",
                        "info": {
                            "total_token_usage": {"total_tokens": 430},
                            "last_token_usage": {
                                "input_tokens": 200,
                                "output_tokens": 80,
                                "total_tokens": 280,
                            },
                            "model_context_window": 258400,
                        },
                    },
                }
            ),
            fallback_session_id="sess-1",
            stream_state=stream_state,
        )
        assert len(events) == 1
        _, payload = events[0]
        assert payload["model"] == "gpt-5.5"

    def test_transcript_line_events_token_count_without_model_omits_it(self):
        # No turn_context seen (or no stream_state): the usage event still emits,
        # just without a model key — never a spurious value.
        events = transcript_stream.transcript_line_events(
            json.dumps(
                {
                    "timestamp": "2026-06-01T10:20:09Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "token_count",
                        "info": {
                            "total_token_usage": {"total_tokens": 430},
                            "last_token_usage": {
                                "input_tokens": 200,
                                "total_tokens": 280,
                            },
                            "model_context_window": 258400,
                        },
                    },
                }
            ),
            fallback_session_id="sess-1",
        )
        assert len(events) == 1
        _, payload = events[0]
        assert "model" not in payload

    def test_transcript_line_events_ignores_token_count_without_usage(self):
        events = transcript_stream.transcript_line_events(
            json.dumps(
                {
                    "timestamp": "2026-06-01T10:20:09Z",
                    "type": "event_msg",
                    "payload": {"type": "token_count", "info": {}},
                }
            ),
            fallback_session_id="sess-1",
        )
        assert events == []

    def test_transcript_line_is_terminal_for_claude_result(self):
        assert transcript_stream.transcript_line_is_terminal('{"type":"result"}')
        assert not transcript_stream.transcript_line_is_terminal('{"type":"assistant"}')

    def test_transcript_stream_active_requires_recent_heartbeat(
        self, monkeypatch, tmp_path: Path
    ):
        payload = {"session_id": "stream-s1"}
        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(transcript_stream.time, "time", lambda: 100.0)

        assert transcript_stream.mark_transcript_stream_active(payload)
        assert transcript_stream.is_transcript_stream_active(payload)

        marker = transcript_stream.transcript_marker_path(payload)
        assert marker is not None
        marker.write_text("89")

        assert not transcript_stream.is_transcript_stream_active(payload)

    def test_transcript_stream_marker_path_matches_shell_sanitization(
        self, monkeypatch, tmp_path: Path
    ):
        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")

        marker = transcript_stream.transcript_marker_path({"session_id": "a::b"})

        assert marker == tmp_path / "state" / "a__b.active"

    def test_transcript_stream_completion_marker_is_not_active(
        self, monkeypatch, tmp_path: Path
    ):
        payload = {"session_id": "stream-s1"}
        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")

        assert transcript_stream.mark_transcript_stream_completed(payload)

        assert transcript_stream.is_transcript_stream_recently_completed(payload)
        assert not transcript_stream.is_transcript_stream_active(payload)

    def test_transcript_stream_completion_marker_outlives_active_heartbeat(
        self, monkeypatch, tmp_path: Path
    ):
        payload = {"session_id": "stream-s1"}
        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(transcript_stream.time, "time", lambda: 1000.0)

        assert transcript_stream.mark_transcript_stream_completed(payload)
        marker = transcript_stream.transcript_completion_marker_path(payload)
        assert marker is not None
        marker.write_text(
            str(1000 - transcript_stream._ACTIVE_MARKER_MAX_AGE_SECONDS - 1)
        )

        assert transcript_stream.is_transcript_stream_recently_completed(payload)

        marker.write_text(
            str(1000 - transcript_stream._COMPLETED_MARKER_MAX_AGE_SECONDS - 1)
        )

        assert not transcript_stream.is_transcript_stream_recently_completed(payload)

    def test_transcript_stream_continues_after_post_error(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text(
            "\n".join(
                [
                    json.dumps(
                        {
                            "type": "assistant",
                            "message": {
                                "role": "assistant",
                                "content": [{"type": "text", "text": "first"}],
                            },
                        }
                    ),
                    json.dumps(
                        {
                            "type": "assistant",
                            "message": {
                                "role": "assistant",
                                "content": [{"type": "text", "text": "second"}],
                            },
                        }
                    ),
                    '{"type":"result"}',
                ]
            )
            + "\n"
        )
        attempts = {"count": 0}
        delivered: list[tuple[str, dict]] = []
        mark_calls: list[dict] = []

        def _mark_active(payload: dict) -> bool:
            mark_calls.append(payload)
            return True

        monkeypatch.setattr(
            transcript_stream, "mark_transcript_stream_active", _mark_active
        )

        def _flaky_post(_client_name: str, event_name: str, payload: dict) -> None:
            attempts["count"] += 1
            if attempts["count"] == 1:
                raise RuntimeError("temporary network error")
            delivered.append((event_name, payload))

        transcript_stream.run_transcript_stream(
            client_name="claude_code",
            payload={"session_id": "s1", "transcript_path": str(transcript_path)},
            post_event=_flaky_post,
            max_seconds=1,
            idle_seconds=1,
            poll_seconds=0.01,
        )

        assert attempts["count"] == 2
        assert len(delivered) == 1
        event_name, payload = delivered[0]
        assert event_name == "message.updated"
        assert payload["session_id"] == "s1"
        assert payload["message"] == {"content": "second"}
        assert mark_calls == []

    def test_transcript_stream_flushes_final_json_line_without_newline(
        self, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text(
            json.dumps(
                {
                    "type": "assistant",
                    "message": {
                        "role": "assistant",
                        "content": [{"type": "text", "text": "final"}],
                    },
                }
            )
        )
        delivered: list[tuple[str, dict]] = []

        transcript_stream.run_transcript_stream(
            client_name="claude_code",
            payload={"session_id": "s1", "transcript_path": str(transcript_path)},
            post_event=lambda _client_name, event_name, payload: delivered.append(
                (event_name, payload)
            ),
            max_seconds=1,
            idle_seconds=0.02,
            poll_seconds=0.01,
        )

        assert len(delivered) == 1
        event_name, payload = delivered[0]
        assert event_name == "message.updated"
        assert payload["message"] == {"content": "final"}

    def test_transcript_stream_does_not_mark_active_before_delivery(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text(
            "\n".join(
                [
                    json.dumps(
                        {
                            "type": "user",
                            "message": {
                                "role": "user",
                                "content": "hello",
                            },
                        }
                    ),
                    '{"type":"result"}',
                ]
            )
            + "\n"
        )
        marker_updates: list[dict] = []
        delivered: list[tuple[str, dict]] = []

        monkeypatch.setattr(
            transcript_stream,
            "mark_transcript_stream_active",
            lambda payload: bool(marker_updates.append(payload) or True),
        )

        transcript_stream.run_transcript_stream(
            client_name="claude_code",
            payload={"session_id": "s1", "transcript_path": str(transcript_path)},
            post_event=lambda _client_name, event_name, payload: delivered.append(
                (event_name, payload)
            ),
            max_seconds=1,
            idle_seconds=0.02,
            poll_seconds=0.01,
        )

        assert delivered == []
        assert marker_updates == []

    def test_transcript_stream_success_marker_suppresses_immediate_stop_backfill(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text(
            "\n".join(
                [
                    json.dumps(
                        {
                            "type": "assistant",
                            "message": {
                                "role": "assistant",
                                "content": [{"type": "text", "text": "streamed"}],
                            },
                        }
                    ),
                    '{"type":"result"}',
                ]
            )
            + "\n"
        )
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}
        delivered: list[tuple[str, dict]] = []
        forwarded: list[dict] = []
        clear_active_saw_completion: list[bool] = []

        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        clear_transcript_stream_active = (
            transcript_stream.clear_transcript_stream_active
        )

        def _clear_transcript_stream_active(active_payload: dict) -> None:
            clear_active_saw_completion.append(
                transcript_stream.is_transcript_stream_recently_completed(
                    active_payload
                )
            )
            clear_transcript_stream_active(active_payload)

        monkeypatch.setattr(
            transcript_stream,
            "clear_transcript_stream_active",
            _clear_transcript_stream_active,
        )

        transcript_stream.run_transcript_stream(
            client_name="claude_code",
            payload=payload,
            post_event=lambda _client_name, event_name, event_payload: delivered.append(
                (event_name, event_payload)
            ),
            max_seconds=1,
            idle_seconds=0.02,
            poll_seconds=0.01,
        )

        assert len(delivered) == 1
        event_name, event_payload = delivered[0]
        assert event_name == "message.updated"
        assert event_payload["session_id"] == "s1"
        assert event_payload["message"] == {"content": "streamed"}
        assert clear_active_saw_completion == [True]
        assert not transcript_stream.is_transcript_stream_active(payload)
        assert transcript_stream.is_transcript_stream_recently_completed(payload)

        monkeypatch.setattr(
            relay,
            "_forward_post",
            lambda _target, wrapper, **_kwargs: forwarded.append(json.loads(wrapper)),
        )

        relay.forward_stop_event("claude_code", "Stop", payload)

        assert forwarded == [
            {"client": "claude_code", "event_name": "Stop", "payload": payload}
        ]

    def test_start_transcript_stream_ignores_completed_marker(
        self, monkeypatch, tmp_path: Path
    ):
        captured: dict = {}
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("")
        payload = {"session_id": "stream-s1", "transcript_path": str(transcript_path)}

        class _FakeStdin:
            def write(self, data):
                captured["stdin"] = data

            def close(self):
                captured["closed"] = True

        class _FakePopen:
            def __init__(self, args, **kwargs):
                captured["args"] = args
                captured["kwargs"] = kwargs
                self.stdin = _FakeStdin()

        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(relay.subprocess, "Popen", _FakePopen)

        assert transcript_stream.mark_transcript_stream_completed(payload)

        started = relay.start_transcript_stream("claude_code", payload)

        assert started is True
        assert captured["args"]
        assert not transcript_stream.is_transcript_stream_recently_completed(payload)

    def test_start_transcript_stream_restarts_when_completed_overlaps_active(
        self, monkeypatch, tmp_path: Path
    ):
        captured: dict = {}
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("")
        payload = {"session_id": "stream-s1", "transcript_path": str(transcript_path)}

        class _FakeStdin:
            def write(self, data):
                captured["stdin"] = data

            def close(self):
                captured["closed"] = True

        class _FakePopen:
            def __init__(self, args, **kwargs):
                captured["args"] = args
                captured["kwargs"] = kwargs
                self.stdin = _FakeStdin()

        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(transcript_stream.time, "time", lambda: 100.0)
        monkeypatch.setattr(relay.subprocess, "Popen", _FakePopen)

        active_marker = transcript_stream.transcript_marker_path(payload)
        completed_marker = transcript_stream.transcript_completion_marker_path(payload)
        assert active_marker is not None
        assert completed_marker is not None
        active_marker.parent.mkdir(parents=True, exist_ok=True)
        active_marker.write_text("100")
        completed_marker.write_text("100")

        started = relay.start_transcript_stream("claude_code", payload)

        assert started is True
        assert captured["args"]
        assert not transcript_stream.is_transcript_stream_recently_completed(payload)

    def test_http_event_poster_uses_tls_client_and_raises_post_errors(
        self, monkeypatch
    ):
        captured: dict = {}

        class _FakeConfig:
            default_host = "https://tenant.runlayer.test"

            def get_secret_for_host(self, host):
                captured["host"] = host
                return "rl_test"

        class _FailingClient:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def post(self, url, **kwargs):
                captured["url"] = url
                captured["kwargs"] = kwargs
                raise RuntimeError("network down")

        monkeypatch.setattr(transcript_stream, "load_config", lambda: _FakeConfig())
        monkeypatch.setattr(transcript_stream, "http_client", lambda: _FailingClient())
        # Legacy per-user path: no org key in MDM.
        monkeypatch.setattr(transcript_stream, "read_managed_config", lambda: {})

        poster = transcript_stream._make_http_event_poster(debug=True)
        with pytest.raises(RuntimeError, match="network down"):
            poster("claude_code", "message.updated", {"session_id": "s1"})

        assert captured["host"] == "https://tenant.runlayer.test"
        assert captured["url"] == "https://tenant.runlayer.test/api/v1/hooks/events"
        assert captured["kwargs"]["headers"]["x-runlayer-api-key"] == "rl_test"
        # Legacy path attaches no device block.
        assert "device" not in json.loads(captured["kwargs"]["content"])

    def test_http_event_poster_org_key_mode_attaches_device(self, monkeypatch):
        captured: dict = {}

        class _FakeConfig:
            default_host = "https://tenant.runlayer.test"

            def get_secret_for_host(self, _host):
                return "rl_user"

        class _FailingClient:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def post(self, url, **kwargs):
                captured["url"] = url
                captured["kwargs"] = kwargs
                raise RuntimeError("network down")

        monkeypatch.setattr(transcript_stream, "load_config", lambda: _FakeConfig())
        monkeypatch.setattr(transcript_stream, "http_client", lambda: _FailingClient())
        monkeypatch.setattr(
            transcript_stream,
            "read_managed_config",
            lambda: {"org_api_key": "org-key-123"},
        )
        monkeypatch.setattr(
            "runlayer_cli.hook.relay._build_device_context",
            lambda: {"device_id": "dev-1", "username": "alice"},
        )

        poster = transcript_stream._make_http_event_poster(debug=True)
        with pytest.raises(RuntimeError, match="network down"):
            poster("claude_code", "message.updated", {"session_id": "s1"})

        assert captured["kwargs"]["headers"]["x-runlayer-api-key"] == "org-key-123"
        body = json.loads(captured["kwargs"]["content"])
        assert body["device"] == {"device_id": "dev-1", "username": "alice"}

    def test_http_event_poster_treats_non_success_as_failure(self, monkeypatch):
        class _FakeConfig:
            default_host = "https://tenant.runlayer.test"

            def get_secret_for_host(self, _host):
                return "rl_test"

        class _Response:
            is_success = False
            status_code = 503

            def raise_for_status(self):
                raise RuntimeError("HTTP 503")

        class _Client:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def post(self, *_args, **_kwargs):
                return _Response()

        monkeypatch.setattr(transcript_stream, "load_config", lambda: _FakeConfig())
        monkeypatch.setattr(transcript_stream, "http_client", lambda: _Client())

        poster = transcript_stream._make_http_event_poster(debug=False)
        with pytest.raises(RuntimeError, match="HTTP 503"):
            poster("claude_code", "message.updated", {"session_id": "s1"})

    def test_http_event_poster_reuses_tls_client_until_closed(self, monkeypatch):
        calls = {"clients": 0, "posts": 0, "closes": 0}

        class _FakeConfig:
            default_host = "https://tenant.runlayer.test"

            def get_secret_for_host(self, _host):
                return "rl_test"

        class _Response:
            is_success = True
            status_code = 200

        class _Client:
            def post(self, *_args, **_kwargs):
                calls["posts"] += 1
                return _Response()

            def close(self):
                calls["closes"] += 1

        def _http_client():
            calls["clients"] += 1
            return _Client()

        monkeypatch.setattr(transcript_stream, "load_config", lambda: _FakeConfig())
        monkeypatch.setattr(transcript_stream, "http_client", _http_client)

        poster = transcript_stream._make_http_event_poster(debug=False)
        poster("claude_code", "message.updated", {"session_id": "s1"})
        poster("claude_code", "message.updated", {"session_id": "s1"})
        poster.close()

        assert calls == {"clients": 1, "posts": 2, "closes": 1}

    def test_claude_user_prompt_submit_starts_transcript_stream(
        self, monkeypatch, capsys
    ):
        started: list[tuple[str, dict, bool]] = []
        forwarded: list[tuple[str, str, dict, bool]] = []
        payload = {
            "hook_event_name": "UserPromptSubmit",
            "session_id": "s1",
            "transcript_path": "/tmp/transcript.jsonl",
        }

        def _fake_start(client_name, input_data, *, debug):
            started.append((client_name, input_data, debug))
            return True

        def _fake_forward(client_name, event_name, input_data, *, debug):
            forwarded.append((client_name, event_name, input_data, debug))

        monkeypatch.setattr(hook_dispatch, "start_transcript_stream", _fake_start)
        monkeypatch.setattr(hook_dispatch, "forward_event", _fake_forward)

        hook_dispatch._dispatch(
            hook_type="UserPromptSubmit",
            original_hook_type="UserPromptSubmit",
            client=Client.CLAUDE_CODE,
            resp=HookResponse(Client.CLAUDE_CODE, "UserPromptSubmit"),
            input_data=payload,
            raw_input=json.dumps(payload),
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert capsys.readouterr().out == ""
        assert started == [("claude_code", payload, False)]
        assert forwarded == [("claude_code", "UserPromptSubmit", payload, False)]

    def test_codex_user_prompt_submit_starts_transcript_stream(
        self, monkeypatch, capsys
    ):
        started: list[tuple[str, dict, bool]] = []
        forwarded: list[tuple[str, str, dict, bool]] = []
        payload = {
            "hook_event_name": "UserPromptSubmit",
            "session_id": "codex-s1",
            "transcript_path": "/tmp/codex-transcript.jsonl",
        }

        def _fake_start(client_name, input_data, *, debug):
            started.append((client_name, input_data, debug))
            return True

        def _fake_forward(client_name, event_name, input_data, *, debug):
            forwarded.append((client_name, event_name, input_data, debug))

        monkeypatch.setattr(hook_dispatch, "start_transcript_stream", _fake_start)
        monkeypatch.setattr(hook_dispatch, "forward_event", _fake_forward)

        hook_dispatch._dispatch(
            hook_type="UserPromptSubmit",
            original_hook_type="UserPromptSubmit",
            client=Client.CODEX,
            resp=HookResponse(Client.CODEX, "UserPromptSubmit"),
            input_data=payload,
            raw_input=json.dumps(payload),
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert capsys.readouterr().out == ""
        assert started == [("codex", payload, False)]
        assert forwarded == [("codex", "UserPromptSubmit", payload, False)]


class TestForwardStopEvent:
    def test_existing_transcript_does_not_sleep(self, monkeypatch, tmp_path):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text('{"ready":true}\n')
        sleeps: list[float] = []
        captured: list[tuple[str, str]] = []

        def _fake_forward(target, wrapper, *, timeout=None, debug=False):
            captured.append((target, wrapper))

        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(relay.time, "sleep", lambda seconds: sleeps.append(seconds))
        monkeypatch.setattr(relay, "_forward_post", _fake_forward)
        monkeypatch.setattr(relay, "_forward_post_strict", _fake_forward)

        relay.forward_stop_event(
            "claude_code",
            "Stop",
            {"session_id": "s1", "transcript_path": str(transcript_path)},
        )

        assert sleeps == []
        assert captured[0][0] == "event"
        wrapper = json.loads(captured[0][1])
        assert wrapper["event_name"] == "Stop"
        assert wrapper["transcript"] == '{"ready":true}\n'

    def test_claude_stop_skips_transcript_backfill_when_stream_active(
        self, monkeypatch, tmp_path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text('{"ready":true}\n')
        captured: list[tuple[str, str]] = []

        def _fake_forward(target, wrapper, *, timeout=None, debug=False):
            captured.append((target, wrapper))

        monkeypatch.setattr(relay, "_forward_post", _fake_forward)
        monkeypatch.setattr(relay, "is_transcript_stream_active", lambda payload: True)

        relay.forward_stop_event(
            "claude_code",
            "Stop",
            {"session_id": "s1", "transcript_path": str(transcript_path)},
        )

        assert captured[0][0] == "event"
        wrapper = json.loads(captured[0][1])
        assert wrapper["event_name"] == "Stop"
        assert "transcript" not in wrapper

    def test_codex_stop_skips_transcript_backfill_when_stream_active(
        self, monkeypatch, tmp_path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text('{"ready":true}\n')
        captured: list[tuple[str, str]] = []

        def _fake_forward(target, wrapper, *, timeout=None, debug=False):
            captured.append((target, wrapper))

        monkeypatch.setattr(relay, "_forward_post", _fake_forward)
        monkeypatch.setattr(relay, "is_transcript_stream_active", lambda payload: True)

        relay.forward_stop_event(
            "codex",
            "Stop",
            {"session_id": "s1", "transcript_path": str(transcript_path)},
        )

        assert captured[0][0] == "event"
        wrapper = json.loads(captured[0][1])
        assert wrapper["event_name"] == "Stop"
        assert "transcript" not in wrapper


class TestSkillPayloadEnrichment:
    def _capture_detached(self, monkeypatch) -> list[tuple[str, str]]:
        captured: list[tuple[str, str]] = []

        def _fake_forward(target, wrapper, *, timeout=None, debug=False):
            captured.append((target, wrapper))

        monkeypatch.setattr(relay, "_forward_post", _fake_forward)
        return captured

    def _capture_checks(
        self,
        monkeypatch,
        *,
        response: str = '{"permission":"allow","blocked":false}',
    ) -> list[tuple[str, str, str, str, dict]]:
        captured: list[tuple[str, str, str, str, dict]] = []

        def _fake_check(target, client_name, event_name, tool_name, payload, *, debug):
            captured.append((target, client_name, event_name, tool_name, payload))
            return response

        monkeypatch.setattr(hook_dispatch, "check_tool_lifecycle", _fake_check)
        return captured

    def _run_pre(
        self,
        monkeypatch,
        payload: dict,
        *,
        client: Client = Client.CLAUDE_CODE,
    ) -> tuple[list[tuple[str, str]], list[tuple[str, str, str, str, dict]]]:
        forwarded = self._capture_detached(monkeypatch)
        checks = self._capture_checks(monkeypatch)
        hook_dispatch._handle_pre_tool_use(
            client=client,
            resp=HookResponse(client, "PreToolUse"),
            input_data=payload,
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )
        return forwarded, checks

    def test_managed_skill_enriches_pre_check_and_event(
        self, monkeypatch, tmp_path: Path
    ) -> None:
        skill_id = "550e8400-e29b-41d4-a716-446655440000"
        skill_dir = tmp_path / ".claude" / "skills" / "sol"
        skill_dir.mkdir(parents=True)
        (skill_dir / ".installed").write_text(
            f"managed:{skill_id}:abc123\n", encoding="utf-8"
        )
        monkeypatch.setattr(Path, "home", classmethod(lambda _cls: tmp_path))
        tool_input = {"skill": "sol", "args": "x"}
        payload = {"tool_name": "Skill", "tool_input": tool_input}

        forwarded, checks = self._run_pre(monkeypatch, payload)

        assert checks[0][4]["skill_id"] == skill_id
        event_payload = json.loads(forwarded[0][1])["payload"]
        assert event_payload["skill_id"] == skill_id
        assert checks[0][4]["tool_input"] == tool_input
        assert event_payload["tool_input"] == tool_input

    def test_user_installed_skill_is_not_enriched(
        self, monkeypatch, tmp_path: Path
    ) -> None:
        skill_dir = tmp_path / ".claude" / "skills" / "sol"
        skill_dir.mkdir(parents=True)
        (skill_dir / ".installed").write_text("", encoding="utf-8")
        monkeypatch.setattr(Path, "home", classmethod(lambda _cls: tmp_path))
        payload = {"tool_name": "Skill", "tool_input": {"skill": "sol"}}

        _, checks = self._run_pre(monkeypatch, payload)

        assert "skill_id" not in checks[0][4]

    def test_missing_skill_dir_is_not_enriched(
        self, monkeypatch, tmp_path: Path
    ) -> None:
        monkeypatch.setattr(Path, "home", classmethod(lambda _cls: tmp_path))
        payload = {"tool_name": "Skill", "tool_input": {"skill": "sol"}}

        _, checks = self._run_pre(monkeypatch, payload)

        assert "skill_id" not in checks[0][4]

    def test_plugin_scoped_skill_is_rejected_before_marker_read(
        self, monkeypatch
    ) -> None:
        monkeypatch.setattr(
            hook_dispatch,
            "managed_marker_skill_id",
            lambda _path: pytest.fail("plugin-scoped skill read a marker"),
        )
        payload = {
            "tool_name": "Skill",
            "tool_input": {"skill": "plug:skill"},
        }

        _, checks = self._run_pre(monkeypatch, payload)

        assert "skill_id" not in checks[0][4]

    @pytest.mark.parametrize("name", ["../evil", "a/b"])
    def test_unsafe_skill_name_is_rejected_before_marker_read(
        self, monkeypatch, name: str
    ) -> None:
        monkeypatch.setattr(
            hook_dispatch,
            "managed_marker_skill_id",
            lambda _path: pytest.fail("unsafe skill name read a marker"),
        )
        payload = {"tool_name": "Skill", "tool_input": {"skill": name}}

        _, checks = self._run_pre(monkeypatch, payload)

        assert "skill_id" not in checks[0][4]

    def test_project_skill_marker_wins_over_global(
        self, monkeypatch, tmp_path: Path
    ) -> None:
        home = tmp_path / "home"
        project = tmp_path / "project"
        global_dir = home / ".claude" / "skills" / "sol"
        project_dir = project / ".claude" / "skills" / "sol"
        global_dir.mkdir(parents=True)
        project_dir.mkdir(parents=True)
        (global_dir / ".installed").write_text(
            "managed:global-id:global-sha", encoding="utf-8"
        )
        (project_dir / ".installed").write_text(
            "managed:project-id:project-sha", encoding="utf-8"
        )
        monkeypatch.setattr(Path, "home", classmethod(lambda _cls: home))
        payload = {
            "tool_name": "Skill",
            "tool_input": {"skill": "sol"},
            "cwd": str(project),
        }

        _, checks = self._run_pre(monkeypatch, payload)

        assert checks[0][4]["skill_id"] == "project-id"

    def test_unmanaged_shadowing_skill_blocks_managed_fallthrough(
        self, monkeypatch, tmp_path: Path
    ) -> None:
        """A local unmanaged copy shadows a managed one — the badge must not
        be borrowed from the copy the client did not run."""
        home = tmp_path / "home"
        project = tmp_path / "project"
        global_dir = home / ".claude" / "skills" / "sol"
        project_dir = project / ".claude" / "skills" / "sol"
        global_dir.mkdir(parents=True)
        project_dir.mkdir(parents=True)
        (global_dir / ".installed").write_text(
            "managed:global-id:global-sha", encoding="utf-8"
        )
        (project_dir / ".installed").write_text("", encoding="utf-8")
        monkeypatch.setattr(Path, "home", classmethod(lambda _cls: home))
        payload = {
            "tool_name": "Skill",
            "tool_input": {"skill": "sol"},
            "cwd": str(project),
        }

        _, checks = self._run_pre(monkeypatch, payload)

        assert "skill_id" not in checks[0][4]

    def test_markerless_shadowing_skill_blocks_managed_fallthrough(
        self, monkeypatch, tmp_path: Path
    ) -> None:
        home = tmp_path / "home"
        project = tmp_path / "project"
        global_dir = home / ".claude" / "skills" / "sol"
        project_dir = project / ".claude" / "skills" / "sol"
        global_dir.mkdir(parents=True)
        project_dir.mkdir(parents=True)
        (global_dir / ".installed").write_text(
            "managed:global-id:global-sha", encoding="utf-8"
        )
        monkeypatch.setattr(Path, "home", classmethod(lambda _cls: home))
        payload = {
            "tool_name": "Skill",
            "tool_input": {"skill": "sol"},
            "cwd": str(project),
        }

        _, checks = self._run_pre(monkeypatch, payload)

        assert "skill_id" not in checks[0][4]

    def test_non_skill_tool_is_untouched(self, monkeypatch) -> None:
        monkeypatch.setattr(
            hook_dispatch,
            "managed_marker_skill_id",
            lambda _path: pytest.fail("non-Skill tool read a marker"),
        )
        payload = {"tool_name": "Bash", "tool_input": {"command": "pwd"}}
        expected = {"tool_name": "Bash", "tool_input": {"command": "pwd"}}

        _, checks = self._run_pre(monkeypatch, payload)

        assert checks[0][4] == expected

    def test_managed_skill_enriches_post_check_and_event(
        self, monkeypatch, tmp_path: Path
    ) -> None:
        skill_id = "550e8400-e29b-41d4-a716-446655440000"
        skill_dir = tmp_path / ".claude" / "skills" / "sol"
        skill_dir.mkdir(parents=True)
        (skill_dir / ".installed").write_text(
            f"managed:{skill_id}:abc123\n", encoding="utf-8"
        )
        monkeypatch.setattr(Path, "home", classmethod(lambda _cls: tmp_path))
        forwarded = self._capture_detached(monkeypatch)
        checks = self._capture_checks(monkeypatch, response='{"blocked":false}')
        tool_input = {"skill": "sol", "args": "x"}
        payload = {
            "tool_name": "Skill",
            "tool_input": tool_input,
            "tool_response": {"ok": True},
        }

        hook_dispatch._dispatch(
            hook_type="PostToolUse",
            original_hook_type="PostToolUse",
            client=Client.CLAUDE_CODE,
            resp=HookResponse(Client.CLAUDE_CODE, "PostToolUse"),
            input_data=payload,
            raw_input="{}",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert checks[0][4]["skill_id"] == skill_id
        event_payload = json.loads(forwarded[0][1])["payload"]
        assert event_payload["skill_id"] == skill_id
        assert checks[0][4]["tool_input"] == tool_input
        assert event_payload["tool_input"] == tool_input

    def test_marker_read_oserror_does_not_break_hook(
        self, monkeypatch, tmp_path: Path
    ) -> None:
        skill_path = tmp_path / ".claude" / "skills" / "sol"
        skill_path.parent.mkdir(parents=True)
        skill_path.write_text("not a directory", encoding="utf-8")
        monkeypatch.setattr(Path, "home", classmethod(lambda _cls: tmp_path))
        payload = {"tool_name": "Skill", "tool_input": {"skill": "sol"}}

        _, checks = self._run_pre(monkeypatch, payload)

        assert "skill_id" not in checks[0][4]


class TestToolLifecycleRouting:
    """Regression: PreToolUse (non-MCP/Read/Bash) and PostToolUse must POST to
    the tool-pre / tool-post endpoints, not the generic events endpoint.

    The bash hook calls /api/v1/hooks/tool/pre and /api/v1/hooks/tool/post for
    these events; the backend depends on receiving them there for proper
    normalization (LocalToolPreRequest / LocalToolPostRequest schemas).
    Routing them to /events silently downgrades the audit/scan pipeline.
    """

    def _capture_detached(self, monkeypatch) -> list[tuple[str, str]]:
        captured: list[tuple[str, str]] = []

        def _fake_forward(target, wrapper, *, timeout=None, debug=False):
            captured.append((target, wrapper))

        monkeypatch.setattr(relay, "_forward_post", _fake_forward)
        return captured

    def _capture_checks(
        self,
        monkeypatch,
        *,
        response: str = '{"permission":"allow","blocked":false}',
    ) -> list[tuple[str, str, str, str, dict]]:
        captured: list[tuple[str, str, str, str, dict]] = []

        def _fake_check(target, client_name, event_name, tool_name, payload, *, debug):
            captured.append((target, client_name, event_name, tool_name, payload))
            return response

        monkeypatch.setattr(hook_dispatch, "check_tool_lifecycle", _fake_check)
        return captured

    def _run_cline_hook(
        self,
        monkeypatch,
        payload: dict[str, object],
        *,
        hook_event_name: str | None = "PreToolUse",
    ) -> None:
        if hook_event_name is None:
            monkeypatch.delenv("HOOK_EVENT_NAME", raising=False)
        else:
            monkeypatch.setenv("HOOK_EVENT_NAME", hook_event_name)
        monkeypatch.setattr(sys, "stdin", StringIO(json.dumps(payload)))
        monkeypatch.setattr(hook_dispatch.flow_spool, "spool_append", lambda *_: None)
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *_, **__: None)
        with patch.object(sys, "argv", ["aiwatch", "--client", "cline-cli"]):
            hook_dispatch.run_hook()

    def test_cline_raw_pretooluse_blocks_sensitive_shell_command(
        self, monkeypatch, capsys
    ) -> None:
        payload = {
            "hookName": "tool_call",
            "taskId": "task-123",
            "sessionContext": {"rootSessionId": "session-123"},
            "workspaceRoots": ["/repo"],
            "tool_call": {
                "id": "call-123",
                "name": "run_commands",
                "input": {"command": "cat .env"},
            },
        }
        self._capture_checks(monkeypatch)

        with pytest.raises(SystemExit) as exc:
            self._run_cline_hook(monkeypatch, payload)

        assert exc.value.code == 0
        control = capsys.readouterr().out.strip().split("\t", 1)
        assert control[0] == "HOOK_CONTROL"
        assert json.loads(control[1])["cancel"] is True

    def test_cline_boundary_adapts_flow_session_workspace_and_version(
        self, monkeypatch
    ) -> None:
        payload = {
            "hookName": "tool_call",
            "taskId": "task-123",
            "sessionContext": {"rootSessionId": "session-123"},
            "workspaceRoots": ["/repo"],
            "clineVersion": "3.24.0",
            "tool_call": {
                "id": "call-123",
                "name": "run_commands",
                "input": {"command": "ls"},
            },
        }
        sessions: list[str] = []
        monkeypatch.setattr(hook_dispatch.flow_trace, "set_session_id", sessions.append)
        checks = self._capture_checks(monkeypatch)

        self._run_cline_hook(monkeypatch, payload)

        forwarded = checks[0][4]
        assert sessions == ["session-123"]
        assert forwarded["session_id"] == "session-123"
        assert forwarded["cwd"] == "/repo"
        assert forwarded["client_version"] == "3.24.0"

    def test_cline_raw_post_tool_result_forwards_canonical_payload(
        self, monkeypatch
    ) -> None:
        tool_input = {"command": "pwd"}
        tool_output = {"stdout": "/repo\n", "exitCode": 0}
        payload = {
            "hookName": "tool_result",
            "taskId": "task-123",
            "sessionContext": {"rootSessionId": "session-123"},
            "workspaceRoots": ["/repo"],
            "clineVersion": "3.24.0",
            "tool_result": {
                "id": "call-123",
                "name": "run_commands",
                "input": tool_input,
                "output": tool_output,
            },
        }
        checks = self._capture_checks(monkeypatch)

        self._run_cline_hook(monkeypatch, payload, hook_event_name=None)

        target, client_name, event_name, tool_name, forwarded = checks[0]
        assert (target, client_name, event_name, tool_name) == (
            "tool-post",
            "cline-cli",
            "tool_result",
            "run_commands",
        )
        assert forwarded["session_id"] == "session-123"
        assert forwarded["cwd"] == "/repo"
        assert forwarded["client_version"] == "3.24.0"
        assert forwarded["tool_input"] == tool_input
        assert forwarded["tool_use_id"] == "call-123"
        assert forwarded["tool_output"] == tool_output

    def test_cline_raw_mcp_call_uses_cline_settings(
        self, tmp_path, monkeypatch, capsys
    ) -> None:
        settings = tmp_path / "data" / "settings" / "cline_mcp_settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text(
            json.dumps(
                {"mcpServers": {"linear": {"url": "https://mcp.linear.example/sse"}}}
            )
        )
        payload = {
            "hookName": "tool_call",
            "taskId": "task-123",
            "tool_call": {
                "id": "call-123",
                "name": "linear__search",
                "input": {"query": "status"},
            },
        }
        captured: list[dict[str, object]] = []

        def _fake_enforce(value: str, *, debug: bool = False) -> str:
            captured.append(json.loads(value))
            return '{"permission":"allow"}'

        monkeypatch.setenv("CLINE_DIR", str(tmp_path))
        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)
        monkeypatch.setattr(
            hook_dispatch,
            "check_tool_lifecycle",
            lambda *_, **__: pytest.fail("Cline MCP call used the local-tool path"),
        )

        self._run_cline_hook(monkeypatch, payload)

        assert capsys.readouterr().out == ""
        assert captured[0]["client"] == "cline-cli"
        assert captured[0]["tool_name"] == "linear__search"
        assert captured[0]["url"] == "https://mcp.linear.example/sse"

    def test_cline_unresolved_mcp_shaped_call_fails_closed(
        self, tmp_path, monkeypatch, capsys
    ) -> None:
        payload = {
            "hookName": "tool_call",
            "tool_call": {
                "id": "call-123",
                "name": "missing__search",
                "input": {"query": "status"},
            },
        }
        monkeypatch.setenv("CLINE_DIR", str(tmp_path))
        monkeypatch.setattr(
            hook_dispatch,
            "check_tool_lifecycle",
            lambda *_, **__: pytest.fail("unresolved Cline MCP used local-tool path"),
        )

        with pytest.raises(SystemExit) as exc:
            self._run_cline_hook(monkeypatch, payload)

        assert exc.value.code == 0
        control = capsys.readouterr().out.strip().split("\t", 1)
        assert control[0] == "HOOK_CONTROL"
        assert json.loads(control[1])["cancel"] is True

    def test_cline_unresolved_hashed_mcp_shape_fails_closed(
        self, tmp_path, monkeypatch, capsys
    ) -> None:
        payload = {
            "hookName": "tool_call",
            "tool_call": {
                "id": "call-123",
                "name": f"{'a' * 55}_1a2b3c4d",
                "input": {"query": "status"},
            },
        }
        monkeypatch.setenv("CLINE_DIR", str(tmp_path))
        monkeypatch.setattr(
            hook_dispatch,
            "check_tool_lifecycle",
            lambda *_, **__: pytest.fail("hashed Cline MCP used local-tool path"),
        )

        with pytest.raises(SystemExit) as exc:
            self._run_cline_hook(monkeypatch, payload)

        assert exc.value.code == 0
        control = capsys.readouterr().out.strip().split("\t", 1)
        assert control[0] == "HOOK_CONTROL"
        assert json.loads(control[1])["cancel"] is True

    def test_cline_builtin_without_separator_uses_local_tool_path(
        self, monkeypatch
    ) -> None:
        payload = {
            "hookName": "tool_call",
            "tool_call": {
                "id": "call-123",
                "name": "run_commands",
                "input": {"command": "ls"},
            },
        }
        monkeypatch.setattr(
            hook_dispatch,
            "enforce",
            lambda *_, **__: pytest.fail("Cline built-in used MCP enforcement"),
        )
        checks = self._capture_checks(monkeypatch)

        self._run_cline_hook(monkeypatch, payload)

        assert checks[0][0] == "tool-pre"
        assert checks[0][3] == "run_commands"

    def test_cline_hook_name_dispatches_without_environment_event(
        self, monkeypatch
    ) -> None:
        payload = {
            "hookName": "tool_call",
            "tool_call": {
                "id": "call-123",
                "name": "run_commands",
                "input": {"command": "ls"},
            },
        }
        checks = self._capture_checks(monkeypatch)

        self._run_cline_hook(monkeypatch, payload, hook_event_name=None)

        assert checks[0][2] == "tool_call"
        assert checks[0][3] == "run_commands"

    def test_hook_relay_targets_include_tool_pre_and_tool_post(self):
        assert relay.HOOK_RELAY_TARGETS["enforce"].timeout == 30
        assert relay.HOOK_RELAY_TARGETS["event"].timeout == 5
        assert "tool-pre" in relay.HOOK_RELAY_TARGETS
        assert "tool-post" in relay.HOOK_RELAY_TARGETS
        assert relay.HOOK_RELAY_TARGETS["tool-pre"].endpoint == (
            "/api/v1/hooks/tool/pre"
        )
        assert relay.HOOK_RELAY_TARGETS["tool-pre"].timeout == 30
        assert relay.HOOK_RELAY_TARGETS["tool-post"].endpoint == (
            "/api/v1/hooks/tool/post"
        )
        assert relay.HOOK_RELAY_TARGETS["tool-post"].timeout == 30

    def test_pretooluse_other_tool_routes_to_tool_pre(self, monkeypatch):
        self._capture_detached(monkeypatch)
        checks = self._capture_checks(monkeypatch)
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={
                "tool_name": "Edit",
                "tool_input": {"file_path": "/tmp/x"},
                "tool_use_id": "edit-1",
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        target, client_name, event_name, tool_name, payload = checks[0]
        assert target == "tool-pre"
        assert client_name == "claude_code"
        assert event_name == "PreToolUse"
        assert tool_name == "Edit"
        assert payload["tool_use_id"] == "edit-1"

    @pytest.mark.parametrize(
        ("raw_event", "tool_info", "expected_tool_name", "expected_tool_input"),
        [
            (
                "pre_run_command",
                {"command_line": "echo safe"},
                "BeforeShellExecution",
                {"command": "echo safe"},
            ),
            (
                "pre_read_code",
                {"file_path": "/repo/README.md"},
                "BeforeReadFile",
                {"file_path": "/repo/README.md"},
            ),
        ],
    )
    def test_windsurf_local_pre_hooks_honor_tool_scanner_denial(
        self,
        monkeypatch,
        capsys,
        raw_event,
        tool_info,
        expected_tool_name,
        expected_tool_input,
    ):
        self._capture_detached(monkeypatch)
        checks = self._capture_checks(
            monkeypatch,
            response='{"permission":"deny","block_reason":"blocked by org policy"}',
        )
        input_data = adapt_windsurf_payload(
            {
                "agent_action_name": raw_event,
                "trajectory_id": "traj-1",
                "tool_info": tool_info,
            }
        )

        with pytest.raises(SystemExit) as exc:
            hook_dispatch._dispatch(
                hook_type=normalize_event_name(raw_event),
                original_hook_type=raw_event,
                client=Client.WINDSURF,
                resp=HookResponse(Client.WINDSURF, raw_event),
                input_data=input_data,
                raw_input=json.dumps(input_data),
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert exc.value.code == 2
        target, client_name, event_name, tool_name, payload = checks[0]
        assert (target, client_name, event_name) == (
            "tool-pre",
            "windsurf",
            raw_event,
        )
        assert tool_name == expected_tool_name
        assert payload["tool_input"] == expected_tool_input
        assert "blocked by org policy" in capsys.readouterr().err

    def test_hermes_mcp_pretooluse_enforces_configured_url(
        self, monkeypatch, tmp_path: Path
    ):
        captured_events = self._capture_detached(monkeypatch)
        captured_enforce: list[dict] = []

        hermes_config = tmp_path / ".hermes" / "config.yaml"
        hermes_config.parent.mkdir()
        hermes_config.write_text(
            "mcp_servers:\n  linear-44:\n    url: https://mcp.example.com/sse\n"
        )

        def _fake_enforce(payload: str, *, debug: bool) -> str:
            captured_enforce.append(json.loads(payload))
            return '{"permission":"allow"}'

        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)

        with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=tmp_path):
            hook_dispatch._handle_pre_tool_use(
                client=Client.HERMES,
                resp=HookResponse(Client.HERMES, "pre_tool_call"),
                input_data={
                    "tool_name": "mcp_linear_44_list_issues",
                    "tool_input": {"query": "runlayer"},
                    "session_id": "session-123",
                },
                original_hook_type="pre_tool_call",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert captured_enforce[0]["client"] == "hermes"
        assert captured_enforce[0]["url"] == "https://mcp.example.com/sse"
        assert captured_enforce[0]["tool_name"] == "mcp_linear_44_list_issues"
        assert json.loads(captured_events[0][1])["event_name"] == "pre_tool_call"

    def test_hermes_mcp_pretooluse_observational_writes_nothing(
        self, monkeypatch, capsys, tmp_path: Path
    ):
        """Monitor preserves the generic-event-only MCP path."""
        captured = self._capture_detached(monkeypatch)

        def _unexpected_enforce(*args, **kwargs):
            pytest.fail("monitoring mode must not call /enforce")

        monkeypatch.setattr(hook_dispatch, "enforce", _unexpected_enforce)

        hermes_config = tmp_path / ".hermes" / "config.yaml"
        hermes_config.parent.mkdir()
        hermes_config.write_text(
            "mcp_servers:\n  linear-44:\n    url: https://mcp.example.com/sse\n"
        )

        with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=tmp_path):
            hook_dispatch._handle_pre_tool_use(
                client=Client.HERMES,
                resp=HookResponse(Client.HERMES, "pre_tool_call"),
                input_data={
                    "tool_name": "mcp_linear_44_list_issues",
                    "tool_input": {"query": "x"},
                },
                original_hook_type="pre_tool_call",
                mode=AIWatchMode.MONITOR,
                debug=False,
            )

        assert [target for target, _ in captured] == ["event"]
        assert capsys.readouterr().out == ""

    def test_claude_mcp_pretooluse_observational_writes_allow(
        self, monkeypatch, capsys
    ):
        """Observational-mode Claude Code mcp__* PreToolUse must mirror the
        enforce path and call ``_write(resp.allow())`` (None for Claude → no
        bytes, but stays symmetric with enforce-branch output)."""
        self._capture_detached(monkeypatch)

        def _unexpected_enforce(*args, **kwargs):
            pytest.fail("monitoring mode must not call /enforce")

        monkeypatch.setattr(hook_dispatch, "enforce", _unexpected_enforce)

        hook_dispatch._handle_pre_tool_use(
            client=Client.CLAUDE_CODE,
            resp=HookResponse(Client.CLAUDE_CODE, "PreToolUse"),
            input_data={
                "tool_name": "mcp__github__list_issues",
                "tool_input": {"owner": "x"},
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.MONITOR,
            debug=False,
        )

        assert capsys.readouterr().out == ""

    def test_posttooluse_routes_to_tool_post(self, monkeypatch):
        self._capture_detached(monkeypatch)
        checks = self._capture_checks(monkeypatch, response='{"blocked":false}')
        resp = HookResponse(Client.CLAUDE_CODE, "PostToolUse")
        hook_dispatch._dispatch(
            hook_type="PostToolUse",
            original_hook_type="PostToolUse",
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={"tool_name": "Edit", "tool_response": {"ok": True}},
            raw_input="{}",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        target, client_name, event_name, tool_name, payload = checks[0]
        assert target == "tool-post"
        assert client_name == "claude_code"
        assert event_name == "PostToolUse"
        assert tool_name == "Edit"
        assert payload["tool_response"] == {"ok": True}

    def test_hermes_post_tool_call_is_monitoring_only(self, monkeypatch):
        captured = self._capture_detached(monkeypatch)

        def _unexpected_sync_check(*args, **kwargs):
            pytest.fail("Hermes post_tool_call return values are ignored")

        monkeypatch.setattr(
            hook_dispatch, "check_tool_lifecycle", _unexpected_sync_check
        )
        resp = HookResponse(Client.HERMES, "post_tool_call")
        hook_dispatch._dispatch(
            hook_type="PostToolUse",
            original_hook_type="post_tool_call",
            client=Client.HERMES,
            resp=resp,
            input_data={"tool_name": "write_file", "result": "ok"},
            raw_input="{}",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert [target for target, _ in captured] == ["tool-post", "event"]
        wrapper = json.loads(captured[0][1])
        assert wrapper["client"] == "hermes"
        assert wrapper["event_name"] == "post_tool_call"

    def test_hermes_transform_tool_result_blocks_with_replacement_string(
        self, monkeypatch, capsys
    ):
        self._capture_detached(monkeypatch)
        self._capture_checks(
            monkeypatch,
            response='{"blocked":true,"block_reason":"output blocked"}',
        )
        resp = HookResponse(Client.HERMES, "transform_tool_result")
        hook_dispatch._dispatch(
            hook_type="PostToolUse",
            original_hook_type="transform_tool_result",
            client=Client.HERMES,
            resp=resp,
            input_data={"tool_name": "read_file", "result": "secret"},
            raw_input="{}",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert json.loads(capsys.readouterr().out) == "output blocked"

    def test_cursor_stop_forwards_synthetic_session_end(self, monkeypatch, capsys):
        captured = self._capture_detached(monkeypatch)
        resp = HookResponse(Client.CURSOR, "Stop")
        hook_dispatch._dispatch(
            hook_type="Stop",
            original_hook_type="stop",
            client=Client.CURSOR,
            resp=resp,
            input_data={"session_id": "s1", "status": "aborted"},
            raw_input="{}",
            mode=AIWatchMode.MONITOR,
            debug=False,
        )

        assert json.loads(capsys.readouterr().out) == {"permission": "allow"}
        assert [target for target, _ in captured] == ["event", "event"]
        stop_wrapper = json.loads(captured[0][1])
        end_wrapper = json.loads(captured[1][1])
        assert stop_wrapper["event_name"] == "stop"
        assert end_wrapper["event_name"] == "sessionEnd"
        assert end_wrapper["payload"]["hook_event_name"] == "sessionEnd"
        assert end_wrapper["payload"]["reason"] == "aborted"

    def test_cursor_cli_stop_without_cursor_version_ends_session(
        self, monkeypatch, capsys
    ) -> None:
        captured = self._capture_detached(monkeypatch)
        payload = {
            "hook_event_name": "stop",
            "session_id": "cursor-cli-1",
            "status": "completed",
        }
        env = {
            key: value
            for key, value in os.environ.items()
            if key not in {"CURSOR_VERSION", "HOOK_EVENT_NAME", "RUNLAYER_HOOK_CLIENT"}
        }
        monkeypatch.setattr(sys, "stdin", StringIO(json.dumps(payload)))
        monkeypatch.setattr(hook_dispatch.flow_spool, "spool_append", lambda *_: None)

        with (
            patch.dict(os.environ, env, clear=True),
            patch.object(sys, "argv", ["aiwatch", "--client", "cursor"]),
        ):
            hook_dispatch.run_hook()

        assert json.loads(capsys.readouterr().out) == {"permission": "allow"}
        assert [target for target, _ in captured] == ["event", "event"]
        stop_wrapper = json.loads(captured[0][1])
        end_wrapper = json.loads(captured[1][1])
        assert stop_wrapper["event_name"] == "stop"
        assert end_wrapper["event_name"] == "sessionEnd"
        assert end_wrapper["payload"]["reason"] == "completed"

    def test_pretooluse_no_enforcement_still_forwards_tool_pre(self, monkeypatch):
        captured = self._capture_detached(monkeypatch)

        def _unexpected_sync_check(*args, **kwargs):
            pytest.fail("monitoring mode should not synchronously enforce tool-pre")

        monkeypatch.setattr(
            hook_dispatch, "check_tool_lifecycle", _unexpected_sync_check
        )
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={
                "tool_name": "Edit",
                "tool_input": {"file_path": "/tmp/x"},
                "tool_use_id": "edit-1",
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.MONITOR,
            debug=False,
        )

        assert [target for target, _ in captured] == ["tool-pre", "event"]
        wrapper = json.loads(captured[0][1])
        assert wrapper["client"] == "claude_code"
        assert wrapper["event_name"] == "PreToolUse"
        assert wrapper["tool_name"] == "Edit"
        assert wrapper["payload"]["tool_use_id"] == "edit-1"

    def test_posttooluse_no_enforcement_still_forwards_tool_post(self, monkeypatch):
        captured = self._capture_detached(monkeypatch)

        def _unexpected_sync_check(*args, **kwargs):
            pytest.fail("monitoring mode should not synchronously enforce tool-post")

        monkeypatch.setattr(
            hook_dispatch, "check_tool_lifecycle", _unexpected_sync_check
        )
        resp = HookResponse(Client.CLAUDE_CODE, "PostToolUse")
        hook_dispatch._dispatch(
            hook_type="PostToolUse",
            original_hook_type="PostToolUse",
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={"tool_name": "Edit", "tool_response": {"ok": True}},
            raw_input="{}",
            mode=AIWatchMode.MONITOR,
            debug=False,
        )

        assert [target for target, _ in captured] == ["tool-post", "event"]
        wrapper = json.loads(captured[0][1])
        assert wrapper["client"] == "claude_code"
        assert wrapper["event_name"] == "PostToolUse"
        assert wrapper["tool_name"] == "Edit"
        assert wrapper["payload"]["tool_response"] == {"ok": True}

    def test_posttooluse_failure_routes_to_tool_post(self, monkeypatch):
        self._capture_detached(monkeypatch)
        checks = self._capture_checks(monkeypatch, response='{"blocked":false}')
        resp = HookResponse(Client.CURSOR, "postToolUseFailure")
        hook_dispatch._dispatch(
            hook_type="PostToolUseFailure",
            original_hook_type="postToolUseFailure",
            client=Client.CURSOR,
            resp=resp,
            input_data={"tool_name": "Bash", "error": "boom"},
            raw_input="{}",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        target, _, event_name, tool_name, payload = checks[0]
        assert target == "tool-post"
        assert event_name == "postToolUseFailure"
        assert tool_name == "Bash"
        assert payload["error"] == "boom"

    def test_pretooluse_read_routes_to_tool_pre(self, monkeypatch):
        """Read tool also needs tool-pre routing — bash hook calls _tool_pre_check
        for ALL non-managed-MCP tools (Read, Bash, generic) after the local checks.
        """
        self._capture_detached(monkeypatch)
        checks = self._capture_checks(monkeypatch)
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={
                "tool_name": "Read",
                "tool_input": {"file_path": "/tmp/safe.txt"},
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )
        assert checks[0][0] == "tool-pre"

    def test_pretooluse_bash_routes_to_tool_pre(self, monkeypatch):
        self._capture_detached(monkeypatch)
        checks = self._capture_checks(monkeypatch)
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={
                "tool_name": "Bash",
                "tool_input": {"command": "ls"},
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )
        assert checks[0][0] == "tool-pre"

    def test_pretooluse_mcp_skips_local_tool_lifecycle(self, monkeypatch):
        captured = self._capture_detached(monkeypatch)
        checks = self._capture_checks(monkeypatch)
        resp = HookResponse(Client.CURSOR, "preToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "tool_name": "mcp__linear44__list_issues",
                "tool_input": {"query": "runlayer"},
            },
            original_hook_type="preToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )
        assert checks == []
        assert "event" in [t for t, _ in captured]

    def test_codex_pretooluse_mcp_enforces_configured_server(
        self, monkeypatch, tmp_path, capsys
    ):
        codex_file = tmp_path / ".codex" / "config.toml"
        codex_file.parent.mkdir()
        codex_file.write_text(
            '[mcp_servers.linear-44]\nurl = "https://mcp.example.com/sse"\n'
        )
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=tmp_path):
            resp = HookResponse(Client.CODEX, "PreToolUse")
            hook_dispatch._handle_pre_tool_use(
                client=Client.CODEX,
                resp=resp,
                input_data={
                    "tool_name": "mcp__linear-44__list_teams",
                    "tool_input": {"limit": 3},
                    "session_id": "session-123",
                    "tool_use_id": "tool-use-456",
                    "cwd": str(tmp_path),
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert capsys.readouterr().out == ""
        assert captured[0]["hook_event_name"] == "beforeMCPExecution"
        assert captured[0]["client"] == "codex"
        assert captured[0]["conversation_id"] == "session-123"
        assert captured[0]["generation_id"] == "tool-use-456"
        assert captured[0]["tool_name"] == "mcp__linear-44__list_teams"
        assert captured[0]["url"] == "https://mcp.example.com/sse"

    def test_claude_pretooluse_mcp_enforces_managed_mcp_json_server(
        self, monkeypatch, tmp_path, capsys
    ):
        """Servers defined only in the enterprise managed-mcp.json must reach
        the backend enforce check with their URL, not local-deny as
        unregistered."""
        managed_file = tmp_path / "managed-mcp.json"
        managed_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "jira": {
                            "type": "http",
                            "url": "https://acme.runlayer.com/api/v1/proxy/7a76c0fc/mcp",
                        }
                    }
                }
            )
        )
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        with (
            patch(
                "runlayer_cli.hook.mcp_lookup.Path.home",
                return_value=tmp_path / "home",
            ),
            patch(
                "runlayer_cli.hook.mcp_lookup._claude_managed_mcp_config_path",
                return_value=managed_file,
            ),
        ):
            resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
            hook_dispatch._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "mcp__jira__getAccessibleAtlassianResources",
                    "tool_input": {},
                    "session_id": "session-123",
                    "tool_use_id": "tool-use-456",
                    "cwd": str(tmp_path),
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert capsys.readouterr().out == ""
        assert captured[0]["hook_event_name"] == "beforeMCPExecution"
        assert captured[0]["client"] == "claude_code"
        assert captured[0]["tool_name"] == "mcp__jira__getAccessibleAtlassianResources"
        assert (
            captured[0]["url"] == "https://acme.runlayer.com/api/v1/proxy/7a76c0fc/mcp"
        )

    def test_goose_pretooluse_extension_tool_enforces_configured_server(
        self, monkeypatch, tmp_path, capsys
    ):
        goose_file = tmp_path / ".config" / "goose" / "config.yaml"
        goose_file.parent.mkdir(parents=True)
        goose_file.write_text(
            "extensions:\n  linear-44:\n    uri: https://mcp.example.com/sse\n"
        )
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        checks = self._capture_checks(monkeypatch)
        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=tmp_path):
            resp = HookResponse(Client.GOOSE, "PreToolUse")
            hook_dispatch._handle_pre_tool_use(
                client=Client.GOOSE,
                resp=resp,
                input_data={
                    "tool_name": "linear-44__search",
                    "tool_input": {"query": "runlayer"},
                    "session_id": "session-123",
                    "tool_use_id": "tool-use-456",
                    "cwd": str(tmp_path),
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert checks == []
        assert capsys.readouterr().out == ""
        assert captured[0]["hook_event_name"] == "beforeMCPExecution"
        assert captured[0]["client"] == "goose"
        assert captured[0]["conversation_id"] == "session-123"
        assert captured[0]["generation_id"] == "tool-use-456"
        assert captured[0]["tool_name"] == "linear-44__search"
        assert captured[0]["url"] == "https://mcp.example.com/sse"

    def test_goose_builtin_developer_shell_uses_local_shell_guard(
        self, monkeypatch, tmp_path, capsys
    ):
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        resp = HookResponse(Client.GOOSE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.GOOSE,
                resp=resp,
                input_data={
                    "tool_name": "developer__shell",
                    "tool_input": {"command": "cat .env"},
                    "cwd": str(tmp_path),
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["decision"] == "block"
        assert "environment files" in out["reason"]
        assert "MCP server" not in out["reason"]

    def test_goose_platform_extension_tool_uses_local_tool_path(
        self, monkeypatch, tmp_path, capsys
    ):
        goose_file = tmp_path / ".config" / "goose" / "config.yaml"
        goose_file.parent.mkdir(parents=True)
        goose_file.write_text(
            "extensions:\n"
            "  todo:\n"
            "    enabled: true\n"
            "    type: platform\n"
            "    name: todo\n"
        )
        checks = self._capture_checks(monkeypatch)
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        monkeypatch.setattr(
            hook_dispatch,
            "enforce",
            lambda *a, **kw: pytest.fail("platform extension used MCP enforcement"),
        )

        with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=tmp_path):
            resp = HookResponse(Client.GOOSE, "PreToolUse")
            hook_dispatch._handle_pre_tool_use(
                client=Client.GOOSE,
                resp=resp,
                input_data={
                    "tool_name": "todo__write",
                    "tool_input": {"item": "ship hooks"},
                    "cwd": str(tmp_path),
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert capsys.readouterr().out == ""
        assert [(target, tool_name) for target, _, _, tool_name, _ in checks] == [
            ("tool-pre", "todo__write")
        ]

    def test_vscode_pretooluse_mcp_enforces_configured_server(
        self, monkeypatch, tmp_path, capsys
    ):
        vscode_file = tmp_path / ".vscode" / "mcp.json"
        vscode_file.parent.mkdir()
        vscode_file.write_text(
            json.dumps(
                {
                    "servers": {
                        "linear-44": {"url": "https://mcp.example.com/sse"},
                    }
                }
            )
        )
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        resp = HookResponse(Client.VSCODE, "PreToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.VSCODE,
            resp=resp,
            input_data={
                "tool_name": "mcp__linear-44__list_teams",
                "tool_input": {"limit": 3},
                "session_id": "session-123",
                "tool_use_id": "tool-use-456",
                "cwd": str(tmp_path),
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert capsys.readouterr().out == ""
        assert captured[0]["hook_event_name"] == "beforeMCPExecution"
        assert captured[0]["client"] == "vscode"
        assert captured[0]["conversation_id"] == "session-123"
        assert captured[0]["generation_id"] == "tool-use-456"
        assert captured[0]["tool_name"] == "mcp__linear-44__list_teams"
        assert captured[0]["url"] == "https://mcp.example.com/sse"

    def test_github_copilot_cli_mcp_server_name_prefix_enforces_configured_server(
        self, monkeypatch, tmp_path, capsys
    ):
        copilot_file = tmp_path / ".github" / "mcp.json"
        copilot_file.parent.mkdir()
        copilot_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "github-mcp-server": {"url": "https://mcp.github.example/sse"},
                    }
                }
            )
        )
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        resp = HookResponse(Client.GITHUB_COPILOT_CLI, "PreToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.GITHUB_COPILOT_CLI,
            resp=resp,
            input_data={
                "tool_name": "github-mcp-server-list_repos",
                "tool_input": {"owner": "runlayer"},
                "session_id": "session-123",
                "tool_use_id": "tool-use-456",
                "cwd": str(tmp_path),
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert capsys.readouterr().out == ""
        assert captured[0]["hook_event_name"] == "beforeMCPExecution"
        assert captured[0]["client"] == "github-copilot-cli"
        assert captured[0]["conversation_id"] == "session-123"
        assert captured[0]["generation_id"] == "tool-use-456"
        assert captured[0]["tool_name"] == "github-mcp-server-list_repos"
        assert captured[0]["url"] == "https://mcp.github.example/sse"

    def test_github_copilot_cli_builtin_mcp_server_enforces_without_config(
        self, monkeypatch, tmp_path, capsys
    ):
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        resp = HookResponse(Client.GITHUB_COPILOT_CLI, "PreToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.GITHUB_COPILOT_CLI,
            resp=resp,
            input_data={
                "tool_name": "github-mcp-server-list_repos",
                "tool_input": {"owner": "runlayer"},
                "session_id": "session-123",
                "tool_use_id": "tool-use-456",
                "cwd": str(tmp_path),
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert capsys.readouterr().out == ""
        assert captured[0]["hook_event_name"] == "beforeMCPExecution"
        assert captured[0]["client"] == "github-copilot-cli"
        assert captured[0]["tool_name"] == "github-mcp-server-list_repos"
        assert captured[0]["mcp_server_name"] == "github-mcp-server"
        assert captured[0]["mcp_server_source"] == "github-copilot-cli-built-in"
        assert "url" not in captured[0]
        assert "command" not in captured[0]

    def test_source_tagged_mcp_server_without_name_fails_closed(
        self, monkeypatch, tmp_path, capsys
    ):
        def _unexpected_enforce(*args, **kwargs):
            pytest.fail("invalid source-tagged server reached backend enforcement")

        monkeypatch.setattr(
            hook_dispatch,
            "lookup_mcp_server",
            lambda server_name, cwd: {"source": "future-source"},
        )
        monkeypatch.setattr(hook_dispatch, "enforce", _unexpected_enforce)
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)

        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=HookResponse(Client.CLAUDE_CODE, "PreToolUse"),
                input_data={
                    "tool_name": "mcp__future__do_thing",
                    "tool_input": {},
                    "cwd": str(tmp_path),
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert exc.value.code == 0
        output = json.loads(capsys.readouterr().out)
        assert output["hookSpecificOutput"]["permissionDecision"] == "deny"
        assert (
            "Failed to prepare"
            in output["hookSpecificOutput"]["permissionDecisionReason"]
        )

    def test_github_copilot_cli_hyphenated_local_name_collision_enforces_mcp(
        self, monkeypatch, tmp_path, capsys
    ):
        copilot_file = tmp_path / ".github" / "mcp.json"
        copilot_file.parent.mkdir()
        copilot_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "web": {"url": "https://mcp.web.example/sse"},
                    }
                }
            )
        )
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        def _unexpected_tool_lifecycle(*args, **kwargs):
            raise AssertionError("hyphenated Copilot MCP tool used local path")

        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)
        monkeypatch.setattr(
            hook_dispatch, "check_tool_lifecycle", _unexpected_tool_lifecycle
        )
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        resp = HookResponse(Client.GITHUB_COPILOT_CLI, "PreToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.GITHUB_COPILOT_CLI,
            resp=resp,
            input_data={
                "tool_name": "web-fetch",
                "tool_input": {"url": "https://example.com"},
                "session_id": "session-123",
                "tool_use_id": "tool-use-456",
                "cwd": str(tmp_path),
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert capsys.readouterr().out == ""
        assert captured[0]["hook_event_name"] == "beforeMCPExecution"
        assert captured[0]["client"] == "github-copilot-cli"
        assert captured[0]["tool_name"] == "web-fetch"
        assert captured[0]["url"] == "https://mcp.web.example/sse"

    def test_github_copilot_cli_unresolved_mcp_shaped_tool_fails_closed(
        self, monkeypatch, tmp_path, capsys
    ):
        def _unexpected_tool_lifecycle(*args, **kwargs):
            raise AssertionError("unresolved Copilot MCP-shaped tool used local path")

        monkeypatch.setattr(
            hook_dispatch, "check_tool_lifecycle", _unexpected_tool_lifecycle
        )
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        resp = HookResponse(Client.GITHUB_COPILOT_CLI, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.GITHUB_COPILOT_CLI,
                resp=resp,
                input_data={
                    "tool_name": "session-only-search",
                    "tool_input": {"value": "x"},
                    "session_id": "session-123",
                    "tool_use_id": "tool-use-456",
                    "cwd": str(tmp_path),
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert exc.value.code == 0
        output = capsys.readouterr().out
        assert "deny" in output
        assert "session-only-search" in output

    def test_gemini_cli_mcp_tool_enforces_configured_server(
        self, monkeypatch, tmp_path, capsys
    ):
        settings = tmp_path / "project" / ".gemini" / "settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text(
            json.dumps(
                {"mcpServers": {"linear-44": {"url": "https://mcp.example.com/sse"}}}
            )
        )
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        def _unexpected_tool_lifecycle(*args, **kwargs):
            raise AssertionError("configured Gemini MCP tool used the local-tool path")

        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)
        monkeypatch.setattr(
            hook_dispatch, "check_tool_lifecycle", _unexpected_tool_lifecycle
        )
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        monkeypatch.setattr(
            mcp_lookup.Path, "home", classmethod(lambda cls: tmp_path / "home")
        )
        resp = HookResponse(Client.GEMINI_CLI, "PreToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.GEMINI_CLI,
            resp=resp,
            input_data={
                "tool_name": "mcp_linear_44_list_issues",
                "tool_input": {"limit": 3},
                "session_id": "session-123",
                "tool_use_id": "tool-use-456",
                "cwd": str(tmp_path / "project"),
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert capsys.readouterr().out == ""
        assert captured[0]["client"] == "gemini-cli"
        assert captured[0]["tool_name"] == "mcp_linear_44_list_issues"
        assert captured[0]["url"] == "https://mcp.example.com/sse"

    @pytest.mark.parametrize(
        ("tool_name", "connection", "expected_field", "expected_value"),
        [
            (
                "list_issues",
                {"url": "https://mcp.example.com/sse"},
                "url",
                "https://mcp.example.com/sse",
            ),
            (
                "linear__list_issues",
                {"tcp": "wss://mcp.example.com/socket"},
                "url",
                "wss://mcp.example.com/socket",
            ),
            (
                "list_issues",
                {"httpUrl": "https://mcp.example.com/mcp"},
                "url",
                "https://mcp.example.com/mcp",
            ),
            (
                "list_issues",
                {"command": "runlayer", "args": ["run", "server-123"]},
                "command",
                "runlayer run server-123",
            ),
        ],
    )
    def test_gemini_cli_mcp_tool_enforces_hook_context_connection(
        self,
        monkeypatch,
        capsys,
        tool_name,
        connection,
        expected_field,
        expected_value,
    ):
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        def _unexpected_tool_lifecycle(*args, **kwargs):
            raise AssertionError("Gemini MCP tool used the local-tool path")

        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)
        monkeypatch.setattr(
            hook_dispatch, "check_tool_lifecycle", _unexpected_tool_lifecycle
        )
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        hook_dispatch._handle_pre_tool_use(
            client=Client.GEMINI_CLI,
            resp=HookResponse(Client.GEMINI_CLI, "PreToolUse"),
            input_data={
                "tool_name": tool_name,
                "tool_input": {"limit": 3},
                "session_id": "session-123",
                "mcp_context": {
                    "server_name": "linear",
                    "tool_name": "list_issues",
                    **connection,
                },
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert capsys.readouterr().out == ""
        assert captured[0]["client"] == "gemini-cli"
        assert captured[0]["tool_name"] == tool_name
        assert captured[0]["mcp_server_name"] == "linear"
        assert captured[0][expected_field] == expected_value

    def test_gemini_cli_unregistered_mcp_shaped_tool_denies_naming_settings(
        self, monkeypatch, tmp_path, capsys
    ):
        def _unexpected_tool_lifecycle(*args, **kwargs):
            raise AssertionError("unresolved Gemini MCP-shaped tool used local path")

        monkeypatch.setattr(
            hook_dispatch, "check_tool_lifecycle", _unexpected_tool_lifecycle
        )
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        monkeypatch.setattr(
            mcp_lookup.Path, "home", classmethod(lambda cls: tmp_path / "home")
        )
        resp = HookResponse(Client.GEMINI_CLI, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.GEMINI_CLI,
                resp=resp,
                input_data={
                    "tool_name": "mcp_ghost_list_issues",
                    "tool_input": {"value": "x"},
                    "session_id": "session-123",
                    "cwd": str(tmp_path / "project"),
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert exc.value.code == 0
        output = json.loads(capsys.readouterr().out)
        assert output["decision"] == "deny"
        assert "mcp_ghost_list_issues" in output["reason"]
        assert "Gemini CLI settings" in output["reason"]

    def test_github_copilot_cli_truncated_mcp_server_name_enforces_configured_server(
        self, monkeypatch, tmp_path, capsys
    ):
        copilot_file = tmp_path / ".github" / "mcp.json"
        copilot_file.parent.mkdir()
        server_name = "a" * 70
        tool_name = "a" * 64
        copilot_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        server_name: {"url": "https://mcp.long.example/sse"},
                    }
                }
            )
        )
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        def _unexpected_tool_lifecycle(*args, **kwargs):
            raise AssertionError("truncated Copilot MCP tool used local path")

        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)
        monkeypatch.setattr(
            hook_dispatch, "check_tool_lifecycle", _unexpected_tool_lifecycle
        )
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        resp = HookResponse(Client.GITHUB_COPILOT_CLI, "PreToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.GITHUB_COPILOT_CLI,
            resp=resp,
            input_data={
                "tool_name": tool_name,
                "tool_input": {"query": "repo:runlayer/Runlayer"},
                "session_id": "session-123",
                "tool_use_id": "tool-use-456",
                "cwd": str(tmp_path),
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert capsys.readouterr().out == ""
        assert captured[0]["hook_event_name"] == "beforeMCPExecution"
        assert captured[0]["client"] == "github-copilot-cli"
        assert captured[0]["tool_name"] == tool_name
        assert captured[0]["url"] == "https://mcp.long.example/sse"

    def test_github_copilot_cli_installed_plugin_mcp_server_enforces_configured_server(
        self, monkeypatch, tmp_path, capsys
    ):
        plugin_dir = tmp_path / ".copilot" / "installed-plugins" / "work-iq" / "workiq"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / ".mcp.json").write_text(
            json.dumps(
                {"mcpServers": {"workiq": {"url": "https://mcp.workiq.example/sse"}}}
            )
        )
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        resp = HookResponse(Client.GITHUB_COPILOT_CLI, "PreToolUse")
        with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=tmp_path):
            hook_dispatch._handle_pre_tool_use(
                client=Client.GITHUB_COPILOT_CLI,
                resp=resp,
                input_data={
                    "tool_name": "workiq-search",
                    "tool_input": {"query": "status"},
                    "session_id": "session-123",
                    "tool_use_id": "tool-use-456",
                    "cwd": str(tmp_path / "repo"),
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert capsys.readouterr().out == ""
        assert captured[0]["hook_event_name"] == "beforeMCPExecution"
        assert captured[0]["client"] == "github-copilot-cli"
        assert captured[0]["tool_name"] == "workiq-search"
        assert captured[0]["url"] == "https://mcp.workiq.example/sse"

    def test_github_copilot_cli_session_mcp_server_enforces_configured_server(
        self, monkeypatch, tmp_path, capsys
    ):
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        def _unexpected_tool_lifecycle(*args, **kwargs):
            raise AssertionError("session Copilot MCP tool used local path")

        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)
        monkeypatch.setattr(
            hook_dispatch, "check_tool_lifecycle", _unexpected_tool_lifecycle
        )
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        resp = HookResponse(Client.GITHUB_COPILOT_CLI, "PreToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.GITHUB_COPILOT_CLI,
            resp=resp,
            input_data={
                "tool_name": "session-only-search",
                "tool_input": {"query": "status"},
                "session_id": "session-123",
                "tool_use_id": "tool-use-456",
                "cwd": str(tmp_path),
                "additional_mcp_config": json.dumps(
                    {
                        "mcpServers": {
                            "session-only": {"url": "https://session.example/sse"}
                        }
                    }
                ),
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert capsys.readouterr().out == ""
        assert captured[0]["hook_event_name"] == "beforeMCPExecution"
        assert captured[0]["client"] == "github-copilot-cli"
        assert captured[0]["tool_name"] == "session-only-search"
        assert captured[0]["url"] == "https://session.example/sse"

    def test_github_copilot_cli_session_mcp_unresolved_tool_denies(
        self, monkeypatch, tmp_path, capsys
    ):
        def _unexpected_tool_lifecycle(*args, **kwargs):
            raise AssertionError("unresolved session Copilot MCP tool used local path")

        monkeypatch.setattr(
            hook_dispatch, "check_tool_lifecycle", _unexpected_tool_lifecycle
        )
        resp = HookResponse(Client.GITHUB_COPILOT_CLI, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.GITHUB_COPILOT_CLI,
                resp=resp,
                input_data={
                    "tool_name": "missing-server-search",
                    "tool_input": {"query": "status"},
                    "session_id": "session-123",
                    "tool_use_id": "tool-use-456",
                    "cwd": str(tmp_path),
                    "additional_mcp_config": json.dumps(
                        {
                            "mcpServers": {
                                "session-only": {"url": "https://session.example/sse"}
                            }
                        }
                    ),
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["permissionDecision"] == "deny"
        assert "missing-server" in out["permissionDecisionReason"]

    def test_tool_pre_deny_blocks(self, monkeypatch, capsys):
        self._capture_detached(monkeypatch)
        self._capture_checks(
            monkeypatch,
            response='{"permission":"deny","block_reason":"pii detected"}',
        )
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "Edit",
                    "tool_input": {"file_path": "/tmp/x"},
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
        assert "pii detected" in out["hookSpecificOutput"]["permissionDecisionReason"]

    def test_tool_pre_scan_unavailable_denies_with_retryable_message(
        self, monkeypatch, capsys
    ):
        """block_state=scan_unavailable renders a retryable infra message —
        not a security violation, and without the do-not-retry directive."""
        self._capture_detached(monkeypatch)
        self._capture_checks(
            monkeypatch,
            response=json.dumps(
                {
                    "permission": "deny",
                    "block_reason": "A required security scan did not complete in time",
                    "block_state": "scan_unavailable",
                }
            ),
        )
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "Bash",
                    "tool_input": {"command": "echo hi"},
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
        reason = out["hookSpecificOutput"]["permissionDecisionReason"]
        assert "Security Scan Unavailable" in reason
        assert "retry" in reason.lower()
        assert "Security Violation Detected" not in reason
        assert "Do not retry" not in reason

    def test_tool_pre_relay_auth_failure_forwards_event_before_deny(
        self, monkeypatch, capsys
    ):
        captured = self._capture_detached(monkeypatch)

        def _raise_auth_failure(*args, **kwargs):
            raise relay.RelayError(1, "no secret")

        monkeypatch.setattr(hook_dispatch, "check_tool_lifecycle", _raise_auth_failure)
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "Edit",
                    "tool_input": {"file_path": "/tmp/x"},
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
        assert "runlayer login" in out["hookSpecificOutput"]["permissionDecisionReason"]
        assert [target for target, _ in captured] == ["event"]
        wrapper = json.loads(captured[0][1])
        assert wrapper["event_name"] == "PreToolUse"
        assert wrapper["payload"]["tool_input"] == {"file_path": "/tmp/x"}

    def test_tool_pre_relay_auth_failure_schedules_deferred_event_before_deny(
        self, monkeypatch, capsys
    ):
        """Daemon-served variant: with the deferred sender installed the event
        is queued (not posted inline) before the deny is written."""
        captured = self._capture_detached(monkeypatch)
        queued: list = []
        monkeypatch.setattr(
            relay,
            "_deferred_event_sender",
            lambda send: queued.append(send) or True,
        )
        monkeypatch.setattr(
            relay,
            "_load_credentials",
            lambda: ("https://api.example.com", "rl_org_test"),
        )

        def _raise_auth_failure(*args, **kwargs):
            raise relay.RelayError(1, "no secret")

        monkeypatch.setattr(hook_dispatch, "check_tool_lifecycle", _raise_auth_failure)
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "Edit",
                    "tool_input": {"file_path": "/tmp/x"},
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
        # Event was scheduled on the deferred queue before the deny; the sync
        # forward path was never used.
        assert captured == []
        assert len(queued) == 1
        posts: list[tuple] = []
        monkeypatch.setattr(
            relay,
            "_post",
            lambda *args, **kwargs: posts.append((args, kwargs)) or "",
        )
        queued[0]()
        (_host, _secret, payload), kwargs = posts[0]
        assert kwargs["target"] == "event"
        assert kwargs["prepared"] is True
        wrapper = json.loads(payload)
        assert wrapper["event_name"] == "PreToolUse"
        assert wrapper["payload"]["tool_input"] == {"file_path": "/tmp/x"}

    def test_tool_pre_scalar_json_response_denies(self, monkeypatch, capsys):
        self._capture_detached(monkeypatch)
        self._capture_checks(monkeypatch, response="null")
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "Edit",
                    "tool_input": {"file_path": "/tmp/x"},
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
        assert (
            "invalid response"
            in out["hookSpecificOutput"]["permissionDecisionReason"].lower()
        )

    @pytest.mark.parametrize(
        "response",
        ['{"permission":null}', '{"permission":"ask"}', '{"permission":true}'],
    )
    def test_tool_pre_malformed_permission_denies(self, monkeypatch, capsys, response):
        self._capture_detached(monkeypatch)
        self._capture_checks(monkeypatch, response=response)
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "Edit",
                    "tool_input": {"file_path": "/tmp/x"},
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
        assert (
            "invalid response"
            in out["hookSpecificOutput"]["permissionDecisionReason"].lower()
        )

    def test_cursor_tool_pre_preserves_modified_args_without_session(
        self, monkeypatch, capsys
    ):
        self._capture_detached(monkeypatch)
        modified_args = {"file_path": "/tmp/x", "content": "[REDACTED]"}
        self._capture_checks(
            monkeypatch,
            response=json.dumps(
                {"permission": "allow", "modified_args": modified_args}
            ),
        )
        resp = HookResponse(Client.CURSOR, "preToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "tool_name": "Edit",
                "tool_input": {"file_path": "/tmp/x", "content": "secret"},
            },
            original_hook_type="preToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        out = json.loads(capsys.readouterr().out)
        assert out == {"permission": "allow", "updated_input": modified_args}

    def test_vscode_tool_pre_preserves_modified_args(self, monkeypatch, capsys):
        self._capture_detached(monkeypatch)
        modified_args = {"command": "echo [REDACTED]"}
        self._capture_checks(
            monkeypatch,
            response=json.dumps(
                {"permission": "allow", "modified_args": modified_args}
            ),
        )
        resp = HookResponse(Client.VSCODE, "PreToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.VSCODE,
            resp=resp,
            input_data={
                "tool_name": "runTerminalCommand",
                "tool_input": {"command": "echo secret"},
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"] == {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "updatedInput": modified_args,
        }

    def test_qwen_tool_pre_denies_modified_args_it_cannot_apply(
        self, monkeypatch, capsys
    ):
        self._capture_detached(monkeypatch)
        modified_args = {"command": "echo [REDACTED]"}
        self._capture_checks(
            monkeypatch,
            response=json.dumps(
                {"permission": "allow", "modified_args": modified_args}
            ),
        )
        resp = HookResponse(Client.QWEN_CODE, "PreToolUse")

        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.QWEN_CODE,
                resp=resp,
                input_data={
                    "tool_name": "run_shell_command",
                    "tool_input": {"command": "echo secret"},
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
        assert (
            "cannot apply Runlayer input redactions"
            in out["hookSpecificOutput"]["permissionDecisionReason"]
        )

    def test_github_copilot_cli_tool_pre_preserves_modified_args(
        self, monkeypatch, capsys
    ):
        self._capture_detached(monkeypatch)
        modified_args = {"command": "echo [REDACTED]"}
        self._capture_checks(
            monkeypatch,
            response=json.dumps(
                {"permission": "allow", "modified_args": modified_args}
            ),
        )
        resp = HookResponse(Client.GITHUB_COPILOT_CLI, "PreToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.GITHUB_COPILOT_CLI,
            resp=resp,
            input_data={
                "tool_name": "runTerminalCommand",
                "tool_input": {"command": "echo secret"},
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        out = json.loads(capsys.readouterr().out)
        assert out == {
            "permissionDecision": "allow",
            "modifiedArgs": modified_args,
        }

    def test_cursor_tool_pre_uses_transcript_id_as_session(self, monkeypatch, capsys):
        self._capture_detached(monkeypatch)
        self._capture_checks(monkeypatch, response='{"permission":"allow"}')
        resp = HookResponse(Client.CURSOR, "preToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "tool_name": "Edit",
                "transcript_id": "transcript-1",
                "tool_input": {"file_path": "/tmp/x"},
            },
            original_hook_type="preToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        out = json.loads(capsys.readouterr().out)
        assert out["updated_input"]["_runlayer_session_id"] == "transcript-1"

    def test_cursor_mcp_pretooluse_does_not_inject_session_id(
        self, monkeypatch, capsys
    ):
        # Cursor MCP tools are session-linked via beforeMCPExecution; injecting
        # _runlayer_session_id into the MCP args here breaks strict schemas
        # (additionalProperties:false, e.g. Atlassian Jira). Must be bare allow.
        self._capture_detached(monkeypatch)
        resp = HookResponse(Client.CURSOR, "preToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "tool_name": "mcp__linear44__list_issues",
                "chat_id": "chat-1",
                "tool_input": {"query": "runlayer"},
            },
            original_hook_type="preToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        out = json.loads(capsys.readouterr().out)
        assert out == {"permission": "allow"}

    def test_cursor_mcp_colon_prefix_does_not_inject_session_id(
        self, monkeypatch, capsys
    ):
        # Cursor names MCP tools "MCP:<tool>", not mcp__*. These must be treated
        # as MCP tools (no local-tool lifecycle, no _runlayer_session_id
        # injection) — the Atlassian Jira bug reported in the field.
        checks = self._capture_checks(monkeypatch)
        self._capture_detached(monkeypatch)
        resp = HookResponse(Client.CURSOR, "preToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "tool_name": "MCP:searchJiraIssuesUsingJql",
                "chat_id": "chat-1",
                "tool_input": {"jql": "project = RUN"},
            },
            original_hook_type="preToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert checks == []
        out = json.loads(capsys.readouterr().out)
        assert out == {"permission": "allow"}

    def test_tool_post_block_outputs_block_shape(self, monkeypatch, capsys):
        captured = self._capture_detached(monkeypatch)
        self._capture_checks(
            monkeypatch,
            response='{"blocked":true,"block_reason":"output blocked"}',
        )
        resp = HookResponse(Client.CLAUDE_CODE, "PostToolUse")
        hook_dispatch._dispatch(
            hook_type="PostToolUse",
            original_hook_type="PostToolUse",
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={"tool_name": "Edit", "tool_response": {"ok": True}},
            raw_input="{}",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )
        out = json.loads(capsys.readouterr().out)
        # decision:block halts; updatedToolOutput redacts what the model sees.
        assert out["decision"] == "block"
        assert out["reason"] == "output blocked"
        assert out["hookSpecificOutput"]["updatedToolOutput"] == {
            "runlayer_redacted": ("[Runlayer blocked this tool output] output blocked")
        }
        assert '"ok"' not in json.dumps(out["hookSpecificOutput"]["updatedToolOutput"])
        assert [target for target, _ in captured] == ["event"]
        wrapper = json.loads(captured[0][1])
        assert wrapper["event_name"] == "PostToolUse"
        assert wrapper["payload"]["tool_response"] == {"ok": True}

    def test_tool_post_scan_unavailable_blocks_with_retryable_message(
        self, monkeypatch, capsys
    ):
        """block_state=scan_unavailable on a post block swaps the reason for
        the retryable scan-unavailable text instead of a violation claim."""
        self._capture_detached(monkeypatch)
        self._capture_checks(
            monkeypatch,
            response=(
                '{"blocked":true,"block_state":"scan_unavailable",'
                '"scan_results":[{"scanner_name":"hidden_ascii",'
                '"scan_action":"block","error":"boom"}]}'
            ),
        )
        resp = HookResponse(Client.CLAUDE_CODE, "PostToolUse")
        hook_dispatch._dispatch(
            hook_type="PostToolUse",
            original_hook_type="PostToolUse",
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={"tool_name": "Edit", "tool_response": {"ok": True}},
            raw_input="{}",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )
        out = json.loads(capsys.readouterr().out)
        assert out["decision"] == "block"
        assert "retry" in out["reason"].lower()
        assert "not a threat detection" in out["reason"].lower()
        # The raw scanner error must not leak as the block reason.
        assert "boom" not in out["reason"]

    def test_tool_post_mask_outputs_updated_tool_output(self, monkeypatch, capsys):
        """Frozen aiwatch path (MDM/enterprise): non-blocking masked output is
        applied via updatedToolOutput, not dropped."""
        self._capture_detached(monkeypatch)
        self._capture_checks(
            monkeypatch,
            response='{"blocked":false,"modified_output":"SSN [REDACTED]"}',
        )
        resp = HookResponse(Client.CLAUDE_CODE, "PostToolUse")
        hook_dispatch._dispatch(
            hook_type="PostToolUse",
            original_hook_type="PostToolUse",
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={"tool_name": "Bash", "tool_response": {"stdout": "SSN 1"}},
            raw_input="{}",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
        assert out["hookSpecificOutput"]["updatedToolOutput"] == {
            "stdout": "SSN [REDACTED]",
            "stderr": "",
            "interrupted": False,
            "isImage": False,
        }
        assert "decision" not in out  # masked, not blocked — turn continues

    def test_goose_tool_post_mask_blocks_instead_of_reporting_redaction(
        self, monkeypatch, capsys
    ):
        self._capture_detached(monkeypatch)
        self._capture_checks(
            monkeypatch,
            response='{"blocked":false,"modified_output":"SSN [REDACTED]"}',
        )
        resp = HookResponse(Client.GOOSE, "PostToolUse")
        hook_dispatch._dispatch(
            hook_type="PostToolUse",
            original_hook_type="PostToolUse",
            client=Client.GOOSE,
            resp=resp,
            input_data={
                "tool_name": "developer__shell",
                "tool_response": {"stdout": "SSN 123-45-6789"},
            },
            raw_input="{}",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )
        out = json.loads(capsys.readouterr().out)
        assert out == {
            "decision": "block",
            "reason": hook_dispatch._GOOSE_MASK_BLOCK_REASON,
        }

    def test_vscode_tool_post_block_redacts_output(self, monkeypatch, capsys):
        self._capture_detached(monkeypatch)
        self._capture_checks(
            monkeypatch,
            response='{"blocked":true,"block_reason":"output blocked"}',
        )
        resp = HookResponse(Client.VSCODE, "PostToolUse")
        hook_dispatch._dispatch(
            hook_type="PostToolUse",
            original_hook_type="PostToolUse",
            client=Client.VSCODE,
            resp=resp,
            input_data={"tool_name": "editFiles", "tool_response": {"ok": True}},
            raw_input="{}",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        out = json.loads(capsys.readouterr().out)
        assert out["decision"] == "block"
        assert out["reason"] == "output blocked"
        assert (
            out["modifiedResult"]["textResultForLlm"]
            == "[Runlayer blocked this tool output] output blocked"
        )
        assert out["modifiedResult"]["resultType"] == "success"

    def test_vscode_tool_post_mask_outputs_modified_result(self, monkeypatch, capsys):
        self._capture_detached(monkeypatch)
        self._capture_checks(
            monkeypatch,
            response='{"blocked":false,"modified_output":"SSN [REDACTED]"}',
        )
        resp = HookResponse(Client.VSCODE, "PostToolUse")
        hook_dispatch._dispatch(
            hook_type="PostToolUse",
            original_hook_type="PostToolUse",
            client=Client.VSCODE,
            resp=resp,
            input_data={
                "tool_name": "runTerminalCommand",
                "tool_response": {"stdout": "SSN 1"},
            },
            raw_input="{}",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        out = json.loads(capsys.readouterr().out)
        assert out["modifiedResult"] == {
            "resultType": "success",
            "textResultForLlm": "SSN [REDACTED]",
        }
        assert "decision" not in out

    def test_tool_post_failure_is_observational_when_output_cannot_be_replaced(
        self, monkeypatch, capsys
    ):
        """Claude cannot suppress PostToolUseFailure output, so do not claim it did."""
        captured = self._capture_detached(monkeypatch)
        checks = self._capture_checks(
            monkeypatch,
            response='{"blocked":true,"block_reason":"secret in error output"}',
        )
        resp = HookResponse(Client.CLAUDE_CODE, "PostToolUseFailure")
        hook_dispatch._dispatch(
            hook_type="PostToolUseFailure",
            original_hook_type="PostToolUseFailure",
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={"tool_name": "Bash", "tool_response": {"stderr": "secret"}},
            raw_input="{}",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )
        assert checks == []
        assert [target for target, _ in captured] == ["tool-post", "event"]
        assert capsys.readouterr().out == ""

    def test_qwen_tool_post_failure_is_observational(self, monkeypatch, capsys):
        captured = self._capture_detached(monkeypatch)
        checks = self._capture_checks(
            monkeypatch,
            response='{"blocked":true,"block_reason":"secret in error output"}',
        )
        resp = HookResponse(Client.QWEN_CODE, "PostToolUseFailure")
        hook_dispatch._dispatch(
            hook_type="PostToolUseFailure",
            original_hook_type="PostToolUseFailure",
            client=Client.QWEN_CODE,
            resp=resp,
            input_data={
                "tool_name": "run_shell_command",
                "tool_response": {"stderr": "secret"},
            },
            raw_input="{}",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )
        assert checks == []
        assert [target for target, _ in captured] == ["tool-post", "event"]
        assert capsys.readouterr().out == ""

    def test_tool_post_relay_auth_failure_blocks_output_shape(
        self, monkeypatch, capsys
    ):
        captured = self._capture_detached(monkeypatch)

        def _raise_auth_failure(*args, **kwargs):
            raise relay.RelayError(1, "no secret")

        monkeypatch.setattr(hook_dispatch, "check_tool_lifecycle", _raise_auth_failure)
        resp = HookResponse(Client.CLAUDE_CODE, "PostToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._dispatch(
                hook_type="PostToolUse",
                original_hook_type="PostToolUse",
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={"tool_name": "Edit", "tool_response": {"ok": True}},
                raw_input="{}",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["decision"] == "block"
        assert "runlayer login" in out["reason"]
        assert [target for target, _ in captured] == ["event"]
        wrapper = json.loads(captured[0][1])
        assert wrapper["event_name"] == "PostToolUse"
        assert wrapper["payload"]["tool_response"] == {"ok": True}

    @pytest.mark.parametrize("response", ["null", "{}"])
    def test_tool_post_invalid_response_blocks_output_shape(
        self, monkeypatch, capsys, response
    ):
        self._capture_detached(monkeypatch)
        self._capture_checks(monkeypatch, response=response)
        resp = HookResponse(Client.CLAUDE_CODE, "PostToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._dispatch(
                hook_type="PostToolUse",
                original_hook_type="PostToolUse",
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={"tool_name": "Edit", "tool_response": {"ok": True}},
                raw_input="{}",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["decision"] == "block"
        assert "Invalid response from Runlayer API" in out["reason"]

    @pytest.mark.parametrize(
        "response",
        ['{"blocked":"true"}', '{"blocked":null}', '{"blocked":1}'],
    )
    def test_tool_post_malformed_blocked_blocks_output_shape(
        self, monkeypatch, capsys, response
    ):
        self._capture_detached(monkeypatch)
        self._capture_checks(monkeypatch, response=response)
        resp = HookResponse(Client.CLAUDE_CODE, "PostToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._dispatch(
                hook_type="PostToolUse",
                original_hook_type="PostToolUse",
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={"tool_name": "Edit", "tool_response": {"ok": True}},
                raw_input="{}",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["decision"] == "block"
        assert "Invalid response from Runlayer API" in out["reason"]


class TestEndToEndObservational:
    def test_cursor_observational_outputs_empty_object(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps({"hook_event_name": "afterAgentResponse", "data": "test"}),
                config_dir=td,
                enforcement=False,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )
            assert result.returncode == 0
            assert result.stdout.strip() == "{}"

    def test_claude_code_observational_no_stdout(self):
        with tempfile.TemporaryDirectory() as td:
            result = _run_python_hook(
                json.dumps(
                    {
                        "hook_event_name": "PostToolUse",
                        "tool_name": "Write",
                        "tool_input": {},
                    }
                ),
                config_dir=td,
                enforcement=False,
                extra_env={"HOOK_EVENT_NAME": "PostToolUse"},
            )
            assert result.returncode == 0
            assert result.stdout.strip() == ""


class TestStringToolInputFailsClosed:
    """Regression: ``tool_input`` arriving as a JSON string (Codex
    PermissionRequest, some Cursor variants) must not crash the hook.

    A crash exits non-zero without a deny shape on stdout — some clients
    treat that as fail-open, silently bypassing file-policy enforcement.
    The string form must be parsed and enforcement must run as if it were
    a dict.
    """

    def test_pretooluse_read_string_tool_input_blocks_dotenv(self, capsys):
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "Read",
                    "tool_input": json.dumps({"file_path": "/project/.env"}),
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_pretooluse_bash_string_tool_input_blocks_cat_dotenv(self, capsys):
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "Bash",
                    "tool_input": json.dumps({"command": "cat .env"}),
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_grok_cli_terminal_tool_blocks_cat_dotenv(self, capsys):
        resp = HookResponse(Client.GROK_CLI, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.GROK_CLI,
                resp=resp,
                input_data={
                    "tool_name": "run_terminal_cmd",
                    "tool_input": {"command": "cat .env"},
                },
                original_hook_type="pre_tool_use",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert exc.value.code == 2
        assert json.loads(capsys.readouterr().out)["decision"] == "deny"

    def test_grok_cli_double_underscore_tool_is_mcp(self):
        assert hook_dispatch._is_mcp_tool(Client.GROK_CLI, "linear__get_issue")
        assert not hook_dispatch._is_mcp_tool(Client.GROK_CLI, "run_terminal_cmd")

    def test_vscode_read_filepath_blocks_dotenv(self, capsys):
        resp = HookResponse(Client.VSCODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.VSCODE,
                resp=resp,
                input_data={
                    "tool_name": "read_file",
                    "tool_input": {"filePath": "/project/.env"},
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_vscode_run_terminal_command_blocks_cat_dotenv(self, capsys):
        resp = HookResponse(Client.VSCODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.VSCODE,
                resp=resp,
                input_data={
                    "tool_name": "runTerminalCommand",
                    "tool_input": {"command": "cat .env"},
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_gemini_cli_run_shell_command_blocks_cat_dotenv(self, monkeypatch, capsys):
        monkeypatch.setattr(
            hook_dispatch,
            "check_tool_lifecycle",
            lambda *args, **kwargs: '{"permission":"allow","blocked":false}',
        )
        resp = HookResponse(Client.GEMINI_CLI, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.GEMINI_CLI,
                resp=resp,
                input_data={
                    "tool_name": "run_shell_command",
                    "tool_input": {"command": "cat .env"},
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["decision"] == "deny"
        assert "environment files" in out["reason"]

    def test_gemini_cli_read_many_files_blocks_protected_path_in_paths(
        self, monkeypatch, capsys
    ):
        monkeypatch.setattr(
            hook_dispatch,
            "check_tool_lifecycle",
            lambda *args, **kwargs: '{"permission":"allow","blocked":false}',
        )
        resp = HookResponse(Client.GEMINI_CLI, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.GEMINI_CLI,
                resp=resp,
                input_data={
                    "tool_name": "read_many_files",
                    "tool_input": {"paths": ["/project/README.md", "/project/.env"]},
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["decision"] == "deny"
        assert "environment files" in out["reason"]

    def test_gemini_cli_read_many_files_blocks_protected_path_in_include(
        self, monkeypatch, capsys
    ):
        monkeypatch.setattr(
            hook_dispatch,
            "check_tool_lifecycle",
            lambda *args, **kwargs: '{"permission":"allow","blocked":false}',
        )
        resp = HookResponse(Client.GEMINI_CLI, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_pre_tool_use(
                client=Client.GEMINI_CLI,
                resp=resp,
                input_data={
                    "tool_name": "read_many_files",
                    "tool_input": {"include": ["/project/README.md", "/project/.env"]},
                },
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )

        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["decision"] == "deny"
        assert "environment files" in out["reason"]

    def test_codex_permission_request_string_tool_input_blocks_cat_dotenv(
        self, monkeypatch, capsys
    ):
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        resp = HookResponse(Client.CODEX, "PermissionRequest")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._dispatch(
                hook_type="PermissionRequest",
                original_hook_type="PermissionRequest",
                client=Client.CODEX,
                resp=resp,
                input_data={
                    "tool_input": json.dumps({"command": "cat .env"}),
                },
                raw_input="{}",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )
        assert exc.value.code == 0
        out = capsys.readouterr().out
        assert '"deny"' in out or '"decision": "block"' in out or "block" in out

    def test_pretooluse_read_invalid_json_string_does_not_crash(
        self, monkeypatch, capsys
    ):
        """Malformed JSON string in ``tool_input`` must not raise — fall back
        to no enforcement (empty file_path) and continue."""
        captured: list[tuple[str, str]] = []

        def _fake_forward(target, wrapper, *, timeout=None, debug=False):
            captured.append((target, wrapper))

        monkeypatch.setattr(relay, "_forward_post", _fake_forward)
        monkeypatch.setattr(
            hook_dispatch,
            "check_tool_lifecycle",
            lambda *a, **kw: '{"permission":"allow"}',
        )
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        hook_dispatch._handle_pre_tool_use(
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={
                "tool_name": "Read",
                "tool_input": "not-valid-json{",
            },
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )
        assert "event" in [t for t, _ in captured]


class TestCursorBeforeMCPResolution:
    def _capture_enforce(self, monkeypatch) -> list[dict[str, object]]:
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        return captured

    def test_cursor_before_mcp_execution_resolves_command_to_url(
        self, monkeypatch, tmp_path, capsys
    ) -> None:
        cursor_file = tmp_path / ".cursor" / "mcp.json"
        cursor_file.parent.mkdir()
        cursor_file.write_text(
            json.dumps(
                {"mcpServers": {"linear-44": {"url": "https://mcp.example.com/sse"}}}
            )
        )
        captured = self._capture_enforce(monkeypatch)

        resp = HookResponse(Client.CURSOR, "beforeMCPExecution")
        hook_dispatch._handle_before_mcp_execution(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "hook_event_name": "beforeMCPExecution",
                "tool_name": "list_teams",
                "tool_input": {"limit": 3},
                "command": "user-Linear44",
                "workspace_roots": [str(tmp_path)],
            },
            raw_input="{}",
            original_hook_type="beforeMCPExecution",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert json.loads(capsys.readouterr().out) == {"permission": "allow"}
        assert captured[0]["client"] == "cursor"
        assert captured[0]["url"] == "https://mcp.example.com/sse"
        assert "command" not in captured[0]
        assert captured[0]["tool_input"] == '{"limit": 3}'

    def test_cursor_before_mcp_execution_resolves_mcp_server_name_to_url(
        self, monkeypatch, tmp_path, capsys
    ) -> None:
        cursor_file = tmp_path / ".cursor" / "mcp.json"
        cursor_file.parent.mkdir()
        cursor_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "snowflake-via-satori": {
                            "url": (
                                "https://lemonade.runlayer.com/api/v1/proxy/"
                                "653ec488-c927-4c12-80e4-001ee67cc750/mcp"
                            )
                        }
                    }
                }
            )
        )
        captured = self._capture_enforce(monkeypatch)

        resp = HookResponse(Client.CURSOR, "beforeMCPExecution")
        hook_dispatch._handle_before_mcp_execution(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "hook_event_name": "beforeMCPExecution",
                "tool_name": "list_semantic_views",
                "tool_input": {},
                "mcp_server_name": "snowflake-via-satori",
                "workspace_roots": [str(tmp_path)],
            },
            raw_input="{}",
            original_hook_type="beforeMCPExecution",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert json.loads(capsys.readouterr().out) == {"permission": "allow"}
        assert captured[0]["url"] == (
            "https://lemonade.runlayer.com/api/v1/proxy/"
            "653ec488-c927-4c12-80e4-001ee67cc750/mcp"
        )
        assert captured[0]["mcp_server_name"] == "snowflake-via-satori"
        assert "command" not in captured[0]

    def test_before_mcp_execution_promotes_cursor_without_detection_signals(
        self, monkeypatch, tmp_path, capsys
    ) -> None:
        cursor_file = tmp_path / ".cursor" / "mcp.json"
        cursor_file.parent.mkdir()
        cursor_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "snowflake-via-satori": {
                            "url": (
                                "https://lemonade.runlayer.com/api/v1/proxy/"
                                "653ec488-c927-4c12-80e4-001ee67cc750/mcp"
                            )
                        }
                    }
                }
            )
        )
        captured = self._capture_enforce(monkeypatch)
        payload = {
            "hook_event_name": "beforeMCPExecution",
            "tool_name": "list_semantic_views",
            "tool_input": {},
            "mcp_server_name": "snowflake-via-satori",
            "workspace_roots": [str(tmp_path)],
        }
        env = {
            key: value
            for key, value in os.environ.items()
            if key
            not in {
                "CURSOR_VERSION",
                "HOOK_EVENT_NAME",
                "RUNLAYER_HOOK_CLIENT",
            }
        }
        monkeypatch.setattr(sys, "stdin", StringIO(json.dumps(payload)))
        monkeypatch.setattr(hook_dispatch.flow_spool, "spool_append", lambda *_: None)

        with (
            patch.dict(os.environ, env, clear=True),
            patch.object(sys, "argv", ["/usr/local/bin/aiwatch"]),
        ):
            hook_dispatch.run_hook()

        assert json.loads(capsys.readouterr().out) == {"permission": "allow"}
        assert captured[0]["client"] == "cursor"
        assert captured[0]["url"] == (
            "https://lemonade.runlayer.com/api/v1/proxy/"
            "653ec488-c927-4c12-80e4-001ee67cc750/mcp"
        )

    def test_cursor_before_mcp_execution_preserves_profile_scope_on_name_collision(
        self, monkeypatch, tmp_path, capsys
    ) -> None:
        workspace = tmp_path / "workspace"
        workspace_cursor_file = workspace / ".cursor" / "mcp.json"
        workspace_cursor_file.parent.mkdir(parents=True)
        workspace_cursor_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "yj-readonly": {"url": "https://workspace.example.com/mcp"}
                    }
                }
            )
        )

        profile_home = tmp_path / "profile"
        profile_cursor_file = profile_home / ".cursor" / "mcp.json"
        profile_cursor_file.parent.mkdir(parents=True)
        profile_cursor_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "yj-readonly": {"url": "https://profile.example.com/mcp"}
                    }
                }
            )
        )
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: profile_home))
        captured = self._capture_enforce(monkeypatch)

        resp = HookResponse(Client.CURSOR, "beforeMCPExecution")
        hook_dispatch._handle_before_mcp_execution(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "hook_event_name": "beforeMCPExecution",
                "tool_name": "search_tools",
                "tool_input": {"query": "Vanta evidence"},
                "command": (
                    "user-yj-readonly::mcpScope:profile:"
                    "aWQ6TWpBMllqZzROV00:cfg:OWM0MmE2YzA"
                ),
                "workspace_roots": [str(workspace)],
            },
            raw_input="{}",
            original_hook_type="beforeMCPExecution",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert json.loads(capsys.readouterr().out) == {"permission": "allow"}
        assert captured[0]["url"] == "https://profile.example.com/mcp"
        assert "command" not in captured[0]
        assert captured[0]["tool_input"] == '{"query": "Vanta evidence"}'

    def test_scoped_command_does_not_fallback_to_unscoped_server_name(
        self, monkeypatch, tmp_path, capsys
    ) -> None:
        workspace = tmp_path / "workspace"
        workspace_cursor_file = workspace / ".cursor" / "mcp.json"
        workspace_cursor_file.parent.mkdir(parents=True)
        workspace_cursor_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "yj-readonly": {"url": "https://workspace.example.com/mcp"}
                    }
                }
            )
        )

        profile_home = tmp_path / "profile"
        profile_cursor_file = profile_home / ".cursor" / "mcp.json"
        profile_cursor_file.parent.mkdir(parents=True)
        profile_cursor_file.write_text(json.dumps({"mcpServers": {}}))
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: profile_home))
        captured = self._capture_enforce(monkeypatch)
        scoped_command = (
            "user-yj-readonly::mcpScope:profile:aWQ6TWpBMllqZzROV00:cfg:OWM0MmE2YzA"
        )

        resp = HookResponse(Client.CURSOR, "beforeMCPExecution")
        hook_dispatch._handle_before_mcp_execution(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "hook_event_name": "beforeMCPExecution",
                "tool_name": "search_tools",
                "tool_input": {"query": "Vanta evidence"},
                "command": scoped_command,
                "mcp_server_name": "yj-readonly",
                "workspace_roots": [str(workspace)],
            },
            raw_input="{}",
            original_hook_type="beforeMCPExecution",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert json.loads(capsys.readouterr().out) == {"permission": "allow"}
        assert captured[0]["command"] == scoped_command
        assert captured[0]["mcp_server_name"] == "yj-readonly"
        assert "url" not in captured[0]

    def test_cursor_before_mcp_execution_resolves_command_to_stdio(
        self, monkeypatch, tmp_path, capsys
    ) -> None:
        cursor_file = tmp_path / ".cursor" / "mcp.json"
        cursor_file.parent.mkdir()
        cursor_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "local-runlayer": {
                            "command": "runlayer",
                            "args": ["run", "server-123"],
                        }
                    }
                }
            )
        )
        captured = self._capture_enforce(monkeypatch)

        resp = HookResponse(Client.CURSOR, "beforeMCPExecution")
        hook_dispatch._handle_before_mcp_execution(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "hook_event_name": "beforeMCPExecution",
                "tool_name": "list_teams",
                "tool_input": "{}",
                "command": "local-runlayer",
                "cwd": str(tmp_path),
            },
            raw_input="{}",
            original_hook_type="beforeMCPExecution",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert json.loads(capsys.readouterr().out) == {"permission": "allow"}
        assert captured[0]["command"] == "runlayer run server-123"
        assert "url" not in captured[0]

    def test_cursor_before_mcp_execution_leaves_unresolved_command(
        self, monkeypatch, tmp_path, capsys
    ) -> None:
        captured = self._capture_enforce(monkeypatch)

        resp = HookResponse(Client.CURSOR, "beforeMCPExecution")
        hook_dispatch._handle_before_mcp_execution(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "hook_event_name": "beforeMCPExecution",
                "tool_name": "list_teams",
                "tool_input": "{}",
                "command": "unknown-server",
                "cwd": str(tmp_path),
            },
            raw_input="{}",
            original_hook_type="beforeMCPExecution",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert json.loads(capsys.readouterr().out) == {"permission": "allow"}
        assert captured[0]["command"] == "unknown-server"
        assert "url" not in captured[0]

    def test_cursor_before_mcp_execution_omits_null_allow_messages(
        self, monkeypatch, capsys
    ) -> None:
        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            return json.dumps(
                {
                    "permission": "allow",
                    "user_message": None,
                    "agent_message": None,
                }
            )

        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)

        resp = HookResponse(Client.CURSOR, "beforeMCPExecution")
        hook_dispatch._handle_before_mcp_execution(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "hook_event_name": "beforeMCPExecution",
                "tool_name": "list_teams",
                "tool_input": {},
                "url": "https://mcp.example.com/sse",
            },
            raw_input="{}",
            original_hook_type="beforeMCPExecution",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert json.loads(capsys.readouterr().out) == {"permission": "allow"}


class TestLoadCredentialsFailClosed:
    """Regression: `_load_credentials` must convert non-RelayError exceptions
    (corrupted YAML producing a non-dict, keyring backend raising an unexpected
    exception, etc.) into ``RelayError(1)``.

    Otherwise the unhandled exception escapes ``enforce()``, escapes the
    ``except RelayError`` clauses in ``_handle_before_mcp_execution`` /
    ``_handle_configured_mcp_tool``, and crashes the hook with exit code 1 — no
    deny shape is written to stdout. Some AI clients interpret a crashed hook
    as fail-open, breaking the security contract documented in
    ``__main__.py:4`` ("Exit code is always 0").
    """

    def test_load_credentials_wraps_runtime_error_as_relay_error(
        self, monkeypatch
    ) -> None:
        def _boom() -> object:
            raise RuntimeError("yaml parsed to a list, not a dict")

        monkeypatch.setattr(relay, "load_config", _boom)

        with pytest.raises(relay.RelayError) as exc:
            relay._load_credentials()
        assert exc.value.exit_code == 1

    def test_load_credentials_wraps_keyring_unexpected_error(self, monkeypatch) -> None:
        class _ConfigStub:
            default_host = "https://app.runlayer.com"

            def get_secret_for_host(self, _host: str) -> str:
                raise OSError("keyring backend exploded")

        monkeypatch.setattr(relay, "load_config", lambda: _ConfigStub())
        # Force the legacy per-user path: an org key in machine MDM config would
        # short-circuit before keyring is ever consulted.
        monkeypatch.setattr(relay, "read_managed_config", lambda: {})

        with pytest.raises(relay.RelayError) as exc:
            relay._load_credentials()
        assert exc.value.exit_code == 1

    def test_enforce_propagates_relay_error_for_corrupt_config(
        self, monkeypatch
    ) -> None:
        """Top-level ``enforce()`` must surface RelayError (not a bare
        exception) so its callers' ``except RelayError`` clauses run."""
        monkeypatch.setattr(
            relay,
            "load_config",
            lambda: (_ for _ in ()).throw(RuntimeError("corrupt")),
        )

        with pytest.raises(relay.RelayError):
            relay.enforce("{}")

    def test_handle_before_mcp_execution_fails_closed_on_corrupt_config(
        self, monkeypatch, capsys
    ) -> None:
        """The Cursor MCP enforcement path must emit a deny + sys.exit(0) when
        credential loading raises an unexpected exception, not crash."""

        def _boom() -> object:
            raise RuntimeError("yaml parsed to a list, not a dict")

        monkeypatch.setattr(relay, "load_config", _boom)
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)

        resp = HookResponse(Client.CURSOR, "beforeMCPExecution")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_before_mcp_execution(
                client=Client.CURSOR,
                resp=resp,
                input_data={"tool_name": "mcp__x", "url": "https://x"},
                raw_input="{}",
                original_hook_type="beforeMCPExecution",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["permission"] == "deny"

    def test_handle_configured_mcp_tool_fails_closed_on_corrupt_config(
        self, monkeypatch, tmp_path, capsys
    ) -> None:
        """The Claude Code MCP enforcement path must emit a deny + sys.exit(0)
        when credential loading raises, not crash."""
        mcp_file = tmp_path / ".mcp.json"
        mcp_file.write_text(
            json.dumps(
                {"mcpServers": {"github": {"url": "https://mcp.github.example"}}}
            )
        )

        def _boom() -> object:
            raise RuntimeError("yaml parsed to a list, not a dict")

        monkeypatch.setattr(relay, "load_config", _boom)
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)

        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_dispatch._handle_configured_mcp_tool(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "mcp__github__list_repos",
                    "cwd": str(tmp_path),
                },
                tool_name="mcp__github__list_repos",
                original_hook_type="PreToolUse",
                mode=AIWatchMode.ENFORCE,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_handle_configured_mcp_tool_sends_cursor_required_fields(
        self, monkeypatch, tmp_path, capsys
    ) -> None:
        mcp_file = tmp_path / ".mcp.json"
        mcp_file.write_text(
            json.dumps(
                {"mcpServers": {"linear-44": {"url": "https://mcp.example.com/sse"}}}
            )
        )
        monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **kw: None)
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        monkeypatch.setattr(hook_dispatch, "enforce", _fake_enforce)

        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        hook_dispatch._handle_configured_mcp_tool(
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={
                "tool_name": "mcp__linear-44__list_teams",
                "tool_input": {},
                "session_id": "session-123",
                "tool_use_id": "tool-use-456",
                "cwd": str(tmp_path),
            },
            tool_name="mcp__linear-44__list_teams",
            original_hook_type="PreToolUse",
            mode=AIWatchMode.ENFORCE,
            debug=False,
        )

        assert capsys.readouterr().out == ""
        assert captured[0]["hook_event_name"] == "beforeMCPExecution"
        assert captured[0]["client"] == "claude_code"
        assert captured[0]["conversation_id"] == "session-123"
        assert captured[0]["generation_id"] == "tool-use-456"
        assert captured[0]["tool_name"] == "mcp__linear-44__list_teams"
        assert captured[0]["url"] == "https://mcp.example.com/sse"


class TestResolveMode:
    """Resolve endpoint mode from managed or legacy hook configuration."""

    def _mark_frozen_aiwatch(self, tmp_path, monkeypatch):
        """Make is_frozen_aiwatch_bundle() return True (frozen + aiwatch exe stem)."""
        monkeypatch.setattr(sys, "frozen", True, raising=False)
        aiwatch_exe = tmp_path / "aiwatch"
        aiwatch_exe.write_text("")
        monkeypatch.setattr(sys, "executable", str(aiwatch_exe), raising=False)

    def test_frozen_reads_mdm_enforcement_false(self, tmp_path, monkeypatch):
        self._mark_frozen_aiwatch(tmp_path, monkeypatch)
        monkeypatch.setattr(
            "runlayer_cli.mdm_config.read_managed_config",
            lambda: {"enforcement": False},
        )
        assert hook_dispatch._resolve_mode() is AIWatchMode.MONITOR

    def test_frozen_reads_mdm_enforcement_true(self, tmp_path, monkeypatch):
        self._mark_frozen_aiwatch(tmp_path, monkeypatch)
        monkeypatch.setattr(
            "runlayer_cli.mdm_config.read_managed_config",
            lambda: {"enforcement": True},
        )
        assert hook_dispatch._resolve_mode() is AIWatchMode.ENFORCE

    def test_frozen_mdm_true_ignores_no_enforcement_arg(self, tmp_path, monkeypatch):
        self._mark_frozen_aiwatch(tmp_path, monkeypatch)
        monkeypatch.setattr(
            sys,
            "argv",
            [str(tmp_path / "aiwatch"), "--no-enforcement"],
        )
        monkeypatch.setattr(
            "runlayer_cli.mdm_config.read_managed_config",
            lambda: {"enforcement": True},
        )
        assert hook_dispatch._resolve_mode() is AIWatchMode.ENFORCE

    def test_frozen_ignores_enforcement_env_override(self, tmp_path, monkeypatch):
        self._mark_frozen_aiwatch(tmp_path, monkeypatch)
        monkeypatch.setenv("RUNLAYER_HOOK_ENFORCEMENT", "false")
        monkeypatch.setattr(
            "runlayer_cli.mdm_config.read_managed_config",
            lambda: {"enforcement": True},
        )
        assert hook_dispatch._resolve_mode() is AIWatchMode.ENFORCE

    def test_frozen_defaults_false_when_key_absent(self, tmp_path, monkeypatch):
        self._mark_frozen_aiwatch(tmp_path, monkeypatch)
        monkeypatch.setattr(
            "runlayer_cli.mdm_config.read_managed_config",
            lambda: {"host": "https://t.example.com"},
        )
        assert hook_dispatch._resolve_mode() is AIWatchMode.MONITOR

    def test_frozen_defaults_false_when_empty_managed_config(
        self, tmp_path, monkeypatch
    ):
        self._mark_frozen_aiwatch(tmp_path, monkeypatch)
        monkeypatch.setattr(
            "runlayer_cli.mdm_config.read_managed_config",
            lambda: {},
        )
        assert hook_dispatch._resolve_mode() is AIWatchMode.MONITOR

    def test_frozen_non_aiwatch_binary_uses_legacy_file_path(
        self, tmp_path, monkeypatch
    ):
        """A frozen non-aiwatch binary (e.g. full runlayer CLI) must NOT route
        through MDM enforcement — it keeps the legacy runlayer-config.json read."""
        monkeypatch.setattr(sys, "frozen", True, raising=False)
        runlayer_exe = tmp_path / "runlayer"
        runlayer_exe.write_text("")
        monkeypatch.setattr(sys, "executable", str(runlayer_exe), raising=False)
        monkeypatch.setattr(
            "runlayer_cli.mdm_config.read_managed_config",
            lambda: {"enforcement": False},
        )
        wrapper = tmp_path / "runlayer-hook"
        wrapper.write_text("")
        monkeypatch.setattr(sys, "argv", [str(wrapper)])
        # No runlayer-config.json next to argv[0] => legacy default (enforce).
        assert hook_dispatch._resolve_mode() is AIWatchMode.ENFORCE

    def test_unfrozen_reads_file_enforcement_false(self, tmp_path, monkeypatch):
        monkeypatch.setattr(sys, "frozen", False, raising=False)
        (tmp_path / "runlayer-config.json").write_text(
            json.dumps({"enforcement": False})
        )
        wrapper = tmp_path / "aiwatch-hook"
        wrapper.write_text("")
        monkeypatch.setattr(sys, "argv", [str(wrapper)])
        assert hook_dispatch._resolve_mode() is AIWatchMode.MONITOR

    def test_unfrozen_defaults_true_when_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(sys, "frozen", False, raising=False)
        wrapper = tmp_path / "aiwatch-hook"
        wrapper.write_text("")
        monkeypatch.setattr(sys, "argv", [str(wrapper)])
        assert hook_dispatch._resolve_mode() is AIWatchMode.ENFORCE

    def test_unfrozen_defaults_true_when_file_malformed(self, tmp_path, monkeypatch):
        monkeypatch.setattr(sys, "frozen", False, raising=False)
        (tmp_path / "runlayer-config.json").write_text("not json")
        wrapper = tmp_path / "aiwatch-hook"
        wrapper.write_text("")
        monkeypatch.setattr(sys, "argv", [str(wrapper)])
        assert hook_dispatch._resolve_mode() is AIWatchMode.ENFORCE


def _claude_usage_line(
    message_id: str,
    *,
    output_tokens: int = 10,
    text: str = "hi",
    model: str = "claude-opus-4-8",
) -> str:
    return json.dumps(
        {
            "type": "assistant",
            "timestamp": "2026-07-21T00:00:00Z",
            "message": {
                "id": message_id,
                "model": model,
                "role": "assistant",
                "usage": {
                    "input_tokens": 2,
                    "output_tokens": output_tokens,
                    "cache_creation_input_tokens": 5,
                    "cache_read_input_tokens": 7,
                },
                "content": [{"type": "text", "text": text}],
            },
        }
    )


class TestIncrementalTranscriptSend:
    @pytest.fixture(autouse=True)
    def _state_dir(self, monkeypatch, tmp_path: Path):
        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")

    def _capture_posts(self, monkeypatch) -> list[dict]:
        captured: list[dict] = []

        def _fake_forward(target, wrapper, *, timeout=None, debug=False):
            assert target == "event"
            captured.append(json.loads(wrapper))

        monkeypatch.setattr(relay, "_forward_post", _fake_forward)
        monkeypatch.setattr(relay, "_forward_post_strict", _fake_forward)
        return captured

    def test_second_stop_sends_only_appended_bytes(self, monkeypatch, tmp_path: Path):
        captured = self._capture_posts(monkeypatch)
        transcript_path = tmp_path / "transcript.jsonl"
        first = _claude_usage_line("msg_1") + "\n"
        transcript_path.write_text(first)
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}

        relay.forward_stop_event("claude_code", "Stop", payload)
        assert captured[-1]["transcript"] == first

        second = _claude_usage_line("msg_2") + "\n"
        transcript_path.write_text(first + second)
        relay.forward_stop_event("claude_code", "Stop", payload)
        assert captured[-1]["transcript"] == second

    def test_fully_sent_transcript_forwards_plain_event(
        self, monkeypatch, tmp_path: Path
    ):
        captured = self._capture_posts(monkeypatch)
        transcript_path = tmp_path / "transcript.jsonl"
        content = _claude_usage_line("msg_1") + "\n"
        transcript_path.write_text(content)
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}
        transcript_stream.store_transcript_sent_state(
            payload,
            client="claude_code",
            transcript_path=transcript_path,
            offset=len(content.encode("utf-8")),
        )

        relay.forward_stop_event("claude_code", "Stop", payload)

        assert "transcript" not in captured[-1]

    def test_chunks_split_on_line_boundaries(self, monkeypatch, tmp_path: Path):
        captured = self._capture_posts(monkeypatch)
        lines = [_claude_usage_line(f"msg_{i}") + "\n" for i in range(3)]
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("".join(lines))
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}
        monkeypatch.setattr(
            relay, "_TRANSCRIPT_SEND_CHUNK_BYTES", len(lines[0].encode()) + 1
        )

        relay.forward_stop_event("claude_code", "Stop", payload)

        chunks = [w["transcript"] for w in captured]
        assert len(chunks) == 3
        assert all(chunk.endswith("\n") for chunk in chunks)
        assert "".join(chunks) == "".join(lines)

    def test_oversized_backlog_skips_oldest_lines(self, tmp_path: Path, monkeypatch):
        captured = self._capture_posts(monkeypatch)
        lines = [_claude_usage_line(f"msg_{i}") + "\n" for i in range(4)]
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("".join(lines))
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}
        max_bytes = len("".join(lines[2:]).encode()) + 3

        sent = relay.send_unsent_transcript(
            "claude_code", "Stop", payload, transcript_path, max_bytes=max_bytes
        )

        assert sent is True
        combined = "".join(w["transcript"] for w in captured)
        assert combined == "".join(lines[2:])
        state = transcript_stream.load_sent_state_for(payload, transcript_path)
        assert state is not None
        assert state["offset"] == transcript_path.stat().st_size

    def test_truncated_transcript_resends_from_start(self, monkeypatch, tmp_path: Path):
        captured = self._capture_posts(monkeypatch)
        transcript_path = tmp_path / "transcript.jsonl"
        content = _claude_usage_line("msg_1") + "\n"
        transcript_path.write_text(content)
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}
        transcript_stream.store_transcript_sent_state(
            payload,
            client="claude_code",
            transcript_path=transcript_path,
            offset=len(content.encode()) + 500,
        )

        relay.forward_stop_event("claude_code", "Stop", payload)

        assert captured[-1]["transcript"] == content

    def test_trailing_partial_line_deferred(self, monkeypatch, tmp_path: Path):
        captured = self._capture_posts(monkeypatch)
        transcript_path = tmp_path / "transcript.jsonl"
        complete = _claude_usage_line("msg_1") + "\n"
        partial = '{"type": "assistant", "message": {"id": "msg_2", "us'
        transcript_path.write_text(complete + partial)
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}

        relay.forward_stop_event("claude_code", "Stop", payload)

        assert captured[-1]["transcript"] == complete
        state = transcript_stream.load_sent_state_for(payload, transcript_path)
        assert state is not None
        assert state["offset"] == len(complete.encode("utf-8"))

    def test_complete_unterminated_final_line_sent(self, monkeypatch, tmp_path: Path):
        captured = self._capture_posts(monkeypatch)
        transcript_path = tmp_path / "transcript.jsonl"
        content = _claude_usage_line("msg_1")
        transcript_path.write_text(content)
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}

        relay.forward_stop_event("claude_code", "Stop", payload)

        assert captured[-1]["transcript"] == content

    def test_codex_chunk_prepends_model_seed(self, monkeypatch, tmp_path: Path):
        captured = self._capture_posts(monkeypatch)
        transcript_path = tmp_path / "transcript.jsonl"
        token_line = json.dumps(
            {
                "type": "event_msg",
                "payload": {
                    "type": "token_count",
                    "info": {
                        "last_token_usage": {"total_tokens": 5},
                        "total_token_usage": {"total_tokens": 5},
                    },
                },
            }
        )
        transcript_path.write_text(token_line + "\n")
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}
        transcript_stream.store_transcript_sent_state(
            payload,
            client="codex",
            transcript_path=transcript_path,
            offset=0,
            model="gpt-5-codex",
        )

        relay.forward_stop_event("codex", "Stop", payload)

        sent_lines = captured[-1]["transcript"].splitlines()
        seed = json.loads(sent_lines[0])
        assert seed == {"type": "turn_context", "payload": {"model": "gpt-5-codex"}}
        assert json.loads(sent_lines[1])["payload"]["type"] == "token_count"

    def test_codex_state_tracks_new_turn_context_model(
        self, monkeypatch, tmp_path: Path
    ):
        self._capture_posts(monkeypatch)
        transcript_path = tmp_path / "transcript.jsonl"
        turn_context = json.dumps(
            {"type": "turn_context", "payload": {"model": "gpt-6-codex"}}
        )
        transcript_path.write_text(turn_context + "\n")
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}

        relay.forward_stop_event("codex", "Stop", payload)

        state = transcript_stream.load_sent_state_for(payload, transcript_path)
        assert state is not None
        assert state["model"] == "gpt-6-codex"

    def test_failed_post_never_advances_offset(self, monkeypatch, tmp_path: Path):
        """Repro for the swallowed-POST bug: a network failure below the
        forward layer must not advance the sent-offset (the chunk sender has
        to use the raising POST variant, not the fire-and-forget one)."""
        monkeypatch.setattr(
            relay, "_load_credentials", lambda: ("https://host", "secret")
        )

        def _post_fails(*args, **kwargs):
            raise relay.RelayError(2, "network down")

        monkeypatch.setattr(relay, "_post", _post_fails)
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text(_claude_usage_line("msg_1") + "\n")
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}

        relay.forward_stop_event("claude_code", "Stop", payload)

        assert transcript_stream.load_sent_state_for(payload, transcript_path) is None

    def test_first_chunk_failure_falls_back_to_plain_event(
        self, monkeypatch, tmp_path: Path
    ):
        plain: list[dict] = []

        def _fail_strict(target, wrapper, *, timeout=None, debug=False):
            raise relay.RelayError(2, "boom")

        def _capture_plain(target, wrapper, *, timeout=None, debug=False):
            plain.append(json.loads(wrapper))

        monkeypatch.setattr(relay, "_forward_post_strict", _fail_strict)
        monkeypatch.setattr(relay, "_forward_post", _capture_plain)
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text(_claude_usage_line("msg_1") + "\n")
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}

        relay.forward_stop_event("claude_code", "Stop", payload)

        assert transcript_stream.load_sent_state_for(payload, transcript_path) is None
        assert len(plain) == 1
        assert "transcript" not in plain[0]

    def test_partial_failure_keeps_progress_and_resumes(
        self, monkeypatch, tmp_path: Path
    ):
        lines = [_claude_usage_line(f"msg_{i}") + "\n" for i in range(2)]
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("".join(lines))
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}
        monkeypatch.setattr(
            relay, "_TRANSCRIPT_SEND_CHUNK_BYTES", len(lines[0].encode()) + 1
        )
        calls = {"count": 0}
        captured: list[dict] = []

        def _flaky(target, wrapper, *, timeout=None, debug=False):
            calls["count"] += 1
            if calls["count"] == 2:
                raise relay.RelayError(2, "boom")
            captured.append(json.loads(wrapper))

        monkeypatch.setattr(relay, "_forward_post", _flaky)
        monkeypatch.setattr(relay, "_forward_post_strict", _flaky)

        relay.forward_stop_event("claude_code", "Stop", payload)
        state = transcript_stream.load_sent_state_for(payload, transcript_path)
        assert state is not None
        assert state["offset"] == len(lines[0].encode("utf-8"))

        relay.forward_stop_event("claude_code", "Stop", payload)
        assert [w["transcript"] for w in captured] == [lines[0], lines[1]]


class TestTailerSentStateAndClaudeUsage:
    @pytest.fixture(autouse=True)
    def _state_dir(self, monkeypatch, tmp_path: Path):
        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")

    def test_tailer_emits_claude_usage_once_and_persists_offset(self, tmp_path: Path):
        transcript_path = tmp_path / "transcript.jsonl"
        lines = [
            _claude_usage_line("msg_1", text="draft"),
            _claude_usage_line("msg_1", text="draft longer"),
            '{"type":"result"}',
        ]
        transcript_path.write_text("\n".join(lines) + "\n")
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}
        delivered: list[tuple[str, dict]] = []

        transcript_stream.run_transcript_stream(
            client_name="claude_code",
            payload=payload,
            post_event=lambda _c, event_name, event_payload: delivered.append(
                (event_name, event_payload)
            ),
            max_seconds=1,
            idle_seconds=1,
            poll_seconds=0.01,
        )

        token_events = [p for n, p in delivered if n == "message.token_count"]
        assert len(token_events) == 1
        event = token_events[0]
        assert event["external_message_id"] == "msg_1"
        assert event["input_tokens"] == 2
        assert event["output_tokens"] == 10
        assert event["cache_creation_tokens"] == 5
        assert event["cache_read_tokens"] == 7
        assert event["model"] == "claude-opus-4-8"
        assert event["token_source"] == "provider"
        assert event["token_origin"] == "client_transcript"

        state = transcript_stream.load_sent_state_for(payload, transcript_path)
        assert state is not None
        assert state["offset"] == transcript_path.stat().st_size

    def test_tailer_does_not_persist_over_undelivered_gap(self, tmp_path: Path):
        transcript_path = tmp_path / "transcript.jsonl"
        backlog = _claude_usage_line("msg_1") + "\n"
        transcript_path.write_text(backlog)
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}
        start_offset = transcript_path.stat().st_size
        transcript_path.write_text(backlog + '{"type":"result"}\n')

        transcript_stream.run_transcript_stream(
            client_name="claude_code",
            payload=payload,
            start_offset=start_offset,
            post_event=lambda *_: None,
            max_seconds=1,
            idle_seconds=1,
            poll_seconds=0.01,
        )

        assert transcript_stream.load_sent_state_for(payload, transcript_path) is None

    def test_tailer_persists_when_backlog_already_sent(self, tmp_path: Path):
        transcript_path = tmp_path / "transcript.jsonl"
        backlog = _claude_usage_line("msg_1") + "\n"
        transcript_path.write_text(backlog)
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}
        start_offset = transcript_path.stat().st_size
        transcript_stream.store_transcript_sent_state(
            payload,
            client="claude_code",
            transcript_path=transcript_path,
            offset=start_offset,
        )
        transcript_path.write_text(
            backlog + _claude_usage_line("msg_2") + "\n" + '{"type":"result"}\n'
        )

        transcript_stream.run_transcript_stream(
            client_name="claude_code",
            payload=payload,
            start_offset=start_offset,
            post_event=lambda *_: None,
            max_seconds=1,
            idle_seconds=1,
            poll_seconds=0.01,
        )

        state = transcript_stream.load_sent_state_for(payload, transcript_path)
        assert state is not None
        assert state["offset"] == transcript_path.stat().st_size

    def test_tailer_skips_to_capped_tail_without_advancing_sent_state(
        self, monkeypatch, tmp_path: Path, capsys
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        event_line = (
            json.dumps(
                {
                    "type": "assistant",
                    "timestamp": "2026-08-17T00:00:00Z",
                    "message": {
                        "role": "assistant",
                        "content": [{"type": "text", "text": "newest"}],
                    },
                }
            )
            + "\n"
        )
        terminal_line = '{"type":"result"}\n'
        transcript_path.write_bytes(
            b"x" * 64 + b"\n" + (event_line + terminal_line).encode()
        )
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}
        delivered: list[tuple[str, dict]] = []
        read_cap = len((event_line + terminal_line).encode()) + 8
        monkeypatch.setattr(
            transcript_stream,
            "_TRANSCRIPT_READ_MAX_BYTES",
            read_cap,
            raising=False,
        )

        transcript_stream.run_transcript_stream(
            client_name="claude_code",
            payload=payload,
            post_event=lambda _c, event_name, event_payload: delivered.append(
                (event_name, event_payload)
            ),
            debug=True,
            max_seconds=1,
            idle_seconds=1,
            poll_seconds=0.01,
        )

        assert [
            event_payload["message"]["content"] for _, event_payload in delivered
        ] == ["newest"]
        assert transcript_stream.load_sent_state_for(payload, transcript_path) is None
        assert not transcript_stream.is_transcript_stream_active(payload)
        assert not transcript_stream.is_transcript_stream_recently_completed(payload)
        assert "capped tail" in capsys.readouterr().err

    def test_tailer_drops_oversized_line_without_parsing_it(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        oversized_line = json.dumps(
            {
                "type": "assistant",
                "message": {
                    "role": "assistant",
                    "content": [{"type": "text", "text": "x" * 512}],
                },
            }
        )
        normal_line = json.dumps(
            {
                "type": "assistant",
                "message": {
                    "role": "assistant",
                    "content": [{"type": "text", "text": "after-large-line"}],
                },
            }
        )
        line_cap = 256
        assert len(normal_line.encode()) < line_cap < len(oversized_line.encode())
        transcript_path.write_text(
            "\n".join([oversized_line, normal_line, '{"type":"result"}']) + "\n"
        )
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}
        delivered: list[tuple[str, dict]] = []
        original_terminal = transcript_stream.transcript_line_is_terminal
        original_events = transcript_stream.transcript_line_events

        def _bounded_terminal(line: str) -> bool:
            assert len(line.encode()) <= line_cap
            return original_terminal(line)

        def _bounded_events(line: str, **kwargs):
            assert len(line.encode()) <= line_cap
            return original_events(line, **kwargs)

        monkeypatch.setattr(
            transcript_stream,
            "_TRANSCRIPT_LINE_MAX_BYTES",
            line_cap,
            raising=False,
        )
        monkeypatch.setattr(
            transcript_stream, "transcript_line_is_terminal", _bounded_terminal
        )
        monkeypatch.setattr(
            transcript_stream, "transcript_line_events", _bounded_events
        )

        transcript_stream.run_transcript_stream(
            client_name="claude_code",
            payload=payload,
            post_event=lambda _c, event_name, event_payload: delivered.append(
                (event_name, event_payload)
            ),
            max_seconds=1,
            idle_seconds=1,
            poll_seconds=0.01,
        )

        assert [
            event_payload["message"]["content"] for _, event_payload in delivered
        ] == ["after-large-line"]
        assert transcript_stream.load_sent_state_for(payload, transcript_path) is None
        assert not transcript_stream.is_transcript_stream_active(payload)
        assert not transcript_stream.is_transcript_stream_recently_completed(payload)

    def test_tailer_detects_oversized_line_after_terminal(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        normal_line = json.dumps(
            {
                "type": "assistant",
                "message": {
                    "role": "assistant",
                    "content": [{"type": "text", "text": "before-terminal"}],
                },
            }
        )
        transcript_path.write_text(
            "\n".join([normal_line, '{"type":"result"}', "x" * 512]) + "\n"
        )
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}
        delivered: list[tuple[str, dict]] = []
        monkeypatch.setattr(
            transcript_stream,
            "_TRANSCRIPT_LINE_MAX_BYTES",
            256,
        )

        transcript_stream.run_transcript_stream(
            client_name="claude_code",
            payload=payload,
            post_event=lambda _c, event_name, event_payload: delivered.append(
                (event_name, event_payload)
            ),
            max_seconds=1,
            idle_seconds=1,
            poll_seconds=0.01,
        )

        assert [
            event_payload["message"]["content"] for _, event_payload in delivered
        ] == ["before-terminal"]
        assert transcript_stream.load_sent_state_for(payload, transcript_path) is None
        assert not transcript_stream.is_transcript_stream_recently_completed(payload)

    def test_tailer_dedupe_evicts_oldest_entry_at_bound(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"

        def _assistant_line(text: str) -> str:
            return json.dumps(
                {
                    "type": "assistant",
                    "timestamp": "2026-08-17T00:00:00Z",
                    "message": {
                        "role": "assistant",
                        "content": [{"type": "text", "text": text}],
                    },
                }
            )

        transcript_path.write_text(
            "\n".join(
                [
                    _assistant_line("a"),
                    _assistant_line("b"),
                    _assistant_line("c"),
                    _assistant_line("a"),
                    '{"type":"result"}',
                ]
            )
            + "\n"
        )
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}
        delivered: list[str] = []
        monkeypatch.setattr(
            transcript_stream,
            "_TRANSCRIPT_DEDUPE_MAX_ENTRIES",
            2,
            raising=False,
        )

        transcript_stream.run_transcript_stream(
            client_name="claude_code",
            payload=payload,
            post_event=lambda _c, _event_name, event_payload: delivered.append(
                event_payload["message"]["content"]
            ),
            max_seconds=1,
            idle_seconds=1,
            poll_seconds=0.01,
        )

        assert delivered == ["a", "b", "c", "a"]

    def test_claude_usage_snapshot_dedupe_is_bounded(self, monkeypatch):
        stream_state: dict = {}
        monkeypatch.setattr(
            transcript_stream,
            "_TRANSCRIPT_DEDUPE_MAX_ENTRIES",
            2,
        )

        for message_id in ("msg_1", "msg_2", "msg_3"):
            transcript_stream.transcript_line_events(
                _claude_usage_line(message_id),
                fallback_session_id="s1",
                stream_state=stream_state,
                client_name="claude_code",
            )

        assert list(stream_state["claude_usage_seen"]) == ["msg_2", "msg_3"]
        replayed = transcript_stream.transcript_line_events(
            _claude_usage_line("msg_1"),
            fallback_session_id="s1",
            stream_state=stream_state,
            client_name="claude_code",
        )
        assert any(event_name == "message.token_count" for event_name, _ in replayed)

    def test_tailer_discards_oversized_partial_buffer(
        self, monkeypatch, tmp_path: Path
    ):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text("x" * 512)
        normal_line = json.dumps(
            {
                "type": "assistant",
                "message": {
                    "role": "assistant",
                    "content": [{"type": "text", "text": "after-partial"}],
                },
            }
        )
        line_cap = 256
        assert len(normal_line.encode()) < line_cap
        payload = {"session_id": "s1", "transcript_path": str(transcript_path)}
        delivered: list[tuple[str, dict]] = []
        original_complete = transcript_stream._buffer_is_complete_json_line
        sleep_calls = 0

        def _bounded_complete(buffer: str) -> bool:
            assert len(buffer.encode()) <= line_cap
            return original_complete(buffer)

        def _append_after_buffer_check(_seconds: float) -> None:
            nonlocal sleep_calls
            sleep_calls += 1
            if sleep_calls == 2:
                with transcript_path.open("a") as transcript:
                    transcript.write("\n" + normal_line + "\n" + '{"type":"result"}\n')

        monkeypatch.setattr(
            transcript_stream,
            "_TRANSCRIPT_LINE_MAX_BYTES",
            line_cap,
        )
        monkeypatch.setattr(
            transcript_stream, "_buffer_is_complete_json_line", _bounded_complete
        )
        monkeypatch.setattr(transcript_stream.time, "sleep", _append_after_buffer_check)

        transcript_stream.run_transcript_stream(
            client_name="claude_code",
            payload=payload,
            post_event=lambda _c, event_name, event_payload: delivered.append(
                (event_name, event_payload)
            ),
            max_seconds=1,
            idle_seconds=1,
            poll_seconds=0.01,
        )

        assert [
            event_payload["message"]["content"] for _, event_payload in delivered
        ] == ["after-partial"]
        assert transcript_stream.load_sent_state_for(payload, transcript_path) is None
        assert not transcript_stream.is_transcript_stream_active(payload)
        assert not transcript_stream.is_transcript_stream_recently_completed(payload)


class TestFlushStaleTranscriptSentStates:
    @pytest.fixture(autouse=True)
    def _state_dir(self, monkeypatch, tmp_path: Path):
        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")

    def _make_state(
        self,
        tmp_path: Path,
        session_id: str,
        *,
        client: str = "claude_code",
        unsent_lines: int = 1,
        stale: bool = True,
    ) -> Path:
        transcript_path = tmp_path / f"{session_id}.jsonl"
        content = "".join(
            _claude_usage_line(f"{session_id}-msg_{i}") + "\n"
            for i in range(unsent_lines + 1)
        )
        transcript_path.write_text(content)
        first_line_end = content.index("\n") + 1
        offset = transcript_path.stat().st_size if unsent_lines == 0 else first_line_end
        payload = {"session_id": session_id, "transcript_path": str(transcript_path)}
        transcript_stream.store_transcript_sent_state(
            payload, client=client, transcript_path=transcript_path, offset=offset
        )
        state_path = transcript_stream.transcript_sent_state_path(payload)
        assert state_path is not None
        if stale:
            old = time.time() - 3600
            os.utime(state_path, (old, old))
        return state_path

    def test_flushes_stale_prunes_done_skips_fresh_and_foreign(
        self, monkeypatch, tmp_path: Path
    ):
        captured: list[dict] = []

        def _fake_forward(target, wrapper, *, timeout=None, debug=False):
            captured.append(json.loads(wrapper))

        monkeypatch.setattr(relay, "_forward_post", _fake_forward)
        monkeypatch.setattr(relay, "_forward_post_strict", _fake_forward)

        stale = self._make_state(tmp_path, "stale-a")
        fresh = self._make_state(tmp_path, "fresh-b", stale=False)
        done = self._make_state(tmp_path, "done-c", unsent_lines=0)
        foreign = self._make_state(tmp_path, "codex-d", client="codex")
        current = self._make_state(tmp_path, "current-e")

        flushed = relay.flush_stale_transcript_sent_states(
            "claude_code", exclude_session_id="current-e"
        )

        assert flushed == 1
        assert len(captured) == 1
        assert captured[0]["payload"]["session_id"] == "stale-a"
        assert "stale-a-msg_1" in captured[0]["transcript"]
        assert "stale-a-msg_0" not in captured[0]["transcript"]
        assert not done.exists()
        assert stale.exists() and fresh.exists()
        assert foreign.exists() and current.exists()

    def test_flush_skips_idle_but_live_session(self, monkeypatch, tmp_path: Path):
        """Repro: an idle session stops persisting new bytes so its sent-state
        goes mtime-stale, but its tailer still heartbeats the active marker —
        the flush must leave it alone."""
        captured: list[dict] = []

        def _fake_forward(target, wrapper, *, timeout=None, debug=False):
            captured.append(json.loads(wrapper))

        monkeypatch.setattr(relay, "_forward_post", _fake_forward)
        monkeypatch.setattr(relay, "_forward_post_strict", _fake_forward)

        self._make_state(tmp_path, "idle-live")
        transcript_stream.mark_transcript_stream_active({"session_id": "idle-live"})

        flushed = relay.flush_stale_transcript_sent_states(
            "claude_code", exclude_session_id="other"
        )

        assert flushed == 0
        assert captured == []


class TestDevinCLIHooks:
    """Devin CLI: Claude-shaped payloads, top-level ``decision: block``."""

    @staticmethod
    def _clean_env(**overrides):
        env = {
            k: v
            for k, v in os.environ.items()
            if k not in ("CURSOR_VERSION", "DEVIN_PROJECT_DIR")
        }
        env.update(overrides)
        return env

    @staticmethod
    def _seed(home: Path, project: Path, files: dict[str, object]) -> None:
        """Write config fixtures; a ``~/`` prefix anchors on *home*, else *project*."""
        for relative, payload in files.items():
            root = home if relative.startswith("~/") else project
            path = root / relative.removeprefix("~/")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                payload if isinstance(payload, str) else json.dumps(payload)
            )

    # -- detection ------------------------------------------------------

    @pytest.mark.parametrize(
        "argv0",
        [
            "/home/user/.config/devin/aiwatch-hook",
            "/repo/.devin/aiwatch-hook",
        ],
    )
    def test_detect_from_devin_config_dir(self, argv0):
        with patch.dict(os.environ, self._clean_env(), clear=True):
            with patch("sys.argv", [argv0]):
                assert detect_client() == Client.DEVIN_CLI

    def test_detect_from_windows_appdata_path(self):
        """Backslash paths must normalize so Devin doesn't fall through to Claude."""
        with patch.dict(os.environ, self._clean_env(), clear=True):
            with patch(
                "runlayer_cli.hook.clients.Path",
                _windows_path_mock("C:\\Users\\dev\\AppData\\Roaming\\devin"),
            ):
                assert detect_client() == Client.DEVIN_CLI

    def test_detect_from_project_dir_env(self):
        """A hook wired without --client is still attributed to the Devin host."""
        with patch.dict(
            os.environ, self._clean_env(DEVIN_PROJECT_DIR="/repo"), clear=True
        ):
            with patch("sys.argv", ["/usr/local/lib/runlayer/aiwatch/aiwatch-hook"]):
                assert detect_client() == Client.DEVIN_CLI

    def test_user_named_devin_does_not_match(self):
        """``/Users/devin`` must not be read as a Devin config directory."""
        with patch.dict(os.environ, self._clean_env(), clear=True):
            with patch("sys.argv", ["/Users/devin/.claude/aiwatch-hook"]):
                assert detect_client() == Client.CLAUDE_CODE

    # -- response shaping -----------------------------------------------

    def test_deny_uses_top_level_decision_block(self):
        r = HookResponse(Client.DEVIN_CLI, "PreToolUse")
        assert json.loads(r.deny("blocked", "agent reason")) == {
            "decision": "block",
            "reason": "agent reason",
        }

    def test_allow_emits_no_output(self):
        assert HookResponse(Client.DEVIN_CLI, "PreToolUse").allow() is None

    def test_allow_with_updated_input_omits_permission_decision(self):
        """Devin documents ``updatedInput`` only; a permissionDecision it does not
        read could otherwise be mistaken for an explicit approve."""
        r = HookResponse(Client.DEVIN_CLI, "PreToolUse")
        assert json.loads(r.allow_with_updated_input({"command": "ls"})) == {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "updatedInput": {"command": "ls"},
            }
        }

    @pytest.mark.parametrize(
        ("event", "expected"),
        [
            # Devin's only divergence from Claude Code's vocabulary.
            ("PostCompaction", "PostCompact"),
            ("PreToolUse", "PreToolUse"),
            ("SessionStart", "SessionStart"),
        ],
    )
    def test_event_name_normalization(self, event, expected):
        assert normalize_event_name(event) == expected

    # -- double-fire guard ----------------------------------------------

    @pytest.mark.parametrize(
        ("case", "devin_is_host", "argv0", "tagged", "expected"),
        [
            # Devin imports and runs other clients' hooks, so an imported copy
            # must stand down for Runlayer's own --client devin-cli entry.
            (
                "tagged claude hook under devin",
                True,
                "/h/.claude/hook",
                "claude_code",
                True,
            ),
            ("tagged cursor hook under devin", True, "/h/.cursor/hook", "cursor", True),
            # Regression: an *untagged* imported hook resolves to DEVIN_CLI via
            # DEVIN_PROJECT_DIR, so the resolved client alone cannot gate this.
            ("untagged claude hook under devin", True, "/h/.claude/hook", None, True),
            (
                "runlayer's own devin hook",
                True,
                "/h/.config/devin/hook",
                "devin-cli",
                False,
            ),
            (
                "untagged hook in devin's dir",
                True,
                "/h/.config/devin/hook",
                None,
                False,
            ),
            ("not a devin host", False, "/h/.claude/hook", "claude_code", False),
        ],
    )
    def test_noop_guard(self, case, devin_is_host, argv0, tagged, expected):
        env = (
            self._clean_env(DEVIN_PROJECT_DIR="/repo")
            if devin_is_host
            else self._clean_env()
        )
        argv = [argv0] + (["--client", tagged] if tagged else [])
        with patch.dict(os.environ, env, clear=True):
            with patch("sys.argv", argv):
                assert should_noop_for_devin(detect_client()) is expected, case

    # -- MCP source resolution ------------------------------------------

    _NATIVE = {"mcpServers": {"linear": {"url": "https://native/sse"}}}
    _CLAUDE = {"mcpServers": {"linear": {"url": "https://c/sse"}}}

    @pytest.mark.parametrize(
        ("case", "files", "field", "expected"),
        [
            (
                "native user config",
                {"~/.config/devin/mcp_config.json": _NATIVE},
                "url",
                "https://native/sse",
            ),
            (
                # Servers lived here before Devin v3000.3 split them out.
                "native pre-migration config.json",
                {"~/.config/devin/config.json": _NATIVE},
                "url",
                "https://native/sse",
            ),
            (
                # read_config_from.claude defaults on.
                "claude import",
                {"~/.claude.json": _CLAUDE},
                "url",
                "https://c/sse",
            ),
            (
                "cursor import",
                {
                    ".cursor/mcp.json": {
                        "mcpServers": {"linear": {"url": "https://cu/sse"}}
                    }
                },
                "url",
                "https://cu/sse",
            ),
            (
                "windsurf import",
                {
                    "~/.codeium/windsurf/mcp_config.json": {
                        "mcpServers": {"linear": {"url": "https://w/sse"}}
                    }
                },
                "url",
                "https://w/sse",
            ),
            (
                # Devin imports ~/.codeium/<channel>/, not just the stable channel.
                "windsurf non-stable channel",
                {
                    "~/.codeium/windsurf-next/mcp_config.json": {
                        "mcpServers": {"linear": {"url": "https://next/sse"}}
                    }
                },
                "url",
                "https://next/sse",
            ),
            (
                "zed context_servers import",
                {
                    ".zed/settings.json": {
                        "context_servers": {"linear": {"url": "https://z/sse"}}
                    }
                },
                "url",
                "https://z/sse",
            ),
            (
                # Zed settings are JSONC by convention.
                "zed with block comments",
                {
                    ".zed/settings.json": "{\n  /* multi\n     line */\n"
                    '  "context_servers": { "linear": { "url": "https://zb/sse" } }\n}\n'
                },
                "url",
                "https://zb/sse",
            ),
            (
                # A block-comment marker inside a string must survive stripping.
                "block comment markers inside a url",
                {
                    ".zed/settings.json": "{\n  /* real */\n"
                    '  "context_servers": { "linear": { "url": "https://x/*glob*/y" } }\n}\n'
                },
                "url",
                "https://x/*glob*/y",
            ),
            (
                "opencode .jsonc with comments",
                {
                    "opencode.jsonc": '{\n  // commented\n  "mcp": {\n'
                    '    "linear": { "type": "remote", "url": "https://oc/sse" },\n  },\n}\n'
                },
                "url",
                "https://oc/sse",
            ),
            (
                # OpenCode carries argv as one list; stringifying it would produce
                # a command no policy could match.
                "opencode argv list is joined",
                {
                    "opencode.json": {
                        "mcp": {
                            "linear": {
                                "type": "local",
                                "command": ["npx", "-y", "linear-mcp"],
                            }
                        }
                    }
                },
                "command",
                "npx -y linear-mcp",
            ),
            (
                # Project config outranks the user-level toggle.
                "project re-enables an import the user disabled",
                {
                    "~/.claude.json": _CLAUDE,
                    "~/.config/devin/config.json": {
                        "read_config_from": {"claude": False}
                    },
                    ".devin/config.json": {"read_config_from": {"claude": True}},
                },
                "url",
                "https://c/sse",
            ),
        ],
    )
    def test_resolves_server(self, tmp_path, case, files, field, expected):
        home, project = tmp_path / "home", tmp_path / "proj"
        home.mkdir(parents=True)
        project.mkdir(parents=True)
        self._seed(home, project, files)

        with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
            server = lookup_devin_cli_mcp_server("linear", str(project))

        assert server is not None, case
        assert server[field] == expected, case

    @pytest.mark.parametrize(
        ("case", "files"),
        [
            (
                # An import must never shadow Devin's own config.
                "native beats cursor import",
                {
                    ".devin/mcp_config.json": _NATIVE,
                    ".cursor/mcp.json": {
                        "mcpServers": {"linear": {"url": "https://cu/sse"}}
                    },
                },
            ),
            (
                "stable windsurf channel beats next",
                {
                    "~/.config/devin/mcp_config.json": _NATIVE,
                    "~/.codeium/windsurf-next/mcp_config.json": {
                        "mcpServers": {"linear": {"url": "https://next/sse"}}
                    },
                },
            ),
        ],
    )
    def test_resolution_precedence(self, tmp_path, case, files):
        home, project = tmp_path / "home", tmp_path / "proj"
        home.mkdir(parents=True)
        project.mkdir(parents=True)
        self._seed(home, project, files)

        with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
            server = lookup_devin_cli_mcp_server("linear", str(project))

        assert server is not None, case
        assert server["url"] == "https://native/sse", case

    @pytest.mark.parametrize(
        ("case", "toggle_config"),
        [
            ("plain json", {"read_config_from": {"claude": False}}),
            # A commented config must not silently drop the toggles and leave a
            # disabled source enabled.
            (
                "jsonc",
                '{\n  // policy\n  "read_config_from": { "claude": false },\n}\n',
            ),
        ],
    )
    def test_disabled_import_source_is_not_resolved(
        self, tmp_path, case, toggle_config
    ):
        home, project = tmp_path / "home", tmp_path / "proj"
        home.mkdir(parents=True)
        project.mkdir(parents=True)
        self._seed(
            home,
            project,
            {
                "~/.claude.json": self._CLAUDE,
                "~/.config/devin/config.json": toggle_config,
            },
        )

        with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
            assert lookup_devin_cli_mcp_server("linear", str(project)) is None, case

    def test_unregistered_server_resolves_to_none(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir(parents=True)
        with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=home):
            assert lookup_devin_cli_mcp_server("absent", str(tmp_path / "proj")) is None
