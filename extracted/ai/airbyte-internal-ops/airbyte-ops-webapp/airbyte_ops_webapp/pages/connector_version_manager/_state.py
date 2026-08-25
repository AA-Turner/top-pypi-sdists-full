"""Typed Prefab state model for the Connector Version Manager page.

`ConnectorVersionManagerPageState` is the single source of truth for the page's
initial state. It extends the shared `OpsPageState` (env / deploy / auth) and the
shared `OrgLookupModalState`, then adds the page-specific fields. Building initial
state through this model means a wrong-typed value fails at page-build time rather
than silently in the browser, and the `tests/test_page_state.py` guardrail catches
key drift (`SetState` / initial-state keys absent from the model). Fields default,
and the model uses Pydantic's `extra="ignore"`, so a missing or unknown key is not
itself a construction error — the guardrail is what enforces key correctness.

Runtime tool results (`RESULT.*`) replace the nested placeholders
(`selected_connector`, `rollout_summary`, `selected_rollout`, `selected_pin`) and
the DataTable row lists wholesale with richer shapes; the models here describe the
*initial* placeholder shape only, mirroring the `EMPTY_*` constants and
`empty_connector()` in `_helpers.py`.

`ConnectorContextResult` and `TabRowsResult` are the typed output models for the
CVM MCP tools (`load_connector_context` and the lazy tab loaders): building tool
results through them means the `RESULT.*` reads in the `on_success` action ladders
are validated at the tool boundary instead of only failing in the browser.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from airbyte_ops_webapp.models import ScopeType
from airbyte_ops_webapp.pages.shared_components.org_lookup_modal import (
    OrgLookupModalState,
)
from airbyte_ops_webapp.pages.shared_components.org_search import OrgSearchRow
from airbyte_ops_webapp.state import OpsPageState


class ConnectorSummary(BaseModel):
    """Selected-connector placeholder, mirroring `empty_connector()`."""

    model_config = ConfigDict(frozen=True)

    id: str = ""
    name: str = ""
    connector_type: str = "source"
    latest_version: str = ""
    docker_repository: str = ""


class RolloutSelection(BaseModel):
    """Selected-rollout placeholder, mirroring `EMPTY_ROLLOUT_STATE`."""

    model_config = ConfigDict(frozen=True)

    rollout_id: str = ""
    connector_id: str = ""
    connector_name: str = ""
    connector_type: str = "source"
    docker_repository: str = ""
    state: str = ""
    rc_docker_image_tag: str = ""
    initial_docker_image_tag: str = ""
    current_target_rollout_pct: str = ""
    final_target_rollout_pct: str = ""
    created_at: str = ""
    updated_at: str = ""


class RolloutSummary(BaseModel):
    """Rollout-summary placeholder, mirroring `EMPTY_ROLLOUT_SUMMARY`.

    The context tool result replaces this with a populated summary (including the
    per-tier `tier_cards`), so the tabular `tier_cards` field is typed loosely as
    the tool-owned row shape.
    """

    model_config = ConfigDict(frozen=True)

    rc_version: str = ""
    tier_summary: str = ""
    highest_tier: str = ""
    next_tier: str = ""
    has_next_stage: bool = False
    autopilot: str = ""
    updated_at: str = ""
    total_rc_pins: str = "0"
    total_actors_display: str = ""
    tier_cards: list[dict[str, object]] = Field(default_factory=list)
    connector_id: str = ""
    connector_name: str = ""
    docker_repository: str = ""
    rc_docker_image_tag: str = ""
    initial_docker_image_tag: str = ""
    advance_rollout_id: str = ""
    advance_tier: str = ""
    advance_pct: str = ""
    promote_rollout_id: str = ""
    pause_rollout_id: str = ""
    is_paused: bool = False
    state: str = ""
    state_display: str = ""
    needs_review: bool = False
    needs_review_reason: str = ""
    needs_review_severity: str = ""
    is_finalizing: bool = False
    finalizing_rollout_id: str = ""
    finalizing_connector_id: str = ""
    finalizing_docker_repository: str = ""
    finalizing_rc_docker_image_tag: str = ""


class PinSelection(BaseModel):
    """Selected-pin placeholder, mirroring `EMPTY_PIN_STATE`."""

    model_config = ConfigDict(frozen=True)

    scope_type: str = ""
    scope_id: str = ""
    scope_url: str = ""
    origin_type: str = ""
    origin_name: str = ""
    description: str = ""
    description_display: str = ""
    created_at: str = ""
    created_at_display: str = ""
    expires_at: str = ""
    expires_at_display: str = ""
    reference_url: str = ""
    scope_name: str = ""


class ConnectorContextResult(BaseModel):
    """Typed output of `load_connector_context` and its builder helpers.

    Row lists (`versions`, `active_rollouts`, `ancestor_configs`,
    `descendant_configs`) and `current_state` are serialized dataclass rows whose
    shape varies by branch, so they stay `dict`/`list[dict]` rather than nested
    models; the scalar and object fields are fully typed.
    """

    model_config = ConfigDict(frozen=True)

    connector: ConnectorSummary = Field(default_factory=ConnectorSummary)
    versions: list[dict[str, object]] = Field(default_factory=list)
    active_rollouts: list[dict[str, object]] = Field(default_factory=list)
    rollout_summary: RolloutSummary = Field(default_factory=RolloutSummary)
    current_state: dict[str, object] = Field(default_factory=dict)
    current_state_markdown: str = ""
    ancestor_configs: list[dict[str, object]] = Field(default_factory=list)
    descendant_configs: list[dict[str, object]] = Field(default_factory=list)
    resolved_context_label: str = ""
    context_guid: str = ""
    context_error: str = ""
    rollout_error: str = ""
    scope_type: ScopeType = "workspace"
    scope_id: str = ""
    actor_workspace_id: str = ""
    customer_tier: str = ""
    customer_tier_label: str = ""


class TabRowsResult(BaseModel):
    """Typed output for the lazy tab loaders.

    `rows` is the loaded page. `limit` is the row count that was requested.
    Tabs that load everything at once leave `limit` at its default.
    """

    model_config = ConfigDict(frozen=True)

    rows: list[dict[str, object]] = Field(default_factory=list)
    limit: int = 0


class SearchConnectorsResult(BaseModel):
    """Typed output of `search_connectors` (connector table + combobox options)."""

    model_config = ConfigDict(frozen=True)

    connectors: list[dict[str, object]] = Field(default_factory=list)
    connector_options: list[dict[str, object]] = Field(default_factory=list)
    selected_connector_id: str = ""


class ScopeResolutionResult(BaseModel):
    """Typed output of `resolve_scope_guid` (a resolved pin scope + labels)."""

    model_config = ConfigDict(frozen=True)

    scope_type: str = ""
    scope_id: str = ""
    scope_name: str = ""
    scope_url: str = ""
    resolved_context_label: str = ""
    context_error: str = ""
    is_valid_uuid: bool = False
    actor_workspace_id: str = ""
    workspace_name: str = ""
    workspace_url: str = ""
    organization_name: str = ""
    organization_url: str = ""
    customer_tier: str = ""
    customer_tier_label: str = ""


class CompoundContextResult(ConnectorContextResult):
    """`ConnectorContextResult` plus the combobox-selected connector/version.

    Returned by the compound-value context loaders (`load_recent_release_context`,
    `load_progressive_rollout_context`) whose combobox values encode both the
    connector id and a target version.
    """

    selected_connector_id: str = ""
    target_version: str = ""


class ConnectorVersionContextResult(CompoundContextResult):
    """`CompoundContextResult` plus resolved version-pin detail for one version.

    Returned by `load_connector_version_context`, which resolves the selected
    version to its release date + pin list for the version-pin detail panel.
    """

    selected_version_release_date: str = ""
    latest_version_release_date: str = ""
    selected_version_display: str = ""
    default_version_display: str = ""
    default_version_tag: str = ""
    ga_default_version_display: str = ""
    ga_default_version_tag: str = ""
    promoting_version_display: str = ""
    version_pins: list[dict[str, object]] = Field(default_factory=list)
    version_pins_total: int = 0
    version_pins_offset: int = 0
    selected_version_id: str = ""
    selected_version_tag: str = ""
    selected_version_yanked: bool = False
    selected_version_yank_yanked_at: str = ""
    selected_version_yank_yanked_at_display: str = ""
    selected_version_yank_reason: str = ""
    selected_version_yank_approval_url: str = ""
    selected_version_yank_raw: str = ""
    selected_version_promotion_pending: bool = False
    selected_version_promotion_requested_at: str = ""
    selected_version_promotion_requested_at_display: str = ""
    selected_version_promotion_requested_by: str = ""
    selected_version_promotion_rollout_id: str = ""
    selected_version_promotion_raw: str = ""
    selected_version_promotion_state: str = ""
    selected_version_promotion_marker_date: str = ""


class VersionPinsResult(BaseModel):
    """Typed output of `load_version_pins` (a page of pins for a version)."""

    model_config = ConfigDict(frozen=True)

    version_pins: list[dict[str, object]] = Field(default_factory=list)
    version_pins_total: int = 0
    version_pins_offset: int = 0
    selected_version_id: str = ""
    selected_version_tag: str = ""


class RemovePinsResult(VersionPinsResult):
    """`VersionPinsResult` plus the outcome of a pin-removal action."""

    remove_message: str = ""
    remove_success: bool = False


class ApplyOverrideResult(BaseModel):
    """Typed output of `apply_override` (a version-pin write result)."""

    model_config = ConfigDict(frozen=True)

    apply_result_json: str = ""
    apply_message: str = ""
    apply_success: bool = False


class RolloutActionResult(BaseModel):
    """Typed output of the rollout/yank action tools (advance, promote, yank)."""

    model_config = ConfigDict(frozen=True)

    rollout_action_result: str = ""
    rollout_action_success: bool = False


class RegistryCacheInvalidationResult(BaseModel):
    """Typed output of the registry cache invalidation tool."""

    invalidated: bool = False


class ConnectorVersionManagerPageState(OpsPageState, OrgLookupModalState):
    """Complete initial Prefab state for the Connector Version Manager page."""

    # Connector selector
    accepts_default_connector: bool = True
    query: str = ""
    connectors: list[dict[str, object]] = Field(default_factory=list)
    connector_options: list[dict[str, object]] = Field(default_factory=list)
    latest_version_rows: list[dict[str, object]] = Field(default_factory=list)
    recent_release_rows: list[dict[str, object]] = Field(default_factory=list)
    recent_release_value: str = ""
    recent_release_options: list[dict[str, object]] = Field(default_factory=list)
    progressive_rollout_value: str = ""
    progressive_rollout_options: list[dict[str, object]] = Field(default_factory=list)
    progressive_rollout_rows: list[dict[str, object]] = Field(default_factory=list)
    pinned_version_rows: list[dict[str, object]] = Field(default_factory=list)
    pin_origin_filter: str = "all"
    yanked_version_rows: list[dict[str, object]] = Field(default_factory=list)
    recent_release_rows_loaded: bool = False
    recent_release_limit: int = 250
    progressive_rollout_rows_loaded: bool = False
    pinned_version_rows_loaded: bool = False
    yanked_version_rows_loaded: bool = False
    selector_tab: str = "active-rollouts"

    # Organization Pins tab (namespaced so it never contaminates the
    # connector-centric tabs). `org_pin_context_id` gates everything below it:
    # when it is empty the tab shows only the org selector, and clearing or
    # switching orgs resets the dependent rows/selection.
    org_pin_context_id: str = ""
    org_pin_context_label: str = ""
    # Namespaced org-lookup-modal keys for this tab, kept separate from the
    # shared `org_search_*` keys that the pin-context-pane modal uses so the two
    # modals on this page can't share open/query/results/selection state.
    org_pin_search_modal_open: bool = False
    org_pin_search_query: str = ""
    org_pin_search_results: list[OrgSearchRow] = Field(default_factory=list)
    org_pin_search_error: str = ""
    org_pin_search_selected_id: str = ""
    org_pin_search_selected_label: str = ""
    org_pin_version_rows: list[dict[str, object]] = Field(default_factory=list)
    org_pin_version_rows_loaded: bool = False
    org_pin_error: str = ""
    org_pin_selected_version_id: str = ""
    org_pin_selected_version_tag: str = ""
    org_pin_rows: list[dict[str, object]] = Field(default_factory=list)
    org_pin_rows_loaded: bool = False
    org_pin_rows_error: str = ""

    # Selected connector + resolved scope context
    selected_connector_id: str = ""
    selected_connector: ConnectorSummary = Field(default_factory=ConnectorSummary)
    scope_type: str = "workspace"
    scope_id: str = ""
    context_guid: str = ""
    resolved_context_label: str = ""
    scope_url: str = ""
    actor_workspace_id: str = ""

    # Version override form
    action: str = "set"
    target_version: str = ""
    override_reason: str = ""
    reference_url: str = ""
    # Submitted as the override's tier filter; replaced by the target's actual
    # tier once a scope resolves, since a mismatch is rejected by the guardrail.
    customer_tier_filter: str = "TIER_2"
    customer_tier_label: str = ""

    # Loaded connector context
    versions: list[dict[str, object]] = Field(default_factory=list)
    active_rollouts: list[dict[str, object]] = Field(default_factory=list)
    rollout_summary: RolloutSummary = Field(default_factory=RolloutSummary)
    current_state: dict[str, object] = Field(default_factory=dict)
    current_state_markdown: str = ""
    ancestor_configs: list[dict[str, object]] = Field(default_factory=list)
    descendant_configs: list[dict[str, object]] = Field(default_factory=list)
    context_error: str = ""
    rollout_error: str = ""

    # Notifications
    notifications: list[str] = Field(default_factory=list)
    has_unviewed_notifications: bool = False

    # Preview / apply result
    preview_json: str = ""
    preview_warnings: str = ""
    apply_result_json: str = ""
    apply_message: str = ""
    apply_success: bool = False

    # Pin modal
    pin_modal_open: bool = False
    locate_pin_modal_open: bool = False

    # Rollout action state
    rollout_modal_open: bool = False
    rollout_action: str = ""
    rollout_action_result: str = ""
    rollout_action_success: bool = False
    rollout_target_percentage: str = ""
    pause_reason: str = ""
    selected_rollout: RolloutSelection = Field(default_factory=RolloutSelection)

    # Yank version state
    yank_modal_open: bool = False
    unyank_modal_open: bool = False
    yank_reason: str = ""
    yank_reference_url: str = ""

    # Selected-version yank detail (populated by load_connector_version_context)
    selected_version_yanked: bool = False
    selected_version_yank_yanked_at: str = ""
    selected_version_yank_yanked_at_display: str = ""
    selected_version_yank_reason: str = ""
    selected_version_yank_approval_url: str = ""
    selected_version_yank_raw: str = ""
    selected_version_promotion_pending: bool = False
    selected_version_promotion_requested_at: str = ""
    selected_version_promotion_requested_at_display: str = ""
    selected_version_promotion_requested_by: str = ""
    selected_version_promotion_rollout_id: str = ""
    selected_version_promotion_raw: str = ""
    selected_version_promotion_state: str = ""
    selected_version_promotion_marker_date: str = ""

    # Version pin detail state
    context_loading: bool = False
    selected_version_tag: str = ""
    selected_version_id: str = ""
    selected_version_release_date: str = ""
    latest_version_release_date: str = ""
    selected_version_display: str = ""
    default_version_display: str = ""
    default_version_tag: str = ""
    ga_default_version_display: str = ""
    ga_default_version_tag: str = ""
    promoting_version_display: str = ""
    version_pins: list[dict[str, object]] = Field(default_factory=list)
    version_pins_total: int = 0
    version_pins_offset: int = 0
    selected_pin_index: int = -1
    selected_pin_checks: list[dict[str, object]] = Field(default_factory=list)
    remove_pins_modal_open: bool = False
    selected_pin: PinSelection = Field(default_factory=PinSelection)
    resolved_pin_scope_name: str = ""
    resolved_pin_scope_url: str = ""
    resolved_pin_workspace_name: str = ""
    resolved_pin_workspace_url: str = ""
    resolved_pin_org_name: str = ""
    resolved_pin_org_url: str = ""
