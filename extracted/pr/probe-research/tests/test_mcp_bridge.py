"""`probe mcp tools` / `probe mcp call`: the hosted Probe MCP from the shell, for
`/probe inline` only.

    "just build the native cli bridge for inline mode - i just dont want to be
    maintaining two seperate read methods so as long as it proxies the existing
    mcp and is not there when the agent isnt in inline mode we're fine"
    (Richard, 2026-10-06)

So: a pure proxy (the server's own tool text and results, nothing re-shaped),
hidden from help, and refused in every session that is not inline. The bridge
runs against REAL servers over real streamable HTTP on localhost: the hosted
`probe.mcp.server` (its own tools and instructions, the fake backend behind its
read service) and a two-tool FastMCP for the call shapes.
"""

from __future__ import annotations

import asyncio
import importlib
import importlib.util
import io
import json
import socket
import sys
import threading
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

import pytest
import typer

from probe import cli
from probe.cli import mcp_bridge, write_gate
from probe.sdk import session_marker

cli_main = importlib.import_module("probe.cli.main")  # `probe.cli.main` the attribute is the entry function
DAEMON_PLUGIN = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-daemon"
SID = "11111111-2222-3333-4444-555555555555"
TOKEN = "probe_pat_bridge_test"


@pytest.fixture(autouse=True)
def _env(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    for name in ("PROBE_CONFIG_PATH", "PROBE_SESSION_STATE", "PROBE_SESSION_TRACKING", "PROBE_PLUGIN_PROFILE",
                 "PROBE_MCP_URL", "PROBE_BASE_URL", "CODEX_THREAD_ID", "PI_SESSION_ID"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    monkeypatch.setenv("PROBE_MCP_TOKEN", TOKEN)


@pytest.fixture
def daemon_session():
    """A session the lean plugin started, at `on (daemon)`."""
    session_marker.mark_session_profile(SID, session_marker.RECORDER_DAEMON)
    session_marker.set_session_state(SID, session_marker.STATE_DAEMON)


@pytest.fixture
def inline(daemon_session):
    """The researcher typed `/probe inline`."""
    assert session_marker.switch_to_inline(SID)
    assert session_marker.is_inline(SID)


# ---------------------------------------------------------------------------
# Real servers on localhost.
# ---------------------------------------------------------------------------


class _Recorder:
    """ASGI middleware that keeps every HTTP request's headers, then serves."""

    def __init__(self, app) -> None:
        self.app = app
        self.headers: list[dict[str, str]] = []

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] == "http":
            self.headers.append({k.decode().lower(): v.decode() for k, v in scope["headers"]})
        await self.app(scope, receive, send)


@contextmanager
def _serve(app):
    """`app` on 127.0.0.1 under uvicorn, in a thread; yields its MCP URL."""
    uvicorn = pytest.importorskip("uvicorn")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, log_level="warning", lifespan="on", timeout_graceful_shutdown=1))
    thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
    thread.start()
    deadline = time.monotonic() + 15
    while not server.started:
        assert thread.is_alive() and time.monotonic() < deadline, "the test MCP server did not start"
        time.sleep(0.01)
    try:
        yield f"http://127.0.0.1:{port}/mcp"
    finally:
        server.should_exit = True
        thread.join(15)
        sock.close()


def _open_security():
    from mcp.server.transport_security import TransportSecuritySettings

    return TransportSecuritySettings(enable_dns_rebinding_protection=False, allowed_hosts=["*"], allowed_origins=["*"])


@pytest.fixture
def hosted(client, monkeypatch):
    """The hosted Probe MCP itself (`create_server`: its tools, instructions and
    argument checks), reading the fake backend."""
    from probe.mcp.server import create_server
    from probe.mcp.service import ResearchReadService
    from probe.mcp.source import ResearchOSSource

    mcp = create_server(ResearchReadService(ResearchOSSource(client)), transport_security=_open_security())
    mcp.settings.streamable_http_path = "/mcp"
    recorder = _Recorder(mcp.streamable_http_app())
    with _serve(recorder) as url:
        monkeypatch.setenv("PROBE_MCP_URL", url)
        yield mcp, recorder


@pytest.fixture
def tiny(monkeypatch):
    """Two tools: one answers, one fails."""
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("tiny", json_response=True, stateless_http=True, transport_security=_open_security())

    @mcp.tool()
    def echo(text: str, times: int = 1) -> str:
        """Say it again."""
        return " ".join([text] * times)

    @mcp.tool()
    def boom(reason: str) -> str:
        """Always fails."""
        raise ValueError(reason)

    @mcp.tool()
    async def slow(seconds: float) -> str:
        """Answers late."""
        import anyio

        await anyio.sleep(seconds)
        return "late"

    recorder = _Recorder(mcp.streamable_http_app())
    with _serve(recorder) as url:
        monkeypatch.setenv("PROBE_MCP_URL", url)
        yield recorder


def _run(argv: list[str], capsys) -> tuple[int, str, str]:
    code = cli.main(argv)
    out = capsys.readouterr()
    return (code or 0), out.out, out.err


# ---------------------------------------------------------------------------
# Not there outside inline.
# ---------------------------------------------------------------------------

BRIDGE = [["mcp", "tools"], ["mcp", "call", "browse", "{}"]]


def _matched(argv: list[str]) -> str:
    return "probe " + " ".join(argv[:2])


@pytest.mark.parametrize("argv", BRIDGE)
@pytest.mark.parametrize("state", [session_marker.STATE_DAEMON, session_marker.STATE_READ_ONLY])
def test_where_the_daemon_reads_it_points_to_probe_ask(daemon_session, capsys, argv, state):
    session_marker.set_session_state(SID, state)
    code, out, err = _run(argv, capsys)
    assert code == mcp_bridge.EXIT_NOT_INLINE == 2
    assert err.strip() == session_marker.DAEMON_PROFILE_DENY.format(matched=_matched(argv))
    assert 'probe ask "<question>"' in err and not out


@pytest.mark.parametrize("argv", BRIDGE)
def test_under_off_it_is_the_off_refusal(daemon_session, capsys, argv):
    """The write gate leaves `mcp` alone (machine plumbing: exit 3 would be its
    refusal); the bridge's own gate refuses, as `off` refuses every read."""
    session_marker.set_session_state(SID, session_marker.STATE_OFF)
    assert write_gate.refusal(argv, directed=False) is None
    code, _out, err = _run(argv, capsys)
    assert code == 2
    assert err.strip() == session_marker.DENY_REASON_OFF.format(matched=_matched(argv))


@pytest.mark.parametrize("argv", BRIDGE)
def test_the_agent_profile_has_the_mcp_tools_instead(capsys, argv):
    session_marker.set_session_state(SID, session_marker.STATE_FULL)
    code, _out, err = _run(argv, capsys)
    assert code == 2
    assert err.strip() == mcp_bridge.NOT_INLINE_DENY.format(matched=_matched(argv))
    assert "`/probe inline`" in err and "the Probe MCP tools are the read surface" in err


@pytest.mark.parametrize("argv", BRIDGE)
def test_no_agent_session_is_refused_too(capsys, monkeypatch, argv):
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID")
    code, _out, err = _run(argv, capsys)
    assert code == 2
    assert err.strip() == mcp_bridge.NOT_INLINE_DENY.format(matched=_matched(argv))


def test_a_full_state_without_the_marker_and_a_finished_stretch_are_not_inline(daemon_session, capsys):
    """`full` alone (an older CLI's `track`) opens nothing, and nor does an
    inline stretch the researcher already ended."""
    session_marker.set_session_state(SID, session_marker.STATE_FULL)
    assert _run(["mcp", "tools"], capsys)[0] == 2
    assert session_marker.switch_to_inline(SID)
    assert session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    code, _out, err = _run(["mcp", "tools"], capsys)
    assert code == 2 and "probe ask" in err


def test_a_refusal_never_reaches_the_server(daemon_session, tiny, capsys):
    assert _run(["mcp", "call", "echo", '{"text": "hi"}'], capsys)[0] == 2
    assert _run(["mcp", "tools"], capsys)[0] == 2
    assert tiny.headers == []


def test_both_are_hidden_from_help(capsys):
    group = typer.main.get_command(cli_main.app).commands["mcp"]
    assert group.commands["tools"].hidden and group.commands["call"].hidden
    code, out, _err = _run(["mcp", "--help"], capsys)
    assert code == 0 and "headers" in out
    assert "Probe MCP tool" not in out and "read guide" not in out
    _code, top, _err = _run(["--help"], capsys)
    assert "Probe MCP tool" not in top


@pytest.mark.parametrize("typo", ["tool", "cal", "calls"])
def test_a_typo_never_suggests_the_hidden_commands(capsys, typo):
    """Typer's "Did you mean" listed hidden commands too, so `probe mcp tool`
    outside inline answered "Did you mean 'tools'?"."""
    code, out, err = _run(["mcp", typo], capsys)
    assert code != 0 and "No such command" in out + err
    assert "'tools'" not in out + err and "'call'" not in out + err


def test_a_typo_still_suggests_a_listed_command(capsys):
    code, out, err = _run(["mcp", "statu"], capsys)
    assert code != 0 and "Did you mean 'status'?" in out + err


# ---------------------------------------------------------------------------
# The guard (the daemon plugin's PreToolUse) agrees: allowed inline, refused otherwise.
# ---------------------------------------------------------------------------


def _load_guard(monkeypatch):
    monkeypatch.setenv("PROBE_PLUGIN_PROFILE", "daemon")
    monkeypatch.setenv("PROBE_AGENT", "claude_code")
    path = DAEMON_PLUGIN / "hooks" / "tracking_guard.py"
    spec = importlib.util.spec_from_file_location("_guard_bridge", path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(path.parent))
    return module


def _guard_says(guard, monkeypatch, capsys, command: str) -> str:
    payload = {"hook_event_name": "PreToolUse", "session_id": SID, "tool_name": "Bash",
               "tool_input": {"command": command}}
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    guard.main()
    return capsys.readouterr().out


@pytest.mark.parametrize("command", ["probe mcp tools", "probe mcp call browse '{}'",
                                     "probe mcp call search_knowledge --args-file - < q.json"])
def test_the_daemon_profile_guard_refuses_it_until_inline(daemon_session, monkeypatch, capsys, command):
    guard = _load_guard(monkeypatch)
    out = _guard_says(guard, monkeypatch, capsys, command)
    decision = json.loads(out)["hookSpecificOutput"]
    assert decision["permissionDecision"] == "deny"
    assert decision["permissionDecisionReason"] == session_marker.DAEMON_PROFILE_DENY.format(matched="probe mcp")
    assert session_marker.switch_to_inline(SID)
    assert _guard_says(guard, monkeypatch, capsys, command) == ""


# ---------------------------------------------------------------------------
# A pure proxy, against the real hosted server.
# ---------------------------------------------------------------------------


def test_tools_prints_the_hosted_mcps_own_guide_and_tools(inline, hosted, capsys):
    from probe.mcp.server import MCP_INSTRUCTIONS

    mcp, recorder = hosted
    served = asyncio.run(mcp.list_tools())
    code, out, err = _run(["mcp", "tools"], capsys)
    assert code == 0, err
    assert out.count(MCP_INSTRUCTIONS.strip()) == 1, "the read guide, once"
    assert [line[3:] for line in out.splitlines() if line.startswith("## ")] == [t.name for t in served]
    for tool in served:
        assert tool.description.strip() in out, f"{tool.name}: its own text, unforked"
    assert len(out) < 30_000, "fits what a coding agent's shell shows"

    code, one, _err = _run(["mcp", "tools", "search_knowledge"], capsys)
    assert code == 0
    by_name = {t.name: t for t in served}
    assert json.dumps(by_name["search_knowledge"].inputSchema, indent=2) in one
    assert MCP_INSTRUCTIONS.strip() not in one

    code, _out, err = _run(["mcp", "tools", "nope"], capsys)
    assert code == 1 and "serves no tool nope" in err and "browse" in err

    sent = recorder.headers[-1]
    assert sent["authorization"] == f"Bearer {TOKEN}"
    assert sent["x-probe-agent"] == "claude_code" and sent["x-probe-agent-session"] == SID
    assert "x-probe-hide-session-work" not in sent, "the inline agent's own records are its work"


def _seed_runs(app, n: int) -> list[str]:
    """`n` runs, created a microsecond apart, wordy enough to need pages."""
    ids = []
    for i in range(n):
        rid = str(uuid.uuid4())
        app.runs[rid] = {"id": rid, "customer_id": "lab-42", "name": f"r{i:02d}", "slug": f"r{i:02d}-7",
                         "status": "completed", "source": "sdk", "project_id": "33333333-3333-3333-3333-333333333333",
                         "experiment_id": None, "created_at": f"2026-09-30T00:00:00.{i + 1:06d}Z",
                         "updated_at": "2026-09-30T00:00:00Z", "summary": {}, "tags": [], "description": "d" * 150}
        ids.append(rid)
    return ids


def test_call_round_trips_through_the_hosted_mcp(inline, hosted, app, capsys):
    """The MCP's own paging arguments (`token_budget`, `cursor`) pass through
    untouched, and each page prints as the server's text, so the walk ends where
    an MCP client's would."""
    ids = _seed_runs(app, 6)
    seen: list[str] = []
    arguments: dict = {"mode": "runs", "token_budget": 512}
    for _ in range(20):
        code, out, err = _run(["mcp", "call", "browse", json.dumps(arguments)], capsys)
        assert code == 0, err
        page = json.loads(out)
        seen += [row["uuid"] for row in page["data"]["runs"]]
        if not page.get("next_cursor"):
            break
        arguments = {**arguments, "cursor": page["next_cursor"]}
    assert seen == [f"run:{rid}" for rid in reversed(ids)]
    assert arguments.get("cursor"), "more than one page"

    code, out, err = _run(["mcp", "call", "browse", '{"bogus": 1}'], capsys)
    assert code == 1 and not out
    assert "browse got unknown argument(s): bogus" in err, "the server's isError text"


@pytest.mark.parametrize(("env", "label"), [("CLAUDE_CODE_SESSION_ID", "claude_code"), ("CODEX_THREAD_ID", "codex"),
                                            ("PI_SESSION_ID", "pi")])
def test_call_prints_text_verbatim_and_names_the_session(inline, tiny, capsys, monkeypatch, env, label):
    if env != "CLAUDE_CODE_SESSION_ID":
        monkeypatch.delenv("CLAUDE_CODE_SESSION_ID")
        monkeypatch.setenv(env, SID)
        if label == "pi":
            monkeypatch.setenv("PI_CODING_AGENT", "1")
    code, out, err = _run(["mcp", "call", "echo", '{"text": "hi", "times": 2}'], capsys)
    assert (code, out, err) == (0, "hi hi\n", "")
    sent = tiny.headers[-1]
    assert sent["authorization"] == f"Bearer {TOKEN}"
    assert (sent["x-probe-agent"], sent["x-probe-agent-session"]) == (label, SID)


def test_a_tool_error_exits_non_zero_with_the_servers_text(inline, tiny, capsys):
    code, out, err = _run(["mcp", "call", "boom", '{"reason": "no such run"}'], capsys)
    assert code == 1 and not out
    assert "no such run" in err


def test_arguments_come_from_a_file_or_stdin(inline, tiny, capsys, monkeypatch, tmp_path):
    args = tmp_path / "args.json"
    args.write_text('{"text": "from a file"}')
    assert _run(["mcp", "call", "echo", "--args-file", str(args)], capsys)[1] == "from a file\n"
    monkeypatch.setattr(sys, "stdin", io.StringIO('{"text": "from stdin", "times": 1}'))
    assert _run(["mcp", "call", "echo", "--args-file", "-"], capsys)[1] == "from stdin\n"


@pytest.mark.parametrize("argv", [["mcp", "call", "echo", "not json"], ["mcp", "call", "echo", "[1]"],
                                  ["mcp", "call", "echo", "{}", "--args-file", "-"]])
def test_bad_arguments_are_a_usage_error(inline, tiny, capsys, argv):
    code, _out, err = _run(argv, capsys)
    assert code == 2 and err
    assert tiny.headers == [], "nothing was sent"


def test_a_refused_token_and_an_unreachable_server_say_so(inline, capsys, monkeypatch):
    from mcp.server.fastmcp import FastMCP

    async def refuse(scope, receive, send):
        if scope["type"] != "http":
            return await FastMCP("x").streamable_http_app()(scope, receive, send)
        await send({"type": "http.response.start", "status": 401, "headers": [(b"content-type", b"text/plain")]})
        await send({"type": "http.response.body", "body": b"no"})

    with _serve(refuse) as url:
        monkeypatch.setenv("PROBE_MCP_URL", url)
        code, _out, err = _run(["mcp", "call", "echo", "{}"], capsys)
    assert code == 1
    assert err.strip() == "error: the Probe MCP answered HTTP 401 Unauthorized (`probe mcp status` checks the token)"

    monkeypatch.setenv("PROBE_MCP_URL", "http://127.0.0.1:9/mcp")
    code, _out, err = _run(["mcp", "tools"], capsys)
    assert code == 1 and err.startswith("error: could not reach the Probe MCP")


def test_the_whole_command_has_one_deadline(inline, tiny, capsys, monkeypatch):
    """Connect, initialize, the call and the cleanup together stay inside the
    shell's budget: past it, one line and exit 1, promptly, never a hang."""
    assert mcp_bridge.TOTAL_TIMEOUT_S == 100.0 and mcp_bridge.READ_TIMEOUT_S <= mcp_bridge.TOTAL_TIMEOUT_S
    monkeypatch.setattr(mcp_bridge, "TOTAL_TIMEOUT_S", 0.5)
    started = time.monotonic()
    code, out, err = _run(["mcp", "call", "slow", '{"seconds": 3}'], capsys)
    assert (code, out) == (1, "")
    assert err.strip() == "error: the Probe MCP did not answer within 0.5 s"
    assert time.monotonic() - started < 2.5
    assert _run(["mcp", "call", "slow", '{"seconds": 0}'], capsys)[1] == "late\n"


def test_no_token_or_no_known_mcp_is_one_line(inline, capsys, monkeypatch):
    monkeypatch.delenv("PROBE_MCP_TOKEN")
    code, _out, err = _run(["mcp", "tools"], capsys)
    assert code == 1 and err.startswith("error: no MCP token")
    monkeypatch.setenv("PROBE_MCP_TOKEN", TOKEN)
    monkeypatch.setenv("PROBE_BASE_URL", "https://probe.internal.example")
    code, _out, err = _run(["mcp", "tools"], capsys)
    assert code == 1 and "set PROBE_MCP_URL" in err


def test_the_target_follows_the_context_like_the_daemon_reader(monkeypatch):
    """One address resolution (`sdk.config.mcp_url`), shared with the daemon's reader."""
    from probe.sdk import config

    assert mcp_bridge.target().url == config.STOCK_MCP_URL
    monkeypatch.setenv("PROBE_MCP_URL", "https://mcp.staging.example/mcp")
    assert mcp_bridge.target(base_url="https://api.staging.example").url == "https://mcp.staging.example/mcp"


def test_the_daemon_reader_resolves_the_same_address():
    pytest.importorskip("pydantic_ai")
    from probe.daemon import agent
    from probe.sdk import config

    assert agent.mcp_url is config.mcp_url and agent.STOCK_MCP_URL == config.STOCK_MCP_URL


def test_result_text_keeps_the_servers_content():
    from mcp import types

    text = types.CallToolResult(content=[types.TextContent(type="text", text='{"a": 1}\n'),
                                         types.TextContent(type="text", text="second")])
    assert mcp_bridge.result_text(text) == '{"a": 1}\n\nsecond'
    structured = types.CallToolResult(content=[], structuredContent={"rows": [1, 2]})
    assert json.loads(mcp_bridge.result_text(structured)) == {"rows": [1, 2]}
    image = types.CallToolResult(content=[types.ImageContent(type="image", data="aGk=", mimeType="image/png")])
    assert json.loads(mcp_bridge.result_text(image))["mimeType"] == "image/png"
