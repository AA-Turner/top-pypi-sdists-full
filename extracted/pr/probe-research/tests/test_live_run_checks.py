"""The live run's verdicts, offline: `checks()` and `report()` over a run's
records, the session stand-in, and the probe shim (`tests/live/`).

A live run lasts hours; what it concludes from its records must not. Each
test here builds the records a run leaves (sessions' status, line and hook
logs, the stub's batches, the driver's samples) and asks the driver what it
makes of them: a session that failed must fail the run, a Windows build that
falls back to `tap watch` must fail `--expect-hosted`, a hook event a plugin
declares and the run never fired must fail coverage, and a `probe` call that
met the service's (machine-keyed) update barrier must be seen to.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import time
from pathlib import Path

import pytest

from probe.service import paths as service_paths

LIVE = Path(__file__).resolve().parent / "live"
MAIN, TAP = "probe-research@research-os-agent", "probe-research-tap@research-os-agent"
#: The events each plugin's hooks.json declares, as the stand-in loads them.
MANIFESTS = {
    MAIN: ["PostToolUse", "PreCompact", "PreToolUse", "SessionEnd", "SessionStart", "Stop", "UserPromptSubmit"],
    TAP: ["SessionEnd", "SessionStart", "Stop", "UserPromptSubmit"],
}


def _load(name: str, file: str):
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, LIVE / file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module  # before exec: its dataclasses look themselves up there
        spec.loader.exec_module(module)
    return sys.modules[name]


@pytest.fixture
def live_run():
    return _load("_live_run_checks", "live_run.py")


class _Ended:
    """A session agent's process, already exited with `code`."""

    def __init__(self, code: int | None) -> None:
        self.returncode = code
        self.pid = 4242

    def poll(self):
        return self.returncode


@pytest.fixture
def run(live_run, tmp_path, monkeypatch):
    r = live_run.Run(live_run.parse_args(["--root", str(tmp_path / "root"), "--no-canary-route"]))
    r.layout.make()
    r.state = live_run.StubState(r.layout, {})
    r.t_sessions = time.time() - 60
    # What the end of a good run reads: the last versions installed, the service idle.
    monkeypatch.setattr(r, "cli_version", lambda via_shim=True: r.versions.cli[2])
    ledger = {"plugins": {MAIN: [{"version": r.versions.plugin[2]}], TAP: [{"version": r.versions.tap[2]}]}}
    path = r.layout.claude / "plugins" / "installed_plugins.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger))
    r.final_missing = {}
    r.samples.append({"t": time.time(), "min": 1.0, "service": {"service_version": r.versions.cli[2]},
                      "update": None, "sessions": {}})
    yield r
    for handle in (r.state.requests_log, r.state.batches_log):
        handle.close()


def _session(run, label: str, *, exit_code: int | None = 0, phase: str = "ended", lines: int = 2,
             finalized: bool = True, events: dict | None = None, hook_exit: dict | None = None):
    """A session's records as the stand-in and the stub leave them."""
    info = run.new_session(label, False)
    info.process = _Ended(exit_code)
    info.exit_code = exit_code
    manifests = MANIFESTS if events is None else events
    info.status_file.write_text(json.dumps({
        "label": label, "sid": info.sid, "phase": phase, "lines": lines, "turns": 1 if lines else 0,
        "plugins": [{"id": pid, "root": f"/plugins/{pid}", "version": "v", "events": evs}
                    for pid, evs in manifests.items()],
    }))
    with info.lines_log.open("w") as handle:
        for n in range(lines):
            handle.write(json.dumps({"n": n, "kind": "user", "marker": f"LIVE-RUN-MARK {label} L{n:06d}"}) + "\n")
    fired = MANIFESTS if events is None else events
    with info.hook_log.open("w") as handle:
        for pid, evs in fired.items():
            for event in evs:
                handle.write(json.dumps({"session": label, "event": event, "plugin": pid, "version": "v",
                                         "exit": (hook_exit or {}).get(event, 0), "timed_out": False,
                                         "duration_s": 0.1, "timeout_s": 10.0}) + "\n")
    if lines:
        run.state.streams[("claude_code", info.sid)] = {"stream": {}, "receipts": {}, "batches": [{
            "status": "accepted", "batch_seq": 0, "line_start": 0, "line_end": lines, "finalize": finalized,
            "markers": [f"{label}:{n}" for n in range(lines)], "t": time.time(),
        }]}
    return info


def _verdicts(run) -> dict:
    return {r["id"]: r for r in run.checks(service_exit_s=5.0)}


def test_a_healthy_run_reads_green(run):
    """The fixture itself: one good session, and every check passes or skips."""
    _session(run, "s1")
    verdicts = _verdicts(run)
    failed = {k: v["detail"] for k, v in verdicts.items() if v["status"] == "fail"}
    assert failed == {}
    assert run.report(list(verdicts.values()), time.time()) == 0


# -- 1. a failed session fails the run -------------------------------------------------------


def test_a_session_that_exited_1_at_startup_fails_the_run(run):
    """Codex R1 on #3305: it read as "0 written / 0 uploaded", its siblings
    satisfied the hook checks, the per-sample checks skipped it (never
    `running`), and the report said pass."""
    _session(run, "s1")
    _session(run, "s2", exit_code=1, phase="starting", lines=0, events={MAIN: ["SessionStart"]})
    verdicts = _verdicts(run)
    assert verdicts["sessions.ran"]["status"] == "fail"
    assert "s2" in verdicts["sessions.ran"]["detail"] and "s1" not in verdicts["sessions.ran"]["detail"]
    assert verdicts["recording.complete"]["status"] == "fail", "no finalized stream for s2"
    assert run.report(list(verdicts.values()), time.time()) == 1


@pytest.mark.parametrize("exit_code", [None, -9, 2])
def test_a_session_killed_or_still_running_or_failing_fails_the_run(run, exit_code):
    _session(run, "s1", exit_code=exit_code)
    assert _verdicts(run)["sessions.ran"]["status"] == "fail"


def test_a_session_that_wrote_nothing_is_no_evidence_of_recording(run):
    _session(run, "s1", lines=0)
    verdicts = _verdicts(run)
    assert verdicts["sessions.ran"]["status"] == "fail", "no workload"
    assert verdicts["recording.complete"]["status"] == "fail", "a session's stream must end finalized"


def test_an_unfinalized_stream_fails_even_when_every_line_arrived(run):
    _session(run, "s1", finalized=False)
    assert _verdicts(run)["recording.complete"]["status"] == "fail"


def test_a_final_upload_wait_that_timed_out_fails_a_check(run):
    _session(run, "s1")
    run.final_missing = {"s1": "1/2 unfinalized"}
    verdicts = _verdicts(run)
    assert verdicts["recording.final_uploads"]["status"] == "fail"
    assert "s1" in verdicts["recording.final_uploads"]["detail"]


def test_end_sessions_keeps_each_exit(run):
    info = _session(run, "s1")
    info.process = _Ended(3)
    info.process.wait = lambda timeout=None: 3
    run.end_sessions()
    assert info.exit_code == 3 and info.ended_at


# -- 3. Windows: --expect-hosted reads the service's recorders -----------------------------------


@pytest.mark.parametrize(("recorded", "verdict"), [(False, "fail"), (True, "pass")])
def test_windows_expect_hosted_is_judged_from_the_services_recorders(run, live_run, monkeypatch, recorded, verdict):
    """Codex R3 on #3305: on Windows the whole `recording.hosted` gate sat in the
    POSIX branch, so a build falling back to `tap watch` there passed it."""
    monkeypatch.setattr(live_run, "WINDOWS", True)
    run.args.expect_hosted = True
    run.service_ok = True
    _session(run, "s1")
    run.samples.append({"t": time.time(), "min": 2.0, "service": {"service_version": run.versions.cli[2]},
                        "update": None, "sessions": {"s1": {
                            "phase": "running", "lines": 2, "uploaded_lines": 2, "tap_alive": True,
                            "hosted": False, "recorded_by_service": recorded, "listed": True}}})
    assert _verdicts(run)["recording.hosted"]["status"] == verdict


@pytest.mark.parametrize(("row", "recorded"), [
    ({"alive": True, "recording": True}, True),
    # Codex R2 on 22154ffa0: the guard thread lives on in its retry wait after
    # the tap loop found the journal claimed (the session's own `tap watch`
    # records it): alive, and recording nothing.
    ({"alive": True, "recording": False}, False),
    ({"alive": True}, False),  # a tap that cannot say whether it holds the claim
])
def test_a_sample_says_whether_the_service_owns_a_sessions_recording(run, monkeypatch, row, recorded):
    info = _session(run, "s1")
    run.service_ok = True
    answers = {"STATUS": {"recorders": [{"sid": info.sid, **row}]}, "SESSION_LIST": {"sessions": []}}
    monkeypatch.setattr(run, "service_call", lambda name, params=None: answers.get(name))
    assert run.sample()["sessions"]["s1"]["recorded_by_service"] is recorded


# -- 4. every hook event a loaded manifest declares is exercised -------------------------------


def test_an_event_a_loaded_manifest_declares_and_the_run_never_fired_fails(run):
    """Codex R4 on #3305: the main plugin declares PreCompact, the stand-in never
    fired it, and the hardcoded expected set left it out."""
    fired = {MAIN: [e for e in MANIFESTS[MAIN] if e != "PreCompact"], TAP: MANIFESTS[TAP]}
    info = _session(run, "s1", events=fired)
    status = json.loads(info.status_file.read_text())
    for plugin in status["plugins"]:
        plugin["events"] = MANIFESTS[plugin["id"]]  # what it LOADED declares PreCompact
    info.status_file.write_text(json.dumps(status))
    verdict = _verdicts(run)["hooks.fired"]
    assert verdict["status"] == "fail"
    assert "PreCompact" in verdict["detail"] and "s1" in verdict["detail"]


def test_a_precompact_hook_that_exits_42_fails_the_run(run):
    _session(run, "s1", hook_exit={"PreCompact": 42})
    assert _verdicts(run)["hooks.ok"]["status"] == "fail"


@pytest.fixture
def agent_module():
    return _load("_live_session_agent", "session_agent.py")


def _agent(agent_module, tmp_path, **cfg):
    plugin = tmp_path / "plugin"
    (plugin / "hooks").mkdir(parents=True)
    events = ["PreCompact", "Stop", "UserPromptSubmit", "PreToolUse", "PostToolUse"]
    (plugin / "hooks" / "hooks.json").write_text(json.dumps({"hooks": {
        e: [{"hooks": [{"type": "command", "command": "exit 0", "timeout": 5}]}] for e in events}}))
    ledger = tmp_path / "claude" / "plugins" / "installed_plugins.json"
    ledger.parent.mkdir(parents=True)
    ledger.write_text(json.dumps({"plugins": {MAIN: [{"installPath": str(plugin), "version": "1"}]}}))
    work = tmp_path / "work"
    work.mkdir()
    base = {
        "label": "s1", "sid": "sid-1", "cwd": str(work), "transcript": str(tmp_path / "t" / "sid-1.jsonl"),
        "plugins": [MAIN], "claude_config_dir": str(tmp_path / "claude"), "env": dict(os.environ),
        "shell": ["/bin/sh", "-c"], "turn_every_s": 0, "line_gap_s": 0, "probe_tool_every": 1000,
        "stop_file": str(tmp_path / "stop"), "status_file": str(tmp_path / "status.json"),
        "hook_log": str(tmp_path / "hooks.jsonl"), "lines_log": str(tmp_path / "lines.jsonl"),
        "tool_log": str(tmp_path / "tools.jsonl"), "compact_file": str(tmp_path / "compact"),
    }
    return agent_module.Session({**base, **cfg})


def _fired(tmp_path) -> list[str]:
    return [json.loads(line)["event"] for line in (tmp_path / "hooks.jsonl").read_text().splitlines()]


@pytest.mark.skipif(os.name != "posix", reason="the stand-in's hooks run under /bin/sh here")
def test_the_stand_in_compacts_on_its_schedule_and_when_asked(agent_module, tmp_path):
    session = _agent(agent_module, tmp_path, compact_every=3)
    for _ in range(3):
        session.turn()
    assert _fired(tmp_path).count("PreCompact") == 2, "its second turn, then every third"
    (tmp_path / "compact").touch()  # the driver, after an update landed
    session.turn()
    assert _fired(tmp_path).count("PreCompact") == 3 and not (tmp_path / "compact").exists()


def test_the_stand_in_reports_the_events_each_loaded_manifest_declares(agent_module, tmp_path):
    session = _agent(agent_module, tmp_path)
    session._status()
    plugins = json.loads((tmp_path / "status.json").read_text())["plugins"]
    assert plugins[0]["events"] == ["PostToolUse", "PreCompact", "PreToolUse", "Stop", "UserPromptSubmit"]


# -- 2. the probe shim sees the machine-keyed update barrier ---------------------------------------


@pytest.mark.skipif(os.name != "posix", reason="the shim's real probe stand-in is a shell script")
@pytest.mark.parametrize("where", ["keyed", "legacy", "none"])
def test_the_shim_sees_the_services_update_barrier(where, tmp_path, monkeypatch):
    """Codex R2 on #3305: the shim looked for `service/update.barrier`, where only
    a service from before the machine key raises it; today's service raises
    `service/<machine key>/update.barrier`, so a call it held logged
    `barrier_at_start: false` and escaped `probe.barrier_budget`."""
    monkeypatch.setenv("HOME", str(tmp_path))
    if where != "none":
        barrier = service_paths.barrier_path() if where == "keyed" else service_paths.legacy_barrier_path()
        barrier.parent.mkdir(parents=True, exist_ok=True)
        barrier.touch()
    real = tmp_path / ".local" / "bin" / "probe"
    real.parent.mkdir(parents=True, exist_ok=True)
    real.write_text("#!/bin/sh\nexit 0\n")
    real.chmod(0o755)
    shim = _load(f"_live_probe_shim_{where}", "probe_shim.py")
    monkeypatch.setattr(sys, "argv", ["probe", "--version"])
    assert shim.main() == 0
    calls = [json.loads(line) for line in (tmp_path / ".live-run" / "probe-calls.jsonl").read_text().splitlines()]
    assert calls[-1]["barrier_at_start"] is (where != "none")


@pytest.mark.skipif(os.name == "nt", reason="the budget check skips on Windows")
def test_a_detached_background_call_at_the_barrier_is_no_budget_overrun(run):
    """Main live run 39936954062: two `notes sync --push-only` calls a hook had
    double-forked (parent: init) met the update barrier and took 15-16 s; no
    agent waited on them, yet they failed probe.barrier_budget. A call an agent
    waits on (any other parent) past the budget still fails it."""
    _session(run, "s1")
    calls = run.layout.live / "probe-calls.jsonl"
    calls.parent.mkdir(parents=True, exist_ok=True)
    detached = {"argv": ["notes", "sync", "--push-only"], "barrier_at_start": True, "ppid": 1,
                "duration_s": 16.3, "exit": 0}
    calls.write_text(json.dumps(detached) + "\n")
    assert _verdicts(run)["probe.barrier_budget"]["status"] == "pass"
    held = {"argv": ["notes", "sync", "--push-only"], "barrier_at_start": True, "ppid": 4242,
            "duration_s": 16.3, "exit": 0}
    calls.write_text(json.dumps(detached) + "\n" + json.dumps(held) + "\n")
    assert _verdicts(run)["probe.barrier_budget"]["status"] == "fail"


# -- a late session stopped at the deadline still does its work -----------------------------------


@pytest.mark.skipif(os.name != "posix", reason="the stand-in's hooks run under /bin/sh here")
def test_a_session_stopped_before_its_first_turn_still_runs_its_compaction_turn(agent_module, tmp_path):
    """Codex R1 on 22154ffa0: a late session started as the run ends (its update
    landed at the deadline) saw its stop before its 2nd turn, so it never fired
    PreCompact, and `hooks.fired` failed a healthy run."""
    session = _agent(agent_module, tmp_path, compact_every=10)
    (tmp_path / "stop").touch()
    assert session.run() == 0
    assert session.turns == 2 and _fired(tmp_path).count("PreCompact") == 1


@pytest.mark.skipif(os.name != "posix", reason="the stand-in's hooks run under /bin/sh here")
def test_an_update_landing_at_the_deadline_leaves_its_late_session_green(run, agent_module, tmp_path):
    """The whole path: the run's last update lands at its deadline, its late
    session starts and is told to stop at once; what it leaves passes."""
    info = run.new_session("n2", False)
    plugin = tmp_path / "late-plugin"
    (plugin / "hooks").mkdir(parents=True)
    (plugin / "hooks" / "hooks.json").write_text(json.dumps({"hooks": {
        e: [{"hooks": [{"type": "command", "command": "exit 0", "timeout": 5}]}] for e in MANIFESTS[MAIN]}}))
    ledger = tmp_path / "late-claude" / "plugins" / "installed_plugins.json"
    ledger.parent.mkdir(parents=True)
    ledger.write_text(json.dumps({"plugins": {MAIN: [{"installPath": str(plugin), "version": "1"}]}}))
    session = agent_module.Session({
        "label": info.label, "sid": info.sid, "cwd": str(info.cwd), "transcript": str(info.transcript),
        "plugins": [MAIN], "claude_config_dir": str(tmp_path / "late-claude"), "env": dict(os.environ),
        "shell": ["/bin/sh", "-c"], "turn_every_s": 20, "line_gap_s": 0, "probe_tool_every": 1000,
        "compact_every": 10, "compact_file": str(info.compact_file), "stop_file": str(info.stop_file),
        "status_file": str(info.status_file), "hook_log": str(info.hook_log), "lines_log": str(info.lines_log),
        "tool_log": str(info.tool_log),
    })
    info.stop_file.touch()  # end_sessions, right after start_late_session
    assert session.run() == 0
    info.process, info.exit_code = _Ended(0), 0
    written = json.loads(info.status_file.read_text())["lines"]
    run.state.streams[("claude_code", info.sid)] = {"stream": {}, "receipts": {}, "batches": [{
        "status": "accepted", "batch_seq": 0, "line_start": 0, "line_end": written, "finalize": True,
        "markers": [f"n2:{n}" for n in range(written)], "t": time.time(),
    }]}
    verdicts = _verdicts(run)
    assert verdicts["sessions.ran"]["status"] == "pass", verdicts["sessions.ran"]["detail"]
    assert verdicts["hooks.fired"]["status"] == "pass", verdicts["hooks.fired"]["detail"]
