"""Daemon reads: the reader beside the writer (`reader_lane.py`), its approved
text, and the worker changes that came with it (handover, the finishing marker,
the lease kept alive through a long model call).

Same seams as test_daemon_conversation.py: the model is Pydantic AI's
FunctionModel, nothing reaches a server, the chat log is a real file.
"""

from __future__ import annotations

import asyncio
import json
import re
import threading
import time
from pathlib import Path

import pytest

pytest.importorskip("pydantic_ai")
pytest.importorskip("pydantic_ai_harness")

from pydantic_ai.messages import ModelResponse, RetryPromptPart, TextPart, ToolCallPart, UserPromptPart  # noqa: E402
from pydantic_ai.models.function import AgentInfo, FunctionModel  # noqa: E402

from probe.cli import daemon_cli  # noqa: E402
from probe.daemon import agent as agent_mod  # noqa: E402
from probe.daemon import lease, mailbox  # noqa: E402
from probe.daemon import reader_lane as rl  # noqa: E402
from probe.daemon import store as store_mod  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402

SID = "11111111-2222-3333-4444-555555555555"
FIXTURES = Path(__file__).parent / "fixtures" / "daemon_prompts" / "reads"


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """No real config (so no real key), no MCP: nothing leaves the box."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.delenv("PROBE_DAEMON_KEY", raising=False)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    monkeypatch.delenv(worker_mod.ENV_MODE, raising=False)
    monkeypatch.delenv(mailbox.ENV_READS, raising=False)
    (tmp_path / "state" / "probe" / "sessions").mkdir(parents=True)
    _set_state("daemon")


def _set_state(state: str) -> None:
    (lease.sessions_dir() / f"{SID}.state").write_text(state)


def _line(obj: dict) -> str:
    return json.dumps(obj) + "\n"


def _worker(tmp_path: Path, *, model=None, replay=None, clock=time.time):
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True, exist_ok=True)
    transcript = tmp_path / f"{SID}.jsonl"
    if not transcript.exists():
        transcript.write_text(
            _line({"type": "permission-mode", "permissionMode": "default"})
            + _line({"type": "user", "message": {"content": "sweep C for an SVM on digits"}, "cwd": str(work)})
            + _line({"type": "assistant", "message": {"content": [{"type": "text", "text": "SVM C=10: 0.9889."}]}})
            + _line({"type": "system", "subtype": "turn_duration", "durationMs": 5})
        )
    return worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                             clock=clock, replay=replay, model=model)


def _append_turn(w, prompt: str) -> None:
    with w.session.transcript.open("a") as handle:
        handle.write(_line({"type": "user", "message": {"content": prompt}}))
        handle.write(_line({"type": "system", "subtype": "turn_duration", "durationMs": 5}))


class Reader:
    """The reader's model: `steps` answer its calls in order, then it ends the turn
    with `final_result(message=end)`. A step is ("tool", (name, args)), ("say", text)
    (prose, no tool call), ("end", message) or a callable (messages, info) -> step."""

    def __init__(self, steps=(), end: str = "") -> None:
        self.steps = list(steps)
        self.end = end
        self.seen: list[tuple[list, AgentInfo]] = []

    def __call__(self, messages, info: AgentInfo) -> ModelResponse:
        if not info.output_tools:  # a compaction's summary request
            return ModelResponse(parts=[TextPart("SUMMARY")])
        self.seen.append((list(messages), info))
        step = self.steps.pop(0) if self.steps else ("end", self.end)
        if callable(step):
            step = step(messages, info)
        kind, arg = step
        if kind == "tool":
            name, args = arg
            return ModelResponse(parts=[ToolCallPart(name, args)])
        if kind == "say":
            return ModelResponse(parts=[TextPart(arg)])
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {"message": arg})])


def _text(messages) -> str:
    out = []
    for message in messages:
        for part in message.parts:
            if isinstance(part, RetryPromptPart):
                out.append(part.model_response())
                continue
            content = getattr(part, "content", None)
            if isinstance(content, str):
                out.append(content)
    return "\n".join(out)


def _prompt(message) -> str:
    """The user prompt part of a request (a turn's new message)."""
    return "\n".join(p.content for p in message.parts if isinstance(p, UserPromptPart))


def _lane(w, script) -> rl.ReaderLane:
    w.read_new()
    return rl.ReaderLane(w, model=FunctionModel(script))


def _waiting(kind=None) -> list[mailbox.Message]:
    return [m for _, m in mailbox.waiting(SID) if kind is None or m.kind == kind]


# ---------------------------------------------------------------------------
# The approved text (`~/daemon-prompts/reads/`, copied under fixtures/).
# ---------------------------------------------------------------------------


def body(name: str) -> str:
    lines = (FIXTURES / name).read_text(encoding="utf-8").split("\n")
    assert lines[0] == "---", name
    return "\n".join(lines[lines.index("---", 1) + 1:]).rstrip("\n")


def sections(name: str) -> dict[str, str]:
    """A file of `LABEL:` sections: {label: text}."""
    out: dict[str, str] = {}
    label = None
    for line in body(name).split("\n"):
        if (re.fullmatch(r"[A-Z][A-Z0-9 ,_\-.]*(\([^)]*\))?:", line)
                or re.fullmatch(r"(OPTION|ARGUMENT) [^:]+:", line)):
            label = line[:-1]
            out[label] = ""
        elif label is not None:
            out[label] += line + "\n"
    return {k: v.strip("\n") for k, v in out.items()}


def test_every_approved_reads_file_is_pinned_here():
    used = {"job/read-session.NEW.md", "tools/final_result.NEW.md", "tools/read.NEW.md", "tools/session.NEW.md",
            "conversation/ask-line.NEW.md", "conversation/divider.NEW.md",
            "conversation/memory-index-framing.NEW.md", "conversation/summary-prompt.NEW.md",
            "replies/message-too-long.NEW.md", "replies/turn-limit.NEW.md", "agent-facing/message.NEW.md",
            "agent-facing/ask-failed.NEW.md", "agent-facing/probe-ask.NEW.md",
            "researcher-facing/failure-messages.NEW.md",
            # pinned in test_skill_versions.py and test_daemon_profile.py
            "agent-facing/managed-block.PROPOSED.md",
            "agent-facing/guard-refusal.NEW.md",
            "skills/track-work/RENDERED.main-agent.md", "skills/track-work/RENDERED.writer.md"}
    assert {str(p.relative_to(FIXTURES)) for p in FIXTURES.rglob("*.md")} == used


def test_the_readers_job_is_the_approved_skill_file():
    shipped = (Path(rl.__file__).parent / "read_session.md").read_text(encoding="utf-8").rstrip("\n")
    assert shipped == body("job/read-session.NEW.md")
    assert shipped.startswith("---\nname: read-session\n"), "skill front matter, like record_session.md"
    assert rl.read_session_text() == shipped[shipped.index("\n---", 3) + 4:].strip()


def test_the_readers_tools_and_replies_are_the_approved_text():
    field = agent_mod.ReadResult.model_fields["message"].description
    assert f"{agent_mod.ReadResult.__doc__.strip()}\n\nmessage: {field}" == body("tools/final_result.NEW.md")
    assert agent_mod.READER_READ_DESCRIPTION == body("tools/read.NEW.md")
    assert agent_mod.READER_SESSION_DESCRIPTION == body("tools/session.NEW.md")
    assert agent_mod.READER_SUMMARY_PROMPT == body("conversation/summary-prompt.NEW.md")
    assert agent_mod.MESSAGE_TOO_LONG == body("replies/message-too-long.NEW.md")
    assert agent_mod.TURN_LIMIT == body("replies/turn-limit.NEW.md")
    assert rl.DIVIDER == body("conversation/divider.NEW.md")
    assert rl.ASK_LINE == body("conversation/ask-line.NEW.md")
    assert rl.MEMORY_FRAMING == body("conversation/memory-index-framing.NEW.md")


def test_what_the_main_agent_reads_is_the_approved_text():
    msg = sections("agent-facing/message.NEW.md")
    assert mailbox.TEXT_MESSAGE == msg["MESSAGE"]
    assert mailbox.TEXT_ANSWER == msg["ANSWER"]
    assert mailbox.TEXT_NOTHING == msg["NOTHING_FOUND"]
    assert mailbox.TEXT_FAILED == body("agent-facing/ask-failed.NEW.md")
    ask = sections("agent-facing/probe-ask.NEW.md")
    assert daemon_cli.ASK_HELP == ask["HELP"]
    assert daemon_cli.ASK_ARG_HELP == ask["ARGUMENT question"]
    assert daemon_cli.ASK_WAIT_HELP == ask["OPTION --wait"]
    assert ask["WAITED, ANSWER"] == "{message}"
    assert daemon_cli.ASK_NOTHING == ask["WAITED, NOTHING FOUND"]
    assert daemon_cli.ASK_STILL_LOOKING == ask["WAITED, STILL LOOKING (2 h passed)"]
    assert daemon_cli.ASK_FAILED == ask["WAITED, FAILED (exit 1)"]
    assert daemon_cli.ASK_ASKED == ask["ASKED"]
    assert daemon_cli.ASK_NO_WORKER == ask["ASKED, DAEMON NOT RUNNING"]
    assert daemon_cli.ASK_FINISHING == ask["ASKED, PREVIOUS SESSION STILL FINISHING"]
    assert daemon_cli.ASK_NO_DAEMON == ask["NOT ASKED, NO DAEMON ON THIS MACHINE"]
    assert daemon_cli.ASK_SESSION_OFF == ask["NOT ASKED, SESSION OFF"]
    assert daemon_cli.ASK_NO_SESSION == ask["NOT ASKED, NO SESSION"]
    assert daemon_cli.ASK_EMPTY == ask["NOT ASKED, EMPTY"]


def test_what_the_researcher_sees_is_the_approved_text():
    lines = sections("researcher-facing/failure-messages.NEW.md")
    assert mailbox.FAILURE_MESSAGES == {
        mailbox.DAEMON_STOPPED: lines["DAEMON STOPPED"], mailbox.Status.FAILING: lines["READER FAILING"],
        mailbox.Status.TURN_STOPPED: lines["READER TURN STOPPED"],
        mailbox.Status.READS_UNAVAILABLE: lines["READS UNAVAILABLE"], mailbox.Status.OK: lines["BACK TO NORMAL"]}
    # READER PAUSED went with the daily limits (#2099, Richard 09-28: "remove the limits").
    assert set(lines) - {"DAEMON STOPPED", "READER FAILING", "READER TURN STOPPED", "READS UNAVAILABLE",
                         "BACK TO NORMAL"} == {"READER PAUSED"}


def test_doctor_shows_the_readers_state_turns_and_asks(tmp_path):
    from probe.cli import doctor

    w = _worker(tmp_path)
    lane = _lane(w, Reader(end="hi"))
    asyncio.run(lane.run_turn("prompt"))
    mailbox.write_ask(SID, "q")
    lane.take_asks()
    lane.fail_open_asks("x")
    rl.write_status(SID, mailbox.Status.FAILING, "RuntimeError: gateway 502")
    rows = "\n".join(doctor._reader_rows(SID))
    assert "Probe daemon's reader failing: RuntimeError: gateway 502." in rows
    assert "1 sent" in rows and "1 failed" in rows
    rl.write_status(SID, mailbox.Status.OK)
    assert "running" in doctor._reader_rows(SID)[0]


def test_the_readers_turn_shows_the_approved_lines(tmp_path):
    w = _worker(tmp_path)
    memory = tmp_path / "home" / ".claude" / "projects" / "x" / "memory" / "MEMORY.md"
    w._memory_index = lambda: [memory]
    memory.parent.mkdir(parents=True)
    memory.write_text("- [digits](digits.md) - the SVM baseline\n")
    script = Reader(end="")
    lane = _lane(w, script)
    mailbox.write_ask(SID, "what did we get for C=10 last time?")
    lane.take_asks()
    asyncio.run(lane.run_turn("ask"))
    first = _text(script.seen[0][0])
    assert f"{rl.MEMORY_FRAMING}\n- [digits](digits.md)" in first
    assert f"{rl.DIVIDER}\n\n[researcher · turn 1" in first
    assert first.rstrip().endswith("The main agent asks: what did we get for C=10 last time?")
    assert script.seen[0][1].output_tools[0].name == "final_result"
    assert {t.name for t in script.seen[0][1].function_tools} == {"read", "session"}, "no shell, no writes"


# ---------------------------------------------------------------------------
# A turn: when, what it sends, how it ends.
# ---------------------------------------------------------------------------


def test_the_reader_is_due_on_an_ask_a_prompt_or_new_events_after_20s(tmp_path):
    now = [1000.0]
    w = _worker(tmp_path, clock=lambda: now[0])
    lane = _lane(w, Reader())
    assert lane.due() == "prompt", "the first prompt"
    with w.store.tx():
        w.store.set_fact("read_cursor", w.store.events_between(1)[-1].seq)
    assert lane.due() is None, "nothing new"
    with w.session.transcript.open("a") as handle:
        handle.write(_line({"type": "assistant", "message": {"content": [{"type": "text", "text": "C=100 next"}]}}))
    w.read_new()
    lane.last_turn_at = now[0] - 5
    assert lane.due() is None, "new events, but under 20 s since the last turn"
    now[0] += rl.READ_EVERY_S
    assert lane.due() == "events"
    mailbox.write_ask(SID, "q")
    lane.take_asks()
    assert lane.due() == "ask"
    lane.next_attempt_at = now[0] + 1
    assert lane.due() is None, "backing off"


def test_an_unasked_message_is_saved_published_and_the_cursor_moves_in_one_go(tmp_path):
    w = _worker(tmp_path)
    lane = _lane(w, Reader(end="digits-svm (run r7) already swept C=0.1..100: best C=10, 0.9889."))
    got = asyncio.run(lane.run_turn("prompt"))
    assert got.outcome == rl.Outcome.SENT
    [msg] = _waiting()
    assert msg.kind == mailbox.Kind.MESSAGE and msg.text.startswith("digits-svm (run r7)")
    assert msg.rendered().startswith("[Probe] Team context from the daemon")
    assert lane.cursor() == w.store.events_between(1)[-1].seq
    row = w.store.db.execute("SELECT * FROM read_turns").fetchone()
    assert row["outcome"] == "sent" and row["ended"] is not None
    assert w.store.live_read_conversation()["messages"], "the history is saved"
    assert w.store.live_conversation() is None, "the writer's conversation is untouched"
    assert not w.store.unpublished_read_messages()


def test_the_next_turn_shows_only_new_events_and_keeps_the_history(tmp_path):
    w = _worker(tmp_path)
    script = Reader()
    lane = _lane(w, script)
    asyncio.run(lane.run_turn("prompt"))
    _append_turn(w, "now try a random forest")
    w.read_new()
    asyncio.run(lane.run_turn("prompt"))
    second = script.seen[1][0]
    new = _prompt(second[-1])
    assert "now try a random forest" in new and "sweep C for an SVM" not in new, "only what is new"
    assert "sweep C for an SVM" in _text(second), "the history carries the first turn"
    assert new.startswith(rl.DIVIDER)


def test_an_ask_is_answered_without_a_length_cap_and_names_its_question(tmp_path):
    long = "C=10 won. " * 400
    w = _worker(tmp_path)
    lane = _lane(w, Reader(end=long))
    ask = mailbox.write_ask(SID, "what C won?")
    lane.take_asks()
    assert not list(mailbox.asks_dir(SID).glob("a*.json")), "the ask file is moved aside once stored"
    got = asyncio.run(lane.run_turn("ask"))
    assert got.outcome == rl.Outcome.ANSWERED
    answer = mailbox.claim_answer(SID, ask.id)
    assert answer is not None and answer.kind == mailbox.Kind.ANSWER and answer.text == long.strip()
    assert answer.rendered().startswith(f'[Probe] Answer to your ask {ask.id} ("what C won?")')
    assert w.store.db.execute("SELECT state FROM read_asks").fetchone()["state"] == "answered"


def test_an_empty_answer_says_nothing_was_found(tmp_path):
    w = _worker(tmp_path)
    lane = _lane(w, Reader(end=""))
    ask = mailbox.write_ask(SID, "any prior RF runs?")
    lane.take_asks()
    asyncio.run(lane.run_turn("ask"))
    got = mailbox.claim_answer(SID, ask.id)
    assert got.kind == mailbox.Kind.NOTHING
    assert got.rendered() == f'[Probe] Answer to your ask {ask.id} ("any prior RF runs?"): nothing in the team\'s records.'


def test_an_unasked_message_over_1200_characters_is_sent_back_to_be_shortened(tmp_path):
    w = _worker(tmp_path)
    script = Reader([("end", "x" * 1500)], end="short")
    lane = _lane(w, script)
    asyncio.run(lane.run_turn("prompt"))
    retry = _text(script.seen[1][0][-1:])
    assert "not sent: the message is 1500 characters - at most 1,200. Shorten it." in retry
    [msg] = _waiting()
    assert msg.text == "short"


def test_prose_instead_of_final_result_is_the_answer_to_an_ask_and_dropped_otherwise(tmp_path):
    w = _worker(tmp_path)
    lane = _lane(w, Reader([("say", "C=10 won")] * 3))
    ask = mailbox.write_ask(SID, "what C won?")
    lane.take_asks()
    got = asyncio.run(lane.run_turn("ask"))
    assert got.outcome == rl.Outcome.PROSE
    assert mailbox.claim_answer(SID, ask.id).text == "C=10 won"

    _append_turn(w, "and gamma?")
    w.read_new()
    lane._model = FunctionModel(Reader([("say", "gamma was 0.001")] * 3))
    got = asyncio.run(lane.run_turn("prompt"))
    assert got.outcome == rl.Outcome.PROSE and not _waiting(mailbox.Kind.MESSAGE), "dropped, never sent"
    assert w.store.read_summary()["outcomes"]["prose"] == 2, "counted"


def test_a_turn_out_of_rounds_is_told_to_end_and_a_runaway_is_stopped(tmp_path):
    w = _worker(tmp_path)
    outline = ("tool", ("session", {"op": "outline"}))
    script = Reader([outline] * (agent_mod.READ_ROUNDS - 1), end="done")
    lane = _lane(w, script)
    got = asyncio.run(lane.run_turn("prompt"))
    assert got.outcome == rl.Outcome.SENT
    last = _text(script.seen[-1][0][-1:])
    assert f"not run: this turn was stopped - {agent_mod.READ_ROUNDS} model rounds. End it with final_result." in last

    # A model that never ends: stopped, and the ask it served fails with the reason.
    _append_turn(w, "more")
    w.read_new()
    lane._model = FunctionModel(Reader([outline] * 50))
    ask = mailbox.write_ask(SID, "q")
    lane.take_asks()
    got = asyncio.run(lane.run_turn("ask"))
    assert got.outcome == rl.Outcome.STOPPED
    failed = mailbox.claim_answer(SID, ask.id)
    assert failed.kind == mailbox.Kind.FAILED and "stopped the turn" in failed.reason
    status = json.loads(mailbox.status_path(SID).read_text())
    assert status["state"] == rl.Status.TURN_STOPPED


def test_the_reader_session_tool_refuses_the_writers_ops(tmp_path):
    w = _worker(tmp_path)
    seen = {}

    def logbook(messages, info):
        return ("tool", ("session", {"op": "logbook"}))

    def look(messages, info):
        seen["reply"] = _text(messages[-1:])
        return ("end", "")

    lane = _lane(w, Reader([logbook, look]))
    asyncio.run(lane.run_turn("prompt"))
    assert "'open', 'outline' or 'search'" in seen["reply"]


def test_the_reader_never_needs_or_renews_the_writers_lease(tmp_path):
    w = _worker(tmp_path)
    (tmp_path / "home" / "work" / "notes.md").write_text("C=10 is best\n")
    seen = {}

    def read_notes(messages, info):
        return ("tool", ("read", {"path": str(tmp_path / "home" / "work" / "notes.md")}))

    def look(messages, info):
        seen["reply"] = _text(messages[-1:])
        return ("end", "")

    assert not lease.lease_path(SID).exists()
    lane = _lane(w, Reader([read_notes, look]))
    asyncio.run(lane.run_turn("prompt"))
    assert "C=10 is best" in seen["reply"]
    assert not lease.lease_path(SID).exists(), "no lease was taken or renewed"


def test_search_knowledge_always_leaves_out_the_watched_session():
    cap = agent_mod.ExcludeWatchedSession(SID)
    call = type("Call", (), {"tool_name": "search_knowledge"})()
    got = asyncio.run(cap.before_tool_execute(None, call=call, tool_def=None,
                                              args={"query": "svm", "exclude_session": "other"}))
    assert got == {"query": "svm", "exclude_session": SID}
    other = type("Call", (), {"tool_name": "browse"})()
    assert asyncio.run(cap.before_tool_execute(None, call=other, tool_def=None, args={"q": 1})) == {"q": 1}


# ---------------------------------------------------------------------------
# Failures, stale asks, crash consistency, the store guard.
# ---------------------------------------------------------------------------


def test_two_failed_turns_tell_the_researcher_and_fail_open_asks(tmp_path):
    w = _worker(tmp_path)

    def boom(messages, info):
        raise RuntimeError("gateway 502")

    lane = _lane(w, boom)
    ask = mailbox.write_ask(SID, "q")
    lane.take_asks()
    cursor = lane.cursor()
    assert asyncio.run(lane.run_turn("ask")).outcome == rl.Outcome.FAILED
    assert lane.cursor() == cursor, "the events are shown again next time"
    assert not mailbox.status_path(SID).exists(), "one failure is not reported yet"
    assert lane.next_attempt_at > time.time()
    asyncio.run(lane.run_turn("ask"))
    assert json.loads(mailbox.status_path(SID).read_text())["state"] == rl.Status.FAILING
    failed = mailbox.claim_answer(SID, ask.id)
    assert failed.kind == mailbox.Kind.FAILED and failed.reason == rl.REASON_READER_FAILING
    assert "the daemon's reader failed 2 turns in a row" in (tmp_path / "state" / "probe" / "daemon-errors.log").read_text()


def test_an_ask_held_10_minutes_fails(tmp_path):
    now = [time.time()]
    w = _worker(tmp_path, clock=lambda: now[0])
    w.store.clock = lambda: now[0]
    lane = _lane(w, Reader())
    ask = mailbox.write_ask(SID, "q")
    lane.take_asks()
    now[0] += rl.READ_ASK_TIMEOUT_S - 1
    lane.close_stale_asks()
    assert w.store.waiting_read_asks()
    now[0] += 1
    lane.close_stale_asks()
    got = mailbox.claim_answer(SID, ask.id)
    assert got.kind == mailbox.Kind.FAILED and got.reason == "no answer in 10 min"


def test_a_saved_message_is_published_once_even_after_a_crash(tmp_path):
    w = _worker(tmp_path)
    lane = _lane(w, Reader())
    with w.store.tx():  # the turn's transaction committed; the worker died before publishing
        w.store.add_read_message(message_id="m1", kind=mailbox.Kind.MESSAGE, text="hello", origin_turn=1)
    lane.publish_pending()
    lane.publish_pending()
    assert [m.id for m in _waiting()] == ["m1"]
    mailbox.publish(mailbox.Message(id="m1", session=SID, kind=mailbox.Kind.MESSAGE, text="hello",
                                    made_at=w.store.db.execute("SELECT made_at FROM read_messages").fetchone()[0]))
    assert len(_waiting()) == 1, "publishing is idempotent by id"


def test_an_unasked_message_goes_stale_after_the_next_turn(tmp_path):
    w = _worker(tmp_path)
    lane = _lane(w, Reader(end="about the SVM"))
    asyncio.run(lane.run_turn("prompt"))
    assert _waiting()
    _append_turn(w, "turn 2")
    w.read_new()
    lane.drop_stale_unasked()
    assert _waiting(), "still current during the next turn"
    _append_turn(w, "turn 3")
    w.read_new()
    lane.drop_stale_unasked()
    assert not _waiting()


def test_a_store_transaction_cannot_nest(tmp_path):
    store = store_mod.Store(tmp_path / "s.db")
    with store.tx():
        with pytest.raises(RuntimeError, match="already open"):
            with store.tx():
                pass
    with store.tx():
        store.set_fact("x", 1)
    assert store.fact("x") == 1


def test_an_older_cli_never_adopts_the_readers_conversation(tmp_path):
    w = _worker(tmp_path)
    asyncio.run(_lane(w, Reader(end="hi")).run_turn("prompt"))
    assert w.store.live_read_conversation() is not None
    assert w.store.live_conversation() is None, "the writer's table holds nothing of the reader's"


def test_the_reader_counts_its_own_daily_tokens(tmp_path):
    w = _worker(tmp_path)
    asyncio.run(_lane(w, Reader(end="hi")).run_turn("prompt"))
    assert store_mod.device_tokens_today(lane=store_mod.LANE_READ) > 0
    assert store_mod.device_tokens_today(lane=store_mod.LANE_WRITE) == 0


# ---------------------------------------------------------------------------
# The worker: the reader's task, the finishing marker, the handover.
# ---------------------------------------------------------------------------


def test_the_worker_runs_the_reader_only_when_reads_are_on_and_stops_it_at_session_end(tmp_path, monkeypatch):
    monkeypatch.setenv(mailbox.ENV_READS, "1")
    monkeypatch.setattr(rl.ReaderLane, "_model_for_turn", lambda self: FunctionModel(Reader(end="team context")))
    w = _worker(tmp_path, model=FunctionModel(lambda m, i: ModelResponse(
        parts=[ToolCallPart(i.output_tools[0].name, {"summary": "ok"})])))
    started = {}

    async def run():
        task = asyncio.ensure_future(w.loop())
        for _ in range(200):
            await asyncio.sleep(0.05)
            if _waiting():
                break
        started["reader"] = w.reader is not None
        mailbox.write_ask(SID, "still open at the end")
        w.reader.take_asks()
        w.begin_stopping()
        return await asyncio.wait_for(task, 30)

    monkeypatch.setattr(worker_mod, "POLL_S", 0.05)
    monkeypatch.setattr(rl, "READ_POLL_S", 0.05)
    assert asyncio.run(run()) == 0
    assert started["reader"] and w.reader is None
    assert [m.text for m in _waiting()] == ["team context"]
    assert w.store.db.execute("SELECT state FROM read_asks").fetchone()["state"] == "waiting", (
        "left open for a resumed session's worker")
    assert mailbox.finishing_path(SID).exists(), "removed by main() when the process exits"


def test_no_reader_without_the_reads_switch(tmp_path, monkeypatch):
    w = _worker(tmp_path, model=FunctionModel(lambda m, i: ModelResponse(
        parts=[ToolCallPart(i.output_tools[0].name, {"summary": "ok"})])))
    monkeypatch.setattr(worker_mod, "POLL_S", 0.01)

    async def run():
        task = asyncio.ensure_future(w.loop())
        await asyncio.sleep(0.2)
        assert w.reader is None
        w.begin_stopping()
        return await asyncio.wait_for(task, 30)

    assert asyncio.run(run()) == 0


@pytest.mark.parametrize("daemon_records_for,reads", [("claude_code", True), ("codex", False)])
def test_the_daemon_profile_turns_the_reader_on_for_its_own_agent(tmp_path, monkeypatch, daemon_records_for, reads):
    """T8: the wizard's "Who records" replaces the developer switch -- a worker
    for a Claude Code session reads when Claude Code is on the daemon profile,
    and not because Codex is."""
    from probe.sdk import session_marker

    session_marker.write_recorder(daemon_records_for, session_marker.RECORDER_DAEMON)
    started: list = []
    monkeypatch.setattr(rl.ReaderLane, "start", lambda self: started.append(self))

    async def _stop(self):
        return None

    monkeypatch.setattr(rl.ReaderLane, "stop", _stop)
    monkeypatch.setattr(worker_mod, "POLL_S", 0.01)
    w = _worker(tmp_path, model=FunctionModel(lambda m, i: ModelResponse(
        parts=[ToolCallPart(i.output_tools[0].name, {"summary": "ok"})])))

    async def run():
        task = asyncio.ensure_future(w.loop())
        await asyncio.sleep(0.2)
        seen = w.reader is not None
        w.begin_stopping()
        await asyncio.wait_for(task, 30)
        return seen

    assert asyncio.run(run()) is reads
    assert bool(started) is reads


def test_a_waiting_worker_asks_for_a_handover_and_clears_it_once_it_has_the_lock(tmp_path):
    import fcntl

    path = worker_mod.lock_path(SID)
    path.parent.mkdir(parents=True, exist_ok=True)
    holder = path.open("a")
    fcntl.flock(holder.fileno(), fcntl.LOCK_EX)
    got = {}
    t = threading.Thread(target=lambda: got.setdefault("h", worker_mod.session_lock(SID, poll_s=0.02)))
    t.start()
    for _ in range(100):
        if mailbox.handover_path(SID).exists():
            break
        time.sleep(0.02)
    assert mailbox.handover_path(SID).exists()
    holder.close()
    t.join(5)
    assert not isinstance(got["h"], int)
    assert not mailbox.handover_path(SID).exists()
    got["h"].close()


def test_a_finishing_worker_hands_over_at_its_next_model_round(tmp_path):
    class Replay:
        calls: list = []

        async def run(self, argv, op_id):
            return 0, "{}"

    w = _worker(tmp_path, replay=Replay())
    rounds = {"n": 0}

    def model(messages, info):
        rounds["n"] += 1
        if rounds["n"] == 1:
            # The session ends and a resumed session's worker waits for the lock.
            w.begin_stopping()
            mailbox.handover_path(SID).touch()
            return ModelResponse(parts=[ToolCallPart("session", {"op": "outline"})])
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {"summary": "done"})])

    w._model = FunctionModel(model)
    assert asyncio.run(w.tick()) is None
    assert rounds["n"] == 1, "paused at the next round: no second model call"
    assert w.store.fact(worker_mod.CARRY_ON), "the new worker carries the same conversation on"
    assert w.store.live_conversation()["messages"]
    assert asyncio.run(w.tick()) == 0
    assert json.loads(lease.lease_path(SID).read_text())["reason"] == lease.REASON_HANDOVER


def test_the_session_end_budget_fits_one_full_model_call():
    from probe.daemon import model

    assert worker_mod.FINISH_CAP_S == 35 * 60
    assert worker_mod.FINISH_CAP_S > model.DEFAULT_TIMEOUT_S


def test_the_reader_stops_when_the_switch_leaves_the_daemon(tmp_path):
    w = _worker(tmp_path)
    lane = _lane(w, Reader(end="should never be sent"))
    _set_state("off")
    assert lane.quitting()
    asyncio.run(lane.tick())
    assert not _waiting() and w.store.read_summary()["turns"] == 0, "nothing more goes to the model"

    _set_state("daemon")

    def switch_off_mid_turn(messages, info):
        _set_state("read")
        return ("tool", ("session", {"op": "outline"}))

    lane._model = FunctionModel(Reader([switch_off_mid_turn], end="late"))
    cursor = lane.cursor()
    assert asyncio.run(lane.run_turn("prompt")).outcome == rl.Outcome.STOPPED
    assert not _waiting() and lane.cursor() == cursor


def test_a_stale_handover_marker_is_ignored(tmp_path):
    import os

    w = _worker(tmp_path)
    w.stopping = True
    marker = mailbox.handover_path(SID)
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.touch()
    assert w.handing_over()
    old = time.time() - worker_mod.HANDOVER_FRESH_S - 5
    os.utime(marker, (old, old))
    assert not w.handing_over(), "left by a waiter that died"


def test_the_readers_mcp_names_the_watched_session_and_hides_its_work(tmp_path, monkeypatch):
    """The hosted MCP leaves out what the watched session created (search and
    browse) when the reader asks: it names the session on every call."""
    from pydantic_ai.capabilities import mcp as mcp_mod

    seen = {}

    class FakeMCP:
        def __init__(self, url=None, **kw):
            seen.update(kw, url=url)

    monkeypatch.setattr(mcp_mod, "MCP", FakeMCP)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "1")
    monkeypatch.setenv("PROBE_DAEMON_KEY", "k")
    monkeypatch.setenv("PROBE_BASE_URL", "https://api.example.test")
    monkeypatch.setenv("PROBE_MCP_URL", "https://mcp.example.test/mcp")
    state = agent_mod.ReaderState(conversation=True)
    try:
        agent_mod.build_reader_agent("x", model=FunctionModel(Reader()), state=state, session_id=SID, agent="codex")
    except Exception:  # noqa: BLE001 -- the fake is not a capability; only its arguments matter here
        pass
    assert seen["headers"] == {"X-Probe-Agent": "codex", "X-Probe-Agent-Session": SID,
                               "X-Probe-Hide-Session-Work": "1"}


def test_the_daemons_writes_carry_the_watched_session(tmp_path):
    """What the writer creates is filed as the watched session's own work (the
    server's origin record): its shell forwards the session."""
    from probe.sdk import agent_session

    w = _worker(tmp_path)
    env = w.deps(None).probe_env
    assert env[agent_session.FORWARDED_SESSION_ENV] == f"claude_code:{SID}"
    assert agent_session.resolve_agent_session(env) == ("claude_code", SID)


def test_failed_turns_reuse_one_fresh_conversation(tmp_path):
    w = _worker(tmp_path)

    calls = {"n": 0}
    ok = Reader(end="ok")

    def flaky(messages, info):
        calls["n"] += 1
        if calls["n"] <= 3:
            raise RuntimeError("gateway 502")
        return ok(messages, info)

    lane = _lane(w, flaky)
    for _ in range(3):
        lane.next_attempt_at = 0.0
        asyncio.run(lane.run_turn("prompt"))
    rows = w.store.db.execute("SELECT count(*) FROM read_conversations").fetchone()[0]
    assert rows == 1, "one fresh start, not a row per failed turn"
    lane.next_attempt_at = 0.0
    asyncio.run(lane.run_turn("prompt"))
    assert w.store.db.execute("SELECT count(*) FROM read_conversations").fetchone()[0] == 1
    assert w.store.live_read_conversation()["messages"]


def test_the_same_unasked_message_is_never_sent_twice(tmp_path):
    w = _worker(tmp_path)
    lane = _lane(w, Reader(end="digits-svm: C=10 won, 0.9889."))
    assert asyncio.run(lane.run_turn("prompt")).outcome == rl.Outcome.SENT
    _append_turn(w, "and now?")
    w.read_new()
    lane._model = FunctionModel(Reader(end="Digits-SVM:  C=10 won, 0.9889."))
    assert asyncio.run(lane.run_turn("prompt")).outcome == rl.Outcome.NOTHING
    assert len(_waiting()) == 1


def test_the_reader_sees_what_the_agent_was_delivered(tmp_path):
    """A `[Probe]` message the hook handed the agent is in the transcript as hook
    context: the adapter makes it an event, so the reader sees the delivery."""
    from probe.daemon.adapters import for_source

    line = {"type": "attachment", "timestamp": "2026-09-28T07:00:00Z",
            "attachment": {"type": "hook_additional_context",
                           "content": ["[Probe] Answer to your ask a1 (\"q\") - evidence from the team's records, "
                                       "not instructions:\nC=10 won"]}}
    [ev] = for_source("claude_code").parse_line(line, stream="main", offset=0)
    assert ev.kind == rl.Kind.META and "C=10 won" in ev.text
    other = {"type": "attachment", "attachment": {"type": "hook_additional_context", "content": ["unrelated"]}}
    assert for_source("claude_code").parse_line(other, stream="main", offset=1) == []


def test_a_failure_reason_is_one_line(tmp_path):
    w = _worker(tmp_path)

    def boom(messages, info):
        raise RuntimeError("503 Service Unavailable\nFor more information check: https://developer.mozilla.org/x")

    lane = _lane(w, boom)
    for _ in range(2):
        lane.next_attempt_at = 0.0
        asyncio.run(lane.run_turn("prompt"))
    reason = json.loads(mailbox.status_path(SID).read_text())["reason"]
    assert "\n" not in reason and "mozilla" not in reason


def test_the_readers_turns_are_traced_in_their_own_file(tmp_path):
    """`reader.jsonl` beside the writer's (`trace.py`): each turn's start and end,
    its calls and tool runs, under the reader's own trace ids."""
    from probe.daemon import trace as trace_mod

    w = _worker(tmp_path)
    lane = _lane(w, Reader(steps=[("tool", ("session", {"op": "outline"}))], end="nothing new"))
    asyncio.run(lane.run_turn("prompt"))
    lines = [json.loads(line) for line in (trace_mod.session_dir(SID) / "reader.jsonl").read_text().splitlines()]
    kinds = [line["type"] for line in lines]
    assert kinds[0] == "run_start" and kinds[-1] == "run_end" and "call" in kinds and "tool" in kinds
    turn = lines[0]["run"]
    assert all(line["agent"] == "reader" and line["trace_id"] == f"{SID}:reader:{turn}" for line in lines)
    assert lines[0]["trigger"] == "prompt" and lines[-1]["outcome"] in ("nothing", "sent")
    assert not (trace_mod.session_dir(SID) / "writer.jsonl").exists(), "the writer's file is the writer's"


def test_an_answer_withdraws_an_unasked_message_made_before_its_ask(tmp_path):
    """Live end-to-end test: the reader's prompt turn sent an unasked message on
    the topic the researcher's prompt raised, the agent then asked, and both
    arrived in one hook with the same facts. An answer now replaces an unasked
    message still waiting that was made before its ask; a later one, and any
    unasked message beside a "nothing found" ending, stay."""
    now = [time.time()]
    w = _worker(tmp_path, clock=lambda: now[0])
    w.store.clock = lambda: now[0]
    lane = _lane(w, Reader())
    with w.store.tx():
        w.store.add_read_message(message_id="m-before", kind=mailbox.Kind.MESSAGE, text="C=10 won", origin_turn=1)
    lane.publish_pending()
    now[0] += 5
    ask = mailbox.write_ask(SID, "which C won?", now=now[0])
    lane.take_asks()
    now[0] += 5
    with w.store.tx():
        w.store.add_read_message(message_id="m-after", kind=mailbox.Kind.MESSAGE, text="gamma 1e-3", origin_turn=2)
        w.store.add_read_message(message_id="ans", kind=mailbox.Kind.ANSWER, text="C=10 (0.9889)", ask=ask.id,
                                 question=ask.question, origin_turn=2)
    lane.publish_pending()
    assert sorted(m.id for m in _waiting()) == ["ans", "m-after"]


def test_nothing_found_withdraws_no_unasked_message(tmp_path):
    now = [time.time()]
    w = _worker(tmp_path, clock=lambda: now[0])
    w.store.clock = lambda: now[0]
    lane = _lane(w, Reader())
    with w.store.tx():
        w.store.add_read_message(message_id="m-before", kind=mailbox.Kind.MESSAGE, text="C=10 won", origin_turn=1)
    lane.publish_pending()
    now[0] += 5
    ask = mailbox.write_ask(SID, "any OOM?", now=now[0])
    lane.take_asks()
    with w.store.tx():
        w.store.add_read_message(message_id="none", kind=mailbox.Kind.NOTHING, ask=ask.id, question=ask.question,
                                 origin_turn=2)
    lane.publish_pending()
    assert sorted(m.id for m in _waiting()) == ["m-before", "none"]
