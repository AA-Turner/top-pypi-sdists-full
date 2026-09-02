"""TeamSpace migration boundary tests for tracker-facing payloads."""

from __future__ import annotations

from dataclasses import asdict

import pytest

from spec_kitty_tracker import CanonicalIssueType, CanonicalStatus, ExternalRef, InMemoryConnector
from spec_kitty_tracker.mission_sync import (
    BidirectionalIssueSync,
    MissionUpdate,
    assert_no_forbidden_teamspace_legacy_keys,
    mission_seed_from_issue,
)
from spec_kitty_tracker.models import CanonicalIssue

MISSION_ULID = "01KQ4Z6CCA970KS5EZ0V54B9NK"


def _issue() -> CanonicalIssue:
    return CanonicalIssue(
        ref=ExternalRef(system="linear", workspace="eng", id="issue-1", key="ENG-1"),
        title="Canonical mission identity",
        body=None,
        status=CanonicalStatus.IN_PROGRESS,
        issue_type=CanonicalIssueType.TASK,
    )


def test_mission_seed_accepts_canonical_mission_id_without_legacy_keys() -> None:
    seed = mission_seed_from_issue(_issue(), mission_id=MISSION_ULID)

    payload = asdict(seed)
    assert payload["mission_id"] == MISSION_ULID
    assert "feature_slug" not in payload
    assert "feature_number" not in payload
    assert "mission_key" not in payload


async def test_publish_mission_update_emits_only_canonical_mission_identity() -> None:
    connector = InMemoryConnector(name="linear", workspace="eng")
    issue = _issue()
    await connector.create_issue(issue)
    sync = BidirectionalIssueSync(connector=connector)

    await sync.publish_mission_update(
        issue_ref=issue.ref,
        update=MissionUpdate(
            mission_id=MISSION_ULID,
            mission_state="in_review",
            target_status=CanonicalStatus.IN_REVIEW,
            mission_url="https://teamspace.example/missions/01KQ4Z6CCA970KS5EZ0V54B9NK",
        ),
    )

    updated = await connector.get_issue(issue.ref)
    payload = updated.custom_fields["spec_kitty_mission"]
    assert payload["mission_id"] == MISSION_ULID
    assert payload["mission_state"] == "in_review"
    assert "feature_slug" not in payload
    assert "feature_number" not in payload
    assert "mission_key" not in payload


def test_tracker_payload_guard_rejects_recursive_legacy_keys() -> None:
    with pytest.raises(ValueError, match="feature_slug"):
        assert_no_forbidden_teamspace_legacy_keys(
            {
                "mission_id": MISSION_ULID,
                "decision_refs": [{"feature_slug": "001-legacy"}],
            }
        )
