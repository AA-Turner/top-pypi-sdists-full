"""Tracker mission-update egress timestamp is unambiguously labeled.

Mission: tracker-egress-time-disambiguation-01KRNT8W

`publish_mission_update` writes a wall-clock timestamp into the
``spec_kitty_mission`` custom-field payload that gets pushed to the
external tracker. Per spec-kitty-events Rule R-T-01 this MUST NOT be named
in a way that a downstream consumer could mistake for canonical mission
occurrence/completion time. This test pins the field name as
``tracker_sync_pushed_at`` and asserts no ``updated_at`` field leaks into
the payload.
"""

from __future__ import annotations

from datetime import datetime

import pytest

from spec_kitty_tracker import (
    BidirectionalIssueSync,
    CanonicalIssue,
    CanonicalIssueType,
    CanonicalStatus,
    ExternalRef,
    InMemoryConnector,
    MissionUpdate,
)


def _issue_ref(provider: str, issue_id: str) -> ExternalRef:
    return ExternalRef(system=provider, workspace=f"{provider}-demo", id=issue_id, key=issue_id)


def _make_issue(provider: str, issue_id: str, status: CanonicalStatus) -> CanonicalIssue:
    return CanonicalIssue(
        ref=_issue_ref(provider, issue_id),
        title=f"{provider.upper()} issue {issue_id}",
        body="egress-time test",
        status=status,
        issue_type=CanonicalIssueType.TASK,
    )


@pytest.mark.asyncio
async def test_publish_mission_update_uses_tracker_sync_pushed_at_not_updated_at() -> None:
    connector = InMemoryConnector(name="jira", workspace="jira-demo")
    sync = BidirectionalIssueSync(connector=connector)
    source_issue = _make_issue("jira", "JRA-99", CanonicalStatus.IN_PROGRESS)
    await connector.create_issue(source_issue)

    update = MissionUpdate(
        mission_id="mission:egress-time",
        mission_state="in_progress",
        summary="Push mission state for egress-time disambiguation regression.",
        mission_url="https://spec-kitty.example/missions/egress-time",
    )

    await sync.publish_mission_update(issue_ref=source_issue.ref, update=update)
    updated_issue = await connector.get_issue(source_issue.ref)

    mission_meta = updated_issue.custom_fields["spec_kitty_mission"]
    assert isinstance(mission_meta, dict)

    # New canonical field name.
    assert "tracker_sync_pushed_at" in mission_meta, (
        "publish_mission_update must emit tracker_sync_pushed_at to disambiguate "
        "egress sync metadata from canonical mission occurrence time."
    )
    # Old ambiguous name must NOT be present.
    assert "updated_at" not in mission_meta, (
        "The legacy 'updated_at' field name was ambiguous and is forbidden. "
        "Use 'tracker_sync_pushed_at' for egress sync metadata."
    )

    # The value parses as ISO-8601.
    pushed_at = mission_meta["tracker_sync_pushed_at"]
    assert isinstance(pushed_at, str) and pushed_at
    # Must round-trip through fromisoformat without error.
    datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
