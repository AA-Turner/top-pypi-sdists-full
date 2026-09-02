"""TRK-M1-03 A13: decision-reference strict parsing and link mismatch.

N17: a malformed decision_refs entry fails closed with a typed
DecisionReferenceContractError; decision_link_mismatches detects a
published/mission decision-set drift, a missing BLOCKED_BY link, or a
published entry that no longer matches the mission's own entry.
"""

from __future__ import annotations

import pytest

from spec_kitty_tracker import (
    CanonicalIssue,
    CanonicalIssueType,
    CanonicalLink,
    CanonicalStatus,
    DecisionReference,
    DecisionReferenceContractError,
    ExternalRef,
    LinkType,
    MissionUpdate,
)
from spec_kitty_tracker.mission_sync import (
    decision_link_mismatches,
    mission_seed_from_issue,
)


def _issue(
    custom_fields: dict[str, object] | None = None, links: list[CanonicalLink] | None = None
) -> CanonicalIssue:
    return CanonicalIssue(
        ref=ExternalRef(system="jira", workspace="demo", id="JRA-1", key="JRA-1"),
        title="Issue",
        body=None,
        status=CanonicalStatus.IN_PROGRESS,
        issue_type=CanonicalIssueType.TASK,
        custom_fields=custom_fields or {},
        links=links or [],
    )


def test_missing_decision_id_raises_dr_001() -> None:
    issue = _issue(custom_fields={"decision_refs": [{"summary": "no id"}]})
    with pytest.raises(DecisionReferenceContractError) as excinfo:
        mission_seed_from_issue(issue)
    assert excinfo.value.reason == "DR-001"


def test_non_dict_entry_raises_dr_001() -> None:
    issue = _issue(custom_fields={"decision_refs": ["not-a-dict"]})
    with pytest.raises(DecisionReferenceContractError) as excinfo:
        mission_seed_from_issue(issue)
    assert excinfo.value.reason == "DR-001"


def test_non_list_container_raises_dr_001() -> None:
    issue = _issue(custom_fields={"decision_refs": "not-a-list"})
    with pytest.raises(DecisionReferenceContractError) as excinfo:
        mission_seed_from_issue(issue)
    assert excinfo.value.reason == "DR-001"
    assert excinfo.value.field_path == "decision_refs"


def test_invalid_external_ref_raises_dr_002() -> None:
    issue = _issue(
        custom_fields={
            "decision_refs": [
                {
                    "decision_id": "DEC-1",
                    "external_ref": {"system": "", "workspace": "w", "id": "1"},
                }
            ]
        }
    )
    with pytest.raises(DecisionReferenceContractError) as excinfo:
        mission_seed_from_issue(issue)
    assert excinfo.value.reason == "DR-002"


def test_absent_decision_refs_is_not_malformed() -> None:
    issue = _issue(custom_fields={})
    seed = mission_seed_from_issue(issue)
    assert seed.decision_references == []


def test_decision_link_mismatches_empty_when_consistent() -> None:
    decision_ref = DecisionReference(
        decision_id="DEC-1",
        summary="s",
        blocking=True,
        external_ref=ExternalRef(system="jira", workspace="demo", id="ARCH-1"),
    )
    update = MissionUpdate(
        mission_id="mission:alpha",
        mission_state="waiting_on_decision",
        decision_references=[decision_ref],
    )
    issue = _issue(
        custom_fields={"spec_kitty_mission": {"decision_refs": [decision_ref.as_dict()]}},
        links=[CanonicalLink(type=LinkType.BLOCKED_BY, target=decision_ref.external_ref)],
    )
    assert decision_link_mismatches(issue, update) == []


def test_decision_link_mismatch_detects_set_drift_dr_003() -> None:
    decision_ref = DecisionReference(decision_id="DEC-1", summary="s", blocking=False)
    update = MissionUpdate(
        mission_id="mission:alpha",
        mission_state="waiting_on_decision",
        decision_references=[decision_ref, DecisionReference(decision_id="DEC-2")],
    )
    issue = _issue(
        custom_fields={"spec_kitty_mission": {"decision_refs": [decision_ref.as_dict()]}}
    )
    mismatches = decision_link_mismatches(issue, update)
    assert any(m.reason == "DR-003" for m in mismatches)


def test_decision_link_mismatch_detects_missing_blocked_by_link_dr_004() -> None:
    decision_ref = DecisionReference(
        decision_id="DEC-1",
        blocking=True,
        external_ref=ExternalRef(system="jira", workspace="demo", id="ARCH-1"),
    )
    update = MissionUpdate(
        mission_id="mission:alpha",
        mission_state="waiting_on_decision",
        decision_references=[decision_ref],
    )
    issue = _issue(
        custom_fields={"spec_kitty_mission": {"decision_refs": [decision_ref.as_dict()]}},
        links=[],
    )
    mismatches = decision_link_mismatches(issue, update)
    assert any(m.reason == "DR-004" for m in mismatches)


def test_decision_link_mismatch_detects_stale_published_entry_dr_005() -> None:
    decision_ref = DecisionReference(decision_id="DEC-1", summary="original", blocking=False)
    update = MissionUpdate(
        mission_id="mission:alpha",
        mission_state="waiting_on_decision",
        decision_references=[decision_ref],
    )
    stale_payload = decision_ref.as_dict()
    stale_payload["summary"] = "edited after publish"
    issue = _issue(custom_fields={"spec_kitty_mission": {"decision_refs": [stale_payload]}})
    mismatches = decision_link_mismatches(issue, update)
    assert any(m.reason == "DR-005" for m in mismatches)
