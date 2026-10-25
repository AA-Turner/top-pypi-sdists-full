"""The reader's gate (daemon cost round 4, D): a cheap model decides, before an
unasked reader turn, whether the reader should look (`reader_gate.py`).

OFF never calls it; SHADOW calls it and the reader looks anyway, its verdict on
the turn's trace; ON closes the wake as a SKIPPED turn on a skip. An ask never
goes through it, a failed gate is a look, and a skip keeps the events unread so
the reader's next turn (or an ask) reads them.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

pytest.importorskip("pydantic_ai")
pytest.importorskip("pydantic_ai_harness")

from pydantic_ai.messages import ModelResponse, TextPart, ToolCallPart  # noqa: E402
from pydantic_ai.models.function import AgentInfo, FunctionModel  # noqa: E402

from probe.daemon import model as model_mod  # noqa: E402
from probe.daemon import reader_gate  # noqa: E402
from probe.daemon import reader_lane as rl  # noqa: E402
from tests.test_daemon_reader import SID, FIXTURES, Reader, _append_turn, _isolated, _worker, body  # noqa: E402,F401


class Gate:
    """The gate's model: says `look` (or raises `fail`), and records each prompt."""

    def __init__(self, look: bool = False, fail: Exception | None = None) -> None:
        self.look = look
        self.fail = fail
        self.prompts: list[str] = []

    def __call__(self, messages, info: AgentInfo) -> ModelResponse:
        self.prompts.append("\n".join(getattr(p, "content", "") for p in messages[-1].parts
                                      if isinstance(getattr(p, "content", None), str)))
        if self.fail is not None:
            raise self.fail
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {"look": self.look, "why": "no ML"})])


def _lane(w, reader, gate) -> rl.ReaderLane:
    w.read_new()
    return rl.ReaderLane(w, model=FunctionModel(reader), gate_model=FunctionModel(gate))


def _wake(lane) -> rl.TurnResult:
    trigger = lane.due()
    assert trigger is not None
    return asyncio.run(lane.wake(trigger))


def _trace(lane) -> list[dict]:
    return [json.loads(line) for line in lane.trace.path.read_text().splitlines()]


@pytest.fixture
def mode(monkeypatch):
    def set_mode(value: str) -> None:
        monkeypatch.setenv(model_mod.ENV_READER_GATE, value)
    return set_mode


def test_off_never_calls_the_gate(tmp_path, mode):
    mode("off")
    gate, reader = Gate(), Reader(end="")
    lane = _lane(_worker(tmp_path), reader, gate)
    assert _wake(lane).outcome == rl.Outcome.NOTHING
    assert gate.prompts == [] and len(reader.seen) == 1


def test_shadow_records_a_skip_and_the_reader_looks_anyway(tmp_path, mode):
    mode("shadow")
    gate, reader = Gate(look=False), Reader(end="Prior work: svm-c-sweep reached 0.991.")
    lane = _lane(_worker(tmp_path), reader, gate)
    result = _wake(lane)
    assert result.outcome == rl.Outcome.SENT, "the reader still looked, and sent"
    assert len(gate.prompts) == 1 and "sweep C for an SVM on digits" in gate.prompts[0]
    start = [r for r in _trace(lane) if r["type"] == "run_start"][-1]
    assert start["gate"] == "skip"
    [line] = [r for r in _trace(lane) if r["type"] == "reader_gate"]
    assert line["decision"] == "skip" and line["mode"] == "shadow"
    row = lane.store.db.execute("SELECT outcome FROM read_turns ORDER BY id DESC").fetchone()
    assert row["outcome"] == "sent", "a miss is measured: skip beside sent"


def test_on_skips_the_turn_and_keeps_its_events_for_the_next(tmp_path, mode):
    mode("on")
    gate, reader = Gate(look=False), Reader(end="")
    w = _worker(tmp_path)
    lane = _lane(w, reader, gate)
    cursor = lane.cursor()
    assert _wake(lane).outcome == rl.Outcome.SKIPPED
    assert reader.seen == [], "no reader turn ran"
    assert lane.cursor() == cursor, "the skipped events stay unread"
    assert lane.due() is None, "the prompt the gate passed over does not wake the reader again"
    row = lane.store.db.execute("SELECT outcome, usd FROM read_turns ORDER BY id DESC").fetchone()
    assert row["outcome"] == "skipped"
    # The next prompt: the gate says look, and the reader reads both turns.
    _append_turn(w, "now compare with the MLP sweep")
    w.read_new()
    gate.look = True
    assert _wake(lane).outcome == rl.Outcome.NOTHING
    seen = "\n".join(str(getattr(p, "content", "")) for m in reader.seen[0][0] for p in m.parts)
    assert "sweep C for an SVM on digits" in seen and "now compare with the MLP sweep" in seen


def test_an_ask_never_goes_through_the_gate(tmp_path, mode):
    from probe.daemon import mailbox

    mode("on")
    gate, reader = Gate(look=False), Reader(end="svm-c-sweep: 0.991")
    lane = _lane(_worker(tmp_path), reader, gate)
    mailbox.write_ask(SID, "what did the team get for SVM C?")
    lane.take_asks()
    assert lane.due() == "ask"
    assert asyncio.run(lane.wake("ask")).outcome == rl.Outcome.ANSWERED
    assert gate.prompts == []


@pytest.mark.parametrize("fail", [RuntimeError("gateway_rejected: refused"), asyncio.TimeoutError()])
def test_a_failed_gate_is_a_look(tmp_path, mode, fail):
    mode("on")
    gate, reader = Gate(fail=fail), Reader(end="")
    lane = _lane(_worker(tmp_path), reader, gate)
    assert _wake(lane).outcome == rl.Outcome.NOTHING
    assert len(reader.seen) == 1, "the reader looked"
    [line] = [r for r in _trace(lane) if r["type"] == "reader_gate"]
    assert line["decision"] == "error" and line["error"]


def test_the_backlog_a_skip_leaves_keeps_to_one_turns_window(tmp_path, mode, monkeypatch):
    mode("on")
    monkeypatch.setattr(rl, "READ_MAX_EVENTS", 3)
    gate, reader = Gate(look=False), Reader(end="")
    w = _worker(tmp_path)
    lane = _lane(w, reader, gate)
    for n in range(4):
        _append_turn(w, f"prompt {n}")
    w.read_new()
    _wake(lane)
    last = int(lane.store.fact(rl.GATE_SEEN))
    unread = lane.store.events_between(lane.cursor() + 1, last)
    assert len(unread) == 3 and unread[-1].seq == last, "the newest three stay, the older drop off"


@pytest.mark.parametrize("gate_mode", ["shadow", "on"])
def test_with_prompt_wakes_off_the_gate_and_the_reader_read_the_newest_window(tmp_path, mode, monkeypatch,
                                                                              gate_mode):
    """Prod's reader gate (SHADOW) chooses the window it puts to the reader: with
    prompt wakes off it is the newest too, and the cursor passes the older backlog."""
    mode(gate_mode)
    monkeypatch.setenv(model_mod.ENV_READER_PROMPT_WAKE, "off")
    monkeypatch.setattr(rl, "READ_MAX_EVENTS", 3)
    gate, reader = Gate(look=True), Reader(end="")
    w = _worker(tmp_path)
    lane = _lane(w, reader, gate)
    for n in range(6):
        _append_turn(w, f"backlog prompt {n}")
    w.read_new()
    newest = lane.store.newest_seq()
    _wake(lane)
    assert "backlog prompt 5" in gate.prompts[0] and "backlog prompt 0" not in gate.prompts[0]
    [request, *_] = reader.seen
    shown = "\n".join(getattr(p, "content", "") for p in request[0][-1].parts
                      if isinstance(getattr(p, "content", None), str))
    assert "backlog prompt 5" in shown and "backlog prompt 0" not in shown
    assert lane.cursor() == newest


def test_the_gate_reads_the_readers_job_and_its_own_line():
    text = reader_gate.instructions(rl.read_session_text())
    assert text.startswith(rl.read_session_text()), "same WHEN TO LOOK, and a prefix that caches"
    assert reader_gate.GATE_INSTRUCTIONS == body("gate/gate-instructions.NEW.md")
    field = reader_gate.GateVerdict.model_fields
    assert (f"{reader_gate.GateVerdict.__doc__.strip()}\n\nlook: {field['look'].description}\n"
            f"why: {field['why'].description}") == body("gate/final_result.NEW.md")


def test_the_server_sets_the_mode_and_the_environment_wins(monkeypatch):
    monkeypatch.delenv(model_mod.ENV_READER_GATE, raising=False)
    monkeypatch.setattr(model_mod, "_PUSHED", {})
    assert model_mod.reader_gate_mode() == model_mod.GateMode.OFF
    model_mod.remember_pushed_settings({"x-probe-reader-gate": "shadow"})
    assert model_mod.reader_gate_mode() == model_mod.GateMode.SHADOW
    model_mod.remember_pushed_settings({"x-probe-reader-gate": "maybe"})
    assert model_mod.reader_gate_mode() == model_mod.GateMode.SHADOW, "a malformed value keeps the last good one"
    monkeypatch.setenv(model_mod.ENV_READER_GATE, "off")
    assert model_mod.reader_gate_mode() == model_mod.GateMode.OFF


def test_prompt_wakes_stay_on_unless_a_hint_serves_and_the_server_agrees(monkeypatch):
    """`x-probe-reader-prompt-wake` (on | off) from the server, honoured only
    while a Probe hint serves this session (`hints_live`); an older server sends
    none, which is ON. The environment wins over both."""
    live = [True]
    monkeypatch.setattr(model_mod, "hints_live", lambda now=None: live[0])
    monkeypatch.delenv(model_mod.ENV_READER_PROMPT_WAKE, raising=False)
    monkeypatch.setattr(model_mod, "_PUSHED", {})
    assert model_mod.reader_prompt_wake() is True
    model_mod.remember_pushed_settings({})
    assert model_mod.reader_prompt_wake() is True, "no header: on"
    model_mod.remember_pushed_settings({"x-probe-reader-prompt-wake": "OFF "})
    assert model_mod.reader_prompt_wake() is False
    live[0] = False
    assert model_mod.reader_prompt_wake() is True, "no hint serves the session now: the reader wakes"
    live[0] = True
    model_mod.remember_pushed_settings({"x-probe-reader-prompt-wake": "sometimes"})
    assert model_mod.reader_prompt_wake() is False, "a malformed value keeps the last good one"
    monkeypatch.setenv(model_mod.ENV_READER_PROMPT_WAKE, "on")
    assert model_mod.reader_prompt_wake() is True
    monkeypatch.setenv(model_mod.ENV_READER_PROMPT_WAKE, "maybe")
    assert model_mod.reader_prompt_wake() is False, "a malformed override is no override"
    monkeypatch.delenv(model_mod.ENV_READER_PROMPT_WAKE)
    model_mod.remember_pushed_settings({"x-probe-reader-prompt-wake": "on"})
    assert model_mod.reader_prompt_wake() is True


def test_hints_are_live_while_the_lanes_marker_is_fresh(monkeypatch):
    from probe.daemon import mailbox

    monkeypatch.setattr(model_mod, "_HINTS_SID", None)
    assert model_mod.hints_live() is False, "no session bound"
    model_mod.bind_hints(SID)
    path = mailbox.hints_live_path(SID)
    assert not path.exists() and model_mod.hints_live() is False, "no marker"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    touched = path.stat().st_mtime
    assert model_mod.hints_live(touched + model_mod.HINTS_LIVE_TTL_S) is True
    assert model_mod.hints_live(touched + model_mod.HINTS_LIVE_TTL_S + 1) is False, "stale: the lane stopped"


def test_every_chat_request_says_whether_hints_serve_its_session(monkeypatch):
    """What the server answers `x-probe-reader-prompt-wake: off` to (only `on`)."""
    import httpx

    live = [True]
    monkeypatch.setattr(model_mod, "hints_live", lambda now=None: live[0])
    chat = f"https://api.example.test{model_mod.ROUTE_PREFIX}{model_mod._CHAT_PATH}"
    for value, said in ((True, "on"), (False, "off")):
        live[0] = value
        request = httpx.Request("POST", chat)
        asyncio.run(model_mod._prefer_served_model(request))
        assert request.headers[model_mod.HINTS_LIVE_HEADER] == said
    other = httpx.Request("GET", "https://api.example.test/v1/anything")
    asyncio.run(model_mod._prefer_served_model(other))
    assert model_mod.HINTS_LIVE_HEADER not in other.headers
    assert model_mod.HINTS_LIVE_HEADER == "x-probe-hints-live"


def test_the_gate_lane_sends_its_header_and_the_servers_alias(monkeypatch):
    """The server keys the gate's own slots, its no-fallback rule and its 422 on
    exactly these strings (`DaemonLane.GATE`, `chat_router.GATE_MODEL_ALIAS`)."""
    monkeypatch.delenv(model_mod.ENV_GATE_MODEL, raising=False)
    ep = model_mod.Endpoint("https://api.example.test", "k")
    built = model_mod.build(ep, model_mod.LANE_GATE)
    assert built.client.default_headers[model_mod.LANE_HEADER] == "gate"
    assert built.model_name == "gate"
    monkeypatch.setenv(model_mod.ENV_GATE_MODEL, "gpt-6-luna")
    assert model_mod.build(ep, model_mod.LANE_GATE).model_name == "gpt-6-luna"


def test_a_skip_records_what_the_gate_spent(tmp_path, mode):
    mode("on")
    gate, reader = Gate(look=False), Reader(end="")
    lane = _lane(_worker(tmp_path), reader, gate)
    assert _wake(lane).outcome == rl.Outcome.SKIPPED
    row = lane.store.db.execute("SELECT input_tokens, output_tokens FROM read_turns ORDER BY id DESC").fetchone()
    [line] = [r for r in _trace(lane) if r["type"] == "reader_gate"]
    assert row["input_tokens"] > 0 and row["input_tokens"] == line["input_tokens"]


def test_a_gate_that_failed_after_answering_still_counts_its_spend():
    """Review 10-13: responses the gate paid for before it failed (here, two that
    never called its output tool) are on the verdict, not dropped."""
    calls = []

    def prose(messages, info):
        calls.append(1)
        return ModelResponse(parts=[TextPart("I think it should look.")])

    verdict = asyncio.run(reader_gate.decide(FunctionModel(prose), "job", "events"))
    assert verdict.decision == reader_gate.Decision.ERROR and verdict.look
    assert len(calls) >= 2 and verdict.input_tokens > 0


def test_the_gate_judges_the_oldest_unread_window_and_a_skip_drops_nothing_unjudged(tmp_path, mode, monkeypatch):
    """Review 10-13: with more unread than one window, the gate reads the window
    the reader would (oldest first), so a prompt early in the backlog is put to it
    before any skip can trim it away."""
    mode("on")
    monkeypatch.setattr(rl, "READ_MAX_EVENTS", 3)
    gate, reader = Gate(look=False), Reader(end="")
    w = _worker(tmp_path)
    for n in range(4):
        _append_turn(w, f"prompt {n}")
    lane = _lane(w, reader, gate)
    first_unread = lane.store.events_after(lane.cursor(), 1)[0].seq
    _wake(lane)
    assert "sweep C for an SVM on digits" in gate.prompts[0], "the oldest unread events were judged first"
    assert lane.cursor() < first_unread or lane.store.fact(rl.GATE_SEEN) >= lane.cursor()
    judged_through = int(lane.store.fact(rl.GATE_SEEN))
    assert judged_through - first_unread + 1 == 3, "one window, and the mark moved past exactly it"


def test_in_shadow_the_gate_and_the_reader_read_the_same_events(tmp_path, mode):
    mode("shadow")
    gate, reader = Gate(look=False), Reader(end="")
    lane = _lane(_worker(tmp_path), reader, gate)
    _wake(lane)
    [line] = [r for r in _trace(lane) if r["type"] == "reader_gate"]
    start = [r for r in _trace(lane) if r["type"] == "run_start"][-1]
    assert line["events"] == start["events"]


def test_a_look_reads_every_judged_event_across_seq_gaps(tmp_path, mode, monkeypatch):
    """Review 10-13 (second pass): seq numbers have gaps (an ignored duplicate
    uses one up); the reader's window is counted in rows, not seq numbers."""
    mode("shadow")
    monkeypatch.setattr(rl, "READ_MAX_EVENTS", 3)
    gate, reader = Gate(look=True), Reader(end="")
    w = _worker(tmp_path)
    lane = _lane(w, reader, gate)
    with lane.store.tx():
        lane.store.db.execute("UPDATE events SET seq = seq * 5")
    judged = lane.new_events(lane.mark())
    assert len(judged) == 3
    assert [ev.seq for ev in lane.window_to(judged[-1].seq)] == [ev.seq for ev in judged]
