from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from runlayer_cli.hook import dispatch as hook_dispatch
from runlayer_cli.hook import hook_io, plugin_context
from runlayer_cli.hook.clients import Client, HookResponse
from runlayer_cli.hook.daemon_protocol import HOOK_ENV_ALLOWLIST
from runlayer_cli.hook.mcp_lookup import lookup_codex_mcp_server
from runlayer_cli.mdm_config import AIWatchMode
from runlayer_cli.regex_safe import compile as compile_regex

PLUGIN_URL = (
    "https://acme.runlayer.com/api/v1/proxy/plugins/"
    f"{plugin_context.RUNLAYER_PLUGIN_ID}/mcp"
)
OTHER_URL = "https://acme.runlayer.com/api/v1/proxy/11111111-2222-3333-********/mcp"
CLAUDE = Client.CLAUDE_CODE
CODEX = Client.CODEX


@pytest.fixture
def home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(plugin_context.DISABLE_ENV, raising=False)
    monkeypatch.setattr(plugin_context, "_configured_runlayer_host", lambda: None)
    with patch("runlayer_cli.hook.mcp_lookup.Path.home", return_value=tmp_path):
        yield tmp_path


def _write_claude_json(home: Path, servers: dict[str, dict[str, str]]) -> None:
    (home / ".claude.json").write_text(json.dumps({"mcpServers": servers}))


def _write_codex_toml(home: Path, servers: dict[str, str]) -> None:
    (home / ".codex").mkdir(exist_ok=True)
    body = "".join(
        f'[mcp_servers.{name}]\nurl = "{url}"\n\n' for name, url in servers.items()
    )
    (home / ".codex" / "config.toml").write_text(body)


def _write_claude_plugin(home: Path) -> None:
    root = home / ".claude" / "plugins" / "runlayer"
    (root / ".claude-plugin").mkdir(parents=True)
    (root / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"name": "runlayer"})
    )
    (root / ".mcp.json").write_text(
        json.dumps({"mcpServers": {"runlayer-plugin": {"url": PLUGIN_URL}}})
    )


def _dispatch(
    monkeypatch: pytest.MonkeyPatch,
    *,
    event: str,
    client: Client,
    cwd: Path,
) -> list[tuple[str, str]]:
    forwarded: list[tuple[str, str]] = []
    monkeypatch.setattr(
        hook_dispatch,
        "forward_event",
        lambda client_name, event_name, _input, *, debug: forwarded.append(
            (client_name, event_name)
        ),
    )
    monkeypatch.setattr(
        hook_dispatch, "start_transcript_stream", lambda *_a, **_k: True
    )
    payload = {"hook_event_name": event, "session_id": "s1", "cwd": str(cwd)}
    hook_dispatch._dispatch(
        hook_type=event,
        original_hook_type=event,
        client=client,
        resp=HookResponse(client, event),
        input_data=payload,
        raw_input=json.dumps(payload),
        mode=AIWatchMode.ENFORCE,
        debug=False,
    )
    return forwarded


class TestFindRunlayerPlugin:
    @pytest.mark.parametrize("name", ["runlayer-plugin", "onelayer"])
    def test_claude_code_direct_entry(self, home, name):
        _write_claude_json(home, {name: {"type": "http", "url": PLUGIN_URL}})
        assert plugin_context.find_runlayer_plugin(
            CLAUDE, str(home)
        ) == plugin_context.PluginInstall(name)

    def test_claude_code_org_zip_plugin_install(self, home):
        _write_claude_plugin(home)
        assert plugin_context.find_runlayer_plugin(
            CLAUDE, str(home)
        ) == plugin_context.PluginInstall(
            "plugin_runlayer_runlayer-plugin", plugin="runlayer"
        )

    @pytest.mark.parametrize("name", ["runlayer-plugin", "onelayer"])
    def test_codex_toml_entry(self, home, name):
        _write_codex_toml(home, {name: PLUGIN_URL})
        assert plugin_context.find_runlayer_plugin(
            CODEX, str(home)
        ) == plugin_context.PluginInstall(name)

    def test_codex_fuzzy_key_reports_the_configured_name(self, home):
        # Codex lookup matches ``runlayer_plugin`` for ``runlayer-plugin``; the
        # injected prefix must use the key Codex builds tool names from.
        _write_codex_toml(home, {"runlayer_plugin": PLUGIN_URL})
        assert plugin_context.find_runlayer_plugin(
            CODEX, str(home)
        ) == plugin_context.PluginInstall("runlayer_plugin")
        context = plugin_context.build_plugin_context(CODEX, str(home))
        assert context is not None
        assert "Its tools are prefixed mcp__runlayer_plugin__." in context
        # The enforcement lookup keeps its previous shape: no ``name`` rides the
        # authorization request because of a fuzzy match.
        assert lookup_codex_mcp_server("runlayer-plugin") == {"url": PLUGIN_URL}

    def test_codex_does_not_read_claude_config(self, home):
        _write_claude_json(home, {"runlayer-plugin": {"url": PLUGIN_URL}})
        assert plugin_context.find_runlayer_plugin(CODEX, str(home)) is None

    def test_root_alias_on_configured_runlayer_host(self, home, monkeypatch):
        monkeypatch.setattr(
            plugin_context,
            "_configured_runlayer_host",
            lambda: "https://acme.runlayer.com",
        )
        _write_claude_json(
            home, {"runlayer-plugin": {"url": "https://acme.runlayer.com/mcp"}}
        )
        _write_codex_toml(home, {"runlayer-plugin": "https://acme.runlayer.com/mcp"})
        for client in (CLAUDE, CODEX):
            assert plugin_context.find_runlayer_plugin(
                client, str(home)
            ) == plugin_context.PluginInstall("runlayer-plugin")

    @pytest.mark.parametrize("host", [None, "https://other.example.com"])
    def test_root_alias_on_other_host_is_ignored(self, home, monkeypatch, host):
        monkeypatch.setattr(plugin_context, "_configured_runlayer_host", lambda: host)
        _write_claude_json(
            home, {"runlayer-plugin": {"url": "https://acme.runlayer.com/mcp"}}
        )
        assert plugin_context.find_runlayer_plugin(CLAUDE, str(home)) is None

    def test_same_name_pointing_elsewhere_is_ignored(self, home):
        _write_claude_json(home, {"runlayer-plugin": {"url": OTHER_URL}})
        _write_codex_toml(home, {"runlayer-plugin": OTHER_URL})
        assert plugin_context.find_runlayer_plugin(CLAUDE, str(home)) is None
        assert plugin_context.find_runlayer_plugin(CODEX, str(home)) is None

    def test_absent_returns_none(self, home):
        assert plugin_context.find_runlayer_plugin(CLAUDE, str(home)) is None
        assert plugin_context.find_runlayer_plugin(CODEX, str(home)) is None

    def test_unsupported_client_returns_none(self, home):
        _write_claude_json(home, {"runlayer-plugin": {"url": PLUGIN_URL}})
        assert plugin_context.find_runlayer_plugin(Client.CURSOR, str(home)) is None


# Every tool the injected text names. The text is one of several copies of the
# plugin protocol (webapp skill, Cursor rule, backend server instructions), so a
# rename or a new tool must show up here on purpose, not drift in silently.
ROUTING_TOOL_NAMES = frozenset(
    {
        "search_skills",
        "list_skills",
        "get_skill",
        "get_skill_file",
        "search_tools",
        "execute_tool",
        "list_agents",
        "get_agent",
        "run_agent",
        "get_agent_run_trace",
    }
)
ROUTING_PLACEHOLDER_PREFIXES = frozenset(
    {"DISABLED_", "AUTH_REQUIRED_", "INPUTS_REQUIRED_"}
)


def test_routing_rules_name_exactly_the_pinned_tools():
    text = plugin_context._ROUTING_RULES
    tools = compile_regex(r"\b[a-z]+(?:_[a-z]+)+\b").findall(text)
    assert set(tools) == ROUTING_TOOL_NAMES
    placeholders = compile_regex(r"\b([A-Z]+(?:_[A-Z]+)*_)[ ,.]").findall(text)
    assert set(placeholders) == ROUTING_PLACEHOLDER_PREFIXES


class TestBuildPluginContext:
    def test_direct_entry_names_server_and_tool_prefix(self, home):
        _write_claude_json(home, {"onelayer": {"url": PLUGIN_URL}})
        context = plugin_context.build_plugin_context(CLAUDE, str(home))
        assert context is not None
        assert context.startswith(
            'Runlayer Plugin is connected as MCP server "onelayer". '
            "Its tools are prefixed mcp__onelayer__."
        )
        for tool in ("search_skills", "get_skill_file", "search_tools", "execute_tool"):
            assert tool in context

    def test_plugin_install_names_plugin_and_tool_prefix(self, home):
        _write_claude_plugin(home)
        context = plugin_context.build_plugin_context(CLAUDE, str(home))
        assert context is not None
        assert context.startswith(
            'Runlayer Plugin is installed as the Claude Code plugin "runlayer". '
            "Its tools are prefixed mcp__plugin_runlayer_runlayer-plugin__."
        )

    def test_codex_names_server(self, home):
        _write_codex_toml(home, {"runlayer-plugin": PLUGIN_URL})
        context = plugin_context.build_plugin_context(CODEX, str(home))
        assert context is not None
        assert context.startswith(
            'Runlayer Plugin is connected as MCP server "runlayer-plugin". '
            "Its tools are prefixed mcp__runlayer-plugin__."
        )

    @pytest.mark.parametrize("value", ["0", "false", "OFF"])
    def test_env_kill_switch(self, home, monkeypatch, value):
        _write_claude_json(home, {"runlayer-plugin": {"url": PLUGIN_URL}})
        monkeypatch.setenv(plugin_context.DISABLE_ENV, value)
        assert plugin_context.build_plugin_context(CLAUDE, str(home)) is None

    def test_kill_switch_reaches_daemon_served_hooks(self, home):
        # The daemon never sees the client's environment: the switch must ride
        # the forwarded request env and be read from there.
        assert plugin_context.DISABLE_ENV in HOOK_ENV_ALLOWLIST
        _write_claude_json(home, {"runlayer-plugin": {"url": PLUGIN_URL}})
        request = hook_io.HookIO(
            env={plugin_context.DISABLE_ENV: "0"}, daemon_served=True
        )
        with hook_io.scoped(request):
            assert plugin_context.build_plugin_context(CLAUDE, str(home)) is None
        assert plugin_context.build_plugin_context(CLAUDE, str(home)) is not None


class TestDispatchInjection:
    @pytest.mark.parametrize("event", ["SessionStart", "UserPromptSubmit"])
    def test_claude_code_gets_additional_context(
        self, home, monkeypatch, capsys, event
    ):
        _write_claude_json(home, {"runlayer-plugin": {"url": PLUGIN_URL}})
        forwarded = _dispatch(monkeypatch, event=event, client=CLAUDE, cwd=home)
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["hookEventName"] == event
        assert (
            'MCP server "runlayer-plugin"'
            in (out["hookSpecificOutput"]["additionalContext"])
        )
        assert forwarded == [("claude_code", event)]

    @pytest.mark.parametrize("event", ["SessionStart", "UserPromptSubmit"])
    def test_codex_gets_additional_context(self, home, monkeypatch, capsys, event):
        _write_codex_toml(home, {"runlayer-plugin": PLUGIN_URL})
        forwarded = _dispatch(monkeypatch, event=event, client=CODEX, cwd=home)
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["hookEventName"] == event
        assert (
            "mcp__runlayer-plugin__" in (out["hookSpecificOutput"]["additionalContext"])
        )
        assert forwarded == [("codex", event)]

    @pytest.mark.parametrize("client", [CLAUDE, CODEX])
    @pytest.mark.parametrize("event", ["SessionStart", "UserPromptSubmit"])
    def test_without_plugin_stays_silent(
        self, home, monkeypatch, capsys, client, event
    ):
        _dispatch(monkeypatch, event=event, client=client, cwd=home)
        assert capsys.readouterr().out == ""

    def test_subagent_start_does_not_inject(self, home, monkeypatch, capsys):
        _write_claude_json(home, {"runlayer-plugin": {"url": PLUGIN_URL}})
        _dispatch(monkeypatch, event="SubagentStart", client=CLAUDE, cwd=home)
        assert capsys.readouterr().out == ""

    def test_cursor_session_start_unchanged(self, home, monkeypatch, capsys):
        _write_claude_json(home, {"runlayer-plugin": {"url": PLUGIN_URL}})
        forwarded = _dispatch(
            monkeypatch, event="SessionStart", client=Client.CURSOR, cwd=home
        )
        assert capsys.readouterr().out == "{}"
        assert forwarded == [("cursor", "SessionStart")]


class TestAllowWithContext:
    @pytest.mark.parametrize("client", [CLAUDE, CODEX])
    @pytest.mark.parametrize("event", ["SessionStart", "UserPromptSubmit"])
    def test_context_shape_for_supported_clients(self, client, event):
        out = json.loads(HookResponse(client, event).allow_with_context("x") or "")
        assert out == {
            "hookSpecificOutput": {"hookEventName": event, "additionalContext": "x"}
        }

    @pytest.mark.parametrize(
        ("client", "event"),
        [
            (CLAUDE, "PreToolUse"),
            (CLAUDE, "SubagentStart"),
            (CODEX, "PreToolUse"),
            (Client.CURSOR, "UserPromptSubmit"),
        ],
    )
    def test_none_outside_supported_session_events(self, client, event):
        assert HookResponse(client, event).allow_with_context("x") is None
