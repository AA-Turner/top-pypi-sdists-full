"""The team-note audit, run by the daemon (`daemon/audit.py`; daemon-team-note-audit,
2026-10-11).

What it must do, and each test below holds one of these:

  * start at most ONCE per session, on the researcher's first prompt, never in a
    session a program drives (`claude -p`, `codex exec`), never while a failed
    audit on this machine backs off;
  * read due-ness off the TEAM's copy (it pulls first), and do nothing when the
    note is not due or another session on this machine holds the audit;
  * edit only its own COPY, asking nobody anything: a command that would be a
    question is refused, so is a `probe` write, the live note and the open web;
  * publish only a run that ENDED after a look, merging its copy into the live
    note (a teammate's paragraph synced in meanwhile stays; a conflict publishes
    nothing); a run cut short changes nothing;
  * hand its report to the main agent as one `[Probe]` message that a reader
    message cannot replace.

Same seams as test_daemon_reader.py: the model is Pydantic AI's FunctionModel,
nothing reaches a server, the chat log is a real file.
"""

from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path

import pytest

pytest.importorskip("pydantic_ai")
pytest.importorskip("pydantic_ai_harness")

from pydantic_ai.messages import ModelResponse, TextPart, ToolCallPart, ToolReturnPart  # noqa: E402
from pydantic_ai.models.function import AgentInfo, FunctionModel  # noqa: E402

from probe.cli import team_note_file as tnf  # noqa: E402
from probe.daemon import agent as agent_mod  # noqa: E402
from probe.daemon import approvals as appr  # noqa: E402
from probe.daemon import audit as audit_mod  # noqa: E402
from probe.daemon import lease, mailbox, precheck, tools  # noqa: E402
from probe.daemon import model as model_mod  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402

SID = "11111111-2222-3333-4444-555555555555"
OLD_NOTE = ("<!-- audited 2020-01-01 -->\n\n## research-os\n\n- the relay stalls under load (#856)\n"
            "- main needs a PR\n")
NEW_NOTE = "<!-- audited 2026-10-11 -->\n\n## research-os\n\n- main needs a PR\n"


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """No real config (so no real key), no MCP: nothing leaves the box."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.delenv("PROBE_DAEMON_KEY", raising=False)
    monkeypatch.delenv(model_mod.ENV_MODEL, raising=False)
    monkeypatch.delenv(model_mod.ENV_AUDIT_MODEL, raising=False)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    monkeypatch.setenv(mailbox.ENV_READS, "1")
    monkeypatch.delenv(worker_mod.ENV_MODE, raising=False)
    (tmp_path / "state" / "probe" / "sessions").mkdir(parents=True)
    (lease.sessions_dir() / f"{SID}.state").write_text("daemon")


def _line(obj: dict) -> str:
    return json.dumps(obj) + "\n"


def _worker(tmp_path: Path, *, entrypoint: str = "cli", prompt: bool = True, model=None):
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True, exist_ok=True)
    (work / "train.py").write_text("print('hi')\n")
    transcript = tmp_path / f"{SID}.jsonl"
    lines = _line({"type": "permission-mode", "permissionMode": "default", "entrypoint": entrypoint})
    if prompt:
        lines += _line({"type": "user", "message": {"content": "sweep C"}, "cwd": str(work),
                        "entrypoint": entrypoint})
        lines += _line({"type": "system", "subtype": "turn_duration", "durationMs": 5})
    transcript.write_text(lines)
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          model=model)
    w.read_new()
    return w


def _note(tmp_path: Path, text: str = OLD_NOTE) -> Path:
    path = tmp_path / "state" / "probe" / "team-note" / tnf.DOCUMENT_NAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class Auditor:
    """The audit's model: `steps` answer its calls in order (("tool", (name, args)),
    ("end", report), or a callable (messages, info) -> step), then it ends with
    final_result(report=end)."""

    def __init__(self, steps=(), end: str = "checked 1 claim; kept it") -> None:
        self.steps = list(steps)
        self.end = end
        self.results: list[str] = []

    def __call__(self, messages, info: AgentInfo) -> ModelResponse:
        if not info.output_tools:
            return ModelResponse(parts=[TextPart("SUMMARY")])
        for part in messages[-1].parts:
            if isinstance(part, ToolReturnPart):
                self.results.append(str(part.content))
        step = self.steps.pop(0) if self.steps else ("end", self.end)
        if callable(step):
            step = step(messages, info)
        kind, arg = step
        if kind == "tool":
            name, args = arg
            return ModelResponse(parts=[ToolCallPart(name, args)])
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {"report": arg})])


LOOK = ("tool", ("shell", {"command": "ls", "why": "look"}))


def _write(path: Path, text: str) -> tuple:
    return ("tool", ("shell", {"command": f"cat > {path} <<'EOF'\n{text}EOF", "why": "the audit"}))


def _due():
    return tnf.audit_due(OLD_NOTE, pct=None, baseline=None)


class _Client:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _lane(w, auditor, monkeypatch, *, due=_due, pulled=True, publish=True) -> audit_mod.AuditLane:
    lane = audit_mod.AuditLane(w, model=FunctionModel(auditor) if isinstance(auditor, Auditor) else auditor)

    async def pull():
        lane._synced = (tnf.paths_for(None), None)  # the credential the pull used
        return pulled

    monkeypatch.setattr(lane, "_pull", pull)
    monkeypatch.setattr(lane, "_due", due)
    pushes: list[str] = []
    lane.pushes = pushes
    if publish:
        # The researcher's credential and the network, stood in for: reconcile is
        # what pushes; render_blocks writes the instruction files.
        monkeypatch.setattr(lane, "_client_and_paths", lambda: (_Client(), tnf.paths_for(None), None))

        def reconcile(client, where):
            pushes.append(where.document.read_text())
            return None, pushes[-1]

        monkeypatch.setattr(tnf, "reconcile", reconcile)
        monkeypatch.setattr(tnf, "render_blocks", lambda text, settings=None: None)
    return lane


def _reports() -> list[mailbox.Message]:
    return [m for _, m in mailbox.waiting(SID)]


# ---------------------------------------------------------------------------
# When it starts.
# ---------------------------------------------------------------------------


def test_it_starts_once_on_the_first_prompt(tmp_path, monkeypatch):
    started = []

    async def run(self):
        started.append(self)

    monkeypatch.setattr(audit_mod.AuditLane, "run", run)
    w = _worker(tmp_path, prompt=False)

    async def go():
        lane = audit_mod.AuditLane(w)
        assert lane.maybe_start() is False, "no prompt yet: no person seen"
        with w.session.transcript.open("a") as handle:
            handle.write(_line({"type": "user", "message": {"content": "go"}, "entrypoint": "cli"}))
        w.read_new()
        assert lane.maybe_start() is True
        assert lane.maybe_start() is False, "once per session"
        await lane.task
        # A respawned worker for the same session: the store remembers.
        assert audit_mod.AuditLane(w).maybe_start() is False

    asyncio.run(go())
    assert len(started) == 1


@pytest.mark.parametrize(
    ("head", "person"),
    [
        ({"type": "user", "entrypoint": "cli"}, True),
        ({"type": "user", "entrypoint": "vscode"}, True),
        ({"type": "user", "entrypoint": "sdk-cli"}, False),  # claude -p
        ({"type": "session_meta", "payload": {"originator": "codex_cli_rs"}}, True),
        ({"type": "session_meta", "payload": {"originator": "codex_exec"}}, False),  # codex exec
        ({"type": "session_meta", "payload": {"originator": "codex_cli_rs", "source": {"subagent": "review"}}}, False),
        ({"type": "session_meta", "payload": {"originator": "T3 Code", "source": "vscode"}}, True),  # T3's Codex
        ({"type": "session_meta", "payload": {"originator": "Codex Desktop", "source": "vscode"}}, True),
        # `codex exec` run from a T3 shell: the override it inherited names T3, its source does not
        ({"type": "session_meta", "payload": {"originator": "T3 Code", "source": "exec"}}, False),
        ({"type": "user"}, True),  # nothing said: a person (a deny-list, like the prompt hook's)
    ],
)
def test_a_session_a_program_drives_never_audits(tmp_path, head, person):
    transcript = tmp_path / "t.jsonl"
    transcript.write_text("not json\n" + _line(head))
    assert audit_mod.interactive(transcript) is person


def _t3_claude_head(*, hooks: int = 6, tools: tuple = ("mcp__t3-code__delegate_task",)) -> str:
    """A Claude Code session T3 Code started, in the shape t3 0.1.2 left on 2026-10-26:
    every line says `sdk-cli`, SessionStart hooks' lines first, then the tool list."""
    stamp = {"entrypoint": "sdk-cli", "userType": "external", "version": "2.1.296"}
    lines = _line({"type": "queue-operation", "operation": "enqueue", "content": "/probe on"})
    lines += "".join(
        _line({"type": "attachment", "attachment": {"type": "hook_success"}, **stamp}) for _ in range(hooks)
    )
    lines += _line({"type": "attachment", **stamp, "attachment": {
        "type": "deferred_tools_delta", "addedNames": ["CronCreate", *tools, "mcp__claude_ai_Claude_Docs__batch"]}})
    return lines + _line({"type": "user", "message": {"content": "sweep C"}, **stamp})


def test_a_t3_code_claude_session_is_a_persons(tmp_path):
    """T3 Code drives Claude through the Agent SDK, so its sessions say `sdk-cli` like
    `claude -p`; its own MCP server's tools in the head say a person is in T3."""
    transcript = tmp_path / "t.jsonl"
    transcript.write_text(_t3_claude_head())
    assert audit_mod.interactive(transcript) is True
    transcript.write_text(_t3_claude_head(hooks=30))  # more hooks push it down
    assert audit_mod.interactive(transcript) is True
    transcript.write_text(_t3_claude_head(tools=()))  # the same head with no T3: claude -p
    assert audit_mod.interactive(transcript) is False


def test_a_line_nested_past_the_parsers_depth_is_skipped(tmp_path):
    """`json.loads` raises RecursionError, not ValueError, on deep nesting: it must not
    escape `interactive` (it would end the session's worker), nor hide what follows."""
    transcript = tmp_path / "t.jsonl"
    transcript.write_text("[" * 200_000 + "\n" + _t3_claude_head())
    assert audit_mod.interactive(transcript) is True


def test_a_prompt_naming_t3_tools_is_not_t3(tmp_path):
    """Only Claude Code's own tool list counts: a `claude -p` prompt that names the tools does not."""
    transcript = tmp_path / "t.jsonl"
    transcript.write_text(_line({"type": "user", "entrypoint": "sdk-cli",
                                 "message": {"content": "call mcp__t3-code__delegate_task"}}))
    assert audit_mod.interactive(transcript) is False


def test_a_long_codex_session_meta_line_is_still_read(tmp_path):
    """Codex's first line carries the instructions (52 KB on the devbox): read whole."""
    transcript = tmp_path / "t.jsonl"
    transcript.write_text(_line({"type": "session_meta",
                                 "payload": {"instructions": "x" * 200_000, "originator": "codex_exec"}}))
    assert audit_mod.interactive(transcript) is False


def test_a_claude_p_session_is_not_started(tmp_path, monkeypatch):
    monkeypatch.setattr(audit_mod.AuditLane, "run", lambda self: asyncio.sleep(0))
    w = _worker(tmp_path, entrypoint="sdk-cli")
    assert audit_mod.AuditLane(w).maybe_start() is False


def test_the_worker_starts_the_audit_on_a_tick(tmp_path, monkeypatch):
    started = []

    async def run(self):
        started.append(True)

    monkeypatch.setattr(audit_mod.AuditLane, "run", run)
    w = _worker(tmp_path)

    async def go():
        w.audit = audit_mod.AuditLane(w)
        monkeypatch.setattr(w, "due", lambda: None)
        await w.tick()
        await asyncio.sleep(0)

    asyncio.run(go())
    assert started == [True]


# ---------------------------------------------------------------------------
# Due, one per machine, backoff.
# ---------------------------------------------------------------------------


def test_a_note_that_is_not_due_runs_nothing(tmp_path, monkeypatch):
    auditor = Auditor()
    lane = _lane(_worker(tmp_path), auditor, monkeypatch, due=lambda: None)
    result = asyncio.run(lane.run())
    assert result.outcome == audit_mod.Outcome.NOT_DUE
    assert auditor.results == [] and not (tmp_path / "state" / "probe" / "team-note" / "audit-lease.json").exists()


def test_a_failed_pull_runs_nothing(tmp_path, monkeypatch):
    lane = _lane(_worker(tmp_path), Auditor(), monkeypatch, pulled=False)
    assert asyncio.run(lane.run()).outcome == audit_mod.Outcome.PULL_FAILED


def test_another_sessions_audit_on_this_machine_holds_it(tmp_path, monkeypatch):
    _note(tmp_path)
    assert tnf.claim_audit_dispatch(holder="another-session") is True
    lane = _lane(_worker(tmp_path), Auditor(), monkeypatch)
    assert asyncio.run(lane.run()).outcome == audit_mod.Outcome.HELD


def test_due_ness_is_read_after_the_pull(tmp_path, monkeypatch):
    """The real `_due`: the local copy as the pull left it (a teammate's fresh stamp)."""
    w = _worker(tmp_path)
    lane = audit_mod.AuditLane(w, model=FunctionModel(Auditor()))
    note = _note(tmp_path)
    today = time.strftime("%Y-%m-%d")

    async def pull():
        note.write_text(f"<!-- audited {today} -->\nbody\n", encoding="utf-8")  # the team's copy
        return True

    monkeypatch.setattr(lane, "_pull", pull)
    assert asyncio.run(lane.run()).outcome == audit_mod.Outcome.NOT_DUE


def test_a_failed_audit_backs_the_machine_off(tmp_path, monkeypatch):
    audit_mod.back_off("failed: test")
    assert audit_mod.backing_off()
    assert not audit_mod.backing_off(now=time.time() + audit_mod.BACKOFF_S + 1)
    lane = _lane(_worker(tmp_path), Auditor(), monkeypatch)
    assert asyncio.run(lane.run()).outcome == audit_mod.Outcome.BACKING_OFF


# ---------------------------------------------------------------------------
# A run: edits its copy, asks nobody, publishes only when it ends.
# ---------------------------------------------------------------------------


def test_the_audit_edits_its_copy_and_publishes_with_no_question(tmp_path, monkeypatch):
    note = _note(tmp_path)
    w = _worker(tmp_path)
    w._renew()
    draft = audit_mod.AuditLane(w).draft
    auditor = Auditor([LOOK, _write(draft, NEW_NOTE)], end="Deleted the #856 line: the relay no longer stalls (ls).")
    lane = _lane(w, auditor, monkeypatch)
    result = asyncio.run(lane.run())
    assert result.outcome == audit_mod.Outcome.DONE and result.evidence == 1
    assert note.read_text(encoding="utf-8") == NEW_NOTE
    assert lane.pushes == [NEW_NOTE], "pushed once, the merged text"
    assert appr.Board().all(session_id=SID) == [], "nothing was asked"
    [msg] = _reports()
    assert msg.keep
    assert msg.text == agent_mod.AUDIT_REPORT_PREFIX + "Deleted the #856 line: the relay no longer stalls (ls)."
    assert not audit_mod.backing_off()


def test_a_teammates_paragraph_synced_in_during_the_audit_stays(tmp_path, monkeypatch):
    note = _note(tmp_path)
    w = _worker(tmp_path)
    w._renew()
    draft = audit_mod.AuditLane(w).draft
    teammate = OLD_NOTE + "- a teammate's new fact\n"

    def theirs(messages, info):
        note.write_text(teammate, encoding="utf-8")  # another session's Stop sync, mid-audit
        return LOOK

    lane = _lane(w, Auditor([theirs, _write(draft, NEW_NOTE)]), monkeypatch)
    assert asyncio.run(lane.run()).outcome == audit_mod.Outcome.DONE
    assert note.read_text(encoding="utf-8") == NEW_NOTE + "- a teammate's new fact\n"


def test_a_conflicting_change_during_the_audit_publishes_nothing(tmp_path, monkeypatch):
    note = _note(tmp_path)
    w = _worker(tmp_path)
    w._renew()
    draft = audit_mod.AuditLane(w).draft
    clashing = OLD_NOTE.replace("- the relay stalls under load (#856)", "- the relay stalls under load (#856, #863)")

    def theirs(messages, info):
        note.write_text(clashing, encoding="utf-8")
        return LOOK

    lane = _lane(w, Auditor([theirs, _write(draft, NEW_NOTE)], end="Deleted #856."), monkeypatch)
    asyncio.run(lane.run())
    assert note.read_text(encoding="utf-8") == clashing and lane.pushes == []
    [msg] = _reports()
    assert "Not published: the note changed during the audit" in msg.text
    assert audit_mod.backing_off()


def test_a_run_cut_short_after_writing_its_copy_changes_nothing(tmp_path, monkeypatch):
    """The session ends mid-run: the live note is as it was (no stamp-only publish)."""
    note = _note(tmp_path)
    w = _worker(tmp_path)
    w._renew()
    draft = audit_mod.AuditLane(w).draft
    steps = [LOOK, _write(draft, NEW_NOTE)]

    async def model(messages, info):
        if steps:
            _kind, (name, args) = steps.pop(0)
            return ModelResponse(parts=[ToolCallPart(name, args)])
        await asyncio.Event().wait()  # never answers: the session ends first

    lane = _lane(w, FunctionModel(model), monkeypatch)

    written = []

    async def go():
        lane.task = asyncio.ensure_future(lane.run())
        for _ in range(500):
            await asyncio.sleep(0.01)
            if draft.exists() and draft.read_text() == NEW_NOTE:
                written.append(True)
                break
        await lane.stop()
        assert lane.task is None

    asyncio.run(go())
    assert written, "the copy was written..."
    assert note.read_text(encoding="utf-8") == OLD_NOTE, "...the live note was not"
    assert lane.pushes == [] and _reports() == []
    assert not draft.parent.exists(), "the copy is removed"
    assert audit_mod.backing_off(), "a cut-short audit backs off"
    ends = [json.loads(line) for line in lane.trace.path.read_text().splitlines() if '"run_end"' in line]
    assert ends and ends[-1]["outcome"] == "stopped"


def test_a_write_before_any_look_is_refused_and_a_lookless_run_goes_again_on_the_writers_model(tmp_path, monkeypatch):
    note = _note(tmp_path)
    w = _worker(tmp_path)
    w._renew()
    draft = audit_mod.AuditLane(w).draft
    first = Auditor([_write(draft, NEW_NOTE)], end="nothing stale")
    lane = _lane(w, first, monkeypatch)
    names = []
    real = lane._model_for
    monkeypatch.setattr(lane, "_model_for", lambda name: (names.append(name), real(name))[1])
    result = asyncio.run(lane.run())
    assert first.results[0] == agent_mod.NO_EVIDENCE_YET
    assert note.read_text(encoding="utf-8") == OLD_NOTE, "nothing was published"
    assert names == [None, "default"], "one more go, on what the writer asks for"
    assert result.outcome == audit_mod.Outcome.NO_LOOK and _reports() == []
    assert audit_mod.backing_off()


def test_a_lookless_run_then_a_looking_rerun_publishes(tmp_path, monkeypatch):
    note = _note(tmp_path)
    w = _worker(tmp_path)
    w._renew()
    draft = audit_mod.AuditLane(w).draft
    auditor = Auditor([("end", "nothing stale"), LOOK, _write(draft, NEW_NOTE)], end="Deleted the #856 line.")
    lane = _lane(w, auditor, monkeypatch)
    assert asyncio.run(lane.run()).outcome == audit_mod.Outcome.DONE
    assert note.read_text(encoding="utf-8") == NEW_NOTE
    [msg] = _reports()
    assert msg.text == agent_mod.AUDIT_REPORT_PREFIX + "Deleted the #856 line."


def test_the_rerun_asks_for_the_writers_model_env_override_included(monkeypatch):
    monkeypatch.setenv(model_mod.ENV_MODEL, "claude-opus-5-5")
    assert audit_mod.AuditLane._writer_model() == "claude-opus-5-5"


def test_an_audit_out_of_rounds_is_stopped_and_publishes_nothing(tmp_path, monkeypatch):
    note = _note(tmp_path)
    w = _worker(tmp_path)
    w._renew()
    # Varied calls, so the loop detector does not trip first.
    steps = [("tool", ("read", {"path": str(tmp_path / "home" / "work" / "train.py"), "limit": n}))
             for n in range(1, agent_mod.AUDIT_ROUNDS + 6)]
    lane = _lane(w, Auditor(steps), monkeypatch)
    result = asyncio.run(lane.run())
    assert result.outcome == audit_mod.Outcome.STOPPED
    assert note.read_text(encoding="utf-8") == OLD_NOTE and _reports() == []


def test_an_unchanged_copy_is_not_published(tmp_path, monkeypatch):
    note = _note(tmp_path)
    w = _worker(tmp_path)
    w._renew()
    lane = _lane(w, Auditor([LOOK], end="nothing stale"), monkeypatch)
    asyncio.run(lane.run())
    assert note.read_text(encoding="utf-8") == OLD_NOTE and lane.pushes == []
    [msg] = _reports()
    assert "Not published" in msg.text and audit_mod.backing_off()


# ---------------------------------------------------------------------------
# The tools ask nothing, and write only the copy.
# ---------------------------------------------------------------------------


def _audit_deps(tmp_path, *, bypass=False, monkeypatch=None):
    w = _worker(tmp_path)
    w._renew()
    if bypass:
        monkeypatch.setattr(w, "permission", lambda: (True, True))
    lane = audit_mod.AuditLane(w)
    lane.draft.parent.mkdir(parents=True, exist_ok=True)
    return lane, lane._deps()


def test_a_command_that_would_be_a_question_is_refused_even_in_bypass(tmp_path, monkeypatch):
    _lane_, deps = _audit_deps(tmp_path, bypass=True, monkeypatch=monkeypatch)
    text = asyncio.run(tools.shell(deps, "curl -s https://example.com", "check"))
    assert text.startswith(tools.AUDIT_REFUSED), text
    assert appr.Board().all(session_id=SID) == []


def test_the_live_note_and_its_sync_state_are_not_written(tmp_path):
    note = _note(tmp_path)
    _lane_, deps = _audit_deps(tmp_path)
    for target in (note, note.parent / "health.json", note.parent / "audit-lease.json"):
        text = asyncio.run(tools.shell(deps, f"cat > {target} <<'EOF'\nx\nEOF", "write"))
        assert text.startswith(tools.AUDIT_REFUSED), (target, text)
    assert note.read_text(encoding="utf-8") == OLD_NOTE
    assert appr.Board().all(session_id=SID) == []


def test_the_copy_is_written_with_no_question(tmp_path):
    lane, deps = _audit_deps(tmp_path)
    text = asyncio.run(tools.shell(deps, f"cat > {lane.draft} <<'EOF'\n{NEW_NOTE}EOF", "write"))
    assert text.startswith("[exit 0"), text
    assert lane.draft.read_text() == NEW_NOTE and appr.Board().all(session_id=SID) == []


@pytest.mark.parametrize(
    ("argv", "runs"),
    [
        (["notes", "team"], True),
        (["run", "list"], True),
        (["notes", "sync"], False),  # the daemon's: under its key it would park the researcher's note
        (["notes", "sync", "--pull-only"], False),
        (["notes", "append", "--team", "x"], False),
        # The open web from the shell, refused as `find_papers` is (AUDIT_REFUSED_TOOLS).
        (["paper", "find", "why GRPO collapses"], False),
        (["paper", "find", "--mode", "read", "--paper-id", "arxiv:2610.02140"], False),
        (["paper", "list"], True),
        # Probe's docs: outside text, refused as `search_in=["docs"]` is.
        (["docs", "codex", "mcp", "install"], False),
        (["--base-url", "x", "docs", "codex"], False),
    ],
)
def test_the_probe_commands_it_may_run(argv, runs):
    parsed = precheck.parse(argv)
    assert (tools.audit_probe_refusal(parsed) is None) is runs


def test_the_open_web_from_the_shell_names_the_web_refusal():
    from probe.daemon.agent import AUDIT_REFUSED_TOOLS, AUDIT_WEB_REFUSED

    assert tools.audit_probe_refusal(precheck.parse(["paper", "find", "q"])) == AUDIT_WEB_REFUSED
    assert "find_papers" in AUDIT_REFUSED_TOOLS, "the shell door mirrors a refused MCP tool"


def test_notes_sync_names_who_does_it():
    assert tools.AUDIT_SYNC_IS_THE_DAEMONS in tools.audit_probe_refusal(precheck.parse(["notes", "sync"]))


@pytest.mark.parametrize(
    ("tool", "args", "look"),
    [
        ("read", {"path": "/repo/app/relay.py"}, True),
        ("read", {"path": "/home/x/.local/state/probe/team-note/health.json"}, False),
        ("read", {"path": "/home/x/.local/state/probe/audit/s/probe-team-note.md"}, False),
        ("shell", {"command": "git log --oneline -5"}, True),
        ("shell", {"command": "cd /repo && rg relay app/"}, True),
        ("shell", {"command": "head -50 app/relay.py"}, True),
        ("shell", {"command": "tail -n 20 CHANGELOG.md"}, True),
        ("shell", {"command": "wc -l app/relay.py"}, True),
        ("shell", {"command": "echo x | head"}, False),
        ("shell", {"command": "date -I"}, False),
        ("shell", {"command": "probe notes sync"}, False),
        ("shell", {"command": "cat ~/.local/state/probe/team-note/probe-team-note.md"}, False),
        # A repo folder whose name carries the words (the trial's own worktree) is still a look.
        ("shell", {"command": "cd ~/trees/research-os/daemon-team-note-audit && rg relay CHANGELOG.md"}, True),
        ("read", {"path": "/home/x/trees/research-os/daemon-team-note-audit/CLAUDE.md"}, True),
        ("probe__search", {"query": "relay"}, True),
    ],
)
def test_what_counts_as_a_look(tool, args, look):
    assert agent_mod.is_a_look(tool, args) is look


_DOCS_ONLY = json.dumps({"query": "codex mcp install", "search_in": ["docs"]})
_DOCS_AND_NOTES = json.dumps({"query": "relay", "search_in": ["docs", "notes"]})


@pytest.mark.parametrize(
    ("tool", "args", "look"),
    [
        # Probe's own docs are a product reference, not the team's record.
        ("search", {"query": "codex", "search_in": ["docs"]}, False),
        ("probe__search", {"query": "codex", "search_in": ["docs"]}, False),
        ("mcp__probe__search", {"query": "codex", "search_in": ["docs", "docs"]}, False),
        # A mixed search reads the team's record too; omitted or empty means every team corpus.
        ("probe__search", {"query": "relay", "search_in": ["docs", "notes"]}, True),
        ("probe__search", {"query": "relay", "search_in": []}, True),
        ("probe__search", {"query": "relay", "search_in": None}, True),
        ("probe__search", {"query": "relay", "search_in": "docs"}, True),
        # Only `search` takes `search_in`; a tool merely ending in those letters is not it.
        ("probe__entity", {"refs": ["team-note"], "search_in": ["docs"]}, True),
        ("probe__research", {"query": "x", "search_in": ["docs"]}, True),
        # The `bash` tool set reaches the same two doors from the shell.
        ("bash", {"command": 'probe docs "codex mcp install"'}, False),
        ("shell", {"command": "probe docs codex"}, False),
        ("bash", {"command": f"probe mcp call search '{_DOCS_ONLY}'"}, False),
        ("bash", {"command": f"probe mcp call search '{_DOCS_AND_NOTES}'"}, True),
        ("bash", {"command": """probe mcp call search '{"query": "relay"}'"""}, True),
        ("bash", {"command": "probe mcp call search 'not json'"}, True),
        ("bash", {"command": f"probe mcp call entity '{_DOCS_ONLY}'"}, True),
        # A docs read beside a real look is still a look.
        ("bash", {"command": "probe docs codex && git log -1"}, True),
        ("bash", {"command": "cd /repo && probe docs codex"}, False),
        # Root options before the command word, as click reads them.
        ("bash", {"command": "probe --base-url x docs install"}, False),
        ("bash", {"command": "probe docs install"}, False),
        ("bash", {"command": f"probe --base-url x mcp call search '{_DOCS_ONLY}'"}, False),
        ("bash", {"command": "probe --base-url x run list"}, True),
        ("bash", {"command": "probe run list"}, True),
    ],
)
def test_a_read_of_probes_own_docs_is_not_a_look(tool, args, look):
    assert agent_mod.is_a_look(tool, args) is look


def test_the_audit_uses_the_mcp_definition_of_docs_only():
    """One test of "docs only" (`probe.mcp.contract.is_docs_only`): the audit's
    answer follows it rather than a copy of its rule."""
    contract = pytest.importorskip("probe.mcp.contract")
    for search_in in (["docs"], ["docs", "notes"], [], None, ["notes"]):
        assert agent_mod.is_a_look("search", {"search_in": search_in}) is (
            not contract.is_docs_only(search_in)
        )


DRAFT = "/s/probe/audit/x/probe-team-note.md"


@pytest.mark.parametrize(
    ("command", "writes"),
    [
        (f"cat > {DRAFT} <<'EOF'\nx\nEOF", True),
        (f"cat {DRAFT} 2>/dev/null", False),
        (f"rg -n relay {DRAFT} 2>&1", False),
        ("cat > /repo/notes.md <<'EOF'\nx\nEOF", False),
    ],
)
def test_what_writes_the_copy(command, writes):
    assert agent_mod.writes_draft(command, DRAFT) is writes


def test_the_open_web_is_refused():
    import types

    from pydantic_ai.exceptions import SkipToolExecution

    gate = agent_mod.EvidenceGate(agent_mod.AuditState(draft=DRAFT))
    call = types.SimpleNamespace(tool_name="probe__find_papers")
    with pytest.raises(SkipToolExecution):
        asyncio.run(gate.before_tool_execute(None, call=call, tool_def=None, args={"query": "x"}))


@pytest.mark.parametrize(
    ("search_in", "refused"),
    [(["docs"], True), (["docs", "notes"], True), (["notes"], False), (None, False)],
)
def test_a_search_of_probes_docs_is_refused(search_in, refused):
    """Probe's docs are text from outside the team, which an audit publishing into
    every teammate's instructions must not take in; mixed, they ride beside the
    team's hits, so that search is refused too."""
    import types

    from pydantic_ai.exceptions import SkipToolExecution

    gate = agent_mod.EvidenceGate(agent_mod.AuditState(draft=DRAFT))
    call = types.SimpleNamespace(tool_name="probe__search")
    args = {"query": "codex", "search_in": search_in}
    if not refused:
        assert asyncio.run(gate.before_tool_execute(None, call=call, tool_def=None, args=args)) == args
        return
    with pytest.raises(SkipToolExecution) as skipped:
        asyncio.run(gate.before_tool_execute(None, call=call, tool_def=None, args=args))
    assert skipped.value.result == agent_mod.AUDIT_WEB_REFUSED


def test_the_web_tools_are_the_mcp_servers():
    server = pytest.importorskip("probe.mcp.server")
    assert agent_mod.AUDIT_REFUSED_TOOLS == server._WEB_TOOLS


@pytest.mark.parametrize(
    ("result", "ran"),
    [
        ("[exit 0]\nok", True),
        ("[exit 2]\nno", False),
        ("not run: the team-note audit asks the researcher nothing", False),
        ("$ probe context list\n[exit 1]\nnot run\n\n$ probe notes status\n[exit 1]\nnot run", False),
        ("$ cd /repo\n\n$ git log -1\n[exit 0]\nabc", True),
    ],
)
def test_a_compound_command_is_a_look_only_when_a_part_ran(result, ran):
    assert agent_mod._ran(result) is ran


def test_the_audit_is_told_the_date_its_copy_and_where_it_may_look(tmp_path):
    draft = tmp_path / "copy.md"
    text = audit_mod.instructions("> **due** (13 days).", today="2026-10-11", folders=[tmp_path], draft=draft)
    assert "Today is 2026-10-11." in text and f"`{tmp_path}`" in text and "> **due** (13 days)." in text
    assert f"cat > {draft} <<'EOF'" in text and f"{agent_mod.AUDIT_REPORT_CHARS:,} characters" in text
    assert "# Skill: audit-team-note" in text and "# Skill: edit-notes" in text
    for slot in ("today", "folders", "due", "draft", "report_chars"):
        assert "{" + slot + "}" not in text


def test_the_report_and_its_label_fit_the_mailbox():
    assert len(agent_mod.AUDIT_REPORT_PREFIX) + agent_mod.AUDIT_REPORT_CHARS <= mailbox.MESSAGE_MAX_CHARS


# ---------------------------------------------------------------------------
# The report, and the client lane.
# ---------------------------------------------------------------------------


def test_the_report_survives_a_later_reader_message(tmp_path):
    w = _worker(tmp_path)
    audit_mod.AuditLane(w).report("Deleted the #856 line.")
    mailbox.publish(mailbox.Message(id=mailbox.new_message_id(), session=SID, kind=mailbox.Kind.MESSAGE,
                                    text="a prior sweep exists", made_at=time.time() + 1, origin_turn=1))
    texts = [m.text for m in _reports()]
    assert agent_mod.AUDIT_REPORT_PREFIX + "Deleted the #856 line." in texts and "a prior sweep exists" in texts
    # ...and an ordinary unasked message still replaces an ordinary one.
    mailbox.publish(mailbox.Message(id=mailbox.new_message_id(), session=SID, kind=mailbox.Kind.MESSAGE,
                                    text="newer", made_at=time.time() + 2, origin_turn=1))
    texts = [m.text for m in _reports()]
    assert "a prior sweep exists" not in texts and "newer" in texts and len(texts) == 2


def test_the_audit_lane_sends_its_header_and_the_servers_alias(monkeypatch):
    ep = model_mod.Endpoint("https://api.example.test", "k")
    built = model_mod.build(ep, model_mod.LANE_AUDIT)
    assert built.client.default_headers[model_mod.LANE_HEADER] == "audit"  # DaemonLane.AUDIT
    assert built.model_name == "auditor"  # chat_router.AUDITOR_MODEL_ALIAS
    monkeypatch.setenv(model_mod.ENV_AUDIT_MODEL, "claude-haiku-5-5")
    assert model_mod.build(ep, model_mod.LANE_AUDIT).model_name == "claude-haiku-5-5"
    assert model_mod.build(ep, model_mod.LANE_AUDIT, name="default").model_name == "default"


def test_a_run_the_loop_detector_stopped_publishes_nothing(tmp_path, monkeypatch):
    """The skill saves the stamp first; three identical refusals (its own `probe
    notes sync`) trip the detector and the model ends: a stamp-only copy is never
    published."""
    note = _note(tmp_path)
    w = _worker(tmp_path)
    w._renew()
    draft = audit_mod.AuditLane(w).draft
    stamp_only = OLD_NOTE.replace("2020-01-01", "2026-10-11")
    sync = ("tool", ("shell", {"command": "probe notes sync", "why": "sync"}))
    lane = _lane(w, Auditor([LOOK, _write(draft, stamp_only), sync, sync, sync, sync], end="stamped"), monkeypatch)
    result = asyncio.run(lane.run())
    assert result.outcome == audit_mod.Outcome.STOPPED
    assert note.read_text(encoding="utf-8") == OLD_NOTE and lane.pushes == [] and _reports() == []


def test_trailing_newlines_do_not_make_a_conflict(tmp_path, monkeypatch):
    """A pulled note has no final newline (the brief is stripped); a heredoc always
    has one. A teammate's end-of-note append during the audit still merges."""
    note = _note(tmp_path, OLD_NOTE.rstrip("\n"))
    w = _worker(tmp_path)
    w._renew()
    draft = audit_mod.AuditLane(w).draft

    def theirs(messages, info):
        note.write_text(OLD_NOTE + "- appended by a teammate", encoding="utf-8")
        return LOOK

    lane = _lane(w, Auditor([theirs, _write(draft, OLD_NOTE.replace("2020-01-01", "2026-10-11"))]), monkeypatch)
    assert asyncio.run(lane.run()).outcome == audit_mod.Outcome.DONE
    text = note.read_text(encoding="utf-8")
    assert "2026-10-11" in text and "- appended by a teammate" in text and "<<<<<<<" not in text


def test_a_note_that_changed_hands_during_the_audit_is_not_written(tmp_path, monkeypatch):
    note = _note(tmp_path)
    w = _worker(tmp_path)
    w._renew()
    draft = audit_mod.AuditLane(w).draft
    where = tnf.paths_for(None)

    def switch(messages, info):
        where.stamp.write_text("another-credential", encoding="utf-8")
        return LOOK

    lane = _lane(w, Auditor([switch, _write(draft, NEW_NOTE)], end="done"), monkeypatch)
    asyncio.run(lane.run())
    assert note.read_text(encoding="utf-8") == OLD_NOTE and lane.pushes == []
    [msg] = _reports()
    assert "changed hands" in msg.text


def test_a_push_that_fails_after_the_merge_says_the_next_sync_sends_it(tmp_path, monkeypatch):
    note = _note(tmp_path)
    w = _worker(tmp_path)
    w._renew()
    draft = audit_mod.AuditLane(w).draft
    lane = _lane(w, Auditor([LOOK, _write(draft, NEW_NOTE)], end="Deleted #856."), monkeypatch)

    def offline(client, where):
        raise ConnectionError("offline")

    monkeypatch.setattr(tnf, "reconcile", offline)
    asyncio.run(lane.run())
    assert note.read_text(encoding="utf-8") == NEW_NOTE
    [msg] = _reports()
    assert "the next sync sends it" in msg.text and not audit_mod.backing_off()


def test_the_copy_is_private_and_carries_the_health_file(tmp_path):
    w = _worker(tmp_path)
    health = tnf.note_health_path()
    health.parent.mkdir(parents=True, exist_ok=True)
    health.write_text('{"sources": {}}', encoding="utf-8")
    lane = audit_mod.AuditLane(w)
    lane._write_draft(OLD_NOTE)
    assert (lane.draft.stat().st_mode & 0o777) == 0o600
    assert (lane.draft.parent.stat().st_mode & 0o777) == 0o700
    assert (lane.draft.parent / "health.json").read_text() == '{"sources": {}}'


def test_a_write_to_the_copy_spelled_from_home_is_still_a_write(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    draft = str(tmp_path / ".local/state/probe/audit/s/probe-team-note.md")
    for spelled in ("~", "$HOME", "${HOME}"):
        command = f"cat > {spelled}/.local/state/probe/audit/s/probe-team-note.md <<'EOF'\nx\nEOF"
        assert agent_mod.writes_draft(command, draft), spelled


def test_an_answer_does_not_withdraw_the_report(tmp_path):
    w = _worker(tmp_path)
    audit_mod.AuditLane(w).report("Deleted the #856 line.")
    mailbox.withdraw_unasked(SID, made_before=time.time() + 60)
    assert [m.text for m in _reports()] == [agent_mod.AUDIT_REPORT_PREFIX + "Deleted the #856 line."]


def test_the_daemon_claims_under_its_own_holder_name(tmp_path, monkeypatch):
    """A prompt hook asking for the same session (an older plugin) is a different
    claimant: it does not pass the lease the daemon holds."""
    _note(tmp_path)
    w = _worker(tmp_path)
    w._renew()
    lane = _lane(w, Auditor([LOOK], end="nothing stale"), monkeypatch)
    claims = []
    real = tnf.claim_audit_dispatch
    monkeypatch.setattr(tnf, "claim_audit_dispatch", lambda **kw: (claims.append(kw.get("holder")), real(**kw))[1])
    asyncio.run(lane.run())
    assert claims == [f"daemon:{SID}"]
    assert tnf.claim_audit_dispatch(holder=SID) is False
