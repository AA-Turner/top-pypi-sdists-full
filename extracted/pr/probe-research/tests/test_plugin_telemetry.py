"""The plugin telemetry hook: classification, enrichment, and its contract.

The contract under test (see the module docstring of
plugins/probe-research/hooks/telemetry.py):

  * stdlib-only, importable with no probe package behind it (the hook runs
    under the system python3 — same property test_policy_sync.py guards for
    version_policy);
  * fail-SILENT: garbage stdin, unknown modes and disabled state all exit 0
    with no output — a hook that prints could alter the session;
  * killswitch: PROBE_TELEMETRY=off disables every mode;
  * metadata only: the enriched batch carries whitelisted names and ids, and
    the funnel dedupes (one mcp_used per session, one skill_invoked per skill).

No test here spawns `probe`, `claude` or `codex`, and none does network:
spawn_sender is monkeypatched in-process, and the subprocess tests run with
the killswitch on or with input that classifies to nothing.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
_HOOKS = _ROOT / "plugins" / "probe-research" / "hooks"
_TELEMETRY = _HOOKS / "telemetry.py"


@pytest.fixture(scope="module")
def tel():
    spec = importlib.util.spec_from_file_location("plugin_telemetry", _TELEMETRY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def no_send(tel, monkeypatch):
    """Capture what would have been sent instead of spawning the sender."""
    sent: list[dict] = []
    monkeypatch.setattr(tel, "spawn_sender", lambda events: sent.extend(events))
    return sent


@pytest.fixture()
def state_dir(tel, tmp_path, monkeypatch):
    monkeypatch.setattr(tel, "STATE_DIR", str(tmp_path / "state"))
    return tmp_path / "state"


# ---------------------------------------------------------------------------
# Standalone: the way the hook actually runs
# ---------------------------------------------------------------------------


def test_stands_up_with_no_probe_package() -> None:
    probe = (
        "import sys, importlib.util; "
        f"spec = importlib.util.spec_from_file_location('t', {str(_TELEMETRY)!r}); "
        "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); "
        "assert 'probe' not in sys.modules, 'telemetry pulled in the probe package'; "
        "assert 'posthog' not in sys.modules, 'telemetry pulled in a posthog client'; "
        "print(m.EVENT_SESSION_STARTED)"
    )
    result = subprocess.run(
        [sys.executable, "-c", probe], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "plugin.session_started"


@pytest.mark.parametrize("mode", ["session-start", "post-tool", "session-end", "send", "bogus"])
def test_fail_silent_on_garbage_stdin(mode: str) -> None:
    """Any mode, fed non-JSON, exits 0 and prints nothing."""
    result = subprocess.run(
        [sys.executable, str(_TELEMETRY), mode],
        input="not json at all",
        capture_output=True,
        text=True,
        timeout=30,
        env={"PATH": "/usr/bin:/bin", "PROBE_TELEMETRY": "on"},
    )
    assert result.returncode == 0
    assert result.stdout == ""


def test_killswitch_disables_before_reading_stdin() -> None:
    result = subprocess.run(
        [sys.executable, str(_TELEMETRY), "session-start"],
        input=json.dumps({"session_id": "s1", "source": "startup"}),
        capture_output=True,
        text=True,
        timeout=30,
        env={"PATH": "/usr/bin:/bin", "PROBE_TELEMETRY": "off"},
    )
    assert result.returncode == 0
    assert result.stdout == ""


@pytest.mark.parametrize(
    ("value", "disabled"),
    [
        ("off", True),
        ("OFF", True),
        ("0", True),
        ("false", True),
        ("no", True),
        ("disabled", True),
        ("", False),
        ("on", False),
        ("1", False),
    ],
)
def test_killswitch_values(tel, monkeypatch, value: str, disabled: bool) -> None:
    monkeypatch.setenv("PROBE_TELEMETRY", value)
    assert tel.telemetry_disabled() is disabled


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("tool", "tool_input", "expected"),
    [
        ("Skill", {"skill": "track-work"}, "track-work"),
        ("Skill", {"skill": "probe-research:visualize-progress"}, "visualize-progress"),
        # pre-consolidation names: a resumed transcript still invokes them,
        # and an unlisted slug silently stops counting
        ("Skill", {"skill": "start-research-work"}, "start-research-work"),
        ("Skill", {"skill": "probe-research:track-research-work"}, "track-research-work"),
        ("SlashCommand", {"command": "/probe-research:start-research-work"}, "start-research-work"),
        ("SlashCommand", {"command": "/start-research-work some args"}, "start-research-work"),
        ("Skill", {"skill": "frontend-design"}, None),
        ("Skill", {}, None),
        ("Bash", {"skill": "start-research-work"}, None),
    ],
)
def test_match_skill(tel, tool, tool_input, expected) -> None:
    assert tel.match_skill(tool, tool_input) == expected


@pytest.mark.parametrize(
    ("command", "expected"),
    [
        ("probe run start --project x", [("run", "start")]),
        ("probe project create foo && probe run start", [("project", "create"), ("run", "start")]),
        ("cd /tmp; probe notes write 'done'", [("notes", "write")]),
        ("probe artifact add ./model.pt", [("artifact", "add")]),
        ("probe artifact list", []),  # read, not a write
        ("probe project get foo", []),
        ("ls -la && echo probe", []),
        ("approbe run start", []),  # substring, not the binary
        ("PYTHONPATH=. probe run set loss=0.1", [("run", "set")]),
        ("", []),
    ],
)
def test_match_probe_writes(tel, command, expected) -> None:
    assert tel.match_probe_writes(command) == expected


@pytest.mark.parametrize(
    ("response", "expected"),
    [
        ({"exit_code": 0}, "success"),
        ({"exit_code": 2}, "error"),
        ({"interrupted": True}, "error"),
        ({"is_error": False}, "success"),
        ({"is_error": True}, "error"),
        ({}, "unknown"),
        (None, "unknown"),
        ("stdout text", "unknown"),
    ],
)
def test_bash_outcome(tel, response, expected) -> None:
    assert tel.bash_outcome(response) == expected


# ---------------------------------------------------------------------------
# Funnel state + dedupe
# ---------------------------------------------------------------------------


def _post_tool(tool_name: str, tool_input: dict, session="s1", response=None) -> dict:
    return {
        "session_id": session,
        "tool_name": tool_name,
        "tool_input": tool_input,
        "tool_response": response,
    }


def test_mcp_used_emitted_once_per_session(tel, no_send, state_dir) -> None:
    call = _post_tool("mcp__plugin_probe-research_probe-research__browse", {})
    tel.handle_post_tool(call)
    tel.handle_post_tool(call)
    tel.handle_post_tool(_post_tool("mcp__probe-research__entity", {}))
    events = [e for e in no_send if e["event"] == tel.EVENT_MCP_USED]
    assert len(events) == 1
    assert events[0]["properties"]["tool"] == "browse"


def test_skill_emitted_once_per_skill(tel, no_send, state_dir) -> None:
    tel.handle_post_tool(_post_tool("Skill", {"skill": "start-research-work"}))
    tel.handle_post_tool(_post_tool("Skill", {"skill": "start-research-work"}))
    tel.handle_post_tool(_post_tool("Skill", {"skill": "track-research-work"}))
    skills = [e["properties"]["skill"] for e in no_send if e["event"] == tel.EVENT_SKILL_INVOKED]
    assert skills == ["start-research-work", "track-research-work"]


def test_write_events_carry_entity_verb_outcome(tel, no_send, state_dir) -> None:
    tel.handle_post_tool(
        _post_tool("Bash", {"command": "probe run start --project x"}, response={"exit_code": 0})
    )
    writes = [e for e in no_send if e["event"] == tel.EVENT_WRITE]
    assert len(writes) == 1
    assert writes[0]["properties"] == {
        "session_id": "s1",
        "entity_type": "run",
        "verb": "start",
        "outcome": "success",
        "via": "cli",
    }


def test_write_events_are_capped_but_counted(tel, no_send, state_dir) -> None:
    for _ in range(tel.MAX_WRITE_EVENTS + 5):
        tel.handle_post_tool(_post_tool("Bash", {"command": "probe run set k=v"}))
    writes = [e for e in no_send if e["event"] == tel.EVENT_WRITE]
    assert len(writes) == tel.MAX_WRITE_EVENTS
    tel.handle_session_end({"session_id": "s1", "reason": "exit"})
    summary = [e for e in no_send if e["event"] == tel.EVENT_SESSION_SUMMARY][0]
    assert summary["properties"]["write_count"] == tel.MAX_WRITE_EVENTS + 5
    assert summary["properties"]["write_happened"] is True


def test_session_end_summarizes_and_clears_state(tel, no_send, state_dir) -> None:
    tel.handle_session_start({"session_id": "s2", "source": "startup"})
    tel.handle_post_tool(_post_tool("mcp__probe-research__browse", {}, session="s2"))
    tel.handle_post_tool(_post_tool("Skill", {"skill": "track-research-work"}, session="s2"))
    tel.handle_session_end({"session_id": "s2", "reason": "logout"})
    summary = [e for e in no_send if e["event"] == tel.EVENT_SESSION_SUMMARY][0]
    props = summary["properties"]
    assert props["mcp_used"] is True
    assert props["skill_invoked"] is True
    assert props["skills_invoked"] == ["track-research-work"]
    assert props["write_happened"] is False
    assert not (Path(str(state_dir)) / "s2.json").exists()


def test_prune_drops_only_stale_state(tel, state_dir) -> None:
    import os
    import time

    tel.save_state("fresh", {"started_at": time.time()})
    tel.save_state("stale", {"started_at": time.time()})
    old = time.time() - 3 * 86400
    os.utime(tel._state_path("stale"), (old, old))
    tel.prune_state()
    assert Path(tel._state_path("fresh")).exists()
    assert not Path(tel._state_path("stale")).exists()


# ---------------------------------------------------------------------------
# Enrichment (build_batch is the sender's pure core)
# ---------------------------------------------------------------------------


def test_batch_authenticated_user_merges_with_server_events(tel) -> None:
    ident = {
        "distinct_id": "8d6c8b3e-user-uuid",
        "email": "m@anthrogen.com",
        "customer_id": "anthrogen",
        "workspace_id": "ws-uuid",
        "authenticated": True,
    }
    events = [{"event": tel.EVENT_MCP_USED, "properties": {"session_id": "s1", "tool": "t"}}]
    (entry,) = tel.build_batch(events, ident, "0.19.0", None)
    assert entry["distinct_id"] == "8d6c8b3e-user-uuid"
    props = entry["properties"]
    assert props["client_kind"] == "plugin"
    assert props["client_version"] == "0.19.0"
    assert props["$groups"] == {"team": "anthrogen"}
    assert props["$set"] == {"email": "m@anthrogen.com"}
    assert props["authenticated"] is True
    assert "$process_person_profile" not in props


def test_batch_unauthenticated_machine_never_mints_a_person(tel) -> None:
    ident = {
        "distinct_id": "machine:abc123",
        "customer_id": None,
        "workspace_id": None,
        "authenticated": False,
    }
    events = [{"event": tel.EVENT_SESSION_STARTED, "properties": {"session_id": "s1"}}]
    (entry,) = tel.build_batch(events, ident, None, "0.75.0")
    props = entry["properties"]
    assert entry["distinct_id"] == "machine:abc123"
    assert props["$process_person_profile"] is False
    # No null-keyed team group, matching app/core/analytics.py's rule.
    assert "$groups" not in props
    assert "team" not in props
    assert props["cli_version"] == "0.75.0"


# ---------------------------------------------------------------------------
# hooks.json wiring
# ---------------------------------------------------------------------------


def test_hooks_json_wires_exactly_the_decided_events() -> None:
    hooks = json.loads((_HOOKS / "hooks.json").read_text())["hooks"]
    # Exact set on purpose: every event here costs the user something on every
    # occurrence, so another one must be a decision, not a drive-by. PreCompact
    # joined in 2026-08 to reach long-lived sessions, which SessionStart cannot
    # (see tests/test_precompact_version_hook.py).
    #
    # Stop joined for the tracking notice, and it is the most expensive event on
    # this list because it fires once per agent TURN. That is why its command
    # tests the opt-in flag IN THE SHELL and exits before starting an
    # interpreter: someone who never enabled the notice pays a file test per
    # turn, not a python process. Asserted below rather than trusted.
    #
    # UserPromptSubmit joined for the tracking toggle: a TYPED slash command
    # produces no tool use, so PostToolUse alone left the most common
    # invocation path with no deterministic flip (see test_tracking_guard.py).
    #
    # PreToolUse joined to REFUSE a probe write from an untracked session, and
    # it is the second-most expensive event here: scoped to Bash, it still
    # fires on every Bash call and doubles this file's interpreter starts on
    # that path (PostToolUse already pays one). Bought knowingly. The warn it
    # sits in front of could only narrate a project that already existed, and
    # no cheaper shape reaches the decision: `matcher` sees the tool NAME, not
    # the command, so the "does this even mention probe" test cannot happen in
    # the shell the way the Stop hook's opt-in flag does. The hook itself is
    # already minimal on the common path -- parse stdin, one stat, return.
    assert set(hooks) == {
        "UserPromptSubmit",
        "SessionStart",
        "PreCompact",
        "PreToolUse",
        "PostToolUse",
        "SessionEnd",
        "Stop",
    }
    pre = hooks["PreToolUse"][0]
    assert pre["matcher"] == "^Bash$|probe[-_]research", (
        "the deny covers Bash AND the Probe MCP tools -- `off` has to refuse a "
        "read, and a read is an MCP call. The server half is a REGEX, not a list "
        "of tool names: the same tool is `mcp__probe-research__browse` under one "
        "install and `mcp__plugin_probe-research_probe-research__browse` under "
        "another, so a list silently misses."
    )
    assert "tracking_guard.py" in pre["hooks"][0]["command"]
    assert pre["hooks"][0]["timeout"] == 5
    # Write/Edit reach the same guard for ONE check: a file write into the Probe
    # daemon's approvals folder is refused (only the researcher answers the
    # daemon). A SEPARATE group, never a wider matcher on the one above: Codex
    # trusts each hook by a hash of its entry, so editing that entry would stop
    # the guard on every Codex install until re-trusted. One more interpreter
    # start per file edit, bought knowingly.
    [edits] = [g for g in hooks["PreToolUse"] if g["matcher"] == "^(Write|Edit|MultiEdit|NotebookEdit)$"]
    assert edits["hooks"] == pre["hooks"]
    assert hooks["PreToolUse"].index(edits) == len(hooks["PreToolUse"]) - 1, "new groups go last: indexes are part of the trust key"
    prompt_hooks = hooks["UserPromptSubmit"][0]["hooks"]
    assert "tracking_guard.py" in prompt_hooks[0]["command"]
    assert all(h["timeout"] == 5 for h in prompt_hooks)
    # THE AUDIT DISPATCH LIVES HERE, and only here. It used to be rendered into
    # the team-note block, which every session of the harness reads -- including
    # `claude -p`, `codex exec` and subagents, none of which can spawn the
    # background agent it asks for. Prompt submission is the presence signal.
    assert any("note_audit.py" in h["command"] for h in prompt_hooks)
    stop = hooks["Stop"][0]["hooks"][0]["command"]
    assert "statusline-notify" in stop and "|| exit 0" in stop, (
        "the Stop hook must short-circuit in the shell before exec'ing python"
    )
    assert stop.index("statusline-notify") < stop.index("python3"), (
        "the flag test must come BEFORE the interpreter is resolved"
    )
    matcher = hooks["PostToolUse"][0]["matcher"]
    import re

    for should_match in (
        "Bash",
        "Skill",
        "SlashCommand",
        "mcp__probe-research__browse",
        "mcp__plugin_probe-research_probe-research__entity",
    ):
        assert re.search(matcher, should_match), (matcher, should_match)
    for should_not in ("Read", "Write", "Edit", "WebFetch", "mcp__posthog__exec"):
        assert not re.search(matcher, should_not), (matcher, should_not)
    # Observation hooks are bounded: a hung hook must not stall the session.
    assert hooks["PostToolUse"][0]["hooks"][0]["timeout"] == 5
    # SessionEnd is 3, not 5, because Codex caps that one event at 3s and warns
    # on every session start when a plugin asks for more ("clamping SessionEnd
    # hook timeout to 3s"). Nothing is lost: the hook only parses stdin, updates
    # the funnel state file and spawns the DETACHED sender, so the 2s we give up
    # were never used. probe-research-tap already ships 3 for the same reason.
    assert hooks["SessionEnd"][0]["hooks"][0]["timeout"] == 3


# ---------------------------------------------------------------------------
# Hosted-only gate + cross-surface join key (added with the shared core)
# ---------------------------------------------------------------------------


def _stdin_events(monkeypatch, tel, events) -> None:
    import io

    monkeypatch.setattr(tel.sys, "stdin", io.StringIO(json.dumps(events)))


def test_send_from_stdin_self_host_never_posts(tel, tmp_path, monkeypatch):
    """The one-line wiring of the egress promise: a self-host base_url must
    suppress the vendor POST — the predicate being right is not enough."""
    cfg = tmp_path / "probe" / "config.json"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(json.dumps({"base_url": "https://research.internal.example.com"}))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(cfg))
    monkeypatch.delenv("PROBE_BASE_URL", raising=False)
    posts: list = []
    monkeypatch.setattr(tel._core, "post_batch", lambda entries: posts.append(entries))
    _stdin_events(monkeypatch, tel, [{"event": tel.EVENT_MCP_USED, "properties": {}}])
    tel.send_from_stdin()
    assert posts == [], "self-host machines must never call the vendor"


def test_send_from_stdin_env_base_url_gates_too(tel, tmp_path, monkeypatch):
    cfg = tmp_path / "probe" / "config.json"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(json.dumps({}))  # empty config would default to hosted...
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(cfg))
    monkeypatch.setenv("PROBE_BASE_URL", "https://research.internal.example.com")
    posts: list = []
    monkeypatch.setattr(tel._core, "post_batch", lambda entries: posts.append(entries))
    _stdin_events(monkeypatch, tel, [{"event": tel.EVENT_MCP_USED, "properties": {}}])
    tel.send_from_stdin()
    assert posts == [], "...but PROBE_BASE_URL outranks the file, like resolve()"


def test_send_from_stdin_hosted_posts(tel, tmp_path, monkeypatch):
    cfg = tmp_path / "probe" / "config.json"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(json.dumps({}))  # unset -> hosted default -> emits
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(cfg))
    monkeypatch.delenv("PROBE_BASE_URL", raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    posts: list = []
    monkeypatch.setattr(tel._core, "post_batch", lambda entries: posts.append(entries))
    _stdin_events(monkeypatch, tel, [{"event": tel.EVENT_MCP_USED, "properties": {}}])
    tel.send_from_stdin()
    (batch,) = posts
    assert batch[0]["event"] == tel.EVENT_MCP_USED


def test_plugin_batches_carry_the_machine_join_key(tel, tmp_path, monkeypatch):
    import re as _re

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    (entry,) = tel.build_batch(
        [{"event": tel.EVENT_MCP_USED, "properties": {"session_id": "s1", "tool": "t"}}],
        {
            "distinct_id": "machine:abc",
            "authenticated": False,
            "customer_id": None,
            "workspace_id": None,
        },
        "0.19.0",
        None,
    )
    assert _re.fullmatch(r"[0-9a-f]{32}", entry["properties"]["machine_id"]), (
        "the cross-surface join key must ride plugin events too"
    )
