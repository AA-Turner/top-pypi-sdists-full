from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from datetime import datetime

from ...database import Base


class AssigneeModel(Base):
    __tablename__ = 'assignees'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    user_name = Column(String(128), nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
