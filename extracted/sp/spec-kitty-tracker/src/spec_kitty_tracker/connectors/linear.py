"""Linear connector for spec-kitty-tracker.

For SaaS-backed operation, this connector is used through NangoProxyAdapter
with host-provided transport context via create_hosted_connector(). Direct
construction with static credentials is supported for test, migration, and
advanced use cases only.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import httpx

from spec_kitty_tracker.capabilities import TrackerCapabilities
from spec_kitty_tracker.connectors.base_http import HTTPConnectorBase
from spec_kitty_tracker.errors import (
    CapabilityNotSupportedError,
    ConnectorConfigError,
    ConnectorRequestError,
)
from spec_kitty_tracker.mapping import (
    canonical_to_linear_priority,
    linear_priority_to_canonical,
    parse_datetime,
)
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

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class LinearConnectorConfig:
    api_key: str
    team_id: str
    workspace: str = "linear"
    graphql_url: str = "https://api.linear.app/graphql"
    status_to_state_id: Mapping[CanonicalStatus, str] = field(default_factory=dict)


class LinearConnector(HTTPConnectorBase):
    name = "linear"

    def __init__(
        self,
        config: LinearConnectorConfig,
        *,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if not config.api_key.strip() or not config.team_id.strip():
            raise ConnectorConfigError("Linear api_key and team_id are required")
        self.config = config
        super().__init__(
            base_url=config.graphql_url,
            headers={
                "Authorization": config.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
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
        # Handle query_key via separate code path (T007)
        if filters and "query_key" in filters:
            return await self._search_by_key(str(filters["query_key"]))

        # Build filter expression for the issues() query
        filter_expr: dict[str, Any] = {"team": {"id": {"eq": self.config.team_id}}}
        if updated_since is not None:
            filter_expr["updatedAt"] = {"gte": updated_since.isoformat()}

        # Canonical query_text takes precedence over provider-specific title_contains
        if filters and "query_text" in filters:
            filter_expr["title"] = {"containsIgnoreCase": str(filters["query_text"])}
        elif filters and "title_contains" in filters:
            filter_expr["title"] = {"contains": str(filters["title_contains"])}

        query = """
        query ListIssues($first: Int!, $after: String, $filter: IssueFilter) {
          issues(first: $first, after: $after, filter: $filter) {
            nodes {
              id
              identifier
              title
              description
              priority
              createdAt
              updatedAt
              url
              state { id name type }
              labels { nodes { name } }
              assignee { id }
              parent { id identifier url }
            }
            pageInfo { hasNextPage endCursor }
          }
        }
        """

        data = await self._graphql(
            query,
            {
                "first": limit,
                "after": cursor,
                "filter": filter_expr,
            },
        )
        issues_payload = data["issues"]
        items = [self._to_canonical(node) for node in issues_payload["nodes"]]
        page_info = issues_payload["pageInfo"]
        next_cursor = str(page_info["endCursor"]) if page_info["hasNextPage"] else None
        return Page(items=items, next_cursor=next_cursor)

    async def get_issue(self, ref: ExternalRef) -> CanonicalIssue:
        query = """
        query GetIssue($id: String!) {
          issue(id: $id) {
            id
            identifier
            title
            description
            priority
            createdAt
            updatedAt
            url
            state { id name type }
            labels { nodes { name } }
            assignee { id }
            parent { id identifier url }
          }
        }
        """
        data = await self._graphql(query, {"id": ref.id})
        issue = data.get("issue")
        if issue is None:
            raise ConnectorRequestError(f"Linear issue not found: {ref.id}")
        return self._to_canonical(issue)

    async def _search_by_key(self, identifier: str) -> Page[CanonicalIssue]:
        """Look up a Linear issue by shorthand identifier with team validation."""
        query = """
        query GetIssue($id: String!) {
          issue(id: $id) {
            id
            identifier
            title
            description
            priority
            createdAt
            updatedAt
            url
            state { id name type }
            labels { nodes { name } }
            assignee { id }
            parent { id identifier url }
            team { id }
          }
        }
        """
        data = await self._graphql(query, {"id": identifier})

        issue = data.get("issue")
        if issue is None:
            return Page(items=[], next_cursor=None)

        if issue["team"]["id"] != self.config.team_id:
            return Page(items=[], next_cursor=None)

        return Page(items=[self._to_canonical(issue)], next_cursor=None)

    async def create_issue(self, issue: CanonicalIssue) -> CanonicalIssue:
        mutation = """
        mutation CreateIssue($input: IssueCreateInput!) {
          issueCreate(input: $input) {
            success
            issue { id }
          }
        }
        """
        payload: dict[str, Any] = {
            "teamId": self.config.team_id,
            "title": issue.title,
            "description": issue.body,
            "priority": canonical_to_linear_priority(issue.priority),
            "labelNames": issue.labels,
        }
        if issue.parent is not None:
            payload["parentId"] = issue.parent.id
        if issue.status in self.config.status_to_state_id:
            payload["stateId"] = self.config.status_to_state_id[issue.status]

        data = await self._graphql(mutation, {"input": payload})
        issue_id = str(data["issueCreate"]["issue"]["id"])
        return await self.get_issue(
            ExternalRef(system=self.name, workspace=self.config.workspace, id=issue_id)
        )

    async def update_issue(
        self,
        ref: ExternalRef,
        patch: Mapping[str, Any],
        *,
        idempotency_key: str | None,
    ) -> CanonicalIssue:
        del idempotency_key
        mutation = """
        mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
          issueUpdate(id: $id, input: $input) { success }
        }
        """
        input_payload: dict[str, Any] = {}

        if "title" in patch:
            input_payload["title"] = patch["title"]
        if "body" in patch:
            input_payload["description"] = patch["body"]
        if "labels" in patch:
            input_payload["labelNames"] = patch["labels"]
        if "priority" in patch:
            input_payload["priority"] = canonical_to_linear_priority(patch["priority"])
        if "parent" in patch and patch["parent"] is not None:
            input_payload["parentId"] = patch["parent"].id
        if "status" in patch:
            status = CanonicalStatus(str(patch["status"]))
            if status in self.config.status_to_state_id:
                input_payload["stateId"] = self.config.status_to_state_id[status]

        if "custom_fields" in patch:
            logger.warning(
                "Linear does not support custom field persistence; skipping spec_kitty_mission blob"
            )

        if input_payload:
            await self._graphql(mutation, {"id": ref.id, "input": input_payload})
        return await self.get_issue(ref)

    async def transition_issue(
        self,
        ref: ExternalRef,
        target_status: CanonicalStatus,
    ) -> CanonicalIssue:
        state_id = self.config.status_to_state_id.get(target_status)
        if state_id is None:
            raise CapabilityNotSupportedError(
                f"Linear status mapping missing for {target_status.value}. "
                "Provide status_to_state_id in LinearConnectorConfig."
            )
        return await self.update_issue(
            ref,
            {"status": target_status, "stateId": state_id},
            idempotency_key=f"transition:{ref.identity}:{target_status.value}",
        )

    async def upsert_link(self, ref: ExternalRef, link: CanonicalLink) -> None:
        relation_type = self._linear_relation_type(link.type)
        mutation = """
        mutation CreateIssueRelation($input: IssueRelationCreateInput!) {
          issueRelationCreate(input: $input) { success }
        }
        """
        await self._graphql(
            mutation,
            {
                "input": {
                    "issueId": ref.id,
                    "relatedIssueId": link.target.id,
                    "type": relation_type,
                }
            },
        )

    async def add_comment(self, ref: ExternalRef, body: str) -> None:
        mutation = """
        mutation CreateComment($input: CommentCreateInput!) {
          commentCreate(input: $input) { success }
        }
        """
        await self._graphql(
            mutation,
            {"input": {"issueId": ref.id, "body": body}},
        )

    async def list_events(
        self,
        cursor: SyncCheckpoint | None,
        limit: int,
    ) -> tuple[list[TrackerEvent], SyncCheckpoint | None]:
        del cursor, limit
        return [], None

    async def _graphql(self, query: str, variables: Mapping[str, Any]) -> dict[str, Any]:
        payload = await self._request(
            "POST",
            self.config.graphql_url,
            json_body={"query": query, "variables": dict(variables)},
        )
        if "errors" in payload:
            raise ConnectorRequestError(f"Linear GraphQL error: {payload['errors']}")
        return dict(payload["data"])

    def _to_canonical(self, payload: Mapping[str, Any]) -> CanonicalIssue:
        state = payload.get("state", {})
        status = self._status_from_linear_state(state)
        labels = [str(node["name"]) for node in payload.get("labels", {}).get("nodes", [])]
        assignee = payload.get("assignee")
        assignees = (
            [str(assignee["id"])] if isinstance(assignee, Mapping) and assignee.get("id") else []
        )

        parent_payload = payload.get("parent")
        parent = None
        if isinstance(parent_payload, Mapping) and parent_payload.get("id"):
            parent = ExternalRef(
                system=self.name,
                workspace=self.config.workspace,
                id=str(parent_payload["id"]),
                key=str(parent_payload.get("identifier") or "") or None,
                url=str(parent_payload.get("url") or "") or None,
            )

        return CanonicalIssue(
            ref=ExternalRef(
                system=self.name,
                workspace=self.config.workspace,
                id=str(payload["id"]),
                key=str(payload.get("identifier") or "") or None,
                url=str(payload.get("url") or "") or None,
            ),
            title=str(payload.get("title") or "Untitled"),
            body=str(payload["description"]) if payload.get("description") is not None else None,
            status=status,
            issue_type=CanonicalIssueType.TASK,
            priority=linear_priority_to_canonical(payload.get("priority")),
            assignees=assignees,
            labels=labels,
            parent=parent,
            created_at=parse_datetime(payload.get("createdAt")),
            updated_at=parse_datetime(payload.get("updatedAt")),
            raw=dict(payload),
        )

    @staticmethod
    def _status_from_linear_state(state: Any) -> CanonicalStatus:
        if not isinstance(state, Mapping):
            return CanonicalStatus.TODO

        state_type = str(state.get("type", "")).lower()
        state_name = str(state.get("name", "")).lower()

        if state_type in {"completed"}:
            return CanonicalStatus.DONE
        if state_type in {"canceled"}:
            return CanonicalStatus.CANCELED
        if state_type in {"started"}:
            if "review" in state_name:
                return CanonicalStatus.IN_REVIEW
            if "block" in state_name or "hold" in state_name:
                return CanonicalStatus.BLOCKED
            return CanonicalStatus.IN_PROGRESS
        if state_type in {"backlog", "unstarted"}:
            return CanonicalStatus.TODO

        if "review" in state_name:
            return CanonicalStatus.IN_REVIEW
        if "block" in state_name or "hold" in state_name:
            return CanonicalStatus.BLOCKED
        return CanonicalStatus.TODO

    @staticmethod
    def _linear_relation_type(link_type: LinkType) -> str:
        if link_type in {LinkType.BLOCKS, LinkType.BLOCKED_BY}:
            return "blocks"
        if link_type is LinkType.DUPLICATES:
            return "duplicate"
        return "related"
