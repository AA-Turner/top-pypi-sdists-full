from __future__ import annotations

import base64
from collections.abc import Mapping
from dataclasses import dataclass, field
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
class AzureDevOpsConnectorConfig:
    organization: str
    project: str
    personal_access_token: str
    base_url: str = "https://dev.azure.com"
    status_map: Mapping[CanonicalStatus, str] = field(default_factory=dict)


class AzureDevOpsConnector(HTTPConnectorBase):
    name = "azure_devops"

    def __init__(
        self,
        config: AzureDevOpsConnectorConfig,
        *,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if not config.organization.strip() or not config.project.strip():
            raise ConnectorConfigError("Azure organization and project are required")
        self.config = config
        token = base64.b64encode(f":{config.personal_access_token}".encode()).decode()
        headers = {
            "Authorization": f"Basic {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        super().__init__(
            base_url=f"{config.base_url.rstrip('/')}/{config.organization}",
            headers=headers,
            client=client,
        )

    async def get_capabilities(self) -> TrackerCapabilities:
        return TrackerCapabilities(
            supports_webhooks=True,
            supports_comments=False,
            supports_hierarchy=True,
            supports_dependencies=True,
            supports_custom_fields=True,
            supports_multi_assignee=False,
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
        del cursor, filters
        work_item_ids = await self._query_work_item_ids(updated_since=updated_since, top=limit)
        if not work_item_ids:
            return Page(items=[], next_cursor=None)

        work_items = await self._get_work_items(work_item_ids)
        issues = [self._to_canonical(item) for item in work_items]
        return Page(items=issues, next_cursor=None)

    async def get_issue(self, ref: ExternalRef) -> CanonicalIssue:
        payload = await self._request(
            "GET",
            f"/{self.config.project}/_apis/wit/workitems/{ref.id}",
            params={"api-version": "7.1"},
        )
        return self._to_canonical(payload)

    async def create_issue(self, issue: CanonicalIssue) -> CanonicalIssue:
        work_item_type = self._to_ado_type(issue.issue_type)
        operations: list[dict[str, Any]] = [
            {"op": "add", "path": "/fields/System.Title", "value": issue.title},
        ]
        if issue.body:
            operations.append(
                {"op": "add", "path": "/fields/System.Description", "value": issue.body}
            )
        if issue.priority is not None:
            operations.append(
                {
                    "op": "add",
                    "path": "/fields/Microsoft.VSTS.Common.Priority",
                    "value": issue.priority,
                }
            )
        if issue.labels:
            operations.append(
                {
                    "op": "add",
                    "path": "/fields/System.Tags",
                    "value": "; ".join(issue.labels),
                }
            )

        payload = await self._request(
            "POST",
            f"/{self.config.project}/_apis/wit/workitems/${work_item_type}",
            params={"api-version": "7.1"},
            headers={"Content-Type": "application/json-patch+json"},
            json_body=operations,
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
        operations: list[dict[str, Any]] = []
        if "title" in patch:
            operations.append(
                {"op": "add", "path": "/fields/System.Title", "value": patch["title"]}
            )
        if "body" in patch:
            operations.append(
                {"op": "add", "path": "/fields/System.Description", "value": patch["body"]}
            )
        if "priority" in patch and patch["priority"] is not None:
            operations.append(
                {
                    "op": "add",
                    "path": "/fields/Microsoft.VSTS.Common.Priority",
                    "value": patch["priority"],
                }
            )
        if "labels" in patch:
            operations.append(
                {
                    "op": "add",
                    "path": "/fields/System.Tags",
                    "value": "; ".join(list(patch["labels"])),
                }
            )
        if "status" in patch:
            status = CanonicalStatus(str(patch["status"]))
            operations.append(
                {
                    "op": "add",
                    "path": "/fields/System.State",
                    "value": self._to_ado_state(status),
                }
            )

        if operations:
            await self._request(
                "PATCH",
                f"/{self.config.project}/_apis/wit/workitems/{ref.id}",
                params={"api-version": "7.1"},
                headers={"Content-Type": "application/json-patch+json"},
                json_body=operations,
            )

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
        target_url = (
            f"{self.config.base_url.rstrip('/')}/{self.config.organization}"
            f"/_apis/wit/workItems/{link.target.id}"
        )
        relation = {
            "rel": self._ado_relation_type(link.type),
            "url": target_url,
        }
        await self._request(
            "PATCH",
            f"/{self.config.project}/_apis/wit/workitems/{ref.id}",
            params={"api-version": "7.1"},
            headers={"Content-Type": "application/json-patch+json"},
            json_body=[{"op": "add", "path": "/relations/-", "value": relation}],
        )

    async def add_comment(self, ref: ExternalRef, body: str) -> None:
        del ref, body
        raise ConnectorConfigError(
            "AzureDevOpsConnector.add_comment is not enabled in v0.1.0. "
            "Set supports_comments=False and write comments through extension APIs if needed."
        )

    async def list_events(
        self,
        cursor: SyncCheckpoint | None,
        limit: int,
    ) -> tuple[list[TrackerEvent], SyncCheckpoint | None]:
        del cursor, limit
        return [], None

    async def _query_work_item_ids(
        self,
        *,
        updated_since: datetime | None,
        top: int,
    ) -> list[int]:
        where_clause = f"[System.TeamProject] = '{self.config.project}'"
        if updated_since is not None:
            where_clause += (
                " AND [System.ChangedDate] >= '"
                + updated_since.strftime("%Y-%m-%dT%H:%M:%SZ")
                + "'"
            )

        wiql = (
            "SELECT [System.Id] FROM WorkItems "
            f"WHERE {where_clause} "
            "ORDER BY [System.ChangedDate] DESC"
        )

        payload = await self._request(
            "POST",
            f"/{self.config.project}/_apis/wit/wiql",
            params={"api-version": "7.1"},
            json_body={"query": wiql, "$top": top},
        )
        return [int(item["id"]) for item in payload.get("workItems", [])]

    async def _get_work_items(self, ids: list[int]) -> list[dict[str, Any]]:
        payload = await self._request(
            "POST",
            f"/{self.config.project}/_apis/wit/workitemsbatch",
            params={"api-version": "7.1"},
            json_body={
                "ids": ids,
                "fields": [
                    "System.Id",
                    "System.Title",
                    "System.Description",
                    "System.State",
                    "System.WorkItemType",
                    "System.AssignedTo",
                    "System.Tags",
                    "System.CreatedDate",
                    "System.ChangedDate",
                    "Microsoft.VSTS.Common.Priority",
                ],
                "$expand": "relations",
            },
        )
        return list(payload.get("value", []))

    def _to_canonical(self, item: Mapping[str, Any]) -> CanonicalIssue:
        fields = item.get("fields", {})
        tags = fields.get("System.Tags")
        labels = [tag.strip() for tag in str(tags).split(";") if tag.strip()] if tags else []

        assignee = fields.get("System.AssignedTo")
        assignees: list[str] = []
        if isinstance(assignee, Mapping):
            display_name = assignee.get("displayName")
            if display_name:
                assignees = [str(display_name)]
        elif isinstance(assignee, str) and assignee:
            assignees = [assignee]

        parent = self._extract_parent(item.get("relations", []))

        return CanonicalIssue(
            ref=ExternalRef(
                system=self.name,
                workspace=f"{self.config.organization}/{self.config.project}",
                id=str(fields.get("System.Id") or item.get("id")),
                key=str(fields.get("System.Id") or item.get("id")),
                url=str(item.get("url") or ""),
            ),
            title=str(fields.get("System.Title") or "Untitled"),
            body=str(fields.get("System.Description"))
            if fields.get("System.Description")
            else None,
            status=self._status_from_ado_state(fields.get("System.State")),
            issue_type=self._issue_type_from_ado(fields.get("System.WorkItemType")),
            priority=self._parse_priority(fields.get("Microsoft.VSTS.Common.Priority")),
            assignees=assignees,
            labels=labels,
            parent=parent,
            created_at=parse_datetime(fields.get("System.CreatedDate")),
            updated_at=parse_datetime(fields.get("System.ChangedDate")),
            raw=dict(item),
        )

    def _extract_parent(self, relations: Any) -> ExternalRef | None:
        if not isinstance(relations, list):
            return None
        for relation in relations:
            if relation.get("rel") != "System.LinkTypes.Hierarchy-Reverse":
                continue
            url = str(relation.get("url", ""))
            issue_id = url.rsplit("/", 1)[-1]
            if issue_id:
                return ExternalRef(
                    system=self.name,
                    workspace=f"{self.config.organization}/{self.config.project}",
                    id=issue_id,
                    key=issue_id,
                    url=url,
                )
        return None

    @staticmethod
    def _parse_priority(value: Any) -> int | None:
        if isinstance(value, int):
            return min(max(value, 0), 4)
        try:
            parsed = int(str(value))
            return min(max(parsed, 0), 4)
        except ValueError:
            return None

    @staticmethod
    def _status_from_ado_state(value: Any) -> CanonicalStatus:
        state = str(value or "").lower()
        if state in {"done", "closed", "resolved"}:
            return CanonicalStatus.DONE
        if state in {"in progress", "active", "committed"}:
            return CanonicalStatus.IN_PROGRESS
        if state in {"blocked", "on hold"}:
            return CanonicalStatus.BLOCKED
        if state in {"review", "in review"}:
            return CanonicalStatus.IN_REVIEW
        if state in {"removed", "canceled", "cancelled"}:
            return CanonicalStatus.CANCELED
        return CanonicalStatus.TODO

    def _to_ado_state(self, status: CanonicalStatus) -> str:
        if status in self.config.status_map:
            return self.config.status_map[status]
        mapping = {
            CanonicalStatus.TODO: "New",
            CanonicalStatus.IN_PROGRESS: "Active",
            CanonicalStatus.IN_REVIEW: "Resolved",
            CanonicalStatus.BLOCKED: "Active",
            CanonicalStatus.DONE: "Closed",
            CanonicalStatus.CANCELED: "Removed",
        }
        return mapping[status]

    @staticmethod
    def _issue_type_from_ado(value: Any) -> CanonicalIssueType:
        name = str(value or "").lower()
        if name in {"epic", "feature", "initiative"}:
            return CanonicalIssueType.EPIC
        if name in {"user story", "story"}:
            return CanonicalIssueType.STORY
        if name in {"bug", "defect"}:
            return CanonicalIssueType.BUG
        if name in {"task"}:
            return CanonicalIssueType.TASK
        return CanonicalIssueType.CHORE

    @staticmethod
    def _to_ado_type(issue_type: CanonicalIssueType) -> str:
        mapping = {
            CanonicalIssueType.EPIC: "Epic",
            CanonicalIssueType.STORY: "User Story",
            CanonicalIssueType.TASK: "Task",
            CanonicalIssueType.BUG: "Bug",
            CanonicalIssueType.CHORE: "Task",
            CanonicalIssueType.SUBTASK: "Task",
        }
        return mapping[issue_type]

    @staticmethod
    def _ado_relation_type(link_type: LinkType) -> str:
        if link_type is LinkType.BLOCKS:
            return "System.LinkTypes.Dependency-Forward"
        if link_type is LinkType.BLOCKED_BY:
            return "System.LinkTypes.Dependency-Reverse"
        if link_type is LinkType.PARENT_OF:
            return "System.LinkTypes.Hierarchy-Forward"
        if link_type is LinkType.CHILD_OF:
            return "System.LinkTypes.Hierarchy-Reverse"
        return "System.LinkTypes.Related"
