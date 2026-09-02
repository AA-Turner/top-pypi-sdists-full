"""Cascade trigger processor for hierarchical spec pipelines.

Implements FR-003 (cascade to next target), FR-004 (halt on speckit:failed),
FR-005 (skip speckit:skip with informational comment), FR-006 (completion comment),
FR-007 (parent notification on last sibling), and NFR-005 (retry with backoff).
"""

from __future__ import annotations

import json
import re
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TypeVar

from agentic_devtools.cli.subprocess_utils import run_safe
from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml
from agentic_devtools.hierarchy.models import CascadeDirection, CascadeEvent, ChildInfo

_T = TypeVar("_T")

# Final phase by hierarchy level.  The original FR-001 mapping from
# specs/1861-implement-cascade-trigger-logic was {"epic": 5, "feature": 5,
# "task": 4}; #3650 (merge SpecKit phases 3–5) superseded that by collapsing
# the plan/tasks/analyze phases into a single phase 3, making phase 3 the
# terminal phase for every hierarchy level.
FINAL_PHASE_BY_LEVEL: dict[str, int] = {"epic": 3, "feature": 3, "task": 3}


class IssueStateError(Exception):
    """Raised when the GitHub API returns a non-404 error for an issue lookup.

    Distinguishes transient/auth/network failures from a genuine 404 (deleted
    or never-existed issue).  Callers must treat this as a cascade-halting
    condition rather than silently skipping the affected child.
    """


class CascadeAction(Enum):
    """Possible cascade actions."""

    TRIGGERED = "triggered"
    SKIPPED = "skipped"
    NO_CHILDREN = "no_children"
    HALTED = "halted"
    CASCADE_COMPLETE = "cascade_complete"


@dataclass
class CascadeResult:
    """Result of a cascade trigger operation.

    Attributes:
        action: The action taken.
        event: The cascade event if a trigger was fired.
        comment: Comment text to post on the parent issue.
        skipped_issues: Issues skipped during cascade (closed, skip label, etc.).
    """

    action: CascadeAction
    event: CascadeEvent | None = None
    comment: str = ""
    skipped_issues: list[int] = field(default_factory=list)


# Label constants
_SPECKIT_LABEL = "speckit"
_SPECKIT_SKIP_LABEL = "speckit:skip"
_SPECKIT_FAILED_LABEL = "speckit:failed"

# Retry configuration (NFR-005): 3 retries = 4 total attempts, backoff 1s/2s/4s
_RETRY_MAX_ATTEMPTS = 4
_RETRY_BASE_DELAY = 1.0  # seconds

# Precise HTTP transient error detection — requires the literal "HTTP" prefix so that
# bare numeric tokens (e.g. issue numbers like 429 in URL paths) are never mistaken
# for transient HTTP responses.  Matches "HTTP 429", "HTTP 502", "HTTP 503"
# case-insensitively (gh CLI emits uppercase; IGNORECASE guards against edge cases).
_TRANSIENT_HTTP_PATTERN = re.compile(r"\bHTTP (429|502|503)\b", re.IGNORECASE)


class _RetryAfterError(RuntimeError):
    """RuntimeError subclass for transient HTTP 429/502/503 responses that carries a Retry-After delay (NFR-005).

    When ``_retry_api_call`` catches this exception it reads ``retry_after`` to
    determine the sleep duration rather than falling back to the exponential
    backoff schedule.  The ``retry_after`` value is only populated for 429
    responses that include a ``Retry-After`` header; for 502/503 the standard
    exponential schedule is used as a fallback.
    """

    def __init__(self, message: str, retry_after: float | None = None) -> None:
        super().__init__(message)
        self.retry_after = retry_after


class CascadeApiRetryExhaustedError(RuntimeError):
    """Raised when retries are exhausted for a cascade GitHub API operation."""


def _parse_retry_after(headers_text: str) -> float | None:
    """Parse the Retry-After value in seconds from ``gh api --include`` header output.

    Args:
        headers_text: Raw text returned by ``gh api --include`` (status line +
            headers + blank line + body).

    Returns:
        Retry delay in seconds, or ``None`` if the header is absent or non-numeric.
    """
    for line in headers_text.splitlines():
        if line.lower().startswith("retry-after:"):
            raw = line.split(":", 1)[1].strip()
            try:
                return float(raw)
            except ValueError:
                return None
    return None


def _retry_api_call(fn: Callable[[], _T], *, max_attempts: int = _RETRY_MAX_ATTEMPTS) -> _T:
    """Retry a callable with exponential backoff on transient failures.

    Retries on RuntimeError. When the exception is a ``_RetryAfterError`` and
    carries a ``retry_after`` value, that value overrides the exponential delay
    so that HTTP 429 ``Retry-After`` headers are honoured (NFR-005).

    Args:
        fn: Zero-argument callable to execute.
        max_attempts: Maximum number of attempts (default: 4). Must be positive.

    Returns:
        The return value of fn on success.

    Raises:
        ValueError: If max_attempts is not positive.
        RuntimeError: The last exception if all retries are exhausted.
    """
    if max_attempts <= 0:
        raise ValueError(f"max_attempts must be positive, got {max_attempts}")
    for attempt in range(max_attempts):
        try:
            return fn()
        except RuntimeError as exc:
            if attempt == max_attempts - 1:
                raise
            # NFR-005: honour Retry-After for transient responses when provided
            if isinstance(exc, _RetryAfterError) and exc.retry_after is not None:
                delay = exc.retry_after
            else:
                # Exponential backoff: 1s, 2s, … (delay = base * 2^attempt)
                delay = _RETRY_BASE_DELAY * (2**attempt)
            time.sleep(delay)
    # Unreachable — the loop always returns or raises. Satisfy type checker.
    raise RuntimeError("retry exhausted")  # pragma: no cover


class CascadeProcessor:
    """Processes cascade triggers between hierarchical issues.

    Args:
        owner: GitHub repository owner.
        repo: GitHub repository name.
    """

    def __init__(self, owner: str, repo: str) -> None:
        self.owner = owner
        self.repo = repo

    def _get_issue_state(self, issue_number: int) -> dict | None:
        """Get issue state via gh CLI.

        Returns:
            The parsed JSON dict on success, or ``None`` when the issue does
            not exist (HTTP 404 / "Not Found").

        Raises:
            IssueStateError: For any non-404 failure (transient network error,
                authentication failure, ``gh`` not found, malformed JSON, …).
                Callers must treat this as a cascade-halting condition.
        """
        try:
            result = run_safe(
                [
                    "gh",
                    "api",
                    f"repos/{self.owner}/{self.repo}/issues/{issue_number}",
                ],
                capture_output=True,
                text=True,
                shell=False,
            )
            if result.returncode != 0:
                stderr = result.stderr or ""
                if "404" in stderr or "Not Found" in stderr:
                    return None
                raise IssueStateError(f"gh API error for issue #{issue_number}: {stderr.strip() or '(empty stderr)'}")
            return json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise IssueStateError(f"Failed to parse gh API response for issue #{issue_number}: {exc}") from exc
        except FileNotFoundError as exc:
            raise IssueStateError(f"gh CLI not found while fetching issue #{issue_number}: {exc}") from exc

    def _issue_has_label(self, issue_data: dict, label_name: str) -> bool:
        """Check if an issue has a specific label."""
        labels = issue_data.get("labels", [])
        # GitHub REST API returns labels as objects with a "name" field.
        # Handle both dict (API response) and string (test/simplified) formats.
        return any((lbl.get("name") if isinstance(lbl, dict) else str(lbl)) == label_name for lbl in labels)

    def _apply_label(self, issue_number: int) -> bool:
        """Apply the speckit label to an issue via the Issues Labels API.

        Uses POST /repos/{owner}/{repo}/issues/{issue_number}/labels (FR-008).
        Passes ``--include`` to ``gh api`` so that response headers (including
        ``Retry-After``) are available in stdout for NFR-005 compliance.
        Wrapped with retry for transient failures (NFR-005).
        Returns True on success.

        Raises:
            CascadeApiRetryExhaustedError: When transient failures exhaust retry
                attempts. This is surfaced so workflow steps can fail and be
                retried by GitHub Actions (NFR-005).
        """

        def _do_apply() -> bool:
            try:
                result = run_safe(
                    [
                        "gh",
                        "api",
                        f"repos/{self.owner}/{self.repo}/issues/{issue_number}/labels",
                        "-X",
                        "POST",
                        "--input",
                        "-",
                        "--include",  # expose response headers so Retry-After can be parsed
                    ],
                    capture_output=True,
                    text=True,
                    shell=False,
                    input=json.dumps({"labels": [_SPECKIT_LABEL]}),
                )
                if result.returncode != 0:
                    stderr = result.stderr or ""
                    # Check for transient errors that should be retried
                    if _TRANSIENT_HTTP_PATTERN.search(stderr):
                        # NFR-005: honour Retry-After when provided by the server
                        retry_after = _parse_retry_after(result.stdout or "")
                        raise _RetryAfterError(
                            f"Transient error applying label: {stderr.strip()}",
                            retry_after=retry_after,
                        )
                    return False
                return True
            except FileNotFoundError:
                return False

        try:
            return _retry_api_call(_do_apply)
        except RuntimeError as exc:
            raise CascadeApiRetryExhaustedError(
                f"Retry exhausted applying `speckit` label to issue #{issue_number}: {str(exc)}",
            ) from exc

    def _post_comment(self, issue_number: int, body: str) -> bool:
        """Post a comment on an issue with retry. Returns True on success.

        Uses the REST comments endpoint via ``gh api`` with ``--include`` so
        ``Retry-After`` can be honored for HTTP 429 responses (NFR-005).

        Raises:
            CascadeApiRetryExhaustedError: When transient failures exhaust retry
                attempts for comment creation.
        """

        def _do_post() -> bool:
            try:
                result = run_safe(
                    [
                        "gh",
                        "api",
                        f"repos/{self.owner}/{self.repo}/issues/{issue_number}/comments",
                        "-X",
                        "POST",
                        "--input",
                        "-",
                        "--include",
                    ],
                    capture_output=True,
                    text=True,
                    shell=False,
                    input=json.dumps({"body": body}),
                )
                if result.returncode != 0:
                    stderr = result.stderr or ""
                    if _TRANSIENT_HTTP_PATTERN.search(stderr):
                        retry_after = _parse_retry_after(result.stdout or "")
                        raise _RetryAfterError(
                            f"Transient error posting comment: {stderr.strip()}",
                            retry_after=retry_after,
                        )
                    return False
                return True
            except FileNotFoundError:
                return False

        try:
            return _retry_api_call(_do_post)
        except RuntimeError as exc:
            raise CascadeApiRetryExhaustedError(
                f"Retry exhausted posting cascade comment to issue #{issue_number}: {str(exc)}",
            ) from exc

    def _find_eligible_child(
        self,
        children: list[ChildInfo],
        *,
        start_after: int | None = None,
    ) -> tuple[ChildInfo | None, list[int], int | None]:
        """Find the next eligible child, skipping closed/skip-labeled/deleted issues.

        Args:
            children: Ordered list of child entries.
            start_after: If provided, start searching after this issue number.

        Returns:
            Tuple of (eligible child or None, list of skipped issue numbers,
            failed_issue_number or None if halted by speckit:failed).

        Raises:
            IssueStateError: Propagated from ``_get_issue_state`` when the API
                returns a non-404 error.  The cascade must be halted in this
                case — do **not** silently skip the affected child.
        """
        skipped: list[int] = []
        found_start = start_after is None

        for child in children:
            if not found_start:
                if child.number == start_after:
                    found_start = True
                continue

            issue_data = self._get_issue_state(child.number)
            if issue_data is None:
                # Deleted issue (404)
                skipped.append(child.number)
                continue

            # Closed issue
            if issue_data.get("state") == "closed":
                skipped.append(child.number)
                continue

            # speckit:failed label — HALT (FR-004)
            if self._issue_has_label(issue_data, _SPECKIT_FAILED_LABEL):
                return (None, skipped, child.number)

            # speckit:skip label
            if self._issue_has_label(issue_data, _SPECKIT_SKIP_LABEL):
                skipped.append(child.number)
                continue

            # Already has speckit label (idempotency)
            if self._issue_has_label(issue_data, _SPECKIT_LABEL):
                skipped.append(child.number)
                continue

            return (child, skipped, None)

        return (None, skipped, None)

    def trigger_first_child(
        self,
        parent_number: int,
        hierarchy_yml_path: Path,
    ) -> CascadeResult:
        """Trigger the first eligible child after a parent completes its final phase.

        Args:
            parent_number: The parent issue number that completed.
            hierarchy_yml_path: Path to the parent's hierarchy.yml.

        Returns:
            CascadeResult describing the action taken.
        """
        try:
            metadata = read_hierarchy_yml(hierarchy_yml_path)
        except (FileNotFoundError, ValueError) as exc:
            comment = f"Could not read hierarchy metadata: {exc}"
            self._post_comment(parent_number, comment)
            return CascadeResult(
                action=CascadeAction.HALTED,
                comment=comment,
            )

        if not metadata.children:
            comment = "✅ **SpecKit cascade complete** — No further sub-issues to process."
            self._post_comment(parent_number, comment)
            return CascadeResult(
                action=CascadeAction.NO_CHILDREN,
                comment=comment,
            )

        # Sort children by order field if present
        sorted_children = self._sort_children_by_order(metadata.children)

        try:
            eligible, skipped, failed_issue = self._find_eligible_child(sorted_children)
        except IssueStateError as exc:
            comment = (
                f"⚠️ **SpecKit cascade halted** — Could not retrieve issue state "
                f"while searching for the first eligible child of #{parent_number}: "
                f"{exc}"
            )
            self._post_comment(parent_number, comment)
            return CascadeResult(
                action=CascadeAction.HALTED,
                comment=comment,
            )

        # FR-004: Halt on speckit:failed
        if failed_issue is not None:
            comment = (
                f"⚠️ **SpecKit cascade halted** — Cascade blocked by failed issue "
                f"#{failed_issue} (labeled `speckit:failed`). Manual intervention required."
            )
            # Post skip notice first if there were skips before the failure
            if skipped:
                skip_comment = self._build_skip_comment(skipped, target=None, exhausted=False)
                self._post_comment(parent_number, skip_comment)
            self._post_comment(parent_number, comment)
            return CascadeResult(
                action=CascadeAction.HALTED,
                comment=comment,
                skipped_issues=skipped,
            )

        if eligible is None:
            # All children were skipped
            if skipped:
                # Post skip notice with exhaustion wording
                skip_comment = self._build_skip_comment(skipped, target=None, exhausted=True)
                self._post_comment(parent_number, skip_comment)
            # Post completion comment (FR-006)
            comment = "✅ **SpecKit cascade complete** — No further sub-issues to process."
            self._post_comment(parent_number, comment)
            return CascadeResult(
                action=CascadeAction.CASCADE_COMPLETE,
                comment=comment,
                skipped_issues=skipped,
            )

        # Apply the speckit label
        if not self._apply_label(eligible.number):
            comment = (
                f"⚠️ **SpecKit cascade halted** — Failed to apply the `speckit` "
                f"label to child #{eligible.number}. Not triggering cascade."
            )
            self._post_comment(parent_number, comment)
            return CascadeResult(
                action=CascadeAction.HALTED,
                comment=comment,
                skipped_issues=skipped,
            )

        event = CascadeEvent(
            source_issue=parent_number,
            target_issue=eligible.number,
            direction=CascadeDirection.PARENT_TO_CHILD,
            skipped_issues=skipped,
        )

        # Post skip notice if there were skips (FR-005)
        if skipped:
            skip_comment = self._build_skip_comment(skipped, target=eligible.number)
            self._post_comment(parent_number, skip_comment)

        comment = (
            f"🚀 **SpecKit cascade**: Triggered `speckit` on child "
            f"#{eligible.number} ({eligible.title}).\n\n"
            f"_This comment was posted by the SpecKit cascade system._"
        )
        self._post_comment(parent_number, comment)

        return CascadeResult(
            action=CascadeAction.TRIGGERED,
            event=event,
            comment=comment,
            skipped_issues=skipped,
        )

    def trigger_next_sibling(
        self,
        completed_child: int,
        hierarchy_yml_path: Path,
        *,
        pipeline_failed: bool = False,
    ) -> CascadeResult:
        """Trigger the next eligible sibling after a child completes its final phase.

        Args:
            completed_child: The child issue that completed.
            hierarchy_yml_path: Path to the PARENT's hierarchy.yml.
            pipeline_failed: If True, halt cascade (FR-011).

        Returns:
            CascadeResult describing the action taken.
        """
        try:
            metadata = read_hierarchy_yml(hierarchy_yml_path)
        except (FileNotFoundError, ValueError) as exc:
            comment = f"Could not read hierarchy metadata: {exc}"
            dir_name = hierarchy_yml_path.parent.name
            numeric_prefix = dir_name.split("-", 1)[0]
            try:
                parent_for_comment = int(numeric_prefix)
            except ValueError:
                parent_for_comment = 0
            if parent_for_comment:
                self._post_comment(parent_for_comment, comment)
            return CascadeResult(
                action=CascadeAction.HALTED,
                comment=comment,
            )

        # Derive the parent issue number from the yml path directory name
        dir_name = hierarchy_yml_path.parent.name
        numeric_prefix = dir_name.split("-", 1)[0]
        try:
            parent_for_comment = int(numeric_prefix)
        except ValueError:
            parent_for_comment = metadata.parent if metadata.parent is not None else 0

        # FR-011: Halt on failure
        if pipeline_failed:
            comment = (
                f"⚠️ **SpecKit cascade halted** — Pipeline failed for #{completed_child}. Not triggering next sibling."
            )
            if parent_for_comment:
                self._post_comment(parent_for_comment, comment)
            return CascadeResult(
                action=CascadeAction.HALTED,
                comment=comment,
            )

        # Guard: completed_child must be in the children list.
        child_numbers = {c.number for c in metadata.children}
        if completed_child not in child_numbers:
            comment = (
                f"⚠️ **SpecKit cascade error** — #{completed_child} is not listed "
                f"as a child in the hierarchy metadata. "
                f"The child list may be stale or the wrong hierarchy.yml was passed."
            )
            if parent_for_comment:
                self._post_comment(parent_for_comment, comment)
            return CascadeResult(
                action=CascadeAction.HALTED,
                comment=comment,
            )

        # Sort children by order field if present
        sorted_children = self._sort_children_by_order(metadata.children)

        try:
            eligible, skipped, failed_issue = self._find_eligible_child(
                sorted_children,
                start_after=completed_child,
            )
        except IssueStateError as exc:
            comment = (
                f"⚠️ **SpecKit cascade halted** — Could not retrieve issue state "
                f"while searching for the next sibling of #{completed_child}: "
                f"{exc}"
            )
            if parent_for_comment:
                self._post_comment(parent_for_comment, comment)
            return CascadeResult(
                action=CascadeAction.HALTED,
                comment=comment,
            )

        # FR-004: Halt on speckit:failed
        if failed_issue is not None:
            comment = (
                f"⚠️ **SpecKit cascade halted** — Cascade blocked by failed issue "
                f"#{failed_issue} (labeled `speckit:failed`). Manual intervention required."
            )
            # Post skip notice first if there were skips before the failure
            if skipped:
                skip_comment = self._build_skip_comment(skipped, target=None, exhausted=False)
                self._post_comment(completed_child, skip_comment)
            self._post_comment(completed_child, comment)
            if parent_for_comment:
                self._post_comment(parent_for_comment, comment)
            return CascadeResult(
                action=CascadeAction.HALTED,
                comment=comment,
                skipped_issues=skipped,
            )

        if eligible is None:
            # All remaining siblings processed or skipped
            # Post skip notice if there were skips (FR-005 + FR-006 two-comment path)
            if skipped:
                skip_comment = self._build_skip_comment(skipped, target=None, exhausted=True)
                self._post_comment(completed_child, skip_comment)
            # Post completion comment on the completed task (FR-006)
            comment = "✅ **SpecKit cascade complete** — No further sub-issues to process."
            self._post_comment(completed_child, comment)
            # Post parent notification (FR-007)
            if parent_for_comment:
                parent_comment = "✅ All subtasks have completed SpecKit processing."
                self._post_comment(parent_for_comment, parent_comment)
            return CascadeResult(
                action=CascadeAction.CASCADE_COMPLETE,
                comment=comment,
                skipped_issues=skipped,
            )

        # Apply the speckit label
        if not self._apply_label(eligible.number):
            comment = (
                f"⚠️ **SpecKit cascade halted** — Failed to apply the `speckit` "
                f"label to sibling #{eligible.number}. Not triggering cascade."
            )
            if parent_for_comment:
                self._post_comment(parent_for_comment, comment)
            return CascadeResult(
                action=CascadeAction.HALTED,
                comment=comment,
                skipped_issues=skipped,
            )

        event = CascadeEvent(
            source_issue=completed_child,
            target_issue=eligible.number,
            direction=CascadeDirection.SIBLING_TO_SIBLING,
            skipped_issues=skipped,
        )

        # Post skip notice if there were skips (FR-005)
        if skipped:
            skip_comment = self._build_skip_comment(skipped, target=eligible.number)
            self._post_comment(completed_child, skip_comment)

        comment = (
            f"🚀 **SpecKit cascade**: Triggered `speckit` on sibling "
            f"#{eligible.number} ({eligible.title}) after "
            f"#{completed_child} completed.\n\n"
            f"_This comment was posted by the SpecKit cascade system._"
        )
        if parent_for_comment:
            self._post_comment(parent_for_comment, comment)

        return CascadeResult(
            action=CascadeAction.TRIGGERED,
            event=event,
            comment=comment,
            skipped_issues=skipped,
        )

    @staticmethod
    def _sort_children_by_order(children: list[ChildInfo]) -> list[ChildInfo]:
        """Sort children by order field.

        Children with an ``order`` value are sorted by that value.
        Children without an ``order`` value retain their relative order among
        themselves but are placed after all ordered children when at least one
        sibling has an ``order`` value.  When no children have an ``order``
        value the original list order is preserved unchanged.
        """
        # If any children have an order field, sort by it; otherwise keep original order
        if any(c.order is not None for c in children):
            return sorted(children, key=lambda c: c.order if c.order is not None else float("inf"))
        return children

    @staticmethod
    def _build_skip_comment(
        skipped_issues: list[int],
        target: int | None = None,
        *,
        exhausted: bool = False,
    ) -> str:
        """Build the informational skip comment (FR-005).

        Args:
            skipped_issues: List of skipped issue numbers.
            target: The issue that will be cascaded to (None if exhausted).
            exhausted: Whether all candidates were exhausted.

        Returns:
            Formatted skip comment string.
        """
        issues_text = ", ".join(f"#{n}" for n in skipped_issues)
        if target is not None:
            return (
                f"ℹ️ **Cascade Skip Notice** — Skipped issues {issues_text} "
                f"(not eligible for cascade). Cascading to #{target}."
            )
        if exhausted:
            return (
                f"ℹ️ **Cascade Skip Notice** — Skipped issues {issues_text} "
                f"(not eligible for cascade). No further cascade target remains."
            )
        return f"ℹ️ **Cascade Skip Notice** — Skipped issues {issues_text} (not eligible for cascade)."
