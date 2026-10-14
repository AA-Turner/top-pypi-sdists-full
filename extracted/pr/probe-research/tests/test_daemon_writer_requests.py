"""The main agent's requests to the daemon's writer (writer channel, 2026-10-13).

`probe ask --writer` files a request in the mailbox's `requests/` folder; the
worker takes it as a META event on the `request` stream, which starts a run at
once; the run that showed it answers it with its `reply` and the writes it made
(from the logbook); a request that will not run fails with a reason and is
never run later. A run with structural writes and no request sends a receipt.

The model is Pydantic AI's FunctionModel (scripted); `probe` commands run
against a recording stub (the replay seam).
"""

from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path

import pytest

pytest.importorskip("pydantic_ai")
pytest.importorskip("pydantic_ai_harness")

from pydantic_ai.messages import ModelResponse, ToolCallPart  # noqa: E402
from pydantic_ai.models.function import AgentInfo, FunctionModel  # noqa: E402

from probe.daemon import bite as bite_mod  # noqa: E402
from probe.daemon import lease, mailbox  # noqa: E402
from probe.daemon import model as model_mod  # noqa: E402
from probe.daemon import requests as requests_mod  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402
from probe.daemon.events import REQUEST_SOURCE, REQUEST_STREAM, Kind  # noqa: E402
from probe.daemon.store import UNRECORDED_BITE  # noqa: E402

SID = "11111111-2222-3333-4444-555555555555"
CREATE = "probe experiment create sft-wave1 --project willow --question 'Does more SFT data help?'"


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """No real config (so no real key), no MCP: nothing leaves the box."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.delenv("PROBE_DAEMON_KEY", raising=False)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    monkeypatch.setenv(worker_mod.ENV_MODE, "conversation")
    monkeypatch.delenv(model_mod.ENV_WRITER_GAP, raising=False)
    (tmp_path / "state" / "probe" / "sessions").mkdir(parents=True)
    (lease.sessions_dir() / f"{SID}.state").write_text("daemon")


class Replay:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    async def run(self, argv, op_id):
        self.calls.append(list(argv))
        return 0, json.dumps({"ok": True})

    def deletion_facts(self, kind, target):
        return {"id": target, "name": target, "what": kind, "others": {}, "count": 0, "updated_at": "t"}


class Script:
    """The writer: `steps` in order, then it ends the run; `("end", (summary, reply))`."""

    def __init__(self, steps) -> None:
        self.steps = list(steps)
        self.seen: list[list] = []

    def __call__(self, messages, info: AgentInfo) -> ModelResponse:
        if not info.output_tools:
            return ModelResponse(parts=[])
        self.seen.append(list(messages))
        kind, arg = self.steps.pop(0) if self.steps else ("end", ("recorded", ""))
        if kind == "shell":
            return ModelResponse(parts=[ToolCallPart("shell", {"command": arg, "why": "t"})])
        summary, reply = arg
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {"summary": summary, "reply": reply})])


def _line(obj: dict) -> str:
    return json.dumps(obj) + "\n"


def _worker(tmp_path: Path, steps=(), *, clock=time.time) -> tuple[worker_mod.Worker, Replay]:
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True, exist_ok=True)
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(
        _line({"type": "permission-mode", "permissionMode": "default"})
        + _line({"type": "user", "message": {"content": "train three SFT arms off base run A"}, "cwd": str(work)})
        + _line({"type": "assistant", "message": {"content": [{"type": "text", "text": "Launched 3 arms."}]}}))
    replay = Replay()
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          clock=clock, replay=replay, model=FunctionModel(Script(steps)))
    return w, replay


def _script(w, steps) -> Script:
    script = Script(steps)
    w._model = FunctionModel(script)
    return script


def _writer_messages() -> list[mailbox.Message]:
    return [m for _p, m in mailbox.waiting(SID) if m.from_writer]


def _request_rows(w) -> dict[str, dict]:
    return {r["id"]: dict(r) for r in w.store.db.execute("SELECT * FROM write_requests")}


# ---------------------------------------------------------------------------
# In: a request is an event, and starts a run at once.
# ---------------------------------------------------------------------------


def test_a_request_is_one_event_shown_whole_and_its_file_is_taken(tmp_path):
    w, _ = _worker(tmp_path)
    long = "group the six arms into one experiment " * 30
    req = mailbox.write_request(SID, long)
    w.read_new()
    [ev] = [e for e in w.store.events_between(1) if e.stream == REQUEST_STREAM]
    assert ev.kind == Kind.META and ev.source == REQUEST_SOURCE
    assert ev.text == requests_mod.REQUEST_LINE.format(text=" ".join(long.split()))
    assert bite_mod.render(ev).endswith(ev.text), "whole, not a 300-character harness preview"
    assert mailbox.pending_requests(SID) == [] and _request_rows(w)[req.id]["state"] == "waiting"
    w.read_new()
    assert len([e for e in w.store.events_between(1) if e.stream == REQUEST_STREAM]) == 1, "taken once"


def test_a_request_shows_under_the_approved_label():
    """`bite/request-label.PROPOSED.md`, `{placeholders}` as wildcards."""
    import re

    fixture = Path(__file__).parent / "fixtures" / "daemon_prompts" / "bite" / "request-label.PROPOSED.md"
    lines = fixture.read_text(encoding="utf-8").split("\n")
    approved = "\n".join(lines[lines.index("---", 1) + 1:]).rstrip("\n")
    pattern = re.compile("[^\n]+?".join(re.escape(p) for p in re.split(r"\{[^{}]+\}", approved)))
    from probe.daemon.store import StoredEvent

    ev = StoredEvent(seq=1, event_id="request:7:0", stream=REQUEST_STREAM, kind=Kind.META, turn=1, ts=None,
                     noticed=0.0, text=requests_mod.REQUEST_LINE.format(text="group the arms"), tool=None,
                     call_id=None, command=None, is_error=False, side_file=None, chars=40, bite=None, offset=7,
                     source=REQUEST_SOURCE)
    assert pattern.fullmatch(bite_mod.render(ev))


def test_a_request_starts_a_run_at_once_wherever_it_sits_and_past_the_least_gap(tmp_path, monkeypatch):
    monkeypatch.setenv(model_mod.ENV_WRITER_GAP, "300")
    w, _ = _worker(tmp_path, clock=lambda: 1000.0)
    w.read_new()
    w.last_run_at = 999.0  # a run just ended: the least gap holds a turn end or the queue's age
    assert w.due() is None
    mailbox.write_request(SID, "file the arms")
    w.read_new()
    assert w.due() == worker_mod.TRIGGER_REQUEST
    assert not w.deferrable(worker_mod.TRIGGER_REQUEST, w.store.pending())


def test_a_request_already_past_its_time_fails_without_an_event(tmp_path):
    w, _ = _worker(tmp_path)
    req = mailbox.write_request(SID, "file the arms", now=time.time() - requests_mod.WRITE_REQUEST_TIMEOUT_S - 5)
    w.read_new()
    assert not [e for e in w.store.events_between(1) if e.stream == REQUEST_STREAM]
    [msg] = _writer_messages()
    assert msg.kind == mailbox.Kind.FAILED and msg.ask == req.id and msg.reason == requests_mod.REASON_TIMEOUT


# ---------------------------------------------------------------------------
# Out: the run that showed it replies, with what it did.
# ---------------------------------------------------------------------------


def test_the_run_that_saw_a_request_replies_with_the_writes_it_made(tmp_path):
    w, replay = _worker(tmp_path)
    req = mailbox.write_request(SID, "group the arms into an experiment", wait=True)
    w.read_new()
    _script(w, [("shell", CREATE), ("shell", "probe run move quiet-seahorse-812 --to sft-wave1"),
                ("shell", "probe run move mystic-cuttlefish-278 --to sft-wave1"),
                ("end", ("Grouped the SFT arms.", "Made sft-wave1 and moved both arms into it."))])
    assert asyncio.run(w.run_bite(w.due())) is True
    assert len(replay.calls) == 3
    [msg] = _writer_messages()
    assert msg.kind == mailbox.Kind.ANSWER and msg.ask == req.id
    assert msg.text == ("Made sft-wave1 and moved both arms into it.\n"
                        "Recorded: created experiment sft-wave1 · moved 2 runs to sft-wave1 "
                        "(quiet-seahorse-812, mystic-cuttlefish-278)")
    assert msg.rendered().startswith(mailbox.TEXT_WRITER_REPLY.split("{", 1)[0])
    row = _request_rows(w)[req.id]
    assert row["state"] == "answered" and row["bite"] == w.store.recent_bites(1)[0]["id"]
    assert mailbox.open_asks(SID) == [req.id], "open until the agent is handed the reply"


def test_a_reply_lists_what_ran_not_what_the_model_says(tmp_path):
    """The write list comes from the logbook: a write that failed is labelled."""
    w, replay = _worker(tmp_path)

    async def fail_moves(argv, op_id):
        replay.calls.append(list(argv))
        if argv[:2] == ["run", "move"]:
            return 1, "Moving the run...\nError: no experiment named sft-wave1"
        return 0, json.dumps({"ok": True})

    replay.run = fail_moves
    mailbox.write_request(SID, "group the arms")
    w.read_new()
    _script(w, [("shell", CREATE), ("shell", "probe run move quiet-seahorse-812 --to sft-wave1"),
                ("shell", "probe notes append --project willow 'arms launched'"),
                ("end", ("Grouped.", "Done: moved every arm."))])
    asyncio.run(w.run_bite(w.due()))
    [msg] = _writer_messages()
    assert msg.text == ("Done: moved every arm.\n"
                        "Recorded: created experiment sft-wave1 · 1 other write\n"
                        "Not recorded: moved run quiet-seahorse-812 to sft-wave1 "
                        "(failed: Error: no experiment named sft-wave1)"), "its output says why, not its purpose"


def test_a_reply_lists_the_writes_of_an_earlier_attempt_that_failed(tmp_path):
    """Codex P2: the list starts at the first bite that saw the request, not
    the bite that finished: a write made before a model error is still told."""

    class FailOnce(Script):
        def __call__(self, messages, info):
            if self.steps and self.steps[0][0] == "raise":
                self.steps.pop(0)
                raise RuntimeError("the model route fell over")
            return super().__call__(messages, info)

    w, _ = _worker(tmp_path)
    req = mailbox.write_request(SID, "group the arms")
    w.read_new()
    w._model = FunctionModel(FailOnce([("shell", CREATE), ("raise", None)]))
    assert asyncio.run(w.run_bite(w.due())) is False
    assert _request_rows(w)[req.id]["state"] == "waiting"
    _script(w, [("shell", "probe run move quiet-seahorse-812 --to sft-wave1"), ("end", ("Grouped.", "Grouped."))])
    assert asyncio.run(w.run_bite(worker_mod.TRIGGER_REQUEST)) is True
    [msg] = _writer_messages()
    assert msg.ask == req.id and msg.text == (
        "Grouped.\nRecorded: created experiment sft-wave1 · moved run quiet-seahorse-812 to sft-wave1")


def test_two_requests_in_one_run_get_the_same_reply(tmp_path):
    w, _ = _worker(tmp_path)
    first = mailbox.write_request(SID, "group the arms")
    second = mailbox.write_request(SID, "and name the experiment sft-wave1")
    w.read_new()
    _script(w, [("shell", CREATE), ("end", ("Grouped.", "Made sft-wave1."))])
    asyncio.run(w.run_bite(w.due()))
    msgs = {m.ask: m.text for m in _writer_messages()}
    assert set(msgs) == {first.id, second.id} and msgs[first.id] == msgs[second.id]
    assert "Recorded: created experiment sft-wave1" in msgs[first.id]


def test_a_paused_run_replies_when_it_finishes_with_the_writes_of_both_bites(tmp_path, monkeypatch):
    """O2: a run pauses after ROUNDS_BEFORE_YIELD rounds with the request shown;
    the reply waits for the run's end, and lists what both bites did."""
    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 2)
    w, _ = _worker(tmp_path)
    req = mailbox.write_request(SID, "group the arms")
    w.read_new()
    _script(w, [("shell", CREATE), ("shell", "probe run move quiet-seahorse-812 --to sft-wave1"),
                ("shell", "probe run move never --to x")])
    assert asyncio.run(w.run_bite(w.due())) is True
    assert w.store.recent_bites(1)[0]["outcome"] == "paused"
    assert _writer_messages() == [] and _request_rows(w)[req.id]["state"] == "waiting"
    _script(w, [("shell", "probe run move mystic-cuttlefish-278 --to sft-wave1"),
                ("end", ("Grouped.", "Grouped both arms."))])
    assert asyncio.run(w.run_bite(w.due())) is True
    [msg] = _writer_messages()
    assert msg.ask == req.id and msg.text == (
        "Grouped both arms.\nRecorded: created experiment sft-wave1 · moved 2 runs to sft-wave1 "
        "(quiet-seahorse-812, mystic-cuttlefish-278)")


def test_an_empty_reply_still_says_what_happened(tmp_path):
    w, _ = _worker(tmp_path)
    mailbox.write_request(SID, "group the arms")
    w.read_new()
    _script(w, [("end", ("nothing new", ""))])
    asyncio.run(w.run_bite(w.due()))
    [msg] = _writer_messages()
    assert msg.text == "No change recorded."


# ---------------------------------------------------------------------------
# Receipts: structural writes nobody asked for.
# ---------------------------------------------------------------------------


def test_a_run_with_structural_writes_and_no_request_sends_one_receipt(tmp_path, monkeypatch):
    monkeypatch.setenv(mailbox.ENV_READS, "on")
    w, _ = _worker(tmp_path)
    w.read_new()
    _script(w, [("shell", CREATE), ("shell", "probe run move quiet-seahorse-812 --to sft-wave1"),
                ("shell", "probe notes append --project willow 'arms launched'"),
                ("end", ("Filed the arms.", ""))])
    asyncio.run(w.run_bite("turn end"))
    [msg] = _writer_messages()
    assert msg.kind == mailbox.Kind.MESSAGE and msg.ask is None
    assert msg.text == "created experiment sft-wave1 · moved run quiet-seahorse-812 to sft-wave1"
    assert msg.rendered() == f"[Probe] The writer recorded: {msg.text}"


def test_no_receipt_where_the_agent_s_hooks_read_no_mailbox(tmp_path, monkeypatch):
    """Like the audit's reports: a session whose agent records with no reader
    has nothing to deliver a receipt."""
    monkeypatch.delenv(mailbox.ENV_READS, raising=False)
    w, _ = _worker(tmp_path)
    w.read_new()
    _script(w, [("shell", CREATE), ("end", ("Filed.", ""))])
    asyncio.run(w.run_bite("turn end"))
    assert _writer_messages() == [] and not w.store.unpublished_writer_messages()


def test_no_receipt_for_a_run_without_structural_writes(tmp_path, monkeypatch):
    monkeypatch.setenv(mailbox.ENV_READS, "on")
    w, _ = _worker(tmp_path)
    w.read_new()
    _script(w, [("shell", "probe notes append --project willow 'arms launched'"),
                ("shell", "probe experiment create --help"), ("end", ("noted", ""))])
    asyncio.run(w.run_bite("turn end"))
    assert _writer_messages() == []


def test_a_receipt_is_capped_with_how_many_more():
    rows = [{"head": "run move", "status": "ran", "reason": None,
             "argv": json.dumps(["probe", "run", "move", f"run-{i:03d}", "--to", f"experiment-number-{i:03d}"])}
            for i in range(40)]
    text = requests_mod.receipt_text(requests_mod.describe(rows))
    assert len(text) <= requests_mod.RECEIPT_MAX_CHARS and text.endswith(" more")
    shown = text.count("moved run")
    assert text.endswith(f"+{40 - shown} more")


def _row(argv, status="ran", *, head=None, reason=None, output=None):
    words = argv.split()
    return {"head": head or " ".join(words[1:3]), "status": status, "reason": reason, "output": output,
            "argv": json.dumps(words)}


def test_writes_are_named_by_the_cli_s_own_parse_and_split_done_from_not_done():
    got = requests_mod.describe([
        _row("probe group create sft-wave1 --name lr-sweep"),
        _row("probe experiment fork sft-wave1 sft-wave2"),
        _row("probe edge add --source run:a --relation led_to --target run:b"),
        _row("probe project move willow-sub --top-level"),
        _row("probe run move --to=sft-wave1 quiet-seahorse-812"),
        _row("probe run set mystic-cuttlefish-278 --name arm-2k"),
        _row("probe run move amber-finch-104 --to sft-wave1", "not_run",
             reason="block b1: it names a file a .probe.config sets to off"),
        _row("probe run delete r9", "held", reason="a delete Probe cannot undo"),
        _row("probe experiment create e9 --project willow", "queued"),
        _row("probe run move r8 --to e1", "failed", output="Error: no run named r8\n"),
        _row("probe notes append --project willow hi", head="notes append"),
        _row("probe notes append --project willow again", "failed", head="notes append"),
        _row("probe run tag r1 x --help", head="run tag"),
        _row("probe run get r1", "read", head="run get"),
        _row("continued run", "not_run", head="skipped", reason="it hit its limits"),
    ])
    assert got.done == ["created group lr-sweep in sft-wave1", "forked experiment sft-wave1 as sft-wave2",
                        "linked run:a led_to run:b", "moved project willow-sub to the top level",
                        "moved run quiet-seahorse-812 to sft-wave1", "changed run mystic-cuttlefish-278"]
    assert got.not_done == [
        "moved run amber-finch-104 to sft-wave1 (not run: it names a file a .probe.config sets to off)",
        "deleted run r9 (held for the researcher)",
        "created experiment e9 (queued: Probe did not answer yet)",
        "moved run r8 to e1 (failed: Error: no run named r8)"]
    assert (got.others_done, got.others_not_done) == (1, 1), "help, reads and a skipped stretch are not writes"
    assert requests_mod.receipt_text(requests_mod.describe([_row("probe run move r8 --to e1", "failed")])) == "", \
        "a receipt names only what was recorded"


def test_a_reply_and_a_failure_reason_are_capped():
    long = "x" * (requests_mod.REPLY_MAX_CHARS + 500)
    text = requests_mod.reply_text(long, requests_mod.Writes())
    assert text == "x" * requests_mod.REPLY_MAX_CHARS + "\nNo change recorded."
    assert requests_mod.failure_reason("r", requests_mod.Writes(others_done=2)) == "r (partly done: 2 other writes)"


def test_a_failure_reason_is_scrubbed_like_the_text(tmp_path):
    w, _ = _worker(tmp_path)
    key = "sk-ant-api03-" + "A" * 93 + "AA"
    with w.store.tx():
        w.store.add_writer_message(message_id="m1", kind=mailbox.Kind.FAILED, ask="w1", reason=f"failed: {key}")
    [row] = w.store.unpublished_writer_messages()
    assert key not in row["reason"]


# ---------------------------------------------------------------------------
# A request that will not run fails, and never runs later.
# ---------------------------------------------------------------------------


def test_a_request_no_run_takes_in_45_minutes_fails_and_is_retired(tmp_path):
    now = [time.time()]
    w, _ = _worker(tmp_path, clock=lambda: now[0])
    req = mailbox.write_request(SID, "group the arms", now=now[0])
    w.read_new()
    now[0] += requests_mod.WRITE_REQUEST_TIMEOUT_S + 1
    w._fail_stuck_requests()
    [msg] = _writer_messages()
    assert msg.kind == mailbox.Kind.FAILED and msg.reason == requests_mod.REASON_TIMEOUT
    assert _request_rows(w)[req.id]["state"] == "failed"
    [ev] = [e for e in w.store.events_between(1) if e.stream == REQUEST_STREAM]
    assert ev.bite == UNRECORDED_BITE and not w.store.has_pending_request()
    assert all(e.stream != REQUEST_STREAM for e in w.store.pending()), "no later run sees it"


def test_read_only_fails_waiting_requests(tmp_path):
    w, _ = _worker(tmp_path)
    w.read_new()
    w.read_only_from = w.store.next_seq()
    req = mailbox.write_request(SID, "group the arms")
    asyncio.run(w._read_only_tick())
    [msg] = _writer_messages()
    assert msg.ask == req.id and msg.reason == requests_mod.REASON_READ_ONLY


def test_a_run_skipped_unfinished_fails_its_requests_with_what_it_did(tmp_path, monkeypatch):
    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 2)
    w, _ = _worker(tmp_path)
    req = mailbox.write_request(SID, "group the arms")
    w.read_new()
    _script(w, [("shell", CREATE), ("shell", "probe run move quiet-seahorse-812 --to sft-wave1"),
                ("shell", "ls")])
    asyncio.run(w.run_bite(w.due()))
    assert w.store.recent_bites(1)[0]["outcome"] == "paused"
    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 40)
    _script(w, [("shell", "ls same")] * 8)  # the loop detector stops the carried-on run
    asyncio.run(w.run_bite(w.due()))
    assert w.store.recent_bites(1)[0]["outcome"] == "cut short: skipped"
    [msg] = _writer_messages()
    assert msg.kind == mailbox.Kind.FAILED and msg.ask == req.id
    assert msg.reason.startswith(requests_mod.REASON_SKIPPED + " (partly done: created experiment sft-wave1")


def test_a_session_that_ends_fails_its_waiting_requests(tmp_path):
    now = [time.time()]
    w, _ = _worker(tmp_path, clock=lambda: now[0])
    w.read_new()
    with w.store.tx():
        w.store.mark_covered(w.store.open_bite("x", 1, 99), 10_000)  # nothing else queued
    req = mailbox.write_request(SID, "group the arms")
    w.read_new()
    w.store.defer(1, 10_000)  # its run never came: the queue is spent
    w.stopping, w.drained, w.finish_by = True, True, now[0] - 1
    assert asyncio.run(w.tick()) == 0
    [msg] = _writer_messages()
    assert msg.ask == req.id and msg.reason == requests_mod.REASON_SESSION_END


def test_a_crash_before_publishing_publishes_once(tmp_path, monkeypatch):
    w, _ = _worker(tmp_path)
    mailbox.write_request(SID, "group the arms")
    w.read_new()
    real = mailbox.publish
    calls = {"n": 0}

    def crash(msg):
        calls["n"] += 1
        raise OSError("disk full")

    monkeypatch.setattr(mailbox, "publish", crash)
    _script(w, [("shell", CREATE), ("end", ("Grouped.", "Made sft-wave1."))])
    assert asyncio.run(w.run_bite(w.due())) is True, "a mailbox that refuses never stops the worker"
    assert calls["n"] == 1 and _writer_messages() == []
    assert w.store.unpublished_writer_messages(), "saved before the publish"
    monkeypatch.setattr(mailbox, "publish", real)
    w.publish_writer_messages()
    w.publish_writer_messages()
    assert len(_writer_messages()) == 1


def test_a_request_shown_to_a_paused_run_that_fails_never_runs_later(tmp_path, monkeypatch):
    """Codex P1: failing a request a paused run was shown ends that conversation,
    so no carry-on acts on it; the paused run's other events go back on the
    queue for a fresh run, the request's is retired."""
    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 2)
    w, _ = _worker(tmp_path)
    req = mailbox.write_request(SID, "group the arms")
    w.read_new()
    _script(w, [("shell", CREATE), ("shell", "ls"), ("shell", "ls again")])
    asyncio.run(w.run_bite(w.due()))
    assert w.store.recent_bites(1)[0]["outcome"] == "paused" and w._carrying_on()
    live = w.store.live_conversation()["id"]
    assert w.fail_requests(requests_mod.REASON_READ_ONLY) == 1
    [msg] = _writer_messages()
    assert msg.ask == req.id
    assert msg.reason == requests_mod.REASON_READ_ONLY + " (partly done: created experiment sft-wave1)"
    assert not w._carrying_on()
    now_live = w.store.live_conversation()
    assert now_live is None or now_live["id"] != live, "the conversation that saw it ended"
    assert w.store.pending(), "the paused run's other events are queued again"
    assert all(e.stream != REQUEST_STREAM for e in w.store.pending()) and not w.store.has_pending_request()


def test_a_request_a_run_saw_that_will_never_finish_fails_and_is_not_answered_later(tmp_path, monkeypatch):
    """A paused run's conversation ended without giving its events back (an
    older paused run, `requeue_paused` takes the newest only): the request is
    failed as skipped, never answered by a fresh run that never saw it."""
    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 2)
    w, _ = _worker(tmp_path)
    req = mailbox.write_request(SID, "group the arms")
    w.read_new()
    _script(w, [("shell", CREATE), ("shell", "ls"), ("shell", "ls again")])
    asyncio.run(w.run_bite(w.due()))
    with w.store.tx():
        w.store.end_conversation(w.store.live_conversation()["id"], "its history no longer serves")
        w.store.set_fact(worker_mod.CARRY_ON, None)
    with (tmp_path / f"{SID}.jsonl").open("a") as f:
        f.write(_line({"type": "user", "message": {"content": "carry on"}, "cwd": str(tmp_path / "home" / "work")}))
    w.read_new()
    _script(w, [("shell", "probe experiment create other-exp --project willow"), ("end", ("noted", "Made it."))])
    asyncio.run(w.run_bite("turn end"))  # a fresh run, before the stuck check: it never saw the request
    assert _request_rows(w)[req.id]["state"] == "waiting", "not answered by a run that never saw it"
    w._fail_stuck_requests()
    [msg] = [m for m in _writer_messages() if m.ask == req.id]
    assert msg.kind == mailbox.Kind.FAILED and msg.reason == (
        requests_mod.REASON_SKIPPED + " (partly done: created experiment sft-wave1)"), "never the fresh run's write"


def test_a_request_whose_event_was_marked_unrecorded_fails(tmp_path):
    w, _ = _worker(tmp_path)
    req = mailbox.write_request(SID, "group the arms")
    w.read_new()
    seq = _request_rows(w)[req.id]["event_seq"]
    with w.store.tx():
        w.store.db.execute("UPDATE events SET bite = ? WHERE seq = ?", (UNRECORDED_BITE, seq))  # `/probe inline`
    w._fail_stuck_requests()
    [msg] = _writer_messages()
    assert msg.ask == req.id and msg.reason == requests_mod.REASON_INLINE


def test_a_paused_run_that_never_carries_on_fails_its_request_after_twice_the_timeout(tmp_path, monkeypatch):
    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 2)
    now = [time.time()]
    w, _ = _worker(tmp_path, clock=lambda: now[0])
    req = mailbox.write_request(SID, "group the arms", now=now[0])
    w.read_new()
    _script(w, [("shell", "ls"), ("shell", "ls again"), ("shell", "ls more")])
    asyncio.run(w.run_bite(w.due()))
    assert w._carrying_on()
    now[0] += requests_mod.WRITE_REQUEST_TIMEOUT_S + 1
    w._fail_stuck_requests()
    assert _writer_messages() == [], "a paused run may still finish it"
    now[0] += requests_mod.WRITE_REQUEST_TIMEOUT_S
    w._fail_stuck_requests()
    [msg] = _writer_messages()
    assert msg.ask == req.id and msg.reason == requests_mod.REASON_STALLED and not w._carrying_on()


def test_requests_start_at_most_one_run_a_minute(tmp_path):
    now = [1000.0]
    w, _ = _worker(tmp_path, clock=lambda: now[0])
    mailbox.write_request(SID, "group the arms", now=now[0])
    w.read_new()
    assert w.due() == worker_mod.TRIGGER_REQUEST
    _script(w, [("end", ("Grouped.", "Grouped."))])
    asyncio.run(w.run_bite(worker_mod.TRIGGER_REQUEST))
    now[0] += 10
    mailbox.write_request(SID, "and the scores", now=now[0])
    w.read_new()
    assert w.due() != worker_mod.TRIGGER_REQUEST, "held for the gap: it goes with the next run"
    now[0] += worker_mod.REQUEST_RUN_MIN_GAP_S
    assert w.due() == worker_mod.TRIGGER_REQUEST


def test_a_reply_lists_what_its_run_wrote_before_the_request_arrived(tmp_path, monkeypatch):
    """A paused run made a write, then a request arrived and its carry-on
    answered it: the run sends no receipt (it had a request), so the reply
    names that earlier write too."""
    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 2)
    w, _ = _worker(tmp_path)
    w.read_new()
    _script(w, [("shell", CREATE), ("shell", "ls"), ("shell", "ls again")])
    asyncio.run(w.run_bite("turn end"))
    assert w._carrying_on()
    req = mailbox.write_request(SID, "and move the arm in")
    w.read_new()
    _script(w, [("shell", "probe run move quiet-seahorse-812 --to sft-wave1"), ("end", ("Filed.", "Moved it."))])
    asyncio.run(w.run_bite(w.due()))
    [msg] = _writer_messages()
    assert msg.ask == req.id and msg.text == (
        "Moved it.\nRecorded: created experiment sft-wave1 · moved run quiet-seahorse-812 to sft-wave1")


def test_a_skipped_run_with_no_request_is_told_by_the_next_receipt(tmp_path, monkeypatch):
    monkeypatch.setenv(mailbox.ENV_READS, "on")
    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 2)
    w, _ = _worker(tmp_path)
    w.read_new()
    _script(w, [("shell", CREATE), ("shell", "ls"), ("shell", "ls again")])
    asyncio.run(w.run_bite("turn end"))
    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 40)
    _script(w, [("shell", "ls same")] * 8)  # the loop detector stops the carried-on run: skipped
    asyncio.run(w.run_bite(w.due()))
    assert w.store.recent_bites(1)[0]["outcome"] == "cut short: skipped"
    with (tmp_path / f"{SID}.jsonl").open("a") as f:
        f.write(_line({"type": "user", "message": {"content": "next"}, "cwd": str(tmp_path / "home" / "work")}))
    w.read_new()
    _script(w, [("end", ("noted", ""))])
    asyncio.run(w.run_bite("prompt"))
    [msg] = _writer_messages()
    assert msg.kind == mailbox.Kind.MESSAGE and msg.text == "created experiment sft-wave1"


def test_bites_mode_answers_a_request_from_the_bite_that_covered_it(tmp_path, monkeypatch):
    monkeypatch.setenv(worker_mod.ENV_MODE, "bites")
    w, _ = _worker(tmp_path)
    req = mailbox.write_request(SID, "group the arms")
    w.read_new()
    _script(w, [("shell", CREATE), ("end", ("Grouped.", "Made sft-wave1."))])
    assert asyncio.run(w.run_bite(w.due())) is True
    [msg] = _writer_messages()
    assert msg.ask == req.id and msg.text == "Made sft-wave1.\nRecorded: created experiment sft-wave1"


def test_an_approved_write_is_named_by_its_command_not_its_logbook_head():
    got = requests_mod.describe([_row("probe project delete willow-old --yes", head="override")])
    assert got.done == ["deleted project willow-old"] and got.others_done == 0


def test_a_write_told_with_a_failed_request_is_not_told_again_by_a_receipt(tmp_path, monkeypatch):
    monkeypatch.setenv(mailbox.ENV_READS, "on")
    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 2)
    now = [time.time()]
    w, _ = _worker(tmp_path, clock=lambda: now[0])
    req = mailbox.write_request(SID, "group the arms", now=now[0])
    w.read_new()
    _script(w, [("shell", CREATE), ("shell", "ls"), ("shell", "ls again")])
    asyncio.run(w.run_bite(w.due()))  # paused with the request in view
    now[0] += 2 * requests_mod.WRITE_REQUEST_TIMEOUT_S + 1
    w._fail_stuck_requests()
    [failed] = _writer_messages()
    assert failed.ask == req.id and failed.reason.endswith("(partly done: created experiment sft-wave1)")
    with (tmp_path / f"{SID}.jsonl").open("a") as f:
        f.write(_line({"type": "user", "message": {"content": "next"}, "cwd": str(tmp_path / "home" / "work")}))
    w.read_new()
    _script(w, [("shell", "probe run move quiet-seahorse-812 --to sft-wave1"), ("end", ("Filed.", ""))])
    asyncio.run(w.run_bite("prompt"))
    receipts = [m.text for m in _writer_messages() if m.kind == mailbox.Kind.MESSAGE]
    assert receipts == ["moved run quiet-seahorse-812 to sft-wave1"], "the create was told with the failure"
