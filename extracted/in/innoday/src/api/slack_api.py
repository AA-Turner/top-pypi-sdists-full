"""
Slack API integration for InnoDay.

This module provides integration with Slack for:
- Sending messages to channels and users
- Receiving and processing Slack events
- Managing Slack workspace connections
- Thread-based conversations
"""

import logging
import os
from typing import Any, Dict, List, Optional

import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SlackMessage(BaseModel):
    """Model for a Slack message."""

    channel: str
    text: str
    thread_ts: Optional[str] = None
    blocks: Optional[List[Dict[str, Any]]] = None
    attachments: Optional[List[Dict[str, Any]]] = None
    as_user: bool = True


class SlackChannel(BaseModel):
    """Model for a Slack channel."""

    id: str
    name: str
    is_channel: bool = True
    is_private: bool = False
    is_member: bool = False
    num_members: Optional[int] = None


class SlackUser(BaseModel):
    """Model for a Slack user."""

    id: str
    name: str
    real_name: Optional[str] = None
    email: Optional[str] = None
    is_bot: bool = False
    is_admin: bool = False


class SlackAPI:
    """Client for interacting with Slack API."""

    def __init__(self, token: Optional[str] = None, webhook_url: Optional[str] = None):
        """
        Initialize Slack API client.

        Args:
            token: Slack Bot User OAuth Token (xoxb-...)
            webhook_url: Slack Incoming Webhook URL for simple notifications
        """
        self.token = token or os.getenv("SLACK_BOT_TOKEN")
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")

        if not self.token and not self.webhook_url:
            raise ValueError(
                "Either SLACK_BOT_TOKEN or SLACK_WEBHOOK_URL must be provided"
            )

        self.base_url = "https://slack.com/api"
        self.headers = (
            {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }
            if self.token
            else {}
        )

        logger.info("Slack API client initialized")

    async def _make_request(
        self, method: str, endpoint: str, **kwargs
    ) -> Dict[str, Any]:
        """Make an authenticated request to Slack API."""
        if not self.token:
            raise ValueError("Slack Bot Token required for API calls")

        url = f"{self.base_url}/{endpoint}"

        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=self.headers, **kwargs)

            response.raise_for_status()
            data = response.json()

            if not data.get("ok", False):
                error = data.get("error", "Unknown error")
                raise Exception(f"Slack API error: {error}")

            return data

    async def send_webhook_message(self, text: str, **kwargs) -> bool:
        """
        Send a simple message via webhook.

        Args:
            text: Message text
            **kwargs: Additional webhook payload fields

        Returns:
            bool: True if successful
        """
        if not self.webhook_url:
            raise ValueError("Webhook URL not configured")

        payload = {"text": text, **kwargs}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )

            return response.status_code == 200

    async def send_message(
        self,
        channel: str,
        text: str,
        thread_ts: Optional[str] = None,
        blocks: Optional[List[Dict[str, Any]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Send a message to a Slack channel or user.

        Args:
            channel: Channel ID, channel name, or user ID
            text: Message text (fallback for blocks)
            thread_ts: Thread timestamp for replies
            blocks: Rich message blocks
            **kwargs: Additional message parameters

        Returns:
            Dict with message details including timestamp
        """
        payload = {"channel": channel, "text": text, "as_user": True, **kwargs}

        if thread_ts:
            payload["thread_ts"] = thread_ts
        if blocks:
            payload["blocks"] = blocks

        result = await self._make_request("POST", "chat.postMessage", json=payload)
        return result

    async def update_message(
        self,
        channel: str,
        ts: str,
        text: str,
        blocks: Optional[List[Dict[str, Any]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Update an existing message."""
        payload = {"channel": channel, "ts": ts, "text": text, **kwargs}

        if blocks:
            payload["blocks"] = blocks

        result = await self._make_request("POST", "chat.update", json=payload)
        return result

    async def delete_message(self, channel: str, ts: str) -> bool:
        """Delete a message."""
        payload = {"channel": channel, "ts": ts}
        result = await self._make_request("POST", "chat.delete", json=payload)
        return result.get("ok", False)

    async def get_channel_list(self, limit: int = 100) -> List[SlackChannel]:
        """
        Get list of channels in the workspace.

        Args:
            limit: Maximum number of channels to return

        Returns:
            List of SlackChannel objects
        """
        result = await self._make_request(
            "GET",
            "conversations.list",
            params={"limit": limit, "types": "public_channel,private_channel"},
        )

        channels = []
        for channel_data in result.get("channels", []):
            channels.append(
                SlackChannel(
                    id=channel_data["id"],
                    name=channel_data["name"],
                    is_channel=True,
                    is_private=channel_data.get("is_private", False),
                    is_member=channel_data.get("is_member", False),
                    num_members=channel_data.get("num_members"),
                )
            )

        return channels

    async def get_channel_info(self, channel_id: str) -> SlackChannel:
        """Get information about a specific channel."""
        result = await self._make_request(
            "GET", "conversations.info", params={"channel": channel_id}
        )

        channel_data = result["channel"]
        return SlackChannel(
            id=channel_data["id"],
            name=channel_data["name"],
            is_channel=True,
            is_private=channel_data.get("is_private", False),
            is_member=channel_data.get("is_member", False),
        )

    async def get_user_list(self, limit: int = 100) -> List[SlackUser]:
        """Get list of users in the workspace."""
        result = await self._make_request("GET", "users.list", params={"limit": limit})

        users = []
        for user_data in result.get("members", []):
            if user_data.get("deleted", False):
                continue

            users.append(
                SlackUser(
                    id=user_data["id"],
                    name=user_data["name"],
                    real_name=user_data.get("real_name"),
                    email=user_data.get("profile", {}).get("email"),
                    is_bot=user_data.get("is_bot", False),
                    is_admin=user_data.get("is_admin", False),
                )
            )

        return users

    async def get_user_info(self, user_id: str) -> SlackUser:
        """Get information about a specific user."""
        result = await self._make_request("GET", "users.info", params={"user": user_id})

        user_data = result["user"]
        return SlackUser(
            id=user_data["id"],
            name=user_data["name"],
            real_name=user_data.get("real_name"),
            email=user_data.get("profile", {}).get("email"),
            is_bot=user_data.get("is_bot", False),
            is_admin=user_data.get("is_admin", False),
        )

    async def get_channel_history(
        self,
        channel: str,
        limit: int = 100,
        oldest: Optional[str] = None,
        latest: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get message history from a channel.

        Args:
            channel: Channel ID
            limit: Maximum number of messages
            oldest: Oldest timestamp (inclusive)
            latest: Latest timestamp (inclusive)

        Returns:
            List of message dictionaries
        """
        params = {"channel": channel, "limit": limit}
        if oldest:
            params["oldest"] = oldest
        if latest:
            params["latest"] = latest

        result = await self._make_request("GET", "conversations.history", params=params)

        return result.get("messages", [])

    async def get_thread_replies(
        self, channel: str, thread_ts: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get replies in a thread."""
        result = await self._make_request(
            "GET",
            "conversations.replies",
            params={"channel": channel, "ts": thread_ts, "limit": limit},
        )

        return result.get("messages", [])

    async def add_reaction(self, channel: str, timestamp: str, emoji: str) -> bool:
        """Add a reaction to a message."""
        result = await self._make_request(
            "POST",
            "reactions.add",
            json={"channel": channel, "timestamp": timestamp, "name": emoji},
        )
        return result.get("ok", False)

    async def test_auth(self) -> Dict[str, Any]:
        """Test authentication and get workspace info."""
        result = await self._make_request("GET", "auth.test")
        return {
            "team": result.get("team"),
            "team_id": result.get("team_id"),
            "user": result.get("user"),
            "user_id": result.get("user_id"),
            "bot_id": result.get("bot_id"),
        }

    def create_ticket_blocks(
        self,
        ticket_id: str,
        title: str,
        description: str,
        status: str,
        assignee: Optional[str] = None,
        url: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Create rich message blocks for a ticket notification.

        Args:
            ticket_id: Ticket identifier
            title: Ticket title
            description: Ticket description
            status: Current status
            assignee: Assigned user
            url: Link to ticket

        Returns:
            List of Slack block elements
        """
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"🎫 Ticket {ticket_id}"},
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Title:*\n{title}"},
                    {"type": "mrkdwn", "text": f"*Status:*\n{status}"},
                ],
            },
        ]

        if description:
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            f"*Description:*\n{description[:500]}..."
                            if len(description) > 500
                            else f"*Description:*\n{description}"
                        ),
                    },
                }
            )

        if assignee:
            blocks.append(
                {
                    "type": "context",
                    "elements": [
                        {"type": "mrkdwn", "text": f"*Assigned to:* {assignee}"}
                    ],
                }
            )

        if url:
            blocks.append(
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "View Ticket"},
                            "url": url,
                            "action_id": "view_ticket",
                        }
                    ],
                }
            )

        return blocks
