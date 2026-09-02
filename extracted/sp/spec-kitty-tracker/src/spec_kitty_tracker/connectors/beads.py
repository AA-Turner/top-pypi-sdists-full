"""Beads connector for spec-kitty-tracker.

This is a local/native connector used directly for local-first workflows.
It is not part of the SaaS-hosted transport model and does not require
NangoConnectionContext or proxy transport.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from spec_kitty_tracker.capabilities import TrackerCapabilities
from spec_kitty_tracker.connectors.cli_runner import (
    CommandRunner,
    SubprocessCommandRunner,
)
from spec_kitty_tracker.context import LocalExecutionContext
from spec_kitty_tracker.errors import (
    CapabilityNotSupportedError,
    ConnectorConfigError,
    ConnectorRequestError,
    IssueNotFoundError,
    IssuePayloadContractError,
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
from spec_kitty_tracker.patch_contract import reject_unknown_patch_keys

# A5 (TRK-M1-03): terminal transitions are host-owned; Beads never closes or
# cancels a Bead on Tracker's behalf.
_TERMINAL_STATUSES = frozenset({CanonicalStatus.DONE, CanonicalStatus.CANCELED})


@dataclass(frozen=True, slots=True)
class BeadsConnectorConfig:
    workspace: str = "beads"
    command: str = "bd"
    cwd: str | None = None
    # TRK-M1-02 A4: caller-supplied scope/actor context. When set, the
    # connector requires an explicit runner (see the fail-closed rule in
    # BeadsConnector.__init__) so a scoped context can never silently fall
    # back to the default direct-subprocess runner.
    context: LocalExecutionContext | None = None


class BeadsConnector:
    name = "beads"

    def __init__(
        self,
        config: BeadsConnectorConfig | None = None,
        *,
        runner: CommandRunner | None = None,
    ) -> None:
        self.config = config or BeadsConnectorConfig()
        if self.config.context is not None and runner is None:
            # Fail-closed (TRK-M1-01 draft D3): a scoped context must never
            # fall back to the default direct-subprocess runner — that is
            # exactly the prohibited bypass (ARCHITECTURE.md §2 invariant 7).
            raise ConnectorConfigError(
                "BeadsConnectorConfig.context is set but no runner was supplied; "
                "a scoped context requires an explicit runner (e.g. a gateway-"
                "backed runner), never the default direct-subprocess runner."
            )
        self._runner = runner or SubprocessCommandRunner()

    async def get_capabilities(self) -> TrackerCapabilities:
        return TrackerCapabilities(
            supports_webhooks=False,
            supports_comments=True,
            supports_hierarchy=True,
            supports_dependencies=True,
            supports_custom_fields=True,
            supports_multi_assignee=False,
            supports_sprints_or_cycles=False,
            supports_bulk_read=True,
            supports_bulk_write=True,
            supports_delete=False,
            # A5 (TRK-M1-03) denies assignment/terminal-transition writes
            # unconditionally; these flags say so honestly.
            supports_assignment=False,
            supports_terminal_transition=False,
        )

    async def list_issues(
        self,
        *,
        updated_since: datetime | None,
        cursor: str | None,
        limit: int,
        filters: Mapping[str, Any] | None,
    ) -> Page[CanonicalIssue]:
        del cursor  # beads CLI is not cursor-paginated
        command = [self.config.command, "--json", "list"]

        if updated_since is not None:
            command.extend(["--updated-after", updated_since.date().isoformat()])
        if filters:
            status = filters.get("status")
            if isinstance(status, CanonicalStatus):
                command.extend(["--status", self._canonical_to_beads_status(status)])
            elif isinstance(status, str) and status:
                command.extend(["--status", status])

            title_contains = filters.get("title_contains")
            if isinstance(title_contains, str) and title_contains:
                command.extend(["--title-contains", title_contains])

            assignee = filters.get("assignee")
            if isinstance(assignee, str) and assignee:
                command.extend(["--assignee", assignee])

        output = self._run(command)
        payload = self._parse_json(output)

        issues_data = payload if isinstance(payload, list) else payload.get("items", [])
        issues = [self._to_canonical(item) for item in issues_data if isinstance(item, Mapping)]
        return Page(items=issues[:limit], next_cursor=None)

    async def get_issue(self, ref: ExternalRef) -> CanonicalIssue:
        output = self._run([self.config.command, "--json", "show", ref.id])
        payload = self._parse_json(output)

        # `bd show --json` may return a details object, a bare issue object, or a list.
        if isinstance(payload, list):
            candidate = payload[0] if payload else None
        else:
            candidate = payload

        if not isinstance(candidate, Mapping):
            raise IssueNotFoundError(f"Beads issue not found: {ref.id}")

        if "issue" in candidate and isinstance(candidate["issue"], Mapping):
            issue = self._to_canonical(candidate["issue"], details=candidate)
        else:
            issue = self._to_canonical(candidate)

        return issue

    async def create_issue(self, issue: CanonicalIssue) -> CanonicalIssue:
        command = [
            self.config.command,
            "--json",
            "create",
            issue.title,
            "--type",
            self._canonical_to_beads_type(issue.issue_type),
            "--priority",
            str(issue.priority if issue.priority is not None else 2),
        ]
        if issue.body:
            command.extend(["--description", issue.body])
        if issue.parent is not None:
            command.extend(["--parent", issue.parent.id])
        # A5 (TRK-M1-03): create_issue never emits --assignee. Assignment is
        # host-owned; Beads never assigns a Bead on Tracker's behalf.
        for label in issue.labels:
            command.extend(["--label", label])

        output = self._run(command)
        payload = self._parse_json(output)
        issue_id = self._extract_issue_id(payload)

        if issue.status not in {CanonicalStatus.TODO, CanonicalStatus.IN_PROGRESS}:
            await self.transition_issue(
                ExternalRef(system=self.name, workspace=self.config.workspace, id=issue_id),
                issue.status,
            )

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
        reject_unknown_patch_keys(patch, provider=self.name)

        # A5 (TRK-M1-03): Beads never assigns, never performs a terminal
        # transition, and never silently drops a key it cannot carry
        # (custom_fields, links) -- every denial is typed and raised before
        # any bd command is issued.
        if "assignees" in patch:
            raise CapabilityNotSupportedError("beads: assignment is host-owned")
        if "custom_fields" in patch:
            raise CapabilityNotSupportedError("beads: custom_fields is read-only")
        if "links" in patch:
            raise CapabilityNotSupportedError("beads: links is read-only")

        command = [self.config.command, "--json", "update", ref.id]

        if "status" in patch:
            status = patch["status"]
            if not isinstance(status, CanonicalStatus):
                status = CanonicalStatus(str(status))
            if status in _TERMINAL_STATUSES:
                raise CapabilityNotSupportedError("beads: terminal transition is host-owned")
            mapped_status = self._canonical_to_beads_status(status)
            command.extend(["--status", mapped_status])

        if "priority" in patch and patch["priority"] is not None:
            command.extend(["--priority", str(int(patch["priority"]))])

        if "title" in patch and patch["title"] is not None:
            command.extend(["--title", str(patch["title"])])

        if "body" in patch:
            command.extend(["--description", str(patch["body"] or "")])

        if "issue_type" in patch and patch["issue_type"] is not None:
            issue_type = patch["issue_type"]
            if not isinstance(issue_type, CanonicalIssueType):
                issue_type = CanonicalIssueType(str(issue_type))
            command.extend(["--type", self._canonical_to_beads_type(issue_type)])

        if "labels" in patch:
            labels = patch["labels"]
            if not isinstance(labels, Sequence):
                raise ConnectorRequestError("labels patch must be a sequence")
            for label in labels:
                command.extend(["--set-labels", str(label)])

        if "parent" in patch:
            parent = patch["parent"]
            if parent is None:
                command.extend(["--parent", ""])
            elif isinstance(parent, ExternalRef):
                command.extend(["--parent", parent.id])
            else:
                raise ConnectorRequestError("parent patch must be ExternalRef or None")

        if len(command) == 4:
            return await self.get_issue(ref)

        self._run(command)
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
        if link.type is LinkType.BLOCKS:
            issue_id = link.target.id
            depends_on = ref.id
            dep_type = "blocks"
        elif link.type is LinkType.BLOCKED_BY:
            issue_id = ref.id
            depends_on = link.target.id
            dep_type = "blocks"
        elif link.type in {LinkType.RELATES_TO, LinkType.DUPLICATES}:
            issue_id = ref.id
            depends_on = link.target.id
            dep_type = "related"
        elif link.type is LinkType.CHILD_OF:
            issue_id = ref.id
            depends_on = link.target.id
            dep_type = "parent-child"
        elif link.type is LinkType.PARENT_OF:
            issue_id = link.target.id
            depends_on = ref.id
            dep_type = "parent-child"
        else:
            raise CapabilityNotSupportedError(f"Unsupported link type for Beads: {link.type}")

        self._run(
            [
                self.config.command,
                "--json",
                "dep",
                "add",
                issue_id,
                depends_on,
                "--type",
                dep_type,
            ]
        )

    async def add_comment(self, ref: ExternalRef, body: str) -> None:
        self._run([self.config.command, "--json", "comments", "add", ref.id, body])

    async def list_events(
        self,
        cursor: SyncCheckpoint | None,
        limit: int,
    ) -> tuple[list[TrackerEvent], SyncCheckpoint | None]:
        del cursor, limit
        return [], None

    def _run(self, command: Sequence[str]) -> str:
        # Pass-through rule (TRK-M1-02 A4): call the runner exactly as in
        # 0.4.3 when no context is configured, so a pre-existing
        # 0.4.3-signature runner (no `context` parameter) keeps working
        # unchanged. Only pass `context=` when the config actually carries
        # one.
        if self.config.context is None:
            return self._runner.run(command, cwd=self.config.cwd)
        return self._runner.run(command, cwd=self.config.cwd, context=self.config.context)

    @staticmethod
    def _parse_json(output: str) -> Any:
        text = output.strip()
        if not text:
            return {}
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            # A8 (TRK-M1-03): malformed bd JSON fails closed, never silently
            # coerced to an empty/default payload.
            raise IssuePayloadContractError(
                f"Invalid JSON from bd: {exc}",
                kind="issue",
                reason="BD-000",
            ) from exc

    def _to_canonical(
        self,
        item: Mapping[str, Any],
        *,
        details: Mapping[str, Any] | None = None,
    ) -> CanonicalIssue:
        labels = item.get("labels", [])
        if not isinstance(labels, list):
            labels = []

        assignee = item.get("assignee")
        assignees = [str(assignee)] if isinstance(assignee, str) and assignee else []

        parent_ref = None
        parent_value = item.get("parent")
        if isinstance(parent_value, str) and parent_value:
            parent_ref = ExternalRef(
                system=self.name, workspace=self.config.workspace, id=parent_value
            )

        links: list[CanonicalLink] = []
        dependencies_payload = None
        if details is not None:
            dependencies_payload = details.get("dependencies")
        if dependencies_payload is None:
            dependencies_payload = item.get("dependencies")

        if isinstance(dependencies_payload, list):
            for dep in dependencies_payload:
                if not isinstance(dep, Mapping):
                    continue
                target = str(
                    dep.get("id") or dep.get("depends_on_id") or dep.get("dependsOnId") or ""
                )
                if not target:
                    continue
                dep_type = str(dep.get("dependency_type") or dep.get("type") or "blocks")
                links.append(
                    CanonicalLink(
                        type=self._beads_dependency_to_link(dep_type),
                        target=ExternalRef(
                            system=self.name, workspace=self.config.workspace, id=target
                        ),
                    )
                )

        custom_fields: dict[str, Any] = {}
        if item.get("metadata") is not None:
            custom_fields["metadata"] = item.get("metadata")
        if details and details.get("comments") is not None:
            custom_fields["comments"] = details.get("comments")

        external_ref = item.get("external_ref")
        raw = dict(item)
        if details:
            raw["details"] = dict(details)

        # A8 (TRK-M1-03): id/title are required and never guessed. A missing
        # or empty value fails closed instead of silently becoming "" or
        # "Untitled".
        raw_id = item.get("id")
        if not isinstance(raw_id, str) or not raw_id.strip():
            raise IssuePayloadContractError(
                "Beads issue payload missing a non-empty id",
                kind="issue",
                field_path="id",
                reason="BD-001",
            )
        raw_title = item.get("title")
        if not isinstance(raw_title, str) or not raw_title.strip():
            raise IssuePayloadContractError(
                "Beads issue payload missing a non-empty title",
                kind="issue",
                field_path="title",
                reason="BD-002",
            )

        return CanonicalIssue(
            ref=ExternalRef(
                system=self.name,
                workspace=self.config.workspace,
                id=raw_id,
                key=raw_id,
                url=str(external_ref) if isinstance(external_ref, str) and external_ref else None,
            ),
            title=raw_title,
            body=str(item.get("description")) if item.get("description") else None,
            status=self._beads_to_canonical_status(str(item.get("status") or "open")),
            issue_type=self._beads_to_canonical_type(str(item.get("issue_type") or "task")),
            priority=self._clamp_priority(item.get("priority")),
            assignees=assignees,
            labels=[str(label) for label in labels],
            parent=parent_ref,
            links=links,
            custom_fields=custom_fields,
            created_at=parse_datetime(item.get("created_at")),
            updated_at=parse_datetime(item.get("updated_at")),
            raw=raw,
        )

    @staticmethod
    def _extract_issue_id(payload: Any) -> str:
        if isinstance(payload, Mapping):
            raw_id = payload.get("id")
            if isinstance(raw_id, str):
                return raw_id
            if isinstance(payload.get("issue"), Mapping):
                issue = payload["issue"]
                issue_id = issue.get("id")
                if isinstance(issue_id, str):
                    return issue_id
        if isinstance(payload, list) and payload and isinstance(payload[0], Mapping):
            first = payload[0]
            first_id = first.get("id")
            if isinstance(first_id, str):
                return first_id
        raise ConnectorRequestError("Unable to determine issue id from beads response")

    @staticmethod
    def _clamp_priority(value: Any) -> int | None:
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            return None
        return max(0, min(4, parsed))

    @staticmethod
    def _beads_to_canonical_status(status: str) -> CanonicalStatus:
        value = status.lower()
        mapping = {
            "open": CanonicalStatus.TODO,
            "in_progress": CanonicalStatus.IN_PROGRESS,
            "blocked": CanonicalStatus.BLOCKED,
            "deferred": CanonicalStatus.TODO,
            "closed": CanonicalStatus.DONE,
            "pinned": CanonicalStatus.IN_PROGRESS,
            "tombstone": CanonicalStatus.CANCELED,
        }
        # A8 (TRK-M1-03): an out-of-vocabulary status fails closed rather
        # than silently defaulting to TODO.
        if value not in mapping:
            raise IssuePayloadContractError(
                f"Unknown Beads status: {status!r}",
                kind="issue",
                field_path="status",
                reason="BD-003",
            )
        return mapping[value]

    @staticmethod
    def _canonical_to_beads_status(status: CanonicalStatus) -> str:
        mapping = {
            CanonicalStatus.TODO: "open",
            CanonicalStatus.IN_PROGRESS: "in_progress",
            CanonicalStatus.IN_REVIEW: "in_progress",
            CanonicalStatus.BLOCKED: "blocked",
            CanonicalStatus.DONE: "closed",
            CanonicalStatus.CANCELED: "closed",
        }
        return mapping[status]

    @staticmethod
    def _beads_to_canonical_type(value: str) -> CanonicalIssueType:
        normalized = value.lower()
        mapping = {
            "epic": CanonicalIssueType.EPIC,
            "feature": CanonicalIssueType.STORY,
            "task": CanonicalIssueType.TASK,
            "bug": CanonicalIssueType.BUG,
            "chore": CanonicalIssueType.CHORE,
            "decision": CanonicalIssueType.CHORE,
        }
        # A8 (TRK-M1-03): an out-of-vocabulary issue type fails closed
        # rather than silently defaulting to TASK.
        if normalized not in mapping:
            raise IssuePayloadContractError(
                f"Unknown Beads issue_type: {value!r}",
                kind="issue",
                field_path="issue_type",
                reason="BD-004",
            )
        return mapping[normalized]

    @staticmethod
    def _canonical_to_beads_type(issue_type: CanonicalIssueType) -> str:
        mapping = {
            CanonicalIssueType.EPIC: "epic",
            CanonicalIssueType.STORY: "feature",
            CanonicalIssueType.TASK: "task",
            CanonicalIssueType.BUG: "bug",
            CanonicalIssueType.CHORE: "chore",
            CanonicalIssueType.SUBTASK: "task",
        }
        return mapping[issue_type]

    @staticmethod
    def _beads_dependency_to_link(dep_type: str) -> LinkType:
        normalized = dep_type.lower()
        if normalized in {"blocks"}:
            return LinkType.BLOCKED_BY
        if normalized in {"related", "relates_to", "relates"}:
            return LinkType.RELATES_TO
        if normalized == "duplicates":
            return LinkType.DUPLICATES
        if normalized == "parent-child":
            return LinkType.CHILD_OF
        if normalized == "discovered-from":
            return LinkType.RELATES_TO
        # A8 (TRK-M1-03): an unknown dependency type fails closed rather
        # than silently defaulting to BLOCKED_BY.
        raise IssuePayloadContractError(
            f"Unknown Beads dependency_type: {dep_type!r}",
            kind="issue",
            field_path="dependencies[].dependency_type",
            reason="BD-005",
        )
