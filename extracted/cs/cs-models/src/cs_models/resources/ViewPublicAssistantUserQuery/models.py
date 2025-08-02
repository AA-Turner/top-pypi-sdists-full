from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Text,
)

from ...database import Base


class ViewPublicAssistantUserQueryModel(Base):
    __tablename__ = "_view_public_assistant_user_queries"

    id = Column(Integer, primary_key=True)
    user_query_id = Column(
        Integer,
        ForeignKey('assistant_user_queries.id'),
        nullable=False,
    )
    data = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
