from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Text,
)

from ...database import Base


class ActionLogModel(Base):
    __tablename__ = "action_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False, index=True)
    action_type = Column(String(50), nullable=False, index=True)
    endpoint = Column(String(128), nullable=False)
    payload = Column(Text, nullable=False)
    table_name = Column(String(128), nullable=True)
    table_id = Column(Integer, nullable=True)
    transformation = Column(String(50), nullable=True)
    timestamp = Column(
        DateTime,
        nullable=False,
        index=True,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
