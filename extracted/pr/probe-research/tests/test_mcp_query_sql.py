"""`query_sql` through the REAL MCP tool layer.

What a fake backend CAN prove here, and nothing more: the request the MCP sends,
the one-page delivery contract, and how refusals reach the agent. Tenant and
project visibility are the database's job and are proven against a real Postgres
in research-os `tests/integration/test_sql_route.py`.
"""

from __future__ import annotations

import asyncio
import json

import pytest
from mcp.server.fastmcp.exceptions import ToolError

from probe.mcp._generated.sql import (
    QUERY_SQL_DESCRIPTION,
    SQL_ARG_DOC,
    TABLES_ARG_DOC,
)
from probe.mcp.server import MCP_INSTRUCTIONS, create_server
from probe.mcp.service import ResearchReadService
from probe.sdk import errors


class _StubSource:
    def __init__(self, payload: object = None, raises: Exception | None = None):
        self._payload = payload if payload is not None else {"database": "experiment"}
        self._raises = raises
        self.calls: list[dict] = []

    def identity(self) -> dict:
        return {"customer_id": "lab-42", "email": "researcher@lab.test"}

    def capabilities(self) -> dict:
        return {}

    def query_sql(self, **kwargs: object) -> object:
        self.calls.append(kwargs)
        if self._raises is not None:
            raise self._raises
        return self._payload


def _call(server, args: dict):
    result = asyncio.run(server.call_tool("query_sql", args))
    payload = result[1] if isinstance(result, tuple) else result
    if isinstance(payload, dict) and "result" in payload:
        return payload["result"]
    if isinstance(payload, list):
        return json.loads(payload[0].text)
    return payload


def _server(source: _StubSource):
    return create_server(ResearchReadService(source))


def _tool():
    tools = asyncio.run(create_server(object()).list_tools())
    return next(t for t in tools if t.name == "query_sql")


def test_the_tool_is_registered_with_the_shared_words():
    tool = _tool()
    assert tool.description == QUERY_SQL_DESCRIPTION
    props = tool.inputSchema["properties"]
    # No `cursor` (paging would re-run the query) and no `max_rows` (derived
    # from token_budget) -- the dashboard's schema has `max_rows`, this one not.
    assert set(props) == {"sql", "tables", "token_budget"}
    assert props["sql"]["description"] == SQL_ARG_DOC
    assert props["tables"]["description"] == TABLES_ARG_DOC
    assert "`query_sql`" in MCP_INSTRUCTIONS


def test_the_shared_description_names_no_argument_the_mcp_lacks():
    # The rule that lets one string serve both surfaces.
    for name in ("max_rows", "cursor"):
        assert f"`{name}`" not in QUERY_SQL_DESCRIPTION


def test_discovery_sends_no_sql_and_no_row_cap():
    source = _StubSource({"database": "experiment", "tables": [{"name": "runs"}]})
    out = _call(_server(source), {})
    assert source.calls == [{"sql": None, "tables": None, "max_rows": None}]
    assert out["tables"] == [{"name": "runs"}]


def test_discovery_passes_the_named_tables_through():
    source = _StubSource({"database": "experiment", "tables": []})
    _call(_server(source), {"tables": ["runs", "experiments"]})
    assert source.calls[0]["tables"] == ["runs", "experiments"]


@pytest.mark.parametrize("budget,rows", [(512, 25), (2000, 100), (8000, 400)])
def test_the_row_cap_is_derived_from_the_delivery_budget(budget, rows):
    source = _StubSource({"database": "experiment", "rows": [], "row_count": 0})
    _call(_server(source), {"sql": "SELECT 1", "token_budget": budget})
    assert source.calls[0]["max_rows"] == rows


def test_an_oversized_result_is_cut_to_one_honest_page_never_a_cursor():
    rows = [[i, "x" * 200] for i in range(100)]
    payload = {
        "database": "experiment",
        "columns": [{"name": "i", "type": "int4"}, {"name": "s", "type": "text"}],
        "rows": rows,
        "row_count": 100,
        "truncated": False,
        "max_rows": 100,
    }
    out = _call(_server(_StubSource(payload)), {"sql": "SELECT 1", "token_budget": 512})
    assert 0 < len(out["rows"]) < 100
    assert out["rows"] == rows[: len(out["rows"])]
    assert out["row_count"] == len(out["rows"])
    assert out["truncated"] is True
    assert out["truncated_reason"] == "byte_limit"
    assert "next_cursor" not in out


def test_a_result_that_fits_comes_back_untouched():
    payload = {"database": "experiment", "rows": [[1]], "row_count": 1, "truncated": False}
    assert _call(_server(_StubSource(payload)), {"sql": "SELECT 1"}) == payload


def test_an_oversized_discovery_names_the_tables_it_left_out():
    tables = [
        {"name": f"t{i}", "columns": [{"name": "c" * 40, "type": "text"}] * 20}
        for i in range(10)
    ]
    out = _call(
        _server(_StubSource({"database": "experiment", "tables": tables})),
        {"tables": [t["name"] for t in tables], "token_budget": 512},
    )
    kept = [t["name"] for t in out["tables"]]
    assert kept and kept == [t["name"] for t in tables[: len(kept)]]
    assert out["omitted_tables"] == [t["name"] for t in tables[len(kept) :]]
    assert "next_cursor" not in out


def test_a_retention_refusal_reaches_the_agent_with_its_hint():
    hint = "Use browse, entity, or metrics scoped to readable runs."
    refusal = errors.LimitReachedError(
        "This run is older than the 30 days your plan keeps open.",
        detail={"limit": "history_locked", "hint": hint},
    )
    with pytest.raises(ToolError) as excinfo:
        _call(_server(_StubSource(raises=refusal)), {"sql": "SELECT 1"})
    assert "older than the 30 days" in str(excinfo.value)
    assert hint in str(excinfo.value)


def test_the_sdk_sends_the_query_as_written_not_scrubbed(app, tmp_path, monkeypatch):
    # A run named like a key prefix is a real name to count, not a credential:
    # the transport's scrubber would rewrite the literal to '<redacted>' and the
    # count would be for the wrong thing, with no error.
    from tests.conftest import make_client

    seen: list[dict] = []
    original = app.handler

    def spy(request):
        if request.url.path == "/v1/sql":
            seen.append(json.loads(request.content))
        return original(request)

    monkeypatch.setattr(app, "handler", spy)
    client = make_client(app, tmp_spool=tmp_path / "spool")
    sql = "SELECT count(*) FROM runs WHERE name = 'sk-baseline'"
    client.query_sql(sql=sql, max_rows=1)
    assert seen and seen[0]["sql"] == sql
