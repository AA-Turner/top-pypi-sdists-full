"""Research-paper MCP reads keep their wire, failure and resource contracts.

General web search and page fetching are absent from the shipped tool registry.
The remaining literature tool must still distinguish an empty answer from an
unavailable provider, preserve open-web provenance, and honor response budgets.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest
from mcp.server.fastmcp.exceptions import ToolError

from probe.mcp.contract import Capability, EnvelopeState, MissingMarker
from probe.mcp.server import create_server
from probe.mcp.service import ResearchReadService
from probe.sdk import errors

_OPEN_WEB = "open-web"


class _StubSource:
    def __init__(self, payload: object = None, raises: Exception | None = None):
        self._payload = payload if payload is not None else {}
        self._raises = raises
        self.calls: list[dict] = []

    def identity(self) -> dict:
        return {"customer_id": "lab-42", "email": "researcher@lab.test"}

    def capabilities(self) -> dict:
        return {}

    def find_papers(self, **kwargs: object) -> object:
        self.calls.append(kwargs)
        if self._raises is not None:
            raise self._raises
        return self._payload


def _service(payload: object = None, raises: Exception | None = None) -> ResearchReadService:
    return ResearchReadService(_StubSource(payload, raises))


def _call(server, tool: str, args: dict):
    result = asyncio.run(server.call_tool(tool, args))
    payload = result[1] if isinstance(result, tuple) else result
    if isinstance(payload, dict) and "result" in payload:
        return payload["result"]
    if isinstance(payload, list):
        return json.loads(payload[0].text)
    return payload


def _e2e(client):
    from probe.mcp.source import ResearchOSSource

    return create_server(ResearchReadService(ResearchOSSource(client)))


@pytest.mark.parametrize(
    "tool,args",
    [
        ("search_web", {"query": "q"}),
        ("read_page", {"url": "https://example.test/a"}),
    ],
)
def test_general_web_tools_are_not_registered_or_dispatchable(client, app, tool, args):
    server = _e2e(client)
    assert tool not in {entry.name for entry in asyncio.run(server.list_tools())}
    with pytest.raises(ToolError, match=f"Unknown tool: {tool}"):
        _call(server, tool, args)
    assert app.web_requests == []


@pytest.mark.parametrize("mode", ["search", "read", "similar"])
def test_provider_matched_nothing_is_no_match_not_partial(mode):
    out = _service({"mode": mode, "state": "empty", "results": []}).find_papers(mode)
    assert out["completeness"]["state"] == EnvelopeState.NO_MATCH
    assert out["completeness"]["missing"] == []
    assert out["data"]["results"] == []
    assert out["data"]["provenance"] == _OPEN_WEB


@pytest.mark.parametrize(
    "status,detail",
    [
        (503, "paper search is not configured on this deployment"),
        (503, "this deployment's search allowance is used up; retrying will not help"),
        (502, "the paper search provider refused our key"),
        (504, "timed out talking to the paper search provider"),
        (404, "Not Found"),
    ],
)
@pytest.mark.parametrize("mode", ["search", "read", "similar"])
def test_an_unavailable_provider_omits_results_entirely(status, detail, mode):
    # A missing route, including a paper read, is a deployment outage. An empty
    # result set would incorrectly tell the caller that the query matched nothing.
    out = _service(raises=errors.error_for(status, detail)).find_papers(mode)
    assert out["completeness"]["state"] == EnvelopeState.PARTIAL
    assert out["completeness"]["missing"] == [MissingMarker.WEB_SEARCH]
    assert "results" not in out["data"]
    assert out["data"]["reason"] == detail
    assert out["data"]["provenance"] == _OPEN_WEB


@pytest.mark.parametrize("mode", ["search", "read", "similar"])
def test_a_statusless_transport_failure_is_an_outage(mode):
    boom = errors.TransportError("POST /v1/web/papers: ReadTimeout('')")
    assert boom.status is None
    out = _service(raises=boom).find_papers(mode)
    assert out["completeness"]["state"] == EnvelopeState.PARTIAL
    assert out["completeness"]["missing"] == [MissingMarker.WEB_SEARCH]
    assert "results" not in out["data"]
    assert out["data"]["provenance"] == _OPEN_WEB


@pytest.mark.parametrize("status", [400, 401, 403, 422, 429, 500])
@pytest.mark.parametrize("mode", ["search", "read", "similar"])
def test_errors_outside_the_provider_outage_set_still_raise(status, mode):
    # In particular, argument refusals must never turn into a retryable outage.
    with pytest.raises(errors.RosError):
        _service(raises=errors.error_for(status, "nope")).find_papers(mode)


def test_the_gateway_outage_set_is_exactly_the_three_gateway_statuses():
    assert ResearchReadService._WEB_DOOR_DOWN == frozenset({502, 503, 504})


def test_find_papers_forwards_its_mode_and_omits_empty_passages():
    svc = _service({"mode": "similar", "state": "ok", "results": [{"paper_id": "p"}]})
    out = svc.find_papers("similar", query="failure modes", paper_id="arxiv:2401.1", expand="citers")
    sent = svc.source.calls[0]  # type: ignore[attr-defined]
    assert (sent["mode"], sent["query"], sent["expand"], sent["paper_id"]) == (
        "similar", "failure modes", "citers", "arxiv:2401.1"
    )
    assert out["data"]["mode"] == "similar"
    assert "passages" not in out["data"]


def test_find_papers_returns_passages_when_reading_one_paper():
    out = _service(
        {
            "mode": "read",
            "state": "ok",
            "results": [{"paper_id": "p", "title": "T"}],
            "passages": [{"text": "the claim in context", "section": "4.2"}],
        }
    ).find_papers("read", paper_id="p", query="does it collapse")
    assert out["data"]["passages"][0]["section"] == "4.2"
    assert out["data"]["provenance"] == _OPEN_WEB
    assert "completeness" not in out


@pytest.mark.parametrize(
    "argument,values",
    [
        ("mode", {"search", "read", "similar"}),
        ("expand", {"similar", "citers", "references"}),
    ],
)
def test_closed_vocabularies_reach_the_caller_as_schema(argument, values):
    tools = asyncio.run(create_server(object()).list_tools())
    schema = next(t for t in tools if t.name == "find_papers").inputSchema
    prop = schema["properties"][argument]
    refs = [
        branch["$ref"]
        for branch in ([prop] + prop.get("anyOf", []))
        if isinstance(branch, dict) and "$ref" in branch
    ]
    assert len(refs) == 1
    target = schema["$defs"][refs[0].rsplit("/", 1)[-1]]
    assert set(target["enum"]) == values


@pytest.mark.parametrize(
    "args,expected",
    [
        ({"mode": "browse", "query": "q"}, "search"),
        ({"mode": "similar", "paper_id": "p", "query": "q", "expand": "neighbors"}, "citers"),
        ({"mode": "search", "query": "q", "limit": 51}, "50"),
        ({"mode": "search", "query": "q" * 501}, "500"),
    ],
)
def test_invalid_arguments_are_refused_before_the_backend(args, expected):
    service = _service()
    with pytest.raises(ToolError) as excinfo:
        _call(create_server(service), "find_papers", args)
    assert expected in str(excinfo.value)
    assert service.source.calls == []  # type: ignore[attr-defined]


def test_the_provider_capability_is_still_declared_for_paper_search():
    from probe.mcp.source import ResearchOSSource

    reported = ResearchOSSource.capabilities(object())
    assert reported[Capability.WEB_SEARCH] is True


@pytest.mark.parametrize("state", [None, "", "weird", "error", 0])
def test_an_unrecognised_provider_state_is_never_reported_complete(state):
    payload = {"mode": "search", "results": []}
    if state is not None:
        payload["state"] = state
    out = _service(payload).find_papers("search", query="q")
    assert out["completeness"]["state"] == EnvelopeState.PARTIAL


@pytest.mark.parametrize("field", ["results", "passages"])
@pytest.mark.parametrize("raw", [[{"title": "a"}, "junk", None, 42], "not-a-list", {"a": 1}, None])
def test_malformed_rows_cannot_reach_the_agent(field, raw):
    out = _service({"mode": "read", "state": "ok", field: raw}).find_papers("read", paper_id="p")
    assert all(isinstance(row, dict) for row in out["data"].get(field, []))


@pytest.mark.parametrize("payload", [["not", "a", "dict"], "garbage", 42])
def test_a_payload_that_is_not_a_dict_at_all_is_survivable(payload):
    out = _service(payload).find_papers("search", query="q")
    assert out["data"]["provenance"] == _OPEN_WEB
    assert out["completeness"]["state"] == EnvelopeState.PARTIAL


@pytest.mark.parametrize("field,text_field", [("results", "abstract"), ("passages", "text")])
def test_the_response_ceiling_covers_abstracts_and_passages(field, text_field):
    out = _service(
        {
            "mode": "read",
            "state": "ok",
            field: [{"paper_id": str(i), text_field: "a" * 30_000} for i in range(10)],
        }
    ).find_papers("read", paper_id="p")
    rows = out["data"][field]
    assert sum(len(row[text_field]) for row in rows) <= ResearchReadService._WEB_MAX_TEXT_CHARS
    assert len(rows) == 10, "matched paper identities must survive a text budget"
    assert out["completeness"]["state"] == EnvelopeState.PARTIAL
    assert out["completeness"]["missing"] == [MissingMarker.TRUNCATED_BY_RESPONSE_BUDGET]


def test_a_capped_abstract_is_flagged_and_later_papers_remain_visible():
    out = _service(
        {
            "mode": "search",
            "state": "ok",
            "results": [
                {"paper_id": "a", "abstract": "s" * 10},
                {"paper_id": "b", "abstract": "z" * 150_000},
                {"paper_id": "c", "abstract": "fits nowhere"},
            ],
        }
    ).find_papers("search", query="q")
    first, capped, starved = out["data"]["results"]
    assert first["abstract"] == "s" * 10 and "truncated" not in first
    assert capped["truncated"] is True and len(capped["abstract"]) < 150_000
    assert starved["paper_id"] == "c"
    assert starved["abstract"] == "" and starved["truncated"] is True


def test_no_match_outranks_truncation():
    out = _service(
        {"mode": "search", "state": "empty", "results": [{"abstract": "a" * 150_000}]}
    ).find_papers("search", query="q")
    assert out["completeness"]["state"] == EnvelopeState.NO_MATCH
    assert out["completeness"]["missing"] == [MissingMarker.TRUNCATED_BY_RESPONSE_BUDGET]


def test_an_unbounded_upstream_error_body_does_not_land_in_the_agents_context():
    page = "<html>" + ("nginx upstream request-id abc " * 200) + "</html>"
    out = _service(raises=errors.error_for(503, page)).find_papers("search", query="q")
    reason = out["data"]["reason"]
    assert len(reason) <= ResearchReadService._WEB_REASON_CHARS + 3
    assert reason.endswith("...")


@pytest.mark.parametrize("name", ["PaperMode", "PaperExpansion", "WebState"])
def test_the_mirrored_vocabulary_matches_the_backend_contract(name):
    from probe.mcp import contract

    schema = json.loads(
        (Path(__file__).resolve().parent.parent / "schema" / "openapi.json").read_text()
    )
    declared = schema["components"]["schemas"][name]["enum"]
    assert [member.value for member in getattr(contract, name)] == declared


@pytest.mark.parametrize(
    "args",
    [
        {
            "mode": "search", "query": "failure modes", "authors": "Researcher",
            "categories": "cs.LG", "published_from": "2025-01-01",
            "published_to": "2026-01-01", "limit": 3,
        },
        {"mode": "read", "paper_id": "arxiv:2401.00001", "query": "does it collapse"},
        {
            "mode": "similar", "paper_id": "arxiv:2401.00001", "query": "failure modes",
            "expand": "citers", "limit": 3,
        },
    ],
    ids=["search", "read", "similar"],
)
def test_each_paper_mode_remains_callable_with_the_backend_request_contract(client, app, args):
    from probe._generated.models import PaperSearchRequest

    mode = args["mode"]
    app.web_responses["papers"] = {
        "mode": mode, "state": "ok",
        "results": [{"paper_id": "p", "title": "T", "url": "https://arxiv.org/abs/2401.00001"}],
    }
    out = _call(_e2e(client), "find_papers", args)
    assert out["data"]["mode"] == mode
    assert out["data"]["results"][0]["paper_id"] == "p"
    assert out["data"]["provenance"] == _OPEN_WEB
    assert "completeness" not in out
    path, body = app.web_requests[0]
    assert path == "/v1/web/papers"
    PaperSearchRequest.model_validate(body)
    assert body == args


def test_the_tool_layer_does_not_pin_the_deployments_defaults(client, app):
    _call(_e2e(client), "find_papers", {"mode": "search", "query": "q"})
    assert app.web_requests == [("/v1/web/papers", {"mode": "search", "query": "q"})]


def test_a_permanent_misconfiguration_costs_one_round_trip(client, app):
    # 503 is normally retryable in the SDK; paid provider calls must not retry it.
    app.web_status = 503
    app.web_detail = "paper search is not configured on this deployment"
    out = _call(_e2e(client), "find_papers", {"mode": "search", "query": "q"})
    assert out["completeness"]["missing"] == [MissingMarker.WEB_SEARCH]
    assert "results" not in out["data"]
    assert len(app.web_requests) == 1


def test_the_paper_sub_quota_is_a_fraction_of_the_pool(monkeypatch):
    from probe.mcp import server as server_mod

    async def sizes():
        return int(server_mod._web_limiter().total_tokens)

    monkeypatch.setenv("PROBE_MCP_TOOL_CAPACITY", "16")
    monkeypatch.delenv("PROBE_MCP_WEB_CAPACITY", raising=False)
    assert asyncio.run(sizes()) == 4
    monkeypatch.setenv("PROBE_MCP_WEB_CAPACITY", "2")
    assert asyncio.run(sizes()) == 2
    monkeypatch.delenv("PROBE_MCP_WEB_CAPACITY")
    monkeypatch.setenv("PROBE_MCP_TOOL_CAPACITY", "2")
    assert asyncio.run(sizes()) == 1


def test_a_paper_burst_cannot_starve_the_other_tools(monkeypatch):
    """Two paper calls cannot occupy both slots when their own quota is one."""
    import threading

    monkeypatch.setenv("PROBE_MCP_TOOL_CAPACITY", "2")
    monkeypatch.setenv("PROBE_MCP_WEB_CAPACITY", "1")
    entered = threading.Event()
    release = threading.Event()

    class Parking:
        def find_papers(self, mode: str, **_kw: object) -> dict:
            entered.set()
            assert release.wait(timeout=30), "test never released the parked paper call"
            return {"data": {"mode": mode, "results": []}}

        def browse_research(self, **_kw: object) -> dict:
            return {
                "data": {"scope": None, "depth": 1, "projects": []},
                "_browse_handles": [{
                    "path": ["projects"], "scope": None, "workspace_id": None,
                    "cursor_parameter": "cursor", "start": "browse1.e30",
                    "after": [], "next_cursor": None,
                }],
                "completeness": {"state": "complete", "missing": []},
                "capabilities": {}, "next_cursor": None,
            }

    async def run() -> object:
        server = create_server(Parking())
        first = asyncio.create_task(server.call_tool("find_papers", {"mode": "search", "query": "a"}))
        await asyncio.to_thread(entered.wait, 10)
        second = asyncio.create_task(server.call_tool("find_papers", {"mode": "search", "query": "b"}))
        await asyncio.sleep(0.2)
        try:
            return await asyncio.wait_for(server.call_tool("browse", {}), timeout=5)
        finally:
            release.set()
            await asyncio.gather(first, second, return_exceptions=True)

    assert asyncio.run(run()) is not None


def test_a_plan_ceiling_reaches_the_agent_as_the_servers_own_sentence():
    refusal = (
        "You're out of web searches this month (100 included). Everything else in "
        "Probe keeps working -- it's only the open web that's paused. Book 30 "
        "minutes with us to lift the limit: https://research.prbe.ai/demo-meeting"
    )
    service = _service(raises=errors.LimitReachedError(refusal, detail={"limit": "web_calls"}))
    with pytest.raises(ToolError) as excinfo:
        _call(create_server(service), "find_papers", {"mode": "search", "query": "q"})
    # FastMCP wraps the refusal, but the backend's full sentence must survive.
    assert refusal in str(excinfo.value)
    assert str(excinfo.value).startswith("Error executing tool find_papers: ")


def test_a_ceiling_is_not_reported_as_a_provider_outage():
    service = _service(raises=errors.LimitReachedError("out of web searches", detail={}))
    with pytest.raises(ToolError):
        _call(create_server(service), "find_papers", {"mode": "search", "query": "q"})
