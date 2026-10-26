"""Kimi Code's hooks: the rendered manifests, the payload/output adapter
(hooks/harness_io.py), the guard's view of Kimi's write tools, how a
`probe` command finds the Kimi session that started it, and the dispatcher
behind Kimi's entries (D19), held to what the per-script entries gave Kimi.

Payloads are the real ones Kimi Code 2.1.1 sent (tests/fixtures/kimi_code).
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import pytest

AGENT = Path(__file__).resolve().parents[1]
HOOKS = AGENT / "plugins" / "probe-research" / "hooks"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "kimi_code"
PAYLOADS = FIXTURES / "hook_payloads"
TUI_SESSION = "session_0d2f2223-e34e-4cd1-87e3-b8d8d39aa229"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


kimi_hooks = _load("_test_kimi_hooks_tool", AGENT / "tools" / "kimi_hooks.py")


@pytest.fixture()
def isolated(tmp_path, monkeypatch):
    """Every Probe and harness root in scratch, Kimi's home a copy of the
    fixture sessions (its session_index points at the fixture paths)."""
    home = tmp_path / "home"
    kimi = tmp_path / "kimi"
    shutil.copytree(FIXTURES / "sessions", kimi / "sessions")
    index = (FIXTURES / "session_index.jsonl").read_text()
    (kimi / "session_index.jsonl").write_text(index.replace("/home/researcher/kimi-fixture/kimi", str(kimi)))
    for name, value in {
        "HOME": home,
        "XDG_STATE_HOME": tmp_path / "state",
        "XDG_CONFIG_HOME": tmp_path / "config",
        "CLAUDE_CONFIG_DIR": tmp_path / "claude",
        "CODEX_HOME": tmp_path / "codex",
        "PI_CODING_AGENT_DIR": tmp_path / "pi",
        "KIMI_CODE_HOME": kimi,
    }.items():
        monkeypatch.setenv(name, str(value))
    for name in ("CLAUDE_PLUGIN_ROOT", "PLUGIN_ROOT", "CLAUDECODE", "CODEX_THREAD_ID", "PROBE_KIMI_SESSION_ID",
                 "CLAUDE_CODE_SESSION_ID"):
        # set first, so the undo restores the real value (or its absence) even
        # when code under test writes os.environ directly
        monkeypatch.setenv(name, "x")
        monkeypatch.delenv(name)
    monkeypatch.setenv("PROBE_AGENT", "kimi_code")
    monkeypatch.setenv("KIMI_PLUGIN_ROOT", str(HOOKS.parent))
    return tmp_path


def _io():
    return _load("_test_harness_io", HOOKS / "harness_io.py")


# --- the rendered manifests ------------------------------------------------


def test_the_kimi_manifests_are_rendered_from_the_wiring():
    """A route added to routes.json and not to Kimi's manifest would silently
    never run under Kimi (it reads only its manifest)."""
    assert kimi_hooks.main(["--check"]) == 0


TRACKING = ["plugins/probe-research", "plugins/probe-research-daemon"]


def _dispatch_of(rel: str):
    return _load(f"_test_kimi_dispatch_{Path(rel).name}", AGENT / rel / "hooks" / "dispatch.py")


def _manifest(rel: str) -> list[dict]:
    return json.loads((AGENT / rel / ".kimi-plugin" / "plugin.json").read_text())["hooks"]


def _routes(rel: str) -> dict:
    return json.loads((AGENT / rel / "hooks" / "routes.json").read_text())["hooks"]


@pytest.mark.parametrize("rel", TRACKING)
def test_kimi_gets_one_dispatcher_entry_per_event(rel):
    """D19: Kimi renders to the same thin client as Claude Code and Codex. One
    entry per routes.json event, each the dispatcher's lane for it; what runs on
    it (scripts, arguments, profile exports) is routes.json's, never the entry's."""
    dispatch = _dispatch_of(rel)
    entries = _manifest(rel)
    routes = _routes(rel)
    assert [e["event"] for e in entries] == list(routes)
    for entry in entries:
        event = entry["event"]
        # Kimi's schema is strict: exactly these keys.
        assert set(entry) <= {"event", "matcher", "command", "timeout"}
        [lane] = {group["lane"] for group in routes[event]}
        assert dispatch.LANE_EVENT[lane] == event
        flags = " --unshown" if event in kimi_hooks.UNSHOWN else ""
        assert entry["command"].endswith(f'exec "$PY" -S "$ROOT/hooks/harness_io.py" --event {event}{flags}\'')
        assert "export PROBE_AGENT=kimi_code;" in entry["command"]
        assert not re.search(r"hooks/(?!harness_io\.py)[A-Za-z0-9_.-]+\.(py|sh)", entry["command"]), entry["command"]
        # The dispatcher prints before Kimi kills the entry (Kimi bounds each
        # hook by its own timeout, 30 s when it names none).
        assert entry["timeout"] == (dispatch.ENTRY_TIMEOUT[lane] or dispatch.HARNESS_DEFAULT_TIMEOUT_S)
        if lane != "session-end":
            assert dispatch.budget(lane) + dispatch.MARGIN_S <= entry["timeout"], event
    assert {e["event"] for e in entries if "--unshown" in e["command"]} == set(kimi_hooks.UNSHOWN)


_KIMI_TOOLS = (
    "Bash", "Write", "Edit", "MultiEdit", "NotebookEdit", "AskUserQuestion", "Skill", "SlashCommand", "WebSearch",
    "Read", "Grep", "Glob", "WebFetch", "Agent", "TodoWrite", "BashOutput", "ReadMediaFile",
    "mcp__plugin-probe-research:probe-research__search", "mcp__probe_research__run_list", "mcp__other__x", "",
)


@pytest.mark.parametrize("rel", TRACKING)
def test_kimi_starts_python_for_exactly_the_tools_a_route_takes(rel):
    """Kimi matches an entry's matcher as a regex search on the tool name (2.1.1
    `matches$1`: `new RegExp(pattern).test(value)`). The one entry per tool event
    must reach every tool some route takes under Kimi (else a guard is skipped)
    and no other (else every Read starts Python). An unshown event's catch-all
    never runs under Kimi, so it does not widen the matcher."""
    dispatch = _dispatch_of(rel)
    routes = _routes(rel)
    for entry in _manifest(rel):
        event = entry["event"]
        if event not in kimi_hooks.TOOL_EVENTS:
            assert entry.get("matcher") == kimi_hooks.EVENT_MATCHERS.get(event), event
            continue
        for tool in _KIMI_TOOLS:
            wanted = any(
                dispatch.matches(group.get("matcher"), tool)
                for group in routes[event]
                if group.get("matcher") or event not in kimi_hooks.UNSHOWN
            )
            assert (re.search(entry.get("matcher") or "", tool) is not None) is wanted, (event, tool)


@pytest.mark.parametrize("rel", TRACKING)
def test_telemetry_keeps_its_positional_event_argument(rel):
    """telemetry.py dispatches on `post-tool` / `session-end`; without it, it
    does nothing. Kimi's entries carry no script: the dispatcher runs the
    route's own command, argument included."""
    dispatch = _dispatch_of(rel)
    events = {e["event"] for e in _manifest(rel)}
    wiring = {"hooks": _routes(rel)}
    for lane, argument in (("post-tool", "post-tool"), ("session-end", "session-end")):
        assert dispatch.LANE_EVENT[lane] in events
        commands = [h["command"] for h in dispatch.routes(lane, {"tool_name": "Bash"}, wiring)]
        assert any(c.endswith(f"telemetry.py\" {argument}'") for c in commands), lane


def test_the_kimi_tracking_plugin_carries_the_oauth_mcp_and_the_daemon_plugin_none():
    full = json.loads((AGENT / "plugins/probe-research/.kimi-plugin/plugin.json").read_text())
    lean = json.loads((AGENT / "plugins/probe-research-daemon/.kimi-plugin/plugin.json").read_text())
    assert full["mcpServers"]["probe-research"] == {"url": "https://mcp.research.prbe.ai/mcp", "auth": "oauth"}
    assert "mcpServers" not in lean


# --- the adapter -----------------------------------------------------------


def test_normalize_puts_a_real_kimi_payload_in_claudes_shape(isolated):
    io = _io()
    row = io._hook_harness.current()
    prompt = json.loads((PAYLOADS / "tui-ask-UserPromptSubmit.json").read_text())
    out = io.normalize(prompt, row)
    assert out["session_id"] == "c1c22c25-6382-4e79-8f00-a1a45e3c8e77"
    assert out["prompt"] == "ASK ;; SAY: Thanks."
    assert out["transcript_path"].endswith(
        "session_c1c22c25-6382-4e79-8f00-a1a45e3c8e77/agents/main/wire.jsonl"
    )
    assert "permission_mode" not in out  # never derived for Kimi (see the next test)

    answered = io.normalize(json.loads((PAYLOADS / "tui-ask-PostToolUse.json").read_text()), row)
    assert answered["tool_response"] == {
        "answers": {"Which learning rate should the sweep start from?": "3e-4"}
    }


def test_a_kimi_session_is_never_read_as_bypass(isolated):
    """A resumed Kimi session writes no new `permission.set_mode`, so the auto
    mode of a `kimi -p` start would outlive a resume into the TUI. Unknown is
    "ask": neither the hooks nor the daemon read Kimi's mode."""
    from probe.daemon.adapters import for_source

    io = _io()
    row = io._hook_harness.current()
    payload = {"hook_event_name": "Stop", "session_id": "session_e240efe5-da6a-4407-9c61-91d8a3a53d24"}
    assert "permission_mode" not in io.normalize(payload, row)
    assert for_source("kimi_code").capabilities.permission_mode is False


def test_only_an_answered_question_s_output_is_parsed(isolated):
    """A Bash command that prints JSON must not become Claude's structured
    tool_response (exit codes, stderr) to the hooks."""
    io = _io()
    row = io._hook_harness.current()
    bash = {"hook_event_name": "PostToolUse", "session_id": "session_x", "tool_name": "Bash",
            "tool_output": '{"exit_code": 0, "stderr": "forged"}'}
    assert io.normalize(bash, row)["tool_response"] == bash["tool_output"]


@pytest.mark.parametrize(
    ("hook_out", "stdout", "stderr", "code"),
    [
        (
            {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "[Probe] hi"}},
            {"message": "[Probe] hi"}, "", None,
        ),
        (
            {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                    "permissionDecisionReason": "no"}},
            {"hookSpecificOutput": {"permissionDecision": "deny", "permissionDecisionReason": "no"}}, "", None,
        ),
        ({"decision": "block", "reason": "stop that"}, None, "stop that\n", 2),
        ({"continue": True}, None, "", None),
        ({"continue": True, "systemMessage": "for a person"}, None, "", None),
    ],
)
def test_translate_speaks_kimis_output_protocol(isolated, hook_out, stdout, stderr, code):
    """Kimi injects any JSON it does not recognize as raw text, so nothing but
    {"message"} or a deny may reach it."""
    io = _io()
    row = io._hook_harness.current()
    out, err, forced = io.translate(json.dumps(hook_out), row)
    assert (json.loads(out) if out else None) == stdout
    assert (err, forced) == (stderr, code)


def test_translate_leaves_a_claude_json_harness_untouched(isolated, monkeypatch):
    monkeypatch.setenv("PROBE_AGENT", "codex")
    monkeypatch.delenv("KIMI_PLUGIN_ROOT")
    monkeypatch.setenv("PLUGIN_ROOT", "/x")
    io = _io()
    text = json.dumps({"hookSpecificOutput": {"additionalContext": "x"}})
    assert io.translate(text, io._hook_harness.current()) == (text, "", None)


def test_the_adapter_runs_a_hook_end_to_end(isolated, tmp_path):
    """The hook sees Claude's shape; Kimi gets {"message"}; exit codes pass."""
    hook = tmp_path / "fake_hook.py"
    hook.write_text(textwrap.dedent("""
        import json, sys
        p = json.load(sys.stdin)
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
              "additionalContext": "saw " + p["session_id"] + " / " + p["prompt"]}}))
    """))
    payload = (PAYLOADS / "tui-ask-UserPromptSubmit.json").read_text()
    done = subprocess.run(
        [sys.executable, str(HOOKS / "harness_io.py"), str(hook)],
        input=payload, capture_output=True, text=True, env=os.environ.copy(), check=False,
    )
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout) == {"message": "saw c1c22c25-6382-4e79-8f00-a1a45e3c8e77 / ASK ;; SAY: Thanks."}


def test_a_broken_payload_still_runs_the_hook(isolated, tmp_path):
    hook = tmp_path / "echo_hook.py"
    hook.write_text("import sys; sys.stdout.write(sys.stdin.read())\n")
    done = subprocess.run(
        [sys.executable, str(HOOKS / "harness_io.py"), str(hook)],
        input="not json", capture_output=True, text=True, env=os.environ.copy(), check=False,
    )
    assert done.returncode == 0
    assert done.stdout == "not json"


# --- the guard -------------------------------------------------------------


def test_the_guard_refuses_kimis_write_into_the_approvals_folder(isolated):
    """Kimi's Write/Edit name the file `path`, often relative to the session
    folder: unmapped, the agent could write its own approval answer."""
    from probe.sdk import session_marker

    approvals = session_marker.approvals_dir()
    answers = approvals / "answers"
    answers.mkdir(parents=True)
    assert session_marker.touches_approvals("Write", {"path": str(answers / "a.json"), "content": "{}"})
    assert session_marker.touches_approvals("Edit", {"path": "answers/a.json"}, cwd=str(approvals))
    assert session_marker.touches_approvals("Write", {"path": "notes.txt"}, cwd=str(isolated)) is None
    # Claude's spelling is unchanged.
    assert session_marker.touches_approvals("Write", {"file_path": str(answers / "a.json")})


# --- which session started this process -------------------------------------


_CHILD = textwrap.dedent("""
    import json, subprocess, sys
    sys.path.insert(0, sys.argv[1])
    from probe.sdk import session_marker
    wrote = session_marker.record_harness_process("kimi_code", sys.argv[2], "kimi-code")
    # A grandchild: what a `probe` command run by Kimi's Bash tool is.
    found = subprocess.run(
        [sys.executable, "-c",
         "import sys, json; sys.path.insert(0, sys.argv[1]);"
         "from probe.sdk import session_marker;"
         "print(json.dumps(session_marker.harness_process_session()))", sys.argv[1]],
        capture_output=True, text=True, check=True,
    ).stdout
    print(json.dumps({"wrote": bool(wrote), "found": json.loads(found)}))
""")


@pytest.mark.skipif(not Path("/proc/self").is_dir(), reason="process walk is exercised on Linux here")
def test_a_command_finds_the_session_its_kimi_process_runs(isolated, tmp_path):
    script = tmp_path / "child.py"
    script.write_text(_CHILD)
    src = str(AGENT / "src")
    # `exec -a kimi-code` gives the stand-in harness process Kimi's own title.
    done = subprocess.run(
        # `; exit $?` keeps that bash alive as the parent (a lone command is exec'd).
        ["bash", "-c", f'exec -a kimi-code bash -c \'"{sys.executable}" "{script}" "{src}" 7d3c-0000-session-uuid; exit $?\''],
        capture_output=True, text=True, env=os.environ.copy(), check=False,
    )
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout) == {"wrote": True, "found": ["kimi_code", "7d3c-0000-session-uuid"]}


def test_no_kimi_ancestor_records_nothing(isolated, monkeypatch):
    from probe.sdk import session_marker

    monkeypatch.setattr(session_marker, "_ancestors", lambda pid=None: [(4300, "800", "bash"), (4250, "790", "zsh")])

    assert session_marker.record_harness_process("kimi_code", "7d3c-0000-session-uuid", "kimi-code") is None
    assert session_marker.harness_process_session() is None


def test_a_found_session_names_itself_in_the_environment(isolated, monkeypatch):
    """Kimi's shells carry no session id: the recorded one is adopted into
    os.environ, so the run and anything the script launches carry it."""
    from probe.sdk import agent_session, session_marker

    monkeypatch.setattr(agent_session, "_ADOPTED", False)
    monkeypatch.setattr(session_marker, "harness_process",
                        lambda pid=None, stop_titles=(): ("kimi_code", "c1c22c25-6382-4e79-8f00-a1a45e3c8e77", 1))
    monkeypatch.setattr(session_marker, "process_environ", lambda pid: None)
    assert agent_session.resolve_agent_session() == ("kimi_code", "c1c22c25-6382-4e79-8f00-a1a45e3c8e77")
    assert os.environ["PROBE_KIMI_SESSION_ID"] == "c1c22c25-6382-4e79-8f00-a1a45e3c8e77"
    assert agent_session.forwarding_env() == {
        "PROBE_AGENT_SESSION": "kimi_code:c1c22c25-6382-4e79-8f00-a1a45e3c8e77"
    }


@pytest.mark.parametrize("inherited", [
    {"CODEX_THREAD_ID": "019c2a53-b5a0-7ba1-8ac7-b27280b9f9cd"},  # from a Codex shell
    {"CLAUDECODE": "1", "CLAUDE_CODE_SESSION_ID": "11111111-1111-1111-1111-111111111111"},  # from a Claude shell
])
def test_the_nearest_kimi_process_wins_over_inherited_agent_markers(isolated, monkeypatch, inherited):
    from probe.sdk import agent_session, session_marker

    monkeypatch.setattr(agent_session, "_ADOPTED", False)
    for key, value in inherited.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setattr(session_marker, "harness_process",
                        lambda pid=None, stop_titles=(): ("kimi_code", "c1c22c25-6382-4e79-8f00-a1a45e3c8e77", 1))
    # The Kimi process itself inherited those markers: they are stale.
    monkeypatch.setattr(session_marker, "process_environ", lambda pid: dict(inherited))
    assert agent_session.resolve_agent_session() == ("kimi_code", "c1c22c25-6382-4e79-8f00-a1a45e3c8e77")
    assert agent_session.session_agent_from_env()[0] == "kimi_code"
    assert not any(os.environ.get(key) for key in inherited)


def test_a_nearer_coding_agent_stops_the_walk(isolated, monkeypatch, tmp_path):
    """Claude Code started inside Kimi: its `probe` belongs to Claude Code."""
    from probe.sdk import session_marker

    record = session_marker._process_record_path(4242, "777")
    record.parent.mkdir(parents=True)
    record.write_text(json.dumps({"harness": "kimi_code", "session_id": "c1c22c25-6382-4e79-8f00-a1a45e3c8e77"}))
    chain = [(4300, "800", "bash"), (4250, "790", "claude"), (4242, "777", "kimi-code")]
    monkeypatch.setattr(session_marker, "_ancestors", lambda pid=None: chain)
    assert session_marker.harness_process_session(stop_titles=("claude", "codex", "pi")) is None
    assert session_marker.harness_process_session(stop_titles=("codex",)) == (
        "kimi_code", "c1c22c25-6382-4e79-8f00-a1a45e3c8e77")


def test_ps_is_read_in_a_fixed_locale_and_zone(isolated, monkeypatch):
    """Off Linux the record key is `ps`'s start time: the hook and the command
    must read it the same way, whatever their locale or time zone."""
    import subprocess as sp

    from probe.sdk import session_marker

    seen = {}

    def fake_run(argv, **kw):
        seen.update(argv=argv, env=kw.get("env"))
        out = "  512   1 Mon Oct  5 03:24:02 2026 /bin/zsh -l\n  900 512 Mon Oct  5 03:30:11 2026 kimi-code\n"
        return sp.CompletedProcess(argv, 0, stdout=out, stderr="")

    monkeypatch.setattr(sp, "run", fake_run)
    table = session_marker._ps_table()
    assert seen["env"]["LC_ALL"] == "C" and seen["env"]["TZ"] == "UTC" and "-ww" in seen["argv"]
    assert table[900] == (512, "Mon-Oct-5-03:30:11-2026", "kimi-code")


def test_old_records_age_out_off_linux(isolated, monkeypatch):
    from probe.sdk import session_marker

    real_isdir = os.path.isdir
    monkeypatch.setattr(session_marker.os.path, "isdir", lambda p: False if p == "/proc/self" else real_isdir(p))
    folder = session_marker.harness_processes_dir()
    folder.mkdir(parents=True)
    old, fresh = folder / "1-old.json", folder / "2-new.json"
    for path in (old, fresh):
        path.write_text("{}")
    os.utime(old, (0, 0))
    session_marker._sweep_process_records(keep=folder / "3-keep.json")
    assert not old.exists() and fresh.exists()


# --- review fixes (Codex structured review, 2026-10-05) ----------------------


def test_kimis_tool_call_id_reaches_the_approvals_hook_as_tool_use_id(isolated):
    """The approvals hook marks an asked question clean by `tool_use_id`, then
    accepts the answer for it; Kimi names that id `tool_call_id`."""
    io = _io()
    row = io._hook_harness.current()
    for name in ("tui-ask-PreToolUse.json", "tui-ask-PostToolUse.json"):
        out = io.normalize(json.loads((PAYLOADS / name).read_text()), row)
        assert out["tool_use_id"] == "call_6"


@pytest.mark.parametrize("rel", TRACKING)
def test_no_kimi_post_tool_hook_claims_a_daemon_message(isolated, rel):
    """reads_hook claims a mailbox message before printing it, and Kimi drops
    PostToolUse output: the answer would vanish. The PostToolUse entry tells the
    dispatcher so (`--unshown`), and the next prompt delivers it."""
    from probe.daemon import mailbox

    sid = "c1c22c25-6382-4e79-8f00-a1a45e3c8e77"
    answer = mailbox.Message(id=mailbox.new_message_id(), session=sid, kind=mailbox.Kind.ANSWER, ask="a1b2c3",
                             question="what did the last sweep find?", text="best val_acc 0.989 at C=10")
    mailbox.publish(answer)
    root = AGENT / rel
    tool = json.loads((PAYLOADS / "tui-ask-PostToolUse.json").read_text())
    tool.update(tool_name="Bash", tool_input={"command": "ls"}, tool_output="")
    done = _kimi(_entry(rel, "PostToolUse"), tool, root)
    assert (done.returncode, done.stdout) == (0, ""), done.stderr
    assert [m.id for _, m in mailbox.waiting(sid)] == [answer.id], "claimed after a tool call nobody reads"

    prompt = json.loads((PAYLOADS / "tui-ask-UserPromptSubmit.json").read_text())
    done = _kimi(_entry(rel, "UserPromptSubmit"), prompt, root)
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout) == {"message": answer.rendered()}
    assert mailbox.waiting(sid) == []


def test_every_kimi_hook_fails_closed_without_its_plugin_root():
    """Never a hooks/ folder found from the session's own directory."""
    for rel in kimi_hooks.PLUGINS:
        for hook in json.loads((AGENT / rel / ".kimi-plugin" / "plugin.json").read_text())["hooks"]:
            command = hook["command"]
            assert '[ -n "$ROOT" ] || exit 0' in command and "$PWD" not in command
            assert "unset PLUGIN_ROOT CLAUDE_PLUGIN_ROOT" in command


def test_the_capture_hooks_never_speak_to_kimis_model():
    """The tap's scripts print Claude's `{"continue": true}` / systemMessage;
    Kimi would inject them into the model's context."""
    tap = json.loads((AGENT / "plugins/probe-research-tap/.kimi-plugin/plugin.json").read_text())
    assert tap["hooks"] and all(h["command"].endswith(">/dev/null'") for h in tap["hooks"])


def test_an_agent_started_inside_kimi_keeps_its_own_session(isolated, monkeypatch):
    """pi run inside Kimi sets PI_* for its children; the Kimi process never had
    them, so they were set below it: the process is pi's, not Kimi's."""
    from probe.sdk import agent_session, session_marker

    monkeypatch.setattr(agent_session, "_ADOPTED", False)
    monkeypatch.setenv("PI_CODING_AGENT", "true")
    monkeypatch.setenv("PI_SESSION_ID", "22222222-2222-2222-2222-222222222222")
    monkeypatch.setattr(session_marker, "harness_process",
                        lambda pid=None, stop_titles=(): ("kimi_code", "c1c22c25-6382-4e79-8f00-a1a45e3c8e77", 1))
    monkeypatch.setattr(session_marker, "process_environ", lambda pid: {"HOME": "/h"})
    assert agent_session.adopt_harness_process_session() == {}
    assert os.environ["PI_SESSION_ID"] == "22222222-2222-2222-2222-222222222222"


def test_a_session_already_carried_is_never_reassigned(isolated, monkeypatch):
    """A job adopted session A; after /new the record says B. The job's later
    children inherit A, and keep it."""
    from probe.sdk import agent_session, session_marker

    monkeypatch.setattr(agent_session, "_ADOPTED", False)
    monkeypatch.setenv("PROBE_KIMI_SESSION_ID", "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
    monkeypatch.setattr(session_marker, "harness_process",
                        lambda pid=None, stop_titles=(): ("kimi_code", "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", 1))
    monkeypatch.setattr(session_marker, "process_environ", lambda pid: {"HOME": "/h"})  # the job set it
    assert agent_session.adopt_harness_process_session() == {}
    assert agent_session.resolve_agent_session() == ("kimi_code", "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")


def test_a_kimi_started_inside_an_adopted_job_gets_its_own_session(isolated, monkeypatch):
    """The inner Kimi process inherited the job's id: that id is stale for it."""
    from probe.sdk import agent_session, session_marker

    monkeypatch.setattr(agent_session, "_ADOPTED", False)
    monkeypatch.setenv("PROBE_KIMI_SESSION_ID", "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
    monkeypatch.setattr(session_marker, "harness_process",
                        lambda pid=None, stop_titles=(): ("kimi_code", "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", 1))
    monkeypatch.setattr(session_marker, "process_environ",
                        lambda pid: {"PROBE_KIMI_SESSION_ID": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"})
    assert agent_session.resolve_agent_session() == ("kimi_code", "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")


def test_on_macos_kimi_reads_as_its_binary_and_is_still_found(isolated, monkeypatch):
    """macOS's `ps` keeps the name Kimi was started as (`kimi`), not the
    `kimi-code` title Linux shows: a hook that looked only for the title wrote
    no record there, and every `probe` command from Kimi's shell said "no
    session id" (seen on Darwin, probe 0.215.0, 2026-10-05)."""
    from probe.sdk import session_marker

    mac = [(45901, "Mon-Oct-5-23:10:02-2026", "/bin/bash"), (35972, "Mon-Oct-5-22:41:13-2026", "kimi"),
           (34815, "Mon-Oct-5-09:00:00-2026", "-zsh")]
    monkeypatch.setattr(session_marker, "_ancestors", lambda pid=None: mac)

    assert session_marker.record_harness_process("kimi_code", "659a3020-6ec3-45c7-8f7b-274f811549be", "kimi-code") is None
    path = session_marker.record_harness_process(
        "kimi_code", "659a3020-6ec3-45c7-8f7b-274f811549be", ("kimi-code", "kimi")
    )
    assert path is not None and path.name.startswith("35972-")
    assert session_marker.harness_process_session() == ("kimi_code", "659a3020-6ec3-45c7-8f7b-274f811549be")


def test_the_hook_offers_kimis_title_and_its_binary(isolated, monkeypatch):
    io = _io()
    seen = []
    monkeypatch.setattr(io._session_marker, "record_harness_process", lambda *args, **kwargs: seen.append(args))
    row = io._hook_harness.current()  # PROBE_AGENT=kimi_code (the fixture)
    io._record({"hook_event_name": "SessionStart", "session_id": "659a3020-6ec3-45c7-8f7b-274f811549be"}, row)
    assert seen == [("kimi_code", "659a3020-6ec3-45c7-8f7b-274f811549be", ("kimi-code", "kimi"))]


@pytest.mark.parametrize(
    ("argv", "title"),
    [
        (["kimi-code"], "kimi-code"),
        (["/Users/r/.kimi-code/bin/kimi"], "/Users/r/.kimi-code/bin/kimi"),
        (["node", "/opt/homebrew/bin/pi", "--mode", "rpc"], "/opt/homebrew/bin/pi"),
        (["/usr/local/bin/bun", "/usr/local/bin/claude"], "/usr/local/bin/claude"),
        (["node", "--inspect"], "node"),
    ],
)
def test_a_script_runtime_reads_as_the_script(argv, title):
    """On macOS `ps` shows no retitle, so an npm-installed agent reads as
    `node <script>`: without this a nested pi inside Kimi was not a stop and its
    commands adopted Kimi's session."""
    from probe.sdk import session_marker

    assert session_marker._title_of(argv) == title


def test_a_nested_agent_run_by_node_stops_the_walk_on_macos(isolated, monkeypatch):
    from probe.sdk import session_marker

    rows = (
        "  501 500 Mon Oct  5 23:10:02 2026 /bin/bash -c probe session status\n"
        "  500 400 Mon Oct  5 23:09:00 2026 node /opt/homebrew/bin/pi\n"
        "  400 300 Mon Oct  5 22:41:13 2026 kimi\n"
    )
    monkeypatch.setattr(session_marker.os.path, "isdir", lambda p: False if p == "/proc/self" else os.path.isdir(p))
    monkeypatch.setattr(
        "subprocess.run", lambda *a, **k: subprocess.CompletedProcess(a, 0, rows, "")
    )
    chain = session_marker._ancestors(501)
    assert [title for _pid, _start, title in chain] == ["/bin/bash", "/opt/homebrew/bin/pi", "kimi"]
    session_marker._publish_atomically(session_marker._process_record_path(400, chain[2][1]),
                                       json.dumps({"harness": "kimi_code", "session_id": "659a3020-6ec3-45c7-8f7b-274f811549be"}))
    assert session_marker.harness_process_session(501, stop_titles=("pi",)) is None
    assert session_marker.harness_process_session(501) == ("kimi_code", "659a3020-6ec3-45c7-8f7b-274f811549be")


# --- a skill the person types fires only TurnStarted in Kimi (2.1.1) ---------

_SKILL_TURN = (
    'User activated the skill "probe". Follow the loaded skill instructions.\n\n'
    '<skill-loaded name="probe" trigger="{trigger}" source="extra" dir="/x/skills/probe" args="{args}">\n'
    "# Probe\n...\nARGUMENTS: {args}\n</skill-loaded>"
)


def _turn(trigger="user-slash", args="on", origin="skill_activation", prompt=None):
    return {"hook_event_name": "TurnStarted", "session_id": "session_bba6ba1d-ca48-4588-8a99-e8112bbd669c",
            "origin_kind": origin, "turn_id": 0,
            "prompt": prompt if prompt is not None else _SKILL_TURN.format(trigger=trigger, args=args)}


@pytest.mark.parametrize(
    ("payload", "typed"),
    [
        (_turn(), "/probe on"),
        (_turn(args="read"), "/probe read"),
        (_turn(args=""), "/probe"),
        (_turn(trigger="model"), None),  # the model loaded it: not a person's switch
        (_turn(origin="user"), None),  # an ordinary prompt came through UserPromptSubmit
        (_turn(prompt="see <skill-loaded name=\"probe\" trigger=\"user-slash\" args=\"on\">"), None),  # quoted, not leading
        ({"hook_event_name": "UserPromptSubmit", "prompt": "/probe on"}, None),
    ],
)
def test_a_typed_skill_is_read_from_kimis_own_block(payload, typed):
    assert _io().typed_skill(payload) == typed


def test_a_typed_probe_on_reaches_the_switch_as_the_typed_line(isolated, tmp_path):
    """`/probe on` in Kimi fired no UserPromptSubmit, so the session stayed off
    while the model reported "on" (seen 2026-10-06). The adapter hands the hook
    the typed line as UserPromptSubmit and keeps the hook's output out of Kimi;
    any other TurnStarted never runs the hook."""
    seen = tmp_path / "seen.json"
    hook = tmp_path / "echo_hook.py"
    hook.write_text(
        "import sys, json\n"
        f"open({str(seen)!r}, 'w').write(sys.stdin.read())\n"
        "print(json.dumps({'hookSpecificOutput': {'additionalContext': 'said'}}))\n"
    )
    run = lambda payload: subprocess.run(  # noqa: E731
        [sys.executable, str(HOOKS / "harness_io.py"), str(hook)],
        input=json.dumps(payload), capture_output=True, text=True, env=os.environ.copy(), check=False,
    )
    done = run(_turn())
    assert done.returncode == 0 and done.stdout == "", done.stderr
    got = json.loads(seen.read_text())
    assert got["hook_event_name"] == "UserPromptSubmit" and got["prompt"] == "/probe on"
    assert got["session_id"] == "bba6ba1d-ca48-4588-8a99-e8112bbd669c"

    seen.unlink()
    assert run(_turn(origin="user")).returncode == 0
    assert not seen.exists()


def test_the_adapter_knows_exactly_the_switchs_skills():
    sys.path.insert(0, str(HOOKS))  # the guard imports its siblings by name
    try:
        guard = _load("_test_tracking_guard_slugs", HOOKS / "tracking_guard.py")
    finally:
        sys.path.remove(str(HOOKS))
    assert _io()._SWITCH_SLUGS == guard.TOGGLE_SKILL_SLUGS


def test_another_typed_skill_never_runs_the_switch():
    """`/commit` typed in Kimi is not Probe's business: running the switch on it
    would claim a daemon notice the dropped output never shows."""
    payload = _turn()
    payload["prompt"] = payload["prompt"].replace('name="probe"', 'name="commit"')
    assert _io().typed_skill(payload) is None


# --- the dispatcher behind Kimi's entries (D19) ------------------------------
#
# Every check below runs a manifest's entries the way Kimi Code 2.1.1 runs them
# (`runMatchedHooks`: the event's entries whose matcher regex-matches the value,
# each command once, the payload on stdin, the plugin folder as cwd) and reads
# the results the way it does (`_kimi_view`). PARITY: the per-script entries
# every manifest through plugin 0.163.0 had (pinned below) and the one dispatcher
# entry per event must give Kimi the same thing.

OLD_HOOKS = FIXTURES / "per_script_hooks_0.163.0.json"
_OLD_SCRIPT = re.compile(r'hooks/([A-Za-z0-9_.-]+\.(?:sh|py))"?((?: (?:--?)?[a-z][a-z-]*)*)')
_OLD_EXPORTS = re.compile(r"export ((?:PROBE_HOOK_EVENT|PROBE_PLUGIN_PROFILE|PROBE_TAP_SOURCE)=[a-z_]+)")
_KIMI_SID = "session_c1c22c25-6382-4e79-8f00-a1a45e3c8e77"


def _old_hooks(rel: str) -> list[dict]:
    return json.loads(OLD_HOOKS.read_text())[Path(rel).name]


def _per_script_entries(routes: dict) -> list[dict]:
    """What plugin 0.163.0's renderer made of a routes.json: one entry per
    script, each `harness_io.py <script> [args]`, the reads catch-all after a
    tool call left out, and TurnStarted as the UserPromptSubmit switch's twin.
    `test_the_per_script_replica_renders_0_163_0` holds it to the real thing."""
    entries = []
    for event, groups in routes.items():
        if event == "TurnStarted":
            continue  # 0.163.0's routes.json had none; the twin below stood for it
        for group in groups:
            for hook in group["hooks"]:
                script, args = _OLD_SCRIPT.findall(hook["command"])[-1]
                if (event, script) == ("PostToolUse", "reads_hook.py"):
                    continue
                exports = [e for e in _OLD_EXPORTS.findall(hook["command"]) if not e.startswith("PROBE_TAP_SOURCE=")]
                env = " ".join(dict.fromkeys(["PROBE_AGENT=kimi_code", *exports]))
                entry = {"event": event}
                if group.get("matcher"):
                    entry["matcher"] = group["matcher"]
                entry["command"] = (
                    "/bin/bash -c 'ROOT=\"${KIMI_PLUGIN_ROOT:-}\"; [ -n \"$ROOT\" ] || exit 0; "
                    f"unset PLUGIN_ROOT CLAUDE_PLUGIN_ROOT; export {env}; "
                    f'[ -f "$ROOT/hooks/{script}" ] || exit 0; PY="$(command -v python3)" || exit 0; '
                    f'exec "$PY" "$ROOT/hooks/harness_io.py" {script}{args}\''
                )
                if isinstance(hook.get("timeout"), int):
                    entry["timeout"] = hook["timeout"]
                entries.append(entry)
    twin = next(e for e in entries if e["event"] == "UserPromptSubmit" and e["command"].endswith(" tracking_guard.py'"))
    entries.append({"event": "TurnStarted", "matcher": "^skill_activation$",
                    **{k: v for k, v in twin.items() if k not in ("event", "matcher")}})
    return entries


def _entry(rel: str, event: str) -> dict:
    [entry] = [e for e in _manifest(rel) if e["event"] == event]
    return entry


def _kimi(entry: dict, payload: dict, root: Path, env: "dict | None" = None) -> subprocess.CompletedProcess:
    """One entry, as Kimi Code runs a plugin hook: KIMI_PLUGIN_ROOT set, the
    plugin folder as cwd. The warm host is off unless `env` turns it on."""
    full = {**os.environ, "KIMI_PLUGIN_ROOT": str(root), "PROBE_HOOK_HOST": "off", **(env or {})}
    return subprocess.run(["/bin/bash", "-c", entry["command"]], input=json.dumps(payload), capture_output=True,
                          text=True, env=full, cwd=str(root), timeout=60, check=False)


def _kimi_value(event: str, payload: dict) -> str:
    """What Kimi matches an entry's matcher against."""
    if event in kimi_hooks.TOOL_EVENTS:
        return payload.get("tool_name") or ""
    if event == "TurnStarted":
        return payload.get("origin_kind") or ""
    prompt = payload.get("prompt")
    if isinstance(prompt, list):
        return " ".join(p.get("text", "") for p in prompt if isinstance(p, dict) and p.get("type") == "text")
    return prompt if isinstance(prompt, str) else ""


def _kimi_runs(entries: list, payload: dict, root: Path, env: "dict | None" = None) -> list:
    event, value = payload["hook_event_name"], _kimi_value(payload["hook_event_name"], payload)
    done, seen = [], set()
    for entry in entries:
        if entry["event"] != event or re.search(entry.get("matcher") or "", value) is None:
            continue
        if entry["command"] not in seen:
            seen.add(entry["command"])
            done.append(_kimi(entry, payload, root, env))
    return done


def _kimi_view(results: list) -> dict:
    """What Kimi Code 2.1.1 makes of an event's results: the block it acts on
    (`blockDecision`: the first; exit 2's stderr, or a structured deny's reason)
    and, when nothing blocks, the context a prompt gets (`renderUserPromptHookResult`:
    every clean result's `message`, else its stdout, joined by a blank line)."""
    block, context = None, []
    for done in results:
        out = done.stdout.strip()
        message, denied = None, None
        if done.returncode == 2:
            denied = done.stderr.strip()
        elif done.returncode == 0 and out:
            try:
                obj = json.loads(out)
            except ValueError:
                obj = None
            if isinstance(obj, dict):
                specific = obj.get("hookSpecificOutput") if isinstance(obj.get("hookSpecificOutput"), dict) else {}
                message = obj.get("message") or specific.get("message")
                if specific.get("permissionDecision") == "deny":
                    denied = specific.get("permissionDecisionReason") or ""
        if denied is not None:
            block = denied if block is None else block
        elif done.returncode == 0 and (message or out):
            context.append(message or out)
    return {"block": block, "context": "" if block is not None else "\n\n".join(context)}


def _payload(event: str, **fields) -> dict:
    body = {"hook_event_name": event, "session_id": _KIMI_SID, "cwd": "/tmp/kimi-proj",
            "client_type": "kimi_code_cli", "session_title": "t"}
    body.update(fields)
    return body


def _prompt(text: str) -> dict:
    return _payload("UserPromptSubmit", prompt=[{"type": "text", "text": text}], is_steer=False)


def _tool(event: str, tool: str, tool_input: dict, **fields) -> dict:
    return _payload(event, tool_name=tool, tool_input=tool_input, tool_call_id="call_9", **fields)


@pytest.mark.parametrize("rel", TRACKING)
def test_the_per_script_replica_renders_0_163_0(rel):
    """The old shape the parity checks compare against is the one that shipped:
    today's routes less the ones added since (the Skill route that refreshes
    Claude Code's skill copies, a no-op under Kimi, which has none; the prompt
    route that moves a session off an old `tap watch`, which leaves Kimi's
    sessions alone)."""
    routes = {
        e: [{**g, "hooks": [h for h in g["hooks"] if "tap_handover.py" not in h["command"]]}
            for g in groups if g.get("matcher") != "^Skill$"]
        for e, groups in _routes(rel).items() if e != "TurnStarted"
    }
    assert _per_script_entries(routes) == _old_hooks(rel)


@pytest.mark.parametrize("rel", TRACKING)
def test_an_open_sessions_per_script_entries_still_find_their_files(rel):
    """A Kimi session left open across this update keeps its 0.163.0 entries
    (Kimi re-reads a manifest only when plugins reload). Each still finds its
    script beside the new harness_io.py, which still takes `<script> [args]`, so
    none falls silent at its `[ -f ... ] || exit 0`."""
    hooks = AGENT / rel / "hooks"
    for entry in _old_hooks(rel):
        script, args = re.search(r'harness_io\.py" ([A-Za-z0-9_.-]+)((?: [a-z-]+)*)\'$', entry["command"]).groups()
        assert f'[ -f "$ROOT/hooks/{script}" ] || exit 0' in entry["command"]
        assert (hooks / script).is_file(), f"{entry['event']}: {script} is gone"
        assert (hooks / "harness_io.py").is_file()


def _fresh_state(tmp_path: Path, monkeypatch, name: str) -> dict:
    """A fresh Probe state folder for one run, made current for this process too."""
    state = tmp_path / name
    state.mkdir()
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    return {"XDG_STATE_HOME": str(state)}


@pytest.mark.parametrize("rel", TRACKING)
def test_parity_a_guarded_write_is_refused_and_a_plain_one_allowed(isolated, rel):
    """CRITICAL. The real guard, both shapes, the same refusal (and the same
    nothing for a write anywhere else)."""
    from probe.sdk import session_marker

    root = AGENT / rel
    aimed = _tool("PreToolUse", "Write", {"path": str(session_marker.approvals_dir() / "answers" / "a.json"),
                                          "content": "{}"})
    plain = _tool("PreToolUse", "Write", {"path": str(isolated / "notes.txt"), "content": "x"})
    for payload, refused in ((aimed, True), (plain, False)):
        old = _kimi_view(_kimi_runs(_old_hooks(rel), payload, root))
        new = _kimi_view(_kimi_runs(_manifest(rel), payload, root))
        assert new == old
        assert (new["block"] is not None) is refused, new
        if refused:
            assert "approvals" in new["block"]


@pytest.mark.parametrize("rel", TRACKING)
def test_parity_a_prompt_gets_the_daemon_answer_waiting_for_it(isolated, tmp_path, monkeypatch, rel):
    """CRITICAL. Five prompt routes in parallel through the dispatcher give Kimi
    the context five entries did: the daemon's answer, once, claimed once."""
    from probe.daemon import mailbox

    root = AGENT / rel
    sid = _KIMI_SID.split("_", 1)[1]
    answer = mailbox.Message(id=mailbox.new_message_id(), session=sid, kind=mailbox.Kind.ANSWER, ask="a1b2c3",
                             question="what did the last sweep find?", text="best val_acc 0.989 at C=10")
    views = {}
    for name, entries in (("old", _old_hooks(rel)), ("new", _manifest(rel))):
        env = _fresh_state(tmp_path, monkeypatch, name)
        mailbox.publish(answer)
        views[name] = _kimi_view(_kimi_runs(entries, _prompt("go on with the sweep"), root, env))
        assert mailbox.waiting(sid) == [], name
    assert views["new"] == views["old"]
    assert views["new"]["block"] is None and answer.rendered() in views["new"]["context"]


@pytest.mark.parametrize("inherited", ["CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID"])
@pytest.mark.parametrize("rel", TRACKING)
def test_a_kimi_started_inside_another_agent_still_gets_its_own_answer(isolated, tmp_path, monkeypatch, rel,
                                                                        inherited):
    """Kimi run from Claude Code's or Codex's shell inherits the parent's session
    id. The reads route's shell gate reads that before the payload: it looked in
    the PARENT's inbox, found nothing, skipped the route (Kimi's own answer was
    never delivered, on any prompt) and started a new turn for the parent. The
    per-script entry ran the hook on Kimi's own id. Review of #3292 (P2)."""
    from probe.daemon import mailbox

    root = AGENT / rel
    sid = _KIMI_SID.split("_", 1)[1]
    parent = "0199a1b2-c3d4-7e5f-8a9b-0c1d2e3f4a5b"
    answer = mailbox.Message(id=mailbox.new_message_id(), session=sid, kind=mailbox.Kind.ANSWER, ask="a1b2c3",
                             question="what did the last sweep find?", text="best val_acc 0.989 at C=10")
    monkeypatch.setenv(inherited, parent)
    views = {}
    for name, entries in (("old", _old_hooks(rel)), ("new", _manifest(rel))):
        env = _fresh_state(tmp_path, monkeypatch, name)
        # The parent is a session the daemon's reader serves: it has a turn.
        turn = Path(env["XDG_STATE_HOME"]) / "probe" / "reads" / "turns" / parent
        turn.parent.mkdir(parents=True)
        turn.write_text("parent-turn")
        mailbox.publish(answer)
        views[name] = _kimi_view(_kimi_runs(entries, _prompt("go on with the sweep"), root, env))
        assert mailbox.waiting(sid) == [], f"{name}: Kimi's answer was never delivered"
        assert turn.read_text() == "parent-turn", f"{name}: a Kimi prompt ended the parent's turn"
    assert views["new"] == views["old"]
    assert answer.rendered() in views["new"]["context"]


@pytest.mark.parametrize("rel", TRACKING)
def test_every_harness_marker_a_route_gate_reads_is_dropped_under_kimi(isolated, rel):
    """The routes' shell gates and the dispatcher's own copy of one read the
    environment before the payload. Every harness marker they read must be one
    `harness_io.py --event` drops, or an inherited one picks the wrong session
    (the case above). A new gate reading another marker fails here first."""
    io = _io()
    registry = json.loads((HOOKS / "harnesses.json").read_text())["harnesses"]
    markers = {name for raw in registry for name in [raw.get("session_env"), *(raw.get("detect_env") or [])] if name}
    commands = json.dumps(_routes(rel))
    read = set(re.findall(r"\$\{([A-Z_][A-Z0-9_]*)", commands))
    read |= set(re.findall(r"""environ\.get\(["']([A-Z_][A-Z0-9_]*)["']""", (AGENT / rel / "hooks" / "dispatch.py").read_text()))
    gated = read & markers
    assert gated, "the reads gates read the session id: this check would hold nothing"
    assert gated <= set(io.foreign_session_envs(io._hook_harness.current())), sorted(gated)
    assert "PROBE_KIMI_SESSION_ID" not in io.foreign_session_envs(io._hook_harness.current())


@pytest.mark.parametrize("rel", TRACKING)
def test_parity_a_typed_switch_flips_the_session_and_says_nothing(isolated, tmp_path, monkeypatch, rel):
    """CRITICAL. `/probe read` typed in Kimi fires only TurnStarted: both shapes
    hand the switch the typed line and drop what it says."""
    from probe.sdk import session_marker

    root = AGENT / rel
    sid = _KIMI_SID.split("_", 1)[1]
    turn = _turn(args="read")
    turn["session_id"] = _KIMI_SID
    states, views = {}, {}
    for name, entries in (("old", _old_hooks(rel)), ("new", _manifest(rel))):
        env = _fresh_state(tmp_path, monkeypatch, name)
        assert session_marker.session_state(sid) is None
        views[name] = _kimi_view(_kimi_runs(entries, turn, root, env))
        states[name] = session_marker.session_state(sid)
    assert views["new"] == views["old"] == {"block": None, "context": ""}
    assert states["new"] == states["old"] is not None
    # Any other turn runs nothing (Kimi's matcher, then the adapter).
    env = _fresh_state(tmp_path, monkeypatch, "model")
    loaded = _turn(trigger="model", args="off")
    loaded["session_id"] = _KIMI_SID
    assert _kimi_view(_kimi_runs(_manifest(rel), loaded, root, env)) == {"block": None, "context": ""}
    assert session_marker.session_state(sid) is None


# The dispatcher's machinery itself, on a plugin of stand-in routes in the real
# routes' shape: several routes merged, arguments, a veto, quiet, the warm host.

_STAND_IN = textwrap.dedent("""
    import json, os, sys
    name = os.path.basename(sys.argv[0])
    payload = json.load(sys.stdin)
    with open(os.path.join(os.environ["XDG_STATE_HOME"], "seen.jsonl"), "a") as fh:
        fh.write(json.dumps([name, sys.argv[1:], payload.get("hook_event_name"), payload.get("session_id"),
                             payload.get("prompt"), os.environ.get("PROBE_HOOK_QUIET"),
                             os.environ.get("PROBE_HOOK_HOSTED"), os.environ.get("PROBE_AGENT")]) + "\\n")
    event = payload.get("hook_event_name")
    def say(text):
        print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}))
    if name == "guard.py":
        if "rm -rf" in (payload.get("tool_input") or {}).get("command", ""):
            print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "permissionDecision": "deny",
                                                     "permissionDecisionReason": "no rm -rf here"}}))
    elif name == "veto.py":
        if "veto" in str(payload.get("prompt")):
            sys.stderr.write("vetoed by Probe\\n")
            sys.exit(2)
    elif name == "silent.py":
        print(json.dumps({"continue": True, "systemMessage": "for a person"}))
    elif name == "tracking_guard.py":
        if str(payload.get("prompt")).startswith("/probe"):
            say("[switch] " + payload["prompt"])
    elif name == "reads_hook.py":
        say("[Probe] delivered after " + str(event))
    else:
        say("[" + " ".join(sys.argv[1:]) + "] saw " + str(payload.get("prompt") or payload.get("tool_name")))
""")
_STAND_INS = ("guard.py", "veto.py", "silent.py", "tracking_guard.py", "reads_hook.py", "note.py", "tool.py")
_COPIED = ("harness_io.py", "dispatch.py", "dispatch.sh", "zygote.py", "_hook_harness.py", "_harness_registry.py",
           "harnesses.json", "_session_marker.py", "_service_paths.py", "_probe_config.py")


def _stand_in_routes(dispatch) -> dict:
    def route(script, *args, timeout=5):
        return {"type": "command", "command": dispatch._plain_command([], script, True, list(args)), "timeout": timeout}

    switch = route("tracking_guard.py")
    return {"hooks": {
        "UserPromptSubmit": [{"lane": "prompt", "hooks": [
            switch, route("note.py", "alpha"), route("silent.py"), route("veto.py"), route("note.py", "beta"),
            route("reads_hook.py"),
        ]}],
        "PreToolUse": [
            {"lane": "pre-tool", "matcher": "^Bash$", "hooks": [route("guard.py")]},
            {"lane": "pre-tool", "matcher": "^(Write|Edit)$", "hooks": [route("note.py", "pre")]},
        ],
        "PostToolUse": [
            {"lane": "post-tool", "matcher": "^Bash$", "hooks": [route("tool.py", "post-tool")]},
            {"lane": "post-tool", "hooks": [route("reads_hook.py")]},
        ],
        "Stop": [{"lane": "stop", "hooks": [route("note.py", "stop")]}],
        "TurnStarted": [{"lane": "turn-started", "hooks": [switch]}],
    }}


@pytest.fixture()
def stand_in(isolated, tmp_path):
    """A plugin folder with the real adapter and dispatcher and stand-in routes;
    (its folder, its old per-script entries, its new dispatcher entries)."""
    root = tmp_path / "plugin"
    hooks = root / "hooks"
    hooks.mkdir(parents=True)
    for name in _COPIED:
        shutil.copy2(HOOKS / name, hooks / name)
    for name in _STAND_INS:
        (hooks / name).write_text(_STAND_IN)
    routes = _stand_in_routes(_load("_test_kimi_stand_in_dispatch", hooks / "dispatch.py"))
    (hooks / "routes.json").write_text(json.dumps(routes))
    return root, _per_script_entries(routes["hooks"]), kimi_hooks.render_hooks(root, True)


def _seen(env: dict) -> list:
    path = Path(env["XDG_STATE_HOME"]) / "seen.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    return sorted(rows, key=json.dumps)


_CASES = {
    "a prompt, several routes": _prompt("go on"),
    "a prompt a route vetoes": _prompt("please veto this"),
    "a refused tool call": _tool("PreToolUse", "Bash", {"command": "rm -rf /"}),
    "an allowed tool call": _tool("PreToolUse", "Bash", {"command": "ls"}),
    "a write with context": _tool("PreToolUse", "Write", {"path": "x.txt", "content": ""}),
    "a tool no route takes": _tool("PreToolUse", "Read", {"path": "x.txt"}),
    "after a tool call": _tool("PostToolUse", "Bash", {"command": "ls"}, tool_output="ok"),
    "a stop": _payload("Stop", stop_hook_active=False),
}


@pytest.mark.parametrize("case", list(_CASES))
def test_parity_the_dispatcher_gives_kimi_what_the_per_script_entries_did(stand_in, tmp_path, monkeypatch, case):
    """CRITICAL. Same view (block and context), same routes run with the same
    payload in Claude's shape, arguments and harness: the merge of several
    routes reads to Kimi as their separate entries did."""
    root, old, new = stand_in
    payload = _CASES[case]
    views, seen = {}, {}
    for name, entries in (("old", old), ("new", new)):
        env = _fresh_state(tmp_path, monkeypatch, name)
        # A daemon message waits: still nothing after a tool call may claim it.
        (Path(env["XDG_STATE_HOME"]) / "probe" / "reads" / "messages" / "s").mkdir(parents=True)
        (Path(env["XDG_STATE_HOME"]) / "probe" / "reads" / "messages" / "s" / "m.json").write_text("{}")
        views[name] = _kimi_view(_kimi_runs(entries, payload, root, env))
        seen[name] = _seen(env)
    assert views["new"] == views["old"], case
    assert seen["new"] == seen["old"], case
    ran = {row[0] for row in seen["new"]}
    if payload["hook_event_name"] == "PostToolUse":
        assert ran == {"tool.py"}, "the reads catch-all never runs after a Kimi tool call"
    assert (ran == set()) is (case == "a tool no route takes"), ran
    assert all(row[3] == "c1c22c25-6382-4e79-8f00-a1a45e3c8e77" and row[7] == "kimi_code" for row in seen["new"])


def test_the_merged_prompt_reads_as_the_separate_entries_did(stand_in, tmp_path, monkeypatch):
    root, _old, new = stand_in
    env = _fresh_state(tmp_path, monkeypatch, "new")
    [done] = _kimi_runs(new, _prompt("go on"), root, env)
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout) == {
        "message": "[alpha] saw go on\n\n[beta] saw go on\n\n[Probe] delivered after UserPromptSubmit"
    }


def test_parity_a_typed_switch_reaches_the_switch_alone_and_quiet(stand_in, tmp_path, monkeypatch):
    root, old, new = stand_in
    turn = _turn(args="on")
    turn["session_id"] = _KIMI_SID
    seen = {}
    for name, entries in (("old", old), ("new", new)):
        env = _fresh_state(tmp_path, monkeypatch, name)
        assert _kimi_view(_kimi_runs(entries, turn, root, env)) == {"block": None, "context": ""}
        seen[name] = _seen(env)
    assert seen["new"] == seen["old"] == [
        ["tracking_guard.py", [], "UserPromptSubmit", "c1c22c25-6382-4e79-8f00-a1a45e3c8e77", "/probe on", "1",
         None, "kimi_code"],
    ]


def test_the_old_per_script_mode_is_unchanged(stand_in, tmp_path, monkeypatch):
    """`harness_io.py <script> [args]`: that one script, on the payload in
    Claude's shape, its own output translated; no dispatcher in between."""
    root, old, _new = stand_in
    env = _fresh_state(tmp_path, monkeypatch, "old")
    [entry] = [e for e in old if e["command"].endswith(" note.py alpha'")]
    done = _kimi(entry, _prompt("go on"), root, env)
    assert (done.returncode, json.loads(done.stdout)) == (0, {"message": "[alpha] saw go on"}), done.stderr
    assert _seen(env) == [["note.py", ["alpha"], "UserPromptSubmit", "c1c22c25-6382-4e79-8f00-a1a45e3c8e77",
                           "go on", None, None, "kimi_code"]]
    [veto] = [e for e in old if e["command"].endswith(" veto.py'")]
    done = _kimi(veto, _prompt("veto"), root, env)
    assert (done.returncode, done.stderr) == (2, "vetoed by Probe\n")


def test_a_half_installed_copy_never_vetoes(stand_in, tmp_path, monkeypatch):
    """No dispatcher beside the adapter (mid-update): the entry runs nothing."""
    root, _old, new = stand_in
    (root / "hooks" / "dispatch.py").unlink()
    env = _fresh_state(tmp_path, monkeypatch, "new")
    for payload in (_prompt("please veto this"), _tool("PreToolUse", "Bash", {"command": "rm -rf /"})):
        [done] = _kimi_runs(new, payload, root, env)
        assert (done.returncode, done.stdout) == (0, ""), done.stderr
    assert _seen(env) == []


@pytest.fixture()
def warm_host(stand_in):
    """The stand-in plugin's warm host (`zygote.py`), as the Probe service runs it."""
    root = stand_in[0]
    sys.path.insert(0, str(root / "hooks"))
    try:
        path = _load("_test_kimi_host_dispatch", root / "hooks" / "dispatch.py").host_socket(str(root))
    finally:
        sys.path.pop(0)
    proc = subprocess.Popen([sys.executable, "-S", str(root / "hooks" / "zygote.py"), path, str(os.getpid())],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    deadline = time.monotonic() + 10
    while not os.path.exists(path):
        assert time.monotonic() < deadline and proc.poll() is None, "the host never listened"
        time.sleep(0.02)
    yield stand_in
    proc.kill()
    proc.wait()
    for leftover in (path, path[: -len(".sock")] + ".key"):  # its socket and its key (#3355)
        if os.path.lexists(leftover):
            os.unlink(leftover)


@pytest.mark.parametrize("case", ["a prompt, several routes", "a refused tool call", "a prompt a route vetoes"])
def test_a_kimi_event_runs_in_the_warm_host_and_reads_the_same(warm_host, tmp_path, monkeypatch, case):
    """The point of D19: Kimi's events reach the service's warm host. What Kimi
    reads is what the event run here gives it."""
    root, _old, new = warm_host
    payload = _CASES[case]
    views, seen = {}, {}
    for name, host in (("here", "off"), ("hosted", "")):
        env = {**_fresh_state(tmp_path, monkeypatch, name), "PROBE_HOOK_HOST": host}
        views[name] = _kimi_view(_kimi_runs(new, payload, root, env))
        seen[name] = _seen(env)
    assert views["hosted"] == views["here"]
    assert seen["hosted"] and {row[6] for row in seen["hosted"]} == {"1"}, "every route ran in the host"
    assert [row[:6] for row in seen["hosted"]] == [row[:6] for row in seen["here"]]


def test_the_adapter_and_the_dispatcher_spell_unshown_alike():
    dispatch = _load("_test_kimi_unshown_dispatch", HOOKS / "dispatch.py")
    assert _io().UNSHOWN_FLAG == dispatch.UNSHOWN
    assert all(e in kimi_hooks.TOOL_EVENTS for e in kimi_hooks.UNSHOWN)


# An update reaches an open Kimi session (plan C3). Kimi keeps the folder a
# session started with ($KIMI_PLUGIN_ROOT) and its entries run that folder's
# adapter; Probe installs each version into a folder of its own beside it. The
# adapter hands each event to the copy Kimi's plugin list records
# (`harness_io.hand_over`, `dispatch.kimi_installed_root`), and an entry whose
# folder is gone runs the newest installed one instead of nothing.

_SAYS = textwrap.dedent("""
    import json, os, sys
    sys.stdin.read()
    with open(os.path.join(os.environ["XDG_STATE_HOME"], "ran.jsonl"), "a") as fh:
        fh.write(json.dumps([sys.argv[1], os.environ.get("CLAUDE_PLUGIN_ROOT"), os.environ.get("KIMI_PLUGIN_ROOT"),
                             os.environ.get("PROBE_HOOKS_HANDED_OVER")]) + "\\n")
""")


def _kimi_copy(kimi: Path, plugin: str, version: str) -> Path:
    """A version folder of a tracking plugin as Probe installs it into Kimi
    (`kimi_config.versioned_dir`): the real adapter and dispatcher, Kimi's
    manifest, and one Stop route that says which copy ran it."""
    root = kimi / "plugins" / "managed" / f"{plugin}@{version}"
    hooks = root / "hooks"
    hooks.mkdir(parents=True)
    for name in _COPIED:
        shutil.copy2(HOOKS / name, hooks / name)
    (hooks / "says.py").write_text(_SAYS)
    dispatch = _load(f"_test_kimi_copy_dispatch_{plugin}_{version}", hooks / "dispatch.py")
    command = dispatch._plain_command([], "says.py", True, [version.replace(".", "-")])
    (hooks / "routes.json").write_text(json.dumps({"hooks": {"Stop": [{"lane": "stop", "hooks": [
        {"type": "command", "command": command, "timeout": 5}]}]}}))
    (root / ".kimi-plugin").mkdir()
    (root / ".kimi-plugin" / "plugin.json").write_text(json.dumps({"name": plugin, "version": version}))
    return root


def _kimi_records(kimi: Path, *records: "tuple[str, Path]") -> None:
    path = kimi / "plugins" / "installed.json"
    path.write_text(json.dumps({"version": 1, "plugins": [
        {"id": plugin, "root": str(root), "source": "local-path", "enabled": True} for plugin, root in records
    ]}, indent=2))


def _stop(root: Path, env: dict) -> "tuple[subprocess.CompletedProcess, list]":
    """The Stop entry of the session's own manifest (rendered from its folder),
    run as Kimi runs it, from that folder."""
    [entry] = [e for e in kimi_hooks.render_hooks(root, True) if e["event"] == "Stop"]
    done = _kimi(entry, _payload("Stop", stop_hook_active=False), root, env)
    path = Path(env["XDG_STATE_HOME"]) / "ran.jsonl"
    return done, [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


@pytest.mark.parametrize("plugin", ["probe-research", "probe-research-daemon"])
def test_an_open_kimi_session_runs_the_installed_copys_hooks(isolated, tmp_path, monkeypatch, plugin):
    kimi = Path(os.environ["KIMI_CODE_HOME"])
    old, new = _kimi_copy(kimi, plugin, "0.171.0"), _kimi_copy(kimi, plugin, "0.172.0")
    _kimi_records(kimi, ("probe-research-tap", kimi / "plugins" / "managed" / "probe-research-tap@0.10.18"),
                  (plugin, new))
    done, ran = _stop(old, _fresh_state(tmp_path, monkeypatch, "s"))
    assert done.returncode == 0, done.stderr
    # The installed copy's routes, given its own folder; the hand-over marker
    # never reaches a route.
    assert ran == [["0-172-0", str(new), str(new), None]]


def test_a_rolled_back_kimi_plugin_stops_running_in_open_sessions_too(isolated, tmp_path, monkeypatch):
    kimi = Path(os.environ["KIMI_CODE_HOME"])
    old, new = _kimi_copy(kimi, "probe-research", "0.171.0"), _kimi_copy(kimi, "probe-research", "0.172.0")
    _kimi_records(kimi, ("probe-research", old))
    _done, ran = _stop(new, _fresh_state(tmp_path, monkeypatch, "s"))
    assert [row[:2] for row in ran] == [["0-171-0", str(old)]]


@pytest.mark.parametrize("case", ["records-this-copy", "no-list", "two-records", "another-plugins-folder",
                                  "recorded-outside-managed", "no-adapter-there", "routes-broken-there",
                                  "no-manifest-there", "already-handed"])
def test_otherwise_a_kimi_event_runs_in_the_sessions_own_copy(isolated, tmp_path, monkeypatch, case):
    kimi = Path(os.environ["KIMI_CODE_HOME"])
    old, new = _kimi_copy(kimi, "probe-research", "0.171.0"), _kimi_copy(kimi, "probe-research", "0.172.0")
    env = _fresh_state(tmp_path, monkeypatch, "s")
    if case == "records-this-copy":
        _kimi_records(kimi, ("probe-research", old))
    elif case == "two-records":
        _kimi_records(kimi, ("probe-research", new), ("probe-research", old))
    elif case == "another-plugins-folder":
        _kimi_records(kimi, ("probe-research-daemon", _kimi_copy(kimi, "probe-research-daemon", "0.172.0")))
    elif case == "recorded-outside-managed":
        _kimi_records(kimi, ("probe-research", shutil.copytree(new, tmp_path / "elsewhere" / new.name)))
    elif case == "no-adapter-there":
        _kimi_records(kimi, ("probe-research", new))
        (new / "hooks" / "harness_io.py").unlink()
    elif case == "routes-broken-there":
        _kimi_records(kimi, ("probe-research", new))
        (new / "hooks" / "routes.json").write_text("{broken")
    elif case == "no-manifest-there":
        _kimi_records(kimi, ("probe-research", new))
        shutil.rmtree(new / ".kimi-plugin")
    elif case == "already-handed":
        _kimi_records(kimi, ("probe-research", new))
        env["PROBE_HOOKS_HANDED_OVER"] = str(tmp_path / "the-copy-it-came-from")
    done, ran = _stop(old, env)
    assert done.returncode == 0, done.stderr
    assert ran == [["0-171-0", str(old), str(old), None]]


def test_a_kimi_session_on_a_pruned_version_runs_the_kept_one(isolated, tmp_path, monkeypatch):
    """A version folder older than a week becomes a link to the kept version
    (`kimi_config._prune_versions`): the session's entries still find their
    adapter, and the kept copy's routes run."""
    kimi = Path(os.environ["KIMI_CODE_HOME"])
    old, new = _kimi_copy(kimi, "probe-research", "0.171.0"), _kimi_copy(kimi, "probe-research", "0.172.0")
    _kimi_records(kimi, ("probe-research", new))
    [entry] = [e for e in kimi_hooks.render_hooks(old, True) if e["event"] == "Stop"]
    shutil.rmtree(old)
    old.symlink_to(new.name)
    env = _fresh_state(tmp_path, monkeypatch, "s")
    done = _kimi(entry, _payload("Stop", stop_hook_active=False), old, env)
    assert done.returncode == 0, done.stderr
    ran = [json.loads(line) for line in (Path(env["XDG_STATE_HOME"]) / "ran.jsonl").read_text().splitlines()]
    assert [row[0] for row in ran] == ["0-172-0"]


def test_a_kimi_session_whose_folder_is_gone_runs_the_newest_installed_copy(isolated, tmp_path, monkeypatch):
    """No folder where the session started (an uninstall and a reinstall, a
    prune that could make no link): the entry runs the newest-installed folder
    of the plugin beside it, instead of nothing."""
    kimi = Path(os.environ["KIMI_CODE_HOME"])
    old = _kimi_copy(kimi, "probe-research", "0.171.0")
    stale = _kimi_copy(kimi, "probe-research", "0.170.0")
    new = _kimi_copy(kimi, "probe-research", "0.172.0")
    os.utime(stale, (1, 1))
    _kimi_records(kimi, ("probe-research", new))
    [entry] = [e for e in kimi_hooks.render_hooks(old, True) if e["event"] == "Stop"]
    shutil.rmtree(old)
    env = _fresh_state(tmp_path, monkeypatch, "s")
    done = _kimi(entry, _payload("Stop", stop_hook_active=False), tmp_path, {**env, "KIMI_PLUGIN_ROOT": str(old)})
    assert done.returncode == 0, done.stderr
    ran = [json.loads(line) for line in (Path(env["XDG_STATE_HOME"]) / "ran.jsonl").read_text().splitlines()]
    assert [row[:2] for row in ran] == [["0-172-0", str(new)]]


def test_every_kimi_entry_finds_a_folder_when_its_own_is_gone():
    """Each rendered entry, of every plugin, falls back before its own check."""
    for rel in kimi_hooks.PLUGINS:
        for hook in json.loads((AGENT / rel / ".kimi-plugin" / "plugin.json").read_text())["hooks"]:
            command = hook["command"]
            own = re.search(r'\[ -[fx] "\$ROOT/hooks/([A-Za-z0-9_.-]+)" \] \|\| exit 0; ', command)
            assert own, command
            fallback = f'if [ ! -e "$ROOT/hooks/{own.group(1)}" ]; then '
            assert command.index("unset PLUGIN_ROOT") < command.index(fallback) < own.start(), command
            assert 'export KIMI_PLUGIN_ROOT="$ROOT"; fi; ' in command[command.index(fallback):own.start()]


def test_the_adapter_and_the_dispatcher_spell_the_hand_over_alike():
    dispatch = _load("_test_kimi_handed_over_dispatch", HOOKS / "dispatch.py")
    assert _io().HANDED_OVER == dispatch.HANDED_OVER
