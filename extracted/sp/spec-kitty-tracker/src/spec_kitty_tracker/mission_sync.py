from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from spec_kitty_tracker.errors import ConnectorRequestError
from spec_kitty_tracker.models import (
    CanonicalIssue,
    CanonicalLink,
    CanonicalStatus,
    ExternalRef,
    LinkType,
    utcnow,
)
from spec_kitty_tracker.protocols import TaskTrackerConnector


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
    if not isinstance(raw, list):
        return []

    parsed: list[DecisionReference] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        decision_id = str(item.get("decision_id", "")).strip()
        if not decision_id:
            continue
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
            except ValueError:
                external_ref = None
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
        custom_fields["spec_kitty_mission"] = {
            "mission_id": update.mission_id,
            "mission_state": update.mission_state,
            "mission_url": update.mission_url,
            "updated_at": utcnow().isoformat(),
            "decision_refs": [ref.as_dict() for ref in update.decision_references],
        }
        patch["custom_fields"] = custom_fields

        idempotency_key = f"mission-update:{update.mission_id}:{issue_ref.identity}"
        updated = await self._update_issue_with_retry(
            ref=issue_ref,
            patch=patch,
            idempotency_key=idempotency_key,
        )

        for decision_ref in update.decision_references:
            if decision_ref.blocking and decision_ref.external_ref is not None:
                await self.connector.upsert_link(
                    issue_ref,
                    CanonicalLink(type=LinkType.BLOCKED_BY, target=decision_ref.external_ref),
                )

        capabilities = await self.connector.get_capabilities()
        if capabilities.supports_comments:
            await self.connector.add_comment(issue_ref, _render_mission_comment(update))

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
        Line 4 (optional): ``Mission: <mission_url>``     — omitted when mission_url is empty or None
        Line 5 (optional): ``Decision refs: <id>, ...``   — omitted when no decision references

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
