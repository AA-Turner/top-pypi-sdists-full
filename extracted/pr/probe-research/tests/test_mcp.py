"""The MCP server is compact, structured, and read-only."""

from __future__ import annotations

import asyncio
import json

import pytest

from probe.mcp.contract import Capability, MissingMarker
from probe.mcp.server import create_server
from probe.mcp.service import ResearchReadService, _supported_views
from probe.mcp.source import ResearchOSSource
from probe.sdk import errors
from tests.conftest import search_response as _search_response


def test_context_and_search_read_through_the_current_api(client, app):
    app.search_response = _search_response(
        exact=[
            {
                "entity_type": "experiment",
                "id": "e-1",
                "name": "dockq-path",
                "slug": "dockq-path",
                "workspace_id": None,
                "project_id": "p-1",
                "experiment_id": None,
                "run_id": None,
                "score": 0.7,
            },
        ],
        semantic_error="engine_timeout",
    )
    project = client.create_project("folding", kind="general")
    client.create_experiment("dockq-path", "dockq-path", question="h", project_id=project["id"])
    client.run(
        project="folding",
        experiment="dockq-path",
        name="eval-1",
    )
    service = ResearchReadService(ResearchOSSource(client))

    context = service.research_context("DockQ scoring paths", project_ref="folding")
    # `scope` is NOT asserted here any more: the envelope is compact by default,
    # and tenant identity is constant per token, so it ships only under
    # verbose=True (pinned by test_verbose_false_keeps_the_fields_an_agent_acts_on).
    # Capabilities are STATIC now (the MCP only ever talks to the hosted
    # backend), so semantic_search is True here and compaction drops it. What a
    # given response actually LACKS is `completeness.missing`, asserted below --
    # which is the split Capability's docstring always prescribed.
    assert "capabilities" not in context
    assert context["data"]["project"]["id"] == project["id"]

    # The engine is down in this fixture, so the response says so through the
    # channel error and the missing marker -- not through the capability map.
    results = service.search_knowledge("DockQ paths")
    assert results["data"]["results"][0]["id"] == "e-1"
    assert results["completeness"]["state"] == "partial"
    assert "semantic_search" in results["completeness"]["missing"]


# -- research_search over POST /v1/search (workspaces+kb fold-in) ------------
def test_search_maps_search_in_and_merges_channels(client, app):
    app.search_response = _search_response(
        exact=[
            {
                "entity_type": "experiment",
                "id": "e-1",
                "name": "adam sweep",
                "slug": "adam-sweep",
                "workspace_id": "ws-1",
                "project_id": "p-1",
                "experiment_id": None,
                "run_id": None,
                "score": 0.91,
            },
            {
                "entity_type": "artifact",
                "id": "a-1",
                "name": "adam.csv",
                "slug": None,
                "workspace_id": None,
                "project_id": None,
                "experiment_id": "e-1",
                "run_id": "r-1",
                "score": 0.55,
            },
        ],
        semantic=[
            {
                "doc_id": "file:f-1",
                "title": "sweep notes",
                "snippet": "adam beta2 ...",
                "score": 0.83,
                "source_system": "workspace",
                "source_url": None,
                "ref": {"kind": "file", "id": "f-1"},
            },
        ],
        exact_cursor="exact-c1",
    )
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge(
        "adam sweep", search_in=["documents"], workspace_id="ws-1", collapse=None
    )

    # search_in vocabulary maps onto backend corpus values (documents -> github+files)
    # and narrows to exactly what was named; the workspace lens rides along and
    # `top_k` is a TOTAL, so each channel is asked for all 8 and the merge cuts.
    body = app.search_requests[-1]
    assert body["query"] == "adam sweep"
    assert body["corpus"] == ["files", "github"]
    assert body["workspace_id"] == "ws-1"
    assert body["top_k"] == 8 and body["exact_limit"] == 8

    # merged result list keeps the tool contract with per-channel provenance
    results = out["data"]["results"]
    assert [r["why_matched"]["channel"] for r in results] == ["exact", "semantic", "exact"]
    assert results[0]["entity_type"] == "experiment"
    assert results[0]["resource"] == "research://experiments/e-1/card"
    assert results[0]["why_matched"] == {
        "mode": "exact",
        "channel": "exact",
        "score": 0.91,
    }
    assert results[1]["entity_type"] == "file" and results[1]["id"] == "f-1"
    assert results[1]["card"]["snippet"] == "adam beta2 ..."
    assert results[2]["entity_type"] == "artifact" and results[2]["card"]["run_id"] == "r-1"

    assert "completeness" not in out
    # The envelope is compact, so a TRUE flag is absent by design -- the report
    # of what the probe discovered lives on the source, which is the surface
    # this is really asserting about.
    caps = service.source.capabilities()
    assert caps["unified_search"] and caps["semantic_search"] and caps["kb_documents"]
    # ...and the compact envelope carries no capability map at all (it is static
    # per release; verbose keeps it).
    assert "capabilities" not in out

    # Per-channel backend cursors ride one opaque tool cursor, round-trippable.
    # Opaque means opaque: this used to assert json.loads(next_cursor) == {...},
    # pinning the cursor to raw JSON -- the very thing that made it unusable through
    # the MCP tool layer (FastMCP pre-parses a JSON-object string arg into a dict,
    # which then fails `cursor: str`). What matters is the ROUND TRIP, below; the
    # encoding is nobody's business. See tests/test_mcp_tool_layer.py.
    with pytest.raises(json.JSONDecodeError):
        json.loads(out["next_cursor"])
    service.search_knowledge("adam sweep", cursor=out["next_cursor"])
    assert app.search_requests[-1]["exact_cursor"] == "exact-c1"
    assert "semantic_cursor" not in app.search_requests[-1]


def test_search_transcripts_value_maps_to_backend(client, app):
    # transcripts is now a first-class backend corpus (POST /v1/search accepts and
    # defaults to it), so the tool maps it through instead of degrading it to an
    # unsupported kb_values miss.
    app.search_response = _search_response()
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("q", search_in=["transcripts", "files"])
    assert app.search_requests[-1]["corpus"] == ["files", "transcripts"]
    assert "completeness" not in out
    assert out["data"]["unsupported_values"] == []


def test_search_narrowing_does_not_drag_experiments_along(client, app):
    """Naming search_in values narrows to EXACTLY those.

    Unioning experiments in unconditionally made a narrowed search unusable: the
    per-channel budget is ~top_k/2 and experiment projections outrank the
    knowledge corpora, so `search_in=["transcripts"]` came back holding nothing but
    experiments — the ingested Claude Code sessions were unreachable through the
    tool even though the backend indexed and returned them."""
    app.search_response = _search_response()
    service = ResearchReadService(ResearchOSSource(client))

    service.search_knowledge("q", search_in=["transcripts"])
    assert app.search_requests[-1]["corpus"] == ["transcripts"]

    # ...and a caller who wants both still says so.
    service.search_knowledge("q", search_in=["experiments", "transcripts"])
    assert app.search_requests[-1]["corpus"] == ["experiments", "transcripts"]

    # An entirely unrecognized narrowing keeps the experiments-only floor rather
    # than falling through to an unfiltered tenant-wide search. The floor is only
    # honest if the envelope also says the narrowing was NOT honored — without the
    # kb_values marker this answers a different question wearing a "complete" label.
    out = service.search_knowledge("q", search_in=["nonsense"])
    assert app.search_requests[-1]["corpus"] == ["experiments"]
    assert out["data"]["unsupported_values"] == ["nonsense"]
    assert out["completeness"] == {"state": "partial", "missing": ["kb_values"]}


def test_search_in_papers_reaches_the_papers_corpus(client, app):
    """`papers` is a real `search_in` value and maps to the papers corpus alone.

    The corpus shipped in research-os 0170 and never reached this vocabulary, so
    for five months there was NO `search_in` value that named it -- the third
    time a backend corpus landed here late (notes and digests were the first
    two). It surfaced as `unsupported_values: ["papers"]` plus the
    experiments-only floor, which is a search of the wrong corpus wearing a
    "partial" label.

    Its OWN value, not folded into `documents` or `notes`: a paper is what the
    field published, not what this team wrote or ran.
    """
    app.search_response = _search_response()
    service = ResearchReadService(ResearchOSSource(client))

    out = service.search_knowledge("q", search_in=["papers"])
    assert app.search_requests[-1]["corpus"] == ["papers"]
    assert out["data"]["unsupported_values"] == []
    assert "completeness" not in out


def test_papers_do_not_drag_experiments_along(client, app):
    """Papers physically SHARE the experiments source_key, and this asserts the
    mapping does not leak that.

    /v1/search separates them after retrieval by document-id prefix. Were the
    mapping to union experiments in "because that is the key they ride", a
    papers search would come back holding the hundreds of project, experiment
    and run documents papers sit beside -- the crowd-out this vocabulary already
    removed once for transcripts."""
    app.search_response = _search_response()
    service = ResearchReadService(ResearchOSSource(client))

    service.search_knowledge("q", search_in=["papers"])
    assert app.search_requests[-1]["corpus"] == ["papers"]

    service.search_knowledge("q", search_in=["papers", "experiments"])
    assert app.search_requests[-1]["corpus"] == ["experiments", "papers"]


def test_one_unrecognized_value_does_not_widen_the_narrowing(client, app):
    """A typo alongside a real value must not resurrect the experiments union.

    The floor is `if not backend`, NOT `if unsupported` — the difference is
    invisible until a caller pairs a good value with a bad one, and getting it
    wrong silently restores the crowd-out bug for exactly that call."""
    app.search_response = _search_response()
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("q", search_in=["documents", "bogus"])
    assert app.search_requests[-1]["corpus"] == ["files", "github"]
    assert out["data"]["unsupported_values"] == ["bogus"]
    assert out["completeness"]["missing"] == ["kb_values"]


def test_a_missing_search_route_fails_truthfully_with_no_keyword_fallback(client, app):
    """`app.search_response` stays None, so the fake 404s POST /v1/search.

    The keyword fallback is gone with the probe. It existed for backends
    predating /v1/search, which the MCP cannot reach, and keeping it meant a
    scoped 404 had to be attributed without asking the server — which made the
    fallback unreachable for every scoped call anyway. A route that is genuinely
    absent now says so instead of quietly answering from trigram matching.
    """
    _p = client.create_project("folding", kind="general")
    client.create_experiment("dockq-path", "dockq-path", question="h", project_id=_p["id"])
    client.run(project="folding", experiment="dockq-path", name="eval-1")
    service = ResearchReadService(ResearchOSSource(client))
    with pytest.raises(errors.CapabilityUnavailable):
        service.search_knowledge("DockQ paths", search_in=["documents"])
    # The original and ONE retry: a stale pod mid-deploy 404s like a missing
    # route, so the retry has to happen before the 404 is attributed.
    assert len(app.search_requests) == 2, "should try POST /v1/search, then retry once"


def test_search_partial_passthrough_when_engine_down(client, app):
    app.search_response = _search_response(
        state="partial",
        exact=[
            {
                "entity_type": "project",
                "id": "p-1",
                "name": "folding",
                "slug": "folding",
                "workspace_id": "ws-1",
                "project_id": None,
                "experiment_id": None,
                "run_id": None,
                "score": 1.0,
            },
        ],
        semantic_error="engine_timeout",
    )
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("folding", collapse=None)
    assert out["completeness"] == {"state": "partial", "missing": ["semantic_search"]}
    assert out["data"]["channels"]["semantic"]["error"] == "engine_timeout"
    assert [r["entity_type"] for r in out["data"]["results"]] == ["project"]
    assert out["data"]["results"][0]["resource"] == "research://projects/p-1/card"
    # The capability map says what the backend SUPPORTS and is static; a channel
    # that could not answer right now is a property of this RESPONSE, and it is
    # reported through completeness.missing (asserted above) plus the channel's
    # own error. Reporting a transient outage as a missing capability would tell
    # an agent the feature does not exist.
    assert service.source.capabilities()["semantic_search"] is True
    assert "capabilities" not in out


def test_capabilities_are_static_and_cost_no_backend_request(client, app):
    """The probe that used to answer this ran a REAL billed search.

    It sent the literal query "capability probe" through POST /v1/search
    without `include_semantic`, inheriting the server default of True, so every
    MCP session start consumed one metered recall action and emitted a
    content-inclusive `search_performed` event. The MCP only ever talks to the
    hosted backend, so the question had a constant answer.
    """
    app.search_response = _search_response()
    service = ResearchReadService(ResearchOSSource(client))
    context = service.research_context("anything")
    caps = service.source.capabilities()
    assert caps["unified_search"] and caps["semantic_search"]
    assert "capabilities" not in context
    assert "semantic_search" not in context.get("completeness", {}).get("missing", [])
    assert app.search_requests == []  # no probe, at any point
    service.research_context("again")
    assert app.search_requests == []


def test_every_declared_capability_is_reported(client):
    """`project_scoped_search` was declared and never populated, so every reader
    saw a capability the product HAS as absent. A map that silently omits a key
    is the same lie as one that hardcodes it False."""
    caps = ResearchOSSource(client).capabilities()
    assert set(caps) == set(Capability)


def test_search_unknown_workspace_is_not_found_not_fallback(client, app):
    # The contract 404s an unknown/foreign workspace_id (oracle-safe); that must
    # surface as NotFound, not silently degrade to the keyword fallback.
    app.search_response = _search_response()
    app.search_404_workspace_ids.add("ws-missing")
    service = ResearchReadService(ResearchOSSource(client))
    with pytest.raises(errors.NotFoundError):
        service.search_knowledge("q", workspace_id="ws-missing")
    # original + ONE retry. The retry costs a wasted request on a genuinely
    # absent scope, and buys a correct answer when the 404 came from a stale pod
    # mid-deploy instead. Attributing a scoped 404 to the scope without retrying
    # turns a rolling deploy into "your project does not exist", which is a
    # wrong answer about the caller's own data. It used to cost three: the
    # middle one was a capability probe working out whether the ROUTE was gone,
    # which the request itself already answers.
    assert len(app.search_requests) == 2  # original + ONE retry


def test_search_cuts_to_top_k_and_says_what_it_could_not_carry(client, app):
    # More rows come back than `top_k`: the extras are NOT emitted (the caller
    # asked for a total), nothing is silently dropped either -- the count that
    # was available rides on the payload and the cursor is withheld.
    exact = [
        {
            "entity_type": "experiment",
            "id": f"e-{i}",
            "name": f"exp {i}",
            "slug": f"exp-{i}",
            "workspace_id": None,
            "project_id": "p-1",
            "experiment_id": None,
            "run_id": None,
            "score": 1.0 - i / 10,
        }
        for i in range(3)
    ]
    semantic = [
        {
            "doc_id": f"file:f-{i}",
            "title": f"doc {i}",
            "snippet": "...",
            "score": 0.9 - i / 10,
            "source_system": "workspace",
            "source_url": None,
            "ref": {"kind": "file", "id": f"f-{i}"},
        }
        for i in range(3)
    ]
    app.search_response = _search_response(exact=exact, semantic=semantic)
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("q", top_k=4, collapse=None)
    body = app.search_requests[-1]
    # `top_k` is a TOTAL: each channel is asked for all of it, and the merge
    # cuts to it. Splitting it meant a default search showed four results and
    # called it eight, because the exact channel answers nothing most of the
    # time.
    assert body["top_k"] == 4 and body["exact_limit"] == 4
    assert len(out["data"]["results"]) == 4
    # Rows were left over, so there is no cursor: the per-channel cursors
    # advance by what was FETCHED, and handing one back here would skip the two
    # rows the caller was told to page for.
    assert "next_cursor" not in out
    assert MissingMarker.RESULTS_BEYOND_BUDGET in out["completeness"]["missing"]
    assert out["data"]["budget"]["results_available"] == 6


def test_search_two_page_walk_skips_and_duplicates_nothing(client, app):
    def exact_row(i):
        return {
            "entity_type": "experiment",
            "id": f"e-{i}",
            "name": f"exp {i}",
            "slug": f"exp-{i}",
            "workspace_id": None,
            "project_id": "p-1",
            "experiment_id": None,
            "run_id": None,
            "score": 1.0 - i / 10,
        }

    def semantic_row(i):
        return {
            "doc_id": f"file:f-{i}",
            "title": f"doc {i}",
            "snippet": "...",
            "score": 0.9 - i / 10,
            "source_system": "workspace",
            "source_url": None,
            "ref": {"kind": "file", "id": f"f-{i}"},
        }

    app.search_responses = [
        _search_response(
            exact=[exact_row(0), exact_row(1)],
            semantic=[semantic_row(0), semantic_row(1)],
            exact_cursor="ex-2",
            semantic_cursor="se-2",
        ),
        _search_response(exact=[exact_row(2)], semantic=[semantic_row(2)]),
    ]
    service = ResearchReadService(ResearchOSSource(client))
    page1 = service.search_knowledge("q", top_k=4, collapse=None)
    assert len(page1["data"]["results"]) == 4
    page2 = service.search_knowledge("q", top_k=4, collapse=None, cursor=page1["next_cursor"])
    assert app.search_requests[-1]["exact_cursor"] == "ex-2"
    assert app.search_requests[-1]["semantic_cursor"] == "se-2"
    ids = [r["id"] for r in page1["data"]["results"] + page2["data"]["results"]]
    assert sorted(ids) == ["e-0", "e-1", "e-2", "f-0", "f-1", "f-2"]  # nothing skipped
    assert len(set(ids)) == len(ids)  # nothing duplicated
    assert "next_cursor" not in page2


def test_search_collapse_experiment_dedupes_across_channels(client, app):
    app.search_response = _search_response(
        exact=[
            {
                "entity_type": "experiment",
                "id": "e-1",
                "name": "adam",
                "slug": "adam",
                "workspace_id": None,
                "project_id": "p-1",
                "experiment_id": None,
                "run_id": None,
                "score": 0.7,
            },
            {
                "entity_type": "project",
                "id": "p-1",
                "name": "folding",
                "slug": "folding",
                "workspace_id": None,
                "project_id": None,
                "experiment_id": None,
                "run_id": None,
                "score": 0.95,
            },
        ],
        semantic=[
            {
                "doc_id": "experiment:e-1",
                "title": "adam card",
                "snippet": "...",
                "score": 0.9,
                "source_system": "experiments",
                "source_url": None,
                "ref": {"kind": "experiment", "id": "e-1"},
            },
            {
                "doc_id": "file:f-1",
                "title": "notes",
                "snippet": "...",
                "score": 0.8,
                "source_system": "workspace",
                "source_url": None,
                "ref": {"kind": "file", "id": "f-1"},
            },
        ],
    )
    service = ResearchReadService(ResearchOSSource(client))

    # default collapse="experiment": the TWO experiment hits become one, keeping
    # the best-scoring representative's channel provenance (semantic, 0.9 > 0.7).
    # The project and file hits are not experiments and are not deduped away —
    # collapse dedupes, it never filters.
    out = service.search_knowledge("adam")
    results = out["data"]["results"]
    assert [r["id"] for r in results] == ["e-1", "p-1", "f-1"]
    assert results[0]["entity_type"] == "experiment"
    assert results[0]["why_matched"]["channel"] == "semantic"
    assert results[0]["why_matched"]["score"] == 0.9

    # collapse=None keeps both experiment rows instead of merging them
    out = service.search_knowledge("adam", collapse=None)
    assert {r["entity_type"] for r in out["data"]["results"]} == {
        "experiment",
        "project",
        "file",
    }
    assert len(out["data"]["results"]) == 4


def test_a_scope_in_hand_wins_over_a_genuinely_absent_route(client, app):
    """The deliberate edge of the 404 rule, stated so nobody 'fixes' it.

    Here the ROUTE is absent (`search_response` stays None) AND a scope was
    given. The rule blames the scope, so this raises NotFound rather than
    CapabilityUnavailable. That is wrong about this fake and right about the
    hosted backend, which is the only backend the MCP talks to and where
    /v1/search always exists — there, a scoped 404 really does mean the scope
    is gone. Telling a researcher "this project is empty" when the project is
    not theirs is the worse error, so the rule is tuned for the real case.

    The honest version of each half: `test_search_unknown_workspace_...` and
    `test_a_project_scoped_search_404_names_the_project_not_the_route` both
    model route-present/scope-absent, which is the shape that actually occurs.
    """
    service = ResearchReadService(ResearchOSSource(client))
    with pytest.raises(errors.NotFoundError):
        service.search_knowledge("q", workspace_id="ws-1")
    assert len(app.search_requests) == 2  # original + ONE retry


def test_a_project_scoped_search_404_names_the_project_not_the_route(client, app):
    """A scoped 404 on a backend that HAS the route means that scope is absent.

    `search_404_project_ids` makes the fake answer normally except for this one
    project, which is the live backend's shape: `/v1/search` is there and
    `require_project` 404s an id the tenant does not own. Reporting that as a
    missing route, or answering it from trigram matching, would both turn "that
    project is not there" into "that project is empty".
    """
    app.search_response = _search_response()
    app.search_404_project_ids.add("p-missing")
    service = ResearchReadService(ResearchOSSource(client))
    with pytest.raises(errors.NotFoundError):
        service.search_knowledge("q", project_id="p-missing")
    assert len(app.search_requests) == 2  # original + ONE retry


def test_search_forwards_project_scope_to_the_backend(client, app):
    app.search_response = _search_response(
        exact=[
            {
                "entity_type": "experiment",
                "id": "e-1",
                "name": "in",
                "slug": "in",
                "workspace_id": None,
                "project_id": "p-1",
                "experiment_id": None,
                "run_id": None,
                "score": 0.9,
            },
            {
                "entity_type": "experiment",
                "id": "e-2",
                "name": "out",
                "slug": "out",
                "workspace_id": None,
                "project_id": "p-2",
                "experiment_id": None,
                "run_id": None,
                "score": 0.8,
            },
            {
                "entity_type": "project",
                "id": "p-1",
                "name": "proj",
                "slug": "proj",
                "workspace_id": None,
                "project_id": None,
                "experiment_id": None,
                "run_id": None,
                "score": 0.7,
            },
            {
                "entity_type": "artifact",
                "id": "a-1",
                "name": "unlinked.csv",
                "slug": None,
                "workspace_id": None,
                "project_id": None,
                "experiment_id": None,
                "run_id": "r-9",
                "score": 0.6,
            },
        ],
        semantic=[
            {
                "doc_id": "file:f-1",
                "title": "doc",
                "snippet": "...",
                "score": 0.9,
                "source_system": "workspace",
                "source_url": None,
                "ref": {"kind": "file", "id": "f-1"},
            },
        ],
        semantic_cursor="se-2",
    )
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("q", project_id="p-1", collapse=None)
    # Project scope is the BACKEND's job now (research-os #103): it re-resolves
    # semantic hits against live rows and over-fetches so the filter runs before
    # the cap. The tool passes the scope through and keeps whatever comes back.
    #
    # This previously emptied the semantic channel client-side and reported
    # project_scope_unsupported, so a scoped search silently degraded to trigram
    # matching -- the single most natural way to search was also the most
    # degraded.
    assert app.search_requests[-1]["project_id"] == "p-1"
    assert out["data"]["channels"]["semantic"]["error"] is None
    assert "file:f-1" in [r["id"] for r in out["data"]["results"]] or any(
        r["entity_type"] == "file" for r in out["data"]["results"]
    )
    assert "completeness" not in out


def test_why_matched_shape_is_uniform_across_channels(client, app):
    expected_keys = {"mode", "channel", "score"}
    app.search_response = _search_response(
        exact=[
            {
                "entity_type": "experiment",
                "id": "e-1",
                "name": "adam",
                "slug": "adam",
                "workspace_id": None,
                "project_id": "p-1",
                "experiment_id": None,
                "run_id": None,
                "score": 0.7,
            },
        ],
        semantic=[
            {
                "doc_id": "file:f-1",
                "title": "notes",
                "snippet": "...",
                "score": 0.8,
                "source_system": "workspace",
                "source_url": None,
                "ref": {"kind": "file", "id": "f-1"},
            },
        ],
    )
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("adam", collapse=None)
    assert out["data"]["results"]
    for row in out["data"]["results"]:
        assert set(row["why_matched"]) == expected_keys
    # The keyword channel used to be checked here too, via the fallback. That
    # path is gone with the capability probe: the two channels a search can
    # answer from are now exactly exact and semantic, both asserted above.
    assert {row["why_matched"]["channel"] for row in out["data"]["results"]} == {
        "exact",
        "semantic",
    }


def test_an_upgrade_is_noticed_immediately_with_no_verdict_to_expire(client, app):
    """There is no cached "unsupported" verdict to go stale any more.

    The old shape cached a 404 for 300 seconds, so a backend that gained the
    route mid-session kept getting the keyword fallback until the window
    lapsed. Retrying per call costs one wasted request against a genuinely
    absent route, which is a case that cannot happen on the hosted backend.
    """
    service = ResearchReadService(ResearchOSSource(client))

    with pytest.raises(errors.CapabilityUnavailable):
        service.search_knowledge("q")  # 404 -> retry -> route is absent
    assert len(app.search_requests) == 2

    app.search_response = _search_response()
    service.search_knowledge("q")  # picked up at once, no window to wait out
    assert len(app.search_requests) == 3
    assert service.source.capabilities()["unified_search"] is True


def test_search_retries_once_on_stale_pod_404(client, app):
    app.search_response = _search_response(
        exact=[
            {
                "entity_type": "experiment",
                "id": "e-1",
                "name": "adam",
                "slug": "adam",
                "workspace_id": None,
                "project_id": "p-1",
                "experiment_id": None,
                "run_id": None,
                "score": 0.7,
            },
        ],
    )
    service = ResearchReadService(ResearchOSSource(client))
    service.search_knowledge("q")  # 1 request
    app.search_404_once = True  # one stale pod mid rolling deploy
    out = service.search_knowledge("q")  # 404 -> retried once, no probe between
    assert len(app.search_requests) == 3
    assert [r["id"] for r in out["data"]["results"]] == ["e-1"]
    assert service.source.capabilities()["unified_search"] is True


def test_malformed_cursor_raises_validation_error(client, app):
    app.search_response = _search_response()
    service = ResearchReadService(ResearchOSSource(client))
    with pytest.raises(errors.ValidationError):
        service.search_knowledge("q", cursor="not-a-packed-cursor")
    with pytest.raises(errors.ValidationError):
        service.search_knowledge("q", cursor='["wrong-shape"]')


def test_search_unknown_collapse_rejected(client, app):
    # only "experiment" (dedupe) and null (heterogeneous) are defined; anything
    # else must fail loudly instead of silently falling through
    app.search_response = _search_response()
    service = ResearchReadService(ResearchOSSource(client))
    with pytest.raises(errors.ValidationError):
        service.search_knowledge("q", collapse="run")
    assert app.search_requests == []  # rejected before any backend call


def test_token_factory_evicts_oldest_pair_beyond_cap(monkeypatch):
    from probe.mcp import server as server_mod

    server_mod._clients.clear()
    server_mod._sources.clear()
    monkeypatch.setattr(server_mod, "_MAX_CACHED_TOKENS", 3)
    closed: list[str] = []

    class FakeClient:
        def __init__(self, token):
            self.token = token

        def close(self):
            closed.append(self.token)

    # The server builds its Client from an explicit Settings (so a missing mcp_token
    # can never fall back to the write token), so read the token off settings.
    monkeypatch.setattr(
        server_mod,
        "Client",
        lambda *, settings, fail_open, surface=None, transport=None: FakeClient(settings.token),
    )

    def resolve(token):
        reset = server_mod._token_var.set(token)
        try:
            return server_mod._service_from_token()
        finally:
            server_mod._token_var.reset(reset)

    try:
        for token in ("t1", "t2", "t3"):
            resolve(token)
        resolve("t1")  # refresh t1's recency: t2 is now the stalest
        resolve("t4")  # exceeds the cap -> t2 evicted, its client closed
        assert closed == ["t2"]
        assert list(server_mod._sources) == ["t3", "t1", "t4"]
        assert list(server_mod._clients) == list(server_mod._sources)  # kept in step
        # an evicted token re-creates cleanly (and evicts the next stalest)
        service = resolve("t2")
        assert service.source.client.token == "t2"
        assert closed == ["t2", "t3"]
        assert list(server_mod._sources) == ["t1", "t4", "t2"]
        assert list(server_mod._clients) == list(server_mod._sources)
    finally:
        server_mod._clients.clear()
        server_mod._sources.clear()


def test_search_malformed_response_degrades_to_partial(client, app):
    # A broken proxy/server returning garbage must degrade, never AttributeError.
    app.search_response = {"state": "ok", "exact": "broken", "semantic": ["nope"]}
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("q", collapse=None)
    assert out["data"]["results"] == []
    assert out["completeness"]["state"] == "partial"
    assert out["data"]["channels"]["exact"]["error"] == "malformed_response"
    assert out["data"]["channels"]["semantic"]["error"] == "malformed_response"

    # wrong-typed rows inside a well-typed section are filtered and marked
    app.search_response = {
        "state": "ok",
        "exact": {
            "results": [
                123,
                {"entity_type": "experiment", "id": "e-1", "name": "x", "slug": "x", "score": 1.0},
            ],
            "cursor": 7,
            "error": None,
        },
        "semantic": {"results": [], "cursor": None, "error": None},
    }
    out = service.search_knowledge("q", collapse=None)
    assert [r["id"] for r in out["data"]["results"]] == ["e-1"]
    assert out["data"]["channels"]["exact"]["error"] == "malformed_response"
    assert "next_cursor" not in out  # the non-string cursor is dropped

    # an entirely non-dict body degrades the same way
    app.search_response = ["garbage"]
    out = service.search_knowledge("q", collapse=None)
    assert out["data"]["results"] == []
    assert out["completeness"]["state"] == "partial"


def test_identity_is_cached_across_token_factory_calls(client, app):
    """Exercises the REAL per-token wiring, and the thing it now buys.

    EVERY envelope carries the caller's identity and every read tool returns an
    envelope, so an uncached `GET /v1/me` is one request per tool call. That was
    strictly more traffic than the capability probe this branch deletes: the
    probe fired once per session, this fired forever.
    """
    from probe.mcp import server as server_mod

    server_mod._clients.clear()
    server_mod._sources.clear()
    server_mod._clients["tok-a"] = client
    app.search_response = _search_response()
    reset = server_mod._token_var.set("tok-a")
    try:
        first = server_mod._service_from_token()
        first.research_context("anything")
        second = server_mod._service_from_token()
        second.get_entity("run:some-run")
        assert first.source is second.source
        assert app.search_requests == []  # no probe, at any point
        assert app.me_requests == 1  # one identity read total, not one per call
    finally:
        server_mod._token_var.reset(reset)
        server_mod._clients.clear()
        server_mod._sources.clear()


def test_identity_cache_expires_and_never_crosses_tokens(client, app, monkeypatch):
    """Bounded staleness, and per-token by construction.

    A role can change, so the cache is a minute, not a session. And because the
    cache lives on the SOURCE and server._acquire_service memoizes one source
    per token, one tenant's identity can never be served to another.
    """
    from probe.mcp import source as source_mod

    first = ResearchOSSource(client)
    assert first.identity()["email"] == "dev@example.com"
    assert first.identity()["email"] == "dev@example.com"
    assert app.me_requests == 1  # second read served from cache

    # Past the window, it refreshes rather than serving a stale role forever.
    first._identity_at -= source_mod._IDENTITY_TTL_SECONDS + 1
    first.identity()
    assert app.me_requests == 2

    # A different source (a different token) shares nothing.
    ResearchOSSource(client).identity()
    assert app.me_requests == 3


def test_a_me_outage_serves_the_last_good_identity_instead_of_failing_every_tool(client, app):
    """Identity is a field on the envelope, not the answer the caller asked for.

    Failing the whole read because /v1/me blipped would take every tool down for
    the duration, and re-request /v1/me on each attempt — the exact per-call
    traffic the cache exists to remove, arriving when the backend can least
    absorb it. A cold cache still propagates, because then there is nothing
    truthful to serve.
    """
    from probe.mcp import source as source_mod

    src = ResearchOSSource(client)
    assert src.identity()["email"] == "dev@example.com"

    src._identity_at -= source_mod._IDENTITY_TTL_SECONDS + 1
    app.me_status = 500
    assert src.identity()["email"] == "dev@example.com"  # stale, knowingly
    assert app.me_requests == 2

    # AND it backs off. Serving stale without this would still cost one attempt
    # per tool call for the whole outage, which is the traffic the cache exists
    # to remove, arriving when the backend can least absorb it.
    for _ in range(5):
        assert src.identity()["email"] == "dev@example.com"
    assert app.me_requests == 2, "backoff should suppress the retry storm"

    # Past the backoff it tries again, and a success clears it.
    src._identity_failed_at -= source_mod._IDENTITY_FAILURE_BACKOFF_SECONDS + 1
    app.me_status = 200
    assert src.identity()["email"] == "dev@example.com"
    assert app.me_requests == 3
    assert src._identity_failed_at == float("-inf")

    # Cold cache has nothing truthful to serve, so it raises.
    app.me_status = 500
    with pytest.raises(errors.RosError):
        ResearchOSSource(client).identity()


def test_a_revoked_token_is_never_stale_served(client, app):
    """401/403 is not a blip, it is the answer changing.

    A revoked or re-scoped token means the cached identity names a researcher
    and tenant that no longer apply, which is precisely what the TTL exists to
    notice. Serving it anyway would keep reporting the old one for as long as
    the process lived.
    """
    from probe.mcp import source as source_mod

    src = ResearchOSSource(client)
    assert src.identity()["email"] == "dev@example.com"

    src._identity_at -= source_mod._IDENTITY_TTL_SECONDS + 1
    app.me_status = 401
    with pytest.raises(errors.AuthError):
        src.identity()


def test_server_exposes_exactly_the_read_tools(client):
    """Thin harness: entity coverage grows through research_get's `view`/`filters`,
    NEVER through more tools. Spans, groups, events, execution records and
    experiment versions all became reachable while the tool count went DOWN
    (trace_file, which had no backend, was removed). If this set grows, the bar
    below applies.

    `research_browse` was the first addition to earn its place, and the bar it
    cleared is worth recording. It is not another way to read an entity -- that
    is research_get's job and no view of it enumerates the tree. It answers a
    question the other tools structurally cannot: search ranks by relevance to a
    query, so it requires you to already know what to search for, and nothing
    answered "what exists here?" A `research_get_spans` would fail this bar,
    because `research_get(view="trajectory")` already answers it.

    The coordinate reads (B7) cleared the same bar. They are not entity reads
    wearing new names: grouped is a server-side REDUCTION with its own algebra
    (agg/by/where/step_bucket) whose parameters are the route's typed contract,
    export pages by a keyset cursor that get_entity's offset cursor cannot
    express without lying about stability, and the catalog is the enumeration
    that makes grouped's axes discoverable. Folding those into `filters` dicts
    on a view would hide a real contract behind an untyped bag.
    """
    service = ResearchReadService(ResearchOSSource(client))
    server = create_server(service)
    tools = asyncio.run(server.list_tools())
    names = {tool.name for tool in tools}
    # MCP tools are served by the SERVER and .mcp.json pins one url for every
    # plugin version, so renaming a tool breaks every installed client the
    # instant the image rolls. A window is therefore OPEN again: the metric
    # collapse registers `read_metrics` and keeps the three names it replaces as
    # deprecated aliases for one release. Both sets are asserted so neither can
    # drift — and DEPRECATED_SURFACE is the list to delete, in one change with
    # the plugin `min` bump, once the alias warnings are quiet.
    assert names == NEW_SURFACE | DEPRECATED_SURFACE
    assert not any(name.startswith(("create", "update", "promote", "upload")) for name in names)


NEW_SURFACE = {
    "browse",
    "search_knowledge",
    "entity",
    "metrics",
    # Research literature is the only externally authored MCP read.
    "find_papers",
    # Read-only SQL: a SELECT in a READ ONLY transaction under the caller's RLS.
    "query_sql",
}

#: Retired names still answered, for one release only. Every one is a
#: fixed-mode delegation to `read_metrics`.
DEPRECATED_SURFACE: set[str] = set()  # hard cutover: the three
# one-release metric stubs went with the browse/entity/metrics rename.


# -- hosted HTTP mode: per-request auth + health -----------------------------
def test_http_auth_middleware_propagates_token_and_health():
    from probe.mcp.server import _token_var, with_auth_and_health

    captured: dict = {}

    async def fake_inner(scope, receive, send):
        captured["token"] = _token_var.get()
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})

    app = with_auth_and_health(fake_inner)

    async def drive(path, headers):
        scope = {"type": "http", "path": path, "headers": headers}
        sent: list = []

        async def receive():
            return {"type": "http.request", "body": b"", "more_body": False}

        async def send(m):
            sent.append(m)

        await app(scope, receive, send)
        return sent

    # the caller's bearer token reaches the inner app (i.e. the tool)
    asyncio.run(drive("/mcp", [(b"authorization", b"Bearer tok-123")]))
    assert captured["token"] == "tok-123"
    # and is cleared after the request (no leak across tenants)
    assert _token_var.get() is None
    # health endpoint answers without touching the inner app
    sent = asyncio.run(drive("/healthz", []))
    assert sent[0]["status"] == 200


def test_service_resolves_from_request_token():
    from probe.mcp.server import _clients, _service_from_token, _sources, _token_var

    _clients.clear()
    _sources.clear()
    reset = _token_var.set("read-only-tok")
    try:
        _service_from_token()
        assert "read-only-tok" in _clients
        assert "read-only-tok" in _sources
        assert _clients["read-only-tok"].settings.token == "read-only-tok"
    finally:
        _token_var.reset(reset)
        _clients.clear()
        _sources.clear()


def test_http_app_builds():
    from probe.mcp.server import http_app

    app = http_app()  # FastMCP streamable-http + auth/health wrapper
    assert callable(app)


def _browse_payload() -> dict:
    return {
        "projects": [
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "name": "bird-sql",
                "slug": "bird-sql",
                "description": "Text-to-SQL agentic RL on the BIRD benchmark.",
                "workspace_id": None,
                "created_at": "2026-07-01T00:00:00Z",
                "experiment_count": 2,
                "active_run_count": 1,
                "experiments": None,
            }
        ],
        "experiments": None,
        "runs": None,
        "cursor": None,
        "depth": 1,
        "limit": 50,
        "truncated": False,
    }


def test_browse_annotates_nodes_with_ref_and_available_views(app, client):
    """Every node carries what the NEXT call needs: both addresses research_get
    accepts, and the exact views valid for that kind -- derived from the same
    matrix research_get validates against, so the two cannot disagree."""
    app.browse_response = _browse_payload()
    service = ResearchReadService(ResearchOSSource(client))
    envelope = service.browse_research()

    [node] = envelope["data"]["projects"]
    assert node["uuid"] == "project:11111111-1111-1111-1111-111111111111"
    assert node["entity_type"] == "project"
    # No `ref` key at all. It held the uuid under a name that said "reference",
    # which taught callers to copy the unreadable address while the readable one
    # sat unused in the same object.
    assert "ref" not in node
    # No bare `id` either: it was byte-identical to the tail of `uuid`, an
    # unlabelled second copy of the one address this surface deprecates.
    assert "id" not in node
    # The one-line identity rides on the node -- deciding which project to open
    # must not cost a per-project card call.
    assert node["description"] == "Text-to-SQL agentic RL on the BIRD benchmark."
    # Null-valued keys are OMITTED (same rule as slug): absence says "nothing
    # here", null invites pasting "None". workspace_id/experiments were null.
    assert "workspace_id" not in node
    assert "experiments" not in node
    # Derived, never hand-written -- but ONCE on the envelope, keyed by kind,
    # not repeated on every node of the kind.
    assert "available_views" not in node
    assert envelope["data"]["available_views"] == {
        "project": ["artifacts", "card", "code", "lineage", "notes", "papers", "record", "summary"]
    }
    assert "completeness" not in envelope
    # Unexpanded levels stay None -- distinct from [] (expanded, empty).
    assert envelope["data"]["experiments"] is None


def test_browse_available_views_track_the_real_view_matrix(app, client):
    """The views advertised must be the views research_get actually accepts.

    A hand-maintained list is how docs end up naming views that no longer
    exist, so this asserts the advertised set IS the validated set.
    """
    from probe.mcp.service import _supported_views

    app.browse_response = {
        **_browse_payload(),
        "projects": None,
        "runs": [
            {
                "id": "22222222-2222-2222-2222-222222222222",
                "name": "r",
                "slug": None,
                "status": "running",
                "created_at": "2026-07-01T00:00:00Z",
                "started_at": None,
                "ended_at": None,
                "alive": None,
            }
        ],
    }
    service = ResearchReadService(ResearchOSSource(client))
    data = service.browse_research(scope="experiment:x")["data"]
    [run] = data["runs"]
    assert "available_views" not in run
    assert data["available_views"]["run"] == _supported_views("run")
    assert "trajectory" in data["available_views"]["run"]


def test_browse_on_an_old_backend_reports_missing_not_empty(app, client):
    """ "Nothing exists" and "I cannot tell you what exists" are opposite claims.

    Returning an empty tree for a backend without the route would stop an agent
    looking any further, so the envelope says the capability is missing instead.
    """
    app.browse_response = None  # route 404s, as a pre-browse backend does
    service = ResearchReadService(ResearchOSSource(client))
    envelope = service.browse_research()

    assert envelope["completeness"]["state"] == "partial"
    assert "structured_browse" in envelope["completeness"]["missing"]
    assert envelope["data"]["projects"] is None
    # The marker carries it, not the capability map: browse finds out by CALLING
    # the route and getting a truthful failure, which is why nothing probes it
    # up front.
    assert "capabilities" not in envelope


def test_browse_scoped_404_is_a_missing_scope_not_a_missing_route(app, client):
    """A scoped 404 means the SCOPE was not found on a backend that HAS the
    route. Treating it as "no browse endpoint" would blind the tool to the whole
    tree because one id was wrong."""
    app.browse_response = None
    service = ResearchReadService(ResearchOSSource(client))
    with pytest.raises(errors.NotFoundError):
        service.browse_research(scope="project:does-not-exist")


def test_browse_truncation_is_reported(app, client):
    """A cut tree must not read as a complete one: an absent child would
    otherwise look like evidence of absence."""
    app.browse_response = {**_browse_payload(), "truncated": True}
    service = ResearchReadService(ResearchOSSource(client))
    envelope = service.browse_research(depth=2)
    assert envelope["completeness"]["state"] == "partial"
    assert "truncated_by_token_budget" in envelope["completeness"]["missing"]


# -- the prose contract ------------------------------------------------------
# Two halves of this product are prose: the server `instructions` (ships with
# the image, cannot go stale) and the tool docstrings (same). Both are load-
# bearing -- they are the entire mechanism by which an agent decides to call
# anything. These guard the claims that would silently rot.


def _call_tool(server, tool: str, args: dict):
    """Invoke a tool the way a real MCP client does, and unwrap the payload."""
    import asyncio as _asyncio

    result = _asyncio.run(server.call_tool(tool, args))
    payload = result[1] if isinstance(result, tuple) else result
    if isinstance(payload, dict) and "result" in payload:
        return payload["result"]
    if isinstance(payload, list):
        return json.loads(payload[0].text)
    return payload


def _tool_docs(client) -> dict[str, str]:
    import asyncio as _asyncio

    server = create_server(ResearchReadService(ResearchOSSource(client)))
    return {t.name: (t.description or "") for t in _asyncio.run(server.list_tools())}


def _tool_schemas(client) -> dict[str, dict]:
    import asyncio as _asyncio

    server = create_server(ResearchReadService(ResearchOSSource(client)))
    return {t.name: t.inputSchema for t in _asyncio.run(server.list_tools())}


def test_the_view_matrix_in_the_schema_matches_the_real_one(client):
    """The docstring advertises views; _VIEWS decides them.

    A hand-written matrix is how documentation ends up naming views that no
    longer exist -- an agent then asks for one, gets a validation error, and the
    error contradicts the docs it just followed.
    """
    from probe.mcp.service import _VIEWS, _supported_views

    # The matrix moved out of the docstring and into `view`'s schema description:
    # a `description` is capped at 2,048 chars by the client and a schema is not,
    # and entity was 7,446. It is now BUILT from `_VIEWS` rather than typed out
    # beside it, so drift is impossible instead of merely caught here -- what this
    # test still proves is that the built matrix REACHES the agent.
    doc = _tool_schemas(client)["entity"]["properties"]["view"]["description"]
    for kind in sorted({k for k, _ in _VIEWS}):
        line = next((ln for ln in doc.splitlines() if ln.strip().startswith(kind + " ")), None)
        assert line, f"get_entity docstring does not document kind {kind!r}"
        advertised = {p.strip() for p in line.split(None, 1)[1].split("|")}
        assert advertised == set(_supported_views(kind)), (
            f"{kind}: docstring says {sorted(advertised)}, _VIEWS says {_supported_views(kind)}"
        )


def test_mcp_guidance_distinguishes_visible_summary_from_hidden_notes(client):
    """ENTITY carries this contract, and since 2026-09-13 only entity.

    The server instruction sheet used to carry it too. It was cut there because
    the sheet is for what is true of EVERY tool -- the ladder, the evidence
    guard, the paging contract -- and `summary_markdown` is one tool's data
    contract, taught better on the tool that returns it.

    Since 2026-09-17 the authored Markdown is the researcher's BY POLICY (the
    `probe <kind> set --summary` flag still exists), so the contract here is
    about READING: what the `summary` view is (whole-document, last-write-wins)
    and that the hidden notes are a separate, appending document. The sheet no
    longer names the write.

    0219 moved WHERE it lives: on a project or experiment it is a block inside
    the Overview page rather than a field below it, and a read of it is the
    page's RENDERING of the document. An agent told to expect its own bytes
    back writes the document again to force a match and degrades it each time,
    so the description has to say that it will not match.
    """
    # Sliced at the client cap on purpose: a sentence pinned here that falls past
    # 2,048 characters is a sentence no agent receives.
    docs = " ".join(_tool_docs(client)["entity"][:2048].split())

    for text in (docs,):
        # 0220: "below the AI Summary" was the RUN's half of this sentence and
        # went with the run's document. What has to survive is the boundary it
        # described: an Overview page the AI writes, carrying a block it may
        # not rewrite.
        assert "Overview" in text and "AI may not rewrite" in text
        assert "authored" in text and "Markdown" in text
        assert "project" in text and "experiment" in text
        assert "document" in text
        assert "hidden" in text and "notes" in text
        assert "whole-document" in text.lower()
        assert "last-write-wins" in text
        # WHERE it lives, and that a read is not the bytes you sent.
        assert "INSIDE a project's or experiment's Overview page" in text
        assert "RENDERED" in text and "byte-identical" in text


def test_verbose_false_keeps_the_fields_an_agent_acts_on(client, app):
    """Compaction must drop bookkeeping, never signal.

    The interesting half of a drop-list is what it KEEPS: a list without stated
    reasons rots into dropping something load-bearing.
    """
    app.search_response = _search_response(
        exact=[
            {
                "entity_type": "experiment",
                "id": "e-1",
                "name": "n",
                "slug": "s",
                "workspace_id": None,
                "project_id": None,
                "experiment_id": None,
                "run_id": None,
                "score": 0.9,
            },
        ],
        semantic_error="engine_timeout",
    )
    service = ResearchReadService(ResearchOSSource(client))
    full = service.search_knowledge("q", verbose=True)
    lean = service.search_knowledge("q", verbose=False)

    # Constant-per-token bookkeeping goes.
    for gone in ("schema_version", "as_of", "scope"):
        assert gone in full and gone not in lean

    # completeness ALWAYS survives: it is the only field saying what the
    # response could not cover. Stripping it turns a partial answer into a
    # confident one.
    assert lean["completeness"]["state"] == "partial"
    assert "semantic_search" in lean["completeness"]["missing"]
    assert lean["data"]["results"] == full["data"]["results"]


def test_compact_envelope_carries_no_default_valued_bookkeeping(client, app):
    """The capability map is STATIC for the hosted backend, so it is constant per
    release like scope/as_of -- and its one False flag (portable_snapshots) rode
    every read. A complete `completeness` and a null `next_cursor` say "this is
    all of it", which absence says for free. Verbose keeps every one of them."""
    app.search_response = _search_response()
    service = ResearchReadService(ResearchOSSource(client))
    lean = service.search_knowledge("q", verbose=False)
    full = service.search_knowledge("q", verbose=True)
    assert set(lean) == {"data"}
    assert full["capabilities"] == service.source.capabilities()
    assert full["completeness"] == {"state": "complete", "missing": []}
    assert "next_cursor" in full and full["next_cursor"] is None


def test_project_scope_degrades_on_a_backend_that_ignores_it(client, app):
    """A backend predating server-side project scope must not answer silently.

    SearchRequest does not forbid extra body fields, so an older server accepts
    `project_id`, ignores it, and returns TENANT-WIDE results with
    state="complete". An agent then attributes another project's runs to this
    one -- worse than any error, because it is confident and unmarked.

    The echo is the only available signal, so its absence is treated as
    unsupported. A false refusal is loud and correctable; a false answer is not.
    """
    app.search_response = _search_response(
        exact=[
            {
                "entity_type": "experiment",
                "id": "e-1",
                "name": "in",
                "slug": "in",
                "workspace_id": None,
                "project_id": "p-1",
                "experiment_id": None,
                "run_id": None,
                "score": 0.9,
            },
            {
                "entity_type": "experiment",
                "id": "e-2",
                "name": "out",
                "slug": "out",
                "workspace_id": None,
                "project_id": "p-OTHER",
                "experiment_id": None,
                "run_id": None,
                "score": 0.8,
            },
        ],
        semantic=[
            {
                "doc_id": "file:f-1",
                "title": "d",
                "snippet": "s",
                "score": 0.9,
                "source_system": "workspace",
                "source_url": None,
                "ref": {"kind": "file", "id": "f-1"},
            },
        ],
    )
    app.echoes_project_scope = False
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("q", project_id="p-1", collapse=None)

    # Out-of-project rows are removed rather than passed through: the whole
    # danger is tenant-wide results wearing a project scope.
    assert [r["id"] for r in out["data"]["results"]] == ["e-1"]
    # The semantic channel cannot be scoped client-side, so it is EMPTIED and
    # marked -- never passed through unscoped.
    assert out["data"]["channels"]["semantic"]["error"] == "project_scope_unsupported"
    assert out["completeness"]["state"] == "partial"
    assert "semantic_search" in out["completeness"]["missing"]

    # An echoing backend keeps its semantic channel, which is the point of the
    # backend change: scoping stops costing you semantic retrieval.
    app.echoes_project_scope = True
    ok = service.search_knowledge("q", project_id="p-1", collapse=None)
    assert ok["data"]["channels"]["semantic"]["error"] is None
    assert any(r["entity_type"] == "file" for r in ok["data"]["results"])


def test_backend_truncation_is_surfaced_not_swallowed(client, app):
    """A trimmed response must not read as a complete one.

    The backend drops chunks and whole results to fit its byte budget and says
    so. If the tool swallows that, an agent reads a short result set as "the lab
    has nothing else" -- the silent false negative this whole surface is built
    to avoid.
    """
    app.search_response = {**_search_response(), "truncated": True}
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("q")
    assert out["completeness"]["state"] == "partial"
    assert "truncated_by_response_budget" in out["completeness"]["missing"]

    # ...and an untruncated response stays complete, so the marker means something.
    app.search_response = _search_response()
    assert "completeness" not in service.search_knowledge("q")


def test_exact_run_hit_carries_slug_and_a_resource(client, app):
    """A run hit from the exact channel is addressable and echoes its petname.

    The backend gained a runs branch so a pasted `tunneling-sambar-254` resolves
    structurally instead of being left to the semantic gatherer, which does not
    do literal identifier lookup. The slug has to survive into the card: a
    run's `name` may be server-derived or since edited, so without it a correct
    hit looks unrelated to the query the caller typed."""
    app.search_response = _search_response(
        exact=[
            {
                "entity_type": "run",
                "id": "r-9",
                "name": "trace-sft-s0",
                "slug": "tunneling-sambar-254",
                "workspace_id": "ws-1",
                "project_id": "p-1",
                "experiment_id": "e-1",
                "run_id": "r-9",
                "score": 1.0,
            },
        ],
    )
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("tunneling-sambar-254", collapse=None)

    hit = out["data"]["results"][0]
    assert hit["entity_type"] == "run" and hit["id"] == "r-9"
    assert hit["card"]["slug"] == "tunneling-sambar-254"
    assert hit["resource"] == "research://runs/r-9/handoff"
    assert hit["why_matched"]["score"] == 1.0


def test_browse_gives_both_addresses_and_omits_an_absent_slug(app, client):
    """`slug` is the handle to prefer, `uuid` the stable key, each named for what
    it holds -- and a run's slug lives in `slug` while a project's lives in
    `slug`, which is a column-rename that has not happened yet and must not leak.

    An entity with no readable handle (a pre-0012 run) OMITS the key rather than
    sending null: an absent key says "there is none", a null one invites a caller
    to paste the string "None" into a ticket.
    """
    from probe.mcp.service import _annotate

    run = _annotate(
        {"id": "3c5f3695-bb4b-44c8-a59f-707b63f93999", "slug": "prophetic-manatee-987"},
        "run",
    )
    assert run["slug"] == "run:prophetic-manatee-987"
    assert run["uuid"] == "run:3c5f3695-bb4b-44c8-a59f-707b63f93999"

    project = _annotate(
        {"id": "11111111-1111-1111-1111-111111111111", "slug": "odyssey"}, "project"
    )
    assert project["slug"] == "project:odyssey"

    legacy = _annotate({"id": "22222222-2222-2222-2222-222222222222"}, "run")
    assert "slug" not in legacy
    assert legacy["uuid"] == "run:22222222-2222-2222-2222-222222222222"


def test_semantic_document_hit_without_ref_has_one_address(app, client):
    """The headline search contract: a plain document hit (no resolved ref)
    carries NO `id` — its one address is card.doc_id — and collapse passes it
    through untouched. A ref with kind but no id is the same case: treating
    it as an entity would emit "id": null, mint a resource URI containing the
    literal string None, and give every such row the identical
    ("experiment", None) collapse key, merging distinct results."""
    from probe.mcp.service import _collapse_experiments, _semantic_result

    plain = _semantic_result(
        {"doc_id": "d-1", "title": "t", "snippet": "s", "score": 0.9, "ref": None}
    )
    assert plain["entity_type"] == "document"
    assert "id" not in plain
    assert plain["card"]["doc_id"] == "d-1"
    assert plain["resource"] is None

    malformed = _semantic_result(
        {"doc_id": "d-2", "title": "t2", "score": 0.8, "ref": {"kind": "experiment"}}
    )
    assert malformed["entity_type"] == "document"
    assert "id" not in malformed
    assert malformed["resource"] is None

    # Distinct id-less rows survive collapse as distinct rows.
    collapsed = _collapse_experiments([plain, malformed])
    assert len(collapsed) == 2


def test_depth_two_browse_annotates_nested_children(app, client):
    """A depth-2 response must not mix labelled addresses at the top level
    with bare backend ids one level down — nested children get the same
    annotation, and their kinds join the envelope views map."""
    from probe.mcp.service import _supported_views

    app.browse_response = {
        **_browse_payload(),
        "projects": [
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "name": "bird-sql",
                "slug": "bird-sql",
                "created_at": "2026-07-01T00:00:00Z",
                "experiment_count": 1,
                "active_run_count": 0,
                "experiments": [
                    {
                        "id": "22222222-2222-2222-2222-222222222222",
                        "name": "e1",
                        "slug": "e1",
                        "project_id": "11111111-1111-1111-1111-111111111111",
                        "created_at": "2026-07-01T00:00:00Z",
                        "updated_at": "2026-07-01T00:00:00Z",
                        "run_count": 0,
                        "active_run_count": 0,
                        "runs": None,
                    }
                ],
            }
        ],
    }
    service = ResearchReadService(ResearchOSSource(client))
    data = service.browse_research(depth=2)["data"]
    [project] = data["projects"]
    [child] = project["experiments"]
    assert "id" not in child
    assert child["uuid"] == "experiment:22222222-2222-2222-2222-222222222222"
    assert child["slug"] == "experiment:e1"
    # Null keys dropped on children too ("runs": None above)...
    assert "runs" not in child
    # ...but FALSY values are values: a zero count is an answer, not absence.
    assert child["run_count"] == 0
    assert child["active_run_count"] == 0
    assert data["available_views"]["experiment"] == _supported_views("experiment")


def test_annotate_keeps_falsy_but_present_values():
    """`v is not None` must never decay to truthiness: zero counts and
    expanded-empty lists are answers, and hiding them would make an idle
    project indistinguishable from an unexpanded one."""
    from probe.mcp.service import _annotate

    out = _annotate(
        {
            "id": "33333333-3333-3333-3333-333333333333",
            "run_count": 0,
            "active_run_count": 0,
            "experiments": [],
            "slug": None,
        },
        "project",
    )
    assert out["run_count"] == 0
    assert out["active_run_count"] == 0
    assert out["experiments"] == []  # expanded-empty, distinct from omitted-null
    assert "slug" not in out and "id" not in out


def test_browse_projects_the_subprojects_level_and_cursors(app, client):
    """0148: the explicit level list is exactly what makes an unlisted level
    vanish silently — the inline comment says so; this test makes it hold.
    The per-level `cursors` pass through verbatim, and the tool params reach
    the wire so an agent can actually SPEND cursors.subprojects."""
    app.browse_response = {
        "projects": None,
        "experiments": [],
        "runs": None,
        "subprojects": [
            {
                "id": "22222222-2222-2222-2222-222222222222",
                "name": "o3-binder-review",
                "slug": "o3-binder-review",
                "workspace_id": None,
                "created_at": "2026-08-01T00:00:00Z",
                "experiment_count": 0,
                "active_run_count": 0,
                "kind": "survey",
                "parent_project_id": "11111111-1111-1111-1111-111111111111",
                "subproject_count": 0,
            }
        ],
        "cursor": None,
        "cursors": {"subprojects": "tok-subprojects", "runs": None},
        "depth": 1,
        "limit": 50,
        "truncated": False,
    }
    service = ResearchReadService(ResearchOSSource(client))
    envelope = service.browse_research(
        scope="project:11111111-1111-1111-1111-111111111111",
        subprojects_cursor="tok-prev",
    )

    [node] = envelope["data"]["subprojects"]
    assert node["uuid"] == "project:22222222-2222-2222-2222-222222222222"
    assert node["kind"] == "survey"
    assert envelope["data"]["cursors"]["subprojects"] == "tok-subprojects"
    # The level cursor reached the wire, not just the docstring.
    assert dict(app.browse_requests[-1])["subprojects_cursor"] == "tok-prev"


def test_search_names_a_lost_engine_channel(client, app):
    """A semantic response that SUCCEEDED but lost a retrieval channel says so.

    The 2026-08-25 kb incident: a failover left the BM25 index unusable, and
    for forty minutes every search answered `state: "complete"` while missing
    every lexical match. The engine recorded the loss the whole time; nothing
    carried it to the agent. Thinned results that look complete are worse than
    an error, because nothing prompts a re-query."""
    app.search_response = _search_response(
        semantic=[
            {
                "entity_type": "experiment",
                "id": "e-1",
                "title": "grpo-r1",
                "snippet": "...",
                "doc_id": "custom_ingest:probe:experiments:experiment:e-1",
                "score": 0.9,
            },
        ],
        semantic_lost_channels=["bm25"],
    )
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("grpo", collapse=None)

    assert out["data"]["channels"]["semantic"]["lost_channels"] == ["bm25"]
    # Results came back, so this is NOT semantic_search (whole channel dead) --
    # it is the quieter marker that says what you are holding is incomplete.
    assert out["completeness"]["missing"] == ["semantic_channel_degraded"]
    assert out["completeness"]["state"] == "partial"
    assert out["data"]["channels"]["semantic"]["error"] is None


def test_search_stays_clean_when_no_channel_was_lost(client, app):
    """A healthy search must not grow a new key or a new marker.

    The block is emitted only when something was actually lost: an always-on
    empty list would train readers to skip the field, which is how the signal
    stops being read before it is ever needed."""
    app.search_response = _search_response(
        semantic=[
            {
                "entity_type": "experiment",
                "id": "e-1",
                "title": "grpo-r1",
                "snippet": "...",
                "doc_id": "custom_ingest:probe:experiments:experiment:e-1",
                "score": 0.9,
            },
        ],
    )
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("grpo", collapse=None)

    assert "lost_channels" not in out["data"]["channels"]["semantic"]
    assert "completeness" not in out


def test_search_tolerates_a_malformed_lost_channels_value(client, app):
    """A malformed body degrades to "nothing lost", never an exception.

    Same discipline as every other field `_section` normalizes: a broken proxy
    or an older server must yield a usable answer, not a traceback."""
    app.search_response = _search_response(semantic=[])
    app.search_response["semantic"]["lost_channels"] = "bm25"  # a string, not a list
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("grpo", collapse=None)

    assert "lost_channels" not in out["data"]["channels"]["semantic"]
    assert "semantic_channel_degraded" not in out.get("completeness", {}).get("missing", [])


def test_every_schema_forbids_undeclared_arguments(client) -> None:
    """pydantic's default DROPS an extra argument, so an invented parameter
    returns a confident answer to a different question -- a lazy-loading agent
    that never read browse's schema passed `query`, got an unfiltered listing,
    and reported absence. Strict clients reject on this flag; call_tool
    enforces it for everyone else."""
    for name, schema in _tool_schemas(client).items():
        assert schema.get("additionalProperties") is False, name


def test_an_unknown_argument_is_refused_with_the_declared_parameters(client) -> None:
    import asyncio as _asyncio

    server = create_server(ResearchReadService(ResearchOSSource(client)))

    async def call() -> str:
        try:
            await server.call_tool("browse", {"query": "anything"})
        except Exception as exc:
            return str(exc)
        return ""

    message = _asyncio.run(call())
    assert "unknown argument" in message and "query" in message
    assert "ref" in message and "token_budget" in message


def _semantic_rows(n: int, *, content: str = "x" * 400, why: str | None = None) -> list[dict]:
    return [
        {
            "doc_id": f"custom_ingest:t:experiments:run:{i:040d}",
            "title": f"doc {i}",
            "snippet": content,
            "score": 0.9 - i / 100,
            "source_system": "custom_ingest",
            "source_url": f"https://example.invalid/d/{i}",
            "ref": None,
            "chunks": [{"content": content, "score": 0.9, "why_relevant": why}] if why else [],
        }
        for i in range(n)
    ]


def test_top_k_is_a_total_when_the_exact_channel_is_empty(client, app):
    """THE regression: `top_k=8` used to show 4 because the budget was split.

    Four semantic and four exact were fetched, and the exact channel answers
    nothing on most searches -- so the default search returned half of what the
    caller asked for and said nothing about it.
    """
    app.search_response = _search_response(exact=[], semantic=_semantic_rows(8))
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("q", top_k=8, collapse=None)
    assert app.search_requests[-1]["top_k"] == 8
    assert len(out["data"]["results"]) == 8


def test_a_response_that_fits_keeps_its_cursor_and_says_nothing_about_budget(client, app):
    app.search_response = _search_response(exact=[], semantic=_semantic_rows(3))
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("q", top_k=8, collapse=None, token_budget=4000)
    assert len(out["data"]["results"]) == 3
    assert MissingMarker.RESULTS_BEYOND_BUDGET not in out.get("completeness", {}).get("missing", [])


def test_cards_are_whole_or_absent_never_shrunk(client, app):
    """The budget decides HOW MANY cards arrive, never how much of one."""
    app.search_response = _search_response(exact=[], semantic=_semantic_rows(20))
    service = ResearchReadService(ResearchOSSource(client))
    full = service.search_knowledge("q", top_k=20, collapse=None, token_budget=8000)
    tight = service.search_knowledge("q", top_k=20, collapse=None, token_budget=512)
    assert len(tight["data"]["results"]) < len(full["data"]["results"])
    # every card that DID arrive is byte-identical to the one the roomy call sent
    for lean, rich in zip(tight["data"]["results"], full["data"]["results"], strict=False):
        assert lean == rich


def test_a_cut_response_withholds_the_cursor_and_names_the_budget_that_fits(client, app):
    app.search_response = _search_response(exact=[], semantic=_semantic_rows(20))
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("q", top_k=20, collapse=None, token_budget=512)
    assert "next_cursor" not in out
    assert MissingMarker.RESULTS_BEYOND_BUDGET in out["completeness"]["missing"]
    note = out["data"]["budget"]
    assert note["results_available"] == 20
    # The number to ask for next time -- legal, and enough for everything found.
    assert 512 < note["fits_all_at_token_budget"] <= 8000


def test_asking_for_the_named_budget_actually_returns_everything(client, app):
    """The hint is not decorative: passing it back must deliver all 20."""
    app.search_response = _search_response(exact=[], semantic=_semantic_rows(20))
    service = ResearchReadService(ResearchOSSource(client))
    first = service.search_knowledge("q", top_k=20, collapse=None, token_budget=512)
    again = service.search_knowledge(
        "q",
        top_k=20,
        collapse=None,
        token_budget=first["data"]["budget"]["fits_all_at_token_budget"],
    )
    assert len(again["data"]["results"]) == 20
    assert MissingMarker.RESULTS_BEYOND_BUDGET not in again.get("completeness", {}).get("missing", [])


def test_one_card_larger_than_the_budget_is_refused_in_words_not_in_halves(client, app):
    """A half card is not a result, so none is sent and the number is named."""
    app.search_response = _search_response(exact=[], semantic=_semantic_rows(3, content="y" * 9000))
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("q", top_k=3, collapse=None, token_budget=512)
    assert out["data"]["results"] == []
    assert MissingMarker.FIRST_RESULT_EXCEEDS_BUDGET in out["completeness"]["missing"]
    note = out["data"]["budget"]
    assert note["first_result_tokens"] > 512
    assert "min_token_budget" in note or note["read_instead"] == "entity"


def test_the_engine_reason_rides_on_the_provenance_it_belongs_to(client, app):
    app.search_response = _search_response(
        exact=[], semantic=_semantic_rows(1, why="Corrects the MPP conclusion the query asks about")
    )
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("q", top_k=4, collapse=None)
    why = out["data"]["results"][0]["why_matched"]
    assert why["reason"] == "Corrects the MPP conclusion the query asks about"
    assert "why" not in out["data"]["results"][0], "one question, asked once"


def test_a_hit_with_no_engine_reason_omits_the_key(client, app):
    app.search_response = _search_response(exact=[], semantic=_semantic_rows(1))
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("q", top_k=4, collapse=None)
    assert "reason" not in out["data"]["results"][0]["why_matched"]


def test_a_long_engine_reason_is_capped(client, app):
    app.search_response = _search_response(exact=[], semantic=_semantic_rows(1, why="z" * 900))
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("q", top_k=4, collapse=None)
    assert len(out["data"]["results"][0]["why_matched"]["reason"]) == 200


def test_an_out_of_range_budget_is_clamped_not_a_traceback(client, app) -> None:
    """The tool surface constrains this; a direct Python caller does not."""
    app.search_response = _search_response(exact=[], semantic=_semantic_rows(3))
    service = ResearchReadService(ResearchOSSource(client))
    for budget in (1, 10**9):
        out = service.search_knowledge("q", top_k=3, collapse=None, token_budget=budget)
        assert isinstance(out["data"]["results"], list)


def test_search_says_when_the_ANSWER_is_degraded_not_just_a_channel(client, app):
    """Every retrieval channel alive, and the answer still worse than a healthy
    run's: the gatherer timed out, or its emit was truncated, or the harness
    fell back to the raw pre-fan-out pool.

    The engine has reported this as `degraded` + `degraded_reason` the whole
    time and research-os forwards both; this boundary dropped them, so a
    fallback answer arrived at a coding agent looking exactly like a good one.
    That is the most dangerous of the three degradations precisely because
    nothing about the response looks wrong."""
    app.search_response = _search_response(
        semantic=[
            {
                "entity_type": "experiment",
                "id": "e-1",
                "title": "grpo-r1",
                "snippet": "...",
                "doc_id": "custom_ingest:probe:experiments:experiment:e-1",
                "score": 0.9,
            },
        ],
        semantic_degraded_reason="loop_timeout",
        semantic_confidence={"EXTRACTED": 0, "INFERRED": 4, "AMBIGUOUS": 1},
    )
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("grpo", collapse=None)

    assert "semantic_answer_degraded" in out["completeness"]["missing"]
    assert out["completeness"]["state"] == "partial"
    # WHY, not just THAT: loop_timeout and schema_violation want different
    # reactions, and a marker alone cannot tell them apart.
    assert out["data"]["channels"]["semantic"]["degraded_reason"] == "loop_timeout"
    assert out["data"]["channels"]["semantic"]["confidence_breakdown"] == {
        "EXTRACTED": 0,
        "INFERRED": 4,
        "AMBIGUOUS": 1,
    }
    # A dead channel is a DIFFERENT fact; this answer lost none.
    assert "semantic_channel_degraded" not in out["completeness"]["missing"]
    assert "lost_channels" not in out["data"]["channels"]["semantic"]


def test_a_healthy_search_grows_no_degraded_keys(client, app):
    """Emitted only when true: an always-present `degraded: false` trains
    readers to skip the field, which is how a signal stops being read before
    it is ever needed."""
    app.search_response = _search_response(
        semantic=[
            {
                "entity_type": "experiment",
                "id": "e-1",
                "title": "grpo-r1",
                "snippet": "...",
                "doc_id": "custom_ingest:probe:experiments:experiment:e-1",
                "score": 0.9,
            },
        ],
    )
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("grpo", collapse=None)

    semantic = out["data"]["channels"]["semantic"]
    assert "degraded_reason" not in semantic and "confidence_breakdown" not in semantic
    assert "completeness" not in out


def test_a_malformed_degraded_flag_reads_as_healthy_never_raises(client, app):
    """Same discipline as every other field `_section` normalizes: a broken
    proxy yields a usable answer, and the safe direction mid-rollout is
    "not degraded"."""
    app.search_response = _search_response(semantic=[])
    app.search_response["semantic"]["degraded"] = "yes"  # a string, not a bool
    app.search_response["semantic"]["confidence_breakdown"] = ["EXTRACTED"]  # a list
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("grpo", collapse=None)

    assert "semantic_answer_degraded" not in out.get("completeness", {}).get("missing", [])
    assert "confidence_breakdown" not in out["data"]["channels"]["semantic"]


def test_a_card_carries_when_the_text_was_written_and_which_corpus(client, app):
    """An agent weighing a six-month-old design note against yesterday's note
    needs the clock, and telling a team note apart from a transcript should not
    mean parsing a doc id. Both were on the wire and dropped here."""
    app.search_response = _search_response(
        semantic=[
            {
                "entity_type": "experiment",
                "id": "e-1",
                "title": "grpo-r1",
                "snippet": "...",
                "doc_id": "custom_ingest:probe:experiments:experiment:e-1",
                "score": 0.9,
                "updated_at": "2026-03-01T12:00:00+00:00",
                "corpus": "experiments",
            },
        ],
    )
    service = ResearchReadService(ResearchOSSource(client))
    out = service.search_knowledge("grpo", collapse=None)

    card = out["data"]["results"][0]["card"]
    assert card["updated_at"] == "2026-03-01T12:00:00+00:00"
    assert card["corpus"] == "experiments"


def _experiment_row(eid: str) -> dict:
    return {
        "entity_type": "experiment", "id": eid, "name": "adam sweep", "slug": f"adam-{eid}",
        "workspace_id": "ws-1", "project_id": "p-1", "experiment_id": None, "run_id": None,
        "score": 0.9,
    }


_FILE_HIT = {
    "doc_id": "file:f-1", "title": "sweep notes", "snippet": "adam beta2 ...", "score": 0.83,
    "source_system": "workspace", "source_url": None, "ref": {"kind": "file", "id": "f-1"},
}


def test_search_offers_views_only_for_kinds_entity_can_open(client, app):
    """`available_views` on a search response names the kinds an agent can hand
    to `entity`. A `file` hit CARRIES an `id` (its engine ref had a kind) and
    entity still has no route for it, so the sheet keys the open-or-terminal
    rule on this list rather than on `id` -- and the list must never offer
    `file`. Keyed by kind, once, sorted, deduped across rows of one kind."""
    app.search_response = _search_response(
        exact=[_experiment_row("e-1"), _experiment_row("e-2")], semantic=[_FILE_HIT]
    )
    out = ResearchReadService(ResearchOSSource(client)).search_knowledge("adam sweep", collapse=None)
    results = out["data"]["results"]
    assert any(r["entity_type"] == "file" and r.get("id") == "f-1" for r in results)
    offered = out["data"]["available_views"]
    assert list(offered) == ["experiment"]
    assert offered["experiment"] == _supported_views("experiment")
    for kind in offered:
        assert _supported_views(kind), kind

    # Only terminal hits: no key at all, not an empty dict.
    app.search_response = _search_response(exact=[], semantic=[_FILE_HIT])
    out = ResearchReadService(ResearchOSSource(client)).search_knowledge("adam sweep", collapse=None)
    assert "available_views" not in out["data"]

    # The sheet teaches exactly that rule.
    docs = " ".join(_tool_docs(client)["search_knowledge"][:2048].split())
    assert "listed in the response's `available_views`" in docs
    assert "every other hit (`document`, `file`) is TERMINAL" in docs


@pytest.mark.parametrize(
    "prior, expected",
    [
        # A healthy search's compact envelope carries no completeness at all.
        (None, [MissingMarker.FIRST_RESULT_EXCEEDS_BUDGET]),
        # A degraded one keeps its marker beside the refusal's.
        (
            {"state": "partial", "missing": [MissingMarker.SEMANTIC_CHANNEL_DEGRADED]},
            sorted([MissingMarker.FIRST_RESULT_EXCEEDS_BUDGET, MissingMarker.SEMANTIC_CHANNEL_DEGRADED]),
        ),
    ],
)
def test_a_refusal_is_partial_and_keeps_the_markers_the_search_already_had(prior, expected):
    from probe.mcp.budget import Budget
    from probe.mcp.service import _fit_whole_results

    def build(results, note):
        envelope = {"data": {"results": results, **(note or {})}}
        if prior is not None:
            envelope["completeness"] = dict(prior)
        return envelope

    out = _fit_whole_results([{"text": "x " * 20000}], build, Budget(512))
    assert out["data"]["results"] == []
    assert out["completeness"] == {"state": "partial", "missing": expected}
