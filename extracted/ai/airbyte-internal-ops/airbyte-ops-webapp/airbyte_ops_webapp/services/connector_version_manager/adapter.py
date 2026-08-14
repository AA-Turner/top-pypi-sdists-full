"""Adapters for connector version pinning workflows."""

from __future__ import annotations

import contextlib
import json
from collections.abc import Callable, Mapping
from dataclasses import asdict
from datetime import datetime

import sqlalchemy.exc
from airbyte import constants
from airbyte.exceptions import PyAirbyteInputError
from airbyte_ops_mcp.cloud_admin import api_client
from airbyte_ops_mcp.cloud_admin.payment_config import (
    PaymentConfigAPIError,
    get_organization_info,
)
from airbyte_ops_mcp.cloud_admin.registry_lookup import (
    _fetch_cloud_registry,
    resolve_canonical_name_to_definition_id,
    resolve_definition_id_to_registry_info,
)
from airbyte_ops_mcp.cloud_admin.version_overrides import (
    ResolvedCloudAuth,
    VersionOverrideTarget,
    set_version_override,
)
from airbyte_ops_mcp.connector_ops.rollouts.constants import CustomerTier
from airbyte_ops_mcp.gcp_auth import get_gcp_credentials_for_tier_gcs_ro
from airbyte_ops_mcp.prod_db_access.queries import (
    query_actor_population_by_org,
    query_connector_rollout_siblings,
    query_connector_rollouts,
    query_connector_rollouts_for_connector,
    query_connector_versions,
    query_new_connector_releases,
    query_org_connector_pins,
    query_org_pin_stats,
    query_raw_pins_for_version,
    query_rollout_pinned_actor_sync_by_version,
    query_versions_with_pins,
)
from airbyte_ops_mcp.registry._constants import PROD_METADATA_SERVICE_BUCKET_NAME
from airbyte_ops_mcp.registry.progressive_rollout_marker import (
    ProgressiveRolloutMarkerAnnotationResult,
    annotate_progressive_rollout_marker,
    get_progressive_rollout_marker,
)
from airbyte_ops_mcp.registry.yank import get_yank_marker, list_yanked_versions
from airbyte_ops_mcp.tier_cache import (
    enrich_rows_by_org,
    filter_rows_by_tier,
    resolve_workspace,
)
from airbyte_ops_mcp.version_summaries import (
    PopulationSummary,
    TierSummary,
    summarize_population,
)

from airbyte_ops_webapp.models import (
    ConnectorOption,
    ConnectorPopulation,
    ConnectorRelease,
    ConnectorRollout,
    ConnectorType,
    ConnectorVersion,
    ContextResolution,
    CurrentVersionState,
    OperationPreview,
    OperationResult,
    OverridePlan,
    ProgressiveRolloutMarkerDetail,
    RolloutSyncSummary,
    ScopedConfiguration,
    ScopeType,
    TierPopulationFactors,
    VersionPinRow,
    YankedVersionRow,
    YankMarkerDetail,
    build_version_override_payload,
    version_override_tool_name,
)

__all__ = [
    "OpsMcpAdapter",
    "configuration_rows",
    "operation_result_to_json",
    "preview_to_json",
]

SCOPE_PRIORITY: dict[ScopeType, int] = {
    "organization": 0,
    "workspace": 1,
    "actor": 2,
}
REQUIRED_APPROVAL_FIELDS: tuple[str, ...] = (
    "override_reason",
    "override_reason_reference_url",
    "customer_tier_filter",
)
SAFE_PREVIEW_WARNINGS: tuple[str, ...] = (
    "Preview only: no connector version override has been executed.",
    "TIER_0 and TIER_1 customers require human escalation before action.",
)
CONTEXT_RESOLUTION_MISS_STATUS_CODES: frozenset[int] = frozenset({400, 404, 422})

CLOUD_UI_BASE_URL = "https://cloud.airbyte.com"


def _fmt_date(value: str) -> str:
    """Format an ISO datetime string to `yyyy-mm-dd (ddd)`."""
    if not value:
        return ""
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    return parsed.strftime("%Y-%m-%d (%a)")


def _cloud_scope_url(
    *,
    scope_type: str,
    scope_id: str,
    workspace_id: str = "",
    actor_type: str = "",
) -> str:
    """Build an Airbyte Cloud URL for viewing the target scope."""
    if scope_type == "workspace":
        return f"{CLOUD_UI_BASE_URL}/workspaces/{scope_id}"
    if scope_type == "organization":
        return f"{CLOUD_UI_BASE_URL}/organization/{scope_id}/settings/organization"
    if scope_type == "actor":
        if not workspace_id:
            raise ValueError(
                f"Actor scope URL requires workspace_id (actor_id={scope_id})."
            )
        if actor_type not in ("source", "destination"):
            raise ValueError(
                f"Actor scope URL requires actor_type 'source' or 'destination'"
                f" (got {actor_type!r})."
            )
        return f"{CLOUD_UI_BASE_URL}/workspaces/{workspace_id}/{actor_type}/{scope_id}"
    raise ValueError(f"Unknown scope_type {scope_type!r}.")


def _select_tier_2(tier_summary: TierSummary | None) -> int:
    """Read a `TierSummary`'s TIER_2 count (`0` when the summary is absent)."""
    return tier_summary.tier_2_count if tier_summary is not None else 0


def _select_tier_1(tier_summary: TierSummary | None) -> int:
    """Read a `TierSummary`'s TIER_1 count (`0` when the summary is absent)."""
    return tier_summary.tier_1_count if tier_summary is not None else 0


def _select_tier_0(tier_summary: TierSummary | None) -> int:
    """Read a `TierSummary`'s TIER_0 count (`0` when the summary is absent)."""
    return tier_summary.tier_0_count if tier_summary is not None else 0


def _tier_population_factors(
    summary: PopulationSummary,
    select: Callable[[TierSummary | None], int],
) -> TierPopulationFactors | None:
    """Assemble one tier's distinct population factors from a `PopulationSummary`.

    `select` picks the relevant tier count from each by-tier summary. Every
    factor is surfaced (nothing collapsed) so the UI can show how both the
    addressable and the backend-eligible denominators are built.

    Returns `None` when no rollout window enabled the job-status gate
    (`addressable_gated_by_tier is None`). In that case the `gate_*` counts are
    all `0`, so a factor-driven card would compute `eligible = pinned` and bury
    the unpinned audience under `no recent sync` — inconsistent with the
    headline eligible, which falls back to `addressable` (active minus
    off-version). Returning `None` makes the card fall back to that same
    headline count instead of inventing a gate breakdown the data can't
    support.
    """
    gated = summary.addressable_gated_by_tier
    if gated is None:
        return None
    active = select(summary.active_by_tier)
    pinned = select(summary.pinned_to_version_active_by_tier)
    off_version = select(summary.off_version_pinned_by_tier)
    addressable_gated = select(gated)
    return TierPopulationFactors(
        active=active,
        pinned_to_rollout=pinned,
        off_version_pinned=off_version,
        unpinned=max(active - pinned - off_version, 0),
        gate_pass=select(summary.gate_pass_by_tier),
        gate_excluded_failed=select(summary.gate_excluded_failed_by_tier),
        gate_excluded_no_recent_sync=select(
            summary.gate_excluded_no_recent_sync_by_tier
        ),
        addressable=select(summary.addressable_by_tier),
        addressable_gated=addressable_gated,
    )


class OpsMcpAdapter:
    """Adapter backed by `airbyte-internal-ops` APIs."""

    mode = "real"

    def __init__(
        self,
        *,
        bearer_token: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        config_api_root: str = constants.CLOUD_CONFIG_API_ROOT,
    ) -> None:
        self.bearer_token = bearer_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.config_api_root = config_api_root

    def search_connectors(self, query: str) -> tuple[ConnectorOption, ...]:
        """Resolve a connector name or definition ID into connector options."""
        normalized_query = query.strip()
        if not normalized_query:
            return self.list_connectors()

        connectors: list[ConnectorOption] = []
        connector_by_id = self._connector_from_definition_id(normalized_query)
        if connector_by_id:
            connectors.append(connector_by_id)

        connector_by_name = self._connector_from_name(normalized_query)
        if connector_by_name and connector_by_name not in connectors:
            connectors.append(connector_by_name)

        if connectors:
            return tuple(connectors)

        return self.list_connectors(normalized_query)

    def list_connectors(self, query: str = "") -> tuple[ConnectorOption, ...]:
        """List Cloud registry connectors, optionally filtered by `query`."""
        if self._is_local_config_api:
            return self._list_local_connectors(query)
        data = _fetch_cloud_registry(from_gcs=True)
        connectors = [
            *(
                self._connector_from_registry_entry(source, "source")
                for source in data.get("sources", [])
                if isinstance(source, Mapping)
            ),
            *(
                self._connector_from_registry_entry(destination, "destination")
                for destination in data.get("destinations", [])
                if isinstance(destination, Mapping)
            ),
        ]
        normalized_query = query.strip().lower()
        if not normalized_query:
            return tuple(sorted(connectors, key=lambda connector: connector.name))
        return tuple(
            connector
            for connector in sorted(connectors, key=lambda connector: connector.name)
            if normalized_query in connector.name.lower()
            or normalized_query in connector.id.lower()
            or normalized_query in connector.docker_repository.lower()
        )

    def get_connector(self, connector_id: str) -> ConnectorOption:
        """Return a connector by definition ID."""
        if self._is_local_config_api:
            for connector in self.list_connectors():
                if connector.id == connector_id:
                    return connector
        connector = self._connector_from_definition_id(connector_id)
        if connector:
            return connector
        raise ValueError(f"Unknown connector ID: {connector_id}")

    def list_versions(self, connector_id: str) -> tuple[ConnectorVersion, ...]:
        """List published versions for a connector definition."""
        if self._is_local_config_api:
            connector = self.get_connector(connector_id)
            return (
                ConnectorVersion(
                    version_id=api_client.resolve_connector_version_id(
                        actor_definition_id=connector.id,
                        connector_type=connector.connector_type,
                        version=connector.latest_version,
                        config_api_root=self.config_api_root,
                        client_id=self.client_id,
                        client_secret=self.client_secret,
                        bearer_token=self.bearer_token,
                    ),
                    docker_image_tag=connector.latest_version,
                    docker_repository=connector.docker_repository,
                    release_stage="",
                    support_level="",
                    cdk_version="",
                    language="",
                    last_published="",
                ),
            )
        return tuple(
            self._version_from_row(row)
            for row in query_connector_versions(connector_definition_id=connector_id)
        )

    def list_recent_releases(
        self,
        *,
        days: int = 30,
        limit: int | None = None,
    ) -> tuple[ConnectorRelease, ...]:
        """List recent published releases across connectors."""
        release_rows = query_new_connector_releases(days=days, limit=limit)
        return tuple(self._release_from_row(row) for row in release_rows)

    def list_active_rollouts(
        self,
        connector_id: str,
    ) -> tuple[ConnectorRollout, ...]:
        """List active progressive rollouts for a connector definition."""
        rollout_rows = query_connector_rollouts_for_connector(
            actor_definition_id=connector_id,
            active_only=True,
        )
        return tuple(self._rollout_from_row(row) for row in rollout_rows)

    def list_active_rollouts_with_siblings(
        self,
        connector_id: str,
    ) -> tuple[ConnectorRollout, ...]:
        """List active rollouts and all sibling tiers for a connector's RCs."""
        active_rows = query_connector_rollouts_for_connector(
            actor_definition_id=connector_id,
            active_only=True,
        )
        pairs = [
            (
                str(row.get("actor_definition_id") or ""),
                str(row.get("release_candidate_version_id") or ""),
            )
            for row in active_rows
            if row.get("actor_definition_id")
            and row.get("release_candidate_version_id")
        ]
        sibling_rows = query_connector_rollout_siblings(pairs)
        rows_by_id = {
            str(row.get("rollout_id") or ""): row
            for row in sibling_rows + active_rows
            if row.get("rollout_id")
        }
        rows_by_pair: dict[tuple[str, str], list[Mapping[str, object]]] = {}
        for row in sibling_rows:
            pair = (
                str(row.get("actor_definition_id") or ""),
                str(row.get("release_candidate_version_id") or ""),
            )
            rows_by_pair.setdefault(pair, []).append(row)
        return tuple(
            self._rollout_from_row(
                row,
                sibling_rows=rows_by_pair.get(
                    (
                        str(row.get("actor_definition_id") or ""),
                        str(row.get("release_candidate_version_id") or ""),
                    ),
                    [],
                ),
            )
            for row in rows_by_id.values()
        )

    def list_progressive_rollouts(
        self,
        *,
        limit: int | None = None,
    ) -> tuple[ConnectorRollout, ...]:
        """List active progressive rollouts across connector definitions."""
        rollout_rows = query_connector_rollouts(active_only=True, limit=limit)
        return tuple(self._rollout_from_row(row) for row in rollout_rows)

    def list_progressive_rollouts_with_siblings(
        self,
        *,
        limit: int | None = None,
    ) -> tuple[ConnectorRollout, ...]:
        """List active rollouts and all sibling tiers for their RCs."""
        active_rows = query_connector_rollouts(active_only=True, limit=limit)
        pairs = [
            (
                str(row.get("actor_definition_id") or ""),
                str(row.get("release_candidate_version_id") or ""),
            )
            for row in active_rows
            if row.get("actor_definition_id")
            and row.get("release_candidate_version_id")
        ]
        sibling_rows = query_connector_rollout_siblings(pairs)
        rows_by_id = {
            str(row.get("rollout_id") or ""): row
            for row in sibling_rows + active_rows
            if row.get("rollout_id")
        }
        rows_to_parse = list(rows_by_id.values())
        rows_by_pair: dict[tuple[str, str], list[Mapping[str, object]]] = {}
        for row in sibling_rows:
            pair = (
                str(row.get("actor_definition_id") or ""),
                str(row.get("release_candidate_version_id") or ""),
            )
            rows_by_pair.setdefault(pair, []).append(row)
        return tuple(
            self._rollout_from_row(
                row,
                sibling_rows=rows_by_pair.get(
                    (
                        str(row.get("actor_definition_id") or ""),
                        str(row.get("release_candidate_version_id") or ""),
                    ),
                    [],
                ),
            )
            for row in rows_to_parse
        )

    def list_version_pins(
        self,
        version_id: str,
        *,
        limit: int = 25,
        offset: int = 0,
    ) -> tuple[list[VersionPinRow], int]:
        """Return pins for a specific connector version from prod DB.

        Returns a tuple of (pin_rows, total_count). Uses raw
        `scoped_configuration` entries so the total matches the Pinned
        Versions tab's pin_count aggregation.
        """
        raw_rows = query_raw_pins_for_version(version_id)
        total = len(raw_rows)
        page = raw_rows[offset : offset + limit]
        pins = [self._pin_row_from_db(row) for row in page]
        return pins, total

    def get_rollout_sync_summary(
        self,
        rollout_id: str,
        *,
        tier: str = "",
        is_destination: bool,
    ) -> RolloutSyncSummary:
        """Build health + population summaries for an active rollout.

        Reads the replica-backed actor sync rows, applies the cached customer-tier
        filter, and computes the webapp aggregate. Returns empty counts when
        `rollout_id` is missing or a query fails.
        """
        if not rollout_id:
            return RolloutSyncSummary()
        try:
            rollout_rows: list[dict[str, object]] | None = None
            if not tier:
                rollout_rows = query_connector_rollouts(rollout_id=rollout_id)
                rollout = rollout_rows[0] if rollout_rows else {}
                tier = str(rollout.get("tag") or "")
                if not tier:
                    rollout_filters = rollout.get("filters")
                    tier = (
                        self._tier_from_filters(rollout_filters)
                        if rollout_filters
                        else "ALL"
                    )
            tier = tier or "ALL"
            rollout_parameters = self._resolve_rollout_sync_parameters(
                rollout_id,
                rollout_rows=rollout_rows,
            )
            if rollout_parameters is None:
                return RolloutSyncSummary()
            enriched_rows = self._get_rollout_sync_rows(
                rollout_parameters,
                is_destination=is_destination,
            )
        except (sqlalchemy.exc.SQLAlchemyError, RuntimeError, ValueError):
            return RolloutSyncSummary()
        if tier == "ALL":
            return self._rollout_sync_summary_from_rows(enriched_rows)
        return self._rollout_sync_summary_from_rows(
            filter_rows_by_tier(enriched_rows, tier)
        )

    def get_rollout_sync_summaries_by_tier(
        self,
        rollout_id: str,
        *,
        is_destination: bool,
    ) -> dict[str, RolloutSyncSummary]:
        """Return one replica-backed rollout summary per customer tier."""
        try:
            rollout_parameters = self._resolve_rollout_sync_parameters(rollout_id)
            if rollout_parameters is None:
                return {}
            enriched_rows = self._get_rollout_sync_rows(
                rollout_parameters,
                is_destination=is_destination,
            )
        except (sqlalchemy.exc.SQLAlchemyError, RuntimeError, ValueError):
            return {}
        rows_by_tier: dict[str, list[dict[str, object]]] = {}
        for row in enriched_rows:
            rows_by_tier.setdefault(
                str(row.get("customer_tier") or CustomerTier.TIER_2.value),
                [],
            ).append(row)
        return {
            tier: self._rollout_sync_summary_from_rows(rows)
            for tier, rows in rows_by_tier.items()
        }

    @staticmethod
    def _resolve_rollout_sync_parameters(
        rollout_id: str,
        *,
        rollout_rows: list[dict[str, object]] | None = None,
    ) -> tuple[str, str, datetime] | None:
        rollout_rows = (
            rollout_rows
            if rollout_rows is not None
            else query_connector_rollouts(rollout_id=rollout_id)
        )
        if not rollout_rows:
            return None
        rollout = rollout_rows[0]
        actor_definition_id = str(rollout.get("actor_definition_id") or "")
        release_candidate_version_id = str(
            rollout.get("release_candidate_version_id") or ""
        )
        if not actor_definition_id or not release_candidate_version_id:
            return None
        rollout_created_at = rollout.get("earliest_created_at")
        if rollout_created_at is None:
            return None
        return (
            actor_definition_id,
            release_candidate_version_id,
            rollout_created_at,
        )

    @staticmethod
    def _get_rollout_sync_rows(
        rollout_parameters: tuple[str, str, datetime],
        *,
        is_destination: bool,
    ) -> list[dict[str, object]]:
        pinned_rows = query_rollout_pinned_actor_sync_by_version(
            *rollout_parameters,
            is_destination=is_destination,
        )
        gcs_credentials = get_gcp_credentials_for_tier_gcs_ro()
        return enrich_rows_by_org(
            rows=[dict(row) for row in pinned_rows],
            credentials=gcs_credentials,
            allow_degraded=False,
        )

    @staticmethod
    def _rollout_sync_summary_from_rows(
        tier_pinned_rows: list[dict[str, object]],
    ) -> RolloutSyncSummary:
        if not tier_pinned_rows:
            return RolloutSyncSummary()
        healthy_count = sum(
            int(row.get("num_connections_succeeded", 0) or 0) > 0
            for row in tier_pinned_rows
        )
        unhealthy_count = sum(
            int(row.get("num_connections_succeeded", 0) or 0) == 0
            and int(row.get("num_connections_failed", 0) or 0) > 0
            for row in tier_pinned_rows
        )
        awaiting_count = sum(
            bool(row.get("has_connection_on_rollout_version"))
            and int(row.get("num_connections_succeeded", 0) or 0) == 0
            and int(row.get("num_connections_failed", 0) or 0) == 0
            for row in tier_pinned_rows
        )
        disabled_count = sum(
            not bool(row.get("has_connection_on_rollout_version"))
            for row in tier_pinned_rows
        )
        health = (
            f"{healthy_count} healthy | "
            f"{unhealthy_count} unhealthy | "
            f"{awaiting_count} awaiting | "
            f"{disabled_count} disabled"
        )
        return RolloutSyncSummary(
            health=health,
            num_pinned=len(tier_pinned_rows),
            num_healthy=healthy_count,
            num_unhealthy=unhealthy_count,
        )

    def get_connector_population(
        self,
        connector_definition_id: str,
        *,
        is_destination: bool,
        target_version_id: str = "",
        rollout_created_at: str = "",
    ) -> ConnectorPopulation:
        """Return the enabled (active-connection) actor population, by rollout tier.

        Backed by the DB `query_actor_population_by_org` + `summarize_population`
        path (cheap: aggregated per-org over `scoped_configuration` + actor /
        connection tables), counting only actors with at least one active
        connection. Provides the connector-wide `total_active` count for the
        single "Eligible Actors" line and the per-tier addressable (eligible)
        counts used to fill in tiers whose rollout has not started.

        The connector-wide `total_active` is a tier-independent aggregate summed
        directly from the population rows. The per-tier eligible split needs tier
        resolution, which reads the platform's GCS tier export under the webapp's
        runtime service account (ADC). Tier resolution failures raise rather than
        degrading to zero: silently returning `0 of 0` would misrepresent a real
        population as empty, so a GCS/credential error propagates and the page
        surfaces it instead of showing fabricated counts.

        Uses `tier_filter="ALL"` because the rollout card shows every tier; the
        result is aggregate counts only (no customer identities).
        """
        if not connector_definition_id:
            return ConnectorPopulation()
        # A rollout window enables the platform's job-status eligibility gate in
        # the query, so the webapp's denominator tracks the backend's rollout
        # audience rather than counting active actors the platform excludes.
        job_gated = bool(rollout_created_at)
        try:
            population_rows = query_actor_population_by_org(
                actor_definition_id=connector_definition_id,
                is_destination=is_destination,
                target_version_id=target_version_id or None,
                rollout_created_at=rollout_created_at or None,
            )
        except sqlalchemy.exc.SQLAlchemyError:
            return ConnectorPopulation()

        total_active = sum(int(row.get("actor_count", 0)) for row in population_rows)

        # Tier resolution reads the GCS tier export under the runtime service
        # account (ADC). A credential or read failure raises `GoogleAuthError` /
        # `RuntimeError`; we let it propagate rather than returning a zeroed
        # breakdown, so a real population is never misrepresented as `0 of 0`.
        gcs_credentials = get_gcp_credentials_for_tier_gcs_ro()
        summary = summarize_population(
            population_rows,
            tier_filter="ALL",
            job_gated=job_gated,
            has_target_version=bool(target_version_id),
            credentials=gcs_credentials,
        )

        # The `eligible` denominator is the tier's job-status-gated audience
        # (`addressable_gated_by_tier`, the backend's
        # `nActorsEligibleOrAlreadyPinned`): unpinned actors that pass the gate
        # plus actors already pinned to the rollout version. This matches the
        # platform's realized rollout denominator. Fall back to `addressable`
        # (active minus off-version pins) when no rollout window enabled the gate,
        # then to `active` when no target version is available. `pinned` is active
        # actors whose effective pin is *the rollout version*
        # (`pinned_to_version_active_by_tier`), so `pinned <= eligible` per tier.
        # Select on `is not None` rather than truthiness: a `TierSummary` is
        # always truthy (a Pydantic model with no `__bool__`), so a legitimately
        # zeroed summary must not fall through to the next fallback. The
        # version-aware fields are `None` exactly when no `target_version_id`
        # (and, for the gated field, no rollout window) was supplied.
        if summary.addressable_gated_by_tier is not None:
            eligible = summary.addressable_gated_by_tier
        elif summary.addressable_by_tier is not None:
            eligible = summary.addressable_by_tier
        else:
            eligible = summary.active_by_tier
        if summary.pinned_to_version_active_by_tier is not None:
            pinned = summary.pinned_to_version_active_by_tier
        else:
            pinned = summary.pinned_any_by_tier
        # Connector-wide gated-eligible total for the headline == sum of the
        # per-tier eligibles, so the "Eligible Actors" number reconciles with the
        # tier cards below it.
        total_eligible = (
            eligible.tier_2_count + eligible.tier_1_count + eligible.tier_0_count
        )
        return ConnectorPopulation(
            total_active=total_active,
            total_eligible=total_eligible,
            eligible_tier_2=eligible.tier_2_count,
            eligible_tier_1=eligible.tier_1_count,
            eligible_tier_0=eligible.tier_0_count,
            pinned_tier_2=pinned.tier_2_count,
            pinned_tier_1=pinned.tier_1_count,
            pinned_tier_0=pinned.tier_0_count,
            tier_resolution_available=True,
            factors_tier_2=_tier_population_factors(summary, _select_tier_2),
            factors_tier_1=_tier_population_factors(summary, _select_tier_1),
            factors_tier_0=_tier_population_factors(summary, _select_tier_0),
        )

    def list_versions_with_pins(self) -> list[dict[str, object]]:
        """Return connector versions that have at least one pin.

        Does not join `connector_rollout`, so each version appears exactly once.
        """
        return query_versions_with_pins()

    def list_org_pin_stats(
        self,
        organization_id: str,
    ) -> list[dict[str, object]]:
        """Return connector versions pinned anywhere under an organization.

        One aggregate row per pinned version, matching pins at the org,
        workspace, and actor scope levels within the organization.
        """
        return query_org_pin_stats(organization_id)

    def list_org_connector_pins(
        self,
        organization_id: str,
        *,
        pinned_version_id: str | None = None,
    ) -> list[dict[str, object]]:
        """Return the individual pins discovered under an organization.

        One row per `scoped_configuration` pin; pass `pinned_version_id` to
        restrict to a single pinned version.
        """
        return query_org_connector_pins(
            organization_id,
            pinned_version_id=pinned_version_id,
        )

    def list_yanked_versions(self) -> tuple[YankedVersionRow, ...]:
        """Return every yanked connector version from the prod registry bucket.

        Reads `version-yank.yml` markers from the coral prod GCS registry via
        `airbyte_ops_mcp.registry.yank.list_yanked_versions`, then resolves each
        connector's canonical name to its actor-definition UUID so rows are
        click-navigable. Connectors that cannot be resolved keep an empty
        `connector_id`.
        """
        return tuple(
            YankedVersionRow(
                connector_id=self._resolve_connector_id(marker.connector_name),
                connector_name=marker.connector_name,
                docker_image_tag=marker.version,
                yanked_at=marker.yanked_at,
                reason=marker.reason,
                approval_url=marker.approval_url,
            )
            for marker in list_yanked_versions(PROD_METADATA_SERVICE_BUCKET_NAME)
        )

    def get_yank_marker(
        self,
        connector_name: str,
        version: str,
    ) -> YankMarkerDetail | None:
        """Return the active yank marker for one version, or `None` if not yanked.

        Reads the version's `version-yank.yml` marker from the coral prod GCS
        registry via `airbyte_ops_mcp.registry.yank.get_yank_marker`, resolving
        the connector's canonical name to its actor-definition UUID so the
        detail stays associated with the selected connector.
        """
        marker = get_yank_marker(
            connector_name,
            version,
            PROD_METADATA_SERVICE_BUCKET_NAME,
        )
        if marker is None:
            return None
        return YankMarkerDetail(
            connector_id=self._resolve_connector_id(connector_name),
            connector_name=marker.connector_name,
            docker_image_tag=marker.version,
            yanked_at=marker.yanked_at,
            reason=marker.reason,
            approval_url=marker.approval_url,
            raw=marker.raw,
        )

    def get_progressive_rollout_marker(
        self,
        connector_name: str,
        version: str,
    ) -> ProgressiveRolloutMarkerDetail | None:
        """Return the active progressive rollout marker for one version."""
        marker = get_progressive_rollout_marker(
            connector_name,
            version,
            PROD_METADATA_SERVICE_BUCKET_NAME,
        )
        if marker is None:
            return None
        return ProgressiveRolloutMarkerDetail(
            connector_id=self._resolve_connector_id(connector_name),
            connector_name=marker.connector_name,
            docker_image_tag=marker.version,
            progressive_rollout=marker.progressive_rollout,
            created_at=marker.created_at,
            promotion_requested_at=marker.promotion_requested_at,
            promotion_requested_by=marker.promotion_requested_by,
            rollout_id=marker.rollout_id,
            raw=marker.raw,
            state=marker.state,
            marker_date=marker.marker_date,
        )

    def annotate_progressive_rollout_marker(
        self,
        connector_name: str,
        version: str,
        *,
        promotion_requested_by: str,
        rollout_id: str,
    ) -> ProgressiveRolloutMarkerAnnotationResult:
        """Annotate the active progressive rollout marker for one version."""
        return annotate_progressive_rollout_marker(
            connector_name=connector_name,
            version=version,
            bucket_name=PROD_METADATA_SERVICE_BUCKET_NAME,
            promotion_requested_by=promotion_requested_by,
            rollout_id=rollout_id,
        )

    @staticmethod
    def _resolve_connector_id(connector_name: str) -> str:
        """Resolve a connector's canonical name to its definition UUID.

        Returns an empty string when the connector is absent from the cloud
        registry (e.g. fully removed), leaving the yanked row non-navigable.
        """
        try:
            return resolve_canonical_name_to_definition_id(
                connector_name,
                from_gcs=True,
            )
        except PyAirbyteInputError:
            return ""

    @staticmethod
    def _pin_row_from_db(row: dict[str, object]) -> VersionPinRow:
        """Map a raw `scoped_configuration` row to a `VersionPinRow`.

        Actor-scope URLs are left empty because the DB row lacks
        `workspace_id`; the full URL is resolved on row click via
        `resolve_scope_guid`.
        """
        scope_type = str(row.get("pin_scope_type", "actor"))
        scope_id = str(row.get("scope_id", ""))
        origin_email = row.get("pinned_by_user_email") or row.get("pinned_by_user_name")
        origin_name = (
            str(origin_email) if origin_email else str(row.get("pinned_by_user_id", ""))
        )
        if scope_type in ("workspace", "organization"):
            scope_url = _cloud_scope_url(
                scope_type=scope_type,
                scope_id=scope_id,
            )
        else:
            scope_url = ""
        return VersionPinRow(
            scope_type=scope_type,
            scope_id=scope_id,
            scope_url=scope_url,
            origin_type=str(row.get("origin_type", "")),
            origin_name=origin_name,
            description=str(row.get("description", "")),
            created_at=str(row.get("created_at", "")),
            created_at_display=_fmt_date(str(row.get("created_at", ""))),
            expires_at=str(row.get("expires_at", "") or ""),
            expires_at_display=_fmt_date(str(row.get("expires_at", "") or "")),
            reference_url=str(row.get("reference_url", "") or ""),
            scope_name="",
        )

    def get_current_context(
        self,
        *,
        connector_id: str,
        scope_type: ScopeType,
        scope_id: str,
        workspace_id: str | None = None,
    ) -> CurrentVersionState:
        """Return current version context for a selected scope."""
        connector = self.get_connector(connector_id)
        latest_version = connector.latest_version
        if scope_type in ("workspace", "organization"):
            scoped_configs = self._scope_context(connector, scope_type, scope_id)
            active_config = self._active_config(scoped_configs, scope_type, scope_id)
            return CurrentVersionState(
                connector_id=connector.id,
                connector_name=connector.name,
                connector_type=connector.connector_type,
                latest_version=latest_version,
                active_version=active_config.value_name
                if active_config
                else latest_version,
                is_version_pinned=active_config is not None,
                active_scope=active_config.scope_type if active_config else None,
                active_scope_id=active_config.scope_id if active_config else None,
                ancestor_configurations=tuple(
                    config
                    for config in scoped_configs
                    if SCOPE_PRIORITY[config.scope_type] < SCOPE_PRIORITY[scope_type]
                ),
                descendant_configurations=tuple(
                    config
                    for config in scoped_configs
                    if SCOPE_PRIORITY[config.scope_type] > SCOPE_PRIORITY[scope_type]
                ),
            )
        if scope_type != "actor":
            return CurrentVersionState(
                connector_id=connector.id,
                connector_name=connector.name,
                connector_type=connector.connector_type,
                latest_version=latest_version,
                active_version=latest_version,
                is_version_pinned=False,
                active_scope=None,
                active_scope_id=None,
                ancestor_configurations=(),
                descendant_configurations=(),
            )

        version_data = api_client.get_connector_version(
            connector_id=scope_id,
            connector_type=connector.connector_type,
            config_api_root=self.config_api_root,
            client_id=self.client_id,
            client_secret=self.client_secret,
            bearer_token=self.bearer_token,
            workspace_id=workspace_id,
        )
        active_version = (
            self._string_field(version_data, "dockerImageTag") or latest_version
        )
        scoped_configs = self._scoped_configurations(
            connector=connector,
            scoped_configs=version_data.get("scopedConfigs"),
        )
        active_config = self._active_config(scoped_configs, scope_type, scope_id)
        return CurrentVersionState(
            connector_id=connector.id,
            connector_name=connector.name,
            connector_type=connector.connector_type,
            latest_version=latest_version,
            active_version=active_version,
            is_version_pinned=active_config is not None
            or bool(version_data.get("isVersionOverrideApplied")),
            active_scope=active_config.scope_type if active_config else None,
            active_scope_id=active_config.scope_id if active_config else None,
            ancestor_configurations=tuple(
                config
                for config in scoped_configs
                if SCOPE_PRIORITY[config.scope_type] < SCOPE_PRIORITY[scope_type]
            ),
            descendant_configurations=tuple(
                config
                for config in scoped_configs
                if SCOPE_PRIORITY[config.scope_type] > SCOPE_PRIORITY[scope_type]
            ),
        )

    def summary_by_connector(self) -> tuple[dict[str, str | int], ...]:
        """Return override summary rows when available."""
        return ()

    def configuration_rows(self) -> tuple[dict[str, str], ...]:
        """Return scoped override rows when available."""
        return ()

    def list_instance_admin_users(self) -> tuple[dict[str, str], ...]:
        """Return Config API instance-admin users for interactive apply identity."""
        return api_client.list_instance_admin_users(
            config_api_root=self.config_api_root,
            client_id=self.client_id,
            client_secret=self.client_secret,
            bearer_token=self.bearer_token,
        )

    def stage_override(self, plan: OverridePlan) -> OperationPreview:
        """Build a non-mutating preview for the matching Ops MCP tool."""
        return OperationPreview(
            tool_name=version_override_tool_name(plan.scope_type),
            mutating=False,
            mode=self.mode,
            payload=build_version_override_payload(plan),
            required_approval_fields=REQUIRED_APPROVAL_FIELDS,
            warnings=SAFE_PREVIEW_WARNINGS,
        )

    def apply_override(
        self,
        plan: OverridePlan,
    ) -> OperationResult:
        """Apply the matching version override operation."""
        auth = ResolvedCloudAuth(
            bearer_token=self.bearer_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        payload = build_version_override_payload(plan)
        target = self._target_from_plan(plan)
        gcs_credentials = get_gcp_credentials_for_tier_gcs_ro()
        result = set_version_override(
            auth=auth,
            target=target,
            approval_comment_url=payload.approval_comment_url,
            version=payload.version,
            unset=payload.unset,
            override_reason=payload.override_reason,
            override_reason_reference_url=payload.override_reason_reference_url,
            issue_url=payload.override_reason_reference_url,
            ai_agent_session_url=payload.ai_agent_session_url,
            customer_tier_filter=payload.customer_tier_filter,
            force=payload.force,
            config_api_root=self.config_api_root,
            user_email=plan.user_email,
            gcs_credentials=gcs_credentials,
        )

        return OperationResult(
            tool_name=version_override_tool_name(plan.scope_type),
            success=result.success,
            mutating=True,
            mode=self.mode,
            message=result.message,
            payload=payload,
        )

    @property
    def _is_local_config_api(self) -> bool:
        return self.config_api_root.startswith("http://localhost:")

    def _list_local_connectors(self, query: str = "") -> tuple[ConnectorOption, ...]:
        connectors = [
            *self._local_definition_options("source"),
            *self._local_definition_options("destination"),
        ]
        normalized_query = query.strip().lower()
        if not normalized_query:
            return tuple(sorted(connectors, key=lambda connector: connector.name))
        return tuple(
            connector
            for connector in sorted(connectors, key=lambda connector: connector.name)
            if normalized_query in connector.name.lower()
            or normalized_query in connector.id.lower()
            or normalized_query in connector.docker_repository.lower()
        )

    def _local_definition_options(
        self,
        connector_type: ConnectorType,
    ) -> tuple[ConnectorOption, ...]:
        endpoint_name = (
            "source_definitions/list_latest"
            if connector_type == "source"
            else "destination_definitions/list_latest"
        )
        access_token = api_client._get_access_token(
            client_id=self.client_id,
            client_secret=self.client_secret,
            bearer_token=self.bearer_token,
            config_api_root=self.config_api_root,
        )
        response = api_client.requests.post(
            f"{self.config_api_root}/{endpoint_name}",
            json={},
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": api_client.ops_constants.USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=30,
        )
        if response.status_code != 200:
            raise PyAirbyteInputError(
                message=(
                    f"Failed to list local {connector_type} definitions: "
                    f"{response.status_code} {response.text}"
                ),
                context={"endpoint": f"{self.config_api_root}/{endpoint_name}"},
            )
        key = (
            "sourceDefinitions"
            if connector_type == "source"
            else "destinationDefinitions"
        )
        return tuple(
            self._connector_from_registry_entry(definition, connector_type)
            for definition in response.json().get(key, [])
            if isinstance(definition, Mapping)
        )

    def _scope_context(
        self,
        connector: ConnectorOption,
        scope_type: ScopeType,
        scope_id: str,
    ) -> tuple[ScopedConfiguration, ...]:
        access_token = api_client._get_access_token(
            client_id=self.client_id,
            client_secret=self.client_secret,
            bearer_token=self.bearer_token,
            config_api_root=self.config_api_root,
        )
        active_config = api_client._get_scoped_configuration_context(
            actor_definition_id=connector.id,
            scope_type=api_client._ScopeType(scope_type),
            scope_id=scope_id,
            config_api_root=self.config_api_root,
            access_token=access_token,
        )
        if not active_config:
            return ()
        return self._scoped_configurations(
            connector=connector,
            scoped_configs={scope_type: active_config},
        )

    def _target_from_plan(self, plan: OverridePlan) -> VersionOverrideTarget:
        if plan.scope_type == "actor":
            return VersionOverrideTarget(
                scope="actor",
                organization_id=plan.organization_id,
                connector_type=plan.connector_type,
                workspace_id=plan.workspace_id,
                actor_id=plan.actor_id,
            )
        if plan.scope_type == "workspace":
            return VersionOverrideTarget(
                scope="workspace",
                organization_id=plan.organization_id,
                connector_type=plan.connector_type,
                workspace_id=plan.workspace_id,
                connector_name=plan.connector_name,
            )
        return VersionOverrideTarget(
            scope="organization",
            organization_id=plan.organization_id,
            connector_type=plan.connector_type,
            connector_name=plan.connector_name,
        )

    def resolve_organization_id(
        self,
        scope_type: ScopeType,
        scope_id: str,
    ) -> str:
        """Return the organization ID for the selected target scope."""
        if scope_type == "organization":
            return scope_id
        if scope_type == "actor":
            return ""
        credentials = get_gcp_credentials_for_tier_gcs_ro()
        return (
            resolve_workspace(
                workspace_id=scope_id,
                credentials=credentials,
                allow_degraded=True,
            ).organization_id
            or ""
        )

    def resolve_context_guid(
        self,
        *,
        connector: ConnectorOption,
        context_guid: str,
    ) -> ContextResolution:
        """Resolve a context GUID into organization, workspace, or actor scope."""
        normalized = context_guid.strip()
        if not normalized:
            raise PyAirbyteInputError(message="Context GUID is required.")

        actor_resolution = self._resolve_actor_context(connector, normalized)
        if actor_resolution:
            return actor_resolution

        workspace_resolution = self._resolve_workspace_context(normalized)
        if workspace_resolution:
            return workspace_resolution

        organization_resolution = self._resolve_organization_context(normalized)
        if organization_resolution:
            return organization_resolution

        raise PyAirbyteInputError(message="Context GUID could not be resolved.")

    @staticmethod
    def _version_from_row(row: Mapping[str, object]) -> ConnectorVersion:
        return ConnectorVersion(
            version_id=OpsMcpAdapter._string_field(row, "version_id"),
            docker_image_tag=OpsMcpAdapter._string_field(row, "docker_image_tag"),
            docker_repository=OpsMcpAdapter._string_field(row, "docker_repository"),
            release_stage=OpsMcpAdapter._string_field(row, "release_stage"),
            support_level=OpsMcpAdapter._string_field(row, "support_level"),
            cdk_version=OpsMcpAdapter._string_field(row, "cdk_version"),
            language=OpsMcpAdapter._string_field(row, "language"),
            last_published=OpsMcpAdapter._string_field(row, "last_published"),
        )

    @staticmethod
    def _connector_name_from_repository(docker_repository: str) -> str:
        return docker_repository.rsplit("/", maxsplit=1)[-1]

    @staticmethod
    def _connector_type_from_repository(docker_repository: str) -> ConnectorType:
        connector_name = OpsMcpAdapter._connector_name_from_repository(
            docker_repository,
        )
        return "destination" if connector_name.startswith("destination-") else "source"

    @staticmethod
    def _release_from_row(row: Mapping[str, object]) -> ConnectorRelease:
        docker_repository = OpsMcpAdapter._string_field(row, "docker_repository")
        return ConnectorRelease(
            version_id=OpsMcpAdapter._string_field(row, "version_id"),
            connector_id=OpsMcpAdapter._string_field(row, "actor_definition_id"),
            connector_name=OpsMcpAdapter._connector_name_from_repository(
                docker_repository,
            ),
            connector_type=OpsMcpAdapter._connector_type_from_repository(
                docker_repository,
            ),
            docker_image_tag=OpsMcpAdapter._string_field(row, "docker_image_tag"),
            docker_repository=docker_repository,
            release_stage=OpsMcpAdapter._string_field(row, "release_stage"),
            last_published=OpsMcpAdapter._string_field(row, "last_published"),
        )

    @staticmethod
    def _tier_from_filters(raw: object) -> str:
        """Extract the customer tier from a rollout's `filters` JSON column.

        The terminal rollout stage targets the `TIER_0` cohort. Older rollouts
        modeled that stage as `ALL` (an empty/absent tier filter), so both an
        explicit `ALL` and no filter at all normalize to `TIER_0` here — they
        must never be mistaken for `TIER_2`, which would collide with the real
        `TIER_2` stage on the display cards.
        """
        filters: dict | None = None
        if isinstance(raw, str):
            with contextlib.suppress(json.JSONDecodeError, TypeError):
                filters = json.loads(raw)
        elif isinstance(raw, dict):
            filters = raw
        if filters:
            # Current format: customerTierFilters list
            tier_filters = filters.get("customerTierFilters")
            if isinstance(tier_filters, list):
                for entry in tier_filters:
                    if isinstance(entry, dict) and entry.get("name") == "TIER":
                        values = entry.get("value")
                        if isinstance(values, list) and values:
                            # A multi-tier filter is a real, distinct cohort — join
                            # it (like `_extract_tier_from_filters` in
                            # `registry/progressive_rollout_status.py`) rather than
                            # falling through to the terminal `TIER_0` default.
                            return ", ".join(
                                OpsMcpAdapter._normalize_tier(str(v)) for v in values
                            )
            # Legacy format: tierFilter dict
            tier_filter = filters.get("tierFilter") or {}
            tier = tier_filter.get("tier")
            if tier:
                return OpsMcpAdapter._normalize_tier(str(tier))
        return CustomerTier.TIER_0.value

    @staticmethod
    def _normalize_tier(tier: str) -> str:
        """Map a legacy `ALL` stage onto the `TIER_0` cohort it rolls out to."""
        if tier == CustomerTier.ALL.value:
            return CustomerTier.TIER_0.value
        return tier

    @staticmethod
    def _rollout_from_row(
        row: Mapping[str, object],
        *,
        sibling_rows: list[Mapping[str, object]] | None = None,
    ) -> ConnectorRollout:
        docker_repository = OpsMcpAdapter._string_field(row, "rc_docker_repository")
        rc_pin_count_raw = row.get("rc_pin_count", 0)
        declared_tag = OpsMcpAdapter._string_field(row, "tag")
        tier = declared_tag or OpsMcpAdapter._tier_from_filters(row.get("filters"))
        if not declared_tag and not row.get("filters"):
            has_explicit_progressive_sibling = any(
                sibling.get("tag") in {"TIER_2", "TIER_1"}
                or OpsMcpAdapter._tier_from_filters(sibling.get("filters"))
                in {"TIER_2", "TIER_1"}
                for sibling in sibling_rows or []
                if sibling is not row
            )
            tier = (
                CustomerTier.TIER_0.value
                if has_explicit_progressive_sibling
                else CustomerTier.ALL.value
            )
        return ConnectorRollout(
            rollout_id=OpsMcpAdapter._string_field(row, "rollout_id"),
            connector_id=OpsMcpAdapter._string_field(row, "actor_definition_id"),
            connector_name=OpsMcpAdapter._connector_name_from_repository(
                docker_repository,
            ),
            connector_type=OpsMcpAdapter._connector_type_from_repository(
                docker_repository,
            ),
            docker_repository=docker_repository,
            state=OpsMcpAdapter._string_field(row, "state"),
            rc_docker_image_tag=OpsMcpAdapter._string_field(
                row,
                "rc_docker_image_tag",
            ),
            initial_docker_image_tag=OpsMcpAdapter._string_field(
                row,
                "initial_docker_image_tag",
            ),
            current_target_rollout_pct=OpsMcpAdapter._string_field(
                row,
                "current_target_rollout_pct",
            ),
            final_target_rollout_pct=OpsMcpAdapter._string_field(
                row,
                "final_target_rollout_pct",
            ),
            created_at=OpsMcpAdapter._string_field(row, "created_at"),
            updated_at=OpsMcpAdapter._string_field(row, "updated_at"),
            rollout_strategy=OpsMcpAdapter._string_field(row, "rollout_strategy"),
            rc_pin_count=int(rc_pin_count_raw) if rc_pin_count_raw else 0,
            tier=tier,
            tier_is_explicit=bool(row.get("tag") or row.get("filters")),
            release_candidate_version_id=OpsMcpAdapter._string_field(
                row,
                "release_candidate_version_id",
            ),
            error_msg=OpsMcpAdapter._string_field(row, "error_msg"),
            failed_reason=OpsMcpAdapter._string_field(row, "failed_reason"),
            paused_reason=OpsMcpAdapter._string_field(row, "paused_reason"),
        )

    @staticmethod
    def _scoped_configurations(
        *,
        connector: ConnectorOption,
        scoped_configs: object,
    ) -> tuple[ScopedConfiguration, ...]:
        if not isinstance(scoped_configs, Mapping):
            return ()

        configs: list[ScopedConfiguration] = []
        for scope_type, config in scoped_configs.items():
            if scope_type in SCOPE_PRIORITY and isinstance(config, Mapping):
                configs.append(
                    ScopedConfiguration(
                        id=OpsMcpAdapter._string_field(config, "id"),
                        connector_id=connector.id,
                        connector_name=connector.name,
                        connector_type=connector.connector_type,
                        scope_type=scope_type,
                        scope_id=OpsMcpAdapter._string_field(config, "scope_id"),
                        scope_name=OpsMcpAdapter._string_field(config, "scope_name"),
                        value_name=OpsMcpAdapter._string_field(config, "value_name"),
                        description=OpsMcpAdapter._string_field(config, "description"),
                        origin_type=OpsMcpAdapter._string_field(config, "origin_type"),
                        origin_name=OpsMcpAdapter._string_field(config, "origin_name"),
                        expires_at=OpsMcpAdapter._string_field(config, "expires_at"),
                        reference_url=OpsMcpAdapter._string_field(
                            config, "reference_url"
                        ),
                    )
                )
        return tuple(configs)

    @staticmethod
    def _active_config(
        configurations: tuple[ScopedConfiguration, ...],
        scope_type: ScopeType,
        scope_id: str,
    ) -> ScopedConfiguration | None:
        scoped = tuple(
            config
            for config in configurations
            if config.scope_type == scope_type and config.scope_id == scope_id
        )
        if scoped:
            return scoped[0]
        inherited = tuple(
            config
            for config in configurations
            if SCOPE_PRIORITY[config.scope_type] < SCOPE_PRIORITY[scope_type]
        )
        if not inherited:
            return None
        return max(inherited, key=lambda config: SCOPE_PRIORITY[config.scope_type])

    @staticmethod
    def _string_field(row: Mapping[str, object], field_name: str) -> str:
        value = row.get(field_name)
        if value is None:
            return ""
        return str(value)

    @staticmethod
    def _connector_from_registry_entry(
        entry: Mapping[str, object],
        connector_type: ConnectorType,
    ) -> ConnectorOption:
        definition_id_field = (
            "sourceDefinitionId"
            if connector_type == "source"
            else "destinationDefinitionId"
        )
        raw_name = OpsMcpAdapter._string_field(entry, "name")
        docker_repository = OpsMcpAdapter._string_field(entry, "dockerRepository")
        canonical_name = docker_repository.rsplit("/", maxsplit=1)[-1] or raw_name
        return ConnectorOption(
            id=OpsMcpAdapter._string_field(entry, definition_id_field),
            name=canonical_name,
            connector_type=connector_type,
            latest_version=OpsMcpAdapter._string_field(entry, "dockerImageTag"),
            docker_repository=docker_repository,
        )

    def _resolve_actor_context(
        self,
        connector: ConnectorOption,
        context_guid: str,
    ) -> ContextResolution | None:
        access_token = api_client._get_access_token(
            client_id=self.client_id,
            client_secret=self.client_secret,
            bearer_token=self.bearer_token,
            config_api_root=self.config_api_root,
        )
        response = api_client.requests.post(
            f"{self.config_api_root}/{connector.connector_type}s/get",
            json={f"{connector.connector_type}Id": context_guid},
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": api_client.ops_constants.USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=30,
        )
        if response.status_code in CONTEXT_RESOLUTION_MISS_STATUS_CODES:
            return None
        if response.status_code != 200:
            raise PyAirbyteInputError(
                message=f"Failed to resolve actor context: {response.status_code} {response.text}",
            )
        actor_info = response.json()
        definition_id = self._string_field(
            actor_info,
            f"{connector.connector_type}DefinitionId",
        )
        if definition_id and definition_id != connector.id:
            return None
        actor_name = self._string_field(actor_info, "name")
        workspace_id = self._string_field(actor_info, "workspaceId")
        workspace_resolution = self._resolve_workspace_context(workspace_id)
        if not workspace_resolution:
            raise PyAirbyteInputError(message="Actor workspace could not be resolved.")
        org_resolution = self._resolve_organization_context(
            workspace_resolution.organization_id,
        )
        return ContextResolution(
            scope_type="actor",
            scope_id=context_guid,
            organization_id=workspace_resolution.organization_id,
            scope_name=actor_name,
            workspace_id=workspace_id,
            workspace_name=workspace_resolution.scope_name,
            organization_name=org_resolution.scope_name if org_resolution else "",
            actor_id=context_guid,
            actor_type=connector.connector_type,
        )

    def _resolve_workspace_context(
        self,
        context_guid: str,
    ) -> ContextResolution | None:
        if not context_guid:
            return None
        access_token = api_client._get_access_token(
            client_id=self.client_id,
            client_secret=self.client_secret,
            bearer_token=self.bearer_token,
            config_api_root=self.config_api_root,
        )
        response = api_client.requests.post(
            f"{self.config_api_root}/workspaces/get",
            json={"workspaceId": context_guid},
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": api_client.ops_constants.USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=30,
        )
        if response.status_code in CONTEXT_RESOLUTION_MISS_STATUS_CODES:
            return None
        if response.status_code != 200:
            raise PyAirbyteInputError(
                message=f"Failed to resolve workspace context: {response.status_code} {response.text}",
            )
        ws_data = response.json()
        organization_id = self._string_field(ws_data, "organizationId")
        workspace_name = self._string_field(ws_data, "name")
        if not organization_id:
            raise PyAirbyteInputError(
                message="Workspace organization could not be resolved."
            )
        org_resolution = self._resolve_organization_context(organization_id)
        return ContextResolution(
            scope_type="workspace",
            scope_id=context_guid,
            organization_id=organization_id,
            scope_name=workspace_name,
            workspace_id=context_guid,
            workspace_name=workspace_name,
            organization_name=org_resolution.scope_name if org_resolution else "",
        )

    def _resolve_organization_context(
        self,
        context_guid: str,
    ) -> ContextResolution | None:
        try:
            organization = get_organization_info(
                organization_id=context_guid,
                config_api_root=self.config_api_root,
                client_id=self.client_id,
                client_secret=self.client_secret,
                bearer_token=self.bearer_token,
            )
        except PaymentConfigAPIError as error:
            raise PyAirbyteInputError(
                message=f"Failed to resolve organization context: {error}",
            ) from error
        if not organization:
            return None
        return ContextResolution(
            scope_type="organization",
            scope_id=context_guid,
            organization_id=context_guid,
            scope_name=organization.organization_name,
            organization_name=organization.organization_name,
        )

    def _connector_from_definition_id(
        self,
        actor_definition_id: str,
    ) -> ConnectorOption | None:
        try:
            (
                connector_name,
                connector_type,
                latest_version,
                docker_repository,
            ) = resolve_definition_id_to_registry_info(
                actor_definition_id,
                from_gcs=True,
            )
        except PyAirbyteInputError:
            return None
        typed_connector_type: ConnectorType = (
            "destination" if connector_type == "destination" else "source"
        )
        return ConnectorOption(
            id=actor_definition_id,
            name=connector_name,
            connector_type=typed_connector_type,
            latest_version=latest_version,
            docker_repository=docker_repository,
        )

    def _connector_from_name(self, connector_name: str) -> ConnectorOption | None:
        try:
            actor_definition_id = resolve_canonical_name_to_definition_id(
                connector_name,
                from_gcs=True,
            )
        except PyAirbyteInputError:
            return None
        return self._connector_from_definition_id(actor_definition_id)


def preview_to_json(preview: OperationPreview) -> str:
    """Serialize an operation preview for display."""
    return json.dumps(
        {
            "tool_name": preview.tool_name,
            "mutating": preview.mutating,
            "payload": preview.payload.model_dump(mode="json"),
            "required_approval_fields": preview.required_approval_fields,
            "warnings": preview.warnings,
        },
        indent=2,
        sort_keys=True,
    )


def operation_result_to_json(result: OperationResult) -> str:
    """Serialize an operation result for display."""
    return json.dumps(
        {
            "tool_name": result.tool_name,
            "success": result.success,
            "mutating": result.mutating,
            "mode": result.mode,
            "message": result.message,
            "payload": result.payload.model_dump(mode="json"),
        },
        indent=2,
        sort_keys=True,
    )


def configuration_rows(
    configurations: tuple[ScopedConfiguration, ...],
) -> tuple[dict[str, str], ...]:
    """Return override rows for display tables."""
    return tuple(asdict(config) for config in configurations)
