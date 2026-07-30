# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the CI-side HITL Slack message builder and MCP tool mapping."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from airbyte_ops_mcp import slack_posting
from airbyte_ops_mcp.human_in_the_loop import (
    APPROVAL_REQUEST_SUMMARY_MAX_LENGTH,
    classify_person_id,
    dispatch_escalation,
    normalize_person_id,
    validate_approval_request_summary,
    validate_person_id,
)
from airbyte_ops_mcp.mcp.human_in_the_loop import (
    _NEWSLETTER_CHANNELS,
    RequestType,
    escalate_to_human,
)

SESSION_URL = "https://app.devin.ai/sessions/abc123def456"
DETAIL_URL = "https://github.com/airbytehq/airbyte/pull/123"

_build_slack_blocks = slack_posting._build_hitl_blocks
_format_mention = slack_posting._format_mention
_resolve_to_slack_id = slack_posting._resolve_to_slack_id
send_hitl_notification = slack_posting.send_hitl_notification


def _find_actions_block(blocks: list[dict]) -> dict | None:
    """Return the first 'actions' block, or None."""
    for block in blocks:
        if block.get("type") == "actions":
            return block
    return None


def _get_action_ids(actions_block: dict) -> list[str]:
    """Extract action_ids from an actions block."""
    return [e.get("action_id", "") for e in actions_block.get("elements", [])]


def _get_element_by_action_id(actions_block: dict, action_id: str) -> dict | None:
    """Get a specific element from an actions block by action_id."""
    for element in actions_block.get("elements", []):
        if element.get("action_id") == action_id:
            return element
    return None


@pytest.mark.unit
@pytest.mark.parametrize(
    "approval_requested, expected_present, expected_absent",
    [
        pytest.param(
            True,
            ["approve_request", "reject_request"],
            [],
            id="approval_requested_true",
        ),
        pytest.param(
            False,
            [],
            ["approve_request", "reject_request"],
            id="approval_requested_false",
        ),
    ],
)
def test_approval_buttons_presence(
    approval_requested: bool,
    expected_present: list[str],
    expected_absent: list[str],
) -> None:
    """Approve and Reject buttons appear only when approval_requested=True."""
    blocks = _build_slack_blocks(
        target_person="aaronsteers",
        target_slack_id="U12345",
        cc_mentions=[],
        message="Test message.",
        agent_session_url=SESSION_URL,
        pr_url=None,
        issue_url=None,
        additional_actions=None,
        approval_requested=approval_requested,
    )
    actions_block = _find_actions_block(blocks)
    assert actions_block is not None
    action_ids = _get_action_ids(actions_block)
    for aid in expected_present:
        assert aid in action_ids
    for aid in expected_absent:
        assert aid not in action_ids


@pytest.mark.unit
@pytest.mark.parametrize(
    "action_id, expected_style",
    [
        pytest.param("approve_request", "primary", id="approve_is_primary"),
        pytest.param("reject_request", "danger", id="reject_is_danger"),
    ],
)
def test_approval_button_styles(action_id: str, expected_style: str) -> None:
    """Approve uses 'primary' style; Reject uses 'danger' style."""
    blocks = _build_slack_blocks(
        target_person="aaronsteers",
        target_slack_id="U12345",
        cc_mentions=[],
        message="Approve this.",
        agent_session_url=SESSION_URL,
        pr_url=None,
        issue_url=None,
        additional_actions=None,
        approval_requested=True,
    )
    actions_block = _find_actions_block(blocks)
    assert actions_block is not None
    btn = _get_element_by_action_id(actions_block, action_id)
    assert btn is not None
    assert btn.get("style") == expected_style


@pytest.mark.unit
def test_reject_button_carries_session_url() -> None:
    """The Reject button value should contain the session URL (same as Approve)."""
    blocks = _build_slack_blocks(
        target_person="aaronsteers",
        target_slack_id="U12345",
        cc_mentions=[],
        message="Approve this.",
        agent_session_url=SESSION_URL,
        pr_url=None,
        issue_url=None,
        additional_actions=None,
        approval_requested=True,
    )
    actions_block = _find_actions_block(blocks)
    assert actions_block is not None
    reject_btn = _get_element_by_action_id(actions_block, "reject_request")
    assert reject_btn is not None
    value = json.loads(reject_btn["value"])
    assert value["session_url"] == SESSION_URL


@pytest.mark.unit
@pytest.mark.parametrize(
    "action_id, expected_title, expected_confirm_text",
    [
        pytest.param(
            "approve_request",
            "Confirm Approval",
            "Yes, Approve",
            id="approve_confirm_dialog",
        ),
        pytest.param(
            "reject_request",
            "Confirm Rejection",
            "Yes, Reject",
            id="reject_confirm_dialog",
        ),
    ],
)
def test_confirmation_dialogs(
    action_id: str, expected_title: str, expected_confirm_text: str
) -> None:
    """Both buttons get confirmation dialogs when summary is provided."""
    blocks = _build_slack_blocks(
        target_person="aaronsteers",
        target_slack_id="U12345",
        cc_mentions=[],
        message="Approve this.",
        agent_session_url=SESSION_URL,
        pr_url=None,
        issue_url=None,
        additional_actions=None,
        approval_requested=True,
        approval_request_summary="Deploy v2.0 to prod",
    )
    actions_block = _find_actions_block(blocks)
    assert actions_block is not None
    btn = _get_element_by_action_id(actions_block, action_id)
    assert btn is not None
    assert "confirm" in btn
    assert btn["confirm"]["title"]["text"] == expected_title
    assert btn["confirm"]["confirm"]["text"] == expected_confirm_text


@pytest.mark.unit
@pytest.mark.parametrize(
    "detail_url, expect_button",
    [
        pytest.param(DETAIL_URL, True, id="detail_url_provided"),
        pytest.param(None, False, id="detail_url_absent"),
    ],
)
def test_view_details_button_presence(
    detail_url: str | None, expect_button: bool
) -> None:
    """View Details button appears only when approval_request_detail_url is set."""
    blocks = _build_slack_blocks(
        target_person="aaronsteers",
        target_slack_id="U12345",
        cc_mentions=[],
        message="Approve this.",
        agent_session_url=SESSION_URL,
        pr_url=None,
        issue_url=None,
        additional_actions=None,
        approval_requested=True,
        approval_request_detail_url=detail_url,
    )
    actions_block = _find_actions_block(blocks)
    assert actions_block is not None
    action_ids = _get_action_ids(actions_block)
    if expect_button:
        assert "view_approval_details" in action_ids
        btn = _get_element_by_action_id(actions_block, "view_approval_details")
        assert btn is not None
        assert btn["url"] == detail_url
        assert btn["text"]["text"] == "View Details"
    else:
        assert "view_approval_details" not in action_ids


@pytest.mark.unit
def test_view_details_without_approval() -> None:
    """View Details button works even without approval_requested=True."""
    blocks = _build_slack_blocks(
        target_person="aaronsteers",
        target_slack_id="U12345",
        cc_mentions=[],
        message="FYI.",
        agent_session_url=SESSION_URL,
        pr_url=None,
        issue_url=None,
        additional_actions=None,
        approval_requested=False,
        approval_request_detail_url=DETAIL_URL,
    )
    actions_block = _find_actions_block(blocks)
    assert actions_block is not None
    assert "view_approval_details" in _get_action_ids(actions_block)


@pytest.mark.unit
def test_approval_buttons_appear_first() -> None:
    """Approve and Reject buttons are the first two buttons when approval_requested=True."""
    blocks = _build_slack_blocks(
        target_person="aaronsteers",
        target_slack_id="U12345",
        cc_mentions=[],
        message="Approve this.",
        agent_session_url=SESSION_URL,
        pr_url="https://github.com/airbytehq/repo/pull/99",
        issue_url="https://github.com/airbytehq/repo/issues/42",
        additional_actions={"Run CI": "https://github.com/actions/run/1"},
        approval_requested=True,
        approval_request_detail_url=DETAIL_URL,
    )
    actions_block = _find_actions_block(blocks)
    assert actions_block is not None
    action_ids = _get_action_ids(actions_block)
    # Approve and Reject must be the first two buttons, View Details third
    assert action_ids[0] == "approve_request"
    assert action_ids[1] == "reject_request"
    assert action_ids[2] == "view_approval_details"
    # Other buttons follow after
    assert "view_pr" in action_ids
    assert "view_issue" in action_ids
    assert "view_session" in action_ids
    # View Details immediately follows Reject, before any link buttons
    details_idx = action_ids.index("view_approval_details")
    for link_id in ["view_pr", "view_issue", "view_session"]:
        assert action_ids.index(link_id) > details_idx, (
            f"{link_id} (index {action_ids.index(link_id)}) should come after "
            f"view_approval_details (index {details_idx})"
        )


@pytest.mark.unit
@pytest.mark.parametrize(
    "approval_requested, first_button_should_be_primary",
    [
        pytest.param(False, True, id="no_approval_first_btn_primary"),
        pytest.param(True, False, id="with_approval_pr_btn_not_primary"),
    ],
)
def test_primary_style_on_first_button(
    approval_requested: bool, first_button_should_be_primary: bool
) -> None:
    """Primary style is set on first button only when no approval buttons exist."""
    blocks = _build_slack_blocks(
        target_person="aaronsteers",
        target_slack_id="U12345",
        cc_mentions=[],
        message="Test.",
        agent_session_url=SESSION_URL,
        pr_url="https://github.com/airbytehq/repo/pull/1",
        issue_url=None,
        additional_actions=None,
        approval_requested=approval_requested,
    )
    actions_block = _find_actions_block(blocks)
    assert actions_block is not None
    pr_btn = _get_element_by_action_id(actions_block, "view_pr")
    assert pr_btn is not None
    if first_button_should_be_primary:
        assert pr_btn.get("style") == "primary"
    else:
        assert pr_btn.get("style") != "primary"


def _find_header_block(blocks: list[dict]) -> dict | None:
    """Return the first 'header' block, or None."""
    for block in blocks:
        if block.get("type") == "header":
            return block
    return None


def _find_context_blocks(blocks: list[dict]) -> list[dict]:
    """Return all 'context' blocks."""
    return [b for b in blocks if b.get("type") == "context"]


@pytest.mark.unit
def test_connector_name_in_header() -> None:
    """When connector_name is provided, it appears in the header block text."""
    blocks = _build_slack_blocks(
        target_person="aaronsteers",
        target_slack_id="U12345",
        cc_mentions=[],
        message="Test.",
        agent_session_url=SESSION_URL,
        pr_url=None,
        issue_url=None,
        additional_actions=None,
        connector_name="source-postgres",
    )
    header = _find_header_block(blocks)
    assert header is not None
    header_text = header["text"]["text"]
    assert "source-postgres" in header_text
    assert "—" in header_text  # em dash separator


@pytest.mark.unit
def test_connector_name_not_in_context_line() -> None:
    """When connector_name is provided, it should NOT appear as 'Re:' in the context line."""
    blocks = _build_slack_blocks(
        target_person="aaronsteers",
        target_slack_id="U12345",
        cc_mentions=[],
        message="Test.",
        agent_session_url=SESSION_URL,
        pr_url=None,
        issue_url=None,
        additional_actions=None,
        connector_name="source-postgres",
    )
    context_blocks = _find_context_blocks(blocks)
    for ctx in context_blocks:
        for elem in ctx.get("elements", []):
            text = elem.get("text", "")
            assert "Re:" not in text, f"Found 'Re:' in context block: {text}"


@pytest.mark.unit
def test_no_connector_name_header_unchanged() -> None:
    """Without connector_name, the header uses only emoji + label."""
    blocks = _build_slack_blocks(
        target_person="aaronsteers",
        target_slack_id="U12345",
        cc_mentions=[],
        message="Test.",
        agent_session_url=SESSION_URL,
        pr_url=None,
        issue_url=None,
        additional_actions=None,
        header_emoji="🔧",
        header_label="Action Requested",
    )
    header = _find_header_block(blocks)
    assert header is not None
    assert header["text"]["text"] == "🔧 Action Requested"


@pytest.mark.unit
def test_custom_header_emoji_and_label() -> None:
    """Custom header_emoji and header_label are used in the header block."""
    blocks = _build_slack_blocks(
        target_person="aaronsteers",
        target_slack_id="U12345",
        cc_mentions=[],
        message="Test.",
        agent_session_url=SESSION_URL,
        pr_url=None,
        issue_url=None,
        additional_actions=None,
        header_emoji="👀",
        header_label="Review Requested",
    )
    header = _find_header_block(blocks)
    assert header is not None
    assert header["text"]["text"] == "👀 Review Requested"


@pytest.mark.unit
def test_custom_header_with_connector_name() -> None:
    """Custom header + connector_name produces combined header text."""
    blocks = _build_slack_blocks(
        target_person="aaronsteers",
        target_slack_id="U12345",
        cc_mentions=[],
        message="Test.",
        agent_session_url=SESSION_URL,
        pr_url=None,
        issue_url=None,
        additional_actions=None,
        header_emoji="✅",
        header_label="Approval Requested",
        connector_name="source-hubspot",
    )
    header = _find_header_block(blocks)
    assert header is not None
    assert header["text"]["text"] == "✅ Approval Requested — source-hubspot"


# ---------------------------------------------------------------------------
# MCP tool: request_type → header resolution
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_newsletter_channel_resolution() -> None:
    """Newsletter names resolve to their expected Slack channels."""
    assert _NEWSLETTER_CHANNELS["DR"] == (
        "C0AH48172M6",
        "#daily-newsletters",
    )
    assert _NEWSLETTER_CHANNELS["Internal AI"] == (
        "C0AH48172M6",
        "#daily-newsletters",
    )
    assert _NEWSLETTER_CHANNELS["AJ"] == ("C0BLUPJ0X0R", "#aj-release-notes")
    assert _NEWSLETTER_CHANNELS["DR"] == _NEWSLETTER_CHANNELS["Internal AI"]


@pytest.mark.unit
@pytest.mark.parametrize(
    "request_type, expected_emoji, expected_label",
    [
        pytest.param(RequestType.ACTION, "🔧", "Action Requested", id="action"),
        pytest.param(RequestType.REVIEW, "👀", "Review Requested", id="review"),
        pytest.param(RequestType.INPUT, "❓", "Input Needed", id="input"),
        pytest.param(RequestType.GUIDANCE, "🧭", "Guidance Needed", id="guidance"),
        pytest.param(RequestType.APPROVAL, "✅", "Approval Requested", id="approval"),
        pytest.param(RequestType.BLOCKED, "🚫", "Still Blocked", id="blocked"),
    ],
)
@patch("airbyte_ops_mcp.mcp.human_in_the_loop.dispatch_escalation")
def test_request_type_resolves_header(
    mock_dispatch: MagicMock,
    request_type: RequestType,
    expected_emoji: str,
    expected_label: str,
) -> None:
    """escalate_to_human passes the correct header_emoji/header_label for each request_type."""
    # Configure mock to return a minimal successful result
    mock_result = MagicMock()
    mock_result.run_url = "https://github.com/actions/runs/1"
    mock_result.workflow_url = "https://github.com/actions/workflows/1"
    mock_result.run_id = 1
    mock_dispatch.return_value = mock_result

    escalate_to_human(
        target_person="aj@airbyte.io",
        message="Test message.",
        agent_session_url="https://app.devin.ai/sessions/abc",
        request_type=request_type,
    )

    mock_dispatch.assert_called_once()
    call_kwargs = mock_dispatch.call_args.kwargs
    assert call_kwargs["header_emoji"] == expected_emoji
    assert call_kwargs["header_label"] == expected_label


# ---------------------------------------------------------------------------
# validate_person_id
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "identifier",
    [
        pytest.param("@aaronsteers", id="github_handle"),
        pytest.param("@aldogonzalez8", id="github_handle_numeric"),
        pytest.param("aj@airbyte.io", id="email"),
        pytest.param("user@airbyte.io", id="email_another_airbyte"),
        pytest.param("U05AKF1BCC9", id="slack_id"),
        pytest.param("U070BMPDUHJ", id="slack_id_2"),
        pytest.param("S0BKR63VAN5", id="slack_usergroup_id"),
        pytest.param("  @aaronsteers  ", id="github_handle_whitespace"),
        pytest.param("  S0BKR63VAN5  ", id="slack_usergroup_id_whitespace"),
    ],
)
def test_validate_person_id_accepts_valid(identifier: str) -> None:
    """validate_person_id accepts well-formed identifiers without raising."""
    validate_person_id(identifier)  # should not raise


@pytest.mark.unit
@pytest.mark.parametrize(
    "identifier",
    [
        pytest.param("aldo.gonzalez", id="bare_name_with_dot"),
        pytest.param("aldogonzalez8", id="bare_github_handle_no_at"),
        pytest.param("aaronsteers", id="bare_handle_no_at"),
        pytest.param("", id="empty_string"),
        pytest.param("   ", id="whitespace_only"),
        pytest.param("@", id="at_sign_only"),
        pytest.param("user@example.com", id="email_non_airbyte"),
        pytest.param("user@gmail.com", id="email_gmail"),
        pytest.param("s0bkr63van5", id="lowercase_slack_usergroup_id"),
        pytest.param("S1234567", id="short_slack_usergroup_id"),
    ],
)
def test_validate_person_id_rejects_invalid(identifier: str) -> None:
    """validate_person_id raises ValueError for ambiguous or empty identifiers."""
    with pytest.raises(ValueError):
        validate_person_id(identifier)


@pytest.mark.unit
@pytest.mark.parametrize(
    "identifier, expected_classification",
    [
        pytest.param("S0BKR63VAN5", "slack_usergroup_id", id="slack_usergroup"),
        pytest.param("U05AKF1BCC9", "slack_id", id="slack_user"),
        pytest.param("@aaronsteers", "github_handle", id="github_handle"),
        pytest.param("aj@airbyte.io", "email", id="email"),
    ],
)
def test_classify_person_id(identifier: str, expected_classification: str) -> None:
    """classify_person_id distinguishes Slack usergroups from other identifiers."""
    assert classify_person_id(identifier) == expected_classification


@pytest.mark.unit
def test_normalize_person_id_preserves_slack_usergroup_id() -> None:
    """normalize_person_id trims but does not alter a Slack usergroup ID."""
    assert normalize_person_id("  S0BKR63VAN5  ") == "S0BKR63VAN5"


@pytest.mark.unit
@patch("airbyte_ops_mcp.human_in_the_loop.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.human_in_the_loop.resolve_ci_trigger_github_token")
def test_dispatch_escalation_accepts_mixed_user_and_usergroup_cc(
    mock_token: MagicMock, mock_dispatch: MagicMock
) -> None:
    """dispatch_escalation accepts Slack users and usergroups together in CC."""
    mock_token.return_value = "fake-token"
    mock_dispatch.return_value = MagicMock()

    dispatch_escalation(
        target_person="S0BKR63VAN5",
        message="Test message.",
        agent_session_url=SESSION_URL,
        cc=["U05AKF1BCC9", "S08SNSK5RHQ"],
    )

    assert mock_dispatch.call_args.kwargs["inputs"]["target_person"] == "S0BKR63VAN5"
    assert mock_dispatch.call_args.kwargs["inputs"]["cc_persons"] == (
        "U05AKF1BCC9,S08SNSK5RHQ"
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "identifier, slack_id, expected",
    [
        pytest.param(
            "S0BKR63VAN5",
            "S0BKR63VAN5",
            "<!subteam^S0BKR63VAN5>",
            id="usergroup_id",
        ),
        pytest.param(
            "U05AKF1BCC9",
            "U05AKF1BCC9",
            "<@U05AKF1BCC9>",
            id="user_id",
        ),
        pytest.param(
            "alice@example.com",
            "W0123456789",
            "<@W0123456789>",
            id="enterprise-grid_user_id",
        ),
    ],
)
def test_format_mention_renders_slack_ids(
    identifier: str, slack_id: str, expected: str
) -> None:
    """_format_mention renders usergroup and user IDs with Slack syntax."""
    assert _format_mention(identifier, slack_id) == expected


@pytest.mark.unit
def test_resolve_to_slack_id_skips_roster_for_usergroup() -> None:
    """_resolve_to_slack_id returns usergroup IDs without roster lookup."""
    assert _resolve_to_slack_id("S0BKR63VAN5", []) == "S0BKR63VAN5"


@pytest.mark.unit
def test_build_slack_blocks_renders_usergroup_target_and_cc() -> None:
    """HITL blocks render usergroup targets and CCs as subteam mentions."""
    blocks = _build_slack_blocks(
        target_person="S0BKR63VAN5",
        target_slack_id="S0BKR63VAN5",
        cc_mentions=["<!subteam^S08SNSK5RHQ>"],
        message="Test message.",
        agent_session_url=SESSION_URL,
        pr_url=None,
        issue_url=None,
        additional_actions=None,
    )

    context = next(block for block in blocks if block["type"] == "context")
    text = context["elements"][0]["text"]
    assert "*To:* <!subteam^S0BKR63VAN5>" in text
    assert "*CC:* <!subteam^S08SNSK5RHQ>" in text


@pytest.mark.unit
@patch("airbyte_ops_mcp.slack_posting._post_message")
def test_send_hitl_notification_renders_usergroups_end_to_end(
    mock_post: MagicMock,
) -> None:
    """send_hitl_notification renders usergroups without roster resolution."""
    send_hitl_notification(
        target_person="S0BKR63VAN5",
        message="Test message.",
        agent_session_url=SESSION_URL,
        cc_persons=["U05AKF1BCC9", "S08SNSK5RHQ"],
        slack_token="xoxb-test",
        roster=[],
    )

    blocks = mock_post.call_args.kwargs["blocks"]
    context = next(block for block in blocks if block["type"] == "context")
    text = context["elements"][0]["text"]
    assert "*To:* <!subteam^S0BKR63VAN5>" in text
    assert "<@U05AKF1BCC9>" in text
    assert "<!subteam^S08SNSK5RHQ>" in text


@pytest.mark.unit
def test_test_suite_blocks_unstubbed_slack_posts() -> None:
    """Outbound Slack posts fail loudly unless a test explicitly stubs them."""
    with pytest.raises(AssertionError, match="Outbound notification attempted"):
        send_hitl_notification(
            target_person="S0BKR63VAN5",
            message="Test message.",
            slack_token="xoxb-test",
            roster=[],
        )


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.human_in_the_loop.dispatch_escalation")
def test_escalate_to_human_rejects_bare_handle(mock_dispatch: MagicMock) -> None:
    """escalate_to_human raises ValueError when target_person is a bare handle."""
    mock_dispatch.side_effect = ValueError(
        "Identifier 'aldo.gonzalez' is not a recognized format."
    )
    with pytest.raises(ValueError, match="not a recognized format"):
        escalate_to_human(
            target_person="aldo.gonzalez",
            message="Test message.",
            agent_session_url="https://app.devin.ai/sessions/abc",
        )


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.human_in_the_loop.dispatch_escalation")
def test_request_type_none_passes_none_headers(mock_dispatch: MagicMock) -> None:
    """When request_type is omitted, header_emoji and header_label are None (backend defaults)."""
    mock_result = MagicMock()
    mock_result.run_url = "https://github.com/actions/runs/1"
    mock_result.workflow_url = "https://github.com/actions/workflows/1"
    mock_result.run_id = 1
    mock_dispatch.return_value = mock_result

    escalate_to_human(
        target_person="aj@airbyte.io",
        message="Test message.",
        agent_session_url="https://app.devin.ai/sessions/abc",
    )

    mock_dispatch.assert_called_once()
    call_kwargs = mock_dispatch.call_args.kwargs
    assert call_kwargs["header_emoji"] is None
    assert call_kwargs["header_label"] is None


# ---------------------------------------------------------------------------
# validate_approval_request_summary
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "summary",
    [
        pytest.param(None, id="none"),
        pytest.param("", id="empty"),
        pytest.param("Deploy v2.0 to prod", id="short_plain_text"),
        pytest.param(
            "Pin `source-hubspot` prerelease `4.5.3-preview`", id="balanced_backticks"
        ),
        pytest.param("a" * APPROVAL_REQUEST_SUMMARY_MAX_LENGTH, id="at_max_length"),
        pytest.param("Line one.\nLine two.\nLine three.", id="multiline"),
    ],
)
def test_validate_approval_request_summary_accepts_valid(summary: str | None) -> None:
    """validate_approval_request_summary accepts well-formed summaries."""
    validate_approval_request_summary(summary)  # should not raise


@pytest.mark.unit
def test_validate_approval_request_summary_rejects_over_limit() -> None:
    """Summaries longer than the limit are rejected with a length-specific error."""
    too_long = "a" * (APPROVAL_REQUEST_SUMMARY_MAX_LENGTH + 1)
    with pytest.raises(ValueError, match="characters"):
        validate_approval_request_summary(too_long)


@pytest.mark.unit
def test_validate_approval_request_summary_rejects_unbalanced_backticks() -> None:
    """Summaries with an odd number of backticks are rejected."""
    with pytest.raises(ValueError, match="backticks"):
        validate_approval_request_summary("Pin `source-hubspot to workspace")


@pytest.mark.unit
def test_validate_approval_request_summary_rejects_session_repro() -> None:
    """The exact summary from session eed9e15… (which triggered the incident) is rejected.

    This is the summary that produced the truncated confirm dialog
    (ending in `af925730-af04-410` with an unterminated backtick) and
    caused the Approve/Reject buttons to no-op with a :warning: emoji.
    """
    summary = (
        "Unpin 3 source-google-search-console actors from prerelease "
        "`1.10.33-preview.57836bf`:\n"
        "\u2022 source `462913f0-f5bc-42a2-8fba-d996cd2bc940` (cobra-search-console) "
        "in workspace `df5f0287-af3f-4285-860c-ca3e6e7e0b13`\n"
        "\u2022 source `b88e338c-b6f2-47f3-8d1c-cc596493b932` (Etnies) "
        "in workspace `af925730-af04-4103-a57e-0dfedebb2998`\n"
        "\u2022 source `d30c97d0-a6fa-4cba-962a-aa01a0f6f029` (32) "
        "in workspace `af925730-af04-4103-a57e-0dfedebb2998`\n\n"
        "Fresh session after prior approve/reject buttons were reported broken."
    )
    # This summary has balanced backticks but is well over the 298-char limit.
    assert len(summary) > APPROVAL_REQUEST_SUMMARY_MAX_LENGTH
    with pytest.raises(ValueError, match="characters"):
        validate_approval_request_summary(summary)


@pytest.mark.unit
@patch("airbyte_ops_mcp.human_in_the_loop.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.human_in_the_loop.resolve_ci_trigger_github_token")
def test_dispatch_rejects_over_limit_summary(
    mock_token: MagicMock, mock_dispatch: MagicMock
) -> None:
    """dispatch_escalation raises before triggering the workflow when summary is over-limit."""
    mock_token.return_value = "fake-token"

    with pytest.raises(ValueError, match="characters"):
        dispatch_escalation(
            target_person="aj@airbyte.io",
            message="Test message.",
            agent_session_url="https://app.devin.ai/sessions/abc",
            approval_requested=True,
            approval_request_summary="a" * (APPROVAL_REQUEST_SUMMARY_MAX_LENGTH + 1),
        )
    mock_dispatch.assert_not_called()
