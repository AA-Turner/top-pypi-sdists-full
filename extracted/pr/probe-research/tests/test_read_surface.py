"""The coordinate read surface (B7): grouped / wide / export / catalog / latest.

Five backend routes were REST-only (the parity ledger's coordinate/telemetry
entries). This file proves the SDK methods that retired those entries actually
speak the routes' contracts: `by` comma-joined, `where` JSON-encoded, grouped and
wide reads follow `next_step` paging, the export generator follows `after_id`
keyset paging, and the 0062 `agg` declaration rides the write so a read can omit
its own. The CLI verbs and read-only MCP tools are smoked over the same fake.
"""

from __future__ import annotations

import asyncio
import json

import pytest

from mcp.server.fastmcp.exceptions import ToolError

from probe import cli, errors
from probe.mcp import server as server_mod
from probe.mcp.contract import MetricMode
from probe.mcp.server import create_server
from probe.mcp.service import ResearchReadService
from probe.mcp.source import ResearchOSSource
from tests.conftest import make_client, open_run, search_response


def _point(id: int, key: str, value: float, step: int, dims: dict | None = None) -> dict:
    return {
        "id": id,
        "key": key,
        "kind": "model",
        "value": value,
        "step_index": step,
        "dimensions": dims or {},
    }


# -- SDK: grouped -------------------------------------------------------------


def test_grouped_encodes_by_comma_joined_and_where_json(client, app):
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [
        _point(1, "loss", 1.0, 0, {"rank": 0, "split": "train"}),
        _point(2, "loss", 3.0, 0, {"rank": 1, "split": "train"}),
        _point(3, "loss", 9.0, 0, {"rank": 0, "split": "val"}),
    ]
    out = client.get_metrics_grouped(
        run.id, "loss", agg="sum", by=["rank", "split"], where={"split": "train"}
    )
    request = next(r for r in app.requests if r.url.path.endswith("/metrics/grouped"))
    assert request.url.params["by"] == "rank,split"  # comma-joined, one param
    assert json.loads(request.url.params["where"]) == {"split": "train"}
    assert out["agg"] == "sum"
    # the val point is filtered out; group labels are each value's JSON text
    assert [(g["group"], g["value"], g["n"]) for g in out["groups"]] == [
        ({"rank": "0", "split": '"train"'}, 1.0, 1),
        ({"rank": "1", "split": '"train"'}, 3.0, 1),
    ]


def test_grouped_follows_next_step_until_exhausted(client, app):
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [_point(i + 1, "loss", float(i), i) for i in range(5)]
    app.grouped_page_rows = 2  # the server's own ceiling sits below the request

    out = client.get_metrics_grouped(run.id, "loss")

    assert [g["value"] for g in out["groups"]] == [0.0, 1.0, 2.0, 3.0, 4.0]
    assert out["truncated"] is False and out["next_step"] is None
    pages = [r for r in app.requests if r.url.path.endswith("/metrics/grouped")]
    assert [p.url.params.get("step_from") for p in pages] == [None, "2", "4"]


def test_grouped_max_rows_bounds_the_total_and_reports_the_cut(client, app):
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [_point(i + 1, "loss", float(i), i) for i in range(5)]

    out = client.get_metrics_grouped(run.id, "loss", max_rows=2)
    assert len(out["groups"]) == 2
    assert out["truncated"] is True and out["next_step"] == 2

    rest = client.get_metrics_grouped(run.id, "loss", step_from=out["next_step"])
    assert [g["value"] for g in rest["groups"]] == [2.0, 3.0, 4.0]
    assert rest["truncated"] is False


def test_grouped_omitted_agg_resolves_the_declared_reduce_fn(client, app):
    """0062: the request carries NO agg param, and the server answers with the
    key's declared fn (else mean)."""
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [
        _point(1, "loss", 1.0, 0),
        _point(2, "loss", 3.0, 0),
    ]
    app.declared_aggs["loss"] = "sum"

    out = client.get_metrics_grouped(run.id, "loss")
    request = next(r for r in app.requests if r.url.path.endswith("/metrics/grouped"))
    assert "agg" not in request.url.params
    assert out["agg"] == "sum"
    assert out["groups"][0]["value"] == 4.0


def test_grouped_conflicting_declarations_are_a_422(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 1.0}, step=0, agg="mean")  # write-side declaration...
    app.declared_aggs["loss"] = "sum"  # ...conflicting with another
    with pytest.raises(errors.ValidationError):
        client.get_metrics_grouped(run.id, "loss")


# -- SDK: the write-side agg declaration --------------------------------------


def test_log_agg_rides_every_point_and_none_stays_off_the_wire(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"tokens": 512.0, "loss": 0.4}, step=1, agg="sum")
    body = json.loads(app.requests[-1].content)
    assert [p["agg"] for p in body["points"]] == ["sum", "sum"]

    run.log({"loss": 0.3}, step=2)
    body = json.loads(app.requests[-1].content)
    assert "agg" not in body["points"][0]


# -- SDK: wide ----------------------------------------------------------------


def test_wide_follows_paging_and_realigns_columns_by_series_identity(client, app):
    """A page's columns cover only its own step window, so a series that starts
    late widens a later page; merged rows must realign, never trust positions."""
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [
        _point(1, "loss", 0.9, 0),
        _point(2, "loss", 0.8, 1),
        _point(3, "loss", 0.7, 2),
        _point(4, "acc", 0.5, 2),
        _point(5, "loss", 0.6, 3),
        _point(6, "acc", 0.6, 3),
    ]
    app.wide_page_rows = 2

    out = client.get_metrics_wide(run.id)

    assert [c["key"] for c in out["columns"]] == ["loss", "acc"]
    assert [(r["step_index"], r["values"]) for r in out["rows"]] == [
        (0, [0.9, None]),
        (1, [0.8, None]),
        (2, [0.7, 0.5]),
        (3, [0.6, 0.6]),
    ]
    assert out["truncated"] is False and out["next_step"] is None
    pages = [r for r in app.requests if r.url.path.endswith("/metrics/wide")]
    assert [p.url.params.get("step_from") for p in pages] == [None, "2"]


def test_wide_key_narrows_as_a_repeated_param(client, app):
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [
        _point(1, "loss", 0.9, 0),
        _point(2, "acc", 0.5, 0),
        _point(3, "lr", 0.1, 0),
    ]
    out = client.get_metrics_wide(run.id, key=["loss", "acc"])
    request = next(r for r in app.requests if r.url.path.endswith("/metrics/wide"))
    assert request.url.params.get_list("key") == ["loss", "acc"]
    assert [c["key"] for c in out["columns"]] == ["acc", "loss"]


# -- SDK: export --------------------------------------------------------------


def test_export_generator_follows_after_id_keyset_paging(client, app):
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [_point(i + 1, "loss", float(i), i) for i in range(5)] + [
        _point(9, "acc", 0.5, 0)
    ]

    points = list(client.export_metric_points(run.id, key="loss", limit=2))

    assert [p["id"] for p in points] == [1, 2, 3, 4, 5]
    pages = [r for r in app.requests if r.url.path.endswith("/metrics/export")]
    assert [p.url.params.get("after_id") for p in pages] == [None, "2", "4"]
    assert all(p.url.params["key"] == "loss" for p in pages)


# -- SDK: coordinates + latest ------------------------------------------------


_CATALOG_ROW = {
    "dims_hash": "h-rank0",
    "dimensions": {"rank": 0},
    "has_metrics": True,
    "has_spans": False,
    "has_artifacts": False,
    "first_seen_at": "2026-07-15T00:00:00Z",
    "last_seen_at": "2026-07-15T00:00:01Z",
}


def test_list_run_coordinates_returns_the_catalog(client, app):
    run = open_run(client, experiment="e", name="r")
    app.coordinates[run.id] = [_CATALOG_ROW]
    assert client.list_run_coordinates(run.id) == [_CATALOG_ROW]
    assert run.coordinates() == [_CATALOG_ROW]


def test_latest_scalars_posts_run_ids_keys_and_kind(client, app):
    first = open_run(client, experiment="e", name="r1")
    second = open_run(client, experiment="e", name="r2")
    app.series[first.id] = [
        {
            "key": "loss",
            "kind": "scalar",
            "dimensions": {},
            "point_count": 2,
            "last_value": 0.3,
            "min_value": 0.3,
            "max_value": 0.9,
            "last_step_index": 1,
        },
    ]
    app.series[second.id] = [
        {
            "key": "loss",
            "kind": "scalar",
            "dimensions": {},
            "point_count": 1,
            "last_value": 0.5,
            "min_value": 0.5,
            "max_value": 0.5,
            "last_step_index": 0,
        },
        {
            "key": "acc",
            "kind": "scalar",
            "dimensions": {},
            "point_count": 1,
            "last_value": 0.7,
            "min_value": 0.7,
            "max_value": 0.7,
            "last_step_index": 0,
        },
    ]

    out = client.latest_scalars([first.id, second.id], keys=["loss"], kind="scalar")

    body = json.loads(app.requests[-1].content)
    # `source_read_contract` rides every provider-capable read: a run mirrored
    # from another tool is refused without it, and this route serves mirrored
    # and local runs through the same call.
    assert body == {
        "run_ids": [first.id, second.id],
        "keys": ["loss"],
        "kind": "scalar",
        "source_read_contract": "coverage-v1",
    }
    assert [(s["run_id"], s["last_value"]) for s in out["scalars"]] == [
        (first.id, 0.3),
        (second.id, 0.5),
    ]


def test_latest_scalars_404s_on_a_deleted_run(client, app):
    run = open_run(client, experiment="e", name="r")
    client.delete_run(run.id)
    with pytest.raises(errors.NotFoundError):
        client.latest_scalars([run.id])


def test_run_handle_delegators_hit_this_runs_routes(client, app):
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [_point(1, "loss", 1.0, 0)]
    run.grouped_metrics("loss")
    run.wide_metrics(key=["loss"])
    list(run.export_points(key="loss"))
    run.coordinates()
    paths = [r.url.path for r in app.requests]
    for suffix in ("/metrics/grouped", "/metrics/wide", "/metrics/export", "/coordinates"):
        assert f"/v1/runs/{run.id}{suffix}" in paths


# -- CLI ----------------------------------------------------------------------


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    def factory(**_kw):
        return make_client(app, tmp_spool=tmp_path / "spool")

    monkeypatch.setattr(cli, "Client", factory)
    cli.main(["project", "create", "--kind", "general", "p"])
    cli.main(["experiment", "create", "e", "--question", "h", "--project", "p"])
    return app


def _started_run(wired, capsys) -> str:
    cli.main(["run", "start", "--experiment", "e", "--name", "r1"])
    return capsys.readouterr().out.strip()


def test_metrics_grouped_command(wired, capsys):
    rid = _started_run(wired, capsys)
    wired.metric_points[rid] = [
        _point(1, "loss", 1.0, 0, {"rank": 0, "split": "train"}),
        _point(2, "loss", 3.0, 0, {"rank": 1, "split": "train"}),
    ]
    rc = cli.main(
        [
            "metrics",
            "grouped",
            rid,
            "--key",
            "loss",
            "--agg",
            "sum",
            "--by",
            "rank",
            "--where",
            '{"split": "train"}',
        ]
    )
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["agg"] == "sum"
    assert [g["group"] for g in out["groups"]] == [{"rank": "0"}, {"rank": "1"}]
    request = next(r for r in wired.requests if r.url.path.endswith("/metrics/grouped"))
    assert request.url.params["by"] == "rank"
    assert json.loads(request.url.params["where"]) == {"split": "train"}


def test_metrics_wide_command(wired, capsys):
    rid = _started_run(wired, capsys)
    wired.metric_points[rid] = [
        _point(1, "loss", 0.9, 0),
        _point(2, "acc", 0.5, 0),
        _point(3, "lr", 0.1, 0),
    ]
    rc = cli.main(["metrics", "wide", rid, "--key", "loss", "--key", "acc"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert [c["key"] for c in out["columns"]] == ["acc", "loss"]
    request = next(r for r in wired.requests if r.url.path.endswith("/metrics/wide"))
    assert request.url.params.get_list("key") == ["loss", "acc"]


def test_metrics_export_command_streams_ndjson(wired, capsys):
    rid = _started_run(wired, capsys)
    wired.metric_points[rid] = [_point(i + 1, "loss", float(i), i) for i in range(3)]
    rc = cli.main(["metrics", "export", rid, "--key", "loss", "--limit", "2"])
    assert rc == 0
    lines = capsys.readouterr().out.strip().splitlines()
    assert [json.loads(line)["id"] for line in lines] == [1, 2, 3]


def test_coordinates_command(wired, capsys):
    rid = _started_run(wired, capsys)
    wired.coordinates[rid] = [_CATALOG_ROW]
    rc = cli.main(["coordinates", rid])
    assert rc == 0
    assert json.loads(capsys.readouterr().out) == [_CATALOG_ROW]


def test_series_latest_command(wired, capsys):
    first = _started_run(wired, capsys)
    cli.main(["run", "start", "--experiment", "e", "--name", "r2"])
    second = capsys.readouterr().out.strip()
    for rid, value in ((first, 0.3), (second, 0.5)):
        wired.series[rid] = [
            {
                "key": "loss",
                "kind": "scalar",
                "dimensions": {},
                "point_count": 1,
                "last_value": value,
                "min_value": value,
                "max_value": value,
                "last_step_index": 0,
            },
        ]
    rc = cli.main(["series", "latest", first, second, "--key", "loss"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert [(s["run_id"], s["last_value"]) for s in out["scalars"]] == [
        (first, 0.3),
        (second, 0.5),
    ]


def test_log_command_declares_agg(wired, capsys):
    rid = _started_run(wired, capsys)
    rc = cli.main(["log", rid, "tokens=512", "--step", "1", "--agg", "sum"])
    assert rc == 0
    body = json.loads(wired.requests[-1].content)
    assert body["points"][0]["agg"] == "sum"


# -- MCP ----------------------------------------------------------------------


def _server(client):
    return create_server(ResearchReadService(ResearchOSSource(client)))


def _call(server, tool: str, args: dict):
    """Invoke a tool the way a real MCP client does, and unwrap the payload."""
    result = asyncio.run(server.call_tool(tool, args))
    payload = result[1] if isinstance(result, tuple) else result
    if isinstance(payload, dict) and "result" in payload:
        return payload["result"]
    if isinstance(payload, list):  # content blocks
        return json.loads(payload[0].text)
    return payload


def test_mcp_grouped_tool_reads_the_reduction(client, app):
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [
        _point(1, "loss", 1.0, 0, {"rank": 0}),
        _point(2, "loss", 3.0, 0, {"rank": 1}),
    ]
    out = _call(
        _server(client),
        "metrics",
        {"run_id": run.id, "mode": "grouped", "key": "loss", "agg": "sum", "by": ["rank"]},
    )
    assert "completeness" not in out
    assert [g["group"] for g in out["data"]["groups"]] == [{"rank": "0"}, {"rank": "1"}]


def test_mcp_grouped_tool_reports_a_cut_read_with_a_resume_cursor(client, app):
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [_point(i + 1, "loss", float(i), i) for i in range(5)]
    server = _server(client)

    page = _call(
        server,
        "metrics",
        {"run_id": run.id, "mode": "grouped", "key": "loss", "max_rows": 2},
    )
    assert page["completeness"]["state"] == "partial"
    assert "rows_beyond_page_bound" in page["completeness"]["missing"]
    values = [g["value"] for g in page["data"]["groups"]]
    for _ in range(3):
        cursor = page["next_cursor"]
        assert isinstance(cursor, str) and cursor and not cursor.isdecimal()
        page = _call(
            server, "metrics",
            {"run_id": run.id, "mode": "grouped", "key": "loss",
             "max_rows": 2, "cursor": cursor},
        )
        values.extend(g["value"] for g in page["data"]["groups"])
        if page.get("next_cursor") is None:
            break
    assert values == [0.0, 1.0, 2.0, 3.0, 4.0]
    assert "completeness" not in page
    assert page.get("next_cursor") is None
    requests = [r for r in app.requests if r.url.path.endswith("/metrics/grouped")]
    assert [r.url.params.get("step_from") for r in requests] == [None, "2", "4"]


def test_mcp_coordinates_tool_lists_the_catalog(client, app):
    run = open_run(client, experiment="e", name="r")
    app.coordinates[run.id] = [_CATALOG_ROW]
    out = _call(_server(client), "metrics", {"run_id": run.id, "mode": "coordinates"})
    assert "completeness" not in out
    assert out["data"]["coordinates"] == [_CATALOG_ROW]


def test_mcp_export_tool_serves_bounded_keyset_pages(client, app):
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [_point(i + 1, "loss", float(i), i) for i in range(5)]
    server = _server(client)

    page = _call(
        server,
        "metrics",
        {"run_id": run.id, "mode": "points", "key": "loss", "limit": 2},
    )
    assert [p["id"] for p in page["data"]["points"]] == [1, 2]
    assert page["completeness"]["state"] == "partial"
    assert "rows_beyond_page_bound" in page["completeness"]["missing"]
    ids = [p["id"] for p in page["data"]["points"]]
    native_starts = [None]
    for _ in range(3):
        cursor = page["next_cursor"]
        assert isinstance(cursor, str) and cursor and not cursor.isdecimal()
        before = len(app.requests)
        page = _call(
            server, "metrics",
            {"run_id": run.id, "mode": "points", "key": "loss", "limit": 2,
             "cursor": cursor},
        )
        requests = [r for r in app.requests[before:] if r.url.path.endswith("/metrics/export")]
        # The source may fetch one lookahead point; check where each MCP
        # invocation starts, not how many underlying generator pages it reads.
        native_starts.append(requests[0].url.params.get("after_id"))
        ids.extend(p["id"] for p in page["data"]["points"])
        if page.get("next_cursor") is None:
            break
    assert ids == [1, 2, 3, 4, 5]
    assert "completeness" not in page
    assert page.get("next_cursor") is None
    assert native_starts == [None, "2", "4"]


def test_mcp_export_tool_clamps_a_runaway_limit(client, app):
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [_point(1, "loss", 1.0, 0)]
    _call(_server(client), "metrics", {"run_id": run.id, "mode": "points", "limit": 10**6})
    request = next(r for r in app.requests if r.url.path.endswith("/metrics/export"))
    assert request.url.params["limit"] == "1000"  # the tool's page ceiling


# -- read_metrics: the merged tool validates against the MODE IT CHOSE --------
#
# The merge's whole risk is that a union schema accepts an argument the chosen
# grain cannot read, the endpoint drops it in silence, and a 200 comes back
# having answered a different question. These tests are the proof it does not:
# one per mode showing the read is REALLY reached, one per mode showing a
# wrong-mode argument is REFUSED, and a structural pair so the tables cannot
# quietly lose a mode.


def _error(server, tool: str, args: dict) -> str:
    """Drive a tool expecting a refusal, and return the message the caller sees.

    Pinned to ToolError, not bare Exception: a KeyError from a missing table row
    is a BUG that a broad catch would score as a successful refusal — the exact
    "the test proves the mode exists, not that it works" gap this file guards."""
    with pytest.raises(ToolError) as excinfo:
        _call(server, tool, args)
    return str(excinfo.value)


@pytest.mark.parametrize(
    ("mode", "table"),
    [("routes", server_mod._METRIC_ROUTES), ("args", server_mod._METRIC_MODE_ARGS)],
)
def test_read_metrics_tables_cover_every_mode(mode, table):
    """Every enum member has a row, and no row names a mode that does not exist.

    Dispatch indexes these tables DIRECTLY, so a member added without a row is a
    KeyError at call time — an opaque 500 for the agent, and one that only fires
    on the mode nobody tested. Equality both ways is the point: a subset check
    would pass a table that has grown a key the enum dropped."""
    assert set(table) == set(MetricMode), mode


def test_read_metrics_required_table_covers_every_mode():
    assert set(server_mod._METRIC_MODE_REQUIRED) == set(MetricMode)


def test_read_metrics_allowlists_and_signature_are_the_same_set(client):
    """The mode allowlists cover exactly the tool's metric-specific arguments.

    Both drifts are silent and opposite. A parameter added to the signature but
    to no allowlist is refused in EVERY mode — the tool advertises an argument it
    always rejects. A name in an allowlist that the signature does not declare is
    dead permission: it can never arrive, so the row reads as coverage that was
    never tested. Neither shows up in a behavioural test, because the modes that
    exist keep working."""
    tools = asyncio.run(_server(client).list_tools())
    spec = next(t for t in tools if t.name == "metrics")
    # Cursor/budget belong to common response delivery, independently of the
    # chosen metric grain; mode itself selects that grain.
    common = {"mode", "cursor", "token_budget"}
    assert common <= set(spec.inputSchema["properties"])
    declared = set(spec.inputSchema["properties"]) - common
    union = set().union(*server_mod._METRIC_MODE_ARGS.values())
    assert not union & common
    assert union == declared

    # And every REQUIRED name is one the mode is actually allowed to receive.
    for mode, required in server_mod._METRIC_MODE_REQUIRED.items():
        assert required <= server_mod._METRIC_MODE_ARGS[mode], mode


def test_read_metrics_grouped_reaches_the_reduction(client, app):
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [
        _point(1, "loss", 1.0, 0, {"rank": 0}),
        _point(2, "loss", 3.0, 0, {"rank": 1}),
    ]
    out = _call(
        _server(client),
        "metrics",
        {"run_id": run.id, "mode": "grouped", "key": "loss", "by": ["rank"]},
    )
    # The GROUPED route, not merely a 200: raw points carry no `groups` key.
    assert [g["group"] for g in out["data"]["groups"]] == [{"rank": "0"}, {"rank": "1"}]
    assert any(r.url.path.endswith("/metrics/grouped") for r in app.requests)


def test_read_metrics_coordinates_reaches_the_catalog(client, app):
    run = open_run(client, experiment="e", name="r")
    app.coordinates[run.id] = [_CATALOG_ROW]
    out = _call(_server(client), "metrics", {"run_id": run.id, "mode": "coordinates"})
    assert out["data"]["coordinates"] == [_CATALOG_ROW]
    assert any(r.url.path.endswith("/coordinates") for r in app.requests)


def test_read_metrics_points_reaches_the_export(client, app):
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [_point(i + 1, "loss", float(i), i) for i in range(3)]
    out = _call(
        _server(client), "metrics", {"run_id": run.id, "mode": "points", "key": "loss"}
    )
    assert [p["id"] for p in out["data"]["points"]] == [1, 2, 3]
    assert any(r.url.path.endswith("/metrics/export") for r in app.requests)


def test_read_metrics_refuses_a_grouping_argument_in_points_mode(client, app):
    """`mode=points, by=[...]` is the exact call that shipped in the backend
    collapse and returned ungrouped points with no error."""
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [_point(1, "loss", 1.0, 0, {"rank": 0})]
    message = _error(
        _server(client),
        "metrics",
        {"run_id": run.id, "mode": "points", "key": "loss", "by": ["rank"]},
    )
    assert "does not read by" in message
    assert "grouped" in message  # points the agent at the mode that does read it
    # REFUSED, not dropped: the request was never built.
    assert not any(r.url.path.endswith("/metrics/export") for r in app.requests)


def test_read_metrics_refuses_a_narrowing_argument_in_coordinates_mode(client, app):
    """The catalog route takes no query parameters, so `key` here is a request to
    narrow an enumeration that cannot be narrowed — it would have returned the
    whole catalog and read as an answer about `loss`."""
    run = open_run(client, experiment="e", name="r")
    app.coordinates[run.id] = [_CATALOG_ROW]
    message = _error(
        _server(client),
        "metrics",
        {"run_id": run.id, "mode": "coordinates", "key": "loss"},
    )
    assert "does not read key" in message
    assert not any(r.url.path.endswith("/coordinates") for r in app.requests)


def test_read_metrics_refuses_a_paging_argument_in_grouped_mode(client, app):
    """`after_id` is the POINTS cursor. Grouped resumes by step, so an agent that
    fed a point id back here would have silently re-read from the beginning."""
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [_point(1, "loss", 1.0, 0)]
    message = _error(
        _server(client),
        "metrics",
        {"run_id": run.id, "mode": "grouped", "key": "loss", "after_id": 2},
    )
    assert "does not read after_id" in message
    assert "points" in message
    assert not any(r.url.path.endswith("/metrics/grouped") for r in app.requests)


def test_read_metrics_refuses_grouped_without_a_key(client, app):
    run = open_run(client, experiment="e", name="r")
    message = _error(_server(client), "metrics", {"run_id": run.id, "mode": "grouped"})
    assert "requires key" in message


def test_read_metrics_refuses_a_bare_string_where_a_list_belongs(client, app):
    """A `str` is a Sequence, so `by="rank"` passes an arity check and then splits
    into one axis per CHARACTER — the backend collapse shipped `keys="loss"`
    reaching the route as `"l"`.

    Over the wire the `list[str]` ANNOTATION is what refuses this, so that is
    what this asserts. The layer's own guard is tested separately and directly
    below; asserting a message here would have scored pydantic either way."""
    run = open_run(client, experiment="e", name="r")
    message = _error(
        _server(client),
        "metrics",
        {"run_id": run.id, "mode": "grouped", "key": "loss", "by": "rank"},
    )
    assert "valid list" in message
    assert not any(r.url.path.endswith("/metrics/grouped") for r in app.requests)


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        ({"by": "rank"}, "must be a list"),
        ({"by": [1, 2]}, "must be a string"),
        ({"where": "rank=1"}, "must be an object"),
    ],
)
def test_metric_args_validator_is_total_for_a_direct_caller(args, expected):
    """`_metric_args_for_mode` is a module-level validator, and pydantic does not
    run for a caller that reaches it directly. It refuses the same shapes the
    annotation does, so the two cannot disagree about what a valid call is."""
    with pytest.raises(ToolError) as excinfo:
        server_mod._metric_args_for_mode(MetricMode.GROUPED, {"run_id": "r", "key": "loss", **args})
    assert expected in str(excinfo.value)


def test_read_metrics_rejects_an_unknown_mode(client):
    run = open_run(client, experiment="e", name="r")
    message = _error(_server(client), "metrics", {"run_id": run.id, "mode": "raw"})
    # The enum annotation puts the vocabulary in the schema, so the rejection
    # names every valid mode without this layer spelling them out again.
    assert "grouped" in message and "coordinates" in message and "points" in message


# -- the deprecated aliases ---------------------------------------------------


_MINIMAL_ARGS = {
    "browse": {},
    "search_knowledge": {"query": "loss"},
    "entity": {"refs": ["run:{run}"]},
    "metrics": {"run_id": "{run}", "mode": "coordinates"},
    "find_papers": {"mode": "search", "query": "what makes GRPO collapse"},
    # Schema discovery: the fake backend answers it without a database.
    "query_sql": {},
}


def test_every_tool_is_compact_by_default(client, app):
    """No tool leads with bookkeeping the agent cannot act on.

    `scope`, `as_of` and `schema_version` are constant per token and per release.
    Re-sending them on every call costs context and pushes the data the caller
    asked for below the fold of anything rendering the response.
    """
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [_point(1, "loss", 1.0, 0)]
    app.coordinates[run.id] = [_CATALOG_ROW]
    # The fake must ANSWER /v1/search: the keyword fallback that used to absorb
    # a 404 here is gone with the capability probe.
    app.search_response = search_response()
    # The MCP now opts into backend-owned row positions. Model a complete
    # empty browse rather than an older backend lacking that contract.
    app.browse_response = {
        "projects": [], "depth": 1, "limit": 10, "truncated": False,
        "continuation_handles": [{
            "path": ["projects"], "scope": None, "workspace_id": None,
            "cursor_parameter": "cursor", "start": "browse1.e30",
            "after": [], "next_cursor": None,
        }],
    }
    server = _server(client)

    registered = {t.name for t in asyncio.run(server.list_tools())}
    assert registered == set(_MINIMAL_ARGS), (
        "a registered tool has no row in _MINIMAL_ARGS (or vice versa) -- add it, "
        "so the new tool's envelope is checked instead of assumed"
    )

    for tool, args in _MINIMAL_ARGS.items():
        out = _call(
            server,
            tool,
            {k: v.format(run=run.id) if isinstance(v, str) else v for k, v in args.items()},
        )
        for gone in ("schema_version", "as_of", "scope"):
            assert gone not in out, f"{tool} still ships {gone}"
        # Only the literature door carries text nobody on the team wrote; every
        # other read is the team's own record and must not claim open-web
        # provenance (nor may find_papers lose it).
        assert ("open-web" in json.dumps(out)) is (tool == "find_papers"), tool
        if tool == "query_sql":
            # No envelope to compact: SQL passes the server's answer through, and
            # its completeness signal is its own `truncated`, not `completeness`.
            assert "tables" in out and "capabilities" not in out
            continue
        # A complete answer carries no `completeness`, and the static capability
        # map never ships compact; a partial one keeps its completeness block.
        assert "capabilities" not in out, tool
        assert out.get("completeness") != {"state": "complete", "missing": []}, tool


def test_verbose_is_still_reachable_for_the_two_tools_that_expose_it(client, app):
    """Compaction is the default, not a wall: the debugging shape is still one
    argument away on the tools whose schema advertises it."""
    app.search_response = search_response()
    server = _server(client)
    for tool, args in (
        ("search_knowledge", {"query": "loss"}),
        ("entity", {"refs": ["run:%s" % open_run(client, experiment="e", name="r2").id]}),
    ):
        full = _call(server, tool, {**args, "verbose": True})
        for kept in ("schema_version", "as_of", "scope"):
            assert kept in full, f"{tool} lost {kept} under verbose=True"
        # Through the DELIVERY layer too, which drops defaults for compact reads.
        assert full["completeness"] == {"state": "complete", "missing": []}, tool
        assert "next_cursor" in full and full["next_cursor"] is None, tool
