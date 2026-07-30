# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the tier_cache module.

Tests cover the pure/round-trip logic layer only — no live GCS or Prod DB calls.
External dependencies (`storage.Client`, `_fetch_tier_data_from_gcs`,
`_resolve_workspace_from_db`) are patched where needed.
"""

from __future__ import annotations

import json
import time
from contextlib import ExitStack
from pathlib import Path
from typing import Any, Callable
from unittest.mock import MagicMock, patch

import pytest
from google.api_core.exceptions import Forbidden
from google.auth.exceptions import RefreshError

from airbyte_ops_mcp.cloud_admin.version_overrides import validate_tier_filter
from airbyte_ops_mcp.tier_cache import (
    CACHE_TTL_SECONDS,
    DEFAULT_TIER,
    OrgTierResult,
    TierCacheLoadResult,
    TierExportStaleError,
    TierExportTimestampError,
    TierExportTooSmallError,
    TierFilteredRows,
    TierSourceHealth,
    TierSummary,
    WorkspaceResolution,
    _extract_export_timestamp,
    _fetch_tier_data_from_gcs,
    _is_cache_fresh,
    _load_tier_cache,
    _parse_positive_env_value,
    _parse_tier_export_line,
    _read_cache_file,
    _resolve_tier_value,
    _write_cache_file,
    build_tier_summary,
    build_weighted_tier_summary,
    enrich_rows_by_org,
    filter_rows_by_tier,
    get_cache_stats,
    get_org_tier,
    get_org_tiers,
    refresh_tier_cache,
    resolve_workspace,
    tier_source_warnings,
)

# ---------------------------------------------------------------------------
# _resolve_tier_value — pure tier string normalization
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "tier_value,expected",
    [
        pytest.param("Tier 0", "TIER_0", id="title_case_tier_0"),
        pytest.param("Tier 1", "TIER_1", id="title_case_tier_1"),
        pytest.param("Tier 2", "TIER_2", id="title_case_tier_2"),
        pytest.param("tier 0", "TIER_0", id="lower_case_tier_0"),
        pytest.param("tier 1", "TIER_1", id="lower_case_tier_1"),
        pytest.param("TIER 0", "TIER_0", id="upper_case_tier_0"),
        pytest.param("  tier 0  ", "TIER_0", id="whitespace_padded"),
    ],
)
def test_resolve_tier_value_valid(tier_value: str, expected: str) -> None:
    """Known tier strings resolve to the correct CustomerTier."""
    assert _resolve_tier_value(tier_value) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "tier_value",
    [
        pytest.param("", id="empty_string"),
        pytest.param("unknown", id="unknown_value"),
        pytest.param("Tier 3", id="nonexistent_tier"),
        pytest.param("gold", id="random_string"),
    ],
)
def test_resolve_tier_value_unknown_defaults(tier_value: str) -> None:
    """Unknown tier values resolve to UNKNOWN."""
    assert _resolve_tier_value(tier_value) == DEFAULT_TIER


# ---------------------------------------------------------------------------
# _extract_export_timestamp — filename timestamp parsing (backend-mirroring)
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "blob_name,expected",
    [
        pytest.param(
            "data/organization_customer_tiers/2024_11_24_1732490206044_0.jsonl",
            1732490206044,
            id="timestamp_at_index_5",
        ),
        pytest.param(
            "invalid_file_name.jsonl",
            0,
            id="too_few_fields",
        ),
        pytest.param(
            "data/organization_customer_tiers/2024_11_24_notanumber_0.jsonl",
            0,
            id="non_numeric_timestamp",
        ),
    ],
)
def test_extract_export_timestamp(blob_name: str, expected: int) -> None:
    """The 6th `_`-delimited field is parsed as the export timestamp, else 0."""
    assert _extract_export_timestamp(blob_name) == expected


@pytest.mark.unit
def test_fetch_tier_data_retains_explicit_tier_2() -> None:
    """The org-grain export retains explicit Tier 2 rows in the cache."""
    blob = MagicMock()
    blob.name = "data/organization_customer_tiers/2024_11_24_1732490206044_0.jsonl"
    blob.download_as_text.return_value = (
        '{"_airbyte_data": {"organization_id": "org-tier2", "customer_tier": "Tier 2"}}'
    )
    client = MagicMock()
    client.list_blobs.return_value = [blob]
    with patch("airbyte_ops_mcp.tier_cache.storage.Client", return_value=client):
        data, export_timestamp_ms = _fetch_tier_data_from_gcs(credentials=object())
        assert data == {"org-tier2": {"customer_tier": "Tier 2"}}
        assert export_timestamp_ms == 1732490206044


# ---------------------------------------------------------------------------
# _parse_tier_export_line — jsonl line parsing
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "line,expected",
    [
        pytest.param(
            '{"_airbyte_data": {"organization_id": "org-1", "customer_tier": "Tier 0"}}',
            ("org-1", "Tier 0"),
            id="valid_row",
        ),
        pytest.param("   ", None, id="blank_line"),
        pytest.param(
            '{"_airbyte_data": {"organization_id": "org-1",'
            ' "customer_tier": "No Customer Tier"}}',
            ("org-1", "No Customer Tier"),
            id="unrecognized_tier_is_retained",
        ),
        pytest.param(
            '{"_airbyte_data": {"organization_id": "org-1"}}',
            None,
            id="missing_tier",
        ),
        pytest.param('{"foo": "bar"}', None, id="missing_airbyte_data"),
    ],
)
def test_parse_tier_export_line(line: str, expected: tuple[str, str] | None) -> None:
    """Export lines parse to `(org, tier)`, dropping blank/incomplete rows."""
    assert _parse_tier_export_line(line) == expected


@pytest.mark.unit
def test_parse_tier_export_line_malformed_json_raises() -> None:
    """A malformed line raises `JSONDecodeError` (never silently skipped): a
    dropped row could hide a protected organization as `UNKNOWN`."""
    with pytest.raises(json.JSONDecodeError):
        _parse_tier_export_line('{"_airbyte_data": {"organization_id": ')


# ---------------------------------------------------------------------------
# _load_tier_cache — hard-fail semantics (no stale-cache masking)
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "error",
    [
        pytest.param(Forbidden("no access"), id="gcs_forbidden"),
        pytest.param(RefreshError("bad creds"), id="auth_refresh_error"),
    ],
)
def test_load_tier_cache_gcs_failure_hard_fails_despite_stale_cache(
    error: Exception,
) -> None:
    """A GCS auth/API failure raises even when a stale cache exists — the loader
    must not mask a broken tier source (would hide an SA access regression and
    could bypass tier protection).

    Uses the normal TTL path (not `force_refresh`) with an expired cache
    timestamp, so the stale cache is actually read, found stale, and the failed
    refresh must still raise instead of serving the stale entries."""
    with ExitStack() as stack:
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.tier_cache.get_gcp_credentials_for_tier_gcs_ro",
                return_value=object(),
            )
        )
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.tier_cache._read_cache_file",
                return_value=(
                    _make_tier_cache(),
                    time.time() - CACHE_TTL_SECONDS - 1,
                    None,
                ),
            )
        )
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.tier_cache._fetch_tier_data_from_gcs",
                side_effect=error,
            )
        )
        with pytest.raises(RuntimeError, match="GCS tier refresh failed"):
            _load_tier_cache()


@pytest.mark.unit
def test_load_tier_cache_empty_export_hard_fails_despite_stale_cache() -> None:
    """An empty export (no rows) raises even when a stale cache exists, rather
    than serving stale tier data behind a silently-broken export.

    Uses the normal TTL path (not `force_refresh`) with an expired cache
    timestamp, so the stale cache is actually read, found stale, and the
    empty-export refresh must still raise instead of serving the stale
    entries."""
    with ExitStack() as stack:
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.tier_cache.get_gcp_credentials_for_tier_gcs_ro",
                return_value=object(),
            )
        )
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.tier_cache._read_cache_file",
                return_value=(
                    _make_tier_cache(),
                    time.time() - CACHE_TTL_SECONDS - 1,
                    None,
                ),
            )
        )
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.tier_cache._fetch_tier_data_from_gcs",
                return_value=({}, 0),
            )
        )
        with pytest.raises(RuntimeError, match="returned no rows"):
            _load_tier_cache()


# ---------------------------------------------------------------------------
# _is_cache_fresh — pure TTL timestamp check
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "offset_seconds,expected_fresh",
    [
        pytest.param(0, True, id="just_fetched"),
        pytest.param(-3600, True, id="one_hour_old"),
        pytest.param(-(CACHE_TTL_SECONDS - 60), True, id="almost_expired"),
        pytest.param(-(CACHE_TTL_SECONDS + 1), False, id="just_expired"),
        pytest.param(-(CACHE_TTL_SECONDS * 2), False, id="very_stale"),
    ],
)
def test_is_cache_fresh(offset_seconds: int, expected_fresh: bool) -> None:
    """Cache freshness is correctly determined by TTL."""
    fetched_at = time.time() + offset_seconds
    assert _is_cache_fresh(fetched_at) is expected_fresh


@pytest.mark.unit
def test_is_cache_fresh_none() -> None:
    """None timestamp is never fresh."""
    assert _is_cache_fresh(None) is False


# ---------------------------------------------------------------------------
# _read_cache_file / _write_cache_file — disk round-trip
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_cache_round_trip(tmp_path: Path) -> None:
    """Written cache data can be read back with correct structure."""
    cache_file = tmp_path / "test_cache.json"
    data = {"org-1": {"customer_tier": "Tier 0"}, "org-2": {"customer_tier": "Tier 1"}}

    _write_cache_file(cache_file, data)
    read_data, fetched_at, _export_timestamp = _read_cache_file(cache_file)

    assert read_data == data
    assert fetched_at is not None
    assert _is_cache_fresh(fetched_at) is True


@pytest.mark.unit
def test_read_cache_file_missing(tmp_path: Path) -> None:
    """Reading a non-existent cache file returns (None, None)."""
    data, ts, _export_timestamp = _read_cache_file(tmp_path / "nonexistent.json")
    assert data is None
    assert ts is None


@pytest.mark.unit
def test_read_cache_file_corrupt(tmp_path: Path) -> None:
    """Corrupt JSON is handled gracefully."""
    cache_file = tmp_path / "corrupt.json"
    cache_file.write_text("not valid json {{{")
    data, ts, _export_timestamp = _read_cache_file(cache_file)
    assert data is None
    assert ts is None


@pytest.mark.unit
def test_read_cache_file_missing_fields(tmp_path: Path) -> None:
    """JSON without required 'data' or 'fetched_at' fields returns (None, None)."""
    cache_file = tmp_path / "bad_structure.json"
    cache_file.write_text(json.dumps({"data": {"org-1": {}}}))  # missing fetched_at
    data, ts, _export_timestamp = _read_cache_file(cache_file)
    assert data is None
    assert ts is None


@pytest.mark.unit
def test_read_cache_file_wrong_data_type(tmp_path: Path) -> None:
    """JSON where 'data' is not a dict returns (None, None)."""
    cache_file = tmp_path / "wrong_type.json"
    cache_file.write_text(
        json.dumps({"data": ["not", "a", "dict"], "fetched_at": time.time()})
    )
    data, ts, _export_timestamp = _read_cache_file(cache_file)
    assert data is None
    assert ts is None


# ---------------------------------------------------------------------------
# get_org_tier / get_org_tiers — tier resolution with mocked cache
# ---------------------------------------------------------------------------


def _make_tier_cache() -> dict[str, dict[str, str]]:
    """Create a sample tier cache for testing."""
    return {
        "org-tier0": {"customer_tier": "Tier 0"},
        "org-tier1": {"customer_tier": "Tier 1"},
    }


@pytest.mark.unit
@pytest.mark.parametrize(
    "org_id,expected_tier,expected_in_cache",
    [
        pytest.param("org-tier0", "TIER_0", True, id="tier_0_in_cache"),
        pytest.param("org-tier1", "TIER_1", True, id="tier_1_in_cache"),
        pytest.param("org-unknown", "UNKNOWN", False, id="unknown_defaults_unknown"),
    ],
)
def test_get_org_tier(org_id: str, expected_tier: str, expected_in_cache: bool) -> None:
    """get_org_tier resolves tiers from cache, defaulting to UNKNOWN."""
    with patch(
        "airbyte_ops_mcp.tier_cache._load_tier_cache",
        return_value=TierCacheLoadResult(data=_make_tier_cache()),
    ):
        result = get_org_tier(org_id)
        assert isinstance(result, OrgTierResult)
        assert result.organization_id == org_id
        assert result.customer_tier == expected_tier
        assert result.is_in_cache is expected_in_cache


@pytest.mark.unit
def test_get_org_tiers_batch() -> None:
    """get_org_tiers resolves multiple orgs in one call."""
    with patch(
        "airbyte_ops_mcp.tier_cache._load_tier_cache",
        return_value=TierCacheLoadResult(data=_make_tier_cache()),
    ):
        results = get_org_tiers(["org-tier0", "org-tier1", "org-unknown"])
        assert len(results) == 3
        assert results[0].customer_tier == "TIER_0"
        assert results[1].customer_tier == "TIER_1"
        assert results[2].customer_tier == "UNKNOWN"
        assert results[2].is_in_cache is False


# ---------------------------------------------------------------------------
# resolve_workspace — workspace→org→tier chain with mocked DB
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_resolve_workspace_cache_hit() -> None:
    """Workspace found in cache resolves org + tier without DB call."""
    ws_cache = {
        "ws-1": {"organization_id": "org-tier0", "dataplane_name": "EU"},
    }
    with ExitStack() as stack:
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.tier_cache._load_workspace_cache",
                return_value=ws_cache,
            )
        )
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.tier_cache._load_tier_cache",
                return_value=TierCacheLoadResult(data=_make_tier_cache()),
            )
        )
        mock_db = stack.enter_context(
            patch("airbyte_ops_mcp.tier_cache._resolve_workspace_from_db")
        )
        result = resolve_workspace("ws-1")
        assert isinstance(result, WorkspaceResolution)
        assert result.workspace_id == "ws-1"
        assert result.organization_id == "org-tier0"
        assert result.customer_tier == "TIER_0"
        assert result.dataplane_name == "EU"
        assert result.is_eu is True
        assert result.resolved is True
        mock_db.assert_not_called()


@pytest.mark.unit
def test_resolve_workspace_not_found() -> None:
    """Workspace not in cache and not in DB returns resolved=False."""
    with ExitStack() as stack:
        stack.enter_context(
            patch("airbyte_ops_mcp.tier_cache._load_workspace_cache", return_value={})
        )
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.tier_cache._load_tier_cache",
                return_value=TierCacheLoadResult(data=_make_tier_cache()),
            )
        )
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.tier_cache._resolve_workspace_from_db",
                return_value=None,
            )
        )
        stack.enter_context(patch("airbyte_ops_mcp.tier_cache._save_workspace_cache"))
        result = resolve_workspace("ws-missing")
        assert result.resolved is False
        assert result.organization_id is None


@pytest.mark.unit
def test_resolve_workspace_us_region() -> None:
    """US workspace has is_eu=False."""
    ws_cache = {
        "ws-us": {"organization_id": "org-tier1", "dataplane_name": "US"},
    }
    with ExitStack() as stack:
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.tier_cache._load_workspace_cache",
                return_value=ws_cache,
            )
        )
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.tier_cache._load_tier_cache",
                return_value=TierCacheLoadResult(data=_make_tier_cache()),
            )
        )
        result = resolve_workspace("ws-us")
        assert result.is_eu is False
        assert result.dataplane_name == "US"


# ---------------------------------------------------------------------------
# enrich_rows_by_org — row enrichment
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "org_id,dataplane,expected_tier,expected_eu",
    [
        pytest.param("org-tier0", "EU", "TIER_0", True, id="tier0_eu"),
        pytest.param("org-tier1", "US", "TIER_1", False, id="tier1_us"),
        pytest.param(
            "org-unknown", "US-Central", "UNKNOWN", False, id="unknown_us_central"
        ),
        pytest.param("org-unknown", "EU", "UNKNOWN", True, id="unknown_eu"),
    ],
)
def test_enrich_rows_by_org(
    org_id: str,
    dataplane: str,
    expected_tier: str,
    expected_eu: bool,
) -> None:
    """Rows are enriched with customer_tier and is_eu based on org_id."""
    rows: list[dict[str, Any]] = [
        {"organization_id": org_id, "dataplane_name": dataplane},
    ]
    with patch(
        "airbyte_ops_mcp.tier_cache._load_tier_cache",
        return_value=TierCacheLoadResult(data=_make_tier_cache()),
    ):
        enriched = enrich_rows_by_org(rows)
        assert len(enriched) == 1
        assert enriched[0]["customer_tier"] == expected_tier
        assert enriched[0]["is_eu"] is expected_eu


# ---------------------------------------------------------------------------
# filter_rows_by_tier — pure filtering
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "tier_filter,expected_count",
    [
        pytest.param("ALL", 4, id="all_returns_everything"),
        pytest.param("TIER_0", 1, id="tier_0_only"),
        pytest.param("TIER_1", 1, id="tier_1_only"),
        pytest.param("TIER_2", 1, id="tier_2_only"),
        pytest.param("UNKNOWN", 1, id="unknown_only"),
    ],
)
def test_filter_rows_by_tier(tier_filter: str, expected_count: int) -> None:
    """Rows are correctly filtered by tier, or returned unfiltered for ALL."""
    rows: list[dict[str, Any]] = [
        {"id": "a", "customer_tier": "TIER_0"},
        {"id": "b", "customer_tier": "TIER_1"},
        {"id": "c", "customer_tier": "TIER_2"},
        {"id": "d", "customer_tier": "UNKNOWN"},
    ]
    filtered = filter_rows_by_tier(rows, tier_filter)  # type: ignore[arg-type]
    assert len(filtered) == expected_count


@pytest.mark.unit
def test_filtered_empty_rows_retain_degraded_source_metadata() -> None:
    """Filtering all UNKNOWN rows still preserves degraded-source metadata."""
    rows = TierFilteredRows(
        [{"customer_tier": "UNKNOWN"}],
        TierSourceHealth(
            degraded=True,
            reason="Tier export is stale.",
            export_age_seconds=3600,
            export_row_count=1,
        ),
    )
    filtered = filter_rows_by_tier(rows, "TIER_2")
    summary = build_tier_summary(filtered, source_health=filtered.source_health)
    assert filtered == []
    assert summary.warnings == [
        "Customer tier is indeterminable: Tier export is stale; export age: 1h old; "
        "1 organization row. Tier classifications are not authoritative."
    ]


@pytest.mark.parametrize(
    "source_health,expected_warning",
    [
        pytest.param(
            TierSourceHealth(
                degraded=True,
                reason="Tier export is stale: age_seconds=255600, max_age_seconds=172800.",
                export_age_seconds=255600,
                export_row_count=152301,
            ),
            "Customer tier is indeterminable: Tier export is stale: age_seconds=255600, "
            "max_age_seconds=172800; export age: 71h old; 152,301 organization rows. "
            "Tier classifications are not authoritative.",
            id="stale-export",
        ),
        pytest.param(
            TierSourceHealth(
                degraded=True,
                reason="Tier export is too small: organization_rows=1, minimum_organization_rows=150000.",
                export_age_seconds=3600,
                export_row_count=1,
            ),
            "Customer tier is indeterminable: Tier export is too small: "
            "organization_rows=1, minimum_organization_rows=150000; export age: 1h old; "
            "1 organization row. Tier classifications are not authoritative.",
            id="thin-export",
        ),
        pytest.param(
            TierSourceHealth(
                degraded=True,
                reason="Tier export unavailable: GCS permission denied.",
            ),
            "Customer tier is indeterminable: Tier export unavailable: GCS permission denied. "
            "Tier classifications are not authoritative.",
            id="unavailable-export",
        ),
        pytest.param(
            TierSourceHealth(
                degraded=True,
                reason="Tier export freshness is unknown: export_timestamp_ms=0.",
            ),
            "Customer tier is indeterminable: Tier export freshness is unknown: "
            "export_timestamp_ms=0. Tier classifications are not authoritative.",
            id="unparseable-timestamp",
        ),
        pytest.param(
            TierSourceHealth(
                degraded=True,
                reason="Tier export freshness is unknown: export_timestamp_ms=999.",
            ),
            "Customer tier is indeterminable: Tier export freshness is unknown: "
            "export_timestamp_ms=999. Tier classifications are not authoritative.",
            id="future-timestamp",
        ),
    ],
)
def test_tier_source_warning_formats_health_details(
    source_health: TierSourceHealth,
    expected_warning: str,
) -> None:
    """Format warning details without mislabeling the degradation reason."""
    assert tier_source_warnings(source_health) == [expected_warning]


@pytest.mark.unit
def test_tier_source_warnings_are_empty_when_healthy() -> None:
    """Healthy tier sources do not produce operation warnings."""
    assert tier_source_warnings(TierSourceHealth()) == []


@pytest.mark.parametrize(
    ("name", "default", "parser", "raw_value"),
    [
        pytest.param(
            "AIRBYTE_OPS_TIER_EXPORT_MAX_AGE_SECONDS",
            48 * 60 * 60,
            float,
            "48h",
            id="max-age-garbage",
        ),
        pytest.param(
            "AIRBYTE_OPS_TIER_EXPORT_MAX_AGE_SECONDS",
            48 * 60 * 60,
            float,
            "",
            id="max-age-empty",
        ),
        pytest.param(
            "AIRBYTE_OPS_TIER_EXPORT_MIN_ORGANIZATION_ROWS",
            150_000,
            int,
            "150k",
            id="min-rows-garbage",
        ),
        pytest.param(
            "AIRBYTE_OPS_TIER_EXPORT_MIN_ORGANIZATION_ROWS",
            150_000,
            int,
            "",
            id="min-rows-empty",
        ),
    ],
)
def test_invalid_tier_export_env_values_use_defaults(
    monkeypatch: pytest.MonkeyPatch,
    name: str,
    default: float,
    parser: Callable[[str], float],
    raw_value: str,
) -> None:
    """Invalid tier export thresholds fall back to their documented defaults."""
    monkeypatch.setenv(name, raw_value)
    assert _parse_positive_env_value(name, default, parser) == default


@pytest.mark.unit
def test_filter_rows_empty_list() -> None:
    """Filtering an empty list returns an empty list."""
    assert filter_rows_by_tier([], "TIER_0") == []


# ---------------------------------------------------------------------------
# build_tier_summary — pure aggregation
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_build_tier_summary() -> None:
    """Summary correctly counts tiers across rows."""
    rows: list[dict[str, Any]] = [
        {"customer_tier": "TIER_0"},
        {"customer_tier": "TIER_0"},
        {"customer_tier": "TIER_1"},
        {"customer_tier": "TIER_2"},
        {"customer_tier": "UNKNOWN"},
        {"customer_tier": "TIER_2"},
        {"customer_tier": "TIER_2"},
    ]
    summary = build_tier_summary(rows)
    assert isinstance(summary, TierSummary)
    assert summary.tier_0_count == 2
    assert summary.tier_1_count == 1
    assert summary.tier_2_count == 3
    assert summary.unknown_count == 1
    assert summary.total == 7


@pytest.mark.unit
def test_build_weighted_tier_summary_counts_unknown() -> None:
    """Weighted summaries include UNKNOWN in its bucket and total."""
    summary = build_weighted_tier_summary(
        [
            {"customer_tier": "TIER_2", "actor_count": 3},
            {"customer_tier": "UNKNOWN", "actor_count": 2},
        ],
        "actor_count",
    )
    assert summary.tier_2_count == 3
    assert summary.unknown_count == 2
    assert summary.total == 5


@pytest.mark.unit
def test_build_tier_summary_empty() -> None:
    """Summary of empty rows is all zeros."""
    summary = build_tier_summary([])
    assert summary.tier_0_count == 0
    assert summary.tier_1_count == 0
    assert summary.tier_2_count == 0
    assert summary.unknown_count == 0
    assert summary.total == 0


@pytest.mark.unit
def test_tier_summary_str() -> None:
    """TierSummary __str__ produces a readable format."""
    summary = TierSummary(tier_0_count=2, tier_1_count=1, tier_2_count=3, total=6)
    result = str(summary)
    assert "2 TIER_0" in result
    assert "1 TIER_1" in result
    assert "3 TIER_2" in result
    assert "0 UNKNOWN" in result
    assert "total: 6" in result


# ---------------------------------------------------------------------------
# get_cache_stats — with mocked cache files
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_get_cache_stats_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Stats report zeros when no cache files exist."""
    monkeypatch.setattr(
        "airbyte_ops_mcp.tier_cache.TIER_CACHE_FILE", tmp_path / "tier.json"
    )
    monkeypatch.setattr(
        "airbyte_ops_mcp.tier_cache.WORKSPACE_CACHE_FILE", tmp_path / "ws.json"
    )
    stats = get_cache_stats()
    assert stats.tier_cache_size == 0
    assert stats.workspace_cache_size == 0
    assert stats.tier_cache_age_seconds is None
    assert stats.workspace_cache_age_seconds is None


@pytest.mark.unit
def test_get_cache_stats_with_data(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Stats report correct sizes and ages for populated caches."""
    tier_file = tmp_path / "tier.json"
    ws_file = tmp_path / "ws.json"

    _write_cache_file(tier_file, _make_tier_cache())
    _write_cache_file(
        ws_file, {"ws-1": {"organization_id": "org-1", "dataplane_name": "US"}}
    )

    monkeypatch.setattr("airbyte_ops_mcp.tier_cache.TIER_CACHE_FILE", tier_file)
    monkeypatch.setattr("airbyte_ops_mcp.tier_cache.WORKSPACE_CACHE_FILE", ws_file)

    stats = get_cache_stats()
    assert stats.tier_cache_size == 2
    assert stats.workspace_cache_size == 1
    assert stats.tier_cache_age_seconds is not None
    assert stats.tier_cache_age_seconds < 5  # freshly written
    assert stats.workspace_cache_age_seconds is not None
    assert stats.workspace_cache_age_seconds < 5


@pytest.mark.unit
def test_fresh_full_export_passes(monkeypatch: pytest.MonkeyPatch) -> None:
    """A fresh export meeting the row floor is accepted."""
    monkeypatch.setattr(
        "airbyte_ops_mcp.tier_cache.TIER_EXPORT_MIN_ORGANIZATION_ROWS", 1
    )
    export = (
        {"org-1": {"customer_tier": "Tier 2"}},
        int(time.time() * 1000),
    )
    with patch(
        "airbyte_ops_mcp.tier_cache._fetch_tier_data_from_gcs",
        return_value=export,
    ):
        result = _load_tier_cache(force_refresh=True, credentials=object())
    assert result.data == export[0]
    assert result.degraded is False


@pytest.mark.unit
def test_stale_export_degrades_reads_and_rejects_writes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Stale exports become explicit UNKNOWN reads but hard-fail writes."""
    monkeypatch.setattr("airbyte_ops_mcp.tier_cache.TIER_EXPORT_MAX_AGE_SECONDS", 1)
    cache = {"org-1": {"customer_tier": "Tier 0"}}
    with patch(
        "airbyte_ops_mcp.tier_cache._read_cache_file",
        return_value=(cache, time.time(), int((time.time() - 3600) * 1000)),
    ):
        with pytest.raises(
            TierExportStaleError, match=r"age_seconds=.*max_age_seconds"
        ):
            _load_tier_cache()
        result = _load_tier_cache(allow_degraded=True)
    assert result.data == {}
    assert result.degraded is True
    assert result.reason is not None


@pytest.mark.unit
def test_thin_export_degrades_reads_and_rejects_writes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Thin exports become explicit UNKNOWN reads but hard-fail writes."""
    monkeypatch.setattr(
        "airbyte_ops_mcp.tier_cache.TIER_EXPORT_MIN_ORGANIZATION_ROWS", 2
    )
    cache = {"org-1": {"customer_tier": "Tier 0"}}
    timestamp = int(time.time() * 1000)
    with patch(
        "airbyte_ops_mcp.tier_cache._read_cache_file",
        return_value=(cache, time.time(), timestamp),
    ):
        with pytest.raises(TierExportTooSmallError, match="organization_rows=1"):
            _load_tier_cache()
        result = _load_tier_cache(allow_degraded=True)
    assert result.data == {}
    assert result.degraded is True
    assert result.export_row_count == 1


@pytest.mark.unit
def test_unparseable_timestamp_rejects_writes() -> None:
    """A zero timestamp fails closed with a distinct freshness error."""
    export = ({"org-1": {"customer_tier": "Tier 2"}}, 0)
    with patch(
        "airbyte_ops_mcp.tier_cache._fetch_tier_data_from_gcs",
        return_value=export,
    ), pytest.raises(TierExportTimestampError, match="freshness is unknown"):
        _load_tier_cache(force_refresh=True, credentials=object())


@pytest.mark.unit
def test_bypassed_unparseable_timestamp_has_no_age_warning(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A bypassed unknown timestamp does not claim an export age."""
    monkeypatch.setenv("AIRBYTE_OPS_TIER_EXPORT_BYPASS_GUARDS", "true")
    export = ({"org-1": {"customer_tier": "Tier 2"}}, 0)
    with patch(
        "airbyte_ops_mcp.tier_cache._fetch_tier_data_from_gcs",
        return_value=export,
    ):
        result = _load_tier_cache(force_refresh=True, credentials=object())
    assert result.export_age_seconds is None
    assert tier_source_warnings(
        TierSourceHealth(
            degraded=result.degraded,
            reason=result.reason,
            export_age_seconds=result.export_age_seconds,
            export_row_count=result.export_row_count,
        )
    ) == [
        "Customer tier is indeterminable: Tier export freshness is unknown: "
        "export_timestamp_ms=0; 1 organization row. "
        "Tier classifications are not authoritative."
    ]


@pytest.mark.unit
def test_future_dated_export_rejects_writes() -> None:
    """A future export timestamp is treated as unknown freshness."""
    export = (
        {"org-1": {"customer_tier": "Tier 2"}},
        int((time.time() + 3600) * 1000),
    )
    with patch(
        "airbyte_ops_mcp.tier_cache._fetch_tier_data_from_gcs",
        return_value=export,
    ), pytest.raises(TierExportTimestampError, match="freshness is unknown"):
        _load_tier_cache(force_refresh=True, credentials=object())


@pytest.mark.unit
def test_refresh_tier_cache_uses_env_bypass_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The environment bypass is used when refresh has no explicit override."""
    load = MagicMock(return_value=TierCacheLoadResult(data={}))
    monkeypatch.setenv("AIRBYTE_OPS_TIER_EXPORT_BYPASS_GUARDS", "true")
    with patch("airbyte_ops_mcp.tier_cache._load_tier_cache", load), patch(
        "airbyte_ops_mcp.tier_cache.get_cache_stats",
        return_value=MagicMock(),
    ):
        refresh_tier_cache()
    load.assert_called_once_with(force_refresh=True)


@pytest.mark.unit
def test_guard_bypass_loads_export_and_logs_warning(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """The operational bypass loads invalid data and names the bypassed guard."""
    monkeypatch.setenv("AIRBYTE_OPS_TIER_EXPORT_BYPASS_GUARDS", "true")
    monkeypatch.setattr(
        "airbyte_ops_mcp.tier_cache.TIER_EXPORT_MIN_ORGANIZATION_ROWS", 2
    )
    export = (
        {"org-1": {"customer_tier": "Tier 2"}},
        int(time.time() * 1000),
    )
    with patch(
        "airbyte_ops_mcp.tier_cache._fetch_tier_data_from_gcs",
        return_value=export,
    ), caplog.at_level("WARNING"):
        result = _load_tier_cache(force_refresh=True, credentials=object())
    assert result.data == export[0]
    assert "Bypassing tier export size guard" in caplog.text


@pytest.mark.unit
def test_legacy_cache_without_export_timestamp_refreshes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A legacy cache lacking export metadata triggers a GCS refresh."""
    monkeypatch.setattr(
        "airbyte_ops_mcp.tier_cache.TIER_EXPORT_MIN_ORGANIZATION_ROWS", 1
    )
    export = (
        {"org-new": {"customer_tier": "Tier 1"}},
        int(time.time() * 1000),
    )
    with patch(
        "airbyte_ops_mcp.tier_cache._read_cache_file",
        return_value=({"org-old": {"customer_tier": "Tier 2"}}, time.time(), None),
    ), patch(
        "airbyte_ops_mcp.tier_cache._fetch_tier_data_from_gcs",
        return_value=export,
    ):
        result = _load_tier_cache(credentials=object())
    assert result.data == export[0]


@pytest.mark.unit
def test_degraded_write_cannot_be_satisfied_by_concrete_tier() -> None:
    """Only an explicit UNKNOWN acknowledgment may pass an indeterminate source."""
    ok, message = validate_tier_filter(
        "UNKNOWN",
        "TIER_0",
        source_health=TierSourceHealth(
            degraded=True,
            reason="Tier export is stale.",
        ),
        organization_id="org-1",
    )
    assert ok is False
    assert "indeterminable" in (message or "")
    ok, message = validate_tier_filter(
        "UNKNOWN",
        "UNKNOWN",
        source_health=TierSourceHealth(
            degraded=True,
            reason="Tier export is stale.",
        ),
        organization_id="org-1",
    )
    assert ok is True
    assert message is None
