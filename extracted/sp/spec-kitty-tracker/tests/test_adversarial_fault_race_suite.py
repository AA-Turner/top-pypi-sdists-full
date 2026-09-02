"""TRK-M1-06: adversarial fault/race suite over SyncEngine.

Each test in this file pins a fault or race that the TRK-M1-03 engine did
not previously guard against -- it was written failing against the
TRK-M1-03 baseline (RED) and only turned passing (GREEN) once the matching
production fix in ``sync.py``/``in_memory.py`` landed, per the acceptance
criteria: "Exercise ... cross-scope access, stale auth/context,
duplicate/out-of-order events, cursor loss, conflict loops, partial
failure, restart with surviving bytes, contract drift, decision-link
mismatch, and legacy-field egress; no false authority or silent
guessing." This suite is scoped to the sync engine's fault/race surface
(concurrent-writer races, conflict loops, partial-failure/idempotency,
cursor/checkpoint corruption, ownership violations); the payload-shape,
cross-repo-scope, and decision-link cases in the wider node criteria are
already exercised by TRK-M1-01/02/03's suites
(test_beads_payload_strictness.py, test_no_shared_team_fallback.py,
test_decision_reference_strictness.py, etc).
"""

from __future__ import annotations

import pytest

from spec_kitty_tracker import (
    CanonicalIssue,
    CanonicalIssueType,
    CanonicalStatus,
    ConflictStrategy,
    ExternalRef,
    FieldOwner,
    InMemoryConnector,
    InMemoryIssueStore,
    IssueNotFoundError,
    OwnershipPolicy,
    SyncCheckpoint,
    SyncEngine,
)
from spec_kitty_tracker.errors import ConnectorRequestError, FailureClass


def _issue(
    issue_id: str,
    *,
    title: str | None = None,
    status: CanonicalStatus = CanonicalStatus.TODO,
) -> CanonicalIssue:
    return CanonicalIssue(
        ref=ExternalRef(system="jira", workspace="demo", id=issue_id, key=issue_id),
        title=title or f"Issue {issue_id}",
        body="body",
        status=status,
        issue_type=CanonicalIssueType.TASK,
    )


# ---------------------------------------------------------------------------
# 1. Concurrent-writer race: two independent writers both believe they are
#    the first to create an issue for the same identity.
# ---------------------------------------------------------------------------


class _InterleavedCreateConnector(InMemoryConnector):
    """Simulates the classic TOCTOU race between two independent sync
    processes: process B creates the same-identity remote issue in the
    window between process A's remote-index snapshot (which found nothing)
    and process A's own ``create_issue`` call. The injection happens
    inside ``create_issue`` itself so it lands exactly at that boundary,
    regardless of how ``push()`` is scheduled."""

    def __init__(self, *, name: str, workspace: str, concurrent_issue: CanonicalIssue) -> None:
        super().__init__(name=name, workspace=workspace)
        self._concurrent_issue = concurrent_issue
        self._injected = False

    async def create_issue(self, issue: CanonicalIssue) -> CanonicalIssue:
        if not self._injected:
            self._injected = True
            self._issues[self._concurrent_issue.ref.identity] = self._concurrent_issue.clone()
        return await super().create_issue(issue)


async def test_concurrent_create_race_does_not_silently_overwrite_other_writer() -> None:
    ref = ExternalRef(system="jira", workspace="demo", id="RACE-1", key="RACE-1")
    concurrent_remote = CanonicalIssue(
        ref=ref,
        title="Created By Other Writer",
        body="body",
        status=CanonicalStatus.TODO,
        issue_type=CanonicalIssueType.TASK,
    )
    connector = _InterleavedCreateConnector(
        name="jira", workspace="demo", concurrent_issue=concurrent_remote
    )
    store = InMemoryIssueStore()
    our_issue = CanonicalIssue(
        ref=ref,
        title="Created By Us",
        body="body",
        status=CanonicalStatus.TODO,
        issue_type=CanonicalIssueType.TASK,
    )
    await store.upsert_issue(our_issue)

    engine = SyncEngine(
        connector=connector, store=store, policy=OwnershipPolicy.local_authoritative()
    )
    result = await engine.push()

    # The other writer's create must survive untouched -- our create must
    # be denied and recorded, never silently overwrite it.
    remote_after = await connector.get_issue(ref)
    assert remote_after.title == "Created By Other Writer"
    assert result.stats.pushed_created == 0
    create_failures = [f for f in result.failures if f.operation == "create"]
    assert len(create_failures) == 1
    assert create_failures[0].retryable is False


# ---------------------------------------------------------------------------
# 2. Conflict loop: a SHARED-field conflict that resolves to a value the
#    remote already holds (so the outgoing patch is empty) must still be
#    materialized locally -- otherwise every subsequent push() re-discovers
#    and re-reports the identical conflict forever.
# ---------------------------------------------------------------------------


async def test_push_persists_resolved_conflict_locally_even_when_remote_patch_is_empty() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    store = InMemoryIssueStore()

    ref = ExternalRef(system="jira", workspace="demo", id="LOOP-1", key="LOOP-1")
    await connector.create_issue(
        CanonicalIssue(
            ref=ref,
            title="Remote Title",
            body="body",
            status=CanonicalStatus.TODO,
            issue_type=CanonicalIssueType.TASK,
        )
    )
    await store.upsert_issue(
        CanonicalIssue(
            ref=ref,
            title="Local Draft Title",
            body="body",
            status=CanonicalStatus.TODO,
            issue_type=CanonicalIssueType.TASK,
        )
    )

    engine = SyncEngine(
        connector=connector,
        store=store,
        policy=OwnershipPolicy.split(field_owners={}, default_owner=FieldOwner.SHARED),
        strategy=ConflictStrategy.EXTERNAL_WINS,
    )

    first = await engine.push()
    assert len(first.conflicts) == 1
    assert first.conflicts[0].resolved_value == "Remote Title"

    local_after_first = await store.get_issue(ref)
    assert local_after_first is not None
    assert local_after_first.title == "Remote Title"

    # A second push() with no pull() in between and no further external
    # edits must find nothing left to resolve -- otherwise this is an
    # infinite conflict loop for any caller that only calls push().
    second = await engine.push()
    assert second.conflicts == []


# ---------------------------------------------------------------------------
# 3. Partial-failure / idempotency: a create whose write actually lands but
#    whose response is lost (a transient error surfaces to the caller
#    anyway) must be retried, and the retry must be idempotent -- neither
#    duplicating the remote issue nor being denied as a "conflict".
# ---------------------------------------------------------------------------


class _CreateSucceedsButResponseLostConnector(InMemoryConnector):
    def __init__(self, *, name: str, workspace: str) -> None:
        super().__init__(name=name, workspace=workspace)
        self.create_attempts = 0

    async def create_issue(self, issue: CanonicalIssue) -> CanonicalIssue:
        self.create_attempts += 1
        if self.create_attempts == 1:
            # The write actually lands server-side, but the caller never
            # sees the response -- the classic idempotency hazard.
            await super().create_issue(issue)
            raise ConnectorRequestError(
                "response lost",
                status_code=503,
                provider=self.name,
                failure_class=FailureClass.TRANSIENT,
            )
        return await super().create_issue(issue)


async def test_create_retry_after_lost_response_is_idempotent_not_duplicated() -> None:
    connector = _CreateSucceedsButResponseLostConnector(name="jira", workspace="demo")
    store = InMemoryIssueStore()
    await store.upsert_issue(_issue("NEW-9"))

    engine = SyncEngine(
        connector=connector, store=store, policy=OwnershipPolicy.local_authoritative()
    )
    result = await engine.push()

    assert result.failures == []
    assert result.stats.pushed_created == 1
    assert connector.create_attempts == 2

    remote_page = await connector.list_issues(
        updated_since=None, cursor=None, limit=100, filters=None
    )
    assert len(remote_page.items) == 1


# ---------------------------------------------------------------------------
# 4. Cursor/checkpoint corruption: a malformed checkpoint restored from
#    outside the engine (e.g. corrupted-on-disk state) must fail closed as
#    a typed, recorded SyncFailure -- never an uncaught crash, and never
#    silently guessed at.
# ---------------------------------------------------------------------------


async def test_pull_with_corrupted_checkpoint_cursor_fails_closed_not_crashes() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    for idx in range(3):
        await connector.create_issue(_issue(f"CUR-{idx}"))

    store = InMemoryIssueStore()
    engine = SyncEngine(
        connector=connector, store=store, policy=OwnershipPolicy.external_authoritative()
    )
    engine.restore_checkpoint(SyncCheckpoint(cursor="not-a-real-cursor", updated_since=None))

    result = await engine.pull()  # must not raise

    assert len(result.failures) == 1
    failure = result.failures[0]
    assert failure.operation == "pull_page"
    assert failure.retryable is False

    stored = await store.list_issues()
    assert stored == []


# ---------------------------------------------------------------------------
# 5. Ownership violation: local must not originate a value for a field it
#    does not own, even when creating a brand-new remote issue where there
#    is no external value yet to compare against and resolve a conflict
#    from.
# ---------------------------------------------------------------------------


async def test_push_create_denies_externally_owned_non_empty_field() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    store = InMemoryIssueStore()

    policy = OwnershipPolicy.split(
        field_owners={"assignees": FieldOwner.EXTERNAL},
        default_owner=FieldOwner.LOCAL,
    )
    new_issue = _issue("OWN-1", title="New Issue")
    new_issue.assignees = ["priti"]  # local tries to originate an assignment it does not own
    await store.upsert_issue(new_issue)

    engine = SyncEngine(connector=connector, store=store, policy=policy)
    result = await engine.push()

    assert result.stats.pushed_created == 0
    create_failures = [f for f in result.failures if f.operation == "create"]
    assert len(create_failures) == 1
    assert "assignees" in create_failures[0].message

    with pytest.raises(IssueNotFoundError):
        await connector.get_issue(new_issue.ref)


async def test_push_create_denies_externally_owned_non_default_priority() -> None:
    # Renata handback (attempt 1): the ownership-violation-on-create guard
    # only covered assignees/labels/links/custom_fields, omitting priority
    # and parent -- both CORE_ISSUE_FIELDS with the exact "unambiguous
    # nothing-asserted empty default" (None) the guard's own doc-comment
    # names as its selection criterion. A local issue asserting a
    # non-default priority it does not own must be denied on create, not
    # silently pushed through as false authority.
    connector = InMemoryConnector(name="jira", workspace="demo")
    store = InMemoryIssueStore()

    policy = OwnershipPolicy.split(
        field_owners={"priority": FieldOwner.EXTERNAL},
        default_owner=FieldOwner.LOCAL,
    )
    new_issue = _issue("OWN-2", title="New Issue")
    new_issue.priority = 1  # local tries to originate a priority it does not own
    await store.upsert_issue(new_issue)

    engine = SyncEngine(connector=connector, store=store, policy=policy)
    result = await engine.push()

    assert result.stats.pushed_created == 0
    create_failures = [f for f in result.failures if f.operation == "create"]
    assert len(create_failures) == 1
    assert "priority" in create_failures[0].message

    with pytest.raises(IssueNotFoundError):
        await connector.get_issue(new_issue.ref)


async def test_push_create_denies_externally_owned_non_default_parent() -> None:
    # Renata handback (attempt 1): same gap as priority above, for parent --
    # the other CORE_ISSUE_FIELDS member with a None empty default that the
    # guard omitted.
    connector = InMemoryConnector(name="jira", workspace="demo")
    store = InMemoryIssueStore()

    policy = OwnershipPolicy.split(
        field_owners={"parent": FieldOwner.EXTERNAL},
        default_owner=FieldOwner.LOCAL,
    )
    new_issue = _issue("OWN-3", title="New Issue")
    new_issue.parent = ExternalRef(
        system="jira", workspace="demo", id="PARENT-1", key="PARENT-1"
    )  # local tries to originate a parent link it does not own
    await store.upsert_issue(new_issue)

    engine = SyncEngine(connector=connector, store=store, policy=policy)
    result = await engine.push()

    assert result.stats.pushed_created == 0
    create_failures = [f for f in result.failures if f.operation == "create"]
    assert len(create_failures) == 1
    assert "parent" in create_failures[0].message

    with pytest.raises(IssueNotFoundError):
        await connector.get_issue(new_issue.ref)


# ---------------------------------------------------------------------------
# 6. Cursor corruption, syntactically-valid variant: a cursor that parses
#    cleanly as an int but is semantically invalid (negative) must also
#    fail closed -- Python's negative-index slicing would otherwise wrap
#    silently to the tail of the list instead of raising.
# ---------------------------------------------------------------------------


async def test_pull_with_negative_checkpoint_cursor_fails_closed_not_silently_truncates() -> None:
    # Renata handback (attempt 1): the corrupted-cursor guard only fails
    # closed on int(cursor) raising ValueError (non-numeric strings). A
    # cursor that parses successfully but is semantically invalid --
    # e.g. "-1" -- was not rejected: negative-index slicing silently wraps
    # to the tail of the identity-sorted list instead of raising, dropping
    # issues with no recorded failure. Same "cursor loss"/"silent
    # guessing" class of bug as the non-numeric case, via a
    # syntactically-valid path.
    connector = InMemoryConnector(name="jira", workspace="demo")
    for idx in range(5):
        await connector.create_issue(_issue(f"NEG-{idx}"))

    store = InMemoryIssueStore()
    engine = SyncEngine(
        connector=connector, store=store, policy=OwnershipPolicy.external_authoritative()
    )
    engine.restore_checkpoint(SyncCheckpoint(cursor="-1", updated_since=None))

    result = await engine.pull()  # must not silently wrap/truncate

    assert len(result.failures) == 1
    failure = result.failures[0]
    assert failure.operation == "pull_page"
    assert failure.retryable is False

    stored = await store.list_issues()
    assert stored == []
