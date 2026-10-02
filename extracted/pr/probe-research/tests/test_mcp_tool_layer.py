"""Round-trip through the REAL MCP tool layer, not the service underneath it.

Every other test calls `ResearchReadService.get_entity(...)` directly. That skips
FastMCP entirely — and FastMCP is not a passthrough. Its `pre_parse_json` runs
json.loads on every string argument and, when the result is not a scalar, REPLACES
the argument with the parsed object. So a `json.dumps({...})` cursor arrives at the
tool as a dict and is rejected against `cursor: str | None`.

That is how research_search shipped paginating perfectly in-process and 422-ing over
the wire, for as long as it has existed. The service-level tests could never see it;
only a call through `mcp.call_tool` can. The cursor is the contract an agent actually
has to use, so this file exercises the layer the agent talks to.
"""

from __future__ import annotations

import asyncio
import hashlib
import json

import pytest

from probe.mcp.budget import Budget
from probe.mcp.server import create_server
from probe.mcp.service import ResearchReadService, _pack_cursor
from probe.mcp.source import ResearchOSSource


def _server(client):
    return create_server(ResearchReadService(ResearchOSSource(client)))


def _call(server, tool: str, args: dict):
    """Invoke a tool the way a real MCP client does, and unwrap the payload."""
    result = asyncio.run(server.call_tool(tool, args))
    # FastMCP returns (content, structured) in this version; older ones return content.
    payload = result[1] if isinstance(result, tuple) else result
    if isinstance(payload, dict) and "result" in payload:
        return payload["result"]
    if isinstance(payload, list):  # content blocks
        return json.loads(payload[0].text)
    return payload


def _run_with_spans(client, app, count: int = 40):
    _proj = client.create_project("folding", kind="general")
    client.create_experiment("e", "e", question="h", project_id=_proj["id"])
    run = client.run(project="folding", experiment="e", name="r")
    app.spans[run.id] = [
        {
            "id": f"span-{i}",
            "run_id": run.id,
            "span_type": "rollout",
            "name": f"n-{i}",
            "step_index": i,
            "status": "ok",
            "parent_span_id": None,
            "attributes": {"reward": i * 0.1},
            "summary": {},
            "started_at": "2026-07-16T00:00:00Z",
            "ended_at": "2026-07-16T00:00:01Z",
            "customer_id": "lab-42",
            "created_at": "2026-07-16T00:00:00Z",
        }
        for i in range(count)
    ]
    return run.id


def test_get_entity_cursor_round_trips_through_the_tool_layer(client, app):
    """The bug this file exists for: a JSON-object cursor is coerced to a dict by
    FastMCP before validation, so passing back a next_cursor the tool JUST issued
    fails with "Input should be a valid string". Caught only by smoke-testing the
    hosted MCP — 264 service-level tests were green."""
    rid = _run_with_spans(client, app)
    server = _server(client)

    page1 = _call(
        server, "entity", {"refs": [f"run:{rid}"], "view": "trajectory", "token_budget": 512}
    )
    cursor = page1["next_cursor"]
    assert cursor is not None and isinstance(cursor, str)

    page2 = _call(
        server,
        "entity",
        {"refs": [f"run:{rid}"], "view": "trajectory", "token_budget": 512, "cursor": cursor},
    )
    # At the minimum budget, a source span page may itself need fragments.
    # The second tool call must continue its exact character position, not
    # restart the document or prematurely advance the source's span cursor.
    first, second = page1["data"], page2["data"]
    assert first["format"] == second["format"] == "json_fragment"
    assert first["offset"] == 0
    assert second["text"], "the cursor the tool just issued returned an empty fragment"
    assert second["offset"] == len(first["text"])
    assert first["sha256"] == second["sha256"]
    assert Budget(512).fits(page1) and Budget(512).fits(page2)


def test_a_cursor_is_opaque_and_survives_fastmcp_pre_parsing(client, app):
    """The token must not be JSON: FastMCP replaces any string arg that json.loads
    to a non-scalar with the parsed object. This pins WHY the cursor is packed —
    revert _pack_cursor to json.dumps and this fails."""
    from mcp.server.fastmcp.utilities.func_metadata import func_metadata

    def research_get(ref: str, cursor: str | None = None) -> dict: ...

    token = _pack_cursor({"offset": 2, "view": "trajectory"})
    with pytest.raises(json.JSONDecodeError):
        json.loads(token)

    survived = func_metadata(research_get).pre_parse_json({"refs": ["run:x"], "cursor": token})
    assert isinstance(survived["cursor"], str), "FastMCP coerced the cursor away from str"


def test_full_trajectory_walk_through_the_tool_layer(client, app):
    """End to end as an agent drives it: every span, no skips, no duplicates."""
    rid = _run_with_spans(client, app, count=40)
    server = _server(client)

    seen: list[str] = []
    fragment_text, fingerprint = "", None
    cursor, pages = None, 0
    while pages < 500:
        args = {"refs": [f"run:{rid}"], "view": "trajectory", "token_budget": 512}
        if cursor:
            args["cursor"] = cursor
        page = _call(server, "entity", args)
        assert Budget(512).fits(page)
        data = page["data"]
        if data.get("format") == "json_fragment":
            assert data["offset"] == len(fragment_text)
            assert data["text"], "fragment cursor made no progress"
            fingerprint = fingerprint or data["sha256"]
            assert data["sha256"] == fingerprint
            fragment_text += data["text"]
            if not data["complete"]:
                assert page["completeness"]["state"] == "partial"
                assert "truncated_by_token_budget" in page["completeness"]["missing"]
            if data["complete"]:
                assert len(fragment_text) == data["total_chars"]
                assert hashlib.sha256(fragment_text.encode()).hexdigest() == fingerprint
                source_page = json.loads(fragment_text)
                seen.extend(s["id"] for s in source_page["data"]["spans"])
                fragment_text, fingerprint = "", None
        else:
            assert not fragment_text, "source advanced before its previous page was complete"
            seen.extend(s["id"] for s in data["spans"])
        cursor = page.get("next_cursor")
        pages += 1
        if not cursor:
            break

    assert pages > 1, "budget did not force pagination; the walk proves nothing"
    assert cursor is None, "trajectory continuation did not terminate"
    assert not fragment_text, "trajectory ended with an incomplete source page"
    assert seen == [f"span-{i}" for i in range(40)]
    assert "completeness" not in page


def test_search_knowledge_cursor_round_trips_through_the_tool_layer(client, app):
    """search_knowledge has the SAME defect surface — same json.dumps({...}) format,
    same coercion. It is not reachable from a service-level test."""
    _proj = client.create_project("folding", kind="general")
    client.create_experiment("dockq", "dockq", question="h", project_id=_proj["id"])
    client.run(project="folding", experiment="dockq", name="r")
    app.search_responses = [
        {
            "query": "q",
            "state": "ok",
            "exact": {
                "results": [{"entity_type": "experiment", "id": "e1", "name": "one"}],
                "cursor": "backend-exact-2",
                "error": None,
            },
            "semantic": {"results": [], "cursor": None, "error": None},
        },
        {
            "query": "q",
            "state": "ok",
            "exact": {
                "results": [{"entity_type": "experiment", "id": "e2", "name": "two"}],
                "cursor": None,
                "error": None,
            },
            "semantic": {"results": [], "cursor": None, "error": None},
        },
    ]
    server = _server(client)

    page1 = _call(server, "search_knowledge", {"query": "dockq", "top_k": 2})
    cursor = page1["next_cursor"]
    assert isinstance(cursor, str) and cursor

    page2 = _call(server, "search_knowledge", {"query": "dockq", "top_k": 2, "cursor": cursor})
    assert [r["id"] for r in page2["data"]["results"]] == ["e2"]
    # the packed token still carries the backend's own per-channel cursor
    assert app.search_requests[-1]["exact_cursor"] == "backend-exact-2"


def test_a_legacy_raw_json_cursor_is_still_honored(client, app):
    """Tokens minted before cursors were packed live in agent transcripts; refusing
    them would turn a stale cursor into an error instead of a page."""
    rid = _run_with_spans(client, app)
    legacy = json.dumps({"offset": 2, "view": "trajectory"}, sort_keys=True)
    service = ResearchReadService(ResearchOSSource(client))

    result = service.get_entity(f"run:{rid}", view="trajectory", cursor=legacy)
    assert [s["id"] for s in result["data"]["spans"]][:1] == ["span-2"]


def _search_response(*, applied, results, total_candidates, excluded=0, error=None):
    """A /v1/search body whose semantic section may or may not know the field."""
    semantic = {
        "results": results,
        "cursor": None,
        "error": error,
        "total_candidates": total_candidates,
        "active_runs_count": 0,
        "excluded_count": excluded,
    }
    if applied is not None:
        semantic["exclusion_applied"] = applied
    return {
        "exact": {
            "results": [],
            "cursor": None,
            "error": None,
            "total_candidates": 0,
            "active_runs_count": 0,
        },
        "semantic": semantic,
    }


def _markers(*, applied, results, total_candidates, exclude, excluded=0, error=None):
    from unittest.mock import MagicMock

    from probe.mcp.service import ResearchReadService

    source = MagicMock()
    source.search.return_value = _search_response(
        applied=applied,
        results=results,
        total_candidates=total_candidates,
        excluded=excluded,
        error=error,
    )
    service = ResearchReadService.__new__(ResearchReadService)
    service.source = source
    answer = service.search_knowledge("q", exclude_session=exclude)
    return [str(marker) for marker in answer.get("completeness", {}).get("missing", [])]


def test_a_backend_that_ignored_the_exclusion_is_reported_not_assumed() -> None:
    """`SearchRequest` permits extra body fields, so an older server accepts
    `exclude_agent_session`, ignores it, and answers 200 with the caller's own
    session still in the results. Absent echo is the only way to tell."""
    assert _markers(applied=None, results=[], total_candidates=5, exclude="s1") == [
        "self_exclusion_unsupported"
    ]


def test_an_applied_exclusion_is_never_reported_as_unsupported() -> None:
    """Regression: the flag is dropped unless `_section` carries it through, and
    a dropped flag made EVERY excluded search claim the server could not do it
    -- a false degradation on the healthy path."""
    markers = _markers(
        applied=True,
        results=[{"doc_id": "d", "snippet": "", "score": 1.0}],
        total_candidates=5,
        exclude="s1",
    )
    assert "self_exclusion_unsupported" not in markers


def test_everything_being_the_callers_own_session_is_a_stop_not_a_degradation() -> None:
    """The corpus answered and every surviving row was the caller's own
    conversation. Rewording cannot change that, so it must not read as the kind
    of partial answer a retry might improve."""
    assert _markers(
        applied=True, results=[], total_candidates=5, excluded=4, exclude="s1"
    ) == ["all_results_were_own_session"]


def test_a_genuinely_empty_corpus_is_an_ordinary_empty_answer() -> None:
    """Claiming self-exclusion emptied a result set it never touched would send
    an agent chasing a filter that did nothing."""
    assert _markers(applied=True, results=[], total_candidates=0, exclude="s1") == []


def test_a_scope_lens_emptying_the_page_is_not_blamed_on_self_exclusion() -> None:
    """total_candidates counts hits BEFORE the workspace/project lenses, so it
    cannot tell "your own session emptied this" from "your project filter did".
    Telling an agent to STOP when the right advice is "widen the scope" is the
    opposite of the guidance it needs. Gated on excluded_count instead."""
    assert (
        _markers(
            applied=True, results=[], total_candidates=40, excluded=0, exclude="s1"
        )
        == []
    )


def test_a_channel_that_could_not_answer_is_not_reported_as_an_old_backend() -> None:
    """Early returns in semantic_channel never reach the filter, so they used to
    carry exclusion_applied=false and be misread as "this deployment predates
    the field, your own session is still in these results" -- on a timeout,
    where there are no results at all."""
    markers = _markers(
        applied=True,
        results=[],
        total_candidates=0,
        exclude="s1",
        error="engine_timeout",
    )
    assert "self_exclusion_unsupported" not in markers
    assert "semantic_search" in markers
