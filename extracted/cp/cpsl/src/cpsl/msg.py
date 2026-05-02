from __future__ import annotations

import time as _time
from dataclasses import dataclass, field
from typing import Literal


Sender = Literal["user", "app"]
"""Who sent the message — the end user or the app itself."""

ChannelType = Literal["chat", "api", "telegram", "slack", "whatsapp"]
"""Transport the message arrived on."""


@dataclass
class Attachment:
    """File attached to a message by the end user.

    Attributes:
        name: Original filename.
        content_type: MIME type (e.g. ``"application/pdf"``).
        url: Presigned download URL (valid for 7 days).
        size: File size in bytes.
    """

    name: str
    content_type: str
    url: str
    size: int = 0

    async def download(self, path: str) -> str:
        """Download the file to a local path. Returns the path."""
        import aiohttp

        async with aiohttp.ClientSession() as http:
            async with http.get(self.url) as resp:
                resp.raise_for_status()
                with open(path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(8192):
                        f.write(chunk)
        return path

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "content_type": self.content_type,
            "url": self.url,
            "size": self.size,
        }


@dataclass
class Message:
    """A single message exchanged between user and app.

    Attributes:
        text: Message body (plain text or markdown).
        sender: ``"user"`` for inbound messages, ``"app"`` for replies.
        channel_type: Transport channel — ``"chat"``, ``"api"``,
            ``"telegram"``, ``"slack"``, or ``"whatsapp"``.
        timestamp: Unix epoch seconds (defaults to now).
        attachments: Optional list of file attachments.
    """

    text: str
    sender: Sender
    channel_type: ChannelType
    timestamp: float = field(default_factory=_time.time)
    attachments: list[Attachment] | None = None

    def to_dict(self) -> dict:
        d = {
            "text": self.text,
            "sender": self.sender,
            "channel_type": self.channel_type,
            "timestamp": self.timestamp,
        }
        if self.attachments:
            d["attachments"] = [a.to_dict() for a in self.attachments]
        return d
