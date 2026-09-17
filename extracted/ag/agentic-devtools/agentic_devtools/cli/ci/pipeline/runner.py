"""Pipeline runner — executes actions sequentially with guard-blocking."""

from __future__ import annotations

import base64
import json
import logging
import os
import re
import sys
import zlib
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import TypedDict, cast

from agentic_devtools.cli.ci.logging_config import is_github_actions
from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.base import Action
from agentic_devtools.cli.ci.pipeline.diff_validation import validate_diff_preservation
from agentic_devtools.cli.ci.pipeline.models import (
    ActionDecision,
    ActionResult,
    PipelineRunSummary,
)
from agentic_devtools.cli.ci.pipeline.snapshot import (
    DerivedState,
    PRStateSnapshot,
    _supports_diff_fingerprint,
    build_pr_state_snapshot,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)
_CONFLICT_REPAIR_MARKER_RE = re.compile(r"<!-- agdt:conflict-repair:([0-9a-f]+):([0-9a-f]+):([^>]+) -->")
_CONFLICT_REPAIR_VALIDATED_MARKER_PREFIX = "<!-- agdt:conflict-repair-validated:"
_CONFLICT_REPAIR_VALIDATED_MARKER_RE = re.compile(r"<!-- agdt:conflict-repair-validated:([0-9a-f]+) -->")
_DIFF_PRESERVATION_BLOCKER_PREFIX = "<!-- agdt:diff-preservation-blocker:"
_DIFF_PRESERVATION_BLOCKER_RE = re.compile(r"<!-- agdt:diff-preservation-blocker:([A-Za-z0-9_-]+) -->")
_MAX_ISSUE_COMMENT_LENGTH = 65_536
_DIFF_PRESERVATION_BLOCKER_CLEARED_PREFIX = "<!-- agdt:diff-preservation-blocker-cleared:"
_DIFF_PRESERVATION_BLOCKER_CLEARED_RE = re.compile(r"<!-- agdt:diff-preservation-blocker-cleared:([0-9a-f]+) -->")


class _RequiredDiffPreservationBlocker(TypedDict):
    """Required fields shared by persisted diff-preservation blockers."""

    baseline_head: str
    baseline_files: list[str]
    baseline_hash: str
    baseline_hash_available: bool
    fingerprint_supported: bool
    allow_file_removal: bool
    intentional_noop: bool


class DiffPreservationBlocker(_RequiredDiffPreservationBlocker, total=False):
    """Persisted baseline required to re-check a dropped-diff mutation across runs."""

    allowed_removed_files: list[str]


class _ConflictRepairDiffPreservationBlocker(DiffPreservationBlocker, total=False):
    conflict_repair: bool


class DiffPreservationBlockerLookupError(RuntimeError):
    """Raised when an authenticated persisted blocker cannot be inspected."""


def _parse_canonical_conflict_repair_marker(body: str) -> re.Match[str] | None:
    """Return the canonical dispatch marker when it is the final standalone line."""
    last_line = body.rstrip("\r\n").splitlines()[-1] if body else ""
    if not last_line:
        return None
    return _CONFLICT_REPAIR_MARKER_RE.fullmatch(last_line)


def _parse_canonical_validated_marker(body: str) -> re.Match[str] | None:
    """Return the canonical validated marker when it is the full comment body."""
    return _CONFLICT_REPAIR_VALIDATED_MARKER_RE.fullmatch(body.rstrip("\r\n"))


def _describe_snapshot_invalidation_skip(action_name: str, invalidated_by: str) -> tuple[str, str]:
    """Return user-facing details and log text for a snapshot invalidation skip."""
    if invalidated_by == "publish" and action_name in {"squash", "rebase"}:
        return (
            "No longer applicable after 'publish' in this run: "
            "pre-publish branch preparation invalidated the PR snapshot; rerun required",
            "superseded by 'publish' via pre-publish branch preparation; PR snapshot invalidated",
        )
    return (
        f"Pipeline halted: '{invalidated_by}' changed PR HEAD; rerun required",
        f"halted by snapshot invalidation in '{invalidated_by}'",
    )


def _log_group(title: str) -> None:
    """Emit a ::group:: annotation when running in GitHub Actions."""
    if is_github_actions():
        print(f"::group::{title}", file=sys.stderr, flush=True)


def _log_endgroup() -> None:
    """Emit an ::endgroup:: annotation when running in GitHub Actions."""
    if is_github_actions():
        print("::endgroup::", file=sys.stderr, flush=True)


def _get_run_url() -> str:
    """Build the GitHub Actions run URL from environment variables."""
    server_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    if repository and run_id:
        return f"{server_url}/{repository}/actions/runs/{run_id}"
    return ""


def _find_recent_conflict_repair_head(
    provider: CIPlatformProvider,
    pr_number: int,
    current_head_sha: str,
) -> str:
    """Return the pre-repair head SHA from the latest unconsumed repair marker.

    Returns an empty string when no trusted dispatch marker is present, the latest
    trusted marker records that the repair output was already validated, or the
    marker targets the current head.

    Raises:
        DiffPreservationBlockerLookupError: If an implemented provider identity lookup
            fails or returns an unusable identity.
    """

    dispatch_login = ""
    get_pr_token_login = getattr(provider, "get_pr_token_login", None)
    if callable(get_pr_token_login):
        if getattr(get_pr_token_login, "__func__", None) is CIPlatformProvider.get_pr_token_login:
            return ""
        try:
            login = get_pr_token_login()
        except Exception as exc:
            if getattr(type(provider), "get_pr_token_login", None) is None:
                return ""
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            raise DiffPreservationBlockerLookupError("failed to resolve authenticated blocker identity") from exc
        if isinstance(login, str):
            dispatch_login = login
        elif getattr(type(provider), "get_pr_token_login", None) is None:
            return ""
        else:
            raise DiffPreservationBlockerLookupError("authenticated blocker identity is unusable")
        if not dispatch_login:
            raise DiffPreservationBlockerLookupError("authenticated blocker identity is empty")

    if dispatch_login:
        comments = provider.list_issue_comments(pr_number)
        latest_dispatch: IssueCommentInfo | None = None
        latest_validated: IssueCommentInfo | None = None
        for comment in comments:
            if comment.author != dispatch_login:
                continue
            validated_match = _parse_canonical_validated_marker(comment.body)
            if validated_match is not None:
                if latest_validated is None or comment.id > latest_validated.id:
                    latest_validated = comment
                continue
            if _parse_canonical_conflict_repair_marker(comment.body) is not None and (
                latest_dispatch is None or comment.id > latest_dispatch.id
            ):
                latest_dispatch = comment
        if latest_validated is not None and (latest_dispatch is None or latest_validated.id > latest_dispatch.id):
            return ""
        if latest_dispatch is None:
            return ""
        comment_body = latest_dispatch.body
    else:
        return ""
    marker = cast(re.Match[str], _parse_canonical_conflict_repair_marker(comment_body))
    marker_head = marker.group(2)
    if marker_head == current_head_sha:
        return ""
    timestamp_raw = marker.group(3).strip()
    try:
        datetime.fromisoformat(timestamp_raw.replace("Z", "+00:00"))
    except ValueError:
        return ""
    return marker_head


def _persist_conflict_repair_validation(
    provider: CIPlatformProvider,
    pr_number: int,
    validated_head_sha: str,
) -> bool:
    """Record that the repaired HEAD was validated so later runs consume the baseline."""
    try:
        live_metadata = provider.get_pr_metadata(pr_number)
    except Exception as exc:
        if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
            raise
        logger.warning(
            "PR #%d: Failed to verify live HEAD before persisting validated conflict-repair baseline for %s: %s",
            pr_number,
            validated_head_sha[:8],
            str(exc)[:200],
        )
        return False
    live_head_sha = getattr(live_metadata, "head_sha", "")
    if not isinstance(live_head_sha, str) or not live_head_sha:
        logger.warning(
            "PR #%d: Skipping validated conflict-repair baseline for %s; live HEAD could not be confirmed",
            pr_number,
            validated_head_sha[:8],
        )
        return False
    if live_head_sha != validated_head_sha:
        logger.warning(
            "PR #%d: Skipping validated conflict-repair baseline for stale HEAD %s; live HEAD is %s",
            pr_number,
            validated_head_sha[:8],
            live_head_sha[:8],
        )
        return False
    marker = f"{_CONFLICT_REPAIR_VALIDATED_MARKER_PREFIX}{validated_head_sha} -->"
    try:
        provider.post_comment_as_pr_token(pr_number, marker)
    except Exception as exc:
        if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
            raise
        logger.warning(
            "PR #%d: Failed to persist validated conflict-repair baseline for %s: %s",
            pr_number,
            validated_head_sha[:8],
            str(exc)[:200],
        )
        return False
    return True


def _find_recent_diff_preservation_blocker(
    provider: CIPlatformProvider,
    pr_number: int,
) -> DiffPreservationBlocker | None:
    """Return the latest unconsumed trusted diff-preservation blocker payload."""

    def _parse_blocker(body: str) -> DiffPreservationBlocker | None:
        match = cast(re.Match[str], _DIFF_PRESERVATION_BLOCKER_RE.search(body.rstrip("\r\n")))
        encoded = match.group(1)
        padding = "=" * (-len(encoded) % 4)
        try:
            raw_payload = base64.urlsafe_b64decode(f"{encoded}{padding}".encode())
            try:
                decoded = zlib.decompress(raw_payload).decode("utf-8")
            except zlib.error:
                decoded = raw_payload.decode("utf-8")
            payload = json.loads(decoded)
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
            return None
        if not isinstance(payload, dict):
            return None
        baseline_head = payload.get("baseline_head")
        baseline_files = payload.get("baseline_files")
        baseline_hash = payload.get("baseline_hash")
        baseline_hash_available = payload.get("baseline_hash_available")
        fingerprint_supported = payload.get("fingerprint_supported")
        allow_file_removal = payload.get("allow_file_removal", False)
        allowed_removed_files = payload.get("allowed_removed_files", [])
        intentional_noop = payload.get("intentional_noop", False)
        conflict_repair = payload.get("conflict_repair", False)
        if not isinstance(baseline_head, str) or not baseline_head:
            return None
        if not isinstance(baseline_files, list) or not all(isinstance(path, str) and path for path in baseline_files):
            return None
        if not isinstance(baseline_hash, str):
            return None
        if not isinstance(baseline_hash_available, bool):
            return None
        if not isinstance(fingerprint_supported, bool):
            return None
        if (
            not isinstance(allow_file_removal, bool)
            or not isinstance(allowed_removed_files, list)
            or not all(isinstance(path, str) and path for path in allowed_removed_files)
            or not isinstance(intentional_noop, bool)
            or not isinstance(conflict_repair, bool)
        ):
            return None
        parsed: _ConflictRepairDiffPreservationBlocker = {
            "baseline_head": baseline_head,
            "baseline_files": cast(list[str], baseline_files),
            "baseline_hash": baseline_hash,
            "baseline_hash_available": baseline_hash_available,
            "fingerprint_supported": fingerprint_supported,
            "allow_file_removal": allow_file_removal,
            "intentional_noop": intentional_noop,
        }
        if "allowed_removed_files" in payload:
            parsed["allowed_removed_files"] = allowed_removed_files
        if conflict_repair:
            parsed["conflict_repair"] = True
        return cast(DiffPreservationBlocker, parsed)

    dispatch_login = ""
    get_pr_token_login = getattr(provider, "get_pr_token_login", None)
    if callable(get_pr_token_login):
        if getattr(get_pr_token_login, "__func__", None) is CIPlatformProvider.get_pr_token_login:
            return None
        try:
            login = get_pr_token_login()
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            raise DiffPreservationBlockerLookupError("failed to resolve authenticated blocker identity") from exc
        if isinstance(login, str):
            dispatch_login = login
        else:
            if getattr(type(provider), "get_pr_token_login", None) is None:
                return None
            raise DiffPreservationBlockerLookupError("authenticated blocker identity is unusable")
        if not dispatch_login:
            raise DiffPreservationBlockerLookupError("authenticated blocker identity is empty")

    if dispatch_login:
        trusted_comments = [
            comment for comment in provider.list_issue_comments(pr_number) if comment.author == dispatch_login
        ]
        latest_cleared_id = max(
            (
                comment.id
                for comment in trusted_comments
                if _DIFF_PRESERVATION_BLOCKER_CLEARED_RE.search(comment.body.rstrip("\r\n")) is not None
            ),
            default=0,
        )
        candidate_blockers = sorted(
            (
                comment
                for comment in trusted_comments
                if comment.id > latest_cleared_id
                and _DIFF_PRESERVATION_BLOCKER_RE.search(comment.body.rstrip("\r\n")) is not None
            ),
            key=lambda comment: comment.id,
            reverse=True,
        )
        if candidate_blockers:
            parsed = _parse_blocker(candidate_blockers[0].body)
            if parsed is None:
                raise DiffPreservationBlockerLookupError("latest authenticated diff-preservation blocker is invalid")
            return parsed
        return None

    return None


def run_pipeline(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    actions: Sequence[Action],
    *,
    actionable_check_names: frozenset[str] | None = None,
) -> PipelineRunSummary:
    """Execute the action pipeline sequentially.

    Each action is evaluated against the current state. If Guards (action 0)
    returns BLOCKED, all subsequent actions are marked BLOCKED_BY_GUARD.

    Args:
        provider: CI platform provider for API interactions.
        snapshot: Immutable PR state snapshot.
        actions: Ordered actions to evaluate and execute.
        actionable_check_names: Optional set of check run names to evaluate. Must be
            the same value used to build ``snapshot`` so that the post-invalidation
            refresh derives ``ci_status`` from an identical check set; ``None`` means
            the snapshot builder's default set.

    Returns:
        PipelineRunSummary with all action results.
    """
    current_snapshot = snapshot
    derived = DerivedState(current_snapshot)
    derived.set("provider", provider)
    results: list[ActionResult] = []
    guard_blocked = False
    guard_block_reason = ""
    # Name of the first side-effecting action that returned FAILED; empty when none.
    exec_failed_by = ""
    snapshot_invalidated_by = ""
    invalidation_preserves_diff_fingerprint = False
    invalidation_intentional_noop = False
    # False whenever an invalidation has been observed but not yet refreshed against.
    # Re-armed (set back to False) by every NEW invalidation so that a second
    # invalidation in the same run cannot be served by the earlier refresh.
    refreshed_after_invalidation = False
    persist_conflict_repair_validation = False
    conflict_repair_validation_persisted = True
    clear_diff_preservation_blocker = False
    clear_diff_preservation_blocker_allow_stale_head = False
    diff_preservation_blocker_persisted = False
    persisted_diff_preservation_allows_file_removal = False
    persisted_diff_preservation_allowed_removed_files: tuple[str, ...] = ()
    pre_mutation_intentional_noop = False
    invalidation_allows_file_removal = False
    invalidation_allowed_removed_files: tuple[str, ...] = ()
    try:
        persisted_diff_preservation_blocker = _find_recent_diff_preservation_blocker(
            provider,
            current_snapshot.pr_number,
        )
    except DiffPreservationBlockerLookupError as exc:
        persisted_diff_preservation_blocker = None
        guard_blocked = True
        guard_block_reason = (
            f"PR #{current_snapshot.pr_number}: persisted post-mutation diff validation unavailable ({exc})"
        )
        logger.error(guard_block_reason)
    pre_repair_head_sha = ""
    persisted_conflict_repair_baseline = bool(
        persisted_diff_preservation_blocker is not None
        and persisted_diff_preservation_blocker.get("conflict_repair", False)
    )
    if persisted_diff_preservation_blocker is not None:
        persisted_baseline_hash = persisted_diff_preservation_blocker["baseline_hash"]
        persisted_baseline_hash_available = persisted_diff_preservation_blocker["baseline_hash_available"]
        if not persisted_baseline_hash_available and persisted_diff_preservation_blocker["fingerprint_supported"]:
            compute_diff_hash = getattr(provider, "compute_diff_hash", None)
            if callable(compute_diff_hash):
                try:
                    recovered_hash = compute_diff_hash(
                        base_branch=current_snapshot.base_branch,
                        sha=persisted_diff_preservation_blocker["baseline_head"],
                    )
                    if isinstance(recovered_hash, str) and recovered_hash:
                        persisted_baseline_hash = recovered_hash
                        persisted_baseline_hash_available = True
                    elif recovered_hash == "":
                        logger.warning(
                            "PR #%d: Ignoring empty persisted baseline fingerprint for %s",
                            current_snapshot.pr_number,
                            persisted_diff_preservation_blocker["baseline_head"][:8],
                        )
                except Exception as exc:
                    if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                        raise
                    logger.warning(
                        "PR #%d: Failed to recompute persisted baseline fingerprint for %s: %s",
                        current_snapshot.pr_number,
                        persisted_diff_preservation_blocker["baseline_head"][:8],
                        str(exc)[:200],
                    )
        persisted_check = validate_diff_preservation(
            pre_files=persisted_diff_preservation_blocker["baseline_files"],
            post_files=current_snapshot.files,
            pre_hash=persisted_baseline_hash,
            post_hash=current_snapshot.diff_hash,
            pre_hash_available=persisted_baseline_hash_available,
            post_hash_available=current_snapshot.diff_hash_available,
            fingerprint_supported=persisted_diff_preservation_blocker["fingerprint_supported"],
            intentional_noop=persisted_diff_preservation_blocker["intentional_noop"],
            allow_file_removal=persisted_diff_preservation_blocker["allow_file_removal"],
            allowed_removed_files=persisted_diff_preservation_blocker.get("allowed_removed_files", []),
        )
        if not persisted_check.valid:
            missing = ", ".join(persisted_check.missing_files) or "<none>"
            guard_blocked = True
            guard_block_reason = (
                f"PR #{current_snapshot.pr_number}: persisted post-mutation diff validation blocked "
                f"(pre-mutation HEAD={persisted_diff_preservation_blocker['baseline_head']}, "
                f"current HEAD={current_snapshot.head_sha}, base={current_snapshot.base_branch}, "
                f"changed-file count={len(current_snapshot.files)}, missing files={missing}; "
                f"{persisted_check.reason})"
            )
            logger.error(guard_block_reason)
        else:
            conflict_repair_still_pending = (
                persisted_conflict_repair_baseline
                and current_snapshot.head_sha == persisted_diff_preservation_blocker["baseline_head"]
            )
            if not conflict_repair_still_pending:
                clear_diff_preservation_blocker = True
                if persisted_conflict_repair_baseline:
                    persist_conflict_repair_validation = True
    if not persisted_conflict_repair_baseline:
        try:
            pre_repair_head_sha = _find_recent_conflict_repair_head(
                provider,
                current_snapshot.pr_number,
                current_snapshot.head_sha,
            )
        except DiffPreservationBlockerLookupError as exc:
            pre_repair_head_sha = ""
            guard_blocked = True
            guard_block_reason = (
                f"PR #{current_snapshot.pr_number}: conflict-repair diff validation unavailable ({exc})"
            )
            logger.error(guard_block_reason)
    if pre_repair_head_sha:
        pre_repair_hash = ""
        pre_repair_hash_available = False
        pre_repair_fingerprint_supported = _supports_diff_fingerprint(provider)
        pre_repair_files: list[str] | None = None
        compute_diff_hash = getattr(provider, "compute_diff_hash", None)
        if pre_repair_fingerprint_supported and callable(compute_diff_hash):
            try:
                baseline_hash = compute_diff_hash(
                    base_branch=current_snapshot.base_branch,
                    sha=pre_repair_head_sha,
                    base_sha=current_snapshot.base_sha,
                )
                if isinstance(baseline_hash, str) and baseline_hash:
                    pre_repair_hash = baseline_hash
                    pre_repair_hash_available = True
                elif baseline_hash == "":
                    logger.warning(
                        "PR #%d: Ignoring empty pre-repair fingerprint for %s",
                        current_snapshot.pr_number,
                        pre_repair_head_sha[:8],
                    )
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.warning(
                    "PR #%d: Failed to compute pre-repair fingerprint for %s: %s",
                    current_snapshot.pr_number,
                    pre_repair_head_sha[:8],
                    str(exc)[:200],
                )
        compute_diff_files = getattr(provider, "compute_diff_files", None)
        if callable(compute_diff_files):
            try:
                baseline_files_result = compute_diff_files(
                    base_branch=current_snapshot.base_branch,
                    sha=pre_repair_head_sha,
                    base_sha=current_snapshot.base_sha,
                )
                if isinstance(baseline_files_result, list):
                    pre_repair_files = [path for path in baseline_files_result if isinstance(path, str) and path]
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.warning(
                    "PR #%d: Failed to compute pre-repair file inventory for %s: %s",
                    current_snapshot.pr_number,
                    pre_repair_head_sha[:8],
                    str(exc)[:200],
                )
        if pre_repair_files is None and not (
            pre_repair_hash_available and current_snapshot.diff_hash_available and pre_repair_fingerprint_supported
        ):
            guard_blocked = True
            guard_block_reason = (
                f"PR #{current_snapshot.pr_number}: post-repair diff validation blocked "
                f"(pre-repair HEAD={pre_repair_head_sha}, post-repair HEAD={current_snapshot.head_sha}, "
                f"base={current_snapshot.base_branch}, changed-file count={len(current_snapshot.files)}, "
                "missing files=<unavailable>; pre-repair file inventory unavailable)"
            )
            logger.error(guard_block_reason)
            pre_repair_head_sha = ""
        baseline_files = (
            pre_repair_files if pre_repair_files is not None else (current_snapshot.files or ["<pre-repair-diff>"])
        )
        if pre_repair_head_sha:
            cross_run_check = validate_diff_preservation(
                pre_files=baseline_files,
                post_files=current_snapshot.files,
                pre_hash=pre_repair_hash,
                post_hash=current_snapshot.diff_hash,
                pre_hash_available=pre_repair_hash_available,
                post_hash_available=current_snapshot.diff_hash_available,
                fingerprint_supported=pre_repair_fingerprint_supported or current_snapshot.diff_hash_supported,
                intentional_noop=False,
            )
            if not cross_run_check.valid:
                missing = ", ".join(cross_run_check.missing_files) or "<none>"
                guard_blocked = True
                guard_block_reason = (
                    f"PR #{current_snapshot.pr_number}: post-repair diff validation blocked "
                    f"(pre-repair HEAD={pre_repair_head_sha}, post-repair HEAD={current_snapshot.head_sha}, "
                    f"base={current_snapshot.base_branch}, changed-file count={len(current_snapshot.files)}, "
                    f"missing files={missing}; {cross_run_check.reason})"
                )
                logger.error(guard_block_reason)
            else:
                persist_conflict_repair_validation = True

    def _persist_diff_preservation_blocker(
        pre_mutation_snapshot: PRStateSnapshot,
        *,
        expected_live_head: str | None = None,
        fingerprint_supported_override: bool | None = None,
        conflict_repair: bool = False,
        allowed_removed_files: Sequence[str] = (),
    ) -> bool:
        nonlocal persisted_diff_preservation_allows_file_removal
        nonlocal persisted_diff_preservation_allowed_removed_files
        try:
            live_metadata = provider.get_pr_metadata(current_snapshot.pr_number)
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.warning(
                "PR #%d: Failed to verify live HEAD before persisting diff-preservation blocker for %s: %s",
                current_snapshot.pr_number,
                pre_mutation_snapshot.head_sha[:8],
                str(exc)[:200],
            )
            return False
        live_head_sha = getattr(live_metadata, "head_sha", "")
        if not isinstance(live_head_sha, str) or not live_head_sha:
            logger.warning(
                "PR #%d: Skipping diff-preservation blocker for %s; live HEAD could not be confirmed",
                current_snapshot.pr_number,
                pre_mutation_snapshot.head_sha[:8],
            )
            return False
        expected_head = expected_live_head or pre_mutation_snapshot.head_sha
        if live_head_sha != expected_head:
            logger.warning(
                "PR #%d: Skipping diff-preservation blocker for unexpected HEAD %s; live HEAD is %s",
                current_snapshot.pr_number,
                expected_head[:8],
                live_head_sha[:8],
            )
            return False
        payload = {
            "baseline_head": pre_mutation_snapshot.head_sha,
            "baseline_files": pre_mutation_snapshot.files,
            "baseline_hash": pre_mutation_snapshot.diff_hash,
            "baseline_hash_available": pre_mutation_snapshot.diff_hash_available,
            "fingerprint_supported": (
                fingerprint_supported_override
                if fingerprint_supported_override is not None
                else (
                    invalidation_preserves_diff_fingerprint
                    and pre_mutation_snapshot.diff_hash_supported
                    and current_snapshot.diff_hash_supported
                )
            ),
            "allow_file_removal": invalidation_allows_file_removal,
            "allowed_removed_files": list(allowed_removed_files),
            "intentional_noop": invalidation_intentional_noop,
        }
        if conflict_repair:
            payload["conflict_repair"] = True
        compressed = zlib.compress(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode(), level=9)
        encoded = base64.urlsafe_b64encode(compressed).decode().rstrip("=")
        marker = f"{_DIFF_PRESERVATION_BLOCKER_PREFIX}{encoded} -->"
        if len(marker) > _MAX_ISSUE_COMMENT_LENGTH:
            logger.warning(
                "PR #%d: Skipping diff-preservation blocker for %s; marker exceeds GitHub's issue-comment limit",
                current_snapshot.pr_number,
                pre_mutation_snapshot.head_sha[:8],
            )
            return False
        persisted_in_summary = False
        from agentic_devtools.cli.ci.pipeline.summary import _find_active_summary_comment

        summary_comment = _find_active_summary_comment(provider, current_snapshot.pr_number)
        if summary_comment is not None:
            summary_id, summary_body = summary_comment
            if _DIFF_PRESERVATION_BLOCKER_PREFIX in summary_body:
                updated_body = _DIFF_PRESERVATION_BLOCKER_RE.sub(marker, summary_body)
            else:
                updated_body = f"{summary_body}\n\n{marker}"
            provider.update_comment(summary_id, updated_body)
            persisted_in_summary = True

        if not persisted_in_summary:
            try:
                provider.post_comment_as_pr_token(current_snapshot.pr_number, marker)
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.warning(
                    "PR #%d: Failed to persist diff-preservation blocker for %s: %s",
                    current_snapshot.pr_number,
                    current_snapshot.head_sha[:8],
                    str(exc)[:200],
                )
                return False
        persisted_diff_preservation_allows_file_removal = invalidation_allows_file_removal
        persisted_diff_preservation_allowed_removed_files = tuple(sorted(allowed_removed_files))
        return True

    def _clear_persisted_diff_preservation_blocker(*, allow_stale_head: bool = False) -> None:
        try:
            live_metadata = provider.get_pr_metadata(current_snapshot.pr_number)
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.warning(
                "PR #%d: Failed to verify live HEAD before clearing diff-preservation blocker for %s: %s",
                current_snapshot.pr_number,
                current_snapshot.head_sha[:8],
                str(exc)[:200],
            )
            return
        live_head_sha = getattr(live_metadata, "head_sha", "")
        if not isinstance(live_head_sha, str) or not live_head_sha:
            logger.warning(
                "PR #%d: Skipping diff-preservation blocker clear for %s; live HEAD could not be confirmed",
                current_snapshot.pr_number,
                current_snapshot.head_sha[:8],
            )
            return
        if live_head_sha != current_snapshot.head_sha and not allow_stale_head:
            logger.warning(
                "PR #%d: Skipping diff-preservation blocker clear for stale HEAD %s; live HEAD is %s",
                current_snapshot.pr_number,
                current_snapshot.head_sha[:8],
                live_head_sha[:8],
            )
            return

        cleared_in_summary = False
        from agentic_devtools.cli.ci.pipeline.summary import _find_active_summary_comment

        summary_comment = _find_active_summary_comment(provider, current_snapshot.pr_number)
        if summary_comment is not None and _DIFF_PRESERVATION_BLOCKER_PREFIX in summary_comment[1]:
            summary_id, summary_body = summary_comment
            cleaned_body = _DIFF_PRESERVATION_BLOCKER_RE.sub("", summary_body).rstrip()
            provider.update_comment(summary_id, cleaned_body)
            cleared_in_summary = True

        # Delete any standalone blocker comments or cleared comments on this PR
        for c in provider.list_issue_comments(current_snapshot.pr_number):
            c_body = (c.body or "").strip()
            if _DIFF_PRESERVATION_BLOCKER_RE.fullmatch(c_body) or _DIFF_PRESERVATION_BLOCKER_CLEARED_RE.fullmatch(
                c_body
            ):
                provider.delete_comment(c.id)

        if not cleared_in_summary:
            marker = f"{_DIFF_PRESERVATION_BLOCKER_CLEARED_PREFIX}{live_head_sha} -->"
            try:
                provider.post_comment_as_pr_token(current_snapshot.pr_number, marker)
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.warning(
                    "PR #%d: Failed to clear diff-preservation blocker for %s: %s",
                    current_snapshot.pr_number,
                    current_snapshot.head_sha[:8],
                    str(exc)[:200],
                )

    def _refresh_snapshot_after_invalidation() -> str | None:
        """Refresh and validate the PR snapshot after a mutating action."""
        nonlocal current_snapshot
        nonlocal derived
        nonlocal guard_blocked
        nonlocal guard_block_reason
        nonlocal refreshed_after_invalidation
        nonlocal clear_diff_preservation_blocker
        nonlocal clear_diff_preservation_blocker_allow_stale_head
        nonlocal diff_preservation_blocker_persisted
        nonlocal persisted_diff_preservation_allows_file_removal
        nonlocal persisted_diff_preservation_allowed_removed_files

        try:
            exclusion_context = derived.get("exclusion_context")
            pre_mutation_snapshot = current_snapshot
            # Run-scoped flag set by SquashAction when a tree-preserving squash
            # executed this run after green CI. Carry it across the
            # post-invalidation refresh so RequestReviewAction can relax its
            # ci_passing gate on the new squashed HEAD (whose checks have not
            # re-reported yet). Consumed ONLY by RequestReviewAction — approve
            # and merge lack runs_after_invalidation and are halted this run.
            #
            # The flag is only restored when the refreshed head_sha matches
            # the exact post-squash commit SHA recorded by SquashAction. A
            # concurrent push after squash_post_repair but before the snapshot
            # refresh would move the PR to a different HEAD, which would not
            # match; the mismatch causes the flag to be withheld so that
            # RequestReviewAction fails closed and defers to fresh CI.
            #
            # The recorded post-squash SHA is not carried into the refreshed
            # derived state, so a re-armed second refresh (triggered by a later
            # invalidation, which moves HEAD again) always drops the flag and
            # falls back to the real CI gate.
            squash_preserved_green = derived.get("squash_preserved_green", False)
            squash_preserved_green_sha = derived.get("squash_preserved_green_sha", "")
            # Run-scoped flag set by ApplySuggestionsAction (which also invalidates
            # the snapshot). It records that autofix ran in THIS iteration, which is
            # independent of the PR HEAD, so it must survive the refresh for
            # ResolveThreadsAction to skip its (token-expensive) SDK evaluation.
            autofix_applied = derived.get("autofix_applied_this_iteration", False)
            current_snapshot = build_pr_state_snapshot(
                provider,
                current_snapshot.pr_number,
                actionable_check_names=actionable_check_names,
            )
            derived = DerivedState(current_snapshot)
            fingerprint_supported = (
                invalidation_preserves_diff_fingerprint
                and pre_mutation_snapshot.diff_hash_supported
                and current_snapshot.diff_hash_supported
            )
            diff_check = validate_diff_preservation(
                pre_mutation_snapshot.files,
                current_snapshot.files,
                pre_hash=pre_mutation_snapshot.diff_hash,
                post_hash=current_snapshot.diff_hash,
                pre_hash_available=pre_mutation_snapshot.diff_hash_available,
                post_hash_available=current_snapshot.diff_hash_available,
                fingerprint_supported=fingerprint_supported,
                intentional_noop=invalidation_intentional_noop,
                allow_file_removal=invalidation_allows_file_removal,
                allowed_removed_files=invalidation_allowed_removed_files,
            )
            if not diff_check.valid:
                missing = ", ".join(diff_check.missing_files) or "<none>"
                diagnostic = (
                    f"PR #{current_snapshot.pr_number}: post-mutation diff validation blocked "
                    f"(pre-mutation HEAD={pre_mutation_snapshot.head_sha}, "
                    f"post-mutation HEAD={current_snapshot.head_sha}, "
                    f"base={current_snapshot.base_branch}, changed-file count={len(current_snapshot.files)}, "
                    f"missing files={missing}; {diff_check.reason})"
                )
                logger.error(diagnostic)
                guard_blocked = True
                guard_block_reason = diagnostic
                if not diff_preservation_blocker_persisted:
                    diff_preservation_blocker_persisted = _persist_diff_preservation_blocker(
                        pre_mutation_snapshot,
                        allowed_removed_files=invalidation_allowed_removed_files,
                    )
            elif (
                diff_preservation_blocker_persisted
                and (
                    invalidation_intentional_noop != pre_mutation_intentional_noop
                    or persisted_diff_preservation_allows_file_removal != invalidation_allows_file_removal
                    or persisted_diff_preservation_allowed_removed_files != invalidation_allowed_removed_files
                )
                and not _persist_diff_preservation_blocker(
                    pre_mutation_snapshot,
                    expected_live_head=current_snapshot.head_sha,
                    allowed_removed_files=invalidation_allowed_removed_files,
                )
            ):
                logger.warning(  # pragma: no cover
                    "PR #%d: Failed to persist the final diff-preservation policy after refresh",
                    current_snapshot.pr_number,
                )
            clear_diff_preservation_blocker = diff_preservation_blocker_persisted
            if exclusion_context is not None:
                derived.set("exclusion_context", exclusion_context)
            if autofix_applied:
                derived.set("autofix_applied_this_iteration", True)
            if (
                squash_preserved_green
                and squash_preserved_green_sha
                and current_snapshot.head_sha == squash_preserved_green_sha
            ):
                derived.set("squash_preserved_green", True)
            refreshed_after_invalidation = True
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.error(
                "Failed to refresh snapshot after invalidation by '%s': %s",
                snapshot_invalidated_by,
                exc,
            )
            return str(exc)
        return None

    for action in actions:
        action_name = action.name
        _log_group(f"Action: {action_name}")

        if guard_blocked:
            result = ActionResult(
                name=action_name,
                decision=ActionDecision.BLOCKED_BY_GUARD,
                details=f"Blocked by guards: {guard_block_reason}",
            )
            logger.info(
                "Action '%s': BLOCKED_BY_GUARD (reason: %s)",
                action_name,
                guard_block_reason,
            )
            results.append(result)
            _log_endgroup()
            continue

        # If a prior side-effecting action failed, skip this action entirely
        # (including evaluation) unless it explicitly opts into recovery work.
        if exec_failed_by and not getattr(action, "runs_on_prior_failure", False):
            result = ActionResult(
                name=action_name,
                decision=ActionDecision.SKIP,
                details=f"Pipeline halted: '{exec_failed_by}' failed",
            )
            logger.info(
                "Action '%s': SKIP (halted by prior failure in '%s')",
                action_name,
                exec_failed_by,
            )
            results.append(result)
            _log_endgroup()
            continue

        if snapshot_invalidated_by:
            if not getattr(action, "runs_after_invalidation", False):
                skip_details, skip_log_reason = _describe_snapshot_invalidation_skip(
                    action_name,
                    snapshot_invalidated_by,
                )
                result = ActionResult(
                    name=action_name,
                    decision=ActionDecision.SKIP,
                    details=skip_details,
                )
                logger.info(
                    "Action '%s': SKIP (%s)",
                    action_name,
                    skip_log_reason,
                )
                results.append(result)
                _log_endgroup()
                continue

            if not refreshed_after_invalidation:
                refresh_error = _refresh_snapshot_after_invalidation()
                if refresh_error is not None:
                    result = ActionResult(
                        name=action_name,
                        decision=ActionDecision.FAILED,
                        error=refresh_error,
                        details=f"Failed to refresh snapshot after '{snapshot_invalidated_by}'",
                    )
                    results.append(result)
                    exec_failed_by = action_name
                    _log_endgroup()
                    continue

            if guard_blocked:
                result = ActionResult(
                    name=action_name,
                    decision=ActionDecision.BLOCKED_BY_GUARD,
                    details=f"Blocked by guards: {guard_block_reason}",
                )
                results.append(result)
                _log_endgroup()
                continue

        # Evaluate preconditions
        try:
            eval_result = action.evaluate(current_snapshot, derived)
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.error("Action '%s' evaluation raised exception: %s", action_name, exc)
            result = ActionResult(
                name=action_name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="Exception during evaluation",
            )
            # Guards fail closed
            if action_name == "guards":
                guard_blocked = True
                guard_block_reason = f"evaluation_exception: {exc}"
                result.decision = ActionDecision.BLOCKED
                result.details = f"Exception during evaluation: {exc}"
            else:
                exec_failed_by = action_name
            results.append(result)
            _log_endgroup()
            continue

        logger.info(
            "Action '%s': evaluated → %s (preconditions: %s)",
            action_name,
            eval_result.decision.value,
            eval_result.preconditions,
        )

        if eval_result.decision == ActionDecision.BLOCKED:
            # Guards action blocking the rest
            if action_name == "guards":
                guard_blocked = True
                guard_block_reason = eval_result.details
            results.append(eval_result)
            _log_endgroup()
            continue

        if eval_result.decision != ActionDecision.EXECUTE:
            # SKIP or other non-execute decision
            results.append(eval_result)
            _log_endgroup()
            continue

        if getattr(action, "may_invalidate_snapshot", False):
            invalidation_preserves_diff_fingerprint = bool(getattr(action, "preserves_diff_fingerprint", False))
            invalidation_intentional_noop = bool(getattr(action, "intentional_noop", False))
            invalidation_allows_file_removal = False
            invalidation_allowed_removed_files = ()
            pre_mutation_intentional_noop = invalidation_intentional_noop
            if not _persist_diff_preservation_blocker(current_snapshot):
                result = ActionResult(
                    name=action_name,
                    decision=ActionDecision.FAILED,
                    preconditions=eval_result.preconditions,
                    error="Failed to persist diff-preservation blocker",
                    details="Mutation skipped because the pre-mutation baseline was not persisted",
                )
                results.append(result)
                exec_failed_by = action_name
                _log_endgroup()
                continue
            diff_preservation_blocker_persisted = True

        if action_name == "dispatch_conflict_resolution":
            invalidation_allows_file_removal = False
            invalidation_allowed_removed_files = ()
            invalidation_intentional_noop = False
            if not _persist_diff_preservation_blocker(
                current_snapshot,
                fingerprint_supported_override=current_snapshot.diff_hash_supported,
                conflict_repair=True,
            ):
                result = ActionResult(
                    name=action_name,
                    decision=ActionDecision.FAILED,
                    preconditions=eval_result.preconditions,
                    error="Failed to persist diff-preservation blocker",
                    details="Conflict repair skipped because the pre-dispatch baseline was not persisted",
                )
                results.append(result)
                exec_failed_by = action_name
                _log_endgroup()
                continue
            diff_preservation_blocker_persisted = True

        # Execute the action
        try:
            exec_result = action.execute(provider, current_snapshot, derived)
            logger.info(
                "Action '%s': executed → %s (details: %s)",
                action_name,
                exec_result.decision.value,
                exec_result.details,
            )
            # Merge preconditions from evaluation into execution result
            if not exec_result.preconditions and eval_result.preconditions:
                exec_result.preconditions = eval_result.preconditions
            if (
                exec_result.decision == ActionDecision.FAILED
                and exec_result.definitive_no_mutation
                and diff_preservation_blocker_persisted
            ):
                # A rejected force-with-lease did not mutate the remote branch.
                # Retire the pre-mutation blocker instead of carrying it into a
                # later run where a concurrent push would be treated as its output.
                clear_diff_preservation_blocker = True
                clear_diff_preservation_blocker_allow_stale_head = True
                diff_preservation_blocker_persisted = False
            if action_name == "dispatch_repair":
                if exec_result.dedup_limit_reached:
                    derived.set("repair_limit_reached", True)
                if exec_result.cycle_limit_reached:
                    derived.set("cycle_limit_reached", True)

            if exec_result.invalidates_snapshot:
                snapshot_invalidated_by = action_name
                invalidation_preserves_diff_fingerprint = exec_result.preserves_diff_fingerprint
                invalidation_intentional_noop = exec_result.intentional_noop
                invalidation_allows_file_removal = exec_result.allows_file_removal
                invalidation_allowed_removed_files = exec_result.allowed_removed_files
                if not invalidation_intentional_noop and (
                    not diff_preservation_blocker_persisted
                    or persisted_diff_preservation_allows_file_removal != invalidation_allows_file_removal
                    or persisted_diff_preservation_allowed_removed_files != invalidation_allowed_removed_files
                ):
                    policy_persisted = _persist_diff_preservation_blocker(
                        current_snapshot,
                        allowed_removed_files=invalidation_allowed_removed_files,
                    )
                    diff_preservation_blocker_persisted = diff_preservation_blocker_persisted or policy_persisted
                # Re-arm the refresh. A NEW invalidation supersedes any earlier
                # post-invalidation refresh performed in this run, so the next
                # runs_after_invalidation action must refresh again instead of
                # evaluating a snapshot that predates this invalidation.
                #
                # The latch is keyed on invalidation identity (an executed action
                # reporting invalidates_snapshot) rather than on the observed
                # head_sha: the invalidating action moved HEAD remotely, so the
                # locally held snapshot cannot detect the change without the very
                # API call the latch is meant to schedule.
                refreshed_after_invalidation = False
                if exec_result.decision == ActionDecision.FAILED:
                    refresh_error = _refresh_snapshot_after_invalidation()
                    if refresh_error is not None:
                        exec_result.details = (
                            f"{exec_result.details}; failed to refresh snapshot after potential partial mutation"
                        )
                        exec_result.error = (
                            f"{exec_result.error}; refresh failed: {refresh_error}"
                            if exec_result.error
                            else f"refresh failed: {refresh_error}"
                        )
            results.append(exec_result)
            # Track first FAILED side-effect to block subsequent executions
            if exec_result.decision == ActionDecision.FAILED and action_name != "guards":
                exec_failed_by = action_name
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                if bool(getattr(exc, "invalidates_snapshot", False)):
                    snapshot_invalidated_by = action_name
                    invalidation_preserves_diff_fingerprint = bool(getattr(exc, "preserves_diff_fingerprint", False))
                    invalidation_intentional_noop = bool(getattr(exc, "intentional_noop", False))
                    invalidation_allows_file_removal = False
                    invalidation_allowed_removed_files = ()
                    if (
                        invalidation_intentional_noop != pre_mutation_intentional_noop
                        and diff_preservation_blocker_persisted
                    ):
                        live_metadata = provider.get_pr_metadata(current_snapshot.pr_number)
                        live_head_sha = getattr(live_metadata, "head_sha", "")
                        _persist_diff_preservation_blocker(
                            current_snapshot,
                            expected_live_head=live_head_sha,
                            allowed_removed_files=invalidation_allowed_removed_files,
                        )
                    if not invalidation_intentional_noop:
                        diff_preservation_blocker_persisted = _persist_diff_preservation_blocker(
                            current_snapshot,
                            allowed_removed_files=invalidation_allowed_removed_files,
                        )
                    _refresh_snapshot_after_invalidation()
                raise
            logger.error("Action '%s' execution raised exception: %s", action_name, exc)
            result = ActionResult(
                name=action_name,
                decision=ActionDecision.FAILED,
                preconditions=eval_result.preconditions,
                error=str(exc),
                details="Exception during execution",
            )
            results.append(result)
            if action_name != "guards":
                exec_failed_by = action_name

        _log_endgroup()

    if (
        persist_conflict_repair_validation
        and not any(
            result.name == "dispatch_conflict_resolution"
            and result.decision in {ActionDecision.EXECUTE, ActionDecision.FAILED}
            for result in results
        )
        and not guard_blocked
        and (not snapshot_invalidated_by or refreshed_after_invalidation)
    ):
        conflict_repair_validation_persisted = _persist_conflict_repair_validation(
            provider,
            current_snapshot.pr_number,
            current_snapshot.head_sha,
        )
    if (
        clear_diff_preservation_blocker
        and not any(
            result.name == "dispatch_conflict_resolution"
            and result.decision in {ActionDecision.EXECUTE, ActionDecision.FAILED}
            for result in results
        )
        and not guard_blocked
        and (not snapshot_invalidated_by or refreshed_after_invalidation)
        and conflict_repair_validation_persisted
    ):
        _clear_persisted_diff_preservation_blocker(
            allow_stale_head=clear_diff_preservation_blocker_allow_stale_head,
        )

    return PipelineRunSummary(
        results=results,
        snapshot=current_snapshot,
        run_url=_get_run_url(),
        timestamp=datetime.now(UTC).isoformat(),
        trigger_reason=os.environ.get("TRIGGER_REASON", ""),
        # Read from the live `derived` binding: after a refresh this is the
        # rebuilt object, i.e. exactly the count the post-refresh gates saw.
        derived_unresolved_threads=derived.unresolved_threads,
    )
