"""Conversation shapes a head row can carry."""

from typing import Literal

# direct: one task per message on the agent; gateway: a router-era head
ConversationKind = Literal["direct", "gateway"]
