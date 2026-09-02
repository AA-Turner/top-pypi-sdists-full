"""TRK-M1-03 A9/A10: attributable conflicts and a typed sync-failure record.

A9: ConflictRecord gains ``issue_ref`` (appended field), populated by
SyncEngine._merge_issues, so a conflict can be attributed to an issue.

A10: SyncFailure (frozen dataclass) and SyncResult.failures: list[SyncFailure]
give the sync engine a typed partial-failure vocabulary (used by A11).
"""

from __future__ import annotations

from spec_kitty_tracker import (
    CanonicalIssue,
    CanonicalIssueType,
    CanonicalStatus,
    ConflictStrategy,
    ExternalRef,
    FieldOwner,
    InMemoryConnector,
    InMemoryIssueStore,
    OwnershipPolicy,
    SyncEngine,
    SyncFailure,
)


def _issue(issue_id: str, status: CanonicalStatus) -> CanonicalIssue:
    return CanonicalIssue(
        ref=ExternalRef(system="jira", workspace="demo", id=issue_id, key=issue_id),
        title=f"Issue {issue_id}",
        body="body",
        status=status,
        issue_type=CanonicalIssueType.TASK,
    )


async def test_conflict_record_carries_issue_ref() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    store = InMemoryIssueStore()

    await connector.create_issue(_issue("SP-1", CanonicalStatus.DONE))
    await store.upsert_issue(_issue("SP-1", CanonicalStatus.TODO))

    policy = OwnershipPolicy.split(field_owners={"status": FieldOwner.SHARED})
    engine = SyncEngine(
        connector=connector,
        store=store,
        policy=policy,
        strategy=ConflictStrategy.MANUAL_REVIEW,
    )

    result = await engine.pull()

    assert len(result.conflicts) == 1
    assert result.conflicts[0].issue_ref is not None
    assert result.conflicts[0].issue_ref.identity == "jira:demo:SP-1"


def test_sync_failure_is_a_frozen_dataclass_with_expected_shape() -> None:
    failure = SyncFailure(
        issue_ref=ExternalRef(system="jira", workspace="demo", id="SP-1"),
        operation="update",
        failure_class=None,
        message="boom",
        retryable=False,
    )
    assert failure.operation == "update"
    assert failure.retryable is False


async def test_sync_result_failures_defaults_to_empty_list() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    store = InMemoryIssueStore()
    engine = SyncEngine(
        connector=connector,
        store=store,
        policy=OwnershipPolicy.external_authoritative(),
    )
    result = await engine.pull()
    assert result.failures == []
