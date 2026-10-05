"""Kimi Code's hooks: the rendered manifests, the payload/output adapter
(hooks/harness_io.py), the guard's view of Kimi's write tools, and how a
`probe` command finds the Kimi session that started it.

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
                 "CURSOR_TRACE_ID", "CLAUDE_CODE_SESSION_ID"):
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


def test_the_kimi_manifests_are_rendered_from_hooks_json():
    """A hook added to hooks.json and not to Kimi's manifest would silently
    never run under Kimi (it reads only its manifest)."""
    assert kimi_hooks.main(["--check"]) == 0


@pytest.mark.parametrize("rel", ["plugins/probe-research", "plugins/probe-research-daemon"])
def test_every_kimi_hook_matches_its_hooks_json_twin(rel):
    manifest = json.loads((AGENT / rel / ".kimi-plugin" / "plugin.json").read_text())
    source = json.loads((AGENT / rel / "hooks" / "hooks.json").read_text())["hooks"]
    twins = [
        (event, group.get("matcher"), hook)
        for event, groups in source.items()
        for group in groups
        for hook in group["hooks"]
        if (event, kimi_hooks._SCRIPT.findall(hook["command"])[-1][0]) not in kimi_hooks.SKIPPED
    ]
    assert len(manifest["hooks"]) == len(twins)
    for entry, (event, matcher, hook) in zip(manifest["hooks"], twins):
        # Kimi's schema is strict: exactly these keys.
        assert set(entry) <= {"event", "matcher", "command", "timeout"}
        assert entry["event"] == event
        assert entry.get("matcher") == matcher
        assert entry.get("timeout") == hook.get("timeout")
        script = kimi_hooks._SCRIPT.findall(hook["command"])[-1][0]
        assert f'harness_io.py" {script}' in entry["command"]
        # Parsed apart from the renderer's own regex: the words after the
        # script (telemetry's event) and every PROBE_* export must survive.
        tail = hook["command"].rsplit(f"hooks/{script}", 1)[1].split("'")[0].lstrip('"')
        assert entry["command"].rsplit(f"{script}", 1)[1].startswith(tail)
        for export in re.findall(r"export (PROBE_[A-Z_]+=[a-z_]+)", hook["command"]):
            if export not in ("PROBE_AGENT=codex", "PROBE_TAP_SOURCE=codex"):
                assert export in entry["command"], export
        assert "export PROBE_AGENT=kimi_code" in entry["command"]
        assert ("PROBE_PLUGIN_PROFILE=daemon" in entry["command"]) == (
            "PROBE_PLUGIN_PROFILE=daemon" in hook["command"]
        )


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
    {"CURSOR_TRACE_ID": "a" * 32},  # Kimi in Cursor's terminal
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


@pytest.mark.parametrize("rel", ["plugins/probe-research", "plugins/probe-research-daemon"])
def test_telemetry_keeps_its_positional_event_argument(rel):
    """telemetry.py dispatches on `post-tool` / `session-end`; without it, it
    does nothing."""
    manifest = json.loads((AGENT / rel / ".kimi-plugin" / "plugin.json").read_text())
    commands = [h["command"] for h in manifest["hooks"] if "telemetry.py" in h["command"]]
    assert any(c.endswith("telemetry.py post-tool'") for c in commands)
    assert any(c.endswith("telemetry.py session-end'") for c in commands)


@pytest.mark.parametrize("rel", ["plugins/probe-research", "plugins/probe-research-daemon"])
def test_no_kimi_post_tool_hook_claims_a_daemon_message(rel):
    """reads_hook claims a mailbox message before printing it, and Kimi drops
    PostToolUse output: the answer would vanish. It is delivered on the next
    prompt instead."""
    manifest = json.loads((AGENT / rel / ".kimi-plugin" / "plugin.json").read_text())
    post = [h["command"] for h in manifest["hooks"] if h["event"] == "PostToolUse"]
    assert post and not any("reads_hook.py" in c for c in post)
    prompt = [h["command"] for h in manifest["hooks"] if h["event"] == "UserPromptSubmit"]
    assert any("reads_hook.py" in c for c in prompt)


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
