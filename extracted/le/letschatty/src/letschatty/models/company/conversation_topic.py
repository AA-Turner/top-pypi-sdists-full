from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class TopicTimelineEntry(BaseModel):
    """
    Simple timeline entry tracking which topics were active at a specific moment.

    Topics are replaced on each user interaction. This creates a complete timeline
    of topic evolution throughout the conversation.
    """
    timestamp: datetime = Field(description="When these topics were active")
    topics: List[str] = Field(
        default_factory=list,
        description="Topic names that were active at this moment"
    )

    @classmethod
    def create(cls, topics: List[str]) -> 'TopicTimelineEntry':
        """
        Create a new timeline entry with current timestamp.

        Args:
            topics: List of topic names

        Returns:
            TopicTimelineEntry instance
        """
        from datetime import datetime
        from zoneinfo import ZoneInfo

        return cls(
            timestamp=datetime.now(tz=ZoneInfo("UTC")),
            topics=topics
        )

    @classmethod
    def empty(cls) -> 'TopicTimelineEntry':
        """
        Create empty timeline entry (no active topics).
        Used for manual cancellation.

        Returns:
            TopicTimelineEntry with empty topics
        """
        from datetime import datetime
        from zoneinfo import ZoneInfo

        return cls(
            timestamp=datetime.now(tz=ZoneInfo("UTC")),
            topics=[]
        )

    @classmethod
    def example(cls) -> dict:
        """Example timeline entry for documentation"""
        return {
            "timestamp": "2025-10-30T10:05:00Z",
            "topics": ["delivery_time", "prices"]
        }
