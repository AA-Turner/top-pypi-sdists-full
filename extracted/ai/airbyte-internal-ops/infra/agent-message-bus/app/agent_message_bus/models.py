# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Pydantic models for GitHub subscription service."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class SubscriptionType(str, Enum):
    """Type of GitHub resource being watched."""

    ISSUE = "issue"
    PULL_REQUEST = "pull_request"


class WatchEvent(str, Enum):
    """Events that can trigger notifications."""

    COMMENT = "comment"
    CLOSE = "close"
    MERGE = "merge"
    REOPEN = "reopen"
    LABEL = "label"
    SYNCHRONIZE = "synchronize"
    READY_FOR_REVIEW = "ready_for_review"
    ASSIGNED = "assigned"

    @classmethod
    def all_events(cls) -> list[WatchEvent]:
        """Return all available watch events."""
        return list(cls)


DEFAULT_TTL_HOURS = 240  # 10 days


class Subscription(BaseModel):
    """A subscription record stored in Firestore."""

    id: str = Field(description="Firestore document ID")
    session_url: str = Field(description="Devin session URL for notifications")
    session_id: str = Field(description="Devin session ID extracted from URL")
    owner: str = Field(description="GitHub repo owner")
    repo: str = Field(description="GitHub repo name")
    number: int = Field(description="Issue or PR number")
    type: SubscriptionType = Field(description="Issue or pull request")
    github_url: str = Field(description="Full GitHub URL of the issue/PR")
    watch_events: list[WatchEvent] = Field(
        default_factory=WatchEvent.all_events,
        description="Events to notify on",
    )
    last_notified_at: datetime | None = Field(
        default=None,
        description="Timestamp of last notification sent",
    )
    last_comment_id: int | None = Field(
        default=None,
        description="ID of the last comment we notified about",
    )
    last_known_state: str = Field(
        default="open",
        description="Last known state of the issue/PR",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
        description="When the subscription was created",
    )
    expires_at: datetime = Field(description="TTL expiry timestamp")
    slack_users_cc: str | None = Field(
        default=None,
        description="Comma-delimited Slack user tags to CC",
    )
    created_by: str | None = Field(
        default=None,
        description="Who created the subscription",
    )


class CreateSubscriptionRequest(BaseModel):
    """Request body for creating a subscription."""

    github_url: str = Field(description="GitHub issue or PR URL")
    session_url: str = Field(description="Devin session URL for notifications")
    watch_events: list[WatchEvent] | None = Field(
        default=None,
        description="Events to watch. Defaults to all events.",
    )
    ttl_hours: int = Field(
        default=DEFAULT_TTL_HOURS,
        description="Hours until subscription expires (default: 240 = 10 days)",
    )
    slack_users_cc: str | None = Field(
        default=None,
        description="Comma-delimited Slack user tags to CC",
    )
    created_by: str | None = Field(
        default=None,
        description="Who is creating the subscription",
    )


class SubscriptionResponse(BaseModel):
    """Response for subscription operations."""

    id: str = Field(description="Subscription ID")
    github_url: str = Field(description="GitHub issue or PR URL")
    session_url: str = Field(description="Devin session URL")
    owner: str = Field(description="GitHub repo owner")
    repo: str = Field(description="GitHub repo name")
    number: int = Field(description="Issue or PR number")
    type: SubscriptionType = Field(description="Issue or pull request")
    watch_events: list[WatchEvent] = Field(description="Events being watched")
    expires_at: datetime = Field(description="When the subscription expires")
    created_at: datetime = Field(description="When the subscription was created")


class DeleteSubscriptionResponse(BaseModel):
    """Response for delete operations."""

    deleted_count: int = Field(description="Number of subscriptions deleted")
    message: str = Field(description="Human-readable status message")
