from __future__ import annotations

from collections.abc import Mapping

import pytest

from spec_kitty_tracker import (
    BidirectionalIssueSync,
    CanonicalIssue,
    CanonicalIssueType,
    CanonicalStatus,
    ConflictStrategy,
    ConnectorRequestError,
    DecisionReference,
    ExternalRef,
    FailureClass,
    InMemoryConnector,
    InMemoryIssueStore,
    LinkType,
    MissionUpdate,
    OwnershipPolicy,
    SyncEngine,
)


def _issue_ref(provider: str, issue_id: str) -> ExternalRef:
    return ExternalRef(
        system=provider,
        workspace=f"{provider}-demo",
        id=issue_id,
        key=issue_id,
    )


def _make_issue(provider: str, issue_id: str, status: CanonicalStatus) -> CanonicalIssue:
    return CanonicalIssue(
        ref=_issue_ref(provider, issue_id),
        title=f"{provider.upper()} issue {issue_id}",
        body="sync core test",
        status=status,
        issue_type=CanonicalIssueType.TASK,
    )


@pytest.mark.parametrize("provider", ["jira", "linear", "github", "gitlab"])
async def test_round_trip_sync_for_p0_provider(provider: str) -> None:
    connector = InMemoryConnector(name=provider, workspace=f"{provider}-demo")
    store = InMemoryIssueStore()
    engine = SyncEngine(
        connector=connector,
        store=store,
        policy=OwnershipPolicy.local_authoritative(),
        strategy=ConflictStrategy.NEWER_TIMESTAMP,
    )

    source_issue = _make_issue(provider, "P0-1", CanonicalStatus.TODO)
    await connector.create_issue(source_issue)

    pull_result = await engine.pull()
    assert pull_result.stats.pulled_created == 1

    local_issue = await store.get_issue(source_issue.ref)
    assert local_issue is not None
    local_issue.status = CanonicalStatus.BLOCKED
    local_issue.custom_fields["sync_origin"] = "mission"
    await store.upsert_issue(local_issue)

    push_result = await engine.push()
    assert push_result.stats.pushed_updated == 1

    remote_issue = await connector.get_issue(source_issue.ref)
    assert remote_issue.status is CanonicalStatus.BLOCKED
    assert remote_issue.custom_fields["sync_origin"] == "mission"


async def test_publish_mission_update_persists_decision_references() -> None:
    connector = InMemoryConnector(name="jira", workspace="jira-demo")
    sync = BidirectionalIssueSync(connector=connector)
    source_issue = _make_issue("jira", "JRA-42", CanonicalStatus.IN_PROGRESS)
    await connector.create_issue(source_issue)

    decision_ref = DecisionReference(
        decision_id="DEC-404",
        summary="Choose React over Vue for runtime parity",
        blocking=True,
        external_ref=_issue_ref("jira", "ARCH-12"),
    )
    update = MissionUpdate(
        mission_id="mission:alpha",
        mission_state="waiting_on_decision",
        target_status=CanonicalStatus.BLOCKED,
        summary="Blocked until architecture decision is confirmed.",
        mission_url="https://spec-kitty.example/missions/alpha",
        decision_references=[decision_ref],
    )

    await sync.publish_mission_update(issue_ref=source_issue.ref, update=update)
    updated_issue = await connector.get_issue(source_issue.ref)

    assert updated_issue.status is CanonicalStatus.BLOCKED
    mission_meta = updated_issue.custom_fields["spec_kitty_mission"]
    assert mission_meta["mission_id"] == "mission:alpha"
    assert mission_meta["mission_state"] == "waiting_on_decision"
    assert mission_meta["decision_refs"][0]["decision_id"] == "DEC-404"
    assert any(link.type is LinkType.BLOCKED_BY for link in updated_issue.links)

    comments = updated_issue.custom_fields["comments"]
    assert isinstance(comments, list)
    assert "DEC-404" in comments[-1]


class _FlakyRetryConnector(InMemoryConnector):
    def __init__(self, *, name: str, workspace: str) -> None:
        super().__init__(name=name, workspace=workspace)
        self.update_attempts = 0
        self.idempotency_keys: list[str | None] = []

    async def update_issue(
        self,
        ref: ExternalRef,
        patch: Mapping[str, object],
        *,
        idempotency_key: str | None,
    ) -> CanonicalIssue:
        self.update_attempts += 1
        self.idempotency_keys.append(idempotency_key)
        if self.update_attempts == 1:
            raise ConnectorRequestError(
                "transient service outage",
                status_code=503,
                provider=self.name,
                failure_class=FailureClass.TRANSIENT,
            )
        return await super().update_issue(ref, patch, idempotency_key=idempotency_key)


async def test_sync_engine_retries_retryable_update_with_stable_idempotency_key() -> None:
    connector = _FlakyRetryConnector(name="jira", workspace="jira-demo")
    store = InMemoryIssueStore()
    engine = SyncEngine(
        connector=connector,
        store=store,
        policy=OwnershipPolicy.local_authoritative(),
    )

    source_issue = _make_issue("jira", "JRA-77", CanonicalStatus.TODO)
    await connector.create_issue(source_issue)
    await engine.pull()

    local_issue = await store.get_issue(source_issue.ref)
    assert local_issue is not None
    local_issue.status = CanonicalStatus.IN_PROGRESS
    await store.upsert_issue(local_issue)

    result = await engine.push()
    assert result.stats.pushed_updated == 1
    assert connector.update_attempts == 2
    assert connector.idempotency_keys == [
        f"sync:{source_issue.ref.identity}",
        f"sync:{source_issue.ref.identity}",
    ]
