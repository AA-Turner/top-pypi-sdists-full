"""FP connector for spec-kitty-tracker.

This is a local/native connector used directly for local-first workflows.
It is not part of the SaaS-hosted transport model and does not require
NangoConnectionContext or proxy transport.
"""

from __future__ import annotations

import re
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
from spec_kitty_tracker.patch_contract import reject_unknown_patch_keys

ISSUE_LINE_RE = re.compile(
    r"^(?P<id>[A-Za-z0-9_-]+)\s+\[(?P<status>[^\]]+)\](?:\s+\[(?P<priority>[^\]]+)\])?\s+(?P<title>.+)$"
)


@dataclass(frozen=True, slots=True)
class FPConnectorConfig:
    workspace: str = "fp"
    command: str = "fp"
    cwd: str | None = None
    default_issue_type: CanonicalIssueType = CanonicalIssueType.TASK
    # TRK-M1-02 A4: caller-supplied scope/actor context. See
    # BeadsConnectorConfig.context for the fail-closed rationale.
    context: LocalExecutionContext | None = None


class FPConnector:
    """Connector for fp.dev CLI.

    This connector intentionally uses CLI output parsing because fp is local-first and
    optimized for terminal workflows. It supports robust list/create/update/comment flows
    and best-effort issue hydration via `fp issue show` + `fp context`.
    """

    name = "fp"

    def __init__(
        self,
        config: FPConnectorConfig | None = None,
        *,
        runner: CommandRunner | None = None,
    ) -> None:
        self.config = config or FPConnectorConfig()
        if self.config.context is not None and runner is None:
            # Fail-closed (TRK-M1-01 draft D3): see BeadsConnector.__init__.
            raise ConnectorConfigError(
                "FPConnectorConfig.context is set but no runner was supplied; "
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
            supports_custom_fields=False,
            supports_multi_assignee=False,
            supports_sprints_or_cycles=False,
            supports_bulk_read=False,
            supports_bulk_write=False,
            supports_delete=False,
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
        del updated_since, cursor
        command = [self.config.command, "issue", "list"]

        if filters:
            status = filters.get("status")
            if isinstance(status, CanonicalStatus):
                command.extend(["--status", self._canonical_to_fp_status(status)])
            elif isinstance(status, str) and status:
                command.extend(["--status", status])

        output = self._run(command)
        issues = self._parse_issue_lines(output)
        return Page(items=issues[:limit], next_cursor=None)

    async def get_issue(self, ref: ExternalRef) -> CanonicalIssue:
        show_output = self._run([self.config.command, "issue", "show", ref.id])
        context_output = self._run([self.config.command, "context", ref.id])

        parsed = self._parse_issue_line_with_id(show_output, ref.id)
        if parsed is None:
            # Fallback to scanning list output if show format changes.
            issues = await self.list_issues(
                updated_since=None,
                cursor=None,
                limit=500,
                filters=None,
            )
            parsed = next((issue for issue in issues.items if issue.ref.id == ref.id), None)
            if parsed is None:
                raise IssueNotFoundError(f"fp issue not found: {ref.id}")
        else:
            parsed.raw = {
                "show": show_output,
                "context": context_output,
            }

        parsed.body = context_output.strip() or parsed.body
        return parsed

    async def create_issue(self, issue: CanonicalIssue) -> CanonicalIssue:
        command = [self.config.command, "issue", "create", "--title", issue.title]
        if issue.body:
            command.extend(["--description", issue.body])
        if issue.parent is not None:
            command.extend(["--parent", issue.parent.id])
        if issue.priority is not None:
            command.extend(["--priority", self._priority_to_fp(issue.priority)])

        depends = [
            link.target.id
            for link in issue.links
            if link.type in {LinkType.BLOCKED_BY, LinkType.RELATES_TO}
        ]
        if depends:
            command.extend(["--depends", ",".join(depends)])

        output = self._run(command)
        issue_id = self._extract_issue_id(output)

        created = await self.get_issue(
            ExternalRef(system=self.name, workspace=self.config.workspace, id=issue_id)
        )

        if issue.status != CanonicalStatus.TODO:
            created = await self.transition_issue(created.ref, issue.status)

        if issue.links:
            for link in issue.links:
                if link.type in {LinkType.BLOCKS, LinkType.BLOCKED_BY, LinkType.RELATES_TO}:
                    await self.upsert_link(created.ref, link)

        return created

    async def update_issue(
        self,
        ref: ExternalRef,
        patch: Mapping[str, Any],
        *,
        idempotency_key: str | None,
    ) -> CanonicalIssue:
        del idempotency_key
        reject_unknown_patch_keys(patch, provider=self.name)

        unsupported = {"assignees", "custom_fields", "labels", "issue_type", "parent"}
        unsupported_keys = unsupported.intersection(patch.keys())
        if unsupported_keys:
            raise CapabilityNotSupportedError(
                "FPConnector does not currently support patch keys: "
                + ", ".join(sorted(unsupported_keys))
            )

        if "title" in patch or "body" in patch:
            # fp docs currently center update around status/priority/deps. We keep
            # this strict so callers don't assume title/body patching is guaranteed.
            raise CapabilityNotSupportedError(
                "FPConnector update currently supports status/priority/dependencies only"
            )

        command = [self.config.command, "issue", "update"]

        if "status" in patch:
            status = patch["status"]
            if not isinstance(status, CanonicalStatus):
                status = CanonicalStatus(str(status))
            command.extend(["--status", self._canonical_to_fp_status(status)])

        if "priority" in patch and patch["priority"] is not None:
            command.extend(["--priority", self._priority_to_fp(int(patch["priority"]))])

        if "depends" in patch:
            depends_value = patch["depends"]
            if isinstance(depends_value, Sequence):
                depends = [str(value) for value in depends_value if str(value)]
            else:
                depends = [str(depends_value)] if depends_value else []
            if depends:
                command.extend(["--depends", ",".join(depends)])

        if len(command) == 3:
            return await self.get_issue(ref)

        command.append(ref.id)
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
            target_issue = link.target.id
            depends = ref.id
        elif link.type in {LinkType.BLOCKED_BY, LinkType.RELATES_TO}:
            target_issue = ref.id
            depends = link.target.id
        else:
            raise CapabilityNotSupportedError(f"Unsupported fp link type: {link.type}")

        self._run(
            [
                self.config.command,
                "issue",
                "update",
                "--depends",
                depends,
                target_issue,
            ]
        )

    async def add_comment(self, ref: ExternalRef, body: str) -> None:
        self._run([self.config.command, "comment", ref.id, body])

    async def list_events(
        self,
        cursor: SyncCheckpoint | None,
        limit: int,
    ) -> tuple[list[TrackerEvent], SyncCheckpoint | None]:
        del cursor, limit
        return [], None

    def _run(self, command: Sequence[str]) -> str:
        # Pass-through rule (TRK-M1-02 A4): see BeadsConnector._run.
        if self.config.context is None:
            return self._runner.run(command, cwd=self.config.cwd)
        return self._runner.run(command, cwd=self.config.cwd, context=self.config.context)

    def _parse_issue_lines(self, text: str) -> list[CanonicalIssue]:
        issues: list[CanonicalIssue] = []
        for raw_line in text.splitlines():
            line = self._normalize_tree_line(raw_line)
            if not line:
                continue
            match = ISSUE_LINE_RE.match(line)
            if not match:
                continue
            issues.append(self._issue_from_match(match))
        return issues

    def _parse_issue_line_with_id(self, text: str, issue_id: str) -> CanonicalIssue | None:
        for raw_line in text.splitlines():
            line = self._normalize_tree_line(raw_line)
            if not line:
                continue
            match = ISSUE_LINE_RE.match(line)
            if match and match.group("id") == issue_id:
                return self._issue_from_match(match)

        fallback = self._extract_issue_id(text)
        if fallback != issue_id:
            return None

        return CanonicalIssue(
            ref=ExternalRef(
                system=self.name, workspace=self.config.workspace, id=issue_id, key=issue_id
            ),
            title=issue_id,
            body=None,
            status=CanonicalStatus.TODO,
            issue_type=self.config.default_issue_type,
            raw={"show": text},
        )

    def _issue_from_match(self, match: re.Match[str]) -> CanonicalIssue:
        issue_id = match.group("id")
        status = self._fp_to_canonical_status(match.group("status"))
        priority = self._priority_from_fp(match.group("priority") or "")
        title = match.group("title").strip()

        return CanonicalIssue(
            ref=ExternalRef(
                system=self.name,
                workspace=self.config.workspace,
                id=issue_id,
                key=issue_id,
            ),
            title=title,
            body=None,
            status=status,
            issue_type=self.config.default_issue_type,
            priority=priority,
            raw={"line": match.group(0)},
        )

    @staticmethod
    def _normalize_tree_line(line: str) -> str:
        normalized = line.strip()
        normalized = re.sub(r"^[│├└─\s]+", "", normalized)
        return normalized.strip()

    @staticmethod
    def _extract_issue_id(output: str) -> str:
        match = re.search(r"\b[A-Z][A-Z0-9]*-[A-Za-z0-9][A-Za-z0-9-]*\b", output)
        if not match:
            raise ConnectorRequestError("Unable to extract fp issue id from command output")
        return match.group(0)

    @staticmethod
    def _fp_to_canonical_status(status: str) -> CanonicalStatus:
        value = status.strip().lower()
        mapping = {
            "todo": CanonicalStatus.TODO,
            "in-progress": CanonicalStatus.IN_PROGRESS,
            "in_progress": CanonicalStatus.IN_PROGRESS,
            "done": CanonicalStatus.DONE,
            "blocked": CanonicalStatus.BLOCKED,
            "in-review": CanonicalStatus.IN_REVIEW,
            "in_review": CanonicalStatus.IN_REVIEW,
            "canceled": CanonicalStatus.CANCELED,
            "cancelled": CanonicalStatus.CANCELED,
        }
        return mapping.get(value, CanonicalStatus.TODO)

    @staticmethod
    def _canonical_to_fp_status(status: CanonicalStatus) -> str:
        mapping = {
            CanonicalStatus.TODO: "todo",
            CanonicalStatus.IN_PROGRESS: "in-progress",
            CanonicalStatus.IN_REVIEW: "in-progress",
            CanonicalStatus.BLOCKED: "in-progress",
            CanonicalStatus.DONE: "done",
            CanonicalStatus.CANCELED: "done",
        }
        return mapping[status]

    @staticmethod
    def _priority_from_fp(value: str) -> int | None:
        normalized = value.strip().lower()
        if not normalized:
            return None
        mapping = {
            "high": 1,
            "medium": 2,
            "low": 3,
        }
        if normalized in mapping:
            return mapping[normalized]
        try:
            parsed = int(normalized)
            return max(0, min(4, parsed))
        except ValueError:
            return None

    @staticmethod
    def _priority_to_fp(priority: int) -> str:
        if priority <= 1:
            return "high"
        if priority == 2:
            return "medium"
        return "low"
