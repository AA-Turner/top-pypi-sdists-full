"""Deterministic mutation leaf for AI PR Loop supervision control operations."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections.abc import Mapping, Sequence
from typing import Any, cast

from agentic_devtools.cli.ci.comment_format import format_ai_pr_loop_comment, normalize_ai_pr_loop_comment
from agentic_devtools.cli.ci.credential_roles import (
    AI_PR_LOOP_BOOKKEEPING_TOKEN,
    DEFAULT_CLASSIC_REPO_WORKFLOW_PAT,
    require_ai_pr_loop_bookkeeping_token,
)
from agentic_devtools.cli.ci.supervision_control import (
    CONTROL_MARKER,
    IGNORE_LABEL,
    SUPERVISED_LABEL,
    Checkpoint,
    ControlError,
    HoldReceipt,
    PRObservation,
    QuarantineReceipt,
    SupervisionControl,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError
from agentic_devtools.cli.subprocess_utils import run_safe

# Bounded allowlist of AI PR Loop workflow files this leaf is permitted to observe or
# mutate. Any workflow outside this set is ignored by ``parse_workflow_states`` so an
# unrelated repository workflow can never be disabled/enabled by this command.
LOOP_WORKFLOW_FILES: tuple[str, ...] = (
    "ai-pr-loop.yml",
    "ai-pr-loop-dispatcher.yml",
    "ai-pr-loop-redispatch.yml",
    "ai-pr-loop-supervisor.yml",
    "ai-pr-loop-throttler.yml",
    "ai-pr-loop-trusted-events.yml",
    "ai-pr-loop-watchdog.yml",
)
MAX_MANAGED_PRS = 1000
CONTROL_ISSUE_COMMENT_PAGE_SIZE = 100
CONTROL_STATE_INDEX_MAX_COMMENT_CHARS = 60_000
OPERATION_RECEIPT_MARKER = "<!-- ai-pr-loop-supervision:receipt:v1 -->"
CONTROL_STATE_INDEX_MARKER = "<!-- ai-pr-loop-supervision:state-index:v1 -->"
_CONTROL_ISSUE_COMMENTS_QUERY = f"""
query($owner:String!, $repo:String!, $number:Int!) {{
  repository(owner:$owner, name:$repo) {{
    issue(number:$number) {{
      comments(last:{CONTROL_ISSUE_COMMENT_PAGE_SIZE}) {{
        nodes {{ body author {{ login }} }}
        pageInfo {{ hasPreviousPage }}
      }}
    }}
  }}
}}
"""
_LEGACY_CONTROL_ISSUE_COMMENTS_QUERY = f"""
query($owner:String!, $repo:String!, $number:Int!, $after:String) {{
  repository(owner:$owner, name:$repo) {{
    issue(number:$number) {{
      comments(first:{CONTROL_ISSUE_COMMENT_PAGE_SIZE}, after:$after) {{
        nodes {{ body author {{ login }} }}
        pageInfo {{ hasNextPage endCursor }}
      }}
    }}
  }}
}}
"""


def parse_expected_heads(values: Sequence[str]) -> dict[int, str]:
    """Parse guarded PR specifications in ``number=head`` form."""
    result: dict[int, str] = {}
    for value in values:
        number_text, separator, head = value.partition("=")
        if not separator or not number_text.isdigit() or int(number_text) <= 0 or not head.strip():
            raise ValueError("PR values must use positive number=head form")
        number = int(number_text)
        if number in result:
            raise ValueError(f"duplicate PR number #{number}")
        result[number] = head.strip()
    return result


def build_parser() -> argparse.ArgumentParser:
    """Build the explicit control command parser."""
    parser = argparse.ArgumentParser(description="Apply verified AI PR Loop supervision control mutations")
    parser.add_argument("--repo", default=None, help="Repository in owner/repo format")
    subparsers = parser.add_subparsers(dest="operation", required=True)
    subparsers.add_parser("status")
    subparsers.add_parser("ensure-labels")
    quarantine = subparsers.add_parser("quarantine")
    quarantine.add_argument("--pr", action="append", required=True, help="Guarded PR in number=head form")
    restore = subparsers.add_parser("restore-prs")
    restore.add_argument("--receipt", required=True, help="JSON quarantine receipt")
    subparsers.add_parser("hold")
    resume = subparsers.add_parser("resume")
    resume.add_argument("--receipt", required=True, help="JSON hold receipt")
    checkpoint = subparsers.add_parser("checkpoint")
    checkpoint.add_argument("--run-id", required=True, help="decimal GitHub Actions run ID")
    checkpoint.add_argument("--payload", required=True, help="JSON checkpoint payload")
    return parser


def parse_pr_observation(raw: object) -> PRObservation:
    """Validate one ``gh pr view --json number,headRefOid,labels`` payload."""
    if not isinstance(raw, dict):
        raise ValueError("PR observation payload must be an object")
    number = raw.get("number")
    head = raw.get("headRefOid")
    labels_raw = raw.get("labels")
    if not isinstance(number, int) or isinstance(number, bool) or number <= 0:
        raise ValueError("PR observation requires a positive integer number")
    if not isinstance(head, str) or not head.strip():
        raise ValueError("PR observation requires a head SHA")
    if not isinstance(labels_raw, list) or not all(
        isinstance(item, dict) and isinstance(item.get("name"), str) for item in labels_raw
    ):
        raise ValueError("PR observation labels must be a list of named label objects")
    return PRObservation(number, head, frozenset(item["name"] for item in labels_raw))


def parse_pr_list(raw: object) -> list[PRObservation]:
    """Validate a ``gh pr list`` array payload."""
    if not isinstance(raw, list):
        raise ValueError("PR list payload must be an array")
    return [parse_pr_observation(item) for item in raw]


_ACTIVE_WORKFLOW_STATE = "active"
_DISABLED_WORKFLOW_STATES = frozenset({"disabled_manually", "disabled_inactivity", "disabled_fork"})


def parse_workflow_states(raw: object, *, known: frozenset[str] = frozenset(LOOP_WORKFLOW_FILES)) -> dict[str, bool]:
    """Validate ``gh workflow list --json name,path,state`` restricted to known loop workflows.

    Fails closed on any ``state`` value outside the documented GitHub Actions
    workflow-state enum (``active`` or one of the ``disabled_*`` values) so an
    unrecognized provider state can never be silently treated as either
    enabled or disabled.
    """
    if not isinstance(raw, list):
        raise ValueError("workflow list payload must be an array")
    states: dict[str, bool] = {}
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError("workflow list entries must be objects")
        path = item.get("path")
        state = item.get("state")
        if not isinstance(path, str) or not isinstance(state, str):
            raise ValueError("workflow list entries require path and state strings")
        name = path.rsplit("/", 1)[-1]
        if name not in known:
            continue
        if name in states:
            raise ValueError(f"duplicate workflow evidence for {name}")
        if state == _ACTIVE_WORKFLOW_STATE:
            states[name] = True
        elif state in _DISABLED_WORKFLOW_STATES:
            states[name] = False
        else:
            raise ValueError(f"unknown workflow state {state!r} for {name}")
    return states


def verify_complete_workflow_set(
    states: Mapping[str, bool], *, required: frozenset[str] = frozenset(LOOP_WORKFLOW_FILES)
) -> None:
    """Fail closed unless every required loop workflow has observed evidence.

    A global hold or resume must never proceed on partial evidence: if the
    provider's ``gh workflow list`` response is missing any known loop
    workflow, a hold could silently leave that workflow running (or a resume
    could silently leave it disabled) while reporting success.
    """
    missing = required - states.keys()
    if missing:
        raise RuntimeError(f"incomplete workflow evidence, missing: {sorted(missing)}")


def parse_label_names(raw: object) -> frozenset[str]:
    """Validate a ``gh label list --json name`` payload."""
    if not isinstance(raw, list) or not all(
        isinstance(item, dict) and isinstance(item.get("name"), str) for item in raw
    ):
        raise ValueError("label list payload must be an array of named label objects")
    return frozenset(item["name"] for item in raw)


def parse_comment_bodies(raw: object, *, trusted_author: str | set[str]) -> list[str]:
    """Validate a GraphQL issue-comment response into ordered comment bodies."""
    trusted_authors = (
        {trusted_author.casefold()}
        if isinstance(trusted_author, str) and trusted_author.strip()
        else {author.casefold() for author in trusted_author if isinstance(author, str) and author.strip()}
        if isinstance(trusted_author, set)
        else set()
    )
    if not trusted_authors:
        raise ValueError("trusted author is required to read control comments")
    if not isinstance(raw, dict):
        raise ValueError("issue comments payload must be an object")
    data = raw.get("data")
    if not isinstance(data, dict):
        raise ValueError("issue comments payload requires a data object")
    repository = data.get("repository")
    if not isinstance(repository, dict):
        raise ValueError("issue comments payload requires a repository object")
    issue = repository.get("issue")
    if not isinstance(issue, dict):
        raise ValueError("issue comments payload requires an issue object")
    connection = issue.get("comments")
    if not isinstance(connection, dict):
        raise ValueError("issue comments payload requires a comments connection")
    comments = connection.get("nodes")
    if not isinstance(comments, list):
        raise ValueError("issue comments payload requires a comments nodes array")
    bodies: list[str] = []
    for comment in comments:
        if not isinstance(comment, dict):
            raise ValueError("issue comment entries must be objects")
        author = comment.get("author")
        login = author.get("login") if isinstance(author, dict) else None
        if not isinstance(login, str) or login.casefold() not in trusted_authors:
            continue
        body = comment.get("body", "")
        if not isinstance(body, str):
            raise ValueError("issue comment body must be a string")
        normalized_body = normalize_ai_pr_loop_comment(body)
        if normalized_body is not None:
            bodies.append(normalized_body)
        elif any(marker in body for marker in (CONTROL_MARKER, OPERATION_RECEIPT_MARKER, CONTROL_STATE_INDEX_MARKER)):
            raise ValueError("trusted control comment has a malformed terminal label")
    return bodies


def _read_control_issue_comments(repo: str, issue_number: int, trusted_author: str | set[str]) -> list[str]:
    """Read an indexed control state, migrating legacy comment history when needed."""
    owner, repository = repo.split("/")
    recent_response = _run_gh(
        [
            "api",
            "graphql",
            "-f",
            f"query={_CONTROL_ISSUE_COMMENTS_QUERY}",
            "-F",
            f"owner={owner}",
            "-F",
            f"repo={repository}",
            "-F",
            f"number={issue_number}",
        ]
    )
    recent = parse_comment_bodies(recent_response, trusted_author=trusted_author)
    data = recent_response.get("data") if isinstance(recent_response, dict) else None
    repository_data = data.get("repository") if isinstance(data, dict) else None
    issue_data = repository_data.get("issue") if isinstance(repository_data, dict) else None
    connection = issue_data.get("comments") if isinstance(issue_data, dict) else None
    page_info = connection.get("pageInfo") if isinstance(connection, dict) else None
    if not isinstance(page_info, dict) or type(page_info.get("hasPreviousPage")) is not bool:
        raise ValueError("issue comments payload requires valid pagination information")

    index_candidates: list[tuple[int, list[str]]] = []
    shard_groups: dict[tuple[str, int], dict[int, tuple[int, list[str]]]] = {}
    for position, body in enumerate(recent):
        if not body.startswith(f"{CONTROL_STATE_INDEX_MARKER}\n"):
            continue
        try:
            index = json.loads(body.split("\n", 1)[1])
        except json.JSONDecodeError as exc:
            raise RuntimeError("stored control state index JSON is invalid") from exc
        if not isinstance(index, dict) or type(index.get("version")) is not int:
            raise RuntimeError("stored control state index is malformed")
        if index["version"] == 1:
            if not isinstance(index.get("entries"), list) or not all(
                isinstance(entry, str) for entry in index["entries"]
            ):
                raise RuntimeError("stored control state index is malformed")
            index_candidates.append((position, index["entries"]))
            continue
        shard_id = index.get("snapshot_id")
        shard_index = index.get("shard_index")
        shard_count = index.get("shard_count")
        entries = index.get("entries")
        if (
            index["version"] != 2
            or not isinstance(shard_id, str)
            or len(shard_id) != 64
            or type(shard_index) is not int
            or type(shard_count) is not int
            or shard_count <= 0
            or shard_index < 0
            or shard_index >= shard_count
            or not isinstance(entries, list)
            or not all(isinstance(entry, str) for entry in entries)
        ):
            raise RuntimeError("stored control state index is malformed")
        shards = shard_groups.setdefault((shard_id, shard_count), {})
        shards[shard_index] = (position, entries)

    for (shard_id, shard_count), shards in shard_groups.items():
        if len(shards) != shard_count:
            continue
        entries = [entry for shard_index in range(shard_count) for entry in shards[shard_index][1]]
        serialized_entries = json.dumps(entries, sort_keys=True, separators=(",", ":"))
        if hashlib.sha256(serialized_entries.encode()).hexdigest() != shard_id:
            raise RuntimeError("stored control state index shard digest mismatch")
        index_candidates.append((max(shards[shard_count - 1][0], 0), entries))

    if index_candidates:
        index_position, entries = max(index_candidates, key=lambda candidate: candidate[0])
        return [*entries, *recent[index_position + 1 :]]

    if not page_info["hasPreviousPage"]:
        return recent

    bodies: list[str] = []
    after = "null"
    while True:
        response = _run_gh(
            [
                "api",
                "graphql",
                "-f",
                f"query={_LEGACY_CONTROL_ISSUE_COMMENTS_QUERY}",
                "-F",
                f"owner={owner}",
                "-F",
                f"repo={repository}",
                "-F",
                f"number={issue_number}",
                "-F",
                f"after={after}",
            ]
        )
        bodies.extend(parse_comment_bodies(response, trusted_author=trusted_author))
        data = response.get("data") if isinstance(response, dict) else None
        repository_data = data.get("repository") if isinstance(data, dict) else None
        issue_data = repository_data.get("issue") if isinstance(repository_data, dict) else None
        connection = issue_data.get("comments") if isinstance(issue_data, dict) else None
        page_info = connection.get("pageInfo") if isinstance(connection, dict) else None
        if not isinstance(page_info, dict) or type(page_info.get("hasNextPage")) is not bool:
            raise ValueError("issue comments payload requires valid pagination information")
        if not page_info["hasNextPage"]:
            return bodies
        cursor = page_info.get("endCursor")
        if not isinstance(cursor, str) or not cursor.strip():
            raise ValueError("issue comments pagination requires a valid end cursor")
        after = cursor


def _write_control_issue_state_index(
    repo: str,
    issue_number: int,
    trusted_author: str | set[str],
    control: SupervisionControl,
    bodies: list[str],
    *,
    _retry_attempt: int = 0,
) -> list[str]:
    """Persist a compact snapshot, retaining active receipts and recent retry records."""
    operation_records: list[tuple[str, dict[str, Any]]] = []
    for body in bodies:
        if not body.startswith(f"{OPERATION_RECEIPT_MARKER}\n"):
            continue
        try:
            raw = json.loads(body.split("\n", 1)[1])
        except json.JSONDecodeError as exc:
            raise RuntimeError("stored operation receipt JSON is invalid") from exc
        if (
            not isinstance(raw, dict)
            or not isinstance(raw.get("operation"), str)
            or not isinstance(raw.get("idempotency_key"), str)
            or not isinstance(raw.get("receipt"), dict)
            or ("completed" in raw and type(raw["completed"]) is not bool)
        ):
            raise RuntimeError("stored operation receipt is malformed")
        find_operation_receipt(control, [body], raw["operation"], raw["idempotency_key"])
        operation_records.append((body, raw))

    quarantine_owners_by_head: dict[tuple[int, str], list[str]] = {}
    for body, raw in operation_records:
        if raw["operation"] != "quarantine" or raw.get("completed") is not True:
            continue
        receipt = find_operation_receipt(control, [body], "quarantine", raw["idempotency_key"])
        if not isinstance(receipt, QuarantineReceipt):
            raise RuntimeError("stored quarantine receipt is malformed")
        for number in receipt.ignore_added:
            head_sha = receipt.heads[number]
            quarantine_owners_by_head.setdefault((number, head_sha), []).append(raw["idempotency_key"])
    latest_quarantine_keys = {keys[-1] for keys in quarantine_owners_by_head.values()}
    completed_quarantines = {
        raw["receipt"].get("quarantine_key")
        for _, raw in operation_records
        if raw["operation"] == "restore-prs" and raw.get("completed") is True
    }
    active_quarantine_keys = latest_quarantine_keys - completed_quarantines
    supersession_tombstone_keys = {
        owner_keys[-1]
        for owner_keys in quarantine_owners_by_head.values()
        if owner_keys[-1] in completed_quarantines and any(key in active_quarantine_keys for key in owner_keys[:-1])
    }
    retained_quarantine_keys = active_quarantine_keys | supersession_tombstone_keys
    latest_completed_restore_keys = {
        raw["idempotency_key"]
        for _, raw in operation_records
        if raw["operation"] == "restore-prs"
        and raw.get("completed") is True
        and raw["receipt"].get("quarantine_key") in supersession_tombstone_keys
    }
    completed_holds = {
        raw["receipt"].get("hold_key")
        for _, raw in operation_records
        if raw["operation"] == "resume" and raw.get("completed") is True
    }
    completed_restore_records = {
        raw["idempotency_key"]
        for _, raw in operation_records
        if raw["operation"] == "restore-prs" and raw.get("completed") is True
    }
    completed_resume_records = {
        raw["idempotency_key"]
        for _, raw in operation_records
        if raw["operation"] == "resume" and raw.get("completed") is True
    }
    retained_keys = {
        raw["idempotency_key"]
        for _, raw in operation_records
        if (raw["operation"] == "quarantine" and raw["idempotency_key"] in retained_quarantine_keys)
        or (raw["operation"] == "hold" and raw["idempotency_key"] not in completed_holds)
        or (
            raw["operation"] == "restore-prs"
            and (
                raw["idempotency_key"] not in completed_restore_records
                or raw["idempotency_key"] in latest_completed_restore_keys
            )
        )
        or (raw["operation"] == "resume" and raw["idempotency_key"] not in completed_resume_records)
    }
    recent_records = operation_records[-100:]
    for _, raw in recent_records:
        if raw["operation"] == "restore-prs":
            retained_keys.add(raw["receipt"].get("quarantine_key", ""))
        elif raw["operation"] == "resume":
            retained_keys.add(raw["receipt"].get("hold_key", ""))
    recent_bodies = {body for body, _ in recent_records}
    retained_bodies = {
        body for body, raw in operation_records if body in recent_bodies or raw["idempotency_key"] in retained_keys
    }
    entries = [body for body, _ in operation_records if body in retained_bodies]
    for body in reversed(bodies):
        if not body.startswith(f"{CONTROL_MARKER}\n"):
            continue
        try:
            checkpoint = control.decode_checkpoint(body)
        except ControlError:
            continue
        if checkpoint.repository == repo:
            entries.append(body)
            break

    serialized_entries = json.dumps(entries, sort_keys=True, separators=(",", ":"))
    snapshot_id = hashlib.sha256(serialized_entries.encode()).hexdigest()
    placeholder = {
        "version": 2,
        "snapshot_id": snapshot_id,
        "shard_index": (1 << 63) - 1,
        "shard_count": (1 << 63) - 1,
        "entries": [],
    }
    empty_shard_size = (
        len(f"{CONTROL_STATE_INDEX_MARKER}\n")
        + len("\n\n")
        + len("🤖 AI PR Loop ·")
        + len(json.dumps(placeholder, sort_keys=True, separators=(",", ":")))
    )
    shards: list[list[str]] = []
    current_shard: list[str] = []
    current_entries_size = 2
    for entry in entries:
        serialized_entry = json.dumps(entry, sort_keys=True, separators=(",", ":"))
        next_entries_size = current_entries_size + len(serialized_entry) + bool(current_shard)
        if empty_shard_size - 2 + next_entries_size > CONTROL_STATE_INDEX_MAX_COMMENT_CHARS:
            if not current_shard:
                raise RuntimeError("a control state index entry exceeds the comment size limit")
            shards.append(current_shard)
            current_shard = []
            current_entries_size = 2
            next_entries_size = current_entries_size + len(serialized_entry)
            if empty_shard_size - 2 + next_entries_size > CONTROL_STATE_INDEX_MAX_COMMENT_CHARS:
                raise RuntimeError("a control state index entry exceeds the comment size limit")
        current_shard.append(entry)
        current_entries_size = next_entries_size
    if entries:
        shards.append(current_shard)
    else:
        shards.append([])

    latest_bodies = _read_control_issue_comments(repo, issue_number, trusted_author)
    concurrent_entries = [body for body in latest_bodies if body not in bodies]
    if concurrent_entries:
        if _retry_attempt >= 3:
            raise RuntimeError("control state changed repeatedly during index update")
        return _write_control_issue_state_index(
            repo,
            issue_number,
            trusted_author,
            control,
            [*bodies, *concurrent_entries],
            _retry_attempt=_retry_attempt + 1,
        )

    for shard_index, shard_entries in enumerate(shards):
        encoded = f"{CONTROL_STATE_INDEX_MARKER}\n" + json.dumps(
            {
                "version": 2,
                "snapshot_id": snapshot_id,
                "shard_index": shard_index,
                "shard_count": len(shards),
                "entries": shard_entries,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        _post_control_issue_comment(repo, issue_number, encoded)
    verified = _read_control_issue_comments(repo, issue_number, trusted_author)
    if verified != entries:
        raise RuntimeError("control state index read-back mismatch")
    return verified


def find_control_issue_number(raw: object, *, trusted_author: str | set[str]) -> int | None:
    """Return the singleton trusted control issue number, or ``None`` when absent."""
    trusted_authors = (
        {trusted_author.casefold()}
        if isinstance(trusted_author, str) and trusted_author.strip()
        else {author.casefold() for author in trusted_author if isinstance(author, str) and author.strip()}
        if isinstance(trusted_author, set)
        else set()
    )
    if not trusted_authors:
        raise ValueError("trusted author is required to identify the control issue")
    if not isinstance(raw, list):
        raise ValueError("control issue lookup returned an invalid response")
    matches: list[dict[str, object]] = []
    for issue in raw:
        number = issue.get("number") if isinstance(issue, dict) else None
        body = issue.get("body") if isinstance(issue, dict) else None
        author = issue.get("author") if isinstance(issue, dict) else None
        author_login = author.get("login") if isinstance(author, dict) else None
        labels = issue.get("labels") if isinstance(issue, dict) else None
        if (
            not isinstance(issue, dict)
            or not isinstance(number, int)
            or isinstance(number, bool)
            or number <= 0
            or not isinstance(body, str)
            or not isinstance(author_login, str)
            or not author_login.strip()
            or not isinstance(labels, list)
            or not all(isinstance(label, dict) and isinstance(label.get("name"), str) for label in labels)
        ):
            raise ValueError("control issue lookup returned malformed issue entries")
        if body.partition("\n")[0] == CONTROL_MARKER and author_login.casefold() in trusted_authors:
            matches.append(issue)
    if len(matches) > 1:
        raise RuntimeError("multiple supervision control issues found")
    if not matches:
        return None
    number = matches[0]["number"]
    assert isinstance(number, int)
    return number


def parse_quarantine_receipt(raw: object) -> QuarantineReceipt:
    """Validate a serialized quarantine receipt before it can authorize ``restore-prs``."""
    if not isinstance(raw, dict):
        raise ValueError("quarantine receipt must be an object")
    run_id = raw.get("run_id")
    changed = raw.get("changed")
    heads = raw.get("heads")
    ignore_added = raw.get("ignore_added", [])
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("quarantine receipt requires a run_id")
    if not isinstance(changed, list) or not all(type(number) is int and number > 0 for number in changed):
        raise ValueError("quarantine receipt changed must contain positive PR numbers")
    if len(changed) != len(set(changed)):
        raise ValueError("quarantine receipt changed must contain unique PR numbers")
    if not isinstance(heads, dict) or not all(
        isinstance(key, str) and key.isdigit() and int(key) > 0 and isinstance(value, str) and value.strip()
        for key, value in heads.items()
    ):
        raise ValueError("quarantine receipt heads must map PR numbers to head SHAs")
    normalized_heads = {int(key): value for key, value in heads.items()}
    if len(normalized_heads) != len(heads):
        raise ValueError("quarantine receipt heads must contain unique PR numbers")
    if not isinstance(ignore_added, list) or not all(type(number) is int and number > 0 for number in ignore_added):
        raise ValueError("quarantine receipt ignore_added must contain positive PR numbers")
    if len(ignore_added) != len(set(ignore_added)):
        raise ValueError("quarantine receipt ignore_added must contain unique PR numbers")
    if not set(ignore_added).issubset(changed):
        raise ValueError("quarantine receipt ignore_added must be a subset of changed")
    if not set(changed).issubset(normalized_heads):
        raise ValueError("quarantine receipt changed must be a subset of heads")
    return QuarantineReceipt(
        run_id,
        tuple(changed),
        normalized_heads,
        tuple(ignore_added),
    )


def parse_hold_receipt(raw: object) -> HoldReceipt:
    """Validate a serialized hold receipt before it can authorize ``resume``."""
    if not isinstance(raw, dict):
        raise ValueError("hold receipt must be an object")
    run_id = raw.get("run_id")
    changed_workflows = raw.get("changed_workflows")
    previous_states = raw.get("previous_states")
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("hold receipt requires a run_id")
    if not isinstance(changed_workflows, list) or not all(
        isinstance(name, str) and name.strip() for name in changed_workflows
    ):
        raise ValueError("hold receipt changed_workflows must be a list of workflow names")
    if not isinstance(previous_states, dict) or not all(
        isinstance(key, str) and type(value) is bool for key, value in previous_states.items()
    ):
        raise ValueError("hold receipt previous_states must map workflow names to booleans")
    return HoldReceipt(run_id, tuple(changed_workflows), dict(previous_states))


def quarantine_receipt_to_json(receipt: QuarantineReceipt) -> dict[str, object]:
    """Serialize a quarantine receipt into a JSON-safe, round-trippable object."""
    return {
        "run_id": receipt.run_id,
        "changed": list(receipt.changed),
        "heads": dict(receipt.heads),
        "ignore_added": list(receipt.ignore_added),
    }


def hold_receipt_to_json(receipt: HoldReceipt) -> dict[str, object]:
    """Serialize a hold receipt into a JSON-safe, round-trippable object."""
    return {
        "run_id": receipt.run_id,
        "changed_workflows": list(receipt.changed_workflows),
        "previous_states": dict(receipt.previous_states),
    }


def build_quarantine_output(
    observations: list[PRObservation],
    expected: Mapping[int, str],
    run_id: str,
    control: SupervisionControl,
) -> dict[str, Any]:
    """Return the complete quarantine outcome, synthesizing a receipt when idempotent."""
    result = control.quarantine(observations, expected, run_id=run_id)
    expected_json = json.dumps(sorted(expected.items()), separators=(",", ":"))
    idempotency_key = f"{run_id}:quarantine:{hashlib.sha256(expected_json.encode()).hexdigest()}"
    if result is None:
        heads = {observation.number: observation.head_sha for observation in observations}
        receipt = QuarantineReceipt(run_id, (), heads, ())
        labels = {observation.number: observation.labels for observation in observations}
        return {
            "idempotent": True,
            "idempotency_key": idempotency_key,
            "receipt": receipt,
            "labels": labels,
        }
    return {
        "idempotent": False,
        "idempotency_key": idempotency_key,
        "receipt": result.receipt,
        "labels": result.labels,
    }


def build_hold_output(
    workflow_states: Mapping[str, bool],
    run_id: str,
    control: SupervisionControl,
) -> dict[str, Any]:
    """Return the complete hold outcome, synthesizing a receipt when idempotent."""
    result = control.hold(workflow_states, run_id=run_id)
    if result is None:
        return {
            "idempotent": True,
            "idempotency_key": f"{run_id}:hold",
            "receipt": HoldReceipt(run_id, (), dict(workflow_states)),
        }
    return {"idempotent": False, "idempotency_key": f"{run_id}:hold", "receipt": result.receipt}


def verify_label_state(
    expected: Mapping[int, frozenset[str]],
    observed: list[PRObservation],
    expected_heads: Mapping[int, str],
) -> None:
    """Fail closed unless observed PR heads and labels match the mutation request."""
    observed_by_number = {observation.number: observation for observation in observed}
    for number, labels in expected.items():
        observation = observed_by_number.get(number)
        if observation is None or observation.head_sha != expected_heads.get(number):
            raise RuntimeError(f"head read-back mismatch for PR #{number}")
        if observation.labels != labels:
            raise RuntimeError(f"label read-back mismatch for PR #{number}")


def verify_workflow_states(expected: Mapping[str, bool], observed: Mapping[str, bool]) -> None:
    """Fail closed unless the observed workflow states exactly match what was just applied."""
    for name, enabled in expected.items():
        if observed.get(name) != enabled:
            raise RuntimeError(f"workflow state read-back mismatch for {name}")


def verify_repo_labels(expected: frozenset[str], observed: frozenset[str]) -> None:
    """Fail closed unless every expected supervision label exists on the repository."""
    missing = expected - observed
    if missing:
        raise RuntimeError(f"labels missing after ensure-labels: {sorted(missing)}")


def _normalized_control_bodies(bodies: list[str]) -> list[str]:
    """Normalize labeled protocol comments while rejecting malformed terminal labels."""
    normalized: list[str] = []
    for body in bodies:
        value = normalize_ai_pr_loop_comment(body)
        if value is not None:
            normalized.append(value)
        elif any(marker in body for marker in (CONTROL_MARKER, OPERATION_RECEIPT_MARKER, CONTROL_STATE_INDEX_MARKER)):
            raise ValueError("trusted control comment has a malformed terminal label")
    return normalized


def latest_valid_checkpoint(
    control: SupervisionControl, bodies: list[str], expected_repository: str
) -> Checkpoint | None:
    """Return the most recent well-formed checkpoint for ``expected_repository``.

    Malformed checkpoints and checkpoints validly signed for a different
    repository are both treated as invalid history and skipped, rather than
    being reported as this repository's control state.
    """
    for body in reversed(_normalized_control_bodies(bodies)):
        if not body.startswith(CONTROL_MARKER):
            continue
        try:
            checkpoint = control.decode_checkpoint(body)
        except ControlError:
            continue
        if checkpoint.repository != expected_repository:
            continue
        return checkpoint
    return None


def find_published_checkpoint(
    control: SupervisionControl, encoded_checkpoint: str, bodies: list[str], expected_repository: str
) -> Checkpoint:
    """Return only the exact checkpoint payload posted for ``expected_repository``."""
    expected_body = normalize_ai_pr_loop_comment(encoded_checkpoint)
    if expected_body is None:
        raise RuntimeError("checkpoint payload has a malformed terminal label")
    expected = control.decode_checkpoint(expected_body)
    if expected.repository != expected_repository:
        raise RuntimeError("checkpoint read-back repository does not match")
    for body in _normalized_control_bodies(bodies):
        if body != expected_body:
            continue
        try:
            checkpoint = control.decode_checkpoint(body)
        except ControlError:
            continue
        if checkpoint == expected:
            return checkpoint
    raise RuntimeError("checkpoint read-back did not find the exact published payload")


def find_operation_receipt(
    control: SupervisionControl, bodies: list[str], operation: str, idempotency_key: str
) -> QuarantineReceipt | HoldReceipt | dict[str, object] | None:
    """Recover the durable receipt for one stable operation key."""
    bodies = _normalized_control_bodies(bodies)
    prefix = f"{OPERATION_RECEIPT_MARKER}\n"
    found: QuarantineReceipt | HoldReceipt | dict[str, object] | None = None
    for body in bodies:
        if not body.startswith(prefix):
            continue
        try:
            raw = json.loads(body[len(prefix) :])
        except json.JSONDecodeError as exc:
            raise RuntimeError("stored operation receipt JSON is invalid") from exc
        if not isinstance(raw, dict):
            raise RuntimeError("stored operation receipt must be an object")
        stored_key = raw.get("idempotency_key")
        stored_operation = raw.get("operation")
        serialized = raw.get("receipt")
        if not isinstance(stored_key, str) or not isinstance(stored_operation, str) or not isinstance(serialized, dict):
            raise RuntimeError("stored operation receipt is malformed")
        if stored_key != idempotency_key:
            continue
        if stored_operation != operation:
            raise RuntimeError("idempotency key is already used by a different operation")
        if operation == "quarantine":
            receipt: QuarantineReceipt | HoldReceipt | dict[str, object] = parse_quarantine_receipt(serialized)
        elif operation == "hold":
            receipt = parse_hold_receipt(serialized)
        elif operation == "ensure-labels":
            created = serialized.get("labels_created")
            reused = serialized.get("labels_reused")
            issue_number = serialized.get("control_issue")
            issue_created = serialized.get("control_issue_created")
            if (
                not isinstance(created, list)
                or not all(isinstance(label, str) and label for label in created)
                or not isinstance(reused, list)
                or not all(isinstance(label, str) and label for label in reused)
                or set(created) & set(reused)
                or set(created) | set(reused) != {IGNORE_LABEL, SUPERVISED_LABEL}
                or not isinstance(issue_number, int)
                or isinstance(issue_number, bool)
                or issue_number <= 0
                or type(issue_created) is not bool
            ):
                raise RuntimeError("stored ensure-labels receipt is malformed")
            receipt = {
                "labels_created": list(created),
                "labels_reused": list(reused),
                "control_issue": issue_number,
                "control_issue_created": issue_created,
            }
        elif operation == "restore-prs":
            run_id = serialized.get("run_id")
            quarantine_key = serialized.get("quarantine_key")
            changed = serialized.get("changed")
            if (
                not isinstance(run_id, str)
                or not run_id.strip()
                or not isinstance(quarantine_key, str)
                or not quarantine_key.strip()
                or not isinstance(changed, list)
                or not all(
                    isinstance(number, int) and not isinstance(number, bool) and number > 0 for number in changed
                )
            ):
                raise RuntimeError("stored restore-prs receipt is malformed")
            receipt = {"run_id": run_id, "quarantine_key": quarantine_key, "changed": list(changed)}
        elif operation == "resume":
            run_id = serialized.get("run_id")
            hold_key = serialized.get("hold_key")
            states = serialized.get("states")
            if (
                not isinstance(run_id, str)
                or not run_id.strip()
                or not isinstance(hold_key, str)
                or not hold_key.strip()
                or not isinstance(states, dict)
                or not all(
                    isinstance(name, str) and name.strip() and type(enabled) is bool for name, enabled in states.items()
                )
            ):
                raise RuntimeError("stored resume receipt is malformed")
            receipt = {"run_id": run_id, "hold_key": hold_key, "states": dict(states)}
        else:
            raise ValueError(f"unsupported durable receipt operation {operation!r}")
        if found is not None and found != receipt:
            raise RuntimeError("conflicting durable receipts share the same idempotency key")
        found = receipt
    return found


def find_hold_progress(
    control: SupervisionControl,
    bodies: list[str],
    idempotency_key: str,
    receipt: HoldReceipt,
) -> tuple[frozenset[str], frozenset[str]]:
    """Recover the monotonically persisted hold progress and mutation intents."""
    bodies = _normalized_control_bodies(bodies)
    if find_operation_receipt(control, bodies, "hold", idempotency_key) != receipt:
        raise RuntimeError("stored hold receipt does not match hold progress")
    enabled_workflows = {name for name, enabled in receipt.previous_states.items() if enabled}
    progressed: set[str] = set()
    attempted: set[str] = set()
    prefix = f"{OPERATION_RECEIPT_MARKER}\n"
    for body in bodies:
        if not body.startswith(prefix):
            continue
        raw = json.loads(body[len(prefix) :])
        if raw.get("operation") != "hold" or raw.get("idempotency_key") != idempotency_key:
            continue
        if "disabled_workflows" not in raw:
            continue
        recorded = raw["disabled_workflows"]
        if (
            not isinstance(recorded, list)
            or not all(isinstance(name, str) and name.strip() for name in recorded)
            or len(set(recorded)) != len(recorded)
        ):
            raise RuntimeError("stored hold progress is malformed")
        updated = set(recorded)
        if not updated.issubset(enabled_workflows) or not progressed.issubset(updated):
            raise RuntimeError("stored hold progress is inconsistent")
        recorded_attempts = raw.get("attempted_workflows", recorded)
        if (
            not isinstance(recorded_attempts, list)
            or not all(isinstance(name, str) and name.strip() for name in recorded_attempts)
            or len(set(recorded_attempts)) != len(recorded_attempts)
        ):
            raise RuntimeError("stored hold progress is malformed")
        updated_attempts = set(recorded_attempts)
        if (
            not updated_attempts.issubset(enabled_workflows)
            or not updated.issubset(updated_attempts)
            or not attempted.issubset(updated_attempts)
        ):
            raise RuntimeError("stored hold progress is inconsistent")
        progressed = updated
        attempted = updated_attempts
    return frozenset(progressed), frozenset(attempted)


def find_completed_operation_receipt(
    control: SupervisionControl, bodies: list[str], operation: str, idempotency_key: str
) -> dict[str, object] | None:
    """Return a durable restore/resume receipt only after its completion record is published."""
    if operation not in {"restore-prs", "resume"}:
        raise ValueError(f"unsupported completion operation {operation!r}")
    bodies = _normalized_control_bodies(bodies)
    stored = find_operation_receipt(control, bodies, operation, idempotency_key)
    if stored is None:
        return None

    prefix = f"{OPERATION_RECEIPT_MARKER}\n"
    for body in bodies:
        if not body.startswith(prefix):
            continue
        raw = json.loads(body[len(prefix) :])
        if raw.get("operation") != operation or raw.get("idempotency_key") != idempotency_key:
            continue
        completed = raw.get("completed", False)
        if type(completed) is not bool:
            raise RuntimeError("stored operation completion marker is malformed")
        if completed:
            return cast(dict[str, object], stored)
    return None


def find_latest_operation_receipt_key(control: SupervisionControl, bodies: list[str], operation: str) -> str | None:
    """Return the newest validated durable receipt key for one operation."""
    bodies = _normalized_control_bodies(bodies)
    prefix = f"{OPERATION_RECEIPT_MARKER}\n"
    for body in reversed(bodies):
        if not body.startswith(prefix):
            continue
        try:
            raw = json.loads(body[len(prefix) :])
        except json.JSONDecodeError as exc:
            raise RuntimeError("stored operation receipt JSON is invalid") from exc
        if not isinstance(raw, dict):
            raise RuntimeError("stored operation receipt must be an object")
        stored_operation = raw.get("operation")
        idempotency_key = raw.get("idempotency_key")
        if not isinstance(stored_operation, str) or not isinstance(idempotency_key, str) or not idempotency_key.strip():
            raise RuntimeError("stored operation receipt is malformed")
        if stored_operation != operation:
            continue
        try:
            find_operation_receipt(control, [body], operation, idempotency_key)
        except (RuntimeError, ValueError) as exc:
            raise RuntimeError("stored operation receipt is malformed") from exc
        return idempotency_key
    return None


def find_latest_quarantine_owner_key(
    control: SupervisionControl,
    bodies: list[str],
    number: int,
    head_sha: str,
) -> str | None:
    """Return the newest quarantine receipt that owns the ignore label for one PR head."""
    bodies = _normalized_control_bodies(bodies)
    prefix = f"{OPERATION_RECEIPT_MARKER}\n"
    for body in reversed(bodies):
        if not body.startswith(prefix):
            continue
        try:
            raw = json.loads(body[len(prefix) :])
        except json.JSONDecodeError as exc:
            raise RuntimeError("stored operation receipt JSON is invalid") from exc
        if not isinstance(raw, dict):
            raise RuntimeError("stored operation receipt must be an object")
        operation = raw.get("operation")
        key = raw.get("idempotency_key")
        if not isinstance(operation, str) or not isinstance(key, str) or not key.strip():
            raise RuntimeError("stored operation receipt is malformed")
        if operation != "quarantine":
            continue
        try:
            receipt = find_operation_receipt(control, [body], operation, key)
        except (RuntimeError, ValueError) as exc:
            raise RuntimeError("stored quarantine receipt is malformed") from exc
        if not isinstance(receipt, QuarantineReceipt):
            raise RuntimeError("stored quarantine receipt is malformed")
        completed = raw.get("completed", False)
        if type(completed) is not bool:
            raise RuntimeError("stored operation completion marker is malformed")
        if not completed:
            continue
        if number in receipt.ignore_added and receipt.heads.get(number) == head_sha:
            return key
    return None


def get_or_store_operation_receipt(
    repo: str,
    issue_number: int,
    control: SupervisionControl,
    operation: str,
    idempotency_key: str,
    proposed: QuarantineReceipt | HoldReceipt | dict[str, object],
) -> tuple[QuarantineReceipt | HoldReceipt | dict[str, object], bool]:
    """Persist a write-ahead receipt, or recover the receipt from an earlier attempt."""
    trusted_author = _trusted_control_authors()

    def read_receipts() -> list[str]:
        return _read_control_issue_comments(repo, issue_number, trusted_author)

    bodies = read_receipts()
    stored = find_operation_receipt(control, bodies, operation, idempotency_key)
    if stored is not None:
        return stored, True
    if operation == "quarantine" and isinstance(proposed, QuarantineReceipt):
        receipt_body = quarantine_receipt_to_json(proposed)
    elif operation == "hold" and isinstance(proposed, HoldReceipt):
        receipt_body = hold_receipt_to_json(proposed)
    elif isinstance(proposed, dict):
        receipt_body = proposed
    else:
        raise ValueError(f"receipt type does not match operation {operation!r}")
    encoded = f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(
        {"idempotency_key": idempotency_key, "operation": operation, "receipt": receipt_body},
        sort_keys=True,
        separators=(",", ":"),
    )
    validated = find_operation_receipt(control, [encoded], operation, idempotency_key)
    if validated != proposed:
        raise ValueError(f"receipt type does not match operation {operation!r}")
    _post_control_issue_comment(repo, issue_number, encoded)
    updated_bodies = read_receipts()
    stored = find_operation_receipt(control, updated_bodies, operation, idempotency_key)
    if stored != proposed:
        raise RuntimeError("operation receipt read-back mismatch")
    _write_control_issue_state_index(repo, issue_number, trusted_author, control, updated_bodies)
    return proposed, False


def build_status_report(
    workflows: Mapping[str, bool],
    control_issue_number: int | None,
    checkpoint: Checkpoint | None,
    prs: list[PRObservation],
) -> dict[str, object]:
    """Assemble the full status contract: workflow states, control issue, managed PRs."""
    return {
        "workflows": dict(sorted(workflows.items())),
        "control_issue": {
            "number": control_issue_number,
            "checkpoint": (
                {"run_id": checkpoint.run_id, "payload": dict(checkpoint.payload)} if checkpoint is not None else None
            ),
        },
        "managed_prs": [{"number": pr.number, "head_sha": pr.head_sha, "labels": sorted(pr.labels)} for pr in prs],
    }


def _run_gh(arguments: list[str], *, env: dict[str, str] | None = None) -> Any:
    try:
        from agentic_devtools.cli.ci.github_provider import _run_readonly_gh_command  # noqa: PLC0415

        kwargs: dict[str, Any] = {"runner": run_safe, "timeout_seconds": 60}
        if tuple(arguments[:2]) in {
            ("api", "graphql"),
            ("pr", "view"),
            ("pr", "list"),
            ("issue", "list"),
        }:
            kwargs["resource"] = "graphql"
        if env is not None:
            kwargs.update(base_env=env, read_pool=False)
        if arguments == ["api", "user"]:
            token = (env or os.environ).get(DEFAULT_CLASSIC_REPO_WORKFLOW_PAT, "").strip()
            kwargs.update(
                token=token or None,
                read_pool=False,
            )
            if token:
                kwargs["credential_identity"] = DEFAULT_CLASSIC_REPO_WORKFLOW_PAT
        result = _run_readonly_gh_command(arguments, **kwargs)
    except (OSError, subprocess.TimeoutExpired, RetryableError, ProviderRateLimitError) as exc:
        raise RuntimeError(f"GitHub CLI operation failed: {exc}") from exc
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "GitHub CLI operation failed")
    try:
        return json.loads(result.stdout) if result.stdout.strip() else None
    except json.JSONDecodeError as exc:
        raise RuntimeError("GitHub CLI returned invalid JSON") from exc


def _run_gh_text(arguments: list[str], *, env: dict[str, str] | None = None) -> str:
    if env is None:
        token = os.environ.get(DEFAULT_CLASSIC_REPO_WORKFLOW_PAT, "").strip()
        env = os.environ.copy()
        if token:
            env["GH_TOKEN"] = token
    try:
        result = run_safe(["gh", *arguments], capture_output=True, text=True, shell=False, timeout=60, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError(f"GitHub CLI operation failed: {exc}") from exc
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "GitHub CLI operation failed")
    return result.stdout.strip()


def _bookkeeping_cli_env() -> tuple[dict[str, str], str]:
    """Verify the bookkeeping role in a child-only gh environment."""
    token = require_ai_pr_loop_bookkeeping_token("write supervision control comments")
    env = os.environ.copy()
    env["GH_TOKEN"] = token
    identity = _run_gh(["api", "graphql", "-f", "query=query { viewer { login } }"], env=env)
    errors = identity.get("errors") if isinstance(identity, dict) else None
    if errors is not None and (not isinstance(errors, list) or errors):
        raise RuntimeError(f"{AI_PR_LOOP_BOOKKEEPING_TOKEN} identity could not be verified")
    data = identity.get("data") if isinstance(identity, dict) else None
    viewer = data.get("viewer") if isinstance(data, dict) else None
    login = viewer.get("login") if isinstance(viewer, dict) else None
    if not isinstance(login, str) or not login.strip():
        raise RuntimeError(f"{AI_PR_LOOP_BOOKKEEPING_TOKEN} identity could not be verified")
    normalized_login = login.strip()
    if normalized_login.casefold() != "github-actions[bot]":
        raise RuntimeError(f"{AI_PR_LOOP_BOOKKEEPING_TOKEN} identity must be github-actions[bot]")
    return env, normalized_login


def _trusted_control_authors() -> set[str]:
    """Trust the verified PAT identity and the Actions service account for reading."""
    identity = _run_gh(["api", "user"])
    login = identity.get("login") if isinstance(identity, dict) else None
    if not isinstance(login, str) or not login.strip():
        raise RuntimeError("authenticated GitHub identity is unavailable")
    authors = {login.casefold()}
    if os.environ.get("GITHUB_ACTIONS", "").strip().lower() == "true":
        _, bookkeeping_login = _bookkeeping_cli_env()
        authors.add(bookkeeping_login.casefold())
    else:
        authors.add("github-actions[bot]")
    return authors


def _post_control_issue_comment(repo: str, issue_number: int, body: str) -> None:
    """Write a labeled control comment using only the explicitly supplied bot role."""
    rendered = format_ai_pr_loop_comment(body)
    args = ["issue", "comment", str(issue_number), "--repo", repo, "--body", rendered]
    if os.environ.get("GITHUB_ACTIONS", "").strip().lower() == "true":
        env, _login = _bookkeeping_cli_env()
        _run_gh_text(args, env=env)
    else:
        _run_gh_text(args)


def _workflow_states(repo: str) -> dict[str, bool]:  # pragma: no cover - provider integration leaf
    return parse_workflow_states(_run_gh(["workflow", "list", "--repo", repo, "--all", "--json", "name,path,state"]))


def _observations(  # pragma: no cover - provider integration leaf
    repo: str, expected: Mapping[int, str]
) -> list[PRObservation]:
    observations: list[PRObservation] = []
    for number in expected:
        facts = _run_gh(["pr", "view", str(number), "--repo", repo, "--json", "number,headRefOid,labels"])
        observations.append(parse_pr_observation(facts))
    return observations


def _find_control_issue(repo: str) -> int | None:  # pragma: no cover - provider integration leaf
    """Find a trusted control issue with one author-scoped query per identity.

    The trusted set contains at most the PAT and bookkeeping identities; separate
    queries keep each author's result limit from hiding older control issues.
    """
    trusted_author = _trusted_control_authors()
    issues: list[object] = []
    for author in sorted(trusted_author):
        result = _run_gh(
            [
                "issue",
                "list",
                "--repo",
                repo,
                "--state",
                "all",
                "--search",
                "ai-pr-loop-supervision:control:v1",
                "--author",
                author,
                "--limit",
                "1000",
                "--json",
                "number,body,author,labels",
            ]
        )
        if not isinstance(result, list):
            raise RuntimeError("GitHub returned an invalid control issue list")
        issues.extend(result)
    return find_control_issue_number(issues, trusted_author=trusted_author)


def _control_issue(repo: str) -> int:  # pragma: no cover - provider integration leaf
    existing = _find_control_issue(repo)
    existing_labels = parse_label_names(
        _run_gh(["label", "list", "--repo", repo, "--search", SUPERVISED_LABEL, "--limit", "1000", "--json", "name"])
    )
    if SUPERVISED_LABEL not in existing_labels:
        _run_gh_text(["label", "create", SUPERVISED_LABEL, "--repo", repo])
    verified_labels = parse_label_names(
        _run_gh(["label", "list", "--repo", repo, "--search", SUPERVISED_LABEL, "--limit", "1000", "--json", "name"])
    )
    verify_repo_labels(frozenset({SUPERVISED_LABEL}), verified_labels)
    if existing is not None:
        return existing
    created = _run_gh_text(
        [
            "issue",
            "create",
            "--repo",
            repo,
            "--title",
            "AI PR Loop supervision control",
            "--body",
            CONTROL_MARKER,
            "--label",
            SUPERVISED_LABEL,
        ]
    )
    if not isinstance(created, str) or "/issues/" not in created:
        raise RuntimeError("control issue creation did not return a URL")
    new_number = int(created.rstrip("/").rsplit("/", 1)[1])
    verified = _find_control_issue(repo)
    if verified != new_number:
        raise RuntimeError("control issue read-back mismatch")
    return new_number


def _repo(args: argparse.Namespace) -> str:
    repo = (args.repo or os.environ.get("GITHUB_REPOSITORY", "")).strip()
    if not repo or repo.count("/") != 1:
        raise ValueError("repository must be in owner/repo form")
    owner, repository = repo.split("/")
    if not owner or not repository or any(character.isspace() for character in repo):
        raise ValueError("repository must be in owner/repo form")
    return repo


def main(argv: Sequence[str] | None = None) -> int:
    """Execute one bounded control operation and print its JSON receipt."""
    args = build_parser().parse_args(argv)
    repo = _repo(args)
    if (
        args.operation in {"ensure-labels", "quarantine", "restore-prs", "hold", "resume", "checkpoint"}
        and not os.environ.get("AGDT_SUPERVISION_LEASE_ID", "").strip()
    ):
        raise ValueError("AGDT_SUPERVISION_LEASE_ID is required for supervision mutations")
    control = SupervisionControl()

    def trusted_logins() -> set[str]:
        return _trusted_control_authors()

    def trusted_comment_bodies(issue_number: int) -> list[str]:
        return _read_control_issue_comments(repo, issue_number, trusted_logins())

    if args.operation == "status":
        workflows = _workflow_states(repo)
        verify_complete_workflow_set(workflows)
        control_issue_number = _find_control_issue(repo)
        checkpoint = None
        if control_issue_number is not None:
            bodies = trusted_comment_bodies(control_issue_number)
            checkpoint = latest_valid_checkpoint(control, bodies, repo)
        prs = parse_pr_list(
            _run_gh(
                [
                    "pr",
                    "list",
                    "--repo",
                    repo,
                    "--state",
                    "open",
                    "--label",
                    SUPERVISED_LABEL,
                    "--limit",
                    str(MAX_MANAGED_PRS + 1),
                    "--json",
                    "number,headRefOid,labels",
                ]
            )
        )
        if len(prs) > MAX_MANAGED_PRS:
            raise RuntimeError(f"managed PR list exceeds the {MAX_MANAGED_PRS}-PR status limit")
        print(json.dumps(build_status_report(workflows, control_issue_number, checkpoint, prs)))
        return 0

    if args.operation == "ensure-labels":
        run_id = os.environ.get("GITHUB_RUN_ID", "").strip()
        if not run_id:
            raise ValueError("GITHUB_RUN_ID is required for durable ensure-labels receipts")
        expected_labels = frozenset({IGNORE_LABEL, SUPERVISED_LABEL})
        observed_labels: set[str] = set()
        labels_created: list[str] = []
        labels_reused: list[str] = []
        for label in sorted(expected_labels):
            existing = parse_label_names(
                _run_gh(["label", "list", "--repo", repo, "--search", label, "--limit", "1000", "--json", "name"])
            )
            observed_labels.update(existing)
            if label in existing:
                labels_reused.append(label)
            else:
                labels_created.append(label)

        if SUPERVISED_LABEL not in observed_labels:
            _run_gh_text(["label", "create", SUPERVISED_LABEL, "--repo", repo])

        existing_issue_number = _find_control_issue(repo)
        issue_number = existing_issue_number if existing_issue_number is not None else _control_issue(repo)
        generation = {
            "run_id": run_id,
        }
        generation_fingerprint = hashlib.sha256(
            json.dumps(generation, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        idempotency_key = f"{repo}:ensure-labels:v1:{generation_fingerprint}"
        proposed_receipt = {
            "labels_created": labels_created,
            "labels_reused": labels_reused,
            "control_issue": issue_number,
            "control_issue_created": existing_issue_number is None,
        }
        receipt, _ = get_or_store_operation_receipt(
            repo,
            issue_number,
            control,
            "ensure-labels",
            idempotency_key,
            proposed_receipt,
        )
        idempotent = existing_issue_number is not None and not labels_created
        if (
            not isinstance(receipt, dict)
            or receipt.get("control_issue") != issue_number
            or type(receipt.get("control_issue")) is not int
            or type(receipt.get("control_issue_created")) is not bool
        ):
            raise RuntimeError("stored ensure-labels receipt does not match the control issue")

        for label in sorted(expected_labels):
            existing = parse_label_names(
                _run_gh(["label", "list", "--repo", repo, "--search", label, "--limit", "1000", "--json", "name"])
            )
            if label not in existing:
                _run_gh_text(["label", "create", label, "--repo", repo])
            verified = parse_label_names(
                _run_gh(["label", "list", "--repo", repo, "--search", label, "--limit", "1000", "--json", "name"])
            )
            verify_repo_labels(frozenset({label}), verified)
        print(
            json.dumps(
                {
                    "idempotent": idempotent,
                    "idempotency_key": idempotency_key,
                    "labels": sorted(expected_labels),
                    "control_issue": issue_number,
                    "receipt": receipt,
                }
            )
        )
        return 0

    if args.operation == "quarantine":
        expected = parse_expected_heads(args.pr)
        observations = _observations(repo, expected)
        run_id = os.environ.get("GITHUB_RUN_ID", "").strip()
        if not run_id:
            raise ValueError("GITHUB_RUN_ID is required for durable quarantine receipts")
        outcome = build_quarantine_output(observations, expected, run_id, control)
        issue_number = _control_issue(repo)
        receipt_bodies = trusted_comment_bodies(issue_number)
        restore_key = f"{outcome['idempotency_key']}:restore"
        completed_restore = find_completed_operation_receipt(control, receipt_bodies, "restore-prs", restore_key)
        if completed_restore is not None:
            if (
                completed_restore.get("run_id") != run_id
                or completed_restore.get("quarantine_key") != outcome["idempotency_key"]
            ):
                raise RuntimeError("stored restore-prs receipt does not match the quarantine receipt")
            raise RuntimeError("quarantine generation has already been restored; use a new GITHUB_RUN_ID")
        existing_ignore_labels = parse_label_names(
            _run_gh(["label", "list", "--repo", repo, "--search", IGNORE_LABEL, "--limit", "1000", "--json", "name"])
        )
        if IGNORE_LABEL not in existing_ignore_labels:
            _run_gh_text(["label", "create", IGNORE_LABEL, "--repo", repo])
        verified_ignore_labels = parse_label_names(
            _run_gh(["label", "list", "--repo", repo, "--search", IGNORE_LABEL, "--limit", "1000", "--json", "name"])
        )
        verify_repo_labels(frozenset({IGNORE_LABEL}), verified_ignore_labels)
        receipt, _ = get_or_store_operation_receipt(
            repo,
            issue_number,
            control,
            "quarantine",
            outcome["idempotency_key"],
            outcome["receipt"],
        )
        if not isinstance(receipt, QuarantineReceipt) or receipt.heads != expected:
            raise RuntimeError("stored quarantine receipt does not match the requested PR heads")
        initial_labels = {observation.number: observation.labels for observation in observations}
        before_mutation = _observations(repo, expected)
        verify_label_state(initial_labels, before_mutation, expected)
        desired_labels = {
            observation.number: observation.labels | {IGNORE_LABEL, SUPERVISED_LABEL} for observation in observations
        }
        current_labels = {observation.number: observation.labels for observation in observations}
        attempted_additions: dict[int, set[str]] = {}
        for number, labels in desired_labels.items():
            for label in (SUPERVISED_LABEL, IGNORE_LABEL):
                if label in labels and label not in current_labels[number]:
                    attempted_additions.setdefault(number, set()).add(label)
                    _run_gh_text(["pr", "edit", str(number), "--repo", repo, "--add-label", label])
        refreshed = _observations(repo, expected)
        try:
            verify_label_state(desired_labels, refreshed, expected)
        except RuntimeError as verification_error:
            refreshed_by_number = {observation.number: observation for observation in refreshed}
            moved_heads = {
                number
                for number, observation in refreshed_by_number.items()
                if observation.head_sha != expected.get(number)
            }
            if moved_heads:
                compensation_observations = _observations(repo, {number: expected[number] for number in moved_heads})
                compensation_by_number = {observation.number: observation for observation in compensation_observations}
                compensation_targets: dict[int, set[str]] = {}
                for number in moved_heads:
                    observation = compensation_by_number.get(number)
                    if observation is None or observation.head_sha == expected[number]:
                        continue
                    newly_added_labels = attempted_additions.get(number, set()) & observation.labels
                    if newly_added_labels:
                        compensation_targets[number] = newly_added_labels
                for number, labels_to_remove in compensation_targets.items():
                    for label in labels_to_remove:
                        _run_gh_text(["pr", "edit", str(number), "--repo", repo, "--remove-label", label])
                if compensation_targets:
                    compensated = _observations(repo, {number: expected[number] for number in compensation_targets})
                    compensated_by_number = {observation.number: observation for observation in compensated}
                    if any(
                        observation.head_sha != expected[number] and labels_to_remove & observation.labels
                        for number, labels_to_remove in compensation_targets.items()
                        if (observation := compensated_by_number.get(number)) is not None
                    ):
                        raise RuntimeError("quarantine label compensation read-back mismatch") from verification_error
            raise
        completion_body = f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(
            {
                "idempotency_key": outcome["idempotency_key"],
                "operation": "quarantine",
                "receipt": quarantine_receipt_to_json(receipt),
                "completed": True,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        if completion_body not in receipt_bodies:
            _post_control_issue_comment(repo, issue_number, completion_body)
            completed_bodies = _write_control_issue_state_index(
                repo,
                issue_number,
                trusted_logins(),
                control,
                trusted_comment_bodies(issue_number),
            )
            if completion_body not in completed_bodies:
                raise RuntimeError("quarantine completion receipt read-back mismatch")
        idempotent = all(current_labels[number] == labels for number, labels in desired_labels.items())
        print(
            json.dumps(
                {
                    "idempotent": idempotent,
                    "idempotency_key": outcome["idempotency_key"],
                    "receipt": quarantine_receipt_to_json(receipt),
                }
            )
        )
        return 0

    if args.operation == "restore-prs":
        receipt = parse_quarantine_receipt(json.loads(args.receipt))
        restore_issue_number = _find_control_issue(repo)
        if restore_issue_number is None:
            raise RuntimeError("no trusted supervision control issue exists for the quarantine receipt")
        expected_json = json.dumps(sorted(receipt.heads.items()), separators=(",", ":"))
        idempotency_key = f"{receipt.run_id}:quarantine:{hashlib.sha256(expected_json.encode()).hexdigest()}"
        receipt_bodies = trusted_comment_bodies(restore_issue_number)
        stored = find_operation_receipt(
            control,
            receipt_bodies,
            "quarantine",
            idempotency_key,
        )
        if stored != receipt:
            raise RuntimeError("restore receipt does not match a durable quarantine receipt")
        active_owned = tuple(
            number
            for number in receipt.ignore_added
            if find_latest_quarantine_owner_key(control, receipt_bodies, number, receipt.heads[number])
            == idempotency_key
        )
        active_heads = (
            receipt.heads if not receipt.ignore_added else {number: receipt.heads[number] for number in active_owned}
        )
        active_receipt = QuarantineReceipt(receipt.run_id, receipt.changed, active_heads, active_owned)
        restore_key = f"{idempotency_key}:restore"
        completed_restore = find_completed_operation_receipt(control, receipt_bodies, "restore-prs", restore_key)
        if completed_restore is not None:
            if (
                completed_restore.get("run_id") != receipt.run_id
                or completed_restore.get("quarantine_key") != idempotency_key
            ):
                raise RuntimeError("stored restore-prs receipt does not match the quarantine receipt")
            completed_observations = _observations(repo, dict(active_heads)) if active_heads else []
            completed_by_number = {observation.number: observation for observation in completed_observations}
            if set(completed_by_number) != set(active_heads) or any(
                completed_by_number[number].head_sha != expected_head for number, expected_head in active_heads.items()
            ):
                raise RuntimeError("completed restore-prs state read-back mismatch: PR heads changed")
            if any(
                number not in completed_by_number or IGNORE_LABEL in completed_by_number[number].labels
                for number in cast(list[int], completed_restore["changed"])
                if number in active_owned
            ):
                raise RuntimeError("completed restore-prs state read-back mismatch: owned ignore label is present")
            print(
                json.dumps(
                    {
                        "idempotent": True,
                        "idempotency_key": restore_key,
                        "run_id": receipt.run_id,
                        "changed": completed_restore["changed"],
                        "receipt": completed_restore,
                    }
                )
            )
            return 0
        observations = _observations(repo, dict(active_heads)) if active_heads else []
        result = control.restore_prs(observations, active_receipt)
        proposed_restore_receipt: dict[str, object] = {
            "run_id": receipt.run_id,
            "quarantine_key": idempotency_key,
            "changed": list(result.changed),
        }
        restore_receipt, _ = get_or_store_operation_receipt(
            repo,
            restore_issue_number,
            control,
            "restore-prs",
            restore_key,
            proposed_restore_receipt,
        )
        if (
            not isinstance(restore_receipt, dict)
            or restore_receipt.get("run_id") != receipt.run_id
            or restore_receipt.get("quarantine_key") != idempotency_key
        ):
            raise RuntimeError("stored restore-prs receipt does not match the quarantine receipt")
        current_by_number = {observation.number: observation for observation in observations}
        idempotent = True
        restore_targets = [number for number in cast(list[int], restore_receipt["changed"]) if number in active_owned]
        for number in restore_targets:
            observation = current_by_number[number]
            if IGNORE_LABEL in observation.labels:
                _run_gh_text(["pr", "edit", str(number), "--repo", repo, "--remove-label", IGNORE_LABEL])
                idempotent = False
        if result.labels:
            try:
                refreshed = _observations(repo, dict(active_heads))
                verify_label_state(result.labels, refreshed, active_heads)
            except (
                RuntimeError,
                ValueError,
            ):
                try:
                    for number in restore_targets:
                        _run_gh_text(["pr", "edit", str(number), "--repo", repo, "--add-label", IGNORE_LABEL])
                    recovered = _observations(repo, dict.fromkeys(restore_targets, ""))
                    recovered_by_number = {observation.number: observation for observation in recovered}
                    if any(
                        number not in recovered_by_number or IGNORE_LABEL not in recovered_by_number[number].labels
                        for number in restore_targets
                    ):
                        raise RuntimeError("restore-prs quarantine label recovery read-back mismatch")
                except Exception as recovery_error:
                    raise RuntimeError("restore-prs failed to reapply the quarantine ignore label") from recovery_error
                raise
        completion_body = f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(
            {
                "idempotency_key": restore_key,
                "operation": "restore-prs",
                "receipt": restore_receipt,
                "completed": True,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        _post_control_issue_comment(repo, restore_issue_number, completion_body)
        completed_bodies = _write_control_issue_state_index(
            repo,
            restore_issue_number,
            trusted_logins(),
            control,
            trusted_comment_bodies(restore_issue_number),
        )
        completed_restore = find_completed_operation_receipt(control, completed_bodies, "restore-prs", restore_key)
        if completed_restore != restore_receipt:
            raise RuntimeError("restore-prs completion receipt read-back mismatch")
        print(
            json.dumps(
                {
                    "idempotent": idempotent,
                    "idempotency_key": restore_key,
                    "run_id": receipt.run_id,
                    "changed": restore_receipt["changed"],
                    "receipt": restore_receipt,
                }
            )
        )
        return 0

    if args.operation == "hold":
        run_id = os.environ.get("GITHUB_RUN_ID", "").strip()
        if not run_id:
            raise ValueError("GITHUB_RUN_ID is required for durable hold receipts")
        states = _workflow_states(repo)
        verify_complete_workflow_set(states)
        outcome = build_hold_output(states, run_id, control)
        issue_number = _control_issue(repo)
        receipt_bodies = trusted_comment_bodies(issue_number)
        latest_hold_key = find_latest_operation_receipt_key(control, receipt_bodies, "hold")
        if latest_hold_key is not None:
            latest_hold = find_operation_receipt(control, receipt_bodies, "hold", latest_hold_key)
            if not isinstance(latest_hold, HoldReceipt):
                raise RuntimeError("stored active hold receipt is malformed")
            completed_resume = find_completed_operation_receipt(
                control,
                receipt_bodies,
                "resume",
                f"{latest_hold.run_id}:resume",
            )
            if completed_resume is None and latest_hold_key != outcome["idempotency_key"]:
                raise RuntimeError("cannot create a new hold while an unresolved hold receipt exists")
            if completed_resume is not None and latest_hold_key == outcome["idempotency_key"]:
                raise RuntimeError("hold generation has already been resumed; use a new GITHUB_RUN_ID")
        hold_receipt, _ = get_or_store_operation_receipt(
            repo,
            issue_number,
            control,
            "hold",
            outcome["idempotency_key"],
            outcome["receipt"],
        )
        if not isinstance(hold_receipt, HoldReceipt) or set(hold_receipt.previous_states) != set(LOOP_WORKFLOW_FILES):
            raise RuntimeError("stored hold receipt does not cover the complete workflow set")
        receipt_bodies = trusted_comment_bodies(issue_number)
        persisted_progress, persisted_attempts = find_hold_progress(
            control, receipt_bodies, outcome["idempotency_key"], hold_receipt
        )
        progressed = set(persisted_progress)
        attempted = set(persisted_attempts)

        def persist_hold_progress() -> None:
            progress_body = f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(
                {
                    "idempotency_key": outcome["idempotency_key"],
                    "operation": "hold",
                    "receipt": hold_receipt_to_json(hold_receipt),
                    "disabled_workflows": sorted(progressed),
                    "attempted_workflows": sorted(attempted),
                },
                sort_keys=True,
                separators=(",", ":"),
            )
            _post_control_issue_comment(repo, issue_number, progress_body)
            progress_bodies = trusted_comment_bodies(issue_number)
            if find_hold_progress(control, progress_bodies, outcome["idempotency_key"], hold_receipt) != (
                frozenset(progressed),
                frozenset(attempted),
            ):
                raise RuntimeError("hold progress read-back mismatch")
            _write_control_issue_state_index(
                repo,
                issue_number,
                trusted_logins(),
                control,
                progress_bodies,
            )

        current_states = _workflow_states(repo)
        verify_complete_workflow_set(current_states)
        for workflow, was_enabled in hold_receipt.previous_states.items():
            if current_states[workflow] != was_enabled and not (
                was_enabled and workflow in attempted and not current_states[workflow]
            ):
                raise RuntimeError(f"workflow state mismatch for {workflow}")
        recovered_workflows = {
            workflow
            for workflow, was_enabled in hold_receipt.previous_states.items()
            if was_enabled and workflow in attempted and not current_states[workflow] and workflow not in progressed
        }
        if recovered_workflows:
            progressed.update(recovered_workflows)
            persist_hold_progress()
        for workflow, was_enabled in hold_receipt.previous_states.items():
            if not was_enabled or workflow in progressed:
                continue
            attempted.add(workflow)
            persist_hold_progress()
            _run_gh_text(["workflow", "disable", workflow, "--repo", repo])
            progressed.add(workflow)
            persist_hold_progress()
            current_states = _workflow_states(repo)
            verify_complete_workflow_set(current_states)
            for name, initially_enabled in hold_receipt.previous_states.items():
                expected_enabled = initially_enabled and name not in progressed
                if current_states[name] != expected_enabled:
                    raise RuntimeError(f"workflow state mismatch for {name}")
        refreshed_states = _workflow_states(repo)
        verify_complete_workflow_set(refreshed_states)
        verify_workflow_states({workflow: False for workflow in states}, refreshed_states)
        idempotent = not any(states.values())
        print(
            json.dumps(
                {
                    "idempotent": idempotent,
                    "idempotency_key": outcome["idempotency_key"],
                    "receipt": hold_receipt_to_json(hold_receipt),
                }
            )
        )
        return 0

    if args.operation == "resume":
        resume_receipt = parse_hold_receipt(json.loads(args.receipt))
        if set(resume_receipt.previous_states) != set(LOOP_WORKFLOW_FILES):
            raise RuntimeError("hold receipt does not cover the complete workflow set")
        resume_issue_number = _find_control_issue(repo)
        if resume_issue_number is None:
            raise RuntimeError("no trusted supervision control issue exists for the hold receipt")
        receipt_bodies = trusted_comment_bodies(resume_issue_number)
        stored = find_operation_receipt(
            control,
            receipt_bodies,
            "hold",
            f"{resume_receipt.run_id}:hold",
        )
        if stored != resume_receipt:
            raise RuntimeError("resume receipt does not match a durable hold receipt")
        if find_latest_operation_receipt_key(control, receipt_bodies, "hold") != f"{resume_receipt.run_id}:hold":
            raise RuntimeError("resume receipt does not match the active hold generation")
        resume_key = f"{resume_receipt.run_id}:resume"
        completed_resume = find_completed_operation_receipt(control, receipt_bodies, "resume", resume_key)
        if completed_resume is not None:
            if (
                completed_resume.get("run_id") != resume_receipt.run_id
                or completed_resume.get("hold_key") != f"{resume_receipt.run_id}:hold"
                or completed_resume.get("states") != resume_receipt.previous_states
            ):
                raise RuntimeError("stored resume receipt does not match the hold receipt")
            completed_states = _workflow_states(repo)
            verify_complete_workflow_set(completed_states)
            verify_workflow_states(cast(dict[str, bool], completed_resume["states"]), completed_states)
            print(
                json.dumps(
                    {
                        "idempotent": True,
                        "idempotency_key": resume_key,
                        "run_id": resume_receipt.run_id,
                        "states": completed_resume["states"],
                        "receipt": completed_resume,
                    }
                )
            )
            return 0
        current = _workflow_states(repo)
        verify_complete_workflow_set(current)
        restored = control.resume(current, resume_receipt)
        proposed_resume_receipt: dict[str, object] = {
            "run_id": resume_receipt.run_id,
            "hold_key": f"{resume_receipt.run_id}:hold",
            "states": restored,
        }
        stored_resume_receipt, _ = get_or_store_operation_receipt(
            repo,
            resume_issue_number,
            control,
            "resume",
            resume_key,
            proposed_resume_receipt,
        )
        if (
            not isinstance(stored_resume_receipt, dict)
            or stored_resume_receipt.get("run_id") != resume_receipt.run_id
            or stored_resume_receipt.get("hold_key") != f"{resume_receipt.run_id}:hold"
            or stored_resume_receipt.get("states") != resume_receipt.previous_states
        ):
            raise RuntimeError("stored resume receipt does not match the hold receipt")
        states = cast(dict[str, bool], stored_resume_receipt["states"])
        idempotent = True
        for workflow, enabled in states.items():
            if enabled and not current[workflow]:
                _run_gh_text(["workflow", "enable", workflow, "--repo", repo])
                idempotent = False
        refreshed_resume_states = _workflow_states(repo)
        verify_complete_workflow_set(refreshed_resume_states)
        verify_workflow_states(states, refreshed_resume_states)
        completion_body = f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(
            {
                "idempotency_key": resume_key,
                "operation": "resume",
                "receipt": stored_resume_receipt,
                "completed": True,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        _post_control_issue_comment(repo, resume_issue_number, completion_body)
        completed_bodies = _write_control_issue_state_index(
            repo,
            resume_issue_number,
            trusted_logins(),
            control,
            trusted_comment_bodies(resume_issue_number),
        )
        completed_resume = find_completed_operation_receipt(control, completed_bodies, "resume", resume_key)
        if completed_resume != stored_resume_receipt:
            raise RuntimeError("resume completion receipt read-back mismatch")
        print(
            json.dumps(
                {
                    "idempotent": idempotent,
                    "idempotency_key": resume_key,
                    "run_id": resume_receipt.run_id,
                    "states": states,
                    "receipt": stored_resume_receipt,
                }
            )
        )
        return 0

    if args.operation == "checkpoint":
        if not args.run_id.isdecimal():
            raise ValueError("checkpoint run ID must contain only decimal digits")
        payload = json.loads(args.payload)
        if not isinstance(payload, dict):
            raise ValueError("checkpoint payload must be a JSON object")
        checkpoint = Checkpoint(args.run_id, payload, repo)
        encoded = control.encode_checkpoint(checkpoint)
        serialized_entry = json.dumps(encoded, sort_keys=True, separators=(",", ":"))
        index_placeholder = {
            "version": 2,
            "snapshot_id": "0" * 64,
            "shard_index": (1 << 63) - 1,
            "shard_count": (1 << 63) - 1,
            "entries": [],
        }
        empty_index_size = (
            len(f"{CONTROL_STATE_INDEX_MARKER}\n")
            + len("\n\n")
            + len("🤖 AI PR Loop ·")
            + len(json.dumps(index_placeholder, sort_keys=True, separators=(",", ":")))
        )
        if empty_index_size + len(serialized_entry) > CONTROL_STATE_INDEX_MAX_COMMENT_CHARS:
            raise RuntimeError("a control state index entry exceeds the comment size limit")
        issue_number = _control_issue(repo)
        bodies = trusted_comment_bodies(issue_number)
        fingerprint = json.loads(encoded.split("\n", 1)[1])["evidence_fingerprint"]
        idempotency_key = f"{args.run_id}:checkpoint:{fingerprint}"
        try:
            find_published_checkpoint(control, encoded, bodies, repo)
        except RuntimeError:
            latest_checkpoint = latest_valid_checkpoint(control, bodies, repo)
            if latest_checkpoint is not None:
                if not latest_checkpoint.run_id.isdecimal():
                    raise RuntimeError("cannot safely order checkpoint runs with non-numeric run IDs")
                if int(latest_checkpoint.run_id) >= int(args.run_id):
                    raise RuntimeError(f"refusing to publish stale checkpoint for run {args.run_id}")
            _post_control_issue_comment(repo, issue_number, encoded)
            bodies = trusted_comment_bodies(issue_number)
            find_published_checkpoint(control, encoded, bodies, repo)
            bodies = _write_control_issue_state_index(
                repo,
                issue_number,
                trusted_logins(),
                control,
                bodies,
            )
            find_published_checkpoint(control, encoded, bodies, repo)
        print(
            json.dumps(
                {
                    "run_id": args.run_id,
                    "checkpoint": encoded,
                    "control_issue": issue_number,
                    "idempotency_key": idempotency_key,
                }
            )
        )
        return 0

    raise NotImplementedError(f"operation {args.operation!r} requires a verified provider leaf")


def supervision_control_command() -> None:
    """Console-script entry point."""
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
