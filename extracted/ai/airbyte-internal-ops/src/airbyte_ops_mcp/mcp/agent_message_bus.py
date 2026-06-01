# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for managing GitHub issue/PR subscriptions.

This module exposes subscription management as MCP tools for AI agents.
It is a thin wrapper that calls the Cloud Run subscription API via HTTP.

## MCP reference

.. include:: ../../../docs/mcp-generated/agent_message_bus.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

import logging
import os
from typing import Annotated

import requests
from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

SUBSCRIPTION_API_URL_ENV = "SUBSCRIPTION_API_URL"
SUBSCRIPTION_API_TOKEN_ENV = "SUBSCRIPTION_API_BEARER_TOKEN"


def _get_api_url() -> str:
    """Get the subscription API base URL."""
    url = os.environ.get(SUBSCRIPTION_API_URL_ENV)
    if not url:
        raise ValueError(
            f"{SUBSCRIPTION_API_URL_ENV} environment variable is not set. "
            "Cannot reach the GitHub subscriptions backend."
        )
    return url.rstrip("/")


def _get_api_token() -> str:
    """Get the subscription API bearer token."""
    token = os.environ.get(SUBSCRIPTION_API_TOKEN_ENV)
    if not token:
        raise ValueError(
            f"{SUBSCRIPTION_API_TOKEN_ENV} environment variable is not set. "
            "Cannot authenticate to the GitHub subscriptions backend."
        )
    return token


def _api_headers() -> dict[str, str]:
    """Build headers for API requests."""
    return {
        "Authorization": f"Bearer {_get_api_token()}",
        "Content-Type": "application/json",
    }


class SubscribeResponse(BaseModel):
    """Response from the subscribe_to_github_issue tool."""

    success: bool = Field(
        description="Whether the subscription was created successfully"
    )
    message: str = Field(description="Human-readable status message")
    subscription_id: str | None = Field(
        default=None,
        description="ID of the created or updated subscription",
    )
    github_url: str | None = Field(
        default=None,
        description="GitHub URL being watched",
    )
    expires_at: str | None = Field(
        default=None,
        description="When the subscription expires (ISO 8601)",
    )


class UnsubscribeResponse(BaseModel):
    """Response from the unsubscribe_from_github_issue tool."""

    success: bool = Field(description="Whether the unsubscribe was successful")
    message: str = Field(description="Human-readable status message")
    deleted_count: int = Field(
        default=0,
        description="Number of subscriptions removed",
    )


class ListSubscriptionsResponse(BaseModel):
    """Response from the list_github_subscriptions tool."""

    success: bool = Field(description="Whether the listing was successful")
    message: str = Field(description="Human-readable status message")
    subscriptions: list[dict[str, str]] = Field(
        default_factory=list,
        description="List of active subscriptions with id, github_url, expires_at",
    )


@mcp_tool(
    read_only=False,
    idempotent=True,
    open_world=True,
)
def subscribe_to_github_issue(
    github_url: Annotated[
        str,
        "The GitHub issue or PR URL to subscribe to. "
        "Examples: https://github.com/airbytehq/airbyte/issues/123 "
        "or https://github.com/airbytehq/airbyte/pull/456",
    ],
    agent_session_url: Annotated[
        str,
        "Your Devin session URL so notifications can be delivered back to "
        "your session. Use the session URL from your system prompt.",
    ],
    watch_events: Annotated[
        list[str] | None,
        "Optional list of event types to watch. Valid values: "
        "'comment', 'close', 'merge', 'reopen', 'label', 'synchronize', "
        "'ready_for_review', 'assigned'. Defaults to all events if not specified.",
    ] = None,
    ttl_hours: Annotated[
        int,
        "Number of hours until the subscription expires. Default is 240 (10 days).",
    ] = 240,
    slack_users_cc: Annotated[
        str | None,
        "Optional comma-delimited list of Slack user tags to CC on "
        "notifications. Example: '<@U12345>, <@U67890>'.",
    ] = None,
) -> SubscribeResponse:
    """Subscribe to notifications on a GitHub issue or pull request.

    Creates a subscription that will deliver real-time notifications back
    to your Devin session when activity occurs on the specified GitHub
    issue or PR. Notifications are triggered by GitHub webhooks and
    delivered within seconds.

    If you are already subscribed to the same issue/PR, the subscription
    is updated (TTL extended, watch events merged).

    Use this tool when you need to monitor a GitHub issue or PR for
    changes, new comments, merges, closures, or other activity.
    """
    try:
        api_url = _get_api_url()
        body: dict[str, str | list[str] | int | None] = {
            "github_url": github_url,
            "session_url": agent_session_url,
            "ttl_hours": ttl_hours,
        }
        if watch_events:
            body["watch_events"] = watch_events
        if slack_users_cc:
            body["slack_users_cc"] = slack_users_cc

        response = requests.post(
            f"{api_url}/subscriptions",
            json=body,
            headers=_api_headers(),
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        return SubscribeResponse(
            success=True,
            message=(
                f"Subscribed to {github_url}. "
                f"You will receive notifications in this session until "
                f"{data.get('expires_at', 'expiry unknown')}."
            ),
            subscription_id=data.get("id"),
            github_url=github_url,
            expires_at=data.get("expires_at"),
        )

    except ValueError as e:
        return SubscribeResponse(
            success=False,
            message=f"Configuration error: {e}",
        )
    except requests.RequestException as e:
        logger.exception("Failed to create subscription")
        return SubscribeResponse(
            success=False,
            message=f"Failed to create subscription: {e}",
        )


@mcp_tool(
    read_only=False,
    idempotent=True,
    open_world=True,
)
def unsubscribe_from_github_issue(
    agent_session_url: Annotated[
        str,
        "Your Devin session URL. Use the session URL from your system prompt.",
    ],
    github_url: Annotated[
        str | None,
        "The GitHub issue or PR URL to unsubscribe from. "
        "If not provided, all subscriptions for this session are removed.",
    ] = None,
    subscription_id: Annotated[
        str | None,
        "Optional specific subscription ID to remove. "
        "Use this if you know the exact subscription to cancel.",
    ] = None,
) -> UnsubscribeResponse:
    """Unsubscribe from notifications on a GitHub issue or pull request.

    Removes an active subscription so you will no longer receive
    notifications for the specified issue/PR.

    You can unsubscribe by:
    - Providing a specific subscription_id
    - Providing a github_url + session_url to unsubscribe from that specific issue/PR
    - Providing only session_url to unsubscribe from all issues/PRs
    """
    try:
        api_url = _get_api_url()

        if subscription_id:
            # Delete by ID
            response = requests.delete(
                f"{api_url}/subscriptions/{subscription_id}",
                headers=_api_headers(),
                timeout=10,
            )
        else:
            # Delete by match
            params: dict[str, str] = {"session_url": agent_session_url}
            if github_url:
                params["github_url"] = github_url
            response = requests.delete(
                f"{api_url}/subscriptions",
                params=params,
                headers=_api_headers(),
                timeout=10,
            )

        response.raise_for_status()
        data = response.json()
        count = data.get("deleted_count", 0)

        return UnsubscribeResponse(
            success=True,
            message=f"Removed {count} subscription(s).",
            deleted_count=count,
        )

    except ValueError as e:
        return UnsubscribeResponse(
            success=False,
            message=f"Configuration error: {e}",
        )
    except requests.RequestException as e:
        logger.exception("Failed to unsubscribe")
        return UnsubscribeResponse(
            success=False,
            message=f"Failed to unsubscribe: {e}",
        )


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def list_github_subscriptions(
    agent_session_url: Annotated[
        str,
        "Your Devin session URL. Use the session URL from your system prompt.",
    ],
) -> ListSubscriptionsResponse:
    """List all active GitHub issue/PR subscriptions for this session.

    Returns the list of GitHub issues and PRs that this session is
    currently subscribed to, along with their expiry times.
    """
    try:
        api_url = _get_api_url()

        response = requests.get(
            f"{api_url}/subscriptions",
            params={"session_url": agent_session_url},
            headers=_api_headers(),
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        subs = [
            {
                "id": s["id"],
                "github_url": s["github_url"],
                "watch_events": ", ".join(s.get("watch_events", [])),
                "expires_at": s.get("expires_at", "unknown"),
            }
            for s in data
        ]

        if not subs:
            return ListSubscriptionsResponse(
                success=True,
                message="No active subscriptions for this session.",
                subscriptions=[],
            )

        return ListSubscriptionsResponse(
            success=True,
            message=f"Found {len(subs)} active subscription(s).",
            subscriptions=subs,
        )

    except ValueError as e:
        return ListSubscriptionsResponse(
            success=False,
            message=f"Configuration error: {e}",
        )
    except requests.RequestException as e:
        logger.exception("Failed to list subscriptions")
        return ListSubscriptionsResponse(
            success=False,
            message=f"Failed to list subscriptions: {e}",
        )


def register_message_bus_tools(app: FastMCP) -> None:
    """Register message bus tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
