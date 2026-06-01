# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the tier_cache module.

Tests cover the pure/round-trip logic layer only — no BigQuery or Prod DB calls.
External dependencies (_fetch_tier_data_from_bigquery, _resolve_workspace_from_db)
are patched where needed.
"""

from __future__ import annotations

import json
import time
from contextlib import ExitStack
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from airbyte_ops_mcp.tier_cache import (
    CACHE_TTL_SECONDS,
    DEFAULT_TIER,
    OrgTierResult,
    TierSummary,
    WorkspaceResolution,
    _is_cache_fresh,
    _read_cache_file,
    _resolve_bq_tier,
    _write_cache_file,
    build_tier_summary,
    enrich_rows_by_org,
    filter_rows_by_tier,
    get_cache_stats,
    get_org_tier,
    get_org_tiers,
    resolve_workspace,
)

# ---------------------------------------------------------------------------
# _resolve_bq_tier — pure tier string normalization
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "bq_value,expected",
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
def test_resolve_bq_tier_valid(bq_value: str, expected: str) -> None:
    """Known BigQuery tier strings resolve to the correct CustomerTier."""
    assert _resolve_bq_tier(bq_value) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "bq_value",
    [
        pytest.param("", id="empty_string"),
        pytest.param("unknown", id="unknown_value"),
        pytest.param("Tier 3", id="nonexistent_tier"),
        pytest.param("gold", id="random_string"),
    ],
)
def test_resolve_bq_tier_unknown_defaults(bq_value: str) -> None:
    """Unknown tier values default to TIER_2."""
    assert _resolve_bq_tier(bq_value) == DEFAULT_TIER


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
    read_data, fetched_at = _read_cache_file(cache_file)

    assert read_data == data
    assert fetched_at is not None
    assert _is_cache_fresh(fetched_at) is True


@pytest.mark.unit
def test_read_cache_file_missing(tmp_path: Path) -> None:
    """Reading a non-existent cache file returns (None, None)."""
    data, ts = _read_cache_file(tmp_path / "nonexistent.json")
    assert data is None
    assert ts is None


@pytest.mark.unit
def test_read_cache_file_corrupt(tmp_path: Path) -> None:
    """Corrupt JSON is handled gracefully."""
    cache_file = tmp_path / "corrupt.json"
    cache_file.write_text("not valid json {{{")
    data, ts = _read_cache_file(cache_file)
    assert data is None
    assert ts is None


@pytest.mark.unit
def test_read_cache_file_missing_fields(tmp_path: Path) -> None:
    """JSON without required 'data' or 'fetched_at' fields returns (None, None)."""
    cache_file = tmp_path / "bad_structure.json"
    cache_file.write_text(json.dumps({"data": {"org-1": {}}}))  # missing fetched_at
    data, ts = _read_cache_file(cache_file)
    assert data is None
    assert ts is None


@pytest.mark.unit
def test_read_cache_file_wrong_data_type(tmp_path: Path) -> None:
    """JSON where 'data' is not a dict returns (None, None)."""
    cache_file = tmp_path / "wrong_type.json"
    cache_file.write_text(
        json.dumps({"data": ["not", "a", "dict"], "fetched_at": time.time()})
    )
    data, ts = _read_cache_file(cache_file)
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
        pytest.param("org-unknown", "TIER_2", False, id="unknown_defaults_tier_2"),
    ],
)
def test_get_org_tier(org_id: str, expected_tier: str, expected_in_cache: bool) -> None:
    """get_org_tier resolves tiers from cache, defaulting to TIER_2."""
    with patch(
        "airbyte_ops_mcp.tier_cache._load_tier_cache",
        return_value=_make_tier_cache(),
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
        return_value=_make_tier_cache(),
    ):
        results = get_org_tiers(["org-tier0", "org-tier1", "org-unknown"])
        assert len(results) == 3
        assert results[0].customer_tier == "TIER_0"
        assert results[1].customer_tier == "TIER_1"
        assert results[2].customer_tier == "TIER_2"
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
                return_value=_make_tier_cache(),
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
                return_value=_make_tier_cache(),
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
                return_value=_make_tier_cache(),
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
            "org-unknown", "US-Central", "TIER_2", False, id="unknown_us_central"
        ),
        pytest.param("org-unknown", "EU", "TIER_2", True, id="unknown_eu"),
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
        return_value=_make_tier_cache(),
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
        pytest.param("ALL", 3, id="all_returns_everything"),
        pytest.param("TIER_0", 1, id="tier_0_only"),
        pytest.param("TIER_1", 1, id="tier_1_only"),
        pytest.param("TIER_2", 1, id="tier_2_only"),
    ],
)
def test_filter_rows_by_tier(tier_filter: str, expected_count: int) -> None:
    """Rows are correctly filtered by tier, or returned unfiltered for ALL."""
    rows: list[dict[str, Any]] = [
        {"id": "a", "customer_tier": "TIER_0"},
        {"id": "b", "customer_tier": "TIER_1"},
        {"id": "c", "customer_tier": "TIER_2"},
    ]
    filtered = filter_rows_by_tier(rows, tier_filter)  # type: ignore[arg-type]
    assert len(filtered) == expected_count


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
        {"customer_tier": "TIER_2"},
        {"customer_tier": "TIER_2"},
    ]
    summary = build_tier_summary(rows)
    assert isinstance(summary, TierSummary)
    assert summary.tier_0_count == 2
    assert summary.tier_1_count == 1
    assert summary.tier_2_count == 3
    assert summary.total == 6


@pytest.mark.unit
def test_build_tier_summary_empty() -> None:
    """Summary of empty rows is all zeros."""
    summary = build_tier_summary([])
    assert summary.tier_0_count == 0
    assert summary.tier_1_count == 0
    assert summary.tier_2_count == 0
    assert summary.total == 0


@pytest.mark.unit
def test_tier_summary_str() -> None:
    """TierSummary __str__ produces a readable format."""
    summary = TierSummary(tier_0_count=2, tier_1_count=1, tier_2_count=3, total=6)
    result = str(summary)
    assert "2 TIER_0" in result
    assert "1 TIER_1" in result
    assert "3 TIER_2" in result
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
