"""Engineering pings for daemon errors: `daemon.error` -> PostHog -> #eng-alerts.

Every case runs the real worker or reader path with real Pydantic AI exceptions
and is read at the telemetry sender's queue (the record that would go on the
wire), never at a mock of `alerts.report`.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import time
from pathlib import Path

import pytest

pytest.importorskip("pydantic_ai")

import httpx  # noqa: E402
from pydantic_ai.exceptions import ContentFilterError, ModelAPIError, ModelHTTPError  # noqa: E402
from pydantic_ai.messages import ModelResponse, ToolCallPart  # noqa: E402
from pydantic_ai.models.function import FunctionModel  # noqa: E402

from probe._shared import telemetry as tm  # noqa: E402
from probe.sdk import _telemetry_core as core  # noqa: E402
from probe.daemon import alerts  # noqa: E402
from probe.daemon import lease, mailbox  # noqa: E402
from probe.daemon import reader_lane as rl  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402

try:
    ExceptionGroup
except NameError:  # Python 3.10
    from exceptiongroup import ExceptionGroup  # noqa: A004

SID = "11111111-2222-3333-4444-555555555555"
DESTINATION = Path(__file__).resolve().parents[2] / "scripts" / "deploy" / "posthog-daemon-error-alerts.json"
HOSTED = "https://api.research.prbe.ai"
#: Stamped by the pipe on every event, not by `alerts.report`.
PIPE_KEYS = {"session_id", "via", "invoked_by", "identity_mode", "agent"}
EVENT_KEYS = {"kind", "lane", "daemon_session", "error_type", "status", "code", "count", "error_text"}


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """No real config, key or MCP; telemetry ON with the sender's queue captured
    (no thread, no network); the daemon pointed at the hosted API."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    for var in ("PROBE_DAEMON_KEY", "PROBE_BASE_URL", "PROBE_TOKEN", "PROBE_MCP_TOKEN"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    monkeypatch.delenv(worker_mod.ENV_MODE, raising=False)
    monkeypatch.delenv(mailbox.ENV_READS, raising=False)
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    monkeypatch.delenv("PROBE_DIAGNOSTICS", raising=False)
    (tmp_path / "state" / "probe" / "sessions").mkdir(parents=True)
    (lease.sessions_dir() / f"{SID}.state").write_text("daemon")
    monkeypatch.setattr(alerts, "_base_url", HOSTED)


@pytest.fixture()
def sent(monkeypatch) -> list[dict]:
    records: list[dict] = []
    monkeypatch.setattr(tm, "_sender", None)
    monkeypatch.setattr(tm, "_flush_registered", True)  # keep atexit out of tests
    monkeypatch.setattr(tm._Sender, "start", lambda self: None)
    monkeypatch.setattr(tm._Sender, "put", lambda self, rec: records.append(rec))
    return records


def _pings(records: list[dict]) -> list[dict]:
    return [r["properties"] for r in records if r["event"] == tm.EVENT_DAEMON_ERROR]


def _line(obj: dict) -> str:
    return json.dumps(obj) + "\n"


def _worker(tmp_path: Path, *, model=None, clock=time.time) -> worker_mod.Worker:
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True, exist_ok=True)
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(
        _line({"type": "permission-mode", "permissionMode": "default"})
        + _line({"type": "user", "message": {"content": "sweep C for an SVM on digits"}, "cwd": str(work)})
        + _line({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "python sweep.py"}}]}})
        + _line({"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": "t1", "content": "svm acc=0.9889"}]}})
        + _line({"type": "assistant", "message": {"content": [{"type": "text", "text": "SVM C=10: 0.9889."}]}})
        + _line({"type": "system", "subtype": "turn_duration", "durationMs": 5})
    )
    return worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                             clock=clock, replay=_Replay(), model=model)


class _Replay:
    async def run(self, argv, op_id):
        return 0, json.dumps({"ok": True})


def _raising(exc: BaseException) -> FunctionModel:
    def fn(messages, info):
        raise exc

    return FunctionModel(fn)


def _mcp_http_error(status: int) -> httpx.HTTPStatusError:
    """What the Probe MCP's client raises on an HTTP refusal (`raise_for_status`)."""
    req = httpx.Request("POST", "https://mcp.research.prbe.ai/mcp")
    return httpx.HTTPStatusError(f"Client error '{status}'", request=req, response=httpx.Response(status, request=req))


def _mcp_connect_error() -> RuntimeError:
    """What the Probe MCP's client raises when it cannot connect (fastmcp, `from exception`)."""
    try:
        try:
            raise httpx.ConnectError("All connection attempts failed")
        except httpx.ConnectError as inner:
            raise RuntimeError(f"Client failed to connect: {inner}") from inner
    except RuntimeError as outer:
        return outer


def _bite(w: worker_mod.Worker) -> bool:
    w.next_attempt_at = 0.0
    return asyncio.run(w.run_bite("turn end"))


# -- the writer's failed bites -------------------------------------------------


def test_a_content_filter_refusal_pings_once_with_its_first_line(tmp_path, sent):
    """The anthrogen loop (923 refusals, 10-03 to 10-07): one ping, not one per retry."""
    refusal = ContentFilterError("Content filter triggered. Finish reason: 'content_filter'",
                                 body='[{"parts": [], "usage": {"input_tokens": 852619}}]')
    w = _worker(tmp_path, model=_raising(refusal))
    w.read_new()
    assert _bite(w) is False and _bite(w) is False
    [ping] = _pings(sent)
    assert ping["kind"] == alerts.Kind.MODEL_REFUSED and ping["lane"] == "write"
    assert ping["daemon_session"] == SID and ping["error_type"] == "ContentFilterError"
    assert ping["error_text"] == ("ContentFilterError: Content filter triggered. Finish reason: "
                                  "'content_filter', body:")
    assert set(ping) - PIPE_KEYS <= EVENT_KEYS


def test_a_4xx_the_route_refused_pings_as_rejected_with_the_servers_code(tmp_path, sent):
    body = {"error": {"code": "context_length_exceeded", "message": "prompt is too long"}}
    w = _worker(tmp_path, model=_raising(ModelHTTPError(400, "default", body=body)))
    w.read_new()
    _bite(w)
    [ping] = _pings(sent)
    assert ping["kind"] == alerts.Kind.MODEL_REJECTED
    assert ping["status"] == 400 and ping["code"] == "context_length_exceeded"


def test_a_bug_in_the_daemon_pings_as_bite_failed(tmp_path, sent):
    w = _worker(tmp_path, model=_raising(RuntimeError("dictionary changed size during iteration")))
    w.read_new()
    _bite(w)
    [ping] = _pings(sent)
    assert ping["kind"] == alerts.Kind.BITE_FAILED and ping["error_type"] == "RuntimeError"
    assert ping["error_text"] == "RuntimeError: dictionary changed size during iteration"


@pytest.mark.parametrize("error", [
    ModelHTTPError(401, "default"),
    ModelHTTPError(403, "default", body={"code": "companion_disabled", "message": "m"}),
    ModelHTTPError(402, "default"),
    ModelHTTPError(408, "default"),
    ModelHTTPError(429, "default", body={"error": {"code": "budget_exhausted"}}),
    ModelHTTPError(429, "default", body={"error": {"code": "rate_limited"}}),
    ModelHTTPError(504, "default", body={"error": {"code": "gateway_timeout"}}),
    RuntimeError("the team's budget is spent"),
    ModelAPIError("default", "Connection error."),
    httpx.ConnectError("[Errno 111] Connection refused"),
    _mcp_connect_error(),
    _mcp_http_error(401),
    ExceptionGroup("unhandled errors in a TaskGroup", [httpx.ConnectError("refused")]),
    ModelHTTPError(502, "default"),  # once: a 5xx pings only when the lease is given back over it
], ids=["401", "403-team", "402", "408", "429-budget-text", "429-rate", "504-timeout", "budget-text", "no-answer",
        "connect", "mcp-connect", "mcp-401", "grouped-offline", "one-502"])
def test_what_the_researcher_fixes_or_what_passes_does_not_ping(tmp_path, sent, error):
    w = _worker(tmp_path, model=_raising(error))
    w.read_new()
    assert _bite(w) is False
    assert _pings(sent) == []


def test_the_gateway_failing_5xx_in_a_row_pings_when_the_lease_goes_back(tmp_path, sent):
    w = _worker(tmp_path, model=_raising(ModelHTTPError(502, "default")))
    w.read_new()
    _bite(w)
    assert _pings(sent) == []
    _bite(w)
    assert w.released_reason == lease.REASON_GATEWAY
    [ping] = _pings(sent)
    assert ping["kind"] == alerts.Kind.GATEWAY_DOWN and ping["status"] == 502
    assert ping["count"] == worker_mod.GATEWAY_FAILURES_BEFORE_RELEASE


def test_the_models_timeout_in_a_row_does_not_ping(tmp_path, sent):
    """504 is the gateway saying the model did not answer in time: a timeout."""
    w = _worker(tmp_path, model=_raising(ModelHTTPError(504, "default")))
    w.read_new()
    for _ in range(worker_mod.GATEWAY_FAILURES_BEFORE_RELEASE + 1):
        _bite(w)
    assert w.released_reason == lease.REASON_GATEWAY
    assert _pings(sent) == []


def test_the_mcp_answering_5xx_is_ours_and_pings(tmp_path, sent):
    w = _worker(tmp_path, model=_raising(_mcp_http_error(502)))
    w.read_new()
    _bite(w)
    [ping] = _pings(sent)
    assert ping["kind"] == alerts.Kind.BITE_FAILED and ping["status"] == 502


def test_no_answer_in_a_row_is_the_network_and_does_not_ping(tmp_path, sent):
    w = _worker(tmp_path, model=_raising(ModelAPIError("default", "Request timed out.")))
    w.read_new()
    for _ in range(worker_mod.GATEWAY_FAILURES_BEFORE_RELEASE + 1):
        _bite(w)
    assert w.released_reason == lease.REASON_GATEWAY
    assert _pings(sent) == []


# -- the writer's own findings ---------------------------------------------------


def _busy(messages, info):
    return ModelResponse(parts=[ToolCallPart("shell", {"command": "ls", "why": "test"})])


@pytest.mark.parametrize(("mode", "how"), [
    ("conversation", "the loop detector stopped 2 bites in a row"),  # no request cap: the repeated `ls` loops
    ("bites", "2 bites in a row hit their limits"),
])
def test_skipped_events_ping_with_how_many(tmp_path, sent, monkeypatch, mode, how):
    monkeypatch.setenv(worker_mod.ENV_MODE, mode)
    monkeypatch.setattr(worker_mod, "BITE_REQUESTS", 2)
    w = _worker(tmp_path, model=FunctionModel(_busy))
    w.read_new()
    _bite(w)
    assert _pings(sent) == [], "one cut-short bite is retried smaller, not skipped"
    _bite(w)
    skipped = w.store.recent_bites(1)[0]
    assert skipped["outcome"] == "cut short: skipped"
    [ping] = _pings(sent)
    assert ping["kind"] == alerts.Kind.EVENTS_SKIPPED
    assert ping["count"] == skipped["last_seq"] - skipped["first_seq"] + 1
    assert ping["error_text"] == f"{ping['count']} events skipped: {how}"


def test_a_rewritten_chat_log_pings(tmp_path, sent):
    w = _worker(tmp_path)
    w.read_new()
    w._stop_stream("main", 1234, "the bytes before the cursor changed")
    [ping] = _pings(sent)
    assert ping["kind"] == alerts.Kind.CHAT_LOG_REWRITTEN
    assert ping["error_text"] == "chat log (main) rewritten in place: the bytes before the cursor changed"


def test_an_unreadable_switch_pings_when_the_worker_stops(tmp_path, sent):
    now = [1000.0]
    w = _worker(tmp_path, clock=lambda: now[0])
    assert w._switch_unreadable() is None
    now[0] += worker_mod.SWITCH_UNREADABLE_EXIT_S + 1
    assert w._switch_unreadable() == worker_mod.EXIT_RESPAWN_LATER
    [ping] = _pings(sent)
    assert ping["kind"] == alerts.Kind.SWITCH_UNREADABLE


# -- the reader ------------------------------------------------------------------


def _lane(w: worker_mod.Worker, exc: BaseException) -> rl.ReaderLane:
    w.read_new()
    return rl.ReaderLane(w, model=_raising(exc))


def test_the_reader_failing_twice_in_a_row_pings(tmp_path, sent):
    lane = _lane(_worker(tmp_path), RuntimeError("tool schema rejected"))
    asyncio.run(lane.run_turn("ask"))
    assert _pings(sent) == []
    lane.next_attempt_at = 0.0
    asyncio.run(lane.run_turn("ask"))
    [ping] = _pings(sent)
    assert ping["kind"] == alerts.Kind.READER_FAILING and ping["lane"] == "read"
    assert ping["count"] == rl.READ_FAILURES_TO_REPORT


@pytest.mark.parametrize("error", [
    httpx.ConnectError("[Errno 111] Connection refused"),
    _mcp_connect_error(),
    ExceptionGroup("unhandled errors in a TaskGroup", [httpx.ConnectError("refused")]),
    ModelHTTPError(401, "reader"),
    ModelHTTPError(402, "reader"),
    ModelHTTPError(403, "reader"),
    ModelHTTPError(408, "reader"),
    ModelHTTPError(429, "reader"),
    ModelHTTPError(504, "reader"),
    _mcp_http_error(401),
    ExceptionGroup("unhandled errors in a TaskGroup", [_mcp_http_error(401)]),
], ids=["offline", "mcp-connect", "grouped-offline", "401", "402", "403", "408", "429", "504", "mcp-401",
        "grouped-mcp-401"])
def test_the_reader_offline_or_refused_does_not_ping(tmp_path, sent, error):
    lane = _lane(_worker(tmp_path), error)
    for _ in range(rl.READ_FAILURES_TO_REPORT):
        lane.next_attempt_at = 0.0
        asyncio.run(lane.run_turn("ask"))
    assert _pings(sent) == []


def _outline(messages, info):
    return ModelResponse(parts=[ToolCallPart("session", {"op": "outline"})])


def _done(messages, info):
    return ModelResponse(parts=[ToolCallPart("final_result", {"message": ""})])


def test_a_reader_turn_out_of_rounds_pings_with_its_limit(tmp_path, sent, monkeypatch):
    from probe.daemon import agent as agent_mod

    monkeypatch.setattr(agent_mod, "READ_ROUNDS", 3)
    w = _worker(tmp_path)
    w.read_new()
    got = asyncio.run(rl.ReaderLane(w, model=FunctionModel(_outline)).run_turn("prompt"))
    assert got.outcome == rl.Outcome.STOPPED
    [ping] = _pings(sent)
    assert ping["kind"] == alerts.Kind.READER_STOPPED and ping["lane"] == "read"
    assert ping["error_text"] == "reader turn stopped: 3 model rounds"


def test_a_reader_turn_that_ends_on_its_own_does_not_ping(tmp_path, sent):
    w = _worker(tmp_path)
    w.read_new()
    got = asyncio.run(rl.ReaderLane(w, model=FunctionModel(_done)).run_turn("prompt"))
    assert got.outcome == rl.Outcome.NOTHING
    assert _pings(sent) == []


# -- a crash ---------------------------------------------------------------------


def test_a_crash_pings_and_sends_its_stack(tmp_path, sent, monkeypatch):
    monkeypatch.setenv("PROBE_DAEMON_KEY", "pk_test_daemon")
    monkeypatch.setenv("PROBE_BASE_URL", HOSTED)
    monkeypatch.setenv("PROBE_DIAGNOSTICS", "on")
    monkeypatch.setattr(alerts, "_base_url", None)  # main() sets it from the endpoint
    monkeypatch.setattr(tm, "_flush_at_exit", lambda: None)
    monkeypatch.setattr(tm, "_current", None)

    class Broken:  # a LookupError would be read as a missing session (EXIT_DO_NOT_RESPAWN), not a crash
        def __init__(self, *a, **kw):
            raise ValueError("not enough values to unpack (expected 2, got 1)")

    monkeypatch.setattr(worker_mod, "Worker", Broken)
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text("")
    code = worker_mod.main(["--session-id", SID, "--transcript", str(transcript), "--cwd", str(tmp_path)])
    assert code == worker_mod.EXIT_CRASHED
    [ping] = _pings(sent)
    assert ping["kind"] == alerts.Kind.CRASHED and ping["error_type"] == "ValueError"
    assert ping["error_text"] == "ValueError: not enough values to unpack (expected 2, got 1)"
    [crash] = [r["properties"] for r in sent if r["event"] == "$exception"]
    assert crash["surface"] == "daemon" and crash["$exception_list"][0]["type"] == "ValueError"


# -- gates and the error text ----------------------------------------------------


def test_telemetry_off_sends_nothing(sent, monkeypatch):
    monkeypatch.setenv("PROBE_TELEMETRY", "off")
    assert alerts.report(alerts.Kind.BITE_FAILED, session_id=SID, lane="write", exc=RuntimeError("x")) is False
    assert _pings(sent) == []


@pytest.mark.parametrize("base_url", [None, "https://probe.internal.corp"], ids=["unknown", "self-hosted"])
def test_an_unknown_or_self_hosted_backend_sends_nothing(sent, monkeypatch, base_url):
    monkeypatch.setattr(alerts, "_base_url", base_url)
    assert alerts.report(alerts.Kind.BITE_FAILED, session_id=SID, lane="write", exc=RuntimeError("x")) is False
    assert _pings(sent) == []


def test_a_new_error_type_of_the_same_kind_pings_again(sent):
    for exc in (RuntimeError("a"), RuntimeError("b"), KeyError("c")):
        alerts.report(alerts.Kind.BITE_FAILED, session_id=SID, lane="write", exc=exc)
    assert [p["error_type"] for p in _pings(sent)] == ["RuntimeError", "KeyError"]


def test_the_error_text_is_one_scrubbed_line_with_no_home_folder():
    home = str(Path.home())
    key = "sk-ant-api03-" + "A" * 93 + "AA"
    exc = RuntimeError(f"cannot read {home}/work/run.py with key {key}\nTraceback: second line")
    text = alerts.error_text(exc)
    assert "\n" not in text and "second line" not in text
    assert home not in text and "~/work/run.py" in text
    assert key not in text and "sk-ant-api03-AAAA" not in text
    assert len(alerts.error_text("x" * 5000)) == alerts.ERROR_TEXT_CHARS


def test_a_group_with_a_real_error_in_it_still_pings(tmp_path, sent):
    group = ExceptionGroup("unhandled errors in a TaskGroup", [httpx.ConnectError("refused"), RuntimeError("bug")])
    lane = _lane(_worker(tmp_path), group)
    for _ in range(rl.READ_FAILURES_TO_REPORT):
        lane.next_attempt_at = 0.0
        asyncio.run(lane.run_turn("ask"))
    [ping] = _pings(sent)
    assert ping["kind"] == alerts.Kind.READER_FAILING


def test_a_rejected_request_carries_the_first_line_of_the_gateways_answer(tmp_path, sent):
    """T1=B (Richard 2026-10-07): the error's first line goes to Slack, scrubbed.
    A model-route 4xx prints its body on that line, so what the gateway said is in it."""
    body = {"error": {"code": "invalid_request", "message": "messages.3.content: too long"}}
    w = _worker(tmp_path, model=_raising(ModelHTTPError(400, "default", body=body)))
    w.read_new()
    _bite(w)
    [ping] = _pings(sent)
    assert ping["error_text"].startswith("ModelHTTPError: status_code: 400, model_name: default, body: ")
    assert "messages.3.content: too long" in ping["error_text"]


def test_a_code_that_is_not_a_plain_code_is_not_sent(tmp_path, sent):
    body = {"error": {"code": "Prompt mentions /home/alice/secret", "message": "m"}}
    w = _worker(tmp_path, model=_raising(ModelHTTPError(400, "default", body=body)))
    w.read_new()
    _bite(w)
    [ping] = _pings(sent)
    assert "code" not in ping


def test_diagnostics_off_sends_the_ping_without_the_error_text(sent, monkeypatch):
    monkeypatch.setenv("PROBE_DIAGNOSTICS", "off")
    assert alerts.report(alerts.Kind.BITE_FAILED, session_id=SID, lane="write", exc=RuntimeError("x")) is True
    [ping] = _pings(sent)
    assert ping["error_type"] == "RuntimeError" and "error_text" not in ping


def test_a_restarted_worker_does_not_ping_the_same_error_again_until_the_window_ends(sent, monkeypatch):
    """A crashed worker comes back as a fresh process: the window is a file, not memory."""
    assert alerts.report(alerts.Kind.CRASHED, session_id=SID, lane="write", exc=ValueError("a")) is True
    assert alerts.report(alerts.Kind.CRASHED, session_id=SID, lane="write", exc=ValueError("b")) is False
    [stamp] = list(Path(os.environ["XDG_STATE_HOME"], "probe", "daemon").glob("telemetry-daemon-error-*.stamp"))
    old = time.time() - alerts.REPORT_INTERVAL_S - 1
    os.utime(stamp, (old, old))
    assert alerts.report(alerts.Kind.CRASHED, session_id=SID, lane="write", exc=ValueError("c")) is True
    assert len(_pings(sent)) == 2


def test_the_home_folder_is_replaced_only_as_a_whole_folder(monkeypatch, tmp_path):
    home = tmp_path / "al"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    assert alerts.error_text(f"read {home}/run.py") == "read ~/run.py"
    assert alerts.error_text(f"read {home}ex/run.py") == f"read {home}ex/run.py"


def test_a_token_after_an_escaped_newline_is_redacted():
    """A KeyError prints its key as a repr: the newline before the token becomes `\\n`."""
    token = "ghp_" + "Ab1" * 12
    assert "\\n" + token in str(KeyError(f"x\n{token}"))
    assert token not in alerts.error_text(KeyError(f"x\n{token}"))


# -- the PostHog destination -------------------------------------------------------


def _destination() -> dict:
    if not DESTINATION.exists():
        pytest.skip("the destination body lives in the repository checkout, not the package")
    return json.loads(DESTINATION.read_text())["destination"]


def _sent_properties(monkeypatch, sent) -> set[str]:
    """Every property a `daemon.error` reaches PostHog with, across every kind,
    through the pipe's real envelope (`build_batch`) for a signed-in user."""
    monkeypatch.setenv("PROBE_DIAGNOSTICS", "on")
    for kind in alerts.Kind:
        alerts.report(kind, session_id=SID, lane="write", exc=ModelHTTPError(400, "default", body={"error": {
            "code": "c"}}), count=3)
    ident = {"distinct_id": "u1", "customer_id": "probe", "workspace_id": "w1", "authenticated": True,
             "email": "a@b.c"}
    keys: set[str] = set()
    for entry in core.build_batch(sent, ident, client_kind="cli", lib="probe-cli", client_version="9.9.9"):
        assert entry["event"] == tm.EVENT_DAEMON_ERROR
        keys |= set(entry["properties"])
    return keys


def test_the_destination_reads_only_properties_the_event_carries(monkeypatch, sent):
    """A template reading a property the event never has posts a blank, silently
    (the first live smoke rendered `CLI ?` from a `cli_version` the CLI never sends)."""
    dest = _destination()
    text = json.dumps(dest["inputs"]) + dest["masking"]["hash"]
    # A property read after `??` is a fallback (`client_version ?? cli_version`);
    # every other one must be on the event.
    first_choice = set(re.findall(r"(?<!\?\? )event\.properties\.([A-Za-z_$][\w$]*)", text))
    assert first_choice, "the template reads no properties: the pattern is wrong"
    assert first_choice - _sent_properties(monkeypatch, sent) == set()


def test_the_destination_listens_to_the_event_and_labels_every_kind():
    dest = _destination()
    assert [e["id"] for e in dest["filters"]["events"]] == [tm.EVENT_DAEMON_ERROR]
    template = dest["inputs"]["blocks"]["value"][0]["text"]["text"]
    missing = [kind.value for kind in alerts.Kind if f"event.properties.kind == '{kind.value}'" not in template]
    assert missing == [], f"these kinds render as 'Unknown daemon error': {missing}"
    assert template.count("\n") == 2, "three lines, nothing else"
    assert "'unfurl_links': false" in dest["hog"]

