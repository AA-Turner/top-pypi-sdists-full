"""Shared helpers for Connector Version Manager page and components."""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import Any

from airbyte.exceptions import PyAirbyteInputError
from airbyte_ops_mcp.connector_ops.rollouts._helpers import get_connector_rollout_config
from airbyte_ops_mcp.connector_ops.rollouts.constants import (
    STRATEGY_DEFAULT,
    TIER_ORDER,
    CustomerTier,
    resolve_strategy,
)
from prefab_ui.actions import AppendState, SetState, ShowToast
from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import ComboboxOption, SelectOption
from prefab_ui.rx import ERROR, RESULT, STATE

from airbyte_ops_webapp.auth.mock_session import mock_oauth_is_authenticated
from airbyte_ops_webapp.models import (
    ConnectorOption,
    RolloutSyncSummary,
    ScopeType,
    TierPopulationFactors,
)
from airbyte_ops_webapp.pages.connector_version_manager._state import (
    ConnectorContextResult,
    PinSelection,
    RolloutSelection,
    RolloutSummary,
)
from airbyte_ops_webapp.services.connector_version_manager.adapter import (
    OpsMcpAdapter,
    _cloud_scope_url,
    _fmt_date,
)
from airbyte_ops_webapp.services.connector_version_manager.demo_mode import (
    MockPinningAdapter,
)
from airbyte_ops_webapp.state import (
    AIRBYTE_BEARER_TOKEN_ENV_VAR,
    AIRBYTE_CONFIG_API_ROOT_ENV_VAR,
    mock_only_enabled,
)

DEFAULT_ADMIN_USER_EMAIL = "devin-local@example.com"
DEFAULT_ADMIN_USER_ID = "00000000-0000-0000-0000-000000000000"
CONTEXT_ERROR = "Connector context failed to load."

# The per-tier rollout cards enumerate the three disjoint customer cohorts
# (Tier 2, Tier 1, Tier 0). The progressive-rollout backend models the final
# stage as `CustomerTier.ALL` (GA to everyone) rather than a `TIER_0` stage, so
# that stage is surfaced under the `TIER_0` cohort it ultimately brings in.
# Each entry pairs the displayed cohort with the rollout `tier` value that
# feeds it. Rollout progression / next-stage logic still uses `TIER_ORDER`.
_CARD_TIER_STAGES: list[tuple[CustomerTier, str]] = [
    (CustomerTier.TIER_2, CustomerTier.TIER_2.value),
    (CustomerTier.TIER_1, CustomerTier.TIER_1.value),
    (CustomerTier.TIER_0, CustomerTier.ALL.value),
]
APPLY_ERROR = "Apply change failed. No connector version override was applied."
SCOPE_PLACEHOLDER_SUFFIX = "_example"

# Canonical empty-state dicts for rollout and pin selection, derived from the
# typed models in `_state` so the placeholder shape has a single source of truth.
# Used in initial state, success handlers, and context resets.
EMPTY_ROLLOUT_STATE: dict[str, Any] = RolloutSelection().model_dump(mode="json")
EMPTY_PIN_STATE: dict[str, Any] = PinSelection().model_dump(mode="json")
EMPTY_ROLLOUT_SUMMARY: dict[str, Any] = RolloutSummary().model_dump(mode="json")


# ---------------------------------------------------------------------------
# Adapter construction
# ---------------------------------------------------------------------------


def auth_available(bearer_token_override: str | None = None) -> bool:
    if mock_only_enabled():
        return mock_oauth_is_authenticated()
    if os.getenv(AIRBYTE_BEARER_TOKEN_ENV_VAR):
        return True
    return bool(bearer_token_override)


def is_scope_placeholder(value: str) -> bool:
    normalized = value.strip()
    return bool(normalized and normalized.endswith(SCOPE_PLACEHOLDER_SUFFIX))


def scope_context_available(
    adapter: OpsMcpAdapter,
    scope_type: ScopeType,
    scope_id: str,
    actor_workspace_id: str,
) -> bool:
    if isinstance(adapter, MockPinningAdapter):
        return True
    if not scope_id.strip() or is_scope_placeholder(scope_id):
        return False
    if scope_type == "actor":
        return bool(actor_workspace_id.strip()) and not is_scope_placeholder(
            actor_workspace_id
        )
    return True


def get_adapter(bearer_token_override: str | None = None) -> OpsMcpAdapter:
    if mock_only_enabled():
        return MockPinningAdapter()
    bearer_token = bearer_token_override or os.getenv(AIRBYTE_BEARER_TOKEN_ENV_VAR)
    return OpsMcpAdapter(
        bearer_token=bearer_token,
        config_api_root=os.getenv(AIRBYTE_CONFIG_API_ROOT_ENV_VAR)
        or "https://cloud.airbyte.com/api/v1",
    )


# ---------------------------------------------------------------------------
# Data formatting
# ---------------------------------------------------------------------------


def connector_rows(query: str) -> list[dict[str, str]]:
    return [asdict(connector) for connector in get_adapter().search_connectors(query)]


def connector_options(query: str) -> list[dict[str, str]]:
    return [
        {
            "label": f"{connector['name']} ({connector['latest_version']})",
            "value": connector["id"],
        }
        for connector in connector_rows(query)
    ]


def recent_release_options() -> list[dict[str, str]]:
    try:
        releases = get_adapter().list_recent_releases()
    except Exception:
        return [{"label": "Recent releases unavailable", "value": ""}]
    return [
        {
            "label": (
                f"{release.connector_name} {release.docker_image_tag}"
                f" — {release.last_published[:10]}"
            ),
            "value": f"{release.connector_id}|{release.docker_image_tag}",
        }
        for release in releases
    ]


def progressive_rollout_options() -> list[dict[str, str]]:
    try:
        rollouts = get_adapter().list_progressive_rollouts()
    except Exception:
        return [{"label": "Progressive rollouts unavailable", "value": ""}]
    return [
        {
            "label": (
                f"{rollout.connector_name} {rollout.rc_docker_image_tag}"
                f" — {rollout.state}"
                f" — target {rollout.current_target_rollout_pct or '0'}%"
            ),
            "value": f"{rollout.connector_id}|{rollout.rc_docker_image_tag}",
        }
        for rollout in rollouts
    ]


def format_rollout_pct(pct: object) -> str:
    """Format a rollout target percentage for display.

    Normalizes empty/missing values to `"0%"` so a started tier never renders a
    bare `"%"`. Accepts values already carrying a trailing `%`.
    """
    text = str(pct if pct is not None else "").strip().rstrip("%").strip()
    if not text:
        text = "0"
    return f"{text}%"


def format_pinned_pct(pinned: int, eligible: int) -> str:
    """Format the actual pinned/eligible rollout ratio as a 1-decimal percentage.

    This is the *realized* rollout progress (how much of the eligible audience is
    pinned), not the rollout's target stage percentage. Uses float division to
    one decimal place (e.g. `1 / 7` renders `14.3%`, not a truncated `0%`).
    Returns `N/A` when `eligible` is `0` — there's no addressable audience to
    compute a ratio against, and a bare `0.0%` would be misleading.
    """
    if eligible <= 0:
        return "N/A"
    return f"{pinned / eligible * 100:.1f}%"


_EM_DASH = "\u2014"
_ARROW = "\u21b3"

# Status glyphs for a tier's rollout stage — shape + color so an operator can
# scan tier state at a glance without reading the numbers.
_STATUS_NOT_STARTED = ("\u26aa", "Not started")  # white circle
_STATUS_IN_PROGRESS = ("\U0001f535", "In progress")  # blue circle
_STATUS_ATTENTION = ("\U0001f7e1", "Attention")  # yellow circle
_STATUS_COMPLETE = ("\U0001f7e2", "Complete")  # green circle
_STATUS_PAUSED = ("\u23f8\ufe0f", "Paused")  # pause glyph

# Rollout `state` values that mean the stage exists but has not begun pinning —
# treated as "not started" so a not-yet-running tier never looks live.
_NOT_STARTED_STATES = frozenset({"", "initialized", "not_started", "pending"})
# Rollout `state` values that mean the stage is finished.
_DONE_STATES = frozenset({"finalized", "succeeded", "completed", "promoted"})


def _is_started(has_rollout: bool, state: str) -> bool:
    """Whether a tier's rollout is actually running (not merely defined)."""
    return has_rollout and (state or "").strip().lower() not in _NOT_STARTED_STATES


def format_ratio_pct(numerator: int, denominator: int, *, empty: str = _EM_DASH) -> str:
    """Format a whole-number `numerator / denominator` percentage.

    Rounds to the nearest whole percent for a compact rollout card (e.g. `10 / 14`
    renders `71%`). A non-zero ratio that rounds below `1%` renders `<1%`, so a
    small-but-present cohort never reads a misleading `0%`. When `denominator` is
    `0` the ratio is undefined and `empty` is returned — callers pass `"100%"` for
    a *started* coverage ratio (0-of-0 eligible is fully covered) or `"0%"` for a
    failure ratio (0-of-0 pinned has no failures).
    """
    if denominator <= 0:
        return empty
    pct = numerator / denominator * 100
    if 0 < pct < 1:
        return "<1%"
    return f"{round(pct)}%"


def tier_rollout_status(
    *, has_rollout: bool, state: str, deployed_pct: int, failing: int
) -> tuple[str, str]:
    """Pick the `(emoji, label)` status glyph for a tier's rollout stage.

    - `⚪ Not started` — no rollout for the tier, or one that is defined but hasn't
      begun pinning (`initialized` / `pending`).
    - `⏸️ Paused` — the rollout is paused.
    - `🟡 Attention` — the rollout is running with one or more failing pinned
      connectors.
    - `🟢 Complete` — the rollout is finished, or reports 100% deployed (every
      actor that will pin is pinned), with no failures.
    - `🔵 In progress` — the rollout is still rolling out, no failures.
    """
    normalized = (state or "").strip().lower()
    if not _is_started(has_rollout, normalized):
        return _STATUS_NOT_STARTED
    if normalized == "paused":
        return _STATUS_PAUSED
    if failing > 0:
        return _STATUS_ATTENTION
    if normalized in _DONE_STATES or deployed_pct >= 100:
        return _STATUS_COMPLETE
    return _STATUS_IN_PROGRESS


def _pct_to_int(pct: object) -> int:
    """Parse a rollout percentage (`"50"`, `"50%"`, `50`) to an `int`; `0` on failure."""
    text = str(pct if pct is not None else "").strip().rstrip("%").strip()
    try:
        return round(float(text))
    except ValueError:
        return 0


def build_breakdown_columns(
    factors: TierPopulationFactors,
    *,
    started: bool = True,
    succeeding: int | None = None,
    failing: int | None = None,
    awaiting: int | None = None,
) -> dict[str, Any]:
    """Build the two-column, operator-facing population breakdown for a tier card.

    Partitions the tier's active actors into two columns whose headers sum to the
    active total (`eligible + ineligible == active`), all scoped to the rollout
    version:

    - **Eligible** (`pinned_to_rollout + gate_pass`) — the platform's
      `nActorsEligibleOrAlreadyPinned`. Subdivided into `pinned` (optionally
      broken out by post-pin health into `succeeding` / `failing` /
      `awaiting results` when the rollout scan supplied those counts) and
      `not yet pinned` (`gate_pass`).
    - **Ineligible** (`off_version_pinned + gate_excluded_no_recent_sync +
      gate_excluded_failed`) — subdivided into `pinned to another version`,
      `no recent sync`, and `recent failure`. Actors pinned to another version
      are listed first; their sync recency is moot for this rollout, so they are
      implicitly mutually exclusive with the sync/failure rows.

    Percentages are whole-number cohort shares (`pinned` / `not yet pinned` as a
    share of `eligible`; health rows as a share of `pinned`). `started` controls
    the 0-of-0 coverage convention — a started tier with no eligible actors reads
    `100%`, an unstarted one reads `—`.

    Returns a dict with `eligible_header`, `eligible_rows`, `ineligible_header`,
    and `ineligible_rows` (each row a `{"text": ...}` for the renderer).
    """
    pinned = factors.pinned_to_rollout
    eligible_unpinned = factors.gate_pass
    eligible = pinned + eligible_unpinned
    ineligible = (
        factors.off_version_pinned
        + factors.gate_excluded_no_recent_sync
        + factors.gate_excluded_failed
    )
    coverage_empty = "100%" if started else _EM_DASH

    eligible_rows: list[dict[str, str]] = [
        {
            "text": f"{_ARROW} {pinned:,} pinned "
            f"({format_ratio_pct(pinned, eligible, empty=coverage_empty)})"
        }
    ]
    if succeeding is not None or failing is not None or awaiting is not None:
        succeeding_n = succeeding or 0
        failing_n = failing or 0
        awaiting_n = awaiting or 0
        eligible_rows.extend(
            [
                {
                    "text": f"    {_ARROW} {succeeding_n:,} succeeding "
                    f"({format_ratio_pct(succeeding_n, pinned, empty=_EM_DASH)})"
                },
                {
                    "text": f"    {_ARROW} {failing_n:,} failing "
                    f"({format_ratio_pct(failing_n, pinned, empty=_EM_DASH)})"
                },
                {
                    "text": f"    {_ARROW} {awaiting_n:,} awaiting results "
                    f"({format_ratio_pct(awaiting_n, pinned, empty=_EM_DASH)})"
                },
            ]
        )
    eligible_rows.append(
        {
            "text": f"{_ARROW} {eligible_unpinned:,} not yet pinned "
            f"({format_ratio_pct(eligible_unpinned, eligible, empty=coverage_empty)})"
        }
    )

    ineligible_rows: list[dict[str, str]] = [
        {"text": f"{_ARROW} {factors.off_version_pinned:,} pinned to another version"},
        {"text": f"{_ARROW} {factors.gate_excluded_no_recent_sync:,} no recent sync"},
        {"text": f"{_ARROW} {factors.gate_excluded_failed:,} recent failure"},
    ]

    return {
        "eligible_header": f"{eligible:,} Eligible Actors",
        "eligible_rows": eligible_rows,
        "ineligible_header": f"{ineligible:,} Ineligible",
        "ineligible_rows": ineligible_rows,
    }


def build_tier_card(
    display_tier: CustomerTier,
    *,
    has_rollout: bool,
    state: str = "",
    deployed_display: str,
    deployed_pct: int,
    factors: TierPopulationFactors | None,
    eligible_fallback: int = 0,
    succeeding: int | None = None,
    failing: int | None = None,
    awaiting: int | None = None,
) -> dict[str, Any]:
    """Assemble the per-tier rollout card dict consumed by the overview renderer.

    Combines the status glyph (`tier_rollout_status`, from `has_rollout` + the
    rollout `state`), the compact Rollout Status line values (`Deployed` /
    `Pinned` / `Failed`), and the two-column Actor Breakdown
    (`build_breakdown_columns`). `deployed_pct` is the backend-reported integer
    percent used both for the status glyph and the `Deployed` line;
    `deployed_display` is its formatted string (or `—` when there is no rollout).

    A tier counts as *started* only when it has a rollout whose `state` has begun
    pinning (see `_is_started`); this drives the 0-of-0 coverage convention.

    When `factors` is `None` (tier resolution unavailable) the breakdown columns
    collapse to just the eligible header from `eligible_fallback`.
    """
    started = _is_started(has_rollout, state)
    fail_count = failing or 0
    emoji, status_label = tier_rollout_status(
        has_rollout=has_rollout,
        state=state,
        deployed_pct=deployed_pct,
        failing=fail_count,
    )
    if factors is not None:
        pinned = factors.pinned_to_rollout
        eligible = pinned + factors.gate_pass
        columns = build_breakdown_columns(
            factors,
            started=started,
            succeeding=succeeding,
            failing=failing,
            awaiting=awaiting,
        )
    else:
        pinned = 0
        eligible = eligible_fallback
        columns = {
            "eligible_header": f"{eligible:,} Eligible Actors",
            "eligible_rows": [],
            "ineligible_header": _EM_DASH,
            "ineligible_rows": [],
        }
    coverage_empty = "100%" if started else _EM_DASH
    pinned_summary = (
        f"{pinned:,} of {eligible:,} eligible "
        f"({format_ratio_pct(pinned, eligible, empty=coverage_empty)})"
    )
    failed_summary = (
        f"{fail_count:,} of {pinned:,} pinned "
        f"({format_ratio_pct(fail_count, pinned, empty='0%')})"
    )
    return {
        "tier_label": display_tier.label,
        "tier_value": display_tier.value,
        "started": started,
        "status_emoji": emoji,
        "status_label": status_label,
        "deployed_display": deployed_display,
        "pinned_summary": pinned_summary,
        "failed_summary": failed_summary,
        **columns,
    }


def _autopilot_display(connector_id: str, rc_version: str | None) -> str:
    """Autopilot status with its strategy, e.g. `"ON (Fast)"` / `"ON (Slow)"`.

    Reads the registry `rolloutConfiguration`: `defaultRolloutMode` gates
    `ON`/`OFF`, and `autopilotConfig.strategy` (defaulting to `default`, which
    resolves to `fast`) selects the speed suffix. Returns `"OFF"` (no suffix)
    when autopilot is disabled or the config can't be read.
    """
    try:
        config = get_connector_rollout_config(connector_id, rc_version=rc_version)
        if config.default_rollout_mode.value != "autopilot":
            return "OFF"
        autopilot_config = config.autopilot_config
        raw_strategy = (
            autopilot_config.strategy.value
            if autopilot_config is not None and autopilot_config.strategy is not None
            else STRATEGY_DEFAULT
        )
        strategy = resolve_strategy(raw_strategy)
        return f"ON ({strategy.value.title()})"
    except Exception:
        return "OFF"


def progressive_rollout_rows() -> list[dict[str, Any]]:
    """Build consolidated dashboard rows for active progressive rollouts.

    Groups rollouts by (connector_id, rc_docker_image_tag) so each RC version
    appears as a single row with a per-tier status summary.
    """
    try:
        rollouts = get_adapter().list_progressive_rollouts()
    except Exception:
        return []
    raw_rows = rows_from_dataclasses(rollouts)

    # Group by connector + RC version
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in raw_rows:
        key = (row.get("connector_id", ""), row.get("rc_docker_image_tag", ""))
        groups.setdefault(key, []).append(row)

    consolidated: list[dict[str, Any]] = []
    tier_index = {t.value: i for i, t in enumerate(TIER_ORDER)}

    for (_connector_id, _rc_tag), group in groups.items():
        sorted_group = sorted(
            group,
            key=lambda r: tier_index.get(r.get("tier", "TIER_2"), 0),
        )

        # Build per-tier summary string, each tier prefixed with its status
        # glyph. This is an approximation: the top-level query has each tier's
        # `state` + `current_target_rollout_pct` (cheap rollout-table read) but
        # not the per-tier failure count, so `failing=0` here — the 🟡 Attention
        # glyph can only surface in the detailed view (which runs the population
        # scan). All other states (Not started / In progress / Complete / Paused)
        # are exact.
        tier_parts: list[str] = []
        for display_tier, stage_value in _CARD_TIER_STAGES:
            matching = [r for r in sorted_group if r.get("tier") == stage_value]
            if matching:
                rollout = matching[0]
                emoji, _ = tier_rollout_status(
                    has_rollout=True,
                    state=str(rollout.get("state") or ""),
                    deployed_pct=_pct_to_int(rollout.get("current_target_rollout_pct")),
                    failing=0,
                )
                pct = format_rollout_pct(rollout.get("current_target_rollout_pct"))
                tier_parts.append(f"{emoji} {display_tier.label}: {pct}")
            else:
                emoji, _ = tier_rollout_status(
                    has_rollout=False, state="", deployed_pct=0, failing=0
                )
                tier_parts.append(f"{emoji} {display_tier.label}: \u2014")

        highest = sorted_group[-1]
        connector_id = highest.get("connector_id", "")
        rc_tag = highest.get("rc_docker_image_tag")
        total_pins = max(
            (int(r.get("rc_pin_count", 0)) for r in sorted_group), default=0
        )

        consolidated.append(
            {
                "connector_id": connector_id,
                "connector_name": highest.get("connector_name", ""),
                "rc_docker_image_tag": rc_tag,
                "tier_summary": " | ".join(tier_parts),
                "state": highest.get("state", ""),
                "autopilot_display": _autopilot_display(connector_id, rc_tag),
                "rc_pin_count_display": f"{total_pins:,}",
            }
        )

    return consolidated


def latest_version_rows() -> list[dict[str, Any]]:
    """Build rows for the Latest Versions tab (one row per connector, GA only)."""
    try:
        connectors = get_adapter().search_connectors("")
    except Exception:
        return []
    return [asdict(c) for c in connectors]


def recent_release_rows() -> list[dict[str, Any]]:
    """Build DataTable rows for the Recent Releases tab (last 30 days, max 50)."""
    try:
        releases = get_adapter().list_recent_releases(limit=50)
    except Exception:
        return []
    rows = rows_from_dataclasses(releases)
    for row in rows:
        row["connector_and_version"] = (
            f"{row.get('connector_name', '')} {row.get('docker_image_tag', '')}"
        )
    return rows


def pinned_version_rows(
    origin_filter: str = "all",
) -> list[dict[str, Any]]:
    """Build rows for the Pinned Versions tab (cross-connector, versions with pins).

    `origin_filter` controls which rows are returned:
    * `"all"` - no filtering (default)
    * `"rollout"` - only versions with `rollout_pins > 0`
    * `"breaking_change"` - only versions with `breaking_change_pins > 0`
    * `"custom"` - only versions with `actor_pins > 0 OR workspace_pins > 0
      OR org_pins > 0`
    """
    try:
        raw = get_adapter().list_versions_with_pins()
    except Exception:
        return []
    rows: list[dict[str, Any]] = []
    for row in raw:
        bc = int(row.get("breaking_change_pins", 0) or 0)
        rollout = int(row.get("rollout_pins", 0) or 0)
        actor = int(row.get("actor_pins", 0) or 0)
        ws = int(row.get("workspace_pins", 0) or 0)
        org = int(row.get("org_pins", 0) or 0)

        if origin_filter == "rollout" and rollout == 0:
            continue
        if origin_filter == "breaking_change" and bc == 0:
            continue
        if origin_filter == "custom" and actor == 0 and ws == 0 and org == 0:
            continue

        docker_repo = row.get("docker_repository", "")
        canonical_name = (
            docker_repo.rsplit("/", 1)[-1]
            if docker_repo
            else row.get("connector_name", "")
        )
        rows.append(
            {
                **row,
                "connector_id": row.get("connector_definition_id", ""),
                "connector_name": canonical_name,
                "custom_pin_count_display": actor + ws + org,
                "breaking_change_pins_display": bc,
                "rollout_pins_display": rollout,
                "actor_pins_display": actor,
                "workspace_pins_display": ws,
                "org_pins_display": org,
            }
        )
    return rows


def admin_user_options() -> list[dict[str, str]]:
    if mock_only_enabled():
        return [{"label": DEFAULT_ADMIN_USER_EMAIL, "value": DEFAULT_ADMIN_USER_EMAIL}]
    try:
        admin_users = list(get_adapter().list_instance_admin_users())
    except Exception:
        admin_users = []
    if not admin_users:
        admin_users = [
            {
                "email": DEFAULT_ADMIN_USER_EMAIL,
                "userId": DEFAULT_ADMIN_USER_ID,
            }
        ]
    return [
        {
            "label": f"{admin_user['email']} ({admin_user['userId']})",
            "value": admin_user["email"],
        }
        for admin_user in admin_users
    ]


def first_admin_user_email() -> str:
    options = admin_user_options()
    return options[0]["value"] if options else DEFAULT_ADMIN_USER_EMAIL


def _format_date_display(value: str) -> str:
    """Format an ISO datetime string to `yyyy-mm-dd (ddd)`."""
    return _fmt_date(value)


def rows_from_dataclasses(rows: Any) -> list[dict[str, Any]]:
    normalized_rows = []
    for row in rows:
        row_dict = asdict(row)
        if "last_published" in row_dict:
            row_dict["last_published_display"] = _format_date_display(
                str(row_dict["last_published"])
            )
        if "updated_at" in row_dict:
            row_dict["updated_at_display"] = _format_date_display(
                str(row_dict["updated_at"])
            )
        normalized_rows.append(row_dict)
    return normalized_rows


def json_text(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True)


def empty_connector() -> dict[str, str]:
    return {
        "id": "",
        "name": "",
        "connector_type": "source",
        "latest_version": "",
        "docker_repository": "",
    }


# ---------------------------------------------------------------------------
# UI option renderers
# ---------------------------------------------------------------------------


def render_select_options(options: list[dict[str, str]]) -> None:
    for option in options:
        SelectOption(label=option["label"], value=option["value"])


def render_combobox_options(options: list[dict[str, str]]) -> None:
    for option in options:
        ComboboxOption(option["label"], value=option["value"])


# ---------------------------------------------------------------------------
# State action builders
# ---------------------------------------------------------------------------


def start_tool_call(message: str) -> list[SetState]:
    return [
        SetState("is_loading", True),
        SetState("loading_message", message),
        SetState("tool_error", ""),
    ]


def finish_tool_call() -> list[SetState]:
    return [
        SetState("is_loading", False),
        SetState("loading_message", ""),
        SetState("tool_error", ""),
    ]


def fail_tool_call(message: Any) -> list[Any]:
    return [
        SetState("is_loading", False),
        SetState("loading_message", ""),
        SetState("tool_error", message),
        ShowToast("Tool call failed", description=message, variant="error"),
        AppendState("notifications", message),
        SetState("has_unviewed_notifications", True),
    ]


def rollout_action_success_actions(
    toast_title: str = "Rollout action completed",
    refresh_message: str = "Refreshing rollouts\u2026",
) -> list[Any]:
    """Post-action feedback for a successful connector-version action.

    Shows a success toast, appends to the notifications panel, marks
    notifications as unviewed, clears the stale rollout selection, and
    refreshes the connector context (including active rollouts list).

    `toast_title` and `refresh_message` default to rollout-specific copy;
    non-rollout callers (e.g. `yank_connector_version`) pass their own copy so
    the toast and loading label reflect the action performed.
    """
    from airbyte_ops_webapp.pages.connector_version_manager._mcp_tools import (
        load_connector_context,
    )

    return [
        *finish_tool_call(),
        SetState("rollout_action_result", RESULT.rollout_action_result),
        SetState("rollout_action_success", RESULT.rollout_action_success),
        ShowToast(
            toast_title,
            description=RESULT.rollout_action_result,
            variant="success",
        ),
        AppendState("notifications", RESULT.rollout_action_result),
        SetState("has_unviewed_notifications", True),
        SetState("selected_rollout", EMPTY_ROLLOUT_STATE),
        SetState("rollout_action", ""),
        SetState("active_rollouts", []),
        SetState("rollout_summary", EMPTY_ROLLOUT_SUMMARY),
        # Refresh context to reload the active rollouts list from DB.
        *start_tool_call(refresh_message),
        CallTool(
            load_connector_context,
            arguments={
                "connector_id": STATE.selected_connector_id,
                "scope_type": STATE.scope_type,
                "scope_id": STATE.scope_id,
                "actor_workspace_id": STATE.actor_workspace_id,
                "context_guid": STATE.context_guid,
                "auth_bearer_token": STATE.auth_bearer_token,
            },
            on_success=[
                *context_success_actions(),
            ],
            on_error=fail_context_actions(),
        ),
    ]


def context_success_actions() -> list[Any]:
    return [
        *finish_tool_call(),
        SetState("selected_connector", RESULT.connector),
        SetState("target_version", RESULT.connector.latest_version),
        SetState("versions", RESULT.versions),
        SetState("active_rollouts", RESULT.active_rollouts),
        SetState("rollout_summary", RESULT.rollout_summary),
        SetState("current_state", RESULT.current_state),
        SetState("current_state_markdown", RESULT.current_state_markdown),
        SetState("ancestor_configs", RESULT.ancestor_configs),
        SetState("descendant_configs", RESULT.descendant_configs),
        SetState("resolved_context_label", RESULT.resolved_context_label),
        SetState("context_guid", RESULT.context_guid),
        SetState("scope_type", RESULT.scope_type),
        SetState("scope_id", RESULT.scope_id),
        SetState("actor_workspace_id", RESULT.actor_workspace_id),
        SetState("context_error", RESULT.context_error),
        SetState("rollout_error", RESULT.rollout_error),
        SetState("selected_rollout", EMPTY_ROLLOUT_STATE),
        SetState("rollout_action", ""),
        SetState("rollout_action_result", ""),
        SetState("rollout_action_success", False),
        SetState("rollout_modal_open", False),
    ]


def context_error_toast_actions() -> list[Any]:
    """Toast + bell notification for context errors.

    Only used by the explicit "Refresh context" button, not on automatic
    connector selection, so users aren't spammed with toasts on page load.
    """
    return [
        ShowToast(
            RESULT.context_error,
            variant="warning",
            duration=6000,
        ),
        AppendState("notifications", RESULT.context_error),
        SetState("has_unviewed_notifications", True),
    ]


def fail_context_actions() -> list[Any]:
    return [
        SetState("context_loading", False),
        *fail_tool_call(ERROR),
        SetState("context_error", ERROR),
        AppendState("notifications", ERROR),
        SetState("has_unviewed_notifications", True),
    ]


# ---------------------------------------------------------------------------
# Tool-layer helpers
# ---------------------------------------------------------------------------


def connector_context_placeholder(message: str) -> ConnectorContextResult:
    """Empty context payload shown before a connector is selected or on error.

    All other fields fall back to `ConnectorContextResult` defaults, which match
    the empty connector / rollout-summary placeholder shapes.
    """
    current_state: dict[str, Any] = {"message": message}
    return ConnectorContextResult(
        current_state=current_state,
        current_state_markdown=json_text(current_state),
        context_error=message,
    )


def fallback_current_state(
    connector: ConnectorOption,
    versions: list[dict[str, Any]],
) -> dict[str, Any]:
    latest_version = connector.latest_version
    return {
        "connector_id": connector.id,
        "connector_name": connector.name,
        "connector_type": connector.connector_type,
        "latest_version": latest_version,
        "active_version": latest_version,
        "is_version_pinned": False,
        "active_scope": "",
        "active_scope_id": "",
        "ancestor_configurations": [],
        "descendant_configurations": [],
    }


def context_error_message(error: Exception) -> str:
    message = str(error)
    if "401" in message or "Unauthorized" in message:
        return (
            "Airbyte Cloud rejected the scoped-configuration request. "
            "Sign out and back in with Airbyte."
        )
    return "Scoped configuration context could not be loaded."


def scope_context_needed_message() -> str:
    return (
        "Enter a Context GUID in Connector pinning tools and refresh to load "
        "scoped pin context."
    )


def version_rows_or_empty(
    adapter: OpsMcpAdapter,
    connector: ConnectorOption,
) -> tuple[list[dict[str, Any]], str]:
    try:
        return rows_from_dataclasses(adapter.list_versions(connector.id)), ""
    except PyAirbyteInputError as error:
        return [], context_error_message(error)


def rollout_rows_or_empty(
    adapter: OpsMcpAdapter,
    connector: ConnectorOption,
) -> tuple[list[dict[str, Any]], str]:
    try:
        rows = rows_from_dataclasses(adapter.list_active_rollouts(connector.id))
    except Exception:
        return [], "Progressive rollout status could not be loaded."
    for row in rows:
        connector_id = row.get("connector_id", "")
        rc_tag = row.get("rc_docker_image_tag")
        row["autopilot_display"] = _autopilot_display(connector_id, rc_tag)
        row["rc_pin_count_display"] = str(row.get("rc_pin_count", 0))
    return rows, ""


def build_rollout_summary(
    active_rollouts: list[dict[str, Any]],
    *,
    total_actors_display: str = "",
    tier_summaries: dict[str, RolloutSyncSummary] | None = None,
    eligible_by_tier: dict[str, int] | None = None,
    pinned_by_tier: dict[str, int] | None = None,
    factors_by_tier: dict[str, TierPopulationFactors] | None = None,
) -> dict[str, Any]:
    """Consolidate multiple tier rollouts into a single summary for the UI.

    `total_actors_display` is the connector-wide *enabled* actor count (active
    connections only, same across tiers), surfaced once on the rollout card
    rather than repeated per tier.

    `tier_summaries` maps a tier value (e.g. `"TIER_2"`) to the
    `RolloutSyncSummary` for that tier's *active* rollout. When supplied, one
    card per tier is emitted in `tier_cards`: the rollout line combines
    pinned/eligible counts with the target percentage (e.g.
    `20 pinned / 20 eligible (100%)`) and a health one-liner.

    `eligible_by_tier` maps a tier value to its enabled, addressable actor count
    from the DB population query. It is used to show `0 pinned / N eligible`
    on tiers whose rollout has *not* started, so future stages can be sized.

    `pinned_by_tier` maps a tier value to its *active-only* pinned actor count
    (`pinned_any_by_tier`), sourced from the same population as
    `eligible_by_tier`. When supplied it is preferred over the rollout scan's
    `num_pinned` for the numerator, guaranteeing `pinned <= eligible` on the
    card (the scan counts inactive/tombstoned pinned actors and can exceed the
    active eligible audience).

    `factors_by_tier` maps a tier value to its full `TierPopulationFactors`.
    When supplied, each tier card's two-column Actor Breakdown (via
    `build_tier_card` / `build_breakdown_columns`) partitions the population into
    an `Eligible` column (pinned — subdivided by post-pin health — and
    not-yet-pinned) and an `Ineligible` column (pinned to another version, no
    recent sync, recent failure), whose headers sum to `active`. It also drives
    the realized `Pinned` coverage on the compact Rollout Status line.
    """
    if not active_rollouts:
        return dict(EMPTY_ROLLOUT_SUMMARY)

    tier_summaries = tier_summaries or {}
    eligible_by_tier = eligible_by_tier or {}
    pinned_by_tier = pinned_by_tier or {}
    factors_by_tier = factors_by_tier or {}
    tier_index = {t.value: i for i, t in enumerate(TIER_ORDER)}
    sorted_rollouts = sorted(
        active_rollouts,
        key=lambda r: tier_index.get(r.get("tier", "TIER_2"), 0),
    )

    # Build per-tier summary string and per-tier cards
    tier_parts: list[str] = []
    tier_cards: list[dict[str, Any]] = []
    for display_tier, stage_value in _CARD_TIER_STAGES:
        # The full distinct-factor breakdown for this tier (traceable arithmetic
        # and both denominators). Built per branch below once the pinned-health
        # subdivision is known; empty when tier resolution was unavailable.
        factors = factors_by_tier.get(display_tier.value)
        matching = [r for r in sorted_rollouts if r.get("tier") == stage_value]
        eligible_fallback = eligible_by_tier.get(display_tier.value) or 0
        if matching:
            rollout = matching[0]
            pct = format_rollout_pct(rollout.get("current_target_rollout_pct"))
            # Only the current-stage percentage is surfaced (a single clean
            # backend-reported number); the final-goal field is not shown.
            deployed_pct = _pct_to_int(rollout.get("current_target_rollout_pct"))
            tier_parts.append(f"{display_tier.label}: {pct}")
            summary = tier_summaries.get(stage_value)
            # Post-pin health subdivision for the pinned cohort; populated from the
            # rollout scan below when available. `healthy | unhealthy | awaiting`
            # partition the active pinned set (`awaiting` absorbs active-pinned
            # actors with no terminal result yet). Fall back to no subdivision when
            # tier resolution is unavailable — the scan's `num_pinned` counts
            # inactive/tombstoned pinned actors and can exceed the active audience.
            succeeding: int | None = None
            failing: int | None = None
            awaiting_health: int | None = None
            active_pinned = pinned_by_tier.get(display_tier.value)
            if summary is not None and summary.health and active_pinned is not None:
                awaiting_health = max(
                    active_pinned - summary.num_healthy - summary.num_unhealthy,
                    0,
                )
                succeeding = summary.num_healthy
                failing = summary.num_unhealthy
            tier_cards.append(
                build_tier_card(
                    display_tier,
                    has_rollout=True,
                    state=str(rollout.get("state") or ""),
                    deployed_display=pct,
                    deployed_pct=deployed_pct,
                    factors=factors,
                    eligible_fallback=eligible_fallback,
                    succeeding=succeeding,
                    failing=failing,
                    awaiting=awaiting_health,
                )
            )
        else:
            # No *active rollout row* for this tier — it hasn't started. Eligible
            # actor counts still render (from `factors`, else `eligible_by_tier`)
            # so future stages can be sized, but the ⚪ status makes clear the
            # numbers are not live rollout data.
            tier_parts.append(f"{display_tier.label}: {_EM_DASH}")
            tier_cards.append(
                build_tier_card(
                    display_tier,
                    has_rollout=False,
                    deployed_display=_EM_DASH,
                    deployed_pct=0,
                    factors=factors,
                    eligible_fallback=eligible_fallback,
                )
            )

    # Highest tier is the last in sorted order
    highest_rollout = sorted_rollouts[-1]
    highest_tier_value = highest_rollout.get("tier", "TIER_2")
    highest_tier_idx = tier_index.get(highest_tier_value, 0)

    # Determine next tier
    next_tier = ""
    has_next_stage = False
    if highest_tier_idx < len(TIER_ORDER) - 1:
        next_tier = TIER_ORDER[highest_tier_idx + 1].value
        has_next_stage = True

    # Autopilot: use highest tier rollout's autopilot display
    autopilot = highest_rollout.get("autopilot_display", "OFF")

    # Updated at: most recent across all rollouts (formatted for display)
    raw_updated = max(
        (r.get("updated_at", "") for r in sorted_rollouts),
        default="",
    )
    updated_at = _fmt_date(raw_updated)

    # Total RC pins (use max, not sum — API returns same total per tier)
    total_pins = max(
        (int(r.get("rc_pin_count", 0)) for r in sorted_rollouts), default=0
    )

    # The "advance" targets the highest tier rollout
    # The "promote to GA" also targets the highest tier rollout
    return {
        "rc_version": highest_rollout.get("rc_docker_image_tag", ""),
        "tier_summary": " | ".join(tier_parts),
        "highest_tier": highest_tier_value,
        "next_tier": next_tier,
        "has_next_stage": has_next_stage,
        "autopilot": autopilot,
        "updated_at": updated_at,
        "total_rc_pins": str(total_pins),
        "total_actors_display": total_actors_display,
        "tier_cards": tier_cards,
        "connector_id": highest_rollout.get("connector_id", ""),
        "connector_name": highest_rollout.get("connector_name", ""),
        "docker_repository": highest_rollout.get("docker_repository", ""),
        "rc_docker_image_tag": highest_rollout.get("rc_docker_image_tag", ""),
        "advance_rollout_id": highest_rollout.get("rollout_id", ""),
        "advance_tier": highest_tier_value,
        "advance_pct": str(highest_rollout.get("current_target_rollout_pct", "0")),
        "promote_rollout_id": highest_rollout.get("rollout_id", ""),
    }


def target_ids(
    *,
    adapter: OpsMcpAdapter,
    scope_type: ScopeType,
    scope_id: str,
    actor_workspace_id: str,
) -> tuple[str, str | None, str | None]:
    if scope_type == "organization":
        return scope_id, None, None
    if scope_type == "actor":
        organization_id = (
            adapter.resolve_organization_id("workspace", actor_workspace_id)
            if actor_workspace_id
            else ""
        )
        return organization_id, actor_workspace_id or None, scope_id
    return (
        adapter.resolve_organization_id("workspace", scope_id),
        scope_id,
        None,
    )


def cloud_scope_url(
    *,
    scope_type: ScopeType,
    scope_id: str,
    workspace_id: str = "",
    actor_type: str = "",
) -> str:
    """Build an Airbyte Cloud URL for viewing the target scope."""
    return _cloud_scope_url(
        scope_type=scope_type,
        scope_id=scope_id,
        workspace_id=workspace_id,
        actor_type=actor_type,
    )
