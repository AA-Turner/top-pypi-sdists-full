"""TRK-M1-03 N13 (frozen matrix §4.2): conflict-loop fixed point.

Renata HANDBACK (attempt-1, MEDIUM): N13 is explicitly owned by TRK-M1-03 /
REQ-06 and named in the §5 decomposition row ("tests P3-P9, N1-N5, N9-N18,
N20"), but no test anywhere called ``SyncEngine.sync()`` -- the combined
pull+push method N13 exercises -- so the conformance suite could not
honestly claim to pass a conflict-loop test that did not exist.

This closes that gap: split ownership (status=EXTERNAL, title left on the
SHARED default), a genuine initial conflict on the SHARED title field
resolved by NEWER_TIMESTAMP, and three consecutive ``sync()`` calls on the
same engine/store/connector with no external edits in between. The engine
must converge to a fixed point -- the second and third runs must not find
anything left to reconcile, and the local store's observable state must be
identical from the moment the fixed point is first reached.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

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
)


def _make_issue(
    *,
    issue_id: str,
    title: str,
    status: CanonicalStatus,
    updated_at: datetime,
) -> CanonicalIssue:
    return CanonicalIssue(
        ref=ExternalRef(system="jira", workspace="demo", id=issue_id, key=issue_id),
        title=title,
        body="Body",
        status=status,
        issue_type=CanonicalIssueType.TASK,
        updated_at=updated_at,
    )


async def test_conflict_loop_converges_to_fixed_point() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    store = InMemoryIssueStore()

    older = datetime(2024, 1, 1, tzinfo=UTC)
    newer = older + timedelta(hours=1)

    # N13 setup: split ownership (status is EXTERNAL-owned; title is left on
    # the SHARED default so it is genuinely contested), a real conflict on
    # the SHARED title field (local is newer, so NEWER_TIMESTAMP must pick
    # local), and no external edits between sync() calls. Seeded directly
    # into the connector's store (rather than via create_issue, which
    # stamps updated_at with the real wall clock) so the initial
    # local-newer-than-remote ordering the scenario requires is exact and
    # deterministic.
    remote_ref = ExternalRef(system="jira", workspace="demo", id="DEMO-13", key="DEMO-13")
    connector._issues[remote_ref.identity] = _make_issue(
        issue_id="DEMO-13",
        title="Remote Title",
        status=CanonicalStatus.IN_PROGRESS,
        updated_at=older,
    )
    await store.upsert_issue(
        _make_issue(
            issue_id="DEMO-13",
            title="Local Title",
            status=CanonicalStatus.TODO,
            updated_at=newer,
        )
    )

    policy = OwnershipPolicy.split(
        field_owners={"status": FieldOwner.EXTERNAL},
        default_owner=FieldOwner.SHARED,
    )
    engine = SyncEngine(
        connector=connector,
        store=store,
        policy=policy,
        strategy=ConflictStrategy.NEWER_TIMESTAMP,
    )

    # First run: resolves the genuine initial conflict (title -> local,
    # since local is newer) and pushes the resolution to the remote.
    first = await engine.sync()
    assert first.stats.pushed_updated == 1
    after_first = list(await store.list_issues())

    # Second and third runs: nothing left to reconcile -- no conflicts, no
    # pushes, no pulls that change anything, and the local store's
    # observable state is byte-for-byte identical to the first run's
    # converged state.
    second = await engine.sync()
    assert second.stats.pushed_updated == 0
    assert second.stats.pulled_updated == 0
    assert second.conflicts == []
    after_second = list(await store.list_issues())
    assert after_second == after_first

    third = await engine.sync()
    assert third.stats.pushed_updated == 0
    assert third.stats.pulled_updated == 0
    assert third.conflicts == []
    after_third = list(await store.list_issues())
    assert after_third == after_first

    # The fixed point is also reflected in the resolved fields themselves.
    settled = await store.get_issue(
        ExternalRef(system="jira", workspace="demo", id="DEMO-13", key="DEMO-13")
    )
    assert settled is not None
    assert settled.title == "Local Title"
    assert settled.status == CanonicalStatus.IN_PROGRESS
