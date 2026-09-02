"""TRK-M1-03 A11/A12: partial-failure push/pull, capability-aware patch
exclusion, and the public checkpoint-restore API.

N4 (push side): a field whose capability flag is False is excluded from the
outgoing patch and recorded as a ``patch_field_denied`` failure, not sent.
N11: cursor loss -- a fresh engine that calls ``restore_checkpoint`` resumes
exactly where a crashed engine left off.
N14: a non-retryable failure on one issue during push does not abort the
other issues; it is recorded as a ``SyncFailure`` and the run continues.
N15: a pull page failure (after retries) stops the loop without advancing
the checkpoint past the last fully processed page.
P8: ``restore_checkpoint`` makes the next ``pull`` resume at that cursor.
"""

from __future__ import annotations

from collections.abc import Mapping

from spec_kitty_tracker import (
    CanonicalIssue,
    CanonicalIssueType,
    CanonicalStatus,
    CapabilityNotSupportedError,
    ConnectorRequestError,
    ExternalRef,
    FailureClass,
    InMemoryConnector,
    InMemoryIssueStore,
    OwnershipPolicy,
    SyncCheckpoint,
    SyncEngine,
    TrackerCapabilities,
)


def _issue(issue_id: str, status: CanonicalStatus = CanonicalStatus.TODO) -> CanonicalIssue:
    return CanonicalIssue(
        ref=ExternalRef(system="jira", workspace="demo", id=issue_id, key=issue_id),
        title=f"Issue {issue_id}",
        body="body",
        status=status,
        issue_type=CanonicalIssueType.TASK,
    )


class _NoAssignmentConnector(InMemoryConnector):
    """InMemory connector that honestly reports it cannot carry assignment
    or a terminal transition, to exercise A11's capability-aware exclusion."""

    async def get_capabilities(self) -> TrackerCapabilities:
        return TrackerCapabilities(supports_assignment=False, supports_terminal_transition=False)


class _FlakyOnRefConnector(InMemoryConnector):
    def __init__(self, *, name: str, workspace: str, fail_id: str) -> None:
        super().__init__(name=name, workspace=workspace)
        self.fail_id = fail_id
        self.update_calls: list[str] = []

    async def update_issue(
        self,
        ref: ExternalRef,
        patch: Mapping[str, object],
        *,
        idempotency_key: str | None,
    ) -> CanonicalIssue:
        self.update_calls.append(ref.id)
        if ref.id == self.fail_id:
            raise ConnectorRequestError(
                "validation failed",
                status_code=422,
                failure_class=FailureClass.VALIDATION,
                provider=self.name,
            )
        return await super().update_issue(ref, patch, idempotency_key=idempotency_key)


class _CapabilityRefusalOnRefConnector(InMemoryConnector):
    def __init__(self, *, name: str, workspace: str, fail_id: str) -> None:
        super().__init__(name=name, workspace=workspace)
        self.fail_id = fail_id
        self.update_calls: list[str] = []

    async def update_issue(
        self,
        ref: ExternalRef,
        patch: Mapping[str, object],
        *,
        idempotency_key: str | None,
    ) -> CanonicalIssue:
        self.update_calls.append(ref.id)
        if ref.id == self.fail_id:
            raise CapabilityNotSupportedError("custom_fields are not supported")
        return await super().update_issue(ref, patch, idempotency_key=idempotency_key)


class _FailOnPageConnector(InMemoryConnector):
    """Fails list_issues on the Nth call (1-indexed), always with a
    transient error, to exercise pull-side partial failure / cursor loss."""

    def __init__(self, *, name: str, workspace: str, fail_on_call: int) -> None:
        super().__init__(name=name, workspace=workspace)
        self.fail_on_call = fail_on_call
        self.call_count = 0

    async def list_issues(self, **kwargs: object):  # type: ignore[override]
        self.call_count += 1
        if self.call_count >= self.fail_on_call:
            raise ConnectorRequestError(
                "transient outage",
                status_code=503,
                failure_class=FailureClass.TRANSIENT,
                provider=self.name,
            )
        return await super().list_issues(**kwargs)  # type: ignore[arg-type]


async def test_push_excludes_assignees_and_terminal_status_when_unsupported() -> None:
    connector = _NoAssignmentConnector(name="jira", workspace="demo")
    store = InMemoryIssueStore()

    remote = _issue("SP-1", status=CanonicalStatus.TODO)
    await connector.create_issue(remote)

    local_issue = remote.clone()
    local_issue.assignees = ["ivan"]
    local_issue.status = CanonicalStatus.DONE
    await store.upsert_issue(local_issue)

    engine = SyncEngine(
        connector=connector, store=store, policy=OwnershipPolicy.local_authoritative()
    )
    result = await engine.push()

    remote_after = await connector.get_issue(remote.ref)
    assert remote_after.assignees == []
    assert remote_after.status == CanonicalStatus.TODO
    denied_ops = [f for f in result.failures if f.operation == "patch_field_denied"]
    assert len(denied_ops) == 2
    assert {f.retryable for f in denied_ops} == {False}


async def test_push_partial_failure_continues_other_issues() -> None:
    connector = _FlakyOnRefConnector(name="jira", workspace="demo", fail_id="SP-2")
    store = InMemoryIssueStore()

    for issue_id in ("SP-1", "SP-2", "SP-3"):
        remote = _issue(issue_id)
        await connector.create_issue(remote)
        local = remote.clone()
        local.title = f"Updated {issue_id}"
        await store.upsert_issue(local)

    engine = SyncEngine(
        connector=connector, store=store, policy=OwnershipPolicy.local_authoritative()
    )
    result = await engine.push()

    assert result.stats.pushed_updated == 2
    assert len(result.failures) == 1
    failure = result.failures[0]
    assert failure.issue_ref is not None and failure.issue_ref.id == "SP-2"
    assert failure.operation == "update"
    assert failure.retryable is False
    assert failure.failure_class is FailureClass.VALIDATION
    assert len(result.errors) == 1

    sp1 = await connector.get_issue(ExternalRef(system="jira", workspace="demo", id="SP-1"))
    sp3 = await connector.get_issue(ExternalRef(system="jira", workspace="demo", id="SP-3"))
    assert sp1.title == "Updated SP-1"
    assert sp3.title == "Updated SP-3"


async def test_push_runtime_capability_refusal_continues_other_issues() -> None:
    connector = _CapabilityRefusalOnRefConnector(name="jira", workspace="demo", fail_id="SP-2")
    store = InMemoryIssueStore()

    for issue_id in ("SP-1", "SP-2", "SP-3"):
        remote = _issue(issue_id)
        await connector.create_issue(remote)
        local = remote.clone()
        local.custom_fields = {"owner": issue_id}
        await store.upsert_issue(local)

    engine = SyncEngine(
        connector=connector, store=store, policy=OwnershipPolicy.local_authoritative()
    )
    result = await engine.push()

    assert result.stats.pushed_updated == 2
    assert len(result.failures) == 1
    failure = result.failures[0]
    assert failure.issue_ref is not None and failure.issue_ref.id == "SP-2"
    assert failure.operation == "update"
    assert failure.failure_class is None
    assert failure.retryable is False

    sp1 = await connector.get_issue(ExternalRef(system="jira", workspace="demo", id="SP-1"))
    sp3 = await connector.get_issue(ExternalRef(system="jira", workspace="demo", id="SP-3"))
    assert sp1.custom_fields == {"owner": "SP-1"}
    assert sp3.custom_fields == {"owner": "SP-3"}


async def test_pull_partial_failure_does_not_advance_checkpoint_past_last_good_page() -> None:
    connector = _FailOnPageConnector(name="jira", workspace="demo", fail_on_call=99)
    for idx in range(5):
        await connector.create_issue(_issue(f"I-{idx}"))
    connector.fail_on_call = connector.call_count + 2  # fail on the 2nd list_issues call

    store = InMemoryIssueStore()
    engine = SyncEngine(
        connector=connector,
        store=store,
        policy=OwnershipPolicy.external_authoritative(),
        max_retry_attempts=1,
    )

    result = await engine.pull(limit=2)

    assert len(result.failures) == 1
    failure = result.failures[0]
    assert failure.operation == "pull_page"
    assert failure.retryable is True

    stored = await store.list_issues()
    assert len(stored) == 2
    assert engine.checkpoint.cursor == "2"


async def test_restore_checkpoint_resumes_pull_at_persisted_cursor() -> None:
    """P8: restore_checkpoint(SyncCheckpoint(cursor="2", ...)) makes the
    next pull() start fetching at page cursor "2", not from the beginning."""
    connector = InMemoryConnector(name="jira", workspace="demo")
    for idx in range(5):
        await connector.create_issue(_issue(f"I-{idx}"))

    store = InMemoryIssueStore()
    engine = SyncEngine(
        connector=connector,
        store=store,
        policy=OwnershipPolicy.external_authoritative(),
    )
    engine.restore_checkpoint(SyncCheckpoint(cursor="2", updated_since=None))

    result = await engine.pull(limit=2)

    assert result.stats.pulled_created == 3
    stored = await store.list_issues()
    assert {issue.ref.id for issue in stored} == {"I-2", "I-3", "I-4"}
    assert engine.checkpoint.cursor is None


async def test_cursor_loss_crash_and_resume_converges_to_full_store() -> None:
    """N11: a crash after page 1 leaves the checkpoint at cursor "2"; a
    fresh engine that restores it and resumes converges to all 5 issues,
    re-delivering no more than the boundary item."""
    connector = _FailOnPageConnector(name="jira", workspace="demo", fail_on_call=2)
    for idx in range(5):
        await connector.create_issue(_issue(f"I-{idx}"))

    store = InMemoryIssueStore()
    crashing_engine = SyncEngine(
        connector=connector,
        store=store,
        policy=OwnershipPolicy.external_authoritative(),
        max_retry_attempts=0,
    )
    crash_result = await crashing_engine.pull(limit=2)
    assert len(crash_result.failures) == 1
    persisted_checkpoint = crashing_engine.checkpoint
    assert persisted_checkpoint.cursor == "2"

    connector.fail_on_call = 10_000  # no further failures on resume
    resumed_engine = SyncEngine(
        connector=connector,
        store=store,
        policy=OwnershipPolicy.external_authoritative(),
    )
    resumed_engine.restore_checkpoint(persisted_checkpoint)
    await resumed_engine.pull(limit=2)

    stored = await store.list_issues()
    assert {issue.ref.id for issue in stored} == {f"I-{i}" for i in range(5)}
    assert resumed_engine.checkpoint.cursor is None


async def test_restart_after_full_completion_is_a_convergent_no_op() -> None:
    """N12 (Tracker-level restart): restoring a checkpoint from a
    completed run and pulling again performs no further creates/updates --
    the result is byte-identical to the single uninterrupted run."""
    connector = InMemoryConnector(name="jira", workspace="demo")
    for idx in range(5):
        await connector.create_issue(_issue(f"I-{idx}"))

    store = InMemoryIssueStore()
    engine = SyncEngine(
        connector=connector,
        store=store,
        policy=OwnershipPolicy.external_authoritative(),
    )
    first_result = await engine.pull(limit=2)
    assert first_result.stats.pulled_created == 5
    completed_checkpoint = engine.checkpoint

    resumed_engine = SyncEngine(
        connector=connector,
        store=store,
        policy=OwnershipPolicy.external_authoritative(),
    )
    resumed_engine.restore_checkpoint(completed_checkpoint)
    second_result = await resumed_engine.pull(limit=2)

    # Only the last-touched issue is re-examined -- updated_since filters
    # out everything else that has not changed since the completed run.
    assert second_result.stats.pulled_created == 0
    assert second_result.stats.pulled_updated == 0
    stored = await store.list_issues()
    assert len(stored) == 5
