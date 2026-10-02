"""Daemon v2 tuning (2026-09-26): one conversation per session (T15), runs that
yield between model rounds (T2), the loop detector, MEMORY.md (T3), per-round
usage (T10) and parallel tools with sequential writes (A5).

Same seams as test_daemon_loop.py: the model is Pydantic AI's FunctionModel,
`probe` commands never reach a server, the chat log is a real file.
"""

from __future__ import annotations

import asyncio
import dataclasses
import hashlib
import json
import time
from pathlib import Path

import pytest

pytest.importorskip("pydantic_ai")
pytest.importorskip("pydantic_ai_harness")

from pydantic_ai.messages import ModelRequest, ModelResponse, TextPart, ToolCallPart  # noqa: E402
from pydantic_ai.models.function import AgentInfo, FunctionModel  # noqa: E402

from probe.daemon import agent as agent_mod  # noqa: E402
from probe.daemon import approvals as appr  # noqa: E402
from probe.daemon import bite as bite_mod  # noqa: E402
from probe.daemon import folders as folders_mod  # noqa: E402
from probe.daemon import lease, tools, usage  # noqa: E402
from probe.daemon import memory as memory_mod  # noqa: E402
from probe.daemon import store as store_mod  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402
from probe.daemon.events import Kind  # noqa: E402

SID = "11111111-2222-3333-4444-555555555555"
RUN = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
FAKE_KEY = "sk-proj-" + "Ab3dE5gH7jK9mN1pQ3sT5vX7zB9dF1hJ3lN5pR7tV9xZ"
FRESH = "The whole session so far is below."


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """No real config (so no real key), no MCP: nothing leaves the box."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.delenv("PROBE_DAEMON_KEY", raising=False)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    monkeypatch.delenv(worker_mod.ENV_MODE, raising=False)
    (tmp_path / "state" / "probe" / "sessions").mkdir(parents=True)
    _set_state("daemon")


class Replay:
    def __init__(self, delays: dict[str, float] | None = None) -> None:
        self.calls: list[list[str]] = []
        self.delays = delays or {}

    async def run(self, argv, op_id):
        await asyncio.sleep(self.delays.get(argv[-1], 0))
        self.calls.append(list(argv))
        return 0, json.dumps({"ok": True})

    def deletion_facts(self, kind, target):
        return {"id": target, "name": target, "what": kind, "others": {}, "count": 0, "updated_at": "t"}


def _set_state(state: str) -> None:
    (lease.sessions_dir() / f"{SID}.state").write_text(state)


def _line(obj: dict) -> str:
    return json.dumps(obj) + "\n"


def _transcript(tmp_path: Path) -> tuple[Path, Path]:
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
    return transcript, work


def _append_turn(transcript: Path, prompt: str) -> None:
    with transcript.open("a") as handle:
        handle.write(_line({"type": "user", "message": {"content": prompt}}))
        handle.write(_line({"type": "system", "subtype": "turn_duration", "durationMs": 5}))


def _worker(tmp_path: Path, *, model=None, replay=None, clock=time.time, mode: str | None = None,
            monkeypatch=None, sid: str = SID):
    if mode is not None:
        monkeypatch.setenv(worker_mod.ENV_MODE, mode)
    transcript, work = _transcript(tmp_path)
    return worker_mod.Worker(worker_mod.Session(sid, transcript, work, "claude_code", home=tmp_path / "home"),
                             clock=clock, replay=replay, model=model)


class Script:
    """The model: `steps` answer the main agent's calls in order (then it ends
    the run); a summary request (compaction: no output tool) gets a summary.
    Every main call's messages and info are kept."""

    def __init__(self, steps=(), summary: str = "SUMMARY: the digits SVM sweep, run tagged.") -> None:
        self.steps = list(steps)
        self.summary = summary
        self.seen: list[tuple[list, AgentInfo]] = []
        self.summaries = 0

    def __call__(self, messages, info: AgentInfo) -> ModelResponse:
        if not info.output_tools:
            self.summaries += 1
            return ModelResponse(parts=[TextPart(self.summary)])
        self.seen.append((list(messages), info))
        step = self.steps.pop(0) if self.steps else ("done", "recorded")
        if callable(step):
            step = step(messages, info)
        kind, arg = step
        if kind == "shell":
            return ModelResponse(parts=[ToolCallPart("shell", {"command": arg, "why": "t"})])
        if kind == "tool":
            name, args = arg
            return ModelResponse(parts=[ToolCallPart(name, args)])
        if kind == "parallel":
            return ModelResponse(parts=[ToolCallPart(name, args) for name, args in arg])
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {"summary": arg})])

    @property
    def calls(self) -> int:
        return len(self.seen)


def _text(message) -> str:
    out = []
    for part in message.parts:
        content = getattr(part, "content", None)
        if isinstance(content, str):
            out.append(content)
        elif isinstance(content, list):
            out += [c if isinstance(c, str) else str(getattr(c, "content", "")) for c in content]
        if isinstance(part, ToolCallPart):
            out.append(f"CALL {part.tool_name} {json.dumps(part.args) if isinstance(part.args, dict) else part.args}")
    return "\n".join(out)


def _all_text(messages) -> str:
    return "\n".join(_text(m) for m in messages)


def _live(w) -> dict:
    row = w.store.live_conversation()
    return dict(row) if row is not None else {}


# ---------------------------------------------------------------------------
# T15: one conversation per session.
# ---------------------------------------------------------------------------


def test_the_mode_is_read_from_the_environment(monkeypatch):
    monkeypatch.delenv(worker_mod.ENV_MODE, raising=False)
    assert worker_mod.daemon_mode() is worker_mod.Mode.CONVERSATION == "conversation", "the default"
    monkeypatch.setenv(worker_mod.ENV_MODE, " Bites ")
    assert worker_mod.daemon_mode() is worker_mod.Mode.BITES == "bites"
    monkeypatch.setenv(worker_mod.ENV_MODE, "chat")
    assert worker_mod.daemon_mode() is worker_mod.Mode.CONVERSATION, "an unknown mode is the default, never a crash"


def test_a_respawned_worker_resumes_the_saved_conversation_with_only_the_new_events(tmp_path, monkeypatch):
    first = Script([("shell", f"probe run tag {RUN} svm"), ("done", "tagged the run")])
    replay = Replay()
    w = _worker(tmp_path, model=FunctionModel(first), replay=replay, mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert FRESH in _text(first.seen[0][0][-1]), "the first run starts fresh from disk"
    live = _live(w)
    assert live["runs"] == 1 and live["messages"] and "sweep C for an SVM" in live["messages"]
    assert w.store.pending() == []
    # The researcher's next turn arrives; capture restarts the worker (a respawn).
    _append_turn(w.session.transcript, "NEWPROMPT: now try an RBF kernel")
    second = Script([("done", "nothing new")])
    w2 = _worker(tmp_path, model=FunctionModel(second), replay=replay, mode="conversation", monkeypatch=monkeypatch)
    w2.read_new()
    assert asyncio.run(w2.run_bite("prompt")) is True
    messages = second.seen[0][0]
    history, last = _all_text(messages[:-1]), _text(messages[-1])
    assert "sweep C for an SVM" in history and f"probe run tag {RUN} svm" in history, "the saved history is back"
    assert "NEWPROMPT" in last and bite_mod.DIVIDER in last
    assert FRESH not in last and "Earlier: turns" not in last, "a fresh bite, not the conversation's next message"
    assert "sweep C for an SVM" not in last, "old chat is not shown twice"
    live2 = _live(w2)
    assert live2["id"] == live["id"] and live2["runs"] == 2
    assert w2.store.pending() == [], "the events the run saw are covered once it succeeded"


def test_a_saved_history_that_cannot_be_read_starts_fresh_from_disk(tmp_path, monkeypatch):
    model = Script([("done", "first")])
    w = _worker(tmp_path, model=FunctionModel(model), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    broken = _live(w)["id"]
    w.store.db.execute("UPDATE conversations SET messages = ? WHERE id = ?", ('[{"kind": "nonsense"}]', broken))
    _append_turn(w.session.transcript, "another prompt")
    w.read_new()
    assert asyncio.run(w.run_bite("prompt")) is True
    rebuilt = model.seen[1][0]
    assert len(rebuilt) == 1 and FRESH in _text(rebuilt[0]), "rebuilt from disk: the window, no history"
    assert "sweep C for an SVM" in _text(rebuilt[0]) and "another prompt" in _text(rebuilt[0])
    row = w.store.db.execute("SELECT ended, end_reason FROM conversations WHERE id = ?", (broken,)).fetchone()
    assert row["ended"] is not None and "could not be read" in row["end_reason"]
    assert _live(w)["id"] != broken and _live(w)["runs"] == 1


@pytest.mark.parametrize("error, dropped", [
    ("400", True), ("422", True), ("user error", True), ("429", False), ("503", False)])
def test_a_saved_history_the_model_refuses_is_dropped_and_the_retry_starts_fresh(tmp_path, monkeypatch, error,
                                                                                 dropped):
    from pydantic_ai.exceptions import ModelHTTPError, UserError

    exc = (UserError("Processed history must end with a `ModelRequest`.") if error == "user error"
           else ModelHTTPError(int(error), "default", body={"error": {"message": "invalid turn order"}}))
    w = _worker(tmp_path, model=FunctionModel(Script([("done", "first")]), model_name="m"), replay=Replay(),
                mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    saved = _live(w)["id"]
    _append_turn(w.session.transcript, "another prompt")
    w.read_new()

    def refuse_history(messages, info):
        if len(messages) > 1:
            raise exc
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {"summary": "fresh"})])

    w._model = FunctionModel(refuse_history, model_name="m")
    assert asyncio.run(w.run_bite("prompt")) is False
    row = w.store.db.execute("SELECT ended, end_reason FROM conversations WHERE id = ?", (saved,)).fetchone()
    if not dropped:
        assert row["ended"] is None, "a rate limit or an outage says nothing about the history: it is kept"
        return
    assert row["ended"] is not None and "refused its saved history" in row["end_reason"]
    retry = Script([("done", "recorded")])
    w._model = FunctionModel(retry)
    w.next_attempt_at = 0.0
    assert asyncio.run(w.run_bite("prompt")) is True
    assert len(retry.seen[0][0]) == 1 and FRESH in _text(retry.seen[0][0][0]), "rebuilt from disk, no history"
    assert "another prompt" in _text(retry.seen[0][0][0]) and w.store.pending() == []


@pytest.mark.parametrize("changed", ["session", "job description", "model", "pydantic ai"])
def test_a_saved_conversation_resumes_only_under_what_made_it(tmp_path, monkeypatch, changed):
    import pydantic_ai

    w = _worker(tmp_path, model=FunctionModel(Script([("done", "first")]), model_name="m"), replay=Replay(),
                mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    saved = _live(w)["id"]
    _append_turn(w.session.transcript, "another prompt")
    sid, name = SID, "m"
    if changed == "session":
        sid = SID + "."  # the same store file (`store_path` keeps [A-Za-z0-9_-]) under another session id
        (lease.sessions_dir() / f"{sid}.state").write_text("daemon")
        assert store_mod.store_path(sid) == w.store.path
    elif changed == "job description":
        monkeypatch.setattr(bite_mod, "record_session_text", lambda: "a newer job description")
    elif changed == "model":
        name = "another-model"
    else:
        monkeypatch.setattr(pydantic_ai, "__version__", "9.9.9")
    nxt = Script([("done", "fresh")])
    w2 = _worker(tmp_path, model=FunctionModel(nxt, model_name=name), replay=Replay(), mode="conversation",
                 monkeypatch=monkeypatch, sid=sid)
    w2.read_new()
    assert asyncio.run(w2.run_bite("prompt")) is True
    assert len(nxt.seen[0][0]) == 1 and FRESH in _text(nxt.seen[0][0][0]), "started fresh from disk"
    row = w2.store.db.execute("SELECT ended, end_reason FROM conversations WHERE id = ?", (saved,)).fetchone()
    assert row["ended"] is not None and "fingerprint" in row["end_reason"]
    assert _live(w2)["id"] != saved and _live(w2)["fingerprint"] == w2._fingerprint()


def test_a_store_from_before_the_fingerprint_column_gains_it(tmp_path):
    import sqlite3

    path = tmp_path / "old.sqlite"
    db = sqlite3.connect(path)
    db.executescript(store_mod._SCHEMA.replace(",\n    fingerprint TEXT\n", "\n"))
    assert "fingerprint" not in {r[1] for r in db.execute("PRAGMA table_info(conversations)")}
    db.close()
    st = store_mod.Store(path)
    assert st.live_conversation() is None
    st.start_conversation("instructions", "fp")
    assert st.live_conversation()["fingerprint"] == "fp"
    store_mod.Store(path).close()  # opened again: nothing to add


def test_a_worker_in_bites_mode_ends_the_live_conversation(tmp_path, monkeypatch):
    """conversation -> bites -> conversation: the bites recorded things the old
    conversation never saw, so the session starts a fresh one."""
    w = _worker(tmp_path, model=FunctionModel(Script([("done", "first")])), replay=Replay(), mode="conversation",
                monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    old = _live(w)["id"]
    _worker(tmp_path, model=FunctionModel(Script()), replay=Replay(), mode="bites", monkeypatch=monkeypatch)
    row = w.store.db.execute("SELECT ended, end_reason FROM conversations WHERE id = ?", (old,)).fetchone()
    assert row["ended"] is not None and "bites" in row["end_reason"]
    _append_turn(w.session.transcript, "back in conversation mode")
    nxt = Script([("done", "fresh")])
    w3 = _worker(tmp_path, model=FunctionModel(nxt), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w3.read_new()
    assert asyncio.run(w3.run_bite("prompt")) is True
    assert len(nxt.seen[0][0]) == 1 and FRESH in _text(nxt.seen[0][0][0]), "not the old conversation"


def test_a_first_run_that_failed_leaves_nothing_to_resume_and_the_retry_starts_fresh(tmp_path, monkeypatch):
    def boom(messages, info):
        raise RuntimeError("provider down")

    w = _worker(tmp_path, model=FunctionModel(boom), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is False
    opened = _live(w)
    assert opened["messages"] is None and w.store.pending()
    retry = Script([("done", "recorded")])
    w._model = FunctionModel(retry)
    w.next_attempt_at = 0.0
    assert asyncio.run(w.run_bite("turn end")) is True
    assert FRESH in _text(retry.seen[0][0][-1])
    assert _live(w)["id"] == opened["id"] and _live(w)["runs"] == 1


def test_conversation_mode_has_no_per_bite_caps(tmp_path, monkeypatch):
    monkeypatch.setattr(worker_mod, "BITE_REQUESTS", 2)
    steps = [("shell", f"ls {i}") for i in range(4)] + [("done", "four looks")]
    conv = Script(list(steps))
    w = _worker(tmp_path, model=FunctionModel(conv), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True and conv.calls == 5, "a bites-mode cap of 2 requests"
    assert w.store.recent_bites(1)[0]["outcome"] == "done"


def test_a_long_conversation_run_pauses_and_the_next_bite_carries_on_with_what_arrived(tmp_path, monkeypatch):
    """No cap on work, but a run pauses after ROUNDS_BEFORE_YIELD rounds: what
    queued meanwhile gets in, and the same conversation carries on."""
    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 3)
    replay = Replay()
    w_ref = {}

    def arrive(messages, info):
        _append_turn(w_ref["w"].session.transcript, "MIDRUN-PROMPT: also try a linear kernel")
        return ("shell", f"probe run tag {RUN} second")

    first = Script([("shell", f"probe run tag {RUN} first"), arrive, ("shell", "ls LAST-BEFORE-PAUSE")]
                   + [("shell", f"ls never-{i}") for i in range(5)])
    w = _worker(tmp_path, model=FunctionModel(first), replay=replay, mode="conversation", monkeypatch=monkeypatch)
    w_ref["w"] = w
    w.read_new()
    first_events = [ev.seq for ev in w.store.pending()]
    assert asyncio.run(w.run_bite("turn end")) is True, "a pause is not a failure"
    assert first.calls == 3 and [c[-1] for c in replay.calls] == ["first", "second"]
    bite = w.store.recent_bites(1)[0]
    assert bite["outcome"] == "paused" and w.failures == 0
    assert all(ev.seq not in first_events for ev in w.store.pending()), "the events it was shown are covered"
    assert [ev.text for ev in w.store.pending()][0].startswith("MIDRUN-PROMPT")
    saved = _live(w)
    assert saved["runs"] == 1 and "LAST-BEFORE-PAUSE" in saved["messages"]
    assert w.store.fact(worker_mod.CARRY_ON) is True and w.due() is not None
    # The next bite continues the same conversation: its last round's tool results, then what arrived.
    second = Script([("done", "tagged both")])
    w._model = FunctionModel(second)
    assert asyncio.run(w.run_bite(w.due())) is True
    messages = second.seen[0][0]
    history, last = _all_text(messages[:-1]), _text(messages[-1])
    assert "ls LAST-BEFORE-PAUSE" in history and f"probe run tag {RUN} second" in history
    assert "MIDRUN-PROMPT" in last and FRESH not in last
    assert replay.calls[-1][-1] == "second", "a write that ran before the pause never runs again"
    assert _live(w)["id"] == saved["id"] and _live(w)["runs"] == 2
    assert w.store.pending() == [] and not w.store.fact(worker_mod.CARRY_ON) and w.due() is None


def test_a_paused_run_carries_on_even_when_nothing_new_arrived(tmp_path, monkeypatch):
    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 2)
    first = Script([("shell", "ls a"), ("shell", "ls b"), ("shell", "ls c")])
    w = _worker(tmp_path, model=FunctionModel(first), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True and first.calls == 2
    assert w.store.pending() == [] and w.due() == "carry on"
    second = Script([("done", "finished the plan")])
    w._model = FunctionModel(second)
    assert asyncio.run(w.run_bite("carry on")) is True
    last = _text(second.seen[0][0][-1])
    assert bite_mod.NOTHING_NEW in last and bite_mod.DIVIDER not in last
    bite = w.store.recent_bites(1)[0]
    assert bite["outcome"] == "done" and bite["first_seq"] == 0
    assert w.due() is None, "carried on: nothing is due any more"


def test_conversation_mode_without_compaction_runs_as_bites(tmp_path, monkeypatch, caplog):
    import pydantic_ai_harness.compaction as compaction

    def unavailable(*args, **kwargs):
        raise ImportError("no compaction here")

    monkeypatch.setattr(compaction, "TieredCompaction", unavailable)
    monkeypatch.setattr(compaction, "SummarizingCompaction", unavailable)
    script = Script([("done", "recorded")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    assert w.mode is worker_mod.Mode.BITES
    assert "cannot be built" in caplog.text
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert w.store.db.execute("SELECT count(*) AS n FROM conversations").fetchone()["n"] == 0


def _compacting(monkeypatch) -> None:
    """Compaction on a tiny budget: every request past the first summarizes."""
    monkeypatch.setattr(agent_mod, "CONTEXT_TOKENS", 50)
    monkeypatch.setattr(agent_mod, "KEEP_MESSAGES", 2)


def test_compaction_keeps_the_instructions_and_the_status_stays_one_call_away(tmp_path, monkeypatch):
    _compacting(monkeypatch)
    replay = Replay()
    script = Script([("shell", f"probe run tag {RUN} svm"), ("shell", "ls"), ("done", "tagged")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=replay, mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert script.summaries >= 1, "the conversation was summarized"
    after = script.seen[-1]
    messages, info = after
    everything = _all_text(messages)
    assert "Summary of previous conversation" in everything and "SUMMARY: the digits SVM sweep" in everything
    assert "sweep C for an SVM" not in everything, "the first message was compacted away"
    # The job description stays; nothing else is re-sent on every request. Plain
    # code's state of the record is one tool call away.
    assert "You are the Probe daemon" in (info.instructions or "")
    assert "<state-of-the-record>" not in everything
    tools_offered = {t.name for t in info.function_tools}
    assert tools_offered == {"shell", "read", "session"}, tools_offered
    status = w.state_of_record()
    assert "<state-of-the-record>" in status and f"probe run tag {RUN} svm" in status
    assert _live(w)["compactions"] >= 1
    # The summary call is a model round like any other: recorded, and on the device counter.
    rounds = w.store.db.execute("SELECT count(*) AS n FROM rounds").fetchone()["n"]
    assert rounds == script.calls + script.summaries


def test_after_a_compaction_the_next_message_carries_the_agent_memory_index_again(tmp_path, monkeypatch):
    """The index rides the first message, which a compaction summarises away: the
    first message after a compaction carries it again, once."""
    from probe.daemon.events import Event, Kind

    _compacting(monkeypatch)
    script = Script([("shell", f"probe run tag {RUN} svm"), ("shell", "ls"), ("done", "tagged")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    index = '<agent-memory-index path="m">WISH: no checkpoints</agent-memory-index>'
    monkeypatch.setattr(w, "memory_block", lambda index_paths=None: index)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert _live(w)["compactions"] >= 1
    w.store.add([Event(kind=Kind.AGENT_TEXT, stream="main", offset=900_000, text="NEW after the compaction")])
    _, history, built = w._next_in_conversation("turn end", None)
    assert history and built.prompt.startswith(index) and "NEW after the compaction" in built.prompt
    _, _, again = w._next_in_conversation("turn end", None)
    assert index not in again.prompt, "once per compaction, not on every message"


def test_after_n_compactions_the_next_bite_starts_fresh_from_disk(tmp_path, monkeypatch):
    _compacting(monkeypatch)
    monkeypatch.setattr(worker_mod, "COMPACTIONS_BEFORE_FRESH", 2)
    script = Script([("shell", "ls"), ("shell", "ls -a"), ("shell", "ls -l"), ("done", "looked")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    ended = w.store.db.execute("SELECT * FROM conversations ORDER BY id DESC LIMIT 1").fetchone()
    assert ended["compactions"] >= 2 and ended["ended"] is not None and "compactions" in ended["end_reason"]
    assert w.store.live_conversation() is None
    _append_turn(w.session.transcript, "the next prompt")
    w.read_new()
    nxt = Script([("done", "nothing new")])
    w._model = FunctionModel(nxt)
    assert asyncio.run(w.run_bite("prompt")) is True
    assert "Earlier: turns" in _text(nxt.seen[0][0][-1]) or FRESH in _text(nxt.seen[0][0][-1])
    assert len(nxt.seen[0][0]) == 1, "no history carried over"


# ---------------------------------------------------------------------------
# The loop detector.
# ---------------------------------------------------------------------------


def test_the_same_refusal_three_times_stops_the_run_and_resets_the_conversation(tmp_path, monkeypatch):
    script = Script([("shell", "probe token create")] * 10)
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    queued = [ev.seq for ev in w.store.pending()]
    conversation = _live(w).get("id")
    assert asyncio.run(w.run_bite("turn end")) is False
    assert script.calls == agent_mod.LOOP_FAILURES, "no model round after the detector tripped"
    bite = w.store.recent_bites(1)[0]
    assert bite["outcome"] == "cut short" and "loop" in bite["error"] and "refusal" in bite["error"]
    assert [ev.seq for ev in w.store.pending()] == queued, "stopped: nothing covered"
    ended = w.store.db.execute("SELECT * FROM conversations ORDER BY id DESC LIMIT 1").fetchone()
    assert ended["ended"] is not None and "loop detector" in ended["end_reason"]
    assert conversation is None or ended["id"] == conversation
    assert w.store.live_conversation() is None, "the next bite starts fresh from disk"


def test_the_same_successful_call_five_times_stops_a_bite(tmp_path, monkeypatch):
    script = Script([("shell", "ls")] * 30)
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), mode="bites", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is False
    assert script.calls == agent_mod.LOOP_REPEATS, "stopped at the fifth identical call, not the request cap"
    assert "the same `shell` call ran 5 times" in w.store.recent_bites(1)[0]["error"]


@pytest.mark.parametrize("result, verdict", [
    ("not run (block 4a1c07e2): the check failed", "refused"),
    ("tool error (OSError): boom", "refused"),
    ("not read: It reads /etc/x: outside the working folders. The reader reads only what a safe `cat` may read",
     "refused"),
    ("[exit 1]\nerror: 422", "failed"),
    ("[auto-approved: bypass mode · exit 2]\nno", "failed"),
    ("[timed out]\n", "failed"),
    ("[exit 0]\nok", "ok"),
    ("held for the researcher (request 7f3) - `make` isn't on the safe list. It runs if they say yes", "ok"),
    ({"rows": []}, "ok"),
])
def test_what_counts_as_a_refusal_or_a_failure(result, verdict):
    assert agent_mod.outcome(result) is agent_mod.Verdict(verdict)


def test_the_detector_counts_the_same_refusal_whatever_its_block_id():
    det = agent_mod.LoopDetector()

    class Call:
        tool_name = "shell"

    for i in range(3):
        asyncio.run(det.after_tool_execute(None, call=Call(), tool_def=None, args={"command": f"probe x {i}"},
                                           result=f"not run (block {i:08x}): a credential in --notes"))
    assert det.tripped and "refusal" in det.tripped
    from pydantic_ai.exceptions import SkipToolExecution

    with pytest.raises(SkipToolExecution) as skipped:
        asyncio.run(det.before_tool_execute(None, call=Call(), tool_def=None, args={}))
    assert "stopped this run" in skipped.value.result


# ---------------------------------------------------------------------------
# T2: a run yields between model rounds.
# ---------------------------------------------------------------------------


def test_a_question_answered_during_a_run_is_settled_before_the_next_round(tmp_path, monkeypatch):
    w_ref = {}
    states = []

    def answer_no(messages, info):
        req = w_ref["w"].board.all(session_id=SID)[0]
        w_ref["w"].board.answer(req.id, req.question.no_label, channel="test")
        return ("shell", "ls")

    def look(messages, info):
        states.append(w_ref["w"].board.all(session_id=SID)[0].state)
        return ("done", "asked")

    script = Script([("shell", "python summarize.py"), answer_no, look])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), monkeypatch=monkeypatch)
    w_ref["w"] = w
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert states == [appr.DENIED], "the answer waited for the run to end"
    notices = [e.text for e in w.store.pending() if e.kind == Kind.META]
    assert any("said no" in n for n in notices)


def test_new_lines_are_read_between_rounds(tmp_path, monkeypatch):
    w_ref = {}
    found = []

    def write_line(messages, info):
        with w_ref["w"].session.transcript.open("a") as handle:
            handle.write(_line({"type": "user", "message": {"content": "MIDRUN-MARKER arrived"}}))
        return ("shell", "ls")

    def look(messages, info):
        # (A sync model function runs in a worker thread: its own connection to the store.)
        found.append(bool(store_mod.Store(w_ref["w"].store.path).search("MIDRUN-MARKER")))
        return ("done", "ok")

    script = Script([("shell", "ls -a"), write_line, look])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), monkeypatch=monkeypatch)
    w_ref["w"] = w
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert found == [True]
    assert [e.text for e in w.store.pending()] == ["MIDRUN-MARKER arrived"], "queued for the next bite, not covered"


def test_the_switch_moving_mid_run_stops_it_at_the_next_round(tmp_path, monkeypatch):
    def flip(messages, info):
        _set_state("full")
        return ("shell", "ls")

    script = Script([("shell", "ls"), flip] + [("shell", "ls -a")] * 5)
    w = _worker(tmp_path, model=FunctionModel(script), monkeypatch=monkeypatch)
    assert w._renew()
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is False
    assert script.calls == 2, "the model was called again after the switch moved"
    assert w.store.recent_bites(1)[0]["outcome"] == "lease lost" and w.store.pending()


def test_a_run_going_when_the_session_ends_stops_at_the_finish_deadline(tmp_path, monkeypatch):
    now = [1000.0]
    w_ref = {}

    def stop(messages, info):
        w_ref["w"].stopping = True  # SIGTERM
        return ("shell", "ls")

    def later(messages, info):
        now[0] += worker_mod.FINISH_CAP_S + 1
        return ("shell", "ls -a")

    script = Script([stop, later] + [("shell", "ls -l")] * 5)
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), clock=lambda: now[0],
                monkeypatch=monkeypatch)
    w_ref["w"] = w
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is False
    assert script.calls == 2 and w.finish_by is not None
    assert w.store.recent_bites(1)[0]["outcome"] == "stopped: session end"
    assert asyncio.run(w.tick()) == 0, "past the deadline the worker leaves"


def test_no_device_fuse_stops_a_run_between_rounds(tmp_path, monkeypatch):
    """No device fuse (Richard 2026-09-28: "we dont want any limit"): a device
    far past the old 60M tokens a day still runs every round of a bite."""
    store_mod.add_device_tokens(10**12)
    script = Script([("shell", "ls"), ("shell", "ls -a"), ("done", "ok")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert script.calls == 3
    assert w.store.recent_bites(1)[0]["outcome"] == "done" and w.released_reason is None
    assert not hasattr(worker_mod, "DEVICE_DAILY_TOKENS")


# ---------------------------------------------------------------------------
# T10: usage per model round, as it happens.
# ---------------------------------------------------------------------------


def test_every_model_round_is_recorded_as_it_arrives(tmp_path, monkeypatch):
    live = []

    def look(messages, info):
        rows = store_mod.Store(w_ref["w"].store.path).db.execute("SELECT tools FROM rounds")
        live.append((store_mod.device_tokens_today(), [json.loads(r["tools"]) for r in rows]))
        return ("done", "ok")

    w_ref = {}
    script = Script([("shell", "ls"), look])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), monkeypatch=monkeypatch)
    w_ref["w"] = w
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert live[0][0] > 0 and live[0][1] == [["shell"]], "counted during the run, not after it"
    rows = list(w.store.db.execute("SELECT * FROM rounds"))
    bite = w.store.recent_bites(1)[0]
    assert len(rows) == 2 and all(r["bite"] == bite["id"] for r in rows)
    assert sum(r["input_tokens"] for r in rows) == bite["input_tokens"]
    assert store_mod.device_tokens_today() == bite["input_tokens"] + bite["output_tokens"], "counted once"
    assert rows[0]["model"] and rows[0]["usd"] is None, "a test model has no price: tokens only"


def test_rounds_are_counted_by_the_usage_meter_alone():
    """No second, unread counter (the harness's spend capability) wraps every request."""
    caps = agent_mod._harness(agent_mod.RunState())
    assert [type(c).__name__ for c in caps if type(c).__module__.startswith("pydantic_ai_harness.spend")] == []
    assert sum(isinstance(c, agent_mod.UsageMeter) for c in caps) == 1
    assert not hasattr(usage, "spend_price")


def test_prices_are_known_for_the_two_route_models_only():
    assert usage.price_key("gemini-3.8-flash") == "gemini-3.8-flash"
    assert usage.price_key("gemini/gemini-3.8-flash") == "gemini-3.8-flash"
    assert usage.price_key("companion-claude-opus-5-5") == "claude-opus-5-5"
    assert usage.price_key("anthropic:claude-opus-5-5-20260901") == "claude-opus-5-5"
    assert usage.price_key("default") is None and usage.price_key("gpt-5") is None
    got = usage.cost("gemini-3.8-flash", input_tokens=1_000_000, cache_read_tokens=800_000, output_tokens=100_000)
    assert got == pytest.approx(0.2 * 0.75 + 0.8 * 0.075 + 0.1 * 3.75)
    assert usage.cost("claude-opus-5-5", input_tokens=1_000_000, cache_write_tokens=1_000_000) == pytest.approx(5.0)
    assert usage.cost("mystery", input_tokens=10) is None


def test_status_shows_tokens_cache_share_and_dollars_per_session(tmp_path, monkeypatch):
    from typer.testing import CliRunner

    from probe.cli import daemon_cli

    st = store_mod.Store(store_mod.store_path(SID))
    st.add_round(bite=1, model="gemini-3.8-flash", input_tokens=1_000_000, cached_tokens=800_000,
                 output_tokens=100_000, tools=["shell"], usd=0.585)
    st.close()
    other = store_mod.Store(store_mod.store_path("22222222-2222-3333-4444-555555555555"))
    other.add_round(bite=1, model="default", input_tokens=5_000, cached_tokens=0, output_tokens=100, tools=[],
                    usd=None)
    other.close()
    out = CliRunner().invoke(daemon_cli.daemon_app, ["status"]).output
    assert "since the session started: 1,000,000 tokens in (80% cached) / 100,000 out, ~$0.58" in out, (
        "lifetime totals are labelled as such, never read as today's")
    assert "5,000 tokens in (none cached) / 100 out (no price known for default: tokens only)" in out
    data = json.loads(CliRunner().invoke(daemon_cli.daemon_app, ["status", "--json"]).output)
    mine = next(s for s in data["sessions"] if s["session"] == SID)
    assert mine["usage"]["cached_tokens"] == 800_000 and mine["usage"]["usd"] == pytest.approx(0.585)


# ---------------------------------------------------------------------------
# T3: the daemon keeps no memory of its own; it shows the agent's memory index.
# ---------------------------------------------------------------------------


def _agent_index(tmp_path: Path, w) -> None:
    slug = str(w.session.cwd).replace("/", "-").replace(".", "-")
    index = tmp_path / "home" / ".claude" / "projects" / slug / "memory" / "MEMORY.md"
    index.parent.mkdir(parents=True)
    index.write_text(f"- [Sweep notes](sweep.md) — AGENT-INDEX-LINE\n- token {FAKE_KEY}\n")


def test_conversation_mode_shows_the_agent_memory_index_once_in_its_first_message(tmp_path, monkeypatch):
    """Nothing rides every request's end: the agent memory index is in the
    conversation's first message (a cached prefix from then on), later messages
    carry only what is new, and the daemon shows no memory of its own."""
    script = Script([("shell", "ls"), ("done", "ok")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    _agent_index(tmp_path, w)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    first = _text(script.seen[0][0][0])
    assert "AGENT-INDEX-LINE" in first and "<agent-memory-index" in first and FAKE_KEY not in first
    for messages, _ in script.seen:
        assert _text(messages[0]) == first, "the first message never changes"
        assert "<agent-memory-index" not in _all_text(messages[1:]), "no index after the first message"
        assert "<daemon-memory" not in _all_text(messages) and "nothing is remembered" not in _all_text(messages)
    _append_turn(w.session.transcript, "LATER-PROMPT")
    w.read_new()
    nxt = Script([("done", "more")])
    w._model = FunctionModel(nxt)
    assert asyncio.run(w.run_bite("prompt")) is True
    last = _text(nxt.seen[0][0][-1])
    assert "LATER-PROMPT" in last and "<agent-memory-index" not in last and "Not recorded yet" not in last


def test_bites_mode_shows_the_agent_memory_index_once_in_the_cached_prompt(tmp_path, monkeypatch):
    """~3.5K tokens of memory rode every round's uncached tail: in bites mode the
    agent memory index closes the bite's prompt, which every round after the
    first reads from cache."""
    script = Script([("shell", "ls"), ("shell", "ls -a"), ("done", "ok")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), monkeypatch=monkeypatch)
    _agent_index(tmp_path, w)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    prompt = _text(script.seen[0][0][0])
    assert "AGENT-INDEX-LINE" in prompt and "<agent-memory-index" in prompt and FAKE_KEY not in prompt
    assert "<daemon-memory" not in prompt
    assert prompt.index("# Not recorded yet") < prompt.index("<agent-memory-index"), "after what changes every bite"
    for messages, _ in script.seen[1:]:
        assert _text(messages[0]) == prompt, "the same prompt: a cached prefix"
        later = _all_text(messages[1:])
        assert "<agent-memory-index" not in later and "AGENT-INDEX-LINE" not in later, "no per-round tail"


def test_the_daemon_has_no_planning_tools():
    """A todo list re-sent at the end of requests breaks the cached prefix, and the
    bench's runs spent 6-22% of their model calls ticking one off."""
    agent = agent_mod.build_agent("instructions", model=FunctionModel(Script()))
    assert not set(agent._function_toolset.tools) & {"write_plan", "update_task_status", "read_plan"}


def test_the_status_counts_only_events_the_model_was_not_shown(tmp_path, monkeypatch):
    """`session(op=status)` is plain code's state of the record, read when the model
    asks: the events its own run was shown are not counted as unseen; one that
    arrived since is."""
    script = Script([("tool", ("session", {"op": "status"})), ("done", "ok")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert "events - 0 not shown to you yet" in _all_text(script.seen[1][0]), "its own prompt's events"
    with w.session.transcript.open("a") as handle:
        handle.write(_line({"type": "user", "message": {"content": "arrived later"}}))
    w.read_new()
    assert "events - 1 not shown to you yet" in w.state_of_record()


def test_the_state_of_the_record_comes_from_the_logbook_and_the_board(tmp_path, monkeypatch):
    w = _worker(tmp_path, replay=Replay(), monkeypatch=monkeypatch)
    st = w.store
    bite = st.open_bite("t", None, None)
    st.log_write(bite=bite, op_id="1", argv=["probe", "run", "move", RUN, "--to", "svm-sweep"], head="run move",
                 status="ran")
    st.log_write(bite=bite, op_id="2", argv=["probe", "run", "move", RUN, "--to", "svm-c"], head="run move",
                 status="ran")
    st.log_write(bite=bite, op_id="3", argv=["probe", "notes", "push", "--experiment", "svm-c"],
                 head="notes push", status="failed", reason="422")
    w.board.hold(policy="shell.unsafe_command", session_id=SID, facts={"command": "python x.py", "cwd": "/w"},
                 held={"kind": "shell", "command": "python x.py", "cwd": "/w", "op_id": "o"}, bypass=False)
    state = w.state_of_record()
    assert f"probe run move {RUN} --to svm-c" in state
    assert "--to svm-sweep" not in state, "one line per command and target: the latest"
    assert "failed: probe notes push --experiment svm-c" in state and "python x.py" in state


# ---------------------------------------------------------------------------
# A5: reads in parallel, writes one at a time in order; the read tool.
# ---------------------------------------------------------------------------


def test_write_tools_run_one_at_a_time_in_the_order_called(tmp_path, monkeypatch):
    replay = Replay(delays={"first": 0.3, "second": 0.0})
    script = Script([("parallel", [("shell", {"command": f"probe run tag {RUN} first", "why": "t"}),
                                   ("shell", {"command": f"probe run tag {RUN} second", "why": "t"})]),
                     ("done", "tagged")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=replay, monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert [c[-1] for c in replay.calls] == ["first", "second"], "the writes overlapped"


def test_reads_are_parallel_and_the_read_tool_calls_the_reader(tmp_path, monkeypatch):
    seen = []
    both: dict = {}

    async def read_file(deps, path: str, offset: int | None = None, limit: int | None = None) -> str:
        """A stand-in for `tools.read_file` that returns only once the other read has
        started too: run one after the other, the first gives up waiting."""
        seen.append((deps.session_id, path, offset, limit))
        started = both.setdefault("event", asyncio.Event())
        if len(seen) == 2:
            started.set()
        try:
            await asyncio.wait_for(started.wait(), 2.0)
        except TimeoutError:
            return f"{path} was read alone: the other read had not started"
        return f"contents of {path}"

    monkeypatch.setattr(tools, "read_file", read_file, raising=False)
    monkeypatch.setattr(tools, "WRITE_TOOLS", frozenset({"shell"}), raising=False)
    agent = agent_mod.build_agent("instructions", model=FunctionModel(Script()))
    defs = agent._function_toolset.tools
    assert defs["shell"].sequential is True
    assert not defs["read"].sequential and not defs["session"].sequential
    script = Script([("parallel", [("read", {"path": "a.csv"}), ("read", {"path": "b.py", "offset": 3, "limit": 9})]),
                     ("done", "read")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert sorted(seen) == [(SID, "a.csv", None, None), (SID, "b.py", 3, 9)]
    returned = _all_text(script.seen[1][0])
    assert "read alone" not in returned, "the reads ran one after the other"
    assert "contents of a.csv" in returned and "contents of b.py" in returned


def test_the_shell_is_the_one_write_tool():
    assert agent_mod.write_tools() == tools.WRITE_TOOLS == frozenset({"shell"})


# ---------------------------------------------------------------------------
# Bites mode still works as before, with no running note and no memory of its own.
# ---------------------------------------------------------------------------


def test_bites_mode_saves_no_conversation_and_ends_with_a_summary(tmp_path, monkeypatch):
    script = Script([("done", "filed nothing new")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), mode="bites", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert w.store.db.execute("SELECT count(*) AS n FROM conversations").fetchone()["n"] == 0
    assert w.store.note() == "filed nothing new"
    first = _text(script.seen[0][0][-1])
    assert FRESH in first and "running note" not in first and "<daemon-memory" not in first
    assert all(isinstance(m, (ModelRequest, ModelResponse)) for m in script.seen[0][0])


# ---------------------------------------------------------------------------
# The real client: Pydantic AI's OpenAI chat model against a mock gateway.
# ---------------------------------------------------------------------------


def test_the_openai_client_resumes_an_append_only_history_and_records_cached_tokens(tmp_path, monkeypatch):
    """The gateway speaks OpenAI chat completions: a resumed conversation maps to
    one message list that only ever grows at its end -- every earlier request is a
    prefix of the next, so a provider's prompt cache reads it back instead of
    writing it again -- the agent memory index rides the first message only, and the cached
    share of each round's input is recorded."""
    import httpx
    from openai import AsyncOpenAI
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider

    bodies: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        bodies.append(body)
        n = len(bodies)
        if n % 2:
            call = {"name": "shell", "arguments": json.dumps({"command": "ls", "why": "look"})}
        else:
            final = next(t["function"]["name"] for t in body["tools"] if t["function"]["name"].startswith("final"))
            call = {"name": final, "arguments": json.dumps({"summary": "done"})}
        return httpx.Response(200, json={
            "id": f"r{n}", "object": "chat.completion", "created": 1, "model": "gemini-3.8-flash",
            "choices": [{"index": 0, "finish_reason": "tool_calls", "message": {
                "role": "assistant", "content": None, "tool_calls": [{"id": f"c{n}", "type": "function",
                                                                       "function": call}]}}],
            "usage": {"prompt_tokens": 1000, "completion_tokens": 50, "total_tokens": 1050,
                      "prompt_tokens_details": {"cached_tokens": 600}}})

    client = AsyncOpenAI(base_url="https://gateway.test/v1/companion", api_key="k",
                         http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)))
    model = OpenAIChatModel("default", provider=OpenAIProvider(openai_client=client))
    w = _worker(tmp_path, model=model, replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    _agent_index(tmp_path, w)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    _append_turn(w.session.transcript, "NEXT-PROMPT")
    w2 = _worker(tmp_path, model=model, replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w2.read_new()
    assert asyncio.run(w2.run_bite("prompt")) is True
    resumed = bodies[2]["messages"]
    roles = [m["role"] for m in resumed if m["role"] != "system"]
    assert roles == ["user", "assistant", "tool", "assistant", "tool", "user"]
    assert "NEXT-PROMPT" in json.dumps(resumed[-1])
    assert "agent-memory-index" not in json.dumps(resumed[-1]) and "state-of-the-record" not in json.dumps(bodies)
    assert "daemon-memory" not in json.dumps(bodies)
    first_user = next(m for m in resumed if m["role"] == "user")
    assert "agent-memory-index" in json.dumps(first_user), "the index rides the first message"
    for earlier, later in zip(bodies, bodies[1:]):
        assert later["messages"][:len(earlier["messages"])] == earlier["messages"], "a request rewrote history"
    assert "prompt_cache_breakpoint" not in json.dumps(bodies)
    rows = list(w2.store.db.execute("SELECT model, input_tokens, cached_tokens, usd FROM rounds"))
    assert len(rows) == 4 and all(r["cached_tokens"] == 600 and r["model"] == "gemini-3.8-flash" for r in rows)
    assert rows[0]["usd"] == pytest.approx(usage.cost("gemini-3.8-flash", input_tokens=1000, cache_read_tokens=600,
                                                      output_tokens=50))


def test_after_compaction_the_gateway_sees_a_user_turn_before_any_tool_call(tmp_path, monkeypatch):
    """Compaction keeps a tail that can open with the model's own tool call. On
    the wire (OpenAI chat completions, what the gateway forwards to Gemini)
    every assistant tool call must follow a user or a tool message: Gemini
    refuses one right after the system messages."""
    import httpx
    from openai import AsyncOpenAI
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider

    _compacting(monkeypatch)
    bodies: list[dict] = []
    main: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        bodies.append(body)
        names = [t["function"]["name"] for t in body.get("tools", [])]
        final = next((n for n in names if n.startswith("final")), None)
        if final is None:  # the summarizer: no tools, a text answer
            message, finish = {"role": "assistant", "content": "SUMMARY: the digits sweep."}, "stop"
        else:
            main.append(body)
            call = ({"name": "shell", "arguments": json.dumps({"command": f"ls {len(main)}", "why": "look"})}
                    if len(main) < 4 else {"name": final, "arguments": json.dumps({"summary": "done"})})
            message = {"role": "assistant", "content": None,
                       "tool_calls": [{"id": f"c{len(bodies)}", "type": "function", "function": call}]}
            finish = "tool_calls"
        return httpx.Response(200, json={
            "id": f"r{len(bodies)}", "object": "chat.completion", "created": 1, "model": "gemini-3.8-flash",
            "choices": [{"index": 0, "finish_reason": finish, "message": message}],
            "usage": {"prompt_tokens": 100, "completion_tokens": 5, "total_tokens": 105}})

    client = AsyncOpenAI(base_url="https://gateway.test/v1/companion", api_key="k",
                         http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)))
    model = OpenAIChatModel("default", provider=OpenAIProvider(openai_client=client))
    w = _worker(tmp_path, model=model, replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    compacted = [b for b in main if "Summary of previous conversation" in json.dumps(b["messages"])]
    assert len(main) == 4 and compacted, "the run was compacted"
    for body in main:
        chat = [m for m in body["messages"] if m["role"] != "system"]
        assert chat[0]["role"] == "user", [m["role"] for m in body["messages"]]
        for before, message in zip(chat, chat[1:]):
            if message["role"] == "assistant" and message.get("tool_calls"):
                assert before["role"] in ("user", "tool"), [m["role"] for m in body["messages"]]
    assert agent_mod.EARLIER_TURNS in json.dumps(compacted[-1]["messages"])
    # The saved history carries the same shape: a resumed run sends it as it is.
    saved = json.loads(_live(w)["messages"])
    assert saved[0]["kind"] == "request" and agent_mod.EARLIER_TURNS in json.dumps(saved[:3])


def test_a_paused_history_resumes_as_a_valid_request_on_the_real_client(tmp_path, monkeypatch):
    """The saved history of a paused run ends with its last tool results; the
    carry-on sends them, then the new user message: assistant -> tool -> user."""
    import httpx
    from openai import AsyncOpenAI
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider

    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 1)
    bodies: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        bodies.append(body)
        final = next(t["function"]["name"] for t in body["tools"] if t["function"]["name"].startswith("final"))
        call = ({"name": "shell", "arguments": json.dumps({"command": "ls", "why": "look"})} if len(bodies) == 1
                else {"name": final, "arguments": json.dumps({"summary": "done"})})
        return httpx.Response(200, json={
            "id": f"r{len(bodies)}", "object": "chat.completion", "created": 1, "model": "gemini-3.8-flash",
            "choices": [{"index": 0, "finish_reason": "tool_calls", "message": {
                "role": "assistant", "content": None,
                "tool_calls": [{"id": f"c{len(bodies)}", "type": "function", "function": call}]}}],
            "usage": {"prompt_tokens": 100, "completion_tokens": 5, "total_tokens": 105}})

    client = AsyncOpenAI(base_url="https://gateway.test/v1/companion", api_key="k",
                         http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)))
    model = OpenAIChatModel("default", provider=OpenAIProvider(openai_client=client))
    w = _worker(tmp_path, model=model, replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True and len(bodies) == 1
    assert w.store.recent_bites(1)[0]["outcome"] == "paused"
    assert asyncio.run(w.run_bite(w.due())) is True and len(bodies) == 2
    chat = [m for m in bodies[1]["messages"] if m["role"] != "system"]
    assert [m["role"] for m in chat[:4]] == ["user", "assistant", "tool", "user"]
    assert chat[2]["tool_call_id"] == chat[1]["tool_calls"][0]["id"] == "c1"
    assert bite_mod.NOTHING_NEW in json.dumps(chat[3:]), "a paused run carries on with only what is new"


# ---------------------------------------------------------------------------
# A thin harness: the daemon's own tools are shell, read and session. The
# daemon keeps no memory of its own, and its whole state folder stays protected.
# ---------------------------------------------------------------------------


def test_the_model_is_offered_shell_read_and_session_and_the_output_tool_only(tmp_path, monkeypatch):
    seen = {}

    def look(messages, info):
        seen["tools"] = sorted(t.name for t in info.function_tools)
        seen["output"] = [t.name for t in info.output_tools]
        return ("done", "ok")

    for mode in ("bites", "conversation"):
        script = Script([look])
        w = _worker(tmp_path / mode, model=FunctionModel(script), replay=Replay(), mode=mode, monkeypatch=monkeypatch)
        w.read_new()
        assert asyncio.run(w.run_bite("turn end")) is True
        assert seen == {"tools": ["read", "session", "shell"], "output": ["final_result"]}, (mode, seen)


def test_with_a_key_the_probe_mcp_is_the_one_other_toolset(monkeypatch):
    from pydantic_ai.capabilities.mcp import MCP

    monkeypatch.setenv("PROBE_DAEMON_MCP", "1")
    monkeypatch.setenv("PROBE_MCP_URL", "http://127.0.0.1:9/mcp")
    monkeypatch.setattr(worker_mod, "probe_env", lambda sid: {"PROBE_TOKEN": "k", "PROBE_BASE_URL": "http://x"})
    agent = agent_mod.build_agent("instructions", model=FunctionModel(Script()),
                                  state=agent_mod.RunState(conversation=True, status=lambda: "state"))
    assert set(agent._function_toolset.tools) == {"shell", "read", "session"}
    caps = agent._root_capability.capabilities
    assert [c.id for c in caps if isinstance(c, MCP)] == ["probe"]
    names = {type(c).__name__ for c in caps}
    assert not names & {"SkillsCapability", "Memory", "ToolOutputLimits"}, names


def _deps_of(tmp_path, monkeypatch, *, bypass: bool = False):
    w = _worker(tmp_path, replay=Replay(), monkeypatch=monkeypatch)
    deps = w.deps(None)
    if bypass:
        deps.bypass, deps.mode_known = True, True
    return w, deps


def _sh(deps, command: str) -> str:
    return asyncio.run(tools.shell(deps, command, "t"))


@pytest.mark.parametrize("bypass", [False, True])
def test_the_whole_state_folder_stays_refused_in_every_mode(tmp_path, monkeypatch, bypass):
    """No memory folder of its own: the daemon's state folder has no exception,
    the old memory folder's path included."""
    w, deps = _deps_of(tmp_path, monkeypatch, bypass=bypass)
    state = store_mod.state_dir()
    store = store_mod.store_path(SID)
    assert store.exists() and deps.write_dirs == folders_mod.note_dirs()
    # Where this project's MEMORY.md lived (the sha256 of its folder's path).
    old = state / "memory" / hashlib.sha256(str(w.session.cwd.resolve()).encode()).hexdigest()
    old.mkdir(parents=True)
    (old / "MEMORY.md").write_text("- an old memory\n")
    commands = [
        f"cat > {old}/MEMORY.md <<'EOF'\n- remember this\nEOF", f"cat >> {old}/MEMORY.md <<'EOF'\nmore\nEOF",
        f"cat > {state}/x.md <<'EOF'\nx\nEOF", f"cat {old}/MEMORY.md", f"rg memory {old}", f"ls {state}",
        f"cat {store}", f"cp {old}/MEMORY.md {w.session.cwd}/stolen",
    ]
    for command in commands:
        out = _sh(deps, command)
        assert out.startswith("not run") and "every mode" in out, (command, out)
    for path in (str(store), str(old / "MEMORY.md"), str(state / "device.json")):
        out = asyncio.run(tools.read_file(deps, path))
        assert out.startswith("not read") and "every mode" in out, (path, out)
    assert (old / "MEMORY.md").read_text() == "- an old memory\n" and not (state / "x.md").exists()
    assert deps.board.all() == [], "never even asked"


def test_the_daemon_has_no_memory_of_its_own():
    assert not hasattr(tools.Deps, "memory_dir") and "memory_dir" not in {f.name for f in dataclasses.fields(tools.Deps)}
    assert not [name for name in dir(memory_mod) if name in ("memory_dir", "memory_file", "read_main", "capability")]
    assert "<<'EOF'" not in agent_mod.SHELL_DESCRIPTION and "memory" not in agent_mod.READ_DESCRIPTION
    job = bite_mod.record_session_text()
    assert "## Your memory" not in job and "MEMORY.md" not in job and "your memory" not in job


def test_read_opens_the_skills_folder_read_only(tmp_path, monkeypatch):
    w, deps = _deps_of(tmp_path, monkeypatch)
    root = bite_mod.skills_root()
    assert root is not None and "`track-work/reference.md`" in agent_mod.READ_DESCRIPTION
    reference = root / "track-work" / "reference.md"
    first = reference.read_text().splitlines()[0]
    for path in (str(reference), "track-work/reference.md"):  # the skills name it relative to their folder
        out = asyncio.run(tools.read_file(deps, path, 1, 3))
        assert not out.startswith("not read") and first in out, (path, out)
    # A file of that name in the session's folder is the session's.
    (deps.cwd / "track-work").mkdir()
    (deps.cwd / "track-work" / "reference.md").write_text("THE SESSION'S OWN\n")
    assert "THE SESSION'S OWN" in asyncio.run(tools.read_file(deps, "track-work/reference.md"))
    assert asyncio.run(tools.read_file(deps, "track-work/../../pyproject.toml")).startswith("not read")
    # Read-only: the shell writes nothing there at once, and `read` is only a reader.
    out = _sh(deps, f"cat > {root}/track-work/x.md <<'EOF'\nx\nEOF")
    assert not out.startswith("[exit 0]") and not (root / "track-work" / "x.md").exists(), out


# ---------------------------------------------------------------------------
# The shell's description is the researcher's own text.
# ---------------------------------------------------------------------------


#: The `shell` description, verbatim from the researcher's draft (tools/shell.PROPOSED.md).
SHELL_PROPOSED = (
    "Run a generic bash command in the session's working folders. \n\n"
    " - Commands are checked against a safe list: a safe command runs at once, anything else waits for the "
    "researcher's yes (in bypass mode, it runs)\n"
    " - Commands are chainable (`cd x && probe ...`, `probe ... | jq ...`)\n"
    " - `why`: one line on why you run it."
)


def test_the_shell_tool_is_described_by_the_researchers_text():
    agent = agent_mod.build_agent("instructions", model=FunctionModel(Script()))
    tool = agent._function_toolset.tools["shell"].tool_def
    assert tool.description == SHELL_PROPOSED
    assert set(tool.parameters_json_schema["properties"]) == {"command", "why"}
    assert tool.parameters_json_schema["required"] == ["command"]


def test_a_yes_that_cannot_run_says_only_why(tmp_path, monkeypatch):
    """The notice of a yes that did not run carries the reason, never a tool's
    reply with its "not run" and its stop order (a later bite would read them as
    an order for that bite)."""
    w = _worker(tmp_path, replay=Replay(), monkeypatch=monkeypatch)
    req = w.board.hold(policy="shell.unsafe_command", session_id=SID, facts={"command": "make", "cwd": "/w"},
                       held={"kind": "shell", "command": "make", "cwd": "/w", "op_id": "o"}, bypass=False)
    w.board.answer(req.id, req.question.yes_label, channel="test")

    def lost(deps, held):
        deps.stopped = "the researcher moved the switch to `off`"
        return tools.write_refusal(deps) if deps.key_refused else f"{tools.NO_LEASE} ({deps.stopped}). Nothing is lost."

    monkeypatch.setattr(tools, "held_refusal", lost)
    asyncio.run(w.settle_answers())
    notices = [e.text for e in w.store.pending() if e.kind == Kind.META]
    assert notices == [f"question {req.id} was answered yes but not run: the researcher moved the switch to `off`"]
    monkeypatch.setattr(tools, "held_refusal", lambda deps, held: f"not run: request {held.id} no longer matches")
    other = w.board.hold(policy="shell.unsafe_command", session_id=SID, facts={"command": "make x", "cwd": "/w"},
                         held={"kind": "shell", "command": "make x", "cwd": "/w", "op_id": "p"}, bypass=False)
    w.board.answer(other.id, other.question.yes_label, channel="test")
    asyncio.run(w.settle_answers())
    last = [e.text for e in w.store.pending() if e.kind == Kind.META][-1]
    assert last == f"question {other.id} was answered yes but not run: request {other.id} no longer matches"
