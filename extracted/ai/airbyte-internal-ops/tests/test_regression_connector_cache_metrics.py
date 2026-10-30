# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Reading the connector's own HTTP cache counters off its stdout.

A `requests_cache` hit is served inside `Session.send()` and never reaches the
wire, so no proxy capture and no replay ratio can observe it. The CDK counts its
own and emits the totals as `ANALYTICS` trace messages at the end of every
command; this is the parsing of that, and the distinction that matters
throughout is *not reported* versus *reported as zero*.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from airbyte_ops_mcp.regression_tests import http_metrics
from airbyte_ops_mcp.regression_tests.http_metrics import (
    ConnectorCacheMetrics,
    parse_connector_cache_metrics,
)
from airbyte_ops_mcp.regression_tests.models import (
    Command,
    ConnectorUnderTest,
    ExecutionResult,
    TargetOrControl,
)

pytestmark = pytest.mark.unit


def _analytics(type_: str, value: Any) -> dict[str, Any]:
    """One analytics message, shaped as the CDK writes it to stdout."""
    return {
        "type": "TRACE",
        "trace": {
            "type": "ANALYTICS",
            "emitted_at": 1_700_000_000_000,
            # The protocol carries the value as a string even when it is numeric.
            "analytics": {"type": type_, "value": value},
        },
    }


_RECORD = {
    "type": "RECORD",
    "record": {"stream": "users", "data": {"id": 1}, "emitted_at": 1_700_000_000_000},
}


def _result(tmp_path: Path, *messages: dict[str, Any]) -> ExecutionResult:
    """A finished `read` whose stdout is exactly these messages."""
    stdout = tmp_path / "stdout.jsonl"
    stdout.write_text("\n".join(json.dumps(message) for message in messages))

    return ExecutionResult(
        connector_under_test=ConnectorUnderTest(
            image_name="airbyte/source-test:1.0.0",
            target_or_control=TargetOrControl.TARGET,
        ),
        command=Command.READ,
        stdout_file_path=stdout,
        stderr_file_path=tmp_path / "stderr.log",
        success=True,
        exit_code=0,
    )


def _metrics(tmp_path: Path, *messages: dict[str, Any]) -> ConnectorCacheMetrics | None:
    """What the harness reads off a run whose stdout is exactly these messages.

    Through a real `ExecutionResult` and its summary, so the messages are parsed
    the way the CLI parses them rather than handed over pre-built.
    """
    return parse_connector_cache_metrics(_result(tmp_path, *messages).summary.analytics)


def test_the_proxy_metric_no_longer_claims_to_be_a_cache_metric() -> None:
    """The duplicate-URL heuristic and the dead helper that emitted it are gone.

    Asserted here rather than in `tests/test_http_metrics.py`, whose dump tests
    are skipped without the `live-tests` dependency group -- and so in the CI
    job that runs the rest of the suite. A removal test that never runs is not
    one.
    """
    assert not hasattr(http_metrics.HttpMetrics, "cache_hit_ratio")
    assert not hasattr(http_metrics, "compute_http_metrics_comparison")
    assert "cache_hits_count" not in http_metrics.HttpMetrics.__dataclass_fields__
    # The metric that replaces it, and the one the legacy report actually had.
    assert hasattr(http_metrics.HttpMetrics, "replay_hit_ratio")


def test_both_counters_are_read_off_the_run(tmp_path: Path) -> None:
    assert _metrics(
        tmp_path,
        _RECORD,
        _analytics("http-request-count", "40"),
        _analytics("http-cache-hit-count", "10"),
    ) == ConnectorCacheMetrics(request_count=40, cache_hits_count=10)


def test_a_connector_that_reported_nothing_reports_none(tmp_path: Path) -> None:
    """The case that must never render as `0%`.

    A Java connector, a connector using its own `requests.Session`, and a
    connector on a CDK predating the counters all look like this. `None` is what
    drives the *not reported* rendering; a zero here would read as a cache the
    version under test had broken.
    """
    assert _metrics(tmp_path, _RECORD) is None


def test_an_unrelated_analytics_message_is_not_mistaken_for_a_counter(
    tmp_path: Path,
) -> None:
    """Connectors emit plenty of other analytics -- `file-cdk-*-stream-count`, say."""
    metrics = _metrics(
        tmp_path,
        _analytics("file-cdk-csv-stream-count", "3"),
        _analytics("http-request-count", "7"),
    )

    assert metrics is not None
    assert metrics.request_count == 7


def test_a_request_count_without_a_hit_count_is_a_measured_zero(
    tmp_path: Path,
) -> None:
    """Unlike a missing request count, this connector did report: it cached nothing."""
    assert _metrics(
        tmp_path, _analytics("http-request-count", "12")
    ) == ConnectorCacheMetrics(request_count=12, cache_hits_count=0)


def test_a_hit_count_without_a_request_count_reports_nothing(tmp_path: Path) -> None:
    """No denominator, no ratio -- and a hit count alone answers no question."""
    assert _metrics(tmp_path, _analytics("http-cache-hit-count", "5")) is None


@pytest.mark.parametrize("value", ["", "not-a-number", None])
def test_an_unparseable_count_is_treated_as_no_report(
    tmp_path: Path, value: Any
) -> None:
    """A malformed value is not zero: nobody measured it.

    Same reasoning as a missing message. Falling back to zero here would put a
    fabricated `0.00%` in the report on the strength of a protocol violation.
    """
    assert _metrics(tmp_path, _analytics("http-request-count", value)) is None


def test_the_counters_are_read_on_the_pass_that_writes_the_artifacts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No second walk of stdout for two numbers.

    A `read`'s stdout is the dataset, and on a stopped-early read a second pass
    over it is charged to the shared read budget. The counters ride on the same
    pass that writes the artifacts and counts the messages.
    """
    result = _result(
        tmp_path,
        _RECORD,
        _analytics("http-request-count", "40"),
        _analytics("http-cache-hit-count", "10"),
    )
    opened = 0
    real_open = Path.open

    def _counting_open(self: Path, *args: Any, **kwargs: Any):
        nonlocal opened
        if self == result.stdout_file_path:
            opened += 1
        return real_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", _counting_open)

    result.save_artifacts(tmp_path / "artifacts")
    metrics = parse_connector_cache_metrics(result.summary.analytics)

    assert metrics == ConnectorCacheMetrics(request_count=40, cache_hits_count=10)
    assert opened == 1


@pytest.mark.parametrize("value", ["", "not-a-number", None])
def test_a_hit_count_that_is_there_but_unreadable_is_no_report(
    tmp_path: Path, value: Any
) -> None:
    """Unlike a hit count that was never emitted, which is a measured zero.

    A message that is present and carries nothing readable is a protocol
    violation, not a connector saying "no hits"; zeroing it would print a
    `0.00%` and a `Caching lost` warning on the strength of the violation.
    """
    assert (
        _metrics(
            tmp_path,
            _analytics("http-request-count", "12"),
            _analytics("http-cache-hit-count", value),
        )
        is None
    )


@pytest.mark.parametrize(
    ("requests", "hits"),
    [
        pytest.param("-1", "0", id="negative-requests"),
        pytest.param("10", "-1", id="negative-hits"),
        pytest.param("10", "11", id="more-hits-than-requests"),
    ],
)
def test_a_pair_that_cannot_be_a_count_is_no_report(
    tmp_path: Path, requests: str, hits: str
) -> None:
    """A ratio over 100% or a negative count is a malformed report, not a number."""
    assert (
        _metrics(
            tmp_path,
            _analytics("http-request-count", requests),
            _analytics("http-cache-hit-count", hits),
        )
        is None
    )


def test_the_last_reported_pair_wins(tmp_path: Path) -> None:
    """The CDK emits these once, in the entrypoint's `finally`.

    A run that somehow emitted two pairs -- a harness invoking the entrypoint
    twice into one stdout -- has only one pair that saw the whole run.
    """
    assert _metrics(
        tmp_path,
        _analytics("http-request-count", "5"),
        _analytics("http-cache-hit-count", "1"),
        _analytics("http-request-count", "50"),
        _analytics("http-cache-hit-count", "20"),
    ) == ConnectorCacheMetrics(request_count=50, cache_hits_count=20)


@pytest.mark.parametrize(
    ("requests", "hits", "expected"),
    [
        (40, 10, "25.00%"),
        (3, 1, "33.33%"),
        (8, 8, "100.00%"),
        (8, 0, "0.00%"),
        # No requests, no ratio: a `0.00%` here would claim a cache that never
        # got the chance to hit. Formatted exactly like the legacy report's.
        (0, 0, "N/A"),
    ],
)
def test_the_ratio_is_formatted_like_the_legacy_report(
    requests: int, hits: int, expected: str
) -> None:
    assert (
        ConnectorCacheMetrics(
            request_count=requests, cache_hits_count=hits
        ).cache_hit_ratio
        == expected
    )
