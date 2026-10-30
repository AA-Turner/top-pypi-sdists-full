"""Daemon cost round 7 (2026-10-25, ~/plans/daemon-cost-round7/PLAN.md).

    F1  a researcher's prompt waits for the writer's least gap like a turn end,
        while the server says so (`x-probe-writer-prompt-waits`)
    F2  a writer conversation idle past `x-probe-writer-cold-fresh-s` starts fresh
        from disk instead of resuming at the full price
    F3  more than `x-probe-writer-file-burst` new files in a row reach the writer
        as a list, not their contents
    F4  `probe daemon task` helpers run on the server's `task` model while it
        serves one (`x-probe-task-model`)
    F5  a task's model calls go to its parent's trace, under the `bash` call that
        started it
    S1  `probe notes find`: the paragraphs of a note that mention some words

Every setting is off without the server's header (an older server): today's
behaviour. A new process starts from what its session last heard, until its
first chat answer settles it.
"""

from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path

import pytest

from probe.cli import notes_find
from probe.daemon import bite as bite_mod
from probe.daemon import lease, tools, toolset
from probe.daemon import model as model_mod
from probe.daemon import approvals as appr
from probe.daemon.events import Kind
from probe.daemon.store import Store, StoredEvent

#: The module runs on the default (`bash`) tool set (conftest).
DAEMON_TOOLS = "bash"
SID = "11111111-2222-3333-4444-555555555555"


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """No real config (so no real key), no MCP, nothing pushed: nothing leaves the box."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.delenv("PROBE_DAEMON_KEY", raising=False)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    for env in (model_mod.ENV_WRITER_GAP, model_mod.ENV_WRITER_PROMPT_WAITS, model_mod.ENV_WRITER_COLD_FRESH,
                model_mod.ENV_WRITER_FILE_BURST, model_mod.ENV_TASK_MODEL, "PROBE_AGENT", toolset.PARALLEL_ENV,
                toolset.TASKS_ENV, toolset.COMMAND_MAP_ENV):
        monkeypatch.delenv(env, raising=False)
    monkeypatch.setattr(model_mod, "_PUSHED", {})
    monkeypatch.setattr(model_mod, "_TASK_MODELS", {})
    monkeypatch.setattr(model_mod, "_RESTORED", set())
    (tmp_path / "state" / "probe" / "sessions").mkdir(parents=True)
    (lease.sessions_dir() / f"{SID}.state").write_text("daemon")


# ---------------------------------------------------------------------------
# The pushed settings.
# ---------------------------------------------------------------------------


def test_each_setting_is_off_until_the_server_says_otherwise():
    assert not model_mod.writer_prompt_waits()
    assert model_mod.writer_cold_fresh_s() == 0
    assert model_mod.writer_file_burst() == 0
    assert model_mod.task_model_name() is None
    model_mod.remember_pushed_settings({model_mod.WRITER_PROMPT_WAITS_HEADER: "on",
                                        model_mod.WRITER_COLD_FRESH_HEADER: "1800",
                                        model_mod.WRITER_FILE_BURST_HEADER: "10",
                                        model_mod.TASK_MODEL_HEADER: "on"})
    assert model_mod.writer_prompt_waits()
    assert model_mod.writer_cold_fresh_s() == 1800
    assert model_mod.writer_file_burst() == 10
    assert model_mod.task_model_name() == model_mod.TASK_MODEL_ALIAS


def test_a_malformed_value_keeps_the_last_good_one_and_a_huge_one_is_capped():
    model_mod.remember_pushed_settings({model_mod.WRITER_COLD_FRESH_HEADER: "1800",
                                        model_mod.WRITER_PROMPT_WAITS_HEADER: "on"})
    model_mod.remember_pushed_settings({model_mod.WRITER_COLD_FRESH_HEADER: "soon",
                                        model_mod.WRITER_PROMPT_WAITS_HEADER: "maybe",
                                        model_mod.WRITER_FILE_BURST_HEADER: "-3"})
    assert model_mod.writer_cold_fresh_s() == 1800 and model_mod.writer_prompt_waits()
    assert model_mod.writer_file_burst() == 0
    model_mod.remember_pushed_settings({model_mod.WRITER_COLD_FRESH_HEADER: str(10**9)})
    assert model_mod.writer_cold_fresh_s() == model_mod.MAX_WRITER_COLD_FRESH_S


def test_the_environment_wins_over_the_server(monkeypatch):
    model_mod.remember_pushed_settings({model_mod.WRITER_PROMPT_WAITS_HEADER: "on",
                                        model_mod.WRITER_COLD_FRESH_HEADER: "1800",
                                        model_mod.WRITER_FILE_BURST_HEADER: "10",
                                        model_mod.TASK_MODEL_HEADER: "off"})
    monkeypatch.setenv(model_mod.ENV_WRITER_PROMPT_WAITS, "off")
    monkeypatch.setenv(model_mod.ENV_WRITER_COLD_FRESH, "60")
    monkeypatch.setenv(model_mod.ENV_WRITER_FILE_BURST, "1")
    monkeypatch.setenv(model_mod.ENV_TASK_MODEL, "claude-haiku-5-5")
    assert not model_mod.writer_prompt_waits()
    assert model_mod.writer_cold_fresh_s() == 60
    assert model_mod.writer_file_burst() == 1
    assert model_mod.task_model_name() == "claude-haiku-5-5"


# ---------------------------------------------------------------------------
# F1: a prompt waits for the least gap.
# ---------------------------------------------------------------------------

pydantic_ai = pytest.importorskip("pydantic_ai")  # the daemon extra; agent-ci runs without it
pytest.importorskip("pydantic_ai_harness")

from pydantic_ai.messages import ModelResponse, TextPart, ToolCallPart  # noqa: E402
from pydantic_ai.models.function import AgentInfo, FunctionModel  # noqa: E402

from probe.daemon import agent as agent_mod  # noqa: E402
from probe.daemon import mailbox  # noqa: E402
from probe.daemon import trace as trace_mod  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402


def _line(obj: dict) -> str:
    return json.dumps(obj) + "\n"


def _worker(tmp_path: Path, *, clock=time.time) -> worker_mod.Worker:
    """A session whose second prompt sits behind other queued events."""
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True, exist_ok=True)
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(
        _line({"type": "permission-mode", "permissionMode": "default"})
        + _line({"type": "user", "message": {"content": "check the intercom"}, "cwd": str(work)})
        + _line({"type": "assistant", "message": {"content": [{"type": "text", "text": "Nothing new."}]}})
        + _line({"type": "user", "message": {"content": "check the intercom"}, "cwd": str(work)}))
    model = FunctionModel(lambda messages, info: ModelResponse(parts=[TextPart("ok")]))
    return worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                             clock=clock, model=model)


def test_a_prompt_starts_a_run_at_once_while_the_switch_is_off(tmp_path, monkeypatch):
    monkeypatch.setenv(model_mod.ENV_WRITER_GAP, "300")
    w = _worker(tmp_path, clock=lambda: 1000.0)
    w.read_new()
    w.last_run_at = 999.0
    assert w.due() == worker_mod.TRIGGER_PROMPT
    assert not w.deferrable(worker_mod.TRIGGER_PROMPT, w.store.pending())


def test_a_prompt_waits_for_the_least_gap_while_the_switch_is_on(tmp_path, monkeypatch):
    monkeypatch.setenv(model_mod.ENV_WRITER_GAP, "300")
    model_mod.remember_pushed_settings({model_mod.WRITER_PROMPT_WAITS_HEADER: "on"})
    now = {"t": 1000.0}
    w = _worker(tmp_path, clock=lambda: now["t"])
    w.read_new()
    w.last_run_at = 999.0
    assert w.deferrable(worker_mod.TRIGGER_PROMPT, w.store.pending())
    assert w.due() is None, "held back: a run ended a second ago"
    now["t"] = 999.0 + 301
    assert w.due() == worker_mod.TRIGGER_PROMPT, "the gap is over"


def test_a_request_still_starts_at_once_while_prompts_wait(tmp_path, monkeypatch):
    monkeypatch.setenv(model_mod.ENV_WRITER_GAP, "300")
    model_mod.remember_pushed_settings({model_mod.WRITER_PROMPT_WAITS_HEADER: "on"})
    w = _worker(tmp_path, clock=lambda: 1000.0)
    w.read_new()
    w.last_run_at = 999.0
    mailbox.write_request(SID, "file the arms")
    w.read_new()
    assert w.due() == worker_mod.TRIGGER_REQUEST
    assert not w.deferrable(worker_mod.TRIGGER_REQUEST, w.store.pending())


def test_the_session_ending_still_starts_a_waiting_prompts_run(tmp_path, monkeypatch):
    monkeypatch.setenv(model_mod.ENV_WRITER_GAP, "300")
    model_mod.remember_pushed_settings({model_mod.WRITER_PROMPT_WAITS_HEADER: "on"})
    w = _worker(tmp_path, clock=lambda: 1000.0)
    w.read_new()
    w.last_run_at = 999.0
    w.stopping = True
    assert w.due() == worker_mod.TRIGGER_PROMPT


# ---------------------------------------------------------------------------
# F2: an idle conversation starts fresh.
# ---------------------------------------------------------------------------


def _big_history() -> str:
    return "x" * (worker_mod.FRESH_FLOOR_TOKENS * bite_mod.CHARS_PER_TOKEN + 1)


def _live(w: worker_mod.Worker, *, updated: float, messages: str) -> int:
    conversation = w.store.start_conversation("job", fingerprint=w._fingerprint())
    w.store.db.execute("UPDATE conversations SET messages = ?, updated = ? WHERE id = ?",
                       (messages, updated, conversation))
    return conversation


@pytest.mark.parametrize(("limit", "idle", "messages", "ends"), [
    (1800, 1801, "big", True),
    (1800, 1799, "big", False),  # its cache is still warm
    (1800, 7200, "small", False),  # a fresh start would not be smaller
    (0, 7200, "big", False),  # off
])
def test_only_a_big_conversation_idle_past_the_limit_is_cold(tmp_path, monkeypatch, limit, idle, messages, ends):
    monkeypatch.setenv(model_mod.ENV_WRITER_COLD_FRESH, str(limit))
    w = _worker(tmp_path, clock=lambda: 10_000.0)
    _live(w, updated=10_000.0 - idle, messages=_big_history() if messages == "big" else "[]")
    live = w.store.live_conversation()
    assert (w._cold_idle_s(live) is not None) is ends


def test_a_cold_conversation_ends_and_the_run_starts_fresh_from_disk(tmp_path, monkeypatch):
    monkeypatch.setenv(model_mod.ENV_WRITER_COLD_FRESH, "1800")
    w = _worker(tmp_path, clock=lambda: 10_000.0)
    w.read_new()
    old = _live(w, updated=10_000.0 - 3600, messages=_big_history())
    conversation, history, built = w._next_in_conversation(worker_mod.TRIGGER_PROMPT, None)
    row = w.store.db.execute("SELECT ended, end_reason FROM conversations WHERE id = ?", (old,)).fetchone()
    assert row["ended"] is not None and row["end_reason"].startswith("idle 60 min: the model's prompt cache is gone")
    assert history is None and built is not None and conversation != old
    assert w._fresh_why == "cold"


# ---------------------------------------------------------------------------
# F3: a file burst is a list.
# ---------------------------------------------------------------------------


def _event(seq: int, text: str, *, kind: Kind = Kind.FILE_CHANGE, stream: str = bite_mod.FOLDERS_STREAM) -> StoredEvent:
    return StoredEvent(seq=seq, event_id=f"{stream}:{seq}:0", stream=stream, kind=kind, turn=1, ts=None, noticed=0.0,
                       text=text, tool=None, call_id=None, command=None, is_error=False, side_file=None,
                       chars=len(text), bite=None, offset=seq)


def _new_files(first: int, n: int, folder: str = "/repo/wt/src") -> list[StoredEvent]:
    return [_event(first + i, f"new file {folder}/f{i}.ts ({1000 + i:,} bytes)\nexport const body = 'secret-ish'")
            for i in range(n)]


def test_more_new_files_in_a_row_than_the_limit_are_one_list(monkeypatch):
    monkeypatch.setenv(model_mod.ENV_WRITER_FILE_BURST, "10")
    events = [_event(1, "train the model", kind=Kind.PROMPT, stream="main"), *_new_files(2, 11),
              _event(13, "changed /repo/cfg.yaml (10 -> 12 bytes)\n-lr: 1\n+lr: 2")]
    shown = bite_mod.rendered(events)
    assert len(shown) == 3
    _, burst = shown[1]
    head, *lines = burst.split("\n")
    assert head == toolset.pick(*bite_mod.FILE_BURST).format(n=11)
    assert lines == ["/repo/wt/src/: " + " · ".join(f"f{i}.ts ({1000 + i:,} bytes) folders:{2 + i}:0"
                                                     for i in range(11))]
    assert "export const body" not in burst
    # A change is one line too (swarm friction T17, R40): its diff is one open away.
    assert shown[2][1] == ("[file changed · folders:13:0] " + toolset.pick(*bite_mod.MORE_LINES).format(
        head="changed /repo/cfg.yaml (10 -> 12 bytes)", n=2, id="folders:13:0"))


def test_up_to_the_limit_each_new_file_shows_as_before(monkeypatch):
    monkeypatch.setenv(model_mod.ENV_WRITER_FILE_BURST, "10")
    events = _new_files(1, 10)
    assert [text for _, text in bite_mod.rendered(events)] == [bite_mod.render(ev) for ev in events]


def test_off_every_new_file_shows_as_before():
    events = _new_files(1, 50)
    assert [text for _, text in bite_mod.rendered(events)] == [bite_mod.render(ev) for ev in events]


def test_a_burst_counts_small_toward_a_bites_budget(tmp_path, monkeypatch):
    from probe.daemon.events import Event

    st = Store(tmp_path / "s.sqlite", clock=time.time)
    st.add([Event(kind=Kind.PROMPT, stream="main", offset=1, text="pull the branch")])
    st.add([Event(kind=Kind.FILE_CHANGE, stream=bite_mod.FOLDERS_STREAM, offset=2 + i,
                  text=f"new file /repo/f{i}.py (3,000 bytes)\n" + "x" * 3000) for i in range(300)])
    monkeypatch.setattr(bite_mod, "NEW_SHOWN_TOKENS", 10_000)
    first, last = bite_mod.cover(st)
    assert last - first + 1 < 301, "a line each, 300 files pass the budget"
    monkeypatch.setenv(model_mod.ENV_WRITER_FILE_BURST, "10")
    first, last = bite_mod.cover(st)
    assert last - first + 1 == 301, "listed, they all fit one bite"


# ---------------------------------------------------------------------------
# F4: tasks run on the server's task model.
# ---------------------------------------------------------------------------


def _endpoint(monkeypatch):
    monkeypatch.setenv("PROBE_DAEMON_KEY", "k")
    monkeypatch.setenv("PROBE_BASE_URL", "http://127.0.0.1:9")


def test_a_task_runs_on_its_parents_model_until_the_server_serves_a_task_model(monkeypatch):
    _endpoint(monkeypatch)
    parent = model_mod.build(model_mod.endpoint(), model_mod.LANE_WRITE)
    assert model_mod.task_model(parent) is parent
    model_mod.remember_pushed_settings({model_mod.TASK_MODEL_HEADER: "on"})
    task = model_mod.task_model(parent)
    assert task is not parent and task.model_name == model_mod.TASK_MODEL_ALIAS
    assert getattr(task, model_mod.PROBE_LANE_ATTR) == model_mod.LANE_WRITE, "the parent's lane, slots and meter"
    assert model_mod.task_model(parent) is task, "one per lane and name"
    reader = model_mod.build(model_mod.endpoint(), model_mod.LANE_READ)
    assert getattr(model_mod.task_model(reader), model_mod.PROBE_LANE_ATTR) == model_mod.LANE_READ
    model_mod.remember_pushed_settings({model_mod.TASK_MODEL_HEADER: "off"})
    assert model_mod.task_model(parent) is parent


def test_a_model_this_module_did_not_build_is_its_own_task_model(monkeypatch):
    monkeypatch.setenv(model_mod.ENV_TASK_MODEL, "claude-haiku-5-5")
    scripted = FunctionModel(lambda messages, info: ModelResponse(parts=[TextPart("ok")]))
    assert model_mod.task_model(scripted) is scripted


# ---------------------------------------------------------------------------
# F5: a task's calls are in its parent's trace.
# ---------------------------------------------------------------------------


def _deps(tmp_path) -> tools.Deps:
    from probe.daemon.folders import note_dirs

    work = tmp_path / "work"
    work.mkdir(parents=True, exist_ok=True)
    st = Store(tmp_path / "s.sqlite", clock=time.time)
    deps = tools.Deps(store=st, board=appr.Board(tmp_path / "appr"), session_id=SID, cwd=work, workdirs=[work],
                      home=tmp_path, write_dirs=note_dirs(), probe_env={}, bypass=False, mode_known=True, bite_id=1,
                      reader=False, harness="claude_code")
    assert lease.renew(SID)
    return deps


def test_a_tasks_calls_are_written_under_the_bash_call_that_started_it(tmp_path):
    deps = _deps(tmp_path)
    (deps.cwd / "a.txt").write_text("the best lr is 0.003\n")
    parent_rounds = [[ToolCallPart("bash", {"command": 'probe daemon task "find the best lr"', "why": "t"},
                                   tool_call_id="c0")]]

    async def fn(messages, info: AgentInfo) -> ModelResponse:
        if not info.output_tools:  # the task: one read, then its answer
            if sum(isinstance(m, ModelResponse) for m in messages) == 0:
                return ModelResponse(parts=[ToolCallPart("bash", {"command": "cat a.txt"}, tool_call_id="t0")])
            return ModelResponse(parts=[TextPart("best lr: 0.003 (a.txt)")])
        if parent_rounds:
            return ModelResponse(parts=parent_rounds.pop(0))
        return ModelResponse(parts=[ToolCallPart("final_result", {"summary": "done"})])

    trace = trace_mod.TraceFile(SID, "writer")
    trace.start_run(7, trigger="prompt")
    state = agent_mod.RunState(trace=trace)
    agent = agent_mod.build_agent("i", model=FunctionModel(fn), state=state)
    asyncio.run(agent.run("go", deps=deps))
    lines = [json.loads(line) for line in trace.path.read_text().splitlines()]
    task_calls = [ln for ln in lines if ln["type"] == "call" and "task" in ln]
    own_calls = [ln for ln in lines if ln["type"] == "call" and "task" not in ln]
    assert [(ln["task"], ln["task_of"], ln["round"], ln["task_round"]) for ln in task_calls] == \
        [(1, "c0", 1, 1), (1, "c0", 1, 2)]
    assert all(ln["run"] == 7 and ln["trace_id"] == trace.trace_id(7) for ln in task_calls)
    assert [ln["round"] for ln in own_calls] == [1, 2]
    [task_tool] = [ln for ln in lines if ln["type"] == "tool" and "task" in ln]
    assert task_tool["args"]["command"] == "cat a.txt" and task_tool["round"] == 1
    # The task's job description is its own line, and the parent's head never reads as rewritten.
    assert not [ln for ln in lines if ln["type"] == "history_rewritten"]
    assert {ln.get("task") for ln in lines if ln["type"] == "instructions"} == {None, 1}
    # Every task line names its task round, the job text and tools too (review 10-25).
    assert all("task_round" in ln for ln in lines if "task" in ln)


# ---------------------------------------------------------------------------
# S1: `probe notes find`.
# ---------------------------------------------------------------------------

NOTE = """# Willow

One line on what this is.

## Where it stands

- Review 02e1117b passed on the frozen verifier.
- The lr sweep is done.

## Decisions

We chose lr 3e-4 after the 02e1117b review.
Not 1e-3: it diverged.
"""


def test_find_prints_each_matching_paragraph_verbatim_with_its_heading_and_lines():
    out = notes_find.report("willow", 12, NOTE, ["02e1117b", "review"])
    head, *blocks = out.split("\n\n")
    assert head.startswith("willow · v12 · ") and "2 of " in head and '"02e1117b" "review"' in head
    assert blocks[0] == "[Where it stands · lines 7-8]\n- Review 02e1117b passed on the frozen verifier.\n" \
                        "- The lr sweep is done."
    assert blocks[1] == "[Decisions · lines 12-13]\nWe chose lr 3e-4 after the 02e1117b review.\nNot 1e-3: it diverged."


def test_find_ranks_paragraphs_that_hold_more_of_the_words_first():
    found, total = notes_find.matches(NOTE, ["lr", "diverged"])
    assert [p.heading for p in found] == ["Decisions", "Where it stands"] and total == 6


def test_find_says_so_when_nothing_matches_and_cuts_a_long_answer(monkeypatch):
    assert notes_find.report("willow", 3, NOTE, ["tokenizer"]).endswith('no paragraph mentions "tokenizer"')
    monkeypatch.setattr(notes_find, "MAX_PARAGRAPHS", 1)
    out = notes_find.report("willow", 3, NOTE, ["02e1117b"])
    assert out.endswith("[... 1 more matching paragraphs: add words to narrow]")


# ---------------------------------------------------------------------------
# Review 10-25.
# ---------------------------------------------------------------------------


def test_a_new_process_starts_from_the_settings_its_session_last_heard(tmp_path, monkeypatch):
    model_mod.remember_pushed_settings({model_mod.WRITER_COLD_FRESH_HEADER: "1800",
                                        model_mod.WRITER_FILE_BURST_HEADER: "10",
                                        model_mod.WRITER_PROMPT_WAITS_HEADER: "on"})
    w = _worker(tmp_path)
    w.store.set_fact(worker_mod.PUSHED_SETTINGS, model_mod.pushed_snapshot())
    monkeypatch.setattr(model_mod, "_PUSHED", {})  # a new process
    assert model_mod.writer_cold_fresh_s() == 0
    _worker(tmp_path)
    assert model_mod.writer_cold_fresh_s() == 1800 and model_mod.writer_file_burst() == 10
    assert model_mod.writer_prompt_waits()
    # What the server says next wins over what was kept.
    model_mod.remember_pushed_settings({model_mod.WRITER_COLD_FRESH_HEADER: "0"})
    assert model_mod.writer_cold_fresh_s() == 0


def test_restoring_never_overrides_what_this_process_heard():
    model_mod.remember_pushed_settings({model_mod.WRITER_FILE_BURST_HEADER: "5"})
    model_mod.restore_pushed({model_mod.WRITER_FILE_BURST_HEADER: "10", "x-other": "1"})
    assert model_mod.writer_file_burst() == 5
    model_mod.restore_pushed("junk")
    assert model_mod.writer_file_burst() == 5


def test_a_task_model_that_cannot_be_built_leaves_tasks_on_their_parents_model(monkeypatch):
    _endpoint(monkeypatch)
    parent = model_mod.build(model_mod.endpoint(), model_mod.LANE_WRITE)
    model_mod.remember_pushed_settings({model_mod.TASK_MODEL_HEADER: "on"})

    def broken(*args, **kwargs):
        raise RuntimeError("no client")

    monkeypatch.setattr(model_mod, "build", broken)
    assert model_mod.task_model(parent) is parent, "no exception out of every bash call"


def test_the_task_model_follows_its_parents_endpoint(monkeypatch):
    _endpoint(monkeypatch)
    parent = model_mod.build(model_mod.endpoint(), model_mod.LANE_WRITE)
    model_mod.remember_pushed_settings({model_mod.TASK_MODEL_HEADER: "on"})
    first = model_mod.task_model(parent)
    assert getattr(first, model_mod.PROBE_ENDPOINT_ATTR) == getattr(parent, model_mod.PROBE_ENDPOINT_ATTR)
    monkeypatch.setenv("PROBE_DAEMON_KEY", "k2")
    rebuilt = model_mod.build(model_mod.endpoint(), model_mod.LANE_WRITE)  # the writer, after a key rotation
    assert model_mod.task_model(rebuilt) is not first and model_mod.task_model(parent) is first


def test_a_restored_setting_the_first_answer_does_not_carry_is_dropped(tmp_path, monkeypatch):
    """An older server (or a rollback) sends none of round 7's headers: what a new
    process restored must not outlive its first answer (review 10-25)."""
    monkeypatch.setattr(model_mod, "_RESTORED", set())
    model_mod.restore_pushed({model_mod.WRITER_FILE_BURST_HEADER: "10", model_mod.WRITER_COLD_FRESH_HEADER: "1800"})
    assert model_mod.writer_file_burst() == 10
    model_mod._confirm_restored({model_mod.WRITER_COLD_FRESH_HEADER: "1800"})
    assert model_mod.writer_file_burst() == 0 and model_mod.writer_cold_fresh_s() == 1800
    model_mod._confirm_restored({})
    assert model_mod.writer_cold_fresh_s() == 1800, "only the first answer settles a restore"


def test_the_task_model_switch_is_never_restored():
    model_mod.restore_pushed({model_mod.TASK_MODEL_HEADER: "on"})
    assert model_mod.task_model_name() is None


def test_on_the_index_layout_a_burst_counts_small_too(tmp_path, monkeypatch):
    """The indexer reads a burst as the list the writer would (swarm friction T17
    (1)): it counts as listed there too, so one bite takes all 300."""
    from probe.daemon.events import Event

    st = Store(tmp_path / "s.sqlite", clock=time.time)
    st.add([Event(kind=Kind.PROMPT, stream="main", offset=1, text="pull the branch")])
    st.add([Event(kind=Kind.FILE_CHANGE, stream=bite_mod.FOLDERS_STREAM, offset=2 + i,
                  text=f"new file /repo/f{i}.py (3,000 bytes)\n" + "x" * 3000) for i in range(300)])
    monkeypatch.setattr(bite_mod, "NEW_SHOWN_TOKENS", 10_000)
    monkeypatch.setenv(model_mod.ENV_WRITER_FILE_BURST, "10")
    monkeypatch.setenv(model_mod.ENV_WRITER_EVENTS, "index")
    first, last = bite_mod.cover(st)
    assert last - first + 1 == 301
