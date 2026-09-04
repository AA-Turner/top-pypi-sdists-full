"""Canonical Cloud Agent in-flight guard for SpecKit workflows."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import uuid
from collections.abc import Callable
from dataclasses import asdict, dataclass
from typing import Any, Never, cast

from agentic_devtools.cli.ci.agent_assignment import (
    _gh_api_call,
    _resolve_assignment_token,
    _validate_repo_format,
)
from agentic_devtools.cli.ci.retry import RetryableError, retry_with_backoff
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

_CLOUD_AGENT_LOGINS = {"copilot-swe-agent", "copilot-swe-agent[bot]"}
_MARKER_PATTERN = re.compile(
    r"<!--\s*speckit:agent-assigned schema_version=1 engine=cloud-agent "
    r"issue=(\d+) phase=([123]) hierarchy=([^\s]+) correlation_id=([^\s]+)\s*-->"
)
_VALID_PHASES = {1, 2, 3}
_VALID_HIERARCHY_LEVELS = {"epic", "feature", "task", "unknown"}
_ApiCall = Callable[..., str]


def _normalize_hierarchy_level(hierarchy_level: str) -> str:
    normalized = hierarchy_level.strip().lower()
    if normalized not in _VALID_HIERARCHY_LEVELS:
        raise ValueError("hierarchy_level must be epic, feature, task, or unknown")
    return normalized


@retry_with_backoff()
def _call_api(api_call: _ApiCall, endpoint: str, *, token: str) -> str:
    return api_call(endpoint, method="GET", paginate=True, token=token)


@dataclass(frozen=True)
class CloudAgentGuardResult:
    """Secret-free result returned by the Cloud Agent in-flight guard."""

    in_flight: bool
    reason: str
    issue_number: int
    phase: int | None = None
    matched_pr_number: int | None = None
    matched_label: str | None = None


def derive_speckit_base_branch(phase: int, hierarchy_level: str, issue_number: int) -> str:
    """Return the expected base branch for a SpecKit Cloud Agent phase."""
    if phase not in _VALID_PHASES:
        raise ValueError("phase must be one of 1, 2, or 3")
    normalized_hierarchy_level = _normalize_hierarchy_level(hierarchy_level)
    if issue_number <= 0:
        raise ValueError("issue_number must be positive")
    if phase == 2:
        return f"speckit/{issue_number}/phase-1-specify"
    if phase == 3 and normalized_hierarchy_level != "task":
        return f"speckit/{issue_number}/phase-2-clarify"
    return "main"


def parse_cloud_agent_marker(body: object) -> dict[str, str | int] | None:
    """Parse the canonical Cloud Agent correlation marker from a PR body."""
    if not isinstance(body, str):
        return None
    match = _MARKER_PATTERN.search(body)
    if match is None:
        return None
    try:
        correlation_id = str(uuid.UUID(match.group(4)))
    except ValueError:
        return None
    try:
        hierarchy_level = _normalize_hierarchy_level(match.group(3))
    except ValueError:
        return None
    return {
        "issue": int(match.group(1)),
        "phase": int(match.group(2)),
        "hierarchy": hierarchy_level,
        "correlation_id": correlation_id,
    }


def _parse_paginated_documents(payload_text: str) -> list[Any]:
    decoder = json.JSONDecoder()
    payload = payload_text.strip()
    if not payload:
        raise RuntimeError("empty response from paginated API call")
    documents: list[Any] = []
    index = 0
    while index < len(payload):
        while index < len(payload) and payload[index].isspace():
            index += 1
        document, index = decoder.raw_decode(payload, index)
        if not isinstance(document, list):
            raise RuntimeError("non-array response from paginated API call")
        documents.append(document)
    flattened: list[Any] = []
    for document in documents:
        flattened.extend(document)
    return flattened


def _cloud_agent_pr_matches(
    pr: object,
    *,
    issue_number: int,
    phase: int,
    hierarchy_level: str | None = None,
) -> bool:
    if not isinstance(pr, dict):
        return False
    user = pr.get("user")
    login = user.get("login") if isinstance(user, dict) else None
    if not isinstance(login, str) or login.lower() not in _CLOUD_AGENT_LOGINS:
        return False
    marker = parse_cloud_agent_marker(pr.get("body"))
    if marker is None:
        return False
    marker_issue = cast(int, marker["issue"])
    marker_phase = cast(int, marker["phase"])
    marker_hierarchy = cast(str, marker["hierarchy"])
    if marker_issue != issue_number or marker_phase != phase:
        return False
    if hierarchy_level is not None and marker_phase == 3 and marker_hierarchy != hierarchy_level:
        return False
    base = pr.get("base")
    base_ref = base.get("ref") if isinstance(base, dict) else None
    expected_base = derive_speckit_base_branch(marker_phase, hierarchy_level or marker_hierarchy, marker_issue)
    return base_ref == expected_base


def check_cloud_agent_in_flight(
    repo: str,
    issue_number: int,
    phase: int = 0,
    hierarchy_level: str = "feature",
    token: str = "",
    *,
    api_call: _ApiCall | None = None,
) -> CloudAgentGuardResult:
    """Check issue labels and open PRs for an active Cloud Agent assignment."""
    api_call = api_call or _gh_api_call
    normalized_repo = _validate_repo_format(repo)
    if normalized_repo is None:
        raise ValueError("repo must be in owner/repo format")
    if issue_number <= 0:
        raise ValueError("issue_number must be positive")
    if phase not in {0, *_VALID_PHASES}:
        raise ValueError("phase must be 0, 1, 2, or 3")
    normalized_hierarchy_level = _normalize_hierarchy_level(hierarchy_level)
    resolved_token = (
        token.strip()
        or _resolve_assignment_token(("SPECKIT_PR_TOKEN", "COPILOT_GITHUB_TOKEN", "GH_TOKEN", "GITHUB_TOKEN"))[1]
    )
    labels = _parse_paginated_documents(
        _call_api(
            api_call,
            f"/repos/{normalized_repo}/issues/{issue_number}/labels",
            token=resolved_token,
        )
    )
    target_phases = _VALID_PHASES if phase == 0 else {phase}
    for label in labels:
        if not isinstance(label, dict):
            continue
        label_name = label.get("name")
        if not isinstance(label_name, str):
            continue
        if label_name in {f"speckit:agent-assigned-phase-{candidate}" for candidate in target_phases}:
            return CloudAgentGuardResult(
                True,
                "label",
                issue_number,
                phase or None,
                matched_label=label_name,
            )
    pulls = _parse_paginated_documents(
        _call_api(
            api_call,
            f"/repos/{normalized_repo}/pulls?state=open&per_page=100",
            token=resolved_token,
        )
    )
    for pr in pulls:
        for candidate_phase in target_phases:
            if _cloud_agent_pr_matches(
                pr,
                issue_number=issue_number,
                phase=candidate_phase,
                hierarchy_level=normalized_hierarchy_level if phase != 0 else None,
            ):
                pr_number = pr.get("number") if isinstance(pr, dict) else None
                return CloudAgentGuardResult(
                    True,
                    "pull-request",
                    issue_number,
                    phase or None,
                    matched_pr_number=pr_number if isinstance(pr_number, int) else None,
                )
    return CloudAgentGuardResult(False, "none", issue_number, phase or None)


def _error_result(issue_number: int = 0, reason: str = "invalid-arguments") -> dict[str, object]:
    return {
        "in_flight": False,
        "reason": reason,
        "issue_number": issue_number,
        "phase": None,
        "matched_pr_number": None,
        "matched_label": None,
    }


class _GuardArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> Never:
        print(json.dumps(_error_result()))
        raise SystemExit(1)


def cloud_agent_guard_command() -> None:
    """Run the Cloud Agent in-flight guard and print secret-free JSON."""
    parser = _GuardArgumentParser(description="Check for an in-flight SpecKit Cloud Agent assignment")
    parser.add_argument("--issue-number")
    parser.add_argument("--phase", default="0")
    parser.add_argument("--hierarchy-level", default="feature")
    parser.add_argument("--repo", default=None)
    args = parser.parse_args()
    try:
        if args.issue_number is None:
            raise ValueError("issue number is required")
        issue_number = int(args.issue_number)
        phase = int(args.phase)
        repo = (args.repo or os.environ.get("GITHUB_REPOSITORY", "")).strip()
        result = check_cloud_agent_in_flight(
            repo,
            issue_number,
            phase=phase,
            hierarchy_level=args.hierarchy_level,
        )
    except json.JSONDecodeError:
        print(json.dumps(_error_result(issue_number, "error")))
        sys.exit(1)
    except (TypeError, ValueError):
        print(
            json.dumps(
                _error_result(int(args.issue_number))
                if args.issue_number and args.issue_number.isdigit()
                else _error_result()
            )
        )
        sys.exit(1)
    except (RetryableError, ProviderRateLimitError, RuntimeError):
        print(json.dumps(_error_result(issue_number, "error")))
        sys.exit(1)
    print(json.dumps(asdict(result)))
    sys.exit(0)


__all__ = [
    "CloudAgentGuardResult",
    "check_cloud_agent_in_flight",
    "cloud_agent_guard_command",
    "derive_speckit_base_branch",
    "parse_cloud_agent_marker",
]
