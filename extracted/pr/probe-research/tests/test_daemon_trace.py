"""The daemon's session folder (`probe/daemon/trace.py`): the worker's log and
each agent's full trace, one JSON object per line.

Same seams as test_daemon_conversation.py: the model is Pydantic AI's
FunctionModel (or the real OpenAI client on a mock transport), `probe` commands
never reach a server, the chat log is a real file.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import stat
import time
from pathlib import Path

import pytest

pytest.importorskip("pydantic_ai")
pytest.importorskip("pydantic_ai_harness")

from pydantic_ai.models.function import FunctionModel  # noqa: E402

from probe.daemon import store as store_mod  # noqa: E402
from probe.daemon import trace as trace_mod  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402
from tests.test_daemon_conversation import (  # noqa: E402,F401 -- `_isolated` is an autouse fixture
    RUN,
    SID,
    Replay,
    Script,
    _append_turn,
    _compacting,
    _isolated,
    _worker,
)


def _lines(path: Path | None = None) -> list[dict]:
    path = path or trace_mod.session_dir(SID) / "writer.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines()]


def _types(lines: list[dict]) -> list[str]:
    return [line["type"] for line in lines]


def test_a_run_writes_its_full_trace_to_the_sessions_folder(tmp_path, monkeypatch):
    script = Script([("shell", f"probe run tag {RUN} svm"), ("done", "tagged the run")])
    w = _worker(tmp_path, model=FunctionModel(script, model_name="m"), replay=Replay(), mode="conversation",
                monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    folder = tmp_path / "state" / "probe" / "daemon" / "sessions" / SID
    assert trace_mod.session_dir(SID) == folder
    lines = _lines()
    assert _types(lines) == ["run_start", "tools", "instructions", "call_start", "call", "tool", "call_start",
                             "call", "run_end"]
    start, tools, instructions, _, first, tool, _, second, end = lines
    run = start["run"]
    trace = f"{SID}:writer:{run}"
    # Every line stands alone: its run and trace, and a step's own span and parent.
    assert all(line["agent"] == "writer" and line["ts"].endswith("Z") for line in lines)
    assert all(line["run"] == run and line["trace_id"] == trace for line in lines)
    assert start["trigger"] == "turn end" and start["mode"] == "conversation" and start["history_messages"] == 0
    assert {t["name"] for t in tools["tools"]} >= {"shell", "read", "session"}
    assert "You are the Probe daemon" in instructions["text"]
    # A call holds what it ADDS (the prompt, never the job description again) and the answer.
    assert first["span_id"] == f"{trace}:r1" and first["parent_id"] == trace
    assert "sweep C for an SVM" in json.dumps(first["input"]) and first["instructions_sha"] == instructions["sha256"]
    call = next(p for p in first["output"]["parts"] if p["part_kind"] == "tool-call")
    assert call["tool_name"] == "shell" and f"probe run tag {RUN} svm" in json.dumps(call["args"])
    assert first["output"]["model_name"] == "m" and "usage" in first["output"] and first["latency_ms"] >= 0
    assert tool["tool"] == "shell" and tool["call_id"] == call["tool_call_id"] and tool["outcome"] == "ok"
    assert tool["args"]["command"] == f"probe run tag {RUN} svm"
    assert tool["parent_id"] == first["span_id"] and tool["span_id"] == f"{trace}:r1:{call['tool_call_id']}"
    assert tool["result"] and tool["duration_ms"] >= 0
    returned = next(p for p in second["input"] if p["part_kind"] == "tool-return")
    assert returned["content"] == tool["result"], "the next call's input holds the real result"
    assert end["outcome"] == "done"
    assert stat.S_IMODE(folder.stat().st_mode) == 0o700
    assert stat.S_IMODE((folder / "writer.jsonl").stat().st_mode) == 0o600


def test_a_resumed_conversation_writes_only_what_is_new(tmp_path, monkeypatch):
    first = Script([("shell", f"probe run tag {RUN} svm"), ("done", "tagged the run")])
    w = _worker(tmp_path, model=FunctionModel(first), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    _append_turn(w.session.transcript, "NEWPROMPT: now try an RBF kernel")
    w2 = _worker(tmp_path, model=FunctionModel(Script([("done", "nothing new")])), replay=Replay(),
                 mode="conversation", monkeypatch=monkeypatch)
    w2.read_new()
    assert asyncio.run(w2.run_bite("prompt")) is True
    lines = _lines()
    starts = [line for line in lines if line["type"] == "run_start"]
    assert len(starts) == 2 and starts[1]["history_messages"] > 0 and starts[0]["run"] != starts[1]["run"]
    inputs = [json.dumps(line["input"]) for line in lines if line["type"] == "call"]
    assert sum("sweep C for an SVM" in i for i in inputs) == 1, "the carried history is not written again"
    assert "NEWPROMPT" in inputs[-1]


def test_a_compaction_is_traced_with_its_summary(tmp_path, monkeypatch):
    _compacting(monkeypatch)
    script = Script([("shell", f"probe run tag {RUN} svm"), ("shell", "ls"), ("done", "tagged")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert script.summaries >= 1
    lines = _lines()
    rewritten = [line for line in lines if line["type"] == "history_rewritten"]
    assert len(rewritten) == script.summaries, "one line per compaction"
    assert rewritten[0]["round"] == 2 and "SUMMARY: the digits SVM sweep" in json.dumps(rewritten[0]["head"])
    first = next(line for line in lines if line["type"] == "call")
    assert "sweep C for an SVM" in json.dumps(first["input"]), "what the summary replaced stays in the trace"


def test_a_model_call_that_raises_is_traced_with_what_it_was_sent(tmp_path, monkeypatch):
    from pydantic_ai.exceptions import ModelHTTPError

    def refuse(messages, info):
        raise ModelHTTPError(503, "default", body={"error": {"message": "upstream down"}})

    w = _worker(tmp_path, model=FunctionModel(refuse), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is False
    lines = _lines()
    error = next(line for line in lines if line["type"] == "model_error")
    assert error["status"] == 503 and "upstream down" in error["error"] and error["latency_ms"] >= 0
    assert "sweep C for an SVM" in json.dumps(error["input"]), "what the failed call was sent"
    assert error["parent_id"] == error["trace_id"] and error["span_id"] == f"{error['trace_id']}:r1"
    assert lines[-1]["type"] == "run_end" and lines[-1]["outcome"] == "failed"


def test_a_tool_that_raises_is_traced_and_still_raises(tmp_path):
    from pydantic_ai.messages import ToolCallPart

    trace = trace_mod.TraceFile(SID, "writer")
    trace.start_run(7)
    recording = trace_mod.Recording(trace=trace, rounds=2)

    async def boom(args):
        raise RuntimeError("the disk went away")

    call = ToolCallPart("read", {"path": "/data/x.csv"}, tool_call_id="c9")
    with pytest.raises(RuntimeError):
        asyncio.run(recording.wrap_tool_execute(None, call=call, tool_def=None, args={"path": "/data/x.csv"},
                                                handler=boom))
    line = _lines()[-1]
    assert line["type"] == "tool" and line["outcome"] == "RuntimeError" and "disk went away" in line["error"]
    assert line["args"] == {"path": "/data/x.csv"} and line["parent_id"] == f"{SID}:writer:7:r2"
    assert line["run"] == 7 and "result" not in line


def test_a_paused_run_ends_with_its_outcome(tmp_path, monkeypatch):
    monkeypatch.setattr(worker_mod, "ROUNDS_BEFORE_YIELD", 1)
    script = Script([("shell", "ls a"), ("shell", "ls b"), ("done", "ok")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=Replay(), mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    ends = [line for line in _lines() if line["type"] == "run_end"]
    assert ends and ends[0]["outcome"] == "paused"


def test_the_worker_entry_point_logs_into_the_sessions_folder(tmp_path, monkeypatch):
    """`main` installs the handlers before anything can fail (here: no daemon key)."""
    root = logging.getLogger()
    before = list(root.handlers)
    monkeypatch.setattr(root, "handlers", [])
    monkeypatch.setattr(root, "level", root.level)
    for name in trace_mod.NOISY_LOGGERS:
        monkeypatch.setattr(logging.getLogger(name), "level", logging.getLogger(name).level)
    try:
        code = worker_mod.main(["--session-id", SID, "--transcript", str(tmp_path / "t.jsonl"),
                                "--cwd", str(tmp_path)])
        assert code == worker_mod.EXIT_DO_NOT_RESPAWN
        files = [h for h in root.handlers if isinstance(h, logging.FileHandler)]
        assert [Path(h.baseFilename) for h in files] == [trace_mod.session_dir(SID) / trace_mod.WORKER_LOG]
        assert logging.getLogger("httpx").level == logging.WARNING
    finally:
        logging.captureWarnings(False)
        for h in root.handlers:
            if h not in before:
                h.close()


def test_tracing_changes_nothing_the_model_is_sent(tmp_path, monkeypatch):
    """The trace only observes: with it on and off, the gateway receives the
    same bytes (so it cannot move the replay bench)."""
    import httpx
    from openai import AsyncOpenAI
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider

    def bodies_for(setting: str, root: Path) -> list[dict]:
        monkeypatch.setenv(trace_mod.ENV_TRACE, setting)
        monkeypatch.setenv("XDG_STATE_HOME", str(root / "state"))
        (root / "state" / "probe" / "sessions").mkdir(parents=True)
        (root / "state" / "probe" / "sessions" / f"{SID}.state").write_text("daemon")
        bodies: list[dict] = []

        def handler(request: httpx.Request) -> httpx.Response:
            body = json.loads(request.content)
            bodies.append(body)
            n = len(bodies)
            if n == 1:
                call = {"name": "shell", "arguments": json.dumps({"command": "ls", "why": "look"})}
            else:
                final = next(t["function"]["name"] for t in body["tools"]
                             if t["function"]["name"].startswith("final"))
                call = {"name": final, "arguments": json.dumps({"summary": "done"})}
            return httpx.Response(200, json={
                "id": f"r{n}", "object": "chat.completion", "created": 1, "model": "gemini-3.8-flash",
                "choices": [{"index": 0, "finish_reason": "tool_calls", "message": {
                    "role": "assistant", "content": None,
                    "tool_calls": [{"id": f"c{n}", "type": "function", "function": call}]}}],
                "usage": {"prompt_tokens": 1000, "completion_tokens": 50, "total_tokens": 1050}})

        client = AsyncOpenAI(base_url="https://gateway.test/v1/companion", api_key="k",
                             http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)))
        model = OpenAIChatModel("default", provider=OpenAIProvider(openai_client=client))
        w = _worker(root, model=model, replay=Replay(), mode="conversation", monkeypatch=monkeypatch,
                    clock=lambda: 1_000_000.0)
        w.read_new()
        assert asyncio.run(w.run_bite("turn end")) is True
        return bodies

    # Same-length roots: the chat log's byte offsets (shown to the model) follow its paths.
    on = bodies_for("on", tmp_path / "t1")
    off = bodies_for("off", tmp_path / "t2")
    assert len(on) == 2 and on == off
    assert (tmp_path / "t1" / "state" / "probe" / "daemon" / "sessions" / SID / "writer.jsonl").exists()
    assert not (tmp_path / "t2" / "state" / "probe" / "daemon" / "sessions" / SID / "writer.jsonl").exists()


def test_a_trace_that_cannot_be_written_never_fails_the_bite(tmp_path, monkeypatch, caplog):
    trace_mod.sessions_dir().parent.mkdir(parents=True, exist_ok=True)
    trace_mod.sessions_dir().write_text("a file where the folder should be")
    w = _worker(tmp_path, model=FunctionModel(Script([("shell", "ls"), ("done", "ok")])), replay=Replay(),
                mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    with caplog.at_level(logging.WARNING, logger="probe.daemon"):
        assert asyncio.run(w.run_bite("turn end")) is True
    assert w.trace.off
    assert sum("the writer trace is off for this process" in r.getMessage() for r in caplog.records) == 1


def test_a_full_trace_stops_with_one_line_and_the_bite_goes_on(tmp_path, monkeypatch):
    monkeypatch.setenv(trace_mod.ENV_TRACE_MAX_MB, str(2_000 / 1024 / 1024))
    w = _worker(tmp_path, model=FunctionModel(Script([("shell", "ls"), ("done", "ok")])), replay=Replay(),
                mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    lines = _lines()
    assert lines[-1]["type"] == "trace_full" and _types(lines).count("trace_full") == 1
    assert (trace_mod.session_dir(SID) / "writer.jsonl").stat().st_size <= 2_000


def test_the_worker_logs_into_the_sessions_folder_and_warnings_reach_stderr_too(tmp_path):
    handlers = trace_mod.log_handlers(SID)
    by_type = {type(h): h for h in handlers}
    into_file = by_type[logging.FileHandler]
    assert Path(into_file.baseFilename) == trace_mod.session_dir(SID) / trace_mod.WORKER_LOG
    assert by_type[logging.StreamHandler].level == logging.WARNING
    into_file.close()


def test_the_per_request_http_lines_stay_out_of_the_log(monkeypatch):
    root = logging.getLogger()
    monkeypatch.setattr(root, "level", logging.INFO)
    for name in trace_mod.NOISY_LOGGERS:
        monkeypatch.setattr(logging.getLogger(name), "level", logging.NOTSET)
    trace_mod.quiet_noisy_loggers()
    assert all(logging.getLogger(n).level == logging.WARNING for n in trace_mod.NOISY_LOGGERS)


def test_stale_session_folders_are_swept_with_their_store(tmp_path):
    base = store_mod.state_dir()
    old = time.time() - 40 * 86400
    for sid in ("dead", "recent", SID):
        folder = trace_mod.session_dir(sid)
        folder.mkdir(parents=True)
        (folder / "writer.jsonl").write_text("{}\n")
        (base / f"{sid}.sqlite").write_text("x")
        if sid != "recent":
            for p in (folder / "writer.jsonl", folder, base / f"{sid}.sqlite"):
                os.utime(p, (old, old))
    # A folder whose own time is old but whose trace is being appended to is not stale.
    appended = trace_mod.session_dir("appended")
    appended.mkdir(parents=True)
    (appended / "writer.jsonl").write_text("{}\n")
    os.utime(appended, (old, old))
    assert worker_mod.sweep_stale(SID) == 2
    left = sorted(p.name for p in trace_mod.sessions_dir().iterdir())
    assert left == sorted(["appended", "recent", SID])


def test_status_names_each_sessions_folder(tmp_path):
    from typer.testing import CliRunner

    from probe.cli import daemon_cli

    store_mod.Store(store_mod.store_path(SID)).close()
    trace_mod.session_dir(SID).mkdir(parents=True)
    out = CliRunner().invoke(daemon_cli.daemon_app, ["status"]).output
    assert f"  log and traces: {trace_mod.session_dir(SID)}" in out
    data = json.loads(CliRunner().invoke(daemon_cli.daemon_app, ["status", "--json"]).output)
    assert data["sessions"][0]["folder"] == str(trace_mod.session_dir(SID))


def test_the_lines_keep_every_field_the_server_maps(tmp_path, monkeypatch):
    """The server's mapping (`app/observability/daemon_trace.py`) is tested on a
    recorded trace, `tests/fixtures/daemon_trace/writer.jsonl`. A line type the
    daemon still writes must still carry every field that recording has, or the
    server test proves a shape nobody sends. (Re-record the fixture when a field
    is added on purpose.)"""
    fixture = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "daemon_trace" / "writer.jsonl"
    def paths(value, prefix=""):
        """Dotted key paths, into dicts and the first item of lists (the server
        reads `output.usage.*`, `output.parts[].part_kind`, `input[].part_kind`)."""
        out = set()
        if isinstance(value, dict):
            for key, child in value.items():
                out.add(prefix + key)
                if key not in ("text", "tools", "head", "result", "args"):  # free-form content
                    out |= paths(child, prefix + key + ".")
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            out |= paths(value[0], prefix.rstrip(".") + "[].")
        return out

    recorded: dict[str, set[str]] = {}
    for raw in fixture.read_text().splitlines():
        line = json.loads(raw)
        recorded.setdefault(line["type"], set()).update(paths(line))
    _compacting(monkeypatch)
    script = Script([("shell", f"probe run tag {RUN} svm"), ("shell", "ls"), ("done", "tagged the run")])
    w = _worker(tmp_path, model=FunctionModel(script, model_name="m"), replay=Replay(), mode="conversation",
                monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    fresh: dict[str, set[str]] = {}
    for line in _lines():
        fresh.setdefault(line["type"], set()).update(paths(line))
    assert set(fresh) - {"model_error"} <= set(recorded)
    for kind, keys in fresh.items():
        missing = recorded.get(kind, set()) - keys
        assert not missing, f"{kind} lines no longer carry {sorted(missing)}"
