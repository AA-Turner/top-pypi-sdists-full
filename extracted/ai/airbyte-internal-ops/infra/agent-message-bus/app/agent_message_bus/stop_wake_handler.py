# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Process Devin Stop events and wake eligible Hydra handoffs."""

from __future__ import annotations

import logging
import os
import re
from typing import Any

import requests

from agent_message_bus.devin_client import get_session
from agent_message_bus.github_app import GITHUB_API_BASE, GITHUB_REPOSITORY, get_installation_token
from agent_message_bus.models import DevinStopEvent

logger = logging.getLogger(__name__)

# "Github CI Service User" (API key is the DEVIN_AI_API_KEY GitHub org secret).
HYDRA_SERVICE_USER_ID = "service-user-19e8281ae7fc4a6da98bb6e5f045c87e"
HYDRA_LABEL = "hyd-chain-v2"
_PR_TAG = re.compile(r"^airbyte-pr-(\d+)$")
_PR_URL = re.compile(r"^https://github\.com/airbytehq/airbyte/pull/(\d+)$")
_ONCALL_ISSUE_TAG = re.compile(r"^oncall-issue-\d+$")
_API_HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def _finish(
    outcome: str,
    session_id: str,
    prompt_id: str,
    pr: int | None = None,
    **context: Any,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "outcome": outcome,
        "session_id": session_id,
        "prompt_id": prompt_id,
    }
    if pr is not None:
        result["pr"] = pr
    result.update(context)
    logger.info(
        "Stop hook event outcome=%s session_id=%s prompt_id=%s pr=%s context=%s",
        outcome,
        session_id,
        prompt_id,
        pr if pr is not None else "(unknown)",
        context,
    )
    return result


def _github_request(method: str, path: str, **kwargs: Any) -> requests.Response:
    token = get_installation_token()
    return requests.request(
        method,
        f"{GITHUB_API_BASE}{path}",
        headers={**_API_HEADERS, "Authorization": f"Bearer {token}"},
        timeout=10,
        **kwargs,
    )


def _response_error(response: requests.Response) -> dict[str, Any]:
    return {
        "status_code": response.status_code,
        "body": response.text[:200],
    }


def _pull_request_number(
    tags: list[str],
    pull_requests: list[dict[str, Any]],
) -> tuple[int | None, str | None, bool]:
    """Resolve a unique Airbyte PR number, preferring its explicit session tag."""
    tag_numbers = {int(match.group(1)) for tag in tags if (match := _PR_TAG.fullmatch(tag))}
    has_pr_tag = bool(tag_numbers)
    if tag_numbers:
        numbers = tag_numbers
    else:
        numbers = {
            int(match.group(1))
            for pull_request in pull_requests
            if isinstance(pull_request.get("pr_url"), str)
            and (match := _PR_URL.fullmatch(pull_request["pr_url"]))
        }
    if not numbers:
        return None, "no_pr", has_pr_tag
    if len(numbers) > 1:
        return None, "ambiguous_pr", has_pr_tag
    return numbers.pop(), None, has_pr_tag


def _source_stage(tags: list[str], has_pr_tag: bool) -> str:
    if "pr-review" in tags:
        return "ai-review"
    if "conflict-resolution" in tags:
        return "ai-resolve-conflicts"
    if any(_ONCALL_ISSUE_TAG.fullmatch(tag) for tag in tags):
        return "ai-fix"
    if has_pr_tag:
        return "ai-prove-fix"
    return "unknown"


def handle_stop_event(event: DevinStopEvent, store: Any) -> dict[str, Any]:
    """Handle one Stop hook event without raising into the background task."""
    session_id = event.session_id.removeprefix("devin-")
    prompt_id = event.prompt_id
    pr: int | None = None

    try:
        if not store.claim_event(session_id, prompt_id):
            return _finish("duplicate", session_id, prompt_id)

        session = get_session(session_id)
        if session is None:
            return _finish("not_hydra", session_id, prompt_id, reason="session_not_found")

        tags = session.get("tags") or []
        expected_service_user_id = os.environ.get("HYDRA_SERVICE_USER_ID", HYDRA_SERVICE_USER_ID)
        if session.get("service_user_id") != expected_service_user_id or "ai-oncall" not in tags:
            return _finish("not_hydra", session_id, prompt_id)

        pr, mapping_outcome, has_pr_tag = _pull_request_number(
            tags,
            session.get("pull_requests") or [],
        )
        if mapping_outcome:
            return _finish(mapping_outcome, session_id, prompt_id)

        response = _github_request("GET", f"/repos/{GITHUB_REPOSITORY}/pulls/{pr}")
        if response.status_code != 200:
            return _finish("error", session_id, prompt_id, pr, **_response_error(response))
        pull_request = response.json()
        if pull_request.get("state") != "open":
            return _finish("closed", session_id, prompt_id, pr)
        labels = {label.get("name") for label in pull_request.get("labels", [])}
        if HYDRA_LABEL not in labels:
            return _finish("no_label", session_id, prompt_id, pr)

        head_sha = pull_request["head"]["sha"]
        source_stage = _source_stage(tags, has_pr_tag)
        dispatch_request = {
            "event_type": "handoff",
            "client_payload": {
                "pr": pr,
                "head_sha": head_sha,
                "source_stage": source_stage,
            },
        }
        dispatch_response = _github_request(
            "POST",
            f"/repos/{GITHUB_REPOSITORY}/dispatches",
            json=dispatch_request,
        )
        if dispatch_response.status_code != 204:
            return _finish(
                "error",
                session_id,
                prompt_id,
                pr,
                **_response_error(dispatch_response),
            )
        return _finish(
            "dispatched",
            session_id,
            prompt_id,
            pr,
            dispatch_request=dispatch_request,
        )
    except Exception:
        logger.exception(
            "Stop hook event processing failed session_id=%s prompt_id=%s pr=%s",
            session_id,
            prompt_id,
            pr if pr is not None else "(unknown)",
        )
        return _finish("error", session_id, prompt_id, pr)
