"""Lean history (daemon cost round 5, D1-D3, D10, D13): the writer's saved
conversation keeps what it was sent and drops its own answers and tool traffic,
so each run's request extends the last run's first request byte for byte -- the
only prefix the model's prompt cache serves (measured 10-13).

Same seams as test_daemon_conversation.py: the model is Pydantic AI's
FunctionModel, `probe` commands never reach a server, the chat log is a real file.
"""

from __future__ import annotations

import asyncio

import pytest

pytest.importorskip("pydantic_ai")
pytest.importorskip("pydantic_ai_harness")

from pydantic_ai.messages import ModelMessagesTypeAdapter, ModelResponse, ToolReturnPart  # noqa: E402
from pydantic_ai.models.function import FunctionModel  # noqa: E402

from probe.daemon import model as model_mod  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402
from tests.test_daemon_conversation import (  # noqa: E402,F401 -- `_isolated` is an autouse fixture
    RUN,
    Replay,
    Script,
    _append_turn,
    _compacting,
    _isolated,
    _live,
    _text,
    _worker,
)


@pytest.fixture
def lean(monkeypatch):
    def set_(value: str | None) -> None:
        if value is None:
            monkeypatch.delenv(model_mod.ENV_WRITER_HISTORY, raising=False)
        else:
            monkeypatch.setenv(model_mod.ENV_WRITER_HISTORY, value)
    monkeypatch.setattr(model_mod, "_PUSHED", {})
    set_("lean")
    return set_


def _saved(w) -> list:
    return ModelMessagesTypeAdapter.validate_json(_live(w)["messages"])


def _texts(messages) -> list[str]:
    """Every part's text, in order: what goes on the wire as one message each
    (Pydantic AI may hold two user prompts in one request; the OpenAI mapping
    sends each as its own message)."""
    out = []
    for m in messages:
        for part in m.parts:
            content = getattr(part, "content", None)
            if isinstance(content, str):
                out.append(content)
    return out


def test_a_lean_run_saves_what_the_writer_was_sent_and_nothing_it_did(tmp_path, monkeypatch, lean):
    script = Script([("shell", f"probe run tag {RUN} svm"), ("done", "tagged the run")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    saved = _saved(w)
    assert not any(isinstance(m, ModelResponse) for m in saved), "no answers of its own"
    assert not any(isinstance(p, ToolReturnPart) for m in saved for p in m.parts), "no tool results"
    assert "sweep C for an SVM" in "\n".join(_texts(saved)), "what it was sent stays"


def test_each_lean_request_extends_the_last_runs_first_request(tmp_path, monkeypatch, lean):
    replay = Replay()
    first = Script([("shell", f"probe run tag {RUN} svm"), ("done", "tagged")])
    w = _worker(tmp_path, model=FunctionModel(first), replay=replay, mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    run1_first = _texts(first.seen[0][0])

    _append_turn(w.session.transcript, "NEXT: now an RBF kernel")
    second = Script([("shell", f"probe run tag {RUN} rbf"), ("done", "tagged rbf")])
    w._model = FunctionModel(second)
    w.read_new()
    assert asyncio.run(w.run_bite("prompt")) is True
    run2_first = _texts(second.seen[0][0])
    assert run2_first[:-1] == run1_first, "the request starts with the last run's first request, unchanged"
    last = run2_first[-1]
    assert last.startswith("# Your writes since your last run") and f"probe run tag {RUN} svm" in last
    assert "NEXT: now an RBF kernel" in last

    _append_turn(w.session.transcript, "THIRD: compare them")
    third = Script([("done", "nothing new")])
    w._model = FunctionModel(third)
    w.read_new()
    assert asyncio.run(w.run_bite("prompt")) is True
    run3_first = _texts(third.seen[0][0])
    assert run3_first[:-1] == run2_first, "and again: the chain holds run after run"
    assert f"probe run tag {RUN} rbf" in run3_first[-1]
    assert f"probe run tag {RUN} svm" not in run3_first[-1], "each write is listed once, in the run after it"


def test_a_paused_lean_run_keeps_its_tool_results_until_the_run_that_finishes_it(tmp_path, monkeypatch, lean):
    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 2)
    first = Script([("shell", "ls PAUSED-A"), ("shell", "ls PAUSED-B"), ("shell", "ls never")])
    w = _worker(tmp_path, model=FunctionModel(first), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True and first.calls == 2
    assert w.store.recent_bites(1)[0]["outcome"] == "paused"
    assert "PAUSED-A" in _live(w)["messages"], "a paused run's tool traffic is kept for the carry-on"
    second = Script([("done", "finished")])
    w._model = FunctionModel(second)
    history = ModelMessagesTypeAdapter.validate_json(_live(w)["messages"])
    assert worker_mod._lean_reset(history, carry_on=True) == "resume", "that carry-on cannot reuse the cache: counted"
    assert asyncio.run(w.run_bite("carry on")) is True
    assert "ls PAUSED-A" in "\n".join(_text(m) for m in second.seen[0][0]), "the carry-on saw what it had done"
    saved = _saved(w)
    assert not any(isinstance(m, ModelResponse) for m in saved), "stripped once the run completed"


def test_a_compaction_summary_survives_a_lean_save(tmp_path, monkeypatch, lean):
    _compacting(monkeypatch)
    script = Script([("shell", f"probe run tag {RUN} svm"), ("shell", "ls"), ("done", "tagged")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert script.summaries >= 1 and _live(w)["compactions"] >= 1
    assert "SUMMARY: the digits SVM sweep" in "\n".join(_texts(_saved(w))), "the summary is a system part: kept"


def test_switching_to_lean_mid_session_lists_every_write_once_and_counts_the_reset(tmp_path, monkeypatch, lean):
    lean(None)  # full history first
    first = Script([("shell", f"probe run tag {RUN} svm"), ("done", "tagged")])
    w = _worker(tmp_path, model=FunctionModel(first), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    full = ModelMessagesTypeAdapter.validate_json(_live(w)["messages"])
    assert any(isinstance(m, ModelResponse) for m in full)
    assert worker_mod._lean_reset(full, carry_on=False) == "switch"

    lean("lean")
    _append_turn(w.session.transcript, "NEXT: lean from here")
    second = Script([("done", "nothing")])
    w._model = FunctionModel(second)
    w.read_new()
    assert asyncio.run(w.run_bite("prompt")) is True
    last = _texts(second.seen[0][0])[-1]
    assert f"probe run tag {RUN} svm" in last, "the first lean run lists the session's writes so far"
    assert not any(isinstance(m, ModelResponse) for m in _saved(w))

    lean("full")  # and back: the stripped history carries on, nothing breaks
    _append_turn(w.session.transcript, "NEXT: full again")
    third = Script([("done", "nothing")])
    w._model = FunctionModel(third)
    w.read_new()
    assert asyncio.run(w.run_bite("prompt")) is True
    owed = _texts(third.seen[0][0])[-1]
    assert owed.startswith("# Your writes since your last run\n- none"), "the first full run settles what lean owed"
    _append_turn(w.session.transcript, "NEXT: full still")
    fourth = Script([("done", "nothing")])
    w._model = FunctionModel(fourth)
    w.read_new()
    assert asyncio.run(w.run_bite("prompt")) is True
    assert not _texts(fourth.seen[0][0])[-1].startswith("# Your writes"), "then full history lists no writes"


def test_the_layout_comes_from_the_server_and_the_environment_wins(monkeypatch):
    monkeypatch.delenv(model_mod.ENV_WRITER_HISTORY, raising=False)
    monkeypatch.delenv(model_mod.ENV_WRITER_EVENTS, raising=False)
    monkeypatch.setattr(model_mod, "_PUSHED", {})
    assert (model_mod.writer_history(), model_mod.writer_events()) == ("full", "raw"), "an older server: today's"
    model_mod.remember_pushed_settings({"x-probe-writer-history": "lean", "x-probe-writer-events": "index"})
    assert (model_mod.writer_history(), model_mod.writer_events()) == ("lean", "index")
    model_mod.remember_pushed_settings({"x-probe-writer-history": "thin", "x-probe-writer-events": ""})
    assert (model_mod.writer_history(), model_mod.writer_events()) == ("lean", "index"), "malformed keeps the last good"
    monkeypatch.setenv(model_mod.ENV_WRITER_HISTORY, "full")
    monkeypatch.setenv(model_mod.ENV_WRITER_EVENTS, "raw")
    assert (model_mod.writer_history(), model_mod.writer_events()) == ("full", "raw")


def test_switching_back_to_full_lists_what_the_lean_runs_wrote_once(tmp_path, monkeypatch, lean):
    """Review (Codex, High): a lean history holds none of the writer's calls, so
    the first full run after the switch must still be told what was written."""
    first = Script([("shell", f"probe run tag {RUN} lean-write"), ("done", "tagged")])
    w = _worker(tmp_path, model=FunctionModel(first), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    lean("full")
    for n, expect in ((2, True), (3, False)):
        _append_turn(w.session.transcript, f"TURN {n}")
        script = Script([("done", "nothing")])
        w._model = FunctionModel(script)
        w.read_new()
        assert asyncio.run(w.run_bite("prompt")) is True
        last = _texts(script.seen[0][0])[-1]
        assert (f"probe run tag {RUN} lean-write" in last) is expect, (n, last[:200])
    assert w.store.fact(worker_mod.LEAN_WRITES_OWED) is False, "nothing owed once a full run listed it"

    lean("lean")  # and lean again: what was listed before is never listed twice
    _append_turn(w.session.transcript, "TURN 4")
    script = Script([("done", "nothing")])
    w._model = FunctionModel(script)
    w.read_new()
    assert asyncio.run(w.run_bite("prompt")) is True
    assert f"probe run tag {RUN} lean-write" not in _texts(script.seen[0][0])[-1]


def test_a_compaction_since_the_last_lean_run_is_counted_as_a_cache_reset(tmp_path, monkeypatch, lean):
    _compacting(monkeypatch)
    first = Script([("shell", f"probe run tag {RUN} svm"), ("shell", "ls"), ("done", "tagged")])
    w = _worker(tmp_path, model=FunctionModel(first), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True and _live(w)["compactions"] >= 1
    started = []
    monkeypatch.setattr(w.trace, "start_run", lambda run, **facts: started.append(facts))
    _append_turn(w.session.transcript, "NEXT")
    w._model = FunctionModel(Script([("done", "nothing")]))
    w.read_new()
    assert asyncio.run(w.run_bite("prompt")) is True
    assert started[-1]["layout"]["cache_reset"] == "compaction"


def test_a_paused_run_settles_its_list_so_the_carry_on_does_not_repeat_it(tmp_path, monkeypatch, lean):
    """Review (Codex, P2): the carry-on extends the paused run's history, which
    already holds the list it was sent."""
    first = Script([("shell", f"probe run tag {RUN} before-pause"), ("done", "tagged")])
    w = _worker(tmp_path, model=FunctionModel(first), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 1)
    _append_turn(w.session.transcript, "TURN 2")
    second = Script([("shell", "ls a"), ("shell", "ls b")])
    w._model = FunctionModel(second)
    w.read_new()
    assert asyncio.run(w.run_bite("prompt")) is True and w.store.recent_bites(1)[0]["outcome"] == "paused"
    assert f"probe run tag {RUN} before-pause" in _texts(second.seen[0][0])[-1]
    third = Script([("done", "finished")])
    w._model = FunctionModel(third)
    assert asyncio.run(w.run_bite("carry on")) is True
    assert f"probe run tag {RUN} before-pause" not in _texts(third.seen[0][0])[-1], "listed once, not again"
