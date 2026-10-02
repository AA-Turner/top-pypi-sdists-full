"""The bench's reader lane (evals/companion: asof.py, reads.py, score_reads.py) -- no model.

Pins what a reader-lane number depends on: Probe rebuilt as of the session's
start (a post-start value never reaches the reader; a fixture that cannot be
rebuilt is invalid), the played delivery hooks (one unasked message per
researcher turn, every answer), the scripted asks, the live store read turn by
turn, and the R1-R5 scorers on synthetic results.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

AGENT = Path(__file__).resolve().parents[1]
EVALS = AGENT / "evals" / "companion"


def _load(name: str):
    if str(EVALS) not in sys.path:
        sys.path.insert(0, str(EVALS))
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, EVALS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


fp = _load("fake_probe")
asof = _load("asof")
rd = _load("reads")
sr = _load("score_reads")
score = _load("score")

PRIOR_PROJECT = "a1a1a1a1-1111-4111-8111-111111111111"
PRIOR_RUN = "a2b2c2d2-2222-4222-8222-222222222222"
OWN_PROJECT = "b1b1b1b1-1111-4111-8111-111111111111"
OWN_RUN = "b2c2d2e2-2222-4222-8222-222222222222"
OWN_EXP = "b3b3b3b3-3333-4333-8333-333333333333"
T = fp.parse_ts
START = T("2026-09-24T03:33:28Z")


def _line(ts: str, obj: dict | None = None) -> tuple[bytes, float]:
    body = {"type": "user", "timestamp": ts, "message": {"content": "hi"}, **(obj or {})}
    return (json.dumps(body) + "\n").encode(), T(ts)


def _fixture(tmp_path: Path, name: str, reads: dict, times: list[str], sid: str) -> SimpleNamespace:
    path = tmp_path / name
    path.mkdir(parents=True, exist_ok=True)
    (path / "reads.json").write_text(json.dumps(reads))
    return SimpleNamespace(path=path, name=name, reads=reads, session_id=sid, lines=[_line(t) for t in times],
                           end_time=T(times[-1]))


def _prior_reads(**late) -> dict:
    run = {"id": PRIOR_RUN, "slug": "old-svm-1", "name": "RBF SVM (C=10, gamma=0.001)", "status": "completed",
           "project_id": PRIOR_PROJECT, "created_at": "2026-09-23T08:02:00Z", "updated_at": "2026-09-23T08:04:00Z",
           "ended_at": "2026-09-23T08:03:00Z", "summary_metrics": {"cv_accuracy_mean": 0.9889}, "tags": []}
    run.update(late)
    return {f"/v1/projects/{PRIOR_PROJECT}": {"id": PRIOR_PROJECT, "slug": "digits-old", "name": "Old digits study",
                                              "kind": "training", "created_at": "2026-09-23T08:01:00Z",
                                              "updated_at": "2026-09-23T08:05:00Z", "tags": [],
                                              "metadata": {"overview": {"blurb": "SVM 0.989 vs LR 0.960",
                                                                        "generated_at": "2026-09-23T09:00:00Z"}}},
            f"/v1/runs/{PRIOR_RUN}": run, f"/v1/runs/{PRIOR_RUN}/artifacts": [], f"/v1/runs/{PRIOR_RUN}/edges": []}


def _own_reads() -> dict:
    return {f"/v1/projects/{OWN_PROJECT}": {"id": OWN_PROJECT, "slug": "digits-new", "name": "New digits study",
                                            "kind": "training", "created_at": "2026-09-24T03:36:00Z",
                                            "updated_at": "2026-09-24T03:51:00Z", "tags": []},
            f"/v1/projects/{OWN_EXP}": {"id": OWN_EXP, "slug": "svm-vs-lr", "name": "SVM vs LR", "kind": "experiment",
                                        "parent_project_id": OWN_PROJECT, "created_at": "2026-09-24T03:36:30Z",
                                        "updated_at": "2026-09-24T03:51:00Z", "tags": [],
                                        "metadata": {"overview": {"blurb": "The SVM wins: 0.989",
                                                                  "generated_at": "2026-09-24T03:44:00Z"}}},
            f"/v1/runs/{OWN_RUN}": {"id": OWN_RUN, "slug": "new-lr-1", "name": "Logistic Regression Baseline",
                                    "status": "completed", "project_id": OWN_PROJECT, "experiment_id": OWN_EXP,
                                    "created_at": "2026-09-24T03:38:21Z", "updated_at": "2026-09-24T03:38:42Z",
                                    "ended_at": "2026-09-24T03:38:42Z", "tags": ["baseline", "live-daemon-tag"],
                                    "summary_metrics": {"cv_accuracy_mean": 0.9701}, "summary": {"x": 1},
                                    "counts": {"metrics": 8}}}


def _rebuild(tmp_path, prior_reads=None, prior_times=None, label=None, *, mtime=None, **kw):
    own = _fixture(tmp_path, "own", _own_reads(), ["2026-09-24T03:33:28Z", "2026-09-24T03:51:02Z"],
                   "11111111-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
    prior = _fixture(tmp_path, "prior", prior_reads if prior_reads is not None else _prior_reads(),
                     prior_times or ["2026-09-23T07:55:57Z", "2026-09-23T08:09:41Z"],
                     "22222222-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
    label = label if label is not None else {"prior": [{"fixture": "prior"}]}

    def load(name):
        if name != "prior":
            raise SystemExit(f"no fixture {name!r}")
        return prior

    return asof.rebuild(own, label, load=load, ledger_state=tmp_path / "state",
                        mtime=mtime or (lambda p: T("2026-09-23T21:06:21Z")), **kw)


# ---------------------------------------------------------------------------
# As of the start.
# ---------------------------------------------------------------------------


def test_prior_work_captured_before_the_start_is_merged(tmp_path):
    rb = _rebuild(tmp_path)
    assert rb.valid and rb.reasons == []
    assert f"/v1/runs/{PRIOR_RUN}" in rb.reads and f"/v1/runs/{OWN_RUN}" in rb.reads
    assert rb.prior_refs[PRIOR_RUN] == "old-svm-1" and OWN_RUN in rb.session_refs
    assert rb.prior[0]["frozen_at_source"].startswith("reads.json mtime")
    assert rb.start == START
    assert any("notes: none served" in n for n in rb.notes)


@pytest.mark.parametrize("case, expect", [
    ("captured-late", "after this session started"),
    ("row-late", "dated after the start"),
    ("overview-late", "overview generated_at"),
    ("overlap", "ran until"),
    ("clash", "both hold"),
    ("missing", "not found"),
    ("memory", "memory newer than the start"),
    ("no-frozen-at-proof", "after this session started"),
])
def test_a_prior_that_could_carry_the_future_makes_the_fixture_invalid(tmp_path, case, expect):
    kw: dict = {}
    if case == "captured-late":
        kw["mtime"] = lambda p: T("2026-09-24T04:00:00Z")
    elif case == "row-late":
        kw["prior_reads"] = _prior_reads(updated_at="2026-09-24T05:00:00Z")
    elif case == "overview-late":
        reads = _prior_reads()
        reads[f"/v1/projects/{PRIOR_PROJECT}"]["metadata"]["overview"]["generated_at"] = "2026-09-25T00:00:00Z"
        kw["prior_reads"] = reads
    elif case == "overlap":
        kw["prior_times"] = ["2026-09-24T03:30:00Z", "2026-09-24T03:40:00Z"]
        kw["prior_reads"] = {}
    elif case == "clash":
        kw["prior_reads"] = {**_prior_reads(), f"/v1/runs/{OWN_RUN}": _own_reads()[f"/v1/runs/{OWN_RUN}"]}
    elif case == "missing":
        kw["label"] = {"prior": [{"fixture": "nowhere"}]}
    elif case == "memory":
        kw["with_home_context"] = True
    elif case == "no-frozen-at-proof":
        # A copy made later moves the file's mtime: an upper bound that no longer proves anything.
        kw["mtime"] = lambda p: time.time()
    rb = _rebuild(tmp_path, **kw)
    assert not rb.valid and any(expect in r for r in rb.reasons), rb.reasons
    if case != "memory":
        assert f"/v1/runs/{PRIOR_RUN}" not in rb.reads  # a prior that could carry the future is never served


def test_an_answer_key_frozen_at_is_used_and_checked(tmp_path):
    ok = _rebuild(tmp_path, label={"prior": [{"fixture": "prior", "frozen_at": "2026-09-23T10:00:00Z"}]},
                  mtime=lambda p: time.time())
    assert ok.valid and ok.prior[0]["frozen_at_source"] == "answer key"


def test_the_live_daemons_run_tags_are_scrubbed_again_from_its_ledger(tmp_path):
    import sqlite3

    ledger = tmp_path / "state" / "probe" / "companion" / "11111111-aaaa-4aaa-8aaa-aaaaaaaaaaaa.sqlite"
    ledger.parent.mkdir(parents=True)
    conn = sqlite3.connect(ledger)
    conn.execute("CREATE TABLE proposals (target_id TEXT, target_type TEXT, kind TEXT, status TEXT, payload TEXT)")
    conn.execute("INSERT INTO proposals VALUES (?, 'run', 'tag', 'published', ?)",
                 (OWN_RUN, json.dumps({"add": ["live-daemon-tag"]})))
    conn.commit()
    conn.close()
    rb = _rebuild(tmp_path)
    assert rb.reads[f"/v1/runs/{OWN_RUN}"]["tags"] == ["baseline"]
    assert rb.ledger == {"found": True, "runs": 1, "tags_dropped_now": 1}
    assert _rebuild(tmp_path / "x").ledger == {"found": False}


def _fake(now: str, reads: dict | None = None, **kw):
    return fp.FakeProbe(reads or {**_own_reads(), **_prior_reads()}, clock=fp.ManualClock(T(now)),
                        token="bench-fake-t", **kw)


def _get(fake, path):
    return fake.handle("GET", path, "", b"", {"authorization": "Bearer bench-fake-t"})


def test_as_of_holds_back_what_the_server_filled_later(tmp_path):
    fake = _fake("2026-09-24T03:38:30Z", as_of=True)
    run = _get(fake, f"/v1/runs/{OWN_RUN}").body
    assert run["status"] == "running" and run["summary_metrics"] == {} and run["summary"] == {} and "counts" not in run
    exp = _get(fake, f"/v1/projects/{OWN_EXP}").body
    assert "overview" not in exp["metadata"] and exp["updated_at"] == exp["created_at"]
    # Prior work is shown whole: everything in it predates the clock.
    old = _get(fake, f"/v1/runs/{PRIOR_RUN}").body
    assert old["summary_metrics"] == {"cv_accuracy_mean": 0.9889}
    assert _get(fake, f"/v1/projects/{PRIOR_PROJECT}").body["metadata"]["overview"]["blurb"].startswith("SVM")
    fake.clock.now = T("2026-09-24T03:45:00Z")
    assert _get(fake, f"/v1/runs/{OWN_RUN}").body["summary_metrics"] == {"cv_accuracy_mean": 0.9701}
    assert _get(fake, f"/v1/projects/{OWN_EXP}").body["metadata"]["overview"]["blurb"] == "The SVM wins: 0.989"
    # Off (the writer bench as before): today's fields, as they were.
    plain = _fake("2026-09-24T03:38:30Z")
    assert _get(plain, f"/v1/runs/{OWN_RUN}").body["summary_metrics"] == {"cv_accuracy_mean": 0.9701}


def test_the_start_time_cut_a_post_start_row_is_invisible_to_the_reader(tmp_path):
    fake = _fake("2026-09-24T03:35:00Z", as_of=True)
    assert _get(fake, f"/v1/runs/{OWN_RUN}").status == 404
    found = fake.handle("POST", "/v1/search", "", json.dumps({"query": "digits study",
                                                              "exclude_agent_session": "s"}).encode(),
                        {"authorization": "Bearer bench-fake-t"}).body
    ids = {r["id"] for r in found["exact"]["results"]} | {r["ref"]["id"] for r in found["semantic"]["results"]}
    assert PRIOR_PROJECT in ids and OWN_PROJECT not in ids and OWN_RUN not in ids
    # The server's echo that it applied the self-exclusion (the MCP marks the answer partial without it).
    assert found["semantic"]["exclusion_applied"] is True and found["semantic"]["excluded_count"] == 0


def test_the_lane_of_each_model_round_is_recorded():
    rec = fp._round_record("/v1/companion/chat/completions", b"{}", 200, b"{}", time.time(), 0.0, "read")
    assert rec["lane"] == "read"
    assert fp._round_record("/p", b"{}", 200, b"{}", time.time(), 0.0)["lane"] == "write"


# ---------------------------------------------------------------------------
# The played hooks, the scripted asks, the live store.
# ---------------------------------------------------------------------------


def _msg(root: Path, sid: str, mid: str, kind: str, made: float, **extra) -> Path:
    folder = root / "messages" / sid
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{int(made * 1e9):020d}-{mid}.json"
    path.write_text(json.dumps({"id": mid, "session": sid, "kind": kind, "text": "t", "made_at": made,
                                "expires_at": made + 3600, **extra}))
    return path


def _raw(obj: dict) -> bytes:
    return (json.dumps(obj) + "\n").encode()


PROMPT = _raw({"type": "user", "message": {"content": "do the study"}})
TOOL = _raw({"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "x", "content": "ok"}]}})
SIDE = _raw({"type": "user", "isSidechain": True,
             "message": {"content": [{"type": "tool_result", "tool_use_id": "y", "content": "ok"}]}})
META = _raw({"type": "user", "isMeta": True, "message": {"content": [{"type": "text", "text": "skill body"}]}})


def test_line_kinds_follow_the_hooks():
    assert rd.line_kind(PROMPT) == "prompt" and rd.line_kind(TOOL) == "tool"
    assert rd.line_kind(SIDE) is None and rd.line_kind(META) is None
    assert rd.line_kind(_raw({"type": "assistant", "message": {"content": []}})) is None
    assert rd.line_kind(_raw({"type": "user", "message": {"content": "<local-command-stdout>x"}})) is None


def test_the_played_hooks_deliver_every_answer_and_one_unasked_message_per_turn(tmp_path):
    sid, now = "s1", time.time()
    d = rd.Deliverer(tmp_path, sid)
    d.on_line(PROMPT, 100.0, 1)
    _msg(tmp_path, sid, "m1", "message", now)
    _msg(tmp_path, sid, "m2", "message", now + 1)
    _msg(tmp_path, sid, "a1", "answer", now + 2, ask="q1")
    d.on_line(SIDE, 101.0, 2)  # a helper agent's call claims nothing
    assert d.log == []
    d.on_line(TOOL, 102.0, 3)
    assert [(x["id"], x["at"], x["via"], x["line"]) for x in d.log] == [("m1", 102.0, "tool", 3),
                                                                        ("a1", 102.0, "tool", 3)]
    d.on_line(TOOL, 103.0, 4)  # the turn's one unasked slot is used: m2 waits
    assert len(d.log) == 2 and list((tmp_path / "messages" / sid).glob("*m2.json"))
    d.on_line(PROMPT, 104.0, 5)  # a new researcher turn: a new slot
    assert d.log[-1]["id"] == "m2" and d.log[-1]["via"] == "prompt" and d.log[-1]["turn"] == 2
    assert sorted(p.name.split("-", 1)[1] for p in (tmp_path / "claimed" / sid).glob("*.json")) == [
        "a1.json", "m1.json", "m2.json"]
    _msg(tmp_path, sid, "old", "answer", now - 7200, expires_at=now - 10)
    d.on_line(TOOL, 105.0, 6)
    assert d.log[-1]["id"] == "m2"  # an expired message is never delivered


#: The keys Claude Code 2.1.283 writes on a `hook_additional_context` line (real
#: transcripts, 2026-09-29): a PostToolUse line also carries `session_id`.
CC_ATTACHMENT_KEYS = ["parentUuid", "isSidechain", "attachment", "type", "uuid", "timestamp", "rendered",
                      "userType", "entrypoint", "cwd", "sessionId", "version", "gitBranch"]
CC_HOOK_KEYS = ["type", "content", "hookName", "toolUseID", "hookEvent"]


def _session_line(obj: dict) -> bytes:
    return _raw({"parentUuid": "p0", "isSidechain": False, "userType": "external", "entrypoint": "cli",
                 "cwd": "/home/r/digits", "sessionId": "s1", "version": "2.1.283", "gitBranch": "HEAD",
                 "timestamp": "2026-09-24T03:40:00.000Z", **obj})


def test_a_delivery_goes_into_the_transcript_as_claude_code_writes_it_and_the_real_adapter_reads_it(tmp_path):
    sys.path.insert(0, str(AGENT / "src"))
    from probe.daemon.adapters.claude_code import PROBE_MESSAGE_PREFIX, ClaudeCode
    from probe.daemon.events import Kind as EventKind
    from probe.daemon.mailbox import Message

    sid, now = "s1", time.time()
    d = rd.Deliverer(tmp_path, sid)
    call = _session_line({"type": "assistant", "uuid": "u-call", "message": {"role": "assistant", "content": [
        {"type": "tool_use", "id": "toolu_1", "name": "Bash", "input": {"command": "python svm.py"}}]}})
    result = _session_line({"type": "user", "uuid": "u-result", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": "toolu_1", "content": "cv 0.9889"}]}})
    assert d.on_line(call, 100.0, 1) is None  # an assistant line delivers nothing
    assert d.on_line(result, 101.0, 2) is None  # nothing waits: no line
    _msg(tmp_path, sid, "m1", "message", now, text="The team ran this SVM on 09-23: 0.989.")
    _msg(tmp_path, sid, "a1", "answer", now + 1, ask="ask1", question="Did anyone run PCA?", text="Yes: 0.988.")
    expected = [Message.from_dict(json.loads(p.read_text())).rendered()
                for p in sorted((tmp_path / "messages" / sid).glob("*.json"))]
    raw = d.on_line(result, 102.5, 3)
    assert raw is not None and raw.endswith(b"\n") and raw.count(b"\n") == 1
    line = json.loads(raw)

    # The shape Claude Code 2.1.283 writes, chained to the tool result whose hook ran.
    assert list(line) == [*CC_ATTACHMENT_KEYS[:7], "session_id", *CC_ATTACHMENT_KEYS[7:]]
    assert list(line["attachment"]) == CC_HOOK_KEYS
    assert line["type"] == "attachment" and line["parentUuid"] == "u-result" and line["session_id"] == "s1"
    assert line["attachment"]["hookName"] == "PostToolUse:Bash" and line["attachment"]["toolUseID"] == "toolu_1"
    assert line["attachment"]["hookEvent"] == "PostToolUse"
    assert line["cwd"] == "/home/r/digits" and line["version"] == "2.1.283"
    assert fp.parse_ts(line["timestamp"]) == pytest.approx(102.5, abs=0.001)
    # One hook run, one additionalContext: every message it delivered, as reads_hook.py renders it.
    assert line["attachment"]["content"] == ["\n\n".join(expected)]
    assert expected[0].startswith("[Probe] Team context") and expected[1].startswith("[Probe] Answer to your ask ask1")
    assert line["rendered"] == [{"content": "<system-reminder>\nPostToolUse:Bash hook additional context: "
                                            + "\n\n".join(expected) + "\n</system-reminder>"}]
    assert [x["text"] for x in d.log] == expected

    # The REAL adapter reads it as a harness line (META) the writer and the reader see.
    events = ClaudeCode().parse_line(line, stream="main", offset=0)
    assert [e.kind for e in events] == [EventKind.META]
    assert events[0].text.startswith(PROBE_MESSAGE_PREFIX) and events[0].text == "\n\n".join(expected)

    # At a prompt: the UserPromptSubmit line, which carries no `session_id`.
    _msg(tmp_path, sid, "m2", "message", now + 2, text="Another team note.")
    prompt = _session_line({"type": "user", "uuid": "u-prompt", "message": {"role": "user", "content": "go on"}})
    line = json.loads(d.on_line(prompt, 200.0, 4))
    assert list(line) == CC_ATTACHMENT_KEYS and list(line["attachment"]) == CC_HOOK_KEYS
    assert line["attachment"]["hookName"] == line["attachment"]["hookEvent"] == "UserPromptSubmit"
    assert line["attachment"]["toolUseID"].startswith("hook-") and line["parentUuid"] == "u-prompt"
    events = ClaudeCode().parse_line(line, stream="main", offset=1)
    assert [e.kind for e in events] == [EventKind.META] and events[0].text.startswith("[Probe] Team context")


def test_the_bench_writes_each_delivery_right_after_the_line_whose_hook_delivered_it(tmp_path):
    import io

    sys.path.insert(0, str(AGENT / "src"))
    bench = _load("bench")
    sid = "s1"
    d = rd.Deliverer(tmp_path, sid)
    prompt = _session_line({"type": "user", "uuid": "u1", "message": {"role": "user", "content": "go"}})
    reply = _session_line({"type": "assistant", "uuid": "u2", "message": {"role": "assistant", "content": [
        {"type": "text", "text": "ok"}]}})
    out = io.BytesIO()
    _msg(tmp_path, sid, "m1", "message", time.time(), text="Prior work: 0.989.")
    for n, raw in enumerate((prompt, reply), 1):
        bench.write_line(out, raw, 100.0 + n, n, d, lambda b: b.replace(b"/home/r", b"/sandbox/r"))
    lines = out.getvalue().splitlines(keepends=True)
    assert len(lines) == 3 and lines[0] == prompt.replace(b"/home/r", b"/sandbox/r") and lines[2] == reply.replace(
        b"/home/r", b"/sandbox/r")
    delivered = json.loads(lines[1])
    assert delivered["attachment"]["type"] == "hook_additional_context" and delivered["cwd"] == "/sandbox/r/digits"
    assert d.log[0]["line"] == 1  # the fixture's line number, not the grown file's
    # The reader off: the recorded lines only.
    out = io.BytesIO()
    bench.write_line(out, prompt, 100.0, 1, None, lambda b: b)
    assert out.getvalue() == prompt


def test_scripted_asks_are_filed_with_the_real_mailbox_in_the_sandbox(tmp_path, monkeypatch):
    sys.path.insert(0, str(AGENT / "src"))
    from probe.daemon import mailbox

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "real-state"))
    lines = [_line("2026-09-24T03:33:28Z"), _line("2026-09-24T03:35:16Z")]
    root = tmp_path / "sandbox" / "probe" / "reads"
    script = rd.AskScript([{"name": "A1", "at": "2026-09-24T03:35:20Z", "question": "Q1?"},
                           {"name": "A0", "after_line": 2, "question": "Q0?"},
                           {"name": "late", "at": "2026-09-25T00:00:00Z", "question": "Q9?"}],
                          lines, root, "sid-1", mailbox)
    script.due(T("2026-09-24T03:35:17Z"))
    assert [a["name"] for a in script.filed] == ["A0"]
    script.due(T("2026-09-24T03:35:21Z"))
    assert [a["name"] for a in script.filed] == ["A0", "A1"]
    with rd.mailbox_at(mailbox, root):
        pending = mailbox.pending_asks("sid-1")
    assert [a.question for a in pending] == ["Q0?", "Q1?"] and {a.id for a in pending} == {
        a["id"] for a in script.filed}
    assert not (tmp_path / "real-state").exists()  # nothing written through the environment's folder
    assert mailbox.root() == tmp_path / "real-state" / "probe" / "reads"  # restored
    assert [a["name"] for a in script.not_filed()] == ["late"]


def _history(prompt: str, *, calls: list[tuple[str, dict, str]], final: str | None):
    from pydantic_ai.messages import (ModelMessagesTypeAdapter, ModelRequest, ModelResponse, ToolCallPart,
                                      ToolReturnPart, UserPromptPart)

    msgs = [ModelRequest(parts=[UserPromptPart(content=prompt)])]
    for i, (tool, args, ret) in enumerate(calls):
        msgs.append(ModelResponse(parts=[ToolCallPart(tool_name=tool, args=args, tool_call_id=f"c{i}")]))
        msgs.append(ModelRequest(parts=[ToolReturnPart(tool_name=tool, content=ret, tool_call_id=f"c{i}")]))
    if final is not None:
        msgs.append(ModelResponse(parts=[ToolCallPart(tool_name="final_result", args={"message": final},
                                                      tool_call_id="f")]))
        msgs.append(ModelRequest(parts=[ToolReturnPart(tool_name="final_result", content="Final result processed.",
                                                       tool_call_id="f")]))
    return msgs, ModelMessagesTypeAdapter


def test_the_readers_conversation_is_read_turn_by_turn():
    pytest.importorskip("pydantic_ai")  # the daemon extra; the release gate runs without it
    one, adapter = _history("──── new since your last look ────\nthe agent runs an SVM",
                            calls=[("search_knowledge", {"query": "svm digits"},
                                    '{"url": "https://research.prbe.ai/runs/' + PRIOR_RUN + '"}')],
                            final="Prior: C=10 got 0.989 " + PRIOR_RUN[:8])
    two, _ = _history("The main agent asks: PCA?", calls=[], final="")
    turns = rd.parse_turns(adapter.dump_json(one + two).decode())
    assert [t["final"] for t in turns] == ["Prior: C=10 got 0.989 " + PRIOR_RUN[:8], ""]
    assert turns[0]["calls"] == [{"tool": "search_knowledge", "args": {"query": "svm digits"}}]
    assert PRIOR_RUN in turns[0]["returns"][0]["text"] and turns[1]["returns"] == []


def test_the_store_is_read_while_the_run_goes_and_a_compaction_loses_nothing(tmp_path):
    pytest.importorskip("pydantic_ai")  # the daemon extra; the release gate runs without it
    sys.path.insert(0, str(AGENT / "src"))
    from probe.daemon.store import Store

    path = tmp_path / "s.sqlite"
    store = Store(path, clock=time.time)
    with store.tx():
        conv = store.start_read_conversation("instructions", "fp")
    one, adapter = _history("look 1", calls=[("entity", {"refs": ["run:x"]}, "https://research.prbe.ai/runs/"
                                               + PRIOR_RUN)], final="m1 " + PRIOR_RUN)
    with store.tx():
        store.save_read_conversation(conv, adapter.dump_json(one).decode(), compactions=0)
        store.add_read_message(message_id="m1", kind="message", text="m1 " + PRIOR_RUN, origin_turn=1)
    watch = rd.StoreWatch(path, every_s=0)
    watch.poll()
    two, _ = _history("look 2", calls=[], final="m2")
    with store.tx():  # the compacted history keeps only the newest turn
        store.save_read_conversation(conv, adapter.dump_json(two).decode(), compactions=1)
    watch.poll()
    turns = watch.ordered_turns()
    assert [t["final"] for t in turns] == ["m1 " + PRIOR_RUN, "m2"]
    assert f"https://research.prbe.ai/runs/{PRIOR_RUN}" in turns[0]["result_links"]
    assert [m["id"] for m in watch.rows["read_messages"]] == ["m1"]
    assert watch.conversations[conv]["compactions"] == 1


def test_links_active_time_and_session_time():
    text = f"See https://research.prbe.ai/runs/{PRIOR_RUN}). Run {PRIOR_RUN[:8]}, 0.98886412 and deadbeef."
    tokens = rd.link_tokens(text)
    assert tokens == {f"https://research.prbe.ai/runs/{PRIOR_RUN}", PRIOR_RUN[:8]}  # the id in the URL is the URL's
    assert PRIOR_RUN in rd.evidence_tokens(text)  # ...but grounds a message that quotes the id alone
    assert "98886412" not in tokens and "deadbeef" not in tokens  # a number, a word: no digit/letter mix
    # Gaps from the start, between lines and to the end, each capped at 5 minutes.
    assert rd.active_seconds([10, 20, 1000, 1010], 0, 2000) == 10 + 10 + 300 + 10 + 300
    assert rd.active_seconds([5000], 0, 2000) == 0.0
    assert rd.session_of(105.0, [(100.0, 5000.0), (103.0, 9000.0)], 2.0) == 9004.0
    # A 429 is an HTTP status in the worker's log, never a timestamp's milliseconds.
    log = ('2026-09-28 08:24:43,429 INFO httpx HTTP Request: POST http://127.0.0.1:1/mcp "HTTP/1.1 200 OK"\n'
           '2026-09-28 08:25:00,001 INFO httpx2 HTTP Request: POST http://x/v1/companion/chat "HTTP/1.1 429 Too '
           'Many Requests"\n')
    assert len(rd.HTTP_429.findall(log)) == 2 and not rd.HTTP_429.findall(log.splitlines()[0])


# ---------------------------------------------------------------------------
# The scorers (synthetic results).
# ---------------------------------------------------------------------------


R1_LABEL = {"name": "R1b best-svm", "before": "2026-09-24T03:42:05Z", "all": ["C\\s*=\\s*10", "gamma\\s*=\\s*0\\.001"],
            "any": ["0\\.989"]}
GOOD = f"Earlier team run old-svm-1 (https://research.prbe.ai/runs/{PRIOR_RUN}): C=10, gamma=0.001 got 0.989."


def _message(mid, text, *, kind="message", made="2026-09-24T03:35:00Z", delivered="2026-09-24T03:35:30Z", **kw):
    return {"id": mid, "kind": kind, "text": text, "made_at": 1000.0, "made_session": T(made),
            "delivered_session": T(delivered) if delivered else None, "ask": kw.pop("ask", None),
            "question": kw.pop("question", None), **kw}


def _result(messages: list[dict], *, turns=None, asks=None, read_asks=None, label_reads=None, **reads) -> dict:
    result = {"fixture": "synthetic", "label": "x-reads-on", "run": 0, "fixture_path": "/nonexistent",
              "final": {"entities": {OWN_RUN: {"slug": "new-lr-1"}}, "created": []},
              "usage_by_lane": {"read": {"rounds": 12, "input_tokens": 600_000, "cached_tokens": 500_000,
                                         "output_tokens": 3000, "cost_usd": 0.9}},
              "reads": {"enabled": True, "messages": messages, "conversation_turns": turns or [],
                        "asks": asks or [], "asks_not_filed": [], "read_asks": read_asks or [],
                        "turns": reads.pop("read_turns", []), "deliveries": [], "active_seconds": 1800,
                        "prior_refs": {PRIOR_RUN: "old-svm-1", PRIOR_PROJECT: "digits-old"},
                        "session_refs": {OWN_RUN: "new-lr-1", OWN_PROJECT: "digits-new"},
                        "rounds_429": reads.pop("rounds_429", 0), "log_429": 0, **reads}}
    result["_label"] = label_reads or {}
    return result


@pytest.fixture(autouse=True)
def _label(monkeypatch):
    monkeypatch.setattr(sr, "answer_key", lambda result: {"reads": result.get("_label") or {}})


def test_r1_counts_an_unasked_message_delivered_before_the_repeat():
    ok = sr.r1(_result([_message("m1", GOOD)]), {"r1": [R1_LABEL]})[0]
    assert ok["pass"] and ok["generated_in_time"] and ok["message"] == "m1"
    late = sr.r1(_result([_message("m1", GOOD, delivered="2026-09-24T03:43:00Z")]), {"r1": [R1_LABEL]})[0]
    assert not late["pass"] and late["generated_in_time"]  # made in time, reached the agent too late
    never = sr.r1(_result([_message("m1", GOOD, delivered=None)]), {"r1": [R1_LABEL]})[0]
    assert not never["pass"] and never["generated_in_time"] and never["delivered_session"] is None
    no_ref = sr.r1(_result([_message("m1", "C=10, gamma=0.001 got 0.989 somewhere")]), {"r1": [R1_LABEL]})[0]
    assert not no_ref["pass"] and no_ref["message"] is None  # the team's record is not named
    by_slug = sr.r1(_result([_message("m1", "old-svm-1: C=10, gamma=0.001 -> 0.989")]), {"r1": [R1_LABEL]})[0]
    assert by_slug["pass"]
    answer = sr.r1(_result([_message("a1", GOOD, kind="answer", ask="q1")]), {"r1": [R1_LABEL]})[0]
    assert not answer["pass"] and answer["via_ask"]  # an ask's answer is R3's, reported apart


def _ask_result(end_kind="answer", text=GOOD, *, reason=None, filed=True):
    asks = [{"name": "A1", "index": 0, "id": "q1", "question": "Q?", "due": 0, "filed_session": T(
        "2026-09-24T03:35:20Z"), "filed_wall": 1000.0}] if filed else []
    msgs = [_message("e1", text, kind=end_kind, ask="q1", question="Q?", made_at=1042.5, reason=reason,
                     delivered="2026-09-24T03:36:20Z")] if end_kind else []
    return _result(msgs, asks=asks, read_asks=[{"id": "q1", "state": "answered"}])


ASK = {"name": "A1", "kinds": ["answer"], "refs": [PRIOR_RUN], "all": ["C=10"], "any": ["0\\.989"],
       "must_not": ["random forest"]}


def test_r3_scores_each_ask_by_its_end_its_facts_and_its_latency():
    row = sr.r3(_ask_result(), {"asks": [ASK]})[0]
    assert row["pass"] and row["kind"] == "answer" and row["latency_s"] == 42.5 and row["delivered_after_s"] == 60.0
    assert not sr.r3(_ask_result("nothing"), {"asks": [ASK]})[0]["pass"]
    wrong = sr.r3(_ask_result(text=GOOD + " A random forest got 0.97."), {"asks": [ASK]})[0]
    assert not wrong["pass"] and "must not" in wrong["why"]
    unnamed = sr.r3(_ask_result(text="C=10 got 0.989"), {"asks": [ASK]})[0]
    assert not unnamed["pass"] and "names none" in unnamed["why"]
    negative = {"name": "A3", "kinds": ["nothing", "answer"], "any": ["\\bno\\b"], "must_not": ["random forest.{0,40}0\\.\\d{3}"]}
    assert sr.r3(_ask_result("nothing", text=""), {"asks": [negative]})[0]["pass"]
    assert sr.r3(_ask_result(text="No, nothing on the digits dataset."), {"asks": [negative]})[0]["pass"]
    assert not sr.r3(_ask_result(text="No: but a random forest got 0.970"), {"asks": [negative]})[0]["pass"]
    failed = sr.r3(_ask_result("failed", text="", reason="the reader is failing"), {"asks": [ASK]})[0]
    assert not failed["pass"] and "failed" in failed["why"]
    missing = sr.r3(_ask_result(None), {"asks": [ASK]})[0]
    assert not missing["pass"] and "no ending message" in missing["why"]


def _turn(order, final, *, result_links=(), prompt_links=(), returns=None, prompt="the agent is sweeping C"):
    return {"conversation": 1, "order": order, "seen_wall": 999.0, "prompt": prompt, "final": final,
            "result_links": list(result_links), "prompt_links": list(prompt_links), "calls": [],
            "returns": returns or [], "retries": 0}


def test_r4_every_link_must_come_from_a_tool_result_the_reader_had():
    url = f"https://research.prbe.ai/runs/{PRIOR_RUN}"
    msgs = [_message("m1", f"See {url} and run {PRIOR_RUN[:8]}."),
            _message("m2", f"Also {OWN_RUN} and https://research.prbe.ai/runs/{PRIOR_PROJECT}")]
    turns = [_turn(0, msgs[0]["text"], result_links=sorted(rd.evidence_tokens(f'{{"url": "{url}"}}'))),
             _turn(1, msgs[1]["text"], prompt_links=[OWN_RUN])]
    out = sr.r4(_result(msgs, turns=turns))
    assert (out["links"], out["from_tool_results"], out["from_session_only"], out["ungrounded"]) == (4, 2, 1, 1)
    assert out["ungrounded_links"] == [{"message": "m2", "link": f"https://research.prbe.ai/runs/{PRIOR_PROJECT}"}]
    assert not out["pass"]
    # A link seen only in a LATER turn does not ground an earlier message.
    later = sr.r4(_result(msgs[:1], turns=[_turn(0, msgs[0]["text"]), _turn(1, "x", result_links=[url])]))
    assert later["ungrounded"] == 2


def test_r5_prose_endings_and_failures_are_counted():
    result = _result([], read_turns=[{"outcome": o, "usd": 0.1} for o in
                                     ("sent", "nothing", "prose", "prose", "stopped", "failed", "answered")],
                     rounds_429=3, turns=[{"order": 0, "calls": [{"tool": "search_knowledge"}, {"tool": "entity"},
                                                                 {"tool": "search_knowledge"}]}])
    five = sr.r5(result)
    assert five["usd_per_active_hour"] == 1.8 and five["active_minutes"] == 30.0
    assert five["tool_calls_per_active_hour"] == {"entity": 2.0, "search_knowledge": 4.0}
    assert five["usd_daemon_priced"] == pytest.approx(0.7)
    out = sr.outcomes(result)
    assert (out["prose_endings"], out["stopped"], out["failed_turns"], out["http_429"]) == (2, 1, 1, 3)


def test_r2_the_judge_is_blind_self_citations_count_apart_and_verdicts_are_cached():
    msgs = [_message("m1", GOOD), _message("m2", "Your own run new-lr-1 got 0.970."),
            _message("a1", "No record.", kind="answer", ask="q1", question="Random forest?")]
    turns = [_turn(0, GOOD, returns=[{"tool": "search_knowledge", "text": "old-svm-1 cv 0.9889"}]),
             _turn(1, msgs[1]["text"]), _turn(2, "No record.")]
    result = _result(msgs, turns=turns)
    seen: list[str] = []

    def call(system, item):
        seen.append(item)
        assert system == sr.JUDGE_PROMPT
        flags = {"irrelevant": False, "stale": False, "unsupported": "0.970" in item, "instruction_like": False}
        return "Here: " + json.dumps({**flags, "why": "checked"})

    cache = sr.judge([result], call=call, cache={})
    assert len(seen) == 3
    for item in seen:  # nothing names the run, the label or the model
        assert "x-reads-on" not in item and "synthetic" not in item and "opus" not in item.lower()
    assert "The agent's question:\n<<<\nRandom forest?" in next(i for i in seen if "No record." in i)
    assert "old-svm-1 cv 0.9889" in next(i for i in seen if "C=10" in i)
    # A later message is judged on everything the reader had by then (it keeps its conversation).
    assert "old-svm-1 cv 0.9889" in next(i for i in seen if "No record." in i)
    two = sr.r2(result, cache)
    assert two["self_citations"] == 1 and two["citations"] == {"prior": 1, "self": 1, "none": 1}
    assert two["counted"] == 2 and two["flags"]["unsupported"] == 0 and two["noise"] == 0
    sr.judge([result], call=call, cache=cache)
    assert len(seen) == 3  # judged once
    assert sr.parse_verdict("no json") is None
    assert sr.parse_verdict('{"irrelevant": 1, "stale": 0, "unsupported": 0, "instruction_like": 0}') == {
        "irrelevant": True, "stale": False, "unsupported": False, "instruction_like": False, "why": ""}


def test_a_message_the_judge_gave_no_verdict_on_is_not_judged_and_never_clean():
    result = _result([_message("m1", GOOD)], turns=[_turn(0, GOOD)])
    calls = []

    def broken(system, item):
        calls.append(item)
        raise RuntimeError("upstream 502")

    cache = sr.judge([result], call=broken, cache={})
    assert len(calls) == 3 and list(cache.values()) == [{"error": "RuntimeError: upstream 502"}]
    two = sr.r2(result, cache)
    assert two["judged"] == 0 and two["counted"] == 0 and two["noise_rate"] is None


def test_a_tool_error_the_reader_got_is_part_of_its_evidence():
    pytest.importorskip("pydantic_ai")  # the daemon extra; the release gate runs without it
    from pydantic_ai.messages import ModelMessagesTypeAdapter, ModelRequest, ModelResponse, RetryPromptPart, ToolCallPart

    msgs, _ = _history("look", calls=[], final=None)
    msgs += [ModelResponse(parts=[ToolCallPart(tool_name="query_sql", args={"sql": "select 1"}, tool_call_id="q")]),
             ModelRequest(parts=[RetryPromptPart(tool_name="query_sql", content="not served: POST /v1/sql",
                                                 tool_call_id="q")])]
    turn = rd.parse_turns(ModelMessagesTypeAdapter.dump_json(msgs).decode())[0]
    assert turn["retries"] == 1 and turn["returns"] == [{"tool": "query_sql", "text": "not served: POST /v1/sql"}]


def test_an_invalid_or_reader_off_result_is_never_scored_as_on():
    invalid = {"fixture": "f", "label": "l", "invalid": True,
               "reads": {"invalid": True, "rebuild": {"reasons": ["prior captured late"]}}}
    assert sr.score_result(invalid) == {"label": "l", "fixture": "f", "run": None, "invalid": True,
                                        "reasons": ["prior captured late"]}
    assert sr.score_result({"fixture": "f", "label": "l", "reads": {"enabled": False}})["enabled"] is False


def test_score_py_skips_an_invalid_result(tmp_path, capsys):
    path = tmp_path / "x-invalid.json"
    path.write_text(json.dumps({"fixture": "f", "label": "l", "invalid": True,
                                "reads": {"invalid": True, "rebuild": {"reasons": ["why"]}}}))
    assert score.load([path]) == []
    assert "INVALID, not scored: why" in capsys.readouterr().out


def test_the_writers_checks_on_vs_off_flag_any_lost_check():
    def fake_score(result):
        return {"checks": dict(result["_checks"]), "metrics": {}, "passed": sum(result["_checks"].values())}

    def arm(enabled, checks):
        return {"fixture": "f", "reads": {"enabled": enabled}, "_checks": checks}

    same = [arm(False, {"E1": True, "E2": True}), arm(True, {"E1": True, "E2": True})]
    ok, lines = sr.writer_compare(same, fake_score)
    assert ok and "NO REGRESSION" in lines[0]
    worse = [arm(False, {"E1": True, "E2": True}), arm(True, {"E1": True, "E2": False})]
    ok, lines = sr.writer_compare(worse, fake_score)
    assert not ok and "lost ['E2']" in lines[0]
    ok, lines = sr.writer_compare([arm(True, {"E1": True})], fake_score)
    assert not ok and "needs both arms" in lines[0]


def test_the_answer_keys_reads_labels_are_well_formed():
    for name in ("daemon-trial-2", "daemon-trial"):
        key = json.loads((EVALS / "expected" / f"{name}.json").read_text())["reads"]
        for spec in key["r1"]:
            assert fp.parse_ts(spec["before"]) is not None
            for pattern in spec.get("all", []) + spec.get("any", []):
                import re

                re.compile(pattern)
        for ask in key["asks"]:
            assert ask["question"] and (fp.parse_ts(ask.get("at")) or ask.get("after_line"))
            assert set(ask.get("kinds") or ["answer"]) <= {"answer", "nothing", "failed"}
    two = json.loads((EVALS / "expected" / "daemon-trial-2.json").read_text())["reads"]
    assert two["prior"] == [{"fixture": "daemon-trial"}] and len(two["r1"]) == 3 and len(two["asks"]) == 3
    # The R1 moments are in the order the session repeated the work.
    befores = [fp.parse_ts(s["before"]) for s in two["r1"]]
    assert befores == sorted(befores)
    # And the labelled facts match the prior result as the as-of-start state shows it.
    blurb = ("An RBF kernel SVM beat logistic regression ... 0.989 against 0.960 ... C of 10.0 and gamma of 0.001 "
             "... a 32 component PCA step before it changed almost nothing")
    assert all(sr.matches(blurb, spec) for spec in two["r1"])
    # The prior values at the precisions the run cards give them (seen in runs).
    assert sr.matches("Winner: C=10, gamma=0.001 (fortunate-quail-346), CV 0.98886 ± 0.00157", two["r1"][1])
    assert sr.matches("PCA32 + SVM (masterful-wildebeest-029): 0.98817 ± 0.00192", two["r1"][2])
    # The PCA verdict is not the SVM's own number: 0.9889 is not 0.988.
    assert not sr.matches("PCA in front of the SVM: 0.9889", two["r1"][2])
    assert not sr.matches("PCA in front of the SVM: 0.98886", two["r1"][2])
    # A3's must-not is a CLAIMED tree-model result, not a search score beside the word (seen in a run).
    a3 = two["asks"][2]
    assert not sr._must_not("A search for random forest, gradient boosting and XGBoost came back empty; every hit "
                            "scored a weak 0.111 and was an SVM", a3)
    assert sr._must_not("A random forest run got 0.972 on the test split.", a3)
    assert sr._must_not("Gradient boosting reached 97.5 % accuracy.", a3)


def test_the_bench_turns_the_reader_on_through_the_workers_env_only():
    pytest.importorskip("pydantic_ai")  # the daemon extra; the release gate runs without it
    bench = _load("bench")
    spec = bench.Spec(SimpleNamespace(), "l", 0, "claude-opus-5-5", "conversation", "recorded", 1.0, None, False, True,
                      False, False, 60.0, reads="on", read_model="claude-opus-5-5")
    assert spec.reads == "on" and spec.read_model == "claude-opus-5-5"
    src = (EVALS / "bench.py").read_text()
    assert 'extra["PROBE_DAEMON_READS"] = "1"' in src and 'extra["PROBE_COMPANION_READ_MODEL"]' in src
    # The reader's MCP is the writer's: one PROBE_MCP_URL at the fake, and the
    # reader builds its URL the same way (agent.mcp_url) -- nothing to route apart.
    sys.path.insert(0, str(AGENT / "src"))
    import inspect

    from probe.daemon import agent as agent_mod

    assert "mcp_url(env.get(\"PROBE_BASE_URL\", \"\"))" in inspect.getsource(agent_mod.build_reader_agent)


def test_the_deliverer_hands_one_more_unasked_message_per_window_of_a_long_turn(tmp_path):
    import json as _json

    from probe.daemon.mailbox import UNASKED_WINDOW_S

    from evals.companion.reads import Deliverer  # noqa: E402

    sid = "s-1"
    d = Deliverer(tmp_path, sid)
    folder = tmp_path / "messages" / sid
    folder.mkdir(parents=True)

    def publish(i):
        (folder / f"{i:020d}-m{i}.json").write_text(_json.dumps({"id": f"m{i}", "session": sid, "kind": "message"}))

    d.on_line(b'{"type": "user", "message": {"content": "go"}}', 0.0, 1)
    publish(1)
    d.deliver(1.0, via="tool")
    publish(2)
    d.deliver(2.0, via="tool")
    assert [e["id"] for e in d.log] == ["m1"], "one per window"
    d.deliver(UNASKED_WINDOW_S + 1.0, via="tool")
    assert [e["id"] for e in d.log] == ["m1", "m2"], "one more ten minutes into the turn"


def test_the_live_bench_scores_ids_and_caps_idle_gaps():
    import importlib.util
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "evals" / "companion" / "live_reads.py"
    spec = importlib.util.spec_from_file_location("_live_reads", path)
    live = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(live)
    assert live.names("see mlp-digits-daemon-b", ["re:mlp-digits-daemon(?!-b)"]) == []
    assert live.names("see mlp-digits-daemon", ["re:mlp-digits-daemon(?!-b)"]) == ["re:mlp-digits-daemon(?!-b)"]
    lines = [("a", 0.0), ("b", 3000.0), ("c", 3030.0)]
    assert live.schedule(lines, speed=1.0, max_gap=120.0) == [0.0, 120.0, 150.0]
    s = live.score({"moments": [{"name": "m", "by_line": 1, "must_any": ["x1"], "must_not": ["own"]}],
                    "asks": []},
                   [{"id": "1", "kind": "message", "text": "x1", "at": 0.5},
                    {"id": "2", "kind": "message", "text": "own", "at": 9.0}], [0.0, 1.0])
    assert s["moments"][0]["passed"], "a look-alike named after the moment does not fail it"


def test_a_fact_that_opts_in_counts_the_targets_tags():
    """The sxs-mlp-daemon-a key says "lr=1.0 counts as flagged by a note on the
    run or a tag"; without `"tags": true` a run the writer tagged `sanity-check`
    (and gave no note) scored as a miss in every arm."""
    run = "4db756cd-d9ed-4080-aae6-199d601d4a82"
    state = {"entities": {run: {"kind": "run", "notes": None, "tags": ["lr-sweep", "sanity-check"]}},
             "edges": []}
    fact = {"name": "lr=1.0 flagged", "targets": [run], "any": ["sanity.check|not a (real )?candidate"]}
    assert score._generic_checks(state, {"facts": [fact]})[0] == {"lr=1.0 flagged": False}
    assert score._generic_checks(state, {"facts": [{**fact, "tags": True}]})[0] == {"lr=1.0 flagged": True}
    state["entities"][run]["tags"] = ["lr-sweep"]
    assert score._generic_checks(state, {"facts": [{**fact, "tags": True}]})[0] == {"lr=1.0 flagged": False}


def test_a_fact_on_every_target_matches_a_document_anywhere():
    """`"targets": "*"` (sxs-mlp-daemon-a-midturn): the researcher's mid-turn
    rule may land on an experiment whose slug the replay made up."""
    state = {"entities": {
        "p1": {"kind": "project", "slug": "mlp-digits-daemon", "notes": "lr sweep done"},
        "e9": {"kind": "experiment", "slug": "replay-made-this", "notes": None,
               "sub_notes": [{"title": "Why 128", "body": "Edge memory budget caps width at 128."}]},
        "r1": {"kind": "run", "notes": None, "tags": ["edge memory budget 128"]}},
        "edges": []}
    fact = {"name": "M1", "all": ["edge|memory budget"], "any": ["128"]}
    assert score._generic_checks(state, {"facts": [{**fact, "targets": "*"}]})[0] == {"M1": True}
    assert score._generic_checks(state, {"facts": [{**fact, "targets": ["mlp-digits-daemon"]}]})[0] == {"M1": False}
    del state["entities"]["e9"]
    assert score._generic_checks(state, {"facts": [{**fact, "targets": ["r1"], "tags": True}]})[0] == {"M1": True}
    assert score._generic_checks(state, {"facts": [{**fact, "targets": "*", "tags": True}]})[0] == {"M1": False}, \
        "tags only count on listed targets"


def _key(name: str) -> dict:
    return json.loads((EVALS / "expected" / f"{name}.json").read_text())


def test_the_midturn_key_is_the_base_key_plus_m1():
    base, midturn = _key("sxs-mlp-daemon-a"), _key("sxs-mlp-daemon-a-midturn")
    assert [f for f in midturn["facts"] if not f["name"].startswith("M1")] == base["facts"]
    assert {k: v for k, v in midturn.items() if k not in ("_doc", "facts")} == \
        {k: v for k, v in base.items() if k not in ("_doc", "facts")}


@pytest.mark.parametrize("text,passes", [
    ("## Constraints\n- The edge device we ship to holds at most 128 hidden units (memory budget).", True),
    ("Move to 128 only if it wins by 0.5 points: the deployment target at the edge can't hold more.", True),
    ("Wider layer (128 units) kept 64: +0.14. See the knowledge base.", False),
    ("knowledge edges: 128 runs, acknowledged", False),
    ("Edge cases: the 128-unit runs stopped early at epoch 12.", False),
])
def test_the_midturn_key_needs_the_edge_constraint_not_any_edge(text, passes):
    [m1] = [f for f in _key("sxs-mlp-daemon-a-midturn")["facts"] if f["name"].startswith("M1")]
    state = {"entities": {"e": {"kind": "experiment", "slug": "x", "notes": text}}, "edges": []}
    assert score._generic_checks(state, {"facts": [m1]})[0][m1["name"]] is passes


def test_the_fake_forwards_only_model_calls(monkeypatch):
    """The daemon's trace shipper posts to `/v1/companion/traces`; the fake used
    to proxy every `/v1/companion/*` path, so a bench's synthetic lines reached
    the real team's trace project with the real key. Only the model routes go
    upstream now; traces get a dark 202 here."""
    pytest.importorskip("starlette")
    import httpx
    from starlette.testclient import TestClient

    sent: list[str] = []

    async def fake_request(self, method, url, **kw):
        sent.append(url)
        return httpx.Response(200, json={"choices": []})

    monkeypatch.setattr(httpx.AsyncClient, "request", fake_request)
    fake = _fake("2026-09-24T03:00:00Z")
    upstream = fp.Upstream(base_url="https://real.invalid", key="real-key")
    auth = {"Authorization": "Bearer bench-fake-t"}
    with TestClient(fp.build_app(fake, upstream=upstream, mcp=False)) as client:
        traces = client.post("/v1/companion/traces", content=b'{"lines": []}', headers=auth)
        other = client.post("/v1/companion/anything", content=b"{}", headers=auth)
        model = client.post("/v1/companion/chat/completions", content=b"{}", headers=auth)
    assert (traces.status_code, traces.json()) == (202, {"dark": True})
    assert other.status_code == 501
    assert model.status_code == 200
    assert sent == ["https://real.invalid/v1/companion/chat/completions"]
    assert [u["path"] for u in fake.unmapped] == ["/v1/companion/traces", "/v1/companion/anything"]


def test_a_note_saying_replaced_by_marks_the_run_superseded():
    """E8: "Replaced by the retry ..." is the writer's commonest way to mark the
    superseded run (8 of 16 daemon-trial-2 runs); the check read only
    "superseded"/"abandoned" and scored those runs as misses."""
    run = "5faaa7c0-ddf6-42b8-89eb-ba467f359981"
    state = {"entities": {run: {"kind": "run", "notes": "Replaced by the retry crystal-trogon-153.", "tags": []}},
             "edges": []}
    assert score._flagged(state, run)
    state["entities"][run]["notes"] = "Test-split evaluation of the chosen SVM."
    assert not score._flagged(state, run)
