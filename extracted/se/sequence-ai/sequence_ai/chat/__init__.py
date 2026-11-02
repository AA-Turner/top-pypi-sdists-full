"""chat (`/v1/chat`) — vision-language for agents: `chat()` sends messages and returns one message
(or streams it), `Conversation` keeps the history across turns, and `image()` / `cached()` build the
content blocks for an image and a prompt-cache breakpoint."""

from __future__ import annotations

from .content import cached, image
from .conversation import Conversation
from .infer import chat
from .types import ChatResult, ChatStream

__all__ = ["chat", "ChatResult", "ChatStream", "Conversation", "image", "cached"]
