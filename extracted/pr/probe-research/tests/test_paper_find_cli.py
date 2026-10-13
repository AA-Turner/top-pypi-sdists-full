"""`probe paper find`: the hosted `find_papers` tool's answer, from the shell.

Every request goes through the REAL `Client` and `Transport` over an
`httpx.MockTransport`, and the hosted tool is the real FastMCP server built on
the same client, so "the same bytes" is checked against the shipped wrapper,
not against a copy of it.
"""

from __future__ import annotations

import asyncio
import contextlib
import hashlib
import importlib
import json
import os
import time

import httpx
import pytest
from typer.testing import CliRunner

from probe.mcp.server import create_server
from probe.mcp.service import ResearchReadService
from probe.mcp.source import ResearchOSSource
from probe.models import PaperExpansion, PaperMode
from probe.sdk import session_marker
from tests.conftest import make_client

cli_main = importlib.import_module("probe.cli.main")

PAPERS = "/v1/web/papers"
SID = "0199a1b2-c3d4-7e5f-8a9b-0c1d2e3f4a5b"


def _paper(n: int, abstract: str = "A short abstract.") -> dict:
    return {
        "paper_id": f"p{n}",
        "title": f"Paper {n}",
        "primary_id": f"arxiv:2610.{n:05d}",
        "abstract": abstract,
        "authors": ["A. Author"],
        "year": 2026,
        "url": f"https://arxiv.org/abs/2610.{n:05d}",
        "score": 0.9,
    }


#: `GET /v1/me`: the envelope's scope, which the hosted tool reads too.
ME = {"customer_id": "lab-42", "email": "researcher@lab.test"}


class _Server:
    """One scripted answer for POST /v1/web/papers (and `/v1/me`); every
    papers request kept."""

    def __init__(self, answer: httpx.Response) -> None:
        self.answer = answer
        self.requests: list[httpx.Request] = []
        self.me_calls = 0

    def handler(self, request: httpx.Request) -> httpx.Response:
        if (request.method, request.url.path) == ("GET", "/v1/me"):
            self.me_calls += 1
            return httpx.Response(200, json=ME)
        self.requests.append(request)
        if (request.method, request.url.path) != ("POST", PAPERS):
            return httpx.Response(404, json={"detail": f"unscripted {request.url.path}"})
        return self.answer

    def bodies(self) -> list[dict]:
        return [json.loads(r.content) for r in self.requests]


@pytest.fixture
def state(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    return tmp_path / "state"


def _install(monkeypatch, tmp_path, answer: httpx.Response):
    server = _Server(answer)
    client = make_client(server, tmp_spool=tmp_path / "spool")
    monkeypatch.setattr(cli_main, "_client", lambda: contextlib.nullcontext(client))
    return server, client


def _hosted(client, arguments: dict) -> str:
    """What the hosted tool sends for these arguments: its one text block."""
    mcp = create_server(ResearchReadService(ResearchOSSource(client)))
    result = asyncio.run(mcp.call_tool("find_papers", arguments))
    blocks = result[0] if isinstance(result, tuple) else result
    return blocks[0].text


def test_the_enums_are_the_servers_closed_vocabularies():
    assert {m.value for m in PaperMode} == {"search", "read", "similar"}
    assert {e.value for e in PaperExpansion} == {"similar", "citers", "references"}


def test_a_search_sends_only_what_was_asked_and_prints_the_hosted_bytes(monkeypatch, tmp_path, state):
    answer = httpx.Response(200, json={"mode": "search", "state": "ok", "results": [_paper(1), _paper(2)]})
    server, client = _install(monkeypatch, tmp_path, answer)

    result = CliRunner().invoke(cli_main.app, ["paper", "find", "why GRPO collapses at zero variance", "--limit", "2"])

    assert result.exit_code == 0, result.output
    assert server.bodies() == [{"mode": "search", "query": "why GRPO collapses at zero variance", "limit": 2}]
    hosted = _hosted(client, {"mode": "search", "query": "why GRPO collapses at zero variance", "limit": 2})
    assert result.stdout.strip() == hosted
    printed = json.loads(result.stdout)
    assert printed["data"]["provenance"] == "open-web"
    assert [p["paper_id"] for p in printed["data"]["results"]] == ["p1", "p2"]


def test_read_and_similar_send_their_mode_arguments(monkeypatch, tmp_path, state):
    answer = httpx.Response(
        200,
        json={
            "mode": "read",
            "state": "ok",
            "results": [_paper(1)],
            "passages": [{"text": "the claim in context", "section": "4.2"}],
        },
    )
    server, _client = _install(monkeypatch, tmp_path, answer)

    read = CliRunner().invoke(
        cli_main.app,
        ["paper", "find", "does it collapse", "--mode", "read", "--paper-id", "arxiv:2610.02140"],
    )
    similar = CliRunner().invoke(
        cli_main.app,
        ["paper", "find", "reports a failure mode", "--mode", "similar", "--paper-id", "p1", "--expand", "citers"],
    )

    assert read.exit_code == 0, read.output
    assert similar.exit_code == 0, similar.output
    assert server.bodies() == [
        {"mode": "read", "query": "does it collapse", "paper_id": "arxiv:2610.02140"},
        {"mode": "similar", "query": "reports a failure mode", "paper_id": "p1", "expand": "citers"},
    ]
    assert json.loads(read.stdout)["data"]["passages"][0]["section"] == "4.2"


def test_search_filters_reach_the_server_under_its_names(monkeypatch, tmp_path, state):
    answer = httpx.Response(200, json={"mode": "search", "state": "ok", "results": [_paper(1)]})
    server, _client = _install(monkeypatch, tmp_path, answer)

    result = CliRunner().invoke(
        cli_main.app,
        ["paper", "find", "q", "--authors", "Karan", "--categories", "cs.LG", "--from", "2026-01-01", "--to", "2026-10-01"],
    )

    assert result.exit_code == 0, result.output
    assert server.bodies() == [
        {
            "mode": "search",
            "query": "q",
            "authors": "Karan",
            "categories": "cs.LG",
            "published_from": "2026-01-01",
            "published_to": "2026-10-01",
        }
    ]


def test_a_cut_answer_resumes_with_its_cursor_and_loses_nothing(monkeypatch, tmp_path, state):
    papers = [_paper(n, abstract="evidence " * 120) for n in range(1, 13)]
    answer = httpx.Response(200, json={"mode": "search", "state": "ok", "results": papers})
    _server, client = _install(monkeypatch, tmp_path, answer)
    args = ["paper", "find", "a sentence", "--token-budget", "512"]

    # Over budget, delivery splits the serialized answer into fragments; each
    # carries the cursor to the next, and the joined text is the whole answer.
    fragments: list[str] = []
    cursor = None
    for _ in range(64):
        result = CliRunner().invoke(cli_main.app, args + (["--cursor", cursor] if cursor else []))
        assert result.exit_code == 0, result.output
        page = json.loads(result.stdout)
        assert page["data"]["format"] == "json_fragment"
        fragments.append(page["data"]["text"])
        cursor = page.get("next_cursor")
        if not cursor:
            assert page["data"]["complete"] is True
            break
    assert len(fragments) > 1, "512 tokens must cut this answer"
    whole = json.loads("".join(fragments))
    assert [p["paper_id"] for p in whole["data"]["results"]] == [p["paper_id"] for p in papers]
    # The hosted tool cuts the same complete answer: every fragment names its
    # sha256. (Fragment edges may differ by a few characters, because each
    # surface's cursor is bound to its own scope and the cursor counts against
    # the budget; a CLI cursor never resumes there.)
    hosted = json.loads(_hosted(client, {"mode": "search", "query": "a sentence", "token_budget": 512}))
    digest = hashlib.sha256("".join(fragments).encode("utf-8")).hexdigest()
    assert digest == page["data"]["sha256"] == hosted["data"]["sha256"]


def test_an_outage_prints_the_hosted_partial_envelope(monkeypatch, tmp_path, state):
    _server, client = _install(monkeypatch, tmp_path, httpx.Response(503, json={"detail": "provider over quota, try later"}))

    result = CliRunner().invoke(cli_main.app, ["paper", "find", "a sentence"])

    assert result.exit_code == 0, result.output
    printed = json.loads(result.stdout)
    assert "results" not in printed["data"], "an outage must not read as 'nothing found'"
    assert printed["completeness"]["state"] == "partial"
    assert "over quota" in printed["data"]["reason"], "the backend's sentence tells an outage from no key"
    assert result.stdout.strip() == _hosted(client, {"mode": "search", "query": "a sentence"})


def test_a_refused_call_is_one_error_line(monkeypatch, tmp_path, state, capsys):
    _install(monkeypatch, tmp_path, httpx.Response(401, json={"detail": "invalid token"}))

    code = cli_main.main(["paper", "find", "a sentence"])

    assert code != 0
    err = capsys.readouterr().err.strip()
    assert err and "Traceback" not in err


def test_a_foreign_cursor_is_an_error_line_not_a_traceback(monkeypatch, tmp_path, state):
    _install(monkeypatch, tmp_path, httpx.Response(200, json={"mode": "search", "state": "ok", "results": []}))

    result = CliRunner().invoke(cli_main.app, ["paper", "find", "q", "--cursor", "prb2_not-a-real-cursor"])

    assert result.exit_code == 1
    assert result.output.startswith("error: ")


def test_inside_an_agent_session_it_stamps_before_the_network(monkeypatch, tmp_path, state):
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    seen_stamp: list[bool] = []

    class _Watching(_Server):
        def handler(self, request):
            seen_stamp.append(session_marker.paper_find_stamp_path(SID).exists())
            return httpx.Response(401, json={"detail": "invalid token"})

        # (no /v1/me answer either: the first request of any kind must see the stamp)

    server = _Watching(httpx.Response(200))
    client = make_client(server, tmp_spool=tmp_path / "spool")
    monkeypatch.setattr(cli_main, "_client", lambda: contextlib.nullcontext(client))

    cli_main.main(["paper", "find", "a sentence"])

    assert seen_stamp and all(seen_stamp), "the stamp lands before the first request"
    assert session_marker.paper_find_stamp_path(SID).parent == state / "probe" / "sessions"


def test_outside_an_agent_session_it_stamps_nothing(monkeypatch, tmp_path, state):
    _install(monkeypatch, tmp_path, httpx.Response(200, json={"mode": "search", "state": "ok", "results": []}))

    result = CliRunner().invoke(cli_main.app, ["paper", "find", "q"])

    assert result.exit_code == 0, result.output
    sessions = state / "probe" / "sessions"
    assert not sessions.exists() or not list(sessions.glob("*.papers"))


def test_the_shell_never_asks_who_it_is(monkeypatch, tmp_path, state):
    """The compact envelope drops `scope`, so GET /v1/me would only add a request
    and a way to fail; the bytes still match the hosted tool's."""
    answer = httpx.Response(200, json={"mode": "search", "state": "ok", "results": [_paper(1)]})
    server, client = _install(monkeypatch, tmp_path, answer)

    result = CliRunner().invoke(cli_main.app, ["paper", "find", "q"])

    assert result.exit_code == 0, result.output
    assert server.me_calls == 0
    assert result.stdout.strip() == _hosted(client, {"mode": "search", "query": "q"})


def test_the_managed_blocks_read_form_runs_as_written(monkeypatch, tmp_path, state):
    """The daemon block (agent_rules.DAEMON_POINTER_BODY) and plan-research-review
    tell agents to pass `--query`; that exact form must parse."""
    from probe.cli import agent_rules

    assert '--mode read --paper-id arxiv:<id> --query "<question>"' in agent_rules.DAEMON_POINTER_BODY
    answer = httpx.Response(200, json={"mode": "read", "state": "ok", "results": [_paper(1)]})
    server, _client = _install(monkeypatch, tmp_path, answer)

    result = CliRunner().invoke(
        cli_main.app, ["paper", "find", "--mode", "read", "--paper-id", "arxiv:2610.02140", "--query", "the accept rule"]
    )

    assert result.exit_code == 0, result.output
    assert server.bodies() == [{"mode": "read", "query": "the accept rule", "paper_id": "arxiv:2610.02140"}]


def test_two_different_queries_are_refused_before_the_network(monkeypatch, tmp_path, state):
    server, _client = _install(monkeypatch, tmp_path, httpx.Response(200, json={"mode": "search", "results": []}))

    same = CliRunner().invoke(cli_main.app, ["paper", "find", "q", "--query", "q"])
    different = CliRunner().invoke(cli_main.app, ["paper", "find", "q", "--query", "other"])

    assert same.exit_code == 0, same.output
    assert different.exit_code == 2 and "give the query once" in different.output
    assert len(server.requests) == 1


def test_a_cursor_that_is_not_ours_spends_nothing(monkeypatch, tmp_path, state):
    """A string without the continuation prefix would read as 'start over' and
    run the paid search again."""
    server, _client = _install(monkeypatch, tmp_path, httpx.Response(200, json={"mode": "search", "results": []}))

    result = CliRunner().invoke(cli_main.app, ["paper", "find", "q", "--cursor", "page-2"])

    assert result.exit_code == 1
    assert "not a `probe paper find` cursor" in result.output
    assert server.requests == []


def _walk(args: list[str]) -> list[dict]:
    pages, cursor = [], None
    for _ in range(64):
        result = CliRunner().invoke(cli_main.app, args + (["--cursor", cursor] if cursor else []))
        assert result.exit_code == 0, result.output
        pages.append(json.loads(result.stdout))
        cursor = pages[-1].get("next_cursor")
        if not cursor:
            return pages
    raise AssertionError("no last page")


def test_cursor_pages_read_the_first_answer_instead_of_searching_again(monkeypatch, tmp_path, state):
    papers = [_paper(n, abstract="evidence " * 120) for n in range(1, 13)]
    server, _client = _install(monkeypatch, tmp_path, httpx.Response(200, json={"mode": "search", "state": "ok", "results": papers}))

    pages = _walk(["paper", "find", "a sentence", "--token-budget", "512"])

    assert len(pages) > 1
    assert len(server.requests) == 1, "one search, however many pages"


def test_a_page_past_the_window_searches_again(monkeypatch, tmp_path, state):
    papers = [_paper(n, abstract="evidence " * 120) for n in range(1, 13)]
    server, _client = _install(monkeypatch, tmp_path, httpx.Response(200, json={"mode": "search", "state": "ok", "results": papers}))
    args = ["paper", "find", "a sentence", "--token-budget", "512"]
    first = json.loads(CliRunner().invoke(cli_main.app, args).stdout)
    for kept in (state / "probe" / "paper-find").glob("*.json"):
        old = time.time() - cli_main.PAPER_FIND_SNAPSHOT_TTL_S - 5
        os.utime(kept, (old, old))

    result = CliRunner().invoke(cli_main.app, args + ["--cursor", first["next_cursor"]])

    assert result.exit_code == 0, result.output
    assert len(server.requests) == 2


def test_a_spent_weekly_allowance_is_one_refusal_with_the_servers_words(monkeypatch, tmp_path, state, capsys):
    detail = {"message": "Your team used its 50 web calls this week.", "kind": "web_calls", "current": 50, "maximum": 50,
              "hint": "Team reads still work."}
    _install(monkeypatch, tmp_path, httpx.Response(402, json={"detail": detail}))

    code = cli_main.main(["paper", "find", "a sentence"])

    assert code != 0
    err = capsys.readouterr().err
    assert "50 web calls" in err and "Traceback" not in err


def test_the_bounds_are_the_hosted_tools(monkeypatch):
    """`--token-budget` and `--limit` take what the hosted tool takes."""
    from typer.main import get_command

    from probe.mcp import budget
    from probe.mcp.server import _WEB_MAX_LIMIT

    find = get_command(cli_main.app).commands["paper"].commands["find"]
    params = {p.name: p for p in find.params}
    budget_range = params["token_budget"].type
    assert (budget_range.min, budget_range.max, params["token_budget"].default) == (budget.MIN_TOKENS, budget.MAX_TOKENS, 2000)
    assert params["limit"].type.max == _WEB_MAX_LIMIT


def test_off_refuses_it_at_the_cli_gate_too(monkeypatch, tmp_path, state):
    """The guard refuses it under `off`; the CLI's own gate does too, for a shell
    no guard sees (pi's guard reads no state)."""
    from probe.cli import write_gate

    assert session_marker.set_session_state(SID, session_marker.STATE_OFF)
    env = {"CLAUDECODE": "1", "CLAUDE_CODE_SESSION_ID": SID}
    assert write_gate.refusal(["paper", "find", "q"], directed=False, env=env)


def _snapshots(state) -> list:
    return sorted((state / "probe" / "paper-find").glob("*")) if (state / "probe" / "paper-find").exists() else []


def test_an_answer_with_no_pages_to_come_is_not_kept(monkeypatch, tmp_path, state):
    _install(monkeypatch, tmp_path, httpx.Response(200, json={"mode": "search", "state": "ok", "results": [_paper(1)]}))

    result = CliRunner().invoke(cli_main.app, ["paper", "find", "q"])

    assert result.exit_code == 0, result.output
    assert "next_cursor" not in json.loads(result.stdout)
    assert _snapshots(state) == []


def test_an_outage_is_never_kept(monkeypatch, tmp_path, state):
    _install(monkeypatch, tmp_path, httpx.Response(503, json={"detail": "provider over quota, try later"}))

    CliRunner().invoke(cli_main.app, ["paper", "find", "q", "--token-budget", "512"])

    assert _snapshots(state) == []


def test_a_kept_answer_is_private_and_dated_now(monkeypatch, tmp_path, state):
    papers = [_paper(n, abstract="evidence " * 120) for n in range(1, 13)]
    _install(monkeypatch, tmp_path, httpx.Response(200, json={"mode": "search", "state": "ok", "results": papers}))

    CliRunner().invoke(cli_main.app, ["paper", "find", "a sentence", "--token-budget", "512"])

    [kept] = _snapshots(state)
    assert kept.suffix == ".json"
    assert kept.stat().st_mode & 0o077 == 0, "readable by this user only"
    assert (kept.parent.stat().st_mode & 0o077) == 0


def test_a_snapshot_dated_in_the_future_is_not_served(monkeypatch, tmp_path, state):
    papers = [_paper(n, abstract="evidence " * 120) for n in range(1, 13)]
    server, _client = _install(monkeypatch, tmp_path, httpx.Response(200, json={"mode": "search", "state": "ok", "results": papers}))
    args = ["paper", "find", "a sentence", "--token-budget", "512"]
    first = json.loads(CliRunner().invoke(cli_main.app, args).stdout)
    for kept in _snapshots(state):
        ahead = time.time() + 3600
        os.utime(kept, (ahead, ahead))

    CliRunner().invoke(cli_main.app, args + ["--cursor", first["next_cursor"]])

    assert len(server.requests) == 2, "a clock-skewed file is searched past, not trusted"
