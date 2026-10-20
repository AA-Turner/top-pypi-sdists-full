"""Daemon v2 worker, end to end: chat log -> queue -> a bite -> a `probe` command.

The model is Pydantic AI's FunctionModel (scripted), `probe` commands run
against a recording stub (the replay seam), and the chat log is a real file the
worker tails.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

import pytest

pytest.importorskip("pydantic_ai")

from pydantic_ai.messages import ModelResponse, ThinkingPart, ToolCallPart  # noqa: E402
from pydantic_ai.models.function import AgentInfo, FunctionModel  # noqa: E402

from probe.daemon import store as store_mod  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402
from probe.daemon.events import Kind  # noqa: E402
from probe.sdk.session_marker import WIZARD_HINT  # noqa: E402

SID = "11111111-2222-3333-4444-555555555555"
RUN = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


@pytest.fixture(autouse=True)
def _no_real_probe(tmp_path, monkeypatch):
    """No real config (so no real key) and no MCP: the Probe MCP now loads at the
    start of every run, and on a machine with a daemon key that would reach the
    real server."""
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.delenv("PROBE_DAEMON_KEY", raising=False)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")


class Replay:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    async def run(self, argv, op_id):
        self.calls.append(list(argv))
        return 0, json.dumps({"ok": True})

    def deletion_facts(self, kind, target):
        return {"id": target, "name": target, "what": kind, "others": {}, "count": 0, "updated_at": "t"}


def _line(obj: dict) -> str:
    return json.dumps(obj) + "\n"


def _session(tmp_path: Path, monkeypatch) -> tuple[Path, Path]:
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    (state / "probe" / "sessions").mkdir(parents=True)
    (state / "probe" / "sessions" / f"{SID}.state").write_text("daemon")
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True)
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(
        _line({"type": "permission-mode", "permissionMode": "default"})
        + _line({"type": "user", "message": {"content": "sweep C for an SVM on digits"}, "cwd": str(work)})
        + _line({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "python sweep.py"}}]}})
        + _line({"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": "t1", "content": f"run {RUN} started\nsvm acc=0.9889"}]}})
        + _line({"type": "assistant", "message": {"content": [{"type": "text", "text": "SVM C=10: 0.9889."}]}})
        + _line({"type": "system", "subtype": "turn_duration", "durationMs": 5})
    )
    return transcript, work


def _scripted(commands: list[str], note: str):
    calls = {"n": 0}

    def fn(messages, info: AgentInfo) -> ModelResponse:
        i = calls["n"]
        calls["n"] += 1
        if i < len(commands):
            return ModelResponse(parts=[ToolCallPart("shell", {"command": commands[i], "why": "test"})])
        tool = info.output_tools[0].name
        return ModelResponse(parts=[ToolCallPart(tool, {"summary": note})])

    return FunctionModel(fn), calls


def test_a_turn_end_triggers_a_bite_that_records_with_probe(tmp_path, monkeypatch):
    transcript, work = _session(tmp_path, monkeypatch)
    replay = Replay()
    model, calls = _scripted([f"probe run tag {RUN} svm"], "Studying SVM vs logreg on digits.")
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=replay, model=model)
    assert w.read_new() > 0
    assert w.due() == "turn end"
    assert asyncio.run(w.run_bite("turn end")) is True
    assert replay.calls == [["run", "tag", RUN, "svm"]]
    assert w.store.note() == "Studying SVM vs logreg on digits."
    assert w.store.pending() == []
    bite = w.store.recent_bites(1)[0]
    assert bite["outcome"] == "done"
    write = w.store.db.execute("SELECT head, status FROM writes").fetchone()
    assert (write["head"], write["status"]) == ("run tag", "ran")
    # The prompt the model saw: instructions first, the chat with outputs behind tags.
    assert calls["n"] == 2


def test_a_command_off_the_safe_list_is_held_and_runs_on_yes(tmp_path, monkeypatch):
    transcript, work = _session(tmp_path, monkeypatch)
    replay = Replay()
    model, _ = _scripted(["python summarize.py"], "note")
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=replay, model=model)
    w.read_new()
    asyncio.run(w.run_bite("turn end"))
    waiting = w.board.all(session_id=SID)
    assert len(waiting) == 1 and waiting[0].policy == "shell.unsafe_command"
    assert "python summarize.py" in waiting[0].question.question
    # The researcher says no: nothing runs, and the next bite hears it.
    w.board.answer(waiting[0].id, waiting[0].question.no_label, channel="test")
    asyncio.run(w.settle_answers())
    assert w.board.get(waiting[0].id).state == "denied"
    notice = [e for e in w.store.pending() if e.kind == Kind.META]
    assert notice and "said no" in notice[0].text


def test_bypass_mode_runs_without_asking(tmp_path, monkeypatch):
    transcript, work = _session(tmp_path, monkeypatch)
    text = transcript.read_text().replace('"permissionMode": "default"', '"permissionMode": "bypassPermissions"')
    transcript.write_text(text)
    (work / "summarize.py").write_text("print('ok')\n")
    model, _ = _scripted(["python3 summarize.py"], "note")
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=Replay(), model=model)
    w.read_new()
    asyncio.run(w.run_bite("turn end"))
    assert w.board.all(session_id=SID) == []  # an auto-approval asks no one, so it leaves no request file
    row = w.store.db.execute("SELECT status, output, reason FROM writes WHERE head = 'shell'").fetchone()
    assert row["status"] == "ran" and "ok" in row["output"] and row["reason"] == "auto-approved: bypass mode"


def test_a_failing_model_is_retried_later_and_never_drops_events(tmp_path, monkeypatch):
    transcript, work = _session(tmp_path, monkeypatch)

    def boom(messages, info):
        raise RuntimeError("provider down")

    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=Replay(), model=FunctionModel(boom))
    w.read_new()
    before = len(w.store.pending())
    assert asyncio.run(w.run_bite("turn end")) is False
    assert len(w.store.pending()) == before
    assert w.next_attempt_at > w.clock()
    assert w.store.recent_bites(1)[0]["outcome"] == "failed"


# ---------------------------------------------------------------------------
# How a bite fails (worker._failed), the back of the queue, no device fuse,
# no judge, and what a harness that cannot show its mode is allowed.
# ---------------------------------------------------------------------------


def _lease(sid: str = SID) -> dict:
    from probe.daemon import lease

    return json.loads(lease.lease_path(sid).read_text())


def _raising(exc: Exception) -> FunctionModel:
    def fn(messages, info):
        raise exc

    return FunctionModel(fn)


@pytest.mark.parametrize("status", [401, 403])
def test_a_refused_key_releases_the_lease_and_waits(tmp_path, monkeypatch, status):
    from pydantic_ai.exceptions import ModelHTTPError

    transcript, work = _session(tmp_path, monkeypatch)
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=Replay(), model=_raising(ModelHTTPError(status, "default")))
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is False
    assert _lease()["reason"] == "unauthorized" and w.released_reason == "unauthorized"
    assert w.next_attempt_at == pytest.approx(w.clock() + worker_mod.UNAUTHORIZED_RETRY_S, abs=5)
    assert w.failures == 0, "a refused key is not a failure that moves events to the back"
    errors = (tmp_path / "state" / "probe" / "daemon-errors.log").read_text()
    assert WIZARD_HINT in errors
    assert len(w.store.pending()) > 0


@pytest.mark.parametrize(
    ("body", "said"),
    [
        ({"code": "companion_disabled", "message": "m"}, "daemon recording is turned off for this team"),
        ({"error": {"code": "companion_disabled", "message": "m"}}, "daemon recording is turned off for this team"),
    ],
)
def test_a_refusal_about_the_team_says_why_instead_of_asking_for_a_new_key(tmp_path, monkeypatch, body, said):
    """A switched-off team refuses a new key the same way: the message
    names the cause and never sends anyone to approve one."""
    from pydantic_ai.exceptions import ModelHTTPError

    transcript, work = _session(tmp_path, monkeypatch)
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=Replay(), model=_raising(ModelHTTPError(403, "default", body=body)))
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is False
    assert _lease()["reason"] == "unauthorized" and w.failures == 0
    errors = (tmp_path / "state" / "probe" / "daemon-errors.log").read_text()
    assert said in errors and "A new key will not change that" in errors
    assert "approves a new one" not in errors


def test_a_key_that_is_not_the_daemons_still_asks_for_a_new_one(tmp_path, monkeypatch):
    from pydantic_ai.exceptions import ModelHTTPError

    transcript, work = _session(tmp_path, monkeypatch)
    body = {"code": "companion_credential_required", "message": "m"}
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=Replay(), model=_raising(ModelHTTPError(403, "default", body=body)))
    w.read_new()
    asyncio.run(w.run_bite("turn end"))
    assert "approves a new one" in (tmp_path / "state" / "probe" / "daemon-errors.log").read_text()


@pytest.mark.parametrize("exc", ["402", "budget"])
def test_the_budget_releases_the_lease_and_backs_off(tmp_path, monkeypatch, exc):
    from pydantic_ai.exceptions import ModelHTTPError

    transcript, work = _session(tmp_path, monkeypatch)
    error = ModelHTTPError(402, "default") if exc == "402" else RuntimeError(f"the team's {exc} is spent")
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=Replay(), model=_raising(error))
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is False
    assert _lease()["reason"] == "budget" and w.released_reason == "budget"
    assert w.failures == 1 and w.next_attempt_at > w.clock()
    assert w.store.recent_bites(1)[0]["outcome"] == "failed"


def test_a_refused_connection_is_not_read_as_the_budget(tmp_path, monkeypatch):
    """No fuse is left to match, and "fuse" hid inside "refused": any failure
    saying "connection refused" used to release the lease as `budget`."""
    transcript, work = _session(tmp_path, monkeypatch)
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=Replay(), model=_raising(RuntimeError("[Errno 111] Connection refused")))
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is False
    assert w.released_reason != "budget"


@pytest.mark.parametrize("status,body,changes", [
    (429, {"code": "budget_exhausted"}, True),
    (429, {"error": {"code": "budget_exhausted"}}, True),
    (429, {"code": "rate_limited", "message": "budget"}, False),
    (503, {"code": "budget_exhausted"}, False),
    (402, {}, False),
])
def test_only_structured_monthly_quota_refusal_moves_live_worker_inline(tmp_path, monkeypatch, status, body, changes):
    from pydantic_ai.exceptions import ModelHTTPError
    from probe.sdk import session_marker
    transcript, work = _session(tmp_path, monkeypatch)
    session_marker.mark_session_profile(SID, session_marker.RECORDER_DAEMON)
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"))
    assert w._quota_inline(ModelHTTPError(status, "default", body=body), "daemon") is changes
    assert session_marker.is_inline(SID) is changes
    assert session_marker.session_state(SID) == ("full" if changes else "daemon")


def test_writer_model_quota_response_enters_inline_without_retrying_or_covering_events(tmp_path, monkeypatch):
    from pydantic_ai.exceptions import ModelHTTPError
    from probe.sdk import session_marker
    transcript, work = _session(tmp_path, monkeypatch)
    session_marker.mark_session_profile(SID, session_marker.RECORDER_DAEMON)
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          model=_raising(ModelHTTPError(429, "default", body={"code": "budget_exhausted"})))
    w.read_new()
    w._renew()
    assert asyncio.run(w.run_bite("turn end")) is False
    assert session_marker.is_inline(SID)
    assert w.released_reason == "budget" and len(w.store.pending()) > 0
    assert w.store.recent_bites(1)[0]["outcome"] == "failed"


def test_a_bite_cut_short_is_retried_smaller_then_skipped_loudly(tmp_path, monkeypatch):
    transcript, work = _session(tmp_path, monkeypatch)
    monkeypatch.setattr(worker_mod, "BITE_REQUESTS", 2)
    model, _ = _scripted(["ls"] * 20, "never reached")
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=Replay(), model=model)
    w.read_new()
    queued = [ev.seq for ev in w.store.pending()]
    assert len(queued) >= 4
    assert asyncio.run(w.run_bite("turn end")) is False
    first = w.store.recent_bites(1)[0]
    assert first["outcome"] == "cut short" and "request_limit" in first["error"]
    assert [ev.seq for ev in w.store.pending()] == queued, "cut short is not recorded: its events stay queued"
    # What it spent before the cut counts, in its row and on the device's counter.
    assert first["input_tokens"] > 0
    assert store_mod.device_tokens_today() == first["input_tokens"] + first["output_tokens"]
    # The next bite takes half as many new events from the same first event...
    assert asyncio.run(w.run_bite("turn end")) is True
    second = w.store.recent_bites(1)[0]
    assert second["first_seq"] == first["first_seq"] == queued[0]
    taken = second["last_seq"] - second["first_seq"] + 1
    assert taken == (first["last_seq"] - first["first_seq"] + 1) // 2
    # ...and cut short again from there, that range is skipped: covered, and said out loud.
    assert second["outcome"] == "cut short: skipped" and w.store.fact("cut_short") is None
    left = w.store.pending()
    assert [ev.seq for ev in left if ev.kind != Kind.META] == queued[taken:]
    notice = [ev.text for ev in left if ev.kind == Kind.META]
    assert len(notice) == 1 and "were not recorded" in notice[0] and "too costly" in notice[0]
    skipped = f"events #{queued[0]}-#{queued[taken - 1]}"
    assert any(line.startswith(f"not run: {skipped}") and "too costly" in line for line in w.pending_lines())
    assert skipped in (tmp_path / "state" / "probe" / "daemon-errors.log").read_text()


def _thinks_to_the_limit(calls: dict) -> FunctionModel:
    """Every answer is thinking cut off at the token limit, so Pydantic AI itself
    raises "Model token limit ... exceeded before any response was generated"
    (gpt-6.1-sol at its 16,384-token default, strand-ai 2026-10-12)."""
    def fn(messages, info):
        calls["n"] += 1
        return ModelResponse(parts=[ThinkingPart("weighing it " * 50)], finish_reason="length")

    return FunctionModel(fn)


def test_an_answer_the_token_limit_ate_is_retried_smaller_then_skipped_never_looped(tmp_path, monkeypatch):
    """The same request thinks to the limit again every time: before, each failure
    backed off, a third moved the range to the back of the queue with the count
    reset, and the bite came back to fail again (41 runaways in 3.5 hours, about
    $0.25 each). Now it is cut short like a bite over its limits: half the events,
    then skipped out loud, and no "Daemon bug" ping."""
    transcript, work = _session(tmp_path, monkeypatch)
    pinged = []
    monkeypatch.setattr(worker_mod.alerts, "report_bite_failure", lambda exc, **kw: pinged.append(exc))
    calls = {"n": 0}
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=Replay(), model=_thinks_to_the_limit(calls))
    w.read_new()
    queued = [ev.seq for ev in w.store.pending()]
    assert asyncio.run(w.run_bite("turn end")) is False
    first = w.store.recent_bites(1)[0]
    assert first["outcome"] == "cut short" and "token limit" in first["error"]
    assert w.failures == 0 and w.no_answers == 1, "not a failure to defer: it is retried smaller"
    assert w.next_attempt_at > w.clock(), "but after a wait, so a model that never answers cannot spin"
    assert asyncio.run(w.run_bite("turn end")) is True
    second = w.store.recent_bites(1)[0]
    assert second["first_seq"] == queued[0] and second["outcome"] == "cut short: skipped"
    notice = [ev.text for ev in w.store.pending() if ev.kind == Kind.META]
    assert len(notice) == 1 and "answered nothing" in notice[0]
    assert calls["n"] == 2 and not pinged


def test_a_tool_call_the_token_limit_cut_off_is_the_same_no_answer(tmp_path, monkeypatch):
    """Thinking until the limit can also end in the middle of the final tool call:
    Pydantic AI's IncompleteToolCall, the same runaway, the same handling."""
    transcript, work = _session(tmp_path, monkeypatch)

    def fn(messages, info):
        return ModelResponse(parts=[ThinkingPart("weighing it " * 50),
                                    ToolCallPart(info.output_tools[0].name, '{"summary": "half')],
                             finish_reason="length")

    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=Replay(), model=FunctionModel(fn))
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is False
    assert w.store.recent_bites(1)[0]["outcome"] == "cut short" and w.failures == 0 and w.no_answers == 1


def test_a_refused_key_outranks_an_answer_the_token_limit_ate(tmp_path, monkeypatch):
    """Probe refused the daemon's key in the same run: the key's handling wins --
    the lease released `unauthorized`, the range kept for when the key works --
    never a cut short that could end in skipping it."""
    transcript, work = _session(tmp_path, monkeypatch)
    monkeypatch.setattr(worker_mod, "_key_refused", lambda deps: True)
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=Replay(), model=_thinks_to_the_limit({"n": 0}))
    w.read_new()
    queued = [ev.seq for ev in w.store.pending()]
    assert asyncio.run(w.run_bite("turn end")) is False
    assert w.released_reason == "unauthorized" and w.no_answers == 0
    assert [ev.seq for ev in w.store.pending()] == queued and w.store.fact("cut_short") is None


def _cut_off_mid_tool_call(calls: dict) -> FunctionModel:
    """Thinking until the limit, then the final tool call cut off mid arguments:
    Pydantic AI's IncompleteToolCall."""
    def fn(messages, info):
        calls["n"] += 1
        return ModelResponse(parts=[ThinkingPart("weighing it " * 50),
                                    ToolCallPart(info.output_tools[0].name, '{"summary": "half')],
                             finish_reason="length")

    return FunctionModel(fn)


@pytest.mark.parametrize("form", [_thinks_to_the_limit, _cut_off_mid_tool_call])
def test_answers_the_token_limit_ate_in_a_row_hand_recording_to_the_agent_until_one_answers(tmp_path, monkeypatch,
                                                                                           form):
    """A model that never answers: each such bite waits longer, and after
    NO_ANSWERS_BEFORE_RELEASE the lease goes (the agent records). A round the
    limit cut off -- with only thinking, or a tool call cut off mid arguments --
    never takes it back; the first that answers does."""
    transcript, work = _session(tmp_path, monkeypatch)
    calls = {"n": 0}
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=Replay(), model=form(calls))
    w.read_new()
    waits = []
    for _ in range(worker_mod.NO_ANSWERS_BEFORE_RELEASE):
        asyncio.run(w.run_bite("turn end"))
        waits.append(w.next_attempt_at - w.clock())
    assert waits == sorted(waits) and waits[0] < waits[-1], "each one in a row waits longer"
    assert w.no_answers == worker_mod.NO_ANSWERS_BEFORE_RELEASE
    assert w.released_reason == "gateway" and "answered nothing" in (tmp_path / "state" / "probe" /
                                                                      "daemon-errors.log").read_text()
    asyncio.run(w.run_bite("turn end"))
    assert w.released_reason == "gateway", "a round that only thought is no answer"
    model, _ = _scripted([], "recorded again")
    w._model = model
    with transcript.open("a") as handle:
        handle.write(_line({"type": "user", "message": {"content": "and now the RBF kernel"}}))
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert w.released_reason is None and w.no_answers == 0


def test_a_released_lease_comes_back_when_the_first_round_only_thinks_and_ends(tmp_path, monkeypatch):
    """A turn that only thought, ended normally (not at the limit), is an answer:
    the model's next round is its retry, and the lease released for the gateway
    comes back rather than the run stopping for want of it."""
    transcript, work = _session(tmp_path, monkeypatch)
    rounds = {"n": 0}

    def fn(messages, info):
        rounds["n"] += 1
        if rounds["n"] == 1:
            return ModelResponse(parts=[ThinkingPart("let me think about the sweep")], finish_reason="stop")
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {"summary": "recorded"})])

    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=Replay(), model=FunctionModel(fn))
    w.read_new()
    w._release("gateway")
    assert asyncio.run(w.run_bite("turn end")) is True
    assert w.released_reason is None


def test_three_failures_move_a_range_to_the_back_and_it_comes_back_later(tmp_path, monkeypatch):
    transcript, work = _session(tmp_path, monkeypatch)
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=Replay(), model=_raising(RuntimeError("provider down")))
    w.read_new()
    first = w.store.pending()
    # A later turn arrives while the first one keeps failing.
    with transcript.open("a") as handle:
        handle.write(_line({"type": "user", "message": {"content": "now try an RBF kernel"}}))
    w.read_new()
    for _ in range(worker_mod.FAILURES_BEFORE_BACK_OF_QUEUE):
        w.next_attempt_at = 0.0
        assert asyncio.run(w.run_bite("turn end")) is False
    assert w.store.fact("deferred_from") == first[0].seq and w.failures == 0
    waiting = w.store.pending()
    assert waiting and all(ev.seq > first[-1].seq for ev in waiting), "the later turn goes first"
    assert any("are queued for later: not recorded yet" in line for line in w.pending_lines())
    w.requeue_deferred()
    assert w.store.fact("deferred_from") == first[0].seq, "not while something else is pending"
    w.store.mark_covered(w.store.open_bite("test", None, None), waiting[-1].seq)
    w.requeue_deferred()
    assert [ev.seq for ev in w.store.pending()] == [ev.seq for ev in first]
    assert w.store.fact("deferred_from") is None


def test_no_device_fuse_a_device_far_past_the_old_one_still_calls_the_model(tmp_path, monkeypatch):
    """No device fuse (Richard 2026-09-28: "we dont want any limit"): the
    device's token counter is a meter only; 10^12 tokens today still calls the
    model and keeps the lease."""
    transcript, work = _session(tmp_path, monkeypatch)
    worker_mod.add_device_tokens(10**12)
    model, calls = _scripted([], "note")
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          replay=Replay(), model=model)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert calls["n"] >= 1 and w.released_reason is None


def test_the_daemon_asks_no_judge_after_a_turn():
    """The per-turn judge (Jev, `POST /v1/companion/judge`) is gone: no module,
    no worker step, no switch for it."""
    import importlib.util

    assert importlib.util.find_spec("probe.daemon.judge") is None
    assert not hasattr(worker_mod.Worker, "judge_turn")
    assert not [name for name in vars(worker_mod) if name.startswith("JUDGE")]


def test_a_pi_worker_never_reports_a_known_permission_mode(tmp_path, monkeypatch):
    transcript, work = _session(tmp_path, monkeypatch)
    # Even a hook record saying bypass: pi cannot show its mode, so the daemon asks.
    (tmp_path / "state" / "probe" / "sessions" / f"{SID}.mode").write_text("bypass")
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "pi", home=tmp_path / "home"),
                          replay=Replay())
    assert w.permission() == (False, False)
    deps = w.deps(None)
    assert deps.bypass is False and deps.mode_known is False
    cc = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                           replay=Replay())
    assert cc.permission() == (True, True)


@pytest.mark.parametrize(("source", "mode", "asks_jev"), [
    ("pi", "bypass", True),  # pi cannot show its mode: never bypass, so Jev first
    ("claude_code", "default", True),
    ("claude_code", None, True),  # a harness with modes whose mode is not read yet
    ("claude_code", "bypass", False),  # bypass runs it as before
])
def test_jev_is_asked_about_a_held_command_in_every_mode_but_bypass(tmp_path, monkeypatch, source, mode, asks_jev):
    """Shell approvals F8 (Richard 2026-10-15): a command off the safe list is
    put to Jev before the researcher in every mode except bypass. Jev judges
    inline Python only (#2899), so the command is one: `python3` on PATH is this
    interpreter, outside the working folders, named by its version."""
    from probe.daemon import command_check
    from probe.daemon import tools as tools_mod

    real = os.path.realpath(sys.executable)
    if not tools_mod._PYTHON_REAL.fullmatch(os.path.basename(real)):
        pytest.skip(f"the test interpreter's real file is not named by its version: {real}")
    (tmp_path / "pybin").mkdir()
    (tmp_path / "pybin" / "python3").symlink_to(real)
    monkeypatch.setenv("PATH", f"{tmp_path / 'pybin'}:/usr/bin:/bin")
    command = "python3 -c \"print(open('file.txt').read()[:5])\""
    transcript, work = _session(tmp_path, monkeypatch)
    if mode is not None:
        (tmp_path / "state" / "probe" / "sessions" / f"{SID}.mode").write_text(mode)
    (work / "file.txt").write_text("hello world\n")
    asked: list[str] = []

    async def check(**kw):
        asked.append(kw["command"])
        return None

    monkeypatch.setattr(command_check, "ask_probe", check)
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, source, home=tmp_path / "home"),
                          replay=Replay())
    out = asyncio.run(tools_mod.shell(w.deps(1), command))
    assert asked == ([command] if asks_jev else [])
    assert ("held for the researcher" in out) is asks_jev, out
