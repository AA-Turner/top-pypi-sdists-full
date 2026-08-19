# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for storage-op metrics (schema, normalization, AIMD env, backends)."""

from __future__ import annotations

import sys
import types
from typing import Any, cast

import pytest

from loadtest.azure_scale_bench import metrics


def test_normalized_rates() -> None:
    m = metrics.StorageOpMetrics(
        stage="phash",
        suffix="s1",
        wall_seconds=10.0,
        num_nodes=4,
        num_cpus=128,
        read_iops=800,
        read_bytes=2000,
        write_iops=200,
        written_bytes=1000,
    )
    norm = m.normalized()
    assert norm["ops_per_s"] == 100.0  # (800+200)/10
    assert norm["bytes_per_s"] == 300.0  # (2000+1000)/10
    assert norm["ops_per_node"] == 250.0  # 1000/4
    assert norm["ops_per_cpu"] == 7.81  # round(1000/128, 2)


def test_normalized_handles_zero_wall_and_missing_scale() -> None:
    m = metrics.StorageOpMetrics(stage="x", suffix="s1")
    norm = m.normalized()
    assert "ops_per_s" not in norm  # wall == 0
    assert "ops_per_node" not in norm  # nodes is None


def test_to_dict_includes_normalized() -> None:
    m = metrics.StorageOpMetrics(stage="x", suffix="s1", wall_seconds=2.0, read_iops=4)
    data = m.to_dict()
    assert data["stage"] == "x"
    assert "normalized" in data
    assert data["normalized"]["ops_per_s"] == 2.0


def test_worker_aimd_env() -> None:
    env = metrics.worker_aimd_env()
    assert "LANCE_AIMD_MAX_RETRIES" in env
    assert "throttle" in env["RUST_LOG"]
    assert metrics.worker_aimd_env(enable=False) == {}
    assert (
        metrics.worker_aimd_env(overrides={"LANCE_AIMD_MAX_RETRIES": "3"})[
            "LANCE_AIMD_MAX_RETRIES"
        ]
        == "3"
    )


def test_blob_resource_id() -> None:
    rid = metrics.blob_resource_id("sub", "rg", "oailancepub")
    assert rid == (
        "/subscriptions/sub/resourceGroups/rg/providers/Microsoft.Storage/"
        "storageAccounts/oailancepub/blobServices/default"
    )


def test_trace_event_counter(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setattr(
        metrics,
        "_THROTTLE",
        {"throttle_events": 0, "retry_events": 0, "max_backoff_ms": 0},
    )
    # Non-throttle target ignored.
    metrics._on_trace_event(types.SimpleNamespace(target="lance::execution", args={}))
    # Throttle events. lance stringifies ALL arg values, so use strings here to
    # reflect reality (a prior bug skipped backoff parsing for stringified args).
    metrics._on_trace_event(
        types.SimpleNamespace(target="lance::object_store::throttle", args={})
    )
    metrics._on_trace_event(
        types.SimpleNamespace(
            target="lance::object_store::throttle",
            args={"attempt": "2", "backoff_ms": "250"},
        )
    )
    snap = metrics.throttle_snapshot()
    assert snap["throttle_events"] == 2
    assert snap["retry_events"] == 1
    assert snap["max_backoff_ms"] == 250  # parsed from the string "250"


def test_metrics_window_rejects_nonpositive() -> None:
    import pytest

    with pytest.raises(ValueError, match="minutes"):
        metrics.metrics_window(0)


def test_azure_monitor_requires_deps() -> None:
    # Only meaningful when azure-monitor-query is absent → clear error. The dep
    # arrives with some extras groups (it entered uv.lock via geneva main), so
    # skip rather than fail where it is installed.
    import importlib.util

    if importlib.util.find_spec("azure.monitor.query") is not None:
        pytest.skip("azure-monitor-query installed; missing-dep error unreachable")
    with pytest.raises(RuntimeError, match="azure-monitor-query"):
        metrics.azure_monitor_metrics(
            subscription_id="s",
            resource_group="rg",
            account="a",
            start_time=0,
            end_time=1,
        )


def test_azure_monitor_wraps_azure_sdk_errors(monkeypatch) -> None:  # noqa: ANN001
    class FakeAzureError(Exception):
        pass

    class FakeCredential:
        pass

    class FakeAggregation:
        TOTAL = "Total"
        AVERAGE = "Average"

    class FakeMetricsClient:
        def __init__(self, credential: FakeCredential) -> None:
            self.credential = credential

        def query_resource(self, *args, **kwargs):  # noqa: ANN002, ANN003, ANN202
            raise FakeAzureError("no usable identity")

    azure_mod = types.ModuleType("azure")
    core_mod = types.ModuleType("azure.core")
    exceptions_mod = types.ModuleType("azure.core.exceptions")
    identity_mod = types.ModuleType("azure.identity")
    monitor_mod = types.ModuleType("azure.monitor")
    query_mod = types.ModuleType("azure.monitor.query")

    cast("Any", exceptions_mod).AzureError = FakeAzureError
    cast("Any", identity_mod).DefaultAzureCredential = FakeCredential
    cast("Any", query_mod).MetricAggregationType = FakeAggregation
    cast("Any", query_mod).MetricsQueryClient = FakeMetricsClient

    cast("Any", azure_mod).core = core_mod
    cast("Any", azure_mod).identity = identity_mod
    cast("Any", azure_mod).monitor = monitor_mod
    cast("Any", core_mod).exceptions = exceptions_mod
    cast("Any", monitor_mod).query = query_mod

    monkeypatch.setitem(sys.modules, "azure", azure_mod)
    monkeypatch.setitem(sys.modules, "azure.core", core_mod)
    monkeypatch.setitem(sys.modules, "azure.core.exceptions", exceptions_mod)
    monkeypatch.setitem(sys.modules, "azure.identity", identity_mod)
    monkeypatch.setitem(sys.modules, "azure.monitor", monitor_mod)
    monkeypatch.setitem(sys.modules, "azure.monitor.query", query_mod)

    with pytest.raises(RuntimeError, match="azure_monitor query failed"):
        metrics.azure_monitor_metrics(
            subscription_id="s",
            resource_group="rg",
            account="a",
            start_time=0,
            end_time=1,
        )


def test_metrics_window() -> None:
    start, end = metrics.metrics_window(30)
    assert end > start
    assert abs((end - start).total_seconds() - 1800) < 1.0


def test_capture_stage_times_and_returns_metrics() -> None:
    with metrics.capture_stage("expand", "s1", num_nodes=2, num_cpus=8) as m:
        m.read_iops = 5
    assert m.stage == "expand"
    assert m.wall_seconds >= 0.0
    assert m.num_nodes == 2
