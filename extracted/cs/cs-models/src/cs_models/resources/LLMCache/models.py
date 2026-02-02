from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Text,
)

from ...database import Base


class LLMCacheModel(Base):
    __tablename__ = "llm_cache"

    id = Column(Integer, primary_key=True)
    message = Column(String(191), nullable=False)
    response = Column(Text, nullable=False)
    model_name = Column(String(50), nullable=False)
    model_provider = Column(String(20), nullable=False)
    model_prompt = Column(Text, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
