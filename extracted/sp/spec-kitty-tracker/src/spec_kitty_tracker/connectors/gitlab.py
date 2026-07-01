"""GitLab connector for spec-kitty-tracker.

For SaaS-backed operation, this connector is used through NangoProxyAdapter
with host-provided transport context via create_hosted_connector(). Direct
construction with static credentials is supported for test, migration, and
advanced use cases only.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import httpx

from spec_kitty_tracker.capabilities import TrackerCapabilities
from spec_kitty_tracker.connectors.base_http import HTTPConnectorBase
from spec_kitty_tracker.errors import ConnectorConfigError
from spec_kitty_tracker.mapping import parse_datetime
from spec_kitty_tracker.models import (
    CanonicalIssue,
    CanonicalIssueType,
    CanonicalLink,
    CanonicalStatus,
    ExternalRef,
    LinkType,
    Page,
    SyncCheckpoint,
    TrackerEvent,
)


@dataclass(frozen=True, slots=True)
class GitLabConnectorConfig:
    project_id: str
    token: str
    base_url: str = "https://gitlab.com/api/v4"


class GitLabConnector(HTTPConnectorBase):
    name = "gitlab"

    def __init__(
        self,
        config: GitLabConnectorConfig,
        *,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if not config.project_id.strip() or not config.token.strip():
            raise ConnectorConfigError("GitLab project_id and token are required")
        self.config = config
        super().__init__(
            base_url=config.base_url,
            headers={
                "PRIVATE-TOKEN": config.token,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            client=client,
        )

    async def get_capabilities(self) -> TrackerCapabilities:
        return TrackerCapabilities(
            supports_webhooks=True,
            supports_comments=True,
            supports_hierarchy=True,
            supports_dependencies=True,
            supports_custom_fields=True,
            supports_multi_assignee=True,
            supports_sprints_or_cycles=True,
            supports_bulk_read=True,
            supports_bulk_write=False,
            supports_delete=False,
        )

    async def list_issues(
        self,
        *,
        updated_since: datetime | None,
        cursor: str | None,
        limit: int,
        filters: Mapping[str, Any] | None,
    ) -> Page[CanonicalIssue]:
        page_num = int(cursor or "1")
        params: dict[str, Any] = {
            "state": "all",
            "per_page": min(limit, 100),
            "page": page_num,
        }
        if updated_since is not None:
            params["updated_after"] = updated_since.isoformat()
        if filters and "search" in filters:
            params["search"] = str(filters["search"])

        payload = await self._request(
            "GET",
            f"/projects/{self.config.project_id}/issues",
            params=params,
        )
        rows = payload.get("items", [])
        issues = [self._to_canonical(item) for item in rows if isinstance(item, Mapping)]
        next_cursor = str(page_num + 1) if len(rows) == min(limit, 100) else None
        return Page(items=issues, next_cursor=next_cursor)

    async def get_issue(self, ref: ExternalRef) -> CanonicalIssue:
        payload = await self._request(
            "GET",
            f"/projects/{self.config.project_id}/issues/{ref.id}",
        )
        return self._to_canonical(payload)

    async def create_issue(self, issue: CanonicalIssue) -> CanonicalIssue:
        payload = await self._request(
            "POST",
            f"/projects/{self.config.project_id}/issues",
            json_body={
                "title": issue.title,
                "description": issue.body,
                "labels": ",".join(issue.labels),
                "assignee_ids": self._assignee_ids(issue.assignees),
            },
        )
        return self._to_canonical(payload)

    async def update_issue(
        self,
        ref: ExternalRef,
        patch: Mapping[str, Any],
        *,
        idempotency_key: str | None,
    ) -> CanonicalIssue:
        del idempotency_key
        payload: dict[str, Any] = {}
        if "title" in patch:
            payload["title"] = patch["title"]
        if "body" in patch:
            payload["description"] = patch["body"]
        if "labels" in patch:
            payload["labels"] = ",".join(list(patch["labels"]))
        if "assignees" in patch:
            payload["assignee_ids"] = self._assignee_ids(list(patch["assignees"]))
        if "status" in patch:
            status = CanonicalStatus(str(patch["status"]))
            payload["state_event"] = "close" if status in {
                CanonicalStatus.DONE,
                CanonicalStatus.CANCELED,
            } else "reopen"

        if payload:
            updated = await self._request(
                "PUT",
                f"/projects/{self.config.project_id}/issues/{ref.id}",
                json_body=payload,
            )
            return self._to_canonical(updated)
        return await self.get_issue(ref)

    async def transition_issue(
        self,
        ref: ExternalRef,
        target_status: CanonicalStatus,
    ) -> CanonicalIssue:
        return await self.update_issue(
            ref,
            {"status": target_status},
            idempotency_key=f"transition:{ref.identity}:{target_status.value}",
        )

    async def upsert_link(self, ref: ExternalRef, link: CanonicalLink) -> None:
        await self._request(
            "POST",
            f"/projects/{self.config.project_id}/issues/{ref.id}/links",
            json_body={
                "target_project_id": self.config.project_id,
                "target_issue_iid": link.target.id,
                "link_type": self._gitlab_link_type(link.type),
            },
        )

    async def add_comment(self, ref: ExternalRef, body: str) -> None:
        await self._request(
            "POST",
            f"/projects/{self.config.project_id}/issues/{ref.id}/notes",
            json_body={"body": body},
        )

    async def list_events(
        self,
        cursor: SyncCheckpoint | None,
        limit: int,
    ) -> tuple[list[TrackerEvent], SyncCheckpoint | None]:
        del cursor, limit
        return [], None

    def _to_canonical(self, payload: Mapping[str, Any]) -> CanonicalIssue:
        labels = [str(label) for label in payload.get("labels", [])]
        issue_type = CanonicalIssueType.BUG if any(label.lower() == "bug" for label in labels) else CanonicalIssueType.TASK
        assignees = [
            str(assignee.get("username"))
            for assignee in payload.get("assignees", [])
            if assignee.get("username")
        ]

        return CanonicalIssue(
            ref=ExternalRef(
                system=self.name,
                workspace=self.config.project_id,
                id=str(payload.get("iid")),
                key=str(payload.get("iid")),
                url=str(payload.get("web_url") or ""),
            ),
            title=str(payload.get("title") or "Untitled"),
            body=str(payload["description"]) if payload.get("description") is not None else None,
            status=self._status_from_gitlab(payload.get("state")),
            issue_type=issue_type,
            priority=None,
            assignees=assignees,
            labels=labels,
            created_at=parse_datetime(payload.get("created_at")),
            updated_at=parse_datetime(payload.get("updated_at")),
            raw=dict(payload),
        )

    @staticmethod
    def _assignee_ids(values: list[str]) -> list[int]:
        ids: list[int] = []
        for value in values:
            try:
                ids.append(int(value))
            except ValueError:
                continue
        return ids

    @staticmethod
    def _status_from_gitlab(value: Any) -> CanonicalStatus:
        state = str(value or "").lower()
        if state == "closed":
            return CanonicalStatus.DONE
        return CanonicalStatus.TODO

    @staticmethod
    def _gitlab_link_type(link_type: LinkType) -> str:
        if link_type is LinkType.BLOCKS:
            return "blocks"
        if link_type is LinkType.BLOCKED_BY:
            return "is_blocked_by"
        return "relates_to"

