from typing import List, Optional, Tuple
from datetime import datetime
from zoneinfo import ZoneInfo
import logging

from letschatty.models.chat.chat import Chat
from letschatty.models.company.conversation_topic import TopicTimelineEntry
from letschatty.models.messages.chatty_messages import ChattyMessage

logger = logging.getLogger("ConversationTopicsService")


class ConversationTopicsService:
    """
    Simple service for managing conversation topics timeline.

    Topics are stored in a timeline. Each entry represents which topics
    were active at a specific moment. The last entry is the current state.
    """

    @staticmethod
    def update_topics(
        chat: Chat,
        detected_topics: List[str]
    ) -> TopicTimelineEntry:
        """
        Update chat's topics timeline with newly detected topics.

        Simply adds a new timeline entry. Topics are replaced, not merged.

        Args:
            chat: Chat instance
            detected_topics: List of topic names detected by tagger

        Returns:
            The new timeline entry that was added
        """
        entry = TopicTimelineEntry.create(detected_topics)
        chat.topics_timeline.append(entry)

        logger.info(
            f"Updated topics for chat {chat.id}: {detected_topics} "
            f"({len(chat.topics_timeline)} timeline entries)"
        )

        return entry

    @staticmethod
    def cancel_all_topics(chat: Chat) -> TopicTimelineEntry:
        """
        Manually cancel all active topics.

        Adds an empty timeline entry to mark that all topics were cancelled.

        Args:
            chat: Chat instance

        Returns:
            The empty timeline entry that was added
        """
        entry = TopicTimelineEntry.empty()
        chat.topics_timeline.append(entry)

        logger.info(f"Cancelled all topics for chat {chat.id}")

        return entry


    @staticmethod
    def get_topics_at_time(chat: Chat, target_time: datetime) -> List[str]:
        """
        Get which topics were active at a specific point in time.

        Args:
            chat: Chat instance
            target_time: The datetime to query

        Returns:
            List of topic names active at that time
        """
        # Find the last entry before or at target_time
        for entry in reversed(chat.topics_timeline):
            if entry.timestamp <= target_time:
                return entry.topics

        return []