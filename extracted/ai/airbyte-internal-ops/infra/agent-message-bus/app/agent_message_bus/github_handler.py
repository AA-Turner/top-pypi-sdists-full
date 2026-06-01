# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""GitHub webhook event handler.

Processes incoming GitHub webhook payloads, matches them against active
subscriptions in Firestore, and notifies subscribed Devin sessions.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
from datetime import datetime, timezone
from typing import Any

from agent_message_bus.devin_client import (
    INJECT_OK,
    INJECT_SESSION_DEAD,
    inject_message,
)
from agent_message_bus.firestore_client import SubscriptionStore
from agent_message_bus.models import Subscription, WatchEvent

logger = logging.getLogger(__name__)


def verify_github_signature(payload_body: bytes, signature_header: str, secret: str) -> bool:
    """Verify the GitHub webhook signature (X-Hub-Signature-256).

    Args:
        payload_body: Raw request body bytes.
        signature_header: Value of X-Hub-Signature-256 header.
        secret: The webhook shared secret.

    Returns:
        True if the signature is valid.
    """
    if not signature_header:
        return False

    expected = (
        "sha256="
        + hmac.new(
            secret.encode("utf-8"),
            payload_body,
            hashlib.sha256,
        ).hexdigest()
    )

    return hmac.compare_digest(expected, signature_header)


def _map_github_event_to_watch_event(
    event_type: str,
    action: str,
    payload: dict[str, Any],
) -> WatchEvent | None:
    """Map a GitHub webhook event+action to our WatchEvent enum.

    Args:
        event_type: The X-GitHub-Event header value.
        action: The 'action' field from the payload.
        payload: The full webhook payload.

    Returns:
        The corresponding WatchEvent, or None if not relevant.
    """
    if event_type == "issue_comment":
        if action in ("created", "edited"):
            return WatchEvent.COMMENT
        return None

    if event_type == "issues":
        action_map: dict[str, WatchEvent] = {
            "closed": WatchEvent.CLOSE,
            "reopened": WatchEvent.REOPEN,
            "labeled": WatchEvent.LABEL,
            "unlabeled": WatchEvent.LABEL,
            "assigned": WatchEvent.ASSIGNED,
            "unassigned": WatchEvent.ASSIGNED,
        }
        return action_map.get(action)

    if event_type == "pull_request":
        if action == "closed":
            # Distinguish merge from close
            pr = payload.get("pull_request", {})
            if pr.get("merged"):
                return WatchEvent.MERGE
            return WatchEvent.CLOSE
        action_map_pr: dict[str, WatchEvent] = {
            "reopened": WatchEvent.REOPEN,
            "synchronize": WatchEvent.SYNCHRONIZE,
            "ready_for_review": WatchEvent.READY_FOR_REVIEW,
            "labeled": WatchEvent.LABEL,
            "unlabeled": WatchEvent.LABEL,
            "assigned": WatchEvent.ASSIGNED,
            "unassigned": WatchEvent.ASSIGNED,
        }
        return action_map_pr.get(action)

    return None


def _format_notification(
    event_type: str,
    action: str,
    payload: dict[str, Any],
    subscription: Subscription,
) -> str:
    """Format a human-readable notification message for the Devin session.

    Args:
        event_type: The X-GitHub-Event header value.
        action: The 'action' field from the payload.
        payload: The full webhook payload.
        subscription: The matching subscription.

    Returns:
        Formatted notification string.
    """
    sender = payload.get("sender", {}).get("login", "someone")
    repo_full = f"{subscription.owner}/{subscription.repo}"
    ref = f"{repo_full}#{subscription.number}"

    if event_type == "issue_comment" and action == "created":
        comment = payload.get("comment", {})
        body = comment.get("body", "")
        # Truncate long comments
        if len(body) > 500:
            body = body[:500] + "..."
        return f"New comment on {ref} by @{sender}:\n\n{body}\n\nView: {subscription.github_url}"

    if event_type == "issues":
        if action == "closed":
            return f"Issue {ref} was closed by @{sender}.\nView: {subscription.github_url}"
        if action == "reopened":
            return f"Issue {ref} was reopened by @{sender}.\nView: {subscription.github_url}"
        if action in ("labeled", "unlabeled"):
            label = payload.get("label", {}).get("name", "unknown")
            verb = "added" if action == "labeled" else "removed"
            return (
                f"Label '{label}' was {verb} on {ref} by @{sender}.\n"
                f"View: {subscription.github_url}"
            )
        if action in ("assigned", "unassigned"):
            assignee = payload.get("assignee", {}).get("login", "unknown")
            verb = "assigned to" if action == "assigned" else "unassigned from"
            return f"@{assignee} was {verb} {ref} by @{sender}.\nView: {subscription.github_url}"

    if event_type == "pull_request":
        pr = payload.get("pull_request", {})
        if action == "closed" and pr.get("merged"):
            return f"PR {ref} was merged by @{sender}.\nView: {subscription.github_url}"
        if action == "closed":
            return f"PR {ref} was closed by @{sender}.\nView: {subscription.github_url}"
        if action == "reopened":
            return f"PR {ref} was reopened by @{sender}.\nView: {subscription.github_url}"
        if action == "synchronize":
            return f"New commits pushed to PR {ref} by @{sender}.\nView: {subscription.github_url}"
        if action == "ready_for_review":
            return (
                f"PR {ref} is now ready for review (marked by @{sender}).\n"
                f"View: {subscription.github_url}"
            )
        if action in ("labeled", "unlabeled"):
            label = payload.get("label", {}).get("name", "unknown")
            verb = "added" if action == "labeled" else "removed"
            return (
                f"Label '{label}' was {verb} on PR {ref} by @{sender}.\n"
                f"View: {subscription.github_url}"
            )
        if action in ("assigned", "unassigned"):
            assignee = payload.get("assignee", {}).get("login", "unknown")
            verb = "assigned to" if action == "assigned" else "unassigned from"
            return f"@{assignee} was {verb} PR {ref} by @{sender}.\nView: {subscription.github_url}"

    return (
        f"Activity on {ref}: {event_type}/{action} by @{sender}.\nView: {subscription.github_url}"
    )


def handle_github_webhook(
    event_type: str,
    payload: dict[str, Any],
    store: SubscriptionStore,
) -> dict[str, Any]:
    """Process a GitHub webhook event.

    Extracts the repo + issue/PR number from the payload, looks up
    active subscriptions in Firestore, and notifies matching sessions.

    Args:
        event_type: The X-GitHub-Event header value.
        payload: The parsed JSON webhook payload.
        store: The Firestore subscription store.

    Returns:
        Summary dict with processing results.
    """
    action = payload.get("action", "")
    sender = payload.get("sender", {})

    # Early discard: bot senders
    if sender.get("type") == "Bot":
        return {"status": "skipped", "reason": "bot_sender"}

    # Extract repo info
    repo_data = payload.get("repository", {})
    owner = repo_data.get("owner", {}).get("login", "")
    repo_name = repo_data.get("name", "")

    if not owner or not repo_name:
        return {"status": "skipped", "reason": "missing_repo_info"}

    # Extract issue/PR number
    number: int | None = None
    if event_type in ("issue_comment", "issues"):
        issue = payload.get("issue", {})
        number = issue.get("number")
    elif event_type == "pull_request":
        pr = payload.get("pull_request", {})
        number = pr.get("number")

    if number is None:
        return {"status": "skipped", "reason": "no_issue_number"}

    # Map to our watch event type
    watch_event = _map_github_event_to_watch_event(event_type, action, payload)
    if watch_event is None:
        return {
            "status": "skipped",
            "reason": "unmapped_event",
            "event": f"{event_type}/{action}",
        }

    # Look up subscriptions
    subscriptions = store.find_by_issue(owner=owner, repo=repo_name, number=number)
    if not subscriptions:
        return {"status": "no_match", "repo": f"{owner}/{repo_name}", "number": number}

    # Notify matching subscriptions
    notified = 0
    cleaned = 0
    for sub in subscriptions:
        # Check if this subscription watches this event type
        if watch_event not in sub.watch_events:
            continue

        # Dedup: skip if this is a comment we already notified about
        if event_type == "issue_comment" and action == "created":
            comment_id = payload.get("comment", {}).get("id")
            if comment_id and sub.last_comment_id and comment_id <= sub.last_comment_id:
                continue

        message = _format_notification(event_type, action, payload, sub)
        result = inject_message(sub.session_url, message)

        if result == INJECT_OK:
            notified += 1
            # Update subscription state
            now = datetime.now(tz=timezone.utc)
            update_data: dict[str, Any] = {"last_notified_at": now}
            if event_type == "issue_comment" and action == "created":
                comment_id = payload.get("comment", {}).get("id")
                if comment_id:
                    update_data["last_comment_id"] = comment_id
            if event_type in ("issues", "pull_request") and action in (
                "closed",
                "reopened",
            ):
                pr = payload.get("pull_request", {})
                if action == "closed" and pr.get("merged"):
                    update_data["last_known_state"] = "merged"
                elif action == "closed":
                    update_data["last_known_state"] = "closed"
                else:
                    update_data["last_known_state"] = "open"
            store._collection.document(sub.id).update(update_data)
        elif result == INJECT_SESSION_DEAD:
            # Session genuinely gone (404) — clean up the subscription
            store.delete_by_id(sub.id)
            cleaned += 1
            logger.info(
                "Cleaned up subscription %s for dead session %s",
                sub.id,
                sub.session_url,
            )
        else:
            # Auth error or transient failure — leave the subscription
            # intact so it can be retried on the next event.
            logger.warning(
                "Could not notify session %s (result=%s), keeping subscription %s",
                sub.session_url,
                result,
                sub.id,
            )

    return {
        "status": "processed",
        "repo": f"{owner}/{repo_name}",
        "number": number,
        "event": f"{event_type}/{action}",
        "subscriptions_matched": len(subscriptions),
        "notified": notified,
        "cleaned": cleaned,
    }
