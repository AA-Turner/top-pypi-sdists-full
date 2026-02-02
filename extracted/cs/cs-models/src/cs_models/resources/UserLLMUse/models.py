from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    ForeignKey,
)

from ...database import Base


class UserLLMUseModel(Base):
    __tablename__ = "user_llm_use"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False, index=True)
    user_query_id = Column(
        Integer,
        ForeignKey("assistant_user_queries.id"),
        nullable=True,
    )
    model_provider = Column(String(50), nullable=False)
    model_name = Column(String(50), nullable=False)
    input_tokens = Column(Integer, nullable=False, default=0)
    thinking_tokens = Column(Integer, nullable=False, default=0)
    output_tokens = Column(Integer, nullable=False, default=0)
    tokens_used = Column(Integer, nullable=False)
    pipeline = Column(String(50), nullable=False)
    timestamp = Column(
        DateTime,
        nullable=False,
        index=True,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
