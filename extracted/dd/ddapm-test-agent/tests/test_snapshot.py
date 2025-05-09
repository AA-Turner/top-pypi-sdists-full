import json
import os

import pytest

from ddapm_test_agent import trace_snapshot
from ddapm_test_agent import tracestats_snapshot
from ddapm_test_agent.trace import add_span_event
from ddapm_test_agent.trace import add_span_link
from ddapm_test_agent.trace import copy_span
from ddapm_test_agent.trace import set_attr
from ddapm_test_agent.trace import set_meta_tag
from ddapm_test_agent.trace import set_metric_tag
from ddapm_test_agent.tracestats import StatsAggr
from ddapm_test_agent.tracestats import StatsBucket

from .conftest import v04_trace
from .trace_utils import random_trace


@pytest.mark.parametrize("snapshot_ci_mode", [False, True])
async def test_snapshot_single_trace(
    agent,
    snapshot_dir,
    snapshot_ci_mode,
    do_reference_v04_http_trace,
):
    """
    When a trace is sent and a snapshot taken
        When not in CI mode
            The test should fail
        When in CI mode
            The snapshot file should be created
            When the same trace is sent again
                The snapshot should pass
    """  # noqa: RST301
    # Send a trace
    resp = await do_reference_v04_http_trace(token="test_case")
    assert resp.status == 200

    # Do the snapshot
    resp = await agent.get("/test/session/snapshot", params={"test_session_token": "test_case"})
    snap_path = snapshot_dir / "test_case.json"
    if snapshot_ci_mode:
        # No previous snapshot file exists so this should fail
        assert resp.status == 400, await resp.text()
        assert f"Trace snapshot file '{snap_path}' not found" in await resp.text()
    else:
        # Since this is the first invocation the snapshot file should be created
        assert resp.status == 200, await resp.text()
        assert os.path.exists(snap_path)
        with open(snap_path, mode="r") as f:
            assert "".join(f.readlines()) != ""

        # Do the snapshot again to actually perform a comparison
        resp = await do_reference_v04_http_trace(token="test_case")
        assert resp.status == 200, await resp.text()

        resp = await agent.get("/test/session/snapshot", params={"test_session_token": "test_case"})
        assert resp.status == 200, await resp.text()


ONE_SPAN_TRACE = random_trace(1)
TWO_SPAN_TRACE = random_trace(2)
FIVE_SPAN_TRACE = random_trace(5)


@pytest.mark.parametrize(
    "expected_traces,actual_traces,error",
    [
        ([ONE_SPAN_TRACE], [ONE_SPAN_TRACE], ""),
        ([FIVE_SPAN_TRACE], [FIVE_SPAN_TRACE], ""),
        # Mismatching trace sizes
        (
            [TWO_SPAN_TRACE],
            [TWO_SPAN_TRACE[:-1]],
            "Received fewer spans (1) than expected (2). Expected unmatched spans: 'postgres.query'",
        ),
        (
            [TWO_SPAN_TRACE[:-1]],
            [TWO_SPAN_TRACE],
            "Received more spans (2) than expected (1). Received unmatched spans: 'postgres.query'",
        ),
        (
            [[set_attr(copy_span(ONE_SPAN_TRACE[0]), "name", "name_expected")]],
            [[set_attr(copy_span(ONE_SPAN_TRACE[0]), "name", "name_received")]],
            "span mismatch on 'name': got 'name_received' which does not match expected 'name_expected'",
        ),
        (
            [
                [
                    TWO_SPAN_TRACE[0],
                    set_attr(copy_span(TWO_SPAN_TRACE[1]), "name", "name_expected"),
                ]
            ],
            [
                [
                    TWO_SPAN_TRACE[0],
                    set_attr(copy_span(TWO_SPAN_TRACE[1]), "name", "name_received"),
                ]
            ],
            "span mismatch on 'name': got 'name_received' which does not match expected 'name_expected'",
        ),
        (
            [
                [
                    TWO_SPAN_TRACE[0],
                    set_meta_tag(copy_span(TWO_SPAN_TRACE[1]), "expected", "value"),
                ]
            ],
            [[TWO_SPAN_TRACE[0], TWO_SPAN_TRACE[1]]],
            "Span meta value 'expected' in expected span but is not in the received span.",
        ),
        (
            [[TWO_SPAN_TRACE[0], TWO_SPAN_TRACE[1]]],
            [
                [
                    TWO_SPAN_TRACE[0],
                    set_metric_tag(copy_span(TWO_SPAN_TRACE[1]), "received", 123.32),
                ]
            ],
            "Span metrics value 'received' in received span but is not in the expected span.",
        ),
        # Mismatching metrics tag
        (
            [
                [
                    TWO_SPAN_TRACE[0],
                    set_metric_tag(copy_span(TWO_SPAN_TRACE[1]), "received", 123.32),
                ]
            ],
            [
                [
                    TWO_SPAN_TRACE[0],
                    set_metric_tag(copy_span(TWO_SPAN_TRACE[1]), "received", 123.32),
                ]
            ],
            "",
        ),
        # Default ignored fields
        (
            [
                [
                    {
                        "name": "s",
                        "span_id": 1234,
                        "trace_id": 1,
                        "parent_id": 0,
                        "resource": "/",
                        "start": 0,
                        "duration": 1,
                        "type": "web",
                        "error": 0,
                        "meta": {},
                        "metrics": {},
                    }
                ]
            ],
            [
                [
                    {
                        "name": "s",
                        "span_id": 4321,
                        "trace_id": 2,
                        "parent_id": 0,
                        "resource": "/",
                        "start": 0,
                        "duration": 1,
                        "type": "web",
                        "error": 0,
                        "meta": {},
                        "metrics": {},
                    }
                ]
            ],
            "",
        ),
    ],
)
async def test_snapshot_trace_differences(agent, expected_traces, actual_traces, error):
    resp = await v04_trace(agent, expected_traces, token="test")
    assert resp.status == 200, await resp.text()

    resp = await agent.get("/test/session/snapshot", params={"test_session_token": "test"})
    assert resp.status == 200, await resp.text()
    resp = await agent.get("/test/session/clear", params={"test_session_token": "test"})
    assert resp.status == 200, await resp.text()

    resp = await v04_trace(agent, actual_traces, token="test")
    assert resp.status == 200, await resp.text()
    resp = await agent.get("/test/session/snapshot", params={"test_session_token": "test"})
    resp_text = await resp.text()
    if error:
        assert resp.status == 400, resp_text
        assert error in resp_text, resp_text
    else:
        assert resp.status == 200, resp_text


@pytest.mark.parametrize(
    "trace,expected",
    [
        (
            [
                [
                    {"trace_id": 1, "span_id": 1, "start": 0},
                    {"trace_id": 1, "parent_id": 1, "span_id": 2, "start": 1},
                    {"trace_id": 1, "parent_id": 1, "span_id": 3, "start": 2},
                    {"trace_id": 1, "parent_id": 2, "span_id": 4, "start": 4},
                ]
            ],
            """[[
  {
    "trace_id": 0,
    "span_id": 1,
    "parent_id": 0,
    "start": 0
  },
     {
       "trace_id": 0,
       "span_id": 2,
       "parent_id": 1,
       "start": 1
     },
        {
          "trace_id": 0,
          "span_id": 4,
          "parent_id": 2,
          "start": 4
        },
     {
       "trace_id": 0,
       "span_id": 3,
       "parent_id": 1,
       "start": 2
     }]]\n""",
        ),
        (
            [
                [
                    {"trace_id": 1, "parent_id": None, "span_id": 1, "start": 0},
                    {"trace_id": 1, "parent_id": 1, "span_id": 2, "start": 1},
                    {"trace_id": 1, "parent_id": 1, "span_id": 3, "start": 2},
                    {"trace_id": 1, "parent_id": 2, "span_id": 4, "start": 4},
                ]
            ],
            """[[
  {
    "trace_id": 0,
    "span_id": 1,
    "parent_id": 0,
    "start": 0
  },
     {
       "trace_id": 0,
       "span_id": 2,
       "parent_id": 1,
       "start": 1
     },
        {
          "trace_id": 0,
          "span_id": 4,
          "parent_id": 2,
          "start": 4
        },
     {
       "trace_id": 0,
       "span_id": 3,
       "parent_id": 1,
       "start": 2
     }]]\n""",
        ),
    ],
)
def test_generate_trace_snapshot(trace, expected):
    assert trace_snapshot.generate_snapshot(trace) == expected


@pytest.mark.parametrize(
    "buckets,expected",
    [
        (
            [
                StatsBucket(  # noqa
                    Start=1000,
                    Duration=10,
                    Stats=[
                        # Not using all the fields of StatsAggr, hence the ignores
                        StatsAggr(  # type: ignore
                            Name="http.request",
                            Type="http",
                            Resource="/users/list",
                            Hits=10,
                            TopLevelHits=10,
                            Duration=100,
                        ),  # noqa
                        StatsAggr(  # type: ignore
                            Name="http.request",
                            Type="http",
                            Resource="/users/create",
                            Hits=5,
                            TopLevelHits=5,
                            Duration=10,
                        ),  # noqa
                    ],
                ),
                StatsBucket(
                    Start=1010,
                    Duration=10,
                    Stats=[
                        StatsAggr(  # type: ignore
                            Name="http.request",
                            Type="http",
                            Resource="/users/list",
                            Hits=20,
                            TopLevelHits=20,
                            Duration=200,
                        ),
                    ],
                ),
            ],
            """[
  {
    "Start": 0,
    "Duration": 10,
    "Stats": [
      {
        "Name": "http.request",
        "Type": "http",
        "Resource": "/users/create",
        "Hits": 5,
        "TopLevelHits": 5,
        "Duration": 10
      },
      {
        "Name": "http.request",
        "Type": "http",
        "Resource": "/users/list",
        "Hits": 10,
        "TopLevelHits": 10,
        "Duration": 100
      }
    ]
  },
  {
    "Start": 10,
    "Duration": 10,
    "Stats": [
      {
        "Name": "http.request",
        "Type": "http",
        "Resource": "/users/list",
        "Hits": 20,
        "TopLevelHits": 20,
        "Duration": 200
      }
    ]
  }
]\n""",
        ),
    ],
)
def test_generate_tracestats_snapshot(buckets, expected):
    assert tracestats_snapshot.generate(buckets) == expected


async def test_snapshot_custom_dir(agent, tmp_path, do_reference_v04_http_trace):
    resp = await do_reference_v04_http_trace(token="test_case")
    assert resp.status == 200

    custom_dir = tmp_path / "custom"
    custom_dir.mkdir()

    resp = await agent.get(
        "/test/session/snapshot",
        params={"test_session_token": "test_case", "dir": str(custom_dir)},
    )
    snap_path = custom_dir / "test_case.json"
    assert resp.status == 200, await resp.text()
    assert os.path.exists(snap_path)
    with open(snap_path, mode="r") as f:
        assert "".join(f.readlines()) != ""


async def test_snapshot_custom_file(agent, tmp_path, do_reference_v04_http_trace):
    resp = await do_reference_v04_http_trace(token="test_case")
    assert resp.status == 200

    custom_dir = tmp_path / "custom"
    custom_dir.mkdir()
    custom_file_name = custom_dir / "custom_snapshot"
    custom_file = custom_dir / "custom_snapshot.json"

    resp = await agent.get(
        "/test/session/snapshot",
        params={"test_session_token": "test_case", "file": str(custom_file_name)},
    )
    assert resp.status == 200, await resp.text()
    assert os.path.exists(custom_file), custom_file
    with open(custom_file, mode="r") as f:
        assert "".join(f.readlines()) != ""


@pytest.mark.parametrize("snapshot_ci_mode", [False, True])
async def test_snapshot_tracestats(agent, tmp_path, snapshot_ci_mode, do_reference_v06_http_stats, snapshot_dir):
    resp = await do_reference_v06_http_stats(token="test_case")
    assert resp.status == 200

    snap_path = snapshot_dir / "test_case_tracestats.json"
    resp = await agent.get("/test/session/snapshot", params={"test_session_token": "test_case"})
    resp_clear = await agent.get("/test/session/clear", params={"test_session_token": "test_case"})
    assert resp_clear.status == 200, await resp_clear.text()

    if snapshot_ci_mode:
        # No previous snapshot file exists so this should fail
        assert resp.status == 400
        assert f"Trace stats snapshot file '{snap_path}' not found" in await resp.text()
    else:
        # First invocation the snapshot, file should be created
        assert resp.status == 200
        assert os.path.exists(snap_path)
        with open(snap_path, mode="r") as f:
            assert "".join(f.readlines()) != ""

        # Do the snapshot again to actually perform a comparison
        resp = await do_reference_v06_http_stats(token="test_case")
        assert resp.status == 200, await resp.text()

        resp = await agent.get("/test/session/snapshot", params={"test_session_token": "test_case"})
        assert resp.status == 200, await resp.text()


@pytest.mark.parametrize("snapshot_removed_attrs", [{"start", "duration", "span_events.name"}])
async def test_removed_attributes(agent, tmp_path, snapshot_removed_attrs, do_reference_v04_http_trace):
    resp = await do_reference_v04_http_trace(token="test_case")
    assert resp.status == 200

    custom_dir = tmp_path / "custom"
    custom_dir.mkdir()
    custom_file_name = custom_dir / "custom_snapshot"
    custom_file = custom_dir / "custom_snapshot.json"

    resp = await agent.get(
        "/test/session/snapshot", params={"test_session_token": "test_case", "file": str(custom_file_name)}
    )
    assert resp.status == 200, await resp.text()

    assert os.path.exists(custom_file), custom_file
    with open(custom_file, mode="r") as f:  # Check that the removed attributes are not present in the span
        file_content = "".join(f.readlines())
        assert file_content != ""
        span = json.loads(file_content)
        for removed_attr in snapshot_removed_attrs:
            assert removed_attr not in span[0]


@pytest.mark.parametrize("snapshot_removed_attrs", [{"metrics.process_id"}])
async def test_removed_attributes_metrics(agent, tmp_path, snapshot_removed_attrs, do_reference_v04_http_trace):
    resp = await do_reference_v04_http_trace(token="test_case")
    assert resp.status == 200

    custom_dir = tmp_path / "custom"
    custom_dir.mkdir()
    custom_file_name = custom_dir / "custom_snapshot"
    custom_file = custom_dir / "custom_snapshot.json"

    resp = await agent.get(
        "/test/session/snapshot", params={"test_session_token": "test_case", "file": str(custom_file_name)}
    )
    assert resp.status == 200, await resp.text()

    assert os.path.exists(custom_file), custom_file
    with open(custom_file, mode="r") as f:
        file_content = "".join(f.readlines())
        assert file_content != ""
        span = json.loads(file_content)
        assert "process_id" not in span[0]


@pytest.mark.parametrize("snapshot_regex_placeholders", [{"addr": "localhost:8080", "path": "^/.*"}])
async def test_with_regex_placeholders(agent, tmp_path, snapshot_removed_attrs, do_reference_v04_http_trace):
    resp = await do_reference_v04_http_trace(token="test_case")
    assert resp.status == 200

    custom_dir = tmp_path / "custom"
    custom_dir.mkdir()
    custom_file_name = custom_dir / "custom_snapshot"
    custom_file = custom_dir / "custom_snapshot.json"

    resp = await agent.get(
        "/test/session/snapshot", params={"test_session_token": "test_case", "file": str(custom_file_name)}
    )
    assert resp.status == 200, await resp.text()

    assert os.path.exists(custom_file), custom_file
    with open(custom_file, mode="r") as f:  # Check that the removed attributes are not present in the span
        file_content = "".join(f.readlines())
        assert file_content != ""
        span = json.loads(file_content)
        assert "http.request" == span[0][0]["name"]
        assert "{path}" == span[0][0]["resource"]
        assert "http://{addr}/users" == span[0][0]["meta"]["http.url"]


ONE_SPAN_TRACE_NO_START = random_trace(1, remove_keys=["start"])
TWO_SPAN_TRACE_NO_START = random_trace(2, remove_keys=["start"])
FIVE_SPAN_TRACE_NO_START = random_trace(5, remove_keys=["start"])


@pytest.mark.parametrize(
    "expected_traces,actual_traces,error,snapshot_removed_attrs",
    [
        ([ONE_SPAN_TRACE_NO_START], [ONE_SPAN_TRACE_NO_START], "", {"start"}),
        ([FIVE_SPAN_TRACE_NO_START], [FIVE_SPAN_TRACE_NO_START], "", {"start"}),
        # Mismatching trace sizes
        (
            [TWO_SPAN_TRACE_NO_START],
            [TWO_SPAN_TRACE_NO_START[:-1]],
            "Received fewer spans (1) than expected (2). Expected unmatched spans: 'flask.request'",
            {"start"},
        ),
        (
            [TWO_SPAN_TRACE_NO_START[:-1]],
            [TWO_SPAN_TRACE_NO_START],
            "Received more spans (2) than expected (1). Received unmatched spans: 'flask.request'",
            {"start"},
        ),
        (
            [[set_attr(copy_span(ONE_SPAN_TRACE_NO_START[0]), "name", "name_expected")]],
            [[set_attr(copy_span(ONE_SPAN_TRACE_NO_START[0]), "name", "name_received")]],
            "span mismatch on 'name': got 'name_received' which does not match expected 'name_expected'",
            {"start"},
        ),
        (
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    set_attr(copy_span(TWO_SPAN_TRACE_NO_START[1]), "name", "name_expected"),
                ]
            ],
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    set_attr(copy_span(TWO_SPAN_TRACE_NO_START[1]), "name", "name_received"),
                ]
            ],
            "span mismatch on 'name': got 'name_received' which does not match expected 'name_expected'",
            {"start"},
        ),
        (
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    set_meta_tag(copy_span(TWO_SPAN_TRACE_NO_START[1]), "expected", "value"),
                ]
            ],
            [[TWO_SPAN_TRACE_NO_START[0], TWO_SPAN_TRACE_NO_START[1]]],
            "Span meta value 'expected' in expected span but is not in the received span.",
            {"start"},
        ),
        (
            [[TWO_SPAN_TRACE_NO_START[0], TWO_SPAN_TRACE_NO_START[1]]],
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    set_metric_tag(copy_span(TWO_SPAN_TRACE_NO_START[1]), "received", 123.32),
                ]
            ],
            "Span metrics value 'received' in received span but is not in the expected span.",
            {"start"},
        ),
        # Mismatching metrics tag
        (
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    set_metric_tag(copy_span(TWO_SPAN_TRACE_NO_START[1]), "received", 123.32),
                ]
            ],
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    set_metric_tag(copy_span(TWO_SPAN_TRACE_NO_START[1]), "received", 123.32),
                ]
            ],
            "",
            {"start"},
        ),
        # Mismatching span links count
        (
            [
                TWO_SPAN_TRACE_NO_START,
            ],
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    add_span_link(copy_span(TWO_SPAN_TRACE_NO_START[1]), TWO_SPAN_TRACE_NO_START[0]),
                ]
            ],
            "Span value 'span_links' in received span but is not in the expected span.",
            {"start"},
        ),
        # Mismatching span link reference
        (
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    add_span_link(copy_span(TWO_SPAN_TRACE_NO_START[1]), TWO_SPAN_TRACE_NO_START[1]),
                ]
            ],
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    add_span_link(copy_span(TWO_SPAN_TRACE_NO_START[1]), TWO_SPAN_TRACE_NO_START[0]),
                ]
            ],
            "Span link 0 mismatch on 'span_id': got '1' which does not match expected '2'.",
            {"start"},
        ),
        # Mismatching span link value
        (
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    add_span_link(copy_span(TWO_SPAN_TRACE_NO_START[1]), TWO_SPAN_TRACE_NO_START[0], flags=1),
                ]
            ],
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    add_span_link(copy_span(TWO_SPAN_TRACE_NO_START[1]), TWO_SPAN_TRACE_NO_START[0], flags=0),
                ]
            ],
            "Span link 0 mismatch on 'flags': got '0' which does not match expected '1'.",
            {"start"},
        ),
        # Mismatching span link fields
        (
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    add_span_link(copy_span(TWO_SPAN_TRACE_NO_START[1]), TWO_SPAN_TRACE_NO_START[0]),
                ]
            ],
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    add_span_link(copy_span(TWO_SPAN_TRACE_NO_START[1]), TWO_SPAN_TRACE_NO_START[0], flags=1),
                ]
            ],
            "Span link 0 value 'flags' in received span link but is not in the expected span link.",
            {"start"},
        ),
        # Mismatching span link attribute
        (
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    add_span_link(
                        copy_span(TWO_SPAN_TRACE_NO_START[1]), TWO_SPAN_TRACE_NO_START[0], {"a": "2", "b": "3"}
                    ),
                ]
            ],
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    add_span_link(
                        copy_span(TWO_SPAN_TRACE_NO_START[1]), TWO_SPAN_TRACE_NO_START[0], {"a": "2", "b": "0"}
                    ),
                ]
            ],
            "Span link 0 attributes mismatch on 'b': got '0' which does not match expected '3'.",
            {"start"},
        ),
        # Matching span link
        (
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    add_span_link(
                        copy_span(TWO_SPAN_TRACE_NO_START[1]), TWO_SPAN_TRACE_NO_START[0], {"a": "2", "b": "0"}, 1
                    ),
                ]
            ],
            [
                [
                    TWO_SPAN_TRACE_NO_START[0],
                    add_span_link(
                        copy_span(TWO_SPAN_TRACE_NO_START[1]), TWO_SPAN_TRACE_NO_START[0], {"a": "2", "b": "0"}, 1
                    ),
                ]
            ],
            "",
            {"start"},
        ),
        # Mismatching span events count
        (
            [TWO_SPAN_TRACE_NO_START],
            [[TWO_SPAN_TRACE_NO_START[0], add_span_event(copy_span(TWO_SPAN_TRACE_NO_START[1]))]],
            "Span value 'span_events' in received span but is not in the expected span.",
            {"start"},
        ),
        # Mismatching span event name
        (
            [[add_span_event(copy_span(ONE_SPAN_TRACE_NO_START[0]), name="expected_name")]],
            [[add_span_event(copy_span(ONE_SPAN_TRACE_NO_START[0]), name="got_name")]],
            "Span event 0 mismatch on 'name': got 'got_name' which does not match expected 'expected_name'.",
            {"start"},
        ),
        # Mismatching span event attributes
        (
            [[add_span_event(copy_span(ONE_SPAN_TRACE_NO_START[0]), attributes={"a": "1", "b": "2"})]],
            [[add_span_event(copy_span(ONE_SPAN_TRACE_NO_START[0]), attributes={"a": "1", "b": "0"})]],
            "Span event 0 attributes mismatch on 'b': got '{'type': 0, 'string_value': '0'}' which does not match expected '{'type': 0, 'string_value': '2'}'.",
            {"start"},
        ),
        # Matching span event
        (
            [[add_span_event(copy_span(ONE_SPAN_TRACE_NO_START[0]), attributes={"a": "1", "b": 2, "c": [3]})]],
            [[add_span_event(copy_span(ONE_SPAN_TRACE_NO_START[0]), attributes={"a": "1", "b": 2, "c": [3]})]],
            "",
            {"start"},
        ),
        # Default ignored fields
        (
            [
                [
                    {
                        "name": "s",
                        "span_id": 1234,
                        "trace_id": 1,
                        "parent_id": 0,
                        "resource": "/",
                        "duration": 1,
                        "type": "web",
                        "error": 0,
                        "meta": {},
                        "metrics": {},
                        "span_events": [
                            {
                                "time_unix_nano": 123,
                                "name": "event_name",
                            },
                        ],
                    }
                ]
            ],
            [
                [
                    {
                        "name": "s",
                        "span_id": 4321,
                        "trace_id": 2,
                        "parent_id": 0,
                        "resource": "/",
                        "duration": 1,
                        "type": "web",
                        "error": 0,
                        "meta": {},
                        "metrics": {},
                        "span_events": [
                            {
                                "time_unix_nano": 456,
                                "name": "event_name",
                            },
                        ],
                    }
                ]
            ],
            "",
            {"start"},
        ),
    ],
)
async def test_snapshot_trace_differences_removed_start(agent, expected_traces, actual_traces, error):
    resp = await v04_trace(agent, expected_traces, token="test")
    assert resp.status == 200, await resp.text()

    resp = await agent.get("/test/session/snapshot", params={"test_session_token": "test"})
    assert resp.status == 200, await resp.text()
    resp = await agent.get("/test/session/clear", params={"test_session_token": "test"})
    assert resp.status == 200, await resp.text()

    resp = await v04_trace(agent, actual_traces, token="test")
    assert resp.status == 200, await resp.text()
    resp = await agent.get("/test/session/snapshot", params={"test_session_token": "test"})
    resp_text = await resp.text()
    if error:
        assert resp.status == 400, resp_text
        assert error in resp_text, resp_text
    else:
        assert resp.status == 200, resp_text


@pytest.mark.parametrize("snapshot_removed_attrs", [{"span_id"}])
async def test_removed_attributes_fails_span_id(agent, tmp_path, snapshot_removed_attrs, do_reference_v04_http_trace):
    resp = await do_reference_v04_http_trace(token="test_case")
    assert resp.status == 200, await resp.text()

    resp = await agent.get("/test/session/snapshot", params={"test_session_token": "test_case"})
    assert resp.status == 400
    assert "Cannot remove 'span_id' from spans" in await resp.text()
