from __future__ import annotations

from collections.abc import Mapping

import pytest

from spec_kitty_tracker import (
    BidirectionalIssueSync,
    CanonicalIssue,
    CanonicalIssueType,
    CanonicalLink,
    CanonicalStatus,
    CapabilityNotSupportedError,
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


class _StatusRefusalRecordingConnector(InMemoryConnector):
    """Records `upsert_link`/`add_comment` calls and can refuse the status
    portion of an `update_issue` patch with a chosen capability tag."""

    def __init__(
        self,
        *,
        name: str,
        workspace: str,
        refuse_status: bool = False,
        refuse_capability: str | None = "status",
    ) -> None:
        super().__init__(name=name, workspace=workspace)
        self.refuse_status = refuse_status
        self.refuse_capability = refuse_capability
        self.update_calls: list[Mapping[str, object]] = []
        self.upsert_link_calls: list[CanonicalLink] = []
        self.add_comment_calls: list[str] = []

    async def update_issue(
        self,
        ref: ExternalRef,
        patch: Mapping[str, object],
        *,
        idempotency_key: str | None,
    ) -> CanonicalIssue:
        self.update_calls.append(dict(patch))
        if self.refuse_status and "status" in patch:
            raise CapabilityNotSupportedError(
                f"No Jira transition matches status '{patch['status']}'",
                capability=self.refuse_capability,
            )
        return await super().update_issue(ref, patch, idempotency_key=idempotency_key)

    async def upsert_link(self, ref: ExternalRef, link: CanonicalLink) -> None:
        self.upsert_link_calls.append(link)
        await super().upsert_link(ref, link)

    async def add_comment(self, ref: ExternalRef, body: str) -> None:
        self.add_comment_calls.append(body)
        await super().add_comment(ref, body)


def _mission_update_with_decision() -> tuple[MissionUpdate, DecisionReference]:
    decision_ref = DecisionReference(
        decision_id="DEC-909",
        summary="Confirm terminal status",
        blocking=True,
        external_ref=_issue_ref("jira", "ARCH-9"),
    )
    update = MissionUpdate(
        mission_id="mission:refusal",
        mission_state="done",
        target_status=CanonicalStatus.DONE,
        summary="Mission complete.",
        decision_references=[decision_ref],
    )
    return update, decision_ref


async def test_publish_mission_update_status_refusal_persists_side_effects_then_reraises() -> None:
    connector = _StatusRefusalRecordingConnector(
        name="jira", workspace="jira-demo", refuse_status=True, refuse_capability="status"
    )
    sync = BidirectionalIssueSync(connector=connector)
    source_issue = _make_issue("jira", "JRA-501", CanonicalStatus.IN_PROGRESS)
    await connector.create_issue(source_issue)

    update, decision_ref = _mission_update_with_decision()

    with pytest.raises(CapabilityNotSupportedError):
        await sync.publish_mission_update(issue_ref=source_issue.ref, update=update)

    assert len(connector.upsert_link_calls) == 1
    assert connector.upsert_link_calls[0].type is LinkType.BLOCKED_BY
    assert connector.upsert_link_calls[0].target == decision_ref.external_ref
    assert len(connector.add_comment_calls) == 1
    assert "DEC-909" in connector.add_comment_calls[-1]


@pytest.mark.parametrize("refuse_capability", [None, "labels"])
async def test_publish_mission_update_non_status_refusal_reraises_immediately(
    refuse_capability: str | None,
) -> None:
    # Both the untagged (None) and the non-status-tagged ("labels") refusal must
    # re-raise before any side effect. The "labels" case exercises the predicate's
    # actual == "status" comparison: weakening it to `capability is not None` would
    # wrongly run the degrade path here and go RED (upserts/comment would fire).
    connector = _StatusRefusalRecordingConnector(
        name="jira",
        workspace="jira-demo",
        refuse_status=True,
        refuse_capability=refuse_capability,
    )
    sync = BidirectionalIssueSync(connector=connector)
    source_issue = _make_issue("jira", "JRA-502", CanonicalStatus.IN_PROGRESS)
    await connector.create_issue(source_issue)

    update, _decision_ref = _mission_update_with_decision()

    with pytest.raises(CapabilityNotSupportedError):
        await sync.publish_mission_update(issue_ref=source_issue.ref, update=update)

    assert connector.upsert_link_calls == []
    assert connector.add_comment_calls == []


async def test_publish_mission_update_happy_path_applies_update_links_and_comment() -> None:
    connector = _StatusRefusalRecordingConnector(name="jira", workspace="jira-demo")
    sync = BidirectionalIssueSync(connector=connector)
    source_issue = _make_issue("jira", "JRA-503", CanonicalStatus.IN_PROGRESS)
    await connector.create_issue(source_issue)

    update, decision_ref = _mission_update_with_decision()

    result = await sync.publish_mission_update(issue_ref=source_issue.ref, update=update)

    assert result.status is CanonicalStatus.DONE
    assert len(connector.upsert_link_calls) == 1
    assert connector.upsert_link_calls[0].target == decision_ref.external_ref
    assert len(connector.add_comment_calls) == 1

    stored_issue = await connector.get_issue(source_issue.ref)
    assert stored_issue.status is CanonicalStatus.DONE
    assert any(link.type is LinkType.BLOCKED_BY for link in stored_issue.links)
