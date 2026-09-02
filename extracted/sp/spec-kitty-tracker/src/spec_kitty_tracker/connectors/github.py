"""GitHub connector for spec-kitty-tracker.

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
from spec_kitty_tracker.errors import CapabilityNotSupportedError, ConnectorConfigError
from spec_kitty_tracker.mapping import (
    github_state_to_status,
    parse_datetime,
    status_to_github_state,
)
from spec_kitty_tracker.models import (
    CanonicalIssue,
    CanonicalIssueType,
    CanonicalLink,
    CanonicalStatus,
    ExternalRef,
    Page,
    SyncCheckpoint,
    TrackerEvent,
    TrackerEventType,
    utcnow,
)


@dataclass(frozen=True, slots=True)
class GitHubConnectorConfig:
    owner: str
    repo: str
    token: str
    base_url: str = "https://api.github.com"


class GitHubConnector(HTTPConnectorBase):
    name = "github"

    def __init__(
        self,
        config: GitHubConnectorConfig,
        *,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if not config.owner.strip() or not config.repo.strip() or not config.token.strip():
            raise ConnectorConfigError("GitHub owner, repo, and token are required")
        self.config = config
        headers = {
            "Authorization": f"Bearer {config.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        super().__init__(base_url=config.base_url, headers=headers, client=client)

    async def get_capabilities(self) -> TrackerCapabilities:
        return TrackerCapabilities(
            supports_webhooks=True,
            supports_comments=True,
            supports_hierarchy=False,
            supports_dependencies=False,
            supports_custom_fields=False,
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
            params["since"] = updated_since.isoformat()
        if filters and "labels" in filters:
            params["labels"] = ",".join(filters["labels"])

        payload = await self._request(
            "GET",
            f"/repos/{self.config.owner}/{self.config.repo}/issues",
            params=params,
        )
        rows = payload.get("items", [])
        issues = [
            self._to_canonical(item)
            for item in rows
            if isinstance(item, Mapping) and "pull_request" not in item
        ]
        next_cursor = str(page_num + 1) if len(rows) == min(limit, 100) else None
        return Page(items=issues, next_cursor=next_cursor)

    async def get_issue(self, ref: ExternalRef) -> CanonicalIssue:
        payload = await self._request(
            "GET",
            f"/repos/{self.config.owner}/{self.config.repo}/issues/{ref.id}",
        )
        return self._to_canonical(payload)

    async def create_issue(self, issue: CanonicalIssue) -> CanonicalIssue:
        payload = await self._request(
            "POST",
            f"/repos/{self.config.owner}/{self.config.repo}/issues",
            json_body={
                "title": issue.title,
                "body": issue.body,
                "labels": issue.labels,
                "assignees": issue.assignees,
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
            payload["body"] = patch["body"]
        if "labels" in patch:
            payload["labels"] = list(patch["labels"])
        if "assignees" in patch:
            payload["assignees"] = list(patch["assignees"])
        if "status" in patch:
            payload["state"] = status_to_github_state(CanonicalStatus(str(patch["status"])))

        if payload:
            updated = await self._request(
                "PATCH",
                f"/repos/{self.config.owner}/{self.config.repo}/issues/{ref.id}",
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
        del ref, link
        raise CapabilityNotSupportedError(
            "GitHub dependency/link upsert is not enabled in v0.1.0 connector implementation"
        )

    async def add_comment(self, ref: ExternalRef, body: str) -> None:
        await self._request(
            "POST",
            f"/repos/{self.config.owner}/{self.config.repo}/issues/{ref.id}/comments",
            json_body={"body": body},
        )

    async def list_events(
        self,
        cursor: SyncCheckpoint | None,
        limit: int,
    ) -> tuple[list[TrackerEvent], SyncCheckpoint | None]:
        page_num = int(cursor.cursor) if cursor and cursor.cursor else 1
        payload = await self._request(
            "GET",
            f"/repos/{self.config.owner}/{self.config.repo}/issues/events",
            params={"per_page": min(limit, 100), "page": page_num},
        )

        events: list[TrackerEvent] = []
        for item in payload.get("items", []):
            issue = item.get("issue", {})
            issue_number = issue.get("number")
            if issue_number is None:
                continue
            ref = ExternalRef(
                system=self.name,
                workspace=f"{self.config.owner}/{self.config.repo}",
                id=str(issue_number),
                key=f"#{issue_number}",
                url=issue.get("html_url"),
            )
            events.append(
                TrackerEvent(
                    event_id=str(item.get("id")),
                    event_type=TrackerEventType.UPDATED,
                    issue_ref=ref,
                    timestamp=parse_datetime(item.get("created_at")) or utcnow(),
                    payload=dict(item),
                )
            )

        next_cursor = (
            str(page_num + 1) if len(payload.get("items", [])) == min(limit, 100) else None
        )
        return events, SyncCheckpoint(cursor=next_cursor)

    def _to_canonical(self, payload: Mapping[str, Any]) -> CanonicalIssue:
        labels = [str(item.get("name")) for item in payload.get("labels", []) if item.get("name")]
        issue_type = (
            CanonicalIssueType.BUG
            if any(label.lower() == "bug" for label in labels)
            else CanonicalIssueType.TASK
        )

        return CanonicalIssue(
            ref=ExternalRef(
                system=self.name,
                workspace=f"{self.config.owner}/{self.config.repo}",
                id=str(payload["number"]),
                key=f"#{payload['number']}",
                url=str(payload.get("html_url") or ""),
            ),
            title=str(payload.get("title") or "Untitled"),
            body=str(payload["body"]) if payload.get("body") is not None else None,
            status=github_state_to_status(str(payload.get("state", "open"))),
            issue_type=issue_type,
            priority=None,
            assignees=[
                str(assignee.get("login"))
                for assignee in payload.get("assignees", [])
                if assignee.get("login")
            ],
            labels=labels,
            created_at=parse_datetime(payload.get("created_at")),
            updated_at=parse_datetime(payload.get("updated_at")),
            raw=dict(payload),
        )
