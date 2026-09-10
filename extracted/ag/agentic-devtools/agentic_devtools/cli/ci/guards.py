"""CI workflow safety guards.

Extracted from ai-pr-loop.yml — these guards determine whether a PR
should be processed by the AI loop or requires human intervention.
"""

from __future__ import annotations

import logging
import os
import re
import uuid
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from hmac import compare_digest
from pathlib import Path
from typing import Any, cast

from agentic_devtools.cli.ci.dispatch_state import (
    DispatchIdentity,
    DispatchRecord,
    DispatchState,
    _attempt_capability_digest,
    load_dispatch_record,
)
from agentic_devtools.cli.ci.models import COPILOT_COMMENT_LOGINS, EventPayload, IssueCommentInfo
from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)
DISPATCH_CONTRACT_MARKER = "<!-- agdt:ref:sub-dedup-ordering -->"
_ITERATION_EXHAUSTED = object()
_ALIAS_CONFLICT = object()


def canonical_dispatch_token(
    identity_or_repo: DispatchIdentity | str,
    pull_request_id: int | None = None,
    sha: str | None = None,
    ordinal: int | None = None,
) -> str:
    """Return the canonical correlation token for a dispatch identity."""
    if isinstance(identity_or_repo, DispatchIdentity):
        if any(value is not None for value in (pull_request_id, sha, ordinal)):
            raise ValueError("identity and individual identity fields cannot be combined")
        return identity_or_repo.token
    if any(value is None for value in (pull_request_id, sha, ordinal)):
        raise ValueError("all dispatch identity fields are required")
    assert pull_request_id is not None and sha is not None and ordinal is not None
    return DispatchIdentity(identity_or_repo, pull_request_id, sha, ordinal).token


def validate_dispatch_identity(repo: str, pull_request_id: int, sha: str, ordinal: int) -> DispatchIdentity:
    """Validate and normalize the immutable identity used by dispatch state."""
    return DispatchIdentity(repo, pull_request_id, sha, ordinal)


def build_dispatch_marker_comment(identity: DispatchIdentity, content: str = "") -> str:
    """Build a byte-zero contract marker containing the identity token."""
    if not isinstance(content, str):
        raise ValueError("marker content must be a string")
    identity = validate_dispatch_identity(
        identity.repo,
        identity.pull_request_id,
        identity.sha,
        identity.ordinal,
    )
    suffix = f"\n\n{content}" if content else ""
    return f"{DISPATCH_CONTRACT_MARKER}\n{identity.token}{suffix}"


def build_task_prompt_header(identity: DispatchIdentity) -> str:
    """Return the structured first line used for task correlation."""
    identity = validate_dispatch_identity(
        identity.repo,
        identity.pull_request_id,
        identity.sha,
        identity.ordinal,
    )
    return f"agdt-dispatch-token: {identity.token}"


def assert_task_creation_allowed(path: Path, record: DispatchRecord) -> bool:
    """Fail closed unless the persisted creating record still matches a local capability."""
    record.validate()
    if not isinstance(record.attempt_capability, str) or not record.attempt_capability:
        raise ValueError("task creation requires a non-replayable local attempt capability")
    digest = _attempt_capability_digest(record.attempt_capability)
    persisted = load_dispatch_record(path, record.identity)
    if (
        persisted is None
        or persisted.to_dict() != record.to_dict()
        or persisted.state is not DispatchState.CREATING
        or persisted.marker_comment_id is None
        or persisted.attempt_capability_digest is None
        or not compare_digest(persisted.attempt_capability_digest, digest)
    ):
        raise ValueError("task creation requires a durably persisted creating marker")
    return True


def append_task_link_idempotently(path: Path, identity: DispatchIdentity, body: str, task_id: str) -> str:
    """Append exactly one Agent Task link for a durably persisted created record."""
    if not isinstance(body, str):
        raise ValueError("comment body must be a string")
    if not isinstance(task_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", task_id):
        raise ValueError("task_id must be a non-empty safe identifier")
    identity = DispatchIdentity(identity.repo, identity.pull_request_id, identity.sha, identity.ordinal)
    record = load_dispatch_record(path, identity)
    if record is None or record.state is not DispatchState.CREATED or record.task_id != task_id:
        raise ValueError("task link edit requires a durably persisted created record")
    link = f"#agent-task-{task_id}"
    if any(line.strip() == link for line in body.splitlines()):
        return body
    return f"{body}\n\n{link}"


@dataclass(frozen=True)
class ReconciliationResult:
    """Bounded result of reconciling uncertain task or marker writes."""

    outcome: str
    task_id: str | None = None
    marker_comment_id: int | None = None
    evidence: dict[str, Any] | None = None


def _candidate_scope(candidate: dict[str, Any]) -> tuple[str | None, int | None]:
    def _normalize_repo(value: object) -> str | None:
        def _valid_segment(segment: str) -> bool:
            return bool(segment) and segment not in {".", ".."}

        if not isinstance(value, str):
            return None
        if value.count("/") == 1:
            owner, repository = value.split("/", 1)
            if not (_valid_segment(owner) and _valid_segment(repository)):
                return None
            value = repository
        elif "/" in value:
            return None
        if not _valid_segment(value):
            return None
        return value.lower()

    def _normalize_pr(value: object) -> int | None:
        if isinstance(value, bool) or not isinstance(value, int):
            return None
        return value

    repo_values = [candidate.get(key) for key in ("repo", "repository", "repository_name") if key in candidate]
    repo_candidates = {_normalize_repo(value) for value in repo_values}
    if None in repo_candidates:
        return None, None
    if len(repo_candidates) > 1:
        return None, None
    repo = next(iter(repo_candidates), None)

    pr_values = [
        candidate.get(key) for key in ("pull_request_id", "pr_number", "pull_request_number") if key in candidate
    ]
    if "pull_request" in candidate:
        nested = candidate.get("pull_request")
        if not isinstance(nested, dict):
            return None, None
        nested_pr_values = [nested.get(key) for key in ("number", "id") if key in nested]
        if not nested_pr_values:
            return None, None
        pr_values.extend(nested_pr_values)

    pr_candidates = {_normalize_pr(value) for value in pr_values}
    if None in pr_candidates:
        return None, None
    if len(pr_candidates) > 1:
        return None, None
    pr = next(iter(pr_candidates), None)

    if repo is None or pr is None:
        return None, None
    return repo, pr


def _has_exact_prompt_header(prompt: object, token: str) -> bool:
    if not isinstance(prompt, str):
        return False
    first_line = prompt.splitlines()[0] if prompt.splitlines() else ""
    pattern = rf"(?:agdt-dispatch-token|agdt:dispatch|dispatch-token)\s*[:=]\s*{re.escape(token)}"
    return bool(re.fullmatch(pattern, first_line))


def _comment_author_login(comment: dict[str, Any]) -> object:
    author_aliases: list[object] = []
    if "author" in comment:
        author = comment.get("author")
        if isinstance(author, dict):
            if "login" not in author:
                return _ALIAS_CONFLICT
            author_aliases.append(author.get("login"))
        else:
            author_aliases.append(author)
    if "author_login" in comment:
        author_aliases.append(comment.get("author_login"))
    if "user" in comment:
        user = comment.get("user")
        if not isinstance(user, dict) or "login" not in user:
            return _ALIAS_CONFLICT
        author_aliases.append(user.get("login"))
    if not author_aliases:
        return None
    normalized_aliases: list[str] = []
    for alias in author_aliases:
        if not isinstance(alias, str) or not alias.strip():
            return _ALIAS_CONFLICT
        normalized_aliases.append(alias.casefold())
    if len(set(normalized_aliases)) != 1:
        return _ALIAS_CONFLICT
    return normalized_aliases[0]


def _consistent_present_aliases(mapping: dict[str, Any], keys: tuple[str, ...]) -> object:
    def _typed_json_equal(left: object, right: object) -> bool:
        if type(left) is not type(right):
            return False
        if isinstance(left, dict):
            right_dict = cast(dict[object, object], right)
            if left.keys() != right_dict.keys():
                return False
            return all(_typed_json_equal(left[key], right_dict[key]) for key in left)
        if isinstance(left, list):
            right_list = cast(list[object], right)
            if len(left) != len(right_list):
                return False
            return all(_typed_json_equal(left_item, right_item) for left_item, right_item in zip(left, right_list))
        return left == right

    aliases = [mapping.get(key) for key in keys if key in mapping]
    if not aliases:
        return None
    value = aliases[0]
    if any(not _typed_json_equal(alias, value) for alias in aliases[1:]):
        return _ALIAS_CONFLICT
    return value


_MAX_RECONCILIATION_FOLLOW_UPS = 32


def _page_parts(page: object) -> tuple[list[dict[str, Any]], bool, bool]:
    """Return tasks, explicit completion, and an invalid/partial flag."""
    if not isinstance(page, dict):
        return [], False, True
    invalid = False
    authorized_raw = page.get("authorized")
    if "authorized" in page:
        if not isinstance(authorized_raw, bool):
            invalid = True
        elif authorized_raw is False:
            invalid = True
    partial_raw = page.get("partial")
    if "partial" in page:
        if not isinstance(partial_raw, bool):
            invalid = True
        elif partial_raw is True:
            invalid = True
    truncated_raw = page.get("truncated")
    if "truncated" in page:
        if not isinstance(truncated_raw, bool):
            invalid = True
        elif truncated_raw is True:
            invalid = True
    status_values: dict[str, int] = {}
    for status_key in ("status", "status_code"):
        if status_key not in page:
            continue
        status_raw = page.get(status_key)
        if isinstance(status_raw, bool) or not isinstance(status_raw, int) or not 200 <= status_raw <= 299:
            invalid = True
            continue
        status_values[status_key] = status_raw
    if (
        "status" in status_values
        and "status_code" in status_values
        and status_values["status"] != status_values["status_code"]
    ):
        invalid = True
    task_aliases = [page.get(key) for key in ("tasks", "items", "data") if key in page]
    if not task_aliases:
        return [], False, True
    normalized_aliases: list[list[dict[str, Any]]] = []
    for alias in task_aliases:
        normalized = alias
        if isinstance(normalized, dict):
            nested_aliases = [normalized.get(key) for key in ("tasks", "items", "data") if key in normalized]
            if not nested_aliases:
                return [], False, True
            normalized = nested_aliases[0]
            nested_alias_mapping = {str(index): alias for index, alias in enumerate(nested_aliases)}
            nested_alias_keys = tuple(nested_alias_mapping)
            if _consistent_present_aliases(nested_alias_mapping, nested_alias_keys) is _ALIAS_CONFLICT:
                invalid = True
        if not isinstance(normalized, list) or any(not isinstance(task, dict) for task in normalized):
            return [], False, True
        normalized_aliases.append(normalized)
    raw_tasks = normalized_aliases[0]
    task_alias_mapping = {str(index): alias for index, alias in enumerate(normalized_aliases)}
    task_alias_keys = tuple(task_alias_mapping)
    if _consistent_present_aliases(task_alias_mapping, task_alias_keys) is _ALIAS_CONFLICT:
        invalid = True
    pagination_keys = ("has_more", "next", "next_url", "next_token", "continuation", "is_last")
    has_pagination = any(key in page for key in pagination_keys)
    has_more = page.get("has_more")
    page_dict = cast(dict[str, Any], page)
    continuation = None
    continuation_aliases = [
        page_dict.get(key) for key in ("next", "next_url", "next_token", "continuation") if key in page_dict
    ]
    if continuation_aliases:
        continuation = continuation_aliases[0]
        if any(type(alias) is not type(continuation) or alias != continuation for alias in continuation_aliases[1:]):
            invalid = True
    is_last_raw = page.get("is_last")
    is_last = is_last_raw if isinstance(is_last_raw, bool) else None
    if "is_last" in page and is_last is None:
        invalid = True
    if "has_more" in page and not isinstance(has_more, bool):
        invalid = True
    if is_last is True and (has_more is True or continuation is not None):
        invalid = True
    if is_last is False:
        if has_more is False:
            invalid = True
        elif continuation is None and has_more is not True:
            invalid = True
    explicit_end = (
        has_more is False
        or is_last is True
        or (has_pagination and continuation is None and has_more is not True and is_last is not False)
    )
    if has_more is True and continuation is None:
        invalid = True
    if has_more is False and continuation is not None:
        invalid = True
    return raw_tasks, explicit_end, invalid


def reconcile_uncertain_dispatch(
    identity: DispatchIdentity,
    pages: Iterable[object] | Callable[[object | None], object],
) -> ReconciliationResult:
    """Reconcile an uncertain task write using every complete page of results.

    Only a structured first-line prompt header is correlated. Missing pagination
    termination, malformed pages, authorization failures, and scope ambiguity
    are deliberately incomplete rather than misses.
    """
    identity = DispatchIdentity(identity.repo, identity.pull_request_id, identity.sha, identity.ordinal)
    matches: set[str] = set()
    invalid = False
    page_count = 0
    scope_attested = False
    continuation: object | None = None
    callable_source_invalid = False
    callable_source = callable(pages)
    max_pages = _MAX_RECONCILIATION_FOLLOW_UPS + 1

    source: Iterator[object]
    if callable_source:
        page_fetcher = cast(Callable[[object | None], object], pages)
        seen_continuations: set[tuple[str, str]] = set()

        def page_source() -> Iterator[object]:
            nonlocal callable_source_invalid, continuation
            while True:
                try:
                    page = page_fetcher(continuation)
                except Exception:
                    callable_source_invalid = True
                    return
                yield page
                _, explicit_end, page_invalid = _page_parts(page)
                if page_invalid or explicit_end:
                    return
                page_dict = cast(dict[str, Any], page)
                continuation_aliases = [
                    page_dict.get(key) for key in ("next", "next_url", "next_token", "continuation") if key in page_dict
                ]
                continuation = continuation_aliases[0] if continuation_aliases else None
                if continuation is None:
                    return
                if isinstance(continuation, bool) or not isinstance(continuation, (str, int)):
                    callable_source_invalid = True
                    return
                continuation_key = (type(continuation).__name__, str(continuation))
                if continuation_key in seen_continuations or len(seen_continuations) >= _MAX_RECONCILIATION_FOLLOW_UPS:
                    callable_source_invalid = True
                    return
                seen_continuations.add(continuation_key)

        source = page_source()
    elif isinstance(pages, dict):
        source = iter((pages,))
    else:
        source = iter(cast(Iterable[object], pages))

    explicit_end = False
    try:
        for page in source:
            page_count += 1
            if page_count > max_pages:
                invalid = True
                break
            tasks, explicit_end, page_invalid = _page_parts(page)
            invalid = invalid or page_invalid
            page_dict = cast(dict[str, Any], page) if isinstance(page, dict) else None
            if page_dict is not None:
                page_scope_keys = (
                    "repo",
                    "repository",
                    "repository_name",
                    "pull_request_id",
                    "pr_number",
                    "pull_request_number",
                    "pull_request",
                )
                if any(key in page_dict for key in page_scope_keys):
                    page_repo, page_pr = _candidate_scope(page_dict)
                    if page_repo != identity.repo or page_pr != identity.pull_request_id:
                        invalid = True
                    else:
                        scope_attested = True
            for candidate in tasks:
                prompt = candidate.get("prompt")
                if not isinstance(prompt, str):
                    invalid = True
                    continue
                repo, pr = _candidate_scope(candidate)
                if not _has_exact_prompt_header(prompt, identity.token):
                    if repo == identity.repo and pr == identity.pull_request_id:
                        scope_attested = True
                    continue
                if repo != identity.repo or pr != identity.pull_request_id:
                    invalid = True
                    continue
                scope_attested = True
                task_id = _consistent_present_aliases(candidate, ("id", "task_id"))
                if task_id is _ALIAS_CONFLICT:
                    invalid = True
                    continue
                if not isinstance(task_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", task_id):
                    invalid = True
                    continue
                matches.add(task_id)
            if explicit_end:
                break
    except Exception:
        invalid = True

    if explicit_end and not callable_source:
        try:
            trailing_page = next(source, _ITERATION_EXHAUSTED)
        except Exception:
            invalid = True
            page_count += 1
        else:
            if trailing_page is not _ITERATION_EXHAUSTED:
                invalid = True
                page_count += 1

    invalid = invalid or callable_source_invalid
    complete = bool(page_count and explicit_end and not invalid)
    evidence = {"pages": page_count, "matches": len(matches), "scope_attested": scope_attested}
    if not complete:
        return ReconciliationResult("incomplete", evidence=evidence)
    if len(matches) == 1:
        return ReconciliationResult("unique_match", task_id=next(iter(matches)), evidence=evidence)
    if len(matches) > 1:
        return ReconciliationResult("ambiguous", evidence=evidence)
    if not scope_attested:
        return ReconciliationResult("incomplete", evidence=evidence)
    return ReconciliationResult("complete_miss", evidence=evidence)


def _as_dispatch_tasks_from_comments(
    identity: DispatchIdentity,
    comments: object,
    *,
    dispatch_login: str = "",
) -> list[dict[str, Any]] | object:
    if isinstance(comments, dict):
        comments = comments.get("comments", comments.get("items", []))
    if not isinstance(comments, list):
        return comments

    def _comment_id_as_task_id(comment: dict[str, Any]) -> object:
        comment_id = _consistent_present_aliases(comment, ("id", "comment_id"))
        if isinstance(comment_id, bool):
            return _ALIAS_CONFLICT
        if isinstance(comment_id, int) and comment_id > 0:
            return str(comment_id)
        return _ALIAS_CONFLICT

    def _invalid_matching_comment(comment: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": _comment_id_as_task_id(comment),
            "repo": "invalid/repo/shape",
            "pull_request_id": identity.pull_request_id,
            "prompt": f"agdt-dispatch-token: {identity.token}",
        }

    tasks: list[dict[str, Any]] = []
    for comment in comments:
        if not isinstance(comment, dict):
            return comments
        body = comment.get("body")
        if not isinstance(body, str):
            tasks.append(_invalid_matching_comment(comment))
            continue
        prompt = ""
        marker_prefix = f"{DISPATCH_CONTRACT_MARKER}\n"
        if body.startswith(marker_prefix) and body[len(marker_prefix) :].split("\n", 1)[0] == identity.token:
            if not dispatch_login:
                tasks.append(_invalid_matching_comment(comment))
                continue
            author_login = _comment_author_login(comment)
            if author_login is _ALIAS_CONFLICT or author_login is None:
                tasks.append(_invalid_matching_comment(comment))
                continue
            if author_login == dispatch_login.casefold():
                prompt = f"agdt-dispatch-token: {identity.token}"
        tasks.append(
            {
                "id": _comment_id_as_task_id(comment),
                "repo": identity.repo,
                "pull_request_id": identity.pull_request_id,
                "prompt": prompt,
            }
        )
    return tasks


def reconcile_uncertain_marker_comment(
    identity: DispatchIdentity,
    pages: Iterable[object] | Callable[[object | None], object],
    *,
    dispatch_login: str = "",
) -> ReconciliationResult:
    """Reconcile an uncertain marker write from paginated PR issue comments.

    Only marker comments authored by ``dispatch_login`` are eligible matches.
    A canonical token without an authenticated expected author is incomplete,
    while spoofed comments from other authors are ignored as misses.
    """
    identity = DispatchIdentity(identity.repo, identity.pull_request_id, identity.sha, identity.ordinal)

    def map_page(page: object) -> object:
        if not isinstance(page, dict):
            return page
        mapped = dict(page)
        mapped.setdefault("repo", identity.repo)
        mapped.setdefault("pull_request_id", identity.pull_request_id)
        comment_aliases = [page.get(key) for key in ("comments", "items", "data") if key in page]
        if not comment_aliases:
            mapped["tasks"] = "invalid-comment-alias-conflict"
            return mapped
        normalized_aliases: list[object] = []
        for alias in comment_aliases:
            normalized = alias
            if isinstance(normalized, dict):
                nested_aliases = [normalized.get(key) for key in ("comments", "items", "data") if key in normalized]
                if not nested_aliases:
                    mapped["tasks"] = "invalid-comment-alias-conflict"
                    return mapped
                normalized = nested_aliases[0]
                nested_alias_mapping = {str(index): alias for index, alias in enumerate(nested_aliases)}
                nested_alias_keys = tuple(nested_alias_mapping)
                if _consistent_present_aliases(nested_alias_mapping, nested_alias_keys) is _ALIAS_CONFLICT:
                    mapped["tasks"] = "invalid-comment-alias-conflict"
                    return mapped
            normalized_aliases.append(normalized)
        raw_comments = normalized_aliases[0]
        comment_alias_mapping = {str(index): alias for index, alias in enumerate(normalized_aliases)}
        comment_alias_keys = tuple(comment_alias_mapping)
        if _consistent_present_aliases(comment_alias_mapping, comment_alias_keys) is _ALIAS_CONFLICT:
            mapped["tasks"] = "invalid-comment-alias-conflict"
            return mapped
        mapped["tasks"] = _as_dispatch_tasks_from_comments(identity, raw_comments, dispatch_login=dispatch_login)
        mapped.pop("items", None)
        mapped.pop("data", None)
        return mapped

    mapped_pages: Iterable[object] | Callable[[object | None], object]
    if callable(pages):

        def mapped_pages(continuation: object | None) -> object:
            return map_page(pages(continuation))
    elif isinstance(pages, dict):
        mapped_pages = (map_page(pages),)
    else:
        mapped_pages = (map_page(page) for page in pages)
    result = reconcile_uncertain_dispatch(identity, mapped_pages)
    evidence = dict(result.evidence or {})
    evidence["operation"] = "marker"
    marker_comment_id = None
    if result.outcome == "unique_match":
        marker_comment_id_raw = result.task_id
        if not isinstance(marker_comment_id_raw, str):
            return ReconciliationResult("incomplete", evidence=evidence)
        if not re.fullmatch(r"[1-9][0-9]*", marker_comment_id_raw):
            return ReconciliationResult("incomplete", evidence=evidence)
        marker_comment_id = int(marker_comment_id_raw)
    return ReconciliationResult(result.outcome, marker_comment_id=marker_comment_id, evidence=evidence)


# Privileged path prefixes that trigger the guard
PRIVILEGED_PREFIXES = (
    ".github/workflows/",
    ".github/actions/",
    ".github/scripts/",
)

# Docker files that trigger the guard
DOCKER_FILES = {"Dockerfile", "docker-compose.yml", "docker-compose.yaml"}
DOCKER_PATTERNS = (re.compile(r"^\.dockerignore$"), re.compile(r"^Dockerfile\..*$"))

# ---------------------------------------------------------------------------
# TTL for timed idempotency guards
# ---------------------------------------------------------------------------

# Minutes after which a dispatch marker is treated as expired, allowing
# re-dispatch.  Applied to:
#   (a) the conflict-repair dispatch marker (CONFLICT_REPAIR_MARKER_*), and
#   (b) the review-ID trigger dedup guard (is_duplicate_trigger).
# NOT applied to check_deduplication (per-SHA budget) or check_cycle_limit
# (global safety valve) — those keep blocking unconditionally.
DISPATCH_IDEMPOTENCY_TTL_MINUTES = 60

# ---------------------------------------------------------------------------
# Conflict-repair marker helpers
# ---------------------------------------------------------------------------

# Marker format: <!-- agdt:conflict-repair:{base_sha}:{head_sha}:{iso8601_utc} -->
CONFLICT_REPAIR_MARKER_PREFIX = "<!-- agdt:conflict-repair:"
_CONFLICT_REPAIR_MARKER_RE = re.compile(r"<!-- agdt:conflict-repair:([0-9a-f]+):([0-9a-f]+):([^>]+) -->")

# Marker format: <!-- agdt:conflict-repair-escalation:{head_sha} -->
# Deliberately distinct from CONFLICT_REPAIR_MARKER_PREFIX (the ``-escalation``
# infix means the dispatch prefix is not a substring of it), so the escalation
# notice is never mistaken for a dispatch marker by
# ``find_comment(CONFLICT_REPAIR_MARKER_PREFIX)`` or counted as an attempt.
CONFLICT_REPAIR_ESCALATION_MARKER_PREFIX = "<!-- agdt:conflict-repair-escalation:"

# Maximum number of conflict-repair dispatches allowed against the *same* HEAD
# SHA before the loop stops retrying and escalates to a human.  A successful
# resolution pushes a new commit, which changes HEAD and resets the budget, so
# this only bounds repeated attempts the cloud agent failed to act on.
MAX_CONFLICT_REPAIR_ATTEMPTS = 3


def build_conflict_repair_marker(*, base_sha: str, head_sha: str) -> str:
    """Return a new conflict-repair idempotency marker with the current UTC time.

    Args:
        base_sha: Full SHA of the base-branch tip at dispatch time.
        head_sha: Full HEAD SHA of the PR branch at dispatch time.

    Returns:
        HTML comment string suitable for embedding in a PR comment body.
    """
    now = datetime.now(UTC).isoformat()
    return f"<!-- agdt:conflict-repair:{base_sha}:{head_sha}:{now} -->"


def _parse_iso8601_timestamp_guard(timestamp: str) -> datetime | None:
    """Parse an ISO 8601 timestamp string to an aware UTC datetime.

    Returns ``None`` when the string cannot be parsed.  Treating an
    unparseable timestamp as ``None`` (expired / fail-open) prevents a
    malformed marker from permanently blocking re-dispatch.
    """
    if not timestamp:
        return None
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def should_dispatch_conflict_repair(
    provider: CIPlatformProvider,
    pr_number: int,
    head_sha: str,
    base_sha: str,
    *,
    dispatch_login: str = "",
    ttl_minutes: int = DISPATCH_IDEMPOTENCY_TTL_MINUTES,
    now: datetime | None = None,
) -> bool:
    """Return True when dispatching a conflict-repair comment is allowed.

    Re-dispatch is allowed when ANY of the following is true:

    * No conflict-repair marker exists on the PR.
    * The marker's ``head_sha`` differs from the current ``head_sha``
      (the PR branch has been updated since the last dispatch).
    * The marker's ``base_sha`` differs from the current ``base_sha``
      (the base branch has advanced again since the last dispatch).
    * The marker's timestamp is older than ``ttl_minutes``.

    An unparseable timestamp is treated as expired (fail-open), so a
    malformed marker can never permanently wedge the PR.

    Args:
        provider: CI platform provider for comment lookup.
        pr_number: Pull request number.
        head_sha: Current HEAD SHA of the PR branch.
        base_sha: Current tip SHA of the base branch.
        dispatch_login: Authenticated login that posts the dispatch comment.
            When provided, only markers from this identity are trusted for
            deduplication.
        ttl_minutes: Age threshold in minutes after which a marker expires.
        now: Override for the current time (UTC); defaults to ``datetime.now(timezone.utc)``.

    Returns:
        True if a (re)dispatch is allowed, False if a recent in-TTL marker
        for the same head and base already exists.
    """
    if dispatch_login:
        matching = [
            comment
            for comment in provider.list_issue_comments(pr_number)
            if comment.author == dispatch_login and CONFLICT_REPAIR_MARKER_PREFIX in comment.body
        ]
        if not matching:
            return True
        comment_body = max(matching, key=lambda comment: comment.id).body
    else:
        existing = provider.find_comment(pr_number, CONFLICT_REPAIR_MARKER_PREFIX)
        if existing is None:
            return True
        _, comment_body = existing

    match = _CONFLICT_REPAIR_MARKER_RE.search(comment_body)
    if not match:
        # Marker prefix found but body is unrecognised — treat as expired.
        logger.warning(
            "PR #%d: conflict-repair marker found but unparseable — treating as expired, allowing re-dispatch",
            pr_number,
        )
        return True

    marker_base_sha = match.group(1)
    marker_head_sha = match.group(2)
    timestamp_str = match.group(3).strip()

    # SHA change → always allow re-dispatch
    if marker_head_sha != head_sha:
        logger.info(
            "PR #%d: conflict-repair marker head SHA mismatch (marker=%s, current=%s) — allowing re-dispatch",
            pr_number,
            marker_head_sha[:8],
            head_sha[:8],
        )
        return True
    if marker_base_sha != base_sha:
        logger.info(
            "PR #%d: conflict-repair marker base SHA mismatch (marker=%s, current=%s) — allowing re-dispatch",
            pr_number,
            marker_base_sha[:8],
            base_sha[:8],
        )
        return True

    # TTL check
    marker_time = _parse_iso8601_timestamp_guard(timestamp_str)
    if marker_time is None:
        logger.warning(
            "PR #%d: conflict-repair marker has unparseable timestamp (%r) — treating as expired, allowing re-dispatch",
            pr_number,
            timestamp_str,
        )
        return True

    current_time = now if now is not None else datetime.now(UTC)
    age_minutes = (current_time - marker_time).total_seconds() / 60
    if age_minutes >= ttl_minutes:
        logger.info(
            "PR #%d: conflict-repair marker is %.1f min old (TTL=%d min) — allowing re-dispatch",
            pr_number,
            age_minutes,
            ttl_minutes,
        )
        return True

    logger.info(
        "PR #%d: conflict-repair marker is %.1f min old (TTL=%d min), same head+base — suppressing re-dispatch",
        pr_number,
        age_minutes,
        ttl_minutes,
    )
    return False


def build_conflict_repair_escalation_marker(*, head_sha: str) -> str:
    """Return the idempotency marker for a conflict-repair escalation notice.

    Args:
        head_sha: Full HEAD SHA of the PR branch the escalation applies to.

    Returns:
        HTML comment string suitable for embedding in a PR comment body.
    """
    return f"{CONFLICT_REPAIR_ESCALATION_MARKER_PREFIX}{head_sha} -->"


def count_conflict_repair_dispatches(
    provider: CIPlatformProvider,
    pr_number: int,
    head_sha: str,
    dispatch_login: str = "",
) -> int:
    """Count conflict-repair dispatches already made against ``head_sha``.

    Only markers whose embedded head SHA equals the *current* HEAD are
    counted: once the cloud agent pushes a resolution the HEAD changes, so
    the attempt budget naturally resets for the new commit.

    When ``dispatch_login`` is provided (non-empty), only comments authored
    by that identity are counted.  This prevents any PR participant from
    inflating the attempt counter by posting a comment that contains the
    public marker format.  When ``dispatch_login`` is empty the function
    falls back to excluding known Copilot identities, which preserves
    backwards compatibility for callers that cannot resolve the dispatch
    identity.

    Args:
        provider: CI platform provider for comment lookup.
        pr_number: Pull request number.
        head_sha: Current HEAD SHA of the PR branch.
        dispatch_login: GitHub login of the identity that posts dispatch
            comments (e.g. the ``SPECKIT_PR_TOKEN`` owner).  When non-empty,
            only comments from this login are counted.

    Returns:
        Number of distinct comments carrying a conflict-repair marker for
        ``head_sha``.  A comment containing several markers counts once.
    """
    count = 0
    for comment in provider.list_issue_comments(pr_number):
        if dispatch_login:
            if comment.author != dispatch_login:
                continue
        elif comment.author in COPILOT_COMMENT_LOGINS:
            continue
        if any(match.group(2) == head_sha for match in _CONFLICT_REPAIR_MARKER_RE.finditer(comment.body)):
            count += 1
    return count


# Labels that affect PR processing
LABEL_SKIP_ENTIRELY = "ai-pr-loop-ignore"
LABEL_AUTO_MERGE_ALLOWED = "ai-auto-merge-allowed"

# Deduplication marker format
DEDUP_MARKER_PREFIX = "<!-- repair-dispatch:"
DEDUP_MARKER_PATTERN = re.compile(r"<!-- repair-dispatch:([a-f0-9]+):(\d+)(?::([A-Za-z0-9._-]+))? -->")

# Squash-wait marker constants
SQUASH_WAIT_MARKER_PREFIX = "<!-- squash-wait\n"
SQUASH_WAIT_MAX_ATTEMPTS = 24  # 24 × 5 min cron = ~120 minutes

# Default limits
DEFAULT_MAX_DISPATCHES_PER_SHA = 3
DEFAULT_MAX_CYCLES = 50

# Cycle tracker marker
CYCLE_TRACKER_MARKER = "<!-- ai-pr-loop-cycle-tracker -->"

# Repair-satisfied markers (no-commit-needed agent signal)
REPAIR_SATISFIED_MARKER = "<!-- ai-pr-loop:repair-satisfied -->"
THREAD_EVALUATED_MARKER = "<!-- ai-pr-loop:thread-evaluated -->"
REVIEW_ID_MARKER_RE = re.compile(r"<!--\s*review-id\s*:\s*(\d+)\s*-->")


def find_repair_satisfied_review_id(issue_comments: list[IssueCommentInfo]) -> int | None:
    """Return the review id of the most recent Copilot ``repair-satisfied`` marker.

    Scans *issue_comments* for Copilot-authored comments containing the
    :data:`REPAIR_SATISFIED_MARKER` together with a ``<!-- review-id:{id} -->``
    marker, and returns the ``review-id`` from the latest such comment (ordered by
    ``(created_at, id)``).  Returns ``None`` when no matching marker is found.

    The repair agent posts this marker after evaluating a review's comments and
    declaring that no code changes are needed.  It is the only signal that can
    clear a suppressed-comments block, since suppressed comments are recovered as
    synthetic negative-ID entries with no real GitHub review threads to resolve.
    """
    matched: list[tuple[str, int, int]] = []
    for c in issue_comments:
        if c.author in COPILOT_COMMENT_LOGINS and REPAIR_SATISFIED_MARKER in c.body:
            match = REVIEW_ID_MARKER_RE.search(c.body)
            if match:
                matched.append((c.created_at, c.id, int(match.group(1))))
    if not matched:
        return None
    _created_at, _id, review_id = max(matched, key=lambda item: (item[0], item[1]))
    return review_id


_DEDUP_WRITER_TOKEN: str | None = None


def get_dedup_writer_token() -> str:
    """Return a per-process token stamped into dedup markers."""
    global _DEDUP_WRITER_TOKEN
    if _DEDUP_WRITER_TOKEN is not None:
        return _DEDUP_WRITER_TOKEN

    run_id = os.environ.get("GITHUB_RUN_ID", "").strip()
    attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "").strip()
    job = os.environ.get("GITHUB_JOB", "").strip().replace(" ", "-")
    if run_id:
        parts = [run_id]
        if attempt:
            parts.append(attempt)
        if job:
            parts.append(job)
        _DEDUP_WRITER_TOKEN = ".".join(parts)
    else:
        _DEDUP_WRITER_TOKEN = f"local.{uuid.uuid4().hex[:12]}"

    return _DEDUP_WRITER_TOKEN


def check_privileged_paths(files: list[str]) -> bool:
    """Check if any PR files touch privileged paths.

    Privileged paths are `.github/workflows/`, `.github/actions/`,
    `.github/scripts/` — excluding markdown files (*.md).

    This guard can be disabled by setting the environment variable
    ``AGDT_ALLOW_PRIVILEGED_PATHS=1`` (also accepts ``true`` / ``yes``).
    Use this only when you intentionally want the AI loop to process PRs
    that modify workflow or action files.

    Args:
        files: List of file paths changed in the PR.

    Returns:
        True if privileged paths are touched (guard triggered), False otherwise.
    """
    if os.environ.get("AGDT_ALLOW_PRIVILEGED_PATHS", "").strip().lower() in {"1", "true", "yes"}:
        logger.warning(
            "Privileged paths guard bypassed via AGDT_ALLOW_PRIVILEGED_PATHS; "
            "PR may include workflow/action/script changes"
        )
        return False

    for f in files:
        if any(f.startswith(prefix) for prefix in PRIVILEGED_PREFIXES):
            if not f.endswith(".md"):
                return True
    return False


def check_docker_files(files: list[str]) -> bool:
    """Check if any PR files are Docker-related.

    Matches: Dockerfile, docker-compose.yml, docker-compose.yaml,
    .dockerignore, Dockerfile.* (e.g., Dockerfile.prod).

    Args:
        files: List of file paths changed in the PR.

    Returns:
        True if Docker files are touched (guard triggered), False otherwise.
    """
    for f in files:
        # Get the basename for matching
        basename = f.rsplit("/", 1)[-1] if "/" in f else f
        if basename in DOCKER_FILES:
            return True
        if any(pattern.match(basename) for pattern in DOCKER_PATTERNS):
            return True
    return False


def is_duplicate_trigger(
    provider: CIPlatformProvider,
    pr_number: int,
    review_id: int,
    *,
    ttl_minutes: int = DISPATCH_IDEMPOTENCY_TTL_MINUTES,
    now: datetime | None = None,
) -> bool:
    """Check if a trigger comment already exists for a given Copilot review ID.

    Searches PR comments for the ``<!-- copilot-trigger:REVIEW_ID -->`` marker
    (legacy format) or ``<!-- copilot-trigger:REVIEW_ID:{iso8601_utc} -->``
    (timestamped format).  This provides best-effort review-cycle-level
    deduplication by skipping when a prior trigger marker is present for
    the same Copilot review and that marker has not yet expired.

    **Timestamp handling:**

    * *Timestamped marker* — treated as a duplicate (returns True) only when
      the embedded timestamp is within ``ttl_minutes`` of ``now``.  A marker
      older than the TTL is treated as *not* a duplicate, allowing re-dispatch
      so that stuck/never-started agent sessions don't permanently block repair.
    * *Legacy marker without a timestamp* — treated as a permanent duplicate
      (returns True unconditionally), preserving the original behaviour for
      comments written by older versions of this code.
    * *Unparseable timestamp* — treated as unexpired (returns True) to match
      the legacy "fail-closed" behaviour; only confirmed-expired markers allow
      re-dispatch.

    Args:
        provider: CI platform provider for API calls.
        pr_number: Pull request number.
        review_id: Copilot review ID to check for.
        ttl_minutes: Age threshold in minutes after which a timestamped marker
            is treated as expired (defaults to ``DISPATCH_IDEMPOTENCY_TTL_MINUTES``).
        now: Override for the current time (UTC); defaults to
            ``datetime.now(timezone.utc)``.  Provided for deterministic testing.

    Returns:
        True if a trigger comment for this review_id already exists AND has
        not expired, False otherwise.
    """
    if review_id <= 0:
        return False

    review_id_str = str(review_id)
    legacy_marker = f"<!-- copilot-trigger:{review_id_str} -->"
    ts_pattern = re.compile(rf"<!-- copilot-trigger:{re.escape(review_id_str)}:([^>]+) -->")

    newest_marker_time: datetime | None = None
    for comment in provider.list_issue_comments(pr_number):
        comment_body = comment.body or ""
        if legacy_marker in comment_body:
            # Legacy format (no timestamp) — treat as permanent duplicate (fail-closed).
            return True

        ts_match = ts_pattern.search(comment_body)
        if ts_match is None:
            continue

        timestamp_str = ts_match.group(1).strip()
        marker_time = _parse_iso8601_timestamp_guard(timestamp_str)
        if marker_time is None:
            # Unparseable timestamp — fail-closed (treat as non-expired duplicate).
            logger.warning(
                "PR #%d: copilot-trigger marker for review_id=%d has unparseable timestamp (%r) "
                "— treating as non-expired",
                pr_number,
                review_id,
                timestamp_str,
            )
            return True

        if newest_marker_time is None or marker_time > newest_marker_time:
            newest_marker_time = marker_time

    if newest_marker_time is None:
        return False

    current_time = now if now is not None else datetime.now(UTC)
    age_minutes = (current_time - newest_marker_time).total_seconds() / 60
    if age_minutes >= ttl_minutes:
        logger.info(
            "PR #%d: copilot-trigger marker for review_id=%d is %.1f min old (TTL=%d min) — treating as expired",
            pr_number,
            review_id,
            age_minutes,
            ttl_minutes,
        )
        return False

    return True


def check_deduplication(
    provider: CIPlatformProvider,
    pr_number: int,
    head_sha: str,
    max_dispatches: int = DEFAULT_MAX_DISPATCHES_PER_SHA,
) -> tuple[bool, int]:
    """Check deduplication via marker comment on the PR.

    Reads/upserts a marker PR comment with format:
    ``<!-- repair-dispatch:<sha>:<count>:<writer_token> -->``
    (tokenless legacy markers are also accepted).

    Args:
        provider: CI platform provider for API calls.
        pr_number: Pull request number.
        head_sha: Current HEAD SHA.
        max_dispatches: Maximum dispatches allowed per SHA.

    Returns:
        Tuple of (should_skip, current_count). should_skip is True if
        the dispatch count has been exceeded.
    """
    writer_token = get_dedup_writer_token()
    existing = provider.find_comment(pr_number, DEDUP_MARKER_PREFIX)

    if existing is not None:
        comment_id, comment_body = existing
        match = DEDUP_MARKER_PATTERN.search(comment_body)
        if match and match.group(1) == head_sha:
            count = int(match.group(2)) + 1
            # Always persist the incremented count so the marker stays accurate
            new_marker = f"<!-- repair-dispatch:{head_sha}:{count}:{writer_token} -->"
            new_body = DEDUP_MARKER_PATTERN.sub(new_marker, comment_body)
            provider.update_comment(comment_id, new_body)
            if count > max_dispatches:
                return (True, count)
            return (False, count)

    # New SHA or no existing marker — create/update with count 1
    marker_body = f"<!-- repair-dispatch:{head_sha}:1:{writer_token} -->\nDispatch tracking for `{head_sha[:8]}`"
    if existing is not None:
        provider.update_comment(existing[0], marker_body)
    else:
        provider.post_comment(pr_number, marker_body)
    return (False, 1)


def check_exclusion_labels(labels: list[str]) -> tuple[bool, str | None]:
    """Check if PR labels trigger exclusion logic.

    Args:
        labels: List of label names on the PR.

    Returns:
        Tuple of (should_skip, flag_name).
        - should_skip=True, flag_name=None: skip entirely (ai-pr-loop-ignore)
        - should_skip=False, flag_name="do_not_merge": process but don't merge
          (ai-auto-merge-allowed label missing)
        - should_skip=False, flag_name=None: no exclusion
    """
    if LABEL_SKIP_ENTIRELY in labels:
        return (True, None)
    if LABEL_AUTO_MERGE_ALLOWED not in labels:
        return (False, "do_not_merge")
    return (False, None)


def check_fork_pr(head_repo: str, base_repo: str) -> bool:
    """Check if a PR is from a fork (different repository).

    Args:
        head_repo: Full name of the head (source) repository.
        base_repo: Full name of the base (target) repository.

    Returns:
        True if the PR is from a fork (guard triggered), False otherwise.
    """
    return head_repo != base_repo


def check_cycle_limit(
    provider: CIPlatformProvider,
    pr_number: int,
    max_cycles: int = DEFAULT_MAX_CYCLES,
) -> tuple[bool, int]:
    """Check if the AI loop cycle limit has been reached.

    Reads a cycle tracker comment on the PR without mutating it.

    Args:
        provider: CI platform provider for API calls.
        pr_number: Pull request number.
        max_cycles: Maximum allowed cycles.

    Returns:
        Tuple of (limit_reached, current_count).
    """
    existing = provider.find_comment(pr_number, CYCLE_TRACKER_MARKER)

    current_count = 0
    if existing is not None:
        _, comment_body = existing
        count_match = re.search(r"cycle:(\d+)", comment_body)
        current_count = int(count_match.group(1)) if count_match else 0

    return (current_count >= max_cycles, current_count)


def increment_cycle_count(provider: CIPlatformProvider, pr_number: int) -> int:
    """Increment and persist the AI loop cycle count tracker comment.

    Args:
        provider: CI platform provider for API calls.
        pr_number: Pull request number.

    Returns:
        The updated cycle count after incrementing.
    """
    existing = provider.find_comment(pr_number, CYCLE_TRACKER_MARKER)

    if existing is not None:
        comment_id, comment_body = existing
        count_match = re.search(r"cycle:(\d+)", comment_body)
        next_count = int(count_match.group(1)) + 1 if count_match else 1
        if count_match:
            new_body = re.sub(r"cycle:\d+", f"cycle:{next_count}", comment_body)
        else:
            new_body = f"{comment_body} cycle:{next_count}"
        provider.update_comment(comment_id, new_body)
        return next_count

    body = f"{CYCLE_TRACKER_MARKER} cycle:1"
    provider.post_comment(pr_number, body)
    return 1


# ---------------------------------------------------------------------------
# Squash-wait marker helpers
# ---------------------------------------------------------------------------

_SQUASH_WAIT_FIELD_RE = re.compile(r"^(\w+)=(.*)$", re.MULTILINE)


def _build_squash_wait_body(
    *,
    pr_number: int,
    sha: str,
    attempt: int,
    head_pushed_at: str,
    ci_passed: bool,
    copilot_session_terminal: bool,
    copilot_session_outcome: str,
    squash_done: bool,
) -> str:
    """Build the full comment body for a squash-wait marker."""
    now = datetime.now(UTC).isoformat()
    return (
        f"{SQUASH_WAIT_MARKER_PREFIX}"
        f"sha={sha}\n"
        f"attempt={attempt}\n"
        f"head_pushed_at={head_pushed_at}\n"
        f"ci_passed={'true' if ci_passed else 'false'}\n"
        f"copilot_session_terminal={'true' if copilot_session_terminal else 'false'}\n"
        f"copilot_session_outcome={copilot_session_outcome}\n"
        f"squash_done={'true' if squash_done else 'false'}\n"
        f"-->\n"
        f"Squash wait in progress for PR #{pr_number} — last checked {now}"
    )


def read_squash_wait_marker(
    provider: CIPlatformProvider,
    pr_number: int,
    head_sha: str,
) -> dict | None:
    """Read and parse the squash-wait marker comment for this PR.

    Returns a dict of parsed field values if the marker exists and the
    ``sha`` field matches ``head_sha``.  Returns ``None`` if the marker
    is absent or the SHA does not match the current head (indicating the
    marker is stale and belongs to a previous commit).

    Args:
        provider: CI platform provider for API calls.
        pr_number: Pull request number.
        head_sha: Current HEAD SHA to validate against the marker's sha field.

    Returns:
        Dict with keys sha, attempt (int), head_pushed_at, ci_passed (bool),
        copilot_session_terminal (bool), copilot_session_outcome, squash_done (bool),
        and comment_id (int).  Returns None when not found or SHA mismatch.
    """
    existing = provider.find_comment(pr_number, SQUASH_WAIT_MARKER_PREFIX)
    if existing is None:
        return None

    comment_id, comment_body = existing
    fields: dict[str, str] = {}
    for match in _SQUASH_WAIT_FIELD_RE.finditer(comment_body):
        fields[match.group(1)] = match.group(2).strip()

    marker_sha = fields.get("sha", "")
    if marker_sha != head_sha:
        logger.info(
            "PR #%d squash-wait marker SHA mismatch (marker=%s, head=%s) — treating as absent",
            pr_number,
            marker_sha[:8] if marker_sha else "",
            head_sha[:8] if head_sha else "",
        )
        return None

    def _bool(val: str) -> bool:
        return val.strip().lower() == "true"

    try:
        attempt = int(fields.get("attempt", "0"))
    except ValueError:
        logger.warning(
            "PR #%d squash-wait marker has non-integer attempt value (%r) — treating marker as absent",
            pr_number,
            fields.get("attempt"),
        )
        return None

    copilot_session_terminal = _bool(fields.get("copilot_session_terminal", "false"))
    copilot_session_outcome = fields.get("copilot_session_outcome", "pending").strip().lower()
    valid_outcomes = {"pending", "success", "failure"}
    if copilot_session_outcome not in valid_outcomes:
        logger.warning(
            "PR #%d squash-wait marker has invalid copilot_session_outcome value (%r) — treating marker as absent",
            pr_number,
            fields.get("copilot_session_outcome"),
        )
        return None
    if copilot_session_terminal and copilot_session_outcome == "pending":
        logger.warning(
            "PR #%d squash-wait marker has inconsistent terminal/outcome values (terminal=true, outcome=pending) "
            "— treating marker as absent",
            pr_number,
        )
        return None
    if not copilot_session_terminal and copilot_session_outcome in {"success", "failure"}:
        logger.warning(
            "PR #%d squash-wait marker has inconsistent terminal/outcome values (terminal=false, outcome=%s) "
            "— treating marker as absent",
            pr_number,
            copilot_session_outcome,
        )
        return None

    return {
        "comment_id": comment_id,
        "sha": marker_sha,
        "attempt": attempt,
        "head_pushed_at": fields.get("head_pushed_at", ""),
        "ci_passed": _bool(fields.get("ci_passed", "false")),
        "copilot_session_terminal": copilot_session_terminal,
        "copilot_session_outcome": copilot_session_outcome,
        "squash_done": _bool(fields.get("squash_done", "false")),
    }


def write_squash_wait_marker(
    provider: CIPlatformProvider,
    pr_number: int,
    *,
    sha: str,
    attempt: int,
    head_pushed_at: str,
    ci_passed: bool,
    copilot_session_terminal: bool,
    copilot_session_outcome: str,
    squash_done: bool,
) -> None:
    """Upsert the squash-wait marker comment on the PR.

    Creates the marker comment if it does not exist; updates it in-place
    if it already exists (identified by ``SQUASH_WAIT_MARKER_PREFIX``).

    Args:
        provider: CI platform provider for API calls.
        pr_number: Pull request number.
        sha: Full head SHA this marker tracks.
        attempt: Current attempt number (1-based).
        head_pushed_at: ISO 8601 UTC reference timestamp used to scope
            Copilot session events for the tracked head SHA.
        ci_passed: Whether CI has passed for this SHA (always True when first written).
        copilot_session_terminal: Whether a terminal session event was found.
        copilot_session_outcome: One of ``"pending"``, ``"success"``, ``"failure"``.
        squash_done: Whether the squash has been executed.
    """
    body = _build_squash_wait_body(
        pr_number=pr_number,
        sha=sha,
        attempt=attempt,
        head_pushed_at=head_pushed_at,
        ci_passed=ci_passed,
        copilot_session_terminal=copilot_session_terminal,
        copilot_session_outcome=copilot_session_outcome,
        squash_done=squash_done,
    )
    existing = provider.find_comment(pr_number, SQUASH_WAIT_MARKER_PREFIX)
    if existing is not None:
        provider.update_comment(existing[0], body)
    else:
        provider.post_comment(pr_number, body)


def delete_squash_wait_marker(
    provider: CIPlatformProvider,
    pr_number: int,
) -> None:
    """Finalise the squash-wait marker after squash completes.

    Updates the marker comment to a completion note so that the
    ai-pr-loop-throttler no longer re-triggers for this PR.

    Args:
        provider: CI platform provider for API calls.
        pr_number: Pull request number.
    """
    existing = provider.find_comment(pr_number, SQUASH_WAIT_MARKER_PREFIX)
    if existing is None:
        return
    now = datetime.now(UTC).isoformat()
    completed_body = f"<!-- squash-wait-completed -->\nSquash-wait completed for PR #{pr_number} at {now}"
    provider.update_comment(existing[0], completed_body)


def check_edit_relevance(event: EventPayload) -> tuple[bool, str]:
    """Check whether an edited PR event is relevant for pipeline processing.

    This guard implements the edit-relevance preflight: for ``edited`` events
    where the provider reliably reports which fields changed, the pipeline
    should only proceed if the title or base branch was modified.  Body-only
    edits (or edits to other non-title/non-base fields) are irrelevant and
    should be skipped.

    The guard fails open: if the event is not ``edited``, or if the provider
    could not determine what changed (``edit_changes_known=False``), the
    pipeline proceeds normally.

    Args:
        event: Normalized event payload from a CI provider.

    Returns:
        Tuple of ``(should_skip, reason)``.  When ``should_skip`` is True,
        the caller should exit early with an INFO log containing the reason.
        When False, ``reason`` is an empty string and the pipeline continues.
    """
    if event.action != "edited":
        return (False, "")

    if not event.edit_changes_known:
        return (False, "")

    if event.title_changed or event.base_changed:
        return (False, "")

    return (True, "edited event with no title or base change")
