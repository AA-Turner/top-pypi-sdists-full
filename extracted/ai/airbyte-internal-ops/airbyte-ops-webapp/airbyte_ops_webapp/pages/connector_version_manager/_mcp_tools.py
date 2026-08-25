"""Tool definitions for the Connector Version Manager page."""

from __future__ import annotations

import logging
import re
from collections.abc import Mapping
from dataclasses import asdict
from datetime import datetime
from typing import Any

from airbyte.exceptions import PyAirbyteInputError
from airbyte_ops_mcp.cloud_admin import api_client as cloud_api
from airbyte_ops_mcp.cloud_admin.registry_lookup import (
    invalidate_cloud_registry_cache,
)
from airbyte_ops_mcp.connector_ops.rollouts import state_transitions
from airbyte_ops_mcp.connector_ops.rollouts.constants import CustomerTier
from airbyte_ops_mcp.github_actions import trigger_workflow_dispatch
from airbyte_ops_mcp.github_api import resolve_ci_trigger_github_token
from fastmcp import FastMCPApp

from airbyte_ops_webapp.models import (
    ConnectorOption,
    OverridePlan,
    RolloutSyncSummary,
    ScopeType,
    TierPopulationFactors,
)
from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    DEFAULT_ADMIN_USER_ID,
    auth_available,
    build_rollout_summary,
    cloud_scope_url,
    connector_context_placeholder,
    connector_options,
    connector_rows,
    context_error_message,
    fallback_current_state,
    get_adapter,
    json_text,
    latest_version_rows,
    org_connector_pin_rows,
    org_pin_version_rows,
    pinned_version_rows,
    progressive_rollout_rows,
    recent_release_rows,
    rollout_rows_or_empty,
    rollout_rows_with_siblings_or_empty,
    rows_from_dataclasses,
    scope_context_available,
    scope_context_needed_message,
    target_ids,
    version_rows_or_empty,
    yanked_version_rows,
)
from airbyte_ops_webapp.pages.connector_version_manager._state import (
    ApplyOverrideResult,
    CompoundContextResult,
    ConnectorContextResult,
    ConnectorVersionContextResult,
    RegistryCacheInvalidationResult,
    RemovePinsResult,
    RolloutActionResult,
    ScopeResolutionResult,
    SearchConnectorsResult,
    TabRowsResult,
    VersionPinsResult,
)
from airbyte_ops_webapp.pages.shared_components.org_search import (
    OrgSearchResult,
    search_organizations_and_workspaces,
)
from airbyte_ops_webapp.services.connector_version_manager.adapter import (
    OpsMcpAdapter,
    operation_result_to_json,
)
from airbyte_ops_webapp.services.connector_version_manager.demo_mode import (
    MockPinningAdapter,
)
from airbyte_ops_webapp.state import mock_only_enabled

connector_version_manager_app = FastMCPApp("Connector Version Manager")
logger = logging.getLogger(__name__)

# Number of pins fetched per "Load More" click.
_PIN_BATCH_SIZE = 100

# Registry yank workflow dispatch target (mirrors `mcp/connector_registry.py`).
_YANK_WORKFLOW_REPO_OWNER = "airbytehq"
_YANK_WORKFLOW_REPO_NAME = "airbyte"
_YANK_WORKFLOW_DEFAULT_BRANCH = "master"
_YANK_WORKFLOW_FILE = "version-yank-command.yml"
YANK_STORE = "coral:prod"
FINALIZE_ROLLOUT_WORKFLOW_URL = (
    "https://github.com/airbytehq/airbyte/actions/workflows/finalize_rollout.yml"
)


@connector_version_manager_app.tool()
def invalidate_registry_cache() -> RegistryCacheInvalidationResult:
    """Invalidate cached cloud registry responses before a refresh."""
    invalidate_cloud_registry_cache()
    return RegistryCacheInvalidationResult(invalidated=True)


def _connector_is_destination(
    connector: ConnectorOption | Mapping[str, Any],
) -> bool:
    """Resolve connector direction from connector metadata."""
    if isinstance(connector, Mapping):
        connector_type = connector["connector_type"]
    else:
        connector_type = connector.connector_type
    return connector_type == "destination"


def _fmt_date_short(value: str) -> str:
    """Format an ISO datetime string to `yyyy-mm-dd (ddd)` for display."""
    if not value:
        return ""
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    return parsed.strftime("%Y-%m-%d (%a)")


def _fmt_date_long(value: str) -> str:
    """Format an ISO datetime string to `Ddd, Mon D, YYYY` (e.g. `Tue, Mar 3, 2026`)."""
    if not value:
        return ""
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    return f"{parsed:%a}, {parsed:%b} {parsed.day}, {parsed:%Y}"


def _version_with_date(tag: str, raw_date: str) -> str:
    """Combine a version tag with its release date, e.g. `1.2.0 (Tue, Mar 3, 2026)`.

    Falls back to just the tag when no release date is available, so the row
    never renders an empty `()`.
    """
    if not tag:
        return ""
    formatted = _fmt_date_long(raw_date)
    return f"{tag} ({formatted})" if formatted else tag


DEFAULT_CUSTOMER_TIER_FILTER = "TIER_2"
SENSITIVE_CUSTOMER_TIERS: frozenset[str] = frozenset({"TIER_0", "TIER_1"})


def _customer_tier_label(customer_tier: str) -> str:
    """Build the scope's customer-tier line for the pin modal."""
    if not customer_tier:
        return (
            "Customer tier: unresolved \u2014 the pin will be submitted as "
            f"{DEFAULT_CUSTOMER_TIER_FILTER}."
        )
    if customer_tier in SENSITIVE_CUSTOMER_TIERS:
        return (
            f"Customer tier: {customer_tier} \u2014 sensitive customer, "
            "human approval required before pinning."
        )
    return f"Customer tier: {customer_tier}"


def _override_plan(
    *,
    adapter: OpsMcpAdapter,
    connector_id: str,
    connector_name: str,
    connector_type: str,
    scope_type: ScopeType,
    scope_id: str,
    actor_workspace_id: str,
    action: str,
    version: str,
    override_reason: str,
    reference_url: str,
    approval_comment_url: str = "",
    user_email: str | None = None,
    customer_tier_filter: str = "TIER_2",
    force: bool = False,
) -> OverridePlan:
    organization_id, workspace_id, actor_id = target_ids(
        adapter=adapter,
        scope_type=scope_type,
        scope_id=scope_id,
        actor_workspace_id=actor_workspace_id,
    )
    return OverridePlan(
        action=action,
        connector_id=connector_id,
        connector_name=connector_name,
        connector_type=connector_type,
        scope_type=scope_type,
        organization_id=organization_id,
        workspace_id=workspace_id or None,
        actor_id=actor_id or None,
        scope_id=scope_id,
        version=None if action == "unset" else version,
        override_reason=override_reason,
        override_reason_reference_url=reference_url,
        approval_comment_url=approval_comment_url,
        user_email=user_email,
        # An unresolved tier keeps the conservative default rather than widening
        # the filter, so the guardrail still rejects sensitive-tier targets.
        customer_tier_filter=customer_tier_filter or DEFAULT_CUSTOMER_TIER_FILTER,
        force=force,
    )


# ---------------------------------------------------------------------------
# Lazy tab-loading tools
# ---------------------------------------------------------------------------


@connector_version_manager_app.tool()
def load_recent_releases_tab(limit: int = 250) -> TabRowsResult:
    """Load Recent Releases tab data on demand (lazy)."""
    rows = recent_release_rows(limit=limit)
    return TabRowsResult(rows=rows, limit=limit)


@connector_version_manager_app.tool()
def load_active_rollouts_tab() -> TabRowsResult:
    """Load Active Rollouts tab data on demand (lazy)."""
    return TabRowsResult(rows=progressive_rollout_rows())


@connector_version_manager_app.tool()
def load_latest_versions_tab() -> TabRowsResult:
    """Load Default Versions tab data on demand."""
    return TabRowsResult(rows=latest_version_rows())


@connector_version_manager_app.tool()
def load_pinned_versions_tab(origin_filter: str = "all") -> TabRowsResult:
    """Load Pinned Versions tab data, optionally filtered by pin origin type."""
    return TabRowsResult(rows=pinned_version_rows(origin_filter=origin_filter))


@connector_version_manager_app.tool()
def load_yanked_versions_tab() -> TabRowsResult:
    """Load Yanked Versions tab data on demand (lazy)."""
    return TabRowsResult(rows=yanked_version_rows())


@connector_version_manager_app.tool()
def load_org_pin_versions(organization_id: str = "") -> TabRowsResult:
    """Load the versions pinned under an organization (aggregate, all scopes)."""
    return TabRowsResult(rows=org_pin_version_rows(organization_id))


@connector_version_manager_app.tool()
def load_org_pins(
    organization_id: str = "",
    pinned_version_id: str = "",
) -> TabRowsResult:
    """Load the individual pins for a version under an organization."""
    return TabRowsResult(
        rows=org_connector_pin_rows(organization_id, pinned_version_id),
    )


# ---------------------------------------------------------------------------
# Connector search & context tools
# ---------------------------------------------------------------------------


@connector_version_manager_app.tool()
def search_connectors(query: str = "") -> SearchConnectorsResult:
    """Search connector definitions by name, definition ID, or Docker repository."""
    connectors = connector_rows(query)
    return SearchConnectorsResult(
        connectors=connectors,
        connector_options=connector_options(query),
        selected_connector_id=connectors[0]["id"] if connectors else "",
    )


@connector_version_manager_app.tool()
def resolve_scope_guid(
    connector_id: str,
    context_guid: str,
    auth_bearer_token: str = "",
) -> ScopeResolutionResult:
    """Validate a GUID and resolve it to a scope type with friendly name."""
    uuid_pattern = re.compile(
        r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
        r"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
    )
    normalized = context_guid.strip()
    if not normalized:
        return ScopeResolutionResult()
    if not uuid_pattern.match(normalized):
        return ScopeResolutionResult(context_error="Invalid UUID format.")
    adapter = get_adapter(auth_bearer_token or None)
    try:
        connector = adapter.get_connector(connector_id)
    except ValueError:
        return ScopeResolutionResult(
            scope_id=normalized,
            context_error=f"Unknown connector ID: {connector_id}",
            is_valid_uuid=True,
        )
    try:
        resolution = adapter.resolve_context_guid(
            connector=connector,
            context_guid=normalized,
        )
    except PyAirbyteInputError as error:
        return ScopeResolutionResult(
            scope_id=normalized,
            context_error=context_error_message(error),
            is_valid_uuid=True,
        )
    scope_url = cloud_scope_url(
        scope_type=resolution.scope_type,
        scope_id=resolution.scope_id,
        workspace_id=resolution.workspace_id or "",
        actor_type=resolution.actor_type,
    )
    if resolution.scope_name:
        label = f'"{resolution.scope_name}" {resolution.scope_type.title()}'
    else:
        label = resolution.scope_type.title()
    workspace_url = ""
    if resolution.workspace_id and resolution.scope_type != "workspace":
        workspace_url = cloud_scope_url(
            scope_type="workspace",
            scope_id=resolution.workspace_id,
        )
    organization_url = ""
    if resolution.organization_id and resolution.scope_type != "organization":
        organization_url = cloud_scope_url(
            scope_type="organization",
            scope_id=resolution.organization_id,
        )
    return ScopeResolutionResult(
        scope_type=resolution.scope_type,
        scope_id=resolution.scope_id,
        scope_name=resolution.scope_name,
        scope_url=scope_url,
        resolved_context_label=label,
        is_valid_uuid=True,
        actor_workspace_id=resolution.workspace_id or "",
        workspace_name=resolution.workspace_name,
        workspace_url=workspace_url,
        organization_name=resolution.organization_name,
        organization_url=organization_url,
        customer_tier=resolution.customer_tier,
        customer_tier_label=_customer_tier_label(resolution.customer_tier),
    )


def _add_description_display(pin_rows: list[dict[str, Any]], max_len: int = 40) -> None:
    """Add truncated `description_display` to each pin row in place.

    For breaking change pins (`origin_type == "breaking_change"`), the description
    is always empty so we substitute an explanatory label using the origin version.
    Connector rollout pins similarly get a synthesized label.
    """
    for row in pin_rows:
        if row.get("origin_type") == "breaking_change":
            origin = row.get("origin_name", "") or row.get("origin", "")
            row["description_display"] = (
                f"Breaking Change ({origin})" if origin else "Breaking Change"
            )
        elif row.get("origin_type") == "connector_rollout":
            row["description_display"] = "[Connector Rollout]"
        else:
            desc = row.get("description", "")
            row["description_display"] = (
                (desc[:max_len] + "\u2026") if len(desc) > max_len else desc
            )


def _build_context_result(
    *,
    connector: object,
    versions: list[dict[str, Any]],
    active_rollouts: list[dict[str, Any]],
    rollout_context: list[dict[str, Any]] | None = None,
    current_state: dict[str, Any],
    ancestor_configs: list[dict[str, Any]] | None = None,
    descendant_configs: list[dict[str, Any]] | None = None,
    resolved_context_label: str = "",
    context_guid: str = "",
    context_error: str = "",
    rollout_error: str = "",
    scope_type: ScopeType = "workspace",
    scope_id: str = "",
    actor_workspace_id: str = "",
    customer_tier: str | None = None,
    adapter: OpsMcpAdapter | None = None,
    include_rollout_sync_summary: bool = False,
) -> ConnectorContextResult:
    """Assemble the standard context result, validated via `ConnectorContextResult`.

    When `include_rollout_sync_summary` is set and an `adapter` is provided, each
    active tier rollout's replica-backed health + population counts are
    folded into `rollout_summary` — per-tier `tier_cards` (rollout line and
    health) plus a single connector-level `total_actors_display`. This is skipped
    for unauthenticated or error paths so the card still renders without them.
    """
    rollout_summary = build_rollout_summary(
        active_rollouts,
        rollout_context=rollout_context,
    )
    if include_rollout_sync_summary and adapter is not None and active_rollouts:
        is_destination = _connector_is_destination(connector)
        tier_summaries: dict[str, RolloutSyncSummary] = {}
        for rollout in active_rollouts:
            rollout_id = rollout.get("rollout_id", "")
            tier = rollout.get("tier", "")
            if not rollout_id:
                continue
            # The Config API call took 33-50s and hit its 60s timeout, blocking
            # the entire connector selection request; use the replica summary.
            # The replica path deliberately excludes tombstoned actors,
            # workspaces, and organizations; the platform endpoint does not,
            # so live counts are lower (the platform behavior is believed to
            # be a bug).
            if rollout.get("tier_is_explicit", False):
                tier_summaries[tier] = adapter.get_rollout_sync_summary(
                    rollout_id,
                    tier=tier,
                    is_destination=is_destination,
                )
            else:
                tier_summaries.update(
                    adapter.get_rollout_sync_summaries_by_tier(
                        rollout_id,
                        is_destination=is_destination,
                    )
                )
        connector_dict = (
            asdict(connector) if not isinstance(connector, dict) else connector
        )
        # All tier rollouts share one rollout version, so attribute the population's
        # pins to it — this lets the card's eligible/pinned exclude actors pinned
        # to a *different* version. Take the first rollout that carries a version.
        target_version_id = next(
            (
                str(rollout.get("release_candidate_version_id", ""))
                for rollout in active_rollouts
                if rollout.get("release_candidate_version_id")
            ),
            "",
        )
        # Earliest rollout `created_at` across the active tier rollouts is the
        # job-status window start passed to the population query — it enables the
        # platform's `filterByJobStatus` eligibility gate so the card's eligible
        # denominator tracks the backend's rollout audience. Earliest (widest
        # window) is the most inclusive single window across tiers.
        rollout_created_ats = [
            str(rollout.get("created_at", ""))
            for rollout in active_rollouts
            if rollout.get("created_at")
        ]
        rollout_created_at = min(rollout_created_ats) if rollout_created_ats else ""
        population = adapter.get_connector_population(
            connector_dict.get("id", ""),
            is_destination=connector_dict.get("connector_type", "source")
            == "destination",
            target_version_id=target_version_id,
            rollout_created_at=rollout_created_at,
        )
        # The headline "Eligible Actors" count is the backend's gated-eligible
        # total (`nActorsEligibleOrAlreadyPinned`). When tier resolution
        # succeeded, `total_eligible` is authoritative even at `0` (e.g. all
        # active actors are off-version pinned or gate-excluded), so render it
        # verbatim — including `0`. Only when tier resolution was unavailable
        # (no gated-eligible total) do we fall back to the connector-wide active
        # count, leaving the row blank if there are no active actors either.
        if population.tier_resolution_available:
            total_actors_display = f"{population.total_eligible:,}"
        elif population.total_active:
            total_actors_display = f"{population.total_active:,}"
        else:
            total_actors_display = ""
        # Only pass per-tier eligible counts when the breakdown was actually
        # computed, so the UI can tell a genuine `0 eligible` apart from
        # "eligible unknown" — the latter meaning `get_connector_population`
        # returned early (no connector id, or the actor-population DB query
        # failed). A GCS tier-export failure doesn't reach here: it raises and
        # aborts the page. Keyed by the disjoint cohort the card enumerates
        # (`TIER_2`, `TIER_1`, `TIER_0`).
        eligible_by_tier: dict[str, int] = {}
        pinned_by_tier: dict[str, int] = {}
        factors_by_tier: dict[str, TierPopulationFactors] = {}
        if population.tier_resolution_available:
            eligible_by_tier = {
                CustomerTier.TIER_2.value: population.eligible_tier_2,
                CustomerTier.TIER_1.value: population.eligible_tier_1,
                CustomerTier.TIER_0.value: population.eligible_tier_0,
            }
            # Active-only pinned counts (pinned ⊆ eligible) from the same
            # population as `eligible_by_tier`, so the card's numerator can't
            # exceed its denominator (which the rollout scan's `num_pinned`
            # can, since it counts inactive/tombstoned pinned actors).
            pinned_by_tier = {
                CustomerTier.TIER_2.value: population.pinned_tier_2,
                CustomerTier.TIER_1.value: population.pinned_tier_1,
                CustomerTier.TIER_0.value: population.pinned_tier_0,
            }
            # The full distinct-factor breakdown per tier, so the card can
            # over-communicate every factor and show how both the addressable
            # and the backend-eligible denominators are built.
            factors_by_tier = {
                tier: factors
                for tier, factors in (
                    (CustomerTier.TIER_2.value, population.factors_tier_2),
                    (CustomerTier.TIER_1.value, population.factors_tier_1),
                    (CustomerTier.TIER_0.value, population.factors_tier_0),
                )
                if factors is not None
            }
        rollout_summary = build_rollout_summary(
            active_rollouts,
            rollout_context=rollout_context,
            total_actors_display=total_actors_display,
            tier_summaries=tier_summaries,
            eligible_by_tier=eligible_by_tier,
            pinned_by_tier=pinned_by_tier,
            factors_by_tier=factors_by_tier,
        )
    connector_info = asdict(connector) if not isinstance(connector, dict) else connector
    return ConnectorContextResult(
        connector=connector_info,
        versions=versions,
        active_rollouts=active_rollouts,
        rollout_summary=rollout_summary,
        current_state=current_state,
        current_state_markdown=json_text(current_state),
        ancestor_configs=ancestor_configs or [],
        descendant_configs=descendant_configs or [],
        resolved_context_label=resolved_context_label,
        context_guid=context_guid,
        context_error=context_error,
        rollout_error=rollout_error,
        scope_type=scope_type,
        scope_id=scope_id,
        actor_workspace_id=actor_workspace_id,
        customer_tier=customer_tier or "",
        # `None` means no scope was resolved, so there is no tier to talk about;
        # an empty string means resolution ran and could not determine one.
        customer_tier_label=(
            "" if customer_tier is None else _customer_tier_label(customer_tier)
        ),
    )


@connector_version_manager_app.tool()
def load_connector_context(
    connector_id: str,
    scope_type: ScopeType = "workspace",
    scope_id: str = "",
    actor_workspace_id: str = "",
    context_guid: str = "",
    auth_bearer_token: str = "",
) -> ConnectorContextResult:
    """Load connector versions and scoped pin context."""
    if not connector_id:
        return connector_context_placeholder(
            "Search for and select a connector before loading scope context."
        )
    adapter = get_adapter(auth_bearer_token or None)
    try:
        connector = adapter.get_connector(connector_id)
    except ValueError:
        return connector_context_placeholder(f"Unknown connector ID: {connector_id}")
    active_rollouts, rollout_error = rollout_rows_or_empty(adapter, connector)
    rollout_context, sibling_rollout_error = rollout_rows_with_siblings_or_empty(
        adapter, connector
    )
    ctx_kwargs: dict[str, Any] = {
        "connector": connector,
        "active_rollouts": active_rollouts,
        "rollout_context": rollout_context,
        "rollout_error": rollout_error,
        "context_guid": context_guid,
        "scope_type": scope_type,
        "scope_id": scope_id,
        "actor_workspace_id": actor_workspace_id,
        "adapter": adapter,
    }
    if sibling_rollout_error and not rollout_error:
        ctx_kwargs["rollout_error"] = sibling_rollout_error
    if not auth_available(auth_bearer_token or None):
        versions, _version_error = version_rows_or_empty(adapter, connector)
        sign_in_msg = "Sign in with Airbyte to load scoped configuration context."
        return _build_context_result(
            **ctx_kwargs,
            versions=versions,
            current_state={"message": sign_in_msg},
            context_error=sign_in_msg,
        )
    versions, version_error = version_rows_or_empty(adapter, connector)
    ctx_kwargs["versions"] = versions
    ctx_kwargs["include_rollout_sync_summary"] = True
    resolved_context_label = ""
    if context_guid.strip():
        try:
            resolution = adapter.resolve_context_guid(
                connector=connector,
                context_guid=context_guid,
            )
            scope_type = resolution.scope_type
            scope_id = resolution.scope_id
            actor_workspace_id = resolution.workspace_id or ""
            ctx_kwargs.update(
                scope_type=scope_type,
                scope_id=scope_id,
                actor_workspace_id=actor_workspace_id,
                customer_tier=resolution.customer_tier,
            )
            if resolution.scope_name:
                resolved_context_label = (
                    f'"{resolution.scope_name}" {scope_type.title()}'
                )
            else:
                resolved_context_label = scope_type.title()
        except PyAirbyteInputError as error:
            return _build_context_result(
                **ctx_kwargs,
                current_state=fallback_current_state(connector, versions),
                context_error=context_error_message(error),
            )
    if not scope_context_available(adapter, scope_type, scope_id, actor_workspace_id):
        return _build_context_result(
            **ctx_kwargs,
            current_state=fallback_current_state(connector, versions),
            resolved_context_label=resolved_context_label,
            context_error=version_error or scope_context_needed_message(),
        )
    workspace_id = scope_id if scope_type == "workspace" else actor_workspace_id
    try:
        if isinstance(adapter, MockPinningAdapter):
            current_state = adapter.get_current_context(
                connector_id=connector.id,
                scope_type=scope_type,
                scope_id=scope_id,
            )
        else:
            current_state = adapter.get_current_context(
                connector_id=connector.id,
                scope_type=scope_type,
                scope_id=scope_id,
                workspace_id=workspace_id,
            )
    except PyAirbyteInputError as error:
        return _build_context_result(
            **ctx_kwargs,
            current_state=fallback_current_state(connector, versions),
            resolved_context_label=resolved_context_label,
            context_error=context_error_message(error),
        )
    return _build_context_result(
        **ctx_kwargs,
        current_state=asdict(current_state),
        ancestor_configs=rows_from_dataclasses(current_state.ancestor_configurations),
        descendant_configs=rows_from_dataclasses(
            current_state.descendant_configurations
        ),
        resolved_context_label=resolved_context_label,
        context_error=version_error,
    )


def _load_context_from_compound_value(
    compound_value: str,
    scope_type: ScopeType = "workspace",
    scope_id: str = "",
    actor_workspace_id: str = "",
    context_guid: str = "",
    auth_bearer_token: str = "",
) -> CompoundContextResult:
    """Shared helper: split a `connector_id|version` value, load context."""
    connector_id, _separator, version = compound_value.partition("|")
    context = load_connector_context(
        connector_id=connector_id,
        scope_type=scope_type,
        scope_id=scope_id,
        actor_workspace_id=actor_workspace_id,
        context_guid=context_guid,
        auth_bearer_token=auth_bearer_token,
    )
    return CompoundContextResult(
        **context.model_dump(),
        selected_connector_id=connector_id,
        target_version=version,
    )


@connector_version_manager_app.tool()
def load_recent_release_context(
    release_value: str,
    scope_type: ScopeType = "workspace",
    scope_id: str = "",
    actor_workspace_id: str = "",
    context_guid: str = "",
    auth_bearer_token: str = "",
) -> CompoundContextResult:
    """Load connector context from a recent release combobox selection."""
    return _load_context_from_compound_value(
        release_value,
        scope_type,
        scope_id,
        actor_workspace_id,
        context_guid,
        auth_bearer_token,
    )


@connector_version_manager_app.tool()
def load_progressive_rollout_context(
    rollout_value: str,
    scope_type: ScopeType = "workspace",
    scope_id: str = "",
    actor_workspace_id: str = "",
    context_guid: str = "",
    auth_bearer_token: str = "",
) -> CompoundContextResult:
    """Load connector context from a progressive rollout selection."""
    return _load_context_from_compound_value(
        rollout_value,
        scope_type,
        scope_id,
        actor_workspace_id,
        context_guid,
        auth_bearer_token,
    )


@connector_version_manager_app.tool()
def load_connector_version_context(
    connector_id: str,
    version_tag: str = "",
    scope_type: ScopeType = "workspace",
    scope_id: str = "",
    actor_workspace_id: str = "",
    context_guid: str = "",
    auth_bearer_token: str = "",
) -> ConnectorVersionContextResult:
    """Load connector context and auto-resolve pins for a specific version.

    Combines `load_connector_context` + `load_version_pins` into a single
    call so that clicking a row in the version selector tabs populates both
    the rollout status and pin detail sections in one round-trip.
    """
    if not connector_id:
        return ConnectorVersionContextResult()

    context = load_connector_context(
        connector_id=connector_id,
        scope_type=scope_type,
        scope_id=scope_id,
        actor_workspace_id=actor_workspace_id,
        context_guid=context_guid,
        auth_bearer_token=auth_bearer_token,
    )
    latest_version = context.connector.latest_version
    effective_version = version_tag or latest_version
    default_version = context.rollout_summary.initial_docker_image_tag or latest_version

    # Resolve version_id and release dates from the versions list
    resolved_version_id = ""
    selected_version_release_date = ""
    latest_version_release_date = ""
    default_version_release_date = ""
    promoting_version_release_date = ""
    for v in context.versions:
        tag = v.get("docker_image_tag", "")
        if tag == effective_version:
            resolved_version_id = str(v.get("version_id", "") or "")
            selected_version_release_date = str(v.get("last_published", "") or "")
        if tag == default_version:
            default_version_release_date = str(v.get("last_published", "") or "")
        if tag == latest_version:
            latest_version_release_date = str(v.get("last_published", "") or "")
        if tag == context.rollout_summary.rc_docker_image_tag:
            promoting_version_release_date = str(v.get("last_published", "") or "")

    adapter = get_adapter(auth_bearer_token or None)

    yank_fields = _selected_version_yank_fields(
        adapter,
        connector_name=context.connector.name,
        version=effective_version,
    )
    promotion_fields = _selected_version_promotion_fields(
        adapter,
        connector_name=context.connector.name,
        version=effective_version,
    )

    # Load pins if we resolved a version_id
    version_pins: list[dict[str, Any]] = []
    version_pins_total = 0
    version_pins_offset = 0
    selected_version_id = ""
    if resolved_version_id:
        pins, version_pins_total = adapter.list_version_pins(
            resolved_version_id,
            limit=_PIN_BATCH_SIZE,
        )
        version_pins = rows_from_dataclasses(pins)
        _add_description_display(version_pins)
        version_pins_offset = _PIN_BATCH_SIZE
        selected_version_id = resolved_version_id

    return ConnectorVersionContextResult(
        **context.model_dump(),
        selected_connector_id=connector_id,
        target_version=effective_version,
        selected_version_release_date=_fmt_date_short(selected_version_release_date),
        latest_version_release_date=_fmt_date_short(latest_version_release_date),
        selected_version_display=_version_with_date(
            effective_version, selected_version_release_date
        ),
        default_version_display=_version_with_date(
            latest_version, latest_version_release_date
        ),
        default_version_tag=latest_version,
        ga_default_version_display=_version_with_date(
            default_version, default_version_release_date
        ),
        ga_default_version_tag=default_version,
        promoting_version_display=_version_with_date(
            context.rollout_summary.rc_docker_image_tag,
            promoting_version_release_date,
        ),
        version_pins=version_pins,
        version_pins_total=version_pins_total,
        version_pins_offset=version_pins_offset,
        selected_version_id=selected_version_id,
        selected_version_tag=effective_version,
        **yank_fields,
        **promotion_fields,
    )


def _selected_version_yank_fields(
    adapter: OpsMcpAdapter,
    *,
    connector_name: str,
    version: str,
) -> dict[str, Any]:
    """Resolve the selected version's yank-marker fields for the status panel.

    Returns a mapping matching the `selected_version_yank_*` fields of
    `ConnectorVersionContextResult`. When the version has no active
    `version-yank.yml` marker (or the registry read fails), the fields signal a
    non-yanked version so the panel degrades gracefully rather than breaking the
    whole context load.
    """
    not_yanked: dict[str, Any] = {
        "selected_version_yanked": False,
        "selected_version_yank_yanked_at": "",
        "selected_version_yank_yanked_at_display": "",
        "selected_version_yank_reason": "",
        "selected_version_yank_approval_url": "",
        "selected_version_yank_raw": "",
    }
    if not connector_name or not version:
        return not_yanked
    try:
        marker = adapter.get_yank_marker(connector_name, version)
    except Exception:
        return not_yanked
    if marker is None:
        return not_yanked
    return {
        "selected_version_yanked": True,
        "selected_version_yank_yanked_at": marker.yanked_at,
        "selected_version_yank_yanked_at_display": _fmt_date_long(marker.yanked_at),
        "selected_version_yank_reason": marker.reason,
        "selected_version_yank_approval_url": marker.approval_url,
        "selected_version_yank_raw": marker.raw,
    }


def _selected_version_promotion_fields(
    adapter: OpsMcpAdapter,
    *,
    connector_name: str,
    version: str,
) -> dict[str, Any]:
    """Resolve the selected version's promotion-pending marker fields.

    Any missing marker or adapter error degrades to an empty, non-pending
    result so registry availability cannot prevent the context from loading.
    """
    empty: dict[str, Any] = {
        "selected_version_promotion_pending": False,
        "selected_version_promotion_requested_at": "",
        "selected_version_promotion_requested_at_display": "",
        "selected_version_promotion_requested_by": "",
        "selected_version_promotion_rollout_id": "",
        "selected_version_promotion_raw": "",
        "selected_version_promotion_state": "",
        "selected_version_promotion_marker_date": "",
    }
    if not connector_name or not version:
        return empty
    try:
        marker = adapter.get_progressive_rollout_marker(connector_name, version)
    except Exception:
        return empty
    if marker is None or (
        marker.state == "active" and not marker.promotion_requested_at
    ):
        return empty
    return {
        "selected_version_promotion_pending": True,
        "selected_version_promotion_requested_at": marker.promotion_requested_at,
        "selected_version_promotion_requested_at_display": _fmt_date_long(
            marker.promotion_requested_at
        ),
        "selected_version_promotion_requested_by": marker.promotion_requested_by,
        "selected_version_promotion_rollout_id": marker.rollout_id,
        "selected_version_promotion_raw": marker.raw,
        "selected_version_promotion_state": marker.state,
        "selected_version_promotion_marker_date": marker.marker_date,
    }


@connector_version_manager_app.tool()
def load_version_pins(
    version_id: str,
    version_tag: str = "",
    auth_bearer_token: str = "",
    offset: int = 0,
) -> VersionPinsResult:
    """Load more pins for a connector version (accumulating).

    Fetches all pins from row 0 through `offset + _PIN_BATCH_SIZE` so the
    client can replace its list with the full accumulated result.
    """
    new_end = offset + _PIN_BATCH_SIZE
    adapter = get_adapter(auth_bearer_token or None)
    pins, total = adapter.list_version_pins(version_id, limit=new_end, offset=0)
    pin_rows = rows_from_dataclasses(pins)
    _add_description_display(pin_rows)
    return VersionPinsResult(
        version_pins=pin_rows,
        version_pins_total=total,
        version_pins_offset=new_end,
        selected_version_id=version_id,
        selected_version_tag=version_tag,
    )


@connector_version_manager_app.tool()
def apply_override(
    connector_id: str,
    connector_name: str,
    connector_type: str,
    scope_type: ScopeType,
    scope_id: str,
    action: str,
    version: str,
    override_reason: str,
    reference_url: str,
    approval_comment_url: str = "",
    user_email: str | None = None,
    auth_bearer_token: str = "",
    actor_workspace_id: str = "",
    customer_tier_filter: str = "TIER_2",
    force: bool = False,
) -> ApplyOverrideResult:
    """Apply a connector version override after user confirmation."""
    adapter = get_adapter(auth_bearer_token or None)
    result = adapter.apply_override(
        _override_plan(
            adapter=adapter,
            connector_id=connector_id,
            connector_name=connector_name,
            connector_type=connector_type,
            scope_type=scope_type,
            scope_id=scope_id,
            actor_workspace_id=actor_workspace_id,
            action=action,
            version=version,
            override_reason=override_reason,
            reference_url=reference_url,
            approval_comment_url=approval_comment_url,
            user_email=user_email,
            customer_tier_filter=customer_tier_filter,
            force=force,
        ),
    )
    return ApplyOverrideResult(
        apply_result_json=operation_result_to_json(result),
        apply_message=result.message,
        apply_success=result.success,
    )


@connector_version_manager_app.tool()
def remove_selected_pins(
    selected_pins: list[dict[str, str]],
    connector_id: str,
    connector_name: str,
    connector_type: str,
    version_id: str = "",
    version_tag: str = "",
    auth_bearer_token: str = "",
    override_reason: str = "Bulk pin removal via Connector Version Manager",
    reference_url: str = "",
    approval_comment_url: str = "",
    user_email: str | None = None,
    customer_tier_filter: str = "TIER_2",
) -> RemovePinsResult:
    """Remove (unset) version overrides for each selected pin.

    Iterates over `selected_pins` and calls `apply_override` with
    `action="unset"` for each one. For actor-scope pins, resolves
    the actor's `workspace_id` via the Config API before unsetting.
    """
    adapter = get_adapter(auth_bearer_token or None)
    removed = 0
    errors: list[str] = []

    for pin in selected_pins:
        pin_scope_type: ScopeType = pin.get("scope_type", "workspace")
        pin_scope_id = pin.get("scope_id", "")
        if not pin_scope_id:
            errors.append("Skipped pin with empty scope_id.")
            continue

        actor_workspace_id = ""
        if pin_scope_type == "actor":
            actor_workspace_id = _resolve_actor_workspace(
                adapter=adapter,
                connector_id=connector_id,
                connector_type=connector_type,
                actor_id=pin_scope_id,
            )
            if not actor_workspace_id:
                errors.append(f"Could not resolve workspace for actor {pin_scope_id}.")
                continue

        try:
            result = adapter.apply_override(
                _override_plan(
                    adapter=adapter,
                    connector_id=connector_id,
                    connector_name=connector_name,
                    connector_type=connector_type,
                    scope_type=pin_scope_type,
                    scope_id=pin_scope_id,
                    actor_workspace_id=actor_workspace_id,
                    action="unset",
                    version="",
                    override_reason=override_reason,
                    reference_url=reference_url,
                    approval_comment_url=approval_comment_url,
                    user_email=user_email,
                    customer_tier_filter=customer_tier_filter,
                    force=False,
                ),
            )
            if result.success:
                removed += 1
            else:
                errors.append(f"{pin_scope_type}:{pin_scope_id} — {result.message}")
        except PyAirbyteInputError as exc:
            errors.append(f"{pin_scope_type}:{pin_scope_id} — {exc}")

    # Reload pins after removal so UI reflects current state
    pin_rows: list[dict[str, Any]] = []
    total = 0
    if version_id:
        pins_list, total = adapter.list_version_pins(
            version_id,
            limit=_PIN_BATCH_SIZE,
        )
        pin_rows = rows_from_dataclasses(pins_list)
        _add_description_display(pin_rows)

    summary = f"Removed {removed} of {len(selected_pins)} pin(s)."
    if errors:
        summary += " Errors: " + "; ".join(errors)

    return RemovePinsResult(
        remove_message=summary,
        remove_success=removed > 0 and not errors,
        version_pins=pin_rows,
        version_pins_total=total,
        version_pins_offset=_PIN_BATCH_SIZE,
        selected_version_id=version_id,
        selected_version_tag=version_tag,
    )


def _resolve_actor_workspace(
    *,
    adapter: OpsMcpAdapter,
    connector_id: str,
    connector_type: str,
    actor_id: str,
) -> str:
    """Resolve the workspace_id for an actor-scope pin via the Config API."""
    try:
        connector = adapter.get_connector(connector_id)
    except ValueError:
        return ""
    try:
        resolution = adapter.resolve_context_guid(
            connector=connector,
            context_guid=actor_id,
        )
        return resolution.workspace_id or ""
    except PyAirbyteInputError:
        return ""


@connector_version_manager_app.tool()
def advance_rollout(
    rollout_id: str,
    connector_id: str,
    docker_repository: str,
    docker_image_tag: str,
    target_percentage: str = "",
    auth_bearer_token: str = "",
    user_email: str = "",
) -> RolloutActionResult:
    """Advance a connector rollout to the next stage."""
    adapter = get_adapter(auth_bearer_token or None)
    config_api_root = adapter.config_api_root

    updated_by = _resolve_updated_by(
        user_email=user_email,
        bearer_token=auth_bearer_token or None,
        config_api_root=config_api_root,
    )

    parsed_pct = int(target_percentage) if target_percentage.strip() else None

    try:
        cloud_api.progress_connector_rollout(
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=connector_id,
            rollout_id=rollout_id,
            updated_by=updated_by,
            config_api_root=config_api_root,
            target_percentage=parsed_pct,
            bearer_token=auth_bearer_token or None,
        )
    except PyAirbyteInputError as exc:
        return RolloutActionResult(
            rollout_action_result=f"Failed to advance rollout: {exc}",
            rollout_action_success=False,
        )

    pct_msg = f" to {parsed_pct}%" if parsed_pct else ""
    return RolloutActionResult(
        rollout_action_result=(
            f"Successfully advanced rollout{pct_msg} for "
            f"{docker_repository}:{docker_image_tag}."
        ),
        rollout_action_success=True,
    )


@connector_version_manager_app.tool()
def pause_rollout(
    rollout_id: str,
    connector_id: str,
    docker_repository: str,
    docker_image_tag: str,
    paused_reason: str,
    auth_bearer_token: str = "",
    user_email: str = "",
) -> RolloutActionResult:
    """Pause a connector rollout, retaining its existing version pins.

    A paused rollout is held in place: Autopilot will not advance or promote it,
    and already-pinned actors stay on the release candidate. This is the
    reversible alternative to finalizing as `canceled`, which the platform
    re-creates for every still-advertised release candidate.
    """
    paused_reason = paused_reason.strip()
    if not paused_reason:
        return RolloutActionResult(
            rollout_action_result="A pause reason is required.",
            rollout_action_success=False,
        )

    adapter = get_adapter(auth_bearer_token or None)
    config_api_root = adapter.config_api_root

    updated_by = _resolve_updated_by(
        user_email=user_email,
        bearer_token=auth_bearer_token or None,
        config_api_root=config_api_root,
    )

    try:
        state_transitions.pause_rollout(
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=connector_id,
            rollout_id=rollout_id,
            updated_by=updated_by,
            paused_reason=paused_reason,
            config_api_root=config_api_root,
            bearer_token=auth_bearer_token or None,
        )
    except PyAirbyteInputError as exc:
        return RolloutActionResult(
            rollout_action_result=f"Failed to pause rollout: {exc}",
            rollout_action_success=False,
        )

    return RolloutActionResult(
        rollout_action_result=(
            f"Successfully paused rollout for "
            f"{docker_repository}:{docker_image_tag}. Existing pins retained. "
            "Status may take a few seconds to reflect this."
        ),
        rollout_action_success=True,
    )


@connector_version_manager_app.tool()
def unpause_rollout(
    rollout_id: str,
    connector_id: str,
    docker_repository: str,
    docker_image_tag: str,
    auth_bearer_token: str = "",
    user_email: str = "",
) -> RolloutActionResult:
    """Resume a paused connector rollout and hand it back to Autopilot.

    Autopilot skips `paused` rollouts and picks one up again as soon as its state is
    `in_progress`, so this submits the smallest manual progression that performs that
    transition: the percentage already pinned, which pins nobody new. A rollout with
    nothing pinned yet resumes at 1% (the platform rejects a `0` target), pinning one
    actor.
    """
    adapter = get_adapter(auth_bearer_token or None)
    config_api_root = adapter.config_api_root

    updated_by = _resolve_updated_by(
        user_email=user_email,
        bearer_token=auth_bearer_token or None,
        config_api_root=config_api_root,
    )

    try:
        _resume_pct, _ = state_transitions.unpause_rollout(
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=connector_id,
            rollout_id=rollout_id,
            updated_by=updated_by,
            config_api_root=config_api_root,
            bearer_token=auth_bearer_token or None,
        )
    except PyAirbyteInputError as exc:
        return RolloutActionResult(
            rollout_action_result=f"Failed to unpause rollout: {exc}",
            rollout_action_success=False,
        )

    return RolloutActionResult(
        rollout_action_result=(
            f"Successfully unpaused rollout for "
            f"{docker_repository}:{docker_image_tag}. "
            "Status may take a few seconds to reflect this."
        ),
        rollout_action_success=True,
    )


@connector_version_manager_app.tool()
def finalize_rollout(
    rollout_id: str,
    connector_id: str,
    docker_repository: str,
    docker_image_tag: str,
    state: str,
    auth_bearer_token: str = "",
    user_email: str = "",
) -> RolloutActionResult:
    """Finalize a connector rollout (promote, cancel, or rollback).

    `state` must be one of: `succeeded`, `canceled`, `failed_rolled_back`.
    """
    adapter = get_adapter(auth_bearer_token or None)
    config_api_root = adapter.config_api_root

    updated_by = _resolve_updated_by(
        user_email=user_email,
        bearer_token=auth_bearer_token or None,
        config_api_root=config_api_root,
    )

    try:
        cloud_api.finalize_connector_rollout(
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=connector_id,
            rollout_id=rollout_id,
            updated_by=updated_by,
            state=state,
            config_api_root=config_api_root,
            bearer_token=auth_bearer_token or None,
        )
    except PyAirbyteInputError as exc:
        return RolloutActionResult(
            rollout_action_result=f"Failed to finalize rollout: {exc}",
            rollout_action_success=False,
        )

    action_label = {
        "succeeded": "promoted",
        "canceled": "canceled",
        "failed_rolled_back": "rolled back",
    }.get(state, state)
    message = (
        f"Successfully {action_label} rollout for "
        f"{docker_repository}:{docker_image_tag}."
    )
    if state == "succeeded":
        connector_name = docker_repository.removeprefix("airbyte/")
        try:
            annotation = adapter.annotate_progressive_rollout_marker(
                connector_name,
                docker_image_tag,
                promotion_requested_by=user_email,
                rollout_id=rollout_id,
            )
            if not annotation.success:
                message += f" Promotion pending marker warning: {annotation.message}"
        except Exception as exc:
            logger.warning(
                "Failed to annotate promotion-pending marker for %s:%s: %s",
                connector_name,
                docker_image_tag,
                exc,
                exc_info=True,
            )
            message += f" Promotion pending marker warning: {exc}"
        message += (
            f" Monitor the promotion job in GitHub Actions: "
            f"{FINALIZE_ROLLOUT_WORKFLOW_URL}"
        )

    return RolloutActionResult(
        rollout_action_result=message,
        rollout_action_success=True,
    )


@connector_version_manager_app.tool()
def promote_to_next_stage(
    connector_id: str,
    docker_repository: str,
    docker_image_tag: str,
    next_tier: str,
    auth_bearer_token: str = "",
    user_email: str = "",
) -> RolloutActionResult:
    """Start a new rollout at the next tier (promote from current stage to next)."""
    valid_tiers = {t.value for t in CustomerTier}
    if next_tier not in valid_tiers:
        return RolloutActionResult(
            rollout_action_result=(
                f"Invalid tier '{next_tier}'. "
                f"Expected one of: {', '.join(sorted(valid_tiers))}."
            ),
            rollout_action_success=False,
        )

    adapter = get_adapter(auth_bearer_token or None)
    config_api_root = adapter.config_api_root

    updated_by = _resolve_updated_by(
        user_email=user_email,
        bearer_token=auth_bearer_token or None,
        config_api_root=config_api_root,
    )

    try:
        cloud_api.start_connector_rollout(
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=connector_id,
            updated_by=updated_by,
            rollout_strategy="manual",
            config_api_root=config_api_root,
            bearer_token=auth_bearer_token or None,
            customer_tier=next_tier,
        )
    except PyAirbyteInputError as exc:
        return RolloutActionResult(
            rollout_action_result=f"Failed to promote to next stage: {exc}",
            rollout_action_success=False,
        )

    tier_label = CustomerTier(next_tier).label
    return RolloutActionResult(
        rollout_action_result=(
            f"Successfully started {tier_label} rollout for "
            f"{docker_repository}:{docker_image_tag}."
        ),
        rollout_action_success=True,
    )


@connector_version_manager_app.tool()
def yank_connector_version(
    connector_name: str,
    version: str,
    reason: str = "",
    reference_url: str = "",
) -> RolloutActionResult:
    """Yank a released connector version from the production registry.

    Dispatches the `version-yank-command.yml` workflow which marks the version
    as yanked in `coral:prod` and recompiles the registry so the version is
    excluded from latest-version resolution. Intended for already-released
    versions that have no active progressive rollout.

    The optional `reference_url` is folded into the yank marker's `reason` as
    audit context. It is deliberately **not** passed as the workflow's
    `approval-url` input: that input is the unsupervised-agent HITL approval
    guard used by the CLI/MCP path, which does not apply to this
    human-operated webapp (see `CONTRIBUTING.md`).
    """
    marker_reason = reason
    if reference_url:
        marker_reason = (
            f"{reason}\n\nReference: {reference_url}"
            if reason
            else f"Reference: {reference_url}"
        )
    return _dispatch_yank_workflow(
        connector_name=connector_name,
        version=version,
        unyank=False,
        reason=marker_reason,
    )


@connector_version_manager_app.tool()
def unyank_connector_version(
    connector_name: str,
    version: str,
) -> RolloutActionResult:
    """Unyank (restore) a previously yanked connector version in the registry.

    Dispatches the same `version-yank-command.yml` workflow as
    `yank_connector_version`, but with `unyank: true`. That renames the active
    `version-yank.yml` marker to a `version-unyanked-<date>.yml` audit marker in
    `coral:prod` and recompiles the registry so the version rejoins
    latest-version resolution. Intended to reverse an earlier yank.
    """
    return _dispatch_yank_workflow(
        connector_name=connector_name,
        version=version,
        unyank=True,
    )


def _dispatch_yank_workflow(
    *,
    connector_name: str,
    version: str,
    unyank: bool,
    reason: str = "",
) -> RolloutActionResult:
    """Dispatch the registry `version-yank-command.yml` workflow.

    Shared by `yank_connector_version` and `unyank_connector_version`; `unyank`
    selects the direction and `reason` (yank only) is recorded in the marker.
    The optional reference URL is deliberately **not** passed as the workflow's
    `approval-url` input: that input is the unsupervised-agent HITL approval
    guard used by the CLI/MCP path, which does not apply to this human-operated
    webapp (see `CONTRIBUTING.md`).
    """
    action = "unyank" if unyank else "yank"
    if not connector_name or not version:
        return RolloutActionResult(
            rollout_action_result=(
                f"A connector and version must be selected before {action}ing."
            ),
            rollout_action_success=False,
        )

    if mock_only_enabled():
        return RolloutActionResult(
            rollout_action_result=(
                f"[Mock] Would {action} {connector_name}@{version} on {YANK_STORE}."
            ),
            rollout_action_success=True,
        )

    try:
        token = resolve_ci_trigger_github_token()
    except ValueError as exc:
        return RolloutActionResult(
            rollout_action_result=f"Failed to {action} version: {exc}",
            rollout_action_success=False,
        )

    workflow_inputs: dict[str, str] = {
        "connector-name": connector_name,
        "version": version,
        "store": YANK_STORE,
        "unyank": str(unyank).lower(),
    }
    if reason:
        workflow_inputs["reason"] = reason

    dispatch_result = trigger_workflow_dispatch(
        owner=_YANK_WORKFLOW_REPO_OWNER,
        repo=_YANK_WORKFLOW_REPO_NAME,
        workflow_file=_YANK_WORKFLOW_FILE,
        ref=_YANK_WORKFLOW_DEFAULT_BRANCH,
        inputs=workflow_inputs,
        token=token,
    )

    view_url = dispatch_result.run_url or dispatch_result.workflow_url
    return RolloutActionResult(
        rollout_action_result=(
            f"{action.capitalize()} workflow triggered for {connector_name}@{version} "
            f"on {YANK_STORE}. View progress at: {view_url}"
        ),
        rollout_action_success=True,
    )


def _resolve_updated_by(
    *,
    user_email: str,
    bearer_token: str | None,
    config_api_root: str,
) -> str:
    """Resolve a user UUID from email, falling back to a default admin ID."""
    if not user_email:
        return DEFAULT_ADMIN_USER_ID

    try:
        return cloud_api.get_user_id_by_email(
            email=user_email,
            config_api_root=config_api_root,
            bearer_token=bearer_token,
        )
    except PyAirbyteInputError:
        return DEFAULT_ADMIN_USER_ID


@connector_version_manager_app.tool()
def search_orgs_workspaces(
    query: str = "",
) -> OrgSearchResult:
    """Search organizations and workspaces by name (case-insensitive substring)."""
    return search_organizations_and_workspaces(query=query)
