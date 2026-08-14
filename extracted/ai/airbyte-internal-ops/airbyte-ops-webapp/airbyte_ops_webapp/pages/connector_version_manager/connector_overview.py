"""Connector Status section and rollout action confirmation modals."""

# ruff: noqa: SIM117

from __future__ import annotations

from prefab_ui.actions import Fetch, SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import (
    H2,
    H3,
    Button,
    CardContent,
    CardHeader,
    Column,
    Dialog,
    Div,
    Input,
    Link,
    Markdown,
    Muted,
    Row,
    Span,
    Text,
    Textarea,
    Tooltip,
)
from prefab_ui.components.control_flow import ForEach, If
from prefab_ui.rx import RESULT, STATE, LoopItem

from airbyte_ops_webapp.auth.oauth import OAUTH_SESSION_PATH
from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    fail_tool_call,
    render_loading_feedback,
    rollout_action_success_actions,
    start_tool_call,
)
from airbyte_ops_webapp.pages.connector_version_manager._mcp_tools import (
    FINALIZE_ROLLOUT_WORKFLOW_URL,
    YANK_STORE,
    advance_rollout,
    finalize_rollout,
    promote_to_next_stage,
    unyank_connector_version,
    yank_connector_version,
)
from airbyte_ops_webapp.theme import (
    BUTTON_DESTRUCTIVE_CLASS,
    BUTTON_INFO_CLASS,
    BUTTON_OUTLINE_CLASS,
    AbCard,
    AbFieldCaption,
)


def _refresh_token_then(on_success: list) -> Fetch:
    """Fetch a fresh OAuth token, then execute chained actions on success."""
    return Fetch.get(
        OAUTH_SESSION_PATH,
        on_success=[
            SetState("auth_bearer_token", RESULT.auth_bearer_token),
            SetState("oauth_user_email", RESULT.oauth_user_email),
            *on_success,
        ],
        on_error=fail_tool_call(
            "Session expired. Please sign in again to perform this action."
        ),
    )


def render_rollout_status_section(
    css_class: str = "",
) -> None:
    """Connector Version Status section (pivoted key-value layout).

    Shows connector name, UUID, version comparison, and rollout status
    with labels on the left and values on the right. `css_class` is applied
    to the panel surface so the caller can control its responsive width.
    """
    _render_promotion_pending_detail()

    with AbCard(css_class=css_class):
        with CardHeader():
            H2("Connector Version Status", css_class="text-lg")
        with CardContent(), Column(gap=3):
            # Loading state while connector context is being fetched
            with If(STATE.context_loading.__eq__(True)):
                render_loading_feedback("Loading connector status…")

            # Populated state
            with If(STATE.context_loading.__eq__(False)):
                _render_connector_identity_rows()
                _render_version_comparison_rows()

                # Always surface whether a rollout is active, so it's visible
                # even while reviewing a non-rollout version.
                _render_active_rollout_row()

                # Active rollout whose version matches the selected version:
                # render the full (compute-heavier) per-tier detail view. When a
                # different version is selected, the summary row above is enough.
                with If(
                    STATE.active_rollouts.length().__and__(
                        STATE.rollout_summary.rc_version.__eq__(
                            STATE.selected_version_tag
                        )
                    )
                ):
                    _render_active_rollout_detail()

                # Selected-version yank detail + yank/unyank action.
                _render_yank_controls()

    # Rollout confirmation modal (shared for all actions)
    _render_rollout_confirmation_modal()
    # Yank / Unyank confirmation modals
    _render_yank_confirmation_modal()
    _render_unyank_confirmation_modal()


def _pivoted_row(label: str, value: object) -> None:
    """Render a single label-value row for the pivoted connector status layout."""
    with Row(justify="between", align="baseline", gap=2):
        AbFieldCaption(label)
        Text(content=value, css_class="text-[0.85rem] text-right")


def _render_connector_identity_rows() -> None:
    """Pivoted rows for connector name and UUID."""
    _pivoted_row("Connector", STATE.selected_connector.name)
    with Row(justify="between", align="baseline", gap=2):
        AbFieldCaption("Connector ID")
        Muted(
            content=STATE.selected_connector.id,
            css_class="text-xs text-right break-all",
        )


def _render_version_comparison_rows() -> None:
    """Condensed rows comparing selected version against the default version.

    Each version and its release date collapse into a single row, e.g.
    `Selected Version: 1.2.0 (Tue, Mar 3, 2026)`.
    """
    _pivoted_row("Selected Version", STATE.selected_version_display)
    _pivoted_row("Default Version", STATE.default_version_display)


# Per-tier rollout card styling. Expressed as Tailwind utility classes (passed
# via `css_class`) per the theme convention — arbitrary-value classes carry the
# themed colors that lack a plain utility. See `CONTRIBUTING.md` → "Ops Webapp
# Styling".
_TIER_CARD_CLASS = "px-2.5 py-2 rounded-md border border-white/[0.12] bg-white/[0.02]"
_TIER_LABEL_CLASS = "text-[0.8rem] font-bold"
_TIER_STATUS_EMOJI_CLASS = "text-[0.85rem] leading-none"
_TIER_STATUS_LABEL_CLASS = (
    "text-[0.68rem] font-semibold uppercase tracking-[0.03em] text-[#9ca3af]"
)
_STATUS_METRIC_LABEL_CLASS = "text-[0.72rem] text-[#9ca3af]"
_STATUS_METRIC_VALUE_CLASS = "text-[0.78rem] tabular-nums"
_INFO_ICON_CLASS = "text-[0.7rem] text-[#9ca3af] cursor-help"
_BREAKDOWN_HEADER_CLASS = "text-[0.76rem] font-bold mb-0.5"
_BREAKDOWN_LINE_CLASS = "text-[0.72rem] text-[#cbd5e1] whitespace-pre tabular-nums"
_BREAKDOWN_COLUMN_CLASS = "min-w-[13rem]"

# Explanatory hover text for the backend-reported target percentage. Shown
# only on hover behind the ⓘ affordance — never rendered inline.
_DEPLOYED_TOOLTIP = (
    '"Target (backend)" is the configured rollout target reported by the backend. '
    "May not match exactly due to time lag and other factors."
)


def _status_metric(label: str, value: object) -> None:
    """Render one compact `label value` pair for the Rollout Status row."""
    with Row(gap=1, align="baseline"):
        Span(label, css_class=_STATUS_METRIC_LABEL_CLASS)
        Text(content=value, css_class=_STATUS_METRIC_VALUE_CLASS)


def _render_breakdown_line(line: LoopItem) -> None:
    """Render one indented Actor Breakdown row (already formatted text)."""
    Span(content=line.text, css_class=_BREAKDOWN_LINE_CLASS)


def _render_tier_card(card: LoopItem) -> None:
    """Render one per-tier rollout card.

    Layout, top to bottom:

    - A header line pairing the status glyph (heavy minus / `🔵 In progress` /
      `⚠️ Attention` / `☑️ Complete`) with the tier label and status word, so the
      rollout state is obvious before any numbers are read.
    - A compact `Rollout Status` row: `Target (backend)` (backend-reported target,
      with an ⓘ hover explaining it can lag), `Pinned` (realized coverage), and
      `Failed` (post-pin failure rate).
    - A two-column `Actor Breakdown`: `Eligible Actors` (pinned — subdivided by
      post-pin health — and not-yet-pinned) beside `Ineligible` (pinned to
      another version, no recent sync, recent failure).
    """
    with Div(css_class=_TIER_CARD_CLASS), Column(gap=1):
        with Row(gap=2, align="center"):
            Span(content=card.status_emoji, css_class=_TIER_STATUS_EMOJI_CLASS)
            Span(content=card.tier_label, css_class=_TIER_LABEL_CLASS)
            Span(content=card.status_label, css_class=_TIER_STATUS_LABEL_CLASS)
        with Row(gap=4, align="baseline", css_class="flex-wrap"):
            with Row(gap=1, align="baseline"):
                Span("Target (backend):", css_class=_STATUS_METRIC_LABEL_CLASS)
                Text(
                    content=card.deployed_display, css_class=_STATUS_METRIC_VALUE_CLASS
                )
                with Tooltip(_DEPLOYED_TOOLTIP):
                    Span(content="\u24d8", css_class=_INFO_ICON_CLASS)
            _status_metric("Pinned:", card.pinned_summary)
            _status_metric("Failed:", card.failed_summary)
        AbFieldCaption("Actor Breakdown")
        with Row(gap=4, align="start", css_class="flex-wrap"):
            with Div(css_class=_BREAKDOWN_COLUMN_CLASS), Column(gap=0):
                Span(content=card.eligible_header, css_class=_BREAKDOWN_HEADER_CLASS)
                with ForEach(card.eligible_rows) as line:
                    _render_breakdown_line(line)
            with Div(css_class=_BREAKDOWN_COLUMN_CLASS), Column(gap=0):
                Span(content=card.ineligible_header, css_class=_BREAKDOWN_HEADER_CLASS)
                with ForEach(card.ineligible_rows) as line:
                    _render_breakdown_line(line)
        with If(card.reason_display.__ne__("")):
            AbFieldCaption("Reason")
            Text(content=card.reason_display, css_class=_YANK_REASON_CLASS)


def _render_active_rollout_row() -> None:
    """Always-visible one-line summary of the connector's active rollout.

    Renders `Active Rollout: {version} ({updated})` when a rollout exists and
    `Active Rollout: (none)` when it does not. This keeps the rollout's existence
    visible regardless of which version is selected, while the compute-heavier
    per-tier detail view is rendered separately only when the rollout version
    matches the selected version.
    """
    with Row(justify="between", align="baseline", gap=2):
        AbFieldCaption("Active Rollout")
        with If(STATE.active_rollouts.length().__eq__(0)):
            Text(content="(none)", css_class="text-[0.85rem] text-right")
        with If(STATE.active_rollouts.length()):
            Text(
                content=STATE.rollout_summary.rc_version
                + " ("
                + STATE.rollout_summary.updated_at
                + ")",
                css_class="text-[0.85rem] text-right",
            )


def _render_active_rollout_detail() -> None:
    """Consolidated rollout detail from `STATE.rollout_summary`, one card per tier."""
    with (
        Div(css_class="p-3 rounded-md border border-white/10"),
        Column(gap=2),
    ):
        H3("Rollout Status", css_class="text-sm mb-1")
        _pivoted_row("Version", STATE.rollout_summary.rc_version)
        _pivoted_row("State", STATE.rollout_summary.state_display)
        _pivoted_row("Autopilot", STATE.rollout_summary.autopilot)
        _pivoted_row("Updated", STATE.rollout_summary.updated_at)
        # Connector-wide gated-eligible actor count (the backend's
        # `nActorsEligibleOrAlreadyPinned`), shown once above the per-tier cards.
        with If(STATE.rollout_summary.total_actors_display.__ne__("")):
            _pivoted_row("Eligible Actors", STATE.rollout_summary.total_actors_display)

        # Per-tier breakdown cards
        with ForEach(STATE.rollout_summary.tier_cards) as card:
            _render_tier_card(card)

        # Needs-review cue (amber = settling/paused, red = errored)
        _render_needs_review_banner()

        # Action buttons
        _render_rollout_action_buttons()


_REVIEW_BANNER_BASE_STYLE: dict[str, str] = {
    "padding": "0.5rem 0.625rem",
    "borderRadius": "0.375rem",
    "fontSize": "0.75rem",
    "marginTop": "0.5rem",
    "border": "1px solid",
}


def _render_needs_review_banner() -> None:
    """Amber/red banner shown when the rollout is in a state needing review."""
    with If(STATE.rollout_summary.needs_review):
        with If(STATE.rollout_summary.needs_review_severity.__eq__("red")):
            Text(
                content=STATE.rollout_summary.needs_review_reason,
                style={
                    **_REVIEW_BANNER_BASE_STYLE,
                    "backgroundColor": "rgba(180,35,24,0.15)",
                    "borderColor": "rgba(180,35,24,0.5)",
                    "color": "#fca5a5",
                },
            )
        with If(STATE.rollout_summary.needs_review_severity.__eq__("amber")):
            Text(
                content=STATE.rollout_summary.needs_review_reason,
                style={
                    **_REVIEW_BANNER_BASE_STYLE,
                    "backgroundColor": "rgba(217,119,6,0.15)",
                    "borderColor": "rgba(217,119,6,0.5)",
                    "color": "#fcd34d",
                },
            )


def _render_rollout_action_buttons() -> None:
    """Advance Rollout %, Promote to Next Stage, Promote to Default GA, Cancel."""
    with Column(gap=2, css_class="mt-2"):
        # Row 1: Advance and Cancel
        with Row(gap=2, css_class="flex-wrap"):
            Button(
                "Advance Rollout %",
                variant="info",
                css_class=BUTTON_INFO_CLASS,
                disabled=STATE.is_loading,
                on_click=[
                    SetState("rollout_action", "advance"),
                    SetState("rollout_modal_open", True),
                ],
            )
            Button(
                "Cancel Rollout",
                variant="destructive",
                css_class=BUTTON_DESTRUCTIVE_CLASS,
                disabled=STATE.is_loading,
                on_click=[
                    SetState("rollout_action", "cancel"),
                    SetState("rollout_modal_open", True),
                ],
            )

        # Row 2: Promote to Next Stage and Promote to Default GA
        with Row(gap=2, css_class="flex-wrap"):
            Button(
                "Promote to Next Stage",
                variant="outline",
                css_class=BUTTON_OUTLINE_CLASS,
                disabled=STATE.is_loading.__or__(
                    STATE.rollout_summary.has_next_stage.__eq__(False)
                ),
                on_click=[
                    SetState("rollout_action", "promote_next_stage"),
                    SetState("rollout_modal_open", True),
                ],
            )
            Button(
                "Promote to Default GA",
                variant="outline",
                css_class=BUTTON_OUTLINE_CLASS,
                disabled=STATE.is_loading,
                on_click=[
                    SetState("rollout_action", "promote_ga"),
                    SetState("rollout_modal_open", True),
                ],
            )

        # Row 3: Re-drive Finalize — only when a rollout is stuck finalizing
        with If(STATE.rollout_summary.is_finalizing):
            with Row(gap=2, css_class="flex-wrap"):
                Button(
                    "Re-drive Finalize",
                    variant="info",
                    css_class=BUTTON_INFO_CLASS,
                    disabled=STATE.is_loading,
                    on_click=[
                        SetState("rollout_action", "redrive_finalize"),
                        SetState("rollout_modal_open", True),
                    ],
                )


_YANK_DETAIL_CARD_CLASS = (
    "mt-2 px-2.5 py-2 rounded-md border border-white/[0.12] bg-white/[0.02]"
)
# Marker values render in a full-width code block so long content (reason
# prose, unbreakable approval URLs) wraps inside the card instead of
# overflowing the parent. URLs break anywhere; reason preserves its wrapping.
_YANK_CODE_BLOCK_CLASS = (
    "text-[0.72rem] font-mono p-2 rounded bg-black/20 border border-white/[0.08]"
)
_YANK_REASON_CLASS = f"{_YANK_CODE_BLOCK_CLASS} whitespace-pre-wrap break-words"
_YANK_URL_CLASS = f"{_YANK_CODE_BLOCK_CLASS} break-all"


def _render_yank_controls() -> None:
    """Yank detail + yank/unyank action for the selected version.

    When the selected version is yanked, show the Version Yank Detail card and
    an Unyank action regardless of any unrelated active rollout. Otherwise offer
    Yank for any non-yanked selected version *except* the version that is
    actively being rolled out: "Yank" overlaps with "Cancel Rollout" only for
    the active RC version (mirroring the `rc_version == selected_version_tag`
    gating of the Rollout Status detail), so a non-RC released version stays
    yankable even while an unrelated rollout is in progress.
    """
    with If(STATE.selected_version_tag):
        with If(STATE.selected_version_yanked.__eq__(True)):
            _render_yank_detail_section()
            _render_unyank_section()
        with If(STATE.selected_version_yanked.__eq__(False)):
            with If(
                STATE.active_rollouts.length()
                .__eq__(0)
                .__or__(
                    STATE.rollout_summary.rc_version.__ne__(STATE.selected_version_tag)
                )
            ):
                _render_yank_section()


def _render_yank_detail_section() -> None:
    """Version Yank Detail card, shown when the selected version is yanked.

    Renders the parsed marker fields (yanked date, reason, approval URL) from
    the `version-yank.yml` marker. Reason and approval URL use full-width code
    blocks so long values wrap inside the card rather than overflowing it.
    """
    with Div(css_class=_YANK_DETAIL_CARD_CLASS), Column(gap=2):
        H3("Version Yank Detail", css_class="text-sm")
        _pivoted_row("Yanked At", STATE.selected_version_yank_yanked_at_display)
        with If(STATE.selected_version_yank_reason.__ne__("")):
            AbFieldCaption("Reason")
            Text(
                content=STATE.selected_version_yank_reason,
                css_class=_YANK_REASON_CLASS,
            )
        with If(STATE.selected_version_yank_approval_url.__ne__("")):
            AbFieldCaption("Approval URL")
            Text(
                content=STATE.selected_version_yank_approval_url,
                css_class=_YANK_URL_CLASS,
            )


def _render_unyank_section() -> None:
    """Unyank Version action, shown when the selected version is yanked."""
    with Row(gap=2, css_class="mt-2 flex-wrap"):
        Button(
            "Unyank Version",
            variant="destructive",
            css_class=BUTTON_DESTRUCTIVE_CLASS,
            disabled=STATE.is_loading,
            on_click=[SetState("unyank_modal_open", True)],
        )


def _render_yank_section() -> None:
    """Yank Version action for a non-yanked, non-RC selected version.

    Gated by `_render_yank_controls`: shown for any non-yanked selected version
    except the active RC version (which uses "Cancel Rollout" instead), so a
    released version stays yankable even while an unrelated rollout is active.
    """
    with Row(gap=2, css_class="mt-2 flex-wrap"):
        Button(
            "Yank Version",
            variant="destructive",
            css_class=BUTTON_DESTRUCTIVE_CLASS,
            disabled=STATE.is_loading,
            on_click=[
                SetState("yank_reason", ""),
                SetState("yank_reference_url", ""),
                SetState("yank_modal_open", True),
            ],
        )


def _render_promotion_pending_detail() -> None:
    """Promotion detail for a version undergoing asynchronous GA rollout."""
    with If(STATE.selected_version_promotion_pending.__eq__(True)):
        with Div(css_class=_YANK_DETAIL_CARD_CLASS), Column(gap=2):
            with If(STATE.selected_version_promotion_state.__eq__("active")):
                H3("Promotion Pending", css_class="text-sm")
            with If(STATE.selected_version_promotion_state.__eq__("promoted")):
                H3("Promotion Completed", css_class="text-sm")
                Text(
                    "Promotion completed the marker-finalize step.",
                    css_class="text-xs text-[#cbd5e1]",
                )
                _pivoted_row(
                    "Marker Date",
                    STATE.selected_version_promotion_marker_date,
                )
            with If(STATE.selected_version_promotion_state.__eq__("aborted")):
                H3("Promotion Aborted", css_class="text-sm")
                Text(
                    "The promotion marker-finalize step was aborted.",
                    css_class="text-xs text-[#cbd5e1]",
                )
                _pivoted_row(
                    "Marker Date",
                    STATE.selected_version_promotion_marker_date,
                )
            with If(STATE.selected_version_promotion_requested_by):
                _pivoted_row(
                    "Requested By",
                    STATE.selected_version_promotion_requested_by,
                )
            with If(STATE.selected_version_promotion_requested_at_display):
                _pivoted_row(
                    "Requested At",
                    STATE.selected_version_promotion_requested_at_display,
                )
            with If(STATE.selected_version_promotion_rollout_id):
                _pivoted_row(
                    "Rollout ID",
                    STATE.selected_version_promotion_rollout_id,
                )
            Text(
                content=(
                    "Registry compile and default-version rollout finish "
                    "asynchronously. Refresh this page to check."
                ),
                css_class="text-xs text-[#cbd5e1]",
            )
            Link(
                "Monitor the promotion job in GitHub Actions",
                href=FINALIZE_ROLLOUT_WORKFLOW_URL,
                target="_blank",
                css_class="text-xs underline",
            )


# ---------------------------------------------------------------------------
# Confirmation modals
# ---------------------------------------------------------------------------


def _render_rollout_confirmation_modal() -> None:
    """Confirmation dialog for rollout actions."""
    with Dialog(
        title="Confirm Rollout Action",
        description="Please confirm the rollout action below.",
        name="rollout_modal_open",
    ):
        Button("", css_class="hidden")

        # --- Advance Rollout % ---
        with If(STATE.rollout_action.__eq__("advance")):
            with Column(gap=4):
                Markdown(
                    content="**Advance rollout percentage?**\n\n"
                    "RC: "
                    + STATE.rollout_summary.rc_docker_image_tag
                    + " — Current tier: "
                    + STATE.rollout_summary.advance_tier
                )
                with Column(gap=1):
                    Markdown("**Target Percentage** (leave blank to auto-increment)")
                    Input(
                        name="rollout_target_percentage",
                        value=STATE.rollout_target_percentage,
                        placeholder="e.g. 50",
                    )
                with Row(justify="end", gap=2):
                    Button(
                        "Cancel",
                        variant="outline",
                        css_class=BUTTON_OUTLINE_CLASS,
                        on_click=[SetState("rollout_modal_open", False)],
                    )
                    Button(
                        "Confirm",
                        variant="info",
                        css_class=BUTTON_INFO_CLASS,
                        disabled=STATE.is_loading,
                        on_click=[
                            SetState("rollout_modal_open", False),
                            *start_tool_call("Advancing rollout…"),
                            _refresh_token_then(
                                [
                                    CallTool(
                                        advance_rollout,
                                        arguments={
                                            "rollout_id": STATE.rollout_summary.advance_rollout_id,
                                            "connector_id": STATE.rollout_summary.connector_id,
                                            "docker_repository": STATE.rollout_summary.docker_repository,
                                            "docker_image_tag": STATE.rollout_summary.rc_docker_image_tag,
                                            "target_percentage": STATE.rollout_target_percentage,
                                            "auth_bearer_token": STATE.auth_bearer_token,
                                            "user_email": STATE.oauth_user_email,
                                        },
                                        on_success=rollout_action_success_actions(),
                                        on_error=fail_tool_call(
                                            "Advance rollout failed."
                                        ),
                                    ),
                                ]
                            ),
                        ],
                    )

        # --- Promote to Next Stage ---
        with If(STATE.rollout_action.__eq__("promote_next_stage")):
            with Column(gap=4):
                Markdown(
                    content="**Promote to next stage?**\n\n"
                    "This will start a new rollout at the next tier for "
                    + STATE.rollout_summary.rc_docker_image_tag
                    + "."
                )
                with Row(justify="end", gap=2):
                    Button(
                        "Cancel",
                        variant="outline",
                        css_class=BUTTON_OUTLINE_CLASS,
                        on_click=[SetState("rollout_modal_open", False)],
                    )
                    Button(
                        "Confirm",
                        variant="info",
                        css_class=BUTTON_INFO_CLASS,
                        disabled=STATE.is_loading,
                        on_click=[
                            SetState("rollout_modal_open", False),
                            *start_tool_call("Promoting to next stage…"),
                            _refresh_token_then(
                                [
                                    CallTool(
                                        promote_to_next_stage,
                                        arguments={
                                            "connector_id": STATE.rollout_summary.connector_id,
                                            "docker_repository": STATE.rollout_summary.docker_repository,
                                            "docker_image_tag": STATE.rollout_summary.rc_docker_image_tag,
                                            "next_tier": STATE.rollout_summary.next_tier,
                                            "auth_bearer_token": STATE.auth_bearer_token,
                                            "user_email": STATE.oauth_user_email,
                                        },
                                        on_success=rollout_action_success_actions(),
                                        on_error=fail_tool_call(
                                            "Promote to next stage failed."
                                        ),
                                    ),
                                ]
                            ),
                        ],
                    )

        # --- Promote to Default GA ---
        with If(STATE.rollout_action.__eq__("promote_ga")):
            with Column(gap=4):
                Markdown(
                    content="**Promote "
                    + STATE.selected_connector.name
                    + " to Default GA?**"
                )
                with Column(gap=1):
                    Text(
                        content=("Current default: " + STATE.ga_default_version_display)
                    )
                    Text(content="Promoting: " + STATE.promoting_version_display)
                Text(
                    content=(
                        "This makes "
                        + STATE.rollout_summary.rc_docker_image_tag
                        + " the default version for all users, replacing "
                        + STATE.ga_default_version_tag
                        + "."
                    )
                )
                with Row(justify="end", gap=2):
                    Button(
                        "Cancel",
                        variant="outline",
                        css_class=BUTTON_OUTLINE_CLASS,
                        on_click=[SetState("rollout_modal_open", False)],
                    )
                    Button(
                        "Confirm",
                        variant="info",
                        css_class=BUTTON_INFO_CLASS,
                        disabled=STATE.is_loading,
                        on_click=[
                            SetState("rollout_modal_open", False),
                            *start_tool_call("Promoting rollout to GA…"),
                            _refresh_token_then(
                                [
                                    CallTool(
                                        finalize_rollout,
                                        arguments={
                                            "rollout_id": STATE.rollout_summary.promote_rollout_id,
                                            "connector_id": STATE.rollout_summary.connector_id,
                                            "docker_repository": STATE.rollout_summary.docker_repository,
                                            "docker_image_tag": STATE.rollout_summary.rc_docker_image_tag,
                                            "state": "succeeded",
                                            "auth_bearer_token": STATE.auth_bearer_token,
                                            "user_email": STATE.oauth_user_email,
                                        },
                                        on_success=rollout_action_success_actions(),
                                        on_error=fail_tool_call(
                                            "Promote rollout failed."
                                        ),
                                    ),
                                ]
                            ),
                        ],
                    )

        # --- Cancel Rollout ---
        with If(STATE.rollout_action.__eq__("cancel")):
            with Column(gap=4):
                Markdown(
                    content="**Cancel rollout?**\n\n"
                    "This will stop the progressive rollout and "
                    "roll back affected users."
                )
                with Row(justify="end", gap=2):
                    Button(
                        "Cancel",
                        variant="outline",
                        css_class=BUTTON_OUTLINE_CLASS,
                        on_click=[SetState("rollout_modal_open", False)],
                    )
                    Button(
                        "Confirm",
                        variant="destructive",
                        css_class=BUTTON_DESTRUCTIVE_CLASS,
                        disabled=STATE.is_loading,
                        on_click=[
                            SetState("rollout_modal_open", False),
                            *start_tool_call("Canceling rollout…"),
                            _refresh_token_then(
                                [
                                    CallTool(
                                        finalize_rollout,
                                        arguments={
                                            "rollout_id": STATE.rollout_summary.promote_rollout_id,
                                            "connector_id": STATE.rollout_summary.connector_id,
                                            "docker_repository": STATE.rollout_summary.docker_repository,
                                            "docker_image_tag": STATE.rollout_summary.rc_docker_image_tag,
                                            "state": "canceled",
                                            "auth_bearer_token": STATE.auth_bearer_token,
                                            "user_email": STATE.oauth_user_email,
                                        },
                                        on_success=rollout_action_success_actions(),
                                        on_error=fail_tool_call(
                                            "Cancel rollout failed."
                                        ),
                                    ),
                                ]
                            ),
                        ],
                    )

        # --- Re-drive Finalize ---
        with If(STATE.rollout_action.__eq__("redrive_finalize")):
            with Column(gap=4):
                Markdown(
                    content="**Re-drive a stuck finalize?**\n\n"
                    "This rollout is `finalizing`. If "
                    + STATE.rollout_summary.finalizing_rc_docker_image_tag
                    + " is already the registry default, re-finalizing spawns a "
                    "fresh Temporal run that closes the rollout as succeeded. "
                    "If the default has not flipped yet, wait for the promote "
                    "workflow to publish it first."
                )
                with Row(justify="end", gap=2):
                    Button(
                        "Cancel",
                        variant="outline",
                        css_class=BUTTON_OUTLINE_CLASS,
                        on_click=[SetState("rollout_modal_open", False)],
                    )
                    Button(
                        "Confirm",
                        variant="info",
                        css_class=BUTTON_INFO_CLASS,
                        disabled=STATE.is_loading,
                        on_click=[
                            SetState("rollout_modal_open", False),
                            *start_tool_call("Re-driving finalize…"),
                            _refresh_token_then(
                                [
                                    CallTool(
                                        finalize_rollout,
                                        arguments={
                                            "rollout_id": STATE.rollout_summary.finalizing_rollout_id,
                                            "connector_id": STATE.rollout_summary.finalizing_connector_id,
                                            "docker_repository": STATE.rollout_summary.finalizing_docker_repository,
                                            "docker_image_tag": STATE.rollout_summary.finalizing_rc_docker_image_tag,
                                            "state": "succeeded",
                                            "auth_bearer_token": STATE.auth_bearer_token,
                                            "user_email": STATE.oauth_user_email,
                                        },
                                        on_success=rollout_action_success_actions(),
                                        on_error=fail_tool_call(
                                            "Re-drive finalize failed."
                                        ),
                                    ),
                                ]
                            ),
                        ],
                    )


def _render_yank_confirmation_modal() -> None:
    """Confirmation dialog for yanking the selected connector version."""
    with Dialog(
        title="Yank Version",
        description="Withdraw a released connector version from the registry.",
        name="yank_modal_open",
    ):
        Button("", css_class="hidden")

        with Column(gap=4):
            Markdown(
                content="**Yank this version?**\n\n"
                "This dispatches the registry yank workflow for "
                + STATE.selected_connector.name
                + " "
                + STATE.selected_version_tag
                + " on "
                + YANK_STORE
                + ". The version will be marked as yanked and excluded from "
                "latest-version resolution after the registry recompiles."
            )
            with Column(gap=1):
                Markdown("**Reason** (recorded in the yank marker)")
                Textarea(
                    name="yank_reason",
                    value=STATE.yank_reason,
                    placeholder="e.g. Critical regression in released version",
                    rows=3,
                )
            with Column(gap=1):
                Markdown(
                    "**Reference URL** — optional "
                    "(GitHub issue/PR, recorded in the yank marker for audit)"
                )
                Input(
                    name="yank_reference_url",
                    value=STATE.yank_reference_url,
                    placeholder="https://github.com/airbytehq/airbyte/issues/...",
                )
            with Row(justify="end", gap=2):
                Button(
                    "Cancel",
                    variant="outline",
                    css_class=BUTTON_OUTLINE_CLASS,
                    on_click=[SetState("yank_modal_open", False)],
                )
                Button(
                    "Confirm Yank",
                    variant="destructive",
                    css_class=BUTTON_DESTRUCTIVE_CLASS,
                    disabled=STATE.is_loading,
                    on_click=[
                        SetState("yank_modal_open", False),
                        *start_tool_call("Yanking version…"),
                        _refresh_token_then(
                            [
                                CallTool(
                                    yank_connector_version,
                                    arguments={
                                        "connector_name": STATE.selected_connector.name,
                                        "version": STATE.selected_version_tag,
                                        "reason": STATE.yank_reason,
                                        "reference_url": STATE.yank_reference_url,
                                    },
                                    on_success=rollout_action_success_actions(
                                        toast_title="Version yanked",
                                        refresh_message="Refreshing connector context\u2026",
                                    ),
                                    on_error=fail_tool_call("Yank version failed."),
                                ),
                            ]
                        ),
                    ],
                )


def _render_unyank_confirmation_modal() -> None:
    """Confirmation dialog for unyanking the selected connector version."""
    with Dialog(
        title="Unyank Version",
        description="Restore a previously yanked connector version.",
        name="unyank_modal_open",
    ):
        Button("", css_class="hidden")

        with Column(gap=4):
            Markdown(
                content="**Unyank this version?**\n\n"
                "This dispatches the registry yank workflow with `unyank: true` "
                "for "
                + STATE.selected_connector.name
                + " "
                + STATE.selected_version_tag
                + " on "
                + YANK_STORE
                + ". The active yank marker is moved to an audit marker and the "
                "version rejoins latest-version resolution after the registry "
                "recompiles."
            )
            with Row(justify="end", gap=2):
                Button(
                    "Cancel",
                    variant="outline",
                    css_class=BUTTON_OUTLINE_CLASS,
                    on_click=[SetState("unyank_modal_open", False)],
                )
                Button(
                    "Confirm Unyank",
                    variant="outline",
                    css_class=BUTTON_INFO_CLASS,
                    disabled=STATE.is_loading,
                    on_click=[
                        SetState("unyank_modal_open", False),
                        *start_tool_call("Unyanking version…"),
                        _refresh_token_then(
                            [
                                CallTool(
                                    unyank_connector_version,
                                    arguments={
                                        "connector_name": STATE.selected_connector.name,
                                        "version": STATE.selected_version_tag,
                                    },
                                    on_success=rollout_action_success_actions(
                                        toast_title="Version unyanked",
                                        refresh_message="Refreshing connector context\u2026",
                                    ),
                                    on_error=fail_tool_call("Unyank version failed."),
                                ),
                            ]
                        ),
                    ],
                )
