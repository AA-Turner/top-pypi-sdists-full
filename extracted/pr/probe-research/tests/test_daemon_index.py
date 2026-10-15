"""The writer's event indexer (daemon cost round 5, D4, D5, D11): plain code
shows the researcher's prompts (and requests, reader messages, notices) whole,
the model indexes the rest one stretch per call, an id it was not given is
removed, and any failure shows that stretch raw."""

from __future__ import annotations

import asyncio

import pytest

pytest.importorskip("pydantic_ai")
pytest.importorskip("pydantic_ai_harness")

from pydantic_ai.messages import ModelResponse, TextPart  # noqa: E402
from pydantic_ai.models.function import FunctionModel  # noqa: E402

from probe.daemon import bite as bite_mod  # noqa: E402
from probe.daemon import index as index_mod  # noqa: E402
from probe.daemon import model as model_mod  # noqa: E402
from probe.daemon.events import READER_SOURCE, REQUEST_SOURCE, Event, Kind  # noqa: E402
from tests.test_daemon_conversation import (  # noqa: E402,F401 -- `_isolated` is an autouse fixture
    RUN,
    Replay,
    Script,
    _isolated,
    _text,
    _worker,
)


def _events(w, specs) -> list:
    """Store `specs` ((kind, text, source)) as events; return them as stored."""
    base = 700_000
    w.store.add([Event(kind=k, stream="main", offset=base + i, text=t, source=s) for i, (k, t, s) in enumerate(specs)])
    rows = w.store.events_between(0, 10**9, recorded=True)
    return [ev for ev in rows if ev.offset >= base]


def _indexer(answer):
    calls = []

    def fn(messages, info):
        sent = messages[-1].parts[-1].content
        calls.append(sent)
        return ModelResponse(parts=[TextPart(answer(sent) if callable(answer) else answer)])
    return FunctionModel(fn), calls


def test_whole_events_are_never_sent_to_the_indexer(tmp_path, monkeypatch):
    w = _worker(tmp_path, model=FunctionModel(Script()), mode="conversation", monkeypatch=monkeypatch)
    evs = _events(w, [(Kind.AGENT_TEXT, "trained 3 arms", None), (Kind.PROMPT, "PROMPT-WHOLE: try lr 1e-5", None),
                      (Kind.AGENT_TEXT, "lr 1e-5 got 35.2", None), (Kind.META, "REQ: file the runs", REQUEST_SOURCE),
                      (Kind.META, "READER: prior run found", READER_SOURCE)])
    parts = index_mod.stretches(evs)
    assert [whole for whole, _ in parts] == [False, True, False, True, True]
    first_id = evs[0].event_id
    model, sent = _indexer(lambda text: f"- trained the arms ({first_id})" if first_id in text else "- an arm scored")
    out = asyncio.run(index_mod.index_events(model, evs))
    assert len(sent) == 2 and not any("PROMPT-WHOLE" in s or "REQ:" in s or "READER:" in s for s in sent)
    assert "PROMPT-WHOLE: try lr 1e-5" in out.text and "REQ: file the runs" in out.text
    assert "READER: prior run found" in out.text
    assert out.text.index("trained the arms") < out.text.index("PROMPT-WHOLE") < out.text.index("an arm scored"), \
        "in session order"
    assert index_mod.HEADER in out.text and out.calls == 2 and out.failed == 0


def test_an_id_the_indexer_was_not_given_is_removed_and_a_line_with_none_says_so():
    known = {"main:1:0", "main:2:0"}
    text, bad = index_mod.checked("- ran the sweep (main:1:0)\n- best arm (main:9:0)\n- wrote a plot\n# Results", known)
    lines = text.splitlines()
    assert lines[0] == "- ran the sweep (main:1:0)"
    assert "main:9:0" not in lines[1] and lines[1].endswith(index_mod.NO_SOURCE) and bad == 1
    assert lines[2].endswith(index_mod.NO_SOURCE), "no id at all: search first"
    assert lines[3] == "# Results", "a heading is not a claim"


@pytest.mark.parametrize("failure", ["error", "empty", "slow"])
def test_a_failed_index_call_shows_its_stretch_raw(tmp_path, monkeypatch, failure):
    w = _worker(tmp_path, model=FunctionModel(Script()), mode="conversation", monkeypatch=monkeypatch)
    evs = _events(w, [(Kind.AGENT_TEXT, "RAW-STEP: lr 5e-5 scored 34.0", None)])

    async def slow(messages, info):
        await asyncio.sleep(1)
        return ModelResponse(parts=[TextPart("- too late")])

    def broken(messages, info):
        if failure == "error":
            raise RuntimeError("422 gateway_rejected")
        return ModelResponse(parts=[TextPart("  ")])
    model = FunctionModel(slow) if failure == "slow" else FunctionModel(broken)
    out = asyncio.run(index_mod.index_events(model, evs, timeout_s=0.05))
    assert out.failed == 1 and "RAW-STEP: lr 5e-5 scored 34.0" in out.text and index_mod.HEADER not in out.text


def test_the_index_lane_sends_its_header_alias_and_no_retries(monkeypatch):
    """The server keys the index lane's deadline, its no-fallback rule and its
    writer settlement on exactly these strings (`DaemonLane.INDEX`, alias `index`)."""
    monkeypatch.delenv(model_mod.ENV_INDEX_MODEL, raising=False)
    ep = model_mod.Endpoint("https://api.example.test", "k")
    built = model_mod.build(ep, model_mod.LANE_INDEX, retries=0)
    assert built.client.default_headers[model_mod.LANE_HEADER] == "index"
    assert built.model_name == "index" and built.client.max_retries == 0
    monkeypatch.setenv(model_mod.ENV_INDEX_MODEL, "claude-haiku-5-5")
    assert model_mod.build(ep, model_mod.LANE_INDEX).model_name == "claude-haiku-5-5"


def test_an_indexed_conversation_message_shows_the_index_and_the_prompt_whole(tmp_path, monkeypatch):
    monkeypatch.setattr(model_mod, "_PUSHED", {})
    monkeypatch.setenv(model_mod.ENV_WRITER_EVENTS, "index")
    first = Script([("shell", f"probe run tag {RUN} svm"), ("done", "tagged")])
    w = _worker(tmp_path, model=FunctionModel(first), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    model, sent = _indexer("- an index line")
    w._index_model = model
    assert asyncio.run(w.run_bite("turn end")) is True
    assert sent == [], "a conversation's first message (a fresh start from disk) is shown raw"
    with w.session.transcript.open("a") as handle:  # one turn: the prompt, then the agent's answer
        handle.write('{"type": "user", "message": {"content": "NEXT-PROMPT: now an RBF kernel"}}\n')
        handle.write('{"type": "assistant", "message": {"content": [{"type": "text", "text": "RBF-RESULT 0.991"}]}}\n')
    second = Script([("done", "nothing")])
    w._model = FunctionModel(second)
    w.read_new()
    assert asyncio.run(w.run_bite("prompt")) is True
    last = _text(second.seen[0][0][-1])
    assert bite_mod.DIVIDER in last and index_mod.HEADER in last and "NEXT-PROMPT: now an RBF kernel" in last
    assert "RBF-RESULT" not in last and any("RBF-RESULT" in s for s in sent), "indexed, not shown raw"


def test_no_index_call_while_probe_refuses_the_key(tmp_path, monkeypatch):
    """Review (Codex, Medium): the run stops before the model while the key is
    refused; indexing first would bill a call on every recovery attempt."""
    monkeypatch.setattr(model_mod, "_PUSHED", {})
    monkeypatch.setenv(model_mod.ENV_WRITER_EVENTS, "index")
    w = _worker(tmp_path, model=FunctionModel(Script([("done", "x")])), replay=Replay(), mode="conversation",
                monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    model, sent = _indexer("- line")
    w._index_model = model
    with w.session.transcript.open("a") as handle:
        handle.write('{"type": "user", "message": {"content": "LATER"}}\n')
    w.read_new()
    w.probe_refused_key = True
    assert asyncio.run(w._index_new_events(None)) is None and sent == []


def test_the_message_covers_exactly_the_span_that_was_indexed(tmp_path, monkeypatch):
    """Events read in while the index call runs wait for the next run: never
    marked covered by a message that did not show them."""
    w = _worker(tmp_path, model=FunctionModel(Script()), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    span = bite_mod.cover(w.store, None)
    _events(w, [(Kind.AGENT_TEXT, "ARRIVED-DURING-INDEX", None)])
    built = bite_mod.build_next(w.store, trigger="t", instructions="i", events_text="INDEXED", span=span)
    assert (built.first_seq, built.last_seq) == span and "ARRIVED-DURING-INDEX" not in built.prompt
