"""Swarm friction T18 (2026-10-29): the runs a writer message names are read
before it is sent.

The writer spent a model round on `probe run get` for most new runs (802 such
reads in this box's daemon stores). Now plain code takes the run ids from the
message's run events (the ones it shows first, then the rest), reads up to
`bite.PREFETCH_RUNS` of them at once in the daemon host, and appends ONE capped
block to the message -- in both bite-building paths (`bite.build`, a bite or a
conversation's fresh start; `bite.build_next`, a conversation's next message).
A read that fails is left out, unsaid; a message with no run events reads nothing.

Same seams as test_daemon_conversation.py (the model is Pydantic AI's
FunctionModel, `probe` commands go to a replay) and test_daemon_host_reads.py
(a fake API over a socket, for the in-host read itself).
"""

from __future__ import annotations

import asyncio
import dataclasses
import json

import pytest

pytest.importorskip("pydantic_ai")
pytest.importorskip("pydantic_ai_harness")

from pydantic_ai.models.function import FunctionModel  # noqa: E402

from probe.daemon import bite as bite_mod  # noqa: E402
from probe.daemon import lease, tools  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402
from probe.daemon.events import Event, Kind  # noqa: E402
from tests.test_daemon_conversation import (  # noqa: E402,F401 -- `_isolated` is an autouse fixture
    SID,
    Script,
    _append_turn,
    _isolated,
    _worker,
)

RUNS = [f"{i:08x}-1111-4222-8333-444444444444" for i in range(1, 8)]
OTHER = "99999999-1111-4222-8333-444444444444"


def _record(run: str, **over) -> dict:
    """A run as `probe run get` prints it: what the writer reads, and what it does not."""
    return {"id": run, "customer_id": "probe", "slug": f"slug-{run[:8]}", "name": "lr sweep", "description": None,
            "name_customized": False, "description_customized": True, "status": "running", "project_id": None,
            "experiment_id": None, "group_id": None, "parent_run_id": None, "parent_relation": None,
            "tags": ["sweep"], "summary_metrics": {"val_acc": 0.93}, "counts": {"spans": 1, "metrics": 2,
                                                                                 "artifacts": 0},
            "config": {"lr": 0.001}, "metadata": {"launch": {"env_names": ["NOT_FOR_THE_PROMPT"]}}, **over}


class RunsReplay:
    """`probe` against a recorded Probe: `run get <id>` answers the run, or what
    `answers[id]` says to do instead; anything else is a plain ok."""

    def __init__(self, answers: dict[str, str] | None = None) -> None:
        self.calls: list[list[str]] = []
        self.answers = answers or {}

    async def run(self, argv, op_id):
        self.calls.append(list(argv))
        if argv[:2] != ["run", "get"]:
            return 0, json.dumps({"ok": True})
        run = argv[2]
        how = self.answers.get(run, "ok")
        if how == "slow":
            await asyncio.sleep(5)
        if how == "raise":
            raise RuntimeError("the replay broke")
        if how == "error":
            return 1, "no such run"
        if how == "garbage":
            return 0, "not json"
        if how == "other":
            return 0, json.dumps(_record(OTHER))
        if how == "nested":
            return 0, "[" * 200_000 + "]" * 200_000
        if how == "none":
            return 0, None
        return 0, json.dumps(_record(run), indent=2)

    def deletion_facts(self, kind, target):
        return {"id": target, "name": target, "what": kind, "others": {}, "count": 0, "updated_at": "t"}

    def run_gets(self) -> list[str]:
        return [argv[2] for argv in self.calls if argv[:2] == ["run", "get"]]


def _run_event(w, run: str, event: str = "run started", **fields) -> None:
    """The SDK's message as capture stores it (`worker._describe_sdk`)."""
    message = {"event": event, "session_id": SID, "run_id": run, **fields}
    with w.store.tx():
        w.store.add([Event(kind=Kind.RUN_EVENT, stream="sdk", offset=w.store.next_offset(),
                           text=worker_mod._describe_sdk(message))])


def _stored(text: str):
    return bite_mod.StoredEvent(seq=1, event_id="sdk:1:0", stream="sdk", kind=Kind.RUN_EVENT, turn=1, ts=None,
                                noticed=0.0, text=text, tool=None, call_id=None, command=None, is_error=False,
                                side_file=None, chars=len(text), bite=None, offset=1)


def _sent(script: Script, call: int = 0) -> str:
    """The user prompt of the model's `call`-th request: the message the writer read."""
    for part in script.seen[call][0][-1].parts:
        content = getattr(part, "content", None)
        if isinstance(content, str) and bite_mod.DIVIDER in content:
            return content
    raise AssertionError("no message with new events")


def _block(*runs: str) -> str:
    return bite_mod.runs_block([_record(r) for r in runs])


# ---------------------------------------------------------------------------
# Which runs: the run events' own run ids.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("message, named", [
    ({"event": "run started", "run_id": RUNS[0], "name": "a"}, RUNS[0]),
    ({"event": "run ended", "run_id": RUNS[0], "status": "completed"}, RUNS[0]),
    ({"event": "run started", "run_id": RUNS[0].upper()}, RUNS[0]),
    # A config past the 900-character cut: the JSON does not parse, its first key still does.
    ({"event": "run started", "config": {f"k{i}": "v" * 40 for i in range(40)}, "run_id": RUNS[0]}, RUNS[0]),
    # The run's parent, or a run id inside a description or a config, is not the run.
    ({"event": "run started", "parent_run_id": RUNS[1], "description": f'"run_id": "{RUNS[2]}"'}, None),
    ({"event": "run started", "run_id": "r-1"}, None),
    ({"event": "run started", "run_id": "--help"}, None),
    ({"event": "run started", "run_id": 7}, None),
])
def test_a_run_event_names_the_run_its_message_names(message, named):
    text = worker_mod._describe_sdk({"session_id": SID, **message})
    assert len(text) <= len(message["event"]) + 2 + 900
    if "config" in message:
        assert text.startswith(f'run started: {{"run_id": "{RUNS[0]}"'), "first, so the cut never takes it"
    assert bite_mod.run_id_of(_stored(text)) == named


def test_only_a_run_event_names_a_run():
    text = f'run ended: {{"run_id": "{RUNS[0]}"}}'
    ev = _stored(text)
    assert bite_mod.run_id_of(ev) == RUNS[0]
    assert bite_mod.run_id_of(dataclasses.replace(ev, kind=Kind.AGENT_TEXT)) is None
    assert bite_mod.run_id_of(_stored("run ended")) is None


def test_a_planted_message_never_stops_a_message_being_built():
    """Any local process can write the socket: a body past the 900-character
    cut, or nested deeper than `json` can parse, names no run and raises nothing
    (review of #3673: a RecursionError would crash the worker on every restart)."""
    deep = "[" * 200_000
    planted = [worker_mod._describe_sdk({"event": f'x": {deep}', "run_id": RUNS[0]}), f"run started: {deep}",
               f'run started: {{"run_id": "{RUNS[0]}", "pad": "{"p" * 900}"}}']
    assert bite_mod.runs_named([_stored(text) for text in planted]) == ()


def test_a_message_reads_at_most_five_runs_first_named_first():
    events = [_stored(f'run started: {{"run_id": "{run}"}}') for run in [RUNS[2], RUNS[0], RUNS[2], *RUNS]]
    assert bite_mod.runs_named(events) == (RUNS[2], RUNS[0], RUNS[1], RUNS[3], RUNS[4])
    assert bite_mod.PREFETCH_RUNS == 5
    assert bite_mod.runs_named([]) == ()


def test_the_block_is_one_line_a_run_with_the_writers_fields_and_capped():
    from probe.cli.reads import render_json

    long = _record(RUNS[1], description="d" * 5_000)
    block = bite_mod.runs_block([_record(RUNS[0]), long])
    lines = block.split("\n")
    assert lines[0] == bite_mod.RUNS_READ
    first = json.loads(lines[1])
    assert list(first) == list(bite_mod.PREFETCH_FIELDS), "the writer's fields, in one order"
    assert "metadata" not in first and "config" not in first and "NOT_FOR_THE_PROMPT" not in block
    assert len(lines[2]) == bite_mod.PREFETCH_RUN_CHARS
    full = render_json({k: long[k] for k in bite_mod.PREFETCH_FIELDS}, pretty=False)
    assert lines[3] == bite_mod.RUN_CUT.format(n=len(full) - bite_mod.PREFETCH_RUN_CHARS, id=RUNS[1])
    assert len(lines) == 4
    # A server without a field: that field is left out, never the run.
    old = {k: v for k, v in _record(RUNS[0]).items() if k != "description_customized"}
    assert "description_customized" not in json.loads(bite_mod.runs_block([old]).split("\n")[1])
    assert bite_mod.runs_block([]) == ""


def test_the_block_is_capped_even_when_every_run_is_cut():
    runs = [_record(r, description="d" * 20_000) for r in RUNS[:bite_mod.PREFETCH_RUNS]]
    block = bite_mod.runs_block(runs)
    cut = len(bite_mod.RUN_CUT.format(n=10**6, id=RUNS[0]))
    assert block.count("more characters: probe run get") == bite_mod.PREFETCH_RUNS
    assert len(block) <= len(bite_mod.RUNS_READ) + bite_mod.PREFETCH_RUNS * (bite_mod.PREFETCH_RUN_CHARS + 2 + cut)


def test_a_cut_takes_only_free_text_never_a_lock_or_a_filing_field():
    """A long (or non-English) description is cut, never the fields the writer
    files and names by: its locks above all (review of #3673)."""
    line = bite_mod.runs_block([_record(RUNS[0], project_id=OTHER, description="説明" * 2_000)]).split("\n")[1]
    assert len(line) == bite_mod.PREFETCH_RUN_CHARS
    for kept in ('"name_customized":false', '"description_customized":true', f'"project_id":"{OTHER}"',
                 '"experiment_id":null', '"status":"running"', '"parent_run_id":null'):
        assert kept in line, kept
    assert "説明" in line, "Unicode kept, as `probe run get` prints it"


def test_the_block_is_scrubbed_like_every_read_and_escapes_display_controls():
    key = "sk-proj-" + "Ab3dE5gH7jK9mN1pQ3sT5vX7zB9dF1hJ3lN5pR7tV9xZ"
    block = bite_mod.runs_block([_record(RUNS[0], name="lr ‮sweep", description=f"uses {key} for the api")])
    assert key not in block and "<redacted" in block
    assert "‮" not in block and "\\u202e" in block


def test_both_builders_name_the_runs_of_their_new_run_events(tmp_path, monkeypatch):
    """`bite.build` and `bite.build_next` (events rendered or indexed): the runs
    shown first (`runs_ahead`), then the span's; never a run event above the
    divider, which an earlier bite showed."""
    w = _worker(tmp_path, model=None, replay=None, mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    _run_event(w, RUNS[0], "run ended", status="completed")
    first, last = bite_mod.cover(w.store)
    w.store.mark_covered(w.store.open_bite("t", first, last), last)  # RUNS[0] is context from here on
    _run_event(w, RUNS[1])
    _run_event(w, RUNS[1], "run ended", status="completed")
    _append_turn(w.session.transcript, "next")  # a new turn: the span ends before it
    w.read_new()
    _run_event(w, RUNS[2])  # past the span: shown first
    span = bite_mod.cover(w.store)
    assert [ev.kind for ev in w.store.events_between(*span)] == [Kind.RUN_EVENT, Kind.RUN_EVENT]
    for built in (bite_mod.build(w.store, trigger="t", context_line="", pending_lines=[], recent_writes=[]),
                  bite_mod.build_next(w.store, trigger="t", instructions="i"),
                  bite_mod.build_next(w.store, trigger="t", instructions="i", events_text="(indexed)", span=span)):
        assert built.runs == (RUNS[2], RUNS[1]), "the one it shows first, then the span's; never the context's"
    w.store.mark_covered(w.store.open_bite("t", *span), span[1])
    assert bite_mod.build_next(w.store, trigger="t", instructions="i").runs == (RUNS[2],)


# ---------------------------------------------------------------------------
# Read, and appended: every writer message.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("mode", ["bites", "conversation"])
def test_a_message_with_no_run_events_reads_nothing(tmp_path, monkeypatch, mode):
    script, replay = Script([("done", "nothing")]), RunsReplay()
    w = _worker(tmp_path, model=FunctionModel(script), replay=replay, mode=mode, monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert replay.run_gets() == []
    assert bite_mod.RUNS_READ.split(":")[0] not in _sent(script)


def test_a_bite_carries_the_runs_it_names(tmp_path, monkeypatch):
    """Bites mode: `bite.build`, then the block closes the prompt."""
    script, replay = Script([("done", "filed")]), RunsReplay()
    w = _worker(tmp_path, model=FunctionModel(script), replay=replay, mode="bites", monkeypatch=monkeypatch)
    w.read_new()
    _run_event(w, RUNS[0])
    _run_event(w, RUNS[0], "run ended", status="completed")
    _run_event(w, RUNS[1])
    starts: list[dict] = []
    real = w.trace.start_run
    monkeypatch.setattr(w.trace, "start_run", lambda run, **facts: (starts.append(facts), real(run, **facts)))
    assert asyncio.run(w.run_bite("run event")) is True
    assert replay.run_gets() == [RUNS[0], RUNS[1]], "each run once, nothing else first"
    assert _sent(script).endswith(f"\n\n{_block(RUNS[0], RUNS[1])}")
    assert starts[0]["layout"]["runs_read"] == "2/2"


def test_a_conversation_carries_the_runs_on_its_fresh_start_and_on_each_next_message(tmp_path, monkeypatch):
    """Conversation mode: its first message is a fresh start from disk
    (`bite.build`), the next ones `bite.build_next`; each closes with the runs
    it names. The block is only appended: the next run's request extends the
    first one, block included, unchanged (the cached prefix)."""
    first, replay = Script([("done", "filed")]), RunsReplay()
    w = _worker(tmp_path, model=FunctionModel(first), replay=replay, mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    _run_event(w, RUNS[0])
    assert asyncio.run(w.run_bite("run event")) is True
    sent = _sent(first)
    assert "The whole session so far is below." in sent, "a fresh start"
    assert sent.endswith(f"\n\n{_block(RUNS[0])}")
    _append_turn(w.session.transcript, "now the next seed")
    w.read_new()
    _run_event(w, RUNS[1])
    _run_event(w, RUNS[0], "run ended", status="completed")
    second = Script([("done", "filed")])
    w._model = FunctionModel(second)
    assert asyncio.run(w.run_bite("run event")) is True
    assert replay.run_gets() == [RUNS[0], RUNS[1], RUNS[0]]
    assert _sent(second).endswith(f"\n\n{_block(RUNS[1], RUNS[0])}")
    history = [getattr(p, "content", None) for m in second.seen[0][0][:-1] for p in m.parts]
    assert sent in history, "the first message, its block included, is in the history unchanged"


def test_a_read_that_fails_leaves_its_run_out_unsaid(tmp_path, monkeypatch, caplog):
    monkeypatch.setattr(worker_mod, "RUN_READ_TIMEOUT_S", 0.1)
    answers = {RUNS[0]: "error", RUNS[1]: "garbage", RUNS[2]: "other", RUNS[3]: "raise", RUNS[4]: "slow"}
    script, replay = Script([("done", "filed")]), RunsReplay(answers)
    w = _worker(tmp_path, model=FunctionModel(script), replay=replay, mode="bites", monkeypatch=monkeypatch)
    w.read_new()
    for run in RUNS[:5]:
        _run_event(w, run)
    with caplog.at_level("WARNING", logger="probe.daemon"):
        assert asyncio.run(w.run_bite("run event")) is True
    assert replay.run_gets() == RUNS[:5]
    sent = _sent(script)
    assert bite_mod.RUNS_READ not in sent, "no run read, no block"
    assert OTHER not in sent
    assert "not read for the writer: RuntimeError" in caplog.text
    assert "not read for the writer: TimeoutError" in caplog.text
    # One good read among them: only it is shown. An answer nested past what `json`
    # parses, or no text at all, is a failed read too, never the worker's crash.
    script, replay = Script([("done", "filed")]), RunsReplay({RUNS[0]: "error", RUNS[2]: "nested", RUNS[3]: "none"})
    w2 = _worker(tmp_path / "b", model=FunctionModel(script), replay=replay, mode="bites", monkeypatch=monkeypatch)
    w2.read_new()
    for run in RUNS[:4]:
        _run_event(w2, run)
    assert asyncio.run(w2.run_bite("run event")) is True
    assert _sent(script).endswith(f"\n\n{_block(RUNS[1])}")


@pytest.mark.parametrize("stop", ["key refused", "lease lost"])
def test_a_refused_key_or_a_lost_lease_while_reading_stops_before_any_model_call(tmp_path, monkeypatch, stop):
    """Found while the runs are read: the bite ends as the same stop found by a
    `probe` command would end it, with no model round paid for it (review of #3673)."""
    script = Script([("done", "filed")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=RunsReplay(), mode="bites", monkeypatch=monkeypatch)
    w.read_new()
    _run_event(w, RUNS[0])

    async def refused(deps, argv, op_id, timeout):
        if stop == "key refused":
            tools._mark_key_refused(deps)
            return tools.ProbeResult(1, "", f"{tools.KEY_REFUSED_LINE}\n")
        deps.stopped = "the lease is another process's"
        return None

    monkeypatch.setattr(tools, "read_in_host", refused)
    assert asyncio.run(w.run_bite("run event")) is False
    assert script.calls == 0, "no model round"
    assert w.store.db.execute("SELECT outcome FROM bites ORDER BY id DESC LIMIT 1").fetchone()[0] == stop
    assert w.probe_refused_key is (stop == "key refused")
    assert w.store.pending_run_events(), "its events stay queued"


def test_no_read_past_the_session_end_deadline(tmp_path, monkeypatch):
    script, replay = Script([("done", "filed")]), RunsReplay()
    w = _worker(tmp_path, model=FunctionModel(script), replay=replay, mode="bites", monkeypatch=monkeypatch)
    w.read_new()
    _run_event(w, RUNS[0])
    built = bite_mod.build(w.store, trigger="t", context_line="", pending_lines=[], recent_writes=[])
    w.finish_by = w.clock() - 1
    assert asyncio.run(w._read_runs(built, w.deps(None))) == 0
    assert replay.run_gets() == []


# ---------------------------------------------------------------------------
# The read itself: in the daemon host, never a process.
# ---------------------------------------------------------------------------


def test_the_read_runs_in_the_host_and_is_counted_apart(tmp_path, monkeypatch):
    from tests.test_daemon_host_reads import Backend, _deps, _seed
    from tests.served_fake_app import serve

    def no_process(*a, **k):
        raise AssertionError("a prefetched read started a process")

    monkeypatch.setattr(asyncio, "create_subprocess_exec", no_process)
    app = Backend()
    seeded = _seed(app)
    run = seeded["run"]["id"]
    with serve(app) as url:
        deps = _deps(tmp_path, url)
        result = asyncio.run(tools.read_in_host(deps, ["run", "get", run], "op", 5.0))
        assert result.code == 0 and json.loads(result.stdout)["id"] == run
        assert worker_mod._run_record(run, result)["id"] == run
        assert asyncio.run(tools.read_in_host(deps, ["run", "get", "--help"], "op", 5.0)) is None, "the CLI's"
        lease.release(SID, "a test")
        assert asyncio.run(tools.read_in_host(deps, ["run", "get", run], "op", 5.0)) is None, "not ours now"
        assert deps.stopped and not deps.key_refused
    assert deps.store.fact(tools.PROBE_READS_FACT) == {tools.PREFETCHED: {"run get": 1}}


def test_a_refused_key_on_a_read_marks_the_session_as_a_command_would(tmp_path):
    from tests.served_fake_app import serve
    from tests.test_daemon_host_reads import Backend, _deps, _seed

    app = Backend()
    run = _seed(app)["run"]["id"]
    with serve(app) as url:
        deps = _deps(tmp_path, url, token=Backend.refused_token)
        result = asyncio.run(tools.read_in_host(deps, ["run", "get", run], "op", 5.0))
    assert tools._key_refused(result)
    assert deps.key_refused and deps.stopped == "Probe refused the daemon's key"
    assert worker_mod._run_record(run, result) is None
