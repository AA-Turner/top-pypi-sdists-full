"""The citation-graph surfaces: `Client.citation_graph` / `paper_citations` /
`refresh_paper_citations` and `probe paper citations` / `probe paper graph`.

Every request goes through the REAL `Client` and `Transport` over an
`httpx.MockTransport`, so the path, the query string and the error mapping are
the shipped ones. The scripted answers are validated against the generated
`CitationGraphOut` / `PaperCitationsOut` first: a fake whose shape the server
never returns would prove nothing.
"""

from __future__ import annotations

import contextlib
import copy
import importlib
import json

import httpx
import pytest
from typer.main import get_command
from typer.testing import CliRunner

from probe.models import CitationGraphOut, PaperCitationsOut
from probe.sdk import errors
from tests.conftest import make_client

cli_main = importlib.import_module("probe.cli.main")

PROJECT_ID = "7d3f7c1e-2b8a-4a63-9f4e-0d6c2f5f0a11"
PAPER_A = "0b0f5d2e-1c55-4a3e-8f0c-8a7f3b6d9e01"
PAPER_B = "5c1d8e7f-9a2b-4c3d-8e4f-1a2b3c4d5e02"
STAMP = "2026-10-03T12:00:00Z"

PAPER_CITATIONS = {
    "paper_id": PAPER_A,
    "state": "partial",
    "keys": ["arxiv:1706.03762"],
    "sync": {
        "identity": "resolved",
        "references": "ok",
        "citers": "partial",
        "references_total": 40,
        "references_linked": 20,
        "citers_nominated": 50,
        "citers_proven": 41,
        "citers_unchecked": 6,
        "citers_not_reconfirmed": 2,
        "citers_capped": 0,
        "references_fetched_at": STAMP,
        "citers_fetched_at": STAMP,
        "stale": False,
    },
    "reference_lists": [
        {
            "source": "arxiv_html",
            "owner_key": "arxiv:1706.03762",
            "url": "https://arxiv.org/html/1706.03762v7",
            "status": "ok",
            "total": 40,
            "linked": 20,
            "fetched_at": STAMP,
        }
    ],
    "links": [
        {
            "direction": "reference",
            "list_source": "arxiv_html",
            "list_owner_key": "arxiv:1706.03762",
            "list_url": "https://arxiv.org/html/1706.03762v7",
            "ordinal": 1,
            "entry_key": "arxiv:1607.06450",
            "work_key": "arxiv:1607.06450",
            "resolution": "printed_id",
            "raw_reference": "J. L. Ba et al. Layer normalization. arXiv:1607.06450, 2016.",
            "title": "Layer Normalization",
            "year": 2016,
            "detail": {},
            "fetched_at": STAMP,
            "confirmed_at": STAMP,
        },
        {
            "direction": "reference",
            "list_source": "arxiv_html",
            "list_owner_key": "arxiv:1706.03762",
            "list_url": "https://arxiv.org/html/1706.03762v7",
            "ordinal": 14,
            "entry_key": None,
            "work_key": None,
            "resolution": "unresolved",
            "raw_reference": "S. Hochreiter. Untersuchungen zu dynamischen neuronalen Netzen. 1991.",
            "detail": {"reason": "no_id"},
            "fetched_at": STAMP,
            "confirmed_at": STAMP,
        },
        {
            "direction": "citer",
            "list_source": "crossref",
            "list_owner_key": "doi:10.1145/3292500.3330701",
            "list_url": "https://api.crossref.org/works/10.1145%2F3292500.3330701",
            "ordinal": 13,
            "entry_key": "arxiv:1706.03762",
            "work_key": "doi:10.1145/3292500.3330701",
            "resolution": "printed_id",
            "title": "Optuna",
            "year": 2019,
            "detail": {"nominated_by": "openalex"},
            "fetched_at": STAMP,
            "confirmed_at": STAMP,
        },
    ],
    "truncated": False,
}

GRAPH = {
    "project_id": PROJECT_ID,
    "state": "ok",
    "nodes": [
        {
            "id": f"paper:{PAPER_A}",
            "kind": "primary",
            "paper_id": PAPER_A,
            "title": "Attention Is All You Need",
            "year": 2017,
            "keys": ["arxiv:1706.03762"],
            "sync": PAPER_CITATIONS["sync"],
        },
        {
            "id": f"paper:{PAPER_B}",
            "kind": "primary",
            "paper_id": PAPER_B,
            "title": "BERT",
            "year": 2018,
            "keys": ["arxiv:1810.04805"],
            "sync": {**PAPER_CITATIONS["sync"], "citers": "ok"},
        },
        {
            "id": "work:arxiv:1607.06450",
            "kind": "suggested",
            "title": "Layer Normalization",
            "year": 2016,
            "keys": ["arxiv:1607.06450"],
            "url": "https://arxiv.org/abs/1607.06450",
            "cited_by_count": 1234,
            "linked_primaries": 2,
        },
    ],
    "edges": [
        {
            "source": f"paper:{PAPER_A}",
            "target": "work:arxiv:1607.06450",
            "relation": "cites",
            "evidence": [
                {
                    "direction": "reference",
                    "list_source": "arxiv_html",
                    "list_owner_key": "arxiv:1706.03762",
                    "list_url": "https://arxiv.org/html/1706.03762v7",
                    "ordinal": 1,
                    "resolution": "printed_id",
                    "fetched_at": STAMP,
                    "confirmed_at": STAMP,
                }
            ],
        },
        {
            "source": f"paper:{PAPER_B}",
            "target": f"paper:{PAPER_A}",
            "relation": "cites",
            "evidence": [
                {
                    "direction": "reference",
                    "list_source": "arxiv_html",
                    "list_owner_key": "arxiv:1810.04805",
                    "list_url": "https://arxiv.org/html/1810.04805v2",
                    "ordinal": 47,
                    "resolution": "printed_id",
                    "fetched_at": STAMP,
                    "confirmed_at": STAMP,
                },
                {
                    "direction": "citer",
                    "list_source": "crossref",
                    "list_owner_key": "doi:10.18653/v1/n19-1423",
                    "list_url": "https://api.crossref.org/works/10.18653%2Fv1%2Fn19-1423",
                    "ordinal": 51,
                    "resolution": "publisher_id",
                    "fetched_at": STAMP,
                    "confirmed_at": STAMP,
                },
            ],
        },
        {
            "source": f"paper:{PAPER_B}",
            "target": f"paper:{PAPER_A}",
            "relation": "discovered_via",
            "edge_id": "9e8d7c6b-5a49-4382-9170-6f5e4d3c2b10",
            "provenance": "human",
            "reason": "its related-work section",
        },
    ],
    "completeness": {
        "primaries_total": 2,
        "primaries_returned": 2,
        "primaries_without_id": 0,
        "primaries_pending": 0,
        "suggested_candidates": 812,
        "suggested_returned": 1,
        "unresolved_references": 396,
        "unchecked_citers": 37,
        "not_reconfirmed_citers": 2,
        "truncated": False,
    },
}


def test_the_scripted_answers_have_the_servers_shape() -> None:
    PaperCitationsOut.model_validate(PAPER_CITATIONS)
    CitationGraphOut.model_validate(GRAPH)


class _Server:
    """A scripted server: one answer per (method, path), every request kept."""

    def __init__(self, answers: dict[tuple[str, str], httpx.Response]) -> None:
        self.answers = answers
        self.requests: list[httpx.Request] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        answer = self.answers.get((request.method, request.url.path))
        if answer is None:
            return httpx.Response(404, json={"detail": f"unscripted {request.url.path}"})
        return answer


def _client(answers: dict[tuple[str, str], httpx.Response], tmp_path):
    server = _Server(answers)
    return server, make_client(server, tmp_spool=tmp_path / "spool")


def _graph_path() -> str:
    return f"/v1/projects/{PROJECT_ID}/citation-graph"


def _citations_path(paper_id: str = PAPER_A) -> str:
    return f"/v1/papers/{paper_id}/citations"


# --------------------------------------------------------------------------
# SDK
# --------------------------------------------------------------------------


def test_citation_graph_sends_only_what_was_asked(tmp_path) -> None:
    server, client = _client({("GET", _graph_path()): httpx.Response(200, json=GRAPH)}, tmp_path)

    assert client.citation_graph(PROJECT_ID) == GRAPH
    # Nothing asked, nothing sent: every default is the server's.
    assert dict(server.requests[-1].url.params) == {}

    client.citation_graph(
        PROJECT_ID,
        suggested=0,
        directions=["citer"],
        min_links=2,
        include_discovery=True,
        include_unresolved=False,
    )
    assert dict(server.requests[-1].url.params) == {
        "suggested": "0",
        "directions": "citer",
        "min_links": "2",
        "include_discovery": "true",
        "include_unresolved": "false",
    }


def test_citation_graph_directions_take_a_comma_list_and_refuse_a_typo(tmp_path) -> None:
    server, client = _client({("GET", _graph_path()): httpx.Response(200, json=GRAPH)}, tmp_path)

    client.citation_graph(PROJECT_ID, directions="reference, citer")
    assert server.requests[-1].url.params["directions"] == "reference,citer"

    sent = len(server.requests)
    with pytest.raises(ValueError, match="reference, citer"):
        client.citation_graph(PROJECT_ID, directions=["references"])
    assert len(server.requests) == sent, "a typo must fail before the request"


def test_paper_citations_path_and_params(tmp_path) -> None:
    server, client = _client(
        {("GET", _citations_path()): httpx.Response(200, json=PAPER_CITATIONS)}, tmp_path
    )

    assert client.paper_citations(PAPER_A) == PAPER_CITATIONS
    assert dict(server.requests[-1].url.params) == {}

    client.paper_citations(PAPER_A, direction="citer", include_unresolved=False, limit=2000)
    assert dict(server.requests[-1].url.params) == {
        "direction": "citer",
        "include_unresolved": "false",
        "limit": "2000",
    }
    with pytest.raises(ValueError, match="citation direction"):
        client.paper_citations(PAPER_A, direction="cites")


def test_refresh_queues_once(tmp_path) -> None:
    path = f"{_citations_path()}/refresh"
    server, client = _client(
        {("POST", path): httpx.Response(202, json={"status": "queued"})}, tmp_path
    )

    assert client.refresh_paper_citations(PAPER_A) == {"status": "queued"}
    assert [(r.method, r.url.path) for r in server.requests] == [("POST", path)]


def test_refresh_too_soon_is_one_request_carrying_retry_after(tmp_path) -> None:
    path = f"{_citations_path()}/refresh"
    server, client = _client(
        {
            ("POST", path): httpx.Response(
                429,
                json={"detail": "this paper's citations were fetched within the last hour"},
                headers={"Retry-After": "3600"},
            )
        },
        tmp_path,
    )

    with pytest.raises(errors.RosError) as caught:
        client.refresh_paper_citations(PAPER_A)
    assert caught.value.status == 429
    assert caught.value.retry_after == 3600
    # Never retried in-process (an hour is not a blip) and never queued offline.
    assert len(server.requests) == 1


def test_refresh_for_a_team_without_citations_is_a_conflict(tmp_path) -> None:
    path = f"{_citations_path()}/refresh"
    detail = {
        "code": "citations_disabled",
        "message": "Citation links are not switched on for your team.",
    }
    _, client = _client({("POST", path): httpx.Response(409, json={"detail": detail})}, tmp_path)

    with pytest.raises(errors.ConflictError) as caught:
        client.refresh_paper_citations(PAPER_A)
    assert caught.value.detail["code"] == "citations_disabled"
    assert "not switched on" in str(caught.value)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _install(monkeypatch, tmp_path, answers):
    server, client = _client(answers, tmp_path)
    monkeypatch.setattr(cli_main, "_client", lambda: contextlib.nullcontext(client))
    monkeypatch.setattr(cli_main, "_project_id", lambda _client, ref: PROJECT_ID)
    return server


def test_paper_citations_prints_each_link_with_its_proof(monkeypatch, tmp_path) -> None:
    server = _install(
        monkeypatch,
        tmp_path,
        {("GET", _citations_path()): httpx.Response(200, json=PAPER_CITATIONS)},
    )

    result = CliRunner().invoke(cli_main.app, ["paper", "citations", PAPER_A])

    assert result.exit_code == 0, result.output
    out = result.output
    assert f"paper {PAPER_A} · state: partial" in out
    assert "keys: arxiv:1706.03762" in out
    assert "references: ok · 40 entries, 20 linked · fetched 2026-10-03" in out
    assert "citers: partial · 50 nominated, 41 proven, 6 unchecked, 2 not reconfirmed" in out
    assert "https://arxiv.org/html/1706.03762v7" in out
    lines = out.splitlines()
    header = next(line for line in lines if line.startswith("DIRECTION"))
    assert header.split() == ["DIRECTION", "PROOF", "WORK", "ENTRY", "TITLE", "OR", "ENTRY", "TEXT"]
    reference = next(line for line in lines if "arxiv:1607.06450" in line)
    assert reference.split()[:4] == ["reference", "printed_id", "arxiv:1607.06450", "1"]
    assert "Layer Normalization (2016)" in reference
    unresolved = next(line for line in lines if "Hochreiter" in line)
    assert unresolved.split()[:4] == ["reference", "unresolved", "-", "14"]
    assert unresolved.endswith("[no_id]")
    citer = next(line for line in lines if line.startswith("citer "))
    assert "doi:10.1145/3292500.3330701" in citer and "Optuna (2019)" in citer
    # The CLI's default asks for unresolved rows explicitly (the route's default too).
    assert dict(server.requests[-1].url.params) == {"include_unresolved": "true"}


def test_paper_citations_json_is_the_servers_answer(monkeypatch, tmp_path) -> None:
    server = _install(
        monkeypatch,
        tmp_path,
        {("GET", _citations_path()): httpx.Response(200, json=PAPER_CITATIONS)},
    )

    result = CliRunner().invoke(
        cli_main.app,
        [
            "paper", "citations", PAPER_A,
            "--json", "--direction", "reference", "--no-include-unresolved", "--limit", "10",
        ],
    )

    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == PAPER_CITATIONS
    assert dict(server.requests[-1].url.params) == {
        "direction": "reference",
        "include_unresolved": "false",
        "limit": "10",
    }


def test_paper_citations_says_when_the_team_is_not_switched_on(monkeypatch, tmp_path) -> None:
    disabled = {"paper_id": PAPER_A, "state": "disabled"}
    PaperCitationsOut.model_validate(disabled)
    _install(
        monkeypatch, tmp_path, {("GET", _citations_path()): httpx.Response(200, json=disabled)}
    )

    result = CliRunner().invoke(cli_main.app, ["paper", "citations", PAPER_A])

    assert result.exit_code == 0, result.output
    assert "not switched on for your team (state: disabled)" in result.output
    assert "DIRECTION" not in result.output


def test_paper_citations_names_a_truncated_answer(monkeypatch, tmp_path) -> None:
    answer = {**PAPER_CITATIONS, "truncated": True}
    _install(monkeypatch, tmp_path, {("GET", _citations_path()): httpx.Response(200, json=answer)})

    result = CliRunner().invoke(cli_main.app, ["paper", "citations", PAPER_A])

    assert result.exit_code == 0, result.output
    assert "truncated: showing 3 rows; raise --limit (max 2000)" in result.output


def test_a_bibliography_entry_cannot_steer_the_terminal(monkeypatch, tmp_path) -> None:
    """Titles and entry text are third-party data: a bidi override or an escape
    sequence in one must not reach the terminal through the table."""
    answer = copy.deepcopy(PAPER_CITATIONS)
    answer["links"][0]["title"] = "Layer\u202e Norm\x1b[31malization\nsecond line"
    _install(monkeypatch, tmp_path, {("GET", _citations_path()): httpx.Response(200, json=answer)})

    result = CliRunner().invoke(cli_main.app, ["paper", "citations", PAPER_A])

    assert result.exit_code == 0, result.output
    assert "\u202e" not in result.output and "\x1b" not in result.output
    assert "Layer Norm[31malization second line (2016)" in result.output


def test_bidi_marks_and_a_key_cannot_steer_the_terminal_either(monkeypatch, tmp_path) -> None:
    """The three bidi MARKS (LRM, RLM, ALM) reorder a line like an override,
    and the paper's `keys` line is server data too: every one is stripped."""
    answer = copy.deepcopy(PAPER_CITATIONS)
    answer["links"][0]["title"] = "Layer\u200e Norm\u200falization\u061c"
    answer["keys"] = ["arxiv:1706.03762\u202e\x1b[2J"]
    _install(monkeypatch, tmp_path, {("GET", _citations_path()): httpx.Response(200, json=answer)})

    result = CliRunner().invoke(cli_main.app, ["paper", "citations", PAPER_A])

    assert result.exit_code == 0, result.output
    for ch in ("\u200e", "\u200f", "\u061c", "\u202e", "\x1b"):
        assert ch not in result.output, repr(ch)
    assert "keys: arxiv:1706.03762[2J" in result.output
    assert "Layer Normalization (2016)" in result.output
    # Built from the shared class, so `_print_json`'s escapes are a subset.
    assert cli_main._DISPLAY_CONTROLS.pattern[1:-1] in cli_main._CITE_CONTROLS.pattern


def test_paper_graph_prints_papers_works_and_labelled_edges(monkeypatch, tmp_path) -> None:
    server = _install(
        monkeypatch, tmp_path, {("GET", _graph_path()): httpx.Response(200, json=GRAPH)}
    )

    result = CliRunner().invoke(
        cli_main.app, ["paper", "graph", "--project", "review", "--include-discovery"]
    )

    assert result.exit_code == 0, result.output
    out = result.output
    assert f"project {PROJECT_ID} · state: ok" in out
    assert "2 of 2 papers (0 without an id, 0 pending) · 1 of 812 suggested works · 3 edges" in out
    assert "not linked: 396 bibliography entries printed no id · 37 citers unchecked" in out
    lines = out.splitlines()
    p1 = next(line for line in lines if line.strip().startswith("P1 "))
    assert "ok 20/40" in p1 and "partial 41/50" in p1 and PAPER_A in p1
    assert "Attention Is All You Need (2017)" in p1
    w1 = next(line for line in lines if line.strip().startswith("W1 "))
    assert w1.split()[:4] == ["W1", "2", "1234", "arxiv:1607.06450"]
    edges = lines[lines.index("EDGES") + 2 :]
    assert edges[0].split()[:3] == ["P1", "cites", "W1"]
    assert "reference · arxiv_html #1 · printed_id" in edges[0]
    assert edges[1].split()[:3] == ["P2", "cites", "P1"]
    assert edges[1].endswith("(+1 more)")
    assert edges[2].split()[:3] == ["P2", "discovered_via", "P1"]
    assert "human: its related-work section" in edges[2]
    assert dict(server.requests[-1].url.params) == {"include_discovery": "true"}


def test_paper_graph_json_passes_every_route_parameter(monkeypatch, tmp_path) -> None:
    server = _install(
        monkeypatch, tmp_path, {("GET", _graph_path()): httpx.Response(200, json=GRAPH)}
    )

    result = CliRunner().invoke(
        cli_main.app,
        [
            "paper", "graph", "--project", "review", "--json",
            "--suggested", "0", "--direction", "citer", "--min-links", "2",
            "--include-unresolved",
        ],
    )

    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == GRAPH
    assert dict(server.requests[-1].url.params) == {
        "suggested": "0",
        "directions": "citer",
        "min_links": "2",
        "include_unresolved": "true",
    }


def test_paper_graph_lists_unresolved_entries_when_asked(monkeypatch, tmp_path) -> None:
    answer = copy.deepcopy(GRAPH)
    answer["nodes"][0]["unresolved_references"] = [
        {
            "list_owner_key": "arxiv:1706.03762",
            "ordinal": 14,
            "raw_reference": "S. Hochreiter. Untersuchungen. 1991.",
            "reason": "no_id",
        }
    ]
    CitationGraphOut.model_validate(answer)
    _install(monkeypatch, tmp_path, {("GET", _graph_path()): httpx.Response(200, json=answer)})

    result = CliRunner().invoke(
        cli_main.app, ["paper", "graph", "--project", "review", "--include-unresolved"]
    )

    assert result.exit_code == 0, result.output
    assert "UNRESOLVED ENTRIES (no id printed; never an edge)" in result.output
    row = next(line for line in result.output.splitlines() if "Hochreiter" in line)
    assert row.split()[:3] == ["P1", "arxiv:1706.03762", "14"]


def test_paper_graph_says_when_the_team_is_not_switched_on(monkeypatch, tmp_path) -> None:
    disabled = {"project_id": PROJECT_ID, "state": "disabled"}
    CitationGraphOut.model_validate(disabled)
    _install(monkeypatch, tmp_path, {("GET", _graph_path()): httpx.Response(200, json=disabled)})

    result = CliRunner().invoke(cli_main.app, ["paper", "graph", "--project", "review"])

    assert result.exit_code == 0, result.output
    assert "not switched on for your team (state: disabled)" in result.output
    assert "PAPERS" not in result.output


def test_paper_graph_needs_a_project(monkeypatch, tmp_path) -> None:
    server = _install(monkeypatch, tmp_path, {})

    result = CliRunner().invoke(cli_main.app, ["paper", "graph"])

    assert result.exit_code == 2
    assert "probe project use" in result.output
    assert server.requests == []


def test_provider_citation_help_says_reference_list_and_points_at_cites() -> None:
    """`provider_citation` is our PATH through the literature ("found it in a
    reference list"); the literature fact itself is a `cites` link."""
    root = get_command(cli_main.app)
    via = next(
        p for p in root.commands["paper"].commands["add"].params if p.name == "via_provenance"
    )
    assert "provider_citation (you found it in a reference list)" in " ".join(via.help.split())
    add_doc = " ".join(root.commands["paper"].commands["add"].help.split())
    assert "`cites` link" in add_doc and "probe paper citations" in add_doc
    provenance = next(
        p for p in root.commands["edge"].commands["add"].params if p.name == "provenance"
    )
    help_text = " ".join(provenance.help.split())
    assert "you found the paper in a reference list" in help_text and "`cites` link" in help_text
