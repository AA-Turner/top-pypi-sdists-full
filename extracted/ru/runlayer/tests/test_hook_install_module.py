"""Unit tests for ``runlayer_cli.hook_install`` (per-client writers + drift checker + tolerant JSON)."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from runlayer_cli.hook_install import (
    Client,
    ClientStatus,
    InstallScope,
    check_all,
    check_client,
    install_client,
)
from runlayer_cli.hook_install.clients import (
    _merge_claude_hooks,
    _merge_cursor_hooks,
    _merge_hermes_hooks,
    hook_command_for_client,
    iter_supported_clients,
)
from runlayer_cli.hook_install.tolerant_json import loads, read_dict


# ── tolerant_json ───────────────────────────────────────────────────


class TestTolerantJson:
    def test_plain_json_parses(self):
        assert loads('{"a": 1}') == {"a": 1}

    def test_line_comments_stripped(self):
        text = """
            {
                // a comment
                "a": 1
            }
        """
        assert loads(text) == {"a": 1}

    def test_trailing_commas_stripped(self):
        text = '{"a": [1, 2,], "b": {"c": 3,}}'
        assert loads(text) == {"a": [1, 2], "b": {"c": 3}}

    def test_read_dict_handles_empty_string(self):
        assert read_dict("") == {}
        assert read_dict("   \n") == {}

    def test_read_dict_coerces_list_to_empty(self):
        assert read_dict("[1, 2, 3]") == {}

    def test_double_slash_inside_string_preserved_with_file_url(self):
        # ``// comment`` forces the cleanup branch; ``file:///`` inside the
        # string value must survive comment stripping.
        text = """
            {
                // a comment
                "url": "file:///Users/me/foo.txt",
            }
        """
        assert loads(text) == {"url": "file:///Users/me/foo.txt"}

    def test_double_slash_inside_string_preserved_with_unc_like_path(self):
        text = """
            {
                // a comment
                "share": "//server/share/foo",
            }
        """
        assert loads(text) == {"share": "//server/share/foo"}

    def test_double_slash_after_escaped_quote_inside_string_preserved(self):
        # Escaped quote inside the string must not flip the in-string state.
        text = r"""
            {
                // a comment
                "weird": "a\"//still-in-string"
            }
        """
        assert loads(text) == {"weird": 'a"//still-in-string'}

    def test_line_comment_after_string_value_still_stripped(self):
        text = """
            {
                "url": "file:///Users/me/foo.txt", // trailing comment
                "a": 1
            }
        """
        assert loads(text) == {"url": "file:///Users/me/foo.txt", "a": 1}


# ── Cursor install ──────────────────────────────────────────────────


class TestCursorInstall:
    def test_writes_hooks_json_into_user_cursor_dir(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        cursor_dir = tmp_path / ".cursor"
        cursor_dir.mkdir()

        result = install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert result.written
        hooks_json = cursor_dir / "hooks.json"
        data = json.loads(hooks_json.read_text())
        assert data["version"] == 1
        assert "beforeMCPExecution" in data["hooks"]
        assert data["hooks"]["beforeMCPExecution"][0]["command"].endswith(
            "aiwatch-hook --client cursor"
        )
        # Enforcement now lives in MDM managed config; the install path no
        # longer writes a sibling runlayer-config.json file.
        assert not (cursor_dir / "hooks" / "runlayer-config.json").exists()

    def test_user_skip_when_client_not_installed(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        result = install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert not result.written
        assert result.skipped_reason == "client not installed"
        assert not (tmp_path / ".cursor").exists()

    def test_user_idempotent_repeat_writes_match(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )
        first = (tmp_path / ".cursor" / "hooks.json").read_text()

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )
        second = (tmp_path / ".cursor" / "hooks.json").read_text()

        assert first == second

    def test_user_preserves_third_party_entries(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        cursor_dir = tmp_path / ".cursor"
        cursor_dir.mkdir()

        third_party_command = "/usr/local/bin/some-other-tool"
        (cursor_dir / "hooks.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "beforeMCPExecution": [{"command": third_party_command}],
                    },
                }
            )
        )

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        data = json.loads((cursor_dir / "hooks.json").read_text())
        commands = [entry["command"] for entry in data["hooks"]["beforeMCPExecution"]]
        assert third_party_command in commands
        assert any(c.endswith("aiwatch-hook --client cursor") for c in commands)

    def test_user_replaces_stale_runlayer_entries(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        cursor_dir = tmp_path / ".cursor"
        cursor_dir.mkdir()

        (cursor_dir / "hooks.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "beforeMCPExecution": [
                            {"command": "/old/path/aiwatch-hook"},
                            {"command": "/usr/local/bin/aiwatch-enforce"},
                        ],
                    },
                }
            )
        )

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command="/new/path/aiwatch-hook",
        )

        data = json.loads((cursor_dir / "hooks.json").read_text())
        commands = [entry["command"] for entry in data["hooks"]["beforeMCPExecution"]]
        assert commands == ["/new/path/aiwatch-hook --client cursor"]


# ── Per-client command hints ───────────────────────────────────────────


class TestHookCommandForClient:
    def test_user_scope_adds_client_arg_for_every_supported_client(self):
        for client in iter_supported_clients():
            command = hook_command_for_client(
                "/usr/local/bin/aiwatch-hook",
                client,
            )

            assert command == f"/usr/local/bin/aiwatch-hook --client {client.value}"


# ── Claude Code install ─────────────────────────────────────────────


class TestClaudeCodeInstall:
    def test_user_writes_settings_json(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        settings = json.loads((claude_dir / "settings.json").read_text())
        assert settings["showThinkingSummaries"] is True
        assert "PreToolUse" in settings["hooks"]
        first_entry = settings["hooks"]["PreToolUse"][0]
        assert first_entry["matcher"] == ""
        assert first_entry["hooks"][0]["command"].endswith(
            "aiwatch-hook --client claude_code"
        )

    def test_user_preserves_unrelated_settings_keys(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        (claude_dir / "settings.json").write_text(
            json.dumps({"theme": "dark", "model": "claude-3"})
        )

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        settings = json.loads((claude_dir / "settings.json").read_text())
        assert settings["theme"] == "dark"
        assert settings["model"] == "claude-3"
        assert "hooks" in settings


# ── Codex install ────────────────────────────────────────────────────


class TestCodexInstall:
    def test_user_enables_features_hooks(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        codex_dir = tmp_path / ".codex"
        codex_dir.mkdir()

        install_client(
            Client.CODEX,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        config_toml = (codex_dir / "config.toml").read_text()
        assert "[features]" in config_toml
        assert "hooks = true" in config_toml
        hooks = json.loads((codex_dir / "hooks.json").read_text())["hooks"]
        command = hooks["PreToolUse"][0]["hooks"][0]["command"]
        assert command.endswith("aiwatch-hook --client codex")

    def test_user_features_hooks_already_set_is_idempotent(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        codex_dir = tmp_path / ".codex"
        codex_dir.mkdir()
        (codex_dir / "config.toml").write_text("[features]\nhooks = true\n")

        install_client(
            Client.CODEX,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        content = (codex_dir / "config.toml").read_text()
        # No duplicate hooks = true lines.
        assert content.count("hooks = true") == 1


# ── Hermes install ───────────────────────────────────────────────────


class TestHermesInstall:
    def test_user_writes_config_yaml(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        hermes_dir = tmp_path / ".hermes"
        hermes_dir.mkdir()

        result = install_client(
            Client.HERMES,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert result.written
        config = yaml.safe_load((hermes_dir / "config.yaml").read_text())
        assert "pre_tool_call" in config["hooks"]
        assert config["hooks"]["pre_tool_call"][0]["command"].endswith(
            "aiwatch-hook --client hermes"
        )
        assert "transform_tool_result" in config["hooks"]
        # Pipeline events not registered by default.
        assert "post_tool_call" not in config["hooks"]

    def test_user_include_pipeline_registers_event_hooks(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".hermes").mkdir()

        install_client(
            Client.HERMES,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        hooks = yaml.safe_load((tmp_path / ".hermes" / "config.yaml").read_text())[
            "hooks"
        ]
        for name in ("post_tool_call", "pre_llm_call", "on_session_start"):
            assert name in hooks

    def test_user_skip_when_client_not_installed(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        result = install_client(
            Client.HERMES,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert not result.written
        assert result.skipped_reason == "client not installed"

    def test_user_preserves_top_level_yaml_keys(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        hermes_dir = tmp_path / ".hermes"
        hermes_dir.mkdir()
        (hermes_dir / "config.yaml").write_text(
            yaml.safe_dump(
                {
                    "mcp_servers": {"linear": {"url": "https://linear.example/mcp"}},
                    "hooks": {
                        "pre_tool_call": [{"command": "/other/tool"}],
                    },
                }
            )
        )

        install_client(
            Client.HERMES,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        config = yaml.safe_load((hermes_dir / "config.yaml").read_text())
        assert config["mcp_servers"]["linear"]["url"] == "https://linear.example/mcp"
        commands = [entry["command"] for entry in config["hooks"]["pre_tool_call"]]
        assert "/other/tool" in commands
        assert any(c.endswith("aiwatch-hook --client hermes") for c in commands)

    def test_user_replaces_stale_runlayer_entries(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        hermes_dir = tmp_path / ".hermes"
        hermes_dir.mkdir()
        (hermes_dir / "config.yaml").write_text(
            yaml.safe_dump(
                {
                    "hooks": {
                        "pre_tool_call": [
                            {"command": "/old/path/aiwatch-hook"},
                            {"command": "/usr/local/bin/aiwatch-enforce"},
                        ]
                    }
                }
            )
        )

        install_client(
            Client.HERMES,
            scope=InstallScope.USER,
            hook_command="/new/path/aiwatch-hook",
        )

        config = yaml.safe_load((hermes_dir / "config.yaml").read_text())
        commands = [entry["command"] for entry in config["hooks"]["pre_tool_call"]]
        assert commands == ["/new/path/aiwatch-hook --client hermes"]


# ── Install never writes runlayer-config.json (enforcement lives in MDM) ───


class TestInstallDoesNotWriteRuntimeConfig:
    """The bundle install path delegates enforcement to MDM managed config;
    no sibling runlayer-config.json should ever be written."""

    def test_user_install_does_not_write_runtime_config(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()
        bin_dir = tmp_path / "usr" / "local" / "bin"
        bin_dir.mkdir(parents=True)
        hook_binary = bin_dir / "aiwatch-hook"

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command=str(hook_binary),
        )

        assert not (tmp_path / ".cursor" / "hooks" / "runlayer-config.json").exists()
        assert not (bin_dir / "runlayer-config.json").exists()

    def test_mdm_install_does_not_write_runtime_config(self, tmp_path, monkeypatch):
        from runlayer_cli.hook_install import clients as clients_module

        enterprise_root = tmp_path / "enterprise" / "Cursor"
        monkeypatch.setattr(
            clients_module, "enterprise_cursor_dir", lambda: enterprise_root
        )
        bin_dir = tmp_path / "usr" / "local" / "bin"
        bin_dir.mkdir(parents=True)
        hook_binary = bin_dir / "aiwatch-hook"

        install_client(
            Client.CURSOR,
            scope=InstallScope.MDM,
            hook_command=str(hook_binary),
        )

        assert not (enterprise_root / "hooks" / "runlayer-config.json").exists()
        assert not (bin_dir / "runlayer-config.json").exists()


# ── check / drift detection ─────────────────────────────────────────


class TestCheck:
    def test_user_reports_client_not_installed(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        result = check_client(Client.CURSOR, scope=InstallScope.USER)
        assert result.status == ClientStatus.CLIENT_NOT_INSTALLED

    def test_user_reports_missing_when_no_config_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()
        result = check_client(Client.CURSOR, scope=InstallScope.USER)
        assert result.status == ClientStatus.MISSING

    def test_user_reports_ok_when_command_matches(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()
        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )
        result = check_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch-hook",
            include_pipeline=False,
        )
        assert result.status == ClientStatus.OK

    def test_user_reports_drifted_when_command_mismatches(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()
        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command="/old/path/aiwatch-hook",
        )
        result = check_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            expected_hook_command="/new/path/aiwatch-hook",
        )
        assert result.status == ClientStatus.DRIFTED

    def test_check_all_returns_one_per_client(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        results = check_all(
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch-hook",
        )
        assert {r.client for r in results} == {
            Client.CURSOR,
            Client.CLAUDE_CODE,
            Client.CODEX,
            Client.HERMES,
        }

    def test_user_reports_ok_for_hermes_when_command_matches(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".hermes").mkdir()
        install_client(
            Client.HERMES,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )
        result = check_client(
            Client.HERMES,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch-hook",
            include_pipeline=False,
        )
        assert result.status == ClientStatus.OK

    def test_user_reports_drifted_for_hermes_when_command_mismatches(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".hermes").mkdir()
        install_client(
            Client.HERMES,
            scope=InstallScope.USER,
            hook_command="/old/path/aiwatch-hook",
        )
        result = check_client(
            Client.HERMES,
            scope=InstallScope.USER,
            expected_hook_command="/new/path/aiwatch-hook",
        )
        assert result.status == ClientStatus.DRIFTED

    def test_mdm_reports_drifted_when_event_hooks_missing(self, tmp_path, monkeypatch):
        """Enforcement-only install is DRIFTED when the event set is expected."""
        from runlayer_cli.hook_install import clients as clients_module

        enterprise_root = tmp_path / "enterprise" / "Cursor"
        monkeypatch.setattr(
            clients_module, "enterprise_cursor_dir", lambda: enterprise_root
        )

        install_client(
            Client.CURSOR,
            scope=InstallScope.MDM,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        result = check_client(
            Client.CURSOR,
            scope=InstallScope.MDM,
            expected_hook_command="/usr/local/bin/aiwatch hook",
            include_pipeline=True,
        )

        assert result.status == ClientStatus.DRIFTED
        assert "missing event hooks" in result.detail

    def test_mdm_reports_ok_when_full_event_set_present(self, tmp_path, monkeypatch):
        from runlayer_cli.hook_install import clients as clients_module

        enterprise_root = tmp_path / "enterprise" / "Cursor"
        monkeypatch.setattr(
            clients_module, "enterprise_cursor_dir", lambda: enterprise_root
        )

        install_client(
            Client.CURSOR,
            scope=InstallScope.MDM,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        result = check_client(
            Client.CURSOR,
            scope=InstallScope.MDM,
            expected_hook_command="/usr/local/bin/aiwatch hook",
            include_pipeline=True,
        )

        assert result.status == ClientStatus.OK

    def test_mdm_claude_code_reports_ok_from_console_home(self, tmp_path, monkeypatch):
        """MDM Claude Code drift check reads the console user's ~/.claude
        link-safe and reports OK when the install is present."""
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import console_user as console_user_module

        console_home = tmp_path / "Users" / "alice"
        console_claude_root = console_home / ".claude"
        monkeypatch.setattr(
            clients_module, "enterprise_claude_code_dir", lambda: console_claude_root
        )
        monkeypatch.setattr(
            console_user_module, "find_console_user_home", lambda: console_home
        )

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        result = check_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            expected_hook_command="/usr/local/bin/aiwatch hook",
            include_pipeline=True,
        )

        assert result.status == ClientStatus.OK

    def test_mdm_claude_code_check_refuses_symlinked_settings(
        self, tmp_path, monkeypatch
    ):
        """Regression (ENG-3217): a planted ``~/.claude/settings.json`` symlink
        must not let the root drift check read a file outside the home. The
        link-safe read returns nothing -> MISSING; the outside target (which
        contains a valid-looking Runlayer hook) is never followed."""
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import console_user as console_user_module

        console_home = tmp_path / "Users" / "alice"
        console_claude_root = console_home / ".claude"
        console_claude_root.mkdir(parents=True)
        outside = tmp_path / "outside.json"
        outside.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/usr/local/bin/aiwatch hook "
                                        "--client claude_code",
                                    }
                                ],
                            }
                        ]
                    }
                }
            )
        )
        (console_claude_root / "settings.json").symlink_to(outside)
        monkeypatch.setattr(
            clients_module, "enterprise_claude_code_dir", lambda: console_claude_root
        )
        monkeypatch.setattr(
            console_user_module, "find_console_user_home", lambda: console_home
        )

        result = check_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            expected_hook_command="/usr/local/bin/aiwatch hook",
            include_pipeline=True,
        )

        # Symlink not followed: the outside hooks were never read.
        assert result.status == ClientStatus.MISSING

    def test_mdm_hermes_check_refuses_symlinked_config(self, tmp_path, monkeypatch):
        """Regression (ENG-3217): a planted ``~/.hermes/config.yaml`` symlink is
        not followed by the root drift check."""
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import console_user as console_user_module

        console_home = tmp_path / "Users" / "alice"
        console_hermes_root = console_home / ".hermes"
        console_hermes_root.mkdir(parents=True)
        outside = tmp_path / "outside.yaml"
        outside.write_text(
            yaml.safe_dump(
                {
                    "hooks": {
                        "pre_tool_call": [
                            {"command": "/usr/local/bin/aiwatch hook --client hermes"}
                        ]
                    }
                }
            )
        )
        (console_hermes_root / "config.yaml").symlink_to(outside)
        monkeypatch.setattr(
            clients_module, "enterprise_hermes_dir", lambda: console_hermes_root
        )
        monkeypatch.setattr(
            console_user_module, "find_console_user_home", lambda: console_home
        )

        result = check_client(
            Client.HERMES,
            scope=InstallScope.MDM,
            expected_hook_command="/usr/local/bin/aiwatch hook",
            include_pipeline=True,
        )

        assert result.status == ClientStatus.MISSING


# ── merge helpers ────────────────────────────────────────────────────


class TestMergeHelpers:
    def test_merge_cursor_preserves_third_party_only_dropping_old_runlayer(self):
        existing = {
            "beforeMCPExecution": [
                {"command": "/old/path/aiwatch-hook"},
                {"command": "/usr/local/bin/some-other"},
            ],
        }
        runlayer = {
            "beforeMCPExecution": [{"command": "/new/path/aiwatch-hook"}],
        }
        merged = _merge_cursor_hooks(existing, runlayer)
        commands = [h["command"] for h in merged["beforeMCPExecution"]]
        assert commands == ["/usr/local/bin/some-other", "/new/path/aiwatch-hook"]

    def test_merge_hermes_preserves_third_party_only_dropping_old_runlayer(self):
        existing = {
            "pre_tool_call": [
                {"command": "/old/path/aiwatch-hook"},
                {"command": "/usr/local/bin/some-other"},
            ],
        }
        runlayer = {
            "pre_tool_call": [{"command": "/new/path/aiwatch-hook"}],
        }
        merged = _merge_hermes_hooks(existing, runlayer)
        commands = [h["command"] for h in merged["pre_tool_call"]]
        assert commands == ["/usr/local/bin/some-other", "/new/path/aiwatch-hook"]

    def test_merge_claude_replaces_runlayer_nested(self):
        existing = {
            "PreToolUse": [
                {"matcher": "", "hooks": [{"command": "/old/aiwatch-hook"}]},
                {"matcher": "Bash", "hooks": [{"command": "/usr/bin/echo"}]},
            ]
        }
        runlayer = {
            "PreToolUse": [{"matcher": "", "hooks": [{"command": "/new/aiwatch-hook"}]}]
        }
        merged = _merge_claude_hooks(existing, runlayer)
        # Third-party preserved + new runlayer appended.
        assert any(entry.get("matcher") == "Bash" for entry in merged["PreToolUse"])
        assert any(
            entry["hooks"][0]["command"] == "/new/aiwatch-hook"
            for entry in merged["PreToolUse"]
        )
        # Old runlayer entry gone.
        assert all(
            entry["hooks"][0]["command"] != "/old/aiwatch-hook"
            for entry in merged["PreToolUse"]
        )
