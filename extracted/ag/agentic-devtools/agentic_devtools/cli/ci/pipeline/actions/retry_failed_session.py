"""Retry or escalate failed Copilot coding-agent sessions."""

from __future__ import annotations

import logging
import re
from dataclasses import replace

from agentic_devtools.cli.ci.guards import (
    AGENT_FAILED_LABEL,
    AGENT_RETRY_ALIAS_MARKER_PREFIX,
    AGENT_RETRY_ESCALATION_MARKER_PREFIX,
    AGENT_RETRY_IDENTITY_MARKER_PREFIX,
    AGENT_RETRY_MARKER_PREFIX,
    check_docker_files,
    check_exclusion_labels,
    check_fork_pr,
    check_privileged_paths,
    classify_agent_retry_failure,
    get_agent_retry_markers,
    is_agent_retry_confirmation_expired,
)
from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.actions.initial_delivery_recovery import InitialDeliveryRecovery
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.session_detector import (
    SessionOutcome,
    SessionState,
    get_latest_session_state,
    is_copilot_session_active_via_agent_task,
)
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.scheduler import resolve_agent_retry_limit
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)
_AGENT_RETRY_ESCALATION_MARKER_RE = re.compile(r"<!-- agdt:agent-retry-escalation:([^:\s>]+) -->")
_AGENT_RETRY_ESCALATION_ALIAS_MARKER_RE = re.compile(r"<!-- agdt:agent-retry-escalation-alias:([^:\s>]+) -->")
_AGENT_RETRY_ESCALATION_PR_MARKER_RE = re.compile(r"<!-- agdt:agent-retry-escalation-pr:(\d+) -->")


class RetryFailedSessionAction:
    """Retry each failed session once, then add a human-readable escalation."""

    terminates_run = True

    def __init__(self, provider: CIPlatformProvider, retry_limit: int | None = None) -> None:
        if retry_limit is not None and (
            not isinstance(retry_limit, int) or isinstance(retry_limit, bool) or not 0 <= retry_limit <= 5
        ):
            raise ValueError("retry_limit must be an integer between 0 and 5")
        self._provider = provider
        self._retry_limit = resolve_agent_retry_limit() if retry_limit is None else retry_limit

    @property
    def name(self) -> str:
        return "retry_failed_session"

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Check the latest session and safety gates before a retry or escalation."""
        unsafe_reason = self._unsafe_reason(snapshot)
        if unsafe_reason:
            return ActionResult(name=self.name, decision=ActionDecision.BLOCKED, details=unsafe_reason)
        state = get_latest_session_state(
            self._provider,
            snapshot.pr_number,
            repo=snapshot.base_repo_full_name,
            head_branch=snapshot.head_branch,
            pr_id=snapshot.pr_id,
            head_sha=snapshot.head_sha,
        )
        if state.outcome is SessionOutcome.FAILED and state.task_id is None:
            lifecycle_active = is_copilot_session_active_via_agent_task(
                snapshot.base_repo_full_name,
                snapshot.pr_number,
                provider=self._provider,
                head_branch=snapshot.head_branch,
                pr_id=snapshot.pr_id,
                head_sha=snapshot.head_sha,
            )
            if lifecycle_active is not False:
                outcome = SessionOutcome.ACTIVE if lifecycle_active is True else SessionOutcome.UNKNOWN
                state = replace(state, outcome=outcome)
                derived.set("latest_session_state", state)
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.BLOCKED,
                    preconditions=(
                        {"session_active": True} if lifecycle_active is True else {"session_outcome_known": False}
                    ),
                    details=(
                        "Active Copilot lifecycle blocks timeline failure retry and subsequent pipeline actions"
                        if lifecycle_active is True
                        else "Copilot lifecycle evidence is unknown; timeline failure retry is blocked"
                    ),
                )
        derived.set("latest_session_state", state)
        result = InitialDeliveryRecovery(self).evaluate_session(snapshot, derived, state)
        if result is not None:
            return result

        failure_id = self._failure_identity(state)
        if not failure_id:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.BLOCKED,
                details="Failed Copilot session has no stable failure identity",
            )

        try:
            dispatch_login = self._provider.get_dispatch_login()
            if not dispatch_login:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.BLOCKED,
                    details="Could not resolve the trusted retry-dispatch identity",
                )
            comments = self._provider.list_issue_comments(snapshot.pr_number)
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.warning("PR #%d: Failed to inspect retry markers: %s", snapshot.pr_number, exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.BLOCKED,
                details="Retry-marker state is unavailable",
            )

        markers = get_agent_retry_markers(comments, dispatch_login)
        failure_identities = {failure_id}
        if state.task_id:
            failure_identities.add(state.task_id)
        if state.failure_event_id is not None:
            failure_identities.add(str(state.failure_event_id))
        marker_status = classify_agent_retry_failure(
            failure_identities,
            state.failure_created_at,
            comments,
            dispatch_login,
            failure_task_id=state.task_id,
            failure_event_id=state.failure_event_id,
        )
        confirmation_expired = marker_status == "handled" and is_agent_retry_confirmation_expired(
            comments,
            dispatch_login,
        )
        if marker_status == "handled" and not confirmation_expired:
            derived.set("agent_retry_mode", "already_handled")
            return ActionResult(
                name=self.name,
                decision=ActionDecision.BLOCKED,
                preconditions={"session_failed": True, "failure_already_handled": True},
                details=f"Failed session {failure_id} already has a retry marker",
            )
        if marker_status == "uncorrelated":
            return ActionResult(
                name=self.name,
                decision=ActionDecision.BLOCKED,
                details="Cannot correlate the timeline failure with an existing Agent Task retry marker",
            )

        escalation_identities = self._escalation_identities(comments, dispatch_login)
        escalation_posted = bool(
            failure_identities.intersection(escalation_identities)
            or self._pr_escalation_identity(snapshot.pr_number) in escalation_identities
        )
        if AGENT_FAILED_LABEL in snapshot.labels and escalation_posted:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.BLOCKED,
                details="Failed-session escalation is already complete",
            )

        aliases = (
            [str(state.failure_event_id)]
            if (state.failure_event_id is not None and str(state.failure_event_id) != failure_id)
            else []
        )
        derived.set("agent_retry_failure_aliases", aliases)
        retries_used = sum(markers.values())
        mode = (
            "escalate"
            if (
                confirmation_expired
                or AGENT_FAILED_LABEL in snapshot.labels
                or escalation_posted
                or retries_used >= self._retry_limit
            )
            else "retry"
        )
        derived.set("agent_retry_mode", mode)
        if confirmation_expired:
            derived.set("agent_retry_escalation_reason", "confirmation_expired")
        derived.set("agent_retry_failure_id", failure_id)
        derived.set("agent_retry_attempt", retries_used + 1)
        derived.set("agent_retry_limit", self._retry_limit)
        derived.set("agent_retry_task_id", state.task_id or "")
        derived.set("agent_retry_failure_event_id", state.failure_event_id)
        derived.set("agent_retry_dispatch_login", dispatch_login)
        derived.set("agent_retry_comments", comments)
        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions={"session_failed": True, "failure_already_handled": False},
            details="Retry confirmation window expired; escalate"
            if confirmation_expired
            else f"Retry failed Copilot session {failure_id}"
            if mode == "retry"
            else "Retry budget exhausted; escalate"
            if retries_used >= self._retry_limit
            else "Complete failed-session escalation",
        )

    @staticmethod
    def _escalation_identities(comments: object, dispatch_login: str) -> set[str]:
        """Return trusted primary and correlated identities from escalation headers."""
        if not isinstance(comments, list) or not dispatch_login:
            return set()
        identities: set[str] = set()
        for comment in comments:
            if not isinstance(comment, IssueCommentInfo) or comment.author != dispatch_login:
                continue
            lines = comment.body.splitlines()
            if not lines:
                continue
            primary = _AGENT_RETRY_ESCALATION_MARKER_RE.fullmatch(lines[0].strip())
            if primary is None:
                continue
            identities.add(primary.group(1))
            for line in lines[1:]:
                if not line.strip():
                    break
                alias = _AGENT_RETRY_ESCALATION_ALIAS_MARKER_RE.fullmatch(line.strip())
                if alias is not None:
                    identities.add(alias.group(1))
                    continue
                pr_marker = _AGENT_RETRY_ESCALATION_PR_MARKER_RE.fullmatch(line.strip())
                if pr_marker is not None:
                    identities.add(RetryFailedSessionAction._pr_escalation_identity(int(pr_marker.group(1))))
                    continue
                break
        return identities

    @staticmethod
    def _pr_escalation_identity(pr_number: int) -> str:
        """Return the persistent escalation identity for one pull request."""
        return f"pr:{pr_number}"

    def _unsafe_reason(self, snapshot: PRStateSnapshot) -> str:
        if check_fork_pr(snapshot.head_repo_full_name, snapshot.base_repo_full_name):
            return "Failed-session retry blocked for fork PR"
        should_skip, _flag = check_exclusion_labels(snapshot.labels)
        if should_skip:
            return "Failed-session retry blocked by exclusion label"
        if check_privileged_paths(snapshot.files):
            return "Failed-session retry blocked for privileged paths"
        if check_docker_files(snapshot.files):
            return "Failed-session retry blocked for Docker files"
        return ""

    @staticmethod
    def _failure_identity(state: SessionState) -> str:
        if state.task_id:
            return state.task_id
        if state.failure_event_id is not None and state.failure_event_id > 0:
            return str(state.failure_event_id)
        return ""

    @staticmethod
    def _is_dispatched_repair_comment(body: str) -> bool:
        """Identify a dispatch-identity comment that carries real repair findings.

        Excludes the dedup tracker (``check_deduplication``'s own
        ``repair-dispatch`` marker comment, which only says "Dispatch tracking
        for ..." and carries no findings) and this action's own agent-retry /
        escalation comments (they restate or report on a failure, they do not
        carry the original task). A dispatch must be identified from its
        ``@copilot`` header; markers quoted later in a comment are not dispatch
        metadata.
        """
        lines = body.lstrip().splitlines()
        if not lines:
            return False
        first_line = lines[0].strip()
        if re.fullmatch(r"<!-- agdt:agent-retry(?:-escalation)?:[^>]+ -->", first_line):
            return False
        if len(lines) < 3:
            return re.match(r"@copilot(?:\s|$)", first_line, re.IGNORECASE) is not None
        copilot_first = re.match(r"@copilot(?:\s|$)", lines[0].strip(), re.IGNORECASE) is not None
        retry_marker = re.fullmatch(r"<!-- agdt:agent-retry:[^:\s>]+:\d+ -->", lines[2].strip())
        if copilot_first:
            return not (not lines[1].strip() and retry_marker is not None)
        return False

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Dispatch one retry or publish an idempotent escalation notice."""
        if derived.get("initial_delivery_mode"):
            return InitialDeliveryRecovery(self).execute(provider, snapshot, derived)
        mode = derived.get("agent_retry_mode", "")
        failure_id = derived.get("agent_retry_failure_id", "")
        if mode not in {"retry", "escalate"} or not isinstance(failure_id, str) or not failure_id:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error="Retry evaluation state is unavailable",
                details="Failed-session action could not recover its evaluation state",
            )

        if mode == "retry":
            attempt = derived.get("agent_retry_attempt", 1)
            limit = derived.get("agent_retry_limit", self._retry_limit)
            prompt = self._build_retry_prompt(snapshot, derived, failure_id, attempt, limit)
            try:
                provider.dispatch_agent_retry(snapshot.pr_number, prompt, failure_id)
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.error("PR #%d: Failed to dispatch failed-session retry: %s", snapshot.pr_number, exc)
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.FAILED,
                    error=str(exc),
                    details="Failed-session retry dispatch failed",
                )
            return ActionResult(
                name=self.name,
                decision=ActionDecision.EXECUTE,
                preconditions={"retry_dispatched": True},
                details=f"Dispatched retry {attempt} of {limit} for failed session {failure_id}",
            )

        return self._escalate(provider, snapshot, derived, failure_id)

    def _build_retry_prompt(
        self,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
        failure_id: str,
        attempt: int,
        limit: int,
    ) -> str:
        marker = f"{AGENT_RETRY_MARKER_PREFIX}{failure_id}:{attempt} -->"
        aliases = derived.get("agent_retry_failure_aliases", [])
        alias_markers = (
            [
                f"{AGENT_RETRY_ALIAS_MARKER_PREFIX}{alias} -->"
                for alias in aliases
                if isinstance(alias, str) and alias and alias != failure_id
            ]
            if isinstance(aliases, (list, tuple))
            else []
        )
        task_id = derived.get("agent_retry_task_id", "")
        task_marker = (
            f"{AGENT_RETRY_IDENTITY_MARKER_PREFIX}task:{task_id} -->" if isinstance(task_id, str) and task_id else ""
        )
        event_id = derived.get("agent_retry_failure_event_id")
        event_marker = (
            f"{AGENT_RETRY_IDENTITY_MARKER_PREFIX}event:{event_id} -->"
            if isinstance(event_id, int) and not isinstance(event_id, bool) and event_id > 0
            else ""
        )
        identity_markers = [identity for identity in (task_marker, event_marker) if identity]
        context_sections: list[str] = []
        original_context_found = False
        task_prompt_found = False
        if snapshot.title:
            context_sections.append(f"## Pull request title\n\n{snapshot.title}")
        task_id = derived.get("agent_retry_task_id", "")
        if isinstance(task_id, str) and task_id:
            try:
                task_prompt = self._provider.get_agent_task_prompt(task_id)
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.warning("PR #%d: Failed to load original Agent Task prompt: %s", snapshot.pr_number, exc)
                task_prompt = ""
            if isinstance(task_prompt, str) and task_prompt.strip():
                context_sections.append(f"## Previous repair task context\n\n{task_prompt}")
                original_context_found = True
                task_prompt_found = True
        comments = derived.get("agent_retry_comments", [])
        dispatch_login = derived.get("agent_retry_dispatch_login", "")
        if not original_context_found and isinstance(comments, list) and isinstance(dispatch_login, str):
            repair_comments = [
                comment
                for comment in comments
                if isinstance(comment, IssueCommentInfo)
                and comment.author == dispatch_login
                and self._is_dispatched_repair_comment(comment.body)
            ]
            if repair_comments:
                latest = max(repair_comments, key=lambda comment: comment.id)
                context_sections.append(f"## Previous repair task context\n\n{latest.body}")
                original_context_found = True

        if not task_prompt_found:
            try:
                closing_issues = self._provider.list_closing_issues(snapshot.pr_number)
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.warning("PR #%d: Failed to load linked retry context: %s", snapshot.pr_number, exc)
                closing_issues = []
            for issue in closing_issues:
                context_sections.append(f"## Linked issue #{issue.number}: {issue.title}\n\n{issue.body}")
            original_context_found = original_context_found or bool(closing_issues)

        if not original_context_found:
            try:
                description = self._provider.get_pr_body(snapshot.pr_number)
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.warning("PR #%d: Failed to load PR description for retry context: %s", snapshot.pr_number, exc)
                description = ""
            if description:
                context_sections.append(f"## Pull request description\n\n{description}")
                original_context_found = True
        if not original_context_found:
            context_sections.append("No linked issue, prior repair context, or PR description could be recovered.")
        context = "\n\n".join(context_sections)
        retry_metadata = "\n".join([marker, *alias_markers, *identity_markers])
        return (
            f"{retry_metadata}\n\n"
            f"Copilot session {failure_id} failed. Retrying attempt {attempt} of {limit}. "
            "Continue the original task and address the failure without discarding existing work.\n\n"
            f"@copilot Please resume the original task using this context:\n\n{context}"
        )

    def _escalate(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
        failure_id: str,
    ) -> ActionResult:
        """Post one human-readable escalation comment, then add the failure label.

        Comment-first ordering prevents scheduler exclusion without an explanation.
        A failed label write leaves the PR schedulable for an idempotent label retry.
        """
        comments = derived.get("agent_retry_comments", [])
        dispatch_login = derived.get("agent_retry_dispatch_login", "")
        marker = f"{AGENT_RETRY_ESCALATION_MARKER_PREFIX}{failure_id} -->"
        aliases = derived.get("agent_retry_failure_aliases", [])
        escalation_identities = {failure_id}
        alias_markers: list[str] = []
        if isinstance(aliases, (list, tuple)):
            for alias in aliases:
                if isinstance(alias, str) and alias and alias != failure_id:
                    escalation_identities.add(alias)
                    alias_markers.append(f"<!-- agdt:agent-retry-escalation-alias:{alias} -->")
        pr_identity = self._pr_escalation_identity(snapshot.pr_number)
        escalation_identities.add(pr_identity)
        pr_marker = f"<!-- agdt:agent-retry-escalation-pr:{snapshot.pr_number} -->"
        existing = bool(escalation_identities.intersection(self._escalation_identities(comments, dispatch_login)))
        failures: list[str] = []
        if not existing:
            markers = (
                get_agent_retry_markers(comments, dispatch_login)
                if isinstance(comments, list) and isinstance(dispatch_login, str)
                else {}
            )
            attempt_count = sum(markers.values())
            failure_identities = {failure_id}
            if isinstance(aliases, (list, tuple)):
                failure_identities.update(
                    alias for alias in aliases if isinstance(alias, str) and alias and alias != failure_id
                )
            failed_sessions = ", ".join(sorted({*markers, *failure_identities}))
            escalation_header = "\n".join([marker, pr_marker, *alias_markers])
            escalation_reason = derived.get("agent_retry_escalation_reason", "")
            if escalation_reason == "confirmation_expired":
                body = (
                    f"{escalation_header}\n\n"
                    "A retry request was not confirmed by a new Copilot session within the bounded "
                    "confirmation window. This PR is excluded from the AI PR Loop. To resume, remove "
                    f"the `{AGENT_FAILED_LABEL}` label and retry the task manually."
                )
            else:
                body = (
                    f"{escalation_header}\n\n"
                    f"{len(markers) + 1} Copilot coding-agent session(s) failed for this PR. "
                    f"Failure identities: {failed_sessions}. "
                    f"The retry budget of {self._retry_limit} retries is exhausted after {attempt_count} retries. "
                    f"This PR is excluded from the AI PR Loop. To resume, remove the `{AGENT_FAILED_LABEL}` label "
                    "and retry the task manually."
                )
            body = derived.get("initial_delivery_escalation_body", body)
            try:
                provider.post_comment_as_pr_token(snapshot.pr_number, body)
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.warning("PR #%d: Could not post failed-agent escalation: %s", snapshot.pr_number, exc)
                failures.append(f"failed to post escalation: {exc}")
        if not failures:
            try:
                InitialDeliveryRecovery(self).validate_escalation(snapshot, derived)
                provider.add_label(snapshot.pr_number, AGENT_FAILED_LABEL)
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.warning("PR #%d: Could not add failed-agent label: %s", snapshot.pr_number, exc)
                failures.append(f"failed to add label: {exc}")
        if failures:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error="; ".join(failures),
                details="Failed-session escalation was incomplete",
            )
        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions={"retry_dispatched": False},
            details=f"Escalated failed session {failure_id} after retry budget exhaustion",
        )
