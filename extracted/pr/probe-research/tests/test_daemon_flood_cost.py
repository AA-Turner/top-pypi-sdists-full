"""Swarm friction T17-T21 (2026-10-29): the folder-check flood and the daemon's cost.

Measured on the swarm orchestrator's daemon store (10-28): file events were 78%
of all event text, and a finished run reached the writer 3.5 min late at the
median.

    T17  a file change is ONE line wherever a model sees it -- the writer's
         bites, its index lane, a turn opened, the reader (R40) -- and its
         content only through `session op=open event_id=`; a package tree or a
         cache is never walked; a folder `cd`'d into only to read is not a
         working folder; a file that changes at check after check is one
         `growing` line, then one `changed` line with the whole change (R35)
    T18  compaction counts tokens as the model route does, one bite before the size
    T19  the index lane: stretches of ~8K tokens, at most 2 calls at once
    T20  a run start or end wakes the writer within 60 s, past its least gap,
         and leads that run's message (R34)
    T21  another agent's message wakes the reader like a prompt (R17)
"""

from __future__ import annotations

import asyncio
import time

import pytest

from probe.daemon import bite as bite_mod
from probe.daemon import folders, lease, toolset, tools
from probe.daemon import model as model_mod
from probe.daemon import store as store_mod
from probe.daemon import worker as worker_mod
from probe.daemon.events import Event, Kind
from tests.test_daemon_midturn_prompt_flow import (  # noqa: F401 -- `_isolated` is an autouse fixture
    SID,
    TURN_END,
    _call,
    _isolated,
    _worker,
)

# ---------------------------------------------------------------------------
# T17 (0): one line, from one function, for every model.
# ---------------------------------------------------------------------------

BURST = 11
_TABLE = [
    "new file /w/prep.py (812 bytes)\nimport numpy as np\nX = np.load('x.npy')",
    "changed /w/train.py (1,200 -> 1,350 bytes)\n@@ -1 +1 @@\n-lr = 1e-3\n+lr = 3e-4",
    "new file /w/service.key (40 bytes): a credential-shaped name, so its content is not read",
    'new file /w/results.json (64 bytes)\n{"val_acc": 0.93, "val_loss": 0.21}',
    folders.GROWING.format(path="/w/train.log", before=100, after=900, delta=800),
    *(f"new file /w/wt/src/f{i}.ts ({1000 + i:,} bytes)\nexport const body = 'BODY{i}'" for i in range(BURST)),
]
_BODIES = ("import numpy", "lr = 3e-4", "val_acc", "BODY")


def _with_file_table(tmp_path, monkeypatch):
    """A worker whose session holds one prompt, then the file-event table."""
    monkeypatch.setenv(model_mod.ENV_WRITER_FILE_BURST, "10")
    w = _worker(tmp_path, [])
    base = w.store.next_offset()
    with w.store.tx():
        w.store.add([Event(kind=Kind.FILE_CHANGE, stream=bite_mod.FOLDERS_STREAM, offset=base + i, text=text)
                     for i, text in enumerate(_TABLE)])
    events = [ev for ev in w.store.events_between(1) if ev.kind == Kind.FILE_CHANGE]
    assert len(events) == len(_TABLE)
    return w, events


def _lines(events) -> list[str]:
    """What every model must read for `events`: one line each, the burst one list."""
    lines = [bite_mod.render(ev) for ev in events[:5]]
    lines.append(bite_mod._burst_text(events[5:]))
    return lines


def test_one_file_event_table_reads_the_same_for_reader_writer_index_and_turn_open(tmp_path, monkeypatch):
    pytest.importorskip("pydantic_ai")
    from pydantic_ai.messages import ModelResponse, TextPart
    from pydantic_ai.models.function import FunctionModel

    from probe.daemon import index as index_mod
    from probe.daemon import reader_lane

    w, events = _with_file_table(tmp_path, monkeypatch)
    lines = _lines(events)
    new, changed, secret, results, growing = lines[:5]
    assert new == (f"[file changed · {events[0].event_id}] " + toolset.pick(*bite_mod.MORE_LINES).format(
        head="new file /w/prep.py (812 bytes)", n=2, id=events[0].event_id))
    assert changed == (f"[file changed · {events[1].event_id}] " + toolset.pick(*bite_mod.MORE_LINES).format(
        head="changed /w/train.py (1,200 -> 1,350 bytes)", n=3, id=events[1].event_id))
    assert secret == f"[file changed · {events[2].event_id}] {_TABLE[2]}"
    assert f"new file /w/results.json (64 bytes) · {bite_mod.RESULTS_FLAG} · 1 more lines" in results
    assert growing == f"[file changed · {events[4].event_id}] {_TABLE[4]}"
    assert lines[5].startswith(toolset.pick(*bite_mod.FILE_BURST).format(n=BURST))

    writer = bite_mod.build_next(w.store, trigger="t", instructions="i").prompt
    reader = reader_lane.ReaderLane(w, model=FunctionModel(lambda m, i: ModelResponse(parts=[]))).build_prompt(
        events, None, first=False)
    sent: list[str] = []

    def indexer(messages, info):
        sent.append(messages[-1].parts[-1].content)
        return ModelResponse(parts=[TextPart("")])  # an empty answer: the stretch goes raw

    indexed = asyncio.run(index_mod.index_events(FunctionModel(indexer), events))
    lease.renew(SID)
    opened = tools.session_open(w.deps(None), turn=events[0].turn)
    for where, text in (("writer", writer), ("reader", reader), ("index lane", sent[0]),
                        ("raw index fallback", indexed.text), ("turn open", opened)):
        for line in lines:
            assert line in text, (where, line)
        for body in _BODIES:
            assert body not in text, (where, body)
    for ev, body in zip(events, ("import numpy", "lr = 3e-4", None, "val_acc")):
        if body is not None:
            assert body in tools.session_open(w.deps(None), event_id=ev.event_id), "the open shows the content"


def test_a_results_file_in_a_burst_keeps_its_flag(monkeypatch):
    """A run's output folder is often a burst: its results file is still flagged."""
    monkeypatch.setenv(model_mod.ENV_WRITER_FILE_BURST, "2")
    texts = ["new file /w/runs/r1/config.yaml (20 bytes)\nlr: 0.001",
             'new file /w/runs/r1/metrics.json (40 bytes)\n{"test_acc": 0.981}',
             "new file /w/runs/r1/model.pt (9,000 bytes)"]
    events = [store_mod.StoredEvent(seq=i, event_id=f"folders:{i}:0", stream=bite_mod.FOLDERS_STREAM,
                                    kind=Kind.FILE_CHANGE, turn=1, ts=None, noticed=0.0, text=t, tool=None,
                                    call_id=None, command=None, is_error=False, side_file=None, chars=len(t),
                                    bite=None, offset=i) for i, t in enumerate(texts, 1)]
    [(_, listed)] = bite_mod.rendered(events)
    assert listed.splitlines()[1] == ("/w/runs/r1/: config.yaml (20 bytes) folders:1:0 · metrics.json (40 bytes) "
                                      f"folders:2:0 · {bite_mod.RESULTS_FLAG} · model.pt (9,000 bytes) folders:3:0")


def test_a_file_change_is_sized_as_its_one_line(tmp_path, monkeypatch):
    w, events = _with_file_table(tmp_path, monkeypatch)
    for ev in events:
        assert len(bite_mod.render(ev)) <= bite_mod.shown_chars(ev) < 300
    sizes = {turn: chars for turn, _, chars in w.store.shown_turn_sizes()}
    files = sum(1 for ev in w.store.events_between(1) if ev.kind == Kind.FILE_CHANGE and ev.turn == events[0].turn)
    others = sum(bite_mod.shown_chars(ev) for ev in w.store.events_between(1)
                 if ev.turn == events[0].turn and ev.kind != Kind.FILE_CHANGE)
    assert sizes[events[0].turn] == others + 200 * files, "a flat 200 a file change"


# ---------------------------------------------------------------------------
# T17 (2), (3): package trees and caches; folders only read in.
# ---------------------------------------------------------------------------


def test_a_package_tree_or_a_cache_is_never_walked(tmp_path):
    work = tmp_path / "work"
    for path in ("train.py", "plot-packages/numpy/__init__.py", "plot-packages/numpy-2.1.0.dist-info/METADATA",
                 "plot-packages/matplotlib/pyplot.py", "uv-cache/CACHEDIR.TAG", "uv-cache/archive-v0/x/y.py",
                 "src/mypkg/__init__.py", "src/mypkg.egg-info/PKG-INFO", "eggs/a.egg-info/PKG-INFO",
                 "eggs/b.egg-info/PKG-INFO", "eggs/a/mod.py"):
        (work / path).parent.mkdir(parents=True, exist_ok=True)
        (work / path).write_text("x = 1\n")
    seen = {s.path for s in folders.scan([work], {}, is_secret=lambda p: False, text_room=10_000)}
    assert seen == {str(work / p) for p in ("train.py", "src/mypkg/__init__.py", "src/mypkg.egg-info/PKG-INFO")}, \
        "one egg-info is a source tree's own (`pip install -e .`)"


@pytest.mark.parametrize("command, working", [
    ("cd {d} && git log --oneline | head -20", False),
    ("cd {d} && git grep -n delete origin/main -- 'app/*.py' | sed 's/x/y/' | head -80", False),
    ("cd {d}; grep -rn TODO src 2>/dev/null | wc -l; ls -la", False),
    ("cd {d} && git show origin/main:app/x.py | sed -n 1,60p", False),
    ("cd {d} && python train.py", True),
    ("cd {d} && git pull", True),
    ("cd {d} && sed -i 's/a/b/' cfg.yaml", True),
    ("cd {d} && grep x a.txt > found.txt", True),
    ("cd {d}", True),
    ("cd {d} && find . -name '*.pyc' -delete", True),
    # The orchestrator's own shapes (10-28): substitutions, loops, a copy written elsewhere.
    ("cd {d}; f=$(git ls-tree -r --name-only origin/main | grep -E 'x\\.py$' | head -3); echo \"$f\"; "
     "for x in $f; do git show origin/main:$x | grep -n y | head -12; done", False),
    ("cd {d}; git show origin/main:a.py > /var/tmp/sm.py; grep -n y /var/tmp/sm.py | head", False),
    ("cd {d} && git show origin/main:a.py > a.py", True),
    ("cd {d}; git fetch -q origin main; kubectl --context c -n research get pods --no-headers | awk '{{print $1}}'",
     False),
    ("cd {d} && kubectl --context c -n research delete pod x", True),
    ("cd {d} && if [ -f x ]; then cat x; fi", False),
    # Writers that look like readers (review of #3664).
    ("cd {d} && sed -Ei 's/lr=1e-3/lr=3e-4/' train.py", True),
    ("cd {d} && yq -i '.lr = 3e-4' configs/train.yaml", True),
    ("cd {d} && sort -o sorted.txt in.txt", True),
    ("cd {d} && uniq in.txt out.txt", True),
    ("cd {d} && awk -i inplace '{{print}}' f.txt", True),
])
def test_a_folder_cd_into_only_to_read_is_not_a_working_folder(tmp_path, command, working):
    home = tmp_path / "home"
    work = home / "work"
    other = home / "other-repo"
    work.mkdir(parents=True)
    other.mkdir()
    st = store_mod.Store(tmp_path / "s.sqlite")
    st.add([Event(kind=Kind.TOOL_CALL, stream="main", offset=1, tool="Bash",
                  tool_input={"command": command.format(d=other)})])
    found = folders.working_folders(st, work, home)
    assert (other.resolve() in found) is working, found


def test_sed_in_place_in_a_flag_group_is_a_write():
    assert folders.written_paths("sed -Ei 's/a/b/' train.py") == ["train.py"]
    assert folders.written_paths("sed -n 1,5p train.py") == []


def test_a_folder_read_in_once_and_worked_in_once_is_a_working_folder(tmp_path):
    home = tmp_path / "home"
    work = home / "work"
    other = home / "other-repo"
    work.mkdir(parents=True)
    other.mkdir()
    st = store_mod.Store(tmp_path / "s.sqlite")
    st.add([Event(kind=Kind.TOOL_CALL, stream="main", offset=1, tool="Bash",
                  tool_input={"command": f"cd {other} && git log | head"}),
            Event(kind=Kind.TOOL_CALL, stream="main", offset=2, tool="Bash",
                  tool_input={"command": f"cd {other} && ls && cd {work} && make"})])
    assert folders.working_folders(st, work, home) == [work.resolve()]
    st.add([Event(kind=Kind.TOOL_CALL, stream="main", offset=3, tool="Bash",
                  tool_input={"command": f"cd {other} && make test"})])
    assert other.resolve() in folders.working_folders(st, work, home)


# ---------------------------------------------------------------------------
# T17 (4): a growing file is one line, then one changed line (R35).
# ---------------------------------------------------------------------------


def _checking(tmp_path):
    home = tmp_path / "home"
    work = home / "work"
    work.mkdir(parents=True)
    st = store_mod.Store(tmp_path / "s.sqlite")
    asyncio.run(folders.baseline(st, work, home))
    seen: list[int] = []

    def check(**kw) -> list[str]:
        folders.check(st, work, home, workdirs=[work], **kw)
        new = [ev for ev in st.events_between(1) if ev.seq not in seen]
        seen.extend(ev.seq for ev in new)
        return [ev.text for ev in new]

    return st, work, check


def test_a_growing_log_is_one_line_then_one_changed_line_with_the_whole_change(tmp_path):
    st, work, check = _checking(tmp_path)
    log = work / "train.log"
    steps = [f"step {i} loss 0.{9 - i}\n" for i in range(1, 9)]
    log.write_text(steps[0])
    [first] = check()
    assert first.startswith(f"new file {log} (16 bytes)")
    log.write_text("".join(steps[:2]))
    [grew] = check()
    assert grew == folders.GROWING.format(path=log, before=16, after=32, delta=16)
    for n in range(3, 9):
        log.write_text("".join(steps[:n]))
        assert check() == [], "nothing while it keeps growing"
    assert check() == [], "quiet for one check"
    [settled] = check()
    head, _, diff = settled.partition("\n")
    assert head == f"changed {log} (16 -> {log.stat().st_size:,} bytes)", "from before it started growing"
    assert "+step 2 loss" in diff and "+step 8 loss" in diff and "+step 1 loss" not in diff
    assert not folders.growing(st)
    [ev] = [e for e in st.events_between(1) if e.text == settled]
    assert bite_mod.render(ev).startswith(f"[file changed · {ev.event_id}] {head} · ")


def test_a_code_file_edited_twice_in_a_row_keeps_both_edits(tmp_path):
    """O7: the last state of an edited file is never lost to the growing rule."""
    st, work, check = _checking(tmp_path)
    code = work / "train.py"
    code.write_text("lr = 1e-3\nepochs = 10\n")
    check()
    check()
    code.write_text("lr = 3e-4\nepochs = 10\n")
    [edit] = check()
    assert edit.startswith(f"changed {code}") and "+lr = 3e-4" in edit
    code.write_text("lr = 3e-4\nepochs = 20\n")
    [grew] = check()
    assert grew.startswith(f"growing {code}")
    assert check() == []
    [last] = check()
    assert last.startswith(f"changed {code}") and "-epochs = 10" in last and "+epochs = 20" in last


def test_the_session_end_does_not_wait_for_a_growing_file(tmp_path):
    st, work, check = _checking(tmp_path)
    status = work / "status.txt"
    status.write_text("a\n")
    check()
    status.write_text("a\nb\n")
    check()
    status.write_text("a\nb\nc\n")
    [last] = check(flush=True)
    assert last.startswith(f"changed {status} (2 -> 6 bytes)") and "+b" in last and "+c" in last
    assert not folders.growing(st)


def test_a_change_made_in_read_only_ends_a_growing_file_unannounced(tmp_path):
    st, work, check = _checking(tmp_path)
    log = work / "out.log"
    log.write_text("1\n")
    check()
    log.write_text("1\n2\n")
    check()
    log.write_text("1\n2\nsecret plan\n")
    assert check(emit=False) == []
    assert not folders.growing(st) and check() == [] and check() == []
    assert not any("secret plan" in ev.text for ev in st.events_between(1))


def test_a_growing_file_excluded_meanwhile_gets_no_changed_line(tmp_path):
    """A `.probe.config` exclusion added while a file grows: its owed line (and
    the diff it would carry) is dropped, never emitted (review of #3664)."""
    st, work, check = _checking(tmp_path)
    log = work / "private.log"
    log.write_text("a\n")
    check()
    log.write_text("a\nb\n")
    check()
    hidden = lambda path: path.endswith("private.log")  # noqa: E731
    assert check(excluded=hidden) == [] and check(excluded=hidden) == []
    assert check(excluded=hidden, flush=True) == [] and not folders.growing(st)


def test_a_growing_files_base_text_counts_toward_the_stored_text(tmp_path):
    st, work, check = _checking(tmp_path)
    log = work / "a.log"
    log.write_text("x" * 100)
    check()
    before = st.stored_text_bytes()
    log.write_text("x" * 150)
    check()
    assert st.stored_text_bytes() == before + 50 + 100, "the latest text, and the text it grew from"
    log.write_text("x" * 160)
    check()
    check()
    check()
    assert st.stored_text_bytes() == 160


def test_the_worker_flushes_a_growing_file_before_it_stops(tmp_path, monkeypatch):
    w = _worker(tmp_path, _call(1) + [TURN_END])
    work = w.session.cwd
    asyncio.run(folders.baseline(w.store, work, w.session.home))
    log = work / "train.log"
    log.write_text("1\n")
    folders.check(w.store, work, w.session.home)
    log.write_text("1\n2\n")
    folders.check(w.store, work, w.session.home)
    assert folders.growing(w.store)
    first, last = bite_mod.cover(w.store)
    w.store.mark_covered(w.store.open_bite("t", first, last), w.store.newest_seq())
    w.stopping = True
    monkeypatch.setattr(w, "_parent_gone", lambda: False)
    assert asyncio.run(w.tick()) is None, "the owed line is made and waits for a bite"
    [owed] = w.store.pending()
    assert owed.text.startswith(f"changed {log} (2 -> 4 bytes)") and not folders.growing(w.store)


# ---------------------------------------------------------------------------
# T18: compaction one bite before the size, counted as the model route counts.
# ---------------------------------------------------------------------------


def test_the_writer_counts_tokens_as_the_route_and_compacts_a_bite_early(tmp_path):
    pytest.importorskip("pydantic_ai_harness")
    pytest.importorskip("tiktoken")
    from pydantic_ai.messages import ModelRequest, UserPromptPart
    from pydantic_ai_harness.compaction import estimate_context_tokens

    from probe.daemon import agent as agent_mod
    from probe.mcp.budget import count_tokens

    w = _worker(tmp_path, [])
    state = w._run_state(None, conversation=True)
    assert state.compact_room == agent_mod.COMPACT_ROOM_TOKENS == bite_mod.NEW_SHOWN_TOKENS
    assert state.tokenizer is agent_mod.server_tokenizer() is not None
    assert w._run_state(None, conversation=False).tokenizer is None, "bites mode never compacts"
    # A bite of file paths and diffs: dense in tokens (the 10-28 422s).
    dense = "\n".join(f"[file changed · folders:{i}:0] changed /home/r/grok-swarm/workers/a{i % 9}/status-{i}.jsonl "
                      f"({i:,} -> {i + 17:,} bytes) · 3 more lines: session op=open event_id=folders:{i}:0"
                      for i in range(2_000))
    messages = [ModelRequest(parts=[UserPromptPart(dense)])]
    truth = count_tokens(dense)
    counted = estimate_context_tokens(messages, state.tokenizer)
    assert abs(counted - truth) <= truth * 0.05, (counted, truth)
    assert estimate_context_tokens(messages) < truth * 0.95, "4 characters a token reads it low"


@pytest.mark.parametrize("room, compacts", [(0, False), (2_000, True)])
def test_a_history_within_the_room_of_its_size_compacts(room, compacts):
    pytest.importorskip("pydantic_ai_harness")
    from probe.daemon import agent as agent_mod
    from tests.test_daemon_compaction_budget import SIZE, Seen, _exchange, _run, _words

    history = [m for i in range(6) for m in _exchange(i, 1_400)]  # ~8.4K of a 10K size
    state, seen = agent_mod.RunState(conversation=True, context_tokens=SIZE, compact_room=room), Seen()
    _run(seen, state, _words(200, "new"), history)
    assert (state.compactions == 1) is compacts


def test_the_room_never_reaches_the_target():
    """A room past half the way down to COMPACT_TO would compact on every request."""
    pytest.importorskip("pydantic_ai")
    from probe.daemon import agent as agent_mod

    assert agent_mod.COMPACT_ROOM_TOKENS < 250_000 * (1 - agent_mod.COMPACT_TO) / 2


# ---------------------------------------------------------------------------
# T19: the index lane's stretches and calls.
# ---------------------------------------------------------------------------


def test_an_index_stretch_is_cut_at_about_8k_tokens_and_two_calls_run_at_once(tmp_path, monkeypatch):
    pytest.importorskip("pydantic_ai")
    from pydantic_ai.messages import ModelResponse, TextPart
    from pydantic_ai.models.function import FunctionModel

    from probe.daemon import index as index_mod

    w = _worker(tmp_path, [])
    base = w.store.next_offset()
    with w.store.tx():
        w.store.add([Event(kind=Kind.AGENT_TEXT, stream="main", offset=base + i, text=f"step {i} " + "w" * 3_000)
                     for i in range(60)])
    events = [ev for ev in w.store.events_between(1) if ev.kind == Kind.AGENT_TEXT]
    chunks = index_mod.chunks(events)
    assert len(chunks) >= 5
    limit = index_mod.STRETCH_TOKENS * bite_mod.CHARS_PER_TOKEN
    assert all(sum(len(t) for _, t in c) <= limit for c in chunks)
    assert [ev for c in chunks for group, _ in c for ev in group] == events, "in order, none lost"
    running, most, sent = [0], [0], []

    async def indexer(messages, info):
        running[0] += 1
        most[0] = max(most[0], running[0])
        await asyncio.sleep(0.01)
        running[0] -= 1
        text = messages[-1].parts[-1].content
        sent.append(text)
        first = text.split("]", 1)[0].rsplit(" · ", 1)[-1]
        return ModelResponse(parts=[TextPart(f"- steps ({first})")])

    out = asyncio.run(index_mod.index_events(FunctionModel(indexer), events))
    assert most[0] == index_mod.CONCURRENT_CALLS == 2
    assert out.calls == len(chunks) == len(sent) and out.failed == 0
    assert out.text.count(toolset.pick(index_mod.HEADER, index_mod.HEADER_BASH)) == len(chunks)


# ---------------------------------------------------------------------------
# T20: a run start or end wakes the writer and leads its message.
# ---------------------------------------------------------------------------


def _run_ended(w, run_id: str = "r-1") -> None:
    with w.store.tx():
        w.store.add([Event(kind=Kind.RUN_EVENT, stream="sdk", offset=w.store.next_offset(),
                           text=f'run ended: {{"run_id": "{run_id}", "status": "completed"}}')])


def test_a_run_ending_right_after_a_writer_pass_is_filed_within_a_minute(tmp_path, monkeypatch):
    now = [1000.0]
    monkeypatch.setenv("PROBE_DAEMON_WRITER_GAP_S", "300")
    w = _worker(tmp_path, _call(1) + [TURN_END], clock=lambda: now[0])
    first, last = bite_mod.cover(w.store)
    w.store.mark_covered(w.store.open_bite("turn end", first, last), last)
    w.last_run_at = now[0]  # the writer just ran
    _run_ended(w)
    now[0] += 30
    assert w.due() is None, "at most one extra run a minute"
    now[0] += 31
    assert w.due() == worker_mod.TRIGGER_RUN, "past the 300 s gap"
    assert not w.deferrable(worker_mod.TRIGGER_RUN, w.store.pending())


def test_a_turn_end_alone_still_waits_for_the_gap(tmp_path, monkeypatch):
    now = [1000.0]
    monkeypatch.setenv("PROBE_DAEMON_WRITER_GAP_S", "300")
    w = _worker(tmp_path, _call(1) + [TURN_END], clock=lambda: now[0])
    w.last_run_at = now[0] - 90
    assert w.due() is None


def test_a_run_event_behind_a_backlog_leads_the_writers_message(tmp_path, monkeypatch):
    monkeypatch.setattr(bite_mod, "MAX_EVENTS_PER_BITE", 5)
    w = _worker(tmp_path, sum((_call(i) for i in range(1, 9)), []))
    _run_ended(w)
    [run] = w.store.pending_run_events()
    first, last = bite_mod.cover(w.store)
    assert run.seq > last, "past what one run covers"
    for built in (bite_mod.build_next(w.store, trigger="t", instructions="i"),
                  bite_mod.build(w.store, trigger="t", context_line="", pending_lines=[], recent_writes=[])):
        assert built.leads == (run.seq,)
        after = built.prompt.split(bite_mod.DIVIDER, 1)[1].lstrip("\n")
        assert after.startswith(f"{bite_mod.RUNS_AHEAD}\n{bite_mod.render(run)}\n\n"), after[:300]
    w.store.mark_covered(w.store.open_bite("t", first, last), last, built.leads)
    assert not w.store.pending_run_events()
    assert w.store.pending()[0].seq == last + 1, "the rest of the backlog waits its turn"


def test_a_lead_run_event_is_never_shown_again_by_the_next_bite(tmp_path, monkeypatch):
    """Covered as a lead, a run event inside the next bite's span is not new
    again: the writer would file the run twice (review of #3664)."""
    monkeypatch.setattr(bite_mod, "MAX_EVENTS_PER_BITE", 5)
    w = _worker(tmp_path, sum((_call(i) for i in range(1, 9)), []))
    _run_ended(w)
    with w.store.tx():
        w.store.add([Event(kind=Kind.AGENT_TEXT, stream="main", offset=w.store.next_offset(), text="next step")])
    [run] = w.store.pending_run_events()
    built = bite_mod.build_next(w.store, trigger="t", instructions="i")
    w.store.mark_covered(w.store.open_bite("t", built.first_seq, built.last_seq), built.last_seq, built.leads)
    monkeypatch.setattr(bite_mod, "MAX_EVENTS_PER_BITE", 400)
    for again in (bite_mod.build_next(w.store, trigger="t", instructions="i"),
                  bite_mod.build(w.store, trigger="t", context_line="", pending_lines=[], recent_writes=[])):
        assert again.first_seq < run.seq <= again.last_seq, "the span crosses it"
        new = again.prompt.split(bite_mod.DIVIDER, 1)[1]
        assert run.event_id not in new and "next step" in new and not again.leads


def test_a_skipped_bite_leaves_its_lead_run_events_for_the_next(tmp_path, monkeypatch):
    """A range skipped after CUT_SHORTS_BEFORE_SKIP bites is not the run event's
    fault: it leads the next bite instead of being dropped with the range."""
    pytest.importorskip("pydantic_ai")  # the skip path reads the agent's wording
    from probe.daemon import alerts

    monkeypatch.setattr(alerts, "report", lambda *a, **kw: None)
    monkeypatch.setattr(bite_mod, "MAX_EVENTS_PER_BITE", 5)
    w = _worker(tmp_path, sum((_call(i) for i in range(1, 9)), []))
    _run_ended(w)
    [run] = w.store.pending_run_events()
    built = bite_mod.build_next(w.store, trigger="t", instructions="i")
    assert built.leads == (run.seq,)
    with w.store.tx():
        w.store.set_fact("cut_short", {"first_seq": built.first_seq, "times": worker_mod.CUT_SHORTS_BEFORE_SKIP - 1})
    bite = w.store.open_bite("t", built.first_seq, built.last_seq)
    assert w._cut_short(bite, built, "too big", {}) is True
    assert w.store.pending_run_events() == [run], "still to be filed"


# ---------------------------------------------------------------------------
# T21: another agent's message wakes the reader.
# ---------------------------------------------------------------------------


def test_a_lead_agents_message_wakes_the_reader_like_a_prompt(tmp_path, monkeypatch):
    pytest.importorskip("pydantic_ai")
    from pydantic_ai.messages import ModelResponse
    from pydantic_ai.models.function import FunctionModel

    from probe.daemon import reader_lane
    from probe.daemon.adapters.base import peer_message

    now = [1000.0]
    w = _worker(tmp_path, _call(1), clock=lambda: now[0])
    lane = reader_lane.ReaderLane(w, model=FunctionModel(lambda m, i: ModelResponse(parts=[])))
    with w.store.tx():
        w.store.set_fact("read_cursor", w.store.newest_seq())
    lane.last_turn_at = 1000.0
    assert lane.due() is None
    with w.store.tx():
        w.store.add([peer_message("main", w.store.next_offset(), text="a4: switch to the NEW arm and rerun",
                                  sender_from="uds:/tmp/s.sock", sender_name="lead")])
    now[0] += 30
    assert lane.due() is None, "at most one peer wake a minute: a swarm's reports come at machine pace"
    now[0] += 31
    assert lane.due() == reader_lane.TRIGGER_PEER
    monkeypatch.setenv(model_mod.ENV_READER_PROMPT_WAKE, "off")
    assert lane.due() is None, "with prompt wakes off, a peer message waits too"


def test_peer_messages_before_the_cursor_wake_nothing(tmp_path):
    from probe.daemon.adapters.base import peer_message

    st = store_mod.Store(tmp_path / "s.sqlite", clock=time.time)
    with st.tx():
        st.add([peer_message("main", 1, text="hi", sender_from="uds:/tmp/s.sock", sender_name="lead")])
    assert st.has_peer_message_after(0) and not st.has_peer_message_after(st.newest_seq())
