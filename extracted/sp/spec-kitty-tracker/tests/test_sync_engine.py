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
    SyncConflictError,
    SyncEngine,
)


def _make_issue(
    *,
    issue_id: str,
    title: str,
    status: CanonicalStatus,
) -> CanonicalIssue:
    return CanonicalIssue(
        ref=ExternalRef(system="jira", workspace="demo", id=issue_id, key=issue_id),
        title=title,
        body="Body",
        status=status,
        issue_type=CanonicalIssueType.TASK,
    )


async def test_sync_pull_external_authoritative() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    store = InMemoryIssueStore()

    remote = _make_issue(
        issue_id="DEMO-1", title="Remote Title", status=CanonicalStatus.IN_PROGRESS
    )
    await connector.create_issue(remote)

    local = _make_issue(issue_id="DEMO-1", title="Local Title", status=CanonicalStatus.TODO)
    await store.upsert_issue(local)

    engine = SyncEngine(
        connector=connector,
        store=store,
        policy=OwnershipPolicy.external_authoritative(),
        strategy=ConflictStrategy.NEWER_TIMESTAMP,
    )

    result = await engine.pull()
    synced = await store.get_issue(local.ref)

    assert result.stats.pulled_updated == 1
    assert synced is not None
    assert synced.title == "Remote Title"
    assert synced.status == CanonicalStatus.IN_PROGRESS


async def test_sync_pull_split_ownership() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    store = InMemoryIssueStore()

    await connector.create_issue(
        _make_issue(issue_id="DEMO-2", title="Remote Title", status=CanonicalStatus.DONE)
    )

    local = _make_issue(issue_id="DEMO-2", title="Local Title", status=CanonicalStatus.TODO)
    await store.upsert_issue(local)

    policy = OwnershipPolicy.split(
        field_owners={
            "title": FieldOwner.LOCAL,
            "status": FieldOwner.EXTERNAL,
        },
        default_owner=FieldOwner.SHARED,
    )
    engine = SyncEngine(
        connector=connector,
        store=store,
        policy=policy,
        strategy=ConflictStrategy.NEWER_TIMESTAMP,
    )

    await engine.pull()
    synced = await store.get_issue(local.ref)

    assert synced is not None
    assert synced.title == "Local Title"
    assert synced.status == CanonicalStatus.DONE


async def test_sync_manual_review_strict_mode() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    store = InMemoryIssueStore()

    await connector.create_issue(
        _make_issue(issue_id="DEMO-3", title="Remote", status=CanonicalStatus.TODO)
    )
    await store.upsert_issue(
        _make_issue(issue_id="DEMO-3", title="Local", status=CanonicalStatus.TODO)
    )

    engine = SyncEngine(
        connector=connector,
        store=store,
        policy=OwnershipPolicy.split(field_owners={"title": FieldOwner.SHARED}),
        strategy=ConflictStrategy.MANUAL_REVIEW,
        strict_manual_review=True,
    )

    try:
        await engine.pull()
    except SyncConflictError:
        assert True
        return

    assert False, "Expected SyncConflictError in strict manual review mode"


async def test_sync_push_creates_remote_issue() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    store = InMemoryIssueStore()

    local = _make_issue(issue_id="DEMO-4", title="Local Only", status=CanonicalStatus.TODO)
    await store.upsert_issue(local)

    engine = SyncEngine(
        connector=connector,
        store=store,
        policy=OwnershipPolicy.local_authoritative(),
    )

    result = await engine.push()
    remote = await connector.get_issue(local.ref)

    assert result.stats.pushed_created == 1
    assert remote.title == "Local Only"
