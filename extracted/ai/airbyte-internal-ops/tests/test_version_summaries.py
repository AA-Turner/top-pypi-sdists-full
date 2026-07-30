# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the version_summaries module.

Covers the pure roll-up logic for health, population, and `get_actor_sync_info`
summaries. Tier resolution is exercised through a patched tier cache so no
GCS or Prod DB calls are made.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from airbyte_ops_mcp.tier_cache import TierCacheLoadResult
from airbyte_ops_mcp.version_summaries import (
    ActorHealthState,
    classify_actor_health,
    summarize_population,
    summarize_sync_info,
    summarize_version_health,
)

_TIER_CACHE = {
    "org-tier0": {"customer_tier": "Tier 0"},
    "org-tier1": {"customer_tier": "Tier 1"},
    "org-other": {"customer_tier": "Tier 2"},
}


def _patch_tier_cache() -> Any:
    return patch(
        "airbyte_ops_mcp.tier_cache._load_tier_cache",
        return_value=TierCacheLoadResult(data=_TIER_CACHE),
    )


# ---------------------------------------------------------------------------
# classify_actor_health — pure tri-state classification
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "succeeded,failed,expected",
    [
        pytest.param(3, 0, ActorHealthState.HEALTHY, id="only_successes"),
        pytest.param(2, 5, ActorHealthState.HEALTHY, id="success_wins_over_failure"),
        pytest.param(0, 4, ActorHealthState.UNHEALTHY, id="only_failures"),
        pytest.param(0, 0, ActorHealthState.UNKNOWN, id="no_terminal_signal"),
    ],
)
def test_classify_actor_health(
    succeeded: int, failed: int, expected: ActorHealthState
) -> None:
    """Actor health follows success-first, then failure, then unknown."""
    assert classify_actor_health(succeeded, failed) == expected


# ---------------------------------------------------------------------------
# summarize_version_health — tri-state rollup with tier split
# ---------------------------------------------------------------------------


def _health_rows() -> list[dict[str, Any]]:
    return [
        {
            "actor_id": "a-healthy-t2",
            "organization_id": "org-other",
            "succeeded_jobs": 5,
            "failed_jobs": 0,
        },
        {
            "actor_id": "a-unhealthy-t0",
            "organization_id": "org-tier0",
            "succeeded_jobs": 0,
            "failed_jobs": 2,
        },
        {
            "actor_id": "a-unknown-t1",
            "organization_id": "org-tier1",
            "succeeded_jobs": 0,
            "failed_jobs": 0,
        },
    ]


@pytest.mark.unit
def test_summarize_version_health_all_tiers() -> None:
    """Each actor lands in the right bucket and tier when unfiltered."""
    with _patch_tier_cache():
        summary = summarize_version_health(_health_rows(), tier_filter="ALL")
    assert (summary.healthy, summary.unhealthy, summary.awaiting, summary.disabled) == (
        1,
        1,
        1,
        0,
    )
    assert summary.total_actors == 3
    assert summary.unhealthy_by_tier.tier_0_count == 1
    assert summary.awaiting_by_tier.tier_1_count == 1
    assert summary.healthy_by_tier.tier_2_count == 1


@pytest.mark.unit
def test_summarize_version_health_tier_2_default() -> None:
    """TIER_2 filtering keeps only the standard-tier actor."""
    with _patch_tier_cache():
        summary = summarize_version_health(_health_rows(), tier_filter="TIER_2")
    assert (summary.healthy, summary.unhealthy, summary.awaiting, summary.disabled) == (
        1,
        0,
        0,
        0,
    )
    assert summary.total_actors == 1


@pytest.mark.unit
def test_summarize_version_health_pinned_disabled_fold_in() -> None:
    """Pinned actors with no jobs in the window are counted as disabled."""
    health_rows = [
        {
            "actor_id": "a-healthy",
            "organization_id": "org-other",
            "succeeded_jobs": 1,
            "failed_jobs": 0,
        },
    ]
    pinned_rows = [
        {"actor_id": "a-healthy", "organization_id": "org-other"},
        {"actor_id": "a-never-ran", "organization_id": "org-other"},
    ]
    with _patch_tier_cache():
        summary = summarize_version_health(
            health_rows, pinned_actor_rows=pinned_rows, tier_filter="ALL"
        )
    assert summary.healthy == 1
    assert summary.disabled == 1
    assert summary.awaiting == 0
    assert summary.total_actors == 2


# ---------------------------------------------------------------------------
# summarize_population — applied vs potential audience by tier
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_summarize_population_eligible_and_tiers() -> None:
    """Eligible is active minus pinned, weighted per-org and split by tier."""
    population_rows = [
        {"organization_id": "org-tier0", "actor_count": 10, "pinned_actor_count": 4},
        {"organization_id": "org-other", "actor_count": 6, "pinned_actor_count": 1},
    ]
    with _patch_tier_cache():
        summary = summarize_population(population_rows, tier_filter="ALL")
    assert summary.active_by_tier.total == 16
    assert summary.pinned_any_by_tier.total == 5
    assert summary.eligible_by_tier.total == 11
    assert summary.eligible_by_tier.tier_0_count == 6
    assert summary.eligible_by_tier.tier_2_count == 5
    assert summary.pinned_to_version_by_tier is None


@pytest.mark.unit
def test_summarize_population_pinned_to_version() -> None:
    """Supplying pinned-version rows yields the applied-audience tier summary."""
    population_rows = [
        {"organization_id": "org-other", "actor_count": 8, "pinned_actor_count": 2},
    ]
    pinned_version_rows = [
        {"actor_id": "a1", "organization_id": "org-other"},
        {"actor_id": "a2", "organization_id": "org-tier0"},
    ]
    with _patch_tier_cache():
        summary = summarize_population(
            population_rows,
            pinned_version_rows=pinned_version_rows,
            tier_filter="ALL",
        )
    assert summary.pinned_to_version_by_tier is not None
    assert summary.pinned_to_version_by_tier.total == 2
    assert summary.pinned_to_version_by_tier.tier_0_count == 1
    # No `pinned_to_version_count` on the population rows ⇒ no version-aware
    # addressable/active-pinned split.
    assert summary.addressable_by_tier is None
    assert summary.pinned_to_version_active_by_tier is None


@pytest.mark.unit
def test_summarize_population_addressable_excludes_off_version_pins() -> None:
    """Addressable = active minus off-version pins; numerator = current-RC pins.

    One org has `10` active actors: `4` effectively pinned, of which `3` are on
    the target RC and `1` is on a *different* version. The addressable audience
    must exclude only that off-version pin (`10 - 1 = 9`), keep the current-RC
    pins in the denominator, and use them as the numerator (`3`), so
    `pinned <= addressable` holds.
    """
    population_rows = [
        {
            "organization_id": "org-other",
            "actor_count": 10,
            "pinned_actor_count": 4,
            "pinned_to_version_count": 3,
        },
    ]
    with _patch_tier_cache():
        summary = summarize_population(population_rows, tier_filter="ALL")
    # Version-agnostic views are unchanged.
    assert summary.active_by_tier.total == 10
    assert summary.pinned_any_by_tier.total == 4
    assert summary.eligible_by_tier.total == 6
    # Version-aware views: addressable excludes the single off-version pin.
    assert summary.addressable_by_tier is not None
    assert summary.addressable_by_tier.total == 9
    assert summary.pinned_to_version_active_by_tier is not None
    assert summary.pinned_to_version_active_by_tier.total == 3
    assert (
        summary.pinned_to_version_active_by_tier.total
        <= summary.addressable_by_tier.total
    )


@pytest.mark.unit
def test_summarize_population_addressable_no_off_version_pins() -> None:
    """With every pin on the target RC, addressable equals the active fleet."""
    population_rows = [
        {
            "organization_id": "org-other",
            "actor_count": 7,
            "pinned_actor_count": 2,
            "pinned_to_version_count": 2,
        },
    ]
    with _patch_tier_cache():
        summary = summarize_population(population_rows, tier_filter="ALL")
    assert summary.addressable_by_tier is not None
    assert summary.addressable_by_tier.total == 7
    assert summary.pinned_to_version_active_by_tier is not None
    assert summary.pinned_to_version_active_by_tier.total == 2


@pytest.mark.unit
def test_summarize_population_explicit_no_target_version_ignores_present_column() -> (
    None
):
    """`has_target_version=False` keeps version-aware summaries `None`.

    The real `SELECT_*_ACTOR_POPULATION_BY_ORG` statements always select
    `pinned_to_version_count` (it is `0` when no target was bound), so key
    presence alone cannot distinguish "no target queried" from "target queried".
    An explicit `has_target_version=False` must win over the key being present.
    """
    population_rows = [
        {
            "organization_id": "org-other",
            "actor_count": 10,
            "pinned_actor_count": 4,
            "pinned_to_version_count": 0,  # always emitted by the SQL, even w/o target
        },
    ]
    with _patch_tier_cache():
        summary = summarize_population(
            population_rows, tier_filter="ALL", has_target_version=False
        )
    # Version-agnostic views still populate.
    assert summary.active_by_tier.total == 10
    assert summary.pinned_any_by_tier.total == 4
    # ...but no target was queried, so the version-aware views stay `None`
    # rather than treating all 4 pins as "off-version".
    assert summary.addressable_by_tier is None
    assert summary.pinned_to_version_active_by_tier is None
    assert summary.off_version_pinned_by_tier is None


@pytest.mark.unit
def test_summarize_population_target_version_detected_when_tier_filter_empties_rows() -> (
    None
):
    """`has_target_version` is a schema property, so it survives tier filtering.

    Every org here is Tier 0, so a `TIER_2` filter drops all rows. The
    version-aware summaries must still be a zeroed `TierSummary` (the query
    *did* carry `pinned_to_version_count`), not `None` — deriving the flag from
    the raw rows rather than the filtered rows guards against this.
    """
    population_rows = [
        {
            "organization_id": "org-tier0",
            "actor_count": 9,
            "pinned_actor_count": 4,
            "pinned_to_version_count": 3,
        },
    ]
    with _patch_tier_cache():
        summary = summarize_population(population_rows, tier_filter="TIER_2")
    # The tier filter removed every row, so the counts are all zero.
    assert summary.active_by_tier.total == 0
    # ...but the version-aware summaries are present (zeroed), not `None`.
    assert summary.addressable_by_tier is not None
    assert summary.addressable_by_tier.total == 0
    assert summary.pinned_to_version_active_by_tier is not None
    assert summary.pinned_to_version_active_by_tier.total == 0
    assert summary.off_version_pinned_by_tier is not None


@pytest.mark.unit
def test_summarize_population_job_gated_factors() -> None:
    """`job_gated=True` surfaces the three job-status factors distinctly.

    The gate factors partition the *unpinned* population
    (`gate_pass + failed + no_recent_sync = eligible`), and the backend-style
    gated denominator is `gate_pass + pinned_to_version` — reproducing the
    platform's `nActorsEligibleOrAlreadyPinned`.
    """
    population_rows = [
        {
            "organization_id": "org-other",
            "actor_count": 20,
            "pinned_actor_count": 7,  # 5 on the rollout version, 2 off-version
            "pinned_to_version_count": 5,
            "eligible_gated_count": 6,  # unpinned actors passing the gate
            "gate_excluded_failed_count": 3,
            "gate_excluded_no_recent_sync_count": 4,
        },
    ]
    with _patch_tier_cache():
        summary = summarize_population(
            population_rows, tier_filter="ALL", job_gated=True
        )
    # Unpinned = active - pinned_any = 20 - 7 = 13.
    assert summary.eligible_by_tier.total == 13
    assert summary.gate_pass_by_tier is not None
    assert summary.gate_excluded_failed_by_tier is not None
    assert summary.gate_excluded_no_recent_sync_by_tier is not None
    assert summary.gate_pass_by_tier.total == 6
    assert summary.gate_excluded_failed_by_tier.total == 3
    assert summary.gate_excluded_no_recent_sync_by_tier.total == 4
    # The three gate factors partition the unpinned population exactly.
    assert (
        summary.gate_pass_by_tier.total
        + summary.gate_excluded_failed_by_tier.total
        + summary.gate_excluded_no_recent_sync_by_tier.total
        == summary.eligible_by_tier.total
    )
    # Backend-style denominator = gate_pass (6) + pinned_to_version (5) = 11,
    # distinct from the honest active-fleet addressable (active - off-version).
    assert summary.addressable_gated_by_tier is not None
    assert summary.addressable_gated_by_tier.total == 11
    assert summary.addressable_by_tier is not None
    assert summary.addressable_by_tier.total == 18


@pytest.mark.unit
def test_summarize_population_gate_factors_none_without_job_gated() -> None:
    """Without `job_gated=True`, the gate factors stay `None` even when the
    population rows carry gate counts (no rollout window ⇒ gate not meaningful)."""
    population_rows = [
        {
            "organization_id": "org-other",
            "actor_count": 20,
            "pinned_actor_count": 7,
            "pinned_to_version_count": 5,
            "eligible_gated_count": 6,
            "gate_excluded_failed_count": 3,
            "gate_excluded_no_recent_sync_count": 4,
        },
    ]
    with _patch_tier_cache():
        summary = summarize_population(population_rows, tier_filter="ALL")
    assert summary.gate_pass_by_tier is None
    assert summary.gate_excluded_failed_by_tier is None
    assert summary.gate_excluded_no_recent_sync_by_tier is None
    assert summary.addressable_gated_by_tier is None


# ---------------------------------------------------------------------------
# summarize_sync_info — rollup of a get_actor_sync_info response
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "sync_info,expected",
    [
        pytest.param(
            {
                "data": {
                    "actorSelectionInfo": {
                        "numActors": 100,
                        "numPinnedToConnectorRollout": 10,
                        "numActorsEligibleOrAlreadyPinned": 40,
                    },
                    "syncs": {
                        "a1": {"numSucceeded": 3, "numFailed": 0},
                        "a2": {"numSucceeded": 0, "numFailed": 2},
                        "a3": {"numSucceeded": 1, "numFailed": 1},
                    },
                }
            },
            (100, 10, 40, 2, 1, 0, 7),
            id="camel_case_with_disabled_remainder",
        ),
        pytest.param(
            {
                "data": {
                    "actorSelectionInfo": {
                        "numActors": 100,
                        "numPinnedToConnectorRollout": 5,
                        "numActorsEligibleOrAlreadyPinned": 40,
                    },
                    "syncs": {
                        "a1": {"numSucceeded": 3, "numFailed": 0},
                        "a2": {"numSucceeded": 0, "numFailed": 0},
                    },
                }
            },
            (100, 5, 40, 1, 0, 1, 3),
            id="awaiting_from_nonterminal_and_disabled_remainder",
        ),
        pytest.param(
            {
                "actor_selection_info": {
                    "num_actors": 5,
                    "num_pinned_to_connector_rollout": 2,
                    "num_actors_eligible_or_already_pinned": 3,
                },
                "syncs": {
                    "a1": {"num_succeeded": 0, "num_failed": 1},
                    "a2": {"num_succeeded": 1, "num_failed": 0},
                },
            },
            (5, 2, 3, 1, 1, 0, 0),
            id="snake_case_all_ran",
        ),
        pytest.param(
            {"data": {"actorSelectionInfo": {}, "syncs": {}}},
            (0, 0, 0, 0, 0, 0, 0),
            id="empty_response",
        ),
    ],
)
def test_summarize_sync_info(
    sync_info: dict[str, Any],
    expected: tuple[int, int, int, int, int, int, int],
) -> None:
    """A sync-info response rolls up to population totals and four-bucket health.

    `healthy + unhealthy + awaiting + disabled` sums to `num_pinned` (the
    rollout's full pinned set); `disabled` is the pinned actors that produced no
    syncs in the window."""
    summary = summarize_sync_info(sync_info)
    actual = (
        summary.num_actors,
        summary.num_pinned,
        summary.num_eligible,
        summary.healthy,
        summary.unhealthy,
        summary.awaiting,
        summary.disabled,
    )
    assert actual == expected
    assert (
        summary.healthy + summary.unhealthy + summary.awaiting + summary.disabled
        == summary.num_pinned
    )
