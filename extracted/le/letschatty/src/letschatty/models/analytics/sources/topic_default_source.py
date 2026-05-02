from __future__ import annotations
from pydantic import Field, ConfigDict

from .source_base import SourceBase
from ...utils.types.source_types import SourceType, SourceCheckerType

class TopicDefaultSource(SourceBase):
    """Default source for topic-matched messages without direct attribution"""
    topic_id: str = Field(..., description="ID of the associated topic", frozen=True)
    agent_email: str = Field(default="default_settings@letschatty.com", frozen=True)
    description: str = Field(
        default="Message matched the Topic but there was no direct source to attribute it to.",
        frozen=True
    )
    source_checker: SourceCheckerType = Field(
        default=SourceCheckerType.SMART_MESSAGES,
        frozen=True
    )
    name: str = Field(frozen=True)

    @property
    def default_category(self) -> str:
        return "Fuente para mensajes de topics sin fuente de origen"

    @property
    def type(self) -> SourceType:
        return SourceType.TOPIC_DEFAULT_SOURCE

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TopicDefaultSource):
            return False
        return self.topic_id == other.topic_id

    def __hash__(self) -> int:
        return hash(self.topic_id)

    @classmethod
    def from_topic(cls, topic_id: str, topic_name: str, default_source_id: str) -> TopicDefaultSource:
        """Create a topic default source from topic information"""
        return cls(
            id=default_source_id,
            name=f"{topic_name} Topic Default Source",
            topic_id=topic_id
        )