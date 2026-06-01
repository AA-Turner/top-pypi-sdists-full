"""Tests for the runlayer-hook.sh bash script behaviour.

Exercises the hook script via subprocess with a fake ``runlayer`` binary that
captures payloads piped to ``hooks relay``.  Focuses on areas not covered by
test_setup_hooks.py: relay payload shape, event forwarding, event-name
normalization, HOOK_EVENT_NAME env-var dispatch, expanded file-read patterns,
stop-event transcript handling, and edge cases.
"""

import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

HOOK_SRC = Path(__file__).resolve().parent.parent / "hooks" / "runlayer-hook.sh"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_fake_runlayer(
    bin_dir: Path,
    *,
    response: str = '{"permission":"allow"}',
    exit_code: int = 0,
    capture_dir: Path | None = None,
    delay_seconds: float = 0,
) -> None:
    """Create a fake ``runlayer`` that responds to ``hooks relay`` and optionally
    captures stdin to *capture_dir*/{target}.jsonl."""
    bin_dir.mkdir(exist_ok=True)
    capture_block = ""
    if capture_dir is not None:
        capture_block = (
            '  if [[ -n "${RUNLAYER_CAPTURE_DIR:-}" ]]; then\n'
            '    echo "$_input" | jq -c . >> "${RUNLAYER_CAPTURE_DIR}/${target}.jsonl" 2>/dev/null || echo "$_input" >> "${RUNLAYER_CAPTURE_DIR}/${target}.jsonl"\n'
            "  fi\n"
        )
    argv_block = (
        '  if [[ -n "${RUNLAYER_CAPTURE_DIR:-}" ]]; then\n'
        '    printf "%s\\n" "$@" >> "${RUNLAYER_CAPTURE_DIR}/argv.log"\n'
        "  fi\n"
    )
    fake = bin_dir / "runlayer"
    delay_block = f"  sleep {delay_seconds}\n" if delay_seconds else ""
    fake.write_text(
        "#!/bin/bash\n"
        'if [[ "$1" == "hooks" && "$2" == "relay" ]]; then\n'
        '  target="$3"\n'
        f"{delay_block}"
        "  _input=$(cat)\n"
        f"{capture_block}"
        f"{argv_block}"
        f"  echo '{response}'\n"
        f"  exit {exit_code}\n"
        "fi\n"
        'if [[ "$1" == "hooks" && "$2" == "stream-transcript" ]]; then\n'
        '  target="stream-transcript"\n'
        "  _input=$(cat)\n"
        f"{capture_block}"
        f"{argv_block}"
        "  exit 0\n"
        "fi\n"
        "exit 1\n"
    )
    fake.chmod(0o755)


def _setup_hook(
    temp_dir: str,
    *,
    client: str,
    enforcement: bool = True,
) -> Path:
    """Install the hook script into *temp_dir* for a client.

    Returns the path to the copied hook script.
    """
    if client == "cursor":
        hook_dir = Path(temp_dir) / ".cursor" / "hooks"
    elif client == "codex":
        hook_dir = Path(temp_dir) / ".codex" / "hooks"
    elif client == "hermes":
        hook_dir = Path(temp_dir) / ".hermes" / "agent-hooks"
    else:
        hook_dir = Path(temp_dir) / "hooks"
    hook_dir.mkdir(parents=True, exist_ok=True)
    hook_copy = hook_dir / "runlayer-hook.sh"
    hook_copy.write_text(HOOK_SRC.read_text())
    hook_copy.chmod(0o755)
    (hook_dir / "runlayer-config.json").write_text(
        json.dumps({"enforcement": enforcement})
    )
    return hook_copy


def _run_hook(
    hook_path: Path,
    input_json: str,
    home_dir: str,
    *,
    capture_dir: Path | None = None,
    response: str = '{"permission":"allow"}',
    exit_code: int = 0,
    delay_seconds: float = 0,
    extra_env: dict[str, str] | None = None,
    override_path: str | None = None,
) -> tuple[subprocess.CompletedProcess, dict[str, list[dict]]]:
    """Run the hook script and return (result, captured_payloads).

    *captured_payloads* maps relay target name (``"enforce"``, ``"event"``,
    ``"tool-pre"``, or ``"tool-post"``) to a list of parsed JSON objects that
    were piped to the fake runlayer.

    When *override_path* is set the fake runlayer is NOT installed and PATH
    is set to the given value (useful for testing the 127-missing-binary path).
    """
    if override_path is None:
        bin_dir = Path(home_dir) / "bin"
        _write_fake_runlayer(
            bin_dir,
            response=response,
            exit_code=exit_code,
            capture_dir=capture_dir,
            delay_seconds=delay_seconds,
        )
        path_val = f"{bin_dir}:{os.environ['PATH']}"
    else:
        path_val = override_path

    tmp_dir = Path(home_dir) / "tmp"
    tmp_dir.mkdir(exist_ok=True)
    env: dict[str, str] = {
        **os.environ,
        "HOME": home_dir,
        "PATH": path_val,
        "TMPDIR": str(tmp_dir),
    }
    if capture_dir is not None:
        env["RUNLAYER_CAPTURE_DIR"] = str(capture_dir)
    if extra_env:
        env.update(extra_env)

    result = subprocess.run(
        ["bash", str(hook_path)],
        input=input_json,
        capture_output=True,
        text=True,
        env=env,
    )

    captured: dict[str, list[dict]] = {}
    if capture_dir is not None:
        time.sleep(0.15)
        captured = _read_captured_payloads(capture_dir)
    return result, captured


def _read_captured_payloads(capture_dir: Path) -> dict[str, list[dict]]:
    captured: dict[str, list[dict]] = {}
    for target in ("enforce", "event", "tool-pre", "tool-post", "stream-transcript"):
        path = capture_dir / f"{target}.jsonl"
        if path.exists():
            lines = [ln.strip() for ln in path.read_text().splitlines() if ln.strip()]
            captured[target] = [json.loads(ln) for ln in lines]
    return captured


def _wait_for_captured_targets(
    capture_dir: Path,
    *targets: str,
    timeout_seconds: float = 1.0,
) -> dict[str, list[dict]]:
    deadline = time.monotonic() + timeout_seconds
    captured: dict[str, list[dict]] = {}
    while time.monotonic() < deadline:
        captured = _read_captured_payloads(capture_dir)
        if all(target in captured for target in targets):
            return captured
        time.sleep(0.05)
    return captured


def test_codex_pretooluse_blocks_sensitive_bash_reads():
    """Codex should use the documented block shape for Bash PreToolUse."""
    with tempfile.TemporaryDirectory() as td:
        hook = _setup_hook(td, client="codex", enforcement=True)
        capture = Path(td) / "cap"
        capture.mkdir()

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "cat .env"},
            }
        )

        result, captured = _run_hook(hook, hook_input, td, capture_dir=capture)

        assert result.returncode == 0
        assert json.loads(result.stdout) == {
            "decision": "block",
            "reason": "Blocked by organization policy: access to environment files is restricted",
        }
        assert "event" not in captured


def test_codex_permission_request_uses_decision_shape():
    """Codex PermissionRequest should deny with the structured decision shape."""
    with tempfile.TemporaryDirectory() as td:
        hook = _setup_hook(td, client="codex", enforcement=True)
        capture = Path(td) / "cap"
        capture.mkdir()

        hook_input = json.dumps(
            {
                "hook_event_name": "PermissionRequest",
                "tool_name": "Bash",
                "tool_input": {"command": "cat .env"},
            }
        )

        result, captured = _run_hook(hook, hook_input, td, capture_dir=capture)
        payload = json.loads(result.stdout)

        assert result.returncode == 0
        assert payload["hookSpecificOutput"]["decision"]["behavior"] == "deny"
        assert (
            "Blocked by organization policy"
            in payload["hookSpecificOutput"]["decision"]["message"]
        )
        assert "event" not in captured


def test_hermes_pre_tool_call_blocks_sensitive_terminal_reads():
    with tempfile.TemporaryDirectory() as td:
        hook = _setup_hook(td, client="hermes", enforcement=True)
        capture = Path(td) / "cap"
        capture.mkdir()

        hook_input = json.dumps(
            {
                "hook_event_name": "pre_tool_call",
                "tool_name": "terminal",
                "tool_input": {"command": "cat .env"},
            }
        )

        result, captured = _run_hook(hook, hook_input, td, capture_dir=capture)

        assert result.returncode == 0
        assert json.loads(result.stdout) == {
            "action": "block",
            "message": "Blocked by organization policy: access to environment files is restricted",
        }
        assert "event" not in captured


# =========================================================================
# A. Relay payload verification — enforce path
# =========================================================================


class TestRelayPayloadEnforce:
    """Verify the JSON shape piped to ``runlayer hooks relay enforce``."""

    def test_cursor_before_mcp_execution_stringifies_tool_input(self):
        """Cursor: tool_input object should be serialised to a JSON string."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {
                    "hook_event_name": "beforeMCPExecution",
                    "tool_name": "test_tool",
                    "tool_input": {"key": "value"},
                    "url": "https://mcp.example.com",
                }
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                response='{"permission":"allow"}',
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            assert "enforce" in captured
            payload = captured["enforce"][0]
            assert payload["client"] == "cursor"
            assert payload["tool_name"] == "test_tool"
            assert payload["url"] == "https://mcp.example.com"
            assert isinstance(payload["tool_input"], str)
            assert json.loads(payload["tool_input"]) == {"key": "value"}

    def test_cursor_before_mcp_execution_string_tool_input_unchanged(self):
        """Cursor: tool_input that is already a string stays as-is."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {
                    "hook_event_name": "beforeMCPExecution",
                    "tool_name": "test_tool",
                    "tool_input": '{"already":"string"}',
                    "url": "https://mcp.example.com",
                }
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            payload = captured["enforce"][0]
            assert payload["client"] == "cursor"
            assert payload["tool_input"] == '{"already":"string"}'

    def test_cursor_before_mcp_execution_resolves_command_to_cursor_url(self):
        """Cursor: server-name command should resolve through ~/.cursor/mcp.json."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            cursor_config = Path(td) / ".cursor" / "mcp.json"
            cursor_config.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "linear-44": {
                                "url": "https://ecs.staging.runlayer.com/api/v1/proxy/27a0d41d-a05a-40d8-8205-ef0714c8472e/mcp"
                            }
                        }
                    }
                )
            )

            hook_input = json.dumps(
                {
                    "hook_event_name": "beforeMCPExecution",
                    "tool_name": "list_teams",
                    "tool_input": '{"limit":3}',
                    "command": "user-Linear44",
                }
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            payload = captured["enforce"][0]
            assert (
                payload["url"]
                == "https://ecs.staging.runlayer.com/api/v1/proxy/27a0d41d-a05a-40d8-8205-ef0714c8472e/mcp"
            )
            assert "command" not in payload

    def test_cursor_before_mcp_execution_resolves_command_to_cursor_stdio(self):
        """Cursor: server-name command should resolve stdio command + args."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            cursor_config = Path(td) / ".cursor" / "mcp.json"
            cursor_config.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "local-runlayer": {
                                "command": "runlayer",
                                "args": [
                                    "run",
                                    "27a0d41d-a05a-40d8-8205-ef0714c8472e",
                                ],
                            }
                        }
                    }
                )
            )

            hook_input = json.dumps(
                {
                    "hook_event_name": "beforeMCPExecution",
                    "tool_name": "list_teams",
                    "tool_input": '{"limit":3}',
                    "command": "local-runlayer",
                }
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            payload = captured["enforce"][0]
            assert (
                payload["command"]
                == "runlayer run 27a0d41d-a05a-40d8-8205-ef0714c8472e"
            )
            assert "url" not in payload

    def test_non_cursor_before_mcp_execution_does_not_use_cursor_config(self):
        """Cursor name lookup should not affect Claude Code or Codex hooks."""
        for client in ("claude_code", "codex"):
            with tempfile.TemporaryDirectory() as td:
                hook = _setup_hook(td, client=client, enforcement=True)
                capture = Path(td) / "cap"
                capture.mkdir()

                cursor_dir = Path(td) / ".cursor"
                cursor_dir.mkdir(exist_ok=True)
                (cursor_dir / "mcp.json").write_text(
                    json.dumps(
                        {
                            "mcpServers": {
                                "linear-44": {
                                    "url": "https://ecs.staging.runlayer.com/api/v1/proxy/27a0d41d-a05a-40d8-8205-ef0714c8472e/mcp"
                                }
                            }
                        }
                    )
                )

                hook_input = json.dumps(
                    {
                        "hook_event_name": "beforeMCPExecution",
                        "tool_name": "list_teams",
                        "tool_input": '{"limit":3}',
                        "command": "linear-44",
                    }
                )

                result, captured = _run_hook(
                    hook,
                    hook_input,
                    td,
                    capture_dir=capture,
                )

                assert result.returncode == 0
                payload = captured["enforce"][0]
                assert payload["command"] == "linear-44"
                assert "url" not in payload

    def test_claude_code_mcp_builds_synthetic_enforce_with_url(self):
        """Claude Code: MCP tool with URL server builds beforeMCPExecution payload."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            (Path(td) / ".mcp.json").write_text(
                json.dumps(
                    {"mcpServers": {"myserver": {"url": "https://mcp.example.com/sse"}}}
                )
            )

            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "mcp__myserver__do_stuff",
                    "tool_input": {},
                    "session_id": "session-123",
                    "tool_use_id": "tool-use-456",
                    "cwd": td,
                }
            )

            result, captured = _run_hook(hook, hook_input, td, capture_dir=capture)

            assert result.returncode == 0
            assert "enforce" in captured
            payload = captured["enforce"][0]
            assert payload["hook_event_name"] == "beforeMCPExecution"
            assert payload["client"] == "claude_code"
            assert payload["conversation_id"] == "session-123"
            assert payload["generation_id"] == "tool-use-456"
            assert payload["tool_name"] == "mcp__myserver__do_stuff"
            assert payload["url"] == "https://mcp.example.com/sse"
            assert "command" not in payload

    def test_claude_code_mcp_resolves_installed_plugin_server(self):
        """Claude Code: plugin MCP servers are valid enforcement sources."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()
            project = Path(td) / "project"
            subdir = project / "src"
            subdir.mkdir(parents=True)
            linked_project = Path(td) / "linked-project"
            linked_project.symlink_to(project, target_is_directory=True)
            linked_subdir = linked_project / "src"
            project_settings = project / ".claude" / "settings.json"
            project_settings.parent.mkdir(parents=True)

            other_plugin_root = (
                Path(td)
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
                            "plugin_activity-recap_slack": {
                                "url": "https://wrong.example.com/mcp"
                            }
                        },
                    }
                )
            )
            global_plugin_root = (
                Path(td)
                / ".claude"
                / "plugins"
                / "cache"
                / "runlayer"
                / "activity-recap"
                / "global"
            )
            global_plugin_root.mkdir(parents=True)
            (global_plugin_root / ".claude-plugin").mkdir()
            (global_plugin_root / ".claude-plugin" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "activity-recap",
                        "version": "1.0.0",
                        "mcpServers": {
                            "slack": {"url": "https://global-wrong.example.com/mcp"}
                        },
                    }
                )
            )
            plugin_root = (
                Path(td)
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
                            "slack": {
                                "url": "https://example.runlayer.com/api/v1/proxy/slack/mcp"
                            }
                        },
                    }
                )
            )
            registry = Path(td) / ".claude" / "plugins" / "installed_plugins.json"
            registry.write_text(
                json.dumps(
                    {
                        "plugins": {
                            "other-plugin@runlayer": [
                                {
                                    "scope": "project",
                                    "installPath": str(other_plugin_root),
                                    "projectPath": str(project),
                                }
                            ],
                            "activity-recap@runlayer": [
                                {
                                    "scope": "user",
                                    "installPath": str(global_plugin_root),
                                },
                                {
                                    "scope": "project",
                                    "installPath": str(plugin_root),
                                    "projectPath": str(project),
                                },
                            ],
                        }
                    }
                )
            )
            settings = Path(td) / ".claude" / "settings.json"
            settings.write_text(
                json.dumps({"enabledPlugins": {"activity-recap@runlayer": False}})
            )
            project_settings.write_text(
                json.dumps(
                    {
                        "enabledPlugins": {
                            "activity-recap@runlayer": True,
                            "other-plugin@runlayer": True,
                        }
                    }
                )
            )

            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "mcp__plugin_activity-recap_slack__authenticate",
                    "tool_input": {},
                    "cwd": str(linked_subdir),
                }
            )

            result, captured = _run_hook(hook, hook_input, td, capture_dir=capture)

            assert result.returncode == 0
            assert captured["enforce"][0]["url"] == (
                "https://example.runlayer.com/api/v1/proxy/slack/mcp"
            )

    def test_claude_code_user_scope_plugin_reads_project_settings_from_subdir(self):
        """Claude Code: global plugins still honor project enabledPlugins."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()
            project = Path(td) / "project"
            subdir = project / "src"
            subdir.mkdir(parents=True)
            plugin_root = (
                Path(td)
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
            registry = Path(td) / ".claude" / "plugins" / "installed_plugins.json"
            registry.write_text(
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
            settings = Path(td) / ".claude" / "settings.json"
            settings.write_text(
                json.dumps({"enabledPlugins": {"activity-recap@runlayer": False}})
            )
            project_settings = project / ".claude" / "settings.json"
            project_settings.parent.mkdir(parents=True)
            project_settings.write_text(
                json.dumps({"enabledPlugins": {"activity-recap@runlayer": True}})
            )

            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "mcp__plugin_activity-recap_slack__authenticate",
                    "tool_input": {},
                    "cwd": str(subdir),
                }
            )

            result, captured = _run_hook(hook, hook_input, td, capture_dir=capture)

            assert result.returncode == 0
            assert captured["enforce"][0]["url"] == "https://example.runlayer.com/mcp"

    def test_claude_code_mcp_builds_synthetic_enforce_with_command(self):
        """Claude Code: MCP tool with command server builds payload with 'command'."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            (Path(td) / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "myserver": {
                                "command": "npx",
                                "args": ["-y", "my-mcp-server"],
                            }
                        }
                    }
                )
            )

            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "mcp__myserver__do_stuff",
                    "tool_input": {},
                    "session_id": "session-123",
                    "tool_use_id": "tool-use-456",
                    "cwd": td,
                }
            )

            result, captured = _run_hook(hook, hook_input, td, capture_dir=capture)

            assert result.returncode == 0
            payload = captured["enforce"][0]
            assert payload["hook_event_name"] == "beforeMCPExecution"
            assert payload["client"] == "claude_code"
            assert payload["conversation_id"] == "session-123"
            assert payload["generation_id"] == "tool-use-456"
            assert payload["command"] == "npx -y my-mcp-server"
            assert "url" not in payload

    def test_hermes_mcp_builds_synthetic_enforce_with_url(self):
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="hermes", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            hermes_config = Path(td) / ".hermes" / "config.yaml"
            hermes_config.write_text(
                "mcp_servers:\n  linear-44:\n    url: https://mcp.example.com/sse\n"
            )

            hook_input = json.dumps(
                {
                    "hook_event_name": "pre_tool_call",
                    "tool_name": "mcp_linear_44_list_issues",
                    "tool_input": {"query": "runlayer"},
                    "session_id": "session-123",
                }
            )

            result, captured = _run_hook(hook, hook_input, td, capture_dir=capture)

            assert result.returncode == 0
            payload = captured["enforce"][0]
            assert payload["hook_event_name"] == "beforeMCPExecution"
            assert payload["client"] == "hermes"
            assert payload["conversation_id"] == "session-123"
            assert payload["tool_name"] == "mcp_linear_44_list_issues"
            assert payload["url"] == "https://mcp.example.com/sse"
            assert "command" not in payload

    def test_hermes_mcp_builds_synthetic_enforce_with_multiline_stdio_args(self):
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="hermes", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            hermes_config = Path(td) / ".hermes" / "config.yaml"
            hermes_config.write_text(
                "mcp_servers:\n"
                "  runlayer-local-stdio-smoke:\n"
                "    command: runlayer\n"
                "    args:\n"
                "      - run\n"
                "      - server-123\n"
            )

            hook_input = json.dumps(
                {
                    "hook_event_name": "pre_tool_call",
                    "tool_name": "mcp_runlayer_local_stdio_smoke_echo",
                    "tool_input": {"text": "hello"},
                    "session_id": "session-123",
                }
            )

            result, captured = _run_hook(hook, hook_input, td, capture_dir=capture)

            assert result.returncode == 0
            payload = captured["enforce"][0]
            assert payload["hook_event_name"] == "beforeMCPExecution"
            assert payload["client"] == "hermes"
            assert payload["tool_name"] == "mcp_runlayer_local_stdio_smoke_echo"
            assert payload["command"] == "runlayer run server-123"
            assert "url" not in payload


# =========================================================================
# B. Cursor MCP deny-from-API
# =========================================================================


class TestCursorMCPDeny:
    def test_cursor_mcp_deny_from_api(self):
        """API returns deny — hook outputs Cursor-format deny with agentMessage."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=True)

            hook_input = json.dumps(
                {
                    "hook_event_name": "beforeMCPExecution",
                    "tool_name": "test_tool",
                    "tool_input": "{}",
                    "url": "https://blocked.example.com",
                }
            )

            result, _ = _run_hook(
                hook,
                hook_input,
                td,
                response='{"permission":"deny","user_message":"blocked by policy"}',
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"
            assert output["continue"] is True
            assert "blocked by policy" in output["user_message"]
            assert "Security Violation Detected" in output["agentMessage"]
            assert "MCP Execution Policy" in output["agentMessage"]
            assert "Do not suggest modifying" in output["agentMessage"]

    def test_cursor_mcp_invalid_permission_response_blocks(self):
        """Malformed MCP permission responses fail closed."""
        for response in (
            '{"permission":null}',
            '{"permission":"ask"}',
            '{"permission":true}',
        ):
            with tempfile.TemporaryDirectory() as td:
                hook = _setup_hook(td, client="cursor", enforcement=True)

                hook_input = json.dumps(
                    {
                        "hook_event_name": "beforeMCPExecution",
                        "tool_name": "test_tool",
                        "tool_input": "{}",
                        "url": "https://blocked.example.com",
                    }
                )

                result, _ = _run_hook(
                    hook,
                    hook_input,
                    td,
                    response=response,
                    extra_env={"CURSOR_VERSION": "1.0.0"},
                )

                assert result.returncode == 0
                output = json.loads(result.stdout)
                assert output["permission"] == "deny"
                assert "Invalid response from Runlayer API" in output["user_message"]


# =========================================================================
# C. Event forwarding payload verification
# =========================================================================


class TestEventForwarding:
    """Verify _forward_event sends the correct envelope to ``relay event``."""

    def test_cursor_mcp_forwards_raw_input(self):
        """Cursor beforeMCPExecution forwards the raw input (not transformed)."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            original_input = {
                "hook_event_name": "beforeMCPExecution",
                "tool_name": "test_tool",
                "tool_input": {"key": "value"},
                "url": "https://mcp.example.com",
            }

            result, captured = _run_hook(
                hook,
                json.dumps(original_input),
                td,
                capture_dir=capture,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            assert "event" in captured
            envelope = captured["event"][0]
            assert envelope["client"] == "cursor"
            assert envelope["event_name"] == "beforeMCPExecution"
            assert envelope["payload"]["tool_name"] == "test_tool"
            assert envelope["payload"]["tool_input"] == {"key": "value"}

    def test_claude_code_read_forwards_with_correct_client(self):
        """Claude Code PreToolUse/Read forwards with client=claude_code."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Read",
                    "tool_input": {"file_path": "/project/main.py"},
                }
            )

            result, captured = _run_hook(hook, hook_input, td, capture_dir=capture)

            assert result.returncode == 0
            assert "event" in captured
            envelope = captured["event"][0]
            assert envelope["client"] == "claude_code"
            assert envelope["event_name"] == "PreToolUse"
            assert envelope["payload"]["tool_name"] == "Read"

    def test_cursor_session_start_forwards(self):
        """Cursor sessionStart event is forwarded with client=cursor."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {
                    "hook_event_name": "sessionStart",
                    "session_id": "abc-123",
                }
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            assert "event" in captured
            envelope = captured["event"][0]
            assert envelope["client"] == "cursor"
            assert envelope["event_name"] == "sessionStart"

    def test_claude_code_mcp_forwards_original_event_name(self):
        """Claude Code MCP enforcement forwards using original event name."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            (Path(td) / ".mcp.json").write_text(
                json.dumps(
                    {"mcpServers": {"myserver": {"url": "https://mcp.example.com"}}}
                )
            )

            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "mcp__myserver__do_stuff",
                    "tool_input": {},
                    "cwd": td,
                }
            )

            result, captured = _run_hook(hook, hook_input, td, capture_dir=capture)

            assert result.returncode == 0
            assert "event" in captured
            envelope = captured["event"][0]
            assert envelope["event_name"] == "PreToolUse"


# =========================================================================
# D. Event name normalization
# =========================================================================


class TestEventNameNormalization:
    """Cursor camelCase events dispatch to the correct handler and forward
    with the *original* (un-normalized) event name."""

    def test_pre_tool_use_normalises_to_enforcement(self):
        """preToolUse dispatches to PreToolUse branch (Read enforcement works)."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=True)

            hook_input = json.dumps(
                {
                    "hook_event_name": "preToolUse",
                    "tool_name": "Read",
                    "tool_input": {"file_path": "/project/.env"},
                }
            )

            result, _ = _run_hook(
                hook,
                hook_input,
                td,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"

    def test_pre_tool_use_forwards_original_name(self):
        """preToolUse forwards as 'preToolUse' (not 'PreToolUse')."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {
                    "hook_event_name": "preToolUse",
                    "tool_name": "Write",
                    "tool_input": {},
                }
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            assert "event" in captured
            assert captured["event"][0]["event_name"] == "preToolUse"

    def test_stop_normalises_and_forwards_original(self):
        """Cursor 'stop' dispatches to Stop handler, forwards as 'stop'."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {"hook_event_name": "stop", "session_id": "s1", "status": "aborted"}
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            assert "event" in captured
            assert captured["event"][0]["event_name"] == "stop"
            assert captured["event"][1]["event_name"] == "sessionEnd"
            assert captured["event"][1]["payload"]["hook_event_name"] == "sessionEnd"
            assert captured["event"][1]["payload"]["reason"] == "aborted"

    def test_before_submit_prompt_normalises(self):
        """Cursor beforeSubmitPrompt normalises and forwards original name."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {"hook_event_name": "beforeSubmitPrompt", "prompt": "hi"}
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["permission"] == "allow"
            assert "event" in captured
            assert captured["event"][0]["event_name"] == "beforeSubmitPrompt"

    def test_before_submit_prompt_waits_for_slow_relay(self):
        """Event-only hooks wait for relay completion instead of dropping it."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {"hook_event_name": "beforeSubmitPrompt", "prompt": "hi"}
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                delay_seconds=0.35,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            assert "event" in captured
            assert captured["event"][0]["event_name"] == "beforeSubmitPrompt"

    def test_session_start_normalises(self):
        """Cursor sessionStart normalises and is handled by the * branch."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {"hook_event_name": "sessionStart", "session_id": "s1"}
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            assert "event" in captured
            assert captured["event"][0]["event_name"] == "sessionStart"


class TestLocalToolLifecycle:
    def test_pretooluse_sends_raw_tool_pre_wrapper(self):
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Write",
                    "tool_input": {"file_path": "/tmp/out", "content": "secret"},
                    "tool_use_id": "write-1",
                }
            )

            result, captured = _run_hook(hook, hook_input, td, capture_dir=capture)

            assert result.returncode == 0
            payload = captured["tool-pre"][0]
            assert payload["client"] == "claude_code"
            assert payload["event_name"] == "PreToolUse"
            assert payload["tool_name"] == "Write"
            assert payload["payload"]["tool_use_id"] == "write-1"
            assert captured["event"][0]["event_name"] == "PreToolUse"

    def test_pretooluse_no_enforcement_still_sends_tool_pre(self):
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Write",
                    "tool_input": {"file_path": "/tmp/out", "content": "secret"},
                }
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                response='{"permission":"deny","block_reason":"pii detected"}',
            )

            assert result.returncode == 0
            assert result.stdout.strip() == ""
            captured = _wait_for_captured_targets(capture, "tool-pre", "event")
            payload = captured["tool-pre"][0]
            assert payload["event_name"] == "PreToolUse"
            assert payload["tool_name"] == "Write"
            assert captured["event"][0]["event_name"] == "PreToolUse"

    def test_pretooluse_deny_from_tool_pre_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Write",
                    "tool_input": {"file_path": "/tmp/out", "content": "secret"},
                }
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                response='{"permission":"deny","block_reason":"pii detected"}',
            )

            assert result.returncode == 0
            output = json.loads(result.stdout)
            hso = output["hookSpecificOutput"]
            assert hso["permissionDecision"] == "deny"
            assert "pii detected" in hso["permissionDecisionReason"]
            assert "tool-pre" in captured
            assert "event" in captured

    def test_pretooluse_invalid_tool_pre_permission_blocks(self):
        for response in (
            '{"permission":null}',
            '{"permission":"ask"}',
            '{"permission":true}',
        ):
            with tempfile.TemporaryDirectory() as td:
                hook = _setup_hook(td, client="claude_code", enforcement=True)

                hook_input = json.dumps(
                    {
                        "hook_event_name": "PreToolUse",
                        "tool_name": "Write",
                        "tool_input": {"file_path": "/tmp/out", "content": "secret"},
                    }
                )

                result, _ = _run_hook(
                    hook,
                    hook_input,
                    td,
                    response=response,
                )

                assert result.returncode == 0
                output = json.loads(result.stdout)
                hso = output["hookSpecificOutput"]
                assert hso["permissionDecision"] == "deny"
                assert (
                    "Invalid response from Runlayer API"
                    in hso["permissionDecisionReason"]
                )

    def test_cursor_pretooluse_modified_args_updates_input(self):
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=True)

            hook_input = json.dumps(
                {
                    "hook_event_name": "preToolUse",
                    "tool_name": "Write",
                    "tool_input": {"file_path": "/tmp/out", "content": "secret"},
                    "session_id": "sess-1",
                }
            )

            result, _ = _run_hook(
                hook,
                hook_input,
                td,
                response=json.dumps(
                    {
                        "permission": "allow",
                        "modified_args": {
                            "file_path": "/tmp/out",
                            "content": "[REDACTED]",
                        },
                    }
                ),
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["permission"] == "allow"
            assert output["updated_input"] == {
                "file_path": "/tmp/out",
                "content": "[REDACTED]",
                "_runlayer_session_id": "sess-1",
            }

    def test_posttooluse_sends_raw_tool_post_wrapper_and_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {
                    "hook_event_name": "PostToolUse",
                    "tool_name": "Write",
                    "tool_input": {"file_path": "/tmp/out"},
                    "tool_response": {"ok": True},
                }
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                response='{"blocked":true,"block_reason":"output blocked"}',
            )

            assert result.returncode == 0
            assert json.loads(result.stdout) == {
                "decision": "block",
                "reason": "output blocked",
            }
            payload = captured["tool-post"][0]
            assert payload["client"] == "claude_code"
            assert payload["event_name"] == "PostToolUse"
            assert payload["tool_name"] == "Write"
            assert captured["event"][0]["event_name"] == "PostToolUse"

    def test_posttooluse_no_enforcement_still_sends_tool_post(self):
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {
                    "hook_event_name": "PostToolUse",
                    "tool_name": "Write",
                    "tool_input": {"file_path": "/tmp/out"},
                    "tool_response": {"ok": True},
                }
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                response='{"blocked":true,"block_reason":"output blocked"}',
            )

            assert result.returncode == 0
            assert result.stdout.strip() == ""
            captured = _wait_for_captured_targets(capture, "tool-post", "event")
            payload = captured["tool-post"][0]
            assert payload["event_name"] == "PostToolUse"
            assert payload["tool_name"] == "Write"
            assert captured["event"][0]["event_name"] == "PostToolUse"

    def test_hermes_post_tool_call_is_monitoring_only(self):
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="hermes", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {
                    "hook_event_name": "post_tool_call",
                    "tool_name": "write_file",
                    "tool_input": {"path": "/tmp/out"},
                    "result": "ok",
                }
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                response='{"blocked":true,"block_reason":"ignored"}',
            )

            assert result.returncode == 0
            assert result.stdout.strip() == ""
            captured = _wait_for_captured_targets(capture, "tool-post", "event")
            assert captured["tool-post"][0]["event_name"] == "post_tool_call"
            assert captured["event"][0]["event_name"] == "post_tool_call"

    def test_hermes_transform_tool_result_blocks_with_replacement_string(self):
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="hermes", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {
                    "hook_event_name": "transform_tool_result",
                    "tool_name": "read_file",
                    "tool_input": {"path": "/tmp/secret.txt"},
                    "result": "secret",
                }
            )

            result, _ = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                response='{"blocked":true,"block_reason":"output blocked"}',
            )

            assert result.returncode == 0
            assert json.loads(result.stdout) == "output blocked"

    def test_posttooluse_invalid_blocked_value_blocks(self):
        for response in (
            '{"blocked":"true"}',
            '{"blocked":1}',
            '{"blocked":null}',
        ):
            with tempfile.TemporaryDirectory() as td:
                hook = _setup_hook(td, client="claude_code", enforcement=True)

                hook_input = json.dumps(
                    {
                        "hook_event_name": "PostToolUse",
                        "tool_name": "Write",
                        "tool_input": {"file_path": "/tmp/out"},
                        "tool_response": {"ok": True},
                    }
                )

                result, _ = _run_hook(
                    hook,
                    hook_input,
                    td,
                    response=response,
                )

                assert result.returncode == 0
                assert json.loads(result.stdout) == {
                    "decision": "block",
                    "reason": "Invalid response from Runlayer API",
                }

    def test_cursor_mcp_pretooluse_skips_local_tool_lifecycle(self):
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {
                    "hook_event_name": "preToolUse",
                    "tool_name": "mcp__linear44__list_issues",
                    "tool_input": {"query": "runlayer"},
                    "session_id": "sess-mcp",
                }
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            assert "tool-pre" not in captured
            assert captured["event"][0]["event_name"] == "preToolUse"
            assert (
                json.loads(result.stdout)["updated_input"]["_runlayer_session_id"]
                == "sess-mcp"
            )


# =========================================================================
# E. HOOK_EVENT_NAME env var
# =========================================================================


class TestHookEventNameEnvVar:
    """Claude Code passes the event name via HOOK_EVENT_NAME env var."""

    def test_env_var_dispatches_pretooluse(self):
        """HOOK_EVENT_NAME=PreToolUse dispatches to enforcement (Read .env denied)."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)

            hook_input = json.dumps(
                {
                    "tool_name": "Read",
                    "tool_input": {"file_path": "/project/.env"},
                }
            )

            result, _ = _run_hook(
                hook,
                hook_input,
                td,
                extra_env={"HOOK_EVENT_NAME": "PreToolUse"},
            )

            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_env_var_dispatches_stop(self):
        """HOOK_EVENT_NAME=Stop dispatches to the Stop handler."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps({"session_id": "s1"})

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                extra_env={"HOOK_EVENT_NAME": "Stop"},
            )

            assert result.returncode == 0
            assert "event" in captured
            assert captured["event"][0]["event_name"] == "Stop"

    def test_env_var_takes_precedence_over_json(self):
        """HOOK_EVENT_NAME env var takes precedence over JSON body."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)

            hook_input = json.dumps(
                {
                    "hook_event_name": "PostToolUse",
                    "tool_name": "Read",
                    "tool_input": {"file_path": "/project/.env"},
                }
            )

            result, _ = _run_hook(
                hook,
                hook_input,
                td,
                extra_env={"HOOK_EVENT_NAME": "PreToolUse"},
            )

            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["hookSpecificOutput"]["permissionDecision"] == "deny"


# =========================================================================
# F. Cursor beforeReadFile — expanded file patterns
# =========================================================================


class TestCursorBeforeReadFileExpanded:
    """Cursor beforeReadFile enforcement for MCP config files and settings.json."""

    def _run_cursor_read(
        self,
        temp_dir: str,
        file_path: str,
        *,
        enforcement: bool = True,
        event_name: str = "beforeReadFile",
    ) -> subprocess.CompletedProcess:
        hook = _setup_hook(temp_dir, client="cursor", enforcement=enforcement)

        hook_input = json.dumps({"hook_event_name": event_name, "file_path": file_path})

        result, _ = _run_hook(
            hook,
            hook_input,
            temp_dir,
            extra_env={"CURSOR_VERSION": "1.0.0"},
        )
        return result

    def test_blocks_mcp_json(self):
        with tempfile.TemporaryDirectory() as td:
            result = self._run_cursor_read(td, "/project/mcp.json")
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"
            assert "MCP configuration" in output["agentMessage"]

    def test_before_tab_file_read_blocks_mcp_json(self):
        with tempfile.TemporaryDirectory() as td:
            result = self._run_cursor_read(
                td, "/project/mcp.json", event_name="beforeTabFileRead"
            )
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"
            assert "MCP configuration" in output["agentMessage"]

    def test_blocks_dot_mcp_json(self):
        with tempfile.TemporaryDirectory() as td:
            result = self._run_cursor_read(td, "/project/.mcp.json")
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"

    def test_blocks_mcp_config_json(self):
        with tempfile.TemporaryDirectory() as td:
            result = self._run_cursor_read(td, "/project/mcp_config.json")
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"

    def test_blocks_mcp_dash_config_json(self):
        with tempfile.TemporaryDirectory() as td:
            result = self._run_cursor_read(td, "/project/mcp-config.json")
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"

    def test_blocks_mcp_yaml(self):
        with tempfile.TemporaryDirectory() as td:
            result = self._run_cursor_read(td, "/project/mcp.yaml")
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"

    def test_blocks_mcp_yml(self):
        with tempfile.TemporaryDirectory() as td:
            result = self._run_cursor_read(td, "/project/mcp.yml")
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"

    def test_blocks_claude_json(self):
        with tempfile.TemporaryDirectory() as td:
            result = self._run_cursor_read(td, f"{td}/.claude.json")
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"

    def test_blocks_claude_desktop_config(self):
        with tempfile.TemporaryDirectory() as td:
            result = self._run_cursor_read(
                td,
                f"{td}/Library/Application Support/Claude/claude_desktop_config.json",
            )
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"

    def test_blocks_claude_settings_json(self):
        with tempfile.TemporaryDirectory() as td:
            result = self._run_cursor_read(td, f"{td}/.claude/settings.json")
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"
            assert "Claude Code settings" in output["agentMessage"]

    def test_blocks_claude_settings_json_case_insensitive(self):
        with tempfile.TemporaryDirectory() as td:
            result = self._run_cursor_read(td, f"{td}/.Claude/settings.json")
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"
            assert "Claude Code settings" in output["agentMessage"]

    def test_allows_vscode_settings_json(self):
        with tempfile.TemporaryDirectory() as td:
            result = self._run_cursor_read(td, "/project/.vscode/settings.json")
            output = json.loads(result.stdout)
            assert output["permission"] == "allow"

    def test_allows_normal_file(self):
        with tempfile.TemporaryDirectory() as td:
            result = self._run_cursor_read(td, "/project/src/main.py")
            output = json.loads(result.stdout)
            assert output["permission"] == "allow"

    def test_blocks_envrc(self):
        with tempfile.TemporaryDirectory() as td:
            result = self._run_cursor_read(td, "/project/.envrc")
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"

    def test_blocks_env_production(self):
        with tempfile.TemporaryDirectory() as td:
            result = self._run_cursor_read(td, "/project/.env.production")
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"


# =========================================================================
# G. Stop event with transcript
# =========================================================================


class TestStopEventTranscript:
    def test_user_prompt_submit_starts_claude_transcript_stream(self):
        """Claude Code UserPromptSubmit starts the hidden transcript stream relay."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            transcript_path = Path(td) / "transcript.jsonl"
            transcript_path.write_text("")
            hook_input = json.dumps(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "session_id": "stream-s1",
                    "transcript_path": str(transcript_path),
                }
            )

            result, _ = _run_hook(hook, hook_input, td, capture_dir=capture)
            captured = _wait_for_captured_targets(capture, "event", "stream-transcript")

            assert result.returncode == 0
            assert captured["event"][0]["event_name"] == "UserPromptSubmit"
            stream_request = captured["stream-transcript"][0]
            assert stream_request["client"] == "claude_code"
            assert stream_request["payload"]["session_id"] == "stream-s1"
            assert stream_request["payload"]["transcript_path"] == str(transcript_path)
            assert stream_request["start_offset"] == 0
            marker = (
                Path(td)
                / "tmp"
                / "runlayer-claude-transcript-stream"
                / "stream-s1.active"
            )
            assert not marker.exists()

    def test_stop_includes_transcript_content(self):
        """Stop event reads transcript file and includes content in forwarded payload."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            transcript_path = Path(td) / "transcript.jsonl"
            transcript_content = '{"type":"message","text":"hello world"}\n'
            transcript_path.write_text(transcript_content)

            hook_input = json.dumps(
                {
                    "hook_event_name": "Stop",
                    "session_id": "s1",
                    "transcript_path": str(transcript_path),
                }
            )

            result, captured = _run_hook(hook, hook_input, td, capture_dir=capture)

            assert result.returncode == 0
            assert "event" in captured
            envelope = captured["event"][0]
            assert envelope["event_name"] == "Stop"
            assert "transcript" in envelope
            assert "hello world" in envelope["transcript"]

    def test_stop_forwards_claude_transcript_jsonl_unchanged(self):
        """Claude thinking lives in transcript_path JSONL, not hook stdin."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            transcript_path = Path(td) / "transcript.jsonl"
            transcript_content = (
                json.dumps(
                    {
                        "type": "assistant",
                        "message": {
                            "role": "assistant",
                            "content": [
                                {
                                    "type": "thinking",
                                    "thinking": "Visible summarized thinking",
                                    "signature": "integrity-token",
                                },
                                {
                                    "type": "redacted_thinking",
                                    "data": "encrypted-thinking",
                                },
                                {
                                    "type": "text",
                                    "text": "Visible assistant response",
                                },
                            ],
                        },
                    }
                )
                + "\n"
            )
            transcript_path.write_text(transcript_content)

            hook_input = json.dumps(
                {
                    "hook_event_name": "Stop",
                    "session_id": "s1",
                    "transcript_path": str(transcript_path),
                }
            )

            result, captured = _run_hook(hook, hook_input, td, capture_dir=capture)

            assert result.returncode == 0
            envelope = captured["event"][0]
            assert envelope["event_name"] == "Stop"
            assert envelope["payload"]["transcript_path"] == str(transcript_path)
            assert envelope["transcript"] == transcript_content
            assert "integrity-token" in envelope["transcript"]
            assert "redacted_thinking" in envelope["transcript"]

    def test_cursor_stop_uses_env_transcript_path(self):
        """Cursor stop event uses CURSOR_TRANSCRIPT_PATH env var."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            transcript_path = Path(td) / "cursor_transcript.jsonl"
            transcript_path.write_text('{"cursor":"data"}\n')

            hook_input = json.dumps({"hook_event_name": "stop", "session_id": "s1"})

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                extra_env={
                    "CURSOR_VERSION": "1.0.0",
                    "CURSOR_TRANSCRIPT_PATH": str(transcript_path),
                },
            )

            assert result.returncode == 0
            assert "event" in captured
            envelope = captured["event"][0]
            assert "transcript" in envelope
            assert "cursor" in envelope["transcript"]

    def test_stop_existing_transcript_does_not_sleep(self):
        """Stop event reads an available transcript without fixed delay."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            bin_dir = Path(td) / "bin"
            _write_fake_runlayer(bin_dir, capture_dir=capture)
            sleep_log = Path(td) / "sleep.log"
            sleep_bin = bin_dir / "sleep"
            sleep_bin.write_text(
                '#!/bin/bash\nprintf "%s\\n" "$*" >> "$RUNLAYER_SLEEP_LOG"\nexit 0\n'
            )
            sleep_bin.chmod(0o755)

            transcript_path = Path(td) / "transcript.jsonl"
            transcript_path.write_text('{"ready":true}\n')

            hook_input = json.dumps(
                {
                    "hook_event_name": "Stop",
                    "session_id": "s1",
                    "transcript_path": str(transcript_path),
                }
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                extra_env={"RUNLAYER_SLEEP_LOG": str(sleep_log)},
                override_path=f"{bin_dir}:{os.environ['PATH']}",
            )

            assert result.returncode == 0
            assert not sleep_log.exists()
            envelope = captured["event"][0]
            assert envelope["event_name"] == "Stop"
            assert envelope["transcript"] == '{"ready":true}\n'

    def test_stop_skips_transcript_backfill_when_claude_stream_active(self):
        """Stop does not re-send transcript when the live transcript streamer is active."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            transcript_path = Path(td) / "transcript.jsonl"
            transcript_path.write_text('{"ready":true}\n')
            marker_dir = Path(td) / "runlayer-claude-transcript-stream"
            marker_dir.mkdir()
            (marker_dir / "s1.active").write_text(str(int(time.time())))

            hook_input = json.dumps(
                {
                    "hook_event_name": "Stop",
                    "session_id": "s1",
                    "transcript_path": str(transcript_path),
                }
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                extra_env={"TMPDIR": td},
            )

            assert result.returncode == 0
            envelope = captured["event"][0]
            assert envelope["event_name"] == "Stop"
            assert "transcript" not in envelope

    def test_stop_backfills_transcript_when_claude_stream_marker_is_stale(self):
        """Stop backfills if the live streamer heartbeat is stale."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            transcript_path = Path(td) / "transcript.jsonl"
            transcript_path.write_text('{"ready":true}\n')
            marker_dir = Path(td) / "runlayer-claude-transcript-stream"
            marker_dir.mkdir()
            (marker_dir / "s1.active").write_text("1")

            hook_input = json.dumps(
                {
                    "hook_event_name": "Stop",
                    "session_id": "s1",
                    "transcript_path": str(transcript_path),
                }
            )

            result, captured = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                extra_env={"TMPDIR": td},
            )

            assert result.returncode == 0
            envelope = captured["event"][0]
            assert envelope["event_name"] == "Stop"
            assert envelope["transcript"] == '{"ready":true}\n'

    def test_stop_without_transcript_still_forwards(self):
        """Stop event without transcript_path still forwards the event."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=False)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps({"hook_event_name": "Stop", "session_id": "s1"})

            result, captured = _run_hook(hook, hook_input, td, capture_dir=capture)

            assert result.returncode == 0
            assert "event" in captured
            envelope = captured["event"][0]
            assert envelope["event_name"] == "Stop"
            assert "transcript" not in envelope


# =========================================================================
# H. Edge cases
# =========================================================================


class TestEdgeCases:
    def test_empty_tool_name_pretooluse_allows(self):
        """PreToolUse with empty tool_name forwards and allows (no crash)."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)

            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "",
                    "tool_input": {},
                }
            )

            result, _ = _run_hook(hook, hook_input, td)

            assert result.returncode == 0
            assert "deny" not in result.stdout

    def test_cursor_observational_event_outputs_empty_object(self):
        """Cursor observational events (default branch) output '{}'."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=False)

            hook_input = json.dumps(
                {
                    "hook_event_name": "afterAgentResponse",
                    "data": "test",
                }
            )

            result, _ = _run_hook(
                hook,
                hook_input,
                td,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            assert result.stdout.strip() == "{}"

    def test_observational_event_does_not_wait_for_slow_relay(self):
        """Default observational events remain fire-and-forget telemetry."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=False)

            hook_input = json.dumps(
                {
                    "hook_event_name": "afterAgentResponse",
                    "data": "test",
                }
            )

            start = time.perf_counter()
            result, _ = _run_hook(
                hook,
                hook_input,
                td,
                delay_seconds=2,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )
            elapsed = time.perf_counter() - start

            assert result.returncode == 0
            assert result.stdout.strip() == "{}"
            assert elapsed < 1.5

    def test_claude_code_observational_event_no_stdout(self):
        """Claude Code observational events (default branch) produce no stdout."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=False)

            hook_input = json.dumps(
                {
                    "hook_event_name": "PostToolUse",
                    "tool_name": "Write",
                    "tool_input": {},
                }
            )

            result, _ = _run_hook(hook, hook_input, td)

            assert result.returncode == 0
            assert result.stdout.strip() == ""

    def test_missing_hook_event_name_exits_silently(self):
        """No hook_event_name in input or env → silent exit 0."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)

            hook_input = json.dumps({"tool_name": "Read", "tool_input": {}})

            result, _ = _run_hook(hook, hook_input, td)

            assert result.returncode == 0
            assert result.stdout.strip() == ""

    def test_cursor_allow_response_shape(self):
        """Cursor allow events produce {"permission":"allow"}."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=True)

            hook_input = json.dumps(
                {
                    "hook_event_name": "beforeReadFile",
                    "file_path": "/project/README.md",
                }
            )

            result, _ = _run_hook(
                hook,
                hook_input,
                td,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output == {"permission": "allow"}

    def test_claude_code_deny_response_shape(self):
        """Claude Code deny produces hookSpecificOutput with correct structure."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)

            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Read",
                    "tool_input": {"file_path": "/project/.env"},
                }
            )

            result, _ = _run_hook(hook, hook_input, td)

            assert result.returncode == 0
            output = json.loads(result.stdout)
            hso = output["hookSpecificOutput"]
            assert hso["hookEventName"] == "PreToolUse"
            assert hso["permissionDecision"] == "deny"
            assert "environment files" in hso["permissionDecisionReason"]

    def test_cursor_deny_response_has_continue_true(self):
        """Cursor deny responses include continue: true."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=True)

            hook_input = json.dumps(
                {
                    "hook_event_name": "beforeReadFile",
                    "file_path": "/project/.env",
                }
            )

            result, _ = _run_hook(
                hook,
                hook_input,
                td,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"
            assert output["continue"] is True
            assert "user_message" in output
            assert "agentMessage" in output

    def test_cursor_username_does_not_false_positive_as_native(self):
        """Hook at /Users/cursor/.claude/hooks/ must no-op, not enforce.

        The old glob *cursor* matched the username; only .cursor/ dir should count.
        """
        with tempfile.TemporaryDirectory() as td:
            hook_dir = Path(td) / "Users" / "cursor" / ".claude" / "hooks"
            hook_dir.mkdir(parents=True)
            hook_copy = hook_dir / "runlayer-hook.sh"
            hook_copy.write_text(HOOK_SRC.read_text())
            hook_copy.chmod(0o755)
            (hook_dir / "runlayer-config.json").write_text(
                json.dumps({"enforcement": True})
            )

            hook_input = json.dumps(
                {
                    "hook_event_name": "beforeReadFile",
                    "file_path": "/project/.env",
                }
            )

            result, _ = _run_hook(
                hook_copy,
                hook_input,
                td,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output == {"permission": "allow"}


# =========================================================================
# Quoted filename bypass in Bash/shell command scanning
# =========================================================================


class TestBashCommandQuotedFilenameBypass:
    """_check_bash_command must strip quotes so `cat ".env"` is still blocked."""

    def test_claude_bash_double_quoted_env_denied(self):
        with tempfile.TemporaryDirectory() as td:
            hook_path = _setup_hook(td, client="claude_code", enforcement=True)
            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Bash",
                    "tool_input": {"command": 'cat ".env"'},
                }
            )
            result, _ = _run_hook(
                hook_path,
                hook_input,
                td,
                extra_env={"HOOK_EVENT_NAME": "PreToolUse"},
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_claude_bash_single_quoted_env_denied(self):
        with tempfile.TemporaryDirectory() as td:
            hook_path = _setup_hook(td, client="claude_code", enforcement=True)
            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Bash",
                    "tool_input": {"command": "cat '.env'"},
                }
            )
            result, _ = _run_hook(
                hook_path,
                hook_input,
                td,
                extra_env={"HOOK_EVENT_NAME": "PreToolUse"},
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_claude_bash_quoted_mcp_json_denied(self):
        with tempfile.TemporaryDirectory() as td:
            hook_path = _setup_hook(td, client="claude_code", enforcement=True)
            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Bash",
                    "tool_input": {"command": "cat '.mcp.json'"},
                }
            )
            result, _ = _run_hook(
                hook_path,
                hook_input,
                td,
                extra_env={"HOOK_EVENT_NAME": "PreToolUse"},
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_claude_bash_quoted_env_production_denied(self):
        with tempfile.TemporaryDirectory() as td:
            hook_path = _setup_hook(td, client="claude_code", enforcement=True)
            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Bash",
                    "tool_input": {"command": 'head -n 10 ".env.production"'},
                }
            )
            result, _ = _run_hook(
                hook_path,
                hook_input,
                td,
                extra_env={"HOOK_EVENT_NAME": "PreToolUse"},
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_cursor_shell_double_quoted_env_denied(self):
        with tempfile.TemporaryDirectory() as td:
            hook_path = _setup_hook(td, client="cursor", enforcement=True)
            hook_input = json.dumps(
                {
                    "hook_event_name": "beforeShellExecution",
                    "command": 'cat ".env"',
                }
            )
            result, _ = _run_hook(
                hook_path,
                hook_input,
                td,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"

    def test_cursor_shell_single_quoted_env_denied(self):
        with tempfile.TemporaryDirectory() as td:
            hook_path = _setup_hook(td, client="cursor", enforcement=True)
            hook_input = json.dumps(
                {
                    "hook_event_name": "beforeShellExecution",
                    "command": "cat '.env'",
                }
            )
            result, _ = _run_hook(
                hook_path,
                hook_input,
                td,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"


# =========================================================================
# Relay dispatch error disambiguation (rc=127 vs rc=2)
# =========================================================================


class TestRelayDispatchErrors:
    """Verify that rc=127 (binary missing) and rc=2 (API unreachable) produce
    distinct, actionable deny messages."""

    def test_claude_code_mcp_relay_missing_says_cli_not_found(self):
        """Claude Code MCP call with relay exit 127 → mentions missing binary."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)

            (Path(td) / ".mcp.json").write_text(
                json.dumps(
                    {"mcpServers": {"myserver": {"url": "https://mcp.example.com"}}}
                )
            )

            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "mcp__myserver__do_stuff",
                    "tool_input": {},
                    "cwd": td,
                }
            )

            result, _ = _run_hook(
                hook,
                hook_input,
                td,
                exit_code=127,
            )

            assert result.returncode == 0
            output = json.loads(result.stdout)
            reason = output["hookSpecificOutput"]["permissionDecisionReason"]
            assert "could be found on the hook" in reason
            assert "Failed to contact the Runlayer API" not in reason

    def test_claude_code_mcp_relay_network_failure_says_api_unreachable(self):
        """Claude Code MCP call with relay exit 2 → 'Failed to contact Runlayer API'."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="claude_code", enforcement=True)

            (Path(td) / ".mcp.json").write_text(
                json.dumps(
                    {"mcpServers": {"myserver": {"url": "https://mcp.example.com"}}}
                )
            )

            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "mcp__myserver__do_stuff",
                    "tool_input": {},
                    "cwd": td,
                }
            )

            result, _ = _run_hook(
                hook,
                hook_input,
                td,
                exit_code=2,
            )

            assert result.returncode == 0
            output = json.loads(result.stdout)
            reason = output["hookSpecificOutput"]["permissionDecisionReason"]
            assert "Failed to contact the Runlayer API" in reason
            assert "CLI not found" not in reason

    def test_cursor_before_mcp_relay_missing_says_cli_not_found(self):
        """Cursor beforeMCPExecution with relay exit 127 → 'CLI not found'."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=True)

            hook_input = json.dumps(
                {
                    "hook_event_name": "beforeMCPExecution",
                    "tool_name": "test_tool",
                    "tool_input": "{}",
                    "url": "https://mcp.example.com",
                }
            )

            result, _ = _run_hook(
                hook,
                hook_input,
                td,
                exit_code=127,
                extra_env={"CURSOR_VERSION": "1.0.0"},
            )

            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["permission"] == "deny"
            assert "Runlayer CLI not found" in output["user_message"]
            assert "Failed to contact Runlayer API" not in output["user_message"]

    def test_relay_debug_env_var_passes_flag(self):
        """RUNLAYER_HOOK_DEBUG=1 causes --debug to be passed to relay."""
        with tempfile.TemporaryDirectory() as td:
            hook = _setup_hook(td, client="cursor", enforcement=True)
            capture = Path(td) / "cap"
            capture.mkdir()

            hook_input = json.dumps(
                {
                    "hook_event_name": "beforeMCPExecution",
                    "tool_name": "test_tool",
                    "tool_input": "{}",
                    "url": "https://mcp.example.com",
                }
            )

            result, _ = _run_hook(
                hook,
                hook_input,
                td,
                capture_dir=capture,
                extra_env={
                    "CURSOR_VERSION": "1.0.0",
                    "RUNLAYER_HOOK_DEBUG": "1",
                },
            )

            assert result.returncode == 0
            argv_log = capture / "argv.log"
            assert argv_log.exists(), "argv.log not written"
            argv_lines = argv_log.read_text().splitlines()
            assert "--debug" in argv_lines
