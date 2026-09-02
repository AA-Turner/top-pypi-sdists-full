"""TRK-M1-03 N2: retired TeamSpace legacy-key egress denial wired into
SyncEngine.push and BidirectionalIssueSync.publish_mission_update.

(a) A local issue carrying a forbidden legacy key in custom_fields must
never reach create_issue/update_issue -- SyncEngine.push records a
SyncFailure and issues no write for that issue.
(b) publish_mission_update must reject a patch whose full custom_fields
(not just the newly-written spec_kitty_mission payload) carries a
pre-existing forbidden legacy key, before any egress call.
"""

from __future__ import annotations

import pytest

from spec_kitty_tracker import (
    BidirectionalIssueSync,
    CanonicalIssue,
    CanonicalIssueType,
    CanonicalStatus,
    ExternalRef,
    InMemoryConnector,
    InMemoryIssueStore,
    IssueNotFoundError,
    MissionUpdate,
    OwnershipPolicy,
    SyncEngine,
)


def _issue(issue_id: str, custom_fields: dict[str, object] | None = None) -> CanonicalIssue:
    return CanonicalIssue(
        ref=ExternalRef(system="jira", workspace="demo", id=issue_id, key=issue_id),
        title=f"Issue {issue_id}",
        body="body",
        status=CanonicalStatus.TODO,
        issue_type=CanonicalIssueType.TASK,
        custom_fields=custom_fields or {},
    )


async def test_push_create_denies_legacy_key_in_custom_fields() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    store = InMemoryIssueStore()
    await store.upsert_issue(_issue("SP-1", custom_fields={"mission_key": "x"}))

    engine = SyncEngine(
        connector=connector, store=store, policy=OwnershipPolicy.local_authoritative()
    )
    result = await engine.push()

    assert result.stats.pushed_created == 0
    assert len(result.failures) == 1
    assert result.failures[0].operation == "create"
    assert result.failures[0].retryable is False
    with pytest.raises(IssueNotFoundError):
        await connector.get_issue(ExternalRef(system="jira", workspace="demo", id="SP-1"))


async def test_push_update_denies_legacy_key_in_custom_fields() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    store = InMemoryIssueStore()

    remote = _issue("SP-2")
    await connector.create_issue(remote)
    local = remote.clone()
    local.custom_fields = {"feature_slug": "001-legacy"}
    await store.upsert_issue(local)

    engine = SyncEngine(
        connector=connector, store=store, policy=OwnershipPolicy.local_authoritative()
    )
    result = await engine.push()

    assert result.stats.pushed_updated == 0
    assert len(result.failures) == 1
    assert result.failures[0].operation == "update"
    remote_after = await connector.get_issue(remote.ref)
    assert remote_after.custom_fields == {}


async def test_publish_mission_update_denies_pre_existing_legacy_key_in_custom_fields() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    issue = _issue("SP-3", custom_fields={"feature_number": "007"})
    await connector.create_issue(issue)
    sync = BidirectionalIssueSync(connector=connector)

    with pytest.raises(ValueError, match="feature_number"):
        await sync.publish_mission_update(
            issue_ref=issue.ref,
            update=MissionUpdate(mission_id="mission:beta", mission_state="in_review"),
        )

    unchanged = await connector.get_issue(issue.ref)
    assert "spec_kitty_mission" not in unchanged.custom_fields
