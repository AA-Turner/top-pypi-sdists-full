"""Daemon v2 core: adapters, store, bites, pre-checks, approvals, tools.

No network, no model: `probe` commands run against a recording stub (the same
seam the replay bench uses), and the model is Pydantic AI's FunctionModel.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from probe.daemon import adapters, approvals as appr, bite as bite_mod, precheck, tools
from probe.daemon.events import Event, Kind
from probe.daemon.store import Store

HOOK = Path(__file__).resolve().parents[1] / "plugins" / "probe-research" / "hooks" / "approvals_hook.py"
FAKE_KEY = "sk-proj-" + "Ab3dE5gH7jK9mN1pQ3sT5vX7zB9dF1hJ3lN5pR7tV9xZ"


def _cc_lines(sid: str = "s1") -> list[dict]:
    return [
        {"type": "permission-mode", "permissionMode": "bypassPermissions", "sessionId": sid},
        {"type": "user", "message": {"role": "user", "content": "train an SVM on digits and compare to logreg"},
         "timestamp": "2026-09-26T10:00:00Z", "cwd": "/tmp/w"},
        {"type": "assistant", "message": {"content": [
            {"type": "thinking", "thinking": "Plan: sweep C."},
            {"type": "text", "text": "I'll run the sweep."},
            {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "python sweep.py"}}]}},
        {"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": "t1",
             "content": "| model | acc |\n|---|---|\n| svm | 0.9889 |\n| logreg | 0.9603 |"}]}},
        {"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": "t2",
             "content": "<persisted-output>\nOutput too large (64KB). Full output saved to: /x/s1/tool-results/b1.txt\n"}]}},
        {"type": "user", "isMeta": True, "message": {"content": "Caveat: The messages below were generated"}},
        {"type": "user", "message": {"content": "<task-notification>\n<task-id>x</task-id>"}},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "SVM wins: 0.9889 vs 0.9603."}],
                                          "stop_reason": "end_turn"}},
        {"type": "system", "subtype": "turn_duration", "durationMs": 1000},
        {"type": "user", "isCompactSummary": True, "message": {"content": "summary of earlier work"}},
    ]


def _parse(adapter, lines: list[dict], stream: str = "main") -> list[Event]:
    out, off = [], 0
    for obj in lines:
        raw = json.dumps(obj).encode()
        off += len(raw) + 1
        out.extend(adapter.parse_bytes(raw, stream=stream, offset=off))
    return out


# ---------------------------------------------------------------------------
# Adapters (D23)
# ---------------------------------------------------------------------------


def test_claude_code_lines_become_normalized_events():
    a = adapters.for_source("claude_code")
    a.session_files(Path("/x/s1.jsonl"))  # the worker's first call: it names this session's side folder
    kinds = [e.kind for e in _parse(a, _cc_lines())]
    assert kinds == [Kind.PROMPT, Kind.AGENT_REASONING, Kind.AGENT_TEXT, Kind.TOOL_CALL, Kind.TOOL_OUTPUT,
                     Kind.TOOL_OUTPUT, Kind.META, Kind.META, Kind.AGENT_TEXT, Kind.TURN_END, Kind.COMPACTION]
    side = [e for e in _parse(a, _cc_lines()) if e.side_file]
    assert side and side[0].side_file == "/x/s1/tool-results/b1.txt"
    assert a.permission_mode(_cc_lines()[0]) == "bypass"


def test_codex_lines_and_mode():
    a = adapters.for_source("codex")
    lines = [
        {"type": "turn_context", "payload": {"approval_policy": "never",
                                             "sandbox_policy": {"type": "danger-full-access"}}},
        {"type": "response_item", "payload": {"type": "message", "role": "user",
                                              "content": [{"type": "input_text", "text": "<environment_context>x"}]}},
        {"type": "response_item", "payload": {"type": "message", "role": "user",
                                              "content": [{"type": "input_text", "text": "run the eval"}]}},
        {"type": "response_item", "payload": {"type": "function_call", "name": "shell", "call_id": "c1",
                                              "arguments": json.dumps({"command": ["bash", "-lc", "python e.py"]})}},
        {"type": "response_item", "payload": {"type": "function_call_output", "call_id": "c1",
                                              "output": json.dumps({"output": "f1=0.8"})}},
        {"type": "event_msg", "payload": {"type": "task_complete"}},
    ]
    events = _parse(a, lines)
    assert [e.kind for e in events] == [Kind.META, Kind.PROMPT, Kind.TOOL_CALL, Kind.TOOL_OUTPUT, Kind.TURN_END]
    assert events[2].command() == "bash -lc python e.py"
    assert events[3].text == "f1=0.8"
    assert a.permission_mode(lines[0]) == "bypass"
    assert not a.capabilities.question_tool  # terminal fallback


def test_unknown_harness_is_refused_loudly():
    with pytest.raises(LookupError):
        adapters.for_source("cursor")


def test_no_harness_name_outside_the_adapters():
    """D23: the core branches on capabilities, never on a harness name."""
    root = Path(precheck.__file__).parent
    names = re.compile(r"""["'](claude_code|claude-code|codex|pi|cursor|kimi_code|kimi-code|kimi)["']""")
    offenders = []
    for path in root.glob("*.py"):
        for n, line in enumerate(path.read_text().splitlines(), 1):
            if names.search(line) and "default=" not in line:
                offenders.append(f"{path.name}:{n}: {line.strip()}")
    assert offenders == []


# ---------------------------------------------------------------------------
# Store and bites (R1)
# ---------------------------------------------------------------------------


def _store(tmp_path) -> Store:
    return Store(tmp_path / "s.sqlite", clock=lambda: 1000.0)


def test_store_is_idempotent_scrubs_and_counts_turns(tmp_path):
    st = _store(tmp_path)
    events = _parse(adapters.for_source("claude_code"), _cc_lines())
    events[2].text = f"my key is {FAKE_KEY}"
    assert st.add(events) == len(events)
    assert st.add(_parse(adapters.for_source("claude_code"), _cc_lines())) == 0  # same ids
    assert FAKE_KEY not in json.dumps([dict(r) for r in st.db.execute("SELECT text, command FROM events")])
    assert st.current_turn() == 1
    hits = st.search("sweep")
    assert hits and hits[0].command == "python sweep.py"


def test_bite_shows_cutoff_window_divider_and_output_tags(tmp_path, monkeypatch):
    monkeypatch.setattr(bite_mod, "WINDOW_TOKENS", 50)
    monkeypatch.setattr(bite_mod, "STEP_TOKENS", 25)
    st = _store(tmp_path)
    a = adapters.for_source("claude_code")
    for turn in range(3):
        lines = _cc_lines()[1:5]
        lines[0] = {**lines[0], "message": {"content": f"prompt number {turn} " + "x" * 400}}
        evs = _parse(a, lines, stream="main")
        for e in evs:
            e.offset += turn * 100_000
        st.add(evs)
        if turn < 2:
            st.mark_covered(st.open_bite("test", 1, 10**6), 10**6)
    built = bite_mod.build(st, trigger="prompt", context_line="user CLAUDE.md ~1K tokens",
                           pending_lines=["question 7f3 is waiting"], recent_writes=["ran: probe run tag x y"])
    assert built is not None
    assert built.prompt.startswith("Earlier: turns 1–")
    assert "new since your last bite" in built.prompt
    assert "[output main:" in built.prompt and "looks like results" in built.prompt
    assert "0.9889" not in built.prompt  # the output itself is behind its tag
    assert built.prompt.index("# The chat") < built.prompt.index("# Not recorded yet")
    assert "running note" not in built.prompt, "MEMORY.md replaced it, in the request's tail"
    assert "record-session" not in built.instructions and "Probe daemon" in built.instructions
    assert "user CLAUDE.md" in built.instructions


# ---------------------------------------------------------------------------
# Pre-checks (D14, D18)
# ---------------------------------------------------------------------------


def test_every_cli_command_has_an_owner():
    import importlib

    import typer.main

    root = typer.main.get_command(importlib.import_module("probe.cli.main").app)
    leaves: list[str] = []

    def walk(cmd, path):
        if getattr(cmd, "commands", None):
            for name, sub in cmd.commands.items():
                walk(sub, path + [name])
        else:
            leaves.append(" ".join(path))

    walk(root, [])
    assert sorted(c for c in leaves if c not in precheck.OWNERS) == []
    assert sorted(c for c in precheck.OWNERS if c not in leaves) == []


@pytest.mark.parametrize("argv, ok", [
    (["run", "tag", "r1", "abandoned"], True),
    (["run", "list", "--unfiled"], True),
    (["run", "start", "--experiment", "e"], False),
    (["session", "toggle"], False),
    (["token", "create"], False),
    (["notes", "push", "--run", "r", "--force"], False),
    (["--base-url", "http://elsewhere", "run", "list"], False),
    (["run", "set", "r1", "--name", "x", "--authored-by", "human"], False),
    # `--summary` is the researcher's Overview Markdown (track-work: "never write it").
    (["experiment", "set", "e", "--summary", "Yes. RBF SVM wins"], False),
    (["project", "set", "p", "--summary", "x"], False),
    (["experiment", "create", "e", "--project", "p", "--question", "q", "--summary", "x"], False),
    (["experiment", "set", "e", "--question", "Does the SVM beat logreg?"], True),
    # A description written here locks the server's description lane out (L15).
    (["project", "set", "p", "--description", "digits classifiers"], False),
    (["project", "create", "p", "--kind", "general", "--description", "x"], False),
    (["project", "patch", "p", "--description", "x"], False),
    (["run", "set", "r1", "--description", "x"], False),
    (["project", "set", "p", "--name", "Digits"], True),
    (["experiment", "create", "e", "--project", "p", "--question", "Does PCA help?"], True),
    # `--async` exits 0 before Probe answers: a refusal would never reach the daemon (L14).
    (["--async", "run", "end", "r1"], False),
    (["run", "end", "r1", "--async"], False),
    (["artifact", "add", "r1", "f.txt", "--async"], False),
    (["--sync", "run", "end", "r1"], True),
    (["run", "end", "r1", "--sync"], True),
])
def test_allowed_for_the_daemon(argv, ok, tmp_path):
    block = precheck.check(precheck.parse(argv), cwd=tmp_path)
    assert (block is None) == ok, block and block.message()


def test_async_is_refused_with_its_reason_and_no_override(tmp_path):
    for argv in (["--async", "run", "end", "r1"], ["run", "end", "r1", "--async"],
                 ["--async", "run", "delete", "r1"]):
        block = precheck.check(precheck.parse(argv), cwd=tmp_path, trash=True)
        assert block is not None and block.why == precheck.ASYNC_REFUSED and not block.overridable, argv
        assert "has no override" in block.message()


def test_a_description_the_server_writes_is_refused_with_its_reason(tmp_path):
    block = precheck.check(precheck.parse(["project", "set", "p", "--description", "x"]), cwd=tmp_path)
    assert block is not None and block.check == "option"
    assert block.why == "a project's description is written by the server once a run finishes under it"
    block = precheck.check(precheck.parse(["run", "set", "r1", "--description", "x"]), cwd=tmp_path)
    assert block.why == "a run's description is written by the server once the run finishes"


def test_secret_scan_on_text_and_files(tmp_path):
    block = precheck.check(precheck.parse(["run", "set", "r", "--name", f"key {FAKE_KEY}"]), cwd=tmp_path)
    assert block is not None and block.check == "secret" and FAKE_KEY not in (block.flagged or "")
    (tmp_path / "notes.md").write_text(f"token = {FAKE_KEY}\n")
    block = precheck.check(precheck.parse(["run", "set", "r", "--notes", "@notes.md"]), cwd=tmp_path)
    assert block is not None and "notes.md" in block.why
    (tmp_path / "clean.md").write_text("val F1 0.812 vs 0.774\n")
    assert precheck.check(precheck.parse(["run", "set", "r", "--notes", "@clean.md"]), cwd=tmp_path) is None
    (tmp_path / ".env").write_text("A=1\n")
    block = precheck.check(precheck.parse(["artifact", "add", "r1", ".env"]), cwd=tmp_path)
    assert block is not None


# ---------------------------------------------------------------------------
# Approvals (D22) and the hook
# ---------------------------------------------------------------------------


def _facts():
    return {"id": "e1", "name": "lr-sweep (copy)", "what": "experiment", "others": {"alice|runs": 2},
            "count": 2, "updated_at": "t", "reason": "made by mistake", "restorable_until": "25 Oct"}


def test_board_holds_once_and_bypass_goes_ahead(tmp_path):
    board = appr.Board(tmp_path)
    r1 = board.hold(policy="delete.others_data", session_id="s", facts=_facts(), held={"kind": "probe"}, bypass=False)
    r2 = board.hold(policy="delete.others_data", session_id="s", facts=_facts(), held={"kind": "probe"}, bypass=False)
    assert r1.id == r2.id and r1.state == appr.WAITING
    assert r1.question.header == f"Probe {r1.id}" and "2 of alice's runs" in r1.question.question
    auto = board.hold(policy="shell.unsafe_command", session_id="s", facts={"command": "python x.py", "cwd": "/w"},
                      held={"kind": "shell"}, bypass=True)
    assert auto.state == appr.APPROVED and auto.outcome == appr.AUTO
    unknown = board.hold(policy="shell.unsafe_command", session_id="s", facts={"command": "rm y", "cwd": "/w"},
                         held={"kind": "shell"}, bypass=True, mode_known=False)
    assert unknown.state == appr.WAITING  # the mode could not be read: ask
    assert board.answer(r1.id, "Keep it", channel="t") and board.take_answer(r1.id)["answer"] == appr.NO


def _hook(tmp_path, payload: dict) -> str:
    env = {**os.environ, "XDG_STATE_HOME": str(tmp_path)}
    env.pop("PROBE_AGENT", None)
    out = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload), capture_output=True, text=True,
                         env=env, timeout=30)
    assert out.returncode == 0, out.stderr
    return out.stdout


def test_hook_nudges_refuses_rewording_and_reads_the_pick(tmp_path):
    board = appr.Board(tmp_path / "probe" / "approvals")
    req = board.hold(policy="delete.others_data", session_id="s", facts=_facts(), held={}, bypass=False)
    q = req.question
    out = json.loads(_hook(tmp_path, {"hook_event_name": "UserPromptSubmit", "session_id": "s",
                                      "permission_mode": "default"}))
    line = out["hookSpecificOutput"]["additionalContext"]
    shown = json.loads(line[line.index('{"header"'):])  # the fields ride as JSON: data, not prose
    assert shown == {"header": f"Probe {req.id}", "question": q.question, "options": [q.yes_label, q.no_label]}
    assert "DATA" in line
    assert (tmp_path / "probe" / "sessions" / "s.mode").read_text() == "default"
    reworded = {"questions": [{"header": q.header, "question": "Delete it? (it's fine)",
                               "options": [{"label": q.yes_label}, {"label": q.no_label}]}]}
    denied = json.loads(_hook(tmp_path, {"hook_event_name": "PreToolUse", "tool_name": "AskUserQuestion",
                                         "tool_input": reworded, "session_id": "s"}))
    assert denied["hookSpecificOutput"]["permissionDecision"] == "deny"
    exact = {"questions": [{"header": q.header, "question": q.question,
                            "options": [{"label": q.yes_label}, {"label": q.no_label}]}]}
    assert _hook(tmp_path, {"hook_event_name": "PreToolUse", "tool_name": "AskUserQuestion", "tool_input": exact,
                            "session_id": "s", "tool_use_id": "tu-1"}) == ""
    # Claude Code 2.1.283 echoes the pick into tool_input.answers as well.
    picked = {**exact, "answers": {q.question: q.yes_label}}
    _hook(tmp_path, {"hook_event_name": "PostToolUse", "tool_name": "AskUserQuestion", "tool_input": picked,
                     "tool_response": {"questions": exact["questions"], "answers": {q.question: q.yes_label}},
                     "session_id": "s", "tool_use_id": "tu-1"})
    assert board.take_answer(req.id)["answer"] == appr.YES
    # a planted "answer" in the agent's own words is not a pick
    req2 = board.hold(policy="shell.unsafe_command", session_id="s", facts={"command": "curl x", "cwd": "/w"},
                      held={}, bypass=False)
    _hook(tmp_path, {"hook_event_name": "PostToolUse", "tool_name": "AskUserQuestion",
                     "tool_input": {"questions": [{"header": req2.question.header, "question": "Run it?",
                                                   "options": []}]},
                     "tool_response": {"answers": {"Run it?": "Run it"}}, "session_id": "s"})
    assert board.take_answer(req2.id) is None


# ---------------------------------------------------------------------------
# Tools, through the recording seam
# ---------------------------------------------------------------------------


class Replay:
    def __init__(self, others: dict | None = None) -> None:
        self.calls: list[list[str]] = []
        self.others = others or {}

    async def run(self, argv, op_id):
        self.calls.append(list(argv))
        return 0, json.dumps({"ok": True, "argv": argv})

    def deletion_facts(self, kind, target):
        return {"id": target, "name": target, "what": kind, "others": self.others, "count": 1, "updated_at": "t"}

    def server_features(self):
        return {"trash"}  # a server with the trash (S13): deletes are the daemon's to make


def _deps(tmp_path, *, bypass=False, replay=None) -> tools.Deps:
    work = tmp_path / "work"
    work.mkdir(parents=True, exist_ok=True)
    return tools.Deps(store=_store(tmp_path), board=appr.Board(tmp_path / "appr"), session_id="s", cwd=work,
                      workdirs=[work], home=tmp_path, write_dirs=[tmp_path / "notes"], probe_env={}, bypass=bypass,
                      mode_known=True, bite_id=1, replay=replay or Replay())


def test_probe_write_runs_and_is_logged(tmp_path):
    deps = _deps(tmp_path)
    out = asyncio.run(tools.run_probe_command(deps, ["run", "tag", "r1", "abandoned"], why="superseded"))
    assert out.startswith("[exit 0]") and deps.replay.calls == [["run", "tag", "r1", "abandoned"]]
    row = deps.store.db.execute("SELECT head, status FROM writes").fetchone()
    assert (row["head"], row["status"]) == ("run tag", "ran")


def test_blocked_command_then_override_is_a_question(tmp_path):
    deps = _deps(tmp_path)
    out = asyncio.run(tools.run_probe_command(deps, ["project", "set", "p", "--name", f"k {FAKE_KEY}"]))
    block_id = re.search(r"block (\w+)", out).group(1)
    assert deps.replay.calls == []
    held = asyncio.run(tools.run_probe_command(deps, ["daemon", "override", block_id, "--why", "a test fixture"]))
    assert "held for the researcher" in held
    req = deps.board.all(session_id="s")[0]
    assert req.policy == "check.override" and FAKE_KEY not in req.question.question


def test_delete_of_others_data_is_held_unless_bypass(tmp_path):
    deps = _deps(tmp_path, replay=Replay(others={"alice|runs": 2}))
    out = asyncio.run(tools.run_probe_command(deps, ["run", "delete", "r9"]))
    assert "held for the researcher" in out and deps.replay.calls == []
    deps2 = _deps(tmp_path / "b", bypass=True, replay=Replay(others={"alice|runs": 2}))
    out2 = asyncio.run(tools.run_probe_command(deps2, ["run", "delete", "r9"]))
    assert appr.AUTO in out2 and deps2.replay.calls == [["run", "delete", "r9"]]
    own = _deps(tmp_path / "c", replay=Replay(others={}))
    assert asyncio.run(tools.run_probe_command(own, ["run", "delete", "r9"])).startswith("[exit 0]")


def test_session_search_and_open(tmp_path):
    deps = _deps(tmp_path)
    deps.store.add(_parse(adapters.for_source("claude_code"), _cc_lines()))
    assert "sweep.py" in tools.session(deps, "search", query="sweep")
    out_ev = next(e for e in deps.store.events_between(1) if e.kind == Kind.TOOL_OUTPUT)
    opened = tools.session(deps, "open", event_id=out_ev.event_id)
    assert "0.9889" in opened and "python sweep.py" in opened
    assert "turn 1" in tools.session(deps, "outline")


def test_a_search_kind_that_does_not_exist_is_refused_with_the_list(tmp_path):
    """A free-string `kind` let a guessed name answer "no event matches" for text
    that IS in the session (the bite's tags say `[output ...]`, the kind is
    `tool_output`): a kind that is not one is refused, naming the real ones."""
    deps = _deps(tmp_path)
    deps.store.add(_parse(adapters.for_source("claude_code"), _cc_lines()))
    out = tools.session(deps, "search", query="0.9889", kind="output")
    assert out.startswith("not run: kind 'output' is not one of:") and "tool_output" in out, out
    assert "0.9889" in tools.session(deps, "search", query="0.9889", kind="tool_output")


def test_each_session_op_answers_as_the_tool_it_replaced(tmp_path):
    """`session(op=...)` merged session_open, session_search and record_status:
    each op answers exactly what the old tool answered for the same arguments."""
    deps = _deps(tmp_path)
    deps.store.add(_parse(adapters.for_source("claude_code"), _cc_lines()))
    deps.store.log_write(bite=1, op_id="1", argv=["probe", "run", "tag", "r1", "svm"], head="run tag", status="ran")
    out_ev = next(e for e in deps.store.events_between(1) if e.kind == Kind.TOOL_OUTPUT)
    pairs = [
        (tools.session(deps, "open", event_id=out_ev.event_id), tools.session_open(deps, out_ev.event_id)),
        (tools.session(deps, "open", event_id=out_ev.event_id, page=3),
         tools.session_open(deps, out_ev.event_id, page=3)),
        (tools.session(deps, "open", turn=1), tools.session_open(deps, turn=1)),
        (tools.session(deps, "outline"), tools.session_open(deps, outline=True)),
        (tools.session(deps, "search", query="sweep", kind="tool_call", turn_from=1, turn_to=1),
         tools.session_search(deps, "sweep", "tool_call", 1, 1)),
        (tools.session(deps, "logbook", query="svm"), tools.session_search(deps, "svm", logbook=True)),
        (tools.session(deps, "status", status=lambda: "STATE OF THE RECORD"), "STATE OF THE RECORD"),
    ]
    for new, old in pairs:
        assert new == old
    assert '"run", "tag", "r1", "svm"' in pairs[5][0]
    assert tools.session(deps, "open") == "give an event_id or a turn (op=outline: one line per turn)"
    assert tools.session(deps, "search") == "not run: op=search needs `query`"
    assert tools.session(deps, "summarize").startswith("not run: op 'summarize' is not one of: open, outline")


def test_a_long_outline_comes_in_pages(tmp_path, monkeypatch):
    """The outline has no end of its own; it relied on the harness spilling a long
    answer to a file. Past a page it pages like `open`."""
    deps = _deps(tmp_path)
    deps.store.add(_parse(adapters.for_source("claude_code"), _cc_lines()))
    short = tools.session(deps, "outline")
    monkeypatch.setattr(tools, "OPEN_PAGE_CHARS", 20)
    paged = tools.session(deps, "outline", page=1)
    assert paged.startswith("[outline · page 2 of ") and paged.split("\n", 1)[1].startswith(short[20:40])


# ---------------------------------------------------------------------------
# Writes are never reads (R5 / T12): shlex tokens, not first-word heads.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("command, written", [
    ("cat > design.md <<'EOF'\nhello\nEOF", ["design.md"]),
    ("echo hi >> notes/log.txt", ["notes/log.txt"]),
    ("python train.py | tee out/train.log", ["out/train.log"]),
    ("sed -i 's/a/b/' config.yaml", ["config.yaml"]),
    ("cp results.json backup/results.json", ["backup/results.json"]),
    ("mv tmp.csv data/final.csv", ["data/final.csv"]),
    ("cat design.md", []),
    ("grep -E '^(wrote|probe run)' log.txt > /dev/null", []),
    ("X=1 python eval.py 2> err.log", ["err.log"]),
])
def test_written_paths(command, written):
    from probe.daemon.folders import written_paths

    assert written_paths(command) == written
