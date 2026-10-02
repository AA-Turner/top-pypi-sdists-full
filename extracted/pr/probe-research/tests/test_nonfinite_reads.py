"""NaN, +inf and -inf survive a raw metric read (plan item (e)).

The server keeps all three in storage but JSON cannot carry them, so a raw point
read sends `value: null` beside `nonfinite: "nan" | "inf" | "-inf"`. The SDK's
read methods turn that back into the float; the strict-JSON writers built on
them (the MCP tools, the CLI's JSON output) keep the wire form, because a bare
NaN token is not JSON and the MCP serializer refuses it outright.

The fake server's rows below are the exact field set of the server's
`ExportPoint` / `MetricPointOut`; research-os's
`tests/unit/test_metric_point_nonfinite.py` feeds the real route's bytes through
this same SDK path.
"""

from __future__ import annotations

import asyncio
import json
import math

import httpx
import pytest

from probe import cli
from probe.mcp.server import create_server
from probe.mcp.service import ResearchReadService
from probe.mcp.source import ResearchOSSource
from probe.sdk.config import Settings
from probe.sdk.nonfinite import to_float, to_wire
from probe.sdk.reader import Reader
from probe.sdk.transport import Transport
from tests.conftest import make_client, open_run

_MARKERS = [None, "nan", "inf", "-inf"]


def _wire_point(id: int, marker: str | None, *, run_id: str | None = None) -> dict:
    """One raw point as the server sends it: a non-finite value is `null` and
    the marker names it (`app/telemetry/schemas.py::ExportPoint`)."""
    point = {
        "id": id,
        "step_index": id - 1,
        "kind": "model",
        "key": "loss",
        "value": 0.5 if marker is None else None,
        "nonfinite": marker,
        "wall_clock": "2026-09-27T12:00:00Z",
        "dimensions": {},
        "labels": {},
        "span_id": None,
    }
    if run_id is not None:  # MetricPointOut carries run_id; ExportPoint does not
        point["run_id"] = run_id
    return point


def _assert_rebuilt(values: list) -> None:
    assert values[0] == 0.5
    assert math.isnan(values[1])
    assert values[2] == math.inf
    assert values[3] == -math.inf


def _strict(text: str):
    def _refuse(token: str):
        raise AssertionError(f"output carries a bare {token} token")

    return json.loads(text, parse_constant=_refuse)


# -- SDK: the floats come back -------------------------------------------------


def test_run_metrics_rebuilds_nan_and_both_infinities(client, app):
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [
        _wire_point(i + 1, m, run_id=run.id) for i, m in enumerate(_MARKERS)
    ]

    points = client.run_metrics(run.id, key="loss")

    _assert_rebuilt([p["value"] for p in points])
    assert [p["nonfinite"] for p in points] == _MARKERS  # the marker stays


def test_export_metric_points_rebuilds_across_pages(client, app):
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [_wire_point(i + 1, m) for i, m in enumerate(_MARKERS)]

    points = list(client.export_metric_points(run.id, key="loss", limit=2))

    assert [p["id"] for p in points] == [1, 2, 3, 4]
    _assert_rebuilt([p["value"] for p in points])


def test_a_server_without_the_marker_still_reads_null(client, app):
    """Negative control: an older server sends a bare null with no marker, and
    there is nothing to rebuild a float from."""
    run = open_run(client, experiment="e", name="r")
    old = _wire_point(1, "nan")
    del old["nonfinite"]
    app.metric_points[run.id] = [old]

    assert [p["value"] for p in client.run_metrics(run.id)] == [None]
    assert [p["value"] for p in client.export_metric_points(run.id)] == [None]


def test_reader_metrics_rebuilds_the_floats():
    rows = [_wire_point(i + 1, m, run_id="r1") for i, m in enumerate(_MARKERS)]

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/runs/r1/metrics"
        return httpx.Response(200, json=rows)

    http = httpx.Client(base_url="http://test", transport=httpx.MockTransport(handler))
    reader = Reader(
        Transport(
            Settings(base_url="http://test", service_token="probe_svc_" + "a" * 32), client=http
        )
    )

    _assert_rebuilt([p["value"] for p in reader.metrics("r1", key="loss")])


def test_to_wire_is_the_inverse_of_to_float():
    for marker in _MARKERS[1:]:
        wire = _wire_point(1, marker)
        assert to_wire(to_float(dict(wire))) == wire
    # a point that never had a marker keeps its shape
    finite = {"id": 1, "value": 2.0}
    assert to_wire(finite) is finite


def test_to_wire_drops_an_empty_marker():
    """`nonfinite: null` says nothing and costs ~5 tokens a point on the MCP
    metrics tool, so a finite point leaves without it."""
    wire = _wire_point(1, None)
    out = to_wire(to_float(dict(wire)))
    assert "nonfinite" not in out
    assert out == {k: v for k, v in wire.items() if k != "nonfinite"}
    assert "nonfinite" in wire  # a copy: the caller's point is untouched


# -- strict-JSON writers keep the wire form --------------------------------------


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


def test_cli_run_metrics_prints_strict_json_with_the_marker(wired, capsys):
    rid = _started_run(wired, capsys)
    wired.metric_points[rid] = [_wire_point(i + 1, m, run_id=rid) for i, m in enumerate(_MARKERS)]

    assert cli.main(["run", "metrics", rid]) == 0

    out = _strict(capsys.readouterr().out)
    assert [(p["value"], p.get("nonfinite", "absent")) for p in out] == [
        (0.5, "absent"),  # a finite point carries no nonfinite key
        (None, "nan"),
        (None, "inf"),
        (None, "-inf"),
    ]


def test_cli_metrics_export_prints_strict_ndjson_with_the_marker(wired, capsys):
    rid = _started_run(wired, capsys)
    wired.metric_points[rid] = [_wire_point(i + 1, m) for i, m in enumerate(_MARKERS)]

    assert cli.main(["metrics", "export", rid, "--key", "loss", "--limit", "2"]) == 0

    lines = capsys.readouterr().out.strip().splitlines()
    assert [(p["value"], p.get("nonfinite", "absent")) for p in map(_strict, lines)] == [
        (0.5, "absent"),  # a finite point carries no nonfinite key
        (None, "nan"),
        (None, "inf"),
        (None, "-inf"),
    ]


def _call(server, tool: str, args: dict):
    """Invoke a tool the way a real MCP client does (through the strict-JSON
    budget serializer), and unwrap the payload."""
    result = asyncio.run(server.call_tool(tool, args))
    payload = result[1] if isinstance(result, tuple) else result
    if isinstance(payload, dict) and "result" in payload:
        return payload["result"]
    if isinstance(payload, list):  # content blocks
        return json.loads(payload[0].text)
    return payload


def test_mcp_points_mode_reads_a_run_that_logged_nan(client, app):
    """The MCP serializer refuses a non-finite float, so without the wire form
    one NaN point would fail the whole tool call."""
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [_wire_point(i + 1, m) for i, m in enumerate(_MARKERS)]
    server = create_server(ResearchReadService(ResearchOSSource(client)))

    out = _call(server, "metrics", {"run_id": run.id, "mode": "points", "key": "loss"})

    assert [(p["value"], p.get("nonfinite", "absent")) for p in out["data"]["points"]] == [
        (0.5, "absent"),  # a finite point carries no nonfinite key
        (None, "nan"),
        (None, "inf"),
        (None, "-inf"),
    ]


def test_mcp_metrics_view_reads_a_run_that_logged_nan(client, app):
    run = open_run(client, experiment="e", name="r")
    app.metric_points[run.id] = [
        _wire_point(i + 1, m, run_id=run.id) for i, m in enumerate(_MARKERS)
    ]
    server = create_server(ResearchReadService(ResearchOSSource(client)))

    out = _call(
        server,
        "entity",
        {"refs": [f"run:{run.id}"], "view": "metrics", "view_options": {"key": "loss"}},
    )

    assert out["data"]["granularity"] == "points"
    assert [(p["value"], p.get("nonfinite", "absent")) for p in out["data"]["points"]] == [
        (0.5, "absent"),  # a finite point carries no nonfinite key
        (None, "nan"),
        (None, "inf"),
        (None, "-inf"),
    ]
