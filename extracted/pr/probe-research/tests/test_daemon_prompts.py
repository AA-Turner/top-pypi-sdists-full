"""The daemon's prompt text is the researcher's approved text, word for word.

`fixtures/daemon_prompts/` holds verbatim copies of the approved files (the
researcher's review folder: one prompt per file, a header, then the prompt below
its closing `---`). Each test reads a body from there and finds it where the
daemon uses it: the job description, the tool descriptions, the compaction
prompt, the loop detector's stop, and the labels a bite shows (`{placeholders}`
are matched as any text). The review folder itself is never read here.
"""

from __future__ import annotations

import asyncio
import json
import re
import time
from pathlib import Path

import pytest

from probe.daemon import bite as bite_mod
from probe.daemon import lease
from probe.daemon import store as store_mod
from probe.daemon.events import Event, Kind

FIXTURES = Path(__file__).parent / "fixtures" / "daemon_prompts"
SID = "11111111-2222-3333-4444-555555555555"


def body(name: str) -> str:
    """The prompt of `name`: everything below the header's closing `---`."""
    lines = (FIXTURES / name).read_text(encoding="utf-8").split("\n")
    assert lines[0] == "---", name
    return "\n".join(lines[lines.index("---", 1) + 1:]).rstrip("\n")


def template(text: str) -> re.Pattern:
    """`text` as a pattern: each `{placeholder}` matches any text on its line."""
    parts = re.split(r"\{[^{}]+\}", text)
    return re.compile("[^\n]+?".join(re.escape(p) for p in parts))


def test_every_approved_file_is_used_here():
    used = {"job/record-session.PROPOSED.md", "tools/shell.PROPOSED.md", "tools/read.PROPOSED.md",
            "tools/session.NEW.md", "tools/edit.NEW.md", "tools/final_result.PROPOSED.md",
            "compaction/summary-prompt.PROPOSED.md", "compaction/earlier-turns.md",
            "compaction/landed-writes.NEW.md", "loop/loop-stop.PROPOSED.md",
            "loop/retries-spent.NEW.md", "bite/summary-outline.NEW.md",
            # the `bash` tool set: pinned in test_daemon_bash_tools.py
            "tools/bash-command-map.NEW.md", "tools/audit-command-map.NEW.md", "tools/draft-edit.NEW.md",
            "tools/bash-replies.NEW.md", "job/record-session-bash.NEW.md", "bite/bash-markers.NEW.md",
            # parallel calls and tasks: pinned in test_daemon_bash_tools.py
            "tools/parallel.NEW.md", "tools/task-command.NEW.md", "tools/task-instructions.NEW.md",
            "tools/task-command-map.NEW.md", "tools/task-replies.NEW.md", "tools/parallel-replies.NEW.md"}
    used |= {f"bite/{p.name}" for p in (FIXTURES / "bite").glob("*.PROPOSED.md")}
    # `reads/` (the daemon's reader) is pinned in test_daemon_reads_prompts.py.
    assert {str(p.relative_to(FIXTURES)) for p in FIXTURES.rglob("*.md") if p.relative_to(FIXTURES).parts[0] != "reads"} == used
    assert len(used) == 41


# ---------------------------------------------------------------------------
# The job description and the model-facing tool text.
# ---------------------------------------------------------------------------


def test_the_job_description_is_the_approved_text():
    """The approved file carries the skill front matter too (daemon reads, 09-28)."""
    approved = body("job/record-session.PROPOSED.md")
    shipped = (Path(bite_mod.__file__).parent / "record_session.md").read_text(encoding="utf-8")
    assert shipped.rstrip("\n") == approved
    assert shipped.startswith("---\nname: record-session\n"), "its skill front matter stays"
    assert bite_mod.record_session_text() == approved[approved.index("\n---", 3) + 4:].strip()


def test_the_instructions_carry_the_researchers_skills_verbatim():
    """What and how to record is track-work and edit-notes, word for word, after the job."""
    text = bite_mod.instructions_for("")
    assert text.startswith(bite_mod.record_session_text())
    at = 0
    from probe import skill_versions

    for name in bite_mod.SHARED_SKILLS:
        # The WRITER's version of each (track-work: its header, its commands with
        # the bash tool set, the base, its footer).
        skill = bite_mod.writer_skill(bite_mod.skills_root() / name)
        skill = skill_versions.split_front_matter(skill)[1].strip()
        assert f"# Skill: {name}\n\n{skill}" in text, name
        assert text.index(f"# Skill: {name}") > at, "in order, after the job"
        at = text.index(f"# Skill: {name}")


def _tools_seen() -> tuple[dict, list]:
    pytest.importorskip("pydantic_ai")
    from pydantic_ai.messages import ModelResponse, ToolCallPart
    from pydantic_ai.models.function import AgentInfo, FunctionModel

    from probe.daemon import agent as agent_mod

    seen: dict = {}

    def fn(messages, info: AgentInfo) -> ModelResponse:
        seen["tools"] = {t.name: t for t in info.function_tools}
        seen["output"] = list(info.output_tools)
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {"summary": "nothing new"})])

    agent = agent_mod.build_agent("instructions", model=FunctionModel(fn))
    asyncio.run(agent.run("go", deps=None))
    return seen["tools"], seen["output"]


def test_the_tool_descriptions_are_the_approved_text(monkeypatch):
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    tools, output = _tools_seen()
    assert tools["shell"].description == body("tools/shell.PROPOSED.md")
    assert tools["read"].description == body("tools/read.PROPOSED.md")
    assert tools["session"].description == body("tools/session.NEW.md")
    assert tools["edit"].description == body("tools/edit.NEW.md")
    for name in ("shell", "read", "session", "edit"):
        props = tools[name].parameters_json_schema["properties"]
        assert all("description" not in p for p in props.values()), f"{name}: no text but the approved"
    ends, fields = body("tools/final_result.PROPOSED.md").split("\n\nsummary: ")
    summary, reply = fields.split("\n\nreply: ")
    (final,) = output
    assert final.name == "final_result" and final.description == ends
    assert final.parameters_json_schema["properties"]["summary"]["description"] == summary
    assert final.parameters_json_schema["properties"]["reply"]["description"] == reply
    assert final.parameters_json_schema["required"] == ["summary"], "a run with no request needs no reply"


def test_the_compaction_prompt_and_the_loop_stop_are_the_approved_text():
    pytest.importorskip("pydantic_ai")
    from pydantic_ai.exceptions import SkipToolExecution

    from probe.daemon import agent as agent_mod

    assert agent_mod.SUMMARY_PROMPT == body("compaction/summary-prompt.PROPOSED.md")
    # The summary's own opening, by which the logbook block finds it, is the harness's.
    from pydantic_ai_harness.compaction import _summarizing_compaction as harness

    assert agent_mod.SUMMARY_HEAD == harness._SUMMARY_PREFIX
    assert agent_mod.EARLIER_TURNS == body("compaction/earlier-turns.md")
    detector = agent_mod.LoopDetector(tripped="the same `shell` call ran 5 times in one run")
    with pytest.raises(SkipToolExecution) as stopped:
        asyncio.run(detector.before_tool_execute(None, call=None, tool_def=None, args={}))
    assert stopped.value.result == body("loop/loop-stop.PROPOSED.md").replace("{why}", detector.tripped)
    assert agent_mod.RETRIES_SPENT == body("loop/retries-spent.NEW.md")


# ---------------------------------------------------------------------------
# The labels a bite shows.
# ---------------------------------------------------------------------------


def _store(tmp_path) -> store_mod.Store:
    return store_mod.Store(tmp_path / "s.sqlite", clock=time.time)


def test_the_summary_outline_lines_are_the_drafted_text():
    """ARTIFACT-PAGES P3 replaced the summary pin (its approved header went with
    it) by an outline per summary; its lines are NEW wording, pinned here until
    approved."""
    from probe.daemon import tools

    names = ("OUTLINE_HEADER", "OUTLINE_ENTITY", "OUTLINE_DRAFT", "OUTLINE_EDITED", "OUTLINE_NO_PAGE",
             "OUTLINE_HEADINGS", "OUTLINE_OPENS", "OUTLINE_SINCE", "OUTLINE_QUIET", "OUTLINE_DIRTY",
             "OUTLINE_MISSING")
    assert "\n".join(getattr(tools, n) for n in names) == body("bite/summary-outline.NEW.md")


def _logged(st: store_mod.Store, bite: int | None, argv: list[str], output: str = "", status: str = "ran") -> None:
    st.log_write(bite=bite, op_id="op", argv=argv, head=" ".join(argv[1:3]), status=status, output=output)


def test_the_landed_writes_block_is_the_logbook_in_the_approved_shape(tmp_path, monkeypatch):
    """Only `probe` writes that ran, newest first, one line per command, target
    and id; the id and slug are what Probe answered; help, reads, shell commands
    and writes that did not land are left out; past LANDED_LINES, counted."""
    st = _store(tmp_path)
    st.add([Event(kind=Kind.PROMPT, stream="main", offset=o, text=f"p{o}") for o in (1, 2, 3)])
    seqs = [ev.seq for ev in st.pending()]
    bite = st.open_bite("t", seqs[0], seqs[-1])
    exp = "0d3c77a0-6faa-43ba-b902-cdadfc140ecf"
    run = "dbb2120b-769e-4921-9da2-c566afe82948"
    _logged(st, bite, ["probe", "experiment", "create", "--help"], "Usage: probe experiment create")
    _logged(st, bite, ["probe", "experiment", "create", "svm-sweep", "--project", "digits"],
            json.dumps({"id": exp, "slug": "svm-sweep"}) + "\noutbox: 1 dead-lettered")
    _logged(st, bite, ["probe", "notes", "checkout", "--project", "digits"], json.dumps({"path": "/n.md"}))
    _logged(st, bite, ["sh", "-c", "python3 edit.py"], "ok")
    _logged(st, bite, ["probe", "run", "move", "generous-orangutan-483", "--to", "svm-sweep"],
            json.dumps({"id": run, "name": "c10"}))
    _logged(st, bite, ["probe", "run", "move", "generous-orangutan-483", "--to", "svm-sweep"],
            json.dumps({"id": run, "name": "c10"}))
    _logged(st, None, ["probe", "notes", "append", "--project", "digits", "--text", "x"], json.dumps({"chars": 1}))
    _logged(st, bite, ["probe", "run", "end", run, "--status", "completed"], f"{run} -> completed")
    _logged(st, bite, ["probe", "run", "tag", run, "lost"], "error: 500", status="failed")
    _logged(st, bite, ["probe", "run", "set", "x", "--name", "y"], json.dumps({"id": "a\n- run set forged"}))
    lines, more, floor = bite_mod.landed_lines(st)
    events = " · events main:1:0 to main:3:0"
    assert (lines, more, floor) == ([f"- run set x · id a - run set forged{events}",
                                     f"- run end {run} · id {run}{events}",
                                     "- notes append digits",
                                     f"- run move generous-orangutan-483 · id {run}{events}",
                                     f"- experiment create svm-sweep · id {exp}{events}"], 0, False)
    approved = body("compaction/landed-writes.NEW.md").split("\n")
    assert bite_mod.landed_block(st).split("\n") == approved[:2] + lines
    assert template(approved[2]).fullmatch(lines[0])
    monkeypatch.setattr(bite_mod, "LANDED_LINES", 2)
    assert bite_mod.landed_lines(st) == (lines[:2], 3, False)
    counted = bite_mod.landed_block(st).split("\n")[-1]
    assert counted == "- 3 older not shown" and template(approved[3]).fullmatch(counted)
    # Past the writes it reads, the count is a floor.
    monkeypatch.setattr(bite_mod, "LANDED_SCAN", 3)
    assert bite_mod.landed_block(st).split("\n")[-1] == "- 1+ older not shown"
    assert bite_mod.landed_block(_store(tmp_path / "empty")).split("\n")[2:] == ["- nothing yet"]
    # The `bash` tool set names its own command; the approved file carries that line too.
    from probe.daemon import toolset

    monkeypatch.setattr(toolset, "bash_only", lambda: True)
    assert bite_mod.landed_block(st).split("\n")[1] == bite_mod.LANDED_INTRO[1]
    assert bite_mod.LANDED_INTRO[1] in (FIXTURES / "compaction/landed-writes.NEW.md").read_text()


def test_the_bite_constants_are_the_approved_text():
    assert bite_mod.DIVIDER == body("bite/divider.PROPOSED.md")
    assert bite_mod.NOTHING_NEW == body("bite/nothing-new.PROPOSED.md")


def test_a_fresh_start_shows_the_approved_labels(tmp_path, monkeypatch):
    monkeypatch.setattr(bite_mod, "WINDOW_TOKENS", 50)
    monkeypatch.setattr(bite_mod, "STEP_TOKENS", 25)
    monkeypatch.setattr(bite_mod, "TEXT_SHOWN_CHARS", 300)
    st = _store(tmp_path)
    for turn in range(6):
        st.add([Event(kind=Kind.PROMPT, stream="main", offset=turn * 10, text=f"prompt {turn} " + "p" * 400),
                Event(kind=Kind.TOOL_OUTPUT, stream="main", offset=turn * 10 + 1, text="| a | b |\n|---|---|")])
    st.mark_covered(st.open_bite("t", None, None), st.pending()[-2].seq)
    built = bite_mod.build(st, trigger="t", context_line="", pending_lines=[], recent_writes=["ran: probe x"])
    prompt = built.prompt
    assert template(body("bite/cut-off-note.PROPOSED.md")).match(prompt), prompt[:300]
    assert body("bite/last-writes-heading.PROPOSED.md") in prompt
    assert template(body("bite/long-text-cut.PROPOSED.md")).search(prompt)
    assert body("bite/output-results-flag.PROPOSED.md") in prompt
    st2 = _store(tmp_path / "c")
    st2.add([Event(kind=Kind.PROMPT, stream="main", offset=1, text="one short prompt")])
    whole = bite_mod.build(st2, trigger="t", context_line="", pending_lines=[], recent_writes=[])
    assert whole.prompt.startswith(body("bite/whole-session-note.PROPOSED.md"))


def test_a_long_turn_cut_shows_the_approved_marker(tmp_path, monkeypatch):
    monkeypatch.setattr(bite_mod, "TURN_SHOWN_TOKENS", 500)
    st = _store(tmp_path)
    st.add([Event(kind=Kind.PROMPT, stream="main", offset=1, text="THE PROMPT")]
           + [Event(kind=Kind.AGENT_TEXT, stream="main", offset=10 + i, text=f"step {i} " + "x" * 300)
              for i in range(40)])
    st.mark_covered(st.open_bite("t", None, None), st.pending()[-1].seq)
    st.add([Event(kind=Kind.AGENT_TEXT, stream="main", offset=1000, text="NEW")])
    built = bite_mod.build(st, trigger="t", context_line="", pending_lines=[], recent_writes=[])
    assert template(body("bite/long-turn-cut.PROPOSED.md")).search(built.prompt), built.prompt[-2000:]


def test_notices_show_whole_and_apart_from_the_harness_lines(tmp_path):
    daemon_label, harness_label = body("bite/notice-label.PROPOSED.md").split(
        "      (a line from the coding agent's harness: ")
    harness_label = harness_label.rstrip(")")
    st = _store(tmp_path)
    long = "the researcher said yes to question q1; it ran:\n" + "o" * 900
    st.add([Event(kind=Kind.META, stream=bite_mod.NOTICE_STREAM, offset=1, text=long),
            Event(kind=Kind.META, stream="main", offset=2, text="<task-notification>done</task-notification>")])
    daemon_ev, harness_ev = st.events_between(1)
    shown = bite_mod.render(daemon_ev)
    assert template(daemon_label).match(shown) and shown.endswith(long), "whole, not 300 characters"
    assert template(harness_label).match(bite_mod.render(harness_ev))
    assert bite_mod.render(harness_ev).startswith("[harness · ")


def test_a_peer_agents_message_shows_who_sent_it_apart_from_the_harness_lines(tmp_path):
    """Plan probe-hints T4 moved a peer agent's sender out of the text (its
    wrapper) into `command`: the writer and the reader still see who sent it,
    in the approved label, as a preview counted like a harness line."""
    from probe.daemon.adapters.base import peer_message

    st = _store(tmp_path)
    st.add([peer_message("main", 1, text="p" * 1000, sender_from="uds:/tmp/cc-socks/11957.sock",
                         sender_name="Unconditional Generation")])
    (ev,) = st.events_between(1)
    shown = bite_mod.render(ev)
    assert template(body("bite/peer-message-label.PROPOSED.md")).match(shown), shown[:120]
    assert shown.startswith("[peer agent · Unconditional Generation (uds:/tmp/cc-socks/11957.sock) · ")
    assert f"session op=open event_id={ev.event_id}" in shown, "a preview, like a harness line"
    assert bite_mod.shown_chars(ev) == st.shown_turn_sizes()[0][2]


def test_a_harness_line_is_a_preview_and_the_store_counts_it_so(tmp_path):
    """A system reminder or skill body in the chat runs to 51K characters: a
    harness line shows HARNESS_SHOWN_CHARS and a pointer to the rest, and the
    window's size estimate (`Store.shown_turn_sizes`) counts the same."""
    st = _store(tmp_path)
    st.add([Event(kind=Kind.META, stream="main", offset=1, text="r" * 50_000)])
    (ev,) = st.events_between(1)
    shown = bite_mod.render(ev)
    assert len(shown) < bite_mod.HARNESS_SHOWN_CHARS + 200 and f"session op=open event_id={ev.event_id}" in shown
    assert bite_mod.shown_chars(ev) == bite_mod.HARNESS_SHOWN_CHARS + 40
    assert st.shown_turn_sizes()[0][2] == bite_mod.HARNESS_SHOWN_CHARS + 40


def test_missing_skills_are_logged_as_an_error(monkeypatch, caplog):
    monkeypatch.setattr(bite_mod, "skills_root", lambda: None)
    with caplog.at_level("ERROR", logger="probe.daemon"):
        assert bite_mod.skills_text() == ""
    assert "skills were not found" in caplog.text


# ---------------------------------------------------------------------------
# What the worker writes: the agent memory index, the stuck events, the status.
# ---------------------------------------------------------------------------


@pytest.fixture
def worker(tmp_path, monkeypatch):
    from probe.daemon import worker as worker_mod

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    monkeypatch.delenv(worker_mod.ENV_MODE, raising=False)
    (tmp_path / "state" / "probe" / "sessions").mkdir(parents=True)
    (lease.sessions_dir() / f"{SID}.state").write_text("daemon")
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True)
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(json.dumps({"type": "user", "message": {"content": "sweep C"}, "cwd": str(work)}) + "\n")
    return worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"))


def test_the_worker_writes_the_approved_lines(worker, tmp_path):
    index = tmp_path / "MEMORY.md"
    index.write_text("- [Sweeps](sweeps.md)\n")
    assert body("bite/agent-memory-index-framing.PROPOSED.md") in worker.memory_block([index])
    worker.store.set_fact("deferred_from", 7)
    assert any(template(body("bite/stuck-events-line.PROPOSED.md")).fullmatch(line)
               for line in worker.pending_lines())
    worker.store.set_fact("deferred_from", None)
    bite = worker.store.open_bite("t", None, None)
    worker.store.log_write(bite=bite, op_id="1", argv=["probe", "run", "tag", "r1", "svm"], head="run tag",
                           status="ran")
    worker.board.hold(policy="shell.unsafe_command", session_id=SID, facts={"command": "make", "cwd": "/w"},
                      held={"kind": "shell", "command": "make", "cwd": "/w", "op_id": "o"}, bypass=False)
    worker.read_new()
    state = worker.state_of_record()
    assert template(body("bite/state-of-the-record.PROPOSED.md")).fullmatch(state), state
    assert "- probe run tag r1 svm" in state and "is waiting for the researcher" in state


def test_a_changed_skill_starts_a_fresh_conversation(worker, monkeypatch):
    """A saved conversation carries the instructions it was made with, skills and all."""
    pytest.importorskip("pydantic_ai")  # the fingerprint holds its version
    before = worker._fingerprint()
    monkeypatch.setattr(bite_mod, "skills_text", lambda: "# Skill: track-work\n\nsomething else")
    assert worker._fingerprint() != before
