"""MessageBroker — file-based inter-agent messaging with in-process notifications.

Messages are stored as individual JSON files in the mailbox directory:
  ~/.emdash/teams/{team-name}/mailbox/{to-agent}/{timestamp}-{id}.json

Delivery model:
  - WRITE: Sender writes a message file to the recipient's directory.
  - NOTIFY: For in-process teammates, an asyncio.Event is set to wake them.
  - POLL: Teammates poll their directory between LLM iterations.
  - DELIVER: On read, messages are moved to .delivered/ subdirectory.

Why file-based?
  - Works across processes (future: out-of-process teammates)
  - Survives crashes (messages persist on disk)
  - No external dependencies (no Redis, no message queue)
  - Atomic writes via temp-file + rename pattern

For v1 (in-process only), we also maintain an asyncio.Queue per agent
for instant notification without polling latency.
"""

import asyncio
import json
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ...utils.logger import log
from .models import TeamMessage, MessageType


class MessageBroker:
    """File-based message broker with optional in-process fast path.

    Usage:
        broker = MessageBroker(Path("~/.emdash/teams/my-team/mailbox"))

        # Send a message
        msg_id = broker.send(
            from_agent="lead",
            to_agent="security-reviewer",
            content="Also check for CSRF vulnerabilities.",
            message_type=MessageType.MESSAGE,
        )

        # Receive pending messages (called by teammate between iterations)
        messages = broker.receive("security-reviewer")
    """

    def __init__(self, mailbox_dir: Path):
        self._mailbox_dir = mailbox_dir
        self._mailbox_dir.mkdir(parents=True, exist_ok=True)

        # In-process notification queues (agent_name -> asyncio.Queue)
        self._queues: dict[str, asyncio.Queue] = {}

        # Subscribers waiting for messages (agent_name -> list of Events)
        self._subscribers: dict[str, list[asyncio.Event]] = {}

    # ─────────────────────────────────────────────────────────
    # Send
    # ─────────────────────────────────────────────────────────

    def send(
        self,
        from_agent: str,
        to_agent: str,
        content: str,
        message_type: MessageType,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Send a message to an agent's mailbox.

        Args:
            from_agent: Sender name.
            to_agent: Recipient name.
            content: Message body (markdown).
            message_type: Type of message.
            metadata: Optional extra data.

        Returns:
            Message ID.
        """
        msg_id = uuid.uuid4().hex[:12]
        now = datetime.now()
        timestamp = now.isoformat()
        file_ts = now.strftime("%Y%m%d-%H%M%S")

        message = TeamMessage(
            id=msg_id,
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            content=content,
            metadata=metadata or {},
            timestamp=timestamp,
        )

        # Write to recipient's mailbox directory
        recipient_dir = self._mailbox_dir / to_agent
        recipient_dir.mkdir(parents=True, exist_ok=True)

        msg_file = recipient_dir / f"{file_ts}-{msg_id}.json"

        # Atomic write: write to temp file then rename
        tmp_file = msg_file.with_suffix(".tmp")
        tmp_file.write_text(json.dumps(message.to_dict(), indent=2))
        tmp_file.rename(msg_file)

        log.debug(f"Message {msg_id}: {from_agent} -> {to_agent} ({message_type.value})")

        # Notify in-process subscribers
        self._notify(to_agent)

        return msg_id

    # ─────────────────────────────────────────────────────────
    # Receive
    # ─────────────────────────────────────────────────────────

    def receive(
        self,
        agent_name: str,
        mark_delivered: bool = True,
    ) -> list[TeamMessage]:
        """Receive all pending messages for an agent.

        Reads all .json files from the agent's mailbox directory,
        optionally moving them to .delivered/ subdirectory.

        Args:
            agent_name: The receiving agent's name.
            mark_delivered: If True, move messages to .delivered/.

        Returns:
            List of messages sorted by timestamp (oldest first).
        """
        agent_dir = self._mailbox_dir / agent_name
        if not agent_dir.exists():
            return []

        messages = []
        for msg_file in sorted(agent_dir.glob("*.json")):
            try:
                data = json.loads(msg_file.read_text())
                message = TeamMessage.from_dict(data)
                messages.append(message)

                if mark_delivered:
                    # Move to .delivered/ subdirectory
                    delivered_dir = agent_dir / ".delivered"
                    delivered_dir.mkdir(exist_ok=True)
                    message.delivered = True
                    message.delivered_at = datetime.now().isoformat()

                    dest = delivered_dir / msg_file.name
                    dest.write_text(json.dumps(message.to_dict(), indent=2))
                    msg_file.unlink()

            except Exception as e:
                log.warning(f"Failed to read message {msg_file}: {e}")

        return messages

    def peek(self, agent_name: str) -> int:
        """Check how many unread messages an agent has (without reading them)."""
        agent_dir = self._mailbox_dir / agent_name
        if not agent_dir.exists():
            return 0
        return len(list(agent_dir.glob("*.json")))

    # ─────────────────────────────────────────────────────────
    # In-process fast path
    # ─────────────────────────────────────────────────────────

    def subscribe(self, agent_name: str) -> asyncio.Event:
        """Subscribe to message notifications for an agent.

        Returns an asyncio.Event that is set whenever a new
        message arrives. The agent should wait on this event
        between iterations and clear it after processing.
        """
        event = asyncio.Event()
        if agent_name not in self._subscribers:
            self._subscribers[agent_name] = []
        self._subscribers[agent_name].append(event)
        return event

    def unsubscribe(self, agent_name: str, event: asyncio.Event) -> None:
        """Remove a subscription."""
        if agent_name in self._subscribers:
            self._subscribers[agent_name] = [
                e for e in self._subscribers[agent_name] if e is not event
            ]

    def _notify(self, agent_name: str) -> None:
        """Notify subscribers that a new message is available."""
        for event in self._subscribers.get(agent_name, []):
            event.set()

    # ─────────────────────────────────────────────────────────
    # History
    # ─────────────────────────────────────────────────────────

    def get_history(
        self,
        agent_name: str,
        limit: int = 50,
    ) -> list[TeamMessage]:
        """Get delivered message history for an agent.

        Reads from the .delivered/ subdirectory.
        """
        delivered_dir = self._mailbox_dir / agent_name / ".delivered"
        if not delivered_dir.exists():
            return []

        messages = []
        files = sorted(delivered_dir.glob("*.json"), reverse=True)[:limit]

        for msg_file in files:
            try:
                data = json.loads(msg_file.read_text())
                messages.append(TeamMessage.from_dict(data))
            except Exception:
                pass

        return list(reversed(messages))  # Oldest first

    def get_all_history(self, limit: int = 100) -> list[TeamMessage]:
        """Get message history across all agents (for the lead's overview)."""
        all_messages = []

        for agent_dir in self._mailbox_dir.iterdir():
            if agent_dir.is_dir() and not agent_dir.name.startswith("."):
                all_messages.extend(self.get_history(agent_dir.name, limit=limit))

        # Sort by timestamp and limit
        all_messages.sort(key=lambda m: m.timestamp)
        return all_messages[-limit:]

    # ─────────────────────────────────────────────────────────
    # Cleanup
    # ─────────────────────────────────────────────────────────

    def cleanup(self) -> None:
        """Remove all mailbox data."""
        if self._mailbox_dir.exists():
            shutil.rmtree(self._mailbox_dir)
            log.info(f"Cleaned up mailbox at {self._mailbox_dir}")
