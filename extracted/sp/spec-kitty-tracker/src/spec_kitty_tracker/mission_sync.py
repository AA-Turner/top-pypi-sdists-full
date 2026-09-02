from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from spec_kitty_tracker.errors import (
    CapabilityNotSupportedError,
    ConnectorRequestError,
    DecisionReferenceContractError,
    is_status_transition_refusal,
)
from spec_kitty_tracker.models import (
    CanonicalIssue,
    CanonicalLink,
    CanonicalStatus,
    ExternalRef,
    LinkType,
    utcnow,
)
from spec_kitty_tracker.protocols import TaskTrackerConnector

FORBIDDEN_TEAMSPACE_LEGACY_KEYS = frozenset({"feature_slug", "feature_number", "mission_key"})


@dataclass(frozen=True, slots=True)
class DecisionReference:
    decision_id: str
    summary: str | None = None
    blocking: bool = True
    url: str | None = None
    external_ref: ExternalRef | None = None

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "decision_id": self.decision_id,
            "summary": self.summary,
            "blocking": self.blocking,
            "url": self.url,
        }
        if self.external_ref is not None:
            payload["external_ref"] = {
                "system": self.external_ref.system,
                "workspace": self.external_ref.workspace,
                "id": self.external_ref.id,
                "key": self.external_ref.key,
                "url": self.external_ref.url,
            }
        return payload


@dataclass(frozen=True, slots=True)
class MissionSeed:
    mission_id: str
    source_issue_ref: ExternalRef
    title: str
    body: str | None
    status: CanonicalStatus
    priority: int | None
    assignees: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    decision_references: list[DecisionReference] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class MissionUpdate:
    mission_id: str
    mission_state: str
    target_status: CanonicalStatus | None = None
    summary: str | None = None
    mission_url: str | None = None
    decision_references: list[DecisionReference] = field(default_factory=list)


def _parse_decision_refs(raw: Any) -> list[DecisionReference]:
    """A13 (TRK-M1-03): strict decision-reference parsing.

    An absent key or ``None`` is not malformed and yields ``[]``. Anything
    else that is not a list, a list entry that is not a dict or lacks a
    non-empty ``decision_id``, or an ``external_ref`` that fails
    :class:`ExternalRef` validation raises a typed
    ``DecisionReferenceContractError`` instead of being silently dropped.
    """
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise DecisionReferenceContractError(
            "custom_fields.decision_refs must be a list",
            kind="mission",
            field_path="decision_refs",
            reason="DR-001",
        )

    parsed: list[DecisionReference] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise DecisionReferenceContractError(
                "decision_refs entry must be an object",
                kind="mission",
                field_path=f"decision_refs[{index}]",
                reason="DR-001",
            )
        decision_id = str(item.get("decision_id", "")).strip()
        if not decision_id:
            raise DecisionReferenceContractError(
                "decision_refs entry missing a non-empty decision_id",
                kind="mission",
                field_path=f"decision_refs[{index}].decision_id",
                reason="DR-001",
            )
        ref_data = item.get("external_ref")
        external_ref: ExternalRef | None = None
        if isinstance(ref_data, dict):
            try:
                external_ref = ExternalRef(
                    system=str(ref_data.get("system", "")),
                    workspace=str(ref_data.get("workspace", "")),
                    id=str(ref_data.get("id", "")),
                    key=str(ref_data.get("key")) if ref_data.get("key") is not None else None,
                    url=str(ref_data.get("url")) if ref_data.get("url") is not None else None,
                )
            except ValueError as exc:
                raise DecisionReferenceContractError(
                    f"decision_refs entry has an invalid external_ref: {exc}",
                    kind="mission",
                    field_path=f"decision_refs[{index}].external_ref",
                    reason="DR-002",
                ) from exc
        parsed.append(
            DecisionReference(
                decision_id=decision_id,
                summary=str(item.get("summary")) if item.get("summary") is not None else None,
                blocking=bool(item.get("blocking", True)),
                url=str(item.get("url")) if item.get("url") is not None else None,
                external_ref=external_ref,
            )
        )
    return parsed


def mission_seed_from_issue(issue: CanonicalIssue, *, mission_id: str | None = None) -> MissionSeed:
    resolved_mission_id = mission_id or f"mission:{issue.ref.identity}"
    decision_refs = _parse_decision_refs(issue.custom_fields.get("decision_refs"))
    return MissionSeed(
        mission_id=resolved_mission_id,
        source_issue_ref=issue.ref,
        title=issue.title,
        body=issue.body,
        status=issue.status,
        priority=issue.priority,
        assignees=list(issue.assignees),
        labels=list(issue.labels),
        decision_references=decision_refs,
    )


class BidirectionalIssueSync:
    def __init__(self, *, connector: TaskTrackerConnector, max_retry_attempts: int = 2) -> None:
        self.connector = connector
        self.max_retry_attempts = max_retry_attempts

    async def mission_from_issue(
        self, issue_ref: ExternalRef, *, mission_id: str | None = None
    ) -> MissionSeed:
        issue = await self.connector.get_issue(issue_ref)
        return mission_seed_from_issue(issue, mission_id=mission_id)

    async def publish_mission_update(
        self,
        *,
        issue_ref: ExternalRef,
        update: MissionUpdate,
    ) -> CanonicalIssue:
        issue = await self.connector.get_issue(issue_ref)
        patch: dict[str, Any] = {}

        if update.target_status is not None:
            patch["status"] = update.target_status

        custom_fields = dict(issue.custom_fields)
        # ``tracker_sync_pushed_at`` is egress sync metadata: the wall-clock
        # moment this tracker push was issued. It is NOT canonical mission
        # occurrence/completion time and MUST NOT be consumed as such by
        # downstream readers (see spec-kitty-events Rule R-T-01 — canonical
        # event time lives on the producer envelope's ``timestamp`` /
        # ``occurred_at``, not on tracker sync metadata).
        mission_payload = {
            "mission_id": update.mission_id,
            "mission_state": update.mission_state,
            "mission_url": update.mission_url,
            "tracker_sync_pushed_at": utcnow().isoformat(),
            "decision_refs": [ref.as_dict() for ref in update.decision_references],
        }
        custom_fields["spec_kitty_mission"] = mission_payload
        # N2 (TRK-M1-03): guard the *whole* outgoing custom_fields, not just
        # the newly written mission_payload -- a pre-existing legacy key
        # elsewhere in issue.custom_fields must also be rejected before any
        # egress call is made.
        assert_no_forbidden_teamspace_legacy_keys(custom_fields)
        patch["custom_fields"] = custom_fields

        idempotency_key = f"mission-update:{update.mission_id}:{issue_ref.identity}"
        # A Jira project may refuse the status transition while accepting every
        # other part of the mission update. Defer that refusal so the decision
        # links and the mission backlink comment below still get applied -- then
        # surface it. Raising here would silently cost the caller both, which is
        # a worse outcome than a late raise. Any other capability refusal is not
        # ours to interpret and propagates immediately.
        status_refusal: CapabilityNotSupportedError | None = None
        try:
            updated = await self._update_issue_with_retry(
                ref=issue_ref,
                patch=patch,
                idempotency_key=idempotency_key,
            )
        except CapabilityNotSupportedError as exc:
            if not is_status_transition_refusal(exc):
                raise
            status_refusal = exc
            updated = issue  # pre-update issue; the return value is moot on the re-raise path

        for decision_ref in update.decision_references:
            if decision_ref.blocking and decision_ref.external_ref is not None:
                await self.connector.upsert_link(
                    issue_ref,
                    CanonicalLink(type=LinkType.BLOCKED_BY, target=decision_ref.external_ref),
                )

        capabilities = await self.connector.get_capabilities()
        if capabilities.supports_comments:
            await self.connector.add_comment(issue_ref, _render_mission_comment(update))

        if status_refusal is not None:
            raise status_refusal

        return updated

    async def _update_issue_with_retry(
        self,
        *,
        ref: ExternalRef,
        patch: dict[str, Any],
        idempotency_key: str,
    ) -> CanonicalIssue:
        attempt = 0
        while True:
            try:
                return await self.connector.update_issue(
                    ref,
                    patch,
                    idempotency_key=idempotency_key,
                )
            except ConnectorRequestError as exc:
                if not exc.is_retryable or attempt >= self.max_retry_attempts:
                    raise
                attempt += 1


def _render_mission_comment(update: MissionUpdate) -> str:
    """Render a stable, parseable mission backlink comment.

    Format contract (line ordering is guaranteed):
        Line 1: ``Spec Kitty mission update: <mission_id>``
        Line 2: ``State: <mission_state>``
        Line 3 (optional): ``Summary: <summary>``        — omitted when summary is empty or None
        Line 4 (optional): ``Mission: <mission_url>``     — omitted when mission_url is
        empty or None
        Line 5 (optional): ``Decision refs: <id>, ...``   — omitted when no decision
        references

    Empty strings are treated identically to ``None`` (field is omitted).
    """
    decision_ids = ", ".join(ref.decision_id for ref in update.decision_references)
    lines = [
        f"Spec Kitty mission update: {update.mission_id}",
        f"State: {update.mission_state}",
    ]
    if update.summary:
        sanitized = " ".join(update.summary.splitlines())
        lines.append(f"Summary: {sanitized}")
    if update.mission_url:
        lines.append(f"Mission: {update.mission_url}")
    if decision_ids:
        lines.append(f"Decision refs: {decision_ids}")
    return "\n".join(lines)


def decision_link_mismatches(
    issue: CanonicalIssue, update: MissionUpdate
) -> list[DecisionReferenceContractError]:
    """A13 (TRK-M1-03): compare what was published on ``issue`` (the
    ``spec_kitty_mission.decision_refs`` payload written by a prior
    :func:`BidirectionalIssueSync.publish_mission_update` call) against the
    mission's own ``update.decision_references`` and return every
    mismatch found. Not raised automatically and not wired into
    ``publish_mission_update`` -- hosts and TRK-M1-06 call this explicitly.

    This function never mutates either input and never reads or writes the
    upstream ``custom_fields.decision_refs`` seed field -- the two
    directions (upstream seed vs. Spec Kitty-published mission payload)
    stay independent, per docs/wp11-sync-core-notes.md.
    """
    mismatches: list[DecisionReferenceContractError] = []

    mission_payload = issue.custom_fields.get("spec_kitty_mission")
    published_refs: list[dict[str, Any]] = []
    if isinstance(mission_payload, dict):
        raw_published = mission_payload.get("decision_refs")
        if isinstance(raw_published, list):
            published_refs = [entry for entry in raw_published if isinstance(entry, dict)]

    published_by_id = {
        str(entry.get("decision_id")): entry
        for entry in published_refs
        if entry.get("decision_id") is not None
    }
    mission_by_id = {ref.decision_id: ref for ref in update.decision_references}

    if set(published_by_id) != set(mission_by_id):
        mismatches.append(
            DecisionReferenceContractError(
                "Published decision_refs set does not match the mission's decision_references set",
                kind="mission",
                field_path="spec_kitty_mission.decision_refs",
                reason="DR-003",
            )
        )

    existing_blocked_by_targets = {
        link.target.identity for link in issue.links if link.type is LinkType.BLOCKED_BY
    }
    for decision_id, mission_ref in mission_by_id.items():
        if not (mission_ref.blocking and mission_ref.external_ref is not None):
            continue
        if mission_ref.external_ref.identity not in existing_blocked_by_targets:
            mismatches.append(
                DecisionReferenceContractError(
                    f"Blocking decision reference {decision_id!r} has no "
                    "corresponding BLOCKED_BY link on the issue",
                    kind="mission",
                    field_path=f"decision_refs[{decision_id}]",
                    reason="DR-004",
                )
            )

    for decision_id, mission_ref in mission_by_id.items():
        published_entry = published_by_id.get(decision_id)
        if published_entry is None:
            continue
        if published_entry != mission_ref.as_dict():
            mismatches.append(
                DecisionReferenceContractError(
                    f"Published decision reference {decision_id!r} no longer "
                    "matches the mission's entry",
                    kind="mission",
                    field_path=f"spec_kitty_mission.decision_refs[{decision_id}]",
                    reason="DR-005",
                )
            )

    return mismatches


def assert_no_forbidden_teamspace_legacy_keys(payload: dict[str, Any]) -> None:
    """Fail if tracker egress would emit legacy TeamSpace mission keys."""
    found = sorted(_find_forbidden_teamspace_legacy_keys(payload))
    if found:
        raise ValueError(f"Forbidden TeamSpace legacy keys in tracker payload: {', '.join(found)}")


def _find_forbidden_teamspace_legacy_keys(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_TEAMSPACE_LEGACY_KEYS:
                found.add(key)
            found.update(_find_forbidden_teamspace_legacy_keys(child))
    elif isinstance(value, list):
        for child in value:
            found.update(_find_forbidden_teamspace_legacy_keys(child))
    return found
