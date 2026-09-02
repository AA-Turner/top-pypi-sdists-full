"""Jira connector for spec-kitty-tracker.

For SaaS-backed operation, this connector is used through NangoProxyAdapter
with host-provided transport context via create_hosted_connector(). Direct
construction with static credentials is supported for test, migration, and
advanced use cases only.
"""

from __future__ import annotations

import base64
import json
import logging
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import httpx

from spec_kitty_tracker.capabilities import TrackerCapabilities
from spec_kitty_tracker.connectors.base_http import HTTPConnectorBase
from spec_kitty_tracker.errors import (
    STATUS_TRANSITION_CAPABILITY,
    CapabilityNotSupportedError,
    ConnectorConfigError,
)
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

logger = logging.getLogger(__name__)

_ISSUE_FIELDS = (
    "summary,description,status,priority,assignee,labels,issuetype,parent,updated,created"
)


@dataclass(frozen=True, slots=True)
class JiraConnectorConfig:
    base_url: str
    email: str
    api_token: str
    project_key: str
    default_issue_type: str = "Task"
    status_name_map: Mapping[CanonicalStatus, str] = field(default_factory=dict)
    spec_kitty_mission_field_id: str | None = None


@dataclass(frozen=True, slots=True)
class JiraTransition:
    """A single available Jira workflow transition, as returned by the
    transitions API. Read-only: carries no ticket-mutating capability.
    """

    id: str
    name: str


class JiraConnector(HTTPConnectorBase):
    name = "jira"

    def __init__(
        self,
        config: JiraConnectorConfig,
        *,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if not config.base_url.strip() or not config.project_key.strip():
            raise ConnectorConfigError("Jira base_url and project_key are required")
        self.config = config
        auth = base64.b64encode(f"{config.email}:{config.api_token}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        super().__init__(base_url=config.base_url, headers=headers, client=client)

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
        # Canonical filter key resolution (query_key > query_text > jql > project default)
        jql: str
        if filters and "query_key" in filters:
            escaped = str(filters["query_key"]).replace('"', '\\"')
            jql = f'key = "{escaped}"'
        elif filters and "query_text" in filters:
            escaped = str(filters["query_text"]).replace('"', '\\"')
            jql = f'project = {self.config.project_key} AND text ~ "{escaped}"'
        elif filters and "jql" in filters:
            jql = str(filters["jql"])
        else:
            jql = f"project = {self.config.project_key}"
        if updated_since is not None:
            stamp = updated_since.strftime("%Y-%m-%d %H:%M")
            jql = f'{jql} AND updated >= "{stamp}"'

        params: dict[str, Any] = {
            "jql": jql,
            "maxResults": limit,
            "fields": _ISSUE_FIELDS,
        }
        if cursor and cursor != "0":
            params["nextPageToken"] = cursor

        payload = await self._request(
            "GET",
            "/rest/api/3/search/jql",
            params=params,
        )

        issues = [self._to_canonical(item) for item in payload.get("issues", [])]
        next_cursor = payload.get("nextPageToken")
        if next_cursor is not None:
            next_cursor = str(next_cursor)
        return Page(items=issues, next_cursor=next_cursor)

    async def get_issue(self, ref: ExternalRef) -> CanonicalIssue:
        issue_key = ref.key or ref.id
        payload = await self._request(
            "GET",
            f"/rest/api/3/issue/{issue_key}",
            params={
                "fields": _ISSUE_FIELDS,
            },
        )
        return self._to_canonical(payload)

    async def create_issue(self, issue: CanonicalIssue) -> CanonicalIssue:
        body = {
            "fields": {
                "project": {"key": self.config.project_key},
                "summary": issue.title,
                "description": self._to_jira_description(issue.body),
                "issuetype": {"name": self._to_jira_issue_type(issue.issue_type)},
                "labels": issue.labels,
            }
        }
        if issue.priority is not None:
            body["fields"]["priority"] = {"name": self._priority_to_name(issue.priority)}

        created = await self._request("POST", "/rest/api/3/issue", json_body=body)
        created_ref = ExternalRef(
            system=self.name,
            workspace=self.config.base_url,
            id=str(created["id"]),
            key=str(created["key"]),
            url=f"{self.config.base_url}/browse/{created['key']}",
        )
        return await self.get_issue(created_ref)

    async def update_issue(
        self,
        ref: ExternalRef,
        patch: Mapping[str, Any],
        *,
        idempotency_key: str | None,
    ) -> CanonicalIssue:
        """Apply ``patch`` to the Jira issue at ``ref``.

        Write ordering (D4): all non-status fields (``title``, ``body``,
        ``labels``, ``priority``, and the ``custom_fields`` →
        ``spec_kitty_mission_field_id`` blob) are collected and PUT to Jira
        **first**. Only after that PUT lands does a ``status`` entry in
        ``patch`` get attempted via :meth:`transition_issue`, **last**. This
        means a status-transition refusal (``CapabilityNotSupportedError``)
        never silently drops the other field writes bundled in the same
        patch — the non-status fields have already persisted by the time the
        transition is attempted.
        """
        del idempotency_key
        issue_key = ref.key or ref.id
        fields: dict[str, Any] = {}

        if "title" in patch:
            fields["summary"] = patch["title"]
        if "body" in patch:
            fields["description"] = self._to_jira_description(patch["body"])
        if "labels" in patch:
            fields["labels"] = patch["labels"]
        if "priority" in patch and patch["priority"] is not None:
            fields["priority"] = {"name": self._priority_to_name(int(patch["priority"]))}

        if "custom_fields" in patch and self.config.spec_kitty_mission_field_id:
            blob = patch["custom_fields"]
            if isinstance(blob, dict) and "spec_kitty_mission" in blob:
                fields[self.config.spec_kitty_mission_field_id] = json.dumps(
                    blob["spec_kitty_mission"]
                )
        elif "custom_fields" in patch:
            logger.warning(
                "Jira custom field persistence skipped: spec_kitty_mission_field_id not configured"
            )

        if fields:
            await self._request(
                "PUT", f"/rest/api/3/issue/{issue_key}", json_body={"fields": fields}
            )

        if "status" in patch:
            await self.transition_issue(ref, CanonicalStatus(str(patch["status"])))

        return await self.get_issue(ref)

    async def transition_issue(
        self,
        ref: ExternalRef,
        target_status: CanonicalStatus,
    ) -> CanonicalIssue:
        """Move the Jira issue at ``ref`` to ``target_status``.

        Decision order (never guesses):

        1. **Idempotent no-op** — fetch the current issue and compare its
           **raw** Jira status name (``issue.raw["fields"]["status"]["name"]``,
           lowercased) against the resolved desired name. If they match,
           return the issue unchanged: no GET-transitions call, no POST, no
           raise. This intentionally does **not** use the lossy canonical
           :meth:`_status_from_jira` mapping, which defaults any unrecognized
           Jira status name to ``CanonicalStatus.TODO`` — using it here would
           cause a silent false no-op whenever ``target_status`` is ``TODO``
           and the ticket sits in an unrecognized custom status (e.g.
           "Triage"). It also makes a retried transition call, issued after
           the transition already succeeded server-side, resolve as a
           successful no-op rather than a false refusal.
        2. **Match** — GET the available transitions and look for one whose
           **destination status** (``transition["to"]["name"]``,
           case-insensitive) equals the resolved desired name. Destination
           status is matched first because ``desired_name`` is a *status*
           name by construction: :meth:`_status_to_jira_name` yields "To Do",
           "In Progress", "Done" and so on, and step 1 above compares it
           against the ticket's raw *status* name. A transition's own
           ``name`` is a different namespace — team-managed Jira projects
           name transitions after their destination status, but a
           company-managed project on a classic workflow names them for the
           action ("Start Progress", "Resolve Issue"), where no transition
           name ever equals a status name.

           A transition whose own ``name`` equals the desired name is kept as
           a **fallback** and used only when no destination status matched,
           so an operator who has populated ``status_name_map`` with
           transition names keeps working. On the first match, POST that
           transition's id and return the refreshed issue. When several
           available transitions match at the same precedence, the first one
           Jira returned is chosen, deterministically.
        3. **Refuse** — otherwise raise :class:`CapabilityNotSupportedError`
           tagged with ``capability=STATUS_TRANSITION_CAPABILITY`` so callers
           can distinguish a status-transition refusal from any other
           capability gap. The message names the requested canonical status,
           the resolved desired status name, and the transitions actually
           available on the ticket rendered as ``name -> destination`` so an
           operator can see both namespaces at once. This method never
           guesses by POSTing an unmatched transition.
        """
        issue_key = ref.key or ref.id
        desired_name = self.config.status_name_map.get(
            target_status,
            self._status_to_jira_name(target_status),
        ).lower()

        current_issue = await self.get_issue(ref)
        raw = current_issue.raw or {}
        raw_fields = raw.get("fields")
        if not isinstance(raw_fields, Mapping):
            raw_fields = {}
        raw_status = raw_fields.get("status")
        current_raw_name = (
            str(raw_status.get("name", "")).lower() if isinstance(raw_status, Mapping) else ""
        )
        if current_raw_name == desired_name:
            return current_issue

        transitions = await self._request("GET", f"/rest/api/3/issue/{issue_key}/transitions")
        raw_available = transitions.get("transitions")
        available = raw_available if isinstance(raw_available, list) else []

        chosen: str | None = None
        name_fallback: str | None = None
        available_names: list[str] = []
        for transition in available:
            if not isinstance(transition, Mapping):
                continue
            name = str(transition.get("name", ""))
            raw_to = transition.get("to")
            to_name = str(raw_to.get("name", "")) if isinstance(raw_to, Mapping) else ""
            available_names.append(f"{name} -> {to_name}" if to_name else name)
            tid = transition.get("id")
            if tid is None:
                continue
            if chosen is None and to_name.lower() == desired_name:
                chosen = str(tid)
            elif name_fallback is None and name.lower() == desired_name:
                name_fallback = str(tid)

        if chosen is None:
            chosen = name_fallback

        if chosen is None:
            raise CapabilityNotSupportedError(
                f"No Jira transition matches status '{target_status.value}' "
                f"(resolved desired name '{desired_name}'); "
                f"available transitions (name -> destination): {available_names}",
                capability=STATUS_TRANSITION_CAPABILITY,
            )

        await self._request(
            "POST",
            f"/rest/api/3/issue/{issue_key}/transitions",
            json_body={"transition": {"id": chosen}},
        )
        return await self.get_issue(ref)

    async def list_transitions(self, ref: ExternalRef) -> list[JiraTransition]:
        """Return the Jira workflow transitions currently available on the
        issue at ``ref``.

        Read-only: issues a single GET, never mutates ticket state. Returns
        ``[]`` when the ticket offers no transitions.
        """
        issue_key = ref.key or ref.id
        payload = await self._request("GET", f"/rest/api/3/issue/{issue_key}/transitions")
        raw_transitions = payload.get("transitions")
        if not isinstance(raw_transitions, list):
            raw_transitions = []
        result: list[JiraTransition] = []
        for t in raw_transitions:
            if not isinstance(t, Mapping):
                continue
            tid = t.get("id")
            if tid is None:
                continue
            result.append(JiraTransition(id=str(tid), name=str(t.get("name", ""))))
        return result

    async def upsert_link(self, ref: ExternalRef, link: CanonicalLink) -> None:
        issue_key = ref.key or ref.id
        target_key = link.target.key or link.target.id
        link_name = self._link_type_to_jira(link.type)
        await self._request(
            "POST",
            "/rest/api/3/issueLink",
            json_body={
                "type": {"name": link_name},
                "inwardIssue": {"key": issue_key},
                "outwardIssue": {"key": target_key},
            },
        )

    async def add_comment(self, ref: ExternalRef, body: str) -> None:
        issue_key = ref.key or ref.id
        await self._request(
            "POST",
            f"/rest/api/3/issue/{issue_key}/comment",
            json_body={"body": self._to_jira_description(body)},
        )

    async def list_events(
        self,
        cursor: SyncCheckpoint | None,
        limit: int,
    ) -> tuple[list[TrackerEvent], SyncCheckpoint | None]:
        del cursor, limit
        return [], None

    def _to_canonical(self, issue: Mapping[str, Any]) -> CanonicalIssue:
        fields = issue.get("fields") or {}
        assignee = fields.get("assignee")
        assignees = (
            [assignee["accountId"]]
            if isinstance(assignee, Mapping) and assignee.get("accountId")
            else []
        )

        parent = fields.get("parent")
        parent_ref = None
        if isinstance(parent, Mapping):
            parent_ref = ExternalRef(
                system=self.name,
                workspace=self.config.base_url,
                id=str(parent.get("id", "")),
                key=str(parent.get("key", "")) or None,
                url=f"{self.config.base_url}/browse/{parent.get('key')}",
            )

        return CanonicalIssue(
            ref=ExternalRef(
                system=self.name,
                workspace=self.config.base_url,
                id=str(issue.get("id", "")),
                key=str(issue.get("key", "")) or None,
                url=f"{self.config.base_url}/browse/{issue.get('key')}",
            ),
            title=str(fields.get("summary", "Untitled")),
            body=self._from_jira_description(fields.get("description")),
            status=self._status_from_jira(fields.get("status", {})),
            issue_type=self._issue_type_from_jira(fields.get("issuetype", {})),
            priority=self._priority_from_name((fields.get("priority") or {}).get("name")),
            assignees=assignees,
            labels=list(fields.get("labels") or []),
            parent=parent_ref,
            created_at=parse_datetime(fields.get("created")),
            updated_at=parse_datetime(fields.get("updated")),
            raw=dict(issue),
        )

    @staticmethod
    def _to_jira_description(text: Any) -> dict[str, Any]:
        content = "" if text is None else str(text)
        return {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": content}],
                }
            ],
        }

    @staticmethod
    def _from_jira_description(value: Any) -> str | None:
        if isinstance(value, str):
            return value
        if not isinstance(value, Mapping):
            return None
        chunks: list[str] = []
        for block in value.get("content", []):
            for entry in block.get("content", []):
                if isinstance(entry, Mapping) and entry.get("type") == "text":
                    chunks.append(str(entry.get("text", "")))
        text = "".join(chunks).strip()
        return text or None

    @staticmethod
    def _status_from_jira(value: Any) -> CanonicalStatus:
        name = ""
        if isinstance(value, Mapping):
            name = str(value.get("name", "")).lower()
        if name in {"done", "closed", "resolved"}:
            return CanonicalStatus.DONE
        if name in {"in progress", "doing", "started"}:
            return CanonicalStatus.IN_PROGRESS
        if name in {"in review", "review"}:
            return CanonicalStatus.IN_REVIEW
        if name in {"blocked", "on hold"}:
            return CanonicalStatus.BLOCKED
        if name in {"canceled", "cancelled"}:
            return CanonicalStatus.CANCELED
        return CanonicalStatus.TODO

    @staticmethod
    def _issue_type_from_jira(value: Any) -> CanonicalIssueType:
        name = ""
        if isinstance(value, Mapping):
            name = str(value.get("name", "")).lower()
        if name in {"epic", "initiative"}:
            return CanonicalIssueType.EPIC
        if name in {"story"}:
            return CanonicalIssueType.STORY
        if name in {"bug", "defect"}:
            return CanonicalIssueType.BUG
        if name in {"sub-task", "subtask"}:
            return CanonicalIssueType.SUBTASK
        if name in {"chore", "maintenance"}:
            return CanonicalIssueType.CHORE
        return CanonicalIssueType.TASK

    @staticmethod
    def _priority_from_name(name: Any) -> int | None:
        if not isinstance(name, str):
            return None
        value = name.lower()
        mapping = {
            "highest": 0,
            "high": 1,
            "medium": 2,
            "low": 3,
            "lowest": 4,
        }
        return mapping.get(value)

    @staticmethod
    def _priority_to_name(priority: int) -> str:
        mapping = {
            0: "Highest",
            1: "High",
            2: "Medium",
            3: "Low",
            4: "Lowest",
        }
        return mapping.get(priority, "Medium")

    @staticmethod
    def _status_to_jira_name(status: CanonicalStatus) -> str:
        mapping = {
            CanonicalStatus.TODO: "To Do",
            CanonicalStatus.IN_PROGRESS: "In Progress",
            CanonicalStatus.IN_REVIEW: "In Review",
            CanonicalStatus.BLOCKED: "Blocked",
            CanonicalStatus.DONE: "Done",
            CanonicalStatus.CANCELED: "Canceled",
        }
        return mapping[status]

    @staticmethod
    def _to_jira_issue_type(issue_type: CanonicalIssueType) -> str:
        mapping = {
            CanonicalIssueType.EPIC: "Epic",
            CanonicalIssueType.STORY: "Story",
            CanonicalIssueType.TASK: "Task",
            CanonicalIssueType.BUG: "Bug",
            CanonicalIssueType.CHORE: "Task",
            CanonicalIssueType.SUBTASK: "Sub-task",
        }
        return mapping[issue_type]

    @staticmethod
    def _link_type_to_jira(link_type: LinkType) -> str:
        if link_type in (LinkType.BLOCKS, LinkType.BLOCKED_BY):
            return "Blocks"
        if link_type is LinkType.DUPLICATES:
            return "Duplicate"
        return "Relates"
