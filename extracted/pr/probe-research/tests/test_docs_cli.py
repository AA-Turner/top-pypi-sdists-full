"""`probe docs "<question>"`: Probe's own docs (docs.prbe.ai), from the shell.

The daemon profile has no MCP, so this is how its agent reads the docs; an MCP
agent searches them with `search(search_in=["docs"])`. Every request goes
through the REAL `Client` and `Transport` over an `httpx.MockTransport`.
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path

import httpx
import pytest
from typer.testing import CliRunner

from probe.sdk import session_marker

cli_main = importlib.import_module("probe.cli.main")

DOCS = "/public/v1/docs"


def _section(n: int, text: str = "Run `npx probe-research install`.") -> dict:
    return {
        "page": f"Page {n}",
        "heading": f"Heading {n}",
        "path": f"/page-{n}",
        "url": f"https://docs.prbe.ai/page-{n}",
        "text": text,
        "rank": n,
    }


class _Server:
    """One scripted answer for GET /public/v1/docs; every request kept."""

    def __init__(self, answer: httpx.Response) -> None:
        self.answer = answer
        self.requests: list[httpx.Request] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if (request.method, request.url.path) != ("GET", DOCS):
            return httpx.Response(404, json={"detail": f"unscripted {request.url.path}"})
        return self.answer


@pytest.fixture
def signed_out(monkeypatch, tmp_path):
    """No stored login and no PROBE_TOKEN (conftest already isolates both); the
    CLI builds its client the real way and only the wire is scripted."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_BASE_URL", "http://test")
    monkeypatch.delenv("PROBE_TOKEN", raising=False)

    def install(answer: httpx.Response) -> _Server:
        server = _Server(answer)
        real = cli_main._new_client

        def new_client(**kwargs):
            client = real(**kwargs)
            assert client.settings.token is None, "this test must run signed out"
            client.transport._client = httpx.Client(
                base_url=client.settings.base_url, transport=httpx.MockTransport(server.handler)
            )
            return client

        monkeypatch.setattr(cli_main, "_new_client", new_client)
        return server

    return install


def _run(*args: str):
    return CliRunner().invoke(cli_main.app, ["docs", *args])


def test_it_answers_signed_out_with_the_question_and_no_credential(signed_out):
    server = signed_out(httpx.Response(200, json={"state": "ok", "sections": [_section(1), _section(2)]}))

    result = _run("how", "do I set up", "Codex")

    assert result.exit_code == 0, result.output
    assert len(server.requests) == 1
    request = server.requests[0]
    assert request.url.params["query"] == "how do I set up Codex"
    assert "authorization" not in {k.lower() for k in request.headers}
    assert result.stdout == (
        "## Page 1 — Heading 1\nhttps://docs.prbe.ai/page-1\n\nRun `npx probe-research install`.\n\n"
        "## Page 2 — Heading 2\nhttps://docs.prbe.ai/page-2\n\nRun `npx probe-research install`.\n"
    )


def test_whole_sections_stop_before_the_cap_and_say_how_many_more(signed_out):
    long = "x" * 3_000
    sections = [_section(n, long) for n in range(1, 6)]
    signed_out(httpx.Response(200, json={"state": "ok", "sections": sections}))

    result = _run("anything")

    assert result.exit_code == 0, result.output
    shown = result.stdout.count("## Page ")
    assert shown == 2, "two 3,000-char sections fit under 8,000; a third would pass it"
    assert long in result.stdout, "a section prints whole, never cut"
    assert result.stdout.rstrip().endswith("3 more matching sections not shown.")


def test_the_first_section_prints_even_when_it_alone_passes_the_cap(signed_out):
    huge = "y" * (cli_main.DOCS_PRINT_CHARS + 500)
    signed_out(httpx.Response(200, json={"state": "ok", "sections": [_section(1, huge), _section(2)]}))

    result = _run("anything")

    assert result.exit_code == 0, result.output
    assert huge in result.stdout
    assert result.stdout.rstrip().endswith("1 more matching section not shown.")


def test_a_stale_copy_says_so_in_one_line(signed_out):
    signed_out(httpx.Response(200, json={"state": "stale", "sections": [_section(1)]}))

    result = _run("anything")

    assert result.exit_code == 0, result.output
    assert "## Page 1 — Heading 1" in result.stdout
    assert result.stderr.strip() == "docs.prbe.ai could not be read just now; this is the last good copy."


@pytest.mark.parametrize(
    "answer",
    [
        httpx.Response(200, json={"state": "unavailable", "sections": []}),
        # The route is not deployed yet (an older API), or it failed.
        httpx.Response(404, json={"detail": "Not Found"}),
        # FastAPI's own 422: a list detail that echoes the input back.
        httpx.Response(
            422,
            json={
                "detail": [
                    {
                        "type": "string_too_long",
                        "loc": ["query", "query"],
                        "msg": "String should have at most 512 characters",
                        "input": "anything",
                        "ctx": {"max_length": 512},
                    }
                ]
            },
        ),
        httpx.Response(200, text="<html>proxy</html>"),
    ],
)
def test_unavailable_or_an_error_is_one_line_on_stderr_and_exits_1(signed_out, answer):
    signed_out(answer)

    result = _run("anything")

    assert result.exit_code == 1
    assert result.stdout == ""
    lines = result.stderr.strip().splitlines()
    assert len(lines) == 1 and lines[0].startswith("error: Probe's docs"), result.stderr


def test_nothing_matched_is_said_plainly(signed_out):
    signed_out(httpx.Response(200, json={"state": "ok", "sections": []}))

    result = _run("zzz")

    assert result.exit_code == 0, result.output
    assert result.stdout.strip() == "Nothing in Probe's docs matched; try other words."


def test_it_touches_no_session_state(signed_out, tmp_path, monkeypatch):
    """Unlike `paper find`, nothing is stamped: a docs read opens, stamps and
    records nothing for the session."""
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "0199a1b2-c3d4-7e5f-8a9b-0c1d2e3f4a5b")
    signed_out(httpx.Response(200, json={"state": "ok", "sections": [_section(1)]}))
    sessions = session_marker.state_dir() / "sessions"
    before = sorted(p.name for p in sessions.rglob("*")) if sessions.exists() else []

    result = _run("anything")

    assert result.exit_code == 0, result.output
    after = sorted(p.name for p in sessions.rglob("*")) if sessions.exists() else []
    assert after == before
    assert not (session_marker.state_dir() / "paper-find").exists()


def test_a_question_over_the_routes_limit_is_refused_before_any_request(signed_out):
    server = signed_out(httpx.Response(200, json={"state": "ok", "sections": []}))

    result = _run("x" * (cli_main.DOCS_QUERY_MAX_CHARS + 1))

    assert result.exit_code == 2
    assert f"{cli_main.DOCS_QUERY_MAX_CHARS} characters" in result.output
    assert server.requests == []
    assert _run("x" * cli_main.DOCS_QUERY_MAX_CHARS).exit_code == 0


def test_question_words_that_look_like_options_are_words(signed_out):
    """`probe docs what does --no-capture do` asks about the flag: once the
    question has started, nothing after it is an option of `probe docs`."""
    server = signed_out(httpx.Response(200, json={"state": "ok", "sections": [_section(1)]}))

    for args in (("what", "does", "--no-capture", "do"), ("--no-capture", "flag")):
        result = _run(*args)
        assert result.exit_code == 0, result.output
        assert server.requests[-1].url.params["query"] == " ".join(args)

    helped = _run("--help")
    assert helped.exit_code == 0 and "Search Probe's own docs" in helped.output
    assert len(server.requests) == 2


def test_the_docs_limits_match_the_route():
    """The CLI, the MCP and the SDK snapshot of the route agree on its bounds:
    a longer query or a larger limit is a 422 that reads as "docs unavailable"."""
    from probe.mcp import contract, service

    schema = json.loads((Path(__file__).resolve().parents[1] / "schema" / "openapi.json").read_text())
    params = {p["name"]: p["schema"] for p in schema["paths"][DOCS]["get"]["parameters"]}
    assert params["query"]["maxLength"] == contract.DOCS_QUERY_MAX_CHARS == cli_main.DOCS_QUERY_MAX_CHARS
    assert params["limit"]["maximum"] == service._DOCS_SECTION_CAP


def test_an_empty_question_is_refused_before_any_request(signed_out):
    server = signed_out(httpx.Response(200, json={"state": "ok", "sections": []}))

    result = _run("   ")

    assert result.exit_code == 2
    assert server.requests == []


def test_a_workspace_limit_does_not_stop_a_signed_out_docs_read(signed_out, monkeypatch):
    """A limit names one of the TEAM's workspaces, looked up with a credential;
    the docs are no workspace's, so a limited process with no token still reads
    them, and never asks `/v1/workspaces`."""
    from probe.sdk import workspace_limit

    monkeypatch.setenv(workspace_limit.LIMIT_ENV, "eng")
    server = signed_out(httpx.Response(200, json={"state": "ok", "sections": [_section(1)]}))

    with cli_main._new_client() as client:
        answer = client.docs("codex")

    assert answer["sections"] == [_section(1)]
    assert [request.url.path for request in server.requests] == [DOCS]
    assert workspace_limit.LIMIT_HEADER not in server.requests[0].headers


def test_a_credential_in_the_question_is_scrubbed_before_it_is_sent(signed_out):
    """The question rides the URL, which access logs keep as sent."""
    server = signed_out(httpx.Response(200, json={"state": "ok", "sections": []}))
    token = "ghp_" + "a1B2" * 9

    with cli_main._new_client() as client:
        client.docs(f"why is {token} rejected")

    [request] = server.requests
    sent = request.url.params["query"]
    assert token not in str(request.url) and sent.startswith("why is <redacted")
    assert sent.endswith(" rejected")


def test_it_is_a_read_of_probes_docs_everywhere_it_is_sorted():
    """A read (so `off` refuses it, as `paper find`), one the daemon profile
    leaves to the agent, and a read in the daemon's owner table."""
    from probe.daemon import precheck

    assert session_marker.classify_probe_args(["docs", "how", "do", "I"]) == ("read", "probe docs")
    assert session_marker.classify_probe_args(["paper", "find", "x"])[0] == "read"
    assert session_marker.daemon_profile_allows(["docs", "how", "do", "I"]) == (True, "probe docs")
    assert precheck.OWNERS["docs"] == precheck.READ
