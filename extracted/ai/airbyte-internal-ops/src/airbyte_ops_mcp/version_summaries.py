# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Health and population summaries for a connector version.

This module holds the pure roll-up logic shared by the MCP tools and the Ops
Webapp for two operational questions about a connector version:

- **Population** — how many actors are *pinned* (the applied audience) versus
  *eligible* for pinning (the potential audience), split by customer tier.
- **Health** — how many actors on the version are `healthy` / `unhealthy` /
  `awaiting` (no terminal job yet) / `disabled` (pinned but with no jobs in the
  window), built on the attempt/version primitive (the version stamped into
  `jobs.config` at job-creation time) rather than the current pin state.

The functions here accept already-fetched query rows and are side-effect free
apart from tier resolution via `tier_cache`, keeping them straightforward to
unit test. The SQL lives in `prod_db_access.sql` and the query wrappers in
`prod_db_access.queries`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

import google.auth.credentials

from airbyte_ops_mcp.tier_cache import (
    TierFilter,
    TierSummary,
    build_tier_summary,
    build_weighted_tier_summary,
    enrich_rows_by_org,
    filter_rows_by_tier,
)

_DEFAULT_TIER_FILTER: TierFilter = "TIER_2"


class ActorHealthState(StrEnum):
    """Tri-state health classification for a single actor on a version."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


def classify_actor_health(
    succeeded_jobs: int,
    failed_jobs: int,
) -> ActorHealthState:
    """Classify an actor's health from its job counts over the lookback window.

    - `healthy`: at least one successful sync — a positive success signal, the
      same signal the autopilot health gate uses (`actors_with_successful_syncs`).
    - `unhealthy`: no successes but at least one failure.
    - `unknown`: neither succeeded nor failed — the actor ran only non-terminal
      jobs, or (when applied to a pinned actor with no jobs at all) has not yet
      produced enough signal to judge.
    """
    if succeeded_jobs > 0:
        return ActorHealthState.HEALTHY
    if failed_jobs > 0:
        return ActorHealthState.UNHEALTHY
    return ActorHealthState.UNKNOWN


@dataclass
class VersionHealthSummary:
    """Four-bucket health rollup for the actors on a connector version.

    - `healthy` / `unhealthy`: actors that ran the version and produced a
      terminal signal (a success, or only failures).
    - `awaiting`: actors that ran but produced no terminal outcome yet (only
      non-terminal jobs in the window).
    - `disabled`: actors pinned to the version that produced no jobs at all in
      the window — the dormant/inactive audience folded in from
      `pinned_actor_rows`. (The data can't perfectly separate a truly-disabled
      connection from an active one that simply didn't run in the window.)
    """

    healthy: int
    unhealthy: int
    awaiting: int
    disabled: int
    total_actors: int
    healthy_by_tier: TierSummary
    unhealthy_by_tier: TierSummary
    awaiting_by_tier: TierSummary
    disabled_by_tier: TierSummary


@dataclass
class PopulationSummary:
    """Applied vs potential audience for a connector definition, by tier.

    - `active_by_tier`: all active actors of the definition (the full fleet).
    - `pinned_any_by_tier`: active actors with an effective pin at any scope to
      *any* version.
    - `eligible_by_tier`: active actors with no effective pin at all
      (`active - pinned_any`) — the unpinned population available to pin.
    - `pinned_to_version_by_tier`: actors pinned to a specific version from the
      `pinned_version_rows` scan (not active-filtered; includes dormant actors).
    - `addressable_by_tier`: active actors *not* pinned to a different version
      (`active - (pinned_any - pinned_to_target_active)`) — the correct
      denominator for a specific-version rollout, since actors pinned elsewhere
      are not candidates for this rollout. Only populated when the population
      rows carry `pinned_to_version_count` (a `target_version_id` was queried).
    - `pinned_to_version_active_by_tier`: active actors whose effective pin is
      the target version — the numerator that pairs with `addressable_by_tier`
      (`pinned_to_version_active <= addressable`). Same gating as above.
    The remaining factors are surfaced distinctly (not collapsed) so the caller
    can show how each denominator is built. All require a `target_version_id`:

    - `off_version_pinned_by_tier`: active actors effectively pinned to a
      *different* version (`pinned_any - pinned_to_version`). These are excluded
      from the rollout's addressable audience.
    - `gate_pass_by_tier`: *unpinned* active actors that pass the platform's
      `filterByJobStatus` gate (most-recent sync since the rollout's
      `created_at` succeeded and none failed).
    - `gate_excluded_failed_by_tier`: unpinned active actors with >=1 recent
      failed sync.
    - `gate_excluded_no_recent_sync_by_tier`: unpinned active actors with no
      qualifying sync in the window. These three partition the unpinned set
      (`gate_pass + failed + no_recent_sync = eligible_by_tier`).
    - `addressable_gated_by_tier`: `gate_pass + pinned_to_version` — reproduces
      the backend's `nActorsEligibleOrAlreadyPinned`, the platform's realized
      denominator (as opposed to `addressable_by_tier`, the honest active-fleet
      denominator). Both are surfaced so the two methodologies can be compared.

    The `gate_*` and `addressable_gated_by_tier` factors are only populated when
    `summarize_population` is called with `job_gated=True` (a rollout window was
    supplied).
    """

    active_by_tier: TierSummary
    pinned_any_by_tier: TierSummary
    eligible_by_tier: TierSummary
    pinned_to_version_by_tier: TierSummary | None = None
    addressable_by_tier: TierSummary | None = None
    pinned_to_version_active_by_tier: TierSummary | None = None
    off_version_pinned_by_tier: TierSummary | None = None
    gate_pass_by_tier: TierSummary | None = None
    gate_excluded_failed_by_tier: TierSummary | None = None
    gate_excluded_no_recent_sync_by_tier: TierSummary | None = None
    addressable_gated_by_tier: TierSummary | None = None


def summarize_version_health(
    health_rows: list[dict[str, Any]],
    pinned_actor_rows: list[dict[str, Any]] | None = None,
    tier_filter: TierFilter = _DEFAULT_TIER_FILTER,
) -> VersionHealthSummary:
    """Roll up per-actor health rows into four-bucket counts, split by tier.

    `health_rows` come from `query_version_actor_health` — one row per actor
    that ran the version in the window, each classified via
    `classify_actor_health` into `healthy`, `unhealthy`, or `awaiting` (ran but
    only non-terminal jobs). When `pinned_actor_rows` (from
    `query_actors_pinned_to_version`) are supplied, pinned actors that produced
    no jobs at all in the window are folded in as `disabled` (the dormant
    audience), so the denominator reflects the full intended audience.

    `tier_filter` restricts which customer tiers are counted (defaults to
    `TIER_2` per the repo's tier-safety convention; pass `ALL` for every tier).
    """
    # Copy each row before enrichment: `enrich_rows_by_org` adds keys in place, so
    # copying keeps this roll-up side-effect free w.r.t. the caller's `health_rows`.
    enriched = filter_rows_by_tier(
        enrich_rows_by_org([dict(row) for row in health_rows]), tier_filter
    )
    buckets: dict[ActorHealthState, list[dict[str, Any]]] = {
        ActorHealthState.HEALTHY: [],
        ActorHealthState.UNHEALTHY: [],
        ActorHealthState.UNKNOWN: [],
    }
    for row in enriched:
        state = classify_actor_health(
            int(row.get("succeeded_jobs", 0)),
            int(row.get("failed_jobs", 0)),
        )
        buckets[state].append(row)

    disabled_rows: list[dict[str, Any]] = []
    if pinned_actor_rows:
        seen = {str(row.get("actor_id")) for row in enriched}
        missing_by_actor: dict[str, dict[str, Any]] = {}
        for row in pinned_actor_rows:
            actor_id = str(row.get("actor_id"))
            if actor_id not in seen and actor_id not in missing_by_actor:
                # Copy so tier enrichment below doesn't mutate the caller's rows.
                missing_by_actor[actor_id] = dict(row)
        disabled_rows = filter_rows_by_tier(
            enrich_rows_by_org(list(missing_by_actor.values())),
            tier_filter,
        )

    healthy_rows = buckets[ActorHealthState.HEALTHY]
    unhealthy_rows = buckets[ActorHealthState.UNHEALTHY]
    awaiting_rows = buckets[ActorHealthState.UNKNOWN]
    return VersionHealthSummary(
        healthy=len(healthy_rows),
        unhealthy=len(unhealthy_rows),
        awaiting=len(awaiting_rows),
        disabled=len(disabled_rows),
        total_actors=(
            len(healthy_rows)
            + len(unhealthy_rows)
            + len(awaiting_rows)
            + len(disabled_rows)
        ),
        healthy_by_tier=build_tier_summary(healthy_rows),
        unhealthy_by_tier=build_tier_summary(unhealthy_rows),
        awaiting_by_tier=build_tier_summary(awaiting_rows),
        disabled_by_tier=build_tier_summary(disabled_rows),
    )


def summarize_population(
    population_rows: list[dict[str, Any]],
    pinned_version_rows: list[dict[str, Any]] | None = None,
    tier_filter: TierFilter = _DEFAULT_TIER_FILTER,
    *,
    job_gated: bool = False,
    has_target_version: bool | None = None,
    credentials: google.auth.credentials.Credentials | None = None,
) -> PopulationSummary:
    """Roll up per-org population rows into applied vs potential counts, by tier.

    `population_rows` come from `query_actor_population_by_org` — one row per
    organization with `actor_count` (active actors of the definition) and
    `pinned_actor_count` (those with an effective pin at any scope). Eligible
    (unpinned, available to pin) is derived per org as the difference. When the
    population query was run with a `target_version_id`, the version-aware
    summaries — `addressable_by_tier` (active actors not pinned to a *different*
    version) and `pinned_to_version_active_by_tier` (active actors pinned to the
    target version) — are populated too. When `pinned_version_rows` (from
    `query_actors_pinned_to_version`) are supplied, they are summarized
    separately as the full applied audience for a specific version (including
    dormant actors).

    `has_target_version` states whether a `target_version_id` was queried, which
    is what gates the version-aware summaries. Pass it explicitly from the
    caller that ran the query: the `SELECT_*_ACTOR_POPULATION_BY_ORG` statements
    *always* select `pinned_to_version_count` (it is `0` when no target was
    bound), so its presence in a row is not a reliable signal. When left `None`
    it falls back to sniffing that key — correct only for hand-built rows in
    tests, never for real query output.

    `tier_filter` restricts which customer tiers are counted (defaults to
    `TIER_2` per the repo's tier-safety convention; pass `ALL` for every tier).

    `credentials` are optional GCP credentials for the BigQuery-backed tier
    refresh (e.g. a per-user OAuth token); falls back to the default identity.
    """
    # Copy each row before enrichment: `enrich_rows_by_org` adds keys in place and the
    # loop below stamps derived counts, so copying keeps the caller's `population_rows`
    # untouched and this roll-up effectively pure.
    enriched = filter_rows_by_tier(
        enrich_rows_by_org(
            [dict(row) for row in population_rows], credentials=credentials
        ),
        tier_filter,
    )
    if has_target_version is None:
        # No explicit signal: fall back to sniffing the raw `population_rows`
        # (not the tier-filtered `enriched` rows, so a filter that drops every
        # row can't masquerade as "no target version"). Real callers should pass
        # `has_target_version` explicitly — the query always selects
        # `pinned_to_version_count`, so key presence alone is always `True` for
        # query output. This fallback exists for hand-built rows in tests.
        has_target_version = any(
            "pinned_to_version_count" in row for row in population_rows
        )
    for row in enriched:
        actor_count = int(row.get("actor_count", 0))
        pinned = int(row.get("pinned_actor_count", 0))
        pinned_to_version = int(row.get("pinned_to_version_count", 0))
        eligible_gated = int(row.get("eligible_gated_count", 0))
        row["eligible_count"] = max(actor_count - pinned, 0)
        # Active actors pinned to a *different* version (`pinned - pinned_to_version`),
        # excluded from the rollout's addressable audience.
        row["off_version_pinned_count"] = max(pinned - pinned_to_version, 0)
        # Active actors not pinned to a *different* version: exclude the
        # off-version pins from the active fleet.
        row["addressable_count"] = max(actor_count - (pinned - pinned_to_version), 0)
        # Job-gated addressable: unpinned actors that pass the platform's
        # `filterByJobStatus` gate, plus actors already pinned to the rollout
        # version (the backend counts already-pinned actors regardless of job
        # status). This mirrors the platform's `nActorsEligibleOrAlreadyPinned`.
        row["addressable_gated_count"] = eligible_gated + pinned_to_version

    pinned_to_version_by_tier: TierSummary | None = None
    if pinned_version_rows is not None:
        pinned_to_version_by_tier = build_tier_summary(
            filter_rows_by_tier(
                enrich_rows_by_org(
                    [dict(row) for row in pinned_version_rows],
                    credentials=credentials,
                ),
                tier_filter,
            )
        )

    addressable_by_tier: TierSummary | None = None
    pinned_to_version_active_by_tier: TierSummary | None = None
    off_version_pinned_by_tier: TierSummary | None = None
    gate_pass_by_tier: TierSummary | None = None
    gate_excluded_failed_by_tier: TierSummary | None = None
    gate_excluded_no_recent_sync_by_tier: TierSummary | None = None
    addressable_gated_by_tier: TierSummary | None = None
    if has_target_version:
        addressable_by_tier = build_weighted_tier_summary(enriched, "addressable_count")
        pinned_to_version_active_by_tier = build_weighted_tier_summary(
            enriched, "pinned_to_version_count"
        )
        off_version_pinned_by_tier = build_weighted_tier_summary(
            enriched, "off_version_pinned_count"
        )
        if job_gated:
            # The three job-status factors partition the unpinned population and
            # are surfaced distinctly so the caller can show every factor.
            gate_pass_by_tier = build_weighted_tier_summary(
                enriched, "eligible_gated_count"
            )
            gate_excluded_failed_by_tier = build_weighted_tier_summary(
                enriched, "gate_excluded_failed_count"
            )
            gate_excluded_no_recent_sync_by_tier = build_weighted_tier_summary(
                enriched, "gate_excluded_no_recent_sync_count"
            )
            addressable_gated_by_tier = build_weighted_tier_summary(
                enriched, "addressable_gated_count"
            )

    return PopulationSummary(
        active_by_tier=build_weighted_tier_summary(enriched, "actor_count"),
        pinned_any_by_tier=build_weighted_tier_summary(enriched, "pinned_actor_count"),
        eligible_by_tier=build_weighted_tier_summary(enriched, "eligible_count"),
        pinned_to_version_by_tier=pinned_to_version_by_tier,
        addressable_by_tier=addressable_by_tier,
        pinned_to_version_active_by_tier=pinned_to_version_active_by_tier,
        off_version_pinned_by_tier=off_version_pinned_by_tier,
        gate_pass_by_tier=gate_pass_by_tier,
        gate_excluded_failed_by_tier=gate_excluded_failed_by_tier,
        gate_excluded_no_recent_sync_by_tier=gate_excluded_no_recent_sync_by_tier,
        addressable_gated_by_tier=addressable_gated_by_tier,
    )


@dataclass
class SyncInfoSummary:
    """Health + population rollup derived from a `get_actor_sync_info` response.

    This is the cheapest correct path for an *active rollout*: the platform API
    already filters syncs to the RC version and returns per-actor success/failure
    counts plus selection totals, so no prod-DB scan is needed. It is not
    tier-split (the API response carries no org/tier), so use the DB-backed
    `summarize_version_health` / `summarize_population` when a tier breakdown is
    required.
    """

    num_actors: int
    num_pinned: int
    num_eligible: int
    healthy: int
    unhealthy: int
    awaiting: int
    disabled: int


def _sync_info_int(value: Any) -> int:
    """Coerce a possibly-`None` API numeric field to an `int`."""
    return int(value) if value else 0


def summarize_sync_info(sync_info: dict[str, Any]) -> SyncInfoSummary:
    """Roll up a `get_actor_sync_info` response into health + population counts.

    Tolerant of camelCase and snake_case keys (matching the autopilot health
    gate). Per-actor health uses the same success signal as the gate, split into
    four buckets over the rollout's full pinned set:

    - `healthy`: at least one succeeded sync of the RC version.
    - `unhealthy`: failures and no successes.
    - `awaiting`: ran in the window but has no terminal outcome yet (only
      non-terminal jobs / in progress).
    - `disabled`: pinned to the rollout but produced no syncs in the window —
      the dormant/inactive majority, computed as `num_pinned` minus the actors
      that ran at all. (The data can't perfectly separate a truly-disabled
      connection from an active one that simply didn't sync in the window.)

    The four buckets sum to `num_pinned` (the rollout's full pinned set), so the
    health line intentionally does not match the active-only `pinned` count on
    the rollout line — `disabled` is exactly that gap.
    """
    data = sync_info.get("data", sync_info)
    selection_info = (
        data.get("actorSelectionInfo") or data.get("actor_selection_info") or {}
    )
    num_actors = _sync_info_int(
        selection_info.get("numActors") or selection_info.get("num_actors")
    )
    num_pinned = _sync_info_int(
        selection_info.get("numPinnedToConnectorRollout")
        or selection_info.get("num_pinned_to_connector_rollout")
    )
    num_eligible = _sync_info_int(
        selection_info.get("numActorsEligibleOrAlreadyPinned")
        or selection_info.get("num_actors_eligible_or_already_pinned")
    )
    syncs_map: dict[str, Any] = data.get("syncs", {}) or {}

    healthy = 0
    unhealthy = 0
    awaiting = 0
    for actor_stats in syncs_map.values():
        succeeded = _sync_info_int(
            actor_stats.get("numSucceeded") or actor_stats.get("num_succeeded")
        )
        failed = _sync_info_int(
            actor_stats.get("numFailed") or actor_stats.get("num_failed")
        )
        state = classify_actor_health(succeeded, failed)
        if state is ActorHealthState.HEALTHY:
            healthy += 1
        elif state is ActorHealthState.UNHEALTHY:
            unhealthy += 1
        else:
            awaiting += 1
    disabled = max(num_pinned - healthy - unhealthy - awaiting, 0)
    return SyncInfoSummary(
        num_actors=num_actors,
        num_pinned=num_pinned,
        num_eligible=num_eligible,
        healthy=healthy,
        unhealthy=unhealthy,
        awaiting=awaiting,
        disabled=disabled,
    )
