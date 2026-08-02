# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Unit tests for the pure helpers in tools/azure_storage_monitor.py.

The tool lives outside the installed package, so it is loaded by path. Only its
Azure-free helpers are exercised here (Azure SDK imports are lazy).
"""

import importlib.util
import sys
from datetime import timedelta
from pathlib import Path

import pytest

_TOOL_PATH = Path(__file__).resolve().parents[2] / "tools" / "azure_storage_monitor.py"
_spec = importlib.util.spec_from_file_location("azure_storage_monitor", _TOOL_PATH)
assert _spec is not None
assert _spec.loader is not None
azmon = importlib.util.module_from_spec(_spec)
# Register before exec so dataclass introspection can resolve the module.
sys.modules[_spec.name] = azmon
_spec.loader.exec_module(azmon)


@pytest.mark.parametrize(
    ("response_type", "expected"),
    [
        ("ClientThrottlingError", True),
        ("ClientAccountRequestThrottlingError", True),
        ("ServerBusyError", True),
        ("SuccessWithThrottling", True),
        ("SomeFutureThrottlingError", True),
        ("Success", False),
        ("AuthorizationError", False),
        ("", False),
        (None, False),
    ],
)
def test_is_throttle(response_type: str | None, expected: bool) -> None:
    assert azmon.is_throttle(response_type) is expected


def test_granularity_for_known_ranges() -> None:
    for key in azmon.TIME_RANGES:
        lookback, granularity = azmon.granularity_for(key)
        assert lookback > timedelta(0)
        assert granularity > timedelta(0)
        assert granularity <= lookback


def test_granularity_for_unknown_defaults_to_24h() -> None:
    assert azmon.granularity_for("nonsense") == azmon.granularity_for("24h")


@pytest.mark.parametrize(
    ("num", "expected"),
    [
        (None, "—"),
        (0, "0.0 B"),
        (512, "512.0 B"),
        (1024, "1.0 KiB"),
        (1024 * 1024, "1.0 MiB"),
        (1024**4, "1.0 TiB"),
    ],
)
def test_humanize_bytes(num: float | None, expected: str) -> None:
    assert azmon.humanize_bytes(num) == expected


def test_pct() -> None:
    assert azmon.pct(25, 100) == 25.0
    assert azmon.pct(1, 0) == 0.0


def test_sparkline_empty_and_flat() -> None:
    assert azmon.sparkline([]) == ""
    assert azmon.sparkline([None, None]) == ""
    flat = azmon.sparkline([5, 5, 5])
    assert flat == "▁▁▁"


def test_sparkline_scales_and_ignores_none() -> None:
    spark = azmon.sparkline([0, None, 100])
    assert len(spark) == 2
    assert spark[0] == "▁"
    assert spark[-1] == "█"


def test_series_total_and_mean_ignore_none() -> None:
    series = azmon.Series(label="x", points=[1.0, None, 3.0])
    assert series.total == 4.0
    assert series.mean == 2.0
    assert azmon.Series(label="empty", points=[None]).mean == 0.0


class _FakeTimeSeries:
    def __init__(self, metadata_values: object) -> None:
        self.metadata_values = metadata_values


class _FakeMetric:
    name = "Transactions"


class _FakeMetaObj:
    def __init__(self, value: str) -> None:
        self.value = value


def test_series_label_dict_metadata() -> None:
    # azure-monitor-query 1.x exposes the split dimension as a dict.
    ts = _FakeTimeSeries({"apiname": "GetBlob"})
    assert azmon._series_label(ts, _FakeMetric()) == "GetBlob"


def test_series_label_object_list_metadata() -> None:
    # Tolerate the older list-of-objects shape.
    ts = _FakeTimeSeries([_FakeMetaObj("PutBlock")])
    assert azmon._series_label(ts, _FakeMetric()) == "PutBlock"


def test_series_label_falls_back_to_metric_name() -> None:
    for empty in ({}, [], None):
        ts = _FakeTimeSeries(empty)
        assert azmon._series_label(ts, _FakeMetric()) == "Transactions"


def test_resolve_resource_id_explicit() -> None:
    config = azmon.Config(resource_id="/subscriptions/abc/explicit")
    assert azmon.resolve_resource_id(config, None) == "/subscriptions/abc/explicit"


def test_resolve_resource_id_constructed() -> None:
    config = azmon.Config(
        account_name="acct", subscription_id="sub", resource_group="rg"
    )
    resource_id = azmon.resolve_resource_id(config, None)
    assert resource_id == (
        "/subscriptions/sub/resourceGroups/rg/providers/"
        "Microsoft.Storage/storageAccounts/acct"
    )


def test_resolve_resource_id_requires_account() -> None:
    with pytest.raises(ValueError, match="account"):
        azmon.resolve_resource_id(azmon.Config(), None)


def test_resolve_resource_id_requires_subscription() -> None:
    with pytest.raises(ValueError, match="subscription"):
        azmon.resolve_resource_id(azmon.Config(account_name="acct"), None)


def test_resolve_resource_id_discovery_needs_credential() -> None:
    config = azmon.Config(account_name="acct", subscription_id="sub")
    with pytest.raises(ValueError, match="credential"):
        azmon.resolve_resource_id(config, None)


def test_access_hint_module_missing_says_not_installed() -> None:
    hint = azmon.access_hint(ModuleNotFoundError("No module named 'azure.identity'"))
    assert "not installed" in hint
    assert "azure-metrics" in hint


def test_access_hint_name_missing_says_version_mismatch() -> None:
    # Module present but a symbol moved (e.g. azure-monitor-query 2.x): this is
    # a version mismatch, not a missing package.
    exc = ImportError(
        "cannot import name 'MetricsQueryClient' from 'azure.monitor.query'"
    )
    hint = azmon.access_hint(exc)
    assert "version mismatch" in hint
    assert "not installed" not in hint


def test_access_hint_forbidden_says_monitoring_reader() -> None:
    hint = azmon.access_hint(Exception("(403) Forbidden: Authorization failed"))
    assert "Monitoring Reader" in hint
