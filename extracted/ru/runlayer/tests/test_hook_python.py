"""Unit tests for the Python hook modules (replaces bash subprocess tests)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from runlayer_cli.hook.clients import (
    Client,
    HookResponse,
    detect_client,
    should_noop_for_cursor,
)
from runlayer_cli.hook.file_policy import (
    FilePolicyViolation,
    check_bash_command,
    check_file_read,
)
from runlayer_cli.hook import (
    _relay_worker,
    _transcript_stream_worker,
    messages,
    relay,
    transcript_stream,
)
from runlayer_cli.hook import __main__ as hook_main
from runlayer_cli.hook.mcp_lookup import (
    _claude_enabled_plugins,
    lookup_codex_mcp_server,
    lookup_cursor_mcp_server,
    lookup_mcp_server,
    resolve_hermes_mcp_tool,
)


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

    def test_finds_serverurl_in_project_mcp_json(self):
        """Windsurf and some other clients use `serverUrl` instead of `url`."""
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

    def test_finds_uri_in_project_mcp_json(self):
        """Goose uses `uri` instead of `url`."""
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

    def test_finds_serverurl_in_claude_json_projects(self):
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

    def test_finds_uri_in_claude_json_global(self):
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

    def test_hermes_tool_lookup_ignores_non_mapping_yaml_root(self):
        with tempfile.TemporaryDirectory() as td:
            hermes_file = Path(td) / ".hermes" / "config.yaml"
            hermes_file.parent.mkdir()
            hermes_file.write_text("- not\n- a\n- mapping\n")

            with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=Path(td)):
                result = resolve_hermes_mcp_tool("mcp_linear_44_list_issues")

            assert result is None


# =========================================================================
# clients tests
# =========================================================================


class TestClientDetection:
    def test_detect_cursor(self):
        with patch.dict(os.environ, {"CURSOR_VERSION": "1.0.0"}):
            assert detect_client() == Client.CURSOR

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

    def test_detect_hermes_from_path(self):
        env = {k: v for k, v in os.environ.items() if k != "CURSOR_VERSION"}
        with patch.dict(os.environ, env, clear=True):
            with patch(
                "sys.argv",
                ["/home/user/.hermes/agent-hooks/aiwatch-enforce"],
            ):
                assert detect_client() == Client.HERMES

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


class TestFrozenBinaryRelaySpawn:
    """Regression: in a PyInstaller frozen `aiwatch-enforce` binary,
    `sys.executable` is the frozen binary itself — it does NOT understand
    `python -m runlayer_cli.hook._relay_worker`. Re-spawning with `-m` would
    re-enter `__main__.main()` (inheriting `HOOK_EVENT_NAME` from parent) and
    silently break all event forwarding.

    Fix: when frozen, spawn `[exe, "__relay_worker__", target, ...]` and route
    that argv shape to the relay worker inside `__main__.main()`.
    """

    def test_detached_relay_uses_sentinel_argv_when_frozen(self, monkeypatch):
        captured: dict = {}

        class _FakePopen:
            def __init__(self, args, **kwargs):
                captured["args"] = args
                captured["kwargs"] = kwargs
                self.stdin = None

        monkeypatch.setattr(sys, "frozen", True, raising=False)
        monkeypatch.setattr(sys, "executable", "/opt/aiwatch-enforce/aiwatch-enforce")
        monkeypatch.setattr(relay.subprocess, "Popen", _FakePopen)

        relay._detached_relay("event", "{}")

        assert captured["args"][0] == "/opt/aiwatch-enforce/aiwatch-enforce"
        assert captured["args"][1] == "__relay_worker__"
        assert captured["args"][2] == "event"
        assert "-m" not in captured["args"]
        assert "runlayer_cli.hook._relay_worker" not in captured["args"]

    def test_detached_relay_uses_module_invocation_when_not_frozen(self, monkeypatch):
        captured: dict = {}

        class _FakePopen:
            def __init__(self, args, **kwargs):
                captured["args"] = args
                self.stdin = None

        monkeypatch.delattr(sys, "frozen", raising=False)
        monkeypatch.setattr(relay.subprocess, "Popen", _FakePopen)

        relay._detached_relay("event", "{}")

        assert captured["args"][1:4] == [
            "-m",
            "runlayer_cli.hook._relay_worker",
            "event",
        ]

    def test_main_routes_sentinel_argv_to_relay_worker(self, monkeypatch):
        """When `aiwatch-enforce __relay_worker__ event` is invoked, the entry
        point must dispatch to the relay worker — NOT re-enter the hook main."""
        called: dict = {"hook_main_ran": False, "relay_args": None}

        def _fake_relay_main():
            called["relay_args"] = list(sys.argv)

        original_dispatch = hook_main._dispatch

        def _spy_dispatch(*args, **kwargs):
            called["hook_main_ran"] = True
            return original_dispatch(*args, **kwargs)

        monkeypatch.setattr(_relay_worker, "main", _fake_relay_main)
        monkeypatch.setattr(hook_main, "_dispatch", _spy_dispatch)
        monkeypatch.setattr(
            sys, "argv", ["/opt/aiwatch-enforce", "__relay_worker__", "event"]
        )
        monkeypatch.setenv("HOOK_EVENT_NAME", "PreToolUse")

        hook_main.main()

        assert called["hook_main_ran"] is False, (
            "Sentinel argv must short-circuit before hook dispatch — "
            "otherwise inherited HOOK_EVENT_NAME causes wrapper JSON to be "
            "processed as a real hook event."
        )
        assert called["relay_args"] == ["/opt/aiwatch-enforce", "event"]

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

    def test_main_routes_sentinel_argv_to_transcript_stream_worker(self, monkeypatch):
        called: dict = {"hook_main_ran": False, "stream_args": None}

        def _fake_stream_main():
            called["stream_args"] = list(sys.argv)

        original_dispatch = hook_main._dispatch

        def _spy_dispatch(*args, **kwargs):
            called["hook_main_ran"] = True
            return original_dispatch(*args, **kwargs)

        monkeypatch.setattr(_transcript_stream_worker, "main", _fake_stream_main)
        monkeypatch.setattr(hook_main, "_dispatch", _spy_dispatch)
        monkeypatch.setattr(
            sys, "argv", ["/opt/aiwatch-enforce", "__transcript_stream_worker__"]
        )
        monkeypatch.setenv("HOOK_EVENT_NAME", "UserPromptSubmit")

        hook_main.main()

        assert called["hook_main_ran"] is False
        assert called["stream_args"] == ["/opt/aiwatch-enforce"]


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

        poster = transcript_stream._make_http_event_poster(debug=True)
        with pytest.raises(RuntimeError, match="network down"):
            poster("claude_code", "message.updated", {"session_id": "s1"})

        assert captured["host"] == "https://tenant.runlayer.test"
        assert captured["url"] == "https://tenant.runlayer.test/api/v1/hooks/events"
        assert captured["kwargs"]["headers"]["x-runlayer-api-key"] == "rl_test"

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

        monkeypatch.setattr(hook_main, "start_transcript_stream", _fake_start)
        monkeypatch.setattr(hook_main, "forward_event", _fake_forward)

        hook_main._dispatch(
            hook_type="UserPromptSubmit",
            original_hook_type="UserPromptSubmit",
            client=Client.CLAUDE_CODE,
            resp=HookResponse(Client.CLAUDE_CODE, "UserPromptSubmit"),
            input_data=payload,
            raw_input=json.dumps(payload),
            enforcement=True,
            debug=False,
        )

        assert capsys.readouterr().out == ""
        assert started == [("claude_code", payload, False)]
        assert forwarded == [("claude_code", "UserPromptSubmit", payload, False)]


class TestForwardStopEvent:
    def test_existing_transcript_does_not_sleep(self, monkeypatch, tmp_path):
        transcript_path = tmp_path / "transcript.jsonl"
        transcript_path.write_text('{"ready":true}\n')
        sleeps: list[float] = []
        captured: list[tuple[str, str]] = []

        def _fake_detached(target, wrapper, *, timeout=None, debug=False):
            captured.append((target, wrapper))

        monkeypatch.setattr(transcript_stream, "_STATE_DIR", tmp_path / "state")
        monkeypatch.setattr(relay.time, "sleep", lambda seconds: sleeps.append(seconds))
        monkeypatch.setattr(relay, "_detached_relay", _fake_detached)

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

        def _fake_detached(target, wrapper, *, timeout=None, debug=False):
            captured.append((target, wrapper))

        monkeypatch.setattr(relay, "_detached_relay", _fake_detached)
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

        def _fake_detached(target, wrapper, *, timeout=None, debug=False):
            captured.append((target, wrapper))

        monkeypatch.setattr(relay, "_detached_relay", _fake_detached)
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

        monkeypatch.setattr(hook_main, "check_tool_lifecycle", _fake_check)
        return captured

    def test_targets_dict_includes_tool_pre_and_tool_post(self):
        assert "tool-pre" in relay._TARGETS
        assert "tool-post" in relay._TARGETS
        assert relay._TARGETS["tool-pre"] == ("/api/v1/hooks/tool/pre", 30)
        assert relay._TARGETS["tool-post"] == ("/api/v1/hooks/tool/post", 30)

    def test_pretooluse_other_tool_routes_to_tool_pre(self, monkeypatch):
        self._capture_detached(monkeypatch)
        checks = self._capture_checks(monkeypatch)
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        hook_main._handle_pre_tool_use(
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={
                "tool_name": "Edit",
                "tool_input": {"file_path": "/tmp/x"},
                "tool_use_id": "edit-1",
            },
            original_hook_type="PreToolUse",
            enforcement=True,
            debug=False,
        )

        target, client_name, event_name, tool_name, payload = checks[0]
        assert target == "tool-pre"
        assert client_name == "claude_code"
        assert event_name == "PreToolUse"
        assert tool_name == "Edit"
        assert payload["tool_use_id"] == "edit-1"

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

        monkeypatch.setattr(hook_main, "enforce", _fake_enforce)

        with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=tmp_path):
            hook_main._handle_pre_tool_use(
                client=Client.HERMES,
                resp=HookResponse(Client.HERMES, "pre_tool_call"),
                input_data={
                    "tool_name": "mcp_linear_44_list_issues",
                    "tool_input": {"query": "runlayer"},
                    "session_id": "session-123",
                },
                original_hook_type="pre_tool_call",
                enforcement=True,
                debug=False,
            )

        assert captured_enforce[0]["client"] == "hermes"
        assert captured_enforce[0]["url"] == "https://mcp.example.com/sse"
        assert captured_enforce[0]["tool_name"] == "mcp_linear_44_list_issues"
        assert json.loads(captured_events[0][1])["event_name"] == "pre_tool_call"

    def test_posttooluse_routes_to_tool_post(self, monkeypatch):
        self._capture_detached(monkeypatch)
        checks = self._capture_checks(monkeypatch, response='{"blocked":false}')
        resp = HookResponse(Client.CLAUDE_CODE, "PostToolUse")
        hook_main._dispatch(
            hook_type="PostToolUse",
            original_hook_type="PostToolUse",
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={"tool_name": "Edit", "tool_response": {"ok": True}},
            raw_input="{}",
            enforcement=True,
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

        monkeypatch.setattr(hook_main, "check_tool_lifecycle", _unexpected_sync_check)
        resp = HookResponse(Client.HERMES, "post_tool_call")
        hook_main._dispatch(
            hook_type="PostToolUse",
            original_hook_type="post_tool_call",
            client=Client.HERMES,
            resp=resp,
            input_data={"tool_name": "write_file", "result": "ok"},
            raw_input="{}",
            enforcement=True,
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
        hook_main._dispatch(
            hook_type="PostToolUse",
            original_hook_type="transform_tool_result",
            client=Client.HERMES,
            resp=resp,
            input_data={"tool_name": "read_file", "result": "secret"},
            raw_input="{}",
            enforcement=True,
            debug=False,
        )

        assert json.loads(capsys.readouterr().out) == "output blocked"

    def test_cursor_stop_forwards_synthetic_session_end(self, monkeypatch, capsys):
        captured = self._capture_detached(monkeypatch)
        resp = HookResponse(Client.CURSOR, "Stop")
        hook_main._dispatch(
            hook_type="Stop",
            original_hook_type="stop",
            client=Client.CURSOR,
            resp=resp,
            input_data={"session_id": "s1", "status": "aborted"},
            raw_input="{}",
            enforcement=False,
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

    def test_pretooluse_no_enforcement_still_forwards_tool_pre(self, monkeypatch):
        captured = self._capture_detached(monkeypatch)

        def _unexpected_sync_check(*args, **kwargs):
            pytest.fail("monitoring mode should not synchronously enforce tool-pre")

        monkeypatch.setattr(hook_main, "check_tool_lifecycle", _unexpected_sync_check)
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        hook_main._handle_pre_tool_use(
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={
                "tool_name": "Edit",
                "tool_input": {"file_path": "/tmp/x"},
                "tool_use_id": "edit-1",
            },
            original_hook_type="PreToolUse",
            enforcement=False,
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

        monkeypatch.setattr(hook_main, "check_tool_lifecycle", _unexpected_sync_check)
        resp = HookResponse(Client.CLAUDE_CODE, "PostToolUse")
        hook_main._dispatch(
            hook_type="PostToolUse",
            original_hook_type="PostToolUse",
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={"tool_name": "Edit", "tool_response": {"ok": True}},
            raw_input="{}",
            enforcement=False,
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
        hook_main._dispatch(
            hook_type="PostToolUseFailure",
            original_hook_type="postToolUseFailure",
            client=Client.CURSOR,
            resp=resp,
            input_data={"tool_name": "Bash", "error": "boom"},
            raw_input="{}",
            enforcement=True,
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
        hook_main._handle_pre_tool_use(
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={
                "tool_name": "Read",
                "tool_input": {"file_path": "/tmp/safe.txt"},
            },
            original_hook_type="PreToolUse",
            enforcement=True,
            debug=False,
        )
        assert checks[0][0] == "tool-pre"

    def test_pretooluse_bash_routes_to_tool_pre(self, monkeypatch):
        self._capture_detached(monkeypatch)
        checks = self._capture_checks(monkeypatch)
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        hook_main._handle_pre_tool_use(
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={
                "tool_name": "Bash",
                "tool_input": {"command": "ls"},
            },
            original_hook_type="PreToolUse",
            enforcement=True,
            debug=False,
        )
        assert checks[0][0] == "tool-pre"

    def test_pretooluse_mcp_skips_local_tool_lifecycle(self, monkeypatch):
        captured = self._capture_detached(monkeypatch)
        checks = self._capture_checks(monkeypatch)
        resp = HookResponse(Client.CURSOR, "preToolUse")
        hook_main._handle_pre_tool_use(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "tool_name": "mcp__linear44__list_issues",
                "tool_input": {"query": "runlayer"},
            },
            original_hook_type="preToolUse",
            enforcement=True,
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

        monkeypatch.setattr(hook_main, "enforce", _fake_enforce)
        monkeypatch.setattr(hook_main, "forward_event", lambda *a, **kw: None)
        with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=tmp_path):
            resp = HookResponse(Client.CODEX, "PreToolUse")
            hook_main._handle_pre_tool_use(
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
                enforcement=True,
                debug=False,
            )

        assert capsys.readouterr().out == ""
        assert captured[0]["hook_event_name"] == "beforeMCPExecution"
        assert captured[0]["client"] == "codex"
        assert captured[0]["conversation_id"] == "session-123"
        assert captured[0]["generation_id"] == "tool-use-456"
        assert captured[0]["tool_name"] == "mcp__linear-44__list_teams"
        assert captured[0]["url"] == "https://mcp.example.com/sse"

    def test_tool_pre_deny_blocks(self, monkeypatch, capsys):
        self._capture_detached(monkeypatch)
        self._capture_checks(
            monkeypatch,
            response='{"permission":"deny","block_reason":"pii detected"}',
        )
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_main._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "Edit",
                    "tool_input": {"file_path": "/tmp/x"},
                },
                original_hook_type="PreToolUse",
                enforcement=True,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
        assert "pii detected" in out["hookSpecificOutput"]["permissionDecisionReason"]

    def test_tool_pre_relay_auth_failure_forwards_event_before_deny(
        self, monkeypatch, capsys
    ):
        captured = self._capture_detached(monkeypatch)

        def _raise_auth_failure(*args, **kwargs):
            raise relay.RelayError(1, "no secret")

        monkeypatch.setattr(hook_main, "check_tool_lifecycle", _raise_auth_failure)
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_main._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "Edit",
                    "tool_input": {"file_path": "/tmp/x"},
                },
                original_hook_type="PreToolUse",
                enforcement=True,
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

    def test_tool_pre_scalar_json_response_denies(self, monkeypatch, capsys):
        self._capture_detached(monkeypatch)
        self._capture_checks(monkeypatch, response="null")
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_main._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "Edit",
                    "tool_input": {"file_path": "/tmp/x"},
                },
                original_hook_type="PreToolUse",
                enforcement=True,
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
            hook_main._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "Edit",
                    "tool_input": {"file_path": "/tmp/x"},
                },
                original_hook_type="PreToolUse",
                enforcement=True,
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
        hook_main._handle_pre_tool_use(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "tool_name": "Edit",
                "tool_input": {"file_path": "/tmp/x", "content": "secret"},
            },
            original_hook_type="preToolUse",
            enforcement=True,
            debug=False,
        )

        out = json.loads(capsys.readouterr().out)
        assert out == {"permission": "allow", "updated_input": modified_args}

    def test_cursor_tool_pre_uses_transcript_id_as_session(self, monkeypatch, capsys):
        self._capture_detached(monkeypatch)
        self._capture_checks(monkeypatch, response='{"permission":"allow"}')
        resp = HookResponse(Client.CURSOR, "preToolUse")
        hook_main._handle_pre_tool_use(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "tool_name": "Edit",
                "transcript_id": "transcript-1",
                "tool_input": {"file_path": "/tmp/x"},
            },
            original_hook_type="preToolUse",
            enforcement=True,
            debug=False,
        )

        out = json.loads(capsys.readouterr().out)
        assert out["updated_input"]["_runlayer_session_id"] == "transcript-1"

    def test_cursor_mcp_pretooluse_uses_chat_id_as_session(self, monkeypatch, capsys):
        self._capture_detached(monkeypatch)
        resp = HookResponse(Client.CURSOR, "preToolUse")
        hook_main._handle_pre_tool_use(
            client=Client.CURSOR,
            resp=resp,
            input_data={
                "tool_name": "mcp__linear44__list_issues",
                "chat_id": "chat-1",
                "tool_input": {"query": "runlayer"},
            },
            original_hook_type="preToolUse",
            enforcement=True,
            debug=False,
        )

        out = json.loads(capsys.readouterr().out)
        assert out["updated_input"]["_runlayer_session_id"] == "chat-1"

    def test_tool_post_block_outputs_block_shape(self, monkeypatch, capsys):
        captured = self._capture_detached(monkeypatch)
        self._capture_checks(
            monkeypatch,
            response='{"blocked":true,"block_reason":"output blocked"}',
        )
        resp = HookResponse(Client.CLAUDE_CODE, "PostToolUse")
        hook_main._dispatch(
            hook_type="PostToolUse",
            original_hook_type="PostToolUse",
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={"tool_name": "Edit", "tool_response": {"ok": True}},
            raw_input="{}",
            enforcement=True,
            debug=False,
        )
        assert json.loads(capsys.readouterr().out) == {
            "decision": "block",
            "reason": "output blocked",
        }
        assert [target for target, _ in captured] == ["event"]
        wrapper = json.loads(captured[0][1])
        assert wrapper["event_name"] == "PostToolUse"
        assert wrapper["payload"]["tool_response"] == {"ok": True}

    def test_tool_post_relay_auth_failure_blocks_output_shape(
        self, monkeypatch, capsys
    ):
        captured = self._capture_detached(monkeypatch)

        def _raise_auth_failure(*args, **kwargs):
            raise relay.RelayError(1, "no secret")

        monkeypatch.setattr(hook_main, "check_tool_lifecycle", _raise_auth_failure)
        resp = HookResponse(Client.CLAUDE_CODE, "PostToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_main._dispatch(
                hook_type="PostToolUse",
                original_hook_type="PostToolUse",
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={"tool_name": "Edit", "tool_response": {"ok": True}},
                raw_input="{}",
                enforcement=True,
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
            hook_main._dispatch(
                hook_type="PostToolUse",
                original_hook_type="PostToolUse",
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={"tool_name": "Edit", "tool_response": {"ok": True}},
                raw_input="{}",
                enforcement=True,
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
            hook_main._dispatch(
                hook_type="PostToolUse",
                original_hook_type="PostToolUse",
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={"tool_name": "Edit", "tool_response": {"ok": True}},
                raw_input="{}",
                enforcement=True,
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
            hook_main._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "Read",
                    "tool_input": json.dumps({"file_path": "/project/.env"}),
                },
                original_hook_type="PreToolUse",
                enforcement=True,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_pretooluse_bash_string_tool_input_blocks_cat_dotenv(self, capsys):
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_main._handle_pre_tool_use(
                client=Client.CLAUDE_CODE,
                resp=resp,
                input_data={
                    "tool_name": "Bash",
                    "tool_input": json.dumps({"command": "cat .env"}),
                },
                original_hook_type="PreToolUse",
                enforcement=True,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_codex_permission_request_string_tool_input_blocks_cat_dotenv(
        self, monkeypatch, capsys
    ):
        monkeypatch.setattr(hook_main, "forward_event", lambda *a, **kw: None)
        resp = HookResponse(Client.CODEX, "PermissionRequest")
        with pytest.raises(SystemExit) as exc:
            hook_main._dispatch(
                hook_type="PermissionRequest",
                original_hook_type="PermissionRequest",
                client=Client.CODEX,
                resp=resp,
                input_data={
                    "tool_input": json.dumps({"command": "cat .env"}),
                },
                raw_input="{}",
                enforcement=True,
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

        def _fake_detached(target, wrapper, *, timeout=None, debug=False):
            captured.append((target, wrapper))

        monkeypatch.setattr(relay, "_detached_relay", _fake_detached)
        monkeypatch.setattr(
            hook_main,
            "check_tool_lifecycle",
            lambda *a, **kw: '{"permission":"allow"}',
        )
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        hook_main._handle_pre_tool_use(
            client=Client.CLAUDE_CODE,
            resp=resp,
            input_data={
                "tool_name": "Read",
                "tool_input": "not-valid-json{",
            },
            original_hook_type="PreToolUse",
            enforcement=True,
            debug=False,
        )
        assert "event" in [t for t, _ in captured]


class TestCursorBeforeMCPResolution:
    def _capture_enforce(self, monkeypatch) -> list[dict[str, object]]:
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        monkeypatch.setattr(hook_main, "enforce", _fake_enforce)
        monkeypatch.setattr(hook_main, "forward_event", lambda *a, **kw: None)
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
        hook_main._handle_before_mcp_execution(
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
            enforcement=True,
            debug=False,
        )

        assert json.loads(capsys.readouterr().out) == {"permission": "allow"}
        assert captured[0]["client"] == "cursor"
        assert captured[0]["url"] == "https://mcp.example.com/sse"
        assert "command" not in captured[0]
        assert captured[0]["tool_input"] == '{"limit": 3}'

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
        hook_main._handle_before_mcp_execution(
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
            enforcement=True,
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
        hook_main._handle_before_mcp_execution(
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
            enforcement=True,
            debug=False,
        )

        assert json.loads(capsys.readouterr().out) == {"permission": "allow"}
        assert captured[0]["command"] == "unknown-server"
        assert "url" not in captured[0]


class TestLoadCredentialsFailClosed:
    """Regression: `_load_credentials` must convert non-RelayError exceptions
    (corrupted YAML producing a non-dict, keyring backend raising an unexpected
    exception, etc.) into ``RelayError(1)``.

    Otherwise the unhandled exception escapes ``enforce()``, escapes the
    ``except RelayError`` clauses in ``_handle_before_mcp_execution`` /
    ``_handle_claude_mcp_tool``, and crashes the hook with exit code 1 — no
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
        monkeypatch.setattr(hook_main, "forward_event", lambda *a, **kw: None)

        resp = HookResponse(Client.CURSOR, "beforeMCPExecution")
        with pytest.raises(SystemExit) as exc:
            hook_main._handle_before_mcp_execution(
                client=Client.CURSOR,
                resp=resp,
                input_data={"tool_name": "mcp__x", "url": "https://x"},
                raw_input="{}",
                original_hook_type="beforeMCPExecution",
                enforcement=True,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["permission"] == "deny"

    def test_handle_claude_mcp_tool_fails_closed_on_corrupt_config(
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
        monkeypatch.setattr(hook_main, "forward_event", lambda *a, **kw: None)

        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        with pytest.raises(SystemExit) as exc:
            hook_main._handle_claude_mcp_tool(
                resp=resp,
                input_data={
                    "tool_name": "mcp__github__list_repos",
                    "cwd": str(tmp_path),
                },
                tool_name="mcp__github__list_repos",
                original_hook_type="PreToolUse",
                enforcement=True,
                debug=False,
            )
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_handle_claude_mcp_tool_sends_cursor_required_fields(
        self, monkeypatch, tmp_path, capsys
    ) -> None:
        mcp_file = tmp_path / ".mcp.json"
        mcp_file.write_text(
            json.dumps(
                {"mcpServers": {"linear-44": {"url": "https://mcp.example.com/sse"}}}
            )
        )
        monkeypatch.setattr(hook_main, "forward_event", lambda *a, **kw: None)
        captured: list[dict[str, object]] = []

        def _fake_enforce(payload: str, *, debug: bool = False) -> str:
            captured.append(json.loads(payload))
            return '{"permission":"allow"}'

        monkeypatch.setattr(hook_main, "enforce", _fake_enforce)

        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        hook_main._handle_claude_mcp_tool(
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
            enforcement=True,
            debug=False,
        )

        assert capsys.readouterr().out == ""
        assert captured[0]["hook_event_name"] == "beforeMCPExecution"
        assert captured[0]["client"] == "claude_code"
        assert captured[0]["conversation_id"] == "session-123"
        assert captured[0]["generation_id"] == "tool-use-456"
        assert captured[0]["tool_name"] == "mcp__linear-44__list_teams"
        assert captured[0]["url"] == "https://mcp.example.com/sse"
