"""Smart-message topics («temas»): the port every topic store implements, and the lock rules of a topic.

A topic is its own aggregate: its `messages` (the texts a click reserves, «slots») are part of it. The entity is
`letschatty.models.analytics.smart_messages.topic.Topic`, unchanged. A read by id is NOT scoped to a company: the use
case checks the company (ADR-007). A deleted topic is still returned by id.
"""
from __future__ import annotations

from typing import Any, Dict, List, Protocol

from ...models.analytics.smart_messages.topic import Topic
from ...models.analytics.smart_messages.topic_message import MessageTopic, MessageTopicStatus
from ...models.utils.types import StrObjectId


class TopicRepository(Protocol):
    """Raises `NotFoundError` when no topic has that id."""

    async def get(self, topic_id: StrObjectId) -> Topic:
        """By id, whatever its company, also a deleted one."""
        ...

    async def list_live(self, company_id: StrObjectId) -> List[Topic]:
        """Live topics of the company, whole (the texts are checked against them)."""
        ...

    async def list_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        """Live topics of the company, newest first, as JSON-ready preview dicts (with `account_id`, no `messages`)."""
        ...

    async def add(self, topic: Topic) -> Topic: ...

    async def update(self, topic_id: StrObjectId, changes: Topic) -> Topic:
        """Writes only the fields `changes` was built with, merged onto what is in the store now."""
        ...

    async def save_messages(self, topic: Topic) -> None:
        """Writes only `messages` (and `updated_at`): the lock state of a click or an incoming message. The copy may
        be a cached one, so the rest of the document is never rewritten from it."""
        ...

    async def delete(self, topic_id: StrObjectId) -> Topic:
        """Marks it deleted (the document stays) and returns it as it was before."""
        ...


def message_status(topic: Topic, message: MessageTopic) -> MessageTopicStatus:
    """Not locked = available; locked for longer than the topic's `lock_duration` = expired; else locked. A message
    marked locked without `lock_time` raises `TypeError` (comparing None), as it always did."""
    if message.is_locked:
        if message.time_locked > topic.lock_duration:
            return MessageTopicStatus.EXPIRED
        return MessageTopicStatus.LOCKED
    return MessageTopicStatus.AVAILABLE


def has_locked_messages(topic: Topic) -> bool:
    return any(message_status(topic, m) == MessageTopicStatus.LOCKED for m in topic.messages)
